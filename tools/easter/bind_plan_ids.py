#!/usr/bin/env python3
"""Backfill planId onto decks authored before the binding existed (A3N-2 §2d).

The binding is not written from a list of which deck I think matches which plan
— that would be the same mistake again. It is DERIVED: a deck is bound only if
exactly one plan has exactly its cells. Zero matches or two matches is reported
and nothing is written, because an ambiguous binding is worse than none.
"""
from __future__ import annotations
import argparse, hashlib, json, re, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
VERSION = "bind-plan-ids-v1.0.0"
CFG = re.compile(r'(<script[^>]*id=["\']lesson-config["\'][^>]*>)(.*?)(</script>)', re.S)


def plan_id(plan: dict) -> str:
    key = "|".join([str(plan.get("family", "")), str(plan.get("ruledWeek", "")),
                    "|".join(sorted(plan.get("cells", [])))])
    return hashlib.sha256(key.encode("utf-8")).hexdigest()[:12]


def bind(path: Path, plans: list, write: bool = True) -> dict:
    raw = path.read_text(encoding="utf-8")
    m = CFG.search(raw)
    if not m:
        return {"file": str(path), "status": "SKIP", "reason": "no lesson-config"}
    cfg = json.loads(m.group(2))
    if cfg.get("planId"):
        return {"file": str(path), "status": "ALREADY", "planId": cfg["planId"]}
    cells = sorted(cfg.get("cells", []))
    if not cells:
        return {"file": str(path), "status": "SKIP", "reason": "deck claims no cells"}
    hits = [p for p in plans if sorted(p.get("cells", [])) == cells]
    if len(hits) != 1:
        return {"file": str(path), "status": "AMBIGUOUS" if hits else "UNMATCHED",
                "matches": len(hits), "cells": cells,
                "reason": "an ambiguous binding is worse than none; nothing written"}
    plan = hits[0]
    pid = plan_id(plan)
    outcomes_match = cfg.get("outcomes") == plan.get("outcomes")
    if write:
        cfg["planId"] = pid
        raw = raw[:m.start(2)] + json.dumps(cfg, ensure_ascii=False) + raw[m.end(2):]
        path.write_text(raw, encoding="utf-8")
    return {"file": str(path), "status": "BOUND", "planId": pid,
            "family": plan["family"], "ruledWeek": plan["ruledWeek"],
            "outcomesMatch": outcomes_match, "cells": cells}


CONTROL_IDS = [
    "a-deck-whose-cells-match-exactly-one-plan-is-bound",
    "a-deck-matching-no-plan-is-left-unbound",
    "a-deck-matching-two-plans-is-left-unbound",
]

_PL = [{"family": "F", "ruledWeek": 1, "cells": ["'S'!C1"], "outcomes": ["a"]},
       {"family": "F", "ruledWeek": 2, "cells": ["'S'!C2"], "outcomes": ["b"]},
       {"family": "G", "ruledWeek": 3, "cells": ["'S'!C2"], "outcomes": ["b"]}]


def _deck(cells):
    cfg = json.dumps({"id": "X", "cells": cells, "outcomes": ["a"]})
    return ('<!doctype html><html><head><script id="lesson-config" '
            f'type="application/json">{cfg}</script></head><body></body></html>')


def controls():
    out = []
    def rec(cid, d, e, o):
        out.append({"id": cid, "description": d, "expected": e, "observed": o, "fired": e == o})
    def tmp(src):
        fh = tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8")
        fh.write(src); fh.close(); return Path(fh.name)
    a = tmp(_deck(["'S'!C1"]))
    rec("a-deck-whose-cells-match-exactly-one-plan-is-bound",
        "the binding is derived from the cells, never from a list of which deck I "
        "think matches which plan",
        ("BOUND", plan_id(_PL[0])), (lambda r: (r["status"], r.get("planId")))(bind(a, _PL)))
    b = tmp(_deck(["'S'!C7"]))
    rec("a-deck-matching-no-plan-is-left-unbound",
        "an unmatched deck is reported, never guessed at",
        "UNMATCHED", bind(b, _PL)["status"])
    c = tmp(_deck(["'S'!C2"]))
    rec("a-deck-matching-two-plans-is-left-unbound",
        "two plans share these cells; binding either would be a coin toss",
        "AMBIGUOUS", bind(c, _PL)["status"])
    for f in (a, b, c):
        f.unlink(missing_ok=True)
    return out


def self_test():
    res = controls(); ids = [r["id"] for r in res]
    missing = [x for x in CONTROL_IDS if x not in ids]
    return {"tool": "bind_plan_ids", "toolVersion": VERSION,
            "file": "tools/easter/bind_plan_ids.py",
            "controlsDeclared": len(CONTROL_IDS), "controlsRun": len(res),
            "controlsFired": sum(1 for r in res if r["fired"]), "missingControls": missing,
            "allListedControlsFired": not missing and all(r["fired"] for r in res),
            "controls": res}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("decks", nargs="*")
    ap.add_argument("--plans", default=str(ROOT / "tools/easter/EASTER_TARGETS.json"))
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--output"); ap.add_argument("--list-controls", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()
    if a.list_controls:
        print("\n".join(CONTROL_IDS)); raise SystemExit(0)
    if a.self_test:
        rep = self_test()
        print(f"bind_plan_ids self-test  [{VERSION}]")
        for r in rep["controls"]:
            print(f"  {'ok  ' if r['fired'] else 'FAIL'} {r['id']:50s} "
                  f"expected={r['expected']} observed={r['observed']}")
        print(f"{rep['controlsFired']}/{rep['controlsRun']} controls fired")
        print("PASS" if rep["allListedControlsFired"] else "MEASUREMENT INVALID")
        raise SystemExit(0 if rep["allListedControlsFired"] else 1)
    pf = Path(a.plans)
    plans = json.loads(pf.read_text())["plans"]
    print(f"  plans {hashlib.sha256(pf.read_bytes()).hexdigest()[:16]}  {pf}")
    recs = [bind(Path(d), plans, write=not a.check) for d in a.decks]
    for r in recs:
        print(f"  {r['status']:9s} {Path(r['file']).name[:56]:56s} "
              f"{r.get('planId','')} {r.get('reason','')}")
    bad = [r for r in recs if r["status"] in ("UNMATCHED", "AMBIGUOUS")]
    om = [r for r in recs if r.get("outcomesMatch") is False]
    print(f"\n{sum(1 for r in recs if r['status']=='BOUND')} bound, {len(bad)} unbound, "
          f"{len(om)} with outcomes differing from their plan")
    if a.output:
        Path(a.output).parent.mkdir(parents=True, exist_ok=True)
        Path(a.output).write_text(json.dumps(
            {"tool": "bind_plan_ids", "file": "tools/easter/bind_plan_ids.py",
             "plansSha256": hashlib.sha256(pf.read_bytes()).hexdigest(),
             "rows": recs}, indent=1) + "\n", encoding="utf-8")
    raise SystemExit(0 if not bad and not om else 1)
