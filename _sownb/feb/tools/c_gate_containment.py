#!/usr/bin/env python3
"""RSH-3 printed-pupil sentence containment with fired controls."""
from __future__ import annotations

import argparse
from collections import Counter
import json
import re
import subprocess
import unicodedata
from pathlib import Path

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[3]
LIGATURES = str.maketrans({"ﬁ": "fi", "ﬂ": "fl", "ﬀ": "ff", "ﬃ": "ffi", "ﬄ": "ffl", "\u00ad": ""})
SENTENCE = re.compile(r"[^.!?]+[.!?]+(?:[\"”’')\]]+)?")


def normalise(text: str) -> str:
    return " ".join(unicodedata.normalize("NFKC", text.translate(LIGATURES)).split())


def sentences(text: str) -> list[str]:
    return [normalise(item).casefold() for item in SENTENCE.findall(normalise(text)) if len(item.split()) >= 2]


def token_multiset(text: str) -> Counter:
    return Counter(re.findall(r"[a-z0-9]+", normalise(text).casefold()))


def extract(pdf: Path) -> dict[str, str]:
    pypdf = "\f".join(page.extract_text() or "" for page in PdfReader(pdf).pages)
    poppler_raw = subprocess.run(["pdftotext", "-raw", str(pdf), "-"], check=True, text=True, capture_output=True).stdout
    poppler_layout = subprocess.run(["pdftotext", "-layout", str(pdf), "-"], check=True, text=True, capture_output=True).stdout
    return {"pypdf": normalise(pypdf), "pdftotextRaw": normalise(poppler_raw), "pdftotextLayout": normalise(poppler_layout)}


def compare(before: str, after: str) -> dict[str, object]:
    left, right = sentences(before), sentences(after)
    index = 0
    for item in right:
        if index < len(left) and item == left[index]:
            index += 1
    missing = left[index:]
    return {
        "beforeSentenceCount": len(left),
        "afterSentenceCount": len(right),
        "matchedInOrder": index,
        "missing": missing,
        "nonVacuous": bool(left),
        "pass": bool(left) and index == len(left),
    }


def controls() -> dict[str, object]:
    before = "Choose the genuine source. Record the approved location. Keep an uncertain gap visible."
    cases = {
        "wordMutation": ("Choose the staged source. Record the approved location. Keep an uncertain gap visible.", False),
        "sentenceDeletion": ("Choose the genuine source. Keep an uncertain gap visible.", False),
        "sentenceReword": ("Select an authentic source. Record the approved location. Keep an uncertain gap visible.", False),
        "sentenceOrder": ("Record the approved location. Choose the genuine source. Keep an uncertain gap visible.", False),
        "sentenceNegation": ("Choose the genuine source. Do not record the approved location. Keep an uncertain gap visible.", False),
        "addedSentence": (before + " Add a bounded check.", True),
        "ligatureNormalisation": ("Choose the genuine source. Record the approved location. Keep an uncertain gap visible. Add an efficient check.", True),
    }
    measured = {}
    for name, (after, expected) in cases.items():
        if name == "ligatureNormalisation":
            result = compare(before + " Add an efﬁcient check.", after)
        else:
            result = compare(before, after)
        measured[name] = {"expectedPass": expected, "observedPass": result["pass"], "fired": result["pass"] == expected, "measurement": result}
    table_before = "Claim / decision Source / date / locator Learner contribution and meaning Shared work / adult support Limit / status."
    table_after = "Claim / decision Source / date / locator Learner Shared work / Limit / status contribution and adult support meaning."
    projection = {
        "mutation": "layout projection walks the same table-header tokens in a different column order",
        "sentenceContainmentPass": compare(table_before, table_after)["pass"],
        "tokenMultisetIdentity": token_multiset(table_before) == token_multiset(table_after),
    }
    projection["fired"] = projection["sentenceContainmentPass"] is False and projection["tokenMultisetIdentity"] is True
    return {"cases": measured, "layoutProjectionControl": projection, "allFired": all(item["fired"] for item in measured.values()) and projection["fired"]}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("before")
    parser.add_argument("after")
    parser.add_argument("output")
    args = parser.parse_args()
    before_path, after_path = Path(args.before).resolve(), Path(args.after).resolve()
    before, after = extract(before_path), extract(after_path)
    semantic_names = ("pypdf", "pdftotextRaw")
    extractors = {name: compare(before[name], after[name]) for name in semantic_names}
    layout = compare(before["pdftotextLayout"], after["pdftotextLayout"])
    layout_tokens_equal = token_multiset(before["pdftotextLayout"]) == token_multiset(after["pdftotextLayout"])
    control = controls()
    passed = all(item["pass"] for item in extractors.values()) and control["allFired"]
    report = {
        "gate": "c-gate-printed-pupil-text",
        "mode": "containment",
        "beforePdf": str(before_path),
        "afterPdf": str(after_path),
        "normalisation": "NFKC, fi/fl/ff/ffi/ffl ligatures, soft-hyphen removal, whitespace collapse, case-fold",
        "extractors": extractors,
        "pdftotextLayoutDiagnostic": {
            "measurement": layout,
            "tokenMultisetIdentity": layout_tokens_equal,
            "classification": "LAYOUT-PROJECTION-ONLY" if not layout["pass"] and layout_tokens_equal and extractors["pdftotextRaw"]["pass"] else "AGREES-WITH-SEMANTIC-EXTRACTORS" if layout["pass"] else "CONTENT-DIFFERENCE",
            "gating": False,
            "reason": "-layout may traverse unchanged table columns in geometry-dependent order; -raw remains the Poppler semantic extractor and all mutation/order controls apply to it",
        },
        "controls": control,
        "status": "PASS" if passed else "RED",
    }
    output = ROOT / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "extractors": {key: value["pass"] for key, value in extractors.items()}, "controlsAllFired": control["allFired"]}, indent=2))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
