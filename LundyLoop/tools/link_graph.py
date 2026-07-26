#!/usr/bin/env python3
"""
link_graph.py  —  LundyLoop instrument  [LL-INST-02]

WHAT IT DERIVES
  A resolved inbound-link graph for every tracked file: for target T, which
  files reference it, from which line, and with what visible anchor text.

HOW IT DERIVES IT
  Literal. Extracts href= / src= / data-href= / "file": values, resolves each
  relative to the *containing file's directory* (the bug this exists to avoid
  is counting a bare-name grep hit against a same-named file in another
  directory), percent-decodes, drops fragments and query strings, and matches
  against the tracked-file set.

WHAT IT STRUCTURALLY CANNOT DETECT
  - Links built at runtime by string concatenation in JS.
  - Links from outside the repo (bookmarks, printed QR codes, staff pack PDFs,
    a link in an email). "Zero inbound" here means zero *in-repo*, which is
    NOT the same as safe to delete. Say so wherever this number is quoted.
  - Whether a resolved link points at the file the anchor text promises. It
    reports the pairing; a human reads it.

STATUS: current
"""

import json
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path
from posixpath import normpath
from urllib.parse import unquote

REPO = Path(__file__).resolve().parents[2]

ATTR = re.compile(
    rb"""(?:href|src|data-href|data-file|data-src)\s*=\s*["']([^"'>]+)["']""", re.I)
JSONF = re.compile(rb'"file"\s*:\s*"([^"]+)"')
ANCHOR = re.compile(
    rb"""<a\b[^>]*?(?:href)\s*=\s*["']([^"'>]+)["'][^>]*>(.*?)</a>""", re.I | re.S)
TAGS = re.compile(rb"<[^>]+>")
SKIP = re.compile(r"^(https?:|mailto:|tel:|javascript:|data:|#|//)", re.I)


def tracked():
    out = subprocess.run(["git", "-C", str(REPO), "ls-files", "-z"],
                         capture_output=True, check=True).stdout
    return {p for p in out.decode().split("\0") if p}


def resolve(src_file: str, raw: str):
    raw = raw.strip()
    if not raw or SKIP.match(raw):
        return None
    raw = unquote(raw.split("#")[0].split("?")[0])
    if not raw:
        return None
    base = "" if "/" not in src_file else src_file.rsplit("/", 1)[0]
    tgt = raw[1:] if raw.startswith("/") else (f"{base}/{raw}" if base else raw)
    return normpath(tgt).lstrip("./")


def main():
    files = tracked()
    inbound = defaultdict(list)
    unresolved = defaultdict(list)

    for f in sorted(files):
        if not f.lower().endswith((".html", ".htm", ".js", ".json", ".css", ".md")):
            continue
        raw = (REPO / f).read_bytes()
        anchors = {}
        for m in ANCHOR.finditer(raw):
            txt = TAGS.sub(b" ", m.group(2)).decode("utf-8", "replace")
            anchors[m.group(1).decode("utf-8", "replace").strip()] = " ".join(txt.split())[:90]
        offsets = [0]
        for line in raw.split(b"\n"):
            offsets.append(offsets[-1] + len(line) + 1)

        def lineno(pos):
            lo, hi = 0, len(offsets) - 1
            while lo < hi:
                mid = (lo + hi) // 2
                if offsets[mid] <= pos:
                    lo = mid + 1
                else:
                    hi = mid
            return lo

        for pat in (ATTR, JSONF):
            for m in pat.finditer(raw):
                rawlink = m.group(1).decode("utf-8", "replace")
                tgt = resolve(f, rawlink)
                if tgt is None:
                    continue
                rec = {"from": f, "line": lineno(m.start()),
                       "as_written": rawlink,
                       "anchor_text": anchors.get(rawlink.strip(), "")}
                if tgt in files:
                    inbound[tgt].append(rec)
                else:
                    unresolved[f].append({**rec, "resolved_to": tgt})

    targets = sys.argv[1:]
    out = {"inbound": {t: inbound.get(t, []) for t in targets} if targets
           else {t: v for t, v in inbound.items()},
           "orphans_zero_inbound_in_repo": sorted(f for f in files if f not in inbound),
           "broken_links_count": sum(len(v) for v in unresolved.values()),
           "broken_links": {k: v for k, v in sorted(unresolved.items())}}
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
