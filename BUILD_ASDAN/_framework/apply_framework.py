#!/usr/bin/env python3
"""Inject the shared ASDAN Teach visual layer into every BUILD_ASDAN lesson deck.

Why inject rather than link a stylesheet?
    Each deck in this suite is a single self-contained .html file. Teachers open
    them straight off a laptop, a USB stick or a shared drive as well as from the
    site, so an external <link>/<script> would break the decks that are not being
    served. Injecting keeps every lesson standalone while still giving the suite
    one source of truth: edit _framework/asdan-teach.{css,js}, re-run this
    script, and all 31 decks update together.

The injected blocks are fenced by HTML comment markers. Re-running replaces the
content between the markers, so the script is idempotent and safe to run as
often as you like. Nothing outside the markers is ever touched — lesson content,
wording, structure and the decks' own styles and scripts are left byte-identical.

Usage
    python3 _framework/apply_framework.py            # update every lesson
    python3 _framework/apply_framework.py --check    # report drift, change nothing
    python3 _framework/apply_framework.py --strip    # remove the layer entirely
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

SUITE = Path(__file__).resolve().parent.parent
FRAMEWORK = SUITE / "_framework"

CSS_START = "<!-- ASDAN-TEACH:CSS:START — generated from _framework/asdan-teach.css, do not edit here -->"
CSS_END = "<!-- ASDAN-TEACH:CSS:END -->"
JS_START = "<!-- ASDAN-TEACH:JS:START — generated from _framework/asdan-teach.js, do not edit here -->"
JS_END = "<!-- ASDAN-TEACH:JS:END -->"

# The trailing \n? is part of the match so that stripping restores the deck
# byte-for-byte — that exactness is what makes the content-integrity check
# in the QA script meaningful.
CSS_BLOCK_RE = re.compile(
    re.escape("<!-- ASDAN-TEACH:CSS:START") + r".*?" + re.escape(CSS_END) + r"\n?",
    re.DOTALL,
)
JS_BLOCK_RE = re.compile(
    re.escape("<!-- ASDAN-TEACH:JS:START") + r".*?" + re.escape(JS_END) + r"\n?",
    re.DOTALL,
)


def lesson_files() -> list[Path]:
    """Every lesson deck in the suite. Hubs and START_HERE indexes are not decks."""
    out: list[Path] = []
    for path in sorted(SUITE.glob("*/*.html")):
        if path.name == "START_HERE.html" or path.parent.name == "_framework":
            continue
        out.append(path)
    return out


def build_css_block() -> str:
    css = (FRAMEWORK / "asdan-teach.css").read_text(encoding="utf-8").strip()
    return f"{CSS_START}\n<style>\n{css}\n</style>\n{CSS_END}\n"


def build_js_block() -> str:
    js = (FRAMEWORK / "asdan-teach.js").read_text(encoding="utf-8").strip()
    return f"{JS_START}\n<script>\n{js}\n</script>\n{JS_END}\n"


def apply(html: str, css_block: str, js_block: str) -> str:
    """Return html with the framework blocks inserted or refreshed."""
    # CSS goes last in <head> so it can build on the deck's own styles.
    if CSS_BLOCK_RE.search(html):
        html = CSS_BLOCK_RE.sub(lambda _: css_block, html, count=1)
    else:
        idx = html.find("</head>")
        if idx == -1:
            raise ValueError("no </head> to insert before")
        html = html[:idx] + css_block + html[idx:]

    # JS goes last in <body> so the deck's own functions already exist to wrap.
    if JS_BLOCK_RE.search(html):
        html = JS_BLOCK_RE.sub(lambda _: js_block, html, count=1)
    else:
        idx = html.rfind("</body>")
        if idx == -1:
            raise ValueError("no </body> to insert before")
        html = html[:idx] + js_block + html[idx:]

    return html


def strip(html: str) -> str:
    html = CSS_BLOCK_RE.sub("", html)
    html = JS_BLOCK_RE.sub("", html)
    return html


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true", help="report drift without writing")
    ap.add_argument("--strip", action="store_true", help="remove the layer from every deck")
    args = ap.parse_args()

    css_block = build_css_block()
    js_block = build_js_block()
    files = lesson_files()
    changed: list[str] = []

    for path in files:
        before = path.read_text(encoding="utf-8")
        try:
            after = strip(before) if args.strip else apply(before, css_block, js_block)
        except ValueError as exc:
            print(f"  !! {path.relative_to(SUITE)}: {exc}", file=sys.stderr)
            return 1
        if after != before:
            changed.append(str(path.relative_to(SUITE)))
            if not args.check:
                path.write_text(after, encoding="utf-8")

    verb = "would change" if args.check else ("stripped" if args.strip else "updated")
    print(f"{len(changed)}/{len(files)} decks {verb}")
    for name in changed:
        print(f"  · {name}")
    if args.check and changed:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
