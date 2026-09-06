#!/usr/bin/env python3
"""c-gate: preserve every pre-existing printed token; permit only declared additions."""

from __future__ import annotations

import collections
import json
import re
import subprocess
import sys
import unicodedata
from pathlib import Path

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[3]
WORD = re.compile(r"[A-Za-z0-9]+(?:['’-][A-Za-z0-9]+)*")
LIGATURES = str.maketrans({"ﬁ": "fi", "ﬂ": "fl", "ﬀ": "ff", "ﬃ": "ffi", "ﬄ": "ffl"})


def normalise(text: str) -> str:
    return " ".join(unicodedata.normalize("NFKC", text.translate(LIGATURES)).split())


def tokens(text: str) -> list[str]:
    return [item.lower() for item in WORD.findall(normalise(text))]


def extract(pdf: Path) -> dict[str, str]:
    reader = PdfReader(pdf)
    pypdf = "\f".join(page.extract_text() or "" for page in reader.pages)
    poppler = subprocess.run(["pdftotext", "-layout", str(pdf), "-"], check=True, text=True, capture_output=True).stdout
    return {"pypdf": normalise(pypdf), "pdftotext": normalise(poppler)}


def compare(before: str, after: str, additions: list[str]) -> dict:
    left, right = tokens(before), tokens(after)
    extras = []
    index = 0
    for position, token in enumerate(right):
        if index < len(left) and token == left[index]:
            index += 1
        else:
            extras.append({"position": position, "token": token})
    preserved = index == len(left)
    declared = collections.Counter(tokens(" ".join(additions)))
    extra_counts = collections.Counter(item["token"] for item in extras)
    undeclared = {token: count - declared[token] for token, count in extra_counts.items() if count > declared[token]}
    return {
        "beforeTokens": len(left), "afterTokens": len(right),
        "preservedAsOrderedSubsequence": preserved,
        "insertedTokens": extras,
        "undeclaredInsertedTokenCounts": undeclared,
        "pass": preserved and not undeclared,
    }


def main() -> int:
    if len(sys.argv) < 4:
        raise SystemExit("usage: c_gate_print_identity.py BEFORE.pdf AFTER.pdf ADDITIONS.json [OUTPUT]")
    before_pdf, after_pdf, additions_path = ((ROOT / item).resolve() for item in sys.argv[1:4])
    additions_payload = json.loads(additions_path.read_text(encoding="utf-8"))
    additions = additions_payload.get("additions", [])
    before, after = extract(before_pdf), extract(after_pdf)
    arms = {name: compare(before[name], after[name], additions) for name in ("pypdf", "pdftotext")}

    planted_tokens = tokens(before["pypdf"])
    planted_after = planted_tokens[:]
    if planted_after:
        planted_after[min(10, len(planted_after) - 1)] = "rshplantedwordchange"
    planted = compare(" ".join(planted_tokens), " ".join(planted_after), [])
    red = {
        "defect": "one existing pypdf word changed in memory",
        "fired": not planted["pass"] and not planted["preservedAsOrderedSubsequence"],
        "measurement": planted,
    }
    pass_now = all(item["pass"] for item in arms.values()) and red["fired"]
    report = {
        "gate": "c-gate-printed-pupil-text-identity",
        "beforePdf": str(before_pdf.relative_to(ROOT)),
        "afterPdf": str(after_pdf.relative_to(ROOT)),
        "ligatureNormalisation": True,
        "declaredAdditions": additions,
        "extractors": arms,
        "redProof": red,
        "status": "PASS" if pass_now else "RED",
    }
    output = (ROOT / sys.argv[4]).resolve() if len(sys.argv) > 4 else ROOT / "_sownb/rsh/output/c_gate.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"gate": report["gate"], "status": report["status"], "arms": {name: item["pass"] for name, item in arms.items()}, "redProofFired": red["fired"]}, indent=2))
    return 0 if pass_now else 1


if __name__ == "__main__":
    raise SystemExit(main())
