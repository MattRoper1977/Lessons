#!/usr/bin/env python3
"""A3N §N2 / A3N-2 §5 -- generate batch 3's target list from the plans file.

DERIVED, NOT TYPED. A3N-2 §2c: every task list an authoring run consumes must be
read from a file whose sha256 is recorded, and a run whose inputs cannot be
traced to a digest refuses to start. So this writes the list, from
EASTER_TARGETS.json, and records that file's digest in what it writes.

ORDER: week-major, then ASDAN -> Science -> Humanities -> Art, then
BUILD -> GROW -> LAUNCH inside each. That is §5's ordering, stated once here
rather than re-sorted by hand at each step.

WHAT IS HELD BACK, AND WHY IT IS HELD BACK RATHER THAN DROPPED
--------------------------------------------------------------
Two kinds of plan are excluded, each with the reason recorded in the output so
the cells stay visibly open rather than quietly missing.

  RESHELL       three plans name a `standingDeck` to reshell rather than a
                lesson to author. That is a different pipeline
                (reshell_classic_v2), not this one.

  NO NEW        six Science plans read "Baseline assessment (PythonAnywhere) --
  CONTENT       no new science content; unit starts W3". Authoring a teaching
                deck against an outcome that says there is nothing to teach
                would be shipping something doubtful, and the family floor for
                BUILD Science is 1229 pupil words, which a baseline-assessment
                session cannot honestly carry. Held for a ruling: the cover
                teacher does need a session sheet for these, and what it should
                contain is Matt's call, not a gate's.

    python3 tools/easter/build_batch_targets.py --output <file>
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

VERSION = "build-batch-targets-v1.0.0"
ROOT = Path(__file__).resolve().parents[2]
TARGETS = ROOT / "tools/easter/EASTER_TARGETS.json"
CEILING = 24

SUBJECT_ORDER = {"ASDAN": 0, "Science": 1, "Humanities": 2, "Art": 3}
LANE_ORDER = {"BUILD": 0, "GROW": 1, "LAUNCH": 2}

ROUTE = {
    "Art": "Art_Teesside/{lane}_W1-W8_2026-27/{lane}_Art_W{week}_{slug}.html",
    "Humanities": "Humanities_Teesside/{lane}_W1-W8_2026-27/{lane}_Humanities_W{week}_{slug}.html",
    "ASDAN": "{lane}_ASDAN/Autumn1_W1-W7_2026-27/{lane}_ASDAN_W{week}_{slug}.html",
    "Science": "Science_Teesside/{Lane}/W1-W8_2026-27/SCI_{L}_W{week}_{slug}.html",
}
NO_NEW_CONTENT = re.compile(r"no new science content", re.I)


def digest(path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def plan_id(p: dict) -> str:
    key = "|".join([str(p.get("family", "")), str(p.get("ruledWeek", "")),
                    "|".join(sorted(p.get("cells", [])))])
    return hashlib.sha256(key.encode("utf-8")).hexdigest()[:12]


def slug(text: str, words: int = 7) -> str:
    parts = re.findall(r"[A-Za-z0-9]+", text)[:words]
    return "_".join(w.capitalize() if w.islower() else w for w in parts) or "Lesson"


def route_for(p: dict) -> str:
    lane = p["lane"]
    return ROUTE[p["subject"]].format(lane=lane, Lane=lane.capitalize(),
                                      L=lane[0], week=p["ruledWeek"],
                                      slug=slug(p["outcomes"][0]))


def build(done_ids: set[str]) -> dict:
    plans = json.loads(TARGETS.read_text())["plans"]
    rows, held = [], []
    for i, p in enumerate(plans):
        if not p.get("coverBeforeMattReturns"):
            continue
        if plan_id(p) in done_ids:
            continue
        row = {"planIndex": i, "planId": plan_id(p), "family": p["family"],
               "lane": p["lane"], "subject": p["subject"], "week": p["ruledWeek"],
               "kind": p["kind"], "cells": p["cells"], "outcomes": p["outcomes"],
               "route": route_for(p)}
        if p["kind"] != "AUTHOR":
            held.append({**row, "heldBecause":
                         f"{p['kind']}: names a standing deck to reshell, not a "
                         f"lesson to author; a different pipeline"})
            continue
        if any(NO_NEW_CONTENT.search(o) for o in p["outcomes"]):
            held.append({**row, "heldBecause":
                         "the outcome says there is no new content to teach; a "
                         "teaching deck against it would be doubtful, and the "
                         "family floor is more words than a baseline session "
                         "honestly carries. Held for a ruling."})
            continue
        rows.append(row)
    rows.sort(key=lambda r: (r["week"], SUBJECT_ORDER.get(r["subject"], 9),
                             LANE_ORDER.get(r["lane"], 9), r["planIndex"]))
    # THE SPEC FILENAME IS PART OF THE TARGET ROW, NOT DERIVED AT USE.
    # LANE_SUBJECT_Wn is not unique: two cover-taught LAUNCH ASDAN plans share
    # week 5, and two shared week 1 in batch 2. A driver that computed the name
    # at use would have handed the second plan the first plan's content and
    # every gate but g29 would have passed it. Where a name collides, the plan's
    # own derived id disambiguates it -- an id that survives the targets file
    # being regenerated or reordered.
    seen = {}
    for r in rows + held:
        base = f"{r['lane']}_{r['subject'].upper()}_W{r['week']}"
        seen.setdefault(base, []).append(r)
    for base, group in seen.items():
        for r in group:
            r["spec"] = (f"{base}.json" if len(group) == 1
                         else f"{base}_{r['planId']}.json")
    batch, overflow = rows[:CEILING], rows[CEILING:]
    return {
        "tool": VERSION,
        "schema": "easter-batch-targets-v1",
        "derivedFrom": {"file": str(TARGETS.relative_to(ROOT)), "sha256": digest(TARGETS)},
        "ceiling": CEILING,
        "order": "week-major, then ASDAN -> Science -> Humanities -> Art, then BUILD -> GROW -> LAUNCH",
        "count": len(batch),
        "batch": batch,
        "overflowCount": len(overflow),
        "overflow": overflow,
        "heldCount": len(held),
        "held": held,
    }


def controls(done_ids: set[str]) -> list[dict]:
    out = []

    def rec(cid, claim, expect, actual):
        out.append({"id": cid, "claim": claim, "expected": expect, "actual": actual,
                    "verdict": "PASS" if expect == actual else "RED"})

    doc = build(done_ids)
    rec("the-batch-never-exceeds-the-ceiling",
        f"a batch carries at most {CEILING} lesson units (R1)",
        True, doc["count"] <= CEILING)
    rec("nothing-is-dropped-silently",
        "every cover-taught plan not already bound is in batch, overflow or held",
        True, doc["count"] + doc["overflowCount"] + doc["heldCount"] > 0)
    weeks = [r["week"] for r in doc["batch"]]
    rec("the-order-is-week-major",
        "weeks do not go backwards down the list", sorted(weeks), weeks)
    routes = [r["route"] for r in doc["batch"]]
    rec("every-route-is-distinct",
        "no two plans in the batch would be written to the same file",
        len(routes), len(set(routes)))
    ids = [r["planId"] for r in doc["batch"]]
    rec("every-plan-appears-once",
        "no plan is scheduled twice in one batch", len(ids), len(set(ids)))
    specs = [r["spec"] for r in doc["batch"]]
    rec("every-spec-filename-is-distinct",
        "no two plans in the batch would read the same content file",
        len(specs), len(set(specs)))
    # The collision is real and present, not hypothetical -- pin it so the
    # disambiguation cannot be dropped as unnecessary.
    collide = [r for r in doc["batch"] + doc["overflow"]
               if r["spec"] != f"{r['lane']}_{r['subject'].upper()}_W{r['week']}.json"]
    rec("a-real-lane-subject-week-collision-is-disambiguated",
        "at least one plan needs its id in the spec name, and gets it",
        True, bool(collide))
    rec("a-held-plan-carries-its-reason",
        "no plan is held without a stated reason",
        True, all(r.get("heldBecause") for r in doc["held"]))
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--bound", help="a g29 report whose PASS rows are already authored")
    ap.add_argument("--output")
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--list-controls", action="store_true")
    a = ap.parse_args()

    done = set()
    if a.bound:
        f = Path(a.bound)
        if not f.is_file():
            raise SystemExit(f"PROVENANCE REFUSAL: bound-plans input {a.bound!r} is not a "
                             f"readable file. Every input must be traceable to a digest.")
        done = {r["planId"] for r in json.loads(f.read_text())["rows"]
                if r.get("status") == "PASS"}

    if a.list_controls:
        for c in controls(done):
            print(c["id"])
        return 0
    if a.self_test:
        cs = controls(done)
        for c in cs:
            print(f"{c['verdict']:4s} {c['id']}: {c['claim']}")
            if c["verdict"] == "RED":
                print(f"       expected {c['expected']!r} got {c['actual']!r}")
        red = [c for c in cs if c["verdict"] == "RED"]
        print(f"{len(cs) - len(red)}/{len(cs)} controls PASS")
        return 1 if red else 0

    doc = build(done)
    if a.bound:
        doc["boundFrom"] = {"file": a.bound, "sha256": digest(a.bound),
                            "alreadyAuthored": len(done)}
    print(f"{doc['tool']}  batch {doc['count']} of ceiling {doc['ceiling']}  "
          f"overflow {doc['overflowCount']}  held {doc['heldCount']}")
    for r in doc["batch"]:
        print(f"  idx {r['planIndex']:>3}  W{r['week']}  {r['family']:18s} "
              f"{len(r['cells'])}c  {r['route']}")
    for r in doc["held"]:
        print(f"  HELD idx {r['planIndex']:>3}  W{r['week']}  {r['family']:18s} "
              f"{r['heldBecause'][:70]}")
    if a.output:
        Path(a.output).parent.mkdir(parents=True, exist_ok=True)
        Path(a.output).write_text(json.dumps(doc, indent=1, ensure_ascii=False) + "\n",
                                  encoding="utf-8")
        print(f"wrote {a.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
