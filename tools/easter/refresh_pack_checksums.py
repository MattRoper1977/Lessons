#!/usr/bin/env python3
"""Refresh a pack's checksum rows in place -- EXISTING ROWS ONLY.

WHY NOT _sownb/feb/tools/update_pack_checksums.py
-------------------------------------------------
That tool REGENERATES a pack's entry set from a glob over the pack, and it names
its three packs as literals. Both properties are wrong for a lesson edit:
regenerating ADDS a row for every file the glob finds, so editing one deck can
silently enrol files nobody reviewed into the pack's manifest, and a literal
pack list means the tool cannot follow the edit. This one refreshes the digest
of rows the file ALREADY has, asserts the row count did not move, and refuses
otherwise.

TWO FILENAMES, AND THIS IS WHY THE TOOL EXISTS
----------------------------------------------
28 packs name the file SHA256SUMS.txt and 3 name it CHECKSUMS.sha256 -- same
format, different name, both live on main. A refresher that knew only the
common name would have walked past GROW_ASDAN/Spring1_W1-W6_2026-27 and left
two edited decks with stale digests and no error. It was found by asking every
affected pack for its file before writing anything, which is the only reason it
is not a defect in this order.

Usage:
  refresh_pack_checksums.py <deck.html> [deck.html ...]
  refresh_pack_checksums.py --check <deck.html> ...   report, write nothing
  refresh_pack_checksums.py --list-controls | --self-test
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
VERSION = "refresh-pack-checksums-v1.0.0"

# Both names seen on main. Order is preference when a pack somehow has both.
SUMS_NAMES = ("SHA256SUMS.txt", "CHECKSUMS.sha256")


def sums_file(pack: Path) -> Path | None:
    for name in SUMS_NAMES:
        p = pack / name
        if p.exists():
            return p
    return None


def refresh(sums: Path, write: bool = True) -> dict:
    pack = sums.parent
    old = sums.read_text(encoding="utf-8").splitlines()
    out, changed, absent = [], [], []
    for line in old:
        if not line.strip():
            out.append(line)
            continue
        parts = line.split(None, 1)
        if len(parts) != 2:
            out.append(line)                       # not a digest row; leave it
            continue
        digest, name = parts[0], parts[1].strip()
        target = pack / name
        if not target.exists():
            absent.append(name)
            out.append(line)                       # never drop a row
            continue
        fresh = hashlib.sha256(target.read_bytes()).hexdigest()
        if fresh != digest:
            changed.append({"name": name, "from": digest, "to": fresh})
        out.append(f"{fresh}  {name}")
    if len(out) != len(old):
        raise AssertionError("row count moved; refusing to write")
    if write and changed:
        sums.write_text("\n".join(out) + "\n", encoding="utf-8")
    return {
        "file": str(sums.relative_to(ROOT)) if sums.is_relative_to(ROOT) else str(sums),
        "toolVersion": VERSION,
        "rowsBefore": len(old), "rowsAfter": len(out),
        "rowsAdded": 0, "rowsRemoved": 0,
        "refreshed": changed,
        "rowsNamingAMissingFile": absent,
        "written": bool(write and changed),
    }


def verify(sums: Path) -> dict:
    pack = sums.parent
    bad = []
    for line in sums.read_text(encoding="utf-8").splitlines():
        parts = line.split(None, 1)
        if len(parts) != 2:
            continue
        digest, name = parts[0], parts[1].strip()
        target = pack / name
        if not target.exists():
            continue
        if hashlib.sha256(target.read_bytes()).hexdigest() != digest:
            bad.append(name)
    return {"file": str(sums), "mismatched": bad, "status": "OK" if not bad else "MISMATCH"}


def packs_for(decks) -> dict:
    out = {}
    for d in decks:
        pack = Path(d).resolve().parent
        s = sums_file(pack)
        out.setdefault(str(pack), {"sums": s, "decks": []})["decks"].append(Path(d).name)
    return out


# --------------------------------------------------------------------------
# Controls
# --------------------------------------------------------------------------

CONTROL_IDS = [
    "a-changed-file-has-its-row-refreshed",
    "an-unchanged-row-is-left-byte-identical",
    "no-row-is-added-for-a-file-the-pack-gained",
    "no-row-is-removed-when-its-file-is-gone",
    "the-alternative-filename-is-found",
    "a-blank-or-non-digest-line-survives-unchanged",
    "check-mode-writes-nothing",
    "verify-catches-a-stale-digest",
]

_A = "alpha\n"
_B = "beta\n"


def _mkpack(d: Path, name: str) -> Path:
    d.mkdir(parents=True, exist_ok=True)
    (d / "a.html").write_text(_A, encoding="utf-8")
    (d / "b.html").write_text(_B, encoding="utf-8")
    rows = "".join(f"{hashlib.sha256((d / f).read_bytes()).hexdigest()}  {f}\n"
                   for f in ("a.html", "b.html"))
    (d / name).write_text(rows, encoding="utf-8")
    return d / name


def controls() -> list[dict]:
    out = []

    def rec(cid, description, expected, observed):
        out.append({"id": cid, "description": description, "expected": expected,
                    "observed": observed, "fired": expected == observed})

    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)

        p1 = _mkpack(d / "p1", "SHA256SUMS.txt")
        (d / "p1/a.html").write_text("alpha changed\n", encoding="utf-8")
        before_b = [l for l in p1.read_text().splitlines() if l.endswith("b.html")][0]
        r = refresh(p1)
        rec("a-changed-file-has-its-row-refreshed",
            "the edited file's digest is rewritten",
            ["a.html"], [c["name"] for c in r["refreshed"]])
        after_b = [l for l in p1.read_text().splitlines() if l.endswith("b.html")][0]
        rec("an-unchanged-row-is-left-byte-identical",
            "a row whose file did not move is not rewritten differently",
            before_b, after_b)

        p2 = _mkpack(d / "p2", "SHA256SUMS.txt")
        (d / "p2/c.html").write_text("gamma\n", encoding="utf-8")   # a file with no row
        r2 = refresh(p2)
        rec("no-row-is-added-for-a-file-the-pack-gained",
            "refreshing must not enrol a file nobody reviewed -- the failure mode "
            "of a regenerate-from-glob tool",
            (2, 2, 0), (r2["rowsBefore"], r2["rowsAfter"], r2["rowsAdded"]))

        p3 = _mkpack(d / "p3", "SHA256SUMS.txt")
        (d / "p3/b.html").unlink()
        r3 = refresh(p3)
        rec("no-row-is-removed-when-its-file-is-gone",
            "a missing file is reported, never silently dropped -- deleting the "
            "row would erase the evidence that it ever existed",
            (2, ["b.html"]), (r3["rowsAfter"], r3["rowsNamingAMissingFile"]))

        p4dir = d / "p4"
        _mkpack(p4dir, "CHECKSUMS.sha256")
        rec("the-alternative-filename-is-found",
            "3 packs on main name it CHECKSUMS.sha256; a refresher that knows only "
            "the common name walks past them and leaves stale digests with no error",
            "CHECKSUMS.sha256",
            sums_file(p4dir).name if sums_file(p4dir) else None)

        # The row-count assertion in refresh() is a defensive invariant that
        # cannot be reached through this API -- `out` gains exactly one entry per
        # input line. Rather than monkeypatch something into failing, which would
        # test the monkeypatch, the control tests the risk the invariant exists
        # for: a line that is not a digest row must survive so the count cannot
        # drift. A comment header and a blank line are both real in this estate.
        p5 = _mkpack(d / "p5", "SHA256SUMS.txt")
        rows = p5.read_text(encoding="utf-8").splitlines()
        p5.write_text("# pack digests\n" + rows[0] + "\n\n" + rows[1] + "\n",
                      encoding="utf-8")
        (d / "p5/a.html").write_text("alpha changed\n", encoding="utf-8")
        r5 = refresh(p5)
        after5 = p5.read_text(encoding="utf-8").splitlines()
        rec("a-blank-or-non-digest-line-survives-unchanged",
            "a comment header and a blank line are preserved verbatim, so the row "
            "count the guard checks cannot drift under a legal file",
            (4, "# pack digests", ""),
            (r5["rowsAfter"], after5[0], after5[2]))

        p6 = _mkpack(d / "p6", "SHA256SUMS.txt")
        (d / "p6/a.html").write_text("alpha changed\n", encoding="utf-8")
        snapshot = p6.read_bytes()
        refresh(p6, write=False)
        rec("check-mode-writes-nothing",
            "--check reports without touching the file",
            snapshot, p6.read_bytes())

        p7 = _mkpack(d / "p7", "SHA256SUMS.txt")
        (d / "p7/a.html").write_text("alpha changed\n", encoding="utf-8")
        rec("verify-catches-a-stale-digest",
            "verification must fail on a digest that no longer matches its file",
            ("MISMATCH", ["a.html"]),
            (verify(p7)["status"], verify(p7)["mismatched"]))

    return out


def self_test() -> dict:
    results = controls()
    ids = [r["id"] for r in results]
    missing = [c for c in CONTROL_IDS if c not in ids]
    extra = [c for c in ids if c not in CONTROL_IDS]
    return {"tool": "refresh_pack_checksums", "toolVersion": VERSION,
            "file": "tools/easter/refresh_pack_checksums.py",
            "controlsDeclared": len(CONTROL_IDS), "controlsRun": len(results),
            "controlsFired": sum(1 for r in results if r["fired"]),
            "missingControls": missing, "undeclaredControls": extra,
            "allListedControlsFired": not missing and not extra and all(r["fired"] for r in results),
            "controls": results}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("decks", nargs="*")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--output")
    ap.add_argument("--list-controls", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()

    if a.list_controls:
        for c in CONTROL_IDS:
            print(c)
        return 0
    if a.self_test:
        rep = self_test()
        print(f"refresh_pack_checksums self-test  [{VERSION}]")
        for r in rep["controls"]:
            print(f"  {'ok  ' if r['fired'] else 'FAIL'} {r['id']:52s} "
                  f"expected={str(r['expected'])[:48]} observed={str(r['observed'])[:48]}")
        print(f"{rep['controlsFired']}/{rep['controlsRun']} controls fired")
        print("PASS" if rep["allListedControlsFired"] else "MEASUREMENT INVALID")
        return 0 if rep["allListedControlsFired"] else 1

    if not a.decks:
        raise SystemExit("usage: refresh_pack_checksums.py <deck.html> ...")

    groups = packs_for(a.decks)
    reports, missing_pack = [], []
    for pack, info in sorted(groups.items()):
        if info["sums"] is None:
            missing_pack.append(pack)
            print(f"  NO CHECKSUM FILE  {pack}  ({len(info['decks'])} deck(s)) "
                  f"-- looked for {' and '.join(SUMS_NAMES)}")
            continue
        r = refresh(info["sums"], write=not a.check)
        r["decksEdited"] = sorted(info["decks"])
        v = verify(info["sums"])
        r["verify"] = v
        reports.append(r)
        print(f"  {r['file']}  rows {r['rowsBefore']}->{r['rowsAfter']} "
              f"(+{r['rowsAdded']}/-{r['rowsRemoved']})  refreshed {len(r['refreshed'])}  "
              f"verify {v['status']}{'  [check only]' if a.check else ''}")
        for c in r["refreshed"]:
            print(f"      {c['name']}  {c['from'][:16]}... -> {c['to'][:16]}...")
        for n in r["rowsNamingAMissingFile"]:
            print(f"      ROW NAMES A MISSING FILE, left in place: {n}")

    ok = not missing_pack and all(r["verify"]["status"] == "OK" for r in reports)
    if a.output:
        out = Path(a.output)
        out = out if out.is_absolute() else ROOT / out
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(
            {"tool": "refresh_pack_checksums", "toolVersion": VERSION,
             "file": "tools/easter/refresh_pack_checksums.py",
             "subject": "pack checksum rows refreshed in place for edited decks; "
                        "existing rows only, none added, none removed",
             "packs": len(groups), "packsWithoutAChecksumFile": missing_pack,
             "allVerified": ok, "reports": reports}, indent=1) + "\n", encoding="utf-8")
    print("PASS" if ok else "RED")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
