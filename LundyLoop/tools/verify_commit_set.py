#!/usr/bin/env python3
"""
LL-INST-10 — commit-set assertion.

Asserts that a declared SET of commits is present and carries what it should,
against `git log` rather than against a memory of having built it.

WHY THIS EXISTS (REGISTER.md R-F08). A per-sub-pass cardinality assertion counts
files inside its own scope. Nothing counted the scopes. In Pass LL-G a commit
silently failed to be created; the three sub-passes after it each asserted
15/15/15 and passed. The assertion that eventually fired did so for a reason
unrelated to the defect. A scope-level check cannot detect a missing scope.

KNOWN LIMIT, quote it with the result: this proves the commits exist and touch
the declared paths. It does NOT prove the content of a change is correct — that
is LL-INST-09's job and the in-file gates'. Two green results are two claims.

Usage:
    python3 verify_commit_set.py <base-ref> [<manifest-dir>]

Default manifest-dir is the directory holding subpass1.txt..subpass3.txt.
Exit 0 if every assertion passes, 1 otherwise.
"""
import subprocess
import sys
from preflight import declare_assumptions  # LL-INST-11 (Pass Y)
import os

# The declared shape of Pass LL-G. Edit for a different pass; do not infer it.
DECLARED = [
    dict(n=1, kind="exact",
         paths=["REGISTER.md"],
         must_contain=[("REGISTER.md", "### R-A09 ")]),
    dict(n=2, kind="exact",
         paths=["LundyLoop/tools/INSTRUMENTS.md",
                "LundyLoop/tools/loop_mark_print_gate.py",
                "LundyLoop/tools/verify_commit_set.py"],
         nonempty=["LundyLoop/tools/loop_mark_print_gate.py",
                   "LundyLoop/tools/verify_commit_set.py"]),
    dict(n=3, kind="manifest", manifest="subpass1.txt", count=15),
    dict(n=4, kind="manifest", manifest="subpass2.txt", count=15),
    dict(n=5, kind="manifest", manifest="subpass3.txt", count=15),
]


def git(*a):
    return subprocess.run(["git", *a], capture_output=True, text=True).stdout


def git_rc(*a):
    p = subprocess.run(["git", *a], capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr


def paths_in(sha):
    out = git("show", "--pretty=", "--name-only", sha).strip()
    return sorted(p for p in out.splitlines() if p)


def main(base, mdir):
    declare_assumptions(["full history + base reachable (guarded)", "the DECLARED commit-set shape is hardcoded per pass", "proves paths touched, not content correct"])
    fails = []

    def check(name, ok, detail=""):
        print(f"  {'PASS' if ok else 'FAIL'}  {name}" + (f"   {detail}" if detail else ""))
        if not ok:
            fails.append(name)

    # `base..HEAD` is empty and non-erroring to read if `base` is not in history — on a
    # shallow clone the base commit may sit below the clone's cutoff. Without checking
    # git's exit code, that empty range reports "commit count found 0", which reads as
    # "the commits were never created" when the real cause is an unreachable base. Name
    # the real cause first. (Pass X — earned by the ko_staleness false-zero class.)
    if git("rev-parse", "--is-shallow-repository").strip() == "true":
        print("FAIL — shallow clone: base..HEAD cannot be trusted; the base commit may "
              "be below the history cutoff. Run `git fetch --unshallow` first. "
              "Nothing checked.")
        return 1
    rc, _, _ = git_rc("rev-parse", "--verify", "--quiet", f"{base}^{{commit}}")
    if rc != 0:
        print(f"FAIL — base ref {base!r} does not resolve to a commit in this clone "
              "(unknown ref, or below a shallow cutoff). Nothing checked.")
        return 1

    shas = [s for s in git("rev-list", "--reverse", f"{base}..HEAD").split() if s]

    print(f"=== COMMIT-SET ASSERTION · {base}..HEAD ===\n")
    check(f"commit count == {len(DECLARED)}", len(shas) == len(DECLARED),
          f"found {len(shas)}")
    if len(shas) != len(DECLARED):
        print("\n  Cannot check individual commits against a set of the wrong size.")
        print("\nCOMMIT-SET: FAIL")
        return 1

    seen_lessons = []
    for d, sha in zip(DECLARED, shas):
        short = sha[:7]
        got = paths_in(sha)
        subj = git("log", "-1", "--format=%s", sha).strip()
        print(f"\n  --- commit {d['n']}  {short}  {subj[:58]}")

        if d["kind"] == "exact":
            check(f"c{d['n']} touches exactly {len(d['paths'])} declared path(s)",
                  got == sorted(d["paths"]),
                  f"got {len(got)}")
            for f, needle in d.get("must_contain", []):
                blob = git("show", f"{sha}:{f}")
                check(f"c{d['n']} {f} contains {needle!r}", needle in blob)
            for f in d.get("nonempty", []):
                blob = git("show", f"{sha}:{f}")
                check(f"c{d['n']} {f} present and non-empty", len(blob.strip()) > 0,
                      f"{len(blob)} bytes")

        else:
            mpath = os.path.join(mdir, d["manifest"])
            declared = sorted(l.strip() for l in open(mpath) if l.strip())
            check(f"c{d['n']} manifest {d['manifest']} has {d['count']} rows",
                  len(declared) == d["count"], f"got {len(declared)}")
            check(f"c{d['n']} touched paths == manifest exactly",
                  got == declared, f"touched {len(got)}")
            seen_lessons += got

    print()
    check("lesson files across sub-passes == 45",
          len(seen_lessons) == 45, f"got {len(seen_lessons)}")
    check("no lesson file appears in two sub-passes",
          len(seen_lessons) == len(set(seen_lessons)))
    total = sorted(set(p for s in shas for p in paths_in(s)))
    check("total distinct paths in the set == 49", len(total) == 49,
          f"got {len(total)}")

    print("\nCOMMIT-SET:", "PASS" if not fails else f"FAIL ({len(fails)})")
    return 0 if not fails else 1


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("usage: verify_commit_set.py <base-ref> [manifest-dir]")
    base = sys.argv[1]
    mdir = sys.argv[2] if len(sys.argv) > 2 else "."
    sys.exit(main(base, mdir))
