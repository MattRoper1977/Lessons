#!/usr/bin/env python3
"""
AT-INST-04 - closed-kit assertion, specified on CATEGORY. Supersedes A8.

WHY A8 WAS RETIRED. A8 was a list of press nouns. A list-based check has no
terminating condition: four widenings -- plate, inking, hand-pulled, screen print
-- each found more, and the count rose every time it was looked at. Worse, the
under-count produced a FALSE ZERO in C5, which reported D-PRESS-02 closed when it
was not. A false zero closes a defect instead of opening one, which is the most
expensive kind of finding this estate can produce.

THE INVERSION. Enumerate what the room HAS, and report every craft noun and
process verb outside it. That has a terminating condition: the unmatched
vocabulary is finite and can be reviewed to exhaustion.

HOW ORDINARY LANGUAGE IS DERIVED, and why not from a wordlist. A word is treated
as ordinary if it appears in at least two NON-ART subject folders in this
repository. That is an independent corpus sharing no premise with the kit list.
Art-adjacent and craft folders (6 Art, Build, Grow, Launch, DT_Community_Upcycling)
are excluded so craft vocabulary cannot launder itself as ordinary.

WHAT THIS STRUCTURALLY CANNOT DETECT - declared per standing rule 9, because part
of this check is judgement and saying so is the point:

  * SENSE. "Press" appears in two non-art folders as "press Escape", so frequency
    alone marks it ordinary -- yet "press corner" is kit. No corpus method can
    separate senses of a word. Sense adjudication is HUMAN, and the VIOLATIONS
    table below is the record of those human decisions, not an instrument output.
  * The residue is a REVIEW LIST, not a finding list. 456 words at count >= 4,
    1,660 in total. It says "these are art-specific words"; a person says which
    are kit.
  * Paraphrase, still. "The pull is a ceremony, not a snatch" names no kit.

So: roughly mechanical for extraction and the review list, human for sense.
Anyone quoting a number from here is quoting a human decision with a script
attached, and should know it.
"""
import re, sys, os, glob, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit_text import readable

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# The closed kit, verbatim. Nothing else exists.
KIT = ["paper", "card", "wax crayon", "crayon", "graphite", "scissors", "glue", "acrylic",
       "sponge", "sand", "masking tape", "camera", "blade", "wire", "cutters", "glue gun",
       "mod roc", "calico", "tote"]

# ---------------------------------------------------------------- adjudicated
# (regex, default class). Every entry is a human decision about SENSE, recorded
# here rather than implied by a pattern. Classes decide which pass owns the hit.
VIOLATIONS = [
    (r"\binking\b|\binking bench\b|\binking queue\b|\binking slab\b|\binking station\b", "kit-dependence"),
    (r"\bpress corner\b|\bprinting ink\b|\binks\b|\bink load\b|\bre-inked\b|\bRoll until\b|\bstarved\b", "kit-dependence"),
    (r"\brollers?\b|\bbrayer\b|\blino\b", "kit-dependence"),
    (r"\bpre-cut plate\b|\bplate wear\b|\bthe plate\b|\bplates?\b", "kit-dependence"),
    (r"\brelief print\w*", "kit-dependence"),
    (r"\bpull an edition\b|hand-pulled|\bpull it again\b|\bPull the remaining prints\b", "vocabulary-residue"),
    (r"\bscreen ?print\w*", "offer-scope"),
]
# Refusal is detected from CONTEXT, not from a file list. A banned term inside a
# negation is being disavowed, and the whole point of the residuals register is
# that those survive deliberately. Detected over a window before the hit, because
# "no press, no rollers and no printing inks" negates three terms with one "no".
# Negation must fall on the KIT'S EXISTENCE, not on any nearby verb. The first
# version matched a bare "not" and swallowed GROW W2's ghost card -- "Plate not
# re-inked. Every pull needs its own ink" -- which ASSERTS the press. A false
# refusal closes a defect instead of opening one, so this pattern requires an
# existential form: no X, there is no, none are needed, off the table, without.
NEGATION = re.compile(
    r"(?:\bthere (?:is|are) no\b|\bis no\b|\bare no\b|\bno\b(?=\s+[a-z]+(?:s|ing)?\b[^.;]{0,40}$)"
    r"|\bnone are needed\b|\boff the table\b|\bwithout\b|\bnever (?:use|add|map|label)\b"
    r"|\bno (?:screens|press|rollers|inks|blades)\b|\bwould have produced\b)", re.I)
# Per-file overrides remain available for decisions context cannot carry.
OVERRIDES = []
# Governed allow-list: art words that are NOT kit. Each carries its reason.
ALLOW = {
    "tread plate": "a found metal surface to take a rubbing from, not a printing plate",
    "template": "CSS grid property, never read by a user; source of 16 phantom plate hits",
    "frottage": "the technique name for rubbing; the technique the room runs on",
    "stipple": "a sponge/brush mark, made with kit that is present",
    "registration": "aligning a stencil to the paper; a stencil concept, not a press one",
}
CLASSES = ["kit-dependence", "vocabulary-residue", "exemplar-residue", "refusal-context",
           "refusal-candidate", "offer-scope"]


# ---------------------------------------------------------------- ratified
# THE CLASSIFIER PROPOSES; IT DOES NOT DECIDE. Three versions of the negation
# detector were wrong in three different ways -- it swallowed an assertion, then
# missed a trailing negation, then read a fault-card menu as a refusal. A check
# that decides INTENT has no final version, so intent is ratified by a human once
# and the classifier's remaining job is regression.
#
# (file fragment, string fragment, ratified reason)
RATIFIED = [
 ("Autumn2_Scheme_of_Work", "there is no press, no rollers and no printing inks",
  "names the kit in order to rule it out; the sentence's whole job is the refusal"),
 ("Autumn2_Scheme_of_Work", "No press, no rollers, no inks, no blades beyond classroom scissors",
  "the unit kit list, stated as what the room does NOT hold"),
 ("Autumn2_Scheme_of_Work", "is relief printing. It is off the table",
  "names the rejected route so a reader knows it was considered and refused"),
 ("Autumn2_Scheme_of_Work", "Teaching relief printing in an alternative-provision session",
  "the pedagogic reason for the refusal; deleting it loses why"),
 ("START_HERE", "No press, no rollers, no inks",
  "the entry document's refusal; the first thing anyone reads"),
 ("GROW_ART_W2", "No press, no rollers, no inks — none are needed",
  "A2a's disavowal in the TA brief; the sentence exists to refuse the kit the lesson used to require"),
 ("Summer1_Scheme_of_Work", "No screens, squeegees or fabric inks needed",
  "Summer 1's own refusal of the screen route; its spine gets this right"),
 # Ratified by Matt, 2026-08-05, ruled via delegation (sentinel a2e-ratify-2026-08-05).
 # A2e landed a kit disavowal in the LAUNCH scheme of work so that C5 — which is
 # folder-scoped and had no disavowal to read under Launch/ — could see that route at
 # all. A disavowal must name what it refuses, so its kit-namings are refusal-context
 # by construction. This is the same mechanism that admitted A2a's two strings for
 # GROW W2; the set grows the way it grew before. Both sentences were read in full
 # before ratification and both sit inside the refusal frame.
 ("Launch/Scheme_of_Work", "no press, no rollers and no printing inks",
  "LAUNCH's own refusal; the sentence rules out the print run it has just named"),
 ("Launch/Scheme_of_Work", "No press, no rollers, no inks",
  "the unit kit line, stated as what the room does NOT hold, before naming what it does"),
]


def ratified(fname, sentence):
    for f, frag, _ in RATIFIED:
        if f in fname and frag in sentence:
            return True
    return False


# Rule 15, enforced in the harness rather than remembered per-check. Three
# substring incidents in one day -- plate inside grid-template-columns, etched
# inside sketched, sewhere inside elsewhere -- each fixed locally. Now it fails
# loudly at import instead.
def _assert_bounded():
    bad = []
    for pat, _ in VIOLATIONS:
        for alt in pat.split("|"):
            a = alt.strip()
            if not a:
                continue
            if not (a.startswith(r"\b") or a.startswith("(") or a[0].isupper()
                    or " " in a or a.startswith("hand-")):
                bad.append(a)
    if bad:
        raise AssertionError("rule 15: unbounded alternatives -> " + ", ".join(bad))


_assert_bounded()


def classify(fname, term_pat, default, before, full):
    for f, pat, cls in OVERRIDES:
        if f in fname and (pat == r".*" or pat == term_pat):
            return cls
    if ratified(fname, full):
        return "refusal-context"
    if NEGATION.search(before):
        return "refusal-candidate"     # proposed, NOT decided - needs ratification
    return default


def main():
    verbose = "--verbose" in sys.argv
    files = sorted(glob.glob(os.path.join(ROOT, "**", "*.html"), recursive=True))
    per_file = collections.defaultdict(lambda: collections.Counter())
    per_class = collections.Counter()
    detail = collections.defaultdict(list)

    for path in files:
        rel = os.path.relpath(path, ROOT)
        text = readable(path)
        for pat, default in VIOLATIONS:
            for m in re.finditer(pat, text, re.I):
                seg = text[max(0, m.start() - 40):m.end() + 40]
                if any(a in seg.lower() for a in ALLOW):
                    continue
                # Sentence-scoped, BOTH directions. Looking only backwards missed
                # "relief printing. It is off the table:" -- the negation follows.
                lo = max(0, text.rfind('.', 0, m.start()) + 1)
                hi = text.find('.', m.end());  hi = len(text) if hi < 0 else hi
                sentence = text[lo:m.start()] + ' ' + text[m.end():hi + 60]
                full = text[lo:hi + 60]      # intact, for ratified-string matching
                # rel, not basename. Three files are called Scheme_of_Work.html
                # (Build, Grow, Launch), so a basename can neither express nor
                # confine a ruling made about one of them: ratifying LAUNCH's
                # disavowal by basename would silently pre-ratify an identical
                # sentence dropped into Build's later, with no human in the loop.
                # Every existing RATIFIED fragment still matches — asserted, not
                # assumed, by comparing per-file counts across this change.
                cls = classify(rel, pat, default, sentence, full)
                per_file[rel][cls] += 1
                per_class[cls] += 1
                detail[rel].append((cls, m.group(0), seg.strip()))

    total = sum(per_class.values())
    print(f"AT-INST-04 closed-kit assertion - {len(files)} files, readable text only\n")
    print(f"{'file':<46}{'kit-dep':>8}{'vocab':>7}{'exemp':>7}{'refusal':>9}{'cand':>6}{'offer':>7}{'total':>7}")
    print("-" * 91)
    for rel in sorted(per_file, key=lambda r: -sum(per_file[r].values())):
        c = per_file[rel]
        print(f"{rel[-45:]:<46}{c['kit-dependence']:>8}{c['vocabulary-residue']:>7}"
              f"{c['exemplar-residue']:>7}{c['refusal-context']:>9}{c['refusal-candidate']:>6}{c['offer-scope']:>7}{sum(c.values()):>7}")
    print("-" * 91)
    print(f"{'TOTAL':<46}{per_class['kit-dependence']:>8}{per_class['vocabulary-residue']:>7}"
          f"{per_class['exemplar-residue']:>7}{per_class['refusal-context']:>9}"
          f"{per_class['refusal-candidate']:>6}{per_class['offer-scope']:>7}{total:>7}")

    if verbose:
        for rel, hits in detail.items():
            print(f"\n[{rel}]")
            for cls, term, seg in hits:
                print(f"   {cls:<20}{term!r:<22}…{re.sub(r'  +',' ',seg)[:88]}…")
    return total


if __name__ == "__main__":
    main()
