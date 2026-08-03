#!/usr/bin/env python3
"""Independent controls and wrappers for the Art Teesside instruments.

The historical instruments deliberately expose known findings. This wrapper
prevents a raw process exit code from being mistaken for a clean estate:

* the closed-kit instrument's non-empty current totals are parsed and asserted;
* the co-occurrence instrument must fail with the exact known baseline, not pass;
* the co-occurrence zero calibration is replayed against its documented historical
  control revision using the current instrument;
* the estate and print instruments are proved capable of detecting a safe,
  temporary defect without altering tracked files.

Run one contract at a time. Each subcommand has its own exit status so it can be
used as a separate deployment gate.
"""
from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
ART = REPO / "Art_Teesside"
TOOLS = ART / "tools"


def run(command: list[str], *, cwd: Path = REPO, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(command, cwd=cwd, env=env, text=True, capture_output=True)
    sys.stdout.write(result.stdout)
    sys.stderr.write(result.stderr)
    return result


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def kit_current() -> None:
    result = run([sys.executable, str(TOOLS / "assert_kit.py"), "--verbose"])
    require(result.returncode == 0, f"assert_kit.py process exit was {result.returncode}")
    require("AT-INST-04 closed-kit assertion - 53 files" in result.stdout, "closed-kit population was not 53")
    match = re.search(
        r"^TOTAL\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s*$",
        result.stdout,
        flags=re.M,
    )
    require(match is not None, "could not parse the closed-kit TOTAL row")
    totals = tuple(map(int, match.groups()))
    expected = (20, 0, 0, 11, 1, 2, 34)
    require(totals == expected, f"closed-kit baseline moved: found {totals}, expected {expected}")
    print(f"CLOSED-KIT CONTRACT PASS — population 53, parsed totals {totals}")


def cooccurrence_current() -> None:
    result = run([sys.executable, str(TOOLS / "assert_cooccurrence.py")])
    require(result.returncode == 1, f"co-occurrence raw exit was {result.returncode}; expected known-finding exit 1")
    expected_fragments = [
        "Art Teesside co-occurrence assertions - 53 HTML files",
        "C1_award_level               0 finding(s)",
        "C2_term                      0 finding(s)",
        "C2_week                      0 finding(s)",
        "C3_kit_beside_disavowal      1 finding(s)",
        "Grow/GROW_ART_W2_Studio_Skills_and_Safe_Practice.html",
        "C5_route_contradiction   Grow: disavowed in 1 file(s), taught in 1",
        "Grow/GROW_ART_W6_Plan_and_Rehearse_the_Skill_Share.html",
        "Launch/LAUNCH_ART_W6_Pilot_Lead_and_Adapt.html",
        "TOTAL 2",
        "declared legitimate pairings: 2",
    ]
    missing = [fragment for fragment in expected_fragments if fragment not in result.stdout]
    require(not missing, "co-occurrence baseline changed; missing output fragments: " + repr(missing))
    print("CO-OCCURRENCE CURRENT CONTRACT PASS — raw failure preserved as two declared pre-existing findings")


def archive_subtree(commit: str, destination: Path) -> None:
    archive = destination / "estate.tar"
    with archive.open("wb") as handle:
        result = subprocess.run(
            ["git", "archive", "--format=tar", commit, "Art_Teesside"],
            cwd=REPO,
            stdout=handle,
            stderr=subprocess.PIPE,
        )
    require(result.returncode == 0, f"git archive {commit} failed: {result.stderr.decode(errors='replace')}")
    with tarfile.open(archive) as bundle:
        bundle.extractall(destination, filter="data")
    archive.unlink()


def cooccurrence_control() -> None:
    # Documented in INSTRUMENTS_ART.md: this revision carries independently known
    # C1=7, C2_term=7 and C2_week=6 defects. The *current* instrument is copied
    # over that historical estate so this is a calibration of today's check.
    commit = "6486176"
    with tempfile.TemporaryDirectory(prefix="art-cooccurrence-control-") as raw:
        temp = Path(raw)
        archive_subtree(commit, temp)
        tools = temp / "Art_Teesside" / "tools"
        tools.mkdir(parents=True, exist_ok=True)
        shutil.copy2(TOOLS / "assert_cooccurrence.py", tools / "assert_cooccurrence.py")
        result = run([sys.executable, str(tools / "assert_cooccurrence.py")], cwd=temp)
        require(result.returncode == 1, f"historical control returned {result.returncode}, expected 1")
        expected = {
            "C1_award_level": 7,
            "C2_term": 7,
            "C2_week": 6,
        }
        for label, count in expected.items():
            match = re.search(rf"^{re.escape(label)}\s+(\d+) finding\(s\)", result.stdout, re.M)
            require(match is not None, f"historical control did not print {label}")
            require(int(match.group(1)) == count, f"historical {label}={match.group(1)}, expected {count}")
    print("CO-OCCURRENCE HISTORICAL CONTROL PASS — detected C1=7, C2_term=7, C2_week=6 at 6486176")


def estate_control() -> None:
    with tempfile.TemporaryDirectory(prefix="art-estate-control-") as raw:
        temp = Path(raw)
        target = temp / "Art_Teesside"
        shutil.copytree(ART, target, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        fixture = target / "Arts_Partnership_Log.html"
        fixture.write_text(fixture.read_text(encoding="utf-8") + "\n<p>AO1 deliberate assertion control</p>\n", encoding="utf-8")
        result = run([sys.executable, str(target / "tools" / "assert_estate.py")], cwd=temp)
        require(result.returncode == 1, f"estate control returned {result.returncode}, expected 1")
        require("A2_no_aos" in result.stdout and "MOVED" in result.stdout and "{'ao1': 1}" in result.stdout, "estate control did not expose the inserted AO1 defect")
    print("ESTATE POSITIVE CONTROL PASS — deliberate AO1 fixture was detected and tracked files were untouched")


def print_control() -> None:
    with tempfile.TemporaryDirectory(prefix="art-print-control-") as raw:
        temp = Path(raw) / "Art_Teesside"
        temp.mkdir(parents=True)
        pack_files = sorted(ART.rglob("*Pack*.html"))
        require(len(pack_files) == 8, f"print control expected 8 packs, found {len(pack_files)}")
        for source in pack_files:
            target = temp / source.relative_to(ART)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
        fixture = temp / pack_files[0].relative_to(ART)
        text = fixture.read_text(encoding="utf-8")
        require("</head>" in text, f"print control fixture has no </head>: {fixture}")
        text = text.replace("</head>", "<style>@media print{.a4{min-height:2000px!important}}</style></head>", 1)
        fixture.write_text(text, encoding="utf-8")
        env = os.environ.copy()
        env["ART_PRINT_ROOT"] = str(temp)
        result = run(["node", str(TOOLS / "assert_print.js"), "--verbose"], env=env)
        require(result.returncode == 1, f"print overflow control returned {result.returncode}, expected 1")
        match = re.search(r"overflowing\s+(\d+)", result.stdout)
        require(match is not None and int(match.group(1)) > 0, "print control did not report a non-zero overflow count")
    print("PRINT POSITIVE CONTROL PASS — deliberate 2000px sheet overflow was detected and tracked files were untouched")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "contract",
        choices=("kit-current", "cooccurrence-current", "cooccurrence-control", "estate-control", "print-control"),
    )
    args = parser.parse_args()
    actions = {
        "kit-current": kit_current,
        "cooccurrence-current": cooccurrence_current,
        "cooccurrence-control": cooccurrence_control,
        "estate-control": estate_control,
        "print-control": print_control,
    }
    try:
        actions[args.contract]()
    except (AssertionError, OSError, subprocess.SubprocessError) as exc:
        print(f"INSTRUMENT CONTRACT FAILED: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
