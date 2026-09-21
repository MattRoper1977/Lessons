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
TERM_LABEL = {"Aut1": "Autumn 1", "Aut2": "Autumn 2", "Spr1": "Spring 1",
              "Spr2": "Spring 2", "Sum1": "Summer 1", "Sum2": "Summer 2"}
STRANDS = {"Humanities": PREFIX, "Science": SCIENCE_PREFIX}


def flat_text(data: bytes) -> str:
    """The deck's visible text, tags stripped and whitespace flattened -- the same shape
    tools/sci/reprove_bindings.py reads a projection out of."""
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", data.decode("utf-8", "replace")))


def projects(entry: dict, text: str) -> bool:
    """Pure. Does this deck's own text project every week the record binds it to?"""
    weeks = entry.get("weeks") or []
    if not weeks:
        return False
    if all(w["key"] in text for w in weeks):
        return True
    return all("%s \u00b7 Week %d" % (TERM_LABEL.get(w["term"], w["term"]), w["weekWithinTerm"]) in text
               for w in weeks)


# ORDER HUM-D5 ADDENDUM 3 v3, STOP-R option (a), ruled by Matt Roper 2026-09-22. The fifty
# served Summer 1 pages that arrived as fragments were given the estate's HTML shell, and a
# landed page is an 'M': the Summer 1 GLV3 route admits additions only, by design and by red
# proof. The ruled route through is ONE REVIEWED ACT rather than a standing widening -- a
# declared replacement transaction whose members are exactly those fifty, admitted by this limb:
#
#   SHELL-WRAP DERIVATION -- BODY BYTES IDENTICAL, WRAPPER ONLY.
#
# A member qualifies only when all of it holds: the path is under a Summer 1 pathway tree; it is
# not a lesson file; the bytes at the merge base had NO shell; the bytes on disk DO; what is
# inside <body> hashes equal to the whole of the base bytes; and the disk bytes are exactly what
# tools/hum/wrap_page_shell.py produces from the base bytes -- the tool's own idempotence, run
# per member. Anything else is refused by name.
SUMMER1_TREES = ("Humanities_Teesside/BUILD_W27-W39_2026-27/",
                 "Humanities_Teesside/GROW_W27-W39_2026-27/",
                 "Humanities_Teesside/LAUNCH_W27-W39_2026-27/")


def judge_shell_wrap(rel: str, before: bytes, after: bytes):
    """Pure. None when this member is a shell wrap of its own base bytes, else the reason."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("wrap_page_shell", ROOT / "tools/hum/wrap_page_shell.py")
    wrapper = importlib.util.module_from_spec(spec); spec.loader.exec_module(wrapper)
    if not rel.startswith(SUMMER1_TREES):
        return "not a Summer 1 pathway page; this transaction wraps nothing else"
    if rel.endswith("_Lesson.html"):
        return "a signed lesson file is never a member of the shell-wrap transaction"
    b = before.decode("utf-8", "replace")
    a = after.decode("utf-8", "replace")
    if wrapper.has_shell(b):
        return "the base bytes already had a shell, so this change is not a wrap"
    if not wrapper.has_shell(a):
        return "the bytes on disk still have no shell"
    if hashlib.sha256(wrapper.body_of(a).strip().encode()).hexdigest() != \
            hashlib.sha256(b.strip().encode()).hexdigest():
        return "the body bytes moved: a wrap changes nothing inside <body>"
    if a != wrapper.wrap(b, Path(rel)):
        return "the bytes on disk are not what the reviewed wrapper produces from the base bytes"
    return None


# --- THE PACK RECORD CLAUSE -----------------------------------------------------------------
# A wrap that the pack's own record does not carry is a wrap the pack cannot verify: the served
# SHA256SUMS would still claim the pre-wrap digests, and the arrival gate reads the record, not
# the diff. So the three packs' SHA256SUMS.txt and CHANGELOG.txt ride in the SAME ONE declared
# transaction as the pages they record -- the shape every landed Science transaction already
# uses (GROW W3 Friction, Diffusion W4L1, Sugar R10 hygiene and BUILD W8A chassis each carry
# their pack's SHA256SUMS.txt beside the bytes it records).
#
# A record is DERIVED from the page members, never accepted on its word:
#   SHA256SUMS.txt  the row PATHS are unchanged, one for one, in order -- a re-cut moves digests
#                   and never rows; the rows whose digest moved are EXACTLY this pack's wrapped
#                   members plus its own CHANGELOG.txt; and every moved digest equals the sha256
#                   of the bytes now on disk.
#   CHANGELOG.txt   the base bytes are a strict prefix of the bytes on disk -- a derivation entry
#                   is appended and never edits what was signed; the appended entry names the
#                   wrapper tool's own digest; and its table names EXACTLY this pack's wrapped
#                   members, each row's before/after digests and its after size agreeing with the
#                   bytes at the merge base and the bytes on disk.
SUMMER1_RECORDS = ("SHA256SUMS.txt", "CHANGELOG.txt")
_TABLE_ROW = re.compile(
    r"^\s+(\S+\.html)\s+([0-9a-f]{12}) -> ([0-9a-f]{12})\s+([\d,]+) -> \s*([\d,]+)\s*$")


def sums_rows(text: str) -> list:
    """[(path, digest)] in file order. A row this cannot read is kept, so it cannot be lost."""
    rows = []
    for line in text.splitlines():
        if not line.strip():
            continue
        digest, sep, rel = line.partition("  ")
        rows.append((rel.strip() if sep else line, digest.strip() if sep else ""))
    return rows


def wrapper_digest() -> str:
    return hashlib.sha256((ROOT / "tools/hum/wrap_page_shell.py").read_bytes()).hexdigest()


def judge_shell_wrap_record(rel: str, before: bytes, after: bytes, members: dict, disk: dict):
    """Pure. None when this pack record is derived from its own wrapped members, else why not.

    members: {pack-relative path: {'before': bytes, 'after': bytes}} for THIS pack's wrapped
    pages. disk: {pack-relative path: bytes} for the record files of this pack on disk.
    """
    tree = next((t for t in SUMMER1_TREES if rel.startswith(t)), None)
    if tree is None:
        return "not a Summer 1 pathway record; this transaction re-cuts nothing else"
    name = rel[len(tree):]
    if name not in SUMMER1_RECORDS:
        return "only a pack's own SHA256SUMS.txt or CHANGELOG.txt is a record member"
    if not members:
        return "no page of this pack was wrapped, so its record has nothing to re-cut"
    b = before.decode("utf-8", "replace")
    a = after.decode("utf-8", "replace")

    if name == "CHANGELOG.txt":
        if not a.startswith(b):
            return "the CHANGELOG was edited, not appended to: a derivation entry only adds"
        added = a[len(b):]
        if not added.strip():
            return "the CHANGELOG gained no derivation entry"
        if wrapper_digest()[:16] not in added:
            return "the derivation entry does not carry the wrapper tool's own digest"
        table = {}
        for line in added.splitlines():
            hit = _TABLE_ROW.match(line)
            if hit:
                table[hit.group(1)] = (hit.group(2), hit.group(3), hit.group(5).replace(",", ""))
        if set(table) != set(members):
            extra = sorted(set(table) - set(members))
            missing = sorted(set(members) - set(table))
            if extra:
                return "the derivation table names a page that was not wrapped: " + extra[0]
            return "the derivation table does not name every wrapped page; missing " + missing[0]
        for page, (was, now, size) in sorted(table.items()):
            real_before = hashlib.sha256(members[page]["before"]).hexdigest()
            real_after = hashlib.sha256(members[page]["after"]).hexdigest()
            if was != real_before[:12]:
                return f"the table's before-digest for {page} is not the digest at the base"
            if now != real_after[:12]:
                return f"the table's after-digest for {page} is not the digest on disk"
            if int(size) != len(members[page]["after"]):
                return f"the table's size for {page} is not the size on disk"
        return None

    was_rows, now_rows = sums_rows(b), sums_rows(a)
    if [r for r, _ in was_rows] != [r for r, _ in now_rows]:
        return "the SHA256SUMS row set moved: a re-cut changes digests, never rows"
    now_by_path = dict(now_rows)
    moved = {r for (r, d0), (_, d1) in zip(was_rows, now_rows) if d0 != d1}
    expected = set(members) | {"CHANGELOG.txt"}
    if moved != expected:
        extra = sorted(moved - expected)
        missing = sorted(expected - moved)
        if extra:
            return "a SHA256SUMS row moved for a file this transaction did not wrap: " + extra[0]
        return "a wrapped file's SHA256SUMS row did not move: " + missing[0]
    for page in sorted(moved):
        bytes_now = members[page]["after"] if page in members else disk.get(page)
        if bytes_now is None:
            return f"the re-cut row for {page} has no bytes on disk to derive from"
        if now_by_path.get(page) != hashlib.sha256(bytes_now).hexdigest():
            return f"the re-cut row for {page} is not the digest of the bytes on disk"
    return None


def shell_wrap_allowed(statuses, blob_reader) -> tuple[set, dict]:
    """The ruled limb applied to the paths this branch changed: pages first, then their records."""
    ok, why = set(), {}
    seen = {}
    for rel, status in sorted(statuses.items()):
        path = ROOT / rel
        if status != "M" or not path.is_file():
            why[rel] = "the shell-wrap transaction replaces landed pages; this is not an 'M'"
            continue
        before, after = blob_reader(rel), path.read_bytes()
        seen[rel] = (before, after)
        if rel.endswith(SUMMER1_RECORDS):
            continue  # judged below, once this pack's wrapped pages are known
        reason = judge_shell_wrap(rel, before, after)
        if reason:
            why[rel] = reason
        else:
            ok.add(rel)

    for rel, (before, after) in sorted(seen.items()):
        if not rel.endswith(SUMMER1_RECORDS):
            continue
        tree = next((t for t in SUMMER1_TREES if rel.startswith(t)), "")
        members = {r[len(tree):]: {"before": seen[r][0], "after": seen[r][1]}
                   for r in ok if tree and r.startswith(tree)}
        disk = {}
        for record in SUMMER1_RECORDS:
            p = ROOT / (tree + record) if tree else None
            if p is not None and p.is_file():
                disk[record] = p.read_bytes()
        reason = judge_shell_wrap_record(rel, before, after, members, disk)
        if reason:
            why[rel] = reason
        else:
            ok.add(rel)
    return ok, why


def judge_science(rel, entry, record_ok, text):
    """Pure. None when the ruled Science limb makes this deck landable, else the reason."""
    if not record_ok:
        return "the SCIENCE_WEEK_BINDINGS record's digest does not equal its pin"
    if entry is None:
        return "no SCIENCE_WEEK_BINDINGS row; the signed record does not bind it"
    if not (entry.get("weeks") or []):
        return "the record binds it to no week, so there is no term-week to project"
    if not projects(entry, text):
        weeks = ", ".join(w["key"] for w in entry["weeks"])
        return f"the record's term-week ({weeks}) is not projected by the deck's own text"
    return None


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
    raw = BINDINGS.read_bytes()
    record_ok = pins().get(BINDINGS_PIN_KEY) == hashlib.sha256(raw).hexdigest()
    entries = json.loads(raw)["entries"]
    ok, why = set(), {}
    for rel in paths:
        path = ROOT / rel
        text = flat_text(path.read_bytes()) if path.is_file() and not path.is_symlink() else ""
        reason = judge_science(rel, entries.get(rel), record_ok, text)
        if reason:
            why[rel] = reason
        else:
            ok.add(rel)
    return ok, why


def derive(base: str, strand: str = "Humanities", limb: str = "") -> tuple[str, dict]:
    prefix = STRANDS[strand]
    mb = merge_base(base)
    # The shell-wrap limb also reads each pack's own two records, because a wrap the record does
    # not carry is a wrap the pack cannot verify. Every other limb sees .html and nothing else.
    kinds = (".html",) + (SUMMER1_RECORDS if limb == "shell-wrap" else ())
    statuses = {}
    for line in git("diff", "--name-status", f"{mb}..HEAD", "--", prefix).splitlines():
        parts = line.split("\t")
        if len(parts) >= 2 and parts[-1].endswith(kinds):
            statuses[parts[-1]] = parts[0][0]

    print(f"SEARCH SCOPE: {len(statuses)} {strand} {' / '.join(kinds)} path(s) differing from "
          f"the merge base {mb[:12]} with {base}; blobs read from that merge base, digests from "
          f"the bytes on disk, pins from CATALOGUE_PINS in {GATE.relative_to(ROOT)}")

    if limb == "shell-wrap":
        allowed, science_why = shell_wrap_allowed(
            statuses, lambda rel: subprocess.run(["git", "show", f"{mb}:{rel}"], cwd=ROOT,
                                                 capture_output=True).stdout)
        pages = len([r for r in allowed if not r.endswith(SUMMER1_RECORDS)])
        print(f"  landable set from the ruled shell-wrap limb (body bytes identical, wrapper "
              f"only): {pages} page(s) and {len(allowed) - pages} derived pack record(s), "
              f"{len(allowed)} of {len(statuses)} path(s)")
    elif strand == "Science":
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
          "is not projected by the deck" in
          judge_science(rel, entry, True, "... the cold case Spr1\u00b7W4 lesson ..."))
    check("Science: a deck projecting NO week at all is refused",
          "is not projected by the deck" in judge_science(rel, entry, True, "nothing here"))
    check("Science: a row the record binds to no week is refused, not silently landable",
          "no term-week to project" in judge_science(rel, {"weeks": []}, True, token_text))
    check("Science: a two-week row needs BOTH weeks projected",
          judge_science(rel, {"weeks": [entry["weeks"][0],
                                        {"key": "Spr1\u00b7W4", "term": "Spr1", "weekWithinTerm": 4,
                                         "label": "Spring 1 \u00b7 Week 4"}]}, True, token_text) is not None)
    # STOP-R option (a): the shell-wrap limb, with the refusals the ruling names.
    import importlib.util as _il
    _spec = _il.spec_from_file_location("wrap_page_shell", ROOT / "tools/hum/wrap_page_shell.py")
    _w = _il.module_from_spec(_spec); _spec.loader.exec_module(_w)
    page = "Humanities_Teesside/GROW_W27-W39_2026-27/GROW/Summer_1/W03/GROW_SU1_W03_Knowledge_Organiser.html"
    frag = b"<h2>Words to use</h2>\n<table><tr><td>river</td></tr></table>\n"
    wrapped = _w.wrap(frag.decode(), Path(page)).encode()
    check("shell-wrap: a page wrapped by the reviewed wrapper is a member",
          judge_shell_wrap(page, frag, wrapped) is None)
    check("RED PROOF (outside the fifty): a page outside the Summer 1 trees is refused",
          "not a Summer 1 pathway page" in
          judge_shell_wrap("Humanities_Teesside/GROW_W1-W8_2026-27/x.html", frag, wrapped))
    lesson = "Humanities_Teesside/GROW_W27-W39_2026-27/GROW/Summer_1/W03/GROW_SU1_W03_Lesson.html"
    check("RED PROOF (a lesson file): a signed lesson is never a member, even wrapped",
          "signed lesson file" in
          judge_shell_wrap(lesson, frag, _w.wrap(frag.decode(), Path(lesson)).encode()))
    moved = wrapped.replace(b"river", b"estuary")
    check("RED PROOF (inner bytes moved): a wrap that edits anything inside <body> is refused",
          "the body bytes moved" in judge_shell_wrap(page, frag, moved))
    shelled = b"<!DOCTYPE html><html><head></head><body><p>x</p></body></html>"
    check("RED PROOF (already whole): a page that had a shell at the base is refused",
          "already had a shell" in judge_shell_wrap(page, shelled, shelled))
    hand = b"<html><head><title>By hand</title></head><body>" + frag + b"</body></html>"
    check("RED PROOF (not the reviewed wrapper): a hand-made shell is refused",
          "not what the reviewed wrapper produces" in judge_shell_wrap(page, frag, hand))
    # The pack record clause. Every record is derived from its own wrapped members, so each way
    # a record could lie is proved to go RED rather than assumed to.
    tree = "Humanities_Teesside/GROW_W27-W39_2026-27/"
    members = {"GROW/Summer_1/W03/GROW_SU1_W03_Knowledge_Organiser.html":
               {"before": frag, "after": wrapped}}
    d_before = hashlib.sha256(frag).hexdigest()
    d_after = hashlib.sha256(wrapped).hexdigest()
    log_before = b"PACK CHANGELOG\nv3 as signed.\n"
    entry = ("\n\nHTML shell added to 1 served page\n"
             "tools/hum/wrap_page_shell.py (sha256 %s)\n\n"
             "    GROW/Summer_1/W03/GROW_SU1_W03_Knowledge_Organiser.html  %s -> %s  %d -> %d\n"
             % (wrapper_digest()[:16], d_before[:12], d_after[:12], len(frag), len(wrapped)))
    log_after = log_before + entry.encode()
    d_log = hashlib.sha256(log_after).hexdigest()
    disk = {"CHANGELOG.txt": log_after}
    check("shell-wrap record: a CHANGELOG appended with the derived entry is a member",
          judge_shell_wrap_record(tree + "CHANGELOG.txt", log_before, log_after,
                                  members, disk) is None)
    check("RED PROOF (CHANGELOG edited): a record whose signed text moved is refused",
          "edited, not appended to" in
          judge_shell_wrap_record(tree + "CHANGELOG.txt", log_before,
                                  log_after.replace(b"v3 as signed", b"v4 as signed"),
                                  members, disk))
    check("RED PROOF (a page the entry does not name): a missing table row is refused",
          "does not name every wrapped page" in
          judge_shell_wrap_record(tree + "CHANGELOG.txt", log_before,
                                  log_before + b"\n\nsha256 " + wrapper_digest()[:16].encode()
                                  + b"\n", members, disk))
    check("RED PROOF (a digest the bytes do not carry): a table row that lies is refused",
          "after-digest" in
          judge_shell_wrap_record(tree + "CHANGELOG.txt", log_before,
                                  log_after.replace(d_after[:12].encode(), b"0" * 12),
                                  members, disk))
    check("RED PROOF (no wrapper digest): an entry that does not name the tool is refused",
          "wrapper tool's own digest" in
          judge_shell_wrap_record(tree + "CHANGELOG.txt", log_before,
                                  log_after.replace(wrapper_digest()[:16].encode(), b"0" * 16),
                                  members, disk))
    sums_before = ("%s  GROW/Summer_1/W03/GROW_SU1_W03_Knowledge_Organiser.html\n"
                   "%s  CHANGELOG.txt\n"
                   "%s  GROW/Summer_1/W03/GROW_SU1_W03_Lesson.html\n"
                   % (d_before, hashlib.sha256(log_before).hexdigest(), "b" * 64)).encode()
    sums_after = ("%s  GROW/Summer_1/W03/GROW_SU1_W03_Knowledge_Organiser.html\n"
                  "%s  CHANGELOG.txt\n"
                  "%s  GROW/Summer_1/W03/GROW_SU1_W03_Lesson.html\n"
                  % (d_after, d_log, "b" * 64)).encode()
    check("shell-wrap record: a SHA256SUMS re-cut for exactly the wrapped rows is a member",
          judge_shell_wrap_record(tree + "SHA256SUMS.txt", sums_before, sums_after,
                                  members, disk) is None)
    check("RED PROOF (a row appeared): a re-cut that adds a row is refused",
          "row set moved" in
          judge_shell_wrap_record(tree + "SHA256SUMS.txt", sums_before,
                                  sums_after + b"c" * 64 + b"  extra.html\n", members, disk))
    check("RED PROOF (a row vanished): a re-cut that drops a row is refused",
          "row set moved" in
          judge_shell_wrap_record(tree + "SHA256SUMS.txt", sums_before,
                                  b"\n".join(sums_after.split(b"\n")[:2]) + b"\n",
                                  members, disk))
    check("RED PROOF (an unwrapped file's row moved): a signed lesson's digest is refused",
          "did not wrap" in
          judge_shell_wrap_record(tree + "SHA256SUMS.txt", sums_before,
                                  sums_after.replace(b"b" * 64, b"c" * 64), members, disk))
    check("RED PROOF (a wrapped file's row stood still): a stale digest is refused",
          "did not move" in
          judge_shell_wrap_record(tree + "SHA256SUMS.txt", sums_before,
                                  sums_after.replace(d_after.encode(), d_before.encode()),
                                  members, disk))
    check("RED PROOF (a re-cut digest that is not the bytes): a typed digest is refused",
          "not the digest of the bytes on disk" in
          judge_shell_wrap_record(tree + "SHA256SUMS.txt", sums_before,
                                  sums_after.replace(d_log.encode(), b"a" * 64), members, disk))
    check("RED PROOF (a record outside the trees): another pack's record is refused",
          "not a Summer 1 pathway record" in
          judge_shell_wrap_record("Humanities_Teesside/GROW_W1-W8_2026-27/SHA256SUMS.txt",
                                  sums_before, sums_after, members, disk))
    check("RED PROOF (another file in the pack root): only the two records are members",
          "only a pack's own" in
          judge_shell_wrap_record(tree + "README.md", log_before, log_after, members, disk))
    check("RED PROOF (a pack with no wrapped page): its record has nothing to re-cut",
          "nothing to re-cut" in
          judge_shell_wrap_record(tree + "CHANGELOG.txt", log_before, log_after, {}, disk))
    check("the Humanities strand still maps to its own prefix, untouched",
          STRANDS["Humanities"] == PREFIX and STRANDS["Science"] == SCIENCE_PREFIX)
    print("self-test " + ("PASS" if not bad else f"FAIL ({bad})"))
    return 1 if bad else 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--name", help="transaction name, e.g. 'HUM-T batch 1 BUILD'")
    parser.add_argument("--base", default="origin/main")
    parser.add_argument("--strand", default="Humanities", choices=sorted(STRANDS))
    parser.add_argument("--limb", default="", choices=["", "shell-wrap"],
                        help="the ruled shell-wrap limb instead of the strand's landable census")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        return self_test()
    if not args.name:
        parser.error("--name is required unless --self-test")
    try:
        base_sha, files = derive(args.base, args.strand, args.limb)
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
