# EDU-Q1 — Friction integrated feedback checkpoint

**Bounded feedback draft complete; GROW pilot remains partial, unmerged and unpublished.** Continue Lessons draft #538 on `codex/edu-q1-grow-w3a-focus-20260915`, from organiser/exit baseline `c7e64b2baf6a3f17f261fb001d416886d46fd32a`. Master §25.2–25.3 re-read at current primary version 159 and second identity 116; no newer amendment found. Matt remains on High.

## Change and reason

The source retained a standalone Lundy Loop stage and a pupil print sheet claiming that writing closed the loop. That conflicts with the approved optional, integrated feedback standard. Replace the existing four-minute stage with **Review the evidence**: revisit one conclusion against actual or explicitly labelled model results, consider adult feedback, retain or improve the explanation, preserve original measurements and label retries. Stage position and timings remain ten stages with `[1,4,2,9,10,4,10,32,4,4]`. Lesson A still stops after We Do 2 and its two-minute exit; Lesson B retains its 32-minute workshop, four-minute review and four-minute exit.

There is one optional native help disclosure within each separate 40-minute lesson: W3A's shared claim sort and W3B's evidence review. Neither adds an input, signature, response requirement or progression gate. Pupil modes include pointing, speech, signing, drawing and trusted-adult support; passing is allowed. Useful adult feedback remains normal teaching, independent of whether the prompt is opened.

Fuller shared guidance appears in an optional staff disclosure, an individual one-page print and the final page of both teacher documents. It describes Space, Voice, actual Audience and Influence, the R gate, evidence/support honesty, feasible adaptations and precise next steps where appropriate. No click, saved answer or completed exit establishes an assessment result automatically.

Remove the old loop print/form and unused participation-only styling. Default pupil packs include the W3A exit and science review, and exclude staff feedback guidance, optional marking notes, assessor witness records and answer keys. Existing optional staff records remain explicitly reachable from staff print controls. The optional marking sheet is labelled staff-only and does not require a duplicate pupil record. Full combined-pack layout remains a later acceptance item.

Remove day/period/clock-time references from the paired HTML's continuation/resource wording, preserving filenames, links and lesson durations. The resume button names **Friction: test the surfaces**. W3A pupil closing directions now include the exit before stopping. W3B pupil/staff continuation names **Levers, pulleys and gears**, checked against the existing W4A teacher title. Historical conversion citations are retained as historical; feedback revisions are dated 15 September 2026.

## Verification

- Standalone and local HTTP, 320/390/768/1280, default theme/reduced motion: **16 help-prompt cases**, **8 staff-disclosure cases**, **8 paired-navigation cases** passed. Space toggles native disclosures; ArrowRight/ArrowDown retain the stage; prompts have no response fields; widths fit. Resume reaches Lesson B and review/exit transitions focus headings.
- **16 scoped axe runs, zero violations** in the new help/review content. This does not certify all stages, staff controls or themes.
- **4 browser PDFs**, each one A4 page: staff guidance and evidence review in both modes. Complete content verified; two unique layouts visually inspected.
- **6 default pack-selection checks** confirm inclusion of W3A exit/review and exclusion of staff records and keys. This checks selected content, not full combined-pack pagination.
- **162 existing focus checks passed again**, with only the expected resume-button accessible name updated. Zero page runtime errors in both harnesses.
- Native DOCX/PDF counts: W3A pupil **13**, W3A teacher **10**, W3B pupil **6**, W3B teacher **5**. **19 pages visually inspected**; other **15 W3A pages pixel-identical** to previous reviewed renders. No clipping found in inspected outputs.
- Arrival, W3A exit, organiser, their print question/answer components and the existing W3B exit DOM remain identical to the baseline. Inline runtime is identical except the TA text dictionary and default print selection. Existing keyboard fixes, models, responses, downloads and timing logic retained.

## Reproduce and limits

```sh
python tools/grow_resources/feedback_checks.py . /path/to/review/feedback
node tools/grow_resources/focus_checks.cjs . /path/to/review/focus
```

Use the installed Playwright/Chromium/axe runtime through PYTHONPATH, PLAYWRIGHT_BROWSERS_PATH and NODE_PATH. `W3_FEEDBACK.json` supplies common content. `author_w3_feedback.py` reconstructs from an explicit organiser/exit baseline: review/rebase BASE before use over later edits. Render DOCX with the documents skill and inspect output before replacing PDFs.

## Candidate hashes

| File | SHA256 |
|---|---|
| `Science_Teesside/Teaching_Packs/GROW/lessons/W3A/GROW_W3A_Friction_Pupil.docx` | `9f8afdf8df90eb845d3ea352d36b9bd19dd192a6c040883fe70957eb8be487de` |
| `Science_Teesside/Teaching_Packs/GROW/lessons/W3A/GROW_W3A_Friction_Pupil.pdf` | `856691efece9acaae40a529f949f3d26567345c8f658de9e26eab1bbbdc585cb` |
| `Science_Teesside/Teaching_Packs/GROW/lessons/W3A/GROW_W3A_Friction_Teacher.docx` | `9da8a692bd1ad6b4a040e4b4a970275c90577cbaf73342492d1908148c5d8717` |
| `Science_Teesside/Teaching_Packs/GROW/lessons/W3A/GROW_W3A_Friction_Teacher.pdf` | `08c926202671c6b2c25778d5d2dcf2f99a473dd704201f0ef9a58e3a359b18f9` |
| `Science_Teesside/Teaching_Packs/GROW/lessons/W3B/GROW_Science_Autumn1_W3B_Friction_Test_Pupil.docx` | `e4333309ef2e2dcf587385063c8e43eee56c3a285089b4f749580124d8c128ea` |
| `Science_Teesside/Teaching_Packs/GROW/lessons/W3B/GROW_Science_Autumn1_W3B_Friction_Test_Pupil.pdf` | `7ddb70eb886f743fd0813b5d581435b36bdfb1a5813e23a6cb6f3b95ccdfee8b` |
| `Science_Teesside/Teaching_Packs/GROW/lessons/W3B/GROW_Science_Autumn1_W3B_Friction_Test_Teacher.docx` | `c0e2ae5adaff89fa05b28e389f7d422e0f638ca9edd33313da61d57d258732cb` |
| `Science_Teesside/Teaching_Packs/GROW/lessons/W3B/GROW_Science_Autumn1_W3B_Friction_Test_Teacher.pdf` | `c9c7bf0a6dc4b4a69c1df89bf7fc3a2fdd73c57828ecb0619688611b52a61d5d` |
| `Science_Teesside/Grow/SCI_G_W3_Friction.html` | `460a95a0464d5db3735a7d64e703fbccd1691d6890bba3c1b78291f97fda8547` |

## Remaining work and holds

Next on High: remaining editable slide/slides-PDF and resource-page alignment for the paired lesson, combined-pack flow, archive/provenance/catalogue/size records, then full pilot accessibility, themes/zoom/layout, motion/media/no-JavaScript, print and actual human AT coverage. No source-admission/publisher pin advanced; required CI not monitored; no publication or all-stage acceptance claim. Original RESULTS.md Not-run rows are unchanged. Matt's Sugar listening pass does not close Friction's AT journey.

Continue EDU-Q1 (GROW W3A, then LAUNCH W4L1 preserving its shared guide), then EDU-D3 → PLAY-D2 → PLAY-Q1 → PLAY-I1 → justified MAINT-1 → PLAY-X1. EDU-D3 has not started. Preserve EDU-TRY-LESSON, EDU-HERO, EDU-HEADER-BRAND and PLAY-BRAND amendments; UK 08:30–15:30 merge hold; Site291/Lessons456/LP1; completed Sugar A11YFIX_CLOSED release and account/admin work.
