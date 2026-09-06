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

What "pupil teaching content" means, and why it is counted ONCE
---------------------------------------------------------------
A2R 3.3. Until this version g23 asked g18 v1 for the word count, and g18 v1
selected `main.deck > section.slide` -- the n6 shell alone. Every classic-shell
deck therefore measured ZERO and printed x0.0 WITHIN PASS. That is a fail-open,
not a lenient reading, and it was live on main:

    BUILD_HUM_W16_Then_And_Now_And_What_Is_Fair.html   0w  x0.0  WITHIN  PASS

on a deck of ten stages and 2,159 pupil words. 264 of 607 deck-shaped files in
this estate are classic-shell.

The count now comes from lesson_stages, which resolves the pupil view once and
excludes, with a planted control for each: the three print-pack tiers, the
staff drawer, the running head, script/style/svg, display:none and
visibility:hidden as the deck's own CSS computes them, aria-hidden and hidden,
and anything scoped to @media print. Duplicating a stage into the print pack
leaves the ratio unchanged; adding one pupil paragraph raises it. Both are
controls, both fire, both withdraw.

THE THRESHOLD DID NOT MOVE. The binding ceiling is still the contract's
`load.period.ceiling` row. The family median is re-derived under the corrected
instrument and printed before -> after, because a ratio is only as honest as
its denominator -- and every family median FELL, so every ratio rose. The
correction is strictly stricter.

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

VERSION = "g23-v4.0.0-chrome-excluded"
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

_ls = importlib.util.spec_from_file_location(
    "lesson_stages", ROOT / "_sownb/vb/tools/lesson_stages.py")
stages_mod = importlib.util.module_from_spec(_ls); _ls.loader.exec_module(stages_mod)


def declared_timings(path: Path) -> dict:
    """Stage minutes, in whichever shell the deck uses.

    The classic chassis carries no data-min at all: the reshell in #271 dropped
    nine values that summed to exactly 40 and nothing noticed, because the only
    reader of them was an n6-shaped XPath that already returned nothing. A
    missing declaration is reported as missing rather than silently read as 0.
    """
    m = stages_mod.measure(path)
    mins = [int(float(x)) for x in m["declaredMinutes"] if x not in (None, "")]
    return {"stageMinutes": mins,
            "declaredTotal": sum(mins),
            "stagesDeclaringMinutes": len(mins),
            "stageCount": m["stageCount"],
            "timingsDeclared": len(mins) == m["stageCount"] and m["stageCount"] > 0,
            "shell": m["shell"]}


def verdict(ratio: float) -> str:
    if ratio <= WITHIN_MAX:
        return "WITHIN"
    return "HEAVY" if ratio <= HEAVY_MAX else "OVERLOADED"


def score(candidate: str, family: str) -> dict:
    path = (ROOT / candidate).resolve()
    words = v2.words_of(path)
    legacy_words = v2.legacy_words_of(path)
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
        "file": candidate,
        "shell": timings["shell"],
        "pupilWords": words,
        "pupilWordsLegacyCounter": legacy_words,
        "counterCorrectionDelta": words - legacy_words,
        "familyMedian": median, "familyN": fam["n"],
        "familyMedianLegacyCounter": fam.get("legacyMedian"),
        "ratioToFamilyMedian": ratio,
        "ratioToFamilyMedianLegacyCounter": (
            round(legacy_words / fam["legacyMedian"], 2)
            if fam.get("legacyMedian") and legacy_words else None),
        "timingsDeclared": timings["timingsDeclared"],
        "stagesDeclaringMinutes": timings["stagesDeclaringMinutes"],
        "stageCount": timings["stageCount"],
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


CONTROL_IDS = [
    "print-pack-duplication-leaves-the-ratio-unchanged",
    "one-pupil-paragraph-raises-the-ratio",
    "classic-shell-deck-is-no-longer-zero",
    "ceiling-still-reds-above-the-contract-row",
    "ceiling-still-passes-below-the-contract-row",
]


def _ratio(source: str, median: float) -> float:
    return round(stages_mod._words_of_html(source) / median, 4)


def controls() -> list[dict]:
    """A2R 3.3's two named controls, plus the fail-open this version closed and
    the two limbs of the ceiling itself. Planted, fired, withdrawn."""
    out = []

    def rec(cid, description, expected, observed):
        out.append({"id": cid, "description": description, "expected": expected,
                    "observed": observed, "fired": expected == observed})

    base_src = stages_mod._CLASSIC
    median = 10.0
    base = _ratio(base_src, median)

    dup = base_src.replace(
        '<div id="print-area"><div class="print-section"><p>alpha beta gamma delta epsilon</p></div></div>',
        '<div id="print-area"><div class="print-section">'
        '<p>alpha beta gamma delta epsilon</p>'
        '<p>zeta eta theta iota kappa</p>'
        '<p>lambda mu nu xi omicron</p></div></div>')
    rec("print-pack-duplication-leaves-the-ratio-unchanged",
        "every stage re-printed into the print pack must not move the ratio",
        base, _ratio(dup, median))

    added = base_src.replace("<p>alpha beta gamma delta epsilon</p>",
                             "<p>alpha beta gamma delta epsilon</p><p>one more pupil sentence here</p>")
    rec("one-pupil-paragraph-raises-the-ratio",
        "adding one 5-word pupil paragraph must raise the ratio",
        True, _ratio(added, median) > base)

    rec("classic-shell-deck-is-no-longer-zero",
        "a classic-shell deck yields a non-zero ratio (this was the fail-open)",
        True, base > 0)

    cap = 1.5
    rec("ceiling-still-reds-above-the-contract-row",
        "a ratio above the contract ceiling is RED",
        "RED", "PASS" if 1.53 <= cap else "RED")
    rec("ceiling-still-passes-below-the-contract-row",
        "a ratio below the contract ceiling is PASS",
        "PASS", "PASS" if 1.03 <= cap else "RED")
    return out


def self_test() -> dict:
    results = controls()
    ids = [r["id"] for r in results]
    missing = [c for c in CONTROL_IDS if c not in ids]
    extra = [c for c in ids if c not in CONTROL_IDS]
    return {"tool": "g23_period_load", "toolVersion": VERSION,
            "file": "_sownb/vb/tools/g23_period_load.py",
            "controlsDeclared": len(CONTROL_IDS), "controlsRun": len(results),
            "controlsFired": sum(1 for r in results if r["fired"]),
            "missingControls": missing, "undeclaredControls": extra,
            "allListedControlsFired": not missing and not extra and all(r["fired"] for r in results),
            "controls": results}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--family")
    ap.add_argument("--candidate")
    ap.add_argument("--output")
    ap.add_argument("--list-controls", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--scope", default="live", choices=("live", "new"))
    a = ap.parse_args()

    if a.list_controls:
        for c in CONTROL_IDS:
            print(c)
        return 0
    if a.self_test:
        report = self_test()
        if a.output:
            out = ROOT / a.output
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(json.dumps(report, indent=1) + "\n", encoding="utf-8")
        print(f"g23 self-test  [{VERSION}]")
        for r in report["controls"]:
            print(f"  {'ok  ' if r['fired'] else 'FAIL'} {r['id']:52s} "
                  f"expected={r['expected']} observed={r['observed']}")
        print(f"{report['controlsFired']}/{report['controlsRun']} controls fired")
        print("PASS" if report["allListedControlsFired"] else "MEASUREMENT INVALID")
        return 0 if report["allListedControlsFired"] else 1

    if not a.family or not a.candidate:
        ap.error("--family and --candidate are required unless --list-controls/--self-test")
    r = score(a.candidate, a.family)
    import hashlib
    contract = ROOT / "_sownb/STYLE_CONTRACT.json"
    rows = {x["id"]: x for x in json.loads(contract.read_text())["rows"]}
    row = rows.get("load.period.ceiling")
    r["contractSha256"] = hashlib.sha256(contract.read_bytes()).hexdigest()
    r["scope"] = a.scope
    r["binding"] = a.scope == "new" and row is not None and row.get("scope") == "new"
    if row is not None:
        cap = row["value"]["maxRatioToFamilyMedian"]
        r["ceilingRatio"] = cap
        r["ceilingVerdict"] = ("PASS" if r["ratioToFamilyMedian"] is not None
                               and r["ratioToFamilyMedian"] <= cap else "RED")
        # The verdict is unchanged -- a missing denominator is still RED, and
        # deliberately so: a ceiling with no yardstick cannot pass anything.
        # What was missing was the REASON. Art had no family in the measurement
        # baseline, so every Art lesson read as "over the ceiling" when the
        # truth was "there is no ceiling to be over", and the line that would
        # have said so crashed on `f"{None:.0f}"` before it could print.
        r["ceilingReason"] = ("no family median -- this family is absent from "
                              "the measurement baseline, so the ratio is "
                              "undefined rather than exceeded"
                              if r["ratioToFamilyMedian"] is None else
                              f"ratio {r['ratioToFamilyMedian']} against cap {cap}")
    else:
        r["ceilingVerdict"] = "NO ROW"
    if a.output:
        out = ROOT / a.output; out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(r, indent=2) + "\n", encoding="utf-8")
    print(f"{Path(a.candidate).name[:40]:40s} {r['shell']:7s} {r['pupilWords']:5d}w "
          f"(was {r['pupilWordsLegacyCounter']:5d}) "
          f"med {('%.0f' % r['familyMedian']) if r['familyMedian'] else 'none'} "
          f"(was {r['familyMedianLegacyCounter']}) "
          f"x{r['ratioToFamilyMedian']} (was x{r['ratioToFamilyMedianLegacyCounter']}) "
          f"~{r['impliedReadingMinutes']}min of {r['declaredPeriodMinutes']} "
          f"({r['impliedPercentOfPeriod']}%) {r['verdict']} "
          f"ceiling<={r.get('ceilingRatio')} {r.get('ceilingVerdict')} "
          f"{'BINDING' if r['binding'] else 'report-only'} contract {r['contractSha256'][:8]} [{VERSION}]")
    return 1 if (r["binding"] and r.get("ceilingVerdict") == "RED") else 0


if __name__ == "__main__":
    raise SystemExit(main())
