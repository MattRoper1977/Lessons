#!/usr/bin/env python3
"""g24 — explanatory visual density. Order VB run 6 §4.1; hardened A2R §3.1.

An EXPLANATORY visual is counted only when all of these hold:
  (a) it carries at least three <text> labels — a picture with no words on it
      explains nothing on its own;
  (b) its viewBox area is larger than an icon (>= 10000 user units, i.e. bigger
      than roughly 100x100);
  (c) it sits inside a pupil TEACHING stage, not nav, hud, splash or the
      control bar;
  (d) the prose of that same stage refers to it — a diagram nobody mentions is
      decoration, and decoration is counted separately;
  (e) it RENDERS ON SCREEN in the pupil view;
  (f) it is a drawing, not a label.

Everything else with a viewBox is DECORATIVE. A visual that cannot survive
print is counted again as PRINT-DEAD, because a diagram that dies on paper is
not available to the pupil who is working from paper.

THE TWO FAIL-OPEN CASES THIS VERSION CLOSES (A2R §3.1)
------------------------------------------------------
1. PRINT-ONLY GRAPHICS COUNTED AS SCREEN TEACHING. The old `stage_of` walked up
   looking for a class of `slide` **or `print-section`**, so a diagram that
   exists only in the print pack satisfied the "inside a teaching stage" test.
   The classic chassis has fourteen `.print-section` blocks per deck. A deck
   could satisfy "two explanatory visuals per lesson" without a pupil ever
   seeing one on the board. Screen visibility is now resolved from the deck's
   own CSS by lesson_stages, so `#print-area{display:none}` excludes the pack
   because of what the deck says, not because of a class name written here.

   The same resolution closes display:none, visibility:hidden, aria-hidden, the
   `hidden` attribute and the staff drawer, none of which the old version
   checked at all.

2. A ROTATED TEXT LABEL COUNTED AS A DIAGRAM. Requirement (a) asks for three
   `<text>` elements and requirement (b) for a large viewBox. An `<svg>` holding
   nothing but rotated axis labels satisfies both. It is typography, not a
   diagram. A visual must now contain at least one GRAPHICAL PRIMITIVE — a
   path, rect, circle, ellipse, line, polyline, polygon, image or use — with
   real geometry. No transform, rotation or CSS makes text into a drawing.

Neither change moves a threshold. `visuals.explanatory.min` is still 2 per
lesson and `visuals.decorative.max` is still 1, both read from the contract.
What changed is which objects are eligible to be counted.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import sys
from pathlib import Path

from lxml import html as lh

VERSION = "g24-v3.0.0-screen-scoped-and-drawings-only"
ROOT = Path(__file__).resolve().parents[3]
MIN_TEXT_LABELS = 3
MIN_VIEWBOX_AREA = 10000

_ls = importlib.util.spec_from_file_location(
    "lesson_stages", ROOT / "_sownb/vb/tools/lesson_stages.py")
stages_mod = importlib.util.module_from_spec(_ls)
_ls.loader.exec_module(stages_mod)

CHROME = ("n6-splash", "controls", "control-bar", "hud", "nav", "mbmhome",
          "n6-nav1", "timer-widget", "progress-wrap", "hint-btn")

# A drawing has at least one of these with real geometry. <text> is not here,
# and no amount of transform puts it here.
SHAPE_TAGS = ("path", "rect", "circle", "ellipse", "line", "polyline",
              "polygon", "image", "use")


def viewbox_area(svg) -> float:
    vb = svg.get("viewBox") or svg.get("viewbox")
    if not vb:
        return 0.0
    parts = re.split(r"[\s,]+", vb.strip())
    if len(parts) != 4:
        return 0.0
    try:
        return abs(float(parts[2]) * float(parts[3]))
    except ValueError:
        return 0.0


def in_chrome(node) -> bool:
    n = node
    while n is not None:
        cls = (n.get("class") or "")
        if any(c in cls for c in CHROME):
            return True
        n = n.getparent()
    return False


def shape_count(svg) -> int:
    """Graphical primitives with real geometry, ignoring zero-size placeholders."""
    total = 0
    for tag in SHAPE_TAGS:
        for el in svg.xpath(f".//*[local-name()='{tag}']"):
            if tag in ("rect", "image", "use"):
                try:
                    w = float((el.get("width") or "0").rstrip("px%") or 0)
                    h = float((el.get("height") or "0").rstrip("px%") or 0)
                except ValueError:
                    w = h = 1.0
                if w <= 0 or h <= 0:
                    continue
            if tag == "circle":
                try:
                    if float(el.get("r") or 0) <= 0:
                        continue
                except ValueError:
                    pass
            if tag == "path" and not (el.get("d") or "").strip():
                continue
            total += 1
    return total


def referred_to(svg, stage) -> bool:
    """Does the stage's prose mention the figure at all?"""
    if stage is None:
        return False
    words = ("diagram", "figure", "image", "picture", "chart", "graph", "map",
             "model", "shown", "above", "below", "look at", "opposite")
    txt = " ".join(stage.text_content().split()).lower()
    if any(w in txt for w in words):
        return True
    label = (svg.get("aria-label") or "").strip().lower()
    return bool(label) and label in txt


def _hidden_within(svg, stage, screen) -> bool:
    """Is this svg hidden inside its stage, in the pupil's screen view?

    The stage itself is the visible root -- both shells page through a lesson
    with .slide{display:none}/.slide.active{display:flex}, so a stage's own
    display state is navigation, not hiding. See lesson_stages.
    """
    node = svg
    while node is not None and node is not stage:
        if screen.declared_hidden(node) or screen.marked_hidden(node):
            return True
        if stages_mod.is_staff(node) or stages_mod.is_chrome(node):
            return True
        node = node.getparent()
    return False


def survives_print(svg, tree) -> bool:
    """A visual is print-dead when the print view hides it."""
    printview = stages_mod.ScreenView(tree, media="print")
    node = svg
    while node is not None:
        if printview.declared_hidden(node) or printview.marked_hidden(node):
            return False
        cls = (node.get("class") or "").split()
        if "no-print" in cls:
            return False
        node = node.getparent()
    return True


def measure(path: Path) -> dict:
    tree = lh.fromstring(Path(path).read_text(encoding="utf-8"))
    screen = stages_mod.ScreenView(tree)
    teaching = stages_mod.stages(tree, screen)
    stage_set = set(teaching)

    explanatory, decorative, printdead, excluded = [], [], [], []
    for svg in tree.xpath("//svg"):
        area = viewbox_area(svg)
        labels = len(svg.xpath(".//*[local-name()='text']"))
        shapes = shape_count(svg)
        stage = None
        for anc in svg.iterancestors():
            if anc in stage_set:
                stage = anc
                break
        entry = {
            "labels": labels, "area": area, "shapes": shapes,
            "stage": (stage.get("data-title") or stage.get("id") or "") if stage is not None else None,
        }
        if stage is None:
            # not in a pupil teaching stage at all: the print pack, the splash,
            # the nav. Recorded so the exclusion is visible, never counted.
            entry["excludedBecause"] = "not inside a screen-visible teaching stage"
            excluded.append(entry)
            continue
        if _hidden_within(svg, stage, screen):
            entry["excludedBecause"] = "hidden in the pupil's screen view, or in the staff drawer"
            excluded.append(entry)
            continue
        if in_chrome(svg):
            entry["excludedBecause"] = "page chrome"
            excluded.append(entry)
            continue
        if shapes == 0:
            entry["excludedBecause"] = "text only: a label is not a drawing, whatever it is rotated by"
            excluded.append(entry)
            continue
        if labels >= MIN_TEXT_LABELS and area >= MIN_VIEWBOX_AREA and referred_to(svg, stage):
            explanatory.append(entry)
            if not survives_print(svg, tree):
                printdead.append(entry)
        else:
            decorative.append(entry)

    with_vis = {e["stage"] for e in explanatory if e["stage"]}
    return {
        "file": str(path), "toolVersion": VERSION,
        "shell": stages_mod.shell_of(tree),
        "explanatory": len(explanatory), "decorative": len(decorative),
        "printDead": len(printdead), "excluded": len(excluded),
        "stages": len(teaching),
        "stagesWithExplanatory": len(with_vis),
        "stagesWithNone": max(0, len(teaching) - len(with_vis)),
        "explanatoryDetail": explanatory,
        "excludedDetail": excluded,
    }


CONTRACT = ROOT / "_sownb/STYLE_CONTRACT.json"


def contract_rows() -> dict:
    rows = {r["id"]: r for r in json.loads(CONTRACT.read_text())["rows"]}
    return {k: rows[k] for k in ("visuals.explanatory.min", "visuals.decorative.max")
            if k in rows}


def judge(m: dict, rows: dict) -> dict:
    exp = rows.get("visuals.explanatory.min")
    dec = rows.get("visuals.decorative.max")
    fails = []
    if exp is not None:
        need = exp["value"]["perLesson"]
        if m["explanatory"] < need:
            fails.append(f"visuals.explanatory.min: {m['explanatory']} < {need} per lesson")
        if m["printDead"]:
            fails.append(f"visuals.explanatory.min: {m['printDead']} print-dead")
    if dec is not None and m["decorative"] > dec["value"]["perLesson"]:
        fails.append(f"visuals.decorative.max: {m['decorative']} > {dec['value']['perLesson']}")
    return {"fails": fails, "verdict": "PASS" if not fails else "RED"}


# --------------------------------------------------------------------------
# Controls
# --------------------------------------------------------------------------

_DRAWING = ('<svg viewBox="0 0 400 300" aria-label="the diagram">'
            '<rect x="10" y="10" width="80" height="60"/>'
            '<path d="M10 10 L90 70"/><circle cx="50" cy="50" r="20"/>'
            '<text>one</text><text>two</text><text>three</text></svg>')
_LABELS_ONLY = ('<svg viewBox="0 0 400 300" aria-label="the diagram">'
                '<g transform="rotate(-90)">'
                '<text>one</text><text>two</text><text>three</text></g></svg>')

_SHELL = """<!doctype html><html><head><style>
#print-area{display:none}
.slide{display:none}.slide.active{display:flex}
.tucked{display:none}
@media print{#print-area{display:block!important}.slide-container{display:none!important}}
</style></head><body>
<main id="lessonDeck" class="deck"><div class="slide-container">
  <div class="slide active" data-title="I Do"><p>Look at the diagram above and say what it shows.</p>__A__</div>
  <div class="slide" data-title="We Do"><p>Look at the diagram below and label it.</p>__B__</div>
</div></main>
<div id="print-area"><div class="print-section">
  <p>Look at the diagram above.</p>__C__
</div></div>
</body></html>"""


def _build(a="", b="", c=""):
    return _SHELL.replace("__A__", a).replace("__B__", b).replace("__C__", c)


def _count(source: str) -> dict:
    import tempfile
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as fh:
        fh.write(source)
        name = fh.name
    try:
        return measure(Path(name))
    finally:
        Path(name).unlink(missing_ok=True)


CONTROL_IDS = [
    "screen-svg-is-counted",
    "print-only-svg-is-not-counted",
    "hidden-svg-is-not-counted",
    "aria-hidden-svg-is-not-counted",
    "staff-drawer-svg-is-not-counted",
    "rotated-text-label-is-not-a-visual",
    "text-only-svg-is-not-a-visual",
    "unreferenced-drawing-is-decorative-not-explanatory",
    "icon-sized-drawing-is-decorative-not-explanatory",
]


def controls() -> list[dict]:
    out = []

    def rec(cid, description, expected, observed):
        out.append({"id": cid, "description": description, "expected": expected,
                    "observed": observed, "fired": expected == observed})

    rec("screen-svg-is-counted",
        "a referred-to drawing on a screen stage counts as explanatory",
        2, _count(_build(a=_DRAWING, b=_DRAWING))["explanatory"])

    rec("print-only-svg-is-not-counted",
        "the same drawing inside #print-area (display:none on screen, block under @media print) counts zero",
        0, _count(_build(c=_DRAWING + _DRAWING))["explanatory"])

    rec("hidden-svg-is-not-counted",
        "a drawing inside a display:none block on a stage counts zero",
        0, _count(_build(a=f'<div class="tucked">{_DRAWING}</div>'))["explanatory"])

    rec("aria-hidden-svg-is-not-counted",
        'a drawing inside aria-hidden="true" counts zero',
        0, _count(_build(a=f'<div aria-hidden="true">{_DRAWING}</div>'))["explanatory"])

    rec("staff-drawer-svg-is-not-counted",
        "a drawing inside the staff drawer counts zero",
        0, _count(_build(a=f'<div data-audience="staff">{_DRAWING}</div>'))["explanatory"])

    rec("rotated-text-label-is-not-a-visual",
        "an svg of three rotated <text> labels in a large viewBox counts zero",
        0, _count(_build(a=_LABELS_ONLY, b=_LABELS_ONLY))["explanatory"])

    rec("text-only-svg-is-not-a-visual",
        "the same labels without the rotation still count zero",
        0, _count(_build(a=_LABELS_ONLY.replace('<g transform="rotate(-90)">', "<g>")))["explanatory"])

    plain = _build(a=_DRAWING).replace(
        "<p>Look at the diagram above and say what it shows.</p>", "<p>Now write your answer.</p>")
    plain = plain.replace(' aria-label="the diagram"', "")
    m = _count(plain)
    rec("unreferenced-drawing-is-decorative-not-explanatory",
        "a drawing the stage prose never mentions is decorative",
        (0, 1), (m["explanatory"], m["decorative"]))

    icon = _DRAWING.replace('viewBox="0 0 400 300"', 'viewBox="0 0 20 20"')
    m2 = _count(_build(a=icon))
    rec("icon-sized-drawing-is-decorative-not-explanatory",
        "a drawing below the icon-size floor is decorative",
        (0, 1), (m2["explanatory"], m2["decorative"]))

    return out


def self_test() -> dict:
    results = controls()
    ids = [r["id"] for r in results]
    missing = [c for c in CONTROL_IDS if c not in ids]
    extra = [c for c in ids if c not in CONTROL_IDS]
    return {"tool": "g24_visual_density", "toolVersion": VERSION,
            "controlsDeclared": len(CONTROL_IDS), "controlsRun": len(results),
            "controlsFired": sum(1 for r in results if r["fired"]),
            "missingControls": missing, "undeclaredControls": extra,
            "allListedControlsFired": not missing and not extra and all(r["fired"] for r in results),
            "controls": results}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="*")
    ap.add_argument("--scope", default="live", choices=("live", "new"))
    ap.add_argument("--output")
    ap.add_argument("--list-controls", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()

    if a.list_controls:
        for c in CONTROL_IDS:
            print(c)
        return 0
    if a.self_test:
        report = self_test()
        if a.output:
            out = ROOT / a.output if not Path(a.output).is_absolute() else Path(a.output)
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(json.dumps(report, indent=1) + "\n", encoding="utf-8")
        print(f"g24 self-test  [{VERSION}]")
        for r in report["controls"]:
            print(f"  {'ok  ' if r['fired'] else 'FAIL'} {r['id']:52s} "
                  f"expected={r['expected']} observed={r['observed']}")
        print(f"{report['controlsFired']}/{report['controlsRun']} controls fired")
        print("PASS" if report["allListedControlsFired"] else "MEASUREMENT INVALID")
        return 0 if report["allListedControlsFired"] else 1

    rows = contract_rows()
    binding = a.scope == "new" and all(r.get("scope") == "new" for r in rows.values())
    sha = hashlib.sha256(CONTRACT.read_bytes()).hexdigest()
    out, red = [], 0
    for f in a.files:
        m = measure(ROOT / f if not Path(f).is_absolute() else Path(f))
        j = judge(m, rows)
        m.update({"scope": a.scope, "binding": binding, "contractSha256": sha, **j})
        if binding and j["verdict"] == "RED":
            red += 1
        out.append(m)
        print(f"{Path(f).name[:44]:44s} shell={m['shell']:7s} explanatory={m['explanatory']} "
              f"decorative={m['decorative']} printDead={m['printDead']} excluded={m['excluded']} "
              f"{j['verdict']:4s} {'BINDING' if binding else 'report-only'} "
              f"contract {sha[:8]} [{VERSION}]")
        for fail in j["fails"]:
            print(f"    {fail}")
    if a.output:
        p = ROOT / a.output if not Path(a.output).is_absolute() else Path(a.output)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")
    else:
        Path("/tmp/g24_last.json").write_text(json.dumps(out, indent=1))
    return 1 if red else 0


if __name__ == "__main__":
    raise SystemExit(main())
