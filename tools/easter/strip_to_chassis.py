#!/usr/bin/env python3
"""A3N-2 s1b -- strip a green deck to its chassis, so Art can be authored onto it.

WHAT A CHASSIS IS, HERE
-----------------------
Everything a gate reads that is NOT a teaching decision: the nine-stage spine,
per-stage data-min, the Lundy strip in its three places, the guide toggle and
its staff drawer, the print pack's page and tier structure, the splash, the
progress control, the running head, the navigation, and a lesson-config with
every donor field replaced by a placeholder.

Everything else goes. "Everything else" is not a list of block names -- s1b
says remove ALL subject content, and a list of names is a list of what the
author remembered. So the strip is SUBTRACTIVE and then VERIFIED against the
donor's own text: after stripping, not one sentence of the donor may survive
anywhere in the whole document, print pack and staff drawer included.

WHAT COUNTS AS FURNITURE, AND WHY IT IS NOT A LIST
--------------------------------------------------
Some text in a deck is neither teaching nor decoration: the Lundy refrain, the
long-form Lundy status statement, the print pack's labels. Deleting it breaks
the contract; keeping the donor's version of it leaks the donor. The line
between them is drawn the same way the authoring pipeline already draws it and
NOT by naming blocks: a text block is FURNITURE when it appears verbatim in
reference decks from two or more different families. One family sharing a
phrase is a house style; two families sharing it is the chassis.

WHY THE DONOR'S STAGE DIAGRAMS GO
----------------------------------
author_deck.KEEP_TAGS keeps a bare <svg> child of a stage, which was right for
icons and wrong for figures: the donor's two explanatory diagrams are direct
children of their stages and carried its labels ("A routine in order / Step 1
needs nothing first") straight through the strip. No shipped deck was affected
-- every one of the sixteen carries its own two figures and the donor it came
from had none at that position -- but a chassis that kept them would have put
one donor's diagram on every Art lesson. They are removed here, and
author_deck.empty_stage no longer keeps a bare svg either.

WHY THE PRINT PACK IS EMPTIED RATHER THAN DELETED
--------------------------------------------------
author_deck.author_print_pack rewrites the pack BY ROLE -- it fills the h1, the
labelled <p><b>Objective:</b> paragraphs, the <li> success criteria, the first
table column, the tier routes. Delete those elements and there is nothing to
fill, and the authored deck ships a pack with no criteria. So each element is
kept as an empty shell with its <b> label intact, and only its prose is removed.

WHAT THIS TOOL DOES NOT CLAIM
------------------------------
A chassis has no pupil words, so it cannot pass g18's family floor or g23's
period load -- gates that measure content on a thing with no content are not
green, they are meaningless. The chassis is proven by AUTHORING a probe deck
onto it and running the full stack on that, which is what s1c's "gate as a
fixture deck" can honestly mean. This tool reports the structural facts; the
proof run is prove_chassis.py.

    python3 tools/easter/strip_to_chassis.py --donor <file> --out <file> --id <id>
    python3 tools/easter/strip_to_chassis.py --self-test
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
from pathlib import Path

import lxml.html as lh

VERSION = "strip-to-chassis-v1.0.0"
ROOT = Path(__file__).resolve().parents[2]


def _load(name: str, rel: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / rel)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


ad = _load("author_deck", "tools/easter/author_deck.py")
ls = _load("lesson_stages", "_sownb/vb/tools/lesson_stages.py")
pad = _load("pick_art_donor", "tools/easter/pick_art_donor.py")
REFERENCE = ROOT / "tools/easter/GREEN_REFERENCE_DECKS.json"

CONFIG_RE = ad.CONFIG_RE
PLACEHOLDER = ""


def digest(path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _clear(el) -> None:
    """Empty an element's prose while keeping the element and any <b> label,
    because the authoring step writes INTO these shells."""
    keep = [k for k in el if isinstance(k.tag, str) and k.tag.lower() == "b"]
    for k in list(el):
        if k not in keep:
            el.remove(k)
    el.text = None
    for k in keep:
        k.tail = None


# Every block-level leaf, plus <span>, which carries text and is not a block.
# The first version listed twelve tag names and missed <header> -- which is what
# the LAUNCH chassis generation uses for its running head -- so that chassis
# shipped "LAUNCH ASDAN . Week 1 . ASDAN cross-strand . Choose Our Community
# Need" as the running head of every Art lesson built from it. A list of tags is
# a list of what the author remembered; take the set the measuring instrument
# already uses instead.
TEXT_TAGS = tuple(sorted(ls.BLOCK_TAGS | {"span"}))

# Interactive labels. A control surface reads as prose to any word counter --
# the deck's own navigation is fifteen words of "Previous / Teacher tools /
# Evidence & print / Calm mode / Static diagrams / Next" -- and every chassis
# generation in this estate names those buttons differently, so it is never
# shared text between two families and a shared-text rule alone calls it a
# donor leak. It is not: it is the UI, s1b keeps navigation, and stripping the
# labels leaves a row of blank buttons.
#
# Discriminated by STRUCTURE, not by element name or class: an element is a
# control surface when every word it shows comes from an interactive child.
# A <div> of buttons qualifies; a <nav> with a paragraph of teaching in it
# does not, and would still be swept and still be flagged.
INTERACTIVE = ("button", "a", "label", "summary", "option", "select", "input")


def is_control_surface(el) -> bool:
    text = " ".join((el.text_content() or "").split())
    if not text:
        return False
    own = " ".join((el.text or "").split())
    from_controls = []
    for kid in el.iter():
        if kid is el:
            continue
        if isinstance(kid.tag, str) and kid.tag.lower() in INTERACTIVE:
            from_controls.append(" ".join((kid.text_content() or "").split()))
            from_controls.append(" ".join((kid.tail or "").split()))
    if own:
        return False
    # Compare CHARACTERS, not words. <div><button>Previous</button><button>Next
    # </button></div> has text_content "PreviousNext" -- one word to any
    # splitter, two to a reader -- so a word-count comparison called the
    # clearest possible control surface prose and swept the navigation labels.
    squash = lambda t: re.sub(r"\s+", "", t)
    return bool(from_controls) and \
        squash("".join(from_controls)) == squash(text)


def furniture(reference_file: Path = REFERENCE) -> set:
    """Text blocks shared by reference decks from two or more families.

    Derived, so it moves when the estate moves, and so nobody has to remember
    that this chassis ships "lundy-status" as well as "lundy-strip" -- the
    mistake that stripped nine Lundy elements per deck the first time."""
    _ = reference_file
    if not Path(reference_file).is_file():
        raise SystemExit(f"PROVENANCE REFUSAL: reference set {reference_file!r} is "
                         f"not a readable file. Every input must have a digest.")
    decks = json.loads(Path(reference_file).read_text())["decks"]
    seen: dict[str, set] = {}
    for rel in decks:
        fam = pad.family_of(rel) or rel
        for block in ad.all_text_blocks(ROOT / rel):
            seen.setdefault(block, set()).add(fam)
    return {b for b, fams in seen.items() if len(fams) >= 2}


def is_chrome(el, spec) -> bool:
    """The contract's own refrain, recognised by the instrument that measures it.

    The shared-across-families rule alone is not enough here. Each chassis
    generation words the Lundy strip slightly differently, so the LAUNCH
    generation's refrain is shared with no other family in the reference set and
    was swept out wholesale -- nine empty lundy grids, chrome zero on every
    stage, the contract's three-places requirement broken by a tool whose whole
    job was to preserve it. R3 already ruled what the refrain is and
    lesson_stages already detects it from STYLE_CONTRACT_RSH3_PINNED.json. Ask
    that, rather than inferring the contract from a sample of decks.
    """
    try:
        return ls.is_contract_chrome(el, spec)
    except Exception:
        return False


def strip(donor: Path, chassis_id: str, shared: set | None = None) -> tuple[str, dict]:
    raw = Path(donor).read_text(encoding="utf-8")
    old_id = ad.donor_id(raw)
    if not old_id:
        raise SystemExit(f"donor {donor} has no lesson-config id")

    if shared is None:
        shared = furniture()
    spec = ls.contract_chrome_spec()
    tree = lh.fromstring(raw.replace(old_id, chassis_id))
    screen = ls.ScreenView(tree)
    stages = ls.stages(tree, screen)

    for st in stages:
        ad.empty_stage(st)
        for svg in st.xpath("./svg"):
            st.remove(svg)
        st.set("data-title", PLACEHOLDER)
        for attr in ("data-ta1", "data-ta2"):
            if st.get(attr) is not None:
                del st.attrib[attr]
        for h2 in st.xpath(".//h2"):
            _clear(h2)
        for chip in st.xpath('.//*[contains(@class,"time-chip")]'
                             '|.//*[contains(@class,"time")]'
                             '|.//*[contains(@class,"phase-tag")]'
                             '|.//*[contains(@class,"tag")]'):
            _clear(chip)

    # The print pack, the staff drawer and the running head all sit OUTSIDE the
    # stages. The first version of the authoring pipeline missed exactly this
    # and shipped 282 words of the donor's print pack, its workbook cells
    # included. Sweep the whole document, not main.deck.
    #
    # list(), and it is not style. _clear removes child elements, and lxml's
    # tree.iter() is a LIVE document-order walk: mutating under it makes the
    # walk lose its place and skip the nodes after the one just changed. With a
    # bare iter() this sweep cleared the first few leaves and then jumped the
    # whole print pack -- seventeen donor blocks survived, the running head, the
    # workbook cells and every success criterion among them, and the sweep
    # reported no error at all. Materialise the walk before touching the tree.
    for el in list(tree.iter()):
        if not isinstance(el.tag, str) or el.tag.lower() not in TEXT_TAGS:
            continue
        if any(isinstance(k.tag, str) and k.tag.lower() in ls.BLOCK_TAGS
               for k in el.iterdescendants()):
            continue
        if is_control_surface(el) or is_chrome(el, spec):
            continue
        text = " ".join((el.text_content() or "").split())
        if text and text not in shared:
            _clear(el)

    html = lh.tostring(tree, encoding="unicode", doctype="<!doctype html>")

    # A lesson-config carrying the donor's week, cells or outcomes is the single
    # worst leak available: g19 and g29 both read it, and a chassis that keeps it
    # hands every Art deck the donor's plan.
    cfg = {"id": chassis_id, "family": "", "week": None, "slot": "", "title": "",
           "outcomes": [], "cells": [], "objective": "",
           "source": {"workbook": "", "sheet": "", "cell": ""},
           "timings": [], "planId": "",
           "chassis": {"tool": VERSION, "donor": ad._rel(donor),
                       "donorSha256": digest(donor)}}
    m = CONFIG_RE.search(html)
    html = html[:m.start(2)] + json.dumps(cfg, ensure_ascii=False) + html[m.end(2):]
    return html, {"donor": ad._rel(donor), "donorId": old_id,
                  "chassisId": chassis_id, "stages": len(stages)}


# --------------------------------------------------------------------------
def verify(donor: Path, out: Path, chassis_id: str, shared: set | None = None) -> dict:
    if shared is None:
        shared = furniture()
    donor_raw = Path(donor).read_text(encoding="utf-8")
    out_raw = Path(out).read_text(encoding="utf-8")
    old_id = ad.donor_id(donor_raw)

    out_tree = lh.fromstring(out_raw)
    spec = ls.contract_chrome_spec()
    control_text = {" ".join((el.text_content() or "").split())
                    for el in out_tree.iter()
                    if isinstance(el.tag, str)
                    and (is_control_surface(el) or is_chrome(el, spec))}
    donor_blocks = set(ad.all_text_blocks(donor))
    survived = [b for b in ad.all_text_blocks(out)
                if b in donor_blocks and b not in shared and b not in control_text]
    kept_furniture = [b for b in ad.all_text_blocks(out) if b in shared]

    # A sentence inside kept furniture is furniture, not a leak: the Lundy
    # status statement is four sentences long and two of them survive every
    # honest strip. Subtract what the block-level rule has already cleared as
    # shared, or this fires on the contract text the chassis is required to
    # carry.
    donor_sentences = set(ad._sentences(
        " ".join(lh.fromstring(donor_raw).text_content().split())))
    kept = " ".join(sorted(shared | control_text))
    out_text = " ".join(lh.fromstring(out_raw).text_content().split())
    sentence_leaks = sorted(s for s in donor_sentences
                            if s and s in out_text and s not in kept)

    cfg = json.loads(CONFIG_RE.search(out_raw).group(2))
    m = ls.measure(Path(out))

    checks = {
        "donorTextBlocksSurviving": survived,
        "furnitureKept": len(kept_furniture),
        "stageSvgSurviving": len(lh.fromstring(out_raw).xpath(
            '//main[contains(@class,"deck")]//*[contains(@class,"slide")]/svg')),
        "donorSentencesSurviving": sentence_leaks,
        # The chassis records the donor it came from, path and digest, and that
        # path contains the donor's lesson-config id. Recorded provenance is the
        # opposite of a leak; blank it before asking whether the id survives, or
        # this check reds on its own audit trail.
        "donorIdSurviving": bool(old_id) and old_id in re.sub(
            r'"chassis":\s*\{[^}]*\}', "", out_raw),
        "rootBlocks": out_raw.count(":root"),
        "stageCount": m["stageCount"],
        "dataMin": len(re.findall(r"data-min=", out_raw)),
        "contentWords": m["contentWords"],
        "chromeWords": m["chromeWords"],
        "configLeak": sorted(k for k, v in cfg.items()
                             if k not in ("id", "chassis") and v not in ("", None, [], {})
                             and k != "source"),
        "configSourceLeak": sorted(k for k, v in cfg["source"].items() if v),
        "runningHeadText": sorted({" ".join((e.text_content() or "").split())
                                   for e in lh.fromstring(out_raw).xpath(
                                       '//*[contains(@class,"running-head")]')} - {""}),
        "dataTa": len(re.findall(r"data-ta[12]=", out_raw)),
    }
    fails = []
    if checks["donorTextBlocksSurviving"]:
        fails.append(f"{len(survived)} donor text blocks survive the strip")
    if checks["donorSentencesSurviving"]:
        fails.append(f"{len(sentence_leaks)} donor sentences survive the strip")
    if checks["donorIdSurviving"]:
        fails.append("the donor's lesson-config id survives")
    if checks["rootBlocks"] != 1:
        fails.append(f"{checks['rootBlocks']} :root blocks, expected exactly 1")
    if checks["stageCount"] != 9:
        fails.append(f"{checks['stageCount']} stages, expected 9")
    if checks["dataMin"] < checks["stageCount"]:
        fails.append(f"data-min on {checks['dataMin']} of {checks['stageCount']} stages")
    if checks["stageSvgSurviving"]:
        fails.append(f"{checks['stageSvgSurviving']} donor stage diagrams survive")
    non_furniture = [b for b in ad.all_text_blocks(out)
                     if b not in shared and b not in control_text]
    if non_furniture:
        fails.append(f"{len(non_furniture)} text blocks survive that are not "
                     f"shared furniture: {non_furniture[:3]}")
    if checks["configLeak"] or checks["configSourceLeak"]:
        fails.append(f"lesson-config leak: {checks['configLeak']}"
                     f"{checks['configSourceLeak']}")
    if checks["runningHeadText"]:
        fails.append(f"running-head leak: {checks['runningHeadText']}")
    if checks["dataTa"]:
        fails.append(f"{checks['dataTa']} donor data-ta attributes survive")
    checks["fails"] = fails
    checks["verdict"] = "PASS" if not fails else "RED"
    return checks


def build(donor: Path, out: Path, chassis_id: str, shared: set | None = None) -> dict:
    if shared is None:
        shared = furniture()
    html, meta = strip(Path(donor), chassis_id, shared)
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    Path(out).write_text(html, encoding="utf-8")
    rep = verify(Path(donor), Path(out), chassis_id, shared)
    rep.update(meta)
    rep["out"] = ad._rel(out)
    rep["outSha256"] = digest(out)
    rep["tool"] = VERSION
    return rep


# --------------------------------------------------------------------------
def controls() -> list[dict]:
    """Planted, fired, withdrawn. Every one of these is a leak this campaign has
    actually shipped once, in an earlier form of this pipeline."""
    import tempfile
    out = []

    def rec(cid, claim, expect, actual):
        out.append({"id": cid, "claim": claim, "expected": expect, "actual": actual,
                    "verdict": "PASS" if expect == actual else "RED"})

    ref = json.loads((ROOT / "tools/easter/GREEN_REFERENCE_DECKS.json").read_text())
    donor = ROOT / ref["decks"][0]
    tmp = Path(tempfile.mkdtemp()) / "chassis.html"
    rep = build(donor, tmp, "ctrl-chassis")

    rec("a-real-deck-strips-to-a-clean-chassis",
        f"{donor.name} strips with no leak of any kind", "PASS", rep["verdict"])
    rec("the-chassis-teaches-nothing-of-its-donors",
        "every text block that survives is furniture two families share",
        [], rep["donorTextBlocksSurviving"])
    chassis_tree = lh.fromstring(tmp.read_text(encoding="utf-8"))
    nav = chassis_tree.xpath('//nav[contains(@class,"controls")]')
    rec("the-navigation-keeps-its-labels",
        "the button row still reads as buttons, not as a row of blanks",
        True, bool(nav) and len((nav[0].text_content() or "").split()) >= 4)
    rec("a-control-surface-is-recognised-by-structure",
        "a div of buttons is a control surface; the same div with a sentence in it is not",
        (True, False),
        (is_control_surface(lh.fromstring(
            "<div><button>Previous</button><button>Next</button></div>")),
         is_control_surface(lh.fromstring(
             "<div>Read the card and say what you can see."
             "<button>Next</button></div>"))))
    rec("the-donors-stage-diagrams-do-not-survive",
        "the two explanatory SVGs the donor draws on the board are gone",
        0, rep["stageSvgSurviving"])
    rec("the-nine-stage-spine-and-its-timings-survive",
        "9 stages, data-min on all 9", (9, 9), (rep["stageCount"], rep["dataMin"]))
    rec("the-lundy-refrain-survives-in-its-three-places",
        "the stripped chassis still carries a lundy-grid element on every stage",
        9, len(lh.fromstring(tmp.read_text(encoding="utf-8")).xpath(
            '//*[contains(@class,"lundy-grid")]')))
    rec("the-refrain-still-has-its-words",
        "every stage still measures chrome words; an empty grid is not a refrain",
        9, sum(1 for st in ls.measure(tmp)["stages"] if st["chromeWords"] > 0))
    rec("shared-furniture-is-kept-not-swept",
        "the chassis still carries the furniture blocks two families share",
        True, rep["furnitureKept"] > 0)
    rec("the-print-pack-shells-survive-so-authoring-has-somewhere-to-write",
        "h1, li and the tier routes are still present after the strip",
        True, all(t in tmp.read_text(encoding="utf-8")
                  for t in ("print-pack", "print-page", "<li", "<h1")))
    rec("the-guide-toggle-survives",
        "the staff drawer's toggle css and js are still present",
        True, all(t in tmp.read_text(encoding="utf-8")
                  for t in ('id="n6m-guide-css"', 'id="n6m-guide-js"')))

    # The leak gate must FIRE, not merely pass. Plant one donor sentence back
    # into the chassis and the verdict must go red -- otherwise "PASS" above
    # measures nothing.
    donor_sentences = ad._sentences(
        " ".join(lh.fromstring(donor.read_text(encoding="utf-8")).text_content().split()))
    planted = tmp.parent / "planted.html"
    planted.write_text(tmp.read_text(encoding="utf-8").replace(
        "</body>", f"<p>{donor_sentences[0]}</p></body>"), encoding="utf-8")
    prep = verify(donor, planted, "ctrl-chassis")
    rec("one-planted-donor-sentence-reds-the-leak-gate",
        "putting a single donor sentence back makes the verdict RED",
        "RED", prep["verdict"])

    # And the donor's own lesson-config must red it, because that is the leak
    # that would hand every Art deck the donor's plan.
    leaked = tmp.parent / "leaked.html"
    donor_cfg = CONFIG_RE.search(donor.read_text(encoding="utf-8")).group(2)
    chassis_raw = tmp.read_text(encoding="utf-8")
    m = CONFIG_RE.search(chassis_raw)
    leaked.write_text(chassis_raw[:m.start(2)] + donor_cfg + chassis_raw[m.end(2):],
                      encoding="utf-8")
    lrep = verify(donor, leaked, "ctrl-chassis")
    rec("the-donors-lesson-config-reds-the-leak-gate",
        "restoring the donor's lesson-config makes the verdict RED",
        "RED", lrep["verdict"])
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--donor")
    ap.add_argument("--out")
    ap.add_argument("--id")
    ap.add_argument("--output")
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

    if not (a.donor and a.out and a.id):
        raise SystemExit("--donor, --out and --id are all required")
    rep = build(Path(a.donor), Path(a.out), a.id)
    print(f"{rep['verdict']}  {rep['out']}  from {rep['donor']}")
    for f in rep["fails"]:
        print(f"   FAIL {f}")
    print(f"   stages {rep['stageCount']}  data-min {rep['dataMin']}  "
          f":root {rep['rootBlocks']}  content {rep['contentWords']}w  "
          f"chrome {rep['chromeWords']}w  sha256 {rep['outSha256'][:16]}")
    if a.output:
        Path(a.output).parent.mkdir(parents=True, exist_ok=True)
        Path(a.output).write_text(json.dumps(rep, indent=1), encoding="utf-8")
    return 0 if rep["verdict"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
