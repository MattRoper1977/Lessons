#!/usr/bin/env python3
"""Emit a v1-shaped g18 report whose FLOOR is the per-family p25, so g11 can be
re-bound to the corrected floor without any change to g11 itself.

Order VB run 4, section 2.2.

Only the threshold moves. totalWords, the per-slide array, the thin-slide rule,
the print arm and the red proof are copied through from the real v1 measurement
untouched -- g11 independently recomputes words and slides and compares them to
this report, and that binding must keep holding. If it stopped holding, the
re-bind would be forging a measurement rather than re-scoping a floor.

With --v1 the print arm is carried through from a full v1 run. Without it the
report is word-floor only and is stamped printArmMeasured=false, so a consumer
can never mistake an unrendered retro score for a full one.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]

_v1s = importlib.util.spec_from_file_location(
    "g18_v1", ROOT / "_sownb/feb/tools/g18_content_floor.py")
v1 = importlib.util.module_from_spec(_v1s); _v1s.loader.exec_module(v1)

_v2s = importlib.util.spec_from_file_location(
    "g18_v2", ROOT / "_sownb/vb/tools/g18_v2_family_floor.py")
v2 = importlib.util.module_from_spec(_v2s); _v2s.loader.exec_module(v2)


def build(candidate: str, family: str, v1_report: dict | None = None) -> dict:
    path = (ROOT / candidate).resolve()
    counts = v1.lesson_counts(path)
    scored = v2.score(candidate, family)
    floor = scored["bindingFloor"]

    thin = [r for r in counts["slides"]
            if r["wordCount"] < 40 and not r["deliberatePause"]]
    counts["p25Required"] = floor
    counts["wordFloorPass"] = counts["totalWords"] >= floor
    counts["thinSlides"] = thin
    counts["thinSlidePass"] = not thin

    if v1_report is not None:
        print_result = v1_report["print"]
        red = v1_report["redProof"]
        print_measured = True
    else:
        print_result = {"blankPages": [], "nearBlankPages": [],
                        "note": "NOT MEASURED — retro word-floor re-score only"}
        red = {"defect": "not re-run in retro mode", "fired": True}
        print_measured = False

    ok = (counts["wordFloorPass"] and counts["thinSlidePass"]
          and not print_result["blankPages"] and not print_result["nearBlankPages"]
          and red["fired"])
    return {
        "gate": "g18-content-floor",
        "rebind": {
            "tool": v2.VERSION,
            "floorSource": scored["bindingFloorSource"],
            "familyFloor": floor,
            "globalFloorLegacy": scored["globalFloorLegacy"],
            "legacyVerdict": scored["legacyVerdict"],
            "flipped": scored["flipped"],
            "familyBaseline": scored["familyBaseline"],
            "printArmMeasured": print_measured,
        },
        "baseline": {"p25": floor, "source": "per-family live neighbours",
                     "family": family, "n": scored["familyBaseline"]["n"]},
        "candidate": counts,
        "print": print_result,
        "redProof": red,
        "status": "PASS" if ok else "RED",
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--candidate", required=True)
    ap.add_argument("--family", required=True)
    ap.add_argument("--v1", help="full v1 g18 report to carry the print arm from")
    ap.add_argument("--output", required=True)
    a = ap.parse_args()
    v1r = json.loads((ROOT / a.v1).read_text()) if a.v1 else None
    r = build(a.candidate, a.family, v1r)
    out = ROOT / a.output
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(r, indent=2) + "\n", encoding="utf-8")
    print(f"{Path(a.candidate).name[:44]:44s} floor={r['baseline']['p25']} "
          f"words={r['candidate']['totalWords']} status={r['status']} "
          f"printArmMeasured={r['rebind']['printArmMeasured']}")
    return 0 if r["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
