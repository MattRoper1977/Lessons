#!/usr/bin/env python3
"""g18: destination-relative pupil-word floor, thin-slide rule and rendered-page floor."""

from __future__ import annotations

import copy
import json
import math
import re
import sys
import unicodedata
from pathlib import Path

from lxml import html


ROOT = Path(__file__).resolve().parents[3]
BASELINE = ROOT / "Science_Teesside/Grow/W8-W13_2026-27"
WORD = re.compile(r"[A-Za-z0-9]+(?:['’-][A-Za-z0-9]+)*")
BLANK_CHARS = 40
BLANK_INK = 0.004
NEAR_CHARS = BLANK_CHARS * 2
NEAR_INK = BLANK_INK * 2


def words(text: str) -> list[str]:
    return WORD.findall(unicodedata.normalize("NFKC", text))


def strip_non_pupil(node) -> None:
    for child in list(node.iterdescendants()):
        tag = child.tag.lower() if isinstance(child.tag, str) else ""
        classes = set((child.get("class") or "").split())
        if (
            tag in {"script", "style", "noscript", "template", "svg"}
            or child.get("data-mbm-guide") is not None
            or child.get("data-audience", "").lower() == "staff"
            or "hero-visual" in classes
        ):
            parent = child.getparent()
            if parent is not None:
                parent.remove(child)


def lesson_counts(path: Path) -> dict:
    root = html.fromstring(path.read_text(encoding="utf-8"))
    slides = root.xpath(
        '//main[contains(concat(" ", normalize-space(@class), " "), " deck ")]'
        '/section[contains(concat(" ", normalize-space(@class), " "), " slide ")]'
    )
    measured = []
    for index, original in enumerate(slides, 1):
        slide = copy.deepcopy(original)
        strip_non_pupil(slide)
        text = " ".join(slide.text_content().split())
        reason = (original.get("data-deliberate-pause") or "").strip()
        measured.append({
            "slide": index,
            "title": original.get("data-title") or "",
            "wordCount": len(words(text)),
            "deliberatePause": reason or None,
        })
    return {"file": path.name, "totalWords": sum(row["wordCount"] for row in measured), "slides": measured}


def nearest_rank(values: list[int], proportion: float) -> int:
    ordered = sorted(values)
    return ordered[max(0, math.ceil(proportion * len(ordered)) - 1)]


def baseline() -> dict:
    paths = sorted(BASELINE.glob("SCI_*.html"))
    sample = [lesson_counts(path) for path in paths]
    totals = [item["totalWords"] for item in sample]
    return {
        "directory": str(BASELINE.relative_to(ROOT)),
        "lessonCount": len(sample),
        "method": "main.deck slide text; staff guidance, staff audience, scripts/styles and aria-hidden hero SVG removed; nearest-rank p25",
        "p25": nearest_rank(totals, 0.25),
        "sample": [{"file": item["file"], "totalWords": item["totalWords"]} for item in sample],
    }


def print_floor(contact_path: Path) -> dict:
    contact = json.loads(contact_path.read_text(encoding="utf-8"))
    target = contact["targets"][0]["print"]
    pypdf = target["pypdfPageChars"]
    poppler = target["pdftotextPageChars"]
    ink = target["inkCoverage"]
    pages = []
    for index in range(max(len(pypdf), len(poppler), len(ink))):
        py = pypdf[index] if index < len(pypdf) else 0
        po = poppler[index] if index < len(poppler) else 0
        coverage = ink[index] if index < len(ink) else 0
        character_blank = py < BLANK_CHARS and po < BLANK_CHARS
        character_near = py < NEAR_CHARS and po < NEAR_CHARS
        blank = character_blank or coverage < BLANK_INK
        near = not blank and (character_near or coverage < NEAR_INK)
        pages.append({
            "page": index + 1, "pypdfChars": py, "pdftotextChars": po,
            "inkCoverage": coverage, "characterBlankBothExtractors": character_blank,
            "blank": blank, "nearBlank": near,
        })
    return {
        "thresholds": {
            "blank": {"characterBothExtractorsBelow": BLANK_CHARS, "inkBelow": BLANK_INK, "join": "OR"},
            "nearBlank": {"characterBothExtractorsBelow": NEAR_CHARS, "inkBelow": NEAR_INK, "join": "OR"},
        },
        "pageCount": target["pageCount"],
        "pages": pages,
        "blankPages": [row["page"] for row in pages if row["blank"]],
        "nearBlankPages": [row["page"] for row in pages if row["nearBlank"]],
    }


def main() -> int:
    if len(sys.argv) < 3:
        raise SystemExit("usage: g18_content_floor.py CANDIDATE CONTACT_METRICS [OUTPUT]")
    candidate_path = (ROOT / sys.argv[1]).resolve()
    contact_path = (ROOT / sys.argv[2]).resolve()
    base = baseline()
    candidate = lesson_counts(candidate_path)
    thin = [
        row for row in candidate["slides"]
        if row["wordCount"] < 40 and not row["deliberatePause"]
    ]
    print_result = print_floor(contact_path)
    candidate["p25Required"] = base["p25"]
    candidate["wordFloorPass"] = candidate["totalWords"] >= base["p25"]
    candidate["thinSlides"] = thin
    candidate["thinSlidePass"] = not thin
    planted = copy.deepcopy(candidate["slides"])
    planted[0]["wordCount"] = 20
    planted[0]["deliberatePause"] = None
    planted_thin = [row for row in planted if row["wordCount"] < 40 and not row["deliberatePause"]]
    red = {
        "defect": "in-memory first slide reduced to 20 pupil-facing words with no deliberate-pause reason",
        "fired": any(row["slide"] == 1 and row["wordCount"] == 20 for row in planted_thin),
        "redRows": planted_thin,
    }
    pass_now = (
        candidate["wordFloorPass"] and candidate["thinSlidePass"]
        and not print_result["blankPages"] and not print_result["nearBlankPages"]
        and red["fired"]
    )
    report = {
        "gate": "g18-content-floor", "baseline": base, "candidate": candidate,
        "print": print_result, "redProof": red,
        "status": "PASS" if pass_now else "RED",
    }
    output = (ROOT / sys.argv[3]).resolve() if len(sys.argv) > 3 else ROOT / "_sownb/rsh/output/g18.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({
        "gate": report["gate"], "status": report["status"], "p25": base["p25"],
        "candidateWords": candidate["totalWords"], "thinSlides": [row["slide"] for row in thin],
        "blankPages": print_result["blankPages"], "nearBlankPages": print_result["nearBlankPages"],
        "redProofFired": red["fired"],
    }, indent=2))
    return 0 if pass_now else 1


if __name__ == "__main__":
    raise SystemExit(main())
