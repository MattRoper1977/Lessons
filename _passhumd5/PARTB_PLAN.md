# PARTB_PLAN — HUM-D5 Part B landing plan, PREPARE ONLY (STOP-B1), assembled 2026-09-20

**Nothing is landed by this document.** No landing branch exists; nothing was pushed to one. It is the written plan the order asked for, in the science release's shape, with counts. Two layers are kept apart and labelled: the **draft** (four read-only research lanes over the packs, the Lessons repo at carrier worktree `0248ea78`, the Site registry at `1e98bec0`, and the science records) and the **critique** (an adversarial re-measure of every count and step, taken after the estate moved). Where they disagree the critique's figure is the later measurement and is the one to carry; the draft's is left in place so the drift is visible. The assembler's own spot checks (same instruments: `find`, `grep`, `sha256sum -c`) are in §0.

## 0. Gate — re-cut at assembly time (refs derived, not transcribed)

| gate limb | state now | evidence | verdict |
|---|---|---|---|
| SCIENCE S5 | the PASS 7 CLOSE readback is being delivered with this document; Site #412 → `1e98bec0`, Lessons #595 → `cbfbc70c`, Apps #118 → `bbce377` are merged; cross-estate is green on both mains (Lessons 35478360154, Apps 35478375227); Watch main re-dispatched, verdict pending at assembly | SX3_LEDGER_pass3.md tail; SX3_PASS7_CLOSE.md | **OPEN until the readback is accepted** |
| Lessons main green | `cbfbc70c`: UX2 35478360136, Education Pages publication 35478360629, FieldOps 35478360130, cross-estate 35478360154 — all SUCCESS; GLV3 not triggered | ledger, main-push table | GREEN |
| Matt's phone check | the five URLs are in SX3_PASS7_CLOSE.md §10; not a measurement this container can make (origin 403) | — | **NOT MEASURED — Matt's** |
| Part A closed, rulings recorded | HUMD5_PARTA_CLOSE.md delivered on `claude/hum-d5-proof` (head `37f04c16`), H1–H9 dispositioned B0001–B0130; **8 decisions still Matt's** (§5 there: media credits, B0125, Salah, H3 five, H6 twelve, Fallback opt-out, timer-ink alternative, phone sizes) | PROOF_LEDGER.md "Rulings applied", HUMD5_PARTA_CLOSE.md §5 | **OPEN on those eight** |
| B0 pack sums | SHA256SUMS.txt in the 11 Final packs: 1605 entries checked, 0 FAIL (regenerated after the last ruled write, 2026-09-19 23:51); Fallback MANIFEST.json rehashed | assembler spot check | PASS |

Token if Part B were attempted now: `HUMD5_BLOCKED:science-S5-readback-not-accepted;part-a-eight-decisions-open`.

**Assembler's spot checks (2026-09-20, `/tmp/claude-0/humd5/unzipped`):** lessons 120; W dirs 120; lesson-dir files 1662 / 228,630,296 B; `../../../START_HERE.html` hrefs 240 over the 120 Lesson.html; RE SoW hrefs 213 (the draft's "0" is wrong, the critique's 213 stands); pack files 1750 / 229,831,832 B. These agree with the critique's re-measure and disagree with the draft's byte totals (bytes moved when the PDFs were re-rendered and the sums/changelogs rewritten).

**Standing limits this plan must satisfy (critique's check, carried):** no force-push, no branch deleted, nothing disabled — none proposed. CI edits: only the generated PIN1 widening (precedent 3b) and the two carrier pin moves are permitted; the hand widening of `glv3-verify.yml` / `cross-estate-on-content.yml` paths is a ruling item, NOT a PR-0 line. Source selection never filesystem order: P0 must produce the 120-row `deck | generations | chosen source | sha256 | bytes` table, ruling the `*_Reviewed` inner-folder names (Final content) and the byte-identical duplicate RE_Autumn_GROW upload explicitly. DECLARED_DIVERGENCES stays empty: `tools/sx3/check_landing_titles.py` (now on main) runs over the landing pages per PR, LISTED 0 / DISTINCT 0 recorded. Every SHA is derived at write time.

---

## 1. Population and homes

### Draft (lanes, at carrier worktree 0248ea78 / Site 1e98bec0)

**Inputs (scope: `ls /tmp/claude-0/humd5/unzipped/`).** 13 packs, 12 carrying lessons + `HUM_00_SoW_and_Order`. Fact 1: every outer folder is `*_Final`, every inner folder `*_Reviewed` (legacy name; STATE.md "Generation check": 120/120 Lesson.html carry `#vary-exit` + a starter block, so the content is the Final generation; `CHANGELOG_Final_2026-09-19.md` in all 11 Final packs). Fact 2: **no `HUM_Autumn_1_BUILD_GROW_Final`** exists; only the Fallback (`READ_ME_FALLBACK.txt`: the Reviewed zip "arrived truncated") → R13's Fallback branch is live for 14 cells.

**Lessons and cells.** 120 incoming = 78 Humanities (A1 7×3, A2 7×3, S1 6×3, S2 6×3; 14 of them Fallback) + 42 RE (A1 7×3, A2 7×3). SoW cells: Humanities 117 (117 `Week N ·` headings, scope: `Humanities_Scheme_of_Work_2026-27.html`), RE 42 (6 pathway·term sections × weeks 1–7, scope: `RE_Scheme_of_Work_Autumn_2026.html`) = 159, matching P0. NO INCOMING: 39 Summer Humanities cells; RE has no Spring/Summer cells in its SoW (Autumn only, R8).

**Pack inventory (scope: `find` over every file under `<pack>/<inner>/`, `partb_scratch/census_detail.txt`).** 1,750 files, 231,750,463 B (221.0 MiB): html 487 / 101,752,796 · mp4 120 / 46,523,541 · pdf 360 / 28,346,800 · docx 228 / 17,646,330 · pptx 120 / 16,643,201 · png 158 / 17,236,296 · svg 106 / 2,608,563 · jpg 6 / 548,133 · txt 130 / 283,923 · xlsx 13 / 94,051 · csv 9 / 3,244 · md 12 / 44,459 · json 1 / 19,126. Final-only (minus Fallback, minus SoW pack) 214,491,822 B ≈ 204.6 MiB — consistent with R9's "≈ 210 MB … the Fallback adds 17" (Fallback 16,960,427 B).

| pack | files | bytes | lessons |
|---|---:|---:|---:|
| HUM_00_SoW_and_Order | 7 | 298,214 | 0 |
| HUM_Autumn_1_BUILD_GROW_Fallback | 127 | 16,960,427 | 14 |
| HUM_Autumn_1_LAUNCH_Final | 97 | 11,638,640 | 7 |
| HUM_Autumn_2_BUILD_Final | 121 | 12,500,460 | 7 |
| HUM_Autumn_2_GROW_Final | 111 | 17,688,950 | 7 |
| HUM_Autumn_2_LAUNCH_Final | 115 | 25,289,160 | 7 |
| HUM_Spring_1_BUILD_GROW_Final | 184 | 24,686,410 | 12 |
| HUM_Spring_1_LAUNCH_Final | 84 | 10,999,023 | 6 |
| HUM_Spring_2_BUILD_GROW_Final | 194 | 26,903,765 | 12 |
| HUM_Spring_2_LAUNCH_Final | 104 | 17,239,876 | 6 |
| RE_Autumn_BUILD_Final | 202 | 21,603,734 | 14 |
| RE_Autumn_GROW_Final | 202 | 22,276,097 | 14 |
| RE_Autumn_LAUNCH_Final | 202 | 23,665,707 | 14 |

**Per-lesson file set (scope: 120 W dirs, prefix `<PATHWAY>_(RE_)?<TERM>_W<nn>_` stripped).** 106 Final lessons: Lesson.html, Knowledge_Organiser.html+.pdf, Pupil_Resources.html+.pdf, Teacher_Notes.docx+.pdf, Editable_Pack.docx, Editable_Slides.pptx, Model_Transcript.txt, Captioned_Model.mp4 + an un-prefixed Sources_and_checks.html (13 files) plus images (Object_Picture_Choices.png+svg in 61, Visual_Resource.png in 64, Teaching_Visual_1.png+svg in 33, Teaching_Photo_1/2.jpg in 3) and Data.csv+xlsx in 9 / Data.xlsx only in 2. 14 Fallback lessons: 8 files (Lesson.html, KO html+pdf, Pupil_Resources.pdf, Teacher_Notes.pdf, Editable_Pack.docx, Editable_Slides.pptx, Captioned_Model.mp4) — no Teacher_Notes.docx, Pupil_Resources.html, Model_Transcript.txt, `#save-independent` (CHECKS.md E16: "14 absent-by-generation").

**Homes (R2), resolved against the repo (scope: `/home/user/lessons-carrier` HEAD 0248ea78, `git ls-files` + `find`).** The repo has NO `Lessons/` directory; R2's `Lessons/…` prefix is the publication prefix (build_education.py L232 `roots={'lessons':(lessons,'/Lessons/')}`), so the homes are repo-root `Humanities_Teesside/2026-27/…` (parent EXISTS: 498 tracked files, 140,242,539 B, 185 html; `2026-27/` NOT FOUND) and `RE_Teesside/2026-27/…` (`RE_Teesside/` NOT FOUND). 18 term directories, 120 W directories (`partb_scratch/target_map_per_week.txt`):

| target `<Subject>/2026-27/<P>/<Term>/` | weeks | files | bytes | source |
|---|---:|---:|---:|---|
| Humanities_Teesside BUILD/Autumn_1 | 7 | 56 | 9,845,926 | Fallback |
| Humanities_Teesside BUILD/Autumn_2 | 7 | 115 | 12,460,504 | A2_BUILD_Final |
| Humanities_Teesside BUILD/Spring_1 | 6 | 100 | 14,796,961 | S1_BUILD_GROW_Final |
| Humanities_Teesside BUILD/Spring_2 | 6 | 90 | 9,418,239 | S2_BUILD_GROW_Final |
| Humanities_Teesside GROW/Autumn_1 | 7 | 56 | 6,775,427 | Fallback |
| Humanities_Teesside GROW/Autumn_2 | 7 | 105 | 17,651,000 | A2_GROW_Final |
| Humanities_Teesside GROW/Spring_1 | 6 | 78 | 9,837,492 | S1_BUILD_GROW_Final |
| Humanities_Teesside GROW/Spring_2 | 6 | 98 | 17,431,056 | S2_BUILD_GROW_Final |
| Humanities_Teesside LAUNCH/Autumn_1 | 7 | 91 | 11,601,782 | A1_LAUNCH_Final |
| Humanities_Teesside LAUNCH/Autumn_2 | 7 | 109 | 25,249,846 | A2_LAUNCH_Final |
| Humanities_Teesside LAUNCH/Spring_1 | 6 | 78 | 10,965,127 | S1_LAUNCH_Final |
| Humanities_Teesside LAUNCH/Spring_2 | 6 | 98 | 17,201,825 | S2_LAUNCH_Final |
| RE_Teesside BUILD/Autumn_1 · Autumn_2 | 7 · 7 | 98 · 98 | 11,077,843 · 10,468,093 | RE_BUILD_Final |
| RE_Teesside GROW/Autumn_1 · Autumn_2 | 7 · 7 | 98 · 98 | 11,715,282 · 10,501,872 | RE_GROW_Final |
| RE_Teesside LAUNCH/Autumn_1 · Autumn_2 | 7 · 7 | 98 · 98 | 12,106,790 · 11,495,459 | RE_LAUNCH_Final |

Lesson-dir files landing: **1,662 / 230,600,524 B** (Humanities 1,074 / 163,235,185; RE 588 / 67,365,339) — html 452 / 101,256,382 · mp4 120 / 46,523,541 · pdf 360 / 28,346,800 · images 258 / 20,073,975 · docx 226 / 17,534,432 · pptx 120 / 16,702,211 · txt 106 / 95,037 · xlsx 11 / 64,902 · csv 9 / 3,244.

**The publisher copies every PUBLIC-suffix file, not only html** (`/home/user/mattroper1977.github.io/domain-split/build_education.py` L42 PUBLIC allowlist includes .pdf .docx .pptx .xlsx .csv .txt .md .json .mp4 .png .svg .jpg; L85–91 `public_file()`; L241–243 copy loop; L58–59 `tracked()` = `git ls-files`, so only committed files publish). All 13 pack suffixes are in PUBLIC and in the admission reader's REVIEWED|INERT (education_publication_admission.py L15–19) → nothing drops by suffix, nothing raises `Unclassified publication file` (L49–50). Every lessons `.html` receives the navigation adapter (L276–280 `with_lesson_navigation`), so served html bytes ≠ tree bytes — the registry digest is of the built output (§4).

**Pack-root files (75 / 869,162 B) — disposition under R2**

| file | copies | measured | R2 disposition → proposal |
|---|---:|---|---|
| START_HERE.html | 11 | all distinct sha256; 99,084 B | rebuild ONE index per subject/term: **6** (Humanities Autumn_1, Autumn_2, Spring_1, Spring_2; RE Autumn_1, Autumn_2). Autumn_1 Humanities has no Fallback START_HERE → built from the LAUNCH START_HERE + Fallback `MANIFEST.json` (proposal). Name/location proposal following the Science PATHWAY_PARENTS precedent (`Science_Teesside/{Build,Grow,Launch}/START_HERE.html`, verify_change_boundary.py L36–38; catalogue rows type `teacher`, pin_catalogue_contract.py L1293–1295): `<Subject>/2026-27/<Term>/START_HERE.html`. RE index states "Autumn only" (R8). |
| Review_record.html | 11 | all distinct; 130,827 B | "keep ONE per subject" is lossy when all 11 differ → RULING: merge with per-pack headings (authoring) or keep the 11 under records (not R2's words) |
| Sources_and_checks.html | 11 root + 106 per-lesson | ONE sha256 (d8229e5f…) across all 117 | ONE per subject is lossless: 2 copies. The 106 per-lesson copies are linked by no Lesson.html (scope: hrefs in sampled Lesson.html + START_HERE) → RULING: land 106 (published html 460) or dedupe (354) |
| README.txt | 11 | identical, 208 B | one per subject or none |
| CHANGELOG_Final_2026-09-19.md | 11 | all distinct | not named by R2; proposal: records dir (they are the proof-pass record) |
| SHA256SUMS.txt | 11 | 185,667 B; describe pack layout | not landed (proposal) |
| Fallback MANIFEST.json, READ_ME_FALLBACK.txt | 1 + 1 | 19,126 B + 504 B | not covered by R2 → ruling |
| Fallback Editable_Visuals/ | 12 svg + READ_ME.txt | 319,444 B | **not covered by R2** → ruling |
| SoW pack | 2 html (62,425 + 75,828 B), 2 docx (109,959 B), 2 xlsx alignment sheets (29,149 B), ORDER_HUM-D5.md (20,853 B) | R8 lands html + docx | xlsx + ORDER md not ruled; proposal: the order text never lands |

**`_records/` cannot be published as named.** build_education.py L89 `not any(x.startswith(('.', '_')) for x in p.parts)` drops any path with an underscore component; a literal `_records/` never reaches the education site, while the rebuilt indexes would link it. RULING: non-underscore name (proposal `<Subject>/2026-27/records/`) or accept unpublished.

**Relative links after the move (scope: hrefs in two sampled Lesson.html + one START_HERE.html).** Every Lesson.html links `../../../START_HERE.html` twice (= 240 hrefs over 120 lessons) plus same-directory Teacher_Notes.pdf, Pupil_Resources.pdf, Editable_Pack.docx; from `<Subject>/2026-27/<P>/<Term>/W<nn>/` the target resolves to `<Subject>/2026-27/START_HERE.html`, which does not exist under R2 → rewrite to the term index (with the proposal above: `../../../<Term>/START_HERE.html`, 240 exact string edits, count proved by the apply script). START_HERE links per lesson: Lesson.html, KO.pdf, Pupil_Resources.pdf, Teacher_Notes.pdf, Editable_Pack.docx, Editable_Slides.pptx, Captioned_Model.mp4 (the mp4 link is what R9's budget step removes). RE SoW html carries 0 hrefs (§7).

**Published-html arithmetic after landing (scope: census + the publisher's rules):** 452 W-dir html + 6 indexes + 2 SoW = **460** (records unpublished) / **464** (records in a public dir) / 354 or 358 if the 106 per-lesson Sources_and_checks copies are deduplicated. Published file count 3,900 → ≈5,577 (variant-dependent, §4).

### Critique — re-measured, corrections to carry

Structure and counts of files/dirs reproduce; the BYTE figures do not, and two R2/R8 facts are wrong.

**Reproduced (scope: `find` over /tmp/claude-0/humd5/unzipped, script partb_scratch/census.py):** 13 packs; 1,750 files; 120 W dirs; 1,662 lesson-dir files (Humanities 1,074, RE 588); per-pack file counts all match; html 487 / mp4 120 / pdf 360 / docx 228 / pptx 120 / png 158 / svg 106 / jpg 6 / txt 130 / xlsx 13 / csv 9 / md 12 / json 1; 240 `../../../START_HERE.html` hrefs over 120 Lesson.html (the only `../` hrefs); Sources_and_checks ONE sha across 11 root + 106 per-lesson copies; README.txt 11 × 208 B identical; START_HERE 11 distinct / 99,084 B; Review_record 11 distinct / 130,827 B; SHA256SUMS 185,667 B; MANIFEST.json 19,126 B; Editable_Visuals 13 files / 319,444 B; Fallback file set 8 per lesson (14 W dirs); files-per-W-dir histogram {14:42, 17:19, 16:2, 15:24, 13:19, 8:14}.

**Not reproduced — bytes moved after the draft's census (CHANGELOG/SHA256SUMS rewritten 23:51; PDFs re-rendered 22:xx):** total 231,750,463 → **229,831,832 B** (219.2 MiB / 229.8 MB); pdf 28,346,800 → 26,370,526; md 44,459 → 57,015; txt 283,923 → 284,297; docx 17,646,330 → 17,644,388; html 101,752,796 → 101,740,441; pptx total is internally inconsistent in the draft (type table 16,643,201 vs lesson-dir 16,702,211 — the latter is the true total, 120 files). Every per-pack byte figure differs (e.g. Fallback 16,960,427 → 16,963,083; A1_LAUNCH 11,638,640 → 11,582,561; S2_BUILD_GROW 26,903,765 → 26,467,227; RE_LAUNCH 23,665,707 → 23,622,566). Lesson-dir bytes 230,600,524 → **228,630,296** (Humanities 161,691,422; RE 66,938,874). Pack-root 869,162 → 882,092 B (READ_ME_FALLBACK.txt 504 → 878 B, CHANGELOGs 36,162 B total). Final-only (minus Fallback, minus SoW pack) 214,491,822 → **212,570,535 B = 212.6 MB**, which is what R9's "≈ 210 MB" means (decimal MB, not the draft's MiB). Every target-table byte column and §6's PR byte column inherit the stale figures; re-cut them from the packs as they stand after B0, and state the census timestamp.

**Publisher set:** `build_education.public_file()` + `excluded_asset()` imported from the Site at 1e98bec0 over `git ls-files` at 0248ea78 gives **3,899 files / 894,517,656 B (853.1 MiB) / 1,506 html** (draft 3,900 / 894,531,940). L42 PUBLIC, L58–59 `tracked()`, L85–91 `public_file()` (L89 underscore rule), L232 `roots`, L241–243 copy loop, L276–280 navigation adapter, L342–343 admission verify — all confirmed at those lines. All 13 pack suffixes are in PUBLIC and in REVIEWED|INERT (education_publication_admission.py L15–19) — confirmed.

**R8 fact wrong:** the RE SoW is not link-less. `RE_Scheme_of_Work_Autumn_2026.html` carries **213 hrefs (single-quoted)**: 210 relative lesson-file links, 35 per pathway·term, i.e. 5 per lesson (`BUILD/Autumn_1/W01/BUILD_RE_A1_W01_{Lesson.html, Pupil_Resources.pdf, Teacher_Notes.pdf, Editable_Pack.docx, Editable_Slides.pptx}`), plus 3 anchors `#BUILD/#GROW/#LAUNCH`. They resolve ONLY if the SoW html sits at `RE_Teesside/2026-27/` (R8 "its lesson links assume the merged RE tree of R2") — the draft names no home for either SoW file. The Humanities SoW carries 1 href (`#plans`) and no lesson links. Add a row: SoW homes = `<Subject>/2026-27/<SoW>.html|.docx`, and count the 210 links in P6's "relative links resolve after the move".

**R2 index rows:** the draft's `<Subject>/2026-27/<Term>/START_HERE.html` proposal is fine, but `Humanities_Teesside/index.html` must ALSO list the 78 new lessons as `article[data-lesson-path]` (check_catalogue_static.py L48–51, confirmed) — this is a SHELVES change in §3, not an index rebuild; say so here.

---

## 2. Catalogue — rows, contract arithmetic, the four writers and the census tail (L21/L23)

### Draft (lanes, at carrier worktree 0248ea78 / Site 1e98bec0)

**Today (scope: `/home/user/lessons-carrier/resources.json`, `tools/catalogue/pin_catalogue_contract.py`, `tools/verify_cross_estate_unification.py`).** 956 rows = ORIGINAL_ROW_COUNT 734 (L18; ORIGINAL_ROWS_SHA256 b8ffcb16… L19) + SHELF_ROWS 104 (literal L20–1286 + appends L1288, L1293–1295) + 118 derived companion-pack rows (`pack_rows_for()` L1745–1760 from `data/companion-packs.json`); `preserved_rows_errors == []`. Gate copy: CATALOGUE_ORIGINAL_ROWS 734 (L673), SHA (L674), CATALOGUE_SHELF_ROWS 222 (L681), CATALOGUE_SHELF_ROWS_SHA256 (L688). Subjects: `Humanities` 98 rows, `Humanities · Teesside` 5; `RE & World Views` / `World Views` **0** (scope: whole file). Schema `resources.schema.json`: required id, subject, title, file, type, family; type enum lesson/game/revision/pupil/teacher/support/hub/Lesson/Hub; year enum 2025-26/2026-27; halfTerm enum Autumn 1…Summer 2; **additionalProperties false**.

**New rows: 129** (sentinel delta stated first; universe = resources.json rows): 120 `lesson` rows (P5's "78 + 42") + 6 subject/term index rows type `teacher` (precedent: the three Science START_HERE rows appended at L1293–1295 and rows [677]–[679] `catalogue-2026-27-humanities-*-w1-w8-vb-wave3`) + 2 SoW rows type `support` (precedent: current SoW rows [231], [233], [235] are `support`) + 1 hub row for the new subject `RE & World Views` (precedent: [735] `humanities-pathway-term-hub` → `Humanities_Teesside/index.html`, type hub). Knowledge_Organiser.html / Pupil_Resources.html / Sources_and_checks.html have **no row precedent**; docx/pptx enter only as derived `pack` rows via `data/companion-packs.json` (tools/ux2/companion_catalogue.py) — not proposed here.

**Row shape (existing lesson row [684], quoted as the template):** `{"id": "humanities-grow-w1-beliefs-and-worldviews", "title": "GROW Humanities W1: Beliefs and world views around us (Autumn 1 · week 1 · C60)", "type": "lesson", "subject": "Humanities", "year": "2026-27", "file": "Humanities_Teesside/GROW_W1-W8_2026-27/GROW_HUM_W1_Beliefs_And_Worldviews_Around_Us.html", "desc": "…", "family": "GROW Humanities · Autumn 1", "keywords": ["humanities", "grow", "re", "world views", "beliefs", "community", "week 1"], "added": "2026-09-02", "halfTerm": "Autumn 1"}`. Proposed new-row shape: same keys; `subject` = `Humanities` or `RE & World Views`; `year` = `2026-27` (R8 year tag on every row); `halfTerm` = the term facet; pathway in `family` (`<PATHWAY> Humanities · <Term>`) and `keywords`; week in `title` (`… (<Term> · week n)`) and `keywords` (`week n`) — because `pathway` / `week` / `generation` are NOT row keys today (gate L686 CATALOGUE_ADDITIVE_TAG_KEYS = {halfTerm, unit}) and the schema refuses new keys. R13's `generation="fallback-2026-09-19"` therefore lives in the P7 report and RETIRE/CELL_MAP, never on the row (R13 says report, not pupil surface). `file` = the R2 path. P5's "chip counts proved through the real filter chain": the chip derivation (`assets/catalogue/catalogue.js` / `hub.js`) was **not traced** — the instrument is owed at P5; the served hub sentinel today reads "1046 resources - 13 subjects" (ledger L12), so +1 subject is the expected chip delta; the hub's counting universe is not measured.

**Where the rows go, and the contract arithmetic (derived from the counts above; universes labelled).** New rows are appended to the SHELF_ROWS literal and land in resources.json at index 838… before the 118 derived pack rows (layout rule L1773–1781: rows == 734 + len(SHELF_ROWS) + len(pack_rows), original block digest-checked, shelf block == SHELF_ROWS, tail == derivation). R4's "rows for retired surfaces are removed, not hidden" hits three blocks (§5): 29 rows inside the frozen 734 ([182]–[205] the 24 v4 slideshows; [230] hub, [231]/[233]/[235] SoW, [363] tracker) — removing them changes ORIGINAL_ROW_COUNT and ORIGINAL_ROWS_SHA256 in pin_catalogue_contract.py L18–19 AND both gate copies L673–674, which the gate comment L670–672 says no tool can bless ("Neither the catalogue pin tool nor the generic manifest pin tool can bless an edited, deleted or reordered original resource") → **hand re-cut under a ruling, red-proved**; 10 shelf rows ([736] David cover hub, [737]–[739] Teaching_Packs hubs, [764]–[767],[769],[770] classic-33-b2) → re-cut the literal; 17 pack-tail rows ([838]–[843],[859]–[863],[877]–[882], Teaching_Packs Week_9–14) are NOT R4-named (W3–W7 only) → left unless ruled. Resulting sentinel: resources.json 956 → **1,046** (= 705 + 223 + 118); SHELF_ROWS 104 → 223 (+129 −10); CATALOGUE_SHELF_ROWS 222 → 341 (re-cut by the pin tool L1825–1831); if the 17 pack rows are also ruled out: 1,029 / 324.

**The four derived records (L21: every row must appear in all four; 3b hit each as a separate CI red) + the fifth (L24):**

| record | writer / check | today | after landing | notes |
|---|---|---:|---:|---|
| `tools/catalogue/TERM_AND_STYLE_EVIDENCE.json` (INTERNAL) | `check_catalogue_static.py` run bare (no --check flag; L7 only `--baseline-root`; L15 every row's `file` in proof; L17 sha256 equality where recorded); writers `build_catalogue.py` (merges, and per the 3b commit body "rewrites 38 unrelated entries and moves the shelf" → 3b recorded its entries separately) and `restamp_evidence_sha256.py --write --decks` | 1,080 entries (111 under Humanities_Teesside/) | +129 entries `{term, terms, style, pathway, evidence, batch, sha256, title}`; every stubbed file that has an entry with sha256 must be restamped or dropped | L42–51: every `subject == 'Humanities'` row (type != hub, kind != pack) must be in `HUMANITIES_SELECTION.json` (142) and `humanities-shelf.json` (142) and listed by `Humanities_Teesside/index.html` as `article[data-lesson-path]` → +78; `RE & World Views` rows bypass this check and have no shelf |
| CATALOGUE_PINS (INTERNAL, both gate copies) | `pin_catalogue_contract.py --lessons DIR --apps DIR [--check]` (L1848–1859); refuses if copies differ (L1795–1796), if REVIEWED_PATHS omits an existing admission (L1798–1800), if rows ≠ 734+shelf+pack (L1773–1781), if `lesson-order.json != build_lesson_order.derive()` (L1806–1808); writes BOTH copies or restores both (L1838–1844) | 543 = REVIEWED_PATHS 543 (27 Humanities: 26 David cover + index.html) | + every stub (≈109, needed by the cross-estate M-rule L1128–1139 and the GLV3 transactions) + the landing manifest (§3) + `RE_Teesside/index.html` if made a SHELF → ≈654 | the ORIGINAL_ROW_COUNT re-cut must precede the pin run or L1773–1781 refuses |
| `data/resource-sizes.json` (**PUBLISHED**, registry pair today 8141fb82 → abd0a1ba) | `tools/ux2/resource_sizes.py --root DIR --write / --check` (L94–116; fails on missing inputs L103–105; byte-for-byte compare L110–115); UX2 gates line 141; `s1m-published-input-proof.yml` L69–70 `cmp`s it against the Site's `domain-split/resource_sizes.py` | 1,476 measured sizes | +129 rows' `file` + `files[].path` | moves a served byte → registry pair (L23) |
| PIN1 trigger list (INTERNAL) | `tools/pin1/derive_triggers.py --root DIR --check / --write` (L180–210); rewrites the block between `# BEGIN/END PIN1 DERIVED PATHS` in BOTH pull_request and push blocks of `mbm-cross-estate-unification.yml` (L28–29, L133–138); fails on `missing=/unexpected=` (L170–174) | 557 per block (L13–571, L575–1133); Humanities 27, RE 0 | +≈111 lines per block (one per new pin) → ≈668 | "a generated TRIGGER-LIST WIDENING, not a hand CI edit and not a pin move" (3b commit body) — the sanctioned shape under "No CI edit except pin moves under existing precedent" |
| `tools/catalogue/STATIC_CHECK_RESULTS.json` (L24, results record, read by no gate) | rewritten by every `check_catalogue_static.py` run (L56); in CATALOGUE_RECORD_PATHS (gate L695) | baseline = the HEAD the writer ran at | regenerate once per PR, accept the one-commit lag (L24 detail) | self-referential by construction |

Also in the same class, all with `--check` in UX2 gates: `tools/ux2/unit_tags.py` (line 114; append-only halfTerm/unit), `tools/ux2/companion_catalogue.py` (125), `tools/catalogue/build_display_titles.py` (106), `tools/ux2/build_spine.py` (139); `assets/catalogue/lesson-order.json` (1,080 entries `{ordinal, canonical, weeks, sourceSha256}`) regenerated by `build_lesson_order.derive()` (iterates every row + humanities-shelf supplements L11–30; new rows need evidence-backed term/week or `unspecified` in TERM_REVIEW.json); `assets/catalogue/humanities-shelf.json` 142 → 142 + 78 − retired Humanities-subject rows via `build_humanities_shelf.py`.

**RULE carried from L21/L23 (the publication census tail).** Before any push that adds or removes a row: run the four `--check`s together (`/tmp/claude-0/pass6/pre_ci_catalogue_sweep.sh`: check_catalogue_static bare · pin_catalogue_contract --check · resource_sizes --check · derive_triggers --check) plus the UX2 checks above; (L23a) end the sweep with the education publication census whenever a PUBLISHED derived record moved (resources.json, lesson-order.json, resource-sizes.json, humanities-shelf.json, and on the Site side data/domain-catalogue.json + data/resource-discovery.json); (L23b) the build that supplies registry digests is taken AFTER the LAST regeneration — "Regenerate, THEN build, THEN write pairs" (the 3b defect: `CHANGED education-lessons/data/resource-sizes.json` on 124f513b). Regenerate with the writers, never hand-edit (L21).

### Critique — re-measured, corrections to carry

All catalogue counts reproduce at 0248ea78: resources.json 956 rows; ORIGINAL_ROW_COUNT 734 (pin_catalogue_contract.py L18), ORIGINAL_ROWS_SHA256 b8ffcb16… (L19); SHELF_ROWS 104 (literal from L20; appends at L1288, L1293–1295); 118 derived pack rows (`pack_rows_for` L1745–1760; `data/companion-packs.json` packs 118); layout rule L1773–1781; refusals L1795–1800 (copies differ; REVIEWED_PATHS omits an admission), L1806–1808 (lesson-order derive); visible_body_sha256 L1811; re-cut L1825–1831; write-both-or-restore L1838–1844; argparse L1848–1859. Gate copy: CATALOGUE_ORIGINAL_ROWS 734 (L673), SHA (L674), CATALOGUE_SHELF_ROWS 222 (L681), ADDITIVE_TAG_KEYS {halfTerm, unit} (L686), SHELF_ROWS_SHA256 (L688), CATALOGUE_RECORD_PATHS (L695), caller digest 16448b91 (L789), boundary_errors L1128–1139, MRD diff L1391–1409. Subjects: Humanities 98, Humanities · Teesside 5, `RE & World Views` 0 (scope: whole file, 24 subjects). Schema (`items`): required [id, subject, title, file, type, family], additionalProperties false, type/year/halfTerm enums as stated. Row indices [182]…[882] all resolve to the ids/files the draft names. TERM_AND_STYLE_EVIDENCE `entries` 1,080 (111 under Humanities_Teesside/); lesson-order `entries` 1,080 (+124 supplements); resource-sizes `sizes` 1,476; humanities-shelf `lessons` 142; HUMANITIES_SELECTION `lessons` 142; CATALOGUE_PINS.files 543 = REVIEWED_PATHS 543 (27 Humanities_Teesside/, 0 RE_Teesside/); PIN1 557 lines per block (L13–571, L575–1133), Humanities 27, RE 0; ux2-gates.yml lines 106/114/125/139/141; s1m L69–70 `cmp`; check_catalogue_static.py has only `--baseline-root` (L7).

**Corrections:**
1. **Counts are for a superseded main.** origin/main cbfbc70c changed `tools/verify_cross_estate_unification.py` (8 lines) and `tools/catalogue/STATIC_CHECK_RESULTS.json`; the gate copy is f38a2a6f on both estates. Re-run the four `--check`s on origin/main before quoting any "today" figure.
2. **The sweep is now tracked.** `tools/sx3/pre_ci_catalogue_sweep.sh` at origin/main runs the same four checks AND a publication-census tail (`check_education_publication_admission.py --build-control`, gated on `SITE=`/`OUTPUT=`). Cite that path, not `/tmp/claude-0/pass6/pre_ci_catalogue_sweep.sh` (a scratch copy, 1,757 B).
3. **DECLARED_DIVERGENCES is a fifth control the draft never names.** `tools/sx3/check_landing_titles.py` at origin/main (L45 `DECLARED_DIVERGENCES: dict[str, str] = {}`; L112 comparison; L183 "LISTED … declared") is the tool the standing limit refers to (SX3_S2_2_TITLES.md L7–8: "LISTED 0 … DECLARED_DIVERGENCES empty"). It compares each landing deck's `<h1>` with the title it is listed under and decks with each other; it is NOT tracked at 0248ea78 (scope: `git ls-files`) and NOT hooked into any workflow at origin/main (scope: every `.github/workflows/*.yml` at origin/main, 0 references). The draft's row-title rule (`… (<Term> · week n)`) would by construction diverge from the deck `<h1>` unless the comparison normalises — run the tool over the 120 + 6 + 2 landing pages, keep the dict empty, and record LISTED 0 / DISTINCT 0 per PR.
4. **R7 furniture is absent from the incoming HTML, so the writers ADD bytes, not re-stamp.** Scope: 120 Lesson.html — `hud.js` 0/120, `<link rel="canonical">` 0/120, `ko-fi` 0/120 (static string presence). Every byte the P1 writers add lands before the evidence/size/pin writers run; the draft's "no rows change until PR-4" is fine, but its "granted build after the last regeneration" must also be after the LAST furniture write (P1 "re-run the render gate after the writers").
5. `RE_Teesside/index.html` as a hub row: the draft proposes it as `hub` ([735] precedent) and, in §3, as a SHELVES member — pick one; a SHELVES member must be pinned in CATALOGUE_PINS (verify_change_boundary.py L373–375), which the count "≈654" does not include explicitly.

---

## 3. GLV3 route per file class

### Draft (lanes, at carrier worktree 0248ea78 / Site 1e98bec0)

**The judge (`/home/user/lessons-carrier/_glv3/tools/verify_change_boundary.py`).** PROTECTED L22–24 = ('Art_Teesside', 'GROW_ASDAN', 'LAUNCH_ASDAN', 'Grow/Slideshows', 'Launch/Slideshows', 'Science_Teesside', 'Humanities_Teesside', 'Baseline_Weeks', 'BUILD_Estate_v3'); `protected()` L282–283 prefix match; `git_changes` L412–421 diffs `base...HEAD` over PROTECTED — **committed work only** (L17: staged files measured as an empty diff). `judge()` L355–409 routes each protected change through exactly five branches (L372–396): SHELVES (L25: `Science_Teesside/index.html`, `Humanities_Teesside/index.html`; A or M, bytes == CATALOGUE_PINS pin) → ALL_REPLACEMENTS (L159; member must be `M` with a `beforeGitBlob`, L182–203) → SCIENCE_PACKS prefix + pin → PATHWAY_PARENTS (L36–38; `A` + pin) → `explicit_cover_paths` (L295–309: 97 manifest-bound paths under COVER, additions only, label edits excepted; inputs pin-checked, BOUND_INPUTS L42–47) → else L396 `original GLV3 protected-path fence rejected`. `verify_humanities()` L312–326 additionally reruns the shared validator: `existing_routes_preserved != 30` is red (L434–435: the 30 SOURCE_MANIFEST retained routes must reject modification). Precedent for a new class: L18 — a new protected navigation page matched none of the routes, a fifth transaction was UNCONSTRUCTIBLE (an addition has no beforeGitBlob), closed by ruling Option 2 (PATHWAY_PARENTS: addition-only, pin-checked, modelled on the cover set); Options 1 (changing what SHELVES means) and 3 (general weakening) refused. L16: read the contract, not the pattern.

| file class | count | today's verdict (line) | proposed route | precedent |
|---|---:|---|---|---|
| new files under `Humanities_Teesside/2026-27/**` (lesson-dir 1,074 + 4 term indexes + records) | ≈1,080 | `A` under PROTECTED, no branch matches → L396 rejected | **new addition-only, manifest-bound route** (the "Humanities cover precedent"): a fixed prefix constant (`Humanities_Teesside/2026-27`) + a manifest of exact paths with sha256, the manifest itself in CATALOGUE_PINS (BOUND_INPUTS shape L42–47); judge: status `A`, file exists, sha256 == manifest; self-test red-proves (a) a protected addition not in the manifest, (b) a manifest sha mismatch, (c) an `M` on a manifest path. A literal tuple (PATHWAY_PARENTS shape) does not scale to ≈1,080 paths | L18 Option 2; explicit_cover_paths L295–309 |
| new files under `RE_Teesside/**` (588 + 2 indexes + records + index.html) | ≈595 | **unprotected** (absent from L22–24; directory does not exist; 0 registry entries; 0 rows; 0 PIN1 lines) → judge drops them (L356–358) | no GLV3 judgement at all; the only fences are the admission registry and the catalogue contract. RULING: add `RE_Teesside` to PROTECTED and its index to SHELVES (a `_glv3/**` edit) so the new subject is fenced like Science/Humanities | Science_Teesside protected; L3-class blindness if left |
| `Humanities_Teesside/index.html` (M: lists +78 lessons) | 1 | SHELVES L373–375 | re-pin through pin_catalogue_contract (visible_body_sha256 L1811) | 3b shelf re-cut |
| redirect stubs on PROTECTED paths (`M`) | **101**: Grow/Slideshows 8 · Launch/Slideshows 9 (8 v4 + `LAUNCH_HUM_W9_…Classic`, row [770]) · Humanities_Teesside/Teaching_Packs html 41 (HTML 15 + Resources 15 + per-pathway index/Pupil_Resources/Teacher_Notes 9 + hub index/web-slides 2) · Humanities_Teesside root SoW ×3 + Pathway_Tracker + humanities_teesside.html + `LAUNCH_W9-W14_2026-27/SCHEME_OF_WORK.html` 6 · RE-strand `*_W1-W8_2026-27` lessons 22 · b2 classics under Humanities_Teesside 5 · David cover BR/GR W3–W7 10 | `M` on a protected path → only ALL_REPLACEMENTS admits it | **declared replacement transaction(s)**: REVIEW_BASE + `{path: {beforeGitBlob, afterSha256, bytes}}` between `# BEGIN/END DECLARED TRANSACTIONS` (L96–133) and the ENTRIES markers (L140–153), written by an admission tool (precedents named at L55–57, L83–84: `tools/build_resources/admit_sx3_release.py`); each member in REVIEWED_PATHS so CATALOGUE_PINS carries afterSha256 (L201–202); `beforeGitBlob` from `git ls-tree` at the merge-base of REVIEW_BASE (L167–179, L195–196); the diff must contain EXACTLY the transaction's members (L187–188) → PR-3's protected diff is the members and nothing else | SX3 REPLACEMENT_TRANSACTIONS L138–154 |
| redirect stubs on UNPROTECTED paths (`M`) | **8**: Build/Slideshows BUILD_HUM_W1–W8 | not judged by GLV3 | cross-estate boundary only: every M/R/D must be in ALLOWED_DIFF ∪ CANONICAL_HASHES ∪ CATALOGUE_PINS.files ∪ CATALOGUE_RECORD_PATHS (verify_cross_estate_unification.py L1128–1139, L1391–1409; additions deliberately invisible L1393–1398) → pin each stub | STOP-ADM (boundary = pins) |
| Estate_v3 copies (`BUILD/GROW/LAUNCH_Estate_v3/Humanities_Teesside/*.html`, 27 rows [539]–[551],[578]–[601],[635],[639]; 18 carry glv3- ids) | 27 rows / 9 protected + 18 unprotected files | not R4-named | **leave untouched**: `glv3-verify.yml` L61–70 asserts `len(html)==94`, 88 glv3- rows, 80 lessons, 34 grow / 46 launch — removing rows or stubbing files reds it → ruling if Matt wants them retired | glv3-verify generated-tree step |

**Two collisions that need a ruling before PR-3 can be constructed.** (A) The 30 retained routes (`tools/humanities_resources/SOURCE_MANIFEST.json` existing_routes = 20 of the 22 RE-strand `*_W1-W8` lessons + the 10 David cover BR/GR pages) must reject modification (L312–326, L434–435), yet R4 orders exactly those surfaces stubbed ("any existing RE Autumn lesson serving a covered cell"; every RE Autumn cell has an incoming lesson). Stubbing any of the 30 turns `existing_routes_preserved` to 29 → red. Either the validator/manifest is amended by ruling (a `_glv3` + SOURCE_MANIFEST change, red-proved) or the 30 are left as live routes beside the new lessons (R1 "one truth per cell" then holds only in the catalogue). (B) The David cover BR/GR stubs: the cover route admits `M` only for label_paths (L385–387); a declared transaction is checked earlier (L376) so it takes precedence, but `replacement_errors` runs for every transaction with a member in the diff and the cover inputs are pin-checked (L401–404) — the two mechanisms are both exercised on the same 10 files; the self-test must prove they do not contradict.

**When the judge actually runs.** Only `glv3-verify.yml`, on pull_request/push whose paths match `GROW_Estate_v3/**, LAUNCH_Estate_v3/**, resources.json, _finish/ROUTES.md, _glv3/**, .github/workflows/glv3-verify.yml` (L9–24), and only when `GITHUB_REF_NAME != main` (L125–130). A PR touching only `Humanities_Teesside/**` + `RE_Teesside/**` **never fires it** (L3-class: a gate blind to the thing it fences). Proposal: PR-0 declares the route + the FULL landing manifest (the pack bytes are final after B0, so every sha256 is known upfront) + its pin + PIN1 widening; each content PR's verdict is then measured LOCALLY against `--base origin/main` before push and recorded in the PR body (L17 precedent: commit first, then measure); to close the blindness for good, widen `glv3-verify.yml` paths to the two new trees — a CI edit outside "pin moves under existing precedent" → **Matt's ruling** (STOP-ADM's broad-caller question is the same class). The cross-estate gate fires only on PIN1 paths (Humanities 27 lines today) or via `cross-estate-on-content.yml` (`Science_Teesside/**` only, L13–14); the pinned manifest becomes a PIN1 trigger, so PR-0 and PR-4 fire it; the content PRs do not unless the caller is widened (same ruling).

**Stub shape (R4 "live routes are never deleted", "printed QR codes must keep working").** No stub exists in Lessons today (0 `http-equiv=refresh` files, scope `git ls-files`); the house pattern is the Site's `domain-split/build_education.py moved_page()` L170–186 (≤2 KB, noindex, canonical, ONE link, JS carries `?query`/`#hash`; checker L223–225 one-link rule) — `partb_scratch/LANE4_RETIRE_CENSUS.md`. Target: the cell's new Lesson.html, or the term index where no 1:1 cell exists. Each stub is one transaction member with `afterSha256` + `bytes`, and one registry pair (§4).

### Critique — re-measured, corrections to carry

Judge citations confirmed at the stated lines (PROTECTED L22–24, SHELVES L25, PATHWAY_PARENTS L36–38, BOUND_INPUTS L42–47, admission-tool precedents L55–57 and L83–84, DECLARED TRANSACTIONS L96–133, ENTRIES L140–153, ALL_REPLACEMENTS L159, `git_before_entries` L167, `replacement_errors` L182–203, `protected()` L282–283, `explicit_cover_paths` L295–309, `verify_humanities` L312–326 with `existing_routes_preserved != 30` at L321, `judge()` L355–409, route branches L372–396, cover-input pins L401–404, `git_changes` L412–421, self-test L434–435). glv3-verify.yml paths L9–24, generated-tree asserts L61–70 (94 html / 88 glv3- / 80 lessons / 34 grow / 46 launch), `GITHUB_REF_NAME != main` L125–130; cross-estate-on-content.yml `Science_Teesside/**` only (L13–14). 0 `http-equiv="refresh"` files (scope: `git grep` over *.html). Estate_v3 Humanities html 9/9/9.

**Collision A is mis-described — the 30 retained routes are not what the draft says.** Measured from `tools/humanities_resources/SOURCE_MANIFEST.json` (25 records, `records[*].existing_routes`): 30 distinct paths, ALL under `Humanities_Teesside/{BUILD,GROW,LAUNCH}_W1-W8_2026-27/` (10 each), **0 under David_Cover_Autumn1_W3-W7**. They are 15 `*_HUM_W3..W7_*` Migration & Identity lessons (e.g. `BUILD_HUM_W3_Places_In_My_Community.html`, `GROW_HUM_W5_Was_It_Significant.html`, `LAUNCH_HUM_W7_Source_Based_Assessment.html`) + 15 `*_Humanities_W3..W7_*` RE-strand lessons (e.g. `BUILD_Humanities_W3_Listen_to_Ruth…`, `LAUNCH_Humanities_W7_Belief_Identity_Assessment.html`). So (a) the David cover BR/GR pages are NOT retained routes and collision B ("two mechanisms on the same 10 files") does not arise from the validator; (b) 15 of the retained routes are HUMANITIES lessons serving covered Autumn 1 W3–W7 cells that match NO R4 family (not v4 slideshows, not Teaching_Packs, not b2_*, not SoW/tracker, not RE) — the draft's §5 does not list them at all (see §5). (c) The RE-strand count "20 of the 22" is wrong: 15 of the 22 are retained (the W1/W2/W8 seven are not).

**"Checker L223–225 one-link rule" is a wrong citation** (carried from partb_scratch/LANE4_RETIRE_CENSUS.md): build_education.py L223–225 is the nav-label replace loop (`('games, lessons','lessons')…`). The play-link check is `check_education_separation.py` L61 (`if tag=='a' and attrs.get('id')=='play-game'`), and `moved_page()` L170–186 is confirmed. Note the house stub is a GAMES stub (`data-game-moved`, canonical → PLAY); a Lessons stub needs its own marker or the admission control `stub marker cannot approve code` (check_education_publication_admission.py L52) must be re-read for it.

**PR-0 is a CI edit beyond pin moves.** PR-0 as drafted edits `_glv3/**` (new route) AND the PIN1 block (generated) AND proposes widening `glv3-verify.yml`/`cross-estate-on-content.yml` paths. Only the PIN1 widening has a generated-edit precedent (3b); the path widening is a hand CI edit outside "pin moves under existing precedent" and must be a STOP with the two options, not a PR-0 line item. The draft puts it in §7 item 5 but also inside PR-0's content — remove it from PR-0.

---

## 4. Admission registry — digests, pairs, the retained fence, Site PR, carrier bump, Apps companion

### Draft (lanes, at carrier worktree 0248ea78 / Site 1e98bec0)

**Today (scope: `/home/user/mattroper1977.github.io/domain-split/education-publication-admission.json`, `trees['education-lessons']`).** 3,726 entries = 3,669 single digests + 57 `[previous, current]` pairs (ext mix html 1,506, pdf 773, docx 415, pptx 246, md 124, json 114, zip 113, svg 112, txt 91, png 80, js 56, css 35, xlsx 32, jpg 11, csv 7, webp 6, mp4 3 …); under `Humanities_Teesside/` 498 (= every tracked file there: Teaching_Packs 245, David_Cover 97, Lundy 27, the nine `*_W*_2026-27` trees 121, index 1, SoW/Tracker/Printable 7); under `Humanities_Teesside/2026-27/` 0; under `RE_Teesside/` 0. education-site 203 (46 pairs); education-apps 107 (7 pairs).

**The verify code that every landed file must satisfy** (`domain-split/education_publication_admission.py` L112–126 `verify_tree_census`: UNREVIEWED for a path not in the registry, MISSING for a registered path absent unless `may_be_absent`, CHANGED when the digest is not in `admitted(expected)`; `census()` L37–56 hashes EVERY file; `validate_digest_set` L78–95: 1–2 distinct digests, an ARRIVING marker beside exactly one digest, never a third). `build_education.py` L342–343 calls it, so the BUILDER fails on any UNREVIEWED/MISSING/CHANGED; `education-publication.yml` runs the builder (L79) then `check_education_publication_admission.py --build-control` (L88), whose controls plant an unlisted file, a changed .js, a missing index.html and disguised .png/.pdf/.pptx and require each to FAIL (L49–76, L135–138).

**New single digests (derived from §1; each variant labelled):**

| variant | lesson-dir | indexes | SoW (html+docx) | records | RE index | total new singles |
|---|---:|---:|---:|---:|---:|---:|
| everything, records in a public dir | 1,662 | 6 | 4 | 4 | 1 | **1,677** |
| everything, literal `_records/` (unpublished) | 1,662 | 6 | 4 | 0 | 1 | 1,673 |
| R9 step fires (no mp4) | 1,542 | 6 | 4 | 4 | 1 | 1,557 |
| no mp4, per-lesson Sources_and_checks deduped | 1,436 | 6 | 4 | 4 | 1 | 1,451 |

Plus, if ruled in: SoW xlsx 2, Fallback Editable_Visuals 13, MANIFEST/READ_ME 2. Registry after landing ≈ 3,726 + 1,677 = 5,403 entries; the digest of an html entry is of the BUILT bytes (navigation adapter, build_education.py L276–280), so the build must use the builder at the SHA the carrier will pin (STOP-G2 precedent: "the exact transform the Education Pages publication applies", build_education.py at f70f4973).

**`[previous, current]` pairs — only for paths that already exist and whose bytes move (a new path has no previous):** 109 stubs (or 98 if the 11 Teaching_Packs navigation pages are left) + `Humanities_Teesside/index.html` + `resources.json` + `assets/catalogue/lesson-order.json` + `data/resource-sizes.json` + `assets/catalogue/humanities-shelf.json` (public by L85–91 if published; not separately measured) + `data/companion-packs.json` only if the 17 pack rows are ruled out → **≈114 Lessons pairs**; Site tree: `data/domain-catalogue.json`, `data/resource-discovery.json` (L23) → 2 pairs. Pairs 57 → ≈171. The precedent wording (L68–73): "exactly two reviewed digests, the byte-state on the owning repository's main today and the reviewed byte-state its pending PR will land".

**ARRIVING vs single (the choice fixes the PR order).** `[digest, 'ARRIVING']` (L82–87, L100–106): "a file the owning repository's main now carries but this repository's own pinned source checkout predates … never CHANGED, never UNREVIEWED; a build that has it must match the one digest exactly". Precedents: HC5 sect.1 (142 Teaching_Packs paths) and RX3 P3 (24 ADD-BESIDE lessons) used ARRIVING when the Lessons pin did not move; Site #410 (5bd7702b) admitted the three Science START_HERE pages as plain singles because the same PR moved both Lessons pins (registry diff L104–106). Proposal (§6): ONE admitting Site PR with ARRIVING singles + pairs BEFORE any Lessons content merge (so no intermediate Lessons main is UNREVIEWED — every intermediate state is a subset the markers tolerate), then ONE closing Site PR that collapses ARRIVING/pairs to singles and moves both Lessons pins to the final Lessons main (precedent #412: "13 literal Lessons pins found (not six)", `lessons_pin_lag_control.py`).

**The granted build (L23b).** Digests come from a build taken AFTER the last regeneration on the full stack head (resource_sizes --write, lesson-order derive, evidence, unit_tags, companion, display titles, spine, STATIC_CHECK_RESULTS) — the 3b defect was seven registry entries taken before `resource_sizes.py --write` ("CHANGED education-lessons/data/resource-sizes.json" on 124f513b). Any Class B ruling that changes bytes after that build invalidates it (§7).

**The retained fence (`domain-split/check_education_separation.py` L146 `baseline_sha = 'd0dc6b3e…'`, L154–161).** `registry_partition()` (L91–104) removes every row under an approved Teaching_Packs prefix and freezes the sha256 of the rest (indent=2). `usage_discovery.py` L111–113 adds every `type=='lesson'` resources.json row and L116–121 every humanities-shelf.json lesson → 120 new lesson rows JOIN the retained set, R4's removed rows LEAVE it, retitled rows CHANGE it → `Installed combined registry records changed` until re-frozen. "Retained fence untouched" can therefore only mean the MECHANISM is untouched: the literal moves once, in the closing Site PR with a `registry_partition()` diff proof (precedent #408 0cd8f842 L136–145: "977 -> 977 retained rows, 0 joined, 0 removed, and 17 existing records change in exactly ONE field"), with the dated comment block `tools/census_typed_literals.py` requires (docstring L26–31, SCAN_EXT L94). The fence is single-valued and the two Site Lessons pins are HELD EQUAL for that reason (`domain-split-verify.yml` L30–42), so the re-freeze travels with the pin move, never before it. The Site-side check runs against the Site's pinned Lessons source, so it stays green through the Lessons merges.

**Site PR contents (admit):** registry rows (ARRIVING singles + pairs); no pin move; `resource_sizes.py` identity kept (s1m cmp). **Site PR contents (close):** collapse to singles; both Lessons pins (`education-publication.yml` L56, `domain-split-verify.yml` L62; 124f513b at research time, moved to b32bf1c7 by #412) → the final Lessons main; `baseline_sha` re-freeze with proof. `domain-split-verify.yml` is blind to `education-publication.yml` changes (L3) → manual `workflow_dispatch` as on #409.

**Carrier bump + caller digest (L23 "THE CARRIER COST").** `education-pages.yml` (Lessons) pins the Site builder by SHA, so each Site registry change costs a Lessons commit moving that pin and a re-cut of the caller digest `sha256(.github/workflows/education-pages.yml)` == `PUBLICATION_CALLER_SHA256_BY_KIND['lessons']` (gate L789; 16448b91 today, LANE2) in BOTH gate copies. Precedent: Lessons #594 b32bf1c7 "carrier re-cut", after Site #411; "Two PRs and a companion to admit one moved byte". Two carrier bumps are implied by the two Site PRs.

**Apps companion.** The gate copy must be byte-identical across estates: Lessons origin/main 6bd51afc == Apps origin/main 85f7e07f 6bd51afc (LANE2_MEASUREMENTS.txt; the PUBLISHED control pair moves both to f38a2a6f when it lands, ledger tail); `pin_catalogue_contract.py --lessons --apps` writes both copies or neither (L1838–1844) and refuses when they differ (L1795–1796); neither CI gate holds the copies identical (RELEASE_LEDGER.md Backlog) — the pin tool's `--check` is the control. Live-state rule as this lane reads it (the phrase is defined in no record read here): the companion is cut against Apps ORIGIN/MAIN re-fetched at the time of cutting, never the stale local checkout `/home/user/matt-s-apps-` 6df9e943 (2 lines differ from origin/main; not at the workflow's Apps pin dfca094b) — lane 1's "byte-identity could not be confirmed" was a stale-checkout reading. Precedent: Apps #117 85f7e07f companion to Lessons #594; Apps main "Made by Matt cross-estate unification" FAILURE on push = the STOP-P1 live-proof routes, expected.

### Critique — re-measured, corrections to carry

Registry counts reproduce at Site 1e98bec0: education-lessons 3,726 = 3,669 singles + 57 lists (0 ARRIVING); ext mix html 1,506 / pdf 773 / docx 415 / pptx 246 / md 124 / json 114 / zip 113 / svg 112 / txt 91 / png 80 / js 56 / css 35 / xlsx 32 / jpg 11 / csv 7 / webp 6 / mp4 3; Humanities_Teesside/ 498 (Teaching_Packs 245, David_Cover 97), Humanities_Teesside/2026-27/ 0, RE_Teesside/ 0; Build/Grow/Launch Slideshows 30/17/19; education-site 203 (46 lists, 3 ARRIVING); education-apps 107 (7 lists); `data/resource-sizes.json` = [8141fb82…, abd0a1ba…]. Admission code confirmed: REVIEWED/INERT L15–19, `census` L37, `validate_digest_set` L78–82, `verify_tree_census` L112–118, Unclassified L49–50; separation `baseline_sha` L146, `registry_partition` L91; usage_discovery L111–121.

**Wrong line numbers / paths (Site at 1e98bec0):** the Lessons pin in `education-publication.yml` is **L63** (`b32bf1c7…`), not L56; the builder runs at **L85–86** (`build_publications.py`, `build_education.py --lessons … --apps …`), not L79; `check_education_publication_admission.py` runs at **L95**, not L88; `domain-split-verify.yml` Lessons pin is **L69** (comment block L30–44 confirmed), not L62; the lag tool is **`tools/lessons_pin_lag_control.py`**, not `domain-split/…`; `domain-split/resource_sizes.py` is **not found** at Site HEAD (scope: `git ls-files`), so the s1m `cmp` (Lessons s1m L69–70) targets a `publisher/` checkout at whatever ref that workflow pins — name it. Note: the current Site comment at education-publication.yml L57–61 already describes b32bf1c7 as "2 commits behind" 545d9e8b, and Lessons main has since moved to cbfbc70c (#595): the "held EQUAL" invariant is now 3+ commits out, before Part B adds ~25 more — the closing pin move is mandatory, not optional.

**Stale estate state:** "Lessons origin/main 6bd51afc == Apps origin/main 85f7e07f" is pre-#595/#118; both gate copies are f38a2a6f at origin/main (derived by `git show origin/main:… | sha256sum` in each checkout); Apps main is bbce3771. The local Apps checkout 6df9e94 still differs from Lessons at L789 only (caller digest 6f04f0b1 vs 16448b91), consistent with "stale checkout". Any companion is cut from Apps origin/main after a fetch — the draft says so; keep it.

**Pair count needs the R4 gap closed.** The draft's ≈114 pairs assume 109 stubs; §5's unclassified 21 `*_HUM_*` W1-W8 lessons, the 2 `classic-33-*` rows [763]/[768] and the 4 START_HERE pages in the W1-W8 dirs all become pairs if stubbed — the pair count is a ruling output, not a plan input. Registry after landing ≈ 3,726 + new singles (1,677 max) — note the mp4 branch: with R9's pre-ruled step the 120 mp4 never enter the registry (1,557 max).

---

## 5. Retire list (R4) with redirect stubs and QR routes; taught-now protection (R5)

### Draft (lanes, at carrier worktree 0248ea78 / Site 1e98bec0)

**R4 families, measured (scope: `git ls-files` at 0248ea78; `partb_scratch/existing_humanities_teesside_files.txt`, `resources_humanities_rows.jsonl`, `LANE4_RETIRE_CENSUS.md`).** Every retired surface becomes a stub (route kept, R4) → one transaction member / pin / registry pair; its catalogue row is removed (R4) → contract arithmetic in §2.

| family (R4 words) | surfaces found | rows | protected? | stub target | notes |
|---|---:|---|---|---|---|
| (a) "the 24 Migration & Identity v4 slideshows" | 24: `Build/Slideshows/BUILD_HUM_W1_Human_Timeline … W8_Where_In_The_World.html` (8), `Grow/Slideshows/GROW_HUM_W1_Time_Detectives … W8` (8), `Launch/Slideshows/LAUNCH_HUM_W1_Source_Investigation … W8_OS_Map_Skills.html` (8) | [182]–[205] (`build|grow|launch-hum-aut1-w1..w8`, in the frozen 734) | Grow/ Launch/ yes; Build/ **no** | cell's new lesson (W1–W7 → Autumn_1 W01–W07; W8 → Autumn_2 W01 per LANE4's C53 reading) — exact map from P0 CELL_MAP | registry: Build/Slideshows 30 html entries, Grow 17, Launch 19 |
| (b) "the HC5 Humanities W3–W7 Teaching_Packs" | 41 html: `Humanities_Teesside/Teaching_Packs/{BUILD,GROW,LAUNCH}/HTML/<P>_Humanities_W3..W7.html` 15 + `Resources/…` 15 + per-pathway index/Pupil_Resources/Teacher_Notes 9 + `Teaching_Packs/index.html`, `web-slides.html` 2 (245 registry entries under the prefix; 114,632,552 B; W3–W7 payload 90 files) | [737]–[739] hubs (shelf); 17 pack rows [838]–[843],[859]–[863],[877]–[882] are Week_9–14 (Autumn 2), NOT W3–W7 | yes | the 30 lesson pages → cell's new lesson; the 11 navigation pages → term index — but they also list the Week_9–14 downloads (not R4-named) → RULING: stub 30 or 41 | downloads (pdf/pptx/zip) are not surfaces; left |
| (c) "any b2_* humanities lesson serving a covered cell" | 0 files named `b2_*` (scope: `git ls-files` `(^|/)b2_` → only `_sownb/vb/evidence/a3n/b2_*.json`); the `classic-33-b2-*` rows point at 6 classics: `Humanities_Teesside/BUILD_W14-W20_2026-27/BUILD_HUM_W12_A_celebration_in_order_Classic.html`, `…/BUILD_HUM_W14_A_fair_chance_to_join_in_Classic.html`, `Humanities_Teesside/GROW_W9-W14_2026-27/GROW_HUM_W13_Compare_celebrations_with_care_Classic.html`, `…/GROW_HUM_W12_Festival_lights_across_places_Classic.html`, `Humanities_Teesside/LAUNCH_W9-W14_2026-27/LAUNCH_HUM_W11_A_growing_town_an_urbanising_region_Classic.html`, `Launch/Slideshows/LAUNCH_HUM_W9_Find_it_with_a_grid_reference_Classic.html` | [764]–[767],[769],[770] (shelf; halfTerm Autumn 2) | 5 yes + 1 (Launch/Slideshows) yes | Autumn_2 cell's new lesson (week map per `_sownb/TERM_DATES.md` rule Aut2 Wn → 8+n, LANE4) | the other 36 existing html in the `*_W9-W14` / `*_W14-W20` / `*_W15-W20` dirs (41 html − 5 classics) serve covered Autumn 2 / Spring cells and are named by no R4 family → P0 CELL_MAP must classify them; ruling |
| (d) "the old SoW + tracker pages" | 6: `Humanities_Teesside/BUILD_Scheme_of_Work.html`, `GROW_…`, `LAUNCH_…`, `Pathway_Tracker.html`, `humanities_teesside.html` (title "Humanities — Teesside Migration & Identity"), `LAUNCH_W9-W14_2026-27/SCHEME_OF_WORK.html` (no row) | [231],[233],[235],[363],[230] (frozen 734) | yes | the new Humanities SoW / term index | RE SoW pre-existing: not found (scope: `git ls-files -i` scheme_of_work|sow|tracker); 3 `*_Printable_Pack.html` adjacent, not named |
| (e) "any existing RE Autumn lesson serving a covered cell" | RE-strand lessons in `*_W1-W8_2026-27/`: 22 (BUILD 8 incl. `BUILD_HUM_W2_A_Special_Book…` [688] and `BUILD_HUM_W8_A_Festival_Of_Light`; GROW 7 incl. [684],[685]; LAUNCH 7 incl. [686],[687]) of which 21 carry RE cell refs C60–C66 / C200–C206 (LANE4) + David cover `BR_W3..W7`, `GR_W3..W7` 10 html (+ downloads and 3 `*_RE_Pack.zip`, left) | 5 lesson rows + [736] cover hub | yes; **30 of them are SOURCE_MANIFEST retained routes** (§3 collision A) | `RE_Teesside/2026-27/<P>/Autumn_1/W0n/` lesson | Autumn 2 RE-flavoured classics are (c)'s [764],[766],[767]; no tracked file is named `RE_*` |

Totals (lane-1 basis): **109 stubs** (101 protected + 8 unprotected); rows removed 29 (frozen) + 10 (shelf) = 39, 17 pack rows pending ruling. "An existing lesson serving a cell with NO incoming lesson is left alone": the Summer cells (39) and everything outside the five families.

**QR routes (R4 "printed QR codes must keep working").** No QR-encoded route was found in Humanities surfaces (HTML 0, PDF text 0, docx 3 = "No … QR code … is required" disclaimers; LANE4). Live Teach QR (`tools/liveteach/qr_source.js`) encodes the lesson's OWN address and 59 Humanities pages load `hud.js`, so a printed QR resolves to the old route → the stub at that route (200, one link, `?query`/`#hash` carried by JS per `moved_page()` L170–186) is what keeps it working. P6 must GET each of the 109 stubbed routes on the served origin (raw-at-SHA vs live) — origin is 403 from this container, so that proof is CI's or Matt's phone's (§0).

**R5 taught-now protection.** Rule: Aut1 W3 = w/c 14 Sep; per subject and pathway, the cell taught in the run week and the following week are swapped LAST and only after STOP S2. Measured (LANE4; `data/calendar-spine.json` weekStarts 3 = 2026-09-14, 4 = 2026-09-21): at a 2026-09-19/20 run the pairs are Humanities {BUILD, GROW, LAUNCH} Autumn_1 W03+W04 and RE {BUILD, GROW, LAUNCH} Autumn_1 W03+W04 = **12 cells**. Existing surfaces for them (from `partb_scratch/existing_lessons_meta.tsv`; BUILD shown, GROW/LAUNCH per CELL_MAP): `BUILD_HUM_W3_Places_In_My_Community.html` (C48), `BUILD_HUM_W4_Then_And_Now.html` (C49), `BUILD_Humanities_W3_Listen_to_Ruth…` (C62), `BUILD_Humanities_W4_Show_Respect…` (C63), plus the David cover `BR_W3/W4`, `GR_W3/W4` and the v4 W3/W4 slideshows. The pair MOVES with the run date: if Part B runs in w/c 28 Sep it is W05+W06. Sequence (order P6/S2 text, literal): the 12 cells' stub commits are the LAST commits added to PR-3 after Matt's "go" at S2, then merge in R10 order; alternative reading ("swapped LAST" = merged last of all, a PR-3b after PR-4) is Matt's choice (§7). The 12 cells' NEW lessons are additions and land with their content PRs either way; only the old route's flip is held.

### Critique — re-measured, corrections to carry

Family file counts reproduce (scope: `git ls-files` at 0248ea78): v4 slideshows 8/8/8 HUM in Build/Grow/Launch Slideshows (+`LAUNCH_HUM_W9_…Classic`, row [770]); Teaching_Packs 41 html of 245 files / 114,632,552 B, 30 of them `W3..W7.html`; SoW/tracker set as listed (+3 `*_Printable_Pack.html`); David cover BR/GR W3–W7 10 html of 26; b2: only 2 tracked `(^|/)b2_` entries (JSON evidence), the 6 `classic-33-b2-*-humanities-*` rows [764]–[767],[769],[770] resolve to the 6 files named; 41 html in `*_W9-W14/W14-W20/W15-W20`, 5 of them Classic; calendar-spine weekStarts 3 = 2026-09-14, 4 = 2026-09-21.

**Missing population — the `*_W1-W8_2026-27` trees.** 51 tracked html there (17 per pathway): 22 RE-strand (the draft's (e), correct), 3 `START_HERE.html` (rows [677]–[679]), 1 `START_HERE_GROW_HUMANITIES_W9-W14.html`, 2 classics with rows — `BUILD_HUM_W7_A_place_in_the_group_Classic.html` [763] `classic-33-build-humanities-belonging` and `LAUNCH_HUM_W3_Can_this_record_prove_it_Classic.html` [768] `classic-33-launch-humanities-archive` (Autumn 1 W7 / W3 — covered cells; not `b2`, so not (c)) — and **21 `*_HUM_W1..W8_*` Migration & Identity lessons with no catalogue row** (BUILD W3–W7 ×5; GROW W1 Migration, W2 Reading, W3–W7, W8 ×8; LAUNCH W1 Migration, W2 Cause, W3–W7, W8 ×8). All 21 serve covered Autumn 1/2 cells (C46–C53 per LANE4), 15 of them are the SOURCE_MANIFEST retained routes (§3), and none is named by an R4 family. The draft's "the other 36 existing html … named by no R4 family" must become "36 + 21 + 2 + 4"; the stub total 109 and the row removals 39 are therefore lower bounds pending the CELL_MAP ruling. The "left alone" sentence of R4 does not cover them (their cells HAVE incoming lessons).

**Collision B removed:** the David cover BR/GR pages are not retained routes (0 of 30), so stubbing them is a plain ALL_REPLACEMENTS transaction plus the label-path cover rule (L385–387) — but the cover route admits only label edits, so a `M` that turns `BR_W3.html` into a stub must be a declared transaction member; that part of the draft holds.

**R5:** 12 cells at a w/c 14 Sep run reproduces from weekStarts; today is Sunday 2026-09-20 (still w/c 14 Sep), so W03+W04 holds only if the merges happen before Monday 21 Sep — state the rule as "pair = weekStarts[n] ≤ merge date < weekStarts[n+1]" and re-derive at S2.

**QR:** the draft's "P6 must GET each of the 109 stubbed routes" is right but uncounted against the order — P6 names external URLs only; served-route proof is S2's "raw-at-SHA vs live". Put the stub-route GETs under S2.

---

## 6. Sequence of PRs, read budgets, one merge at a time, main-push observation, served proof, PASS-style close

### Draft (lanes, at carrier worktree 0248ea78 / Site 1e98bec0)

**Proposal: ≤12 lessons per content PR (science precedent: six content branches, `sx3-build-1` carried "the 12 landing decks of one branch", STOP-ADM), one source pack per PR where it fits, R10 order kept.** Every content PR carries its own admission (STOP-ADM: "A content PR without its pins is red by construction") — here: the lesson bytes + the local judge verdict against the PR-0 manifest (§3) + `check_catalogue_static` bare + the UX2 `--check`s (no rows change until PR-4, so the four writers' `--check` is a no-op proof, recorded).

| PR | content | lessons | files | bytes | notes |
|---|---|---:|---:|---:|---|
| PR-0 | GLV3 route + full landing manifest + pin (both gate copies) + PIN1 widening + self-test red proofs; STATIC_CHECK_RESULTS regen | 0 | — | — | fires glv3-verify (`_glv3/**`) with 0 protected changes → PASS by construction, red-proved by self-test; fires cross-estate (pinned path) |
| PR-1a | HUM BUILD Autumn_1 (Fallback) | 7 | 56 | 9,845,926 | R13 generation in PR body |
| PR-1b | HUM GROW Autumn_1 (Fallback) | 7 | 56 | 6,775,427 | |
| PR-1c | HUM LAUNCH Autumn_1 | 7 | 91 | 11,601,782 | |
| PR-1d | HUM BUILD Autumn_2 | 7 | 115 | 12,460,504 | |
| PR-1e | HUM GROW Autumn_2 | 7 | 105 | 17,651,000 | |
| PR-1f | HUM LAUNCH Autumn_2 | 7 | 109 | 25,249,846 | largest |
| PR-1g | HUM BUILD+GROW Spring_1 | 12 | 178 | 24,634,453 | one pack |
| PR-1h | HUM LAUNCH Spring_1 | 6 | 78 | 10,965,127 | |
| PR-1i | HUM BUILD+GROW Spring_2 | 12 | 188 | 26,849,295 | one pack |
| PR-1j | HUM LAUNCH Spring_2 | 6 | 98 | 17,201,825 | |
| PR-2a…2f | RE BUILD A1 · BUILD A2 · GROW A1 · GROW A2 · LAUNCH A1 · LAUNCH A2 | 7 each = 42 | 98 each = 588 | 11,077,843 · 10,468,093 · 11,715,282 · 10,501,872 · 12,106,790 · 11,495,459 | unprotected tree (§3) |
| PR-3 | 109 stubs = 1–2 declared transactions + 8 unprotected pins; the 12 taught-now stubs as the final commits after S2 (§5) | — | 109 | ≤2 KB each | protected diff == transaction members exactly |
| PR-4 | catalogue (+129 −39 rows, contract re-cut), hub(s), 6 term indexes, records, 2 SoW html + 2 docx, humanities-shelf, lesson-order, resource-sizes, evidence, unit tags, PIN1, STATIC_CHECK_RESULTS | — | ≈ 20 + derived | — | the four writers + census tail (§2); fires glv3-verify (resources.json) and cross-estate |

Sums: Humanities 78 lessons / 1,074 files / 163,235,185 B over 10 PRs; RE 42 / 588 / 67,365,339 B over 6 PRs; Lessons PRs = 1 + 10 + 6 + 1 + 1 = **19**. Alternative A: one PR per term-dir (12 + 6 = 18 content PRs, all ≤7 lessons). Alternative B: R10 literal (PR-1 = 78 lessons / 1,074 files, PR-2 = 42 / 588) — no precedent for a >12-lesson content PR; read budget is per head, so fewer heads but each red costs the whole batch. Matt chooses. Known window: between a term's content merges and PR-4, the 240 rewritten `START_HERE` links dangle (index lands in PR-4 per R10); alternative: each term index rides with the last content PR of its term (ruling).

**Estate sequence (from §4; precedent SEQUENCE STATE: Site #411 → Lessons carrier #594 → Apps #117):**
1. B0 → P0 → STOP S1 → P1 → stack PR-0…PR-4 on `claude/hum-d5-landing` (stacked PRs, CI per head) → P6 gates on the stack head (120 lessons, both transports, 1280×720 + 390×844; contact sheet committed) → **STOP S2** → "go" → taught-now commits → all writers → **granted build** at the stack head (L23b).
2. Site-ADMIT PR: ≈1,677 ARRIVING singles + ≈116 pairs; no pin move → merge → Site main-push observation.
3. Lessons CARRIER-1: education-pages.yml → Site-ADMIT SHA; caller digest re-cut (both gate copies) → merge → observation. Apps COMPANION-1 (gate copy: manifest pin + caller digest; cut from Apps origin/main) → merge → observation.
4. Lessons merges, ONE AT A TIME, R10 order: PR-0, PR-1a…1j, PR-2a…2f, PR-3, PR-4 — after EACH merge a main-push observation table before the next merge is started.
5. Site-CLOSE PR: collapse ARRIVING/pairs to singles; both Lessons pins → the final Lessons main; `baseline_sha` re-freeze with the `registry_partition()` proof → merge → observation (manual dispatch of domain-split-verify, L3).
6. Lessons CARRIER-2 + Apps COMPANION-2 → merges → observations.
7. Served proof → INFLIGHT closed → P7.
PR count ceiling: 19 Lessons + 2 carrier + 2 Site + 2 Apps = **25 heads, 25 merges**.

**Read budgets (ledger practice: "Read counts: Site #411 head 2f36f00b 2/3; Lessons #594 head 0248ea78 1/3").** 3 CI reads per head + 3 per main-push observation → ceiling 25×3 + 25×3 = 150 reads; instrument corrections in force: #7 `get_job_logs` needs `return_content=true` (blob host 403); #8 `actions_list` filters are advisory → filter locally by head_sha; #9 `failed_jobs: 0` is not a pass — completion is a separate fact; #10 tail truncation → the one log read at full depth; L17 a zero-finding gate result must be distinguished from a zero-input one; L22 on a PR a cross-estate red is never STOP-P1 (live-proof runs only on push/dispatch) and must be root-caused.

**Main-push observation table (shape from the ledger, one per merged head):**

| workflow | run | conclusion |
|---|---|---|
| Education Pages publication | <run id> | SUCCESS / FAILURE |
| FieldOps P2, the sweep, and the serve proof | <run id> | … |
| UX2 gates | triggered? (paths) | … |
| Made by Matt cross-estate unification | triggered? (PIN1 paths) | live-proof red = STOP-P1 by attribution only once the PASS 6 control has NOT yet landed; otherwise root-cause |
| GROW LAUNCH v3 generated-tree verification | not triggered on main (L125–130) | — |
| Watch main | observer | reported separately |
Close line per head: "Main green at <sha>: N of N triggered workflows with verdicts, all SUCCESS." A red halts the sequence (STOP-M1 shape: attribution, the failing line, the fix verified but NOT pushed).

**Served proof (order S2: "prove served on main (raw-at-SHA vs live)").** The origin is 403 CONNECT from this container (L10: a local build reproduces the BUILDER, not the SERVED ORIGIN), so the proof is CI's: FieldOps `served` job (precedent "59 served byte-identical · 0 red · 0 inconclusive, of 59 derived"), the Education Pages publication artefact sha256, and the registry-admitted digests == served (precedent: 15 LAUNCH decks + hub 5c4e3ced == registry, 15/15), for: the 120 Lesson.html, the 6 indexes, the 109 stub routes (200 + one link), the 2 SoW pages, `data/resource-sizes.json`. Grant needed for the dispatch + reads (ledger "STOP for a grant (dispatch + reads) before PASS 5").

**PASS-style close.** INFLIGHT.md closed for Part B; token `HUMD5_CLOSED` (or `HUMD5_PARTIAL:<what>`); P7 report: Part A totals (Class A 27 groups / 545 occurrences / 71 lessons + A0028–A0038 applied; Class B B0001–B0130 dispositioned H1–H9; CHECKS table), landed (files, rows), stubbed (109), repo size before/after (three measures, §7), contract amendment proposal (R6), dead links (E10 NOT RUN unless granted), tracker contradictions (R8: list, do not edit), the Fallback 14 rows first in residue (R13), anything held and why.

### Critique — re-measured, corrections to carry

Arithmetic of the PR table is internally consistent with §1's target table (e.g. PR-1g 100 + 78 = 178 files, 14,796,961 + 9,837,492 = 24,634,453 B), but every byte column inherits §1's stale census (packs total now 229,831,832 B; lesson-dir 228,630,296 B) — re-cut after B0.

**Departures from R10 that are not flagged as such.** R10 is four PRs in a fixed order; the draft's 19-PR stack adds PR-0 (a `_glv3/**` + PIN1 edit BEFORE PR-1) and splits PR-1/PR-2 sixteen ways. Splitting is presented as Matt's choice (fine); PR-0's position is not — it changes the order (a fence PR before content) and it is the only PR whose diff touches `.github/workflows/` (PIN1 block). State it as a proposed exception to R10 with the L18 Option-2 precedent, and keep the hand widening of `glv3-verify.yml` paths out of it (§3).

**Source selection is not recorded.** CHASSIS_CONTRACT.md L556 ("Source selection is never filesystem order … duplicates detected by content … a filename carrying two generations must have an explicit ruling … recorded per deck in the ledger") and RELEASE_LEDGER.md L35 (per-deck table: deck | generations | chosen source | sha256 | bytes) apply. The draft maps packs to PRs but has no per-lesson selection table. Three cases need explicit rows: (a) every Final pack's inner folder is `*_Reviewed` (a WITHDRAWN generation name carrying Final content — STATE.md "Generation check" is the evidence, but it is not in the plan); (b) `RE_Autumn_GROW_Final.zip` was uploaded twice, byte-identical (STATE.md A0: md5 2de3d2c9…, 13,460,339 B) — one generation, two copies, must be recorded, not silently deduplicated; (c) the 14 Fallback cells (R13). Add a 120-row table `deck | generations | chosen source path | sha256 | bytes` to P0's output.

**R3 is unaddressed.** State the negative with its scope: 0 donor/earlier archives and 0 `HUM_*_ALL` / non-`_Final` packs present (scope: `ls /tmp/claude-0/humd5/unzipped` = 12 `*_Final|*_Fallback` + `HUM_00_SoW_and_Order`).

**Main-push observation table:** the Watch-main row and the "STOP-P1 by attribution" rule are now stale — the PUBLISHED control pair has MERGED (Lessons #595 cbfbc70c, Apps #118 bbce3771; ledger tail) with 0/3 observation reads. The first Part B observation must first close those two observations (they are the "Lessons main green" precondition), and the cross-estate live-proof line should then read root-cause, not attribution.

**Served proof:** add the 210 RE SoW lesson links and the 2 SoW pages' own routes to the served list; the draft lists 120 Lesson.html + 6 indexes + 109 stubs + 2 SoW + resource-sizes.

**Close:** P7's "Part A totals" must quote HUMD5_PARTA_CLOSE.md §1 (220 / 505 / 175; H2 180; H5+H6 365 in 120 files) rather than the draft's "27 groups / 545 occurrences / 71 lessons" (that is A1's proofread count, STATE.md L114; the applied count is 220 edits).

---

## 7. Risks and open questions for Matt (STOP-B1 list)

### Draft (lanes, at carrier worktree 0248ea78 / Site 1e98bec0)

**R9 — the budget line is breached on every measure BEFORE landing (scope: `git ls-files` at 0248ea78; 2 tracked node_modules entries absent on disk excluded).** All tracked regular files 1,127,172,968 B = 1075.0 MiB; top-level `_*`/`.*` dirs 196.6 MiB; tracked excluding those 878.4 MiB; the `public_file()` set the publisher copies 894,531,940 B = 853.1 MiB (3,900 files, 1,506 html). Projection with all 13 packs (221.0 MiB; the 120 mp4 = 44.4 MiB): all-tracked 1075.0 → 1296.0 (→ 1251.6 without mp4); public set 853.1 → 1074.1 (→ 1029.7); tracked-minus-underscore 878.4 → 1099.4 (→ 1055.0). R9's text then says "STOP before the content PR and report". **Ruling needed: which measure R9 intends, and whether the 950 MB line stands** — as written, Part B cannot reach PR-1a. Never strip the base64 video; never drop another class on my own ruling (R9).

**The Fallback 14 (R13).** No Final pack exists (Fact 2). `generation="fallback-2026-09-19"` cannot be a row key (schema `additionalProperties false`; ADDITIVE_TAG_KEYS = halfTerm/unit) → report + CELL_MAP/RETIRE_LIST + first residue item only. The 14 lack Teacher_Notes.docx, Pupil_Resources.html, Model_Transcript.txt, `#save-independent`, `re_safeguard`; `config.sehm` was inserted into the 7 GROW_A1 configs by H6 (A0038), the 7 BUILD_A1 not stated; E8 safe-area "not measurable" on them; no START_HERE (Autumn_1 index built from LAUNCH's + MANIFEST.json — proposal); `Editable_Visuals/` 13 files uncovered by R2. If a Final pack arrives after landing, "never land both" makes the swap a second release: 14×8 = 112 file replacements (registry pairs) + 14 row edits + re-gates.

**The 8 Teacher_Notes.pdf.** Two records disagree: STATE.md L114 "14 occurrences in 8 Teacher_Notes.pdf whose DOCX is proofed but which this container cannot re-render (LibreOffice loads no DOCX at all)" vs `/tmp/claude-0/humd5/RERENDER.log` "teacher notes converted 8 of 8" with `RERENDER_DOCX.json` listing 8 RE Teacher_Notes.docx (GROW_RE_A2_W02, W03; LAUNCH_RE_A1_W05; LAUNCH_RE_A2_W01, W02, W03, W06, W07) at exit code 0. Which is current is **not measured** here; B0 must settle it (sha256 of the 8 PDFs vs the pre-proof sums; page count). If not re-rendered: either land with 14 Class A residues in the report, or re-render on Matt's machine BEFORE the granted build (bytes → digests).

**Class B rulings (PROOF_LEDGER.md L221+, B0001–B0130 under H1–H9).** H1 by design (KO "Remember" line, 218/218); H2 applied (A0028: 180 HTML + 180 DOCX/PPTX + 180 PDFs; 16 W01 word-help variants held); **H3 STOP-X** — 5 lessons (`H3_TARGETS.json`), ruling requested before any move; H4 report (94 uncredited pupil pictures, `Visual_Resource.png` on disk in 64 lessons referenced by no HTML — land or not?); H5: B0008 closed as instrument artefact, B0123/B0124/B0129/B0127/B0128 applied (A0029–A0037), **B0125 "Matt's call"**, B0126/B0130 re-measured — E6 POST in progress (40/120 in the log); H6: 7 applied (A0038), 12 not derivable; H7 report-only (incl. 29 video durations outside 30–40 s, 59 readability flags, focus-indicator gaps); H8 NOT RUN (E10 57 URLs, E11, E8 OCR — proxy 403 / tesseract absent) → P6's "GET every distinct URL" and R14's Jan Halliday URL check will be NOT RUN again from this container unless granted or done by Matt. Any ruling that changes bytes after the granted build invalidates §4's digests (L23b).

**Pack integrity (B0).** 531/1,613 SHA256SUMS FAIL in the workspace (§0); the order's "any mismatch = STOP". Prove applied == expected against `APPLY_PLAN.json` + `APPLY_PLAN_second_write.json`, regenerate sums after the last write, then census.

**Structural rulings (each blocks a PR):**
1. `_records/` is unpublishable as named (build_education.py L89) — non-underscore name, or unpublished?
2. Review_record ×11 all distinct — merge (authoring) or keep 11? Sources_and_checks: 2 copies + dedupe the 106 per-lesson copies (354 published html) or land all (460)?
3. R4 row removal inside the frozen 734 (29 rows): hand re-cut of ORIGINAL_ROW_COUNT/SHA in pin_catalogue_contract.py L18–19 and both gate copies L673–674 — who rules, red-proof shape, and in PR-4?
4. The 30 retained routes (SOURCE_MANIFEST) vs R4's RE-Autumn stubs (§3 collision A): amend the validator, or leave the 30 live?
5. `RE_Teesside` unfenced: add to PROTECTED + SHELVES (a `_glv3` edit)? And widen `glv3-verify.yml` / `cross-estate-on-content.yml` paths to the two new trees (a CI edit beyond pin moves) — or accept L3-class blindness with local judge runs recorded per PR?
6. Teaching_Packs: stub 30 lesson pages or all 41 (the 11 navigation pages also carry the un-named Week_9–14 downloads and 17 pack rows)?
7. The 36 existing `*_W9-W14` / `*_W14-W20` / `*_W15-W20` Humanities lessons that serve covered Autumn 2 / Spring cells but match no R4 family — stub, or "left alone"? (P0 CELL_MAP will list them.)
8. Estate_v3 copies (27 rows; glv3-verify asserts 94 html / 88 glv3- rows) — untouched unless ruled.
9. Taught-now: 12 cells today (W03+W04); the pair moves with the run week; PR-3 final commits (literal reading) or a PR-3b after PR-4?
10. Content-PR granularity: 16 × ≤12 (proposal), 18 per term-dir, or R10's literal 4? Term indexes in PR-4 (dangling-link window) or with each term's last content PR?
11. RE SoW html carries 0 hrefs (R8 says its links assume the merged tree): add links at landing (authoring) or is the .docx the linked version? Year tag: Humanities SoW carries only `2026–27` (en dash, ×2), RE SoW `2026` ×2 — is the en-dash form acceptable, or does the tag live on the row only?
12. SoW pack extras (2 xlsx alignment sheets, ORDER_HUM-D5.md), Fallback MANIFEST.json / READ_ME_FALLBACK.txt / Editable_Visuals — land where?
13. `RE & World Views` chips: no subject exists anywhere; the chip derivation was not traced (P5 "through the real filter chain") — instrument owed before PR-4.
14. STATIC_CHECK_RESULTS.json (L24) — regenerate once per PR with the one-commit lag accepted, or drop from tracking (PASS 6 decision pending)?
15. Science state to close first: Site #412 (pins → b32bf1c7; the research's L56 = 124f513b reading is pre-#412), the PUBLISHED control pair (gate copies → f38a2a6f), Watch main red by attribution — S5's definition and Matt's phone check are not in any record read here.
16. Apps: the local checkout `/home/user/matt-s-apps-` (6df9e943) is stale; every companion is cut from origin/main.

**Not measured in this lane (never a pass):** the served origin (403); the catalogue chip chain; whether `humanities-shelf.json` and `terms-and-styles.json` are in the registry as published records; the GROW/LAUNCH taught-now existing surfaces by name; the exact per-cell stub map (P0's job); the Humanities index's article list after +78; which write post-dates the pack sums; the current state of the 8 Teacher_Notes.pdf.

### Critique — re-measured, corrections to carry

**R9 (re-measured, decimal MB as the order writes it; scope: `git ls-files` at 0248ea78, 1 tracked file absent on disk, not 2):** tracked 1,127,177,064 B = 1,127.2 MB (1,075.0 MiB); top-level `_*`/`.*` 206,116,473 B; tracked-minus-underscore 921,060,591 B = 921.1 MB; publisher set 894,517,656 B = 894.5 MB (853.1 MiB, 3,899 files, 1,506 html). Packs 229,831,832 B (mp4 46,523,541 B). Projections: tracked 1,357.0 MB (1,310.5 without mp4); publisher 1,124.3 MB (1,077.8 without mp4); tracked-minus-underscore 1,150.9 MB (1,104.4). Every measure exceeds 950 MB before AND after the pre-ruled mp4 step, so R9's "STOP before the content PR" fires on any reading — the draft's conclusion holds; its numbers (1296.0/1074.1/1099.4 MiB) are stale and in the wrong unit. Also note the `.git` pack alone is 1.46 GiB (`git count-objects -vH`), which the order's "Lessons repo size" may mean — add it as a fourth measure.

**The 8 Teacher_Notes.pdf are settled, not "not measured".** All eight PDFs have mtime 2026-09-19 20:39 (48,088 / 48,068 / 48,343 / 48,069 / 48,310 / 48,292 / 48,561 / 48,312 B) while their DOCX were written at 22:27; `RERENDER_DOCX.json` (22:32) lists the DOCX paths with exit 0 and the PDF byte sizes above — i.e. it recorded the existing PDFs, it did not re-render them. HUMD5_PARTA_CLOSE.md §3 ("Eight Teacher_Notes.pdf not re-rendered") is the current record; RERENDER.log's "converted 8 of 8" is the misleading one. B0 must re-render on Matt's machine or land with the 14 Class A residues declared.

**R6 is unmeasured and the order's premise is wrong.** `_sownb/STYLE_CONTRACT_v2.json` (445 rows; scopes `shared` 69, `family:BUILD Humanities` 35, `family:GROW Humanities` 36, …) SPEAKS on the pathway colour for all three Humanities families: `family.build-humanities.theme.lo-border`, `family.grow-humanities.theme.lo-border`, `family.launch-humanities.theme.lo-border` = `--lo-border #9c27b0` (kind token-last); `palette.token.lo-border` (shared) = #9c27b0; #4e7a9b appears only in 3 `family:BUILD Science` rows (`--lo-border`, `--aspire-border`, `--btn-bg`); #3f7d6e appears in 0 rows. The incoming lessons (one per pathway, HUM and RE) bind #4E7A9B to `--lo-border`/`--btn-bg`/`--aspire-border`, #3f7d6e to `--lo-border`/`--btn-bg`, #9c27b0 to `--lo-border`. "Contract wins where it speaks" would therefore recolour BUILD and GROW Humanities `--lo-border` to the LAUNCH purple — the opposite of R6's "where silent, keep incoming (BUILD #4E7A9B, GROW #3f7d6e)". This is a ruling item (contract amendment for R6/P7) missing from the list. The RE SoW's three pathway buttons also carry the incoming colours inline (`style='background:#4E7A9B'` …).

**R7 unmeasured:** 0/120 incoming Lesson.html load `hud.js`, 0/120 carry `rel="canonical"`, 0/120 mention ko-fi (static). `<h1` occurs twice in 106 lessons and once in the 14 Fallback, but one occurrence is inside a JS template string (`'<h1 contenteditable="true">'+esc(d.title)`), so "exactly one h1" is a rendered measurement the plan must schedule after P1, per lesson (120 rows). Way-home/guide/splash stamps: not counted.

**R11/R12/R14/R15 unmeasured (scope: 120 Lesson.html, static):** `re_safeguard` 42/42 RE and 64/78 HUM (the 14 Fallback lack it — already in residue); "not worship" 42/42 RE; "Nobody is asked to share a personal belief" 42/42 RE; "mark scheme"/"band descriptor" 0/120; Jan Halliday named in exactly 1 lesson (`GROW_RE_A2_W05_Lesson.html`, URL `https://humanists.uk/celebrants/jan-halliday/naming-ceremonies/`; `humanists.uk` in 10 RE lessons) — name the lesson and URL for P6; "Save my responses" 106/120 (Fallback 14 lack it), `localStorage|sessionStorage|indexedDB` 0/120 — R15's "do not add storage" is a constraint on the P1 writers and must be re-measured after them. R11's "any writer that rewrites slide text must leave them intact" needs the same before/after count.

**P6 has no plan rows.** Static pre-counts the draft could have stated: `assessment_mode` true in 16 lessons (the four summative RE — BUILD_RE_A2_W07, GROW_RE_A2_W07, LAUNCH_RE_A1_W07, LAUNCH_RE_A2_W07 — plus 12 HUM W07/W06; BUILD_RE_A1_W07 false ✓); `#re-starter` 42/42 RE; `#vary-starter` 78/78 HUM; `#vary-exit` 120/120; `#activity-board` string 120/120; `#interactive-map` string 120/120; "© OpenStreetMap contributors" 5 HUM lessons; `.ndjson/.log/.tmp/.bak` in the packs 0. The rendered checks (9 stages, timers 40, keyboard rounds, print routes, 390 px, reduced motion) have instruments in `_passhumd5/` (render_e4_print.js, render_e5_keyboard.js, render_e6_axe.js, render_e7_e16_e17.js, render_visibility.js) — name them as the P6 instruments and budget the 120 × 2-transport × 2-viewport run.

**Item 11 is wrong:** RE SoW has 213 hrefs (210 lesson-file links), not 0 (§1). The year-tag counts (Humanities SoW `2026–27` ×2 en-dash, `2026-27` ×0; RE SoW `2026` ×2; "Autumn only" 0 in the RE SoW — R8 puts that statement on the INDEX) reproduce.

**Item 15 is stale:** Site #412 merged (Site main 1e98bec0), Lessons #595 and Apps #118 merged; the open science items are the two 0/3 main-push observations and PASS 7 CLOSE (task #26 in progress).

**H3_TARGETS.json** is at `/tmp/claude-0/humd5/H3_TARGETS.json` (1,494 B), not under `_passhumd5/` (scope: ls) — uncommitted evidence for a STOP-X; say so.

**Missing ruling items:** (16) R6 contract-vs-incoming collision above; (17) the 21 + 2 + 4 unclassified W1-W8 surfaces (§5); (18) SoW homes (§1); (19) DECLARED_DIVERGENCES / check_landing_titles run over the landing set (§2); (20) per-deck source-selection table incl. the `*_Reviewed` folder names and the duplicate RE GROW upload (§6); (21) the fourth repo-size measure (.git pack).

---

## Requirements not addressed, or addressed without a count (critique)

Scope: the draft text as supplied vs ORDER_HUMD5_PARTB.txt R1–R15, P0–P7.

| req | draft status | what is missing (measured here) |
|---|---|---|
| R1 | partial | no statement that the 1,662 landed basenames are unchanged; the one-truth rule collides with 21 unrowed `*_HUM_*` W1-W8 lessons + 2 classic-33 rows + 4 START_HERE pages (§5) |
| R2 | addressed with counts | SoW homes absent; `Humanities_Teesside/index.html` shelf listing (+78) belongs here as a SHELVES change |
| R3 | NOT addressed | state "0 donor/withdrawn packs present" with scope (`ls unzipped`: 12 Final/Fallback + SoW) |
| R4 | counts, with errors | 30 retained routes mis-identified (0 David cover); 27 W1-W8 surfaces unclassified |
| R5 | addressed | add the merge-date rule; pair moves Monday 21 Sep |
| R6 | NOT measured | contract speaks (`--lo-border #9c27b0` for all three Humanities families); incoming binds #4E7A9B/#3f7d6e/#9c27b0 — ruling needed |
| R7 | NOT measured | hud.js 0/120, canonical 0/120, ko-fi 0/120, h1 rendered count owed |
| R8 | partial | RE SoW 210 lesson links (not 0); tracker contradictions: no list started, no count |
| R9 | addressed, stale | re-measured in MB above; add .git pack (1.46 GiB) |
| R10 | addressed | PR-0 before PR-1 is an unflagged order change |
| R11 | NOT measured | 42/42 RE carry all three safeguard markers; re-measure after writers |
| R12 | NOT measured | 0/120 "mark scheme"/"band descriptor" (static, Lesson.html only; docx/pptx/pdf not scanned) |
| R13 | addressed | — |
| R14 | partial | lesson and URL not named (GROW_RE_A2_W05; humanists.uk/celebrants/jan-halliday/naming-ceremonies/) |
| R15 | NOT addressed | 106/120 carry the button; 0/120 storage APIs; writer constraint unstated |
| P0 | addressed | add the per-deck source table |
| P1 | partial | writers not named by path; furniture is added, not re-stamped |
| P2–P5 | addressed | chip-count instrument owed (draft says so) |
| P6 | NOT planned | no gate rows, instruments or static pre-counts (§7) |
| P7 | addressed | use HUMD5_PARTA_CLOSE.md §1 totals |

---

## Standing-limit check of the draft's steps (critique)

Scope: the draft's §0–§7 steps against the limits named in the task (no force-push, no branch deleted, nothing disabled, no CI edit except carrier pin moves, source selection never filesystem order, DECLARED_DIVERGENCES empty) and ORDER_HUMD5_FULL.txt L4 GROUND RULES.

- **Force-push / branch deletion / disabling:** none proposed. PASS.
- **CI edits:** PR-0 carries (a) a generated PIN1 widening — precedent exists (`tools/pin1/derive_triggers.py --write`, 3b commit); (b) a proposed hand widening of `glv3-verify.yml` and `cross-estate-on-content.yml` `paths:` — NOT a pin move, no precedent; must be a STOP option, not a PR-0 item. The two carrier bumps (`education-pages.yml` builder pin, currently a1b2a85c at L98/L100) are pin moves. VIOLATION as drafted (fixable by moving (b) to the ruling list only).
- **Source selection never filesystem order:** the draft selects by pack folder and `find`, records no per-deck generations/sha table, and does not rule the `*_Reviewed` folder names or the duplicate RE GROW upload (CHASSIS_CONTRACT.md L556; RELEASE_LEDGER.md L35 table shape). VIOLATION by omission.
- **DECLARED_DIVERGENCES empty:** the tool (`tools/sx3/check_landing_titles.py`, origin/main L45) is never run in the plan; the proposed row titles diverge from deck `<h1>` by construction. NOT ADDRESSED.
- **SHAs derived from refs, never transcribed:** the draft carries 545d9e8b, 6bd51afc, 85f7e07f, 49311258 as current — all superseded at review time (cbfbc70c, f38a2a6f, bbce3771, 37f04c16). Re-derive every SHA at write time.
- **Behaviour measured in a rendered browser:** the draft's R7/P6 statements are static or absent; my counts above are static pre-counts and are labelled so — they do not discharge P6.

---

## Counts as re-measured by the critique (scopes inside)

```json
{
 "sha256sums_entries_checked": {
  "value": 1605,
  "fail": 0,
  "scope": "sha256sum -c in each of the 11 *_Final/*_Reviewed inner dirs, 2026-09-20; draft said 531/1613 FAIL"
 },
 "packs": {
  "value": 13,
  "scope": "ls /tmp/claude-0/humd5/unzipped"
 },
 "pack_files": {
  "value": 1750,
  "bytes": 229831832,
  "scope": "find over all 13 packs (draft: 231,750,463 B)"
 },
 "lesson_dir_files": {
  "value": 1662,
  "bytes": 228630296,
  "humanities_files": 1074,
  "humanities_bytes": 161691422,
  "re_files": 588,
  "re_bytes": 66938874,
  "scope": "files under */W\\d\\d/ in the 13 packs"
 },
 "final_only_bytes": {
  "value": 212570535,
  "scope": "packs minus Fallback (16,963,083) minus SoW pack (298,214); R9 says ≈210 MB"
 },
 "mp4_bytes": {
  "value": 46523541,
  "files": 120,
  "scope": "packs"
 },
 "pack_root_files": {
  "value": 75,
  "bytes": 882092,
  "scope": "inner-root files of the 13 packs (draft 869,162)"
 },
 "start_here_hrefs_in_lesson_html": {
  "value": 240,
  "lessons": 120,
  "scope": "href= in every Lesson.html; all are ../../../START_HERE.html"
 },
 "sources_and_checks_copies": {
  "root": 11,
  "per_lesson": 106,
  "distinct_sha256": 1,
  "scope": "packs"
 },
 "re_sow_hrefs": {
  "value": 213,
  "lesson_file_links": 210,
  "anchors": 3,
  "scope": "RE_Scheme_of_Work_Autumn_2026.html (single-quoted href); draft said 0"
 },
 "hum_sow_hrefs": {
  "value": 1,
  "scope": "Humanities_Scheme_of_Work_2026-27.html"
 },
 "hum_sow_week_headings": {
  "value": 117,
  "scope": "'Week N ·' in Humanities SoW html"
 },
 "resources_rows": {
  "value": 956,
  "original": 734,
  "shelf_rows": 104,
  "pack_rows": 118,
  "scope": "/home/user/lessons-carrier resources.json at 0248ea78"
 },
 "subjects_rows": {
  "Humanities": 98,
  "Humanities · Teesside": 5,
  "RE & World Views": 0,
  "scope": "resources.json"
 },
 "catalogue_pins_files": {
  "value": 543,
  "humanities_teesside": 27,
  "re_teesside": 0,
  "scope": "tools/verify_cross_estate_unification.py CATALOGUE_PINS at 0248ea78"
 },
 "pin1_lines_per_block": {
  "value": 557,
  "humanities": 27,
  "re": 0,
  "blocks": 2,
  "scope": ".github/workflows/mbm-cross-estate-unification.yml L13-571, L575-1133"
 },
 "term_and_style_evidence_entries": {
  "value": 1080,
  "humanities_teesside": 111,
  "scope": "tools/catalogue/TERM_AND_STYLE_EVIDENCE.json entries"
 },
 "lesson_order_entries": {
  "value": 1080,
  "scope": "assets/catalogue/lesson-order.json entries"
 },
 "resource_sizes_sizes": {
  "value": 1476,
  "scope": "data/resource-sizes.json sizes"
 },
 "humanities_shelf_lessons": {
  "value": 142,
  "selection_lessons": 142,
  "scope": "assets/catalogue/humanities-shelf.json, tools/catalogue/HUMANITIES_SELECTION.json"
 },
 "retained_routes": {
  "value": 30,
  "david_cover": 0,
  "hum_strand_w3_w7": 15,
  "re_strand_w3_w7": 15,
  "scope": "tools/humanities_resources/SOURCE_MANIFEST.json records[*].existing_routes; all under Humanities_Teesside/{BUILD,GROW,LAUNCH}_W1-W8_2026-27/"
 },
 "w1_w8_html": {
  "value": 51,
  "re_strand": 22,
  "hum_strand_unrowed": 21,
  "classic_rows_763_768": 2,
  "start_here_pages": 4,
  "scope": "git ls-files Humanities_Teesside/*_W1-W8_2026-27/ at 0248ea78"
 },
 "v4_slideshows_hum": {
  "build": 8,
  "grow": 8,
  "launch": 9,
  "scope": "git ls-files */Slideshows/ matching _HUM_W"
 },
 "teaching_packs": {
  "files": 245,
  "html": 41,
  "w3_w7_html": 30,
  "bytes": 114632552,
  "scope": "git ls-files Humanities_Teesside/Teaching_Packs/"
 },
 "david_cover_br_gr_w3_w7_html": {
  "value": 10,
  "scope": "git ls-files Humanities_Teesside/David_Cover_Autumn1_W3-W7/"
 },
 "w9_w20_html": {
  "value": 41,
  "classic": 5,
  "scope": "git ls-files Humanities_Teesside/*_W{9-W14,14-W20,15-W20}_2026-27/"
 },
 "estate_v3_humanities_html": {
  "build": 9,
  "grow": 9,
  "launch": 9,
  "scope": "git ls-files *_Estate_v3/Humanities_Teesside/"
 },
 "http_equiv_refresh_files": {
  "value": 0,
  "scope": "git grep over *.html at 0248ea78"
 },
 "humanities_teesside_tracked": {
  "files": 498,
  "bytes": 140242539,
  "html": 185,
  "scope": "git ls-files Humanities_Teesside/"
 },
 "lessons_repo_size": {
  "tracked_bytes": 1127177064,
  "tracked_files": 8282,
  "missing_on_disk": 1,
  "top_level_underscore_dot_bytes": 206116473,
  "tracked_minus_underscore_bytes": 921060591,
  "publisher_public_set_files": 3899,
  "publisher_public_set_bytes": 894517656,
  "publisher_public_set_html": 1506,
  "git_pack_size": "1.46 GiB",
  "scope": "git ls-files at 0248ea78; public set via Site build_education.public_file()+excluded_asset() at 1e98bec0"
 },
 "r9_projection_MB": {
  "tracked_plus_packs": 1357,
  "tracked_plus_packs_no_mp4": 1310.5,
  "public_plus_packs": 1124.3,
  "public_plus_packs_no_mp4": 1077.8,
  "tracked_minus_underscore_plus_packs": 1150.9,
  "line": 950,
  "scope": "decimal MB from the byte counts above"
 },
 "registry_education_lessons": {
  "entries": 3726,
  "singles": 3669,
  "pairs": 57,
  "arriving": 0,
  "humanities_teesside": 498,
  "humanities_2026_27": 0,
  "re_teesside": 0,
  "scope": "Site domain-split/education-publication-admission.json at 1e98bec0"
 },
 "registry_other_trees": {
  "education_site": 203,
  "education_site_pairs": 46,
  "education_apps": 107,
  "education_apps_pairs": 7,
  "scope": "same file"
 },
 "gate_copy_sha256_prefix_at_origin_main": {
  "lessons": "f38a2a6f",
  "apps": "f38a2a6f",
  "scope": "git show origin/main:tools/verify_cross_estate_unification.py | sha256sum in both checkouts; draft said 6bd51afc"
 },
 "refs_now": {
  "lessons_origin_main": "cbfbc70c",
  "site_main": "1e98bec0",
  "apps_origin_main": "bbce3771",
  "carrier_worktree": "0248ea78",
  "proof_branch_head": "37f04c16",
  "files_between_worktree_and_main": 18,
  "scope": "git rev-parse / git diff --stat at review time 2026-09-20"
 },
 "lesson_html_static_markers": {
  "re_safeguard_RE": 42,
  "re_safeguard_HUM": 64,
  "not_worship_RE": 42,
  "nobody_asked_RE": 42,
  "save_my_responses": 106,
  "storage_apis": 0,
  "hud_js": 0,
  "canonical_link": 0,
  "ko_fi": 0,
  "mark_scheme_or_band_descriptor": 0,
  "assessment_mode_true": 16,
  "assessment_mode_false": 104,
  "re_starter_RE": 42,
  "vary_starter_HUM": 78,
  "vary_exit": 120,
  "osm_attribution": 5,
  "halliday_lessons": 1,
  "humanists_uk_lessons": 10,
  "h1_tag_count_2": 106,
  "h1_tag_count_1": 14,
  "scope": "static string presence over the 120 pack Lesson.html; not a rendered measurement"
 },
 "style_contract_rows": {
  "rows": 445,
  "mention_4e7a9b": 6,
  "mention_9c27b0": 12,
  "mention_3f7d6e": 0,
  "humanities_family_lo_border_rows": 3,
  "scope": "_sownb/STYLE_CONTRACT_v2.json"
 },
 "teacher_notes_pdf_not_rerendered": {
  "value": 8,
  "pdf_mtime": "2026-09-19 20:39",
  "docx_mtime": "2026-09-19 22:27",
  "scope": "the 8 RE Teacher_Notes.pdf named in RERENDER_DOCX.json"
 },
 "parta_close_doc": {
  "exists": true,
  "lines": 89,
  "commit": "45e1b58e",
  "matt_decisions_pending": 8,
  "scope": "/home/user/lessons/_passhumd5/HUMD5_PARTA_CLOSE.md"
 },
 "science_records_scope_lines": {
  "value": 3807,
  "scope": "wc -l _sx3/*.md (15 files) + SX3_LEDGER_pass3.md (393); draft said 386"
 },
 "e6_axe_post_progress": {
  "value": "90/120",
  "scope": "/tmp/claude-0/humd5/E6_AXE_POST.log tail at review time; draft said 40/120"
 },
 "declared_divergences": {
  "value": 0,
  "tool": "tools/sx3/check_landing_titles.py L45 at origin/main cbfbc70c",
  "tracked_at_worktree_0248ea78": false,
  "ci_hooks_at_origin_main": 0,
  "scope": "git ls-tree origin/main; grep over every workflow at origin/main"
 },
 "draft_requirements_unaddressed_or_uncounted": {
  "R3": "not addressed",
  "R6": "not measured",
  "R7": "not measured",
  "R11": "not measured",
  "R12": "not measured",
  "R15": "not addressed",
  "P6": "no gate plan",
  "R8_tracker_contradictions": "no list",
  "R14": "lesson/URL not named",
  "R1": "basenames/one-truth collision uncounted",
  "scope": "draft text vs ORDER_HUMD5_PARTB.txt"
 },
 "draft_numbers_not_reproduced": {
  "value": 14,
  "items": "531/1613 sha FAIL; PARTA_CLOSE not found; head 49311258 + uncommitted; 386-line scope; pack bytes (total, per type, per pack, lesson-dir, pack-root, READ_ME 504 B, Final-only); publisher 3900/894,531,940; 30 retained routes composition; RE SoW 0 hrefs; Site workflow line numbers L56/L79/L88/L62 and two tool paths; gate copy 6bd51afc / Apps 85f7e07f / Lessons main 545d9e8b; repo bytes 1,127,172,968 (2 missing); checker L223-225; E6 40/120",
  "scope": "this review"
 }
}
```

## STOP-B1 — the ruling list, consolidated

The draft's §7 items 1–16 stand, with these corrections: item 11 (RE SoW has 213 hrefs, 210 lesson-file links — it needs a home at `RE_Teesside/2026-27/`), item 15 (science state: #412/#595/#118 merged; the open items are the S5 readback acceptance and the phone check). Added by the critique: (16) R6 — the STYLE_CONTRACT speaks on all three Humanities families' `--lo-border` (#9c27b0), so "contract wins where it speaks" would recolour BUILD/GROW; ruling or amendment; (17) the 21 unrowed `*_HUM_W1..W8` lessons (15 of them SOURCE_MANIFEST retained routes), rows [763]/[768] and the 4 START_HERE pages in the W1-W8 dirs — stub or leave; (18) SoW homes; (19) DECLARED_DIVERGENCES / check_landing_titles over the landing set and whether the proposed row-title form is accepted; (20) the per-deck source-selection table incl. the `*_Reviewed` names and the duplicate RE GROW upload; (21) the fourth repo-size measure (.git pack 1.46 GiB) and which measure the 950 MB line binds — every measure exceeds it before landing, so R9 fires on any reading; (22) B0 — re-render the 8 RE Teacher_Notes.pdf on Matt's machine before the granted build, or land with the 14 Class A residues declared.

### Open questions (critique's list, verbatim)

- R6: the STYLE_CONTRACT speaks per pathway (`family.{build,grow,launch}-humanities.theme.lo-border` = --lo-border #9c27b0, token-last) while the order presumes it is silent on BUILD/GROW — does the contract win (recolouring BUILD/GROW `--lo-border` to purple) or is the order's 'keep incoming' the ruling, with a contract amendment in P7?
- R4/R1: the 21 unrowed `*_HUM_W1..W8` Migration & Identity lessons in the W1-W8 dirs (15 of them SOURCE_MANIFEST retained routes), rows [763]/[768] (classic-33, Autumn 1 W7/W3) and the 4 START_HERE pages there — stub, or 'left alone'? The validator's `existing_routes_preserved != 30` (L321) reds on any stub of the 15.
- Where do the two SoW html/docx pairs live? The RE SoW's 210 relative links resolve only from `RE_Teesside/2026-27/`.
- DECLARED_DIVERGENCES: is `tools/sx3/check_landing_titles.py` to be run over the 128 landing pages per PR, and does its `<h1>`-vs-listed-title comparison accept the proposed `… (<Term> · week n)` row titles?
- Source selection: are the `*_Reviewed` inner folder names (Final content) and the byte-identical duplicate RE_Autumn_GROW upload to be recorded as explicit per-deck rulings in the RELEASE_LEDGER table shape?
- R9: which of the four size measures (tracked, tracked-minus-underscore, publisher set, .git pack 1.46 GiB) does the 950 MB line bind, given every one exceeds it before landing?
- B0: re-render the 8 RE Teacher_Notes.pdf on Matt's machine before the granted build, or land with the 14 Class A residues declared?
- Lessons main green: the #595 (cbfbc70c) and Apps #118 (bbce3771) main-push observations stand at 0/3 reads — who spends those reads before Part B's gate is re-evaluated?
- PR-0: is a fence PR before PR-1 an accepted exception to R10's order, and is the `glv3-verify.yml` path widening refused outright (hand CI edit) or ruled?
- R5: if the merges slip past Monday 21 Sep the taught-now pair becomes W04+W05 — is the pair fixed at S2 or at the first stub merge?
