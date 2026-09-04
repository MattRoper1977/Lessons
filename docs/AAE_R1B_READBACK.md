# AAE-R1B readback — draft awaiting ordered merges and closeout

**Bronze workbook cells: 0 → 0 (AAE-H7). Gold new cells: 0, printed separately.**

All **42 authorised new decks are authored and built**: Bronze 14, Explore 14, Silver 14. Each level is a separate 14-unit batch, below the 24-unit ceiling. At the checkpoint supplied for this draft, Bronze is merged; Explore and Silver are awaiting their ordered merges. Do not convert the 42 built count into a 42 shipped count until the merge records below are completed. Registers, gates, the R2 repair, census, placement, Gold documentation and catalogue changes count zero lesson units.

This draft reads current local source and evidence without changing Lessons. Paths below are repository-relative. It distinguishes historical reports, fresh checks and pending publication. The controlling register is `tools/artsaward/SPEC.json`, SHA-256 `e57b5bfbdd48a4b9973131cbcb544e0abc2c87aa2a2e6dd0f9a60cf8fa791d49`.

## Merge and delivery checkpoint — root must update before final publication

| Work | Status at this draft | Exact evidence / outstanding field |
|---|---|---|
| Register and original g30–g35, PR #299 | Merged historical prerequisite | `202cee92e0dcbefb9686cf2e0626f2fee413e765` |
| Original R2 classification and R3(i) census, PR #300 | Merged historical prerequisite | `9fd27b1bf95ab3822ff27bc4862d53368e55f518` |
| Plan binding and presentation mechanism, PR #303 | Merged | `4f36647151a525911e3dfd15b7d502b3c198ac9a`; 18/18 changed blobs verified |
| Bronze 14, PR #304 | Merged | Head `856d2a88ddc37bfbc829f144e7b465d1ee92ae7d`; actual fork `4f36647151a525911e3dfd15b7d502b3c198ac9a`; merge `2f7eda8e62096cd23fef8128b92c3563ed170bc3`; 58/58 changed blobs verified |
| Assertion/multipart gates, PR #305 | Root to refresh | **PENDING: merge SHA, exact head, actual fork, blob count and current-head checks** |
| R2 functioning slot-reader/prose follow-up, PR #306 | Root to refresh | **PENDING: merge SHA, exact head, actual fork, blob count and current-head checks** |
| Explore 14, PR #307 | Built; merge pending | **PENDING: merge SHA, exact head, actual fork, blob count and current-head checks** |
| Silver 14, PR #308 | Built; merge pending | **PENDING: merge SHA, exact head, actual fork, blob count and current-head checks** |
| Bronze→GROW and Silver→LAUNCH placement | Pending separate zero-unit PR | **PENDING: actual rows, destinations, PR and merge proof** |
| Gold shelf OPEN record | Pending zero-unit documentation closeout | **PENDING: final document PR and merge proof** |
| Catalogue | Pending; last, alone, per batch | **PENDING: each batch’s catalogue PR, count and merge proof** |

Every merge must be compared with its own actual fork base. Later changes already on main are not branch reversions. No terminal campaign token is claimed in this draft.

## R2: the required eleven MIMA mentions

The original evidence contains **11 teaching-deck mentions on 10 physical lines**, because one line contains MIMA twice. The result is **10 EXAMPLE retained and 1 ASSERTED converted**. It is not 9 retained and 2 converted. The table below is generated from `venue_classification_before.json`; line numbers refer to that original snapshot.

| # | Original file | Line | Original context | Classification/action |
|---:|---|---:|---|---|
| 1 | `Art_Teesside/Build/BUILD_ART_A2_W2_Arts_Inspiration.html` | 341 | `lick="presTap(this)">👥 Mackenzie Thorpe 🖼️ MIMA 🛠️ A local maker <div class="pres-ca` | EXAMPLE — retained |
| 2 | `Art_Teesside/Build/BUILD_ART_A2_W2_Arts_Inspiration.html` | 341 | `> 2. Name your organisation. MIMA or own answer. 3. What are you taking f` | EXAMPLE — retained |
| 3 | `Art_Teesside/Build/BUILD_ART_A2_W2_Arts_Inspiration.html` | 342 | `ng> Teesside figures and industry, heavy outline and simplified form — feeling before accuracy. MIMA ORGANISATION. Middlesbrough Institute of Modern Art — shows contemporary work and r` | EXAMPLE — retained |
| 4 | `Art_Teesside/Build/BUILD_ART_A2_W2_Arts_Inspiration.html` | 407 | `Why must the third column be locatable?"}, "We Do 1": {"F": "Which cards are organisations?", "M": "What does MIMA actually do?", "S": "How does a community studio differ from a gallery?"}, "Independent Work": {"F": "Which a` | EXAMPLE — retained |
| 5 | `Art_Teesside/Build/BUILD_ART_W2_Artists_Makers_and_Teesside_Connections.html` | 359 | `> 3. Organisations (Recall) Name a place near here where art is shown or made. MIMA, local galleries, community studios, street walls.` | EXAMPLE — retained |
| 6 | `Art_Teesside/Build/BUILD_ART_W2_Artists_Makers_and_Teesside_Connections.html` | 365 | `pan class="country-badge">People in place 🖼️ MIMA A modern gallery in the middle of town Organisation <div cl` | EXAMPLE — retained |
| 7 | `Art_Teesside/Build/BUILD_ART_W2_Artists_Makers_and_Teesside_Connections.html` | 377 | `" onclick="presTap(this)">🖨️ Printmaker 🖼️ MIMA (organisation) 🏺 Ceramicist` | EXAMPLE — retained |
| 8 | `Art_Teesside/Build/BUILD_ART_W2_Artists_Makers_and_Teesside_Connections.html` | 412 | `tence. 3. Name one Teesside arts organisation. MIMA (or any local gallery/studio).` | EXAMPLE — retained |
| 9 | `Art_Teesside/Build/BUILD_ART_W2_Artists_Makers_and_Teesside_Connections.html` | 427 | `"margin-top:12px">Key Facts Artists have worked the Tees as a subject for over 150 years. MIMA sits in the middle of Middlesbrough — art organisations are local, not distant. Part B evidence = you` | EXAMPLE — retained |
| 10 | `Art_Teesside/Build/BUILD_ART_W2_Artists_Makers_and_Teesside_Connections.html` | 431 | `er 🏭 Industrial landscape painter, 📷 Documentary photographer, 🎨 Community muralist, 🖨️ Printmaker, 🖼️ MIMA (organisation), 🏺 Ceramicist` | EXAMPLE — retained |
| 11 | `Art_Teesside/Grow/GROW_ART_W4_Arts_Event_Attend_Capture_and_Review.html` | 359 | `nt-size="10" fill="#fff">ADMIT ONE MIMA · GALLERY · SHOW <rect x="240" y="52" width="110" height` | ASSERTED — hardcoded MIMA removed from ticket; drawing retained; functioning slot follow-up below |

The wider search counted **20 mentions before: 19 EXAMPLE, 1 ASSERTED**. The extra nine are organisation-teaching examples in the Build, Grow and Launch Spring 2 source-card packs. All remain. After the original conversion, the classifier records **19 mentions, all EXAMPLE**. The teaching-deck venue-line count falls from ten in three decks to nine in two decks; the remainder are teaching examples, not outstanding visit assertions.

The original PR #300 removed MIMA from the ticket but did not actually wire that legacy deck to a live slot reader. A subsequent prose review also found assertions the regex census missed: “Tonight”, “this week’s visit”, promised audience attendance, a venue asking for reviews, and an unsupported claim that a prior cohort changed a label height. The R2 follow-up corrects these statements and installs a real `ORG_SLOT` reference alongside the applicable `EVENT_SLOT` readiness check. An organisation being named does not establish that a pupil attended an event. Empty or invalid slots leave preparation labelled as preparation; an actually undertaken online exhibition remains a legitimate audience experience.

The follow-up preserves all ten legacy stages, their metadata, styles, SVGs and cell tokens. Its embedded reader matches `tools/artsaward/slot_reader.js`, reads `../../tools/artsaward/SLOTS.json`, supports a local file picker offline, renders values as text, and rejects stale async responses. Local adapter evidence records 12/12 controls. Root’s checked browser checkpoint is run **33919123514**, job **101173117156**, successful. Its merge status remains the pending PR #306 row above until refreshed.

Sources: `_sownb/vb/evidence/aae/venue_classification_{before,after}.json`, `r2-adapter-checks.json`, `r2-structural-checks.json`, and the actual GROW W4 file.

## R3(i): what the historical census establishes

**76 is the order/register-era description; 82 is the measured claim-scoped census after batch 4.** The stored survey scanned 136 files and found 82 award-scoped, deck-shaped files: 66 under `Art_Teesside`, eight under `BUILD_Estate_v3`, and eight under `GROW_Estate_v3`. It inferred Bronze in 29, Explore in 26, Silver in 20, and no level in seven. All 82 were undeclared to the new award gates at that historical snapshot. The archived g30 report therefore records 82 undeclared RED rows: a scope/declaration result, not evidence of 82 factual teaching errors.

The survey found zero matches in seven narrow categories: incorrect level name, incorrect qualification number, UCAS outside Gold, leadership in inferred Explore, dated events, asserted visits, and its limited invented-requirement patterns. Its eighth category retained MIMA examples in two files and must be read with R2. The census recorded **zero lesson units**. That regex zero was not a semantic sign-off: the later R2 prose findings demonstrate the limitation. The complete measured **82-file list** is printed below rather than relabelled as a 76-row artefact.

## Measured delivery by level

Word bands come from `tools/easter/BATCH4_WORD_TARGETS.json`. Teaching-word counts and pupil Flesch–Kincaid use different extraction measures; neither is substituted for the other. Each pack contains fourteen lesson HTML files, `START_HERE.html`, a manifest and a 16-file checksum list. Generated print content comes from the same source blocks as the board content.

| Level | Built | Teaching words | Required Art word band | Pupil FK | Required FK | New workbook cells | Placement |
|---|---:|---:|---:|---:|---:|---|---|
| Bronze | 14 | 1092–1333 | 888–1523 | 2.08–3.60 | 1–4 | 0 → 0 (AAE-H7) | BUILD canonical; GROW row pending |
| Explore | 14 | 1091–1308 | 888–1523 | 2.52–4.00 | 1–4 | 0 → 0 (independent review) | BUILD only |
| Silver | 14 | 1073–1287 | 902–1378 | 5.34–6.28 | 3–7 | 0 → 0 (independent review) | GROW canonical; LAUNCH row pending |

Each level is a **560-minute / 9-hour-20-minute teaching spine**, not the whole award programme. SPEC totals are Bronze 60 hours, Explore 35 hours and Silver 95 hours. Additional actual practice, experiences, practitioner contact and delivery must be arranged and recorded; preparation pages do not establish completed participation.

### Evidence organisation and staff rules

| Level | Suggested cumulative files | Actual pupil files supplied/verified | Cap | Assessment and completion rule |
|---|---:|---|---:|---|
| Bronze | 4: A, B, C, D | Unknown — authoring decks supplies no pupil portfolio | 10 | Three assessment areas; one Attempted overall; any Not Attempted = Below Pass |
| Explore | 4: A, B, C, D | Unknown — authoring decks supplies no pupil portfolio | 10 | Three assessment areas; one Attempted overall; any Not Attempted = Below Pass |
| Silver | 9: one per part; two clearly sectioned unit files also possible | Unknown — authoring decks supplies no pupil portfolio | 20 across Silver | Four assessment areas; one Attempted per unit; any Not Attempted = Below Pass; units separately evidenced |

These are suggested filing options, not extra award rules. File/page/slide/timecode locators must identify the pupil’s real evidence. Fourteen teaching decks are not fourteen pupil evidence files. The three shared assessment areas are art form knowledge and understanding, creativity, and communication; Silver additionally assesses planning and review. Staff blocks name the part(s) taught and retain the required rule, cap and adviser/centre conditions.

### Part-to-serving-deck map

The rows below come from each canonical target register and built `lesson-config`. Multipart Silver rows retain both parts. A serving deck teaches and supports evidence production; it does not certify a pupil’s completion.

#### Bronze

| Plan index | Week | Part(s) | Serving deck | Slots declared and read |
|---:|---:|---|---|---|
| 1001 | 1 | A | `Art_Teesside/BUILD_BRONZE_W1-W7_2026-27/BUILD_Art_Bronze_W1_Where_My_Art_Is_Now.html` | None required |
| 1002 | 1 | A | `Art_Teesside/BUILD_BRONZE_W1-W7_2026-27/BUILD_Art_Bronze_W1_What_Getting_Better_Would_Look_Like.html` | None required |
| 1003 | 2 | A | `Art_Teesside/BUILD_BRONZE_W1-W7_2026-27/BUILD_Art_Bronze_W2_Practise_The_Skill_Session_One.html` | None required |
| 1004 | 2 | A | `Art_Teesside/BUILD_BRONZE_W1-W7_2026-27/BUILD_Art_Bronze_W2_Practise_The_Skill_And_Take_One_Piece_Of_Feedback.html` | None required |
| 1005 | 3 | A | `Art_Teesside/BUILD_BRONZE_W1-W7_2026-27/BUILD_Art_Bronze_W3_Make_The_Change_The_Feedback_Asked_For.html` | None required |
| 1006 | 3 | A | `Art_Teesside/BUILD_BRONZE_W1-W7_2026-27/BUILD_Art_Bronze_W3_What_Improved_In_My_Own_Words.html` | None required |
| 1007 | 4 | B | `Art_Teesside/BUILD_BRONZE_W1-W7_2026-27/BUILD_Art_Bronze_W4_What_An_Audience_Member_Actually_Does.html` | EVENT_SLOT |
| 1008 | 4 | B | `Art_Teesside/BUILD_BRONZE_W1-W7_2026-27/BUILD_Art_Bronze_W4_The_Review_Frame_Before_The_Experience.html` | EVENT_SLOT |
| 1009 | 5 | B | `Art_Teesside/BUILD_BRONZE_W1-W7_2026-27/BUILD_Art_Bronze_W5_The_Experience_Captured.html` | EVENT_SLOT |
| 1010 | 5 | C | `Art_Teesside/BUILD_BRONZE_W1-W7_2026-27/BUILD_Art_Bronze_W5_Choosing_A_Practitioner_And_Saying_Why.html` | None required |
| 1011 | 6 | C | `Art_Teesside/BUILD_BRONZE_W1-W7_2026-27/BUILD_Art_Bronze_W6_Their_Practice_Career_Life_And_Work.html` | None required |
| 1012 | 6 | D | `Art_Teesside/BUILD_BRONZE_W1-W7_2026-27/BUILD_Art_Bronze_W6_Plan_The_Skills_Share.html` | None required |
| 1013 | 7 | D | `Art_Teesside/BUILD_BRONZE_W1-W7_2026-27/BUILD_Art_Bronze_W7_Deliver_The_Skills_Share.html` | None required |
| 1014 | 7 | D | `Art_Teesside/BUILD_BRONZE_W1-W7_2026-27/BUILD_Art_Bronze_W7_Review_The_Share_And_Find_The_Evidence.html` | None required |

#### Explore

| Plan index | Week | Part(s) | Serving deck | Slots declared and read |
|---:|---:|---|---|---|
| 2001 | 1 | A | `Art_Teesside/BUILD_EXPLORE_W1-W7_2026-27/BUILD_Art_Explore_W1_Try_Drawing_With_Line.html` | None required |
| 2002 | 1 | A | `Art_Teesside/BUILD_EXPLORE_W1-W7_2026-27/BUILD_Art_Explore_W1_Use_Tone_And_Say_What_I_Learnt.html` | None required |
| 2003 | 2 | A | `Art_Teesside/BUILD_EXPLORE_W1-W7_2026-27/BUILD_Art_Explore_W2_Build_With_Folded_Paper.html` | None required |
| 2004 | 2 | A | `Art_Teesside/BUILD_EXPLORE_W1-W7_2026-27/BUILD_Art_Explore_W2_Test_A_Join_And_Compare_My_Learning.html` | None required |
| 2005 | 3 | B | `Art_Teesside/BUILD_EXPLORE_W1-W7_2026-27/BUILD_Art_Explore_W3_Get_Ready_To_Explore_An_Artist_And_Organisation.html` | ORG_SLOT, PRACTITIONER_SLOT |
| 2006 | 3 | B | `Art_Teesside/BUILD_EXPLORE_W1-W7_2026-27/BUILD_Art_Explore_W3_Explore_An_Artist_Through_A_Live_Activity.html` | ORG_SLOT, PRACTITIONER_SLOT |
| 2007 | 4 | B | `Art_Teesside/BUILD_EXPLORE_W1-W7_2026-27/BUILD_Art_Explore_W4_Explore_What_An_Arts_Organisation_Does.html` | ORG_SLOT, PRACTITIONER_SLOT |
| 2008 | 4 | B | `Art_Teesside/BUILD_EXPLORE_W1-W7_2026-27/BUILD_Art_Explore_W4_Connect_The_Artist_Organisation_And_What_I_Found.html` | ORG_SLOT, PRACTITIONER_SLOT |
| 2009 | 5 | C | `Art_Teesside/BUILD_EXPLORE_W1-W7_2026-27/BUILD_Art_Explore_W5_Choose_A_New_Artwork_To_Make.html` | None required |
| 2010 | 5 | C | `Art_Teesside/BUILD_EXPLORE_W1-W7_2026-27/BUILD_Art_Explore_W5_Start_Making_And_Keep_The_Process.html` | None required |
| 2011 | 6 | C | `Art_Teesside/BUILD_EXPLORE_W1-W7_2026-27/BUILD_Art_Explore_W6_Develop_The_Work_And_Record_A_Choice.html` | None required |
| 2012 | 6 | C | `Art_Teesside/BUILD_EXPLORE_W1-W7_2026-27/BUILD_Art_Explore_W6_Finish_The_Artwork_And_Show_Its_Making.html` | None required |
| 2013 | 7 | D | `Art_Teesside/BUILD_EXPLORE_W1-W7_2026-27/BUILD_Art_Explore_W7_Look_Back_And_Choose_What_To_Share.html` | None required |
| 2014 | 7 | D | `Art_Teesside/BUILD_EXPLORE_W1-W7_2026-27/BUILD_Art_Explore_W7_Share_My_Enjoyment_Or_Achievement.html` | None required |

#### Silver

| Plan index | Week | Part(s) | Serving deck | Slots declared and read |
|---:|---:|---|---|---|
| 3001 | 1 | 1A | `Art_Teesside/GROW_SILVER_W1-W7_2026-27/GROW_Art_Silver_W1_Choose_My_Arts_Challenge.html` | None required |
| 3002 | 1 | 1A | `Art_Teesside/GROW_SILVER_W1-W7_2026-27/GROW_Art_Silver_W1_Make_My_Own_Action_Plan.html` | None required |
| 3003 | 2 | 1B | `Art_Teesside/GROW_SILVER_W1-W7_2026-27/GROW_Art_Silver_W2_Try_Record_And_Refine.html` | None required |
| 3004 | 2 | 1C | `Art_Teesside/GROW_SILVER_W1-W7_2026-27/GROW_Art_Silver_W2_Experience_Review_And_Share.html` | EVENT_SLOT |
| 3005 | 3 | 1D | `Art_Teesside/GROW_SILVER_W1-W7_2026-27/GROW_Art_Silver_W3_Meet_A_Practitioner_And_Trace_A_Path.html` | ORG_SLOT, PRACTITIONER_SLOT |
| 3006 | 3 | 1B | `Art_Teesside/GROW_SILVER_W1-W7_2026-27/GROW_Art_Silver_W3_Compare_The_Reviews_And_Judge_Progress.html` | None required |
| 3007 | 4 | 2A | `Art_Teesside/GROW_SILVER_W1-W7_2026-27/GROW_Art_Silver_W4_Plan_My_Arts_Project_And_Role.html` | None required |
| 3008 | 4 | 2B | `Art_Teesside/GROW_SILVER_W1-W7_2026-27/GROW_Art_Silver_W4_Make_The_Practical_Plan.html` | None required |
| 3009 | 5 | 2B, 2D | `Art_Teesside/GROW_SILVER_W1-W7_2026-27/GROW_Art_Silver_W5_Test_The_Plan_With_The_Team.html` | None required |
| 3010 | 5 | 2C, 2D | `Art_Teesside/GROW_SILVER_W1-W7_2026-27/GROW_Art_Silver_W5_Lead_The_Project_In_Action.html` | None required |
| 3011 | 6 | 2C, 2D | `Art_Teesside/GROW_SILVER_W1-W7_2026-27/GROW_Art_Silver_W6_Continue_The_Project_And_Adapt.html` | None required |
| 3012 | 6 | 2D | `Art_Teesside/GROW_SILVER_W1-W7_2026-27/GROW_Art_Silver_W6_Work_Well_With_Others.html` | None required |
| 3013 | 7 | 2E | `Art_Teesside/GROW_SILVER_W1-W7_2026-27/GROW_Art_Silver_W7_Review_My_Leadership_Project.html` | None required |
| 3014 | 7 | 2E | `Art_Teesside/GROW_SILVER_W1-W7_2026-27/GROW_Art_Silver_W7_Find_The_Evidence_Across_Both_Units.html` | None required |

Bronze keeps participant baseline/practice/feedback/refinement/review across A1–A6; actual audience experience, review and shared views in B1–B3; a chosen real practitioner’s practice/career/life/work in C1–C2; and planning/delivery/review of an actual skills share in D1–D3. Part B supports the three routes without asserting a booking; an online exhibition can be a real experience.

Explore retains A’s two activities (drawing and paper construction), B’s live/active artist **and** organisation exploration, C’s distinct artwork/process/final work, and D’s communication of chosen enjoyment or achievement. The original AAE §5 was not recovered in this session; medium choices, theme and exact week allocation are explicitly recorded as conservative implementation choices, not quotations from that unseen clause.

Silver 1C and 1D are full decks. 1C requires an actual audience experience, review and evidenced sharing. 1D requires first-hand practitioner contact, organisation research, education **and** career pathways, and a personal influence summary. 1A retains pupil ownership of challenge and plan; 1B includes someone else’s review and the pupil’s own. Unit 2 serves 2A–2E separately, and final 2E lists **1A, 1B, 1C, 1D, 2A, 2B, 2C, 2D, 2E**.

### Shared slots

`SLOTS.json` remains unconfirmed: all four `entries` arrays are empty. Candidate names are options, not bookings. No pupil attendance, meeting or public showing is claimed.

| Slot | New serving decks | Current contents/boundary |
|---|---|---|
| EVENT_SLOT | Bronze 1007–1009; Silver 3004 | Empty; actual audience experience needed before the corresponding evidence is complete |
| ORG_SLOT | Explore 2005–2008; Silver 3005; legacy R2 reference | Empty; an organisation entry alone does not confirm an event |
| PRACTITIONER_SLOT | Explore 2005–2008; Silver 3005 | Empty; desk research/archives/video do not replace required first-hand or live/active work |
| SHOWING_SLOT | No compulsory new Bronze, Explore or Silver declaration | Empty; Gold 2D shelf use. Silver leadership does not acquire a mandatory public showing |

Routes remain R1 pupils visit, R2 visitors come in, R3 live remote exchange. Shared slots can be updated without rewriting each lesson. Current hosted/offline readers are tested; that does not imply any candidate is confirmed.

### Workbook cells and placement

Bronze’s **0 → 0** follows AAE-H7. It has fourteen award-plan identities, with no invented workbook-cell claim. Explore and Silver were reviewed independently and do not inherit a blanket H7 ruling.

Explore compared all 24 BUILD Art targets: seven already claimed and 17 unclaimed. One narrow full-action overlap was found (Spring C93, adding a review to the arts log), but it is ruled week 21 rather than proposed week 2 and remains the existing Discover workbook strand. No cell was reassigned. Silver compared all 39 GROW Art workbook/spine values with zero mismatches and the 23 Easter targets. Six target cells have claims and 17 are unclaimed. All ruled W1–7 Art cells already have claimants. Autumn C103 has a plausible same-week skill/record action but is already owned; unclaimed Spring C89 repeats that action at week 17 rather than Silver week 2. **Zero new claims result from either independent review.**

The proposed secondary placements point to the same canonical decks and retain the measured band, plan and cell set. They add zero units and no duplicated copy. Actual placement rows and merge proofs remain pending above. Sources: `_sownb/vb/AAE_EXPLORE_CELL_REVIEW.md`, `_sownb/vb/AAE_SILVER_CELL_REVIEW.md`, and the three canonical plan/target registers.

## g30–g35 and mechanism controls

A fresh read-only call to the current `g30_arts_award.judge()` from `Lessons-Award-Gates` against all 42 built files in `Lessons-Silver` returned **Bronze 14 PASS / Explore 14 PASS / Silver 14 PASS**, zero RED and zero SKIP. This differs from the archived per-level report versions: Bronze records v1.0.0, Explore v1.1.0 and Silver v1.1.1. The fresh check uses the current v1.1.1 attendance-reference logic for all three.

The latest `Lessons-Award-Gates/_sownb/vb/evidence/aae/battery_assertion_scope.json` records **28 tools, 347 declared controls, all fired**, including **67 g30–g35 controls**. `--prove-red` planted an incorrect expected value in a stage control: the broken tool exited 1 and the battery turned red. The older inherited report in the content worktrees records 323 controls and must not be mislabelled as the latest result.

| Gate | Scope of protection | Current result |
|---|---|---|
| g30 | Correct award identity/numbers/rules/caps; progress counts not mistaken for caps; Gold unknowns retained | Controls fired within the 67-control suite; all 42 decks pass |
| g31 | Correct part/unit purpose; truthful negative challenge restrictions allowed; no leadership-only Silver practice challenge | Controls fired; all 42 pass |
| g32 | Asserted attendance, bookings, dated venues, promised practitioner contact and missing required slots; legitimate teaching/ticket/evidence examples retained | Permanent must-fire controls retained; truthful denials/questions pass while adjacent positive assertions still red; all 42 pass |
| g33 | Complete registered parts when a portfolio is listed, including all nine Silver parts | Controls fired; all 42 pass |
| g34 | Required review sharing with evidence; a draft peer swap alone fails | Controls fired; all 42 pass |
| g35 | No invented compulsory file format, Gantt requirement or unsupported Gold rule | Controls fired; all 42 pass |

The comparative nine-gate build result is 14/14 for each level, with zero detected donor-language leaks. It is **not** nine fresh green gates on every deck: g16, g19 and g24 are explicitly `PRE-EXISTING` donor outcomes; g18, g23, g25, g26, g28 and g29 pass.

Root’s independently checked browser checkpoint is run **33920405525**, job **101177167095**, covering all 42 source/print packs. It verifies navigation, toolbar/focus behaviour, shared-slot reading and actual print invocation. **This is not PDF pagination or physical print-fit proof.** Retain the tested head and final ordered-merge CI references in the final closeout.

## Gold shelf — separate from new authoring

**Gold: 0 new decks; 0 new cells.** It remains LAUNCH-only on the shelf until AAE-H6 (a named Gold entrant). No exemplar binaries were imported or treated as committed decks. The voided exemplar repairs are not claimed as completed; their findings remain in SPEC and the gates.

The required OPEN record is against `SPEC.json`, not absent decks:

| OPEN item | Register reference | Required actual evidence/condition |
|---|---|---|
| 1A: new art form with experienced practitioner | `levels.Gold.parts.1A` | New-form skills with an experienced practitioner; actual new work, sharing and review |
| 1B: placement/volunteering with leading practitioner comments | `levels.Gold.parts.1B` | Actual career-development activity, including the comments of its leading practitioner |
| 1C: reviews of events attended | `levels.Gold.parts.1C` | Actually attended arts experiences and reviews, alongside registered practitioner/organisation research |
| 2D: a PUBLIC showing | `levels.Gold.parts.2D` | Actual public showing arrangements/delivery/responsibilities, participant and audience feedback |

Gold’s Attempted rule and file cap remain **UNKNOWN/null**; Silver’s rules are not copied across. AAE-H1–H5 remain recorded conditions/defaults, not asserted completion. The final Gold documentation merge remains pending above.

## Complete historical R3(i) measured census list: 82 files

This reproduces `contamination.json` at the post-batch-4 historical snapshot. “None in tested patterns” means exactly that, not semantic certification. “Undetermined” is an inferred-level result. All 82 were undeclared at that snapshot. The new award packs are not retroactively added to that denominator.

| # | File | Inferred level | Stored pattern findings |
|---:|---|---|---|
| 1 | `Art_Teesside/BUILD_W1-W8_2026-27/BUILD_Art_W1_Explore_Drawing_Colour_And_Technique_To_Show.html` | Undetermined | None in tested patterns |
| 2 | `Art_Teesside/BUILD_W1-W8_2026-27/BUILD_Art_W2_Create_An_Identity_Piece_Using_A_Chosen.html` | Undetermined | None in tested patterns |
| 3 | `Art_Teesside/BUILD_W1-W8_2026-27/BUILD_Art_W3_Find_Out_About_An_Artist_Whose_Work.html` | Undetermined | None in tested patterns |
| 4 | `Art_Teesside/BUILD_W1-W8_2026-27/BUILD_Art_W4_Try_A_New_Art_Technique_And_Review.html` | Undetermined | None in tested patterns |
| 5 | `Art_Teesside/BUILD_W1-W8_2026-27/BUILD_Art_W5_Add_To_My_Arts_Log_Photo_Comment.html` | Undetermined | None in tested patterns |
| 6 | `Art_Teesside/BUILD_W1-W8_2026-27/BUILD_Art_W6_Share_My_Identity_Piece_With_The_Group.html` | Undetermined | None in tested patterns |
| 7 | `Art_Teesside/BUILD_W1-W8_2026-27/BUILD_Art_W7_Reflect_On_Identity_In_My_Artwork.html` | Undetermined | None in tested patterns |
| 8 | `Art_Teesside/Build/BUILD_ART_A2_W1_Surface_Hunt.html` | Bronze | None in tested patterns |
| 9 | `Art_Teesside/Build/BUILD_ART_A2_W2_Arts_Inspiration.html` | Bronze | [{'what': 'a venue named in the deck rather than in SLOTS.json', 'line': 341, 'text': '</div></div></div><div class="slide" data-title="Arrival Task" data-timer="3" id="arrival-slide"> <span class="slide-tag'}, {'what': 'a venue named in the deck rather than in SLOTS.json', 'line': 342, 'text': '<div id="print-area"><div id="print-ko" class="print-section"><h2>Knowledge Organiser</h2><div class="prevent-break"><ta'}, {'what': 'a venue named in the deck rather than in SLOTS.json', 'line': 407, 'text': 'const _ccQuestions={"Title": {"F": "What are we finding out about artists today?", "M": "What makes research count as ev'}] |
| 10 | `Art_Teesside/Build/BUILD_ART_A2_W3_Stencil_Lab.html` | Bronze | None in tested patterns |
| 11 | `Art_Teesside/Build/BUILD_ART_A2_W4_Audience_Week.html` | Bronze | None in tested patterns |
| 12 | `Art_Teesside/Build/BUILD_ART_A2_W5_Layer_and_Combine.html` | Bronze | None in tested patterns |
| 13 | `Art_Teesside/Build/BUILD_ART_A2_W6_Resolve_and_Edition.html` | Bronze | None in tested patterns |
| 14 | `Art_Teesside/Build/BUILD_ART_A2_W7_Bank_It_and_Plan_the_Teach.html` | Bronze | None in tested patterns |
| 15 | `Art_Teesside/Build/BUILD_ART_W1_The_Local_Canvas.html` | Explore | None in tested patterns |
| 16 | `Art_Teesside/Build/BUILD_ART_W2_Artists_Makers_and_Teesside_Connections.html` | Explore | [{'what': 'a venue named in the deck rather than in SLOTS.json', 'line': 359, 'text': '<div id="arrival-standard" class="arrival-grid" style="display:none"><div class="task-box animate-enter"><h3>1. Retrieva'}, {'what': 'a venue named in the deck rather than in SLOTS.json', 'line': 365, 'text': '<div class="product-grid"><div class="product-card"><div class="icon">🏭</div><h4>The Industrial Painters</h4><p>Furnace '}, {'what': 'a venue named in the deck rather than in SLOTS.json', 'line': 377, 'text': '<div style="display:flex;flex-wrap:wrap;gap:8px;justify-content:center;margin:8px 0" id="pres-pills"><div class="pres-ca'}, {'what': 'a venue named in the deck rather than in SLOTS.json', 'line': 412, 'text': '<div id="exit-supported" class="arrival-grid"><div class="task-box"><h3>1.</h3><p>Name the four analysis moves.</p><p cl'}, {'what': 'a venue named in the deck rather than in SLOTS.json', 'line': 427, 'text': '<h2 style="margin-top:12px">Key Facts</h2><ul><li>Artists have worked the Tees as a subject for over 150 years.</li><li>'}, {'what': 'a venue named in the deck rather than in SLOTS.json', 'line': 431, 'text': '<div class="stretch-content"><p>1) Why label every sketchbook experiment?</p><div class=\'print-line\'></div><p>2) Content'}] |
| 17 | `Art_Teesside/Build/BUILD_ART_W3_Industrial_Surface_Skills_Lab.html` | Explore | None in tested patterns |
| 18 | `Art_Teesside/Build/BUILD_ART_W4_Build_the_Brief.html` | Explore | None in tested patterns |
| 19 | `Art_Teesside/Build/BUILD_ART_W5_Critique_Test_and_Redirect.html` | Explore | None in tested patterns |
| 20 | `Art_Teesside/Build/BUILD_ART_W6_Resolve_the_Artwork.html` | Explore | None in tested patterns |
| 21 | `Art_Teesside/Build/BUILD_ART_W7_Curate_the_Showcase.html` | Explore | None in tested patterns |
| 22 | `Art_Teesside/Build/BUILD_ART_W8_Share_Reflect_and_Close_the_Loop.html` | Explore | None in tested patterns |
| 23 | `Art_Teesside/Build/Spring2_2026-27/BUILD_ART_Spring2_W1_Armature_and_Frame_OUTSTANDING_V3.html` | Explore | None in tested patterns |
| 24 | `Art_Teesside/Build/Spring2_2026-27/BUILD_ART_Spring2_W2_Scale_and_Negative_Space_OUTSTANDING_V3.html` | Explore | None in tested patterns |
| 25 | `Art_Teesside/Build/Spring2_2026-27/BUILD_ART_Spring2_W3_Surface_and_Patination_OUTSTANDING_V3.html` | Explore | None in tested patterns |
| 26 | `Art_Teesside/Build/Spring2_2026-27/BUILD_ART_Spring2_W4_Contextual_Study_Kapoor_Whiteread_Barlow_OUTSTANDING_V3.html` | Explore | None in tested patterns |
| 27 | `Art_Teesside/Build/Spring2_2026-27/BUILD_ART_Spring2_W5_Site_Integration_OUTSTANDING_V3.html` | Explore | None in tested patterns |
| 28 | `Art_Teesside/Build/Spring2_2026-27/BUILD_ART_Spring2_W6_Proposal_Pitch_and_Review_OUTSTANDING_V3.html` | Explore | None in tested patterns |
| 29 | `Art_Teesside/GROW_W1-W8_2026-27/GROW_Art_W2_Develop_A_Skill_And_Record_It_In.html` | Explore | None in tested patterns |
| 30 | `Art_Teesside/GROW_W1-W8_2026-27/GROW_Art_W3_Plan_An_Identity_Portrait_Or_Piece.html` | Explore | None in tested patterns |
| 31 | `Art_Teesside/GROW_W1-W8_2026-27/GROW_Art_W4_Create_My_Identity_Piece_BHM_Artist_Inspiration.html` | Explore | None in tested patterns |
| 32 | `Art_Teesside/GROW_W1-W8_2026-27/GROW_Art_W5_Review_And_Improve_My_Work.html` | Explore | None in tested patterns |
| 33 | `Art_Teesside/Grow/GROW_ART_W1_The_Local_Canvas.html` | Bronze | None in tested patterns |
| 34 | `Art_Teesside/Grow/GROW_ART_W2_Studio_Skills_and_Safe_Practice.html` | Bronze | None in tested patterns |
| 35 | `Art_Teesside/Grow/GROW_ART_W3_Independent_Studio_Challenge.html` | Bronze | None in tested patterns |
| 36 | `Art_Teesside/Grow/GROW_ART_W4_Arts_Event_Attend_Capture_and_Review.html` | Bronze | None in tested patterns |
| 37 | `Art_Teesside/Grow/GROW_ART_W5_Practitioner_Career_and_Inspiration.html` | Bronze | None in tested patterns |
| 38 | `Art_Teesside/Grow/GROW_ART_W6_Plan_and_Rehearse_the_Skill_Share.html` | Bronze | None in tested patterns |
| 39 | `Art_Teesside/Grow/GROW_ART_W7_Deliver_the_Skill_Share_and_Curate.html` | Bronze | None in tested patterns |
| 40 | `Art_Teesside/Grow/GROW_ART_W8_Reflect_Audit_and_Close_the_Loop.html` | Bronze | None in tested patterns |
| 41 | `Art_Teesside/Grow/Spring2_2026-27/GROW_ART_Spring2_W1_Armature_and_Frame_OUTSTANDING_V3.html` | Bronze | None in tested patterns |
| 42 | `Art_Teesside/Grow/Spring2_2026-27/GROW_ART_Spring2_W2_Scale_and_Negative_Space_OUTSTANDING_V3.html` | Bronze | None in tested patterns |
| 43 | `Art_Teesside/Grow/Spring2_2026-27/GROW_ART_Spring2_W3_Surface_and_Patination_OUTSTANDING_V3.html` | Bronze | None in tested patterns |
| 44 | `Art_Teesside/Grow/Spring2_2026-27/GROW_ART_Spring2_W4_Contextual_Study_Kapoor_Whiteread_Barlow_OUTSTANDING_V3.html` | Bronze | None in tested patterns |
| 45 | `Art_Teesside/Grow/Spring2_2026-27/GROW_ART_Spring2_W5_Site_Integration_OUTSTANDING_V3.html` | Bronze | None in tested patterns |
| 46 | `Art_Teesside/Grow/Spring2_2026-27/GROW_ART_Spring2_W6_Proposal_Pitch_and_Review_OUTSTANDING_V3.html` | Bronze | None in tested patterns |
| 47 | `Art_Teesside/LAUNCH_W1-W8_2026-27/LAUNCH_Art_W1_Set_Arts_Development_Goals_Silver_Gold_Unit.html` | Silver | None in tested patterns |
| 48 | `Art_Teesside/LAUNCH_W1-W8_2026-27/LAUNCH_Art_W2_Develop_A_Skill_Document_Progress.html` | Silver | None in tested patterns |
| 49 | `Art_Teesside/LAUNCH_W1-W8_2026-27/LAUNCH_Art_W3_Research_An_Artist_Practitioner.html` | Silver | None in tested patterns |
| 50 | `Art_Teesside/LAUNCH_W1-W8_2026-27/LAUNCH_Art_W4_Refine_Technique_With_Feedback.html` | Silver | None in tested patterns |
| 51 | `Art_Teesside/LAUNCH_W1-W8_2026-27/LAUNCH_Art_W6_Attend_Experience_An_Arts_Event.html` | Silver | None in tested patterns |
| 52 | `Art_Teesside/LAUNCH_W1-W8_2026-27/LAUNCH_Art_W7_Begin_A_Critical_Review.html` | Silver | None in tested patterns |
| 53 | `Art_Teesside/Launch/LAUNCH_ART_W1_Frame_the_Local_Challenge.html` | Silver | None in tested patterns |
| 54 | `Art_Teesside/Launch/LAUNCH_ART_W2_Practice_Careers_and_Pathways.html` | Silver | None in tested patterns |
| 55 | `Art_Teesside/Launch/LAUNCH_ART_W3_Implement_and_Critically_Develop.html` | Silver | None in tested patterns |
| 56 | `Art_Teesside/Launch/LAUNCH_ART_W4_Arts_Experience_Attend_Analyse_and_Share.html` | Silver | None in tested patterns |
| 57 | `Art_Teesside/Launch/LAUNCH_ART_W5_Design_the_Leadership_Project.html` | Silver | None in tested patterns |
| 58 | `Art_Teesside/Launch/LAUNCH_ART_W6_Pilot_Lead_and_Adapt.html` | Silver | None in tested patterns |
| 59 | `Art_Teesside/Launch/LAUNCH_ART_W7_Deliver_and_Curate_the_Arts_Project.html` | Silver | None in tested patterns |
| 60 | `Art_Teesside/Launch/LAUNCH_ART_W8_Review_Influence_and_Portfolio_Audit.html` | Silver | None in tested patterns |
| 61 | `Art_Teesside/Launch/Spring2_2026-27/LAUNCH_ART_Spring2_W1_Armature_and_Frame_OUTSTANDING_V3.html` | Silver | None in tested patterns |
| 62 | `Art_Teesside/Launch/Spring2_2026-27/LAUNCH_ART_Spring2_W2_Scale_and_Negative_Space_OUTSTANDING_V3.html` | Silver | None in tested patterns |
| 63 | `Art_Teesside/Launch/Spring2_2026-27/LAUNCH_ART_Spring2_W3_Surface_and_Patination_OUTSTANDING_V3.html` | Silver | None in tested patterns |
| 64 | `Art_Teesside/Launch/Spring2_2026-27/LAUNCH_ART_Spring2_W4_Contextual_Study_Kapoor_Whiteread_Barlow_OUTSTANDING_V3.html` | Silver | None in tested patterns |
| 65 | `Art_Teesside/Launch/Spring2_2026-27/LAUNCH_ART_Spring2_W5_Site_Integration_OUTSTANDING_V3.html` | Silver | None in tested patterns |
| 66 | `Art_Teesside/Launch/Spring2_2026-27/LAUNCH_ART_Spring2_W6_Proposal_Pitch_and_Review_OUTSTANDING_V3.html` | Silver | None in tested patterns |
| 67 | `BUILD_Estate_v3/Art_Teesside/BUILD_ART_W1_The_Local_Canvas.html` | Explore | None in tested patterns |
| 68 | `BUILD_Estate_v3/Art_Teesside/BUILD_ART_W2_Artists_Makers_and_Teesside_Connections.html` | Explore | None in tested patterns |
| 69 | `BUILD_Estate_v3/Art_Teesside/BUILD_ART_W3_Industrial_Surface_Skills_Lab.html` | Explore | None in tested patterns |
| 70 | `BUILD_Estate_v3/Art_Teesside/BUILD_ART_W4_Build_the_Brief.html` | Explore | None in tested patterns |
| 71 | `BUILD_Estate_v3/Art_Teesside/BUILD_ART_W5_Critique_Test_and_Redirect.html` | Explore | None in tested patterns |
| 72 | `BUILD_Estate_v3/Art_Teesside/BUILD_ART_W6_Resolve_the_Artwork.html` | Explore | None in tested patterns |
| 73 | `BUILD_Estate_v3/Art_Teesside/BUILD_ART_W7_Curate_the_Showcase.html` | Explore | None in tested patterns |
| 74 | `BUILD_Estate_v3/Art_Teesside/BUILD_ART_W8_Share_Reflect_and_Close_the_Loop.html` | Explore | None in tested patterns |
| 75 | `GROW_Estate_v3/Art_Teesside/GROW_ART_W1_The_Local_Canvas.html` | Bronze | None in tested patterns |
| 76 | `GROW_Estate_v3/Art_Teesside/GROW_ART_W2_Studio_Skills_Safe_Practice.html` | Bronze | None in tested patterns |
| 77 | `GROW_Estate_v3/Art_Teesside/GROW_ART_W3_Independent_Studio_Challenge.html` | Bronze | None in tested patterns |
| 78 | `GROW_Estate_v3/Art_Teesside/GROW_ART_W4_Arts_Event_Attend_Capture_Review.html` | Bronze | None in tested patterns |
| 79 | `GROW_Estate_v3/Art_Teesside/GROW_ART_W5_Practitioner_Career_Inspiration.html` | Bronze | None in tested patterns |
| 80 | `GROW_Estate_v3/Art_Teesside/GROW_ART_W6_Plan_Rehearse_the_Skill_Share.html` | Bronze | None in tested patterns |
| 81 | `GROW_Estate_v3/Art_Teesside/GROW_ART_W7_Deliver_the_Skill_Share_Curate.html` | Bronze | None in tested patterns |
| 82 | `GROW_Estate_v3/Art_Teesside/GROW_ART_W8_Reflect_Audit_Close_the_Loop.html` | Bronze | None in tested patterns |

## Final closeout fields

- Exact current Lessons main after last authorised merge: **PENDING**.
- All 42 merged lesson units and exact per-level merge/blob proofs: **PENDING for Explore/Silver**.
- Bronze→GROW / Silver→LAUNCH placement rows: **PENDING**.
- Gold shelf documentation merge: **PENDING**.
- Catalogue last, alone, per batch: **PENDING**.
- Post-merge ledger and VB_STATE reconciled, including 76/82 and cells distinctions: **PENDING**.
- Terminal token: **NOT EMITTED BY THIS DRAFT**. Root selects the order’s token only after its condition is actually met.
