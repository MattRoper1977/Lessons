# Pass E (KO Triage) — TRIAGE LEDGER

> **Provisional letter Z was spent** (pedagogy *Pass Z*, commits `453b5e6`/`d5c8cf1`, merged to main
> 2026-07-25). Per R-H09 + master-prompt §0a this pass **self-renamed Z → E** (`E`/`I` were the only
> pass-letters free in both git and the ledger; `E` chosen as lowest free, mirroring the existing
> *Pass H / §H / R-H##* coexistence). Branch `pass-e-ko-triage`; rollback SHA `12cb6d9`.

**Derived at HEAD** `12cb6d9cd8074cf66d351010504de7afcbd010b3` (origin/main tip = rollback SHA). Instruments UNMODIFIED (R-E09).
**assumptions:** full clone · 161-file KO corpus (`id="print-ko"`) · network not required ·
co-modification is a consistency proxy, not consistency (the 44 'clean' are UNCHECKED, not verified).

## Verdict totals

| | count |
|---|---|
| candidates at HEAD | 117 |
| &nbsp;&nbsp;non-assessed read this pass | 115 |
| &nbsp;&nbsp;&nbsp;&nbsp;**STILL-TRUE** | **112** |
| &nbsp;&nbsp;&nbsp;&nbsp;**STALE** (Tier 2, held) | **3** |
| &nbsp;&nbsp;assessed pair (read-only, Matt/Tier 3) | 2 |

Reading method: 8 suite-scoped read-only passes (conservative — default STILL-TRUE, STALE only on a
quotable KO-vs-body contradiction), each STALE **independently re-verified against the file** before
entering this ledger. A KO is a summary, not a copy; wording differences are not staleness.

## §2 · Re-derivation (never inherited)

| figure | value |
|---|---|
| KO corpus (`id="print-ko"`) | 161 |
| CANDIDATES at HEAD | **117** |
| dropped — architecture-only | 0 |
| clean (co-mod proxy, UNCHECKED) | 44 |
| cardinality | 117 + 0 + 44 = 161 == 161 ✓ (tool + independent re-derivation) |
| carryforward (not inherited) | 114 → **+3 vs HEAD, within ±10** |

## §2c · Bucket split — old (of 114) vs new (of 117)

| bucket | carryforward (114) | HEAD (117) |
|---|---|---|
| R-E07 Loop-Mark artefact (first mover = Loop Mark) | 39 | 34 |
| other body-mover | 75 | 81 |
| assessed pair | 2 | 2 |
| **sum** | 114 | **117** |

## §3a · SHAPE-BREAK (recorded; halt-gate fired, reported, authorised to continue)

R-E07's VERIFIED remedy (strip the Loop Mark region `<td class="lm-strip">` + `<span class="lm-own">`)
re-run as a diff-class test: **artefact bucket cleared 0 of 34**; **0 of 117** candidates are cheap-clearable.
The Loop Mark (2026-07-28) is the most-recent mover but Pass F/O/W/W2 (07-24/25) and the art-remediation
merge (07-29) moved the same bodies earlier — so the carryforward's 'clear the artefacts cheaply' model is
false at HEAD and all 115 non-assessed candidates were content-read. **Outcome: 112 STILL-TRUE, 3 STALE**
— the estate's KOs are overwhelmingly current; the candidate list was inflated by chassis co-movement, exactly
the ko_staleness proxy shape R-E07 predicted.

## §3b/§4 · STALE findings (Tier 2 — held, batched by suite)

### BUILD_ASDAN suite — Careers W6/W7 KO week-label swap (2 files)
Standing-rule-7 case ('a Careers file named W6 carrying W7'). In each file the `<title>`, slide-tag and
`Week N of 7` marker agree on the swapped week; only the KO `<h1>` lagged. KO-text-only.

| file | KO line (old) | KO line (new) | body fact (3 surfaces agree) |
|---|---|---|---|
| `CAREERS_W6_My_Career_Profile.html` | `Knowledge Organiser (BUILD ASDAN W6): My Career Profile` | `…(BUILD ASDAN W7):…` | `<title>… slot W7 …` · `Careers · Week 7 of 7` |
| `CAREERS_W7_After_Year_11.html` | `Knowledge Organiser (BUILD ASDAN W7): What Happens After Year 11` | `…(BUILD ASDAN W6):…` | `<title>… slot W6 …` · `Careers · Week 6 of 7` |

### Build suite — BUILD_HUM_W6 PEE→PEEL (1 file, 2 hunks)
The `Humanities: PEE -> PEEL` pass updated the body (and GROW_HUM_W6's KO) but left BUILD_HUM_W6's KO on the
4-part model. Body teaches `What does PEEL stand for? Point, evidence, explanation, link.` + `Link bank — the L in PEEL`.

| hunk | old | new |
|---|---|---|
| KO table row (insert Link before Close) | *(no Link row)* | `<tr><td>Link</td><td>The phrase tying each paragraph back to the enquiry — the L in PEEL</td></tr>` |
| Key Fact bullet | `Every point needs evidence; every evidence needs explanation.` | `Every point needs evidence, every evidence needs explanation, and a link ties it back to the enquiry — that is PEEL.` |

## §3c · Assessed pair — READ FIRST, READ-ONLY (Matt / Tier 3, his key)

| file | verdict | note |
|---|---|---|
| `Grow/Slideshows/GROW_HUM_W7_Write_The_Account.html` | HELD (Matt/Tier 3) | SURFACE STILL-TRUE + 1 residue: KO row 'Evaluation clause — Deployed provenance honesty' echoes the removed 'Evaluation Deployments'; 'Reference Zone' ×3 lingers though LL-A2a swapped it for the Conditions Card. Read against the Card, Matt's key. |
| `Launch/Slideshows/LAUNCH_HUM_W7_Source_Assessment.html` | HELD (Matt/Tier 3) | SURFACE STILL-TRUE: KO names none of the removed support (Connective Bank/Evaluation Deployments 0/0); 'Reference Zone' ×3 residue to confirm benign. |

Neither KO literally names the removed Connective Bank / Evaluation Deployments — the carryforward's worst
case is not confirmed on the face of it. Both carry the LL-A2a Conditions Card. Any fix is Matt's, one hunk
inside the intended block; **excluded from Tier 2 regardless of verdict**.

## §5 · R-G05 resolution (the '37 of 49 KOs disagree with slides')

Pre-`9f657b6` historical figure (KO as a stale snapshot of the We-Do-2 game pills). **Method at HEAD:** per
ASDAN file, KO key-word terms vs `match-pill` terms. **0/49** KO tables are still snapshots (13/49 share ≥1
term as legit vocabulary; 36/49 share none). Pass G decoupled KO (real vocab) from game (classification
task); the figure is **retired by the rebuild**. All 49 ASDAN KO files sit in the 117-candidate set and were
content-read here (all STILL-TRUE). Append-only REGISTER text: `_passe/REGISTER_APPEND_RG05.md`.

## Full candidate table (117)

`n` = content-commit count.

| # | n | verdict | bucket | suite | file | most-recent content mover |
|--:|--:|---|---|---|---|---|
| 1 | 7 | HELD(assessed) | assessed | Grow | `Grow/Slideshows/GROW_HUM_W7_Write_The_Account.html` | Pass LL-A2a: Assessed Conditions Card replaces the Reference |
| 2 | 4 | HELD(assessed) | assessed | Launch | `Launch/Slideshows/LAUNCH_HUM_W7_Source_Assessment.html` | Pass LL-A2a: Assessed Conditions Card replaces the Reference |
| 3 | 1 | STILL-TRUE | body-mover | 2 Physics 10 | `2 Physics 10/Waves/L4a_Wave_Anatomy.html` | Add files via upload |
| 4 | 4 | STILL-TRUE | body-mover | Art_Teesside | `Art_Teesside/Build/BUILD_ART_A2_W1_Surface_Hunt.html` | Merge art-remediation into main — the landed art remediation |
| 5 | 4 | STILL-TRUE | body-mover | Art_Teesside | `Art_Teesside/Build/BUILD_ART_A2_W2_Arts_Inspiration.html` | Merge art-remediation into main — the landed art remediation |
| 6 | 4 | STILL-TRUE | body-mover | Art_Teesside | `Art_Teesside/Build/BUILD_ART_A2_W3_Stencil_Lab.html` | Merge art-remediation into main — the landed art remediation |
| 7 | 4 | STILL-TRUE | body-mover | Art_Teesside | `Art_Teesside/Build/BUILD_ART_A2_W4_Audience_Week.html` | Merge art-remediation into main — the landed art remediation |
| 8 | 3 | STILL-TRUE | body-mover | Art_Teesside | `Art_Teesside/Build/BUILD_ART_A2_W5_Layer_and_Combine.html` | Merge art-remediation into main — the landed art remediation |
| 9 | 5 | STILL-TRUE | body-mover | Art_Teesside | `Art_Teesside/Build/BUILD_ART_A2_W6_Resolve_and_Edition.html` | Merge art-remediation into main — the landed art remediation |
| 10 | 3 | STILL-TRUE | body-mover | Art_Teesside | `Art_Teesside/Build/BUILD_ART_A2_W7_Bank_It_and_Plan_the_Teach.html` | Merge art-remediation into main — the landed art remediation |
| 11 | 6 | STILL-TRUE | artefact(LoopMark-first) | Art_Teesside | `Art_Teesside/Build/BUILD_ART_W1_The_Local_Canvas.html` | Pass LL-G sub-pass 1 of 3: the Loop Mark, 15 BUILD lessons |
| 12 | 7 | STILL-TRUE | artefact(LoopMark-first) | Art_Teesside | `Art_Teesside/Build/BUILD_ART_W2_Artists_Makers_and_Teesside_Connections.html` | Pass LL-G sub-pass 1 of 3: the Loop Mark, 15 BUILD lessons |
| 13 | 6 | STILL-TRUE | artefact(LoopMark-first) | Art_Teesside | `Art_Teesside/Build/BUILD_ART_W3_Industrial_Surface_Skills_Lab.html` | Pass LL-G sub-pass 1 of 3: the Loop Mark, 15 BUILD lessons |
| 14 | 6 | STILL-TRUE | artefact(LoopMark-first) | Art_Teesside | `Art_Teesside/Build/BUILD_ART_W4_Build_the_Brief.html` | Pass LL-G sub-pass 1 of 3: the Loop Mark, 15 BUILD lessons |
| 15 | 6 | STILL-TRUE | artefact(LoopMark-first) | Art_Teesside | `Art_Teesside/Build/BUILD_ART_W5_Critique_Test_and_Redirect.html` | Pass LL-G sub-pass 1 of 3: the Loop Mark, 15 BUILD lessons |
| 16 | 6 | STILL-TRUE | artefact(LoopMark-first) | Art_Teesside | `Art_Teesside/Build/BUILD_ART_W6_Resolve_the_Artwork.html` | Pass LL-G sub-pass 1 of 3: the Loop Mark, 15 BUILD lessons |
| 17 | 6 | STILL-TRUE | artefact(LoopMark-first) | Art_Teesside | `Art_Teesside/Build/BUILD_ART_W7_Curate_the_Showcase.html` | Pass LL-G sub-pass 1 of 3: the Loop Mark, 15 BUILD lessons |
| 18 | 6 | STILL-TRUE | artefact(LoopMark-first) | Art_Teesside | `Art_Teesside/Build/BUILD_ART_W8_Share_Reflect_and_Close_the_Loop.html` | Pass LL-G sub-pass 1 of 3: the Loop Mark, 15 BUILD lessons |
| 19 | 5 | STILL-TRUE | body-mover | Art_Teesside | `Art_Teesside/Grow/GROW_ART_W1_The_Local_Canvas.html` | Pass C (1/2): Arts Award compliance, caption honesty, author |
| 20 | 9 | STILL-TRUE | body-mover | Art_Teesside | `Art_Teesside/Grow/GROW_ART_W2_Studio_Skills_and_Safe_Practice.html` | Merge art-remediation into main — the landed art remediation |
| 21 | 9 | STILL-TRUE | body-mover | Art_Teesside | `Art_Teesside/Grow/GROW_ART_W3_Independent_Studio_Challenge.html` | Merge art-remediation into main — the landed art remediation |
| 22 | 6 | STILL-TRUE | body-mover | Art_Teesside | `Art_Teesside/Grow/GROW_ART_W4_Arts_Event_Attend_Capture_and_Review.html` | Pass C (2/2): access routes and dependency contingencies for |
| 23 | 7 | STILL-TRUE | body-mover | Art_Teesside | `Art_Teesside/Grow/GROW_ART_W5_Practitioner_Career_and_Inspiration.html` | Art Pass J: Artist Decision Matrix in BUILD W2 / GROW W5 / L |
| 24 | 5 | STILL-TRUE | body-mover | Art_Teesside | `Art_Teesside/Grow/GROW_ART_W6_Plan_and_Rehearse_the_Skill_Share.html` | Pass C (1/2): Arts Award compliance, caption honesty, author |
| 25 | 6 | STILL-TRUE | body-mover | Art_Teesside | `Art_Teesside/Grow/GROW_ART_W7_Deliver_the_Skill_Share_and_Curate.html` | Pass C (2/2): access routes and dependency contingencies for |
| 26 | 5 | STILL-TRUE | body-mover | Art_Teesside | `Art_Teesside/Grow/GROW_ART_W8_Reflect_Audit_and_Close_the_Loop.html` | Pass C (1/2): Arts Award compliance, caption honesty, author |
| 27 | 6 | STILL-TRUE | body-mover | Art_Teesside | `Art_Teesside/Launch/LAUNCH_ART_W1_Frame_the_Local_Challenge.html` | Pass C (2/2): access routes and dependency contingencies for |
| 28 | 6 | STILL-TRUE | body-mover | Art_Teesside | `Art_Teesside/Launch/LAUNCH_ART_W2_Practice_Careers_and_Pathways.html` | Art Pass J: Artist Decision Matrix in BUILD W2 / GROW W5 / L |
| 29 | 8 | STILL-TRUE | body-mover | Art_Teesside | `Art_Teesside/Launch/LAUNCH_ART_W3_Implement_and_Critically_Develop.html` | Merge art-remediation into main — the landed art remediation |
| 30 | 6 | STILL-TRUE | body-mover | Art_Teesside | `Art_Teesside/Launch/LAUNCH_ART_W4_Arts_Experience_Attend_Analyse_and_Share.html` | Pass C (2/2): access routes and dependency contingencies for |
| 31 | 6 | STILL-TRUE | body-mover | Art_Teesside | `Art_Teesside/Launch/LAUNCH_ART_W5_Design_the_Leadership_Project.html` | Pass C (2/2): access routes and dependency contingencies for |
| 32 | 5 | STILL-TRUE | body-mover | Art_Teesside | `Art_Teesside/Launch/LAUNCH_ART_W6_Pilot_Lead_and_Adapt.html` | Pass C (1/2): Arts Award compliance, caption honesty, author |
| 33 | 5 | STILL-TRUE | body-mover | Art_Teesside | `Art_Teesside/Launch/LAUNCH_ART_W7_Deliver_and_Curate_the_Arts_Project.html` | Pass C (1/2): Arts Award compliance, caption honesty, author |
| 34 | 5 | STILL-TRUE | body-mover | Art_Teesside | `Art_Teesside/Launch/LAUNCH_ART_W8_Review_Influence_and_Portfolio_Audit.html` | Pass C (1/2): Arts Award compliance, caption honesty, author |
| 35 | 7 | STILL-TRUE | body-mover | BUILD_ASDAN | `BUILD_ASDAN/Careers/CAREERS_W1_My_Strengths.html` | Pass SB Tier 1: Careers W1-W5 week-count 'of 6' -> 'of 7' |
| 36 | 7 | STILL-TRUE | body-mover | BUILD_ASDAN | `BUILD_ASDAN/Careers/CAREERS_W2_Jobs_in_My_Community.html` | Pass SB Tier 1: Careers W1-W5 week-count 'of 6' -> 'of 7' |
| 37 | 7 | STILL-TRUE | body-mover | BUILD_ASDAN | `BUILD_ASDAN/Careers/CAREERS_W3_Skills_Employers_Want.html` | Pass SB Tier 1: Careers W1-W5 week-count 'of 6' -> 'of 7' |
| 38 | 8 | STILL-TRUE | body-mover | BUILD_ASDAN | `BUILD_ASDAN/Careers/CAREERS_W4_Routines_and_Reliability.html` | Pass SB Tier 1: Careers W1-W5 week-count 'of 6' -> 'of 7' |
| 39 | 9 | STILL-TRUE | body-mover | BUILD_ASDAN | `BUILD_ASDAN/Careers/CAREERS_W5_Applying_Myself.html` | Pass SB Tier 1: Careers W1-W5 week-count 'of 6' -> 'of 7' |
| 40 | 4 | STALE **⟵STALE** | artefact(LoopMark-first) | BUILD_ASDAN | `BUILD_ASDAN/Careers/CAREERS_W6_My_Career_Profile.html` | Pass LL-G sub-pass 1 of 3: the Loop Mark, 15 BUILD lessons |
| 41 | 5 | STALE **⟵STALE** | artefact(LoopMark-first) | BUILD_ASDAN | `BUILD_ASDAN/Careers/CAREERS_W7_After_Year_11.html` | Pass LL-G sub-pass 2 of 3: the Loop Mark, 15 BUILD lessons |
| 42 | 5 | STILL-TRUE | artefact(LoopMark-first) | BUILD_ASDAN | `BUILD_ASDAN/Community_Project/COMM_W1_Choose_Our_Asset.html` | Pass LL-G sub-pass 2 of 3: the Loop Mark, 15 BUILD lessons |
| 43 | 5 | STILL-TRUE | artefact(LoopMark-first) | BUILD_ASDAN | `BUILD_ASDAN/Community_Project/COMM_W2_The_Site's_Need.html` | Pass LL-G sub-pass 2 of 3: the Loop Mark, 15 BUILD lessons |
| 44 | 5 | STILL-TRUE | artefact(LoopMark-first) | BUILD_ASDAN | `BUILD_ASDAN/Community_Project/COMM_W3_Our_Team_Roles.html` | Pass LL-G sub-pass 2 of 3: the Loop Mark, 15 BUILD lessons |
| 45 | 5 | STILL-TRUE | artefact(LoopMark-first) | BUILD_ASDAN | `BUILD_ASDAN/Community_Project/COMM_W4_Partner_Update.html` | Pass LL-G sub-pass 2 of 3: the Loop Mark, 15 BUILD lessons |
| 46 | 5 | STILL-TRUE | artefact(LoopMark-first) | BUILD_ASDAN | `BUILD_ASDAN/Community_Project/COMM_W5_Plan_the_Handover.html` | Pass LL-G sub-pass 2 of 3: the Loop Mark, 15 BUILD lessons |
| 47 | 5 | STILL-TRUE | artefact(LoopMark-first) | BUILD_ASDAN | `BUILD_ASDAN/Community_Project/COMM_W6_The_Handover_and_Its_Benefit.html` | Pass LL-G sub-pass 2 of 3: the Loop Mark, 15 BUILD lessons |
| 48 | 5 | STILL-TRUE | artefact(LoopMark-first) | BUILD_ASDAN | `BUILD_ASDAN/Duke_and_Enterprise/DUKE_W1_Choose_My_Challenges.html` | Pass LL-G sub-pass 2 of 3: the Loop Mark, 15 BUILD lessons |
| 49 | 5 | STILL-TRUE | artefact(LoopMark-first) | BUILD_ASDAN | `BUILD_ASDAN/Duke_and_Enterprise/DUKE_W2_A_Kindness_Challenge.html` | Pass LL-G sub-pass 2 of 3: the Loop Mark, 15 BUILD lessons |
| 50 | 5 | STILL-TRUE | artefact(LoopMark-first) | BUILD_ASDAN | `BUILD_ASDAN/Duke_and_Enterprise/DUKE_W3_An_Eco_Challenge.html` | Pass LL-G sub-pass 2 of 3: the Loop Mark, 15 BUILD lessons |
| 51 | 5 | STILL-TRUE | artefact(LoopMark-first) | BUILD_ASDAN | `BUILD_ASDAN/Duke_and_Enterprise/DUKE_W4_An_Independence_Challenge.html` | Pass LL-G sub-pass 2 of 3: the Loop Mark, 15 BUILD lessons |
| 52 | 5 | STILL-TRUE | artefact(LoopMark-first) | BUILD_ASDAN | `BUILD_ASDAN/Duke_and_Enterprise/DUKE_W5_Our_Social_Enterprise.html` | Pass LL-G sub-pass 2 of 3: the Loop Mark, 15 BUILD lessons |
| 53 | 5 | STILL-TRUE | artefact(LoopMark-first) | BUILD_ASDAN | `BUILD_ASDAN/Duke_and_Enterprise/DUKE_W6_Pitch_and_Reflect.html` | Pass LL-G sub-pass 2 of 3: the Loop Mark, 15 BUILD lessons |
| 54 | 5 | STILL-TRUE | artefact(LoopMark-first) | BUILD_ASDAN | `BUILD_ASDAN/FoodWise/FW_W1_Food_Groups.html` | Pass LL-G sub-pass 2 of 3: the Loop Mark, 15 BUILD lessons |
| 55 | 4 | STILL-TRUE | artefact(LoopMark-first) | BUILD_ASDAN | `BUILD_ASDAN/FoodWise/FW_W2_A_Balanced_Plate.html` | Pass LL-G sub-pass 2 of 3: the Loop Mark, 15 BUILD lessons |
| 56 | 5 | STILL-TRUE | artefact(LoopMark-first) | BUILD_ASDAN | `BUILD_ASDAN/FoodWise/FW_W3_Reading_Labels.html` | Pass LL-G sub-pass 3 of 3: the Loop Mark, 15 BUILD lessons |
| 57 | 5 | STILL-TRUE | artefact(LoopMark-first) | BUILD_ASDAN | `BUILD_ASDAN/FoodWise/FW_W4_Kitchen_Hygiene_and_Safety.html` | Pass LL-G sub-pass 3 of 3: the Loop Mark, 15 BUILD lessons |
| 58 | 5 | STILL-TRUE | artefact(LoopMark-first) | BUILD_ASDAN | `BUILD_ASDAN/FoodWise/FW_W5_Prepare_a_Healthy_Snack.html` | Pass LL-G sub-pass 1 of 3: the Loop Mark, 15 BUILD lessons |
| 59 | 5 | STILL-TRUE | artefact(LoopMark-first) | BUILD_ASDAN | `BUILD_ASDAN/FoodWise/FW_W6_Plan_a_Healthy_Meal.html` | Pass LL-G sub-pass 3 of 3: the Loop Mark, 15 BUILD lessons |
| 60 | 5 | STILL-TRUE | artefact(LoopMark-first) | BUILD_ASDAN | `BUILD_ASDAN/Living_Independently/LI_W1_Where_Money_Comes_From.html` | Pass LL-G sub-pass 3 of 3: the Loop Mark, 15 BUILD lessons |
| 61 | 5 | STILL-TRUE | artefact(LoopMark-first) | BUILD_ASDAN | `BUILD_ASDAN/Living_Independently/LI_W2_Notes_and_Coins.html` | Pass LL-G sub-pass 3 of 3: the Loop Mark, 15 BUILD lessons |
| 62 | 5 | STILL-TRUE | artefact(LoopMark-first) | BUILD_ASDAN | `BUILD_ASDAN/Living_Independently/LI_W3_Needs_vs_Wants.html` | Pass LL-G sub-pass 3 of 3: the Loop Mark, 15 BUILD lessons |
| 63 | 5 | STILL-TRUE | artefact(LoopMark-first) | BUILD_ASDAN | `BUILD_ASDAN/Living_Independently/LI_W4_Everyday_Prices.html` | Pass LL-G sub-pass 3 of 3: the Loop Mark, 15 BUILD lessons |
| 64 | 6 | STILL-TRUE | artefact(LoopMark-first) | BUILD_ASDAN | `BUILD_ASDAN/Living_Independently/LI_W5_A_Simple_Budget.html` | Pass LL-G sub-pass 3 of 3: the Loop Mark, 15 BUILD lessons |
| 65 | 5 | STILL-TRUE | artefact(LoopMark-first) | BUILD_ASDAN | `BUILD_ASDAN/Living_Independently/LI_W6_Shopping_and_Change.html` | Pass LL-G sub-pass 3 of 3: the Loop Mark, 15 BUILD lessons |
| 66 | 2 | STILL-TRUE | body-mover | Build | `Build/Slideshows/BUILD_DT_W1_Workshop_Audit.html` | W1 D&T Pass S: start the cut list (Track C) |
| 67 | 6 | STILL-TRUE | body-mover | Build | `Build/Slideshows/BUILD_DT_W2_Blueprint.html` | W2 D&T Pass S: ergonomics mirror + choice line + start the c |
| 68 | 5 | STILL-TRUE | body-mover | Build | `Build/Slideshows/BUILD_DT_W3_Core_Cut.html` | W3 D&T Pass S: check the cut list before the saw (Track C) |
| 69 | 3 | STILL-TRUE | body-mover | Build | `Build/Slideshows/BUILD_DT_W4_Assembly.html` | D&T: fix stale week labels reaching the printed teacher pack |
| 70 | 5 | STILL-TRUE | body-mover | Build | `Build/Slideshows/BUILD_DT_W5_Finish.html` | W5 D&T Pass S: inclusive finish mirror + contrast pill (Trac |
| 71 | 3 | STILL-TRUE | body-mover | Build | `Build/Slideshows/BUILD_DT_W6_Handover.html` | D&T: fix stale week labels reaching the printed teacher pack |
| 72 | 2 | STILL-TRUE | body-mover | Build | `Build/Slideshows/BUILD_HUM_W1_Human_Timeline.html` | LAUNCH_HUM W2-W8 parity, and make the Reference Zone actuall |
| 73 | 5 | STILL-TRUE | body-mover | Build | `Build/Slideshows/BUILD_HUM_W2_History_Detectives.html` | LAUNCH_HUM W2-W8 parity, and make the Reference Zone actuall |
| 74 | 5 | STILL-TRUE | body-mover | Build | `Build/Slideshows/BUILD_HUM_W3_Why_People_Came.html` | LAUNCH_HUM W2-W8 parity, and make the Reference Zone actuall |
| 75 | 5 | STILL-TRUE | body-mover | Build | `Build/Slideshows/BUILD_HUM_W4_People_Who_Shaped_Britain.html` | LAUNCH_HUM W2-W8 parity, and make the Reference Zone actuall |
| 76 | 5 | STILL-TRUE | body-mover | Build | `Build/Slideshows/BUILD_HUM_W5_Big_Deal.html` | LAUNCH_HUM W2-W8 parity, and make the Reference Zone actuall |
| 77 | 6 | STALE **⟵STALE** | body-mover | Build | `Build/Slideshows/BUILD_HUM_W6_Plan_The_Story.html` | LAUNCH_HUM W2-W8 parity, and make the Reference Zone actuall |
| 78 | 6 | STILL-TRUE | body-mover | Build | `Build/Slideshows/BUILD_HUM_W7_Tell_The_Story.html` | LAUNCH_HUM W2-W8 parity, and make the Reference Zone actuall |
| 79 | 5 | STILL-TRUE | body-mover | Build | `Build/Slideshows/BUILD_HUM_W8_Where_In_The_World.html` | LAUNCH_HUM W2-W8 parity, and make the Reference Zone actuall |
| 80 | 3 | STILL-TRUE | body-mover | GROW_ASDAN | `GROW_ASDAN/Community_Project/GCOMM_W1_Our_Patch_Our_Say.html` | Pass W2: name the task on every ASDAN We Do 2, on screen and |
| 81 | 3 | STILL-TRUE | body-mover | GROW_ASDAN | `GROW_ASDAN/Community_Project/GCOMM_W2_Choose_The_Need.html` | Pass W2: name the task on every ASDAN We Do 2, on screen and |
| 82 | 3 | STILL-TRUE | body-mover | GROW_ASDAN | `GROW_ASDAN/Community_Project/GCOMM_W3_Roles_Steps_Resources.html` | Pass W2: name the task on every ASDAN We Do 2, on screen and |
| 83 | 3 | STILL-TRUE | body-mover | GROW_ASDAN | `GROW_ASDAN/Community_Project/GCOMM_W4_First_Contact.html` | Pass W2: name the task on every ASDAN We Do 2, on screen and |
| 84 | 3 | STILL-TRUE | body-mover | GROW_ASDAN | `GROW_ASDAN/Community_Project/GCOMM_W5_Risk_And_Ready.html` | Pass W2: name the task on every ASDAN We Do 2, on screen and |
| 85 | 4 | STILL-TRUE | body-mover | GROW_ASDAN | `GROW_ASDAN/Community_Project/GCOMM_W6_Green_Light.html` | Pass W2: name the task on every ASDAN We Do 2, on screen and |
| 86 | 3 | STILL-TRUE | body-mover | GROW_ASDAN | `GROW_ASDAN/Enterprise/ENT_W1_Helps_And_Earns.html` | Pass W2: name the task on every ASDAN We Do 2, on screen and |
| 87 | 3 | STILL-TRUE | body-mover | GROW_ASDAN | `GROW_ASDAN/Enterprise/ENT_W2_Spot_The_Gap.html` | Pass W2: name the task on every ASDAN We Do 2, on screen and |
| 88 | 3 | STILL-TRUE | body-mover | GROW_ASDAN | `GROW_ASDAN/Enterprise/ENT_W3_Our_Idea_Our_Users.html` | Pass W2: name the task on every ASDAN We Do 2, on screen and |
| 89 | 3 | STILL-TRUE | body-mover | GROW_ASDAN | `GROW_ASDAN/Enterprise/ENT_W4_Money_In_Money_Out.html` | Pass W2: name the task on every ASDAN We Do 2, on screen and |
| 90 | 4 | STILL-TRUE | body-mover | GROW_ASDAN | `GROW_ASDAN/Enterprise/ENT_W5_Brand_And_Pitch.html` | Pass W2: name the task on every ASDAN We Do 2, on screen and |
| 91 | 4 | STILL-TRUE | body-mover | GROW_ASDAN | `GROW_ASDAN/Enterprise/ENT_W6_Pitch_Day.html` | Pass W2: name the task on every ASDAN We Do 2, on screen and |
| 92 | 3 | STILL-TRUE | body-mover | GROW_ASDAN | `GROW_ASDAN/PEQ/PEQ_W1_Knowing_Myself.html` | Pass W2: name the task on every ASDAN We Do 2, on screen and |
| 93 | 3 | STILL-TRUE | body-mover | GROW_ASDAN | `GROW_ASDAN/PEQ/PEQ_W2_Goals_That_Work.html` | Pass W2: name the task on every ASDAN We Do 2, on screen and |
| 94 | 4 | STILL-TRUE | body-mover | GROW_ASDAN | `GROW_ASDAN/PEQ/PEQ_W3_Working_With_Others.html` | Pass W2: name the task on every ASDAN We Do 2, on screen and |
| 95 | 3 | STILL-TRUE | body-mover | GROW_ASDAN | `GROW_ASDAN/PEQ/PEQ_W4_Managing_Myself.html` | Pass W2: name the task on every ASDAN We Do 2, on screen and |
| 96 | 3 | STILL-TRUE | body-mover | GROW_ASDAN | `GROW_ASDAN/PEQ/PEQ_W5_Solving_Problems.html` | Pass W2: name the task on every ASDAN We Do 2, on screen and |
| 97 | 4 | STILL-TRUE | body-mover | GROW_ASDAN | `GROW_ASDAN/PEQ/PEQ_W6_Present_My_Progress.html` | Pass W2: name the task on every ASDAN We Do 2, on screen and |
| 98 | 5 | STILL-TRUE | body-mover | Grow | `Grow/Slideshows/GROW_HUM_W1_Time_Detectives.html` | LAUNCH_HUM W2-W8 parity, and make the Reference Zone actuall |
| 99 | 5 | STILL-TRUE | body-mover | Grow | `Grow/Slideshows/GROW_HUM_W2_Source_Detectives.html` | LAUNCH_HUM W2-W8 parity, and make the Reference Zone actuall |
| 100 | 5 | STILL-TRUE | body-mover | Grow | `Grow/Slideshows/GROW_HUM_W3_Cause_And_Consequence.html` | LAUNCH_HUM W2-W8 parity, and make the Reference Zone actuall |
| 101 | 5 | STILL-TRUE | body-mover | Grow | `Grow/Slideshows/GROW_HUM_W4_People_Who_Shaped_Britain.html` | LAUNCH_HUM W2-W8 parity, and make the Reference Zone actuall |
| 102 | 5 | STILL-TRUE | body-mover | Grow | `Grow/Slideshows/GROW_HUM_W5_Significance.html` | LAUNCH_HUM W2-W8 parity, and make the Reference Zone actuall |
| 103 | 3 | STILL-TRUE | body-mover | Grow | `Grow/Slideshows/GROW_HUM_W6_Plan_The_Account.html` | LAUNCH_HUM W2-W8 parity, and make the Reference Zone actuall |
| 104 | 5 | STILL-TRUE | body-mover | Grow | `Grow/Slideshows/GROW_HUM_W8_Where_In_The_World.html` | LAUNCH_HUM W2-W8 parity, and make the Reference Zone actuall |
| 105 | 3 | STILL-TRUE | body-mover | Launch | `Launch/Slideshows/LAUNCH_HUM_W1_Source_Investigation.html` | LAUNCH_HUM W1 pilot: illuminator, reduced motion, Reference  |
| 106 | 3 | STILL-TRUE | body-mover | Launch | `Launch/Slideshows/LAUNCH_HUM_W2_Cause_Consequence_Courtroom.html` | LAUNCH_HUM W2-W8 parity, and make the Reference Zone actuall |
| 107 | 3 | STILL-TRUE | body-mover | Launch | `Launch/Slideshows/LAUNCH_HUM_W3_Archive_NOP.html` | LAUNCH_HUM W2-W8 parity, and make the Reference Zone actuall |
| 108 | 3 | STILL-TRUE | body-mover | Launch | `Launch/Slideshows/LAUNCH_HUM_W4_Century_Of_Change.html` | LAUNCH_HUM W2-W8 parity, and make the Reference Zone actuall |
| 109 | 3 | STILL-TRUE | body-mover | Launch | `Launch/Slideshows/LAUNCH_HUM_W5_People_Modern_Britain.html` | LAUNCH_HUM W2-W8 parity, and make the Reference Zone actuall |
| 110 | 3 | STILL-TRUE | body-mover | Launch | `Launch/Slideshows/LAUNCH_HUM_W6_Structured_Account.html` | LAUNCH_HUM W2-W8 parity, and make the Reference Zone actuall |
| 111 | 3 | STILL-TRUE | body-mover | Launch | `Launch/Slideshows/LAUNCH_HUM_W8_OS_Map_Skills.html` | LAUNCH_HUM W2-W8 parity, and make the Reference Zone actuall |
| 112 | 3 | STILL-TRUE | body-mover | biology | `biology/L4_Aerobic.html` | Add files via upload |
| 113 | 2 | STILL-TRUE | body-mover | biology | `biology/Lesson_2_Absorption_v4-6.html` | Absorption: route the fatty acid to a lacteal, and let pupil |
| 114 | 2 | STILL-TRUE | body-mover | biology | `biology/Structure_of_the_Thorax.html` | Add files via upload |
| 115 | 2 | STILL-TRUE | body-mover | chemistry | `chemistry/Lesson3_Ions_Neutralisation_v4.html` | Lesson 3: add ion animation ending on the named salt |
| 116 | 3 | STILL-TRUE | body-mover | chemistry | `chemistry/Lesson4b_Gas_Tests_NH3_Cl2.html` | Add files via upload |
| 117 | 1 | STILL-TRUE | body-mover | chemistry | `chemistry/Lesson5_Flame_Tests.html` | Add files via upload |

_Row count asserted: **117 == 117**. STILL-TRUE 112 + STALE 3 + assessed 2 == 117._