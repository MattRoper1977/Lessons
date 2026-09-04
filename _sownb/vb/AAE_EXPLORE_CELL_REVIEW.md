# Explore: independent BUILD Art cell measurement

Read-only review of the current working tree. No repository file, target, cell claim or deck was changed. This assessment does not transfer Bronze’s AAE-H7 ruling to Explore.

## Measured result

`tools/easter/EASTER_TARGETS.json` contains **24 BUILD Art plans, one cell each**. Its measured SHA-256 is `e3415a8bad6ae6bd00749dfd97935ffe8ef56a2035e5ea9aa3e306eebd4ef4fb`.

Using the existing `cell_coverage.load()` read path scanned **691 HTML surfaces / 525 recognised lesson surfaces**, plus manifest and audited-spine claims. Among these 24 target cells:

- **7 have a current claim:** `'BUILD Weekly - Autumn'!C102` through `C108`.
- **17 have no current claim** in that scan: Autumn C110–C115; Spring C88–C98.
- Each of the seven has one current claimant, with agreeing **body + lesson-config + manifest** sources.
- Calling the existing `g29_plan_binding.judge()` on those seven current claimant files returned **7 PASS**, with `outcomesMatch: true` for all seven. This validates their current plan bindings, not a fresh independent semantic reassessment of their teaching.
- `BATCH3_TARGETS.json` identifies the landed campaign routes for C102–C105; `BATCH4_TARGETS.json` identifies C106–C108. Both build reports record their batches as passed. The coverage column below therefore distinguishes an existing landed claim from an unclaimed target. “Unclaimed” does not assert that no old lesson anywhere has related content.

These are new measurements of Explore’s potential target space. A cell does not need to literally say “Explore Part A” to be teachable within an Explore lesson. A candidate must, however, serve its entire real workbook outcome as well as its award requirement. Broad overlap is not permission to claim the cell.

## Definitions used in the mapping

The sequence numbers refer to `bronze-drafts/explore-plan-review.md` outside the repository.

- **EXACT, narrow cell action:** the proposed sequence already entails the complete workbook action at planning level. It is not a complete award-part match, a built deck, or a new coverage claim.
- **POSSIBLE:** a specific addition or change is needed before the proposed teaching guarantees the whole workbook outcome. Current wording is insufficient for a claim.
- **NOT MATCHED:** the current drawing/paper-sculpture/artist/organisation sequence does not teach the required performance, music or drama activity. Replacing an activity could make a different valid sequence, but this would be more than attaching a cell label.

All 24 rows derive from workbook path `_passsb/inputs/Build SOW 2026-2027.xlsx`, under `Creative Arts (Trinity Arts Award Discover)`. Their qualified sheet/cell references are reproduced below. The exact plan location is `tools/easter/EASTER_TARGETS.json`, with zero-based `plans[index]` and its legacy `planId`. The existing Discover strand label is a real mapping constraint; it must not silently be rewritten to Explore.

## Complete 24-cell table

| Plan path within EASTER_TARGETS.json | Workbook cell | Ruled week | Verbatim outcome | Current covered/claimed status | Proposed Explore mapping |
|---|---|---:|---|---|---|
| `plans[8]`, P0009 | `'BUILD Weekly - Autumn'!C102` | 1 | Explore drawing, colour and technique to show identity. | Existing landed claimant C102 below; g29 PASS. | **POSSIBLE**, A decks 1–2. They teach drawing and tone, but do not currently guarantee colour or an identity purpose. Already claimed: no new coverage. |
| `plans[17]`, P0018 | `'BUILD Weekly - Autumn'!C103` | 2 | Create an identity piece using a chosen medium. | Existing landed claimant C103; g29 PASS. | **POSSIBLE**, C decks 9–12, only if the new artwork is explicitly an identity piece with pupil-chosen medium. Current proposal leaves theme open. Already claimed. |
| `plans[27]`, P0028 | `'BUILD Weekly - Autumn'!C104` | 3 | Find out about an artist whose work I like | Existing landed claimant C104; g29 PASS. | **POSSIBLE**, B decks 5–8, if the pupil identifies genuine interest/liking for a work and explores that artist. A slot-selected artist is not automatically one the pupil likes. Explore B still requires the organisation and live/active experience. Already claimed. |
| `plans[36]`, P0037 | `'BUILD Weekly - Autumn'!C105` | 4 | Try a new art technique and review it. | Existing landed claimant C105; g29 PASS. | **POSSIBLE**, A decks 2/4. Make the new-to-the-pupil technique and its review explicit, rather than assuming all taught techniques are new. Already claimed. |
| `plans[47]`, P0048 | `'BUILD Weekly - Autumn'!C106` | 5 | Add to my arts log (photo + comment). | Existing landed claimant C106; g29 PASS. | **POSSIBLE**, C process decks 10–12. Proposal currently allows several record formats and does not guarantee both a photo and a comment. Photographing the artwork can avoid photographing pupils. Already claimed. |
| `plans[56]`, P0057 | `'BUILD Weekly - Autumn'!C107` | 6 | Share my identity piece with the group. | Existing landed claimant C107; g29 PASS. | **POSSIBLE**, only with an actual identity-piece group share. D’s pupil-chosen enjoyment/achievement cannot be replaced by mandatory display of one prescribed piece; any C share and D communication must remain distinct. Already claimed. |
| `plans[65]`, P0066 | `'BUILD Weekly - Autumn'!C108` | 7 | Reflect on identity in my artwork. | Existing landed claimant C108; g29 PASS. | **POSSIBLE**, C/D reflection only if art-related identity is genuinely addressed. The current proposal does not impose Bronze’s identity theme on Explore. Already claimed. |
| `plans[83]`, P0084 | `'BUILD Weekly - Autumn'!C110` | 10 | Keep a steady beat / join a group piece. | No current claim in the scan. | **NOT MATCHED.** Drawing and paper sculpture do not teach keeping a beat or joining a group music piece. Could replace an A activity with properly taught group rhythm; the other distinct activity and learning evidence must remain. |
| `plans[94]`, P0095 | `'BUILD Weekly - Autumn'!C111` | 11 | Create festival-themed art (light/colour). | No current claim. | **POSSIBLE**, C decks 9–12 if a researched festival/light/colour art brief is deliberately chosen and the complete creation process/final work retained. Avoid asserted attendance, personal religious disclosure, or importing a theme absent from §5. |
| `plans[103]`, P0104 | `'BUILD Weekly - Autumn'!C112` | 12 | Rehearse a short performance. | No current claim. | **NOT MATCHED.** Rehearsing how to explain an artwork is not necessarily rehearsing an arts performance. Would require a real performance activity. |
| `plans[114]`, P0115 | `'BUILD Weekly - Autumn'!C113` | 13 | Perform for an audience (seasonal showcase). | No current claim. | **NOT MATCHED.** A D conversation or visual-work display does not guarantee an arts performance or seasonal-showcase context. Never claim a showcase exists without an actual arrangement. |
| `plans[124]`, P0125 | `'BUILD Weekly - Autumn'!C114` | 14 | Review what went well in my performance. | No current claim. | **NOT MATCHED.** The current proposal contains no pupil arts performance to review. Generic achievement reflection is not sufficient. |
| `plans[131]`, P0132 | `'BUILD Weekly - Autumn'!C115` | 15 | Add performance evidence to arts log (Award). | No current claim. | **NOT MATCHED.** An artwork process record is not performance evidence. Requires actual performance and an accurately located record. |
| `plans[137]`, P0138 | `'BUILD Weekly - Spring'!C88` | 16 | Use colour/sound to express a feeling. | No current claim. | **POSSIBLE**, A deck 2: add actual colour or sound choices intended to express a chosen feeling and record what was learnt. A fictional scene or supplied mood can avoid personal disclosure. Tone alone without that expressive purpose is insufficient. |
| `plans[142]`, P0143 | `'BUILD Weekly - Spring'!C89` | 17 | Create art linked to an emotion (links PSHE). | No current claim. | **POSSIBLE**, C decks 9–12: create the distinct artwork with a chosen represented emotion and an explicit, safe link to emotion vocabulary. No demand to disclose a pupil’s own emotional life. Must retain process and final work. |
| `plans[155]`, P0156 | `'BUILD Weekly - Spring'!C90` | 18 | Find out about an artist who expresses feelings. | No current claim. | **POSSIBLE**, B decks 5–8: choose an actual practitioner whose expressive purpose is supported by a reliable source or first-hand explanation. Do not infer the artist’s feelings from colour. Artist exploration alone still leaves Explore B’s organisation requirement. |
| `plans[168]`, P0169 | `'BUILD Weekly - Spring'!C91` | 19 | Try a new expressive technique. | No current claim. | **POSSIBLE**, A decks 1–4: explicitly teach a new-to-the-pupil expressive use of line, colour or form, with real practice. Keep both distinct A activities and identify learning. Current generic technique instruction does not guarantee expressive intent or novelty. |
| `plans[181]`, P0182 | `'BUILD Weekly - Spring'!C92` | 20 | Review and improve my piece. | No current claim. | **POSSIBLE**, C deck 11: add an actual pupil review and a chosen, observable improvement, preserving the before state. “Develop and record a choice” alone does not guarantee review plus improvement. An unsuccessful change is honest process evidence but does not itself establish the cell’s improvement outcome. |
| `plans[194]`, P0195 | `'BUILD Weekly - Spring'!C93` | 21 | Add a review to my arts log. | No current claim. | **EXACT, narrow cell action**, A deck 4 plus the stated A-file evidence plan: the pupil compares learning from the two actual activities and records that review in the cumulative arts file. This is a planning-level semantic match only; current proposed week 2 does not equal ruled week 21, so no automatic binding or new claim follows. Keep the review explicit when drafting. |
| `plans[207]`, P0208 | `'BUILD Weekly - Spring'!C94` | 22 | Use freeze-frame/role-play to tell a story. | No current claim. | **NOT MATCHED.** No freeze-frame or role-play activity is proposed. Could replace one A activity with a complete accessible storytelling/drama activity; simply talking about a sculpture is not role-play. |
| `plans[220]`, P0221 | `'BUILD Weekly - Spring'!C95` | 23 | Develop a character with voice and movement. | No current claim. | **NOT MATCHED.** No character-development task, vocal work or movement work appears in the current sequence. |
| `plans[233]`, P0234 | `'BUILD Weekly - Spring'!C96` | 24 | Sequence a short drama with a group. | No current claim. | **NOT MATCHED.** Pair feedback or a group audience does not create a sequenced group drama. |
| `plans[246]`, P0247 | `'BUILD Weekly - Spring'!C97` | 25 | Rehearse and refine our performance. | No current claim. | **NOT MATCHED.** The proposal does not contain a group arts performance to rehearse and refine. |
| `plans[259]`, P0260 | `'BUILD Weekly - Spring'!C98` | 26 | Perform our drama (World Book Day link). | No current claim. | **NOT MATCHED.** No drama production or literary-event connection is taught. Do not invent a dated event or treat a generic D share as this performance. |

Count check: **13 POSSIBLE; 1 EXACT narrow action; 10 NOT MATCHED = 24**. Among the 17 unclaimed cells: **6 POSSIBLE; 1 EXACT narrow action; 10 NOT MATCHED**. **Zero new cells are claimed by this review.** No complete Explore part is equivalent to a single row above; the award evidence must still be assembled across the appropriate lessons.

## Existing claimant paths

All seven files currently contain the expected cell and outcome and pass the existing g29 binding check. They are the reason Autumn C102–C108 must not be counted as newly covered by a new Explore strand.

| Cell | Current claimant path |
|---|---|
| Autumn C102 | `Art_Teesside/BUILD_W1-W8_2026-27/BUILD_Art_W1_Explore_Drawing_Colour_And_Technique_To_Show.html` |
| Autumn C103 | `Art_Teesside/BUILD_W1-W8_2026-27/BUILD_Art_W2_Create_An_Identity_Piece_Using_A_Chosen.html` |
| Autumn C104 | `Art_Teesside/BUILD_W1-W8_2026-27/BUILD_Art_W3_Find_Out_About_An_Artist_Whose_Work.html` |
| Autumn C105 | `Art_Teesside/BUILD_W1-W8_2026-27/BUILD_Art_W4_Try_A_New_Art_Technique_And_Review.html` |
| Autumn C106 | `Art_Teesside/BUILD_W1-W8_2026-27/BUILD_Art_W5_Add_To_My_Arts_Log_Photo_Comment.html` |
| Autumn C107 | `Art_Teesside/BUILD_W1-W8_2026-27/BUILD_Art_W6_Share_My_Identity_Piece_With_The_Group.html` |
| Autumn C108 | `Art_Teesside/BUILD_W1-W8_2026-27/BUILD_Art_W7_Reflect_On_Identity_In_My_Artwork.html` |

## Adaptation options that preserve Explore evidence

The least disruptive semantic additions are Spring C91 (a taught expressive technique), C92 (review and improve the new C artwork), and C93 (record a genuine review). These are related but remain separate ruled-week plans. Do not merge them into one arbitrary target or change their workbook weeks merely to make a new strand fit.

A coherent optional expressive-art strand could also serve C88/C89/C90 if the actual art tasks, source-supported artist choice and safe emotion vocabulary are built into the teaching. The pupil can explore an assigned fictional mood; no private disclosure is necessary. This is a possible curriculum adaptation, **not** evidence that missing AAE §5 prescribed that theme. Do not make it a requirement until root has reconciled the governing order and timing.

Choosing music or drama as one of A’s two activities is allowed by the registered Explore requirement and could genuinely serve some of the currently unmatched cells. It would require actual teaching and activity time, an accessible participation route, and accurate records. It must not replace B’s active artist-and-organisation exploration, C’s distinct creation/process/final work, or D’s separate pupil-chosen communication.

Before any binding, reconcile three independent things:

1. **Teaching:** does every support route teach the full selected workbook outcome and preserve all Explore requirements?
2. **Identity and timetable:** does the declared target correspond to the real plan, ruled week and Discover-labelled workbook strand, with an explicit legitimate treatment of its relationship to Explore? No invented reference, silent relabel or false week match.
3. **Existing ownership:** does another deck already claim that cell? Current C102–C108 are owned; an additional claim must not be reported as new coverage or used to evade g29.

The result supports cautious, outcome-based mapping rather than “all Explore cells must be empty because Bronze had H7.” It also does not authorise changing the workbook, lowering evidence, forcing a theme or claiming coverage before the actual decks exist.

## Reproduction notes

Inputs read: `tools/easter/EASTER_TARGETS.json`; `tools/easter/BATCH3_TARGETS.json`; `tools/easter/BATCH4_TARGETS.json`; current claimant HTML; manifests and audited-spine data through `_sownb/vb/tools/cell_coverage.py`; `_sownb/vb/tools/g29_plan_binding.py`; and the proposed Explore plan review. The two tool calls used library functions only, with `PYTHONDONTWRITEBYTECODE=1`, and did not invoke report-writing main functions. Counts describe this working-tree observation, not an immutable remote revision or a fresh semantic audit of all 691 surfaces.
