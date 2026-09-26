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
import os
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


def title_stage_text(data: bytes) -> str:
    """What a Science deck CLAIMS about its own week: the visible text of its TITLE STAGE, the first
    top-level slide (its meta line included), read through deck_dom -- the estate's one stage
    reader -- with scripts and styles skipped. Ruled 2026-09-23 (Matt, on the limbs review): a
    recall or review line on a later stage quotes another lesson's week and is not the deck's
    claim; reading the whole deck is what refused SCI_B_W4A-W7A. build_lesson_order's
    deck_statement_text reads the same stage for the same reason."""
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import deck_dom
    stages = deck_dom.stages(deck_dom.parse(data.decode("utf-8", "replace")))
    return stages[0].inner_text() if stages else ""


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
    if not want <= got:
        return ("the deck states %s about itself, which does not cover the record's term-week (%s)"
                % (", ".join(sorted(got)), ", ".join(sorted(want))))
    # Ruled 2026-09-23 (Matt, on SCI_G_W16B): a week the TITLE STAGE claims that the row does not
    # bind is a refusal, whatever another form covers. Cover alone let W16B land: its label
    # "Spring 1 · Week 16" is read as Spr1·W16, and its own lesson-config cell C29 (Spr1·W2) covered
    # the row, so the wrong week a pupil reads on the title stage went unrefused.
    stray = projected(text, set(), spine or {}) - want
    if stray:
        return ("the deck's title stage states %s, which its row (%s) does not bind"
                % (", ".join(sorted(stray)), ", ".join(sorted(want))))
    return None  # forms (i)-(iii): every bound week is one the deck states about itself


class Refuse(Exception):
    """A condition that makes declaring unsafe. Never repaired."""


def git(*args: str, root=None) -> str:
    return subprocess.run(["git", *args], cwd=root or ROOT, capture_output=True, text=True,
                          check=True).stdout


def merge_base(base: str, root=None) -> str:
    return git("merge-base", base, "HEAD", root=root).strip()


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


def blob_at(ref: str, rel: str, root=None) -> str:
    out = git("ls-tree", ref, "--", rel, root=root).split()
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


# --- THE EXPLICIT-TAGS LIMB (Matt Roper, 2026-09-22, ruling on STOP-R2, option (a)) ---------
# "explicit document tags -- DOM identical, wrapper only".
#
# The fifty Summer 1 pages were never fragments: each opens <!doctype html><html ...> and closes
# </html>, leaving <head> and <body> implied as HTML5 allows. The corrective writes those tags
# down and moves no content. A member qualifies only when all of it holds: the path is under a
# Summer 1 pathway tree; the bytes at the merge base are what tools/hum/explicit_document_tags.py
# would mark up; the bytes on disk are exactly what it produces; and its own checker -- which
# undoes the recorded insertions and demands the original back -- passes. Anything else is
# refused by name. The packs' own SHA256SUMS.txt and CHANGELOG.txt ride in the same one declared
# transaction, derived from the page members, as every landed Science transaction already does.
SUMMER1_TREES = ("Humanities_Teesside/BUILD_W27-W39_2026-27/",
                 "Humanities_Teesside/GROW_W27-W39_2026-27/",
                 "Humanities_Teesside/LAUNCH_W27-W39_2026-27/")
SUMMER1_RECORDS = ("SHA256SUMS.txt", "CHANGELOG.txt")
_TABLE_ROW = re.compile(
    r"^\s+(\S+\.html)\s+([0-9a-f]{12}) -> ([0-9a-f]{12})\s+([\d,]+) -> \s*([\d,]+)\s*$")


def _tagger():
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "explicit_document_tags", ROOT / "tools/hum/explicit_document_tags.py")
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m


def tool_digest() -> str:
    return hashlib.sha256((ROOT / "tools/hum/explicit_document_tags.py").read_bytes()).hexdigest()


# --- THE RESPONSIVE LIMB (PACK-1R v4 re-delivery, ruling 2026-09-23 §4) --------------------
# "responsive re-delivery -- GPT PACK-1R v4 pages, lesson bytes untouched".
#
# Same shape as the explicit-tags limb and for the same reason: the change is an ADDITIVE,
# REVERSIBLE wrapper that moves no content. tools/hum/responsive_pages.py writes down a
# viewport meta (only where the page declares none) and one reviewed <style> block, both
# immediately before the page's own </head>. A member qualifies only when the bytes on disk
# are EXACTLY what that reviewed tool produces from the bytes at the merge base, and when the
# tool's own checker -- which undoes the recorded insertions, demands the original bytes back,
# and compares the two PARSED documents' text content -- passes.
#
# The delivery arrived from outside this estate. That is precisely why it is judged and not
# trusted: repair() over main's own bytes reproduces all twenty-one delivered pages byte for
# byte, so "GPT sent it" is nowhere in the predicate.


def _responsive():
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "responsive_pages", ROOT / "tools/hum/responsive_pages.py")
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m


def responsive_tool_digest() -> str:
    return hashlib.sha256((ROOT / "tools/hum/responsive_pages.py").read_bytes()).hexdigest()


def judge_responsive(rel: str, before: bytes, after: bytes):
    """Pure. None when this member is its own base bytes with the responsive furniture added."""
    R = _responsive()
    if not rel.startswith(SUMMER1_TREES):
        return "not a Summer 1 pathway page; this transaction re-delivers nothing else"
    b = before.decode("utf-8", "replace")
    a = after.decode("utf-8", "replace")
    try:
        want, inserts = R.repair(b)
    except R.Refuse as why:
        return "the reviewed tool refuses this page: %s" % why
    if not inserts:
        return "the base bytes already carry the responsive furniture, so there is nothing to add"
    if a != want:
        return "the bytes on disk are not what the reviewed tool produces from the base bytes"
    try:
        R.check(b, a, inserts)
    except R.Refuse as why:
        return "the tool's own checker refuses the result: %s" % why
    return None


def judge_explicit_tags(rel: str, before: bytes, after: bytes):
    """Pure. None when this member is its own base bytes with the implied tags written down."""
    T = _tagger()
    if not rel.startswith(SUMMER1_TREES):
        return "not a Summer 1 pathway page; this transaction marks up nothing else"
    b = before.decode("utf-8", "replace")
    a = after.decode("utf-8", "replace")
    try:
        want, inserts = T.repair(b)
    except T.Refuse as why:
        return "the reviewed tool refuses this page: %s" % why
    if not inserts:
        return "the base bytes already wrote head and body down, so there is nothing to mark up"
    if a != want:
        return "the bytes on disk are not what the reviewed tool produces from the base bytes"
    try:
        T.check(b, a, inserts)
    except T.Refuse as why:
        return "the tool's own checker refuses the result: %s" % why
    return None


def sums_rows(text: str) -> list:
    """[(path, digest)] in file order. A row this cannot read is kept, so it cannot be lost."""
    rows = []
    for line in text.splitlines():
        if not line.strip():
            continue
        digest, sep, rel = line.partition("  ")
        rows.append((rel.strip() if sep else line, digest.strip() if sep else ""))
    return rows


def judge_explicit_tags_record(rel: str, before: bytes, after: bytes, members: dict, disk: dict,
                               digest: str = ""):
    """Pure. None when this pack record is derived from its own re-cut members, else why not.

    `digest` is the digest of the tool that derived the members -- the tagger's by default,
    the responsive writer's when the responsive limb calls it. A CHANGELOG entry must carry
    it, so a record cannot claim a derivation the transaction did not perform."""
    digest = digest or tool_digest()
    tree = next((t for t in SUMMER1_TREES if rel.startswith(t)), None)
    if tree is None:
        return "not a Summer 1 pathway record; this transaction re-cuts nothing else"
    name = rel[len(tree):]
    if name not in SUMMER1_RECORDS:
        return "only a pack's own SHA256SUMS.txt or CHANGELOG.txt is a record member"
    if not members:
        return "no page of this pack was marked up, so its record has nothing to re-cut"
    b = before.decode("utf-8", "replace")
    a = after.decode("utf-8", "replace")

    if name == "CHANGELOG.txt":
        if not a.startswith(b):
            return "the CHANGELOG was edited, not appended to: a derivation entry only adds"
        added = a[len(b):]
        if not added.strip():
            return "the CHANGELOG gained no derivation entry"
        if digest[:16] not in added:
            return "the derivation entry does not carry the tool's own digest"
        table = {}
        for line in added.splitlines():
            hit = _TABLE_ROW.match(line)
            if hit:
                table[hit.group(1)] = (hit.group(2), hit.group(3), hit.group(5).replace(",", ""))
        if set(table) != set(members):
            extra = sorted(set(table) - set(members))
            missing = sorted(set(members) - set(table))
            if extra:
                return "the derivation table names a page that was not marked up: " + extra[0]
            return "the derivation table does not name every marked-up page; missing " + missing[0]
        for page, (was, now, size) in sorted(table.items()):
            if was != hashlib.sha256(members[page]["before"]).hexdigest()[:12]:
                return f"the table's before-digest for {page} is not the digest at the base"
            if now != hashlib.sha256(members[page]["after"]).hexdigest()[:12]:
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
            return "a SHA256SUMS row moved for a file this transaction did not touch: " + extra[0]
        return "a marked-up file's SHA256SUMS row did not move: " + missing[0]
    for page in sorted(moved):
        bytes_now = members[page]["after"] if page in members else disk.get(page)
        if bytes_now is None:
            return f"the re-cut row for {page} has no bytes on disk to derive from"
        if now_by_path.get(page) != hashlib.sha256(bytes_now).hexdigest():
            return f"the re-cut row for {page} is not the digest of the bytes on disk"
    return None


def explicit_tags_allowed(statuses, blob_reader) -> tuple[set, dict]:
    """The ruled limb applied to the paths this branch changed: pages first, then their records."""
    return _pack_limb_allowed(statuses, blob_reader, judge_explicit_tags, tool_digest())


def responsive_allowed(statuses, blob_reader) -> tuple[set, dict]:
    """The ruled responsive limb, same walk, its own page judge and its own tool digest."""
    return _pack_limb_allowed(statuses, blob_reader, judge_responsive, responsive_tool_digest())


def _pack_limb_allowed(statuses, blob_reader, judge_page, digest) -> tuple[set, dict]:
    """Shared by both pack limbs: pages first, then each pack's records from its own members."""
    ok, why, seen = set(), {}, {}
    for rel, status in sorted(statuses.items()):
        path = ROOT / rel
        if status != "M" or not path.is_file():
            why[rel] = "this transaction replaces landed pages; this is not an 'M'"
            continue
        before, after = blob_reader(rel), path.read_bytes()
        seen[rel] = (before, after)
        if rel.endswith(SUMMER1_RECORDS):
            continue                      # judged below, once this pack's pages are known
        reason = judge_page(rel, before, after)
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
        reason = judge_explicit_tags_record(rel, before, after, members, disk, digest)
        if reason:
            why[rel] = reason
        else:
            ok.add(rel)
    return ok, why


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
        text = title_stage_text(data) if data else ""
        reason = judge_science(rel, entries.get(rel), record_ok, text,
                               config_cells(data), spine, spine_ok)
        if reason:
            why[rel] = reason
        else:
            ok.add(rel)
    return ok, why


# --- THE SCIENCE PACK-RECORD LIMB (Matt Roper, 2026-09-22, ruling S3 on the S02 STOP) ---------
# "EXTEND admit_transaction's Science part to accept SHA256SUMS.txt as a transaction member
# (derived digest of the re-cut manifest, pinned), red-proved: a manifest not in the transaction
# -> refused; a manifest whose rows disagree with member bytes -> refused. No one-off declarer."
#
# A Science pack's SHA256SUMS.txt is declared in the SAME transaction as the decks it lists, and
# only as the derivation of their re-cut bytes. The Humanities record limb above is the model,
# with one ruled difference: a row that was ALREADY stale on main may be refreshed in the same
# re-cut (D-1, admit_w8a_chassis.py, "rows that were already stale on main move with the
# lesson's"), because the refresher cannot scope to one row. A row that moves for a file this
# transaction does not declare is refused if it was fresh at the base, or if that file's bytes
# moved since the base -- either way the file changed outside the transaction. And a re-cut must
# be derived FROM the transaction: at least one declared deck of the pack must have a row in it.
# A deck with no row (the five Classics) is not enrolled: "refresh the rows that exist, leave the
# rest" (ruling 2026-09-23 §2, correction #32). Like every member, the manifest must carry a
# CATALOGUE_PINS admission equal to its bytes (judge_member), so its derived digest is pinned.
SCIENCE_RECORD = "SHA256SUMS.txt"


def science_packs_of(rel: str) -> list:
    """Every folder whose SHA256SUMS.txt could list this deck, nearest first: its own folder,
    then each ancestor up to the Science root. The three Teaching_Packs manifests list their
    decks one folder down (HTML/BUILD_Science_W6A.html), so the deck's own folder is not the
    only place a row for it can live."""
    parts = rel.split("/")
    return ["/".join(parts[:i]) + "/" for i in range(len(parts) - 1, 0, -1)
            if ("/".join(parts[:i]) + "/").startswith(SCIENCE_PREFIX)]


def judge_science_record(rel: str, before: bytes, after: bytes, members: dict,
                         disk_digest, base_digest):
    """Pure. None when this Science manifest is the derived re-cut of this transaction's members.

    members      {row name in this pack: {"after": bytes}} -- the decks of THIS pack the Science
                 limb landed in this transaction
    disk_digest  row name -> sha256 of that file on disk now, or None
    base_digest  row name -> sha256 of that file at the merge base, or None"""
    if not rel.startswith(SCIENCE_PREFIX) or not rel.endswith("/" + SCIENCE_RECORD):
        return "only a Science pack's own SHA256SUMS.txt is a record member"
    if not members:
        return "a manifest re-cut for a pack this transaction does not touch: no deck of it is declared"
    was_rows = sums_rows(before.decode("utf-8", "replace"))
    now_rows = sums_rows(after.decode("utf-8", "replace"))
    if [r for r, _ in was_rows] != [r for r, _ in now_rows]:
        return "the SHA256SUMS row set moved: a re-cut changes digests, never rows"
    # BYTES, not only parsed rows (review of the S3 PR): every line that changed must be the same
    # row with only its digest replaced, so the manifest is exactly the refresher's in-place re-cut.
    b_lines, a_lines = before.splitlines(keepends=True), after.splitlines(keepends=True)
    if len(b_lines) != len(a_lines):
        return "the re-cut changes lines, not only row digests"
    for lb, la in zip(b_lines, a_lines):
        if lb == la:
            continue
        rb = sums_rows(lb.decode("utf-8", "replace"))
        ra = sums_rows(la.decode("utf-8", "replace"))
        if (len(rb) != 1 or len(ra) != 1 or rb[0][0] != ra[0][0] or not rb[0][1] or not ra[0][1]
                or la != lb.replace(rb[0][1].encode(), ra[0][1].encode())):
            return "a re-cut line is not the same row with only its digest replaced"
    now = dict(now_rows)
    if not any(page in now for page in members):
        return ("no declared deck of this pack has a row in it: the re-cut would not be derived "
                "from this transaction")
    for page in sorted(members):
        if page not in now:
            continue                      # no row: not enrolled (correction #32)
        if now[page] != hashlib.sha256(members[page]["after"]).hexdigest():
            return f"the manifest's row for {page} disagrees with the member's bytes"
    for (row, d0), (_, d1) in zip(was_rows, now_rows):
        if d0 == d1 or row in members:
            continue
        if d1 != disk_digest(row):
            return f"a re-cut row for {row} is not the digest of the bytes on disk"
        if d0 == base_digest(row):
            return f"a SHA256SUMS row moved for {row}, which was fresh at the base and is not declared"
        if d1 != base_digest(row):
            return f"a SHA256SUMS row moved for {row}, whose file changed outside this transaction"
    return None


def science_records_allowed(statuses: dict, blob_reader, landed: set, root=None) -> tuple[set, dict]:
    """The record limb over this branch's changed manifests, then the other half of the rule:
    a landed deck whose pack manifest lists it must have that manifest re-cut IN this
    transaction, or the deck is refused -- its row would be left disagreeing with its bytes.

    root: the tree read for bytes on disk (default ROOT) -- the seam the self-test uses to judge a
    real manifest through this wiring, not only through judge_science_record (review of the S3 PR).
    blob_reader reads the MERGE BASE; a manifest's before-bytes come from it, never from disk."""
    root = root or ROOT
    ok, why = set(), {}
    for rel, status in sorted(statuses.items()):
        if not rel.endswith("/" + SCIENCE_RECORD):
            continue
        if status != "M":
            why[rel] = "this transaction replaces landed records; this is not an 'M'"
            continue
        pack = rel[: -len(SCIENCE_RECORD)]
        gone = sorted(r for r in landed if r.startswith(pack) and not (root / r).is_file())
        if gone:
            why[rel] = f"a declared deck of this pack is not a regular file: {gone[0]}"
            continue
        members = {r[len(pack):]: {"after": (root / r).read_bytes()}
                   for r in landed if r.startswith(pack)}
        disk = lambda row, pack=pack: (hashlib.sha256((root / pack / row).read_bytes()).hexdigest()
                                       if (root / pack / row).is_file() else None)
        def base(row, pack=pack):
            data = blob_reader(pack + row)
            return hashlib.sha256(data).hexdigest() if data else None
        reason = judge_science_record(rel, blob_reader(rel), (root / rel).read_bytes(),
                                      members, disk, base)
        if reason:
            why[rel] = reason
        else:
            ok.add(rel)
    for deck in sorted(landed):
        for pack in science_packs_of(deck):
            manifest = root / pack / SCIENCE_RECORD
            # The manifest as it stands, or as it stood at the merge base if this branch renamed or
            # removed it: a deck its base manifest listed is not freed by moving the manifest away
            # (review of the S3 PR: a rename slipped past this limb).
            text = (manifest.read_bytes() if manifest.is_file() else blob_reader(pack + SCIENCE_RECORD) or b"")
            if not text:
                continue
            rows = dict(sums_rows(text.decode("utf-8", "replace")))
            if deck[len(pack):] not in rows:
                continue                  # no row: not enrolled (correction #32)
            if pack + SCIENCE_RECORD in why:
                why[deck] = (f"its pack manifest {pack + SCIENCE_RECORD} is re-cut in this transaction "
                             f"but refused: {why[pack + SCIENCE_RECORD]}")
                break
            if pack + SCIENCE_RECORD not in ok:
                why[deck] = (f"its pack manifest {pack + SCIENCE_RECORD} lists it but is not re-cut "
                             f"in this transaction: a manifest not in the transaction is refused")
                break
    return ok, why


def science_limb(statuses: dict, blob_reader, deck_limb=None, root=None) -> tuple[set, dict, set]:
    """derive()'s Science part: the ruled deck limb over the changed decks, the record limb over
    the changed manifests, then the record limb's refusals taken OUT of the landable set.

    Split out of derive() so the wiring is under the self-test and not only the judges: the
    review of the first cut found the refusal of a deck whose manifest is not re-cut lived in one
    line of derive() that no check reached. Returns (landable, reason per refused path, records).
    """
    decks = {r: s for r, s in statuses.items() if not r.endswith("/" + SCIENCE_RECORD)}
    allowed, why = (deck_limb or science_allowed)(decks)
    records, record_why = science_records_allowed(statuses, blob_reader, allowed, root)
    for rel, reason in record_why.items():
        allowed.discard(rel)
        why[rel] = reason
    return allowed | records, why, records


# --- THE DLG-1 LIMB (ruling LAND-A2 R8 §2, 26 September 2026) ---------------------------------
# "the bytes on disk equal fix_dialog_audience.py applied to the base bytes; manifests may re-cut
# digests only."
#
# DLG-1 (R5 §2) copies a dialog's own audience attributes onto the opening tag of the control that
# opens it, on exactly the pages and controls the Chromium probe measured. Same shape as the
# responsive limb (#647), and for the same reason: judged from the base bytes, never trusted.
#
#   PAGE    the fixer and the pairs record are the reviewed bytes, pinned below by digest, so a
#           changed fixer or a widened record refuses EVERY member rather than admitting one; the
#           page is named by tools/hum/DLG1_PAIRS.json (a page the record holds out by ruling --
#           SCI_B_W8B, R8 §1 -- is refused by name); and the bytes on disk are exactly what the
#           fixer's pure fix_text() produces from the bytes at the merge base under that page's
#           recorded pairs.
#   RECORD  a pack's SHA256SUMS.txt (or CHECKSUMS.sha256), or a JSON manifest named in
#           DLG1_JSON_MANIFESTS (the Fallback pack's MANIFEST.json, R8 §5), is a member only as a
#           digest re-cut: every line equal to the base except the digest of a row naming a page
#           member of THIS transaction, and each such digest the sha256 of that page's bytes on
#           disk. Row set, row order, every other digest -- a row already stale at the base
#           included -- and every other byte stay as they were.
#   BOTH    a page member that a manifest lists at the base must have that manifest re-cut in the
#           same transaction, or the page is refused: its row would disagree with its bytes.
#
# ONE TRANSACTION, BOTH STRANDS. The record spans Humanities and Science, so the limb reads both
# prefixes and declares one 'DLG-1' transaction. The Science pages are judged here, not by the
# Science landability limb: that limb proves a deck's own week claim against the signed bindings,
# which an attribute added to a <button> tag cannot move, and it bounds nothing about WHICH bytes
# changed; its record rule (S3) lets a row stale at the base ride along, which R8 §2 does not. One
# predicate, byte-exact, for all 192 members is the ruled rule with no second rule beside it.
#
# The GLV3 boundary does not take the declaration on trust either: it calls limb_verdicts() below on
# every member of a transaction it lists as limb-judged, binding this file to its CATALOGUE_PINS
# admission first. A DLG-1 claim on a path an earlier transaction declared counts only for a change
# this limb judges its own; any other change to that path stays with the earlier transaction.
DLG1_FIXER = "tools/hum/fix_dialog_audience.py"
DLG1_PAIRS = "tools/hum/DLG1_PAIRS.json"
DLG1_FIXER_SHA256 = "2670c6df1a40958c39cbf81e71de138c8a5fb1c5c02271fc13f12323842a6523"
DLG1_PAIRS_SHA256 = "3e4cbb64a3b5e1b39549cd3da57845202c4fd6575aa738c60effd3df0ff0744d"
DLG1_PREFIXES = (PREFIX, SCIENCE_PREFIX)
DLG1_SUMS = ("SHA256SUMS.txt", "CHECKSUMS.sha256")
# A JSON manifest is named, with the folder its keys are relative to; never matched by pattern.
DLG1_JSON_MANIFESTS = {
    "Humanities_Teesside/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/MANIFEST.json":
        "Humanities_Teesside/Teaching_Packs/",
}
_DLG1_ROW = {
    "sums": re.compile(r"^(?P<digest>[0-9a-f]{64})  (?P<name>[^\r\n]+?)\r?\n?$"),
    "json": re.compile(r'^\s*"(?P<key>(?:[^"\\]|\\.)*)"\s*:\s*"(?P<digest>[0-9a-f]{64})"\s*,?\s*\r?\n?$'),
}


def dlg1_tools(root=None):
    """(fixer module, {page: [(action, dialog)]}, {page: held-out row}), built from the bytes of
    the fixer and the pairs record only after each is proved to be the reviewed bytes. The module
    is compiled from the very bytes that were hashed, so nothing can change between the two."""
    import types
    root = root or ROOT
    data = {}
    for rel, pinned in ((DLG1_FIXER, DLG1_FIXER_SHA256), (DLG1_PAIRS, DLG1_PAIRS_SHA256)):
        path = root / rel
        if path.is_symlink() or not path.is_file():
            raise Refuse(f"{rel} is not a regular file")
        data[rel] = path.read_bytes()
        digest = hashlib.sha256(data[rel]).hexdigest()
        if digest != pinned:
            raise Refuse(f"{rel} is not the reviewed bytes (sha256 {digest[:12]}, pinned "
                         f"{pinned[:12]}): a changed fixer or pairs record cannot widen the limb")
    F = types.ModuleType("fix_dialog_audience")
    F.__file__ = str(root / DLG1_FIXER)
    exec(compile(data[DLG1_FIXER], F.__file__, "exec"), F.__dict__)
    try:
        record = json.loads(data[DLG1_PAIRS])
        return F, F.record_pairs(record), F.held_out(record)
    except (ValueError, KeyError, TypeError, F.Refuse) as why:
        raise Refuse(f"{DLG1_PAIRS} is not a pairs record: {why}")


def judge_dlg1(rel: str, before: bytes, after: bytes, tools):
    """Pure. None when this page is its own base bytes with its recorded controls given their
    dialogs' audience by the reviewed fixer, else why not."""
    F, pairs, held = tools
    if rel in held:
        return (f"held out of DLG-1 by ruling ({held[rel].get('ruling', '?')}; until "
                f"{held[rel].get('until', '?')}): the pairs record names no pair for it")
    if rel not in pairs:
        return ("not a page the DLG-1 pairs record names; the probe measured no hidden-dialog "
                "opener to fix here")
    try:
        base = before.decode("utf-8")
    except UnicodeDecodeError:
        return "the base bytes are not UTF-8, so the reviewed fixer cannot read them"
    try:
        want, edits = F.fix_text(base, pairs[rel])
    except F.Refuse as why:
        return "the reviewed fixer refuses this page: %s" % why
    if not edits:
        return "the base bytes already carry every recorded audience, so there is nothing to fix"
    if after != want.encode("utf-8"):
        return "the bytes on disk are not what the reviewed fixer produces from the base bytes"
    return None


def dlg1_manifest_kind(rel: str):
    """'json' for a named JSON manifest, 'sums' for a pack checksum file, None for anything else."""
    if rel in DLG1_JSON_MANIFESTS:
        return "json"
    if rel.startswith(DLG1_PREFIXES) and rel.rsplit("/", 1)[-1] in DLG1_SUMS:
        return "sums"
    return None


def _dlg1_row(line: str, kind: str):
    """(row name, digest, the line before the digest, the line after it), or None: not a row."""
    m = _DLG1_ROW[kind].match(line)
    if not m:
        return None
    try:
        name = m.group("name") if kind == "sums" else json.loads('"%s"' % m.group("key"))
    except ValueError:
        return None
    return name, m.group("digest"), line[:m.start("digest")], line[m.end("digest"):]


def dlg1_rows(text: str, kind: str) -> dict:
    """{row name: digest} for every row of a manifest."""
    rows = {}
    for line in text.splitlines(keepends=True):
        row = _dlg1_row(line, kind)
        if row:
            rows[row[0]] = row[1]
    return rows


def dlg1_listing(page: str, read) -> list:
    """[(manifest, row name)] for every manifest that lists this page as `read` (the merge base)
    has it: a checksum file in the page's folder or any ancestor inside its strand, and each named
    JSON manifest whose keys the page falls under."""
    out, parts = [], page.split("/")
    for i in range(len(parts) - 1, 0, -1):
        folder = "/".join(parts[:i]) + "/"
        for name in DLG1_SUMS:
            text = read(folder + name)
            if text and page[len(folder):] in dlg1_rows(text.decode("utf-8", "replace"), "sums"):
                out.append((folder + name, page[len(folder):]))
    for manifest, keyroot in DLG1_JSON_MANIFESTS.items():
        if page.startswith(keyroot):
            text = read(manifest)
            if text and page[len(keyroot):] in dlg1_rows(text.decode("utf-8", "replace"), "json"):
                out.append((manifest, page[len(keyroot):]))
    return out


def judge_dlg1_record(rel: str, before: bytes, after: bytes, members: dict):
    """Pure. None when this manifest is its base bytes with exactly its page members' row digests
    re-cut to their bytes on disk, else why not.

    members  {row name: sha256 of that page's bytes on disk} -- the page members of THIS
             transaction that this manifest lists at the base"""
    kind = dlg1_manifest_kind(rel)
    if kind is None:
        return ("only a pack's SHA256SUMS.txt, or a JSON manifest the limb names (the Fallback "
                "pack's MANIFEST.json), is a DLG-1 record member")
    if not members:
        return "a manifest re-cut for a pack this transaction does not touch: it lists no page member"
    try:
        b, a = before.decode("utf-8"), after.decode("utf-8")
    except UnicodeDecodeError:
        return "the manifest is not UTF-8"
    b_lines, a_lines = b.splitlines(keepends=True), a.splitlines(keepends=True)
    if len(b_lines) != len(a_lines):
        return "the re-cut adds or drops a line: a re-cut changes digests, never rows"
    moved = {}
    for lb, la in zip(b_lines, a_lines):
        if lb == la:
            continue
        rb, ra = _dlg1_row(lb, kind), _dlg1_row(la, kind)
        if rb is None or ra is None or la != rb[2] + ra[1] + rb[3]:
            return "a changed line is not the same row with only its digest replaced"
        if rb[0] in moved:
            return f"the row for {rb[0]} moved twice"
        moved[rb[0]] = ra[1]
    if kind == "json":
        try:
            same_keys = list(json.loads(a)) == list(json.loads(b))
        except ValueError:
            return "the manifest is not JSON"
        if not same_keys:
            return "the manifest's keys moved: a re-cut changes digests, never keys"
    extra = sorted(set(moved) - set(members))
    if extra:
        return f"a digest moved for {extra[0]}, which is not a page member of this transaction"
    still = sorted(set(members) - set(moved))
    if still:
        return f"a page member's row did not move, so it would disagree with its bytes: {still[0]}"
    for row in sorted(moved):
        if moved[row] != members.get(row):
            return f"the re-cut digest for {row} is not the sha256 of its bytes on disk"
    return None


def dlg1_allowed(statuses, blob_reader, root=None) -> tuple[set, dict]:
    """The ruled DLG-1 limb over the changed paths: pages first, then the manifests re-cut from
    them, then each page whose listing manifest is not an admitted re-cut taken back out (and its
    manifests judged again without it). `blob_reader` reads the merge base; bytes on disk are read
    from `root` (default ROOT) -- the seam the boundary and the self-test use."""
    root = root or ROOT
    try:
        tools = dlg1_tools(root)
    except Refuse as why:
        return set(), {rel: str(why) for rel in statuses}
    cache = {}

    def read(rel):
        if rel not in cache:
            cache[rel] = blob_reader(rel) or b""
        return cache[rel]

    pages, why, digest, records = set(), {}, {}, {}
    for rel, status in sorted(statuses.items()):
        path = root / rel
        if status != "M" or path.is_symlink() or not path.is_file():
            why[rel] = "this transaction replaces landed files; this is not an 'M' of a regular file"
            continue
        data = path.read_bytes()
        if dlg1_manifest_kind(rel):
            records[rel] = (read(rel), data)
            continue
        if not rel.endswith(".html"):
            why[rel] = ("DLG-1 changes the pages its record names and the manifests that list "
                        "them, nothing else")
            continue
        reason = judge_dlg1(rel, read(rel), data, tools)
        if reason:
            why[rel] = reason
        else:
            pages.add(rel)
            digest[rel] = hashlib.sha256(data).hexdigest()
    listed = {page: dlg1_listing(page, read) for page in pages}
    while True:
        admitted = set()
        for rel, (before, after) in sorted(records.items()):
            members = {row: digest[page] for page in pages for m, row in listed[page] if m == rel}
            reason = judge_dlg1_record(rel, before, after, members)
            if reason:
                why.setdefault(rel, reason)   # the first cause, not the empty pack it leaves behind
            else:
                admitted.add(rel)
                why.pop(rel, None)
        dropped = set()
        for page in sorted(pages):
            missing = [m for m, _ in listed[page] if m not in admitted]
            if missing:
                m = missing[0]
                why[page] = (f"its pack manifest {m} lists it but is "
                             + (f"refused: {why[m]}" if m in records else "not re-cut in this transaction"))
                dropped.add(page)
        if not dropped:
            return pages | admitted, why
        pages -= dropped


# The ruled limbs the GLV3 boundary may re-judge a declared transaction by, by --limb name.
LIMB_WALKS = {"dlg-1": dlg1_allowed}


def limb_verdicts(limb: str, paths, blob_reader, root=None) -> dict:
    """{path: None, or the limb's reason}: a ruled limb's own verdict on each declared member,
    for the GLV3 boundary, which re-judges a limb-declared transaction rather than trusting it."""
    ok, why = LIMB_WALKS[limb]({rel: "M" for rel in paths}, blob_reader, root)
    return {rel: (None if rel in ok else why.get(rel, "not admitted by the limb")) for rel in paths}


def strand_kinds(strand: str, limb: str = "") -> tuple:
    """The path endings derive() collects. The explicit-tags limb also reads each pack's own two
    records, because a mark-up the record does not carry is a mark-up the pack cannot verify.
    Ruling S3: a Science pack manifest rides as a member. Every other limb sees .html.
    Ruling R8 §2: the DLG-1 limb collects EVERY changed path under both strands ("" ends every
    path), so a file it does not change is refused by name instead of left out of the declaration."""
    if limb == "dlg-1":
        return ("",)
    kinds = (".html",) + (SUMMER1_RECORDS if limb in ("explicit-tags", "responsive") else ())
    if strand == "Science" and not limb:
        kinds += ("/" + SCIENCE_RECORD,)
    return kinds


def diff_statuses(name_status: str, kinds: tuple) -> dict:
    """{path: status letter} from `git diff --name-status` output, for the paths ending in kinds.
    A rename or copy is keyed by its NEW path with status R/C, so a judge that requires 'M'
    refuses it by name."""
    statuses = {}
    for line in name_status.splitlines():
        parts = line.split("\t")
        if len(parts) >= 2 and parts[-1].endswith(kinds):
            statuses[parts[-1]] = parts[0][0]
    return statuses


def strand_landable(strand: str, limb: str, statuses: dict, blob_reader, base: str = "",
                    deck_limb=None, root=None) -> tuple[set, dict, set]:
    """derive()'s choice of limb, pure over its inputs: (landable, reason per refused path,
    derived records). Extracted so the self-test reaches the call derive() actually makes
    (review of the S3 PR: putting back the pre-S3 Science call left every check green)."""
    if limb == "dlg-1":
        allowed, why = dlg1_allowed(statuses, blob_reader, root)
        return allowed, why, {r for r in allowed if dlg1_manifest_kind(r)}
    if limb == "responsive":
        allowed, why = responsive_allowed(statuses, blob_reader)
        return allowed, why, {r for r in allowed if r.endswith(SUMMER1_RECORDS)}
    if limb == "explicit-tags":
        allowed, why = explicit_tags_allowed(statuses, blob_reader)
        return allowed, why, {r for r in allowed if r.endswith(SUMMER1_RECORDS)}
    if strand == "Science":
        return science_limb(statuses, blob_reader, deck_limb, root)
    return landable(base), {}, set()


def derive(base: str, strand: str = "Humanities", limb: str = "", *, root=None, registry=None,
           deck_limb=None) -> tuple[str, dict]:
    """root, registry, deck_limb: seams for the self-test, which runs THIS function against a
    throwaway git repository (review of the S3 PR: putting back the pre-S3 call inside derive(),
    reading the base from disk, or skipping the manifest's pin all left the self-test green).
    Defaults: this repository, CATALOGUE_PINS from the gate copy, the ruled deck limbs."""
    root = root or ROOT
    # R8 §2: the DLG-1 record spans both strands, so its limb reads both prefixes as one scope.
    prefixes = DLG1_PREFIXES if limb == "dlg-1" else (STRANDS[strand],)
    mb = merge_base(base, root)
    kinds = strand_kinds(strand, limb)
    statuses = diff_statuses(git("diff", "--name-status", f"{mb}..HEAD", "--", *prefixes, root=root), kinds)

    scope = "Humanities + Science, every" if limb == "dlg-1" else f"{strand} {' / '.join(kinds)}"
    print(f"SEARCH SCOPE: {len(statuses)} {scope} path(s) differing from "
          f"the merge base {mb[:12]} with {base}; blobs read from that merge base, digests from "
          f"the bytes on disk, pins from CATALOGUE_PINS in {GATE.relative_to(ROOT)}")

    base_blob = lambda rel: subprocess.run(["git", "show", f"{mb}:{rel}"], cwd=root,
                                           capture_output=True).stdout
    allowed, science_why, records = strand_landable(strand, limb, statuses, base_blob, base,
                                                    deck_limb, root)
    if limb == "dlg-1":
        print(f"  landable set from the ruled DLG-1 limb (the reviewed fixer reproduces these "
              f"bytes from the base under {DLG1_PAIRS}): {len(allowed) - len(records)} page(s) "
              f"and {len(records)} manifest(s) re-cut from them, {len(allowed)} of "
              f"{len(statuses)} path(s)")
    elif limb == "responsive":
        pages = len([r for r in allowed if not r.endswith(SUMMER1_RECORDS)])
        print(f"  landable set from the ruled responsive limb (the reviewed writer reproduces "
              f"these bytes from the base): {pages} page(s) and {len(allowed) - pages} derived "
              f"pack record(s), {len(allowed)} of {len(statuses)} path(s)")
    elif limb == "explicit-tags":
        pages = len([r for r in allowed if not r.endswith(SUMMER1_RECORDS)])
        print(f"  landable set from the ruled explicit-tags limb (DOM identical, the implied "
              f"tags written down): {pages} page(s) and {len(allowed) - pages} derived pack "
              f"record(s), {len(allowed)} of {len(statuses)} path(s)")
    elif strand == "Science":
        decks = sum(1 for r in statuses if not r.endswith("/" + SCIENCE_RECORD))
        print(f"  landable set from the ruled Science limb over "
              f"{BINDINGS.relative_to(ROOT)}: {len(allowed) - len(records)} of {decks} deck(s), "
              f"and {len(records)} pack manifest(s) re-cut from them (ruling S3)")
    else:
        print(f"  landable set from {CENSUS.relative_to(ROOT)}: {len(allowed)} deck(s)")
    registry = pins() if registry is None else registry
    files, refused = {}, []
    for rel, status in sorted(statuses.items()):
        path = root / rel
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
        files[rel] = {"beforeGitBlob": blob_at(mb, rel, root),
                      "afterSha256": digest,
                      "bytes": len(data)}

    for rel, why in refused:
        print(f"  REFUSED {rel}: {why}")
    if refused:
        raise Refuse(f"{len(refused)} path(s) refused; nothing declared")
    if not files:
        raise Refuse("no member to declare")
    print(f"  derived {len(files)} member(s)")
    return mb, files


def slug(name: str) -> str:
    return re.sub(r"[^A-Z0-9]+", "_", name.upper()).strip("_")


LIMB_NOTES = {
    "dlg-1": ("# RULING LAND-A2 R8 §2 · {name}: each control given the audience of the dialog it opens,\n"
              "# by tools/hum/fix_dialog_audience.py under tools/hum/DLG1_PAIRS.json, and the pack\n"
              "# manifests re-cut for exactly those pages. One transaction, derived and written by\n"
              "# tools/hum/admit_transaction.py --limb dlg-1; every member also carries a CATALOGUE_PINS\n"
              "# admission, and LIMB_JUDGED_TRANSACTIONS has the boundary re-judge every member.\n"),
}


def write(name: str, base_sha: str, files: dict, check: bool, limb: str = "") -> bool:
    mark = slug(name)
    var, basevar = f"{mark}_REPLACEMENTS", f"{mark}_REVIEW_BASE"
    text = original = BOUNDARY.read_text()
    if f"{basevar} = " not in text:
        note = LIMB_NOTES[limb].format(name=name) if limb in LIMB_NOTES else (
            f"# ORDER HUM-T · {name}: this batch's transplanted decks, each stage carrying the\n"
            f"# science exemplar's loop panel. One transaction, derived and written by\n"
            f"# tools/hum/admit_transaction.py. Every member also carries a CATALOGUE_PINS\n"
            f"# admission, which replacement_errors cross-checks.\n")
        text = text.replace(
            "# BEGIN DECLARED TRANSACTIONS\n",
            note + f"{basevar} = {base_sha!r}\n# BEGIN DECLARED TRANSACTIONS\n", 1)
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
    # STOP-R2 option (a): the explicit-tags limb, with the refusals the ruling implies.
    T = _tagger()
    page = "Humanities_Teesside/GROW_W27-W39_2026-27/GROW/Summer_1/W03/Sources_and_checks.html"
    implied = (b'<!doctype html><html lang="en-GB"><meta charset="utf-8">'
               b'<title>Sources</title><style>p{}</style><h2>Where this came from</h2>'
               b'<p>Ordnance Survey.</p></html>')
    marked = T.repair(implied.decode())[0].encode()
    check("explicit tags: a page marked up by the reviewed tool is a member",
          judge_explicit_tags(page, implied, marked) is None)
    check("RED PROOF (outside the fifty): a page outside the Summer 1 trees is refused",
          "not a Summer 1 pathway page" in
          judge_explicit_tags("Humanities_Teesside/GROW_W1-W8_2026-27/x.html", implied, marked))
    check("RED PROOF (already explicit): a page that wrote its tags down is refused",
          "already wrote head and body down" in judge_explicit_tags(page, marked, marked))
    check("RED PROOF (content edited): a mark-up that moves a byte is refused",
          "not what the reviewed tool produces" in
          judge_explicit_tags(page, implied, marked.replace(b"Ordnance", b"Ordinance")))
    nested = b'<!doctype html><html><head><title>t</title></head><body>' + implied + b'</body></html>'
    check("RED PROOF (a wrap, not a mark-up): a nested document is refused",
          judge_explicit_tags(page, implied, nested) is not None)
    check("RED PROOF (no document): a page with no <html> is refused by the tool itself",
          "refuses this page" in judge_explicit_tags(page, b"<h2>bare</h2>", b"<h2>bare</h2>"))

    # The pack record clause, derived from the page members.
    tree = "Humanities_Teesside/GROW_W27-W39_2026-27/"
    rel = "GROW/Summer_1/W03/Sources_and_checks.html"
    members = {rel: {"before": implied, "after": marked}}
    d0, d1 = hashlib.sha256(implied).hexdigest(), hashlib.sha256(marked).hexdigest()
    log_before = b"PACK CHANGELOG\nv3 as signed.\n"
    log_after = log_before + (
        "\n\nImplied tags written down on 1 served page\n"
        "tools/hum/explicit_document_tags.py (sha256 %s)\n\n"
        "    %s  %s -> %s  %6d -> %6d\n"
        % (tool_digest()[:16], rel, d0[:12], d1[:12], len(implied), len(marked))).encode()
    d_log = hashlib.sha256(log_after).hexdigest()
    disk = {"CHANGELOG.txt": log_after}
    check("explicit tags: a CHANGELOG appended with the derived entry is a member",
          judge_explicit_tags_record(tree + "CHANGELOG.txt", log_before, log_after,
                                     members, disk) is None)
    check("RED PROOF (CHANGELOG edited): a record whose signed text moved is refused",
          "edited, not appended to" in
          judge_explicit_tags_record(tree + "CHANGELOG.txt", log_before,
                                     log_after.replace(b"v3 as", b"v4 as"), members, disk))
    check("RED PROOF (a page the entry does not name): a missing table row is refused",
          "does not name every marked-up page" in
          judge_explicit_tags_record(tree + "CHANGELOG.txt", log_before,
                                     log_before + b"\n\nsha256 "
                                     + tool_digest()[:16].encode() + b"\n", members, disk))
    check("RED PROOF (a digest the bytes do not carry): a table row that lies is refused",
          "after-digest" in
          judge_explicit_tags_record(tree + "CHANGELOG.txt", log_before,
                                     log_after.replace(d1[:12].encode(), b"0" * 12),
                                     members, disk))
    check("RED PROOF (no tool digest): an entry that does not name the tool is refused",
          "tool's own digest" in
          judge_explicit_tags_record(tree + "CHANGELOG.txt", log_before,
                                     log_after.replace(tool_digest()[:16].encode(), b"0" * 16),
                                     members, disk))
    sums_before = ("%s  %s\n%s  CHANGELOG.txt\n%s  GROW/Summer_1/W03/GROW_SU1_W03_Lesson.html\n"
                   % (d0, rel, hashlib.sha256(log_before).hexdigest(), "b" * 64)).encode()
    sums_after = ("%s  %s\n%s  CHANGELOG.txt\n%s  GROW/Summer_1/W03/GROW_SU1_W03_Lesson.html\n"
                  % (d1, rel, d_log, "b" * 64)).encode()
    check("explicit tags: a SHA256SUMS re-cut for exactly the marked-up rows is a member",
          judge_explicit_tags_record(tree + "SHA256SUMS.txt", sums_before, sums_after,
                                     members, disk) is None)
    check("RED PROOF (a row appeared): a re-cut that adds a row is refused",
          "row set moved" in
          judge_explicit_tags_record(tree + "SHA256SUMS.txt", sums_before,
                                     sums_after + b"c" * 64 + b"  extra.html\n", members, disk))
    check("RED PROOF (a row vanished): a re-cut that drops a row is refused",
          "row set moved" in
          judge_explicit_tags_record(tree + "SHA256SUMS.txt", sums_before,
                                     b"\n".join(sums_after.split(b"\n")[:2]) + b"\n",
                                     members, disk))
    check("RED PROOF (an untouched file's row moved): a signed lesson's digest is refused",
          "did not touch" in
          judge_explicit_tags_record(tree + "SHA256SUMS.txt", sums_before,
                                     sums_after.replace(b"b" * 64, b"c" * 64), members, disk))
    check("RED PROOF (a marked-up file's row stood still): a stale digest is refused",
          "did not move" in
          judge_explicit_tags_record(tree + "SHA256SUMS.txt", sums_before,
                                     sums_after.replace(d1.encode(), d0.encode()), members, disk))
    check("RED PROOF (a re-cut digest that is not the bytes): a typed digest is refused",
          "not the digest of the bytes on disk" in
          judge_explicit_tags_record(tree + "SHA256SUMS.txt", sums_before,
                                     sums_after.replace(d_log.encode(), b"a" * 64), members, disk))
    check("RED PROOF (a record outside the trees): another pack's record is refused",
          "not a Summer 1 pathway record" in
          judge_explicit_tags_record("Humanities_Teesside/GROW_W1-W8_2026-27/SHA256SUMS.txt",
                                     sums_before, sums_after, members, disk))
    check("RED PROOF (another file in the pack root): only the two records are members",
          "only a pack's own" in
          judge_explicit_tags_record(tree + "README.md", log_before, log_after, members, disk))
    check("RED PROOF (a pack with no marked-up page): its record has nothing to re-cut",
          "nothing to re-cut" in
          judge_explicit_tags_record(tree + "CHANGELOG.txt", log_before, log_after, {}, disk))
    # RULING 2026-09-23 §4: the responsive limb, with the refusals its shape implies.
    R = _responsive()
    rpage = "Humanities_Teesside/GROW_W27-W39_2026-27/GROW/Summer_1/W03/GROW_SU1_W03_Pupil_Resources.html"
    plain = (b'<!doctype html><html lang="en-GB"><head><meta charset="utf-8">'
             b'<title>Pupil resources</title><style>body{max-width:180mm}</style></head>'
             b'<body><h1>Sheet</h1><table><tr><td>x</td></tr></table></body></html>')
    served = R.repair(plain.decode())[0].encode()
    check("responsive: a page the reviewed writer produces from its base bytes is a member",
          judge_responsive(rpage, plain, served) is None)
    check("RED PROOF (outside the trees): a page outside the Summer 1 trees is refused",
          "not a Summer 1 pathway page" in
          judge_responsive("Humanities_Teesside/GROW_W1-W8_2026-27/x.html", plain, served))
    check("RED PROOF (already responsive): a page that already carries the block is refused",
          "already carry the responsive furniture" in judge_responsive(rpage, served, served))
    check("RED PROOF (content edited beside correct furniture): a smuggled edit is refused",
          "not what the reviewed tool produces" in
          judge_responsive(rpage, plain, served.replace(b"<h1>Sheet</h1>", b"<h1>Sheat</h1>")))
    check("RED PROOF (hand-written furniture): a block that is not the reviewed bytes is refused",
          judge_responsive(rpage, plain,
                           served.replace(b"box-sizing: border-box",
                                          b"box-sizing: content-box")) is not None)
    check("RED PROOF (no </head>): a page the writer cannot place furniture in is refused",
          "refuses this page" in
          judge_responsive(rpage, b"<html><body><h1>bare</h1></body></html>",
                           b"<html><body><h1>bare</h1></body></html>"))
    # THE TRAP THIS LIMB MUST NOT FALL INTO: the explicit-tags limb would admit nothing here,
    # and the responsive limb must likewise admit nothing an explicit-tags transaction changed.
    # The two limbs read the same trees, so a member judged by the wrong one would slip through.
    marked = _tagger().repair(
        '<!doctype html><html lang="en-GB"><meta charset="utf-8"><title>t</title>'
        '<style>p{}</style><h2>h</h2></html>')[0].encode()
    check("RED PROOF (wrong limb): a marked-up page is not a responsive member",
          judge_responsive(rpage,
                           b'<!doctype html><html lang="en-GB"><meta charset="utf-8">'
                           b'<title>t</title><style>p{}</style><h2>h</h2></html>',
                           marked) is not None)
    check("RED PROOF (wrong limb, the other way): a responsive page is not a tags member",
          judge_explicit_tags(rpage, plain, served) is not None)
    # The record clause carries the RESPONSIVE writer's digest, not the tagger's, so a
    # CHANGELOG naming the wrong tool cannot pass for a derivation this transaction performed.
    check("the two limbs' tool digests differ, so a record cannot claim the wrong derivation",
          responsive_tool_digest() != tool_digest())

    check("the Humanities strand still maps to its own prefix, untouched",
          STRANDS["Humanities"] == PREFIX and STRANDS["Science"] == SCIENCE_PREFIX)

    # --- ruling 3 on the limbs review (2026-09-23): the deck's claim is its TITLE STAGE ---
    row4 = {"weeks": [{"key": "Aut1\u00b7W4"}]}
    recall = (b'<section class="slide"><p>BUILD \xc2\xb7 Science \xc2\xb7 Week 4A</p></section>'
              b'<section class="slide"><p>Retrieve the actual previous lesson: Aut1\xc2\xb7W3</p></section>')
    check("CLAIM: a recall line on a later stage is not the deck's claim, so form (iv) lands it",
          judge_science("Science_Teesside/B/x.html", row4, True, title_stage_text(recall)) is None)
    wrong = (b'<section class="slide"><p>BUILD \xc2\xb7 Science \xc2\xb7 Aut1\xc2\xb7W3</p></section>'
             b'<section class="slide"><p>body</p></section>')
    check("CLAIM RED PROOF: a title stage claiming the wrong week still refuses",
          "does not cover" in (judge_science("Science_Teesside/B/x.html", row4, True, title_stage_text(wrong)) or ""))
    check("CLAIM RED PROOF: the same wrong week read over the WHOLE deck would have refused the recall deck",
          "does not cover" in (judge_science("Science_Teesside/B/x.html", row4, True, flat_text(recall)) or ""))
    w16b = "Science_Teesside/Grow/W15-W20_2026-27/SCI_G_W16B_Getting_The_Solid_Back_Do.html"
    check("W16B RED PROOF, real tree: a title-stage week the row does not bind refuses, although the deck's own cell covers the row",
          "title stage states Spr1\u00b7W16" in science_allowed([w16b])[1].get(w16b, ""))
    row2 = {"weeks": [{"key": "Spr1\u00b7W2"}]}
    check("W16B RED PROOF, pure: title claim Spr1\u00b7W16 plus a covering cell still refuses",
          "does not bind" in (judge_science("Science_Teesside/G/x.html", row2, True, "Spring 1 \u00b7 Week 16",
                                            {"C"}, {"C": {"termWeek": "Spr1\u00b7W2"}}) or ""))
    check("and a title claim that IS the row, beside the same cell, still lands",
          judge_science("Science_Teesside/G/x.html", row2, True, "Spring 1 \u00b7 Week 2",
                        {"C"}, {"C": {"termWeek": "Spr1\u00b7W2"}}) is None)
    w4a = "Science_Teesside/Build/v3_40min/SCI_B_W4A_Muscles_Explore.html"
    check("CLAIM, real tree (the wiring): science_allowed lands SCI_B_W4A, whose only Aut1\u00b7W3 is a recall line",
          w4a in science_allowed([w4a])[0])

    # --- ruling S3: the Science pack-record limb, planted against the judge that decides ---
    h = lambda b: hashlib.sha256(b).hexdigest()
    man = "Science_Teesside/Launch/W8-W13_2026-27/SHA256SUMS.txt"
    deck_b, deck_a, other, stale_base = b"<html>deck before</html>", b"<html>deck after</html>", b"other", b"old"
    sums = lambda rows: "".join(f"{d}  {r}\n" for r, d in rows).encode()
    before = sums([("A.html", h(deck_b)), ("B.html", h(other)), ("C.html", h(stale_base))])
    after_ok = sums([("A.html", h(deck_a)), ("B.html", h(other)), ("C.html", h(other))])
    disk = {"A.html": h(deck_a), "B.html": h(other), "C.html": h(other)}.get
    base = {"A.html": h(deck_b), "B.html": h(other), "C.html": h(other)}.get
    members = {"A.html": {"after": deck_a}}
    check("S3: a manifest re-cut from its member's bytes is declared, a stale row riding along",
          judge_science_record(man, before, after_ok, members, disk, base) is None)
    check("S3 RED PROOF: a manifest whose row disagrees with the member's bytes is refused",
          "disagrees with the member's bytes" in (judge_science_record(
              man, before, sums([("A.html", h(deck_b)), ("B.html", h(other)), ("C.html", h(other))]),
              members, disk, base) or ""))
    w9l2 = "Science_Teesside/Launch/W8-W13_2026-27/SCI_L_W9L2_Mitosis_Sequence_Explore.html"
    check("S3 RED PROOF: a deck whose pack manifest is not in the transaction is refused",
          (lambda ok_why: "not re-cut in this transaction" in ok_why[1].get("Science_Teesside/Launch/W8-W13_2026-27/SCI_L_W9L2_Mitosis_Sequence_Explore.html", ""))(
              science_records_allowed({}, lambda rel: b"",
                                      {"Science_Teesside/Launch/W8-W13_2026-27/SCI_L_W9L2_Mitosis_Sequence_Explore.html"})))
    check("S3: a manifest re-cut for a pack no declared deck belongs to is refused",
          "does not touch" in (judge_science_record(man, before, after_ok, {}, disk, base) or ""))
    check("S3: a re-cut that adds or drops a row is refused (digests move, never rows)",
          "row set moved" in (judge_science_record(
              man, before, after_ok + f"{h(other)}  D.html\n".encode(), members, disk, base) or ""))
    check("S3: a row that was FRESH at the base and moves for an undeclared file is refused",
          "fresh at the base" in (judge_science_record(
              man, before, sums([("A.html", h(deck_a)), ("B.html", h(b"new")), ("C.html", h(other))]),
              members, {"A.html": h(deck_a), "B.html": h(b"new"), "C.html": h(other)}.get, base) or ""))
    check("S3: a riding-along row that is not the digest on disk is refused",
          "not the digest of the bytes on disk" in (judge_science_record(
              man, before, sums([("A.html", h(deck_a)), ("B.html", h(other)), ("C.html", h(b"wrong"))]),
              members, disk, base) or ""))
    check("S3: a deck with no row (a Classic) is not enrolled and not refused",
          judge_science_record(man, before, after_ok, {**members, "Z_Classic.html": {"after": b"x"}}, disk, base) is None)
    # Second cut, after the adversarial review of the first.
    check("S3 RED PROOF (the wiring): derive's Science limb takes a landable deck OUT when its pack "
          "manifest lists it and is not re-cut",
          (lambda r: w9l2 not in r[0] and "not re-cut in this transaction" in r[1].get(w9l2, ""))(
              science_limb({w9l2: "M"}, lambda rel: b"", deck_limb=lambda p: (set(p), {}))))
    check("S3 RED PROOF: a deck listed by an ANCESTOR pack manifest (Teaching_Packs/*/HTML/) is "
          "refused when that manifest is not re-cut",
          "Teaching_Packs/BUILD/SHA256SUMS.txt" in science_records_allowed({}, lambda rel: b"", {
              "Science_Teesside/Teaching_Packs/BUILD/HTML/BUILD_Science_W6A.html"})[1].get(
              "Science_Teesside/Teaching_Packs/BUILD/HTML/BUILD_Science_W6A.html", ""))
    check("S3: a row that was stale at the base but whose FILE changed outside the transaction is "
          "refused", "changed outside this transaction" in (judge_science_record(
              man, before, sums([("A.html", h(deck_a)), ("B.html", h(other)), ("C.html", h(b"ed"))]),
              members, {"A.html": h(deck_a), "B.html": h(other), "C.html": h(b"ed")}.get, base) or ""))
    check("S3: a re-cut whose only declared deck has no row is refused -- not derived from it",
          "not be derived from this transaction" in (judge_science_record(
              man, before, after_ok, {"Z_Classic.html": {"after": b"x"}}, disk, base) or ""))
    check("S3: a manifest whose declared deck is gone is refused by name, not by a traceback",
          "not a regular file" in science_records_allowed(
              {man: "M"}, lambda rel: before,
              {"Science_Teesside/Launch/W8-W13_2026-27/NO_SUCH_DECK.html"})[1].get(man, ""))
    check("S3: only a Science pack's own SHA256SUMS.txt is a record member",
          "only a Science pack" in (judge_science_record(
              "Humanities_Teesside/BUILD_W1-W8_2026-27/SHA256SUMS.txt", before, after_ok, members, disk, base) or ""))
    # --- the S3 WIRING on a real (temporary) pack: science_records_allowed / science_limb /
    # strand_landable read bytes from `root`, the merge base from the blob reader. Review of the S3
    # PR: every refusal above was proved at the pure judge only, so removing the line that ACTS on
    # its verdict, or putting back derive()'s pre-S3 call, left this self-test green.
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        troot = Path(tmp)
        pk = "Science_Teesside/Launch/TEST_pack/"
        deck, readme, man = pk + "A.html", pk + "README.md", pk + "SHA256SUMS.txt"
        base_files = {deck: b"<html>A before</html>", readme: b"readme", pk + "B.html": b"<html>B</html>"}
        stale = h(b"<html>B stale</html>")                        # B's row is already stale at the base
        base_man = (f"{h(base_files[deck])}  A.html\n{h(base_files[readme])}  README.md\n"
                    f"{stale}  B.html\n").encode()
        def lay(files):
            for rel, data in files.items():
                (troot / rel).parent.mkdir(parents=True, exist_ok=True)
                (troot / rel).write_bytes(data)
        after_deck = b"<html>A after</html>"
        good_man = (f"{h(after_deck)}  A.html\n{h(base_files[readme])}  README.md\n"
                    f"{h(base_files[pk + 'B.html'])}  B.html\n").encode()
        lay({**base_files, deck: after_deck, man: good_man})
        reader = {**base_files, man: base_man}.get
        stub = lambda decks: (set(decks), {})
        both = {deck: "M", man: "M"}
        allowed, why, records = science_limb(both, reader, stub, troot)
        check("S3 WIRING: a correct re-cut (a stale row riding along) lands deck AND manifest through science_limb",
              allowed == {deck, man} and records == {man} and not why)
        check("S3 WIRING: strand_landable -- the call derive() makes -- gives the same verdict",
              strand_landable("Science", "", both, reader, deck_limb=stub, root=troot) == (allowed, why, records))
        lay({man: good_man.replace(h(after_deck).encode(), h(b"not the bytes").encode())})
        allowed, why, records = strand_landable("Science", "", both, reader, deck_limb=stub, root=troot)
        check("S3 WIRING RED PROOF: a manifest whose row disagrees with the member's bytes is refused, and so is its deck",
              "disagrees with the member's bytes" in why.get(man, "") and "re-cut in this transaction but refused" in why.get(deck, "")
              and not allowed)
        lay({man: good_man, readme: b"readme edited outside",
             })
        moved = good_man.replace(h(base_files[readme]).encode(), h(b"readme edited outside").encode())
        lay({man: moved})
        allowed, why, records = strand_landable("Science", "", both, reader, deck_limb=stub, root=troot)
        check("S3 WIRING RED PROOF: a row FRESH at the base (read from the merge base, not disk) that moves for an undeclared file is refused",
              "fresh at the base" in why.get(man, "") and man not in allowed)
        lay({man: good_man, readme: base_files[readme]})
        allowed, why, records = strand_landable("Science", "", {deck: "M"}, reader, deck_limb=stub, root=troot)
        check("S3 WIRING RED PROOF: a deck whose pack manifest lists it but is not in the transaction is refused",
              "not re-cut in this transaction" in why.get(deck, "") and not allowed)
        lay({man: good_man.replace(b"  README.md\n", b"  README.md \n")})   # parses to the same rows
        allowed, why, records = strand_landable("Science", "", both, reader, deck_limb=stub, root=troot)
        check("S3 WIRING RED PROOF: a re-cut that rewrites a line beyond its digest is refused (bytes, not parsed rows)",
              "not the same row with only its digest replaced" in why.get(man, ""))
        (troot / man).unlink()
        ok, rwhy = science_records_allowed({deck: "M"}, reader, {deck}, troot)
        check("S3 WIRING RED PROOF: a manifest renamed or removed on the branch still binds the deck its base manifest lists",
              "not re-cut in this transaction" in rwhy.get(deck, ""))
        lay({man: good_man})
        ok, rwhy = science_records_allowed({man: "D"}, reader, set(), troot)
        check("S3 WIRING: a manifest that is not an 'M' is refused by name",
              "not an 'M'" in rwhy.get(man, ""))
        classic = pk + "C_Classic.html"
        lay({classic: b"<html>C</html>"})
        ok, rwhy = science_records_allowed({}, reader, {classic}, troot)
        check("S3 WIRING: a deck with no manifest row (a Classic) is not enrolled and not refused (correction #32)",
              classic not in rwhy)
        lay({man: good_man + b"\n"})
        allowed, why, records = strand_landable("Science", "", both, reader, deck_limb=stub, root=troot)
        check("S3 WIRING RED PROOF: a re-cut that adds a line (here a blank one) is refused -- digests move, never lines",
              "changes lines, not only row digests" in why.get(man, ""))

    # --- derive() ITSELF, against a throwaway git repository (review of the S3 fix round: the
    # seams above left derive()'s own call, its merge-base reader and its pin lookup untested).
    # The throwaway repository must never touch the caller's: every git variable that could point
    # at another repository or index is removed for the block, and nothing is signed (review of the
    # S3 PR head: with GIT_DIR or GIT_INDEX_FILE exported, as a pre-commit hook does, the self-test
    # committed into the caller's repository and still printed PASS).
    import contextlib, io
    leak = ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_OBJECT_DIRECTORY",
            "GIT_ALTERNATE_OBJECT_DIRECTORIES", "GIT_COMMON_DIR", "GIT_NAMESPACE", "GIT_PREFIX")
    saved = {k: os.environ.pop(k) for k in leak if k in os.environ}
    try:
      with tempfile.TemporaryDirectory() as tmp:
        repo = Path(tmp)
        g = lambda *a: subprocess.run(["git", "-c", "commit.gpgsign=false", "-c", "tag.gpgsign=false", *a],
                                      cwd=repo, capture_output=True, text=True, check=True).stdout.strip()
        g("init", "-q"); g("config", "user.email", "t@t"); g("config", "user.name", "t")
        pk = "Science_Teesside/Launch/TEST_pack/"
        deck, readme, man = pk + "A.html", pk + "README.md", pk + "SHA256SUMS.txt"
        before = {deck: b"<html>A before</html>", readme: b"readme"}
        man0 = f"{h(before[deck])}  A.html\n{h(before[readme])}  README.md\n".encode()
        def put(files):
            for rel, data in files.items():
                (repo / rel).parent.mkdir(parents=True, exist_ok=True)
                (repo / rel).write_bytes(data)
        put({**before, man: man0}); g("add", "-A"); g("commit", "-qm", "base")
        base_sha = g("rev-parse", "HEAD")
        # The BASE the operator names is a side tip, so it differs from the merge base: derive()
        # must read before-bytes and before-blobs at the merge base, never at the named base.
        g("checkout", "-qb", "side"); side_readme = b"readme on the side"
        put({readme: side_readme, man: man0.replace(h(before[readme]).encode(), h(side_readme).encode())})
        g("add", "-A"); g("commit", "-qm", "side"); side_sha = g("rev-parse", "HEAD")
        g("checkout", "-q", "-"); g("reset", "-q", "--hard", base_sha)
        stub = lambda decks: (set(decks), {})
        after = b"<html>A after</html>"
        man1 = man0.replace(h(before[deck]).encode(), h(after).encode())
        def run_case(files, pinned):
            g("reset", "-q", "--hard", base_sha)
            put(files); g("add", "-A"); g("commit", "-qm", "case")
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                mb = None
                try:
                    mb, got = derive(side_sha, "Science", root=repo, deck_limb=stub,
                                     registry={r: h((repo / r).read_bytes()) for r in pinned})
                except Refuse as why:
                    return (None, mb), out.getvalue() + str(why)
            return (got, mb), out.getvalue()
        (got, mb), log = run_case({deck: after, man: man1}, [deck, man])
        check("S3 DERIVE: a deck and its correctly re-cut, pinned manifest are declared together by derive() itself",
              got is not None and set(got) == {deck, man} and mb == base_sha)
        check("S3 DERIVE: each declared member's before-blob is the MERGE BASE's, and its after-digest the bytes on disk",
              got is not None and all(got[r]["beforeGitBlob"] == g("rev-parse", f"{base_sha}:{r}")
                                      and got[r]["afterSha256"] == h((repo / r).read_bytes()) for r in (deck, man)))
        (got, _), log = run_case({deck: after}, [deck])
        check("S3 DERIVE RED PROOF: derive() refuses a deck whose pack manifest is not re-cut",
              got is None and "not re-cut in this transaction" in log)
        (got, _), log = run_case({deck: after, readme: b"readme edited",
                             man: man1.replace(h(before[readme]).encode(), h(b"readme edited").encode())}, [deck, man])
        check("S3 DERIVE RED PROOF: derive() reads the manifest's before-bytes from the merge base (a fresh row moved for an undeclared file refuses)",
              got is None and "fresh at the base" in log)
        (got, _), log = run_case({deck: after, man: man1}, [deck])
        check("S3 DERIVE RED PROOF: derive() refuses a re-cut manifest with no CATALOGUE_PINS admission",
              got is None and "no CATALOGUE_PINS admission" in log)
    finally:
        os.environ.update(saved)

    check("S3: derive() collects Science pack manifests as members, and only in the Science strand's own limb",
          strand_kinds("Science") == (".html", "/" + SCIENCE_RECORD) and strand_kinds("Humanities") == (".html",)
          and "/" + SCIENCE_RECORD not in strand_kinds("Science", "responsive"))
    check("S3: a renamed manifest reaches the judges keyed by its new path with status R",
          diff_statuses("M\tScience_Teesside/x/SHA256SUMS.txt\nR100\tScience_Teesside/o/SHA256SUMS.txt\tScience_Teesside/n/SHA256SUMS.txt\nM\ta.css\n",
                        strand_kinds("Science")) == {"Science_Teesside/x/SHA256SUMS.txt": "M", "Science_Teesside/n/SHA256SUMS.txt": "R"})
    check("S3: a Science manifest member with no CATALOGUE_PINS admission is refused (the 'pinned' clause)",
          "no CATALOGUE_PINS admission" in (judge_member(man, "M", {man}, None, "a" * 64) or ""))
    check("S3: a Science path that is not a manifest is not a record member",
          "only a Science pack" in (judge_science_record("Science_Teesside/Launch/x/notes.txt", b"", b"", {"a": 1}, None, None) or ""))

    # --- RULING LAND-A2 R8 §2: the DLG-1 limb, with the refusals the ruling and its order name ---
    D = dlg1_tools()
    DF, dpairs, dheld = D
    check("DLG-1: the fixer and the pairs record on disk are the reviewed bytes the limb pins",
          h((ROOT / DLG1_FIXER).read_bytes()) == DLG1_FIXER_SHA256
          and h((ROOT / DLG1_PAIRS).read_bytes()) == DLG1_PAIRS_SHA256)
    w8b = "Science_Teesside/Build/W8-W13_2026-27/SCI_B_W8B_Autumn_Science_Checkpoint_Do.html"
    check("DLG-1 (R8 §1): SCI_B_W8B is held out by name, dated, with its measured pairs and no pair of its own",
          w8b in dheld and w8b not in dpairs and dheld[w8b].get("until") and dheld[w8b].get("pairs"))
    dpage = next(p for p in sorted(dpairs) if p.startswith(PREFIX) and dpairs[p] == [("cold-call", "cold-call-dialog")])
    dsci = next(p for p in sorted(dpairs) if p.startswith(SCIENCE_PREFIX) and dpairs[p] == [("cold-call", "cold-call-dialog")])
    plain_d = (b'<!doctype html><html lang="en-GB"><head><meta charset="utf-8"><title>t</title></head><body>'
               b'<button class="tool" data-action="cold-call" type="button">Cold Call</button>'
               b'<dialog id="cold-call-dialog" data-audience="staff" data-mbm-guide="staff"><p>Who?</p></dialog>'
               b'<script>document.querySelector("[data-action]");</script></body></html>')
    fixed_d = DF.fix_text(plain_d.decode(), dpairs[dpage])[0].encode()
    check("DLG-1: a recorded page the reviewed fixer produces from its base bytes is a member",
          judge_dlg1(dpage, plain_d, fixed_d, D) is None)
    check("DLG-1: the fixer adds exactly the dialog's own audience to the control's opening tag, nothing else",
          fixed_d == plain_d.replace(b'type="button">', b'type="button" data-audience="staff" data-mbm-guide="staff">'))
    check("RED PROOF (one extra byte): a page one byte beyond the fixer's output is refused",
          "not what the reviewed fixer produces" in (judge_dlg1(dpage, plain_d, fixed_d + b"\n", D) or ""))
    check("RED PROOF (a smuggled edit beside a correct fix): a moved byte elsewhere is refused",
          "not what the reviewed fixer produces" in
          (judge_dlg1(dpage, plain_d, fixed_d.replace(b"Who?", b"Who!"), D) or ""))
    check("RED PROOF (a hand-written audience): an audience the dialog does not carry is refused",
          judge_dlg1(dpage, plain_d, fixed_d.replace(b'data-audience="staff" data-mbm',
                                                     b'data-audience="pupil" data-mbm'), D) is not None)
    unrecorded = "Humanities_Teesside/BUILD_W1-W8_2026-27/NOT_IN_THE_DLG1_RECORD.html"
    check("RED PROOF (not in the record): a page the fixer changes but the record does not name is refused",
          unrecorded not in dpairs and "record names" in (judge_dlg1(unrecorded, plain_d, fixed_d, D) or ""))
    w8b_base = (ROOT / w8b).read_bytes()
    w8b_fixed = DF.fix_text(w8b_base.decode("utf-8"),
                            [(p["action"], p["dialog"]) for p in dheld[w8b]["pairs"]])[0].encode()
    check("RED PROOF (SCI_B_W8B, real bytes): W8B changed by the reviewed fixer itself is refused -- held out "
          "by R8 §1, it is not in the record",
          w8b_fixed != w8b_base and "held out of DLG-1 by ruling" in (judge_dlg1(w8b, w8b_base, w8b_fixed, D) or ""))
    check("RED PROOF (already fixed): a page whose base bytes already carry the audience has nothing to fix",
          "nothing to fix" in (judge_dlg1(dpage, fixed_d, fixed_d, D) or ""))
    bare = plain_d.replace(b' data-audience="staff" data-mbm-guide="staff"><p>', b"><p>")
    check("RED PROOF (the fixer's own refusal): a dialog with no audience to copy is refused",
          "refuses this page" in (judge_dlg1(dpage, bare, bare, D) or ""))
    check("RED PROOF (wrong limb): a DLG-1 page is not a responsive member",
          judge_responsive(dpage, plain_d, fixed_d) is not None)
    check("RED PROOF (wrong limb, the other way): a responsive page is not a DLG-1 member",
          judge_dlg1(rpage, plain, served, D) is not None)

    # The record clause: digests of this transaction's page members, and nothing else.
    sums_rel = "Humanities_Teesside/Teaching_Packs/HUM_TEST_Reviewed/SHA256SUMS.txt"
    row = "BUILD/Autumn_1/W01/BUILD_A1_W01_Lesson.html"
    stale = "0" * 64
    sums_b = (f"{h(plain_d)}  {row}\n{h(b'pdf')}  BUILD/Autumn_1/W01/Pupil.pdf\n{stale}  README.txt\n").encode()
    sums_a = sums_b.replace(h(plain_d).encode(), h(fixed_d).encode())
    mem = {row: h(fixed_d)}
    J = judge_dlg1_record
    check("DLG-1 record: a SHA256SUMS whose only change is its page member's digest, re-cut to the page's "
          "bytes, is a member", J(sums_rel, sums_b, sums_a, mem) is None)
    check("RED PROOF (a non-digest byte): a row renamed beside a correct re-cut is refused",
          "only its digest replaced" in (J(sums_rel, sums_b, sums_a.replace(b"Pupil.pdf", b"Pupil2.pdf"), mem) or ""))
    check("RED PROOF (a non-digest byte): whitespace added to the re-cut row itself is refused",
          "only its digest replaced" in (J(sums_rel, sums_b, sums_a.replace(f"  {row}\n".encode(),
                                                                            f"  {row} \n".encode()), mem) or ""))
    check("RED PROOF (a line added): a re-cut that adds a line is refused",
          "adds or drops a line" in (J(sums_rel, sums_b, sums_a + b"\n", mem) or ""))
    swapped = b"".join([sums_a.splitlines(keepends=True)[i] for i in (1, 0, 2)])
    check("RED PROOF (rows reordered): a re-cut that moves a row is refused",
          "only its digest replaced" in (J(sums_rel, sums_b, swapped, mem) or ""))
    check("RED PROOF (a digest that is not the bytes): a re-cut digest unequal to the member on disk is refused",
          "not the sha256 of its bytes on disk" in
          (J(sums_rel, sums_b, sums_b.replace(h(plain_d).encode(), h(b"other").encode()), mem) or ""))
    check("RED PROOF (a stale row riding along): a digest moved for a file this transaction did not change is "
          "refused, even a row already stale at the base",
          "not a page member of this transaction" in
          (J(sums_rel, sums_b, sums_a.replace(stale.encode(), h(b"readme").encode()), mem) or ""))
    check("RED PROOF (a member left stale): a page member whose row did not move is refused",
          "did not move" in (J(sums_rel, sums_b, sums_b, mem) or ""))
    check("RED PROOF (an untouched pack): a manifest that lists no page member of the transaction is refused",
          "lists no page member" in (J(sums_rel, sums_b, sums_a, {}) or ""))
    check("RED PROOF (not a manifest): another file of the pack is not a record member",
          "only a pack's" in (J(sums_rel.replace("SHA256SUMS.txt", "README.txt"), sums_b, sums_a, mem) or ""))
    jrel = next(iter(DLG1_JSON_MANIFESTS))
    jkey = "HUM_Autumn_1_BUILD_GROW_Fallback/BUILD/Autumn_1/W01/BUILD_A1_W01_Lesson.html"
    jother = "HUM_Autumn_1_BUILD_GROW_Fallback/BUILD/Autumn_1/W01/BUILD_A1_W01_Knowledge_Organiser.pdf"
    json_b = ('{\n"%s": "%s",\n"%s": "%s"\n}' % (jother, h(b"pdf"), jkey, h(plain_d))).encode()
    json_a = json_b.replace(h(plain_d).encode(), h(fixed_d).encode())
    jm = {jkey: h(fixed_d)}
    check("DLG-1 record (R8 §5): the Fallback MANIFEST.json with only its page member's sha256 re-cut is a member",
          J(jrel, json_b, json_a, jm) is None)
    check("RED PROOF (R8 §5, another value): a MANIFEST.json sha256 other than a page member's changed is refused",
          "not a page member of this transaction" in
          (J(jrel, json_b, json_a.replace(h(b"pdf").encode(), h(b"pdf2").encode()), jm) or ""))
    check("RED PROOF (R8 §5, a key renamed): a MANIFEST.json key changed beside the re-cut is refused",
          "only its digest replaced" in (J(jrel, json_b, json_a.replace(b".pdf", b".PDF"), jm) or ""))
    check("RED PROOF (R8 §5, the structure): a MANIFEST.json byte outside every row changed is refused",
          "only its digest replaced" in (J(jrel, json_b, json_a.replace(b"{\n", b"{ \n"), jm) or ""))
    check("RED PROOF (R8 §5, not the bytes): a MANIFEST.json sha256 unequal to its page on disk is refused",
          "not the sha256 of its bytes on disk" in
          (J(jrel, json_b, json_b.replace(h(plain_d).encode(), h(b"x").encode()), jm) or ""))
    check("RED PROOF (an unnamed JSON manifest): a MANIFEST.json the limb does not name is not a record member",
          "only a pack's" in (J("Humanities_Teesside/Teaching_Packs/OTHER/MANIFEST.json", json_b, json_a, jm) or ""))

    # The pins on the fixer and the record: a changed tool or a widened record refuses the limb.
    import shutil
    with tempfile.TemporaryDirectory() as tmp:
        troot = Path(tmp)
        for rel in (DLG1_FIXER, DLG1_PAIRS):
            (troot / rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / rel, troot / rel)
        check("DLG-1: a faithful copy of the fixer and the record loads the same pairs", dlg1_tools(troot)[1] == dpairs)
        def refusal(root):
            try:
                dlg1_tools(root)
            except Refuse as why:
                return str(why)
            return ""
        (troot / DLG1_FIXER).write_bytes((ROOT / DLG1_FIXER).read_bytes() + b"\n")
        check("RED PROOF (changed fixer): a fixer one byte from its pinned digest refuses the limb",
              DLG1_FIXER in refusal(troot) and "cannot widen the limb" in refusal(troot))
        ok, why = dlg1_allowed({dpage: "M"}, {dpage: plain_d}.get, troot)
        check("RED PROOF (changed fixer, the wiring): every path is refused, not one admitted",
              not ok and "cannot widen the limb" in why.get(dpage, ""))
        shutil.copy2(ROOT / DLG1_FIXER, troot / DLG1_FIXER)
        widened = json.loads((ROOT / DLG1_PAIRS).read_text())
        widened["pairs"].append({"page": unrecorded, "action": "cold-call", "dialog": "cold-call-dialog"})
        (troot / DLG1_PAIRS).write_text(json.dumps(widened))
        check("RED PROOF (widened record): a pairs record naming one more page refuses the limb",
              DLG1_PAIRS in refusal(troot) and "cannot widen the limb" in refusal(troot))

    # --- the DLG-1 WIRING on a real (temporary) tree: dlg1_allowed / strand_landable read bytes from
    # `root` and the merge base from the blob reader, with the real pinned fixer and record.
    with tempfile.TemporaryDirectory() as tmp:
        troot = Path(tmp)
        def lay(files):
            for rel, data in files.items():
                (troot / rel).parent.mkdir(parents=True, exist_ok=True)
                (troot / rel).write_bytes(data)
        lay({rel: (ROOT / rel).read_bytes() for rel in (DLG1_FIXER, DLG1_PAIRS)})
        parts = dpage.split("/")                             # a manifest up to two folders above the page
        pack = "/".join(parts[:max(2, len(parts) - 3)]) + "/"
        man = pack + "SHA256SUMS.txt"
        base_man = f"{h(plain_d)}  {dpage[len(pack):]}\n{h(b'x')}  other.pdf\n".encode()
        good_man = base_man.replace(h(plain_d).encode(), h(fixed_d).encode())
        base_files = {dpage: plain_d, man: base_man, dsci: plain_d, w8b: w8b_base}
        reader = base_files.get
        lay({dpage: fixed_d, man: good_man, dsci: fixed_d})
        both = {dpage: "M", man: "M", dsci: "M"}
        ok, why = dlg1_allowed(both, reader, troot)
        check("DLG-1 WIRING: a Humanities page, its re-cut ancestor manifest and a Science page are admitted as one "
              "transaction", ok == {dpage, man, dsci} and not why)
        check("DLG-1 WIRING: strand_landable -- the call derive() makes -- gives the same verdict, whatever the strand",
              strand_landable("Science", "dlg-1", both, reader, root=troot) == (ok, why, {man})
              and strand_landable("Humanities", "dlg-1", both, reader, root=troot) == (ok, why, {man}))
        ok, why = dlg1_allowed({dpage: "M", dsci: "M"}, reader, troot)
        check("DLG-1 WIRING RED PROOF: a page whose manifest lists it but is not re-cut is refused",
              "not re-cut in this transaction" in why.get(dpage, "") and ok == {dsci})
        lay({man: good_man.replace(b"other.pdf", b"other.PDF")})
        ok, why = dlg1_allowed(both, reader, troot)
        check("DLG-1 WIRING RED PROOF: a refused manifest takes its page out with it",
              "only its digest replaced" in why.get(man, "") and "refused:" in why.get(dpage, "")
              and dpage not in ok and man not in ok)
        lay({man: good_man, pack + "notes.txt": b"n"})
        ok, why = dlg1_allowed({**both, pack + "notes.txt": "M"}, {**base_files, pack + "notes.txt": b"m"}.get, troot)
        check("DLG-1 WIRING RED PROOF: a changed file that is neither a recorded page nor a manifest is refused by name",
              "nothing else" in why.get(pack + "notes.txt", "") and ok == {dpage, man, dsci})
        ok, why = dlg1_allowed({dpage: "A", man: "M"}, reader, troot)
        check("DLG-1 WIRING RED PROOF: an addition is not a member, and its manifest then re-cuts for no member",
              "not an 'M'" in why.get(dpage, "") and "lists no page member" in why.get(man, "") and not ok)
        lay({w8b: w8b_fixed})
        ok, why = dlg1_allowed({**both, w8b: "M"}, reader, troot)
        check("DLG-1 WIRING RED PROOF: SCI_B_W8B fixed and offered beside the 173 is refused by name",
              "held out" in why.get(w8b, "") and w8b not in ok and ok == {dpage, man, dsci})
        check("DLG-1: derive() collects every changed path of both strands for the limb",
              strand_kinds("Humanities", "dlg-1") == ("",) and
              diff_statuses("M\tHumanities_Teesside/a.html\nM\tScience_Teesside/b/notes.txt\n",
                            strand_kinds("Science", "dlg-1")) == {"Humanities_Teesside/a.html": "M",
                                                                   "Science_Teesside/b/notes.txt": "M"})
        check("DLG-1: limb_verdicts -- the boundary's call -- agrees with the walk",
              limb_verdicts("dlg-1", [dpage, man, dsci, w8b], reader, troot)
              == {dpage: None, man: None, dsci: None, w8b: why[w8b]})

    # --- derive() ITSELF with --limb dlg-1, against a throwaway git repository.
    saved = {k: os.environ.pop(k) for k in leak if k in os.environ}
    try:
      with tempfile.TemporaryDirectory() as tmp:
        repo = Path(tmp)
        g = lambda *a: subprocess.run(["git", "-c", "commit.gpgsign=false", "-c", "tag.gpgsign=false", *a],
                                      cwd=repo, capture_output=True, text=True, check=True).stdout.strip()
        g("init", "-q"); g("config", "user.email", "t@t"); g("config", "user.name", "t")
        put = lambda files: [((repo / r).parent.mkdir(parents=True, exist_ok=True), (repo / r).write_bytes(d))
                             for r, d in files.items()]
        put({rel: (ROOT / rel).read_bytes() for rel in (DLG1_FIXER, DLG1_PAIRS)})
        put({dpage: plain_d, man: base_man, dsci: plain_d, w8b: w8b_base}); g("add", "-A"); g("commit", "-qm", "base")
        base_sha = g("rev-parse", "HEAD")
        def run_case(files):
            g("reset", "-q", "--hard", base_sha)
            put(files); g("add", "-A"); g("commit", "-qm", "case")
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                try:
                    _, got = derive(base_sha, "Humanities", "dlg-1", root=repo,
                                    registry={r: h((repo / r).read_bytes()) for r in files})
                except Refuse as why:
                    return None, out.getvalue() + str(why)
            return got, out.getvalue()
        got, log = run_case({dpage: fixed_d, man: good_man, dsci: fixed_d})
        check("DLG-1 DERIVE: derive() declares a Humanities page, its re-cut manifest and a Science page as one "
              "transaction, before-blobs from the merge base",
              got is not None and set(got) == {dpage, man, dsci}
              and all(got[r]["beforeGitBlob"] == g("rev-parse", f"{base_sha}:{r}") for r in got))
        got, log = run_case({dpage: fixed_d + b"\n", man: base_man.replace(h(plain_d).encode(), h(fixed_d + b"\n").encode())})
        check("DLG-1 DERIVE RED PROOF: one byte beyond the fixer output refuses the declaration",
              got is None and "not what the reviewed fixer produces" in log)
        got, log = run_case({dpage: fixed_d})
        check("DLG-1 DERIVE RED PROOF: a page whose manifest is not re-cut refuses the declaration",
              got is None and "not re-cut in this transaction" in log)
        got, log = run_case({dpage: fixed_d, man: good_man, w8b: w8b_fixed})
        check("DLG-1 DERIVE RED PROOF: SCI_B_W8B changed beside the others refuses the declaration",
              got is None and "held out of DLG-1 by ruling" in log)
    finally:
        os.environ.update(saved)

    print("self-test " + ("PASS" if not bad else f"FAIL ({bad})"))
    return 1 if bad else 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--name", help="transaction name, e.g. 'HUM-T batch 1 BUILD'")
    parser.add_argument("--base", default="origin/main")
    parser.add_argument("--strand", default="Humanities", choices=sorted(STRANDS))
    parser.add_argument("--limb", default="", choices=["", "explicit-tags", "responsive", "dlg-1"],
                        help="the ruled limb that decides the landable set (dlg-1 reads both "
                             "strands; --strand is not consulted)")
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
        changed = write(args.name, base_sha, files, args.check, args.limb)
    except (Refuse, subprocess.CalledProcessError) as exc:
        print(f"[FAIL] {exc}")
        return 1
    return 1 if (args.check and changed) else 0


if __name__ == "__main__":
    raise SystemExit(main())
