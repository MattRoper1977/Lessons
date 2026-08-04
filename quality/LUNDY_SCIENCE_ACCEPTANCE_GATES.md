# Lundy × Science — acceptance gates

**STATUS: draft · OWNER: Matt · Pass LL-S1, 2026-08-04 · derived at `7cffd92` · review-by 1 September 2026**
**Intended users: staff-facing (Science teachers, TAs, whoever briefs them). No pupil-facing surface.**

**This file extends the existing set. It does not restate it.** Where a rule already lives somewhere in
`quality/`, this file points at it rather than copying it — a copy is a twin, and twins diverge
(**R-G01**, **R-G03**).

| defers entirely to | for |
|---|---|
| `quality/SEMH_PEDAGOGY_STANDARD.md` | the twelve non-negotiables; lesson-level pedagogy |
| `quality/toolkits/TOOLKIT_HOUSE_STANDARD.md` | A–H, including the prohibitions on receipt marks, aggregation, collection registers and hours gates |
| `quality/toolkits/ACCESSIBILITY_CONTRACT.md` | the measured accessibility baseline |
| `quality/toolkits/DATA_GOVERNANCE.md` | the six storage questions and the firewall wording |
| `quality/SAFEGUARDING_CONTENT_GATE.md` | dated statutory claims, help routes, disclosure separation |
| `quality/LUNDY_SCIENCE_DATA_FIREWALL.md` | the Science-specific disclosure boundary (PENDING-LOCAL-APPROVAL) |

## What this does

Gives a **decision procedure for accepting or refusing a proposed Science Lundy artefact**, so the next
pack that arrives is judged against the estate's ratified designs rather than against how professional
it looks.

## What this does not do

- It does not authorise anything. Nothing here is a merge grant (**R-SEMH01**).
- It does not grade pupils, evidence or adults, and produces no score, rate or percentage.
- It does not define closure. Closure is defined once, estate-wide (**Gate 1**).
- It does not replace the awarding-body process. No repository change closes a centre action.

---

## Gate 1 — One account of closure, and Science does not get its own

> **BUILD closes when an adult genuinely receives it. GROW and LAUNCH close when the pupil writes the
> line — the adult is audience, not verifier, and no initial is expected.**

Any Science artefact teaching a different closure **fails this gate outright**, however good the rest
of it is. A subject-flavoured second account of closure is the **R-H08** mis-training defect, which
cost a pass to close (`eea4062`). This is why the Science companion was folded into
`LundyLoop/3_subject_guides/science.html` rather than shipped as a sibling, and why no second
calibration file was created in `LundyLoop/5_staff_training/`.

## Gate 2 — No second copy, ever

**R-A09**: the pupil's closure mark has no second copy — *the absence is the control*. An artefact
fails if it introduces a store, column, total, running tally, register, queue, board or aggregate of
closure marks, prompt codes, branch labels or loop marks.

**The test, stated so it can be run:** *if a second copy of the mark exists anywhere — a list, a
sheet, a column, a total — the thing has changed species and the pass stops.*

A diagnostic branch is **expressed as the next step the adult gives** and nowhere else. The moment a
branch becomes a code that is written down, this gate has failed.

## Gate 3 — No adult receipt on a pupil-owned surface

No initial, signature, countersignature, "seen by", "received by" or sign-off field is added to any
pupil-facing surface on any pathway. GROW and LAUNCH closure is pupil-owned; the adult is audience.

## Gate 4 — One next step per pupil per lesson

**B2 Amendment 2.** The adult's day-close act is the **return visit** to the step already given —
*"what happened to it?"* — never the issuing of a new one. An artefact that produces a second next
step at a second grain fails: a write with no reader, recreated one layer up.

## Gate 5 — Optional means optional, and a missed slot is not a debt

**B2 Amendment 3.** A slot in an SEMH setting will be missed, often. **A day whose close never
happened is a closed day.** An artefact fails if it introduces a dated cadence, a catch-up
expectation, or a status queue that accumulates — *a backlog of unread items becomes a portfolio
someone audits.*

## Gate 6 — No failing answer

**B2 Amendment 1.** A reflective or triangulation question must have **no failing answer**, and
disagreement is information about the day, never about the pupil. An end-state that hands a pupil a
verdict — *"returned for…"* — fails this gate. Reframe it as information about the item, or drop it.

## Gate 7 — Nothing pupil-facing ships on a pack's say-so

Pupil-facing wording is **authoring** and is Matt's read, every time, inline. The LAUNCH warrant
clause specifically: **B3 ratified the dimension (evidence/warrant); the wording is Matt's** and waits
for the specimen. Candidates may be proposed; none ships.

## Gate 8 — Derive, never quote

Sentinel populations, file counts and lesson inventories are **derived at the time of use** with the
universe string stated — *"tracked `*.html` containing `<marker>`"*. A number in prose goes stale
silently (**R-SEMH03**, **R-G06**). A pack's figures are its observation, not the estate's state, and
where a pack disagrees with HEAD, **HEAD wins and the disagreement is the finding**.

## Gate 9 — Runtime floor for anything authored here

Zero persistent browser storage · zero network egress · zero external dependencies · a
`prefers-reduced-motion` block · print rules present · no meaning carried by motion or colour alone.
Re-verified on each authored file, never inherited from an upstream validation table.

**A supplier's PASS table applies to the supplier's workspace, not to this repository.** No row from
it may be inherited as a gate result here.

## Gate 10 — Approvals are named, not assumed

Anything needing local sign-off carries a `PENDING-LOCAL-APPROVAL` line in the file **and** a row in
`quality/toolkits/PENDING_APPROVALS.md`. **A signed row means a person read the wording in the file,
not a summary of it.** States requiring a centre action are never closed by a commit.

---

## What is currently deferred, and on what trigger

**The 15-minute Evidence Studio and everything belonging to it** — the upload queue, the moderation
tool, the weekly rhythm, the six-phase routine, the tutor handoff cards, the evidence-status
workflow — are **design-evaluation only** and are **not built**.

The operative reason is not the collisions above; it is that **the day card and the tutor-time slot
were shelved by Matt's own decision**, to run only if the lesson-level mark is observed working in a
real room. A larger version of a shelved thing does not satisfy the condition that shelved it.

> **Reopen trigger — BOTH required:** (a) the late-September three-week check has been run and its
> outcome recorded; **and** (b) Pass LL-J has delivered and Matt has read its specimens.
> Then it becomes its own pass with its own brief.

Recorded in `HANDOVER.md`'s queue and `/_close/OPEN_ITEMS.md`, because an item whose only guard is
Matt's memory is a cached claim.
