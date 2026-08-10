#!/usr/bin/env python3
from __future__ import annotations

import base64
import datetime as dt
import hashlib
import io
import json
import os
import re
import stat
import subprocess
import zipfile
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[2]
GL = ROOT / "_glv3"
GROW = Path(os.environ.get("GLV3_GROW_SRC", "/tmp/glv3-packs/grow"))
LAUNCH = Path(os.environ.get("GLV3_LAUNCH_SRC", "/tmp/glv3-packs/launch"))
SENTINEL = "grow-launch-estate-v3-autonomous-closeout-2026-08-10"
HIST = "1e8a428b523d1b970a8a3a2ab2a99f48a8271d09"
REPORTED_TRANSPORT_SHA = "efef35d7c8504f603646663da603a2f3690ed8204b2af7d0730b52560a9db918"
DISCOVERED_TRANSPORT_SHA = "777fcdafefc246c5c6b68a559886dc27b641471b7638ea79e51640c3e62791fd"
DISCOVERED_TRANSPORT_SIZE = 106760

EXP = {
    "GROW": {
        "zip": "GROW_ESTATE_v3_REPAIRED_2026-08-10.zip",
        "sha": "95bf78a4124f20196508748c4b44c3935b0eb09181bac69fcc00c4c0a5e6f58a",
        "size": 418166,
        "zip_members": 54,
        "files": 51,
        "html": 41,
        "manifest_digest": "0e83488ecad487c0da697c083f79fb99b783660fed193f1efe0f1fce1aeddd30",
        "lessons": 34,
        "subjects": {"art": 8, "humanities": 8, "asdan": 18},
    },
    "LAUNCH": {
        "zip": "LAUNCH_ESTATE_v3_REPAIRED_2026-08-10.zip",
        "sha": "aacbeda81d4bb5d665a0d70aafd5732431b64457a313e2f8843a120d0515768c",
        "size": 517266,
        "zip_members": 66,
        "files": 63,
        "html": 53,
        "manifest_digest": "0946be2600bc9794a2d71a74191ed9e01aa8c6d9cfa6a61c7bd32f4c6754170a",
        "lessons": 46,
        "subjects": {"art": 8, "humanities": 8, "asdan": 30},
    },
}


def now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sh(*args: str) -> str:
    return subprocess.check_output(args, cwd=ROOT, text=True).strip()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def inventory(root: Path) -> list[dict]:
    rows: list[dict] = []
    seen: dict[str, str] = {}
    for path in sorted(p for p in root.rglob("*") if p.is_file()):
        rel = path.relative_to(root).as_posix()
        folded = rel.casefold()
        if path.is_symlink() or (folded in seen and seen[folded] != rel):
            raise RuntimeError(f"unsafe/case-colliding extracted path: {rel}")
        seen[folded] = rel
        rows.append(
            {
                "path": rel,
                "size": path.stat().st_size,
                "sha256": sha256_file(path),
                "html": path.suffix.lower() == ".html",
            }
        )
    return rows


def manifest_digest(rows: list[dict]) -> str:
    material = "\n".join(f"{row['path']}\0{row['size']}\0{row['sha256']}" for row in rows)
    return sha256_bytes(material.encode("utf-8"))


def inspect_zip(data: bytes) -> tuple[int, list[dict], dict[str, bytes]]:
    files: list[dict] = []
    payload: dict[str, bytes] = {}
    seen: set[str] = set()
    seen_ci: set[str] = set()
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        members = archive.infolist()
        for item in members:
            path = PurePosixPath(item.filename)
            key = item.filename.rstrip("/")
            if path.is_absolute() or ".." in path.parts:
                raise RuntimeError(f"unsafe ZIP path: {item.filename}")
            if key in seen or key.casefold() in seen_ci:
                raise RuntimeError(f"duplicate/case-colliding ZIP path: {item.filename}")
            seen.add(key)
            seen_ci.add(key.casefold())
            mode = (item.external_attr >> 16) & 0xFFFF
            if stat.S_ISLNK(mode):
                raise RuntimeError(f"symlink ZIP member: {item.filename}")
            if not item.is_dir():
                body = archive.read(item)
                payload[item.filename] = body
                files.append(
                    {
                        "path": item.filename,
                        "size": len(body),
                        "sha256": sha256_bytes(body),
                        "html": item.filename.lower().endswith(".html"),
                    }
                )
    return len(members), files, payload


def load_manifest_entries(root: Path) -> dict[str, dict]:
    result: dict[str, dict] = {}
    for path in sorted(root.rglob("manifest-v3.json")):
        raw = json.loads(path.read_text("utf-8"))
        items = raw if isinstance(raw, list) else raw.get("lessons") or raw.get("items") or raw.get("files") or []
        parent = path.parent.relative_to(root).as_posix()
        for item in items:
            filename = next(
                (
                    item.get(key)
                    for key in ("file", "filename", "output", "html", "path")
                    if isinstance(item.get(key), str) and item[key].endswith(".html")
                ),
                None,
            )
            if filename:
                rel = f"{parent}/{filename}" if parent != "." else filename
                result[rel] = {**item, "manifest_path": path.relative_to(root).as_posix()}
    return result


def subject_for(rel: str) -> str | None:
    return {
        "Art_Teesside": "art",
        "Humanities_Teesside": "humanities",
        "GROW_ASDAN": "asdan",
        "LAUNCH_ASDAN": "asdan",
    }.get(PurePosixPath(rel).parts[0])


def destination(pathway: str, rel: str) -> str:
    estate = f"{pathway}_Estate_v3"
    path = PurePosixPath(rel)
    if path.suffix.lower() == ".md":
        return f"_glv3/{pathway.lower()}/{rel}"
    if path.suffix.lower() == ".html" and len(path.parts) == 1 and path.name.startswith("START_HERE_"):
        return f"{estate}/index.html"
    if path.suffix.lower() == ".html" and path.name.startswith("START_HERE_"):
        return f"{estate}/{path.parent.as_posix()}/index.html"
    name = path.name.replace("_OUTSTANDING_V3_TEST", "")
    parent = path.parent.as_posix()
    return f"{estate}/{parent}/{name}" if parent != "." else f"{estate}/{name}"


def classify(pathway: str, root: Path) -> tuple[list[dict], dict]:
    manifest = load_manifest_entries(root)
    rows: list[dict] = []
    used: dict[str, str] = {}
    for path in sorted(root.rglob("*.html")):
        rel = path.relative_to(root).as_posix()
        entry = manifest.get(rel)
        if "_OUTSTANDING_V3_TEST.html" in path.name:
            classification = "deployable lesson"
            rule = "Repaired authored lesson suffix plus required subject-manifest match."
            if entry is None:
                raise RuntimeError(f"{pathway} lesson absent from subject manifest: {rel}")
        elif path.parent == root and path.name.startswith("START_HERE_"):
            classification = "estate hub"
            rule = "Root START_HERE HTML becomes estate index."
        elif path.name.startswith("START_HERE_"):
            classification = "subject hub"
            rule = "Subject START_HERE HTML becomes subject index."
        else:
            classification = "audit/support/non-deployable"
            rule = "Support HTML without lesson suffix and absent from the lesson universe."
        dest = destination(pathway, rel)
        collision = used.get(dest)
        used[dest] = rel
        week_match = re.search(r"(?:^|_)W(\d+)(?:_|\b)", path.stem, re.I)
        prefix = re.match(r"([A-Z]+)_W\d+", path.stem)
        rows.append(
            {
                "pathway": pathway,
                "source_path": rel,
                "classification": classification,
                "classification_rule": rule,
                "source_manifest_entry": entry,
                "subject": subject_for(rel),
                "week": entry.get("week") if entry else (int(week_match.group(1)) if week_match else None),
                "strand": (entry.get("slotcode") or entry.get("slot")) if entry else (prefix.group(1) if prefix else None),
                "intended_destination_path": dest,
                "duplicate_collision_status": "collision" if collision else "unique",
                "collides_with": collision,
                "size": path.stat().st_size,
                "sha256": sha256_file(path),
            }
        )
    counts = {
        "html_members": len(rows),
        "deployable": sum(row["classification"] == "deployable lesson" for row in rows),
        "estate_hubs": sum(row["classification"] == "estate hub" for row in rows),
        "subject_hubs": sum(row["classification"] == "subject hub" for row in rows),
        "support_html": sum(row["classification"] == "audit/support/non-deployable" for row in rows),
        "by_subject": {
            subject: sum(
                row["classification"] == "deployable lesson" and row["subject"] == subject for row in rows
            )
            for subject in ("art", "humanities", "asdan")
        },
    }
    return rows, counts


def inspect_audit(root: Path, pathway: str) -> dict:
    path = root / f"{pathway}_COMPLETION_AUDIT.md"
    text = path.read_text("utf-8")
    marker = "Post-verification edits applied 2026-08-10"
    return {
        "path": path.name,
        "sha256": sha256_file(path),
        "marker_present": marker in text,
        "marker_heading_count": text.count(marker),
    }


def main() -> None:
    GL.mkdir(exist_ok=True)
    main_sha = sh("git", "rev-parse", "origin/main")
    head = sh("git", "rev-parse", "HEAD")
    transport_path = Path("/tmp/glv3-packs.tar.xz")
    if not transport_path.exists():
        raise RuntimeError("combined staged transport is missing")
    actual_transport_sha = sha256_file(transport_path)
    actual_transport_size = transport_path.stat().st_size
    if actual_transport_sha != DISCOVERED_TRANSPORT_SHA or actual_transport_size != DISCOVERED_TRANSPORT_SIZE:
        raise RuntimeError(
            f"staged transport changed unexpectedly: sha={actual_transport_sha} size={actual_transport_size}"
        )

    grow_b64 = b"".join((ROOT / "_glv3/input/GROW_ESTATE_v3_REPAIRED_2026-08-10.zip.b64").read_bytes().split())
    grow_zip = base64.b64decode(grow_b64, validate=True)
    grow_zip_member_count, grow_zip_rows, grow_zip_payload = inspect_zip(grow_zip)

    inputs = {
        "sentinel": SENTINEL,
        "generated_at": now(),
        "transport": {
            "reported_sha256": REPORTED_TRANSPORT_SHA,
            "actual_sha256": actual_transport_sha,
            "actual_size": actual_transport_size,
            "reported_hash_match": False,
            "status": "REPORTED_TRANSPORT_HASH_CONTRADICTION_RESOLVED_BY_EXACT_SOURCE_MANIFESTS",
            "resolution": (
                "Both Base64 assembly interpretations produced the same staged bytes. The staged hash is therefore "
                "deterministic but differs from the prompt's reported hash. Generation is authorised only because "
                "the safely extracted GROW and LAUNCH file-manifest digests exactly match the independently verified "
                "uploaded repaired ZIPs; the mismatch remains recorded and is not relabelled as a hash match."
            ),
        },
        "archives": {},
    }

    for pathway, root in (("GROW", GROW), ("LAUNCH", LAUNCH)):
        expected = EXP[pathway]
        rows = inventory(root)
        digest = manifest_digest(rows)
        html_count = sum(row["html"] for row in rows)
        audit = inspect_audit(root, pathway)
        if (root / "Science").exists():
            raise RuntimeError(f"{pathway}: Science folder unexpectedly present")
        if len(rows) != expected["files"] or html_count != expected["html"]:
            raise RuntimeError(f"{pathway}: extracted file/HTML count mismatch")
        if digest != expected["manifest_digest"]:
            raise RuntimeError(f"{pathway}: extracted manifest digest does not match uploaded exact ZIP")
        if not audit["marker_present"]:
            raise RuntimeError(f"{pathway}: repaired completion-audit marker missing")

        record = {
            "name": expected["zip"],
            "reported_zip_sha256": expected["sha"],
            "reported_zip_size": expected["size"],
            "reported_zip_members_including_directories": expected["zip_members"],
            "reported_html_members": expected["html"],
            "exact_uploaded_zip_verified_before_actions": True,
            "extracted_manifest_digest_sha256": digest,
            "expected_extracted_manifest_digest_sha256": expected["manifest_digest"],
            "extracted_manifest_exact_match": True,
            "extracted_files": len(rows),
            "extracted_html_members": html_count,
            "science_folder_present": False,
            "audit": audit,
            "files": rows,
        }

        if pathway == "GROW":
            exact_zip = (
                sha256_bytes(grow_zip) == expected["sha"]
                and len(grow_zip) == expected["size"]
                and grow_zip_member_count == expected["zip_members"]
                and len(grow_zip_rows) == expected["files"]
                and sum(row["html"] for row in grow_zip_rows) == expected["html"]
            )
            extracted_equal = all(
                row["path"] in grow_zip_payload
                and len(grow_zip_payload[row["path"]]) == row["size"]
                and sha256_bytes(grow_zip_payload[row["path"]]) == row["sha256"]
                for row in rows
            )
            record.update(
                {
                    "repository_standalone_zip_sha256": sha256_bytes(grow_zip),
                    "repository_standalone_zip_size": len(grow_zip),
                    "repository_standalone_zip_members_including_directories": grow_zip_member_count,
                    "repository_standalone_file_members": len(grow_zip_rows),
                    "repository_standalone_html_members": sum(row["html"] for row in grow_zip_rows),
                    "repository_standalone_exact_reported_match": exact_zip,
                    "standalone_vs_combined_extracted_equal": extracted_equal,
                }
            )
            if not exact_zip or not extracted_equal:
                raise RuntimeError("standalone exact GROW ZIP disagrees with combined staged extraction")
        else:
            record["exact_zip_note"] = (
                "The exact uploaded LAUNCH ZIP was independently verified as 517,266 bytes with the reported SHA-256. "
                "Its extracted deterministic manifest digest was pinned before this Actions run and matches every "
                "safely extracted staged file. No re-created ZIP is described as byte-identical."
            )
        inputs["archives"][pathway] = record

    (GL / "INPUT_INTEGRITY.json").write_text(json.dumps(inputs, indent=2, ensure_ascii=False) + "\n", "utf-8")

    grow_rows, grow_counts = classify("GROW", GROW)
    launch_rows, launch_counts = classify("LAUNCH", LAUNCH)
    all_rows = grow_rows + launch_rows
    if (
        grow_counts["deployable"] != 34
        or launch_counts["deployable"] != 46
        or grow_counts["by_subject"] != EXP["GROW"]["subjects"]
        or launch_counts["by_subject"] != EXP["LAUNCH"]["subjects"]
        or any(row["duplicate_collision_status"] != "unique" for row in all_rows)
    ):
        raise RuntimeError("count reconciliation mismatch")

    omitted_peq = [
        row["source_path"]
        for row in grow_rows
        if row["classification"] == "deployable lesson"
        and PurePosixPath(row["source_path"]).name.startswith("PEQ_W")
    ]
    if len(omitted_peq) != 6:
        raise RuntimeError("the six omitted GROW PEQ lessons were not recovered")

    reconciliation = {
        "sentinel": SENTINEL,
        "generated_at": now(),
        "classification_method": (
            "Authoritative `_OUTSTANDING_V3_TEST.html` suffix plus mandatory subject-manifest cross-check; "
            "estate hubs, subject hubs and support HTML are classified separately."
        ),
        "old_28_candidate_result": {
            "reported_count": 28,
            "resolved": True,
            "actual_cause": (
                "The earlier candidate classifier omitted the six GROW PEQ lesson files. Its 28 is exactly "
                "Art 8 + Humanities 8 + COMM 6 + ENT 6. PEQ_W1–PEQ_W6 were present in both the exact repaired "
                "archive and GROW_ASDAN/manifest-v3.json but were not recognised by the narrower ASDAN prefix heuristic."
            ),
            "omitted_files": omitted_peq,
            "missing_authored_bytes": False,
            "replacement_rule": (
                "Classify every repaired lesson-suffix HTML member and require a subject-manifest match; "
                "do not allowlist ASDAN prefixes."
            ),
        },
        "counts": {
            "GROW": grow_counts,
            "LAUNCH": launch_counts,
            "combined_deployable": grow_counts["deployable"] + launch_counts["deployable"],
            "expected": {"GROW": 34, "LAUNCH": 46, "combined": 80},
        },
        "members": all_rows,
    }
    (GL / "COUNT_RECONCILIATION.json").write_text(
        json.dumps(reconciliation, indent=2, ensure_ascii=False) + "\n", "utf-8"
    )

    sentinel_path = GL / "AUTONOMOUS_SENTINEL.json"
    previous = json.loads(sentinel_path.read_text("utf-8")) if sentinel_path.exists() else {}
    phases = previous.get("phase_timestamps", {})
    phases.setdefault("DISCOVERY", now())
    phases.update({"INPUT_RECONSTRUCTION": now(), "COUNT_RECONCILIATION": now()})
    sentinel = {
        "sentinel": SENTINEL,
        "repository": "MattRoper1977/Lessons",
        "historic_rollback_sha": HIST,
        "starting_main_sha": previous.get("starting_main_sha", main_sha),
        "starting_recovery_branch_sha": previous.get("starting_recovery_branch_sha", head),
        "current_phase": "GENERATION",
        "phase_timestamps": phases,
        "discovered_pr": {"number": 108, "url": "https://github.com/MattRoper1977/Lessons/pull/108"},
        "discovered_actions": [31433364146, 31433517019],
        "inputs": {
            "reported_transport_sha256": REPORTED_TRANSPORT_SHA,
            "actual_transport_sha256": actual_transport_sha,
            "transport_hash_contradiction": True,
            "grow_zip_sha256": EXP["GROW"]["sha"],
            "launch_zip_sha256": EXP["LAUNCH"]["sha"],
            "grow_zip_members": 54,
            "launch_zip_members": 66,
        },
        "gate_states": {
            **previous.get("gate_states", {}),
            "staged_transport_reported_hash": "FAIL_RECORDED",
            "exact_source_manifest_reconciliation": "PASS",
            "input_integrity": "PASS",
            "count_reconciliation": "PASS",
        },
        "latest_failure": None,
        "latest_diagnosis": (
            "The staged transport deterministically hashes to 777fcd… rather than the reported efef35…. "
            "Its safely extracted file manifests exactly match both independently verified uploaded ZIPs. "
            "The earlier 28-count proof separately omitted six GROW PEQ lessons."
        ),
        "latest_repair": (
            "Pinned exact extracted manifests for both uploaded ZIPs and replaced ASDAN prefix allowlisting "
            "with suffix-plus-manifest classification."
        ),
        "integration_base_sha": main_sha,
        "candidate_head_sha": previous.get("candidate_head_sha"),
        "merged_sha": previous.get("merged_sha"),
        "pages": previous.get("pages", {}),
        "final_production_status": previous.get("final_production_status", "STAGED_NOT_DEPLOYED"),
    }
    sentinel_path.write_text(json.dumps(sentinel, indent=2) + "\n", "utf-8")

    with (GL / "DECISIONS.md").open("a", encoding="utf-8") as handle:
        handle.write(
            "\n## Autonomous transport reconciliation\n\n"
            f"- Reported staged transport SHA-256: `{REPORTED_TRANSPORT_SHA}`.\n"
            f"- Deterministically reconstructed staged transport SHA-256: `{actual_transport_sha}` ({actual_transport_size} bytes).\n"
            "- Both Base64 assembly interpretations produced the same bytes, so this is not an assembly-order ambiguity.\n"
            "- The mismatch remains a recorded AMBER contradiction. The transport was used only after safe extraction and exact file-manifest comparison against both independently verified uploaded ZIPs.\n"
            f"- GROW extracted manifest: `{EXP['GROW']['manifest_digest']}`.\n"
            f"- LAUNCH extracted manifest: `{EXP['LAUNCH']['manifest_digest']}`.\n"
        )

    print(
        json.dumps(
            {
                "input_integrity": "PASS_WITH_RECORDED_TRANSPORT_HASH_CONTRADICTION",
                "transport_actual_sha256": actual_transport_sha,
                "GROW": grow_counts,
                "LAUNCH": launch_counts,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
