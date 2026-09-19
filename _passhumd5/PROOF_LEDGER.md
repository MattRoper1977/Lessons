# HUM-D5 PROOF_LEDGER — Class A (mechanical, to FIX)

Scanned 123,520 text rows across 120 lessons and 20 surfaces, plus a separate
raw-file pass for whitespace (the index normalises \s+, so it cannot see it).

**27 groups · 545 occurrences · 71 lessons affected** (A0001–A0026 from the text index; A0027 from the E2 cross-surface parity check)

| id | kind | occ | current | proposed |
|---|---|---|---|---|
| A0001 | house-spelling | 130 | `Quran` | `Qur’an` |
| A0002 | house-spelling | 80 | `bar mitzvah` | `Bar Mitzvah` |
| A0003 | broken-join-after-means | 42 | `means A` | `means a` |
| A0004 | missing-space-after-punctuation | 40 | `evidence anchor B,C or read one rele` | `—` |
| A0005 | house-spelling | 36 | `bat mitzvah` | `Bat Mitzvah` |
| A0006 | missing-space-after-punctuation | 35 | `evidence anchor A,B or read one rele` | `—` |
| A0007 | missing-space-after-punctuation | 15 | `evidence anchor A,C or read one rele` | `—` |
| A0008 | missing-space-after-punctuation | 15 | `evidence anchor D,H or read one rele` | `—` |
| A0009 | broken-join-after-means | 14 | `means An` | `means an` |
| A0010 | broken-join-after-means | 7 | `means Moving` | `means moving` |
| A0011 | broken-join-after-means | 7 | `means Giving` | `means giving` |
| A0012 | broken-join-after-means | 7 | `means Weather` | `means weather` |
| A0013 | broken-join-after-means | 7 | `means Related` | `means related` |
| A0014 | broken-join-after-means | 7 | `means Important` | `means important` |
| A0015 | broken-join-after-means | 7 | `means Feeling` | `means feeling` |
| A0016 | broken-join-after-means | 7 | `means The` | `means the` |
| A0017 | broken-join-after-means | 7 | `means Showing` | `means showing` |
| A0018 | missing-space-after-punctuation | 5 | `evidence anchor C,D or read one rele` | `—` |
| A0019 | doubled-full-stop | 4 | ` day.. “Sa` | `—` |
| A0020 | doubled-full-stop | 4 | `ship.. Nam` | `—` |
| A0021 | doubled-full-stop | 4 | `eful.. It ` | `—` |
| A0022 | doubled-full-stop | 4 | `kely.. “Th` | `—` |
| A0023 | doubled-full-stop | 4 | `oice.. It ` | `—` |
| A0024 | doubled-full-stop | 4 | ` not.. Nam` | `—` |
| A0025 | broken-join-after-means | 2 | `means Unit` | `means unit` |
| A0026 | space-before-punctuation | 1 | `.` | `—` |
| A0027 | docx-heading-punctuation-stripped | 50 | `S One family s celebration plan` (and 49 more: hyphens, apostrophes, colons, commas, ?, quotes dropped from Editable_Pack.docx headings) | the config title, punctuation restored: `S One family’s celebration plan` |

## Held, not fixed

| kind | occ | why |
|---|---|---|
| house-lowercase `Salah` | 5 | heading position ("Assessment source Salah"); the capital may be correct there. Class B if it matters. |


# Class B — meaning-bearing or design-level, NOT changed, LEDGERED (numbered)

Each item is one measured finding for Matt to rule ACCEPT / REJECT / AMEND.
Nothing below was edited. Source instrument in brackets.

## Rulings requested — systematic by design (E3 / E4)

| id | lesson(s) | surface | finding | source |
|---|---|---|---|---|
| B0001 | all 120 (218/218 strings) | Knowledge_Organiser.html/.pdf, and page 1 of every printed route pack | the KO's "Remember: q? a" line prints the check question WITH its answer on the pupil organiser | E3, E4 |
| B0002 | 106/120 | Lesson.html Arrival stage (on screen, default state) and the printed arrival page | the "Previous lesson reminder:" strip (W01: "Word help: X means …") restates arrival question 1's answer verbatim; the question's hint says "Use the reminder strip" | E3, E4 |
| B0003 | 5 (BUILD_RE_A1_W01, BUILD_RE_A1_W04, BUILD_RE_A2_W05, GROW_RE_A2_W03, LAUNCH_S1_W01) | Pupil_Resources.html | the check answer appears as ordinary prose on the pupil sheet (e.g. "In a synagogue the Torah scroll is kept in a special cupboard called the Ark") | E3 |

## Media rights (E12)

| id | lesson(s) | surface | finding |
|---|---|---|---|
| B0004 | BUILD_A1_W04, BUILD_S1_W03, BUILD_S1_W04, BUILD_S1_W06 | Lesson.html figures + Pupil_Resources.html | the two Transporter Bridge photographs carry licence + author (CC BY-SA 2.0 Oliver Dixon; CC BY 2.0 Reading Tom) but no source URL on any surface where they render (0/18) |
| B0005 | 61 RE/Humanities lessons (Object_Picture_Choices.png) + 33 LAUNCH_A2 (Teaching_Visual_N.png) | Pupil_Resources.html and the inline lesson copy | `alt="Credited visual resource for this lesson"` but no visible credit or "authored" mark on the surface (94 renderings) |

## Data (E9)

| id | lesson(s) | surface | finding |
|---|---|---|---|
| B0006 | GROW_S2_W03, GROW_S2_W05, GROW_S2_W06 | Data.csv | the CSV carries the unit only in the column header ("Anomaly °C"); the reference period ("°C relative to 1951–1980") that the config, XLSX and printed table carry is absent |

## Cross-surface (E2), informational

| id | lesson(s) | surface | finding |
|---|---|---|---|
| B0007 | 13 (BUILD_A2_W07, BUILD_S1_W06, BUILD_S2_W05, GROW_A2_W06, GROW_S1_W05, GROW_S1_W06, LAUNCH_A1_W03, LAUNCH_A1_W06, LAUNCH_A1_W07, LAUNCH_A2_W07, LAUNCH_S1_W04, LAUNCH_S1_W05, LAUNCH_S2_W06) | Editable_Slides.pptx | the check answer is in the speaker notes only, not on a slide body, where the other 107 lessons carry it on both |

## Phone reality (E17), report only (R6: no restyle)

| id | scope | finding |
|---|---|---|
| B0008 | every lesson, every route/toolbar `<button>` | 43.5 px tall at 390×844 — 0.5 px under the 44 px target |
| B0009 | every lesson, 8 `<summary>` disclosures per lesson | 17.8 px tall |
| B0010 | every lesson | `a.mbmhome` "← Lessons" 72.5×19; `a.skip` 119.6×38; `a.pack-link` 346×41.9; "Printable pupil resources" link 346×18 |
| B0011 | 9 data lessons | data cells and `#chart-title` inputs 154×37.6 / 342×37.6 |
| B0012 | 103 lessons (254 stage-visits) / 111 lessons | at scroll 0 the lowest control sits partly under the fixed prev/next cluster / the 10 px progress bar until scrolled |

## Keyboard (E5), sample of 17

| id | scope | finding |
|---|---|---|
| B0013 | every lesson | no visible focus indicator on the timer buttons `button.at-btn` / `#auto-timer-toggle` (301 focus stops in the sample) |
| B0014 | every lesson with the chip starter/exit | no visible focus indicator on `button.vary-chip` (120 stops in the sample) |
| B0015 | activity boards | 15 focus stops on plain board buttons without a visible indicator |

## Sensitive content (E18), gaps

| id | lesson | gap |
|---|---|---|
| B0016–B0020 | LAUNCH_S1_W01, W03, W04, W05, W06 | teacher notes do not name a monitoring/aftercare step (W02 does: "monitor regulation") |
| B0021–B0027 | LAUNCH_A1_W01–W07 | teacher notes do not name a monitoring/aftercare step ("Use sensitive content warnings… Do not ask for family details" is a safeguard, not aftercare) |
| B0028–B0034 | GROW_A1_W01–W07 (Fallback) | no opt-out / quiet alternative stated (no `sehm` field) AND no teacher-notes surface exists to carry a monitoring step |

## Readability (E14), 59 flags — Class B

| id | lesson · route | grade | ceiling |
|---|---|---|---|
| B0035 | BUILD_A1_W01 · stretch | 6.29 | 5 |
| B0036 | BUILD_A1_W02 · stretch | 5.96 | 5 |
| B0037 | BUILD_A1_W03 · stretch | 5.13 | 5 |
| B0038 | BUILD_A1_W04 · stretch | 7.21 | 5 |
| B0039 | BUILD_A1_W05 · stretch | 6.74 | 5 |
| B0040 | BUILD_A1_W06 · stretch | 6.46 | 5 |
| B0041 | BUILD_A1_W07 · standard | 5.1 | 5 |
| B0042 | BUILD_A1_W07 · stretch | 7.26 | 5 |
| B0043 | BUILD_A2_W01 · standard | 6.34 | 5 |
| B0044 | BUILD_A2_W01 · stretch | 6.66 | 5 |
| B0045 | BUILD_A2_W02 · standard | 6.06 | 5 |
| B0046 | BUILD_A2_W02 · stretch | 6.67 | 5 |
| B0047 | BUILD_A2_W03 · standard | 5.85 | 5 |
| B0048 | BUILD_A2_W03 · stretch | 7.76 | 5 |
| B0049 | BUILD_A2_W04 · standard | 5.64 | 5 |
| B0050 | BUILD_A2_W04 · stretch | 7.06 | 5 |
| B0051 | BUILD_A2_W05 · standard | 6.3 | 5 |
| B0052 | BUILD_A2_W05 · stretch | 6.95 | 5 |
| B0053 | BUILD_A2_W06 · stretch | 6.63 | 5 |
| B0054 | BUILD_A2_W07 · standard | 6.39 | 5 |
| B0055 | BUILD_A2_W07 · stretch | 6.75 | 5 |
| B0056 | BUILD_RE_A1_W03 · stretch | 5.44 | 5 |
| B0057 | BUILD_RE_A1_W04 · stretch | 5.09 | 5 |
| B0058 | BUILD_RE_A1_W05 · stretch | 5.19 | 5 |
| B0059 | BUILD_RE_A2_W01 · stretch | 5.35 | 5 |
| B0060 | BUILD_RE_A2_W02 · stretch | 5.71 | 5 |
| B0061 | BUILD_RE_A2_W04 · stretch | 6.05 | 5 |
| B0062 | BUILD_RE_A2_W05 · stretch | 5.56 | 5 |
| B0063 | BUILD_S1_W02 · stretch | 5.99 | 5 |
| B0064 | BUILD_S1_W03 · standard | 5.53 | 5 |
| B0065 | BUILD_S1_W03 · stretch | 5.88 | 5 |
| B0066 | BUILD_S1_W04 · standard | 5.49 | 5 |
| B0067 | BUILD_S1_W04 · stretch | 6.95 | 5 |
| B0068 | BUILD_S1_W05 · stretch | 5.42 | 5 |
| B0069 | BUILD_S1_W06 · stretch | 5.85 | 5 |
| B0070 | BUILD_S2_W01 · stretch | 6.32 | 5 |
| B0071 | BUILD_S2_W02 · standard | 5.06 | 5 |
| B0072 | BUILD_S2_W02 · stretch | 5.75 | 5 |
| B0073 | BUILD_S2_W03 · stretch | 5.12 | 5 |
| B0074 | BUILD_S2_W05 · standard | 5.03 | 5 |
| B0075 | BUILD_S2_W05 · stretch | 5.34 | 5 |
| B0076 | BUILD_S2_W06 · standard | 6.17 | 5 |
| B0077 | BUILD_S2_W06 · stretch | 7.37 | 5 |
| B0078 | GROW_A1_W04 · stretch | 7.65 | 7 |
| B0079 | GROW_A1_W05 · stretch | 7.77 | 7 |
| B0080 | GROW_A1_W06 · stretch | 7.21 | 7 |
| B0081 | GROW_A1_W07 · stretch | 7.25 | 7 |
| B0082 | GROW_A2_W03 · stretch | 7.42 | 7 |
| B0083 | GROW_A2_W04 · standard | 7.51 | 7 |
| B0084 | GROW_A2_W04 · stretch | 8.11 | 7 |
| B0085 | GROW_A2_W06 · stretch | 7.13 | 7 |
| B0086 | GROW_A2_W07 · stretch | 7.12 | 7 |
| B0087 | GROW_S1_W02 · stretch | 7.16 | 7 |
| B0088 | GROW_S1_W04 · stretch | 7.48 | 7 |
| B0089 | GROW_S2_W02 · stretch | 7.01 | 7 |
| B0090 | GROW_S2_W04 · stretch | 8.07 | 7 |
| B0091 | GROW_S2_W05 · stretch | 7.52 | 7 |
| B0092 | LAUNCH_A1_W01 · stretch | 9.51 | 9 |
| B0093 | LAUNCH_S1_W06 · stretch | 9.48 | 9 |

## Accessibility (E6), report only (R6: no recolour, no restyle)

| id | scope | finding |
|---|---|---|
| B0123 | all 40 LAUNCH lessons | primary buttons white text on `#3b82f6` — 3.68:1 (below 4.5:1); the incoming LAUNCH button colour is not R6's `#9c27b0` |
| B0124 | all 120 lessons | timer text `#auto-timer-display` and timer buttons `button.at-btn` `#c9803b` on white — 3.17:1 |
| B0125 | all 120 lessons | model-node current button white on `#f3e6da` / `#ede9fe` — 1.2:1 |
| B0126 | all 120 lessons | axe `color-contrast` serious on `#previous-slide` / `#next-slide` (509 / 499 stage-visits) and `button[data-action="organiser"]` (80) |
| B0127 | 27 lessons (map SVGs) | `svg-img-alt`: inline `<svg role="img">` without an accessible name (35 nodes) |
| B0128 | 18 lessons (map SVGs) | `nested-interactive`: interactive controls inside a `role="img"` SVG (26 nodes) |
| B0129 | 4 rank-kind lessons (GROW_A1_W05, GROW_S1_W04, LAUNCH_A1_W05, LAUNCH_S1_W04) | `select-name` **critical**: `#rank-criterion` has no accessible label |
| B0130 | all 120 lessons | no lesson is free of a serious axe finding at either viewport; moderate/minor: 0 |

## Video duration (E8), 29 outside 30–40 s — Class B

| id | lesson | container duration |
|---|---|---|
| B0094 | LAUNCH_A1_W02 | 41.0 s |
| B0095 | LAUNCH_A1_W07 | 41.0 s |
| B0096 | BUILD_A2_W02 | 48.0 s |
| B0097 | GROW_A2_W02 | 29.0 s |
| B0098 | GROW_A2_W05 | 47.0 s |
| B0099 | GROW_A2_W06 | 51.0 s |
| B0100 | GROW_A2_W07 | 29.0 s |
| B0101 | GROW_S1_W01 | 47.0 s |
| B0102 | GROW_S1_W05 | 48.0 s |
| B0103 | LAUNCH_S1_W02 | 43.0 s |
| B0104 | LAUNCH_S1_W06 | 54.0 s |
| B0105 | GROW_S2_W05 | 28.0 s |
| B0106 | GROW_S2_W06 | 29.0 s |
| B0107 | LAUNCH_S2_W05 | 28.0 s |
| B0108 | BUILD_RE_A1_W05 | 48.0 s |
| B0109 | BUILD_RE_A1_W07 | 49.0 s |
| B0110 | BUILD_RE_A2_W02 | 47.0 s |
| B0111 | GROW_RE_A1_W01 | 47.0 s |
| B0112 | GROW_RE_A1_W04 | 47.0 s |
| B0113 | GROW_RE_A1_W07 | 47.0 s |
| B0114 | GROW_RE_A2_W03 | 28.0 s |
| B0115 | GROW_RE_A2_W07 | 29.0 s |
| B0116 | LAUNCH_RE_A1_W02 | 52.0 s |
| B0117 | LAUNCH_RE_A1_W04 | 47.0 s |
| B0118 | LAUNCH_RE_A1_W06 | 47.0 s |
| B0119 | LAUNCH_RE_A2_W01 | 47.0 s |
| B0120 | LAUNCH_RE_A2_W03 | 28.0 s |
| B0121 | LAUNCH_RE_A2_W05 | 50.0 s |
| B0122 | LAUNCH_RE_A2_W06 | 28.0 s |

# Class V — video captions

None ledgered: OCR of caption frames is NOT RUN (no tesseract). The text leg
(Model_Transcript.txt carries every config model step) is PASS 106/106; the 14
Fallback lessons have no transcript surface. Every video decodes (PyAV), 0 blank
sampled frames, embedded copies byte-identical.

## Rulings applied 2026-09-19 — ORDER FINISH H1–H9, disposition of B0001–B0130

Matt's rulings on the Class B ledger, what was done under each, and what came back. Every count below was re-checked on the instrument that first produced it (grep -oF / the render scripts / axe 4.10.2); the workflow subagents that scoped the edits were read-only and their figures were re-measured here before any write.

| ruling | ledger ids | disposition | what was done / measured |
|---|---|---|---|
| H1 | B0001 | **BY DESIGN, recorded** | the KO "Remember: q? a" line stays; no change to 218/218 strings |
| H2 | B0002 | **DEFECT — applied, uniform proved** | pattern uniform on 90/106 lessons ("Previous lesson reminder: <arrival Q1 answer>", one shape, 628 occurrences over config, Editable_Pack.docx, Editable_Slides.pptx notes, Pupil_Resources.html and the rendered stage/print); A0028 applied: 180 HTML + 180 DOCX/PPTX edits, 180 PDFs re-rendered (Chromium A4). **Held variants, by lesson id (16 W01)**: BUILD_A2_W01, BUILD_S1_W01, BUILD_S2_W01, GROW_A2_W01, GROW_S1_W01, GROW_S2_W01, LAUNCH_A1_W01, LAUNCH_A2_W01, LAUNCH_S1_W01, LAUNCH_S2_W01, BUILD_RE_A1_W01, BUILD_RE_A2_W01, GROW_RE_A1_W01, GROW_RE_A2_W01, LAUNCH_RE_A1_W01, LAUNCH_RE_A2_W01 — their strip is "You can begin without previous learning. Word help: X means <definition>" (a word-help line, not a reminder), untouched. **Re-measured (render_visibility.js, same instrument, 120 lessons, control 120/120)**: `#slide-2 > p` route 106 → **0**; lessons VISIBLE_IN_DEFAULT_STATE 112 → **27** (26 match-option buttons on `#slide-3 > button`, 3 `#slide-3 > p`), all in the classes already recorded as by-design in E3_VISIBLE_CLASSIFIED.json. Instrument note: the 16 W01 word-help lines no longer register because Class A A0010 ("means Moving" → "means moving") lowercased them and the instrument compares case-sensitively; the definition text is still on screen there, by design, held. |
| H3 | B0003 | **STOP-X — not applied, facts recorded** | the five "pupil-sheet prose answers" are not prose answers on inspection: BUILD_RE_A1_W02 ("…kept in a special cupboard called the Ark.") and BUILD_RE_A1_W06 ("It is held every year on 21 September.") are EVIDENCE-CARD text (config cards[].text, 8 occurrences each in Lesson.html) — moving them strips the pupil's evidence and breaks E2 parity; BUILD_RE_A2_W04 ("We use battery lights only. No real flame.") is a safety instruction; BUILD_S2_W04 maps to no answer string (apostrophe variant ’ vs ' in the scanner); GROW_RE_A2_W03 is a Choose-hint (B0002 family) and is in the held-PDF set. H3_TARGETS.json holds the five. Ruling requested before any move. |
| H4 | B0004–B0005 | **REPORT — nothing invented, no image removed** | Sources_and_checks.html is ONE file (117 byte-identical copies, md5 cbd16e17, 36 rows of URL + access check); no row names an image. Credits that already exist and can be surfaced: Teaching_Photo_1/2.jpg — figcaptions "21 November 2008 · Oliver Dixon · CC BY-SA 2.0" / "31 January 2020 · Reading Tom · CC BY 2.0" in all 4 lessons (BUILD_S1_W03/W04/W06, BUILD_A1_W04) and Pupil_Resources "Source: …" lines in the 3 S1 lessons; Teaching_Visual_1.png V4 local OSM maps (LAUNCH_A2_W02/W04/W05/W06/W07) carry "© OpenStreetMap contributors · data captured 19 September 2026" in-image plus rows 31/32 (OSM) in Sources_and_checks; V5 world maps (17 lessons) carry "Natural Earth public-domain outlines" in-image plus row 27 (Natural Earth terms). **List for Matt — no credit anywhere**: Object_Picture_Choices.png in 61 lessons (BUILD_A2 W01–W07; BUILD_S1 W01–W06; BUILD_S2 W01–W06; all 42 RE lessons); Teaching_Visual_1.png V1 unlit-object diagrams (BUILD_A2_W01/W02/W03/W04/W07, GROW_A2_W05/W06), V2 telephone diagrams (BUILD_S1_W02/W05), V3 practice map (GROW_A2_W02, LAUNCH_A2_W01); Visual_Resource.png on disk in 64 lessons, referenced by no HTML surface. The Fallback pack's Editable_Visuals/READ_ME.txt is the only "marked authored" statement and covers only its own SVGs. |
| H5 | B0008 | **INSTRUMENT ARTEFACT — closed, no edit (correction #12)** | 43.5 px was getBoundingClientRect read ~90 ms into `.slide.active`'s 450 ms fadeIn (`transform:scale(.985)` → 44 × 0.9886); offsetHeight was 44 throughout. Re-measured on all 120 at 390×844 DPR3 after a 700 ms settle (E17_B0008_ATREST.json): every button 44 px by both offsetHeight and rect, 0 lessons under. The same artefact explains 17.8/37.6/41.9 in E17; the at-rest sizes are summary 18, `a.pack-link` 42, `a.skip` 38, `a.mbmhome` 19, inputs 38, `select` 37 — B0009–B0012 stay report-only under H7. |
| H5 | B0123 | **APPLIED — one token value per LAUNCH pack (A0029)** | `--btn-bg:#3b82f6` → `#2563eb` in the 40 LAUNCH Lesson.html (80 occurrences: the :root copy and the effective body block); white on #2563eb = 5.17:1. BUILD/GROW untouched: their effective copies (#4e7a9b 4.58:1, #3f7d6e 4.81:1) already pass and their :root copy is inert (proved by injection). |
| H5 | B0124 | **APPLIED — one template change per BUILD/GROW pack (A0030/A0031)** | the `#auto-timer` rule pair (byte-identical 120/120, two copies per file) now sets ink `#985719` (5.66:1 on white, 4.62:1 on the hover bg) in the 80 BUILD/GROW lessons; the border keeps `var(--ido-border)` (non-text, 3.17:1 ≥ 3:1). LAUNCH's timer ink `#7c3aed` (5.70:1) untouched. The alternative (re-valuing `--ido-border` itself, 35 selectors) is recorded, not taken. |
| H5 | B0125 | **REPORT ONLY (ruled)** | model-node `.current` white on `#f3e6da`/`#ede9fe` 1.2:1; the one byte-identical string that would fix it is `.step-ribbon>*{…background:var(--ido-bg);padding:16px…}` → add `color:var(--text)` (11.98:1 / 12.36:1). Matt's call. |
| H5 | B0129 | **APPLIED — one engine string, all 120 (A0032)** | `#rank-criterion` select bound to its visible label with `l.htmlFor='rank-criterion'` (the engine's own pattern for the sort selects); renders in the 4 rank lessons. |
| H5 | B0127/B0128 | **APPLIED — one opener string per svg class (A0033–A0037)** | 78 static `<svg role="img">` openers in 38 lessons named: world map 900×450 (31/17) and practice grid 920×430 (20/7) and local map 850×520 (9/5) → `role="group"` + aria-label (names from config map_mode and the lesson prose; their place buttons are no longer nested inside an image); object diagrams 900×400 (14/7) and telephone diagrams 900×410 (4/2) → aria-label = the svg's own first caption. Pupil_Resources.html / KO carry no `role="img"` svg (0 files). |
| H5 | B0126, B0130 | **RE-MEASURED after the edits (E6, same instrument)** | see the E6 POST line in CHECKS.md |
| H6 | B0016–B0027 | **NOT DERIVABLE — report, nothing authored** | the "compliant population" for a teacher-notes monitoring/aftercare line is 5 of the 24 target lessons, and those five share no body line: "; monitor regulation" (3, appended to the "Evidence to retain: F:" line), "monitor emotional response(s)" (3 RE, three different sentences), "offer a structured break" (1). No population standard exists to insert into LAUNCH_S1 W01/W03–W06 or LAUNCH_A1 W01–W07; inserting any of the fragments would be authoring. The 106-carrier line that IS uniform (config.sehm: "Offer a predictable start, private response and agreed pause…") is already in all 12. |
| H6 | B0028–B0034 | **APPLIED where derivable (A0038), gap stated** | config.sehm — one distinct string across its 106 carriers, verified by parse of all 120 configs — inserted into the 7 GROW_A1 Fallback configs after `sow_page`. Nothing authored. No renderer reads the key and these 7 lessons have no Teacher_Notes.docx (Fallback ships PDFs only), so this is config parity: the pupil/teacher-visible opt-out line is still absent there. The RE "not worship / nobody asked to share" line (re_safeguard) is untouched everywhere (42 RE carriers verified). |
| H7 | B0006, B0007, B0009–B0015, B0035–B0093, B0094–B0122 | **REPORT ONLY** | unchanged |
| H8 | E10, E11, E8 OCR leg | **NOT RUN, with reason** | E10 57 URLs proxy-refused (CONNECT 403); E11 cited pages unreachable; E8 OCR needs tesseract (absent). Never ABSENT. |

Apply record: `apply_proof.py` map A0029–A0038, 365 planned edits in 120 Lesson.html, 0 refusals; second write 0 planned / 365 already applied; full-map dry run 0 planned / 945 already applied (idempotent). `raw` groups (markup and config-structure edits) are validated after the write by re-parsing `window.CLASSIC_LESSON` in every touched file (120/120 parse). SHA256SUMS.txt regenerated in the 11 Final packs and the Fallback MANIFEST.json rehashed (14 entries); each pack's CHANGELOG carries a "Rulings applied 2026-09-19" block with its own counts.
