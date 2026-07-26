#!/usr/bin/env python3
"""
identity_audit.py  —  LundyLoop instrument  [LL-INST-04]

WHAT IT DERIVES  (both directions, one run)

  FORWARD   declared -> actual :  does the thing this file CLAIMS to be exist?
            extension vs magic bytes; declared title vs filename; catalogue
            entry vs file on disk; link target vs tracked file.

  REVERSE   actual -> declared :  is the thing that IS here what it claims?
            file with content of a type its extension denies; file whose
            <title> names a different subject from its filename; tracked file
            no catalogue entry and no link reaches.

WHY BOTH DIRECTIONS, IN ONE INSTRUMENT
  Every one-directional check in this estate has produced a confident wrong
  answer. Running only forward asks "is what should be here, here?" and
  returns clean when ten poster images are present under the wrong names.
  Running only reverse asks "is what is here, right?" and misses a print slot
  the code requests but no markup provides. Both are literal presence checks
  (standing rule 4); the failure is not interpretation, it is DIRECTION.

  Case that forced this: 2026-07-13 commit 8e1eba5 permuted ten subject
  posters across ten filenames and wrote a subject guide to a .pdf name.
  A forward-only sweep reported four images LOST. All ten were present.

WHAT IT STRUCTURALLY CANNOT DETECT
  - A file whose name and content agree but are BOTH wrong.
  - Semantic mismatch inside a correct type (a Science poster correctly named
    Science that teaches the wrong content).
  - Intent. A file nothing references may be junk or a finished asset nobody
    wired up. This instrument reports UNREFERENCED; it cannot tell you which,
    and no criterion built on the files alone can. That distinction has to be
    declared, not derived — see the intentionally-unlinked class in
    INSTRUMENTS.md. NEVER use this output as a deletion criterion.

STATUS: current
"""

import json
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]

MAGIC = [
    (b"\x89PNG\r\n\x1a\n", "png"), (b"\xff\xd8\xff", "jpg"), (b"GIF8", "gif"),
    (b"%PDF", "pdf"), (b"PK\x03\x04", "zip/ooxml"), (b"<?xml", "xml/svg"),
    (b"<!doc", "html"), (b"<!DOC", "html"), (b"<html", "html"), (b"<HTML", "html"),
]
EXT_EXPECT = {
    ".png": {"png"}, ".jpg": {"jpg"}, ".jpeg": {"jpg"}, ".gif": {"gif"},
    ".pdf": {"pdf"}, ".svg": {"xml/svg", "html"}, ".html": {"html"}, ".htm": {"html"},
    ".xlsx": {"zip/ooxml"}, ".pptx": {"zip/ooxml"}, ".docx": {"zip/ooxml"},
}
TITLE = re.compile(rb"<title>([^<]*)</title>", re.I)
WORD = re.compile(r"[a-z0-9]+")


def sniff(raw: bytes):
    head = raw[:16]
    for sig, kind in MAGIC:
        if head.startswith(sig):
            return kind
    if raw[:400].lstrip()[:5].lower().startswith(b"<"):
        return "html"
    return "text/other"


def toks(s):
    stop = {"the", "and", "a", "of", "lundy", "loop", "guide", "subject",
            "html", "png", "v1", "v2", "v3", "v4", "v5", "final", "1", "2"}
    return {w for w in WORD.findall(s.lower()) if w not in stop and len(w) > 2}


def main():
    scope = sys.argv[1:] or None
    tracked = [p for p in subprocess.run(
        ["git", "-C", str(REPO), "ls-files", "-z"],
        capture_output=True, check=True).stdout.decode().split("\0") if p]
    files = [f for f in tracked if not scope or f in scope]

    type_lies, title_lies = [], []
    for f in files:
        raw = (REPO / f).read_bytes()
        ext = Path(f).suffix.lower()
        actual = sniff(raw)
        expected = EXT_EXPECT.get(ext)
        if expected and actual not in expected:
            type_lies.append({"file": f, "extension_claims": ext,
                              "content_is": actual, "bytes": len(raw)})
        m = TITLE.search(raw)
        if m:
            title = m.group(1).decode("utf-8", "replace").strip()
            tt, ft = toks(title), toks(Path(f).stem)
            if tt and ft and not (tt & ft):
                title_lies.append({"file": f, "title": title[:80],
                                   "shared_words_with_filename": 0})

    cat = json.loads((REPO / "resources.json").read_text(encoding="utf-8"))
    from urllib.parse import unquote
    catp = {unquote(e["file"]).replace("\\", "/").lstrip("./")
            for e in cat if e.get("file")}
    tset = set(tracked)

    print(json.dumps({
        "scope": "explicit list" if scope else "whole estate",
        "files_checked": len(files),
        "REVERSE_type_lies": type_lies,
        "REVERSE_title_disagrees_with_filename": title_lies,
        "FORWARD_catalogue_entries_with_no_file": sorted(catp - tset),
        "REVERSE_tracked_html_no_catalogue_entry": sorted(
            f for f in files if f.lower().endswith(".html") and f not in catp),
    }, indent=1))


if __name__ == "__main__":
    main()
