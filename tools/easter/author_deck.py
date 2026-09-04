#!/usr/bin/env python3
"""Author a lesson deck onto a family donor's chassis. A3N batch loop.

THE PROPERTY THIS TOOL EXISTS TO GUARANTEE
------------------------------------------
A deck authored from a donor must carry NONE of the donor's teaching. That is
easy to believe and hard to be sure of, because a chassis is mostly text: staff
notes, tier ladders, print sheets, model steps. Leave one behind and a lesson
about personal care quietly instructs a pupil about budgeting -- and it will
pass every gate, because gates count words and check structure, not provenance.

So the transform is subtractive first: every pupil-facing and staff-facing body
block inside every stage is REMOVED, and the authored content is inserted into
an emptied chassis. What survives from the donor is only what is not teaching --
the slide head, the heading element, the Lundy strip, the scripts, the styles
and the shell furniture. A control asserts it directly: not one donor sentence
of twelve words or more may appear in the output.

WHY NOT A TEMPLATE FROM NOTHING
-------------------------------
Because the chassis is load-bearing and unwritten down. Print pagination, the
guide toggle, the HUD, the progress bar, the evidence dialog, the print route,
the reduced-motion behaviour and the id namespacing are all in the donor and
none of them are documented anywhere else. Rebuilding them from scratch would
reproduce them wrongly and nothing would notice until a lesson was taught.

GATE-READABLE TIMINGS. The donor must declare stage minutes as `data-min`, which
is what lesson_stages -- and therefore every gate -- reads. 55 of 81 measured
decks use `data-minutes` instead and report no timings at all. A deck authored
from one of those would be born unmeasurable.

Usage:
  author_deck.py --donor D --plan-index N --content C.json --out O.html
  author_deck.py --list-controls | --self-test
"""
from __future__ import annotations

import argparse
import copy
import importlib.util
import json
import re
import sys
import tempfile
from pathlib import Path

from lxml import html as lh

ROOT = Path(__file__).resolve().parents[2]
VERSION = "author-deck-v1.0.0"

_ls = importlib.util.spec_from_file_location(
    "lesson_stages", ROOT / "_sownb/vb/tools/lesson_stages.py")
ls = importlib.util.module_from_spec(_ls); _ls.loader.exec_module(ls)

CONFIG_RE = re.compile(
    r'(<script[^>]*id=["\']lesson-config["\'][^>]*>)(.*?)(</script>)', re.S)

# Kept because they are not teaching. Everything else inside a stage goes.
# The Lundy elements stay. The contract requires the refrain in three places and
# the first version stripped nine of them per deck, because only "lundy-strip"
# was listed and this chassis also ships "lundy", "lundy-grid" and
# "lundy-status". R3 counts all of them as zero words, so keeping them costs the
# measurement nothing and losing them breaks lundy-in-three-places.
KEEP_CLASSES = ("slide-head", "phase-tag", "time-chip", "lundy-strip", "lundy",
                "lundy-grid", "lundy-status", "running-head", "progress-wrap",
                "time", "tag", "slide-tag")
KEEP_TAGS = ("script", "style", "svg", "button", "h2")


def _rel(p) -> str:
    try:
        return str(Path(p).resolve().relative_to(ROOT))
    except ValueError:
        return str(p)


def donor_id(raw: str) -> str | None:
    m = CONFIG_RE.search(raw)
    if not m:
        return None
    try:
        return json.loads(m.group(2)).get("id")
    except Exception:
        return None


def _is_keeper(el) -> bool:
    cls = set((el.get("class") or "").split())
    if any(k in cls for k in KEEP_CLASSES):
        return True
    return isinstance(el.tag, str) and el.tag.lower() in KEEP_TAGS


def empty_stage(stage):
    """Remove every teaching body block, keep the chassis furniture."""
    for child in list(stage):
        if not isinstance(child.tag, str):
            continue
        if _is_keeper(child):
            continue
        stage.remove(child)


def render_figure(spec: dict) -> str:
    """Build the explanatory SVG from LABELS, not from author-written markup.

    g24 requires two explanatory visuals with real geometry, and a deck authored
    without them is red. Asking a writer for raw SVG invites malformed markup in
    a lesson file; asking for four labels and a caption cannot. Two shapes cover
    what these lessons need: a left-to-right chain of steps, and two columns
    resting on a shared condition.
    """
    kind = spec.get("kind", "chain")
    boxes = spec.get("boxes", [])[:4]
    cap = spec.get("caption", "")
    title = spec.get("title", "Diagram")
    esc = lambda t: (t or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    if kind == "columns" and len(boxes) >= 2:
        parts = [f'<svg viewBox="0 0 620 190" role="img" width="100%" '
                 f'aria-label="{esc(spec.get("alt", title))}"><title>{esc(title)}</title>']
        for i, b in enumerate(boxes[:2]):
            x = 16 + i * 318
            dash = ' stroke-dasharray="7 4"' if i else ""
            parts.append(f'<rect x="{x}" y="16" width="270" height="104" rx="8" fill="none" '
                         f'stroke="#333" stroke-width="2"{dash}/>')
            parts.append(f'<circle cx="{x+24}" cy="42" r="7" fill="none" stroke="#333" stroke-width="2"/>')
            parts.append(f'<text x="{x+135}" y="48" text-anchor="middle" font-size="14">{esc(b.get("head",""))}</text>')
            parts.append(f'<text x="{x+135}" y="74" text-anchor="middle" font-size="11">{esc(b.get("line1",""))}</text>')
            parts.append(f'<text x="{x+135}" y="94" text-anchor="middle" font-size="11">{esc(b.get("line2",""))}</text>')
            parts.append(f'<line x1="{x+135}" y1="120" x2="{x+135}" y2="140" stroke="#333" stroke-width="2"/>')
            parts.append(f'<path d="M{x+129} 132 L{x+135} 142 L{x+141} 132 Z" fill="#333"/>')
        parts.append('<rect x="16" y="140" width="588" height="40" rx="8" fill="none" '
                     'stroke="#333" stroke-width="2" stroke-dasharray="6 4"/>')
        parts.append(f'<text x="310" y="165" text-anchor="middle" font-size="12">{esc(cap)}</text>')
        parts.append("</svg>")
        return "".join(parts)
    n = max(2, len(boxes))
    w = int((604 - 28 * (n - 1)) / n)
    parts = [f'<svg viewBox="0 0 620 150" role="img" width="100%" '
             f'aria-label="{esc(spec.get("alt", title))}"><title>{esc(title)}</title>']
    for i, b in enumerate(boxes):
        x = 8 + i * (w + 28)
        parts.append(f'<rect x="{x}" y="42" width="{w}" height="60" rx="8" fill="none" '
                     f'stroke="#333" stroke-width="2"/>')
        parts.append(f'<text x="{x+w//2}" y="70" text-anchor="middle" font-size="13">{esc(b.get("head",""))}</text>')
        parts.append(f'<text x="{x+w//2}" y="88" text-anchor="middle" font-size="11">{esc(b.get("line1",""))}</text>')
        if i:
            parts.append(f'<line x1="{x-28}" y1="72" x2="{x-4}" y2="72" stroke="#333" stroke-width="2"/>')
            parts.append(f'<path d="M{x-12} 66 L{x} 72 L{x-12} 78 Z" fill="#333"/>')
    parts.append(f'<text x="306" y="126" text-anchor="middle" font-size="12">{esc(cap)}</text>')
    parts.append("</svg>")
    return "".join(parts)


def render_blocks(spec: list[dict]) -> list:
    """Authored content -> elements. Only shapes the chassis already uses."""
    out = []
    for b in spec:
        kind = b.get("kind", "p")
        if kind == "h3":
            e = lh.Element("h3"); e.text = b["text"]
        elif kind == "list":
            e = lh.Element("ul")
            for item in b["items"]:
                li = lh.Element("li"); li.text = item; e.append(li)
        elif kind == "svg":
            e = lh.fromstring(b["svg"])
        elif kind == "figure":
            e = lh.fromstring(render_figure(b))
        elif kind == "staff":
            e = lh.Element("div")
            e.set("class", "box rehearsal"); e.set("data-mbm-guide", "staff")
            e.text = b["text"]
        elif kind == "box":
            e = lh.Element("div"); e.set("class", "box " + b.get("boxClass", "objective"))
            e.text = b["text"]
        else:
            e = lh.Element("p"); e.text = b["text"]
        out.append(e)
    return out


def author_print_pack(tree, plan: dict, content: dict) -> None:
    """Rewrite the printable pack by ROLE, then let the whole-document leak gate
    catch whatever role this function did not know about."""
    pk = content.get("print", {})
    head = (f'{plan["family"]} · Week {plan["ruledWeek"]} · '
            f'{content.get("slot", "")} · {content["title"]}')
    for pack in tree.xpath('//section[contains(@class,"print-pack")]'):
        for el in pack.xpath('.//*[contains(@class,"running-head")]'):
            el.text = head
            for k in list(el):
                el.remove(k)
        for h1 in pack.xpath(".//h1"):
            h1.text = content["title"]
            for k in list(h1):
                h1.remove(k)
        for para in pack.xpath(".//p[b]"):
            label = (para.xpath("./b")[0].text or "").strip().rstrip(":")
            value = {"Workbook trace": " · ".join(plan["cells"]),
                     "Verbatim outcome": " · ".join(plan["outcomes"]),
                     "Objective": content["objective"]}.get(label)
            if value is None:
                continue
            b = para.xpath("./b")[0]
            for k in list(para):
                if k is not b:
                    para.remove(k)
            para.text = None
            b.tail = " " + value
        # EVERY heading, not just the ones the author remembered. Supplying two
        # section names for a pack with four headings left two donor headings in
        # place -- "Every profile statement bound to genuine evidence or MISSING:"
        # on a lesson about strengths. A surplus heading falls back to the deck
        # title, which is always true of the deck and never true of the donor.
        sections = pk.get("sections", [])
        for i, h2 in enumerate(pack.xpath(".//h2")):
            h2.text = sections[i] if i < len(sections) else content["title"]
            for k in list(h2):
                h2.remove(k)
        # THE SCREEN DIAGRAM IS PRINT-DEAD BY DEFAULT, AND THAT IS A CHASSIS FACT.
        # A2R R3 measured it: the shell hides the slide container under @media
        # print, so every explanatory visual a deck draws on the board is absent
        # from the sheet a pupil is handed. Putting the same figure in the print
        # pack is not a gate workaround -- the printed sheet genuinely needs the
        # diagram, and g24 counts it because it genuinely survives.
        figs = pk.get("figures", [])
        if figs:
            page = pack.xpath('.//section[contains(@class,"print-page")]')
            target = page[0] if page else pack
            for svg in figs:
                target.append(lh.fromstring(svg))

        # The success-criteria list. Two donor items survived here on the first
        # GROW build -- "Every profile statement bound to genuine evidence or
        # MISSING:" printed on a lesson about strengths. Surplus items are
        # removed rather than left, because an unauthored criterion is the
        # donor's criterion.
        checks = pk.get("checks", [])
        for lst in pack.xpath(".//ol|.//ul"):
            items = [li for li in lst if isinstance(li.tag, str) and li.tag.lower() == "li"]
            for i, li in enumerate(items):
                if i < len(checks):
                    li.text = checks[i]
                    for k in list(li):
                        li.remove(k)
                else:
                    lst.remove(li)

        rows = pk.get("focusRows", [])
        cells = pack.xpath(".//table//tr/td[1]")
        for i, td in enumerate(cells):
            if i < len(rows):
                td.text = rows[i]
                for k in list(td):
                    td.remove(k)
        tiers = pk.get("tiers", [])
        for i, route in enumerate(pack.xpath('.//*[contains(@class,"print-route")]')):
            if i >= len(tiers):
                break
            for para in route.xpath("./p"):
                para.text = tiers[i]
                for k in list(para):
                    route_child = k
                    para.remove(route_child)
        for para in pack.xpath(".//p[not(b)]"):
            t = " ".join((para.text_content() or "").split())
            if len(t.split()) >= 8 and para.getparent().get("class", "").find("print-route") < 0:
                if pk.get("intro"):
                    para.text = pk["intro"]
                    for k in list(para):
                        para.remove(k)


def sweep_donor_text(tree, donor: Path, plan: dict, content: dict) -> None:
    """The belt. Role-based rewriting knows the roles it was told about, and this
    estate has more print-pack variants than roles.

    On the LAUNCH ASDAN chassis three donor blocks survived every role handler:
    a plain <p> "Learning objective: ..." with no <b> to match on, a <p> "SoW:
    'LAUNCH Weekly - Autumn'!C171" carrying THE DONOR'S OWN WORKBOOK CELL, and a
    <div class="print-note">. Chasing each variant's markup is a losing game; the
    reliable move is to sweep for donor text at the end and neutralise whatever
    is left, whatever element it happens to live in.

    Donor-specific means: present in the donor and NOT in the family reference,
    so chassis furniture is never touched. A labelled line is rewritten to the
    truth about THIS lesson; anything else is removed, because an unauthored
    block is the donor's block.
    """
    ref = content.get("_reference")
    if not ref:
        return
    donor_only = set(all_text_blocks(donor)) - set(all_text_blocks(Path(ref)))
    if not donor_only:
        return
    rewrite = {
        "learning objective": f'Learning objective: {content["objective"]}',
        "objective": f'Objective: {content["objective"]}',
        "sow": f'SoW: {" · ".join(plan["cells"])} — "{plan["outcomes"][0]}"',
        "workbook trace": f'Workbook trace: {" · ".join(plan["cells"])}',
        "verbatim outcome": f'Verbatim outcome: {" · ".join(plan["outcomes"])}',
    }
    for el in list(tree.iter()):
        if not isinstance(el.tag, str) or el.tag.lower() not in BLOCK_TAGS_LOCAL:
            continue
        if any(isinstance(k.tag, str) and k.tag.lower() in BLOCK_TAGS_LOCAL
               for k in el.iterdescendants()):
            continue
        text = " ".join((el.text_content() or "").split())
        if text not in donor_only:
            continue
        low = text.lower()
        new = next((v for k, v in rewrite.items() if low.startswith(k)), None)
        if new is not None:
            for k in list(el):
                el.remove(k)
            el.text = new
        else:
            parent = el.getparent()
            if parent is not None:
                parent.remove(el)


BLOCK_TAGS_LOCAL = ls.BLOCK_TAGS


def author(donor: Path, plan: dict, content: dict, out: Path) -> dict:
    raw = Path(donor).read_text(encoding="utf-8")
    old_id = donor_id(raw)
    new_id = content["id"]
    if not old_id:
        raise SystemExit("donor has no lesson-config id")

    # id namespace first, on the raw text, so onclick handlers and ids move together
    raw2 = raw.replace(old_id, new_id)
    tree = lh.fromstring(raw2)
    screen = ls.ScreenView(tree)
    stages = ls.stages(tree, screen)
    if len(stages) != len(content["stages"]):
        raise SystemExit(f"donor has {len(stages)} stages, content supplies "
                         f"{len(content['stages'])}")

    for st, spec in zip(stages, content["stages"]):
        empty_stage(st)
        st.set("data-title", spec["title"])
        st.set("data-min", str(spec["minutes"]))
        if spec.get("type"):
            st.set("data-type", spec["type"])
        for k in ("data-ta1", "data-ta2"):
            if spec.get(k):
                st.set(k, spec[k])
            elif st.get(k) is not None:
                del st.attrib[k]
        for h2 in st.xpath(".//h2"):
            h2.text = spec["title"]
            for kid in list(h2):
                h2.remove(kid)
        for chip in st.xpath('.//*[contains(@class,"time-chip")]|.//*[contains(@class,"time")]'):
            chip.text = f'{spec["minutes"]} min'
        for tag in st.xpath('.//*[contains(@class,"phase-tag")]'):
            if spec.get("phase"):
                tag.text = spec["phase"]
        anchor = None
        for kid in st:
            if isinstance(kid.tag, str) and "lundy-strip" in (kid.get("class") or ""):
                anchor = kid
                break
        for el in render_blocks(spec["blocks"]):
            if anchor is not None:
                anchor.addprevious(el)
            else:
                st.append(el)

    author_print_pack(tree, plan, content)
    sweep_donor_text(tree, donor, plan, content)
    html = lh.tostring(tree, encoding="unicode", doctype="<!doctype html>")

    # lesson-config replaced wholesale: no donor field may survive
    cfg = {
        "id": new_id, "family": plan["family"], "week": plan["ruledWeek"],
        "slot": content.get("slot", plan.get("subject", "")),
        "title": content["title"], "outcomes": plan["outcomes"],
        "cells": plan["cells"], "objective": content["objective"],
        "source": {"workbook": plan["workbook"], "sheet": plan["sheet"],
                   "cell": plan["cells"][0]},
        "timings": [s["minutes"] for s in content["stages"]],
    }
    if content.get("weDoType"):
        cfg["weDoType"] = content["weDoType"]
    if content.get("tierLadder"):
        cfg["tierLadder"] = content["tierLadder"]
    m = CONFIG_RE.search(html)
    html = html[:m.start(2)] + json.dumps(cfg, ensure_ascii=False) + html[m.end(2):]

    Path(out).parent.mkdir(parents=True, exist_ok=True)
    Path(out).write_text(html, encoding="utf-8")
    return verify(donor, Path(out), plan, content, old_id, new_id,
                  reference=content.get("_reference"))


def _sentences(text: str) -> list[str]:
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+|\n+", text)
            if len(s.strip().split()) >= 12]


def all_text_blocks(path) -> list[str]:
    """EVERY text-bearing leaf block in the whole document, not just the stages.

    The first version read only `main.deck` stages, and it declared a deck clean
    while 282 words of the donor's PRINT PACK sat outside that element -- wrong
    week, wrong title, and the donor's workbook cells, which is a coverage lie
    printed on the sheet a pupil is handed. The leak gate now reads the document.
    """
    tree = ls.parse(Path(path))
    out = []
    for el in tree.iter():
        if not isinstance(el.tag, str) or el.tag.lower() not in ls.BLOCK_TAGS:
            continue
        if any(isinstance(k.tag, str) and k.tag.lower() in ls.BLOCK_TAGS
               for k in el.iterdescendants()):
            continue
        t = " ".join((el.text_content() or "").split())
        if len(t.split()) >= 8:
            out.append(t)
    return out


def pupil_blocks(path) -> list[str]:
    """Compare BLOCK BY BLOCK, not sentence by sentence across a joined stage.

    The first version joined every stage into one string and split it on sentence
    punctuation. Chrome then contaminated the boundaries -- the donor's exit
    sentence was recorded as "5 min Exit Donor exit sentence ..." because the time
    chip and the heading sat in front of it with no full stop between. A planted
    leak went undetected and the control reported PASS. Blocks have edges the
    chassis cannot blur."""
    tree = ls.parse(Path(path))
    screen = ls.ScreenView(tree)
    spec = ls.contract_chrome_spec()
    out = []
    for st in ls.stages(tree, screen):
        node = ls.stage_pupil_node(st, screen)
        for el in ls._leaf_blocks(node):
            t = " ".join((el.text_content() or "").split())
            if len(t.split()) >= 12 and not ls.is_contract_chrome(el, spec):
                out.append(t)
    return out


def chassis_blocks(donor: Path, reference: Path | None) -> set:
    """Text the CHASSIS carries, derived rather than judged.

    The first leak gate flagged seven blocks and not one was teaching: the Lundy
    banner and its four dimension definitions, the guide-toggle explanation, the
    navigation bar. Those are supposed to be identical between two decks of the
    same chassis -- that is what a chassis is.

    Telling chassis from donor teaching by reading it would be my opinion. It is
    derivable instead: a block that also appears in a THIRD, unrelated deck of
    the same family is furniture; a block only the donor and the new deck share
    is the donor's, and it leaked.
    """
    return set(all_text_blocks(reference)) if reference else set()


def verify(donor, out, plan, content, old_id, new_id, reference=None) -> dict:
    o_raw = Path(out).read_text(encoding="utf-8")
    chassis = chassis_blocks(donor, reference)
    donor_sents = set(all_text_blocks(donor)) - chassis
    out_blocks = set(all_text_blocks(out))
    leaked = sorted(donor_sents & out_blocks)
    meas = ls.measure(Path(out))
    cfg = json.loads(CONFIG_RE.search(o_raw).group(2))
    mins = [int(float(r["minutes"])) for r in meas["stages"] if r["minutes"] not in (None, "")]
    return {
        "file": _rel(out), "toolVersion": VERSION, "donor": _rel(donor),
        "donorSentences": len(donor_sents), "donorSentencesLeaked": len(leaked),
        "chassisBlocksExcluded": len(chassis), "referenceDeck": _rel(reference) if reference else None,
        "leakedExamples": leaked[:3],
        "donorIdRemains": old_id in o_raw,
        "stageCount": meas["stageCount"], "contentWords": meas["contentWords"],
        "timingsGateReadable": len(mins) == meas["stageCount"],
        "timingsSum": sum(mins),
        "configCells": cfg.get("cells"), "configOutcomes": len(cfg.get("outcomes", [])),
        "lundyStrips": o_raw.count("lundy-strip"),
        "status": "PASS" if (not leaked and not (old_id in o_raw)
                             and len(mins) == meas["stageCount"]) else "RED",
    }


# --------------------------------------------------------------------------
# Controls
# --------------------------------------------------------------------------

CONTROL_IDS = [
    "not-one-donor-sentence-survives",
    "the-donors-print-pack-does-not-survive-either",
    "a-print-heading-the-author-did-not-name-still-loses-its-donor-text",
    "an-unroled-donor-block-is-swept-not-shipped",
    "the-donor-id-namespace-is-gone",
    "a-planted-leak-is-caught",
    "stage-count-and-chassis-furniture-survive",
    "timings-are-gate-readable-and-sum-to-the-session",
    "the-lesson-config-carries-the-plans-cells-not-the-donors",
]

_DONOR = """<!doctype html><html><head><style>.slide{display:none}
.slide.active{display:flex}</style>
<script id="lesson-config" type="application/json">{"id":"OLD_W1","family":"F","timings":[0,5,5],"cells":["'X'!C1"],"outcomes":["donor outcome"]}</script>
</head><body><main class="deck">
<section class="slide active" data-title="Lesson overview" data-min="0" data-type="title">
<div class="slide-head"><span class="phase-tag">SEE</span><span class="time">0 min</span></div>
<h2>Lesson overview</h2><p>Donor overview sentence that is quite long indeed and must not survive this transform at all.</p>
<div class="lundy-strip"><span>SPACE</span><span>VOICE</span><span>AUDIENCE</span><span>INFLUENCE</span></div></section>
<section class="slide" data-title="I Do" data-min="5">
<div class="slide-head"><span class="phase-tag">SEE</span><span class="time">5 min</span></div>
<h2>I Do</h2><div id="OLD_W1-model-1"><div class="model-step">Donor modelling step that is quite long indeed and must not survive this transform.</div></div>
<div class="box rehearsal" data-mbm-guide="staff">Donor staff note that is quite long indeed and must not survive this transform.</div>
<div class="lundy-strip"><span>SPACE</span><span>VOICE</span><span>AUDIENCE</span><span>INFLUENCE</span></div></section>
<section class="slide" data-title="Exit" data-min="5">
<div class="slide-head"><span class="phase-tag">ACT</span><span class="time">5 min</span></div>
<h2>Exit</h2><p>Donor exit sentence that is quite long indeed and must not survive this transform at all.</p>
<div class="lundy-strip"><span>SPACE</span><span>VOICE</span><span>AUDIENCE</span><span>INFLUENCE</span></div></section>
</main></body></html>"""

_PLAN = {"family": "F2", "ruledWeek": 3, "outcomes": ["new outcome one"],
         "cells": ["'Y'!C9"], "workbook": "wb.xlsx", "sheet": "Y", "subject": "S"}

_CONTENT = {
    "id": "NEW_W3", "title": "New title", "objective": "New objective sentence.",
    "stages": [
        {"title": "Lesson overview", "minutes": 0, "type": "title", "phase": "SEE",
         "blocks": [{"kind": "p", "text": "A fresh overview sentence written for this lesson and nobody else."}]},
        {"title": "I Do", "minutes": 20, "phase": "SEE",
         "blocks": [{"kind": "p", "text": "A fresh modelling sentence written for this lesson and nobody else."},
                    {"kind": "staff", "text": "A fresh staff note written for this lesson and nobody else here."}]},
        {"title": "Exit", "minutes": 20, "phase": "ACT",
         "blocks": [{"kind": "p", "text": "A fresh exit sentence written for this lesson and for nobody else."}]},
    ],
}


def _tmp(src: str) -> Path:
    fh = tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8")
    fh.write(src); fh.close()
    return Path(fh.name)


def ad_all(p):
    return all_text_blocks(p)


def controls() -> list[dict]:
    out = []

    def rec(cid, description, expected, observed):
        out.append({"id": cid, "description": description, "expected": expected,
                    "observed": observed, "fired": expected == observed})

    d = _tmp(_DONOR)
    o = Path(tempfile.mkdtemp()) / "new.html"
    r = author(d, _PLAN, _CONTENT, o)

    rec("not-one-donor-sentence-survives",
        "a chassis is mostly text; one staff note or model step left behind teaches "
        "the wrong lesson and passes every gate, because gates count words not provenance",
        (0, []), (r["donorSentencesLeaked"], r["leakedExamples"]))

    rec("the-donors-print-pack-does-not-survive-either",
        "the print pack sits OUTSIDE main.deck, so a stage-only leak test declares a "
        "deck clean while 282 donor words -- wrong week, wrong title, the donor's "
        "workbook cells -- print on the sheet a pupil is handed",
        (0, True),
        (sum(1 for b in ad_all(o) if b in set(ad_all(d))),
         "'Y'!C9" in Path(o).read_text(encoding="utf-8")))

    rec("a-print-heading-the-author-did-not-name-still-loses-its-donor-text",
        "supplying two section names for a pack with more headings left donor "
        "headings standing; a surplus heading falls back to the deck title",
        True, all("Donor" not in b for b in ad_all(o)))

    rec("the-donor-id-namespace-is-gone",
        "ids and their onclick handlers move together or the reveal widget breaks",
        False, r["donorIdRemains"])

    leaky = dict(_CONTENT)
    leaky = json.loads(json.dumps(_CONTENT))
    leaky["id"] = "LEAK_W3"
    leaky["stages"][2]["blocks"].append(
        {"kind": "p", "text": "Donor exit sentence that is quite long indeed and "
                              "must not survive this transform at all."})
    o2 = Path(tempfile.mkdtemp()) / "leak.html"
    r2 = author(d, _PLAN, leaky, o2)
    rec("a-planted-leak-is-caught",
        "the leak test must be able to fail, or it proves nothing",
        ("RED", 1), (r2["status"], r2["donorSentencesLeaked"]))

    rec("stage-count-and-chassis-furniture-survive",
        "the shell is load-bearing and undocumented; emptying stages must not empty it",
        (3, 3), (r["stageCount"], r["lundyStrips"]))

    rec("timings-are-gate-readable-and-sum-to-the-session",
        "data-min is what every gate reads; data-minutes is invisible to all of them",
        (True, 40), (r["timingsGateReadable"], r["timingsSum"]))

    rec("the-lesson-config-carries-the-plans-cells-not-the-donors",
        "a deck claiming the donor's cell is a coverage lie",
        (["'Y'!C9"], 1), (r["configCells"], r["configOutcomes"]))

    # An unroled donor block, and a labelled line carrying the DONOR'S OWN CELL.
    # Both survived every role handler on the real LAUNCH ASDAN chassis.
    donor_sweep = _DONOR.replace(
        "</main>",
        '</main><section class="print-pack"><div class="print-page">'
        '<p>Learning objective: I can review the donor community project outcome '
        'using genuine evidence and bounded claims.</p>'
        '<p>SoW: LAUNCH Weekly - Autumn!C171 - "Autumn community-project review."</p>'
        '<div class="print-note">Teaching and potential evidence only, a donor '
        'sentence in an element no role handler covers at all.</div>'
        "</div></section>")
    ds = _tmp(donor_sweep)
    ref = _tmp(_DONOR)                     # reference lacks the pack, so it is donor-specific
    c3 = json.loads(json.dumps(_CONTENT)); c3["id"] = "SWEPT_W3"
    c3["_reference"] = ref
    o3 = Path(tempfile.mkdtemp()) / "swept.html"
    r3 = author(ds, _PLAN, c3, o3)
    # read the RAW file: the rewritten SoW line is shorter than the 8-word floor
    # all_text_blocks applies, so asserting on that view would miss it
    body3 = o3.read_text(encoding="utf-8")
    rec("an-unroled-donor-block-is-swept-not-shipped",
        "role handlers know only the roles they were told about, and this estate "
        "has more print variants than roles; an unroled donor block is removed and "
        "a labelled line is rewritten to this lesson's truth -- the donor's own "
        "workbook cell must not survive on the printed sheet",
        (0, False, True),
        (r3["donorSentencesLeaked"],
         "C171" in body3,
         "'Y'!C9" in body3))

    for f in (ds, ref):
        f.unlink(missing_ok=True)
    d.unlink(missing_ok=True)
    return out


def self_test() -> dict:
    res = controls()
    ids = [r["id"] for r in res]
    missing = [c for c in CONTROL_IDS if c not in ids]
    extra = [c for c in ids if c not in CONTROL_IDS]
    return {"tool": "author_deck", "toolVersion": VERSION,
            "file": "tools/easter/author_deck.py",
            "controlsDeclared": len(CONTROL_IDS), "controlsRun": len(res),
            "controlsFired": sum(1 for r in res if r["fired"]),
            "missingControls": missing, "undeclaredControls": extra,
            "allListedControlsFired": not missing and not extra and all(r["fired"] for r in res),
            "controls": res}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--donor"); ap.add_argument("--plan-index", type=int)
    ap.add_argument("--content"); ap.add_argument("--out"); ap.add_argument("--output")
    ap.add_argument("--list-controls", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()
    if a.list_controls:
        print("\n".join(CONTROL_IDS)); return 0
    if a.self_test:
        rep = self_test()
        print(f"author_deck self-test  [{VERSION}]")
        for r in rep["controls"]:
            print(f"  {'ok  ' if r['fired'] else 'FAIL'} {r['id']:52s} "
                  f"expected={str(r['expected'])[:38]} observed={str(r['observed'])[:38]}")
        print(f"{rep['controlsFired']}/{rep['controlsRun']} controls fired")
        print("PASS" if rep["allListedControlsFired"] else "MEASUREMENT INVALID")
        return 0 if rep["allListedControlsFired"] else 1

    plans = json.loads((ROOT / "tools/easter/EASTER_TARGETS.json").read_text())["plans"]
    content = json.loads(Path(a.content).read_text(encoding="utf-8"))
    rec = author(Path(a.donor), plans[a.plan_index], content, Path(a.out))
    print(json.dumps(rec, indent=1))
    if a.output:
        Path(a.output).write_text(json.dumps(rec, indent=1) + "\n", encoding="utf-8")
    return 0 if rec["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
