# HUM-D5 A3 — CHECKS.md

Population: 120 lessons (78 Humanities, 42 RE; 14 of the Humanities are the
Autumn 1 BUILD/GROW **Fallback** generation). Every check reports PASS, FAIL or
NOT RUN with evidence and its search scope. A check that could not run is
NOT RUN with the reason — never a pass, never silently skipped. A FAIL that is
**systematic by design** is scored as measured and handed to Matt as a ruling
item at STOP S0; nothing is rewritten to make it pass.

Instruments live in `_passhumd5/` (`scan_*.py`, `render_*.js`); raw results in
the workspace `/tmp/claude-0/humd5/` (E*_*.json); the E4 PDFs in `pdf_e4/`.

| id | check | verdict | count | evidence |
|---|---|---|---|---|
| E1 | SoW fidelity (outcome + assessment == SoW cell) | **PASS** | 120/120 | E1_DRIFT.json empty; Humanities vs Humanities_Scheme_of_Work_2026-27.html, RE vs RE_Scheme_of_Work_Autumn_2026.html |
| E2 | Cross-surface parity | **PASS** (0 meaning-level disagreements) | 2,653 field rows × 7 surfaces | scan_e2_parity.py; 50 DOCX heading punctuation drops → Class A group; 13 lessons carry the check answer in slide notes only (informational) |
| E3 | Answers never on a pupil surface | **RULED** H1 by design (KO), H2 applied (strip: 106 → 0 on screen, re-measured), H3 STOP-X | POST: 27/120 visible in default state, all by-design classes (match options 26, word bank/hints); KO 218/218 by design; Pupil_Resources.html 5 held | render_visibility.js (default state, per stage, control proved 120/120); E3_VISIBLE_CLASSIFIED.json |
| E4 | Print routes | **PASS** on pages/blank/clipped/.vary-box; **FAIL — systematic, ruling** on zero answers | 480 PDFs (3 routes + organiser × 120) | render_e4_print.js + E4_RESULT.json: pages 6–7 / organiser 1; 0 blank; 0 clipped candidates at A4 width; .vary-box 0 visible; answers on the organiser page (KO "Remember" q/a) and the arrival page (reminder strip) in 480/480 |
| E5 | Keyboard-only | **PASS** on rounds, traps, Next, starters, exits, modals; **focus indicator gaps — Class B** | 17 sampled lessons | render_e5_keyboard.js; E5_SAMPLE.json names the sample and the two absent kinds |
| E6 | Accessibility (axe, both viewports) + contrast | **RULED H5, edits applied, re-measure in progress (E6 POST)**; PRE:  serious color-contrast on 120/120, svg-img-alt 27, nested-interactive 18, select-name critical 4; LAUNCH button text 3.68:1; brandline PASS | 120 × 9 stages × 2 viewports | render_e6_axe.js (axe 4.10.2, preload off, 800 ms settle); E6_AXE.json |
| E7 | Reduced motion | **PASS** | 120/120; memory flash 12/12 | render_e7_e16_e17.js: 0 running animations > 10 ms and 0 visible elements with animation/transition > 0.01 s on any stage; the memory-flash starter (12 lessons, W05 of each term) still hides its words at 10 s (JS timer) |
| E8 | Video | decode **PASS** 120/120; embedded copy **PASS** 120/120; blank frames **PASS** 0; duration **29 outside 30–40 s — Class B**; safe area PASS 106/106 (Fallback 14 not measurable); caption OCR **NOT RUN** | 120 videos | scan_e8_pyav.py (PyAV); E8_TEXT_LEG.json; tesseract absent |
| E9 | Data | **PASS** numbers; 3 minor | 9 datasets, 9 CSV, 11 XLSX, 9 printed tables | scan_e9_data.py: config == CSV == XLSX == printed table cell-for-cell (ISO timestamps == Excel datetimes); units + source present on config/XLSX/printed; CSV carries units only in the header on 3 (GROW_S2_W03/W05/W06); no lesson has a pupil-input-driven graph (graph leg vacuous, recorded) |
| E10 | External links | **NOT RUN** | 57 distinct URLs | collect_e10_urls.py + curl: every host is refused by the egress proxy (CONNECT 403) — "dead" cannot be distinguished from "blocked"; URL list retained in E10_URLS.json |
| E11 | Facts spot-audit against cited sources | **NOT RUN** | — | the cited pages are unreachable (same proxy policy as E10); the claims themselves were read for E18 and Class B; nothing scored |
| E12 | Media rights | **FAIL — report only** | 18 photo renderings (2 photos, 4 lessons); 94 uncredited pupil pictures; maps 18/18 NE credited, 5/5 OSM credited | scan_e12_media.py; see §E12 |
| E13 | Personal data and residue | **PASS** | 112,098 text units, 20 surfaces | scan_e13_residue.py: 0 emails/phones/paths/artefacts/review-copy/TODO/lorem/NaN/undefined/template braces; 81 name candidates read: historical figures, photo credits (E12), and R14's Jan Halliday |
| E14 | Readability (FK grade per route) | **59 flags — Class B** | 120 × 3 routes | scan_e14_readability.py; see §E14 |
| E15 | RE safeguards and pitch | **PASS** | 42/42 | see §E15 |
| E16 | "Save my responses" | **PASS** 106/106; 14 absent-by-generation | 120 | render_e7_e16_e17.js: .txt carries title, outcome, the visible route's labels and the typed text on 106/106; localStorage/sessionStorage/cookies/indexedDB empty after; 0 non-file network requests from load to save; the 14 Fallback lessons have no #save-independent control (absent, not failed) |
| E17 | Phone reality (390×844 touch) | **PASS on buttons (44 px at rest, correction #12); report only on the rest** | 120 × 9 stages | see §E17: no horizontal scroll (0/1080 stages), Next reachable on every stage; buttons 44 px by offsetHeight and rect after settle (E17_B0008_ATREST.json); summaries 18, pack-link 42, skip 38, inputs 38 at rest |
| E18 | Sensitive-content read | **PASS** framing; 19 gaps ruled H6: 7 filled where derivable (config.sehm, GROW_A1), 12 not derivable (no population line) | 24 target lessons | see §E18 and PROOF_LEDGER "Rulings applied" |

## E3 — Answers never on a pupil surface — FAIL, systematic, ruling

Correction #11: the rendered text index force-reveals every panel, so a hit
there is "present in the DOM", not "visible". The on-screen leg was
re-measured with `render_visibility.js`: the lesson opened as a pupil sees it,
only the Next button pressed, each of the 9 stages measured (checkVisibility +
non-zero box + no hidden/inert ancestor), against all 612 answer strings (`a`,
`ma`, every `arrival[i].questions[j][2]`). Positive control: `#arrival-reveal`
pressed on its stage and the same instrument then saw the answers — 120/120.

| leg | measured | what it is |
|---|---|---|
| on screen, default state | **106/120** lessons show an answer on the Arrival stage | the "Previous lesson reminder:" strip (90) / W01 "Word help: X means …" (16) restates, verbatim, the answer to arrival question 1 — the question's own hint says "Use the reminder strip" |
| on screen, default state | 26 `#slide-3 > button`, 16 "Choose: A OR B" hints, 3 word-bank paragraphs | the key-word definition IS the choice set / glossary (design) |
| on screen, everything else | hidden until `#arrival-reveal`; `ma` only after `#check-method` | 8 Fallback lessons show nothing at all |
| Knowledge_Organiser (html/pdf) | **218/218** q/a strings present | the KO's "Remember: q? a" line — every lesson |
| Pupil_Resources.html | 5 lessons | the check answer appears as ordinary prose on the sheet |
| Pupil_Resources.pdf only | 25 hits, all Fallback | the Fallback pupil PDF bundles the KO (11 pages); not scored twice |
| Editable_Pack pupil pages | reported, not scored | pack pages are teacher-editable |
| print routes | see E4 | same two classes: organiser page + arrival page |

Ruling requested at STOP S0: (a) the KO "Remember" q/a line and (b) the
arrival reminder strip are generator patterns across the whole population, not
lesson defects. Nothing changed.

## E4 — Print routes

`printArm(level)` for each route and `printSection('organiser')`, window.print
stubbed, print media emulated, page.pdf A4. 480 PDFs, 0 errors. Pages: routes
6–7, organiser 1. Blank pages: 0. Clipped text: 0 elements past the A4 width
(measured at a 794 px viewport under print media). `.vary-box`: 2 per lesson,
0 visible under print. Answers: every route pack's page 1 is the organiser
(KO "Remember" q/a) and page 2 the arrival page (reminder strip) — the E3
classes; the "Arrival answers" block on the exit stage does NOT print.

## E5 — Keyboard-only (sample)

Sample (one match, sort, decision, sequence, source, editor per pathway):
BUILD A1_W01 · A2_W02 · A1_W02 · A2_W04 · A1_W05 (no BUILD editor kind
exists); GROW RE_A1_W01 · A2_W05 · RE_A2_W04 · A1_W01 · A1_W02 · A1_W06;
LAUNCH RE_A1_W03 · A2_W03 · S2_W03 · A1_W02 (chain — no LAUNCH sequence kind
exists) · A1_W01 · A1_W06. Results are filled in below when the run completes.

Measured with `render_e5_keyboard.js` on the 17 sampled lessons (E5_KEYBOARD.json;
the five source/sequence boards re-measured with a board-content state signature
after the first signature — aria-pressed/class only — proved blind to a source board
opening its inspect panel and a sequence board reordering its list).

| leg | measured |
|---|---|
| Tab traversal, every stage | 2,959 focus stops across 153 stage-visits; **0 traps**; the stage's Next control reached on every non-final stage (17/17) |
| focus always visible | **not on every stop**: `button.at-btn` / `#auto-timer-toggle` (timer, 301 stops) and `button.vary-chip` (starter/exit chips, 120 stops) and 15 plain board buttons show no outline or box-shadow when focused — B0013–B0015 |
| one full card round by keyboard | **17/17**: the board's first control reached by Tab (≤ 80 presses), Enter/Space acted, board state changed (match, sort, decision, sequence, source, editor, chain) |
| starter block and #vary-exit | **17/17** reached by Tab and operated (Enter / typing) with a state change |
| modals (tools, TA, organiser, words, pause) | **85/85** open on Enter, take focus inside, close on Escape, return focus to the opener |

BUILD has no editor-kind lesson; LAUNCH has no sequence-kind lesson (chain LAUNCH_A1_W02 run as the nearest, named).

## E6 — axe + contrast

`render_e6_axe.js`, axe-core 4.10.2 (`preload:false` — the default asset preload cost a
flat 10 s per run on file:// pages), scoped to the active stage plus the fixed chrome,
on every stage of every lesson at 1280×720 and 390×844 touch, after an 800 ms settle
(the first run sampled each stage mid-fade and read blended colours: `.brandline`
came out #96a6b3 against its real rgb(47,80,104); that run is kept as
E6_AXE_midfade.json and NOT used). 120/120 lessons, 0 NOT RUN, 2,160 stage-visits.

| leg | measured |
|---|---|
| serious/critical, axe | **no lesson is clean**: `color-contrast` serious on every lesson (2,208 nodes desktop / 2,190 phone) — targets `#auto-timer-display` (1,440), `#previous-slide` (509), `#next-slide` (499), the model-node `.current` button (240), `button[data-action="organiser"]` (80); `svg-img-alt` serious on 27 lessons (35 nodes: the inline map `<svg role="img">` without an accessible name); `nested-interactive` serious on 18 lessons (26: interactive controls inside those `role="img"` SVGs); `select-name` **critical** on 4 rank-kind lessons (`#rank-criterion` has no label) |
| moderate/minor | 0 entries at either viewport |
| contrast leg (own): button text on the pathway colours | BUILD `#4E7A9B` and GROW `#3f7d6e` primary buttons with white text are **≥ 4.5:1** (4.59, 4.81); **LAUNCH primary buttons are white on `#3b82f6` = 3.68:1 — FAIL** on all 40 LAUNCH lessons (the incoming LAUNCH button colour is not R6's `#9c27b0`) |
| contrast leg: other buttons | timer buttons `button.at-btn` `#c9803b` on white **3.17:1** (BUILD + GROW, 80 lessons); the model-node current button white on `#f3e6da` / `#ede9fe` **1.2:1** (all 120) |
| contrast leg: `.brandline` | **0** below 4.5:1 at either viewport (settled state) |

Nothing recoloured (R6). Ledgered B0123–B0130.

## E8 — Video

`render_e8_video.js` could not run: the Playwright Chromium build has no H.264
decoder (loadedmetadata never fires on any file). The legs were re-run with
`scan_e8_pyav.py` (PyAV 18.1 / bundled ffmpeg), 120 videos, every frame decoded.

| leg | measured |
|---|---|
| decode | **120/120** decode fully (h264, 1280×720, 280–640 frames); 0 decoder errors |
| embedded copy | **120/120** lesson HTML `data:video/mp4` payloads are byte-identical to the file |
| duration 30–40 s | **91/120**; 29 outside the range (28–54 s): LAUNCH_A1_W02 41.0s, LAUNCH_A1_W07 41.0s, BUILD_A2_W02 48.0s, GROW_A2_W02 29.0s, GROW_A2_W05 47.0s, GROW_A2_W06 51.0s, GROW_A2_W07 29.0s, GROW_S1_W01 47.0s, GROW_S1_W05 48.0s, LAUNCH_S1_W02 43.0s, LAUNCH_S1_W06 54.0s, GROW_S2_W05 28.0s, GROW_S2_W06 29.0s, LAUNCH_S2_W05 28.0s, BUILD_RE_A1_W05 48.0s, BUILD_RE_A1_W07 49.0s, BUILD_RE_A2_W02 47.0s, GROW_RE_A1_W01 47.0s, GROW_RE_A1_W04 47.0s, GROW_RE_A1_W07 47.0s, GROW_RE_A2_W03 28.0s, GROW_RE_A2_W07 29.0s, LAUNCH_RE_A1_W02 52.0s, LAUNCH_RE_A1_W04 47.0s, LAUNCH_RE_A1_W06 47.0s, LAUNCH_RE_A2_W01 47.0s, LAUNCH_RE_A2_W03 28.0s, LAUNCH_RE_A2_W05 50.0s, LAUNCH_RE_A2_W06 28.0s — ledgered B0094–B0122 |
| blank frames | **0** of 960 sampled frames (8 per video; grey sd < 2) |
| safe area | 106/106 Final videos: every sampled frame's content inside the 5 % margin; the 14 **Fallback** videos carry a full-frame non-flat background, so the corner-pixel method cannot isolate the caption box — NOT MEASURED for those 14 |
| caption text vs transcript / model steps | text leg **PASS 106/106** (every config model step present in Model_Transcript.txt; the 14 Fallback lessons have no transcript surface); **OCR of the burned-in captions NOT RUN** (no tesseract) — no Class V item can be raised or cleared by reading the frames |


## E12 — Media rights — report only

- **Photographs** (2: Transporter Bridge, 21 Nov 2008 · Oliver Dixon · CC BY-SA 2.0; 31 Jan 2020 · Reading Tom · CC BY 2.0) render 18 times across BUILD_A1_W04, BUILD_S1_W03/W04/W06 (lesson + pupil sheet). Licence and author are on every surface; the **source URL is on none** (0/18).
- **Pupil pictures**: `Object_Picture_Choices.png` (61, RE + Humanities pupil sheets and the inline copy on the lesson) and `Teaching_Visual_N.png` (33, LAUNCH_A2 pupil sheets) carry `alt="Credited visual resource for this lesson"` but **no visible credit or authored mark** on the surface where they render (94 renderings). The lesson config's `media_note` ("Original captioned teaching model made for this pack…") describes the video, not the pictures.
- **Maps**: 18 lessons render the inline SVG world map and every one carries "Natural Earth public-domain outlines" inside the SVG (18/18). 5 lessons render the OSM-derived local map and every one shows "© OpenStreetMap contributors" (5/5). 49 lessons have config `map_mode: "world"` but render no map (the flag is unused there). 4 lessons cite "OpenStreetMap place references" as a card source without rendering a map.
- **Unreferenced files**: 170 image files in the packs are referenced by no HTML (61 + 33 SVG twins of the PNGs, 64 `Visual_Resource.png`, 12 pack-root SVGs) — residue, not a rights gap.

## E14 — Readability — 59 flags, Class B

FK grade on the CONFIG route units (arrival questions + hints, task steps,
help, extension, exit prompts; the hidden teacher answers excluded); the
rendered-panel measure is kept beside it for the record but over-reads because
whitespace collapse fuses control labels into sentences. Syllables by a vowel-
group heuristic — the same counter for every lesson.

| pathway | route | median | max | over ceiling |
|---|---|---|---|---|
| BUILD (≤5) | Supported | 3.33 | 4.94 | 0 |
| BUILD | Standard | 4.20 | 6.39 | **12** |
| BUILD | Stretch | 5.80 | 7.76 | **31** |
| GROW (≤7) | Supported | 4.47 | 6.66 | 0 |
| GROW | Standard | 5.46 | 7.51 | **1** |
| GROW | Stretch | 6.53 | 8.11 | **13** |
| LAUNCH (≤9) | Supported | 5.54 | 7.52 | 0 |
| LAUNCH | Standard | 6.33 | 8.36 | 0 |
| LAUNCH | Stretch | 7.23 | 9.51 | **2** |

Supported reads harder than Standard: **0** lessons. The 59 flags are listed
per lesson in E14_READABILITY.json (`flags`).

## E15 — RE safeguards and pitch — PASS

Measured on the RENDERED DOM of all 42 RE lessons: "not worship" 42/42 (in
the opening stage 42/42); "Nobody is asked to share a personal belief, family
detail or loss" 42/42; no RE surface invites prayer, worship or personal
disclosure (0); LAUNCH RE carries no mark scheme, band descriptor or exam-
technique language (0 across 14). Three keyword hits were negations of the
pattern (the safeguard text itself) and were read before being classified.

## E17 — Phone reality — report only

390×844, touch, DPR 3, every stage of every lesson. Horizontal scroll: 0 of
1,080 stage-visits. Primary action (`#next-slide`) inside the viewport on every
stage. Control sizes (exact, unrounded): every route/toolbar `<button>` is
**43.5 px** tall (0.5 px under 44); `<summary>` disclosure controls **17.8 px**
(8 per lesson); `a.mbmhome` "← Lessons" 72.5×19; `a.skip` 119.6×38;
`a.pack-link` 346×41.9; "Printable pupil resources" link 346×18; data/chart
inputs 154×37.6. Fixed chrome: skip link, `#auto-timer`, tools `nav` (62–112),
prev/next cluster (786–830), `#classic-progress` (834–844). At scroll 0 the
bottom-most control of 103 lessons' stages sits partly under the prev/next
cluster (254 stage-visits) and 111 lessons' under the 10 px progress bar; while
scrolled, controls pass under the tools nav as any scrolling content does. All
reported, nothing restyled (R6).

## E18 — Sensitive-content read — framing PASS, 19 gaps Class B

24 target lessons (BUILD_A2_W05; GROW_A1 W01–W07 and LAUNCH_A1 W01–W07
migration; LAUNCH_S1 W01–W06 conflict/Holocaust/remembrance; RE
BUILD_RE_A2_W05, GROW_RE_A1_W07, LAUNCH_RE_A1_W06). Read: every evidence
card, model step, note/access/sehm/re_safeguard field and every keyword
paragraph of the teacher notes (E18_EXTRACT.md).

- No graphic imagery or description: **24/24** (the Holocaust unit's cards are the factual definition and an oral-history paraphrase; keyword scan 0 on pupil surfaces).
- Third-person framing: **24/24** (0 second-person personal prompts on pupil surfaces).
- Opt-out or quiet alternative stated: 17/24 — the 7 Fallback GROW_A1 lessons state none (no `sehm` field, no teacher-notes surface).
- Teacher notes name the monitoring/aftercare step: 5/24 (BUILD_A2_W05, the three RE, LAUNCH_S1_W02 "monitor regulation") — **absent in LAUNCH_S1 W01/W03–W06 (5), LAUNCH_A1 W01–W07 (7: "Use sensitive content warnings… Do not ask for family details" is a safeguard, not aftercare) and GROW_A1 W01–W07 (7: surface absent)**.

## P6 requirement settled early — assessment_mode

`assessment_mode: true` on 16 lessons; the four summative RE lessons P6 names
are exactly the RE members (BUILD_RE_A2_W07 · GROW_RE_A2_W07 · LAUNCH_RE_A1_W07
· LAUNCH_RE_A2_W07); BUILD_RE_A1_W07 absent — formative. **PASS.**

## Instrument limitations, named

- `TEXT_INDEX.jsonl` stores non-empty STRINGS only: booleans/numbers/nulls are absent by design (assessment_mode, sow_page, dataset numbers) — those checks read the config source.
- The rendered index is force-revealed (correction #11) — visibility is measured by `render_visibility.js`, never inferred from it.
- axe's default asset preload cost a flat 10 s per run on file:// pages; `preload:false` was set (rule set unchanged).
- PDF text extraction wraps long URLs at line ends (the ONS URL in GROW_RE_A1_W01 Teacher_Notes.pdf) — the DOCX carries it whole; not a dead link.
