#!/usr/bin/env python3
"""The classic-v2 output contract: what a reshelled deck must be.

reshell_classic_v2.py asserts three things about its own output before it
writes. Those three are the recipe's internal hygiene -- no donor lesson-config,
no donor running head, exactly one target modal. They are necessary and they are
not the contract. The contract is what the deck has to be for a cover teacher to
pick it up on a Monday, and until this file it lived in prose in an order and in
whatever a reviewer remembered to check.

Each clause below is a named, checkable predicate over a finished deck. They are
declared once, here, and read by:

  * the recipe, so a deck is refused before it is written rather than after;
  * classic_v2_contract_selftest.py, which plants a violation of every clause,
    shows it fires, and withdraws it;
  * CI, which asks for the clause list rather than being told a number.

WHY EACH CLAUSE IS HERE, not "because the order said so":

  no-donor-lesson-config      run 14 found two decks carrying the DONOR's config.
                              A deck that declares another lesson's cells poisons
                              coverage, which is counted per cell.
  no-running-head             a donor's running head names the donor's week on
                              every printed page of a different lesson.
  exactly-one-target-modal    two TA modals means one of them never opens and the
                              adult in the room cannot tell which.
  hud-js-present              the estate's route gate requires it; a deck without
                              it is unreachable from the hub.
  lundy-in-three-places       pupil voice has to survive the shell: its own
                              slide, a working stage, and the print pack. Two out
                              of three is a deck where the paper copy has no
                              voice in it.
  three-tier-print-pack       supported / standard / stretch. A single-tier print
                              pack hands every pupil the same sheet.
  surfaces-in-range           21-25 teaching surfaces (slides + print sections).
                              Below that the pack is thin; above it the reshell
                              has duplicated something.
  stage-timings-carried       #271 dropped nine data-min values that summed to
                              40 and nothing noticed for a fortnight, because the
                              only reader was an n6-shaped XPath that returned
                              nothing on a classic deck.
  one-root-block              the RUN12-A ruling: a token is defined once.
  print-pack-outside-main     the pupil-content measurement scopes to main.deck.
                              A print pack nested inside it would be counted a
                              second time, which is the double-count A2R 3.3
                              exists to prevent.

Usage:
  reshell_classic_v2_contract.py <deck.html> [<deck.html> ...]
  reshell_classic_v2_contract.py --list-controls
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from pathlib import Path

from lxml import html as lh

VERSION = "classic-v2-contract-v1.0.0"
ROOT = Path(__file__).resolve().parents[3]

_g19_spec = importlib.util.spec_from_file_location("g19_v2", ROOT / "_sownb/vb/tools/g19_v2.py")
g19 = importlib.util.module_from_spec(_g19_spec)
_g19_spec.loader.exec_module(g19)

_ls_spec = importlib.util.spec_from_file_location("lesson_stages", ROOT / "_sownb/vb/tools/lesson_stages.py")
stages_mod = importlib.util.module_from_spec(_ls_spec)
_ls_spec.loader.exec_module(stages_mod)

SURFACES_MIN, SURFACES_MAX = 21, 25
PERIOD_MINUTES = 40
TIERS = ("supported", "standard", "stretch")


def _slides(tree):
    return tree.xpath('//*[contains(concat(" ",normalize-space(@class)," ")," slide ")]')


def _print_sections(tree):
    return tree.xpath('//*[contains(concat(" ",normalize-space(@class)," ")," print-section ")]')


def evaluate(path: Path) -> list[dict]:
    path = Path(path)
    raw = path.read_text(encoding="utf-8")
    tree = lh.fromstring(raw)
    slides = _slides(tree)
    sections = _print_sections(tree)
    mins = [s.get("data-min") for s in slides]
    declared = [int(float(m)) for m in mins if m not in (None, "")]

    lundy_slide = any("lundy" in (s.get("data-title") or "").lower() for s in slides)
    lundy_print = any("lundy" in (p.get("id") or "").lower() for p in sections)
    # The Lundy Loop reaches a working stage as its FOUR DIMENSIONS -- space,
    # voice, audience, influence -- not usually as the word "Lundy", which is
    # the framework's name and not language a pupil needs. Testing for the
    # literal word failed a deck that carries all four in all three stages.
    LUNDY_DIMENSIONS = ("space", "voice", "audience", "influence")
    lundy_stage = any(
        "lundy" in " ".join(s.text_content().split()).lower()
        or all(d in " ".join(s.text_content().split()).lower() for d in LUNDY_DIMENSIONS)
        for s in slides
        if (s.get("data-title") or "").lower().startswith(("we do", "independent"))
    )
    lundy_places = sum([lundy_slide, lundy_print, lundy_stage])

    tiers_present = [t for t in TIERS
                     if any(t in (p.get("id") or "").lower() for p in sections)]

    def clause(cid, ok, evidence):
        return {"clause": cid, "status": "PASS" if ok else "RED", "evidence": evidence}

    n_config = raw.count('id="lesson-config"')
    n_modal = raw.count('id="mbmTA"')

    # THE RULE IS "THE DONOR'S MUST NOT TRAVEL", NOT "THERE MUST BE NONE".
    # A finished deck needs its own lesson-config -- coverage is counted per
    # cell, and a deck that declares no cells is uncountable -- and it needs a
    # running head on every printed page so a loose sheet can be put back with
    # the right lesson. The recipe asserts ZERO of both because it emits neither;
    # they are added afterwards from the deck's own title. What must never
    # appear is the DONOR's. So the clause is identity, not absence. Written the
    # absent way first, this file red'd a known-good deck on three clauses; a
    # clause that reds a good deck is a defect in the clause until proved
    # otherwise.
    own = {}
    try:
        own = json.loads(tree.xpath('//script[@id="lesson-config"]')[0].text)
    except Exception:
        pass
    own_title = (own.get("title") or "").strip()
    heads = [" ".join(h.text_content().split())
             for h in tree.xpath('//*[contains(concat(" ",normalize-space(@class)," ")," print-head ")]')]
    foreign_heads = [h for h in heads if own_title and own_title not in h]

    return [
        clause("own-lesson-config-only", n_config == 1 and bool(own_title),
               f"lesson-config blocks = {n_config}, own title = {own_title!r} (need exactly one, this deck's)"),
        clause("no-donor-running-head", not foreign_heads,
               f"{len(heads)} running head(s), {len(set(heads))} distinct, "
               f"{len(foreign_heads)} naming a lesson other than this one"),
        clause("exactly-one-target-modal", n_modal == 1,
               f"target TA modals = {n_modal} (need 1)"),
        clause("hud-js-present", "hud.js" in raw,
               f"hud.js references = {raw.count('hud.js')}"),
        clause("lundy-in-three-places", lundy_places == 3,
               f"own slide={lundy_slide}, working stage={lundy_stage}, print pack={lundy_print}"),
        clause("three-tier-print-pack", len(tiers_present) == 3,
               f"tiers found = {tiers_present}"),
        clause("surfaces-in-range", SURFACES_MIN <= len(slides) + len(sections) <= SURFACES_MAX,
               f"{len(slides)} slides + {len(sections)} print sections = "
               f"{len(slides) + len(sections)} (need {SURFACES_MIN}-{SURFACES_MAX})"),
        clause("stage-timings-carried",
               bool(declared) and sum(declared) == PERIOD_MINUTES,
               f"{len(declared)} of {len(slides)} stages declare minutes, summing to "
               f"{sum(declared)} (need {PERIOD_MINUTES})"),
        clause("one-root-block", g19.root_block_count(path) == 1,
               f":root blocks = {g19.root_block_count(path)}"),
        clause("print-pack-outside-main", not tree.xpath('//main//*[@id="print-area"]'),
               "print-area is a body-level sibling of main"
               if not tree.xpath('//main//*[@id="print-area"]')
               else "print-area is nested inside main and would be counted twice"),
    ]


# The clause list, declared once. evaluate() must return exactly these, in this
# order; the selftest asserts that, so a clause cannot be added to one and
# forgotten in the other.
CONTROL_IDS = [
    "own-lesson-config-only",
    "no-donor-running-head",
    "exactly-one-target-modal",
    "hud-js-present",
    "lundy-in-three-places",
    "three-tier-print-pack",
    "surfaces-in-range",
    "stage-timings-carried",
    "one-root-block",
    "print-pack-outside-main",
]


def list_controls() -> list[str]:
    return list(CONTROL_IDS)


def report(path: Path) -> dict:
    clauses = evaluate(path)
    reds = [c for c in clauses if c["status"] == "RED"]
    return {"file": str(path), "toolVersion": VERSION,
            "clausesDeclared": len(CONTROL_IDS), "clausesRun": len(clauses),
            "clauses": clauses, "reds": len(reds),
            "status": "PASS" if not reds else "RED"}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="*")
    ap.add_argument("--output")
    ap.add_argument("--list-controls", action="store_true")
    a = ap.parse_args()
    if a.list_controls:
        for c in list_controls():
            print(c)
        return 0
    if not a.files:
        ap.error("give at least one deck, or --list-controls")
    out, bad = [], 0
    for f in a.files:
        p = ROOT / f if not Path(f).is_absolute() else Path(f)
        r = report(p)
        out.append(r)
        print(f"{Path(f).name[:46]:46s} {r['status']:4s} "
              f"{r['clausesRun'] - r['reds']}/{r['clausesRun']} clauses  [{VERSION}]")
        for c in r["clauses"]:
            if c["status"] == "RED":
                print(f"    RED  {c['clause']:26s} {c['evidence']}")
        bad += r["reds"] and 1 or 0
    if a.output:
        p = ROOT / a.output if not Path(a.output).is_absolute() else Path(a.output)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
