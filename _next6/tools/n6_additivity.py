#!/usr/bin/env python3
"""N6-F — additivity: strip every insertion and see whether the intake comes back.

The gate the order states is "strip the insertion -> byte-identical". That is a
strong claim and it is only worth anything if the intake is available to compare
against. This runs it against the twelve supplied source packs.

It reports three classes, and the distinction is the point:

  identical            every change to this file is a MARKED insertion that
                       strips cleanly. Additivity holds.

  content edit         the file differs by a deliberate wording change that is
                       NOT meant to be reversible — the N6 tier-vocabulary
                       normalisation (Reach -> Stretch, Secure route ->
                       Standard route) and the N10 UAS hedge
                       ("(unit unconfirmed - centre record)"). These are
                       decisions, not insertions, and they SHOULD fail an
                       additivity test. Recording them as their own class is
                       what stops a reviewer reading them as damage.

  unmarked insertion   a genuine insertion that carries no comment marker, so
                       nothing can strip it generically. At the time of writing
                       that is the N3 print route, inserted as a bare
                       `<style id="n6-print-route">` with no open/close comment.
                       It is reversible in practice but not by the same rule as
                       everything else, and it should be given a marker.

  unexplained          anything else. This must be zero.

Usage: n6_additivity.py <intake_root>
       where <intake_root> holds the twelve unpacked source packs.
"""
import os, sys, glob, collections

PAIRS = [
    ('BUILD_ASDAN/Autumn2_W1-W6_2026-27', 'BUILD_ASDAN_Autumn2_W1W6'),
    ('GROW_ASDAN/Autumn2_W1-W6_2026-27', 'GROW_ASDAN_Autumn2_W1W6'),
    ('LAUNCH_ASDAN/W7-W12_2026-27', 'LAUNCH_ASDAN_W7W12'),
    ('Science_Teesside/Build/W8-W13_2026-27', 'BUILD_Science_W8W13'),
    ('Science_Teesside/Grow/W8-W13_2026-27', 'GROW_Science_W8W13'),
    ('Science_Teesside/Launch/W8-W13_2026-27', 'LAUNCH_Science_W8W13'),
    ('Humanities_Teesside/BUILD_W9-W14_2026-27', 'BUILD_Humanities_W9W14'),
    ('Humanities_Teesside/GROW_W9-W14_2026-27', 'GROW_Humanities_W9W14'),
    ('Humanities_Teesside/LAUNCH_W9-W14_2026-27', 'LAUNCH_Humanities_W9W14'),
    ('Art_Teesside/Build/Spring2_2026-27', 'BUILD_Art_Spring2'),
    ('Art_Teesside/Grow/Spring2_2026-27', 'GROW_Art_Spring2'),
    ('Art_Teesside/Launch/Spring2_2026-27', 'LAUNCH_Art_Spring2'),
]

MARKED = ['n6-learner-confirm', 'n6-nav1', 'n6-print-fit']
UNMARKED_STYLE = ('<style id="n6-print-route">', '</style>')
# Known content edits, as (intake text, current text) pairs. These are matched
# against the ACTUAL differing spans rather than blind-replaced, because
# `<b>Stretch</b>` also occurs natively in packs that were never normalised and
# a blind reversal would manufacture a difference where there is none.
CONTENT_EDITS = [
    ('<b>Reach</b>', '<b>Stretch</b>'),        # N6 tier vocabulary
    ('▲ Secure route', '▲ Standard route'),
    ('★ Reach route', '★ Stretch route'),
]
HEDGES = [' (unit unconfirmed &#8212; centre record)']   # N10 UAS hedge


def strip_marked(s):
    for m in MARKED:
        o, c = '<!--%s:v1-->' % m, '<!--/%s-->' % m
        while o in s and c in s:
            i = s.find(o)
            j = s.index(c, i) + len(c)
            s = s[:i] + s[j:]
    return s


def strip_unmarked(s):
    o, c = UNMARKED_STYLE
    n = 0
    while o in s:
        i = s.find(o)
        j = s.index(c, i) + len(c)
        s = s[:i] + s[j:]
        n += 1
    return s, n


def classify_spans(orig, cur):
    """Every difference must be a known content edit. Returns (n, ok).

    Applies the edits FORWARD to the intake — the direction they were actually
    made in — and asks whether that reproduces the current file. Reversing them
    instead would be wrong: `Reach` and `Secure` occur natively in packs that
    were never normalised, and a blind reverse-replace manufactures differences
    that are not there. Forward is well defined; backward is not.

    A whole-file difflib was the first attempt and it is far too slow on 192
    files of 60KB. Nothing is lost by dropping it: the question is only whether
    the known edits account for the whole delta, and equality answers that.
    """
    s = orig
    n = 0
    for old, new in CONTENT_EDITS:
        if not old:
            continue
        c = s.count(old)
        if c:
            s = s.replace(old, new)
            n += c
    return n, s == cur


def index(root):
    idx = {}
    for d, _, fs in os.walk(root):
        for f in fs:
            if f.endswith('.html'):
                idx.setdefault(f, os.path.join(d, f))
    return idx


def main():
    intake = sys.argv[1]
    roots = {}
    for repo, hint in PAIRS:
        cands = [d for d in glob.glob(os.path.join(intake, '*'))
                 if os.path.isdir(d) and hint.lower().replace('_', '') in
                 os.path.basename(d).lower().replace('_', '').replace('-', '')]
        roots[repo] = cands[0] if cands else None

    per = collections.defaultdict(lambda: collections.Counter())
    unexplained = []
    for repo, _ in PAIRS:
        r = roots.get(repo)
        if not r:
            print('NO INTAKE for %s' % repo)
            continue
        idx = index(r)
        for p in sorted(glob.glob(os.path.join(repo, '**', '*.html'), recursive=True)):
            b = os.path.basename(p)
            if b not in idx:
                per[repo]['absent-from-intake'] += 1
                continue
            orig = open(idx[b], encoding='utf-8').read()
            s = strip_marked(open(p, encoding='utf-8').read())
            if s == orig:
                per[repo]['identical'] += 1
                continue
            s2, nstyle = strip_unmarked(s)
            if s2 == orig:
                per[repo]['unmarked-insertion'] += 1
                continue
            # the N10 hedge is an inserted phrase; remove it from the current
            # side before comparing, and count it separately
            nh = s2.count(HEDGES[0])
            s2h = s2.replace(HEDGES[0], '') if nh else s2
            ncont, ok = classify_spans(orig, s2h)
            ncont += nh
            if ok:
                if nstyle:
                    per[repo]['unmarked-insertion'] += 1
                if ncont:
                    per[repo]['content-edit'] += 1
                continue
            per[repo]['UNEXPLAINED'] += 1
            unexplained.append(p)

    tot = collections.Counter()
    print('%-44s %10s %13s %19s %12s' % ('pack', 'identical', 'content-edit',
                                         'unmarked-insertion', 'UNEXPLAINED'))
    for repo, _ in PAIRS:
        c = per[repo]
        tot.update(c)
        print('%-44s %10d %13d %19d %12d'
              % (repo, c['identical'], c['content-edit'],
                 c['unmarked-insertion'], c['UNEXPLAINED']))
    print('%-44s %10d %13d %19d %12d'
          % ('TOTAL', tot['identical'], tot['content-edit'],
             tot['unmarked-insertion'], tot['UNEXPLAINED']))
    if unexplained:
        print('\nUNEXPLAINED:')
        for p in unexplained[:20]:
            print('   ', p)
    return 1 if tot['UNEXPLAINED'] else 0


if __name__ == '__main__':
    sys.exit(main())
