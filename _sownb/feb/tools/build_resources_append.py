#!/usr/bin/env python3
"""Build and validate the ORDER FEB wave-one resources.json append."""
from __future__ import annotations

import argparse
import difflib
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
ADDED = [
    {
        "id": "catalogue-2026-27-science-build-w14-w20-feb-wave1",
        "title": "BUILD Science · Weeks 14–16 · review and fossils",
        "type": "teacher", "subject": "Science · Teesside", "year": "2026-27",
        "file": "Science_Teesside/Build/W14-W20_2026-27/START_HERE.html",
        "desc": "Start page for six BUILD Science lessons on autumn review, fossil formation and fossil evidence.",
        "family": "BUILD Science",
        "keywords": ["build", "science", "weeks 14–16", "review", "fossils", "start here"],
        "added": "2026-09-01",
    },
    {
        "id": "catalogue-2026-27-science-launch-autumn2-w7-feb-wave1",
        "title": "LAUNCH Science · Autumn 2 Week 7 · Topics 2–3 assessment",
        "type": "teacher", "subject": "Science · Teesside", "year": "2026-27",
        "file": "Science_Teesside/Launch/Autumn2_W7_2026-27/START_HERE.html",
        "desc": "Start page for three LAUNCH Science lessons that introduce, complete and review the supplied Topics 2–3 assessment.",
        "family": "LAUNCH Science",
        "keywords": ["launch", "science", "autumn 2", "week 7", "assessment", "start here"],
        "added": "2026-09-01",
    },
    {
        "id": "catalogue-2026-27-science-grow-w15-w16-feb-wave1",
        "title": "GROW Science · Weeks 15–16 · materials and solubility",
        "type": "teacher", "subject": "Science · Teesside", "year": "2026-27",
        "file": "Science_Teesside/Grow/W15-W20_2026-27/START_HERE.html",
        "desc": "Start page for three GROW Science lessons on material properties, solubility and recovering a substance from solution.",
        "family": "GROW Science",
        "keywords": ["grow", "science", "weeks 15–16", "materials", "solubility", "start here"],
        "added": "2026-09-01",
    },
    {
        "id": "catalogue-2026-27-science-launch-w15-feb-wave1",
        "title": "LAUNCH Science · Week 15 · variation and natural selection",
        "type": "teacher", "subject": "Science · Teesside", "year": "2026-27",
        "file": "Science_Teesside/Launch/W15-W20_2026-27/START_HERE.html",
        "desc": "Start page for three LAUNCH Science lessons on variation, natural selection evidence and cautious explanation.",
        "family": "LAUNCH Science",
        "keywords": ["launch", "science", "week 15", "variation", "natural selection", "start here"],
        "added": "2026-09-01",
    },
    {
        "id": "catalogue-2026-27-humanities-build-w14-w15-feb-wave1",
        "title": "BUILD Humanities · Weeks 14–15 · festivals, time and caring",
        "type": "teacher", "subject": "Humanities", "year": "2026-27",
        "file": "Humanities_Teesside/BUILD_W14-W20_2026-27/START_HERE.html",
        "desc": "Start page for two BUILD Humanities lessons on festival evidence, timelines and caring stories.",
        "family": "BUILD Humanities",
        "keywords": ["build", "humanities", "weeks 14–15", "festivals", "timeline", "start here"],
        "added": "2026-09-01",
    },
    {
        "id": "catalogue-2026-27-humanities-grow-w15-feb-wave1",
        "title": "GROW Humanities · Week 15 · rights and belief resilience",
        "type": "teacher", "subject": "Humanities", "year": "2026-27",
        "file": "Humanities_Teesside/GROW_W15-W20_2026-27/START_HERE.html",
        "desc": "Start page for the GROW Humanities lesson on a rights timeline and careful accounts of belief resilience.",
        "family": "GROW Humanities",
        "keywords": ["grow", "humanities", "week 15", "rights", "belief", "start here"],
        "added": "2026-09-01",
    },
    {
        "id": "catalogue-2026-27-humanities-launch-w15-feb-wave1",
        "title": "LAUNCH Humanities · Week 15 · conflict and ethical decisions",
        "type": "teacher", "subject": "Humanities", "year": "2026-27",
        "file": "Humanities_Teesside/LAUNCH_W15-W20_2026-27/START_HERE.html",
        "desc": "Start page for the LAUNCH Humanities lesson on conflict causes, evidence limits and ethical decisions.",
        "family": "LAUNCH Humanities",
        "keywords": ["launch", "humanities", "week 15", "conflict", "ethics", "start here"],
        "added": "2026-09-01",
    },
    {
        "id": "catalogue-2026-27-asdan-build-spring1-w15-w16-feb-wave1",
        "title": "BUILD ASDAN · Weeks 15–16 · choices and project goals",
        "type": "teacher", "subject": "BUILD Vocational & PfA", "year": "2026-27",
        "file": "BUILD_ASDAN/Spring1_W1-W6_2026-27/START_HERE.html",
        "desc": "Start page for two BUILD ASDAN lessons on choices, budgeting, partner challenges and seasonal project goals.",
        "family": "BUILD ASDAN · Spring 1",
        "keywords": ["build", "asdan", "spring 1", "weeks 15–16", "budget", "project", "start here"],
        "added": "2026-09-01",
    },
    {
        "id": "catalogue-2026-27-asdan-grow-spring1-w15-w16-feb-wave1",
        "title": "GROW ASDAN · Weeks 15–16 · strengths and project planning",
        "type": "teacher", "subject": "GROW Vocational & PfA", "year": "2026-27",
        "file": "GROW_ASDAN/Spring1_W1-W6_2026-27/START_HERE.html",
        "desc": "Start page for two GROW ASDAN lessons on strengths, an authorised task, project planning and honest goals.",
        "family": "GROW ASDAN · Spring 1",
        "keywords": ["grow", "asdan", "spring 1", "weeks 15–16", "strengths", "project", "start here"],
        "added": "2026-09-01",
    },
    {
        "id": "catalogue-2026-27-asdan-launch-spring1-w16-feb-wave1",
        "title": "LAUNCH ASDAN · Week 16 · decisions and practical planning",
        "type": "teacher", "subject": "LAUNCH Vocational & PfA", "year": "2026-27",
        "file": "LAUNCH_ASDAN/Spring1_W1-W6_2026-27/START_HERE.html",
        "desc": "Start page for the LAUNCH ASDAN lesson on decision tools, banking, plant care and project planning.",
        "family": "LAUNCH ASDAN · Spring 1",
        "keywords": ["launch", "asdan", "spring 1", "week 16", "decisions", "banking", "start here"],
        "added": "2026-09-01",
    },
]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("output_directory")
    args = parser.parse_args()
    output = Path(args.output_directory).resolve()
    output.mkdir(parents=True, exist_ok=True)
    source_path = ROOT / "resources.json"
    source_bytes = source_path.read_bytes()
    source = json.loads(source_bytes)
    existing_count = 667
    if len(source) != existing_count:
        raise SystemExit(f"expected {existing_count} existing objects, measured {len(source)}")
    if not source_bytes.endswith(b"\n]\n"):
        raise SystemExit("resources.json terminal shape changed; textual append not attempted")
    old_ids = {row["id"] for row in source}
    new_ids = [row["id"] for row in ADDED]
    if old_ids.intersection(new_ids) or len(new_ids) != len(set(new_ids)):
        raise SystemExit("duplicate catalogue id")
    missing = [row["file"] for row in ADDED if not (ROOT / row["file"]).is_file()]
    if missing:
        raise SystemExit("unresolved catalogue targets: " + ", ".join(missing))
    appended_text = ",\n" + ",\n".join(json.dumps(row, indent=2, ensure_ascii=False) for row in ADDED) + "\n]\n"
    candidate_bytes = source_bytes[:-3] + appended_text.encode("utf-8")
    candidate = json.loads(candidate_bytes)
    prefix_identity = candidate[:existing_count] == source
    raw_prefix_identity = candidate_bytes.startswith(source_bytes[:-3])
    if not prefix_identity or not raw_prefix_identity or len(candidate) != existing_count + len(ADDED):
        raise SystemExit("existing-object identity or append cardinality failed")
    candidate_path = output / "resources.planned.json"
    patch_path = output / "resources.append.patch"
    report_path = output / "resources.append.validation.json"
    candidate_path.write_bytes(candidate_bytes)
    diff = difflib.unified_diff(
        source_bytes.decode("utf-8").splitlines(keepends=True),
        candidate_bytes.decode("utf-8").splitlines(keepends=True),
        fromfile="a/resources.json", tofile="b/resources.json",
    )
    patch_path.write_text("".join(diff), encoding="utf-8")
    report = {
        "gate": "g13-resources-append-nonmutation",
        "source": "resources.json",
        "sourceSha256": hashlib.sha256(source_bytes).hexdigest(),
        "existingObjects": len(source),
        "plannedObjects": len(candidate),
        "existingObjectsIdentity": prefix_identity,
        "rawPrefixIdentity": raw_prefix_identity,
        "newObjects": ADDED,
        "newTargetsResolve": not missing,
        "sourceWorkingTreeUnchanged": hashlib.sha256(source_path.read_bytes()).hexdigest() == hashlib.sha256(source_bytes).hexdigest(),
        "status": "PASS",
    }
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "existing": len(source), "planned": len(candidate), "sourceSha256": report["sourceSha256"], "newIds": new_ids}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
