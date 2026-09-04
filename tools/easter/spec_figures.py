#!/usr/bin/env python3
"""Generate a spec's print-sheet SVGs from its own figure blocks.

NOT A NEW DRAWING. Every spec this campaign has written carries two figures --
a four-box chain in "I Do · model" and a two-box columns in "I Do 2 · connect"
-- and each is drawn twice: once as data in the stage, and once as an SVG
string in `print.figures` for the sheet a pupil is handed. Until now the SVG
was written by hand beside the data, which means it could disagree with the
drawing it is supposed to be, and a print sheet disagreeing with the board is
the kind of defect nobody reports because both look fine alone.

This re-emits the SVG from the block data using the geometry already shipped.
The control does not assert that the geometry is good; it asserts that this
module reproduces EVERY figure in EVERY committed spec byte for byte. A
generator that cannot reproduce what shipped has no business writing what ships
next. Two specs in the estate carry print figures with no stage figure behind
them -- the two batch-1 ASDAN decks, authored before the block form existed --
and they are reported and skipped rather than reflowed.

    python3 tools/easter/spec_figures.py --self-test
    python3 tools/easter/spec_figures.py --apply tools/artsaward/content/*.json
"""

import argparse
import glob
import json
from pathlib import Path

VERSION = "spec-figures-v1.0.0"

CONTROL_IDS = [
    "every-shipped-figure-rebuilds-byte-for-byte",
    "a-print-figure-with-no-block-behind-it-is-named-not-reflowed",
    "a-planted-difference-is-caught",
]

def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;"))

def chain(b):
    heads = b["boxes"]
    out = [f'<svg viewBox="0 0 620 150" role="img" width="100%" aria-label="{esc(b["alt"])}">',
           f'<title>{esc(b["title"])}</title>']
    for i, bx in enumerate(heads):
        x = 8 + i * 158
        cx = x + 65
        out.append(f'<rect x="{x}" y="42" width="130" height="60" rx="8" fill="none" stroke="#333" stroke-width="2"/>')
        out.append(f'<text x="{cx}" y="70" text-anchor="middle" font-size="13">{esc(bx["head"])}</text>')
        out.append(f'<text x="{cx}" y="88" text-anchor="middle" font-size="11">{esc(bx["line1"])}</text>')
        if i:
            lx1 = x - 28
            out.append(f'<line x1="{lx1}" y1="72" x2="{x - 4}" y2="72" stroke="#333" stroke-width="2"/>')
            out.append(f'<path d="M{x - 12} 66 L{x} 72 L{x - 12} 78 Z" fill="#333"/>')
    out.append(f'<text x="306" y="126" text-anchor="middle" font-size="12">{esc(b["caption"])}</text>')
    out.append('</svg>')
    return "".join(out)

def columns(b):
    a, c = b["boxes"]
    out = [f'<svg viewBox="0 0 620 190" role="img" width="100%" aria-label="{esc(b["alt"])}">',
           f'<title>{esc(b["title"])}</title>']
    for i, bx in enumerate((a, c)):
        x = 16 + i * 318
        cx = x + 135
        dash = ' stroke-dasharray="7 4"' if i else ''
        out.append(f'<rect x="{x}" y="16" width="270" height="104" rx="8" fill="none" stroke="#333" stroke-width="2"{dash}/>')
        out.append(f'<circle cx="{x + 24}" cy="42" r="7" fill="none" stroke="#333" stroke-width="2"/>')
        out.append(f'<text x="{cx}" y="48" text-anchor="middle" font-size="14">{esc(bx["head"])}</text>')
        out.append(f'<text x="{cx}" y="74" text-anchor="middle" font-size="11">{esc(bx["line1"])}</text>')
        out.append(f'<text x="{cx}" y="94" text-anchor="middle" font-size="11">{esc(bx["line2"])}</text>')
        out.append(f'<line x1="{cx}" y1="120" x2="{cx}" y2="140" stroke="#333" stroke-width="2"/>')
        out.append(f'<path d="M{cx - 6} 132 L{cx} 142 L{cx + 6} 132 Z" fill="#333"/>')
    out.append('<rect x="16" y="140" width="588" height="40" rx="8" fill="none" stroke="#333" stroke-width="2" stroke-dasharray="6 4"/>')
    out.append(f'<text x="310" y="165" text-anchor="middle" font-size="12">{esc(b["caption"])}</text>')
    out.append('</svg>')
    return "".join(out)

def render(b):
    return {"chain": chain, "columns": columns}[b["shape"]](b)

def figures(spec):
    out = []
    for st in spec["stages"]:
        for b in st["blocks"]:
            if b.get("kind") == "figure":
                out.append(render(b))
    return out



def apply(paths) -> dict:
    """Write print.figures into each spec from its own figure blocks."""
    out = {"tool": VERSION, "written": [], "unchanged": [], "skipped": []}
    for p in paths:
        p = Path(p)
        d = json.loads(p.read_text(encoding="utf-8"))
        got = figures(d)
        if not got:
            out["skipped"].append({"file": str(p), "why": "no figure block in any stage"})
            continue
        if d.get("print", {}).get("figures") == got:
            out["unchanged"].append(str(p)); continue
        d.setdefault("print", {})["figures"] = got
        p.write_text(json.dumps(d, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
        out["written"].append({"file": str(p), "figures": len(got)})
    return out


def self_test() -> dict:
    """Rebuild every figure in every committed spec and refuse on one byte."""
    res = []
    def rec(cid, why, expected, observed):
        res.append({"id": cid, "why": why, "expected": expected,
                    "observed": observed, "fired": expected == observed})
    checked = bad = 0
    for p in sorted(glob.glob("tools/easter/content/*.json")
                    + glob.glob("tools/artsaward/content/*.json")):
        d = json.loads(Path(p).read_text(encoding="utf-8"))
        want = d.get("print", {}).get("figures")
        if not want:
            continue
        got = figures(d)
        if len(got) != len(want):
            continue                      # counted by the second control instead
        for g, w in zip(got, want):
            checked += 1
            bad += (g != w)
    rec("every-shipped-figure-rebuilds-byte-for-byte",
        "a generator that cannot reproduce what shipped has no business writing "
        "what ships next",
        (True, 0), (checked > 0, bad))

    # TWO DIFFERENT MISMATCHES, AND ONLY ONE OF THEM IS A FAULT.
    #   printed > stage : a print figure with no block behind it. The two
    #                     batch-1 ASDAN specs predate the block form and their
    #                     decks are shipped, so a spec must stay in step with
    #                     the deck built from it. Named, never reflowed.
    #   stage > printed : a spec whose SVGs have not been generated yet. That
    #                     is what --apply is for, and it is reported as pending
    #                     rather than failed -- otherwise this control reds on
    #                     every freshly authored spec, and a control that reds
    #                     on the normal case teaches people to ignore it.
    orphans, pending = [], []
    for p in sorted(glob.glob("tools/easter/content/*.json")
                    + glob.glob("tools/artsaward/content/*.json")):
        d = json.loads(Path(p).read_text(encoding="utf-8"))
        stage = sum(1 for s in d["stages"] for b in s["blocks"] if b.get("kind") == "figure")
        printed = len(d.get("print", {}).get("figures", []))
        if printed > stage:
            orphans.append((Path(p).name, stage, printed))
        elif stage > printed:
            pending.append((Path(p).name, stage, printed))
    rec("a-print-figure-with-no-block-behind-it-is-named-not-reflowed",
        "the two batch-1 ASDAN specs predate the block form and their decks are "
        "shipped; a spec must stay in step with the deck built from it, so they "
        "are reported rather than rewritten",
        [("BUILD_ASDAN_W1.json", 0, 2), ("GROW_ASDAN_W1.json", 0, 2)],
        sorted(orphans))

    # MUST FIRE. A control that only ever says "identical" cannot be trusted to
    # notice a difference, so plant one and require that it is caught.
    sample = None
    for p in sorted(glob.glob("tools/easter/content/*.json")):
        d = json.loads(Path(p).read_text(encoding="utf-8"))
        if d.get("print", {}).get("figures") and figures(d):
            sample = d; break
    planted = False
    if sample is not None:
        hacked = json.loads(json.dumps(sample))
        for s in hacked["stages"]:
            for b in s["blocks"]:
                if b.get("kind") == "figure":
                    b["caption"] = b["caption"] + " (planted)"
        planted = figures(hacked)[0] != sample["print"]["figures"][0]
    rec("a-planted-difference-is-caught",
        "MUST FIRE. One changed caption must change the rebuilt SVG, or the "
        "byte-for-byte control above is measuring nothing",
        True, planted)

    return {"tool": VERSION, "controlsRun": len(res),
            "controlsFired": sum(1 for r in res if r["fired"]),
            "allListedControlsFired": all(r["fired"] for r in res), "controls": res,
            "figuresRebuilt": checked,
            "pendingGeneration": sorted(pending)}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("specs", nargs="*")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--output")
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--list-controls", action="store_true")
    a = ap.parse_args()
    if a.list_controls:
        print("\n".join(CONTROL_IDS)); raise SystemExit(0)
    if a.self_test:
        rep = self_test()
        for c in rep["controls"]:
            print(f"  {'ok  ' if c['fired'] else 'FAIL'} {c['id']:56s} "
                  f"expected={c['expected']} observed={c['observed']}")
        print(f"{rep['controlsFired']}/{rep['controlsRun']} controls fired "
              f"({rep['figuresRebuilt']} figures rebuilt)")
        if rep["pendingGeneration"]:
            print(f"  PENDING --apply: {len(rep['pendingGeneration'])} spec(s) have a "
                  f"figure block and no printed figure yet")
        print("PASS" if rep["allListedControlsFired"] else "MEASUREMENT INVALID")
        if a.output:
            Path(a.output).parent.mkdir(parents=True, exist_ok=True)
            Path(a.output).write_text(json.dumps(rep, indent=1) + "\n", encoding="utf-8")
        raise SystemExit(0 if rep["allListedControlsFired"] else 1)
    rep = apply(a.specs)
    for w in rep["written"]:
        print(f"  wrote {w['figures']} figure(s)  {w['file']}")
    for u in rep["unchanged"]:
        print(f"  unchanged            {u}")
    for s in rep["skipped"]:
        print(f"  skipped              {s['file']}  ({s['why']})")
    if a.output:
        Path(a.output).parent.mkdir(parents=True, exist_ok=True)
        Path(a.output).write_text(json.dumps(rep, indent=1) + "\n", encoding="utf-8")
