# REVIEW — run 14 (read this first)

Read on a phone. Plain lines, no tables. Every number below is re-derived from the repo this run.

What landed, in order
  #252  the pre-gate, TERM_DATES.md written once (BOUNDARY=26), FILENAME_DRIFT.md written once (67 rows), R4 and R5 recorded
  #251  g28 cell-existence gate, first and alone (already on main when this run's PRs opened)
  #253  SUBJECT_TERMS.md register and the case patcher, gate change alone
  #254  BUILD ASDAN: six Duke decks, 12 mid-sentence 'Social Enterprise' to house case
  #255  GROW Science: three W9-W10 decks, 11 mid-sentence 'Solar System' to house case
  #256 #257 #258  the next eight reshells by teaching date: BUILD W7-W8, GROW W6-W8, LAUNCH W6-W8 Humanities
  #259  GROW ASDAN week 15, second deck, C157 and C187 only
  #260  wave 4 run 3, GROW Humanities: RE strand weeks 1 and 2 (C60, C61)
  #261  wave 4 run 3, BUILD Humanities: RE strand week 2 (C61)
  #262  wave 4 run 3, GROW ASDAN: Choose my Young Duke challenge (C144)
  #263  wave 4 run 3, LAUNCH Humanities: RE and Ethics strand weeks 1 and 2 (C200, C201)
  #265  GROW ASDAN weeks 1 and 15: the donor lesson-config and running head no longer travel
  #266  the catalogue, last and alone: 682 -> 689

The calendar and the stop line
  Dates are in _sownb/TERM_DATES.md once, with the source line. BOUNDARY=26: Autumn 1 weeks 1-8, Autumn 2 weeks 9-15, Spring 1 weeks 16-21, Spring 2 weeks 22-26. Summer is out of scope.
  CALENDAR_SPINE.json points at it through a six-line termDates block; the spine was not re-serialised.

P0
  Anchor 7243d780; the only commit since was this order's own g28 PR. Chromium unchanged; the font set changed (24 families now, 59 recorded), so the engine-artefact rule applied.
  Control: the four RSH-3 references re-rendered to the run-11 page counts (2/2/10/10) and g21 read the same (three PASS, grow-asdan COLLAPSIBLE). Pagination gates trusted. Corpus freeze 49/54 vs RUN4, five divergent paths all from merged PRs of this order; re-baselined.

R1  g28
  Firing control: C999 RED, a real address PASS. Sweep: the five run-12 modules RED on exactly C171, C172, C138 twice, C89, C198; the run-11 module PASS. GROW ASDAN week 15 corrected to TWO open cells everywhere it said three.

R2  subject terms
  Register grep-derived from the three workbooks: Solar System, Social Enterprise, Religious Education, Religious Studies, Mary Anning (NAMED-AFTER). No Edexcel or IGCSE keyword list exists in the repo; none was invented.
  BUILD ASDAN: 6 decks, 12 occurrences, every diff byte a case change inside the term, containment held.
    BUILD_ASDAN_A2_DUKE_W1_Plan_a_Community_Social_Action_Project.html  before [] -> after []  residue ['One Goal', 'Useful Roles']
    BUILD_ASDAN_A2_DUKE_W2_Decide_Our_Project_Goal_and_Roles.html  before [] -> after []  residue ['Will Change', 'Kindness That']
    BUILD_ASDAN_A2_DUKE_W3_Carry_Out_a_Community_Kindness_Action.html  before [] -> after []  residue ['One Goal', 'Useful Roles', 'Skills Challenge']
    BUILD_ASDAN_A2_DUKE_W4_Complete_a_Creative_Skills_Challenge.html  before [] -> after []  residue ['Kindness That', 'Truth Trail']
    BUILD_ASDAN_A2_DUKE_W5_Gather_and_Present_Project_Evidence.html  before [] -> after []  residue ['Skills Challenge']
    BUILD_ASDAN_A2_DUKE_W6_Celebrate_Community_Impact.html  before [] -> after []  residue ['Truth Trail']
  GROW Science: 3 decks, 11 occurrences, every diff byte a case change inside the term, containment held.
    SCI_G_W10A_Solar_System_Research_Explore.html  before ['Solar System', 'System Research'] -> after ['Solar System', 'System Research']  residue ['Museums Greenwich', 'One Martian', 'Spherical Bodies', 'Mission Briefing']
    SCI_G_W10B_Solar_System_Presentation_Do.html  before ['Solar System', 'System Presentation'] -> after ['Solar System', 'System Presentation']  residue ['Mission Briefing', 'Climate Chain', 'From Gas']
    SCI_G_W9A_Spherical_Bodies_Explore.html  before ['Solar System'] -> after []  residue ['The Sun', 'Hour Control', 'Spherical Bodies']
  Planted-surname control after landing: still RED, register stands.

R3  allowlist
  Frozen at 28 entries; none added this run; redesign NOT TRIGGERED.

R4  Trekkers
  HANDOFF — not measurable in this venue; nothing widened: not Lessons-side in one file. Timeout lines: tools/verify_games_rendered.mjs:65 NAV_MS=30000, :67 JUDGE_MS=20000. hud-coverage.json cites a real verifier for all eight V6 games.

R5  the two rules
  A: Games/Vortex.html:4171 and Games/Prism.html:4066, offline/standalone means zero external elements.
  B: tools/verify_hud_on_lessons_games.mjs:112 and data/hud-coverage.json:9, a game route must carry the HUD script.
  Both are pupil-protecting. STOPPED at this section. RULE_CHOICE=<a|b> is yours, Matt.

R6.1  the eight reshells
  GW6  GROW_HUM_W6_Planning_An_Account.html: 1453 -> 2741 words, containment PASS, g16 v2 105/105 PASS, g10 PASS, g24 2 visuals, g26 PASS, g28 PASS, tiers PASS, 10 pages
  LW6  LAUNCH_HUM_W6_A_Structured_Account_From_Evidence.html: 1225 -> 2420 words, containment PASS, g16 v2 104/104 PASS, g10 PASS, g24 2 visuals, g26 PASS, g28 PASS, tiers PASS, 10 pages
  BW7  BUILD_HUM_W7_Groups_We_Belong_To.html: 2273 -> 4102 words, containment PASS, g16 v2 104/104 PASS, g10 PASS, g24 2 visuals, g26 PASS, g28 PASS, tiers PASS, 10 pages
  GW7  GROW_HUM_W7_Writing_And_Marking_The_Account.html: 1487 -> 2829 words, containment PASS, g16 v2 105/105 PASS, g10 PASS, g24 2 visuals, g26 PASS, g28 PASS, tiers PASS, 10 pages
  LW7  LAUNCH_HUM_W7_Source_Based_Assessment.html: 1226 -> 2354 words, containment PASS, g16 v2 104/104 PASS, g10 PASS, g24 2 visuals, g26 PASS, g28 PASS, tiers PASS, 10 pages
  BW8  BUILD_HUM_W8_A_Festival_Of_Light.html: 2303 -> 4033 words, containment PASS, g16 v2 104/104 PASS, g10 PASS, g24 2 visuals, g26 PASS, g28 PASS, tiers PASS, 10 pages
  GW8  GROW_HUM_W8_Finding_Places_In_An_Atlas.html: 1481 -> 2809 words, containment PASS, g16 v2 105/105 PASS, g10 PASS, g24 2 visuals, g26 PASS, g28 PASS, tiers PASS, 10 pages
  LW8  LAUNCH_HUM_W8_Maps_Symbols_And_Grid_References.html: 1257 -> 2443 words, containment PASS, g16 v2 104/104 PASS, g10 PASS, g24 2 visuals, g26 PASS, g28 PASS, tiers PASS, 10 pages
  g18 v3, g21, g23, g25 read the n6 chassis and are not applicable on the classic chassis (evidence/run11/FEB_GATES_ON_CLASSIC.json); containment and the tier proof stand in. g22: contract byte-identical to the anchor. g27: PASS at P0.

R6.2  GROW ASDAN week 15
  GROW_ASDAN_W15_Bank_It_Young_Duke_And_The_Team serves C157 and C187 only. g19 v2 PASS after the :root scope migration; the live donor GROW_ASDAN_W7 still carries 15 duplicate :root definitions (finding, not fixed here).

R6.3  wave 4 run 3
  From the content reading: 445 open cells through week 26, 368 eligible, 176 with no lesson at 0.85 in lane and subject.
  The earliest ASDAN gaps have live week-1 strand decks with no trace; recorded untraced-not-unserved, not built (WAVE4_RUN3_TARGETS.json).
  GROW_HUM_W1_Beliefs_And_Worldviews_Around_Us  'GROW Weekly - Autumn'!C60  week 1: containment PASS, g16 v2 105/105, g10 PASS, g15 PASS, g19 v2 PASS, g24 PASS (2 visuals), g26 PASS FK 5.03, g28 PASS, tiers PASS, 10 pages
  GROW_HUM_W2_How_Beliefs_Shape_Who_We_Are  'GROW Weekly - Autumn'!C61  week 2: containment PASS, g16 v2 105/105, g10 PASS, g15 PASS, g19 v2 PASS, g24 PASS (2 visuals), g26 PASS FK 5.19, g28 PASS, tiers PASS, 10 pages
  LAUNCH_HUM_W1_Belief_Identity_And_Belonging  'LAUNCH Weekly - Autumn'!C200  week 1: containment PASS, g16 v2 104/104, g10 PASS, g15 PASS, g19 v2 PASS, g24 PASS (2 visuals), g26 PASS FK 7.28, g28 PASS, tiers PASS, 10 pages
  LAUNCH_HUM_W2_Two_Worldviews_Side_By_Side  'LAUNCH Weekly - Autumn'!C201  week 2: containment PASS, g16 v2 104/104, g10 PASS, g15 PASS, g19 v2 PASS, g24 PASS (2 visuals), g26 PASS FK 7.31, g28 PASS, tiers PASS, 10 pages
  BUILD_HUM_W2_A_Special_Book_A_Special_Place  'BUILD Weekly - Autumn'!C61  week 2: containment PASS, g16 v2 104/104, g10 PASS, g15 PASS, g19 v2 PASS, g24 PASS (2 visuals), g26 PASS FK 2.32, g28 PASS, tiers PASS, 10 pages
  GROW_ASDAN_W1_Choose_My_Young_Duke_Challenge  'GROW Weekly - Autumn'!C144  week 1: containment PASS, g16 v2 96/96, g10 PASS, g15 PASS, g19 v2 PASS, g24 PASS (2 visuals), g26 PASS FK 4.37, g28 PASS, tiers PASS, 4 pages

Not done, and why
  Four week-1 ASDAN cells (BUILD and GROW C174, LAUNCH C88, GROW C131) are taught by live strand decks that carry no trace; not built, recorded for a ruling (H14-2).
  The lesson-file ceiling (24) was reached: 9 case-patched, 8 reshelled, 7 authored. The next true gaps by week are in WAVE4_RUN3_TARGETS.json.
  Trekkers HUD: not measurable from a Lessons-only checkout; handed to SC3 with the exact lines.
  R5: stopped for RULE_CHOICE.

For Matt
  RULE_CHOICE=<a|b>  (R5)
  The four week-1 ASDAN cells whose live strand decks carry no trace: a trace row on a VERIFIED deck is your call.
  GROW_ASDAN_W7 donor: 15 duplicate :root definitions, not in the run-12 migration set.
