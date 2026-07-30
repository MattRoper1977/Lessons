# FIN-1 §3.1 — Estate Render Sweep: Report-Only Failure List

Swept **459** tracked *.html headless (Chromium, http://). `/hud.js`+favicon stubbed
(they resolve at the domain root in production). A 'failure' = any console/script/page error
or non-benign network failure.

- **Total files flagged:** 84
- **Network-independent code defects that break ONLINE:** 0
- **Humanities lesson failures (the reported-bug family):** 0
- All flags are blocked EXTERNAL hosts (load on the live site) or absolute-root shared assets.

## A. Functional breakers OFFLINE (JS/CSS libraries — degrade behaviour without network)

**cdn.jsdelivr.net** — 8 file(s):
  - `5_6 Local Choice/Opening_Night.html`
  - `5_6 Local Choice/The_Foxglove_Case.html`
  - `5_6 Local Choice/Trekkers_Trail_Runner (2).html`
  - `Games/Orbital_source.html`
  - `Games/Slipstream_GP.html`
  - `Games/Trail_Runner.html`
  - `Games/Trekkers_Trail_Runner_Tees_Coast.html`
  - `Games/Wrecking_Crew.html`

**cdn.tailwindcss.com** — 2 file(s):
  - `5_6 Local Choice/Opening_Night.html`
  - `5_6 Local Choice/The_Foxglove_Case.html`

**cdnjs.cloudflare.com** — 1 file(s):
  - `Games/Neon_Snake_Overdrive.html`

## B. Cosmetic offline (fonts fall back; thumbnails show broken-image; video links still work online)
- **fonts.googleapis.com** — 75 file(s)
- **i.ytimg.com** — 52 file(s)
- **www.youtube-nocookie.com** — 1 file(s)

## C. Absolute-root shared assets (resolve at domain root in production — NOT defects)
  - `index.html` → `/theme.js` (served by user-page repo root, same as `/hud.js`)
  - `primary/index.html` → `/theme.js` (served by user-page repo root, same as `/hud.js`)

## Full flagged-file list (all 84)
- `2 Physics 10/Consolidation_Electricity_Review-1.html` — i.ytimg.com
- `2 Physics 10/current_rush.html` — fonts.googleapis.com
- `5_6 Local Choice/Opening_Night.html` — cdn.jsdelivr.net, cdn.tailwindcss.com, fonts.googleapis.com
- `5_6 Local Choice/Rivers/L1a_Tees_Source_to_Sea.html` — i.ytimg.com
- `5_6 Local Choice/Rivers/L1b_Your_River_Your_Home.html` — i.ytimg.com
- `5_6 Local Choice/Rivers/L1c_Reading_the_River.html` — i.ytimg.com
- `5_6 Local Choice/The_Foxglove_Case.html` — cdn.jsdelivr.net, cdn.tailwindcss.com, fonts.googleapis.com
- `5_6 Local Choice/Trekkers_Trail_Runner (2).html` — cdn.jsdelivr.net, fonts.googleapis.com
- `6 Art/Art_Exquisite_Corpse_STAGE_COUNTDOWNS_FINAL.html` — i.ytimg.com, www.youtube-nocookie.com
- `Games/Globe_Snake (1).html` — fonts.googleapis.com
- `Games/Grapple.html` — fonts.googleapis.com
- `Games/Grid_Chase.html` — fonts.googleapis.com
- `Games/Marble.html` — fonts.googleapis.com
- `Games/Neon_Garden.html` — fonts.googleapis.com
- `Games/Neon_Siege.html` — fonts.googleapis.com
- `Games/Neon_Snake_Overdrive.html` — cdnjs.cloudflare.com [CODE: THREE not defined]
- `Games/Orbital.html` — fonts.googleapis.com
- `Games/Orbital_source.html` — cdn.jsdelivr.net, fonts.googleapis.com
- `Games/Prism.html` — fonts.googleapis.com
- `Games/Slipstream.html` — fonts.googleapis.com
- `Games/Slipstream_GP.html` — cdn.jsdelivr.net, fonts.googleapis.com
- `Games/Static.html` — fonts.googleapis.com
- `Games/Trail_Runner.html` — cdn.jsdelivr.net, fonts.googleapis.com
- `Games/Trekkers_Trail_Runner_Tees_Coast.html` — cdn.jsdelivr.net, fonts.googleapis.com
- `Games/Vortex.html` — fonts.googleapis.com
- `Games/Wrecking_Crew.html` — cdn.jsdelivr.net, fonts.googleapis.com
- `Tutor_Time/Week2_Fri_Values_MutualRespect_Respectful.html` — fonts.googleapis.com
- `Tutor_Time/Wk3_KCSIE_TRAP_Sextortion.html` — fonts.googleapis.com
- `chemistry/Lesson4a_Gas_Tests_H2_O2_CO2 (1).html` — i.ytimg.com
- `chemistry/Lesson4b_Gas_Tests_NH3_Cl2.html` — i.ytimg.com
- `index.html` — 127.0.0.1:8140
- `primary/index.html` — 127.0.0.1:8140, fonts.googleapis.com
- `primary/year4/science/autumn/group-classify-living-things/Lesson1_GroupAnimals.html` — fonts.googleapis.com, i.ytimg.com
- `primary/year4/science/autumn/group-classify-living-things/Lesson2_VertebratesInvertebrates.html` — fonts.googleapis.com, i.ytimg.com
- `primary/year4/science/autumn/group-classify-living-things/Lesson3_ClassificationKeysAnimals.html` — fonts.googleapis.com, i.ytimg.com
- `primary/year4/science/autumn/group-classify-living-things/Lesson4_GroupPlants.html` — fonts.googleapis.com, i.ytimg.com
- `primary/year4/science/autumn/group-classify-living-things/Lesson5_ClassificationKeysPlants.html` — fonts.googleapis.com, i.ytimg.com
- `primary/year4/science/autumn/group-classify-living-things/index.html` — fonts.googleapis.com
- `primary/year4/science/autumn/states-of-matter/Lesson10_EvaluateEvaporation.html` — fonts.googleapis.com, i.ytimg.com
- `primary/year4/science/autumn/states-of-matter/Lesson1_ExploreStates.html` — fonts.googleapis.com, i.ytimg.com
- `primary/year4/science/autumn/states-of-matter/Lesson2_ThinkDifferently.html` — fonts.googleapis.com, i.ytimg.com
- `primary/year4/science/autumn/states-of-matter/Lesson3_ChangeStates.html` — fonts.googleapis.com, i.ytimg.com
- `primary/year4/science/autumn/states-of-matter/Lesson4_UseEquipment.html` — fonts.googleapis.com, i.ytimg.com
- `primary/year4/science/autumn/states-of-matter/Lesson5_PlanMelting.html` — fonts.googleapis.com, i.ytimg.com
- `primary/year4/science/autumn/states-of-matter/Lesson6_InvestigateMelting.html` — fonts.googleapis.com, i.ytimg.com
- `primary/year4/science/autumn/states-of-matter/Lesson7_WaterCycle.html` — fonts.googleapis.com, i.ytimg.com
- `primary/year4/science/autumn/states-of-matter/Lesson8_PlanEvaporation.html` — fonts.googleapis.com, i.ytimg.com
- `primary/year4/science/autumn/states-of-matter/Lesson9_InvestigateEvaporation.html` — fonts.googleapis.com, i.ytimg.com
- `primary/year4/science/autumn/states-of-matter/index.html` — fonts.googleapis.com
- `primary/year5/science/autumn/forces/Lesson1_Friction.html` — fonts.googleapis.com, i.ytimg.com
- `primary/year5/science/autumn/forces/Lesson2_AirResistance.html` — fonts.googleapis.com, i.ytimg.com
- `primary/year5/science/autumn/forces/Lesson3_PlanParachute.html` — fonts.googleapis.com, i.ytimg.com
- `primary/year5/science/autumn/forces/Lesson4_InvestigateParachute.html` — fonts.googleapis.com, i.ytimg.com
- `primary/year5/science/autumn/forces/Lesson5_EvaluateParachute.html` — fonts.googleapis.com, i.ytimg.com
- `primary/year5/science/autumn/forces/Lesson6_PlanWaterResistance.html` — fonts.googleapis.com, i.ytimg.com
- `primary/year5/science/autumn/forces/Lesson7_InvestigateWaterResistance.html` — fonts.googleapis.com, i.ytimg.com
- `primary/year5/science/autumn/forces/Lesson8_ExploreGravity.html` — fonts.googleapis.com, i.ytimg.com
- `primary/year5/science/autumn/forces/Lesson9_SmallForcesGreaterEffects.html` — fonts.googleapis.com, i.ytimg.com
- `primary/year5/science/autumn/forces/index.html` — fonts.googleapis.com
- `primary/year5/science/autumn/space/Lesson1_TheSolarSystem.html` — fonts.googleapis.com, i.ytimg.com
- `primary/year5/science/autumn/space/Lesson2_ThePlanets.html` — fonts.googleapis.com
- `primary/year5/science/autumn/space/Lesson3_Modelling.html` — fonts.googleapis.com, i.ytimg.com
- `primary/year5/science/autumn/space/Lesson4_MotionOfEarthAndPlanets.html` — fonts.googleapis.com, i.ytimg.com
- `primary/year5/science/autumn/space/Lesson5_IdeasOverTime.html` — fonts.googleapis.com, i.ytimg.com
- `primary/year5/science/autumn/space/Lesson6_PlanetEarth.html` — fonts.googleapis.com, i.ytimg.com
- `primary/year5/science/autumn/space/Lesson7_NightAndDay.html` — fonts.googleapis.com, i.ytimg.com
- `primary/year5/science/autumn/space/Lesson8_TheMoon.html` — fonts.googleapis.com, i.ytimg.com
- `primary/year5/science/autumn/space/index.html` — fonts.googleapis.com
- `primary/year6/science/autumn/living-things/Lesson1_ConditionsForLife.html` — fonts.googleapis.com, i.ytimg.com
- `primary/year6/science/autumn/living-things/Lesson2_GroupOrganisms.html` — fonts.googleapis.com, i.ytimg.com
- `primary/year6/science/autumn/living-things/Lesson3_ClassifyAnimals.html` — fonts.googleapis.com, i.ytimg.com
- `primary/year6/science/autumn/living-things/Lesson4_ClassifyPlants.html` — fonts.googleapis.com, i.ytimg.com
- `primary/year6/science/autumn/living-things/Lesson5_Microorganisms.html` — fonts.googleapis.com, i.ytimg.com
- `primary/year6/science/autumn/living-things/Lesson6_ClassifyMicroorganisms.html` — fonts.googleapis.com, i.ytimg.com
- `primary/year6/science/autumn/living-things/Lesson7_CarlLinnaeus.html` — fonts.googleapis.com, i.ytimg.com
- `primary/year6/science/autumn/living-things/index.html` — fonts.googleapis.com
- `primary/year6/science/autumn/renewable-energy/Lesson1_WhatIsRenewableEnergy.html` — fonts.googleapis.com, i.ytimg.com
- `primary/year6/science/autumn/renewable-energy/Lesson2_FossilFuelsAndEnvironment.html` — fonts.googleapis.com, i.ytimg.com
- `primary/year6/science/autumn/renewable-energy/Lesson3_SolarPower.html` — fonts.googleapis.com, i.ytimg.com
- `primary/year6/science/autumn/renewable-energy/Lesson4_WindPower.html` — fonts.googleapis.com, i.ytimg.com
- `primary/year6/science/autumn/renewable-energy/Lesson5_WeighingItUp.html` — fonts.googleapis.com, i.ytimg.com
- `primary/year6/science/autumn/renewable-energy/Lesson6_RenewableInOurCommunity.html` — fonts.googleapis.com, i.ytimg.com
- `primary/year6/science/autumn/renewable-energy/Lesson7_PlanForOurSchool.html` — fonts.googleapis.com, i.ytimg.com
- `primary/year6/science/autumn/renewable-energy/index.html` — fonts.googleapis.com

---

## D. Art_Teesside/Build — per-file print-pack population (LL-INST-09, requested)
Authoritative print gate (Chromium `media=print`, invokes each file's own `printPack(level)`,
reads back rendered box + `.visible` sections + printed text). All 8 BUILD Art lessons:

| Lesson (Art_Teesside/Build/BUILD_ART_) | supported | standard | stretch | sections on paper |
|---|---|---|---|---|
| W1 The_Local_Canvas | 17/17 ✓ | 17/17 ✓ | 17/17 ✓ | 9 |
| W2 Artists_Makers_and_Teesside_Connections | 17/17 ✓ | 17/17 ✓ | 17/17 ✓ | 9 |
| W3 Industrial_Surface_Skills_Lab | 17/17 ✓ | 17/17 ✓ | 17/17 ✓ | 9 |
| W4 Build_the_Brief | 17/17 ✓ | 17/17 ✓ | 17/17 ✓ | 9 |
| W5 Critique_Test_and_Redirect | 17/17 ✓ | 17/17 ✓ | 17/17 ✓ | 9 |
| W6 Resolve_the_Artwork | 17/17 ✓ | 17/17 ✓ | 17/17 ✓ | 9 |
| W7 Curate_the_Showcase | 17/17 ✓ | 17/17 ✓ | 17/17 ✓ | 9 |
| W8 Share_Reflect_and_Close_the_Loop | 17/17 ✓ | 17/17 ✓ | 17/17 ✓ | 9 |

**PER-TIER GATE: PASS** — every BUILD Art print pack fully populates on paper, all tiers.
Console-error sweep (§3.1): Art_Teesside/Build had **0 failures**. Only absolute-path ref is
`/hud.js` (no other offline-breakers), so these lessons are fully offline-safe.

## E. Art ZIP verdict (MadeByMatt offline pack vs repo blobs)
Rebuilt via the committed pipeline `_passsci1/inputs/build_staff_pack.py` (REPO→/workspace/lessons).
- Each MadeByMatt offline BUILD Art copy differs from its repo blob by **exactly one thing**: removal
  of ` <script defer src="/hud.js"></script>` (−38 bytes). No pupil content, no print section, no
  interactive lost. (hud.js sits on the `</body></html>` line, so `diff` shows it as a 2-line hunk.)
- LL-INST-09 on the offline copies (file://, hud.js stripped): **PASS, 17/17 per tier, 9 sections on
  paper** — identical population to the repo.
- **The transform does NOT eat pack data.** "No fix needed" holds at the builder level FOR THE
  COMMITTED PIPELINE.
- CAVEAT (must be quoted): `build_staff_pack.py`'s own docstring says it is a reconstruction of a
  builder that "was never committed (404 on main)." I proved the AVAILABLE builder is clean; I cannot
  diff against a lost original. If Matt's actual MadeByMatt_Term_1_1 zip predates this reconstruction,
  share the zip (I diff the real artifact) or rebuild from the committed pipeline (clean).
