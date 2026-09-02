#!/usr/bin/env python3
"""H12-4 firing control: the sweep must RED on a record with no attribution.

ORDER VB-RUN13 H12-4: "the two gates emitting unattributable records gain the
attribution field the sweep keys on (Shape A -- additive, no assertion removed),
each with a firing control (strip the field in a scratch record -> sweep must
RED). The sweep is not hand-patched."

The fix is only worth anything if its absence is detectable. So this plants a
scratch record in the evidence tree twice -- once as the gates now emit it, once
with "file" and "subject" removed -- and requires the stale-evidence sweep to be
clean on the first and to name the file on the second. The scratch record is
removed either way.

Usage: attribution_control.py [--output <report.json>]
"""
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SCRATCH = ROOT / "_sownb/vb/evidence/run13/attribution_control_scratch.json"

RECORD = {
    "gate": "g16-v2-frozen",
    "family": "BUILD Humanities",
    "candidate": "Humanities_Teesside/BUILD_W1-W8_2026-27/BUILD_HUM_W4_Then_And_Now.html",
    "frozenRowCount": 1,
    "passed": 1,
    "failed": 0,
    "firingControl": {"fired": True},
    "status": "PASS",
    "file": "Humanities_Teesside/BUILD_W1-W8_2026-27/BUILD_HUM_W4_Then_And_Now.html",
    "subject": "attribution control scratch record; deleted by the tool that wrote it",
}


def sweep_names_scratch() -> tuple[bool, str]:
    # The sweep enumerates with `git ls-files`, so it reads TRACKED files only.
    # An untracked scratch record is invisible to it, and a control that plants
    # one and sees nothing has proved nothing -- which is exactly what the first
    # version of this control did, and it reported the fix as unproven rather
    # than claiming a pass it had not earned.
    subprocess.run(["git", "add", "-N", str(SCRATCH.relative_to(ROOT))], cwd=ROOT, capture_output=True)
    run = subprocess.run(["node", "tools/stale_evidence_sweep.mjs"], cwd=ROOT,
                         capture_output=True, text=True)
    out = run.stdout + run.stderr
    # Only the INCONCLUSIVE block counts. The sweep names every evidence file it
    # reads in its normal reporting, so "the output mentions the scratch file" is
    # true whether the fix works or not -- the first version of this control used
    # that test and called a healthy record a failure.
    lines = out.split("\n")
    try:
        start = next(i for i, l in enumerate(lines) if l.startswith("[INCONCLUSIVE]"))
    except StopIteration:
        return False, out
    block = "\n".join(lines[start:start + 40])
    return SCRATCH.name in block, out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output")
    args = ap.parse_args()

    results = {}
    try:
        SCRATCH.parent.mkdir(parents=True, exist_ok=True)
        SCRATCH.write_text(json.dumps(RECORD, indent=1) + "\n", encoding="utf-8")
        fired_with, _ = sweep_names_scratch()
        results["withAttribution"] = {"mustFire": False, "fired": fired_with, "ok": not fired_with}

        stripped = {k: v for k, v in RECORD.items() if k not in ("file", "subject")}
        SCRATCH.write_text(json.dumps(stripped, indent=1) + "\n", encoding="utf-8")
        fired_without, out = sweep_names_scratch()
        results["withoutAttribution"] = {"mustFire": True, "fired": fired_without, "ok": fired_without}
        lines = out.split("\n")
        start = next((i for i, l in enumerate(lines) if l.startswith("[INCONCLUSIVE]")), None)
        results["whatTheSweepSaid"] = next(
            (l.strip() for l in (lines[start:start + 40] if start is not None else []) if SCRATCH.name in l), "")
    finally:
        subprocess.run(["git", "rm", "-q", "--cached", "--force", str(SCRATCH.relative_to(ROOT))],
                       cwd=ROOT, capture_output=True)
        SCRATCH.unlink(missing_ok=True)

    report = {
        "file": "_sownb/vb/tools/attribution_control.py",
        "subject": ("ORDER VB-RUN13 H12-4 firing control: a gate record carrying file and subject passes the "
                    "stale-evidence sweep, and the same record with those two fields removed does not"),
        "gatesFixedAtSource": ["_sownb/feb/tools/g15_guidance_hidden.js", "_sownb/vb/tools/g16_v2.py"],
        "shape": "Shape A, additive: two fields added to each record, no assertion, measurement or control removed",
        "controls": results,
        "status": "PASS" if all(v["ok"] for v in results.values() if isinstance(v, dict)) else "RED",
    }
    if args.output:
        out_path = ROOT / args.output if not Path(args.output).is_absolute() else Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(report, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")

    for name, v in results.items():
        if isinstance(v, dict):
            print(f"  {name:22s} mustFire={v['mustFire']!s:5s} fired={v['fired']!s:5s} {'ok' if v['ok'] else 'FAILED'}")
    print(report["status"])
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
