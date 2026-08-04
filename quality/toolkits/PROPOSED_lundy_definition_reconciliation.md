# PROPOSED — Lundy closure definition reconciliation

**STATUS: PROPOSED — awaiting Matt + the LL-I / B2 programme. APPLIED NOWHERE.**
**OWNER: Matt · Pass TK-1, 2026-08-04 · quoted at `74e6fee`**

Nothing in this document has been applied to any live file. `LundyLoop/5_staff_training/` is
**proposed-diffs-only** for TK-1, and the closure design belongs to the in-flight LL-I / B2 programme. This
queues into that programme; it does not pre-empt it.

---

## 0 · What the audit could not see

The 2026-08-04 toolkit audit reads, at `6aaffb7`, a conflict between the whole-school guide and the calibration
game, and asks for a three-state model. **Two of its premises have already moved:**

- **R-H08 is CLOSED** (`18270dc`), on Matt's second paper read of the rebuilt game.
- **HANDOVER queue 13 LANDED.** At `a5092bb` the game gained a pathway card; at `eea4062` it was rebuilt under
  Option 1 — label 0 broadened from *"Closed (R)"* to *"Closed"*, the legend made **pathway-relative**, and two
  GROW/LAUNCH scenarios authored **into the question array itself** so a question-only TA meets both closes
  inside the flow (**R-H10**, **R-E14**).

So the audit's headline finding is **largely already fixed** — by a pass that ran before the audit was read.

## 1 · The quote table — how each artefact defines closure at `74e6fee`

| artefact | what it says | shape |
|---|---|---|
| `LundyLoop/5_staff_training/R_Gate_Calibration_Game.html` — legend | *"**Closed** = the loop reached its pathway's close — BUILD: an adult genuinely received it (R); GROW/LAUNCH: the pupil wrote the line, **no adult initial expected**"* | **pathway-relative — correct** |
| same — pathway card | *"a day whose close never happened is still a closed day. Never 'catch it up tomorrow' — a backlog of unread lines becomes a portfolio someone audits, which is the thing this design removes."* | **correct, and load-bearing** |
| same — false-record warning | *"A TA who supplies a receipt here (an initial, a 'seen by', a tick) is not filling a gap; they are inventing an audience-token the pathway never asks for."* | **correct** |
| same — truthful null | *"Voice is present and genuine — Audience is pending. Review it, engage with it, and only then has the loop closed."* | **correct** |
| `LundyLoop/1_whole_school/Whole_School_Reference_v2.html` | *"Feedback is complete only when a student can respond, **the response is genuinely received**, and it influences the next learning move."* · *"without Influence, the cycle has not informed learning."* | **BUILD-shaped — the residual** |
| `LundyLoop/3_subject_guides/*.html` | `Space → Voice → Audience → Influence`, unqualified | **pathway-neutral — silent, not wrong** |
| `LundyLoop/6_posters/` | the four stages as headings; no closure test stated | **no definition — nothing to reconcile** |

## 2 · The actual residual — one artefact, not four

**The calibration game was corrected. The whole-school guide was not.**

`Whole_School_Reference_v2.html` still defines a complete loop as one where *the response is genuinely
received* — with no pathway qualifier. Read literally by a TA working GROW or LAUNCH, that requires an adult
reception event that those pathways **do not have by design**, and it is the precise failure R-H08 was raised
about, now surviving in the one document that outranks the game.

This is **R-H10 one turn out**: the correction was placed on the surface the trainee operates (the game's
questions), and the document the trainee is told to read first still carries the old shape.

## 3 · Proposed diffs — none applied

### 3a · `Whole_School_Reference_v2.html` — the substantive one

Current:

> Feedback is complete only when a student can respond, the response is genuinely received, and it influences
> the next learning move.

Proposed:

> Feedback is complete only when a student can respond, **the response reaches its pathway's close**, and it
> influences the next learning move. **BUILD closes when an adult genuinely receives it. GROW and LAUNCH close
> when the pupil writes the line — the adult is audience, not verifier, and no initial is expected.**

**Word-for-word from the game's own rebuilt legend.** No new vocabulary is introduced anywhere — that was the
constraint on the rebuild and it is the constraint here.

### 3b · Subject guides — optional, low value

The guides state the four stages without a closure test, so they are silent rather than wrong. **Proposed: add
nothing.** A pathway note in ten files to fix a definition none of them gives is churn, and each copy is a
future divergence (**R-G01**). If Matt wants it, the same sentence as 3a, once, in the guide the subject
teacher actually opens.

### 3c · Posters — no change proposed

No closure test appears. Nothing to reconcile.

### 3d · Calibration game — no change proposed

It is already correct. **Do not re-open it.** It is owned by LL-I/B2, it was ratified on a human paper read, and
its shared answer-model was broadened once already under a gate that re-verified all fourteen pre-existing
scenarios (**R-E14**). A second edit from a pass that has not run that gate is exactly the risk R-E09 exists to
prevent.

## 4 · The three-state language — welcome as definition, forbidden as mechanism

The audit's model is **compatible** with the estate's design and is good language:

1. **pupil response recorded** — the pupil made a response;
2. **response genuinely received** — someone engaged with it;
3. **formative loop completed** — the evidence changed the next move.

**It may be adopted as vocabulary. It must never be implemented as structure.** Specifically, and these are hard
constraints, not preferences:

- **No receipt marks.** No adult initials, "seen by", ticks or countersignatures on any pupil-owned closure
  surface. On GROW and LAUNCH, supplying one **invents a token the pathway does not ask for**.
- **No daily collection register**, and no reception requirement on a pupil tool.
- **Reading is not recording.** An adult reading a line does not create an artefact.
- **Pupil-owned GROW/LAUNCH closure stands.** The written line closes it. An adult may be audience or
  next-step-giver — **never a signatory, verifier or receipt-mark**.
- **No second copy of the Loop Mark**, anywhere — no list, sheet, column or total (**R-A09**). If one exists,
  the thing has changed species and the pass stops.
- **A day whose close never happened is a closed day.** No catch-up backlog.

**The trap, named so it is not walked into.** State 2 is exactly the shape that becomes a receipt if
implemented rather than merely defined. The estate has an existing warning about this in the game's own words —
*"receipt by the back door"* — and it applies to this document's own recommendation.

## 5 · The calibration game as discussion, not quiz — the audit's P1

The audit asks for confidence rating, an evidence-needed prompt and a facilitator note. Partly landed already:
the rebuild made the game pathway-aware and put the correction inside the flow.

**Proposed additions, PROPOSED ONLY, for B2 to accept or refuse:**

- a **confidence rating** before reveal — *"how sure are you? 1–3"*;
- an **evidence prompt** — *"what evidence would you need to be sure?"* — answered before the reveal, so the
  participant commits;
- a **facilitator note** per scenario naming what makes it genuinely arguable;
- a **local-policy check** — *"what does our policy say here?"* — because some answers are the centre's.

**Reuse the estate's own truthful null verbatim:** *"Not yet = Voice present, Audience pending."* It already
exists, staff-facing, in this same game. Authoring a second null beside it would be the R-G01 shape again.

**Gate inherited from R-E14, and it is not optional.** Any change to the shared answer model re-scores **every**
existing scenario. Before such an edit ships, all sixteen are re-verified one line each,
correct-answer-before vs correct-answer-after. **Any item whose correct answer moves is a STOP** — a
shared-model edit that silently re-scores existing training is worse than the gap it closed.

## 6 · Handover

Queue into the **LL-I / B2** programme. Depends on nothing in TK-1. §3a is the only substantive proposal;
everything else is either already landed or deliberately declined.
