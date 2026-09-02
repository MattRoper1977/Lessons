# Filename labels

Filenames are labels. ORDER VB-RUN13 H12-3 keeps every one of them: renaming a
live deck breaks links, the catalogue, planners and QR codes. The stale week in a
name is recorded here once and read by nobody -- g27 fails any tool under
`_sownb/` or `tools/` that derives a week from a path, and the script that built
this file lives outside both for that reason.

Measured 2026-09-02 across 445 deck files whose name carries a week number.

## What the numbers are

    91  the name agrees with the ruled week of the cells the deck claims
    67  the name DRIFTS from the ruled week of its cells
     6  the name is term-relative, so its number was never an absolute week
   281  the deck claims no cell, so there is nothing to compare the name with

Nearly every drift is one week, and it has a single cause: the run-11 spine
re-key moved Autumn 2, Spring 1, Spring 2 and Summer 2 up by one, and the D-C
correction that carried it through the estate was text only, with zero renames.
That was the right call and it is why this file exists.

  drift distribution, ruled week minus the number in the name:
    +1 week   67 files

## The drifted names, and the ruled week of the cells each deck claims

Read the right-hand column. The left is a label.

  BUILD_ASDAN/Spring1_W1-W6_2026-27/BUILD_ASDAN_W15_Choice_Budget_and_Project_Reset.html
      name says W15, cells say [16]
  BUILD_ASDAN/Spring1_W1-W6_2026-27/BUILD_ASDAN_W16_Partner_Challenge_and_Seasonal_Goals.html
      name says W16, cells say [17]
  Build/Slideshows/BUILD_ART_W8_Festival_Sounds.html
      name says W8, cells say [9]
  GROW_ASDAN/Spring1_W1-W6_2026-27/GROW_ASDAN_W15_Strengths_Challenge_and_Project_Reset.html
      name says W15, cells say [16]
  GROW_ASDAN/Spring1_W1-W6_2026-27/GROW_ASDAN_W16_Authorised_Task_Project_Plan_and_New_Goals.html
      name says W16, cells say [17]
  Grow/Slideshows/GROW_ART_W8_Festival_Sounds.html
      name says W8, cells say [9]
  Humanities_Teesside/BUILD_W1-W8_2026-27/BUILD_HUM_W8_A_Festival_Of_Light.html
      name says W8, cells say [9]
  Humanities_Teesside/BUILD_W14-W20_2026-27/BUILD_HUM_W14_Festivals_Display_and_Reflection.html
      name says W14, cells say [15]
  Humanities_Teesside/BUILD_W14-W20_2026-27/BUILD_HUM_W15_My_Week_Timeline_and_Caring_Stories.html
      name says W15, cells say [16]
  Humanities_Teesside/BUILD_W14-W20_2026-27/BUILD_HUM_W16_Then_And_Now_And_What_Is_Fair.html
      name says W16, cells say [17]
  Humanities_Teesside/GROW_W1-W8_2026-27/GROW_HUM_W8_Finding_Places_In_An_Atlas.html
      name says W8, cells say [9]
  Humanities_Teesside/GROW_W15-W20_2026-27/GROW_HUM_W15_Rights_Timeline_and_Belief_Resilience.html
      name says W15, cells say [16]
  Humanities_Teesside/GROW_W15-W20_2026-27/GROW_HUM_W16_Sources_Campaigns_And_Hope.html
      name says W16, cells say [17]
  Humanities_Teesside/GROW_W9-W14_2026-27/GROW_HUM_W10_Teesside_Connected_World_OUTSTANDING_V3_1.html
      name says W10, cells say [11]
  Humanities_Teesside/GROW_W9-W14_2026-27/GROW_HUM_W11_Light_Across_the_Map_OUTSTANDING_V3_1.html
      name says W11, cells say [12]
  Humanities_Teesside/GROW_W9-W14_2026-27/GROW_HUM_W12_Compare_With_Care_OUTSTANDING_V3_1.html
      name says W12, cells say [13]
  Humanities_Teesside/GROW_W9-W14_2026-27/GROW_HUM_W13_Belonging_Briefing_OUTSTANDING_V3_1.html
      name says W13, cells say [14]
  Humanities_Teesside/GROW_W9-W14_2026-27/GROW_HUM_W14_Map_and_Belonging_Challenge_OUTSTANDING_V3_1.html
      name says W14, cells say [15]
  Humanities_Teesside/GROW_W9-W14_2026-27/GROW_HUM_W9_Pinpoint_the_Place_OUTSTANDING_V3_1.html
      name says W9, cells say [10]
  Humanities_Teesside/LAUNCH_W1-W8_2026-27/LAUNCH_HUM_W8_Maps_Symbols_And_Grid_References.html
      name says W8, cells say [9]
  Humanities_Teesside/LAUNCH_W15-W20_2026-27/LAUNCH_HUM_W15_Conflict_Causes_and_Ethical_Decisions.html
      name says W15, cells say [16]
  Humanities_Teesside/LAUNCH_W15-W20_2026-27/LAUNCH_HUM_W16_Steps_In_Law_And_What_Comes_After.html
      name says W16, cells say [17]
  LAUNCH_ASDAN/Spring1_W1-W6_2026-27/LAUNCH_ASDAN_W16_Decision_Tools_Banking_Plant_Care_and_Project_Plan.html
      name says W16, cells say [17]
  LAUNCH_ASDAN/W13-W14_2026-27/lessons/COMM/COMM_W13_Record_And_Organise_Project_Evidence_LAUNCH.html
      name says W13, cells say [14]
  LAUNCH_ASDAN/W13-W14_2026-27/lessons/COMM/COMM_W14_Autumn_Community_Project_Review_Outcome_LAUNCH.html
      name says W14, cells say [15]
  LAUNCH_ASDAN/W7-W12_2026-27/lessons/COMM/COMM_W11_Mid_Point_Review_Keep_Change_or_Stop_LAUNCH.html
      name says W11, cells say [12]
  LAUNCH_ASDAN/W7-W12_2026-27/lessons/COMM/COMM_W8_Run_the_Project_Need_Before_Activity_LAUNCH.html
      name says W8, cells say [9]
  LAUNCH_ASDAN/W7-W12_2026-27/lessons/COMM/COMM_W9_Solve_a_Delivery_Problem_Cause_Options_Change_LAUNCH.html
      name says W9, cells say [10]
  LAUNCH_ASDAN/W7-W12_2026-27/lessons/LI/LI_W11_Plan_a_Healthy_Week_Balance_Time_Culture_Routine_LAUNCH.html
      name says W11, cells say [12]
  LAUNCH_ASDAN/W7-W12_2026-27/lessons/LI/LI_W12_Budget_the_Food_Shop_Price_Portions_Best_Value_LAUNCH.html
      name says W12, cells say [13]
  LAUNCH_ASDAN/W7-W12_2026-27/lessons/LI/LI_W9_Prepare_a_Balanced_Meal_Safe_Timed_Low_Waste_LAUNCH.html
      name says W9, cells say [10]
  LAUNCH_ASDAN/W7-W12_2026-27/lessons/PEQ/PEQ_W10_Use_the_Plan_Carry_Out_the_Team_Activity_LAUNCH.html
      name says W10, cells say [11]
  LAUNCH_ASDAN/W7-W12_2026-27/lessons/PEQ/PEQ_W11_Adapt_Under_Pressure_Manage_Barriers_Own_My_Role_LAUNCH.html
      name says W11, cells say [12]
  LAUNCH_ASDAN/W7-W12_2026-27/lessons/PEQ/PEQ_W8_Agree_the_Team_Contract_Goals_Roles_Ground_Rules_LAUNCH.html
      name says W8, cells say [9]
  LAUNCH_ASDAN/W7-W12_2026-27/lessons/PEQ/PEQ_W9_Plan_the_Team_Activity_Barriers_Support_Review_LAUNCH.html
      name says W9, cells say [10]
  LAUNCH_ASDAN/W7-W12_2026-27/lessons/VOC/VOC_W11_Run_the_Service_Standards_Under_Pressure_LAUNCH.html
      name says W11, cells say [12]
  Science_Teesside/Build/W14-W20_2026-27/SCI_B_W14A_Autumn_Science_Review_Explore.html
      name says W14, cells say [15]
  Science_Teesside/Build/W14-W20_2026-27/SCI_B_W14B_Autumn_Science_Evidence_Do.html
      name says W14, cells say [15]
  Science_Teesside/Build/W14-W20_2026-27/SCI_B_W15A_Fossil_Formation_Story_Explore.html
      name says W15, cells say [16]
  Science_Teesside/Build/W14-W20_2026-27/SCI_B_W15B_Fossil_Formation_Evidence_Do.html
      name says W15, cells say [16]
  Science_Teesside/Build/W14-W20_2026-27/SCI_B_W16A_Fossil_Clues_Explore.html
      name says W16, cells say [17]
  Science_Teesside/Build/W14-W20_2026-27/SCI_B_W16B_Fossil_Evidence_Do.html
      name says W16, cells say [17]
  Science_Teesside/Build/W8-W13_2026-27/SCI_B_W10A_Rock_Hardness_Explore.html
      name says W10, cells say [11]
  Science_Teesside/Build/W8-W13_2026-27/SCI_B_W10B_Hardness_Evidence_Do.html
      name says W10, cells say [11]
  Science_Teesside/Build/W8-W13_2026-27/SCI_B_W13A_Fair_Test_Planner_Change_One_Thing_Explore.html
      name says W13, cells say [14]
  Science_Teesside/Build/W8-W13_2026-27/SCI_B_W13B_Method_Pilot_Test_The_Test_Do.html
      name says W13, cells say [14]
  Science_Teesside/Build/W8-W13_2026-27/SCI_B_W9A_Rock_Evidence_Explore.html
      name says W9, cells say [10]
  Science_Teesside/Build/W8-W13_2026-27/SCI_B_W9B_Rock_Sorting_Key_Do.html
      name says W9, cells say [10]
  Science_Teesside/Grow/W15-W20_2026-27/SCI_G_W15A_Materials_Properties_Explore.html
      name says W15, cells say [16]
  Science_Teesside/Grow/W15-W20_2026-27/SCI_G_W15B_Materials_Properties_Evidence_Do.html
      name says W15, cells say [16]
  Science_Teesside/Grow/W15-W20_2026-27/SCI_G_W16A_Solubility_And_Recovery_Explore.html
      name says W16, cells say [17]
  Science_Teesside/Grow/W15-W20_2026-27/SCI_G_W16B_Getting_The_Solid_Back_Do.html
      name says W16, cells say [17]
  Science_Teesside/Grow/W8-W13_2026-27/SCI_G_W10A_Solar_System_Research_Explore.html
      name says W10, cells say [11]
  Science_Teesside/Grow/W8-W13_2026-27/SCI_G_W10B_Solar_System_Presentation_Do.html
      name says W10, cells say [11]
  Science_Teesside/Grow/W8-W13_2026-27/SCI_G_W11A_Global_Warming_Explore.html
      name says W11, cells say [12]
  Science_Teesside/Grow/W8-W13_2026-27/SCI_G_W11B_Climate_Action_Do.html
      name says W11, cells say [12]
  Science_Teesside/Grow/W8-W13_2026-27/SCI_G_W12A_Science_Connections_Explore.html
      name says W12, cells say [13]
  Science_Teesside/Grow/W8-W13_2026-27/SCI_G_W12B_Science_Answer_Lab_Do.html
      name says W12, cells say [13]
  Science_Teesside/Grow/W8-W13_2026-27/SCI_G_W13A_Rover_Rescue_Plan_Explore.html
      name says W13, cells say [14]
  Science_Teesside/Grow/W8-W13_2026-27/SCI_G_W13B_Rover_Rescue_Investigation_Do.html
      name says W13, cells say [14]
  Science_Teesside/Grow/W8-W13_2026-27/SCI_G_W8A_Day_And_Night_Explore.html
      name says W8, cells say [9]
  Science_Teesside/Grow/W8-W13_2026-27/SCI_G_W8B_Day_And_Night_Do.html
      name says W8, cells say [9]
  Science_Teesside/Grow/W8-W13_2026-27/SCI_G_W9A_Spherical_Bodies_Explore.html
      name says W9, cells say [10]
  Science_Teesside/Grow/W8-W13_2026-27/SCI_G_W9B_Spherical_Bodies_Do.html
      name says W9, cells say [10]
  Science_Teesside/Launch/W15-W20_2026-27/SCI_L_W15L1_Variation_and_Natural_Selection_Introduce.html
      name says W15, cells say [16]
  Science_Teesside/Launch/W15-W20_2026-27/SCI_L_W15L2_Natural_Selection_Evidence_Explore.html
      name says W15, cells say [16]
  Science_Teesside/Launch/W15-W20_2026-27/SCI_L_W15L3_Natural_Selection_Explanation_Do.html
      name says W15, cells say [16]

## Names that are term-relative, not absolute

These carry a term marker before the week number, so the number is a position
inside a term and was never a claim about an absolute week. Not drift.

  PEQ_A2_W7_Complete_Profile_and_Evidence_GROW_v3_40min.html — 7 within its term, cells say [15]
  SCI_G_A2_W7A_Autumn_Science_Review_Explore.html — 7 within its term, cells say [15]
  SCI_G_A2_W7B_Autumn_Science_Evidence_Do.html — 7 within its term, cells say [15]
  SCI_L_A2_W7L1_Topics_2_3_Assessment_Introduce.html — 7 within its term, cells say [15]
  SCI_L_A2_W7L2_Topics_2_3_Assessment_Explore.html — 7 within its term, cells say [15]
  SCI_L_A2_W7L3_Topics_2_3_Assessment_Do.html — 7 within its term, cells say [15]

## Why this file has no bulleted list

Register files in this estate are tokenised bullet by bullet by the g10 name
gate. This is not a register, it is a record, and it carries no bullets so that
it can never be mistaken for one.
