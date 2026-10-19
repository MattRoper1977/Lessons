#!/usr/bin/env python3
"""tm-4(b): every lesson row's outcome is present, is not a placeholder, and Week 8 says what its page says.

The Science hub cards print a lesson row's `desc` as the lesson's outcome. Two of
them were wrong on the live hub, and nothing failed: the BUILD Week 8 P2 row read
"I can show an idea" (a placeholder), and the P1 row carried one success criterion
instead of the lesson's goal. All seven Week 8 rows turned out to carry their
page's first "Today I can" criterion rather than its learning goal.

What is checked, on every row whose type is lesson (either case):

  O1  an outcome is present on every row whose page states a learning goal
  O2  rows with neither an outcome nor a learning goal on their page are listed in
      lesson-outcome-baseline.json, and that list can only shrink: a new row may not
      join it, a listed row whose page gains a learning goal must gain an outcome,
      and a listed row that gains an outcome must leave the list
  O3  no outcome is a placeholder
  O4  the seven Week 8 rows (ruling tm add.2) equal their page's learning-goal line

The 101 rows in the baseline are a later supplier job (ruling tm add.2): their
outcomes are held, not invented here.

    python3 tools/ux2/check_lesson_outcomes.py              check, exit 1 on any finding
    python3 tools/ux2/check_lesson_outcomes.py --self-test  five planted defects must each go red
"""
from __future__ import annotations

import argparse
import copy
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CATALOGUE = ROOT / "resources.json"
BASELINE = Path(__file__).resolve().parent / "lesson-outcome-baseline.json"

# The rows the ruling names: the seven corrected Week 8 Science lessons.
WEEK8 = [
    "dy4-sci-build-a1-w08-p1-animals-get-food-by-eating",
    "dy4-sci-build-a1-w08-p2-show-what-you-know-about-body-science",
    "dy4-sci-grow-a1-w08-p1-the-moon-s-journey",
    "dy4-sci-grow-a1-w08-p2-autumn-science-show-your-thinking",
    "dy4-sci-launch-a1-w08-l1-enzyme-action-preparing-the-ph-investigation",
    "dy4-sci-launch-a1-w08-l2-amylase-and-ph-continuous-sampling-investigation",
    "dy4-sci-launch-a1-w08-l3-amylase-rate-graph-and-topic-1-consolidation",
]

# The page's own statement: a "Learning goal" heading followed by its line.
GOAL = re.compile(r"Learning goal\s*</[^>]+>\s*(?:<[^>]+>\s*)*([^<]{8,400})")
# A row's outcome may open with its catalogue position ("BUILD Science · Autumn 1 · Week 8. ").
POSITION = re.compile(r"^[^.]*?·\s*Week \d+\.\s*")
# Shapes that say nothing about the lesson. The first is the live defect.
PLACEHOLDERS = [
    re.compile(r"^I can (show|do|say|try|use|share|make|write) (an? |the |my )?(idea|ideas|it|this|that|thing|things|something|work)\.?$", re.I),
    re.compile(r"\b(TODO|TBC|TBD|lorem ipsum|placeholder|XXX)\b", re.I),
    re.compile(r"^\W*$"),
]


def norm(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def page_goal(rel: str, pages: dict[str, str] | None = None) -> str | None:
    if pages is not None and rel in pages:
        text = pages[rel]
    else:
        path = ROOT / rel
        if not rel.endswith(".html") or not path.is_file():
            return None
        text = path.read_text(encoding="utf-8", errors="ignore")
    found = GOAL.search(text)
    return norm(found.group(1)) if found else None


def outcome_of(row: dict) -> str:
    return norm(POSITION.sub("", str(row.get("desc") or "")))


def check(rows: list[dict], baseline: list[str], pages: dict[str, str] | None = None) -> list[str]:
    errors: list[str] = []
    listed = set(baseline)
    if len(listed) != len(baseline):
        errors.append(f"{BASELINE.name}: lists a row twice")
    lessons = [r for r in rows if str(r.get("type", "")).lower() == "lesson"]
    ids = {r["id"] for r in lessons}
    for rid in sorted(listed - ids):
        errors.append(f"{rid}: is in {BASELINE.name} but is not a lesson row; remove it")
    for row in lessons:
        rid, desc = row["id"], str(row.get("desc") or "")
        goal = page_goal(str(row.get("file", "")), pages)
        if not desc.strip():
            if goal:
                errors.append(f"{rid}: has no outcome, but its page states a learning goal ({goal[:70]!r}) (O1)")
            elif rid not in listed:
                errors.append(f"{rid}: has no outcome and its page states no learning goal, and it is not in "
                              f"{BASELINE.name}; the list can only shrink (O2)")
            continue
        if rid in listed:
            errors.append(f"{rid}: now has an outcome; remove it from {BASELINE.name} (O2)")
        outcome = outcome_of(row)
        if any(p.search(outcome) for p in PLACEHOLDERS):
            errors.append(f"{rid}: the outcome {outcome!r} is a placeholder (O3)")
    by_id = {r["id"]: r for r in lessons}
    for rid in WEEK8:
        row = by_id.get(rid)
        if row is None:
            errors.append(f"{rid}: the Week 8 row is missing (O4)")
            continue
        goal = page_goal(str(row.get("file", "")), pages)
        if goal is None:
            errors.append(f"{rid}: its page states no learning goal to compare with (O4)")
        elif outcome_of(row) != goal:
            errors.append(f"{rid}: the outcome {outcome_of(row)!r} is not its page's learning goal {goal!r} (O4)")
    return errors


def load() -> tuple[list[dict], list[str]]:
    rows = json.loads(CATALOGUE.read_text(encoding="utf-8"))
    baseline = [str(e["id"]) for e in json.loads(BASELINE.read_text(encoding="utf-8"))["rows"]]
    return rows, baseline


def self_test() -> int:
    rows, baseline = load()
    clean = set(check(rows, baseline))
    lessons = {r["id"]: r for r in rows if str(r.get("type", "")).lower() == "lesson"}
    with_goal = next(r for r in rows if str(r.get("type", "")).lower() == "lesson" and r.get("desc")
                     and r["id"] not in WEEK8 and page_goal(str(r["file"])))
    problems = 0

    def control(label: str, mutated_rows: list[dict], mutated_baseline: list[str], expect: str,
                pages: dict[str, str] | None = None) -> None:
        nonlocal problems
        added = [e for e in check(mutated_rows, mutated_baseline, pages) if e not in clean]
        if any(expect in e for e in added):
            print(f"[PASS] control: {label}")
        else:
            print(f"[FAIL] control not detected: {label}")
            problems += 1

    def edit(rid: str, **fields) -> list[dict]:
        out = copy.deepcopy(rows)
        for r in out:
            if r["id"] == rid:
                r.update(fields)
        return out

    control("the live placeholder returns to a row",
            edit(with_goal["id"], desc="BUILD Science · Autumn 1 · Week 3. I can show an idea"), baseline, "(O3)")
    control("a Week 8 row drifts from its page",
            edit(WEEK8[0], desc="BUILD Science · Autumn 1 · Week 8. I can name the planted drift of this control"),
            baseline, "(O4)")
    control("a row whose page states a goal loses its outcome", edit(with_goal["id"], desc=""), baseline, "(O1)")
    stray = copy.deepcopy(rows) + [{"id": "control-new-row", "type": "lesson", "file": "no/such/page.html",
                                    "title": "control", "subject": "control"}]
    control("a new row joins the no-outcome list", stray, baseline, "the list can only shrink")
    if baseline:
        listed = lessons[baseline[0]]
        control("a listed row's page gains a learning goal", rows, baseline, "(O1)",
                pages={listed["file"]: "<h3>Learning goal</h3><p>I can name the planted goal of this control.</p>"})
    after = set(check(rows, baseline))
    if after != clean:
        print("[FAIL] the catalogue does not check the same way after the controls")
        problems += 1
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    rows, baseline = load()
    errors = check(rows, baseline)
    lessons = sum(1 for r in rows if str(r.get("type", "")).lower() == "lesson")
    for e in errors:
        print("  -", e)
    problems = self_test() if args.self_test else 0
    if errors or problems:
        print(f"[RED] {len(errors)} finding(s), {problems} control problem(s)")
        return 1
    print(f"[PASS] lesson outcomes: {lessons} lesson rows; {len(baseline)} held in the baseline; "
          f"{len(WEEK8)} Week 8 rows equal their pages")
    return 0


if __name__ == "__main__":
    sys.exit(main())
