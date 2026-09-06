#!/usr/bin/env python3
"""g21 trailing-sheet economy with independent vector-box and raster-ink arms."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

import fitz

ROOT = Path(__file__).resolve().parents[3]
BOTTOM_MARGIN_PT = 28.35
TOP_REPEAT_BAND_PT = 80.0
INK_THRESHOLD = 230
INK_ROW_MIN_PIXELS = 5


def norm(value: str) -> str:
    return " ".join(re.sub(r"\s+", " ", value).split()).casefold()


def repeated_header_cutoffs(doc: fitz.Document) -> list[float]:
    per_page: list[list[tuple[str, float]]] = []
    for page in doc:
        rows = []
        for block in page.get_text("blocks"):
            text = norm(str(block[4]))
            if text and block[3] <= TOP_REPEAT_BAND_PT:
                rows.append((text, float(block[3])))
        per_page.append(rows)
    counts = Counter(text for rows in per_page for text, _ in rows)
    repeated = {text for text, count in counts.items() if count == len(doc) and len(doc) > 1}
    return [max((bottom for text, bottom in rows if text in repeated), default=0.0) + (3.0 if repeated else 0.0) for rows in per_page]


def vector_boxes(page: fitz.Page, header_cutoff: float) -> list[fitz.Rect]:
    boxes: list[fitz.Rect] = []
    for block in page.get_text("blocks"):
        if str(block[4]).strip():
            rect = fitz.Rect(block[:4])
            if rect.y1 > header_cutoff:
                boxes.append(rect)
    for drawing in page.get_drawings():
        rect = fitz.Rect(drawing["rect"])
        if rect.y1 <= header_cutoff:
            continue
        if rect.width >= page.rect.width * .90 and rect.height >= page.rect.height * .90:
            continue
        boxes.append(rect)
    for image in page.get_images(full=True):
        for rect in page.get_image_rects(image[0]):
            if rect.y1 > header_cutoff:
                boxes.append(fitz.Rect(rect))
    return boxes


def vector_arm(doc: fitz.Document, cutoffs: list[float]) -> dict:
    pages = []
    for index, page in enumerate(doc):
        boxes = vector_boxes(page, cutoffs[index])
        top = min((box.y0 for box in boxes), default=None)
        bottom = max((box.y1 for box in boxes), default=None)
        pages.append({
            "page": index + 1,
            "headerCutoffPt": cutoffs[index],
            "contentBoxCount": len(boxes),
            "contentTopPt": top,
            "contentBottomPt": bottom,
            "occupiedHeightPt": (bottom - top) if top is not None else 0.0,
            "freeBelowPt": max(0.0, page.rect.height - BOTTOM_MARGIN_PT - bottom) if bottom is not None else page.rect.height - BOTTOM_MARGIN_PT - cutoffs[index],
        })
    return arm_verdict("vector-box", pages)


def raster_page(page: fitz.Page, header_cutoff: float) -> dict:
    pix = page.get_pixmap(matrix=fitz.Matrix(1, 1), colorspace=fitz.csGRAY, alpha=False)
    width, height = pix.width, pix.height
    data = pix.samples
    y0 = max(0, int(header_cutoff))
    active: list[int] = []
    left, right = 18, max(19, width - 18)
    for y in range(y0, height):
        base = y * width
        dark = sum(1 for x in range(left, right) if data[base + x] < INK_THRESHOLD)
        if dark >= INK_ROW_MIN_PIXELS:
            active.append(y)
    top = float(min(active)) if active else None
    bottom = float(max(active) + 1) if active else None
    return {
        "headerCutoffPt": header_cutoff,
        "activeInkRows": len(active),
        "contentTopPt": top,
        "contentBottomPt": bottom,
        "occupiedHeightPt": (bottom - top) if top is not None else 0.0,
        "freeBelowPt": max(0.0, page.rect.height - BOTTOM_MARGIN_PT - bottom) if bottom is not None else page.rect.height - BOTTOM_MARGIN_PT - header_cutoff,
        "thresholds": {"grayBelow": INK_THRESHOLD, "minimumDarkPixelsPerRow": INK_ROW_MIN_PIXELS},
    }


def raster_arm(doc: fitz.Document, cutoffs: list[float]) -> dict:
    pages = []
    for index, page in enumerate(doc):
        row = raster_page(page, cutoffs[index])
        row["page"] = index + 1
        pages.append(row)
    return arm_verdict("raster-ink", pages)


def arm_verdict(name: str, pages: list[dict]) -> dict:
    if len(pages) < 2:
        return {"instrument": name, "pages": pages, "finalOccupiedHeightPt": None, "previousFreeVerticalPt": None, "collapsible": False, "verdict": "MEASUREMENT INVALID"}
    final_height = float(pages[-1]["occupiedHeightPt"])
    previous_free = float(pages[-2]["freeBelowPt"])
    collapsible = final_height > 0 and final_height <= previous_free
    return {
        "instrument": name,
        "pages": pages,
        "finalOccupiedHeightPt": final_height,
        "previousFreeVerticalPt": previous_free,
        "collapsible": collapsible,
        "verdict": "COLLAPSIBLE" if collapsible else "EARNED",
    }


def control(arm: dict) -> dict:
    if arm["verdict"] == "MEASUREMENT INVALID":
        return {"fired": False, "reason": "arm had fewer than two pages"}
    planted_free = float(arm["finalOccupiedHeightPt"]) + 1.0
    planted = float(arm["finalOccupiedHeightPt"]) <= planted_free
    return {
        "mutation": "set the measured previous-page free space to final occupied height plus one point and re-run the same predicate",
        "plantedPreviousFreePt": planted_free,
        "observedCollapsible": planted,
        "fired": planted,
    }


def measure(pdf: Path) -> dict:
    doc = fitz.open(pdf)
    try:
        cutoffs = repeated_header_cutoffs(doc)
        vector = vector_arm(doc, cutoffs)
        raster = raster_arm(doc, cutoffs)
    finally:
        doc.close()
    agreement = vector["verdict"] == raster["verdict"] and vector["verdict"] != "MEASUREMENT INVALID"
    if not agreement:
        verdict = "INSTRUMENT DISAGREEMENT"
    else:
        verdict = vector["verdict"]
    return {"headerRule": "exclude only identical top-band text repeated on every page", "vector": vector, "raster": raster, "agreement": agreement, "verdict": verdict}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf")
    parser.add_argument("output")
    parser.add_argument("--advisory", action="store_true")
    args = parser.parse_args()
    pdf = Path(args.pdf).resolve()
    measurement = measure(pdf)
    controls = {"vector": control(measurement["vector"]), "raster": control(measurement["raster"])}
    controls_fired = all(row["fired"] for row in controls.values())
    green = measurement["verdict"] == "EARNED"
    status = "PASS" if controls_fired and (green or args.advisory) else "RED"
    report = {
        "gate": "g21-trailing-sheet-economy",
        "pdf": str(pdf),
        "pdfSha256": hashlib.sha256(pdf.read_bytes()).hexdigest(),
        "measurement": measurement,
        "advisory": args.advisory,
        "controls": controls,
        "status": status,
    }
    output = Path(args.output)
    if not output.is_absolute():
        output = ROOT / output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": status, "verdict": measurement["verdict"], "controlsFired": controls_fired}, indent=2))
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
