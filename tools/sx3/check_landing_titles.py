#!/usr/bin/env python3
"""Two controls over a landing set of lesson decks.

Neither existed when the SX3 release put five GROW `_Do` decks into the landing
set carrying their `_Explore` partner's lesson verbatim. Condition (d) could not
see it — it baselines on each branch's pre-change head, where the wrong content
already sat — and `build_display_titles.py --check` passed throughout, because
display titles derive from the catalogue and never from the deck's own heading.
Nothing compared one deck with another, and nothing compared a deck with the
title it is listed under.

  (i)  DISTINCT. No two decks in the landing set are the same lesson. Checked on
       the `<h1>` and, more sharply, on the whole visible text: the five decks
       that prompted this were byte-for-byte identical to their partners once
       script and style were stripped, so the text digest is what actually
       catches the cause while the `<h1>` catches only the symptom. BLOCKING.

  (ii) LISTED. Each deck's `<h1>` matches the title it is listed under in
       assets/catalogue/display-titles.json, or the divergence is DECLARED by
       name in DECLARED_DIVERGENCES below. A deck with no entry is reported and
       not failed; that is a pre-existing gap, identical on main.

Both are red-proved by --self-test, which requires each to fail on a planted
fault and pass without it.

  python3 tools/sx3/check_landing_titles.py --base origin/main [--self-test]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

from lxml import html as LH

ROOT = Path(__file__).resolve().parents[2]
DISPLAY_TITLES = "assets/catalogue/display-titles.json"

# A divergence recorded here is a REVIEW DECISION: the page heading and the
# listed title are known to differ and that is accepted. Nothing is added here
# to make a check pass; each entry is a deck someone looked at.
DECLARED_DIVERGENCES: dict[str, str] = {}


def run(*args: str) -> str:
    return subprocess.run(args, cwd=ROOT, capture_output=True, text=True, check=True).stdout


def landing_decks(base: str) -> list[str]:
    out = run("git", "diff", "--name-only", f"{base}...HEAD", "--", "Science_Teesside/")
    return sorted(p for p in out.split() if p.endswith(".html"))


def parse(data: bytes):
    doc = LH.fromstring(data)
    for bad in doc.xpath("//script|//style"):
        bad.getparent().remove(bad)
    return doc


def heading(doc) -> str | None:
    found = doc.xpath("//h1")
    return " ".join(" ".join(found[0].itertext()).split()) if found else None


def visible(doc) -> str:
    return " ".join(" ".join(doc.itertext()).split())


def digest(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()[:12]


def listed_titles() -> dict:
    entries = json.loads((ROOT / DISPLAY_TITLES).read_text())["entries"]
    if isinstance(entries, dict):
        return {k: (v if isinstance(v, str) else v.get("displayTitle") or v.get("title"))
                for k, v in entries.items()}
    out = {}
    for row in entries:
        key = row.get("path") or row.get("file")
        if key:
            out[key] = row.get("displayTitle") or row.get("title")
    return out


def distinct_errors(decks: dict[str, tuple[str | None, str]]) -> list[str]:
    errors = []
    for label, index in (("heading", 0), ("visible text", 1)):
        groups: dict[str, list[str]] = {}
        for path, values in decks.items():
            key = values[index]
            if key is None:
                continue
            groups.setdefault(key if index == 0 else digest(key), []).append(path)
        for key, paths in sorted(groups.items()):
            if len(paths) > 1:
                errors.append(f"{len(paths)} decks share a {label} ({key!r}): " + ", ".join(sorted(paths)))
    return errors


def listed_errors(decks: dict[str, tuple[str | None, str]], listed: dict) -> tuple[list[str], list[str]]:
    errors, notes = [], []
    for path, (head, _) in sorted(decks.items()):
        title = listed.get(path)
        if title is None:
            notes.append(f"no display-titles entry: {path}")
        elif title != head:
            if DECLARED_DIVERGENCES.get(path) == head:
                notes.append(f"declared divergence: {path}")
            else:
                errors.append(f"listed as {title!r} but the page is headed {head!r}: {path}")
    return errors, notes


def self_test() -> int:
    def deck(h1: str, body: str) -> bytes:
        return f"<html><body><h1>{h1}</h1><p>{body}</p></body></html>".encode()

    def read(pairs):
        return {p: (heading(parse(d)), visible(parse(d))) for p, d in pairs.items()}

    failures = []
    clean = read({"a.html": deck("Alpha", "one"), "b.html": deck("Beta", "two")})
    if distinct_errors(clean):
        failures.append("DISTINCT fired on a clean set")

    same_head = read({"a.html": deck("Alpha", "one"), "b.html": deck("Alpha", "two")})
    if not any("share a heading" in e for e in distinct_errors(same_head)):
        failures.append("DISTINCT did not fire on two decks sharing a heading")

    # The real fault: different filenames, identical lesson. The heading check alone
    # also catches this one, so the control that matters is the text digest firing
    # when the headings have been made to differ.
    same_text = read({"a.html": deck("Alpha", "one"), "b.html": deck("Alpha", "one")})
    if not any("share a visible text" in e for e in distinct_errors(same_text)):
        failures.append("DISTINCT did not fire on two decks with identical visible text")

    listed = {"a.html": "Alpha", "b.html": "Beta"}
    if listed_errors(clean, listed)[0]:
        failures.append("LISTED fired when every heading matched its listed title")
    if not listed_errors(read({"a.html": deck("Alpha renamed", "one")}), listed)[0]:
        failures.append("LISTED did not fire on a heading that differs from the listed title")
    if listed_errors(read({"a.html": deck("Alpha", "one")}), {})[0]:
        failures.append("LISTED failed a deck that has no entry; that is a note, not a failure")

    for line in failures:
        print(f"[SELF-TEST] {line}")
    print(f"[SELF-TEST] {'PASS' if not failures else 'FAIL'} — {len(failures)} control(s) failed")
    return 1 if failures else 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", default="origin/main")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test and self_test():
        return 1

    paths = landing_decks(args.base)
    print(f"SEARCH SCOPE: {len(paths)} Science .html deck(s) differing from {args.base}, "
          f"read from the working tree; listed titles from {DISPLAY_TITLES}")
    decks = {}
    for path in paths:
        source = ROOT / path
        if not source.is_file():
            continue
        doc = parse(source.read_bytes())
        decks[path] = (heading(doc), visible(doc))

    errors = distinct_errors(decks)
    listed_fail, notes = listed_errors(decks, listed_titles())
    for note in notes:
        print(f"  note: {note}")
    print(f"\n  DISTINCT : {len(errors)} failure(s)")
    for line in errors:
        print(f"     {line}")
    print(f"  LISTED   : {len(listed_fail)} failure(s), {len(DECLARED_DIVERGENCES)} declared")
    for line in listed_fail:
        print(f"     {line}")
    return 1 if errors or listed_fail else 0


if __name__ == "__main__":
    sys.exit(main())
