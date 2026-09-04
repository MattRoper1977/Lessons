#!/usr/bin/env python3
"""g29 PLAN BINDING — a deck claims its own plan's cells, exactly.

WHY g28 IS NOT ENOUGH, AND WHY THIS IS A REPAIR RATHER THAN A NEW GATE
---------------------------------------------------------------------
g28 asks whether a cited cell EXISTS on a real sheet. It cannot ask whether THIS
deck is the one that teaches it. Twice in this campaign a deck would have shipped
carrying another plan's cells and passed every gate in the stack:

  * the batch-2 driver keyed decks on `family+week`, and two LAUNCH ASDAN plans
    share week 1, so the second deck would silently have received the first's
    cells;
  * an authoring run was launched from a task list typed out of a console print,
    in which five of twelve cell sets and eight of twelve OUTCOMES were wrong.

Both are the same failure: a rendering of the plan treated as the plan. A cell
claimed by the wrong deck is a coverage lie — the census counts the cell as
taught, and nobody teaches it.

THE BINDING. A plan's identity is DERIVED FROM ITS OWN CONTENT, not from its
position in a file and not from a name someone typed:

    planId = sha256(family | ruledWeek | sorted(cells))[:12]

so it survives the targets file being regenerated or reordered, and two plans
that share a family and a week still have different ids. Every authored deck
records its planId, and this gate asserts the deck's claimed cells are EXACTLY
the plan's: not a superset (stealing another plan's cells) and not a subset
(a silent under-claim that leaves a cell open while looking covered).

Usage:
  g29_plan_binding.py <deck.html> [...]        [--targets F] [--output r.json]
  g29_plan_binding.py --scope authored         every deck carrying a planId
  g29_plan_binding.py --list-controls | --self-test
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
VERSION = "g29-v1.0.0-plan-binding"
TARGETS = ROOT / "tools/easter/EASTER_TARGETS.json"
CFG = re.compile(r'id=["\']lesson-config["\'][^>]*>(.*?)</script>', re.S)


def plan_id(plan: dict) -> str:
    """Derived from the plan's own content, so it cannot drift with the file."""
    key = "|".join([str(plan.get("family", "")), str(plan.get("ruledWeek", "")),
                    "|".join(sorted(plan.get("cells", [])))])
    return hashlib.sha256(key.encode("utf-8")).hexdigest()[:12]


def load_plans(path: Path = TARGETS) -> tuple[dict, str]:
    raw = path.read_bytes()
    plans = json.loads(raw.decode("utf-8"))["plans"]
    return ({plan_id(p): p for p in plans},
            hashlib.sha256(raw).hexdigest())


def deck_config(path: Path) -> dict | None:
    m = CFG.search(Path(path).read_text(encoding="utf-8"))
    if not m:
        return None
    try:
        return json.loads(m.group(1))
    except Exception:
        return None


def judge(path: Path, by_id: dict) -> dict:
    cfg = deck_config(path) or {}
    pid = cfg.get("planId")
    claimed = sorted(cfg.get("cells", []))
    rec = {"file": str(path), "planId": pid, "claimedCells": claimed}
    if not pid:
        rec.update({"status": "SKIP", "reason": "deck records no planId; not an "
                                                "authored deck of this campaign"})
        return rec
    plan = by_id.get(pid)
    if plan is None:
        rec.update({"status": "RED", "reason": f"planId {pid} matches no plan in the "
                                               "targets file"})
        return rec
    expected = sorted(plan["cells"])
    extra = [c for c in claimed if c not in expected]
    missing = [c for c in expected if c not in claimed]
    rec.update({
        "family": plan["family"], "ruledWeek": plan["ruledWeek"],
        "expectedCells": expected, "extraCells": extra, "missingCells": missing,
        "outcomesMatch": cfg.get("outcomes") == plan.get("outcomes"),
        "status": "PASS" if not extra and not missing
                  and cfg.get("outcomes") == plan.get("outcomes") else "RED",
    })
    if extra:
        rec["reason"] = f"claims {len(extra)} cell(s) belonging to another plan"
    elif missing:
        rec["reason"] = f"under-claims {len(missing)} cell(s) its plan requires"
    elif not rec["outcomesMatch"]:
        rec["reason"] = "outcomes do not match the plan's"
    return rec


# --------------------------------------------------------------------------
# Controls. All three must fire (A3N-2 §2b) or the measurement is invalid.
# --------------------------------------------------------------------------

CONTROL_IDS = [
    "a-deck-claiming-another-plans-cells-reds",
    "a-deck-claiming-a-subset-reds",
    "two-correctly-bound-decks-in-one-family-week-both-pass",
    "the-plan-id-survives-the-targets-file-being-reordered",
    "a-deck-with-no-planId-is-skipped-not-silently-passed",
]

_P1 = {"family": "F ASDAN", "ruledWeek": 1, "cells": ["'S'!C1", "'S'!C2"],
       "outcomes": ["o1", "o2"]}
_P2 = {"family": "F ASDAN", "ruledWeek": 1, "cells": ["'S'!C9"], "outcomes": ["o9"]}


def _deck(cells, outcomes, pid) -> str:
    cfg = json.dumps({"id": "X", "cells": cells, "outcomes": outcomes, "planId": pid})
    return ('<!doctype html><html><head><script id="lesson-config" '
            f'type="application/json">{cfg}</script></head><body></body></html>')


def _tmp(src: str) -> Path:
    fh = tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8")
    fh.write(src); fh.close()
    return Path(fh.name)


def controls() -> list[dict]:
    out = []

    def rec(cid, description, expected, observed):
        out.append({"id": cid, "description": description, "expected": expected,
                    "observed": observed, "fired": expected == observed})

    by_id = {plan_id(_P1): _P1, plan_id(_P2): _P2}

    steal = _tmp(_deck(["'S'!C1", "'S'!C2", "'S'!C9"], ["o1", "o2"], plan_id(_P1)))
    r = judge(steal, by_id)
    rec("a-deck-claiming-another-plans-cells-reds",
        "a cell claimed by the wrong deck is a coverage lie: the census counts it "
        "taught and nobody teaches it",
        ("RED", ["'S'!C9"]), (r["status"], r["extraCells"]))

    subset = _tmp(_deck(["'S'!C1"], ["o1", "o2"], plan_id(_P1)))
    r2 = judge(subset, by_id)
    rec("a-deck-claiming-a-subset-reds",
        "an under-claim leaves a cell open while the deck looks covered, which is "
        "the same lie told quietly",
        ("RED", ["'S'!C2"]), (r2["status"], r2["missingCells"]))

    d1 = _tmp(_deck(_P1["cells"], _P1["outcomes"], plan_id(_P1)))
    d2 = _tmp(_deck(_P2["cells"], _P2["outcomes"], plan_id(_P2)))
    rec("two-correctly-bound-decks-in-one-family-week-both-pass",
        "two plans sharing a family and a week are the case family+week keying got "
        "wrong; correctly bound, both must pass",
        ("PASS", "PASS"), (judge(d1, by_id)["status"], judge(d2, by_id)["status"]))

    rec("the-plan-id-survives-the-targets-file-being-reordered",
        "the id is derived from the plan's content, so regenerating or reordering "
        "the targets file cannot rebind a deck",
        plan_id(_P1), plan_id(dict(reversed(list(_P1.items())))))

    nopid = _tmp('<!doctype html><html><head><script id="lesson-config" '
                 'type="application/json">{"cells":["\'S\'!C1"]}</script>'
                 "</head><body></body></html>")
    r5 = judge(nopid, by_id)
    rec("a-deck-with-no-planId-is-skipped-not-silently-passed",
        "the estate's older decks predate this binding; they are SKIP, never PASS, "
        "so the tally cannot flatter itself",
        "SKIP", r5["status"])

    for f in (steal, subset, d1, d2, nopid):
        f.unlink(missing_ok=True)
    return out


def self_test() -> dict:
    res = controls()
    ids = [r["id"] for r in res]
    missing = [c for c in CONTROL_IDS if c not in ids]
    extra = [c for c in ids if c not in CONTROL_IDS]
    return {"tool": "g29_plan_binding", "toolVersion": VERSION,
            "file": "_sownb/vb/tools/g29_plan_binding.py",
            "controlsDeclared": len(CONTROL_IDS), "controlsRun": len(res),
            "controlsFired": sum(1 for r in res if r["fired"]),
            "missingControls": missing, "undeclaredControls": extra,
            "allListedControlsFired": not missing and not extra and all(r["fired"] for r in res),
            "controls": res}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("decks", nargs="*")
    ap.add_argument("--scope", choices=("authored",))
    ap.add_argument("--targets", default=str(TARGETS))
    ap.add_argument("--output")
    ap.add_argument("--list-controls", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()
    if a.list_controls:
        print("\n".join(CONTROL_IDS)); return 0
    if a.self_test:
        rep = self_test()
        print(f"g29 self-test  [{VERSION}]")
        for r in rep["controls"]:
            print(f"  {'ok  ' if r['fired'] else 'FAIL'} {r['id']:56s} "
                  f"expected={str(r['expected'])[:34]} observed={str(r['observed'])[:34]}")
        print(f"{rep['controlsFired']}/{rep['controlsRun']} controls fired")
        print("PASS" if rep["allListedControlsFired"] else "MEASUREMENT INVALID")
        return 0 if rep["allListedControlsFired"] else 1

    by_id, digest = load_plans(Path(a.targets))
    paths = [Path(d) for d in a.decks]
    if a.scope == "authored":
        paths = []
        for f in sorted(ROOT.rglob("*.html")):
            rel = f.relative_to(ROOT)
            if rel.parts and rel.parts[0] in ("Site", "Games", "Apps"):
                continue
            try:
                if '"planId"' in f.read_text(encoding="utf-8"):
                    paths.append(f)
            except Exception:
                continue
    recs = [judge(p, by_id) for p in paths]
    reds = [r for r in recs if r["status"] == "RED"]
    for r in recs:
        name = Path(r["file"]).name[:56]
        print(f"  {r['status']:4s} {name:56s} {r.get('reason','')}")
    print(f"\n{len(recs)} deck(s): {sum(1 for r in recs if r['status']=='PASS')} PASS, "
          f"{len(reds)} RED, {sum(1 for r in recs if r['status']=='SKIP')} SKIP")
    print(f"targets sha256 {digest[:16]}  [{VERSION}]")
    if a.output:
        o = Path(a.output); o = o if o.is_absolute() else ROOT / o
        o.parent.mkdir(parents=True, exist_ok=True)
        o.write_text(json.dumps({"gate": "g29-plan-binding", "toolVersion": VERSION,
                                 "file": "_sownb/vb/tools/g29_plan_binding.py",
                                 "targetsSha256": digest, "decks": len(recs),
                                 "red": len(reds), "rows": recs}, indent=1) + "\n",
                     encoding="utf-8")
    return 0 if not reds else 1


if __name__ == "__main__":
    raise SystemExit(main())
