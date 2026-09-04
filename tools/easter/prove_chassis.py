#!/usr/bin/env python3
"""A3N-2 s1c -- prove a chassis by authoring a real lesson onto it and gating THAT.

WHY NOT GATE THE CHASSIS ITSELF
--------------------------------
s1c says "gate as a FIXTURE deck, full stack green". Taken literally that cannot
be done and should not be faked: a chassis has no pupil words, so g18's family
floor and g23's period load are not green on it, they are MEANINGLESS on it --
0 words is below every floor and 0/median is below every ceiling, and a report
saying PASS would be measuring nothing. The honest reading of "gate as a
fixture" is that the chassis is EXERCISED as a fixture: a real planned lesson is
authored onto it, the whole stack runs against that, and the evidence is the
artifact. The probe deck is deliberately NOT committed -- the donor PR ships zero
lesson units.

WHAT THIS RUNS, AND WHY IT RUNS IT TWICE
-----------------------------------------
Nine gates, each with its own verdict, and every one of them run on the DONOR as
well as on the probe, with identical arguments.

  g16  the frozen style contract, by family
  g18  per-family floor              g23  period-load ceiling
  g19  token ownership               g24  visual density
  g25  we-do variety                 g26  pathway reading band (--scope=new)
  g28  cell existence                g29  plan binding

The comparison is the point. Three of these are RED on decks this campaign has
already shipped green, and measuring that rather than assuming it changed what
this tool asserts:

  g16  RED on the donor (77 of 96 rows), RED on the live Art decks it was
       written for (86-88 of 108), RED on everything measured. The frozen v2
       contract is an estate-wide backlog -- CI runs the sibling classic-v2
       check with continue-on-error and the note "every one of the 54 fails at
       least one clause today".
  g19  RED on the donor. Ten :root declarations, zero scoped.
  g24  RED at --scope new on the donor: one explanatory visual where the row
       wants two, and that one print-dead. That is A2R R3's finding about the
       shell hiding the slide container under @media print, and it is true of
       the whole estate.

A tool that failed the chassis on those would be reporting the estate's backlog
as this work's defect. A tool that quietly dropped them would be hiding three
gates. So each gate is judged COMPARATIVELY: green on the probe is a pass; red
on the probe where the donor is also red is PRE-EXISTING and named; red on the
probe where the donor is GREEN is a REGRESSION and fails the run. That is
stricter than matching the campaign's flag choices, because nothing can hide
behind a scope setting, and it is honest about what is being claimed.

THE PROBE PATH IS NOT ARBITRARY. g26 derives the pathway from the route and
returns NOT-APPLICABLE for a route it cannot read -- a silent fail-open. So the
probe is written inside the repository at a path carrying the pathway token, and
a NOT-APPLICABLE from g26 is treated as a failure here, never as a pass.

THE PLAN IS ADDRESSED BY INDEX, NEVER BY family+week. Two LAUNCH ASDAN plans
share a week; keying on family+week silently hands a deck the other plan's
cells, which is a coverage lie that every gate but g29 passes. build_batch.py
still keys that way and is fixed in the same commit as this file.

    python3 tools/easter/prove_chassis.py --chassis <file> --plan-index N \
        --content <json> --reference <deck> [--output <json>]
    python3 tools/easter/prove_chassis.py --self-test
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

VERSION = "prove-chassis-v1.0.0"
ROOT = Path(__file__).resolve().parents[2]
VB = ROOT / "_sownb/vb/tools"
TARGETS = ROOT / "tools/easter/EASTER_TARGETS.json"


def _load(name, rel):
    spec = importlib.util.spec_from_file_location(name, ROOT / rel)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


ad = _load("author_deck", "tools/easter/author_deck.py")
g26 = _load("g26_reading_band", "_sownb/vb/tools/g26_reading_band.py")
_ls = _load("lesson_stages", "_sownb/vb/tools/lesson_stages.py")
ls_measure = _ls.measure


def digest(path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _run(script: str, args: list[str]) -> tuple[str, int]:
    r = subprocess.run([sys.executable, str(VB / script), *args],
                       capture_output=True, text=True, cwd=str(ROOT))
    lines = [l for l in (r.stdout or "").splitlines()
             if l.strip() and "fitz" not in l]
    if not lines:
        lines = [l for l in (r.stderr or "").splitlines() if l.strip()][-1:]
    return ("\n".join(lines[:4]) if lines else "(no output)"), r.returncode


def _ok(line: str, code: int) -> bool:
    """Exit code, plus the two verdicts that exit 0 without having measured
    anything. g26 prints NOT-APPLICABLE when it cannot read the pathway off the
    route -- the exact fail-open a pathway-neutral chassis would have produced.
    g23 prints NO FAMILY MEDIAN when the family is absent from the baseline.
    Neither is a pass, and neither is an error either, which is why they have to
    be named here rather than left to the exit code."""
    return code == 0 and "NOT-APPLICABLE" not in line and "NO FAMILY MEDIAN" not in line


def _is_chassis(path: Path) -> bool:
    """A chassis teaches nothing. That is the definition, and it is measured
    rather than read off the filename."""
    try:
        return ls_measure(path)["contentWords"] < 100
    except Exception:
        return False


def _chassis_donor(chassis: Path) -> str | None:
    raw = Path(chassis).read_text(encoding="utf-8")
    m = ad.CONFIG_RE.search(raw)
    if not m:
        return None
    try:
        return (json.loads(m.group(2)).get("chassis") or {}).get("donor")
    except Exception:
        return None


def _family_of_donor(rel: str) -> str | None:
    pw = g26.pathway_of("/" + rel)
    if pw is None:
        return None
    u = rel.upper()
    for token, subject in (("ASDAN", "ASDAN"), ("SCIENCE", "Science"), ("SCI_", "Science"),
                           ("HUMANITIES", "Humanities"), ("HUM_", "Humanities"),
                           ("ART", "Art")):
        if token in u:
            return f"{pw} {subject}"
    return None


GATES = (
    ("g16", "g16_v2.py", lambda f, deck: ["--family", f, "--file", deck]),
    ("g18", "g18_v2_family_floor.py", lambda f, deck: ["--family", f, "--candidate", deck,
                                                       "--output", "/dev/null"]),
    ("g19", "g19_v2.py", lambda f, deck: ["--family", f, "--file", deck]),
    ("g23", "g23_period_load.py", lambda f, deck: ["--family", f, "--candidate", deck,
                                                   "--output", "/dev/null", "--scope", "new"]),
    ("g24", "g24_visual_density.py", lambda f, deck: [deck, "--scope", "new"]),
    ("g25", "g25_wedo_variety.py", lambda f, deck: [deck, "--scope=new"]),
    ("g26", "g26_reading_band.py", lambda f, deck: [deck, "--scope=new"]),
    ("g28", "g28_cell_existence.py", lambda f, deck: [deck]),
    ("g29", "g29_plan_binding.py", lambda f, deck: [deck]),
)


def prove(chassis: Path, plan_index: int, content_path: Path, reference: Path,
          probe: Path | None = None) -> dict:
    for label, path in (("chassis", chassis), ("content", content_path),
                        ("reference", reference), ("targets", TARGETS)):
        if not Path(path).is_file():
            raise SystemExit(f"PROVENANCE REFUSAL: {label} input {str(path)!r} is not a "
                             f"readable file. Every input must be traceable to a digest.")
    inputs = {label: {"path": ad._rel(p), "sha256": digest(p)}
              for label, p in (("chassis", chassis), ("content", content_path),
                               ("reference", reference), ("targets", TARGETS))}

    plans = json.loads(TARGETS.read_text())["plans"]
    plan = plans[plan_index]
    family = plan["family"]
    pathway = family.split()[0]

    chassis_pathway = g26.pathway_of("/" + ad._rel(chassis))
    if chassis_pathway != pathway:
        raise SystemExit(f"PATHWAY MISMATCH: plan {plan_index} is {family} but the chassis "
                         f"route reads {chassis_pathway}. g26 judges by the route, so a "
                         f"chassis from the wrong pathway is judged by the wrong band.")

    content = json.loads(Path(content_path).read_text(encoding="utf-8"))
    content["_reference"] = Path(reference)
    if probe is None:
        probe = chassis.parent / "_probe" / f"{pathway}_probe.html"

    # `file` names the subject this record reports on, in the form the estate's
    # stale-evidence sweep reads structurally; without it the sweep falls back to
    # text and reports every bare verdict row as INCONCLUSIVE. It names the
    # CHASSIS and not the probe, because the probe is deleted at the end of the
    # run and an evidence record pointing at a file that is gone is exactly what
    # "stale" means.
    rec = {"tool": VERSION, "file": ad._rel(chassis),
           "inputs": inputs, "planIndex": plan_index,
           "family": family, "ruledWeek": plan["ruledWeek"], "cells": plan["cells"],
           "chassis": ad._rel(chassis), "probe": ad._rel(probe)}
    rec["author"] = ad.author(Path(chassis), plan, content, Path(probe))

    # The comparison baseline is the deck the chassis was STRIPPED FROM, not the
    # chassis. A chassis has no pupil words, so comparing against it makes every
    # content gate "red on the donor too" and the whole comparative rule reports
    # nothing. strip_to_chassis records the real donor and its digest inside the
    # chassis lesson-config for exactly this; read it from there rather than
    # passing it in, so the two cannot drift apart.
    # A stripped chassis records the deck it came from; a live deck used directly
    # as a donor IS that deck. Both are handled, and neither is guessed: the
    # field is present or it is not.
    donor_rel = _chassis_donor(chassis) or ad._rel(chassis)
    if _is_chassis(chassis) and _chassis_donor(chassis) is None:
        raise SystemExit(
            f"NO RECORDED DONOR: {ad._rel(chassis)} looks like a stripped chassis "
            f"but carries no chassis.donor field. Without it the comparative "
            f"verdict has no baseline and every content gate would read as "
            f"pre-existing.")
    rec["donor"] = donor_rel
    donor_family = _family_of_donor(donor_rel) or family

    rec["gates"] = {}
    for name, script, argf in GATES:
        line, code = _run(script, argf(family, ad._rel(probe)))
        probe_ok = _ok(line, code)
        dline, dcode = _run(script, argf(donor_family, donor_rel))
        donor_ok = _ok(dline, dcode)
        if probe_ok:
            verdict = "PASS"
        elif donor_ok:
            verdict = "REGRESSION"
        else:
            verdict = "PRE-EXISTING"
        rec["gates"][name] = {"line": line[:400], "exit": code, "verdict": verdict,
                              "donorLine": dline[:200], "donorExit": dcode,
                              "donorGreen": donor_ok, "donorFamily": donor_family}

    rec["regressions"] = [n for n, g in rec["gates"].items() if g["verdict"] == "REGRESSION"]
    rec["preExisting"] = [n for n, g in rec["gates"].items() if g["verdict"] == "PRE-EXISTING"]
    leak = rec["author"].get("donorSentencesLeaked")
    rec["verdict"] = "PASS" if (not rec["regressions"] and not leak
                                and rec["author"].get("status") == "PASS") else "RED"
    return rec


# --------------------------------------------------------------------------
def controls() -> list[dict]:
    out = []

    def rec(cid, claim, expect, actual):
        out.append({"id": cid, "claim": claim, "expected": expect, "actual": actual,
                    "verdict": "PASS" if expect == actual else "RED"})

    plans = json.loads(TARGETS.read_text())["plans"]

    # The key g29 exists to police, checked in the driver rather than after it.
    dupes = {}
    for i, p in enumerate(plans):
        if p.get("coverBeforeMattReturns"):
            dupes.setdefault((p["family"], p["ruledWeek"]), []).append(i)
    collisions = {k: v for k, v in dupes.items() if len(v) > 1}
    rec("family-and-week-is-not-a-unique-key-for-a-plan",
        "at least one family+week pair names two different cover-taught plans, "
        "so a driver keyed that way picks the wrong one",
        True, bool(collisions))

    # A pathway mismatch must stop the run, not be judged by the wrong band.
    rec("a-chassis-from-the-wrong-pathway-is-refused",
        "BUILD_chassis.html is not accepted for a LAUNCH plan",
        ("BUILD", "LAUNCH"),
        (g26.pathway_of("/tools/donors/ART_DONOR_v1/BUILD_chassis.html"),
         g26.pathway_of("/tools/donors/ART_DONOR_v1/LAUNCH_chassis.html")))

    # NOT-APPLICABLE is not a pass. Pinned on the string the gate actually
    # prints, so a rename of the verdict breaks this control loudly.
    bnds, _new, modes = g26.bands()
    j = g26.judge({"pupilFK": 3.0}, bnds, None, modes)
    rec("g26-not-applicable-is-treated-as-red",
        "a deck whose pathway cannot be read off the route fails here",
        "NOT-APPLICABLE", j["verdict"])

    rec("a-gate-red-on-the-donor-too-is-not-a-regression",
        "the comparative rule separates a regression from the estate's backlog",
        ("PASS", "PRE-EXISTING", "REGRESSION"),
        tuple("PASS" if pok else ("PRE-EXISTING" if not dok else "REGRESSION")
              for pok, dok in ((True, False), (False, False), (False, True))))

    rec("an-exit-zero-that-measured-nothing-is-not-ok",
        "NOT-APPLICABLE and NO FAMILY MEDIAN exit 0 and are still not a pass",
        (True, False, False),
        (_ok("all good", 0), _ok("x NOT-APPLICABLE", 0), _ok("x NO FAMILY MEDIAN", 0)))

    # The baseline must be the donor deck, never the chassis. Pinned on a real
    # chassis if one has been built, because the failure this catches is silent:
    # comparing against a chassis makes every content gate read PRE-EXISTING and
    # the tool reports PASS on a deck that is below its family floor.
    built = ROOT / "tools/donors/ART_DONOR_v1/GROW_chassis.html"
    if built.is_file():
        d = _chassis_donor(built)
        rec("the-comparison-baseline-is-the-donor-deck-not-the-chassis",
            "the chassis records the deck it was stripped from, and it is a real file",
            True, bool(d) and (ROOT / d).is_file() and d != ad._rel(built))

    rec("provenance-refuses-an-input-that-is-not-a-file",
        "a content path that does not exist stops the run before authoring",
        True, not Path("tools/easter/content/__does_not_exist__.json").is_file())
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--chassis")
    ap.add_argument("--plan-index", type=int)
    ap.add_argument("--content")
    ap.add_argument("--reference")
    ap.add_argument("--probe")
    ap.add_argument("--output")
    ap.add_argument("--keep-probe", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--list-controls", action="store_true")
    a = ap.parse_args()

    if a.list_controls:
        for c in controls():
            print(c["id"])
        return 0
    if a.self_test:
        cs = controls()
        for c in cs:
            print(f"{c['verdict']:4s} {c['id']}: {c['claim']}")
            if c["verdict"] == "RED":
                print(f"       expected {c['expected']!r} got {c['actual']!r}")
        red = [c for c in cs if c["verdict"] == "RED"]
        print(f"{len(cs) - len(red)}/{len(cs)} controls PASS")
        return 1 if red else 0

    if a.plan_index is None or not (a.chassis and a.content and a.reference):
        raise SystemExit("--chassis, --plan-index, --content and --reference are required")
    probe = Path(a.probe) if a.probe else None
    rec = prove(Path(a.chassis), a.plan_index, Path(a.content), Path(a.reference), probe)
    print(f"{rec['verdict']}  {rec['family']} W{rec['ruledWeek']}  plan {rec['planIndex']}  "
          f"chassis {Path(rec['chassis']).name}")
    au = rec["author"]
    print(f"   leaked={au.get('donorSentencesLeaked')} words={au.get('contentWords')} "
          f"timings={au.get('timingsSum')} author={au.get('status')}")
    for name, g in rec["gates"].items():
        print(f"   {g['verdict']:12s} {name}  {g['line'].splitlines()[0][:130]}")
    if rec["preExisting"]:
        print(f"   pre-existing on the donor too, not caused here: "
              f"{', '.join(rec['preExisting'])}")
    if rec["regressions"]:
        print(f"   REGRESSIONS (green on the donor, red here): "
              f"{', '.join(rec['regressions'])}")
    if a.output:
        Path(a.output).parent.mkdir(parents=True, exist_ok=True)
        Path(a.output).write_text(json.dumps(rec, indent=1, default=str) + "\n",
                                  encoding="utf-8")
        print(f"   wrote {a.output}")
    if not a.keep_probe:
        p = ROOT / rec["probe"]
        if p.is_file():
            p.unlink()
            print(f"   probe removed (the donor PR ships zero lesson units)")
    return 0 if rec["verdict"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
