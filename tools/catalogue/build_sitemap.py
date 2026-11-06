#!/usr/bin/env python3
"""Derive sitemap.xml and robots.txt from the catalogue.

The catalogue (resources.json) is the only declaration of what this
repository publishes, so the sitemap is derived from it rather than hand
kept. A hand-kept sitemap has no symptom when it drifts: nothing errors,
the pages simply stop being found. A derived one can be checked.

    python3 tools/catalogue/build_sitemap.py              write sitemap.xml and robots.txt
    python3 tools/catalogue/build_sitemap.py --check      exit 1 if either committed file
                                                          differs from the derivation
    python3 tools/catalogue/build_sitemap.py --self-test  plant every excluded shape on a
                                                          temporary tree and prove each is
                                                          left out, and that --check bites

What goes in: the hub itself, then every catalogue row whose `file` is a
served .html path that exists in the tree. Fragments and query strings are
stripped, so a page that several rows point at appears once.

What stays out, and why:
  * anything under Games/ and under any folder beginning with "_"
    (recreational handoffs and working folders are not Education resources);
  * rows typed `game` (the publisher turns these into data-game-moved
    handoffs, see tools/ux2/resource_sizes.py) and rows typed `teacher`;
  * files whose path names staff, teacher, TA or answer material;
  * non-HTML files (packs, PDFs, spreadsheets), external URLs, and any row
    whose file is missing from the tree. A missing file is reported by
    tools/catalogue/dead_links_plan.json and by the compliance auditor,
    not silently promoted to a URL.

No lastmod is written. A git-derived date would make --check depend on the
depth of the clone it runs in; a file-mtime date would make it depend on
the checkout. The sitemap must be a pure function of the catalogue and the
tree so the same input always gives the same bytes.

The base URL is read from the hub's og:url meta tag in index.html, which is
how the publication already states where it lives. The derivation never
reads the network and never writes outside --root.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import tempfile
from pathlib import Path, PurePosixPath
from urllib.parse import quote
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[2]
CATALOGUE = "resources.json"
HUB = "index.html"
SITEMAP = "sitemap.xml"
ROBOTS = "robots.txt"

SKIP_TOP_FOLDERS = {"Games"}
SKIP_TYPES = {"game", "teacher"}
# Staff-facing material is kept off the crawl surface. The token must stand on
# its own between separators so "Data" or "Stage" never matches.
STAFF_TOKEN = re.compile(r"(?i)(?:^|[\W_])(?:staff|teacher|teachers|ta|answer|answers|markscheme|mark_scheme)(?=[\W_]|$)")
OG_URL = re.compile(r'<meta\s+property="og:url"\s+content="([^"]+)"', re.I)


def base_url(root: Path) -> str:
    """The published location of this tree, as the hub declares it."""
    text = (root / HUB).read_text("utf-8")
    match = OG_URL.search(text)
    if not match:
        raise SystemExit(f"FAIL | base_url | no og:url meta tag in {HUB}")
    url = match.group(1).strip()
    if not url.startswith("https://"):
        raise SystemExit(f"FAIL | base_url | og:url is not https: {url!r}")
    return url if url.endswith("/") else url + "/"


def served_html_path(value: str) -> str | None:
    """A clean relative .html path, or None when the value is not one."""
    if not value or "://" in value:
        return None
    value = value.split("#")[0].split("?")[0].strip().lstrip("/")
    if not value:
        return None
    path = PurePosixPath(value)
    if path.suffix.lower() not in {".html", ".htm"}:
        return None
    if "\\" in value or any(part in {".", ".."} for part in path.parts):
        return None
    return value


def excluded(rel: str, row: dict) -> str | None:
    """The reason a row stays out of the sitemap, or None when it goes in."""
    parts = PurePosixPath(rel).parts
    if parts[0] in SKIP_TOP_FOLDERS:
        return "games folder"
    if any(part.startswith("_") for part in parts):
        return "working folder"
    if str(row.get("type", "")).lower() in SKIP_TYPES:
        return f"type {row.get('type')}"
    if STAFF_TOKEN.search(rel):
        return "staff material"
    return None


def derive_paths(root: Path) -> tuple[list[str], list[tuple[str, str, str]]]:
    """Return (sorted served paths, [(id, file, reason) for every row left out])."""
    rows = json.loads((root / CATALOGUE).read_text("utf-8"))
    if not isinstance(rows, list):
        raise SystemExit(f"FAIL | catalogue | {CATALOGUE} must be a JSON list of rows")
    wanted = {""}  # the hub: the base URL itself
    left_out: list[tuple[str, str, str]] = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        raw = str(row.get("file") or "")
        rel = served_html_path(raw)
        if rel is None:
            left_out.append((str(row.get("id", "")), raw, "not a served html path"))
            continue
        reason = excluded(rel, row)
        if reason:
            left_out.append((str(row.get("id", "")), raw, reason))
            continue
        if not (root / rel).is_file():
            left_out.append((str(row.get("id", "")), raw, "file missing"))
            continue
        wanted.add(rel)
    return sorted(wanted), left_out


def render_sitemap(base: str, paths: list[str]) -> str:
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for rel in paths:
        loc = base + quote(rel, safe="/")
        lines.append(f"  <url><loc>{escape(loc)}</loc></url>")
    lines.append("</urlset>")
    return "\n".join(lines) + "\n"


def render_robots(base: str) -> str:
    return f"User-agent: *\nAllow: /\n\nSitemap: {base}{SITEMAP}\n"


def derive(root: Path) -> dict[str, str]:
    base = base_url(root)
    paths, _ = derive_paths(root)
    return {SITEMAP: render_sitemap(base, paths), ROBOTS: render_robots(base)}


def write(root: Path) -> int:
    base = base_url(root)
    paths, left_out = derive_paths(root)
    (root / SITEMAP).write_text(render_sitemap(base, paths), "utf-8")
    (root / ROBOTS).write_text(render_robots(base), "utf-8")
    print(f"PASS | write | {len(paths)} URLs under {base} -> {SITEMAP}, {ROBOTS}; {len(left_out)} rows left out")
    return 0


def check(root: Path) -> int:
    expected = derive(root)
    failures = 0
    for name, text in expected.items():
        target = root / name
        if not target.is_file():
            print(f"FAIL | check | {name} is not committed; run tools/catalogue/build_sitemap.py")
            failures += 1
            continue
        actual = target.read_text("utf-8")
        count = f" ({text.count('<loc>')} URLs)" if name == SITEMAP else ""
        if actual != text:
            drift = f" (committed {actual.count('<loc>')} URLs, derived {text.count('<loc>')})" if name == SITEMAP else ""
            print(f"FAIL | check | {name} differs from the derivation{drift}; run tools/catalogue/build_sitemap.py")
            failures += 1
        else:
            print(f"PASS | check | {name} matches the derivation{count}")
    return 1 if failures else 0


def self_test() -> int:
    with tempfile.TemporaryDirectory(prefix="sitemap-selftest-") as temp:
        root = Path(temp)
        (root / HUB).write_text('<html><head><meta property="og:url" content="https://example.test/Lessons/"></head></html>', "utf-8")
        pages = {
            "Science/Lesson 1 (2).html", "Science/Teaching_Packs/index.html", "Games/Clash.html",
            "_working/Draft.html", "Art/Teacher_Notes.html", "Art/L4_TA_Sheet.html", "Art/Answers.html",
            "Art/Data_Stage.html", "Summer/Showdown.html", "Science/deck.pptx",
        }
        for rel in pages:
            (root / rel).parent.mkdir(parents=True, exist_ok=True)
            (root / rel).write_text("<html></html>", "utf-8")
        rows = [
            {"id": "ok-space", "type": "lesson", "file": "Science/Lesson 1 (2).html"},
            {"id": "frag-a", "type": "hub", "file": "Science/Teaching_Packs/index.html#build"},
            {"id": "frag-b", "type": "hub", "file": "Science/Teaching_Packs/index.html#grow"},
            {"id": "game-folder", "type": "lesson", "file": "Games/Clash.html"},
            {"id": "working", "type": "lesson", "file": "_working/Draft.html"},
            {"id": "teacher-type", "type": "teacher", "file": "Art/Data_Stage.html"},
            {"id": "teacher-name", "type": "lesson", "file": "Art/Teacher_Notes.html"},
            {"id": "ta-name", "type": "lesson", "file": "Art/L4_TA_Sheet.html"},
            {"id": "answers-name", "type": "lesson", "file": "Art/Answers.html"},
            {"id": "game-type", "type": "game", "file": "Summer/Showdown.html"},
            {"id": "pack", "type": "support", "file": "Science/deck.pptx"},
            {"id": "external", "type": "teacher", "file": "https://example.test/elsewhere"},
            {"id": "missing", "type": "lesson", "file": "Science/Gone.html"},
            {"id": "traversal", "type": "lesson", "file": "../outside.html"},
        ]
        (root / CATALOGUE).write_text(json.dumps(rows), "utf-8")

        paths, left_out = derive_paths(root)
        want = ["", "Science/Lesson 1 (2).html", "Science/Teaching_Packs/index.html"]
        if paths != want:
            print(f"FAIL | self-test | derived {paths}, wanted {want}")
            return 1
        reasons = {i: r for i, _, r in left_out}
        expect = {
            "game-folder": "games folder", "working": "working folder", "teacher-type": "type teacher",
            "teacher-name": "staff material", "ta-name": "staff material", "answers-name": "staff material",
            "game-type": "type game", "pack": "not a served html path", "external": "not a served html path",
            "missing": "file missing", "traversal": "not a served html path",
        }
        if reasons != expect:
            print(f"FAIL | self-test | exclusion reasons {reasons} != {expect}")
            return 1
        sitemap = render_sitemap(base_url(root), paths)
        if "https://example.test/Lessons/Science/Lesson%201%20%282%29.html" not in sitemap:
            print("FAIL | self-test | path was not percent-encoded")
            return 1
        if sitemap.count("<loc>") != 3 or "<loc>https://example.test/Lessons/</loc>" not in sitemap:
            print("FAIL | self-test | hub URL or count wrong")
            return 1

        if check(root) == 0:
            print("FAIL | self-test | --check passed with nothing committed")
            return 1
        write(root)
        if check(root) != 0:
            print("FAIL | self-test | --check failed straight after write")
            return 1
        robots = (root / ROBOTS).read_text("utf-8")
        if "Sitemap: https://example.test/Lessons/sitemap.xml" not in robots:
            print("FAIL | self-test | robots.txt does not point at the sitemap")
            return 1
        (root / "Science/Extra.html").write_text("<html></html>", "utf-8")
        rows.append({"id": "extra", "type": "lesson", "file": "Science/Extra.html"})
        (root / CATALOGUE).write_text(json.dumps(rows), "utf-8")
        if check(root) == 0:
            print("FAIL | self-test | --check did not notice a new catalogue row")
            return 1
        # A changed base URL must move both files.
        write(root)
        (root / HUB).write_text('<html><head><meta property="og:url" content="https://example.test/Moved/"></head></html>', "utf-8")
        if check(root) == 0:
            print("FAIL | self-test | --check did not notice a moved base URL")
            return 1
    print("PASS | self-test | hub + 2 pages kept, 11 planted exclusions named, encoding right, --check red before write, green after, red on drift")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", type=Path, default=ROOT, help="tree to derive from (default: this repository)")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="fail if the committed files differ from the derivation")
    mode.add_argument("--self-test", action="store_true", help="prove the derivation and the check on a planted tree")
    args = parser.parse_args()
    if args.self_test:
        return self_test()
    root = args.root.resolve()
    if args.check:
        return check(root)
    return write(root)


if __name__ == "__main__":
    sys.exit(main())
