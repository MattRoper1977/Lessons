# LL-I · B2.0 — Closure definitions

> **OBSERVATION RECORD — not a description of the estate.**
> **These findings were true at `195ee37` and MUST be re-derived before being relied on.** The
> numbers re-run; the two things that **do not** are flagged in place — **F2 is a negative finding
> across a search space** (re-deriving a negative costs a full re-search with no guarantee of the
> same scope), and **the counter-case is argument, not measurement** (re-running greps returns
> numbers, not the reasoning that keeps 0-of-8 from being re-opened as a defect). Those two are why
> this record is committed rather than left to re-derive.
> **Pass:** LL-I · **Date:** 2026-07-28 · **Last observed true at** `195ee37`.

---

## 1 · Name the R-gate

**There is no coded R-gate.** `ls LundyLoop/tools/*.py` → ten scripts, none an R-gate; no `r_gate` predicate anywhere in `tools/`. **The "0 of 8" has no derivable predicate in the tree** — an assertion, not an instrument output (R-G01 cached-claim shape; retired as a defect claim in R-H07). The only artefact defining "R" *as a gate* is `LundyLoop/5_staff_training/R_Gate_Calibration_Game.html`: *"Closed (R) = Voice happened AND an adult genuinely received it."* **It keys on adult receipt — a BUILD-shaped token** — so it is structurally blind to GROW's *pupil-writes* closure. 0-of-8 measures the absence of a token GROW does not use by design; **not** a GROW defect.

## 2 · The two closure theories, from file evidence

- **BUILD — closes when an adult *receives* it.** `lm-r` span, all 45 (`BUILD_ART_W1:439`, `CAREERS_W1:472`); BUILD prose *"out loud… is enough here… an adult scribes it in their words. Pass is always allowed"* (`BUILD_ART_W1:432`); the R-gate game; `biology/Testing Breath…(1).html:1246` book codes *"R = response received / loop closed"* — the documented **source** of BUILD's `R`/`NS+`.
- **GROW/LAUNCH — closes when the pupil *writes* it.** Byte-identical prose across five directories (`GROW_HUM_W1:164`, `GROW_ART_W8:420`, `PEQ_W1:459`, `LAUNCH_ART_W1:420`): *"this one ends on paper — your own hand… writing it is what closes it. Pass is always allowed"* + *"What I said, and what it changed:"*. R-A02's null encodes the same theory.

## 3 · The counter-case against the ruling *(argument — does not re-derive)*

A loop needs Audience/Influence, which are inherently *received*; the R-gate game flags *"'good' received it, but nothing moved"* as barely-closed. So if nothing reads the written line, the pupil writes into a void and *"writing it closes it"* is unverifiable — 0-of-8 could mark a real Audience gap. **Where it lands:** it does **not** reinstate an adult initial (the BUILD token); it makes **F2 the live question.** Gate-is-BUILD-shaped and a-real-no-reader-question can both hold. (This is the reasoning that stops the next session re-opening 0-of-8 as a defect — it is why the record is committed.)

## 4 · The two falsifiers

- **F1 — CLEAN.** No GROW/LAUNCH pupil- or TA-facing text promises an adult receipt the pathway does not provide (grep for *"an adult will/has received"*, *"shown to an adult"*, *"read back to an adult"* across the five dirs → none). No F1-type defect; ruling not reversed.
- **F2 — PARTIAL, not empty *(the load-bearing negative)*.** Adult responders to the *work* exist: Yellow-Box/DIRT *"Teacher will deep-mark… draw a Yellow Box. Next lesson you respond inside it in a coloured pen"* (`GROW_ART_W1`; also in BUILD Art — general marking); the Feedback Sheet's *"Pupil response — my next step"*; the ASDAN Assessor Witness Statement. **But no instruction reads the closure *line* `"What I said, and what it changed:"` specifically.** Not a "write with no reader" in the strong sense, but **no dedicated reader of the line** — the real B2 question, answered without an adult-R initial. *Search space: `taBriefs`, print slots, plenary/marking routines across `Grow/ GROW_ASDAN/ Launch/ Art_Teesside/Grow|Launch/`.*

## 5 · Reading ages — two measures, fragment caveat

| text | words | FK grade (~age) | ARI grade (~age) | Reading Ease |
|---|---|---|---|---|
| BUILD strip + ownership + null | 44 | 5.4 (~10.4) | 3.2 (~8.2) | 68 |
| GROW = LAUNCH written line | 40 | 1.4 (~6.4) | −0.1 (~4.9) | 94 |

GROW/LAUNCH **byte-identical — two points, not three.** Relation robust (closure line easier than BUILD strip; both very low); absolutes indicative only. Carry the **inversion** and the **glyph caveat** (B3 §1).

## 6 · §4 correction — the R-definition is not an estate-wide singleton

*"Only surviving definition anywhere"* was withdrawn (an unverified singleton wider than its search). Estate-wide: `R = response received` book-code → `biology/Testing Breath…(1).html` (the **source** of BUILD's R, evidence for the ruling, **not** a B2 starting point); the R-gate definition also in `R_Gate_Calibration_Game.html`; *"loop closed"* as a concept across ~7 files. The scoped negative (no `lm-r` in the five GROW/LAUNCH dirs) stands.

## Verdict

R-gate uncoded; where "R" is defined it is adult-receipt (BUILD's theory), so 0-of-8 is not a GROW defect. F1 clean; F2 partial — adult responders to the work, no dedicated reader of the line — the real B2 question (resolved in `LL-I_B2_day_close_reader.md`: the pupil is the reader, no adult-R initial).
