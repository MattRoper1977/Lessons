#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sentinel emitter — recomputes the ll-g:loop-mark count AT EMIT TIME and prints the file list.
No number is ever carried between reports (the cached-claim shape that has bitten this estate).

Universe: TRACKED *.html files (git). This is the gate's universe (`-- '*.html'`) and it excludes
build artefacts (_passsci1/out, _passsci1/pack are gitignored) and non-html tooling/docs that merely
mention the string. The all-files universe drifts with tooling and is NOT used for the sentinel.

Usage:
  sentinel.py                 # count at HEAD, write _passsci1/SENTINEL_AFTER.txt
  sentinel.py <ref>           # count at a ref
  sentinel.py <base> <head>   # delta between two refs (before/after)
"""
import subprocess
import sys
import pathlib

HERE = pathlib.Path(__file__).parent


# The universe, declared (R-G06 corollary): an emitter that names its sentinel joins the population
# it counts, so it MUST state its exclusions in output, not merely enact them in code.
UNIVERSE = ("universe = TRACKED *.html (git grep -- '*.html'). EXCLUDED by construction: gitignored "
            "build artefacts (_passsci1/out, _passsci1/pack) and all non-html tooling/docs that merely "
            "mention 'll-g:loop-mark' (this emitter, render_v5.py, FINDINGS*.md, REGISTER.md, …).")


def files_at(ref):
    r = subprocess.run(["git", "grep", "-I", "-l", "ll-g:loop-mark", ref, "--", "*.html"],
                       capture_output=True, text=True, cwd=HERE.parent)
    out = [l.split(":", 1)[1] for l in r.stdout.splitlines() if ":" in l]
    # Belt-and-braces: even within tracked *.html, drop anything under the emitter's own tooling
    # tree, so the instrument provably cannot count itself. (None today, but declared and enforced.)
    out = [f for f in out if not f.startswith("_passsci1/")]
    return sorted(out)


def main(argv):
    print(f"# {UNIVERSE}")
    if len(argv) == 2:
        base = files_at(argv[0])
        head = files_at(argv[1])
        b, h = set(base), set(head)
        print(f"SENTINEL (tracked *.html) — derived at emit time")
        print(f"  {argv[0]} = {len(base)}")
        print(f"  {argv[1]} = {len(head)}")
        print(f"  delta = {len(head) - len(base):+d}")
        added = sorted(h - b)
        removed = sorted(b - h)
        print(f"  ADDED ({len(added)}):")
        for f in added:
            print(f"    + {f}")
        if removed:
            print(f"  REMOVED ({len(removed)}):")
            for f in removed:
                print(f"    - {f}")
        return
    ref = argv[0] if argv else "HEAD"
    fl = files_at(ref)
    (HERE / "SENTINEL_AFTER.txt").write_text("\n".join(fl) + "\n", encoding="utf-8")
    print(f"SENTINEL (tracked *.html) at {ref}: {len(fl)}  (file list -> _passsci1/SENTINEL_AFTER.txt)")
    for f in fl:
        print(f"  {f}")


if __name__ == "__main__":
    main(sys.argv[1:])
