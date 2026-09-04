#!/usr/bin/env python3
"""Keep a pack's manifest and checksum file true after decks are added.

WHY THIS IS NOT refresh_pack_checksums.py
-----------------------------------------
That tool refreshes rows a checksum file ALREADY has, and refuses to add any,
because it exists for edits to landed decks: a new row there would silently
enrol a file nobody reviewed. Adding a deck is the opposite case -- the row MUST
appear, or the pack's own record denies that the lesson exists.

The manifest is rebuilt from the decks actually present, reading each one's
lesson-config, so a pack cannot end up listing a deck it does not have or
missing one it does. Everything else in the manifest is preserved: this runs
against packs that already exist and were written by other hands.

Usage:
  pack_furniture.py <pack dir> [...]
  pack_furniture.py --list-controls | --self-test
"""
from __future__ import annotations
import argparse, hashlib, json, re, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
VERSION = "pack-furniture-v1.0.0"
SUMS_NAMES = ("SHA256SUMS.txt", "CHECKSUMS.sha256")
CFG = re.compile(r'id=["\']lesson-config["\'][^>]*>(.*?)</script>', re.S)


def deck_config(p: Path):
    m = CFG.search(p.read_text(encoding="utf-8"))
    if not m:
        return None
    try:
        return json.loads(m.group(1))
    except Exception:
        return None


def update(pack: Path) -> dict:
    decks = []
    for f in sorted(pack.glob("*.html")):
        if f.name.startswith("START_HERE"):
            continue
        cfg = deck_config(f)
        if cfg:
            decks.append((f, cfg))
    mf = pack / "manifest.json"
    data = json.loads(mf.read_text(encoding="utf-8")) if mf.exists() else {"schema": "feb-pack-v1"}

    # A MANIFEST WHOSE SCHEMA THIS TOOL DOES NOT KNOW IS LEFT ALONE.
    #
    # The Humanities packs carry a different manifest entirely -- no `lessons`
    # array at all, but `sequence`, `notAuthoredYet` and `weekSpine`, written for
    # another purpose by another hand. Rewriting one of them added an eleven-entry
    # `lessons` list and pushed `lessonCount` from 8 to 11 while
    # `plannedLessonCount` still said 8, leaving the file internally inconsistent
    # and `notAuthoredYet` still claiming decks that now exist.
    #
    # Updating those fields correctly needs the intent behind that schema, and
    # guessing at it is worse than leaving it: the checksum rows still go in, so
    # the pack's integrity record is complete either way. The mismatch is
    # REPORTED so it can be repaired deliberately.
    known = "lessons" in data or data.get("schema") == "feb-pack-v1"
    if not known:
        rows_only = _write_sums(pack)
        rows_only.update({"manifestSkipped": True,
                          "manifestSchemaKeys": sorted(data.keys()),
                          "reason": "manifest schema not recognised; rows written, "
                                    "manifest left for a deliberate repair"})
        return rows_only
    lessons = []
    for f, cfg in decks:
        entry = {"id": cfg.get("id", f.stem), "file": f.name,
                 "absoluteWeek": cfg.get("week"),
                 "cells": [{"reference": c, "cell": c.split("!")[-1],
                            "sheet": (cfg.get("source") or {}).get("sheet", ""),
                            "workbook": (cfg.get("source") or {}).get("workbook", "")}
                           for c in cfg.get("cells", [])],
                 "outcomes": cfg.get("outcomes", []),
                 "objective": cfg.get("objective", "")}
        if cfg.get("timings"):
            entry["timings"] = cfg["timings"]
        lessons.append(entry)
    before = len(data.get("lessons", []))
    data["lessons"] = lessons
    data["lessonCount"] = len(lessons)
    data.setdefault("start", "START_HERE.html")
    # a pack-level timings array is true only while every deck shares one spine
    spines = [e["timings"] for e in lessons if e.get("timings")]
    if spines and all(s == spines[0] for s in spines):
        data["timings"] = spines[0]
    elif "timings" in data:
        del data["timings"]
    mf.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    out = _write_sums(pack)
    out.update({"lessonsBefore": before, "lessonsAfter": len(lessons),
                "manifestListsEveryDeck": len(lessons) == len(decks)})
    return out


def _write_sums(pack: Path) -> dict:
    sums = next((pack / n for n in SUMS_NAMES if (pack / n).exists()), pack / SUMS_NAMES[0])
    existing = {}
    if sums.exists():
        for line in sums.read_text(encoding="utf-8").splitlines():
            parts = line.split(None, 1)
            if len(parts) == 2:
                existing[parts[1].strip()] = parts[0]
    rows, added = [], []
    for f in sorted(pack.glob("*")):
        if f.name == sums.name or f.is_dir():
            continue
        if f.name not in existing:
            added.append(f.name)
        rows.append(f"{hashlib.sha256(f.read_bytes()).hexdigest()}  {f.name}")
    sums.write_text("\n".join(rows) + "\n", encoding="utf-8")
    bad = [n for n, d in ((r.split(None, 1)[1], r.split(None, 1)[0]) for r in rows)
           if hashlib.sha256((pack / n).read_bytes()).hexdigest() != d]
    def _rel(x):
        try: return str(Path(x).resolve().relative_to(ROOT))
        except ValueError: return str(x)
    return {"file": _rel(pack) + "/manifest.json", "pack": _rel(pack),
            "sumsFile": sums.name, "rowsAdded": added, "rowCount": len(rows),
            "manifestSkipped": False,
            "verify": "OK" if not bad else f"MISMATCH {bad}"}


CONTROL_IDS = [
    "a-new-deck-gains-a-checksum-row",
    "the-manifest-lists-every-deck-present-and-no-others",
    "an-existing-manifest-field-is-preserved",
    "a-pack-level-spine-is-dropped-when-decks-disagree",
    "an-unrecognised-manifest-schema-is-left-untouched",
]

_D = ('<!doctype html><html><head><script id="lesson-config" type="application/json">'
      '{"id":"%s","week":%d,"cells":["\'S\'!C%d"],"outcomes":["o"],"objective":"obj",'
      '"timings":%s}</script></head><body></body></html>')


def controls():
    out = []

    def rec(cid, d, e, o):
        out.append({"id": cid, "description": d, "expected": e, "observed": o, "fired": e == o})

    with tempfile.TemporaryDirectory() as tmp:
        pk = Path(tmp) / "pack"; pk.mkdir()
        (pk / "a.html").write_text(_D % ("A", 1, 1, "[0,5,5]"), encoding="utf-8")
        (pk / "manifest.json").write_text(json.dumps(
            {"schema": "feb-pack-v1", "family": "F", "title": "keep me",
             "timings": [0, 9, 9], "lessons": []}), encoding="utf-8")
        (pk / "SHA256SUMS.txt").write_text("", encoding="utf-8")
        r1 = update(pk)
        rec("a-new-deck-gains-a-checksum-row",
            "refresh_pack_checksums refuses to add rows because that is right for an "
            "EDIT; adding a deck is the opposite case and the row must appear",
            True, "a.html" in r1["rowsAdded"])
        m1 = json.loads((pk / "manifest.json").read_text(encoding="utf-8"))
        rec("the-manifest-lists-every-deck-present-and-no-others",
            "a pack cannot list a deck it does not have or miss one it does",
            (1, True), (m1["lessonCount"], r1["manifestListsEveryDeck"]))
        rec("an-existing-manifest-field-is-preserved",
            "these packs were written by other hands; only lessons and counts move",
            "keep me", m1.get("title"))
        (pk / "b.html").write_text(_D % ("B", 2, 2, "[0,4,6]"), encoding="utf-8")
        update(pk)
        m2 = json.loads((pk / "manifest.json").read_text(encoding="utf-8"))
        rec("a-pack-level-spine-is-dropped-when-decks-disagree",
            "one array cannot be true of two decks with different spines, and a "
            "value true of no deck is worse than no value",
            (False, 2), ("timings" in m2, m2["lessonCount"]))
        pk2 = Path(tmp) / "foreign"; pk2.mkdir()
        (pk2 / "a.html").write_text(_D % ("A", 1, 1, "[0,5,5]"), encoding="utf-8")
        foreign = {"pack": "written by another hand", "sequence": [1, 2],
                   "notAuthoredYet": ["x"], "weekSpine": {}, "lessonCount": 8}
        (pk2 / "manifest.json").write_text(json.dumps(foreign), encoding="utf-8")
        r5 = update(pk2)
        after = json.loads((pk2 / "manifest.json").read_text(encoding="utf-8"))
        rec("an-unrecognised-manifest-schema-is-left-untouched",
            "the Humanities packs use sequence/notAuthoredYet/weekSpine and no "
            "lessons array; rewriting one left lessonCount 11 against a "
            "plannedLessonCount of 8. Rows still go in; the manifest is reported, "
            "not guessed at",
            (True, foreign, True),
            (r5.get("manifestSkipped"), after, "a.html" in r5["rowsAdded"]))
    return out


def self_test():
    res = controls(); ids = [r["id"] for r in res]
    missing = [c for c in CONTROL_IDS if c not in ids]
    return {"tool": "pack_furniture", "toolVersion": VERSION,
            "file": "tools/easter/pack_furniture.py",
            "controlsDeclared": len(CONTROL_IDS), "controlsRun": len(res),
            "controlsFired": sum(1 for r in res if r["fired"]),
            "missingControls": missing,
            "allListedControlsFired": not missing and all(r["fired"] for r in res),
            "controls": res}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("packs", nargs="*")
    ap.add_argument("--output"); ap.add_argument("--list-controls", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()
    if a.list_controls:
        print("\n".join(CONTROL_IDS)); raise SystemExit(0)
    if a.self_test:
        rep = self_test()
        print(f"pack_furniture self-test  [{VERSION}]")
        for r in rep["controls"]:
            print(f"  {'ok  ' if r['fired'] else 'FAIL'} {r['id']:52s} "
                  f"expected={r['expected']} observed={r['observed']}")
        print(f"{rep['controlsFired']}/{rep['controlsRun']} controls fired")
        print("PASS" if rep["allListedControlsFired"] else "MEASUREMENT INVALID")
        raise SystemExit(0 if rep["allListedControlsFired"] else 1)
    recs = [update(Path(p)) for p in a.packs]
    for r in recs:
        if r.get("manifestSkipped"):
            print(f"  {r['pack']}  manifest LEFT ALONE (schema not recognised: "
                  f"{','.join(r['manifestSchemaKeys'][:4])}...)  "
                  f"+{len(r['rowsAdded'])} rows  verify {r['verify']}")
        else:
            print(f"  {r['pack']}  lessons {r['lessonsBefore']}->{r['lessonsAfter']}  "
                  f"+{len(r['rowsAdded'])} rows  {r['sumsFile']}  verify {r['verify']}")
    if a.output:
        Path(a.output).parent.mkdir(parents=True, exist_ok=True)
        Path(a.output).write_text(json.dumps(recs, indent=1) + "\n", encoding="utf-8")
