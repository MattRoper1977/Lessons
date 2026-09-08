#!/usr/bin/env python3
"""UX2 A2 — publish the calendar spine the hub reads at runtime.

_sownb/ is never published (the education builder skips every `_`-prefixed
directory), so the hub cannot read _sownb/CALENDAR_2026_27.json itself. This
tool DERIVES data/calendar-spine.json from that file: the week-start dates and
the six half-term blocks (absolute week ranges). Nothing is authored here; a
date that is not in the source cannot appear in the output.

    python3 tools/ux2/build_spine.py --write     regenerate data/calendar-spine.json
    python3 tools/ux2/build_spine.py --check     committed file == derivation (exit 1 on drift)
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "_sownb/CALENDAR_2026_27.json"
TERM_DATES = ROOT / "_sownb/TERM_DATES.md"
OUTPUT = ROOT / "data/calendar-spine.json"
BLOCKS = [("Autumn 1", "Autumn", "Aut1"), ("Autumn 2", "Autumn", "Aut2"), ("Spring 1", "Spring", "Spr1"),
          ("Spring 2", "Spring", "Spr2"), ("Summer 1", "Summer", "Sum1"), ("Summer 2", "Summer", "Sum2")]


def derive() -> dict:
    source = json.loads(SOURCE.read_text("utf-8"))
    week_starts = {str(k): v for k, v in source["weekStarts"].items()}
    blocks = {}
    for label, term, key in BLOCKS:
        abs_range = source["terms"][term][key]["abs"]
        first, last = (int(x) for x in abs_range.split("-"))
        blocks[label] = {"label": label, "abs": [first, last], "weeks": last - first + 1,
                         "start": week_starts[str(first)], "lastWeekStart": week_starts[str(last)]}
    return {"schema": "mbm-calendar-spine-published-v1", "derivedFrom": SOURCE.relative_to(ROOT).as_posix(),
            "sourceSchema": source.get("schema"), "sourceStatement": source.get("source"),
            "termDates": TERM_DATES.relative_to(ROOT).as_posix(), "totalWeeks": source.get("totalWeeks"),
            "weekStarts": week_starts, "blocks": blocks}


def serialise(value: dict) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    text = serialise(derive())
    if args.write:
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT.write_text(text, "utf-8")
        print(f"[DONE] wrote {OUTPUT.relative_to(ROOT)}")
    if args.check or not args.write:
        current = OUTPUT.read_text("utf-8") if OUTPUT.is_file() else ""
        if current != text:
            print(f"[FAIL] {OUTPUT.relative_to(ROOT)} differs from its derivation — run: python3 tools/ux2/build_spine.py --write")
            return 1
        print(f"[PASS] {OUTPUT.relative_to(ROOT)} equals its derivation ({len(derive()['blocks'])} blocks, {len(derive()['weekStarts'])} weeks)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
