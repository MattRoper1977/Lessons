# Pass SL — SoW/LAUNCH Alignment Audit — FINDINGS

**Status: PHASE 1 COMPLETE (measure-only). Held at the Phase-1/Phase-2 gate — awaiting
Matt's answers to the week-mapping DECISION GATE and the decision items below. No lesson file
touched; nothing merged.**

## Lineage
- **Brief:** "PASS SL — MASTER BRIEF: LAUNCH LESSONS vs THE 2026-27 LAUNCH SoW"
- **Repo:** `mattroper1977/lessons` (verified — NOT the site repo)
- **Build base:** `32ca685e1df619b333f3ee4385aed227aa675cdf` (origin/main tip @ session start)
- **Working branch:** `pass-sl-sow-launch` (off build base; never commits to main)
- **Ledger:** "Pass SL" — no pre-existing `_passsl` at base, no self-rename.
- **SoW input:** `_passsl/inputs/LAUNCH KS4 - 2026-27.xlsx` (sha256 head `05f385ae…`, 11 sheets).
- All measurements **measured @ 32ca685**. Units stated per count.

## Session setup (Section 0) — done
Repo identity corrected (session opened on the **site repo** — the exact default the brief warns
of; rejected per §0.1, then `mattroper1977/lessons` attached & verified). Base pinned; branch
created; SoW committed to `_passsl/inputs/`; extracted to `_passsl/sow_extract/`.

## Quarantine state AS FOUND (§4f) — verified @ 32ca685
- **Assessed files present** (measure/propose-only, no patch w/o per-file auth): `Launch/Slideshows/LAUNCH_HUM_W7_Source_Assessment.html`, `Grow/Slideshows/GROW_HUM_W7_Write_The_Account.html`.
- **Art_Teesside quarantine:** 53 tracked files under `Art_Teesside/`; the 8 `Art_Teesside/Launch/LAUNCH_ART_W*` LAUNCH lessons measured but **fixes proposed-only** until Matt lifts quarantine in writing.
- **D&T:** `DT_Community_Upcycling/` = 2 files; standing no-touch on v5 printPack id lists / Lundy print page — not in LAUNCH lesson population (confirmed).
- **Storage keys / `ps_coldcall_roster`:** untouched.

---

## Divergences from brief premises (brief-verification rule — these bind upward)
1. **SoW weekly grid is NOT uniformly "W1–W7 per half term."** Derived from the workbook:
   Autumn Aut1 **W1-7** / Aut2 **W1-7**; Spring Spr1 **W1-6** / Spr2 **W1-6**; Summer Sum1 **W1-6** / Sum2 **W1-7**.
   The brief's "W1–W7" holds for Autumn only. Weekly records: Autumn 252, Spring 216, Summer 234 (= 702). This reshapes the §4c week-mapping gate.
2. **No `LAUNCH_`-prefixed files at repo root.** LAUNCH population is folder-scoped (`Launch/`, `Art_Teesside/Launch/`, `Humanities_Teesside/LAUNCH_*`, science suites) — not root-prefixed as §4a implies.
3. **`resources.json` also present in THIS (Lessons) repo** (7082 lines). Brief says catalogue lives in the site repo (read-only). Treating site copy as authoritative; neither written.
4. **The SoW is 18 strands ✓** (brief correct). Themes ✓ (Autumn Identity & Belonging / Spring Resilience & Change / Summer Our World, My Future). N2 Foundation-tier & N6 PEQ-boundary statements ✓ present in Qualification Map.

---

## §4a — LAUNCH population (mechanical enumeration, measured @ 32ca685)
**Derivation rule:** LAUNCH-serving teaching HTML in the four LAUNCH-scoped areas + GCSE-level
science suites (per §4a). Support/index/README files and other pathways (GROW/BUILD/primary/Games/
LundyLoop) excluded.

**65 lesson files** extracted across surfaces, per-suite split:

| Suite | Files | Strand served |
|--|--|--|
| `Launch/` ART identity (`Art_L1/L2` v5) | 2 | Creative Arts |
| `Launch/Slideshows/LAUNCH_ART_W1–W8` | 8 | Creative Arts |
| `Launch/Slideshows/LAUNCH_HUM_W1–W8` | 8 | Humanities (Hist/Geog) |
| `Art_Teesside/Launch/LAUNCH_ART_W1–W8` (QUARANTINED) | 8 | Creative Arts |
| `Humanities_Teesside/LAUNCH_*` (pack + SoW) | 2 | Humanities |
| `biology/` | 11 | Science (Biology 1BI0) |
| `chemistry/` | 9 | Science (Combined / IGCSE option) |
| `2 Physics 10/` (+`/Waves`) | 17 | Science (Combined / IGCSE option) |
| **TOTAL (files)** | **65** | |

**Near-twin variants (NOT byte-identical — md5-distinct; population-hygiene, not alignment defects):**
`2 Physics 10/L2_Voltage_Current_Resistance.html` vs `…-1.html`;
`…/L2b_Ohms_Law_PhET_Practical-1.html` vs `…_1.html` (+`L2c_…_Take2 (1).html`);
`biology/L4_Aerobic.html` vs `biology/L4_Aerobic_Respiration.html`.
Canonical-vs-legacy selection needs the catalogue (resources.json, site repo) — **not resolved this pass**.

## §4b — Coverage matrix (18 SoW strands → LAUNCH lesson suites)
**LAUNCH lessons exist for only 3 of 18 strands** (+ the IGCSE-option strand via chem/phys).
Absence of a suite is a coverage report only — **NOT a defect this pass fixes** (§4b).

| # | SoW strand | LAUNCH lessons in repo? |
|--|--|--|
| 3 | Science (Biology 1BI0 F) | **Yes** — `biology/` (11) |
| 4 | Humanities, History & Geography (NC KS3/4) | **Yes** — `Launch/HUM` (8) + `Humanities_Teesside` (2) |
| 11 | Creative Arts (Trinity Silver/Gold) | **Yes** — `Launch/ART` (8) + `Art_L1/2` (2) + `Art_Teesside/Launch` (8, QUAR) |
| 17 | Science – IGCSE option (4CH1/4PH1/4BI1) | **Partial** — `chemistry/` (9) + `2 Physics 10/` (17) map here; chem cites 4SS0 (see D2) |
| 1,2,5,6,7,8,9,10,12,13,14,15,16,18 | English, Maths, GCSE Hist 8145, GCSE Lit 8702, PEQ, Employability, Independent Living, Vocational, PSHE/RSHE/Citizenship, PE, RE, D&T, Community Project, Young Duke | **No LAUNCH suite** — coverage report only |

## §4c — Week-mapping table — **DECISION GATE (unresolved; needs Matt)**
| Suite | Repo weeks | SoW target | Mapping status |
|--|--|--|--|
| `Launch/HUM W1–W8` | W1–W8, self-labelled **Aut 1** | Aut1 History (7 wks) + Aut2 Geography (7 wks) | W1–W7 → Aut1 History (clean); **W8 = OS-Map/Geography = SoW Aut2** but self-labels Aut1 → week/term-label question |
| `Art_Teesside/Launch W1–W8` | W1–W8, self-labelled **Aut 1** | Creative Arts Aut1 (develop) + Aut2 (experience/review) | 8-wk arc spans BOTH half-terms but labels all Aut1; fold-into-7 or span Aut1–2? |
| `Launch/ART W1–W8` | W1–W8, **no self-SoW label** | Creative Arts Autumn | Same 8-wk arc; parallel/legacy vs Teesside suite |
| `biology/`, `chemistry/`, `2 Physics 10/` | **no week labels; topic-based** | Science by topic across the year | Topics (respiration/digestion/acids/circuits/waves) = **Combined/IGCSE content mapping to Spring/Summer**, NOT Autumn Biology (cells/mitosis/genetics) — term/topic mapping unresolved |

## Non-negotiable check (§3) — results measured @ 32ca685
- **N1 (spec codes):** Humanities correctly cites **no** GCSE code (NC KS3/4). Creative Arts cites **Arts Award Silver/Gold** ✓. **Chemistry pH/Ions cite `Edexcel IGCSE 4SS0`** — off the SoW Qualification Map → **decision item D2**. Biology & Physics cite **no** accreditation string (N1 PARTIAL candidate — pending whether expected).
- **N2 (tier ceiling):** No Higher-tier **demand** found in visible LO/SC. ("Higher tier" tokens appeared only inside `<script>`/CSS, not taught content — verified false positives.) **Zero Foundation caps introduced.** N2 clean in visible surfaces.
- **N3 (term theme):** Autumn theme present as content-framing in Art (Identity named) and Humanities (migration/belonging) though not always literally named — acceptable per N3 ("framing, not forced content").
- **N4/N5 (vocab / assessment rhythm):** Per-lesson vocab-vs-SoW and F/S-rhythm comparison **deferred to Phase 2** (gated); HUM W7/GROW_HUM_W7 are the assessed points and are quarantined.
- **N6 (PEQ boundary), N7 (SEND), N8 (estate structure):** No PEQ LAUNCH lessons in scope; SEND/estate machinery **byte-preserved** (no edits this pass).

## DECISION ITEMS (Tier-3 — report only, never auto-fixed)
- **D1 — Two parallel suites per subject.** Art: `Launch/ART` (older v5, no SoW label) vs `Art_Teesside/Launch` (newer, SoW-labelled, quarantined). Humanities: `Launch/HUM` slides vs `Humanities_Teesside` pack. Which is **canonical** vs legacy? Silently aligning the wrong one would revert a decision. **Needs Matt.**
- **D2 — `Edexcel IGCSE 4SS0` in chemistry** (`Lesson2_pH_Scale`, `Lesson3_Ions_Neutralisation`). This is N1's IGCSE/"legacy Single Science" exception. **Reading A:** stale code → SoW route is 1SC0 (Combined) / 4CH1 (separate) → fixable. **Reading B:** live optional IGCSE route for eligible students → do NOT rewrite. Tabled with both readings per N1. **Needs Matt.**
- **D3 — Science term/topic mapping.** Science lessons carry no SoW week labels and teach topics the SoW places in Spring/Summer, not Autumn. Confident per-week classification is impossible until Matt confirms which term/topics these suites serve.

## Phase-1 verdict table (one row per lesson; row count = population = 65)
Tally: MAPPING-PENDING 35 · PARTIAL 9 · DECISION/QUAR 8 · ALIGNED\* 7 · SOW-SILENT? 4 · MISALIGNED? 2 · **= 65**.
`ALIGNED*` = strong SoW self-alignment pending Phase-2 SC-operationalisation spot-check. Full table below.

| # | Strand | File | self-SoW | wk | SC | code(visible) | Class | Note |
|--|--|--|--|--|--|--|--|--|
| 1 | Creative Arts | `Launch/Art_L1_Colours_Lines_Like_Me_v5.html` | — | — | - | — | **SOW-SILENT?** | v5 identity lessons (Art_L1/L2); no SoW week; likely legacy — report only |
| 2 | Creative Arts | `Launch/Art_L2_My_Identity_Picture_v5.html` | — | — | - | — | **SOW-SILENT?** | v5 identity lessons (Art_L1/L2); no SoW week; likely legacy — report only |
| 3 | Creative Arts | `Launch/Slideshows/LAUNCH_ART_W1_Gallery_Detectives.html` | — | — | - | Arts Award Silver | **PARTIAL** | Arts Award Silver present but NO self-SoW label, no 'Success looks like' idiom, theme not named — older v5-style; parallel to Art_Teesside/Launch (canonical?) |
| 4 | Creative Arts | `Launch/Slideshows/LAUNCH_ART_W2_Symbolism_Self_Portrait.html` | — | — | - | Arts Award Silver | **PARTIAL** | Arts Award Silver present but NO self-SoW label, no 'Success looks like' idiom, theme not named — older v5-style; parallel to Art_Teesside/Launch (canonical?) |
| 5 | Creative Arts | `Launch/Slideshows/LAUNCH_ART_W3_Practitioner_Research.html` | — | — | - | Arts Award Silver | **PARTIAL** | Arts Award Silver present but NO self-SoW label, no 'Success looks like' idiom, theme not named — older v5-style; parallel to Art_Teesside/Launch (canonical?) |
| 6 | Creative Arts | `Launch/Slideshows/LAUNCH_ART_W4_Refine_With_Feedback.html` | — | — | - | Arts Award Silver | **PARTIAL** | Arts Award Silver present but NO self-SoW label, no 'Success looks like' idiom, theme not named — older v5-style; parallel to Art_Teesside/Launch (canonical?) |
| 7 | Creative Arts | `Launch/Slideshows/LAUNCH_ART_W5_Plan_The_Experience.html` | — | — | - | Arts Award Silver | **PARTIAL** | Arts Award Silver present but NO self-SoW label, no 'Success looks like' idiom, theme not named — older v5-style; parallel to Art_Teesside/Launch (canonical?) |
| 8 | Creative Arts | `Launch/Slideshows/LAUNCH_ART_W6_Experience_The_Event.html` | — | — | - | Arts Award Silver | **PARTIAL** | Arts Award Silver present but NO self-SoW label, no 'Success looks like' idiom, theme not named — older v5-style; parallel to Art_Teesside/Launch (canonical?) |
| 9 | Creative Arts | `Launch/Slideshows/LAUNCH_ART_W7_Begin_The_Review.html` | — | — | - | Arts Award Silver | **PARTIAL** | Arts Award Silver present but NO self-SoW label, no 'Success looks like' idiom, theme not named — older v5-style; parallel to Art_Teesside/Launch (canonical?) |
| 10 | Creative Arts | `Launch/Slideshows/LAUNCH_ART_W8_Complete_The_Review.html` | — | — | - | Arts Award Silver | **PARTIAL** | Arts Award Silver present but NO self-SoW label, no 'Success looks like' idiom, theme not named — older v5-style; parallel to Art_Teesside/Launch (canonical?) |
| 11 | Humanities | `Launch/Slideshows/LAUNCH_HUM_W1_Source_Investigation.html` | Humanities Aut 1 | 1/8 | Y | — | **ALIGNED*** | Self-declared SoW Aut1 Wk match; SC present; NC KS3/4 (no code correct). *pending SC-operationalisation spot-check |
| 12 | Humanities | `Launch/Slideshows/LAUNCH_HUM_W2_Cause_Consequence_Courtroom.html` | Humanities Aut 1 | 2/8 | Y | — | **ALIGNED*** | Self-declared SoW Aut1 Wk match; SC present; NC KS3/4 (no code correct). *pending SC-operationalisation spot-check |
| 13 | Humanities | `Launch/Slideshows/LAUNCH_HUM_W3_Archive_NOP.html` | Humanities Aut 1 | 3/8 | Y | — | **ALIGNED*** | Self-declared SoW Aut1 Wk match; SC present; NC KS3/4 (no code correct). *pending SC-operationalisation spot-check |
| 14 | Humanities | `Launch/Slideshows/LAUNCH_HUM_W4_Century_Of_Change.html` | Humanities Aut 1 | 4/8 | Y | — | **ALIGNED*** | Self-declared SoW Aut1 Wk match; SC present; NC KS3/4 (no code correct). *pending SC-operationalisation spot-check |
| 15 | Humanities | `Launch/Slideshows/LAUNCH_HUM_W5_People_Modern_Britain.html` | Humanities Aut 1 | 5/8 | Y | — | **ALIGNED*** | Self-declared SoW Aut1 Wk match; SC present; NC KS3/4 (no code correct). *pending SC-operationalisation spot-check |
| 16 | Humanities | `Launch/Slideshows/LAUNCH_HUM_W6_Structured_Account.html` | Humanities Aut 1 | 6/8 | Y | — | **ALIGNED*** | Self-declared SoW Aut1 Wk match; SC present; NC KS3/4 (no code correct). *pending SC-operationalisation spot-check |
| 17 | Humanities | `Launch/Slideshows/LAUNCH_HUM_W7_Source_Assessment.html` | Humanities Aut 1 | 7/8 | Y | — | **ALIGNED*** | Self-declared SoW Aut1 Wk match; SC present; NC KS3/4 (no code correct). *pending SC-operationalisation spot-check |
| 18 | Humanities | `Launch/Slideshows/LAUNCH_HUM_W8_OS_Map_Skills.html` | Humanities Aut 1 | 8/8 | Y | — | **PARTIAL** | Self-labels Aut1 but OS-Map=Geography content sits in SoW Aut2; week-label vs term-mapping (4c gate) |
| 19 | Creative Arts | `Art_Teesside/Launch/LAUNCH_ART_W1_Frame_the_Local_Challenge.html` | Arts Aut 1 | 1/8 | Y | — | **DECISION/QUAR** | SoW-labelled Aut1 8-wk arc (develop→experience→review) vs SoW 7-wk half-terms; QUARANTINED → propose-only; parallel to Launch/ART (canonical?) |
| 20 | Creative Arts | `Art_Teesside/Launch/LAUNCH_ART_W2_Practice_Careers_and_Pathways.html` | Arts Aut 1 | 2/8 | Y | — | **DECISION/QUAR** | SoW-labelled Aut1 8-wk arc (develop→experience→review) vs SoW 7-wk half-terms; QUARANTINED → propose-only; parallel to Launch/ART (canonical?) |
| 21 | Creative Arts | `Art_Teesside/Launch/LAUNCH_ART_W3_Implement_and_Critically_Develop.html` | Arts Aut 1 | 3/8 | Y | — | **DECISION/QUAR** | SoW-labelled Aut1 8-wk arc (develop→experience→review) vs SoW 7-wk half-terms; QUARANTINED → propose-only; parallel to Launch/ART (canonical?) |
| 22 | Creative Arts | `Art_Teesside/Launch/LAUNCH_ART_W4_Arts_Experience_Attend_Analyse_and_Share.html` | Arts Aut 1 | 4/8 | Y | — | **DECISION/QUAR** | SoW-labelled Aut1 8-wk arc (develop→experience→review) vs SoW 7-wk half-terms; QUARANTINED → propose-only; parallel to Launch/ART (canonical?) |
| 23 | Creative Arts | `Art_Teesside/Launch/LAUNCH_ART_W5_Design_the_Leadership_Project.html` | Arts Aut 1 | 5/8 | Y | — | **DECISION/QUAR** | SoW-labelled Aut1 8-wk arc (develop→experience→review) vs SoW 7-wk half-terms; QUARANTINED → propose-only; parallel to Launch/ART (canonical?) |
| 24 | Creative Arts | `Art_Teesside/Launch/LAUNCH_ART_W6_Pilot_Lead_and_Adapt.html` | Arts Aut 1 | 6/8 | Y | — | **DECISION/QUAR** | SoW-labelled Aut1 8-wk arc (develop→experience→review) vs SoW 7-wk half-terms; QUARANTINED → propose-only; parallel to Launch/ART (canonical?) |
| 25 | Creative Arts | `Art_Teesside/Launch/LAUNCH_ART_W7_Deliver_and_Curate_the_Arts_Project.html` | Arts Aut 1 | 7/8 | Y | — | **DECISION/QUAR** | SoW-labelled Aut1 8-wk arc (develop→experience→review) vs SoW 7-wk half-terms; QUARANTINED → propose-only; parallel to Launch/ART (canonical?) |
| 26 | Creative Arts | `Art_Teesside/Launch/LAUNCH_ART_W8_Review_Influence_and_Portfolio_Audit.html` | Arts Aut 1 | 8/8 | Y | — | **DECISION/QUAR** | SoW-labelled Aut1 8-wk arc (develop→experience→review) vs SoW 7-wk half-terms; QUARANTINED → propose-only; parallel to Launch/ART (canonical?) |
| 27 | Humanities | `Humanities_Teesside/LAUNCH_Printable_Pack.html` | — | — | - | UAS | **SOW-SILENT?** | Pack/SoW support doc, not a weekly lesson; parallel to Launch/HUM slides — canonical? (decision) |
| 28 | Humanities | `Humanities_Teesside/LAUNCH_Scheme_of_Work.html` | — | — | - | AQA UAS; UAS | **SOW-SILENT?** | Pack/SoW support doc, not a weekly lesson; parallel to Launch/HUM slides — canonical? (decision) |
| 29 | Science-Bio | `biology/Bio_Respiration_Limewater_Exercise.html` | — | — | - | — | **MAPPING-PENDING** | no self-SoW label; topic (respiration/acids/circuits/waves) = Combined/IGCSE content mapping to SoW Spring/Summer, not Autumn — term/topic mapping unresolved (4c) |
| 30 | Science-Bio | `biology/Chem_Making_Limewater.html` | — | — | - | — | **MAPPING-PENDING** | no self-SoW label; topic (respiration/acids/circuits/waves) = Combined/IGCSE content mapping to SoW Spring/Summer, not Autumn — term/topic mapping unresolved (4c) |
| 31 | Science-Bio | `biology/Digestion_and_Absorption (1).html` | — | — | - | — | **MAPPING-PENDING** | no self-SoW label; topic (respiration/acids/circuits/waves) = Combined/IGCSE content mapping to SoW Spring/Summer, not Autumn — term/topic mapping unresolved (4c) |
| 32 | Science-Bio | `biology/L4_Aerobic.html` | — | — | - | — | **MAPPING-PENDING** | no self-SoW label; topic (respiration/acids/circuits/waves) = Combined/IGCSE content mapping to SoW Spring/Summer, not Autumn — term/topic mapping unresolved (4c) |
| 33 | Science-Bio | `biology/L4_Aerobic_Respiration.html` | — | — | - | — | **MAPPING-PENDING** | no self-SoW label; topic (respiration/acids/circuits/waves) = Combined/IGCSE content mapping to SoW Spring/Summer, not Autumn — term/topic mapping unresolved (4c) |
| 34 | Science-Bio | `biology/L5_Anaerobic.html` | — | — | - | — | **MAPPING-PENDING** | no self-SoW label; topic (respiration/acids/circuits/waves) = Combined/IGCSE content mapping to SoW Spring/Summer, not Autumn — term/topic mapping unresolved (4c) |
| 35 | Science-Bio | `biology/Lesson_2_Absorption_v4-6.html` | — | — | - | — | **MAPPING-PENDING** | no self-SoW label; topic (respiration/acids/circuits/waves) = Combined/IGCSE content mapping to SoW Spring/Summer, not Autumn — term/topic mapping unresolved (4c) |
| 36 | Science-Bio | `biology/Respiration_ATP_Recap.html` | — | — | - | — | **MAPPING-PENDING** | no self-SoW label; topic (respiration/acids/circuits/waves) = Combined/IGCSE content mapping to SoW Spring/Summer, not Autumn — term/topic mapping unresolved (4c) |
| 37 | Science-Bio | `biology/Respiration_and_ATP_Lesson_1.html` | — | — | - | — | **MAPPING-PENDING** | no self-SoW label; topic (respiration/acids/circuits/waves) = Combined/IGCSE content mapping to SoW Spring/Summer, not Autumn — term/topic mapping unresolved (4c) |
| 38 | Science-Bio | `biology/Structure_of_the_Thorax.html` | — | — | - | — | **MAPPING-PENDING** | no self-SoW label; topic (respiration/acids/circuits/waves) = Combined/IGCSE content mapping to SoW Spring/Summer, not Autumn — term/topic mapping unresolved (4c) |
| 39 | Science-Bio | `biology/Testing Breath - FINAL Observation Lesson (1).html` | — | — | - | — | **MAPPING-PENDING** | no self-SoW label; topic (respiration/acids/circuits/waves) = Combined/IGCSE content mapping to SoW Spring/Summer, not Autumn — term/topic mapping unresolved (4c) |
| 40 | Science-Chem | `chemistry/L3c_VirtualLab_AcidsAlkalis (2).html` | — | — | - | — | **MAPPING-PENDING** | no self-SoW label; topic (respiration/acids/circuits/waves) = Combined/IGCSE content mapping to SoW Spring/Summer, not Autumn — term/topic mapping unresolved (4c) |
| 41 | Science-Chem | `chemistry/Lesson1_Indicators-1.html` | — | — | - | — | **MAPPING-PENDING** | no self-SoW label; topic (respiration/acids/circuits/waves) = Combined/IGCSE content mapping to SoW Spring/Summer, not Autumn — term/topic mapping unresolved (4c) |
| 42 | Science-Chem | `chemistry/Lesson2_pH_Scale_v4.html` | — | — | - | Edexcel IGCSE 4SS0 — Spec 2 | **MISALIGNED?** | cites off-map Edexcel IGCSE 4SS0 (N1 exception → DECISION, not auto-fix); no self-SoW label; topic (respiration/acids/circuits/waves) = Combined/IGCSE content mapping to SoW Spring/Summer, not Autumn — term/topic mapping unresolved (4c) |
| 43 | Science-Chem | `chemistry/Lesson3_Ions_Neutralisation_v4.html` | — | — | - | Edexcel IGCSE 4SS0 — Spec 2 | **MISALIGNED?** | cites off-map Edexcel IGCSE 4SS0 (N1 exception → DECISION, not auto-fix); no self-SoW label; topic (respiration/acids/circuits/waves) = Combined/IGCSE content mapping to SoW Spring/Summer, not Autumn — term/topic mapping unresolved (4c) |
| 44 | Science-Chem | `chemistry/Lesson4a_Gas_Tests_H2_O2_CO2 (1).html` | — | — | - | — | **MAPPING-PENDING** | no self-SoW label; topic (respiration/acids/circuits/waves) = Combined/IGCSE content mapping to SoW Spring/Summer, not Autumn — term/topic mapping unresolved (4c) |
| 45 | Science-Chem | `chemistry/Lesson4b_Gas_Tests_NH3_Cl2.html` | — | — | - | — | **MAPPING-PENDING** | no self-SoW label; topic (respiration/acids/circuits/waves) = Combined/IGCSE content mapping to SoW Spring/Summer, not Autumn — term/topic mapping unresolved (4c) |
| 46 | Science-Chem | `chemistry/Lesson5_Flame_Tests.html` | — | — | - | — | **MAPPING-PENDING** | no self-SoW label; topic (respiration/acids/circuits/waves) = Combined/IGCSE content mapping to SoW Spring/Summer, not Autumn — term/topic mapping unresolved (4c) |
| 47 | Science-Chem | `chemistry/Lesson6_Anion_Water_Tests.html` | — | — | - | — | **MAPPING-PENDING** | no self-SoW label; topic (respiration/acids/circuits/waves) = Combined/IGCSE content mapping to SoW Spring/Summer, not Autumn — term/topic mapping unresolved (4c) |
| 48 | Science-Chem | `chemistry/Lesson6b_Consolidation.html` | — | — | - | — | **MAPPING-PENDING** | no self-SoW label; topic (respiration/acids/circuits/waves) = Combined/IGCSE content mapping to SoW Spring/Summer, not Autumn — term/topic mapping unresolved (4c) |
| 49 | Science-Phys | `2 Physics 10/Consolidation_Electricity_Review-1.html` | — | — | - | — | **MAPPING-PENDING** | no self-SoW label; topic (respiration/acids/circuits/waves) = Combined/IGCSE content mapping to SoW Spring/Summer, not Autumn — term/topic mapping unresolved (4c) |
| 50 | Science-Phys | `2 Physics 10/L1_Circuits_Symbols_Series_Parallel-1.html` | — | — | - | — | **MAPPING-PENDING** | no self-SoW label; topic (respiration/acids/circuits/waves) = Combined/IGCSE content mapping to SoW Spring/Summer, not Autumn — term/topic mapping unresolved (4c) |
| 51 | Science-Phys | `2 Physics 10/L2_Voltage_Current_Resistance-1.html` | — | — | - | — | **MAPPING-PENDING** | no self-SoW label; topic (respiration/acids/circuits/waves) = Combined/IGCSE content mapping to SoW Spring/Summer, not Autumn — term/topic mapping unresolved (4c) |
| 52 | Science-Phys | `2 Physics 10/L2_Voltage_Current_Resistance.html` | — | — | - | — | **MAPPING-PENDING** | no self-SoW label; topic (respiration/acids/circuits/waves) = Combined/IGCSE content mapping to SoW Spring/Summer, not Autumn — term/topic mapping unresolved (4c) |
| 53 | Science-Phys | `2 Physics 10/L2b_Ohms_Law_PhET_Practical-1.html` | — | — | - | — | **MAPPING-PENDING** | no self-SoW label; topic (respiration/acids/circuits/waves) = Combined/IGCSE content mapping to SoW Spring/Summer, not Autumn — term/topic mapping unresolved (4c) |
| 54 | Science-Phys | `2 Physics 10/L2b_Ohms_Law_PhET_Practical_1.html` | — | — | - | — | **MAPPING-PENDING** | no self-SoW label; topic (respiration/acids/circuits/waves) = Combined/IGCSE content mapping to SoW Spring/Summer, not Autumn — term/topic mapping unresolved (4c) |
| 55 | Science-Phys | `2 Physics 10/L2c_Ohms_Law_PhET_Take2 (1).html` | — | — | - | — | **MAPPING-PENDING** | no self-SoW label; topic (respiration/acids/circuits/waves) = Combined/IGCSE content mapping to SoW Spring/Summer, not Autumn — term/topic mapping unresolved (4c) |
| 56 | Science-Phys | `2 Physics 10/L3_Ohms_Law_Action.html` | — | — | - | — | **MAPPING-PENDING** | no self-SoW label; topic (respiration/acids/circuits/waves) = Combined/IGCSE content mapping to SoW Spring/Summer, not Autumn — term/topic mapping unresolved (4c) |
| 57 | Science-Phys | `2 Physics 10/L4_Electron_Flow_Series_Calculations.html` | — | — | - | — | **MAPPING-PENDING** | no self-SoW label; topic (respiration/acids/circuits/waves) = Combined/IGCSE content mapping to SoW Spring/Summer, not Autumn — term/topic mapping unresolved (4c) |
| 58 | Science-Phys | `2 Physics 10/L4_Wave_Properties_Definitions-1.html` | — | — | - | — | **MAPPING-PENDING** | no self-SoW label; topic (respiration/acids/circuits/waves) = Combined/IGCSE content mapping to SoW Spring/Summer, not Autumn — term/topic mapping unresolved (4c) |
| 59 | Science-Phys | `2 Physics 10/L4a_Electron_Flow_in_Metals.html` | — | — | - | — | **MAPPING-PENDING** | no self-SoW label; topic (respiration/acids/circuits/waves) = Combined/IGCSE content mapping to SoW Spring/Summer, not Autumn — term/topic mapping unresolved (4c) |
| 60 | Science-Phys | `2 Physics 10/L5_Wave_Speed_Equation-1.html` | — | — | - | — | **MAPPING-PENDING** | no self-SoW label; topic (respiration/acids/circuits/waves) = Combined/IGCSE content mapping to SoW Spring/Summer, not Autumn — term/topic mapping unresolved (4c) |
| 61 | Science-Phys | `2 Physics 10/L6_Waves_Context_Reflection_Refraction-1.html` | — | — | - | — | **MAPPING-PENDING** | no self-SoW label; topic (respiration/acids/circuits/waves) = Combined/IGCSE content mapping to SoW Spring/Summer, not Autumn — term/topic mapping unresolved (4c) |
| 62 | Science-Phys | `2 Physics 10/Waves/L4a_Wave_Anatomy.html` | — | — | - | — | **MAPPING-PENDING** | no self-SoW label; topic (respiration/acids/circuits/waves) = Combined/IGCSE content mapping to SoW Spring/Summer, not Autumn — term/topic mapping unresolved (4c) |
| 63 | Science-Phys | `2 Physics 10/Waves/L4b_Frequency_Period.html` | — | — | - | — | **MAPPING-PENDING** | no self-SoW label; topic (respiration/acids/circuits/waves) = Combined/IGCSE content mapping to SoW Spring/Summer, not Autumn — term/topic mapping unresolved (4c) |
| 64 | Science-Phys | `2 Physics 10/Waves/L4c_Energy_Transfer.html` | — | — | - | — | **MAPPING-PENDING** | no self-SoW label; topic (respiration/acids/circuits/waves) = Combined/IGCSE content mapping to SoW Spring/Summer, not Autumn — term/topic mapping unresolved (4c) |
| 65 | Science-Phys | `2 Physics 10/current_rush.html` | — | — | - | — | **MAPPING-PENDING** | no self-SoW label; topic (respiration/acids/circuits/waves) = Combined/IGCSE content mapping to SoW Spring/Summer, not Autumn — term/topic mapping unresolved (4c) |

### Class tally
- MAPPING-PENDING: 35
- PARTIAL: 9
- DECISION/QUAR: 8
- ALIGNED*: 7
- SOW-SILENT?: 4
- MISALIGNED?: 2
- TOTAL rows: 65

_measured @ 32ca685e1df619b333f3ee4385aed227aa675cdf_

---

# PHASE 2 — post-decision (Matt's calls recorded 2026-07-28)

**Decisions received:** D1 → **`_Teesside/` is canonical** (Launch/ART + Launch/HUM slides = legacy).
D2 → **4SS0 treated as stale, to be fixed** (proposed diff, not auto-committed — N1-flagged).
D3 → **infer science mapping from SoW content** (done below).

## Committable fixes this pass: **ZERO** — and that is the honest headline.
Once the canonical suite is fixed as `_Teesside/`, the alignment work collapses to items that are
each gated, already-done, or a decision:
- **Canonical Humanities (`Humanities_Teesside/`) is ALREADY ALIGNED.** Its SoW self-describes
  "Autumn 1 (8 weeks) · AQA UAS 'History around us' + GCSE AO bridge · LAUNCH tier · Week 7 assessed"
  — consistent with SoW Humanities Aut1 (7-wk History, W7 summative) + a W8 Geography bridge. No
  code defect, correct NC/UAS framing (N1 ✓). **No fix required.**
- **Canonical Art (`Art_Teesside/Launch/`) is QUARANTINED** → propose-only; I cannot write to it
  until Matt lifts the quarantine in writing. It also shows a possible **leadership/careers
  resequencing** in Autumn (W2 Careers, W5 Design-the-Leadership-Project, W6 Pilot/Lead) vs the SoW
  Autumn Creative Arts (Unit 1 "developing as an artist" + "experiencing & reviewing") — a
  DELIBERATE-DIVERGENCE candidate, not an auto-fix. **Needs (a) quarantine lift AND (b) a call on
  the resequencing** before any edit.
- **Legacy suites** (`Launch/ART`, `Launch/HUM`, `Launch/Art_L1/2`): report-only per D1; not aligned.
- **Science:** topic-aligned but carries no SoW week-label / no spec-code — correcting that is a
  Tier-2 content edit AND is blocked on the same code decision as D2. **Held pending code choice.**

## D2 decision pack — 4SS0 replacement (deliver both options, per brief; NOT patched)
Exact strings (each appears once, visible accreditation line):
- `chemistry/Lesson2_pH_Scale_v4.html`: `Edexcel IGCSE 4SS0 — Spec 2.29 & 2.30`
- `chemistry/Lesson3_Ions_Neutralisation_v4.html`: `Edexcel IGCSE 4SS0 — Spec 2.31 & 2.32`

`4SS0` = Edexcel International GCSE **Science (Double Award)** — absent from the SoW Qualification
Map. The map offers two defensible targets; **the spec-point numbers are entangled with the code**,
so neither is a blind string-swap:
- **Option A — `Edexcel GCSE Combined Science 1SC0 (F)`** (the SoW primary LAUNCH route). Cost:
  1SC0 is topic-referenced, not "2.29"-style; the point numbers must be **replaced with the 1SC0
  topic reference**, not kept. Best fit if these lessons are the accessible main-route class.
- **Option B — `Edexcel IGCSE Chemistry 4CH1`** (the SoW separate-science IGCSE stretch). Cost:
  4CH1 uses different section numbering; `2.29–2.32` must be **re-mapped to 4CH1 references** (science
  lead to confirm). Best fit if this is the eligible-students IGCSE stretch class the 4SS0 code implies.
**I will not invent replacement spec-point numbers** (brief: never author accreditation content
loosely). Pick A or B and confirm the point refs, and I'll ship the two-file diff for approval.

## D3 — science → SoW mapping (inferred from topic; report-only)
Physics → SoW **Spring** IGCSE-option (electricity Spr1W6–Spr2W2, waves Spr2W3): 17/17 HIGH.
Chemistry → SoW **Spring** chem (acids/salts Spr1W3 + analysis): HIGH/MED.
Biology → SoW **Summer** (ventilation/exchange Sum1W4 HIGH); **respiration & digestion are NOT
explicit SoW weekly outcomes → SOW-SILENT** (report only, don't delete). Full table:

| File | Inferred SoW target | Week | Conf |
|--|--|--|--|
| `2 Physics 10/Consolidation_Electricity_Review-1.html` | IGCSE-option Phys Spr1 W6–Spr2 W2 'circuits/current/voltage/resistance/power' | Spr Spr1W6-Spr2W2 | HIGH |
| `2 Physics 10/L1_Circuits_Symbols_Series_Parallel-1.html` | IGCSE-option Phys Spr1 W6–Spr2 W2 'circuits/current/voltage/resistance/power' | Spr Spr1W6-Spr2W2 | HIGH |
| `2 Physics 10/L2_Voltage_Current_Resistance-1.html` | IGCSE-option Phys Spr1 W6–Spr2 W2 'circuits/current/voltage/resistance/power' | Spr Spr1W6-Spr2W2 | HIGH |
| `2 Physics 10/L2_Voltage_Current_Resistance.html` | IGCSE-option Phys Spr1 W6–Spr2 W2 'circuits/current/voltage/resistance/power' | Spr Spr1W6-Spr2W2 | HIGH |
| `2 Physics 10/L2b_Ohms_Law_PhET_Practical-1.html` | IGCSE-option Phys Spr1 W6–Spr2 W2 'circuits/current/voltage/resistance/power' | Spr Spr1W6-Spr2W2 | HIGH |
| `2 Physics 10/L2b_Ohms_Law_PhET_Practical_1.html` | IGCSE-option Phys Spr1 W6–Spr2 W2 'circuits/current/voltage/resistance/power' | Spr Spr1W6-Spr2W2 | HIGH |
| `2 Physics 10/L2c_Ohms_Law_PhET_Take2 (1).html` | IGCSE-option Phys Spr1 W6–Spr2 W2 'circuits/current/voltage/resistance/power' | Spr Spr1W6-Spr2W2 | HIGH |
| `2 Physics 10/L3_Ohms_Law_Action.html` | IGCSE-option Phys Spr1 W6–Spr2 W2 'circuits/current/voltage/resistance/power' | Spr Spr1W6-Spr2W2 | HIGH |
| `2 Physics 10/L4_Electron_Flow_Series_Calculations.html` | IGCSE-option Phys Spr1 W6–Spr2 W2 'circuits/current/voltage/resistance/power' | Spr Spr1W6-Spr2W2 | HIGH |
| `2 Physics 10/L4_Wave_Properties_Definitions-1.html` | IGCSE-option Phys Spr2 W3 'waves – properties, reflection & refraction' | Spr Spr2 W3 | HIGH |
| `2 Physics 10/L4a_Electron_Flow_in_Metals.html` | IGCSE-option Phys Spr1 W6–Spr2 W2 'circuits/current/voltage/resistance/power' | Spr Spr1W6-Spr2W2 | HIGH |
| `2 Physics 10/L5_Wave_Speed_Equation-1.html` | IGCSE-option Phys Spr2 W3 'waves – properties, reflection & refraction' | Spr Spr2 W3 | HIGH |
| `2 Physics 10/L6_Waves_Context_Reflection_Refraction-1.html` | IGCSE-option Phys Spr2 W3 'waves – properties, reflection & refraction' | Spr Spr2 W3 | HIGH |
| `2 Physics 10/Waves/L4a_Wave_Anatomy.html` | IGCSE-option Phys Spr2 W3 'waves – properties, reflection & refraction' | Spr Spr2 W3 | HIGH |
| `2 Physics 10/Waves/L4b_Frequency_Period.html` | IGCSE-option Phys Spr2 W3 'waves – properties, reflection & refraction' | Spr Spr2 W3 | HIGH |
| `2 Physics 10/Waves/L4c_Energy_Transfer.html` | IGCSE-option Phys Spr2 W3 'waves – properties, reflection & refraction' | Spr Spr2 W3 | HIGH |
| `2 Physics 10/current_rush.html` | IGCSE-option Phys Spr1 W6–Spr2 W2 'circuits/current/voltage/resistance/power' | Spr Spr1W6-Spr2W2 | HIGH |
| `biology/Bio_Respiration_Limewater_Exercise.html` | GCSE Bio Sum1 W4 'exchange surfaces & ventilation' | Sum Sum1 W4 | HIGH |
| `biology/Chem_Making_Limewater.html` | GCSE Bio ~Sum1 (exchange/transport region); respiration NOT an explicit SoW week | Sum1 W3-5 / SOW-SILENT? | MED |
| `biology/Digestion_and_Absorption (1).html` | GCSE Bio — digestion/enzymes not an explicit SoW weekly outcome | (no direct week) | LOW |
| `biology/L4_Aerobic.html` | GCSE Bio ~Sum1 (exchange/transport region); respiration NOT an explicit SoW week | Sum1 W3-5 / SOW-SILENT? | MED |
| `biology/L4_Aerobic_Respiration.html` | GCSE Bio ~Sum1 (exchange/transport region); respiration NOT an explicit SoW week | Sum1 W3-5 / SOW-SILENT? | MED |
| `biology/L5_Anaerobic.html` | GCSE Bio ~Sum1 (exchange/transport region); respiration NOT an explicit SoW week | Sum1 W3-5 / SOW-SILENT? | MED |
| `biology/Lesson_2_Absorption_v4-6.html` | GCSE Bio — digestion/enzymes not an explicit SoW weekly outcome | (no direct week) | LOW |
| `biology/Respiration_ATP_Recap.html` | GCSE Bio ~Sum1 (exchange/transport region); respiration NOT an explicit SoW week | Sum1 W3-5 / SOW-SILENT? | MED |
| `biology/Respiration_and_ATP_Lesson_1.html` | GCSE Bio ~Sum1 (exchange/transport region); respiration NOT an explicit SoW week | Sum1 W3-5 / SOW-SILENT? | MED |
| `biology/Structure_of_the_Thorax.html` | GCSE Bio Sum1 W4 'exchange surfaces & ventilation' | Sum Sum1 W4 | HIGH |
| `biology/Testing Breath - FINAL Observation Lesson (1).html` | GCSE Bio ~Sum1 (exchange/transport region); respiration NOT an explicit SoW week | Sum1 W3-5 / SOW-SILENT? | MED |
| `chemistry/L3c_VirtualLab_AcidsAlkalis (2).html` | IGCSE-option Chem Spr1 W3 'acids, bases and preparing salts' | Spr Spr1 W3 | HIGH |
| `chemistry/Lesson1_Indicators-1.html` | IGCSE-option Chem Spr1 W3 'acids, bases and preparing salts' | Spr Spr1 W3 | HIGH |
| `chemistry/Lesson2_pH_Scale_v4.html` | IGCSE-option Chem Spr1 W3 'acids, bases and preparing salts' | Spr Spr1 W3 | HIGH |
| `chemistry/Lesson3_Ions_Neutralisation_v4.html` | IGCSE-option Chem Spr1 W3 'acids, bases and preparing salts' | Spr Spr1 W3 | HIGH |
| `chemistry/Lesson4a_Gas_Tests_H2_O2_CO2 (1).html` | GCSE Bio ~Sum1 (exchange/transport region); respiration NOT an explicit SoW week | Sum1 W3-5 / SOW-SILENT? | MED |
| `chemistry/Lesson4b_Gas_Tests_NH3_Cl2.html` | IGCSE-option Chem Spr1 W3 'acids, bases and preparing salts' | Spr Spr1 W3 | HIGH |
| `chemistry/Lesson5_Flame_Tests.html` | Chem qualitative analysis (flame/gas/anion) — Combined/IGCSE analysis, ~Spring chem | Spr chem (analysis) | MED |
| `chemistry/Lesson6_Anion_Water_Tests.html` | IGCSE-option Chem Spr1 W3 'acids, bases and preparing salts' | Spr Spr1 W3 | HIGH |
| `chemistry/Lesson6b_Consolidation.html` | Chem qualitative analysis (flame/gas/anion) — Combined/IGCSE analysis, ~Spring chem | Spr chem (analysis) | MED |

Confidence tally: {'HIGH': 25, 'MED': 10, 'LOW': 2} of 37 files

_measured @ 32ca685e1df619b333f3ee4385aed227aa675cdf · Phase 2 decisions 2026-07-28_

---

# PHASE 2 — FINAL (decisions 2: quarantine lift + 4SS0 park, 2026-07-28)

**Decisions:** Art_Teesside quarantine **LIFTED in writing** (writes now permitted); 4SS0 **PARKED**
(no chemistry-code action this pass).

## Canonical Art (`Art_Teesside/Launch`) — assessed WITH quarantine lifted → still NO auto-fix
Even able to write, the correct action is to table, not adapt. The suite is a **coherent designed
divergence**, not a misalignment:
- Week arc: W1 Frame the Local Challenge · W2 Practice Careers & Pathways · W3 Implement & Critically
  Develop · W4 Arts Experience (Attend/Analyse/Share) · W5 Design the Leadership Project · W6 Pilot,
  Lead & Adapt · W7 Deliver & Curate · W8 Review, Influence & Portfolio Audit.
- Maps partly to SoW Autumn Creative Arts (W3≈"developing as an artist"; W4≈"experiencing the arts";
  W8≈"review") but **W1/W2/W5/W6 are an intentional Arts-Award leadership/project blend** (Silver
  Unit 2 / Gold), coherently sequenced, Trinity Silver/Gold cited correctly (N1 ✓), structure healthy
  (9 slides · 7 lundy-box · 16 print ids · reduced-motion present · no ll-g sentinel).
- Per brief §2.3 / Tier-3: a coherent alternative sequence is a **DECISION ITEM for Matt, never an
  auto-fix**. Rewriting it to the SoW's "identity/developing-artist" Autumn theme (N3) would destroy
  a designed arc and revert a decision. **Tabled. No edit made.** (Quarantine lift used only to READ
  and confirm; nothing written.)

## FINAL committable-fix tally this pass: **0 lesson files changed.**
- Canonical Humanities: already aligned.
- Canonical Art: designed divergence → decision item (not a fix).
- Science: topic-aligned; spec-code/week-label correction blocked on the **parked** 4SS0 decision.
- 4SS0: parked by Matt.
- Legacy suites: report-only.

## What waits on Matt
1. **Art_Teesside leadership resequencing** — accept as designed (close the item) OR ask for a
   re-alignment to SoW Autumn Creative Arts (then it becomes a scoped Tier-2 job).
2. **4SS0 code** (parked) — pick 1SC0 vs 4CH1 + confirm spec-point refs to unlock the 2-file diff
   and the wider science spec-code/week-label alignment.
3. **Merge** — review branch `pass-sl-sow-launch` and run your spot-checks. Nothing merged by me.

_measured @ 32ca685e1df619b333f3ee4385aed227aa675cdf · Phase 2 final 2026-07-28_

---

# RULINGS FROM MATT (2026-07-28) — recorded verbatim for successor sessions

**Premise corrections ADOPTED (now govern, not the brief):**
- SoW weekly grid is **Autumn 7/7 · Spring 6/6 · Summer 6/7** (my derivation governs; brief's uniform W1–W7 retires).
- **No root-`LAUNCH_` files** exist; population is folder-scoped.
- **`resources.json` lives in THIS repo too** — any catalogue correction is in-repo, one class per commit; the brief's "site-repo read-only" line applies to the *site* repo's own copy only.

## RULING 1 — SCIENCE FROZEN (all 37 files, both directions)
The `biology/` `chemistry/` `2 Physics 10/` suites are **last year's provision (2025-26)**. This
year's LAUNCH science is being built fresh & externally (PythonAnywhere-assessed). The 2026-27 SoW
does **not** govern them and they need not match it.
- **4SS0 decision pack → RETIRED-UNANSWERED.** No 2-file diff, no wider science spec-code/week-label
  alignment. Question no longer applies to live provision.
- **All 37 science verdict rows RECLASSIFIED → `OUT-OF-SCOPE — LEGACY PROVISION (2025-26)`**
  (superseded by the 2026-27 science rebuild, external/PythonAnywhere-assessed). Rows & the
  Phys→Spring / Chem→Spring / Bio→Summer mapping are **kept as archival record**; their fix classes retire.
- **SOW-SILENT respiration/digestion finding RETIRES** — it compared a legacy suite to a SoW that
  doesn't govern it.
- **STANDING NO-TOUCH (binds this pass + successors):** no Pass SL commit touches any file under the
  science folders in either direction (no fixes, no label sweeps, no "harmless" string edits). Any
  future class that would sweep those folders **excludes them in its manifest and asserts the exclusion**.

## RULING 2 — ART_TEESSIDE/LAUNCH RE-ALIGNMENT AUTHORISED (Tier-2, gated)
Designed-divergence resolves to: **re-align to the SoW Autumn arc, hard-gated on Trinity Silver
coverage surviving intact.** Quarantine LIFTED. Gates **G1–G6** (nine-part floor with hyphen-range-aware
detector; Unit-1=art-form / Unit-2=leadership boundary; hard prohibitions — no public-showing assertion,
no hours/TQT, no mark schemes; Pass C survivors preserved; four-surface agreement; standard estate gates).
**Design-first:** deliver a mapping proposal → Matt approves/amends → build. **Silver wins** any genuine
SoW↔Silver conflict, returned as a decision. Proposal delivered: `_passsl/ART_REALIGN_PROPOSAL.md`.

_measured @ 32ca685e1df619b333f3ee4385aed227aa675cdf · rulings 2026-07-28_

---

# PHASE 2 — ART BUILD COMPLETE (Option A, quarantine lifted; 2026-07-28)

Mapping proposal approved (Option A; Unit 2 stays in Autumn — accepted divergence). Built on branch,
one class per commit, gates run per file. **7 lesson files changed; surfaces needed no change.**

## Commits (rollback bases named)
| Class | Commit | Files | What |
|--|--|--|--|
| Vocab (N4) | `5b88c23` | W1, W4 | Missing SoW Autumn vocab added to existing KO tables (taught, w/ defs): W1 (Aut1) art form·identity·reflection; W4 (Aut2) critique·inspiration·research |
| Label (SoW provenance) | `dffeca9` | W4–W8 | W4 Aut1→Aut2; W5–W8 Aut1→"Unit 2 · SoW Spring/Summer" |
| Label (cont.) | `301acb9` | W2 | W2 (Silver 1D research-artist) Aut1→Aut2 — completes scheme |
| Surfaces (G5) | — (no-op) | — | START_HERE / Scheme_of_Work / Printable pack already Unit-1/Unit-2 framed and enforce the art-form/leadership boundary themselves; no SURFACE-SPLIT created, no edit needed |

**Final SoW-provenance scheme:** W1/W3 = Aut 1 (1A/1B develop-as-artist) · W2/W4 = Aut 2 (1D/1C
experience-review) · W5–W8 = Unit 2 · SoW Spring/Summer (leadership, taught early). Delivery "Week N" unchanged.

## Gate results (measured post-build)
- **G1 nine-part floor:** 1A–1D, 2A–2E all present across the suite ✓ (hyphen-range-aware detector; self-test passed).
- **G2 Unit boundary:** untouched; the pack's WEEKS[] generator itself enforces "Unit 1 = art form, not leadership".
- **G3 prohibitions:** public-showing assertions = 0 (5 guardrails preserved, all "Gold-only, not required at Silver"); no hours/TQT; no mark schemes authored.
- **G4 Pass C survivors:** W1 shrink-line, W2 artist+organisation evidence, W5 crew cards, print-pack authorship/support splits all intact (added-only + label edits; nothing relocated or deleted).
- **G5 four-surface agreement:** surfaces already consistent; no split.
- **G6 estate gates (per file, per commit):** slide / .lundy-box / print-id / ko-table counts unchanged; reduced-motion @media block byte-identical; `node --check` 0 failures across inline scripts; stale "Arts Aut 1" asserted gone from every relabelled file; cardinality asserted per commit; no `ll-g` sentinel in touched files.
- **N4 vocab:** all 11 SoW Aut1+Aut2 Creative-Arts vocab terms now present across W1–W4 (MISSING: none).

## Honest headline for the Art job
The canonical suite was already ~90% SoW-aligned (correct Silver 9-part coverage, art-form/leadership
boundary already enforced, accreditation correct). The build was a **light-touch N3/N4 + provenance-label
pass — 6 vocab terms and 6 label corrections across 7 files — not a resequence.** No lesson task chain
rewritten; no structure touched. Nothing merged — Matt merges.

_measured @ 32ca685e1df619b333f3ee4385aed227aa675cdf · Art build 2026-07-28_

---

# FINAL — FROZEN RECORD (verbatim-checkable · session close-out 2026-07-29)

**Status: PARKED UNMERGED. Do NOT merge.** Merge belongs to the scheduled single sitting on
**29 August**, order **SL → SBX → PQ → SG**. This section supersedes any earlier line implying merge-now.

- **Base:** `32ca685e1df619b333f3ee4385aed227aa675cdf`
- **Branch:** `pass-sl-sow-launch` — **12 commits total** = 11 work commits (`40a0637`…`54aec9c`) + this handover commit (12th).
- **Build SHAs:** vocab `5b88c23` · provenance labels `dffeca9` + `301acb9`.
- **Final SoW-provenance scheme (Art_Teesside/Launch):** W1/W3 = **Aut 1** (1A/1B develop-as-artist) ·
  W2/W4 = **Aut 2** (1D/1C experience-review) · W5–W8 = **Unit 2 · SoW Spring/Summer, taught early**
  (accepted divergence — Silver-wins; Unit 2 stays in the Autumn vehicle until Spring/Summer Art suites exist).
- **Gates measured green post-build:** G1 nine-part 1A–1D,2A–2E ALL PRESENT (hyphen-range detector, self-test passed) ·
  G2 art-form/leadership boundary untouched (pack generator enforces it) · G3 public-showing assertions **0**
  (5 guardrails preserved), no hours/TQT, no mark schemes · G4 Pass C survivors intact (W1 shrink, W2 artist+organisation,
  W5 crew cards, print authorship/support splits) · G5 four surfaces agree (no split) · G6 per-file per-commit:
  slide/.lundy-box/print-id/ko-table counts unchanged, reduced-motion @media byte-identical, `node --check` 0 failures,
  stale "Arts Aut 1" asserted gone from relabelled files, cardinality asserted · **N4: all 11 SoW Autumn Creative-Arts
  vocab terms present across W1–W4, MISSING none.**

## RULING 1 (frozen) — science
- **All 37 science rows → `OUT-OF-SCOPE — LEGACY PROVISION (2025-26)`** (external 2026-27 rebuild, PythonAnywhere-assessed).
- **4SS0 decision pack → RETIRED-UNANSWERED** (no longer applies to live provision).
- **STANDING NO-TOUCH on the science folders** (`biology/`, `chemistry/`, `2 Physics 10/`) — no Pass SL commit
  touches them in either direction; any future class that would sweep them excludes them and asserts the exclusion.

## WHERE THE SCIENCE NO-TOUCH LIVES (successor-critical)
1. **`_passsl/FINDINGS.md`** — RULING 1 section above and the earlier "RULINGS FROM MATT" section.
2. **`_passsl/HANDOVER.md`** — restated in the parked-branch handover.
3. **NOT yet in `REGISTER.md`** (the estate standing-rules file successors actually read: *"Load this before any
   pass that measures, patches or deletes"*). `REGISTER.md` is **main-owned and has advanced past this branch's base
   (`32ca685` → `59ad56a`)**; editing it from this parked branch would violate the coexistence freeze (it is not one
   of this branch's changed paths). **ACTION FOR THE 29 AUG MERGE SITTING:** transcribe the science no-touch into
   `REGISTER.md` at merge time, since a successor pass that never reads this branch will only hit it there.

## COEXISTENCE AT CLOSE (fetched @ origin/main `59ad56a82e4c0c297910fe61df45129bbd231bc9`)
origin/main advanced `32ca685`→`59ad56a` (74 paths). **Overlap with this branch's changed paths (7 Art files + `_passsl/`)
= EMPTY** — DISJOINT, no textual conflict. Note: main separately modified `Art_Teesside/Launch/LAUNCH_ART_W3_*` and
`Art_Teesside/Launch/Printable_LAUNCH_Evidence_and_Lundy_Pack.html` (files this branch did NOT change) — no conflict,
but the merge sitting should re-verify the W1–W8 + pack provenance scheme is still coherent after main's W3/pack edits.

_measured @ 32ca685e1df619b333f3ee4385aed227aa675cdf · frozen 2026-07-29_
