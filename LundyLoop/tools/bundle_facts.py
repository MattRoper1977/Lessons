#!/usr/bin/env python3
"""bundle_facts.py — emit one dated OBSERVATION RECORD of the estate's standing figures.

READ-ONLY BY CONSTRUCTION: prints to stdout, writes nothing, stages nothing.
Every figure is emitted beside the exact command that derived it, stamped at HEAD.
A figure whose derivation cannot be trusted prints NOT_DERIVED with the reason —
a truthful null, never a guess (an empty row is a finished row).

WHAT IT KEYS ON (the tell): literal marker strings and git-tracked file extensions.
WHAT IT CANNOT SEE (the unseen sibling): same-purpose content under other wording,
uncommitted working-tree state (it reads HEAD via git), and whether any counted
thing is CORRECT — this bundles cardinalities, not judgements.

The sentinel strings appear in this .py file; the estate's sentinel derivations
carry the pathspec -- '*.html' (R-E10), so this file can never join those counts.

Usage: python3 bundle_facts.py        Exit: 0 emitted · 2 environment refusal.
"""
import subprocess, sys, datetime, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GAME = ROOT / "LundyLoop" / "5_staff_training" / "R_Gate_Calibration_Game.html"
INSTR = ROOT / "LundyLoop" / "tools" / "INSTRUMENTS.md"
STAFF_EXCL = ":(exclude)LundyLoop/5_staff_training/*"

def git(*args):
    r = subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True, text=True)
    return r.returncode, r.stdout, r.stderr

def count_grep(pattern, *pathspec):
    code, out, err = git("grep", "-l", pattern, "--", *pathspec)
    if code not in (0, 1):
        return None, f"git grep failed: {err.strip()}"
    return len([l for l in out.splitlines() if l.strip()]), None

def line(label, value, cmd):
    v = "NOT_DERIVED — " + value[1] if isinstance(value, tuple) else str(value)
    print(f"{label:<46} {v}\n{'':<46} $ {cmd}")

def main():
    code, head, err = git("rev-parse", "HEAD")
    if code != 0:
        print(f"REFUSED: not a git repo at {ROOT} ({err.strip()})", file=sys.stderr); return 2
    head = head.strip()
    print("=" * 78)
    print("OBSERVATION RECORD — not a description of the estate")
    print(f"Derived at HEAD {head[:10]} · {datetime.date.today().isoformat()}")
    print("Figures below were true at this commit only. Re-derive before relying on any.")
    print("=" * 78 + "\n")

    for name, pat in (("loop-mark (BUILD)", "ll-g:loop-mark v1"),
                      ("written line (GROW/LAUNCH)", "What I said, and what it changed")):
        n, e = count_grep(pat, "*.html")
        line(f"Sentinel · {name} · raw", (n, e) if e else n, f"git grep -l '{pat}' -- '*.html'")
        n2, e2 = count_grep(pat, "*.html", STAFF_EXCL)
        line(f"Sentinel · {name} · R-E08 form", (n2, e2) if e2 else n2,
             f"git grep -l '{pat}' -- '*.html' '{STAFF_EXCL}'")
        if e is None and e2 is None and n != n2:
            print(f"{'':<46} !! forms diverge: something in 5_staff_training/ quotes this marker")
        print()

    code, out, _ = git("ls-files", "*.html")
    line("HTML files at HEAD", len(out.splitlines()) if code == 0 else (0, "ls-files failed"),
         "git ls-files '*.html' | wc -l"); print()

    code, out, _ = git("ls-files", "LundyLoop/tools/*.py")
    tools = out.splitlines() if code == 0 else []
    line("Instruments in tools/ (.py)", len(tools), "git ls-files 'LundyLoop/tools/*.py' | wc -l")
    if INSTR.is_file():
        txt = INSTR.read_text(encoding="utf-8", errors="replace")
        hdrs = re.findall(r"^#{2,3}\s+\S+\.py\b", txt, re.M)
        if hdrs:
            line("Entries in INSTRUMENTS.md", len(hdrs), r"grep -cE '^#{2,3} +\S+\.py' INSTRUMENTS.md")
            if len(hdrs) != len(tools):
                print(f"{'':<46} !! census mismatch: {len(tools)} scripts vs {len(hdrs)} entries")
        else:
            line("Entries in INSTRUMENTS.md", (0, "no '## name.py' headings matched — entry format unknown to this instrument"), "manual read required")
    else:
        line("Entries in INSTRUMENTS.md", (0, "file not found at LundyLoop/tools/INSTRUMENTS.md"), "n/a")
    print()

    if GAME.is_file():
        n = len(re.findall(r"\{\s*s\s*:", GAME.read_text(encoding="utf-8", errors="replace")))
        line("Calibration-game scenarios (heuristic)", n, r"grep -cE '\{ *s *:' R_Gate_Calibration_Game.html")
        print(f"{'':<46} (heuristic: counts '{{s:' object literals; a reformat breaks it — confirm on screen)")
    else:
        line("Calibration-game scenarios", (0, "game file not found"), "n/a")
    print()
    print("End of record. Nothing was written by this instrument.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
