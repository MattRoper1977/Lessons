#!/usr/bin/env python3
"""Finalize the candidate proof and evidence ZIP without self-referential hashes."""
from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from pathlib import Path

MEMBERS = [
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


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def write_json(path: Path, value) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n", "utf-8")


def build_zip(path: Path, root: Path) -> None:
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as bundle:
        for name in sorted(MEMBERS):
            source = root / name
            if not source.is_file():
                raise SystemExit(f"evidence member missing: {name}")
            info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            bundle.writestr(info, source.read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path("."))
    args = parser.parse_args()
    root = args.repo.resolve() / "_glv3"
    proof_path = root / "GROW_LAUNCH_v3_DEPLOY_PROOF.json"
    zip_path = root / "GROW_LAUNCH_v3_REPORT_AND_PROOF.zip"
    integrity_path = root / "EVIDENCE_ZIP_INTEGRITY.json"

    proof = json.loads(proof_path.read_text("utf-8"))
    proof["artifacts"] = [
        {
            "path": f"_glv3/{name}",
            "byte_size": (root / name).stat().st_size,
            "sha256": sha256(root / name),
        }
        for name in MEMBERS
        if name != "GROW_LAUNCH_v3_DEPLOY_PROOF.json"
    ]
    proof["evidence_bundle"] = {
        "path": "_glv3/GROW_LAUNCH_v3_REPORT_AND_PROOF.zip",
        "integrity_manifest": "_glv3/EVIDENCE_ZIP_INTEGRITY.json",
        "self_referential_hash_omitted_from_embedded_proof": True,
    }
    write_json(proof_path, proof)

    build_zip(zip_path, root)
    with zipfile.ZipFile(zip_path) as bundle:
        corrupt = bundle.testzip()
        names = sorted(bundle.namelist())
        embedded_proof = bundle.read("GROW_LAUNCH_v3_DEPLOY_PROOF.json")
    if corrupt is not None:
        raise SystemExit(f"evidence ZIP integrity failure at {corrupt}")
    if names != sorted(MEMBERS):
        raise SystemExit("evidence ZIP member set mismatch")
    if embedded_proof != proof_path.read_bytes():
        raise SystemExit("embedded proof does not match repository proof")

    write_json(integrity_path, {
        "result": "PASS",
        "path": "_glv3/GROW_LAUNCH_v3_REPORT_AND_PROOF.zip",
        "byte_size": zip_path.stat().st_size,
        "sha256": sha256(zip_path),
        "member_count": len(MEMBERS),
        "members": sorted(MEMBERS),
        "zip_test": "PASS",
        "embedded_proof_matches_repository_proof": True,
        "note": "The ZIP hash is intentionally external to the ZIP and its embedded proof, avoiding an impossible self-referential digest.",
    })
    print(json.dumps({
        "result": "PASS",
        "zip_sha256": sha256(zip_path),
        "members": len(MEMBERS),
    }))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
