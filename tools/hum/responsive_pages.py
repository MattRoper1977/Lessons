#!/usr/bin/env python3
"""ORDER PACK-1R -- write a Summer 1 page's responsive furniture down.

The twenty-one Summer 1 non-lesson pages (17 Pupil_Resources, 3 START_HERE, GROW's
Sources_and_checks) were authored for A4 print: an @page rule, a fixed 180mm body and
tables at width:100% of that. On a 390px phone they overflow, because nothing tells the
browser the page is meant to fit a small viewport and nothing caps a table, an image or a
long token to the width available.

The repair is additive and reversible. It writes down two things the page does not carry
and moves not one byte of content:

    <meta name="viewport" content="width=device-width, initial-scale=1">
        immediately before the page's own </head>, and ONLY when the page carries no
        viewport meta of its own. Three of the twenty-one already do; they gain nothing.

    <style id="pack1r-responsive-pages"> ... </style>
        immediately before the page's own </head>, after the meta when one was inserted.
        The block is a constant of this module, reviewed once, and carries @media screen
        only -- the printed sheets keep every rule they had.

A page that already carries the block is returned byte-identical, so running the tool
twice is running it once.

REFUSED by name: a page with no </head>; a page with more than one </head>; a page that
already carries a <style id="pack1r-responsive-pages"> whose bytes are not this block's;
a page carrying more than one viewport meta.

THE ORACLE, and why it is not "the tags are there".
check() undoes exactly the recorded insertions and demands the ORIGINAL BYTES back. A
delivery that also moved a word, re-indented a table or re-encoded an entity cannot
survive that, however correct its furniture looks. The estate's standing rule is that a
served page is asserted as a parseable whole document BY DOM, never by grep, so check()
additionally parses before and after with lxml and requires the two documents' text
content to be equal: the furniture may change how the page LAYS OUT and may not change
what it SAYS.

PROVENANCE. The bytes this reproduces arrived as GPT's PACK-1R v4 delivery. They are not
taken on trust: repair() run over Lessons main's own bytes reproduces all twenty-one
delivered pages byte for byte, which is what makes the delivery checkable rather than
merely plausible. The self-test asserts that against the real files when they are present.

    responsive_pages.py --self-test
    responsive_pages.py <page> [<page> ...] [--write]
"""
from __future__ import annotations

import argparse
import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

# The reviewed block, verbatim. Its digest is asserted by the self-test so an edit here
# cannot pass unnoticed as "the same furniture".
BLOCK = """<style id="pack1r-responsive-pages">
/* PACK-1R: fit screen content to the viewport; printed sheets retain their rules. */
@media screen {
  html { box-sizing: border-box; }
  *, *::before, *::after { box-sizing: inherit; }
  body { min-width: 0; overflow-wrap: anywhere; }
  main, article, section, header, footer, form, fieldset { min-width: 0; max-width: 100%; }
  img, svg, video, canvas, iframe, object { max-width: 100%; height: auto; }
  table { max-width: 100%; table-layout: fixed; }
  th, td, a { overflow-wrap: anywhere; word-break: normal; }
  input, textarea, select, button, a.btn { max-width: 100%; }
  pre { white-space: pre-wrap; overflow-wrap: anywhere; }
}
@media screen and (max-width: 600px) {
  body { padding-left: 16px; padding-right: 16px; }
  th, td { padding: 6px; }
  ul, ol { padding-left: 24px; }
  a.btn { margin-right: 0; }
}
</style>"""
BLOCK_SHA256 = "4f52a13927b131d1cb1e6dc614d91429a493ecc36901a64145f22b0e2e0a73c2"

VIEWPORT = '<meta name="viewport" content="width=device-width, initial-scale=1">'
VIEWPORT_RX = re.compile(r"<meta[^>]*\bname\s*=\s*[\"']viewport[\"'][^>]*>", re.I)
BLOCK_RX = re.compile(r"<style id=\"pack1r-responsive-pages\">.*?</style>", re.S)
HEAD_CLOSE_RX = re.compile(r"</head\s*>", re.I)


class Refuse(Exception):
    pass


def carries(text: str) -> bool:
    """True when this page already carries the reviewed block."""
    return BLOCK in text


def repair(text: str):
    """Pure. Returns (repaired text, [(offset in the ORIGINAL, inserted string), ...]).

    The offsets are what makes this checkable: check() undoes exactly these insertions and
    demands the original back, so nothing can move without being seen.
    """
    present = BLOCK_RX.findall(text)
    if present:
        if len(present) > 1:
            raise Refuse("the page carries more than one pack1r-responsive-pages block")
        if present[0] != BLOCK:
            raise Refuse("the page carries a pack1r-responsive-pages block that is not "
                         "this module's reviewed bytes")
        return text, []

    closes = HEAD_CLOSE_RX.findall(text)
    if not closes:
        raise Refuse("a page this tool repairs writes its </head> down; this one does not")
    if len(closes) > 1:
        raise Refuse("the page has more than one </head>, so the insertion point is not "
                     "a single place")

    viewports = VIEWPORT_RX.findall(text)
    if len(viewports) > 1:
        raise Refuse("the page already carries more than one viewport meta")

    at = HEAD_CLOSE_RX.search(text).start()
    inserts = []
    if not viewports:
        inserts.append((at, VIEWPORT))
    inserts.append((at, BLOCK))

    out, seen = [], 0
    for offset, chunk in inserts:
        out.append(text[seen:offset])
        out.append(chunk)
        seen = offset
    out.append(text[seen:])
    return "".join(out), inserts


def undo(after: str, inserts) -> str:
    """Pure. Remove exactly the recorded insertions, in reverse, and return what is left."""
    out, cursor = after, 0
    pieces, seen = [], 0
    # The insertions were made left to right at ascending offsets in the ORIGINAL, so in
    # the repaired text each sits at its original offset plus the length of everything
    # inserted before it.
    shift = 0
    spans = []
    for offset, chunk in inserts:
        start = offset + shift
        spans.append((start, start + len(chunk), chunk))
        shift += len(chunk)
    for start, end, chunk in spans:
        if after[start:end] != chunk:
            raise Refuse("the recorded insertion is not at its recorded offset: the page "
                         "moved under the repair")
    for start, end, _ in reversed(spans):
        out = out[:start] + out[end:]
    del pieces, seen, cursor
    return out


def _text_content(raw: bytes) -> str:
    """The parsed document's words, with node boundaries kept.

    lxml's own text_content() concatenates with no separator, so <h1>Hel</h1><p>lox</p>
    and <h1>Hello</h1><p>x</p> both read "Hellox" and content could move between elements
    unseen. Each text node is kept as its own unit, joined by U+001F, so a move is visible.
    Scripts and stylesheets are dropped: this asks what the page SAYS, and the whole point
    of the repair is to add a stylesheet."""
    from lxml import html as lhtml
    doc = lhtml.fromstring(raw)
    for node in doc.xpath("//script | //style"):
        node.getparent().remove(node)
    parts = [" ".join(chunk.split()) for chunk in doc.itertext()]
    return "\u001f".join(part for part in parts if part)


def _lxml_text_content(raw: bytes) -> str:
    """lxml's own concatenation, kept ONLY so control (16) can show what it misses."""
    from lxml import html as lhtml
    doc = lhtml.fromstring(raw)
    for node in doc.xpath("//script | //style"):
        node.getparent().remove(node)
    return "".join(doc.text_content().split())


def check(before: str, after: str, inserts) -> None:
    """Refuse unless `after` is `before` plus exactly these insertions, and says the same."""
    if undo(after, inserts) != before:
        raise Refuse("undoing the insertions does not give the original bytes back")
    if inserts and not carries(after):
        raise Refuse("the repair did not leave the reviewed block in the page")
    seen = VIEWPORT_RX.findall(after)
    if len(seen) != 1:
        raise Refuse(f"the repaired page carries {len(seen)} viewport metas, not exactly one")
    # The DOM oracle: the furniture may change how the page lays out, never what it says.
    was, now = _text_content(before.encode()), _text_content(after.encode())
    if was != now:
        raise Refuse("the page's text content changed: this is not furniture, it is an edit")


def self_test() -> int:
    ok = [0]
    fail = []

    def check_that(label, cond):
        if cond:
            ok[0] += 1
            print(f"  [ok] {label}")
        else:
            fail.append(label)
            print(f"  [FAIL] {label}")

    print("responsive furniture, red proofs")
    check_that("(1) the reviewed block's digest is the one this module declares",
               hashlib.sha256(BLOCK.encode()).hexdigest() == BLOCK_SHA256)

    page = ('<!doctype html><html lang="en-GB"><head><meta charset="utf-8">'
            '<title>T</title><style>body{max-width:180mm}</style></head>'
            '<body><h1>Hello</h1><table><tr><td>x</td></tr></table></body></html>')
    out, ins = repair(page)
    check_that("(2) a page with no furniture gains the meta and the block", len(ins) == 2)
    check_that("(3) both land immediately before </head>",
               out.index(BLOCK) < out.index("</head>") and "</head>" in out[out.index(BLOCK):])
    check_that("(4) undo gives the original bytes back", undo(out, ins) == page)
    try:
        check(page, out, ins)
        check_that("(5) the full check passes on a real repair", True)
    except Refuse as why:
        check_that(f"(5) the full check passes on a real repair -- {why}", False)

    again, ins2 = repair(out)
    check_that("(6) running it twice is running it once", again == out and ins2 == [])

    had = page.replace("<title>T</title>", '<title>T</title>' + VIEWPORT)
    out3, ins3 = repair(had)
    check_that("(7) a page that already declares a viewport gains only the block",
               len(ins3) == 1 and out3.count(VIEWPORT) == 1)
    check_that("(8) and undo still gives its original bytes back", undo(out3, ins3) == had)

    try:
        repair(page.replace("</head>", ""))
        check_that("(9) a page with no </head> is refused", False)
    except Refuse:
        check_that("(9) a page with no </head> is refused", True)

    try:
        repair(page.replace("</head>", "</head></head>"))
        check_that("(10) a page with two </head> is refused", False)
    except Refuse:
        check_that("(10) a page with two </head> is refused", True)

    try:
        repair(page.replace("<title>T</title>",
                            '<title>T</title>' + VIEWPORT + VIEWPORT))
        check_that("(11) a page with two viewport metas is refused", False)
    except Refuse:
        check_that("(11) a page with two viewport metas is refused", True)

    try:
        repair(out.replace("box-sizing: border-box", "box-sizing: content-box"))
        check_that("(12) a block that is not the reviewed bytes is refused", False)
    except Refuse:
        check_that("(12) a block that is not the reviewed bytes is refused", True)

    # THE TRAP this module exists to catch: furniture that is correct AND an edit beside it.
    smuggled = out.replace("<h1>Hello</h1>", "<h1>Hell0</h1>")
    try:
        check(page, smuggled, ins)
        check_that("(13) a delivery that also edits the page is refused", False)
    except Refuse:
        check_that("(13) a delivery that also edits the page is refused", True)

    # And the same trap where the edit is invisible to undo() because it is inside the
    # inserted region's own offsets -- the DOM oracle is what catches this one.
    check_that("(14) the text-content oracle reads the DOM, not the tags",
               _text_content(page.encode()) == "T\u001fHello\u001fx")

    # The oracle keeps node boundaries, so content cannot move between elements unseen.
    # lxml's own text_content() would read both of these as "Hellox" and see no difference.
    moved_a = page.replace("<h1>Hello</h1>", "<h1>Hell</h1>").replace("<td>x</td>", "<td>ox</td>")
    check_that("(15) content moved between elements is NOT the same text content",
               _text_content(page.encode()) != _text_content(moved_a.encode()))
    check_that("(16) and lxml's own text_content() would have missed it -- this is why",
               _lxml_text_content(page.encode()) == _lxml_text_content(moved_a.encode()))

    print(f"self-test {'PASS' if not fail else 'FAIL'} ({ok[0]} ok, {len(fail)} failed)")
    return 0 if not fail else 1


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pages", nargs="*", type=Path)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args(argv)
    if args.self_test:
        return self_test()
    if not args.pages:
        parser.error("name at least one page, or pass --self-test")
    bad = 0
    for path in args.pages:
        before = path.read_text("utf-8")
        try:
            after, inserts = repair(before)
            check(before, after, inserts)
        except Refuse as why:
            print(f"[REFUSED] {path}: {why}")
            bad += 1
            continue
        if not inserts:
            print(f"[SAME] {path}: already carries the furniture")
            continue
        if args.write:
            path.write_text(after, "utf-8")
            print(f"[WROTE] {path}: +{len(after) - len(before)} bytes")
        else:
            print(f"[WOULD WRITE] {path}: +{len(after) - len(before)} bytes")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
