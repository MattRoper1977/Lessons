#!/usr/bin/env python3
"""N6 · F1 — make the BUILD_ASDAN print surface fit the paper it is printed on.

WHAT THE RENDER FOUND. Every one of the 24 BUILD_ASDAN lesson decks overflows
its first `.print-page` past the A4 content box, by 12.1mm to 30.9mm. Each deck
declares three print pages and emits four sheets; in two of them the spilled
sheet carries nothing but the tail of a sentence (0.123% and 0.058% ink), which
is the near-blank page the F1 render count is about.

WHY. That pack's `@media print` block sets visibility and pagination and no
typography whatsoever, so the headings print at their SCREEN sizes: `h1` at
57.6px (~43pt) and `h2` at 40.8px (~31pt) on a 190mm-wide page. Six headings on
page one consume roughly a third of the sheet. The LAUNCH_ASDAN donor
(`n3_donor_print.css`) already sets print sizes for exactly this reason; the
BUILD chassis never got the equivalent.

WHAT THIS CHANGES, AND WHAT IT DELIBERATELY DOES NOT. Heading sizes and block
spacing only. No reading text changes size: `p` and `li` keep their 12pt, and
the evidence-record lines keep their height. These are Entry 3 pupil-facing
packs and buying vertical space by shrinking what a pupil reads would be the
wrong trade. What is taken instead is screen-scale whitespace — a 43pt heading
and a 16px gap between every paragraph are defensible on a monitor and simply
waste paper — and that alone returns more than the worst overflow needs.

MEASURE ON THE PAPER, NOT IN THE VIEWPORT. An element-geometry probe under
`emulateMedia('print')` still lays out at the 1280px viewport, so text wraps
wider than A4 and every page looks like it fits. It said all 24 were clear
while the PDF still spilled eight of them. The page count in the rendered PDF
is the only measurement that settles this.

Screen rendering is untouched: every rule is inside `@media print`.
Idempotent, and strip-reversible for the additivity gate.
"""
import os, sys, glob

OPEN  = '<!--n6-print-fit:v1-->'
CLOSE = '<!--/n6-print-fit-->'

CSS = (
    '<style id="n6-print-fit">@media print{'
    '.print-pack h1{font-size:20pt;line-height:1.15;margin:0 0 3mm}'
    '.print-pack h2{font-size:13pt;line-height:1.2;margin:3mm 0 1.5mm;padding-bottom:0}'
    '.print-pack h3{font-size:11pt;line-height:1.2;margin:2.5mm 0 1mm}'
    '.print-pack p,.print-pack ul,.print-pack ol{margin:2mm 0}'
    '.print-pack ul,.print-pack ol{padding-left:6mm}'
    '}</style>'
)
PAYLOAD = OPEN + CSS + CLOSE


def strip(s):
    i = s.find(OPEN)
    if i < 0:
        return s
    j = s.index(CLOSE, i) + len(CLOSE)
    return s[:i] + s[j:]


def patch(p, dry=False):
    s = open(p, encoding='utf-8').read()
    if 'print-pack' not in s:
        return 'no-print-pack'
    if OPEN in s:
        return 'already'
    if '</head>' not in s:
        return 'no-head'
    out = s.replace('</head>', PAYLOAD + '</head>', 1)
    if not dry:
        open(p, 'w', encoding='utf-8').write(out)
    return 'fitted'


if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    root = args[0]
    mode_strip = '--strip' in sys.argv
    dry = '--dry' in sys.argv
    tally = {}
    for f in sorted(glob.glob(os.path.join(root, '**', '*.html'), recursive=True)):
        if mode_strip:
            s = open(f, encoding='utf-8').read()
            o = strip(s)
            k = 'stripped' if o != s else 'clean'
            if o != s and not dry:
                open(f, 'w', encoding='utf-8').write(o)
        else:
            k = patch(f, dry)
        tally[k] = tally.get(k, 0) + 1
    print('%-40s %s' % (os.path.basename(root.rstrip('/')), tally))
