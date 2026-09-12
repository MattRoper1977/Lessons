#!/usr/bin/env python3
"""tools/gc1/check_sb3_parents.py - D43: a block's referrer must be its parent.

WHY SCHEMA VALIDITY IS NOT ENOUGH

`scratch-parser` answers one question: is this project.json shaped like a Scratch
3 project? It is the right question and the wrong one to stop at. A project can
satisfy the schema completely while its block graph is internally inconsistent,
because the schema constrains the SHAPE of each block and never cross-checks the
two directions of a link.

In a .sb3 every block carries `next`, `parent`, and `inputs` that may name another
block. Those are two-way: if A lists B as its `next`, or embeds B in an input,
then B must name A as its `parent`. Nothing in the schema says so. So a block can
be referenced by another block and still record `"parent": null`, and every
validator that only reads the schema will call the project fine.

The superseded Weeks 7-8 pack carried exactly one such link per project. The
revision carries none. That is a real defect that the instrument in use could not
see, which is why this exists.

THE PATTERN THIS IS THE FOURTH INSTANCE OF, AND THE FOURTH WAS THIS FILE

Four instruments this week reported a result they were not able to measure:

  - basename keying said 17 of 42 payloads mismatched, because originals and
    re-cuts share basenames and it was comparing across packages;
  - the detached-clone read said 25 of 42 decks failed the third-party gate,
    because a detached clone has no layout so innerText silently degrades to
    textContent and swallowed every <script> body;
  - the schema validator said the block graph was fine, because the schema has
    nothing to say about it;
  - and the first draft of THIS file reported a bad link in the revised pack,
    because it built one block map for the whole project. Block ids are unique
    per target, not per project, and these packs restart at k1 in every sprite:
    eleven ids appear in both Player and Hazard in W07_Bug_Hunt. Player's k11 was
    being judged against Hazard's k11's parent. It would have been a STOP on a
    sound pack, produced by the module written to prevent exactly that.

Each was a verdict from an instrument that could not observe the property it was
reporting on. So per D28 this ships with BOTH controls: a real run over the
estate, and a planted null parent on a copy proving the check fires -- plus a
self-test fixture of two sprites sharing block ids, which is the shape that caught
this module out.

USAGE
  python3 tools/gc1/check_sb3_parents.py <dir> [<dir> ...]
  python3 tools/gc1/check_sb3_parents.py --self-test
  python3 tools/gc1/check_sb3_parents.py --red-proof <sb3>   plant, prove, discard

SB1 additive modes (the original parent-only commands stay separate):
  --schema --registry <pinned-builder-registry> --report <json>
  --schema-self-test <genuine-sb3>
Schema mode: exit 0 all Scratch 3; 1 invalid project; 2 UNMEASURED.
It never asserts program behaviour or repairs a deliberately seeded lesson fault.

Exit 0 clean, 1 if any link is inconsistent, 2 on a usage error.
"""
import argparse
import glob
import json
import os
import sys
import zipfile
import subprocess
import re
from pathlib import Path


# SB1: schema is additive. The original graph functions and their controls below
# remain independent; valid projects may deliberately contain behavioural faults.
SCHEMA_RUNTIME = Path(__file__).resolve().parent / 'schema-runtime/node_modules/scratch-parser'
SCHEMA_BRIDGE = r'''
const fs = require('fs');
let parser;
try {
  if (require(process.argv[1] + '/package.json').version !== '6.0.1') throw Error('Unexpected parser version');
  parser = require(process.argv[1]);
} catch (e) { console.log(JSON.stringify({unmeasured:String(e)})); process.exit(2); }
(async () => {
  const paths = JSON.parse(fs.readFileSync(0, 'utf8'));
  const rows = [];
  for (const path of paths) {
    let bytes;
    try { bytes = fs.readFileSync(path); }
    catch (e) { rows.push({path, status:'UNMEASURED', reason:String(e)}); continue; }
    rows.push(await new Promise(resolve => {
      try {
        parser(bytes, false, (err, result) => {
          if (err) return resolve({path, status:'FAIL', reason:JSON.stringify(err)});
          if (!result || !result[0]) return resolve({path, status:'UNMEASURED', reason:'No parsed project'});
          const version = result[0].projectVersion;
          resolve({path, status:version === 3 ? 'PASS' : 'FAIL',
            reason:version === 3 ? 'Official Scratch 3 schema accepted' : 'Expected Scratch 3; got ' + version});
        });
      } catch (e) { resolve({path, status:'UNMEASURED', reason:String(e)}); }
    }));
  }
  console.log(JSON.stringify({parser_version:'6.0.1', rows}));
})().catch(e => {console.log(JSON.stringify({unmeasured:String(e)}));process.exitCode=2;});
'''


def schema_check(paths, runtime=SCHEMA_RUNTIME, node='node'):
    """Official parser only. Exit 2 is unavailable evidence, never invalid schema."""
    paths = [str(Path(p).resolve()) for p in paths]
    if not paths:
        return {'status': 'UNMEASURED', 'reason': 'No Scratch files to measure', 'rows': []}, 2
    try:
        run = subprocess.run([node, '-e', SCHEMA_BRIDGE, str(runtime)],
                             input=json.dumps(paths), text=True, capture_output=True, timeout=60)
        value = json.loads(run.stdout)
        if run.returncode or not isinstance(value, dict) or value.get('parser_version') != '6.0.1':
            raise ValueError('Parser unavailable or unexpected response: ' + run.stdout[:1500])
        rows = value['rows']
        if [r['path'] for r in rows] != paths or any(r['status'] not in {'PASS', 'FAIL', 'UNMEASURED'} for r in rows):
            raise ValueError('Parser response does not cover the exact requested population')
        code = 2 if any(r['status'] == 'UNMEASURED' for r in rows) else 1 if any(r['status'] == 'FAIL' for r in rows) else 0
        value['status'] = {0: 'PASS', 1: 'FAIL', 2: 'UNMEASURED'}[code]
        return value, code
    except (OSError, subprocess.SubprocessError, ValueError, KeyError, TypeError) as error:
        return {'status': 'UNMEASURED', 'reason': str(error), 'rows': []}, 2


def publisher_ref(root):
    text = (root / '.github/workflows/education-pages.yml').read_text()
    uses = re.findall(r'^\s*uses: MattRoper1977/mattroper1977.github.io/\.github/workflows/education-publication.yml@([0-9a-f]{40})\s*$', text, re.M)
    refs = re.findall(r'^\s*builder_ref: ([0-9a-f]{40})\s*$', text, re.M)
    if len(uses) != 1 or refs != uses:
        raise ValueError('Cannot derive one matching immutable publisher and builder ref')
    return refs[0]


def schema_population(root, registry):
    """All tracked SB3s, a conservative superset of this repo's admitted SB3s.

    Registry rows are NOT digest-checked here: that independent admission gate
    must not mask the schema diagnosis on an unreviewed test fixture.
    """
    def unique_pairs(items):
        out = {}
        for key, value in items:
            if key in out:
                raise ValueError('Duplicate registry key: ' + key)
            out[key] = value
        return out
    value = json.loads(registry.read_text(), object_pairs_hook=unique_pairs)
    if value.get('schemaVersion') != 1 or set(value.get('trees', {})) != {'education-site', 'education-lessons', 'education-apps'}:
        raise ValueError('Unsupported or incomplete admission registry')
    admitted = {p: d for p, d in value['trees']['education-lessons'].items() if p.lower().endswith('.sb3')}
    tracked = subprocess.check_output(['git', '-C', str(root), 'ls-files', '-z'], text=True).split('\0')
    tracked = {p for p in tracked if p.lower().endswith('.sb3')}
    absent_arriving, paths = [], []
    for relative in sorted(tracked | set(admitted)):
        path = root / relative
        if Path(relative).is_absolute() or '..' in Path(relative).parts or path.is_symlink() or not path.resolve().is_relative_to(root):
            raise ValueError('Unsafe Scratch input: ' + relative)
        if not path.is_file():
            if relative not in tracked and isinstance(admitted.get(relative), list) and 'ARRIVING' in admitted[relative]:
                absent_arriving.append(relative)
                continue
            raise ValueError('Missing Scratch input: ' + relative)
        if relative not in tracked:
            raise ValueError('Admitted Scratch input is not tracked: ' + relative)
        paths.append(path)
    return paths, {'tracked': len(tracked), 'registered': len(admitted),
                   'registered_present': len(set(admitted) & tracked),
                   'source_only': sorted(tracked - set(admitted)), 'absent_arriving': absent_arriving}


def schema_run(root, registry, report_path):
    from datetime import datetime, timezone
    try:
        import hashlib
        ref = publisher_ref(root)
        builder_head = subprocess.check_output(['git', '-C', str(registry.parent), 'rev-parse', 'HEAD'], text=True).strip()
        committed_registry = subprocess.check_output(['git', '-C', str(registry.parent), 'show',
                                                     ref + ':domain-split/education-publication-admission.json'])
        if builder_head != ref or registry.read_bytes() != committed_registry:
            raise ValueError('Registry must be unchanged bytes from the caller-pinned builder checkout')
        paths, population = schema_population(root, registry)
        report, code = schema_check(paths)
        report['population'] = population
        report['source_sha'] = subprocess.check_output(['git', '-C', str(root), 'rev-parse', 'HEAD'], text=True).strip()
        report['publisher_ref'] = ref
        report['registry_sha256'] = hashlib.sha256(committed_registry).hexdigest()
        for row in report['rows']:
            row['path'] = Path(row['path']).relative_to(root).as_posix()
    except (OSError, ValueError, KeyError, TypeError, AttributeError, subprocess.SubprocessError) as error:
        report, code = {'status': 'UNMEASURED', 'reason': str(error), 'rows': []}, 2
    report['measured_at'] = datetime.now(timezone.utc).isoformat()
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))
    return code


def schema_self_test(genuine):
    """Real parser controls on temporary archives, no production files changed."""
    import tempfile
    controls = []
    def want(name, paths, expected, **kwargs):
        result, code = schema_check(paths, **kwargs)
        controls.append({'name': name, 'expected_exit': expected, 'exit': code,
                         'pass': code == expected, 'result': result})
    with tempfile.TemporaryDirectory(prefix='sb1-schema-controls-') as temp:
        temp = Path(temp)
        want('genuine project', [genuine], 0)
        with zipfile.ZipFile(genuine) as archive:
            payload = {name: archive.read(name) for name in archive.namelist()}
        for name, replacement in [('missing-project-json', None), ('corrupt-json', b'{broken'),
                                  ('invalid-schema', b'{}'), ('scratch-2', b'{"objName":"Stage"}')]:
            path = temp / (name + '.sb3')
            with zipfile.ZipFile(path, 'w', zipfile.ZIP_DEFLATED) as archive:
                for member, data in payload.items():
                    if member != 'project.json': archive.writestr(member, data)
                if replacement is not None: archive.writestr('project.json', replacement)
            # Assert the mutation landed before invoking the gate.
            with zipfile.ZipFile(path) as archive:
                assert ('project.json' not in archive.namelist()) if replacement is None else archive.read('project.json') == replacement
            want(name, [path], 1)
        want('no inputs', [], 2)
        want('missing input', [temp / 'absent.sb3'], 2)
        want('missing parser', [genuine], 2, runtime=temp / 'absent-module')
        want('missing Node', [genuine], 2, node=str(temp / 'absent-node'))
        # Population controls: newly added files cannot hide behind the registry,
        # and a tracked missing file is not silently treated as absent ARRIVING.
        fixture = temp / 'population'
        fixture.mkdir()
        subprocess.run(['git', 'init', '-q', str(fixture)], check=True)
        project = fixture / 'new-unit.SB3'
        project.write_bytes(Path(genuine).read_bytes())
        subprocess.run(['git', '-C', str(fixture), 'add', project.name], check=True)
        registry = temp / 'registry.json'
        registry.write_text(json.dumps({'schemaVersion': 1, 'trees': {
            'education-site': {}, 'education-lessons': {}, 'education-apps': {}}}))
        paths, population = schema_population(fixture, registry)
        controls.append({'name': 'new unregistered uppercase SB3 is measured',
                         'pass': paths == [project] and population['source_only'] == [project.name]})
        project.unlink()
        caught = False
        try:
            schema_population(fixture, registry)
        except ValueError as error:
            caught = 'Missing Scratch input' in str(error)
        controls.append({'name': 'tracked missing SB3 cannot disappear from census', 'pass': caught})
    for row in controls:
        print(json.dumps(row))
    print('Schema controls: %d/%d PASS' % (sum(r['pass'] for r in controls), len(controls)))
    return 0 if all(r['pass'] for r in controls) else 1


def blocks_by_target(project):
    """One block map PER TARGET. Never one map for the whole project.

    Scratch block ids are unique within a target, not across a project, and these
    packs are hand-authored with k1..kN restarting in every sprite: measured on
    W07_Bug_Hunt, ELEVEN ids appear in both Player and Hazard. A single flat map
    lets one sprite's block overwrite another's, and the parent check then compares
    a block in Player against a parent in Hazard.

    An earlier draft of this file did exactly that and reported Player's k11 as
    having parent k7, which is Hazard's k11's parent. Player's k11 is correct and
    always was. That would have been a STOP on a sound pack -- the same failure
    this module was written to catch, produced by this module.
    """
    out = []
    for t in project.get('targets', []):
        blocks = {bid: b for bid, b in (t.get('blocks') or {}).items()
                  if isinstance(b, dict) and 'opcode' in b}
        out.append((t.get('name', '?'), blocks))
    return out


def referenced_ids(block):
    """Ids this block points at: its next, and any block embedded in an input.

    An input is [shadow, value] or [shadow, value, obscured]; a value that is a
    string is a block id, a value that is a list is a literal. Shadow blocks (a
    dropdown menu, a number slot) are blocks too and carry parents of their own,
    so they count.
    """
    out = []
    nxt = block.get('next')
    if isinstance(nxt, str):
        out.append(('next', nxt))
    for key, spec in (block.get('inputs') or {}).items():
        if not isinstance(spec, list):
            continue
        for item in spec[1:]:
            if isinstance(item, str):
                out.append(('input ' + key, item))
    return out


def check_project(project, label='project.json'):
    problems = []
    for target, blocks in blocks_by_target(project):
        for bid, b in sorted(blocks.items()):
            for how, ref in referenced_ids(b):
                if ref not in blocks:
                    # Not a block in THIS target. Real projects reference variable and
                    # list ids from inputs, and those are not blocks; this unit declares
                    # none (measured: 0 variables, 0 lists in all 23), so it is reported
                    # rather than assumed benign.
                    problems.append('%s: %s %s of %s (%s) names %s, which is not a block in this sprite'
                                    % (label, target, how, bid, b.get('opcode'), ref))
                    continue
                child = blocks[ref]
                if child.get('parent') != bid:
                    problems.append('%s: %s %s of %s (%s) names %s, but that block\'s parent is %r'
                                    % (label, target, how, bid, b.get('opcode'), ref, child.get('parent')))
    return problems


def check_sb3(path):
    try:
        with zipfile.ZipFile(path) as z:
            project = json.loads(z.read('project.json'))
    except Exception as e:                       # a crash is not a clean result
        return ['%s: UNREADABLE (%s)' % (os.path.basename(path), e)]
    return check_project(project, os.path.basename(path))


def plant_null_parent(path, out_path):
    """Copy the .sb3 with one referenced block's parent set to null.

    This is the control. If the check cannot fire on a project that is broken in
    exactly the way the superseded pack was broken, it is not measuring anything.
    """
    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        project = json.loads(z.read('project.json'))
        payload = {n: z.read(n) for n in names}
    planted = None
    for t in project.get('targets', []):
        blocks = t.get('blocks') or {}
        for bid, b in blocks.items():
            if not isinstance(b, dict) or 'opcode' not in b:
                continue
            for _, ref in referenced_ids(b):
                child = blocks.get(ref)
                if isinstance(child, dict) and child.get('parent') == bid:
                    child['parent'] = None
                    planted = (t.get('name'), bid, ref)
                    break
            if planted: break
        if planted: break
    if not planted:
        return None, None
    payload['project.json'] = json.dumps(project).encode()
    with zipfile.ZipFile(out_path, 'w', zipfile.ZIP_DEFLATED) as z:
        for n in names:
            z.writestr(n, payload[n])
    return out_path, planted


def self_test():
    n, bad = [0], []
    def want(name, cond):
        n[0] += 1
        print(('  PASS  ' if cond else '  FAIL  ') + name)
        if not cond: bad.append(name)

    good = {'targets': [{'name': 'Player', 'blocks': {
        'a': {'opcode': 'event_whenflagclicked', 'next': 'b', 'parent': None, 'inputs': {}},
        'b': {'opcode': 'motion_gotoxy', 'next': None, 'parent': 'a',
              'inputs': {'X': [1, 'm']}},
        'm': {'opcode': 'math_number', 'next': None, 'parent': 'b', 'inputs': {}},
    }}]}
    want('a consistent project is clean', check_project(good) == [])

    broken_next = json.loads(json.dumps(good))
    broken_next['targets'][0]['blocks']['b']['parent'] = None
    p = check_project(broken_next)
    want('a next whose child has parent null is caught', len(p) == 1)
    want('  ... and the message names both blocks and the opcode',
         'a' in p[0] and 'b' in p[0] and 'event_whenflagclicked' in p[0])
    want('  ... and it prints the parent it actually found', "parent is None" in p[0])

    broken_input = json.loads(json.dumps(good))
    broken_input['targets'][0]['blocks']['m']['parent'] = 'a'
    p2 = check_project(broken_input)
    want('an INPUT whose child names the wrong parent is caught', len(p2) == 1)
    want('  ... and it says which input', 'input X' in p2[0])

    dangling = json.loads(json.dumps(good))
    dangling['targets'][0]['blocks']['b']['next'] = 'nope'
    want('a next naming a block that does not exist is caught',
         any('not a block in this sprite' in x for x in check_project(dangling)))

    # A shadow block in an obscured input: [shadow, real, obscuredShadow]. Both the
    # real block and the obscured shadow are blocks and both need parents.
    obscured = {'targets': [{'name': 'P', 'blocks': {
        'x': {'opcode': 'motion_movesteps', 'next': None, 'parent': None,
              'inputs': {'STEPS': [3, 'r', 's']}},
        'r': {'opcode': 'motion_xposition', 'next': None, 'parent': 'x', 'inputs': {}},
        's': {'opcode': 'math_number', 'next': None, 'parent': 'x', 'inputs': {}},
    }}]}
    want('an obscured shadow is checked too, not skipped', check_project(obscured) == [])
    obscured['targets'][0]['blocks']['s']['parent'] = None
    want('  ... and a broken obscured shadow is caught', len(check_project(obscured)) == 1)

    # THE CONTROL FOR THIS MODULE'S OWN DEFECT. Two sprites, the same block ids,
    # each internally consistent. A flat project-wide map lets one overwrite the
    # other and invents a mismatch. Measured on the real pack: 11 ids appear in
    # both Player and Hazard, and the first draft reported a false STOP because of
    # exactly this shape.
    reused = {'targets': [
        {'name': 'Player', 'blocks': {
            'k14': {'opcode': 'control_if', 'next': None, 'parent': 'k16',
                    'inputs': {'SUBSTACK': [2, 'k11']}},
            'k11': {'opcode': 'motion_gotoxy', 'next': None, 'parent': 'k14', 'inputs': {}},
            'k16': {'opcode': 'control_forever', 'next': None, 'parent': None,
                    'inputs': {'SUBSTACK': [2, 'k14']}},
        }},
        {'name': 'Hazard', 'blocks': {
            'k7': {'opcode': 'event_whenflagclicked', 'next': 'k11', 'parent': None, 'inputs': {}},
            'k11': {'opcode': 'control_forever', 'next': None, 'parent': 'k7', 'inputs': {}},
        }},
    ]}
    want('two sprites reusing the same block ids are each judged on their own',
         check_project(reused) == [])
    reused['targets'][1]['blocks']['k11']['parent'] = None
    pr = check_project(reused)
    want('  ... and a real break in the SECOND sprite is still caught', len(pr) == 1)
    want('  ... and it is attributed to that sprite, not the first', 'Hazard' in pr[0])

    empty = {'targets': [{'name': 'Stage', 'blocks': {}}]}
    want('a target with no blocks is clean, not a crash', check_project(empty) == [])

    want('a project with no targets key is clean, not a crash', check_project({}) == [])

    print('\n%d checks, %d failed' % (n[0], len(bad)))
    for b in bad: print('  FAILED:', b)
    return 1 if bad else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('dirs', nargs='*')
    ap.add_argument('--self-test', action='store_true', dest='self_test')
    ap.add_argument('--red-proof')
    ap.add_argument('--schema', action='store_true')
    ap.add_argument('--schema-self-test', type=Path)
    ap.add_argument('--publisher-ref', action='store_true')
    ap.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[2])
    ap.add_argument('--registry', type=Path)
    ap.add_argument('--report', type=Path)
    a = ap.parse_args()
    if a.publisher_ref:
        try:
            print(publisher_ref(a.root.resolve()))
        except (OSError, ValueError) as error:
            print('UNMEASURED: ' + str(error), file=sys.stderr)
            sys.exit(2)
        sys.exit(0)
    if a.schema_self_test:
        sys.exit(schema_self_test(a.schema_self_test))
    if a.schema:
        if not a.registry or not a.report:
            ap.error('--schema requires --registry and --report')
        sys.exit(schema_run(a.root.resolve(), a.registry, a.report))
    if a.self_test:
        sys.exit(self_test())
    if a.red_proof:
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            out, planted = plant_null_parent(a.red_proof, os.path.join(d, 'planted.sb3'))
            if not out:
                print('could not plant: no two-way link found in ' + a.red_proof, file=sys.stderr)
                sys.exit(2)
            before = check_sb3(a.red_proof)
            after = check_sb3(out)
            print('RED PROOF on %s' % os.path.basename(a.red_proof))
            print('  planted null parent: target %s, %s -> %s' % planted)
            print('  original : %d problem(s)' % len(before))
            print('  planted  : %d problem(s)' % len(after))
            for x in after[:2]:
                print('    ' + x)
            ok = not before and len(after) >= 1
            print('  control %s' % ('FIRES' if ok else 'DID NOT FIRE'))
            sys.exit(0 if ok else 1)
    if not a.dirs:
        print('give one or more directories, or --self-test', file=sys.stderr)
        sys.exit(2)
    files = []
    for d in a.dirs:
        files += sorted(glob.glob(os.path.join(d, '**', '*.sb3'), recursive=True))
    problems = []
    for f in files:
        problems += check_sb3(f)
    print('sb3 checked           : %d' % len(files))
    print('inconsistent links    : %d' % len(problems))
    for p in problems[:40]:
        print('  ' + p)
    sys.exit(1 if problems else 0)


if __name__ == '__main__':
    main()
