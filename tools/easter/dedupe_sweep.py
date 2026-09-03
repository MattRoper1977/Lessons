#!/usr/bin/env python3
"""Estate-wide sweep for the duplicated-paragraph defect.

WHY THIS EXISTS
---------------
Three W15 Humanities decks were trimmed one at a time -- BUILD (#280), GROW
(#281), LAUNCH (this PR) -- and all three carried the SAME defect in the SAME
stage: one paragraph in which every sentence is printed exactly four times.
BUILD: 16 sentences x4. GROW: x4. LAUNCH: 16 sentences x4, uniform, no
exceptions. Three independent authoring accidents do not produce a uniform
x4 in one named stage. That is a generator emitting its paragraph four times,
and a generator defect is estate-shaped, not deck-shaped.

Trimming decks as they are noticed measures nothing about how many are left.
This sweep asks the whole estate the same question with the same instrument
(dedupe_stage_text.analyse, which is read-only) so the remaining exposure is a
number the repo can re-derive rather than an impression.

WHAT IT DELIBERATELY DOES NOT DO
--------------------------------
It never writes. Remediation stays a per-family lesson PR with its own g23 and
containment evidence, because a sweep that could also fix would be a sweep
nobody reads before it fixes.

SCOPE. Deck-shaped files only -- a file lesson_stages finds at least one stage
in. Site/, Games/ and Apps/ are excluded: SC3 owns them and this is a single
writer. Directories of preserved/superseded copies are excluded by name so the
count reports the LIVE estate; --include-archived reports them too, separately.

Usage:
  dedupe_sweep.py                     sweep the live estate
  dedupe_sweep.py --output r.json
  dedupe_sweep.py --include-archived
  dedupe_sweep.py --project            what deduping would do to each deck's g23
  dedupe_sweep.py --list-controls | --self-test
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
import tempfile
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
VERSION = "dedupe-sweep-v1.0.0"

_spec = importlib.util.spec_from_file_location(
    "dedupe_stage_text", Path(__file__).resolve().parent / "dedupe_stage_text.py")
dst = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(dst)
ls = dst.ls

# SC3 owns these; a single writer does not read them into a remediation list.
FOREIGN = ("Site", "Games", "Apps")
# Copies kept for provenance. Counting them as live exposure would overstate it.
ARCHIVED_MARKERS = ("_approved", "_archive", "archive", "superseded", "preserved",
                    "_retired", "backup", "node_modules", ".git")


def _is_archived(rel: Path) -> bool:
    return any(any(m.lower() in part.lower() for m in ARCHIVED_MARKERS)
               for part in rel.parts[:-1])


def candidates(root: Path = ROOT, include_archived: bool = False) -> list[Path]:
    out = []
    for p in sorted(root.rglob("*.html")):
        rel = p.relative_to(root)
        if rel.parts and rel.parts[0] in FOREIGN:
            continue
        if not include_archived and _is_archived(rel):
            continue
        out.append(p)
    return out


def sweep(root: Path = ROOT, include_archived: bool = False) -> dict:
    rows, unreadable, scanned = [], [], 0
    for p in candidates(root, include_archived):
        try:
            tree = ls.parse(p)
            if not ls.stages(tree, ls.ScreenView(tree)):
                continue
        except Exception as e:                       # not a deck; not an error
            continue
        scanned += 1
        try:
            plan = dst.analyse(p)
        except Exception as e:
            unreadable.append({"file": str(p.relative_to(root)), "error": repr(e)[:200]})
            continue
        if not plan["targets"] and not plan["refused"]:
            continue
        factors = Counter()
        for t in plan["targets"] + plan["refused"]:
            factors.update(t["repeatedSentences"].values())
        rows.append({
            "file": str(p.relative_to(root)),
            "removable": plan["duplicatedWordsRemovable"],
            "refused": plan["duplicatedWordsRefused"],
            "stages": sorted({t["stage"] for t in plan["targets"] + plan["refused"]}),
            "stageTitles": sorted({t["stageTitle"] for t in plan["targets"] + plan["refused"] if t["stageTitle"]}),
            "repeatFactors": dict(sorted(factors.items())),
        })
    rows.sort(key=lambda r: -r["removable"])
    all_factors = Counter()
    for r in rows:
        for k, v in r["repeatFactors"].items():
            all_factors[k] += v
    return {
        "tool": "dedupe_sweep", "toolVersion": VERSION,
        "file": "tools/easter/dedupe_sweep.py",
        "subject": ("estate-wide read-only sweep for the duplicated-paragraph defect: "
                    "how many live deck-shaped files still carry a paragraph whose "
                    "sentences repeat, and by what factor"),
        "includesArchived": include_archived,
        "decksScanned": scanned,
        "decksAffected": len(rows),
        "wordsRemovableTotal": sum(r["removable"] for r in rows),
        "wordsRefusedTotal": sum(r["refused"] for r in rows),
        "repeatFactorHistogram": dict(sorted(all_factors.items())),
        "unreadable": unreadable,
        "rows": rows,
    }


# --------------------------------------------------------------------------
# Projection
# --------------------------------------------------------------------------

# A ratio quoted from arithmetic is a claim; a ratio quoted from the gate is a
# measurement. This copies each affected deck to a scratch directory, dedupes
# THE COPY, and re-runs g23 against it. The repository is never written to, and
# the number in the ledger is the number g23 printed.
FAMILY_LANES = ("BUILD", "GROW", "LAUNCH")


def family_of(rel: str) -> str | None:
    if rel.startswith("Science_Teesside/"):
        return f"{rel.split('/')[1].upper()} Science"
    if rel.startswith("Humanities_Teesside/"):
        return f"{rel.split('/')[1].split('_')[0]} Humanities"
    for lane in FAMILY_LANES:
        if rel.startswith(f"{lane}_ASDAN/"):
            return f"{lane} ASDAN"
    return None


def _g23(family: str, path: Path, root: Path = ROOT) -> dict | None:
    import subprocess
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as fh:
        out = Path(fh.name)
    r = subprocess.run(
        [sys.executable, str(ROOT / "_sownb/vb/tools/g23_period_load.py"),
         "--family", family, "--candidate", str(path), "--output", str(out)],
        capture_output=True, text=True, cwd=str(root))
    if r.returncode not in (0, 1) or not out.exists():
        return None
    try:
        return json.loads(out.read_text(encoding="utf-8"))
    finally:
        out.unlink(missing_ok=True)


def project(rep: dict, root: Path = ROOT) -> dict:
    rows = []
    with tempfile.TemporaryDirectory() as tmp:
        for r in rep["rows"]:
            if r["removable"] <= 0:
                continue
            fam = family_of(r["file"])
            if fam is None:
                rows.append({"file": r["file"], "family": None,
                             "note": "no family mapping; not projected"})
                continue
            src = root / r["file"]
            copy = Path(tmp) / Path(r["file"]).name
            copy.write_bytes(src.read_bytes())
            before = _g23(fam, src, root)
            dst.apply(copy)
            after = _g23(fam, copy, root)
            if not before or not after:
                rows.append({"file": r["file"], "family": fam,
                             "note": "g23 did not report; not projected"})
                continue
            rows.append({
                "file": r["file"], "family": fam,
                "wordsBefore": before["pupilWords"], "wordsAfter": after["pupilWords"],
                "familyMedian": before["familyMedian"],
                "ratioBefore": before["ratioToFamilyMedian"],
                "ratioAfter": after["ratioToFamilyMedian"],
                "verdictBefore": before["verdict"], "verdictAfter": after["verdict"],
                "statusBefore": before["ceilingVerdict"],
                "statusAfter": after["ceilingVerdict"],
                "clearsTheCeiling": (before["ceilingVerdict"] == "RED"
                                     and after["ceilingVerdict"] != "RED"),
                "reachesOperativeTarget": after["ratioToFamilyMedian"] <= 1.25,
            })
    scored = [r for r in rows if "ratioAfter" in r]
    return {
        "tool": "dedupe_sweep --project", "toolVersion": VERSION,
        "file": "tools/easter/dedupe_sweep.py",
        "subject": ("what de-duplication alone would do to each affected deck's g23 "
                    "period load, measured by copying the deck, deduping the COPY and "
                    "re-running the gate -- never by arithmetic on a word count"),
        "decksProjected": len(scored),
        "redBefore": sum(1 for r in scored if r["statusBefore"] == "RED"),
        "redAfter": sum(1 for r in scored if r["statusAfter"] == "RED"),
        "ceilingRedsCleared": sum(1 for r in scored if r["clearsTheCeiling"]),
        "reachOperativeTarget": sum(1 for r in scored if r["reachesOperativeTarget"]),
        "rows": rows,
    }


# --------------------------------------------------------------------------
# Controls
# --------------------------------------------------------------------------

CONTROL_IDS = [
    "a-planted-duplicated-deck-is-found",
    "a-clean-deck-is-not-reported",
    "a-non-deck-html-file-is-not-scanned",
    "the-repeat-factor-is-reported-not-just-the-word-count",
    "a-file-under-an-archived-directory-is-excluded-by-default",
    "the-same-file-is-included-when-archived-are-asked-for",
    "a-foreign-tree-is-never-scanned",
    "projection-leaves-the-source-file-byte-unchanged",
    "the-projection-reaches-a-family-mapped-deck",
    "a-deck-outside-every-family-mapping-is-reported-not-dropped",
]

_SENT = ("The furnace cooled overnight and the shift ended before the light came. ")
_DECK = ("<!doctype html><html><head><style>.slide{display:none}"
         ".slide.active{display:flex}</style></head><body><main class=\"deck\">"
         "<section class=\"slide active\" data-title=\"I Do 2 &#183; connect\">"
         "<p>%s</p></section></main></body></html>")


def _plant(d: Path, rel: str, repeats: int) -> Path:
    p = d / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(_DECK % (_SENT * repeats), encoding="utf-8")
    return p


def controls() -> list[dict]:
    out = []

    def rec(cid, description, expected, observed):
        out.append({"id": cid, "description": description, "expected": expected,
                    "observed": observed, "fired": expected == observed})

    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        _plant(d, "live/dup.html", 4)
        _plant(d, "live/clean.html", 1)
        _plant(d, "_approved0805/old.html", 4)
        _plant(d, "Games/game.html", 4)
        (d / "live/notes.html").write_text(
            "<!doctype html><html><body><p>%s</p></body></html>" % (_SENT * 4),
            encoding="utf-8")

        r = sweep(d)
        names = {row["file"] for row in r["rows"]}

        rec("a-planted-duplicated-deck-is-found",
            "a deck whose paragraph repeats one sentence four times is reported",
            True, "live/dup.html" in names)

        rec("a-clean-deck-is-not-reported",
            "a deck with no repeat contributes no row",
            True, "live/clean.html" not in names)

        rec("a-non-deck-html-file-is-not-scanned",
            "an html file with no stages is not a deck and is not counted as one",
            True, "live/notes.html" not in names)

        row = next((x for x in r["rows"] if x["file"] == "live/dup.html"), {})
        rec("the-repeat-factor-is-reported-not-just-the-word-count",
            "the histogram must name the factor, because x4 across many decks is "
            "a generator and x2 in one deck is a typo",
            {4: 1}, row.get("repeatFactors"))

        rec("a-file-under-an-archived-directory-is-excluded-by-default",
            "preserved copies must not be counted as live exposure",
            True, "_approved0805/old.html" not in names)

        r2 = sweep(d, include_archived=True)
        rec("the-same-file-is-included-when-archived-are-asked-for",
            "the exclusion is a scope choice, not a blind spot",
            True, "_approved0805/old.html" in {x["file"] for x in r2["rows"]})

        rec("a-foreign-tree-is-never-scanned",
            "Site/Games/Apps belong to another writer, in either scope",
            (True, True),
            ("Games/game.html" not in names,
             "Games/game.html" not in {x["file"] for x in r2["rows"]}))

        # The projection DEDUPES to learn what deduping would do. If it ever
        # edited the real file instead of the copy, the sweep would silently
        # become a writer -- so the invariant is a control, not a comment.
        #
        # THE FIRST VERSION OF THIS CONTROL WAS VACUOUS. It planted the deck at
        # live/dup.html, which family_of() does not recognise, so project()
        # appended a note and returned BEFORE reaching apply(). Planting a
        # source-writing mutation left the digest unchanged and the control
        # still fired green. The deck is now planted under a family-mapped path
        # so the apply is actually executed, and the mutation reds it.
        import hashlib
        mapped = _plant(d, "Science_Teesside/Build/W1_2026-27/SCI_B_dup.html", 4)
        digest_before = hashlib.sha256(mapped.read_bytes()).hexdigest()
        pj = project(sweep(d), root=d)
        rec("projection-leaves-the-source-file-byte-unchanged",
            "the projection edits a copy; a sweep that writes is not a sweep",
            digest_before, hashlib.sha256(mapped.read_bytes()).hexdigest())

        rec("the-projection-reaches-a-family-mapped-deck",
            "the byte-unchanged control above is only meaningful if apply() ran, "
            "so require the mapped deck to be projected rather than noted",
            (True, False),
            (any(r["file"].endswith("SCI_B_dup.html") for r in pj["rows"]),
             any(r["file"].endswith("SCI_B_dup.html") and "note" in r for r in pj["rows"])))

        rec("a-deck-outside-every-family-mapping-is-reported-not-dropped",
            "a deck the family map does not recognise must appear with a note, "
            "because a silently shorter list reads as a smaller problem",
            (True, True),
            (any(r["file"] == "live/dup.html" for r in pj["rows"]),
             all("note" in r for r in pj["rows"] if r["file"] == "live/dup.html")))

    return out


def self_test() -> dict:
    results = controls()
    ids = [r["id"] for r in results]
    missing = [c for c in CONTROL_IDS if c not in ids]
    extra = [c for c in ids if c not in CONTROL_IDS]
    return {"tool": "dedupe_sweep", "toolVersion": VERSION,
            "file": "tools/easter/dedupe_sweep.py",
            "controlsDeclared": len(CONTROL_IDS), "controlsRun": len(results),
            "controlsFired": sum(1 for r in results if r["fired"]),
            "missingControls": missing, "undeclaredControls": extra,
            "allListedControlsFired": not missing and not extra and all(r["fired"] for r in results),
            "controls": results}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output")
    ap.add_argument("--include-archived", action="store_true")
    ap.add_argument("--project", action="store_true")
    ap.add_argument("--list-controls", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()

    if a.list_controls:
        for c in CONTROL_IDS:
            print(c)
        return 0
    if a.self_test:
        rep = self_test()
        print(f"dedupe_sweep self-test  [{VERSION}]")
        for r in rep["controls"]:
            print(f"  {'ok  ' if r['fired'] else 'FAIL'} {r['id']:56s} "
                  f"expected={r['expected']} observed={r['observed']}")
        print(f"{rep['controlsFired']}/{rep['controlsRun']} controls fired")
        print("PASS" if rep["allListedControlsFired"] else "MEASUREMENT INVALID")
        return 0 if rep["allListedControlsFired"] else 1

    rep = sweep(include_archived=a.include_archived)
    print(f"dedupe sweep  [{VERSION}]  "
          f"{rep['decksScanned']} decks scanned, {rep['decksAffected']} affected")
    for r in rep["rows"]:
        print(f"  {r['removable']:6d}w  {r['file']}")
        print(f"          stages={r['stages']} {r['stageTitles']} factors={r['repeatFactors']}")
    print(f"  total removable {rep['wordsRemovableTotal']}w, "
          f"refused {rep['wordsRefusedTotal']}w")
    print(f"  repeat-factor histogram (sentences at each factor): "
          f"{rep['repeatFactorHistogram']}")
    if rep["unreadable"]:
        print(f"  {len(rep['unreadable'])} file(s) could not be analysed:")
        for u in rep["unreadable"][:10]:
            print(f"    {u['file']}: {u['error']}")
    if a.project:
        pj = sweep_projection = project(rep)
        print(f"\n  projection -- deduped on a COPY, g23 re-run, repository untouched")
        for r in pj["rows"]:
            if "ratioAfter" not in r:
                print(f"    -- {r['file']}: {r['note']}")
                continue
            mark = ("CLEARS" if r["clearsTheCeiling"]
                    else ("STILL RED" if r["statusAfter"] == "RED" else "      "))
            print(f"    {r['wordsBefore']:5d} -> {r['wordsAfter']:5d}w  "
                  f"x{r['ratioBefore']:<5} -> x{r['ratioAfter']:<5} "
                  f"{r['statusBefore']:4s} -> {r['statusAfter']:4s} {mark:9s} "
                  f"{Path(r['file']).name}")
        print(f"    {pj['decksProjected']} projected: ceiling reds {pj['redBefore']} -> "
              f"{pj['redAfter']} ({pj['ceilingRedsCleared']} cleared), "
              f"{pj['reachOperativeTarget']} reach the 1.25 operative target")
        rep["projection"] = pj

    if a.output:
        out = Path(a.output)
        out = out if out.is_absolute() else ROOT / out
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(rep, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
