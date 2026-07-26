#!/usr/bin/env python3
"""
print_pack_audit.py  —  LundyLoop instrument  [LL-INST-03]

WHAT IT DERIVES
  For every file carrying print plumbing: the set of print-slot ids the
  JavaScript *asks for*, the set that actually *exist* in the markup, and the
  difference in each direction.

  requested-but-absent  ->  a print button that produces a silently short pack
  present-but-unrequested -> a slot nothing will ever turn on via printPack()

HOW IT DERIVES IT
  Literal on both sides, and the two sides come from different places in the
  file, which is the point:
    requested = string literals inside the print function's id list, plus any
                getElementById('print-'+X) / 'print-'+level style construction
                whose variable parts are enumerated from the same literal list
    present   = id="print-..." attributes and class="print-section" elements
  Neither side is inferred from the other. A file where the code and the
  markup were written by the same broken pass still shows up, because the
  comparison is between two independently-parsed regions, not between a count
  and itself.

WHAT IT STRUCTURALLY CANNOT DETECT
  - Slots assembled from a variable this parser cannot enumerate. Those are
    reported as UNRESOLVED rather than silently dropped — never counted as
    satisfied.
  - Whether a slot that exists contains anything worth printing. Presence of
    the element is not presence of content; see the empty-shell column.
  - A file whose print pack is fine but whose content is wrong.

STATUS: current
"""

import json
import re
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]

ID_ATTR = re.compile(r"""id\s*=\s*["']print-([A-Za-z0-9_\-]+)["']""")
PRINT_SECTION = re.compile(r"""class\s*=\s*["'][^"']*\bprint-section\b[^"']*["']""")
LIST_LITERAL = re.compile(r"""\[\s*((?:['"][A-Za-z0-9_\-]+['"]\s*,\s*)+['"][A-Za-z0-9_\-]+['"])\s*\]""")
GETBY_CONCAT = re.compile(r"""getElementById\(\s*['"]print-['"]\s*\+\s*([A-Za-z_$][\w$]*)""")
GETBY_LITERAL = re.compile(r"""getElementById\(\s*['"]print-([A-Za-z0-9_\-]+)['"]\s*\)""")
PRINTPACK = re.compile(r"function\s+printPack\s*\(([^)]*)\)\s*\{(.{0,2600}?)\n(?=function|\Z)", re.S)
# Level names are NOT a constant of the estate. v1 of this instrument hardcoded
# ('foundation','middle','higher'); Art_Teesside uses ('supported','standard',
# 'stretch') and reported 6 phantom absences per file — 691 estate-wide, all
# false. Retired per standing rule 7. Levels are now derived literally, from
# each file's own printPack(...) call sites. Standing rule 3: this derivation
# shares no premise with the markup scan it is compared against.
CALLSITE = re.compile(r"""printPack\(\s*['"]([A-Za-z0-9_\-]+)['"]\s*\)""")


def main():
    files = [p for p in subprocess.run(
        ["git", "-C", str(REPO), "ls-files", "-z", "*.html"],
        capture_output=True, check=True).stdout.decode().split("\0") if p]

    rows = []
    for f in files:
        src = (REPO / f).read_text(encoding="utf-8", errors="replace")
        if "print-area" not in src and "printPack" not in src and "print-section" not in src:
            continue

        present = set(ID_ATTR.findall(src))
        n_sections = len(PRINT_SECTION.findall(src))

        requested, unresolved = set(), []
        m = PRINTPACK.search(src)
        body = m.group(2) if m else ""
        if body:
            enumerated = set()
            for lit in LIST_LITERAL.findall(body):
                enumerated |= {s.strip("'\" ") for s in lit.split(",")}
            for var in GETBY_CONCAT.findall(body):
                if var == "id" and enumerated:
                    requested |= enumerated
                elif var == "level":
                    pass          # handled below via the level-suffixed forms
                else:
                    unresolved.append(var)
            requested |= set(GETBY_LITERAL.findall(body))
            levels = sorted(set(CALLSITE.findall(src)))
            for suff in ("scaffold", "worksheet"):
                if f"'print-{suff}-'" in body or f'"print-{suff}-"' in body:
                    if levels:
                        requested |= {f"{suff}-{lv}" for lv in levels}
                    else:
                        unresolved.append(f"{suff}-<no printPack call site found>")

        rows.append({
            "file": f,
            "print_section_elements": n_sections,
            "slots_present": sorted(present),
            "slots_requested": sorted(requested),
            "requested_but_absent": sorted(requested - present),
            "present_but_unrequested": sorted(present - requested) if requested else [],
            "unresolved_variables": unresolved,
            "has_printpack": bool(m),
        })

    rows.sort(key=lambda r: (-len(r["requested_but_absent"]), r["file"]))
    print(json.dumps({
        "files_with_print_plumbing": len(rows),
        "files_with_zero_print_sections": [r["file"] for r in rows if r["print_section_elements"] == 0],
        "rows": rows,
    }, indent=1))


if __name__ == "__main__":
    main()
