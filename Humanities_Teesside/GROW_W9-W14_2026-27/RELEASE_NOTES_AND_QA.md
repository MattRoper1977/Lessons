# Release notes and QA · GROW Humanities W9–W14 v3.1

## Release position

- Exact continuation: GROW Weekly – Autumn B54:C59.
- Existing Week 8 is treated as Autumn 2 Week 1; this pack implements Weeks 9–14 only.
- Six lessons, nine slides and 40 minutes each.
- W9–W13 have Supported, Standard and Stretch print routes; W14 uses one protected common assessment booklet with staff-only pre-start and record pages.

## Checks passed

- 354 automated structural/content assertions across the final files.
- JavaScript syntax checks for every lesson.
- Unique IDs and resolved ARIA labels/controls.
- No external runtime assets, network APIs, browser storage or pupil-data tracking.
- Source provenance, adaptation and limitation fields present.
- Independent pedagogy/source/assessment re-audit passed with no high-priority blocker.
- W14 assessment guardrails, first-entry lock, access-only TA mode, source lock and post-pens-down Response unlock checked in the generated code.

## Verification boundary

The current build environment did not provide an installed local Chromium/Firefox binary, and its cloud browser cannot open local lesson files. Live click-through and rendered-PDF clipping could therefore not be executed here. Static print structure uses explicit A4 pages and break controls; staff should still open one lesson and print-preview the selected route on the school browser/printer before first delivery.
