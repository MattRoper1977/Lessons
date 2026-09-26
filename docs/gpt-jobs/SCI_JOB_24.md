# SCI_JOB_24 — SCI_B_W12_Give_a_rock_a_job_Classic

Lane: GPT authors · Claude rules · Code lands and measures. Nothing lands without Matt.
Standing rule (Matt, 2026-09-23): authoring new science, computing/coding and cyber-safety
lessons goes to GPT (PACK-1R lane). Code does not author this.

| field | value |
|---|---|
| served deck | `Science_Teesside/Build/W8-W13_2026-27/SCI_B_W12_Give_a_rock_a_job_Classic.html` |
| why held | R-GAPS row 30: .teacher-only blocks absent, no pack source; writing them is authoring (_sx3/RELEASE_LEDGER.md R-GAPS) |
| pathway | BUILD |
| SoW cell | Aut2·W4 · `'BUILD Weekly - Autumn'!C42` — **cell inferred from binding, not from deck records** (the pathway cell for the deck's bound term·week in `lesson-order.json`; accepted 2026-09-23) |
| learning outcome (workbook, verbatim) | Identify everyday uses of different rocks (links D&T / Construction). |
| shape | unchanged (existing Classic deck, Aut2·W4) |
| chassis | **donor (confirmed by Matt, 2026-09-23):** `Science_Teesside/Grow/W8-W13_2026-27/SCI_G_W9_Turn_Earth_explain_the_sky_Classic.html` — blob `9db52ce5f13e`, sha256 `4568d8d3e033b9f5…`, last changed by `be82fe86` (#662), published run 35823783961, D3 row 48 PASS, not held; unchanged on main `6d5a05ad`. Match its chassis: 7 stages — opening 2 · arrival 5 · starter 4 · I do 7 · We do 10 · independent 10 · exit 2 (timer total 40); 5 Lundy panels. The donor fixes the chassis only, never the content; the reading band follows this spec's pathway. Style: `_sownb/STYLE_CONTRACT_v2.json` |
| reading-age band | Build: "Reading age significantly below chronological age (typically below 8 where measurable)" (Curriculum Policy §6.2, quoted in `docs/orders/LESSON_STANDARD_2026-27.md`) |
| deliverable | zip of `teacher_only_blocks.html` (the two blocks) + `Editable_lesson_source.json` + `START_HERE.md` |

## The job
Author the two `.teacher-only` staff blocks this Classic deck lacks (R-GAPS row 30). Content only: the teacher notes for this lesson, matching the BUILD exemplar's two `.teacher-only` blocks in role. No other change to the deck.

## HARD STOP
Downloads only. Nothing is pushed to any repository. Matt hands the zip to Claude for intake.

## Gates it is measured against on return
- SHA256 on arrival; the zip's own `SHA256SUMS` verifies.
- PASS B chassis census (`tools/sci/chassis_census.py`).
- D3 row 48 (`tools/hum/verify_loop.py`): modelling bounded, no third "I do"/"We do", no "2" before "1".
- 40-minute timing per lesson (timer total 40).
- The SoW cell above: the lesson's stated outcome equals the workbook cell, and its term·week is Aut2·W4.
- 0 third-party loads (no http(s) script, link, font, image or fetch).
