#!/usr/bin/env python3
"""N6 · N2 — port the T2-4 learner-confirmation block into the three new ASDAN packs.

D2: PORT the estate block, do NOT invent one. The bytes are recovered from live
carriers on main, never retyped. Two variants exist and they differ ONLY in four
newlines — BUILD_ASDAN/GROW_ASDAN carry the pretty-printed 566-byte form (x49),
LAUNCH_ASDAN the minified 562-byte form (x30). 49+30 = the 79 carriers the order
names. Each pack gets its own lane's form so formatting stays consistent per lane.

WHERE IT GOES, and why not where the order says. The order specifies "insert after
the assessor declaration table". THESE PACKS HAVE NO SUCH TABLE: `witness`
structure is 0 files, and the evidence windows explicitly disclaim being assessment
records ("It stores, uploads and scores nothing"; "assessment and any claim remain
with the authorised coordinator/assessor"). There is no anchor to insert after.
So the block is appended to the END OF THE PRINT SURFACE, on its own page. That is
the coherent placement given N3's reasoning: the PRINTED deck is the portfolio
artefact, so the learner signs the artefact.

Confined to print, no on-screen copy: `.n6-lc{display:none}` with a print-only
override. Assessor material is never touched — BUILD_ASDAN_AUT2_TEACHER_PLANNING_SOW.html
holds the only assessor-side field in all twelve packs and is explicitly excluded.

Idempotent and strip-reversible.
"""
import os, sys, glob, re

HERE = os.path.dirname(os.path.abspath(__file__))
OPEN  = '<!--n6-learner-confirm:v1-->'
CLOSE = '<!--/n6-learner-confirm-->'
CSS = ('<style id="n6-lc-css">.n6-lc{display:none}'
       '@media print{.n6-lc{display:block!important;break-before:page;'
       'page-break-before:always;background:#fff;color:#111;padding:7mm;'
       'font-family:"Segoe UI",Arial,sans-serif}}</style>')

def block(lane):
    v = 'LAUNCH' if lane == 'LAUNCH' else 'BUILD_GROW'
    return open(os.path.join(HERE, 't2_4_learner_confirmation_%s.html' % v),
                encoding='utf-8').read()

def payload(lane):
    return OPEN + CSS + '<section class="n6-lc">' + block(lane) + '</section>' + CLOSE

def strip(s):
    i = s.find(OPEN)
    if i < 0: return s
    j = s.index(CLOSE, i) + len(CLOSE)
    return s[:i] + s[j:]

# The only assessor-side surface in all twelve packs — never touched.
EXCLUDE = {'BUILD_ASDAN_AUT2_TEACHER_PLANNING_SOW.html', 'START_HERE.html',
           'START_HERE_BUILD_ASDAN_AUT2.html', 'STAFF_GUIDE.html', 'index.html',
           'PRINTABLE_RESOURCES.html'}

def surfaces(root):
    out = []
    for p in sorted(glob.glob(os.path.join(root, '**', '*.html'), recursive=True)):
        if os.path.basename(p) in EXCLUDE: continue
        out.append(p)
    return out

def _close_of(s, start, tag='section'):
    """Offset just past the tag that closes the element opened at `start`."""
    rx = re.compile(r'</?%s\b' % tag); depth = 1; i = start + 1
    while True:
        m = rx.search(s, i)
        if not m: return -1
        depth += -1 if s[m.start() + 1] == '/' else 1
        i = m.end()
        if depth == 0: return s.index('>', m.start()) + 1

def patch(p, lane, dry=False):
    """Insert into the file's OWN print surface.

    BUILD_ASDAN's 24 decks carry a real print surface — a `<section class="print-pack">`
    of `.print-page` divs, gated by `body>*:not(.print-pack){display:none!important}`.
    Appending before </body> put the block OUTSIDE that container, so all 24 carried it
    and none of them PRINTED it. A grep for the block reported 75/75 success; a headless
    print render reported 51/75. The render is the evidence. The block now goes in as a
    final `.print-page` INSIDE `.print-pack`, which is what "confine to the print
    surface" actually means on this chassis.

    GROW_ASDAN and LAUNCH_ASDAN have no such container — their whole deck is the print
    surface via @media print — so there the block is appended before </body> with a
    print-only display rule."""
    s = open(p, encoding='utf-8').read()
    if OPEN in s: return 'already'
    m = re.search(r'<section[^>]*class="[^"]*\bprint-pack\b[^"]*"[^>]*>', s)
    if m:
        end = _close_of(s, m.start(), 'section')
        if end < 0: return 'unbalanced-print-pack'
        ins = (OPEN + '<div class="print-page n6-lc-page">' + block(lane)
               + '</div>' + CLOSE)
        close_start = s.rindex('</section>', m.start(), end)
        out = s[:close_start] + ins + s[close_start:]
        mode = 'print-pack'
    else:
        if '</body>' not in s: return 'no-body'
        out = s.replace('</body>', payload(lane) + '</body>', 1)
        mode = 'body+css'
    if not dry: open(p, 'w', encoding='utf-8').write(out)
    return mode

if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    root, lane = args[0], args[1]
    intake = args[2] if len(args) > 2 else None
    dry, verify = '--dry' in sys.argv, '--verify' in sys.argv
    files = surfaces(root); tally = {}
    for f in files:
        if verify:
            base = os.path.relpath(f, root)
            o = open(os.path.join(intake, base), encoding='utf-8').read()
            k = 'strip==intake' if strip(open(f, encoding='utf-8').read()) == o else 'STRIP MISMATCH'
        else:
            k = patch(f, lane, dry)
        tally[k] = tally.get(k, 0) + 1
    print('%-46s %d surfaces: %s' % (os.path.basename(root), len(files), tally))
    sys.exit(1 if 'STRIP MISMATCH' in tally or 'no-body' in tally else 0)
