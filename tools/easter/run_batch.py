#!/usr/bin/env python3
"""Author and gate one batch, from files with recorded digests.

Every input is a FILE: the target list, the donor map, the content specs and
the plans. A3N-2 §2c -- a run whose inputs cannot be traced to a digest refuses
to start. Nothing here is typed from a console print, and the plan is addressed
by index, never by family and week.

Each deck goes through prove_chassis, which runs nine gates on the authored deck
AND on its donor, so a red the estate already carries is reported as
PRE-EXISTING and only a red the donor does not carry fails the deck.

    python3 tools/easter/run_batch.py --targets tools/easter/BATCH3_TARGETS.json \
        --donors tools/easter/BATCH3_DONORS.json --content-dir tools/easter/content \
        [--only 8,9,17] [--output <json>]
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path

VERSION = "run-batch-v1.0.0"
ROOT = Path(__file__).resolve().parents[2]


def _rel(p) -> str:
    """A path as this repository names it.

    `spec` is a subject in the record, and the estate's stale-evidence sweep
    resolves subjects beside the evidence, in the evidence directory, or at the
    repository root -- never against an absolute container path. `file` was
    fixed for exactly this reason during batch 3; `spec` is the same decision
    made in the same file and missed. Fourth tool in this campaign to make it.
    """
    from pathlib import Path as _P
    try:
        return str(_P(p).resolve().relative_to(ROOT))
    except ValueError:
        return str(p)


def _load(name, rel):
    spec = importlib.util.spec_from_file_location(name, ROOT / rel)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


pc = _load("prove_chassis", "tools/easter/prove_chassis.py")


def digest(path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _require(label, path) -> dict:
    f = Path(path)
    if not f.is_file():
        raise SystemExit(f"PROVENANCE REFUSAL: {label} input {str(path)!r} is not a "
                         f"readable file. Every input must be traceable to a digest.")
    return {"path": str(f), "sha256": digest(f)}


def spec_for(content_dir: Path, row: dict) -> Path:
    """Read from the TARGET ROW, never recomputed here.

    LANE_SUBJECT_Wn is not unique -- two cover-taught LAUNCH ASDAN plans share
    week 5 -- so the name is derived once, with collisions disambiguated by the
    plan's own id, in the tool that writes the target list. Recomputing it here
    is how the second of two colliding plans gets handed the first's content.
    """
    if not row.get("spec"):
        raise SystemExit(f"TARGET ROW HAS NO SPEC NAME: plan {row['planIndex']} "
                         f"({row['family']} W{row['week']}). Regenerate the target "
                         f"list with build_batch3_targets.py.")
    return Path(content_dir) / row["spec"]


def run(targets: Path, donors: Path, content_dir: Path, only: set | None) -> dict:
    inputs = {"targets": _require("targets", targets),
              "donors": _require("donors", donors)}
    tdoc = json.loads(Path(targets).read_text())
    ddoc = json.loads(Path(donors).read_text())["families"]

    if tdoc.get("plansFrom") == "row":
        try:
            pc.ad._pi.validate_award_targets(tdoc)
        except (ValueError, OSError, KeyError) as exc:
            raise SystemExit(str(exc))
    rows, results = tdoc["batch"], []
    for row in rows:
        if only is not None and row["planIndex"] not in only:
            continue
        spec = spec_for(content_dir, row)
        fam = ddoc.get(row["family"])
        if fam is None:
            results.append({**row, "file": row["route"], "verdict": "NO DONOR",
                            "why": f"{row['family']} has no entry in the donor map"})
            continue
        if not spec.is_file():
            results.append({**row, "file": row["route"], "verdict": "NO SPEC",
                            "spec": _rel(spec),
                            "why": "no content spec has been written for this plan yet"})
            continue
        out = ROOT / row["route"]
        # WHERE THE PLAN COMES FROM. By default a plan is a row of
        # EASTER_TARGETS.json addressed by index, which is every plan this
        # campaign had authored until Bronze. A target list may instead declare
        # `plansFrom: "row"` -- the Bronze strand does, because AAE-H7 ruled it
        # claims no workbook cell and so has no row to index. The row IS the
        # plan then, and the file it was derived from is what gets digested.
        if tdoc.get("plansFrom") == "row":
            plan = {"family": row["family"], "ruledWeek": row["week"],
                    "cells": row.get("cells", []), "outcomes": row["outcomes"],
                    "title": row.get("title", ""), "subject": row.get("subject", "")}
            if row.get("artsAward"):
                plan["artsAward"] = row["artsAward"]
            rec = pc.prove(ROOT / fam["donor"], row["planIndex"], spec,
                           ROOT / fam["reference"], probe=out, plan=plan,
                           plan_source=ROOT / tdoc["derivedFrom"]["path"])
        else:
            rec = pc.prove(ROOT / fam["donor"], row["planIndex"], spec,
                           ROOT / fam["reference"], probe=out)
        # `file` names the subject each row reports on, in the form the estate's
        # stale-evidence sweep reads structurally. Without it the sweep falls
        # back to reading the text and reports every bare "verdict": "PASS" row
        # as INCONCLUSIVE, which is exactly what it exists to do.
        results.append({**row, "file": row["route"],
                        "spec": _rel(spec), "donor": fam["donor"],
                        "verdict": rec["verdict"],
                        "inputs": rec["inputs"],
                        "regressions": rec["regressions"],
                        "preExisting": rec["preExisting"],
                        "words": rec["author"].get("contentWords"),
                        "leaked": rec["author"].get("donorSentencesLeaked"),
                        "gates": {k: v["verdict"] for k, v in rec["gates"].items()}})
    if not results:
        raise SystemExit("PROVENANCE REFUSAL: no target rows selected")
    built = [r for r in results if r["verdict"] in ("PASS", "RED")]
    return {"tool": VERSION, "inputs": inputs,
            "attempted": len(results),
            "built": len(built),
            "passed": sum(1 for r in built if r["verdict"] == "PASS"),
            "rows": results}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--targets", required=True)
    ap.add_argument("--donors", required=True)
    ap.add_argument("--content-dir", default=str(ROOT / "tools/easter/content"))
    ap.add_argument("--only", help="comma-separated plan indexes")
    ap.add_argument("--output")
    a = ap.parse_args()
    only = ({int(x) for x in a.only.split(",")} if a.only else None)
    doc = run(Path(a.targets), Path(a.donors), Path(a.content_dir), only)
    for r in doc["rows"]:
        tag = r["verdict"]
        extra = ""
        if tag in ("PASS", "RED"):
            extra = (f" {r['words']}w leaked={r['leaked']}"
                     + (f" REGRESSIONS={r['regressions']}" if r["regressions"] else ""))
        print(f"  {tag:9s} idx {r['planIndex']:>3} W{r['week']} {r['family']:18s}{extra}")
    print(f"{doc['passed']} of {doc['built']} built decks PASS "
          f"({doc['attempted']} attempted)")
    if a.output:
        Path(a.output).parent.mkdir(parents=True, exist_ok=True)
        Path(a.output).write_text(json.dumps(doc, indent=1, default=str) + "\n",
                                  encoding="utf-8")
    return 0 if doc["passed"] == doc["built"] == doc["attempted"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
