# Art Teesside — handover

Start here. This file is written so a fresh session needs nothing else.

## State

| | |
|---|---|
| Branch | `art-remediation` — **never push to `main`, never force-push, never merge** |
| Tip | `A2a-2` — see git log |
| `origin/main` at writing | `4023ab5` — moved six times today by a live Lundy Loop workstream, never touching `Art_Teesside/` |
| Estate | 53 HTML files |
| Finished | **BUILD Autumn 2** — the only completed thing. `vocabulary-residue 0` **and** `C5 0`, two independent signals per rule 14 |

**Open by printing** `origin/main`, its message and date, and the branch tip. Main moves under you. A workstream collision (`Pass LL-A2a` vs Art `A2a`) once cost an hour.

**Never trust a base commit quoted in a prompt.** Resolve it first; if it does not resolve, stop. Eleven SHAs quoted to this programme did not exist — they lived in a session sandbox that could not push.

## Landed

`R1` seven Autumn 2 headers · `R2` orphans linked + catalogued · `R3` GROW scheme states its Part mapping · `R4` Silver 1B observer block · `R5` 1B portfolio row · `R6` `.ladder` rule · `R7` the one overflowing sheet (56 pages → 55) · `A2d` + `A2d-2` BUILD press vocabulary · **`A2a` GROW W2 ported off the press**.

Withdrawn, not deleted: `R8` `.a4.dense`; `min-height: 277mm`; "GROW Part B absent"; fault cards `lift` and `shift`; the cue "squeeze until it stops dripping".

## The ladder — enumerated, never a bare number

| file | kit-dep | refusal | cand | offer | total | owner |
|---|---|---|---|---|---|---|
| `Launch/LAUNCH_ART_W6` | 10 | | | | **10** | A2e |
| `Build/Autumn2_Scheme_of_Work` | | 6 | | | **6** | terminal |
| `Grow/GROW_ART_W6` | 3 | | | | **3** | A2b |
| `Grow/GROW_ART_W7` | 2 | | 1 | | **3** | A2b |
| `Launch/LAUNCH_ART_W7` | 3 | | | | **3** | A2e |
| `Build/START_HERE` | | 2 | | | **2** | terminal |
| `Grow/GROW_ART_W2` | | 2 | | | **2** | terminal |
| `Launch/LAUNCH_ART_W1` | | | | 2 | **2** | A2e |
| `Launch/LAUNCH_ART_W5` | 2 | | | | **2** | A2e |
| `Summer1_Scheme_of_Work` | | 1 | | | **1** | terminal |
| **TOTAL** | **20** | **11** | **1** | **2** | **34** | |

`34 → A2b −6 → 28 → A2e −17 → 11`. **Terminal 11**, named: Autumn 2 SoW ×6, START_HERE ×2, GROW W2 ×2, Summer 1 SoW ×1 — each with a ratified reason in `assert_kit.py`.

## The instruments

All in `Art_Teesside/tools/`. Load `INSTRUMENTS_ART.md` before any measuring pass.

- **AT-INST-01** `assert_estate.py` — AO/grade/hours/tier/names. A8 retired here, superseded.
- **AT-INST-02** `assert_cooccurrence.py` — C1–C6, the co-present contradictions. Self-tested at `6486176` where it must return non-zero.
- **AT-INST-03** `assert_print.js` — render at **718×1047px**, 55 sheets / 55 pages, warns under 50px clearance. GROW Week 7 clears by 9px; escalation ladder is in the register.
- **AT-INST-04** `assert_kit.py` + `kit_text.py` — closed kit, specified on category.
- `safe_edit.py` — every substitution declares its expected count and is read back.

### A contradiction detector needs both sides present — read this before quoting any C5 zero

C5 is folder-scoped and reports a route whose scheme disavows kit its own lessons
teach. **It can only fire where a disavowal exists to anchor on.** A folder
containing no refusal can never report one, and its zero is not evidence of
anything — it is an unasked question.

| folder | anchor (a disavowal) present? | is a C5 zero informative? |
|---|---|---|
| `Build/` | **yes** — Autumn 2 SoW ×6, START_HERE ×2 | yes |
| `Grow/` | **yes, since A2a** — GROW W2 ×2 | yes — and it immediately reported GROW W6, which was invisible before |
| `Launch/` | **NO** | **no. C5's silence on LAUNCH means nothing.** |

**LAUNCH is right now in exactly the state GROW was in before A2a** — and it is the
tier carrying 17 hits and the inking-station staging of the Silver project. C5 on
LAUNCH stays uninformative until A2e lands a disavowal there. Landing that
disavowal should be an early step of A2e, not a late one, so the check can see the
rest of the pass.

**A zero that cannot be non-zero is not a pass.** Rule 7 says replay any zero
against a commit where it must be non-zero; this is the structural version — check
that the anchor side exists at all before believing the answer.

**Declared human, not mechanical:** sense ("press Escape" vs "press corner") and refusal intent. Both are ratified once and recorded. The classifier **proposes**; it does not decide.

## Rules 1–16

1. One pass, one commit, one push. Report the SHA and that it resolves at origin.
2. Full assertion set across all 53 files after each pass, reported as counts.
3. Stop if a pass exceeds its predicted file count, or if the shape of the work changes.
4. Method is declared **Literal** or **Interpretive**; interpretive findings are read by eye.
5. A pass is not done until verified at `origin/art-remediation` by a read **separate from the write**.
6. **Substitution counts are not verification. Read-back is.** Read back every field you claim to have changed.
7. Any assertion returning zero is replayed against a commit where it must return non-zero, before the zero is reported.
8. Read every context before reporting. A false negative closes an argument; a false positive only costs one.
9. **Assertions are specified on category and destination, not on phrasing.** Where that is impossible, say so and it becomes a human check.
10. A print measurement taken at screen width is not a print measurement. 718×1047px.
11. An expected value may change in the commit that moved it **only** if the message carries the full decomposition.
12. **An artefact does not assert its own delivery state.** "Nothing is pushed" belongs in the report, not the file.
13. Assertions run over **readable text** — string literals and markup text — not identifiers, selectors, class names or JSON keys. **Location is not the test; role is.**
14. **A defect closes on two independent signals, never one.** Independent = not sharing a vocabulary, corpus or premise.
15. **Word boundaries, never substrings.** Enforced in the harness at import.
16. **You cannot read a gate.** Verification and the action it gates are separate steps, exit code checked between. No compound command holds both.

Plus: **a substitution matching zero occurrences is an error, not a no-op.** And **a fix that grows an allowance list is suspect; one that shrinks it is the rule being obeyed rather than negotiated with.**

## Open passes

- **A2b — GROW W6 and W7, 6 hits.** Downstream of A2a's settled chain. W6's "cutting the plate myself so my learner starts at inking" needs re-physicsing, not rewording. W7's three are `Learner stuck at inking` — **and W7 is Bronze Part D, where the pupil teaches a real learner, so the assumption reaches a second person in a room that cannot do the thing. That is a worse instance of kit-dependence than W2's, not a milder one.** Worth testing any other Part D or skill-share content the same way. C5 now reports GROW W6 — it could not before A2a gave GROW a disavowal to anchor on.
- **A2e — LAUNCH, two kinds of work, scoped separately.** (a) 15 re-physicsing hits across W5/W6/W7 — the Silver leadership project is staged around an inking station. (b) **Authoring, signed off, gated:** replace LAUNCH W1's sixth challenge option with **"Master a three-layer registered stencil from zero"**. Two conditions: it cannot land before A2a (done, so it is now clear), and **the card must say it spans sessions** — three layers in register need each layer dry, and periods are forty minutes.
- **A2c** — parked on Matt's bench test.
- **D6 and the staff zip** — queued behind everything. Staff zip rebuilt once, at the end.

## Do not

- No `main`. No force-push. No merges — the merge is Matt's.
- **The 24-week GROW and LAUNCH gap is not touched, not stubbed, not placeholdered.** Autumn 2 and Spring 1 have no GROW content at all. That is D1, it shares a root with D2, it is two terms of authoring plus a scoping conversation, and it is opened deliberately or not at all. **A2b is GROW remediation and is bounded; it is not a doorway into D1.**

## The defect class — the most transferable thing learned here

This estate's characteristic fault is not a false statement. It is a **co-present contradiction**: two individually true halves that cannot both hold, sitting inches apart. Seven lesson headers carried `BUILD · Explore` beside `Bronze Part A` and passed seven human reviews, because whichever half you looked at was correct. An absence check is structurally blind to this class — every string it hunts for is legitimately present — which is why AT-INST-02 exists and why single-signal closure is banned. The same class caught its own auditor: a traceback and a SHA on screen together, twice, and the reader took the half that fitted, pushing a broken instrument. Assume any zero is blindness until a second, independent signal agrees with it.
