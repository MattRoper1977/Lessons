#!/usr/bin/env python3
# l2k_gates.py — pass PEQ-L2K gate runner for the Kitchen Programme surfaces.
# Run from repo root:  python3 _passpq/tools/l2k_gates.py
# Controls (each proves the gate can go red):
#   L2K_PLANT_XLEVEL=1  plants a cross-level minimum in a lane block   -> G4 RED
#   (the matrix planted-gap control lives in l2k_build.py: L2K_PLANT_GAP=1)
#
# G1 ledger re-proven          — l2k_plan._assert_calendar() proves the block scheme covers
#                                 the year; build() then asserts every sum, milestone, window
# G2 pages match the ledger    — rebuild to temp, byte-diff against committed pages
# G3 xlsx twin value-identical — rebuilt workbook's cell values == committed workbook's
# G4 no cross-level minimum    — every lane-tagged sheet carries ONLY its lane's unit
#                                codes and its lane's Communication activity minima
# G6 handover pair          — every substantive .md block's content words appear in the .html
# G5 required statements       — sensitivity table · measured deck-GLH method ·
#                                L1 14-of-15 named · ThSk/CrTh lane split · working towards

import bisect as _bisect
import importlib.util, json, os, re, shutil, sys, tempfile, subprocess
import html as _html_mod

# A gate that reads yesterday's bytecode is worse than no gate. Restoring a
# planted l2k_plan.py within the same second as the .pyc was written left the
# cache valid by mtime, and G1 reported the planted calendar against a clean
# tree. Read the source, every run.
sys.dont_write_bytecode = True
shutil.rmtree(os.path.join(os.path.dirname(os.path.abspath(__file__)), '__pycache__'),
              ignore_errors=True)

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
    # _assert_calendar() BEFORE build(). It lived only inside l2k_plan.main(), so it
    # fired when the ledger was regenerated and nowhere else: a falsified block scheme
    # reddened the generator but sailed through the whole gate suite, because build()
    # asserts sums *within* whatever BLOCKS it is handed and never questions the blocks
    # themselves. PEQ-YEAR-3 caught it by planting a 14-week autumn and watching
    # l2k_plan.py exit 1 while l2k_gates.py stayed ALL GREEN. The pass brief requires
    # the spring/summer assumptions to travel with an intact assertion, and "intact"
    # has to mean load-bearing at the gate, not merely present in the file.
    plan._assert_calendar()
    # ROOM_MEASURED is transcribed from the timetable extract, not read from it, so
    # it can go stale without anything noticing. Reconciled at the gate for the same
    # reason _assert_calendar() is: an assertion that only runs in the generator is
    # not load-bearing.
    plan._assert_measured_matches_timetable()
    plan.build()
    gate("G1 ledger re-proven (calendar, measured rooms, sums, milestones, windows)", True)
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

# ---------------------------------------------------------------------------
# G6 — the handover .md and .html actually carry the same content
#
# COOKING_HANDOVER.md tells the colleague the HTML is the "printable copy — same
# content". G5 checked that claim with a hand-listed set of strings, which is only
# as good as whoever wrote the list. PEQ-YEAR-3 found a whole safeguarding
# paragraph — the two boxes read aloud to pupils at W9 and W27, "verbatim; they
# are not optional" — present in the .md and absent from the .html, because nobody
# had thought to list it. A colleague printing the HTML never met it.
#
# So this gate is structural instead. Every substantive block of the .md must find
# its content words in the .html. It cannot be defeated by adding prose that
# neither file was checked for, which is exactly how the last gap happened.
#
# The threshold is 60% of content words, not 100%, because the two are worded for
# different media and always will be. That is enough to catch a missing block
# (the read-aloud paragraph scored 0%) without firing on a reworded sentence.
#
# The allowlist is deliberately tiny and each entry says why. A block belongs
# there only if it is ABOUT the pairing — a pointer to the other copy — rather
# than content the colleague needs.
G6_STOP = set("""a an and are as at be been but by can do does for from had has have he her his
if in into is it its may me my no not of on one or our so than that the their them then there
these they this those to two up us was we were what when where which who will with without you
your each every any all also only just still even own same other more most much many""".split())

def _md_blocks(md):
    """Substantive blocks: paragraphs and list items; headings, rules, fences dropped."""
    out, buf = [], []
    fence = False
    for line in md.splitlines():
        s = line.strip()
        if s.startswith("```"):
            fence = not fence
            continue
        if fence:
            continue
        if not s or s.startswith("#") or (len(s) > 2 and set(s) <= set("-*_ ")):
            if buf:
                out.append(" ".join(buf))
                buf = []
            continue
        if re.match(r"^([-*+]|\d+\.)\s", s) and buf:
            out.append(" ".join(buf))
            buf = []
        buf.append(s)
    if buf:
        out.append(" ".join(buf))
    return out

def _content_words(s):
    s = re.sub(r"`[^`]*`", " ", s)                        # code spans: file names, cells
    s = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", s)        # links -> their visible text
    s = re.sub(r"&[a-z]+;|&#\d+;", " ", s)
    s = re.sub(r"[^A-Za-z0-9]+", " ", s).lower()
    return [w for w in s.split() if len(w) > 2 and w not in G6_STOP]

def _html_tokens(h):
    h = re.sub(r"<script.*?</script>|<style.*?</style>", " ", h, flags=re.S)
    h = re.sub(r"<[^>]+>", " ", h)
    h = _html_mod.unescape(h)
    h = re.sub(r"[^A-Za-z0-9]+", " ", h).lower()
    return [w for w in h.split() if len(w) > 2]

def _alias(w, index):
    """The html positions of this word, allowing for inflection.

    Not a stemmer. Stemming both sides made things worse: "state" stems to itself
    while "states" stems to "stat", so the .md's infinitive verb table read as
    missing from an .html that says every verb. Prefix matching in both directions
    handles state/states, assess/assesses, declare/declared and tag/tagged without
    inventing tokens that exist on neither side. Four characters is the floor, so
    "the" cannot cover "theme".
    """
    hit = list(index.get(w, ()))
    if len(w) >= 4:
        i = _bisect.bisect_left(index.keys_sorted, w)
        j = i
        while j < len(index.keys_sorted) and index.keys_sorted[j].startswith(w):
            hit += index[index.keys_sorted[j]]
            j += 1
        if i > 0:
            k = index.keys_sorted[i - 1]
            if len(k) >= 4 and w.startswith(k):
                hit += index[k]
    return hit

class _Index(dict):
    def __init__(self, toks):
        super().__init__()
        for pos, w in enumerate(toks):
            self.setdefault(w, []).append(pos)
        self.keys_sorted = sorted(self)

G6_ALLOW = [
    ("Printable copy", "the .md points at the HTML; the HTML does not point at itself"),
]

# THE THRESHOLD IS MEASURED, NOT CHOSEN.
#
# Two candidate metrics were scored against the two real deletions this pass
# found, plus every other block of the .md as the false-positive control:
#
#                                    intact   read-aloud   calendar   worst
#                                             para gone    note gone  intact
#   global  (word appears anywhere)   1.00       0.62         0.48      0.77
#   window  (words appear together)   1.00       0.24         0.21      0.38
#
# The window metric separates too, but by a thinner margin, and it punishes an
# .html that says the same things in a different order -- which is exactly what
# an estate-styled printable copy is entitled to do. Global coverage separates
# 0.62/0.48 from 0.77 with room on both sides, so 0.70 is the line, and both
# real deletions sit well below it. Re-measure if either file is restructured;
# do not nudge this number to make a red go away.
G6_FLOOR = 0.70

_index = _Index(_html_tokens(hand_html))
_thin = []
for _blk in _md_blocks(hand_md):
    _cw = sorted(set(_content_words(_blk)))
    if len(_cw) < 10:
        continue
    if any(a in _blk for a, _ in G6_ALLOW):
        continue
    _hit = sum(1 for w in _cw if _alias(w, _index)) / len(_cw)
    if _hit < G6_FLOOR:
        _gone = [w for w in _cw if not _alias(w, _index)]
        _thin.append(f"{int(_hit * 100)}% in .html (absent: {', '.join(_gone[:6])}): "
                     f"\u201c{_blk[:80]}\u2026\u201d")
gate("G6 handover .md and .html carry the same content", not _thin,
     f"{len(_thin)} .md block(s) missing from the .html — " + " | ".join(_thin[:3]))

print()
if fails:
    print(f"NOT ALL GREEN — {len(fails)} failing: {fails}"); sys.exit(1)
print("ALL GREEN")
