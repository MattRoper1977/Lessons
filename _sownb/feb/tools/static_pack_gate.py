#!/usr/bin/env python3
"""RSH-3 carried static battery plus pack/checksum/chain integrity."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

from lxml import html

ROOT = Path(__file__).resolve().parents[3]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def lesson_config(tree) -> dict:
    nodes = tree.xpath('//script[@id="lesson-config"]')
    return json.loads(nodes[0].text) if len(nodes) == 1 and nodes[0].text else {}


def is_lesson_source(source: str) -> bool:
    """Classify a teaching surface by its rendered lesson role, not its name."""
    try:
        tree = html.fromstring(source)
    except Exception:
        return False
    return bool(tree.xpath('//main[contains(concat(" ",normalize-space(@class)," ")," deck ")]'))


def judge_source(source: str, path: Path) -> dict[str, object]:
    tree = html.fromstring(source)
    ids = [item for item in tree.xpath('//*[@id]/@id')]
    duplicates = sorted({item for item in ids if ids.count(item) > 1})
    slides = tree.xpath('//main[contains(concat(" ",normalize-space(@class)," ")," deck ")]/section[contains(concat(" ",normalize-space(@class)," ")," slide ")]')
    minutes = [float(node.get("data-min")) for node in slides if node.get("data-min") is not None]
    config = lesson_config(tree)
    config_minutes = [float(item) for item in config.get("timings", [])]
    confirmation = tree.xpath('//*[contains(concat(" ",normalize-space(@class)," ")," print-pack ")]//*[contains(concat(" ",normalize-space(@class)," ")," n6-lc-page ")]')
    foreign_runtime = {token: source.count(token) for token in ("fetch(", "XMLHttpRequest", "serviceWorker", "http://", "https://", "localStorage", "sessionStorage", "data:")}
    checks = {
        "uniqueIds": not duplicates,
        "nineSlides": len(slides) == 9,
        "timingsMatch": len(minutes) == 9 and minutes == config_minutes and sum(minutes) == 40,
        "noKeyframes": "@keyframes" not in source.lower(),
        "offlineRuntime": all(value == 0 for value in foreign_runtime.values()),
        "confirmationInsidePrintPack": len(confirmation) == 1,
        "workbookTrace": all(config.get("source", {}).get(key) for key in ("workbook", "sheet", "cell", "outcome")),
        "guideRevealRevert": bool(re.search(r"html\.mbm-guide-on\s*\[data-mbm-guide\]\s*\{\s*display:revert!important", source)) and not bool(re.search(r"html\.mbm-guide-on\s*\[data-mbm-guide\]\s*\{\s*display:block!important", source)),
        "overlayFlex": ".overlay.on{display:flex}" in source,
        "navMarkers": source.count("<!--n6-nav1:v1-->") >= 2 and source.count("<!--/n6-nav1-->") >= 2,
    }
    return {"file": str(path.relative_to(ROOT)), "sha256": hashlib.sha256(source.encode()).hexdigest(), "measurements": {"ids": len(ids), "duplicateIds": duplicates, "slides": len(slides), "dataMinutes": minutes, "configMinutes": config_minutes, "foreignRuntime": foreign_runtime, "confirmationInsidePrintPack": len(confirmation)}, "checks": checks, "pass": all(checks.values()), "config": config}


def checksum_gate(pack: Path, checksum: Path) -> dict[str, object]:
    rows = []
    for line in checksum.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        digest, name = line.split(None, 1)
        name = name.strip().lstrip("*")
        target = pack / name
        rows.append({"file": name, "declared": digest, "exists": target.is_file(), "actual": sha(target) if target.is_file() else None})
    expected = sorted(
        [str(item.relative_to(pack)) for item in pack.rglob("*.html")]
        + [str(item.relative_to(pack)) for item in pack.rglob("manifest*.json")]
    )
    actual = sorted(item["file"] for item in rows)
    return {"file": checksum.name, "rows": rows, "expectedEntrySet": expected, "actualEntrySet": actual, "entrySetExact": expected == actual, "hashesExact": all(row["exists"] and row["declared"] == row["actual"] for row in rows), "pass": expected == actual and all(row["exists"] and row["declared"] == row["actual"] for row in rows)}


def chain_gate(pack: Path, lessons: list[Path]) -> dict[str, object]:
    rows = []
    configs = {}
    for lesson in lessons:
        tree = html.fromstring(lesson.read_text(encoding="utf-8"))
        configs[lesson.resolve()] = lesson_config(tree)
    for lesson, config in configs.items():
        row = {"file": str(lesson.relative_to(pack)), "previousFile": config.get("previousFile"), "nextFile": config.get("nextFile"), "links": []}
        for key in ("previousFile", "nextFile"):
            value = config.get(key)
            if value:
                target = (lesson.parent / value).resolve()
                reciprocal_key = "nextFile" if key == "previousFile" else "previousFile"
                reciprocal = None
                if target in configs:
                    reciprocal = configs[target].get(reciprocal_key) == lesson.name
                row["links"].append({"kind": key, "target": str(target), "exists": target.is_file(), "reciprocal": reciprocal})
        rows.append(row)
    links = [link for row in rows for link in row["links"]]
    return {
        "rows": rows,
        "pass": bool(links) and all(link["exists"] and link["reciprocal"] is not False for link in links),
        "nonVacuous": bool(links),
    }


def controls() -> dict[str, object]:
    seed = '<main class="deck"><section class="slide" data-min="40"><div id="one"></div></section></main><div class="print-pack"><div class="n6-lc-page"></div></div><script id="lesson-config" type="application/json">{"timings":[40],"source":{"workbook":"w","sheet":"s","cell":"C1","outcome":"o"}}</script><!--n6-nav1:v1--><!--/n6-nav1--><!--n6-nav1:v1--><!--/n6-nav1--><style>[data-mbm-guide]{display:none!important}html.mbm-guide-on [data-mbm-guide]{display:revert!important}.overlay.on{display:flex}</style>'
    cases = {
        "duplicateId": seed.replace('</div></section>', '</div><div id="one"></div></section>'),
        "timingPlusOne": seed.replace('data-min="40"', 'data-min="41"'),
        "networkRuntime": seed + '<script>fetch("https://invalid.example")</script>',
        "storageRuntime": seed + '<script>localStorage.setItem("planted","1")</script>',
        "dataUri": seed + '<img src="data:image/png;base64,AA==">',
        "keyframes": seed + '<style>@keyframes planted{}</style>',
        "confirmationDeletion": seed.replace('class="n6-lc-page"', 'class="removed"'),
    }
    results = {}
    for name, source in cases.items():
        result = judge_source(source, ROOT / "_sownb/rsh3/fixtures/control.html")
        results[name] = {"expectedPass": False, "observedPass": result["pass"], "fired": not result["pass"]}
    classifier = {
        "lessonPositive": is_lesson_source(seed),
        "frontDoorAliasNegative": not is_lesson_source('<main><a href="lesson.html">Open lesson</a></main>'),
    }
    classifier["fired"] = all(classifier.values())
    return {"cases": results, "supportClassifier": classifier, "allFired": all(item["fired"] for item in results.values()) and classifier["fired"]}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pack", required=True)
    parser.add_argument("--checksum", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    pack = ROOT / args.pack
    html_files = sorted(pack.rglob("*.html"))
    lessons = [item for item in html_files if is_lesson_source(item.read_text(encoding="utf-8"))]
    static = [judge_source(path.read_text(encoding="utf-8"), path) for path in lessons]
    checksums = checksum_gate(pack, pack / args.checksum)
    chains = chain_gate(pack, lessons)
    control = controls()
    passed = all(item["pass"] for item in static) and checksums["pass"] and chains["pass"] and control["allFired"]
    report = {"gate": "rsh3-static-pack-integrity", "pack": args.pack, "lessonSelection": {"rule": "HTML carrying main.deck", "htmlFiles": [str(item.relative_to(pack)) for item in html_files], "selectedLessons": [str(item.relative_to(pack)) for item in lessons]}, "lessons": static, "checksums": checksums, "chains": chains, "controls": control, "status": "PASS" if passed else "RED"}
    output = ROOT / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "lessons": len(lessons), "static": [item["pass"] for item in static], "checksum": checksums["pass"], "chains": chains["pass"], "controls": control["allFired"]}, indent=2))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
