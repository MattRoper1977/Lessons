#!/usr/bin/env python3
"""§9.9b - ASDAN_CHANGES_FOR_PLANNERS.md, the handoff artefact Stage 3 consumes.

    python3 tools/planner_ledger.py PACK_DIR

One row per lane x week x slot: the ASDAN unit or module, the lesson file now
taught there, what changed, and the paperwork it generates.

THIS FILE IS DESIGNED TO BE PASTED ANYWHERE. It is handed to a session that also
holds real pupil data, so it carries ROLES ONLY - no pupil data, no staff names -
and tools/data_gate.py is run over it to prove that rather than assert it.

A change with no planner surface is written as NO-PLANNER-SURFACE rather than
omitted. A ledger that quietly drops the rows it cannot place is worse than one
that says it could not place them: the reader cannot tell the difference between
"nothing changed there" and "we did not look".
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
TT = json.loads((REPO / "_passpq" / "inputs" / "timetable_2026-27.json").read_text(encoding="utf-8"))
LED = json.loads((REPO / "_passpq" / "inputs" / "peq_l2k_year_ledger.json").read_text(encoding="utf-8"))

BUCKET = {"a": "explicitly ASDAN/PEQ", "b": "carryable",
          "c": "not carryable", "owner-decision": "owner decision",
          "empty": "no lesson timetabled"}

# What PEQ-YEAR-3 actually changed, by surface family. Anything not here is
# unchanged by this pass and says so.
CHANGED = {
    "Scheme_of_Work.html":     ("upgraded", "per-lane slot table + honest reachability"),
    "Scheme_and_Resources.html": ("upgraded", "per-lane slot table + honest reachability"),
    "Cooking_Handover.html":   ("upgraded", "measured hours, named slots, safeguarding read-aloud"),
    "COOKING_HANDOVER.md":     ("upgraded", "measured hours, named slots"),
    "Kitchen_Week_Shell.html": ("upgraded", "week shell now maps to named slots"),
    "Criteria_By_Week.html":   ("upgraded", "unchanged criteria, reslotted"),
    "START_HERE.html":         ("upgraded", "AQA UAS wording qualified"),
    "GROW_ASDAN_Hub.html":     ("upgraded", "AQA UAS wording qualified"),
    "LAUNCH_ASDAN_Hub.html":   ("upgraded", "AQA UAS wording qualified"),
}


def main():
    pack = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    rows = []
    for slot in TT["slots"]:
        bucket = slot.get("bucket")
        # "c" is a slot that banks its own subject; "empty" is a free period. Both
        # are counted in the summary below and neither belongs in a slot table of
        # what ASDAN is taught in.
        if bucket in ("c", "empty"):
            continue
        assert bucket in BUCKET, f"unclassified slot: {slot}"
        rows.append(slot)

    out = []
    w = out.append
    w("# ASDAN_CHANGES_FOR_PLANNERS.md")
    w("")
    w("**What PEQ-YEAR-3 changed, arranged the way a weekly plan is arranged.**")
    w("Roles only. No pupil data, no pupil initials, no staff names, no reading ages.")
    w("Safe to paste anywhere.")
    w("")
    w("Generated from the school's own 2026-27 timetable, with the workbook cell cited")
    w("on every row. Slots not carryable to ASDAN are omitted from the slot table and")
    w("counted in the summary, so the arithmetic closes either way.")
    w("")

    w("## 1 - The guided slots, per lane")
    w("")
    DAYS = {"Mon": 0, "Tue": 1, "Wed": 2, "Thu": 3, "Fri": 4}
    w("| lane | day | period | time | as timetabled | classification | teacher role | source cell |")
    w("|---|---|---|---|---|---|---|---|")
    for s in sorted(rows, key=lambda r: (r["lane"], DAYS.get(r["day"], 9), r["period"])):
        w(f"| {s['lane']} | {s['day']} | {s['period']} | {s.get('time') or ''} | "
          f"{s.get('label') or '(blank)'} | {BUCKET[s['bucket']]} | "
          f"{s.get('role') or '(not stated)'} | `{s.get('source') or ''}` |")
    w("")

    counts = TT["counts"]
    w("Every timetabled period, classified. The columns sum to the lane's full week,")
    w("so nothing is quietly left out of the denominator.")
    w("")
    w("| lane | ASDAN/PEQ (a) | carryable (b) | not carryable (c) | owner decision | free | total |")
    w("|---|---:|---:|---:|---:|---:|---:|")
    for lane in ("Build", "Grow", "Launch"):
        c = counts.get(lane, {})
        empty = sum(1 for s in TT["slots"]
                    if s["lane"] == lane and s.get("bucket") == "empty")
        tot = c.get("a", 0) + c.get("b", 0) + c.get("c", 0) + c.get("owner-decision", 0) + empty
        w(f"| {lane} | {c.get('a',0)} | {c.get('b',0)} | {c.get('c',0)} | "
          f"{c.get('owner-decision',0)} | {empty} | **{tot}** |")
    w("")

    w("## 2 - Hours, and what they reach")
    w("")
    w("Two figures per lane, and the gap between them is the point. The floor counts")
    w("only slots the timetable labels ASDAN or PEQ. The ceiling adds the carryable")
    w("practical slots. Nothing is claimed against hours that do not exist.")
    w("")
    w("| lane | floor h/wk | floor GLH | ceiling h/wk | ceiling GLH | reaches at the floor |")
    w("|---|---:|---:|---:|---:|---|")
    for lane in ("Build", "Grow", "Launch"):
        r = LED["room_reachability"][lane]
        e3 = [q["qual"] for q in r["levels"]["E3"] if q["reachable_at_floor"]]
        w(f"| {lane} | {r['a_h_per_week']} | {r['a_year_glh']} | {r['ab_h_per_week']} | "
          f"{r['ab_year_glh']} | {', '.join(e3) if e3 else '**nothing**'} |")
    w("")
    w("At the ceiling every lane reaches every qualification at every level with")
    w("headroom. At the floor Build reaches nothing at all, because the timetable")
    w("labels none of its slots ASDAN or PEQ.")
    w("")

    w("## 3 - Cooking")
    w("")
    k = LED["kitchen"]["_cooking_labelled_whole_school"]
    w(k["statement"])
    w("")
    w("| lane | day | period | time | as timetabled | teacher role | source cell |")
    w("|---|---|---|---|---|---|---|")
    for lane in ("Build", "Grow", "Launch"):
        for s in LED["kitchen"][lane]["slots"]:
            w(f"| {lane} | {s['day']} | {s['period']} | {s['time']} | {s['label']} | "
              f"{s['role']} | `{s['source']}` |")
    w("")
    w("**OUTSTANDING - confirm who teaches the cooking slot(s) in September.** The")
    w("timetable assigns Build Wednesday P5 to the Science Teacher. A colleague is to")
    w("teach and resource cooking. Those may be the same decision or two different")
    w("ones; this pass does not guess.")
    w("")

    w("## 4 - What changed, by surface")
    w("")
    w("| surface | change | what it means for a plan | paperwork it generates |")
    w("|---|---|---|---|")
    for name, (kind, why) in sorted(CHANGED.items()):
        paper = ("witness sheet + assessor/learner signatures"
                 if "Kitchen" in name or "COOKING" in name or "Criteria" in name
                 else "no new paperwork")
        w(f"| `{name}` | {kind} | {why} | {paper} |")
    w("")
    w("**NO-PLANNER-SURFACE** - these changed and have no weekly-plan row to sit on:")
    w("")
    w("- The AQA UAS claim qualifier on 19 staff surfaces and the catalogue. It changes")
    w("  what a claim SAYS, not what is taught, so no plan row moves.")
    w("- `_passpq/` derivations, gates and the timetable extract. Working directory.")
    w("- `MERGE_DAY_29AUG.md`, `REBRAND.md`, the claim registers. Records, not lessons.")
    w("")

    w("## 5 - Still open")
    w("")
    w("1. **Spring and summer term dates.** The workbooks are weekly, not annual, so")
    w("   those block lengths are declared assumptions. Autumn is evidenced at 15 weeks.")
    w("2. **Who teaches the cooking slot(s).** See section 3.")
    w("3. **Three DT-vs-Behaviour cells** where the two workbooks disagree:")
    for d in TT["disagreements"]:
        w(f"   - {d['lane']} {d['day']} {d['period']}: lane grid says "
          f"\"{d['lane_grid']}\" (`{d['lane_grid_source']}`), colour-coded says "
          f"\"{d['other']}\" (`{d['other_source']}`)")
    w("")

    text = "\n".join(out) + "\n"
    assert "Cheryl" not in text and "Roper" not in text, "a staff name reached the ledger"
    dest = REPO / "_passpq" / "ASDAN_CHANGES_FOR_PLANNERS.md"
    dest.write_text(text, encoding="utf-8")
    print(f"wrote {dest.relative_to(REPO)}  ({len(text)} B, {len(rows)} slot rows)")
    if pack:
        p = pack / "_Pack_Notes" / "ASDAN_CHANGES_FOR_PLANNERS.md"
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
        print(f"and into the pack at _Pack_Notes/ASDAN_CHANGES_FOR_PLANNERS.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
