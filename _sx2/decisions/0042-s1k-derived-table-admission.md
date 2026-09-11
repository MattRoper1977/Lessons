## S1-K — the derived-table admission ratchet and the coverage condition

Order S1-K, issued by Matt on 2026-09-11. K4 fallback, selected because K2 failed its source-input control.

K1: the constraint is general, not specific to #463.
The generator was invoked with --write on fresh prospective source trees for open PR #464 (b3c731bb7bf290b4d2909f5c7fb41cf039df82b3) and open PR #493 (c460eada50a93b266f7330e70cb436b82ec6304d), each over current Lessons main 8c7d3e9e4c24faf48c13f5d73bb70226703a7c12. Only generator inputs changed by each PR were overlaid; all other measured bytes were verified against main's Git blobs. Neither PR changes the generator or its two input manifests.
#464: seven measured HTML inputs change. Regenerated source-table SHA-256 e95e243275602ed3a0faabc199f2e3d81c7038c37b94303cc21662a81d3f7fcf; publisher-filtered SHA-256 273a5725d5315cb7c7d0da526a1601ac97a4c8d9415f2c32568b79603af22840. BLOCKED.
#493: the measured ICT/Teaching_Packs/index.html changes; its eleven additional HTML pages are outside this generator's inputs. Regenerated source-table SHA-256 7fe56f4a38ead37e945986fb66eb9f4813473e873c0cf4e637f112a16b3ef6c8; publisher-filtered SHA-256 ab5f6a6a16c2f2135c4ebadbf249a5c5b48475c3607237b4d5cf975a04b97425. BLOCKED.
Tested PRs blocked on the derived table: 2/2. This result concerns table admission, not the complete publication or browser checks of either PR.
Every new emitted size-table digest needs a new reviewed publisher admission. The narrower factual boundary matters: the generator measures listed file sizes, not arbitrary content bytes; a same-length edit or an edit outside its input set need not change the table.

K2: exact path membership was nominal for 31 inputs.
The input list was obtained by invoking paths() in tools/ux2/resource_sizes.py, not by a hand-maintained list: 1,494 measured file paths, plus the two selector manifests resources.json and data/companion-packs.json which choose them.
All 1,494 paths have exact entries in the active publisher's education-lessons registry. The publisher retains 1,463 as content subject to those exact-path rules, but substitutes route-only redirect stubs for 31 game sources. Counts of rule coverage for the measured inputs: covered 1,463; not covered 31; covered only by a path pattern 0; undetermined 0. These are rule-coverage counts, not 1,463 independent source-tamper experiments or a new full-build verdict.
The active publisher is Site 7072a5605e795b1c872f843f04f2403a8880c409. Its domain-split/build_education.py:234-241 writes moved_page(route) for classified games. The source bytes do not enter that output. domain-split/education_publication_admission.py:115-127 compares only emitted paths and digests.
Adversarial example: change exactly one byte of 2 Physics 10/current_rush.html in a scratch tree. Source SHA-256 changes from 944ee81e7b98b6ee031886e159771d2db5a9842864720224628d1dbf920da880 to 1f87296433bfc1236ca7f6d42de40eb153bfe6d4f53d2f17f408e2eaad286e25. The emitted stub remains 2375242fbb11a172bbf099dd4b8c31ea6cff5a6c4f471290272ac43e3bee5e96. Its production admission predicate exits 0. Mutating that stub itself exits 1 and names CHANGED education-lessons/2 Physics 10/current_rush.html. Restoring the source exits 0.
This fails K2's condition. K3 derivation-admission is forbidden in this state. No admission assertion, registry entry, publisher or caller pin was changed.

K4: synchronised-entry rule, adopted verbatim.
When a content PR changes the derived table, its new digest must be added to the admission list IN THE SAME COMMIT as the sources that produced it, never as a separate preparatory change. This does not remove the re-pinning cost.
D1 remains the measured authority: the registry is read from the pinned Site builder checkout, never from Site main or a proposed Lessons-local copy. Sources are in Lessons. These are different repositories. A preparatory Site registry commit followed by a Lessons pin-and-source commit is two commits, even if the new authority only becomes active on the second one. K0 does not authorise silently replacing K4's same-commit requirement with that two-commit protocol.
Consequently the rule is recorded and binding, but the literal same-commit publication route is blocked in the current architecture. No alternative registry, extra digest, different publisher or weakened assertion is introduced here. A later ruling must explicitly define a permitted cross-repository atomic activation or provide an authority which can travel in the source commit before this route can land content.

Named resumption condition: S1K_REAL_PUBLISHED_INPUT_COVERAGE.
K2 may be retried only when every generator input is bound by a real admission rule to the exact material used in the same published tree, including the selector manifests and trusted generator version; no measured source may be discarded into an admitted substitute before its bytes are guarded. The 31 route-only substitutions below must be resolved under an explicit order. A source-byte mutation must block that source, not merely its derived table or substitute. Then re-run the complete input enumeration and K2 firing control before considering K3.

Fresh #463 preflight against the K4 constraint.
The eight HTML files were fetched again at 1a6feedf7b5b861bbf25cd4d21321a7034f8177b and each verified against its Git blob. The two href="#mbm-science-pack" links per file were restored to their existing resources/WnLn.html targets, retaining the HUD navigation hook. This is a newly generated scratch candidate, not S1-J's saved candidate.
The named generator --write and --check exit 0. Source-table SHA-256 4318b5eb49b4663d2ddfeafce30a083e6a36efc34fd8ba3831569934793746b0. Publisher-filtered SHA-256 3775b6e3d046ba27b579bd1ddb4c3f5762b565aab0b695b8a18cded8e642c384.
The unchanged active admission exits 1: CHANGED education-lessons/data/resource-sizes.json. No browser pass, full publication or served-proof result is claimed. #463 and #464 remain unmerged. K6 remains pending the permitted landing route; the existing proof still covers Site 2 / Lessons 5 / Games 36 / Apps 1.

Uncovered measured source inputs follow; this list was generated from the generator and active publisher classifier.

2 Physics 10/current_rush.html
5 Intervention 10/InterventionA_Battle_Arena (1).html
5 Intervention 10/InterventionB_Escape_Room.html
5 Intervention 10/L8a_Powerhouse_Arena_TeamQuiz.html
5_6 Local Choice/Trekkers_Trail_Runner (2).html
Games/Globe_Snake (1).html
Games/Grapple.html
Games/Grid_Chase.html
Games/KidsVsStaff_Showdown (3).html
Games/Lumins.html
Games/Marble.html
Games/Neon_Garden.html
Games/Neon_Siege.html
Games/Neon_Snake_Overdrive.html
Games/OneGuy.html
Games/Orbital.html
Games/Prism.html
Games/Slipstream.html
Games/Slipstream_GP.html
Games/Static.html
Games/The_Last_Lighthouse_v1_1_The_Archipelago_Update_FINAL.html
Games/Trail_Runner.html
Games/Trekkers_Trail_Runner_Tees_Coast.html
Games/Vortex.html
Games/Voxel_Frontier.html
Games/WorldCup_ThreeLions_Final.html
Games/WorldCup_v3_MatchDirector.html
Games/WorldCup_v5_Showdown.html
Games/Wrecking_Crew.html
Games/voxelcraft.html
Summer Term Fun/Kids_vs_Staff_Studio_Game_Show_v8_Autopilot.html


## S1-M — permanent admission repair, 2026-09-11

The preceding S1-K text is a historical decision record. The cross-repository SAME COMMIT rule was voided by S1-L: it cannot be satisfied across two repositories and should never have been written that way. S1-M authorised Track B after the 31 mis-included / 0 legitimate classification.

The generator now excludes the handoff class from its size inputs. The exact difference from the deployed table was 31 paths, all 31 matching the preserved census, with zero unaccounted paths. The aligned generator emits 1,463 sizes and zero missing inputs. The deliberate downstream size-table filter moved to the generator; other catalogue filtering is unchanged.

Publisher 810ae8f8830dc9e30a7ceec9ada4ec24d575a04d, direct child of 7072a5605e795b1c872f843f04f2403a8880c409, admits only education-lessons/data/resource-sizes.json by derivation from the same finished published tree. Every other admission retains its existing digest assertion. The 1,463 aligned inputs are exactly covered: 0 uncovered, 0 pattern-only, 0 undetermined. A planted one-byte input defect was rejected on that input.

Wrong size, deleted table entry, and changed input without regeneration each blocked the full candidate publication on derivation, then passed after restoration. The final full preflight ran as 34596434017, job 103253153724, with all 61 controls passing. Other admitted paths still reject planted changes.

Lessons #509 merged at 67e9c6fea9c40d5f8c4b914cec311282aa7caa46, after Apps #80. Publication run 34597860802 reached deploy job 103259984344 SUCCESS; github-pages artifact 10263716116 was 707060767 bytes and expired false when verified. The derived-table digest ratchet is removed by this same-publication derivation assertion; it does not remove exact admissions for source content.

S1-M M5 repairs this PR's evidence artifact, not the sweep parser: its verification record now names the census file, and structured input records are generated from the unchanged ordered 31 paths. The bounded negative control reports an absent input as STALE — SUBJECT ABSENT and clears on exact restoration. The dry-run sweep reports stale rows with exit 0; that firing signal is the verdict and count, not a claimed nonzero exit.
