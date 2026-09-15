# EDU-Q1 — GROW W3A keyboard checkpoint

15 September 2026. **Draft; the GROW pilot remains open.** Matt confirmed High and asked to continue. This is the next bounded EDU-Q1 outcome after the completed Sugar release. EDU-D3 has not started.

## Source and scope

Base Lessons main: `929cf731173aeca8c9941cecd76cb350387499d1`.
Canonical source: `Science_Teesside/Grow/SCI_G_W3_Friction.html`.
Baseline SHA256: `9cb74fc75182432f89e34e70a98ab0c9100a8e8bc15ccde8a64320dd74fd5fd6`.
Candidate SHA256: `a2096b155ada93452a69a5699014fa66dc82f92c9478fa36b938c25edbda09a9`.

Read master §25, the EDU-Q1 refinement brief and the original pilot intake. Refreshed Lessons main and checked repository instructions (no tracked AGENTS.md files). The canonical paired source still matches the intake baseline. The W3A teacher pack confirms seven stages totalling 40 minutes; W3B retains 32 + 4 + 4 minutes. The separate v3_40min routes are alternatives, not replacement sources.

## Demonstrated defects and changes

Baseline Chromium reproduced: Next retained focus after changing slide; entering a prediction pause disabled the focused model button and lost focus to BODY; revealing removed the focused button and again lost focus to BODY; Space on the helpful/unhelpful card both operated the card and advanced the lesson.

The source now focuses the active heading on an actual slide change, retaining focus on a same-slide refresh. The global shortcut handler respects controls, already-handled events and other focused non-heading targets. Heading/background shortcuts remain usable. At a model prediction pause, focus moves from the disabled model Next to its reveal control. Reveal returns focus to a usable model control; completing the model moves focus from disabled Next to Replay. Deck-driven model steps and reveals retain focus on the deck control.

Only inline JavaScript changes. A byte comparison after removing script bodies proves all non-script markup identical, including teaching content, print sections, timing and W3B content. Companions, media, alternative lesson routes, source-admission records and publication pins are unchanged. Preserving existing content at this checkpoint does not accept its outstanding quality gaps.

## Verification

`tools/grow_resources/focus_checks.cjs` runs the canonical file directly and through local HTTP. Each mode covers 320px/reduced motion, 1280px/reduced motion and 1280px/default motion: **162 passing checks, zero page runtime errors**. Checks cover all ten slide headings, both period boundaries and exact pacing, keyboard reveal/replay/completion, deck-driven model progression, native card/sort/link key handling and no focus theft on same-slide updates. The unrepaired baseline is rejected by the new heading-focus assertion; the separate baseline probe records the reveal and card defects above.

Phone and desktop prediction screenshots inspected: focused reveal is visible with its focus outline. This is a targeted focus review, not full visual/overflow acceptance. Local HTTP is not a publisher-built or live-site proof. The final EOF was restored to the original no-newline form after the browser run; this changes no browser content or script.

No new axe, PDF/DOCX/PPTX, full reading-theme/zoom, media-playback or human screen-reader acceptance is claimed. Matt's successful listening pass applies to Sugar, not Friction. No merge or deployment is part of this checkpoint.

## Next checkpoint — remain on High

Continue GROW W3A's four-question arrivals and matching answers, optional non-rubbing route, reachable organiser, two-check exit and matching pupil/staff resources. Integrate the optional Lundy prompt under §25, removing compulsory duplicated written-response claims within the appropriate scope. Preserve W3B teaching and shared 40+40 timing while reconciling source/print/companion boundaries. Complete the actual GROW accessibility, motion, layout, print and companion acceptance before source admission or publication. Then LAUNCH W4L1, preserving its shared teacher guide.

Remaining order: EDU-Q1 → EDU-D3 → PLAY-D2 → PLAY-Q1 → PLAY-I1 → justified MAINT-1 → PLAY-X1. Preserve EDU-HERO-20260915, EDU-HEADER-BRAND-20260915 and PLAY-BRAND-20260915, the 08:30–15:30 UK merge hold, Site291/Lessons456/LP1, completed work and account/admin boundaries. Light is suitable for routine CI monitoring once a candidate is settled; keep High for the next authoring and accessibility work.
