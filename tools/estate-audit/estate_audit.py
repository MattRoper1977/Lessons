#!/usr/bin/env python3
"""Integrity-check and execute the ordered Lessons estate-audit source set."""

from __future__ import annotations

import hashlib
import pathlib

_EXPECTED_SHA256 = "86837601c2efa7febc9e460f6bb4d7308ac75700dc96452b12b93d60fb5de31e"
_SOURCE_DIR = pathlib.Path(__file__).with_name("source")
_PARTS = sorted(_SOURCE_DIR.glob("*.inc"))
if not _PARTS:
    raise RuntimeError(f"Estate audit source set is missing: {_SOURCE_DIR}")
_SOURCE = "".join(part.read_text(encoding="utf-8") for part in _PARTS)
_ACTUAL_SHA256 = hashlib.sha256(_SOURCE.encode("utf-8")).hexdigest()
if _ACTUAL_SHA256 != _EXPECTED_SHA256:
    raise RuntimeError(
        "Estate audit source-set checksum mismatch: "
        f"expected {_EXPECTED_SHA256}, got {_ACTUAL_SHA256}"
    )
exec(compile(_SOURCE, str(_SOURCE_DIR / "assembled_estate_audit.py"), "exec"), globals(), globals())
