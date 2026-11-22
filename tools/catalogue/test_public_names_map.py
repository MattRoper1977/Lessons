#!/usr/bin/env python3
"""N3a proofs for the plain public wording of the catalogue (ruling thread, 22 Nov 2026).

The guard on the first 755 catalogue rows keeps its strength: it gained a reviewed
new digest, and this test proves every difference is the reviewed map.

No old wording is stored in this repository, so the old rows are read from the
base commit in git history (BASE below). Run from a clone that has that commit:

    git fetch --depth=1 origin <BASE>      # once, in a shallow clone
    python3 tools/catalogue/test_public_names_map.py

Proofs, each fatal on failure:
  1. the base rows carry the digest the guard held before N3a;
  2. applying the map to the base rows gives the current first 1,422 rows byte for
     byte (so the map alone explains the new digest), and only the declared fields
     differ; row count, order and every file path are unchanged;
  3. with the declared fields removed, the first 755 rows digest the same before and after;
  4. every old id resolves through assets/catalogue/old-ids.json to the row with the
     same file, every old subject value resolves to that row's subject now, and no
     old id or old subject value appears unhashed in a public catalogue file;
  5. an unknown value resolves to nothing (no redirect), and no new value is a map key.
"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from pin_catalogue_contract import ORIGINAL_ROW_COUNT, ORIGINAL_ROWS_SHA256, SHELF_ROWS, row_digest, without_tags  # noqa: E402
import apply_public_names as apply  # noqa: E402

BASE = "ed7cd6f6f21a7567bf9230e8011d8d6b455a8ae3"
BASE_ORIGINAL_ROWS_SHA256 = "15150552200dcf96089afd27ec81b5712a63aef929d07e62544dda6fa53b703b"
PUBLIC_FILES = ("resources.json", "assets/catalogue/old-ids.json", "assets/catalogue/display-titles.json", "assets/catalogue/pack-notes.json")


def fail(message: str):
    print("[FAIL] " + message)
    raise SystemExit(1)


def main() -> int:
    shown = subprocess.run(["git", "-C", str(ROOT), "show", BASE + ":resources.json"], capture_output=True)
    if shown.returncode != 0:
        fail("base commit not in this clone; run: git fetch --depth=1 origin " + BASE)
    old = json.loads(shown.stdout.decode("utf-8"))
    new = json.loads((ROOT / "resources.json").read_text("utf-8"))
    record = json.loads(apply.MAP.read_text("utf-8"))
    strings, fields = apply.load_map(), set(record["fields"])
    fixed = ORIGINAL_ROW_COUNT + len(SHELF_ROWS)

    if row_digest(without_tags(old[:ORIGINAL_ROW_COUNT])) != BASE_ORIGINAL_ROWS_SHA256:
        fail("the base rows do not carry the digest the guard held before N3a")
    if row_digest(without_tags(new[:ORIGINAL_ROW_COUNT])) != ORIGINAL_ROWS_SHA256:
        fail("the current rows do not carry the guard's digest")

    if len(old) != len(new) or [r["file"] for r in old] != [r["file"] for r in new]:
        fail("row count, order or a file path changed")
    mapped = apply.swap(old[:fixed], strings, [0])
    if mapped != new[:fixed]:
        fail("the map applied to the base rows does not give the current rows")
    touched = {key for a, b in zip(old[:fixed], new[:fixed]) for key in a if a[key] != b.get(key)}
    if not touched <= fields:
        fail("a field outside the declared ones changed: " + ", ".join(sorted(touched - fields)))

    strip = lambda rows: [{k: v for k, v in r.items() if k not in fields} for r in without_tags(rows)]
    if row_digest(strip(old[:ORIGINAL_ROW_COUNT])) != row_digest(strip(new[:ORIGINAL_ROW_COUNT])):
        fail("an undeclared field of an original row changed")

    lookup = json.loads((ROOT / "assets/catalogue/old-ids.json").read_text("utf-8"))
    public = "\n".join((ROOT / name).read_text("utf-8") for name in PUBLIC_FILES)
    ids_now = {r["id"] for r in new}
    moved = 0
    for a, b in zip(old, new):
        resolved = a["id"] if a["id"] == b["id"] else lookup["ids"].get(apply.digest(a["id"]))
        if resolved != b["id"]:
            fail("an old id does not resolve to its own row (row file digest " + apply.digest(a["file"])[:12] + ")")
        if a["id"] != b["id"]:
            moved += 1
            if a["id"] in ids_now or json.dumps(a["id"]) in public:
                fail("an old id is still present unhashed (id digest " + apply.digest(a["id"])[:12] + ")")
        if a["subject"] != b["subject"]:
            if lookup["subjects"].get(apply.digest(a["subject"])) != b["subject"]:
                fail("an old subject value does not resolve")
            if json.dumps(a["subject"], ensure_ascii=False) in public:
                fail("an old subject value is still present unhashed")
    if len({r["id"] for r in new}) != len(new):
        fail("ids are no longer unique")
    probe = apply.digest("no-such-id-n3a-probe")
    if probe in lookup["ids"] or probe in lookup["subjects"]:
        fail("the unknown-value probe resolved")
    for group in ("ids", "subjects"):
        if any(apply.digest(value) in lookup[group] for value in lookup[group].values()):
            fail("a new value is itself an old key (redirect loop)")
    print(f"[PASS] public names map: {len(old)} rows in order, {len(strings)} map entries, {moved} ids moved and all {len(old)} old ids resolve; "
          f"only {', '.join(sorted(touched))} changed; base digest {BASE_ORIGINAL_ROWS_SHA256[:8]} -> {ORIGINAL_ROWS_SHA256[:8]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
