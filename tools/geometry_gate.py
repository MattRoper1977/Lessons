#!/usr/bin/env python3
"""The permanent geometry gate: prove the assembled tree is in DRIVE shape.

    python3 tools/geometry_gate.py PACK_DIR [--plant-repo-shape]

Runs BEFORE any zip is written. A run that can reach the zip step in repo shape
will, and has: two previous packs went out assembled from the repo tree, which
looks plausible in a listing and is wrong in every path staff actually click.

THE THREE THINGS THIS CATCHES
-----------------------------
1. Repo-tree names at the root. BUILD_ASDAN/ instead of "ASDAN PEQ/Build/" is an
   instant fail, not a warning - the whole point of the mirror is that the top
   folders drag onto their twins on the drive, and a repo-shaped root has no twin.

2. grow-anim or LundyLoop nested one level deeper than root. This is the
   124-dead-loader failure: 38+ decks reference ../grow-anim/grow-anim.js from a
   known depth, so one extra level silently kills every loader. Silently, because
   a missing script tag throws nothing a person opening the page would notice.

3. A deep page that cannot resolve its own relative links FROM ITS OWN LOCATION.
   Crawling from the root proves nothing about a page four folders down.

THE WHITELIST IS GROUND TRUTH, NOT A PREFERENCE
-----------------------------------------------
It is transcribed from the pass brief's §9.2b block, which is itself the drive's
own listing. TAXONOMY_MAP.md in the repo is the mapping authority and is read
here to cross-check, so a disagreement between the two is detectable rather than
silently resolved in favour of whichever was consulted first.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

# --- §9.2b ground truth ----------------------------------------------------
DRIVE_FOLDERS = {
    "Art", "ASDAN PEQ", "Computing", "Curriculum Intent and Rationale", "English",
    "Feedback and Marking", "grow-anim",
    "Humanities Lessons (Whiteboards and resources)", "Lesson Slideshows_Resources",
    "LundyLoop", "Science_Teesside", "SMSC and BV Calendar Evidence",
    "Tutor Time BF_BV_KCSIE", "Weekly Plans",
}
LOOSE_HUBS = {"art_teesside", "build_asdan", "build_dt_upcycling", "humanities_teesside"}
LOOSE_DOCS = {"CHANGES_SINCE", "HOW_TO_USE_THESE_LESSONS", "README_FIRST",
              # §9.9b handoff ledger. A declared NEW root file - it is not on the
              # drive's own listing, so the placement guide names it under NEW.
              "ASDAN_CHANGES_FOR_PLANNERS"}

# Pack-internal, deliberately NOT drive folders. Each is allowed by name with a
# reason, so a stray directory cannot hide among them.
PACK_INTERNAL = {
    "_Pack_Notes": "build artefacts for Matt - manifest, rulings, placement guide",
    "FONT_LICENCES.txt": "licence text for the fonts vendored into the pages",
    "_New_This_Rebuild": "quarantine for files with no classified destination",
    "index.html": "the generated offline library index (Network_Library only)",
}

# Any of these at root means the repo-tree builder ran. Instant fail.
REPO_SHAPE = {"BUILD_ASDAN", "GROW_ASDAN", "LAUNCH_ASDAN", "Build", "Grow", "Launch",
              "Lessons", "Art_Teesside", "Humanities_Teesside", "DT_Community_Upcycling"}

# Must be present or the pack does not do its job.
REQUIRED = {"ASDAN PEQ", "grow-anim", "LundyLoop", "README_FIRST.txt", "_Pack_Notes"}

# Five deep ASDAN paths, crawled from their own location.
# Five real paths, four folders deep or more, spread across all three lanes and
# including one this pass regenerated. Sampling from the root proves nothing.
DEEP_SAMPLES = [
    "ASDAN PEQ/Launch/START_HERE.html",
    "ASDAN PEQ/Build/Careers/START_HERE.html",
    "ASDAN PEQ/Grow/Community and Enterprise/START_HERE.html",
    "ASDAN PEQ/Build/DT/build_dt_upcycling.html",
    "ASDAN PEQ/Grow/PEQ_L2_Kitchen/Scheme_of_Work.html",
]

HREF = re.compile(r'(?:href|src)\s*=\s*["\']([^"\']+)["\']', re.I)


def stem(name):
    return name.rsplit(".", 1)[0] if "." in name else name


def check_root(pack, problems):
    entries = sorted(p.name for p in pack.iterdir())
    print(f"root entries ({len(entries)}):")
    for e in entries:
        kind = ("DRIVE FOLDER" if e in DRIVE_FOLDERS else
                "loose hub" if stem(e) in LOOSE_HUBS else
                "loose doc" if stem(e) in LOOSE_DOCS else
                "pack-internal" if e in PACK_INTERNAL else
                "UNCLASSIFIED")
        print(f"   {e:<52} {kind}")
        if e in REPO_SHAPE:
            problems.append(f"REPO SHAPE AT ROOT: {e!r} - the repo-tree builder ran")
        elif kind == "UNCLASSIFIED":
            problems.append(f"unclassified root entry {e!r}: not a drive folder, "
                            "not a loose hub or doc, not pack-internal")
    missing = REQUIRED - set(entries)
    if missing:
        problems.append(f"required root entries absent: {sorted(missing)}")
    return entries


def check_siblings(pack, problems):
    """grow-anim and LundyLoop are ROOT SIBLINGS. One extra level kills 38+ loaders."""
    for name in ("grow-anim", "LundyLoop"):
        if not (pack / name).is_dir():
            problems.append(f"{name}/ is not at the root - the loaders will not resolve")
            continue
        # the ONLY other legitimate LundyLoop is inside the Humanities folder
        found = sorted(str(p.relative_to(pack)) for p in pack.rglob(name) if p.is_dir())
        legit = {name, f"Humanities Lessons (Whiteboards and resources)/{name}"}
        stray = [f for f in found if f not in legit]
        print(f"{name}: {len(found)} placement(s) {found}")
        if stray:
            problems.append(f"{name} nested where it must not be: {stray}")


def check_deep(pack, problems):
    print("deep sample crawl, each from its own location:")
    for rel in DEEP_SAMPLES:
        p = pack / rel
        if not p.is_file():
            problems.append(f"deep sample missing: {rel}")
            print(f"   MISSING  {rel}")
            continue
        text = p.read_text(encoding="utf-8", errors="replace")
        dead, absolute, n = [], [], 0
        for raw in HREF.findall(text):
            if raw.startswith(("http:", "https:", "data:", "mailto:", "#", "javascript:")):
                continue
            if raw.startswith("/"):
                absolute.append(raw)
                continue
            n += 1
            target = unquote(urlsplit(raw).path)
            if not target:
                continue
            if not (p.parent / target).exists():
                dead.append(raw)
        print(f"   {'ok  ' if not dead and not absolute else 'FAIL'} {rel}"
              f"  {n} relative link(s), {len(dead)} dead, {len(absolute)} root-absolute")
        if dead:
            problems.append(f"{rel}: {len(dead)} dead relative link(s) e.g. {dead[:3]}")
        if absolute:
            problems.append(f"{rel}: {len(absolute)} root-absolute path(s) e.g. {absolute[:3]}")


def cross_check_taxonomy(repo, problems):
    """TAXONOMY_MAP.md is the mapping authority; disagreement is a STOP, not a preference."""
    tm = repo / "TAXONOMY_MAP.md"
    if not tm.is_file():
        problems.append("TAXONOMY_MAP.md absent from the repo - the mapping has no authority")
        return
    text = tm.read_text(encoding="utf-8")
    dests = re.findall(r"\|\s*`[^`]+`\s*\|\s*`([^`]+)`\s*\|", text)
    roots = {d.split("/", 1)[0] for d in dests}
    roots = {r for r in roots if r}
    unknown = sorted(r for r in roots
                     if r not in DRIVE_FOLDERS and stem(r) not in LOOSE_HUBS | LOOSE_DOCS)
    print(f"TAXONOMY_MAP.md: {len(dests)} mappings, {len(roots)} distinct destination roots")
    if unknown:
        problems.append(f"TAXONOMY_MAP.md maps into roots the §9.2b whitelist does not "
                        f"contain: {unknown} - resolve this, do not prefer one silently")


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        sys.exit("usage: geometry_gate.py PACK_DIR [--plant-repo-shape]")
    pack = Path(args[0])
    repo = Path(__file__).resolve().parent.parent
    if not pack.is_dir():
        sys.exit(f"no such pack directory: {pack}")

    if "--plant-repo-shape" in sys.argv:
        (pack / "LAUNCH_ASDAN").mkdir(exist_ok=True)
        print("*** PLANTED: LAUNCH_ASDAN/ at the assembled root ***")

    problems = []
    cross_check_taxonomy(repo, problems)
    print()
    check_root(pack, problems)
    print()
    check_siblings(pack, problems)
    print()
    check_deep(pack, problems)

    print()
    if problems:
        print(f"[FAIL] geometry gate: {len(problems)} problem(s)")
        for p in problems:
            print(f"   - {p}")
        return 1
    print("[PASS] geometry gate: drive shape, root siblings intact, deep pages resolve")
    return 0


if __name__ == "__main__":
    sys.exit(main())
