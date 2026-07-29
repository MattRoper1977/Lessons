#!/usr/bin/env python3
"""Pass Q — deterministic verdict-table generator (Tier-1). Emits the ledger rows and
counts from movers.json + the read-derived group/verdict rules, so no count is transcribed."""
import json, sys
d = json.load(open("_passq/tools/movers.json"))
ASSESSED = {"Grow/Slideshows/GROW_HUM_W7_Write_The_Account.html",
            "Launch/Slideshows/LAUNCH_HUM_W7_Source_Assessment.html"}
# 4 worksheet-template files whose print-ko slot holds only a Name/Class/Date header (no organiser)
NO_ORGANISER = {"2 Physics 10/Waves/L4a_Wave_Anatomy.html",
                "biology/L4_Aerobic.html",
                "chemistry/Lesson4b_Gas_Tests_NH3_Cl2.html",
                "chemistry/Lesson5_Flame_Tests.html"}
def suite(f):
    if f.startswith("BUILD_ASDAN") or f.startswith("GROW_ASDAN"): return "ASDAN"
    if f.startswith("Art_Teesside"): return "Art"
    if "HUM" in f: return "Humanities"
    if "BUILD_DT" in f: return "D&T"
    if f.split("/")[0] in ("biology","chemistry","2 Physics 10"): return "Science"
    return "Other"
def group(f):
    if f in ASSESSED: return "A-assessed"
    if suite(f) == "ASDAN": return "B-asdan(R-G05)"
    return "C-body-mover"
def verdict(f):
    if f in NO_ORGANISER: return "NO-ORGANISER"
    return "STILL-TRUE"
rows = sorted(d, key=lambda x: (suite(x["file"]), x["file"]))
from collections import Counter
gc, vc, sc = Counter(), Counter(), Counter()
lines = ["| # | file | suite | group | verdict | KO unchanged since | fix |",
         "|---|---|---|---|---|---|---|"]
for i, x in enumerate(rows, 1):
    f = x["file"]; gc[group(f)] += 1; vc[verdict(f)] += 1; sc[suite(f)] += 1
    lines.append(f"| {i} | `{f}` | {suite(f)} | {group(f)} | {verdict(f)} | `{x['ko_last_change']}` | n/a |")
open("_passq/tools/_table.md","w").write("\n".join(lines)+"\n")
print("TOTAL", len(rows))
print("by suite:", dict(sc))
print("by group:", dict(gc))
print("by verdict:", dict(vc))
print("cardinality group-sum:", sum(gc.values()), "== 114 ->", sum(gc.values())==114)
