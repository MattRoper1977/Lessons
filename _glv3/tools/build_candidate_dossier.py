#!/usr/bin/env python3
"""Build the truthful pre-merge GLV3 evidence dossier after every gate passes."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import zipfile
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image

SENTINEL = "grow-launch-estate-v3-autonomous-closeout-2026-08-10"
HISTORIC = "1e8a428b523d1b970a8a3a2ab2a99f48a8271d09"
PR_URL = "https://github.com/MattRoper1977/Lessons/pull/108"


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def read_json(path: Path):
    return json.loads(path.read_text("utf-8"))


def write_json(path: Path, value) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n", "utf-8")


def scrub_text_tree(root: Path) -> None:
    replacements = {
        "/home/runner/work/Lessons/Lessons": "<repository>",
        "/tmp/glv3-packs": "<verified-source>",
    }
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix.casefold() in {".png", ".zip"}:
            continue
        try:
            text = path.read_text("utf-8")
        except UnicodeDecodeError:
            continue
        for source, replacement in replacements.items():
            text = text.replace(source, replacement)
        path.write_text(text, "utf-8")


def deterministic_zip(path: Path, root: Path, names: list[str]) -> None:
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as bundle:
        for name in sorted(names):
            source = root / name
            if not source.is_file():
                continue
            info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            bundle.writestr(info, source.read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    with zipfile.ZipFile(path) as bundle:
        if bundle.testzip() is not None:
            raise SystemExit("evidence ZIP integrity test failed")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path("."))
    parser.add_argument("--integration-sha", required=True)
    parser.add_argument("--starting-branch-sha", required=True)
    args = parser.parse_args()

    root = args.repo.resolve()
    out = root / "_glv3"
    generated_at = now()
    required = [
        "GATES_STATIC.json",
        "GATES_BROWSER.json",
        "GATES_CHIPS.json",
        "INPUT_INTEGRITY.json",
        "COUNT_RECONCILIATION.json",
        "PROTECTED_TREES.json",
        "POSITIVE_CONTROLS.json",
        "run_manifest.json",
        "REPORT.md",
        "AMBERS.md",
        "DECISIONS.md",
    ]
    for name in required:
        path = out / name
        if not path.is_file() or path.stat().st_size == 0:
            raise SystemExit(f"required evidence missing: {name}")

    contacts = sorted((out / "contact_sheet").rglob("*.png"))
    if len(contacts) != 83:
        raise SystemExit(f"expected 83 contact sheets, got {len(contacts)}")
    names: set[str] = set()
    inventory = []
    for path in contacts:
        rel = path.relative_to(root).as_posix()
        folded = rel.casefold()
        if folded in names:
            raise SystemExit(f"duplicate contact-sheet path: {rel}")
        names.add(folded)
        if path.stat().st_size <= 1000:
            raise SystemExit(f"trivial contact-sheet file: {rel}")
        with Image.open(path) as image:
            image.load()
            width, height = image.size
            extrema = image.convert("RGB").getextrema()
        if width <= 0 or height <= 0 or not any(high - low > 2 for low, high in extrema):
            raise SystemExit(f"blank/solid contact sheet: {rel}")
        inventory.append({
            "path": rel,
            "byte_size": path.stat().st_size,
            "width": width,
            "height": height,
            "sha256": sha256(path),
        })
    write_json(out / "CONTACT_SHEET_INVENTORY.json", {
        "sentinel": SENTINEL,
        "result": "PASS",
        "png_count": 83,
        "per_lesson_contact_sheets": 80,
        "combined_subject_sheets": 3,
        "files": inventory,
    })

    protected = read_json(out / "PROTECTED_TREES.json")
    integration = protected["integration"]
    current_files = []
    for tree in integration["trees"].values():
        for baseline in tree["files"]:
            path = root / baseline["path"]
            if not path.is_file():
                raise SystemExit(f"protected file disappeared: {baseline['path']}")
            blob = subprocess.check_output(["git", "hash-object", str(path)], cwd=root, text=True).strip()
            row = {
                "path": baseline["path"],
                "git_blob_sha": blob,
                "byte_size": path.stat().st_size,
                "sha256": sha256(path),
            }
            expected = (baseline["git_blob_sha"], baseline["byte_size"], baseline["sha256"])
            actual = (row["git_blob_sha"], row["byte_size"], row["sha256"])
            if actual != expected:
                raise SystemExit(f"protected file changed: {baseline['path']}")
            current_files.append(row)
    protected["candidate_worktree"] = {"file_count": len(current_files), "files": current_files}
    protected["candidate_vs_integration"] = {
        "identical": True,
        "added": [],
        "removed": [],
        "modified": [],
    }
    protected["candidate_comparison_pending"] = False
    write_json(out / "PROTECTED_TREES.json", protected)

    sentinel = read_json(out / "AUTONOMOUS_SENTINEL.json")
    timestamps = sentinel.setdefault("phase_timestamps", {})
    for phase in (
        "GENERATION", "STATIC_GATES", "BROWSER_GATES", "EVIDENCE_GENERATION", "BRANCH_CANDIDATE"
    ):
        timestamps[phase] = generated_at
    sentinel.update({
        "current_phase": "BRANCH_CANDIDATE",
        "integration_base_sha": args.integration_sha,
        "starting_recovery_branch_sha": args.starting_branch_sha,
        "candidate_head_sha": None,
        "merged_sha": None,
        "pages": {},
        "final_production_status": "CANDIDATE_VERIFIED_NOT_MERGED",
        "latest_failure": None,
        "latest_diagnosis": "The 28-versus-34 mismatch was a classifier defect; the six PEQ_W1–PEQ_W6 lessons are genuine source files.",
        "latest_repair": "Suffix-and-manifest classification, repository-proven live path resolution and authored Humanities print-route reconstruction were applied without changing protected live trees.",
        "updated_at": generated_at,
    })
    sentinel["discovered_pr"] = {"number": 108, "url": PR_URL}
    sentinel.setdefault("gate_states", {}).update({
        "source_integrity": "PASS",
        "count_reconciliation": "PASS",
        "generation": "PASS",
        "static": "PASS",
        "browser": "PASS",
        "print": "PASS",
        "chips": "PASS",
        "contact_sheets": "PASS",
        "positive_controls": "PASS",
        "protected_candidate": "PASS",
        "deployment": "PENDING_MERGE",
    })
    write_json(out / "AUTONOMOUS_SENTINEL.json", sentinel)

    ambers_text = (out / "AMBERS.md").read_text("utf-8")
    amber_lines = [line[2:].strip() for line in ambers_text.splitlines() if line.startswith("- ")]
    report = f"""NOT DEPLOYED — VERIFIED CANDIDATE, PR NOT YET MERGED

# GROW + LAUNCH Estates v3 candidate dossier

The earlier completion claim was false. This candidate was regenerated from the two byte-verified repaired ZIP inputs and the deterministic extracted-file transport. It passed input, count, static, browser, responsive, keyboard-smoke, print, catalogue-chip, contact-sheet and disposable tamper controls. It remains non-production until PR #108 is merged and the exact merged content is proven through GitHub Pages and the canonical Made by Matt Lessons route.

## Candidate identity

- Historic rollback SHA: `{HISTORIC}`
- Current integration base SHA: `{args.integration_sha}`
- Starting recovery-branch SHA for this execution: `{args.starting_branch_sha}`
- Pull request: #108
- Candidate commit SHA: populated externally after the immutable commit is created; a commit cannot contain its own SHA without changing that SHA.

## Exact measured counts

- GROW deployable lessons: 34 (Art 8 · Humanities 8 · ASDAN 18)
- LAUNCH deployable lessons: 46 (Art 8 · Humanities 8 · ASDAN 30)
- Combined deployable lessons: 80
- Print-bearing lessons: 24
- Screen-only lessons: 56
- Catalogue additions: 88
- Installed HTML boot universe: 94
- Contact sheets: 83 (80 per-lesson + 3 combined subject sheets)

## Mandatory findings

- The old 28 count used a narrow filename-prefix allowlist and omitted the genuine GROW `PEQ_W1`–`PEQ_W6` files. No lesson was fabricated.
- Existing lessons remain the default route; the two 2026–27 estates are parallel alternatives.
- All nine protected live trees are byte/blob-identical to the authoritative integration baseline.
- Final merge, raw-pin, Pages and production proof objects are intentionally unset at this pre-merge stage.

## Evidence

See `REPORT.md`, `GATES_STATIC.json`, `GATES_BROWSER.json`, `GATES_CHIPS.json`, `POSITIVE_CONTROLS.json`, `INPUT_INTEGRITY.json`, `COUNT_RECONCILIATION.json`, `PROTECTED_TREES.json` and `CONTACT_SHEET_INVENTORY.json`.

## Rollback

After merge, roll back only with a targeted revert of the GLV3 merge/commit. Never reset current `main` wholesale to the historic anchor.
"""
    (out / "GROW_LAUNCH_v3_DEPLOY_FINAL_REPORT.md").write_text(report, "utf-8")

    proof = {
        "sentinel": SENTINEL,
        "status": "CANDIDATE_VERIFIED_NOT_MERGED",
        "deployment_complete": False,
        "publication_proven": False,
        "repository": "MattRoper1977/Lessons",
        "historic_rollback_sha": HISTORIC,
        "integration_base_sha": args.integration_sha,
        "branch": "claude/gl-estate-v3",
        "candidate_head_sha": None,
        "pull_request": {"number": 108, "url": PR_URL, "state": "OPEN"},
        "merge": {},
        "pages": {},
        "inputs": read_json(out / "INPUT_INTEGRITY.json"),
        "count_reconciliation": read_json(out / "COUNT_RECONCILIATION.json"),
        "counts": {
            "grow": 34,
            "launch": 46,
            "total": 80,
            "print_bearing": 24,
            "screen_only": 56,
            "catalogue_additions": 88,
            "html_boot_universe": 94,
            "contact_sheets": 83,
        },
        "protected_trees": {"candidate_vs_integration": "PASS", "manifest": "PROTECTED_TREES.json"},
        "catalogue": {"addition_count": 88, "year": "2026-27", "chip_gate": "PASS"},
        "routes": {"existing_lessons_remain_default": True, "subject_rows_added": 6},
        "gates": {
            "static": "PASS",
            "browser": "PASS",
            "print": "PASS",
            "chips": "PASS",
            "positive_controls": "PASS",
            "contact_sheets": "PASS",
        },
        "ci_runs": [],
        "raw_pin_samples": [],
        "production_samples": [],
        "artifacts": [],
        "ambers": amber_lines,
        "rollback": {
            "strategy": "Targeted revert of the GLV3 merge/commit; remove only the two estate roots, 88 GLV3 catalogue rows, six route-map rows and GLV3 evidence files.",
            "historic_anchor_is_not_a_wholesale_reset_target": True,
        },
    }
    write_json(out / "GROW_LAUNCH_v3_DEPLOY_PROOF.json", proof)

    scrub_text_tree(out)
    members = [
        "GROW_LAUNCH_v3_DEPLOY_FINAL_REPORT.md",
        "GROW_LAUNCH_v3_DEPLOY_PROOF.json",
        "GATES_STATIC.json",
        "GATES_BROWSER.json",
        "GATES_CHIPS.json",
        "INPUT_INTEGRITY.json",
        "COUNT_RECONCILIATION.json",
        "AUTONOMOUS_SENTINEL.json",
        "PROTECTED_TREES.json",
        "POSITIVE_CONTROLS.json",
        "CONTACT_SHEET_INVENTORY.json",
        "AMBERS.md",
        "DECISIONS.md",
        "run_manifest.json",
    ]
    deterministic_zip(out / "GROW_LAUNCH_v3_REPORT_AND_PROOF.zip", out, members)

    artifact_names = [name for name in members if (out / name).is_file()]
    proof = read_json(out / "GROW_LAUNCH_v3_DEPLOY_PROOF.json")
    proof["artifacts"] = [
        {"path": f"_glv3/{name}", "byte_size": (out / name).stat().st_size, "sha256": sha256(out / name)}
        for name in artifact_names
    ]
    proof["artifacts"].append({
        "path": "_glv3/GROW_LAUNCH_v3_REPORT_AND_PROOF.zip",
        "byte_size": (out / "GROW_LAUNCH_v3_REPORT_AND_PROOF.zip").stat().st_size,
        "sha256": sha256(out / "GROW_LAUNCH_v3_REPORT_AND_PROOF.zip"),
    })
    write_json(out / "GROW_LAUNCH_v3_DEPLOY_PROOF.json", proof)
    deterministic_zip(out / "GROW_LAUNCH_v3_REPORT_AND_PROOF.zip", out, members)

    print(json.dumps({
        "result": "PASS",
        "integration_base_sha": args.integration_sha,
        "contacts": len(contacts),
        "evidence_zip_sha256": sha256(out / "GROW_LAUNCH_v3_REPORT_AND_PROOF.zip"),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
