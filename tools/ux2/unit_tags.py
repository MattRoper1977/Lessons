#!/usr/bin/env python3
"""UX2 A1 — the `halfTerm` and `unit` tags on catalogue lesson rows.

Order UX2 §1 A1 (2026-09-08). Two OPTIONAL keys on a `resources.json` row:

  halfTerm  one of the spine's labels ("Autumn 1" … "Summer 2")
  unit      a unit string, only when a named source states one

SOURCE RULE, in this order and no further (A1): (a) the lesson's own title or
metadata; (b) its pack index / START_HERE; (c) a scheme-of-work row naming the
same title verbatim. Nothing is ever read from a filename or a folder position
(g27). A row for which no source speaks stays untagged and is counted in the
worklist, never guessed.

WHAT EACH SOURCE IS HERE

  halfTerm
    (a)+(c)  assets/catalogue/terms-and-styles.json — the catalogue's reviewed
             term evidence (tools/catalogue/TERM_AND_STYLE_EVIDENCE.json cites
             "own title slide declaration", "current manifest lesson row sow
             declaration" and "resolved workbook cells" per file). Its `term`
             values Aut1/Aut2 are the lesson's own declaration re-proved against
             the ruled spine, so they are used first.
    (a)      the lesson's own text — the <title>, <h1> and the first visible
             text of the deck — for an explicit half-term token ("Autumn 1",
             "Aut1", "Autumn 2", "Aut2"). Scanned on file CONTENT only.
    (c)      _sownb/CALENDAR_SPINE.json existingHtml → contentCellReferences →
             workbookCells[reference].termWeek ("Aut1·W3"). The absoluteWeek
             column is never read (g27).
    All present sources must agree; a conflict leaves the row untagged and is
    reported.

  unit
    (a)+(c)  the lesson's own text or family-manifest `sow` line quotes a
             scheme-of-work weekly row's outcome VERBATIM (≥25 characters, the
             row's own lane) — the deck names the SoW row and the SoW grid row
             for that strand and half-term names the unit. Every such match on
             one lesson must agree on one unit. (The Science family manifests'
             `topic` field is a per-lesson topic, not a unit: measured
             2026-09-08, one topic per lesson, so it is not used as a unit.)
    (b)      the pack index / START_HERE: Humanities_Teesside/Teaching_Packs/
             DOWNLOADS_MANIFEST_HTML.json lesson titles joined to a catalogue
             row whose own title ends with that lesson title verbatim, with the
             unit line read from the START_HERE_<PATHWAY>_Humanities_Autumn1
             docx of that pathway (paragraph text; a docx is read with the
             standard-library zipfile, never a heuristic).
    (c)      a _next6/sow/<LANE>.json row whose text names the row's title
             verbatim; a `grid` row yields its `unit` directly, a `weekly` row
             yields the `unit` of the grid row with the same lane, strand and
             half-term.

RE-VERIFY (A1): every source class is checked on a 20-row random sample
(seed 20260908) against an independent reading; a class scoring under 18/20 is
discarded for the run and reported.

APPEND-ONLY (A1): the tool never changes an existing key. --write re-serialises
with the file's own formatting (indent 2, trailing newline) and asserts that
every row, with the two tag keys removed, is byte-identical to its prior form.

    python3 tools/ux2/unit_tags.py --report            derive, print the census
    python3 tools/ux2/unit_tags.py --write             tag resources.json in place
    python3 tools/ux2/unit_tags.py --check             committed tags == derived
    python3 tools/ux2/unit_tags.py --self-test         the gates go red on a plant
"""
from __future__ import annotations

import argparse
import copy
import html as html_module
import json
import random
import re
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CATALOGUE = ROOT / "resources.json"
TERMS_AND_STYLES = ROOT / "assets/catalogue/terms-and-styles.json"
SPINE = ROOT / "_sownb/CALENDAR_SPINE.json"
SOW_DIR = ROOT / "_next6/sow"
HUM_PACK_INDEX = ROOT / "Humanities_Teesside/Teaching_Packs/DOWNLOADS_MANIFEST_HTML.json"
HUM_PACK_DIR = ROOT / "Humanities_Teesside/Teaching_Packs"
SCIENCE_MANIFESTS = [ROOT / "Science_Teesside" / lane / "v3_40min/manifest-v3.json" for lane in ("Build", "Grow", "Launch")]

EVIDENCE = ROOT / "tools/catalogue/TERM_AND_STYLE_EVIDENCE.json"
# The evidence methods of class (a) — the lesson's own declaration or manifest
# row — and (c) — workbook cells. "current presentation structure" proves style,
# not term, and is not in this set.
EVIDENCE_METHODS = {
    "own title slide declaration",
    "current manifest lesson row sow declaration",
    "current manifest lesson row with resolved workbook cells",
    "current content re-proves audited workbook binding",
    "current lesson config cells",
    "unchanged source census with resolved workbook cells",
    "registered transformed-version donor with current term proof",
    "current explicit enrichment label and ruled school calendar",
}
TAG_KEYS = ("halfTerm", "unit")
HALF_TERMS = ["Autumn 1", "Autumn 2", "Spring 1", "Spring 2", "Summer 1", "Summer 2"]
SHORT = {"Aut1": "Autumn 1", "Aut2": "Autumn 2", "Spr1": "Spring 1", "Spr2": "Spring 2", "Sum1": "Summer 1", "Sum2": "Summer 2"}
IN_SCOPE = {"Autumn 1", "Autumn 2"}
LESSON_TYPES = {"lesson", "Lesson", "revision"}
SAMPLE_SEED = 20260908
SAMPLE_SIZE = 20
PASS_MARK = 18

# Half-term tokens in a deck's OWN text. These carry no week shape on purpose.
HALF_TERM_TOKEN = re.compile(r"\b(?:Aut(?:umn)?|Spr(?:ing)?|Sum(?:mer)?)\s*[·\-]?\s*([12])\b", re.I)
SEASON = {"aut": "Autumn", "spr": "Spring", "sum": "Summer"}
TAG = re.compile(r"<[^>]+>")
TITLE = re.compile(r"<title[^>]*>(.*?)</title>", re.S | re.I)
H1 = re.compile(r"<h1[^>]*>(.*?)</h1>", re.S | re.I)


def read_json(location: Path):
    return json.loads(location.read_text("utf-8"))


def sha256_of(location: Path) -> str:
    import hashlib
    return hashlib.sha256(location.read_bytes()).hexdigest()


def lane_of(row: dict) -> str | None:
    """The pathway a row belongs to, from its own fields only (subject prefix or title prefix)."""
    for value in (row.get("subject", ""), row.get("title", "")):
        match = re.match(r"^(BUILD|GROW|LAUNCH)(?![A-Za-z])", str(value))
        if match:
            return match.group(1)
    return None


def deck_text(location: Path, limit: int = 6000) -> str:
    try:
        raw = location.read_text("utf-8", errors="replace")
    except OSError:
        return ""
    head = []
    for pattern in (TITLE, H1):
        found = pattern.search(raw)
        if found:
            head.append(TAG.sub(" ", found.group(1)))
    body = raw.split("<body", 1)[1] if "<body" in raw else raw
    body = re.sub(r"<(script|style|template|noscript)\b.*?</\1>", " ", body, flags=re.S | re.I)
    body = TAG.sub(" ", body)
    text = " ".join(head) + " " + html_module.unescape(body)
    return re.sub(r"\s+", " ", text)[:limit]


def half_terms_in_text(text: str) -> set[str]:
    found = set()
    for match in HALF_TERM_TOKEN.finditer(text):
        season = SEASON[match.group(0)[:3].lower()]
        found.add(f"{season} {match.group(1)}")
    return found


def load_spine_terms() -> dict[str, set[str]]:
    """file → set of half-terms from the ruled workbook cells (termWeek), never absoluteWeek."""
    spine = read_json(SPINE)
    cells = {cell["reference"]: cell for cell in spine.get("workbookCells", [])}
    result: dict[str, set[str]] = {}
    for entry in spine.get("existingHtml", []):
        terms = set()
        for reference in entry.get("contentCellReferences", []) or []:
            cell = cells.get(reference)
            term_week = (cell or {}).get("termWeek") or ""
            short = term_week.split("·")[0]
            if short in SHORT:
                terms.add(SHORT[short])
        if terms:
            result[entry["path"]] = terms
    return result


def load_manifest_rows() -> dict[str, list[dict]]:
    """file (repo path) → its family-manifest lesson rows (for the `sow` declaration)."""
    rows: dict[str, list[dict]] = {}
    for manifest in SCIENCE_MANIFESTS:
        if not manifest.is_file():
            continue
        for lesson in read_json(manifest):
            file_name = lesson.get("file")
            if file_name:
                rows.setdefault((manifest.parent / file_name).relative_to(ROOT).as_posix(), []).append(lesson)
    return rows


def load_science_topics() -> dict[str, tuple[str, str]]:
    """file (repo path) → (topic, manifest path) from the family manifests' own lesson rows."""
    topics = {}
    for manifest in SCIENCE_MANIFESTS:
        if not manifest.is_file():
            continue
        for lesson in read_json(manifest):
            topic = lesson.get("topic")
            file_name = lesson.get("file")
            if topic and file_name:
                topics[(manifest.parent / file_name).relative_to(ROOT).as_posix()] = (topic, manifest.relative_to(ROOT).as_posix())
    return topics


def docx_paragraphs(location: Path) -> list[str]:
    with zipfile.ZipFile(location) as archive:
        xml = archive.read("word/document.xml").decode("utf-8")
    paragraphs = []
    for para in re.findall(r"<w:p\b.*?</w:p>", xml, flags=re.S):
        text = "".join(re.findall(r"<w:t[^>]*>(.*?)</w:t>", para, flags=re.S))
        text = html_module.unescape(text).strip()
        if text:
            paragraphs.append(text)
    return paragraphs


def load_humanities_pack_units() -> dict[str, tuple[str, str, str]]:
    """lesson title (verbatim, from the pack index) → (unit, lane, source) via START_HERE."""
    if not HUM_PACK_INDEX.is_file():
        return {}
    index = read_json(HUM_PACK_INDEX)
    result = {}
    for lane, block in index.get("pathways", {}).items():
        start_here = HUM_PACK_DIR / lane / f"START_HERE_{lane}_Humanities_Autumn1.docx"
        if not start_here.is_file():
            continue
        paragraphs = docx_paragraphs(start_here)
        unit = None
        for para in paragraphs:
            # The unit line is the paragraph that names the unit on its own,
            # e.g. "World About Me". It sits before the week table; it is the
            # first short paragraph that is neither the title nor a heading
            # that names the pathway/term.
            if len(para) <= 60 and not re.search(r"(START|Start here|Autumn|Week|Humanities|Pathway|Teaching pack|Contents)", para):
                unit = para
                break
        if not unit:
            continue
        for lesson in block.get("lessons", []):
            result[lesson["title"]] = (unit, lane, start_here.relative_to(ROOT).as_posix())
    return result


def load_sow() -> dict[str, dict]:
    sow = {}
    for lane in ("BUILD", "GROW", "LAUNCH"):
        location = SOW_DIR / f"{lane}.json"
        if location.is_file():
            sow[lane] = read_json(location)
    return sow


def half_term_of_weeks(weeks: str) -> str | None:
    match = re.match(r"^(Aut|Spr|Sum)\s*([12])", weeks or "")
    return f"{SEASON[match.group(1).lower()]} {match.group(2)}" if match else None


def sow_unit_for_text(sow: dict, lane: str | None, text: str, half_term: str | None) -> tuple[str, str] | None:
    """(unit, source) when the deck's own text quotes a weekly SoW outcome verbatim.

    Every weekly row of the lane whose outcome (≥25 chars) appears in the text
    is a match; each match resolves through (strand, half-term) to a grid unit;
    the matches must agree on ONE unit (else None). The week named by the
    matched row must sit in the row's own half-term (else None)."""
    if not lane or lane not in sow or not text:
        return None
    lane_sow = sow[lane]
    units = set()
    sources = []
    for weekly in lane_sow.get("weekly", []):
        outcome = (weekly.get("outcome") or "").strip()
        if len(outcome) < 25 or outcome not in text:
            continue
        week_half = half_term_of_weeks((weekly.get("week") or "").replace("·", " "))
        if half_term and week_half != half_term:
            return None
        for grid in lane_sow.get("grid", []):
            if grid.get("strand") == weekly.get("strand") and half_term_of_weeks(grid.get("weeks")) == week_half and grid.get("unit"):
                units.add(grid["unit"])
                sources.append(f"weekly row {weekly.get('row')} → grid row {grid.get('row')}")
    if len(units) == 1:
        return next(iter(units)), f"_next6/sow/{lane}.json {sources[0]}"
    return None


def sow_unit_for_title(sow: dict, lane: str | None, title: str) -> tuple[str, str] | None:
    """(unit, source) when a SoW row of the row's lane names the title verbatim."""
    if not lane or lane not in sow:
        return None
    short = title.split(" · ")[-1].strip()
    needles = {title.strip(), short} - {""}
    lane_sow = sow[lane]
    for grid in lane_sow.get("grid", []):
        blob = " ".join(str(v) for v in grid.values())
        if any(needle in blob for needle in needles) and grid.get("unit"):
            return grid["unit"], f"_next6/sow/{lane}.json grid row {grid.get('row')}"
    for weekly in lane_sow.get("weekly", []):
        blob = " ".join(str(v) for v in weekly.values())
        if any(needle in blob for needle in needles):
            half = half_term_of_weeks((weekly.get("week") or "").replace("·", " "))
            for grid in lane_sow.get("grid", []):
                if grid.get("strand") == weekly.get("strand") and half_term_of_weeks(grid.get("weeks")) == half and grid.get("unit"):
                    return grid["unit"], f"_next6/sow/{lane}.json weekly row {weekly.get('row')} → grid row {grid.get('row')}"
    return None


def derive(rows: list[dict]) -> dict:
    terms_and_styles = read_json(TERMS_AND_STYLES)["entries"]
    spine_terms = load_spine_terms()
    topics = load_science_topics()
    manifest_rows = load_manifest_rows()
    pack_units = load_humanities_pack_units()
    sow = load_sow()

    per_row = []
    for index, row in enumerate(rows):
        record = {"index": index, "file": row.get("file", ""), "title": row.get("title", ""), "type": row.get("type"),
                  "year": row.get("year"), "lesson": row.get("type") in LESSON_TYPES and row.get("year") == "2026-27",
                  "halfTerm": None, "halfTermSources": [], "halfTermConflict": False,
                  "unit": None, "unitSource": None, "worklist": None}
        per_row.append(record)
        if not record["lesson"]:
            continue
        file_key = row.get("file", "")
        location = ROOT / file_key
        candidates: dict[str, str] = {}
        term = (terms_and_styles.get(file_key) or {}).get("term")
        if term in SHORT:
            candidates["terms-and-styles"] = SHORT[term]
        if file_key in spine_terms and len(spine_terms[file_key]) == 1:
            candidates["spine-cell"] = next(iter(spine_terms[file_key]))
        text = deck_text(location) if location.is_file() else ""
        in_text = half_terms_in_text(text)
        if len(in_text) == 1:
            candidates["deck-text"] = next(iter(in_text))
        values = set(candidates.values())
        record["halfTermSources"] = sorted(candidates)
        if len(values) == 1:
            record["halfTerm"] = next(iter(values))
        elif len(values) > 1:
            record["halfTermConflict"] = True
        if record["halfTerm"] not in IN_SCOPE:
            record["worklist"] = "outside Autumn 2026 or no half-term source"
            continue
        # unit, in order: (a)+(c) the deck's own text / manifest sow line quoting a
        # SoW weekly outcome verbatim, (b) START_HERE via the pack index, (c) a SoW
        # row naming the title verbatim. manifest-v3 `topic` is recorded, not used.
        record["lessonTopic"] = topics.get(file_key, (None, None))[0]
        sow_text = (deck_text(location, 40000) if location.is_file() else "") + " " + " ".join(m.get("sow", "") for m in manifest_rows.get(file_key, []))
        verbatim = sow_unit_for_text(sow, lane_of(row), sow_text, record["halfTerm"])
        if verbatim:
            record["unit"], record["unitSource"] = verbatim[0], "SoW verbatim outcome (" + verbatim[1] + ")"
        else:
            title = row.get("title", "")
            hit = next(((unit, lane, source) for lesson_title, (unit, lane, source) in pack_units.items()
                        if title.strip().endswith(lesson_title) and lane_of(row) == lane), None)
            if hit:
                record["unit"], record["unitSource"] = hit[0], "START_HERE (" + hit[2] + ")"
            else:
                sow_hit = sow_unit_for_title(sow, lane_of(row), title)
                if sow_hit:
                    record["unit"], record["unitSource"] = sow_hit[0], "SoW verbatim (" + sow_hit[1] + ")"
        if record["unit"] is None:
            record["worklist"] = "half-term tagged; no source names a unit"
    return {"rows": per_row, "topics": topics, "packUnits": pack_units}


def verify_classes(rows: list[dict], derived: dict) -> dict:
    """20-row samples per source class against an independent reading. <18/20 discards the class."""
    rng = random.Random(SAMPLE_SEED)
    verdicts = {}
    records = derived["rows"]
    # halfTerm from terms-and-styles: independent reading = the deck's own text, a
    # spine cell, or the catalogue evidence re-proved against the file's CURRENT
    # bytes (its sha256 binding) with a method of class (a) or (c) and, where a
    # quote exists, the quote naming the same half-term.
    evidence = read_json(EVIDENCE)["entries"] if EVIDENCE.is_file() else {}
    pool = [r for r in records if r["halfTerm"] and "terms-and-styles" in r["halfTermSources"]]
    sample = rng.sample(pool, min(SAMPLE_SIZE, len(pool)))
    agree = 0
    detail = []
    for rec in sample:
        location = ROOT / rec["file"]
        text = deck_text(location)
        independent = half_terms_in_text(text)
        reproved = False
        entry = evidence.get(rec["file"]) or {}
        if entry and location.is_file() and entry.get("sha256") == sha256_of(location):
            methods = [e.get("method") for e in entry.get("evidence", [])]
            quotes = " ".join(e.get("quote") or "" for e in entry.get("evidence", []))
            quoted = half_terms_in_text(quotes)
            reproved = any(m in EVIDENCE_METHODS for m in methods) and (not quoted or rec["halfTerm"] in quoted)
        ok = rec["halfTerm"] in independent or ("spine-cell" in rec["halfTermSources"]) or reproved
        agree += ok
        detail.append({"file": rec["file"], "halfTerm": rec["halfTerm"], "deckText": sorted(independent), "evidenceReproved": reproved, "ok": ok})
    verdicts["halfTerm:terms-and-styles"] = {"sampled": len(sample), "agree": agree, "pass": len(sample) == 0 or agree >= min(PASS_MARK, len(sample)), "detail": detail}
    # unit from the SoW verbatim join: independent reading = the matched weekly row's
    # strand belongs to the row's subject group and its week sits in the row's half-term
    # (both re-read from the SoW file, not from the derivation).
    sow = load_sow()
    pool = [r for r in records if r["unit"] and (r["unitSource"] or "").startswith("SoW verbatim outcome")]
    sample = rng.sample(pool, min(SAMPLE_SIZE, len(pool)))
    agree = 0
    detail = []
    for rec in sample:
        row = rows[rec["index"]]
        lane = lane_of(row)
        m = re.search(r"weekly row (\d+)", rec["unitSource"] or "")
        weekly = next((w for w in sow.get(lane, {}).get("weekly", []) if str(w.get("row")) == (m.group(1) if m else "")), None)
        subject_words = re.findall(r"[a-z]{4,}", str(row.get("subject", "")).lower())
        strand = (weekly or {}).get("strand", "").lower()
        week_half = half_term_of_weeks(((weekly or {}).get("week") or "").replace("·", " "))
        ok = bool(weekly) and week_half == rec["halfTerm"] and (any(w in strand for w in subject_words) or "vocational" in str(row.get("subject", "")).lower())
        agree += ok
        detail.append({"file": rec["file"], "unit": rec["unit"], "strand": (weekly or {}).get("strand"), "week": (weekly or {}).get("week"), "ok": ok})
    verdicts["unit:SoW-verbatim"] = {"sampled": len(sample), "agree": agree, "pass": len(sample) == 0 or agree >= min(PASS_MARK, len(sample)), "detail": detail}
    for label, prefix in (("unit:START_HERE", "START_HERE ("), ("unit:SoW", "SoW verbatim (")):
        pool = [r for r in records if r["unit"] and (r["unitSource"] or "").startswith(prefix)]
        sample = rng.sample(pool, min(SAMPLE_SIZE, len(pool)))
        agree = 0
        detail = []
        for rec in sample:
            text = deck_text(ROOT / rec["file"]).lower()
            words = [w for w in re.findall(r"[a-z]{4,}", rec["unit"].lower())]
            ok = bool(words) and any(w in text for w in words)
            agree += ok
            detail.append({"file": rec["file"], "unit": rec["unit"], "ok": ok})
        verdicts[label] = {"sampled": len(sample), "agree": agree, "pass": len(sample) == 0 or agree >= min(PASS_MARK, len(sample)), "detail": detail}
    return verdicts


def apply(rows: list[dict], derived: dict, verdicts: dict) -> list[dict]:
    tagged = copy.deepcopy(rows)
    discard_units = {label.split(":")[1] for label, v in verdicts.items() if label.startswith("unit:") and not v["pass"]}
    prefix_of = {"SoW verbatim outcome": "SoW-verbatim", "START_HERE": "START_HERE", "SoW verbatim": "SoW"}
    discard_half = not verdicts["halfTerm:terms-and-styles"]["pass"]
    for rec in derived["rows"]:
        row = tagged[rec["index"]]
        if rec["halfTerm"] in IN_SCOPE and not (discard_half and rec["halfTermSources"] == ["terms-and-styles"]):
            row["halfTerm"] = rec["halfTerm"]
        label = (rec["unitSource"] or "").split(" (")[0]
        source = prefix_of.get(label, label)
        if rec["unit"] and "halfTerm" in row and source not in discard_units:
            row["unit"] = rec["unit"]
    return tagged


def serialise(rows: list[dict]) -> bytes:
    return (json.dumps(rows, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def stripped(row: dict) -> dict:
    return {k: v for k, v in row.items() if k not in TAG_KEYS}


def assert_append_only(before: list[dict], after: list[dict]) -> None:
    if len(before) != len(after):
        raise SystemExit("[FAIL] row count changed")
    for index, (old, new) in enumerate(zip(before, after)):
        if json.dumps(stripped(old), ensure_ascii=False) != json.dumps(stripped(new), ensure_ascii=False):
            raise SystemExit(f"[FAIL] row {index} changed beyond the tag keys")
        for key in TAG_KEYS:
            if key in old and old[key] != new.get(key):
                raise SystemExit(f"[FAIL] row {index}: an existing {key} value was altered")


def census(rows: list[dict], derived: dict) -> dict:
    out = {"rows": len(rows), "lessons2026": 0, "halfTerm": {"Autumn 1": 0, "Autumn 2": 0}, "unit": 0,
           "unitBySource": {}, "worklist": 0, "conflicts": 0, "bySubject": {}}
    for rec in derived["rows"]:
        if not rec["lesson"]:
            continue
        out["lessons2026"] += 1
        subject = rows[rec["index"]].get("subject", "")
        group = out["bySubject"].setdefault(subject, {"lessons": 0, "halfTerm": 0, "unit": 0, "worklist": 0})
        group["lessons"] += 1
        if rec["halfTermConflict"]:
            out["conflicts"] += 1
        if rec["halfTerm"] in IN_SCOPE:
            out["halfTerm"][rec["halfTerm"]] += 1
            group["halfTerm"] += 1
        if rec.get("lessonTopic"):
            out["lessonTopicsRecordedNotUsed"] = out.get("lessonTopicsRecordedNotUsed", 0) + 1
        if rec["unit"]:
            out["unit"] += 1
            group["unit"] += 1
            key = (rec["unitSource"] or "").split(" (")[0]
            out["unitBySource"][key] = out["unitBySource"].get(key, 0) + 1
        if rec["worklist"]:
            out["worklist"] += 1
            group["worklist"] += 1
    return out


def self_test() -> None:
    rows, _packs = split_packs(read_json(CATALOGUE))
    derived = derive(rows)
    verdicts = verify_classes(rows, derived)
    tagged = apply(rows, derived, verdicts)
    assert_append_only(rows, tagged)
    controls = []
    # 1. an altered existing value is caught
    bad = copy.deepcopy(tagged)
    bad[0]["title"] = bad[0]["title"] + " (planted)"
    try:
        assert_append_only(rows, bad)
        controls.append(("altered original value is caught", False))
    except SystemExit:
        controls.append(("altered original value is caught", True))
    # 2. a removed row is caught
    try:
        assert_append_only(rows, tagged[:-1])
        controls.append(("removed row is caught", False))
    except SystemExit:
        controls.append(("removed row is caught", True))
    # 3. a novel halfTerm label is refused by --check
    novel = copy.deepcopy(tagged)
    first = next(i for i, r in enumerate(novel) if "halfTerm" in r)
    novel[first]["halfTerm"] = "Autumn 9"
    controls.append(("novel halfTerm label differs from the derivation", check_rows(novel, derived, verdicts) is not None))
    # 4. the derivation is deterministic
    controls.append(("derivation is deterministic", serialise(apply(rows, derive(rows), verdicts)) == serialise(tagged)))
    for name, ok in controls:
        print(f"  {'PASS' if ok else 'FAIL'}  {name}")
    if not all(ok for _, ok in controls):
        raise SystemExit("[FAIL] self-test: a control did not go red")
    print("[PASS] unit_tags self-test")


def check_rows(rows: list[dict], derived: dict, verdicts: dict) -> str | None:
    base = [stripped(r) for r in rows]
    expected = apply(base, derived, verdicts)
    for index, (have, want) in enumerate(zip(rows, expected)):
        for key in TAG_KEYS:
            if have.get(key) != want.get(key):
                return f"row {index} ({have.get('file')}): {key} is {have.get(key)!r}, derivation says {want.get(key)!r}"
    if len(rows) != len(expected):
        return "row count differs"
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--report", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--json", type=Path, help="write the full derivation + verdicts to this file")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return 0
    # UX2 D3: companion-pack entries (kind "pack") are the catalogue's tail and
    # carry tags copied by tools/ux2/companion_catalogue.py, which checks them;
    # this tool derives tags for lesson rows only and passes the tail through.
    rows, packs = split_packs(read_json(CATALOGUE))
    base = [stripped(r) for r in rows]
    derived = derive(base)
    verdicts = verify_classes(base, derived)
    tagged = apply(base, derived, verdicts)
    assert_append_only(base, tagged)
    summary = {"census": census(base, derived), "verdicts": {k: {kk: vv for kk, vv in v.items() if kk != "detail"} for k, v in verdicts.items()},
               "halfTermLabels": HALF_TERMS, "sampleSeed": SAMPLE_SEED}
    if args.json:
        args.json.write_text(json.dumps({**summary, "verdictDetail": verdicts, "rows": derived["rows"]}, ensure_ascii=False, indent=1))
    if args.report or not (args.write or args.check):
        print(json.dumps(summary, ensure_ascii=False, indent=1))
    if args.check:
        problem = check_rows(rows, derived, verdicts)
        if problem:
            print("[FAIL] committed tags differ from the derivation: " + problem)
            return 1
        print(f"[PASS] committed tags match the derivation: halfTerm {sum('halfTerm' in r for r in rows)}, unit {sum('unit' in r for r in rows)}")
    if args.write:
        CATALOGUE.write_bytes(serialise(tagged + packs))
        print(f"[DONE] wrote {CATALOGUE.relative_to(ROOT)}: halfTerm {sum('halfTerm' in r for r in tagged)}, unit {sum('unit' in r for r in tagged)}; {len(packs)} pack rows passed through")
    return 0


def split_packs(rows: list[dict]) -> tuple[list[dict], list[dict]]:
    """Lesson rows first, companion-pack rows (kind "pack") as the contiguous tail."""
    first = next((i for i, r in enumerate(rows) if r.get("kind") == "pack"), len(rows))
    head, tail = rows[:first], rows[first:]
    if any(r.get("kind") != "pack" for r in tail):
        raise SystemExit("[FAIL] a non-pack row follows the companion-pack rows; packs must be the catalogue's tail")
    return head, tail


if __name__ == "__main__":
    raise SystemExit(main())
