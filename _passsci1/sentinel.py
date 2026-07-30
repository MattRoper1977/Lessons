#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sentinel emitter — recomputes counts AT EMIT TIME and prints the file list.
No number is ever carried between reports (the cached-claim shape that has bitten this estate).

TWO universes are printed, each labelled, both derived from the SHA at emit time — because
naming only one and calling it "tracked *.html" is exactly the confusion R-G06 exists to kill
(45 / 51 / 76 / 79 / 235 all came from mixing these):

  1. LOOP-MARK sentinel  = tracked *.html files CONTAINING 'll-g:loop-mark' (the lessons).
     This is the meaningful science count: 45 at fork 8540eee -> 70 at merged main.
     EXCLUDES gitignored build artefacts (_passsci1/out, _passsci1/pack) and every non-html
     tooling/doc that merely mentions the string (this emitter, render_v5.py, FINDINGS*.md,
     REGISTER.md, ...). It also drops any _passsci1/ path defensively.

  2. ALL tracked *.html   = `git ls-files '*.html' | wc -l` at the ref. This universe DRIFTS
     with every non-lesson html across the whole estate (~433 at fork, ~459 at merged main).
     It is printed ONLY so a future reader who runs `git ls-files '*.html' | wc -l` sees the
     number it will actually get, next to the label that explains why it is not 70. Never
     quote this number as "the sentinel"; the loop-mark count is the sentinel.

Usage:
  sentinel.py                 # counts at HEAD, write _passsci1/SENTINEL_AFTER.txt
  sentinel.py <ref>           # counts at a ref
  sentinel.py <base> <head>   # delta between two refs (before/after)
"""
import subprocess
import sys
import pathlib

HERE = pathlib.Path(__file__).parent

# The universes, declared exactly (R-G06 corollary): an emitter that names its sentinel joins the
# population it counts, so it MUST state its universe + exclusions in output, not merely enact them.
UNIVERSE_LOOPMARK = ("universe#1 (the sentinel) = tracked *.html CONTAINING 'll-g:loop-mark' "
                     "(git grep -Il 'll-g:loop-mark' -- '*.html'). EXCLUDED by construction: "
                     "gitignored build artefacts (_passsci1/out, _passsci1/pack), any _passsci1/ "
                     "path, and all non-html tooling/docs that merely mention the string "
                     "(this emitter, render_v5.py, FINDINGS*.md, REGISTER.md, ...).")
UNIVERSE_ALLHTML = ("universe#2 (context only, NOT the sentinel) = ALL tracked *.html "
                    "(git ls-files '*.html'). Drifts with every non-lesson html estate-wide; "
                    "printed so a literal `git ls-files '*.html' | wc -l` reader sees its own number.")


def loopmark_files_at(ref):
    r = subprocess.run(["git", "grep", "-I", "-l", "ll-g:loop-mark", ref, "--", "*.html"],
                       capture_output=True, text=True, cwd=HERE.parent)
    out = [l.split(":", 1)[1] for l in r.stdout.splitlines() if ":" in l]
    # Belt-and-braces: even within tracked *.html, drop anything under the emitter's own tooling
    # tree, so the instrument provably cannot count itself. (None today, but declared and enforced.)
    out = [f for f in out if not f.startswith("_passsci1/")]
    return sorted(out)


def all_html_count_at(ref):
    r = subprocess.run(["git", "ls-tree", "-r", "--name-only", ref],
                       capture_output=True, text=True, cwd=HERE.parent)
    return sum(1 for l in r.stdout.splitlines() if l.endswith(".html"))


def main(argv):
    print(f"# {UNIVERSE_LOOPMARK}")
    print(f"# {UNIVERSE_ALLHTML}")
    if len(argv) == 2:
        base = loopmark_files_at(argv[0])
        head = loopmark_files_at(argv[1])
        b, h = set(base), set(head)
        ab, ah = all_html_count_at(argv[0]), all_html_count_at(argv[1])
        print(f"SENTINEL delta — derived at emit time")
        print(f"  [loop-mark *.html]  {argv[0]} = {len(base)}   {argv[1]} = {len(head)}   delta = {len(head) - len(base):+d}")
        print(f"  [ALL tracked *.html] {argv[0]} = {ab}   {argv[1]} = {ah}   delta = {ah - ab:+d}   (context, not the sentinel)")
        added = sorted(h - b)
        removed = sorted(b - h)
        print(f"  LOOP-MARK ADDED ({len(added)}):")
        for f in added:
            print(f"    + {f}")
        if removed:
            print(f"  LOOP-MARK REMOVED ({len(removed)}):")
            for f in removed:
                print(f"    - {f}")
        return
    ref = argv[0] if argv else "HEAD"
    fl = loopmark_files_at(ref)
    allh = all_html_count_at(ref)
    (HERE / "SENTINEL_AFTER.txt").write_text("\n".join(fl) + "\n", encoding="utf-8")
    print(f"SENTINEL at {ref} — derived at emit time")
    print(f"  [loop-mark *.html]   {len(fl)}   (file list -> _passsci1/SENTINEL_AFTER.txt)")
    print(f"  [ALL tracked *.html] {allh}   (context, not the sentinel)")
    for f in fl:
        print(f"  {f}")


if __name__ == "__main__":
    main(sys.argv[1:])
