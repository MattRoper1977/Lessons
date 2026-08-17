# PH-1 final execution report — stopped on gate result

## BASE, tip and deployment commits

- BASE: `ae1d3c7af2526781aad6fb82e7cbbf6b87ded380`
- Gate input tip: `55c35cd68cdd423c7c9c16c68a34348a1150e9f9`
- Branch: `pass-ph1-peq-hardening`
- Census: `daf746f5d8894d1b56e203ed34b641b74b0e9522`
- P1: `4c8bfa413e3df3fa604daf4aafbab058c90f0cbf`
- P2: `e60f6500a22e93a2a4267e6bf20caf6f9c5f37a1`
- P3: `4c573608525d1a06e9d5d67376904ee3118f49e2`
- P4: `3f29c050fb5e8f42fc5d2aa1dbb7c02ce9bde2f5`
- P5: `3e66061012cfc4ebc5c01b02a1f3975e05537c8c`
- P6: `ae8631882d7d3a02e1bf0c12032e610513c52650`
- P7: `6e5b34981e667cc398bea364f35d5fd72e59104a`

## Census — predicted versus actual

| Census | Predicted | Actual |
|---|---|---|
| C1 | approximately 84 in LAUNCH PEQ | 84 live / 312 whole-tree |
| C2 | not fixed | 2 production pages |
| C3 | not fixed | 101 line-level occurrences; B1 18 / B2 80 / B3 3 / B4 0 |
| C4 | 0 | 0 |
| C5 | not fixed | 6 pages |
| C6 | report only | 0 |
| C7 | 0 | 1 affirmative Level 2 registration claim |

## P1–P7 status

| Item | Status | Reason |
|---|---|---|
| P1 | **DONE** | 2 staff/print minima blocks added; pupil tasks unchanged. |
| P2 | **PARTIAL** | 18 B1 occurrences corrected; 80 B2 and 3 B3 occurrences held; W6 filename unchanged. |
| P3 | **DONE** | 6 measured credit-route pages carry the corrected route rules. |
| P4 | **DONE** | 4 suite-level partial-achievement notes added. |
| P5 | **DONE — REPORT ONLY** | C6 was zero; no lesson wording changed. |
| P6 | **DONE** | 7 BUILD hub/START_HERE panels and 1 LAUNCH Vocational panel added. |
| P7 | **DONE** | Prohibited tools, automatic awards and PEQ002 credit claims were not deployed. |

## Gate results

| Gate | Result |
|---|---|
| G1 | **PASS** |
| G2 | **RED** |
| G3 | **PASS** |
| G4 | **PASS** |
| G5 | **PASS** |
| G6 | **RED** |
| G7 | **PASS** |
| G8 | **RED** |
| G9 | **PASS** |
| G10 | **PASS** |

**Overall: RED. Red gates: G2, G6, G8.**

Phase 4 records were **not** written. `REGISTER.md` and `_close/OPEN_ITEMS.md` remain unchanged because PH-1 forbids fix-forward or records closure past a red gate.

## Exact BASE-to-tip changed files

| File | Added | Deleted |
|---|---:|---:|
| `BUILD_ASDAN/BUILD_ASDAN_Hub.html` | 25 | 1 |
| `BUILD_ASDAN/Careers/CAREERS_W6_My_Career_Profile.html` | 1 | 1 |
| `BUILD_ASDAN/Careers/START_HERE.html` | 12 | 1 |
| `BUILD_ASDAN/Community_Project/COMM_W6_The_Handover_and_Its_Benefit.html` | 1 | 1 |
| `BUILD_ASDAN/Community_Project/START_HERE.html` | 12 | 1 |
| `BUILD_ASDAN/Duke_and_Enterprise/DUKE_W6_Pitch_and_Reflect.html` | 1 | 1 |
| `BUILD_ASDAN/Duke_and_Enterprise/START_HERE.html` | 12 | 1 |
| `BUILD_ASDAN/FoodWise/FW_W5_Prepare_a_Healthy_Snack.html` | 1 | 1 |
| `BUILD_ASDAN/FoodWise/FW_W6_Plan_a_Healthy_Meal.html` | 1 | 1 |
| `BUILD_ASDAN/FoodWise/START_HERE.html` | 12 | 1 |
| `BUILD_ASDAN/Living_Independently/LI_W6_Shopping_and_Change.html` | 1 | 1 |
| `BUILD_ASDAN/Living_Independently/START_HERE.html` | 12 | 1 |
| `Build/Slideshows/BUILD_DT_W6_Handover.html` | 1 | 1 |
| `GROW_ASDAN/GROW_ASDAN_Hub.html` | 2 | 0 |
| `GROW_ASDAN/Scheme_and_Resources.html` | 11 | 0 |
| `LAUNCH_ASDAN/LAUNCH_ASDAN_Hub.html` | 13 | 0 |
| `LAUNCH_ASDAN/PEQ/PEQ_W4_Plan_a_Communication_Activity.html` | 14 | 1 |
| `LAUNCH_ASDAN/PEQ/PEQ_W5_Deliver_the_Activity_and_Gather_Evidence.html` | 14 | 1 |
| `LAUNCH_ASDAN/PEQ/PEQ_W6_Review_Progress_and_Sign_Off_the_Unit.html` | 5 | 5 |
| `LAUNCH_ASDAN/PEQ/START_HERE.html` | 12 | 1 |
| `LAUNCH_ASDAN/Resources_and_Tools.html` | 11 | 0 |
| `LAUNCH_ASDAN/Scheme_of_Work.html` | 12 | 1 |
| `LAUNCH_ASDAN/Vocational/START_HERE.html` | 12 | 0 |
| `_passph1/C7_FINDING.md` | 30 | 0 |
| `_passph1/CENSUS.md` | 1457 | 0 |
| `_passph1/EXECUTOR_FAILURE.md` | 41 | 0 |
| `_passph1/G2_HARNESS.cjs` | 109 | 0 |
| `_passph1/G2_HARNESS_PROOF.md` | 48 | 0 |
| `_passph1/G4_DETECTOR_FINDING.md` | 132 | 0 |
| `_passph1/G4_MUTATION_PROOF.md` | 16 | 0 |
| `_passph1/G4_WITNESS_COMPARATOR.py` | 107 | 0 |
| `_passph1/L1_DEMAND_REPORT.md` | 10 | 0 |
| `_passph1/P1_P7_DRY_RUN_RESULT.md` | 89 | 0 |
| `_passph1/P7_NOT_DEPLOYED.md` | 13 | 0 |
| `_passph1/SCOPE_GUARD_PROOF.md` | 18 | 0 |
| `_passph1/SIGNOFF_CLASSIFICATION.md` | 142 | 0 |
| `_passph1/TEST_COPY_DIVERGENCE.md` | 503 | 0 |
| `build_asdan.html` | 12 | 1 |
| `build_dt_upcycling.html` | 3 | 1 |

## AWAITING-WORD — one-line questions

- Should the live GROW Level 2 registration claim be corrected in a separately authorised P8?
- Which, if any, of the 80 B2 pupil-action or real-world sign-off occurrences should change?
- Should the 2 W6 witness-section sign-off occurrences be changed in a later pass that intentionally establishes a new G4 baseline?
- Should `PEQ_W6_…_Sign_Off_the_Unit.html` be renamed later with a redirect plan?
- What should happen to the materially divergent `*_Estate_v3` TEST COPY estates on main?
- Are the LAUNCH Vocational banked titles affected by the planned ASDAN Vocational Taster withdrawal?
- Is any learner evidence still held in the ASDAN e-portfolio that needs exporting?

## Rollback

`git checkout pass-ph1-peq-hardening && git revert --no-commit ae1d3c7af2526781aad6fb82e7cbbf6b87ded380..HEAD && git commit -m "Rollback PH-1" && git push origin pass-ph1-peq-hardening`
