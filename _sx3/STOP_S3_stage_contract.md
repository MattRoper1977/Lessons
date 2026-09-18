# STOP-S3 — the stage-count ten do not just change a number; they leave the contract

ORDER SX3-FINISH2 held the stage count as Matt's call. Measuring it produced a
larger finding, so it is reported before any ruling is asked for.

## Search scope

The ten `expectedStageCount`-pinned decks that are in the landing 56.
**Current** = the file at `origin/main`. **Proposed** = the same path on its sx3
branch (`claude/sx3-build-2`, `claude/sx3-grow-2`). **Pin** =
`tools/easter/SCIENCE_ORIGINAL_TARGETS.json`. Instrument = the same rule
`science_original_browser.cjs` uses (every `.slide` element and its `data-title`
/ `data-timer`), read here by **static parse**. Static, not rendered: a browser
confirmation is still owed before any of this is called a PASS, per the standing
rule. It is reported as a measurement of the files, not as a gate verdict.

## The count

| deck | pin | main | pack |
|---|---|---|---|
| `SCI_B_W3_Backbones.html` | 12 | 12 | 13 |
| `SCI_B_W4_Muscle_Pairs.html` | 12 | 12 | 13 |
| `SCI_B_W5_Right_Nutrition.html` | 12 | 12 | 13 |
| `SCI_B_W6_Balanced_Plate.html` | 12 | 12 | 13 |
| `SCI_B_W7_Where_Food_Comes_From.html` | 12 | 12 | 13 |
| `SCI_G_W3_Friction.html` | 10 | 10 | 13 |
| `SCI_G_W4_Mechanisms.html` | 10 | 10 | 13 |
| `SCI_G_W5_Fair_Test.html` | 10 | 10 | 13 |
| `SCI_G_W6_Earth_And_Planets.html` | 10 | 10 | 13 |
| `SCI_G_W7_The_Moon.html` | 10 | 10 | 13 |

Timer sums are 80 on both sides for all ten, against a `periodMinutes` target of
`[40, 40]`.

## The larger finding — the stage *names* are gone

Main's stages are structural labels. The pack's are content titles.

```
main (SCI_B_W3): Title, Arrival Task, Today at a Glance, I Do 1, I Do 1b,
                 We Do 1, We Do 1b, I Do 2, We Do 2, Independent Work,
                 Lundy Loop, Exit Ticket
pack (SCI_B_W3): Backbones and No Backbones, Four clues to start, What would
                 count as evidence?, Look inside: find the backbone, Sort using
                 body evidence, Show the rule, not a guess, Two small checks,
                 Backbone evidence lab, Predict, reveal, then use the evidence,
                 Does your choice fit the evidence?, Make one mystery animal
                 card, Keep or change one idea, Use the rule in a new case
```

Not one label survives, on any of the ten. `science_original_browser.cjs` makes
three assertions about those labels. All three hold on main and fail on the pack,
for all ten:

| assertion | source | main | pack |
|---|---|---|---|
| active slide's `data-title` is `Title` | `title()` | 10/10 pass | **0/10** |
| `.slide` count equals `expectedStageCount` | `minutes()` | 10/10 pass | **0/10** |
| a stage named `Independent Work` exists at index > 0 and carries `independentMinutes` (32) | `minutes()` | 10/10 pass (32 = 32) | **0/10 — no such stage** |

The third is the one that matters most. `minutes()` finds `Independent Work` by
name and uses its index to split the two 40-minute sessions
(`sessionCount === 2`). With no stage of that name, `findIndex` returns `-1`,
`assert.ok(index > 0)` fails, and the session split cannot be computed at all.

## What this changes about the question

The question is not "does the stage count go 12/10 → 13". It is: **the pack decks
do not implement the Original Science stage contract.** Re-pinning
`expectedStageCount` to 13 would satisfy one of the three assertions and leave the
other two failing.

This is the same root as the "Original Science navigation" defect ORDER SX3-END4
required be root-caused before any content change. It is that defect, named: the
pack authors stages by content title; the estate's gate addresses them by
structural label.

## Requested ruling

Three options, and I am not choosing:

1. **Restore the structural labels** in the pack decks — the transplant carries
   `data-title`/`data-timer` from the chassis rather than the pack, and
   `expectedStageCount` stays 12/10. Keeps the contract; needs the 13 pack stages
   mapped onto 12/10 chassis slots, which may not be possible without dropping a
   stage.
2. **Re-author the contract** — teach `science_original_browser.cjs` to find the
   independent-work stage by something other than a literal name, and re-pin all
   ten counts to 13. A gate change, and a large one.
3. **Hold all ten** out of this release and land the other 36.

Until ruled, all ten stay HELD and appear in no PR — which is option 3 by
default, not by decision.
