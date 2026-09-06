# Silver: independent GROW Art cell review

## Decision for the current proposal

**No new GROW Art cell claim is justified by the proposed fourteen Silver decks at present.** This is an independent comparison of real outcomes, ruled weeks and existing claims. It does not extend Bronze’s AAE-H7 ruling to Silver, and it does not assume that a cell must literally say “Silver” to be teachable through Silver work.

The strongest same-week semantic candidate is Autumn C103, “Develop a skill and record it in my arts log.” The proposed `SILVER_W2_1B1.json` can teach that full narrow action, but an existing campaign deck already owns the cell. It is not new coverage. Spring C89 repeats that action and is unclaimed, but its ruled week is **17**, not the proposed Silver week 2. No silent timetable or cell reassignment is justified.

The reviewed proposal is `silver-drafts/silver-plan-proposal.md`: 1A in W1; 1B1 and full 1C in W2; full 1D and 1B2 in W3; Unit 2 planning/delivery/team work/review in W4–7. These are proposed serving lessons, not authored or tested Silver content. Final cell eligibility must be checked against the actual complete teaching in every support route.

## What was measured

- Read the real workbook `_passsg/inputs/GROW SOW 2026-27.xlsx` with `openpyxl` in read-only/data-only mode. All **39 GROW Art cell values** equal the spine’s verbatim outcomes: **39 compared, zero mismatches**.
- Read `tools/easter/EASTER_TARGETS.json`: **23 GROW Art plans**, all one cell each. **6 have existing claims; 17 are currently unclaimed**.
- Read current claims via `_sownb/vb/tools/cell_coverage.py`’s `load()` path, without invoking its report-writing main. The scan saw **706 HTML surfaces / 539 recognised lesson surfaces**. Across all 39 GROW Art spine cells, **8 have a claimant**. There are no duplicate recognised claimants on those eight.
- All ruled W1–7 Art cells already have claimants. Four campaign files pass existing `g29_plan_binding.judge()` with `outcomesMatch: true`. The other three are older `spine-audited/ALIGNED` claims and g29 **SKIP**, which is not a g29 pass. Autumn C109 at ruled W9 is another older aligned claim.
- One old deck, `Grow/Slideshows/GROW_ART_W2_Level_Up_Portrait.html`, has an unresolved `MULTI` spine reading across Autumn C103, Spring C89 and Summer C95. It is **not counted as owning any of them**. “Unclaimed” therefore does not mean there is no related old teaching.

Claims and binding results are not a fresh semantic audit of all existing decks. Counts describe the checked working tree, based at commit `c0e3e901ed85a4e76a16b41f083acdf9e9ca7772`, with concurrent new Explore work present. No claim, plan, workbook or repository file was changed by this review.

## Current planned cells and Silver fit

Every row below comes from `_passsg/inputs/GROW SOW 2026-27.xlsx`, under the existing strand **Creative Arts (Trinity Arts Award Explore/Bronze)**. That label is not silently rewritten. The table reproduces the complete workbook action, including explicit award objects and themes; matching one word is insufficient.

`plans[index]` is the zero-based position in `EASTER_TARGETS.json`; `P…` is its legacy label. Ruled weeks come from the plan, and match `cell_coverage.ruled_week()` applied to the cell’s `termWeek`, not the spine’s obsolete `absoluteWeek`.

| Workbook cell | Ruled week / plan | Verbatim outcome | Existing claim | Silver conclusion |
|---|---|---|---|---|
| `'GROW Weekly - Autumn'!C103` | 2 · `plans[18]`, P0019 | Develop a skill and record it in my arts log. | Owned | Strong narrow content match to W2 1B1: actually practise/develop the chosen skill and record it. Same week, but already owned; not new coverage and no duplicate claim. |
| `'GROW Weekly - Autumn'!C104` | 3 · `plans[28]`, P0029 | Plan an identity portrait or piece. | Owned | Conditional 1A content only if the pupil actually plans an identity piece. The proposal keeps challenge choices open and plans at W1, not W3. Already owned. |
| `'GROW Weekly - Autumn'!C105` | 4 · `plans[37]`, P0038 | Create my identity piece (BHM artist inspiration). | Owned | Needs actual identity-piece creation plus source-supported Black History Month artist inspiration. W4 is Unit 2 project planning, not this creation task. Already owned. |
| `'GROW Weekly - Autumn'!C106` | 5 · `plans[48]`, P0049 | Review and improve my work. | Owned | Could be served by genuine artwork review followed by improvement in 1B. W5 practical/team work is not automatically artwork improvement. Already owned. |
| `'GROW Weekly - Autumn'!C107` | 6 · `plans[57]`, P0058 | Research an artist who inspires me. | Owned | Possible 1D research overlap if an actual artist is personally inspiring and researched. Proposal 1D is W3; W6 is leadership/team work. Already owned. |
| `'GROW Weekly - Autumn'!C108` | 7 · `plans[66]`, P0067 | Share my Explore portfolio evidence so far. | Owned | Not a Silver-only consolidation match: this action explicitly shares Explore evidence. Do not silently replace Explore with Silver. Already owned. |
| `'GROW Weekly - Autumn'!C110` | 10 · `plans[84]`, P0085 | Learn a part for a group performance. | Unclaimed | Conditional on a real chosen performance activity and learning a personal performing part. Planning or leading an arts workshop is not itself performing a part. Ruled W10 is outside the proposed W1–7. |
| `'GROW Weekly - Autumn'!C111` | 11 · `plans[95]`, P0096 | Create festival/light-themed artwork. | Unclaimed | Conditional on actual festival/light-themed creation in 1B or an appropriate project; the open challenge/project does not guarantee that theme. W11 mismatch. |
| `'GROW Weekly - Autumn'!C112` | 12 · `plans[104]`, P0105 | Rehearse the group performance. | Unclaimed | Requires actual group performance rehearsal. Generic leadership preparation does not meet it. A performance route could serve it with a legitimate W12 timetable. |
| `'GROW Weekly - Autumn'!C113` | 13 · `plans[115]`, P0116 | Perform for an audience. | Unclaimed | Requires the pupil to perform to an audience. Attending as audience member in 1C is the opposite role; hosting/leading without performing is insufficient. W13 mismatch. |
| `'GROW Weekly - Autumn'!C114` | 14 · `plans[125]`, P0126 | Review the performance and event. | Unclaimed | The neighbouring workbook sequence is the pupil group performance. Review that actual performance/event; do not automatically bind the separate 1C audience review. Conditional performance-project review, W14 mismatch. |
| `'GROW Weekly - Autumn'!C115` | 15 · `plans[132]`, P0133 | Complete arts log + Explore/Bronze evidence. | Unclaimed | Not met by completing a Silver portfolio. The full outcome explicitly includes Explore/Bronze evidence; no award substitution or false completion. W15 mismatch. |
| `'GROW Weekly - Spring'!C88` | 16 · `plans[138]`, P0139 | Explore how artists express resilience and change. | Unclaimed | Conditional on real, source-supported practitioner work expressing resilience/change. 1D does not guarantee those themes. Never infer an artist’s feelings or life from visual style. W16 mismatch. |
| `'GROW Weekly - Spring'!C89` | 17 · `plans[143]`, P0144 | Develop a skill and record it in my arts log. | Unclaimed | Best unclaimed narrow content overlap: Silver 1B skill practice plus an actual located record can serve the full action. But this cell is W17, not proposed W2; it cannot be attached merely because the words match. |
| `'GROW Weekly - Spring'!C90` | 18 · `plans[156]`, P0157 | Plan an artwork on the theme of resilience. | Unclaimed | Conditional on the pupil’s own resilience-themed artwork plan. Do not pre-write a challenge or force private disclosure to obtain this cell. Proposed 1A is W1, not W18. |
| `'GROW Weekly - Spring'!C91` | 19 · `plans[169]`, P0170 | Create my resilience-themed piece. | Unclaimed | Conditional on actual pupil creation with that theme; neither an open challenge nor general leadership delivery guarantees it. W19 mismatch. |
| `'GROW Weekly - Spring'!C92` | 20 · `plans[182]`, P0183 | Review and improve my work. | Unclaimed | Possible 1B review/refinement route only when both review and actual improvement are taught/evidenced; a progress judgement or failed trial alone does not guarantee the full cell. W20 mismatch. |
| `'GROW Weekly - Spring'!C93` | 21 · `plans[195]`, P0196 | Research an artist or performer who inspires me (Bronze). | Unclaimed | Research/inspiration can overlap 1D, but needs the actual inspiring artist/performer and full task. The explicit (Bronze) qualifier also requires an honest curriculum/award mapping; never claim Bronze completion from Silver research. W21 mismatch. |
| `'GROW Weekly - Spring'!C94` | 22 · `plans[208]`, P0209 | Share Explore/Bronze portfolio evidence so far. | Unclaimed | Not met by sharing Silver evidence alone: the object of the action is explicitly Explore/Bronze portfolio evidence. W22 mismatch. |
| `'GROW Weekly - Spring'!C95` | 23 · `plans[221]`, P0222 | Develop drama or music skills for performance. | Unclaimed | Possible 1B performance challenge if actual drama/music skill development occurs; an open visual-art challenge or general leadership task does not guarantee this. W23 mismatch. |
| `'GROW Weekly - Spring'!C96` | 24 · `plans[234]`, P0235 | Devise a short performance about overcoming change. | Unclaimed | Requires devising an actual short performance with the specified overcoming-change theme. Neither rehearsing a talk nor a generic arts project guarantees it. W24 mismatch. |
| `'GROW Weekly - Spring'!C97` | 25 · `plans[247]`, P0248 | Rehearse and refine the group performance. | Unclaimed | Requires actual group rehearsal and refinement. Could fit a performance challenge/project, with separate evidence of any claimed leadership role. No generic Unit 2 equivalence. W25 mismatch. |
| `'GROW Weekly - Spring'!C98` | 26 · `plans[260]`, P0261 | Perform for an audience. | Unclaimed | Requires the pupil’s actual audience-facing performance. Do not use 1C audience attendance or a portfolio share as a substitute. W26 mismatch. |

## Additional spine cells are not a hidden supply of Easter targets

The remaining **16** GROW Art cells are absent from this 23-plan target set: two already-owned autumn cells, one non-timetabled spring cell, and thirteen summer cells. They were checked so that absence from `EASTER_TARGETS` is not mistaken for absence from the real workbook.

| Cell | Ruled week | Verbatim outcome | Status for this proposal |
|---|---|---|---|
| `'GROW Weekly - Autumn'!C102` | 1 | Explore materials and techniques in my chosen art form. | Already owned. No new coverage; not a free target. |
| `'GROW Weekly - Autumn'!C109` | 9 | Explore festival music, sound and instruments. | Already owned. No new coverage; not a free target. |
| `'GROW Weekly - Spring'!C99` | NOT-TIMETABLED | Review the performance; complete arts log + Bronze evidence. | Not timetabled under the ruled spine; no lesson-week claim. |
| `'GROW Weekly - Summer'!C94` | 27 | Explore nature and environment as inspiration for art. | Unclaimed in the current scan, but outside this Easter target set and the proposed W1–7 programme. No automatic authority to add it. |
| `'GROW Weekly - Summer'!C95` | 28 | Develop a skill and record it in my arts log. | Unclaimed in the current scan, but outside this Easter target set and the proposed W1–7 programme. No automatic authority to add it. |
| `'GROW Weekly - Summer'!C96` | 29 | Plan a nature/environment artwork. | Unclaimed in the current scan, but outside this Easter target set and the proposed W1–7 programme. No automatic authority to add it. |
| `'GROW Weekly - Summer'!C97` | 30 | Create my environment-themed piece. | Unclaimed in the current scan, but outside this Easter target set and the proposed W1–7 programme. No automatic authority to add it. |
| `'GROW Weekly - Summer'!C98` | 31 | Review and improve my work. | Unclaimed in the current scan, but outside this Easter target set and the proposed W1–7 programme. No automatic authority to add it. |
| `'GROW Weekly - Summer'!C99` | 32 | Research an artist or performer (Bronze). | Unclaimed in the current scan, but outside this Easter target set and the proposed W1–7 programme. No automatic authority to add it. |
| `'GROW Weekly - Summer'!C100` | 34 | Complete and share Explore/Bronze portfolio evidence. | Unclaimed in the current scan, but outside this Easter target set and the proposed W1–7 programme. No automatic authority to add it. |
| `'GROW Weekly - Summer'!C101` | 35 | Develop music/drama skills for the summer production. | Unclaimed in the current scan, but outside this Easter target set and the proposed W1–7 programme. No automatic authority to add it. |
| `'GROW Weekly - Summer'!C102` | 36 | Learn parts and rehearse for the production. | Unclaimed in the current scan, but outside this Easter target set and the proposed W1–7 programme. No automatic authority to add it. |
| `'GROW Weekly - Summer'!C103` | 37 | Make set, props or artwork for the celebration. | Unclaimed in the current scan, but outside this Easter target set and the proposed W1–7 programme. No automatic authority to add it. |
| `'GROW Weekly - Summer'!C104` | 38 | Final rehearsal for the summer performance. | Unclaimed in the current scan, but outside this Easter target set and the proposed W1–7 programme. No automatic authority to add it. |
| `'GROW Weekly - Summer'!C105` | 39 | Perform in the summer production for an audience. | Unclaimed in the current scan, but outside this Easter target set and the proposed W1–7 programme. No automatic authority to add it. |
| `'GROW Weekly - Summer'!C106` | 40 | Review the performance; complete arts log + Bronze evidence. | Unclaimed in the current scan, but outside this Easter target set and the proposed W1–7 programme. No automatic authority to add it. |

Summer nature/environment planning, making and review could form an optional future pupil-authored practice challenge; the performance rows could fit a genuine performance project. Such routes need actual teaching, the real ruled timetable and their own canonical plan. Summer’s explicit Explore/Bronze portfolio actions cannot be renamed Silver. This review does not authorise importing any of these rows into the current batch.

## Existing claimant paths

| Cell | Current claimant | Source and binding result |
|---|---|---|
| `'GROW Weekly - Autumn'!C102` | `Grow/Slideshows/GROW_ART_W1_Art_Battle_Tasters.html` | spine-audited/ALIGNED; g29 SKIP |
| `'GROW Weekly - Autumn'!C103` | `Art_Teesside/GROW_W1-W8_2026-27/GROW_Art_W2_Develop_A_Skill_And_Record_It_In.html` | body + lesson-config + manifest; g29 PASS |
| `'GROW Weekly - Autumn'!C104` | `Art_Teesside/GROW_W1-W8_2026-27/GROW_Art_W3_Plan_An_Identity_Portrait_Or_Piece.html` | body + lesson-config + manifest; g29 PASS |
| `'GROW Weekly - Autumn'!C105` | `Art_Teesside/GROW_W1-W8_2026-27/GROW_Art_W4_Create_My_Identity_Piece_BHM_Artist_Inspiration.html` | body + lesson-config + manifest; g29 PASS |
| `'GROW Weekly - Autumn'!C106` | `Art_Teesside/GROW_W1-W8_2026-27/GROW_Art_W5_Review_And_Improve_My_Work.html` | body + lesson-config + manifest; g29 PASS |
| `'GROW Weekly - Autumn'!C107` | `Grow/Slideshows/GROW_ART_W6_Artist_Research.html` | spine-audited/ALIGNED; g29 SKIP |
| `'GROW Weekly - Autumn'!C108` | `Grow/Slideshows/GROW_ART_W7_Share_The_Portfolio.html` | spine-audited/ALIGNED; g29 SKIP |
| `'GROW Weekly - Autumn'!C109` | `Grow/Slideshows/GROW_ART_W8_Festival_Sounds.html` | spine-audited/ALIGNED; g29 SKIP |

## Binding conditions that preserve Silver

1. **Full cell action:** the actual lesson must teach the entire outcome in every support route. Open challenge/project options do not guarantee identity, BHM inspiration, resilience, festival art, drama/music or group performance. A pupil may genuinely choose one of those routes; that does not make every learner-facing deck globally serve that themed cell.
2. **Pupil authorship:** 1A/1B offer choices and prompts. Never pre-write a challenge, plan or review to force a cell match. A curriculum theme may inform genuine pupil choices, but any changed brief needs to preserve ownership and the original award requirement.
3. **Role and evidence:** performing, leading, attending as an audience member, researching, and sharing a portfolio are different actions. Silver 1C still needs an actual audience experience, artistic-quality/creative-impact review and evidenced sharing. Silver 1D still needs first-hand practitioner contact, organisation research, education AND career pathways and the pupil’s influence summary. Generic artist research does not finish 1D.
4. **Identity and timetable:** reconcile the real workbook strand, full outcome and ruled week with the canonical Silver plan. A higher award or LAUNCH catalogue placement does not itself reassign a GROW workbook cell. Do not edit a week or omit a qualifier just to make g29 pass.
5. **Ownership:** preserve existing claimants and the one-deck/one-cell Art rule. A semantic overlap with an owned cell is not new coverage. An unclaimed matching action at W17 is not interchangeable with W2.
6. **Nine parts remain:** no cell shortcut removes Silver’s two separately evidenced units, 1A–1D/2A–2E, one Attempted per unit, twenty-file cap or four assessment areas.

**Concrete outcome:** keep the proposed Silver rows without new cell claims unless a later, properly authorised mapping passes all these checks. Record the genuine potential match to Spring C89 and the conditional rows above; do not report that “Silver has no possible workbook matches.” No workbook change or blanket award-cell hold has been inferred.

## Reproduction and source fingerprints

- Workbook SHA-256: `5b56e6a9a18f3d79816ac02cc66067d3af42ff06b71ee4c0b73d78eddea93c8a`.
- `EASTER_TARGETS.json` SHA-256: `e3415a8bad6ae6bd00749dfd97935ffe8ef56a2035e5ea9aa3e306eebd4ef4fb`.
- `CALENDAR_SPINE.json` SHA-256: `646edbfff4d815cd297367a807a4a836c158d79799fa9fe9e9b36b6bd12c16a2`.
- Award authority: `tools/artsaward/SPEC.json`, Silver and universal rules, plus the supplied AAE-R1B mandate. No external standard or exemplar was substituted.
- Read-only controls: `cell_coverage.load()`, `cell_coverage.ruled_week()`, `g29_plan_binding.load_plans()`, `g29_plan_binding.judge()`. Imports used `PYTHONDONTWRITEBYTECODE=1`; tool main/report writers were not called. Actual workbook values were compared against all 39 GROW Art spine entries.
