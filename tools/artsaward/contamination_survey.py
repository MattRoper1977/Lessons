#!/usr/bin/env python3
"""The contamination list. ORDER AAE §9 -- per level, requirement -> served by
-> evidence route -> verdict, plus every contradiction with deck and line.

WHY THIS IS A SURVEY AND NOT A GATE
------------------------------------
g30-g35 read the level from the deck's own `artsAward` declaration and refuse to
guess. That is right for a gate: a deck that does not say what it is does not
get judged as though it had. But nothing in this estate declares yet -- the
register landed today -- so a gate can only report "76 decks declare nothing",
which is one fact and not a list.

This tool INFERS the level from the deck's text so the contamination list has
something in it, and every row it produces says `inferred` so nobody mistakes it
for a verdict. An inference is a place to look, not a finding.

    python3 tools/artsaward/contamination_survey.py --out docs/ARTS_AWARD_BSG_CHECK.md
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
from collections import defaultdict
from pathlib import Path

VERSION = "arts-award-contamination-survey-v1.0.0"
ROOT = Path(__file__).resolve().parents[2]
SPEC_PATH = ROOT / "tools/artsaward/SPEC.json"

_g = importlib.util.spec_from_file_location(
    "g30_arts_award", ROOT / "_sownb/vb/tools/g30_arts_award.py")
g30 = importlib.util.module_from_spec(_g)
_g.loader.exec_module(g30)

LEVEL_PAT = {
    "Explore": re.compile(r"\b(?:Explore\s+Arts\s+Award|Arts\s+Award\s+Explore|"
                          r"Entry\s*Level\s+Award\s+in\s+the\s+Arts)\b", re.I),
    "Bronze": re.compile(r"\b(?:Bronze\s+Arts\s+Award|Arts\s+Award\s+Bronze|"
                         r"Level\s*1\s+Award\s+in\s+the\s+Arts)\b", re.I),
    "Silver": re.compile(r"\b(?:Silver\s+Arts\s+Award|Arts\s+Award\s+Silver|"
                         r"Level\s*2\s+Award\s+in\s+the\s+Arts)\b", re.I),
    "Gold": re.compile(r"\b(?:Gold\s+Arts\s+Award|Arts\s+Award\s+Gold|"
                       r"Level\s*3\s+Certificate\s+in\s+the\s+Arts)\b", re.I),
}


def digest(p) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def infer(raw: str) -> tuple[str | None, dict]:
    text = g30.deck_text(raw, pupil_only=False)
    hits = {lvl: len(pat.findall(text)) for lvl, pat in LEVEL_PAT.items()}
    hits = {k: v for k, v in hits.items() if v}
    if len(hits) == 1:
        return next(iter(hits)), hits
    return None, hits


def lines_of(path: Path, needle: re.Pattern) -> list[tuple[int, str]]:
    out = []
    for i, line in enumerate(path.read_text(encoding="utf-8", errors="replace")
                             .splitlines(), 1):
        if needle.search(line):
            out.append((i, " ".join(line.split())[:120]))
    return out


CONTRADICTIONS = [
    ("a level name that is not this deck's level",
     lambda lvl, sp: re.compile(
         "|".join(re.escape(v["rqfLevel"]) for k, v in sp["levels"].items() if k != lvl),
         re.I)),
    ("a qualification number that is not this deck's",
     lambda lvl, sp: re.compile(
         "|".join(re.escape(v["qualificationNumber"])
                  for k, v in sp["levels"].items() if k != lvl))),
    ("UCAS outside Gold",
     lambda lvl, sp: re.compile(r"\bUCAS\b", re.I) if lvl != "Gold" else None),
    ("'leadership' in an Explore deck",
     lambda lvl, sp: re.compile(r"\bleadership\b", re.I) if lvl == "Explore" else None),
    ("a dated event inside the deck",
     lambda lvl, sp: g30.DATE_HINT),
    ("a visit asserted in the deck",
     lambda lvl, sp: g30.VENUE_HINT),
    ("a requirement the register does not carry",
     lambda lvl, sp: re.compile(r"\b(signed witness statement|Gantt chart)\b", re.I)),
    ("a venue named in the deck rather than in SLOTS.json",
     lambda lvl, sp: _venue_pattern()),
]


def _venue_pattern():
    slots_path = ROOT / "tools/artsaward/SLOTS.json"
    if not slots_path.is_file():
        return None
    names = [c["name"] for c in
             (json.loads(slots_path.read_text(encoding="utf-8")).get("candidates") or [])]
    return re.compile("|".join(rf"\b{re.escape(n)}\b" for n in names)) if names else None


# MUST FIRE. A survey that reports nothing has to be shown capable of reporting
# something, or "no contradiction found" means "the patterns are broken". The
# first version's whole list was 191 hits on the word "ticket" -- every deck in
# this estate ends on a stage called Exit Ticket -- so it was reporting garbage;
# tightening it to an ASSERTED attendance took the list to zero, and a zero from
# a pattern that has just been narrowed is exactly the number to distrust.
def self_test() -> list[dict]:
    import tempfile
    out = []

    def rec(cid, claim, expect, actual):
        out.append({"id": cid, "claim": claim, "expected": expect, "actual": actual,
                    "verdict": "PASS" if expect == actual else "RED"})

    def planted(body: str) -> dict:
        src = ('<!doctype html><html><body><main class="deck">'
               '<section class="slide">' + body + "</section></main></body></html>")
        fh = tempfile.NamedTemporaryFile("w", suffix=".html", delete=False,
                                         encoding="utf-8")
        fh.write(src)
        fh.close()
        return survey([fh.name])

    d = planted("<p>Your Bronze Arts Award. When we visit MIMA on 14th November, "
                "bring your ticket. You must produce a Gantt chart.</p>")
    kinds = {c["what"] for r in d["rows"] for c in r["contradictions"]}
    rec("the-survey-can-still-find-something",
        "a planted deck asserting a visit, a date, a venue and an invented "
        "requirement is reported on all four",
        4, len(kinds))

    clean = planted("<p>Your Bronze Arts Award. Keep your ticket as evidence. "
                    "Write what you thought of the event on your exit ticket.</p>")
    rec("a-ticket-kept-as-evidence-is-not-a-contradiction",
        "the register keeps ticket, programme, photo and URL as primary evidence, "
        "and every deck in this estate ends on a stage called Exit Ticket",
        0, sum(len(r["contradictions"]) for r in clean["rows"]))
    return out


def survey(files: list[str]) -> dict:
    sp = json.loads(SPEC_PATH.read_text(encoding="utf-8"))
    rows, by_level = [], defaultdict(list)
    for f in files:
        p = Path(f)
        raw = p.read_text(encoding="utf-8", errors="replace")
        scoped, aa, _why = g30.in_scope(raw)
        if not scoped:
            continue
        declared_level = (aa or {}).get("level")
        lvl, hits = infer(raw)
        # The fourth time this campaign has hit relative_to on a temp path.
        try:
            rel = str(p.resolve().relative_to(ROOT))
        except ValueError:
            rel = str(p)
        row = {"file": rel,
               "declaredLevel": declared_level,
               "inferredLevel": lvl, "levelWordCounts": hits,
               "contradictions": []}
        use = declared_level or lvl
        if use:
            for name, mk in CONTRADICTIONS:
                pat = mk(use, sp)
                if pat is None:
                    continue
                for ln, txt in lines_of(p, pat):
                    row["contradictions"].append(
                        {"what": name, "line": ln, "text": txt})
            by_level[use].append(row)
        rows.append(row)
    return {"tool": VERSION, "specSha256": digest(SPEC_PATH),
            "scanned": len(files), "inScope": len(rows),
            "byLevel": {k: len(v) for k, v in by_level.items()},
            "undeclared": sum(1 for r in rows if not r["declaredLevel"]),
            "withContradictions": sum(1 for r in rows if r["contradictions"]),
            "rows": rows}


def markdown(doc: dict) -> str:
    sp = json.loads(SPEC_PATH.read_text(encoding="utf-8"))
    L = []
    a = L.append
    a("# Arts Award — what the estate serves, and what contradicts the register")
    a("")
    a(f"Generated by `tools/artsaward/contamination_survey.py` ({VERSION}) against")
    a(f"`tools/artsaward/SPEC.json` sha256 `{doc['specSha256'][:16]}`. Re-runnable.")
    a("")
    a("## Read this first")
    a("")
    a("The register landed with this document, so **nothing in the estate declares")
    a("against it yet**: every deck below is `UNDECLARED`, and the level in each row")
    a("is **inferred from the deck's own words**, not read from a declaration. An")
    a("inference is a place to look, not a verdict. g30–g35 refuse to guess a level;")
    a("this survey guesses on purpose so the list has something in it.")
    a("")
    a(f"- deck-shaped files naming the Arts Award: **{doc['inScope']}**")
    a(f"- declaring an `artsAward` block: **{doc['inScope'] - doc['undeclared']}**")
    a(f"- carrying at least one contradiction: **{doc['withContradictions']}**")
    a("")
    a("## Requirement → served by → evidence route → verdict")
    a("")
    for lvl, ref in sp["levels"].items():
        a(f"### {lvl} — {ref['title']} ({ref['qualificationNumber']})")
        a("")
        a("| part | requirement | served by | evidence route | verdict |")
        a("|---|---|---|---|---|")
        for pid, part in ref["parts"].items():
            req = (part.get("requires") or part["name"])
            req = req if len(req) < 90 else req[:87] + "…"
            a(f"| {pid} | {part['name']} — {req} | _not yet served_ | — | **OPEN** |")
        a("")
    a("Every row reads OPEN because no deck in this estate declares a part against")
    a("the register yet. The rows fill in as decks are authored or repaired with an")
    a("`artsAward` block naming the parts they serve; g30–g35 then bind them.")
    a("")
    a("## Contamination list — deck and line")
    a("")
    hits = [r for r in doc["rows"] if r["contradictions"]]
    if not hits:
        a("No contradiction found by this survey. That is not a clean bill: the survey")
        a("checks the level facts, the leadership rule, dated events, asserted visits")
        a("and two invented requirements. It does not read for meaning.")
    else:
        for r in sorted(hits, key=lambda r: -len(r["contradictions"]))[:60]:
            a(f"**{r['file']}** — inferred {r['inferredLevel'] or 'ambiguous'}"
              f" ({len(r['contradictions'])})")
            a("")
            for c in r["contradictions"][:6]:
                a(f"- line {c['line']}: {c['what']} — `{c['text']}`")
            if len(r["contradictions"]) > 6:
                a(f"- …and {len(r['contradictions']) - 6} more in this file")
            a("")
        if len(hits) > 60:
            a(f"…and {len(hits) - 60} further files. The JSON beside this document")
            a("carries every row; nothing is truncated there.")
    a("")
    a("## What this survey does not do")
    a("")
    a("It does not read a deck for meaning. A deck can teach the wrong thing under")
    a("the right heading and pass every pattern here. That is what the gates are for,")
    a("once a deck declares what it is.")
    return "\n".join(L) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="*")
    ap.add_argument("--out")
    ap.add_argument("--json")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()
    if a.self_test:
        cs = self_test()
        for c in cs:
            print(f"{c['verdict']:4s} {c['id']}: {c['claim']}")
            if c["verdict"] == "RED":
                print(f"       expected {c['expected']!r} got {c['actual']!r}")
        red = [c for c in cs if c["verdict"] == "RED"]
        print(f"{len(cs) - len(red)}/{len(cs)} controls PASS")
        return 1 if red else 0
    files = a.files or [str(p) for p in ROOT.rglob("*.html")
                        if "node_modules" not in str(p)
                        and "Arts Award" in p.read_text(encoding="utf-8", errors="replace")]
    doc = survey(files)
    print(f"{VERSION}: {doc['inScope']} deck-shaped Arts Award files, "
          f"{doc['undeclared']} undeclared, {doc['withContradictions']} with "
          f"contradictions; by inferred level {doc['byLevel']}")
    if a.out:
        Path(a.out).parent.mkdir(parents=True, exist_ok=True)
        Path(a.out).write_text(markdown(doc), encoding="utf-8")
        print(f"wrote {a.out}")
    if a.json:
        Path(a.json).parent.mkdir(parents=True, exist_ok=True)
        Path(a.json).write_text(json.dumps(doc, indent=1) + "\n", encoding="utf-8")
        print(f"wrote {a.json}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
