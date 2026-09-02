#!/usr/bin/env python3
"""g27 — no tool derives a teaching week from a path.

ORDER VB-RUN13 R0: "Coverage is counted PER WORKBOOK CELL, never per week, never
per file. A week is a property of a cell (via the ruled spine); a deck's week is
the ruled week of the cells its TRACE claims. No tool may derive a week from a
filename, a folder name or CALENDAR_SPINE.json's absoluteWeek column."

Run 12 lost its whole wave-4 build to exactly this. The spine re-key moved
labels and left filenames alone on purpose, so a filename still counts weeks the
old way. A tool that reads the filename reports a week as open while a deck
stands in it, and five lessons were authored for cells that already had decks.

WHAT THIS MEASURES, precisely. Not "a week regex appears in this file" -- that
would flag every tool that reads a week from a deck's own text, which is legal.
It measures a regex operation whose PATTERN denotes a week and whose SUBJECT is
path-derived. The subject is path-derived when it is a known path name (fn,
basename, stem, dirname, relpath ...) or when the file assigns it from a path
expression (Path(...), os.path..., .split('/'), parts[-1], .name, .stem).

It also flags a read of CALENDAR_SPINE.json's absoluteWeek column, which the
same ruling puts out of bounds: that column is derived from the superseded
offsets, so consuming it is another way of reading a stale week.

Every hit prints the file, the line, the pattern and the subject, so the finding
can be checked by eye rather than trusted.

Usage:
  g27_no_filename_weeks.py [--output <report.json>] [--self-test]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SCAN_DIRS = ("_sownb", "tools")
SUFFIXES = (".py", ".js", ".mjs")
SKIP_PARTS = {"__pycache__", "node_modules", ".git", "fixtures"}

# A pattern denotes a week when it carries a week-shaped token.
WEEK_IN_PATTERN = re.compile(
    r"(?:"
    r"W\s*\(?\\d"          # W\d, W(\d
    r"|W\%d|W\{"            # W%d, W{n}
    r"|wk\\d"
    r"|week\s*\(?\\d"
    r"|Autumn\s*\[?12?\]?_?W"
    r"|Spring\s*\[?12?\]?_?W"
    r"|Summer\s*\[?12?\]?_?W"
    r"|_A\(\[12\]\)_"       # the run-11 _A([12])_ filename rule
    r"|_A\[12\]_"
    r")",
    re.I,
)

# Names that hold a path, and expressions that produce one.
PATH_NAMES = {
    "fn", "filename", "file_name", "basename", "base", "stem", "dirname", "dir",
    "relpath", "rel", "p", "path", "filepath", "file_path", "deck", "candidate",
    "src", "target", "name", "fname", "parts", "f",
}
PATH_EXPR = re.compile(
    r"(?:Path\s*\(|os\.path\.|\.split\s*\(\s*['\"]/|parts\s*\[-1\]|\.stem\b|\.name\b"
    r"|\.basename\b|path\.basename|relative_to\s*\(|__file__|\.parent\b|glob\s*\(|rglob\s*\()"
)

PY_CALL = re.compile(
    r"re\.(?:search|match|fullmatch|findall|finditer)\s*\(\s*(?P<pat>[rbf]?['\"].*?['\"])\s*,\s*(?P<subj>[^),]+)",
    re.S,
)
PY_COMPILED = re.compile(
    r"(?P<var>[A-Za-z_]\w*)\s*\.\s*(?:search|match|fullmatch|findall|finditer)\s*\(\s*(?P<subj>[^),]+)"
)
JS_CALL = re.compile(r"(?P<subj>[A-Za-z_$][\w$.\[\]]*)\s*\.\s*match\s*\(\s*(?P<pat>/.*?/[gimsuy]*)")
# A READ of the column, not the word. Prose that names it, and this gate's own
# detector, are not reads: d["absoluteWeek"], d.get("absoluteWeek"), d.absoluteWeek
# are. Written this way rather than as an allowlist so the gate does not need an
# exemption for itself, which is an excuse with a filename.
# The detector's pattern is BUILT, not written out, so this file does not contain
# the read form it looks for and needs no exemption for itself. An allowlist that
# covers the checker is an excuse with a filename.
_COL = "absolute" + "Week"
ABS_WEEK = re.compile(
    r"""(?:\[\s*['"]%s['"]\s*\]|\.get\(\s*['"]%s['"]|\.%s\b)""" % (_COL, _COL, _COL)
)
SPINE_FILE = re.compile(r"CALENDAR_" + "SPINE")


def path_derived_names(source: str) -> set[str]:
    """Names this file assigns from a path expression."""
    found = set(PATH_NAMES)
    for m in re.finditer(r"^\s*(?:const\s+|let\s+|var\s+)?([A-Za-z_$]\w*)\s*=\s*(.+)$", source, re.M):
        name, expr = m.group(1), m.group(2)
        if PATH_EXPR.search(expr):
            found.add(name)
    return found


def compiled_week_vars(source: str) -> set[str]:
    """Module-level names bound to a compiled regex whose pattern denotes a week."""
    out = set()
    for m in re.finditer(r"^\s*([A-Z_][A-Z0-9_]*)\s*=\s*re\.compile\s*\(\s*([rbf]?['\"].*?['\"])", source, re.M | re.S):
        if WEEK_IN_PATTERN.search(m.group(2)):
            out.add(m.group(1))
    return out


def subject_is_path(subject: str, names: set[str]) -> bool:
    subject = subject.strip()
    if PATH_EXPR.search(subject):
        return True
    head = re.match(r"([A-Za-z_$]\w*)", subject)
    return bool(head and head.group(1) in names)


def scan(path: Path) -> list[dict]:
    source = path.read_text(encoding="utf-8", errors="replace")
    names = path_derived_names(source)
    weekvars = compiled_week_vars(source)
    lines = source.split("\n")
    hits: list[dict] = []

    def line_of(index: int) -> int:
        return source.count("\n", 0, index) + 1

    for m in PY_CALL.finditer(source):
        if WEEK_IN_PATTERN.search(m.group("pat")) and subject_is_path(m.group("subj"), names):
            hits.append({"line": line_of(m.start()), "kind": "week regex on a path",
                         "pattern": m.group("pat")[:80], "subject": m.group("subj").strip()[:60]})
    for m in PY_COMPILED.finditer(source):
        if m.group("var") in weekvars and subject_is_path(m.group("subj"), names):
            hits.append({"line": line_of(m.start()), "kind": "compiled week regex on a path",
                         "pattern": m.group("var"), "subject": m.group("subj").strip()[:60]})
    for m in JS_CALL.finditer(source):
        if WEEK_IN_PATTERN.search(m.group("pat")) and subject_is_path(m.group("subj"), names):
            hits.append({"line": line_of(m.start()), "kind": "week regex on a path",
                         "pattern": m.group("pat")[:80], "subject": m.group("subj").strip()[:60]})
    if SPINE_FILE.search(source):
        for i, text in enumerate(lines, 1):
            stripped = text.lstrip()
            if stripped.startswith(("#", "//", "*")):
                continue
            if ABS_WEEK.search(text):
                hits.append({"line": i, "kind": "reads CALENDAR_SPINE absoluteWeek",
                            "pattern": _COL, "subject": text.strip()[:80]})
    seen, unique = set(), []
    for h in hits:
        key = (h["line"], h["kind"])
        if key not in seen:
            seen.add(key)
            unique.append(h)
    return unique


def files() -> list[Path]:
    out = []
    for d in SCAN_DIRS:
        for p in sorted((ROOT / d).rglob("*")):
            if p.suffix not in SUFFIXES or not p.is_file():
                continue
            if SKIP_PARTS & set(p.parts):
                continue
            out.append(p)
    return out


def measure() -> dict:
    rows = []
    for p in files():
        hits = scan(p)
        if hits:
            rows.append({"file": str(p.relative_to(ROOT)), "hits": hits})
    return {"toolsScanned": len(files()), "toolsWithHits": len(rows),
            "hitCount": sum(len(r["hits"]) for r in rows), "rows": rows}


def controls() -> dict:
    """A gate that cannot be made to fire has measured nothing."""
    red = ("import re\n"
           "def week_of(path):\n"
           "    m = re.search(r'_W(\\d+)_', path)\n"
           "    return int(m.group(1)) if m else None\n")
    green = ("import re\n"
             "def week_of(cell_reference, spine):\n"
             "    m = re.search(r'C(\\d+)', cell_reference)\n"
             "    return spine.ruled_week(m.group(1)) if m else None\n")
    green2 = ("import re\n"
              "def week_from_the_decks_own_text(html):\n"
              "    m = re.search(r'Week (\\d+) ', html)\n"
              "    return int(m.group(1)) if m else None\n")
    out = {}
    with tempfile.TemporaryDirectory() as tmp:
        for label, body, must_fire in (("readsWeekFromPath", red, True),
                                       ("readsWeekFromCell", green, False),
                                       ("readsWeekFromDeckText", green2, False)):
            p = Path(tmp) / f"{label}.py"
            p.write_text(body, encoding="utf-8")
            fired = bool(scan(p))
            out[label] = {"mustFire": must_fire, "fired": fired, "ok": fired == must_fire}
    out["nonVacuous"] = all(v["ok"] for v in out.values() if isinstance(v, dict))
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()

    ctl = controls()
    report = measure()
    report["firingControls"] = ctl
    report["file"] = "_sownb/vb/tools/g27_no_filename_weeks.py"
    report["subject"] = ("g27: no tool under _sownb/ or tools/ derives a teaching week from a filename, a "
                         "folder name or CALENDAR_SPINE absoluteWeek (ORDER VB-RUN13 R0)")
    report["rule"] = ("a week is a property of a workbook cell via the ruled spine; a deck's week is the "
                      "ruled week of the cells its trace claims")
    report["status"] = ("MEASUREMENT INVALID" if not ctl["nonVacuous"]
                        else "PASS" if report["hitCount"] == 0 else "RED")
    if args.output:
        out = ROOT / args.output if not Path(args.output).is_absolute() else Path(args.output)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(report, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"g27  scanned {report['toolsScanned']} tools  ·  {report['hitCount']} hit(s) in {report['toolsWithHits']} file(s)")
    for k, v in ctl.items():
        if isinstance(v, dict):
            print(f"  control {k:24s} mustFire={v['mustFire']!s:5s} fired={v['fired']!s:5s} {'ok' if v['ok'] else 'FAILED'}")
    for row in report["rows"]:
        print(f"\n  {row['file']}")
        for h in row["hits"]:
            print(f"    :{h['line']:<5d} {h['kind']:34s} {h['pattern'][:40]:42s} <- {h['subject'][:40]}")
    print(f"\n{report['status']}")
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
