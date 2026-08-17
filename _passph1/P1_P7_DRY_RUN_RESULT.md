# PH-1 P1–P7 dry-run result

- Input branch commit: `f060fb9cbab8c1dd16796aaae73bc4828fd90b94`
- Runtime executor SHA-256: `20973939a9527769ba02c19bf1e2e7d529c809f4317b4e493b7ca5912dac823a`
- Exit code: **0**
- Result: **PASS**

## Simulated commits

- **P1:** `c19ce4a52cdfc30606e7957a4895733a495ef86d`
- **P2:** `49242e26cc025fe5b8a550f472d610022813b013`
- **P3:** `b38f7a5fb075815c9554ba91ce4b212266278005`
- **P4:** `6eeb213b27e7eb107f48b3438b5f5bd961108770`
- **P5:** `32f1c78df816966d0c2c5ac8407dba1b100e8c4d`
- **P6:** `9cdc09b0d280cdcdd9c7ab3703722b5c3aae6271`
- **P7:** `579af857c5ec5d6a1365818ff98aae9f5a7a9969`

- Simulated tip: `579af857c5ec5d6a1365818ff98aae9f5a7a9969`
- Changed files: **27**
- Witness comparator: **PASS** — BASE 145 / simulated tip 145
- Print-section and reduced-motion invariants: **PASS**
- Tracked ASDAN PDFs: **0**
- Runtime localStorage additions: **False**
- P8 authorised: **False**

## Changed files

- `BUILD_ASDAN/BUILD_ASDAN_Hub.html`
- `BUILD_ASDAN/Careers/CAREERS_W6_My_Career_Profile.html`
- `BUILD_ASDAN/Careers/START_HERE.html`
- `BUILD_ASDAN/Community_Project/COMM_W6_The_Handover_and_Its_Benefit.html`
- `BUILD_ASDAN/Community_Project/START_HERE.html`
- `BUILD_ASDAN/Duke_and_Enterprise/DUKE_W6_Pitch_and_Reflect.html`
- `BUILD_ASDAN/Duke_and_Enterprise/START_HERE.html`
- `BUILD_ASDAN/FoodWise/FW_W5_Prepare_a_Healthy_Snack.html`
- `BUILD_ASDAN/FoodWise/FW_W6_Plan_a_Healthy_Meal.html`
- `BUILD_ASDAN/FoodWise/START_HERE.html`
- `BUILD_ASDAN/Living_Independently/LI_W6_Shopping_and_Change.html`
- `BUILD_ASDAN/Living_Independently/START_HERE.html`
- `Build/Slideshows/BUILD_DT_W6_Handover.html`
- `GROW_ASDAN/GROW_ASDAN_Hub.html`
- `GROW_ASDAN/Scheme_and_Resources.html`
- `LAUNCH_ASDAN/LAUNCH_ASDAN_Hub.html`
- `LAUNCH_ASDAN/PEQ/PEQ_W4_Plan_a_Communication_Activity.html`
- `LAUNCH_ASDAN/PEQ/PEQ_W5_Deliver_the_Activity_and_Gather_Evidence.html`
- `LAUNCH_ASDAN/PEQ/PEQ_W6_Review_Progress_and_Sign_Off_the_Unit.html`
- `LAUNCH_ASDAN/PEQ/START_HERE.html`
- `LAUNCH_ASDAN/Resources_and_Tools.html`
- `LAUNCH_ASDAN/Scheme_of_Work.html`
- `LAUNCH_ASDAN/Vocational/START_HERE.html`
- `_passph1/L1_DEMAND_REPORT.md`
- `_passph1/P7_NOT_DEPLOYED.md`
- `build_asdan.html`
- `build_dt_upcycling.html`

## Diff stat

```text
 BUILD_ASDAN/BUILD_ASDAN_Hub.html                   | 26 +++++++++++++++++++++-
 .../Careers/CAREERS_W6_My_Career_Profile.html      |  2 +-
 BUILD_ASDAN/Careers/START_HERE.html                | 13 ++++++++++-
 .../COMM_W6_The_Handover_and_Its_Benefit.html      |  2 +-
 BUILD_ASDAN/Community_Project/START_HERE.html      | 13 ++++++++++-
 .../DUKE_W6_Pitch_and_Reflect.html                 |  2 +-
 BUILD_ASDAN/Duke_and_Enterprise/START_HERE.html    | 13 ++++++++++-
 .../FoodWise/FW_W5_Prepare_a_Healthy_Snack.html    |  2 +-
 .../FoodWise/FW_W6_Plan_a_Healthy_Meal.html        |  2 +-
 BUILD_ASDAN/FoodWise/START_HERE.html               | 13 ++++++++++-
 .../LI_W6_Shopping_and_Change.html                 |  2 +-
 BUILD_ASDAN/Living_Independently/START_HERE.html   | 13 ++++++++++-
 Build/Slideshows/BUILD_DT_W6_Handover.html         |  2 +-
 GROW_ASDAN/GROW_ASDAN_Hub.html                     |  2 ++
 GROW_ASDAN/Scheme_and_Resources.html               | 11 +++++++++
 LAUNCH_ASDAN/LAUNCH_ASDAN_Hub.html                 | 13 +++++++++++
 .../PEQ/PEQ_W4_Plan_a_Communication_Activity.html  | 15 ++++++++++++-
 ...5_Deliver_the_Activity_and_Gather_Evidence.html | 15 ++++++++++++-
 ...Q_W6_Review_Progress_and_Sign_Off_the_Unit.html | 10 ++++-----
 LAUNCH_ASDAN/PEQ/START_HERE.html                   | 13 ++++++++++-
 LAUNCH_ASDAN/Resources_and_Tools.html              | 11 +++++++++
 LAUNCH_ASDAN/Scheme_of_Work.html                   | 13 ++++++++++-
 LAUNCH_ASDAN/Vocational/START_HERE.html            | 12 ++++++++++
 _passph1/L1_DEMAND_REPORT.md                       | 10 +++++++++
 _passph1/P7_NOT_DEPLOYED.md                        | 13 +++++++++++
 build_asdan.html                                   | 13 ++++++++++-
 build_dt_upcycling.html                            |  4 +++-
 27 files changed, 236 insertions(+), 24 deletions(-)
```

- Patch SHA-256: `d62bf07f09eda32ae518b3bb152eb358b463ffd64b864cc031140213e4cc2ea3`
