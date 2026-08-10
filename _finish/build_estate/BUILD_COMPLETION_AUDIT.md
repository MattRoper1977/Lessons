# BUILD Estate Outstanding v3 — completion audit

Repository observed during this work: MattRoper1977/Lessons
Current source line used for the later BUILD audit: 7a846cba9ee8c2cc128006d6be9b0244c3b7d893
Repository writes: NONE.

## Completed test suites

| Suite | v3 lesson files | Scope |
|---|---:|---|
| BUILD Science | 10 | W3–W7, A Explore + B Do |
| BUILD Art · Teesside Studio Suite | 8 | W1–W8 |
| BUILD Humanities · Teesside History Studio | 8 | W1–W8 |
| BUILD D&T · Community Upcycling | 6 | W1–W6 core + W7–W8 finish/evidence support |
| BUILD ASDAN | 31 | Careers 7 + Living Independently 6 + FoodWise 6 + Community Project 6 + Duke/Social Enterprise 6 |
| TOTAL | 63 | lesson HTML files |

## Why these are included
Each has an authoritative current source combination: scheme/weekly plan, real existing lesson files, and pathway-specific quality/feedback evidence.

## Deliberate stop boundaries
The BUILD year-plan README says that, in that rebuild, only Science and ASDAN were rebuilt while English, Maths, PSHE, Humanities and Arts remained on original weeks. Since then, this task used independent subject authorities to safely upgrade Humanities and Art, and the D&T weekly plan to upgrade Community Upcycling.

The uploaded BUILD SOW does give high-level Autumn curriculum direction for Communication & Literacy, Numeracy and PSHE/Citizenship. However, this pass did not find an equivalent current, authoritative HTML lesson sequence in the repo that could be upgraded without authoring a new course from scratch. Those subjects are therefore NOT declared v3-complete here.

Likewise, duplicate/legacy generic `Build/Slideshows/BUILD_ART_*` rows were not silently substituted for the separately governed `Art_Teesside/Build` suite.

Autumn 2 is not generated. The repo README says Aut 2 W9–W15 was not yet built in that year-plan workstream.

## Common v3 standard
- 40-minute core lessons where a lesson file was created.
- Predictable grammar: Arrival → Starter → I Do → We Do → I Do 2 → We Do 2 → Independent → Exit.
- Arrival retrieves previous learning; Starter does not assume today’s knowledge.
- Supported / Standard / Stretch are movable routes, not pupil identities.
- Scaffold → fade support as independence increases.
- Staff direction tells the adult what to look for, do next and when to step back.
- Feedback creates a learner response; no shake/punishment scoring.
- Lundy Space → Voice → Audience → Influence is live inside teaching.
- Evidence = learner decision → observable action/product → learner explanation/review.
- No persistent pupil data, cookies, form submission or automatic evidence upload in the test HTML.
- Qualification/accreditation claims remain locally verified.
- Practical/safety controls remain local risk-assessment/COSHH/competent-supervision territory.

## Separate safety boundary
D&T v3 test copies do not repeat the known legacy wood-dust/open-window/generic-mask or HT-stamp-only framing identified by the repo safety gate.

## Post-verification edits applied 2026-08-10 (Claude, pre-deployment)

Two repairs were applied to this pack before deployment. Nothing else was changed.

1. **Print-tier defect (63 files).** `<body>` carried no `data-tier`, and `.proute{display:none}` was
   lifted only inside `printTier()`. Any plain browser print — Ctrl+P, File → Print, Save as PDF, an MFD
   driver — silently dropped every tiered task and scaffold. Fixed so the print default shows all three
   routes and a print button still selects one: `.proute{display:block}body[data-tier] .proute{display:none}`.
   The 500 ms `setTimeout` that cleared the attribute was replaced with an `afterprint` listener, because
   it raced print preview in browsers where `window.print()` does not block.
   Verified: 75 files boot with 0 console errors, all inline script blocks pass `node --check`.

2. **BUILD_ART_W3 Arts Award tag — EDIT MADE, THEN WITHDRAWN 2026-08-10.**
   This file was briefly changed from `Explore Parts A + C` to `Explore Part C`, on the belief that the
   live `Art_Teesside/Build` suite tagged W3 as Part C only. **That belief was false.** Checked against
   live main `651a88e`, `BUILD_ART_W3_Industrial_Surface_Skills_Lab.html` tags `Explore Parts A+C ·
   Take Part + Create`, and `BUILD_ART_W2` tags `Explore Part B` alone. The v3 pack was mirroring live
   correctly; the edit diverged it. **Reverted — the pack is byte-identical to its original state on this
   file, and its manifest was never touched, so no page-vs-manifest split exists.**

   The underlying question is real and stays open for the Arts Award adviser, not for code: Trinity requires
   Part C to be a *distinct activity* from Part A. Whether W3's test strips can evidence both depends on
   what the pupil actually produces, and the live suite has separate Part A (W1) and Part C (W4–W6)
   activities either side of it. **This applies to the live file as much as this one, so fixing it in one
   place would leave two conflicting tags for the same week.** Adviser question, one decision, both files.

Known and NOT changed here — see the deployment master prompt:
- the Assessor Witness Statement and its learner-confirmation line are absent from all 31 ASDAN v3 files
  while live main carries both in 49 witness surfaces;
- the hidden-nail magnetic sweep, verified closed on main, is absent from the six D&T v3 files;
- this pack's ten `Science/` copies still carry the six healthy-eating links and the `Aut1·W2` baseline
  error that were fixed during the science install, so they are **superseded, not duplicates** — skip them.
