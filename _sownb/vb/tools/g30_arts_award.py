#!/usr/bin/env python3
"""g30-g35 -- the Arts Award gates. ORDER AAE §4.

WHY SIX GATES IN ONE FILE
--------------------------
Every one of them divides by the same register, `tools/artsaward/SPEC.json`, and
every one of them needs the same answer to "what counts as pupil-facing text on
this deck". Six files would be six copies of that answer, kept in step by hand;
this campaign has already shipped one defect of exactly that shape -- a control
surface predicate written in the strip and missing from the sweep, which deleted
the navigation bar from fifteen decks. One file, six gates, one reading of the
deck. `--gate g31` runs one; the default runs all six and reports each verdict
separately, so nothing is rolled up.

    g30  LEVEL-FACT     a level, RQF, qualification number, hours, UCAS,
                        standard or file-cap claim must EQUAL the register.
                        UCAS appears nowhere but Gold.
    g31  PART-MAP       text naming a Part or Unit must match the register's part
                        FOR THAT LEVEL. "leadership" may not appear in an Explore
                        deck, nor in the title, subtitle or body of any
                        arts-challenge deck (Unit 1A/1B) at any level. Explore's
                        A-D names may not appear in another level.
    g32  SLOT           a deck serving a slot-dependent part must read SLOTS.json.
                        A hardcoded venue, ticket, date or "your visit" reds.
    g33  CONSOLIDATION  a deck that lists portfolio sections lists EVERY part of
                        that level: Explore 4, Bronze 4, Silver 9, Gold 9.
    g34  SHARE-EVIDENCE Bronze B, Silver 1C, Explore D and Gold 1A/1D need an
                        explicit, evidenced sharing step -- with whom, how,
                        recorded. A peer draft-swap does not count.
    g35  INVENTED-REQ   pupil-facing text may not assert an assessment rule the
                        register does not carry. Such things may appear only as
                        EXAMPLES of evidence.

SCOPE IS DECLARED, AND A DECK CANNOT HIDE FROM IT
--------------------------------------------------
A deck is in scope when its lesson-config carries an `artsAward` block naming its
level and parts. A deck whose text mentions the Arts Award and carries no such
block is RED under `--scope new`, not skipped -- otherwise the cheapest way past
every gate here would be to say nothing in the one place the gates read.

BINDING ON NEW WORK, REPORT-ONLY ON LIVE, like g23's ceiling and g26's band.
This estate already holds about a hundred live decks that mention the Arts Award
and predate the register. Reddening all of them on the day the register lands
would manufacture a backlog nobody asked for and would say nothing about the
work being done. So `--scope live` (the default) REPORTS, and `--scope new`
BINDS. The report is the contamination list; it is not hidden, it is just not
a gate on somebody else's deck.

    python3 _sownb/vb/tools/g30_arts_award.py <files...> [--gate g31]
    python3 _sownb/vb/tools/g30_arts_award.py --self-test
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import sys
import tempfile
from pathlib import Path

VERSION = "g30-g35-arts-award-v1.0.0"
ROOT = Path(__file__).resolve().parents[3]
SPEC_PATH = ROOT / "tools/artsaward/SPEC.json"
SLOTS_PATH = ROOT / "tools/artsaward/SLOTS.json"

_ls = importlib.util.spec_from_file_location(
    "lesson_stages", ROOT / "_sownb/vb/tools/lesson_stages.py")
ls = importlib.util.module_from_spec(_ls)
_ls.loader.exec_module(ls)

CONFIG_RE = re.compile(r'(<script[^>]*id="lesson-config"[^>]*>)(.*?)(</script>)', re.S)
GATES = ("g30", "g31", "g32", "g33", "g34", "g35")


def digest(p) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def spec() -> dict:
    if not SPEC_PATH.is_file():
        raise SystemExit(f"PROVENANCE REFUSAL: the register {SPEC_PATH} is not a "
                         f"readable file. These gates have nothing to divide by.")
    return json.loads(SPEC_PATH.read_text(encoding="utf-8"))


def slots() -> dict:
    return json.loads(SLOTS_PATH.read_text(encoding="utf-8")) if SLOTS_PATH.is_file() else {}


# --------------------------------------------------------------------------
def deck_text(raw: str, pupil_only: bool) -> str:
    """One reading of the deck, used by every gate.

    pupil_only drops the staff drawer, because g30 and g35 judge what a PUPIL is
    told. g31, g33 and g34 read the whole document: a part named wrongly in a
    staff note misleads the adviser, who is the person marking it.
    """
    import lxml.html as lh
    tree = lh.fromstring(raw)
    for bad in tree.xpath('//script|//style'):
        bad.getparent().remove(bad)
    if pupil_only:
        for bad in tree.xpath('//*[@data-mbm-guide]|//*[@data-audience="staff"]'):
            bad.getparent().remove(bad)
    return " ".join((tree.text_content() or "").split())


def declared(raw: str) -> dict | None:
    m = CONFIG_RE.search(raw)
    if not m:
        return None
    try:
        return (json.loads(m.group(2)) or {}).get("artsAward")
    except Exception:
        return None


MENTIONS = re.compile(r"\bArts\s+Award\b", re.I)


DECK_SHAPED = ('class="deck"', 'class="deck ', 'id="lessonDeck"', "slide-container")


def in_scope(raw: str) -> tuple[bool, dict | None, str | None]:
    if not any(t in raw for t in DECK_SHAPED):
        return False, None, None
    aa = declared(raw)
    if aa:
        return True, aa, None
    if MENTIONS.search(deck_text(raw, pupil_only=False)):
        return True, None, ("names the Arts Award and declares no artsAward block in "
                            "its lesson-config; a deck cannot be in the scheme for a "
                            "reader and out of it for the gates")
    return False, None, None


# --------------------------------------------------------------------------
LEVEL_WORDS = re.compile(r"\b(Explore|Bronze|Silver|Gold)\b")
QUAL_NO = re.compile(r"\b\d{3}/\d{4}/\d\b")
HOURS = re.compile(r"\b(\d{2,3})\s*(?:guided\s+learning\s+)?hours?\b", re.I)
UCAS = re.compile(r"\bUCAS\b", re.I)
FILECAP = re.compile(r"\b(\d{1,3})\s*(?:file|files)\b", re.I)
RQF = re.compile(r"\b(Entry\s*3|Level\s*[123])\b", re.I)


def g30(raw: str, aa: dict, sp: dict) -> list[str]:
    """Every level fact a pupil is shown must equal the register's."""
    fails = []
    lvl = aa.get("level")
    ref = sp["levels"].get(lvl)
    if ref is None:
        return [f"g30: level {lvl!r} is not in the register"]
    text = deck_text(raw, pupil_only=True)

    for n in QUAL_NO.findall(text):
        if n != ref["qualificationNumber"]:
            fails.append(f"g30: qualification number {n} is not {lvl}'s "
                         f"({ref['qualificationNumber']})")
    for r in RQF.findall(text):
        if r.replace(" ", "").lower() != ref["rqfLevel"].replace(" ", "").lower():
            fails.append(f"g30: RQF level {r!r} is not {lvl}'s ({ref['rqfLevel']})")
    allowed_hours = {str(ref["hours"]["guided"]), str(ref["hours"]["independent"]),
                     str(ref["hours"]["total"])}
    for h in HOURS.findall(text):
        if h not in allowed_hours:
            fails.append(f"g30: {h} hours is not one of {lvl}'s "
                         f"{sorted(allowed_hours)}")
    if UCAS.search(text) and lvl != "Gold":
        fails.append(f"g30: UCAS appears in a {lvl} deck; only Gold carries UCAS points")
    if ref.get("fileCap") is None and FILECAP.search(text):
        fails.append(f"g30: a file cap is stated for {lvl}, whose cap the register "
                     f"records as UNKNOWN (toolkit only)")
    elif ref.get("fileCap") is not None:
        for c in FILECAP.findall(text):
            if int(c) != ref["fileCap"]:
                fails.append(f"g30: file cap {c} is not {lvl}'s ({ref['fileCap']})")
    return fails


PART_TOKEN = re.compile(r"\b(?:Part|Unit)\s+([12]?[A-Z])\b")
# "Unit 1C = organisation research". A token that EXISTS but is given the wrong
# name is the exemplar's actual mistake, and the one that misleads an adviser:
# the deck teaches organisation research and the portfolio files it under the
# part that wants a review of an arts event. Caught by comparing the words after
# the token to the register's name for it.
PART_NAMED = re.compile(r"\b(?:Part|Unit)\s+([12]?[A-Z])\b\s*(?:[-:=\u2013\u2014]|\bis\b|\bmeans\b)\s*"
                        r"([A-Za-z][A-Za-z' ]{3,60})")
STOPWORDS = {"the", "a", "an", "and", "or", "of", "in", "to", "for", "your",
             "you", "own", "as", "at", "with", "on", "into", "about", "this"}


def _content_words(text: str) -> set:
    return {w for w in re.findall(r"[a-z]+", text.lower())
            if w not in STOPWORDS and len(w) > 2}
LEADERSHIP = re.compile(r"\bleadership\b", re.I)


def g31(raw: str, aa: dict, sp: dict) -> list[str]:
    """A part named here must be that part in THIS level's register."""
    fails = []
    lvl = aa.get("level")
    ref = sp["levels"].get(lvl)
    if ref is None:
        return [f"g31: level {lvl!r} is not in the register"]
    text = deck_text(raw, pupil_only=False)
    parts = ref["parts"]

    for token in set(PART_TOKEN.findall(text)):
        if token not in parts:
            fails.append(f"g31: {lvl} has no Part/Unit {token}; its parts are "
                         f"{sorted(parts)}")

    if lvl == "Explore" and LEADERSHIP.search(text):
        fails.append("g31: 'leadership' appears in an Explore deck; leadership is "
                     "Bronze D onward and is not an Explore part")

    challenge = {p for p in aa.get("parts", []) if p in ("1A", "1B")}
    if challenge and lvl in ("Silver", "Gold") and LEADERSHIP.search(text):
        fails.append(f"g31: this deck serves {sorted(challenge)}, the arts challenge, "
                     f"and the register says the challenge must NOT focus on "
                     f"leadership; 'leadership' appears in its text")

    for token, given in PART_NAMED.findall(text):
        ref_part = parts.get(token)
        if ref_part is None:
            continue
        given_words = _content_words(given)
        if len(given_words) < 2:
            continue
        # Share a single content word and it is a paraphrase, not a mislabel.
        # Share none and the deck has filed the work under the wrong part.
        if not (given_words & _content_words(ref_part["name"])):
            fails.append(f"g31: {lvl} {token} is {ref_part['name']!r} in the register, "
                         f"and this deck calls it {given.strip()!r}")

    if lvl != "Explore":
        explore_names = {v["name"].lower() for v in sp["levels"]["Explore"]["parts"].values()}
        low = text.lower()
        for n in explore_names:
            if re.search(rf"\bpart\s+[a-d]\s*[-:—]?\s*{re.escape(n)}\b", low):
                fails.append(f"g31: Explore's part name {n!r} appears in a {lvl} deck")
    return fails


# "ticket" is NOT a venue hint, and the first version of this pattern said it was.
# Every deck in this estate ends on a stage called "Exit Ticket", so the survey's
# whole contamination list came back as 191 hits on that heading and nothing
# else -- a selector giving false reasons, which is the thing this campaign just
# ruled against. Worse, §6b explicitly KEEPS a ticket as primary evidence, so
# flagging the word would have argued against the order. What is actually wrong
# is a deck ASSERTING an attendance that is not booked.
VENUE_HINT = re.compile(
    r"\b(?:your visit|when we visit|when you visit|on the trip|during the trip|"
    r"book(?:ing)? (?:your |the )?tickets?|buy (?:a |your )?tickets?|"
    r"bring your ticket)\b", re.I)
DATE_HINT = re.compile(r"\b(\d{1,2}(?:st|nd|rd|th)?\s+"
                       r"(?:January|February|March|April|May|June|July|August|September|"
                       r"October|November|December)|"
                       r"(?:January|February|March|April|May|June|July|August|September|"
                       r"October|November|December)\s+\d{4})\b", re.I)


def g32(raw: str, aa: dict, sp: dict) -> list[str]:
    """A slot-dependent deck reads the slots file; it does not name a venue."""
    fails = []
    sl = slots()
    lvl, parts = aa.get("level"), set(aa.get("parts", []))
    needed = set()
    for slot, cfg in (sl.get("slots") or {}).items():
        for part in (cfg.get("serves") or {}).get(lvl, []):
            if part in parts:
                needed.add(slot)
    if not needed:
        return fails
    if not set(aa.get("slots", [])) >= needed:
        fails.append(f"g32: this deck serves {sorted(parts)} of {lvl}, which needs "
                     f"{sorted(needed)}, and declares {sorted(aa.get('slots', []))}")
    text = deck_text(raw, pupil_only=False)
    for m in set(VENUE_HINT.findall(text)):
        fails.append(f"g32: {m!r} asserts a visit; the route is unconfirmed and lives "
                     f"in SLOTS.json")
    for m in set(DATE_HINT.findall(text)):
        fails.append(f"g32: a dated event ({m!r}) is inside the deck; dates live in "
                     f"SLOTS.json")
    named = {c["name"] for c in (sl.get("candidates") or [])}
    for n in named:
        if re.search(rf"\b{re.escape(n)}\b", text):
            fails.append(f"g32: the deck names {n!r}; a venue is a slot entry, not deck text")
    return fails


LIST_HINT = re.compile(r"\b(portfolio|sections?|parts? of the award|contents)\b", re.I)


def g33(raw: str, aa: dict, sp: dict) -> list[str]:
    """A deck that lists the portfolio lists ALL of it."""
    lvl = aa.get("level")
    ref = sp["levels"].get(lvl)
    if ref is None or not aa.get("listsPortfolio"):
        return []
    text = deck_text(raw, pupil_only=False)
    want = set(ref["parts"])
    seen = {t for t in PART_TOKEN.findall(text)} | {
        t for t in want if re.search(rf"\b{re.escape(t)}\b", text)}
    missing = sorted(want - seen)
    if missing:
        return [f"g33: this deck lists portfolio sections for {lvl} and omits "
                f"{missing} of {len(want)} parts"]
    return []


SHARE_PARTS = {"Explore": {"D"}, "Bronze": {"B"}, "Silver": {"1C"},
               "Gold": {"1A", "1D"}}
SHARE_WORDS = re.compile(r"\b(shared? (?:it |the |your )?(?:with|to)|"
                         r"show(?:ed|n)? (?:it )?to|read (?:it )?(?:out )?to|"
                         r"present(?:ed)? (?:it )?to|sent (?:it )?to)\b", re.I)
RECORDED = re.compile(r"\b(record|recorded|evidence|evidenced|photograph|photo|"
                      r"note|noted|written down|log)\b", re.I)
PEER_SWAP = re.compile(r"\b(swap|swapped|swap sheets|with your partner|"
                       r"with a partner)\b", re.I)


def g34(raw: str, aa: dict, sp: dict) -> list[str]:
    lvl, parts = aa.get("level"), set(aa.get("parts", []))
    if not (parts & SHARE_PARTS.get(lvl, set())):
        return []
    text = deck_text(raw, pupil_only=False)
    fails = []
    if not SHARE_WORDS.search(text):
        fails.append(f"g34: {lvl} {sorted(parts)} needs an explicit sharing step and "
                     f"the deck names none")
    if not RECORDED.search(text):
        fails.append(f"g34: the sharing step is not evidenced; the register wants with "
                     f"whom, how, and recorded")
    if SHARE_WORDS.search(text) is None and PEER_SWAP.search(text):
        fails.append("g34: a peer draft-swap is the only sharing named, and the "
                     "register does not count it")
    return fails


INVENTED = (
    (re.compile(r"\bsigned witness statement\b", re.I), "signed witness statement"),
    (re.compile(r"\bGantt chart\b", re.I), "Gantt chart"),
    (re.compile(r"\breceipts?\b", re.I), "receipts"),
)
MANDATORY = re.compile(r"\b(must|have to|required|requires|mandatory|you need)\b", re.I)
EXAMPLE = re.compile(r"\b(for example|such as|e\.g\.|might|could|one way)\b", re.I)


def g35(raw: str, aa: dict, sp: dict) -> list[str]:
    """An assessment rule the register does not carry may not be asserted."""
    fails = []
    lvl = aa.get("level")
    ref = sp["levels"].get(lvl, {})
    text = deck_text(raw, pupil_only=True)

    for sentence in re.split(r"(?<=[.!?])\s+", text):
        for pat, name in INVENTED:
            if pat.search(sentence) and MANDATORY.search(sentence) \
                    and not EXAMPLE.search(sentence):
                fails.append(f"g35: {name!r} is asserted as required; the register does "
                             f"not carry it, so it may appear only as an example")
    if ref.get("attemptedRule") is None and re.search(
            r"\b(one|1)\s+attempted\b", text, re.I):
        fails.append(f"g35: an Attempted rule is stated for {lvl}, which the register "
                     f"records as UNKNOWN (toolkit only) and which is never inferred "
                     f"from Silver")
    return fails


RUNNERS = {"g30": g30, "g31": g31, "g32": g32, "g33": g33, "g34": g34, "g35": g35}


def judge(path: Path, only: str | None = None, scope: str = "live") -> dict:
    raw = Path(path).read_text(encoding="utf-8", errors="replace")
    scoped, aa, why = in_scope(raw)
    rel = str(path)
    if not scoped:
        return {"file": rel, "status": "NOT-IN-SCOPE", "gates": {}}
    if aa is None:
        return {"file": rel, "status": "RED" if scope == "new" else "UNDECLARED",
                "binding": scope == "new", "reason": why,
                "gates": {g: [why] for g in GATES}}
    sp = spec()
    out = {}
    for g in (GATES if only is None else (only,)):
        out[g] = RUNNERS[g](raw, aa, sp)
    red = any(out[g] for g in out)
    return {"file": rel, "level": aa.get("level"), "parts": aa.get("parts"),
            "status": "RED" if red else "PASS", "binding": scope == "new",
            "gates": out, "specSha256": digest(SPEC_PATH)}


# --------------------------------------------------------------------------
def _deck(cfg: dict, body: str) -> Path:
    src = ('<!doctype html><html><head><script id="lesson-config" '
           f'type="application/json">{json.dumps(cfg)}</script></head>'
           f'<body><main class="deck"><section class="slide">{body}'
           "</section></main></body></html>")
    fh = tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8")
    fh.write(src)
    fh.close()
    return Path(fh.name)


CONTROL_IDS = [
    "g30-an-explore-deck-calling-itself-level-1-reds",
    "g30-ucas-outside-gold-reds",
    "g30-a-file-cap-stated-for-gold-reds",
    "g31-a-unit-1c-called-organisation-research-reds",
    "g31-leadership-in-an-explore-deck-reds",
    "g31-leadership-in-an-arts-challenge-deck-reds",
    "g32-a-hardcoded-venue-reds",
    "g32-a-dated-event-reds",
    "g33-a-silver-list-missing-parts-reds",
    "g34-a-share-part-with-no-sharing-step-reds",
    "g35-a-mandatory-gantt-chart-reds",
    "g35-a-gold-attempted-rule-reds",
    "a-deck-that-names-the-award-and-declares-nothing-reds",
    "a-correct-deck-of-each-level-passes",
]


def controls() -> list[dict]:
    out = []

    def rec(cid, claim, expect, actual):
        out.append({"id": cid, "claim": claim, "expected": expect, "actual": actual,
                    "fired": expect == actual})

    def reds(cfg, body, gate):
        return bool(judge(_deck(cfg, body), gate)["gates"][gate])

    E = {"id": "X", "artsAward": {"level": "Explore", "parts": ["A"]}}
    G = {"id": "X", "artsAward": {"level": "Gold", "parts": ["1B"]}}
    S = {"id": "X", "artsAward": {"level": "Silver", "parts": ["1A"]}}

    rec("g30-an-explore-deck-calling-itself-level-1-reds",
        "the exemplar's mistake: Explore named as a Level 1 award",
        True, reds(E, "<p>This is a Level 1 award.</p>", "g30"))
    rec("g30-ucas-outside-gold-reds",
        "UCAS points appear nowhere but Gold",
        True, reds(S, "<p>This is worth 16 UCAS points.</p>", "g30"))
    rec("g30-a-file-cap-stated-for-gold-reds",
        "Gold's file cap is UNKNOWN in the register and is never inferred from Silver",
        True, reds(G, "<p>You may upload 20 files.</p>", "g30"))

    rec("g31-a-unit-1c-called-organisation-research-reds",
        "the exemplar's mistake: Silver 1C is reviewing arts events, not organisation research",
        True, reds({"id": "X", "artsAward": {"level": "Silver", "parts": ["1C"],
                                             "slots": ["EVENT_SLOT"]}},
                   "<p>Unit 1C: organisation research and career pathways.</p>", "g31"))
    rec("g31-leadership-in-an-explore-deck-reds",
        "leadership is not an Explore part",
        True, reds(E, "<p>Today you practise leadership.</p>", "g31"))
    rec("g31-leadership-in-an-arts-challenge-deck-reds",
        "the register says the arts challenge must NOT focus on leadership",
        True, reds(S, "<p>Your arts challenge is about leadership.</p>", "g31"))

    rec("g32-a-hardcoded-venue-reds",
        "a venue is a slot entry, not deck text",
        True, reds({"id": "X", "artsAward": {"level": "Bronze", "parts": ["B"],
                                             "slots": ["EVENT_SLOT"]}},
                   "<p>When we visit MIMA you will look at three works.</p>", "g32"))
    rec("g32-a-dated-event-reds",
        "no dated event lives inside a deck",
        True, reds({"id": "X", "artsAward": {"level": "Bronze", "parts": ["B"],
                                             "slots": ["EVENT_SLOT"]}},
                   "<p>The exhibition opens on 14th November.</p>", "g32"))

    rec("g33-a-silver-list-missing-parts-reds",
        "the exemplar's Silver list '1A, 1B, 2A-C, 2D-E' omits 1C and 1D",
        True, reds({"id": "X", "artsAward": {"level": "Silver", "parts": ["2E"],
                                             "listsPortfolio": True}},
                   "<p>Your portfolio sections: 1A, 1B, 2A, 2B, 2C, 2D, 2E.</p>", "g33"))

    rec("g34-a-share-part-with-no-sharing-step-reds",
        "Bronze B needs an explicit, evidenced sharing step",
        True, reds({"id": "X", "artsAward": {"level": "Bronze", "parts": ["B"],
                                             "slots": ["EVENT_SLOT"]}},
                   "<p>Write what you thought of the event.</p>", "g34"))

    rec("g35-a-mandatory-gantt-chart-reds",
        "a requirement the register does not carry may appear only as an example",
        True, reds(G, "<p>You must produce a Gantt chart.</p>", "g35"))
    rec("g35-a-gold-attempted-rule-reds",
        "Gold's Attempted rule is UNKNOWN and is never stated to a pupil",
        True, reds(G, "<p>You are allowed one Attempted part.</p>", "g35"))

    undeclared = _deck({"id": "X"}, "<p>This lesson is part of your Arts Award.</p>")
    rec("a-deck-that-names-the-award-and-declares-nothing-reds",
        "a deck cannot be in the scheme for a reader and out of it for the gates; "
        "binding on new work, reported on live",
        ("RED", "UNDECLARED"),
        (judge(undeclared, scope="new")["status"], judge(undeclared)["status"]))

    clean = {
        "Explore": ({"id": "X", "artsAward": {"level": "Explore", "parts": ["A"]}},
                    "<p>Take part in two arts activities. Say what you learnt.</p>"),
        "Bronze": ({"id": "X", "artsAward": {"level": "Bronze", "parts": ["A"]}},
                   "<p>Take part, get better at it, and write a summary.</p>"),
        "Silver": ({"id": "X", "artsAward": {"level": "Silver", "parts": ["1A"]}},
                   "<p>Name a strength and a weakness. Write your own action plan.</p>"),
        # 1B needs ORG_SLOT, and declaring it is part of being a correct deck --
        # the first version of this fixture omitted it and g32 was right to red.
        "Gold": ({"id": "X", "artsAward": {"level": "Gold", "parts": ["1B"],
                                           "slots": ["ORG_SLOT"]}},
                 "<p>Research a career route, then do a placement and reflect on it.</p>"),
    }
    verdicts = {k: judge(_deck(*v))["status"] for k, v in clean.items()}
    rec("a-correct-deck-of-each-level-passes",
        "the gates are not simply red on everything",
        {k: "PASS" for k in clean}, verdicts)
    return out


def self_test() -> dict:
    res = controls()
    ids = [r["id"] for r in res]
    missing = [c for c in CONTROL_IDS if c not in ids]
    extra = [c for c in ids if c not in CONTROL_IDS]
    return {"tool": "g30-g35 arts award", "toolVersion": VERSION,
            "file": "_sownb/vb/tools/g30_arts_award.py",
            "controlsDeclared": len(CONTROL_IDS), "controlsRun": len(res),
            "controlsFired": sum(1 for r in res if r["fired"]),
            "missingControls": missing, "undeclaredControls": extra,
            "allListedControlsFired": not missing and not extra
            and all(r["fired"] for r in res),
            "controls": res}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="*")
    ap.add_argument("--gate", choices=GATES)
    ap.add_argument("--scope", default="live", choices=("live", "new"),
                    help="live REPORTS (the default; the estate holds ~100 decks that "
                         "predate the register), new BINDS")
    ap.add_argument("--output")
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--list-controls", action="store_true")
    a = ap.parse_args()

    if a.list_controls:
        print("\n".join(CONTROL_IDS))
        return 0
    if a.self_test:
        rep = self_test()
        for c in rep["controls"]:
            print(f"  {'ok  ' if c['fired'] else 'FAIL'} {c['id']:52s} "
                  f"expected={c['expected']} observed={c['actual']}")
        print(f"{rep['controlsFired']}/{rep['controlsRun']} controls fired")
        print("PASS" if rep["allListedControlsFired"] else "MEASUREMENT INVALID")
        if a.output:
            Path(a.output).parent.mkdir(parents=True, exist_ok=True)
            Path(a.output).write_text(json.dumps(rep, indent=1) + "\n", encoding="utf-8")
        return 0 if rep["allListedControlsFired"] else 1

    rows = [judge(Path(f), a.gate, a.scope) for f in a.files]
    red = 0
    for r in rows:
        if r["status"] == "NOT-IN-SCOPE":
            continue
        print(f"  {r['status']:4s} {Path(r['file']).name[:52]:52s} "
              f"{r.get('level') or '?'} {r.get('parts') or []}")
        for g, fails in (r.get("gates") or {}).items():
            for f in fails:
                print(f"        {f}")
        if r["status"] in ("RED", "UNDECLARED"):
            red += 1
    inscope = [r for r in rows if r["status"] != "NOT-IN-SCOPE"]
    print(f"{len(inscope)} Arts Award deck(s): {len(inscope) - red} PASS, {red} "
          f"{'RED' if a.scope == 'new' else 'reported'} "
          f"({'BINDING' if a.scope == 'new' else 'report-only'}) "
          f"[{VERSION}]  register {digest(SPEC_PATH)[:16]}")
    if a.output:
        Path(a.output).parent.mkdir(parents=True, exist_ok=True)
        Path(a.output).write_text(json.dumps(
            {"tool": VERSION, "file": "_sownb/vb/tools/g30_arts_award.py",
             "specSha256": digest(SPEC_PATH), "decks": len(inscope), "red": red,
             "rows": rows}, indent=1) + "\n", encoding="utf-8")
    return 1 if (red and a.scope == "new") else 0


if __name__ == "__main__":
    raise SystemExit(main())
