#!/usr/bin/env python3
"""Exercise the catalogue release's preservation and containment boundaries.

All sabotage happens in disposable fixtures. No checkout or manifest is edited.
The git control executes the real git boundary against committed test changes.
"""
from __future__ import annotations

import argparse
import copy
import importlib.util
import json
import re
from pathlib import Path
import shutil
import subprocess
import tempfile

from pin_catalogue_contract import GATE, ORIGINAL_ROW_COUNT, SHELF_ROWS, pin, preserved_rows_errors


def load(path):
    spec = importlib.util.spec_from_file_location("reviewed_gate", path)
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


def run(lessons: Path, apps: Path, canonical: Path) -> list[dict]:
    gate = load(lessons / GATE)
    results = []

    def check(name, ok):
        if not ok:
            raise AssertionError(name)
        results.append({"name": name, "status": "PASS"})

    rows = json.loads((lessons / "resources.json").read_text())
    check("Reviewed 734 original rows plus three real hubs are accepted", not preserved_rows_errors(rows))
    for index, hub in enumerate(SHELF_ROWS):
        bad = copy.deepcopy(rows); del bad[ORIGINAL_ROW_COUNT + index]
        check("Missing catalogue hub row is rejected: " + hub["id"], bool(preserved_rows_errors(bad)))
    bad = copy.deepcopy(rows); bad[0]["title"] += " silently changed"
    check("An original row rewrite is rejected", bool(preserved_rows_errors(bad)))
    bad = copy.deepcopy(rows); del bad[0]
    check("An original row deletion is rejected", bool(preserved_rows_errors(bad)))
    bad = copy.deepcopy(rows); bad[0], bad[1] = bad[1], bad[0]
    check("Reordering retained rows is rejected", bool(preserved_rows_errors(bad)))
    bad = copy.deepcopy(rows); bad.append(copy.deepcopy(rows[-1]))
    check("A duplicate appended hub is rejected", bool(preserved_rows_errors(bad)))
    bad = copy.deepcopy(rows); bad[ORIGINAL_ROW_COUNT]["file"] = "unexpected.html"
    check("A misdirected new shelf row is rejected", bool(preserved_rows_errors(bad)))
    bad = copy.deepcopy(rows); bad[ORIGINAL_ROW_COUNT]["type"] = "lesson"
    check("A navigation hub cannot count as an authored lesson", bool(preserved_rows_errors(bad)))

    with tempfile.TemporaryDirectory(prefix="catalogue-contract-controls-") as temp:
        base = Path(temp); lroot = base / "Lessons"; aroot = base / "Apps"
        for src, dst, kind in ((lessons, lroot, "lessons"), (apps, aroot, "apps")):
            paths = {"index.html", "resources.json" if kind == "lessons" else "apps.json", GATE, "tools/pin_manifests.py", gate.PUBLICATION_CALLER_PATH, gate.PUBLICATION_GATE_WORKFLOW_PATH, *gate.CANONICAL_HASHES}
            if kind == "lessons": paths.update(gate.CATALOGUE_PINS["files"])
            for rel in paths:
                output = dst / rel; output.parent.mkdir(parents=True, exist_ok=True); shutil.copy2(src / rel, output)
        check("Unmodified Lessons fixture passes the complete cross-estate gate", not gate.run_checks(lroot, kind="lessons", canonical=canonical))
        apps_html = (aroot / "index.html").read_text()
        check("Unmodified Apps fixture retains its complete cross-estate checks", not gate.run_checks(aroot, kind="apps", canonical=canonical, base_html=apps_html))

        def mutate(rel, transform, expected, *, root=lroot, kind="lessons", base_html=None):
            path = root / rel; original = path.read_bytes()
            try:
                changed = transform(original); check(expected + " sabotage is non-vacuous", changed != original); path.write_bytes(changed)
                errors = gate.run_checks(root, kind=kind, canonical=canonical, base_html=base_html)
                check(expected, bool(errors))
            finally: path.write_bytes(original)

        mutate("index.html", lambda b: b.replace(b"</main>", b"<p>Unreviewed teaching advice</p></main>", 1), "Unreviewed visible hub wording is rejected")
        mutate("assets/catalogue/catalogue.css", lambda b: b + b"\n.card{display:none!important}\n", "Unreviewed catalogue styling is rejected")
        mutate("assets/catalogue/catalogue.js", lambda b: b + b"\nlocation.href='/games/';\n", "Unreviewed catalogue routing is rejected")
        mutate("assets/mbm-platform.js", lambda b: b + b"\n/* drift */\n", "Canonical shared asset drift remains rejected")
        mutate("resources.json", lambda b: b + b"\n", "Unpinned manifest byte drift remains rejected")
        mutate("index.html", lambda b: b.replace(b"</main>", b"<p>Unreviewed copy</p></main>", 1), "Apps authored wording protection remains active", root=aroot, kind="apps", base_html=apps_html)
        for hub in SHELF_ROWS:
            path = lroot / hub["file"]; original = path.read_bytes(); path.unlink()
            try: check("A missing reviewed hub file is rejected: " + hub["id"], bool(gate.run_checks(lroot, kind="lessons", canonical=canonical)))
            finally: path.write_bytes(original)

        for owner, kind in ((lroot, "lessons"), (aroot, "apps")):
            check(kind + " admits the exact reviewed caller through its named boundary", not gate.boundary_errors({gate.PUBLICATION_CALLER_PATH}, kind))
            caller_trigger = ("      - " + gate.PUBLICATION_CALLER_PATH + "\n").encode()
            mutate(gate.PUBLICATION_GATE_WORKFLOW_PATH, lambda b: b.replace(caller_trigger, b"", 1), kind + " rejects missing pull-request caller trigger", root=owner, kind=kind)
            mutate(gate.PUBLICATION_GATE_WORKFLOW_PATH, lambda b: b"".join(b.rsplit(caller_trigger, 1)), kind + " rejects missing push caller trigger", root=owner, kind=kind)
            mutate(gate.PUBLICATION_GATE_WORKFLOW_PATH, lambda b: b.replace(caller_trigger, b"      # " + caller_trigger.strip() + b"\n", 1), kind + " rejects a comment masquerading as a caller trigger", root=owner, kind=kind)
            mutate(gate.PUBLICATION_CALLER_PATH, lambda b: b.replace(b"contents: read", b"contents: write", 1), kind + " rejects broader publication permissions", root=owner, kind=kind)
            mutate(gate.PUBLICATION_CALLER_PATH, lambda b: b + b"\n  unreviewed-job:\n    runs-on: ubuntu-latest\n", kind + " rejects an extra publication job", root=owner, kind=kind)
            mutate(gate.PUBLICATION_CALLER_PATH, lambda b: re.sub(rb"builder_ref: [0-9a-f]{40}", b"builder_ref: main", b, count=1), kind + " rejects a floating or mismatched builder", root=owner, kind=kind)
            mutate(gate.PUBLICATION_CALLER_PATH, lambda b: re.sub(rb"education-publication.yml@[0-9a-f]{40}", b"education-publication.yml@main", b, count=1), kind + " rejects a floating reusable workflow", root=owner, kind=kind)
            caller_path = owner / gate.PUBLICATION_CALLER_PATH; original_caller = caller_path.read_bytes(); caller_path.unlink()
            try: check(kind + " rejects a missing education publisher", bool(gate.run_checks(owner, kind=kind, canonical=canonical)))
            finally: caller_path.write_bytes(original_caller)
            check(kind + " still rejects an unrelated modified workflow", bool(gate.boundary_errors({".github/workflows/unreviewed.yml"}, kind)))

        # Execute the real Git diff boundary; an independently edited lesson
        # cannot be smuggled through a green catalogue digest.
        def git(*args):
            return subprocess.check_output(["git", *args], cwd=lroot, text=True, stderr=subprocess.DEVNULL).strip()
        git("init", "-q"); git("config", "user.name", "Catalogue controls"); git("config", "user.email", "controls@example.invalid")
        payload = lroot / "retained-standalone-lesson.html"; payload.write_text("<h1>Retained lesson</h1>")
        git("add", "."); git("commit", "-qm", "Fixture baseline"); base_ref = git("rev-parse", "HEAD")
        payload.write_text("<h1>Unexpected lesson replacement</h1>"); git("add", "."); git("commit", "-qm", "Boundary sabotage")
        errors = gate.run_checks(lroot, kind="lessons", canonical=canonical, check_git=True, base_ref=base_ref)
        check("A committed standalone lesson modification fails the real Git boundary", any("retained-standalone-lesson.html" in e for e in errors))
        check("A game payload is outside both estate boundaries", bool(gate.boundary_errors({"Games/ApexKick/index.html"}, "lessons")) and bool(gate.boundary_errors({"Games/ApexKick/index.html"}, "apps")))
        check("A modified unlisted catalogue path is still outside the boundary", bool(gate.boundary_errors({"assets/catalogue/unreviewed.js"}, "lessons")))
        check("A catalogue file does not become allowed in Apps", bool(gate.boundary_errors({"humanities_teesside.html"}, "apps")))

        # Re-pinning cannot bless an edited original row, and failure writes
        # neither gate. Likewise divergent gate logic must be reconciled first.
        originals = [(lroot / GATE).read_bytes(), (aroot / GATE).read_bytes()]
        manifest = lroot / "resources.json"; manifest_bytes = manifest.read_bytes()
        changed = json.loads(manifest_bytes); changed[0]["title"] += " sabotage"; manifest.write_text(json.dumps(changed))
        try:
            rejected = False
            try: pin(lroot, aroot, check=False)
            except ValueError: rejected = True
            check("Re-pinning cannot bless changes to an original resource", rejected)
            check("Rejected row re-pin changes neither gate", originals == [(lroot / GATE).read_bytes(), (aroot / GATE).read_bytes()])
            generic = subprocess.run(["python3", str(lroot / "tools/pin_manifests.py"), "--lessons", str(lroot), "--apps", str(aroot)], text=True, capture_output=True)
            check("Generic manifest re-pin sabotage actually updates both matching gate copies", generic.returncode == 0 and (lroot / GATE).read_bytes() != originals[0] and (lroot / GATE).read_bytes() == (aroot / GATE).read_bytes())
            repinned_gate = load(lroot / GATE)
            errors = repinned_gate.run_checks(lroot, kind="lessons", canonical=canonical)
            check("Immutable row preservation still fails after a successful generic manifest re-pin", any("original catalogue row" in error for error in errors))
        finally:
            manifest.write_bytes(manifest_bytes)
            for path, original in zip((lroot / GATE, aroot / GATE), originals): path.write_bytes(original)
        (aroot / GATE).write_bytes(originals[1] + b"\n# divergence\n")
        divergent = [(lroot / GATE).read_bytes(), (aroot / GATE).read_bytes()]
        rejected = False
        try: pin(lroot, aroot, check=False)
        except ValueError: rejected = True
        check("Divergent gate logic prevents re-pinning before either write", rejected and divergent == [(lroot / GATE).read_bytes(), (aroot / GATE).read_bytes()])
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lessons", type=Path, required=True); parser.add_argument("--apps", type=Path, required=True); parser.add_argument("--canonical", type=Path, required=True)
    args = parser.parse_args(); results = run(args.lessons.resolve(), args.apps.resolve(), args.canonical.resolve())
    print(json.dumps({"status": "PASS", "controls": results, "total": len(results)}, indent=2))


if __name__ == "__main__": main()
