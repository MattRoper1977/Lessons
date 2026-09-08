#!/usr/bin/env python3
"""UX2 D3 — the companion-pack entries in resources.json, derived from
data/companion-packs.json (the D2 placement manifest) and never typed.

One catalogue entry per pack (the two packs that pre-date the order are hub
rows already and are not re-catalogued):

    id                 the pack id from the manifest
    kind               "pack"
    companionOf        the deployed lesson the pack was matched to (D1)
    files              [{role, type, path}] — the landed files only
    builtFrom          sha256 of the pack's own source HTML
    packRevisionDrift  the D1 DRIFT verdict
    halfTerm           copied from the matched lesson's catalogue row when one
                       exists, else the pack's own term (the filename week —
                       D2's tie-break rule); unit copied only from the lesson
    subject / family   the convention of the directory the lesson lives in,
                       read from its START_HERE (teacher) row
    file               the editable deck (role "lesson"), so the entry opens
                       and sizes like every other row
    title / desc       "<W> · <title> · Companion pack" and the roles present

    python3 tools/ux2/companion_catalogue.py --write        append / refresh the pack rows
    python3 tools/ux2/companion_catalogue.py --check        committed == derived, files resolve once
    python3 tools/ux2/companion_catalogue.py --report       counts, drift, attachment
    python3 tools/ux2/companion_catalogue.py --self-test    six planted defects, each red
    …  --manifest PATH  --tree PATH   derive from another checkout (before the
                                      placement PR is merged into this one)
"""
from __future__ import annotations

import argparse
import copy
import json
import os
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CATALOGUE = ROOT / "resources.json"
DEFAULT_MANIFEST = ROOT / "data/companion-packs.json"
HALF_TERMS = ("Autumn 1", "Autumn 2", "Spring 1", "Spring 2", "Summer 1", "Summer 2")
ROLES = ("lesson", "teacher", "pupil", "slides")
TYPES = ("pptx", "docx", "pdf")
ROLE_WORDS = {"lesson": "editable slides", "slides": "slides", "teacher": "teacher notes", "pupil": "pupil booklet"}
PACK_KEYS = ("kind", "companionOf", "files", "builtFrom", "packRevisionDrift")


def read_json(path: Path):
    return json.loads(path.read_text("utf-8"))


def serialise(rows) -> str:
    return json.dumps(rows, ensure_ascii=False, indent=2) + "\n"


def is_pack(row: dict) -> bool:
    return row.get("kind") == "pack"


def anchor_for(directory: str, rows: list[dict]) -> dict | None:
    """The catalogue row that states the directory's subject/family convention:
    its START_HERE (teacher) row, else any catalogued sibling."""
    siblings = [r for r in rows if not is_pack(r) and os.path.dirname(r.get("file", "")) == directory]
    for r in siblings:
        if r.get("type") == "teacher" and os.path.basename(r["file"]).upper().startswith("START_HERE"):
            return r
    return siblings[0] if siblings else None


def describe(files: list[dict]) -> str:
    parts = []
    for role in ROLES:
        types = sorted({f["type"].upper() for f in files if f["role"] == role})
        if types:
            parts.append(f"{ROLE_WORDS[role]} ({', '.join(types)})")
    return ", ".join(parts)


def derive(rows: list[dict], manifest: dict) -> tuple[list[dict], list[dict]]:
    """Return (pack rows, problems). A pack with a problem is not landed."""
    base = [r for r in rows if not is_pack(r)]
    by_file = {r["file"]: r for r in base}
    ids = {r["id"] for r in base}
    generated = str(manifest.get("generated", ""))[:10]
    if len(generated) != 10:
        raise SystemExit("[FAIL] manifest has no generated date")
    out, problems = [], []
    for pack in manifest["packs"]:
        lesson = pack["companionOf"]
        directory = os.path.dirname(lesson)
        anchor = anchor_for(directory, base)
        if anchor is None:
            problems.append({"id": pack["id"], "problem": "no catalogued row states the directory's subject/family", "directory": directory})
            continue
        # The manifest id keeps the W-token verbatim (A2_W7L2); the catalogue's id
        # pattern is ^[a-z0-9-]+$, so the underscore becomes a hyphen and nothing else changes.
        row_id = pack["id"].replace("_", "-")
        if row_id in ids:
            problems.append({"id": pack["id"], "problem": "id collides with an existing catalogue row"})
            continue
        files = [{"role": f["role"], "type": f["type"], "path": f["path"]} for f in pack["files"]]
        if not files or any(f["role"] not in ROLES or f["type"] not in TYPES for f in files):
            problems.append({"id": pack["id"], "problem": "a file has a role or type outside the closed sets"})
            continue
        primary = next((f for f in files if f["role"] == "lesson"), files[0])
        host = by_file.get(lesson)
        half_term = (host or {}).get("halfTerm") or pack.get("term")
        if half_term not in HALF_TERMS:
            problems.append({"id": pack["id"], "problem": f"half-term {half_term!r} is not a spine label"})
            continue
        year = "2026-27" if "2026-27" in lesson else (host or {}).get("year")
        if year not in ("2025-26", "2026-27"):
            problems.append({"id": pack["id"], "problem": "academic year not derivable from the lesson path or row"})
            continue
        row = {
            "id": row_id,
            "subject": anchor["subject"],
            "title": f"{pack['wtoken']} · {pack['title']} · Companion pack",
            "file": primary["path"],
            "type": "support",
            "family": anchor["family"],
            "added": generated,
            "desc": f"Companion pack for the {pack['pathway']} {pack['subject']} lesson {pack['wtoken']} · {pack['title']}: {describe(files)}. The lesson itself is unchanged.",
            "year": year,
            "halfTerm": half_term,
        }
        if host and host.get("unit"):
            row["unit"] = host["unit"]
        row.update({
            "kind": "pack",
            "companionOf": lesson,
            "builtFrom": pack["builtFrom"],
            "packRevisionDrift": bool(pack.get("packRevisionDrift")),
            "files": files,
        })
        out.append(row)
    return out, problems


def apply(rows: list[dict], packs: list[dict]) -> list[dict]:
    return [r for r in rows if not is_pack(r)] + packs


def check(rows: list[dict], manifest: dict, tree: Path) -> list[str]:
    errors: list[str] = []
    packs, problems = derive(rows, manifest)
    for p in problems:
        errors.append(f"{p['id']}: {p['problem']}")
    have = [r for r in rows if is_pack(r)]
    if [r["id"] for r in have] != [r["id"] for r in packs]:
        errors.append(f"pack rows differ from the derivation: {len(have)} committed vs {len(packs)} derived (order and set must match)")
    for index, (h, w) in enumerate(zip(have, packs)):
        if h != w:
            keys = sorted(k for k in set(h) | set(w) if h.get(k) != w.get(k))
            errors.append(f"pack row {index} ({h.get('id')}): differs from the derivation on {keys}")
    if rows and is_pack(rows[0]):
        errors.append("a pack row precedes the original rows (packs are appended)")
    first_pack = next((i for i, r in enumerate(rows) if is_pack(r)), len(rows))
    if any(not is_pack(r) for r in rows[first_pack:]):
        errors.append("a non-pack row follows the pack rows (packs are the tail)")
    owners: Counter = Counter()
    for r in have:
        for key in PACK_KEYS:
            if key not in r:
                errors.append(f"{r.get('id')}: pack row lacks {key}")
        if r.get("file") not in {f["path"] for f in r.get("files", [])}:
            errors.append(f"{r.get('id')}: file is not one of its own files[]")
        for f in r.get("files", []):
            owners[f["path"]] += 1
            if not (tree / f["path"]).is_file():
                errors.append(f"{r.get('id')}: missing on disk: {f['path']}")
    for path, n in owners.items():
        if n != 1:
            errors.append(f"{path}: listed under {n} pack entries (must be exactly one)")
    return errors


def report(rows: list[dict], manifest: dict) -> dict:
    packs, problems = derive(rows, manifest)
    base = [r for r in rows if not is_pack(r)]
    by_file = {r["file"]: r for r in base}
    return {
        "packs": len(packs),
        "notLanded": problems,
        "bySubjectPathway": dict(Counter(f"{p['subject']} · {p['pathway']}" for p in manifest["packs"])),
        "byHalfTerm": dict(Counter(r["halfTerm"] for r in packs)),
        "attachedToCatalogueLesson": sum(1 for r in packs if r["companionOf"] in by_file),
        "standalone": sum(1 for r in packs if r["companionOf"] not in by_file),
        "withUnit": sum(1 for r in packs if "unit" in r),
        "driftFlagged": [r["id"] for r in packs if r["packRevisionDrift"]],
        "files": sum(len(r["files"]) for r in packs),
        "subjectSources": dict(Counter(f"{r['subject']} / {r['family']}" for r in packs)),
    }


def self_test(rows: list[dict], manifest: dict, tree: Path) -> None:
    packs, problems = derive(rows, manifest)
    if problems:
        raise SystemExit(f"[FAIL] self-test needs a clean derivation; problems: {problems[:3]}")
    good = apply(rows, packs)
    if check(good, manifest, tree):
        raise SystemExit(f"[FAIL] self-test: the real derivation is not green: {check(good, manifest, tree)[:3]}")
    plants = []
    a = copy.deepcopy(good); a[-1]["files"][0]["role"] = "answers"; plants.append(("a file role outside the closed set", a))
    b = copy.deepcopy(good); b[-1]["kind"] = "bundle"; plants.append(("a novel kind", b))
    c = copy.deepcopy(good); c[-1]["files"].append(dict(c[-2]["files"][0])); plants.append(("one file under two pack entries", c))
    d = copy.deepcopy(good); del d[-1]["companionOf"]; plants.append(("a pack row without companionOf", d))
    e = copy.deepcopy(good); e[-1]["halfTerm"] = "Spring 2"; plants.append(("a pack half-term that is not its derivation", e))
    f = copy.deepcopy(good); f.pop(); plants.append(("a dropped pack row", f))
    for name, planted in plants:
        red = bool(check(planted, manifest, tree))
        print(f"  {'PASS' if red else 'FAIL'}  red on {name}")
        if not red:
            raise SystemExit("[FAIL] companion catalogue self-test: a planted defect passed")
    print(f"[PASS] companion catalogue self-test: {len(plants)}/{len(plants)} plants red, real derivation green ({len(packs)} packs)")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--tree", type=Path, default=ROOT, help="working tree holding the pack files (default: this repository)")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--report", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if not args.manifest.is_file():
        print(f"[INCONCLUSIVE] no placement manifest at {args.manifest}")
        return 2
    manifest = read_json(args.manifest)
    rows = read_json(CATALOGUE)
    if args.self_test:
        self_test(rows, manifest, args.tree)
        return 0
    if args.report:
        print(json.dumps(report(rows, manifest), ensure_ascii=False, indent=2))
    if args.write:
        packs, problems = derive(rows, manifest)
        if problems:
            print(json.dumps({"notLanded": problems}, ensure_ascii=False, indent=2))
        text = serialise(apply(rows, packs))
        CATALOGUE.write_text(text, "utf-8")
        print(f"[DONE] {len(packs)} pack rows written after {sum(1 for r in rows if not is_pack(r))} rows ({len(problems)} not landed)")
        rows = json.loads(text)
    if args.check or not (args.write or args.report):
        errors = check(rows, manifest, args.tree)
        for e in errors:
            print("  " + e)
        if errors:
            print(f"[FAIL] companion catalogue: {len(errors)} problem(s)")
            return 1
        print(f"[PASS] companion catalogue: {sum(1 for r in rows if is_pack(r))} pack rows equal their derivation; every file on disk and owned once")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
