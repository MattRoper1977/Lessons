#!/usr/bin/env python3
"""N3a: the old-address list, assets/catalogue/old-ids.json.

Built from tools/catalogue/PUBLIC_NAMES_MAP.json and the current catalogue. It
holds SHA-256 hashes of old values only, never the old wording:

    ids       hash of an old row id          -> the row's id now
    subjects  hash of an old subject value,  -> the subject value now,
              or of its old card slug           or the card slug now

    python3 tools/catalogue/build_old_ids.py            write
    python3 tools/catalogue/build_old_ids.py --check    fail if the file is stale
"""
import argparse
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "assets/catalogue/old-ids.json"


def slugify(text: str) -> str:  # the hub's own slugify (assets/catalogue/hub.js)
    return re.sub(r"^-+|-+$", "", re.sub(r"[^a-z0-9]+", "-", text.lower().replace("&", " and ")))


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def build() -> dict:
    record = json.loads((ROOT / "tools/catalogue/PUBLIC_NAMES_MAP.json").read_text("utf-8"))
    strings, slugs = record["strings"], record.get("subjectSlugs", {})
    rows = json.loads((ROOT / "resources.json").read_text("utf-8"))
    ids = {row["id"] for row in rows}
    subjects = {row["subject"] for row in rows}
    out_ids = {key: new for key, new in sorted(strings.items()) if new in ids}
    out_subjects = {key: new for key, new in sorted(strings.items()) if new in subjects and new not in ids}
    for key, new in sorted(slugs.items()):
        out_subjects[key] = new
    return {"schema": 1, "basis": "N3a: SHA-256 of each old id, subject value and subject card slug; no old wording is stored.", "ids": out_ids, "subjects": out_subjects}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    value = json.dumps(build(), ensure_ascii=False, indent=1) + "\n"
    if args.check:
        if not OUTPUT.exists() or OUTPUT.read_text("utf-8") != value:
            raise SystemExit("[FAIL] old-ids.json is stale; rebuild it")
        print("[PASS] old-ids.json equals its derivation")
    else:
        OUTPUT.write_text(value, "utf-8")
        built = json.loads(value)
        print(f"old-ids.json: {len(built['ids'])} ids, {len(built['subjects'])} subject values and slugs")
