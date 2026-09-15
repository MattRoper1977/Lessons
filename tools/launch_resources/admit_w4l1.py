#!/usr/bin/env python3
"""CX2 §3 · stage the LAUNCH W4L1 Diffusion source admission through the existing tools
(the shape tools/grow_resources/admit_w3_friction.py and tools/rw1/admit_w8.py established).

Computes the exact replacement transaction (every protected Science path that differs
from the review base: the lesson, its native pack files and the pack records), then:

  1. declares it in _glv3/tools/verify_change_boundary.py as its own block and its own
     REPLACEMENT_TRANSACTIONS entry (previous git blob at the review base, exact bytes
     and SHA-256 after), never a directory permission;
  2. adds the members, and the review records that move with them but are not Science
     payload (the original-targets ledger), to REVIEWED_PATHS in
     tools/catalogue/pin_catalogue_contract.py so the cross-estate gate carries an
     owner-reviewed digest for each;
  3. refreshes the lesson's sha256 in tools/catalogue/TERM_AND_STYLE_EVIDENCE.json,
     re-derives assets/catalogue/lesson-order.json, data/resource-sizes.json and
     re-runs the static check;
  4. re-pins CATALOGUE_PINS in tools/verify_cross_estate_unification.py with the
     helper's own pin(); the Apps gate copy is out of this repository's scope, so a
     scratch copy stands in and the apps.json digest is restored from the committed gate;
  5. regenerates the PIN1 trigger lists with tools/pin1/derive_triggers.py --write.

    python3 tools/launch_resources/admit_w4l1.py [--check]

Review base: the Lane D foundation commit the branch was cut from (the boundary
machinery lives there). --check reports differences without writing.
"""
from pathlib import Path
import argparse, hashlib, importlib, json, re, shutil, subprocess, sys, tempfile

ROOT = Path(__file__).resolve().parents[2]
BOUNDARY = ROOT / '_glv3/tools/verify_change_boundary.py'
HELPER = ROOT / 'tools/catalogue/pin_catalogue_contract.py'
GATE = ROOT / 'tools/verify_cross_estate_unification.py'
EVIDENCE = ROOT / 'tools/catalogue/TERM_AND_STYLE_EVIDENCE.json'
REVIEW_BASE = 'acae624f34ab4b2a88903cb6ea528976b5a1e210'   # main after Friction #538 merged (CX2 §2)
PREFIXES = ('Science_Teesside/',)
LESSON = 'Science_Teesside/Launch/SCI_L_W4_L1_Diffusion.html'
# Review records that move with the transaction but are not protected Science payload.
RECORDS = ('tools/easter/SCIENCE_ORIGINAL_TARGETS.json',)
VAR, NAME, MARK = 'CX2_W4L1_REPLACEMENTS', 'Diffusion W4L1', 'DIFFUSION W4L1'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args):
    return subprocess.check_output(['git', '-C', str(ROOT), *args]).decode()


def foreign_paths():
    """Paths another declared transaction already owns (the shape
    tools/grow_resources/admit_w3_friction.py established). The sweep takes every
    protected Science path that differs from the review base; once main carries other
    transactions over Science_Teesside/ (S3's web-slides.html), a path one of those
    changed still differs from this base, and claiming it here would both record a file
    W4L1 never touched and, under the declaration-order supersession rule, strip the
    real owner of its member."""
    import importlib.util
    spec = importlib.util.spec_from_file_location('_glv3_boundary', BOUNDARY)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    # Only a path whose bytes on this tree are still the owner's declared bytes is
    # foreign. A path this branch changes again (the teaching-pack hub after GROW W3
    # Friction merged) must be claimed here, declared after the earlier owner, so
    # the declaration-order supersession rule moves it to this transaction and the
    # earlier one keeps its exactness over the members it still owns.
    foreign = set()
    for rel, owner in module.ALL_REPLACEMENTS.items():
        if owner == NAME:
            continue
        declared = module.REPLACEMENT_TRANSACTIONS[owner][1][rel]['afterSha256']
        if sha(ROOT / rel) == declared:
            foreign.add(rel)
    return foreign


def transaction():
    foreign = foreign_paths()
    files = {}
    for row in git('diff', '--name-status', REVIEW_BASE, '--').splitlines():
        kind, rel = row.split('\t', 1)
        if not rel.startswith(PREFIXES) or rel in foreign:
            continue
        assert kind == 'M', 'protected path is not a modification: ' + row
        entry = git('ls-tree', REVIEW_BASE, '--', rel).split()
        assert entry[0] == '100644' and entry[1] == 'blob', row
        path = ROOT / rel
        files[rel] = {'beforeGitBlob': entry[2], 'afterSha256': sha(path), 'bytes': path.stat().st_size}
    untracked = [r for r in git('status', '--porcelain', '--', *PREFIXES).splitlines() if r.startswith('??')]
    assert not untracked, 'untracked protected files: ' + str(untracked)
    assert LESSON in files, 'the lesson is not part of the transaction'
    return dict(sorted(files.items()))


def write_boundary(files, check):
    text = BOUNDARY.read_text()
    block = '# BEGIN %s REPLACEMENTS\n%s = %r\n# END %s REPLACEMENTS\n' % (MARK, VAR, files, MARK)
    if 'CX2_W4L1_REVIEW_BASE' not in text:
        text = text.replace('# BEGIN DECLARED TRANSACTIONS\n',
                            "# CX2 §3: the LAUNCH W4L1 Diffusion lesson with its native pack files and pack\n"
                            "# records, one transaction, written by tools/launch_resources/admit_w4l1.py.\n"
                            "CX2_W4L1_REVIEW_BASE = %r\n# BEGIN DECLARED TRANSACTIONS\n" % REVIEW_BASE, 1)
    pattern = r'# BEGIN %s REPLACEMENTS\n.*?# END %s REPLACEMENTS\n' % (MARK, MARK)
    if re.search(pattern, text, flags=re.S):
        text = re.sub(pattern, lambda _: block, text, flags=re.S)
    else:
        text = text.replace('# END DECLARED TRANSACTIONS\n', block + '# END DECLARED TRANSACTIONS\n', 1)
    entry = "    %r: (CX2_W4L1_REVIEW_BASE, %s),\n" % (NAME, VAR)
    if entry not in text:
        text = text.replace('    # END DECLARED TRANSACTION ENTRIES\n', entry + '    # END DECLARED TRANSACTION ENTRIES\n', 1)
    assert text.count(entry) == 1 and text.count('# BEGIN %s REPLACEMENTS' % MARK) == 1
    changed = text != BOUNDARY.read_text()
    if changed and check:
        raise SystemExit('[FAIL] boundary transaction differs from the tree')
    if changed:
        BOUNDARY.write_text(text)
    return changed


def extend_reviewed_paths(files, check):
    sys.path.insert(0, str(HELPER.parent))
    helper = importlib.import_module('pin_catalogue_contract')
    missing = [rel for rel in (*files, *RECORDS) if rel not in helper.REVIEWED_PATHS]
    if missing:
        if check:
            raise SystemExit('[FAIL] reviewed-path list lacks: ' + ', '.join(missing))
        text = HELPER.read_text()
        addition = ('\n\n# CX2 §3 LAUNCH W4L1 Diffusion: the lesson, its native pack files, the LAUNCH pack\n'
                    '# records and the original-targets ledger admitted as one reviewed replacement transaction.\n'
                    'REVIEWED_PATHS += (\n' + ''.join('    %r,\n' % rel for rel in missing) + ')\n')
        anchor = "\n\ndef pack_rows_for(lessons: Path, rows: list) -> list:"
        assert text.count(anchor) == 1
        HELPER.write_text(text.replace(anchor, addition + anchor))
        importlib.reload(helper)
    return missing


def refresh_evidence(check):
    data = json.loads(EVIDENCE.read_text())
    entry = data['entries'][LESSON]
    current = sha(ROOT / LESSON)
    changed = entry.get('sha256') != current
    if changed and check:
        raise SystemExit('[FAIL] evidence sha256 stale for the lesson')
    if changed:
        entry['sha256'] = current
        EVIDENCE.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n')
    return changed


def run(*cmd):
    return subprocess.run([sys.executable, *cmd], cwd=ROOT, capture_output=True, text=True)


def repin(check):
    sys.path.insert(0, str(HELPER.parent))
    helper = importlib.reload(importlib.import_module('pin_catalogue_contract'))
    committed = git('show', 'HEAD:tools/verify_cross_estate_unification.py')
    apps_digest = re.search(r'"apps\.json":\s*"([0-9a-f]{64})"', committed).group(1)
    # The stand-in's apps.json can never carry the Apps digest, so pin in write mode
    # and compare the gate bytes; --check restores the original bytes afterwards.
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


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--check', action='store_true')
    args = ap.parse_args()
    files = transaction()
    report = {'members': len(files), 'boundaryChanged': write_boundary(files, args.check),
              'reviewedPathsAdded': extend_reviewed_paths(files, args.check),
              'evidenceRefreshed': refresh_evidence(args.check)}
    steps = {}
    for label, cmd in (('resourceSizes', ('tools/ux2/resource_sizes.py', '--check' if args.check else '--write')),
                       ('lessonOrder', ('tools/catalogue/build_lesson_order.py', *(['--check'] if args.check else []))),
                       ('staticCheck', ('tools/catalogue/check_catalogue_static.py',))):
        proc = run(*cmd)
        steps[label] = proc.returncode
        report[label] = {'returncode': proc.returncode, 'tail': (proc.stdout + proc.stderr).strip()[-200:]}
    report['pin'] = repin(args.check)
    pin1 = run('tools/pin1/derive_triggers.py', '--check' if args.check else '--write')
    steps['pin1'] = pin1.returncode
    report['pin1'] = {'returncode': pin1.returncode, 'tail': (pin1.stdout + pin1.stderr).strip()[-200:]}
    print(json.dumps(report, indent=2, default=str))
    raise SystemExit(0 if all(code == 0 for code in steps.values()) else 1)
