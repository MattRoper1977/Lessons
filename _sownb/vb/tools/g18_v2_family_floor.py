#!/usr/bin/env python3
"""g18 v2 — per-family pupil-word floor.

Order VB run 4, section 2.

Why this exists
---------------
g18_content_floor.py describes itself as a "destination-relative pupil-word
floor". It is not. Its BASELINE is hard-coded to
Science_Teesside/Grow/W8-W13_2026-27, so it computes ONE global p25 (1638
words) and applies it to every family in the estate. Families that teach
shorter lessons by design -- the live LAUNCH Humanities pack runs 895-1007
pupil words -- red against a floor imported from GROW Science.

What v2 changes
---------------
  BINDING verdict  = p25 of the destination family's own live neighbours.
  LEGACY verdict   = the old global p25, retained and printed on every line
                     so earlier runs stay comparable.
  n < 5 neighbours = fall back to the global floor and print GLOBAL-FALLBACK.

Word counting, slide parsing and the thin-slide rule are IMPORTED from the v1
module unchanged -- v2 re-scopes the floor and nothing else, so a flip between
v1 and v2 can only ever be the baseline, never the measurement.

Not changed here: v2 makes no lesson edit and licenses none. A red under v2 is
a finding; a green under v2 where v1 was red is a ledger correction.
"""
from __future__ import annotations

import argparse
import glob
import importlib.util
import json
import statistics
from pathlib import Path

VERSION = "g18-v2.1.0-per-family-floor-lessons-only"
ROOT = Path(__file__).resolve().parents[3]

_spec = importlib.util.spec_from_file_location(
    "g18_v1", ROOT / "_sownb/feb/tools/g18_content_floor.py"
)
v1 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(v1)

MIN_NEIGHBOURS = 5

# A neighbour counts only if it is an actual lesson deck. The packs also hold
# teacher-planning pages, SOW sheets, evidence windows and portfolio studios;
# those carry no pupil slides at all, so leaving them in drags the family p25
# down and makes the floor too lenient. Measured on BUILD ASDAN: three such
# files (SAME_DAY_EVIDENCE, TEACHER_PLANNING_SOW, W7_PORTFOLIO_STUDIO) score
# zero pupil words and pulled that family's p25 to 1041.
MIN_LESSON_SLIDES = 5

# Each family's live neighbour pack: the pack that was already teaching before
# the candidate landed. Globs, not counts -- the tree wins (order 0.5).
FAMILY_NEIGHBOURS = {
    "GROW Science":      "Science_Teesside/Grow/W8-W13_2026-27/SCI_G_W*.html",
    "LAUNCH Science":    "Science_Teesside/Launch/W8-W13_2026-27/SCI_L_W*.html",
    "BUILD Science":     "Science_Teesside/Build/W8-W13_2026-27/SCI_B_*.html",
    "GROW ASDAN":        "GROW_ASDAN/Autumn2_W1-W6_2026-27/PEQ_A2_W*.html",
    "LAUNCH ASDAN":      "LAUNCH_ASDAN/W7-W12_2026-27/lessons/*/*.html",
    "BUILD ASDAN":       "BUILD_ASDAN/Autumn2_W1-W6_2026-27/BUILD_ASDAN_*.html",
    "BUILD Humanities":  "Humanities_Teesside/BUILD_W9-W14_2026-27/BUILD_HUM_*.html",
    "GROW Humanities":   "Humanities_Teesside/GROW_W9-W14_2026-27/GROW_HUM_*.html",
    "LAUNCH Humanities": "Humanities_Teesside/LAUNCH_W9-W14_2026-27/LAUNCH_HUM_*.html",
}


def words_of(path: Path) -> int:
    return v1.lesson_counts(path)["totalWords"]


def is_lesson_deck(path: Path) -> bool:
    """True when the file is a taught lesson, not pack support furniture."""
    counts = v1.lesson_counts(path)
    return len(counts["slides"]) >= MIN_LESSON_SLIDES and counts["totalWords"] > 0


def family_baseline(family: str, exclude: Path | None = None) -> dict:
    pattern = FAMILY_NEIGHBOURS.get(family)
    if pattern is None:
        return {"family": family, "pattern": None, "n": 0, "p25": None,
                "median": None, "files": [], "error": "NO NEIGHBOUR PATTERN"}
    files = [Path(p) for p in sorted(glob.glob(str(ROOT / pattern)))]
    if exclude is not None:
        files = [p for p in files if p.resolve() != exclude.resolve()]
    support = [p.name for p in files if not is_lesson_deck(p)]
    files = [p for p in files if is_lesson_deck(p)]
    totals = [words_of(p) for p in files]
    return {
        "family": family,
        "pattern": pattern,
        "n": len(totals),
        "p25": v1.nearest_rank(totals, 0.25) if totals else None,
        "median": statistics.median(totals) if totals else None,
        "min": min(totals) if totals else None,
        "max": max(totals) if totals else None,
        "files": [{"file": p.name, "words": w} for p, w in zip(files, totals)],
        "excludedSupportSurfaces": support,
    }


def score(candidate: str, family: str) -> dict:
    path = (ROOT / candidate).resolve()
    counts = v1.lesson_counts(path)
    total = counts["totalWords"]

    fam = family_baseline(family, exclude=path)
    legacy = v1.baseline()
    global_p25 = legacy["p25"]

    fallback = fam["n"] < MIN_NEIGHBOURS
    binding_floor = global_p25 if fallback else fam["p25"]
    binding_source = (f"GLOBAL-FALLBACK n={fam['n']}" if fallback
                      else f"family p25 of {fam['n']} live neighbours")

    thin = [r for r in counts["slides"]
            if r["wordCount"] < 40 and not r["deliberatePause"]]

    binding_pass = total >= binding_floor and not thin
    legacy_pass = total >= global_p25 and not thin

    return {
        "gate": "g18-v2-per-family-floor",
        "toolVersion": VERSION,
        "candidate": candidate,
        "family": family,
        "candidateWords": total,
        "thinSlides": thin,
        "familyBaseline": fam,
        "bindingFloor": binding_floor,
        "bindingFloorSource": binding_source,
        "globalFloorLegacy": global_p25,
        "globalFloorSource": legacy["directory"] + " nearest-rank p25 (v1 baseline)",
        "bindingVerdict": "PASS" if binding_pass else "RED",
        "legacyVerdict": "PASS" if legacy_pass else "RED",
        "flipped": binding_pass != legacy_pass,
        "ratioToFamilyMedian": (round(total / fam["median"], 2)
                                if fam["median"] else None),
    }


def line(r: dict) -> str:
    return (f"{Path(r['candidate']).name[:44]:44s} fam={r['family']:17s} "
            f"n={r['familyBaseline']['n']:2d} famP25={str(r['bindingFloor']):>5s} "
            f"globalP25={r['globalFloorLegacy']} words={r['candidateWords']:5d} "
            f"BINDING={r['bindingVerdict']:4s} LEGACY={r['legacyVerdict']:4s}"
            f"{'  <-- FLIP' if r['flipped'] else ''}  [{r['toolVersion']}]")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--family", required=True)
    ap.add_argument("--candidate", required=True)
    ap.add_argument("--output")
    a = ap.parse_args()
    r = score(a.candidate, a.family)
    if a.output:
        out = ROOT / a.output
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(r, indent=2) + "\n", encoding="utf-8")
    print(line(r))
    return 0 if r["bindingVerdict"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
