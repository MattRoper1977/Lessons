# PROPOSED — the AQA UAS claim qualifier

**Pass PEQ-YEAR-2 §3. PROPOSED DIFFS, NOT APPLIED.** Emitted under the estate's own
claim-accuracy-only discipline, the same route `PROPOSED_asdan_claim_accuracy_residuals.md`
and OPEN_ITEMS item 17(b) used for this exact class of change.

## Why these are proposed rather than applied

Two standing rulings, both Matt's, reach this material and neither is this pass's to set aside:

1. **`_close/OPEN_ITEMS.md` item 17** — *"Until that sitting all 25 sheets stay
   byte-pristine."* The 25 Science Teesside witness sheets carry the sharpest instances
   of this defect and **cannot be edited at all** until the restore sitting.
2. **The same row** — *"Pupil-facing authoring stays Matt's."* Every string below sits in
   a pupil-facing lesson strip. Rewording them is authoring.

So this pass did the part that is unambiguously record-keeping — Q-003 and the three
registers now carry the canonical wording and a re-measured count — and leaves the
pupil-facing half here, ready to apply as one sweep on Matt's word.

## The canonical wording (now in `QUALIFICATION_CLAIMS_REGISTRY.json` Q-003)

> Every AQA UAS unit code and unit title on any estate surface is an **unverified centre
> record awaiting confirmation** from the UAS coordinator's entry record. It is not a
> compliance claim, and no surface may present it as one. Registration and unit entry
> being settled does **not** confirm a code.

## The two transforms

Both are additive, leave the ASDAN short-course module half untouched (it is **HELD**),
and change no other byte:

| # | where | before | after |
|---|---|---|---|
| **T1** | a UAS **unit title** is quoted | `AQA UAS ‘Personal challenge’` | `AQA UAS ‘Personal challenge’ (unit unconfirmed — centre record)` |
| **T2** | a bare UAS family reference | `; AQA UAS` | `; AQA UAS (unit unconfirmed)` |

## Scope: 185 occurrences across 44 files, 88 distinct strings

The compound case matters and is why this is not a blind find-and-replace:
`Banks: ASDAN LI M8 / AQA UAS` — the `ASDAN LI M8` half is a short-course module code and
**stays HELD**; only the `AQA UAS` half takes the qualifier.

### Unit titles asserted with no qualifier (T1) — the sharpest cases

12 distinct unit titles, 108 occurrences. Each names a specific
AQA UAS unit as though it were settled, when the entered code has never been read from the
coordinator's entry record.

| occ | files | asserted title |
|---:|---:|---|
| 56 | 8 | `AQA UAS ‘Personal challenge’` |
| 8 | 3 | `AQA UAS ‘Contributing to the community’` |
| 8 | 3 | `AQA UAS ‘Active citizen’` |
| 4 | 2 | `AQA UAS ‘Personal skills’` |
| 4 | 2 | `AQA UAS ‘Personal organisation’` |
| 4 | 2 | `AQA UAS ‘Health and safety at home’` |
| 4 | 2 | `AQA UAS ‘Household tasks’` |
| 4 | 2 | `AQA UAS ‘Keeping a room clean’` |
| 4 | 2 | `AQA UAS ‘Managing personal information’` |
| 4 | 2 | `AQA UAS ‘Planning a meal’` |
| 4 | 2 | `AQA UAS ‘Enterprise skills’` |
| 4 | 2 | `AQA UAS ‘Working in a team’` |

### Every affected file

**BUILD_ASDAN/** — 14 files
- `BUILD_ASDAN/Careers/CAREERS_W1_My_Strengths.html`
- `BUILD_ASDAN/Careers/CAREERS_W2_Jobs_in_My_Community.html`
- `BUILD_ASDAN/Careers/CAREERS_W3_Skills_Employers_Want.html`
- `BUILD_ASDAN/Careers/CAREERS_W4_Routines_and_Reliability.html`
- `BUILD_ASDAN/Careers/CAREERS_W5_Applying_Myself.html`
- `BUILD_ASDAN/Careers/CAREERS_W6_My_Career_Profile.html`
- `BUILD_ASDAN/Careers/CAREERS_W7_After_Year_11.html`
- `BUILD_ASDAN/Duke_and_Enterprise/DUKE_W1_Choose_My_Challenges.html`
- `BUILD_ASDAN/Duke_and_Enterprise/DUKE_W2_A_Kindness_Challenge.html`
- `BUILD_ASDAN/Duke_and_Enterprise/DUKE_W3_An_Eco_Challenge.html`
- `BUILD_ASDAN/Duke_and_Enterprise/DUKE_W4_An_Independence_Challenge.html`
- `BUILD_ASDAN/Duke_and_Enterprise/DUKE_W5_Our_Social_Enterprise.html`
- `BUILD_ASDAN/Duke_and_Enterprise/DUKE_W6_Pitch_and_Reflect.html`
- `BUILD_ASDAN/Scheme_of_Work.html`

**GROW_ASDAN/** — 6 files
- `GROW_ASDAN/Enterprise/ENT_W1_Helps_And_Earns.html`
- `GROW_ASDAN/Enterprise/ENT_W2_Spot_The_Gap.html`
- `GROW_ASDAN/Enterprise/ENT_W3_Our_Idea_Our_Users.html`
- `GROW_ASDAN/Enterprise/ENT_W4_Money_In_Money_Out.html`
- `GROW_ASDAN/Enterprise/ENT_W5_Brand_And_Pitch.html`
- `GROW_ASDAN/Enterprise/ENT_W6_Pitch_Day.html`

**LAUNCH_ASDAN/** — 24 files
- `LAUNCH_ASDAN/Careers/CAREERS_W1_Know_Myself_for_Work.html`
- `LAUNCH_ASDAN/Careers/CAREERS_W2_The_World_of_Work_and_Its_Sectors.html`
- `LAUNCH_ASDAN/Careers/CAREERS_W3_Labour-Market_Information_and_Pathways.html`
- `LAUNCH_ASDAN/Careers/CAREERS_W4_Meeting_an_Employer.html`
- `LAUNCH_ASDAN/Careers/CAREERS_W5_Matching_My_Profile_to_Opportunities.html`
- `LAUNCH_ASDAN/Careers/CAREERS_W6_Setting_SMART_Careers_Targets.html`
- `LAUNCH_ASDAN/Community_Enterprise/COMM_W1_Identify_a_Community_Need.html`
- `LAUNCH_ASDAN/Community_Enterprise/COMM_W2_Plan_a_Social-Action_or_Enterprise_Project.html`
- `LAUNCH_ASDAN/Community_Enterprise/COMM_W3_Agree_Roles_Aims_and_Timeline.html`
- `LAUNCH_ASDAN/Community_Enterprise/COMM_W4_Partner_with_a_Local_Group_or_Charity.html`
- `LAUNCH_ASDAN/Community_Enterprise/COMM_W5_Begin_Delivering_the_Project.html`
- `LAUNCH_ASDAN/Community_Enterprise/COMM_W6_Promote_Our_Project.html`
- `LAUNCH_ASDAN/Living_Independently/LI_W1_Self-Care_Routines_and_Organisation.html`
- `LAUNCH_ASDAN/Living_Independently/LI_W2_Home_Safety_and_Hazard_Awareness.html`
- `LAUNCH_ASDAN/Living_Independently/LI_W3_Laundry_and_Household_Maintenance.html`
- `LAUNCH_ASDAN/Living_Independently/LI_W4_Keeping_a_Clean_Safe_Living_Space.html`
- `LAUNCH_ASDAN/Living_Independently/LI_W5_Personal_Admin_and_Responsibilities.html`
- `LAUNCH_ASDAN/Living_Independently/LI_W6_Plan_and_Shop_for_a_Balanced_Meal.html`
- `LAUNCH_ASDAN/Vocational/VOC_W1_Introduction_to_Vocational_Skills_and_Workplaces.html`
- `LAUNCH_ASDAN/Vocational/VOC_W2_Health_Safety_and_Hygiene_at_Work.html`
- `LAUNCH_ASDAN/Vocational/VOC_W3_Following_Instructions_and_Routines.html`
- `LAUNCH_ASDAN/Vocational/VOC_W4_Teamwork_in_a_Vocational_Setting.html`
- `LAUNCH_ASDAN/Vocational/VOC_W5_Tools_Equipment_and_Safe_Use.html`
- `LAUNCH_ASDAN/Vocational/VOC_W6_Complete_a_Supported_Vocational_Task.html`

### Distinct strings, with occurrence and file counts

| occ | files | string |
|---:|---:|---|
| 28 | 7 | `Banks: ASDAN LI M8 / AQA UAS` |
| 12 | 3 | `Banks: AQA UAS 'Personal challenge'` |
| 7 | 1 | `Banks: ASDAN LI M8 / AQA UAS.` |
| 4 | 1 | `Banks: AQA UAS 'Personal challenge' — term complete` |
| 4 | 1 | `Banks: AQA UAS 'Personal challenge' · SMSC Kindness` |
| 4 | 1 | `Banks: AQA UAS 'Personal challenge' · links Humanities/D&amp;T` |
| 4 | 1 | `Banks: AQA UAS enterprise · links FS Maths (real calcu` |
| 4 | 1 | `Banks: AQA UAS enterprise · ASDAN PEQ core-skills evid` |
| 4 | 1 | `Banks: AQA UAS enterprise · ASDAN PEQ communication +` |
| 4 | 1 | `Banks: AQA UAS enterprise · links FS English (speaking` |
| 4 | 1 | `Banks: AQA UAS enterprise · ASDAN PEQ Team working (Tm` |
| 4 | 1 | `Banks: AQA UAS enterprise · links FS English (survey q` |
| 3 | 1 | `Banks: AQA UAS &#x27;Personal challenge&#x27;.` |
| 2 | 1 | `Banks: ASDAN Careers world of work; AQA UAS` |
| 2 | 1 | `Banks: ASDAN Careers LMI; AQA UAS` |
| 2 | 1 | `Banks: ASDAN Careers matching; AQA UAS` |
| 2 | 1 | `Banks: ASDAN Careers SMART targets; AQA UAS` |
| 2 | 1 | `Banks: ASDAN Careers self-audit; AQA UAS` |
| 2 | 1 | `Banks: ASDAN Careers employer encounter; AQA UAS` |
| 2 | 1 | `Banks: ASDAN Living Independently plan a meal; AQA UAS` |
| 2 | 1 | `Banks: ASDAN Living Independently home safety; AQA UAS` |
| 2 | 1 | `Banks: ASDAN Living Independently clean space; AQA UAS` |
| 2 | 1 | `Banks: ASDAN Living Independently routines; AQA UAS` |
| 2 | 1 | `Banks: ASDAN Living Independently personal admin; AQA UAS` |
| 2 | 1 | `Banks: ASDAN Living Independently laundry; AQA UAS` |
| 2 | 1 | `Banks: ASDAN Community plan a project; AQA UAS` |
| 2 | 1 | `Banks: ASDAN Community promote; AQA UAS` |
| 2 | 1 | `Banks: ASDAN Community partnership; AQA UAS` |
| 2 | 1 | `Banks: ASDAN Community identify a need; AQA UAS` |
| 2 | 1 | `Banks: ASDAN Community begin delivery; AQA UAS` |
| 2 | 1 | `Banks: ASDAN Community roles and timeline; AQA UAS` |
| 2 | 1 | `Banks: ASDAN Hospitality / Gardening H&amp;S; AQA UAS` |
| 2 | 1 | `Banks: ASDAN Hospitality / Gardening instructions; AQA UAS` |
| 2 | 1 | `Banks: ASDAN Hospitality / Gardening tools; AQA UAS` |
| 2 | 1 | `Banks: ASDAN Hospitality / Gardening complete a task; AQA UAS` |
| 2 | 1 | `Banks: ASDAN Hospitality / Gardening teamwork; AQA UAS` |
| 2 | 1 | `Banks: ASDAN Hospitality / Gardening intro; AQA UAS` |
| 1 | 1 | `Banks: AQA UAS &#x27;Personal challenge&#x27; · SMSC Kindness.` |
| 1 | 1 | `Banks: AQA UAS &#x27;Personal challenge&#x27; · links Humanities/D&amp;T.` |
| 1 | 1 | `Banks: AQA UAS &#x27;Personal challenge&#x27; — term complete.` |
| 1 | 1 | `Banks: ASDAN Careers &amp; Experiencing Work — world of work; AQA UAS` |
| 1 | 1 | `Banks: ASDAN Careers &amp; Experiencing Work — world of work; AQA UAS.` |
| 1 | 1 | `Banks: ASDAN Careers &amp; Experiencing Work — labour-market information; AQA UAS` |
| 1 | 1 | `Banks: ASDAN Careers &amp; Experiencing Work — labour-market information; AQA UAS.` |
| 1 | 1 | `Banks: ASDAN Careers &amp; Experiencing Work — matching to opportunities; AQA UAS` |
| 1 | 1 | `Banks: ASDAN Careers &amp; Experiencing Work — matching to opportunities; AQA UAS.` |
| 1 | 1 | `Banks: ASDAN Careers &amp; Experiencing Work — SMART careers targets; AQA UAS` |
| 1 | 1 | `Banks: ASDAN Careers &amp; Experiencing Work — SMART careers targets; AQA UAS.` |
| 1 | 1 | `Banks: ASDAN Careers &amp; Experiencing Work — self-audit; AQA UAS ‘Personal skills’` |
| 1 | 1 | `Banks: ASDAN Careers &amp; Experiencing Work — self-audit; AQA UAS.` |
| 1 | 1 | `Banks: ASDAN Careers &amp; Experiencing Work — employer encounter; AQA UAS` |
| 1 | 1 | `Banks: ASDAN Careers &amp; Experiencing Work — employer encounter; AQA UAS.` |
| 1 | 1 | `Banks: ASDAN Living Independently — plan and shop for a meal; AQA UAS ‘Planning a meal’ (links Maths)` |
| 1 | 1 | `Banks: ASDAN Living Independently — plan and shop for a meal; AQA UAS.` |
| 1 | 1 | `Banks: ASDAN Living Independently — home safety; AQA UAS ‘Health and safety at home’` |
| 1 | 1 | `Banks: ASDAN Living Independently — home safety; AQA UAS.` |
| 1 | 1 | `Banks: ASDAN Living Independently — clean and safe space; AQA UAS ‘Keeping a room clean’` |
| 1 | 1 | `Banks: ASDAN Living Independently — clean and safe space; AQA UAS.` |
| 1 | 1 | `Banks: ASDAN Living Independently — self-care and routines; AQA UAS ‘Personal organisation’` |
| 1 | 1 | `Banks: ASDAN Living Independently — self-care and routines; AQA UAS.` |
| 1 | 1 | `Banks: ASDAN Living Independently — personal admin; AQA UAS ‘Managing personal information’` |
| 1 | 1 | `Banks: ASDAN Living Independently — personal admin; AQA UAS.` |
| 1 | 1 | `Banks: ASDAN Living Independently — laundry and maintenance; AQA UAS ‘Household tasks’` |
| 1 | 1 | `Banks: ASDAN Living Independently — laundry and maintenance; AQA UAS.` |
| 1 | 1 | `Banks: ASDAN Community / Active Citizenship — plan a project; AQA UAS ‘Enterprise skills’` |
| 1 | 1 | `Banks: ASDAN Community / Active Citizenship — plan a project; AQA UAS.` |
| 1 | 1 | `Banks: ASDAN Community / Active Citizenship — promote the project; AQA UAS ‘Active citizen’` |
| 1 | 1 | `Banks: ASDAN Community / Active Citizenship — promote the project; AQA UAS.` |
| 1 | 1 | `Banks: ASDAN Community / Active Citizenship — partnership; AQA UAS ‘Contributing to the community’` |
| 1 | 1 | `Banks: ASDAN Community / Active Citizenship — partnership; AQA UAS.` |
| 1 | 1 | `Banks: ASDAN Community / Active Citizenship — identify a need; AQA UAS ‘Contributing to the community’` |
| 1 | 1 | `Banks: ASDAN Community / Active Citizenship — identify a need; AQA UAS.` |
| 1 | 1 | `Banks: ASDAN Community / Active Citizenship — begin delivery; AQA UAS ‘Active citizen’` |
| 1 | 1 | `Banks: ASDAN Community / Active Citizenship — begin delivery; AQA UAS.` |
| 1 | 1 | `Banks: ASDAN Community / Active Citizenship — roles and timeline; AQA UAS ‘Working in a team’` |
| 1 | 1 | `Banks: ASDAN Community / Active Citizenship — roles and timeline; AQA UAS.` |
| 1 | 1 | `Banks: ASDAN Hospitality / Gardening — health, safety and hygiene at work; AQA UAS` |
| 1 | 1 | `Banks: ASDAN Hospitality / Gardening — health, safety and hygiene; AQA UAS.` |
| 1 | 1 | `Banks: ASDAN Hospitality / Gardening — following instructions and routines; AQA UAS` |
| 1 | 1 | `Banks: ASDAN Hospitality / Gardening — following instructions; AQA UAS.` |
| 1 | 1 | `Banks: ASDAN Hospitality / Gardening — tools and equipment, safe use; AQA UAS` |
| 1 | 1 | `Banks: ASDAN Hospitality / Gardening — tools and equipment; AQA UAS.` |
| 1 | 1 | `Banks: ASDAN Hospitality / Gardening — complete a supported vocational task; AQA UAS occupational units` |
| 1 | 1 | `Banks: ASDAN Hospitality / Gardening — complete a supported task; AQA UAS.` |
| 1 | 1 | `Banks: ASDAN Hospitality / Gardening — teamwork in a vocational setting; AQA UAS` |
| 1 | 1 | `Banks: ASDAN Hospitality / Gardening — teamwork; AQA UAS.` |
| 1 | 1 | `Banks: ASDAN Hospitality / Gardening — vocational skills introduction; AQA UAS occupational units` |
| 1 | 1 | `Banks: ASDAN Hospitality / Gardening — vocational skills introduction; AQA UAS.` |

## Not in this proposal

- The **63 `Science_Teesside/` surfaces** carrying `TBC (Cheryl)` — 25 held byte-pristine,
  38 variants outside that set. Reported against item 17; not edited, because correcting
  the variants while the sheets they mirror are frozen would diverge the two halves mid-hold.
- The **ASDAN short-course module and challenge codes** (FoodWise / Living Independently /
  Duke). Explicitly **HELD** by this pass's own brief.
- The **source SoW workbooks** and the `_pass*` / `_close` audit trees — records of what was,
  not live claims.
