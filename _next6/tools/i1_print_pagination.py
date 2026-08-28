#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ORDER N6-I · I1 — the pagination fix the render gate found.

WHAT THE RENDER FOUND, which nothing before it could.

Rendering all 75 evidence surfaces to A4 showed the learner-confirmation block
printing 75/75 — N2's defect really was remediated. It also showed something
neither the order nor the previous pass knew about:

  BUILD_ASDAN's printable pack offers four A4 route options and the DEFAULT is
  "All three routes". In that state the first `.print-page` carries the header,
  the objective, the success criteria, all three route blocks, the independent
  task and the safety note — more than one A4 sheet holds. It spilled. In four
  of the 24 decks it spilled by a single clause, leaving physical page 2 holding
  ten to thirty-eight characters:

      BUILD_ASDAN_A2_DUKE_W5   page 2: ink 0.061%,  10 chars
      BUILD_ASDAN_A2_COMM_W1   page 2: ink 0.129%,  20 chars  ("and systems, not blame.")
      BUILD_ASDAN_A2_CON_W5    page 2: ink 0.148%,  23 chars
      BUILD_ASDAN_A2_COMM_W5   page 2: ink 0.244%,  38 chars

  A near-blank sheet in the middle of a printed portfolio artefact. Every
  element was present, so element-presence checks were green; the block that
  spilled was visible, so `checkVisibility()` was green. Only the rendered page
  shows it.

THE FIX, and why this one.

Three candidates were rendered and measured over all 24 decks, not reasoned
about. The one applied here is the smallest that works and the only one that
changes nothing about what appears on a page — only where the break falls:

    .print-page { orphans:4; widows:4 }
    .print-route{ break-inside:avoid; page-break-inside:avoid }

`widows:4` forbids a break that would leave fewer than four lines of a paragraph
at the top of the next sheet, so a paragraph that cannot satisfy that moves whole.
`break-inside:avoid` on a route block says a route is a unit — a pupil should
never meet half of their route at a page turn, which is worth having on its own
merits. Measured result across all 24 decks, route-all: minimum page-2 ink rises
from 0.061% to 0.976%, sixteen times the gate's 0.4% floor, and every page 2 now
carries a whole paragraph (159-373 characters) instead of an orphaned clause.

A rejected candidate shrank `.print-pack` to `.92em` and did fit four decks onto
three sheets. It was rejected: reducing type size on an accessibility-led pupil
artefact to win a pagination argument is the wrong trade, and it changes what a
page looks like rather than where it breaks.

Scope: the 24 decks that carry `<section class="print-pack">`. GROW_ASDAN and
LAUNCH_ASDAN print clean at 10 pages with no near-blank sheet and are not
touched — a fix goes where the defect is measurable, not everywhere.

Confined to `@media print`, so screen rendering is byte-identical by
construction. Idempotent; strip-reversible for the additivity gate.
"""
import glob
import os
import re
import sys

OPEN = '<style id="n6i-print-pagination">'
CLOSE = '</style>'

CSS = ('@media print{'
       '.print-page{orphans:4;widows:4}'
       '.print-route{break-inside:avoid;page-break-inside:avoid}'
       '}')

BLOCK = OPEN + CSS + CLOSE


def targets(root):
    """Files carrying the route-gated printable pack — the only ones at risk."""
    out = []
    for p in sorted(glob.glob(os.path.join(root, '**', '*.html'), recursive=True)):
        s = open(p, encoding='utf-8').read()
        if re.search(r'<section[^>]*class="[^"]*\bprint-pack\b', s) and 'id="printRoute"' in s:
            out.append(p)
    return out


def strip(s):
    i = s.find(OPEN)
    if i < 0:
        return s
    j = s.index(CLOSE, i) + len(CLOSE)
    return s[:i] + s[j:]


def patch(p, dry=False):
    s = open(p, encoding='utf-8').read()
    if OPEN in s:
        return 'already'
    if '</head>' not in s:
        return 'no-head'
    out = s.replace('</head>', BLOCK + '</head>', 1)
    if not dry:
        open(p, 'w', encoding='utf-8').write(out)
    return 'patched'


if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    dry = '--dry' in sys.argv
    revert = '--strip' in sys.argv
    root = args[0]
    files = targets(root)
    tally = {}
    for f in files:
        if revert:
            s = open(f, encoding='utf-8').read()
            t = strip(s)
            k = 'stripped' if t != s else 'nothing-to-strip'
            if not dry and t != s:
                open(f, 'w', encoding='utf-8').write(t)
        else:
            k = patch(f, dry)
        tally[k] = tally.get(k, 0) + 1
    print('%s: %d print-pack surfaces %s' % (os.path.basename(root.rstrip('/')), len(files), tally))
    sys.exit(1 if 'no-head' in tally else 0)
