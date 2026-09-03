#!/usr/bin/env python3
"""Plant a violation of every classic-v2 contract clause, show it fires, withdraw it.

A contract nobody has seen fail is a list of sentences. This runs each clause in
reshell_classic_v2_contract.py against a deck that satisfies every clause, then
against the same deck with exactly one clause broken, and requires the verdict to
move. A clause that cannot be made to red has not been tested; a clause that reds
the good deck too is not specific and is reported separately.

THE BASE IS A REAL DECK, NOT A FIXTURE. It is the landed
BUILD_HUM_W16_Then_And_Now_And_What_Is_Fair.html with its stage timings restored
-- the one clause it genuinely fails, because #271's reshell dropped nine
data-min values that summed to 40. Building the base from an invented fixture
would test the fixture. Building it from the real deck means every clause is
exercised against markup the estate actually ships.

DETERMINISM. --self-test runs the whole battery twice and compares the two
reports byte for byte. Nothing here may depend on a clock, a temp-file name, a
dict ordering or the order of a glob.

Usage:
  classic_v2_contract_selftest.py --self-test [--output report.json]
  classic_v2_contract_selftest.py --list-controls
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
VERSION = "classic-v2-contract-selftest-v1.0.0"

_spec = importlib.util.spec_from_file_location(
    "contract", ROOT / "_sownb/vb/tools/reshell_classic_v2_contract.py")
contract = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(contract)

BASE_DECK = ROOT / "Humanities_Teesside/BUILD_W14-W20_2026-27/BUILD_HUM_W16_Then_And_Now_And_What_Is_Fair.html"

# The nine n6 stage minutes #271 dropped, plus 0 for the classic title slide.
# Recorded here because the base deck no longer carries them; the repair itself
# belongs to a lesson PR, not to a selftest.
RESTORED_MINUTES = [0, 0, 3, 3, 4, 3, 3, 4, 16, 4]


def _passing_base() -> str:
    """The real deck with its timings restored: every clause must pass."""
    raw = BASE_DECK.read_text(encoding="utf-8")
    it = iter(RESTORED_MINUTES)

    def stamp(m):
        try:
            return m.group(0) + f' data-min="{next(it)}"'
        except StopIteration:
            return m.group(0)

    return re.sub(r'<div class="slide(?: active)?"', stamp, raw)


# Each mutation breaks exactly one clause. The mutation is a function so that a
# clause whose violation needs more than a string swap can still be expressed.
def _break_own_config(raw):
    return raw.replace('id="lesson-config"', 'id="lesson-config-removed"', 1)


def _break_donor_head(raw):
    return raw.replace(
        'BUILD Humanities · Week 16 · Then and now, and what is fair',
        'BUILD Humanities · Week 6 · Plan the story', 1)


def _break_two_modals(raw):
    return raw.replace('id="mbmTA"', 'id="mbmTA"', 1).replace(
        "</body>", '<div id="mbmTA"></div></body>', 1)


def _break_hud(raw):
    return raw.replace("hud.js", "hud-REMOVED.js")


def _break_lundy(raw):
    out = raw.replace('data-title="Lundy Loop"', 'data-title="Reflection"')
    out = out.replace('id="print-lundy"', 'id="print-reflection"')
    for word in ("Space", "Voice", "Audience", "Influence",
                 "space", "voice", "audience", "influence"):
        out = out.replace(word, "Aspect" if word[0].isupper() else "aspect")
    return out


def _break_tiers(raw):
    return raw.replace('id="print-scaffold-stretch"', 'id="print-scaffold-extra"').replace(
        'id="print-worksheet-stretch"', 'id="print-worksheet-extra"')


def _break_surfaces(raw):
    """Push past the 25-surface ceiling. Anchored on </body>, which every deck
    has, rather than on a closing-div pair that happens to differ per deck --
    the first version of this mutation silently did nothing and the control
    reported PASS -> PASS, which is how a selftest lies."""
    extra = "".join(
        f'<div class="print-section" id="print-padding-{i}"><p>padding</p></div>'
        for i in range(6))
    return raw.replace("</body>", extra + "</body>", 1)


def _break_timings(raw):
    return re.sub(r'\sdata-min="\d+"', "", raw)


def _break_root_blocks(raw):
    return raw.replace(":root{", ":root{--planted-second:1}\n:root{", 1)


def _break_print_inside_main(raw):
    """Move the print pack inside main, which is the double-count shape.

    Done on the tree, not with a regex over the text: #print-area is tens of
    kilobytes of nested markup and no regex reliably finds its closing tag."""
    from lxml import html as _lh
    tree = _lh.fromstring(raw)
    area = tree.xpath('//*[@id="print-area"]')
    main = tree.xpath("//main")
    if not area or not main:
        return raw
    node = area[0]
    node.getparent().remove(node)
    main[0].append(node)
    return _lh.tostring(tree, encoding="unicode", doctype="<!DOCTYPE html>")


MUTATIONS = [
    ("own-lesson-config-only", _break_own_config,
     "the deck's own lesson-config is removed, so coverage cannot be counted"),
    ("no-donor-running-head", _break_donor_head,
     "one running head names the DONOR's week and title instead of this lesson's"),
    ("exactly-one-target-modal", _break_two_modals,
     "a second TA modal is added, so one of them can never open"),
    ("hud-js-present", _break_hud,
     "the hud.js tag is renamed, making the route unreachable from the hub"),
    ("lundy-in-three-places", _break_lundy,
     "the Lundy slide, its print section and its four dimensions are all renamed away"),
    ("three-tier-print-pack", _break_tiers,
     "the stretch tier is renamed, leaving supported and standard only"),
    ("surfaces-in-range", _break_surfaces,
     "six padding print sections push the deck past the 25-surface ceiling"),
    ("stage-timings-carried", _break_timings,
     "every data-min is stripped, exactly as #271's reshell did"),
    ("one-root-block", _break_root_blocks,
     "a second :root block is planted, against the RUN12-A ruling"),
    ("print-pack-outside-main", _break_print_inside_main,
     "the print pack is moved inside main, where the word count would read it twice"),
]


def _evaluate(source: str) -> dict:
    with tempfile.TemporaryDirectory() as tmp:
        p = Path(tmp) / "deck.html"
        p.write_text(source, encoding="utf-8")
        return {c["clause"]: c["status"] for c in contract.evaluate(p)}


def list_controls() -> list[str]:
    return [cid for cid, _, _ in MUTATIONS]


def run() -> dict:
    base_src = _passing_base()
    base = _evaluate(base_src)

    declared = contract.list_controls()
    order_ok = list(base.keys()) == declared
    base_reds = sorted(k for k, v in base.items() if v == "RED")

    results = []
    for cid, mutate, description in MUTATIONS:
        mutated = _evaluate(mutate(base_src))
        fired = base.get(cid) == "PASS" and mutated.get(cid) == "RED"
        collateral = sorted(k for k, v in mutated.items()
                            if v == "RED" and k != cid and base.get(k) == "PASS")
        results.append({
            "clause": cid, "planted": description,
            "baseVerdict": base.get(cid), "mutatedVerdict": mutated.get(cid),
            "fired": fired, "collateralReds": collateral,
        })

    return {
        "tool": "classic_v2_contract_selftest", "toolVersion": VERSION,
        "contractVersion": contract.VERSION,
        "baseDeck": str(BASE_DECK.relative_to(ROOT)),
        "baseDeckNote": ("the landed deck with the nine stage timings #271 dropped "
                         "restored in memory, so that every clause can start from PASS"),
        "clausesDeclared": len(declared),
        "clauseOrderMatchesContract": order_ok,
        "baseReds": base_reds,
        "controlsRun": len(results),
        "controlsFired": sum(1 for r in results if r["fired"]),
        "allListedControlsFired": (order_ok and not base_reds
                                   and all(r["fired"] for r in results)),
        "controls": results,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--list-controls", action="store_true")
    ap.add_argument("--output")
    a = ap.parse_args()

    if a.list_controls:
        for c in list_controls():
            print(c)
        return 0

    first = json.dumps(run(), indent=1, sort_keys=True)
    second = json.dumps(run(), indent=1, sort_keys=True)
    deterministic = first == second
    report = json.loads(first)
    report["deterministic"] = deterministic
    report["runDigest"] = hashlib.sha256(first.encode()).hexdigest()

    print(f"classic-v2 contract selftest  [{VERSION}] against {contract.VERSION}")
    print(f"  base deck: {report['baseDeck']}")
    if report["baseReds"]:
        print(f"  BASE IS NOT CLEAN, so no clause starts from PASS: {report['baseReds']}")
    for r in report["controls"]:
        mark = "ok  " if r["fired"] else "FAIL"
        extra = f"  collateral={r['collateralReds']}" if r["collateralReds"] else ""
        print(f"  {mark} {r['clause']:26s} {r['baseVerdict']} -> {r['mutatedVerdict']}{extra}")
    print(f"  {report['controlsFired']}/{report['controlsRun']} controls fired; "
          f"clause order matches the contract: {report['clauseOrderMatchesContract']}")
    print(f"  deterministic (two runs byte-identical): {deterministic}  "
          f"digest {report['runDigest'][:16]}")

    ok = report["allListedControlsFired"] and deterministic
    if a.output:
        out = ROOT / a.output if not Path(a.output).is_absolute() else Path(a.output)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(report, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    print("PASS" if ok else "MEASUREMENT INVALID")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
