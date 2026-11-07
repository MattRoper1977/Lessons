# PACK-1R P1 report

**STOP-P1: three Sum1 W1 lessons and three pathway landing pages are ready for review. Wait for “P1 ok” before authoring the remaining 36 lessons.**

Date: 21 September 2026. Repository: MattRoper1977/Lessons. Authoring branch: `claude/pack1r-hum-summer`. Base main: `3887f7acc99468b55ecc9f0b67b6be043aebc8ed` (HUM-T batch 1, PR #606).

This report supersedes the pre-authoring STOP. Matt’s R1–R3 rulings close those questions; they do not constitute P1 approval. All changes are confined to `_incoming/pack1r/`. No estate tool, registry, served file, manifest, pin or CI file is changed. No lesson is registered or published.

## Authored population and phone preview paths

The three HTML files are the canonical intake previews. The served targets below are the paths tested in the served-equivalent tree; they are not claimed to be live published URLs.

| Pathway | Intake preview | Served target | Title |
|---|---|---|---|
| BUILD | `packs/HUM_Summer_1_BUILD_Final/BUILD/Summer_1/W01/BUILD_HUM_S1_W01_Lesson.html` | `Humanities_Teesside/BUILD_W27-W39_2026-27/BUILD_HUM_S1_W01_Lesson.html` | My school and local features |
| GROW | `packs/HUM_Summer_1_GROW_Final/GROW/Summer_1/W01/GROW_HUM_S1_W01_Lesson.html` | `Humanities_Teesside/GROW_W27-W39_2026-27/GROW_HUM_S1_W01_Lesson.html` | My place, the UK and the wider world |
| LAUNCH | `packs/HUM_Summer_1_LAUNCH_Final/LAUNCH/Summer_1/W01/LAUNCH_HUM_S1_W01_Lesson.html` | `Humanities_Teesside/LAUNCH_W27-W39_2026-27/LAUNCH_HUM_S1_W01_Lesson.html` | Resource use and climate evidence |

Pathway landing pages are under `landing/<PATHWAY>_W27-W39_2026-27/START_HERE.html`; each maps to `Humanities_Teesside/<PATHWAY>_W27-W39_2026-27/START_HERE.html`. They name **Summer: Change** and **Year A: Self and Belonging**, display the 21 September 2026 update, and link only the available lesson. Future weeks are described without dead lesson cards. The pack-root START_HERE pages index the corresponding companion resources.

Each P1 pack also includes an A4 knowledge organiser, seven-page pupil resource pack, editable teacher notes and PDF, nine-stage editable slides, source checks, COVERAGE.csv, content snapshot, QA reports, SHA256SUMS and changelog. The three ZIPs are explicitly P1 previews, not six completed Summer packs.

## Rulings applied

**R1 containment.** Only the literal BUILD `<script defer src="/hud.js">`, pathway A2 Lessons anchors, and GROW/LAUNCH `a.way-home` to `./START_HERE.html` are exempt. The target depth is two levels below the Lessons root: BUILD uses `../../index.html?subject=Humanities&pathway=BUILD`; GROW/LAUNCH `a.mbmhome` uses `../../index.html`. The harness red-proves an extra HUD attribute, a query added to the HUD path, an external script and an escaping anchor. Other runtime references and companion links stay inside their pack. Source URLs are printed provenance, not external resource loads.

The unchanged live HUD returned HTTP 200 from `https://madebymatt.uk/hud.js`; its hash is in `qa/hud_origin.json`. It is fetched into memory by the test server, never vendored or inlined. The catalogue anchors resolve HTTP 200 to the checkout’s real index, and the own-folder anchors resolve HTTP 200 to the authored landing pages.

**R2 instruments.** The intake harness imports the estate’s unchanged `classify()`, title parser/heading/distinct functions, HUM-T loop battery and `render_proof.cjs` function with exactly three lessons. The browser import shim relocates its hard-coded axe path and maps file navigation to the served-equivalent route; it does not alter the function body. The Class A pattern/helper list is ported locally; the original module is neither run nor imported. All reports are written inside the intake. Source-tool hashes are recorded in `qa/static_checks.json`.

LISTED is **NOT YET APPLICABLE — registration is Code’s admission**. The replacement check passes: `<title> == <h1> == COVERAGE.csv title == START_HERE card title`. DISTINCT also passes. The historical r38–r40 counters inside the HUM-T browser tool are loop evidence; the intake report separately measures the chassis contract’s actual rows 38–42.

**R3 stages and timers.** Nine stages, in the exact order: Title · Arrival · Starter · I Do · We Do · I Do 2 · We Do 2 · Independent · Exit. Stage minutes: **0, 4, 4, 5, 5, 4, 4, 10, 4**. Total: **40 minutes in one session**. Independent starts after 26 minutes and Exit lasts four. Arrival includes retrieval; no tenth stage or two-session split is introduced. Timer parity uses the science exemplar; the untimed Humanities batch-1 deck is not the timer reference.

## Sources and accepted corrections

The authoritative source is `Humanities_Teesside/Teaching_Packs/HUM_00_SoW_and_Order/Humanities_Scheme_of_Work_2026-27.html`, SHA256 `ac8f8d0a4188d147097a491b0db59efef16feb0c0f6c4fa8e13144bb8a53f69f`. All 39 Summer objectives are present and uniquely assigned. The Alignment workbook covers Autumn/Spring only and is not used to invent Summer objectives.

There is no TERM_BASES.json on this main. The SoW lengths **7,7,6,6,6,7** yield offsets **0,7,14,20,26,32**, therefore Summer 1 slots **27–32** and Summer 2 slots **33–39**. COVERAGE.csv records all 39 target paths; only the three P1 rows have authored files and titles. The other 36 remain WAITING P1 ok.

Exact accreditation caveat retained:

> UAS means unit Award Scheme: match evidence to the exact selected unit and its requirements before submission. The plans do not identify approved unit codes.

No accreditation code or URL is invented.

The supplied Feedback Policy uses **EFL**. TA layers quote exact body §5 Space text and body §14 procedure/capture text from the PDF, not the adapter’s paraphrases. The staff code strip remains staff-side. EFL capture appears in the Exit staff guidance. Policy body numbering is used because the contents page differs. Policy hashes: Curriculum `593ab59361d1f1d22360a0ba12bdb96e08dcd94404a07368c09768414e982aed`; Feedback `41046284a00c9218679b946134cbc6e53c1897aad28b15fc4bd4aa963720ff3b`.

BUILD uses an explicitly fictional plan for modelling and requires transfer to the actual school name and nearby features, with teacher preparation stated. GROW uses Natural Earth land geometry and a Middlesbrough example at UK/world views. LAUNCH uses a fixed DESNZ online-data snapshot, published 5 February 2026, with source/date/unit/territorial scope, rounded values, resource-use explanation and a limitation. It distinguishes UK emissions from global temperature and consumption emissions. Every lesson includes a specific careers connection.

## Measured results

| Lesson | Chassis | 38 | 39–42 | 45 | 46 | Axe serious/critical at 390 px | Class A | Containment | Titles | Careers |
|---|---|---|---|---|---|---|---|---|---|---|
| BUILD_HUM_S1_W01 | classroom | PASS | PASS | PASS | PASS | 0 | 0 | PASS | PASS | Y |
| GROW_HUM_S1_W01 | review | PASS | PASS | PASS | PASS | 0 | 0 | PASS | PASS | Y |
| LAUNCH_HUM_S1_W01 | review | PASS | PASS | PASS | PASS | 0 | 0 | PASS | PASS | Y |

- Row 38: zero uncaught page errors; zero failed requests during the rendered run.
- Rows 39 and 41: all six dialogs in each lesson opened, had nonzero dimensions, and closed; goto and print controls were driven.
- Row 40: native dialog IDs are used directly; no remapped wrapper needs an alias. Actual opener/goto/close calls run without a showModal error.
- Row 42: one action per shell click; loop controls have separate listeners, no shell ancestry and no cross-stage state leak.
- Row 45: **21/21** panels reached; **21/21** refuse Audience before Voice; **21/21** refuse Influence before Audience; **21/21** complete in order. I Do stages have no panel. Voice controls are visibly named, Audience receives the specific response, and Influence names the next task and agreed change.
- Row 46: Humanities tasks ask for map/source evidence, not personal religious or political belief.
- Axe: nine stages plus six dialogs per lesson at 390 px, plus the three landing pages; no serious or critical findings. No horizontal overflow in the nine stage views. Reduced motion is supported without timed animation.
- Print: the real organiser print output is one A4 page in each lesson. Companion organisers are also one page; pupil resources are seven pages; teacher notes are five pages. Actual print-control invocations, answer reveals, routes, maps, model reveals, timer start/pause/decrement, picker clearing and staff preference were driven.
- A1–A3 and pathway selector matrix: classroom for BUILD; review for GROW/LAUNCH. Expected controls, intentional zeroes, effective exemplar palette values and root classes pass. BUILD writes no storage; GROW/LAUNCH use only `mbm_guide_v1`. R-KO uses printable HTML, not fabricated SVG markers. Contract lexical variable counts include n6 comments and inline ordering; actual colour-property values are compared separately.
- HTML rebuild: two passes produce identical bytes for all generated HTML. ZIP packaging is also byte-identical across two packaging passes. Full DOCX/PPTX/PDF regeneration parity is not claimed at this P1 checkpoint.

Evidence: `qa/static_checks.json`, `qa/browser_checks.json`, `qa/pack_checks.json`, `qa/print_companions.json`, `qa/package_checks.json`, rendered mobile/desktop captures and organiser PDFs. Presentation structural/native-chart validation receipts are retained under `qa/slides-*/validation.json`; editable maps are raster coastline references with editable surrounding text, and LAUNCH charts retain native editable data.

## All 39 planned lessons

“WAITING P1 ok” is the user’s stage gate, not a missing SoW objective. No QA result is claimed for these 36 unauthored lessons.

| ID | Pathway | Term | Week | SoW slot | Exact SoW objective | Status |
|---|---|---|---|---|---|---|
| BUILD_HUM_S1_W01 | BUILD | Sum1 | 1 | 27 | Name and locate my school and local features. | P1 authored |
| BUILD_HUM_S1_W02 | BUILD | Sum1 | 2 | 28 | Use a simple map or plan of a familiar place. | WAITING P1 ok |
| BUILD_HUM_S1_W03 | BUILD | Sum1 | 3 | 29 | Compare my place with a contrasting place. | WAITING P1 ok |
| BUILD_HUM_S1_W04 | BUILD | Sum1 | 4 | 30 | Carry out simple fieldwork in the grounds. | WAITING P1 ok |
| BUILD_HUM_S1_W05 | BUILD | Sum1 | 5 | 31 | Talk about the wider world using continents and oceans. | WAITING P1 ok |
| BUILD_HUM_S1_W06 | BUILD | Sum1 | 6 | 32 | Record local features on a class map. | WAITING P1 ok |
| GROW_HUM_S1_W01 | GROW | Sum1 | 1 | 27 | Locate my place the UK and the wider world on maps. | P1 authored |
| GROW_HUM_S1_W02 | GROW | Sum1 | 2 | 28 | Use atlases grid references and digital maps. | WAITING P1 ok |
| GROW_HUM_S1_W03 | GROW | Sum1 | 3 | 29 | Carry out simple fieldwork about my local area. | WAITING P1 ok |
| GROW_HUM_S1_W04 | GROW | Sum1 | 4 | 30 | Describe physical and human features of a place. | WAITING P1 ok |
| GROW_HUM_S1_W05 | GROW | Sum1 | 5 | 31 | Compare my locality with a contrasting place. | WAITING P1 ok |
| GROW_HUM_S1_W06 | GROW | Sum1 | 6 | 32 | Complete a fieldwork and locality study and bank UAS evidence. | WAITING P1 ok |
| LAUNCH_HUM_S1_W01 | LAUNCH | Sum1 | 1 | 27 | Explain resource use and climate change using online data. | P1 authored |
| LAUNCH_HUM_S1_W02 | LAUNCH | Sum1 | 2 | 28 | Evaluate responses to climate change. | WAITING P1 ok |
| LAUNCH_HUM_S1_W03 | LAUNCH | Sum1 | 3 | 29 | Make a reasoned geographical decision. | WAITING P1 ok |
| LAUNCH_HUM_S1_W04 | LAUNCH | Sum1 | 4 | 30 | Create a digital sustainability campaign linked to Earth Day. | WAITING P1 ok |
| LAUNCH_HUM_S1_W05 | LAUNCH | Sum1 | 5 | 31 | Link learning to local action with Community Project links. | WAITING P1 ok |
| LAUNCH_HUM_S1_W06 | LAUNCH | Sum1 | 6 | 32 | Complete a sustainability decision report. | WAITING P1 ok |
| BUILD_HUM_S2_W01 | BUILD | Sum2 | 1 | 33 | Identify ways we can look after our planet linked to Earth Day. | WAITING P1 ok |
| BUILD_HUM_S2_W02 | BUILD | Sum2 | 2 | 34 | Sort recycling and explain why with Science links. | WAITING P1 ok |
| BUILD_HUM_S2_W03 | BUILD | Sum2 | 3 | 35 | Take part in an eco action linked to World Environment Day. | WAITING P1 ok |
| BUILD_HUM_S2_W04 | BUILD | Sum2 | 4 | 36 | Talk about caring for living things and places. | WAITING P1 ok |
| BUILD_HUM_S2_W05 | BUILD | Sum2 | 5 | 37 | Make a change to help our environment. | WAITING P1 ok |
| BUILD_HUM_S2_W06 | BUILD | Sum2 | 6 | 38 | Share our planet project with others. | WAITING P1 ok |
| BUILD_HUM_S2_W07 | BUILD | Sum2 | 7 | 39 | Review Humanities skills and bank UAS evidence. | WAITING P1 ok |
| GROW_HUM_S2_W01 | GROW | Sum2 | 1 | 33 | Investigate how people affect the environment over time. | WAITING P1 ok |
| GROW_HUM_S2_W02 | GROW | Sum2 | 2 | 34 | Use historical sources about land settlement or industry. | WAITING P1 ok |
| GROW_HUM_S2_W03 | GROW | Sum2 | 3 | 35 | Explain how and why our environment has changed. | WAITING P1 ok |
| GROW_HUM_S2_W04 | GROW | Sum2 | 4 | 36 | Investigate how communities care for the planet with an RE link. | WAITING P1 ok |
| GROW_HUM_S2_W05 | GROW | Sum2 | 5 | 37 | Plan and present an enquiry about our world. | WAITING P1 ok |
| GROW_HUM_S2_W06 | GROW | Sum2 | 6 | 38 | Present geographical and historical findings. | WAITING P1 ok |
| GROW_HUM_S2_W07 | GROW | Sum2 | 7 | 39 | Complete an our-world enquiry assessment with map and source checks and bank UAS evidence. | WAITING P1 ok |
| LAUNCH_HUM_S2_W01 | LAUNCH | Sum2 | 1 | 33 | Investigate local heritage and change using digital archives. | WAITING P1 ok |
| LAUNCH_HUM_S2_W02 | LAUNCH | Sum2 | 2 | 34 | Conduct geographical fieldwork in the locality. | WAITING P1 ok |
| LAUNCH_HUM_S2_W03 | LAUNCH | Sum2 | 3 | 35 | Use GIS to map how the locality has changed. | WAITING P1 ok |
| LAUNCH_HUM_S2_W04 | LAUNCH | Sum2 | 4 | 36 | Connect history and geography to my place with preparation for adulthood links. | WAITING P1 ok |
| LAUNCH_HUM_S2_W05 | LAUNCH | Sum2 | 5 | 37 | Build a multimedia my-place project. | WAITING P1 ok |
| LAUNCH_HUM_S2_W06 | LAUNCH | Sum2 | 6 | 38 | Present the local-heritage project. | WAITING P1 ok |
| LAUNCH_HUM_S2_W07 | LAUNCH | Sum2 | 7 | 39 | Complete the project and bank UAS evidence. | WAITING P1 ok |

## Handoff boundary

The draft PR is for P1 review only. Code’s registration, admission and publication remain outside this authoring branch. Continue only after Matt gives **P1 ok**. Do not infer that permission from the closed R1–R3 pre-authoring STOP.
