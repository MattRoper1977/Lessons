# LOOP CONTRACT — derived from the served population, not from a plan
ORDER HUM-T · stage M1 · 2026-09-20
Scope: Lessons main `96452dad`. Every figure below was measured by
`tools/hum/measure_loop.py` (6 red-proofs passing) over the decks named here.
Weeks are read from each deck's own text, never from a filename (VB-RUN13 R0 / g27).

## 1. The exemplar population

The order names "the served science W9–W14 decks (98 Lundy panels)". Measured against
the estate as served, the real-loop science population is:

| measured | value |
|---|---|
| science files examined | 293 |
| decks carrying the interactive loop panel | 14 |
| weeks those decks state in their own text | 9, 10, 11, 12, 13 (no deck states 14) |
| pathways | BUILD 9, GROW 5 (LAUNCH: none) |
| loop panels in that population | **126** (14 decks x 9 stages) |

**The order's figure of 98 reconciles exactly.** Every one of the 14 decks has the same
nine stages: title, arrival, starter, I Do x2, We Do x2, independent, exit. The two
I Do stages are teacher modelling, where no pupil response is invited:

    126 panels - 28 I Do panels (14 decks x 2) = 98

So 98 is the count of panels on stages where a pupil response is expected. Both numbers
are correct and they measure different things; this contract uses 126 for structure and
98 for the pupil-response population.

Two further facts about the science estate, both measured:
* 40 other science decks carry only the static ribbon — the same defect this order
  fixes in Humanities. The science estate is itself split.
* No LAUNCH science deck carries the interactive panel at all.

## 2. What a panel is, mechanically

Two distinct objects share the class `lundy`. The discriminator is exact and testable:

| | real loop panel | static ribbon |
|---|---|---|
| `aria-label` | `Lundy participation status` | `Lundy participation strip` |
| grid children | `.ls[data-lundy-step][data-state]` | plain `<span>` |
| state | advances SPACE -> VOICE -> AUDIENCE -> INFLUENCE | none |
| controls | `data-action="lundy-voice|lundy-audience|lundy-influence"` | none |
| sentence | per-stage, names this stage's task | one generic sentence, identical on every stage |

The ribbon's generic sentence ("AUDIENCE names back exactly. INFLUENCE changes one real
next action.") repeats verbatim on every stage of every deck that has it. A measurement
that reads stage text without removing the ribbon scores that sentence as if it were the
stage's own loop. **The instrument removes the ribbon subtree before scoring a stage**;
red-proof 1 asserts it.

## 3. The contract, per stage (14 decks, 126 panels)

| stage | panel | response point | audience prompt | influence branch | mechanism |
|---|---|---|---|---|---|
| title (overview) | 14/14 | . | . | . | panel only |
| arrival | 14/14 | 14 | . | . | prose |
| starter | 14/14 | . | . | . | panel only |
| I Do (x2) | 28/28 | 3 | . | . | prose |
| We Do (x2) | 28/28 | . | 14 | . | **control** `lundy-audience` |
| independent | 14/14 | 1 | . | . | prose |
| exit | 14/14 | 14 | 14 | 14 | **controls** R+A+I |

**The full triad exists at Exit only, in every one of the 14 decks.** We Do carries the
audience half. Every other stage carries the stateful panel and nothing more.

This matters for ruling R1. R1 asks for a response point, an audience prompt and an
influence branch on *every* stage. The science exemplar does not do that today: it is
the Exit stage that is the model, exactly as R1 says, and the transplant will put on
every stage something science currently has only at Exit. That is an **increase over
the exemplar**, not a copy of it, and the acceptance rows must be written for the
increase.

## 4. Elements the order expects that the served science decks DO NOT carry

Searched for in every stage of all 14 decks; count of stages carrying each: **0**.

| element | found in the lesson decks | where it actually lives |
|---|---|---|
| staff code strip VF WS I NS E R // ? | no | `Science_Teesside/Teaching_Packs/*/Teacher_Notes.html`, `LundyLoop/` staff cards |
| Earwig / lean-capture prompt (E) | no | the same staff furniture |
| Space: regulation first | no | `LundyLoop/1_whole_school/Whole_School_Reference_v2.html` |
| Space: no public comparison | no | as above |
| Space: permission to refuse | no | as above |

So rulings R2, R3 and R4 cannot be satisfied by transplanting from a science lesson
deck — the source material is in the staff furniture and the policy, not in the
exemplar. R2 (codes on the TA layer, never at pupils) is consistent with what is
measured: the codes are already absent from every pupil surface in science.

## 5. Policy clause map

Feedback & Marking Policy 2025/2026 (Pilot), Issue 1, May 2026, and Curriculum Policy
2026/27, Issue 2. **Numbering note:** the Feedback Policy's contents page and its body
headings disagree from section 9 onward — the contents lists "9. INFLUENCE", the body
numbers INFLUENCE as 8, Pathway-Specific as 10 and Coding System as 11. The order's R1
cites "policy §10" for the pathway modalities, which matches the **body** numbering, so
body numbering is used throughout.

| contract element | clause | what the clause requires | served science |
|---|---|---|---|
| stateful panel, four steps | Feedback §3 | "All four conditions must be in order, or the cycle is broken" | yes |
| response point | Feedback §6 VOICE; Curriculum §14.4 | response in the pupil's own modality; "Communication need changes the method of response, not the entitlement to respond" | Exit + arrival only |
| pathway modalities | Feedback §10 | BUILD point/sign/repeat/demonstrate/Earwig clip/choice board · GROW short margin edit/verbal reply/tick success criteria/voice clip · LAUNCH in-lesson edit/structured verbal/deferred edit for full essays | not surfaced per pathway |
| audience prompt, name-back | Feedback §7 | "The adult names what they heard back to the student" | We Do + Exit |
| R only after Audience | Feedback §7, §11, §13 step 4 | "R must not be added until Audience has happened" | absent from decks |
| influence branch, NS + one thing | Feedback §8, §11 | "NS + … Next step one specific thing" | Exit only |
| codes VF WS I NS E R // ? | Feedback §11; Curriculum §14.3 | minimal codes, taught to pupils | staff furniture only |
| Earwig lean capture | Feedback §12, §13 | 30-second clip, photo or one-line note; "Listen / look before tagging" | staff furniture only |
| Space conditions | Feedback §5; Curriculum §14.4 | regulation first, no public comparison, permission to refuse | absent from decks |

**Policy requirements with no element anywhere in the served science lesson decks:**
the R-after-Audience rule (§7), the code strip (§11), Earwig capture (§12), and all
three Space conditions (§5). These are the elements rulings R2–R4 must source from the
policy and the staff furniture rather than from the exemplar.

## 6. What a transplanted panel must carry

Derived from the Exit stage, which R1 names as the model:

1. **Response point** — names THIS stage's task and offers the pathway's modalities
   (Feedback §10), not a generic invitation.
2. **Audience prompt** — an adult receives it and names it back; R only after
   (Feedback §7).
3. **Influence branch** — NS + one specific thing, or this stage's next step adapted,
   drawn from the deck's own sequence (Feedback §8).
4. **Stateful furniture** — the four steps with `data-state`, so the panel shows where
   the loop has got to rather than asserting it.
5. **Enforced sequence** — see §7. The panel must refuse out-of-order operation, because
   that refusal is what makes it a loop rather than a label.

Each part must be filled from the deck's own stage text. A panel filled from a different
stage must fail the adapter's self-test (order stage B).

## 7. The mechanism: the panel enforces the policy's sequence

This is the most important thing the static ribbon lacks, and it is not cosmetic. The
science panel is driven by a small state machine that **refuses out-of-order operation**:

* `markAudience()` refuses while `state.voice` is false and says so:
  *"Receive pupil Voice first. A response can be spoken, pointed, shown, drawn or
  scribed exactly."*
* the influence control refuses while `state.voice` is false:
  *"Voice comes first. Invite a response in a workable mode."*
* and again while `state.audience` is false:
  *"Audience comes next. An adult must genuinely receive the response before choosing
  what changes."*

That is Feedback Policy §3 ("All four conditions must be in order, or the cycle is
broken") and §7 ("R must not be added until Audience has happened") implemented as
behaviour rather than printed as a reminder. The static ribbon asserts the same four
words and enforces nothing.

### The influence branch is a named choice, not free text

The exemplar offers five next moves, each with its own consequence text:

| branch | what it means |
|---|---|
| secure | transfer to an unfamiliar example or remove one scaffold |
| mixed | contrast two examples, allow peer reasoning, then recheck every pupil |
| misconception | use this lesson's own counterexample, re-model, ask a fresh question |
| access | keep the subject goal; change response mode, sensory load, presentation or adult role |
| method / evidence | preserve the first result, repair the method, repeat |

The misconception branch is filled from the deck's own `cfg.misconception`. **This is the
proof that the transplant can be mechanical**: the influence branch already reads its
content from the deck's own configuration rather than from authored prose, which is
exactly what stage B requires.

## 8. P1 shape (overnight order, 2026-09-21) — stated reading, pending Matt's P1 ok; P1-2 RULED

Matt's four lines, verbatim: "no Title-stage panel; one distinct influence line per option;
collapsed 'Feedback loop' disclosure per stage; Voice names the stage's task." Applied to
batches not yet built (batch 3 onward); batches already built land as-is and are re-cut in a
follow-on batch. The reading below is mine; each line names the derivation so the morning can
correct the reading without re-deriving the facts.

| | rule | derivation | row |
|---|---|---|---|
| P1-1 | the Title stage carries no panel | it is metadata, not a response point (its "task" was the deck's objective) | 14 |
| P1-2 | one distinct influence line per option | **RULED (Matt Roper, 2026-09-21): the four response outcomes are the canonical influence outcomes, one line each, phrased for THIS stage's task** — not yet / needs help → reduce the prompt; did it with support → same task, new example; did it independently → explain a reason; did it and explained → move on. One labelled control (`data-next-move`, the outcome as its label) and one line per outcome; the first three carry the stage's own task (the one row 8 proves), the fourth carries the deck's own "what happens next" sentence or its own next stage. No two lines identical in one panel (row 16 reds on a repeat). The text is NOT the science exemplar's influence section (a deck-wide mirror with one generic sentence per stage — the STOP-T2 finding); the per-stage independent wiring and order enforcement are batch 1's (e.g. `BUILD_HUM_W1_People_Special_To_Me`). Two earlier readings (the pupil's task choice; §7's five named moves) are superseded by the ruling. | 16 |
| P1-3 | collapsed "Feedback loop" disclosure per stage | `<details class="loop-disclosure">` with the summary "Feedback loop", closed by default, opened by a real tap on its summary OR by use of the stage's own task (a control, field or chip of the stage outside the disclosure — `openOnTaskUse` in the loop script, capture-phase click / input / change on the stage); print excludes it (`@media print{.loop-disclosure{display:none}}`). The render harness first uses the stage's task (a field input, else a chip tap) and counts `openedByTask`, falling back to the summary tap, and reads visibility with `checkVisibility()`, because a closed details still gives its content a box in Chromium (measured 330×791 while hidden) | 15 |
| P1-4 | Voice names the stage's task | the VOICE step reads "VOICE · <task>" and the control "I have answered: <task>", the same task row 8 proves the response point quotes; the label is at most 40 characters, cut at a word boundary only where one falls after the first 24 characters (correction #14) | 17 |

Rows 14–17 join the row-45 composite. Ten red proofs in the verifier's self-test.

P1-1 "six per lesson": a deck with two We Do stages carries seven panels (one per response
stage); none is dropped by this reading — the count is reported per deck and left for the ok.
P1-5 (a GROW deck at 508 KB with embedded media): no deck in the HUM-T population is that size
(the largest landable GROW deck is 166 KB; the only landable deck with embedded media is
`BUILD_HUM_W7_A_place_in_the_group_Classic`, whose media sizes are reported in the batch record);
nothing is inlined or re-encoded by the transplant, which changes only the panel furniture.
Status: stated reading, pending Matt's P1 ok.
