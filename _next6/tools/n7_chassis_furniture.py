#!/usr/bin/env python3
"""N6 · N7 (PARTIAL) — NAV-1 way-home + Made by Matt splash.

SCOPE, and why it is partial. D7 asks for three pieces of chassis furniture in
priority order. The third — the PH-3 hide-teacher-guidance toggle — is HELD on
Matt's ruling of 2026-08-28, for two blockers the order did not anticipate:

  1. `_eca1/tools/guidepatch.js`, the patcher D7 names, classifies ALL 192 new
     files as chassis `doc` and skips every one. They are a new chassis
     generation carrying none of its markers (`mbmTAopen`, `showTABrief`,
     `/v3_40min/SCI_`). Applying it needs a new per-family hide-set map — new
     authoring, and the patcher's own comments record the B-2 incident where
     mis-tagging left 140 of 175 decks rendering "a heading and nothing else".
  2. PH-3 persists `mbm_guide_v1` in localStorage (all 175 estate carriers do),
     which §4 gate 4 forbids and which every new deck contradicts by declaring
     `storageKeys: []`.

The two pieces applied here carry neither risk: both are pure additive markup,
no storage, no hide-set judgement, and both are PRINT-HIDDEN so gate 7 holds.

DONORS are the estate's own bytes, not retyped:
  way-home — `<a class="mbmhome" href="…index.html" …>← Lessons</a>`, the single
             form on 50 carriers; only the `../` depth varies, one per level.
  splash   — the single 503-byte inline-SVG block on 116 carriers. Inline SVG,
             zero external references, so offline integrity is untouched.

Idempotent and strip-reversible.
"""
import os, re, sys, glob

HERE = os.path.dirname(os.path.abspath(__file__))
OPEN, CLOSE = '<!--n6-nav1:v1-->', '<!--/n6-nav1-->'
SPLASH = open(os.path.join(HERE, 'nav1_splash.html'), encoding='utf-8').read().strip()
WAYHOME = ('<a class="mbmhome" href="%sindex.html" '
           'aria-label="Back to the Lessons catalogue">← Lessons</a>')
# Gate 7: print output must be byte-identical before and after. Both additions are
# therefore print-hidden. BUILD_ASDAN's own print CSS already hides everything outside
# .print-pack, so this is belt and braces there and load-bearing everywhere else.
CSS = ('<style id="n6-nav1-css">@media print{.mbmhome,.n6-splash{display:none!important}}'
       '.mbmhome{display:inline-block;margin:6px 0 0 8px;font:600 .85rem/1.4 "Segoe UI",Arial,sans-serif;'
       'color:#1e3a8a;text-decoration:none}.mbmhome:hover,.mbmhome:focus{text-decoration:underline}</style>')

def depth_prefix(rel):
    """One ../ per directory level between the file and the repo root."""
    return '../' * rel.replace(os.sep, '/').count('/')

def strip(s):
    while OPEN in s:
        i = s.find(OPEN); j = s.index(CLOSE, i) + len(CLOSE)
        s = s[:i] + s[j:]
    return s

def patch(path, rel, dry=False):
    s = open(path, encoding='utf-8').read()
    if OPEN in s: return 'already'
    m = re.search(r'<body\b[^>]*>', s)
    if not m or '</body>' not in s: return 'no-body'
    head = OPEN + CSS + WAYHOME % depth_prefix(rel) + CLOSE
    tail = OPEN + '<div class="n6-splash">' + SPLASH + '</div>' + CLOSE
    out = s[:m.end()] + head + s[m.end():]
    out = out.replace('</body>', tail + '</body>', 1)
    if not dry: open(path, 'w', encoding='utf-8').write(out)
    return 'patched'

if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    root, destprefix = args[0], args[1]          # destprefix = repo-relative dir of pack root
    intake = args[2] if len(args) > 2 else None
    dry, verify = '--dry' in sys.argv, '--verify' in sys.argv
    tally = {}
    for p in sorted(glob.glob(os.path.join(root, '**', '*.html'), recursive=True)):
        rel_in_pack = os.path.relpath(p, root)
        rel_in_repo = os.path.join(destprefix, rel_in_pack)
        if verify:
            o = open(os.path.join(intake, rel_in_pack), encoding='utf-8').read()
            k = 'strip==intake' if strip(open(p, encoding='utf-8').read()) == o else 'STRIP MISMATCH'
        else:
            k = patch(p, rel_in_repo, dry)
        tally[k] = tally.get(k, 0) + 1
    print('%-46s %s' % (os.path.basename(root), tally))
    sys.exit(1 if 'STRIP MISMATCH' in tally or 'no-body' in tally else 0)
