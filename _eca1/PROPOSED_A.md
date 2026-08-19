# ECA-1 PROPOSED_A — judgement calls for Matt (PART A)

Applied fixes are NOT here (see the eight `ECA-1 A/*` commit bodies for the full
before/after register). Quotes verified verbatim in-file at audit time (372/373).
Humanities / DT / Art-estate-docs findings appended when their audits complete.

## Pass-level rulings already recorded (DECISIONS.md)

- BUILD HUM oral close + GROW/LAUNCH HUM W7 missing written line: sentinel-held
  (50/123 must hold), so any closure-marker change needs its own pass.
- `{Build,Grow,Launch}/Slideshows/*_ART_*` (24 decks) are a separate art suite
  outside ECA-1's universe (Art = Art_Teesside) — unaudited; rule if wanted.
- LAUNCH_HUM_W2 'judgment' ×7: correct British legal register in the courtroom
  frame — accepted exception, not patched.

## Serious findings needing a ruling (WRONG/MISALIGNED, fix is a judgement call)

**P1 · BUILD_ASDAN/Community_Project/COMM_W3_Our_Team_Roles.html** (C-construction, screen; WRONG)
- Current: “Next lesson: Partner Update — keep them informed. UPDATEWK 4 ✓”
- Issue: Lesson-complete modal's next-lesson teaser ends with the leftover junk token 'UPDATEWK 4 ✓'.
- Proposed: Next lesson: Partner Update — keep them informed.
- Source: Internal consistency — W1/W4/W5/W6 next-lesson lines carry no such token

**P2 · BUILD_ASDAN/Community_Project/COMM_W1_Choose_Our_Asset.html** (C-construction, screen; WRONG)
- Current: “Say who our asset is for and why it matters. Today's outcome goes ont…”
- Issue: Lesson-complete modal summary line is cut mid-word ('ont…') by a build-time character cap.
- Proposed: end the line at '…why it matters.' or complete it as 'Today's outcome goes onto the Project Board.'
- Source: Internal — sentence ends mid-word; the complete pattern 'Today's outcome goes on the display' appears in the same file's _taBriefs

**P3 · BUILD_ASDAN/Community_Project/COMM_W2_The_Site's_Need.html** (C-construction, screen; WRONG)
- Current: “Share one requirement with the group. Today's outcome goes onto the P…”
- Issue: Lesson-complete modal summary line is cut mid-word ('the P…') by a build-time character cap.
- Proposed: end the line at '…with the group.' or complete it as 'Today's outcome goes onto the Project Board.'
- Source: Internal — sentence ends mid-word; same systemic truncation in all six decks

**P4 · BUILD_ASDAN/Community_Project/COMM_W3_Our_Team_Roles.html** (C-construction, screen; WRONG)
- Current: “Say how your role helps the whole team succeed. Today's outcome goes…”
- Issue: Lesson-complete modal summary line is cut mid-sentence ('goes…') by a build-time character cap.
- Proposed: end the line at '…team succeed.' or complete it as 'Today's outcome goes onto the Project Board.'
- Source: Internal — sentence ends mid-clause; same systemic truncation in all six decks

**P5 · BUILD_ASDAN/Community_Project/COMM_W4_Partner_Update.html** (C-construction, screen; WRONG)
- Current: “Say one thing you'd tell our partner. Today's outcome goes onto the P…”
- Issue: Lesson-complete modal summary line is cut mid-word ('the P…') by a build-time character cap.
- Proposed: end the line at '…our partner.' or complete it as 'Today's outcome goes onto the Project Board.'
- Source: Internal — sentence ends mid-word; same systemic truncation in all six decks

**P6 · BUILD_ASDAN/Community_Project/COMM_W5_Plan_the_Handover.html** (C-construction, screen; WRONG)
- Current: “Say your part in the handover to the group. Today's outcome goes onto…”
- Issue: Lesson-complete modal summary line is cut mid-sentence ('onto…') by a build-time character cap.
- Proposed: end the line at '…to the group.' or complete it as 'Today's outcome goes onto the Project Board.'
- Source: Internal — sentence ends mid-clause; same systemic truncation in all six decks

**P7 · BUILD_ASDAN/Community_Project/COMM_W6_The_Handover_and_Its_Benefit.html** (C-construction, screen; WRONG)
- Current: “Agree who reports the benefit back to the class. Today's outcome goes…”
- Issue: Lesson-complete modal summary line is cut mid-sentence ('goes…') by a build-time character cap.
- Proposed: end the line at '…back to the class.' or complete it as 'Today's outcome goes onto the Project Board.'
- Source: Internal — sentence ends mid-clause; same systemic truncation in all six decks

**P8 · BUILD_ASDAN/Community_Project/START_HERE.html** (D-alignment, screen; MISALIGNED)
- Current: “Weeks 7–8: consolidation &amp; portfolio completion (see the Scheme of Work).”
- Issue: START_HERE says weeks 7–8 are consolidation while the Scheme of Work it cites says only 'Week 8 is consolidation &amp; portfolio completion'; the SoW is silent on W7 for this slot.
- Proposed: align one side — either 'Week 8: consolidation & portfolio completion' here, or state W7's use on the SoW.
- Source: BUILD_ASDAN/Scheme_of_Work.html shared-blueprint paragraph ('Week 8 is consolidation & portfolio completion')

**P9 · BUILD_ASDAN/Careers/CAREERS_W1_My_Strengths.html** (C-construction, screen; WRONG)
- Current: “Onto the Strengths Wall: Say which job area you'd like to explore next. Today's outcome goes o…”
- Issue: The lesson-complete overlay's Lundy summary line is cut off mid-word and carries the SoW's old W1 voice ask instead of this deck's actual Lundy Voice ('Say one strength you would want written about you').
- Proposed: "Onto the Strengths Wall: Say one strength you would want written about you." (full sentence, drop the truncated tail)
- Source: Same file's Lundy VOICE box (4 consistent surfaces) vs BUILD_ASDAN/Scheme_of_Work.html W1 row

**P10 · BUILD_ASDAN/Careers/CAREERS_W2_Jobs_in_My_Community.html** (C-construction, both; WRONG)
- Current: “Name a job someone in your family does.”
- Issue: Arrival supported Q1 (screen and print) asks pupils to name a family member's job — exactly what the same file's staff sensory note forbids ('never ask a pupil to name a family member's job').
- Proposed: PROPOSED (learner-task text — do not silently alter): e.g. "Name a job someone does in our town."
- Source: Same file, Access & sensory notes (staff), Scaffolding – Supported section

**P11 · BUILD_ASDAN/Careers/CAREERS_W2_Jobs_in_My_Community.html** (C-construction, screen; WRONG)
- Current: “Onto the Strengths Wall: Tell a partner one job you'd like to find out more about. Today's out…”
- Issue: Lesson-complete Lundy line is truncated mid-word and uses the SoW's old W2 ask instead of the deck's Voice ('Say one local job you would want to know more about.').
- Proposed: "Onto the Strengths Wall: Say one local job you would want to know more about."
- Source: Same file's Lundy VOICE box vs BUILD_ASDAN/Scheme_of_Work.html W2 row

**P12 · BUILD_ASDAN/Careers/CAREERS_W3_Skills_Employers_Want.html** (C-construction, both; WRONG)
- Current: “Round 1: Reliable · Teamwork · Effort · Blue eyes, Round 2: On time · Kind words · Gives up fast · Listens, Reliable, Effort”
- Issue: 'Odd one out' promises each card is a set with one odd item, but cards 3–4 are the bare words 'Reliable' and 'Effort' that just reveal definitions — half the activity does not match its own instruction ('Three of these belong together and one does not').
- Proposed: replace the two stray cards with real Round 3/Round 4 sets, or drop them and set the counter to /2
- Source: Slide's own 'How it works' text vs _pres t2/t3 reveals in the same file

**P13 · BUILD_ASDAN/Careers/CAREERS_W3_Skills_Employers_Want.html** (C-construction, screen; WRONG)
- Current: “Onto the Strengths Wall: Pick one skill to grow this term — who will notice? Today's outcome g…”
- Issue: Lesson-complete Lundy line is truncated mid-word and uses the SoW's old W3 ask instead of the deck's Voice ('Say the skill you are growing, not the one you have mastered.').
- Proposed: "Onto the Strengths Wall: Say the skill you are growing, not the one you have mastered."
- Source: Same file's Lundy VOICE box vs BUILD_ASDAN/Scheme_of_Work.html W3 row

**P14 · BUILD_ASDAN/Careers/CAREERS_W4_Routines_and_Reliability.html** (C-construction, screen; WRONG)
- Current: “Onto the Strengths Wall: Say one thing that would make your morning easier. Today's outcome go…”
- Issue: Lesson-complete Lundy line is truncated mid-word ('goes o…' family artifact); the voice ask itself matches this deck, so only the truncation needs fixing here.
- Proposed: end the line at "…make your morning easier." and drop the truncated tail
- Source: Same truncation artifact appears in all seven decks' lc-summary lines

**P15 · BUILD_ASDAN/Careers/CAREERS_W5_Applying_Myself.html** (C-construction, both; WRONG)
- Current: “LEAVE OFF: Never on a profile — that's for after you…”
- Issue: Four of the six 'Goes On the Profile, or Stays Off?' match targets are cut mid-word with '…' on screen and in print; the full sentences exist in the We Do 1 pool.
- Proposed: restore full endings from _pres — "…after you're hired, securely", "…the profile is your best self", "…people going somewhere", "…an employer skill too"
- Source: _pres t1/t3/t4/t5 in the same file hold the complete texts

**P16 · BUILD_ASDAN/Careers/CAREERS_W5_Applying_Myself.html** (D-alignment, screen; MISALIGNED)
- Current: “Next lesson: My Career Profile — poster &amp; portfolio. MY CAREER”
- Issue: Trailer names the wrong next lesson (taught Week 6 is 'What Happens After Year 11'; My Career Profile is Week 7) and ends with the leaked junk suffix ' MY CAREER'.
- Proposed: "Next lesson: What Happens After Year 11 — four post-16 routes."
- Source: START_HERE.html: 'Week 6 · What Happens After Year 11' and footnote 'Week 6 is now taught (post-16 routes)'

**P17 · BUILD_ASDAN/Careers/CAREERS_W5_Applying_Myself.html** (C-construction, screen; WRONG)
- Current: “Onto the Strengths Wall: Share one line of your profile with the group or the TA. Today's outc…”
- Issue: Lesson-complete Lundy line is truncated mid-word and uses the SoW's old W5 ask instead of the deck's Voice ('Read one line of your profile out loud — one line, not the page.').
- Proposed: "Onto the Strengths Wall: Read one line of your profile out loud — one line, not the page."
- Source: Same file's Lundy VOICE box vs BUILD_ASDAN/Scheme_of_Work.html W5 row

**P18 · BUILD_ASDAN/Careers/CAREERS_W5_Applying_Myself.html** (C-construction, both; WRONG)
- Current: “Use the Banked Strengths Deck in the print pack”
- Issue: The Independent Work slide sends catch-up pupils to the Banked Strengths Deck 'in the print pack', but printPack()'s section list omits 'strengthsdeck' and no control ever shows it — the promised sheet cannot be printed from this file.
- Proposed: add 'strengthsdeck' to the printPack id list (or a dedicated print button) in this file
- Source: printPack() id list ['ko','intro','arrival','starter','wedo','exit','witness','feedback'] in the same file; #print-strengthsdeck is referenced nowhere else

**P19 · BUILD_ASDAN/Careers/CAREERS_W6_My_Career_Profile.html** (C-construction, both; WRONG)
- Current: “Use the Banked Strengths Deck in the print pack”
- Issue: Same defect as W5: #print-strengthsdeck exists but printPack()'s section list omits 'strengthsdeck', so the catch-up sheet the slide promises can never be printed.
- Proposed: add 'strengthsdeck' to the printPack id list (or a dedicated print button) in this file
- Source: printPack() id list in the same file; 'strengthsdeck' appears only once (the div itself)

**P20 · BUILD_ASDAN/Careers/CAREERS_W6_My_Career_Profile.html** (C-construction, screen; WRONG)
- Current: “Onto the Strengths Wall: Name one adult who can help with your next step — they report back. T…”
- Issue: Lesson-complete Lundy line is truncated mid-word and uses the SoW's W7 ask instead of the deck's Voice ('Say the one thing you would want a stranger to notice about your poster.').
- Proposed: "Onto the Strengths Wall: Say the one thing you would want a stranger to notice about your poster."
- Source: Same file's Lundy VOICE box vs BUILD_ASDAN/Scheme_of_Work.html W7 row

**P21 · BUILD_ASDAN/Careers/CAREERS_W6_My_Career_Profile.html** (C-construction, print; WRONG)
- Current: “Real example — prove it · Name · strengths with examples · a job area · The Strengths Wall · Your call — say it proud”
- Issue: The printed We Do 2 answer list uses '·' both between answers and inside the multi-part answer 'Name · strengths with examples · a job area', so 4 questions face 6 apparent answers on paper.
- Proposed: "Real example — prove it · Name, strengths with examples, a job area · The Strengths Wall · Your call — say it proud"
- Source: The 4 question pills printed directly above this list in the same #print-wedo section

**P22 · BUILD_ASDAN/Careers/CAREERS_W7_After_Year_11.html** (A-qa, both; WRONG)
- Current: “data-correct="m2" onclick="pickTarget(this)">You have work lined up already and you will study alongside it”
- Issue: 'Which Route Fits?' keys the We Do 1 quiz questions to route scenarios: 'Which route is mostly in a workplace?' is keyed to the work-with-study scenario while the supported-internship scenario ('EHC plan… job coach') is keyed to 'Where is our nearest college?' — the taught-correct pairing scores as wrong on screen and the printed line-match is incoherent ('Can you stop learning at 16?' has no vali
- Proposed: make the four pills the routes (College · Apprenticeship · Work + study · Supported internship) and re-key m0→'try a subject properly', m1→'earn while you learn', m2→'work lined up already', m3→'EHC plan… job coach'
- Source: Same deck's I Do 1 step 2 and _pres t2 ('The supported internship — most of the time is spent in the workplace, with a job coach.')

**P23 · BUILD_ASDAN/Careers/CAREERS_W7_After_Year_11.html** (C-construction, both; WRONG)
- Current: “there is no wrong answer here, only your answer.”
- Issue: The 'Rule It In, or Rule It Out' instruction (and TA brief 'Not a quiz') sits over cards that are factual quiz questions with right answers revealed on tap ('Can you stop learning at 16?' → 'No — …until you turn 18'), and the print pack titles the same activity 'We Do 1: Team quiz — talk, then reveal'.
- Proposed: either restore team-quiz framing on the slide (matching the print/hub) or swap the cards for the four routes to genuinely rule in/out
- Source: Same file: _pres reveals, _taBriefs 'We Do 1', and #print-wedo heading 'We Do 1: Team quiz — talk, then reveal'

**P24 · BUILD_ASDAN/Careers/CAREERS_W7_After_Year_11.html** (A-qa, screen; WRONG)
- Current: “Who you are, your headline strength, and where you're heading.”
- Issue: The stretch Arrival Q2 answer key is the poster-in-ten-seconds key copied from the My Career Profile deck and does not answer its own stem ('Which of your strengths would an employer notice on day one of an apprenticeship?').
- Proposed: "Own pick — the visible ones first: turning up on time, listening, sticking at the task."
- Source: CAREERS_W6_My_Career_Profile.html stretch Q2 uses the identical key for its poster stem, where it fits

**P25 · BUILD_ASDAN/Careers/CAREERS_W7_After_Year_11.html** (C-construction, screen; WRONG)
- Current: “Onto the Strengths Wall: The routes you pin decide which providers we invite in and which open days we go to. T…”
- Issue: Lesson-complete Lundy line is truncated mid-word and carries the Influence text where every other week carries a Voice ask.
- Proposed: "Onto the Strengths Wall: Say the route you are leaning towards — 'not sure yet' counts."
- Source: Same file's Lundy VOICE box ('Say the route you are leaning towards — leaning is enough…')

**P26 · BUILD_ASDAN/Careers/START_HERE.html** (A-fact, screen; WRONG)
- Current: “Confirm ASDAN module codes and any approvals before teaching.”
- Issue: The footnote frames ASDAN approvals as potentially pending, but the school's ASDAN registration/approval was completed 30 Jul 2026 and must never be framed as pending; only module-code confirmation should remain.
- Proposed: "Confirm ASDAN module codes with the course coordinator before teaching — registration and approval are in place (30 Jul 2026)."
- Source: _passpq/SPEC_FACTS.md §19: registration/approval DONE (Matt, 30 Jul 2026), never to be framed as pending

**P27 · BUILD_ASDAN/Duke_and_Enterprise/DUKE_W2_A_Kindness_Challenge.html** (A-qa, screen; WRONG)
- Current: “I noticed Callum eats alone on Tuesdays, so I planned to sit with him and bring the Uno cards”
- Issue: The We Do 2 WAGOLL model answer names a specific child ('Callum') and publicly describes his vulnerability (eats alone), directly contradicting this same lesson's taught rules — payload hotspot 'KEEP DIGNITY: The action should not display, embarrass or identify another person' and 'REFLECT WITHOUT CLAIMING CREDIT ... rather than presenting another person as evidence' — and the SoW blueprint's 'no 
- Proposed: anonymise the recipient, e.g. 'I noticed someone in our class often eats alone, so I planned to sit with them and bring the Uno cards' (and adjust the following pronouns), keeping the structure tags intact.
- Source: Same deck's ASDANVisualPayloads DUKE_W2 hotspots h2/h6; BUILD_ASDAN/Scheme_of_Work.html shared blueprint ('no pupil names')

**P28 · BUILD_ASDAN/Duke_and_Enterprise/DUKE_W5_Our_Social_Enterprise.html** (C-construction, both; WRONG)
- Current: “HELPS PEOPLE: Helps wildlife and the site — and can sel…”
- Issue: All six We Do 2 match-target texts are build-truncated with an ellipsis, several mid-word ('sel…', 'chan…', 'a d…', 'miss…', 'two…'), on the interactive slide and in the printed pack, though the full sentences exist in this deck's _pres pool.
- Proposed: restore the full _pres sentences on the six match targets (e.g. '…and can sell to fund more', '…pocket money just changes pockets', '…a double fail', '…one engine missing', '…two engines').
- Source: Same file's _pres object holds the untruncated sentences; truncation visible on #wedo2 targets and print-wedo section

**P29 · BUILD_ASDAN/Duke_and_Enterprise/DUKE_W1_Choose_My_Challenges.html** (C-construction, print; WRONG)
- Current: “Doing it while nervous — not not being nervou…”
- Issue: The printed We Do 2 match-up definitions are truncated mid-word ('nervou…', and 'One of our challenge areas — and how we treat…'), so pupils drawing lines on the printed pack cannot read two of the six definitions.
- Proposed: print the full _pres definitions: 'Doing it while nervous — not not being nervous.' and 'One of our challenge areas — and how we treat ourselves when it's hard.'
- Source: Same file's _pres t5/t4 hold the full sentences; print-wedo section carries the truncated copies

**P30 · BUILD_ASDAN/Duke_and_Enterprise/DUKE_W3_An_Eco_Challenge.html** (C-construction, screen; WRONG)
- Current: “Next lesson: An Independence Challenge — skills for life. I DID IT”
- Issue: The lesson-complete overlay both truncates its Lundy line mid-sentence ('who benefits? Today's outcome goes on…') and appends a stray build token 'I DID IT' (W4's wall-card label) to the next-lesson trail.
- Proposed: complete the outcome sentence and drop the trailing token: 'Next lesson: An Independence Challenge — skills for life.'
- Source: Compare W1/W2 LC overlays (no token) and the deck's data descriptors; truncation pattern identical across all six decks

**P31 · BUILD_ASDAN/Duke_and_Enterprise/DUKE_W4_An_Independence_Challenge.html** (C-construction, screen; WRONG)
- Current: “Next lesson: Our Social Enterprise — a small idea for good. £OUR STALL”
- Issue: The lesson-complete overlay appends the stray build token '£OUR STALL' to the next-lesson trail and truncates its Lundy line ('get better at. Today's outcome goes onto th…').
- Proposed: 'Next lesson: Our Social Enterprise — a small idea for good.' and complete the outcome sentence.
- Source: Compare W1/W2 LC overlays (clean descriptors); same generator defect as W3/W5

**P32 · BUILD_ASDAN/Duke_and_Enterprise/DUKE_W5_Our_Social_Enterprise.html** (C-construction, screen; WRONG)
- Current: “Next lesson: Pitch &amp; Reflect — present &amp; log. WE DID THIS”
- Issue: The lesson-complete overlay appends the stray token 'WE DID THIS' to the next-lesson trail and truncates its Lundy line ('with the group. Today's outcome goes onto t…').
- Proposed: 'Next lesson: Pitch &amp; Reflect — present &amp; log.' and complete the outcome sentence.
- Source: Compare W1/W2 LC overlays (clean descriptors); same generator defect as W3/W4

**P33 · BUILD_ASDAN/Duke_and_Enterprise/DUKE_W1_Choose_My_Challenges.html** (C-construction, screen; WRONG)
- Current: “looking forward to. Today's outcome g…”
- Issue: The lesson-complete overlay's 'Onto the Challenge Wall' summary line is build-truncated mid-word ('Today's outcome g…'); the same truncation recurs in W2 ('goes ont…') and W6 ('Today's out…').
- Proposed: complete the sentence, e.g. '…Today's outcome goes onto the display.' (apply the same completion in W2 and W6).
- Source: Visible ellipsis mid-word in the lc-summary spans of W1, W2 and W6; TA brief text names the display action in full

**P34 · BUILD_ASDAN/Duke_and_Enterprise/DUKE_W2_A_Kindness_Challenge.html** (B-spelling, both; WRONG)
- Current: “world kindness day. What do you think we'll be doing?”
- Issue: 'World Kindness Day' is a proper noun (the named observance) but is printed lower-case in the Arrival (Standard) Q2 on screen and in the print pack (2 occurrences), and likewise in W1's lesson-complete overlay 'Next lesson: A Kindness Challenge — world kindness day'.
- Proposed: capitalise to 'World Kindness Day' in both W2 occurrences and the W1 overlay.
- Source: World Kindness Day (13 November) is a named international observance — verified knowledge; capitalised correctly in the SoW and in W2's I Do 1

**P35 · BUILD_ASDAN/FoodWise/FW_W1_Food_Groups.html** (A-qa, screen; WRONG)
- Current: “The apple and the carrot sticks in your lunch”
- Issue: We Do 2 match slide keys this target to the pill FRUIT (data-correct="m1"), but a carrot is a vegetable, and the same lesson's FRUIT reveal card defines fruit specifically as "Nature's sweet defence — vitamins and fibre" — the deck teaches carrot = fruit.
- Proposed: change the target to a fruit-only example, e.g. "The apple and the orange in your lunch" (or relabel the pill FRUIT & VEG to match the Eatwell group, as the WAGOLL's "apple and carrots to fruit and veg" does).
- Source: Verified knowledge: carrot is a vegetable; the Eatwell Guide group is "fruit and vegetables", but the pill in play is FRUIT alone. Same file's _pres t1 and WAGOLL text.

**P36 · BUILD_ASDAN/FoodWise/FW_W1_Food_Groups.html** (B-spelling, both; WRONG)
- Current: “Today is 'Food Groups' — the eatwell guide. What do you think we'll be doing?”
- Issue: Arrival Task (standard tier, on-screen slide and print-arrival pack) writes the proper noun "Eatwell Guide" in lower case; every other surface in the suite capitalises it.
- Proposed: Today is 'Food Groups' — the Eatwell Guide. What do you think we'll be doing? (two occurrences: #arrival-standard and print-arrival standard-content)
- Source: NHS/PHE proper noun "Eatwell Guide"; SoW W1 subtitle "The Eatwell Guide"; the same file's KO table entry "EATWELL GUIDE".

**P37 · BUILD_ASDAN/FoodWise/FW_W1_Food_Groups.html** (C-construction, print; WRONG)
- Current: “Milk, cheese, yoghurt — calcium for bones and… · The builder group — meat, fish, eggs, beans. · The fuel group — bread, pasta, rice, potatoes. · The UK guide plate showing how much of each g…”
- Issue: The printed We Do 2 draw-lines worksheet truncates two of the six definitions mid-word ("bones and…", "each g…"), so the pupil-facing print pack carries cut-off sentences.
- Proposed: print the full definitions from the _pres pool: "Milk, cheese, yoghurt — calcium for bones and teeth." and "The UK guide plate showing how much of each group to eat."
- Source: Same file: _pres t3/t0 full texts at line 1615 vs the truncated print-wedo block at line 1438.

**P38 · BUILD_ASDAN/FoodWise/FW_W2_A_Balanced_Plate.html** (D-alignment, screen; MISALIGNED)
- Current: “Show your plate to a partner and name one healthy choice. Today's out…”
- Issue: The completion overlay repeats the SoW's W2 Lundy prompt, but the deck's own Lundy AUDIENCE box rules the opposite — "Partners hear the swap, not the plate — we discuss the choice, never anyone's eating" — so the deck issues two contradictory gallery instructions.
- Proposed: replace the overlay line with the deck's actual Voice prompt ("Say the one swap you would actually keep."); the SoW W2 row carries the show-your-plate wording and would need the same decision (SOW-SIDE origin).
- Source: BUILD_ASDAN/Scheme_of_Work.html Slot 4 W2 row vs the W2 Lundy slide's VOICE/AUDIENCE boxes in the same file.

**P39 · BUILD_ASDAN/FoodWise/FW_W2_A_Balanced_Plate.html** (D-alignment, both; MISALIGNED)
- Current: “We Do 1: Match it up”
- Issue: The print pack and the Starter card ("Today We Play: Match it up") — echoing START_HERE's and the SoW's settle sequence — promise a match-up settle, but the on-screen We Do 1 slide is "Make one swap", a tap-to-reveal game; the actual matching happens later in We Do 2.
- Proposed: rename the print heading and Starter card to "Make one swap" (or retitle the We Do 1 slide "Match it up" if the hub list is authoritative) so screen, print, hub and SoW agree.
- Source: Same file: We Do 1 h2 "Make one swap" vs print-wedo and Starter card; BUILD_ASDAN/FoodWise/START_HERE.html "Week 2 … · Match it up".

**P40 · BUILD_ASDAN/FoodWise/FW_W2_A_Balanced_Plate.html** (C-construction, screen; WRONG)
- Current: “Next lesson: Reading Labels — traffic lights. LABELSUGAR · LOWSALT · MEDFAT · HIGH”
- Issue: The completion modal's next-lesson keyword teaser has a missing separator producing the malformed token "LABELSUGAR" (the W3 label keywords are LABEL, SUGAR, LOWSALT, MEDFAT, HIGH).
- Proposed: Next lesson: Reading Labels — traffic lights. LABEL · SUGAR · LOWSALT · MEDFAT · HIGH
- Source: File-internal generator output; W3's ILM uses SUGAR / MED FAT / LOW SALT / HIGH as its label terms.

**P41 · BUILD_ASDAN/FoodWise/FW_W5_Prepare_a_Healthy_Snack.html** (C-construction, print; WRONG)
- Current: “EVERY DAY: The everyday drink — free, sugarless, doe… · EVERY DAY: Everyday — the defence group in snack form · SOMETIMES: Sometimes food — fine as a treat, not as…”
- Issue: The printed We Do 2 draw-lines worksheet truncates three of the six definitions mid-word ("doe…", "not as…", and later "a treat…"), leaving cut-off sentences on the pupil-facing print pack.
- Proposed: print the full _pres texts: "…free, sugarless, does the job", "…fine as a treat, not as a habit", "…salt and fat make it a treat slot".
- Source: Same file: _pres t0/t1/t3 full texts at line 1615 vs the truncated print-wedo block at line 1438.

**P42 · BUILD_ASDAN/Living_Independently/LI_W2_Notes_and_Coins.html** (A-qa, screen; WRONG)
- Current: “{"id":"i8","icon":"🪙","label":"£1 + £1 + 50p","answer":"b","reason":"This totals £2.50, so it does not match £2.35."}”
- Issue: In the shared ASDANVisualPayloads LI_W2 sort (We Do 1 rehearsal panel), item i8 totals £2.50 but its answer is category b (£2.35); the engine's renderSort place() greets that placement with 'Placed correctly.' plus a reason saying it does NOT match, and the activity cannot complete without it.
- Proposed: give i8 a genuine £2.35 build (e.g. label "50p + 50p + 50p + 50p + 20p + 10p + 5p", reason "The coins total 235p.") — edit in _framework/asdan-teach.js (blob is generated, byte-identical in all suite decks) and regenerate payloadSha256
- Source: Arithmetic (£1+£1+50p=£2.50 ≠ £2.35) + engine place() at the 'Placed correctly' branch in the same file's ASDAN-TEACH JS block

**P43 · BUILD_ASDAN/Living_Independently/LI_W5_A_Simple_Budget.html** (A-qa, screen; WRONG)
- Current: “{"min":3,"max":4,"label":"budget just balances","message":"The plan may work but has little room for change."}”
- Issue: The LI_W5 budget-simulator payload maps quality-point sums to bands that contradict the arithmetic pupils are taught to do: £25 income + £20 essentials + 'Spend £8 now' scores 3 → 'budget just balances', but 25−20−8 = −£3 (shortfall); £25 + £30 essentials + delay also scores 3 despite being £5 short.
- Proposed: band on the computed balance (income − essentials − optional) instead of additive quality, or rescore options so every negative-balance combination lands in 'budget shortfall risk' — fix in _framework/asdan-teach.js and regenerate payloadSha256
- Source: Arithmetic on the payload's own amounts vs engine scoring (score += option.quality; findOutcome min/max) in the same file's ASDAN-TEACH JS

**P44 · BUILD_ASDAN/Living_Independently/LI_W4_Everyday_Prices.html** (A-qa, screen; WRONG)
- Current: “{"min":5,"max":6,"label":"stronger value in this scenario","message":"Price, amount and access cost align."}”
- Issue: The LI_W4 comparator payload's additive scoring awards the top band to £1.80 + 500 g + no travel (2+1+2=5) even though that is £3.60/kg — worse unit value than the £2.40 + 1 kg combination the deck's own I Do model teaches pupils to prefer (£2.40/kg); its prediction options also reference 'two offers' though the controls configure one offer and requiredRuns is 1.
- Proposed: make the top band require the better unit price (e.g. 500 g quality 0, or compute pence-per-kg incl. travel) — fix in _framework/asdan-teach.js and regenerate payloadSha256
- Source: Arithmetic: £1.80/500g = £3.60/kg vs £2.40/1kg = £2.40/kg; deck's own I Do 1 unit-price model in the same file

**P45 · BUILD_ASDAN/Living_Independently/LI_W1_Where_Money_Comes_From.html** (C-construction, screen; WRONG)
- Current: “making amounts. £1£250p20p£5”
- Issue: Lesson-complete modal's next-lesson teaser runs the W2 settle tokens together with no separators (should read £1 £2 50p 20p £5), and the same modal truncates the Lundy line mid-word ('Today's outcome goes onto th…').
- Proposed: "making amounts. £1 · £2 · 50p · 20p · £5" and complete the truncated line as "Today's outcome goes onto the Money-Smart Board." (generator caps the string)
- Source: Deck-internal: W2 deck's own cards are '£1', '£2', '50p', '20p', '£5 note' — teaser is a joined list

**P46 · BUILD_ASDAN/Living_Independently/LI_W6_Shopping_and_Change.html** (C-construction, screen; WRONG)
- Current: “report back. Today's outco…”
- Issue: Lesson-complete modal truncates the Lundy summary mid-word ('Today's outco…') on the pupil-facing celebration screen.
- Proposed: end the summary line at "…report back." (or complete it: "Today's outcome goes onto the Money-Smart Board.") — generator caps the string
- Source: Deck-internal: full Lundy line exists on the Lundy slide of the same file

**P47 · BUILD_ASDAN/Living_Independently/LI_W3_Needs_vs_Wants.html** (C-construction, both; WRONG)
- Current: “The first three are money IN; spending is mon…”
- Issue: Two We Do 2 match targets are truncated mid-word on the slide itself and again in the print pack ('…spending is mon…' and 'The first three are needs — trainers are a wa…'), so pupils read cut-off answer text.
- Proposed: restore the full sentences — "The first three are money IN; spending is money OUT" and "The first three are needs — trainers are a want" (full text exists in _pres in the same file)
- Source: Deck-internal: untruncated versions in the _pres pool (t0/t1) of the same file

**P48 · BUILD_ASDAN/Living_Independently/LI_W1_Where_Money_Comes_From.html** (C-construction, print; WRONG)
- Current: “What something costs — the number on the labe… · Money going OUT — every purchase, big or smal…”
- Issue: The print pack's 'We Do 2: Match the Word to the Real Amount' definitions are truncated mid-word on the pupil worksheet.
- Proposed: print the full definitions from _pres ("…the number on the label.", "…every purchase, big or small.")
- Source: Deck-internal: full definitions in the _pres pool of the same file

**P49 · BUILD_ASDAN/Living_Independently/LI_W5_A_Simple_Budget.html** (C-construction, print; WRONG)
- Current: “We Do 2: Needs Covered — What Does the £3 Buy?</h2><p>Draw lines to match:</p><p>Toothpaste · Fizzy drink · Bus pass · New game skin · Warm coat · Takeaway</p>”
- Issue: The print section is titled after the on-screen We Do 2 (£3 choices → consequences) but actually reprints the We Do 1 sort items with truncated NEED/WANT captions ('…big consequence…', '…it ear…'); the activity the class actually played never reaches the print pack.
- Proposed: regenerate the print We Do 2 from the deck's kw-pills/targets (SPEND ALL £3 FRIDAY … → consequence lines), or retitle the section as the We Do 1 sort and print the captions in full
- Source: Deck-internal: on-screen #kw-pills/.match-target pairs vs #print-wedo content in the same file

**P50 · BUILD_ASDAN/Living_Independently/LI_W5_A_Simple_Budget.html** (C-construction, screen; WRONG)
- Current: “What does 'Toothpaste' mean in your own words?”
- Issue: Cold Call 'We Do 1' Standard-tier stem is a template misfire — it inserts the first settle card label into a keyword-definition stem, producing an unusable question (define 'Toothpaste').
- Proposed: M:"Is toothpaste a need or a want — and why?"
- Source: Template calibration: W1's version ('What does 'MONEY' mean in your own words?') is coherent because W1's cards are keywords; W5's cards are shopping items

**P51 · BUILD_ASDAN/Living_Independently/LI_W2_Notes_and_Coins.html** (C-construction, both; WRONG)
- Current: “<strong>Stretch:</strong> make the same amount with the FEWEST coins possible.”
- Issue: Take-it-further tier adds no demand: the Standard/Stretch base task on the same slide is already 'Make three given amounts using the fewest coins' — tier parity broken (same text repeats on the title Aspire strip and the print Stretch worksheet).
- Proposed: give the stretch a distinct demand, e.g. "Stretch: build £4.99 two different ways, then prove which way uses fewer coins."
- Source: Deck-internal tier-parity check: Standard task text on the same Independent Work slide

**P52 · BUILD_ASDAN/Living_Independently/LI_W1_Where_Money_Comes_From.html** (D-alignment, both; MISALIGNED)
- Current: “<h2>Wordsearch — settle in</h2>”
- Issue: W1's settle is advertised as a wordsearch (deck slide title, print heading, START_HERE grid and the SoW's 'W1 wordsearch') but the activity is tap-to-reveal definition cards, and the print pack gives only a word list — no wordsearch grid exists anywhere.
- Proposed: retitle the activity (e.g. "Word cards — settle in") in deck, print, START_HERE and SoW, or add a real letter-grid wordsearch to the print pack
- Source: BUILD_ASDAN/Scheme_of_Work.html shared blueprint ('W1 wordsearch') and START_HERE.html vs the deck's actual pres-card mechanics

**P53 · BUILD_ASDAN/Living_Independently/LI_W2_Notes_and_Coins.html** (D-alignment, both; MISALIGNED)
- Current: “Say which coin you find hardest to recognise. Half the room usually says the same one.”
- Issue: Lundy VOICE prompt (also the KO 'Pupil voice' line in print) differs from the SoW's W2 Lundy line 'Show a partner an amount and have them name it.' — which the deck's own lesson-complete modal quotes, so slide/KO and modal/SoW disagree inside one lesson.
- Proposed: pick one prompt per week and align Lundy slide, KO print, lesson-complete modal and the SoW row
- Source: BUILD_ASDAN/Scheme_of_Work.html Slot 3 W2 Lundy line + the deck's lc-summary in the same file

**P54 · BUILD_ASDAN/Living_Independently/LI_W3_Needs_vs_Wants.html** (D-alignment, both; MISALIGNED)
- Current: “Say one thing you would defend as a need even if somebody argued. You do not have to say why.”
- Issue: Lundy VOICE prompt (and KO 'Pupil voice') differs from the SoW's W3 Lundy line "Decide one 'want' you could wait for — why?" which the deck's lesson-complete modal quotes.
- Proposed: align Lundy slide, KO print, lesson-complete modal and SoW to one prompt
- Source: BUILD_ASDAN/Scheme_of_Work.html Slot 3 W3 Lundy line + the deck's lc-summary

**P55 · BUILD_ASDAN/Living_Independently/LI_W5_A_Simple_Budget.html** (D-alignment, both; MISALIGNED)
- Current: “Say the first thing you would protect if money got tight. “Pass” is fine on this one.”
- Issue: Lundy VOICE prompt (and KO 'Pupil voice') differs from the SoW's W5 Lundy line 'Show your budget to a partner and explain one choice.' which the deck's lesson-complete modal quotes.
- Proposed: align Lundy slide, KO print, lesson-complete modal and SoW to one prompt
- Source: BUILD_ASDAN/Scheme_of_Work.html Slot 3 W5 Lundy line + the deck's lc-summary

**P56 · BUILD_ASDAN/Living_Independently/LI_W6_Shopping_and_Change.html** (D-alignment, both; MISALIGNED)
- Current: “Say one thing that would make paying at a till easier for you.”
- Issue: Lundy VOICE prompt (and KO 'Pupil voice') differs from the SoW's W6 Lundy line "Name one real place you'll practise this — report back." which the deck's lesson-complete modal and Exit stretch Q3 use.
- Proposed: align Lundy slide, KO print, lesson-complete modal and SoW to one prompt
- Source: BUILD_ASDAN/Scheme_of_Work.html Slot 3 W6 Lundy line + the deck's lc-summary and exit-stretch

**P57 · GROW_ASDAN/Community_Project/GCOMM_W2_Choose_The_Need.html** (A-qa, screen; WRONG)
- Current: “👀 Look: many ideas in, one need out — real, doable, and ours.”
- Issue: I Do 1 model slide: the funnel SVG labels the three tests REAL? / DOABLE? / OURS? and the caption says 'real, doable, and ours', but everywhere else the deck teaches the third test as LASTING ('will it last') — KO (REAL/DOABLE/LASTING), arrival stretch ('Real, doable, lasting'), word bank, We Do 2 targets ('Lasting?'), cold-call pool.
- Proposed: change SVG pill text 'OURS?' to 'LASTING?' and the caption to '👀 Look: many ideas in, one need out — real, doable, and lasting.'
- Source: Internal consistency of the same deck (KO table line 420, arrival stretch line 349, word bank line 434, We Do 2 line 386) and SoW kit list 'scoring grids (three tests)' in GROW_ASDAN/Scheme_and_Resources.html

**P58 · GROW_ASDAN/Community_Project/GCOMM_W5_Risk_And_Ready.html** (C-construction, both; WRONG)
- Current: “STOP AND FIX: High impact uncontrolled — stop and fix b…”
- Issue: We Do 2: all six match targets are truncated mid-word with an ellipsis on the slide (line 386) and again in the print pack's 'Draw lines to match' list (line 426) — e.g. 'stop and fix b…', 'supervision is the mas…', 'non-negot…', 'expen…' — pupils match against cut-off sentences.
- Proposed: restore the full captions that already exist in the same file's _pres pool (line 602), e.g. 'STOP AND FIX: High impact uncontrolled — stop and fix before anything else', in both the on-screen targets and the print list.
- Source: Full untruncated texts present in the same file's _pres reveal pool (line 602); generator sliced at ~55 chars

**P59 · GROW_ASDAN/Community_Project/GCOMM_W1_Our_Patch_Our_Say.html** (C-construction, both; WRONG)
- Current: “<h2>Wordsearch — settle in</h2>”
- Issue: We Do 1 is titled 'Wordsearch — settle in' (also on the Starter card, line 354, and the print pack heading, line 425) but the activity is a tap-to-reveal definition-card game, and the print pack prints only the eight words with no wordsearch grid — the named activity does not exist on any surface.
- Proposed: rename the activity on all three surfaces (e.g. 'Word cards — settle in'), or supply an actual wordsearch grid in the print pack.
- Source: Same deck: We Do 1 mechanic is presTap cards revealing definitions (_pres pool line 602); print-wedo section (line 425) prints only the word list; every other week names its game accurately (Match it up / Odd one out / P

**P60 · GROW_ASDAN/Community_Project/GCOMM_W6_Green_Light.html** (B-spelling, both; WRONG)
- Current: “Today is 'Green Light' — plan → sign-off → aut 2 delivery. What do you think we'll be doing?”
- Issue: Arrival Task, standard tier (slide line 348 and print pack line 424): 'aut 2' is lower-case; the deck capitalises 'Aut 2' everywhere else (title strip, success criteria, exit ticket, lc-summary).
- Proposed: 'plan → sign-off → Aut 2 delivery' (capitalisation only; occurs twice — screen and print).
- Source: House usage in the same file and START_HERE.html ('Aut 2 delivery', 'Aut 2 delivers'); learner-task text so not silently alterable

**P61 · GROW_ASDAN/Enterprise/ENT_W4_Money_In_Money_Out.html** (A-fact, screen; WRONG)
- Current: “The pessimist\'s version still clears by stall three.”
- Issue: The We Do 2 WAGOLL model answer contradicts the deck's own arithmetic: break-even is 24 sales at surveyed demand 12 a stall, so the pessimist's half-estimate (6 a stall) clears at stall FOUR, not three — as the same deck's exit-stretch key ('the decision point is stall four') and W6's arrival-stretch key ('decision point is stall four') both state.
- Proposed: change 'still clears by stall three' to 'still clears by stall four' (24 break-even ÷ 6 pessimist sales per stall = 4 stalls), keeping the WAGOLL consistent with the W4 exit key and W6.
- Source: Internal number check: WAGOLL costs £8+£14+£2=£24, price £1, break-even 24 sales, demand 12/stall (all in this file); ENT_W4 exit-stretch answer and ENT_W6 arrival-stretch answer both give 'stall four'.

**P62 · GROW_ASDAN/Enterprise/ENT_W2_Spot_The_Gap.html** (A-qa, print; WRONG)
- Current: “Games-loan crate · Custom cover service · Hot drinks stall · Refill station + branded bottles”
- Issue: The print-pack 'We Do 2: Match the Gap to the Evidence For It' offers ANSWER cards, not evidence — the on-screen We Do 2 matches each gap to an evidence line ('Three lunchtime incidents logged in a fortnight' etc.), so the paper activity contradicts its own heading and duplicates We Do 1's gap-to-answer pairing.
- Proposed: replace the option list with the four on-screen evidence lines: 'Three lunchtime incidents logged in a fortnight · Nine planners in one form already falling apart by October · 14 of 20 parents said they stand in the cold at every pickup · A bin count: over forty bottles binned in one day'.
- Source: Same file: on-screen #wedo2 match targets vs #print-wedo second list; heading text 'Match the Gap to the Evidence For It'.

**P63 · GROW_ASDAN/Enterprise/ENT_W1_Helps_And_Earns.html** (A-qa, print; WRONG)
- Current: “We Do 2: Match the Word to the Business It Describes</h2><p>Draw lines to match:</p>”
- Issue: The print-pack We Do 2 heading promises matching words to businesses, but the printed options are dictionary definitions ('What's left after every cost is covered.' etc.), not the six business scenarios used on screen ('£18 in, £7 out — the £11 that's left' etc.).
- Proposed: either retitle the print heading 'Match the Word to its Definition', or replace the definition list with the six on-screen business scenarios so paper matches screen.
- Source: Same file: on-screen #wedo2 targets vs #print-wedo definitions list under the quoted heading.

**P64 · GROW_ASDAN/Enterprise/ENT_W3_Our_Idea_Our_Users.html** (C-construction, print; WRONG)
- Current: “Three gates every idea must pass — cool-but-i… · The one sentence that answers 'why us?' — and survives being challenged”
- Issue: Two of the four print-pack We Do 2 match options are ellipsis-truncated mid-word ('cool-but-i…' and 'Three people every enterprise has — bystander…'), so pupils on paper get incomplete option text; the full versions exist in the on-screen _pres reveal strings.
- Proposed: complete the two truncated options from the on-screen texts: '…cool-but-impossible fails at the door.' and 'Three people every enterprise has — bystanders aren’t part of the model.'
- Source: Same file: #print-wedo option list vs the complete _pres t0/t1 reveal texts in the script pool.

**P65 · GROW_ASDAN/Enterprise/ENT_W5_Brand_And_Pitch.html** (C-construction, print; WRONG)
- Current: “WEAK PITCH: Audiences smell it — shown costs buy trus…”
- Issue: All six print-pack We Do 2 match options are ellipsis-truncated mid-word ('trus…', 'the ord…', ''the cold pi…', 'ramblin…', 'hiding it lo…', 'action — n…'), leaving pupils incomplete reasons to match; the full texts exist in the on-screen _pres reveal strings.
- Proposed: print the six full reason texts from the _pres pool (e.g. 'Audiences smell it — shown costs buy trust that praise can't').
- Source: Same file: #print-wedo option list vs the complete _pres t0–t5 reveal texts in the script pool.

**P66 · GROW_ASDAN/Enterprise/ENT_W6_Pitch_Day.html** (C-construction, print; WRONG)
- Current: “Gap · answer · who it helps · price · ask · Customer AND beneficiary — name both”
- Issue: In the print-pack We Do 2 the ' · ' character is both the separator between options and the internal separator of the first option (the five-part pitch shape), so the four answer options read as eight indistinguishable items on paper.
- Proposed: punctuate the first option internally with commas — 'Gap, answer, who it helps, price, ask' — so the four options separate cleanly.
- Source: Same file: #print-wedo answer list vs the four on-screen match targets (the first target is the single option 'gap · answer · who it helps · price · ask').

**P67 · GROW_ASDAN/Enterprise/ENT_W1_Helps_And_Earns.html** (C-construction, both; WRONG)
- Current: “Today We Play</h4><p>Wordsearch — settle in</p>”
- Issue: The Starter card, the We Do 1 slide title and the print pack all promise a 'Wordsearch', but the activity is a tap-the-card definitions game and the print pack prints only a bare word list — no wordsearch grid exists on any surface (W2–W6 game labels all match their mechanics; only W1 does not).
- Proposed: rename the game on all three surfaces to match the mechanic (e.g. 'Word cards — settle in'), or add an actual wordsearch grid to the print pack.
- Source: Same file: We Do 1 mechanic ('Say what you think each word means first. Then tap') and print line 'We Do 1: Wordsearch — settle in</h2><p>ENTERPRISE, PROFIT, …'; calibration: W2 'Match it up', W4 'Put it in order', W5 'S

**P68 · GROW_ASDAN/PEQ/PEQ_W6_Present_My_Progress.html** (D-alignment, screen; MISALIGNED)
- Current: “Three minutes is a ceiling not a target — a strong ninety seconds beats a padded three.”
- Issue: W6 TA Brief (Independent Work) tells staff to prefer a 90-second presentation, but the ComSk1 use-of-plan minimum is a presentation of AT LEAST 3 minutes (E3: ≥2 min) — the deck's own Standard task says "Deliver your three-minute progress presentation", and this is the estate's only presentation vehicle, so steering below 3 minutes understates the minimum and risks banking sub-threshold Communicat
- Proposed: "Three strong minutes, not a padded five — if this presentation may bank Communication, three minutes is the ASDAN floor (two at E3), so don't cut it short."
- Source: _passpq/SPEC_FACTS.md §15 ComSk1 (1.5.1): presentation ≥3 min; ComSkE3 ≥2 min; §18: Communication plan/use evidence expected via a challenge leading to another PEQ unit.

**P69 · GROW_ASDAN/PEQ/PEQ_W4_Managing_Myself.html** (C-construction, print; WRONG)
- Current: “<h2 style="margin-top:14px">We Do 2: Skip One Step — What Breaks Your Day?</h2><p>Draw lines to match:</p><p>Plan the day · Pack what I need · Arrive on time · Do the task · Review and log it</p><p>Step 3 · Step 4 · Step”
- Issue: Print pack We Do 2 offers bare ordinals ("Step 3 · Step 4 · …") as the match options, which cannot answer the heading's question (what breaks when you skip a step) and merely duplicates We Do 1's ordering task; the on-screen version matches steps to consequences.
- Proposed: replace the ordinal list with the five on-screen consequence lines ("Skip it and the day decides for you · Skip it and you spend the lesson borrowing · Skip it and you're catching up before you've begun · Skip it and the plan was decoration · Skip it and there's nothing to show the term happened").
- Source: Same file, on-screen We Do 2 match targets (internal consistency).

**P70 · GROW_ASDAN/PEQ/PEQ_W2_Goals_That_Work.html** (C-construction, screen; WRONG)
- Current: “Share one goal with a partner — a heard goal is twice as likely to ha…”
- Issue: Lesson-complete modal summary line is mechanically truncated mid-word ("ha…" for "happen") by an ~100-character cap on the board-prompt string.
- Proposed: complete the line ("…twice as likely to happen.") or shorten it to end at a word boundary within the cap.
- Source: Internal consistency — five sibling decks show the same capped pattern; W2/W3/W4/W6 cut mid-word.

**P71 · GROW_ASDAN/PEQ/PEQ_W3_Working_With_Others.html** (C-construction, screen; WRONG)
- Current: “Agree one team rule this class will actually keep — it becomes a stan…”
- Issue: Lesson-complete modal summary line is truncated mid-word ("stan…", presumably "standard" or "standing rule").
- Proposed: complete or re-trim the line at a word boundary, e.g. "Agree one team rule this class will actually keep."
- Source: Internal consistency — same ~100-char truncation mechanism as W2/W4/W6 lesson-complete summaries.

**P72 · GROW_ASDAN/PEQ/PEQ_W4_Managing_Myself.html** (C-construction, screen; WRONG)
- Current: “Say the one thing that most often derails your day — naming it out lo…”
- Issue: Lesson-complete modal summary line is truncated mid-word ("lo…" for "loud").
- Proposed: complete or re-trim at a word boundary, e.g. "Say the one thing that most often derails your day."
- Source: Internal consistency — same truncation mechanism across the six decks' lesson-complete summaries.

**P73 · GROW_ASDAN/PEQ/PEQ_W6_Present_My_Progress.html** (C-construction, screen; WRONG)
- Current: “Name the skill this course should push hardest next half term — the a…”
- Issue: Lesson-complete modal summary line is truncated mid-word ("the a…").
- Proposed: complete or re-trim at a word boundary, e.g. "Name the skill this course should push hardest next half term."
- Source: Internal consistency — same truncation mechanism across the six decks' lesson-complete summaries.

**P74 · LAUNCH_ASDAN/Community_Enterprise/COMM_W1_Identify_a_Community_Need.html** (D-alignment, print; MISALIGNED)
- Current: “<strong>Stretch (L2 standard):</strong> rank several community needs by impact and justify the top one, to a strong standard.”
- Issue: The print Stretch worksheet labels the stretch task "(L2 standard)" on a strand that banks an unlevelled ASDAN short course + AQA UAS — the SoW scopes "Stretch tier written to an L2 evidence standard" to the PEQ (Personal Effectiveness) strand only, so "L2" has no referent here; the same "Stretch (L2 standard):" label recurs in the print-worksheet-stretch section of all six COMM_W* decks.
- Proposed: change "Stretch (L2 standard):" to "Stretch:" (or "Stretch (strong standard):") in the print-worksheet-stretch block of all six COMM_W1–W6 decks; exact-search "Stretch (L2 standard):" hits one instance per file.
- Source: LAUNCH_ASDAN/Scheme_of_Work.html (L2-stretch parenthetical sits inside the Personal Effectiveness/PEQ sentence; Community strand rows say only "Banks the ASDAN short course named per week + AQA UAS") + SPEC_FACTS §2/§3 (

**P75 · LAUNCH_ASDAN/Careers/CAREERS_W1_Know_Myself_for_Work.html** (C-construction, both; WRONG)
- Current: “Wordsearch — work words”
- Issue: Starter tile, We Do 1 slide title and print pack all promise a wordsearch, but the on-screen activity is a tap-to-define card game ('Say what each word means, then tap to check') and #print-wedo prints only a comma-separated word list — no grid exists on any surface.
- Proposed: retitle all three occurrences 'Word cards — work words' (matching the actual mechanic), or add a real wordsearch grid to #print-wedo.
- Source: Same file — We Do 1 li-box instruction, presTap() reveal mechanic, #print-wedo content; calibrated against We Do 2, whose print 'Draw lines to match' does deliver the promised mechanic.

**P76 · LAUNCH_ASDAN/Careers/CAREERS_W2_The_World_of_Work_and_Its_Sectors.html** (C-construction, both; WRONG)
- Current: “Wordsearch — sectors”
- Issue: Same wordsearch mislabel as W1: the We Do 1 activity is a tap-to-define card game and the print pack prints only a word list, no grid; the run-together entry ENTRYROLE betrays a planned grid that was never built.
- Proposed: retitle the Starter tile, We Do 1 h2 and print h2 'Word cards — sectors' and unfuse ENTRYROLE → ENTRY ROLE, or add a real grid to #print-wedo.
- Source: Same file — We Do 1 li-box instruction, presTap() mechanic, #print-wedo content.

**P77 · LAUNCH_ASDAN/Careers/CAREERS_W3_Labour-Market_Information_and_Pathways.html** (C-construction, both; WRONG)
- Current: “Wordsearch — labour-market words”
- Issue: Same wordsearch mislabel: tap-to-define card game on screen, bare word list in print (including run-together ENTRYROLE), no grid anywhere.
- Proposed: retitle the three occurrences 'Word cards — labour-market words' and unfuse ENTRYROLE → ENTRY ROLE, or add a real grid to #print-wedo.
- Source: Same file — We Do 1 li-box instruction, presTap() mechanic, #print-wedo content.

**P78 · LAUNCH_ASDAN/Careers/CAREERS_W4_Meeting_an_Employer.html** (C-construction, both; WRONG)
- Current: “Wordsearch — encounter words”
- Issue: Same wordsearch mislabel: tap-to-define card game on screen, bare word list in print (including run-together THANKYOU), no grid anywhere.
- Proposed: retitle the three occurrences 'Word cards — encounter words' and unfuse THANKYOU → THANK-YOU, or add a real grid to #print-wedo.
- Source: Same file — We Do 1 li-box instruction, presTap() mechanic, #print-wedo content.

**P79 · LAUNCH_ASDAN/Careers/CAREERS_W5_Matching_My_Profile_to_Opportunities.html** (C-construction, both; WRONG)
- Current: “Wordsearch — matching words”
- Issue: Same wordsearch mislabel: tap-to-define card game on screen, bare word list in print, no grid anywhere.
- Proposed: retitle the three occurrences 'Word cards — matching words', or add a real grid to #print-wedo.
- Source: Same file — We Do 1 li-box instruction, presTap() mechanic, #print-wedo content.

**P80 · LAUNCH_ASDAN/Careers/CAREERS_W6_Setting_SMART_Careers_Targets.html** (C-construction, both; WRONG)
- Current: “Wordsearch — target words”
- Issue: Same wordsearch mislabel: tap-to-define card game on screen, bare word list in print (including run-together FIRSTSTEP), no grid anywhere.
- Proposed: retitle the three occurrences 'Word cards — target words' and unfuse FIRSTSTEP → FIRST STEP, or add a real grid to #print-wedo.
- Source: Same file — We Do 1 li-box instruction, presTap() mechanic, #print-wedo content.

**P81 · LAUNCH_ASDAN/Careers/CAREERS_W1_Know_Myself_for_Work.html** (D-alignment, print; MISALIGNED)
- Current: “<strong>Stretch (L2 standard):</strong> back each strength with a dated, checkable example to a professional standard.”
- Issue: The stretch print worksheet stamps '(L2 standard)' on a Careers short-course task; ASDAN Short Courses are unregulated and carry no RQF level, and the SoW confines 'L2 evidence standard' stretch language to the PEQ strand — on short-course evidence it reads to a moderator as a level claim.
- Proposed: drop the bracket → '<strong>Stretch:</strong> back each strength with a dated, checkable example to a professional standard.'
- Source: LAUNCH_ASDAN/Scheme_of_Work.html ('Stretch tier written to an L2 evidence standard' appears only in the PEQ paragraph); ASDAN Short Courses are unregulated, not RQF-levelled — verified knowledge.

**P82 · LAUNCH_ASDAN/Careers/CAREERS_W2_The_World_of_Work_and_Its_Sectors.html** (D-alignment, print; MISALIGNED)
- Current: “<strong>Stretch (L2 standard):</strong> describe how a sector might change in the future to a professional standard.”
- Issue: '(L2 standard)' on a short-course stretch worksheet — same misalignment as W1: the SoW's L2-evidence-standard language belongs to the PEQ strand only; short courses are unlevelled.
- Proposed: drop the bracket → '<strong>Stretch:</strong> describe how a sector might change in the future to a professional standard.'
- Source: LAUNCH_ASDAN/Scheme_of_Work.html PEQ paragraph; ASDAN Short Courses unlevelled — verified knowledge.

**P83 · LAUNCH_ASDAN/Careers/CAREERS_W3_Labour-Market_Information_and_Pathways.html** (D-alignment, print; MISALIGNED)
- Current: “<strong>Stretch (L2 standard):</strong> use two sources of labour-market information to compare options to a professional standard.”
- Issue: '(L2 standard)' on a short-course stretch worksheet — same misalignment as W1.
- Proposed: drop the bracket → '<strong>Stretch:</strong> use two sources of labour-market information to compare options to a professional standard.'
- Source: LAUNCH_ASDAN/Scheme_of_Work.html PEQ paragraph; ASDAN Short Courses unlevelled — verified knowledge.

**P84 · LAUNCH_ASDAN/Careers/CAREERS_W4_Meeting_an_Employer.html** (D-alignment, print; MISALIGNED)
- Current: “<strong>Stretch (L2 standard):</strong> follow up an employer encounter with a thoughtful thank-you to a professional standard.”
- Issue: '(L2 standard)' on a short-course stretch worksheet — same misalignment as W1.
- Proposed: drop the bracket → '<strong>Stretch:</strong> follow up an employer encounter with a thoughtful thank-you to a professional standard.'
- Source: LAUNCH_ASDAN/Scheme_of_Work.html PEQ paragraph; ASDAN Short Courses unlevelled — verified knowledge.

**P85 · LAUNCH_ASDAN/Careers/CAREERS_W5_Matching_My_Profile_to_Opportunities.html** (D-alignment, print; MISALIGNED)
- Current: “<strong>Stretch (L2 standard):</strong> weigh two opportunities against your profile and justify a choice to a professional standard.”
- Issue: '(L2 standard)' on a short-course stretch worksheet — same misalignment as W1.
- Proposed: drop the bracket → '<strong>Stretch:</strong> weigh two opportunities against your profile and justify a choice to a professional standard.'
- Source: LAUNCH_ASDAN/Scheme_of_Work.html PEQ paragraph; ASDAN Short Courses unlevelled — verified knowledge.

**P86 · LAUNCH_ASDAN/Careers/CAREERS_W6_Setting_SMART_Careers_Targets.html** (D-alignment, print; MISALIGNED)
- Current: “<strong>Stretch (L2 standard):</strong> link your target to a real pathway and justify each SMART part to a professional standard.”
- Issue: '(L2 standard)' on a short-course stretch worksheet — same misalignment as W1.
- Proposed: drop the bracket → '<strong>Stretch:</strong> link your target to a real pathway and justify each SMART part to a professional standard.'
- Source: LAUNCH_ASDAN/Scheme_of_Work.html PEQ paragraph; ASDAN Short Courses unlevelled — verified knowledge.

**P87 · LAUNCH_ASDAN/Careers/CAREERS_W1_Know_Myself_for_Work.html** (C-construction, print; WRONG)
- Current: “1) 1. Say it Name one thing you are good at.”
- Issue: Supported-tier Arrival print items fuse the auto-number, the on-screen card heading and the question with no separator ('1) 1. Say it Name…') — garbled on paper; the same pattern appears on all three supported items in every deck of this batch (18 lines total, one exemplar quoted).
- Proposed: drop the fused heading → '1) Name one thing you are good at.' — apply to items 2–3 here and to W2–W6 equivalents (locate with grep pattern '[0-9]) [0-9]\.').
- Source: Same files — #print-arrival supported-content vs the on-screen Arrival cards whose h3s ('1. Say it' etc.) were concatenated in; standard/stretch print items are clean, proving the intended format.

**P88 · LAUNCH_ASDAN/PEQ/PEQ_W6_Review_Progress_and_Sign_Off_the_Unit.html** (A-fact, both; WRONG)
- Current: “A review names a positive outcome, use of listening, an area to develop, and future use.”
- Issue: W6 (the ComSk1 review lesson) models a review with ONE positive outcome and ONE area to develop throughout, but ComSk1 1.6.1 requires at least 2 positive outcomes (1.6.1a) and at least 2 areas of further development (1.6.1e) — the W4/W5 staff panels in this same suite state the correct review minima that W6 then understates; the singular recurs in the title success criteria ('I can name what went 
- Proposed: sweep the recurrence list to plural minima, e.g. 'A review names two positive outcomes, use of listening, two areas to develop, and future use.' — and add the W4/W5 staff ComSk1-minima panel (or its Review line) to the W6 title slide.
- Source: SPEC_FACTS.md §15 Level 1 ComSk1 (pp38–39): ≥2 positives (1.6.1a) · ≥2 areas of further development (1.6.1e); also the deck estate's own W4/W5 staff panel 'Review: at least 2 positive outcomes and at least 2 areas of fur

**P89 · LAUNCH_ASDAN/PEQ/PEQ_W6_Review_Progress_and_Sign_Off_the_Unit.html** (D-alignment, both; MISALIGNED)
- Current: “Write a review of your communication: a positive outcome, use of listening, an area to develop, and future use.”
- Issue: The Standard independent task (repeated on the print worksheet and the witness-sheet STANDARD cell) produces only one positive outcome and one area to develop, so the task cannot evidence ComSk1 1.6.1 at the standard the deck banks ('ComSk1 — unit complete'); the Supported task and exit tickets have the same singular shape.
- Proposed: PROPOSED (ASDAN learner-task text — do not silently alter): 'Write a review of your communication: two positive outcomes, use of listening, two areas to develop, and future use.' — mirror in the print worksheet and witness-sheet cell.
- Source: SPEC_FACTS.md §15 ComSk1 1.6.1a/1.6.1e minima vs the deck's award-strip claim 'ASDAN PEQ Level 1 — Communication skills (ComSk1) — unit complete'.

**P90 · LAUNCH_ASDAN/PEQ/PEQ_W6_Review_Progress_and_Sign_Off_the_Unit.html** (A-fact, screen; WRONG)
- Current: “Reviewing my Communication unit honestly: a positive outcome was that my three-minute talk was clear and two questions were answered.”
- Issue: The W6 WAGOLL model answer (JS _wagollText, We Do 2) names one positive outcome and one area to develop ('My area to develop is speaking more slowly under pressure') and then declares 'the unit is complete and signed off' — a model that would fail ComSk1 1.6.1 minima at moderation.
- Proposed: extend the model to two positives and two areas, e.g. '…a positive outcome was that my three-minute talk was clear, and another was that two questions were answered well. My areas to develop are speaking more slowly under pressure and looking up from my notes.'
- Source: SPEC_FACTS.md §15 ComSk1 (pp38–39): ≥2 positives, ≥2 areas of further development.

**P91 · LAUNCH_ASDAN/PEQ/PEQ_W4_Plan_a_Communication_Activity.html** (A-fact, print; WRONG)
- Current: “Why must the plan be used over several weeks, not one lesson?”
- Issue: Print exit-ticket Stretch Q2 invents a mandatory weeks-long use requirement on ComSk1 (which has activity minimums, not a duration window — the deck's own staff panel says there is no 10-hour gate on Communication), and it diverges from the screen version of the same stem ('Why plan the activity across several weeks, not one lesson?').
- Proposed: align the print stem to the screen wording: 'Why plan the activity across several weeks, not one lesson?'
- Source: SPEC_FACTS.md §16 — the 10-hour plan-use window is absent from Communication; ComSk1 use = one activity (≥3-min talk / ≥8-min discussion / ≥250 words); screen/print parity within the same deck.

**P92 · LAUNCH_ASDAN/Vocational/VOC_W1_Introduction_to_Vocational_Skills_and_Workplaces.html** (C-construction, print; WRONG)
- Current: “1) 1. Say it Name a job that uses your hands.”
- Issue: Supported-tier Arrival Task print section (#print-arrival .supported-content) duplicates the ordinal and jams the on-screen card title into the question with no punctuation — all three lines read '1) 1. Say it …', '2) 2. Spot it …', '3) 3. Point to it …', while the standard/stretch print variants drop the card titles cleanly.
- Proposed: drop the embedded card ordinal/title or punctuate it, e.g. '1) Say it: Name a job that uses your hands.' (same treatment for lines 2 and 3); note the identical pattern exists in all 30 LAUNCH_ASDAN decks, so fix at generator/chassis level for consistency.
- Source: Internal consistency check: supported vs standard/stretch print-arrival blocks in the same file

**P93 · LAUNCH_ASDAN/Vocational/VOC_W2_Health_Safety_and_Hygiene_at_Work.html** (C-construction, print; WRONG)
- Current: “1) 1. Say it Name one safety rule at work.”
- Issue: Supported-tier Arrival Task print section duplicates the ordinal and concatenates the card title into the question without punctuation on all three lines ('1) 1. Say it', '2) 2. Spot it', '3) 3. Point to it'); standard/stretch variants are clean.
- Proposed: '1) Say it: Name one safety rule at work.' (and same for lines 2–3); chassis-wide pattern across all 30 LAUNCH_ASDAN decks.
- Source: Internal consistency check: supported vs standard/stretch print-arrival blocks in the same file

**P94 · LAUNCH_ASDAN/Vocational/VOC_W3_Following_Instructions_and_Routines.html** (C-construction, print; WRONG)
- Current: “1) 1. Say it Name one task that has steps you follow.”
- Issue: Supported-tier Arrival Task print section duplicates the ordinal and concatenates the card title into the question without punctuation on all three lines; standard/stretch variants are clean.
- Proposed: '1) Say it: Name one task that has steps you follow.' (and same for lines 2–3); chassis-wide pattern across all 30 LAUNCH_ASDAN decks.
- Source: Internal consistency check: supported vs standard/stretch print-arrival blocks in the same file

**P95 · LAUNCH_ASDAN/Vocational/VOC_W4_Teamwork_in_a_Vocational_Setting.html** (C-construction, print; WRONG)
- Current: “1) 1. Say it Name one job you could do in a team.”
- Issue: Supported-tier Arrival Task print section duplicates the ordinal and concatenates the card title into the question without punctuation on all three lines; standard/stretch variants are clean.
- Proposed: '1) Say it: Name one job you could do in a team.' (and same for lines 2–3); chassis-wide pattern across all 30 LAUNCH_ASDAN decks.
- Source: Internal consistency check: supported vs standard/stretch print-arrival blocks in the same file

**P96 · LAUNCH_ASDAN/Vocational/VOC_W5_Tools_Equipment_and_Safe_Use.html** (C-construction, print; WRONG)
- Current: “1) 1. Say it Name one tool used in a kitchen or garden.”
- Issue: Supported-tier Arrival Task print section duplicates the ordinal and concatenates the card title into the question without punctuation on all three lines; standard/stretch variants are clean.
- Proposed: '1) Say it: Name one tool used in a kitchen or garden.' (and same for lines 2–3); chassis-wide pattern across all 30 LAUNCH_ASDAN decks.
- Source: Internal consistency check: supported vs standard/stretch print-arrival blocks in the same file

**P97 · LAUNCH_ASDAN/Vocational/VOC_W6_Complete_a_Supported_Vocational_Task.html** (C-construction, print; WRONG)
- Current: “1) 1. Say it Name one vocational task you could finish today.”
- Issue: Supported-tier Arrival Task print section duplicates the ordinal and concatenates the card title into the question without punctuation on all three lines; standard/stretch variants are clean.
- Proposed: '1) Say it: Name one vocational task you could finish today.' (and same for lines 2–3); chassis-wide pattern across all 30 LAUNCH_ASDAN decks.
- Source: Internal consistency check: supported vs standard/stretch print-arrival blocks in the same file

**P98 · BUILD_ASDAN/BUILD_ASDAN_Hub.html** (D-alignment, doc; MISALIGNED)
- Current: “Unit and level attribution is the centre coordinator’s decision — nothing is promised to a learner.”
- Issue: BUILD is the only suite hub whose staff facts panel lacks the required partial-achievement line — GROW and LAUNCH panels both carry 'Partial achievement still certificates at unit level', BUILD's #peq-facts-panel (ending at the quoted anchor) does not.
- Proposed: append to the panel after the quoted sentence: ' Where a pupil is on PEQ, partial achievement still certificates at unit level.'
- Source: ECA-1 ASDAN brief (partial-achievement line must be present on suite hubs); SPEC_FACTS §3 (spec v1.2 §5.1 p9); presence proven on GROW/LAUNCH hub panels

**P99 · BUILD_ASDAN/Scheme_of_Work.html** (D-alignment, doc; MISALIGNED)
- Current: “<b>W7 My Career Profile</b> — Poster &amp; portfolio.”
- Issue: The Careers slot list jumps W5 → W7, omitting the Week 6 lesson 'What Happens After Year 11' (post-16 routes) that the page's own preamble ('Careers has a taught W6 (post-16 routes)') promises and the slot folder contains.
- Proposed: insert before the W7 line: <li><b>W6 What Happens After Year 11</b> — Four post-16 routes. Banks: ASDAN LI M8 / AQA UAS.</li> (wording to match the deck).
- Source: BUILD_ASDAN/Careers/START_HERE.html (Week 6 · What Happens After Year 11) and CAREERS_W7_After_Year_11.html <title> 'slot W6 · What Happens After Year 11'

**P100 · BUILD_ASDAN/Scheme_of_Work.html** (B-spelling, doc; WRONG)
- Current: “Banks: banks ASDAN LI M8 / AQA UAS.”
- Issue: Template artefact duplicates the word: every weekly bullet in all five slot lists reads 'Banks: banks …' (30 occurrences of 'Banks: banks' across the page).
- Proposed: delete the duplicated lowercase 'banks ' after the 'Banks:' label in all 30 bullets (e.g. 'Banks: ASDAN LI M8 / AQA UAS.').
- Source: grammar/house prose standard — duplication visible in rendered text

**P101 · BUILD_ASDAN/Scheme_of_Work.html** (B-spelling, doc; WRONG)
- Current: “like to explore next.</b>.”
- Issue: The full stop sits inside the bold Lundy prompt and again after it, rendering a double full stop ('next..'); the same pattern ends the Lundy sentence of every weekly bullet (~30 occurrences).
- Proposed: remove one of the two full stops (keep exactly one) on each weekly bullet's Lundy sentence.
- Source: grammar/house prose standard — double period visible in rendered text

**P102 · BUILD_ASDAN/Scheme_of_Work.html** (A-fact, doc; WRONG)
- Current: “<b>W2 A Kindness Challenge</b> — World Kindness Day.”
- Issue: This is an Autumn 1 scheme (W2 falls mid-September; even W8 ends by late-October half term) but World Kindness Day is 13 November and Anti-Bullying Week is mid-November — both Autumn 2 — so the W2 anchor and the Slot 6 header tag 'SMSC: Anti-Bullying Week, World Kindness Day' are out of season.
- Proposed: retheme W2 as a general kindness challenge (or 'ahead of World Kindness Day, 13 Nov') and move both SMSC anchors to the Autumn 2 plan; coordinate with Duke_and_Enterprise/DUKE_W2_A_Kindness_Challenge.html, which stages the lesson on the day itself (other batch).
- Source: World Kindness Day = 13 November; Anti-Bullying Week (UK) = mid-November — verified knowledge; English Autumn 1 half term ends late October. Calibration: FoodWise's 'World Food Day 16 Oct' anchor DOES fit Autumn 1

**P103 · Art_Teesside/Build/BUILD_ART_A2_W2_Arts_Inspiration.html** (C-construction, screen; WRONG)
- Current: “<h2>W</h2> <div class="li-box"><strong>How it works:</strong> e”
- Issue: The We Do 1 slide's heading and instruction line are truncated to 'W' and 'e' (compare W1's intact 'We Do: Tap the Surface' / full tap instruction), so the slide opens with garbage text.
- Proposed: <h2>We Do: Artist or Organisation?</h2> and instruction 'Tap each card to reveal who or what it is — and what you could take from them.' (matches this week's six cards: three artists, two organisations, the steal).
- Source: Internal comparison with W1 deck (intact pattern) and A1 deck BUILD_ART_W2 ('Tap each maker card to reveal what they do…'); same byte-identical truncation confirmed in W2–W7.

**P104 · Art_Teesside/Build/BUILD_ART_A2_W3_Stencil_Lab.html** (C-construction, screen; WRONG)
- Current: “<h2>W</h2> <div class="li-box"><strong>How it works:</strong> e”
- Issue: Same truncated We Do 1 heading/instruction ('W' / 'e') as W2 — the slide that introduces the six fault cards has no usable title or instruction.
- Proposed: <h2>We Do: Name the Fault</h2> and instruction 'Tap each card to reveal what went wrong — and the fix.' (TA brief for this slide: 'Six fault cards, five faults and one success. Make pupils name the FIX').
- Source: Internal comparison with W1 deck's intact We Do 1 slide; _taBriefs['We Do 1'] in the same file.

**P105 · Art_Teesside/Build/BUILD_ART_A2_W4_Audience_Week.html** (C-construction, screen; WRONG)
- Current: “<h2>W</h2> <div class="li-box"><strong>How it works:</strong> e”
- Issue: Same truncated We Do 1 heading/instruction ('W' / 'e') on the slide carrying the six review cards.
- Proposed: <h2>We Do: The Six Parts of a Shared View</h2> and instruction 'Tap each card to reveal what a real review needs — and why the last card matters most.' (TA brief: 'Card six is the one that matters').
- Source: Internal comparison with W1 deck's intact We Do 1 slide; _taBriefs['We Do 1'] in the same file.

**P106 · Art_Teesside/Build/BUILD_ART_A2_W5_Layer_and_Combine.html** (C-construction, screen; WRONG)
- Current: “<h2>W</h2> <div class="li-box"><strong>How it works:</strong> e”
- Issue: Same truncated We Do 1 heading/instruction ('W' / 'e') on the slide carrying the six layer cards.
- Proposed: <h2>We Do: Six Cards, Three Layers</h2> and instruction 'Tap each card to reveal what each layer does — and the two habits that stop mud.' (TA brief: 'Card 4 (drying) and card 5 (lifting back) are the two that prevent most disasters').
- Source: Internal comparison with W1 deck's intact We Do 1 slide; _taBriefs['We Do 1'] in the same file.

**P107 · Art_Teesside/Build/BUILD_ART_A2_W6_Resolve_and_Edition.html** (C-construction, screen; WRONG)
- Current: “<h2>W</h2> <div class="li-box"><strong>How it works:</strong> e”
- Issue: Same truncated We Do 1 heading/instruction ('W' / 'e') on the slide carrying the six edition-rule cards.
- Proposed: <h2>We Do: The Rules of a Set</h2> and instruction 'Tap each card to reveal what keeps five prints reading as one set.' (TA brief: 'Cards 1 and 2 prevent nearly every failure. Card 6 is the shrink line').
- Source: Internal comparison with W1 deck's intact We Do 1 slide; _taBriefs['We Do 1'] in the same file.

**P108 · Art_Teesside/Build/BUILD_ART_A2_W7_Bank_It_and_Plan_the_Teach.html** (C-construction, screen; WRONG)
- Current: “<h2>W</h2> <div class="li-box"><strong>How it works:</strong> e”
- Issue: Same truncated We Do 1 heading/instruction ('W' / 'e') on the slide carrying the six skill-sizing cards.
- Proposed: <h2>We Do: Size the Skill</h2> and instruction 'Tap each card to reveal whether it is the right size to teach in ten minutes.' (TA brief: 'Cards 5 and 6 are the deliberate wrong sizes. Make pupils say WHY').
- Source: Internal comparison with W1 deck's intact We Do 1 slide; _taBriefs['We Do 1'] in the same file.

**P109 · Art_Teesside/Build/BUILD_ART_A2_W2_Arts_Inspiration.html** (A-qa, screen; WRONG)
- Current: “onclick="selectKW(this,'m1')">✅ METHOD</div>”
- Issue: In We Do 2 (Method or Biography?) the three visually identical '✅ METHOD' pills carry hidden distinct ids (m1/m2/m3) and each target accepts only one of them, so a pupil who correctly classifies a statement as METHOD is marked '❌ Try again!' two times out of three.
- Proposed: give all three METHOD pills the id 'm' and all three BIOGRAPHY pills 'b', and set the six targets' data-correct to 'm'/'b' accordingly — pickTarget compares ids literally, so any METHOD pill then matches any method statement.
- Source: pickTarget() in the same file (el.getAttribute('data-correct')===selectedKWId); pills are indistinguishable on screen. Not DISTRACTOR-BY-DESIGN — the classification itself is correct but rejected.

**P110 · Art_Teesside/Build/BUILD_ART_A2_W4_Audience_Week.html** (A-qa, screen; WRONG)
- Current: “onclick="selectKW(this,'u1')">✅ USABLE</div>”
- Issue: In We Do 2 (Usable or Not?) the three identical '✅ USABLE' pills (u1/u2/u3) and three '❌ NOT USABLE' pills (n1/n2/n3) carry hidden distinct ids keyed to specific targets, so a correct usable/not-usable classification is rejected unless the pupil happens to tap the invisible matching pill.
- Proposed: same repair as W2 — collapse pill ids to 'u' and 'n' and set the six targets' data-correct to 'u'/'n'.
- Source: pickTarget() in the same file; pills are indistinguishable on screen.

**P111 · Art_Teesside/Build/BUILD_ART_A2_W1_Surface_Hunt.html** (C-construction, screen; WRONG)
- Current: “<li>I can record what I notice in my local area</li><li>I can choose materials or images that say 'Teesside' to me</li><li>I can explain one choice I made</li>”
- Issue: The Title-slide 'Success looks like' list, the 'Aspire · GROW reach: pair two finds that CONTRAST' line and the lesson-complete summary are byte-identical in ALL SEVEN A2 decks — copied from Autumn 1's The Local Canvas — so W1–W7 all display criteria that do not describe their lesson and contradict each deck's mid-point modal, which states different 'today's success criteria'.
- Proposed: write per-deck criteria (and matching lc-summary lines) derived from each deck's own mid-point prompt and enquiry — e.g. W1: 'I can take a rubbing that holds the detail · I can label where each rubbing came from · I can say which surface I will use again, and why'; likewise for W2–W7. Aspire line likewise per lesson.
- Source: BUILD_ART_W1_The_Local_Canvas.html carries the identical text while BUILD_ART_W3 (A1) has lesson-specific criteria, proving the suite intends per-lesson criteria; mid-point modals in each A2 deck state the real per-lesso

**P112 · Art_Teesside/Build/BUILD_ART_A2_W3_Stencil_Lab.html** (D-alignment, both; MISALIGNED)
- Current: “Cutting mats, safety blades and steel rules at ONE bench station, counted out.”
- Issue: The W3 deck (Title TA brief, I Do 1 'Cut on the mat, blade away from you, hand behind the line', Lundy SPACE 'Take a break from the blade', Independent-Work TA brief 'Count blades back in') runs a blade station, but the Autumn 2 SoW kit box states 'No press, no rollers, no inks, no blades beyond classroom scissors' and lists only scissors.
- Proposed: owner decision — either recut the W3 deck to scissors-only cutting (matching SoW, evidence pack and run sheets, which never mention blades), or amend the SoW kit line to admit the supervised blade bench per the House Standard scalpel card. The two documents currently promise different rooms.
- Source: Autumn2_Scheme_of_Work.html kit box ('no blades beyond classroom scissors'); House_Standard_and_Safety.html scalpel bench card (blades permitted estate-wide with counting rules).

**P113 · Art_Teesside/Build/BUILD_ART_A2_W7_Bank_It_and_Plan_the_Teach.html** (D-alignment, both; MISALIGNED)
- Current: “Needs a blade, so it needs supervision — pick it only if you can be supervised throughout.”
- Issue: The 'Cutting a bridge' skill card (We Do 1 _pres text and the print-wedo section, appears twice) presumes blades are unit kit, inheriting the same conflict with the SoW's 'no blades beyond classroom scissors' line.
- Proposed: resolve in the same direction as the W3 blade finding — if the unit stays scissors-only, reword to 'Needs careful scissor work, so cut it at the bench with an adult watching.'
- Source: Autumn2_Scheme_of_Work.html kit box; same conflict as W3 finding.

**P114 · Art_Teesside/Build/Scheme_of_Work.html** (D-alignment, doc; MISALIGNED)
- Current: “AQA UAS &#x27;Creating artwork&#x27;”
- Issue: The SoW subtitle claims a second accreditation (AQA Unit Award Scheme) alongside Trinity Explore, but the house standard is Trinity Arts Award only and no deck or pack in the suite references AQA.
- Proposed: delete " · AQA UAS &#x27;Creating artwork&#x27;" from the subtitle (or the owner confirms UAS is genuinely co-run and adds it consistently).
- Source: House_Standard_and_Safety.html §1.5 ("This provision runs Trinity Arts Award only") + BRIEF_ART house rule

**P115 · Art_Teesside/Build/Scheme_of_Work.html** (D-alignment, doc; MISALIGNED)
- Current: “no sorts or retrieval quizzes — which is the right pitch for Explore-supported pupils, so none were added”
- Issue: The SoW asserts the suite has no sorts or retrieval quizzes, but every one of the eight decks opens with a slide tagged "Retrieval Quiz" (tiered arrival grid) and carries two interactive tap/match sorting games (We Do 1 and We Do 2).
- Proposed: delete or reword the sentence to describe the decks as shipped (tiered retrieval arrival + two We Do interactives).
- Source: BUILD_ART_W1–W8 decks: slide-tag "Retrieval Quiz", presTap and match-pill/match-target games in each

**P116 · Art_Teesside/Build/Scheme_of_Work.html** (D-alignment, doc; MISALIGNED)
- Current: “A &quot;Not an art specialist? Say this&quot; cue”
- Issue: The "How these lessons were upgraded" section promises features that do not exist in any of the eight decks: the per-week "Not an art specialist? Say this" cue, the "📖 Reading toggle cycling Cream → Pink → Blue" dyslexia themes, the "animated Lundy loop ring", the spine band "on every lesson" (it exists only on the evidence-pack sheets), and an untouched "Calm Mode" (no Calm Mode exists in the dec
- Proposed: either build the missing cue/toggle/ring into the decks or rewrite these bullets to describe only what shipped (tinted Lundy zones, pack tickets, pack spine, BUILD→GROW ladder).
- Source: grep of all 8 decks + Art_Teesside/visual-learning/*.js: zero matches for specialist cue, Reading toggle/dyslexia, loop ring, Inherited/Feeds band, Calm Mode

**P117 · Art_Teesside/Build/START_HERE.html** (D-alignment, doc; MISALIGNED)
- Current: “Teesside-tinted Lundy zones + loop ring, per-week stamped tickets, a connecting spine, a BUILD&rarr;GROW ladder, non-specialist cues and dyslexia reading themes”
- Issue: The hub's "Upgraded build" note advertises a Lundy loop ring, non-specialist cues and dyslexia reading themes, none of which exist in the eight linked decks (tickets, spine and ladder exist only in the evidence pack).
- Proposed: trim the note to features actually present, e.g. "Teesside-tinted Lundy zones, per-week stamped tickets, a connecting spine and a BUILD→GROW ladder in the evidence pack".
- Source: grep of all 8 decks: zero matches for loop ring, specialist cue, Reading/dyslexia toggle

**P118 · Art_Teesside/Build/Printable_BUILD_Weekly_Evidence_Pack.html** (D-alignment, print; MISALIGNED)
- Current: “{"w": 3, "t": "Industrial Surface Skills Lab", "part": "Explore Part C"”
- Issue: The pack contradicts itself on Week 3's award part: the W3 sheet stamps "Explore Part C" (and its recovery route claims "the SAME award part"), while the pack's own Evidence Locator files "Week 3 · surface strips tried" under Part A and warns Part C "cannot double-count with the Part A evidence above"; the W3 deck says "Parts A+C" and the W2 sheet says "Part A + Part B" where the W2 deck says Part
- Proposed: pick one canonical part mapping for W2/W3 with the owner and align the WEEKS part labels, the locator rows and the deck award-strips to it.
- Source: Same file: LOCP Part A row "Week 3 &middot; surface strips tried" and Part C req "must be a DISTINCT activity"; BUILD_ART_W3 award-strip

**P119 · Art_Teesside/Build/BUILD_ART_W1_The_Local_Canvas.html** (D-alignment, screen; MISALIGNED)
- Current: “Sketchbooks + 4B pencils + fine-liners out; photo card packs on tables.”
- Issue: The Title-slide TA brief does not open with a non-specialist orientation note — the house rule requires every Title TA brief to orient a non-specialist first (the A2 decks all open "NON-SPECIALIST NOTE: no art expertise needed — …").
- Proposed: prepend a non-specialist opener, e.g. "NON-SPECIALIST NOTE: no art expertise needed — today is looking and labelling: one element per box, element + tool written under it. " before the existing text.
- Source: BRIEF_ART house rule; calibration: BUILD_ART_A2_W1/W2 Title briefs carry the required opener

**P120 · Art_Teesside/Build/BUILD_ART_W1_The_Local_Canvas.html** (C-construction, both; MISALIGNED)
- Current: “<h3>1. Look (Recall)</h3>”
- Issue: The Supported arrival grid is four Recall boxes (Look/Lines/Tools/Colour) with no Think box, breaking the 2×2 ladder rule (two Recall + at least one Think; box 4 should reach for greater depth) while Standard and Stretch each carry two Think boxes; the same four questions repeat in the print pack's supported arrival.
- Proposed: make box 4 a Think, e.g. "4. Colour (Think): Why might an artist choose rust — an 'ugly' colour — as a subject?" (slide + print-arrival supported).
- Source: House_Standard_and_Safety.html §1.1 recall ladder + BRIEF_ART arrival rule; calibration: W2/W4–W8 Supported arrivals each contain a Think box

**P121 · Art_Teesside/Build/BUILD_ART_W1_The_Local_Canvas.html** (C-construction, screen; WRONG)
- Current: “<div class="timer-display" id="timerDisplay">20:00</div>”
- Issue: The Independent Work widget displays 20:00 (and the slide is billed 20 min via data-timer="20") but the countdown constants are `timerTotal=900,timerLeft=900` — a 15-minute timer; identical mismatch in all eight weekly decks.
- Proposed: set timerTotal=1200,timerLeft=1200 (or change the initial display to 15:00) consistently in all eight decks.
- Source: Same file, shared JS block (line ~468); verified identical across W1–W8 by diff

**P122 · Art_Teesside/Build/BUILD_ART_W2_Artists_Makers_and_Teesside_Connections.html** (D-alignment, screen; MISALIGNED)
- Current: “Maker card packs + artist card frames on tables.”
- Issue: Title-slide TA brief does not open with the required non-specialist orientation note.
- Proposed: prepend e.g. "NON-SPECIALIST NOTE: no art expertise needed — this week is research: who the maker is, one method, and the steal sentence; Part B needs an organisation card too. ".
- Source: BRIEF_ART house rule; calibration: BUILD_ART_A2_W2 Title brief opener

**P123 · Art_Teesside/Build/BUILD_ART_W2_Artists_Makers_and_Teesside_Connections.html** (C-construction, screen; WRONG)
- Current: “What goes onto the Wall accepts any artist YOU rate — bring a name, a photo, a scre?”
- Issue: Two cold-call questions are garbled template injections — the Starter Standard question above, and the Lundy Standard question "How does your choice on the Wall accepts any artist YOU rate — bring a name, a photo, a scre shape what we do next?" — a truncated fragment of the SPACE box was pasted into the question slot, leaving nonsense a teacher would read aloud.
- Proposed: "What goes onto the Makers Wall?" and "How does your choice on the Makers Wall shape what we do next?".
- Source: _ccQuestions pool vs the Lundy SPACE box text in the same file

**P124 · Art_Teesside/Build/BUILD_ART_W3_Industrial_Surface_Skills_Lab.html** (D-alignment, screen; MISALIGNED)
- Current: “Six stations set BEFORE entry: wash, dry-brush, stipple, frottage (real brick/grate samples), scratch-back, layering.”
- Issue: Title-slide TA brief does not open with the required non-specialist orientation note.
- Proposed: prepend e.g. "NON-SPECIALIST NOTE: no art expertise needed — the lab runs on one rule: test on scrap, label technique + tool + verdict, move on. ".
- Source: BRIEF_ART house rule; calibration: A2 deck Title briefs

**P125 · Art_Teesside/Build/BUILD_ART_W3_Industrial_Surface_Skills_Lab.html** (C-construction, both; MISALIGNED)
- Current: “<h3>4. Safety (Recall)</h3>”
- Issue: The Supported arrival grid is Last week/Recall/Recall/Recall — no Think box — breaking the two-Recall-plus-at-least-one-Think ladder rule that every other tier and week meets; repeated in the print pack's supported arrival.
- Proposed: convert one box to a Think, e.g. "4. Safety (Think): Why do we count tools back in before anyone leaves?".
- Source: House_Standard_and_Safety.html §1.1 + BRIEF_ART arrival rule; calibration: W2/W4–W8 Supported arrivals

**P126 · Art_Teesside/Build/BUILD_ART_W3_Industrial_Surface_Skills_Lab.html** (D-alignment, both; MISALIGNED)
- Current: “Explore Parts A+C · Take Part + Create”
- Issue: The deck claims Week 3 evidences Parts A+C (title strip, KO header, evidence line, and "Best Strip … Part C evidence" starter card) while the evidence pack's W3 sheet says "Explore Part C" and the pack's locator files W3 strips under Part A with an explicit no-double-counting rule for Part C — three sources, three answers.
- Proposed: agree the canonical W3 part with the owner and align deck strip/KO/evidence line with the pack sheet and locator.
- Source: Printable_BUILD_Weekly_Evidence_Pack.html WEEKS[2].part and LOCP Part A/Part C rows

**P127 · Art_Teesside/Build/BUILD_ART_W3_Industrial_Surface_Skills_Lab.html** (D-alignment, both; MISALIGNED)
- Current: “Your bets + results decide which TWO techniques get deep-dive time in Week 6's Resolve lesson.”
- Issue: The Lundy INFLUENCE promise (repeated in the print Lundy table, and in the TA exit brief "Collect the bets vs results tally for the Week 6 vote") is never honoured: Week 6's deck contains no two-technique deep-dive and no vote — in a suite whose stated design is that influence promises must be paid back.
- Proposed: either add the class-chosen two-technique deep-dive to W6 (e.g. in I Do 1 / rescue cards) or reword W3's Influence to the feed W4 actually honours (materials and demonstrations kept available).
- Source: BUILD_ART_W6_Resolve_the_Artwork.html (read in full — no such content); suite loop-payback principle in Scheme_of_Work/START_HERE

**P128 · Art_Teesside/Build/BUILD_ART_W4_Build_the_Brief.html** (D-alignment, screen; MISALIGNED)
- Current: “Brief frames + last week's mounted strips out (pupils plan FROM their own results).”
- Issue: Title-slide TA brief does not open with the required non-specialist orientation note.
- Proposed: prepend e.g. "NON-SPECIALIST NOTE: no art expertise needed — a brief is four decisions: subject, one-word message, method from their own strips, plan; every box must be filled, none must be clever. ".
- Source: BRIEF_ART house rule; calibration: A2 deck Title briefs

**P129 · Art_Teesside/Build/BUILD_ART_W5_Critique_Test_and_Redirect.html** (D-alignment, screen; MISALIGNED)
- Current: “Works-in-progress out on tables BEFORE pupils sit; critique card frames + scrap paper stacked per trio.”
- Issue: Title-slide TA brief does not open with the required non-specialist orientation note.
- Proposed: prepend e.g. "NON-SPECIALIST NOTE: no art expertise needed — critique runs on the frame: owner speaks first, every comment names a WHERE and a WHY, doubts go to scrap. ".
- Source: BRIEF_ART house rule; calibration: A2 deck Title briefs

**P130 · Art_Teesside/Build/BUILD_ART_W6_Resolve_the_Artwork.html** (D-alignment, screen; MISALIGNED)
- Current: “Drying rack cleared, 3-metre line re-taped, rescue-card packs on tables.”
- Issue: Title-slide TA brief does not open with the required non-specialist orientation note.
- Proposed: prepend e.g. "NON-SPECIALIST NOTE: no art expertise needed — today's rule: finish the focal point first, leave the quiet areas alone, and 'enough' is declared out loud at the 3-metre line. ".
- Source: BRIEF_ART house rule; calibration: A2 deck Title briefs

**P131 · Art_Teesside/Build/BUILD_ART_W7_Curate_the_Showcase.html** (D-alignment, screen; MISALIGNED)
- Current: “Curation trolley in, hanging strips/tack ready, height-guide sticks cut, label cards + thick pens out.”
- Issue: Title-slide TA brief does not open with the required non-specialist orientation note.
- Proposed: prepend e.g. "NON-SPECIALIST NOTE: no art expertise needed — hanging is four checks: audience eye height, a hand-width of air, label beside the work, and can everyone reach it. ".
- Source: BRIEF_ART house rule; calibration: A2 deck Title briefs

**P132 · Art_Teesside/Build/BUILD_ART_W8_Share_Reflect_and_Close_the_Loop.html** (D-alignment, screen; MISALIGNED)
- Current: “Folders + the term's photo prints laid ready; four-photo row spaces marked on tables; sticky notes + staplers out; the recording corner set for testimonies.”
- Issue: Title-slide TA brief does not open with the required non-specialist orientation note.
- Proposed: prepend e.g. "NON-SPECIALIST NOTE: no art expertise needed — today is an audit, not art: point at the before/after pages, find gaps, fix one today. ".
- Source: BRIEF_ART house rule; calibration: A2 deck Title briefs

**P133 · Art_Teesside/Grow/GROW_ART_W8_Reflect_Audit_and_Close_the_Loop.html** (D-alignment, both; WRONG)
- Current: “Bronze needs evidenced time — the adviser audits it.”
- Issue: Arrival Task (Supported, box 4 'Hours') answer key states the adviser audits evidenced time, directly contradicting the House Standard ('the adviser audits parts, not attendance') and this suite's own pack locator ('There is no minimum-hours gate').
- Proposed: replace with 'Hours are guidance only — the adviser audits parts, not attendance; the log just shows the journey.' (stem 'Why do we log arts hours?' prints in the Supported pack too).
- Source: House_Standard_and_Safety.html §1.5 flag ('adviser audits parts, not attendance') + Printable_GROW pack locator ('There is no minimum-hours gate — Trinity states time figures are guidance only')

**P134 · Art_Teesside/Grow/GROW_ART_W8_Reflect_Audit_and_Close_the_Loop.html** (D-alignment, print; WRONG)
- Current: “<td>Hours log</td><td>The honest tally the adviser checks</td>”
- Issue: Printed Knowledge Organiser defines 'Hours log' as a tally the adviser checks — an hours-audit claim banned by the House Standard, on a pupil revision sheet.
- Proposed: '<td>Hours log</td><td>A guide to the journey — the adviser audits parts, not hours</td>'
- Source: House_Standard_and_Safety.html: 'The adviser audits parts, not attendance. Attendance volume must never be used to withhold a claim.'

**P135 · Art_Teesside/Grow/GROW_ART_W8_Reflect_Audit_and_Close_the_Loop.html** (D-alignment, screen; WRONG)
- Current: “your folder + hours go to the Arts Award adviser, who audits before any Bronze claim.”
- Issue: We Do 1 'Adviser handover' reveal (_pres adviser8) tells pupils their hours go to the adviser for audit — the hours-gate framing the house rules prohibit.
- Proposed: 'your folder goes to the Arts Award adviser, who audits the parts before any Bronze claim.'
- Source: House_Standard_and_Safety.html: adviser audits parts, not attendance; Trinity guided-learning figures are guidance only

**P136 · Art_Teesside/Grow/GROW_ART_W2_Studio_Skills_and_Safe_Practice.html** (C-construction, screen; WRONG)
- Current: “<span class="wagoll-tag" data-trigger="registration">📐 Registration</span>”
- Issue: WAGOLL badge trigger 'registration' never occurs in W2's _wagollText, so the '📐 Registration' badge can never reveal during or after typing.
- Proposed: either add a registration clause to _wagollText (e.g. '…taped for registration so my prints align…') or retarget the tag to a phrase the text contains.
- Source: Same file _wagollText (no 'registration'); _wagollCheckTags only shows tags whose trigger appears in the text

**P137 · Art_Teesside/Grow/GROW_ART_W1_The_Local_Canvas.html** (D-alignment, screen; MISALIGNED)
- Current: “"Title": "Blank map sheets + local print-map extracts + clipboards ready.”
- Issue: Title-slide TA brief opens with kit logistics, not the required non-specialist orientation (house rule: _taBriefs Title must orient a non-specialist first; the SoW also claims a per-week non-specialist cue that no GROW deck carries).
- Proposed: prepend a non-specialist opener, e.g. 'NON-SPECIALIST NOTE: no art expertise needed — today is choosing and reasoning, not drawing skill. Then: blank map sheets + …' (pattern from BUILD_ART_A2 decks).
- Source: Art suite house rule (Title TA brief must open non-specialist) + Grow/Scheme_of_Work.html claim; positive control Build/BUILD_ART_A2_W1_Surface_Hunt.html 'NON-SPECIALIST NOTE: no art expertise needed'

**P138 · Art_Teesside/Grow/GROW_ART_W2_Studio_Skills_and_Safe_Practice.html** (D-alignment, screen; MISALIGNED)
- Current: “"Title": "Stencil stations set: cutting tables”
- Issue: Title-slide TA brief does not open with a non-specialist orientation (house rule for this non-specialist-taught suite).
- Proposed: prepend a non-specialist opener before the station list (e.g. 'NON-SPECIALIST NOTE: no art expertise needed — the safety script and one-variable rule carry the lesson.').
- Source: Art suite house rule + Grow/Scheme_of_Work.html 'Not an art specialist? Say this' claim

**P139 · Art_Teesside/Grow/GROW_ART_W3_Independent_Studio_Challenge.html** (D-alignment, screen; MISALIGNED)
- Current: “"Title": "Full studio open per the ballot's stock. Log sheets on every table”
- Issue: Title-slide TA brief does not open with a non-specialist orientation.
- Proposed: prepend a non-specialist opener (e.g. 'NON-SPECIALIST NOTE: no art expertise needed — you protect independence by asking, not showing.').
- Source: Art suite house rule + Grow/Scheme_of_Work.html claim

**P140 · Art_Teesside/Grow/GROW_ART_W4_Arts_Event_Attend_Capture_and_Review.html** (D-alignment, screen; MISALIGNED)
- Current: “"Title": "Event logistics on the board (venue/visiting artist, times, groups, venue rules).”
- Issue: Title-slide TA brief does not open with a non-specialist orientation.
- Proposed: prepend a non-specialist opener (e.g. 'NON-SPECIALIST NOTE: no art expertise needed — being an honest audience member is the skill this week.').
- Source: Art suite house rule + Grow/Scheme_of_Work.html claim

**P141 · Art_Teesside/Grow/GROW_ART_W5_Practitioner_Career_and_Inspiration.html** (D-alignment, screen; MISALIGNED)
- Current: “"Title": "Source packs out (practitioner interviews/bios — verified sources only)”
- Issue: Title-slide TA brief does not open with a non-specialist orientation.
- Proposed: prepend a non-specialist opener (e.g. 'NON-SPECIALIST NOTE: no art expertise needed — this is careers research; sourcing and honesty are the skills.').
- Source: Art suite house rule + Grow/Scheme_of_Work.html claim

**P142 · Art_Teesside/Grow/GROW_ART_W6_Plan_and_Rehearse_the_Skill_Share.html** (D-alignment, screen; MISALIGNED)
- Current: “"Title": "Control sheets from W2 back on tables (plans grow FROM them).”
- Issue: Title-slide TA brief does not open with a non-specialist orientation.
- Proposed: prepend a non-specialist opener (e.g. 'NON-SPECIALIST NOTE: no art expertise needed — chunking and calm rescue lines are teaching craft, not art craft.').
- Source: Art suite house rule + Grow/Scheme_of_Work.html claim

**P143 · Art_Teesside/Grow/GROW_ART_W7_Deliver_the_Skill_Share_and_Curate.html** (D-alignment, screen; MISALIGNED)
- Current: “"Title": "Room per the format vote. Learner groups scheduled + consent list CHECKED before entry.”
- Issue: Title-slide TA brief does not open with a non-specialist orientation.
- Proposed: prepend a non-specialist opener (e.g. 'NON-SPECIALIST NOTE: no art expertise needed — the pupils are the teachers today; you run consent, cameras and calm.').
- Source: Art suite house rule + Grow/Scheme_of_Work.html claim

**P144 · Art_Teesside/Grow/GROW_ART_W8_Reflect_Audit_and_Close_the_Loop.html** (D-alignment, screen; MISALIGNED)
- Current: “"Title": "Six audit stations labelled A/B/C/D/Hours/Handover”
- Issue: Title-slide TA brief does not open with a non-specialist orientation (and its station list bakes in the Hours-audit framing flagged separately).
- Proposed: prepend a non-specialist opener and rename the Hours station per the hours findings (e.g. stations A/B/C/D/Log/Handover).
- Source: Art suite house rule + Grow/Scheme_of_Work.html claim + House_Standard hours flag

**P145 · Art_Teesside/Grow/Scheme_of_Work.html** (D-alignment, doc; MISALIGNED)
- Current: “a 📖 Reading toggle that remembers each pupil&#x27;s choice”
- Issue: The 'How these lessons were upgraded' section describes a dark-mode 12-section suite with Reading themes (Cream/Pink/Blue), an animated Lundy loop ring and per-lesson spine bands — none of which exist in the shipped GROW decks (light 10-slide chassis, no toggle, no ring; spine/tickets live only in the printable pack).
- Proposed: rewrite the enhancement-layer section to describe the shipped build (light chassis, tinted Lundy grid, pack-side tickets/spine/ladder) or rebuild the decks to match — owner decision.
- Source: Grep of all 8 GROW decks: 0 hits for Reading/📖/Cream/dark theme/loop ring; positive control: tinted Lundy zones claim verified present

**P146 · Art_Teesside/Grow/Scheme_of_Work.html** (D-alignment, doc; MISALIGNED)
- Current: “Left deliberately untouched: his engine, his dark studio palette, his per-week visual explainers, and his Calm Mode.”
- Issue: The decks have no dark studio palette and no Calm Mode at all (no calm/reduced-motion toggle beyond the CSS prefers-reduced-motion block), so 'left untouched' misdescribes the shipped files; only the per-week visual explainers exist.
- Proposed: trim to what is true of the shipped decks (per-week visual explainers; prefers-reduced-motion support) or restore the described features.
- Source: Grep of all 8 GROW decks: 0 hits for 'Calm', no dark palette (body background #fff)

**P147 · Art_Teesside/Grow/Scheme_of_Work.html** (D-alignment, doc; MISALIGNED)
- Current: “A &quot;Not an art specialist? Say this&quot; cue”
- Issue: The SoW promises an exact-words non-specialist cue in each week's visual-explainer slide, but no GROW deck contains any such cue ('specialist' has zero hits across all 8 decks).
- Proposed: add the cue line to each deck's visual-explainer (.ilm caption) or remove/reword this bullet — pairs with the eight Title-TA-brief findings.
- Source: Grep of GROW decks (0 hits) vs positive control in Build A2 decks

**P148 · Art_Teesside/Grow/START_HERE.html** (D-alignment, doc; MISALIGNED)
- Current: “reading themes that add light Cream/Pink/Blue options over the studio dark”
- Issue: The hub's 'Upgraded build' note advertises a dark-mode suite with reading themes, loop ring and non-specialist cues that the linked GROW decks do not contain (Lundy tinting, ladder, tickets and spine exist only partly, in the printable pack).
- Proposed: reword the note to describe the shipped build, in step with the Scheme_of_Work fix.
- Source: Grep of all 8 GROW decks: 0 hits for reading themes/dark/loop ring/specialist cues

**P149 · Art_Teesside/Grow/GROW_ART_W6_Plan_and_Rehearse_the_Skill_Share.html** (D-alignment, both; MISALIGNED)
- Current: “Logistics vote: skill-share format next week — stations carousel or paired sessions? Your ruling configures the room.”
- Issue: The W6/W7 decks frame the delivery choice as carousel-vs-paired and never mention the Channel A/B/C system (live pair / skill station / hands-only video) that the evidence pack's Week 6-7 sheets, the Channel card and the hub all treat as a required, recorded choice ('My channel is A / B / C because ____').
- Proposed: teach the A/B/C channel menu in W6 (and mirror it in W7) or rewrite the pack's channel sheets to the decks' carousel/paired language — owner decision; quote appears twice in W6 (slide + print-lundy).
- Source: Printable_GROW pack W6 ticket + W7 'Channel used today' block + Channel card; START_HERE 'Skill Share: Pick Your Channel — Week 6 card'

**P150 · Art_Teesside/Launch/LAUNCH_ART_W1_Frame_the_Local_Challenge.html** (D-alignment, screen; MISALIGNED)
- Current: “Statement frames + A3 scrap stock + last term's Bronze folders available (baselines cite them).”
- Issue: Title-slide TA brief (_taBriefs["Title"]) opens with a kit list, not the required non-specialist orientation — art is not taught by a specialist and every Title TA brief must open with a non-specialist note (Build A2 decks all do).
- Proposed: prepend "NON-SPECIALIST NOTE: no art expertise needed — today is writing and one scrap test; hold pupils to the four-sentence frame. " before the existing text.
- Source: Art brief house rule (_taBriefs[0] must open non-specialist); calibration: Build/BUILD_ART_A2_W1–W7 Title briefs all open 'NON-SPECIALIST NOTE:'

**P151 · Art_Teesside/Launch/LAUNCH_ART_W1_Frame_the_Local_Challenge.html** (C-construction, both; MISALIGNED)
- Current: “<h3>4. Time (Recall)</h3><p>How many weeks does Unit 1 run?</p>”
- Issue: Supported arrival grid is four Recall boxes with no Think box, breaking the 2×2 recall-ladder standard (two Recall + at least one Think; box 4 synoptic) and tier parity — Standard/Stretch grids and W2/W5/W6/W8 Supported grids all carry a Think.
- Proposed: recast box 4 as a Think, e.g. '4. Size (Think): Why must a Silver challenge be demanding AND achievable?'
- Source: House_Standard_and_Safety.html §1.1 recall ladder + art brief arrival rule; calibration: W2/W5/W6/W8 supported grids contain a Think box

**P152 · Art_Teesside/Launch/LAUNCH_ART_W2_Practice_Careers_and_Pathways.html** (D-alignment, screen; MISALIGNED)
- Current: “Source packs (verified practitioner interviews, course pages, apprenticeship listings) + the careers shelf + outreach corner (approved contact list) ready.”
- Issue: Title-slide TA brief opens with logistics, not the required non-specialist orientation.
- Proposed: prepend "NON-SPECIALIST NOTE: no art expertise needed — this is research; the one rule is every question must change the making. "
- Source: Art brief house rule (_taBriefs[0]); calibration: Build A2 Title briefs

**P153 · Art_Teesside/Launch/LAUNCH_ART_W3_Implement_and_Critically_Develop.html** (D-alignment, screen; MISALIGNED)
- Current: “Clinic tables set per Week 1's hardest-parts vote, staffed/signed.”
- Issue: Title-slide TA brief opens with room set-up, not the required non-specialist orientation.
- Proposed: prepend "NON-SPECIALIST NOTE: no art expertise needed — hold the cycle v1 → judged → v2, photographed; the log does the art thinking. "
- Source: Art brief house rule (_taBriefs[0]); calibration: Build A2 Title briefs

**P154 · Art_Teesside/Launch/LAUNCH_ART_W3_Implement_and_Critically_Develop.html** (C-construction, both; MISALIGNED)
- Current: “<h3>4. Fix (Recall)</h3><p>Diagnosis before…?</p>”
- Issue: Supported arrival grid is 1 Last-week + 3 Recall with no Think box, breaking the 2×2 ladder standard (at least one Think; box 4 synoptic).
- Proposed: recast box 4 as a Think, e.g. '4. Fix (Think): Why diagnose before abandoning — what does plan B cost that a fix doesn't?'
- Source: House_Standard_and_Safety.html §1.1 + art brief arrival rule; anchors verified: 'time, decision, reason' and 'Diagnosis before abandonment' are taught in Grow/GROW_ART_W3

**P155 · Art_Teesside/Launch/LAUNCH_ART_W4_Arts_Experience_Attend_Analyse_and_Share.html** (D-alignment, both; WRONG)
- Current: “<td>The share</td><td>Outcome + analysis, public, two-way</td>”
- Issue: KO defines the 1C share as 'public', and the matching game pill '📤 The public share' (screen + print) repeats the framing; both write a public requirement into Silver.
- Proposed: KO row → '<td>The share</td><td>Outcome + analysis, known audience, two-way</td>'; rename pill/print text 'The public share' → 'The share'.
- Source: House rule; Printable pack Locator: 'A public showing is a GOLD requirement — welcome at Silver, never required'

**P156 · Art_Teesside/Launch/LAUNCH_ART_W4_Arts_Experience_Attend_Analyse_and_Share.html** (D-alignment, screen; MISALIGNED)
- Current: “Experience logistics live (venue/visiting show), assumption slips + seal envelopes ready, share floor plan drawn, invited audience confirmed, receipt cards stacked.”
- Issue: Title-slide TA brief opens with logistics, not the required non-specialist orientation.
- Proposed: prepend "NON-SPECIALIST NOTE: no art expertise needed — push every 'it's good' to a HOW three times; that is the whole lesson. "
- Source: Art brief house rule (_taBriefs[0]); calibration: Build A2 Title briefs

**P157 · Art_Teesside/Launch/LAUNCH_ART_W4_Arts_Experience_Attend_Analyse_and_Share.html** (C-construction, both; MISALIGNED)
- Current: “<h3>4. Share (Recall)</h3><p>How does Unit 1 end?</p>”
- Issue: Supported arrival grid is 1 Last-week + 3 Recall with no Think box, breaking the 2×2 ladder standard (at least one Think).
- Proposed: recast box 4 as a Think, e.g. '4. Share (Think): Why must the share be two-way to count?'
- Source: House_Standard_and_Safety.html §1.1 + art brief arrival rule

**P158 · Art_Teesside/Launch/LAUNCH_ART_W5_Design_the_Leadership_Project.html** (D-alignment, screen; WRONG)
- Current: “the inker teaches the roll, the greeter owns the welcome.”
- Issue: I Do 2 'shine moments' step gives a crew member the role of 'inker' teaching 'the roll' — rollers and printing inks are banned kit ('no press, no rollers... no block/screen inks'; the SoW: 'stencils, sponged acrylic and registered layers only').
- Proposed: 'the sponge lead teaches the double-dab, the greeter owns the welcome.'
- Source: Art brief kit bans + Launch Scheme_of_Work 'Media and the room' (no press, no rollers, no printing inks)

**P159 · Art_Teesside/Launch/LAUNCH_ART_W5_Design_the_Leadership_Project.html** (D-alignment, screen; MISALIGNED)
- Current: “Week 4's receipts + audit lines displayed (needs get cited FROM them). Plan frames, role-card blanks, permission checklists ready.”
- Issue: Title-slide TA brief opens with logistics, not the required non-specialist orientation.
- Proposed: prepend "NON-SPECIALIST NOTE: no art expertise needed — this is planning; hold every need to its evidence and every aim to a count. "
- Source: Art brief house rule (_taBriefs[0]); calibration: Build A2 Title briefs

**P160 · Art_Teesside/Launch/LAUNCH_ART_W6_Pilot_Lead_and_Adapt.html** (D-alignment, screen; MISALIGNED)
- Current: “Guinea-pig group scheduled + consent checked. Stopwatches/clipboards for data roles.”
- Issue: Title-slide TA brief opens with logistics, not the required non-specialist orientation.
- Proposed: prepend "NON-SPECIALIST NOTE: no art expertise needed — the pupils lead today; your job is consent, cameras and the clock. "
- Source: Art brief house rule (_taBriefs[0]); calibration: Build A2 Title briefs

**P161 · Art_Teesside/Launch/LAUNCH_ART_W7_Deliver_and_Curate_the_Arts_Project.html** (D-alignment, screen; MISALIGNED)
- Current: “Participant groups scheduled, consent list CHECKED, host staff briefed. Peg line + exit-path receipt station rigged.”
- Issue: Title-slide TA brief opens with logistics, not the required non-specialist orientation.
- Proposed: prepend "NON-SPECIALIST NOTE: no art expertise needed — leaders lead today; you evidence, protect close time, and guard dignity. "
- Source: Art brief house rule (_taBriefs[0]); calibration: Build A2 Title briefs

**P162 · Art_Teesside/Launch/LAUNCH_ART_W7_Deliver_and_Curate_the_Arts_Project.html** (C-construction, both; MISALIGNED)
- Current: “<h3>4. Crew (Recall)</h3><p>One signal your crew knows?</p>”
- Issue: Supported arrival grid is 1 Last-week + 3 Recall with no Think box, breaking the 2×2 ladder standard (at least one Think).
- Proposed: recast box 4 as a Think, e.g. '4. Crew (Think): Why introduce your crew as the experts?'
- Source: House_Standard_and_Safety.html §1.1 + art brief arrival rule

**P163 · Art_Teesside/Launch/LAUNCH_ART_W8_Review_Influence_and_Portfolio_Audit.html** (D-alignment, screen; MISALIGNED)
- Current: “Six stations labelled (1AB/1CD/2AB/2CD/2E/Hours+Handover). Folders, the year's photo prints, receipts bundles, sticky notes, the recording corner.”
- Issue: Title-slide TA brief opens with room set-up, not the required non-specialist orientation.
- Proposed: prepend "NON-SPECIALIST NOTE: no art expertise needed — this is an audit; walk folders station to station and hunt gaps. "
- Source: Art brief house rule (_taBriefs[0]); calibration: Build A2 Title briefs

**P164 · Art_Teesside/Launch/Scheme_of_Work.html** (D-alignment, doc; MISALIGNED)
- Current: “a 📖 Reading toggle cycling Cream → Pink → Blue”
- Issue: The enhancement-layer list claims features absent from every LAUNCH file: no Reading toggle/dyslexia themes, no 'animated Lundy loop ring', and no Calm Mode exists to be 'left untouched' (grep across all 11 Launch files finds none); the stamped tickets, spine and GOLD ladder exist only in the Evidence Pack, not 'on every lesson'.
- Proposed: either build the claimed layer into the decks or rewrite this section to describe only what shipped (tinted Lundy zones in decks; tickets/spine/ladder/diagnostics in the Evidence Pack).
- Source: Grep of all Launch files: no 'Reading', 'Cream', 'dyslexia', 'loop ring', 'stamped' or Calm Mode in any deck; pack carries spine/ticket/ladder

**P165 · Art_Teesside/Launch/Scheme_of_Work.html** (D-alignment, doc; MISALIGNED)
- Current: “in his CHEESE-LAYER slide”
- Issue: Claims a 'Not an art specialist? Say this' cue exists in the decks; no LAUNCH deck contains any non-specialist cue or the string 'specialist', and no CHEESE-LAYER slide exists.
- Proposed: add the non-specialist cue to the decks (see the eight Title TA-brief findings) or delete this bullet.
- Source: Grep: 'specialist'/'CHEESE' absent from all 8 LAUNCH decks; Build A2 decks show the house pattern

**P166 · Art_Teesside/Launch/START_HERE.html** (D-alignment, doc; MISALIGNED)
- Current: “a LAUNCH&rarr;GOLD ladder, non-specialist cues and dyslexia reading themes”
- Issue: Hub note advertises 'loop ring', 'non-specialist cues' and 'dyslexia reading themes' that exist in no LAUNCH file, and 'per-week stamped tickets + spine' that exist only in the Evidence Pack, not the lessons.
- Proposed: trim the note to features that shipped, or build the missing features; align wording with Scheme_of_Work once corrected.
- Source: Grep of all Launch files (no reading toggle, no loop ring, no non-specialist cue); Printable pack carries ticket/spine/ladder

## AMBIGUOUS / pitch / UNVERIFIED flags

**A1 · BUILD_ASDAN/Community_Project/COMM_W1_Choose_Our_Asset.html** (A-qa, screen; AMBIGUOUS)
- Current: “Somewhere to sit that wasn't there before”
- Issue: We Do 2 match-target keyed to BENEFIT (m4) also plausibly describes the ASSET itself (the bench), so a pupil can defensibly map two pills to it; the print pack avoids this by using 'The good our asset does, and for whom'.
- Proposed: reword the target to foreground the good done, e.g. 'The good it does — visitors can now rest', mirroring the print definition.
- Source: Same file: KO table defines BENEFIT as 'The good it does, and for whom'; print We Do 2 uses the unambiguous _pres wording

**A2 · BUILD_ASDAN/Community_Project/COMM_W3_Our_Team_Roles.html** (C-construction, screen; AMBIGUOUS)
- Current: “Three of these belong together and one does not. Talk it out, then tap to see if you called it right.”
- Issue: We Do 1 'Odd one out' instruction claims every card is an odd-one-out round, but cards t2 ('Documentarian') and t3 ('Relying on each other') are single-term definition cards whose reveals contain no odd-one-out.
- Proposed: reword the How-it-works line, e.g. 'Two cards hold odd-one-out rounds, two hold key words — talk each out before you tap.'
- Source: Internal — _pres t2/t3 reveals (line 1615) are definitions, not round answers, unlike t0/t1

**A3 · BUILD_ASDAN/Careers/CAREERS_W3_Skills_Employers_Want.html** (A-qa, both; AMBIGUOUS)
- Current: “data-correct="m0" onclick="pickTarget(this)">You can grow the first three — they're skills.”
- Issue: In 'Skill, or Not a Skill?' the target keyed to 'Blue eyes' describes 'the first three' of a list not shown on this slide, and 'Employers want people who stick at it.' (keyed to 'Gives up fast') is equally true of the pill 'Effort' — the sorter lacks exactly-one-correct-target.
- Proposed: reword targets to name their pill's concept (e.g. Blue eyes → "You're born with it and can't grow it — not a skill"; Gives up fast → "The opposite of what employers look for")
- Source: Exactly-one-correct-target rule (BRIEF_COMMON) applied to the four target texts vs four pills

**A4 · BUILD_ASDAN/Careers/START_HERE.html** (A-fact, screen; UNVERIFIED)
- Current: “banks ASDAN Living Independently M8 / AQA UAS”
- Issue: The mapping of a Careers module onto ASDAN Living Independently 'M8' cannot be verified against any committed authority (SPEC_FACTS covers PEQ only; no LI module list is in the repo), and the estate's own facts panel names 'Careers & Experiencing Work' as a banked Short Course — the code needs the coordinator's one-time confirmation, then propagation to all seven decks' award strips.
- Proposed: none until the coordinator confirms the module code (the hub's own note already requires this before teaching)
- Source: No committed ASDAN Short Course module list; START_HERE's PEQ facts panel and 'Confirm ASDAN module codes' note

**A5 · BUILD_ASDAN/Duke_and_Enterprise/DUKE_W1_Choose_My_Challenges.html** (A-fact, both; UNVERIFIED)
- Current: “The wall has witnesses — a pledge said out loud is twice as likely to happen.”
- Issue: The 'twice as likely' statistic (Lundy AUDIENCE box, on screen and in the printed Lundy Loop table) is presented as fact to pupils but I can find no supportable source for a 2x effect of spoken pledges; goal-commitment research shows an effect but not that multiplier.
- Proposed: soften to '…a pledge said out loud is far more likely to happen.'
- Source: Could not verify: no citable study supports a specific 2x figure for spoken pledges (goal-setting literature, e.g. Matthews 2015, shows smaller/other effects)

**A6 · BUILD_ASDAN/Duke_and_Enterprise/DUKE_W1_Choose_My_Challenges.html** (D-alignment, both; AMBIGUOUS)
- Current: “Evidence goes in your ASDAN portfolio — Documentarian photo + annotation + witness tick — AQA UAS 'Personal challenge'.”
- Issue: The evidence slot tells pupils the destination is 'your ASDAN portfolio' while the named bank is AQA UAS (a different awarding body); the same mixed wording recurs in all six decks and the print feedback sheets say 'Keep with your ASDAN portfolio' — a moderation-confusion risk the suite's own START_HERE panel is at pains to avoid ('AQA UAS — a separate product from PEQ').
- Proposed: 'Evidence goes in your portfolio — Documentarian photo + annotation + witness tick — banks AQA UAS 'Personal challenge'.' (mirror in W2–W6 and the feedback-sheet strapline).
- Source: START_HERE.html peq-facts-panel; SoW Slot 6 banking line; SPEC_FACTS.md preamble (ASDAN products vs other awarding bodies)

**A7 · BUILD_ASDAN/FoodWise/START_HERE.html** (A-fact, screen; UNVERIFIED)
- Current: “ASDAN FoodWise · M1 Healthy Eating (Aut1)”
- Issue: The FoodWise short-course module title "M1 Healthy Eating" and the challenge numbering used across all six decks ("challenge 1"–"challenge 4", "(practical)", "module complete") cannot be verified offline — SPEC_FACTS covers PEQ only and the FoodWise student book is not in the repo.
- Proposed: no text change; confirm module title and challenge numbers against the FoodWise student book (ASDAN member area) — the hub and SoW already direct staff to confirm codes before teaching.
- Source: SPEC_FACTS.md scope (PEQ spec v1.2 only); BUILD_ASDAN/Scheme_of_Work.html "Before you teach — confirm locally: Exact ASDAN module/challenge codes per slot".

**A8 · BUILD_ASDAN/FoodWise/FW_W1_Food_Groups.html** (C-construction, both; AMBIGUOUS)
- Current: “<h2>Wordsearch — settle in</h2>”
- Issue: The We Do 1 activity is named a wordsearch (slide h2, Starter card, print pack, START_HERE, SoW) but is actually a tap-to-reveal definition game, and the printed sheet gives only the bare word list under the heading "We Do 1: Wordsearch — settle in" with no grid to search.
- Proposed: either rename the activity (e.g. "Word cards — settle in") on slide, starter card and print, or add a real wordsearch grid to the print pack; keep the hub/SoW settle-activity list in step with whichever is chosen.
- Source: Same file: presTap mechanic and print-wedo block; BUILD_ASDAN/FoodWise/START_HERE.html settle list "(wordsearch → match-up → odd-one-out → sequence → sort → team quiz)".

**A9 · BUILD_ASDAN/FoodWise/FW_W1_Food_Groups.html** (C-construction, screen; AMBIGUOUS)
- Current: “Say one healthy food you'd like to try. Today's outcome goes onto the…”
- Issue: The lesson-complete modal's gallery line is truncated mid-sentence with an ellipsis; the same mechanical truncation appears in all six decks (W2 "Today's out…", W3 "goes…", W4 "goes onto…", W5 "onto the Bal…", W6 "outcome g…").
- Proposed: end each lc-summary gallery line at the sentence boundary (e.g. "…Say one healthy food you'd like to try.") in all six decks.
- Source: File-internal: lc-summary spans at line 1426 of each FW deck; full sentences exist on each deck's Lundy slide.

**A10 · BUILD_ASDAN/FoodWise/FW_W3_Reading_Labels.html** (C-construction, screen; AMBIGUOUS)
- Current: “Three of these belong together and one does not. Talk it out, then tap to see if you called it right.”
- Issue: The We Do 1 "Odd one out" instruction only describes cards 1–2 (Round 1 and Round 2); cards 3–4 ("Per 100g", "Amber you eat daily") are single concepts whose reveals are definitions, not odd-one-out rounds, so the stated rule doesn't fit half the activity.
- Proposed: soften the instruction (e.g. "Rounds 1–2: three belong together, one does not. The last two cards: say what each means before you tap.") or make cards 3–4 into real rounds.
- Source: File-internal: pres-pills at line 1378 vs _pres reveal texts at line 1615 ("The honest ruler — same measure on every pack", "Can outweigh a red you eat rarely — frequency counts").

**A11 · BUILD_ASDAN/Living_Independently/LI_W4_Everyday_Prices.html** (A-qa, screen; AMBIGUOUS)
- Current: “Own example — e.g. '3 for £3' on £1.05 items dressed as a deal; unit maths exposes it.”
- Issue: Exit Ticket stretch Q1's model answer gives a real bargain as its 'fake bargain' example: 3 × £1.05 = £3.15, so '3 for £3' genuinely saves 15p — unit maths confirms rather than exposes it.
- Proposed: "Own example — e.g. '3 for £3' on 95p items: the 'deal' charges 15p more than three singles — unit maths exposes it (and any multibuy costs more if you only needed one)."
- Source: Arithmetic: 3 × £1.05 = £3.15 > £3.00

**A12 · BUILD_ASDAN/Living_Independently/LI_W3_Needs_vs_Wants.html** (C-construction, screen; AMBIGUOUS)
- Current: “Three of these belong together and one does not. Talk it out, then tap to see if you called it right.”
- Issue: The We Do 1 'Odd one out' instruction only describes cards 1–2 (Round 1/Round 2); cards 'A phone' and 'Warm coat in January' are single discussion items whose reveals are verdicts, not odd-one-out rounds, so the instruction misdescribes half the activity.
- Proposed: "Rounds 1–2: three belong together and one does not. Cards 3–4: argue need or want — then tap to check."
- Source: Same file: _pres t2/t3 reveal texts are single-item verdicts, not rounds

**A13 · BUILD_ASDAN/Living_Independently/START_HERE.html** (A-fact, doc; UNVERIFIED)
- Current: “<b>Module:</b> ASDAN Living Independently · M1 Earning &amp; Spending Money (Aut1).”
- Issue: The module attribution 'M1 Earning & Spending Money' (which every deck's 'Banks: ASDAN LI M1 challenge n' strip inherits) cannot be verified against any committed authority — SPEC_FACTS.md covers the PEQ spec only, not Short Course module lists.
- Proposed: verify the module number/title against the ASDAN Living Independently student book and record the confirmation in the SoW (the hub already instructs staff to confirm codes)
- Source: _passpq/SPEC_FACTS.md scope (PEQ-only; no Short Course module tables) — could not verify from committed sources

**A14 · GROW_ASDAN/Community_Project/GCOMM_W3_Roles_Steps_Resources.html** (A-qa, both; AMBIGUOUS)
- Current: “data-correct="m0" onclick="pickTarget(this)">Three project habits — one project killer.”
- Issue: We Do 2: the target for 'Hogs every job' just repeats the slide title and names no distinguishing feature; both 'Hogs every job' (round 1) and 'Wing it' (round 2) are 'project killers', and the text that would separate them sits in the truncated m1 target — two pills plausibly fit this target.
- Proposed: reword the m0 target to describe hogging specifically, e.g. 'The team habit that kills projects — one person grabbing every job'.
- Source: BRIEF_COMMON exactly-one-correct-target rule; round sets on the same deck's We Do 1 slide (line 366)

**A15 · GROW_ASDAN/Enterprise/ENT_W6_Pitch_Day.html** (D-alignment, both; AMBIGUOUS)
- Current: “🏅 Banks: AQA UAS enterprise · ASDAN PEQ presentation + cross-unit project work cross-evidence”
- Issue: The banks strip could be read as claiming the relay pitch banks a PEQ 'presentation', but the modelled per-pupil pitch section is ~26 seconds (WAGOLL) — far short of the one-activity minimum for ComSk1 use-of-plan (presentation ≥3 min at L1, ≥2 min at E3), so a moderator-facing claim of 'presentation' evidence cannot be met by this task alone; the SoW W6 row carries the identical phrase.
- Proposed: keep the loose cross-evidence framing but drop the word 'presentation' (e.g. 'ASDAN PEQ communication cross-evidence'), or add a staff note that a ComSk1 1.5.1 claim needs a ≥3-minute presentation per learner; change the SoW W6 row in step if altered.
- Source: SPEC_FACTS.md §15 (ComSk1 pp38–39: presentation ≥3 min / discussion ≥8 min / text ≥250 words, ONE activity) and §18; WAGOLL in same file ('my numbers section at twenty-six seconds'); GROW_ASDAN/Scheme_and_Resources.html 

**A16 · GROW_ASDAN/Enterprise/ENT_W3_Our_Idea_Our_Users.html** (C-construction, screen; AMBIGUOUS)
- Current: “Three of these belong together and one does not.”
- Issue: The We Do 1 'Odd one out' instruction describes all four cards as odd-one-out rounds, but only cards 1–2 are rounds; cards 3–4 ('Customer vs beneficiary', 'USP') are concept cards whose taps reveal definitions, leaving pupils told to find an odd one where none exists.
- Proposed: reword the how-it-works line, e.g. 'Rounds 1–2: three belong together and one does not — call it before you tap. Cards 3–4: say what the term means, then tap to check.'
- Source: Same file: pres-card texts and _pres reveal strings (t2/t3 are definitions, not rounds).

**A17 · GROW_ASDAN/PEQ/START_HERE.html** (A-fact, screen; UNVERIFIED)
- Current: “Assessment records need assessor and learner signatures; IQA before EQA; the first-year EQA sampling visit is booked.”
- Issue: The staff facts panel asserts the mandatory first-year EQA sampling visit IS booked, but the committed authority explicitly keeps this open as an unconfirmed centre action.
- Proposed: change to "…IQA before EQA; the first-year EQA sampling activity must be booked within the first delivery year — confirm with the coordinator." (Same sentence also appears on GROW_ASDAN/Scheme_and_Resources.html, outside this batch.)
- Source: _passpq/COMPLIANCE_CHECKLIST.md PH-3 addendum (2026-08-18): "Item 6 stays open as written — confirm the first-year EQA sampling activity is booked"; SPEC_FACTS §10 (§12 p19).

**A18 · GROW_ASDAN/PEQ/PEQ_W2_Goals_That_Work.html** (A-fact, both; UNVERIFIED)
- Current: “A witnessed goal is twice as likely to land — that is the only reason it goes up.”
- Issue: Lundy AUDIENCE box (screen and print-lundy table) states an unsourced "twice as likely" multiplier as fact; the commonly cited accountability research (Matthews, Dominican University) shows roughly 76% vs 43% — well under 2× — and the lesson-complete summary repeats the claim ("a heard goal is twice as likely to ha…").
- Proposed: "A witnessed goal is far more likely to land — that is the only reason it goes up."
- Source: No source given in estate; Gail Matthews goal-accountability study (Dominican University of California) ≈76% vs 43% achievement — verified knowledge, under 2×.

**A19 · GROW_ASDAN/PEQ/PEQ_W6_Present_My_Progress.html** (C-construction, print; AMBIGUOUS)
- Current: “<p>Define it, then break it into steps · The Effectiveness Board — audit to evidence · Listening · building on ideas · sharing credit · A wish</p>”
- Issue: Print We Do 2 uses " · " both as the option separator and inside the option "Listening · building on ideas · sharing credit", so the four match options read as six on paper and cannot be reliably paired with the four prompts.
- Proposed: change the internal separators, e.g. "Listening, building on ideas, sharing credit", or separate options with line breaks.
- Source: Same file, on-screen We Do 2 target "Listening · building on ideas · sharing credit — name where you did one" (internal consistency).

**A20 · GROW_ASDAN/PEQ/PEQ_W5_Solving_Problems.html** (B-spelling, both; AMBIGUOUS)
- Current: “MAKES IT WORSE: Problems compound interest while you wait”
- Issue: Garbled grammar in the We Do 2 target and the matching reveal caption ("Problems compound interest…") — "compound" needs either no object ("problems compound") or a different verb ("gather interest").
- Proposed: "MAKES IT WORSE: Problems gather compound interest while you wait" (also update the _pres t1 caption to match).
- Source: Standard English grammar; appears twice in the file (match target and _pres pool t1).

**A21 · GROW_ASDAN/PEQ/PEQ_W3_Working_With_Others.html** (C-construction, screen; AMBIGUOUS)
- Current: “<strong>How it works:</strong> Three of these belong together and one does not. Talk it out, then tap to see if you called it right.”
- Issue: We Do 1 "Odd one out" instruction describes all four cards as odd-one-out rounds, but only t0 (Round 1) and t1 (Round 2) are; "Chairperson" and "Disagree with the idea" are vocabulary cards whose reveals are definitions, so the instruction misdescribes half the game.
- Proposed: "Rounds 1 and 2: three belong together and one does not — call it before you tap. Last two cards: say what the term means, then tap to check."
- Source: Same file, _pres pool (t2/t3 reveal definitions, not odd-one-out verdicts) — internal consistency.

**A22 · LAUNCH_ASDAN/Community_Enterprise/COMM_W1_Identify_a_Community_Need.html** (A-fact, both; UNVERIFIED)
- Current: “🏅 Banks: ASDAN Community / Active Citizenship — identify a need; AQA UAS ‘Contributing to the community’”
- Issue: Every banking claim in this suite names the short course "ASDAN Community / Active Citizenship", a slashed double title I cannot verify as a real ASDAN short-course product from any committed authority (SPEC_FACTS covers PEQ only; no instrument in _passpq lists the short-course roster); the label is estate-consistent (SoW, hub, all six decks), so if the title is wrong the error is SOW-SIDE as well
- Proposed: coordinator confirms the exact ASDAN short-course title being banked (candidates from ASDAN's roster: Enterprise, Volunteering, Citizenship) and the label is then normalised in one pass across Scheme_of_Work.html, LAUNCH_ASDAN_Hub.html and all six COMM_W* decks; no lesson-side edit before that confirmation.
- Source: _passpq/SPEC_FACTS.md (PEQ-only; silent on short-course titles); LAUNCH_ASDAN/Scheme_of_Work.html and LAUNCH_ASDAN_Hub.html carry the identical label; ASDAN short-course roster could not be checked offline

**A23 · LAUNCH_ASDAN/Community_Enterprise/COMM_W1_Identify_a_Community_Need.html** (C-construction, both; AMBIGUOUS)
- Current: “<h2>Wordsearch — community words</h2>”
- Issue: The We Do 1 activity is labelled "Wordsearch" on the Starter tile, the We Do 1 slide and the print pack, but the actual on-screen task is tap-a-card-to-reveal-definition ("Say what each word means, then tap to check") and the print pack prints only the bare word list with no wordsearch grid, so a pupil handed the pack cannot do the promised activity; the identical pattern recurs in W2 ("project-pl
- Proposed: either rename the activity to match the mechanic (e.g. "Word wall — community words") in the Starter tile, We Do 1 h2 and print h2 of all six decks, or supply an actual wordsearch grid in each print-wedo section; learner-task text, so not to be silently altered.
- Source: Internal consistency check: We Do 1 li-box instruction "Say what each word means, then tap to check" and print-wedo section (word list, no grid) versus the "Wordsearch" label, same structure verified in all six decks

**A24 · LAUNCH_ASDAN/Community_Enterprise/COMM_W1_Identify_a_Community_Need.html** (C-construction, print; AMBIGUOUS)
- Current: “<p>1) 1. Say it Name one thing that could be better near you.</p>”
- Issue: The Supported Arrival Task print block concatenates the print numbering, the on-screen card heading and the prompt with no punctuation, producing garbled double-numbered lines ("1) 1. Say it Name one thing…", "2) 2. Spot it…", "3) 3. Point to it…"); the same duplicated-numbering pattern appears in the print-arrival supported-content block of all six COMM_W* decks.
- Proposed: reformat each supported print-arrival line as "1) Say it — Name one thing that could be better near you." (dropping the duplicated card number, adding a dash) across all six decks; learner-facing print text, so not to be silently altered.
- Source: Internal comparison with the on-screen Arrival slide, where the heading ("1. Say it") and prompt are separate elements; the Standard/Stretch print blocks in the same section print cleanly with single numbering, proving t

**A25 · LAUNCH_ASDAN/Community_Enterprise/COMM_W6_Promote_Our_Project.html** (A-fact, screen; AMBIGUOUS)
- Current: “Promote kindly, in the spirit of Kindness and Anti-Bullying Week: share to inspire, not to boast.”
- Issue: W6 of Autumn 1 (mid-October) ties the lesson to "Kindness and Anti-Bullying Week", but Anti-Bullying Week (Anti-Bullying Alliance, UK) falls in the third week of November — Autumn 2 — and this estate's own SoW matrices pin Anti-Bullying Week tasks to Aut2 (_passsb/_passsg SOW_MATRIX "Aut2·W5/W6 (Anti-Bullying Week)"); the staff TA brief in the same file hardens the tie ("tying to Kindness and Anti
- Proposed: reword to "in the spirit of kindness — share to inspire, not to boast" or "ahead of Anti-Bullying Week in November" in both the I Do 1 step text and the _taBriefs "Independent Work" entry.
- Source: Anti-Bullying Week runs in the third week of November each year (Anti-Bullying Alliance) — verified knowledge; corroborated by /home/user/Lessons/_passsb/SOW_MATRIX.md and _passsg/SOW_MATRIX.md placing Anti-Bullying Week

**A26 · LAUNCH_ASDAN/Community_Enterprise/COMM_W6_Promote_Our_Project.html** (A-qa, both; AMBIGUOUS)
- Current: “‘A calm place to sit is ready for you’”
- Issue: In We Do 2 "Match the Audience to the Message", the RESIDENTS and OLDER NEIGHBOURS pills have cross-valid targets: older neighbours are residents, so "‘Your green space is clean and open again’" (keyed to RESIDENTS) and "‘A calm place to sit is ready for you’" (keyed to OLDER NEIGHBOURS) each read as correct for both pills — the only disambiguating cue is the W1 WAGOLL back-story ("older neighbour
- Proposed: make the RESIDENTS message explicitly whole-community (e.g. "‘Your green space is clean and open again — everyone welcome’") or replace one of the two pills with a non-overlapping audience, in both the slide and the print-wedo list.
- Source: Exactly-one-correct-target check on the sorter; calibration: the parallel sorters in W1, W3, W4 and W5 each pass the same check cleanly

**A27 · LAUNCH_ASDAN/Careers/CAREERS_W1_Know_Myself_for_Work.html** (A-qa, both; AMBIGUOUS)
- Current: “Full attendance an employer can check”
- Issue: In We Do 2 the STRENGTH pill has two defensible targets: the deck's own I Do 1 step 3 and WAGOLL define a strength via 'I kept full attendance', so this RELIABLE target is also a valid STRENGTH answer, and the auto-marker buzzes the defensible pairing.
- Proposed: reword the RELIABLE target (slide and print 'Draw lines to match' copy) to the deck's own We Do 1 definition, e.g. 'You do what you said, when you said — they can count on you', so only RELIABLE fits full attendance.
- Source: Same file — I Do 1 step 3 ('A strength is a skill you can prove... "I kept full attendance"'), _wagollText ('Strength: I kept full attendance last term'), _pres t5 definition.

**A28 · LAUNCH_ASDAN/Careers/CAREERS_W4_Meeting_an_Employer.html** (A-qa, both; AMBIGUOUS)
- Current: “Shows you are present and interested”
- Issue: In We Do 2 the EYE CONTACT and LISTEN targets overlap — 'Shows you are present and interested' and 'Shows you value what they are saying' each plausibly fit both pills (the I Do teaches 'eye contact, and listening' together without distinguishing), so a defensible pairing gets buzzed wrong.
- Proposed: make each target modality-specific, e.g. EYE CONTACT → 'Meeting their eyes shows you are focused on them', LISTEN → 'Letting them finish shows you value what they are saying' (slide and print copy).
- Source: Same file — We Do 2 targets m2/m3 vs I Do 1 step 2 ('a clear hello, eye contact, and listening').

**A29 · LAUNCH_ASDAN/Living_Independently/LI_W1_Self-Care_Routines_and_Organisation.html** (C-construction, screen; OVER-PITCHED)
- Current: “"Exit Ticket":{F:"Describe two parts of a good routine.",M:"Where does today\'s evidence bank?",H:"Describe how your routine flexes."}”
- Issue: Cold-call pool for the Exit Ticket slide inverts tier parity: the Supported (F) question is the Standard exit ticket's 'Describe two parts' (L1 'Describe' verb) while Standard (M) gets the easy recall 'Where does today's evidence bank?' — the supported exit ticket itself only asks 'say one part'.
- Proposed: swap F and M (F:"Where does today\'s evidence bank?", M:"Describe two parts of a good routine.") or ease F to "Say one part of a good routine."
- Source: Same file's exit-supported stems ('You can describe a self-care routine — true? Say one part.') vs exit-standard Q1; SPEC_FACTS §14 (E3 verbs State/Name vs L1 Describe); calibrated against non-exit CC rows where F is gen

**A30 · LAUNCH_ASDAN/Living_Independently/LI_W1_Self-Care_Routines_and_Organisation.html** (C-construction, both; AMBIGUOUS)
- Current: “Wordsearch — routine words”
- Issue: The We Do 1 activity is labelled 'Wordsearch' (Starter 'Today We Play', slide h2, and print 'We Do 1: Wordsearch — routine words') but is actually a tap-to-define word-card game, and the print pack supplies only a word list with no wordsearch grid to search.
- Proposed: rename to 'Word cards — routine words' on all three occurrences, or add a real wordsearch grid to the print pack (leave as is only if a physical wordsearch is issued separately in class).
- Source: Same file: We Do 1 mechanics ('Say what each word means, then tap to check') and #print-wedo content (word list only); pattern identical in W2–W6

**A31 · LAUNCH_ASDAN/Living_Independently/LI_W2_Home_Safety_and_Hazard_Awareness.html** (C-construction, screen; OVER-PITCHED)
- Current: “"Exit Ticket":{F:"Name two hazards and a safe action for each.",M:"Where does today\'s evidence bank?",H:"Set out an emergency plan for one hazard."}”
- Issue: Exit-Ticket cold-call tiers inverted: Supported (F) gets the Standard exit's two-part compound demand ('Name two hazards and a safe action for each') while Standard (M) gets the recall question; the supported exit ticket itself asks 'Name one'.
- Proposed: swap F and M, or ease F to "Name one home hazard."
- Source: Same file's exit-supported stems ('You can spot a home hazard — true? Name one.'); calibrated against this deck's non-exit CC rows where F is easiest

**A32 · LAUNCH_ASDAN/Living_Independently/LI_W2_Home_Safety_and_Hazard_Awareness.html** (C-construction, both; AMBIGUOUS)
- Current: “Wordsearch — safety words”
- Issue: We Do 1 is labelled 'Wordsearch' on screen and in print but is a tap-to-define card game; the print pack has only a word list, no grid.
- Proposed: rename to 'Word cards — safety words' (all occurrences) or add a wordsearch grid to the print pack.
- Source: Same file: We Do 1 mechanics and #print-wedo content

**A33 · LAUNCH_ASDAN/Living_Independently/LI_W3_Laundry_and_Household_Maintenance.html** (C-construction, screen; OVER-PITCHED)
- Current: “"Exit Ticket":{F:"Describe how you sort a wash and why.",M:"Where does today\'s evidence bank?",H:"Set out a weekly household schedule."}”
- Issue: Exit-Ticket cold-call tiers inverted: Supported (F) gets the Standard exit's 'Describe...and why' question while Standard (M) gets the recall question; supported exit asks 'true? Say how'.
- Proposed: swap F and M, or ease F to "Say one group you sort a wash into."
- Source: Same file's exit-supported stems ('You can sort laundry — true? Say how.'); non-exit CC rows show correct tiering

**A34 · LAUNCH_ASDAN/Living_Independently/LI_W3_Laundry_and_Household_Maintenance.html** (C-construction, both; AMBIGUOUS)
- Current: “Wordsearch — household words”
- Issue: We Do 1 labelled 'Wordsearch' on screen and in print but is a tap-to-define card game; print pack carries a word list, no grid.
- Proposed: rename to 'Word cards — household words' (all occurrences) or add a wordsearch grid to the print pack.
- Source: Same file: We Do 1 mechanics and #print-wedo content

**A35 · LAUNCH_ASDAN/Living_Independently/LI_W4_Keeping_a_Clean_Safe_Living_Space.html** (C-construction, screen; OVER-PITCHED)
- Current: “"Exit Ticket":{F:"Describe a simple cleaning routine.",M:"Where does today\'s evidence bank?",H:"Set out a weekly cleaning rota."}”
- Issue: Exit-Ticket cold-call tiers inverted: Supported (F) gets the Standard exit's 'Describe' question while Standard (M) gets the recall question; supported exit asks 'name a cleaning job — say one'.
- Proposed: swap F and M, or ease F to "Name one cleaning job."
- Source: Same file's exit-supported stems ('You can name a cleaning job — true? Say one.'); non-exit CC rows show correct tiering

**A36 · LAUNCH_ASDAN/Living_Independently/LI_W4_Keeping_a_Clean_Safe_Living_Space.html** (C-construction, both; AMBIGUOUS)
- Current: “Wordsearch — cleaning words”
- Issue: We Do 1 labelled 'Wordsearch' on screen and in print but is a tap-to-define card game; print pack carries a word list, no grid.
- Proposed: rename to 'Word cards — cleaning words' (all occurrences) or add a wordsearch grid to the print pack.
- Source: Same file: We Do 1 mechanics and #print-wedo content

**A37 · LAUNCH_ASDAN/Living_Independently/LI_W5_Personal_Admin_and_Responsibilities.html** (C-construction, screen; OVER-PITCHED)
- Current: “"Exit Ticket":{F:"Name two key documents.",M:"Where does today\'s evidence bank?",H:"Design a privacy routine."}”
- Issue: Exit-Ticket cold-call tiers inverted (mildest instance of the batch pattern): Supported (F) doubles the supported exit's demand ('Name two' vs 'Say one') while Standard (M) gets the easy recall question.
- Proposed: swap F and M, or ease F to "Name one key document."
- Source: Same file's exit-supported stems ('You can name a key document — true? Say one.'); non-exit CC rows show correct tiering

**A38 · LAUNCH_ASDAN/Living_Independently/LI_W5_Personal_Admin_and_Responsibilities.html** (C-construction, both; AMBIGUOUS)
- Current: “Wordsearch — admin words”
- Issue: We Do 1 labelled 'Wordsearch' on screen and in print but is a tap-to-define card game; print pack carries a word list, no grid.
- Proposed: rename to 'Word cards — admin words' (all occurrences) or add a wordsearch grid to the print pack.
- Source: Same file: We Do 1 mechanics and #print-wedo content

**A39 · LAUNCH_ASDAN/Living_Independently/LI_W6_Plan_and_Shop_for_a_Balanced_Meal.html** (A-qa, both; AMBIGUOUS)
- Current: “Carrots, apples — fill much of the plate”
- Issue: We Do 2 match has two defensible targets for two pills: the VEG & FRUIT target ('Carrots, apples — fill much of the plate') and the EVERYDAY FOOD target ('Foods most of the plate is built from') both describe everyday foods filling the plate, so a pupil pairing EVERYDAY FOOD with the carrots/apples card is marked wrong despite a defensible reading; same overlap in the printed draw-lines version.
- Proposed: reword the VEG & FRUIT target to remove the plate-share phrasing, e.g. 'Carrots, apples — vitamins and fibre', keeping 'Foods most of the plate is built from' unique to EVERYDAY FOOD.
- Source: Exactly-one-correct-target check; calibrated against W2's hazard match where all six pairs map uniquely

**A40 · LAUNCH_ASDAN/Living_Independently/LI_W6_Plan_and_Shop_for_a_Balanced_Meal.html** (D-alignment, screen; UNVERIFIED)
- Current: “Next lesson: Spring: Budgeting and Managing Money — practice money in more depth”
- Issue: Lesson-complete overlay points to a 'Spring: Budgeting and Managing Money' lesson that exists nowhere in the repo (the committed SoW covers Autumn 1 only, and the wording also skips Autumn 2), so the pointer cannot be verified.
- Proposed: verify against the year overview and reword (e.g. 'Next term: Budgeting and Managing Money') or point at the actual Autumn 2 strand content.
- Source: Grep across LAUNCH_ASDAN: the phrase occurs only in this file; LAUNCH_ASDAN/Scheme_of_Work.html is 'Autumn 1' only

**A41 · LAUNCH_ASDAN/Living_Independently/LI_W6_Plan_and_Shop_for_a_Balanced_Meal.html** (C-construction, screen; OVER-PITCHED)
- Current: “"Exit Ticket":{F:"Describe a balanced meal using the Eatwell groups.",M:"Where does today\'s evidence bank?",H:"How would you fit a smaller practice budget?"}”
- Issue: Exit-Ticket cold-call tiers inverted: Supported (F) gets the Standard exit's 'Describe... using the Eatwell groups' while Standard (M) gets the recall question; supported exit only asks 'Name one everyday food'.
- Proposed: swap F and M, or ease F to "Name one everyday food from your plate."
- Source: Same file's exit-supported stems ('You planned a balanced plate — true? Name one everyday food.'); non-exit CC rows show correct tiering

**A42 · LAUNCH_ASDAN/Living_Independently/LI_W6_Plan_and_Shop_for_a_Balanced_Meal.html** (C-construction, both; AMBIGUOUS)
- Current: “Wordsearch — food and shopping words”
- Issue: We Do 1 labelled 'Wordsearch' on screen and in print but is a tap-to-define card game; print pack carries a word list, no grid.
- Proposed: rename to 'Word cards — food and shopping words' (all occurrences) or add a wordsearch grid to the print pack.
- Source: Same file: We Do 1 mechanics and #print-wedo content

**A43 · LAUNCH_ASDAN/PEQ/PEQ_W4_Plan_a_Communication_Activity.html** (A-fact, both; AMBIGUOUS)
- Current: “Because it shows sustained, deliberate use of the skill — the standard the unit asks for.”
- Issue: Arrival Stretch Q1 answer attributes a sustained/weeks-long-use standard to the ComSk1 unit; the unit's use criterion is one activity meeting a time/word minimum, and the deck's own staff panel disclaims any duration gate on Communication — the weeks-long span is this scheme's delivery model (cross-challenge banking), not a unit standard.
- Proposed: 'Because it shows sustained, deliberate use of the skill — and one challenge can bank Communication alongside another PEQ unit.'
- Source: SPEC_FACTS.md §15 ComSk1 use minima and §16 (no 10-hour window on Communication); §18 cross-challenge evidence expectation.

**A44 · LAUNCH_ASDAN/PEQ/PEQ_W5_Deliver_the_Activity_and_Gather_Evidence.html** (A-fact, screen; AMBIGUOUS)
- Current: “Why must the plan show use across weeks?”
- Issue: Cold-call pool (_ccQuestions, 'Starter' H tier) frames weeks-long use as a requirement ('must') on the Communication unit; same invented-duration family as the W4 print stem — the deck's title-slide staff panel states there is no duration gate on ComSk1.
- Proposed: 'Why does showing use across weeks strengthen your evidence?'
- Source: SPEC_FACTS.md §16 — 10-hour/duration window absent from Communication; deck's own staff panel.

**A45 · LAUNCH_ASDAN/PEQ/PEQ_W5_Deliver_the_Activity_and_Gather_Evidence.html** (A-fact, screen; AMBIGUOUS)
- Current: “The least the unit accepts — 3 minutes or 250 words.”
- Issue: On-screen We Do 1 definition of MINIMUM (JS _pres t7) claims to state what 'the unit accepts' but omits the equally valid ≥8-minute discussion route; the deck's own print KO gives the complete rule ('3 minutes spoken, 8 minutes of discussion, or 250 words'), so screen and print disagree.
- Proposed: The least the unit accepts — a 3-minute talk, an 8-minute discussion, or 250 words.
- Source: SPEC_FACTS.md §15 ComSk1 1.5.1: presentation ≥3 min OR discussion ≥8 min OR text ≥250 words; W5 print KO MINIMUM row (complete version).

**A46 · LAUNCH_ASDAN/PEQ/PEQ_W1_Intro_and_Choosing_My_Level.html** (A-qa, both; AMBIGUOUS)
- Current: “Weighing reasons before you settle on an answer”
- Issue: We Do 2 match target for THINKING overlaps the DECISION definition the deck itself taught two slides earlier in We Do 1 ('Weighing choices and picking one you can explain'), so both this target and 'Choosing between options and saying why' are defensible matches for the DECISION pill — the sorter loses exactly-one-correct-target for a pupil using the taught definitions.
- Proposed: reword the THINKING target to mirror the deck's own We Do 1 definition, e.g. 'Working things out with reasons, not guesses' (update slide target, print 'Draw lines to match' list, and keep data-correct mapping).
- Source: Internal consistency: W1 We Do 1 _pres definitions (DECISION: 'Weighing choices and picking one you can explain'; THINKING: 'Working things out with reasons, not guesses') vs We Do 2 targets; ECA-1 exactly-one-correct-ta

**A47 · LAUNCH_ASDAN/Vocational/VOC_W6_Complete_a_Supported_Vocational_Task.html** (D-alignment, screen; UNVERIFIED)
- Current: “Next lesson: Spring: Horticulture and Enterprise — from garden to table”
- Issue: The W6 lesson-complete overlay points to a 'Spring: Horticulture and Enterprise' module that appears in no committed LAUNCH scheme (Scheme_of_Work.html covers Autumn 1 only), so the pointer — and the implication that the Vocational strand skips Autumn 2 — cannot be verified; it is, however, consistent with the house pattern (the W6 decks of Careers, Community and Living Independently all point to 
- Proposed: no change now; confirm the pointer when the Spring/next-half-term SoW is committed.
- Source: LAUNCH_ASDAN/Scheme_of_Work.html (Autumn 1 only, no Spring plan); calibration grep of 'Next lesson:' in all LAUNCH W6 decks (four strands all point to Spring modules)

**A48 · LAUNCH_ASDAN/Vocational/VOC_W1_Introduction_to_Vocational_Skills_and_Workplaces.html** (C-construction, print; AMBIGUOUS)
- Current: “['ko','intro','arrival','starter','wedo','exit','witness','feedback'].forEach”
- Issue: The 'Lundy Loop — this lesson' print sheet (#print-lundy), which carries pupil-completion lines ('What I said, and what it changed:') and the 'Closing the loop: this one ends on paper' instruction, is unreachable: printPack() never includes 'lundy' in its section list and printSection() is defined but never called from any button, so no print path can ever produce the sheet the deck tells pupils t
- Proposed: add 'lundy' to the printPack section array (chassis-wide change across the 30 LAUNCH decks), unless the exclusion is deliberate — in which case remove the dead #print-lundy sections.
- Source: Internal consistency: #print-lundy exists in every deck; grep shows no caller passes 'lundy' to printSection and printPack's id list omits it

**A49 · BUILD_ASDAN/BUILD_ASDAN_Hub.html** (D-alignment, doc; AMBIGUOUS)
- Current: “Each slot is a 6-lesson module (W1–6); Careers also has a taught W6 (post-16 routes); Week 8 is consolidation &amp; portfolio completion.”
- Issue: Footer sentence garbles the Careers structure: every slot already has a taught W6, and Careers actually runs SEVEN taught weeks — Week 6 = What Happens After Year 11 (post-16 routes), Week 7 = My Career Profile — so 'also has a taught W6' is self-contradictory and hides W7.
- Proposed: Each slot is a 6-lesson module (W1–6); Careers runs to W7 (post-16 routes at W6, My Career Profile at W7); Week 8 is consolidation &amp; portfolio completion.
- Source: BUILD_ASDAN/Careers/START_HERE.html (Week 6 · What Happens After Year 11; Week 7 · My Career Profile) and the lesson <title> tags (slot W6/W7)

**A50 · BUILD_ASDAN/Scheme_of_Work.html** (A-fact, doc; UNVERIFIED)
- Current: “ASDAN Living Independently · M1 Earning &amp; Spending Money (Aut1)”
- Issue: The short-course module numbers/titles asserted across the page (LI M1 'Earning & Spending Money', LI M8 for Careers, FoodWise M1 'Healthy Eating') cannot be verified — SPEC_FACTS covers PEQ only and no short-course booklet facts are committed; the page's own footer already says to confirm exact codes locally.
- Proposed: no text change; when confirming codes locally, check these module numbers/titles against the ASDAN short-course student books and correct here if they differ.
- Source: SPEC_FACTS scope (PEQ only); page's own 'Before you teach — confirm locally' instruction

**A51 · GROW_ASDAN/GROW_ASDAN_Hub.html** (A-fact, doc; UNVERIFIED)
- Current: “IQA before EQA; the first-year EQA sampling visit is booked.”
- Issue: The staff facts panel states the first-year EQA sampling visit 'is booked', but the committed compliance record still lists that booking as an open, unconfirmed centre action, and the spec ties the booking to a date once ≥1 unit is completed, assessed and IQA'd.
- Proposed: 'IQA before EQA; the first-year EQA sampling visit must be booked during this first delivery year (coordinator action).' — or confirm the booking with the coordinator and keep the sentence.
- Source: _passpq/COMPLIANCE_CHECKLIST.md Item 6 ('stays open as written — confirm the first-year EQA sampling activity is booked'); SPEC_FACTS §10 (spec §12 p19)

**A52 · GROW_ASDAN/Resources_and_Tools.html** (A-fact, doc; UNVERIFIED)
- Current: “IQA before EQA; the first-year EQA sampling visit is booked.”
- Issue: Same unsupported status claim as the GROW hub: the committed compliance record lists the first-year EQA booking as an open, unconfirmed centre action.
- Proposed: 'IQA before EQA; the first-year EQA sampling visit must be booked during this first delivery year (coordinator action).' — or confirm the booking and keep.
- Source: _passpq/COMPLIANCE_CHECKLIST.md Item 6; SPEC_FACTS §10 (spec §12 p19)

**A53 · GROW_ASDAN/Scheme_and_Resources.html** (A-fact, doc; UNVERIFIED)
- Current: “IQA before EQA; the first-year EQA sampling visit is booked.”
- Issue: Same unsupported status claim as the GROW hub: the committed compliance record lists the first-year EQA booking as an open, unconfirmed centre action.
- Proposed: 'IQA before EQA; the first-year EQA sampling visit must be booked during this first delivery year (coordinator action).' — or confirm the booking and keep.
- Source: _passpq/COMPLIANCE_CHECKLIST.md Item 6; SPEC_FACTS §10 (spec §12 p19)

**A54 · GROW_ASDAN/Scheme_and_Resources.html** (A-fact, doc; AMBIGUOUS)
- Current: “at most 3 adjacent-level credits count toward an L1 qualification”
- Issue: In a bank line whose stated target is the 'ASDAN PEQ Level 1 Award (Entry 3 floor)', this over-promises: the 3-adjacent-credit allowance exists only for the Extended Award (9) and Certificate (14); the 4-credit L1 Award requires all 4 credits at Level 1 (max adjacent N/A), so adjacent-level units contribute nothing to the Award itself.
- Proposed: 'adjacent-level credits can count toward an L1 Extended Award or Certificate (max 3 — in practice one unit); the 4-credit L1 Award needs all four credits at Level 1.'
- Source: SPEC_FACTS §3 (spec v1.2 §5.1 p10 table: L1 Award total 4, min at level 4, max adjacent N/A)

**A55 · LAUNCH_ASDAN/LAUNCH_ASDAN_Hub.html** (A-fact, doc; UNVERIFIED)
- Current: “IQA before EQA; the first-year EQA sampling visit is booked.”
- Issue: Same unsupported status claim as the GROW hub: the committed compliance record lists the first-year EQA booking as an open, unconfirmed centre action.
- Proposed: 'IQA before EQA; the first-year EQA sampling visit must be booked during this first delivery year (coordinator action).' — or confirm the booking and keep.
- Source: _passpq/COMPLIANCE_CHECKLIST.md Item 6; SPEC_FACTS §10 (spec §12 p19)

**A56 · LAUNCH_ASDAN/Resources_and_Tools.html** (A-fact, doc; UNVERIFIED)
- Current: “IQA before EQA; the first-year EQA sampling visit is booked.”
- Issue: Same unsupported status claim as the GROW hub: the committed compliance record lists the first-year EQA booking as an open, unconfirmed centre action.
- Proposed: 'IQA before EQA; the first-year EQA sampling visit must be booked during this first delivery year (coordinator action).' — or confirm the booking and keep.
- Source: _passpq/COMPLIANCE_CHECKLIST.md Item 6; SPEC_FACTS §10 (spec §12 p19)

**A57 · LAUNCH_ASDAN/Scheme_of_Work.html** (A-fact, doc; UNVERIFIED)
- Current: “assessor and learner signatures; the first-year EQA sampling visit is booked.”
- Issue: Same unsupported status claim (this panel variant also drops 'IQA before EQA', though the page's before-teaching checklist covers IQA-before-EQA): the committed compliance record lists the first-year EQA booking as an open, unconfirmed centre action.
- Proposed: 'assessor and learner signatures; IQA before EQA; the first-year EQA sampling visit must be booked during this first delivery year (coordinator action).'
- Source: _passpq/COMPLIANCE_CHECKLIST.md Item 6; SPEC_FACTS §10 (spec §12 p19)

**A58 · LAUNCH_ASDAN/Scheme_of_Work.html** (A-fact, doc; AMBIGUOUS)
- Current: “<b>Review Progress and Sign Off the Unit</b>”
- Issue: The W6 lesson title in the PEQ table (mirrored in the deck PEQ_W6, where a pupil-facing step says 'Name future use, and sign off.') implies the pupil signs off the unit; under the estate rule sign-off is the assessor's act (assessor + learner sign records, IQA where sampled).
- Proposed: rename the week here and in LAUNCH_ASDAN/PEQ/PEQ_W6 (learner-task text — same coordinated change, never silent) to e.g. 'Review Progress and Complete the Unit', reserving 'sign-off' for the assessor's act.
- Source: SPEC_FACTS §8 (spec v1.2 §10 p17: records signed by assessor, learner, IQA where sampled); ECA-1 ASDAN brief sign-off rule

**A59 · Art_Teesside/Build/BUILD_ART_A2_W7_Bank_It_and_Plan_the_Teach.html** (D-alignment, both; AMBIGUOUS)
- Current: “🎨 Bronze Part C close · Part D scope”
- Issue: The award strip (and print-intro 'Award part' line) claims 'Part C close', but no W7 task, exit ticket or worksheet produces or checks Part C evidence — everything is Part D scoping — and the evidence pack's own Part C locator rows end at 'Week 5 / 6 · where the borrowed decision shows in your piece'.
- Proposed: either add a visible Part C close step to W7 (e.g. a 'point at where your steal shows in the piece you will teach from' check on the worksheet) or trim the strip to 'Bronze Part D scope' and let the pack's Week 5/6 row close Part C; house rule is that a claimed part must actually be evidenced.
- Source: Art brief house rule ('every part reference must … actually evidence it'); Autumn2_Printable_Weekly_Evidence_Pack.html LOCP Part C rows; Autumn2_Scheme_of_Work.html Week 7 heading (same label, so the SoW would need the s

**A60 · Art_Teesside/Build/BUILD_ART_A2_W7_Bank_It_and_Plan_the_Teach.html** (A-qa, screen; AMBIGUOUS)
- Current: “Right size — visible, fast, fixes a real fault”
- Issue: In We Do 2 the three 'Right size —' targets are near-interchangeable across the SQUEEZE TEST / TAPING / CRAYON FLAT pills ('fixes a real fault' also describes taping, whose own card says 'the drift disappears'; 'one move, obvious result' also fits crayon-flat), so more than one pill is defensible per target.
- Proposed: name the skill-specific outcome in each target — squeeze: 'Right size — stops paint bleeding under the edge'; tape: 'Right size — stops the prints drifting'; flat: 'Right size — turns a ghost into a clear rubbing'.
- Source: Common brief exactly-one-correct-target rule; the print-wedo cards in the same file, which give each skill its distinct outcome.

**A61 · Art_Teesside/Build/BUILD_ART_A2_W6_Resolve_and_Edition.html** (A-fact, screen; AMBIGUOUS)
- Current: “Union and trade banners were often made in numbers. Why?”
- Issue: Arrival Stretch box 3 asserts union/trade banners were 'often made in numbers' with the key 'Carried in different places at once, and replaceable when damaged' — but historically each lodge/branch banner was a one-off commission (Tutill's workshop repeated stock DESIGNS across branches; individual banners were not editioned), so the premise is shaky as stated.
- Proposed: 'Banner-makers like Tutill’s repeated the same designs for union branches all over the country. Why repeat a design?' — keeps the editioning link without claiming identical multiples of one banner.
- Source: Verified knowledge: George Tutill (est. 1837) mass-produced trade-union banners from repeated stock designs, one commissioned banner per branch, replaced when worn.

**A62 · Art_Teesside/Build/BUILD_ART_W1_The_Local_Canvas.html** (A-qa, screen; AMBIGUOUS)
- Current: “Why does the 'why it matters' line make evidence stronger than a photo alone?”
- Issue: The I Do 2 cold-call Stretch question presumes a taught "'why it matters' line" (and the Standard question an "annotation") that no slide in this deck — or any of the eight decks, where the identical string recurs — ever teaches; W1's actual scaffold is the label + "next-time note".
- Proposed: per deck, point the question at the week's real written scaffold, e.g. W1: "Why does the next-time note make evidence stronger than a photo alone?" and M: "What will you write under each box?".
- Source: _ccQuestions template; grep: "why it matters" appears only inside this question in each of the 8 decks

**A63 · Art_Teesside/Build/BUILD_ART_W2_Artists_Makers_and_Teesside_Connections.html** (A-qa, both; AMBIGUOUS)
- Current: “<h3>2. Analysis (Recall)</h3>”
- Issue: Stretch arrival box 2 asks "Content, form, process, mood — what are these?" labelled (Recall), but the four analysis moves are first taught later in this same lesson (I Do 1) — nothing prior covers them, so it is not retrieval.
- Proposed: relabel as a Think/preview box or swap for a Week-1-taught item (e.g. "Which element carried the mood of your W1 page?").
- Source: W1 deck content (formal elements only) vs W2 I Do 1; BRIEF_ART arrival rule (last-week retrieval)

**A64 · Art_Teesside/Build/BUILD_ART_W8_Share_Reflect_and_Close_the_Loop.html** (A-fact, both; UNVERIFIED)
- Current: “Last year's class put the Skills Lab where it is.”
- Issue: The Lundy INFLUENCE box (slide and print Lundy table) tells pupils a previous cohort's verdicts placed the Skills Lab, but this suite is presented throughout as the 2026–27 build and nothing in the repo evidences a prior cohort's SoW review — if untrue, it fabricates provenance to make the influence promise feel real.
- Proposed: owner confirms a real prior-cohort decision, else delete the sentence (the promise stands without it).
- Source: Could not verify: Scheme_of_Work/START_HERE date the suite 2026–27 with no prior-run record in the repo

## SOW-SIDE (error lives in the quoted spec/SoW text)

**O1 · BUILD_ASDAN/Scheme_of_Work.html** (B-spelling, screen; SOW-SIDE)
- Current: “Banks: banks ASDAN LI M8 / AQA UAS.”
- Issue: Every Careers bullet (and every other slot's bullets) doubles the word — 'Banks: banks …' — while the decks themselves print 'Banks: ASDAN LI M8 / AQA UAS' correctly.
- Proposed: "Banks: ASDAN LI M8 / AQA UAS." (apply the same de-duplication to the other slots' lines)
- Source: BUILD_ASDAN/Scheme_of_Work.html vs the seven decks' award strips

**O2 · BUILD_ASDAN/Scheme_of_Work.html** (D-alignment, screen; SOW-SIDE)
- Current: “W7 My Career Profile</b> — Poster &amp; portfolio.”
- Issue: The Careers list jumps W5→W7 with no row for the taught Week 6 (What Happens After Year 11) that the page's own intro announces, and the W1/W2/W3/W5/W7 Lundy lines (e.g. 'Say which job area you&#x27;d like to explore next.') are superseded voice asks the shipped decks no longer use.
- Proposed: add a W6 'What Happens After Year 11' row and refresh the five Lundy lines to the decks' current VOICE texts
- Source: CAREERS_W7_After_Year_11.html exists as taught Week 6 (title strip 'Week 6 of 7'); deck Lundy VOICE boxes; START_HERE ordering note

**O3 · BUILD_ASDAN/Duke_and_Enterprise/START_HERE.html** (D-alignment, screen; SOW-SIDE)
- Current: “SMSC: Anti-Bullying Week, World Kindness Day.”
- Issue: The module strip schedules this suite as 'BUILD ASDAN Aut 1' (Sept–Oct 2026) yet its SMSC hooks — Anti-Bullying Week (16–20 Nov 2026) and World Kindness Day (13 Nov 2026) — both fall in Autumn 2, so W2's 'World Kindness Day' theming cannot coincide with the day; the mismatch originates in the SoW/hub planning line, which the decks inherit.
- Proposed: either move the kindness week's SMSC hook to an Aut 1 observance or annotate 'builds towards World Kindness Day (13 Nov)'.
- Source: World Kindness Day is 13 November; Anti-Bullying Week 2026 is 16–20 November (Anti-Bullying Alliance) — verified knowledge; deck sow-strips read 'BUILD ASDAN Aut 1 · 2026–27'

**O4 · LAUNCH_ASDAN/Vocational/VOC_W2_Health_Safety_and_Hygiene_at_Work.html** (B-spelling, both; SOW-SIDE)
- Current: “<h1>Health Safety and Hygiene at Work</h1>”
- Issue: The title-slide H1, page <title>, sow-strip, witness statement and print-intro all use the comma-less 'Health Safety and Hygiene at Work' (a three-item list missing its commas), while the same deck's Knowledge Organiser and lesson-complete overlay print the correctly punctuated 'Health, Safety and Hygiene at Work' — the comma-less form originates in the SoW/hub naming, which the deck inherits, so 
- Proposed: standardise on 'Health, Safety and Hygiene at Work' across Scheme_of_Work.html, START_HERE.html and this deck (or accept the comma-less registry name everywhere and drop the commas from the KO/overlay for consistency).
- Source: LAUNCH_ASDAN/Scheme_of_Work.html W2 row and START_HERE.html Week-2 card (both comma-less) vs this deck's print-ko heading 'Knowledge Organiser (LAUNCH ASDAN W2): Health, Safety and Hygiene at Work'

**O5 · LAUNCH_ASDAN/Vocational/VOC_W5_Tools_Equipment_and_Safe_Use.html** (B-spelling, both; SOW-SIDE)
- Current: “<h1>Tools Equipment and Safe Use</h1>”
- Issue: The title-slide H1, page <title>, witness statement and print-intro use the comma-less 'Tools Equipment and Safe Use' (list missing its commas) while the same deck's Knowledge Organiser and lesson-complete overlay use 'Tools, Equipment and Safe Use'; the comma-less form is inherited from the SoW/hub naming ('Tools Equipment and Safe Use' in both), so the defect is SoW-side and a fix must be applie
- Proposed: standardise on 'Tools, Equipment and Safe Use' across Scheme_of_Work.html, START_HERE.html and this deck (or make the comma-less registry name uniform).
- Source: LAUNCH_ASDAN/Scheme_of_Work.html W5 row and START_HERE.html Week-5 card (both comma-less) vs this deck's print-ko heading 'Knowledge Organiser (LAUNCH ASDAN W5): Tools, Equipment and Safe Use'


---

# Appendix — Humanities, DT and Art-estate-docs batches (audits completed later)

## Serious findings needing a ruling (appendix)

**XP1 · Art_Teesside/Spring2_Printable_Weekly_Evidence_Pack.html** (D-alignment, print; MISALIGNED)
- Current: “"t": "Proposal, Pitch &amp; Review", "part": "Explore D · Bronze D · Silver 2A&ndash;B"”
- Issue: Week 6 (proposal/pitch) is chipped as Bronze Part D (arts skills share) and the chip prints in the sheet header, footer and recovery-route box as the week's banked part, but nothing in Spring 2 shares a skill with a learner — no learner, nothing a learner made — breaking 'a plan is not a teach' and the estate's own precedent of chipping non-delivery weeks as 'Part D scope' (A2 pack W7).
- Proposed: remap the Bronze chip for W6 (e.g. "Bronze A" or "Bronze D scope") and keep Explore D / Silver 2A–B; owner to confirm the intended Bronze mapping since it also feeds the week-select dropdown and Locator.
- Source: House_Standard_and_Safety.html §2 ('A plan is not a teach. Sharing skills needs a real learner and something the learner made'); Build/Autumn2_Printable_Weekly_Evidence_Pack.html W7 chip 'Bronze Part C close &middot; Par

**XP2 · Art_Teesside/Spring2_Printable_Weekly_Evidence_Pack.html** (D-alignment, print; MISALIGNED)
- Current: “Explore Part D: you actively chose what to share and can say why. Bronze Part D: you shared a skill with others. Silver Unit 2: you led a project involving other people.”
- Issue: The Evidence Locator block 'Presenting, sharing or leading' maps Bronze Part D ('you shared a skill with others') onto rows that are all Week 6 proposal evidence ('Week 6 · your proposal and the channel you chose', 'the response you received'), but presenting a proposal is not a skills share, so an adviser filing from this form would bank Bronze D on non-qualifying evidence.
- Proposed: drop the Bronze Part D sentence from this block (Bronze D is delivered in Spring 1 'Pass It On' and via the Summer 2 feeder workshop) or add a genuine skill-share row; also soften 'Silver Unit 2: you led a project' since Spring 2 W6 only evidences the 2A–B planning side.
- Source: House_Standard_and_Safety.html §2 'A plan is not a teach'; Build/Spring1_Scheme_of_Work.html (Spring 1 'exists to finish Part D properly')

**XP3 · Art_Teesside/Summer1_Printable_Weekly_Evidence_Pack.html** (D-alignment, print; MISALIGNED)
- Current: “"t": "Text, Edition &amp; Assembly", "part": "Explore C · Bronze A/D · Silver 1B"”
- Issue: Week 5's Bronze chip includes '/D' (arts skills share), but the week's 'sharing' is giving away edition spares — sharing artwork with an audience, not passing on a skill to a learner; no learner or learner-made piece exists in the week or anywhere in Summer 1.
- Proposed: change the Bronze chip to "Bronze A" (participation) unless a real skill-share step is added to the week.
- Source: House_Standard_and_Safety.html §2 (skills share needs a real learner and something the learner made); Trinity Bronze Part D = arts skills share — verified knowledge

**XP4 · Art_Teesside/Summer1_Printable_Weekly_Evidence_Pack.html** (D-alignment, print; MISALIGNED)
- Current: “"t": "Pop-Up Installation &amp; Voice", "part": "Explore D · Bronze D · Silver 2C&ndash;D"”
- Issue: Week 6 (pop-up installation, visitor response) is chipped Bronze Part D, but installing a banner and capturing a visitor's words is audience/presenting evidence, not a skills share — Summer 1 contains no teach anywhere, so the chip claims a part the whole unit never evidences.
- Proposed: remap the Bronze chip (e.g. "Bronze A") and keep Explore D / Silver 2C–D; owner to confirm.
- Source: House_Standard_and_Safety.html §2; estate precedent: Build/Autumn2_Printable_Weekly_Evidence_Pack.html uses 'Part D scope' where Part D is not delivered

**XP5 · Art_Teesside/Summer2_Printable_Weekly_Evidence_Pack.html** (D-alignment, print; MISALIGNED)
- Current: “"t": "Portfolio Review &amp; Selection", "part": "Explore D · Bronze D · Silver 2E"”
- Issue: Week 1 (portfolio audit/selection) is chipped Bronze Part D though selecting work is not a skills share, and the sheet's own recovery rule ('Recovery evidences the SAME award part') is unsatisfiable — the W1 recovery route ('Audit from photographs') cannot evidence Bronze D either.
- Proposed: chip W1's Bronze slot as a review/audit contribution (e.g. "Bronze audit" or "Bronze D scope") — the term's real Bronze D vehicle is the Week 6 feeder-school workshop, which the Locator correctly guards as 'if run (Bronze Part D)'.
- Source: House_Standard_and_Safety.html §2 'A plan is not a teach'; Summer2 pack Locator block 'The claim' ('Feeder-school workshop, if run (Bronze Part D)')

**XP6 · Art_Teesside/Summer2_Printable_Weekly_Evidence_Pack.html** (D-alignment, print; MISALIGNED)
- Current: “"t": "Labels, Statements &amp; Your North-East Anchor", "part": "Explore B/D · Bronze C/D · Silver 1D"”
- Issue: Week 4's Bronze chip 'C/D' half-claims Part D: writing wall labels and an artist-anchor line evidences Bronze C (arts inspiration/research) but contains no skills share, so the '/D' is unearned on this week's sheet.
- Proposed: change the Bronze chip to "Bronze C" only.
- Source: House_Standard_and_Safety.html §2; Trinity Bronze Part C = arts inspiration research, Part D = skills share — verified knowledge

**XP7 · Art_Teesside/Summer2_Scheme_of_Work.html** (A-fact, doc; WRONG)
- Current: “a North-East artist &mdash; Tabner, Shaw, Barlow, Deller or their own choice”
- Issue: Week 4's exemplar list of North-East artists is faulty: Jeremy Deller is London-born and London-based (not a North-East artist), and 'Shaw' resolves to no artist anchored anywhere in this estate and no notable North-East artist — almost certainly a slip for 'Thorpe' (Mackenzie Thorpe, b. Middlesbrough, anchored with Len Tabner in A2 W2); only Tabner (South Bank/Boulby) and Barlow (b. Newcastle 194
- Proposed: "a North-East artist &mdash; Tabner, Thorpe, Barlow or their own choice" (or reframe as "an artist met this year" if Deller is to stay).
- Source: Jeremy Deller b. London 1966, London-based; Mackenzie Thorpe b. Middlesbrough 1956; Len Tabner b. South Bank, Middlesbrough 1946; Phyllida Barlow b. Newcastle 1944 — verified knowledge; estate grep: 'Shaw' appears only i

**XP8 · Art_Teesside/Summer2_Printable_Weekly_Evidence_Pack.html** (A-fact, print; WRONG)
- Current: “a North-East artist — Tabner, Shaw, Barlow, Deller or your own choice”
- Issue: Week 4's printed fix line repeats the Summer 2 SoW's faulty North-East artist list: Deller is not a North-East artist and 'Shaw' is a dangling name taught nowhere in the estate (likely 'Thorpe', the Middlesbrough-born A2 W2 anchor).
- Proposed: "a North-East artist — Tabner, Thorpe, Barlow or your own choice" (mirror whatever wording the owner settles on for the SoW).
- Source: Same as the Summer2 SoW finding: Deller b. London 1966; Thorpe b. Middlesbrough; estate grep shows 'Shaw' only in Summer 2 files

**XP9 · Build/Slideshows/BUILD_HUM_W1_Human_Timeline.html** (A-fact, screen; WRONG)
- Current: “Still carrying people across the Tees”
- Issue: Starter product card presents the Transporter Bridge as still carrying people, but the bridge has been closed to all users since December 2019 and remains closed for the 2026-27 teaching year.
- Proposed: 'Spanning the Tees since 1911 (closed for repairs since 2019)'.
- Source: Tees Transporter Bridge closed December 2019 on safety grounds; still closed as of Jan 2026 (restoration unfunded/incomplete) — verified knowledge; fixer should confirm no 2026 reopening.

**XP10 · Build/Slideshows/BUILD_HUM_W1_Human_Timeline.html** (D-alignment, both; MISALIGNED)
- Current: “How can clues and centuries help us place local events in a defensible order, from 1000 CE to today?”
- Issue: On-deck W1 enquiry adds 'and centuries' and 'from 1000 CE to today' versus the SoW's named enquiry 'How can clues help us place local events in a defensible chronological order?'; the deck matches the Pathway Tracker, so the drift is deck+Tracker vs SoW.
- Proposed: reconcile — either update SoW W1 enquiry to the deck wording (likely, since Tracker is generated from decks) or trim the deck.
- Source: Humanities_Teesside/BUILD_Scheme_of_Work.html Week 1 vs deck title slide and print KO; Pathway_Tracker.html agrees with deck.

**XP11 · Build/Slideshows/BUILD_HUM_W2_History_Detectives.html** (D-alignment, both; MISALIGNED)
- Current: “How can we distinguish what a source shows from what we infer or still need to ask?”
- Issue: On-deck W2 enquiry ends 'or still need to ask?' where the SoW's named enquiry ends 'or still cannot know?'; deck matches the Tracker.
- Proposed: reconcile deck/Tracker wording with SoW Week 2.
- Source: Humanities_Teesside/BUILD_Scheme_of_Work.html Week 2 vs deck title slide and print KO.

**XP12 · Build/Slideshows/BUILD_HUM_W4_People_Who_Shaped_Britain.html** (D-alignment, both; MISALIGNED)
- Current: “How can evidence show why a person or community matters without reducing them to a single story?”
- Issue: On-deck W4 enquiry says 'a single story' where the SoW's named enquiry says 'one story' — trivial wording drift; deck matches the Tracker.
- Proposed: reconcile with SoW Week 4 (or accept deck wording and update SoW).
- Source: Humanities_Teesside/BUILD_Scheme_of_Work.html Week 4 vs deck title slide and print KO.

**XP13 · Build/Slideshows/BUILD_HUM_W5_Big_Deal.html** (D-alignment, both; MISALIGNED)
- Current: “How can we judge significance using criteria rather than fame or personal taste?”
- Issue: On-deck W5 enquiry ends 'personal taste' where the SoW's named enquiry ends 'personal liking' — trivial wording drift; deck matches the Tracker.
- Proposed: reconcile with SoW Week 5.
- Source: Humanities_Teesside/BUILD_Scheme_of_Work.html Week 5 vs deck title slide and print KO.

**XP14 · Build/Slideshows/BUILD_HUM_W6_Plan_The_Story.html** (D-alignment, both; MISALIGNED)
- Current: “How can sequence, evidence and explanation turn facts into a coherent historical story?”
- Issue: On-deck W6 enquiry says 'coherent historical story' where the SoW's named enquiry says 'coherent account' — wording drift; deck matches the Tracker.
- Proposed: reconcile with SoW Week 6.
- Source: Humanities_Teesside/BUILD_Scheme_of_Work.html Week 6 vs deck title slide and print KO.

**XP15 · Build/Slideshows/BUILD_HUM_W6_Plan_The_Story.html** (D-alignment, both; MISALIGNED)
- Current: “That bridge is where the marks live, and where the thinking lives.”
- Issue: 'Where the marks live' is exam-mark-scheme framing in a BUILD deck: the SoW names no board and BUILD is judged Secure/Developing/Not yet, not marked; the phrase recurs in the print reference zone ('That bridge is where the marks live.').
- Proposed: 'That bridge is where the thinking lives.' (both instances).
- Source: Brief rule: no mark-scheme/exam-board framing; Pathway_Tracker.html BUILD judgement scale has no marks.

**XP16 · Build/Slideshows/BUILD_HUM_W7_Tell_The_Story.html** (C-construction, print; WRONG)
- Current: “What does the E-for-evidence do?”
- Issue: Print Arrival (Supported) Q2 asks about E-for-evidence while the on-screen Arrival (Supported) Q2 asks 'What does the L-for-link do?' (with its answer key) — the printed sheet no longer matches the delivered retrieval question.
- Proposed: change print Q2 to 'What does the L-for-link do?' to match the screen.
- Source: Deck-internal: #arrival-supported vs #print-arrival supported-content.

**XP17 · Build/Slideshows/BUILD_HUM_W7_Tell_The_Story.html** (A-qa, print; WRONG)
- Current: “👪 Family at showcase</td><td>Conversational &mdash; invite questions”
- Issue: The print Reference Zone audience table contradicts the We Do 2 match key: on screen 'Conversational — invite questions' is the correct answer for 'One partner' and Family pairs with 'Warmth + the local details they'll know' (absent from the reference), so a pupil using the printed reference during the match gets marked wrong.
- Proposed: align the reference rows to the match key — Family: 'Warmth + the local details they'll know'; One partner: 'Conversational — invite questions' (or vice versa in the match; pick one canonical pairing).
- Source: Deck-internal: #wedo2 data-correct keys vs #print-reference table rows.

**XP18 · Build/Slideshows/BUILD_HUM_W7_Tell_The_Story.html** (D-alignment, both; MISALIGNED)
- Current: “How can I communicate a historical account so an audience understands what happened and why?”
- Issue: On-deck W7 enquiry ends 'understands what happened and why' where the SoW's named enquiry ends 'understands claim, evidence and uncertainty' — substantive drift (uncertainty dropped); deck matches the Tracker.
- Proposed: reconcile with SoW Week 7 (SoW wording carries the uncertainty strand that the deck's Aspire line partially covers).
- Source: Humanities_Teesside/BUILD_Scheme_of_Work.html Week 7 vs deck title slide and print KO.

**XP19 · Build/Slideshows/BUILD_HUM_W8_Where_In_The_World.html** (A-qa, print; WRONG)
- Current: “🏴 Merthyr &rarr; the Tees</td><td>Coastal steamer, or the east-coast line”
- Issue: The print Reference Zone journeys table swaps the Merthyr and Clydeside routes relative to the We Do 2 match key: on screen (geographically correct) Clydeside → 'Coastal steamer or the east-coast line' and Merthyr → 'Rail up the spine of England'; the printed table reverses them, so it contradicts the activity and the geography (an east-coast line from South Wales makes no sense).
- Proposed: swap the two route cells in the reference table to match the on-screen key.
- Source: Deck-internal: #wedo2 data-correct keys vs #print-reference table; east-coast main line serves Scotland→Teesside, not South Wales — verified knowledge.

**XP20 · Build/Slideshows/BUILD_HUM_W8_Where_In_The_World.html** (C-construction, print; WRONG)
- Current: “🏴&#xF3;&#xF3; Clydeside &rarr; Teesside”
- Issue: Corrupted entity sequence in the print Reference Zone journeys table: the Scotland flag renders as a black flag followed by 'óó' (mangled tag-sequence escape).
- Proposed: replace with the proper Scotland flag sequence 🏴󠁧󠁢󠁳󠁣󠁴󠁿 as used elsewhere in the same deck.
- Source: Raw file text; the same deck's match pill uses the correct 🏴󠁧󠁢󠁳󠁣󠁴󠁿 sequence.

**XP21 · Build/Slideshows/BUILD_HUM_W8_Where_In_The_World.html** (D-alignment, both; MISALIGNED)
- Current: “How does mapping movement change our understanding of migration, connection and place?”
- Issue: On-deck W8 enquiry ends 'connection and place' where the SoW's named enquiry ends 'connection and identity' — notable because the unit itself is 'Migration & Identity'; deck matches the Tracker.
- Proposed: reconcile with SoW Week 8 (SoW's 'identity' ties the closing week back to the unit enquiry).
- Source: Humanities_Teesside/BUILD_Scheme_of_Work.html Week 8 vs deck title slide and print KO.

**XP22 · Launch/Slideshows/LAUNCH_HUM_W5_People_Modern_Britain.html** (A-qa, screen; WRONG)
- Current: “W4 agency/context + W5 significance + W2 causation ranks.”
- Issue: Arrival stretch Q4 answer key ('Which weeks does this enquiry braid together?') uses the GROW/BUILD week map, not LAUNCH's: in LAUNCH, W4 is Century of Change (change/continuity, not agency/context) and W5 is this very lesson, so it cannot be a braided prior week — the deck's own W7 tool map labels W4 'Change dials' and W5 'Person + pattern'.
- Proposed: 'W4 change/continuity + W2 causation ranks + W1 source weighing.'
- Source: LAUNCH_Scheme_of_Work.html and Pathway_Tracker.html week map; LAUNCH_HUM_W7 We Do 2 pills ('🧭 W4 Change dials', '🔗 W5 Person + pattern'); GROW/BUILD W4 = People Who Shaped Britain, W5 = significance

**XP23 · Launch/Slideshows/LAUNCH_HUM_W5_People_Modern_Britain.html** (A-qa, screen; WRONG)
- Current: “W4 balance + W5 frames + W2 ranks”
- Issue: Exit stretch Q3 answer key ('Which earlier weeks did today braid, and how?') cites W5 — the current week — as an earlier week and mislabels W4 ('balance' is this lesson's agency/structure content; LAUNCH W4 was turning-point/change), again matching the sibling-tier week map rather than LAUNCH's.
- Proposed: 'W4 turning-point judgement + W2 ranks + W1 weighing — named braid.'
- Source: LAUNCH week map (SoW + Tracker); same-deck evidence: W4 retrieval questions in this deck are all about hinge/endpoint, not agency

**XP24 · Grow/Slideshows/GROW_HUM_W1_Time_Detectives.html** (A-fact, print; WRONG)
- Current: “the bridge (1911) is Georgian by days, Edwardian by habit.”
- Issue: Knowledge Organiser Key Fact: the Transporter Bridge opened 17 Oct 1911, about 17 months after George V acceded (6 May 1910), so 'Georgian by days' is false under any reading.
- Proposed: "the bridge (1911) is Georgian by a year and a half, Edwardian by habit."
- Source: Edward VII died / George V acceded 6 May 1910; Transporter Bridge opened 17 Oct 1911 — verified knowledge

**XP25 · Grow/Slideshows/GROW_HUM_W1_Time_Detectives.html** (A-fact, print; WRONG)
- Current: “<em>Edwardian by a whisker, not Victorian</em>”
- Issue: Reference Zone says the 1911 bridge is 'Edwardian by a whisker' while the same Reference Zone table defines Edwardian as 1901–1910 and the KO says 'Georgian by days' — the deck contradicts itself on its own signature teaching point (period-label precision).
- Proposed: e.g. "just past Edwardian — opened under George V in 1911, though habit still calls it Edwardian" so table, Reference Zone and KO agree.
- Source: Deck's own period table 'Edwardian 1901–1910' + Edwardian era ended with Edward VII's death May 1910 — verified knowledge

**XP26 · Grow/Slideshows/GROW_HUM_W1_Time_Detectives.html** (C-construction, print; WRONG)
- Current: “<div class="print-section" id="print-lundy">”
- Issue: In W1–W6 and W8, #print-lundy (carrying 'What I said, and what it changed') and #print-feedback are nested inside #print-exit > .supported-content and are never added to printPack's visible list, so the written Lundy close and the feedback sheet never print in any pack and additionally sit in the supported-only branch (tier parity broken); W7 has #print-feedback nested the same way.
- Proposed: move #print-lundy and #print-feedback out to be direct children of #print-area and add 'lundy','feedback' to the printPack() visible list in all eight decks (W7: 'feedback' only — its Lundy absence is sentinel-held).
- Source: Deck CSS .print-section{display:none}/.print-section.visible and printPack() list ['ko','arrival','starter','wedo','reference','exit'] in all 8 files; HUM brief says GROW packs carry the written line

**XP27 · Grow/Slideshows/GROW_HUM_W6_Plan_The_Account.html** (C-construction, screen; WRONG)
- Current: “Four pillars beneath it are ordered PEEL units holding it up.”
- Issue: I Do 1 illuminator (SVG + aria-label) shows FOUR PEEL pillars while the entire lesson teaches a THREE-unit blueprint ('PEEL units — Three…', 'Opening, 3 units, counter, close', reference 'six slots' with UNIT 1–3) — the diagram contradicts the taught structure.
- Proposed: redraw with three PEEL pillars (or relabel the fourth as COUNTER) and update the aria-label to match.
- Source: Same deck: blueprint text, Reference Zone 'six slots', W7 checklist (Unit 1–3); internal consistency check

**XP28 · Grow/Slideshows/GROW_HUM_W7_Write_The_Account.html** (A-fact, screen; WRONG)
- Current: “The ore waited in the hills for eighty years”
- Issue: I Do 2 model close asserts an eighty-year wait that fits no interval in the suite's taught chronology (railway 1825 → ironstone 1850 is the taught 25-year wait; the ore then did not wait at all) — an unanchored figure pupils are invited to reproduce in the assessed account of an interval-precision suite.
- Proposed: e.g. "The ore waited in the hills while the railway ran for a quarter of a century" or drop the number.
- Source: Suite chronology: S&D Railway 1825, Eston ironstone find June 1850, town founded 1830 — verified knowledge; W1 worked model ('25 years')

**XP29 · Humanities_Teesside/BUILD_Scheme_of_Work.html** (C-construction, doc; WRONG)
- Current: “the *same zone hues as the Teesside art suites*”
- Issue: Unconverted markdown emphasis renders literal asterisks in prose — 3 occurrences (line 22, and line 34 'what a source *shows* from what we *infer*').
- Proposed: replace each *…* pair with <i>…</i> (or drop the markers) at lines 22 and 34.
- Source: Raw file; HTML does not interpret markdown — asterisks display verbatim.

**XP30 · Humanities_Teesside/GROW_Scheme_of_Work.html** (C-construction, doc; WRONG)
- Current: “into *defensible history*”
- Issue: Unconverted markdown emphasis renders literal asterisks — 6 occurrences (lines 11, 22, 27, 34 twice, and inside the Week 1 enquiry at line 48).
- Proposed: replace each *…* pair with <i>…</i> throughout (6 places).
- Source: Raw file; HTML does not interpret markdown.

**XP31 · Humanities_Teesside/LAUNCH_Scheme_of_Work.html** (C-construction, doc; WRONG)
- Current: “the *same zone family as the whole Teesside programme*”
- Issue: Unconverted markdown emphasis renders literal asterisks — 2 occurrences (line 22, and line 34 'weigh *how far* a source').
- Proposed: replace each *…* pair with <i>…</i> (2 places).
- Source: Raw file; HTML does not interpret markdown.

**XP32 · Humanities_Teesside/BUILD_Scheme_of_Work.html** (D-alignment, doc; MISALIGNED)
- Current: “<h2>Week 1: The Big Timeline</h2>”
- Issue: SoW Week 1 title 'The Big Timeline' does not match the deployed deck and Pathway Tracker title 'The Local History Timeline' (the deck itself is split — its <title>/h1/KO say 'The Local History Timeline' while its feedback sheet and TA modal say 'The Big Timeline').
- Proposed: retitle to 'Week 1: The Local History Timeline' to match the deck <title> and tracker, or unify the name suite-wide (deck internals are the hum batch's remit).
- Source: Build/Slideshows/BUILD_HUM_W1_Human_Timeline.html <title> and KO; Pathway_Tracker.html W1 BUILD row ('taken from the deployed lesson files').

**XP33 · Humanities_Teesside/BUILD_Printable_Pack.html** (D-alignment, both; MISALIGNED)
- Current: “{w:1,t:"The Big Timeline",tk:"THE TIMELINE TICKET"”
- Issue: Printable pack Week 1 sheet/dropdown title 'The Big Timeline' does not match the deployed deck and tracker title 'The Local History Timeline'.
- Proposed: t:"The Local History Timeline" (keep consistent with whichever name the fixer unifies on).
- Source: Build/Slideshows/BUILD_HUM_W1_Human_Timeline.html <title>; Pathway_Tracker.html W1 BUILD row.

**XP34 · Humanities_Teesside/BUILD_Scheme_of_Work.html** (D-alignment, doc; MISALIGNED)
- Current: “so an audience understands claim, evidence and uncertainty?”
- Issue: SoW Week 7 enquiry promises 'claim, evidence and uncertainty' but the deployed deck and tracker teach 'so an audience understands what happened and why' — the most substantive of the BUILD drifts.
- Proposed: replace with "so an audience understands what happened and why?" to match the deck, or escalate if the SoW framing was the intended upgrade (deck edit belongs to the hum batch).
- Source: BUILD_HUM_W7 deck enquiry; Pathway_Tracker.html W7 BUILD row.

**XP35 · Humanities_Teesside/BUILD_Scheme_of_Work.html** (D-alignment, doc; MISALIGNED)
- Current: “The engine is deliberately light — no sorts or retrieval quizzes — which is the right pitch for Explore/BUILD, so none were added.”
- Issue: Stale claim: all 8 deployed BUILD_HUM decks now contain a level-toggled retrieval grid, a 'Tap-tap sort' and a match round (house chassis inheritance), so 'no sorts or retrieval quizzes… so none were added' is false of the shipped suite.
- Proposed: rewrite to reflect the current decks, e.g. note that the house retrieval grid, tap-tap sort and match round were later inherited from the shared chassis.
- Source: grep: 'Retrieval grid' and 'Tap-tap' present in all 8 Build/Slideshows/BUILD_HUM_W*.html decks.

**XP36 · Humanities_Teesside/GROW_Scheme_of_Work.html** (D-alignment, doc; MISALIGNED)
- Current: “The engine is deliberately light — right for GROW — so no extra quiz engine was added.”
- Issue: Stale claim: all 8 deployed GROW_HUM decks now carry the house retrieval grid and tap-tap sort engine, contradicting 'no extra quiz engine was added'.
- Proposed: rewrite to acknowledge the chassis-inherited retrieval/sort engine (same fix pattern as the BUILD SoW).
- Source: grep: 'Retrieval grid'/'Tap-tap' present in all 8 Grow/Slideshows/GROW_HUM_W*.html decks (and all 8 LAUNCH decks; LAUNCH SoW makes no equivalent claim).

**XP37 · Humanities_Teesside/Pathway_Tracker.html** (D-alignment, doc; MISALIGNED)
- Current: “Teesside &middot; Migration &amp; the Making of Modern Teesside &middot; Autumn 1, 2026&ndash;27”
- Issue: The visible subtitle names the unit 'Migration & the Making of Modern Teesside' while this file's own <title>, all three SoWs, all three packs and the hub call it 'Teesside Migration & Identity'.
- Proposed: "Teesside &middot; Migration &amp; Identity &middot; Autumn 1, 2026&ndash;27 &middot; Progress Schools Tees Valley"
- Source: Pathway_Tracker.html line 3 <title> vs line 33; BUILD/GROW/LAUNCH SoW and pack titles.

**XP38 · Build/Slideshows/BUILD_DT_W6_Handover.html** (D-alignment, screen; WRONG)
- Current: “<strong>Key Question:</strong> When is a thing finished — and how do you know to stop?”
- Issue: W6's on-screen Starter slide is a leftover copy of W5's — key question, Big Idea 'The finish is the difference.', game card 'Sort it' (W6's actual We Do 1 is 'Team quiz — talk, then reveal') and footer 'Finishing is slow on purpose…' — while W6's own print-starter already carries the correct handover key question.
- Proposed: mirror print-starter — key question 'What does the community get that was not there in September?', Big Idea 'Handed over, not just finished.', game card 'Team quiz', footer 'Speak, carry, or photograph — all three count as taking part.'
- Source: Same file's print-starter section ('Key question: What does the community get that was not there in September?') and We Do 1 header ('Team quiz — talk, then reveal'); DT_Community_Upcycling/Weekly_Plan.html W6 row.

**XP39 · Build/Slideshows/BUILD_DT_W2_Blueprint.html** (D-alignment, screen; WRONG)
- Current: “Onto the Build Board: vote for what we build, and today’s stage photo goes up.”
- Issue: W2's lesson-complete modal tells pupils to vote for what to build, but the vote was W1's Lundy VOICE activity and W2's own VOICE is 'Your measurements go on the blueprint' — an un-updated copy of W1's modal line.
- Proposed: 'Onto the Build Board: your measurements went on the blueprint, and today’s stage photo goes up.'
- Source: W1 Lundy VOICE ('Vote for the community asset we'll build'), W2 Lundy VOICE in the same file; SoW: the vote is W1's Lundy VOICE.

**XP40 · Build/Slideshows/BUILD_DT_W3_Core_Cut.html** (D-alignment, screen; WRONG)
- Current: “Onto the Build Board: vote for what we build, and today’s stage photo goes up.”
- Issue: W3's lesson-complete modal repeats W1's 'vote for what we build' line although the build was decided in W1 and W3's VOICE is 'You say when you are ready for the tool'.
- Proposed: 'Onto the Build Board: you said when you were ready for the tool, and today’s stage photo goes up.'
- Source: W3 Lundy VOICE in the same file; W1 Lundy VOICE (the vote); SoW W1 line 'Lundy VOICE: vote the community asset'.

**XP41 · Build/Slideshows/BUILD_DT_W4_Assembly.html** (D-alignment, screen; WRONG)
- Current: “Onto the Build Board: vote for what we build, and today’s stage photo goes up.”
- Issue: W4's lesson-complete modal repeats W1's 'vote for what we build' line although W4's VOICE is 'Each builder explains one joining choice they made'.
- Proposed: 'Onto the Build Board: you explained a joining choice, and today’s stage photo goes up.'
- Source: W4 Lundy VOICE in the same file; W1 Lundy VOICE (the vote).

**XP42 · Build/Slideshows/BUILD_DT_W5_Finish.html** (D-alignment, screen; WRONG)
- Current: “Onto the Build Board: vote for what we build, and today’s stage photo goes up.”
- Issue: W5's lesson-complete modal repeats W1's 'vote for what we build' line although W5's VOICE is 'You say when yours is finished'.
- Proposed: 'Onto the Build Board: you said when yours was finished, and today’s stage photo goes up.'
- Source: W5 Lundy VOICE in the same file; W1 Lundy VOICE (the vote).

**XP43 · Build/Slideshows/BUILD_DT_W6_Handover.html** (D-alignment, screen; WRONG)
- Current: “Onto the Build Board: vote for what we build, and today’s stage photo goes up.”
- Issue: W6's lesson-complete modal — the final week — still tells pupils to vote for what to build; W6's VOICE is explaining the finished build to the partner.
- Proposed: 'Onto the Build Board: you explained the build to the partner — the last link in the chain.'
- Source: W6 Lundy VOICE in the same file; W1 Lundy VOICE (the vote).

**XP44 · Build/Slideshows/BUILD_DT_W1_Workshop_Audit.html** (D-alignment, screen; MISALIGNED)
- Current: “<h2>Wordsearch — settle in</h2>”
- Issue: W1's We Do 1 (and its Starter game card) is titled 'Wordsearch' but is a tap-to-reveal vocabulary card game — no wordsearch grid exists in any DT deck or print pack, though the suite SoW promises 'a subject-specific wordsearch' every week.
- Proposed: rename to 'Word cards — settle in' on the We Do 1 header and Starter game card, or add a real wordsearch grid to the print pack; align the SoW either way.
- Source: DT_Community_Upcycling/Scheme_of_Work.html standard-blueprint bullet and Weekly_Plan.html per-week wordsearch names; grep across all six decks finds no wordsearch grid — the only 'wordsearch' strings are W1's two titles.

## AMBIGUOUS / pitch / UNVERIFIED flags (appendix)

**XA1 · Art_Teesside/Build/Spring1_Scheme_of_Work.html** (A-fact, doc; UNVERIFIED)
- Current: “The <b>Skill Deck</b> (eight printed tiles of skills taught this year) is the recovery route for Week 1”
- Issue: The count 'eight' cannot be verified: no eight-tile Skill Deck exists anywhere in the estate — A2 W7 (the built source of the deck) defines it only as 'The printed set of skills taught this year, to choose from' with no count, and the same unverifiable 'eight' is echoed in the Spring 1 pack W1 recovery route ('eight things taught across this year, one per tile').
- Proposed: soften both mentions to "the printed tiles of skills taught this year", or pin the deck at eight tiles when Spring 1 is unpaused (do not build it now — Spring 1 is deliberately paused).
- Source: Estate-wide grep for 'Skill Deck': defined only in Build/BUILD_ART_A2_W7_Bank_It_and_Plan_the_Teach.html with no tile count; no tile set printed in any A2 material

**XA2 · Build/Slideshows/BUILD_HUM_W1_Human_Timeline.html** (A-fact, both; AMBIGUOUS)
- Current: “1911 · Edwardian era”
- Issue: We Do 2 match target (correct answer for 'Transporter Bridge opens', repeated in the print-wedo section) labels 1911 as the Edwardian era; Edward VII died in May 1910, so October 1911 is strictly George V's reign (the loose 'long Edwardian' usage to 1914 exists but conflicts with the standard 1901-1910 period label).
- Proposed: 1911 · Early 20th century
- Source: Edwardian era 1901–1910; Transporter Bridge opened 17 Oct 1911 — verified knowledge; brief anchor list gives the same dates.

**XA3 · Build/Slideshows/BUILD_HUM_W1_Human_Timeline.html** (A-fact, print; AMBIGUOUS)
- Current: “Ironstone found in the Eston Hills, 1850 — Middlesbrough boomed from ~40 farmers to an iron town.”
- Issue: KO Key Fact compresses two decades: the ~40 figure is 1829; by 1850 Middlesbrough was already a coal-port town of roughly 7,000 (founded 1830, Port Darlington/St Hilda's), so it did not boom 'from ~40 farmers' when ironstone was found.
- Proposed: 'Ironstone found in the Eston Hills, 1850 — the young coal port of Middlesbrough (begun 1830) boomed into an iron town.'
- Source: Middlesbrough pop. ~40 in 1829, ~5,400 in 1841, ~7,600 in 1851; coal port established 1830 — verified knowledge; brief anchor 'Middlesbrough's founding/growth from 1830 (Port Darlington; St Hilda's)'.

**XA4 · Build/Slideshows/BUILD_HUM_W2_History_Detectives.html** (A-qa, both; AMBIGUOUS)
- Current: “The port was busy that year”
- Issue: We Do 1 sort keys this statement as SUGGESTS, but a single-day photo cannot support a claim about a whole year, and the deck's own I Do 2 teaches that purpose/selection weakens 'the port was always this busy' — 'CAN'T TELL US' is equally defensible, breaking exactly-one-correct-target.
- Proposed: change the pill to 'The port was busy that day'.
- Source: Deck-internal: I Do 2 postcard caveat and the taught SHOWS/SUGGESTS/CANNOT definitions in the print reference zone.

**XA5 · Build/Slideshows/BUILD_HUM_W3_Why_People_Came.html** (A-qa, both; AMBIGUOUS)
- Current: “⛪ A Welsh chapel already here”
- Issue: We Do 1 keys this as NETWORK, but the deck's own taught decision rule (print reference 'HOME TEST': something AT THE NEW PLACE inviting them over → PULL; a PERSON who showed the way → NETWORK) classifies a chapel at the destination as PULL, so Supported pupils applying the taught test get marked wrong — two defensible targets.
- Proposed: change pill to '✉️ Friends from chapel wrote: join us' (clearly a person/network), or extend the taught test to include 'a community you already belong to → NETWORK'.
- Source: Deck-internal contradiction between the sort key and the print reference zone's PUSH/PULL/NETWORK test.

**XA6 · Build/Slideshows/BUILD_HUM_W5_Big_Deal.html** (A-qa, both; AMBIGUOUS)
- Current: “Which event made Middlesbrough grow from 40 people?”
- Issue: Exit (Supported) keys 'Ironstone found, 1850' as the event that made Middlesbrough grow from 40 people, but the growth from ~40 (1829) began with the 1830 railway extension/coal port — by 1850 the town already held thousands; ironstone drove the later boom to 90,000.
- Proposed: reword stem to 'Which 1850 discovery turned Middlesbrough into a booming iron town?' (answer key unchanged).
- Source: Middlesbrough founded as coal port 1830; pop. ~5,400 by 1841 before the 1850 Eston ironstone find — verified knowledge; brief anchor 'founding/growth from 1830'.

**XA7 · Build/Slideshows/BUILD_HUM_W5_Big_Deal.html** (A-fact, both; AMBIGUOUS)
- Current: “NUMBERS · a town of thousands from 40”
- Issue: We Do 2 match target keyed to 'Ironstone found, 1850' repeats the conflation that the town went from 40 people because of the 1850 find (the 40→thousands step happened 1830-1850 as a coal port; 1850 took it from thousands to 90,000).
- Proposed: 'NUMBERS · 90,000 people by 1901' (still uniquely matchable to the ironstone pill).
- Source: Same population evidence as previous finding — verified knowledge.

**XA8 · Build/Slideshows/BUILD_HUM_W6_Plan_The_Story.html** (A-fact, screen; AMBIGUOUS)
- Current: “the railway arrives, 1825, and gives the place a reason to exist”
- Issue: I Do 1 worked plan: the 1825 S&DR ran Stockton-Darlington; the railway 'arrived' at Middlesbrough via the 1830 Port Darlington extension, which is what actually gave the place its reason to exist — and in a lesson about sequencing, this Set-up (1825) is narrated after an Opening dated 1829.
- Proposed: 'the railway reaches the Tees in 1825, and its 1830 extension gives this spot a reason to exist'.
- Source: S&DR opened 27 Sep 1825 (Stockton-Darlington); Middlesbrough branch/Port Darlington opened Dec 1830 — verified knowledge.

**XA9 · Launch/Slideshows/LAUNCH_HUM_W2_Cause_Consequence_Courtroom.html** (A-qa, both; AMBIGUOUS)
- Current: “⚓ The navigable Tees itself”
- Issue: We Do 1 sorter locks this pill to CONTRIBUTING (data-cat="con") and marks DECISIVE as wrong, but by the deck's own remove-the-cause test a decisive reading is defensible — Middlesbrough was sited in 1830 precisely for navigable deep water (Port Darlington), so without the navigable Tees the port town and its boom arguably never happen there at all.
- Proposed: reword the pill so the contributing reading is unambiguous, e.g. '⚓ River shipping up the Tees (coastal sea routes already existed)' — mirroring how the I Do argues the rail down to contributing.
- Source: Deck's own I Do 2 counterfactual method; Middlesbrough founded 1830 as Port Darlington for deeper-water access than Stockton — verified knowledge

**XA10 · Launch/Slideshows/LAUNCH_HUM_W6_Structured_Account.html** (A-qa, both; AMBIGUOUS)
- Current: “Name the four blueprint zones.”
- Issue: Arrival supported Q2 is tagged (Recall) but 'blueprint zones' is GROW-pathway vocabulary (GROW W6 Plan the Account / GROW W7) that appears nowhere in LAUNCH W1–W5, so a supported LAUNCH pupil has never met the term being recalled; the question also prints in the supported arrival pack.
- Proposed: replace with a LAUNCH-native recall, e.g. 'An essay's claim that every sentence serves is called the…?' (answer: thesis) or reword to 'An account runs opening → body → counter → close: name the four parts' without the 'blueprint' label.
- Source: grep: 'blueprint' occurs in LAUNCH suite only in this deck (lines 98/168) but 39 times across GROW_HUM_W6_Plan_The_Account.html and GROW_HUM_W7_Write_The_Account.html

**XA11 · Launch/Slideshows/LAUNCH_HUM_W6_Structured_Account.html** (A-fact, screen; AMBIGUOUS)
- Current: “yet ore made nothing for eighty years until hands arrived”
- Issue: I Do 2 model turn: the 'eighty years' figure has no anchor (main-seam ironstone was found in 1850 and worked almost immediately) and contradicts the same argument as modelled in W2 ('ore sat unmined for centuries').
- Proposed: 'yet ore made nothing for centuries until hands arrived' — aligning with W2's phrasing.
- Source: LAUNCH_HUM_W2 I Do 2: 'ore sat unmined for centuries; only PEOPLE changed that'; Eston main seam discovered June 1850 and mined from that year — verified knowledge

**XA12 · Launch/Slideshows/LAUNCH_HUM_W7_Source_Assessment.html** (A-qa, both; AMBIGUOUS)
- Current: “Equal time on a source you rate lightly”
- Issue: We Do 1 sorter classes this as a WEAK assessed move, but the deck's own trained route prescribes exactly equal time per source ('~5 read · 15 + 15 per source · 8 verdict · 2 check' in arrival standard A4, the I Do route diagram, and the Standard task steps) — a pupil who follows the route as taught is told their move is weak.
- Proposed: reword the pill to target coverage rather than the timetable, e.g. 'Writing as much ABOUT a source you rate lightly as about your key source', or reconcile with the clock rule explicitly.
- Source: Same deck: arrival standard Q4 answer, I Do 1 route SVG (15 min per source), print-scaffold-standard Route Card '5 read · 15 Source A … 15 Source B'

**XA13 · Launch/Slideshows/LAUNCH_HUM_W7_Source_Assessment.html** (A-fact, screen; UNVERIFIED)
- Current: “Last term's ballot changed this one.”
- Issue: Lundy INFLUENCE box asserts as fact that a previous term's post-assessment ballot altered this assessed-week design; the suite is dated Autumn 1 2026–27 and the repo holds no record of an earlier run, so if this is the scheme's first term the promise is fabricated history — a real problem for a framework whose stated principle is that pupil influence is real.
- Proposed: if no prior ballot happened, soften to a forward promise only, e.g. 'Post-assessment ballot: the ONE change to assessed-week design for next term — your vote is logged and honoured.'
- Source: Could not verify: Tracker/SoW date the programme Autumn 1 2026–27 with no earlier-run record in the repo; settled by Matt confirming whether a 2025–26 LAUNCH assessed-week ballot occurred

**XA14 · Launch/Slideshows/LAUNCH_HUM_W8_OS_Map_Skills.html** (A-fact, both; UNVERIFIED)
- Current: “Last year's cohort put THIS map week here.”
- Issue: Lundy INFLUENCE box (slide and print-lundy table) asserts a 2025–26 cohort's term review placed the map week in this SoW; the scheme is dated 2026–27 and the repo contains no earlier-run evidence — if untrue, this manufactures the very 'real influence' the Lundy loop promises. (Contrast: the decks' reconstructed sources are properly caveated as illustrative.)
- Proposed: if no prior cohort review occurred, drop the sentence or recast as 'your review can move weeks like this one — it goes to the SoW meeting with your name on it.'
- Source: Could not verify: Pathway_Tracker.html and SoW date the programme Autumn 1 2026–27; no prior-year LAUNCH humanities artefacts in repo; settled by author confirmation

**XA15 · Grow/Slideshows/GROW_HUM_W1_Time_Detectives.html** (A-qa, screen; AMBIGUOUS)
- Current: “data-correct="victorian" onclick="pickTarget(this)">1911 — Edwardian, not”
- Issue: We Do 2 match target teaches '1911 — Edwardian, not Victorian', which the deck's own period table (Edwardian 1901–1910) contradicts; defensible only under the loose extended-Edwardian usage the deck never introduces.
- Proposed: reword target to "1911 — not Victorian (Victoria died 1901)" so the tested error is provable without the shaky Edwardian claim.
- Source: Deck-internal consistency vs Edwardian era 1901–1910; extended usage to 1914 exists but is untaught — verified knowledge

**XA16 · Grow/Slideshows/GROW_HUM_W1_Time_Detectives.html** (A-qa, screen; AMBIGUOUS)
- Current: “1911 is Edwardian; the period label fails.”
- Issue: Exit ticket Standard Q3 answer key asserts '1911 is Edwardian' — a pupil applying the deck's own Edwardian 1901–1910 table would rightly answer '1911 is after the Edwardian era' and be contradicted by the key.
- Proposed: key e.g. "Victoria died in 1901 — 1911 cannot be Victorian (strictly it is even after Edward VII, d. 1910)."
- Source: Deck's own Reference Zone period table + reign dates — verified knowledge

**XA17 · Grow/Slideshows/GROW_HUM_W3_Cause_And_Consequence.html** (A-qa, screen; AMBIGUOUS)
- Current: “<div class="sort-pill" data-cat="cond" onclick="selectSort(this)">🥔 Failed harvests in Ireland</div>”
- Issue: We Do 1 sorter keys 'Failed harvests in Ireland' as CONDITION only, but the same deck teaches the famine is 'Mostly trigger (crisis) on top of conditions' (arrival Standard key) and 'Crisis — condition and trigger at once' (We Do 2 target), so a pupil following the deck's own teaching who taps TRIGGER is marked wrong — two deck-endorsed targets.
- Proposed: replace the pill with an unambiguous condition (e.g. "Years of rural poverty in Ireland") or key the pill to accept both categories.
- Source: Same deck: arrival Standard Q3 answer and We Do 2 famine target; exit Standard Q1 'Why can the famine be condition AND trigger?'

**XA18 · Grow/Slideshows/GROW_HUM_W7_Write_The_Account.html** (C-construction, print; AMBIGUOUS)
- Current: “Paragraph 2 (row 2):”
- Issue: Supported assessed worksheet provides slots only for Paragraph 1 (row 1) and Paragraph 2 (row 2) plus frames, while its own on-screen steps say 'one paragraph per plan row' and the W6 Supported blueprint records three unit strips — sheet and steps disagree (may be a deliberate Supported reduction, but then the steps line is wrong).
- Proposed: add "Paragraph 3 (row 3):" with print-lines, or amend the Supported steps to "one paragraph for each of your two strongest plan rows".
- Source: Same deck Supported task steps; W6 print-worksheet-supported 'Unit strips (3) + evidence partners'

**XA19 · Grow/Slideshows/GROW_HUM_W8_Where_In_The_World.html** (A-qa, screen; AMBIGUOUS)
- Current: “Does 800 ≠ 60 change 'why they”
- Issue: Starter card contrasts 800 miles with 60 miles, but no 60-mile journey exists anywhere in the deck (the taught journeys are Mayo ~330, Merthyr ~260, Gdańsk ~800) — the comparison figure is unanchored for pupils.
- Proposed: "Does 800 ≠ 260 change 'why they came'?" or first add a ~60-mile local journey (e.g. from the Durham coalfield) to the cards.
- Source: Same slide's three distance cards and the KO Key Fact 'Mayo ~330 miles; Merthyr ~260; Gdańsk ~800'

**XA20 · Grow/Slideshows/GROW_HUM_W8_Where_In_The_World.html** (A-qa, both; AMBIGUOUS)
- Current: “What did Week 8 BUILD call the map's limit?”
- Issue: Arrival Standard Q4 asks GROW pupils to recall content from the parallel BUILD pathway's same-week lesson (a different class, delivered the same week), and the key 'It shows the road, not the reason.' is a paraphrase — BUILD W8's actual line is 'the map shows the road; the letter shows the reason.'
- Proposed: reword to "Finish the line: 'the map shows the road; the ___ shows the reason'" (answer: letter) and drop the cross-pathway attribution.
- Source: Build/Slideshows/BUILD_HUM_W8_Where_In_The_World.html (phrase grep: 'the map shows the road; the letter shows the reason.'); Lundy AUDIENCE lines show BUILD is a separate class

**XA21 · Humanities_Teesside/BUILD_Scheme_of_Work.html** (A-fact, doc; UNVERIFIED)
- Current: “AQA UAS &#x27;History around us&#x27;”
- Issue: Could not verify that AQA's Unit Award Scheme has a unit titled 'History around us' — that name is best known as the OCR SHP GCSE B site-study component — and the same label appears in the GROW and LAUNCH SoW subtitles.
- Proposed: confirm the exact registered UAS unit title/code with the centre (each SoW's assessor note already requires matching the exact unit code/version); no text change until confirmed.
- Source: Verified knowledge: 'History Around Us' is the OCR B (SHP) GCSE component name; AQA UAS units are code-numbered and centre-selected — offline, cannot enumerate UAS unit titles.

**XA22 · Build/Slideshows/BUILD_DT_W1_Workshop_Audit.html** (D-alignment, both; UNVERIFIED)
- Current: “🏅 Banks: ASDAN Vocational / D&amp;T module evidence”
- Issue: All six decks claim banking into an 'ASDAN Vocational / D&T module' but no such named ASDAN product exists anywhere in the estate — the suite SoW says the exact module codes are still to confirm locally, W6's own staff facts panel names only FoodWise/Living Independently/Careers Short Courses + AQA UAS, and if the intended target is an ASDAN Vocational Taster that product line is being withdrawn (
- Proposed: once the coordinator confirms the target, name it (e.g. a specific AQA UAS unit or named ASDAN Short Course) in the award strip, KO headers and witness sheets of all six decks; until then soften to 'Banks: vocational portfolio evidence (ASDAN/AQA UAS — module TBC)'.
- Source: SPEC_FACTS.md §19 (all Vocational Taster titles being withdrawn; dates); DT_Community_Upcycling/Scheme_of_Work.html 'Before you teach' ('the exact ASDAN Vocational/D&T module codes these map to'); BUILD_DT_W6 title staff

**XA23 · Build/Slideshows/BUILD_DT_W1_Workshop_Audit.html** (C-construction, print; AMBIGUOUS)
- Current: “An adult checks and signs that your station is safe”
- Issue: The W1 Knowledge Organiser defines SIGN OFF as adult-only, but the same deck's Stretch task and witness-sheet Stretch descriptor have the pupil running the safety check on a peer's station and signing it off.
- Proposed: KO row → 'A check you put your name to — an adult signs your station; at Stretch you may check and sign a classmate's.'
- Source: Same file: Stretch task 'run the safety check on someone ELSE's station and sign it off' and witness STRETCH descriptor. Classroom-station sign-off, not ASDAN unit sign-off, so no spec breach — but the KO contradicts the

## SOW-SIDE (appendix)

**XO1 · Humanities_Teesside/BUILD_Scheme_of_Work.html** (D-alignment, doc; SOW-SIDE)
- Current: “no sorts or retrieval quizzes”
- Issue: The SoW's 'How these lessons were upgraded' section describes a deck architecture that does not exist in the deployed BUILD_HUM decks: it claims the engine has 'no sorts or retrieval quizzes ... so none were added', yet every week has a We Do sort, a match round and a three-tier retrieval Arrival grid; the described Reading toggle, stamped ticket, Lundy loop ring, Inherited/Feeds spine band, 'Not 
- Proposed: rewrite the SoW's enhancement-layer section to describe the deployed 10-slide Made-by-Matt chassis (or flag for the hum-docs fixer) — the error lives in the SoW, not the lessons.
- Source: Grep of all 8 decks for 'specialist', 'Reading', 'ticket', 'Inherited', 'Feeds', 'Calm Mode' returned zero; every deck contains sort-pills, match-pills and Arrival retrieval grids.

**XO2 · Humanities_Teesside/LAUNCH_Scheme_of_Work.html** (D-alignment, doc; SOW-SIDE)
- Current: “AQA UAS &#x27;History around us&#x27; + GCSE AO bridge”
- Issue: The suite brief states 'the SoW names no board', but the LAUNCH SoW subtitle (and BUILD/GROW SoWs and printable packs) names AQA UAS; AQA UAS is the Unit Award Scheme (accreditation, not GCSE grading), and 'History Around Us' is also the name of an OCR GCSE B component, so the UAS unit title could not be verified. The 8 LAUNCH decks themselves contain zero board names or grade language (grep-confi
- Proposed: no deck change; brief/SoW discrepancy recorded for the fixer — verify 'History around us' against the registered AQA UAS unit list before teaching (the SoW itself already instructs matching to the exact registered unit).
- Source: BRIEF_HUM ('the SoW names no board'); LAUNCH_Scheme_of_Work.html line 8; grep AQA|Edexcel|OCR across LAUNCH_HUM decks = 0 hits; 'History Around Us' is an OCR SHP GCSE B component name — verified knowledge

**XO3 · Humanities_Teesside/GROW_Scheme_of_Work.html** (D-alignment, doc; SOW-SIDE)
- Current: “How can dates, periods and intervals help us build *and challenge* chronology?”
- Issue: SoW weekly enquiry wording lags the deployed decks in 7 of 8 weeks (W1 'chronology' vs decks' 'chronological claims'; W2 'or' vs 'and'; W3 no 'shape…and its consequences'; W5 'how big a deal' vs 'it depends…about significance'; W6 no 'coherent, qualified'; W7 'qualified uncertainty' vs 'a qualified judgement'; W8 no 'of migration') — decks and Pathway_Tracker agree with each other throughout, so t
- Proposed: regenerate the SoW week enquiries from the deployed decks (the Tracker already states it is generated from them); W4 needs no change.
- Source: Compared GROW_Scheme_of_Work.html weeks 1–8 vs on-deck enquiries and Pathway_Tracker.html rows (all three read in full)

**XO4 · Humanities_Teesside/GROW_Scheme_of_Work.html** (D-alignment, doc; SOW-SIDE)
- Current: “GROW Humanities — Teesside Migration &amp;amp; Identity (The History Studio)”
- Issue: SoW file double-escapes ampersands in its h1 and 'Connected studio journey' line (renders literally as '…Migration &amp; Identity') and uses literal markdown asterisks for emphasis (*defensible history*, *and challenge*, *the same zone hues…*) that render as asterisks in HTML — display defects in the staff-facing SoW, not the lessons.
- Proposed: replace '&amp;amp;' with '&amp;' (2 places) and swap *…* emphasis for <em>…</em> in the SoW file.
- Source: Raw file inspection of GROW_Scheme_of_Work.html lines 7, 11, 14, 22

**XO5 · DT_Community_Upcycling/Weekly_Plan.html** (D-alignment, doc; SOW-SIDE)
- Current: “MODEL: Fatal Four + safe handling”
- Issue: The Weekly Plan's W1 flow names 'Fatal Four' — an industry term for the four fatal construction risks (falls, struck-by, electrocution, caught-between) — but the shipped W1 deck teaches four bench-scale hazard families (sharp, trip, dust, lift) and never mentions 'Fatal Four'.
- Proposed: 'MODEL: four hazard families (sharp, trip, dust, lift) + safe handling'
- Source: BUILD_DT_W1 'I Do 1 — The Model — Sharp, Trip, Dust, Lift'; 'Fatal Four' is HSE/OSHA construction-fatality terminology — verified knowledge. Error lives in the plan, not the lesson.

**XO6 · DT_Community_Upcycling/Scheme_of_Work.html** (D-alignment, doc; SOW-SIDE)
- Current: “a 2×2 retrieval grid + a subject-specific <b>wordsearch</b> (no crosswords) to settle the room”
- Issue: The SoW's standard lesson blueprint promises a 2×2 retrieval grid plus a weekly wordsearch, but every shipped deck opens with a three-question tiered retrieval quiz and a different tap-card game each week — no grid, no wordsearch.
- Proposed: 'a three-question tiered retrieval quiz + a subject-specific word game to settle the room and build vocational vocabulary.'
- Source: All six BUILD_DT decks: Arrival Task = 3 task-boxes per tier; We Do 1 games are Wordsearch(cards)/Match it up/Odd one out/Put it in order/Sort it/Team quiz. Error lives in the SoW.

**XO7 · DT_Community_Upcycling/Scheme_of_Work.html** (D-alignment, doc; SOW-SIDE)
- Current: “differentiated <b>Standard</b> and <b>Supported</b> tasks (toggle in the pack)”
- Issue: The SoW describes two differentiation tiers, but every shipped deck (and its print packs, witness sheets and toggles) runs three: Supported / Standard / Stretch.
- Proposed: 'differentiated <b>Supported</b>, <b>Standard</b> and <b>Stretch</b> tasks (toggle in the pack)' — Weekly_Plan.html's footer 'Standard + Supported in every pack' needs the same update.
- Source: All six BUILD_DT decks: level-toggle buttons, print-scaffold/worksheet sections and witness 'ring ONE' tables carry three tiers. Error lives in the SoW/plan.

