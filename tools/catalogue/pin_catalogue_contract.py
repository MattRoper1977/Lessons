#!/usr/bin/env python3
"""Pin the explicitly reviewed education catalogue in both estate gate copies.

This is a deliberate review operation, never a CI repair. The row-preservation
check is independent of the moved digest: re-pinning cannot hide a removed,
reordered or rewritten original resource. Run builders and QA before this tool.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import re

GATE = "tools/verify_cross_estate_unification.py"
ORIGINAL_ROW_COUNT = 734
ORIGINAL_ROWS_SHA256 = "b8ffcb16f5fd2a413e8a0b06ad2d4b112f450364fa294377869dc32c8235bb2c"
SHELF_ROWS = [
    {
        "subject": "Science · Teesside", "title": "Science · browse by pathway, term and teaching version",
        "file": "Science_Teesside/index.html", "id": "science-pathway-term-hub", "type": "hub", "family": "Science Teesside",
        "keywords": ["science", "build", "grow", "launch", "pathway", "term", "lesson hub"],
        "desc": "Choose a Science pathway and term, then browse the recommended sequence and retained teaching versions.",
        "added": "2026-09-05", "new": True, "year": "2026-27"
    },
    {
        "subject": "Humanities · Teesside", "title": "Humanities · browse by pathway, term and teaching version",
        "file": "Humanities_Teesside/index.html", "id": "humanities-pathway-term-hub", "type": "hub", "family": "Humanities Teesside",
        "keywords": ["humanities", "religious education", "build", "grow", "launch", "pathway", "term", "lesson hub"],
        "desc": "Choose a Humanities pathway and term, then browse current lessons, retained teaching versions and classroom references.",
        "added": "2026-09-05", "new": True, "year": "2026-27"
    },
    {
        "subject": "Humanities · Teesside", "title": "David's Humanities and RE cover pack · Autumn 1 Weeks 3–7",
        "file": "Humanities_Teesside/David_Cover_Autumn1_W3-W7/index.html", "id": "david-humanities-re-cover-hub", "type": "hub", "family": "Humanities Teesside",
        "keywords": ["humanities", "religious education", "david", "cover", "build", "grow", "launch", "autumn 1", "weeks 3–7", "downloads"],
        "desc": "Twenty-five 40-minute cover periods with PowerPoint, Word and PDF downloads, linked to the existing Humanities and RE lessons.",
        "added": "2026-09-05", "new": True, "year": "2026-27"
    }
]

# Exact reviewed files, not patterns. A future new UI file requires an explicit
# change here; a lesson cannot become permitted because it shares a directory.
# The verifier and pin tool exclude themselves to avoid a recursive file hash.
REVIEWED_PATHS = (
    "index.html", "Science_Teesside/index.html", "Humanities_Teesside/index.html", "humanities_teesside.html",
    "Humanities_Teesside/David_Cover_Autumn1_W3-W7/index.html",
    "assets/catalogue/catalogue.css", "assets/catalogue/catalogue.js",
    "assets/catalogue/lesson-navigation.js",
    "assets/catalogue/science-shelf.css", "assets/catalogue/science-shelf.js",
    "assets/catalogue/terms-and-styles.json", "assets/catalogue/science-shelf.json", "assets/catalogue/humanities-shelf.json",
    "tools/catalogue/build_catalogue.py", "tools/catalogue/build_science_shelf.py", "tools/catalogue/build_humanities_shelf.py",
    "tools/catalogue/check_catalogue_static.py", "tools/catalogue/check_catalogue_dom.cjs", "tools/catalogue/verify_education_navigation.cjs",
    "tools/catalogue/SHELF_SELECTION.json", "tools/catalogue/HUMANITIES_SELECTION.json",
    "tools/easter/science_original_browser.cjs",
    "tools/prepare_served_publications.py", "tools/test_served_publications.py",
    "tools/catalogue/TERM_AND_STYLE_EVIDENCE.json", "tools/catalogue/TERM_REVIEW.json",
)


def row_digest(rows: list) -> str:
    return hashlib.sha256(json.dumps(rows, ensure_ascii=False, separators=(",", ":")).encode("utf-8")).hexdigest()


def preserved_rows_errors(rows: list) -> list[str]:
    errors = []
    if len(rows) != ORIGINAL_ROW_COUNT + len(SHELF_ROWS):
        errors.append("catalogue must contain the original 734 rows plus exactly three reviewed hub rows")
    if row_digest(rows[:ORIGINAL_ROW_COUNT]) != ORIGINAL_ROWS_SHA256:
        errors.append("an original catalogue row was removed, reordered or edited")
    if rows[ORIGINAL_ROW_COUNT:] != SHELF_ROWS:
        errors.append("the appended hub rows differ from the three reviewed navigation entries")
    return errors


def module(path: Path):
    spec = importlib.util.spec_from_file_location("catalogue_gate", path)
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


def pin(lessons: Path, apps: Path, *, check: bool) -> dict:
    gates = [lessons / GATE, apps / GATE]
    originals = [p.read_text("utf-8") for p in gates]
    if originals[0] != originals[1]:
        raise ValueError("gate copies differ; reconcile their reviewed logic before pinning. Nothing written")
    rows = json.loads((lessons / "resources.json").read_text("utf-8"))
    errors = preserved_rows_errors(rows)
    if errors:
        raise ValueError("; ".join(errors))
    gate = module(gates[0])
    files = {path: hashlib.sha256((lessons / path).read_bytes()).hexdigest() for path in REVIEWED_PATHS}
    text = (lessons / "index.html").read_text("utf-8")
    pins = {"visible_body_sha256": hashlib.sha256(gate.normalized_visible_body(text, "lessons").encode("utf-8")).hexdigest(), "files": files}
    replacement = "# BEGIN REVIEWED CATALOGUE PINS\nCATALOGUE_PINS = " + json.dumps(pins, indent=4) + "\n# END REVIEWED CATALOGUE PINS"
    patched, count = re.subn(r"# BEGIN REVIEWED CATALOGUE PINS\n.*?# END REVIEWED CATALOGUE PINS", lambda _: replacement, originals[0], flags=re.S)
    if count != 1:
        raise ValueError("expected exactly one reviewed catalogue pin block")
    for name, owner in (("resources.json", lessons), ("apps.json", apps)):
        digest = hashlib.sha256((owner / name).read_bytes()).hexdigest()
        pattern = re.compile(r'("' + re.escape(name) + r'":\s*")([0-9a-f]{64})(")')
        patched, count = pattern.subn(lambda m: m[1] + digest + m[3], patched)
        if count != 1:
            raise ValueError("expected exactly one manifest pin: " + name)
    changed = patched != originals[0]
    if check and changed:
        raise ValueError("reviewed catalogue or manifest pins differ; review and re-pin both copies")
    if not check and changed:
        # Prepare the complete, identical replacement before the first write.
        # Restore both originals if an OS write fails during the local operation.
        try:
            for path in gates:
                path.write_text(patched, "utf-8")
        except OSError:
            for path, original in zip(gates, originals):
                path.write_text(original, "utf-8")
            raise
    return {"status": "PASS", "mode": "check" if check else "pin", "reviewedFiles": len(files), "originalRowsPreserved": ORIGINAL_ROW_COUNT, "appendedShelfRows": len(SHELF_ROWS), "gateSha256": hashlib.sha256(patched.encode()).hexdigest()}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lessons", type=Path, required=True)
    parser.add_argument("--apps", type=Path, required=True)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        print(json.dumps(pin(args.lessons.resolve(), args.apps.resolve(), check=args.check), indent=2))
        return 0
    except (ValueError, OSError) as exc:
        print("[FAIL] " + str(exc))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
