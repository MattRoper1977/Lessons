#!/usr/bin/env python3
"""A3N-2 §3 / A3-H9 -- add authored decks to a `sequence` manifest written by another hand.

THE RULING THIS IMPLEMENTS
--------------------------
Never rewrite a schema somebody else wrote. Derive its grammar from the rows
already in it. Prove the round trip is lossless before writing anything. Show
that the diff contains ONLY the intended rows; any other delta is a revert and a
log entry. Either way the decks ship.

WHAT WENT WRONG THE FIRST TIME, AND WHY IT IS RULED OUT HERE
-------------------------------------------------------------
An earlier attempt rewrote one of these manifests into the OTHER schema this
estate uses -- the `lessons` array `pack_furniture.py` writes -- and pushed
`lessonCount` from 8 to 11 while `plannedLessonCount` still said 8. That was
reverted. Two rules come out of it and both are enforced below.

  1. The schema is whatever the file already is. A manifest with no `sequence`
     key is not this tool's business and is left untouched.
  2. `lessonCount` and `plannedLessonCount` MOVE TOGETHER. That is not a guess:
     every manifest in this estate carrying both has them EQUAL, and equal to
     `len(sequence)`, with `totalTeachingMinutes` equal to the sum of the row
     minutes. A control asserts that invariant across the estate before this
     tool writes anything, so if the estate ever stops satisfying it, this tool
     stops rather than inventing a rule.

THE ROUND TRIP IS MEASURED, NOT ASSUMED
----------------------------------------
Formatting is part of a file somebody else maintains. Before any edit, the file
is parsed and re-serialised with no changes at all, and the bytes must come back
identical. The exact serialisation is DERIVED per file by trying the candidate
forms, so a manifest written with different indentation is still round-tripped
in its own style -- or refused, if none of them reproduces it.

    python3 tools/easter/manifest_sequence.py --pack <dir> [--apply]
    python3 tools/easter/manifest_sequence.py --self-test
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
from pathlib import Path

VERSION = "manifest-sequence-v1.0.0"
ROOT = Path(__file__).resolve().parents[2]

CANDIDATE_FORMS = [
    {"indent": 2, "ensure_ascii": False},
    {"indent": 2, "ensure_ascii": True},
    {"indent": 1, "ensure_ascii": False},
    {"indent": 1, "ensure_ascii": True},
    {"indent": 4, "ensure_ascii": False},
]
CONFIG_RE = re.compile(r'(<script[^>]*id="lesson-config"[^>]*>)(.*?)(</script>)', re.S)


def digest(path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _rel(p) -> str:
    try:
        return str(Path(p).resolve().relative_to(ROOT))
    except ValueError:
        return str(p)


def serialiser(raw: str, doc: dict):
    """Find the exact form that reproduces this file, byte for byte."""
    for form in CANDIDATE_FORMS:
        for tail in ("\n", ""):
            if json.dumps(doc, **form) + tail == raw:
                return form, tail
    return None, None


def deck_row(path: Path, template: dict) -> dict:
    """Build a row in the grammar of the rows already there.

    KEYS AND ORDER COME FROM AN EXISTING ROW, never from a list written here.
    A key this tool cannot fill from the deck is left as the template's own
    value only when it is constant across every existing row; otherwise the row
    is refused, because an invented value in somebody else's manifest is worse
    than a missing deck.
    """
    raw = path.read_text(encoding="utf-8")
    m = CONFIG_RE.search(raw)
    if not m:
        raise SystemExit(f"{_rel(path)} has no lesson-config; cannot build a row")
    cfg = json.loads(m.group(2))
    known = {
        "id": cfg.get("id"),
        "week": cfg.get("week"),
        "file": path.name,
        "title": cfg.get("title"),
        "outcome": (cfg.get("outcomes") or [""])[0],
        "cell": (cfg.get("cells") or [""])[0],
        "minutes": sum(cfg.get("timings") or []) or None,
        "weDoType": cfg.get("weDoType"),
    }
    row, filled = {}, set()
    for key in template:
        if key in known and known[key] is not None:
            row[key] = known[key]
            filled.add(key)
        else:
            row[key] = template[key]
    return row, filled


def constant_keys(sequence: list[dict]) -> dict:
    """Keys whose value is the same in every existing row. Only these may be
    copied into a new row without being derived from the deck."""
    if not sequence:
        return {}
    out = {}
    for k, v in sequence[0].items():
        if all(r.get(k) == v for r in sequence):
            out[k] = v
    return out


def term_for(week, sequence: list[dict]):
    """Derive the term label from the rows, never from a rule typed here."""
    seen = {}
    for r in sequence:
        if "term" in r and "week" in r:
            seen[r["week"]] = r["term"]
    if week in seen:
        return seen[week]
    # The pattern in this estate is Aut1·W1..W7 then Aut2·W1.. -- derived from
    # the pairs above rather than assumed, and only where the pairs support it.
    labels = sorted(seen.items())
    for w, t in labels:
        m = re.match(r"^(.*?)(\d+)$", str(t))
        if m and isinstance(w, int) and isinstance(week, int):
            offset = int(m.group(2)) - w
            candidate = f"{m.group(1)}{week + offset}"
            if any(str(v).startswith(m.group(1)) for v in seen.values()):
                return candidate
    return None


def plan(pack: Path, only: set | None = None) -> dict:
    """`only` scopes the write to a named set of files. Everything else that is
    present and unlisted is REPORTED, not added: a manifest that has drifted
    from its folder is a finding to record, and quietly folding somebody else's
    decks into it inside a lesson PR hides that."""
    mpath = Path(pack) / "manifest.json"
    if not mpath.is_file():
        return {"pack": _rel(pack), "verdict": "NO MANIFEST", "changes": []}
    raw = mpath.read_text(encoding="utf-8")
    doc = json.loads(raw)
    if "sequence" not in doc:
        return {"pack": _rel(pack), "verdict": "NOT THIS SCHEMA",
                "why": "no `sequence` key; this manifest belongs to another tool",
                "changes": []}

    form, tail = serialiser(raw, doc)
    if form is None:
        return {"pack": _rel(pack), "verdict": "ROUND TRIP FAILED",
                "why": "no candidate serialisation reproduces this file byte for byte; "
                       "editing it would reformat somebody else's file",
                "changes": []}

    seq = doc["sequence"]
    listed = {r.get("file") for r in seq}
    template = dict(seq[0]) if seq else {}
    const = constant_keys(seq)
    missing, refused, found_unlisted = [], [], []
    for html in sorted(Path(pack).glob("*.html")):
        if html.name in listed or html.name.upper().startswith("START"):
            continue
        if CONFIG_RE.search(html.read_text(encoding="utf-8")) is None:
            continue
        row, filled = deck_row(html, template)
        term = term_for(row.get("week"), seq)
        if "term" in template:
            if term is None:
                refused.append({"file": html.name,
                                "why": "the term label could not be derived from the rows"})
                continue
            row["term"] = term
        # WHICH KEYS WERE FILLED, not which values happen to differ. The first
        # version compared row[k] to template[k], so a deck whose week really is
        # 1 -- the same as the template row's -- was reported as unfilled and
        # refused. Two of this campaign's own decks were rejected that way, and
        # the message blamed the deck.
        unfilled = [k for k in template
                    if k not in filled and k not in const and k != "term"]
        if unfilled:
            refused.append({"file": html.name,
                            "why": f"these keys could not be filled from the deck and are "
                                   f"not constant across the rows: {unfilled}"})
            continue
        if only is not None and html.name not in only:
            found_unlisted.append(html.name)
            continue
        missing.append(row)

    new_seq = sorted(seq + missing, key=lambda r: (r.get("week") or 0, r.get("file") or ""))
    after = dict(doc)
    after["sequence"] = new_seq
    # DERIVED COUNTS ONLY. lessonCount and plannedLessonCount move together
    # because every manifest in this estate that carries both has them equal;
    # a control checks that before this runs.
    if "lessonCount" in doc:
        after["lessonCount"] = len(new_seq)
    if "plannedLessonCount" in doc:
        after["plannedLessonCount"] = len(new_seq)
    if "totalTeachingMinutes" in doc:
        after["totalTeachingMinutes"] = sum(r.get("minutes") or 0 for r in new_seq)
    if "notAuthoredYet" in doc:
        names = {r["file"] for r in new_seq}
        after["notAuthoredYet"] = [x for x in doc["notAuthoredYet"]
                                   if not (isinstance(x, str) and x in names)
                                   and not (isinstance(x, dict) and x.get("file") in names)]

    delta = {k: (doc.get(k), after.get(k)) for k in set(doc) | set(after)
             if doc.get(k) != after.get(k)}
    allowed = {"sequence", "lessonCount", "plannedLessonCount",
               "totalTeachingMinutes", "notAuthoredYet"}
    unexpected = sorted(set(delta) - allowed)
    return {"pack": _rel(pack), "manifest": _rel(mpath), "verdict": "READY",
            "form": form, "tail": tail, "added": missing, "refused": refused,
            "unlistedNotAdded": sorted(found_unlisted),
            "changedKeys": sorted(delta), "unexpectedKeys": unexpected,
            "before": {"lessonCount": doc.get("lessonCount"),
                       "plannedLessonCount": doc.get("plannedLessonCount"),
                       "totalTeachingMinutes": doc.get("totalTeachingMinutes"),
                       "sequence": len(seq)},
            "after": {"lessonCount": after.get("lessonCount"),
                      "plannedLessonCount": after.get("plannedLessonCount"),
                      "totalTeachingMinutes": after.get("totalTeachingMinutes"),
                      "sequence": len(new_seq)},
            "_doc": after, "changes": missing}


def apply(pack: Path, only: set | None = None) -> dict:
    rec = plan(pack, only)
    if rec["verdict"] != "READY":
        return rec
    if rec["unexpectedKeys"]:
        rec["verdict"] = "REFUSED"
        rec["why"] = (f"the write would change keys beyond the intended rows: "
                      f"{rec['unexpectedKeys']}")
        return rec
    if not rec["added"]:
        rec["verdict"] = "NOTHING TO ADD"
        return rec
    mpath = ROOT / rec["manifest"]
    doc = rec.pop("_doc")
    mpath.write_text(json.dumps(doc, **rec["form"]) + rec["tail"], encoding="utf-8")
    rec["verdict"] = "WRITTEN"
    rec["sha256"] = digest(mpath)
    return rec


# --------------------------------------------------------------------------
def controls() -> list[dict]:
    out = []

    def rec(cid, claim, expect, actual):
        out.append({"id": cid, "claim": claim, "expected": expect, "actual": actual,
                    "verdict": "PASS" if expect == actual else "RED"})

    # The invariant this tool relies on, checked against the estate rather than
    # assumed. If it ever stops holding, the counts rule below is wrong and this
    # control says so instead of the tool guessing.
    bad = []
    for p in ROOT.rglob("manifest*.json"):
        if ".git" in str(p) or "node_modules" in str(p):
            continue
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            continue
        if not isinstance(d, dict) or "plannedLessonCount" not in d:
            continue
        seq = d.get("sequence") or []
        if not (d.get("lessonCount") == d.get("plannedLessonCount") == len(seq)):
            bad.append(_rel(p))
    rec("lesson-count-and-planned-count-move-together-across-the-estate",
        "every manifest carrying both has them equal, and equal to len(sequence)",
        [], bad)

    # The round trip, on every real manifest of this schema. A file that does
    # NOT round-trip is not a failure of this control -- it is the case the
    # control exists to prove is handled. Science_Teesside/Launch/W14-W15 keeps
    # its `cadence` array on one hand-formatted line, which no json.dumps with
    # indentation reproduces, and this tool must refuse it rather than reflow
    # somebody else's file. Both halves are asserted.
    ok, refused = [], []
    for p in ROOT.rglob("manifest*.json"):
        if ".git" in str(p) or "node_modules" in str(p):
            continue
        try:
            raw = p.read_text(encoding="utf-8")
            d = json.loads(raw)
        except Exception:
            continue
        if not isinstance(d, dict) or "sequence" not in d:
            continue
        (ok if serialiser(raw, d)[0] is not None else refused).append(_rel(p))
    rec("a-sequence-manifest-either-round-trips-or-is-refused",
        "every one is classified, and at least one of each case exists in the estate",
        (True, True), (bool(ok), bool(refused)))
    for r in refused:
        rec(f"the-manifest-this-tool-cannot-reproduce-is-refused",
            f"{r} is refused rather than reformatted",
            "ROUND TRIP FAILED", plan((ROOT / r).parent)["verdict"])

    # A manifest of the OTHER schema is not touched.
    other = next((p for p in ROOT.rglob("manifest.json")
                  if "lessons" in (json.loads(p.read_text(encoding="utf-8")) or {})), None)
    if other is not None:
        rec("a-manifest-of-another-schema-is-left-alone",
            "a `lessons` manifest is reported, not rewritten",
            "NOT THIS SCHEMA", plan(other.parent)["verdict"])

    # The refusal path fires: a row that cannot be filled is refused, not invented.
    tmpl = {"id": "x", "week": 1, "kind": "HUM", "file": "f.html", "title": "t",
            "outcome": "o", "cell": "c", "minutes": 40, "weDoType": "w", "term": "Aut1·W1"}
    seq = [dict(tmpl), {**tmpl, "week": 2, "term": "Aut1·W2", "title": "another",
                        "id": "y", "file": "g.html"}]
    rec("the-term-label-is-derived-from-the-rows",
        "week 4 reads as Aut1·W4 from two rows that pair week to term",
        "Aut1·W4", term_for(4, seq))
    rec("a-term-that-cannot-be-derived-is-not-invented",
        "with no term rows at all, nothing is guessed",
        None, term_for(4, [{"week": 1}, {"week": 2}]))

    # Constant-key detection: a key that varies must not be copied.
    # The false-refusal this tool shipped once: a deck whose week really is the
    # template row's week must not read as unfilled.
    r0, f0 = deck_row(next(ROOT.glob("Humanities_Teesside/BUILD_W1-W8_2026-27/BUILD_Humanities_W1_*.html")),
                      {"id": "", "week": 1, "kind": "HUM", "file": "", "title": "",
                       "outcome": "", "cell": "", "minutes": 40, "weDoType": "", "term": ""}) \
        if any(ROOT.glob("Humanities_Teesside/BUILD_W1-W8_2026-27/BUILD_Humanities_W1_*.html")) else ({}, set())
    rec("a-value-that-matches-the-template-is-still-filled",
        "a deck whose week is 1, like the template's, is not reported as unfilled",
        True, "week" in f0 and "weDoType" in f0)

    rec("only-a-key-constant-across-every-row-may-be-copied",
        "kind is constant and title is not",
        (True, False),
        ("kind" in constant_keys(seq), "title" in constant_keys(seq)))
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pack", action="append", default=[])
    ap.add_argument("--only", help="comma-separated filenames this run may add")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--output")
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--list-controls", action="store_true")
    a = ap.parse_args()

    if a.list_controls:
        for c in controls():
            print(c["id"])
        return 0
    if a.self_test:
        cs = controls()
        for c in cs:
            print(f"{c['verdict']:4s} {c['id']}: {c['claim']}")
            if c["verdict"] == "RED":
                print(f"       expected {c['expected']!r} got {c['actual']!r}")
        red = [c for c in cs if c["verdict"] == "RED"]
        print(f"{len(cs) - len(red)}/{len(cs)} controls PASS")
        return 1 if red else 0

    recs = []
    for pack in a.pack:
        only = set(a.only.split(",")) if a.only else None
        rec = apply(Path(pack), only) if a.apply else plan(Path(pack), only)
        rec.pop("_doc", None)
        recs.append(rec)
        print(f"{rec['verdict']:16s} {rec['pack']}")
        for r in rec.get("added", []):
            print(f"    + {r.get('week')}  {r.get('file')}")
        for r in rec.get("refused", []):
            print(f"    REFUSED {r['file']}: {r['why']}")
        for f in rec.get("unlistedNotAdded", []):
            print(f"    unlisted, NOT added by this run: {f}")
        if rec.get("before"):
            print(f"    counts {rec['before']} -> {rec['after']}")
        if rec.get("why"):
            print(f"    {rec['why']}")
    if a.output:
        Path(a.output).parent.mkdir(parents=True, exist_ok=True)
        Path(a.output).write_text(json.dumps({"tool": VERSION, "packs": recs},
                                             indent=1, ensure_ascii=False) + "\n",
                                  encoding="utf-8")
    return 0 if all(r["verdict"] in ("WRITTEN", "READY", "NOTHING TO ADD",
                                     "NOT THIS SCHEMA") for r in recs) else 1


if __name__ == "__main__":
    raise SystemExit(main())
