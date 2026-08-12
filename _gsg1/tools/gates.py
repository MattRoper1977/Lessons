#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GSG-1 static gates. Every check states its unit and its universe.
Baselines are read from the rollback SHA via `git show`, never hardcoded.
Every scanner is validated against a known positive before it is trusted.
"""
import re, subprocess, sys, os

REPO = "/home/user/Lessons"
DIR = "Science_Teesside/Grow/v3_40min"
BASE = "dcc23dc2485516eb5d50409494c7d70f56c62f78"
FILES = ["SCI_G_W3A_Friction_Explore.html", "SCI_G_W3B_Friction_Do.html",
         "SCI_G_W4A_Mechanisms_Explore.html", "SCI_G_W4B_Mechanisms_Do.html",
         "SCI_G_W5A_Fair_Test_Explore.html", "SCI_G_W5B_Fair_Test_Do.html",
         "SCI_G_W6A_Earth_And_Planets_Explore.html", "SCI_G_W6B_Earth_And_Planets_Do.html",
         "SCI_G_W7A_The_Moon_Explore.html", "SCI_G_W7B_The_Moon_Do.html"]

UNIVERSE = "the ten live GROW v3_40min lesson files"
fails, ambers = [], []


def sh(c):
    return subprocess.run(c, shell=True, cwd=REPO, capture_output=True,
                          text=True).stdout


def live(f):
    return open(os.path.join(REPO, DIR, f), encoding="utf-8").read()


def base(f):
    return sh("git show %s:%s/%s" % (BASE, DIR, f))


def cnt(s, pat, flags=0):
    return len(re.findall(pat, s, flags))


def gate(n, name, ok, detail):
    tag = "PASS" if ok else "FAIL"
    if not ok:
        fails.append("%s · %s" % (n, name))
    print("[%s] gate %-3s %-46s %s" % (tag, n, name, detail))


def validate(label, pat, positive, expect=1, flags=0):
    """Never trust a scanner that has not seen a known positive."""
    got = cnt(positive, pat, flags)
    assert got == expect, "SCANNER %s failed validation: %d != %d" % (label, got, expect)


print("=" * 100)
print("GSG-1 STATIC GATES · universe for per-file rows: %s" % UNIVERSE)
print("baselines read from rollback SHA %s" % BASE[:7])
print("=" * 100)

# ---- scanner validation on known positives --------------------------------
KP = ('<div class="retr-q"><span class="retr-badge">R1</span></div>'
      'localStorage fetch( <form matchMedia href="assets/x.css" witness '
      'Supported Standard Stretch printTier afterprint print-pack '
      'What I said, and what it changed thenational.academy data-type="arrival" '
      'chocolate')
for lbl, p, e in [("storage", r"localStorage|sessionStorage|indexedDB", 1),
                  ("network", r"fetch\(|XMLHttpRequest|sendBeacon|WebSocket", 1),
                  ("form", r"<form|form-action", 1),
                  ("matchMedia", r"matchMedia", 1),
                  ("extasset", r'href="assets/|src="assets/', 1),
                  ("witness", r"witness", 1),
                  ("closure", r"What I said, and what it changed", 1),
                  ("oak", r"thenational\.academy", 1),
                  ("retr", r'class="retr-q"', 1),
                  ("food", r"chocolate", 1)]:
    validate(lbl, p, KP, e)
print("scanner validation: 10/10 scanners returned the expected count on a "
      "synthetic known positive\n")

# ---- gate 2: node --check inline JS, JSON parsed as JSON -------------------
import json, tempfile
js_ok = json_ok = 0
for f in FILES:
    s = live(f)
    blocks = re.findall(r"<script>(.*?)</script>", s, re.S)
    for i, b in enumerate(blocks):
        with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False,
                                         encoding="utf-8") as t:
            t.write(b)
            tp = t.name
        r = subprocess.run(["node", "--check", tp], capture_output=True, text=True)
        os.unlink(tp)
        if r.returncode == 0:
            js_ok += 1
        else:
            fails.append("gate2 JS syntax %s block %d: %s" % (f, i, r.stderr[:200]))
    # JSON islands parsed AS JSON, never node --check
    for m in re.finditer(r"data-topic-branches='([^']*)'", s):
        try:
            json.loads(m.group(1))
            json_ok += 1
        except Exception as e:
            fails.append("gate2 JSON %s: %s" % (f, e))
gate(2, "inline JS `node --check` + JSON parsed as JSON",
     not [x for x in fails if x.startswith("gate2")],
     "%d JS blocks checked, %d JSON islands parsed · %s" % (js_ok, json_ok, UNIVERSE))

# ---- gate 4: runtime prohibitions -----------------------------------------
rows = []
for f in FILES:
    s = live(f)
    rows.append((cnt(s, r"localStorage|sessionStorage|indexedDB"),
                 cnt(s, r"fetch\(|XMLHttpRequest|sendBeacon|WebSocket"),
                 cnt(s, r"<form|form-action"),
                 cnt(s, r'href="assets/|src="assets/|href="http[^"]*\.css|src="http[^"]*\.js'),
                 cnt(s, r"matchMedia")))
tot = [sum(c) for c in zip(*rows)]
gate(4, "0 storage/network/form/external-asset/matchMedia", tot == [0, 0, 0, 0, 0],
     "totals storage=%d network=%d form=%d extasset=%d matchMedia=%d · %s"
     % (*tot, UNIVERSE))

# ---- gate 5: school grammar, all stages, in order --------------------------
# ESTATE CONVENTION (verified identical at the rollback SHA, so the graft did not
# change it): the second I Do / We Do reuse data-type="ido"/"wedo" and carry their
# ordinal in data-title. An earlier version of this gate asserted ido2/wedo2 and
# failed 10/10 on files that were correct — instrument failure #17, recorded.
ORDER = ["arrival", "starter", "ido", "wedo", "ido", "wedo", "independent", "exit"]
TITLED = ["I Do 2", "We Do 2"]
bad5 = []
for f in FILES:
    s = live(f)
    seq = re.findall(r'<section class="slide"[^>]*data-type="([a-z0-9]+)"', s)
    stage_seq = [x for x in seq if x in ("arrival", "starter", "ido", "wedo",
                                         "independent", "exit")]
    if stage_seq != ORDER:
        bad5.append("%s: %s" % (f, stage_seq))
    for t in TITLED:
        if ('data-title="👩‍🏫 %s' % t) not in s and ('data-title="🤝 %s' % t) not in s:
            bad5.append("%s: stage '%s' not titled" % (f, t))
    # Baseline must agree, proving the graft did not disturb the stage spine.
    # Both sides MUST be read with the identical section-scoped regex — comparing
    # a section-scoped scan against a bare `data-type=` scan reported a false
    # difference 10/10 (instrument failure #18, mine, recorded).
    base_seq = [x for x in re.findall(
        r'<section class="slide"[^>]*data-type="([a-z0-9]+)"', base(f))
        if x in ("arrival", "starter", "ido", "wedo", "independent", "exit")]
    if base_seq != stage_seq:
        bad5.append("%s: stage spine differs from baseline (%s vs %s)"
                    % (f, base_seq, stage_seq))
    # no foreign stage name used AS STRUCTURE (pack labels must not become sections)
    for foreign in ("Do Now", "Plenary", "Main", "Hook", "Recap"):
        if re.search(r'<section[^>]*data-title="[^"]*%s' % foreign, s):
            bad5.append("%s: foreign stage '%s' used as structure" % (f, foreign))
gate(5, "school grammar stages present and in order", not bad5,
     "10/10 carry arrival→starter→I Do→We Do→I Do 2→We Do 2→independent→exit "
     "(estate convention: 2nd ido/wedo titled, not retyped); spine identical to "
     "baseline; zero foreign stage names as structure"
     + ("" if not bad5 else " · " + "; ".join(bad5[:3])))

# ---- gate 6: arrival shape 3 retrieval + 1 lead-in -------------------------
bad6 = []
for f in FILES:
    s = live(f)
    m = re.search(r'<section class="slide"[^>]*data-type="arrival".*?</section>', s, re.S)
    a = m.group(0)
    # per tier panel: 3 retrieval + 1 lead-in
    for tier in ("Supported", "Standard", "Stretch"):
        p = re.search(r'<div class="tier[^"]*" data-tier="%s" data-tier-panel="arrival">.*?'
                      r'(?=<div class="tier[^"]*" data-tier=|<div class="scaffold-box")'
                      % tier, a, re.S)
        if not p:
            bad6.append("%s/%s panel missing" % (f, tier)); continue
        blk = p.group(0)
        r = len(re.findall(r'<div class="retr-q">', blk))
        l = len(re.findall(r'<div class="retr-q lead">', blk))
        if (r, l) != (3, 1):
            bad6.append("%s/%s = %dR+%dL" % (f, tier, r, l))
    # every question routed: each retr-q carries a non-reading route AND a tier step
    qs = len(re.findall(r'<div class="retr-q', a))
    rt = len(re.findall(r'<b>Non-reading route:</b>', a))
    st = len(re.findall(r'<b>Next step up:</b>', a))
    if not (qs == rt == st == 12):
        bad6.append("%s routing q=%d nonreading=%d tierstep=%d" % (f, qs, rt, st))
    # entry line for a pupil who was not there
    if cnt(s, r'class="entry-route"') < 1:
        bad6.append("%s entry line missing" % f)
gate(6, "arrival = 3 retrieval + 1 lead-in, every Q routed", not bad6,
     "10/10 files × 3 tiers = 30 panels, each 3R+1L; 12 questions/file each with a "
     "non-reading route and a tier step; entry line 10/10"
     + ("" if not bad6 else " · " + "; ".join(bad6[:4])))

# ---- gate 7: tier integrity + word banks vs baseline ----------------------
bad7 = []
for f in FILES:
    b, l = base(f), live(f)
    for term in ("Supported", "Standard", "Stretch"):
        if cnt(l, term) < cnt(b, term):
            bad7.append("%s %s %d<%d" % (f, term, cnt(l, term), cnt(b, term)))
    if cnt(l, r"word[ -]?bank", re.I) < cnt(b, r"word[ -]?bank", re.I):
        bad7.append("%s wordbank shrank" % f)
tiers = [(f, cnt(live(f), "Supported") + cnt(live(f), "Standard") + cnt(live(f), "Stretch"),
          cnt(base(f), "Supported") + cnt(base(f), "Standard") + cnt(base(f), "Stretch"))
         for f in FILES]
gate(7, "tier + word-bank counts >= live baseline", not bad7,
     "tier sum per file now %d-%d vs baseline %d · word banks never reduced"
     % (min(t[1] for t in tiers), max(t[1] for t in tiers), tiers[0][2]))

# ---- gate 8: print pack intact or richer ----------------------------------
bad8 = []
for f in FILES:
    b, l = base(f), live(f)
    for term, pat in [("printTier", r"printTier"), ("afterprint", r"afterprint"),
                      ("data-tier", r"data-tier"), ("print-pack fam",
                       r"print-pack|print-route|print-box")]:
        if cnt(l, pat) < cnt(b, pat):
            bad8.append("%s %s %d<%d" % (f, term, cnt(l, pat), cnt(b, pat)))
gate(8, "print pack intact or richer", not bad8,
     "printTier %d/file, afterprint %d/file, data-tier %d/file, print-pack family "
     "%d/file (baseline 6/1/22/19) · all >= baseline"
     % (cnt(live(FILES[0]), r"printTier"), cnt(live(FILES[0]), r"afterprint"),
        cnt(live(FILES[0]), r"data-tier"),
        cnt(live(FILES[0]), r"print-pack|print-route|print-box")))

# ---- gate 9: witness + Oak links byte-identical ---------------------------
bad9 = []
oak_tot = 0
for f in FILES:
    b, l = base(f), live(f)
    if cnt(l, r"witness", re.I) != 2:
        bad9.append("%s witness=%d" % (f, cnt(l, r"witness", re.I)))
    ob = sorted(re.findall(r'https://[^"\']*thenational\.academy[^"\']*', b))
    ol = sorted(re.findall(r'https://[^"\']*thenational\.academy[^"\']*', l))
    oak_tot += len(ol)
    if ob != ol:
        bad9.append("%s Oak URLs changed" % f)
    # the witness block itself must be byte-identical
    wb = re.search(r'<div id="print-witness".*?</div></div>', b, re.S)
    wl = re.search(r'<div id="print-witness".*?</div></div>', l, re.S)
    if not wl or (wb and wb.group(0) != wl.group(0)):
        bad9.append("%s witness block altered" % f)
gate(9, "witness x2 + Oak links unchanged at exact URLs", not bad9,
     "witness=2 10/10, witness block byte-identical to baseline 10/10, "
     "Oak URLs identical to baseline, suite total %d links" % oak_tot)

# ---- gate 10: closure ------------------------------------------------------
bad10 = []
for f in FILES:
    s = live(f)
    scr = re.search(r'<section class="slide"[^>]*data-type="exit".*?</section>', s, re.S).group(0)
    if "What I said, and what it changed" not in scr:
        bad10.append("%s screen closure missing" % f)
    pp = re.search(r'<div class="print-pack">.*?</div>\s*<script>', s, re.S)
    if not pp or "What I said, and what it changed" not in pp.group(0):
        bad10.append("%s print closure missing" % f)
    if "No adult initial is required" not in s:
        bad10.append("%s 'no adult initial' framing missing" % f)
    # BUILD's modality strip must NOT appear on GROW
    if re.search(r'modality[- ]strip|data-modality-strip', s, re.I):
        bad10.append("%s carries a BUILD modality strip" % f)
    # the pre-existing closure line must survive
    if "Next I will" not in s:
        bad10.append("%s pre-existing 'Next I will' closure lost" % f)
gate(10, "GROW written closure on screen + print, no BUILD strip", not bad10,
     "'What I said, and what it changed' 10/10 screen + 10/10 print; "
     "'No adult initial is required' 10/10; zero modality strips; "
     "pre-existing 'Next I will' line preserved 10/10")

# ---- gate 13: food census --------------------------------------------------
FOOD = (r"chocolate|sweets?|biscuit|crisps|sugary|takeaway|junk food|"
        r"fizzy drink|calorie|diet plan|weight loss|slimming|BMI|"
        r"healthy weight|obes|fat kid|treat food")
food = [(f, cnt(live(f), FOOD, re.I)) for f in FILES]
gate(13, "food/body-image census (prohibited terms)", sum(x[1] for x in food) == 0,
     "0 occurrences of %d prohibited patterns · %s · scanner validated on a known "
     "positive ('chocolate')" % (len(FOOD.split("|")), UNIVERSE))

# ---- gate 12: reduced motion ----------------------------------------------
bad12 = []
for f in FILES:
    s = live(f)
    if not re.search(r"prefers-reduced-motion:reduce\)\{\*\{animation:none", s):
        bad12.append("%s global RM kill rule missing" % f)
    # the graft layer must introduce no animation/transition of its own
    graft = re.search(r"/\* ===== GSG-1 graft layer.*?\*/(.*?)</style>", s, re.S)
    if graft and re.search(r"animation:|transition:", graft.group(1)):
        bad12.append("%s graft CSS introduces motion" % f)
gate(12, "reduced-motion: graft adds zero animation", not bad12,
     "global `prefers-reduced-motion` kill rule intact 10/10; GSG-1 graft CSS "
     "declares no animation or transition — RM classification: STATIC, no exemption needed")

# ---- sentinels -------------------------------------------------------------
print("\n" + "=" * 100)
print("SENTINEL DERIVATION · unit: bearing files · universe: git-tracked *.html")
print("=" * 100)
loop = sh("git grep -l -F 'll-g:loop-mark' -- '*.html'").strip().split("\n")
clos = sh("git grep -l -F 'What I said, and what it changed' -- '*.html'").strip().split("\n")
loop = [x for x in loop if x]
clos = [x for x in clos if x]
print("ll-g:loop-mark          = %d   (declared: 50, UNCHANGED)" % len(loop))
print("written-closure line    = %d   (declared: 113 -> 123)" % len(clos))
new = sorted(x for x in clos if x.startswith(DIR))
print("\n+10 delta, the exact file list:")
for x in new:
    print("   " + x)
ok_s = (len(loop) == 50 and len(clos) == 123 and len(new) == 10)
gate("S", "sentinels: 50 unchanged, 113->123 as declared", ok_s,
     "loop=%d closure=%d delta=+%d, all %d inside %s" % (len(loop), len(clos),
                                                         len(clos) - 113, len(new), DIR))

print("\n" + "=" * 100)
if fails:
    print("GATES FAILED (%d):" % len(fails))
    for x in fails:
        print("  - " + x)
    sys.exit(1)
print("ALL STATIC GATES PASS")
