# GROW + LAUNCH v3 deployment verification

ROLLBACK_SHA: `1e8a428b523d1b970a8a3a2ab2a99f48a8271d09`

## Three findings first

1. **56/80 deployable lessons are screen-only**: GROW ASDAN 18, LAUNCH ASDAN 30, LAUNCH Art 8. The live ASDAN suites therefore remain the printable PEQ assessment-record route, including the witness statement and T2-4 learner-confirmation line; live LAUNCH Art remains the printable Silver portfolio route.
2. **Source-authored PEQ code wording is present in 6 of the 48 deployable v3 ASDAN lessons.** 6 LAUNCH PEQ lesson files carry source-authored `ComSk1` in qualification/boundary wording; generation introduced zero new PEQ codes. A code mention does not establish a per-activity criterion mapping, so the live Evidence Binder/authorised mapping remains necessary where criterion mapping is not explicitly stated.
3. **Arts Award tags are adviser decisions, not code changes.** GROW reduces W2 A+D→A and W4 A+B→B; LAUNCH reduces W8 from the whole portfolio tag set to Unit 2E alone. No tag was changed by this run.

## Pack / install counts

- GROW: 34 lessons (Art 8 · Humanities 8 · ASDAN 18)
- LAUNCH: 46 lessons (Art 8 · Humanities 8 · ASDAN 30)
- Total: 80 lessons + 2 estate hubs + 6 subject hubs = 88 new catalogue entries.
- Print-bearing: 24 lessons.
- Screen-only: 56 lessons.

## Catalogue

- Base resources universe: 552 entries.
- Added universe: 88 entries.
- Final universe: 640 entries.
- Conditional Humanities_Teesside year corrections applied: 0 IDs.
- Expected 2026-27 chip totals: `{"Art · Teesside Studio Suite": 81, "GROW Vocational & PfA": 42, "Humanities": 59, "LAUNCH Vocational & PfA": 68}`.

## Arts Award adviser tables

### GROW Bronze

| Week | live Bronze tag | v3 Bronze tag |
| --- | --- | --- |
| W1 | A | A |
| W2 | A+D | A |
| W3 | A | A |
| W4 | A+B | B |
| W5 | C | C |
| W6 | D | D |
| W7 | D | D |
| W8 | all four | all four |

### LAUNCH Silver

| Week | live Silver tag | v3 Silver tag |
| --- | --- | --- |
| W1 | 1A | 1A |
| W2 | 1D | 1D |
| W3 | 1B | 1B |
| W4 | 1C | 1C |
| W5 | 2A–B | 2A–B |
| W6 | 2C–D | 2C–D |
| W7 | 2C–D | 2C–D |
| W8 | 1A–B, 1C–D, 2A–B, 2C–D, 2E | 2E |

Organisation evidence artefacts confirmed: `{"GROW W5": {"organisation_mentions": 24, "evidence_artefact_confirmed": true}, "LAUNCH W2": {"organisation_mentions": 12, "evidence_artefact_confirmed": true}}`.

Hours-threshold gate: 0 bad thresholds across 16 v3 Art lesson files. Raw GLH/TQT/guidance contexts, if any, are preserved in `GATES_STATIC.json`.
`new art form` claims: 0.

## PEQ live-vs-v3 unit-code tables

### GROW

| v3 lesson | live counterpart | live unit code(s) | v3 lesson code(s) |
| --- | --- | --- | --- |
| `GROW_Estate_v3/GROW_ASDAN/PEQ_W1_Knowing_Myself.html` | `GROW_ASDAN/PEQ/PEQ_W1_Knowing_Myself.html` | — | — |
| `GROW_Estate_v3/GROW_ASDAN/PEQ_W2_Goals_That_Work.html` | `GROW_ASDAN/PEQ/PEQ_W2_Goals_That_Work.html` | — | — |
| `GROW_Estate_v3/GROW_ASDAN/PEQ_W3_Working_With_Others.html` | `GROW_ASDAN/PEQ/PEQ_W3_Working_With_Others.html` | TmWkSk1 | — |
| `GROW_Estate_v3/GROW_ASDAN/PEQ_W4_Managing_Myself.html` | `GROW_ASDAN/PEQ/PEQ_W4_Managing_Myself.html` | — | — |
| `GROW_Estate_v3/GROW_ASDAN/PEQ_W5_Solving_Problems.html` | `GROW_ASDAN/PEQ/PEQ_W5_Solving_Problems.html` | ThSk1 | — |
| `GROW_Estate_v3/GROW_ASDAN/PEQ_W6_Present_My_Progress.html` | `GROW_ASDAN/PEQ/PEQ_W6_Present_My_Progress.html` | — | — |
| `GROW_Estate_v3/GROW_ASDAN/COMM_W1_Our_Patch_Our_Say.html` | `GROW_ASDAN/Community_Project/GCOMM_W1_Our_Patch_Our_Say.html` | — | — |
| `GROW_Estate_v3/GROW_ASDAN/COMM_W2_Choose_the_Need.html` | `GROW_ASDAN/Community_Project/GCOMM_W2_Choose_the_Need.html` | — | — |
| `GROW_Estate_v3/GROW_ASDAN/COMM_W3_Roles_Steps_Resources.html` | `GROW_ASDAN/Community_Project/GCOMM_W3_Roles_Steps_Resources.html` | TmWkSk1 | — |
| `GROW_Estate_v3/GROW_ASDAN/COMM_W4_First_Contact.html` | `GROW_ASDAN/Community_Project/GCOMM_W4_First_Contact.html` | — | — |
| `GROW_Estate_v3/GROW_ASDAN/COMM_W5_Risk_Ready.html` | `GROW_ASDAN/Community_Project/GCOMM_W5_Risk_Ready.html` | — | — |
| `GROW_Estate_v3/GROW_ASDAN/COMM_W6_Green_Light.html` | `GROW_ASDAN/Community_Project/GCOMM_W6_Green_Light.html` | — | — |
| `GROW_Estate_v3/GROW_ASDAN/ENT_W1_Helps_and_Earns.html` | `GROW_ASDAN/Enterprise/ENT_W1_Helps_and_Earns.html` | — | — |
| `GROW_Estate_v3/GROW_ASDAN/ENT_W2_Spot_the_Gap.html` | `GROW_ASDAN/Enterprise/ENT_W2_Spot_the_Gap.html` | — | — |
| `GROW_Estate_v3/GROW_ASDAN/ENT_W3_Our_Idea_Our_Users.html` | `GROW_ASDAN/Enterprise/ENT_W3_Our_Idea_Our_Users.html` | TmWkSk1 | — |
| `GROW_Estate_v3/GROW_ASDAN/ENT_W4_Money_In_Money_Out.html` | `GROW_ASDAN/Enterprise/ENT_W4_Money_In_Money_Out.html` | — | — |
| `GROW_Estate_v3/GROW_ASDAN/ENT_W5_Brand_and_Pitch.html` | `GROW_ASDAN/Enterprise/ENT_W5_Brand_and_Pitch.html` | — | — |
| `GROW_Estate_v3/GROW_ASDAN/ENT_W6_Pitch_Day.html` | `GROW_ASDAN/Enterprise/ENT_W6_Pitch_Day.html` | — | — |
### LAUNCH

| v3 lesson | live counterpart | live unit code(s) | v3 lesson code(s) |
| --- | --- | --- | --- |
| `LAUNCH_Estate_v3/LAUNCH_ASDAN/PEQ_W1_Intro_Choosing_My_Level.html` | `LAUNCH_ASDAN/PEQ/PEQ_W1_Intro_and_Choosing_My_Level.html` | ComSk1 | ComSk1 |
| `LAUNCH_Estate_v3/LAUNCH_ASDAN/PEQ_W2_What_Makes_Communication_Effective.html` | `LAUNCH_ASDAN/PEQ/PEQ_W2_What_Makes_Communication_Effective.html` | ComSk1 | ComSk1 |
| `LAUNCH_Estate_v3/LAUNCH_ASDAN/PEQ_W3_Active_Listening_Giving_Feedback.html` | `LAUNCH_ASDAN/PEQ/PEQ_W3_Active_Listening_and_Giving_Feedback.html` | ComSk1 | ComSk1 |
| `LAUNCH_Estate_v3/LAUNCH_ASDAN/PEQ_W4_Plan_a_Communication_Activity.html` | `LAUNCH_ASDAN/PEQ/PEQ_W4_Plan_a_Communication_Activity.html` | ComSk1 | ComSk1 |
| `LAUNCH_Estate_v3/LAUNCH_ASDAN/PEQ_W5_Deliver_the_Activity_Gather_Evidence.html` | `LAUNCH_ASDAN/PEQ/PEQ_W5_Deliver_the_Activity_and_Gather_Evidence.html` | ComSk1 | ComSk1 |
| `LAUNCH_Estate_v3/LAUNCH_ASDAN/PEQ_W6_Review_Progress_Sign_Off_the_Unit.html` | `LAUNCH_ASDAN/PEQ/PEQ_W6_Review_Progress_and_Sign_Off_the_Unit.html` | ComSk1 | ComSk1 |
| `LAUNCH_Estate_v3/LAUNCH_ASDAN/CAREERS_W1_Know_Myself_for_Work.html` | `LAUNCH_ASDAN/Careers/CAREERS_W1_Know_Myself_for_Work.html` | — | — |
| `LAUNCH_Estate_v3/LAUNCH_ASDAN/CAREERS_W2_The_World_of_Work_Its_Sectors.html` | `LAUNCH_ASDAN/Careers/CAREERS_W2_The_World_of_Work_and_Its_Sectors.html` | — | — |
| `LAUNCH_Estate_v3/LAUNCH_ASDAN/CAREERS_W3_Labour_Market_Information_Pathways.html` | `LAUNCH_ASDAN/Careers/CAREERS_W3_Labour-Market_Information_and_Pathways.html` | — | — |
| `LAUNCH_Estate_v3/LAUNCH_ASDAN/CAREERS_W4_Meeting_an_Employer.html` | `LAUNCH_ASDAN/Careers/CAREERS_W4_Meeting_an_Employer.html` | — | — |
| `LAUNCH_Estate_v3/LAUNCH_ASDAN/CAREERS_W5_Matching_My_Profile_to_Opportunities.html` | `LAUNCH_ASDAN/Careers/CAREERS_W5_Matching_My_Profile_to_Opportunities.html` | — | — |
| `LAUNCH_Estate_v3/LAUNCH_ASDAN/CAREERS_W6_Setting_SMART_Careers_Targets.html` | `LAUNCH_ASDAN/Careers/CAREERS_W6_Setting_SMART_Careers_Targets.html` | — | — |
| `LAUNCH_Estate_v3/LAUNCH_ASDAN/LI_W1_Self_Care_Routines_Organisation.html` | `LAUNCH_ASDAN/Living_Independently/LI_W1_Self-Care_Routines_and_Organisation.html` | — | — |
| `LAUNCH_Estate_v3/LAUNCH_ASDAN/LI_W2_Home_Safety_Hazard_Awareness.html` | `LAUNCH_ASDAN/Living_Independently/LI_W2_Home_Safety_and_Hazard_Awareness.html` | — | — |
| `LAUNCH_Estate_v3/LAUNCH_ASDAN/LI_W3_Laundry_Household_Maintenance.html` | `LAUNCH_ASDAN/Living_Independently/LI_W3_Laundry_and_Household_Maintenance.html` | — | — |
| `LAUNCH_Estate_v3/LAUNCH_ASDAN/LI_W4_Keeping_a_Clean_Safe_Living_Space.html` | `LAUNCH_ASDAN/Living_Independently/LI_W4_Keeping_a_Clean_Safe_Living_Space.html` | — | — |
| `LAUNCH_Estate_v3/LAUNCH_ASDAN/LI_W5_Personal_Admin_Responsibilities.html` | `LAUNCH_ASDAN/Living_Independently/LI_W5_Personal_Admin_and_Responsibilities.html` | — | — |
| `LAUNCH_Estate_v3/LAUNCH_ASDAN/LI_W6_Plan_Shop_for_a_Balanced_Meal.html` | `LAUNCH_ASDAN/Living_Independently/LI_W6_Plan_and_Shop_for_a_Balanced_Meal.html` | — | — |
| `LAUNCH_Estate_v3/LAUNCH_ASDAN/VOC_W1_Introduction_to_Vocational_Skills_Workplaces.html` | `LAUNCH_ASDAN/Vocational/VOC_W1_Introduction_to_Vocational_Skills_and_Workplaces.html` | — | — |
| `LAUNCH_Estate_v3/LAUNCH_ASDAN/VOC_W2_Health_Safety_Hygiene_at_Work.html` | `LAUNCH_ASDAN/Vocational/VOC_W2_Health_Safety_and_Hygiene_at_Work.html` | — | — |
| `LAUNCH_Estate_v3/LAUNCH_ASDAN/VOC_W3_Following_Instructions_Routines.html` | `LAUNCH_ASDAN/Vocational/VOC_W3_Following_Instructions_and_Routines.html` | — | — |
| `LAUNCH_Estate_v3/LAUNCH_ASDAN/VOC_W4_Teamwork_in_a_Vocational_Setting.html` | `LAUNCH_ASDAN/Vocational/VOC_W4_Teamwork_in_a_Vocational_Setting.html` | — | — |
| `LAUNCH_Estate_v3/LAUNCH_ASDAN/VOC_W5_Tools_Equipment_Safe_Use.html` | `LAUNCH_ASDAN/Vocational/VOC_W5_Tools_Equipment_and_Safe_Use.html` | — | — |
| `LAUNCH_Estate_v3/LAUNCH_ASDAN/VOC_W6_Complete_a_Supported_Vocational_Task.html` | `LAUNCH_ASDAN/Vocational/VOC_W6_Complete_a_Supported_Vocational_Task.html` | — | — |
| `LAUNCH_Estate_v3/LAUNCH_ASDAN/COMM_W1_Identify_a_Community_Need.html` | `LAUNCH_ASDAN/Community_Enterprise/COMM_W1_Identify_a_Community_Need.html` | — | — |
| `LAUNCH_Estate_v3/LAUNCH_ASDAN/COMM_W2_Plan_a_Social_Action_or_Enterprise_Project.html` | `LAUNCH_ASDAN/Community_Enterprise/COMM_W2_Plan_a_Social-Action_or_Enterprise_Project.html` | — | — |
| `LAUNCH_Estate_v3/LAUNCH_ASDAN/COMM_W3_Agree_Roles_Aims_Timeline.html` | `LAUNCH_ASDAN/Community_Enterprise/COMM_W3_Agree_Roles_Aims_and_Timeline.html` | — | — |
| `LAUNCH_Estate_v3/LAUNCH_ASDAN/COMM_W4_Partner_with_a_Local_Group_or_Charity.html` | `LAUNCH_ASDAN/Community_Enterprise/COMM_W4_Partner_with_a_Local_Group_or_Charity.html` | — | — |
| `LAUNCH_Estate_v3/LAUNCH_ASDAN/COMM_W5_Begin_Delivering_the_Project.html` | `LAUNCH_ASDAN/Community_Enterprise/COMM_W5_Begin_Delivering_the_Project.html` | — | — |
| `LAUNCH_Estate_v3/LAUNCH_ASDAN/COMM_W6_Promote_Our_Project.html` | `LAUNCH_ASDAN/Community_Enterprise/COMM_W6_Promote_Our_Project.html` | — | — |

Note: the A2 gate universe is the **48 deployable ASDAN lesson files**. The copied LAUNCH ASDAN **subject hub** already contains `ComSk1` in contextual live-mapping wording from the repaired pack; it was not added by this run. Hub code hits: `{"LAUNCH_Estate_v3/LAUNCH_ASDAN/index.html": ["ComSk1"]}`.

Banned unit-label gate: 0. Communication 10-hour assertion: 0. L2 registration claim in deployable lesson files: 0.

## Sentinels

Expected delta was derived from the repaired pack bytes **before** deployment:
- `ll-g:loop-mark`: 0 new bearing files.
- `What I said, and what it changed`: 0 new bearing files.

Rollback file-set sizes:
- loop: 50
- closure: 113

Working-tree file-set sizes after install:
- loop: 50
- closure: 113

## Reading level — prose only, report only

Selector: BeautifulSoup: script/style/svg/nav/header/footer/form/button/template/noscript removed; select main p, main li, article p, article li, .slide p, .slide li (fallback p/li); exclude ancestors whose class matches print|proute|key-fact|worksheet|evidence-pack.

Instrument: Flesch-Kincaid grade using one deterministic vowel-group syllable heuristic for both live and v3.

| Pathway / subject | lessons | live prose words | live FK | v3 prose words | v3 FK | delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| GROW art | 8 | 5478 | 6.13 | 2047 | 9.12 | 2.99 |
| GROW asdan | 18 | 15947 | 5.47 | 2957 | 8.44 | 2.97 |
| GROW humanities | 8 | 5494 | 6.94 | 1859 | 11.55 | 4.61 |
| LAUNCH art | 8 | 5443 | 6.52 | 2051 | 12.22 | 5.7 |
| LAUNCH asdan | 30 | 20959 | 4.76 | 4782 | 10.43 | 5.67 |
| LAUNCH humanities | 8 | 5571 | 7.38 | 933 | 13.84 | 6.46 |

## Static gates

- Inline scripts: 84 blocks across 94 new HTML files; 0 `node --check` failures.
- Privacy across all new estate HTML: 0 storage · 0 network · 0 `<form>` · 0 `eval(` · 0 external URLs.
- LAUNCH red line: 0 hits across every installed LAUNCH HTML file (universe recorded in `GATES_STATIC.json`).
- Print static gate: 24/24 route-bearing files repaired; 56 screen-only files confirmed as an expected state.
- Internal relative hrefs: 0 unresolved.
- Live invariance: all nine protected trees byte/blob-identical to ROLLBACK_SHA. Blob-manifest digests are in `GATES_STATIC.json`.
- Root sitemap: no `sitemap.xml` exists at ROLLBACK_SHA, so this run did not invent a rival sitemap.

## Complete-universe filename finalisation

- Complete-universe filename finalisation: 80 source lesson paths proved the transform non-vacuous; 64 references across four support pages were normalised; all 94 generated HTML files rechecked at zero residue; support-page HTML references resolved, including 30 retained repository-root source-provenance paths.

## Browser gates and contact sheets

- Boot: 94 installed HTML files; 0 console errors; 0 page errors.
- Print: 24/24 repaired route-bearing lessons passed default-all-three / selected-one / afterprint-clear behavior.
- Catalogue reachability: all 88 new entries are reachable through active 2026-27 + their existing chip; advertised, rendered and JSON-derived chip counts agree in `GATES_BROWSER.json`. Catalogue-shell console diagnostics are recorded separately from the estate boot universe.
- Filename normalization proof: 80 source lesson paths carried the authorised token; generated output was independently rechecked at 0 occurrence(s).
- Contact sheets: 80/80 per-lesson PNGs plus 3 combined subject sheets.
- Combined sheets: `_glv3/contact_sheet/art/combined-art.png`, `_glv3/contact_sheet/asdan/combined-asdan.png`, `_glv3/contact_sheet/humanities/combined-humanities.png`.

## Chip-count browser gate

- Art · Teesside Studio Suite: advertised 81 = returned 81 = JSON-derived 81; 18/18 new GLV3 entries reachable in active 2026-27.
- GROW Vocational & PfA: advertised 42 = returned 42 = JSON-derived 42; 20/20 new GLV3 entries reachable in active 2026-27.
- Humanities: advertised 59 = returned 59 = JSON-derived 59; 18/18 new GLV3 entries reachable in active 2026-27.
- LAUNCH Vocational & PfA: advertised 68 = returned 68 = JSON-derived 68; 32/32 new GLV3 entries reachable in active 2026-27.
