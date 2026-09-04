#!/usr/bin/env python3
"""Run every VB mechanism tool's controls, with the counts DERIVED.

WHY THIS EXISTS RATHER THAN A LIST OF `run:` STEPS IN A WORKFLOW
---------------------------------------------------------------
The workflow used to assert literals -- "18 controls", "133 tools". Both were
true on the day somebody typed them. Both stop being true the moment the estate
grows: adding lesson_stages.py alone moved the scanned-tool count from 130 to
131. A literal like that fails for the wrong reason, and the tempting repair is
to edit the number until it goes green, which is how a gate quietly stops
gating. (The apexpool hardcoded-count precedent is the same story.)

So nothing here is pinned. Each tool publishes its controls through
--list-controls; the battery asks for that list, runs --self-test, and requires
that EVERY LISTED CONTROL FIRED. The number is printed as a fact and never
asserted. A tool that adds a control needs no change here; a tool that loses one
still reds, because the tool's own report says how many it declared and how many
it ran.

--prove-red is the control on the battery itself. It copies one tool, inverts a
single control's expectation so that control cannot fire, and requires the
battery to go red on the copy. A battery that cannot be made to red is a green
tick with extra steps.

Usage:
  mechanism_battery.py                 run every tool's controls
  mechanism_battery.py --prove-red     prove the battery reds on a broken tool
  mechanism_battery.py --output r.json
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
TOOLS_DIR = ROOT / "_sownb/vb/tools"
VERSION = "mechanism-battery-v1.0.0"

# The mechanism, named once. Each entry is a tool that publishes --list-controls
# and runs --self-test. g19 is here for its control list only: its controls fire
# per-invocation against a real deck rather than in a standalone self-test, so
# the battery checks that it publishes them and the deck gates exercise them.
# The mechanism is not all in one directory. The Easter campaign tools live in
# tools/easter/ and were, until now, exercised by nobody: dedupe_stage_text.py
# landed in #280 carrying two bugs that only its OWN controls caught, and
# nothing in CI ran them. A tool whose controls are never run is a tool whose
# controls are decoration.
#
# An entry containing "/" is repo-relative and always resolves against ROOT; a
# bare name resolves against the tools directory the battery was handed. That
# distinction matters to --prove-red, which stages a COPY of the VB tools
# directory: a bare name follows the copy, which is the point, and a
# repo-relative one keeps pointing at the real file rather than at a path that
# happens not to exist beside the copy.
SELFTEST_TOOLS = [
    "lesson_stages.py",
    "g18_v2_family_floor.py",
    "g23_period_load.py",
    "g24_visual_density.py",
    "g25_wedo_variety.py",
    "g27_no_filename_weeks.py",
    "g29_plan_binding.py",
    "g30_arts_award.py",
    "cgate_containment.py",
    "classic_v2_contract_selftest.py",
    "tools/easter/dedupe_stage_text.py",
    "tools/easter/dedupe_sweep.py",
    "tools/easter/refresh_pack_checksums.py",
    "tools/easter/chrome_flip_list.py",
    "tools/easter/derive_stage_timings.py",
    "tools/easter/author_deck.py",
    "tools/easter/pack_furniture.py",
    "tools/easter/bind_plan_ids.py",
    "tools/easter/pick_art_donor.py",
    "tools/easter/strip_to_chassis.py",
    "tools/easter/prove_chassis.py",
    "tools/easter/build_batch3_targets.py",
    "tools/easter/manifest_sequence.py",
]
LIST_ONLY_TOOLS = [
    "g19_v2.py",
    "reshell_classic_v2.py",
    "reshell_classic_v2_contract.py",
]


def _run(args, cwd=None):
    return subprocess.run([sys.executable, *args], capture_output=True, text=True,
                          cwd=str(cwd or ROOT))


def _controls(tool: Path) -> list[str]:
    p = _run([str(tool), "--list-controls"])
    if p.returncode != 0:
        return []
    return [l.strip() for l in p.stdout.splitlines()
            if l.strip() and not l.startswith("warning:")]


def _selftest(tool: Path) -> tuple[int, str]:
    # g27 has no --self-test flag: its controls run on every invocation and its
    # exit code already carries the verdict.
    flag = [] if tool.name == "g27_no_filename_weeks.py" else ["--self-test"]
    p = _run([str(tool), *flag])
    return p.returncode, (p.stdout + p.stderr)


def _resolve(name: str, tools_dir: Path) -> Path:
    return (ROOT / name) if "/" in name else (tools_dir / name)


def battery(tools_dir: Path = TOOLS_DIR) -> dict:
    rows = []
    for name in SELFTEST_TOOLS:
        tool = _resolve(name, tools_dir)
        declared = _controls(tool)
        code, output = _selftest(tool)
        # the tool's own report is the authority on how many it ran
        m = re.search(r"(\d+)\s*/\s*(\d+)\s+(?:listed\s+)?controls", output)
        ran = int(m.group(2)) if m else None
        fired = int(m.group(1)) if m else None
        rows.append({
            "tool": Path(name).name,
            "toolPath": str(tool.relative_to(ROOT)) if tool.is_relative_to(ROOT) else str(tool),
            "controlsDeclared": len(declared),
            "controlsRun": ran,
            "controlsFired": fired,
            "exitCode": code,
            "allListedControlsFired": (
                code == 0 and bool(declared)
                and ran is not None and fired == ran and ran == len(declared)),
            "controls": declared,
        })
    for name in LIST_ONLY_TOOLS:
        declared = _controls(_resolve(name, tools_dir))
        rows.append({
            "tool": Path(name).name, "controlsDeclared": len(declared),
            "controlsRun": None, "controlsFired": None, "exitCode": 0,
            "allListedControlsFired": bool(declared),
            "note": "publishes its controls; they fire per-invocation against a real deck",
            "controls": declared,
        })
    ok = all(r["allListedControlsFired"] for r in rows)
    return {
        "battery": VERSION,
        "file": "_sownb/vb/tools/mechanism_battery.py",
        "toolsRun": len(rows),
        "controlsDeclaredTotal": sum(r["controlsDeclared"] for r in rows),
        "allListedControlsFired": ok,
        "note": ("every count above is DERIVED from --list-controls and each tool's "
                 "own report; no number in this battery or in the workflow that calls "
                 "it is pinned"),
        "rows": rows,
    }


def prove_red() -> dict:
    """Copy one tool, break exactly one control, require the battery to red."""
    with tempfile.TemporaryDirectory() as tmp:
        stage = Path(tmp) / "tools"
        shutil.copytree(TOOLS_DIR, stage)
        target = stage / "lesson_stages.py"
        src = target.read_text(encoding="utf-8")
        # invert one control's expectation so it cannot fire
        broken = src.replace(
            'record("classic-shell-is-seen",\n'
            '           "main.deck > .slide-container > div.slide is a stage",\n'
            '           "a classic-shell deck", 15, base_classic)',
            'record("classic-shell-is-seen",\n'
            '           "main.deck > .slide-container > div.slide is a stage",\n'
            '           "a classic-shell deck", 9999, base_classic)')
        planted = broken != src
        target.write_text(broken, encoding="utf-8")
        code, output = _selftest(target)
        row = next((r for r in battery(stage)["rows"] if r["tool"] == "lesson_stages.py"), {})
        return {
            "planted": "lesson_stages control `classic-shell-is-seen` expectation set to 9999",
            "mutationApplied": planted,
            "brokenToolExitCode": code,
            "batteryReds": planted and code != 0 and not row.get("allListedControlsFired"),
            "controlsFired": row.get("controlsFired"),
            "controlsRun": row.get("controlsRun"),
        }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--prove-red", action="store_true")
    ap.add_argument("--output")
    a = ap.parse_args()

    report = battery()
    print(f"VB mechanism battery  [{VERSION}]")
    for r in report["rows"]:
        ran = "n/a" if r["controlsRun"] is None else f"{r['controlsFired']}/{r['controlsRun']}"
        print(f"  {'ok  ' if r['allListedControlsFired'] else 'FAIL'} {r['tool']:34s} "
              f"declared={r['controlsDeclared']:3d}  fired={ran}")
    print(f"  {report['toolsRun']} tools, {report['controlsDeclaredTotal']} controls declared "
          f"(derived, never pinned)")

    ok = report["allListedControlsFired"]
    if a.prove_red:
        pr = prove_red()
        report["proveRed"] = pr
        print(f"\n  control on the battery itself:")
        print(f"    planted: {pr['planted']}")
        print(f"    mutation applied: {pr['mutationApplied']}  "
              f"broken tool exit={pr['brokenToolExitCode']}  "
              f"battery reds: {pr['batteryReds']}")
        ok = ok and pr["batteryReds"]

    if a.output:
        out = ROOT / a.output if not Path(a.output).is_absolute() else Path(a.output)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(report, indent=1) + "\n", encoding="utf-8")
    print("\nPASS" if ok else "\nMEASUREMENT INVALID")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
