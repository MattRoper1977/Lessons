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
