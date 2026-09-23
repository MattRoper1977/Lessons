# GPT JOB 16 — SCI_G_W5_Fair_Test

Lane: GPT authors · Claude rules · Code lands and measures. Nothing lands without Matt.
Standing rule (Matt, 2026-09-23): authoring new science, computing/coding and cyber-safety
lessons goes to GPT (PACK-1R lane). Code does not author this.

| field | value |
|---|---|
| served deck | `Science_Teesside/Grow/SCI_G_W5_Fair_Test.html` |
| why held | Original Science stage contract: supply defect, queued for re-authoring (_sx3/HELD.md §B, ORDER SX3-M2 §4) |
| pathway | GROW |
| SoW cell | Aut1·W5 · `'GROW Weekly - Autumn'!C36` (the pack manifest / spine audit cites this cell) |
| learning outcome (workbook, verbatim) | Plan and carry out a fair test about forces; record results. |
| shape | Explore (A) / Do (B), 40 minutes each |
| chassis | donor `c4cfa942` (as ordered) + `_sownb/STYLE_CONTRACT_v2.json` |
| reading-age band | Grow: "Reading age 8–11" (Curriculum Policy §6.2, quoted in `docs/orders/LESSON_STANDARD_2026-27.md`) |
| deliverable | zip of `Lesson.html` + PPTX/DOCX/PDF + `Editable_lesson_source.json` + `START_HERE.md` |

## The job
Re-author this Original Science lesson. The pack version is a supply defect (no structural stage label survives; `Independent Work` is how the tool split the two 40-minute sessions — ORDER SX3-M2 §4). Queued for re-authoring.

## HARD STOP
Downloads only. Nothing is pushed to any repository. Matt hands the zip to Claude for intake.

## Gates it is measured against on return
- SHA256 on arrival; the zip's own `SHA256SUMS` verifies.
- PASS B chassis census (`tools/sci/chassis_census.py`).
- D3 row 48 (`tools/hum/verify_loop.py`): modelling bounded, no third "I do"/"We do", no "2" before "1".
- 40-minute timing per lesson (timer total 40).
- The SoW cell above: the lesson's stated outcome equals the workbook cell, and its term·week is Aut1·W5.
- 0 third-party loads (no http(s) script, link, font, image or fetch).
