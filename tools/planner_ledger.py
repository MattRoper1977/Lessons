#!/usr/bin/env python3
"""§9.9b - ASDAN_CHANGES_FOR_PLANNERS.md, the handoff artefact Stage 3 consumes.

    python3 tools/planner_ledger.py PACK_DIR

One row per lane x week x slot: the ASDAN unit or module, the deck now taught
there, what changed, the PEQ skills that week banks, and the paperwork it generates.
1,064 rows - 3 rooms x their guided slots x 38 weeks.

THE FINDING THIS TABLE EXISTS TO MAKE UNMISSABLE
------------------------------------------------
117 of those rows have a deck. 947 do not. Every authored ASDAN deck in the estate
sits in weeks 1-7 - one Autumn 1 strand per subject - while the timetable runs 38.
From week 7 the slots are still there, still carryable, still banking PEQ evidence,
and there is nothing to teach in them.

That is the largest single decision facing the weekly-plan job, and it is exactly
the kind of thing a ledger hides by omitting the rows it cannot fill. So they are
written out as NO-PLANNER-SURFACE, with the reason, and counted in section 2.

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
import re
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


# --- slot label -> the ASDAN strand that supplies its deck -------------------
# Derived from the timetable's own labels, not invented. A label with no strand is
# not a gap in this table: it is a slot that carries no ASDAN deck, and it says so.
STRAND = {
    "PfA / ASDAN":                  ("PEQ", "Personal Effectiveness"),
    "PfA / independence":           ("Living_Independently", "Independent Living"),
    "PfA / cooking":                ("PEQ_L2_Kitchen", "Kitchen Programme"),
    "Careers / Gatsby":             ("Careers", "Employability & Careers"),
    "Careers: work experience prep": ("Careers", "Employability & Careers"),
    "Community project":            ("Community_Project", "Community Project"),
    "Community / enterprise":       ("Enterprise", "Community & Enterprise"),
    "Community / social enterprise": ("Duke_and_Enterprise", "Duke & Enterprise"),
    "Vocational / practical":       ("Vocational", "Vocational Skills"),
    "Vocational / ASDAN option":    ("Vocational", "Vocational Skills"),
}
# Deliberately unmapped, with the reason. These are guided slots that carry PEQ
# evidence but have no deck of their own, and never did.
NO_DECK = {
    "Enrichment / outdoor":         "enrichment; evidence is banked from the activity, not a deck",
    "Enrichment":                   "enrichment; evidence is banked from the activity, not a deck",
    "Outdoor learning / regulation": "regulation time; owner-decision slot, no deck",
    "Behaviour Intervention":       "owner-decision slot; the two workbooks disagree on it",
    "Catch-up":                     "catch-up; content is whatever the week needs",
}
SUITE = {"Build": "BUILD_ASDAN", "Grow": "GROW_ASDAN", "Launch": "LAUNCH_ASDAN"}
SKILL = {"Com": "Communication", "DecMk": "Decision making", "LSk": "Learning skills",
         "TmWk": "Team working", "Th": "Thinking", "Wellb": "Wellbeing in learning"}


def deck_index():
    """{(suite, strand): {week: filename}} from the repo, measured not assumed."""
    out = {}
    for suite in SUITE.values():
        base = REPO / suite
        if not base.is_dir():
            continue
        for f in sorted(base.rglob("*.html")):
            m = re.search(r"_W(\d+)_", f.name)
            if not m:
                continue
            strand = f.parent.name
            out.setdefault((suite, strand), {})[int(m.group(1))] = f.name
    return out


def block_of(week):
    for name, a, z in LED["blocks"]:
        if a <= week <= z:
            return name
    return "?"


def main():
    pack = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    decks = deck_index()
    slots = [s for s in TT["slots"] if s.get("bucket") in ("a", "b", "owner-decision")]
    weeks = LED["weeks"]
    DAYS = {"Mon": 0, "Tue": 1, "Wed": 2, "Thu": 3, "Fri": 4}

    # skills in focus per week, common across the three levels (same room, same task,
    # three standards - the level differs per pupil, not per slot)
    focus = {}
    for w in range(1, weeks + 1):
        keys = set()
        for lane in LED["lanes"].values():
            keys |= {k for k in lane["rows"][w - 1] if k != "QA"}
        focus[w] = ", ".join(SKILL.get(k, k) for k in sorted(keys)) or "QA / consolidation"

    out, w_ = [], None
    def W(s=""):
        out.append(s)

    W("# ASDAN_CHANGES_FOR_PLANNERS.md")
    W("")
    W("**One row per lane x week x slot.** This is the input to the weekly-plan update:")
    W("what is timetabled, what deck sits there, what changed, and what paperwork it")
    W("generates.")
    W("")
    W("Roles only. No pupil data, no pupil initials, no staff names, no reading ages.")
    W("**Safe to paste anywhere**, including into a session that holds real pupil records.")
    W("")
    W("Generated from the school's own 2026-27 timetable, with the workbook cell cited on")
    W("every slot. Slots that bank their own subject, and free periods, are excluded from")
    W("the rows and counted in the summary, so the denominator stays visible.")
    W("")

    # ---- the finding that matters most to a planner -------------------------
    covered = sorted({wk for d in decks.values() for wk in d})
    W("## 0 - Read this before you plan anything")
    W("")
    W(f"**The ASDAN suites cover weeks {min(covered)}-{max(covered)}. The year is "
      f"{weeks} weeks long.**")
    W("")
    W(f"Every authored ASDAN deck in the estate sits in weeks {min(covered)}-{max(covered)}")
    W("- one Autumn 1 strand per subject. From week 7 onward the slots are still")
    W("timetabled, still carryable, and still bank PEQ evidence, but **there is no deck**")
    W("for them. Those rows below read `NO-PLANNER-SURFACE (no deck authored)`.")
    W("")
    W("That is not a defect in this table. It is the single largest thing the weekly-plan")
    W("job has to decide, and it would be invisible if the rows were quietly omitted.")
    W("")

    W("## 1 - The rows")
    W("")
    for lane in ("Build", "Grow", "Launch"):
        ls = sorted([s for s in slots if s["lane"] == lane],
                    key=lambda r: (DAYS.get(r["day"], 9), r["period"]))
        W(f"### {lane} - {len(ls)} guided slot(s) a week x {weeks} weeks = "
          f"{len(ls) * weeks} rows")
        W("")
        for bname, a, z in LED["blocks"]:
            W(f"<details><summary><b>{lane} · {bname} · weeks {a}-{z}</b></summary>")
            W("")
            W("| wk | day | period | time | as timetabled | ASDAN module | deck now taught there | changed | skills banked | paperwork | source cell |")
            W("|---|---|---|---|---|---|---|---|---|---|---|")
            for week in range(a, z + 1):
                for s in ls:
                    label = s.get("label") or "(blank)"
                    key = STRAND.get(label)
                    if key:
                        strand, module = key
                        fn = decks.get((SUITE[lane], strand), {}).get(week)
                        if fn:
                            deck = f"`{fn}`"
                            changed = "upgraded"
                            paper = "witness sheet · assessor + learner signature"
                        elif strand == "PEQ_L2_Kitchen":
                            deck = "`Kitchen_Week_Shell.html` (frame, no lesson)"
                            changed = "upgraded"
                            paper = "witness sheet · assessor + learner signature"
                        else:
                            deck = "**NO-PLANNER-SURFACE** (no deck authored)"
                            changed = "unchanged"
                            paper = "portfolio evidence only"
                    else:
                        module = NO_DECK.get(label, "unmapped")
                        deck = "**NO-PLANNER-SURFACE** (" + module + ")"
                        module = "-"
                        changed = "unchanged"
                        paper = "none"
                    W(f"| {week} | {s['day']} | {s['period']} | {s.get('time') or ''} | "
                      f"{label} | {module} | {deck} | {changed} | {focus[week]} | {paper} | "
                      f"`{s.get('source') or ''}` |")
            W("")
            W("</details>")
            W("")

    # ---- counts -------------------------------------------------------------
    W("## 2 - What the rows add up to")
    W("")
    counts = TT["counts"]
    W("| lane | ASDAN/PEQ (a) | carryable (b) | not carryable (c) | owner decision | free | total periods |")
    W("|---|---:|---:|---:|---:|---:|---:|")
    for lane in ("Build", "Grow", "Launch"):
        c = counts.get(lane, {})
        empty = sum(1 for s in TT["slots"] if s["lane"] == lane and s.get("bucket") == "empty")
        tot = c.get("a", 0) + c.get("b", 0) + c.get("c", 0) + c.get("owner-decision", 0) + empty
        W(f"| {lane} | {c.get('a',0)} | {c.get('b',0)} | {c.get('c',0)} | "
          f"{c.get('owner-decision',0)} | {empty} | **{tot}** |")
    W("")
    n_rows = sum(len([s for s in slots if s['lane'] == l]) for l in ("Build", "Grow", "Launch")) * weeks
    n_deck = sum(1 for lane in ("Build", "Grow", "Launch")
                 for s in slots if s["lane"] == lane
                 for wk in range(1, weeks + 1)
                 if STRAND.get(s.get("label") or "") and
                 (decks.get((SUITE[lane], STRAND[s["label"]][0]), {}).get(wk)
                  or STRAND[s["label"]][0] == "PEQ_L2_Kitchen"))
    W(f"**{n_rows} rows. {n_deck} have a deck. {n_rows - n_deck} are NO-PLANNER-SURFACE** "
      f"({100 * (n_rows - n_deck) // n_rows}%), and the great majority of those are weeks "
      f"{max(covered)+1}-{weeks}, where the ASDAN suites simply stop.")
    W("")

    # ---- hours --------------------------------------------------------------
    W("## 3 - Hours, and what they reach")
    W("")
    W("Two figures per lane. The floor counts only slots the timetable labels ASDAN or")
    W("PEQ; the ceiling adds the carryable practical slots. Nothing is claimed against")
    W("hours that do not exist.")
    W("")
    W("| lane | floor h/wk | floor GLH | ceiling h/wk | ceiling GLH | reaches at the floor |")
    W("|---|---:|---:|---:|---:|---|")
    for lane in ("Build", "Grow", "Launch"):
        r = LED["room_reachability"][lane]
        e3 = [q["qual"] for q in r["levels"]["E3"] if q["reachable_at_floor"]]
        W(f"| {lane} | {r['a_h_per_week']} | {r['a_year_glh']} | {r['ab_h_per_week']} | "
          f"{r['ab_year_glh']} | {', '.join(e3) if e3 else '**nothing**'} |")
    W("")
    W("At the ceiling every lane reaches every qualification at every level with headroom.")
    W("At the floor Build reaches nothing at all: the timetable labels none of its slots")
    W("ASDAN or PEQ.")
    W("")

    # ---- cooking ------------------------------------------------------------
    W("## 4 - Cooking")
    W("")
    k = LED["kitchen"]["_cooking_labelled_whole_school"]
    W(k["statement"])
    W("")
    W("| lane | day | period | time | as timetabled | teacher role | source cell |")
    W("|---|---|---|---|---|---|---|")
    for lane in ("Build", "Grow", "Launch"):
        for s in LED["kitchen"][lane]["slots"]:
            W(f"| {lane} | {s['day']} | {s['period']} | {s['time']} | {s['label']} | "
              f"{s['role']} | `{s['source']}` |")
    W("")
    W("**OUTSTANDING - confirm who teaches the cooking slot(s) in September.** The")
    W("timetable assigns Build Wednesday P5 to the Science Teacher; a colleague is to")
    W("teach and resource cooking. Those may be one decision or two. This pass does not")
    W("guess.")
    W("")

    # ---- changes with no planner row ---------------------------------------
    W("## 5 - Changed, with NO planner row")
    W("")
    W("Written out rather than omitted, so nobody has to work out whether they were")
    W("missed or genuinely have nowhere to sit.")
    W("")
    W("- **The AQA UAS claim qualifier**, 88 sites across 19 staff surfaces plus the")
    W("  catalogue. Changes what a claim SAYS, not what is taught. No plan row moves.")
    W("- **`index.html:422` `AQA UAS ALIGNED`** - ruled a named exception and left as is.")
    W("- **`_passpq/` derivations, gates, the timetable extract.** Working directory.")
    W("- **`MERGE_DAY_29AUG.md`, `REBRAND.md`, the claim registers.** Records, not lessons.")
    W("- **The two school-network zips.** A distribution, not a timetable change.")
    W("")

    # ---- still open ---------------------------------------------------------
    W("## 6 - Still open")
    W("")
    W("1. **Spring and summer term dates.** The workbooks are weekly, not annual, so those")
    W(f"   block lengths are declared assumptions. Autumn is evidenced at 15 weeks.")
    W("2. **Who teaches the cooking slot(s).** Section 4.")
    W(f"3. **Weeks {max(covered)+1}-{weeks} have no ASDAN decks.** Section 0. The largest")
    W("   single decision on this table.")
    W("4. **Three DT-vs-Behaviour cells** where the two workbooks disagree:")
    for d in TT["disagreements"]:
        W(f"   - {d['lane']} {d['day']} {d['period']}: lane grid says \"{d['lane_grid']}\" "
          f"(`{d['lane_grid_source']}`), colour-coded says \"{d['other']}\" "
          f"(`{d['other_source']}`)")
    W("")

    text = "\n".join(out) + "\n"
    for banned in ("Cheryl", "Roper", "reading age:"):
        assert banned not in text, f"'{banned}' reached the planner ledger"
    dest = REPO / "_passpq" / "ASDAN_CHANGES_FOR_PLANNERS.md"
    dest.write_text(text, encoding="utf-8")
    print(f"wrote {dest.relative_to(REPO)}  ({len(text)} B, {n_rows} lane x week x slot rows, "
          f"{n_deck} with a deck, {n_rows - n_deck} NO-PLANNER-SURFACE)")
    if pack:
        # The pack ROOT, not _Pack_Notes. The Network Library strips _Pack_Notes as a
        # OneDrive-only concern, and this file has to ship in BOTH zips: it is the
        # handoff the weekly-plan job consumes, not a build note for Matt.
        (pack / "ASDAN_CHANGES_FOR_PLANNERS.md").write_text(text, encoding="utf-8")
        print("and into the pack at ASDAN_CHANGES_FOR_PLANNERS.md (root, so both zips carry it)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
