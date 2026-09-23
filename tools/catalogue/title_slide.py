#!/usr/bin/env python3
"""The deck's own title, read from its TITLE SLIDE.

RULING 2026-09-23 B.2: "the LISTED rule takes the <h1> of the TITLE STAGE (the deck's own
title slide), never the first <h1> in the document."

This lives in its own module because build_science_hub.py builds as it imports, so nothing
can import it to test it. One definition, used by the writer and by its red proof.
"""
from __future__ import annotations
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'hum'))
import deck_dom as D          # the estate's own stage reader -- one definition of a stage, not two

HEADINGS = ('h1', 'h2', 'h3')


def title_slide_heading(text: str) -> str | None:
    """The heading of the deck's own title slide; None when the page carries no slides.

    THE TITLE SLIDE IS STAGE 0, not "the stage deck_dom names 'title'". deck_dom.stage_name()
    returns 'title' for ANY untimed slide it cannot read as the completion marker, so on a deck
    whose opener is timed the only untimed slide is the exit and the name lands there. Measured
    on the 200 Science pages: keying on the name rewrites 77 card titles, most of them wrongly --
    "Photosynthesis: The Light Lab" becomes "Next useful step", "Soil: what is in the mix?"
    becomes "Look closely; keep a trace". Keying on POSITION 0 changes 26, every one an
    improvement, and position 0 is what deck_dom's own evidence records: "data-timer='0' appears
    AT POSITION 0 on 128 landed decks and all 18 Summer 1 decks".

    Heading level is not fixed: measured 174 of 200 title slides use <h1> and 26 use <h2>, so the
    first heading of any level is taken. Five of those 26 are the W8 exemplars whose listed title
    read "Your task * 1 of 2" -- a task slide's <h1>, reached because the title slide has none.

    data-title is the slide's own declaration and is used only where it renders no heading at all.
    """
    slides = D.stages(D.parse(text))
    if not slides:
        return None
    slide = slides[0]
    for node in slide.walk():
        if node is slide:
            continue
        if node.tag in HEADINGS:
            heading = ' '.join(node.inner_text().split()).strip()
            if heading and heading.lower() not in STAGE_LABELS:
                return heading
    declared = (slide.attrs.get('data-title') or '').strip()
    if declared and declared.lower() not in STAGE_LABELS:     # W8B declares data-title="Lesson overview" too
        return declared
    return head_title_name(text)


# HUB1 R3 (ruled 2026-09-23): "W8B's title comes from the deck's <title>/h1, not the stage label."
# A heading that is the NAME OF A STAGE is not the deck's title. Measured over the 145 current
# Science decks: exactly one title slide opens on a label -- SCI_B_W8B, whose title stage is
# <h2>Lesson overview</h2>, <h3>Learning objective</h3>, <h3>Success looks like</h3> and no <h1>
# anywhere -- and the hub listed it as "Do · Lesson overview". Labels are skipped, never guessed
# past: with no real heading and no data-title, the deck's own head <title> names it.
STAGE_LABELS = frozenset({'lesson overview', 'learning objective', 'success looks like'})


def head_title_name(text: str) -> str | None:
    """The deck's own name from its head <title>: the segment before the first ' · '. The rest of
    that title is the deck's pathway and occasion ("Body Science Checkpoint · BUILD · October
    review"), which the card already shows beside the name."""
    import html as H, re
    head = re.search(r'<head\b.*?</head>', text, re.S | re.I)          # the HEAD title: inline SVGs carry their own
    m = re.search(r'<title[^>]*>(.*?)</title>', head.group(0) if head else '', re.S | re.I)
    name = ' '.join(H.unescape(m.group(1)).split()).strip() if m else ''
    name = name.split(' \u00b7 ')[0].strip()
    return name or None


def first_document_h1(text: str) -> str | None:
    """The rule this replaces, kept so the red proof can show what it used to return."""
    from lxml import html as lhtml
    doc = lhtml.fromstring(text.encode('utf-8'))
    for e in doc.iter('h1'):
        got = ' '.join(e.text_content().split()).strip()
        if got:
            return got
    return None
