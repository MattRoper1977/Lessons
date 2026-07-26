#!/usr/bin/env python3
"""
assessed_conditions_gate.py  —  LundyLoop instrument  [LL-INST-06]

WHAT IT DERIVES
  For every assessed file: what the Conditions Card AUTHORISES at each tier, what
  the file actually OFFERS at each tier, and every offer that appears in neither
  the allowed nor the forbidden list — i.e. that nobody has ruled on.

WHY IT EXISTS
  Three contradictions were found inside the estate's two most protected files, by
  reading two surfaces of one file and noticing they disagreed:

    LAUNCH W7  Standard is offered a "Route Card" (45 min). Not in its allowed list.
    GROW  W7   Standard is offered a "Time Budget" (39 min). Not in its allowed list.
    LAUNCH W7  Supported is offered THREE frames; the Card authorises two.

  In a supervised assessed sitting, an adult reading the Card withholds the scaffold
  and an adult reading the slide hands it out. Two pupils get different access from
  one file.

  GROW's 39 minutes FITS its 40-minute period, so it never surfaced as an arithmetic
  problem. LAUNCH's 45 did. The timing mismatch was the tell, not the fault —
  and a defect found through a symptom will have symptomless siblings. This gate
  searches for the fault, not the tell.

THE RULE IT ENFORCES
  The Conditions Card is authoritative for its file. Everything else in that file is
  checked against it. A slide may never quietly exceed its Card; if a tier genuinely
  needs more, the CARD is amended deliberately and the slide follows it.

SELECTOR
  '★ ASSESSED LESSON' — the INCLUSION-safe selector (see /REGISTER.md R-A01).
  NEVER '★ ASSESSED', which returns six files, four of which carry the marker as a
  reference. Using the broad string here would gate files that have no Card.

HOW HONEST THIS IS — READ BEFORE TRUSTING A CLEAN RESULT
  The two sides are extracted LITERALLY. The comparison between them is
  INTERPRETIVE: an allowed list says "the opening and close frames" and an offer
  says "Opening Frame ... Close Frame ...". Deciding those match requires reading
  meaning, and standing rule 4 says interpretive derivations fail quietly.

  So this gate NEVER returns a pass. For each tier it prints the offer text and the
  Card's allowed and forbidden text SIDE BY SIDE, sets NEEDS_HUMAN_RULING, and adds
  three token-overlap HINTS. The hints are a bag-of-words heuristic and are labelled
  as such: "account" appears both in GROW's permitted Opening Frame and in its
  forbidden text, so raw overlap reads as a breach when it is not. **The hints
  triage; the human rules.** All three findings above are things nobody had written
  any rule about — they are absences in the Card, which no token comparison can
  detect and only a reader can.

WHAT IT STRUCTURALLY CANNOT SEE
  - RUNTIME STATE. Verified 2026-07-26: prevSlide() is unguarded in both assessed
    files — `if(currentSlide>0){currentSlide--;showSlide(currentSlide)}` — ArrowLeft
    is bound, and there is no lock of any kind. So the file's own We Do teaching
    content (Close Moves: "'More precisely…' if the thesis wobbles", "Opening
    sentence two, verbatim or sharpened") is one keypress from the assessed slide.
    Front-of-class delivery makes the DEFAULT safe; the access arrangements the Card
    guarantees — a device for reading support, a scribe working from the screen, a
    separate room — are exactly what puts a pupil in front of a navigable file.
    THIS GATE CANNOT SEE THAT. It is a staff-note problem, not a static one.
  - Whether an authorised scaffold is pedagogically right.
  - Anything in a printed pack that was edited after export.

STATUS: current
"""

import html
import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

REPO = Path(__file__).resolve().parents[2]

SELECTOR = "★ ASSESSED LESSON"
TIERS = ("Supported", "Standard", "Stretch")

TAGS = re.compile(r"<[^>]+>")
SCRIPTSTYLE = re.compile(r"<(script|style)[^>]*>.*?</\1>", re.S | re.I)

# The Card's tier table: <tier emoji+name> | allowed | not allowed
ROW = re.compile(
    r"(?:🤝|👤|🚀)\s*(Supported|Standard|Stretch)\s*(.{0,220}?)\s*(?=(?:🤝|👤|🚀)|The judgement is|$)",
    re.S)
OFFER = re.compile(r"Scaffolding\s*[–—-]\s*(Supported|Standard|Stretch)\s*(.{0,300})", re.S)

STOP = {"the", "a", "an", "and", "or", "of", "to", "in", "on", "at", "any", "kind",
        "this", "that", "is", "are", "it", "for", "with", "no", "not", "sheet",
        "paper", "tier", "here", "all", "your", "you", "if", "min", "mins",
        "minute", "minutes", "what", "which", "how", "one", "two", "each"}


def flat(src: str) -> str:
    """Tags out, THEN entities decoded. Skipping the unescape made v1 of this gate
    fail to find the tier table (the emoji are &#129309; etc. in source) and then
    report 'no breaches' — a gate returning clean on a file it could not read, which
    is the single failure this instrument exists to prevent. See the verdict logic:
    an unparsed file is now NOT CLEAN, never silent."""
    return " ".join(html.unescape(TAGS.sub(" ", SCRIPTSTYLE.sub(" ", src))).split())


def toks(s: str):
    return {w for w in re.findall(r"[a-z]+", s.lower()) if w not in STOP and len(w) > 2}


def assessed_files():
    out = subprocess.run(["git", "-C", str(REPO), "ls-files", "-z", "*.html"],
                         capture_output=True, check=True).stdout
    hits = []
    for f in (p for p in out.decode().split("\0") if p):
        if SELECTOR in (REPO / f).read_text(encoding="utf-8", errors="replace"):
            hits.append(f)
    return hits


def parse_card(t: str):
    """allowed / forbidden token sets per tier, from the Card's own table."""
    i = t.find("Conditions Card")
    if i < 0:
        return None
    card = t[i:i + 2600]
    out = {}
    for m in ROW.finditer(card):
        tier, body = m.group(1), m.group(2)
        # the row is "<allowed ...> <forbidden ...>"; split on the first forbidding cue
        cut = re.search(r"(New content|Frames,|Any content help)", body)
        allowed = body[:cut.start()] if cut else body
        forbidden = body[cut.start():] if cut else ""
        out[tier] = {"allowed_text": allowed.strip()[:170],
                     "forbidden_text": forbidden.strip()[:170],
                     "allowed": toks(allowed), "forbidden": toks(forbidden)}
    return out or None


def parse_offers(t: str):
    """Slice BETWEEN the Scaffolding headings rather than capturing a fixed window.
    v1 used finditer with a 300-char capture: the first match swallowed the Standard
    heading, finditer resumed past it, and Standard and Stretch came back EMPTY —
    which the gate would then have reported as 'nothing offered, nothing to check'.
    An empty offer is not an absent offer."""
    marks = [(m.start(), m.group(1), m.end())
             for m in re.finditer(r"Scaffolding\s*[\u2013\u2014-]\s*(Supported|Standard|Stretch)", t)]
    out = {}
    for k, (start, tier, end) in enumerate(marks):
        stop = marks[k + 1][0] if k + 1 < len(marks) else len(t)
        body = t[end:stop]
        body = re.split(r"\u2b50 Assessed Conditions Card", body)[0]
        out.setdefault(tier, body.strip()[:300])
    return out


def main():
    report = {"selector": SELECTOR, "files": [], "verdict": None,
              "cannot_see": "runtime state — backward navigation is unguarded in both "
                            "assessed files; a device-based access arrangement puts the "
                            "file's own We Do teaching one keypress from the assessed "
                            "slide. Not visible to any static instrument."}
    breaches = unruled = unparsed = 0
    for f in assessed_files():
        t = flat((REPO / f).read_text(encoding="utf-8", errors="replace"))
        card, offers = parse_card(t), parse_offers(t)
        entry = {"file": f, "card_parsed": bool(card), "tiers": {}}
        if not card:
            entry["ERROR"] = "no Conditions Card table found — CANNOT JUDGE THIS FILE"
            unparsed += 1
            report["files"].append(entry)
            continue
        for tier in TIERS:
            offer = offers.get(tier, "")
            c = card.get(tier)
            if not c:
                entry["tiers"][tier] = {"ERROR": "tier absent from the Card table"}
                continue
            ot = toks(offer)
            if re.search(r"No scaffold at this tier", offer):
                entry["tiers"][tier] = {"offer": "(declared: no scaffold)",
                                        "verdict": "DECLARED-ABSENCE — consistent"}
                continue
            entry["tiers"][tier] = {
                "offer": offer[:150],
                "card_allows": c["allowed_text"],
                "card_forbids": c["forbidden_text"],
                # These three are SIGNALS, not verdicts. Token overlap is a bag-of-words
                # heuristic: "account" appears in GROW's forbidden text ("anyone deciding
                # ... what the account argues") and also in its permitted Opening Frame,
                # so a raw overlap reads as a breach when it is not. The gate's job is to
                # put the two surfaces side by side and force a human to rule; it must not
                # pretend the ruling is derivable.
                "hint_matches_allowed": sorted(ot & c["allowed"]),
                "hint_matches_forbidden": sorted(ot & c["forbidden"]),
                "hint_unruled": sorted(ot - c["allowed"] - c["forbidden"]),
                "NEEDS_HUMAN_RULING": True,
            }
            breaches += len(entry["tiers"][tier]["hint_matches_forbidden"])
            unruled += 1 if entry["tiers"][tier]["hint_unruled"] else 0
        report["files"].append(entry)
    if unparsed:
        report["verdict"] = (
            "NOT CLEAN — %d file(s) could not be parsed at all. An unreadable file is "
            "never a pass. Fix the parser or the file before reading anything else "
            "here." % unparsed)
    elif unruled or breaches:
        report["verdict"] = (
            "NOT CLEAN — %d tier-offers carry content the Card does not mention, and "
            "%d overlap its forbidden text. Both are HINTS requiring a human ruling, "
            "not verdicts. Content the Card does not mention is the dangerous case: "
            "it is an absence in the Card, which no comparison can rule on."
            % (unruled, breaches))
    else:
        report["verdict"] = ("No breaches and nothing unruled in the static surface. "
                             "RUNTIME STATE REMAINS UNJUDGED — see cannot_see.")
    report["counts"] = {"files": len(report["files"]), "unparsed": unparsed,
                        "tier_offers_with_unruled": unruled, "forbidden_tokens": breaches}
    print(json.dumps(report, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
