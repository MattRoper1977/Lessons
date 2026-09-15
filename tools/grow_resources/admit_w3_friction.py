"""Stage the EDU-Q1 GROW W3 Friction source admission through the existing tools.

Computes the exact replacement transaction (every protected Science path that
differs from the review base), then:

  1. writes the GROW W3 block in _glv3/tools/verify_change_boundary.py
     (previous git blob at the merge base, exact bytes and SHA-256 after);
  2. appends any newly reviewed paths to REVIEWED_PATHS in
     tools/catalogue/pin_catalogue_contract.py;
  3. re-pins CATALOGUE_PINS in tools/verify_cross_estate_unification.py with that
     helper's own pin(); the Apps gate copy is out of this repository's scope, so
     a scratch copy stands in for it and the apps.json digest is restored unchanged;
  4. regenerates the PIN1 trigger lists with tools/pin1/derive_triggers.py --write.

Run after every content, record and derived file is final.

    python3 tools/grow_resources/admit_w3_friction.py [--check]
"""
from pathlib import Path
import argparse, hashlib, json, re, shutil, subprocess, sys, tempfile

ROOT = Path(__file__).resolve().parents[2]
BASE = '929cf731173aeca8c9941cecd76cb350387499d1'
BOUNDARY = ROOT / '_glv3/tools/verify_change_boundary.py'
HELPER = ROOT / 'tools/catalogue/pin_catalogue_contract.py'
GATE = ROOT / 'tools/verify_cross_estate_unification.py'
PREFIXES = ('Science_Teesside/',)
# Review records that move with the transaction but are not protected Science
# payload: the original-targets ledger carries the patched lesson's SHA-256 and
# the GROW resource content is the source the resource pages are built from.
# Neither is served as a studio, so they stay out of the GLV3 replacement block,
# but the cross-estate boundary reds on any modified file it does not pin --
# so they are admitted by exact digest through REVIEWED_PATHS like every other
# reviewed record (BUILD_QA.json, TERM_AND_STYLE_EVIDENCE.json).
RECORDS = ('tools/easter/SCIENCE_ORIGINAL_TARGETS.json', 'tools/grow_resources/CONTENT.json')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args):
    return subprocess.check_output(['git', '-C', str(ROOT), *args]).decode()


def transaction():
    status = git('diff', '--name-status', BASE, '--')
    files = {}
    for row in status.splitlines():
        kind, rel = row.split('\t', 1)
        if not rel.startswith(PREFIXES):
            continue
        assert kind == 'M', 'protected path is not a modification: ' + row
        entry = git('ls-tree', BASE, '--', rel).split()
        assert entry[0] == '100644' and entry[1] == 'blob', row
        path = ROOT / rel
        files[rel] = {'beforeGitBlob': entry[2], 'afterSha256': sha(path), 'bytes': path.stat().st_size}
    untracked = [r for r in git('status', '--porcelain', '--', *PREFIXES).splitlines() if r.startswith('??')]
    assert not untracked, 'untracked protected files: ' + str(untracked)
    return dict(sorted(files.items()))


def write_boundary(files, check):
    text = BOUNDARY.read_text()
    block = '# BEGIN GROW W3 REPLACEMENTS\nGROW_W3_REPLACEMENTS = ' + repr(files) + '\n# END GROW W3 REPLACEMENTS'
    patched, count = re.subn(r'# BEGIN GROW W3 REPLACEMENTS\n.*?# END GROW W3 REPLACEMENTS', lambda _: block, text, flags=re.S)
    assert count == 1
    if patched != text:
        if check:
            raise SystemExit('[FAIL] GROW W3 replacement block differs from the tree')
        BOUNDARY.write_text(patched)
    return patched != text


def extend_reviewed_paths(files, check):
    sys.path.insert(0, str(HELPER.parent))
    import importlib
    helper = importlib.import_module('pin_catalogue_contract')
    missing = [rel for rel in (*files, *RECORDS) if rel not in helper.REVIEWED_PATHS]
    if missing:
        if check:
            raise SystemExit('[FAIL] reviewed-path list lacks: ' + ', '.join(missing))
        text = HELPER.read_text()
        addition = ('\n\n# EDU-Q1 GROW W3 Friction: the paired lesson, its resource pages, the Week 3\n'
                    '# pack records, the original-targets ledger and the GROW resource content\n'
                    '# admitted as one reviewed replacement transaction.\nREVIEWED_PATHS += (\n'
                    + ''.join(f'    {rel!r},\n' for rel in missing) + ')\n')
        anchor = "\n\ndef pack_rows_for(lessons: Path, rows: list) -> list:"
        assert text.count(anchor) == 1
        HELPER.write_text(text.replace(anchor, addition + anchor))
        importlib.reload(helper)
    return missing


def repin(check):
    sys.path.insert(0, str(HELPER.parent))
    import importlib
    helper = importlib.reload(importlib.import_module('pin_catalogue_contract'))
    # The apps.json pin belongs to the Apps repository; take it from the committed
    # gate so a stand-in never leaks into the Lessons copy.
    committed = git('show', 'HEAD:tools/verify_cross_estate_unification.py')
    apps_digest = re.search(r'"apps\.json":\s*"([0-9a-f]{64})"', committed).group(1)
    # The stand-in's apps.json can never carry the Apps repository's digest, so
    # the helper's own check mode would always report the manifest pin as moved.
    # --check therefore pins in write mode and compares the gate file before and
    # after (with the apps.json digest put back), then restores the original bytes:
    # a differing gate is the same finding the helper's check mode exists to raise.
    before = GATE.read_bytes()
    with tempfile.TemporaryDirectory(prefix='apps-gate-stand-in-') as temp:
        apps = Path(temp); (apps / 'tools').mkdir()
        shutil.copyfile(GATE, apps / 'tools/verify_cross_estate_unification.py')
        (apps / 'apps.json').write_bytes(b'{}')
        try:
            result = helper.pin(ROOT, apps, check=False)
        except ValueError as exc:
            raise SystemExit('[FAIL] ' + str(exc))
    after = GATE.read_text()
    after, count = re.subn(r'("apps\.json":\s*")[0-9a-f]{64}(")', lambda m: m[1] + apps_digest + m[2], after)
    assert count == 1
    if check:
        GATE.write_bytes(before)
        if after.encode() != before:
            raise SystemExit('[FAIL] reviewed catalogue pins differ from the tree; re-run without --check')
        result['mode'] = 'check'
    else:
        GATE.write_text(after)
    return result


def triggers(check):
    return subprocess.run([sys.executable, str(ROOT / 'tools/pin1/derive_triggers.py'), '--check' if check else '--write'],
                          cwd=ROOT, capture_output=True, text=True)


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--check', action='store_true')
    args = ap.parse_args()
    files = transaction()
    report = {'members': len(files), 'boundaryChanged': write_boundary(files, args.check),
              'reviewedPathsAdded': extend_reviewed_paths(files, args.check)}
    report['pin'] = repin(args.check)
    pin1 = triggers(args.check)
    report['pin1'] = {'returncode': pin1.returncode, 'tail': (pin1.stdout + pin1.stderr).strip()[-400:]}
    print(json.dumps(report, indent=2))
    raise SystemExit(0 if pin1.returncode == 0 else 1)
