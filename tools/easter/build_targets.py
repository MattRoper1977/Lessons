#!/usr/bin/env python3
"""Build EASTER_TARGETS.json: every open cell through week 26, grouped into deck plans.

ORDER VB-EASTER-A3 §1c. A PLAN is what one honest 21-25 slide lesson can teach:
same family, same ruled week, adjacent or co-dependent outcomes, at most
CELLS_PER_DECK cells. A plan of one cell is fine. Nothing is padded to reach
three -- the TRACE threshold decides what a deck may claim, so a plan that
bundles unrelated outcomes just produces a deck that fails its own claims.

Grouping key: family (lane + subject) and RULED WEEK, then at most
CELLS_PER_DECK cells in workbook order.

STRAND IS NOT THE KEY, and the reason is measured rather than assumed. Every
one of the 573 cells in scope -- all 134 covered and all 439 open -- is a unique
(lane, subject, strand, week) tuple: the workbook grants exactly one outcome per
strand per week. Group by strand and every plan is one cell by construction,
which would be an artefact of the key, not a fact about teaching.

What the estate actually does is fuse strands within a family-week. The landed
BUILD_HUM_W16_Then_And_Now_And_What_Is_Fair.html claims two cells from two
different strands in the same ruled week:

    'BUILD Weekly - Spring'!C41  World About Me  "Compare old and new objects (then & now)."
    'BUILD Weekly - Spring'!C53  RE & World Views "Talk about what is right and wrong, simply."

under one title, and it passes its gates. That is the precedent this grouping
follows. A plan still may be one cell, and nothing is padded to reach three --
the TRACE threshold decides what a deck may claim, so bundling outcomes that do
not belong together just builds a deck that fails its own claims.

Week comes from the ruled spine only (g27); filenames are labels and are never
read. Cells the spine marks OUT_OF_SCOPE are excluded and counted separately, so
the exclusion is visible rather than silent.

Usage:
  build_targets.py [--output tools/easter/EASTER_TARGETS.json] [--week-to 26]
                   [--cells-per-deck 3] [--batch-ceiling 24]
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
VERSION = "easter-targets-v1.0.0"

_cc = importlib.util.spec_from_file_location(
    "cell_coverage", ROOT / "_sownb/vb/tools/cell_coverage.py")
cc = importlib.util.module_from_spec(_cc)
_cc.loader.exec_module(cc)

# Ordering the order fixes: week-major; inside a week ASDAN -> Science ->
# Humanities -> Art; inside a family BUILD -> GROW -> LAUNCH.
SUBJECT_ORDER = {"ASDAN": 0, "Science": 1, "Humanities": 2, "Art": 3}
LANE_ORDER = {"BUILD": 0, "GROW": 1, "LAUNCH": 2}

# Weeks a cover teacher teaches before Matt is back (w/c 19 Oct 2026 is week 8,
# the enrichment week; everything at or before it is taught in his absence).
COVER_WEEK_MAX = 8


def ruled_week(cell):
    w = cc.ruled_week(cell)
    return w if isinstance(w, int) else None


def cell_number(ref: str) -> int:
    m = re.search(r"C(\d+)", ref)
    return int(m.group(1)) if m else 0


def build(week_to: int, cells_per_deck: int, coverage: dict, cells: dict) -> dict:
    covered = set(coverage["coveredCells"])
    emitted = set(coverage["openCellsInScope"]) | covered

    in_scope, out_of_scope = [], []
    for ref, c in cells.items():
        w = ruled_week(c)
        if w is None or w > week_to:
            continue
        if ref in emitted:
            in_scope.append(ref)
        else:
            out_of_scope.append({"cell": ref, "ruledWeek": w,
                                 "scopeStatus": c.get("scopeStatus"),
                                 "scopeReason": c.get("scopeReason")})

    open_cells = [r for r in in_scope if r not in covered]

    groups = defaultdict(list)
    for ref in open_cells:
        c = cells[ref]
        groups[(c.get("lane"), c.get("subject"), ruled_week(c))].append(ref)

    plans = []
    for (lane, subject, week), refs in sorted(groups.items(), key=lambda kv: (kv[0][2], str(kv[0][0]), str(kv[0][1]))):
        refs.sort(key=cell_number)
        for i in range(0, len(refs), cells_per_deck):
            chunk = refs[i:i + cells_per_deck]
            plans.append({
                "family": f"{lane} {subject}",
                "lane": lane, "subject": subject, "ruledWeek": week,
                "strands": [cells[x].get("strand") for x in chunk],
                "cells": chunk,
                "outcomes": [cells[x].get("verbatimOutcome") for x in chunk],
                "workbook": cells[chunk[0]].get("workbook"),
                "sheet": cells[chunk[0]].get("sheet"),
                "kind": "AUTHOR",
                "coverBeforeMattReturns": week <= COVER_WEEK_MAX,
            })

    # §1b/§1e. A cell whose STANDING deck claims it but whose content does not
    # carry the outcome is not a fresh authoring job -- the lesson exists and
    # falls short. Those are RESHELL plans: one unit, repair the deck it already
    # has rather than build a second deck for the same week.
    #
    # A cell the instrument CANNOT score -- no distinctive words survive
    # stopword and corpus-ubiquity removal -- is neither served nor unserved.
    # It is held as HUMAN, because "I cannot measure this" and "this is missing"
    # are different answers and only one of them justifies building.
    unscorable = {r["cell"]: r for r in coverage.get("unscorableClaims", [])}
    below = {r["cell"]: r for r in coverage.get("traceCorrections", [])}
    claimed = set(coverage.get("claimedCells", []))

    held, reshells = [], 0
    for p in plans:
        p["cells"] = list(p["cells"])
        kinds = []
        for ref in p["cells"]:
            if ref in unscorable:
                kinds.append("HUMAN")
            elif ref in claimed and ref in below:
                kinds.append("RESHELL")
            else:
                kinds.append("AUTHOR")
        if "HUMAN" in kinds:
            p["heldCells"] = [c for c, k in zip(p["cells"], kinds) if k == "HUMAN"]
            p["humanQuestion"] = (
                "These cells' outcomes carry no distinctive words, so SERVES cannot be "
                "evaluated either way. A standing deck already claims each. Does it teach "
                "the outcome? If yes the cell is covered and needs no deck; if no it needs one.")
            for c in p["heldCells"]:
                held.append({"cell": c, "planId": None, "deck": unscorable[c].get("deck"),
                             "outcome": unscorable[c].get("outcome"),
                             "ruledWeek": unscorable[c].get("ruledWeek")})
        if "RESHELL" in kinds:
            p["kind"] = "RESHELL"
            p["reshellCells"] = [c for c, k in zip(p["cells"], kinds) if k == "RESHELL"]
            p["standingDecks"] = sorted({below[c]["deck"] for c in p["reshellCells"]})
            p["standingScores"] = {c: below[c]["score"] for c in p["reshellCells"]}
            reshells += 1
        p["cellKinds"] = dict(zip(p["cells"], kinds))

    plans.sort(key=lambda p: (
        0 if p["coverBeforeMattReturns"] else 1,
        p["ruledWeek"],
        SUBJECT_ORDER.get(p["subject"], 9),
        LANE_ORDER.get(p["lane"], 9),
        cell_number(p["cells"][0]),
    ))
    for i, p in enumerate(plans, 1):
        p["planId"] = f"P{i:04d}"

    return {
        "toolVersion": VERSION,
        "subject": "ORDER VB-EASTER-A3 §1c: every open cell through week "
                   f"{week_to}, grouped into deck plans of at most {cells_per_deck} cells",
        "weekTo": week_to,
        "cellsPerDeck": cells_per_deck,
        "spineSha256": cc.__dict__.get("SPINE_SHA", None),
        "headline": {
            "inScope": len(in_scope),
            "covered": len(in_scope) - len(open_cells),
            "open": len(open_cells),
            "reading": "content",
        },
        "outOfScopeExcluded": out_of_scope,
        "planCount": len(plans),
        "cellsInPlans": sum(len(p["cells"]) for p in plans),
        "reshellPlans": reshells,
        "heldCells": held,
        "plans": plans,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", default="tools/easter/EASTER_TARGETS.json")
    ap.add_argument("--week-to", type=int, default=26)
    ap.add_argument("--cells-per-deck", type=int, default=3)
    ap.add_argument("--batch-ceiling", type=int, default=24)
    ap.add_argument("--coverage", default=None,
                    help="a CELL_COVERAGE.json to read; default runs the census fresh")
    a = ap.parse_args()

    if a.coverage:
        coverage = json.loads(Path(a.coverage).read_text())
    else:
        import subprocess, sys, tempfile
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as fh:
            tmp = fh.name
        subprocess.run([sys.executable, str(ROOT / "_sownb/vb/tools/cell_coverage.py"),
                        "--output", tmp], cwd=str(ROOT), capture_output=True, check=True)
        coverage = json.loads(Path(tmp).read_text())
        Path(tmp).unlink(missing_ok=True)

    spine = json.loads((ROOT / "_sownb/CALENDAR_SPINE.json").read_text())
    cells = {c["reference"]: c for c in spine["workbookCells"]}

    report = build(a.week_to, a.cells_per_deck, coverage, cells)
    out = ROOT / a.output
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")

    h = report["headline"]
    print(f"EASTER TARGETS  [{VERSION}]")
    print(f"  headline (content) : in scope {h['inScope']} · covered {h['covered']} · open {h['open']}")
    print(f"  out of scope excluded : {len(report['outOfScopeExcluded'])}")
    for r in report["outOfScopeExcluded"]:
        print(f"      {r['cell']}  wk{r['ruledWeek']}  {r['scopeReason']}")
    print(f"  plans              : {report['planCount']}  covering {report['cellsInPlans']} cells")
    print(f"  RESHELL plans      : {report['reshellPlans']}  (a standing deck claims the cell and falls short)")
    print(f"  HELD cells (HUMAN) : {len(report['heldCells'])}  (unscorable: no distinctive words)")
    for h in report["heldCells"]:
        print(f"      {h['cell']}  wk{h['ruledWeek']}  {h['deck'].split('/')[-1]}")
    sizes = Counter(len(p["cells"]) for p in report["plans"])
    print(f"  plan sizes         : " + " · ".join(f"{k}-cell x{v}" for k, v in sorted(sizes.items())))
    fam = Counter(p["family"] for p in report["plans"])
    print("  plans by family    :")
    for k, v in sorted(fam.items(), key=lambda kv: -kv[1]):
        print(f"      {k:20s} {v:4d}")
    ceiling = a.batch_ceiling
    batches = -(-report["planCount"] // ceiling)
    print(f"  FORECAST           : at BATCH_CEILING {ceiling}, "
          f"{ceiling} plans/batch ≈ {report['cellsInPlans']/max(1,report['planCount'])*ceiling:.0f} cells/batch, "
          f"{batches} batches to DONE")
    print(f"  batch 1 (cover weeks ≤{COVER_WEEK_MAX} first): "
          f"{sum(1 for p in report['plans'][:ceiling] if p['coverBeforeMattReturns'])} of {ceiling} are cover-taught weeks")
    print(f"  written: {a.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
