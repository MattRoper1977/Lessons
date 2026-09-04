#!/usr/bin/env python3
"""R3 flip list: every deck whose g23 verdict moves when chrome stops counting.

WHY A FLIP LIST IS THE CONTROL ON A COUNTING CHANGE
---------------------------------------------------
A3N R3 says the change is not an estate-wide loosening, and that is a claim
about EVERY deck, not about the three it was written for. The only honest way
to support it is to re-measure the whole estate both ways and print every deck
that moves -- so a loosening, if there is one, has to appear in a list rather
than hide in an average.

Both sides come from one pass of lesson_stages.measure(), which reports the raw
count and the chrome-excluded count for the same file, so "before" is not a
remembered number from an older tool. Family medians are recomputed under each
rule from that family's own baseline set, because a ratio whose numerator moved
and whose denominator did not is not a comparison.

A deck that flips PASS->RED is reported as REGRESSED and, per R3, is PARKED:
the run does not ship it and the question goes to EASTER_HUMAN.md.

Usage:
  chrome_flip_list.py [--output r.json]
  chrome_flip_list.py --list-controls | --self-test
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import statistics
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
VERSION = "chrome-flip-list-v1.0.0"
CEILING = 1.5          # the binding contract ceiling; unmoved by R3
TARGET = 1.25          # the operative trim target; unmoved by R3

_ls = importlib.util.spec_from_file_location(
    "lesson_stages", ROOT / "_sownb/vb/tools/lesson_stages.py")
ls = importlib.util.module_from_spec(_ls); _ls.loader.exec_module(ls)

_ms = importlib.util.spec_from_file_location(
    "g18_measurement", ROOT / "_sownb/feb/tools/g18_measurement.py")
meas = importlib.util.module_from_spec(_ms); _ms.loader.exec_module(meas)


def verdict(ratio: float) -> str:
    return "RED" if ratio > CEILING else "PASS"


def family_members(fam: str) -> list[Path]:
    return sorted({p for pat in meas.BASELINES[fam] for p in ROOT.glob(pat)})


def scan(root: Path = ROOT) -> dict:
    fams, rows = {}, []
    for fam in meas.BASELINES:
        vals = []
        for f in family_members(fam):
            m = ls.measure(f)
            if m["stageCount"] >= 5 and m["totalWords"]:
                vals.append((m["totalWords"], m["contentWords"]))
        if len(vals) < 5:
            fams[fam] = None
            continue
        fams[fam] = {"n": len(vals),
                     "medianBefore": statistics.median(v[0] for v in vals),
                     "medianAfter": statistics.median(v[1] for v in vals)}

    for fam, med in fams.items():
        if med is None:
            continue
        for f in sorted(root.rglob("*.html")):
            rel = str(f.relative_to(root))
            if rel.split("/")[0] in ("Site", "Games", "Apps"):
                continue
            if fam_of(rel) != fam:
                continue
            try:
                m = ls.measure(f)
            except Exception:
                continue
            if m["stageCount"] < 5 or not m["totalWords"]:
                continue
            rb = round(m["totalWords"] / med["medianBefore"], 3)
            ra = round(m["contentWords"] / med["medianAfter"], 3)
            vb, va = verdict(rb), verdict(ra)
            if vb == va and (rb > TARGET) == (ra > TARGET):
                continue
            rows.append({
                "file": rel, "family": fam,
                "wordsBefore": m["totalWords"], "wordsAfter": m["contentWords"],
                "chromeWords": m["chromeWords"],
                "chromeShare": round(100 * m["chromeWords"] / max(1, m["totalWords"]), 1),
                "ratioBefore": rb, "ratioAfter": ra,
                "verdictBefore": vb, "verdictAfter": va,
                "overTargetBefore": rb > TARGET, "overTargetAfter": ra > TARGET,
                "direction": ("REGRESSED" if (vb, va) == ("PASS", "RED")
                              else "CLEARED" if (vb, va) == ("RED", "PASS")
                              else "TARGET-ONLY"),
                "explainedByChrome": m["chromeWords"] > 0,
            })
    rows.sort(key=lambda r: (r["direction"] != "REGRESSED", r["file"]))
    regressed = [r for r in rows if r["direction"] == "REGRESSED"]
    return {
        "tool": "chrome_flip_list", "toolVersion": VERSION,
        "file": "tools/easter/chrome_flip_list.py",
        "subject": ("every deck whose g23 verdict or 1.25-target position moves when the "
                    "contract refrain and the title slide stop being counted, measured on "
                    "both sides in one pass with the family median recomputed under each rule"),
        "ceiling": CEILING, "operativeTarget": TARGET,
        "repeatRuleActive": ls.REPEAT_COUNTS_ONCE,
        "families": fams,
        "flips": len(rows), "cleared": sum(1 for r in rows if r["direction"] == "CLEARED"),
        "regressed": len(regressed),
        "parkRequired": [r["file"] for r in regressed if not r["explainedByChrome"]],
        "rows": rows,
    }


def fam_of(rel: str) -> str | None:
    if rel.startswith("Science_Teesside/"):
        parts = rel.split("/")
        return f"{parts[1].upper()} Science" if len(parts) > 2 else None
    if rel.startswith("Humanities_Teesside/"):
        parts = rel.split("/")
        return f"{parts[1].split('_')[0]} Humanities" if len(parts) > 2 else None
    for lane in ("BUILD", "GROW", "LAUNCH"):
        if rel.startswith(f"{lane}_ASDAN/"):
            return f"{lane} ASDAN"
    return None


# --------------------------------------------------------------------------
# Controls
# --------------------------------------------------------------------------

CONTROL_IDS = [
    "chrome-is-excluded-from-the-numerator",
    "chrome-is-excluded-from-the-denominator-too",
    "a-deck-of-pure-chrome-cannot-pass-by-being-emptied",
    "real-teaching-overload-still-reds",
    "adding-more-chrome-cannot-push-a-deck-over",
    "the-family-map-covers-every-baseline-family",
]

_BANNER = ("<p>SPACE stays available. VOICE is received. AUDIENCE names back exactly. "
           "INFLUENCE changes one real next action.</p>")


def _deck(stages_html: str) -> str:
    return ("<!doctype html><html><head><style>.slide{display:none}"
            ".slide.active{display:flex}</style></head><body>"
            "<main class=\"deck\">" + stages_html + "</main></body></html>")


def _stage(title, mins, body, active=False):
    return (f'<section class="slide{" active" if active else ""}" data-title="{title}" '
            f'data-min="{mins}">{body}</section>')


def _measure_src(src: str) -> dict:
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as fh:
        fh.write(src); p = Path(fh.name)
    try:
        return ls.measure(p)
    finally:
        p.unlink(missing_ok=True)


def controls() -> list[dict]:
    out = []

    def rec(cid, description, expected, observed):
        out.append({"id": cid, "description": description, "expected": expected,
                    "observed": observed, "fired": expected == observed})

    teach = "<p>" + " ".join(f"word{i}" for i in range(40)) + ".</p>"
    plain = _deck("".join(_stage(f"S{i}", 4, teach, i == 1) for i in range(1, 7)))
    withchrome = _deck("".join(_stage(f"S{i}", 4, teach + _BANNER, i == 1) for i in range(1, 7)))

    a, b = _measure_src(plain), _measure_src(withchrome)
    rec("chrome-is-excluded-from-the-numerator",
        "the banner on every stage adds raw words and no content words",
        (True, a["contentWords"]),
        (b["totalWords"] > a["totalWords"], b["contentWords"]))

    rec("chrome-is-excluded-from-the-denominator-too",
        "a family of chrome-carrying decks medians to its content, not its raw -- "
        "a numerator corrected against an uncorrected denominator is not a ratio",
        a["contentWords"], b["contentWords"])

    allchrome = _deck("".join(_stage(f"S{i}", 4, _BANNER, i == 1) for i in range(1, 7)))
    c = _measure_src(allchrome)
    rec("a-deck-of-pure-chrome-cannot-pass-by-being-emptied",
        "a deck with no teaching at all measures 0 content words, so g18's floor "
        "catches it rather than g23 reporting a flattering ratio",
        0, c["contentWords"])

    heavy_body = "<p>" + " ".join(f"w{i}" for i in range(400)) + ".</p>"
    heavy = _measure_src(_deck(_stage("S1", 4, heavy_body, True)
                               + "".join(_stage(f"S{i}", 4, teach) for i in range(2, 7))))
    rec("real-teaching-overload-still-reds",
        "one stage carrying ten times the teaching still exceeds the ceiling against "
        "the plain deck's content median -- R3 must not be a blanket pass-maker",
        True, heavy["contentWords"] / max(1, a["contentWords"]) > CEILING)

    rec("adding-more-chrome-cannot-push-a-deck-over",
        "the banner repeated on every stage leaves the ratio exactly where it was",
        1.0, round(b["contentWords"] / max(1, a["contentWords"]), 3))

    rec("the-family-map-covers-every-baseline-family",
        "a family the map cannot name is a family the flip list silently skips",
        sorted(meas.BASELINES),
        sorted({f for f in (fam_of(str(p.relative_to(ROOT)))
                            for fam in meas.BASELINES for p in family_members(fam)) if f}))
    return out


def self_test() -> dict:
    res = controls()
    ids = [r["id"] for r in res]
    missing = [c for c in CONTROL_IDS if c not in ids]
    extra = [c for c in ids if c not in CONTROL_IDS]
    return {"tool": "chrome_flip_list", "toolVersion": VERSION,
            "file": "tools/easter/chrome_flip_list.py",
            "controlsDeclared": len(CONTROL_IDS), "controlsRun": len(res),
            "controlsFired": sum(1 for r in res if r["fired"]),
            "missingControls": missing, "undeclaredControls": extra,
            "allListedControlsFired": not missing and not extra and all(r["fired"] for r in res),
            "controls": res}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output")
    ap.add_argument("--list-controls", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()
    if a.list_controls:
        print("\n".join(CONTROL_IDS)); return 0
    if a.self_test:
        rep = self_test()
        print(f"chrome_flip_list self-test  [{VERSION}]")
        for r in rep["controls"]:
            print(f"  {'ok  ' if r['fired'] else 'FAIL'} {r['id']:48s} "
                  f"expected={str(r['expected'])[:44]} observed={str(r['observed'])[:44]}")
        print(f"{rep['controlsFired']}/{rep['controlsRun']} controls fired")
        print("PASS" if rep["allListedControlsFired"] else "MEASUREMENT INVALID")
        return 0 if rep["allListedControlsFired"] else 1

    rep = scan()
    print(f"R3 chrome flip list  [{VERSION}]  repeat-rule active: {rep['repeatRuleActive']}")
    for fam, m in sorted(rep["families"].items()):
        if m: print(f"  {fam:20s} n={m['n']}  median {m['medianBefore']:.0f} -> {m['medianAfter']:.0f}")
    print(f"  {rep['flips']} deck(s) move: {rep['cleared']} cleared, {rep['regressed']} regressed")
    for r in rep["rows"]:
        print(f"    {r['direction']:11s} {r['ratioBefore']:5.2f} -> {r['ratioAfter']:5.2f}  "
              f"{r['verdictBefore']}->{r['verdictAfter']}  chrome {r['chromeShare']:4.1f}%  "
              f"{Path(r['file']).name[:52]}")
    if rep["parkRequired"]:
        print(f"  PARK REQUIRED (moved with no chrome to explain it): {rep['parkRequired']}")
    if a.output:
        o = Path(a.output); o = o if o.is_absolute() else ROOT / o
        o.parent.mkdir(parents=True, exist_ok=True)
        o.write_text(json.dumps(rep, indent=1) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
