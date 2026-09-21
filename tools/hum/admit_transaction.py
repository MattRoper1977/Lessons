#!/usr/bin/env python3
"""ORDER HUM-T · declare this batch's transplanted decks as a GLV3 replacement transaction.

_glv3/tools/verify_change_boundary.py protects the whole `Humanities_Teesside`
prefix. A modification to a lesson deck matches none of its admitted cases and
falls through to the fence:

    original GLV3 protected-path fence rejected: <deck>

The designed admission is a declared replacement transaction, GLV3's equivalent
of CATALOGUE_PINS, which `replacement_errors` then judges member by member:
exactly the declared set and no more, status M, the previous blob identity read
from the real merge base, exact bytes on disk, and a matching CATALOGUE_PINS
admission. This tool declares; it never judges, and it never widens the fence.

ONE TRANSACTION PER BRANCH, NOT ONE FOR THE ORDER. `replacement_errors` requires
the CHANGED set to equal the DECLARED set, so a declaration naming every deck of
the order could never be satisfied on any single batch branch. Declaration order
is review order and a later declaration supersedes an earlier claim on the same
path, so the batches accumulate on main without colliding.

Every value is DERIVED. `beforeGitBlob` comes from `git ls-tree` at the real
merge base with the base ref, `afterSha256` and `bytes` from the bytes on disk,
and the pin from the CATALOGUE_PINS the deck already carries. Nothing is typed.

Refusals:
  - a deck outside the landable set tools/hum/evidence_limb_census.py measures.
    That set is the two digest fences, not a preference: a deck the re-stamp tool
    refuses, or one the David cover pack pins by route, is never declared here.
  - a deck with no CATALOGUE_PINS admission, or whose pin disagrees with its bytes
  - a change whose status is not M
  - a member whose bytes are unreadable, or which is not a regular file

  admit_transaction.py --name "<transaction>" [--base REF] [--check]
  admit_transaction.py --self-test
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BOUNDARY = ROOT / "_glv3/tools/verify_change_boundary.py"
GATE = ROOT / "tools/verify_cross_estate_unification.py"
CENSUS = ROOT / "tools/hum/evidence_limb_census.py"
PREFIX = "Humanities_Teesside/"

# --- SCIENCE LANDABILITY LIMB (Matt Roper, 2026-09-22, ruling on STOP-B2) -------------------
# _glv3 protects Science_Teesside exactly as it protects Humanities_Teesside, so a transplanted
# Science deck needs a declared transaction too -- but the Humanities landable census measures the
# two HUMANITIES digest fences and knows no Science route, so it could only ever answer "no member
# to declare". The ruled Science limb, in the Q1 shape:
#
#   a Science deck is landable when its SCIENCE_WEEK_BINDINGS row EXISTS (the record signed at
#   STOP-SIGN-A), the RECORD's digest equals its pin, and the row's term-week equals the deck's
#   OWN PROJECTION.
#
# "Projection" is the estate's existing notion, not a new one: the two forms tools/sci/
# reprove_bindings.py already accepts as a deck stating its own binding -- the week key token
# (Spr1-W3) or the label (Spring 1 - Week 3). The quote limb is an evidence sentence rather than a
# term-week projection, so it is not one of the two here.
SCIENCE_PREFIX = "Science_Teesside/"
BINDINGS = ROOT / "tools/catalogue/SCIENCE_WEEK_BINDINGS.json"
BINDINGS_PIN_KEY = "tools/catalogue/SCIENCE_WEEK_BINDINGS.json"
# STOP-B3 (Matt Roper, 2026-09-22). The limb as first ruled accepted two forms of projection,
# and MEASURED over the 180 bound science routes it admitted 49 of them: 19 more state their
# week only as the SoW CELL their own lesson-config names, and 108 state nothing at all. PASS B
# batch 1 was 0 of 12 landable under it. The ruling widens the accepted forms to four, matching
# the STOP-T3 Q1 shape on the Humanities side:
#
#   (i)   the week key token          Spr1·W3, in the deck's own text
#   (ii)  the week label              Spring 1 · Week 3, in the deck's own text
#   (iii) the SoW-cell chain          the deck's own lesson-config names a workbook cell, and
#                                     the SIGNED calendar spine maps that cell to a term-week
#   (iv)  the signed row alone        where the deck projects NOTHING by (i)-(iii), the signed
#                                     SCIENCE_WEEK_BINDINGS row proves it: row present, and the
#                                     record's digest equal to its CATALOGUE_PINS entry
#
# A deck that projects a DIFFERENT week from its row still refuses — that is the one case (iv)
# must never swallow, and it is red-proved below. Both records the limb reads are pinned, and a
# drifted one refuses every deck rather than letting a stale row through.
SPINE = ROOT / "_sownb/CALENDAR_SPINE.json"
SPINE_PIN_KEY = "_sownb/CALENDAR_SPINE.json"
WEEK_TOKEN = re.compile(r"(Aut[12]|Spr[12]|Sum[12])\u00b7W(\d+)")
WEEK_LABEL = re.compile(r"(Autumn|Spring|Summer) ([12]) \u00b7 Week (\d+)")
LABEL_TERM = {"Autumn": "Aut", "Spring": "Spr", "Summer": "Sum"}
TERM_LABEL = {"Aut1": "Autumn 1", "Aut2": "Autumn 2", "Spr1": "Spring 1",
              "Spr2": "Spring 2", "Sum1": "Summer 1", "Sum2": "Summer 2"}
STRANDS = {"Humanities": PREFIX, "Science": SCIENCE_PREFIX}


def flat_text(data: bytes) -> str:
    """The deck's visible text, tags stripped and whitespace flattened -- the same shape
    tools/sci/reprove_bindings.py reads a projection out of."""
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", data.decode("utf-8", "replace")))


def config_cells(data: bytes) -> set:
    """Pure. The workbook cells the deck's OWN lesson-config names, as spine references.
    Read from the raw bytes, because the config is a <script> body and flat_text strips it."""
    out = set()
    for body in re.findall(r"<script[^>]*id=[\"']lesson-config[\"'][^>]*>(.*?)</script>",
                           data.decode("utf-8", "replace"), re.S | re.I):
        try:
            source = json.loads(body).get("source") or {}
        except Exception:
            continue
        sheet, cell = source.get("sheet"), source.get("cell")
        if sheet and cell:
            out.add("'%s'!%s" % (sheet, cell))
    return out


def projected(text: str, cells: set, spine: dict) -> set:
    """Pure. EVERY term-week this deck states about itself, by any of the three reading forms.
    Not narrowed to the record's own weeks: a deck that names a week its row does not bind must
    be visible here, or the mismatch below could not refuse it."""
    out = {"%s\u00b7W%d" % (m[1], int(m[2])) for m in WEEK_TOKEN.finditer(text)}
    out |= {"%s%s\u00b7W%d" % (LABEL_TERM[m[1]], m[2], int(m[3])) for m in WEEK_LABEL.finditer(text)}
    for ref in cells:
        row = spine.get(ref)
        if row and row.get("termWeek"):
            out.add(row["termWeek"])
    return out


def judge_science(rel, entry, record_ok, text, cells=frozenset(), spine=None, spine_ok=True):
    """Pure. None when the ruled Science limb makes this deck landable, else the reason."""
    if not record_ok:
        return "the SCIENCE_WEEK_BINDINGS record's digest does not equal its pin"
    if not spine_ok:
        return "the calendar spine's digest does not equal its pin"
    if entry is None:
        return "no SCIENCE_WEEK_BINDINGS row; the signed record does not bind it"
    if not (entry.get("weeks") or []):
        return "the record binds it to no week, so there is no term-week to project"
    want = {w["key"] for w in entry["weeks"]}
    got = projected(text, set(cells), spine or {})
    if not got:
        return None  # form (iv): the deck states nothing, and the signed row proves it
    if want <= got:
        return None  # forms (i)-(iii): every bound week is one the deck states about itself
    return ("the deck states %s about itself, which does not cover the record's term-week (%s)"
            % (", ".join(sorted(got)), ", ".join(sorted(want))))


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


def landable(revision: str) -> set:
    """The decks the census proves may move, at the same revision the gate compares with."""
    out = subprocess.run([sys.executable, str(CENSUS), "--json", "--revision", revision],
                         cwd=ROOT, capture_output=True, text=True)
    if out.returncode:
        raise Refuse("the landable census could not be taken: " + out.stderr.strip()[:200])
    return {row["path"] for row in json.loads(out.stdout)["rows"] if row["landable"]}


def blob_at(ref: str, rel: str) -> str:
    out = git("ls-tree", ref, "--", rel).split()
    if len(out) < 3 or out[0] != "100644" or out[1] != "blob":
        raise Refuse(f"no regular-file blob at {ref} for {rel}")
    return out[2]


def judge_member(rel, status, allowed, pinned, digest):
    """The refusal rule, pure so the self-test plants against the code that judges.

    Returns None when the member may be declared, or the reason it may not."""
    if rel not in allowed:
        return "outside the landable set the census measures; the fences hold it"
    if status != "M":
        return f"status is {status!r}, not a modification"
    if pinned is None:
        return "no CATALOGUE_PINS admission; pin it before declaring"
    if pinned != digest:
        return f"pin {pinned[:12]} disagrees with the bytes {digest[:12]}"
    return None


def science_allowed(paths) -> tuple[set, dict]:
    """The ruled Science limb, applied to the paths this branch changed.

    Returns (landable set, reason per refused path). The record is read once and its digest
    compared with its CATALOGUE_PINS entry, so a record that has drifted refuses every deck
    rather than letting one through on a stale row."""
    registry = pins()
    raw = BINDINGS.read_bytes()
    record_ok = registry.get(BINDINGS_PIN_KEY) == hashlib.sha256(raw).hexdigest()
    entries = json.loads(raw)["entries"]
    # The cell chain (form iii) reads the calendar spine, so the spine is held to the same
    # standard as the bindings record: a digest that is not its pin refuses every deck.
    spine_raw = SPINE.read_bytes() if SPINE.is_file() else b""
    spine_ok = bool(spine_raw) and registry.get(SPINE_PIN_KEY) == hashlib.sha256(spine_raw).hexdigest()
    spine = {row["reference"]: row
             for row in (json.loads(spine_raw)["workbookCells"] if spine_ok else [])}
    ok, why = set(), {}
    for rel in paths:
        path = ROOT / rel
        data = path.read_bytes() if path.is_file() and not path.is_symlink() else b""
        text = flat_text(data) if data else ""
        reason = judge_science(rel, entries.get(rel), record_ok, text,
                               config_cells(data), spine, spine_ok)
        if reason:
            why[rel] = reason
        else:
            ok.add(rel)
    return ok, why


def derive(base: str, strand: str = "Humanities") -> tuple[str, dict]:
    prefix = STRANDS[strand]
    mb = merge_base(base)
    statuses = {}
    for line in git("diff", "--name-status", f"{mb}..HEAD", "--", prefix).splitlines():
        parts = line.split("\t")
        if len(parts) >= 2 and parts[-1].endswith(".html"):
            statuses[parts[-1]] = parts[0][0]

    print(f"SEARCH SCOPE: {len(statuses)} {strand} .html path(s) differing from the merge "
          f"base {mb[:12]} with {base}; blobs read from that merge base, digests from the "
          f"bytes on disk, pins from CATALOGUE_PINS in {GATE.relative_to(ROOT)}")

    if strand == "Science":
        allowed, science_why = science_allowed(statuses)
        print(f"  landable set from the ruled Science limb over "
              f"{BINDINGS.relative_to(ROOT)}: {len(allowed)} of {len(statuses)} deck(s)")
    else:
        allowed, science_why = landable(base), {}
        print(f"  landable set from {CENSUS.relative_to(ROOT)}: {len(allowed)} deck(s)")
    registry = pins()
    files, refused = {}, []
    for rel, status in sorted(statuses.items()):
        path = ROOT / rel
        if path.is_symlink() or not path.is_file():
            refused.append((rel, "not a regular file in the tree"))
            continue
        data = path.read_bytes()
        digest = hashlib.sha256(data).hexdigest()
        why = judge_member(rel, status, allowed, registry.get(rel), digest)
        if why and rel in science_why:
            why = science_why[rel]  # the ruled limb's own words, not the generic refusal
        if why:
            refused.append((rel, why))
            continue
        files[rel] = {"beforeGitBlob": blob_at(mb, rel),
                      "afterSha256": digest,
                      "bytes": len(data)}

    for rel, why in refused:
        print(f"  REFUSED {rel}: {why}")
    if refused:
        raise Refuse(f"{len(refused)} deck(s) refused; nothing declared")
    if not files:
        raise Refuse("no member to declare")
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
            f"# ORDER HUM-T · {name}: this batch's transplanted decks, each stage carrying the\n"
            f"# science exemplar's loop panel. One transaction, derived and written by\n"
            f"# tools/hum/admit_transaction.py. Every member also carries a CATALOGUE_PINS\n"
            f"# admission, which replacement_errors cross-checks.\n"
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


def self_test() -> int:
    bad = 0

    def check(name, cond):
        nonlocal bad
        print(f'  [{"ok" if cond else "FAIL"}] {name}')
        bad += 0 if cond else 1

    allowed = {"Humanities_Teesside/a.html"}
    d = "a" * 64
    check("a landable, pinned modification is declared",
          judge_member("Humanities_Teesside/a.html", "M", allowed, d, d) is None)
    check("a deck outside the landable set is refused",
          "outside the landable set" in
          judge_member("Humanities_Teesside/z.html", "M", allowed, d, d))
    check("an addition is refused, the transaction replaces and never adds",
          "not a modification" in
          judge_member("Humanities_Teesside/a.html", "A", allowed, d, d))
    check("a deletion is refused",
          "not a modification" in
          judge_member("Humanities_Teesside/a.html", "D", allowed, d, d))
    check("an unpinned deck is refused",
          "no CATALOGUE_PINS admission" in
          judge_member("Humanities_Teesside/a.html", "M", allowed, None, d))
    check("a pin disagreeing with the bytes is refused",
          "disagrees with the bytes" in
          judge_member("Humanities_Teesside/a.html", "M", allowed, "b" * 64, d))
    check("the slug is stable and file-safe", slug("HUM-T batch 1 (BUILD)") == "HUM_T_BATCH_1_BUILD")

    # --- the ruled Science limb, with the three red proofs the ruling names
    rel = "Science_Teesside/Grow/W18-W26_2026-27/SCI_G_W18A_The_Cold_Case.html"
    entry = {"weeks": [{"key": "Spr1\u00b7W3", "term": "Spr1", "weekWithinTerm": 3,
                        "label": "Spring 1 \u00b7 Week 3"}]}
    token_text = "... the cold case Spr1\u00b7W3 lesson ..."
    label_text = "... the cold case Spring 1 \u00b7 Week 3 lesson ..."
    check("Science: a bound deck that projects its week by TOKEN is landable",
          judge_science(rel, entry, True, token_text) is None)
    check("Science: the same deck projecting by LABEL is landable",
          judge_science(rel, entry, True, label_text) is None)
    check("RED PROOF (row absent): a deck the signed record does not bind is refused",
          "does not bind it" in judge_science(rel, None, True, token_text))
    check("RED PROOF (pin mismatch): a record whose digest is not its pin refuses every deck",
          "does not equal its pin" in judge_science(rel, entry, False, token_text))
    check("RED PROOF (week mismatch): a deck projecting a different week is refused",
          "does not cover the record's term-week" in
          judge_science(rel, entry, True, "... the cold case Spr1\u00b7W4 lesson ..."))
    # STOP-B3 forms (iii) and (iv), with the refusals the ruling names.
    spine = {"'GROW Weekly - Spring'!C28": {"reference": "'GROW Weekly - Spring'!C28",
                                            "termWeek": "Spr1\u00b7W3"},
             "'GROW Weekly - Spring'!C40": {"reference": "'GROW Weekly - Spring'!C40",
                                            "termWeek": "Spr1\u00b7W5"}}
    cell_deck = b'<script id="lesson-config">{"source":{"sheet":"GROW Weekly - Spring","cell":"C28"}}</script>'
    other_cell = b'<script id="lesson-config">{"source":{"sheet":"GROW Weekly - Spring","cell":"C40"}}</script>'
    check("Science (iii): a deck whose own lesson-config cell the spine maps to its row's "
          "term-week is landable",
          judge_science(rel, entry, True, "nothing here", config_cells(cell_deck), spine) is None)
    check("RED PROOF (iii): the same chain pointing at a DIFFERENT week is refused",
          "does not cover the record's term-week" in
          judge_science(rel, entry, True, "nothing here", config_cells(other_cell), spine))
    check("Science (iv): a deck that states NOTHING about its own week is proved by the signed row",
          judge_science(rel, entry, True, "nothing here") is None)
    check("RED PROOF (iv): form (iv) does not swallow a deck that states a DIFFERENT week",
          "does not cover the record's term-week" in
          judge_science(rel, entry, True, "... the cold case Spr1\u00b7W5 lesson ..."))
    check("RED PROOF (spine pin): a calendar spine whose digest is not its pin refuses every deck",
          "the calendar spine's digest does not equal its pin" in
          judge_science(rel, entry, True, token_text, frozenset(), spine, False))
    check("Science: the cell reader ignores a lesson-config that names no cell",
          config_cells(b'<script id="lesson-config">{"week":15}</script>') == set())
    check("Science: a row the record binds to no week is refused, not silently landable",
          "no term-week to project" in judge_science(rel, {"weeks": []}, True, token_text))
    check("Science: a two-week row is not covered by a deck that states only one of them",
          judge_science(rel, {"weeks": [entry["weeks"][0],
                                        {"key": "Spr1\u00b7W4", "term": "Spr1", "weekWithinTerm": 4,
                                         "label": "Spring 1 \u00b7 Week 4"}]}, True, token_text) is not None)
    check("the Humanities strand still maps to its own prefix, untouched",
          STRANDS["Humanities"] == PREFIX and STRANDS["Science"] == SCIENCE_PREFIX)
    print("self-test " + ("PASS" if not bad else f"FAIL ({bad})"))
    return 1 if bad else 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--name", help="transaction name, e.g. 'HUM-T batch 1 BUILD'")
    parser.add_argument("--base", default="origin/main")
    parser.add_argument("--strand", default="Humanities", choices=sorted(STRANDS))
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        return self_test()
    if not args.name:
        parser.error("--name is required unless --self-test")
    try:
        base_sha, files = derive(args.base, args.strand)
        for rel, entry in sorted(files.items()):
            print(f"     {entry['beforeGitBlob'][:12]} -> {entry['afterSha256'][:12]}  "
                  f"{entry['bytes']:>9,}  {rel.rsplit('/', 1)[1]}")
        changed = write(args.name, base_sha, files, args.check)
    except (Refuse, subprocess.CalledProcessError) as exc:
        print(f"[FAIL] {exc}")
        return 1
    return 1 if (args.check and changed) else 0


if __name__ == "__main__":
    raise SystemExit(main())
