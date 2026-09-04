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
                        deck; arts-challenge decks (Unit 1A/1B) may state the
                        negative restriction but not assign leadership. Explore's
                        A-D names may not appear in another level.
    g32  SLOT           a deck serving a slot-dependent part must read SLOTS.json.
                        Asserted attendance, booking, event/venue-plus-date or
                        "your visit" reds; teaching examples and tickets do not.
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

VERSION = "g30-g35-arts-award-v1.1.1-attendance-reference-scope"
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


# A progress count describes work already held, not the qualification's cap.
# Remove only that numeric occurrence: a second, incorrect cap in the same
# sentence must still red. Other numeric-file wording keeps the old strict
# interpretation; this is not an exemption for all sentences containing "have".
FILE_PROGRESS = re.compile(
    r"\b(?:you|we|I)\s+(?:(?:already|currently|now)\s+)?have\s+$|"
    r"\b(?:your|the|my|our)\s+portfolio\s+"
    r"(?:(?:already|currently|now)\s+)?(?:has|contains|holds)\s+$", re.I)


def file_cap_claims(text: str) -> list[str]:
    claims = []
    for match in FILECAP.finditer(text):
        before = re.split(r"[.!?;]", text[:match.start()])[-1]
        after = text[match.end():]
        # "You have 2 files so far" / "your portfolio contains 2 files" are
        # observations. "You have 2 files as the limit" is still a cap claim.
        limit_suffix = re.match(
            r"\s+(?:(?:as|for)\s+)?(?:the\s+)?(?:cap|limit|maximum)\b", after, re.I)
        progress_suffix = re.match(
            r"\s*(?:(?:so far|already|now|saved)\b|[,.!?;]|$)", after, re.I)
        if FILE_PROGRESS.search(before) and progress_suffix and not limit_suffix:
            continue
        claims.append(match.group(1))
    return claims


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
    cap_claims = file_cap_claims(text)
    if ref.get("fileCap") is None and cap_claims:
        fails.append(f"g30: a file cap is stated for {lvl}, whose cap the register "
                     f"records as UNKNOWN (toolkit only)")
    elif ref.get("fileCap") is not None:
        for c in cap_claims:
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

# This is the register's restriction, not an assigned challenge. Match only
# the negative proposition; do not exempt its whole paragraph, staff drawer,
# or deck, because a positive leadership instruction may follow it.
LEADERSHIP_RESTRICTION = re.compile(
    r"\b(?:(?:the|your|this|an?)\s+)?(?:arts\s+)?challenge\s+"
    r"(?:must|should)\s+not\s+(?:focus\s+on|be\s+about)\s+leadership\b", re.I)


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
    challenge_text = LEADERSHIP_RESTRICTION.sub("", text)
    if challenge and lvl in ("Silver", "Gold") and LEADERSHIP.search(challenge_text):
        fails.append(f"g31: this deck serves {sorted(challenge)}, the arts challenge, "
                     f"and the register says the challenge must NOT focus on "
                     f"leadership; 'leadership' appears outside the negative restriction")

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


# R1/R2 distinguish assertions about this class from teaching content. The
# candidate list is not a blacklist of organisations pupils may learn about.
# These patterns add the common direct booking/attendance assertions missed by
# the original ticket/visit hints. They do not treat "may", "could", a
# negation, or a conditional preparation instruction as a completed booking.
CLASS_SUBJECT = r"(?:we|you|our\s+class|your\s+class|our\s+group|your\s+group)"
BOOKING_ASSERTION = re.compile(
    rf"\b(?:{CLASS_SUBJECT}|the\s+(?:event|exhibition|visit|trip|workshop|meeting))\s+"
    r"(?:(?:are|is|were|was|have|has|have\s+been|has\s+been|will\s+be)\s+)?"
    r"(?:already\s+)?(?:booked|reserved)\b", re.I)
ATTENDANCE_ASSERTION = re.compile(
    rf"\b{CLASS_SUBJECT}\s+(?:"
    r"(?:already\s+)?(?:attended|visited|met|went\s+to)|"
    r"(?:have|has|had)\s+(?:already\s+)?(?:attended|visited|met|been\s+to)|"
    r"(?:will|are\s+going\s+to|is\s+going\s+to)\s+"
    r"(?:attend|visit|meet|go\s+to))\b", re.I)
TRAVEL_PREFIX = re.compile(
    rf"\b{CLASS_SUBJECT}\s+(?:are|is)\s+(?:going|travelling|traveling)\s+to\s+", re.I)
TRAVEL_DESTINATION = re.compile(
    r"(?:(?:the|an?)\s+)?(?:gallery|museum|exhibition|event|workshop|concert|"
    r"screening|showing|performance|meeting)\b", re.I)
INCOMING_ASSERTION = re.compile(
    r"\b(?:the|our|your)\s+(?:artist|practitioner|speaker)\s+"
    r"(?:will\s+(?:visit|come|meet)|is\s+coming)\b", re.I)
EVENT_SCHEDULE = re.compile(
    r"\b(?:the|our|your)\s+(?:event|exhibition|visit|trip|workshop|"
    r"showing|performance|concert|screening|meeting)\s+"
    r"(?:opens|starts|begins|takes\s+place|runs|is\s+(?:on|scheduled|booked)|"
    r"will\s+(?:open|start|begin|take\s+place|run|be))\b", re.I)
# A date next to a venue is only an assertion when coupled with this class or
# an event/schedule. A biographical date and an organisation name alone do not
# satisfy that rule. Keep this separate from the date regex so a historical
# date never acquires an invented "event" label merely by matching a month.
VENUE_EVENT = re.compile(
    r"\b(?:our|your)\s+(?:class|group|visit|trip|event|exhibition|workshop|meeting)\b|"
    r"\b(?:event|exhibition|workshop|concert|screening|showing|performance|meeting)"
    r"\s+(?:at|in|on)\b", re.I)
CONDITIONAL_PREFIX = re.compile(r"\b(?:if|once)\b[^.!?;:]*$", re.I)
RECORDING_PROMPT = re.compile(
    r"\b(?:record|name|note|describe|list|check|write\s+down)\s+"
    r"(?:(?:the|an?|any|your)\s+)?"
    r"(?:event|experience|workshop|exhibition|meeting|artist|practitioner)"
    r"(?:\s+that)?\s+$", re.I)


# Denials and evidence-check questions can refer to attendance without claiming
# it happened. Anchor the grammatical prefix at EACH attendance occurrence; a
# later positive clause receives its own check. These rules do not exempt a
# booking, incoming practitioner, travel or venue/date assertion.
ATTENDANCE_DENIAL_PREFIX = re.compile(
    r"\b(?:does|do|did)\s+not\s+(?:show|prove|confirm|establish|mean)\s+that\s+$",
    re.I)
ATTENDANCE_SAMPLE_PREFIX = re.compile(
    r"\b(?:these|those)\s+are\s+(?:sample|example|model)\s+"
    r"(?:notes|responses|reviews),?\s+not\s+claims?\s+about\s+"
    r"(?:an?|the|any)\s+(?:arts\s+)?"
    r"(?:event|experience|workshop|exhibition|meeting)\s+(?:that\s+)?$", re.I)
ATTENDANCE_RECORD_QUESTION_PREFIX = re.compile(
    r"\b(?:"
    r"(?:can|could)\s+(?:a|the|another)\s+reader\s+"
    r"(?:tell|see|identify|check)\s+(?:which|what)\s+(?:arts\s+)?"
    r"(?:event|experience|workshop|exhibition|meeting)"
    r"|does\s+(?:it|(?:the|your|this)\s+(?:record|evidence|review))\s+"
    r"(?:identify|show|record|name)\s+(?:who|which\s+(?:artist|practitioner))"
    r")\s+$", re.I)
PAST_ATTENDANCE_REFERENCE = re.compile(
    rf"{CLASS_SUBJECT}\s+(?:(?:already\s+)?(?:attended|visited|met|went\s+to)|"
    r"(?:have|has|had)\s+(?:already\s+)?(?:attended|visited|met|been\s+to))", re.I)


def _is_nonassertive_attendance_reference(statement: str, match: re.Match) -> bool:
    before = statement[:match.start()]
    if ATTENDANCE_DENIAL_PREFIX.search(before) or ATTENDANCE_SAMPLE_PREFIX.search(before):
        return True
    # Only a past-experience record question qualifies. A question about who
    # pupils WILL meet must not turn an unconfirmed promise into a safe prompt.
    # deck_text can join adjacent HTML paragraphs with no space after "?";
    # bound this reference at its own punctuation, not the flattened paragraph.
    return bool(re.match(r"[^.!?;]*\?", statement[match.end():])
                and PAST_ATTENDANCE_REFERENCE.fullmatch(match.group(0))
                and ATTENDANCE_RECORD_QUESTION_PREFIX.search(before))


def _is_preparation_reference(statement: str, start: int) -> bool:
    before = statement[:start]
    return bool(CONDITIONAL_PREFIX.search(before) or RECORDING_PROMPT.search(before))


def slot_assertions(text: str, candidate_names: set[str]) -> list[str]:
    """Return the matched assertion and reason, never bare venue/date hits.

    A teaching example prefix is not a global escape: "For example, our class
    is booked" still asserts a booking. Conditional/recording references and
    narrowly matched denials or record questions exempt only their attendance
    occurrence, never a later assertion. Existing 'your visit' and
    'when we visit' hints remain strict under the explicit R1 ruling.
    """
    findings = []
    for statement in re.split(r"(?<=[.!?;])\s+", text):
        for match in VENUE_HINT.finditer(statement):
            findings.append(f"{match.group(0)!r} asserts a visit or ticket booking")
        for pattern, reason in (
                (BOOKING_ASSERTION, "asserts a booking"),
                (ATTENDANCE_ASSERTION, "asserts attendance"),
                (INCOMING_ASSERTION, "asserts a practitioner meeting")):
            for match in pattern.finditer(statement):
                nonassertive_reference = (pattern is ATTENDANCE_ASSERTION
                    and _is_nonassertive_attendance_reference(statement, match))
                if not (_is_preparation_reference(statement, match.start())
                        or nonassertive_reference):
                    findings.append(f"{match.group(0)!r} {reason}")
        for match in TRAVEL_PREFIX.finditer(statement):
            destination = statement[match.end():]
            venue = next((name for name in sorted(candidate_names)
                          if re.match(rf"(?:the\s+)?{re.escape(name)}\b", destination, re.I)), None)
            place = TRAVEL_DESTINATION.match(destination)
            if (venue or place) and not _is_preparation_reference(statement, match.start()):
                findings.append(f"{match.group(0).strip()!r} {venue or place.group(0)!r} "
                                "asserts travel to an arts venue or event")
        dates = list(DATE_HINT.finditer(statement))
        if not dates:
            continue
        schedule = EVENT_SCHEDULE.search(statement)
        if schedule and not _is_preparation_reference(statement, schedule.start()):
            findings.append(f"{schedule.group(0)!r} with {dates[0].group(0)!r} "
                            "asserts a scheduled event")
            continue
        venues = [name for name in sorted(candidate_names)
                  if re.search(rf"\b{re.escape(name)}\b", statement)]
        context = VENUE_EVENT.search(statement)
        if venues and context and not _is_preparation_reference(statement, context.start()):
            findings.append(f"{venues[0]!r} with {dates[0].group(0)!r} "
                            "asserts a venue and event date")
    return list(dict.fromkeys(findings))


def g32(raw: str, aa: dict, sp: dict) -> list[str]:
    """Require the slots and reject assertions, not teaching examples."""
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
    named = {c["name"] for c in (sl.get("candidates") or [])}
    for assertion in slot_assertions(text, named):
        fails.append(f"g32: {assertion}; arrangements live in SLOTS.json")
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
# Object-bearing phrases are equivalent to "share it with": the first
# matcher missed "Share your review with a member of staff". Keep the object
# vocabulary explicit; a peer draft swap remains distinct from the final share.
SHARE_OBJECT = (r"(?:(?:it|(?:your|the|my|our|their|a|an)\s+"
                r"(?:(?:final|completed|own)\s+)?"
                r"(?:review|views|response|work|artwork|piece|findings))\s+)?")
SHARE_WORDS = re.compile(
    rf"\b(?:shared?\s+{SHARE_OBJECT}(?:with|to)|"
    rf"show(?:ed|n)?\s+{SHARE_OBJECT}to|"
    rf"read\s+{SHARE_OBJECT}(?:(?:out|aloud)\s+)?to|"
    rf"present(?:ed)?\s+{SHARE_OBJECT}to|"
    rf"(?:send|sent)\s+{SHARE_OBJECT}to)\b", re.I)
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
    'g30-progress-count-is-not-a-cap',
    'g30-incorrect-cap-beside-progress-still-reds',
    'g30-gold-progress-does-not-invent-a-cap',
    'g30-progress-wording-with-explicit-limit-still-reds',
    'g31-negative-challenge-restriction-passes',
    'g31-negative-restriction-does-not-mask-assigned-leadership',
    'g31-two-unit-consolidation-checks-all-nine-parts',
    'g32-teaching-organisation-example-passes',
    'g32-biographical-date-is-not-a-scheduled-event',
    'g32-biographical-date-with-organisation-example-passes',
    'g32-generic-asserted-booking-reds',
    'g32-negated-booking-and-conditional-preparation-pass',
    'g32-asserted-past-attendance-reds',
    'g32-recording-past-experience-is-not-attendance-assertion',
    'g32-venue-plus-event-date-reds',
    'g32-ticket-evidence-example-and-exit-ticket-pass',
    'g32-visit-assertion-still-reds-without-candidate-name',
    'g32-example-prefix-does-not-mask-booking',
    'g32-incoming-practitioner-promise-reds',
    'g32-recording-word-does-not-mask-booking',
    'g32-after-lunch-does-not-mask-past-attendance',
    'g32-travel-to-named-venue-reds',
    'g32-possible-travel-is-not-booked',
    'g30-file-allowance-is-not-progress',
    'g32-missing-silver-slots-still-red',
    'g34-object-bearing-final-review-share-passes',
    'g34-read-review-aloud-to-person-passes',
    'g34-final-share-without-record-still-reds',
    'g34-peer-draft-swap-still-reds',
    'g32-attendance-denial-is-not-completion',
    'g32-sample-notes-do-not-assert-attendance',
    'g32-reader-question-checks-attendance-record',
    'g32-record-question-checks-practitioner-evidence',
    'g32-denial-followed-by-attendance-still-reds',
    'g32-denial-positive-second-clause-still-reds',
    'g32-sample-followed-by-attendance-still-reds',
    'g32-sample-positive-second-clause-still-reds',
    'g32-reader-question-followed-by-attendance-still-reds',
    'g32-reader-question-positive-second-clause-still-reds',
    'g32-record-question-followed-by-meeting-still-reds',
    'g32-record-question-positive-second-clause-still-reds',
    'g32-denial-does-not-mask-booking',
    'g32-sample-does-not-mask-dated-venue',
    'g32-record-question-does-not-mask-future-promise',
    'g32-future-promise-is-not-a-record-question',
    'g32-positive-proof-is-not-denial',
    'g32-sample-label-is-not-denial',
    'g32-positive-reader-statement-is-not-record-question',
    'g32-positive-record-statement-is-not-record-question',
    'g32-reader-question-at-html-boundary-passes',
    'g32-record-question-at-html-boundary-passes',
    'g32-reader-question-at-html-boundary-does-not-mask-attendance',
    'g32-record-question-at-html-boundary-does-not-mask-promise',
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
    # Focused assertion-scope regressions: every exemption has a nearby
    # must-fire counterpart, so narrowing to zero is not accepted as success.
    SE = {"id": "X", "artsAward": {"level": "Silver", "parts": ["1C"],
                                     "slots": ["EVENT_SLOT"]}}
    SD = {"id": "X", "artsAward": {"level": "Silver", "parts": ["1D"],
                                     "slots": ["ORG_SLOT", "PRACTITIONER_SLOT"]}}
    SC = {"id": "X", "artsAward": {"level": "Silver", "parts": ["2E"],
                                     "listsPortfolio": True}}

    rec("g30-progress-count-is-not-a-cap",
        "an observed file count is not a different Silver cap", False,
        reds(S, "<p>You have 2 files so far. The cap is 20 files.</p>", "g30"))
    rec("g30-incorrect-cap-beside-progress-still-reds",
        "a progress exemption applies to one number, not the sentence or deck", True,
        reds(S, "<p>You have 2 files so far, but the cap is 10 files.</p>", "g30"))
    rec("g30-gold-progress-does-not-invent-a-cap",
        "a Gold portfolio count does not turn its unknown cap into a claim", False,
        reds(G, "<p>Your portfolio contains 2 files so far.</p>", "g30"))
    rec("g30-progress-wording-with-explicit-limit-still-reds",
        "an explicit limit is not an observed progress count", True,
        reds(S, "<p>You have 2 files as the limit.</p>", "g30"))
    rec("g31-negative-challenge-restriction-passes",
        "the staff restriction from the register is not a leadership challenge", False,
        reds(S, '<aside data-audience="staff">The arts challenge must not focus on '
             'leadership.</aside><p>Choose your own arts skill and plan.</p>', "g31"))
    rec("g31-negative-restriction-does-not-mask-assigned-leadership",
        "the exact negative proposition cannot exempt a later positive assignment", True,
        reds(S, '<p>The arts challenge must not focus on leadership. '
             'Your arts challenge is about leadership.</p>', "g31"))
    rec("g31-two-unit-consolidation-checks-all-nine-parts",
        "2E may check every part without claiming to teach all of them", False,
        reds(SC, '<p>Unit 1: Arts practice and pathways. Unit 2: Arts leadership. '
             'Parts: 1A, 1B, 1C, 1D, 2A, 2B, 2C, 2D, 2E.</p>', "g31"))
    rec("g32-teaching-organisation-example-passes",
        "R2 retains organisations named as teaching content", False,
        reds(SD, '<p>For example, MIMA is an arts organisation. No visit is asserted.</p>', "g32"))
    rec("g32-biographical-date-is-not-a-scheduled-event",
        "a date needs an event assertion; this is a synthetic biography fixture", False,
        reds(SD, '<p>The biography gives the artist’s birth date as 14 November.</p>', "g32"))
    rec("g32-biographical-date-with-organisation-example-passes",
        "even a venue name beside a biography date is not itself an event promise", False,
        reds(SD, '<p>A teaching card at MIMA gives the artist’s birth date as '
             '14 November.</p>', "g32"))
    rec("g32-generic-asserted-booking-reds",
        "R1 booking assertions red without a known venue or date", True,
        reds(SE, '<p>Our class is booked to attend the exhibition.</p>', "g32"))
    rec("g32-negated-booking-and-conditional-preparation-pass",
        "unconfirmed slots and conditional preparation do not assert booking", False,
        reds(SE, '<p>Our class is not booked to attend the exhibition. '
             'If a slot is confirmed, we will attend. We may go, they may come in, '
             'or we may meet live on screen.</p>', "g32"))
    rec("g32-asserted-past-attendance-reds",
        "a stock deck cannot assert the pupil attended", True,
        reds(SE, '<p>You attended the exhibition yesterday.</p>', "g32"))
    rec("g32-recording-past-experience-is-not-attendance-assertion",
        "a conditional evidence prompt describes what to record after an experience", False,
        reds(SE, '<p>After an event has taken place, record the event you attended '
             'and what you experienced.</p>', "g32"))
    rec("g32-venue-plus-event-date-reds",
        "a venue and dated event are an asserted arrangement, not a name alone", True,
        reds(SE, '<p>Your class event at MIMA is on 14 November.</p>', "g32"))
    rec("g32-ticket-evidence-example-and-exit-ticket-pass",
        "R1 keeps Exit Ticket and a ticket as an evidence example", False,
        reds(SE, '<h2>Exit Ticket</h2><p>A ticket could be kept as evidence '
             'of the experience.</p>', "g32"))
    rec("g32-visit-assertion-still-reds-without-candidate-name",
        "the explicit your-visit rule is not limited to seeded venues", True,
        reds(SE, '<p>Your visit will help you review the art.</p>', "g32"))
    rec("g32-example-prefix-does-not-mask-booking",
        "example is not a blanket escape for an asserted class booking", True,
        reds(SE, '<p>For example, our class is booked to attend the exhibition.</p>', "g32"))
    rec("g32-incoming-practitioner-promise-reds",
        "an incoming route is also an unconfirmed arrangement", True,
        reds(SD, '<p>The practitioner will visit us tomorrow.</p>', "g32"))
    rec("g32-recording-word-does-not-mask-booking",
        "a recording prompt is a relative reference, not a sentence-wide exemption", True,
        reds(SE, '<p>Record your feedback, but our class is booked to attend '
             'the exhibition.</p>', "g32"))
    rec("g32-after-lunch-does-not-mask-past-attendance",
        "after is not by itself a hypothetical condition", True,
        reds(SE, '<p>After lunch, you attended the exhibition.</p>', "g32"))
    rec("g32-travel-to-named-venue-reds",
        "going to a named venue with a date is an asserted arrangement", True,
        reds(SE, '<p>We are going to MIMA on 14 November.</p>', "g32"))
    rec("g32-possible-travel-is-not-booked",
        "a candidate route is not a promised visit", False,
        reds(SE, '<p>We may go to MIMA if a suitable slot is confirmed.</p>', "g32"))
    rec("g30-file-allowance-is-not-progress",
        "an allowance or maximum is not an observed current count", True,
        reds(S, '<p>You have 10 files available as the maximum.</p>', "g30"))
    missing_event = {"id": "X", "artsAward": {"level": "Silver", "parts": ["1C"]}}
    missing_practitioner = {"id": "X", "artsAward": {"level": "Silver", "parts": ["1D"],
                                                       "slots": ["ORG_SLOT"]}}
    rec("g32-missing-silver-slots-still-red",
        "text narrowing cannot remove the slot declaration requirement", (True, True),
        (reds(missing_event, '<p>Prepare questions.</p>', "g32"),
         reds(missing_practitioner, '<p>Prepare questions.</p>', "g32")))
    rec("g34-object-bearing-final-review-share-passes",
        "share your review with a person is an explicit sharing step", False,
        reds(SE, '<p>Share your review with a member of staff. Record who heard it, '
             'how you shared it and where the evidence is saved.</p>', "g34"))
    rec("g34-read-review-aloud-to-person-passes",
        "reading the completed review aloud is another genuine sharing route", False,
        reds(SE, '<p>Read your final review aloud to another person. '
             'Record whom, how and the evidence location.</p>', "g34"))
    rec("g34-final-share-without-record-still-reds",
        "recognising a share does not excuse missing evidence", True,
        reds(SE, '<p>Share your review with a member of staff.</p>', "g34"))
    rec("g34-peer-draft-swap-still-reds",
        "a recorded draft swap is not the final review share", True,
        reds(SE, '<p>Swap drafts with your partner and record your edits.</p>', "g34"))

    # Silver rendered-text regressions: each safe reference has a positive
    # neighbour that must still fire, in a later sentence and the same sentence.
    rec('g32-attendance-denial-is-not-completion',
        'a practice record explicitly does not prove attendance', False,
        reds(SE, '<p>A practice review does not show that you attended an experience.</p>', "g32"))
    rec('g32-sample-notes-do-not-assert-attendance',
        'a labelled sample disclaims any pupil attendance', False,
        reds(SE, '<p>These are sample notes, not claims about an event you attended.</p>', "g32"))
    rec('g32-reader-question-checks-attendance-record',
        'a question checks an experience record rather than asserting completion', False,
        reds(SE, '<p>Can a reader tell which arts experience you attended and what you communicated about it?</p>', "g32"))
    rec('g32-record-question-checks-practitioner-evidence',
        'a question checks the recorded encounter and individual involvement', False,
        reds(SD, '<p>Does it identify who you met, what the activity was and what you personally explored?</p>', "g32"))
    rec('g32-denial-followed-by-attendance-still-reds',
        'a denial cannot exempt a positive next sentence', True,
        reds(SE, '<p>A practice review does not show that you attended an experience. You attended the exhibition yesterday.</p>', "g32"))
    rec('g32-denial-positive-second-clause-still-reds',
        'a denial exempts only its subordinate reference', True,
        reds(SE, '<p>A practice review does not show that you attended an experience, but you attended the exhibition yesterday.</p>', "g32"))
    rec('g32-sample-followed-by-attendance-still-reds',
        'a sample disclaimer cannot exempt a positive next sentence', True,
        reds(SE, '<p>These are sample notes, not claims about an event you attended. You attended the exhibition yesterday.</p>', "g32"))
    rec('g32-sample-positive-second-clause-still-reds',
        'a sample disclaimer cannot exempt another attendance clause', True,
        reds(SE, '<p>These are sample notes, not claims about an event you attended, but our class visited the exhibition yesterday.</p>', "g32"))
    rec('g32-reader-question-followed-by-attendance-still-reds',
        'a record question cannot exempt a positive next sentence', True,
        reds(SE, '<p>Can a reader tell which arts experience you attended and what you communicated about it? You attended the exhibition yesterday.</p>', "g32"))
    rec('g32-reader-question-positive-second-clause-still-reds',
        'a question mark cannot exempt a second independent attendance clause', True,
        reds(SE, '<p>Can a reader tell which arts experience you attended, given that our class visited the exhibition yesterday?</p>', "g32"))
    rec('g32-record-question-followed-by-meeting-still-reds',
        'a record question cannot exempt a later meeting assertion', True,
        reds(SD, '<p>Does it identify who you met, what the activity was and what you personally explored? You met the artist yesterday.</p>', "g32"))
    rec('g32-record-question-positive-second-clause-still-reds',
        'a record question exempts only the interrogative encounter reference', True,
        reds(SD, '<p>Does it identify who you met, given that you met the artist yesterday?</p>', "g32"))
    rec('g32-denial-does-not-mask-booking',
        'denial matching cannot alter booking checks', True,
        reds(SE, '<p>A practice review does not show that you attended an experience, but our class is booked to attend the exhibition.</p>', "g32"))
    rec('g32-sample-does-not-mask-dated-venue',
        'sample matching cannot alter venue and event date checks', True,
        reds(SE, '<p>These are sample notes, not claims about an event you attended; your class event at MIMA is on 14 November.</p>', "g32"))
    rec('g32-record-question-does-not-mask-future-promise',
        'a completed-record check cannot hide the next promised encounter', True,
        reds(SD, '<p>Does it identify who you met, what the activity was and what you personally explored? You will meet arts practitioners in this session.</p>', "g32"))
    rec('g32-future-promise-is-not-a-record-question',
        'a future meeting in a question is not a past-experience evidence check', True,
        reds(SD, '<p>Does it identify who you will meet in this session?</p>', "g32"))
    rec('g32-positive-proof-is-not-denial',
        'showing attendance is the positive counterpart of the denied proof', True,
        reds(SE, '<p>A practice review shows that you attended an experience.</p>', "g32"))
    rec('g32-sample-label-is-not-denial',
        'labelling notes as samples does not cancel an actual attendance claim', True,
        reds(SE, '<p>These are sample notes which prove that you attended the exhibition.</p>', "g32"))
    rec('g32-positive-reader-statement-is-not-record-question',
        'an affirmative reader statement is not an evidence check question', True,
        reds(SE, '<p>A reader can tell which arts experience you attended.</p>', "g32"))
    rec('g32-positive-record-statement-is-not-record-question',
        'an affirmative encounter statement is not an evidence check question', True,
        reds(SD, '<p>It identifies who you met.</p>', "g32"))
    rec('g32-reader-question-at-html-boundary-passes',
        'adjacent rendered paragraphs need not have whitespace after the question', False,
        reds(SE, '<p>Can a reader tell which arts experience you attended and what you communicated about it?</p><p>Save the record in the portfolio.</p>', "g32"))
    rec('g32-record-question-at-html-boundary-passes',
        'a record question remains a prompt when the next paragraph is joined', False,
        reds(SD, '<p>Does it identify who you met, what the activity was and what you personally explored?</p><p>Now check the organisation and pathway sources.</p>', "g32"))
    rec('g32-reader-question-at-html-boundary-does-not-mask-attendance',
        'a joined HTML paragraph does not hide an attendance assertion', True,
        reds(SE, '<p>Can a reader tell which arts experience you attended?</p><p>You attended the exhibition yesterday.</p>', "g32"))
    rec('g32-record-question-at-html-boundary-does-not-mask-promise',
        'a joined HTML paragraph does not hide the future practitioner promise', True,
        reds(SD, '<p>Does it identify who you met?</p><p>You will meet arts practitioners in this session.</p>', "g32"))
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
