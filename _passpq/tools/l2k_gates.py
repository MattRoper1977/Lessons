#!/usr/bin/env python3
# l2k_gates.py — pass PEQ-L2K gate runner for the Kitchen Programme surfaces.
# Run from repo root:  python3 _passpq/tools/l2k_gates.py
# Controls (each proves the gate can go red):
#   L2K_PLANT_XLEVEL=1  plants a cross-level minimum in a lane block   -> G4 RED
#   (the matrix planted-gap control lives in l2k_build.py: L2K_PLANT_GAP=1)
#
# G1 ledger re-proven          — l2k_plan.build() asserts every sum, milestone, window
# G2 pages match the ledger    — rebuild to temp, byte-diff against committed pages
# G3 xlsx twin value-identical — rebuilt workbook's cell values == committed workbook's
# G4 no cross-level minimum    — every lane-tagged sheet carries ONLY its lane's unit
#                                codes and its lane's Communication activity minima
# G5 required statements       — sensitivity table · measured deck-GLH method ·
#                                L1 14-of-15 named · ThSk/CrTh lane split · working towards

import importlib.util, json, os, re, sys, tempfile, subprocess

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
KIT = os.path.join(ROOT, "GROW_ASDAN", "PEQ_L2_Kitchen")
fails = []

def gate(name, ok, detail=""):
    print(f"{'PASS' if ok else 'FAIL'}  {name}" + (f" — {detail}" if detail else ""))
    if not ok: fails.append(name)

# G1 — re-prove the ledger
def load(modname, path):
    spec = importlib.util.spec_from_file_location(modname, path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m
try:
    plan = load("l2k_plan", os.path.join(ROOT, "_passpq", "tools", "l2k_plan.py"))
    plan.build()
    gate("G1 ledger re-proven (sums, milestones, windows)", True)
except AssertionError as e:
    gate("G1 ledger re-proven", False, str(e))

# G2 — committed pages == a fresh build
tmp = tempfile.mkdtemp()
env = dict(os.environ); env.pop("L2K_PLANT_GAP", None)
r = subprocess.run([sys.executable, os.path.join(ROOT, "_passpq", "tools", "l2k_build.py")],
                   cwd=ROOT, env={**env, "L2K_OUT": tmp}, capture_output=True, text=True)
# l2k_build writes into the repo; instead verify by re-running and diffing git status
r2 = subprocess.run(["git", "status", "--porcelain", "GROW_ASDAN/PEQ_L2_Kitchen"],
                    cwd=ROOT, capture_output=True, text=True)
gate("G2 committed pages match a fresh build (no drift after rebuild)",
     r.returncode == 0 and r2.stdout.strip() == "", r2.stdout.strip()[:200])

# G3 — xlsx twin values match the ledger JSON
try:
    import openpyxl
    led = json.load(open(os.path.join(ROOT, "_passpq", "inputs", "peq_l2k_year_ledger.json")))
    wb = openpyxl.load_workbook(os.path.join(ROOT, "_passpq", "inputs", "PEQ_L2K_YearPlan_2026-27.xlsx"))
    ws = wb["UnitLedgers"]
    ok = True; seen = 0
    for row in ws.iter_rows(min_row=2, values_only=True):
        lane, code, cr, glh, ledger_h, wk = row
        skill = next(sk for sk, u in led["units"][lane].items() if u["code"] == code)
        ok &= (led["units"][lane][skill]["glh"] == glh and
               led["lanes"][lane]["totals_min"][skill] / 60.0 == ledger_h and
               led["lanes"][lane]["complete_week"][skill] == wk)
        seen += 1
    gate("G3 xlsx twin value-identical to the ledger JSON", ok and seen == 18, f"{seen} unit rows")
except Exception as e:
    gate("G3 xlsx twin value-identical", False, repr(e))

# G4 — no cross-level minimum: lane blocks carry only their lane's codes + minima
LANE_CODES = {"E3": {"ComSkE3", "DecMkSkE3", "LSkE3", "TmWkSkE3", "ThSkE3", "WellbLeE3"},
              "L1": {"ComSk1", "DecMkSk1", "LSk1", "TmWkSk1", "ThSk1", "WellbLe1"},
              "L2": {"ComSk2", "DecMkSk2", "LSk2", "TmWkSk2", "CrThSk2", "WellbLe2"}}
COM_MIN = {"E3": ">=2 min", "L1": ">=3 min", "L2": ">=4 min"}
ALL_CODES = set().union(*LANE_CODES.values())
bad = []
plant = os.environ.get("L2K_PLANT_XLEVEL") == "1"
for fn in ("Plan_Templates.html", "Evidence_Sheets.html", "Assessor_Checklists.html"):
    s = open(os.path.join(KIT, fn), encoding="utf-8").read()
    for m in re.finditer(r'<div class="sheet lane-(E3|L1|L2)">(.*?)</div>\n?', s, re.S):
        lane, block = m.group(1), m.group(2)
        if plant and lane == "E3" and "ComSkE3" in block:
            block = block.replace("100 words", "500 words", 1)  # planted L2 figure on an E3 surface
        codes = set(re.findall(r'\b(?:Com|DecMk|L|TmWk|Th|CrTh|Wellb)\w*Sk\w*\b|\b(?:ComSk|DecMkSk|LSk|TmWkSk|ThSk|CrThSk|WellbLe)(?:E3|1|2)\b', block))
        codes = {c for c in codes if c in ALL_CODES}
        alien = codes - LANE_CODES[lane]
        if alien: bad.append(f"{fn}: lane-{lane} block carries {sorted(alien)}")
        # the Communication activity minima must be the lane's own figures
        if "presentation" in block and "words" in block:
            want = {"E3": "100 words", "L1": "250 words", "L2": "500 words"}[lane]
            others = {v for k, v in {"E3": "100 words", "L1": "250 words", "L2": "500 words"}.items() if k != lane}
            if want not in block or any(o in block for o in others):
                bad.append(f"{fn}: lane-{lane} Communication minima wrong (expected {want})")
gate("G4 no cross-level minimum on any lane surface", not bad, "; ".join(bad[:4]))

# G5 — required statements present
sow = open(os.path.join(KIT, "Scheme_of_Work.html"), encoding="utf-8").read()
checks = {
 "sensitivity table": "Sensitivity: what each weekly commitment",
 "deck GLH by measurement + method": "40-minute period each = 480 min = 8.0 GLH",
 "programmed-vs-slot honesty": "PROGRAM 53 min",
 "L1 14-of-15 named": "14-of-15",
 "ThSk vs CrTh split": "only the L2 lane plans <b>CrThSk2</b>",
 "working towards": "working towards",
 # PEQ-YEAR-3 §2/§3: the timetable is now EVIDENCE. Every string this gate used to
 # assert - "seven timetabled 40-minute periods", the measured-band-plus-ruling
 # provenance, "GROW and LAUNCH are NOT establishable" - names something this pass
 # retired. Asserting them now would assert a falsehood, which is the same failure
 # that once left a self-contradicting sentence on this page. Replaced by what is
 # load-bearing at the MEASURED rates.
 "measured from the timetable": "MEASURED from the school's own 2026-27 timetable",
 "classification rule printed": "The classification rule, printed so it can be argued with",
 "per-room table present": "Measured, per room",
 "no lane inherits another's rate": "not because one figure was copied onto the others",
 "Build's zero floor stated": "Build has no explicitly ASDAN-labelled slot at all",
 "reachability at floor and ceiling": "What each room's real hours can reach",
 "the unreachable stated, not implied": "Build reaches nothing at all",
 "cooking capacity stated": "cooking-labelled slot",
 "kitchen slots named per lane": "the kitchen is a context, not a room booking",
 "teacher attribution not assumed": "confirm who teaches the cooking slot",
 "GROW/LAUNCH question closed by evidence": "the open question is closed by evidence",
 "co-delivery still withdrawn": "co-delivery claim stays withdrawn",
 "QA headroom declared, not claimed": "never claimed against a unit",
}
# Whitespace in HTML is insignificant, and the generated prose wraps where the
# source wraps - so a required sentence can be present and correct on the page
# while a raw substring test misses it because a newline fell mid-phrase. Compare
# on collapsed whitespace instead of reflowing authored prose to suit the gate.
import re as _re
_flat = lambda t: _re.sub(r"\s+", " ", t)
sow_f = _flat(sow)
missing = [k for k, v in checks.items() if _flat(v) not in sow_f]
# PEQ-YEAR-2 §4: G5 read only the year map, so the handover and the ledger could
# drift from it unwatched -- and did (the handover's hours section carried no
# measured-vs-ruled split at all, and the generated HTML had no hours section
# while the markdown promised "same content"). Gate all three.
hand_md = open(os.path.join(KIT, "COOKING_HANDOVER.md"), encoding="utf-8").read()
hand_html = open(os.path.join(KIT, "Cooking_Handover.html"), encoding="utf-8").read()
for label, text in (("handover .md", hand_md), ("handover .html", hand_html)):
    for k, v in {"measured from the timetable": "measured from the school's own timetable",
                 "slot table present": "Your slots, named",
                 "cooking slot teacher lodged": "confirm who teaches the cooking slot",
                 "the cooking slot named": "PfA / cooking"}.items():
        if _flat(v) not in _flat(text):
            missing.append(f"{label}: {k}")
for k, v in {"source cell cited on kitchen slots": "[Build Timetable]!D11",
             "owner-decision slots not absorbed": "owner-decision",
             "calendar evidence split": "Spring and summer have NO term dates"}.items():
    if _flat(v) not in sow_f:
        missing.append(k)
mtx = open(os.path.join(KIT, "Criteria_Coverage_Matrix.html"), encoding="utf-8").read()
if "174 criteria mapped, 0 gaps" not in mtx: missing.append("matrix zero-gap line")
staff = open(os.path.join(KIT, "Staff_Kitchen_Guide.html"), encoding="utf-8").read()
for k, v in {"safeguarding DecMk box": "Safeguarding — Decision making",
             "safeguarding Wellb box": "Safeguarding — Wellbeing in learning",
             "risk assessment school-side": "risk assessment is named school-side",
             "no-diet-framing rule": "no diet, calorie, weight or body framing"}.items():
    if v not in staff: missing.append(k)
gate("G5 required statements present on the surfaces", not missing, "; ".join(missing))

print()
if fails:
    print(f"NOT ALL GREEN — {len(fails)} failing: {fails}"); sys.exit(1)
print("ALL GREEN")
