#!/usr/bin/env python3
"""Safely validate and extract the deterministic GLV3 source transport."""
from __future__ import annotations

import argparse
import hashlib
import json
import stat
import tarfile
from pathlib import Path, PurePosixPath

ARCHIVE_SUFFIXES = {".zip", ".7z", ".rar", ".tar", ".gz", ".bz2", ".xz"}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("archive", type=Path)
    parser.add_argument("destination", type=Path)
    parser.add_argument("--sha256", required=True)
    parser.add_argument("--size", type=int, required=True)
    args = parser.parse_args()

    archive = args.archive.resolve()
    destination = args.destination.resolve()
    if not archive.is_file():
        raise SystemExit(f"transport missing: {archive}")
    actual_sha = sha256(archive)
    actual_size = archive.stat().st_size
    if actual_sha != args.sha256 or actual_size != args.size:
        raise SystemExit(
            f"transport mismatch: sha={actual_sha} size={actual_size}; "
            f"expected sha={args.sha256} size={args.size}"
        )

    if destination.exists():
        import shutil
        shutil.rmtree(destination)
    destination.mkdir(parents=True)

    seen: set[str] = set()
    seen_casefold: set[str] = set()
    validated = []
    with tarfile.open(archive, "r:xz") as bundle:
        members = bundle.getmembers()
        for member in members:
            pure = PurePosixPath(member.name)
            key = member.name.rstrip("/")
            folded = key.casefold()
            if pure.is_absolute() or ".." in pure.parts or "\\" in member.name:
                raise SystemExit(f"unsafe transport path: {member.name}")
            if key in seen or folded in seen_casefold:
                raise SystemExit(f"duplicate/case-colliding transport path: {member.name}")
            seen.add(key)
            seen_casefold.add(folded)
            if member.issym() or member.islnk() or member.isdev() or member.isfifo():
                raise SystemExit(f"unsupported transport member: {member.name}")
            if member.isfile() and member.mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH):
                raise SystemExit(f"unexpected executable transport member: {member.name}")
            if member.isfile() and PurePosixPath(member.name).suffix.casefold() in ARCHIVE_SUFFIXES:
                raise SystemExit(f"undocumented nested archive: {member.name}")
            validated.append(member.name)
        bundle.extractall(destination, filter="data")

    roots = {}
    for name in ("grow", "launch"):
        root = destination / name
        if not root.is_dir():
            raise SystemExit(f"missing extracted root: {name}")
        if any(path.is_dir() and path.name.casefold() == "science" for path in root.iterdir()):
            raise SystemExit(f"unexpected Science folder under {name}")
        roots[name] = {
            "files": sum(path.is_file() for path in root.rglob("*")),
            "html": sum(path.is_file() and path.suffix.casefold() == ".html" for path in root.rglob("*")),
        }

    result = {
        "result": "PASS",
        "transport_sha256": actual_sha,
        "transport_size": actual_size,
        "tar_members": len(validated),
        "roots": roots,
    }
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
