#!/usr/bin/env python3
"""N3a: apply the reviewed plain-words map to the catalogue's public strings.

The map (tools/catalogue/PUBLIC_NAMES_MAP.json) holds no old wording. Each
entry is the SHA-256 of one exact old string (an id, a title or a subject
value) and the plain string that replaces it. This step walks the listed
files, hashes every string it meets (JSON keys and values, Python string
literals) and swaps the ones the map names. Nothing else is touched: row
order, row count, file paths and every other field stay as they are.

    python3 tools/catalogue/apply_public_names.py --write   apply (idempotent)
    python3 tools/catalogue/apply_public_names.py --check   fail if anything is still to apply,
                                                            or a new string is itself a map key
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import tokenize
import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MAP = ROOT / "tools/catalogue/PUBLIC_NAMES_MAP.json"
JSON_FILES = (
    "resources.json",
    "data/companion-packs.json",
    "assets/catalogue/pack-notes.json",
    "tools/catalogue/TERM_AND_STYLE_EVIDENCE.json",
    "tools/ux2/lesson-outcome-baseline.json",
)
PYTHON_FILES = ("tools/catalogue/pin_catalogue_contract.py",)


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def load_map() -> dict:
    strings = json.loads(MAP.read_text("utf-8"))["strings"]
    loops = sorted(new for new in strings.values() if digest(new) in strings)
    if loops:
        raise ValueError("a replacement is itself a map key (not idempotent): " + ", ".join(loops[:5]))
    return strings


def swap(value, strings: dict, count: list):
    if isinstance(value, str):
        new = strings.get(digest(value))
        if new is None:
            return value
        count[0] += 1
        return new
    if isinstance(value, list):
        return [swap(item, strings, count) for item in value]
    if isinstance(value, dict):
        return {swap(key, strings, count): swap(item, strings, count) for key, item in value.items()}
    return value


def json_dump_like(original: str, data) -> str:
    """Re-serialise in the file's own style, so only the swapped strings differ."""
    for kwargs in (
        {"indent": 2, "ensure_ascii": False},
        {"indent": 2, "ensure_ascii": True},
        {"indent": 1, "ensure_ascii": False},
        {"indent": 4, "ensure_ascii": False},
        {"separators": (",", ":"), "ensure_ascii": False},
        {"ensure_ascii": False},
        {"ensure_ascii": True},
        {"indent": 2, "ensure_ascii": False, "sort_keys": True},
    ):
        for tail in ("\n", ""):
            if json.dumps(json.loads(original), **kwargs) + tail == original:
                return json.dumps(data, **kwargs) + tail
    raise ValueError("unrecognised JSON layout; refusing to rewrite")


def apply_json(path: Path, strings: dict) -> tuple[str, int]:
    original = path.read_text("utf-8")
    count = [0]
    data = swap(json.loads(original), strings, count)
    return (json_dump_like(original, data) if count[0] else original), count[0]


def apply_python(path: Path, strings: dict) -> tuple[str, int]:
    original = path.read_text("utf-8")
    lines = original.splitlines(keepends=True)
    edits = []
    for token in tokenize.generate_tokens(io.StringIO(original).readline):
        if token.type != tokenize.STRING or token.start[0] != token.end[0]:
            continue
        try:
            value = ast.literal_eval(token.string)
        except (ValueError, SyntaxError):
            continue
        if not isinstance(value, str):
            continue
        new = strings.get(digest(value))
        if new is not None:
            edits.append((token.start[0] - 1, token.start[1], token.end[1], repr(new)))
    for row, start, end, text in sorted(edits, reverse=True):
        lines[row] = lines[row][:start] + text + lines[row][end:]
    return "".join(lines), len(edits)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--write", action="store_true")
    group.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        strings = load_map()
        pending = {}
        for name in JSON_FILES:
            text, count = apply_json(ROOT / name, strings)
            if count:
                pending[name] = (text, count)
        for name in PYTHON_FILES:
            text, count = apply_python(ROOT / name, strings)
            if count:
                pending[name] = (text, count)
    except (ValueError, OSError) as error:
        print("[FAIL] " + str(error))
        return 1
    if args.check:
        if pending:
            print("[FAIL] old strings still present: " + ", ".join(f"{k} ({v[1]})" for k, v in pending.items()))
            return 1
        print(f"[PASS] public names map applied: {len(strings)} entries, nothing left to apply")
        return 0
    for name, (text, count) in pending.items():
        (ROOT / name).write_text(text, "utf-8")
        print(f"applied {count:4d} in {name}")
    print(f"[DONE] {sum(v[1] for v in pending.values())} strings swapped in {len(pending)} files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
