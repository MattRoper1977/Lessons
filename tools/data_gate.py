#!/usr/bin/env python3
"""§9.7 data gate: roles ship, names do not - and nothing pupil-identifying ships at all.

    python3 tools/data_gate.py PACK_DIR [--fix] [--plant-dish] [--plant-name]

The regenerated surfaces carry a timetable, so this pack is the first that could
carry staff attribution onto a shared drive. Three separate questions, and they
have three different right answers - which is why this is a gate with rules
rather than one grep.

1. A NAMED TEACHER WHOSE ROLE IS KNOWABLE -> substitute the role, in the pack only.
   60 Science Teesside files carry, inside an HTML comment,
   "restore on Cheryl's confirmation". Invisible on the page, present in the file,
   and it names who is holding a confirmation up. The timetable assigns that work
   to the UAS coordinator, so the role is knowable and the substitution is exact.
   IT HAPPENS IN THE PACK ONLY. Those files are under the OPEN_ITEMS item 17
   byte-pristine hold and are not editable in the repo at all.

2. THE OWNER'S OWN NAME IN HIS OWN AUTHORED LESSONS -> report, never strip.
   "Mr Roper is the adult who'll set it up" is lesson text where the named adult
   is the point, in a pack going to that person's own school. Replacing it with a
   role would damage the lesson, and rewriting lesson text is authoring, which is
   not this pass's to do. Reported as owner-decision, shipped as written.

3. ANYTHING PUPIL-IDENTIFYING -> zero tolerance, no substitution, hard stop.

A name with no rule is a STOP, not a silent inclusion. That is the whole point:
the failure mode this gate exists for is a pack that ships a name because nobody
had written down what to do with it.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

# --- 1. named teacher -> role, applied to the pack only --------------------
ROLE_SUBS = [
    (re.compile(r"restore on Cheryl's confirmation"),
     "restore on the UAS coordinator's confirmation",
     "the timetable assigns UAS unit entry to the coordinator; the role is exact"),
    (re.compile(r"\bCheryl\b"),
     "the UAS coordinator",
     "catch-all for the same person named anywhere else"),
]

# --- 2. reported, never stripped -------------------------------------------
OWNER_NAME = re.compile(r"\bRoper\b|\bMr R\b|\bMatt(?:'s|&#x27;s)?\b")

# --- 3. pupil-identifying: zero, no exceptions -----------------------------
# Match the DATA, not the word for it. Every artefact here has to be able to state
# that it holds no reading ages without that sentence being the thing that fails -
# the planner ledger's own assurance line, "no pupil data, no reading ages", tripped
# the first version of this. Same lesson as the cooking census above: a gate that
# cannot tell a claim from an instance is useless.
PUPIL = {
    "reading age as data":  re.compile(r"\breading age\s*[:=]?\s*\d", re.I),
    "date of birth as data": re.compile(r"\b(?:date of birth|d\.o\.b\.?)\s*[:=]?\s*\d", re.I),
    "EHCP against a person": re.compile(r"\bEHCP\s*[:=#]?\s*(?:\d|[A-Z][a-z]+\s+[A-Z])", re.I),
    "Students sheet content": re.compile(r"\bStudents\s+sheet\b\s*[:=]", re.I),
    "pupil initials":       re.compile(r"\bpupil\s+[A-Z]\.\s?[A-Z]\.", re.I),
    "named pupil row":      re.compile(r"\b(?:pupil|student)\s+name\s*[:=]\s*[A-Z][a-z]+", re.I),
}

# --- the food census, re-run on the assembled tree -------------------------
# Named dishes ONLY, as explicit lists, and scoped to the surfaces THIS PASS
# created. Both of those constraints are borrowed from _passpq/tools/food_gate.py,
# which learned them the hard way and states the reason better than a comment here
# could: "the frame has to be able to TALK ABOUT recipes while containing none, and
# a gate that cannot tell those apart is useless."
#
# A first version of this census ignored both and reported four reds, every one a
# false positive: "Check the local recipe, allergies and equipment" in a Careers
# deck, "Method:" as an art technique, and a jacket potato inside a LAUNCH lesson
# about planning a balanced meal - pupil-facing lesson content that predates this
# pass and is supposed to name food.
#
# It also must never be built by splitting a pipe-delimited blob on whitespace.
# That produced empty alternatives matching at every position and tore "fish and
# chips" into three entries, making the bare word "and" a dish name: 495,372 hits.
DISHES = ["spaghetti bolognese", "shepherd's pie", "cottage pie", "fish and chips",
          "chilli con carne", "macaroni cheese", "toad in the hole", "bangers and mash",
          "victoria sponge", "flapjack", "scrambled eggs", "jacket potato",
          "tomato pasta", "chicken curry", "beef stew", "apple crumble"]
DISH_RE = re.compile(r"\b(?:" + "|".join(re.escape(d) for d in DISHES) + r")\b", re.I)
assert not DISH_RE.match(""), "the dish pattern matches the empty string"

# The surfaces PEQ-YEAR-3 and PEQ-YEAR-2 created. These must carry zero named
# dishes. Everywhere else in the pack, a named dish is pre-existing lesson content
# and is counted and reported, not failed.
PASS_SURFACES = {"Cooking_Handover.html", "COOKING_HANDOVER.md", "Kitchen_Week_Shell.html",
                 "Criteria_By_Week.html", "Kitchen_Completion_Checklist.html"}

# --- detecting a personal name that has no rule ----------------------------
# NOT by name shape. The assembled tree holds 3,015 distinct Capitalised-Capitalised
# pairs - "Independent Work", "Cold Call", "Arrival Task", "Even Better" - so
# shape alone is 3,015 false positives, and an allowlist that size is a place for a
# real name to hide rather than a control.
#
# A person is named in a NAMING CONTEXT: after a title, after a verb that addresses
# or attributes ("contact", "ask", "taught by", "signed by"), in a possessive about
# a decision ("X's confirmation"), or beside an email address. A first version of
# this gate matched titles only, and a planted "Contact Deborah Fairweather" walked
# straight through it.
NAME = r"[A-Z][a-z]{2,}(?:\s+[A-Z][a-z]{2,})?"
NAMING_CONTEXTS = [
    ("title",      re.compile(r"\b(?:Mr|Mrs|Miss|Ms|Dr|Sir)\.?\s+(" + NAME + r")")),
    # The verb is case-insensitive, the NAME group is NOT: a scoped (?i:...) rather
    # than re.I on the pattern, because a case-insensitive NAME matches every
    # lowercase word in the corpus. "Contact Deborah Fairweather." at the start of a
    # line walked through the first version for want of exactly this.
    ("addressed",  re.compile(r"\b(?i:contact|email|e-mail|speak to|talk to|ask|chase|"
                              r"confirm with|check with|see)\s+(" + NAME + r")\b")),
    ("attributed", re.compile(r"\b(?i:taught by|written by|signed by|assessed by|"
                              r"delivered by|verified by|per)\s+(" + NAME + r")\b")),
    ("possessive", re.compile(r"\b(" + NAME + r")(?:'s|&#x27;s)\s+"
                              r"(?:confirmation|say-so|sign-off|ruling|decision|class|group)")),
    ("beside mail", re.compile(r"\b(" + NAME + r")\b[^<>\n]{0,20}"
                               r"[A-Za-z0-9._%%+-]+@[A-Za-z0-9.-]+")),
]
# Words that are a role, a place or a product, never a person. Small, and every
# entry is here because it appeared in a naming context in the assembled tree.
NOT_A_PERSON = re.compile(
    r"^(?:The|This|That|Your|Our|Their|Each|Every|Both|All|Any|One|Two|Some|More|Most|"
    r"What|When|Where|Which|Who|How|Why|If|It|They|You|We|Use|Add|Put|Set|Make|Take|"
    r"Progress Schools|Tees Valley|Lundy Loop|Loop Lundy|Cold Call|Tutor Time|"
    r"Arts Award|Eatwell Guide|Gatsby Benchmarks|Independent Work|Living Independently|"
    r"Experiencing Work|Community Project|Witness Statement|Studio Time|Key Word|"
    r"Feedback Sheet|Arrival Task|Retrieval Quiz|Big Idea|Print Tools|"
    r"UAS|ASDAN|AQA|PEQ|Entry|Level|Award|Certificate|Science|English|Maths|"
    r"Humanities|Careers|Enterprise|Vocational|Teacher|Coordinator|Assessor)\b")

TEXT = {".html", ".txt", ".md", ".csv", ".js", ".css"}


def lowercase_vocabulary(pack):
    """Every word that appears LOWERCASE anywhere in the assembled tree.

    The discriminator between a name and an ordinary word, measured from the corpus
    rather than guessed. "nobody", "point", "scaffolding", "week" and "clouds" all
    occur in lower case somewhere; a person's name does not. This is what separates
    a real hit from the eight sentence-initial capitals that a naming-context regex
    inevitably picks up after "ask" or "taught by".
    """
    vocab = set()
    for p in files(pack):
        text = re.sub(r"<[^>]+>", " ", p.read_text(encoding="utf-8", errors="replace"))
        vocab.update(re.findall(r"\b[a-z]{3,}\b", text))
    return vocab


# Third-party libraries vendored into the pack. Their source carries author
# credits and contact addresses - jsPDF's contributors, PDF.js's - which are MIT
# licence ATTRIBUTION, not staff data. Stripping them would breach the licence.
# They are excluded from the personal-name census by path, and uas_pack.py asserts
# the vendored tree is byte-identical to the site repo's, so this exclusion cannot
# become a place to hide anything.
THIRD_PARTY = re.compile(r"(?:^|/)vendor/")


def files(pack, include_vendor=True):
    for p in sorted(pack.rglob("*")):
        if p.is_file() and p.suffix.lower() in TEXT:
            if not include_vendor and THIRD_PARTY.search(
                    str(p.relative_to(pack)).replace("\\", "/")):
                continue
            yield p


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        sys.exit("usage: data_gate.py PACK_DIR [--fix] [--plant-dish] [--plant-name]")
    pack = Path(args[0])
    fix = "--fix" in sys.argv

    if "--plant-dish" in sys.argv:
        t = pack / "ASDAN PEQ/Grow/PEQ_L2_Kitchen/Cooking_Handover.html"
        t.write_text(t.read_text(encoding="utf-8").replace(
            "</h1>", "</h1><p>Week 3: spaghetti bolognese, serves 4.</p>", 1), encoding="utf-8")
        print("*** PLANTED a dish name inside the assembled tree ***")
    if "--plant-name" in sys.argv:
        t = pack / "README_FIRST.txt"
        t.write_text(t.read_text(encoding="utf-8") + "\nContact Deborah Fairweather.\n",
                     encoding="utf-8")
        print("*** PLANTED an unruled personal name ***")

    vocab = lowercase_vocabulary(pack)
    print(f"corpus vocabulary: {len(vocab)} distinct lowercase words "
          "(the name-vs-ordinary-word discriminator)")
    subs, owner, pupil, dishes, kinds = 0, {}, {}, {}, {}
    unruled = {}

    for p in files(pack, include_vendor=False):
        text = p.read_text(encoding="utf-8", errors="replace")
        rel = str(p.relative_to(pack))
        new = text
        for pat, repl, _why in ROLE_SUBS:
            new, n = pat.subn(repl, new)
            subs += n
        if new != text:
            if fix:
                assert len(new) >= len(text) * 0.5, f"{rel}: substitution shrank the file"
                if p.suffix.lower() == ".html":
                    assert new.rstrip().endswith((">", "</html>")), f"{rel}: bad tail"
                p.write_text(new, encoding="utf-8")
            text = new
        for m in set(OWNER_NAME.findall(text)):
            owner.setdefault(m or "Matt", []).append(rel)
        for label, pat in PUPIL.items():
            if pat.search(text):
                pupil.setdefault(label, []).append(rel)
        for m in set(DISH_RE.findall(text)):
            bucket = dishes if p.name in PASS_SURFACES else kinds
            bucket.setdefault(m.lower(), []).append(rel)
        flat = re.sub(r"<[^>]+>", " ", text)
        for label, pat in NAMING_CONTEXTS:
            for m in set(pat.findall(flat)):
                cand = m.strip()
                if not cand or NOT_A_PERSON.match(cand) or OWNER_NAME.search(cand):
                    continue
                if any(p.search(cand) for p, _r, _w in ROLE_SUBS):
                    continue
                # a candidate whose every word also occurs in lower case in this
                # corpus is an ordinary word that happened to start a sentence
                if label in ("addressed", "attributed") and all(
                        w.lower() in vocab for w in cand.split()):
                    continue
                unruled.setdefault(f"{cand} ({label})", []).append(rel)

    print(f"\nrole substitutions {'applied' if fix else 'that WOULD apply'}: {subs}")
    for _pat, repl, why in ROLE_SUBS:
        print(f"   -> {repl!r}  ({why})")

    print(f"\nowner's own name, reported and shipped as written: "
          f"{sum(len(v) for v in owner.values())} occurrence(s) in "
          f"{len(set(f for v in owner.values() for f in v))} file(s)")
    for k, v in sorted(owner.items()):
        print(f"   {k:<12} {len(v)} file(s), e.g. {v[0]}")

    print(f"\npupil-identifying: {len(pupil)} pattern(s) matched")
    for k, v in pupil.items():
        print(f"   RED {k}: {len(v)} file(s) {v[:3]}")

    print(f"\ncooking content on the {len(PASS_SURFACES)} surfaces this pass created: "
          f"{len(dishes)} named dish(es)")
    for k, v in list(dishes.items())[:5]:
        print(f"   RED dish {k!r}: {v[:2]}")
    print(f"named dishes elsewhere in the pack (pre-existing lesson content, reported "
          f"not failed): {len(kinds)}")
    for k, v in list(kinds.items())[:5]:
        print(f"   note {k!r}: {v[:2]}")

    print(f"\nunruled personal names: {len(unruled)}")
    for k, v in unruled.items():
        print(f"   STOP {k!r}: {len(v)} file(s) {v[:2]}")

    problems = []
    if pupil:
        problems.append(f"{len(pupil)} pupil-identifying pattern(s)")
    if dishes:
        problems.append(f"{len(dishes)} named dish(es) on a surface this pass created")
    if unruled:
        problems.append(f"{len(unruled)} personal name(s) with no rule - owner decision")
    if not fix and subs:
        problems.append(f"{subs} role substitution(s) not yet applied (run with --fix)")

    print()
    if problems:
        print("[FAIL] data gate: " + "; ".join(problems))
        return 1
    print("[PASS] data gate: roles only, 0 pupil data, 0 cooking content on this pass's "
          "surfaces, 0 unruled names")
    return 0


if __name__ == "__main__":
    sys.exit(main())
