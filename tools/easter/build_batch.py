#!/usr/bin/env python3
"""Author one planned deck and run the gate stack over it. A3N batch driver."""
from __future__ import annotations
import argparse, importlib.util, json, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
_ad = importlib.util.spec_from_file_location("author_deck", ROOT / "tools/easter/author_deck.py")
ad = importlib.util.module_from_spec(_ad); _ad.loader.exec_module(ad)


def gate(script, args):
    r = subprocess.run([sys.executable, str(ROOT / "_sownb/vb/tools" / script), *args],
                       capture_output=True, text=True, cwd=str(ROOT))
    line = [l for l in (r.stdout or "").splitlines() if l.strip() and "fitz" not in l]
    return (line[0] if line else "(no output)"), r.returncode


def build(family, week, donor, reference, content_path, out, evidence=None,
          plan_index=None):
    """Address the plan by INDEX, never by family+week.

    This driver used to pick with `next(p for p in plans if p["family"] == family
    and p["ruledWeek"] == week)`. Two cover-taught LAUNCH ASDAN plans share week
    1, so that expression silently returns the FIRST of them and the second deck
    is authored carrying the first's cells -- a coverage lie the census reads as
    taught and nobody teaches. g29 now catches it after the fact; this stops it
    happening. The index is asserted against the family and week it was asked
    for, so a stale index is an error rather than a different lesson.
    """
    plans = json.loads((ROOT / "tools/easter/EASTER_TARGETS.json").read_text())["plans"]
    if plan_index is None:
        matches = [i for i, p in enumerate(plans)
                   if p["family"] == family and p["ruledWeek"] == week
                   and p.get("coverBeforeMattReturns")]
        if len(matches) != 1:
            raise SystemExit(
                f"AMBIGUOUS PLAN: {family} week {week} names {len(matches)} cover-taught "
                f"plans {matches}. Pass --plan-index; family+week is not a unique key.")
        plan_index = matches[0]
    plan = plans[plan_index]
    if plan["family"] != family or plan["ruledWeek"] != week:
        raise SystemExit(f"PLAN INDEX MISMATCH: index {plan_index} is "
                         f"{plan['family']} week {plan['ruledWeek']}, "
                         f"not {family} week {week}.")
    content = json.loads(Path(content_path).read_text(encoding="utf-8"))
    content["_reference"] = Path(reference)
    rec = ad.author(Path(donor), plan, content, Path(out))
    rec["gates"] = {}
    for script, args in (
            ("g23_period_load.py", ["--family", family, "--candidate", str(out), "--output", "/dev/null"]),
            ("g18_v2_family_floor.py", ["--family", family, "--candidate", str(out), "--output", "/dev/null"]),
            ("g24_visual_density.py", [str(out)]),
            ("g25_wedo_variety.py", [str(out)]),
            ("g28_cell_existence.py", [str(out)])):
        line, code = gate(script, args)
        rec["gates"][script.split("_")[0]] = {"line": line[:200], "exit": code}
    if evidence:
        Path(evidence).parent.mkdir(parents=True, exist_ok=True)
        Path(evidence).write_text(json.dumps(rec, indent=1, default=str) + "\n", encoding="utf-8")
    return rec


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    for f in ("family", "donor", "reference", "content", "out", "evidence"):
        ap.add_argument(f"--{f}")
    ap.add_argument("--week", type=int)
    ap.add_argument("--plan-index", type=int)
    a = ap.parse_args()
    r = build(a.family, a.week, a.donor, a.reference, a.content, a.out, a.evidence,
              a.plan_index)
    print(f"{Path(a.out).name}")
    print(f"  leaked={r['donorSentencesLeaked']} words={r['contentWords']} "
          f"timings={r['timingsSum']} status={r['status']}")
    for g, v in r["gates"].items():
        print(f"  {g:5s} {v['line'][:150]}")
    raise SystemExit(0 if r["status"] == "PASS" else 1)
