#!/usr/bin/env python3
"""tools/lf1/check_admission_move.py - a PR-time proof that changed served bytes
carry a staged admission move.

WHY THIS EXISTS

On 2026-09-09 the same gate blocked publication twice in one day, for the same
reason both times. #454 added new served paths that the Site all-file admission
registry did not list. LF1 #468 did not add a path -- it changed the BYTES of 30
paths the registry already admitted, at their pinned pre-fix digests. Both were
caught only after merge, by a red publication, with the fix sitting on main and
not being served. On the second occasion a pupil went on reading a placeholder
for the length of the recovery.

The test that was applied before #468 merged was "does this add a new served
path?". The answer was no, and it was the wrong question. The right one is "does
this change the bytes of any path that is already admitted?" -- because the
registry pins a digest per path, and a changed digest is a blocked publication
whether the path is new or not. That is D11.

WHAT IT ASSERTS

For every file a branch changes, if its path appears in the education-lessons
tree of the registry, then that path's registry row must offer more than one
admitted digest -- a transition pair [pre, post], which is how a byte move is
staged so that a build at either state passes. A single-valued row for a changed
path is exactly the state that reds the publisher, and is reported RED here
instead.

WHAT IT DELIBERATELY DOES NOT ASSERT

It does not compare digests. The registry pins the digest of the PUBLISHED
artefact, and the publisher injects navigation into many pages, so a source hash
is simply a different number -- 19 of 40 sampled paths match their source blob
and the rest do not, by design. Proving the digest right needs the reviewed
builder and a full build, which is the publisher's own gate and takes minutes.

So this is a necessary condition, not a sufficient one: it cannot tell you the
pair holds the right digests, but it will not let a changed served path reach
main with no pair at all. That is the failure that actually happened, twice.

USAGE
  python3 tools/lf1/check_admission_move.py --registry <admission.json> \
      [--base origin/main] [--head HEAD] [--tree education-lessons]
  python3 tools/lf1/check_admission_move.py --self-test

Exit 0 clean, 1 if any changed admitted path lacks a staged move, 2 on a usage
or input error.
"""
import argparse
import json
import subprocess
import sys

ARRIVING = 'ARRIVING'


def admitted(row):
    """The digests a row admits, ignoring the ARRIVING marker that permits absence."""
    return [d for d in (row if isinstance(row, list) else [row]) if d != ARRIVING]


def changed_paths(base, head, cwd='.'):
    out = subprocess.run(['git', 'diff', '--name-status', '-z', base + '...' + head],
                         cwd=cwd, capture_output=True, text=True)
    if out.returncode:
        print('cannot diff %s...%s: %s' % (base, head, out.stderr.strip()), file=sys.stderr)
        sys.exit(2)
    fields = [f for f in out.stdout.split('\0') if f]
    rows, i = [], 0
    while i < len(fields):
        status = fields[i]
        if status.startswith('R') or status.startswith('C'):     # rename/copy: old, new
            rows.append((status[0], fields[i + 2])); rows.append(('D', fields[i + 1])); i += 3
        else:
            rows.append((status[0], fields[i + 1])); i += 2
    return rows


def served_dirs(admittedmap):
    """Directories the publisher already serves at least one file from."""
    return {p.rsplit('/', 1)[0] for p in admittedmap if '/' in p}


def check(registry, rows, tree='education-lessons'):
    admittedmap = registry['trees'][tree]
    dirs = served_dirs(admittedmap)
    problems, staged = [], []
    for status, path in rows:
        row = admittedmap.get(path)
        if row is None:
            # A new file is only the publisher's business if it lands where the
            # publisher already serves. tools/, _sx2/ and the rest of the working
            # repository are not served and must not be reported: a gate that
            # cries about every new script is a gate people learn to ignore.
            if status in ('A', 'C') and '/' in path and path.rsplit('/', 1)[0] in dirs:
                problems.append('UNADMITTED %s: added where the publisher serves, but no registry row' % path)
            continue
        if status == 'D':
            if ARRIVING not in (row if isinstance(row, list) else [row]):
                problems.append('REMOVED %s: deleted, but its row does not permit absence' % path)
            continue
        if len(admitted(row)) < 2:
            problems.append('NO STAGED MOVE %s: bytes change, registry pins one digest (%s)'
                            % (path, admitted(row)[0][:12] if admitted(row) else 'none'))
        else:
            staged.append(path)
    return problems, staged


def self_test():
    ok, bad = [0], []
    def want(name, cond):
        ok[0] += 1
        print(('  PASS  ' if cond else '  FAIL  ') + name)
        if not cond: bad.append(name)

    reg = {'trees': {'education-lessons': {
        'pinned.html': 'a' * 64,
        'staged.html': ['a' * 64, 'b' * 64],
        'arriving.html': ['a' * 64, ARRIVING],
    }}}

    p, s = check(reg, [('M', 'pinned.html')])
    want('a changed path pinned to one digest is RED', len(p) == 1 and p[0].startswith('NO STAGED MOVE'))
    want('  ... and the message names the pinned digest', 'aaaaaaaaaaaa' in p[0])

    p, s = check(reg, [('M', 'staged.html')])
    want('a changed path with a transition pair is clean', not p and s == ['staged.html'])

    p, s = check(reg, [('M', 'not-served.html')])
    want('a changed path that is not served at all is ignored', not p)

    reg2 = {'trees': {'education-lessons': dict(reg['trees']['education-lessons'],
                                                **{'Science/unit/one.html': 'c' * 64})}}
    p, s = check(reg2, [('A', 'Science/unit/two.html')])
    want('an ADDED file in a directory the publisher serves is RED',
         len(p) == 1 and p[0].startswith('UNADMITTED'))
    p, s = check(reg2, [('A', 'tools/lf1/new_tool.py')])
    want('an ADDED file where nothing is served is ignored', not p)
    p, s = check(reg2, [('A', 'brand-new.html')])
    want('an ADDED file at the repository root is ignored (no served sibling)', not p)

    p, s = check(reg, [('A', 'staged.html')])
    want('an added path that already has a row is treated as a byte move', not p)

    p, s = check(reg, [('D', 'pinned.html')])
    want('a DELETED served path whose row forbids absence is RED', len(p) == 1 and p[0].startswith('REMOVED'))

    p, s = check(reg, [('D', 'arriving.html')])
    want('a DELETED path whose row carries ARRIVING is clean', not p)

    p, s = check(reg, [('M', 'arriving.html')])
    want('ARRIVING alone is not a staged move: one real digest is still one digest',
         len(p) == 1 and p[0].startswith('NO STAGED MOVE'))

    p, s = check(reg, [('M', 'pinned.html'), ('M', 'staged.html'), ('M', 'other.html')])
    want('a mixed branch reports only the unstaged path', len(p) == 1 and 'pinned.html' in p[0])

    want('admitted() drops ARRIVING', admitted(['x' * 64, ARRIVING]) == ['x' * 64])
    want('admitted() accepts a bare string', admitted('y' * 64) == ['y' * 64])

    print('\n%d checks, %d failed' % (ok[0], len(bad)))
    for b in bad: print('  FAILED:', b)
    return 1 if bad else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--registry')
    ap.add_argument('--base', default='origin/main')
    ap.add_argument('--head', default='HEAD')
    ap.add_argument('--tree', default='education-lessons')
    ap.add_argument('--repo', default='.')
    ap.add_argument('--self-test', action='store_true', dest='self_test')
    a = ap.parse_args()
    if a.self_test:
        sys.exit(self_test())
    if not a.registry:
        print('--registry is required (the Site checkout\'s education-publication-admission.json)',
              file=sys.stderr)
        sys.exit(2)
    registry = json.load(open(a.registry, encoding='utf-8'))
    rows = changed_paths(a.base, a.head, a.repo)
    problems, staged = check(registry, rows, a.tree)
    print('changed files            : %d' % len(rows))
    print('of those, served paths   : %d' % (len(problems) + len(staged)))
    print('with a staged move       : %d' % len(staged))
    print('WITHOUT a staged move    : %d' % len(problems))
    for p in problems:
        print('  ' + p)
    if problems:
        print('\nThese change bytes the publisher has pinned. Move them in the Site '
              'registry as transition pairs [pre, post] and advance builder_ref before '
              'merging, or the publication will red and the change will not be served. (D11)')
    sys.exit(1 if problems else 0)


if __name__ == '__main__':
    try:
        main()
    except BrokenPipeError:      # piping into head is a normal way to read this
        try:
            sys.stdout.close()
        finally:
            sys.exit(1)
