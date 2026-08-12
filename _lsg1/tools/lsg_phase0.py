#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LSG-1 Phase 0 census. Unit and universe stated on every row.

Print dialect note: LAUNCH uses the BUILD-family dialect (`pp`, `proute`) PLUS
its own `printpack`/`pline`/`pidline`/`pentry` — a THIRD dialect, distinct from
both BUILD's pp/proute-only and GROW's print-pack/print-route. Counting LAUNCH
with the GROW dialect returns a false low; that is what the three-dialect
warning is about.
"""
import re, os, subprocess, glob, json, sys

REPO = "/home/user/Lessons"
DIR = "Science_Teesside/Launch/v3_40min"
PACK = "/tmp/claude-0/-home-user-Lessons/8ffd7f98-50c8-5e7d-a4b6-c4c2af1f9aec/scratchpad/lpack"

PRINT_FAMILY = (r'\bpp\b|\bproute\b|\bpline\b|\bpidline\b|\bpentry\b|'
                r'printpack|print-section|print-witness|printTier|afterprint|'
                r'data-print-tier|data-tier')

# Mark-scheme prohibitions. Every hit is CONTEXT-READ before it becomes a finding
# (the W7L2 caution-card precedent).
MARKS = (r'mark scheme|markscheme|mark allocation|\bAO[1-3]\b|band descriptor|'
         r'grade boundar|\[\s*\d+\s*marks?\s*\]|\(\s*\d+\s*marks?\s*\)|'
         r'award \d+ mark|out of \d+ marks')


def live_files():
    return sorted(glob.glob(os.path.join(REPO, DIR, "SCI_L_W*L*.html")))


def pack_files():
    return sorted(f for f in glob.glob(os.path.join(PACK, "SCI_L_W*L*.html"))
                  if not f.endswith("-1.html"))


def n(s, pat, flags=0):
    return len(re.findall(pat, s, flags))


def sh(c):
    return subprocess.run(c, shell=True, cwd=REPO, capture_output=True, text=True).stdout


print("=" * 104)
print("LSG-1 PHASE 0 · every count carries a unit and a universe")
print("=" * 104)

LF, PF = live_files(), pack_files()
print("universe A = the %d live LAUNCH v3_40min lesson files" % len(LF))
print("universe B = the %d unsuffixed loose pack lesson files (twins are one artefact)"
      % len(PF))
print()

rows = []
for p in LF:
    s = open(p, encoding="utf-8").read()
    rows.append(dict(
        f=os.path.basename(p)[6:],
        closure=n(s, r'What I said, and what it changed'),
        nosig=n(s, r'(?i)no adult (signature|initial)|No signature|no initials'),
        witness=n(s, r'(?i)witness'),
        pfam=n(s, PRINT_FAMILY),
        ptier=n(s, r'printTier'),
        aft=n(s, r'afterprint'),
        sup=n(s, r'Supported'), std=n(s, r'Standard'), stg=n(s, r'Stretch'),
        wbank=n(s, r'(?i)word[ -]?bank'),
        oak=n(s, r'thenational\.academy'),
        marks=n(s, MARKS, re.I),
        aut1w2=n(s, r'Aut1·W2'),
        baselinepack=n(s, r'Baseline_Weeks'),
        storage=n(s, r'localStorage|sessionStorage|indexedDB'),
        net=n(s, r'fetch\(|XMLHttpRequest|sendBeacon|WebSocket'),
        form=n(s, r'<form|form-action'),
        ext=n(s, r'href="assets/|src="assets/|href="http[^"]*\.css|src="http[^"]*\.js'),
        mm=n(s, r'matchMedia'),
    ))

hdr = ("FILE", "clos", "nosig", "witn", "pFam", "pTier", "aft", "Sup", "Std", "Str",
       "tierΣ", "wbank", "oak", "mark")
print(("%-40s" + "%6s" * 13) % hdr)
for r in rows:
    print(("%-40s" + "%6d" * 13) % (r["f"][:38], r["closure"], r["nosig"], r["witness"],
                                    r["pfam"], r["ptier"], r["aft"], r["sup"], r["std"],
                                    r["stg"], r["sup"] + r["std"] + r["stg"],
                                    r["wbank"], r["oak"], r["marks"]))

print()
print("RUNTIME · universe A · totals across all 15:")
for k, lbl in (("storage", "storage"), ("net", "network"), ("form", "form"),
               ("ext", "external CSS/JS/assets"), ("mm", "matchMedia")):
    print("   %-24s %d" % (lbl, sum(r[k] for r in rows)))

print()
print("BASELINE · universe A · totals:")
print("   Aut1·W2 occurrences      %d" % sum(r["aut1w2"] for r in rows))
print("   Baseline_Weeks links     %d" % sum(r["baselinepack"] for r in rows))

print()
print("PACK · universe B · totals across all 15:")
pk = []
for p in PF:
    s = open(p, encoding="utf-8").read()
    pk.append(dict(closure=n(s, r'What I said, and what it changed'),
                   witness=n(s, r'(?i)witness'),
                   pfam=n(s, PRINT_FAMILY),
                   storage=n(s, r'localStorage|sessionStorage|indexedDB'),
                   net=n(s, r'fetch\(|XMLHttpRequest|sendBeacon|WebSocket'),
                   form=n(s, r'<form|form-action'),
                   ext=n(s, r'href="assets/|src="assets/'),
                   mm=n(s, r'matchMedia'),
                   marks=n(s, MARKS, re.I)))
for k in ("closure", "witness", "pfam", "storage", "net", "form", "ext", "mm", "marks"):
    print("   %-24s %d" % (k, sum(x[k] for x in pk)))

print()
print("SENTINELS · unit: bearing files · universe: git-tracked *.html (BSG-1 ratified)")
loop = [x for x in sh("git grep -l -F 'll-g:loop-mark' -- '*.html'").split("\n") if x]
clos = [x for x in sh("git grep -l -F 'What I said, and what it changed' -- '*.html'").split("\n") if x]
print("   ll-g:loop-mark        = %d" % len(loop))
print("   written-closure line  = %d" % len(clos))
print("   LAUNCH v3_40min files inside the closure set: %d (expect 15)"
      % len([x for x in clos if x.startswith(DIR)]))
print("   BUILD  v3_40min files inside the closure set: %d (expect 0)"
      % len([x for x in clos if x.startswith("Science_Teesside/Build/v3_40min")]))
print("   GROW   v3_40min files inside the closure set: %d (expect 10)"
      % len([x for x in clos if x.startswith("Science_Teesside/Grow/v3_40min")]))

json.dump(rows, open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                  "lsg_live_census.json"), "w"), indent=1)
