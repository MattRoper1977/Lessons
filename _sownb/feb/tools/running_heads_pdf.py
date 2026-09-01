#!/usr/bin/env python3
"""Bind named running-head text to each physical PDF page MediaBox."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import fitz

ROOT = Path(__file__).resolve().parents[3]


def inside(top: float | None, page_top: float) -> bool:
    return top is not None and top >= page_top


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf")
    parser.add_argument("output")
    parser.add_argument("--expect", required=True, help="case-insensitive running-head text fragment expected on every page")
    args = parser.parse_args()
    pdf = Path(args.pdf).resolve()
    doc = fitz.open(pdf)
    rows = []
    for index, page in enumerate(doc):
        matches = [
            block for block in page.get_text("blocks")
            if args.expect.casefold() in str(block[4]).casefold()
        ]
        first = min(matches, key=lambda block: block[1]) if matches else None
        top = float(first[1]) if first else None
        page_top = float(page.rect.y0)
        rows.append({
            "page": index + 1,
            "physicalPageBoxPt": [round(value, 3) for value in page.rect],
            "expectedFragment": args.expect,
            "matchedBlockCount": len(matches),
            "runningHeadTopPt": round(top, 3) if top is not None else None,
            "clearancePt": round(top - page_top, 3) if top is not None else None,
            "text": str(first[4]).strip() if first else None,
            "status": "PASS" if inside(top, page_top) else "RED",
        })
    doc.close()
    non_vacuous = bool(rows) and all(row["matchedBlockCount"] >= 1 for row in rows)
    green = non_vacuous and all(row["status"] == "PASS" for row in rows)
    planted_top = float(rows[0]["physicalPageBoxPt"][1]) - 1.0 if rows else None
    planted_pass = inside(planted_top, float(rows[0]["physicalPageBoxPt"][1])) if rows else True
    red = bool(rows) and not planted_pass
    report = {
        "gate": "running-head-physical-page-box",
        "pdf": str(pdf),
        "pdfSha256": hashlib.sha256(pdf.read_bytes()).hexdigest(),
        "derivation": "top of the named running-head text block minus the local page MediaBox top; each physical page is independent",
        "rows": rows,
        "greenControl": {"namedHeadFoundEveryPage": non_vacuous},
        "redControl": {
            "mutation": "set the first measured named-head top to one point above its page MediaBox and re-run the same inside-page predicate",
            "plantedTopPt": planted_top,
            "fired": red,
        },
        "status": "PASS" if green and red else "RED",
    }
    output = Path(args.output)
    if not output.is_absolute():
        output = ROOT / output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "clearancesPt": [row["clearancePt"] for row in rows], "redControlFired": red}, indent=2))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
