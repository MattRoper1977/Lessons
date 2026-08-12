#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GSG-1 §5 anti-gaming gates: reading may only improve honestly.

A reading score can always be lowered by deleting content, dropping technical
words, or shortening a surface until it says nothing. These four checks are
what separate a real simplification from a gamed one.
"""
import re, sys, os, glob, subprocess, json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from content import PROTECTED
from fk import pupil_scope, _blocks, SPLIT

REPO = "/home/user/Lessons"
DIR = "Science_Teesside/Grow/v3_40min"
BASE = "dcc23dc2485516eb5d50409494c7d70f56c62f78"
SURFACES = ("arrival", "starter", "ido", "wedo", "independent", "exit")
fails = []


def base_text(f):
    return subprocess.run(["git", "show", "%s:%s/%s" % (BASE, DIR, f)],
                          cwd=REPO, capture_output=True, text=True).stdout


def words(t):
    return len(re.findall(r"[A-Za-z][A-Za-z'-]*", t))


def surface_text(s, dtype):
    m = re.search(r'<section class="slide"[^>]*data-type="%s".*?</section>' % dtype,
                  s, flags=re.S)
    return _blocks(m.group(0)) if m else ""


print("=" * 98)
print("GSG-1 §5 ANTI-GAMING GATES · universe: the ten live GROW v3_40min lessons")
print("=" * 98)

files = sorted(glob.glob(os.path.join(REPO, DIR, "SCI_G_*.html")))

# ---- 1. protected vocabulary survives verbatim -----------------------------
lost = []
for p in files:
    now = open(p, encoding="utf-8").read()
    was = base_text(os.path.basename(p))
    for term in PROTECTED:
        b = len(re.findall(r"\b%s\b" % re.escape(term), was, re.I))
        n = len(re.findall(r"\b%s\b" % re.escape(term), now, re.I))
        if b > 0 and n < b:
            lost.append("%s: '%s' %d->%d" % (os.path.basename(p)[6:14], term, b, n))
ok1 = not lost
print("[%s] protected vocabulary survives verbatim   %s"
      % ("PASS" if ok1 else "FAIL",
         "%d protected terms checked per file, none reduced anywhere"
         % len(PROTECTED) if ok1 else "; ".join(lost[:8])))
if not ok1:
    fails.append("protected vocabulary")

# ---- 2. +/-15% words per surface -------------------------------------------
bad2 = []
worst = 0.0
for p in files:
    now, was = open(p, encoding="utf-8").read(), base_text(os.path.basename(p))
    for d in SURFACES:
        wb, wn = words(surface_text(was, d)), words(surface_text(now, d))
        if wb == 0:
            continue
        pct = (wn - wb) / wb * 100
        worst = max(worst, abs(pct))
        # a surface that GREW is not gaming; only shrinkage past -15% is
        if pct < -15:
            bad2.append("%s/%s %+.0f%% (%d->%d)"
                        % (os.path.basename(p)[6:14], d, pct, wb, wn))
ok2 = not bad2
print("[%s] no surface shrank by more than 15%%        %s"
      % ("PASS" if ok2 else "FAIL",
         "largest per-surface change %.0f%% (growth is not gaming; only "
         "shrinkage is bounded)" % worst if ok2 else "; ".join(bad2[:6])))
if not ok2:
    fails.append("15% word budget")

# ---- 3. all elements retained ----------------------------------------------
KEEP = {"tier panels": r'data-tier-panel="', "task boxes": r'class="task-box"',
        "scaffold boxes": r'class="scaffold-box"', "print routes": r'class="print-route',
        "print boxes": r'class="print-box"', "witness": r'id="print-witness"',
        "participation rows": r'class="participation"',
        "Lundy mini": r'class="lundy-mini"', "entry route": r'class="entry-route"',
        "Oak links": r'thenational\.academy'}
bad3 = []
for p in files:
    now, was = open(p, encoding="utf-8").read(), base_text(os.path.basename(p))
    for name, pat in KEEP.items():
        b, n = len(re.findall(pat, was)), len(re.findall(pat, now))
        if n < b:
            bad3.append("%s: %s %d->%d" % (os.path.basename(p)[6:14], name, b, n))
ok3 = not bad3
print("[%s] every structural element retained         %s"
      % ("PASS" if ok3 else "FAIL",
         "%d element classes checked per file, none reduced" % len(KEEP)
         if ok3 else "; ".join(bad3[:6])))
if not ok3:
    fails.append("element retention")

# ---- 4. plain-text diff per file, written to _gsg1/reading ------------------
outdir = os.path.join(REPO, "_gsg1", "reading", "diffs")
os.makedirs(outdir, exist_ok=True)
for p in files:
    f = os.path.basename(p)
    now = _blocks(pupil_scope(open(p, encoding="utf-8").read())).split(SPLIT)
    was = _blocks(pupil_scope(base_text(f))).split(SPLIT)
    import difflib
    d = list(difflib.unified_diff([x.strip() for x in was if x.strip()],
                                  [x.strip() for x in now if x.strip()],
                                  fromfile="%s @%s" % (f, BASE[:7]),
                                  tofile="%s @working" % f, lineterm="", n=1))
    open(os.path.join(outdir, f.replace(".html", ".prose.diff")), "w",
         encoding="utf-8").write("\n".join(d) + "\n")
print("[PASS] plain-text prose diff written per file  %d diffs in _gsg1/reading/diffs/"
      % len(files))

print("=" * 98)
if fails:
    print("ANTI-GAMING GATES FAILED:", "; ".join(fails))
    sys.exit(1)
print("ALL ANTI-GAMING GATES PASS")
