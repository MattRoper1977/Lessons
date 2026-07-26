#!/usr/bin/env python3
"""
hash_sweep.py  —  LundyLoop instrument  [LL-INST-01]

WHAT IT DERIVES
  Sets of identical and near-identical files across the tracked estate, and
  each member's catalogue status in resources.json.

HOW IT DERIVES IT  (three methods, deliberately not sharing a premise)
  M1  raw SHA-256 over bytes.           Literal. Presence only. Cannot lie.
  M2  SHA-256 over normalised text:     Literal after a stated transform
      data-URIs stripped, comments      (data-URI strip is mandated by
      removed, whitespace collapsed.    standing rule 10).
  M3  MinHash/Jaccard over 8-word       Approximate. Catches near-twins that
      shingles of the normalised text.  M2's exact hash cannot.
  X   filename-stem similarity.         INDEPENDENT of all three above: it
                                        reads names, not content. Used as the
                                        cross-check, because M1/M2/M3 all
                                        share the premise "content defines
                                        identity" and would fail together if
                                        that premise were wrong for a file.

  Catalogue membership is a literal path match against resources.json["file"],
  normalised for ./ prefixes, backslashes, and percent-encoding. No
  interpretation, no fuzzy title matching — per standing rule 4, presence over
  interpretation.

WHAT IT STRUCTURALLY CANNOT DETECT
  - Two files that are semantically the same lesson but share no text.
  - A catalogue entry that points at the *wrong* file which nonetheless exists.
  - Whether an uncatalogued file is *meant* to be catalogued. It reports the
    fact, not the disposition.

SCOPE
  git ls-files at HEAD. Untracked working-copy files (including this script
  before it is committed) are deliberately out of scope, so the instrument
  cannot see itself and inflate.

STATUS: current
"""

import hashlib
import json
import re
import subprocess
import sys
from collections import defaultdict
from difflib import SequenceMatcher
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parents[2]

DATA_URI = re.compile(rb"data:[a-zA-Z0-9.+/-]+;base64,[A-Za-z0-9+/=\s]+")
COMMENT = re.compile(rb"<!--.*?-->", re.S)
WS = re.compile(rb"\s+")

NUM_PERM = 128
SHINGLE = 8
MASK = (1 << 61) - 1
RNG = np.random.default_rng(20260726)          # fixed seed: reproducible
A = RNG.integers(1, MASK, NUM_PERM, dtype=np.uint64)
B = RNG.integers(0, MASK, NUM_PERM, dtype=np.uint64)


def _is_texty(raw: bytes) -> bool:
    """Content sniff, not extension. Binary formats are excluded because shingling
    them is meaningless, not because of what they are called."""
    if raw[:8] == b"\x89PNG\r\n\x1a\n" or raw[:3] == b"\xff\xd8\xff" or raw[:4] == b"PK\x03\x04":
        return False
    if raw[:4] == b"%PDF" and b"<html" not in raw[:400].lower():
        return False
    return b"\x00" not in raw[:8192]


def tracked_files():
    out = subprocess.run(
        ["git", "-C", str(REPO), "ls-files", "-z"],
        capture_output=True, check=True).stdout
    return [p for p in out.decode().split("\0") if p]


def normalise(raw: bytes) -> bytes:
    """Standing rule 10: strip data-URIs before ANY text measurement."""
    t = DATA_URI.sub(b"data:STRIPPED", raw)
    t = COMMENT.sub(b" ", t)
    t = WS.sub(b" ", t)
    return t.strip()


def minhash(norm: bytes):
    words = norm.split()
    if len(words) < SHINGLE:
        return None
    hs = np.fromiter(
        (int.from_bytes(
            hashlib.blake2b(b" ".join(words[i:i + SHINGLE]), digest_size=8).digest(),
            "big") & MASK
         for i in range(len(words) - SHINGLE + 1)),
        dtype=np.uint64)
    hs = np.unique(hs)
    sig = ((A[:, None] * hs[None, :] + B[:, None]) & MASK).min(axis=1)
    return sig


def load_catalogue():
    cat = json.loads((REPO / "resources.json").read_text(encoding="utf-8"))
    from urllib.parse import unquote

    def norm_path(p):
        p = unquote(str(p)).replace("\\", "/").lstrip("./")
        return p

    by_path = defaultdict(list)
    for e in cat:
        f = e.get("file")
        if f:
            by_path[norm_path(f)].append(e.get("id") or e.get("title") or "?")
    return cat, by_path


def stem_sim(a, b):
    return SequenceMatcher(None, Path(a).stem.lower(), Path(b).stem.lower()).ratio()


def main():
    files = tracked_files()
    cat, cat_by_path = load_catalogue()

    raw_h, norm_h, sigs, sizes, norm_sizes = {}, {}, {}, {}, {}
    for f in files:
        p = REPO / f
        try:
            raw = p.read_bytes()
        except OSError as e:
            print(f"UNREADABLE {f}: {e}", file=sys.stderr)
            continue
        raw_h[f] = hashlib.sha256(raw).hexdigest()
        sizes[f] = len(raw)
        n = normalise(raw)
        norm_h[f] = hashlib.sha256(n).hexdigest()
        norm_sizes[f] = len(n)
        # EXTENSION BLINDNESS, FIXED. v1 selected candidates by file extension, in a
        # repo whose defining defect is that filenames lie. It never tested
        # Head_Office_Summary.pdf (which is HTML) or weekly_loop_log.csv (also
        # HTML), so two displaced copies were invisible to the instrument that
        # exists to find displaced copies. Sniff the content instead.
        if _is_texty(raw):
            s = minhash(n)
            if s is not None:
                sigs[f] = s

    def group(hd):
        g = defaultdict(list)
        for f, h in hd.items():
            g[h].append(f)
        return {h: sorted(v) for h, v in g.items() if len(v) > 1}

    exact = group(raw_h)
    normed = group(norm_h)

    # near-identical via MinHash, excluding pairs already caught by M2
    names = sorted(sigs)
    M = np.array([sigs[f] for f in names], dtype=np.uint64)
    near = []
    for i in range(len(names)):
        eq = (M[i + 1:] == M[i]).mean(axis=1) if i + 1 < len(names) else np.array([])
        for j_off, jac in enumerate(eq):
            if jac >= 0.60:
                a, b = names[i], names[i + 1 + j_off]
                if norm_h[a] == norm_h[b]:
                    continue
                near.append((round(float(jac), 3), a, b))
    near.sort(reverse=True)

    def cat_status(f):
        ids = cat_by_path.get(f)
        return ("CATALOGUED:" + ",".join(ids)) if ids else "UNCATALOGUED"

    report = {
        "head": subprocess.run(["git", "-C", str(REPO), "rev-parse", "HEAD"],
                               capture_output=True, text=True).stdout.strip(),
        "files_swept": len(raw_h),
        "catalogue_entries": len(cat),
        "exact_sets": [
            {"sha": h[:12], "bytes": sizes[v[0]],
             "members": [{"file": f, "catalogue": cat_status(f)} for f in v]}
            for h, v in sorted(exact.items(), key=lambda kv: -sizes[kv[1][0]])],
        "normalised_only_sets": [
            {"nsha": h[:12],
             "members": [{"file": f, "bytes": sizes[f], "catalogue": cat_status(f)} for f in v]}
            for h, v in normed.items() if h not in {norm_h[m[0]] for m in exact.values()}],
        "near_identical": [
            {"jaccard": j, "a": a, "b": b,
             "a_cat": cat_status(a), "b_cat": cat_status(b),
             "stem_sim": round(stem_sim(a, b), 2),
             "a_norm_bytes": norm_sizes[a], "b_norm_bytes": norm_sizes[b]}
            for j, a, b in near],
        "catalogue_entries_pointing_at_missing_files": sorted(
            p for p in cat_by_path if not (REPO / p).exists()),
        "tracked_html_not_catalogued": sorted(
            f for f in raw_h
            if f.lower().endswith(".html") and f not in cat_by_path),
    }
    print(json.dumps(report, indent=1))


if __name__ == "__main__":
    main()
