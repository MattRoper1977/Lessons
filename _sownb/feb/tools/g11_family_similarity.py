#!/usr/bin/env python3
"""Family-parameterised g11 with an active chassis allowlist and bound content floor."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
import re
import sys
from dataclasses import dataclass
from pathlib import Path

from lxml import html


ROOT = Path(__file__).resolve().parents[3]
TOKEN = re.compile(r"[a-z0-9]+(?:['’-][a-z0-9]+)*", re.I)
FAMILY = {
    "GROW Science": {
        "patterns": ["Science_Teesside/Grow/W8-W13_2026-27/SCI_*.html"],
        "ceiling": 0.15806601580660157,
        "group": "GROW Science Autumn 2 W7",
    },
    "GROW ASDAN": {
        "patterns": ["GROW_ASDAN/Autumn2_W1-W6_2026-27/PEQ_*.html"],
        "ceiling": 0.11764705882352941,
        "group": "GROW ASDAN PEQ W7",
    },
    "LAUNCH ASDAN": {
        "patterns": ["LAUNCH_ASDAN/W7-W12_2026-27/lessons/**/*.html"],
        "ceiling": 0.2858048162230672,
        "group": "LAUNCH ASDAN pack p95",
    },
    "LAUNCH Science": {
        "patterns": ["Science_Teesside/Launch/W8-W13_2026-27/SCI_*.html"],
        "ceiling": 0.1884576098059244,
        "group": "LAUNCH Science W14",
    },
    "BUILD Science": {
        "patterns": ["Science_Teesside/Build/W8-W13_2026-27/SCI_*.html"],
        "ceiling": None,
        "group": "nearest sibling BUILD Science W8-W13 pack p95",
    },
    "BUILD Humanities": {
        "patterns": ["Humanities_Teesside/BUILD_W9-W14_2026-27/BUILD_HUM_*.html"],
        "ceiling": None,
        "group": "nearest sibling BUILD Humanities W9-W14 pack p95",
    },
    "BUILD ASDAN": {
        "patterns": ["BUILD_ASDAN/Autumn2_W1-W6_2026-27/BUILD_ASDAN_A2_*.html"],
        "ceiling": None,
        "group": "nearest sibling BUILD ASDAN Autumn 2 pack p95",
    },
    "GROW Humanities": {
        "patterns": ["Humanities_Teesside/GROW_W9-W14_2026-27/GROW_HUM_*.html"],
        "ceiling": None,
        "group": "nearest sibling GROW Humanities W9-W14 pack p95",
    },
    "LAUNCH Humanities": {
        "patterns": ["Humanities_Teesside/LAUNCH_W9-W14_2026-27/LAUNCH_HUM_*.html"],
        "ceiling": None,
        "group": "nearest sibling LAUNCH Humanities W9-W14 pack p95",
    },
}
CHASSIS_CLASSES = ("lundy", "ladder", "chips", "tag", "time", "brandline", "sowline")


@dataclass(frozen=True)
class Lesson:
    name: str
    path: Path
    slides: tuple[tuple[str, ...], ...]

    @property
    def tokens(self) -> tuple[str, ...]:
        return tuple(token for slide in self.slides for token in slide)


def tokenise(value: str) -> tuple[str, ...]:
    return tuple(match.group(0).casefold() for match in TOKEN.finditer(value))


def extract(path: Path) -> Lesson:
    tree = html.fromstring(path.read_text(encoding="utf-8"))
    decks = tree.xpath('//main[contains(concat(" ",normalize-space(@class)," ")," deck ")]')
    if len(decks) != 1:
        raise ValueError(f"{path}: expected one main.deck, found {len(decks)}")
    slides = []
    for source in decks[0].xpath('./section[contains(concat(" ",normalize-space(@class)," ")," slide ")]'):
        node = html.fromstring(html.tostring(source, encoding="unicode"))
        discard = node.xpath(
            './/script|.//style|.//svg|.//*[@aria-hidden="true"]|.//*[@data-mbm-guide]|'
            './/*[@data-addressee="staff"]|.//*[@data-audience="staff"]|'
            './/*[contains(concat(" ",normalize-space(@class)," ")," controls ")]|'
            + "|".join(
                f'.//*[contains(concat(" ",normalize-space(@class)," ")," {class_name} ")]'
                for class_name in CHASSIS_CLASSES
            )
        )
        for child in discard:
            parent = child.getparent()
            if parent is not None:
                parent.remove(child)
        slides.append(tokenise(" ".join(node.text_content().split())))
    if not slides or not any(slides):
        raise ValueError(f"{path}: pupil corpus is empty")
    return Lesson(path.name, path, tuple(slides))


def shingles(tokens: tuple[str, ...], width: int = 5) -> set[tuple[str, ...]]:
    return {tokens[index:index + width] for index in range(max(0, len(tokens) - width + 1))}


def jaccard(left: set, right: set) -> float:
    union = left | right
    return len(left & right) / len(union) if union else 0.0


def document_score(left: Lesson, right: Lesson) -> float:
    return jaccard(shingles(left.tokens), shingles(right.tokens))


def slide_pair_max(left: Lesson, right: Lesson) -> tuple[float, int, int]:
    best = (-1.0, -1, -1)
    for left_index, left_tokens in enumerate(left.slides):
        for right_index, right_tokens in enumerate(right.slides):
            score = jaccard(shingles(left_tokens), shingles(right_tokens))
            if (score, -left_index, -right_index) > (best[0], -best[1], -best[2]):
                best = (score, left_index, right_index)
    return best


def allow_sequences() -> tuple[list[tuple[str, ...]], list[dict]]:
    contract = json.loads((ROOT / "_sownb/STYLE_CONTRACT.json").read_text(encoding="utf-8"))
    evidence = []
    sequences = []
    for row in contract["rows"]:
        if row.get("kind") not in {"visible-string", "byte-block"} or not isinstance(row.get("value"), str):
            continue
        value = row["value"]
        if row["kind"] == "byte-block":
            try:
                fragment = html.fragment_fromstring(value, create_parent=True)
                for node in fragment.xpath(".//script|.//style|.//svg"):
                    node.getparent().remove(node)
                value = " ".join(fragment.text_content().split())
            except Exception:
                value = ""
        tokens = tokenise(value)
        if 0 < len(tokens) <= 20:
            sequences.append(tokens)
            evidence.append({"row": row["id"], "tokens": list(tokens)})
    return sorted(set(sequences), key=lambda item: (-len(item), item)), evidence


def subtract(tokens: tuple[str, ...], sequences: list[tuple[str, ...]]) -> tuple[str, ...]:
    result = []
    index = 0
    while index < len(tokens):
        hit = next((sequence for sequence in sequences if tokens[index:index + len(sequence)] == sequence), None)
        if hit:
            index += len(hit)
        else:
            result.append(tokens[index])
            index += 1
    return tuple(result)


def adjusted(lesson: Lesson, sequences: list[tuple[str, ...]]) -> Lesson:
    return Lesson(lesson.name, lesson.path, tuple(subtract(slide, sequences) for slide in lesson.slides))


def paths_for(config: dict) -> list[Path]:
    paths = []
    for pattern in config["patterns"]:
        paths.extend(ROOT.glob(pattern))
    return sorted({path.resolve() for path in paths if path.is_file()})


def peer_paths(candidate_path: Path) -> list[Path]:
    """Return authored teaching peers in the candidate's destination pack.

    The donor pack still derives the ceiling.  These peers only extend the
    comparison surface so repeated prose created during this run cannot hide
    behind a clean comparison with older donors.
    """
    peers = []
    for path in sorted(candidate_path.parent.glob("*.html")):
        if path.resolve() == candidate_path or path.name.startswith("START_HERE"):
            continue
        source = path.read_text(encoding="utf-8")
        if re.search(r'<main\b[^>]*class=["\'][^"\']*\bdeck\b', source, re.I):
            peers.append(path.resolve())
    return peers


def nearest_rank(values: list[float], proportion: float) -> float:
    ordered = sorted(values)
    if not ordered:
        raise ValueError("cannot derive p95 from an empty comparison set")
    return ordered[max(0, math.ceil(proportion * len(ordered)) - 1)]


def g18_measurement(path: Path) -> dict:
    module_path = ROOT / "_sownb/feb/tools/g18_measurement.py"
    spec = importlib.util.spec_from_file_location("rsh3_g18_binding", module_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module.count_lesson(path)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--family", required=True, choices=sorted(FAMILY))
    parser.add_argument("--candidate", required=True)
    parser.add_argument("--g18", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    config = FAMILY[args.family]
    candidate_path = (ROOT / args.candidate).resolve()
    g18_path = (ROOT / args.g18).resolve()
    g18 = json.loads(g18_path.read_text(encoding="utf-8"))
    sequences, evidence = allow_sequences()
    baseline_raw = [extract(path) for path in paths_for(config)]
    peer_raw = [extract(path) for path in peer_paths(candidate_path)]
    candidate_raw = extract(candidate_path)
    baseline = [adjusted(item, sequences) for item in baseline_raw]
    peers = [adjusted(item, sequences) for item in peer_raw]
    candidate = adjusted(candidate_raw, sequences)
    pack_pairs = []
    for left_index, left in enumerate(baseline):
        for right in baseline[left_index + 1:]:
            pack_pairs.append({"left": left.name, "right": right.name, "score": document_score(left, right)})
    ceiling = nearest_rank([row["score"] for row in pack_pairs], 0.95)
    raw_rows = [{"against": item.name, "source": "donor-pack", "score": document_score(candidate_raw, item)} for item in baseline_raw]
    raw_rows += [{"against": item.name, "source": "destination-peer", "score": document_score(candidate_raw, item)} for item in peer_raw]
    rows = [{"against": item.name, "source": "donor-pack", "score": document_score(candidate, item)} for item in baseline]
    rows += [{"against": item.name, "source": "destination-peer", "score": document_score(candidate, item)} for item in peers]
    raw_max = max(raw_rows, key=lambda item: (item["score"], item["against"]))
    maximum = max(rows, key=lambda item: (item["score"], item["against"]))
    copies = []
    for other in baseline + peers:
        score, left_index, right_index = slide_pair_max(candidate, other)
        if score == 1.0 and len(shingles(candidate.slides[left_index])) >= 10:
            copies.append({"against": other.name, "candidateSlide": left_index + 1, "baselineSlide": right_index + 1})

    injection = next((item for item in sequences if item == ("ta", "brief")), next(item for item in sequences if len(item) >= 2))
    injected = candidate_raw.slides[0] + injection
    allowlist_control = {
        "defect": "contract chassis string injected into the first pupil-facing slide in memory",
        "string": " ".join(injection),
        "rawInjectedTokens": len(injection),
        "allowlistedInjectedTokens": len(subtract(injected, sequences)) - len(subtract(candidate_raw.slides[0], sequences)),
    }
    allowlist_control["fired"] = allowlist_control["rawInjectedTokens"] > 0 and allowlist_control["allowlistedInjectedTokens"] == 0

    donor, donor_index, donor_tokens = max(
        ((lesson, index, tokens) for lesson in baseline for index, tokens in enumerate(lesson.slides)),
        key=lambda item: len(shingles(item[2])),
    )
    planted = Lesson("IN_MEMORY_COPY.html", Path("<in-memory>"), candidate.slides + (donor_tokens,))
    copy_score, planted_index, donor_hit = slide_pair_max(planted, donor)
    copy_control = {
        "defect": "one exact substantial destination slide appended after chassis subtraction",
        "donor": donor.name,
        "donorSlide": donor_index + 1,
        "score": copy_score,
        "fired": copy_score == 1.0 and planted_index == len(planted.slides) - 1 and donor_hit == donor_index,
    }

    current_floor = g18_measurement(candidate_path)
    floor_bound = (
        g18.get("status") == "PASS"
        and g18.get("candidate", {}).get("file") == candidate_path.name
        and g18.get("candidate", {}).get("wordFloorPass") is True
        and g18.get("candidate", {}).get("totalWords") == current_floor["totalWords"]
        and g18.get("candidate", {}).get("slides") == current_floor["slides"]
    )
    floor_control = {
        "binding": {"g18": str(g18_path), "g18Sha256": hashlib.sha256(g18_path.read_bytes()).hexdigest(), "candidateFile": g18.get("candidate", {}).get("file"), "candidateStatus": g18.get("status"), "currentSourceSha256": hashlib.sha256(candidate_path.read_bytes()).hexdigest(), "recomputedWords": current_floor["totalWords"]},
        "mutation": "substitute a different candidate basename in the binding predicate",
        "expectedPass": False,
        "observedPass": floor_bound and g18.get("candidate", {}).get("file") == "PLANTED_DIFFERENT_CANDIDATE.html",
    }
    floor_control["fired"] = floor_bound and floor_control["observedPass"] is False
    non_vacuous = len(baseline) >= 2 and bool(pack_pairs) and bool(shingles(candidate.tokens)) and ceiling > 0
    passed = non_vacuous and maximum["score"] <= ceiling and not copies and allowlist_control["fired"] and copy_control["fired"] and floor_control["fired"]
    report = {
        "gate": "g11-family-parameterised-chassis-aware-similarity",
        "family": args.family,
        "method": "5-token set-Jaccard on main.deck pupil core; named chassis furniture excluded and exact contract chassis sequences removed before adjusted comparison",
        "ceiling": {"value": ceiling, "rung": "nearest sibling pack p95", "group": config["group"], "source": "current baseline, adjusted corpus, nearest-rank p95", "carriedPrediction": config["ceiling"], "deltaFromCarriedPrediction": None if config["ceiling"] is None else ceiling - config["ceiling"]},
        "baseline": {"patterns": config["patterns"], "count": len(baseline), "files": [item.name for item in baseline], "pairCount": len(pack_pairs), "pairScores": pack_pairs, "nonVacuous": non_vacuous, "excludedChassisClasses": list(CHASSIS_CLASSES)},
        "destinationPeers": {"count": len(peers), "files": [item.name for item in peers], "role": "comparison only; donor pack p95 remains the ceiling rung"},
        "candidate": {
            "file": args.candidate,
            "sha256": hashlib.sha256(candidate_path.read_bytes()).hexdigest(),
            "withoutAllowlist": {"maximum": raw_max, "all": raw_rows},
            "withAllowlist": {"maximum": maximum, "all": rows},
            "exactCopiedSlidesAfterAllowlist": copies,
            "g18Status": g18.get("status"),
        },
        "chassisStrings": {"contractRows": len(evidence), "uniqueTokenSequences": len(sequences), "rows": evidence},
        "allowlistFiringControl": allowlist_control,
        "redProof": copy_control,
        "floorBindingRedControl": floor_control,
        "status": "PASS" if passed else "RED",
    }
    output = (ROOT / args.output).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "family": args.family, "baseline": len(baseline), "destinationPeers": len(peers), "pairCount": len(pack_pairs), "ceiling": ceiling, "carriedPrediction": config["ceiling"], "maximum": maximum, "allowlistFired": allowlist_control["fired"], "copyControlFired": copy_control["fired"], "floorControlFired": floor_control["fired"]}, indent=2))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
