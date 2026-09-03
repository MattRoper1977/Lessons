#!/usr/bin/env python3
"""lesson_stages — the one place the estate decides what pupil teaching content is.

WHY THIS FILE EXISTS
--------------------
g18, g23, g24 and g25 each carried their own idea of "a slide". All four used
the same XPath:

    //main[contains(@class,"deck")]/section[contains(@class,"slide")]

That selector describes ONE shell. The classic chassis puts its stages in
``main.deck > div.slide-container > div.slide`` instead, so on every classic
deck all four gates measured **nothing** and reported it as a pass:

    BUILD_HUM_W16_Then_And_Now_And_What_Is_Fair.html   0w  x0.0  WITHIN  PASS

That deck carries ten stages and 2,191 pupil words. It was reshelled onto the
classic chassis and landed on main in PR #271, and from that moment its period
load, its content floor and its we-do variety were unmeasured. 264 of the 607
deck-shaped files in this estate are classic-shell; every one of them was
invisible to those gates. This module is the single shell-aware answer, and
every gate now imports it rather than re-deciding.

THE TRAP THAT MAKES "IS IT VISIBLE" HARD
----------------------------------------
Both shells run a carousel:

    .slide         { display:none }
    .slide.active  { display:flex }

So nine of ten stages are ``display:none`` at any instant. A gate that asked
"is this element visible on screen?" would count ONE stage and call the lesson
thin. Slide-level display toggling is NAVIGATION, not hiding.

The rule this module implements, therefore, has two levels:

  STAGE ELIGIBILITY  is decided by the ancestor chain ABOVE the stage. The
                     classic shell hides its print pack with a plain, unmedia'd
                     ``#print-area{display:none}`` and re-shows it under
                     ``@media print``. So the print pack's stages fail
                     eligibility and the pack is excluded because of what the
                     deck's own CSS says, not because of a class name this file
                     had to be told about.

  CONTENT VISIBILITY is resolved WITHIN a stage, with the stage itself taken as
                     a visible root. A ``display:none`` block inside a stage is
                     hidden; the stage's own carousel state is not consulted.

Everything else follows from those two sentences.

WHAT IS EXCLUDED FROM PUPIL TEACHING TEXT, AND WHY
--------------------------------------------------
  the three print-pack tiers  they re-print the stage text; counting them
                              counts the lesson twice
  the staff drawer            ``data-audience="staff"`` and ``data-mbm-guide``
                              are the two keys the decks actually use
  the running head            chrome, repeated on every stage
  script / style / template / noscript / svg
  display:none, visibility:hidden   resolved from the deck's own CSS
  aria-hidden="true", hidden        not offered to the pupil
  anything scoped to @media print   it is not in the pupil's screen view

MEDIA QUERIES ARE READ CONSERVATIVELY. A rule applies to the screen view when
it sits outside any ``@media``, or inside one whose query is ``screen`` or
``all``. ``@media print`` is print. A width- or feature-conditional query is
NOT applied, and is counted in ``skippedMediaBlocks`` so the omission is
visible: applying one would let a phone breakpoint delete pupil text from a
projector measurement.

A selector this module's parser cannot read is likewise counted, and separately
if it would have hidden something -- ``unreadableHidingSelectors``. A parser
that silently drops a ``display:none`` rule is a fail-open with a tidy report.

Usage:
  lesson_stages.py --list-controls
  lesson_stages.py --self-test [--output report.json]
  lesson_stages.py <deck.html> [<deck.html> ...]
"""
from __future__ import annotations

import argparse
import copy
import json
import re
import sys
import unicodedata
from pathlib import Path

from lxml import html as lh
from lxml.cssselect import CSSSelector
from cssselect import SelectorError, parse as css_parse

VERSION = "lesson-stages-v1.0.0-shell-aware-screen-scoped"
ROOT = Path(__file__).resolve().parents[3]

WORD = re.compile(r"[A-Za-z0-9]+(?:['’-][A-Za-z0-9]+)*")

# The tags that are never pupil teaching text wherever they appear.
NON_PUPIL_TAGS = {"script", "style", "noscript", "template", "svg"}

# The two keys the decks use for staff-only content. Both are checked as
# attributes rather than classes because that is what the estate writes.
STAFF_ATTRS = ("data-mbm-guide",)
STAFF_AUDIENCE = "staff"

# Chrome that repeats on every stage and is not taught.
CHROME_CLASSES = ("running-head", "slide-tag", "timer-widget", "progress-wrap",
                  "progress-label", "controls", "control-bar", "hud", "mbmhome")


# --------------------------------------------------------------------------
# A small, honest CSS reader.
# --------------------------------------------------------------------------

class Rule:
    __slots__ = ("selector", "decls", "media", "order")

    def __init__(self, selector: str, decls: dict, media: str, order: int):
        self.selector = selector
        self.decls = decls
        self.media = media          # "screen" | "print" | "skip"
        self.order = order


def _decls(body: str) -> dict:
    """{property: (value, important)} for the properties we resolve."""
    out = {}
    for chunk in body.split(";"):
        if ":" not in chunk:
            continue
        prop, _, value = chunk.partition(":")
        prop = prop.strip().lower()
        if prop not in ("display", "visibility"):
            continue
        value = value.strip().lower()
        important = "!important" in value
        value = value.replace("!important", "").strip()
        if value:
            out[prop] = (value, important)
    return out


def _media_kind(query: str) -> str:
    """screen | print | skip. Conservative: only unconditional queries apply."""
    q = " ".join(query.lower().split())
    q = q.lstrip("@").removeprefix("media").strip()
    if not q or q in ("all", "screen", "only screen", "screen, print", "print, screen"):
        return "screen"
    if q in ("print", "only print"):
        return "print"
    # "screen and (max-width: 600px)", "(prefers-reduced-motion: reduce)", ...
    return "skip"


def parse_css(css: str) -> tuple[list[Rule], int]:
    """Flatten a stylesheet into rules, tracking the @media context.

    Written as a brace walker rather than a regex because a regex cannot tell a
    nested at-rule from a declaration block, and getting that wrong is how a
    @media print body leaks into the screen view.
    """
    css = re.sub(r"/\*.*?\*/", " ", css, flags=re.S)
    rules: list[Rule] = []
    skipped_media = 0
    order = 0
    i, n = 0, len(css)
    # stack of media kinds; "screen" at the base
    stack = ["screen"]
    buf = []
    while i < n:
        ch = css[i]
        if ch == "{":
            prelude = "".join(buf).strip()
            buf = []
            if prelude.startswith("@"):
                name = prelude.split(None, 1)[0].lower()
                if name == "@media":
                    kind = _media_kind(prelude)
                    if kind == "skip":
                        skipped_media += 1
                    # a nested media block can only narrow: print inside screen
                    # is still print, and skip anywhere stays skip
                    parent = stack[-1]
                    if parent == "skip" or kind == "skip":
                        stack.append("skip")
                    elif parent == "print" or kind == "print":
                        stack.append("print")
                    else:
                        stack.append("screen")
                    i += 1
                    continue
                if name in ("@supports", "@layer", "@container", "@scope"):
                    # transparent to us: their contents still cascade
                    stack.append(stack[-1])
                    i += 1
                    continue
                # @keyframes, @font-face, @page ... : swallow the whole block
                depth = 1
                i += 1
                while i < n and depth:
                    if css[i] == "{":
                        depth += 1
                    elif css[i] == "}":
                        depth -= 1
                    i += 1
                continue
            # an ordinary rule: read its body to the matching brace
            depth = 1
            j = i + 1
            while j < n and depth:
                if css[j] == "{":
                    depth += 1
                elif css[j] == "}":
                    depth -= 1
                j += 1
            body = css[i + 1:j - 1]
            d = _decls(body)
            if d:
                for sel in prelude.split(","):
                    sel = sel.strip()
                    if sel:
                        order += 1
                        rules.append(Rule(sel, d, stack[-1], order))
            i = j
            continue
        if ch == "}":
            if len(stack) > 1:
                stack.pop()
            buf = []
            i += 1
            continue
        buf.append(ch)
        i += 1
    return rules, skipped_media


def _specificity(selector: str) -> tuple:
    try:
        parsed = css_parse(selector)
    except Exception:
        return (0, 0, 0)
    best = (0, 0, 0)
    for s in parsed:
        try:
            best = max(best, s.specificity())
        except Exception:
            pass
    return best


class ScreenView:
    """Resolves display/visibility for one document under one media context."""

    def __init__(self, tree, media: str = "screen"):
        self.tree = tree
        self.media = media
        css = "\n".join(e.text or "" for e in tree.xpath("//style"))
        self.rules, self.skippedMediaBlocks = parse_css(css)
        self.unreadableSelectors = 0
        self.unreadableHidingSelectors = []
        # element -> {prop: (important, specificity, order, value)}
        self._won: dict = {}
        self._apply()

    def _apply(self):
        for rule in self.rules:
            if rule.media != self.media:
                continue
            try:
                sel = CSSSelector(rule.selector, translator="html")
            except (SelectorError, Exception):
                self.unreadableSelectors += 1
                if any(v in ("none", "hidden") for v, _ in rule.decls.values()):
                    self.unreadableHidingSelectors.append(rule.selector)
                continue
            spec = _specificity(rule.selector)
            try:
                matches = sel(self.tree)
            except Exception:
                self.unreadableSelectors += 1
                continue
            for el in matches:
                slot = self._won.setdefault(el, {})
                for prop, (value, important) in rule.decls.items():
                    key = (1 if important else 0, spec, rule.order)
                    prev = slot.get(prop)
                    if prev is None or key > prev[0]:
                        slot[prop] = (key, value)

    def declared_hidden(self, el) -> bool:
        """True when this element's OWN computed display/visibility hides it."""
        style = (el.get("style") or "").lower()
        inline = _decls(style)
        if inline.get("display", ("", False))[0] == "none":
            return True
        if inline.get("visibility", ("", False))[0] == "hidden":
            return True
        slot = self._won.get(el)
        if slot:
            # an inline non-hiding value beats a stylesheet rule of any
            # specificity unless that rule is !important
            for prop, hide in (("display", "none"), ("visibility", "hidden")):
                won = slot.get(prop)
                if won is None:
                    continue
                (important, _, _), value = won
                if prop in inline and not important:
                    continue
                if value == hide:
                    return True
        return False

    def marked_hidden(self, el) -> bool:
        """Hidden by attribute rather than by style."""
        if el.get("hidden") is not None:
            return True
        return (el.get("aria-hidden") or "").strip().lower() == "true"


def is_staff(el) -> bool:
    if (el.get("data-audience") or "").strip().lower() == STAFF_AUDIENCE:
        return True
    return any(el.get(a) is not None for a in STAFF_ATTRS)


def is_chrome(el) -> bool:
    classes = set((el.get("class") or "").split())
    return any(c in classes for c in CHROME_CLASSES)


# --------------------------------------------------------------------------
# Stages
# --------------------------------------------------------------------------

DECK = ('//main[contains(concat(" ",normalize-space(@class)," ")," deck ")]'
        '|//main[@id="lessonDeck"]')


def _has_class(el, name: str) -> bool:
    return name in (el.get("class") or "").split()


def stages(tree, screen: ScreenView | None = None) -> list:
    """Every pupil TEACHING stage, in document order, in either shell.

    A stage is an element carrying class ``slide`` inside the deck's ``main``.
    It is eligible when nothing ABOVE it (up to and including ``main``) is
    hidden in the screen view -- which is what excludes the print pack, since
    the classic shell hides ``#print-area`` with an unmedia'd rule and re-shows
    it only under ``@media print``.

    The stage's OWN display is deliberately not consulted: ``.slide{display:none}``
    plus ``.slide.active{display:flex}`` is how both shells page through a
    lesson, and treating that as hiding would count one stage in ten.
    """
    if screen is None:
        screen = ScreenView(tree)
    mains = tree.xpath(DECK)
    if not mains:
        return []
    found = []
    for main in mains:
        for el in main.iter():
            if el is main or not isinstance(el.tag, str):
                continue
            if not _has_class(el, "slide"):
                continue
            # eligibility: the chain strictly above the stage, up to main
            ok = True
            parent = el.getparent()
            while parent is not None:
                if screen.declared_hidden(parent) or screen.marked_hidden(parent):
                    ok = False
                    break
                if parent is main:
                    break
                parent = parent.getparent()
            if ok and not any(_has_class(a, "slide") for a in el.iterancestors()):
                found.append(el)
    return found


def stage_pupil_node(stage, screen: ScreenView):
    """A deep copy of one stage with everything that is not pupil teaching text
    removed. The stage itself is the visible root -- see the module docstring."""
    keep_hidden = set()
    for el in stage.iter():
        if el is stage or not isinstance(el.tag, str):
            continue
        if screen.declared_hidden(el) or screen.marked_hidden(el):
            keep_hidden.add(el)
    # mark before copying: identity does not survive deepcopy
    marks = []
    for el in stage.iter():
        if not isinstance(el.tag, str):
            continue
        drop = (
            el is not stage and (
                el.tag.lower() in NON_PUPIL_TAGS
                or is_staff(el)
                or is_chrome(el)
                or el in keep_hidden
            )
        )
        if drop:
            el.set("data-ls-drop", "1")
            marks.append(el)
    node = copy.deepcopy(stage)
    for el in marks:
        del el.attrib["data-ls-drop"]
    for el in list(node.iter()):
        if isinstance(el.tag, str) and el.get("data-ls-drop") == "1":
            parent = el.getparent()
            if parent is not None:
                parent.remove(el)
    return node


# Two adjacent block elements have no whitespace between them in the source, so
# lxml's text_content() returns "...epsilonone more..." and the boundary pair
# counts as ONE word. g18's v1 counter has this defect and every figure it has
# ever printed is short by roughly the number of block boundaries in the deck.
# c-gate already solved it by giving every block element a tail; this does the
# same, so the two instruments agree on where a word ends.
BLOCK_TAGS = {"p", "div", "h1", "h2", "h3", "h4", "h5", "h6", "li", "td", "th",
              "tr", "section", "article", "table", "ul", "ol", "dl", "dt", "dd",
              "blockquote", "figure", "figcaption", "header", "footer", "main",
              "aside", "nav", "br", "hr", "pre", "form", "label", "fieldset",
              "legend", "option", "caption", "summary", "details"}


def stage_text(stage, screen: ScreenView) -> str:
    node = stage_pupil_node(stage, screen)
    for el in node.iter():
        if isinstance(el.tag, str) and el.tag.lower() in BLOCK_TAGS:
            el.tail = " " + (el.tail or "")
            if el.text:
                el.text = " " + el.text
    return " ".join(node.text_content().split())


def words(text: str) -> int:
    return len(WORD.findall(unicodedata.normalize("NFKC", text)))


def shell_of(tree) -> str:
    mains = tree.xpath(DECK)
    if not mains:
        return "none"
    for main in mains:
        if main.xpath('.//*[contains(concat(" ",normalize-space(@class)," ")," slide-container ")]'):
            return "classic"
    if tree.xpath(DECK + '/section[contains(concat(" ",normalize-space(@class)," ")," slide ")]'):
        return "n6"
    return "other"


def parse(path: Path):
    return lh.fromstring(Path(path).read_text(encoding="utf-8"))


def measure(path: Path) -> dict:
    """The one measurement. Every gate that counts pupil content calls this."""
    tree = parse(path)
    screen = ScreenView(tree)
    st = stages(tree, screen)
    rows = []
    for index, s in enumerate(st, 1):
        text = stage_text(s, screen)
        rows.append({
            "stage": index,
            "title": s.get("data-title") or "",
            "type": s.get("data-type") or "",
            "minutes": s.get("data-min"),
            "wordCount": words(text),
            "deliberatePause": (s.get("data-deliberate-pause") or "").strip() or None,
        })
    return {
        "file": str(path),
        "toolVersion": VERSION,
        "shell": shell_of(tree),
        "stages": rows,
        "stageCount": len(rows),
        "totalWords": sum(r["wordCount"] for r in rows),
        "declaredMinutes": [r["minutes"] for r in rows],
        "declaredTotalMinutes": sum(int(float(r["minutes"])) for r in rows if r["minutes"]),
        "skippedMediaBlocks": screen.skippedMediaBlocks,
        "unreadableSelectors": screen.unreadableSelectors,
        "unreadableHidingSelectors": screen.unreadableHidingSelectors,
    }


# --------------------------------------------------------------------------
# Controls. Planted, shown to fire, withdrawn.
# --------------------------------------------------------------------------

_CLASSIC = """<!doctype html><html><head><style>
#print-area{display:none}
.slide{display:none}
.slide.active{display:flex}
.drawer{display:none}
@media print{#print-area{display:block!important}.slide-container{display:none!important}}
@media screen and (max-width:600px){.tight{display:none}}
</style></head><body>
<main id="lessonDeck" class="deck"><div class="slide-container">
  <div class="slide active" data-title="I Do one" data-min="10"><p>alpha beta gamma delta epsilon</p></div>
  <div class="slide" data-title="We Do sort the cards" data-min="10"><p>zeta eta theta iota kappa</p></div>
  <div class="slide" data-title="Independent" data-min="20"><p>lambda mu nu xi omicron</p></div>
</div></main>
<div id="print-area"><div class="print-section"><p>alpha beta gamma delta epsilon</p></div></div>
</body></html>"""

_N6 = """<!doctype html><html><head><style>
.slide{display:none}.slide.active{display:block}
.print-pack{display:none}
@media print{.print-pack{display:block}}
</style></head><body>
<main class="deck">
  <section class="slide active" data-title="I Do" data-min="20"><p>one two three four five</p></section>
  <section class="slide" data-title="We Do" data-min="20"><p>six seven eight nine ten</p></section>
</main>
<section class="print-pack"><p>one two three four five</p></section>
</body></html>"""


def _words_of_html(source: str) -> int:
    tree = lh.fromstring(source)
    screen = ScreenView(tree)
    return sum(words(stage_text(s, screen)) for s in stages(tree, screen))


def _stagecount_of_html(source: str) -> int:
    tree = lh.fromstring(source)
    return len(stages(tree, ScreenView(tree)))


CONTROL_IDS = [
    "every-stage-counted-not-just-active",
    "classic-shell-is-seen",
    "n6-shell-is-seen",
    "print-pack-duplication-is-neutral",
    "one-pupil-paragraph-raises-the-count",
    "staff-audience-drawer-excluded",
    "mbm-guide-drawer-excluded",
    "running-head-excluded",
    "inline-display-none-excluded",
    "css-display-none-excluded",
    "visibility-hidden-excluded",
    "aria-hidden-excluded",
    "hidden-attribute-excluded",
    "media-print-only-block-excluded",
    "script-and-style-excluded",
    "svg-text-not-counted-as-prose",
    "narrow-breakpoint-does-not-delete-text",
    "unreadable-hiding-selector-is-reported",
]


def controls() -> list[dict]:
    """Each control plants a defect (or a must-not-fire case), measures, and
    withdraws it. A gate that cannot be made to fire has measured nothing."""
    out = []

    def record(cid, description, planted, expected, observed):
        out.append({
            "id": cid, "description": description, "planted": planted,
            "expected": expected, "observed": observed,
            "fired": expected == observed,
        })

    base_classic = _words_of_html(_CLASSIC)      # 15 words over 3 stages
    base_n6 = _words_of_html(_N6)                # 10 words over 2 stages

    record("every-stage-counted-not-just-active",
           "the carousel hides 2 of 3 stages with display:none; all 3 must count",
           "nothing - this is the base measurement", 3, _stagecount_of_html(_CLASSIC))

    record("classic-shell-is-seen",
           "main.deck > .slide-container > div.slide is a stage",
           "a classic-shell deck", 15, base_classic)

    record("n6-shell-is-seen",
           "main.deck > section.slide is a stage",
           "an n6-shell deck", 10, base_n6)

    dup = _CLASSIC.replace(
        '<div id="print-area"><div class="print-section"><p>alpha beta gamma delta epsilon</p></div></div>',
        '<div id="print-area"><div class="print-section"><p>alpha beta gamma delta epsilon</p>'
        '<p>zeta eta theta iota kappa</p><p>lambda mu nu xi omicron</p></div></div>')
    record("print-pack-duplication-is-neutral",
           "every stage's text duplicated into the print pack must not change the count",
           "all three stages re-printed into #print-area", base_classic, _words_of_html(dup))

    added = _CLASSIC.replace("<p>alpha beta gamma delta epsilon</p>",
                             "<p>alpha beta gamma delta epsilon</p><p>one more pupil sentence here</p>")
    record("one-pupil-paragraph-raises-the-count",
           "adding one pupil paragraph of 5 words must raise the count by 5",
           "a 5-word pupil paragraph in stage 1", base_classic + 5, _words_of_html(added))

    for cid, marker, desc in [
        ("staff-audience-drawer-excluded", '<div data-audience="staff"><p>staff only words here now</p></div>',
         'data-audience="staff"'),
        ("mbm-guide-drawer-excluded", '<div data-mbm-guide="1"><p>guide only words here now</p></div>',
         "data-mbm-guide"),
        ("running-head-excluded", '<div class="running-head"><p>running head words here now</p></div>',
         "class=running-head"),
        ("inline-display-none-excluded", '<div style="display:none"><p>inline hidden words here now</p></div>',
         "inline display:none"),
        ("aria-hidden-excluded", '<div aria-hidden="true"><p>aria hidden words here now</p></div>',
         'aria-hidden="true"'),
        ("hidden-attribute-excluded", '<div hidden><p>attribute hidden words here now</p></div>',
         "the hidden attribute"),
        ("script-and-style-excluded", '<script>var a = "script words here now";</script><style>.x{color:red}</style>',
         "script and style"),
        ("svg-text-not-counted-as-prose",
         '<svg viewBox="0 0 200 200"><text>svg words here now</text></svg>', "svg text"),
    ]:
        planted = _CLASSIC.replace("<p>alpha beta gamma delta epsilon</p>",
                                   "<p>alpha beta gamma delta epsilon</p>" + marker)
        record(cid, f"{desc} inside a stage is not pupil teaching text",
               marker[:60], base_classic, _words_of_html(planted))

    css_hidden = _CLASSIC.replace(".drawer{display:none}", ".drawer{display:none}") \
        .replace("<p>alpha beta gamma delta epsilon</p>",
                 '<p>alpha beta gamma delta epsilon</p><div class="drawer"><p>css hidden words here now</p></div>')
    record("css-display-none-excluded",
           "a stylesheet display:none inside a stage is not pupil teaching text",
           'class="drawer" with .drawer{display:none}', base_classic, _words_of_html(css_hidden))

    vis = _CLASSIC.replace(".drawer{display:none}", ".drawer{display:none}.vis{visibility:hidden}") \
        .replace("<p>alpha beta gamma delta epsilon</p>",
                 '<p>alpha beta gamma delta epsilon</p><div class="vis"><p>invisible words here now</p></div>')
    record("visibility-hidden-excluded",
           "visibility:hidden inside a stage is not pupil teaching text",
           'class="vis" with visibility:hidden', base_classic, _words_of_html(vis))

    printonly = _CLASSIC.replace("@media print{", "@media print{.ponly{display:block}") \
        .replace(".drawer{display:none}", ".drawer{display:none}.ponly{display:none}") \
        .replace("<p>alpha beta gamma delta epsilon</p>",
                 '<p>alpha beta gamma delta epsilon</p><div class="ponly"><p>print only words here now</p></div>')
    record("media-print-only-block-excluded",
           "a block hidden on screen and shown under @media print is not in the pupil view",
           'class="ponly", display:none on screen, display:block under @media print',
           base_classic, _words_of_html(printonly))

    narrow = _CLASSIC.replace("<p>alpha beta gamma delta epsilon</p>",
                              '<p class="tight">alpha beta gamma delta epsilon</p>')
    record("narrow-breakpoint-does-not-delete-text",
           "a max-width breakpoint must NOT remove pupil text from the projector measurement",
           'class="tight", hidden only under @media screen and (max-width:600px)',
           base_classic, _words_of_html(narrow))

    # nth-child(An+B of S) is valid CSS that cssselect cannot translate. A
    # parser that drops it silently drops a display:none with it, which is a
    # fail-open wearing a clean report, so the omission has to be named.
    bad = _CLASSIC.replace(".drawer{display:none}",
                           ".drawer{display:none}\np:nth-child(2n of .ghost){display:none}")
    tree = lh.fromstring(bad)
    view = ScreenView(tree)
    record("unreadable-hiding-selector-is-reported",
           "a selector the parser cannot read, that would have hidden something, is reported not dropped",
           "p:nth-child(2n of .ghost){display:none}", True,
           len(view.unreadableHidingSelectors) > 0)

    return out


def list_controls() -> list[str]:
    return list(CONTROL_IDS)


def self_test() -> dict:
    results = controls()
    ids = [r["id"] for r in results]
    declared = list_controls()
    missing = [c for c in declared if c not in ids]
    extra = [c for c in ids if c not in declared]
    return {
        "tool": "lesson_stages", "toolVersion": VERSION,
        "controlsDeclared": len(declared), "controlsRun": len(results),
        "controlsFired": sum(1 for r in results if r["fired"]),
        "missingControls": missing, "undeclaredControls": extra,
        "allListedControlsFired": not missing and not extra and all(r["fired"] for r in results),
        "controls": results,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("files", nargs="*")
    ap.add_argument("--list-controls", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--output")
    a = ap.parse_args()

    if a.list_controls:
        for c in list_controls():
            print(c)
        return 0

    if a.self_test:
        report = self_test()
        if a.output:
            out = ROOT / a.output if not Path(a.output).is_absolute() else Path(a.output)
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(json.dumps(report, indent=1) + "\n", encoding="utf-8")
        print(f"lesson_stages self-test  [{VERSION}]")
        for r in report["controls"]:
            print(f"  {'ok  ' if r['fired'] else 'FAIL'} {r['id']:44s} expected={r['expected']} observed={r['observed']}")
        print(f"\n{report['controlsFired']}/{report['controlsRun']} controls fired; "
              f"declared {report['controlsDeclared']}")
        print("PASS" if report["allListedControlsFired"] else "MEASUREMENT INVALID")
        return 0 if report["allListedControlsFired"] else 1

    rows = []
    for f in a.files:
        p = ROOT / f if not Path(f).is_absolute() else Path(f)
        m = measure(p)
        rows.append(m)
        print(f"{Path(f).name[:52]:52s} shell={m['shell']:8s} stages={m['stageCount']:2d} "
              f"words={m['totalWords']:5d} mins={m['declaredTotalMinutes']:3d} [{VERSION}]")
        if m["unreadableHidingSelectors"]:
            print(f"    unreadable hiding selectors: {m['unreadableHidingSelectors']}")
    if a.output:
        out = ROOT / a.output if not Path(a.output).is_absolute() else Path(a.output)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(rows, indent=1) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
