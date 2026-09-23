# SCI_JOB_19 — SCI_G_W9B_Spherical_Bodies_Do

Lane: GPT authors · Claude rules · Code lands and measures. Nothing lands without Matt.
Standing rule (Matt, 2026-09-23): authoring new science, computing/coding and cyber-safety
lessons goes to GPT (PACK-1R lane). Code does not author this.

| field | value |
|---|---|
| served deck | `Science_Teesside/Grow/W8-W13_2026-27/SCI_G_W9B_Spherical_Bodies_Do.html` |
| why held | body provenance: the Do deck carries its Explore partner's lesson; the Do lesson is absent (_sx3/HELD.md §D) |
| pathway | GROW |
| SoW cell | Aut2·W2 · `'GROW Weekly - Autumn'!C40` (the pack manifest / spine audit cites this cell) |
| learning outcome (workbook, verbatim) | Describe the Sun, Earth and Moon as approximately spherical bodies. |
| shape | the Do (B) half of: Explore (A) / Do (B), 40 minutes each |
| chassis | **donor (confirmed by Matt, 2026-09-23):** `Science_Teesside/Grow/W8-W13_2026-27/SCI_G_W9_Turn_Earth_explain_the_sky_Classic.html` — blob `9db52ce5f13e`, sha256 `4568d8d3e033b9f5…`, last changed by `be82fe86` (#662), published run 35823783961, D3 row 48 PASS, not held; unchanged on main `6d5a05ad`. Match its chassis: 7 stages — opening 2 · arrival 5 · starter 4 · I do 7 · We do 10 · independent 10 · exit 2 (timer total 40); 5 Lundy panels. The donor fixes the chassis only, never the content; the reading band follows this spec's pathway. Style: `_sownb/STYLE_CONTRACT_v2.json` |
| reading-age band | Grow: "Reading age 8–11" (Curriculum Policy §6.2, quoted in `docs/orders/LESSON_STANDARD_2026-27.md`) |
| deliverable | zip of `Lesson.html` + PPTX/DOCX/PDF + `Editable_lesson_source.json` + `START_HERE.md` |

## Status: HOLD (ruling 2026-09-23)
Whether a source for this Do lesson exists outside the repositories is Matt's to answer on his return (19 Oct). Default if no answer by then: write it.

## The job
Author the missing **Do** lesson for this cell. The served `_Do` deck carries its `_Explore` partner's lesson byte for byte (_sx3/HELD.md §D); the Do lesson itself is absent. The Explore lesson stays as it is. If a correct donor for the Do lesson already exists outside the repository, Matt supplies it instead and this job is cancelled (transplant, not authoring).

## HARD STOP
Downloads only. Nothing is pushed to any repository. Matt hands the zip to Claude for intake.

## Gates it is measured against on return
- SHA256 on arrival; the zip's own `SHA256SUMS` verifies.
- PASS B chassis census (`tools/sci/chassis_census.py`).
- D3 row 48 (`tools/hum/verify_loop.py`): modelling bounded, no third "I do"/"We do", no "2" before "1".
- 40-minute timing per lesson (timer total 40).
- The SoW cell above: the lesson's stated outcome equals the workbook cell, and its term·week is Aut2·W2.
- 0 third-party loads (no http(s) script, link, font, image or fetch).
