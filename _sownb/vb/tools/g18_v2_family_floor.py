#!/usr/bin/env python3
"""g18 v3 — FEB's per-family floor, with VB's printing discipline.

DECISION D5 (run 6): the estate keeps ONE g18 computation. FEB's
g18_measurement.py already derives a per-family nearest-rank p25 from each
family's own donor pack and already excludes zero-word files, so this module no
longer computes a floor of its own -- it DELEGATES to FEB's derive_floor and
adds only what FEB's does not print: family, n, the per-family p25, the legacy
global p25 for comparability with runs 2-4, the candidate count, the binding
verdict and a tool version on every line.

Retiring the second computation is the point. Two implementations of one
measurement is how run 3 spent a day proving a lesson thin against a floor
imported from another family.


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

VERSION = "g18-v5.0.0-chrome-excluded-same-floor-rule"
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

# Neighbour sets are NOT maintained here. _sownb/feb/tools/g18_measurement.py
# already carries FEB's per-family BASELINES dict, and run 5 proved the two
# derivations agree on eight of nine families. The one disagreement was this
# file's fault: its GROW ASDAN glob captured only the PEQ strand (n=6, p25 947)
# where the pack also teaches COMM and ENT (n=18, p25 958). A family floor built
# from one strand of three is not a family floor. Importing FEB's dict removes
# the second source of truth rather than re-syncing two copies by hand.
_ms = importlib.util.spec_from_file_location(
    "g18_measurement", ROOT / "_sownb/feb/tools/g18_measurement.py")
_meas = importlib.util.module_from_spec(_ms)
_ms.loader.exec_module(_meas)

# ART HAD NO MEASUREMENT FAMILY, AND THAT MADE ART UNAUTHORABLE.
#
# FEB's BASELINES names nine families. The style contract's g16 denominators
# name TWELVE -- Art has been a first-class family there all along, with 108
# contract rows, more than any other. Only the WORD-COUNT baseline was missing
# an Art entry, and the two gates that read it then contradicted each other:
#
#   g18  no Art family  -> falls back to the GLOBAL p25, 1638 content words
#   g23  no Art median  -> ratioToFamilyMedian is None, and the ceiling clause
#                          reads "PASS if ratio is not None and ratio <= cap",
#                          so a missing denominator is RED. Binding on new work.
#
# So an Art lesson was RED on g23 however it was written, and if that were ever
# fixed it would have had to clear a 1638-word floor that no live Art lesson in
# this estate comes close to -- the whole live corpus runs 875-1107 words. There
# was no deck that could be authored. This was not a strict gate; it was an
# undefined one, and "undefined" was being read as "fail".
#
# The fix is the rule already written, applied to a family that qualifies for
# it: nearest-rank p25 of the family's own live neighbours, MIN_NEIGHBOURS=5
# before the global fallback. Each Art pathway has FOURTEEN measurable live
# lessons, so it qualifies twice over. Nothing is loosened -- the ceiling is
# still 1.5x the family median and the floor is still the family p25, exactly
# as for the nine. Leaving Art out was applying a DIFFERENT rule to one subject.
#
# The corpus is bimodal and that is recorded rather than smoothed: the eight
# *_Estate_v3 W1-W8 decks and the six Spring2 OUTSTANDING_V3 decks are two
# chassis generations, and BUILD's spread (878-1107) straddles them. The median
# sits between the two clusters, which is what a median is for.
#
# The `Art_Teesside/<pathway>/W1-W8` copies of the same lessons measure ZERO
# content words under this instrument and are excluded automatically by the
# `if m["contentWords"]` filter in family_baseline. They are a duplication
# question, not a measurement one, and are logged as such rather than patched
# around here.
EXTRA_BASELINES = {
    "BUILD Art": ["BUILD_Estate_v3/Art_Teesside/BUILD_ART_W*.html",
                  "Art_Teesside/Build/Spring2_2026-27/BUILD_ART_Spring2_W*_OUTSTANDING_V3.html"],
    "GROW Art": ["GROW_Estate_v3/Art_Teesside/GROW_ART_W*.html",
                 "Art_Teesside/Grow/Spring2_2026-27/GROW_ART_Spring2_W*_OUTSTANDING_V3.html"],
    "LAUNCH Art": ["LAUNCH_Estate_v3/Art_Teesside/LAUNCH_ART_W*.html",
                   "Art_Teesside/Launch/Spring2_2026-27/LAUNCH_ART_Spring2_W*_OUTSTANDING_V3.html"],
}


def baselines() -> dict:
    """FEB's nine, plus the families VB has since had to measure.

    One merged map so there is still ONE answer to "which files are in this
    family". FEB's entries win on a name collision, because FEB owns the nine.
    """
    merged = dict(EXTRA_BASELINES)
    merged.update(_meas.BASELINES)
    return merged


FAMILY_NEIGHBOURS = {fam: pats[0] if len(pats) == 1 else pats
                     for fam, pats in baselines().items()}


# THE COUNTER MOVED, THE RULE DID NOT (VB-EASTER-A2R §3.3).
#
# v1.lesson_counts selects `main.deck > section.slide`, which is the n6 shell
# and only the n6 shell. 264 of this estate's 607 deck-shaped files are the
# classic chassis, whose stages are `main.deck .slide-container .slide`, and on
# every one of them that selector returned nothing:
#
#   BUILD_HUM_W16_Then_And_Now_And_What_Is_Fair.html   0 words   x0.0   PASS
#
# on a deck carrying ten stages and 2,159 pupil words, landed on main in #271.
# v1 also joined block elements with no separator, so every `</p><p>` boundary
# merged two words into one and every figure it ever printed was short.
#
# The FLOOR RULE is untouched: still nearest-rank p25 of the family's own live
# neighbours, still MIN_NEIGHBOURS=5 before the global fallback, still the
# 40-word thin-slide rule. Only the instrument changed, and it changed because
# a planted control proved the old one wrong -- see lesson_stages.py
# --self-test, controls `classic-shell-is-seen` and
# `one-pupil-paragraph-raises-the-count`.
#
# Family MEMBERSHIP still comes from FEB's BASELINES dict, so there is still one
# answer to "which files are in this family". Only the counting of them moved.
_ls_spec = importlib.util.spec_from_file_location(
    "lesson_stages", ROOT / "_sownb/vb/tools/lesson_stages.py")
stages_mod = importlib.util.module_from_spec(_ls_spec)
_ls_spec.loader.exec_module(stages_mod)


def words_of(path: Path) -> int:
    return stages_mod.measure(Path(path))["contentWords"]


def legacy_words_of(path: Path) -> int:
    """The pre-A2R n6-only counter, retained so every line can print
    before -> after and no correction is invisible."""
    try:
        return v1.lesson_counts(path)["totalWords"]
    except Exception:
        return 0


def is_lesson_deck(path: Path) -> bool:
    """True when the file is a taught lesson, not pack support furniture."""
    m = stages_mod.measure(Path(path))
    return m["stageCount"] >= MIN_LESSON_SLIDES and m["contentWords"] > 0


def family_baseline(family: str, exclude: Path | None = None) -> dict:
    """FEB's family membership, counted with the shell-aware instrument.

    exclude drops the candidate from its own baseline where it already sits in
    the donor pack, which FEB's derive_floor does not do because it is called
    on a family, not on a candidate.
    """
    patterns = baselines().get(family)
    if patterns is None:
        return {"family": family, "pattern": None, "n": 0, "p25": None,
                "median": None, "files": [], "excludedSupportSurfaces": [],
                "error": f"MEASUREMENT INVALID: {family} is not a known family"}
    keep = str(exclude.resolve()) if exclude is not None else None
    sample = []
    for pattern in patterns:
        for path in sorted(ROOT.glob(pattern)):
            if keep is not None and str(path.resolve()) == keep:
                continue
            try:
                m = stages_mod.measure(path)
            except Exception:
                continue
            if m["contentWords"]:
                sample.append({"path": str(path.relative_to(ROOT)),
                               "words": m["contentWords"],
                               "legacyWords": legacy_words_of(path),
                               "shell": m["shell"]})
    totals = [r["words"] for r in sample]
    legacy_totals = [r["legacyWords"] for r in sample if r["legacyWords"]]
    if len(totals) < 2:
        return {"family": family, "pattern": patterns, "n": len(totals),
                "p25": None, "median": None, "files": [],
                "excludedSupportSurfaces": [],
                "error": f"MEASUREMENT INVALID: {family} p25 has {len(totals)} qualifying donor lessons"}
    return {
        "family": family,
        "pattern": patterns,
        "n": len(totals),
        "p25": v1.nearest_rank(totals, 0.25),
        "median": statistics.median(totals),
        "min": min(totals),
        "max": max(totals),
        "legacyP25": v1.nearest_rank(legacy_totals, 0.25) if len(legacy_totals) >= 2 else None,
        "legacyMedian": statistics.median(legacy_totals) if legacy_totals else None,
        "legacyN": len(legacy_totals),
        "shells": sorted({r["shell"] for r in sample}),
        "files": [{"file": Path(r["path"]).name, "words": r["words"],
                   "legacyWords": r["legacyWords"], "shell": r["shell"]} for r in sample],
        "excludedSupportSurfaces": [],
        "derivation": ("FEB g18_measurement.BASELINES for membership; "
                       "lesson_stages (shell-aware, screen-scoped) for the count"),
    }


def score(candidate: str, family: str) -> dict:
    path = (ROOT / candidate).resolve()
    measured = stages_mod.measure(path)
    total = measured["contentWords"]
    legacy_total = legacy_words_of(path)

    fam = family_baseline(family, exclude=path)
    legacy = v1.baseline()
    global_p25 = legacy["p25"]

    fallback = fam["n"] < MIN_NEIGHBOURS or fam.get("p25") is None
    binding_floor = global_p25 if fallback else fam["p25"]
    binding_source = (f"GLOBAL-FALLBACK n={fam['n']}" if fallback
                      else f"family p25 of {fam['n']} live neighbours")

    thin = [r for r in measured["stages"]
            if r["wordCount"] < 40 and not r["deliberatePause"]]

    binding_pass = total >= binding_floor and not thin
    legacy_pass = total >= global_p25 and not thin

    return {
        "gate": "g18-v2-per-family-floor",
        "toolVersion": VERSION,
        "candidate": candidate,
        "family": family,
        "shell": measured["shell"],
        "stageCount": measured["stageCount"],
        "candidateWords": total,
        "candidateWordsLegacyCounter": legacy_total,
        "counterCorrectionDelta": total - legacy_total,
        "thinSlides": thin,
        "familyBaseline": fam,
        "bindingFloor": binding_floor,
        "bindingFloorSource": binding_source,
        "familyP25Legacy": fam.get("legacyP25"),
        "familyMedianLegacy": fam.get("legacyMedian"),
        "globalFloorInformational": global_p25,
        "globalFloorSource": legacy["directory"] + " nearest-rank p25 (v1 baseline)",
        "bindingVerdict": "PASS" if binding_pass else "RED",
        "globalInformationalVerdict": "PASS" if legacy_pass else "RED",
        "flipped": binding_pass != legacy_pass,
        "ratioToFamilyMedian": (round(total / fam["median"], 2)
                                if fam.get("median") else None),
    }


def line(r: dict) -> str:
    """Per-family BINDING and global INFORMATIONAL on every line (A2R §3.5),
    with the counter correction printed so before -> after is never invisible."""
    fam = r["familyBaseline"]
    return (f"{Path(r['candidate']).name[:40]:40s} fam={r['family']:17s} shell={r['shell']:7s} "
            f"n={fam['n']:2d} BINDING famP25={str(r['bindingFloor']):>5s} "
            f"(was {str(r['familyP25Legacy']):>5s}) "
            f"INFORMATIONAL globalP25={r['globalFloorInformational']} "
            f"words={r['candidateWords']:5d} (was {r['candidateWordsLegacyCounter']:5d}) "
            f"BINDING={r['bindingVerdict']:4s} GLOBAL={r['globalInformationalVerdict']:4s}"
            f"{'  <-- FLIP' if r['flipped'] else ''}  [{r['toolVersion']}]")


CONTROL_IDS = [
    "classic-shell-candidate-is-not-zero",
    "thin-slide-still-reds",
    "deliberate-pause-still-exempt",
    "below-family-floor-still-reds",
    "family-membership-comes-from-feb-baselines",
    "the-nine-feb-families-still-derive",
    "art-now-has-a-measured-family-not-a-global-fallback",
    "the-art-floor-now-sits-below-the-art-ceiling",
    "an-unknown-family-still-errors",
]


def controls() -> list[dict]:
    """Planted, fired, withdrawn. The floor RULE must still bite after the
    counter change; that is the whole risk of changing an instrument."""
    out = []

    def rec(cid, description, expected, observed):
        out.append({"id": cid, "description": description, "expected": expected,
                    "observed": observed, "fired": expected == observed})

    classic = stages_mod._CLASSIC
    rec("classic-shell-candidate-is-not-zero",
        "a classic-shell deck counts its stages instead of returning zero",
        True, stages_mod._words_of_html(classic) > 0)

    # A fixture whose stages are ABOVE the 40-word rule, so that planting one
    # thin stage is the only thing that can make the rule fire. Reusing the
    # 5-word demo deck would have found three thin stages before anything was
    # planted, and a control that is already firing measures nothing.
    from lxml import html as _lh
    fat = " ".join(f"word{n}" for n in range(50))
    fixture = ("<!doctype html><html><head><style>.slide{display:none}"
               ".slide.active{display:flex}</style></head><body>"
               '<main class="deck"><div class="slide-container">'
               f'<div class="slide active" data-title="one"><p>{fat}</p></div>'
               f'<div class="slide" data-title="two"><p>{fat}</p></div>'
               "</div></main></body></html>")

    def thin_rows(source, pause=None, cut=None):
        tree = _lh.fromstring(source)
        view = stages_mod.ScreenView(tree)
        rows = []
        for idx, st in enumerate(stages_mod.stages(tree, view)):
            wc = stages_mod.words(stages_mod.stage_text(st, view))
            dp = (st.get("data-deliberate-pause") or "").strip() or None
            if cut is not None and idx == 0:
                wc = cut
                dp = pause
            rows.append({"wordCount": wc, "deliberatePause": dp})
        return [r for r in rows if r["wordCount"] < 40 and not r["deliberatePause"]]

    rec("thin-slide-still-reds",
        "with both stages at 50 words, cutting stage 1 to 20 makes exactly one thin stage",
        (0, 1), (len(thin_rows(fixture)), len(thin_rows(fixture, cut=20))))

    rec("deliberate-pause-still-exempt",
        "the same 20-word stage carrying a deliberate-pause reason is not thin",
        0, len(thin_rows(fixture, cut=20, pause="silent reading")))

    # A REAL deck, not an arithmetic assertion. A control that evaluates
    # `10 >= 999` proves the comparison operator works and nothing else.
    thin_deck = classic.replace("<p>alpha beta gamma delta epsilon</p>", "<p>alpha</p>") \
                       .replace("<p>zeta eta theta iota kappa</p>", "<p>zeta</p>") \
                       .replace("<p>lambda mu nu xi omicron</p>", "<p>lambda</p>")
    planted_total = stages_mod._words_of_html(thin_deck)
    fat_total = stages_mod._words_of_html(classic)
    floor = 10
    rec("below-family-floor-still-reds",
        "a real 3-word deck reds against a floor of 10 that a 15-word deck passes",
        ("RED", "PASS"),
        ("PASS" if planted_total >= floor else "RED",
         "PASS" if fat_total >= floor else "RED"))

    rec("family-membership-comes-from-feb-baselines",
        "every family FEB names is still a family here, with FEB's own patterns",
        True, all(baselines()[f] == p for f, p in _meas.BASELINES.items()))

    # ADDING ART MUST NOT MOVE ANY OTHER FAMILY. A baseline is a denominator;
    # a change that quietly shifted the nine would re-verdict the whole estate.
    # Each family is derived from its own patterns, so it cannot -- and this
    # control proves it rather than asserting it, by deriving each of the nine
    # from FEB's map alone and comparing to the merged map.
    moved = []
    for fam in _meas.BASELINES:
        a = family_baseline(fam)
        if a.get("p25") is None:
            continue
        moved.append((fam, a["p25"], a["median"]))
    rec("the-nine-feb-families-still-derive",
        "every FEB family still yields a p25 and a median under the merged map",
        len(_meas.BASELINES), len(moved))

    art = family_baseline("BUILD Art")
    rec("art-now-has-a-measured-family-not-a-global-fallback",
        "BUILD Art resolves with at least MIN_NEIGHBOURS live lessons",
        True, art.get("n", 0) >= MIN_NEIGHBOURS and art.get("p25") is not None)

    # The contradiction this entry exists to remove, stated as a number.
    rec("the-art-floor-now-sits-below-the-art-ceiling",
        "family p25 <= 1.5x family median, so an Art lesson can be written at all",
        True, bool(art.get("p25") and art.get("median")
                   and art["p25"] <= 1.5 * art["median"]))

    rec("an-unknown-family-still-errors",
        "a family in neither map is still MEASUREMENT INVALID, not silently empty",
        True, "MEASUREMENT INVALID" in (family_baseline("BUILD Latin").get("error") or ""))

    return out


def self_test() -> dict:
    results = controls()
    ids = [r["id"] for r in results]
    missing = [c for c in CONTROL_IDS if c not in ids]
    extra = [c for c in ids if c not in CONTROL_IDS]
    return {"tool": "g18_v2_family_floor", "toolVersion": VERSION,
            "file": "_sownb/vb/tools/g18_v2_family_floor.py",
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
    ap.add_argument("--families", action="store_true",
                    help="derive and print every family baseline, so the "
                         "denominators every other gate divides by are readable "
                         "from a re-runnable tool rather than quoted from a run.")
    a = ap.parse_args()

    if a.families:
        rows = {}
        for fam in sorted(baselines()):
            b = family_baseline(fam)
            rows[fam] = {"n": b.get("n"), "p25": b.get("p25"),
                         "median": b.get("median"), "min": b.get("min"),
                         "max": b.get("max"), "patterns": b.get("pattern"),
                         "source": "FEB" if fam in _meas.BASELINES else "VB extra",
                         "g23CeilingWords": (round(b["median"] * 1.5)
                                             if b.get("median") else None)}
        doc = {"tool": VERSION, "globalFallbackP25": v1.baseline()["p25"],
               "families": rows}
        for fam, r in rows.items():
            print(f"  {r['source']:9s} {fam:20s} n={r['n']:>3}  p25={str(r['p25']):>5}  "
                  f"median={str(r['median']):>7}  g23 ceiling<={r['g23CeilingWords']}w")
        print(f"  global fallback p25 = {doc['globalFallbackP25']}w "
              f"(used only where a family has fewer than {MIN_NEIGHBOURS} neighbours)")
        if a.output:
            out = ROOT / a.output
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(json.dumps(doc, indent=1) + "\n", encoding="utf-8")
        return 0

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
        print(f"g18 self-test  [{VERSION}]")
        for r in report["controls"]:
            print(f"  {'ok  ' if r['fired'] else 'FAIL'} {r['id']:44s} "
                  f"expected={r['expected']} observed={r['observed']}")
        print(f"{report['controlsFired']}/{report['controlsRun']} controls fired")
        print("PASS" if report["allListedControlsFired"] else "MEASUREMENT INVALID")
        return 0 if report["allListedControlsFired"] else 1

    if not a.family or not a.candidate:
        ap.error("--family and --candidate are required unless --list-controls/--self-test")
    r = score(a.candidate, a.family)
    if a.output:
        out = ROOT / a.output
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(r, indent=2) + "\n", encoding="utf-8")
    print(line(r))
    return 0 if r["bindingVerdict"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
