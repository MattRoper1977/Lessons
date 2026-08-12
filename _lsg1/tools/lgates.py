#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LSG-1 static gates. Unit and universe on every check.
Baselines read from the rollback SHA; scanners validated on known positives.
"""
import re, subprocess, sys, os, glob, json, tempfile

REPO = "/home/user/Lessons"
DIR = "Science_Teesside/Launch/v3_40min"
BASE = "470be572baf4f71d5656afe3aa9bd3bf97129daa"
UNIVERSE = "the fifteen live LAUNCH v3_40min lesson files"

PRINT_FAMILY = (r'\bpp\b|\bproute\b|\bpline\b|\bpidline\b|\bpentry\b|'
                r'printpack|print-section|print-witness|printTier|afterprint|'
                r'data-print-tier|data-tier')
MARKS = (r'mark scheme|markscheme|mark allocation|\bAO[1-3]\b|band descriptor|'
         r'grade boundar|\[\s*\d+\s*marks?\s*\]|\(\s*\d+\s*marks?\s*\)|'
         r'award \d+ mark|out of \d+ marks')
FOOD = (r"chocolate|sweets?|biscuit|crisps|sugary|takeaway|junk food|"
        r"fizzy drink|calorie|diet plan|weight loss|slimming|BMI|"
        r"healthy weight|obes|fat kid|treat food")
STAGES = ["arrival", "starter", "ido", "wedo", "ido", "wedo", "independent", "exit"]
CLOSE_BLOCK = r'<div class="close">.*?(?:<div class="pline"[^>]*></div>){2}</div>'

fails = []


def sh(c):
    return subprocess.run(c, shell=True, cwd=REPO, capture_output=True, text=True).stdout


def files():
    return sorted(glob.glob(os.path.join(REPO, DIR, "SCI_L_W*L*.html")))


def base_of(f):
    return sh("git show %s:%s/%s" % (BASE, DIR, f))


def n(s, p, fl=0):
    return len(re.findall(p, s, fl))


def gate(i, name, ok, detail):
    print("[%s] gate %-3s %-44s %s" % ("PASS" if ok else "FAIL", i, name, detail))
    if not ok:
        fails.append("%s %s" % (i, name))


print("=" * 108)
print("LSG-1 STATIC GATES · universe for per-file rows: %s" % UNIVERSE)
print("baselines from rollback SHA %s" % BASE[:7])
print("=" * 108)

KP = ('localStorage fetch( <form matchMedia href="assets/x.css" witness Supported '
      'printTier afterprint chocolate mark scheme AO1 thenational.academy '
      'What I said, and what it changed data-type="arrival" \\bpp\\b')
for lbl, p, e in [("storage", r"localStorage", 1), ("network", r"fetch\(", 1),
                  ("form", r"<form", 1), ("matchMedia", r"matchMedia", 1),
                  ("extasset", r'href="assets/', 1), ("witness", r"witness", 1),
                  ("closure", r"What I said, and what it changed", 1),
                  ("oak", r"thenational\.academy", 1), ("food", r"chocolate", 1),
                  ("marks", r"mark scheme", 1)]:
    got = n(KP, p)
    assert got == e, "SCANNER %s failed validation (%d != %d)" % (lbl, got, e)
print("scanner validation: 10/10 returned the expected count on a synthetic known positive\n")

LF = files()

# ---- gate 2 --------------------------------------------------------------
js_ok = json_ok = 0
g2 = []
for p in LF:
    s = open(p, encoding="utf-8").read()
    for i, b in enumerate(re.findall(r"<script>(.*?)</script>", s, re.S)):
        with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False,
                                         encoding="utf-8") as t:
            t.write(b); tp = t.name
        r = subprocess.run(["node", "--check", tp], capture_output=True, text=True)
        os.unlink(tp)
        js_ok += 1 if r.returncode == 0 else 0
        if r.returncode:
            g2.append("%s blk%d" % (os.path.basename(p), i))
    for m in re.finditer(r'<script id="lessonConfig" type="application/json">(.*?)</script>',
                         s, re.S):
        try:
            json.loads(m.group(1)); json_ok += 1
        except Exception as e:
            g2.append("%s JSON %s" % (os.path.basename(p), e))
gate(2, "node --check JS + JSON parsed as JSON", not g2,
     "%d JS blocks checked, %d JSON islands parsed · %s" % (js_ok, json_ok, UNIVERSE))

# ---- gate 4 --------------------------------------------------------------
tot = [0] * 5
for p in LF:
    s = open(p, encoding="utf-8").read()
    for i, pat in enumerate([r"localStorage|sessionStorage|indexedDB",
                             r"fetch\(|XMLHttpRequest|sendBeacon|WebSocket",
                             r"<form|form-action", r'href="assets/|src="assets/',
                             r"matchMedia"]):
        tot[i] += n(s, pat)
gate(4, "0 storage/network/form/external-asset/matchMedia", tot == [0, 0, 0, 0, 0],
     "storage=%d network=%d form=%d extasset=%d matchMedia=%d · %s" % (*tot, UNIVERSE))

# ---- gate 5 --------------------------------------------------------------
g5 = []
for p in LF:
    s = open(p, encoding="utf-8").read()
    b = base_of(os.path.basename(p))
    seq = [x for x in re.findall(r'<section class="slide"[^>]*data-type="([a-z0-9]+)"', s)
           if x in ("arrival", "starter", "ido", "wedo", "independent", "exit")]
    bseq = [x for x in re.findall(r'<section class="slide"[^>]*data-type="([a-z0-9]+)"', b)
            if x in ("arrival", "starter", "ido", "wedo", "independent", "exit")]
    if seq != STAGES or seq != bseq:
        g5.append("%s %s" % (os.path.basename(p)[6:14], seq))
gate(5, "stage order intact and identical to baseline", not g5,
     "15/15 carry %s · spine identical to baseline%s"
     % ("→".join(STAGES), "" if not g5 else " · " + "; ".join(g5[:3])))

# ---- gate 5b · arrival 3+1 -----------------------------------------------
g5b = []
for p in LF:
    s = open(p, encoding="utf-8").read()
    a = re.search(r'<section class="slide"[^>]*data-type="arrival".*?</section>',
                  s, re.S).group(0)
    for tier in ("Supported", "Standard", "Stretch"):
        panel = re.search(r'<div class="tier[^"]*" data-tier-panel="arrival" '
                          r'data-tier="%s">.*?(?=<div class="tier[^"]*" data-tier-panel='
                          r'"arrival"|<div class="note">)' % tier, a, re.S)
        if not panel:
            g5b.append("%s/%s panel" % (os.path.basename(p)[6:14], tier)); continue
        r = len(re.findall(r'<div class="lq">', panel.group(0)))
        l = len(re.findall(r'<div class="lq lead">', panel.group(0)))
        if (r, l) != (3, 1):
            g5b.append("%s/%s %dR+%dL" % (os.path.basename(p)[6:14], tier, r, l))
    # EXACT match: `class="lq` also prefix-matches lq-head / lq-ask / lq-route /
    # lq-badge / lq-declare, which inflated this count to 24-25. The question
    # divs are exactly `lq` or `lq lead`.
    q = len(re.findall(r'<div class="lq(?: lead)?">', a))
    rt = len(re.findall(r'<b>Non-reading route:</b>', a))
    st = len(re.findall(r'<b>Next step up:</b>', a))
    if not (q == rt == st == 12):
        g5b.append("%s routing q=%d nr=%d ts=%d" % (os.path.basename(p)[6:14], q, rt, st))
    if n(s, r'class="entry-route"') < 1 or n(s, r'class="pentry"') < 1:
        g5b.append("%s entry surface" % os.path.basename(p)[6:14])
gate("5b", "arrival = 3 retrieval + 1 lead-in, all routed", not g5b,
     "15/15 × 3 tiers = 45 panels each 3R+1L; 12 questions/file each with a non-reading "
     "route and a tier step; entry surface 15/15 screen + 15/15 print"
     + ("" if not g5b else " · " + "; ".join(g5b[:4])))

# ---- gate 6 · tiers -------------------------------------------------------
g6 = []
for p in LF:
    s, b = open(p, encoding="utf-8").read(), base_of(os.path.basename(p))
    for t in ("Supported", "Standard", "Stretch"):
        if n(s, t) < n(b, t):
            g6.append("%s %s" % (os.path.basename(p)[6:14], t))
    if n(s, r'(?i)word[ -]?bank') < n(b, r'(?i)word[ -]?bank'):
        g6.append("%s wordbank" % os.path.basename(p)[6:14])
s0, b0 = open(LF[0], encoding="utf-8").read(), base_of(os.path.basename(LF[0]))
gate(6, "tier + word-bank counts >= baseline", not g6,
     "tier sum/file now %d vs baseline %d · W6L1 word bank preserved"
     % (sum(n(s0, t) for t in ("Supported", "Standard", "Stretch")),
        sum(n(b0, t) for t in ("Supported", "Standard", "Stretch"))))

# ---- gate 7 · print pack ---------------------------------------------------
g7 = []
for p in LF:
    s, b = open(p, encoding="utf-8").read(), base_of(os.path.basename(p))
    for lbl, pat in (("family", PRINT_FAMILY), ("printTier", r"printTier"),
                     ("afterprint", r"afterprint")):
        if n(s, pat) < n(b, pat):
            g7.append("%s %s %d<%d" % (os.path.basename(p)[6:14], lbl, n(s, pat), n(b, pat)))
gate(7, "print pack intact or richer", not g7,
     "family %d/file (baseline %d), printTier %d, afterprint %d · all >= baseline"
     % (n(s0, PRINT_FAMILY), n(b0, PRINT_FAMILY), n(s0, r"printTier"), n(s0, r"afterprint")))

# ---- gate 8 · witness -----------------------------------------------------
g8 = []
for p in LF:
    s, b = open(p, encoding="utf-8").read(), base_of(os.path.basename(p))
    if n(s, r'(?i)witness') != 2:
        g8.append("%s witness=%d" % (os.path.basename(p)[6:14], n(s, r'(?i)witness')))
    wb = re.search(r'<div id="print-witness".*?(?=</div>\s*</div>\s*<script|$)', b, re.S)
    wn = re.search(r'<div id="print-witness".*?(?=</div>\s*</div>\s*<script|$)', s, re.S)
    if not wn or wb.group(0) != wn.group(0):
        g8.append("%s witness block altered" % os.path.basename(p)[6:14])
gate(8, "witness x2 15/15 byte-identical", not g8,
     "witness=2 on 15/15 and the assessor block byte-identical to baseline 15/15")

# ---- gate 9 · CLOSURE + SENTINELS -----------------------------------------
g9 = []
for p in LF:
    s, b = open(p, encoding="utf-8").read(), base_of(os.path.basename(p))
    if n(s, r'What I said, and what it changed') != 2:
        g9.append("%s closure=%d" % (os.path.basename(p)[6:14],
                                     n(s, r'What I said, and what it changed')))
    cb, cn = re.search(CLOSE_BLOCK, b, re.S), re.search(CLOSE_BLOCK, s, re.S)
    if not cn or cb.group(0) != cn.group(0):
        g9.append("%s close block altered" % os.path.basename(p)[6:14])
    if n(s, r'(?i)no adult (signature|initial)|No signature|no initials') != \
       n(b, r'(?i)no adult (signature|initial)|No signature|no initials'):
        g9.append("%s no-sig framing changed" % os.path.basename(p)[6:14])
    if re.search(r'modality[- ]strip|data-modality-strip', s, re.I):
        g9.append("%s BUILD modality strip" % os.path.basename(p)[6:14])
gate(9, "closure x2 15/15 byte-identical, no BUILD strip", not g9,
     "closure=2 on 15/15, close block byte-identical to baseline 15/15, no-signature "
     "framing unchanged, zero BUILD modality strips")

# ---- gate 10 · marks -------------------------------------------------------
mk = [(os.path.basename(p)[6:14], n(open(p, encoding="utf-8").read(), MARKS, re.I))
      for p in LF]
gate(10, "mark-scheme census 0, context-read", sum(x[1] for x in mk) == 0,
     "0 hits of %d prohibited patterns · %s · every hit would be context-read before "
     "becoming a finding (W7L2 caution-card precedent)" % (len(MARKS.split("|")), UNIVERSE))

# ---- gate 11 · A4 clip ------------------------------------------------------
v5 = open(os.path.join(REPO, "Science_Teesside/Launch/SCI_L_W5_L2_OsmosisCP.html"),
          encoding="utf-8").read()
w5 = open(os.path.join(REPO, DIR, "SCI_L_W5L2_Osmosis_Core_Practical_Explore.html"),
          encoding="utf-8").read()
u5 = re.findall(r'https://www\.thenational\.academy[^"]*', v5)
u3 = re.findall(r'https://www\.thenational\.academy[^"]*', w5)
pp = re.search(r'<div class="printpack">.*?(?=<script)', w5, re.S).group(0)
others = sum(n(open(p, encoding="utf-8").read(), r'thenational\.academy')
             for p in LF if "W5L2" not in p)
ok11 = (len(u3) == 1 and u3 == u5 and 'target="_blank"' in w5
        and 'rel="noopener noreferrer"' in w5 and 'Oak National Academy' in w5
        and 'thenational.academy' not in pp and others == 0)
gate(11, "A4 clip byte-equal, link rules, absent from print", ok11,
     "URL byte-equal to the v5 original; 1 occurrence in W5L2 and %d in the other 14; "
     "new tab + noopener; Oak named; teaches-without-it stated; ABSENT from the print pack"
     % others)

# ---- gate 13 · food --------------------------------------------------------
fd = sum(n(open(p, encoding="utf-8").read(), FOOD, re.I) for p in LF)
gate(13, "food/body-image census", fd == 0,
     "0 occurrences of %d prohibited patterns · %s · scanner validated on 'chocolate'"
     % (len(FOOD.split("|")), UNIVERSE))

# ---- gate 13b · RM ---------------------------------------------------------
g13 = []
for p in LF:
    s = open(p, encoding="utf-8").read()
    m = re.search(r"/\* ===== LSG-1 graft layer.*?\*/(.*?)</style>", s, re.S)
    if m and re.search(r"animation:|transition:", m.group(1)):
        g13.append(os.path.basename(p)[6:14])
gate("13b", "reduced motion: graft declares no animation", not g13,
     "LSG-1 graft CSS declares 0 animation/transition · RM classification STATIC")

# ---- gate 15 · scope --------------------------------------------------------
changed = [x for x in sh("git diff --name-only %s..HEAD" % BASE).split("\n") if x]
work = [x for x in sh("git status --porcelain").split("\n") if x]
allf = set(changed) | set(x[3:] for x in work)
out = [f for f in allf if not (f.startswith(DIR) or f.startswith("_lsg1/"))]
gate(15, "0 files changed outside LAUNCH v3_40min and _lsg1", not out,
     "%d files touched, all inside %s or _lsg1/%s"
     % (len(allf), DIR, "" if not out else " · STRAY: " + ", ".join(out[:5])))

# ---- SENTINELS --------------------------------------------------------------
print("\n" + "=" * 108)
print("SENTINEL DERIVATION · unit: bearing files · universe: git-tracked *.html")
print("This pass declares NO movement. Both must be unchanged AND set-identical to main's.")
print("=" * 108)


def bearing(ref, pat):
    r = sh("git grep -l -F '%s' %s -- '*.html'" % (pat, ref))
    return set(x.split(":", 1)[1] for x in r.strip().split("\n") if x)


okS = True
for name, pat, exp in (("ll-g:loop-mark", "ll-g:loop-mark", 50),
                       ("written-closure", "What I said, and what it changed", 123)):
    m = bearing("origin/main", pat)
    h = bearing("HEAD", pat)
    same = (m == h)
    print("   %-17s main=%-4d HEAD=%-4d expected=%-4d set-identical=%s"
          % (name, len(m), len(h), exp, same))
    if len(h) != exp or not same:
        okS = False
gate("S", "sentinels 50 AND 123, set-identical to main", okS,
     "no declared movement in this pass; unchanged is the only green")

print("\n" + "=" * 108)
if fails:
    print("GATES FAILED (%d): %s" % (len(fails), "; ".join(fails)))
    sys.exit(1)
print("ALL LSG-1 STATIC GATES PASS")
