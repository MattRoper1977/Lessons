#!/usr/bin/env python3
"""g28 — every cited workbook cell exists in the spine.

ORDER VB-RUN14 R1. Five of the cell references the run-12 authoring modules
claimed -- C171, C172, C138 twice, C89 and C198 -- exist nowhere in
CALENDAR_SPINE.json's workbookCells. A lesson was nearly traced to cells that do
not exist, and a coverage count nearly credited them. So: every cell address in
any trace, module, candidate list or planner note must resolve to a spine row,
and a miss is RED.

WHAT COUNTS AS A CITATION. Two forms, both read wherever they occur in the files
named on the command line:
  fully qualified   'BUILD Weekly - Autumn'!C142      resolved directly
  bare              C142   resolved against the nearest sheet named before it;
                    failing that, against the deck's own lane (read from its
                    lesson-config family or its brand line, never its path) and
                    every term sheet -- kept ONLY if exactly one spine row
                    matches. That is the rule the run-11 census used for the
                    "C44 only" screen chips the W8-W13 Science chassis carries.
A bare address that resolves to no row is NOT IN SPINE; one that resolves to
more than one is AMBIGUOUS; one with no lane in scope is UNRESOLVABLE. All three
are red, because the run-12 modules cited bare addresses and that is how the
invented ones slipped through.

FIRING CONTROLS, both required or the verdict is MEASUREMENT INVALID:
  a scratch trace citing C999 on a real sheet   must RED
  a scratch trace citing a real address          must NOT

Usage:
  g28_cell_existence.py <file> [<file> ...] [--output <report.json>]
  g28_cell_existence.py --self-test
"""
from __future__ import annotations

import argparse
import json
import re
import tempfile
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SPINE = ROOT / "_sownb/CALENDAR_SPINE.json"

QUALIFIED = re.compile(r"'(BUILD|GROW|LAUNCH) Weekly - (Autumn|Spring|Summer)'!C(\d+)")
SHEET = re.compile(r"'?(BUILD|GROW|LAUNCH) Weekly - (Autumn|Spring|Summer)'?")
BARE = re.compile(r"(?<![A-Za-z0-9_])C(\d{2,3})(?![0-9A-Za-z_])")


def without_svg_path_coordinates(text: str) -> str:
    """Mask only actual SVG path geometry, preserving all citation offsets.

    `C210 50 ...` is a cubic-curve command, not workbook cell C210. Visible
    SVG text and accessible labels remain checked, as do JSON/config traces.
    """
    lines = [0]
    for match in re.finditer('\n', text): lines.append(match.end())
    spans = []
    class Paths(HTMLParser):
        def handle_starttag(self, tag, attrs):
            if tag != 'path': return
            raw = self.get_starttag_text()
            for match in re.finditer(r'''(?:\s)d\s*=\s*(["'])(.*?)\1''', raw, re.S):
                value = match.group(2)
                if re.fullmatch(r'[MmZzLlHhVvCcSsQqTtAa0-9+.,eE\s-]+', value):
                    line, col = self.getpos();start = lines[line - 1] + col
                    spans.append((start + match.start(2), start + match.end(2)))
        handle_startendtag = handle_starttag
    parser = Paths(convert_charrefs=False)
    parser.feed(text)
    for start, end in reversed(spans):
        text = text[:start] + ' ' * (end - start) + text[end:]
    return text


def spine_cells() -> set[str]:
    data = json.loads(SPINE.read_text(encoding="utf-8"))
    return {c["reference"] for c in data["workbookCells"]}


LANE = re.compile(r'"family"\s*:\s*"(BUILD|GROW|LAUNCH)')
LANE_TEXT = re.compile(r"\b(BUILD|GROW|LAUNCH)\b")


def lane_of(text: str) -> str | None:
    """The deck's own lane, from its lesson-config or brand line. Not its path."""
    m = LANE.search(text)
    if m:
        return m.group(1)
    m = LANE_TEXT.search(text[:4000])
    return m.group(1) if m else None


def citations(text: str, cells: set[str] | None = None) -> list[dict]:
    """Every cell citation in the text, qualified where the text lets it be."""
    text = without_svg_path_coordinates(text)
    out = []
    lane = lane_of(text)
    for m in QUALIFIED.finditer(text):
        out.append({"reference": m.group(0), "form": "qualified", "at": m.start()})
    # a bare address resolves against the nearest sheet name before it
    sheets = [(m.start(), f"'{m.group(1)} Weekly - {m.group(2)}'") for m in SHEET.finditer(text)]
    qualified_spans = {(m.start(), m.end()) for m in QUALIFIED.finditer(text)}
    for m in BARE.finditer(text):
        if any(a <= m.start() < b for a, b in qualified_spans):
            continue
        before = [s for pos, s in sheets if pos < m.start()]
        if before:
            out.append({"reference": f"{before[-1]}!C{m.group(1)}", "form": "bare, resolved against the nearest sheet named before it", "at": m.start()})
            continue
        if lane and cells is not None:
            hits = [f"'{lane} Weekly - {term}'!C{m.group(1)}" for term in ("Autumn", "Spring", "Summer")
                    if f"'{lane} Weekly - {term}'!C{m.group(1)}" in cells]
            if len(hits) == 1:
                out.append({"reference": hits[0], "form": "bare, resolved uniquely by the deck's own lane", "at": m.start()})
            elif len(hits) > 1:
                out.append({"reference": f"AMBIGUOUS!C{m.group(1)}", "form": f"bare, matches {len(hits)} rows in lane {lane}", "at": m.start()})
            else:
                out.append({"reference": f"'{lane} Weekly - ?'!C{m.group(1)}", "form": "bare, no row in any term sheet for this lane", "at": m.start()})
        else:
            out.append({"reference": f"?!C{m.group(1)}", "form": "bare, no sheet or lane in scope", "at": m.start()})
    return out


def judge(path: Path, cells: set[str]) -> dict:
    text = path.read_text(encoding="utf-8", errors="ignore")
    rows = citations(text, cells)
    missing = sorted({r["reference"] for r in rows if r["reference"] not in cells
                      and not r["reference"].startswith(("?!", "AMBIGUOUS!"))})
    unresolvable = sorted({r["reference"] for r in rows if r["reference"].startswith(("?!", "AMBIGUOUS!"))})
    return {
        "file": str(path.relative_to(ROOT)) if str(path).startswith(str(ROOT)) else str(path),
        "citations": len(rows),
        "distinct": len({r["reference"] for r in rows}),
        "notInSpine": missing,
        "unresolvable": unresolvable,
        "status": "PASS" if rows and not missing and not unresolvable else ("RED" if rows else "NO CITATIONS"),
    }


def controls(cells: set[str]) -> dict:
    with tempfile.TemporaryDirectory() as tmp:
        red = Path(tmp) / "red.py"
        red.write_text("L = {'sheet': 'BUILD Weekly - Autumn', 'cells': [\"'BUILD Weekly - Autumn'!C999\"]}\n")
        green = Path(tmp) / "green.py"
        green.write_text("L = {'sheet': 'BUILD Weekly - Autumn', 'cells': [\"'BUILD Weekly - Autumn'!C142\"]}\n")
        r = judge(red, cells)
        g = judge(green, cells)
    out = {
        "citesC999OnARealSheet": {"mustFire": True, "fired": r["status"] == "RED", "ok": r["status"] == "RED"},
        "citesARealAddress": {"mustFire": False, "fired": g["status"] == "RED", "ok": g["status"] == "PASS"},
    }
    path = '<svg><path d="M0 0 C210 10 30 40 50 60"/><text>C999</text></svg>'
    rows = citations('BUILD ' + path, cells)
    out['svgGeometryIsNotACellButSvgTextStillIs'] = {'mustFire':True,
        'fired':len(rows) == 1 and rows[0]['reference'].endswith('C999'),
        'ok':len(rows) == 1 and rows[0]['reference'].endswith('C999')}
    labelled = citations('BUILD <svg><path d="M0 0 C210 10 30 40 50 60" aria-label="C999"/></svg>', cells)
    out['accessibleSvgCitationStillFires'] = {'mustFire':True,
        'fired':len(labelled) == 1 and labelled[0]['reference'].endswith('C999'),
        'ok':len(labelled) == 1 and labelled[0]['reference'].endswith('C999')}
    out["nonVacuous"] = all(v["ok"] for v in out.values() if isinstance(v, dict))
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="*")
    ap.add_argument("--output")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    cells = spine_cells()
    ctl = controls(cells)
    rows = [judge(Path(f) if Path(f).is_absolute() else ROOT / f, cells) for f in args.files]
    red = [r for r in rows if r["status"] == "RED"]
    report = {
        "file": "_sownb/vb/tools/g28_cell_existence.py",
        "subject": "g28: every workbook cell cited in the named files resolves to a spine row (ORDER VB-RUN14 R1)",
        "spineCells": len(cells),
        "firingControls": ctl,
        "rows": rows,
        "filesRed": len(red),
        "status": "MEASUREMENT INVALID" if not ctl["nonVacuous"] else ("PASS" if not red else "RED"),
    }
    if args.output:
        out = ROOT / args.output if not Path(args.output).is_absolute() else Path(args.output)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(report, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    for k, v in ctl.items():
        if isinstance(v, dict):
            print(f"  control {k:26s} mustFire={v['mustFire']!s:5s} fired={v['fired']!s:5s} {'ok' if v['ok'] else 'FAILED'}")
    for r in rows:
        print(f"  {r['status']:13s} {r['file'][-58:]:58s} cites {r['distinct']:3d}"
              + (f"  NOT IN SPINE {r['notInSpine']}" if r["notInSpine"] else "")
              + (f"  UNRESOLVABLE {r['unresolvable']}" if r["unresolvable"] else ""))
    print(report["status"])
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
