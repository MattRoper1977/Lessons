# LAUNCH Humanities W9–W14 · Verification Report

**Release status: PASS**  
**Verified:** 28 August 2026

## Static and curriculum gates

- Exactly six lessons: W9, W10, W11, W12, W13 and W14.
- Exactly nine slides and 40 minutes per lesson.
- W9–W13 timing: `0,3,3,4,3,3,4,16,4`.
- W14 protected timing: `0,3,3,3,3,2,2,20,4`.
- Titles, week identity, SOW anchors and W8→W14 progression agree.
- HTML/JavaScript syntax, inline handlers, DOM IDs, links and hashes pass.
- No external runtime, remote request, persistent learner storage or form submission.
- Constructed resources are labelled on screen and in print.
- Every independent route is executable from the supplied screen/print pack.
- Independent curriculum, geography-content and chassis/accessibility reviews returned final PASS.

## Browser and interaction gates

Chromium was run from `file://` in 18 cases:

- Six lessons at 1366×768 desktop.
- Six lessons at 390×844 touch-mobile.
- Six lessons with reduced motion at 1366×768.

Result: **288 browser assertions passed; 0 failed**. There were 0 console errors, 0 page errors, 0 failed requests and 0 external requests.

Coverage included navigation, keyboard bounds, hashes, tiers, reveals, hinge retry/correct paths, all six lesson widgets, scaffold/protected states, TA/response overlays, focus trap/return, mobile teacher tools, 44px touch targets, body overflow, Calm mode and reduced-motion film suppression.

An additional 11 targeted post-repair checks passed for combined GIS layers, bounded planning gauges, raw fieldwork repeats, spreadsheet calculations, scatter points/ticks, real-source/fallback wording, W14 frozen evidence, protected TA/response locks and mobile focus restoration.

## Print gates

- All 18 combinations (six lessons × Supported/Standard/Stretch) generated successfully.
- Each final PDF contains four A4 pages with the selected route isolated.
- Title, week, evidence resource, independent task and judgement record survive text extraction.
- No blank pages were detected.
- Contact-sheet inspection found no clipped or overlapping content, including the resource-heavy W11 and protected W14 packs.

## Archive and integrity gates

- `SHA256SUMS.txt` covers every payload file except itself and verifies cleanly.
- Archive paths contain one top folder, no absolute or parent paths, no hidden/macOS metadata and no symlinks.
- `unzip -t` returned no errors.
- A fresh extraction passed the complete static/content/hash verifier.

## Centre-controlled boundaries

- W11 live/local micro-fieldwork requires the centre’s risk assessment, supervision and approved route; the supplied desk-based route is the equal-access fallback.
- W13’s real contrasting-place/online-source core must be teacher-curated and rights-checked; the fictional pair is the complete offline fallback.
- W14’s evidence pack and access contract must be frozen before the protected outcome. Any content prompt invalidates protected status and triggers the centre’s fresh-opportunity process.
- Exact UAS unit/version/outcomes and assessment decisions remain centre-controlled.
