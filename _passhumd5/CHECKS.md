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
| E1 | SoW fidelity (outcome + assessment == SoW cell) | **NOT RUN** | 0 of 120 | RULED 2026-09-22 (ADDENDUM 2, ruling 3): the former **PASS** rested on E1_DRIFT.json, a two-byte `[]` that no instrument in `_passhumd5/` writes or reads — an empty file proves nothing about whether the comparison ran. The file is deleted from the record. E1 stays NOT RUN until a drift instrument writes it from the config outcome/assessment against the SoW cell (Humanities vs Humanities_Scheme_of_Work_2026-27.html, RE vs RE_Scheme_of_Work_Autumn_2026.html). |
| E2 | Cross-surface parity | **PASS** (0 meaning-level disagreements) | 2,653 field rows × 7 surfaces | scan_e2_parity.py; 50 DOCX heading punctuation drops → Class A group; 13 lessons carry the check answer in slide notes only (informational) |
| E3 | Answers never on a pupil surface | **RULED** H1 by design (KO), H2 applied (strip: 106 → 0 on screen, re-measured), H3 STOP-X | POST: 27/120 visible in default state, all by-design classes (match options 26, word bank/hints); KO 218/218 by design; Pupil_Resources.html 5 held | render_visibility.js (default state, per stage, control proved 120/120); E3_VISIBLE_CLASSIFIED.json |
| E4 | Print routes | **PASS** on pages/blank/clipped/.vary-box; **FAIL — systematic, ruling** on zero answers | 480 PDFs (3 routes + organiser × 120) | render_e4_print.js + E4_RESULT.json: pages 6–7 / organiser 1; 0 blank; 0 clipped candidates at A4 width; .vary-box 0 visible; answers on the organiser page (KO "Remember" q/a) and the arrival page (reminder strip) in 480/480 |
| E5 | Keyboard-only | **PASS** on rounds, traps, Next, starters, exits, modals; **focus indicator gaps — Class B** | 17 sampled lessons | render_e5_keyboard.js; E5_SAMPLE.json names the sample and the two absent kinds |
| E6 | Accessibility (axe, both viewports) + contrast | **RULED H5, edits applied, RE-MEASURED (E6 POST, same instrument, 120 × 9 × 2)**: svg-img-alt 35 → 0, nested-interactive 26 → 0, select-name 4 → 0, color-contrast stage-visits 1080 → 120 per viewport — the one residue is the model-node ribbon (B0125, white on #f3e6da / #ede9fe, 1.2:1, REPORT ONLY as ruled), so B0130 stays "no lesson free of a serious finding" for that row alone; LAUNCH button (3.68:1) and timer (3.17:1) rows are gone from the contrast leg. PRE:  serious color-contrast on 120/120, svg-img-alt 27, nested-interactive 18, select-name critical 4; LAUNCH button text 3.68:1; brandline PASS | 120 × 9 stages × 2 viewports | render_e6_axe.js (axe 4.10.2, preload off, 800 ms settle); E6_AXE.json |
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

## ADDENDUM 3 — Summer 1, all three pathways (A3.0–A3.5), 2026-09-21

Eighteen lessons, ids `BUILD_SU1_W01..W06`, `GROW_SU1_W01..W06`,
`LAUNCH_SU1_W01..W06`. Measured before any landing; nothing edited to make a
line pass.

### A3.0 inputs — verified by content, not by trusting the file name

| pack | SHA256SUMS | lessons found |
|---|---|---|
| BUILD  | 93/93 verified by content, 0 failed | 6 |
| GROW   | 88/88 verified by content, 0 failed | 6 |
| LAUNCH | 90/90 verified by content, 0 failed (91 files, as A3.0 states) | 6 |

**A3.0 input 2, the name — RULED 2026-09-22 (A3.5 ruling 1): accepted by CONTENT.**
A3.0 named `HUM_Summer_1_GROW_W01-06_Final.zip`; the artefact delivered is
`HUM_Summer_1_GROW_Final.zip`. Its 88 of 88 entries verify by digest and it carries
`CHANGELOG_Final_2026-09-21.md`, and that pair — the digests plus the Addendum 2
changelog — **is** the identity. The record is corrected to the delivered name. Not a
hold; nothing about the pack is in question.

### A3.1 counts — derived from the pack population

    previous HUM-D5 population : 78 Humanities + 42 RE = 120
    Summer 1 adds              : 6 BUILD + 6 GROW + 6 LAUNCH = 18, all Humanities
    Humanities                 : 78 + 18 = 96
    RE                         : 42 + 0  = 42
    combined                   : 96 + 42 = 138

A3.1 expects 96 + 42 = 138. **MATCHES.**

### A3.2 — pre-ruled items, recorded by name

**R1 — the authorised skeleton difference, by name.**
`LAUNCH_SU1_W01` carries **six** NOAA annual-mean rows where its donor skeleton
(`LAUNCH_S2_W05`) carries four. GPT's own strict G2 skeleton check scored this
FAIL at 784 donor / 790 output — two extra `tr` and four extra `td`. **RULED NOT
A DEFECT (A3.2 R1): the six years were the brief.** Re-derived here with a
parser, not a byte diff: W01's printed data table is

    Year | CO2 ppm
    1980 | 338.76
    1990 | 354.45
    2000 | 369.71
    2010 | 390.10
    2020 | 414.21
    2025 | 427.35

six year rows, twelve cells, against the donor's four rows and eight cells:
exactly the +2 `tr` / +4 `td` GPT reported. W02 780/780, W03 780/780, W04
778/778, W05 783/783, W06 769/769 all PASS on GPT's own gate.

HUM-D5 has **no skeleton or donor-diff gate of its own** — E1–E18 contain none,
and the G2 check is the pack builder's. The exception is therefore recorded here,
by name, so that any skeleton or diff gate added to HUM-D5 reads it before it
runs, and so that nobody "repairs" the two rows:

> **AUTHORISED DIFFERENCE `R1-LAUNCH_SU1_W01-NOAA-SIX-YEARS`** — two additional
> `tr` and four additional `td` in the `LAUNCH_SU1_W01` data table against donor
> `LAUNCH_S2_W05`. Authorised by ADDENDUM 3 A3.2 R1. Not to be repaired, and not
> to be hidden by widening the skeleton gate.

**R2 — NOAA 2025, UNVERIFIED.** `https://gml.noaa.gov/webdata/ccgg/trends/co2/co2_annmean_mlo.csv`
was attempted twice from this session. Both attempts:
`curl: (56) CONNECT tunnel failed, response 403`. The 2025 line was never read,
so 427.35 ppm is **UNVERIFIED-BY-CLAUDE**, exactly as R2 anticipates. Nothing was
edited; A3.2 R2 says continue when there is no egress, and that is what happened.

**R3** — LAUNCH ships six per-week `Sources_and_checks.html` plus one at pack root:
confirmed, 7 files. They are evidence pages and take no catalogue row.

### A3.3 gates — re-derived here

**G-A — PASS 18/18.** 9 slides per lesson, `data-timer` summing 40, pathway in
the title, and exactly **one** `<h1>` per lesson. The `<h1>` count was taken with
a parser. A naive `<h1` regex reports 2 on the LAUNCH lessons: the second hit
lives inside a JavaScript string, the same trap that produced the 1.12 MB Science
hub (L47). A regex count would have failed a gate that in fact passes.

**G-B — PASS, 36 rows of 36 clean.** Real Chromium, each pack served over http
from its own root, every stage activated in turn so that no stage's width goes
unmeasured:

    BUILD   lessons 6, rows 12 (390 and 1280), clean 12, flagged 0
    GROW    lessons 6, rows 12 (390 and 1280), clean 12, flagged 0
    LAUNCH  lessons 6, rows 12 (390 and 1280), clean 12, flagged 0

0 page errors, 0 console errors, 0 off-origin requests, no horizontal overflow at
either width. **No runner run id**: A3.3 asks for the runner *"if the container
has no browser"*. This container has Chromium, so G-B ran here, on real Chromium,
and the condition for the runner leg was never met. The GROW and LAUNCH READMEs
both record "Chromium was unavailable… desktop/phone layout tests were NOT RUN" —
this is the line that closes that gap for them.

**G-C — PASS 18/18, 0 occurrences.** Pupil-visible text, measured as the union of
`document.body.innerText` over every activated stage (a hidden stage returns the
empty string, so the union is what a pupil can actually see). Named terms, counted
case-sensitively **and** case-insensitively: `USGS`, `earthquake`, `Migration`,
`OS symbol`, `LAUNCH_S2_`, `LAUNCH_A1_`, `LAUNCH_A2_` — every count 0. The
equivalent donor-id leg for BUILD and GROW was derived from their own records
(BUILD ← `HUM_Autumn_2_BUILD_Reviewed.zip`; GROW ← `GROW_S2_W03/W04`,
`GROW_A2_W05/W07`; LAUNCH ← `LAUNCH_S2_W03/W05`, `LAUNCH_A1_W02/W06/W07`,
`LAUNCH_A2_W03`) and generalised to any foreign lesson id
`(BUILD|GROW|LAUNCH)_(A1|A2|S1|S2)_W\d+` — 0 in all 18.

*Red proof:* a copy of `LAUNCH_SU1_W01` was seeded inside its `<h1>` with
`USGS earthquake LAUNCH_S2_W05 Thunberg`. The instrument then reported 5 clean /
1 flagged, naming `USGS 1`, `earthquake 1`, `LAUNCH_S2_ 1`, foreign id
`LAUNCH_S2_W05`, `thunberg 1` — and flagged only the seeded lesson. An instrument
that cannot go red proves nothing when it goes green.

**G-D — PASS. 0 quotations, 0 extracts.** Case-insensitive scan of the whole
LAUNCH pack, text surfaces *and* binary (12 DOCX, 6 PPTX, 18 PDF, 1 XLSX, all
extracted and read — the DOCX/PPTX/PDF/XLSX libraries are importable in this
container, so this leg RAN). The name appears in 18 staff files and in the
lessons' config, never as book text. Every occurrence is one of three sentences:
"the teacher supplies the school's copy of No One Is Too Small by Greta Thunberg;
no extract or quotation is included", "This pack includes no quotation or
extract", and the SoW resources line "selected No One Is Too Small extracts by
Thunberg" — the scheme's own list of what the *teacher* brings. **Pupil-visible
count: 0 in all six lessons.**

**G-E — NOT RUN.** `resources.json` rows, the chip-count filter chain and
hub reachability are landing-time gates; the 18 have not landed.

### Proofread — two defects found in LAUNCH, neither by a supplied gate

Measured by comparing each lesson's **on-screen** organiser dialog against its
**print** organiser and its `Knowledge_Organiser.html`, then re-measured as
rendered by real Chromium (the source table could have been repainted from the
config at load; it is not — what is in the bytes is what the pupil reads).

| lesson | word | on screen | print + Knowledge_Organiser |
|---|---|---|---|
| `LAUNCH_SU1_W01` | provenance | "1980 is 338.76 ppm and 2025 is 427.35 ppm." | "Who made a source, when and why" |
| `LAUNCH_SU1_W02` | mitigation | "Reducing a source of greenhouse-gas emissions." | "Reducing greenhouse-gas emissions or increasing their removal" |

16 of 18 lessons are clean. W01's screen cell is not a definition of provenance
at all — a data sentence has replaced it. W02's screen cell is narrower than the
printed one: it drops removal, which is half of what mitigation means.

Neither is confined to one cell. W01's wrong string is carried by
`LAUNCH_SU1_W01_Lesson.html` (×2), `Editable_Slides.pptx`, `Teacher_Notes.docx`
and `Teacher_Notes.pdf`; the right string by `Knowledge_Organiser.html`/`.pdf`,
the lesson (×1) and the same PPTX. W02 has the identical shape. So both packs
disagree with themselves across surfaces — an E2 meaning-level disagreement, the
class E2 currently records as 0.

**RULED 2026-09-22 (A3.5 ruling 2): HELD, author's defect, sent back to GPT.**
Neither cell was edited — a vocabulary definition is authored text, and R2 sets this pack's
precedent. `LAUNCH_SU1_W01` and `LAUNCH_SU1_W02` do not land until GPT re-delivers them.
**BUILD W01–W06, GROW W01–W06 and LAUNCH W03–W06 are clear on every gate above** and proceed
to intake and landing once the `Sources_and_checks.html` re-delivery of ruling 3 arrives.

## Rulings on this addendum, recorded 2026-09-22

| # | ruling | state here |
|---|---|---|
| 1 | GROW pack accepted by content; the A3.0 name corrected in the record | applied above |
| 2 | `LAUNCH_SU1_W01` / `W02` HELD, author's defect, back to GPT; the other 16 proceed once ruling 3 lands | applied above |
| 3 | `Sources_and_checks.html` back to GPT — ids must match the lessons' own anchors, one per pack root, identical to the `_records` copy | HELD, not re-delivered |
| 4 | NOAA 2025 (427.35 ppm) stays as authored, flagged UNVERIFIED; no edit until Matt replies "NOAA ok" or a value | applied — nothing edited |
| 5 | the R1 exception is recorded; "HUM-D5 has no donor-diff gate" is a **next-order finding**, not built now | recorded above, not built |
| 6 | G-B on this container's real Chromium stands; no runner run needed | recorded above |
| 7 | `stage_name()` returning `data-type` verbatim: confirmed, fixed, red-proved | see `tools/hum/STAGE_IDENTITY_RULE.md` |
| 8 | correction #26 accepted | recorded above |

### Ruling 3 — what the re-delivery has to satisfy, measured

The supplied `Sources_and_checks.html` offers the anchor ids `sow, authored, book, w01 … w06`.
The BUILD lessons cite `#sow`, `#plans` and `#townside`. So **`#plans` and `#townside` — 4 of
the 11 links — would land dead**, and the file is not byte-identical to any `_records` copy.
That is the whole of the hold: ids that match the lessons' own anchors, one file at the pack
root, identical to the `_records` copy.

## ADDENDUM 3 v2 — the three W01-06_Final packs, every gate re-run, 2026-09-21

ADDENDUM 3 was re-issued with three new zips,
`HUM_Summer_1_{BUILD,GROW,LAUNCH}_W01-06_Final.zip`, and it withdrew what the A3.0–A3.3
results above were measured on. **Those results are therefore VOID as evidence for what
lands.** Everything below is re-derived on the new artefacts. The withdrawn extractions
were moved out of the working area before a single line of this was measured, so that no
gate here could read a withdrawn byte.

### A3.0 v2 — inputs verified by CONTENT

| pack | SHA256SUMS | files | lessons | `PACK-1R` section in the changelog |
|---|---|---|---|---|
| BUILD  | 106/106 verified, 0 failed, 0 missing | 107 | 6 | yes |
| GROW   |  89/89  verified, 0 failed, 0 missing |  90 | 6 | no |
| LAUNCH | 101/101 verified, 0 failed, 0 missing | 102 | 6 | yes |

The withdrawal clause requires the `PACK-1R` section only of a **BUILD** W01-06 Final, and
BUILD has one. GROW's absence is not a withdrawal trigger. File counts differ from the
withdrawn generation (93 / 88 / 90), which is one more way of showing these are not those.

### G-A v2 — and CORRECTION #30, against my own A3.3 line

9 slides, `data-timer` summing 40, and the pathway in the title: **18/18**.

The `<h1>` leg does not read as A3.3 recorded it. Counted with the parser:

```
deck carries exactly one <h1>   : 18/18
document carries exactly one    : 13/18
```

`BUILD_SU1_W02..W06` carry **four** `<h1>` each: one in `slide-1`, two inside `v4-modal`
dialogs (the organiser and the Teacher card) and one in the print-only organiser section.
`BUILD_SU1_W01` and all twelve GROW and LAUNCH lessons carry one.

**A3.3 states "exactly one `<h1>` per lesson … PASS 18/18". That was measured over the
DECK and written as though it were over the document.** The two are the same number on
thirteen lessons and not on five. The withdrawn generation has the identical shape at
identical byte offsets, so this is **not** a regression in the new packs — it is a defect
in my own reporting, and the line above is the correction. Only one of the four is visible
in any one medium, so no pupil sees two; but five lessons differ from the convention their
own twelve stablemates keep, and that is GPT's to reconcile, not mine to edit.

### G-B v2 — PASS, 36 rows of 36 clean

Real Chromium, each pack served over http from its own root, every stage activated in turn.
BUILD 12/12, GROW 12/12, LAUNCH 12/12 at 390 and 1280: 0 page errors, 0 console errors,
0 off-origin requests, no horizontal overflow at either width.

### G-C v2 — PASS 18/18, 0 flagged

Pupil-visible text, the union of `document.body.innerText` over every activated stage.

### G-D v2 — PASS, 0 pupil-visible

Rendered leg 18/18 clean. Whole-pack leg, text **and** binary, every file opened and read
(0 library failures, so nothing is NOT RUN):

```
BUILD    107 files   "Thunberg" occurrences 0
GROW      90 files   "Thunberg" occurrences 0
LAUNCH   102 files   "Thunberg" occurrences 62, in 23 files
```

Every one of the 62 is a staff or config sentence of the three kinds A3.3 names — "the
teacher supplies the school's copy … no extract or quotation is included", "This pack
includes no quotation or extract", and the scheme's own resources line. **0 book text, 0
pupil-visible.**

### G-E — still NOT RUN

`resources.json` rows, the chip-count filter chain and hub reachability are landing-time
gates and the 18 have not landed.

### Ruling 3 v2 — `Sources_and_checks.html`

Every link resolved to a real file and, where it carries a fragment, to a real id in that
file — in both directions:

```
lesson -> Sources links   BUILD  8    GROW 15    LAUNCH 27    broken 0
Sources -> * links        BUILD  0    GROW 12    LAUNCH 18    broken 0
```

The `#authored` fragment I first counted as unmatched is an id in the root record itself
(`w01..w06, authored, sow, book`); it resolves, and the count above is the corrected one.

| pack | root copy | per-week copies | `_records` copy | byte-identical to root |
|---|---|---|---|---|
| BUILD  | yes, 2 232 B  | none      | five, differently named | **all five, yes** |
| GROW   | yes, 7 452 B  | W03–W06   | **no `_records` directory at all** | cannot be checked |
| LAUNCH | yes, 17 691 B | W01–W06   | one | **yes** |

Ruling 3's "identical to the `_records` copy" is satisfied for BUILD and LAUNCH. **GROW
ships no `_records` directory**, so for GROW the clause has nothing to compare against.
That is the one outstanding item of ruling 3 and it is the author's to supply.

### Ruling 2 v2 — THE TWO LAUNCH DEFECTS ARE STILL THERE

The re-delivery did **not** repair them. Byte for byte the same two cells:

| lesson | word | on screen | print + Knowledge_Organiser |
|---|---|---|---|
| `LAUNCH_SU1_W01` | provenance | "1980 is 338.76 ppm and 2025 is 427.35 ppm." | "Who made a source, when and why" |
| `LAUNCH_SU1_W02` | mitigation | "Reducing a source of greenhouse-gas emissions." | "Reducing greenhouse-gas emissions or increasing their removal" |

16 of 18 clean. **The A3.5 ruling-2 hold stands unchanged: `LAUNCH_SU1_W01` and
`LAUNCH_SU1_W02` do not land.** Nothing was edited.

### Ruling 4 v2 — NOAA 2025 still UNVERIFIED-BY-CLAUDE

A third attempt at `https://gml.noaa.gov/webdata/ccgg/trends/co2/co2_annmean_mlo.csv` from
this session: `curl: (56) CONNECT tunnel failed, response 403`. 427.35 ppm is unread by me,
exactly as A3.2 R2 anticipates, and nothing was edited.

What *can* be measured here: the lesson's printed table equals the shipped CSV's data rows
exactly —

```
Year CO2 ppm | 1980 338.76 | 1990 354.45 | 2000 369.71 | 2010 390.10 | 2020 414.21 | 2025 427.35
```

— and the XLSX carries the same six values, with one presentational loss: it stores
`390.10` as the number `390.1`, so the spreadsheet shows one fewer significant figure than
the lesson and the CSV. Report-only.

### Report-only extras

* **LAUNCH claim table** — 25 claim rows, **all 25** with an access date; 22 with an
  external URL and 3 citing the pack's own authored-practice anchor, which resolves. The
  three are the invented practice numbers and say so ("Invented teaching number, not a
  school observation"). URL reachability is UNVERIFIED-BY-CLAUDE: no egress.
* **Mark-scheme language** — pupil-visible, all 18: **0**, against `mark scheme`, `AO1–4`,
  `level 1–4`, `band 1–4`, `N marks`, `grade`, `assessment objective`.
* **GROW W05 Middlesbrough / Helmsley** — pupil-visible text names the two places as the
  comparison subject and asserts nothing about them (4 label strings, no claim sentence).
  The factual claims sit in the sources record, each with a named source, a URL and an
  explicit limitation ("This identifies a built feature, not current bridge access";
  "This does not establish the absence of other transport").
* **GROW W03 dataset** — lesson table == `Data.csv` == `Data.xlsx`, exactly, all three.
* **BUILD W05 world map at 390 px** — 22 labels on each of four slides, smallest rendered
  font **17 CSS px**, 0 labels clipped to zero width, 0 overlapping label pairs.

### One cross-finding this re-run turned up, which is not about the packs

Measured on 238 decks — the 220 landed, plus these three new packs — under the oracle
**as it stands on Lessons main (`17b3d554`)** and under the oracle on the unmerged #634:

```
                                        main 17b3d554     PR #634
data-type="starter" slides named 'title'        132            0
title stages per deck                 {1:107, 2:131}      {1:238}
zero-timer slides not title/complete              1            0
```

The two defects the first adversarial round found are **live on main right now**, because
the fix for them is #634 and #634 is not merged. Nothing already served is harmed —
affected decks 132, transplanted decks 62, **overlap 0** — but the affected 132 include
**all twelve GROW and LAUNCH Summer 1 lessons in these new packs**, which are precisely the
ones ruling 2 sends to intake. A Summer 1 transplant cut from main today would silently
withhold the Lundy panel from the starter stage of every one of the twelve. **#634 merges
before any Summer 1 or PASS B batch is cut.**

### Part A v2 — the index and the static E-checks, re-run on the new packs

**A0 / TEXT_INDEX — 19,649 rows, 0 NOT_RUN.** Every surface opened and read; the DOCX, PPTX,
PDF and XLSX libraries all import in this container, so no leg is silently absent.

```
rows 19,649   NOT_RUN 0   lesson ids 18 (+3 pack roots)   config rows 3,125
BUILD 6,299   GROW 6,379   LAUNCH 6,971
surfaces: config, Pupil_Resources.html/.pdf, Editable_Pack.docx, Teacher_Notes.docx/.pdf,
          Editable_Slides.pptx (+:notes), Knowledge_Organiser.html/.docx/.pdf,
          Sources_and_checks.html, START_HERE.html, Data.csv, Data.xlsx, Model_Transcript.txt
```

Every one of the 18 carries config rows. The withdrawn generation gave 19,130; this is 19,649.

**E13 residue — PASS.** 19,649 text units across 16 surfaces: **0** emails, phone numbers, file
paths, artefacts, review-copy markers, TODO, lorem, NaN, undefined or template braces. 33 name
candidates, of the same kinds as the HUM-D5 pass — table-header pairs read as names
(`Europe Southern`, `Continent Ocean`, `Cause Impact`) and historical figures.

**E2 cross-surface parity — 392 field rows × 7 surfaces, 34 coverage flags — and a gap in E2
itself.** The flags are the kinds the HUM-D5 E2 already records: 9 where the field is simply
absent on that surface (`Editable_Slides.pptx:notes` for 7 of them), and the rest case,
punctuation or truncation differences.

**None of the 34 names `provenance` or `mitigation`.** E2 compares the **config** against each
**surface**; the two held LAUNCH defects are a disagreement *between two renderings of the same
lesson* — the on-screen organiser against the print organiser and the Knowledge Organiser — and
that axis is not one E2 tests. So **E2 as built cannot see either defect**, and its PASS on this
class would have been a clean report over a comparison that was never made. The vocabulary-parity
leg is what finds them, and that is why it exists. Recorded here rather than left implied.

**Still owed on Part A:** E1 and E3–E18 on these 18. E4 (480 PDFs), E6 (axe, 18 × 9 × 2), E8
(video) and E17 are the heavy legs and have not been re-run on the new artefacts; E10/E11 remain
NOT RUN for want of egress, exactly as for the 120.

## ADDENDUM 3 v3 — INTAKE on the PACK-1R_v3 packs, 2026-09-21

Three v3 zips arrived; the GROW v3 zip was **not in the container** and is requested. Every
claim in the addendum's cover text was re-measured here on the delivered bytes before it was
believed; nothing below is copied from the cover.

### Hash on arrival, and A3.0 v3 by content

```
Humanities_Summer_1_LAUNCH_Weeks_01-06_PACK-1R_v3.zip   251f190b3584b877ba77cebfb6ccb63a3ce8307a8ee41031873982baa119f505   4,543,989 B
Humanities_Summer_1_BUILD_Weeks_01-03_PACK-1R_v3.zip    1c4edef4c911980e607f957b0569da9c83ab67249aa6a3e066833f9b6966adb7   4,445,375 B
Humanities_Summer_1_BUILD_Weeks_04-06_PACK-1R_v3.zip    b902013aec3313649faeb3ca123740d961f904d846f03247fa0ef2e265d6173d   3,836,139 B
```

| pack | SHA256SUMS by content | files | lessons |
|---|---|---|---|
| LAUNCH W01–06 | 105/105, 0 failed, 0 missing | 106 | 6 |
| BUILD W01–03  |  62/62,  0 failed, 0 missing |  63 | 3 |
| BUILD W04–06  |  60/60,  0 failed, 0 missing |  61 | 3 |

227/227 delivered here; the addendum expects 330 across four packs, so GROW v3 accounts for
the remainder. **One id, one file: 12/12.** The v2 extractions stay quarantined; no lesson id
has two live generations in front of an instrument.

### CHANGELOG byte-offset claims — checked, not believed

Each changelog names a Before and After SHA-256 per lesson, zero-based byte ranges with old
and new hex, and says no byte outside those ranges changes. Against the v2 bytes held here:

```
After-SHA matches the delivered v3 file     : 12 of 12
Before-SHA matches the v2 copy held here     : 12 of 12
applying the listed hex patches to v2, highest offset first, reproduces v3 byte for byte : 12 of 12
first differing byte lies inside a listed range                                          : 12 of 12
teaching files (DOCX/PPTX/PDF/MP4/CSV/XLSX/SVG/PNG) byte-identical to v2 : 74 + 32 + 37, 0 differ
```

BUILD W01 is declared UNCHANGED and is byte-identical. The LAUNCH edits are one or two
organiser cells per lesson; the BUILD W02–W06 edits are six single-byte `1`→`2` demotions
(three `<h1>`→`<h2>` pairs).

### Ruling 2 — the two LAUNCH holds are CLEARED on the bytes

| lesson | word | screen | print | Knowledge Organiser |
|---|---|---|---|---|
| `LAUNCH_SU1_W01` | provenance | Who made a source, when and why | same | same |
| `LAUNCH_SU1_W02` | mitigation | Reducing greenhouse-gas emissions or increasing their removal | same | same |

One definition on all three surfaces, the KO's. 12/12 clean on the by-word check.

### Correction #30 restated — `<h1>` on the STATIC document, script strings and dialog templates excluded

```
lesson            all <h1>   in a script string   in a dialog / v4-modal   print-only   STATIC
every one of 12          2                    1                        0            0        1
```

**12/12.** The second `<h1>` in every v3 lesson sits inside a script string (the
organiser-dialog template). That was **not** so in v2: there the extra `<h1>`s in BUILD W02–W06
were real elements in `v4-modal` divs and the print organiser, at `inside=None` under the same
measurement — v3's six demotions are what moved them. The exemplar-parity claim holds for v3.

### Ruling 3 v3 — `Sources_and_checks.html`

Every internal link out of every copy, and every lesson → Sources link, resolved to a real file
and a real id: LAUNCH 45, BUILD W01–03 5, BUILD W04–06 3 — **0 broken**. `_records` copies
byte-identical to the root copy in all three packs (LAUNCH 1, BUILD W01–03 4, BUILD W04–06 1).

### G-vocab — a new check, red-proved on the bytes the ruling names

`_passhumd5/scan_gvocab.py`. A lesson's vocabulary is on three surfaces a pupil can meet — the
on-screen organiser, the print organiser, the Knowledge Organiser — and they must agree on
**(1) the set of terms** and **(2) the definition of every shared term**. Clause (1) exists
because of what the v1/v2 LAUNCH packs carried: a first screen row (`sustainability`, with a
definition belonging to no term) that print and KO did not carry at all. A by-word comparison
had nothing to compare it with and passed it — the vocabulary-parity leg above reported
16/18 clean on v2 for exactly that reason. Set equality is what sees a row present on one
surface only. Where a KO carries its words as `word: meaning` prose under "Words to use" rather
than a table (BUILD W01), the check reads that form from the file's own structure.

```
self-test (8 controls, exit 0):
  v1 withdrawn LAUNCH   6/6 flag   W01,W02 by definition · W03–W06 by term-set (screen-only row)
  v2 LAUNCH             6/6 flag   same six, same kinds
  v3 W04 clean before seeding; seeded control flags exactly one definition defect, screen only
v3, 12 lessons  : 12/12 clean, exit 0
v2, 18 lessons  :  6/18 flagged — exactly the six LAUNCH lessons (record)
```

The instrument arrives as an added file and is admitted and pinned rather than taking the
boundary's free pass.

### G-B / G-C / G-D / E6 on v3

* **G-B — PASS 24/24 rows.** Real Chromium, each pack served over http from its own root,
  every stage activated, 390 and 1280: 0 page errors, 0 console errors, 0 off-origin, no
  horizontal overflow. GPT's own browser leg is recorded NOT RUN; this is the line that runs it.
* **G-C — PASS 12/12.** **G-D — PASS**: rendered 12/12; whole-pack incl. binary, 0 library
  failures; LAUNCH 61 occurrences in 22 files, all staff or config sentences of the three
  named kinds; BUILD 0; **0 pupil-visible.**
* **E6 — axe 4.10.2, 12/12 run, 216 stage × viewport, 0 NOT RUN.** `color-contrast` serious on
  216/216 (the `#auto-timer-display` / `.at-btn` chrome at 3.17:1 and 3.68:1, and the ruled
  REPORT-ONLY model-node ribbon at 1.19:1); **0 `svg-img-alt`, 0 `nested-interactive`** — the
  v2 run's 12 and 10 were on GROW only, and GROW v3 is not here. 0 of 12 free of a serious
  finding, as for the 120.

### Still held / still owed

* **GROW v3** — not in the container; A3.0's 330 and G-vocab / G-B / E6 on GROW await it.
* **NOAA 2025 (427.35 ppm)** — UNVERIFIED-BY-CLAUDE, pending Matt (ruling 6).
* **Landing** — only after intake closes on all four packs, by the SX1-style route the
  addendum names; nothing has landed.
