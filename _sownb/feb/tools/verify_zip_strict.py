#!/usr/bin/env python3
"""Second-implementation ZIP verifier with an EOF-bound outer EOCD."""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import struct
import tempfile
import zipfile
from pathlib import Path, PurePosixPath


EOCD = b"PK\x05\x06"
CENTRAL = b"PK\x01\x02"


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def expected_entries(source: Path) -> list[str]:
    entries = []
    for path in sorted(source.rglob("*")):
        rel = path.relative_to(source).as_posix()
        entries.append(rel + "/" if path.is_dir() else rel)
    return entries


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("archive")
    parser.add_argument("source_directory")
    parser.add_argument("--output")
    args = parser.parse_args()
    archive = Path(args.archive).resolve()
    source = Path(args.source_directory).resolve()
    data = archive.read_bytes()
    start = max(0, len(data) - 65557)
    eocd_offset = data.rfind(EOCD, start)
    if eocd_offset < 0 or eocd_offset + 22 > len(data):
        raise SystemExit("outer EOCD not found")
    signature, disk, cd_disk, disk_entries, total_entries, cd_size, cd_offset, comment_length = struct.unpack_from("<4s4H2LH", data, eocd_offset)
    eocd_at_eof = eocd_offset + 22 + comment_length == len(data)
    central_bound = cd_offset + cd_size == eocd_offset and data[cd_offset:cd_offset + 4] == CENTRAL
    expected = expected_entries(source)
    with zipfile.ZipFile(archive) as bundle:
        infos = bundle.infolist()
        names = [item.filename for item in infos]
        safe = all(
            not PurePosixPath(name).is_absolute()
            and ".." not in PurePosixPath(name).parts
            and "\\" not in name
            for name in names
        )
        duplicate_free = len(names) == len(set(names))
        exact_entries = sorted(names) == sorted(expected)
        testzip = bundle.testzip()
        with tempfile.TemporaryDirectory(prefix="rsh3_zip_verify_") as temp:
            extract_root = Path(temp)
            bundle.extractall(extract_root)
            extracted = expected_entries(extract_root)
            extracted_exact = sorted(extracted) == sorted(expected)
            hashes = []
            for name in expected:
                if name.endswith("/"):
                    continue
                source_file = source / name
                extracted_file = extract_root / name
                hashes.append({"entry": name, "sourceSha256": sha(source_file), "extractedSha256": sha(extracted_file), "match": sha(source_file) == sha(extracted_file)})
    report = {
        "gate": "rsh3-strict-archive-verifier",
        "archive": str(archive),
        "archiveBytes": len(data),
        "archiveSha256": hashlib.sha256(data).hexdigest(),
        "outerEocdOffset": eocd_offset,
        "outerEocdTerminatesAtFileEnd": eocd_at_eof,
        "centralDirectoryOffset": cd_offset,
        "centralDirectoryBytes": cd_size,
        "centralDirectoryBoundToOuterEocd": central_bound,
        "declaredEntries": total_entries,
        "diskEntries": disk_entries,
        "singleDisk": disk == 0 and cd_disk == 0,
        "expectedEntries": expected,
        "actualEntries": names,
        "exactEntrySet": exact_entries,
        "actualEntryOrder": names,
        "duplicateFree": duplicate_free,
        "safePaths": safe,
        "zipfileTestzip": testzip,
        "extractedEntrySetExact": extracted_exact,
        "extractedHashes": hashes,
    }
    report["status"] = "PASS" if all([
        eocd_at_eof, central_bound, total_entries == len(names), disk_entries == total_entries,
        report["singleDisk"], exact_entries, duplicate_free, safe, testzip is None,
        extracted_exact, all(row["match"] for row in hashes),
    ]) else "RED"
    if args.output:
        output = Path(args.output).resolve()
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: report[key] for key in ("status", "archive", "archiveBytes", "archiveSha256", "outerEocdTerminatesAtFileEnd", "centralDirectoryBoundToOuterEocd", "declaredEntries", "exactEntrySet", "extractedEntrySetExact")}, indent=2))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
