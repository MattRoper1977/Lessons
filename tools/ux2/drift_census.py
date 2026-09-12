#!/usr/bin/env python3
"""PIN1 §2.2: report UX2's existing proof outcomes; never infer pin coverage.

Exit 0: all nine proof steps and all three jobs succeeded.
Exit 1: complete evidence contains a failure.
Exit 2: evidence/context is missing, cancelled, skipped, malformed or unknown.
Failure details remain in the original jobs; a failed job alone does not prove
file drift (an execution/environment failure can also make it fail).
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re

PROOFS = {
    "catalogue-contract": ("schema", "tags", "contract", "companions"),
    "derived-data": ("spine", "sizes"),
    "hub-and-subject": ("hub", "chips", "dom"),
}


def census(needs, context):
    issues, rows = [], []
    if not isinstance(needs, dict):
        needs = {}
        issues.append("Needs payload is not an object")
    if set(needs) != set(PROOFS):
        issues.append("Dependency population differs from the three UX2 jobs")
    for key in ("repository", "sha", "event", "run_id", "run_attempt"):
        if not isinstance(context.get(key), str) or not context[key]:
            issues.append(f"Missing context: {key}")
    if not re.fullmatch(r"[0-9a-f]{40}", context.get("sha", "")):
        issues.append("Source SHA is not a full commit SHA")
    failures = []
    for job, proofs in PROOFS.items():
        value = needs.get(job)
        value = value if isinstance(value, dict) else {}
        result = value.get("result")
        if result == "failure":
            failures.append(f"{job}: job failed; inspect its log")
        elif result != "success":
            issues.append(f"{job}: job result missing or incomplete")
        outputs = value.get("outputs")
        outputs = outputs if isinstance(outputs, dict) else {}
        if set(outputs) != set(proofs):
            issues.append(f"{job}: proof output population differs")
        for proof in proofs:
            outcome = outputs.get(proof)
            status = {"success": "PASS", "failure": "FAIL"}.get(outcome, "UNMEASURED")
            rows.append({"job": job, "proof": proof, "status": status})
            if status == "FAIL":
                failures.append(f"{job}/{proof}: assertion or execution failed; inspect its log")
            elif status == "UNMEASURED":
                issues.append(f"{job}/{proof}: proof did not supply a terminal outcome")
    verdict, code = ("UNMEASURED", 2) if issues else ("FAIL", 1) if failures else ("PASS", 0)
    return {
        "schema": "mbm-ux2-drift-census-v1",
        "measured_at": datetime.now(timezone.utc).isoformat(),
        "context": context,
        "scope": "UX2 existing assertions only; file-pin coverage is not asserted",
        "verdict": verdict,
        "proofs": rows,
        "failures": failures,
        "unmeasured": issues,
    }, code


def markdown(report):
    ctx = report["context"]
    lines = [f"# UX2 drift census: {report['verdict']}", "", report["scope"], "",
             f"Commit: `{ctx.get('sha', '')}`; event: `{ctx.get('event', '')}`; "
             f"run: `{ctx.get('run_id', '')}`; attempt: `{ctx.get('run_attempt', '')}`.", "",
             "PASS means the nine existing UX2 proofs succeeded at this commit. "
             "FAIL includes assertion or execution failures; original job logs supply the diagnosis. "
             "UNMEASURED is never a pass. This is not a pinned-file trigger proof.", "",
             "| Job | Proof | Result |", "|---|---|---|"]
    lines += [f"| {r['job']} | {r['proof']} | {r['status']} |" for r in report["proofs"]]
    lines += ["", *[f"- {item}" for item in report["failures"] + report["unmeasured"]], ""]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    try:
        needs = json.loads(os.environ.get("UX2_NEEDS", ""))
    except (ValueError, TypeError):
        needs = None
    context = {k: os.environ.get(v, "") for k, v in {
        "repository": "GITHUB_REPOSITORY", "sha": "GITHUB_SHA", "event": "GITHUB_EVENT_NAME",
        "run_id": "GITHUB_RUN_ID", "run_attempt": "GITHUB_RUN_ATTEMPT",
    }.items()}
    report, code = census(needs, context)
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "census.json").write_text(json.dumps(report, indent=2) + "\n", "utf-8")
    rendered = markdown(report)
    (args.out / "census.md").write_text(rendered, "utf-8")
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as stream:
            stream.write(rendered)
    print(rendered)
    return code


if __name__ == "__main__":
    raise SystemExit(main())
