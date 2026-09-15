<!-- mbm-edu-q1-a11y-fix-2026-09-15-TOP -->
# Sugar accessibility fix — 15 September 2026

Status: A11YFIX_PARTIAL — requested source fixes and browser/print evidence pass; release integration and fresh CI are in progress. No merge or deployment yet. Working level: High.

Matt reports the human screen-reader listening pass worked successfully and authorizes merge/deploy when the other gates are ready. Record this as Matt's result: the browser, assistive technology and OS were not specified. No assistant-run screen-reader pass is claimed. Original supplied RESULTS.md, including its Not-run rows, is preserved unchanged. This latest approval supersedes the earlier no-merge STOP; the UK 08:30–15:30 hold and serialized release process remain.

## Changes

- Native focusable controls are exempt from slide navigation, including summary/video/audio and focused non-heading slide content.
- Tools slide selection waits for Go or Enter; Escape cancels.
- Detective marks expose persistent accessible names, with grouped control labels and retained aria-pressed state.
- TA and overflowing dialogs open at their heading and scroll top. Empty source list item removed. Narrow tables have a labelled, keyboard-focusable horizontal scroll region.
- All six exit questions use fieldset/legend; Question heading matches its button.
- Timer, model captions and question-help label colours corrected. Duplicate progress/chart live announcements removed.
- Only Sugar's corresponding source hashes, paired catalogue admissions and browser expectations are reconciled. Six native companions and original print content remain unchanged.

## Requested measurements

| Check | Standalone | Served candidate |
| --- | --- | --- |
| Focused control probes | 4/4 stage unchanged, native key unprevented | 4/4 stage unchanged, native key unprevented |
| Focus/mark/dialog assertions | 82/82 | 82/82 |
| Empty list items | 0 | 0 |
| Exit controls with question legend | 12/12 inputs, six fieldsets | 12/12 inputs, six fieldsets |
| TA open | scrollTop 0, heading focused | scrollTop 0, heading focused |
| Layout at 320/390/768/1280, 100% | 36 stage + 24 dialog cases clear | 36 stage + 24 dialog cases clear |
| axe serious/critical | 0 on each of nine stages | 0 on each of nine stages |
| Console/page errors | 0 | 0 |
| Each of three pupil PDFs | 6 pages; two complete tickets on p6; 0 Answer text | Same |
| PDF preservation | All 22 pages pixel/text identical to fresh baseline | All 22 pages pixel/text identical to fresh baseline |

Existing repository browser suite additionally passes 89 checks and all nine PDF checks (25 pages). Catalogue mutation controls pass 265/265; protected-boundary controls pass 118/118.

The summary Space probe opens the native disclosure. Select ArrowDown changes only the pending option; Go/Enter confirms and Escape cancels. Video Space/ArrowRight reach the native control without changing slides. Actual H.264 playback and pause after playing are **untested here**: Chromium headless reports NotSupportedError. This is the explicit environment exception in §2.4, not a playback pass.

Additional stress check, outside the requested 100% matrix: 320 px at 150% text has horizontal overflow on stages 3, 8 and 9. The wider tested enlarged-text layouts pass. Moderate axe heading/landmark observations are retained; zero serious/critical does not mean zero observations.

## Exact candidate identities

Source: `8594f15916211ff3de03bb928b2de3756bff0dbe8c52adabd3e4cccfda9d42a3` (628443 bytes).

Publication: `aa212587bdb7b92867e2b1630bfbd9f2e9f69d634fd42c6bbf9c3dba8002973a` (628620 bytes), including the existing usage client/styles and lesson-navigation insertions. These match the tested copies; full publication binding and remote commit identities are recorded separately when complete.

Baseline: Lessons #537 at 5a4f81f22a0f533b8e30dc97c701f5469ab0b1fe, source fdf2d09803e19d11e8f82949efaeb8255893627841fd1a3f7860093350bbca1e. Supplied evidence zip SHA256 d0ec4df789a791f49df781c034b237be60283c54c55f989c03bd343886af4aef.

## Evidence and continuity

Original review.py and viewport.py are retained beside runnable adaptations. Adapters use local runtime/output paths, repair the original browser-variable shadowing and film selector, wait for entrance animation before axe, extend axe to all nine stages, and measure every dialog. Intentional labelled table scrolling is distinguished from clipping. proof.json independently verifies the narrow region's label, focus and reachable content. Pixel/text preservation is against the unchanged baseline rendered by the same Chromium 141 engine.

EDU-HERO-20260915, EDU-HEADER-BRAND-20260915 and PLAY-BRAND-20260915 have been read and remain recorded. Pass order: EDU-Q1 → EDU-D3 → PLAY-D2 → PLAY-Q1 → PLAY-I1 → justified MAINT-1 → PLAY-X1. EDU-D3 does not start in this order. It coordinates the approved owl/resources homepage, classroom/resources Teachers blend, original silver M, cream/navy/sage and the one-line MADE BY MATT header (including mobile), with Learn • Build • Explore below. The approved LEFT Xbox hero and unified M/circle/star splashes remain in their agreed Play passes.

Preserve Site291/Lessons456/LP1, completed account/admin work, GROW W3B/shared timing and the LAUNCH shared guide. After Sugar acceptance, remaining EDU-Q1 pilots are GROW W3A then LAUNCH W4L1. No whole-EDU-Q1 closure is claimed.
<!-- mbm-edu-q1-a11y-fix-2026-09-15-BOTTOM -->
