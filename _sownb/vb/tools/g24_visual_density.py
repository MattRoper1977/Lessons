#!/usr/bin/env python3
"""g24 — explanatory visual density. REPORT ONLY. Order VB run 6 §4.1.

An EXPLANATORY visual is counted only when all four hold:
  (a) it carries at least three <text> labels — a picture with no words on it
      explains nothing on its own;
  (b) its viewBox area is larger than an icon (>= 10000 user units, i.e. bigger
      than roughly 100x100);
  (c) it sits inside a teaching stage, not nav, hud, splash or the control bar;
  (d) the prose of that same stage refers to it — a diagram nobody mentions is
      decoration, and decoration is counted separately.

Everything else with a viewBox is DECORATIVE. A visual that cannot survive
print (colour-only meaning, or it lives in a print-hidden region) is counted
again as PRINT-DEAD, because a diagram that dies on paper is not available to
the pupil who is working from paper.
"""
from __future__ import annotations
import json, re, sys
from pathlib import Path
from lxml import html as lh

VERSION = "g24-v2.0.0-binding-on-scope-new"
ROOT = Path(__file__).resolve().parents[3]
MIN_TEXT_LABELS = 3
MIN_VIEWBOX_AREA = 10000
CHROME = ("n6-splash", "controls", "control-bar", "hud", "nav", "mbmhome",
          "n6-nav1", "timer-widget", "progress-wrap", "hint-btn")

def viewbox_area(svg) -> float:
    vb = svg.get("viewBox") or svg.get("viewbox")
    if not vb: return 0.0
    parts = re.split(r"[\s,]+", vb.strip())
    if len(parts) != 4: return 0.0
    try: return abs(float(parts[2]) * float(parts[3]))
    except ValueError: return 0.0

def in_chrome(node) -> bool:
    n = node
    while n is not None:
        cls = (n.get("class") or "")
        if any(c in cls for c in CHROME): return True
        n = n.getparent()
    return False

def stage_of(node):
    n = node
    while n is not None:
        cls = (n.get("class") or "")
        if "slide" in cls.split() or "print-section" in cls.split(): return n
        n = n.getparent()
    return None

def referred_to(svg, stage) -> bool:
    """Does the stage's prose mention the figure at all?"""
    if stage is None: return False
    words = ("diagram", "figure", "image", "picture", "chart", "graph", "map",
             "model", "shown", "above", "below", "look at", "opposite")
    txt = " ".join(stage.text_content().split()).lower()
    if any(w in txt for w in words): return True
    # an explicit accessible name that also appears in the prose counts
    label = (svg.get("aria-label") or "").strip().lower()
    return bool(label) and label in txt

def measure(path: Path) -> dict:
    tree = lh.fromstring(path.read_text(encoding="utf-8"))
    explanatory, decorative, printdead = [], [], []
    for svg in tree.xpath("//svg"):
        area = viewbox_area(svg)
        labels = len(svg.xpath(".//*[local-name()='text']"))
        stage = stage_of(svg)
        chrome = in_chrome(svg)
        entry = {"labels": labels, "area": area,
                 "stage": (stage.get("data-title") or stage.get("id") or "") if stage is not None else None}
        if (labels >= MIN_TEXT_LABELS and area >= MIN_VIEWBOX_AREA
                and stage is not None and not chrome and referred_to(svg, stage)):
            explanatory.append(entry)
            src = lh.tostring(svg, encoding="unicode")
            hidden = stage is not None and "no-print" in (stage.get("class") or "")
            if hidden: printdead.append(entry)
        elif not chrome:
            decorative.append(entry)
    stages = tree.xpath('//main[contains(concat(" ",normalize-space(@class)," ")," deck ")]'
                        '/section[contains(concat(" ",normalize-space(@class)," ")," slide ")]')
    with_vis = set()
    for e in explanatory:
        if e["stage"]: with_vis.add(e["stage"])
    return {"file": str(path.relative_to(ROOT)), "toolVersion": VERSION,
            "explanatory": len(explanatory), "decorative": len(decorative),
            "printDead": len(printdead), "stages": len(stages),
            "stagesWithExplanatory": len(with_vis),
            "stagesWithNone": max(0, len(stages) - len(with_vis))}

CONTRACT = ROOT / "_sownb/STYLE_CONTRACT.json"

def contract_rows() -> dict:
    """The two rows this gate enforces, and their scope."""
    rows = {r["id"]: r for r in json.loads(CONTRACT.read_text())["rows"]}
    return {k: rows[k] for k in ("visuals.explanatory.min", "visuals.decorative.max")
            if k in rows}


def judge(m: dict, rows: dict) -> dict:
    """Binding only where the row's scope is 'new'. Live work is never judged."""
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


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    scope = "new" if "--scope=new" in sys.argv else "live"
    rows = contract_rows()
    binding = scope == "new" and all(r.get("scope") == "new" for r in rows.values())
    out, red = [], 0
    for a in args:
        m = measure(ROOT / a)
        j = judge(m, rows)
        m["scope"] = scope
        m["binding"] = binding
        m["contractSha256"] = __import__("hashlib").sha256(CONTRACT.read_bytes()).hexdigest()
        m.update(j)
        if binding and j["verdict"] == "RED":
            red += 1
        out.append(m)
        print(f"{Path(a).name[:46]:46s} explanatory={m['explanatory']} decorative={m['decorative']} "
              f"printDead={m['printDead']} {j['verdict']:4s} "
              f"{'BINDING' if binding else 'report-only'} contract {m['contractSha256'][:8]} [{VERSION}]")
        for f in j["fails"]:
            print(f"    {f}")
    Path("/tmp/g24_last.json").write_text(json.dumps(out, indent=1))
    sys.exit(1 if red else 0)
