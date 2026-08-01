#!/usr/bin/env python3
"""Remove CSS rules from the lesson decks that can never match anything.

Every BUILD_ASDAN deck was cloned from an Art lesson template and inherited the
template's full stylesheet, including components the BUILD decks never use — a
biography reader, a fact carousel, a comparison grid, a catch-up banner whose
label still names two Art lessons. Around a hundred lines per deck, thirty-one
decks, none of it reachable.

A selector is treated as dead only when the class it needs appears in NO deck's
markup and in NO deck's JavaScript — checked across the whole suite at once, so
a class used by one lesson is never pruned from another. Grouped selectors are
pruned per-selector, so `.a, .b {}` keeps `.a` when only `.b` is dead.

Deliberately conservative:
  · @keyframes are left alone — they are cheap and referenced by name.
  · The injected ASDAN-TEACH block is skipped entirely.
  · Anything a selector needs that is not a plain class (ids, elements,
    attributes, pseudo-elements) counts as alive.

Verify with _framework/pixel_check.js, which renders every slide of a deck
before and after and requires the images to be identical.

Usage:
    python3 _framework/prune_dead_css.py --report   # list what would go
    python3 _framework/prune_dead_css.py            # prune
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from apply_framework import SUITE, CSS_BLOCK_RE, lesson_files  # noqa: E402

STYLE_RE = re.compile(r"(<style>)(.*?)(</style>)", re.DOTALL)
CLASS_IN_SELECTOR_RE = re.compile(r"\.(-?[_a-zA-Z][\w-]*)")


def deck_without_framework(html: str) -> str:
    return CSS_BLOCK_RE.sub("", html)


def live_classes() -> set[str]:
    """Every class referenced by markup or script anywhere in the suite."""
    live: set[str] = set()
    for path in lesson_files():
        html = deck_without_framework(path.read_text(encoding="utf-8"))
        body = html[html.find("<body") :]
        for attr in re.findall(r'class="([^"]*)"', body):
            live.update(attr.split())
        # Anything a script mentions as a bare word could be applied at runtime.
        for script in re.findall(r"<script>(.*?)</script>", html, re.DOTALL):
            live.update(re.findall(r"[-\w]+", script))
    return live


def split_top_level(css: str) -> list[str]:
    """Split a stylesheet into top-level chunks, respecting nested braces."""
    chunks, depth, start = [], 0, 0
    for i, ch in enumerate(css):
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                chunks.append(css[start : i + 1])
                start = i + 1
    if css[start:].strip():
        chunks.append(css[start:])
    return chunks


COMMENT_RE = re.compile(r"/\*.*?\*/", re.DOTALL)
COMBINATOR_RE = re.compile(r"\s*[>+~]\s*|\s+")


def selector_is_dead(selector: str, live: set[str]) -> bool:
    """True when no element can ever match this selector.

    A compound (`.a.b`) needs every one of its classes at once, so one dead
    class kills it. A full selector needs every compound in its chain, so one
    dead compound kills the selector — `.bio-block .key-fact.revealed` is dead
    once `.bio-block` never exists, whatever the rest requires.
    """
    selector = COMMENT_RE.sub(" ", selector)
    for compound in COMBINATOR_RE.split(selector):
        classes = CLASS_IN_SELECTOR_RE.findall(compound)
        if classes and any(c not in live for c in classes):
            return True
    return False


def prune_chunk(chunk: str, live: set[str], removed: list[str]) -> str:
    stripped = chunk.strip()
    if not stripped:
        return chunk

    # A rule may be introduced by a comment (`/* MOBILE */ @media …`). Look past
    # any leading comments before deciding whether this is an at-rule, or a
    # commented @media's contents never get walked.
    if COMMENT_RE.sub("", stripped).strip().startswith("@"):
        stripped = COMMENT_RE.sub("", stripped).strip()
        at_name = stripped[1:].split(None, 1)[0].split("{")[0].lower()
        # Never touch keyframes; recurse into conditional groups.
        if at_name.startswith("keyframes") or at_name in {"page", "font-face", "charset"}:
            return chunk
        open_brace = chunk.find("{")
        close_brace = chunk.rfind("}")
        if open_brace == -1 or close_brace == -1:
            return chunk
        prelude = chunk[: open_brace + 1]
        inner = chunk[open_brace + 1 : close_brace]
        pruned_inner = "".join(
            prune_chunk(c, live, removed) for c in split_top_level(inner)
        )
        if not pruned_inner.strip():
            return ""
        return prelude + pruned_inner + chunk[close_brace:]

    open_brace = chunk.find("{")
    if open_brace == -1:
        return chunk
    selectors = chunk[:open_brace]
    body = chunk[open_brace:]

    leading = selectors[: len(selectors) - len(selectors.lstrip())]
    kept, dropped = [], []
    for sel in selectors.split(","):
        (dropped if selector_is_dead(sel, live) else kept).append(sel.strip())

    if not dropped:
        return chunk
    removed.extend(dropped)
    if not kept:
        return ""
    return leading + ",".join(kept) + body


def prune_css(css: str, live: set[str], removed: list[str]) -> str:
    return "".join(prune_chunk(c, live, removed) for c in split_top_level(css))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--report", action="store_true", help="list removals, change nothing")
    args = ap.parse_args()

    live = live_classes()
    all_removed: list[str] = []
    changed = 0

    for path in lesson_files():
        html = path.read_text(encoding="utf-8")
        framework = CSS_BLOCK_RE.search(html)
        guard = framework.group(0) if framework else None
        # Hide the framework block so its styles are never pruned.
        working = html.replace(guard, "\x00FRAMEWORK\x00") if guard else html

        removed: list[str] = []

        def repl(m: re.Match) -> str:
            return m.group(1) + prune_css(m.group(2), live, removed) + m.group(3)

        working = STYLE_RE.sub(repl, working)
        if guard:
            working = working.replace("\x00FRAMEWORK\x00", guard)

        if removed:
            all_removed.extend(removed)
            changed += 1
            if not args.report:
                path.write_text(working, encoding="utf-8")

    unique = sorted(set(all_removed))
    verb = "would be removed from" if args.report else "removed from"
    print(f"{len(all_removed)} dead selectors {verb} {changed} deck(s)")
    print(f"{len(unique)} distinct selectors:")
    for sel in unique:
        print(f"  · {sel}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
