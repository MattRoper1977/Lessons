#!/usr/bin/env python3
"""CX2 §8.3 Lane D · stage the return-week W8 admission for ONE pathway through the
existing tools (the shape tools/grow_resources/admit_w3_friction.py established).

For the pathway's lessons (BUILD: W8B; GROW: W8A, W8B; LAUNCH: W8L1, W8L2, W8L3):

  1. declare the exact replacement transaction in _glv3/tools/verify_change_boundary.py
     (previous git blob at the review base, exact bytes and SHA-256 after), as its own
     block and its own REPLACEMENT_TRANSACTIONS entry, never a directory permission;
  2. add the lesson paths to REVIEWED_PATHS in tools/catalogue/pin_catalogue_contract.py
     so the cross-estate gate carries an owner-reviewed digest for each (the boundary
     requires a matching admission for every replacement member);
  3. refresh each lesson's sha256 in tools/catalogue/TERM_AND_STYLE_EVIDENCE.json
     (the static check compares every hashed entry with the bytes on disk), re-derive
     assets/catalogue/lesson-order.json and re-run the static check;
  4. re-pin CATALOGUE_PINS in tools/verify_cross_estate_unification.py with the helper's
     own pin(); the Apps gate copy is out of this repository's scope, so a scratch copy
     stands in and the apps.json digest is restored from the committed gate;
  5. regenerate the PIN1 trigger lists with tools/pin1/derive_triggers.py --write.

    python3 tools/rw1/admit_w8.py --pathway BUILD [--check]

Review base: the origin/main commit the branch was cut from, recorded in the boundary
file as RW_W8_REVIEW_BASE. --check reports differences without writing.
"""
from pathlib import Path
import argparse, hashlib, importlib, json, re, shutil, subprocess, sys, tempfile

ROOT = Path(__file__).resolve().parents[2]
BOUNDARY = ROOT / '_glv3/tools/verify_change_boundary.py'
HELPER = ROOT / 'tools/catalogue/pin_catalogue_contract.py'
GATE = ROOT / 'tools/verify_cross_estate_unification.py'
EVIDENCE = ROOT / 'tools/catalogue/TERM_AND_STYLE_EVIDENCE.json'
REVIEW_BASE = 'ec7d34ab48eb290f9abb67b27c735b6e09b9930c'   # main after Sugar #547 merged (CX2 §4.8)

LESSONS = {
    'BUILD': ['Science_Teesside/Build/W8-W13_2026-27/SCI_B_W8B_Autumn_Science_Checkpoint_Do.html'],
    'GROW': ['Science_Teesside/Grow/W8-W13_2026-27/SCI_G_W8A_Day_And_Night_Explore.html',
             'Science_Teesside/Grow/W8-W13_2026-27/SCI_G_W8B_Day_And_Night_Do.html'],
    'LAUNCH': ['Science_Teesside/Launch/W8-W13_2026-27/SCI_L_W8L1_Enzyme_Action_Introduce.html',
               'Science_Teesside/Launch/W8-W13_2026-27/SCI_L_W8L2_Amylase_pH_Core_Practical_Explore.html',
               'Science_Teesside/Launch/W8-W13_2026-27/SCI_L_W8L3_Amylase_Rate_And_Topic_1_Do.html'],
}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args):
    return subprocess.check_output(['git', '-C', str(ROOT), *args]).decode()


def transaction(pathway):
    files = {}
    for rel in LESSONS[pathway]:
        entry = git('ls-tree', REVIEW_BASE, '--', rel).split()
        assert entry and entry[0] == '100644' and entry[1] == 'blob', rel
        path = ROOT / rel
        assert git('diff', '--name-status', REVIEW_BASE, '--', rel).startswith('M\t'), 'not a modification vs review base: ' + rel
        files[rel] = {'beforeGitBlob': entry[2], 'afterSha256': sha(path), 'bytes': path.stat().st_size}
    return dict(sorted(files.items()))


def write_boundary(pathway, files, check):
    text = BOUNDARY.read_text()
    var = 'RW_W8_%s_REPLACEMENTS' % pathway
    name = 'Return week W8 %s' % pathway
    block = ('# BEGIN RETURN WEEK W8 %s REPLACEMENTS\n%s = %r\n# END RETURN WEEK W8 %s REPLACEMENTS\n' % (pathway, var, files, pathway))
    if 'RW_W8_REVIEW_BASE' not in text:
        text = text.replace('# BEGIN DECLARED TRANSACTIONS\n',
                            "# CX2 §8.3 Lane D: the return-week W8 lessons, one transaction per pathway,\n"
                            "# written by tools/rw1/admit_w8.py.\nRW_W8_REVIEW_BASE = %r\n# BEGIN DECLARED TRANSACTIONS\n" % REVIEW_BASE, 1)
    pattern = r'# BEGIN RETURN WEEK W8 %s REPLACEMENTS\n.*?# END RETURN WEEK W8 %s REPLACEMENTS\n' % (pathway, pathway)
    if re.search(pattern, text, flags=re.S):
        text = re.sub(pattern, lambda _: block, text, flags=re.S)
    else:
        text = text.replace('# END DECLARED TRANSACTIONS\n', block + '# END DECLARED TRANSACTIONS\n', 1)
    entry = "    %r: (RW_W8_REVIEW_BASE, %s),\n" % (name, var)
    if entry not in text:
        text = text.replace('    # END DECLARED TRANSACTION ENTRIES\n', entry + '    # END DECLARED TRANSACTION ENTRIES\n', 1)
    assert text.count(entry) == 1 and text.count('# BEGIN RETURN WEEK W8 %s REPLACEMENTS' % pathway) == 1
    changed = text != BOUNDARY.read_text()
    if changed and check:
        raise SystemExit('[FAIL] boundary transaction for %s differs from the tree' % pathway)
    if changed:
        BOUNDARY.write_text(text)
    return changed


def extend_reviewed_paths(files, check):
    sys.path.insert(0, str(HELPER.parent))
    helper = importlib.import_module('pin_catalogue_contract')
    missing = [rel for rel in files if rel not in helper.REVIEWED_PATHS]
    if missing:
        if check:
            raise SystemExit('[FAIL] reviewed-path list lacks: ' + ', '.join(missing))
        text = HELPER.read_text()
        addition = ('\n\n# CX2 §8.3 Lane D: return-week W8 lessons admitted as reviewed replacement transactions.\n'
                    'REVIEWED_PATHS += (\n' + ''.join('    %r,\n' % rel for rel in missing) + ')\n')
        anchor = "\n\ndef pack_rows_for(lessons: Path, rows: list) -> list:"
        assert text.count(anchor) == 1
        HELPER.write_text(text.replace(anchor, addition + anchor))
        importlib.reload(helper)
    return missing


def refresh_evidence(files, check):
    data = json.loads(EVIDENCE.read_text())
    changed = []
    for rel in files:
        entry = data['entries'][rel]
        current = sha(ROOT / rel)
        if entry.get('sha256') != current:
            changed.append(rel)
            entry['sha256'] = current
    if changed and check:
        raise SystemExit('[FAIL] evidence sha256 stale for: ' + ', '.join(changed))
    if changed:
        EVIDENCE.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n')
    return changed


def run(*cmd):
    return subprocess.run([sys.executable, *cmd], cwd=ROOT, capture_output=True, text=True)


def repin(check):
    sys.path.insert(0, str(HELPER.parent))
    helper = importlib.reload(importlib.import_module('pin_catalogue_contract'))
    committed = git('show', 'HEAD:tools/verify_cross_estate_unification.py')
    apps_digest = re.search(r'"apps\.json":\s*"([0-9a-f]{64})"', committed).group(1)
    # The stand-in's apps.json can never carry the Apps repository's digest, so the
    # helper's own check mode would always report the manifest pin as moved. --check
    # therefore pins in write mode, compares the gate bytes (apps digest put back) and
    # restores the original bytes; a differing gate is the finding check mode exists for.
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
    ap.add_argument('--pathway', required=True, choices=sorted(LESSONS))
    ap.add_argument('--check', action='store_true')
    args = ap.parse_args()
    files = transaction(args.pathway)
    report = {'pathway': args.pathway, 'members': list(files),
              'boundaryChanged': write_boundary(args.pathway, files, args.check),
              'reviewedPathsAdded': extend_reviewed_paths(files, args.check),
              'evidenceRefreshed': refresh_evidence(files, args.check)}
    order = run('tools/catalogue/build_lesson_order.py', *(['--check'] if args.check else []))
    report['lessonOrder'] = {'returncode': order.returncode, 'tail': (order.stdout + order.stderr).strip()[-200:]}
    static = run('tools/catalogue/check_catalogue_static.py')
    report['staticCheck'] = {'returncode': static.returncode, 'tail': (static.stdout + static.stderr).strip()[-160:]}
    report['pin'] = repin(args.check)
    pin1 = run('tools/pin1/derive_triggers.py', '--check' if args.check else '--write')
    report['pin1'] = {'returncode': pin1.returncode, 'tail': (pin1.stdout + pin1.stderr).strip()[-200:]}
    print(json.dumps(report, indent=2, default=str))
    raise SystemExit(0 if (order.returncode == 0 and static.returncode == 0 and pin1.returncode == 0) else 1)
