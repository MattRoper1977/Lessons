#!/usr/bin/env python3
"""SX3 · declare this branch's landing decks as a GLV3 replacement transaction.

_glv3/tools/verify_change_boundary.py protects the whole `Science_Teesside`
prefix (PROTECTED, line 22). A modification to a lesson deck matches none of the
four admitted cases and falls through to the fence at line 347:

    original GLV3 protected-path fence rejected: <deck>

The designed admission is a declared replacement transaction — GLV3's equivalent
of CATALOGUE_PINS — which `replacement_errors` then judges member by member:
exactly the reviewed set and no more, status M, the previous blob identity from
the real merge base, exact bytes, and a matching CATALOGUE_PINS admission.

ONE TRANSACTION PER BRANCH, NOT ONE FOR THE RELEASE. Measured, not assumed: a
single declaration naming all 31 landing decks was judged on claude/sx3-build-1,
where exactly one of them is modified, and returned

    SX3 hypothetical replacement must contain exactly the 31 reviewed file modifications

because `replacement_errors` requires the CHANGED set to equal the DECLARED set
(lines 143-144). A release-wide declaration can therefore never be satisfied on
any single branch. Each branch declares its own members; declaration order is
review order and later declarations supersede earlier claims on the same path,
so the four accumulate on main without colliding.

Every value is DERIVED. `beforeGitBlob` comes from `git ls-tree` at the real
merge base with the base ref, `afterSha256` and `bytes` from the bytes on disk,
and the pin from the CATALOGUE_PINS the deck already carries. Nothing is typed.

Refusals:
  - a deck that is not in this branch's landing set
  - a deck named in the held list
  - a deck with no CATALOGUE_PINS admission, or whose pin disagrees with its bytes
  - a change whose status is not M
  - a member whose bytes are unreadable or which is not a regular file

  python3 tools/build_resources/admit_sx3_release.py --name "<transaction>" [--base REF] [--check]
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BOUNDARY = ROOT / "_glv3/tools/verify_change_boundary.py"
GATE = ROOT / "tools/verify_cross_estate_unification.py"
PREFIX = "Science_Teesside/"

# ORDER SX3-S2: the five GROW _Do decks held on body provenance. They sit at
# main's bytes and so cannot appear as a modification, but they are named here
# too: a hold that depends on a deck happening not to differ is not a hold.
HELD = (
    "Science_Teesside/Grow/W8-W13_2026-27/SCI_G_W9B_Spherical_Bodies_Do.html",
    "Science_Teesside/Grow/W8-W13_2026-27/SCI_G_W10B_Solar_System_Presentation_Do.html",
    "Science_Teesside/Grow/W8-W13_2026-27/SCI_G_W11B_Climate_Action_Do.html",
    "Science_Teesside/Grow/W8-W13_2026-27/SCI_G_W12B_Science_Answer_Lab_Do.html",
    "Science_Teesside/Grow/W8-W13_2026-27/SCI_G_W13B_Rover_Rescue_Investigation_Do.html",
)


class Refuse(Exception):
    """A condition that makes declaring unsafe. Never repaired."""


def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True,
                          check=True).stdout


def merge_base(base: str) -> str:
    return git("merge-base", base, "HEAD").strip()


def pins() -> dict:
    tree = ast.parse(GATE.read_text())
    found = [ast.literal_eval(node.value) for node in tree.body
             if isinstance(node, ast.Assign)
             and any(isinstance(t, ast.Name) and t.id == "CATALOGUE_PINS" for t in node.targets)]
    if len(found) != 1:
        raise Refuse("CATALOGUE_PINS is not a single literal assignment in the gate copy")
    return found[0].get("files", {})


def blob_at(ref: str, rel: str) -> str:
    out = git("ls-tree", ref, "--", rel).split()
    if len(out) < 3 or out[0] != "100644" or out[1] != "blob":
        raise Refuse(f"no regular-file blob at {ref} for {rel}")
    return out[2]


def derive(base: str) -> tuple[str, dict]:
    mb = merge_base(base)
    statuses = {}
    for line in git("diff", "--name-status", f"{mb}..HEAD", "--", PREFIX).splitlines():
        parts = line.split("\t")
        if len(parts) >= 2 and parts[-1].endswith(".html"):
            statuses[parts[-1]] = parts[0][0]

    print(f"SEARCH SCOPE: {len(statuses)} Science .html path(s) differing from the merge base "
          f"{mb[:12]} with {base}; blobs read from that merge base, digests from the bytes on "
          f"disk, pins from CATALOGUE_PINS in {GATE.relative_to(ROOT)}")

    registry = pins()
    files, refused = {}, []
    for rel, status in sorted(statuses.items()):
        try:
            if rel in HELD:
                raise Refuse("named in the held list; a held deck is never admitted")
            if status != "M":
                raise Refuse(f"status is {status!r}, not a modification")
            path = ROOT / rel
            if path.is_symlink() or not path.is_file():
                raise Refuse("not a regular file in the tree")
            data = path.read_bytes()
            digest = hashlib.sha256(data).hexdigest()
            pinned = registry.get(rel)
            if pinned is None:
                raise Refuse("no CATALOGUE_PINS admission; pin it before declaring")
            if pinned != digest:
                raise Refuse(f"pin {pinned[:12]} disagrees with the bytes {digest[:12]}")
            files[rel] = {"beforeGitBlob": blob_at(mb, rel),
                          "afterSha256": digest,
                          "bytes": len(data)}
        except Refuse as exc:
            refused.append((rel, str(exc)))

    for rel, why in refused:
        print(f"  REFUSED {rel}: {why}")
    if refused:
        raise Refuse(f"{len(refused)} deck(s) refused; nothing declared")
    print(f"  derived {len(files)} member(s)")
    return mb, files


def slug(name: str) -> str:
    return re.sub(r"[^A-Z0-9]+", "_", name.upper()).strip("_")


def write(name: str, base_sha: str, files: dict, check: bool) -> bool:
    mark = slug(name)
    var, basevar = f"{mark}_REPLACEMENTS", f"{mark}_REVIEW_BASE"
    text = original = BOUNDARY.read_text()
    if f"{basevar} = " not in text:
        text = text.replace(
            "# BEGIN DECLARED TRANSACTIONS\n",
            f"# SX3 · {name}: this branch's landing decks, re-dressed on the pathway exemplar\n"
            f"# chassis, one transaction, derived and written by\n"
            f"# tools/build_resources/admit_sx3_release.py. Every member also carries a\n"
            f"# CATALOGUE_PINS admission, which replacement_errors cross-checks.\n"
            f"{basevar} = {base_sha!r}\n# BEGIN DECLARED TRANSACTIONS\n", 1)
    block = f"# BEGIN {mark} REPLACEMENTS\n{var} = {files!r}\n# END {mark} REPLACEMENTS\n"
    pattern = rf"# BEGIN {re.escape(mark)} REPLACEMENTS\n.*?# END {re.escape(mark)} REPLACEMENTS\n"
    if re.search(pattern, text, flags=re.S):
        text = re.sub(pattern, lambda _: block, text, flags=re.S)
    else:
        text = text.replace("# END DECLARED TRANSACTIONS\n", block + "# END DECLARED TRANSACTIONS\n", 1)
    entry = f"    {name!r}: ({basevar}, {var}),\n"
    if entry not in text:
        text = text.replace("    # END DECLARED TRANSACTION ENTRIES\n",
                            entry + "    # END DECLARED TRANSACTION ENTRIES\n", 1)
    if not (text.count(entry) == 1 and text.count(f"# BEGIN {mark} REPLACEMENTS") == 1
            and text.count(f"{basevar} = ") == 1):
        raise Refuse("declaration did not land exactly once; refusing to write")
    changed = text != original
    if changed and check:
        print("[FAIL] the declaration differs from the tree; --check writes nothing")
        return True
    if changed:
        BOUNDARY.write_text(text)
        ast.parse(BOUNDARY.read_text())
        print(f"  declared {name!r} with {len(files)} member(s) in {BOUNDARY.relative_to(ROOT)}")
    else:
        print("  declaration already matches the tree")
    return changed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--name", required=True, help="transaction name, e.g. 'SX3 BUILD W12'")
    parser.add_argument("--base", default="origin/main")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        base_sha, files = derive(args.base)
        for rel, entry in sorted(files.items()):
            print(f"     {entry['beforeGitBlob'][:12]} -> {entry['afterSha256'][:12]}  "
                  f"{entry['bytes']:>9,}  {rel.rsplit('/', 1)[1]}")
        changed = write(args.name, base_sha, files, args.check)
    except Refuse as exc:
        print(f"[FAIL] {exc}")
        return 1
    return 1 if (args.check and changed) else 0


if __name__ == "__main__":
    sys.exit(main())
