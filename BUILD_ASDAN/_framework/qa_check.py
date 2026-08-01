#!/usr/bin/env python3
"""QA gate for the ASDAN Teach visual layer.

Proves the two things that must stay true after every change to the framework:

  1 · CONTENT PRESERVED — stripping the injected blocks from each deck leaves
      the file byte-for-byte identical to the recorded baseline. If that holds,
      the layer cannot have altered a single word of lesson content, task
      instruction, answer or assessment text.

  2 · LAYER INTACT — every deck actually carries the current framework, matching
      the source files exactly.

The baseline is a checksum manifest in _framework/.content-baseline.json, so the
gate works in a fresh clone with no network and no git ref to chase. Regenerate
it ONLY when deck content changes on purpose, and say why in the commit:

    python3 _framework/qa_check.py --rebaseline

To check against a git ref instead — useful for proving a whole branch inert:

    python3 _framework/qa_check.py --against origin/main

Run from anywhere. Exits non-zero on any failure so it can gate a commit.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from apply_framework import (  # noqa: E402
    FRAMEWORK,
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


MANIFEST = FRAMEWORK / ".content-baseline.json"


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--against",
        help="compare against a git ref instead of the stored manifest",
    )
    ap.add_argument(
        "--rebaseline",
        action="store_true",
        help="record current stripped decks as the baseline (deck content changed on purpose)",
    )
    args = ap.parse_args()

    css_block = build_css_block()
    js_block = build_js_block()
    files = lesson_files()

    if args.rebaseline:
        manifest = {
            str(p.relative_to(SUITE)): digest(strip(p.read_text(encoding="utf-8")))
            for p in files
        }
        MANIFEST.write_text(json.dumps(manifest, indent=1, sort_keys=True), encoding="utf-8")
        print(f"baseline recorded for {len(manifest)} decks")
        return 0

    stored: dict[str, str] = {}
    if not args.against:
        if not MANIFEST.exists():
            print("no baseline recorded — run with --rebaseline first", file=sys.stderr)
            return 1
        stored = json.loads(MANIFEST.read_text(encoding="utf-8"))

    content_fail: list[str] = []
    layer_fail: list[str] = []
    untracked: list[str] = []

    for path in files:
        rel = str(path.relative_to(SUITE))
        current = path.read_text(encoding="utf-8")

        # 2 · the deck carries the current framework, verbatim
        if css_block not in current or js_block not in current:
            layer_fail.append(rel)

        # 1 · with the layer removed, the deck is exactly what the baseline holds
        if args.against:
            baseline = committed(args.against, path)
            if baseline is None:
                untracked.append(rel)
                continue
            if strip(current) != baseline:
                content_fail.append(rel)
        else:
            if rel not in stored:
                untracked.append(rel)
                continue
            if digest(strip(current)) != stored[rel]:
                content_fail.append(rel)

    source = args.against or "recorded baseline"
    print(f"Checked {len(files)} decks against {source}\n")

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
        print(f"\nNOTE · {len(untracked)} deck(s) not in the baseline (new files):")
        for name in untracked:
            print(f"  · {name}")

    return 1 if (content_fail or layer_fail) else 0


if __name__ == "__main__":
    raise SystemExit(main())
