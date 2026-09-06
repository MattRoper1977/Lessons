#!/usr/bin/env python3
"""Re-materialise the ASDAN visual-learning owned JS block into the BUILD decks.

ASDAN_Visual_Learning/integrate.py writes the SHARED sources (the three pathway
css/js pairs and the six D&T lessons). It does not write the 31 BUILD_ASDAN lesson
decks, which inline a byte-identical copy of BUILD_ASDAN/_framework/asdan-teach.js's
owned block - its materialised_check() only asserts the marker pair is present, not
that the copy is fresh. So a regenerated payload lands in the framework and the shared
sources and stops there, leaving 31 decks serving the old blob.

Verified at the PROP-1 rollback anchor e63f047: all 31 decks carried a block byte-
identical to the framework's, so materialisation is a verbatim copy and nothing else.

    materialise.py --check   report drift, write nothing, exit 1 if any
    materialise.py           copy the framework block into every stale deck
"""
import subprocess, sys, os
from pathlib import Path

ROOT = Path(subprocess.run(["git","rev-parse","--show-toplevel"],capture_output=True,text=True).stdout.strip())
FRAMEWORK = ROOT / "BUILD_ASDAN/_framework/asdan-teach.js"
JS_START = "/* ASDAN-VISUAL-LEARNING:JS:BEGIN v1 */"
JS_END   = "/* ASDAN-VISUAL-LEARNING:JS:END v1 */"

def block(text):
    i, j = text.find(JS_START), text.find(JS_END)
    return text[i:j+len(JS_END)] if i >= 0 and j >= 0 else None

def decks():
    out = subprocess.run(["git","ls-files","BUILD_ASDAN/**/*.html"],cwd=ROOT,capture_output=True,text=True).stdout.split()
    return [f for f in out if block((ROOT/f).read_text(encoding="utf-8"))]

want = block(FRAMEWORK.read_text(encoding="utf-8"))
if want is None:
    print("FAIL: no owned JS block in the framework source"); sys.exit(1)

check = "--check" in sys.argv
stale = []
for rel in decks():
    p = ROOT / rel
    text = p.read_text(encoding="utf-8")
    have = block(text)
    if have == want: continue
    stale.append(rel)
    if not check:
        p.write_text(text.replace(have, want), encoding="utf-8")

n = len(decks())
if check:
    print(f"materialise: {n} decks carry the block; {len(stale)} STALE" if stale
          else f"materialise: all {n} decks byte-identical to the framework block")
    for s in stale: print("   stale:", s)
    sys.exit(1 if stale else 0)
print(f"materialise: {len(stale)} of {n} decks refreshed from the framework block")
