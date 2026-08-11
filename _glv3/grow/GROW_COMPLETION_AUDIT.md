# GROW Estate Outstanding v3 — completion audit

Repository: MattRoper1977/Lessons
Source main inspected: 17b07463918e6bbfde2b2f297168d89074a35032
GitHub writes: NONE

## Authoritative Autumn-1 v3 lesson scope
| Suite | Lesson files |
|---|---:|
| Science | 10 |
| Art · Bronze Teesside Studio Suite | 8 |
| Humanities · Teesside History Studio | 8 |
| GROW ASDAN | 18 |
| TOTAL | 44 |

## GROW demand
The pathway challenge material used in this work defines strong GROW demand as:
- explain cause/process;
- compare and rank;
- apply to a related new context;
- control variables / work within constraints;
- justify with evidence;
- monitor and adjust;
- distinguish main and contributing factors.
Stretch uses counterexample, alternative interpretation, constraint or validity judgement rather than simply more writing.

## Lundy / feedback
GROW Space: predictable lesson structure, success criteria visible, quiet response time, no public comparison.
Voice: short edit, verbal reply, success-criteria tick/re-attempt, authorised pupil-voice clip.
Audience: adult genuinely reads/listens/watches and names the change before R.
Influence: next task/scaffold/half-term plan changes.

## Qualification / evidence boundaries
- Science v3 does not self-award Entry Level outcomes.
- Bronze Art requires trained-adviser/centre audit of the complete portfolio/current requirements.
- Humanities AQA UAS requires exact selected unit/version and centre summary; W7 assessment follows centre-approved conditions/access arrangements.
- GROW ASDAN PEQ/UAS registration, level and final claims remain with the authorised coordinator/assessor.
- Interactive rehearsal panels are not qualification evidence.

## Current repository note
The repo advanced to `651a88ecf2f760c61fa2a221dc9b3351731e6f4e` after the original Science test ZIP was created. See `CURRENT_REPO_SCIENCE_NOTE.md`; no silent Science overwrite has been made.

## Post-verification edits applied 2026-08-10 (Claude, pre-deployment)

Verified independently, not from this pack's own claims: **0** localStorage / sessionStorage / IndexedDB /
cookies / fetch / XHR / sendBeacon / `<form>` / `eval(` across all files. External URLs are Oak links in the
Science folder only; Art, Humanities and ASDAN carry none. No banned PEQ unit label appears anywhere —
no "Delivering a Project", no "Working with Others" or "Problem Solving" used as unit names — and no
lesson asserts a 10-hour requirement on Communication, which the ASDAN spec does not impose.

Two changes were made. Nothing else.

1. **`Science/` REMOVED from this pack (16 files).** Its ten lessons are the earlier test bundle, already
   superseded by the installed `Science_Teesside/Grow/v3_40min/` route. Verified per file: the pack's
   `SCI_G_W3A` still carries the `Aut1·W2` baseline error twice, which the installed route no longer has.
   Installing this folder would regress a live site. The pack's own `CURRENT_REPO_SCIENCE_NOTE.md` reaches
   the same conclusion; removing the folder makes it impossible for a glob to sweep it in by accident.
   **Lesson count for deployment is therefore 34, not 44** — Art 8 · Humanities 8 · ASDAN 18.

2. **Print-tier defect fixed in 16 files** (Art 8, Humanities 8). `<body>` carried no `data-tier` while
   `.proute{display:none}` was lifted only inside `printTier()`, so any plain browser print silently dropped
   every tiered task and scaffold. Print default now shows all three routes; a print button still selects one;
   the 500 ms `setTimeout` was replaced with an `afterprint` listener, which does not race print preview.

Known and NOT changed here — see the deployment master prompt:
- **the 18 GROW ASDAN lessons have no print pack at all** — zero `@media print`, zero print classes, no
  print button. They are screen-only, so they produce no printable pupil work and no ASDAN assessment
  record, on the pathway whose ASDAN strand is the accredited PEQ Level 1 delivery;
- **no PEQ unit codes appear anywhere** (`ComSk1`, `TmWkSk1`, `ThSk1`, `WellbLe1`, `DecMkSk1`, `LSk1`) —
  the lessons say "PEQ" without naming a unit, so no activity can be mapped to a criterion;
- **Arts Award Part tags differ from live in two places**: v3 W2 tags Part A where live tags A+D, and v3 W4
  tags Part B where live tags A+B. Both are reductions. Reported, not changed — an adviser question.
