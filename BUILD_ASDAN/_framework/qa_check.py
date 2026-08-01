#!/usr/bin/env python3
"""QA gate for the ASDAN Teach visual layer.

Proves the two things that must stay true after every change to the framework:

  1 · CONTENT PRESERVED — stripping the injected blocks from each deck restores
      the file byte-for-byte to its committed state. If that holds, the layer
      cannot have altered a single word of lesson content, task instruction,
      answer or assessment text.

  2 · LAYER INTACT — every deck actually carries the current framework, matching
      the source files exactly.

Run from anywhere:  python3 _framework/qa_check.py [--against <git-ref>]
Exits non-zero on any failure so it can gate a commit.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from apply_framework import (  # noqa: E402
    SUITE,
    build_css_block,
    build_js_block,
    lesson_files,
    strip,
)


def committed(ref: str, path: Path) -> str | None:
    """The deck's content at `ref`, or None if it is not tracked there."""
    rel = path.relative_to(SUITE.parent)
    try:
        out = subprocess.run(
            ["git", "show", f"{ref}:{rel.as_posix()}"],
            cwd=SUITE.parent,
            capture_output=True,
            check=True,
        )
    except subprocess.CalledProcessError:
        return None
    return out.stdout.decode("utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--against",
        default="origin/main",
        help="git ref holding the pre-framework decks (default: origin/main)",
    )
    args = ap.parse_args()

    css_block = build_css_block()
    js_block = build_js_block()
    files = lesson_files()

    content_fail: list[str] = []
    layer_fail: list[str] = []
    untracked: list[str] = []

    for path in files:
        rel = str(path.relative_to(SUITE))
        current = path.read_text(encoding="utf-8")

        # 2 · the deck carries the current framework, verbatim
        if css_block not in current or js_block not in current:
            layer_fail.append(rel)

        # 1 · with the layer removed, the deck is exactly what was committed
        baseline = committed(args.against, path)
        if baseline is None:
            untracked.append(rel)
            continue
        if strip(current) != baseline:
            content_fail.append(rel)

    print(f"Checked {len(files)} decks against {args.against}\n")

    if content_fail:
        print(f"FAIL · lesson content changed in {len(content_fail)} deck(s):")
        for name in content_fail:
            print(f"  · {name}")
    else:
        print("PASS · lesson content byte-identical in all decks")

    if layer_fail:
        print(f"\nFAIL · framework missing or stale in {len(layer_fail)} deck(s):")
        for name in layer_fail:
            print(f"  · {name}")
        print("      run: python3 _framework/apply_framework.py")
    else:
        print("PASS · current framework present in all decks")

    if untracked:
        print(f"\nNOTE · {len(untracked)} deck(s) not present at {args.against} (new files):")
        for name in untracked:
            print(f"  · {name}")

    return 1 if (content_fail or layer_fail) else 0


if __name__ == "__main__":
    raise SystemExit(main())
