# ART_DONOR_v1 — the chassis Art is authored onto

Order VB-EASTER-A3N-2 §1. **Not lessons.** Three stripped chassis, one per
pathway, with every word of their donors' teaching removed and the furniture the
gates read left in place.

## Why three and not one

§1a says the donor comes from the SAME pathway. That is not a preference. g26
derives the pathway from the ROUTE and reds a deck whose pupil Flesch-Kincaid
sits outside that pathway's band — BUILD 1.0–4.0, GROW 3.0–7.0, LAUNCH a ceiling
of 14.21. A single pathway-neutral chassis makes g26 return NOT-APPLICABLE: a
fail-open on the one gate that reads how the lesson speaks to a child. So the
route of each file carries its pathway token, and `prove_chassis.py` treats
NOT-APPLICABLE as a failure rather than a pass.

## What is in each file

| kept | removed |
|---|---|
| the nine-stage spine and per-stage `data-min` | every teaching block in every stage |
| the Lundy strip in its three places | the donor's two explanatory diagrams |
| the guide toggle and its staff drawer | every print-pack sentence, heading and criterion |
| the print pack's pages, tiers and table shells | the running head |
| the splash, progress control and navigation labels | every field of the donor's `lesson-config` |
| exactly one `:root` block | |

Text shared by reference decks from **two or more families** is kept as
furniture; text in only one family is the donor's and goes. That line is derived
from a reference set with a recorded digest, not drawn by hand — see
`tools/easter/GREEN_REFERENCE_DECKS.json`.

## Provenance

| chassis | stripped from | margin |
|---|---|---|
| `BUILD_chassis.html` | `BUILD_ASDAN/Autumn1_W1-W7_2026-27/BUILD_ASDAN_W3_Cook_One_Snack_as_a_Team_from_a_Picture_Card.html` | 0.135 |
| `GROW_chassis.html` | `Humanities_Teesside/GROW_W1-W8_2026-27/GROW_Humanities_W3_Match_the_Lamp_to_Its_Meaning.html` | 0.431 |
| `LAUNCH_chassis.html` | `LAUNCH_ASDAN/Autumn1_W1-W7_2026-27/LAUNCH_ASDAN_W1_Choose_Our_Community_Need_and_Launch_My_Challenge.html` | 0.194 |

Each file records its own donor and that donor's sha256 inside its
`lesson-config`, under `chassis`. `prove_chassis.py` reads the baseline from
there rather than being told, so the two cannot drift apart.

## How they were proved

A chassis has no pupil words, so g18's family floor and g23's period load are
not green on it — they are meaningless on it, and a report saying PASS would be
measuring nothing. Each chassis was proved by authoring a **real planned Art
lesson** onto it and running the whole stack on that, with every gate also run
on the donor so a red the estate already carries is never reported as this
work's defect. The probe decks are not committed; this PR ships zero lesson
units.

    python3 tools/easter/prove_chassis.py --chassis <file> --plan-index N \
        --content <json> --reference <deck>

## Re-deriving them

    python3 tools/easter/pick_art_donor.py                    # the choice, with margins
    python3 tools/easter/strip_to_chassis.py --donor <deck> \
        --out tools/donors/ART_DONOR_v1/<PATHWAY>_chassis.html --id ART_CHASSIS_<PATHWAY>
