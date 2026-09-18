#!/usr/bin/env python3
"""Make the catalogue's title for a landing deck follow the deck's own <h1>.

ORDER SX3-S2 Phase 1, option 1: titles follow the decks. A deck's title is
mirrored in FOUR places (five for a continuation deck) and only one is the source:

    the deck's own <h1>                                   <- THE SOURCE
    data/companion-packs.json          "title"            <- what display-titles reads
    assets/catalogue/science-shelf.json "title"           <- composite; must CONTAIN it
      -> assets/catalogue/lesson-order.json
      -> assets/catalogue/display-titles.json             <- derived
    tools/downloads/definitions/*.json "continuations"    <- separate, not touched here

build_display_titles.py refuses with "Review changed lesson title" unless the
companion-pack title appears verbatim inside the host's shelf title, so both the
pack record and the shelf composite move together or neither does.

The shelf title is a composite,
"LAUNCH GCSE Biology W10L1 · Growth and Differentiation: Building an Organism · 40 minutes",
and only the MIDDLE segment is the lesson title; the lane/course/week prefix and
the duration suffix are never touched.

Refusals, because a title rewrite over a catalogue must damage nothing:
  - the deck has no <h1>
  - the record is in neither resources.json nor science-shelf.json
  - a composite shelf title does not split into exactly three ' · ' segments
  - the middle segment is not what display-titles.json currently lists, which
    would mean this tool has found the wrong segment
  - the old title string does not occur exactly once in the raw file

  python3 tools/sx3/align_shelf_titles.py [--base REF] [--check]
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

from lxml import html as LH

ROOT = Path(__file__).resolve().parents[2]
SHELF = "assets/catalogue/science-shelf.json"
RESOURCES = "resources.json"
DISPLAY = "assets/catalogue/display-titles.json"
COMPANIONS = "data/companion-packs.json"
SEP = " · "


class Refuse(Exception):
    """A condition that makes rewriting unsafe. Never repaired."""


def heading(path: Path) -> str | None:
    doc = LH.fromstring(path.read_bytes())
    for bad in doc.xpath("//script|//style"):
        bad.getparent().remove(bad)
    found = doc.xpath("//h1")
    return " ".join(" ".join(found[0].itertext()).split()) if found else None


def listed(entries) -> dict:
    if isinstance(entries, dict):
        return {k: (v if isinstance(v, str) else v.get("displayTitle") or v.get("title"))
                for k, v in entries.items()}
    out = {}
    for row in entries:
        key = row.get("path") or row.get("file")
        if key:
            out[key] = row.get("displayTitle") or row.get("title")
    return out


def realign(current: str, head: str, shown: str) -> str:
    parts = current.split(SEP)
    if len(parts) == 1:
        if current != shown:
            raise Refuse(f"plain title {current!r} is not the listed title {shown!r}")
        return head
    if len(parts) == 2:
        # A second recorded shape, "<lesson title> · LAUNCH Science": the lesson
        # title comes FIRST and the lane second. Only accepted when the leading
        # segment is exactly what display-titles.json lists, so the tool is never
        # guessing which half is the title.
        if parts[0] != shown:
            raise Refuse(f"two-segment title {current!r} does not lead with the listed "
                         f"title {shown!r}")
        return SEP.join([head, parts[1]])
    if len(parts) != 3:
        raise Refuse(f"composite title does not split into three segments: {current!r}")
    if parts[1] != shown:
        raise Refuse(f"middle segment {parts[1]!r} is not the listed title {shown!r}")
    return SEP.join([parts[0], head, parts[2]])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", default="origin/main",
                        help="the landing set is the decks differing from this ref; "
                             "decks outside it are NOT touched, whatever their titles say")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    shelf = json.loads((ROOT / SHELF).read_text())
    resources = json.loads((ROOT / RESOURCES).read_text())
    shown = listed(json.loads((ROOT / DISPLAY).read_text())["entries"])
    shelf_rows = {row["path"]: row for row in shelf["lessons"] if "path" in row}
    resource_rows = {row["file"]: row for row in resources
                     if isinstance(row, dict) and "file" in row}

    diff = subprocess.run(["git", "diff", "--name-only", f"{args.base}...HEAD", "--",
                           "Science_Teesside/"], cwd=ROOT, capture_output=True, text=True,
                          check=True).stdout.split()
    landing = {p for p in diff if p.endswith(".html")}

    targets = []
    for path, title in sorted(shown.items()):
        if path not in landing:
            continue
        source = ROOT / path
        if not source.is_file():
            continue
        head = heading(source)
        if head is None or head == title:
            continue
        targets.append((path, head, title))

    print(f"SEARCH SCOPE: {len(landing)} deck(s) in the landing set (differing from {args.base}); "
          f"{len(landing & set(shown))} of them listed in {DISPLAY}; {len(targets)} whose <h1> "
          f"differs from the listed title. Decks outside the landing set are not touched.")

    changed, refused = [], []
    for path, head, title in targets:
        try:
            if path in shelf_rows:
                record, where = shelf_rows[path], SHELF
            elif path in resource_rows:
                record, where = resource_rows[path], RESOURCES
            else:
                raise Refuse("in neither the shelf nor resources.json")
            new = realign(record["title"], head, title)
            if new != record["title"]:
                changed.append((path, where, record["title"], new, head))
        except Refuse as exc:
            refused.append((path, str(exc)))

    for path, where, before, after, _ in changed:
        print(f"\n  {path.rsplit('/', 1)[1]}  [{where}]")
        print(f"     before : {before}")
        print(f"     after  : {after}")
    for path, why in refused:
        print(f"\n  REFUSED {path}: {why}")
    print(f"\n  titles realigned : {len(changed)}")
    print(f"  REFUSED          : {len(refused)}")

    if refused:
        return 1
    if args.check:
        return 1 if changed else 0
    if not changed:
        return 0

    companions = json.loads((ROOT / COMPANIONS).read_text())
    by_companion = {pack["companionOf"]: pack for pack in companions["packs"]}
    moved = 0
    for path, _where, _before, _after, head in changed:
        pack = by_companion.get(path)
        if pack is not None and pack["title"] != head:
            pack["title"] = head
            moved += 1
    if moved:
        (ROOT / COMPANIONS).write_text(json.dumps(companions, indent=2, ensure_ascii=False) + "\n")
        print(f"  {COMPANIONS}: {moved} reviewed pack title(s) realigned")

    # Surgical splice, never a JSON round-trip: science-shelf.json does not
    # re-serialise byte-identically (json.dumps turns 34KB into 45KB) and the ten
    # title edits would be buried in a whole-file reformat.
    for where in sorted({row[1] for row in changed}):
        target = ROOT / where
        raw = target.read_text()
        for path, source, before, after, _ in changed:
            if source != where:
                continue
            needle = json.dumps(before, ensure_ascii=False)
            if raw.count(needle) != 1:
                raise Refuse(f"{where}: {before!r} occurs {raw.count(needle)} times, expected once")
            raw = raw.replace(needle, json.dumps(after, ensure_ascii=False))
        target.write_text(raw)
        json.loads(target.read_text())
        print(f"  {where}: rewritten and re-parsed")
    print("  written; now regenerate lesson-order.json, then companion_catalogue/unit_tags, "
          "THEN display-titles last")
    return 0


if __name__ == "__main__":
    sys.exit(main())
