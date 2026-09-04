#!/usr/bin/env python3
"""Coverage counted PER WORKBOOK CELL (ORDER VB-RUN13 R0/R1).

THE PRINCIPLE. Coverage is counted per workbook cell, never per week and never
per file. A week is a property of a cell, taken from the cell's own term-relative
position through the ruled spine. Nothing here reads a week from a filename, a
folder name, or CALENDAR_SPINE's absoluteWeek column -- g27 enforces that.

TWO READINGS, as R1 defines them:
  path     a cell is claimed when some deck's TRACE names it.
  content  a cell is covered when a deck's trace names it AND that deck's text
           actually serves the cell's outcome.
The readback carries the CONTENT number. Path is secondary.

WHERE A CLAIM COMES FROM. A deck's trace is the pack manifest row for it, its own
lesson-config block, and any workbook cell reference in its body. All three are
read; a claim from any of them counts.

WHAT "SERVES" MEANS, and how the threshold was measured rather than chosen. Take
the cell's verbatimOutcome, reduce it to distinctive content words -- stopwords
removed, lightly stemmed, and any word carried by more than 35% of the corpus
dropped, because a word every deck contains cannot evidence a match. SERVES is
the fraction of those words present in the deck's pupil-facing text.

The threshold comes from a measured separation, not a preference:
  positives  the (deck, cell) pairs the estate's own traces assert: 89 pairs,
             median score 1.00
  negatives  pairs from a different lane, which cannot be right: 2413 pairs,
             90th percentile 0.333
  at 0.85    recall 0.820 on the asserted pairs, false-positive rate 0.0058
The 18% of asserted pairs that fall below it are not noise to be tuned away:
they are the TRACE CORRECTION candidates R1 asks for -- a claim whose content
does not serve it.

THREE DIFFERENCE CLASSES, per R1:
  TRACE CORRECTION  a trace claims a cell its own text does not serve
  AUTHORING GAP     a deck's text serves a cell no trace claims
  DUPLICATE         two decks claim one cell; the elder keeps it

An AUTHORING GAP is held to a higher bar than a claim, because it is asserted
without a trace to stand on: same lane, at least three distinctive outcome words,
at or above threshold, and a single best-matching deck. A gap is a trace row to
add, not a lesson to build.

Usage: cell_coverage.py [--output <report.json>] [--threshold 0.85]
"""
from __future__ import annotations

import argparse
import collections
import json
import re
import subprocess
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SPINE = ROOT / "_sownb/CALENDAR_SPINE.json"

# The ruled spine, ORDER VB-RUN11F / VB-RUN13. A week comes from the cell's own
# term-relative label through this map, and from nowhere else.
TERM_OFFSET = {"Aut1": 0, "Aut2": 8, "Spr1": 15, "Spr2": 21, "Sum1": 26, "Sum2": 33}
# RUN11F/RUN13 name two positions that carry no teaching week: Spring 2 has five
# timetabled weeks so its sixth column is NOT-TIMETABLED, and absolute 8 is the
# enrichment week with no workbook row. Without this, Spr2 W6 arithmetics to 27
# and collides with Summer 1 week 1.
NOT_TIMETABLED = {"Spr2·W6"}

ROOTS = ["BUILD_ASDAN", "GROW_ASDAN", "LAUNCH_ASDAN", "Science_Teesside",
         "Humanities_Teesside", "Art_Teesside", "Build/Slideshows", "Grow/Slideshows", "Launch/Slideshows"]
REF = re.compile(r"'(?:BUILD|GROW|LAUNCH) Weekly - (?:Autumn|Spring|Summer)'!C\d+")
SCRIPT = re.compile(r"<(script|style|svg)\b.*?</\1>", re.S | re.I)
TAG = re.compile(r"<[^>]+>")
CONFIG = re.compile(r'<script id="lesson-config"[^>]*>(.*?)</script>', re.S)

STOP = set("""a an the and or but if then than that this these those of in on at to for with without from by as is are
was were be been being it its it's do does did doing have has had having i you he she they we my your our their them us
me one two three four five six seven eight nine ten new own can will would should could may might must not no yes so
up down out over under more most less least each every some any all both few many much other another same different
next last first second third about into onto after before during while when where which who whom whose what how why
also just only very too still even now today week weeks lesson lessons pupils pupil learner learners class classes""".split())


def ruled_week(cell: dict):
    tw = cell.get("termWeek") or ""
    if tw in NOT_TIMETABLED:
        return "NOT-TIMETABLED"
    m = re.match(r"(Aut[12]|Spr[12]|Sum[12])\D+(\d+)", tw)
    return TERM_OFFSET[m.group(1)] + int(m.group(2)) if m else None


def words(text: str) -> list[str]:
    return [w for w in re.findall(r"[a-z']+", text.lower()) if len(w) > 2 and w not in STOP]


def stem(w: str) -> str:
    for suf in ("ing", "edly", "ed", "es", "s"):
        if w.endswith(suf) and len(w) - len(suf) >= 4:
            return w[: -len(suf)]
    return w


# A cell may legitimately carry more than one deck. Science is taught as a
# sequence -- Explore/Do for BUILD and GROW, Introduce/Explore/Do for LAUNCH --
# so a Science cell with two or three decks is the shape the contract asks for,
# not a duplicate. Everything else is one deck to a cell.
EXPECTED_DECKS = {("BUILD", "Science"): 2, ("GROW", "Science"): 2, ("LAUNCH", "Science"): 3}

# Only a LESSON claims a cell. A hub, a start page, a scheme of work or a
# planning sheet names many cells because that is its job; counting those as
# claims made 17 of the first 18 "trace corrections" one evidence-tracker page.
SUPPORT_NAME = re.compile(
    r"(START_HERE|Scheme_of_Work|_Hub\b|index|manifest|Resources_and_Tools"
    r"|TEACHER_PLANNING|_SOW\b|SAME_DAY_EVIDENCE|CONTRAST_MANIFEST)", re.I)


def is_lesson(path: str, raw: str) -> bool:
    if SUPPORT_NAME.search(path.split("/")[-1]):
        return False
    return raw.count('class="slide') >= 9 or "data-mbm-guide" in raw


def subject_of(path: str) -> str | None:
    if "ASDAN" in path:
        return "ASDAN"
    for prefix, subject in (("Science_", "Science"), ("Humanities_", "Humanities"), ("Art_", "Art")):
        if path.startswith(prefix):
            return subject
    m = re.match(r"(?:BUILD|GROW|LAUNCH)_(ART|HUM|DT|L1)_", path.split("/")[-1])
    if m:
        return {"ART": "Art", "HUM": "Humanities", "DT": None, "L1": "ASDAN"}[m.group(1)]
    return None


def lane_of(path: str) -> str | None:
    p = path.upper()
    for lane in ("BUILD", "GROW", "LAUNCH"):
        if p.startswith(lane) or f"/{lane}" in p or f"{lane}_" in p:
            return lane
    return None


def body_claims(raw: str, known_cells) -> tuple[set[str], list[dict]]:
    """Read the same reference whether its apostrophes are literal or escaped.

    BUILD's Autumn 2 source paragraphs use &#x27;. Reading the HTML bytes as
    plain text hid their current-outcome references and sent existing lessons
    back to the authoring queue. Decode once, as HTML does; a printed entity
    example encoded twice must not become a claim. This changes reference
    recognition only, not the content threshold or the ruled calendar.
    """
    found = set(REF.findall(unescape(raw)))
    excluded = [{'reference': ref, 'reason': 'reference absent from the scoped workbook-cell inventory'}
                for ref in sorted(found) if ref not in known_cells]
    return found.intersection(known_cells), excluded


def controls() -> list[dict]:
    ref = "'BUILD Weekly - Autumn'!C137"
    rows = []
    def check(cid, expected, actual):
        rows.append({'id': cid, 'expected': expected, 'actual': actual, 'fired': expected == actual})
    for name, quote in [('literal', "'"), ('hex', '&#x27;'), ('decimal', '&#39;'), ('named', '&apos;')]:
        raw = '<p>Source: '+ref.replace("'", quote)+'</p>'
        check(name+'-apostrophes-read-the-same-cell', [ref], sorted(body_claims(raw, {ref})[0]))
    check('double-escaped-example-is-not-a-reference', [],
          sorted(body_claims(ref.replace("'", '&amp;#x27;'), {ref})[0]))
    check('screen-and-print-copy-claim-once', [ref], sorted(body_claims(ref+ref, {ref})[0]))
    kept, excluded = body_claims(ref, set())
    check('unknown-cell-is-excluded-with-a-reason', ([], 1, True),
          (sorted(kept), len(excluded), all(bool(e['reason']) for e in excluded)))
    check('neighbour-outcome-text-is-not-a-cell-claim', [],
          sorted(body_claims('<p>Feeds next: Wash up / clean up after an activity.</p>', {ref})[0]))
    actual = ROOT/'BUILD_ASDAN/Autumn2_W1-W6_2026-27/BUILD_ASDAN_A2_PFA_W1_Plan_a_Simple_Healthy_Snack.html'
    check('shipped-snack-plan-keeps-its-current-cell', [ref], sorted(body_claims(actual.read_text(), {ref})[0]))
    return rows


def load() -> tuple[dict, list[str], dict, dict]:
    spine = json.loads(SPINE.read_text())
    cells = {c["reference"]: c for c in spine["workbookCells"]}
    listing = subprocess.run(
        ["bash", "-c", "cd %s && find %s -name '*.html' | sort" % (ROOT, " ".join(ROOTS))],
        capture_output=True, text=True).stdout.split()

    claims: dict[str, set[str]] = collections.defaultdict(set)
    source: dict[tuple[str, str], set[str]] = collections.defaultdict(set)
    for man in ROOT.rglob("manifest.json"):
        if "/.git/" in str(man):
            continue
        try:
            m = json.loads(man.read_text())
        except Exception:
            continue
        if not isinstance(m, dict):
            continue
        for lesson in m.get("lessons", []):
            if not isinstance(lesson, dict) or "file" not in lesson:
                continue
            rel = str((man.parent / lesson["file"]).relative_to(ROOT))
            for c in lesson.get("cells", []):
                ref = c.get("reference")
                if ref in cells:
                    claims[rel].add(ref)
                    source[(rel, ref)].add("manifest")

    # The spine carries an AUDITED second-instrument reading per deck:
    # existingHtml[].contentCellReferences, each with its own secondInstrumentEvidence
    # and a spineStatus. That is a real trace, not a proxy, so it counts as a claim.
    # The spine's own spineStatus says how far each audited reading got.
    # ALIGNED and SPINE-SPLIT resolved to a cell and are claims. MULTI means the
    # audit could NOT pick between several cells, and MEASUREMENT INVALID means it
    # could not read the deck at all; counting either as a claim would turn the
    # audit's honesty about its own limits into false coverage. They are recorded
    # separately so nothing is silently dropped.
    ambiguous = []
    for e in spine.get("existingHtml", []):
        status = e.get("spineStatus", "?")
        refs = [r for r in (e.get("contentCellReferences") or []) if r in cells]
        if status in ("ALIGNED", "SPINE-SPLIT"):
            for ref in refs:
                claims[e["path"]].add(ref)
                source[(e["path"], ref)].add(f"spine-audited/{status}")
        elif refs:
            ambiguous.append({"deck": e["path"], "spineStatus": status, "cells": sorted(refs),
                              "reason": ("the spine's own audit did not resolve this deck to a single cell, so its "
                                         "references are recorded and not counted as claims")})

    text: dict[str, str] = {}
    excluded_body_claims = []
    lessons: set[str] = set()
    for f in listing:
        raw = (ROOT / f).read_text(encoding="utf-8", errors="ignore")
        if not is_lesson(f, raw):
            text[f] = TAG.sub(" ", SCRIPT.sub(" ", raw))
            continue
        lessons.add(f)
        body_refs, excluded = body_claims(raw, cells)
        excluded_body_claims.extend({'deck': f, **row} for row in excluded)
        for ref in body_refs:
            claims[f].add(ref)
            source[(f, ref)].add("body")
        cfg = CONFIG.search(raw)
        if cfg:
            try:
                j = json.loads(cfg.group(1))
                for c in (j.get("cells") or []):
                    if isinstance(c, str) and c in cells:
                        claims[f].add(c)
                        source[(f, c)].add("lesson-config")
            except Exception:
                pass
        text[f] = TAG.sub(" ", SCRIPT.sub(" ", raw))
    return cells, listing, claims, {"source": source, "text": text, "lessons": lessons,
                                   "ambiguous": ambiguous, "excludedBodyClaims": excluded_body_claims}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output")
    ap.add_argument("--threshold", type=float, default=0.85)
    ap.add_argument("--list-controls", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()

    if args.list_controls or args.self_test:
        rows = controls()
        if args.list_controls:
            print('\n'.join(r['id'] for r in rows))
            return 0
        fired = sum(r['fired'] for r in rows)
        report = {'file': '_sownb/vb/tools/cell_coverage.py', 'controls': rows,
                  'controlsRun': len(rows), 'controlsFired': fired,
                  'allListedControlsFired': fired == len(rows)}
        if args.output:
            out = Path(args.output)
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(json.dumps(report, indent=1)+'\n')
        print(f'{fired}/{len(rows)} controls fired')
        return 0 if fired == len(rows) else 1

    cells, listing, claims, extra = load()
    text, source, lessons = extra["text"], extra["source"], extra["lessons"]
    ambiguous = [a for a in extra["ambiguous"]]
    claims = {d: refs for d, refs in claims.items() if d in lessons}
    tokens = {f: set(stem(w) for w in words(t)) for f, t in text.items()}
    df = collections.Counter()
    for toks in tokens.values():
        df.update(toks)
    n_decks = len(tokens)

    def outcome_words(ref: str) -> list[str]:
        ow = [stem(w) for w in words(cells[ref].get("verbatimOutcome") or "")]
        return [w for w in dict.fromkeys(ow) if df.get(w, 0) < 0.35 * n_decks]

    def serves(deck: str, ref: str) -> tuple[float | None, int]:
        ow = outcome_words(ref)
        if not ow:
            return None, 0
        return sum(1 for w in ow if w in tokens.get(deck, ())) / len(ow), len(ow)

    in_scope = {r: c for r, c in cells.items() if c.get("scopeStatus") == "IN_SCOPE"}
    claimed_by: dict[str, list[str]] = collections.defaultdict(list)
    for deck, refs in claims.items():
        for r in refs:
            if r in in_scope:
                claimed_by[r].append(deck)

    trace_corrections, duplicates, covered, unscorable = [], [], set(), []
    for ref, decks in sorted(claimed_by.items()):
        served = []
        for d in decks:
            s, n = serves(d, ref)
            if s is not None and s >= args.threshold:
                served.append((d, round(s, 3)))
            elif s is None:
                unscorable.append({
                    "class": "UNSCORABLE", "cell": ref, "deck": d,
                    "ruledWeek": ruled_week(cells[ref]),
                    "outcome": (cells[ref].get("verbatimOutcome") or "")[:120],
                    "reason": ("this cell's outcome has no distinctive words left after stopwords and "
                               "corpus-ubiquitous terms are removed, so SERVES cannot be evaluated either "
                               "way. Counted as neither covered nor a correction, and named here so the "
                               "difference between the path and content numbers is fully accounted for")})
            else:
                trace_corrections.append({
                    "class": "TRACE CORRECTION", "cell": ref, "deck": d,
                    "ruledWeek": ruled_week(cells[ref]), "score": round(s, 3),
                    "distinctiveWords": n, "claimSource": sorted(source[(d, ref)]),
                    "outcome": (cells[ref].get("verbatimOutcome") or "")[:120],
                    "reason": "the trace claims this cell and the deck's own text does not serve its outcome"})
        if served:
            covered.add(ref)
        cell = cells[ref]
        expected = EXPECTED_DECKS.get((cell.get("lane"), cell.get("subject")), 1)
        if len(decks) > expected:
            duplicates.append({
                "class": "DUPLICATE", "cell": ref, "ruledWeek": ruled_week(cells[ref]),
                "decks": sorted(decks), "servedBy": served, "expectedDecks": expected,
                "reason": ("more decks claim this cell than its family takes (Science is a sequence, so two "
                           "for BUILD and GROW and three for LAUNCH are correct); the elder keeps it, the "
                           "younger's claim is removed and its deck is recorded as ORPHAN CONTENT, never deleted")})

    gaps = []
    for ref, cell in sorted(in_scope.items()):
        if ref in claimed_by:
            continue
        ow = outcome_words(ref)
        if len(ow) < 3:
            continue
        best = []
        for d in sorted(lessons):
            if lane_of(d) != cell.get("lane"):
                continue
            if cell.get("subject") and subject_of(d) != cell.get("subject"):
                continue
            s, _ = serves(d, ref)
            if s is not None and s >= args.threshold:
                best.append((round(s, 3), d))
        if len(best) == 1:
            gaps.append({"class": "AUTHORING GAP", "cell": ref, "ruledWeek": ruled_week(cell),
                         "deck": best[0][1], "score": best[0][0], "distinctiveWords": len(ow),
                         "outcome": (cell.get("verbatimOutcome") or "")[:120],
                         "reason": ("PROXY CANDIDATE ONLY, not a finding. No trace claims this cell and exactly "
                                    "one lesson in its lane and subject scores at or above threshold. Nine of "
                                    "these were put to two independent adversarial reviewers each and SEVEN were "
                                    "refuted, so roughly three in four are wrong. Word overlap is sound as a test "
                                    "of a claim that already exists and is not sound as an assertion that one "
                                    "should. Do not act on these without reading the deck.")})

    report = {
        "file": "_sownb/CALENDAR_SPINE.json",
        "subject": ("ORDER VB-RUN13 R1: coverage counted per workbook cell. Content is the number; path is "
                    "secondary. Every differing row is classed TRACE CORRECTION, AUTHORING GAP or DUPLICATE."),
        "threshold": args.threshold,
        "thresholdDerivation": ("measured, not chosen: 89 trace-asserted positives (median 1.00) against 2413 "
                                "cross-lane negatives (p90 0.333); at 0.85 recall is 0.820 and the false-positive "
                                "rate 0.0058. The positives below threshold are the TRACE CORRECTION candidates."),
        "cellsInScope": len(in_scope),
        "surfacesScanned": len(listing),
        "lessonSurfaces": len(lessons),
        "decksCarryingAClaim": len([d for d in claims if claims[d]]),
        "pathReading_cellsClaimed": len(claimed_by),
        "contentReading_cellsCovered": len(covered),
        # Named, not just counted: anything downstream that asks "is this cell
        # served?" must be able to answer from the record rather than re-deriving
        # it, and a count alone cannot be checked by eye.
        "coveredCells": sorted(covered),
        "coveredCellsByRuledWeek": {
            str(w): sorted(c for c in covered if ruled_week(cells[c]) == w)
            for w in sorted({ruled_week(cells[c]) for c in covered}, key=lambda x: (isinstance(x, str), x))
        },
        "claimedCells": sorted(claimed_by),
        "openCellsInScope": sorted(r for r in in_scope if r not in covered),
        "ambiguousSpineReadings": ambiguous,
        "excludedBodyClaims": extra["excludedBodyClaims"],
        "unscorableClaims": unscorable,
        "traceCorrections": trace_corrections,
        "authoringGapCandidates_proxyOnly": gaps,
        "authoringGapCandidatesWarning": ("a 9-row adversarial sample of these was refuted 7 times out of 9 by two "
                                          "independent reviewers each; treat every row as unverified"),
        "duplicates": duplicates,
        "counts": {"traceCorrection": len(trace_corrections), "authoringGapCandidates_proxyOnly": len(gaps), "duplicate": len(duplicates), "unscorable": len(unscorable)},
        "status": "MEASURED",
    }
    if args.output:
        out = ROOT / args.output if not Path(args.output).is_absolute() else Path(args.output)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(report, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"cells in scope                 {len(in_scope)}")
    print(f"surfaces scanned               {len(listing)}")
    print(f"of those, lessons              {len(lessons)}")
    print(f"decks carrying a trace claim   {report['decksCarryingAClaim']}")
    print(f"PATH    cells claimed          {len(claimed_by)}")
    print(f"CONTENT cells covered          {len(covered)}")
    print(f"TRACE CORRECTION rows          {len(trace_corrections)}")
    print(f"authoring-gap CANDIDATES       {len(gaps)}   (proxy only; 7 of a 9-row sample were refuted)")
    print(f"DUPLICATE rows                 {len(duplicates)}")
    print(f"UNSCORABLE claims              {len(unscorable)}   (outcome has no distinctive words)")
    corrected_only = {r["cell"] for r in trace_corrections} - covered
    unscorable_only = {r["cell"] for r in unscorable} - covered - corrected_only
    print(f"ambiguous spine readings       {len(ambiguous)}   (MULTI or MEASUREMENT INVALID, not counted)")
    print(f"accounting: {len(claimed_by)} claimed = {len(covered)} covered + {len(corrected_only)} "
          f"claimed-but-unserved + {len(unscorable_only)} unscorable")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
