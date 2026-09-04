#!/usr/bin/env python3
"""Build and gate a batch of authored lesson specs. A3N batch driver."""
from __future__ import annotations
import argparse, hashlib, importlib.util, json, re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
_ad = importlib.util.spec_from_file_location("author_deck", ROOT / "tools/easter/author_deck.py")
ad = importlib.util.module_from_spec(_ad); _ad.loader.exec_module(ad)
_dt = importlib.util.spec_from_file_location("dt", ROOT / "tools/easter/derive_stage_timings.py")
dt = importlib.util.module_from_spec(_dt); _dt.loader.exec_module(dt)

STAGES = ["Lesson overview", "Arrival · retrieve", "Starter · create the need",
          "I Do · model", "We Do · everyone commits", "I Do 2 · connect",
          "We Do 2 · lab", "Independent · evidence", "Exit · Audience and Influence"]
MINUTES = [0, 3, 3, 7, 3, 7, 5, 9, 3]
PHASES = ["SEE", "SEE", "SEE", "SEE", "SAY", "SEE", "SAY", "ACT", "ACT"]


def normalise(content: dict) -> tuple[dict, list]:
    """Force the nine-stage spine the chassis needs, whatever the writer sent."""
    notes = []
    stages = content.get("stages", [])
    if len(stages) != 9:
        notes.append(f"writer sent {len(stages)} stages, spine needs 9")
    out = []
    for i, title in enumerate(STAGES):
        src = stages[i] if i < len(stages) else {"blocks": []}
        st = {"title": title, "minutes": MINUTES[i], "phase": PHASES[i],
              "blocks": src.get("blocks", [])}
        if i == 0:
            st["type"] = "title"
        # ADULT GUIDANCE MOVES INTO A RENDERED BLOCK, NOT AN INERT ATTRIBUTE.
        # A reviewer caught this: data-ta1 and data-ta2 are read by NOTHING in
        # this chassis -- zero references in its CSS or its JS -- so nine prep
        # instructions and a safeguarding deflection script would have been
        # invisible to the cover teacher who needs them. The attribute is kept
        # because the estate's decks carry it, and the text is ALSO emitted as a
        # data-mbm-guide="staff" block, which the guide toggle actually shows.
        guide = [src[k] for k in ("ta1", "ta2") if src.get(k)]
        for k in ("ta1", "ta2"):
            if src.get(k):
                st[f"data-{k}"] = src[k]
        if guide:
            st["blocks"] = ([{"kind": "staff", "text": " ".join(guide)}]
                            + st["blocks"])
        out.append(st)
    content["stages"] = out
    for st in content["stages"]:
        for b in st["blocks"]:
            if b.get("kind") == "figure":
                b["kind"] = "figure"
                b.setdefault("boxes", [])
                if b.get("figureKind"):
                    b["kind"] = "figure"
    return content, notes


def figures_of(content: dict) -> list:
    out = []
    for st in content["stages"]:
        for b in st["blocks"]:
            if b.get("kind") == "figure":
                spec = dict(b); spec["kind"] = spec.pop("figureKind", "chain")
                out.append(ad.render_figure(spec))
    return out


def gate(script, args):
    r = subprocess.run([sys.executable, str(ROOT / "_sownb/vb/tools" / script), *args],
                       capture_output=True, text=True, cwd=str(ROOT))
    lines = [l for l in (r.stdout or "").splitlines() if l.strip() and "fitz" not in l]
    return (lines[0] if lines else "(none)"), r.returncode


def build_one(spec, donors, plans, outdir_map):
    # KEYED ON THE PLAN INDEX, NOT family+week. Two LAUNCH ASDAN plans share
    # week 1 and a family+week lookup silently returns the first, which would
    # give the second deck the first one's workbook cells -- a coverage lie that
    # every gate would pass, because g28 only checks the cell EXISTS.
    fam, week = spec["family"], spec["week"]
    plan = plans[spec["planIndex"]]
    assert plan["family"] == fam and plan["ruledWeek"] == week, (
        f"planIndex {spec['planIndex']} is {plan['family']} wk{plan['ruledWeek']}, "
        f"spec says {fam} wk{week}")
    content, notes = normalise(spec["content"])
    content["slot"] = content.get("slot") or f'{plan["subject"]} cross-strand'
    content["id"] = re.sub(r"[^A-Za-z0-9_]", "", f'{fam.replace(" ", "_")}_W{week}')
    content.setdefault("print", {})["figures"] = figures_of(content)
    d = donors[fam]
    content["_reference"] = Path(d["reference"])
    pack = ROOT / outdir_map[fam]
    slug = re.sub(r"[^A-Za-z0-9]+", "_", content["title"]).strip("_")[:58]
    out = pack / f'{fam.replace(" ", "_")}_W{week}_{slug}.html'
    rec = ad.author(Path(d["donor"]), plan, content, out)
    rec["normaliseNotes"] = notes
    if rec["status"] == "PASS":
        dt.apply(out)
        rec["gates"] = {}
        for script, a in (("g23_period_load.py", ["--family", fam, "--candidate", str(out), "--output", "/dev/null"]),
                          ("g18_v2_family_floor.py", ["--family", fam, "--candidate", str(out), "--output", "/dev/null"]),
                          ("g24_visual_density.py", [str(out)]),
                          ("g25_wedo_variety.py", [str(out)]),
                          ("g28_cell_existence.py", [str(out)])):
            line, code = gate(script, a)
            rec["gates"][script.split("_")[0]] = {"line": line[:190], "exit": code}
        rec["g23Pass"] = "PASS" in rec["gates"]["g23"]["line"]
        rec["g18Pass"] = "BINDING=PASS" in rec["gates"]["g18"]["line"]
        rec["shipped"] = rec["g23Pass"] and rec["g18Pass"]
        if not rec["shipped"]:
            out.unlink(missing_ok=True)
    else:
        rec["shipped"] = False
        out.unlink(missing_ok=True)
    rec["out"] = str(out.relative_to(ROOT))
    rec["family"] = fam
    rec["week"] = week
    return rec


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--specs", required=True)
    ap.add_argument("--donors", required=True)
    ap.add_argument("--output")
    a = ap.parse_args()
    donors = json.loads(Path(a.donors).read_text())
    plans = json.loads((ROOT / "tools/easter/EASTER_TARGETS.json").read_text())["plans"]
    outdir = {"BUILD ASDAN": "BUILD_ASDAN/Autumn1_W1-W7_2026-27",
              "GROW ASDAN": "GROW_ASDAN/Autumn1_W1-W7_2026-27",
              "LAUNCH ASDAN": "LAUNCH_ASDAN/Autumn1_W1-W7_2026-27",
              "BUILD Humanities": "Humanities_Teesside/BUILD_W1-W8_2026-27",
              "GROW Humanities": "Humanities_Teesside/GROW_W1-W8_2026-27",
              "LAUNCH Humanities": "Humanities_Teesside/LAUNCH_W1-W8_2026-27"}
    recs = []
    for spec in json.loads(Path(a.specs).read_text()):
        if spec["family"] not in outdir:
            recs.append({"family": spec["family"], "week": spec["week"],
                         "shipped": False, "status": "NO PACK MAPPING"})
            continue
        try:
            recs.append(build_one(spec, donors, plans, outdir))
        except Exception as e:
            recs.append({"family": spec["family"], "week": spec["week"],
                         "shipped": False, "status": f"ERROR {e!r}"[:200]})
    for r in recs:
        mark = "ship" if r.get("shipped") else "PARK"
        print(f"  {mark} {r.get('family','?'):18s} wk{r.get('week','?'):<2} "
              f"leak={r.get('donorSentencesLeaked','-')} words={r.get('contentWords','-')} "
              f"{r.get('status','')}")
        if r.get("gates"):
            print(f"        g23 {'PASS' if r['g23Pass'] else 'RED'}  g18 {'PASS' if r['g18Pass'] else 'RED'}")
    print(f"\n{sum(1 for r in recs if r.get('shipped'))} of {len(recs)} shipped")
    if a.output:
        Path(a.output).parent.mkdir(parents=True, exist_ok=True)
        Path(a.output).write_text(json.dumps(recs, indent=1, default=str) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
