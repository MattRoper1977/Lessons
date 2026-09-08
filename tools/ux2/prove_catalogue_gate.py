#!/usr/bin/env python3
"""UX2 A1 — prove the catalogue contract still bites after the additive-tag allowance.

The shared gate (tools/verify_cross_estate_unification.py, catalogue_errors) now
strips `halfTerm` and `unit` before digesting the 734 original rows. This tool
shows, on temporary copies of the repository's own catalogue, that the digest
still catches everything else. A green control needs a non-vacuity proof, so
every plant is asserted RED and the unplanted file is asserted GREEN.

    python3 tools/ux2/prove_catalogue_gate.py
"""
from __future__ import annotations

import copy
import importlib.util
import json
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GATE = ROOT / "tools/verify_cross_estate_unification.py"


def gate_module():
    spec = importlib.util.spec_from_file_location("catalogue_gate", GATE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def catalogue_errors_on(gate, rows: list[dict]) -> list[str]:
    with tempfile.TemporaryDirectory(prefix="ux2-catalogue-gate-") as temp:
        root = Path(temp)
        (root / "resources.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", "utf-8")
        text = (ROOT / "index.html").read_text("utf-8")
        for rel in gate.CATALOGUE_PINS.get("files", {}):
            source = ROOT / rel
            if source.is_file():
                (root / rel).parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(source, root / rel)
        return [e for e in gate.catalogue_errors(root, "lessons", text) if "row" in e or "catalogue" in e.lower()]


def main() -> int:
    gate = gate_module()
    rows = json.loads((ROOT / "resources.json").read_text("utf-8"))
    original = gate.CATALOGUE_ORIGINAL_ROWS
    controls = []

    def row_errors(value):
        return [e for e in catalogue_errors_on(gate, value) if "original catalogue row" in e or "hub rows" in e or "requires the original" in e or "carried" in e]

    controls.append(("unplanted catalogue is green", not row_errors(rows)))
    first = next(i for i, r in enumerate(rows[:original]) if r.get("type") in {"lesson", "Lesson"})
    a = copy.deepcopy(rows); a[first]["title"] += " (planted)"
    controls.append(("edited title on an original row is red", bool(row_errors(a))))
    b = copy.deepcopy(rows); b[first]["plantedKey"] = "x"
    controls.append(("unknown key on an original row is red", bool(row_errors(b))))
    c = copy.deepcopy(rows); del c[first]
    controls.append(("removed original row is red", bool(row_errors(c))))
    d = copy.deepcopy(rows); d[first], d[first + 1] = d[first + 1], d[first]
    controls.append(("reordered original rows are red", bool(row_errors(d))))
    e = copy.deepcopy(rows); e[first]["halfTerm"] = "Autumn 1"; e[first]["unit"] = "Planted unit"
    controls.append(("halfTerm + unit appended to an original row is green", not row_errors(e)))
    f = copy.deepcopy(rows); f[first]["halfTerm"] = "Autumn 1"; f[first]["desc"] = "planted"
    controls.append(("tag plus an edited value is still red", bool(row_errors(f))))
    g = copy.deepcopy(rows); g[original + 1]["title"] = "planted"
    controls.append(("edited shelf row is red", bool(row_errors(g))))
    for name, ok in controls:
        print(f"  {'PASS' if ok else 'FAIL'}  {name}")
    if not all(ok for _, ok in controls):
        print("[FAIL] catalogue gate proof")
        return 1
    print(f"[PASS] catalogue gate proof: {len(controls)} controls")
    return 0


if __name__ == "__main__":
    sys.exit(main())
