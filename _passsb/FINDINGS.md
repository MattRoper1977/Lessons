# Pass SB — BUILD lessons ⇄ BUILD SoW 2026-27 audit

**Status:** IN PROGRESS (measurement phase). Nothing merged. Matt merges.

## Lineage & provenance

| Field | Value |
|---|---|
| Pass letter | **SB** (no `_passsb/` or prior Pass SB ledger existed at base — letter stands, no self-rename needed) |
| Sibling pass | **Pass SL** (LAUNCH lessons ⇄ LAUNCH SoW) — this is the BUILD sibling |
| Repo | `MattRoper1977/Lessons` (the Lessons repo — **not** the site repo `mattroper1977.github.io`) |
| Base SHA (pinned) | `32ca685e1df619b333f3ee4385aed227aa675cdf` (origin/main @ session start) |
| Base commit | `LL-I close (final): commit the measurement records + remedy-observed line` (2026-07-28 18:27:26 +0000) |
| Branch | `pass-sb-sow-build` (off origin/main) |
| Branch tip | _(derived at close-out, never hand-typed)_ |
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

SoW weekly strand (14) → estate BUILD suite. Only **4** SoW strands carry BUILD lessons in this repo; the other
10 are **SOW-SILENT(b)** (taught by colleagues from other resources — an empty strand is not a defect).

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
_Pending._

## SOW-SILENT lists (both directions, report-only)
_Pending._

## Gate 1 (week mapping) / Gate 2 (accreditation) items awaiting Matt
_Pending._

## Tier 2 diffs awaiting approval
_Pending._

## Tier 1 commits (with rollback SHAs)
_Pending._

## Final verification sweep (at tip)
_Pending._
