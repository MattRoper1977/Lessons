#!/usr/bin/env python3
"""UX2 A1 — enforce resources.schema.json on resources.json (schema first).

The schema existed but nothing ran it (A0 §3: zero references in any workflow
or tool, and 105 rows already outside it). This is the enforcement step. It is
dependency-free on purpose — CI runners here carry no jsonschema — and covers
exactly the subset the catalogue schema uses: type, enum, pattern, minLength,
required, additionalProperties, items, uniqueItems, properties.

    python3 tools/ux2/check_catalogue_schema.py             validate, exit 1 on any error
    python3 tools/ux2/check_catalogue_schema.py --self-test  plant a novel halfTerm, an
                                                              unknown key, a bad role and a
                                                              novel kind; each must go red
"""
from __future__ import annotations

import argparse
import copy
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCHEMA = ROOT / "resources.schema.json"
CATALOGUE = ROOT / "resources.json"


def validate(value, schema, where="$") -> list[str]:
    errors: list[str] = []
    kind = schema.get("type")
    if "enum" in schema and value not in schema["enum"]:
        return [f"{where}: {value!r} is not one of {schema['enum']}"]
    if kind == "array":
        if not isinstance(value, list):
            return [f"{where}: expected array"]
        if schema.get("uniqueItems") and len({json.dumps(v, sort_keys=True) for v in value}) != len(value):
            errors.append(f"{where}: items are not unique")
        for index, item in enumerate(value):
            errors += validate(item, schema.get("items", {}), f"{where}[{index}]")
        return errors
    if kind == "object":
        if not isinstance(value, dict):
            return [f"{where}: expected object"]
        properties = schema.get("properties", {})
        for key in schema.get("required", []):
            if key not in value:
                errors.append(f"{where}: missing required {key}")
        for key, item in value.items():
            if key in properties:
                errors += validate(item, properties[key], f"{where}.{key}")
            elif schema.get("additionalProperties") is False:
                errors.append(f"{where}: unknown key {key}")
        return errors
    if kind == "string":
        if not isinstance(value, str):
            return [f"{where}: expected string"]
        if "minLength" in schema and len(value) < schema["minLength"]:
            errors.append(f"{where}: shorter than {schema['minLength']}")
        if "pattern" in schema and not re.search(schema["pattern"], value):
            errors.append(f"{where}: {value!r} does not match {schema['pattern']}")
        return errors
    if kind == "boolean":
        return [] if isinstance(value, bool) else [f"{where}: expected boolean"]
    if kind == "integer":
        return [] if isinstance(value, int) and not isinstance(value, bool) else [f"{where}: expected integer"]
    return errors


def run(rows, schema) -> list[str]:
    return validate(rows, schema)


def self_test(schema, rows) -> None:
    baseline = run(rows, schema)
    if baseline:
        raise SystemExit("[FAIL] self-test needs a clean catalogue first:\n  " + "\n  ".join(baseline[:5]))
    plants = []
    first = next(i for i, r in enumerate(rows) if r.get("type") in {"lesson", "Lesson"})
    a = copy.deepcopy(rows); a[first]["halfTerm"] = "Autumn 9"; plants.append(("novel halfTerm label", a))
    b = copy.deepcopy(rows); b[first]["unexpectedKey"] = 1; plants.append(("unknown key on a row", b))
    c = copy.deepcopy(rows); c[first]["unit"] = ""; plants.append(("empty unit string", c))
    d = copy.deepcopy(rows); d[first]["kind"] = "bundle"; plants.append(("novel kind", d))
    e = copy.deepcopy(rows); e[first]["files"] = [{"role": "answers", "type": "pdf", "path": "x.pdf"}]; plants.append(("bad file role", e))
    f = copy.deepcopy(rows); f[first]["files"] = [{"role": "teacher", "type": "xlsx", "path": "x.xlsx"}]; plants.append(("bad file type", f))
    g = copy.deepcopy(rows); g[first]["builtFrom"] = "not-a-digest"; plants.append(("malformed builtFrom", g))
    h = copy.deepcopy(rows); del h[first]["title"]; plants.append(("missing required title", h))
    ok = True
    for name, planted in plants:
        red = bool(run(planted, schema))
        print(f"  {'PASS' if red else 'FAIL'}  {name} is rejected")
        ok &= red
    if not ok:
        raise SystemExit("[FAIL] schema self-test: a planted defect passed")
    print("[PASS] catalogue schema self-test: 8/8 plants red, real catalogue green")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--catalogue", type=Path, default=CATALOGUE)
    args = parser.parse_args()
    schema = json.loads(SCHEMA.read_text("utf-8"))
    rows = json.loads(args.catalogue.read_text("utf-8"))
    if args.self_test:
        self_test(schema, rows)
        return 0
    errors = run(rows, schema)
    if errors:
        print(f"[FAIL] {len(errors)} schema error(s) in {args.catalogue.name}:")
        for line in errors[:40]:
            print("  " + line)
        return 1
    print(f"[PASS] {args.catalogue.name}: {len(rows)} rows valid against {SCHEMA.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
