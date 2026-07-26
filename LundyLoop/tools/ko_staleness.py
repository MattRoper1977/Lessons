#!/usr/bin/env python3
"""
ko_staleness.py  —  LundyLoop instrument  [LL-INST-08]

WHAT IT DERIVES
  Files whose Knowledge Organiser may have gone stale: the lesson's visible text
  moved in a commit after the KO block's text last moved, AND at least one of the
  moving commits was a CONTENT pass rather than an architecture pass.

WHY TEMPORAL AND NOT SEMANTIC
  "Does this KO correctly summarise its lesson?" needs judgement on 161 files and
  would produce a false-positive chain. That is not the risk anyway. The risk is
  that a KO went stale when its lesson changed underneath it — and staleness is
  temporal. This asks nothing about correctness and reads no content.

TWO REFINEMENTS IT NEEDED, BOTH RECORDED BECAUSE BOTH WERE WRONG FIRST
  v1 asked "has the FILE changed since the KO changed" and returned 161 of 161 —
  every file, which is a statement about the instrument, not the estate. Almost
  every pass in this history touched every lesson with print blocks, TA briefs or
  reduced-motion CSS, none of which a KO summarises.
  v2 keys on VISIBLE TEXT (tags, scripts, styles and data-URIs removed), so a
  commit that only changed markup or CSS does not count as the body moving.
  v3 additionally classifies the moving commits: an architecture pass cannot make
  a KO stale, so files moved only by architecture passes are dropped.

WHAT IT STRUCTURALLY CANNOT DETECT — its own blind twin, stated up front
  A lesson and its KO changed IN THE SAME COMMIT but inconsistently. Co-modification
  is a proxy for consistency, not consistency itself. Files this instrument calls
  clean are UNCHECKED, not verified. That case needs a human, and only on the files
  flagged here.

  It also cannot tell a stale KO from a KO that was always going to differ — a
  summary is not a copy. The output is a CANDIDATE LIST for reading, never a
  defect count.

STATUS: current
"""

import hashlib
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
KO_SLOT = 'id="print-ko"'
DATA = re.compile(r"data:[a-zA-Z0-9.+/-]+;base64,[A-Za-z0-9+/=\s]+")
TAG = re.compile(r"<[^>]+>")
SCRIPTSTYLE = re.compile(r"<(script|style)[^>]*>.*?</\1>", re.S | re.I)

# Passes that add architecture. None of these change anything a KO summarises.
# Add to this list rather than widening it with a fuzzy pattern: a wrong entry here
# silently DROPS a real candidate, which is the expensive direction to be wrong in.
# That happened on the first run: "Pass LL-A2a" was listed here, but it REPLACED the
# Reference Zone with a Conditions Card inside the two assessed files — a content
# change, and the most consequential one in the history. Removed. The lesson is in
# the docstring for a reason; the list is the dangerous part of this instrument.
ARCHITECTURE = re.compile(
    r"^(Pass LL-3|Pass LL-4|Honour prefers-reduced-motion|"
    r"Mobile pathway legend|nv-embed-guard|Add contact footer|Unify branding|"
    r"LundyLoop:|Instruments and|Remove |REGISTER|Sitemap:|Provenance|"
    r"assessed_conditions_gate|INSTRUMENTS:|Tools:|Live-Teach HUD)", re.I)


def sh(*a):
    return subprocess.run(a, capture_output=True, text=True, errors="replace",
                          cwd=str(REPO)).stdout


def visible(src: str) -> str:
    return " ".join(TAG.sub(" ", DATA.sub("D", SCRIPTSTYLE.sub(" ", src))).split())


def ko_text(src: str):
    i = src.find(KO_SLOT)
    if i < 0:
        return None
    j = src.find('id="print-', i + 10)
    return visible(src[i: j if j > 0 else i + 6000])


def h(x):
    return hashlib.sha256(x.encode()).hexdigest()[:10] if x is not None else None


def main():
    files = [p for p in sh("git", "ls-files", "-z", "*.html").split("\0") if p]
    ko_files = [f for f in files if KO_SLOT in sh("git", "show", f"HEAD:{f}")]
    print(f"files carrying a KO block: {len(ko_files)}")

    rows, clean, arch_only = [], 0, 0
    for f in ko_files:
        log = [c for c in sh("git", "log", "--format=%H", "--", f).split("\n") if c]
        seen = []
        for c in log:
            s = sh("git", "show", f"{c}:{f}")
            seen.append((c, h(visible(s)), h(ko_text(s))))

        def last_change(idx):
            for k in range(len(seen) - 1):
                if seen[k][idx] != seen[k + 1][idx]:
                    return k
            return len(seen) - 1

        i_ko, i_body = last_change(2), last_change(1)
        if i_ko <= i_body:
            clean += 1
            continue
        movers = [seen[k][0] for k in range(i_body, i_ko)]
        subjects = [sh("git", "log", "-1", "--format=%s", c).strip() for c in movers]
        content = [s for s in subjects if not ARCHITECTURE.match(s)]
        if not content:
            arch_only += 1
            continue
        rows.append((len(content), f, content))

    assessed = {f for f in ko_files
                if "★ ASSESSED LESSON" in (REPO / f).read_text(encoding="utf-8",
                                                               errors="replace")}
    rows.sort(key=lambda r: (r[1] not in assessed, -r[0]))
    print(f"CANDIDATES (content pass moved the body after the KO): {len(rows)}")
    print(f"dropped — architecture passes only: {arch_only}")
    print(f"clean — KO and body last moved together, or KO later: {clean}")
    total = len(rows) + arch_only + clean
    print(f"cardinality {len(rows)}+{arch_only}+{clean} = {total} == {len(ko_files)} "
          f"-> {total == len(ko_files)}")
    print("\nranked — assessed files first, then by content-commit count:")
    for n, f, c in rows:
        mark = "  ★ASSESSED" if f in assessed else ""
        print(f"  {n:>2}{mark}  {f}")
        print(f"        first content mover: {c[0][:88]}")


if __name__ == "__main__":
    main()
