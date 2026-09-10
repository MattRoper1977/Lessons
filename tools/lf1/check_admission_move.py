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

WHICH REGISTRY IT MUST READ

There is only one registry that decides anything, and it is not the obvious one.
The publisher reads the all-file admission record from the BUILDER CHECKOUT at
the `builder_ref` this repository pins, never from Site main (D1). Those are not
the same tree and never have been: the pinned builder is a deliberately surgical
commit kept off Site main, so Site main's copy of the record can disagree with
the one in force by thousands of rows.

On 2026-09-09 this guard was pointed at a Site main checkout and reported "0
served paths" for a commit that had just moved the bytes of three admitted
manifests. It was not wrong about the diff. It was reading a file in which those
three paths had no row at all, so each one fell into "not served, ignore" -- and
said nothing, in the same run in which the publisher blocked publication on
exactly those paths. A guard that reads the wrong authority does not fail; it
agrees with you.

So --pin-from is the normal mode: read `builder_ref` out of the publication
workflow, then read the record out of the Site checkout AT THAT REF. --registry
still works for a file you have in hand, and says loudly in the output that it is
not the pinned authority. Either way the output now names the registry it read,
because the version that did not name it is the version that missed this.

USAGE
  python3 tools/lf1/check_admission_move.py --site <site checkout> \
      [--pin-from .github/workflows/education-pages.yml] \
      [--base origin/main] [--head HEAD] [--tree education-lessons]
  python3 tools/lf1/check_admission_move.py --registry <admission.json> ...
  python3 tools/lf1/check_admission_move.py --self-test

Exit 0 clean, 1 if any changed admitted path lacks a staged move, 2 on a usage
or input error.
"""
import argparse
import json
import re
import subprocess
import sys

ARRIVING = 'ARRIVING'
REGISTRY_IN_SITE = 'domain-split/education-publication-admission.json'
PIN_DEFAULT = '.github/workflows/education-pages.yml'


def read_builder_pin(text):
    """The builder_ref this repository pins, read from the publication workflow.

    Keyed on the `builder_ref:` line and nothing else. The same sha also appears
    on the `uses: ...@<sha>` line and abbreviated in the advance comments, and a
    looser scan would happily return one of those -- which is fine until the day
    they disagree, which is precisely the day it matters.
    """
    found = re.findall(r'^\s*builder_ref:\s*["\']?([0-9a-f]{40})["\']?\s*$', text, re.M)
    if not found:
        raise ValueError('no builder_ref: <40-hex sha> line in the workflow')
    if len(set(found)) > 1:
        raise ValueError('workflow pins more than one builder_ref: ' + ', '.join(sorted(set(found))))
    return found[0]


def registry_at(site_repo, ref, path=REGISTRY_IN_SITE):
    out = subprocess.run(['git', 'show', '%s:%s' % (ref, path)],
                         cwd=site_repo, capture_output=True, text=True)
    if out.returncode:
        raise ValueError('cannot read %s at %s in %s: %s'
                         % (path, ref[:12], site_repo, out.stderr.strip()))
    return json.loads(out.stdout)


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


def under_served_tree(path, dirs):
    """True if any ANCESTOR directory of this path is one the publisher serves.

    The first version of this asked only about the immediate parent, which is the
    right question for a file dropped beside existing ones and the wrong one for a
    whole new subtree. GC1 added 162 files under
    ICT/Teaching_Packs/GROW_Computing/Week_01/ and friends. None of those
    directories existed, so none was a served directory, so the guard reported
    "served paths: 1" -- the one already-admitted index.html whose bytes moved --
    and said nothing about the other 162.

    The publisher would have said plenty. verify_tree_census walks the whole built
    tree and calls every path it does not recognise UNREVIEWED, so those 162 were
    162 blocked publications the guard could not see. ICT/Teaching_Packs IS served
    (its index.html is admitted), so an ancestor test catches them while still
    ignoring tools/ and _sx2/, which have no served ancestor at all.
    """
    parts = path.split('/')
    for i in range(len(parts) - 1, 0, -1):
        if '/'.join(parts[:i]) in dirs:
            return True
    return False


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
            if status in ('A', 'C') and '/' in path and under_served_tree(path, dirs):
                problems.append('UNADMITTED %s: added under a tree the publisher serves, but no registry row' % path)
            continue
        if status in ('A', 'C'):
            # A path that did not exist before is not a byte MOVE, and asking it for
            # [pre, post] asks for a "pre" that never existed. The row it needs is
            # [ARRIVING, digest]: ARRIVING permits the prior absence, the digest
            # admits the bytes now arriving. A row without ARRIVING claims the file
            # was already there, which contradicts the diff, so that is reported
            # rather than waved through.
            #
            # Until the first genuinely new served path met this guard, every case it
            # had seen was a modification; an added path fell into the branch below
            # and was told to stage a move it could not have.
            if ARRIVING in (row if isinstance(row, list) else [row]):
                staged.append(path)
            else:
                problems.append('ADDED WITHOUT ARRIVING %s: new path, but its row pins %d digest(s) '
                                'and does not permit the absence it is arriving from'
                                % (path, len(admitted(row))))
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

    # The shape the first version missed: a wholly new SUBTREE under a served one.
    # None of its directories exists yet, so a parent-only test sees nothing, while
    # the publisher censuses the built tree and calls all of them UNREVIEWED.
    p, s = check(reg2, [('A', 'Science/unit/newweek/lesson.html')])
    want('an ADDED file in a NEW subdirectory under a served tree is RED',
         len(p) == 1 and p[0].startswith('UNADMITTED'))
    p, s = check(reg2, [('A', 'Science/unit/a/b/c/deep.html')])
    want('  ... however deep the new subtree goes', len(p) == 1)
    p, s = check(reg2, [('A', 'tools/lf1/a/b/new_tool.py')])
    want('  ... and a deep path with NO served ancestor is still ignored', not p)
    want('under_served_tree finds a grandparent',
         under_served_tree('Science/unit/new/x.html', {'Science/unit'}))
    want('  ... and does not match a sibling prefix',
         not under_served_tree('Science/unitother/x.html', {'Science/unit'}))
    p, s = check(reg2, [('A', 'tools/lf1/new_tool.py')])
    want('an ADDED file where nothing is served is ignored', not p)
    p, s = check(reg2, [('A', 'brand-new.html')])
    want('an ADDED file at the repository root is ignored (no served sibling)', not p)

    # This assertion used to read "an added path that already has a row is treated
    # as a byte move", and it passed because that is what the code did. It was the
    # DEFECT written down as an expectation: staged.html's row is [pre, post], which
    # says the file existed and changed, while the diff says it was added. Those
    # disagree, and the guard should say so rather than accept the pair.
    p, s = check(reg, [('A', 'staged.html')])
    want('an ADDED path whose row is a [pre, post] pair is RED, not silently accepted',
         len(p) == 1 and p[0].startswith('ADDED WITHOUT ARRIVING'))

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

    # A genuinely NEW served path: the row it needs is [ARRIVING, digest].
    reg3 = {'trees': {'education-lessons': {
        'Science/unit/one.html': 'a' * 64,
        'Science/unit/new.json': [ARRIVING, 'd' * 64],
        'Science/unit/badnew.json': 'e' * 64,
    }}}
    p, s = check(reg3, [('A', 'Science/unit/new.json')])
    want('an ADDED path whose row carries ARRIVING is clean', not p and s == ['Science/unit/new.json'])
    p, s = check(reg3, [('A', 'Science/unit/badnew.json')])
    want('an ADDED path whose row has no ARRIVING is RED',
         len(p) == 1 and p[0].startswith('ADDED WITHOUT ARRIVING'))
    want('  ... and it says the row does not permit the absence', 'permit the absence' in p[0])
    p, s = check(reg3, [('M', 'Science/unit/one.html')])
    want('  ... and a MODIFIED path still needs a real pair, not ARRIVING',
         len(p) == 1 and p[0].startswith('NO STAGED MOVE'))
    want('admitted() accepts a bare string', admitted('y' * 64) == ['y' * 64])

    # --- the pin parser: which registry is the authority (D1) ---
    PIN, OTHER = 'a' * 40, 'b' * 40
    wf = ('jobs:\n  publication:\n'
          '    # Advanced 2026-09-09 (LF1) 94ae15f8 -> 2e4d9966, surgical\n'
          '    uses: Owner/repo/.github/workflows/education-publication.yml@%s\n'
          '    with:\n      builder_ref: %s\n' % (PIN, PIN))
    want('reads builder_ref out of the publication workflow', read_builder_pin(wf) == PIN)

    # The near-miss: a looser scan for "any 40-hex" would return whichever it hit
    # first. Here the reusable-workflow ref and the builder_ref disagree, which is
    # the only case where guessing costs anything -- and it is exactly the case a
    # sha-anywhere regex gets wrong.
    skew = wf.replace('education-publication.yml@' + PIN, 'education-publication.yml@' + OTHER)
    want('a uses: @sha that disagrees with builder_ref does not win', read_builder_pin(skew) == PIN)

    want('an abbreviated sha in an advance comment is not mistaken for the pin',
         read_builder_pin('      builder_ref: %s\n# was 2e4d9966 -> 2a154e33\n' % PIN) == PIN)
    want('a quoted value is read', read_builder_pin('      builder_ref: "%s"\n' % PIN) == PIN)

    def raises(text):
        try:
            read_builder_pin(text); return False
        except ValueError:
            return True
    want('no builder_ref line at all is an error, not a silent None',
         raises('jobs:\n  publication:\n    uses: Owner/repo/wf.yml@' + PIN + '\n'))
    want('two disagreeing builder_ref lines are an error, not a coin toss',
         raises('      builder_ref: %s\n      builder_ref: %s\n' % (PIN, OTHER)))
    want('the same pin written twice is not an error',
         read_builder_pin('      builder_ref: %s\n      builder_ref: %s\n' % (PIN, PIN)) == PIN)
    want('an abbreviated builder_ref is refused rather than half-read',
         raises('      builder_ref: 2e4d9966\n'))

    # The blind spot itself, as an assertion: a path with no row in the registry
    # you happen to be holding is reported as "not served" -- which is true of
    # that file and false of the estate. This is why the source is now printed.
    p, s = check(reg, [('M', 'Science_Teesside/Grow/W18-W26_2026-27/manifest.json')])
    want('a MODIFIED path absent from THIS registry is silent -- hence --site',
         not p and not s)

    print('\n%d checks, %d failed' % (ok[0], len(bad)))
    for b in bad: print('  FAILED:', b)
    return 1 if bad else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--registry', help='an admission record in hand; NOT the pinned authority')
    ap.add_argument('--site', help='a Site checkout, read at the pinned builder_ref')
    ap.add_argument('--pin-from', default=PIN_DEFAULT, dest='pin_from')
    ap.add_argument('--base', default='origin/main')
    ap.add_argument('--head', default='HEAD')
    ap.add_argument('--tree', default='education-lessons')
    ap.add_argument('--repo', default='.')
    ap.add_argument('--self-test', action='store_true', dest='self_test')
    a = ap.parse_args()
    if a.self_test:
        sys.exit(self_test())
    if a.site:
        try:
            pin = read_builder_pin(open(a.pin_from, encoding='utf-8').read())
            registry = registry_at(a.site, pin)
        except (ValueError, OSError) as e:
            print(e, file=sys.stderr)
            sys.exit(2)
        source = '%s@%s (builder_ref, from %s)' % (a.site, pin[:12], a.pin_from)
    elif a.registry:
        registry = json.load(open(a.registry, encoding='utf-8'))
        source = '%s -- NOT the pinned builder; the publisher reads builder_ref (D1)' % a.registry
    else:
        print('give --site <site checkout> (preferred: reads the pinned builder_ref) '
              'or --registry <admission.json>', file=sys.stderr)
        sys.exit(2)
    rows = changed_paths(a.base, a.head, a.repo)
    problems, staged = check(registry, rows, a.tree)
    print('registry read from       : %s' % source)
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
