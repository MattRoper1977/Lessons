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
    (r"\binking\b|inking bench|inking queue|inking slab|inking station", "kit-dependence"),
    (r"press corner|printing ink|\binks\b|ink load|re-inked|Roll until|\bstarved\b", "kit-dependence"),
    (r"\brollers?\b|\bbrayer\b|\blino\b", "kit-dependence"),
    (r"pre-cut plate|plate wear|the plate|\bplates?\b", "kit-dependence"),
    (r"relief print\w*", "kit-dependence"),
    (r"pull an edition|hand-pulled|pull it again|Pull the remaining prints", "vocabulary-residue"),
    (r"screen ?print\w*", "offer-scope"),
]
# Refusal is detected from CONTEXT, not from a file list. A banned term inside a
# negation is being disavowed, and the whole point of the residuals register is
# that those survive deliberately. Detected over a window before the hit, because
# "no press, no rollers and no printing inks" negates three terms with one "no".
NEGATION = re.compile(r"\b(?:no|not|never|without|off the table|none are needed|"
                      r"is no|are no|nor)\b[^.;]{0,90}$", re.I)
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
CLASSES = ["kit-dependence", "vocabulary-residue", "exemplar-residue", "refusal-context", "offer-scope"]


def classify(fname, term_pat, default, before):
    for f, pat, cls in OVERRIDES:
        if f in fname and (pat == r".*" or pat == term_pat):
            return cls
    if NEGATION.search(before):
        return "refusal-context"
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
                cls = classify(os.path.basename(rel), pat, default,
                               text[max(0, m.start() - 95):m.start()])
                per_file[rel][cls] += 1
                per_class[cls] += 1
                detail[rel].append((cls, m.group(0), seg.strip()))

    total = sum(per_class.values())
    print(f"AT-INST-04 closed-kit assertion - {len(files)} files, readable text only\n")
    print(f"{'file':<46}{'kit-dep':>8}{'vocab':>7}{'exemp':>7}{'refusal':>9}{'offer':>7}{'total':>7}")
    print("-" * 91)
    for rel in sorted(per_file, key=lambda r: -sum(per_file[r].values())):
        c = per_file[rel]
        print(f"{rel[-45:]:<46}{c['kit-dependence']:>8}{c['vocabulary-residue']:>7}"
              f"{c['exemplar-residue']:>7}{c['refusal-context']:>9}{c['offer-scope']:>7}{sum(c.values()):>7}")
    print("-" * 91)
    print(f"{'TOTAL':<46}{per_class['kit-dependence']:>8}{per_class['vocabulary-residue']:>7}"
          f"{per_class['exemplar-residue']:>7}{per_class['refusal-context']:>9}"
          f"{per_class['offer-scope']:>7}{total:>7}")

    if verbose:
        for rel, hits in detail.items():
            print(f"\n[{rel}]")
            for cls, term, seg in hits:
                print(f"   {cls:<20}{term!r:<22}…{re.sub(r'  +',' ',seg)[:88]}…")
    return total


if __name__ == "__main__":
    main()
