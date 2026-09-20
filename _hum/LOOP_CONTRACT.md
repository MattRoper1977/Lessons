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
