# Pass SB — BUILD lessons ⇄ BUILD SoW 2026-27 audit

**Status:** MEASUREMENT COMPLETE · awaiting Matt on Gate 1 & Gate 2. 0 lesson files modified. Nothing merged. Matt merges.

## Lineage & provenance

| Field | Value |
|---|---|
| Pass letter | **SB** (no `_passsb/` or prior Pass SB ledger existed at base — letter stands, no self-rename needed) |
| Sibling pass | **Pass SL** (LAUNCH lessons ⇄ LAUNCH SoW) — this is the BUILD sibling |
| Repo | `MattRoper1977/Lessons` (the Lessons repo — **not** the site repo `mattroper1977.github.io`) |
| Base SHA (pinned) | `32ca685e1df619b333f3ee4385aed227aa675cdf` (origin/main @ session start) |
| Base commit | `LL-I close (final): commit the measurement records + remedy-observed line` (2026-07-28 18:27:26 +0000) |
| Branch | `pass-sb-sow-build` (off origin/main) |
| Branch tip | close-out content commit `45b83ed` (derived via `git rev-parse`); this pointer commit is its child |
| SoW instrument | `Build SOW 2026-2027.xlsx`, sha256 `730f9a86a105a50fae64cc3560deb33a8f78f8a15959c608fa0c9fc197ce5bac`, committed at `_passsb/inputs/` |
| Instrument provenance | Supplied by Matt as attachment `Scheme_of_Work_20262027_Build.zip` during session. **Not** the archived `BUILD_SOW_2026-27_vA_with_LivingIndependently.xlsx` (Version A, superseded). |

## Brief-verification log (Ground Rule 3 — repo wins, mismatches reported)

1. **Working tree:** brief warns three prior sessions ran in the site repo. First act verified this is the Lessons repo (`resources.json`, `BUILD_ASDAN/`, `Art_Teesside/`, `DT_Community_Upcycling/`, `Humanities_Teesside/`, `build-engine/` all present). ✔
2. **Branch name:** brief §0.1 says branch `pass-sb-sow-build`; the harness "Git Development Branch Requirements" name `claude/pass-sb-build-sow-audit-fqb5qb` — but that requirement is scoped to the *site* repo. For the Lessons repo the brief's name governs. Branch created as **`pass-sb-sow-build`**.
3. **SoW instrument absent from repo:** the exact `Build SOW 2026-2027.xlsx` named in the brief was **not** committed to the repo. The only BUILD SoW workbook on disk was the archived **Version A** (`Build/_Archive_VersionA_LivingIndependently/…vA_with_LivingIndependently.xlsx`), explicitly superseded per `Build/_Archive…/README.md` ("Decision July 2026: Build runs the FoodWise-only pathway (Version B)"). Matt supplied the live vB instrument as an attachment; audit binds to that. vB structure (11 sheets, weekly sheets shorter than vA) is consistent with the LI strand dropped.
4. _(further mismatches appended as measurement proceeds)_

## Phase 1 — SoW target matrix
_Pending → see `_passsb/SOW_MATRIX.md`._

## Phase 2 — BUILD population & strand→suite mapping

### 2.1 Population derivation (unit = **lessons**, scope = BUILD-labelled decks at base `32ca685e`)

Derived mechanically from folder/filename patterns **and** `resources.json`, excluding scaffolds
(`START_HERE`, `*_Hub`, `Scheme_of_Work`, `Resources_and_Tools`, `*Evidence_Pack`, `*Run_Sheets`).

| Suite | Location | Lessons | In resources.json |
|---|---|---:|---|
| ASDAN · Careers | `BUILD_ASDAN/Careers/` | 7 | 7/7 |
| ASDAN · Living Independently | `BUILD_ASDAN/Living_Independently/` | 6 | 6/6 |
| ASDAN · FoodWise | `BUILD_ASDAN/FoodWise/` | 6 | 6/6 |
| ASDAN · Community Project | `BUILD_ASDAN/Community_Project/` | 6 | 6/6 |
| ASDAN · Duke & Enterprise | `BUILD_ASDAN/Duke_and_Enterprise/` | 6 | 6/6 |
| **ASDAN subtotal** | | **31** | 31/31 |
| D&T (v5) | `Build/Slideshows/BUILD_DT_W1–6` | 6 | 6/6 |
| Humanities | `Build/Slideshows/BUILD_HUM_W1–8` | 8 | 8/8 |
| **`Build` subtotal** | | **14** | 14/14 |
| Art Teesside · main route | `Art_Teesside/Build/BUILD_ART_W1–8` | 8 | 8/8 |
| Art Teesside · Autumn-2 route | `Art_Teesside/Build/BUILD_ART_A2_W1–7` | 7 | 5/7 |
| **Art Teesside subtotal** | | **15** | 13/15 |
| **TOTAL BUILD population** | | **60** | 58/60 |

### 2.2 Three-way reconciliation (all agree on 60; breakdowns differ)

| Source | BUILD count | Breakdown | Measured @ |
|---|---:|---|---|
| This pass (mechanical) | **60** | ASDAN 31 · `Build` 14 · Art_Teesside/Build 15 | `32ca685e` (base) |
| REGISTER **R-A02** (LL-3-lacking population) | **60** | `BUILD_ASDAN` 31 · `Art_Teesside/Build` 15 · `Build` 14 | `7226b08` |
| Brief's cited T-audit verdict table | **60** | (not itemised in brief) | `7889055a` |
| Brief §2 *expected membership* | **53** stated + "whatever else" | ASDAN 31 · DT 6 · HUM 8 · **Art ×8** | — (a claim, not a measurement) |

**Delta tabled (Ground Rule 3):** the brief §2 says "Art Teesside BUILD route **×8**". The repo has **15**
(main `BUILD_ART_W1–8` = 8 **plus** the Autumn-2 route `BUILD_ART_A2_W1–7` = 7). The brief omitted the
A2 route. REGISTER R-A02 and my derivation both agree on 15. **Repo wins: Art Teesside BUILD = 15.**
Brief §2 ASDAN sub-breakdown (Careers ×7, LI ×6, FoodWise ×6, Community ×6, Duke&Ent ×6 = 31) matches exactly.
Brief §2 "BUILD_DT ×6 (now v5)" confirmed — all six decks carry `v5`/`V5` markers and `printPack` lists.

### 2.3 Excluded / out-of-population (report-only)

- **LEGACY art (excluded by standing decision):** `Build/Slideshows/BUILD_ART_W1–8` (8 files, "Technique_Tasters"
  family). Present in `resources.json` but **measured: nothing** (brief §2). Distinct from the live
  `Art_Teesside/Build/BUILD_ART_W1–8` route (different titles: "The_Local_Canvas" etc.).
- **Orphaned vB sample lessons (7):** `Build/Slideshows/BUILD_L1_{Careers_Strengths, CommunityA_Explore,
  CommunityB_Duke_Launch, FW_Practical_Hygiene_FruitPot, LI_Where_Money_Comes_From, Vocational_Kitchen_Induction}`
  + `FW_L1_Food_Groups`. **Not** in `resources.json`, **not** referenced by `index.html`/`sitemap.xml`, **not** in
  REGISTER's 60. These are single-lesson vB taster samples superseded by the full `BUILD_ASDAN` suites
  (`BUILD_L1_LI_Where_Money_Comes_From` duplicates `BUILD_ASDAN/Living_Independently/LI_W1`). Out of the measured
  population; listed as SOW-SILENT(a)/superseded. **No measurement, no fix** — flagged for Matt (delete-vs-keep is his call).
- **resources.json catalogue gaps (2):** `Art_Teesside/Build/BUILD_ART_A2_W3_Stencil_Lab.html` and
  `…A2_W4_Audience_Week.html` are on disk and in the population but **absent from `resources.json`**. These sit
  under Art_Teesside **patch quarantine** (§5) → recorded as a proposed catalogue addition in FINDINGS only, no commit.
- **Companions (not lessons, used for print/screen parity in Phase 3):** `Humanities_Teesside/BUILD_{Scheme_of_Work,
  Printable_Pack}` + `Pathway_Tracker` (for BUILD_HUM); `DT_Community_Upcycling/{Scheme_of_Work, Weekly_Plan}` (for
  BUILD_DT); `Art_Teesside/Build/{Printable_BUILD_Weekly_Evidence_Pack, Autumn2_*, Spring1_*, Scheme_of_Work}` (for Art);
  `BUILD_ASDAN/{Scheme_of_Work, BUILD_ASDAN_Hub}` + per-slot `START_HERE` (for ASDAN).

### 2.4 Strand → suite mapping (**a finding, not an assumption** — brief §3)

SoW weekly strand (14) → estate BUILD suite. **6** SoW strands (#4, 9, 11, 12, 13, 14) carry BUILD lessons in this
repo; the other **8** are **SOW-SILENT(b)** (taught by colleagues from other resources — an empty strand is not a defect).

| # | SoW weekly strand | Estate BUILD suite(s) | Lessons | Notes / wrinkle resolved |
|---|---|---|---:|---|
| 1 | Communication & Literacy | — | 0 | SOW-SILENT(b) |
| 2 | Numeracy | — | 0 | SOW-SILENT(b) |
| 3 | Science | — | 0 | SOW-SILENT(b) |
| 4 | World About Me (Humanities) | `Build/BUILD_HUM_W1–8` | 8 | + `Humanities_Teesside/BUILD_*` companions |
| 5 | RE & World Views | — | 0 | SOW-SILENT(b) |
| 6 | PSHE & Citizenship | — | 0 | SOW-SILENT(b) |
| 7 | RSHE | — | 0 | SOW-SILENT(b) (ASDAN Consent packs are not BUILD-labelled) |
| 8 | Computing & ICT | — | 0 | SOW-SILENT(b) |
| 9 | Creative Arts (Trinity **Discover**) | `Art_Teesside/Build` (×15) | 15 | **Gate 2(a):** estate route built as **Explore**; weekly-prog names **Discover** |
| 10 | PE | — | 0 | SOW-SILENT(b) |
| 11 | PfA: Independent Living, Careers & Vocational | ASDAN Careers ×7 + Living Independently ×6 (+ FoodWise ×6, shared) | 13 (+6) | **LI wrinkle:** Ladder R14 dropped LI, weekly strand 11 name+prog retains "ASDAN Living Independently" → LI ×6 map here |
| 12 | Enrichment Award: Junior/Young Duke | ASDAN Duke & Enterprise ×6 | 6 | "Duke & Enterprise" slot = SoW's Junior/Young Duke strand |
| 13 | Design & Technology (Foodwise/Textiles/Construction) | `Build/BUILD_DT_W1–6` + FoodWise ×6 (shared) | 6 (+6) | **D&T wrinkle:** estate "D&T Community Upcycling" arc (Workshop_Audit→Handover) = SoW Construction/Textiles taster; `DT_Community_Upcycling/` holds its scheme+plan |
| 14 | Community Project & Vocational (flexible) | ASDAN Community Project ×6 | 6 | GCOMM/Community arc = SoW strand 14 |

**Dual-home (tabled, not forced):** FoodWise ×6 satisfies BOTH strand 13 (D&T · Foodwise component) and strand 11
(PfA weekly "Foodwise snack"); the SoW itself dual-references it. Primary mapping = **strand 13 (D&T)**; secondary = strand 11.
Sum of lessons across suites = 8 (HUM) + 15 (Art) + 7+6+6 (Careers/LI/FoodWise) + 6 (Duke) + 6 (DT) + 6 (Community) = **60**. ✔

## Phase 3 — Per-lesson classification table

Every surface was extracted mechanically (title · `<h1>` · slide-tag week line · `.sow-strip` · `.award-strip`
· `.sc-v4` Success-looks-like · printPack tiers · KO · exit · reduced-motion · div/script balance). Comparison is
against the mapped SoW cell(s) via the §2.4 strand→suite map. **Unit = lessons.**

### 3.1 Classification summary (unit = lessons, scope = 60 BUILD lessons @ base `32ca685e`)

| Class | Count | Lessons |
|---|---:|---|
| **ALIGNED** (LO-level; term/week placement tabled as Gate 1) | **43** | Careers W1–W5 (5) · LI ×6 · FoodWise ×6 · Community ×6 · Duke ×6 · DT ×6 · Art-main W1–W8 (8) |
| **DELIBERATE-DIVERGENCE** (§4 protected) | **2** | Careers W6, W7 (Pass H swap) |
| **PARTIAL** (pitch/content divergence vs mapped strand) | **8** | Humanities W1–W8 |
| **SURFACE-SPLIT** (screen surfaces disagree; Art quarantine) | **7** | Art A2 W1–W7 |
| **MISALIGNED** | 0 | — |
| **SOW-SILENT** | 0 in-population | (both directions listed separately below — all report-only) |
| **TOTAL** | **60** | |

### 3.2 Per-suite classification (SoW cell + lesson surface cited)

**Careers ×7 → SoW strand 11 "PfA: Independent Living, Careers & Vocational" (weekly Spr1·W1, Spr2·W1–W6 "careers"; half-term R19; Ladder R14).**
- W1–W5 **ALIGNED**: SC (`.sc-v4`) map to strand-11 careers LOs (strengths→jobs→skills→routines→applying). *Surface:* weektag "Week n of 6", sow-strip "Aut 1 · Careers & Work slot · Week n", award "Banks: ASDAN LI M8 / AQA UAS". **Placement (Aut 1) diverges from SoW's Spring careers weeks → Gate 1.** **Week-count "of 6" is stale (suite is 7; W6/W7 say "of 7") → Gate 1 (entangled with the protected Pass H swap; not auto-fixed).**
- W6 (`CAREERS_W6_My_Career_Profile.html`) & W7 (`CAREERS_W7_After_Year_11.html`) **DELIBERATE-DIVERGENCE** (§4 Pass H swap): each presents internally swapped (file-W6→"Week 7 · My Career Profile"; file-W7→"Week 6 · What Happens After Year 11"). Title/weektag/sow-strip agree *within each file*. Post-16 facts in W7-file verified — **not re-derived**.

**Living Independently ×6 → SoW strand 11 (weekly prog "ASDAN Living Independently"; Spr1·W1–W6; half-term R19). ALIGNED.**
- SC map to money/independence LOs (money sources→coins→needs/wants→prices→budget→shopping); award "ASDAN LI M1". Internally consistent ("Week n of 6"). §4 LI_W1 "family finances" line **present, untouched**; money is practice money.
- **SoW-internal inconsistency (report-only):** Ladder R14 BUILD dropped LI ("Foodwise/Gardening taster"); weekly strand 11 name+prog retains it. LI decks classified ALIGNED **to the weekly strand**; the Ladder headline is a SoW-internal defect, not a lesson defect. Placement (Aut 1) → Gate 1.

**FoodWise ×6 → SoW strand 13 "D&T (Foodwise/Textiles/Construction)" (Aut1·W1–W4 FOODWISE; half-term R20) + strand 11 (dual). ALIGNED.**
- SC map to food-groups→balanced-plate→labels→hygiene→snack→meal. §4 Eatwell framing intact; FW_W2 "the calories, or something else?" line **present, untouched**; **no calorie/weight/restriction language introduced**. Placement → Gate 1.

**Community Project ×6 → SoW strand 14 "Community Project & Vocational (flexible)" (Aut1·W1–W7; half-term R22). ALIGNED.**
- SC map to choose-asset→need→roles→partner-update→plan-handover→handover. Award "ASDAN/UAS community evidence · links D&T Slot 2". Internally consistent. Placement → Gate 1.

**Duke & Enterprise ×6 → SoW strand 12 "Enrichment Award: Junior/Young Duke" (Aut1·W1–W7; Programmes R6). ALIGNED.**
- SC map to choose-challenges→kindness→eco→independence→social-enterprise→pitch. Award "AQA UAS 'Personal challenge'" — **matches** SoW strand-12 acc exactly. **No PEQ claim → Gate 2(c) clear.** Placement → Gate 1.

**D&T (Community Upcycling) ×6 → SoW strand 13 (Construction component: Aut2·W1–W4; half-term R21). ALIGNED. — §5 QUARANTINE (v5 decks).**
- SC map to workshop-audit→blueprint→core-cut→assembly→finish→handover = SoW Construction LOs (materials/tools/safety→mark-out→make→test/evaluate). Award "ASDAN Vocational / D&T module evidence". **Read & classified only; no printPack id changes, no Lundy-print edits.** Estate concentrates Construction as a 6-week arc at "Aut 1" vs SoW's Aut2 construction weeks → Gate 1.

**Humanities ×8 → SoW strand 4 "World About Me (Humanities)" (Aut1·W1–W7; half-term R10; Ladder R7; QualMap R11). PARTIAL.**
- Estate BUILD_HUM is a **Teesside local-history disciplinary-enquiry** arc (timeline/centuries→sources→migration causation→significance→historical account→mapping). SoW **weekly strand 4** is pitched at **"World About Me" NC-KS1** (family/people-who-help/festivals/then-&-now). *Divergence:* pitch (KS2/3 disciplinary vs KS1 enquiry) and content (migration history vs family/festivals). *Aligns* to Ladder R7 "Kapow History" and QualMap R11 "substantive knowledge, disciplinary skills" — so the estate realises the **Kapow-History** intent the weekly strand under-specifies. Theme (Identity & Belonging / migration / belonging) **matches**. → **Tier 3 report-only** (curriculum-pitch decision for Matt: is BUILD Humanities "World About Me KS1" or "Kapow disciplinary KS2/3"?). No award-strip (Humanities banks UAS/RE via SoW — not a defect).

**Art Teesside — main route W1–W8 ×8 → SoW strand 9 "Creative Arts" (Aut1·W1–W7; half-term R16; Ladder R11). ALIGNED. — §5 Art PATCH QUARANTINE.**
- SC distinct per week, map to local-canvas→artists→technique→brief→critique→resolve→curate→share. Internally consistent ("Week n of 8", sow-strip week n). **Gate 2(a): award-strip "Explore Part A–D" (estate built as Explore) vs SoW weekly prog "Trinity Arts Award Discover".**

**Art Teesside — Autumn-2 route A2 W1–W7 ×7 → SoW strand 9 (Autumn 2). SURFACE-SPLIT. — §5 Art PATCH QUARANTINE (fixes = proposed diffs only, §Tier-2/3 below).**
- Defects (screen surfaces disagree with each other and with the route):
  1. **sow-strip week stuck at "Week 1" on all 7** (weektag correctly says Week 1…7). SURFACE-SPLIT.
  2. **sow-strip "Arts Aut 1" but weektag "Autumn 2"** — term mismatch (route is Autumn 2).
  3. **award-strip "Bronze Part A/B/C" but weektag "Explore"** — accreditation internal inconsistency; **Bronze is a GROW-level award** (Ladder R11: BUILD = Discover/Explore) → also Gate 2.
  4. **SC identical across all 7 A2 decks** ("record what I notice… choose materials… explain one choice") — undifferentiated per week; the main route varies SC per week. Likely copy-paste defect.

### 3.3 §4 protected content register (verified present at base; never modified this pass)

| Protection | Location | Status |
|---|---|---|
| LI money = practice money; "why we don't share family finances" | `LI_W1` | present ✔ untouched |
| FoodWise Eatwell framing, no calorie/weight/restriction; "the calories, or something else?" | `FW_W2` | present ✔ untouched |
| Deliberate wrong match-pills (CAREERS_W3 "Blue eyes") | `CAREERS_W3` | present ✔ never sequenced/corrected |
| CAREERS post-16 facts (participation-to-18, internships, Teesside providers) | `CAREERS_W7` file (internal Week 6) | verified ✔ not re-derived |
| Pass H W6/W7 swap; each file internally consistent | `CAREERS_W6/W7` | intact ✔ |
| SEMH: icon+label+colour, calm palette, no leaderboards; reduced-motion block | all 60 | reduced-motion present in all 60 ✔ |

### 3.4 Print/screen parity (§8)

Print packs are **generated by the `printPack(tier)` JS from the same tiered task data shown on screen** (Independent-Work
slides), so screen⇄print LO/task content shares one source — no static duplicate to drift. `.sow-strip`/`.award-strip`
are single title-slide surfaces (no separate print copy). The only screen-surface disagreements found are the **Art A2**
sow-strip/weektag/award splits (§3.2), which are screen-vs-screen, not print-vs-screen. printPack tiers uniform
(`supported/standard/stretch`) across all 60.

### 3.5 Integrity at base

- **Sentinel-45 = exactly 45** (31 BUILD_ASDAN + 6 BUILD_DT + 8 Art-main; HUM ×8 and Art-A2 ×7 do **not** carry `ll-g`). Pinned for §5 gate.
- **div/script tag balance: 0 imbalances across all 60.**
- reduced-motion block present in all 60.

## SOW-SILENT lists (both directions, report-only)

**(a) Lessons with no plausible SoW strand:** **none** — all 60 in-population lessons map to a SoW strand (§2.4).
The 7 orphaned `Build/Slideshows/BUILD_L1_*`/`FW_L1` samples (§2.3) are out-of-population and superseded by the
`BUILD_ASDAN` suites; report-only, no measurement, delete-vs-keep is Matt's call.

**(b) SoW strands with no BUILD lessons in this repo (expected — taught by colleagues from other resources; an empty
strand is not a defect):** 8 of 14 weekly strands —
Communication & Literacy · Numeracy · Science · RE & World Views · PSHE & Citizenship · RSHE · Computing & ICT · PE.

## Gate 1 (week mapping) / Gate 2 (accreditation) items awaiting Matt

### GATE 1 — one consolidated question (week/term placement)
The repo cannot settle two entangled week-mapping facts; both are batched here (never guessed):
1. **Concentrated-slot vs woven-strand model.** Every estate BUILD suite runs its **own internal W1–N and tags a single
   half-term** (all ASDAN + DT + Art-main = "Aut 1"; Art A2 = "Autumn 2"). The SoW instead **weaves** strands 11–14 as a
   single lesson/week across all three terms (e.g. careers content sits in **Spring** strand 11; construction in **Aut 2**
   strand 13). **Confirm the estate's concentrated-slot model is intended** — if so, every "placement" divergence above is
   **DELIBERATE**, not a defect, and no week-level rewrite follows.
2. **Careers slot length.** `CAREERS_W1–W5` weektags say **"Week n of 6"**; `CAREERS_W6/W7` (the Pass-H-swapped pair) say
   **"of 7"**. The suite has 7 lessons. **Confirm the slot is 7 weeks** → then `W1–W5` "of 6"→"of 7" is a clean Tier-1 fix
   (held, not applied, because it is entangled with the protected §4 swap). If a "6-week core + 1" reading was intended, "of 6" stays.

### GATE 2 — one consolidated question (accreditation)
1. **Arts Award level.** Estate BUILD Art route is built as **Explore** (main route award-strips "Explore Part A–D";
   weektags "Explore"); the SoW **weekly** Creative-Arts prog names **Discover** (Ladder R11 allows "Discover / Explore").
   Additionally the **Art A2 route award-strips claim "Bronze"** (a GROW-level award per Ladder R11) while its weektags say
   "Explore". **Confirm the intended BUILD Arts Award level** (Discover / Explore / Bronze). Brief notes a recorded open
   scheme decision about Explore adviser training — Matt's call, not a defect. *(Tabled, not rewritten.)*
2. **BUILD science GCSE/IGCSE references:** N/A — **no BUILD science lessons in the population** (Science strand is SOW-SILENT(b)).
3. **PEQ beyond E3 at BUILD:** none found — no BUILD lesson claims PEQ (ASDAN suites bank LI/FoodWise short-course modules
   + UAS Personal Challenge). Gate 2(c) **clear**.

## Tier 2 diffs awaiting approval
**None built.** No in-population change to LO/SC *meaning*, task, KO, or accreditation is warranted outside the Gate items
above. (The Humanities pitch question is a Tier-3 curriculum decision, not a Tier-2 diff.)

## Tier 3 — report-only (structural / quarantined / curriculum decisions)

- **Humanities ×8 pitch decision** (§3.2): "World About Me (KS1)" vs "Kapow disciplinary history (KS2/3)". Matt's curriculum call.
- **D&T v5 ×6** (§5 quarantine): classified ALIGNED to SoW Construction LOs; no edits made. Sequencing (Aut1 vs SoW Aut2 construction) → Gate 1.
- **Art Teesside A2 ×7 — proposed diffs (patch quarantine §5; NOT committed):**
  - `sow-strip` week number: change hard-coded "· BUILD · Week 1" → the deck's real week (`Week 2`…`Week 7`) on A2_W2…A2_W7.
  - `sow-strip` term: change "Arts Aut 1" → "Arts Aut 2" on all 7 A2 decks (route is Autumn 2, per weektag).
  - Accreditation: reconcile award-strip "Bronze Part …" with the intended BUILD level (Gate 2) — do **not** apply until Gate 2 settled.
  - Success criteria: differentiate the identical per-week SC on A2_W2…A2_W7 (currently all equal to A2_W1's) — content change, needs Matt sign-off.
  - `resources.json` catalogue gaps: add entries for `Art_Teesside/Build/BUILD_ART_A2_W3_Stencil_Lab.html` and `…A2_W4_Audience_Week.html` (proposed; describes quarantined files, so held).

## Tier 1 commits (with rollback SHAs)
**None.** Every actionable mechanical mismatch found is entangled with a §4 protection, a §5 quarantine (Art / D&T-v5),
or a Gate decision — so nothing qualified for free auto-fix. This is the expected outcome for a population that is
almost entirely protected/quarantined. No lesson file was modified by this pass.

## Final verification sweep (at tip)

| Check | Result |
|---|---|
| Sentinel-45 (ll-g set, data-URIs stripped) | **45 → PASS** (unchanged from base) |
| Lesson (non-`_passsb/`) files modified base..tip | **0** |
| `node --check` touched inline scripts | **N/A** — no lesson HTML modified |
| jsdom-boot touched files | **N/A** — none modified |
| div/script tag balance across 60 | 0 imbalances (measured at base; unchanged) |
| print-section counts | unchanged (no print surface edited) |
| Committed paths | only under `_passsb/` |
| Merged | **No** |

---

## Lineage & close-out

| Field | Value |
|---|---|
| Base SHA | `32ca685e1df619b333f3ee4385aed227aa675cdf` |
| Branch | `pass-sb-sow-build` |
| Branch tip | `45b83ed` (close-out commit; this pointer commit is its child) |
| Sibling pass | **Pass SL** (LAUNCH lessons ⇄ LAUNCH SoW) |
| Sentinel-45 | 45 at base; **unchanged** (no lesson file modified) |
| Lessons modified | **0** |
| Commits | scaffold · SOW_MATRIX · Phase 2 · Phase 3/close-out (all under `_passsb/`) |
| Merged? | **No.** Matt merges. |
