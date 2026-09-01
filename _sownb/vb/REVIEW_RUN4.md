# REVIEW — Order VB run 4

Phone-shaped, easiest first. Nothing was authored and no lesson prose changed. Two tools were built, one ledger entry was corrected, twelve surfaces were verified, and the calendar work for Phase 2 was mapped.

## Wave B2 — all 12 VERIFIED, nothing to fix
BUILD ASDAN W16 + two front doors · GROW ASDAN W15, W16 + front door · LAUNCH ASDAN W16 + front door · BUILD Science W16A, W16B · GROW Science W16A · GROW Humanities front-door variant.
Full battery green, every red control fired, all four engine controls green. Cohort B is now completely verified: 36 of 36 surfaces.

## The instrument fix (the important bit)
Run 3 found that g18 judged every family against a single word floor of 1,638 computed from the GROW Science pack, though it described itself as family-relative. That is now fixed.

**g18 v2** uses each family's own live neighbours. The effect is not uniformly softer — it is simply correct:
- BUILD Science's floor *rises* to 1,767 (its lessons genuinely run longer)
- LAUNCH Humanities' floor *falls* to 897 (its lessons genuinely run shorter)

Re-scoring all 25 previously-verified lessons: **one flip**, and it is the one run 3 predicted. BUILD Humanities W14 goes RED → PASS. No lesson turned red. No file was touched.

While building it I found the neighbour sets were pulling in three BUILD ASDAN teacher-planning and portfolio pages that contain no pupil slides at all; they were dragging that family's floor down. v2.1 counts lesson decks only.

## The new instrument, and what it found
The battery could say a lesson was too short and could never say one was too long for the period. **g23** now measures that. It is report-only — it blocks nothing and licenses no cut.

**Six lessons are OVERLOADED**, and they cluster — every one is a FEB Spring 1 ASDAN or Humanities W15 lesson:

| lesson | words | family median | ratio | reading time |
|---|---|---|---|---|
| LAUNCH Humanities W15 | 3,460 | 924 | ×3.75 | ~38 of 40 min |
| GROW Humanities W15 | 3,463 | 1,104 | ×3.14 | ~38 of 40 min |
| GROW ASDAN W16 | 2,897 | 954 | ×3.04 | ~32 of 40 min |
| GROW ASDAN W15 | 2,881 | 954 | ×3.02 | ~32 of 40 min |
| BUILD ASDAN W16 | 2,927 | 1,082 | ×2.70 | ~33 of 40 min |
| BUILD ASDAN W15 | 2,886 | 1,082 | ×2.67 | ~32 of 40 min |

At the assumed reading rate the two Humanities lessons need 96% of the period for reading alone, before any activity. **The rate is an assumption, not a measurement** — no reading rate exists anywhere in the repo, so 90 wpm was chosen and stated, with a 60–120 band reported so nothing hangs on the exact figure.

Each has two options, both of which are authoring and therefore yours: split across two periods, or trim into the family band. The word deltas are in the state file. I have not touched them.

## For Phase 2 — the calendar
**Two real double-bookings**, where two different lessons claim the same family's same absolute week:

1. **LAUNCH Science week 14** — six lessons, two sequences. `Autumn2_W7/SCI_L_A2_W7L1–L3` (declares week 14, workbook cell C45, "Topics 2–3 assessment") and `W14-W15/SCI_L_W14L1–L3` (cell C44, "Research a genetic condition"). Different cells, same week. Either the SoW wants both and the week is over-filled, or one is misplaced.
2. **BUILD Humanities week 14** — `BUILD_HUM_W14_Festivals_Display_and_Reflection` (week 14, cell C59) against `BUILD_HUM_W14_Industry_and_Nature_The_Tees_Story` in the older pack.

**Three label-only collisions**, which are the week-numbering dialect problem, not double-bookings: GROW Science W7 (absolute 7 vs 14) and GROW ASDAN W1–W6 (absolute 1–6 vs 8–13) reuse week numbers across terms. Worth naming so nobody "fixes" them by mistake.

**One real gap**: GROW Science has no week 14 lesson at all. BUILD ASDAN's main strand is empty from week 7 to week 14, though its five sub-strands cover weeks 1–6.

The three disputed timetable cells do not decide any of these. They are Behaviour Intervention versus DT — neither is an in-scope subject — so they change how many teachable slots each lane has, not which lesson wins a week. They stay UNRESOLVED.

## What still cannot be measured
Public 200 body-hash binding is now marked **VENUE_BLOCKED** permanently: this venue's proxy refuses github.io, and three runs have confirmed it. It is never counted as a pass. The binding substitute — every verified file byte-equal to what is on main — held 12 of 12 this run.
