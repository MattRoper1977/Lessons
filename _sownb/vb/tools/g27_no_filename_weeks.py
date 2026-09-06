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

DERIVE, DO NOT RE-PIN (A2R 3.4). Earlier callers asserted "18 controls" and
"133 tools" as literals in a workflow. Both are facts about the repository on
the day somebody looked, and a literal that has to be re-typed when the estate
grows is a gate that goes red for the wrong reason -- or, worse, one that
somebody quietly edits to match. The apexpool hardcoded-count precedent is the
same lesson. The tool now publishes its control list through --list-controls,
and the workflow asserts that EVERY LISTED CONTROL FIRED without ever naming a
number. The scanned-tool count is reported, never asserted.

Usage:
  g27_no_filename_weeks.py [--output <report.json>] [--self-test] [--list-controls]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import tempfile
from pathlib import Path

VERSION = "g27-v2.0.0-controls-derived-not-pinned"
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
    """Is the thing being matched against derived from a path?

    Reading only the HEAD identifier missed every wrapped form -- str(d),
    f"{d}", "/".join(parts) -- so a week could be read from a folder name by
    putting the path inside a call. A path name ANYWHERE in the subject
    expression counts, matched on word boundaries so `deck_text` is not `deck`.
    Found by the control py-term-folder-regex-on-a-path, which failed to fire.
    """
    subject = subject.strip()
    if PATH_EXPR.search(subject):
        return True
    for name in names:
        if re.search(r"\b" + re.escape(name) + r"\b", subject):
            return True
    return False


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


# Each control is a tiny source file that either MUST or MUST NOT be flagged.
# Positives prove the detector fires; negatives prove it is not a rubber stamp
# that flags every week-shaped regex in the estate.
#
# THE BODIES ARE ASSEMBLED, NOT WRITTEN OUT. This file scans _sownb/ and tools/,
# so it scans itself. A control written as a plain literal would make the gate
# flag its own control list, and the tempting fix -- an allowlist naming this
# file -- is an excuse with a filename. The same reasoning already governs
# _COL above. So the scannable fragments are built from pieces and no form this
# tool looks for appears in it verbatim.
_BS = chr(92)
_NL = chr(10)
_WD = "W(" + _BS + "d+)"           # W(\d+)
_WKD = "wk" + _BS + "d+"           # wk\d+
_A12 = "_A(" + "[12])_"            # the run-11 _A([12])_ filename rule
_SPRING = "Spring" + "[12]_W"
_AUT = "Autumn2" + "_W(" + _BS + "d+)"

CONTROLS = [
    # ---- positives: a week derived from a path -------------------------------
    ("py-week-regex-on-filename-var", True,
     f"import re{_NL}fn = 'BUILD_HUM_W16.html'{_NL}m = re.search(r'_{_WD}_', fn){_NL}"),
    ("py-week-regex-on-path-name", True,
     f"import re{_NL}from pathlib import Path{_NL}m = re.search(r'_{_WD}_', Path(x).name){_NL}"),
    ("py-week-regex-on-path-stem", True,
     f"import re{_NL}from pathlib import Path{_NL}m = re.search(r'{_WD}', Path(x).stem){_NL}"),
    ("py-week-regex-on-basename", True,
     f"import re, os{_NL}m = re.match(r'.*_{_WD}_', os.path.basename(p)){_NL}"),
    ("py-week-regex-on-dirname", True,
     f"import re, os{_NL}rows = re.findall(r'{_AUT}', os.path.dirname(p)){_NL}"),
    ("py-week-regex-on-parts-minus-one", True,
     f"import re{_NL}seg = parts[-1]{_NL}m = re.search(r'{_WKD}', seg){_NL}"),
    ("py-compiled-week-regex-on-a-path", True,
     f"import re{_NL}WEEK = re.compile(r'_{_WD}_'){_NL}"
     f"from pathlib import Path{_NL}name = Path(p).name{_NL}m = WEEK.search(name){_NL}"),
    ("py-run11-underscore-A-filename-rule", True,
     f"import re{_NL}fn = candidate{_NL}m = re.search(r'{_A12}', fn){_NL}"),
    ("py-term-folder-regex-on-a-path-wrapped-in-str", True,
     f"import re{_NL}from pathlib import Path{_NL}d = Path(p).parent{_NL}"
     f"m = re.search(r'{_SPRING}', str(d)){_NL}"),
    ("js-week-regex-on-path-var", True,
     f"const filename = 'GROW_HUM_W15.html';{_NL}const m = filename.match(/_{_WD}_/);{_NL}"),
    ("js-week-regex-on-derived-path-var", True,
     f"const base = path.basename(f);{_NL}const m = base.match(/{_WD}/);{_NL}"),
    # ---- positives: a week read from the superseded spine column -------------
    ("spine-absolute-week-subscript-read", True,
     f"import json{_NL}d = json.load(open('CALENDAR_" + "SPINE.json'))" + f"{_NL}"
     f"w = d['rows'][0]['{_COL}']{_NL}"),
    ("spine-absolute-week-get-read", True,
     f"import json{_NL}d = json.load(open('CALENDAR_" + "SPINE.json'))" + f"{_NL}"
     f"w = d.get('{_COL}'){_NL}"),
    ("spine-absolute-week-attribute-read", True,
     "spine = load('CALENDAR_" + "SPINE.json')" + f"{_NL}w = spine.{_COL}{_NL}"),
    # ---- negatives: legal ways to know a week --------------------------------
    ("week-from-a-workbook-cell-via-the-spine", False,
     f"import re{_NL}def week_of(cell_reference, spine):{_NL}"
     f"    m = re.search(r'C({_BS}{_BS}d+)', cell_reference){_NL}"
     f"    return spine.ruled_week(m.group(1)) if m else None{_NL}"),
    ("week-from-the-decks-own-text", False,
     f"import re{_NL}def week_from_markup(raw):{_NL}"
     f"    m = re.search(r'Week ({_BS}{_BS}d+) ', raw){_NL}"
     f"    return int(m.group(1)) if m else None{_NL}"),
    ("spine-absolute-week-named-only-in-a-comment", False,
     f"import json{_NL}# the {_COL} column is superseded and is not read here{_NL}"
     "d = json.load(open('CALENDAR_" + "SPINE.json'))" + f"{_NL}w = d['rows'][0]['ruledWeek']{_NL}"),
    ("spine-read-for-a-column-that-is-not-absolute-week", False,
     "import json" + f"{_NL}d = json.load(open('CALENDAR_" + "SPINE.json'))"
     + f"{_NL}w = d['rows'][0]['termLabel']{_NL}"),
    ("non-week-regex-on-a-path", False,
     f"import re{_NL}from pathlib import Path{_NL}m = re.search(r'START_HERE', Path(p).name){_NL}"),
]


def list_controls() -> list[str]:
    return [cid for cid, _, _ in CONTROLS]


def controls() -> dict:
    """A gate that cannot be made to fire has measured nothing. Every control is
    planted in a temporary file, scanned, and withdrawn when the directory goes."""
    out = {}
    with tempfile.TemporaryDirectory() as tmp:
        for label, must_fire, body in CONTROLS:
            p = Path(tmp) / f"{label.replace('-', '_')}.py"
            if label.startswith("js-"):
                p = p.with_suffix(".js")
            p.write_text(body, encoding="utf-8")
            hits = scan(p)
            fired = bool(hits)
            out[label] = {"mustFire": must_fire, "fired": fired, "ok": fired == must_fire,
                          "hits": hits}
    out["nonVacuous"] = all(v["ok"] for v in out.values() if isinstance(v, dict))
    out["controlsDeclared"] = len(CONTROLS)
    out["controlsFiredAsDeclared"] = sum(
        1 for v in out.values() if isinstance(v, dict) and v.get("ok"))
    out["allListedControlsFired"] = (
        out["controlsFiredAsDeclared"] == out["controlsDeclared"])
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output")
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--list-controls", action="store_true")
    args = ap.parse_args()

    if args.list_controls:
        for c in list_controls():
            print(c)
        return 0

    ctl = controls()
    report = measure()
    report["firingControls"] = ctl
    report["file"] = "_sownb/vb/tools/g27_no_filename_weeks.py"
    report["toolVersion"] = VERSION
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

    print(f"g27  scanned {report['toolsScanned']} tools  ·  {report['hitCount']} hit(s) in "
          f"{report['toolsWithHits']} file(s)  [{VERSION}]")
    for k, v in ctl.items():
        if isinstance(v, dict):
            print(f"  control {k:46s} mustFire={v['mustFire']!s:5s} fired={v['fired']!s:5s} "
                  f"{'ok' if v['ok'] else 'FAILED'}")
    print(f"  {ctl['controlsFiredAsDeclared']}/{ctl['controlsDeclared']} listed controls behaved as declared "
          f"(count DERIVED from --list-controls, never pinned)")
    for row in report["rows"]:
        print(f"\n  {row['file']}")
        for h in row["hits"]:
            print(f"    :{h['line']:<5d} {h['kind']:34s} {h['pattern'][:40]:42s} <- {h['subject'][:40]}")
    print(f"\n{report['status']}")
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
