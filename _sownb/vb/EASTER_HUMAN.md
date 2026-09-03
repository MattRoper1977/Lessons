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

