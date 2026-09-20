# HUMD5_PARTA_CLOSE — HUM-D5 Part A, closed under ORDER FINISH H1–H9 (2026-09-20)

Scope: the 13 zips as unpacked (12 distinct packs, 120 lessons: 78 Humanities + 42 RE; 106 Final + 14 Fallback), proofed in the workspace `/tmp/claude-0/humd5/unzipped`, with every instrument and record on Lessons branch `claude/hum-d5-proof` under `_passhumd5/`. Nothing has been landed: Part B is PREPARE ONLY (see PARTB_PLAN.md, STOP-B1). Every count here was produced by the named instrument and re-checked on it; the four workflow subagents that scoped the H4/H5/H6 edits were read-only and their figures were re-measured before any write.

## 1. What was done, per pack

Class A = the mechanical proof fixes (A0001–A0027: house spellings, joins after "means", spacing after punctuation, doubled full stops, DOCX heading punctuation). H2 = A0028 (arrival reminder strip loses its answer). H5/H6 = A0029–A0038 (Matt's rulings: LAUNCH button token, BUILD/GROW timer ink, rank-select label, svg names, config.sehm). "edits" are file-level exact-match replacements by `apply_proof.py`; "rows" are the ledger occurrences they discharge.

| pack | lessons | Class A edits / rows / files | H2 edits (files) · PDFs re-rendered | H5+H6 edits (Lesson.html files) | sums |
|---|---|---|---|---|---|
| HUM_00_SoW_and_Order | — | 2 / 2 / 2 | — | — | no SHA256SUMS in pack |
| HUM_Autumn_1_BUILD_GROW_Fallback | 14 | 0 | — (no reminder surface) | 54 (14) | MANIFEST.json rehashed (14 entries) |
| HUM_Autumn_1_LAUNCH_Final | 7 | 12 / 23 / 12 | 12 (12) · 12 | 14 (7) | regenerated |
| HUM_Autumn_2_BUILD_Final | 7 | 11 / 16 / 10 | 12 (12) · 12 | 26 (7) | regenerated |
| HUM_Autumn_2_GROW_Final | 7 | 13 / 21 / 13 | 12 (12) · 12 | 28 (7) | regenerated |
| HUM_Autumn_2_LAUNCH_Final | 7 | 11 / 13 / 10 | 12 (12) · 12 | 21 (7) | regenerated |
| HUM_Spring_1_BUILD_GROW_Final | 12 | 13 / 23 / 11 | 20 (20) · 20 | 38 (12) | regenerated |
| HUM_Spring_1_LAUNCH_Final | 6 | 6 / 11 / 6 | 10 (10) · 10 | 12 (6) | regenerated |
| HUM_Spring_2_BUILD_GROW_Final | 12 | 8 / 12 / 8 | 20 (20) · 20 | 42 (12) | regenerated |
| HUM_Spring_2_LAUNCH_Final | 6 | 5 / 7 / 5 | 10 (10) · 10 | 18 (6) | regenerated |
| RE_Autumn_BUILD_Final | 14 | 22 / 35 / 17 | 24 (24) · 24 | 42 (14) | regenerated |
| RE_Autumn_GROW_Final | 14 | 32 / 70 / 27 | 24 (24) · 24 | 42 (14) | regenerated |
| RE_Autumn_LAUNCH_Final | 14 | 85 / 272 / 54 | 24 (24) · 24 | 28 (14) | regenerated |
| **total** | **120** | **220 / 505 / 175** | **180 (180) · 180** | **365 (120)** | 11 packs + Fallback manifest |

H3 (B0003): nothing moved — STOP-X, see §3. H4: nothing edited — report, see §3. Each pack's CHANGELOG_Final carries a "Rulings applied 2026-09-19" block with its own counts; the Fallback READ_ME carries the equivalent note. Idempotence: the full map re-run plans 0 edits / 945 already applied / 0 refusals.

## 2. The rulings and what came back (B0001–B0130)

Full table with measurements: `PROOF_LEDGER.md` § "Rulings applied 2026-09-19". Compact:

| ruling | ids | disposition |
|---|---|---|
| H1 | B0001 | BY DESIGN, recorded; KO "Remember" line unchanged (218/218) |
| H2 | B0002 | DEFECT, uniform proved (90 lessons, one shape, 628 occurrences), applied; re-measured: strip route 106 → 0; 16 W01 word-help variants held by id |
| H3 | B0003 | STOP-X: the five are evidence-card text (2), a safety instruction (1), a scanner apostrophe variant (1) and a Choose-hint (1); no move without a ruling |
| H4 | B0004–B0005 | REPORT: no Sources_and_checks row names any image; existing credits listed; the no-credit list is in §3; no image removed, nothing invented |
| H5 | B0008 | INSTRUMENT ARTEFACT (correction #12): rect read mid-fadeIn; at rest 44 px on all 120 by offsetHeight and rect; closed, no edit |
| H5 | B0123 | APPLIED: LAUNCH `--btn-bg` #3b82f6 → #2563eb (5.17:1), 40 files, 80 occurrences |
| H5 | B0124 | APPLIED: BUILD/GROW timer ink #985719 (5.66:1) in the `#auto-timer` rule pair, 80 files |
| H5 | B0125 | REPORT ONLY (ruled): model-node 1.2:1; one-string fix named for Matt |
| H5 | B0126, B0130 | RE-MEASURED after the edits — E6 POST, §4 |
| H5 | B0127/B0128 | APPLIED: 78 static svg openers named in 38 lessons; maps as `role=group` |
| H5 | B0129 | APPLIED: `#rank-criterion` bound to its label (engine string, 120 files; renders in 4) |
| H6 | B0016–B0027 | NOT DERIVABLE: 5 of 24 target lessons carry a monitoring line and share none; nothing authored |
| H6 | B0028–B0034 | APPLIED where derivable: config.sehm (one population string) into the 7 GROW_A1 configs; visible gap stays (no renderer, no docx there) |
| H7 | B0006, B0007, B0009–B0015, B0035–B0093, B0094–B0122 | REPORT ONLY |
| H8 | E10, E11, E8 OCR | NOT RUN with reason (proxy-refused URLs; unreachable cited pages; no tesseract) |

## 3. Residue — what is still open, led by the Fallback 14

**The Fallback 14 (HUM Autumn 1 BUILD W01–W07, GROW W01–W07).** The Reviewed zip arrived truncated; the Fallback ships 8 files per lesson (Lesson.html, KO html+pdf, Pupil_Resources.pdf, Teacher_Notes.pdf, Editable_Pack.docx, Editable_Slides.pptx, Captioned_Model.mp4) and no Pupil_Resources.html, Teacher_Notes.docx, Sources_and_checks.html, README, SHA256SUMS or Review_record. Consequences: no `#save-independent` (E16), no config.sehm/re_safeguard/media_note (config parity now restored for sehm in GROW_A1 only), no re-renderable PDF, video safe-area not measurable, no credit surface. They received the H5 edits (54 in 14 files) like every other lesson. A Final pack for these 14 remains the input Part B needs (R13 Fallback branch otherwise).

**Eight Teacher_Notes.pdf not re-rendered** (Class A edited their DOCX; LibreOffice here cannot load any DOCX): GROW_RE_A2_W02, GROW_RE_A2_W03, LAUNCH_RE_A1_W05, LAUNCH_RE_A2_W01, LAUNCH_RE_A2_W02, LAUNCH_RE_A2_W03, LAUNCH_RE_A2_W06, LAUNCH_RE_A2_W07. Their PDFs carry the pre-proof text (house-spelling and punctuation items only).

**On-screen answer visibility after H2 (E3 POST):** 27/120 lessons still show an answer string in the default state — 26 as one option among the match-round buttons on `#slide-3` and 3 as `#slide-3 > p` word-bank/"Choose:" hints; all in the classes already recorded as by-design (a choice list must show its options). The 16 W01 word-help lines (definition of the key word) stay by design.

**H3 five (STOP-X):** BUILD_RE_A1_W02, BUILD_RE_A1_W06 (evidence-card text), BUILD_RE_A2_W04 (safety line), BUILD_S2_W04 (no answer string; apostrophe variant), GROW_RE_A2_W03 (Choose-hint, held-PDF set).

**H6 twelve not derivable:** LAUNCH_S1 W01, W03–W06; LAUNCH_A1 W01–W07 — teacher notes name no monitoring/aftercare step and the population offers no shared line to quote.

**Phone reality (B0009–B0012, report only):** at rest `summary` 18 px (20 of 25 per lesson), `a.pack-link` 42, `a.skip` 38, `a.mbmhome` 19, data-editor inputs 38, sort/rank selects 37/19; buttons are 44.

**Accessibility residue (E6 POST):** see §4.

**Video (B0094–B0122):** 29 of 120 captioned models outside 30–40 s (28–54 s); OCR leg NOT RUN. **Readability (B0035–B0093):** 59 flags, report only. **Data (B0006):** 3 CSVs carry units only in the header. **Slide notes (B0007):** 13 lessons carry the check answer in slide notes only. **E10/E11:** NOT RUN (57 URLs proxy-refused).

## 4. Re-measurement after the rulings

| instrument | before | after |
|---|---|---|
| render_visibility.js (E3, default state, 120 lessons, control 120/120) | 112 VISIBLE (106 via the reminder strip) | 27 VISIBLE (0 via the strip) |
| render_e17_b0008_atrest.js (B0008, 390×844 DPR3, 700 ms settle) | 43.5 px (rect mid-animation) | 44 px offsetHeight and rect, all 120, 0 under |
| axe 4.10.2 in situ (verify stage, 4 rank lessons; sampled map/diagram stages) | select-name critical 4/4; svg-img-alt + nested-interactive on every sampled map | 0 violations |
| render_e6_axe.js (E6, 120 × 9 stages × 2 viewports) — full re-run | color-contrast serious 120/120; svg-img-alt 27; nested-interactive 18; select-name 4 | E6 POST: pending at close time — the run is in progress; the line is filled in CHECKS.md when it lands |

## 5. Matt's decisions (nothing here was ruled by me)

1. **Media credits (H4).** Nothing invented. Existing credits that can be surfaced: Teaching_Photo figcaptions "21 November 2008 · Oliver Dixon · CC BY-SA 2.0" / "31 January 2020 · Reading Tom · CC BY 2.0" (BUILD_S1_W03/W04/W06, BUILD_A1_W04) and the Pupil_Resources "Source:" lines; in-image "© OpenStreetMap contributors" (LAUNCH_A2_W02/W04/W05/W06/W07) with Sources_and_checks rows 31/32; in-image "Natural Earth public-domain outlines" (17 world-map lessons) with row 27. **No credit anywhere:** Object_Picture_Choices.png in 61 lessons (BUILD_A2 W01–W07; BUILD_S1 W01–W06; BUILD_S2 W01–W06; all 42 RE); Teaching_Visual_1.png V1 (BUILD_A2_W01/W02/W03/W04/W07, GROW_A2_W05/W06), V2 (BUILD_S1_W02/W05), V3 (GROW_A2_W02, LAUNCH_A2_W01); Visual_Resource.png on disk in 64 lessons, referenced by nothing. The only "marked authored" statement is the Fallback Editable_Visuals READ_ME and it covers only its own SVGs.
2. **Model-node contrast (B0125).** White on `#f3e6da`/`#ede9fe` = 1.2:1 on every lesson's I-do ribbon. One byte-identical string fixes it (`.step-ribbon>*{…}` + `color:var(--text)`, 11.98:1 / 12.36:1). Report only as ruled.
3. **"Salah" heading.** 5 occurrences of the house-lowercase rule hit a heading position ("Assessment source Salah") where the capital may be the proper noun; left as found, Class B.
4. **H3 five** (§3) — move, hold, or leave.
5. **H6 twelve** (§3) — author a line, or accept the gap.
6. **Fallback GROW_A1 opt-out line** — config parity only; the pupil/teacher-visible line needs a Final pack or an authored surface.
7. **Timer ink alternative.** Applied: hard ink `#985719` in the timer template, BUILD/GROW only. Alternative on record: re-value `--ido-border` itself (35 selectors move).
8. **Phone sizes** (B0009–B0012) and the 29 video durations — report only under H7.

## 6. Instrument corrections recorded this pass
#11 a force-revealed text index is not a visibility measurement; #12 getBoundingClientRect is scaled by an ancestor's entrance animation for ~450 ms — read offsetHeight, or settle ≥ 500 ms, or measure under `prefers-reduced-motion: reduce`.
