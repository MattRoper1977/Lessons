# Wave 3 plan — written, not run

Written in VB run 7. **Nothing in this file has been executed.** It is the
build order for runs 8 onward, and it can be edited before any of it happens.

## Shape

**Week-major across pathways, not pack-major.** One week's lesson is built for
every pathway that teaches that week before moving to the next week. Reason: a
run that finishes a whole pack leaves the other pathways with nothing teachable
for the same fortnight, and the first thing that goes wrong in a new chassis
shows up in the *second* family, not the second week of the first.

**Runs of at most 12 lessons**, hand-authored. Scripted byte-identical patches
across a family count as one edit; hand-authoring does not.

## The cells

BUILD Humanities Autumn, `'BUILD Weekly - Autumn'` column C, verbatim from
`_passsb/inputs/Build SOW 2026-2027.xlsx`:

| abs wk | workbook term | cell | outcome (verbatim) | we-do type |
|---|---|---|---|---|
| 1 | Aut1·W1 | C46 | Talk about my family and people special to me. | commit-and-reveal — **built** |
| 2 | Aut1·W2 | C47 | Identify people who help us in the community. | sort-or-match |
| 3 | Aut1·W3 | C48 | Recognise places in my local community. | label-or-annotate |
| 4 | Aut1·W4 | C49 | Sort 'then and now' photographs. | sequence-or-rank |
| 5 | Aut1·W5 | C50 | Show respect for what makes us same/different (Black History Month). | predict-then-check |
| 6 | Aut1·W6 | C51 | Contribute to a class community map. | spot-the-error |
| 7 | Aut1·W7 | C52 | Share a group/team/community I belong to. | commit-and-reveal |
| 8 | Aut2·W1 | C53 | Explore a festival of light and why it matters. | sort-or-match |

Note the spine: **C53 is Aut2·W1, which is absolute week 8.** The pack spans
Autumn, not Autumn 1. Anything that labels weeks 1–8 "Autumn 1" is wrong.

## The we-do rotation

`wedo.rotation` in the contract requires no type to repeat within three
consecutive weeks of the same family. The column above satisfies it: the two
`commit-and-reveal` weeks are 1 and 7 (six apart), the two `sort-or-match`
weeks are 2 and 8 (six apart).

The type is not chosen to fill the rotation — it is chosen because it fits the
outcome, and the rotation is then checked. Week 4 sorts photographs, so
`sequence-or-rank`. Week 6 builds a shared map, so `spot-the-error` on a map
with a deliberate mistake. Where the fit and the rotation disagree, the fit
wins and the rotation constraint gets raised as a question rather than
silently satisfied.

## Runs

- **Run 8** — weeks 2 and 3 (C47, C48). Two lessons, not more. First run on the
  new contract after the proof lesson, so the point is to find out what the
  proof lesson got away with rather than to cover ground. Front door relinked,
  checksums, full battery each, engine-artefact control in the same session.
- **Run 9** — weeks 4, 5, 6 (C49–C51). Week 5 is Black History Month: the
  outcome is *"show respect for what makes us same/different"*, which is a
  respect outcome, not a history-of-a-group outcome. It gets built to the
  workbook's wording and no further, and it is the one to put in front of a
  second pair of eyes before it lands.
- **Run 10** — weeks 7 and 8 (C52, C53), then the pack closes: manifest,
  checksums, front door with every week linked, catalogue entry.

## Before run 8 starts

1. **Matt's ruling on reading level** (see `PROOF_LESSON_NOTES.md`). Weeks 2–8
   are pitched from the answer. If there is no answer by run 8, weeks 2 and 3
   are built at the proof lesson's level and flagged, not held.
2. **The blank-row count** on the print worksheet, from teaching week 1.
3. `resources.json` / catalogue entry for the pack — **its own PR, alone**,
   per §0.13. Not stacked with a content run.

## What wave 3 does not do

No other family is started. No live lesson is re-judged against the new
contract rows (they are `scope: "new"`). No overload found in Phase 2 is split
or trimmed. The three UNRESOLVED timetable cells stay unresolved and no lesson
is assigned to them.
