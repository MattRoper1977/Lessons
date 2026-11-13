# SX3 — PASS 7 CLOSE (one readback, ORDER FINISH S5) — 2026-09-20 00:47Z

## 1. Per-repo main and every main-push workflow (run ids)

**Lessons main `cbfbc70c`** (#595 squash, 00:17Z): UX2 gates 35478360136 SUCCESS; Education Pages publication 35478360629 SUCCESS; FieldOps P2 35478360130 SUCCESS; Made by Matt cross-estate unification 35478360154 **SUCCESS** (live-proof leg included, completed 00:33Z); GLV3 not triggered.

**Previous Lessons head `545d9e8b`** (#591 squash, 23:40Z):
| workflow | run | verdict |
|---|---|---|
| Education Pages publication | 35476763636 | SUCCESS |
| FieldOps P2, the sweep, and the serve proof | 35476763297 | SUCCESS |
| UX2 gates · Made by Matt cross-estate unification · GROW LAUNCH v3 | not triggered (paths) | — |
Previous heads this order: `18ff3333` (#590): publication 35475673519 SUCCESS, FieldOps 35475673293 SUCCESS, three not triggered. `b32bf1c7` (#594): UX2 35472218239 SUCCESS, publication 35472218580 SUCCESS, FieldOps 35472218231 SUCCESS, cross-estate 35472218232 **FAILURE** (live-proof, STOP-P1), GLV3 not triggered.

**Apps main `bbce3771`** (#118 squash, 00:17Z): Education Pages publication 35478375554 SUCCESS; Verify LundyLoop Professional OS 35478375212 SUCCESS; Made by Matt cross-estate unification 35478375227 **SUCCESS**; GLV3 not triggered. Previous head `85f7e07f` (#117): publication 35472709978 SUCCESS, LundyLoop 35472709689 SUCCESS, cross-estate 35472709705 FAILURE (live-proof, STOP-P1) — closed by the control.

**Site main `1e98bec0`** (#412 squash, 00:16Z): Splash region records 35478319755 SUCCESS; MBM audience discovery closeout 35478319729 SUCCESS; Education publication 35478319781 SUCCESS; Domain split publication 35478319728 SUCCESS (00:44Z); Professional site design audit and AGX-1 live verification not triggered on push. Previous head `a1b2a85c` (#411): MBM audience discovery closeout 35471407959, Education publication 35471407932, Domain split publication 35471407923, Splash region records 35471407916 — all SUCCESS.

**Watch main (observer, separate):** dispatch 35475189621 FAILURE on b32bf1c7 (it reported the cross-estate red). Re-dispatched after the control pair merged: run 35479185188 on `cbfbc70c` **SUCCESS** (00:35Z).

## 2. STOP-P1 — attributed once, then closed by the control

Attribution (L12, CI's own measurement of the origin, live-proof job 105928321042 / run 35447908661 attempt 2): the served origin is UP and STABLE; only the typed table is stale.
| route | PINNED (check_tokens_inert.cjs:22) | SERVED (origin, HTTP 200) | |
|---|---|---|---|
| lessons `""` | `01e571fa…` | `5c4e3ced…` | MISMATCH |
| lessons `subject.html` | `048f41f8…` | `93a071a8…` | MISMATCH |
| `/assets/mbm-tokens.css` | `2e78ad73…` | matched | — |
(apps `""` pinned `a2d5dedc…`, registry CURRENT `f15bc17d…`.)

Closed by the control pair: Lessons #595 (`7e540bf5`) + Apps #118 (`34660c47`) — `tools/sw2/pin_published_digests.py` derives the three from the Site admission registry (CI-proved: green publications on both mains); the derived values equal the SERVED digests CI measured. --check RED 3/3 → PASS; self-test 6/6; gate copies re-pinned byte-identical `f38a2a6f`. State: both merged (Lessons `cbfbc70c`, Apps `bbce3771`). Cross-estate on main after the pair: Lessons 35478360154 SUCCESS, Apps 35478375227 SUCCESS — STOP-P1 closed on both mains. Watch main re-dispatched: 35479185188 SUCCESS on `cbfbc70c`.

The separation window (Education Pages publication red on Lessons main from `ca184d38` to the retained-registry re-freeze `d0dc6b3e` at Site #408 `0cd8f842` / Lessons #581 `eab8daaf`; then the resource-sizes STOP-R at `124f513b`, closed by Site #411 `a1b2a85c` + Lessons #594 `b32bf1c7`): opened `ca184d38`, closed `b32bf1c7` — publication SUCCESS 35472218580 and on every main since.

The S1 deeper log read (to the `##[error]`) was not retaken: the one granted read reached only the tail (instrument slip, #10 family). Attribution above rests on L12's earlier read of the same job class, not on 35472218232's log.

## 2b. Stops carried into the close (not ruled here)
- **S1 STOP-X.** The one granted log read on cross-estate 35472218232 was taken at tail depth and did not reach the `##[error]`; a deeper read was not retaken. Attribution to the three STOP-P1 routes rests on L12's earlier read of the same job class (run 35447908661), and is now moot in effect: the control pair derived exactly those served digests and both mains' cross-estate runs are green.
- **S3 STOP-B (PASS 5, 3c).** Rows 37/38/39/41 on SERVED bytes for one deck per pathway, `/hud.js` 200 on a BUILD and a LAUNCH route, LISTED + DISTINCT against the served hub, composite card titles == served `<h1>` ×31, and the three START_HERE 200 with palette and ← Lessons resolving: not measured. The served origin is 403 from this container and the earlier built tree is gone; a granted build (or Matt's phone) is the instrument. Source-side facts stand: composite card titles carry a "PATHWAY Science Wnn ·" prefix before the deck h1; LISTED has resources.json rows for 5 of 36; the START_HERE pages carry data-pathway and ← Lessons `../../index.html`.
- **Site pin SHA (S4).** The order named b32bf1c7; Lessons main has since taken #590, #591 and #595. The lag control shows the two carrier pins EQUAL in published content (0 published paths moved) and 3 commits behind by SHA; the closing pin move is the next order's, with the control as the instrument.
- **HELD count.** 25 (A 10 + B 10 + D 5) against the order's 24, as HELD.md records.

## 2c. HUM-D5 arc, state at this close
Part A closed on `claude/hum-d5-proof` (head a4a6ba7c): rulings H1–H9 applied and dispositioned B0001–B0130 (PROOF_LEDGER.md), HUMD5_PARTA_CLOSE.md delivered, E6 re-measured (svg-img-alt / nested-interactive / select-name → 0; contrast residue = the model-node ribbon only, B0125 report-only). Eight decisions are Matt's (PARTA_CLOSE §5). Part B: PARTB_PLAN.md (STOP-B1) written — draft and adversarial re-measure kept apart; no landing branch, nothing pushed to one; token if attempted now `HUMD5_BLOCKED:science-S5-readback-not-accepted;part-a-eight-decisions-open`.

## 3. PR / SHA ledger, merge order (this order)
| repo | PR | head | merge | note |
|---|---|---|---|---|
| Site | #411 | 2f36f00b | `a1b2a85c` squash | registry pair re-cut; both Lessons pins held EQUAL |
| Lessons | #594 | 0248ea78 | `b32bf1c7` squash | carrier → a1b2a85c; caller digest 16448b91 |
| Apps | #117 | 167195b | `85f7e07f` | gate copy mirrored 6bd51afc |
| Lessons | #590 | 8217a180 | `18ff3333` squash | breach record, docs-only |
| Lessons | #591 | ef1b02a0 | `545d9e8b` squash | toolchain, sweep, PASSES ledger, L24 record |
| Site | #412 | 4cb7f4d2 | `1e98bec0` squash | sixth-pin discharge + lag control; 5/5 SUCCESS on the head |
| Lessons | #595 | 7e540bf5 | `cbfbc70c` squash | PUBLISHED re-derivation control; 3/3 SUCCESS on the head |
| Apps | #118 | 34660c47 | `bbce3771` squash | its companion; 3/3 SUCCESS on the head; gate copies f38a2a6f on both mains |
Four empty-PR closes: already done 2026-09-18 17:44–17:45 — #577, #579, #582, #583, each with a comment naming the held decks and linking `_sx3/HELD.md`; branches kept.

## 4. Landed 31, by pathway (+ 3 START_HERE)
- BUILD (1): SCI_B_W12_Give_a_rock_a_job_Classic (R-GAPS row 30 `.teacher-only`, the one named exception).
- GROW (7): SCI_G_W9A_Spherical_Bodies_Explore, SCI_G_W9_Turn_Earth_explain_the_sky_Classic, SCI_G_W10A_Solar_System_Research_Explore, SCI_G_W11A_Global_Warming_Explore, SCI_G_W12A_Science_Connections_Explore, SCI_G_W12_Follow_the_warming_chain_Classic, SCI_G_W13A_Rover_Rescue_Plan_Explore.
- LAUNCH (23): W9 L1–L3 + W9 Classic; W10 L1–L3; W11 L1–L3; W12 L1–L3 + W12 Classic; W13 L1–L3; W14 L1–L3; A2 W7 L1–L3.
- START_HERE (3): Science_Teesside/Build|Grow|Launch/START_HERE.html at 72b931f7 / 23ce9304 / 97037f62 (type teacher, no shelf entry).
Served proof (S2, CI's measurement relayed via the FieldOps serve job on b32bf1c7, run 35472218231): 59 served byte-identical · 0 red · 0 inconclusive (site 38, lessons 20 = 4 labs + hub + 15 LAUNCH decks, apps 1); the 15 LAUNCH decks and the hub serve at their registry-admitted digests; the remaining 16 landed decks + 3 START_HERE + composite + resource-sizes are registry-admitted and published green (run 35472218580) but not individually in that serve job's route set.

## 5. HELD.md — 25 by name (+15 parked)
- A (10, second generation, Ruling 4): SCI_B_W9A_Rock_Evidence_Explore, W9B_Rock_Sorting_Key_Do, W10A_Rock_Hardness_Explore, W10B_Hardness_Evidence_Do, W12A_Rock_Jobs_Which_Property_Matters_Explore, W12B_Choose_Rock_For_The_Job_Do, W13A_Fair_Test_Planner_Change_One_Thing_Explore, W13B_Method_Pilot_Test_The_Test_Do, W14A_Autumn_Science_Review_Explore, W14B_Autumn_Science_Evidence_Do.
- B (10, Original Science stage contract): SCI_B_W3_Backbones, W4_Muscle_Pairs, W5_Right_Nutrition, W6_Balanced_Plate, W7_Where_Food_Comes_From; SCI_G_W3_Friction, W4_Mechanisms, W5_Fair_Test, W6_Earth_And_Planets, W7_The_Moon.
- D (5, body provenance — carry the `_Explore` partner's lesson): SCI_G_W9B_Spherical_Bodies_Do, W10B_Solar_System_Presentation_Do, W11B_Climate_Action_Do, W12B_Science_Answer_Lab_Do, W13B_Rover_Rescue_Investigation_Do.
- C parked (15, LAUNCH W3–W7, 0 print pages in the authoritative generation): SCI_L_W3_L1–L3, W4_L1–L3, W5_L1–L3, W6_L1–L3, W7_L1–L3.
HELD.md's own arithmetic says 25 (A+B+D) against the order's 24; recorded there, not reconciled away.

## 6. Breach + history branch
`git push -f origin claude/sx3-build-1` (2026-09-18) replaced seven transplant commits with one squash; nothing lost — `d93ac149` preserved as `claude/sx3-build-1-history`, never merged, never deleted; recorded in #590 (`18ff3333`) with the standing rule restated: a rewrite that needs -f is the signal to add a commit instead.

## 7. Instrument corrections + checklist
#1–#5 standing (RELEASE_LEDGER "Five instrument corrections"); #6 derive a SHA from the ref, never transcribe; #7 get_job_logs needs return_content=true and the blob host is 403 here; #8 actions_list filters are advisory — filter locally; #9 completion ≠ verdict; #10 an instrument answers a narrower question than asked (tail truncation, string-only index); #11 a force-revealed text index is not a visibility measurement (HUM-D5); #12 getBoundingClientRect is scaled by an ancestor's entrance animation (HUM-D5). Pre-CI checklist: the four-writer sweep + census tail (`tools/sx3/pre_ci_catalogue_sweep.sh`, landed in #591), regenerate AND pin, commit generated records before any branch switch, refs refreshed explicitly.

## 8. FINDINGS (pointers)
77/129 SCIENCE_WEEK_BINDINGS stale (55 by sourceSha256) and `build_science_shelf.py` dead → STOP_C2b_shelf_restore.md; 31 evidence digests re-stamped (20 of 875 had drifted, green by absence) and the evidence record not reproducible from its builder (38 entries) → RELEASE_LEDGER "Backlog"; two catalogue checks that were never run → RELEASE_LEDGER l.1439; census first-failing-tree (L23/L24: STATIC_CHECK_RESULTS self-referential baseline); carrier drift → Site #412's lag control (13 pins, not six); two `prepare_one` copies → RELEASE_LEDGER "The two selector copies"; trigger/boundary pair → STOP_ADM_admission.md; evidence model / fallback limb two arms → RELEASE_LEDGER "FENCE" (11 decks) and l.1170; STOP-P1 re-pin → the control pair; GLV3 fires on Science_Teesside/** → RELEASE_LEDGER l.1899; Domain split publication path-filter gap → L3.

## 9. Next-order inputs (one document)
1. Authoring order, four lanes: Held B scaffold re-cut per Matt's ruling (I do / We do / Independent Work preserved, 10 decks); Held A (10, needs the generation ruling); the 5 GROW `_Do` (body provenance); the 15 LAUNCH W3–W7 print lane.
2. Shelf restore: 55/51/Spr2·W6/two-week — STOP_C2b_shelf_restore.md.
3. Bindings and evidence: 77 bindings, 31 evidence, the 38-entry non-reproducible evidence record; one deck registry instead of four.
4. The two `prepare_one` copies unified with a comparison control.
5. FieldOps ordering dependency (the serve job reads the latest publication artifact; a build after the served one changes the comparison).
6. Domain split publication path-filter gap (L3).
7. Lessons typed-literal census (the gap C1 stands in for).
8. The four b54c9006 pins: policy "one step behind" restated, moved only with a reviewed re-stamp.

## 10. Phone-check URLs
- BUILD: https://madebymatt.uk/Lessons/Science_Teesside/Build/W8-W13_2026-27/SCI_B_W12_Give_a_rock_a_job_Classic.html
- GROW: https://madebymatt.uk/Lessons/Science_Teesside/Grow/W8-W13_2026-27/SCI_G_W9A_Spherical_Bodies_Explore.html
- LAUNCH: https://madebymatt.uk/Lessons/Science_Teesside/Launch/W8-W13_2026-27/SCI_L_W9L1_Cell_Cycle_Introduce.html
- parent START_HERE: https://madebymatt.uk/Lessons/Science_Teesside/Launch/START_HERE.html
- Science shelf: https://madebymatt.uk/Lessons/Science_Teesside/index.html
(prefix `Lessons` derived from the cross-estate workflow's published base; deck paths are the published paths in the admission registry (git ls-files; only the BUILD deck has a resources.json row of its own).)

## 11. Trees — clean, nothing running (00:48Z)
| checkout | branch @ head | dirty |
|---|---|---|
| Site `/home/user/mattroper1977.github.io` | main @ 1e98bec0 | 0 |
| Lessons `/home/user/lessons` | claude/hum-d5-proof @ a4a6ba7c (pushed) | 0 |
| Lessons carrier worktree | claude/sx3-carrier-a1b2a85c @ 0248ea78 (merged as #594) | 0 |
| Lessons toolchain worktree | claude/sx3-toolchain @ ef1b02a0 (merged as #591) | 0 |
| Lessons control worktree | claude/sx3-published-pin @ 7e540bf5 (merged as #595) | 0 |
| Lessons close worktree | claude/sx3-pass7-close @ cbfbc70c + this record | 0 after commit |
| Apps `/home/user/matt-s-apps-` | claude/sx3-apps-pair4 @ 6df9e94 — the ruled-discard amendment dropped (git status first) | 0 |
| Apps companion worktree | claude/sx3-apps-carrier-a1b2a85c @ 167195b (merged as #117) | 0 |
| Apps control worktree | claude/sx3-apps-published-pin @ 34660c47 (merged as #118) | 0 |
No node, chromium, render or apply process alive; no background wait armed. No branch deleted; no force-push anywhere this order.
