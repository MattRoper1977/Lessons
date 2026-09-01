#!/usr/bin/env python3
"""g23 -- period load. REPORT ONLY. Order VB run 4, section 3.

Why it exists
-------------
The battery has a floor (g18) and no ceiling. It can say a lesson is too short
and can never say a lesson is unteachable in the period it is booked into.
Three wave-B1 lessons ran 2.7x-3.7x their family's usual pupil-word load in a
fixed 40-minute lesson and passed every gate in the estate.

What it does NOT do
-------------------
g23 binds nothing, blocks nothing and licenses no cut. Trimming or splitting an
overloaded lesson is authoring, and authoring is Matt's. Where a lesson comes
out OVERLOADED this tool prints the two options and the word delta each needs,
as a decision to take -- not a plan to execute.

The reading rate is an ASSUMPTION, not a measurement
----------------------------------------------------
No words-per-minute figure exists anywhere in this repository or in the
workbooks; it was searched for before this rate was chosen. WPM_ASSUMED below
is therefore a stated assumption, and every report carries a sensitivity band
so that no verdict rests on the exact number. Implied minutes are also an UPPER
BOUND on reading load: the pupil-word count includes headings, option lists and
table cells that a learner scans rather than reads through.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path

VERSION = "g23-v1.0.0-period-load-report-only"
ROOT = Path(__file__).resolve().parents[3]

WPM_ASSUMED = 90
WPM_BAND = (60, 120)
WPM_PROVENANCE = ("ASSUMED, not measured. No reading rate is recorded in this "
                  "repository or in the workbooks (searched 2026-09-01). 90 wpm "
                  "is a deliberately conservative supported-reading rate for a "
                  "SEN secondary setting; the 60-120 band is reported so no "
                  "verdict depends on the point estimate.")
PERIOD_MINUTES = 40

WITHIN_MAX = 1.5
HEAVY_MAX = 2.5

_s = importlib.util.spec_from_file_location(
    "g18_v2", ROOT / "_sownb/vb/tools/g18_v2_family_floor.py")
v2 = importlib.util.module_from_spec(_s); _s.loader.exec_module(v2)


def declared_timings(path: Path) -> dict:
    from lxml import html as lh
    tree = lh.fromstring(path.read_text(encoding="utf-8"))
    nodes = tree.xpath('//main[contains(concat(" ",normalize-space(@class)," ")," deck ")]'
                       '/section[contains(concat(" ",normalize-space(@class)," ")," slide ")]')
    mins = [int(float(n.get("data-min", "0"))) for n in nodes]
    return {"stageMinutes": mins, "declaredTotal": sum(mins)}


def verdict(ratio: float) -> str:
    if ratio <= WITHIN_MAX:
        return "WITHIN"
    return "HEAVY" if ratio <= HEAVY_MAX else "OVERLOADED"


def score(candidate: str, family: str) -> dict:
    path = (ROOT / candidate).resolve()
    words = v2.words_of(path)
    fam = v2.family_baseline(family, exclude=path)
    median = fam["median"]
    ratio = round(words / median, 2) if median else None
    timings = declared_timings(path)
    period = timings["declaredTotal"] or PERIOD_MINUTES

    implied = round(words / WPM_ASSUMED, 1)
    band = (round(words / WPM_BAND[1], 1), round(words / WPM_BAND[0], 1))
    v = verdict(ratio) if ratio is not None else "NO FAMILY MEDIAN"

    row = {
        "gate": "g23-period-load", "toolVersion": VERSION,
        "candidate": candidate, "family": family,
        "pupilWords": words,
        "familyMedian": median, "familyN": fam["n"],
        "ratioToFamilyMedian": ratio,
        "readingRateAssumed": WPM_ASSUMED, "readingRateBand": list(WPM_BAND),
        "readingRateProvenance": WPM_PROVENANCE,
        "impliedReadingMinutes": implied,
        "impliedReadingMinutesBand": list(band),
        "impliedPercentOfPeriod": round(100 * implied / period, 1),
        "declaredStageMinutes": timings["stageMinutes"],
        "declaredPeriodMinutes": period,
        "verdict": v,
        "binding": False,
        "note": "REPORT ONLY. g23 blocks nothing and licenses no cut.",
    }
    if v == "OVERLOADED":
        to_band = int(round(median * HEAVY_MAX))
        row["decisionForMatt"] = {
            "optionA_split": {
                "what": "teach across two periods",
                "wordsPerPeriodAfterSplit": int(round(words / 2)),
                "ratioAfterSplit": round((words / 2) / median, 2),
            },
            "optionB_trim": {
                "what": f"trim into the family band (<= {HEAVY_MAX}x median)",
                "targetWords": to_band,
                "wordDeltaNeeded": words - to_band,
            },
            "whoDecides": "Matt. Both options are authoring, not repair.",
        }
    return row


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--family", required=True)
    ap.add_argument("--candidate", required=True)
    ap.add_argument("--output")
    a = ap.parse_args()
    r = score(a.candidate, a.family)
    if a.output:
        out = ROOT / a.output; out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(r, indent=2) + "\n", encoding="utf-8")
    print(f"{Path(a.candidate).name[:44]:44s} {r['pupilWords']:5d}w "
          f"med {r['familyMedian']:.0f} x{r['ratioToFamilyMedian']} "
          f"~{r['impliedReadingMinutes']}min of {r['declaredPeriodMinutes']} "
          f"({r['impliedPercentOfPeriod']}%) {r['verdict']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
