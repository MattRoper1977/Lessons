# ORDER HUM-T — the evidence re-stamp fence, measured

Derived by `tools/hum/evidence_limb_census.py` (self-test PASS). Nothing below is typed:
every row is read from the deck's own bytes at `origin/main`, from
`tools/catalogue/TERM_AND_STYLE_EVIDENCE.json`, and from `_sownb/CALENDAR_SPINE.json`.

## What the fence is

Each of the 73 signed Humanities/RE decks carries a pinned source digest in the evidence
record. `tools/catalogue/check_catalogue_static.py` asserts that pin against the working
tree, so **any** byte change to a deck turns it red until the entry is re-stamped.

`tools/catalogue/restamp_evidence_sha256.py` is the only tool permitted to re-stamp, and
it refuses a deck whose week binding nothing but the pin can demonstrate:

> a deck it cannot prove is refused, because re-stamping would freeze in a week binding
> nothing can demonstrate.

`tools/catalogue/build_lesson_order.py` holds the limbs it accepts. A deck it cannot prove
falls into `unresolvedTiming`, where its weeks project as `[]`.

## The measurement

A limb that holds before the transplant holds after it: the adapter only adds. It never
removes a config field, a declared cell or a term token. So the census can be taken on the
pre-transplant bytes and still describe the post-transplant tree.

That was checked against ground truth, not assumed. All 73 decks were transplanted in the
working tree and `build_lesson_order.derive()` was run: `refreshedSourceProofs` named the
same 31 decks this census names, and `unresolvedTiming` named the same 42. The nine decks
of the first batch were built and derived independently first, and agreed 9 of 9.

## The split

SEARCH SCOPE: 73 signed decks in tools/catalogue/HUMANITIES_STRAND.json, bytes at origin/main
pinned source digest: 73 of 73
re-stampable (a limb holds): 31
refused (only the pin holds the week): 42
refused decks whose config spells the whole reference in `cell`: 12
of those, rescued if the reference were built as the deck spells it: 0

| deck | pathway | limb | verdict |
| --- | --- | --- | --- |
| BUILD_HUM_W1_People_Special_To_Me.html | BUILD | declared cell | LANDABLE |
| BUILD_HUM_W2_A_Special_Book_A_Special_Place.html | BUILD | declared cell | LANDABLE |
| BUILD_HUM_W2_People_Who_Help_Us.html | BUILD | declared cell | LANDABLE |
| BUILD_HUM_W3_Places_In_My_Community.html | BUILD | declared cell | LANDABLE |
| BUILD_HUM_W4_Then_And_Now.html | BUILD | declared cell | LANDABLE |
| BUILD_HUM_W5_Same_And_Different.html | BUILD | declared cell | LANDABLE |
| BUILD_HUM_W6_Our_Class_Map.html | BUILD | declared cell | LANDABLE |
| BUILD_HUM_W7_A_place_in_the_group_Classic.html | BUILD | — | the deck carries no lesson-config, so it declares nothing |
| BUILD_HUM_W7_Groups_We_Belong_To.html | BUILD | declared cell | LANDABLE |
| BUILD_HUM_W8_A_Festival_Of_Light.html | BUILD | declared cell | LANDABLE |
| BUILD_Humanities_W4_Show_Respect_When_Handling_Special_Objects.html | BUILD | — | even read as the deck spells it, the deck declares the cell but records no outcome text |
| BUILD_Humanities_W5_Notice_Similarities_Between_People_S_Beliefs.html | BUILD | — | even read as the deck spells it, the deck declares the cell but records no outcome text |
| BUILD_Humanities_W6_Reflect_Quietly_On_Belonging_Day_Of_Peace.html | BUILD | — | even read as the deck spells it, the deck declares the cell but records no outcome text |
| BUILD_Humanities_W7_Share_A_Special_To_Me_Object_With.html | BUILD | — | even read as the deck spells it, the deck declares the cell but records no outcome text |
| BUILD_HUM_W12_A_celebration_in_order_Classic.html | BUILD | — | the deck carries no lesson-config, so it declares nothing |
| BUILD_HUM_W14_A_fair_chance_to_join_in_Classic.html | BUILD | — | the deck carries no lesson-config, so it declares nothing |
| BUILD_HUM_W14_Festivals_Display_and_Reflection.html | BUILD | declared cell | LANDABLE |
| BUILD_HUM_W15_My_Week_Timeline_and_Caring_Stories.html | BUILD | declared cell | LANDABLE |
| BUILD_HUM_W16_Then_And_Now_And_What_Is_Fair.html | BUILD | — | the declared outcome differs from the spine cell |
| BUILD_HUM_W10_Rails_Meet_the_River_OUTSTANDING_V4.html | BUILD | — | the deck carries no lesson-config, so it declares nothing |
| BUILD_HUM_W11_The_Iron_Rush_OUTSTANDING_V4.html | BUILD | — | the deck carries no lesson-config, so it declares nothing |
| BUILD_HUM_W12_A_Town_Grows_Fast_OUTSTANDING_V4.html | BUILD | — | the deck carries no lesson-config, so it declares nothing |
| BUILD_HUM_W13_Crossing_the_Steel_River_OUTSTANDING_V4.html | BUILD | — | the deck carries no lesson-config, so it declares nothing |
| BUILD_HUM_W14_Industry_and_Nature_The_Tees_Story_OUTSTANDING_V4.html | BUILD | — | the deck carries no lesson-config, so it declares nothing |
| BUILD_HUM_W9_Meet_the_Lower_Tees_OUTSTANDING_V4.html | BUILD | — | the deck carries no lesson-config, so it declares nothing |
| GROW_HUM_W1_Beliefs_And_Worldviews_Around_Us.html | GROW | declared cell | LANDABLE |
| GROW_HUM_W1_Migration_On_A_Timeline.html | GROW | declared cell | LANDABLE |
| GROW_HUM_W2_How_Beliefs_Shape_Who_We_Are.html | GROW | declared cell | LANDABLE |
| GROW_HUM_W2_Reading_A_Migration_Source.html | GROW | declared cell | LANDABLE |
| GROW_HUM_W3_Why_People_Moved_And_What_Changed.html | GROW | declared cell | LANDABLE |
| GROW_HUM_W4_Diverse_British_History.html | GROW | declared cell | LANDABLE |
| GROW_HUM_W5_Was_It_Significant.html | GROW | declared cell | LANDABLE |
| GROW_HUM_W6_Planning_An_Account.html | GROW | declared cell | LANDABLE |
| GROW_HUM_W7_Writing_And_Marking_The_Account.html | GROW | declared cell | LANDABLE |
| GROW_HUM_W8_Finding_Places_In_An_Atlas.html | GROW | declared cell | LANDABLE |
| GROW_Humanities_W4_Explore_Hanukkah_And_The_Theme_Of_Light.html | GROW | — | even read as the deck spells it, the deck declares the cell but records no outcome text |
| GROW_Humanities_W5_Explore_Christmas_And_Christian_Belief.html | GROW | — | even read as the deck spells it, the deck declares the cell but records no outcome text |
| GROW_Humanities_W6_Compare_Festivals_Of_Light_Respectfully.html | GROW | — | even read as the deck spells it, the deck declares the cell but records no outcome text |
| GROW_Humanities_W7_Reflect_On_Remembrance_And_Shared_Values.html | GROW | — | even read as the deck spells it, the deck declares the cell but records no outcome text |
| GROW_HUM_W15_Rights_Timeline_and_Belief_Resilience.html | GROW | — | the declared cell is not a spine cell: 'GROW Spring'!C40 |
| GROW_HUM_W16_Sources_Campaigns_And_Hope.html | GROW | — | the declared outcome differs from the spine cell |
| GROW_HUM_W10_Teesside_Connected_World_OUTSTANDING_V3_1.html | GROW | — | the deck carries no lesson-config, so it declares nothing |
| GROW_HUM_W11_Light_Across_the_Map_OUTSTANDING_V3_1.html | GROW | — | the deck carries no lesson-config, so it declares nothing |
| GROW_HUM_W12_Compare_With_Care_OUTSTANDING_V3_1.html | GROW | — | the deck carries no lesson-config, so it declares nothing |
| GROW_HUM_W12_Festival_lights_across_places_Classic.html | GROW | — | the deck carries no lesson-config, so it declares nothing |
| GROW_HUM_W13_Belonging_Briefing_OUTSTANDING_V3_1.html | GROW | — | the deck carries no lesson-config, so it declares nothing |
| GROW_HUM_W13_Compare_celebrations_with_care_Classic.html | GROW | — | the deck carries no lesson-config, so it declares nothing |
| GROW_HUM_W14_Map_and_Belonging_Challenge_OUTSTANDING_V3_1.html | GROW | — | the deck carries no lesson-config, so it declares nothing |
| GROW_HUM_W9_Pinpoint_the_Place_OUTSTANDING_V3_1.html | GROW | — | the deck carries no lesson-config, so it declares nothing |
| LAUNCH_HUM_W1_Belief_Identity_And_Belonging.html | LAUNCH | declared cell | LANDABLE |
| LAUNCH_HUM_W1_Migration_And_Identity_In_Modern_Britain.html | LAUNCH | declared cell | LANDABLE |
| LAUNCH_HUM_W2_Cause_And_Consequence_Of_Migration.html | LAUNCH | declared cell | LANDABLE |
| LAUNCH_HUM_W2_Two_Worldviews_Side_By_Side.html | LAUNCH | declared cell | LANDABLE |
| LAUNCH_HUM_W3_Can_this_record_prove_it_Classic.html | LAUNCH | — | the deck carries no lesson-config, so it declares nothing |
| LAUNCH_HUM_W3_Evaluating_A_Digital_Archive_Source.html | LAUNCH | declared cell | LANDABLE |
| LAUNCH_HUM_W4_A_Timeline_Of_Twentieth_Century_Britain.html | LAUNCH | declared cell | LANDABLE |
| LAUNCH_HUM_W5_Who_Shaped_Britain.html | LAUNCH | declared cell | LANDABLE |
| LAUNCH_HUM_W6_A_Structured_Account_From_Evidence.html | LAUNCH | declared cell | LANDABLE |
| LAUNCH_HUM_W7_Source_Based_Assessment.html | LAUNCH | declared cell | LANDABLE |
| LAUNCH_HUM_W8_Maps_Symbols_And_Grid_References.html | LAUNCH | declared cell | LANDABLE |
| LAUNCH_Humanities_W4_Festivals_Shared_Values_Day_Of_Peace.html | LAUNCH | — | even read as the deck spells it, the deck declares the cell but records no outcome text |
| LAUNCH_Humanities_W5_Structured_Explain_Response.html | LAUNCH | — | even read as the deck spells it, the deck declares the cell but records no outcome text |
| LAUNCH_Humanities_W6_Remembrance_Peace_Across_Beliefs.html | LAUNCH | — | even read as the deck spells it, the deck declares the cell but records no outcome text |
| LAUNCH_Humanities_W7_Belief_Identity_Assessment.html | LAUNCH | — | even read as the deck spells it, the deck declares the cell but records no outcome text |
| LAUNCH_HUM_W15_Conflict_Causes_and_Ethical_Decisions.html | LAUNCH | — | the declared cell is not a spine cell: 'LAUNCH Spring'!C40 |
| LAUNCH_HUM_W16_Steps_In_Law_And_What_Comes_After.html | LAUNCH | — | the declared outcome differs from the spine cell |
| LAUNCH_HUM_W10_Settlement_And_Urbanisation.html | LAUNCH | — | the deck carries no lesson-config, so it declares nothing |
| LAUNCH_HUM_W11_A_growing_town_an_urbanising_region_Classic.html | LAUNCH | — | the deck carries no lesson-config, so it declares nothing |
| LAUNCH_HUM_W11_Local_Fieldwork_Collect_Data.html | LAUNCH | — | the deck carries no lesson-config, so it declares nothing |
| LAUNCH_HUM_W12_Fieldwork_Data_Graphs.html | LAUNCH | — | the deck carries no lesson-config, so it declares nothing |
| LAUNCH_HUM_W13_Contrasting_Places.html | LAUNCH | — | the deck carries no lesson-config, so it declares nothing |
| LAUNCH_HUM_W14_Fieldwork_Enquiry_Write_Up.html | LAUNCH | — | the deck carries no lesson-config, so it declares nothing |
| LAUNCH_HUM_W9_GIS_Layers_Reading_Place.html | LAUNCH | — | the deck carries no lesson-config, so it declares nothing |
