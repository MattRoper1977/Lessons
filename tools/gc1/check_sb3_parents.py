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

Exit 0 clean, 1 if any link is inconsistent, 2 on a usage error.
"""
import argparse
import glob
import json
import os
import sys
import zipfile


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
    a = ap.parse_args()
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
