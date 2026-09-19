# HUM-D5 A3 — CHECKS.md

Population: 120 lessons (78 Humanities, 42 RE). Every check reports PASS,
FAIL or NOT RUN with evidence. A check that could not run is NOT RUN with the
reason — never a pass, never silently skipped.

| id | check | verdict | count | evidence |
|---|---|---|---|---|
| E15 | RE safeguards and pitch | **PASS** | 42/42 | see below |
| E8 | Video captions — OCR leg | **NOT RUN** | 120 | `ffmpeg` and `tesseract` are not installable in this container (apt has no network route). Decode/duration/blank-frame legs remain runnable via Chromium and are pending. |
| E1–E7, E9–E14, E16–E18 | — | pending | — | — |

## E15 — RE safeguards and pitch — PASS

Measured on the RENDERED DOM of all 42 RE lessons, not on source.

| requirement | measured |
|---|---|
| "not worship" renders | **42/42**, and in the OPENING stage (`#slide-1`) in 42/42 |
| "Nobody is asked to share a personal belief, family detail or loss" | **42/42**, opening stage 42/42 |
| no RE surface invites prayer, worship or personal disclosure | **0 violations** |
| LAUNCH RE carries no mark scheme, band descriptor or exam-technique language | **0 violations**, 14 LAUNCH RE lessons |

Three keyword hits were raised and all three are NEGATIONS — the safeguard
text itself matching the violation pattern. Each was read in context before
being classified:

- `LAUNCH_RE_A1_W06` — "Reflection is not worship … **Nobody is asked to pray
  or to share a personal loss.**" That is the safeguard.
- `LAUNCH_RE_A1_W05` — "This is a support for clear thinking, **not an exam
  technique.**"
- `LAUNCH_RE_A2_W06` — "A support for clear thinking, **not an exam
  technique.**"

A keyword scan cannot tell a rule from its breach. Every hit in this table was
read before it was scored.

## P6 requirement settled early — assessment_mode

Read from the config source, not the text index (booleans are not text):

`assessment_mode: true` on **16** lessons. The four summative RE lessons P6
names are exactly the RE members of that set:

  BUILD_RE_A2_W07 · GROW_RE_A2_W07 · LAUNCH_RE_A1_W07 · LAUNCH_RE_A2_W07

`BUILD_RE_A1_W07` is **absent** from the set — formative, as required. **PASS.**

The other 12 are the Humanities summatives (W06/W07 per term), outside that
rule and consistent with it.

## Index limitation, named

`TEXT_INDEX.jsonl` stores non-empty STRINGS only. Booleans, numbers and nulls
are absent by design, so `assessment_mode` (bool) and `sow_page` (int 3–6)
read as "0/120 present" against it. That is the index answering a narrower
question than asked. Both were re-measured from the config source. Any check
on a non-string config value must read the source, not the index.
