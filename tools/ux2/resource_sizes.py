#!/usr/bin/env python3
"""UX2 A3.1 — the size table the subject page reads.

data/resource-sizes.json maps every catalogue path (and every companion-pack
file listed in data/companion-packs.json, when that manifest exists) to its
byte size in the working tree. A size is never typed: it is measured here and
re-measured by --check. The publisher is immutable and never edits source, so
this file is committed and kept in step by the UX2 gates workflow (see README,
"Resource sizes").

    python3 tools/ux2/resource_sizes.py --write    regenerate
    python3 tools/ux2/resource_sizes.py --check    committed == working tree (exit 1 on drift)
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CATALOGUE = ROOT / "resources.json"
PACKS = ROOT / "data/companion-packs.json"
OUTPUT = ROOT / "data/resource-sizes.json"


def paths() -> list[str]:
    wanted = []
    for row in json.loads(CATALOGUE.read_text("utf-8")):
        value = row.get("file") or row.get("url") or ""
        if value and "://" not in value:
            wanted.append(value.split("#")[0].split("?")[0])
        for item in row.get("files", []) or []:
            if item.get("path"):
                wanted.append(item["path"])
    if PACKS.is_file():
        for pack in json.loads(PACKS.read_text("utf-8")).get("packs", []):
            for item in pack.get("files", []):
                wanted.append(item["path"])
    return sorted(set(wanted))


def derive() -> dict:
    sizes = {}
    missing = []
    for rel in paths():
        target = ROOT / rel
        if target.is_file():
            sizes[rel] = target.stat().st_size
        else:
            missing.append(rel)
    return {"schema": "mbm-resource-sizes-v1", "unit": "bytes", "measured": len(sizes), "missing": missing, "sizes": sizes}


def serialise(value: dict) -> str:
    return json.dumps(value, ensure_ascii=False, indent=1) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    value = derive()
    text = serialise(value)
    if args.write:
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT.write_text(text, "utf-8")
        print(f"[DONE] wrote {OUTPUT.relative_to(ROOT)}: {value['measured']} sizes, {len(value['missing'])} missing")
    if args.check or not args.write:
        current = OUTPUT.read_text("utf-8") if OUTPUT.is_file() else ""
        if current != text:
            print(f"[FAIL] {OUTPUT.relative_to(ROOT)} differs from the working tree — run: python3 tools/ux2/resource_sizes.py --write")
            return 1
        print(f"[PASS] {OUTPUT.relative_to(ROOT)} matches the working tree: {value['measured']} sizes, {len(value['missing'])} missing")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
