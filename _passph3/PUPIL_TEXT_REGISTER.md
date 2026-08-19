# PH-3 A2 — Pupil-facing claim corrections (the complete register)

Scope rule applied: edit only where the page tells a pupil the *unit requires* something it does not
require, or understates a minimum so a pupil following the lesson would produce a non-compliant plan.
Facts source: spec v1.2 Oct 2025 ComSk1 additional assessment requirements (§2.3 of the PH-3 prompt,
cross-checked against `_passpq/SPEC_FACTS.md`). No case-insensitive global replaces — every edit was an
exact-match string with surrounding context, asserted to occur exactly once before replacing. Idempotent
(second run = no-op, verified).

## Edited — W4 `LAUNCH_ASDAN/PEQ/PEQ_W4_Plan_a_Communication_Activity.html` (3)

| # | Location | Old → New | Why it is a claim, not design |
|---|---|---|---|
| 1 | I Do 1, step 2 (slide) | "…prepare at least **two** questions your audience could ask. This is the plan the unit asks for." → "…at least **four** questions…" (only the word changed) | The sentence itself labels the content as what the unit asks for; 1.4.1f requires ≥4 audience questions prepared in the plan. Two prepared questions → non-compliant plan. |
| 2 | Print pack, Knowledge Organiser Key Facts | "<li>Prepare at least **two** questions your audience could ask.</li>" → "…at least **four**…" | Print mirror of #1, in a Key Facts list presented as unit fact. |
| 3 | Print pack, Knowledge Organiser Key Facts | "ComSk1 asks for a talk of at least 3 minutes OR a text of at least 250 words; a group activity needs at least three people." → "ComSk1 asks for ONE activity: a talk of at least 3 minutes OR a discussion of at least 8 minutes OR a text of at least 250 words; a group activity needs at least three people." | A statement labelled "ComSk1 asks for" must be the unit's actual requirement (1.5.1: one activity; three routes incl. discussion ≥8 min). Completed additively; no existing route removed. |

## Edited — W5 `LAUNCH_ASDAN/PEQ/PEQ_W5_Deliver_the_Activity_and_Gather_Evidence.html` (5)

| # | Location | Old → New | Why it is a claim, not design |
|---|---|---|---|
| 4 | I Do 1 v5-step heading (slide) | "<h3>Meet the two-way minimum.</h3>" → "<h3>Take audience questions — two-way communication.</h3>" | "The two-way minimum" presents the lesson's two-question target as a ComSk1 minimum; no such unit minimum exists. |
| 5 | I Do 1 v5-step paragraph (slide) | "Take at least two audience questions and respond to them. This shows communication, not recitation, and it is part of the ComSk1 evidence." → "Take at least two audience questions and respond — our lesson target for two-way communication (your plan already holds four prepared questions). This shows communication, not recitation, and it is part of the ComSk1 evidence." | Reframed as the lesson's own target per §4.2's proposed wording; the evidence sentence (true) retained. |
| 6 | Print pack, KO Key Facts | "ComSk1 minimum: 3 minutes spoken OR 250 words written; group of at least three." → "ComSk1 minimum: 3 minutes spoken OR 8 minutes of discussion OR 250 words written; four audience questions prepared in the plan; group of at least three." | A string labelled as the unit's minimum must be the unit's minimum. Completed additively. |
| 7 | Print pack, KO Key Facts (line under #6) | "Answer at least two audience questions to show two-way communication." → "…two-way communication — our lesson target (your plan already holds four prepared questions)." | Sits in "Key Facts" directly under the ComSk1-minimum line — reads as unit fact; reframed as lesson target. |
| 8 | Print pack, KO keyword table | "MINIMUM · The least the unit accepts — 3 minutes or 250 words." → "…— 3 minutes spoken, 8 minutes of discussion, or 250 words." | "The least the unit accepts" is a labelled unit-minimum claim with a partial route list; completed. |

## Left as lesson design (deliberately NOT edited)

- **W4 success-measure examples** — "two audience questions answered" in the Arrival answer, We Do 2 match card, Exit answer, WAGOLL and KO/print scaffolds: a measurable success test the lesson chose, not a unit-minimum claim (§4.2 ruling).
- **W5 task text** — "Deliver…, take two questions, and gather dated evidence" (Independent Work task boxes, print scaffold frames, print worksheets, plan-pyramid STANDARD cell): tasks, not claims.
- **W5 We Do 2 match pills** (`TWO QUESTIONS` ↔ `Two-way shown` etc.), WAGOLL text, all answer keys: game data — never edited.
- **W5 Arrival Q/A** — "What is the ComSk1 minimum — talk length or word count?" / answer "3 minutes spoken, or 250 words written" (screen + print-arrival mirror): question-and-answer-key game data. The completed minimum now stands two lines away in the same print pack (edit #6).
- **Cold Call pools** (`_ccQuestions`, incl. "What is the two-way minimum, in your own words?") and TA briefs: inside `<script>` — Job A touches no script block (G8 asserts scripts byte-identical). The A2 slide reframe (#4/#5) is the visible authority the question now points at.
- **W5 I Do 1 step 1** — "Give your talk of at least three minutes, or share your text of at least 250 words" — the lesson's chosen talk-or-text routes; both compliant; not a unit-minimum label.

Gate result at A2 commit: G1–G9 all PASS (see `_passph3/GATES.md`).
