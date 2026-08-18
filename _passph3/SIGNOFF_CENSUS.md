# PH-3 SIGNOFF CENSUS — every `sign off` / `sign-off` occurrence, classified (REPORT-ONLY except the seven A5 lines)

Method: regex `sign[ -]off` case-insensitive over the 101 ASDAN-tree surfaces plus the two D&T route
files; **93 occurrences in 44 files** (§2.1's "≈109" double-counts the case variants by its own method —
same population). Classes: `pupil-task` / `staff` / `heading-title` / `answer-key` / `filename` /
`game-data`. The only sign-off EDITS in PH-3 are the seven A5 one-liners (verified equivalent
corrections recovered read-only from `ab7730c`); everything below is classification + proposal.

## The patterns, judged

1. **BUILD evidence-step lines — `Witness: staff sign off …`** (one per BUILD lesson, W1–W7).
   The A5 seven (Careers W6, COMM W6, DUKE W6, FW W5, FW W6, LI W6, D&T W6) are now
   "staff **prepare** … **for assessor sign-off**". The remaining ~24 sibling lines in W1–W5/W7
   lessons carry the identical pattern. **Proposal (awaiting Matt):** apply the same rewording
   estate-wide; only the seven PH-1R-verified lines were authorised this pass.
2. **`LAUNCH_ASDAN/PEQ/PEQ_W6_Review_Progress_and_Sign_Off_the_Unit.html`** — the FILENAME and the
   lesson title claim the lesson signs off the unit; the sign-off is the assessor's act (the deck's own
   §4 witness block says so correctly). Filename is never renamed (hub/SoW/catalogue links) — recorded
   question, redirect plan needed if ever renamed (OPEN_ITEMS 42). Title/headings: proposal —
   "Review Progress and Prepare the Unit for Sign-Off" if ever retitled with the filename question.
3. **PEQ W6 I Do 1 step** — "Name future use, and sign off." + "…the unit is complete and ready to
   hand to the assessor" *(step body)*: the step heading tells the pupil they sign off; **proposal:**
   "Name future use — ready for assessor sign-off." Not edited: pupil-slide text outside A2's measured
   claim scope.
4. **Green-Light Board contexts** (GCOMM W5/W6 ×27, GROW S&R, GROW R&T, GCOMM START_HERE): the
   sign-off is the staff/partner **plan** approval on the project board (needs → decision → plan →
   sign-off) — no qualification-certification authority claimed. **Leave.**
5. **Assessor Witness Statement blocks** (PEQ W5/W6, D&T W6, LAUNCH SoW/START_HERE checklist lines):
   correct usage — sign-off routed to the assessor. **Leave.**
6. **Game data** (match pills `SIGN-OFF`, We Do 2 print mirrors, cold-call pools, TA briefs, `<title>`
   tags, lesson-complete overlays, print pack headers that mirror the lesson title): carry the
   filename/title wording — resolve with pattern 2's question, not by editing game data.
7. **D&T W6 note:** the (now A5-corrected) line still ends "completed portfolio + **predicted grade**";
   ASDAN Short Courses and AQA UAS carry no grade — flagged for Matt as a wording question (not a
   sign-off claim, out of A5 scope).

## Full enumeration

| file | @byte | class | context (trimmed) |
|---|---|---|---|
| `BUILD_ASDAN/Careers/CAREERS_W1_My_Strengths.html` | 316362 | staff wording | …ion."},{"id":"s3","label":"Complete the authorised quality and safety sign-off route.","reason":"Pupil self-check does not replace responsible-adult… |
| `BUILD_ASDAN/Careers/CAREERS_W2_Jobs_in_My_Community.html` | 315059 | staff wording | …ion."},{"id":"s3","label":"Complete the authorised quality and safety sign-off route.","reason":"Pupil self-check does not replace responsible-adult… |
| `BUILD_ASDAN/Careers/CAREERS_W3_Skills_Employers_Want.html` | 317267 | staff wording | …ion."},{"id":"s3","label":"Complete the authorised quality and safety sign-off route.","reason":"Pupil self-check does not replace responsible-adult… |
| `BUILD_ASDAN/Careers/CAREERS_W4_Routines_and_Reliability.html` | 317179 | staff wording | …ion."},{"id":"s3","label":"Complete the authorised quality and safety sign-off route.","reason":"Pupil self-check does not replace responsible-adult… |
| `BUILD_ASDAN/Careers/CAREERS_W5_Applying_Myself.html` | 321805 | staff wording | …ion."},{"id":"s3","label":"Complete the authorised quality and safety sign-off route.","reason":"Pupil self-check does not replace responsible-adult… |
| `BUILD_ASDAN/Careers/CAREERS_W6_My_Career_Profile.html` | 102801 | heading/title | …s="v5-step"><h3>Witness</h3><p>staff prepare the profile for assessor sign-off as portfolio evidence.</p></div></div> <div class="wit-panel" style="… |
| `BUILD_ASDAN/Careers/CAREERS_W6_My_Career_Profile.html` | 320517 | staff wording | …ion."},{"id":"s3","label":"Complete the authorised quality and safety sign-off route.","reason":"Pupil self-check does not replace responsible-adult… |
| `BUILD_ASDAN/Careers/CAREERS_W7_After_Year_11.html` | 318423 | staff wording | …ion."},{"id":"s3","label":"Complete the authorised quality and safety sign-off route.","reason":"Pupil self-check does not replace responsible-adult… |
| `BUILD_ASDAN/Community_Project/COMM_W1_Choose_Our_Asset.html` | 316455 | staff wording | …ion."},{"id":"s3","label":"Complete the authorised quality and safety sign-off route.","reason":"Pupil self-check does not replace responsible-adult… |
| `BUILD_ASDAN/Community_Project/COMM_W2_The_Site's_Need.html` | 315204 | staff wording | …ion."},{"id":"s3","label":"Complete the authorised quality and safety sign-off route.","reason":"Pupil self-check does not replace responsible-adult… |
| `BUILD_ASDAN/Community_Project/COMM_W3_Our_Team_Roles.html` | 315395 | staff wording | …ion."},{"id":"s3","label":"Complete the authorised quality and safety sign-off route.","reason":"Pupil self-check does not replace responsible-adult… |
| `BUILD_ASDAN/Community_Project/COMM_W4_Partner_Update.html` | 315208 | staff wording | …ion."},{"id":"s3","label":"Complete the authorised quality and safety sign-off route.","reason":"Pupil self-check does not replace responsible-adult… |
| `BUILD_ASDAN/Community_Project/COMM_W5_Plan_the_Handover.html` | 316571 | staff wording | …ion."},{"id":"s3","label":"Complete the authorised quality and safety sign-off route.","reason":"Pupil self-check does not replace responsible-adult… |
| `BUILD_ASDAN/Community_Project/COMM_W6_The_Handover_and_Its_Benefit.html` | 103171 | heading/title | …><h3>Witness</h3><p>staff prepare the community evidence for assessor sign-off.</p></div></div> <div class="wit-panel" style="margin-top:14px;border… |
| `BUILD_ASDAN/Community_Project/COMM_W6_The_Handover_and_Its_Benefit.html` | 315568 | staff wording | …ion."},{"id":"s3","label":"Complete the authorised quality and safety sign-off route.","reason":"Pupil self-check does not replace responsible-adult… |
| `BUILD_ASDAN/Duke_and_Enterprise/DUKE_W1_Choose_My_Challenges.html` | 316055 | staff wording | …ion."},{"id":"s3","label":"Complete the authorised quality and safety sign-off route.","reason":"Pupil self-check does not replace responsible-adult… |
| `BUILD_ASDAN/Duke_and_Enterprise/DUKE_W2_A_Kindness_Challenge.html` | 314951 | staff wording | …ion."},{"id":"s3","label":"Complete the authorised quality and safety sign-off route.","reason":"Pupil self-check does not replace responsible-adult… |
| `BUILD_ASDAN/Duke_and_Enterprise/DUKE_W3_An_Eco_Challenge.html` | 316060 | staff wording | …ion."},{"id":"s3","label":"Complete the authorised quality and safety sign-off route.","reason":"Pupil self-check does not replace responsible-adult… |
| `BUILD_ASDAN/Duke_and_Enterprise/DUKE_W4_An_Independence_Challenge.html` | 315635 | staff wording | …ion."},{"id":"s3","label":"Complete the authorised quality and safety sign-off route.","reason":"Pupil self-check does not replace responsible-adult… |
| `BUILD_ASDAN/Duke_and_Enterprise/DUKE_W5_Our_Social_Enterprise.html` | 316987 | staff wording | …ion."},{"id":"s3","label":"Complete the authorised quality and safety sign-off route.","reason":"Pupil self-check does not replace responsible-adult… |
| `BUILD_ASDAN/Duke_and_Enterprise/DUKE_W6_Pitch_and_Reflect.html` | 103388 | heading/title | …h3>Witness</h3><p>staff prepare the completed challenges for assessor sign-off.</p></div></div> <div class="wit-panel" style="margin-top:14px;border… |
| `BUILD_ASDAN/Duke_and_Enterprise/DUKE_W6_Pitch_and_Reflect.html` | 315909 | staff wording | …ion."},{"id":"s3","label":"Complete the authorised quality and safety sign-off route.","reason":"Pupil self-check does not replace responsible-adult… |
| `BUILD_ASDAN/FoodWise/FW_W1_Food_Groups.html` | 316068 | staff wording | …ion."},{"id":"s3","label":"Complete the authorised quality and safety sign-off route.","reason":"Pupil self-check does not replace responsible-adult… |
| `BUILD_ASDAN/FoodWise/FW_W2_A_Balanced_Plate.html` | 314774 | staff wording | …ion."},{"id":"s3","label":"Complete the authorised quality and safety sign-off route.","reason":"Pupil self-check does not replace responsible-adult… |
| `BUILD_ASDAN/FoodWise/FW_W3_Reading_Labels.html` | 315838 | staff wording | …ion."},{"id":"s3","label":"Complete the authorised quality and safety sign-off route.","reason":"Pupil self-check does not replace responsible-adult… |
| `BUILD_ASDAN/FoodWise/FW_W4_Kitchen_Hygiene_and_Safety.html` | 315505 | staff wording | …ion."},{"id":"s3","label":"Complete the authorised quality and safety sign-off route.","reason":"Pupil self-check does not replace responsible-adult… |
| `BUILD_ASDAN/FoodWise/FW_W5_Prepare_a_Healthy_Snack.html` | 103889 | heading/title | …ss</h3><p>staff prepare the practical + hygiene evidence for assessor sign-off.</p></div></div> <div class="wit-panel" style="margin-top:14px;border… |
| `BUILD_ASDAN/FoodWise/FW_W5_Prepare_a_Healthy_Snack.html` | 316798 | staff wording | …ion."},{"id":"s3","label":"Complete the authorised quality and safety sign-off route.","reason":"Pupil self-check does not replace responsible-adult… |
| `BUILD_ASDAN/FoodWise/FW_W6_Plan_a_Healthy_Meal.html` | 103203 | heading/title | …h3>Witness</h3><p>staff prepare the FoodWise M1 evidence for assessor sign-off.</p></div></div> <div class="wit-panel" style="margin-top:14px;border… |
| `BUILD_ASDAN/FoodWise/FW_W6_Plan_a_Healthy_Meal.html` | 315569 | staff wording | …ion."},{"id":"s3","label":"Complete the authorised quality and safety sign-off route.","reason":"Pupil self-check does not replace responsible-adult… |
| `BUILD_ASDAN/Living_Independently/LI_W1_Where_Money_Comes_From.html` | 316536 | staff wording | …ion."},{"id":"s3","label":"Complete the authorised quality and safety sign-off route.","reason":"Pupil self-check does not replace responsible-adult… |
| `BUILD_ASDAN/Living_Independently/LI_W2_Notes_and_Coins.html` | 313941 | staff wording | …ion."},{"id":"s3","label":"Complete the authorised quality and safety sign-off route.","reason":"Pupil self-check does not replace responsible-adult… |
| `BUILD_ASDAN/Living_Independently/LI_W3_Needs_vs_Wants.html` | 315199 | staff wording | …ion."},{"id":"s3","label":"Complete the authorised quality and safety sign-off route.","reason":"Pupil self-check does not replace responsible-adult… |
| `BUILD_ASDAN/Living_Independently/LI_W4_Everyday_Prices.html` | 316421 | staff wording | …ion."},{"id":"s3","label":"Complete the authorised quality and safety sign-off route.","reason":"Pupil self-check does not replace responsible-adult… |
| `BUILD_ASDAN/Living_Independently/LI_W5_A_Simple_Budget.html` | 316392 | staff wording | …ion."},{"id":"s3","label":"Complete the authorised quality and safety sign-off route.","reason":"Pupil self-check does not replace responsible-adult… |
| `BUILD_ASDAN/Living_Independently/LI_W6_Shopping_and_Change.html` | 103338 | heading/title | …itness</h3><p>staff prepare the LI M1 practical evidence for assessor sign-off.</p></div></div> <div class="wit-panel" style="margin-top:14px;border… |
| `BUILD_ASDAN/Living_Independently/LI_W6_Shopping_and_Change.html` | 315555 | staff wording | …ion."},{"id":"s3","label":"Complete the authorised quality and safety sign-off route.","reason":"Pupil self-check does not replace responsible-adult… |
| `GROW_ASDAN/Community_Project/GCOMM_W1_Our_Patch_Our_Say.html` | 96170 | staff wording | … Green-Light Board runs the whole project — needs → decision → plan → sign-off, visible all term.", "Exit Ticket": "Answers independent — celebrate … |
| `GROW_ASDAN/Community_Project/GCOMM_W3_Roles_Steps_Resources.html` | 46582 | answer key | …ass="answer">Own trace — usually the partner confirmation or the risk sign-off; everything downstream waits on it.</p></div><div class="task-box ani… |
| `GROW_ASDAN/Community_Project/GCOMM_W4_First_Contact.html` | 47179 | answer key | …p><p class="answer">Own rewrite — greeting, full words, specific ask, sign-off; warmth kept, slang retired.</p></div></div> </div><div class="slide"… |
| `GROW_ASDAN/Community_Project/GCOMM_W5_Risk_And_Ready.html` | 58620 | heading/title | …tem">Right tool per risk</span><span class="wagoll-tag" data-trigger="sign-off">Travels to approval</span></div><p id="wagoll-text"></p></div> </div… |
| `GROW_ASDAN/Community_Project/GCOMM_W5_Risk_And_Ready.html` | 65949 | staff wording | …(--ido-border)">Next lesson: Green Light — present the whole plan for sign-off</span></div><button onclick="hideLessonComplete()">Onwards! 🚀</button… |
| `GROW_ASDAN/Community_Project/GCOMM_W5_Risk_And_Ready.html` | 85387 | staff wording | …th a Friday deadline. Grid photographed and off to the Trips & Visits sign-off.'; function startWagoll(){const panel=document.getElementById('wagoll… |
| `GROW_ASDAN/Community_Project/GCOMM_W6_Green_Light.html` | 43070 | answer key | … looks like</h3><ul><li>I can present my part of the project case for sign-off</li><li>I can answer a challenge question with plan evidence</li><li>… |
| `GROW_ASDAN/Community_Project/GCOMM_W6_Green_Light.html` | 45822 | answer key | …m-delay-1"><h3>2. Today's work</h3><p>Today is 'Green Light' — plan → sign-off → aut 2 delivery. What do you think we'll be doing?</p><p class="answ… |
| `GROW_ASDAN/Community_Project/GCOMM_W6_Green_Light.html` | 46123 | answer key | …should be able to say: 'I can present my part of the project case for sign-off.' What will that take today?</p><p class="answer">Name one thing you’… |
| `GROW_ASDAN/Community_Project/GCOMM_W6_Green_Light.html` | 50941 | heading/title | …ything organised.</p></div><div class="v5-step"><h3>Presenting it for sign-off — anticipating the approver’s questions.</h3><p>Presenting for sign-o… |
| `GROW_ASDAN/Community_Project/GCOMM_W6_Green_Light.html` | 51013 | answer key | …ything organised.</p></div><div class="v5-step"><h3>Presenting it for sign-off — anticipating the approver’s questions.</h3><p>Presenting for sign-o… |
| `GROW_ASDAN/Community_Project/GCOMM_W6_Green_Light.html` | 55827 | staff wording | …rget" data-correct="m2" onclick="pickTarget(this)">Trips &amp; Visits sign-off, via the risk assessment — booked four weeks ahead</div></div> <p id=… |
| `GROW_ASDAN/Community_Project/GCOMM_W6_Green_Light.html` | 57033 | staff wording | …oom, to the approver alone, or on paper read aloud by a partner — the sign-off counts the same. Evidence goes in your ASDAN portfolio — Documentaria… |
| `GROW_ASDAN/Community_Project/GCOMM_W6_Green_Light.html` | 59999 | heading/title | …3A;background:#D5A63A14"><h3 style="color:#D5A63A">⭐ INFLUENCE</h3><p>Sign-off here is what makes Aut 2 delivery instead of paperwork.</p></div></di… |
| `GROW_ASDAN/Community_Project/GCOMM_W6_Green_Light.html` | 60921 | answer key | …task-box"><h3>1.</h3><p>I can present my part of the project case for sign-off — true for you today? Say how.</p><p class="answer">Point to today’s … |
| `GROW_ASDAN/Community_Project/GCOMM_W6_Green_Light.html` | 63583 | heading/title | …>📸</span><span>✍️</span></div><h2>Green Light — banked!</h2><p>Plan → sign-off → Aut 2 delivery ✅</p><div class="lc-summary"><span><strong>✓</strong… |
| `GROW_ASDAN/Community_Project/GCOMM_W6_Green_Light.html` | 63709 | answer key | …een Light — banked!</h2><p>Plan → sign-off → Aut 2 delivery ✅</p><div class="lc-summary"><span><strong>✓</strong… |
| `GROW_ASDAN/Community_Project/GCOMM_W6_Green_Light.html` | 63939 | staff wording | … Aut 2</span><span><strong>✓</strong> Onto the Green-Light Board: The sign-off decision comes back to the class — and the board flips f…</span><span… |
| `GROW_ASDAN/Community_Project/GCOMM_W6_Green_Light.html` | 64553 | answer key | …oday’s success: <strong>I can present my part of the project case for sign-off</strong> and <strong>I can answer a challenge question with plan evid… |
| `GROW_ASDAN/Community_Project/GCOMM_W6_Green_Light.html` | 65376 | staff wording | …d><td>Permission to go ahead, once the case is made.</td></tr><tr><td>SIGN-OFF</td><td>The approval that has to be given before delivery.</td></tr><… |
| `GROW_ASDAN/Community_Project/GCOMM_W6_Green_Light.html` | 65916 | staff wording | …d tell the approver if you had one sentence.</li><li>What it changes: Sign-off here is what makes Aut 2 delivery instead of paperwork.</li><li>Launc… |
| `GROW_ASDAN/Community_Project/GCOMM_W6_Green_Light.html` | 67120 | staff wording | …p><div class='print-line'></div><p>2) Today is 'Green Light' — plan → sign-off → aut 2 delivery. What do you think we'll be doing?</p><div class='pr… |
| `GROW_ASDAN/Community_Project/GCOMM_W6_Green_Light.html` | 67305 | staff wording | …should be able to say: 'I can present my part of the project case for sign-off.' What will that take today?</p><div class='print-line'></div></div> … |
| `GROW_ASDAN/Community_Project/GCOMM_W6_Green_Light.html` | 68670 | heading/title | …e board · The dependency — name it and its owner · Trips &amp; Visits sign-off — via the risk assessment</p></div><div id="print-scaffold-supported"… |
| `GROW_ASDAN/Community_Project/GCOMM_W6_Green_Light.html` | 70151 | heading/title | …s ______.</p><p>The step that blocks the most others is ______.</p><p>Sign-off comes from ______.</p><h3>Word bank</h3><p>green light &middot; case … |
| `GROW_ASDAN/Community_Project/GCOMM_W6_Green_Light.html` | 70238 | heading/title | …s ______.</p><p>The step that blocks the most others is ______.</p><p>Sign-off comes from ______.</p><h3>Word bank</h3><p>green light &middot; case … |
| `GROW_ASDAN/Community_Project/GCOMM_W6_Green_Light.html` | 72716 | answer key | …t – Supported</h2><p>1) I can present my part of the project case for sign-off — true for you today? Say how.</p><div class='print-line'></div><p>2)… |
| `GROW_ASDAN/Community_Project/GCOMM_W6_Green_Light.html` | 79271 | staff wording | …yle="width:22%;vertical-align:top"><strong>Influence</strong></td><td>Sign-off here is what makes Aut 2 delivery instead of paperwork.</td></tr></ta… |
| `GROW_ASDAN/Community_Project/GCOMM_W6_Green_Light.html` | 94259 | staff wording | …n?"}, "Exit Ticket":{F:"I can present my part of the project case for sign-off \u2014 true for you today? Say how.",M:"What does 'A green light is e… |
| `GROW_ASDAN/Community_Project/GCOMM_W6_Green_Light.html` | 103870 | staff wording | …The dependency — name it and its owner'},t2:{text:'Trips &amp; Visits sign-off — via the risk assessment'},t3:{text:'We deliver — this term bought t… |
| `GROW_ASDAN/Community_Project/START_HERE.html` | 2407 | staff wording | … · Green Light<br><span style="font-size:.88rem;color:#64748b">Plan → sign-off → Aut 2 delivery</span></a><div class="note">🏅 Wed P3 · banks PEQ cro… |
| `GROW_ASDAN/Resources_and_Tools.html` | 2294 | heading/title | …cs checklist</li><li>The Green-Light Board (needs → decision → plan → sign-off)</li></ul><h2 style="color:#C08A3E">Community &amp; Enterprise · Wedn… |
| `GROW_ASDAN/Scheme_and_Resources.html` | 6428 | staff wording | …idence</td></tr><tr><td><b>W6</b></td><td><b>Green Light</b> — Plan → sign-off → Aut 2 delivery</td><td>I can present my part of the project case fo… |
| `GROW_ASDAN/Scheme_and_Resources.html` | 6508 | staff wording | …idence</td></tr><tr><td><b>W6</b></td><td><b>Green Light</b> — Plan → sign-off → Aut 2 delivery</td><td>I can present my part of the project case fo… |
| `GROW_ASDAN/Scheme_and_Resources.html` | 7313 | heading/title | …cs checklist</li><li>The Green-Light Board (needs → decision → plan → sign-off)</li></ul><h2 style="color:#C08A3E">Community & Enterprise <span styl… |
| `LAUNCH_ASDAN/PEQ/PEQ_W5_Deliver_the_Activity_and_Gather_Evidence.html` | 65100 | staff wording | …tyle:italic;color:var(--ido-border)">Next lesson: Review Progress and Sign Off the Unit — closing Communication (ComSk1)</span></div><button onclick… |
| `LAUNCH_ASDAN/PEQ/PEQ_W6_Review_Progress_and_Sign_Off_the_Unit.html` | 213 | staff wording | … ASDAN · PEQ Level 1 (E3 floor · L2 stretch) W6 · Review Progress and Sign Off the Unit</title> <style> :root{--bg:#fff;--slide-bg:#fff;--text:#1f29… |
| `LAUNCH_ASDAN/PEQ/PEQ_W6_Review_Progress_and_Sign_Off_the_Unit.html` | 42979 | heading/title | … · Personal Effectiveness · Week 6 of 6</span><h1>Review Progress and Sign Off the Unit</h1><p style="font-size:1.05rem;color:var(--muted);margin:-6… |
| `LAUNCH_ASDAN/PEQ/PEQ_W6_Review_Progress_and_Sign_Off_the_Unit.html` | 49307 | staff wording | …y="126" text-anchor="middle" font-size="11" fill="#8E4F82">REVIEW and SIGN OFF</text><g class="pop" style="animation-delay:0.3s"><rect x="29" y="43"… |
| `LAUNCH_ASDAN/PEQ/PEQ_W6_Review_Progress_and_Sign_Off_the_Unit.html` | 51553 | heading/title | …ot a weakness.</p></div><div class="v5-step"><h3>Name future use, and sign off.</h3><p>Say where you will use communication next. With plan, deliver… |
| `LAUNCH_ASDAN/PEQ/PEQ_W6_Review_Progress_and_Sign_Off_the_Unit.html` | 55791 | staff wording | …">EVIDENCE</div><div class="match-pill" onclick="selectKW(this,'m5')">SIGN-OFF</div></div><div style="display:grid;grid-template-columns:repeat(3,1f… |
| `LAUNCH_ASDAN/PEQ/PEQ_W6_Review_Progress_and_Sign_Off_the_Unit.html` | 63359 | heading/title | …an>🏅</span><span>📸</span><span>✍️</span></div><h2>Review Progress and Sign Off the Unit — banked!</h2><p>Communication (ComSk1) complete ✅</p><div c… |
| `LAUNCH_ASDAN/PEQ/PEQ_W6_Review_Progress_and_Sign_Off_the_Unit.html` | 64646 | heading/title | …e:1.55rem">Knowledge Organiser (LAUNCH ASDAN W6): Review Progress and Sign Off the Unit</h1><p style="text-align:center;margin:2px 0 8px"><strong>LA… |
| `LAUNCH_ASDAN/PEQ/PEQ_W6_Review_Progress_and_Sign_Off_the_Unit.html` | 65749 | heading/title | …v><div id="print-intro" class="print-section"><h2>Review Progress and Sign Off the Unit</h2><p><strong>Name:</strong> ____________________ &nbsp; <s… |
| `LAUNCH_ASDAN/PEQ/PEQ_W6_Review_Progress_and_Sign_Off_the_Unit.html` | 67874 | staff wording | …UTCOME · USE OF LISTENING · AREA TO DEVELOP · FUTURE USE · EVIDENCE · SIGN-OFF</p><p>A specific success you can point to · Where paying attention he… |
| `LAUNCH_ASDAN/PEQ/PEQ_W6_Review_Progress_and_Sign_Off_the_Unit.html` | 69839 | heading/title | …Name your listening and one area to develop. 3) Name future use, then sign off.</p></div></div><div id="print-scaffold-stretch" class="print-section… |
| `LAUNCH_ASDAN/PEQ/PEQ_W6_Review_Progress_and_Sign_Off_the_Unit.html` | 72891 | staff wording | … 10px;font-size:.88rem"><strong>LAUNCH ASDAN W6 · Review Progress and Sign Off the Unit</strong><br>LAUNCH · ASDAN Studio · Personal Effectiveness ·… |
| `LAUNCH_ASDAN/PEQ/PEQ_W6_Review_Progress_and_Sign_Off_the_Unit.html` | 73609 | staff wording | …<td style="padding:7px 8px;border:1px solid #999">Review Progress and Sign Off the Unit</td></tr></table><p style="margin:12px 0 4px;font-weight:800… |
| `LAUNCH_ASDAN/PEQ/PEQ_W6_Review_Progress_and_Sign_Off_the_Unit.html` | 78389 | heading/title | …ass="print-section"><h2 style="text-align:center">Review Progress and Sign Off the Unit — Feedback Sheet</h2><p style="font-size:.95rem;color:#444">… |
| `LAUNCH_ASDAN/PEQ/PEQ_W6_Review_Progress_and_Sign_Off_the_Unit.html` | 93407 | staff wording | … real area to develop.", "I Do 1": "Narrate the four review parts and sign-off slowly.", "We Do 1": "Everyone plays; pace it so nobody is tapping al… |
| `LAUNCH_ASDAN/PEQ/PEQ_W6_Review_Progress_and_Sign_Off_the_Unit.html` | — | filename | LAUNCH_ASDAN/PEQ/PEQ_W6_Review_Progress_and_Sign_Off_the_Unit.html |
| `LAUNCH_ASDAN/PEQ/START_HERE.html` | 2991 | staff wording | …gress_and_Sign_Off_the_Unit.html"><b>Week 6</b> · Review Progress and Sign Off the Unit<br><span style="font-size:.88rem;color:#64748b">review my ow… |
| `LAUNCH_ASDAN/Scheme_of_Work.html` | 4170 | staff wording | …ng evidence</td></tr><tr><td><b>W6</b></td><td><b>Review Progress and Sign Off the Unit</b></td><td>I can review my own success in communicating</td… |
| `Build/Slideshows/BUILD_DT_W6_Handover.html` | 54557 | heading/title | …>staff prepare the completed portfolio + predicted grade for assessor sign-off.</p></div></div> </div><div class="slide" data-title="We Do 2" data-t… |
| `Build/Slideshows/BUILD_DT_W6_Handover.html` | 96626 | staff wording | …", "Independent Work": "Supported/Standard/Stretch per pupil. Witness sign-off and predicted grade both happen here. Give the next step out loud whi… |
| `Build/Slideshows/BUILD_DT_W6_Handover.html` | 125090 | staff wording | …ion."},{"id":"s3","label":"Complete the authorised quality and safety sign-off route.","reason":"Pupil self-check does not replace responsible-adult… |
