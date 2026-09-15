# EDU Q1 BUILD Sugar candidate

Status: first authored candidate for browser review, not a release candidate.

Base: Lessons 11bba1875e27016547186754ed65752152e27c9b. The source was unchanged from the 15 September intake when refreshed. No existing EDU-Q1 pull request was found.

## Amendment received

PLAY-BRAND-20260915 was read in both current master copies and recorded in the working checkpoint. EDU-Q1 remains first, then PLAY-D2's approved left Xbox-style homepage illustration, then PLAY-Q1's unified current Play-logo splashes using YOUR NEXT GAME STARTS HERE. Existing PLAY-Q1 runtime work follows the splash checkpoint, with evidenced broken launches or saves taking priority. PLAY-D1, NAV-2 and EDU-D2 remain closed. Site291, Lessons456 and LP1 remain held; the 08:30-15:30 UK merge hold remains.

## Candidate

The approved Sugar classroom example supplies the lesson design, science and tiered tasks. Its source identity was checked against SHA256 a55fe3804c754032480a6bc8ee5cde0e78f798ea229053285072ea133c5fc823. This adaptation retains the canonical lesson route, 40-minute timing, incoming slide fragments, four-question arrivals, knowledge organiser, label sort, equal-serving model, annotation and two-check exits. It integrates one optional feedback prompt with fuller staff notes and does not award Audience, Influence or R through a control.

Changes from the example include working lesson/next links; removal of the example-only source link and fixed pupil dates; clear context-change and dialog focus destinations; focus retention at the serving limit; selected-section printing with afterprint reset; matched wording for the standard print exit; an accessible fallback when scripting is unavailable; and responsive layout controls. Teacher notes retain an unknown starting point and a truthful first-lesson-back approach.

The revised pupil DOCX/PDF (14 A4 pages) and teacher DOCX/PDF (8 A4 pages) are prepared separately and all rendered pages have been visually reviewed. They have not replaced the live downloads. The pupil document includes all three routes; only the selected route is needed. Native content remains editable. Matching slide companions and final print equivalence are still open.

## Verification and release boundary

Inline scripts and the new browser check parse successfully; whitespace checks pass. Browser access to the local preview is blocked by the environment. The existing Science teaching pack workflow now also captures the changed lesson's keyboard interactions, four viewport sizes, 200 percent text, no-script and reduced-motion states, source hash, and all authored print routes. Existing checks remain in place. The new browser test has not yet run; screenshots and printed pages require review before any acceptance.

Do not merge this draft. Complete the PowerPoint/slide PDF and current companion mapping, check browser and print evidence, resolve the actual source-admission requirements with exact changes, and reconcile relevant canonical discovery before promotion. Screen-reader acceptance remains unperformed, not waived. Preserve GROW W3B and the shared LAUNCH guide when their pilots are reached.

Next boundary: routine CI monitoring on Light, then pause for High before screenshot review or fixes. No later pass starts while paused.

## 15 September — first CI repair candidate

Initial Science run 34953613643 timed out at hidden #slide-picker. Prepared per-dialog state and synchronous Escape/Close cleanup to remove a queued-close focus race. Added repeated keyboard reopen checks and failure-state reporting; browser confirmation remains pending. The original artifact download returned HTTP 403, so its screenshots and PDF evidence could not be reviewed here.

FieldOps archive preparation excluded Sugar after its old Guidance marker was replaced. The revised preparation keeps exactly the same 47 source identities, checked against their sorted path digest, and requires actual teacher-dialog/Next/Previous controls. The offline browser now clicks the new dialog, closes it, checks focus and uses Next/Previous at both original widths. Other 46 routes retain their existing interaction checks. Forty packaging controls pass, including missing, substituted and duplicate route refusals and removal of each Sugar control. Inline lesson and changed browser scripts parse; git diff --check passes.

All initial runs have now finished. Cross-estate browser-matrix passed; static-contract failed on the intentionally changed Sugar source and workflow. FieldOps seven jobs passed, archive job failed. Exact source admission, affected test-tool admission, both catalogue gate copies and immutable publisher reconciliation remain pending until accepted final source/companions. Do not waive or re-pin around these failures. This draft remains unready for release.

Next: routine new-head CI monitoring on Light, then High for remaining diagnosis, evidence review and slide companions. No merge/publication or later-pass start. PLAY-BRAND-20260915 and all holds remain in force.
