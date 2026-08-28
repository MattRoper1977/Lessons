#!/usr/bin/env python3
"""Observed controls for tools/generated_delta_predicate.py, across BOTH estates.

One positive control and four negative controls per estate. A green here is
worth nothing unless every negative is OBSERVED red, so each is asserted to be
red by its exact reason rather than merely "not green".
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from generated_delta_predicate import BEGIN, END, only_generated_delta, split_region  # noqa: E402

SITE = Path("/home/user/mattroper1977.github.io")
LESSONS = Path("/home/user/Lessons")
PRE_SPLASH = "7041e767c5eed08b05bb01a2b1cd90356cb378fa"

rows: list[tuple[str, bool, str]] = []


def record(name: str, ok: bool, detail: str) -> None:
    rows.append((name, ok, detail))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}  ·  {detail}")


def show(repo: Path, ref: str, path: str) -> bytes:
    p = subprocess.run(["git", "show", f"{ref}:{path}"], capture_output=True, cwd=repo)
    if p.returncode:
        raise SystemExit(f"git show {ref}:{path} failed: {p.stderr.decode()[:200]}")
    return p.stdout


def stamp(base: bytes, region: bytes) -> bytes:
    """Insert the region the way the generator does: after <body ...>."""
    low = base.lower()
    k = low.index(b"<body")
    k = low.index(b">", k) + 1
    return base[:k] + b"\n" + region + b"\n" + base[k:]


def run_estate(label: str, base: bytes, head: bytes, canon: bytes) -> None:
    print(f"\n=== {label} ===")
    ok, why = only_generated_delta(base, head, canon)
    record(f"{label}: POSITIVE — a legitimately stamped file passes", ok, why)

    tampered = bytearray(head)
    idx = head.index(b"<body")
    tampered[idx : idx + 5] = b"<BODY"
    ok, why = only_generated_delta(base, bytes(tampered), canon)
    record(
        f"{label}: NEGATIVE A — an authored edit riding beside the stamp turns it red",
        (not ok) and "reverse-apply" in why,
        why,
    )

    forged = head.replace(canon, canon.replace(b"mbm_splash_last", b"mbm_splash_lasT", 1), 1)
    ok, why = only_generated_delta(base, forged, canon)
    record(
        f"{label}: NEGATIVE B — a hand-forged region turns it red",
        (not ok) and "canonical bytes" in why,
        why,
    )

    ok, why = only_generated_delta(base, base, canon)
    record(f"{label}: NEGATIVE C — an unstamped file turns it red", (not ok) and "never stamped" in why, why)

    doubled = head.replace(BEGIN, BEGIN + b"\n" + BEGIN, 1)
    ok, why = only_generated_delta(base, doubled, canon)
    record(
        f"{label}: NEGATIVE D — two regions turn it red",
        (not ok) and "exactly one" in why,
        why,
    )


site_base = show(SITE, PRE_SPLASH, "townlife/index.html")
site_head = show(SITE, "origin/main", "townlife/index.html")
parts = split_region(site_head)
assert parts, "Site head carries no generated region"
canon = parts[1]
print(f"canonical region: {len(canon)} bytes")
print(f"Site base {len(site_base)} B -> head {len(site_head)} B (delta {len(site_head)-len(site_base)})")
run_estate("SITE /townlife/", site_base, site_head, canon)

lesson_rel = "Games/Neon_Garden.html"
lesson_base = (LESSONS / lesson_rel).read_bytes()
lesson_head = stamp(lesson_base, canon)
print(f"\nLessons base {len(lesson_base)} B -> synthesised head {len(lesson_head)} B (delta {len(lesson_head)-len(lesson_base)})")
run_estate(f"LESSONS /{lesson_rel}", lesson_base, lesson_head, canon)

passed = sum(1 for _, ok, _ in rows if ok)
print(f"\n{passed}/{len(rows)} controls behaved as specified")
sys.exit(0 if passed == len(rows) else 1)
