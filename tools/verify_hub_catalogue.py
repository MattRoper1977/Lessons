#!/usr/bin/env python3
"""Every hub entry resolves to a catalogue row. ORDER AAV-NIGHT §6c.

WHY THIS EXISTS
---------------
The hub is catalogue-driven: it fetches resources.json and renders what it
finds. That is the design, and it is worth keeping, because the failure mode of
a hand-listed hub is silent -- a link is typed once, the file it points at is
later renamed or retired, and the hub goes on offering it. Nothing errors. A
teacher clicks it in a lesson and gets a 404.

So this checks the one thing the catalogue-driven design cannot check about
itself: any link hard-coded into index.html must ALSO have a catalogue row.
A hub entry with no row is either a link that will rot, or a resource missing
from the catalogue every other surface reads. Both are defects; which one it is
is a judgement for whoever reads the red.

Deliberately NOT checked here: whether the file exists on disk. That is a
different gate's job (the serve proof), and folding the two together would mean
a missing file and an uncatalogued link produce the same message.

    python3 tools/verify_hub_catalogue.py
    python3 tools/verify_hub_catalogue.py --self-test
    python3 tools/verify_hub_catalogue.py --list-controls
"""
from __future__ import annotations
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HUB = ROOT / "index.html"
CATALOGUE = ROOT / "resources.json"
VERSION = "hub-catalogue-v1.0.0"

# Anchors that are navigation, not resource entries.
SKIP = re.compile(r"^(#|https?:|mailto:|index\.html$|404\.html$)")


def catalogue_files(raw: str) -> set[str]:
    rows = json.loads(raw)
    return {(r.get("file") or "").lstrip("./") for r in rows if r.get("file")}


def hub_links(raw: str) -> set[str]:
    out = set()
    for h in re.findall(r'href="([^"]+\.html)"', raw):
        if SKIP.match(h):
            continue
        out.add(h.lstrip("./"))
    return out


def judge(hub_raw: str, cat_raw: str) -> dict:
    links = hub_links(hub_raw)
    files = catalogue_files(cat_raw)
    orphans = sorted(l for l in links if l not in files)
    return {"tool": VERSION, "hubLinks": len(links), "catalogueRows": len(files),
            "orphans": orphans, "status": "RED" if orphans else "PASS"}


def controls() -> list[dict]:
    """The gate has to be able to go red, or its green says nothing."""
    rows = []

    def row(cid, expected, actual):
        rows.append({"id": cid, "expected": expected, "actual": actual,
                     "fired": expected == actual})

    cat = '[{"file":"a/b.html"}]'
    row("aLinkWithARowPasses", "PASS", judge('<a href="a/b.html">x</a>', cat)["status"])
    row("aLinkWithNoRowReds", "RED", judge('<a href="ghost/none.html">x</a>', cat)["status"])
    row("theOrphanIsNamed", ["ghost/none.html"], judge('<a href="ghost/none.html">x</a>', cat)["orphans"])
    # Navigation anchors are not resource entries and must not manufacture reds.
    row("navigationAnchorsAreNotEntries", "PASS",
        judge('<a href="#top">t</a><a href="index.html">h</a><a href="404.html">e</a>'
              '<a href="https://x.test/p.html">o</a>', cat)["status"])
    # A leading ./ is the same link; treating it as different would red the hub
    # for a formatting difference rather than a real orphan.
    row("leadingDotSlashIsTheSameLink", "PASS", judge('<a href="./a/b.html">x</a>', cat)["status"])
    # NEGATIVE control: an empty hub must not be reported as passing for want of
    # anything to check - it passes, but the link count proves it was vacuous.
    row("anEmptyHubIsVisiblyVacuous", 0, judge("<p>no links</p>", cat)["hubLinks"])
    return rows


def main() -> int:
    if "--list-controls" in sys.argv:
        print("\n".join(c["id"] for c in controls()))
        return 0
    if "--self-test" in sys.argv:
        rows = controls()
        for c in rows:
            print(f"  {'ok  ' if c['fired'] else 'FAIL'} {c['id']:34s} "
                  f"expected={c['expected']!r} observed={c['actual']!r}")
        fired = sum(1 for c in rows if c["fired"])
        print(f"{fired}/{len(rows)} controls fired")
        print("PASS" if fired == len(rows) else "MEASUREMENT INVALID")
        return 0 if fired == len(rows) else 1

    rep = judge(HUB.read_text(encoding="utf-8"), CATALOGUE.read_text(encoding="utf-8"))
    print(f"  hub links checked: {rep['hubLinks']}   catalogue rows: {rep['catalogueRows']}")
    for o in rep["orphans"]:
        print(f"  RED  hub entry with no catalogue row: {o}")
    print(f"{rep['status']}  [{VERSION}]")
    return 0 if rep["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
