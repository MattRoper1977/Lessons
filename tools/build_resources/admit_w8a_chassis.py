#!/usr/bin/env python3
"""D-1 · stage the BUILD W8A chassis port's record moves through the existing tools
(the shape tools/launch_resources/admit_w4l1.py and tools/grow_resources/admit_w3_friction.py
established). Every digest below is computed from the bytes on disk; none is typed.

Computes the exact replacement transaction (every protected Science path that differs from
the review base: the ported lesson and the pack checksum file that names it), then:

  0. refreshes the pack's SHA256SUMS.txt rows in place with tools/easter/refresh_pack_checksums.py
     (existing rows only; the tool recomputes every row it already has, so the three rows that
     were already stale on main — W8B, W11A and manifest.json — move with the lesson's);
  1. declares the transaction in _glv3/tools/verify_change_boundary.py as its own block and its
     own REPLACEMENT_TRANSACTIONS entry (previous git blob at the review base, exact bytes and
     SHA-256 after), never a directory permission; declared last, so the supersession rule
     moves the lesson path from the Sugar R10 hygiene transaction to this one;
  2. adds any member not yet reviewed to REVIEWED_PATHS in tools/catalogue/pin_catalogue_contract.py;
  3. refreshes the lesson's sha256 in tools/catalogue/TERM_AND_STYLE_EVIDENCE.json (the entry's
     quote, chassis and Lundy evidence are unchanged by the port; build_catalogue.py is not the
     instrument here because it re-derives every entry and moves unrelated rows), re-derives
     data/chassis-census.json, data/resource-sizes.json and assets/catalogue/lesson-order.json,
     and re-runs the static check;
  4. re-pins CATALOGUE_PINS in both gate copies with the helper's own pin(), against the Apps
     tree given by --apps (the Lessons gate is copied over the Apps copy first: pin() refuses
     when the two differ);
  5. wires the census gate into .github/workflows/mbm-cross-estate-unification.yml -- the workflow
     the lesson path already triggers -- as `chassis_census.py --self-test` then `--check --gate`,
     and adds the checker to PIN1's non-digest dependencies; without a RUNNING --gate the shell this
     port fixes can regress on main and the run still exits 0;
  6. regenerates the PIN1 trigger lists with tools/pin1/derive_triggers.py --write.

    python3 tools/build_resources/admit_w8a_chassis.py --apps <apps checkout> [--check]

Review base: main at 48c2ecb9, the commit the D-1 branch was cut from. --check reports differences
without writing ANYTHING, in this repository or in the Apps checkout given by --apps.
"""
from pathlib import Path
import argparse, hashlib, importlib, json, os, re, shutil, subprocess, sys

ROOT = Path(__file__).resolve().parents[2]
BOUNDARY = ROOT / '_glv3/tools/verify_change_boundary.py'
HELPER = ROOT / 'tools/catalogue/pin_catalogue_contract.py'
GATE_REL = 'tools/verify_cross_estate_unification.py'
GATE = ROOT / GATE_REL
EVIDENCE = ROOT / 'tools/catalogue/TERM_AND_STYLE_EVIDENCE.json'
REVIEW_BASE = '48c2ecb9ab19f238cdbe5443196935a5c45f375b'   # main after #563 (R10 estate sweep), the D-1 branch point
PREFIXES = ('Science_Teesside/',)
LESSON = 'Science_Teesside/Build/W8-W13_2026-27/SCI_B_W8A_Sugar_Labels_Explore.html'
# The chassis census record moves with this transaction and had no admission anywhere: it was ADDED
# by 03c46e53 and never modified since, and --diff-filter=MRD cannot see an addition, so this branch
# is the first change the cross-estate boundary can see. Admitting it as a REVIEWED path is what the
# other records of this transaction already do -- it lands in CATALOGUE_PINS['files'] with its
# digest, which admits it in boundary_errors() and, because PIN1 derives its triggers from that same
# registry, also puts it in both paths: filters. Nothing is widened: the digest still has to be
# re-pinned on every future refresh.
RECORDS = ('data/chassis-census.json',)
STATIC_RESULTS = ROOT / 'tools/catalogue/STATIC_CHECK_RESULTS.json'
PIN1 = ROOT / 'tools/pin1/derive_triggers.py'
WORKFLOW = ROOT / '.github/workflows/mbm-cross-estate-unification.yml'
CENSUS_STEP = '''
      - name: Verify the taught-lesson chassis census and the declared classroom shells
        shell: bash
        run: |
          set -euo pipefail
          # Lessons only; resources.json is this estate's marker, as in the step above.
          # --check proves the record is fresh. --gate is the verdict that carries D-1: without
          # it a declared lesson that leaves the classroom shell prints RED and still exits 0.
          if [ -f resources.json ]; then
            python tools/chassis_census.py --self-test
            python tools/chassis_census.py --check --gate
          fi
'''
VAR, NAME, MARK, BASEVAR = 'BUILD_W8A_CHASSIS_REPLACEMENTS', 'BUILD W8A chassis', 'BUILD W8A CHASSIS', 'BUILD_W8A_CHASSIS_REVIEW_BASE'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args):
    return subprocess.check_output(['git', '-C', str(ROOT), *args]).decode()


def run(*cmd):
    return subprocess.run([sys.executable, *cmd], cwd=ROOT, capture_output=True, text=True)


def foreign_paths():
    """Paths another declared transaction already owns and whose bytes on this tree are still
    that owner's declared bytes. A path this branch changes again (the lesson, owned by the
    Sugar R10 hygiene transaction) is not foreign: it is claimed here, declared after the
    earlier owner, so the declaration-order supersession rule moves it to this transaction."""
    import importlib.util
    spec = importlib.util.spec_from_file_location('_glv3_boundary', BOUNDARY)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    foreign = set()
    for rel, owner in module.ALL_REPLACEMENTS.items():
        if owner == NAME:
            continue
        declared = module.REPLACEMENT_TRANSACTIONS[owner][1][rel]['afterSha256']
        if (ROOT / rel).is_file() and sha(ROOT / rel) == declared:
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


def pack_checksums(check):
    proc = run('tools/easter/refresh_pack_checksums.py', *(['--check'] if check else []), LESSON)
    return {'returncode': proc.returncode, 'tail': (proc.stdout + proc.stderr).strip()[-400:]}


def write_boundary(files, check):
    text = BOUNDARY.read_text()
    block = '# BEGIN %s REPLACEMENTS\n%s = %r\n# END %s REPLACEMENTS\n' % (MARK, VAR, files, MARK)
    if BASEVAR not in text:
        text = text.replace('# BEGIN DECLARED TRANSACTIONS\n',
                            "# D-1: the BUILD W8A Sugar Evidence lesson re-dressed on the classroom chassis and the\n"
                            "# pack checksum file that names it, one transaction, written by\n"
                            "# tools/build_resources/admit_w8a_chassis.py.\n"
                            "%s = %r\n# BEGIN DECLARED TRANSACTIONS\n" % (BASEVAR, REVIEW_BASE), 1)
    pattern = r'# BEGIN %s REPLACEMENTS\n.*?# END %s REPLACEMENTS\n' % (MARK, MARK)
    if re.search(pattern, text, flags=re.S):
        text = re.sub(pattern, lambda _: block, text, flags=re.S)
    else:
        text = text.replace('# END DECLARED TRANSACTIONS\n', block + '# END DECLARED TRANSACTIONS\n', 1)
    entry = "    %r: (%s, %s),\n" % (NAME, BASEVAR, VAR)
    if entry not in text:
        text = text.replace('    # END DECLARED TRANSACTION ENTRIES\n', entry + '    # END DECLARED TRANSACTION ENTRIES\n', 1)
    assert text.count(entry) == 1 and text.count('# BEGIN %s REPLACEMENTS' % MARK) == 1 and text.count(BASEVAR + ' = ') == 1
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
        addition = ('\n\n# D-1 BUILD W8A chassis: the pack checksum file that names the re-dressed lesson,\n'
                    '# admitted with it as one reviewed replacement transaction.\n'
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


def wire_census(check):
    """The census gate has to RUN somewhere or the shell it proves can regress silently on main.
    Adds the step to the workflow this lesson path already triggers (and which already installs
    lxml), and adds the checker itself to PIN1's non-digest dependencies so an edit to the checker
    also fires the workflow. The record's own trigger comes free with its CATALOGUE_PINS admission."""
    changed = []
    text = WORKFLOW.read_text()
    if CENSUS_STEP not in text:
        anchor = '\n      - name: Preserve the PIN1 trigger-versus-assertion census\n'
        assert text.count(anchor) == 1, 'workflow anchor is not unique'
        text = text.replace(anchor, CENSUS_STEP + anchor, 1)
        assert text.count(CENSUS_STEP) == 1
        changed.append('workflowStep')
        if not check:
            WORKFLOW.write_text(text)
    pin1 = PIN1.read_text()
    if "'tools/chassis_census.py'" not in pin1:
        anchor = "    'tools/pin1/derive_triggers.py', 'tools/pin1/test_derive_triggers.py',\n"
        assert pin1.count(anchor) == 1, 'PIN1 CHECKER_PATHS anchor is not unique'
        pin1 = pin1.replace(anchor, anchor + "    # D-1: the shell census gate runs in this workflow, so an edit to the checker fires it.\n"
                                             "    'tools/chassis_census.py',\n", 1)
        changed.append('pin1CheckerPath')
        if not check:
            PIN1.write_text(pin1)
    if changed and check:
        raise SystemExit('[FAIL] the chassis census is not wired into CI: ' + ', '.join(changed))
    return changed


def repin(apps, check):
    sys.path.insert(0, str(HELPER.parent))
    helper = importlib.reload(importlib.import_module('pin_catalogue_contract'))
    apps_gate = apps / GATE_REL
    if not (apps / 'apps.json').is_file() or not apps_gate.is_file():
        raise SystemExit('[FAIL] --apps must be an Apps checkout carrying apps.json and ' + GATE_REL)
    # pin() refuses when the two gate copies differ; the Lessons copy is the reviewed one. Under
    # --check nothing is written into the Apps tree: a difference is reported, not repaired, because
    # a --check that writes into two repositories cannot audit a tree you do not want mutated.
    if check:
        if GATE.read_bytes() != apps_gate.read_bytes():
            raise SystemExit('[FAIL] the two gate copies differ; run without --check to reconcile')
    else:
        shutil.copyfile(GATE, apps_gate)
    try:
        return helper.pin(ROOT, apps, check=check)
    except ValueError as exc:
        raise SystemExit('[FAIL] ' + str(exc))


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--apps', type=Path, required=True, help='the Apps checkout whose gate copy is re-pinned alongside')
    ap.add_argument('--check', action='store_true')
    args = ap.parse_args()
    report = {'packChecksums': pack_checksums(args.check)}
    files = transaction()
    report.update({'members': files, 'boundaryChanged': write_boundary(files, args.check),
                   'reviewedPathsAdded': extend_reviewed_paths(files, args.check),
                   'evidenceRefreshed': refresh_evidence(args.check),
                   'ciWiring': wire_census(args.check)})
    for label, cmd in (('chassisCensus', ('tools/chassis_census.py', *(['--check', '--gate'] if args.check else ['--write', '--gate']))),
                       ('resourceSizes', ('tools/ux2/resource_sizes.py', '--check' if args.check else '--write')),
                       ('lessonOrder', ('tools/catalogue/build_lesson_order.py', *(['--check'] if args.check else []))),
                       ('staticCheck', ('tools/catalogue/check_catalogue_static.py',))):
        # check_catalogue_static.py has no --check and always rewrites its own record, so under
        # --check the bytes are snapshotted and put back, and the report says whether it would move.
        snapshot = None
        if label == 'staticCheck' and args.check and STATIC_RESULTS.is_file():
            stat = STATIC_RESULTS.stat()
            snapshot = (STATIC_RESULTS.read_bytes(), (stat.st_atime, stat.st_mtime))
        proc = run(*cmd)
        report[label] = {'returncode': proc.returncode, 'tail': (proc.stdout + proc.stderr).strip()[-200:]}
        if snapshot is not None:
            data, times = snapshot
            report[label]['wouldRewriteRecord'] = STATIC_RESULTS.read_bytes() != data
            STATIC_RESULTS.write_bytes(data)   # bytes AND timestamps back, so --check leaves no trace
            os.utime(STATIC_RESULTS, times)
    report['pins'] = repin(args.apps.resolve(), args.check)
    proc = run('tools/pin1/derive_triggers.py', '--check' if args.check else '--write')
    report['pin1'] = {'returncode': proc.returncode, 'tail': (proc.stdout + proc.stderr).strip()[-200:]}
    failed = [k for k, v in report.items() if isinstance(v, dict) and v.get('returncode')]
    report['status'] = 'FAIL' if failed else 'PASS'
    print(json.dumps(report, indent=2))
    raise SystemExit(1 if failed else 0)
