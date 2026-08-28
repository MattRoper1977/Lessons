#!/usr/bin/env python3
"""N6 · N3 — add the house print route to LAUNCH_ASDAN's 30 lesson decks.

D3, confirmed by Matt 2026-08-28. The pack shipped with NO print pathway at all
(0 @media print / printpack / print-area / window.print) and its own QA_REPORT
recorded that as a deliberate PASS. It is overridden here for one reason: these
are ASDAN evidence lessons and the portfolio is paper.

DONOR is the GROW_ASDAN print CSS, byte-for-byte. That donor is print-CSS only —
no button, no #print-area, no window.print — so SCREEN BEHAVIOUR IS BYTE-IDENTICAL
BEFORE AND AFTER by construction: an @media print block cannot affect screen
rendering. The additivity gate proves it rather than trusting it.

THE DONOR ALONE IS NOT ENOUGH, and this is the part a naive port gets wrong.
GROW hides slides with [hidden] and sizes them with min-height. LAUNCH hides with
`.slide{display:none}` / `.slide.active{display:flex}` and sizes with
`height:91%`, inside `.deck{height:100%;display:flex}` and `body{overflow:hidden}`.
Porting the donor unchanged reveals the slides — `.slide{display:block!important}`
beats display:none — but every one of them is then 91% of a page tall inside a
clipped, non-scrolling body. That prints as nine mostly-blank pages and would pass
any "does it have @media print" check. The ADDENDUM below neutralises the three
LAUNCH-specific properties the donor never had to know about. Verified by an
actual headless print-to-PDF, not by grepping for the block.

Idempotent: re-running is a no-op. Reversible: strip the marked block to recover
the intake bytes exactly.
"""
import re, sys, os, glob, hashlib

OPEN  = '<style id="n6-print-route">'
CLOSE = '</style>'

DONOR = open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          'n3_donor_print.css'), encoding='utf-8').read().strip()

# LAUNCH chassis neutralisation — each line names the LAUNCH rule it defeats.
ADDENDUM = (
 '@media print{'
 'html,body{overflow:visible!important;height:auto!important}'        # body{overflow:hidden}
 '.deck{height:auto!important;display:block!important;padding:0!important}'  # .deck{height:100%;display:flex}
 '.slide{height:auto!important;min-height:0!important;overflow:visible!important;'
 'display:block!important;border-radius:0;box-shadow:none}'           # .slide{display:none;height:91%}
 '.slide.active{display:block!important}'
 '.overlay,.drawer,.controls,.progress,.skip,.a11y-live{display:none!important}'
 '}')

BLOCK = OPEN + DONOR + ADDENDUM + CLOSE

def patch(p, dry=False):
    s = open(p, encoding='utf-8').read()
    if OPEN in s: return 'already'
    if '</head>' not in s: return 'no-head'
    out = s.replace('</head>', BLOCK + '</head>', 1)
    if not dry: open(p, 'w', encoding='utf-8').write(out)
    return 'patched'

def strip(s):
    """Reverse: remove the marked block. Used by the additivity gate."""
    i = s.find(OPEN)
    if i < 0: return s
    j = s.index(CLOSE, i) + len(CLOSE)
    return s[:i] + s[j:]

if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    dry = '--dry' in sys.argv
    check = '--verify' in sys.argv
    root, intake = args[0], (args[1] if len(args) > 1 else None)
    files = sorted(glob.glob(os.path.join(root, '**', '*.html'), recursive=True))
    files = [f for f in files if '/lessons/' in f.replace(os.sep, '/')]
    tally = {}
    for f in files:
        if check:
            s = open(f, encoding='utf-8').read()
            base = os.path.relpath(f, root)
            o = open(os.path.join(intake, base), encoding='utf-8').read()
            same = strip(s) == o
            tally['strip==intake' if same else 'STRIP MISMATCH'] = \
                tally.get('strip==intake' if same else 'STRIP MISMATCH', 0) + 1
        else:
            r = patch(f, dry); tally[r] = tally.get(r, 0) + 1
    print('%d files: %s' % (len(files), tally))
    sys.exit(1 if 'STRIP MISMATCH' in tally or 'no-head' in tally else 0)
