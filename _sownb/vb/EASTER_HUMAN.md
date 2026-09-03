# EASTER HUMAN ITEMS — campaign VB_EASTER_A3

A human item blocks only the plans that need its answer. It never blocks a
family and never blocks the campaign. Each carries the question, the evidence,
and the cells held.

---

## A3-H1 — three cells the coverage instrument cannot score

**Cells held: 3.** Their workbook outcomes carry no distinctive words once
stopwords and corpus-ubiquitous terms are removed, so the SERVES test cannot be
evaluated in either direction. Each already has a standing deck that claims it.

| cell | ruled week | standing deck | verbatim outcome |
|---|---|---|---|
| `'GROW Weekly - Autumn'!C150` | 7 | `GROW_ASDAN/Autumn1_W7_2026-27/GROW_ASDAN_W7_A_Visitor_And_The_Evidence_We_Keep.html` | "Record challenge evidence." |
| `'BUILD Weekly - Spring'!C112` | 16 | `BUILD_ASDAN/Spring1_W1-W6_2026-27/BUILD_ASDAN_W15_Choice_Budget_and_Project_Reset.html` | "Make a choice and say why." |
| `'BUILD Weekly - Spring'!C113` | 17 | `BUILD_ASDAN/Spring1_W1-W6_2026-27/BUILD_ASDAN_W16_Partner_Challenge_and_Seasonal_Goals.html` | "Work with a partner to complete a task." |

**The question, Matt:** does each standing deck teach its outcome? If yes, the
cell is covered and needs no deck. If no, it needs one and joins the target list.

**Why this is not a measurement to improve.** "Make a choice and say why" is four
content words, every one of which appears in most lessons in the estate. Lowering
the distinctiveness floor to score it would make the instrument fire on almost
anything, which is the fail-open the run-13 threshold exists to prevent. The
honest answer is that this outcome is not machine-scorable, and a person should
read the deck.

**Evidence:** `_sownb/vb/evidence/run14/CELL_COVERAGE.json` → `unscorableClaims`;
re-derivable at any time by `_sownb/vb/tools/cell_coverage.py`.

---

## A3-H2 — GROW_HUM_W15 and LAUNCH_HUM_W15 are split candidates

Carried from A2R §4.4, unresolved.

| deck | words | family median | ratio |
|---|---|---|---|
| `GROW_HUM_W15_Rights_Timeline_and_Belief_Resilience.html` | 3529 | 906 | **3.90** |
| `LAUNCH_HUM_W15_Conflict_Causes_and_Ethical_Decisions.html` | 3526 | 822 | **4.29** |

Both declare 40 minutes, so neither is a double period. In both, the overload is
one stage: "I Do 2 · connect" carries ~1,450 words against a 3-minute
declaration, where the same stage in the sibling deck carries 108. Deleting that
stage outright still leaves them near ×2.3; reaching ×1.25 would move about 70%
of the lesson into the drawer, which is not a trim by any reading of the run-11
R5.5 precedent.

**The question:** split each across two periods, or accept a heavy single period
with the overload moved to the drawer? This order's §0c trims them once first;
whatever remains above ×1.6 comes back here.

**Cells held:** none — both decks stand and their cells read covered.

---

## A3-H3 — 19 stale `lesson-config` week labels block the reshell recipe

Carried from A2R, unresolved, and it blocks reshell plans specifically.

The recipe refuses a source whose `lesson-config` week disagrees with the ruled
week of the workbook cell it cites — correctly, as a red control. 19 decks
disagree, **every one by exactly +1**, and every one is a week 14/15/16 deck
whose config carries a filename-era label the run-11 spine re-key left behind.
Meanwhile all 30 decks the recipe *would* accept are already classic-shell, so
reshelling them is a no-op.

**The repair is the 19 labels, not the check.** Correcting them to the ruled week
of their cited cells is a register PR with a planted control. Until it lands, no
n6 deck can be reshelled.

**Cells held:** none directly; the five §1e RESHELL plans may need this first.

---

## A3-H4 — carried, unchanged

- **H14-1 `RULE_CHOICE=<a|b>`** — two pupil-facing rules, no one game file can
  satisfy both. Evidence `_sownb/vb/evidence/run14/R5_TWO_RULES.json`.
- **C100** — LAUNCH ASDAN week 15, E3-L1 versus live Level 2. Matt + Cheryl.
- **ASDAN g16 reference ruling** — g16 passes on 0 of 10 BUILD ASDAN and 0 of 14
  GROW ASDAN decks. Which live deck is each family's reference is a ruling, not
  a measurement.
- **The 54-deck classic-v2 contract backlog** — 54/54 lack stage timings, 24/54
  lack their own lesson-config, 24/54 miss Lundy in one of its three places. CI
  prints the distribution every run, report-only, until the backlog is zero.

---

## A3-H5 — the Lundy banner is counted once per stage, and it is what puts three decks over

**Cells held: none.** Three standing decks are affected; none of their cells is
blocked. This is a ruling about a measurement, not about a lesson.

The three W16 Humanities decks read over the 1.25 operative target. Their excess
is almost entirely one thing: the pupil-facing Lundy banner, printed identically
on every stage.

> "Space means you get room to join in." · "Voice means you get to say it." ·
> "Audience means someone really listens." · "Influence means something changes
> because of what you said."

| deck | ratio | words over target | Lundy banner words | ratio counting banner once |
|---|---|---|---|---|
| `BUILD_HUM_W16_Then_And_Now_And_What_Is_Fair.html` | 1.53 | 394 | **383** | 1.26 |
| `GROW_HUM_W16_Sources_Campaigns_And_Hope.html` | 1.38 | 116 | **112** | 1.25 |
| `LAUNCH_HUM_W16_Steps_In_Law_And_What_Comes_After.html` | 1.28 | 26 | **144** | 1.11 |

**The question, Matt:** should g23 count a banner repeated verbatim on every
stage once, or once per stage?

**Why I have not just done it.** Both readings are defensible. A pupil reads the
banner once and thereafter recognises it, which argues for counting it once. It
also occupies the slide on every stage and a pupil with a reading difficulty may
re-read it, which argues for counting it as it appears. What is not defensible is
me choosing: discounting a cross-stage refrain makes **every deck in the estate**
pass g23 more easily, and §5 of this order forbids loosening a threshold. A
measurement may be corrected when a planted control proves the old one wrong —
but here the old measurement is not wrong, it is answering a different question
from the one we want asked.

**What happens if it stands as is.** The three decks need ~394, ~116 and ~26
words of real teaching moved into the staff drawer, to compensate for a banner
the estate's own contract requires them to carry (`lundy-in-three-places`). That
is a lesson made worse to satisfy a counting artefact, so I have not done it.

**What happens if the banner is counted once.** All three land at or under the
threshold with no edit at all, and the correction is recorded in
WRONG_BEFORE_RIGHT with a planted control — a deck whose only excess is a refrain
passes, and a deck with genuinely repeated *teaching* still reds.

**Evidence:** re-derivable at any time; the per-deck figures above come from
`_sownb/vb/tools/g23_period_load.py` plus a cross-stage repeat count over
`lesson_stages.stages()`.


---

## A3-H6 — 7,593 words of duplicated instruction, 19 decks, one generator

**Found:** 2026-09-03, while trimming the third of three W15 Humanities decks.
**Status:** measured, projected, not applied. Needs your scheduling decision.

Three Humanities decks were de-duplicated one at a time (#280, #281, #282) and
all three carried the same defect in the same stage. That is not three authoring
accidents — a uniform ×4 repeat inside one named stage is a generator emitting
its task paragraph more than once. So the whole estate was asked the same
question with the same read-only instrument.

    377 decks scanned · 24 affected · 19 with removable duplication
    7,593 removable words · 170 sentences at exactly ×4, 17 at ×2

**What a pupil currently reads.** In `SCI_B_W16B` the eight-sentence task block
("Place two approved fossil images side by side. Describe each before
comparing…") appears **four times running** inside one flat paragraph. There is
no tier label, no heading, nothing that would make the repetition read as three
differentiated versions. The same eight instructions, four times.

**It is not missing differentiation.** I checked, because if the loop had been
meant to emit three tiers then dedupe would leave the deck short of content.
The clean sibling `SCI_B_W14A` has the identical stage structure — three
distinct `<h3>` tier headings, each with its own `<p>` — and differs only in the
task paragraph, 108 words against 597. Nothing is missing. Dedupe restores the
authored shape.

**Ten of the nineteen are live g23 ceiling reds on main right now**, and nobody
has reported them, because §0c was scoped to Humanities. De-duplication alone
clears five of the ten:

| group | decks | ratio now | after dedupe | outcome |
|---|---|---|---|---|
| Science — Build/Grow/Launch, W7 and W14–W20 | 14 | ×1.28–1.78 | ×1.09–1.49 | every one PASSES; 5 reds cleared, 7 reach the 1.25 target |
| ASDAN Spring1 W15/W16 — BUILD ×2, GROW ×2, LAUNCH ×1 | 5 | ×2.40–3.08 | ×1.97–2.57 | **still red** |

Those ratios are measured, not calculated: `dedupe_sweep.py --project` copies
each deck, dedupes the copy and re-runs g23. The repository is never written to,
and a planted mutation that made it write the source reds its own control.

**The five ASDAN decks are the useful negative.** Their overload survives
de-duplication, so it is real teaching content at two-and-a-half times an ASDAN
lesson. They belong with A3-H2's split question, not with this one — and they
are worse than either Humanities split candidate was before its trim.

**The remediation is denominator-neutral.** Not one affected file sits in any of
the nine family baseline sets, so no family median and no p25 floor moves. The
backlog cannot loosen g18 by lowering a floor, and no ratio anywhere else in the
estate changes. That is checked, not assumed.

**Why I stopped rather than fixed it.** Nineteen decks is nineteen lesson units
against a ceiling of 24 with three already spent, and batch 1 alone needs 24
plans. Doing this now would spend the campaign's ceiling on de-duplication and
starve the build the order actually asks for. Scaling the order down is your
call, not mine.

**The question, Matt:** do you want this as its own order before batch 1, or
after the build campaign? My reading is *before*, for one reason — every deck
batch 1 produces comes from the same estate, and if the generator still runs
anywhere, the batch inherits the defect and the ceiling pays for it twice. I
could find no generator script in this repository, so the defect may already be
historical; but "I could not find it" is not "it is not there", and the sweep is
cheap to re-run against anything batch 1 produces.

**Re-run any of this:**

    python3 tools/easter/dedupe_sweep.py --project --output <out>.json
    python3 tools/easter/dedupe_sweep.py --self-test        # 10 controls

**Evidence:** `_sownb/vb/evidence/a3/dedupe_sweep_live.json` — every row carries
the file, the removable words, the stage, and the repeat-factor histogram.

---

## A3-H6 — CLOSED, 2026-09-03, PR #283

Your ruling was "before batch 1, own order". Done: nineteen decks, 7,593 words
of duplicated instruction removed, containment PASS on every one with zero
missing sentences, no family median moved, and the estate re-sweeps to **zero**
removable duplication. Ceiling reds across those decks went 10 → 5.

**Two things you need from this, not one.**

*First, the ceiling.* Nineteen units spent here plus three earlier leaves **2 of
24**. Batch 1 needs 24 plans. The build campaign cannot start against the
current ceiling — it needs raising or re-scoping, and that is a decision only
you can make. I have not assumed either way.

*Second, the five ASDAN decks now belong to A3-H2 below.* Their overload
survived de-duplication, which is exactly what makes them yours.

---

## A3-H2 — split candidates, now seven not two

`GROW_HUM_W15` (×3.02) and `LAUNCH_HUM_W15` (×3.30) are joined by five ASDAN
Spring1 decks whose overload is real teaching content:

| deck | post-dedupe | ratio | family median |
|---|---|---|---|
| `GROW_ASDAN_W16_Authorised_Task_Project_Plan_and_New_Goals` | 2421w | ×2.57 | 940 |
| `GROW_ASDAN_W15_Strengths_Challenge_and_Project_Reset` | 2387w | ×2.54 | 940 |
| `BUILD_ASDAN_W16_Partner_Challenge_and_Seasonal_Goals` | 2441w | ×2.49 | 980 |
| `BUILD_ASDAN_W15_Choice_Budget_and_Project_Reset` | 2394w | ×2.44 | 980 |
| `LAUNCH_ASDAN_W16_Decision_Tools_Banking_Plant_Care_and_Project_Plan` | 2686w | ×1.97 | 1365 |

**Where the overload actually sits, which changes the question.** All five have
the identical profile — nine stages, forty declared minutes — and the words are
distributed against the clock almost exactly backwards:

| stage | words | declared | rate |
|---|---|---|---|
| Lesson overview (title slide) | 327–384 | **0 min** | not timetabled |
| I Do · model | 436–526 | 4 min | 109–132 w/min |
| **I Do 2 · connect** | 491–568 | **3 min** | **164–189 w/min** |
| Independent · evidence | 276–313 | **16 min** | 17–20 w/min |

Two stages carrying about 40% of the words hold 7 of the 40 minutes, while the
stage with 16 minutes carries about 12%. At a 90 w/min supported-reading rate,
"I Do 2 · connect" alone needs roughly 5.5 minutes against its declared 3.

**So this may not be a split at all.** A split assumes there is too much lesson
for one period. What the numbers actually show is a period whose minutes are
allocated against the reverse of its content. Three routes, and the choice is
pedagogic, so it is yours:

1. **Re-declare the minutes** so they match where the teaching is. Cheapest, no
   content lost, and it changes the deck's own data rather than any threshold.
   It would not move the g23 ratio, which is words against the family median —
   but it would make the deck honest about its own shape.
2. **Move content out of the two I Do stages into the drawer.** This is the R5.5
   trim, and here it is defensible in a way it was not for the Humanities decks,
   because the overload is concentrated rather than spread.
3. **Split into two lessons.** Only if the content genuinely needs two periods.

My reading is (2) then (1): trim the concentrated overload, then re-declare what
remains. I have done neither — you said hand them back, and the ratios above are
the measurement, not a proposal I have acted on.

**One observation, recorded rather than acted on, because it is A3-H5's question
in a second form.** The "Lesson overview" stage is the title slide —
`data-type="title"`, `data-min="0"` — and carries 327–384 words of objective,
success evidence and the Lundy banner in every deck in the estate. g23 counts it
as pupil teaching content. Whether a title slide with zero declared minutes
should count is the same question as whether a banner repeated on every stage
should count once or once per stage, and answering either one loosens g23 for
every deck. §5 forbids me deciding it. It is noted here because it is roughly
14% of every deck's word count and it explains part of why the whole estate
reads heavy — not as an argument for any particular answer.
