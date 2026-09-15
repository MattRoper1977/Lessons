# EDU-Q1 GROW W3A arrival checkpoint

15 September 2026. Draft continuation of Lessons #538, parent `74929d1b1eadf66f4caaa4f98e1ec65cd009c112`. This completes the bounded arrival authoring checkpoint; the full Friction pilot remains open and unmerged.

## Changes

The canonical paired lesson now has four arrival questions in each Supported, Standard and Stretch route, arranged 2×2 on wide screens and stacked on phones. They retrieve familiar pushes/pulls, touching surfaces and grip, then invite an observation or prediction. Knowing the word friction is optional before teaching it. The existing four-minute arrival slot remains.

Every route offers pointing, speech, signing, drawing or writing, with passing/uncertainty allowed. Brief hand rubbing is optional; watching an adult or discussing a familiar hand-rubbing example is equivalent. Observations, memories and predictions are distinguished. There are no new compulsory pupil fields or duplicate screen/paper records.

Native details/summary controls reveal the matching answers, initially closed. Route buttons expose their selected state. Separate print actions select only the requested pupil arrival or staff answers. Questions and answer guidance come from `tools/grow_resources/W3A_ARRIVAL.json`, shared by source and companion authoring.

The existing W3A pupil DOCX/PDF now contains nine pages: original common/task/card pages 1–6 plus one selectable arrival page each on 7–9. The teacher DOCX/PDF contains eight pages, with route answers on 6–8. Introductory directions and the old arrival answer paragraph point to those pages. Original paragraphs/tables remain unchanged except pupil paragraph 7 and teacher paragraphs 9 and 28. All 17 rendered DOCX/PDF pages were visually inspected. Original branding/styles retained.

## Evidence

- 24 arrival browser cases passed: standalone/local HTTP × 320/390/768/1280 × three routes. Exact question/access/answer text, selected route, native Space reveal, ArrowRight exemption, and no document/arrival horizontal overflow checked. Each question and print action remains reachable through the slide scroller.
- 12 browser print outputs passed: both delivery modes × three routes × pupil/staff. Each is one A4 page, with four matching questions and answers present only on staff pages. Six unique layouts visually inspected.
- The earlier 162 keyboard/focus checks passed again; zero page runtime errors in both harnesses.
- Native PDFs have 9/8 A4 pages and all 12 matching questions; answer text is confined to the teacher PDF. All nine other lesson stages and pre-existing non-arrival print sections remain unchanged, including W3B and its timing.

Source SHA256: `0a284e326369005f15b0a78b69c6d6786ddf36853a1b32368e3e971a12f68dc0`.

| Companion | SHA256 |
|---|---|
| Pupil DOCX | `3712756c49afb95b1774755957ed4901a294145968700fa41aeeb0ff9cca1a03` |
| Pupil PDF | `54386d11e37d69621ce2ecc5472450750e4c91fa3b804f47d9ade8c07aac0a2d` |
| Teacher DOCX | `5ca80110631e8a94a60e07ee88676166727bbb5bdbd07ede636702d5e90a2f09` |
| Teacher PDF | `81960d8b7e4d8afd540ba34635b8bfb7fe1034605f93cbd13ac43e69a74f3c9f` |

Reproduce the browser check with `python tools/grow_resources/arrival_checks.py REPO_ROOT REPORT_DIR` using Playwright and PyMuPDF, and the retained `focus_checks.cjs`. The authoring script explicitly binds the original keyboard draft; do not run it over subsequent edits without rebasing its input. PDFs are rendered from the DOCX files using the established document renderer.

## Remaining work and holds

Next on High: reachable knowledge organiser, low-load two-check exit and optional integrated Lundy guidance within the correct W3A/shared boundaries. Complete remaining companion alignment, including editable slide/slides-PDF arrival parity, resource pages, provenance, manifests, download archives, catalogue/size records and controlled source/publisher admission. Those release records remain unchanged at this intermediate draft; do not publish the incomplete candidate. Full lesson axe, themes/enlarged-text/layout, media and meaningful human AT acceptance remain open. Sugar's listening pass does not sign off Friction. Legacy full-pack print content and old guidance outside arrivals have not been newly accepted.

EDU-TRY-LESSON-20260915 has been read in master version 157 and recorded in the working checkpoint. The published-only Sugar → Friction → Diffusion showcase remains queued inside EDU-D3, with eight-second rotation, accessible Previous/Next/Pause-Play, focus/manual-selection stop, hover/visibility pause, reduced-motion default off, matching previews and lesson/resource links, and static/no-JavaScript fallback. No homepage change started.

Preserve EDU-Q1 → EDU-D3 → PLAY-D2 → PLAY-Q1 → PLAY-I1 → justified MAINT-1 → PLAY-X1, all approved hero/header/Play amendments, Site291/Lessons456/LP1, 08:30–15:30 UK merge hold, W3B/shared timing and LAUNCH shared guide. Sugar and account/admin work remain complete.
