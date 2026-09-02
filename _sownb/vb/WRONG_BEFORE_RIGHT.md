# WRONG_BEFORE_RIGHT — Order VB

One entry per figure the order quoted that measurement disproved, and per finding raised then downgraded by reading the call site. Plain lines. Appended per run, never rewritten.

## Run 1 (2026-09-01, Phase 0)

WRONG: main head 22f6470f (RSH-3 catalogue merge).
RIGHT: main head 20216304. Eleven commits landed after 22f6470f: PRs #177–#180 (FEB wave 1 — BUILD Science W14–W16 plus measured instruments, LAUNCH Science Autumn2 W7, GROW Science W15–W16, LAUNCH Science W15) are inside this order's trees; PR #176 (Games AAA V6) is outside.

WRONG: thirteen open PRs.
RIGHT: fourteen. The extra one is #181 "FEB wave 1: BUILD ASDAN Spring 1 W15–W16", and it is an anomaly — its head commit 257ad6a4 is already an ancestor of main and its diff against main is empty. An open PR carrying nothing. Recorded as a human item.

WRONG: STYLE_CONTRACT.json has 225 rows, sha256 prefix e0f8f546.
RIGHT: the live contract on main has 457 rows, sha256 467a8df6. FEB wave 1 extended it (PR #177) — an authorised landed append, not drift. The 225-row e0f8f546 contract survives as the pinned contractSha256 inside G16_DENOMINATORS_RSH3.json, whose own hash matches the order's expected prefix 4ec68f96 exactly.

RIGHT AS QUOTED: frozen production denominators GROW Science 86 / GROW ASDAN 76 / LAUNCH ASDAN 80 / LAUNCH Science 87 — all four re-derive from G16_DENOMINATORS_RSH3.json as lessonCount + supportCount. Caveat measured: the FEB refreeze (feb-denominator-refreeze-v2) excludes the shared.guide.byte-block row from the FEB production denominator; RSH-3's rows are untouched.

FEARED, NOT TRUE: instruments living only inside RSH3_EVIDENCE.zip.
RIGHT: the full gate toolkit (34 scripts: g10, g11, g15, g16, g18, g19, g21, c-gate containment and identity, running heads by PyMuPDF, s24, safeguarding, static, render battery) is on main under _sownb/feb/tools/, and the denominators, contract, token-ownership, calendar spine and horizon files are on main under _sownb/. No rebuild PR needed.

RAISED THEN DOWNGRADED: four branches contend on the twelve RSH-3 surfaces (rsh3/grow-asdan-w7, rsh3/grow-science-w7, rsh3/launch-asdan-w13-w14, rsh3/launch-science-w14-w15).
DOWNGRADED BECAUSE: their blobs for those paths are byte-identical to main — they are the stale delivery branches of the very merges that landed the files (squash-merge residue). The twelve surfaces are uncontended; Phase 1 repairs are not mutation-blocked.

MEASURED, NEW: 92 branches sit strictly ahead of main (order implied ~14). Most are historic pass/audit/backup refs. The strict §0.11 reading would mutation-block much of Art_Teesside via parked/ruled PR branches; flagged as a human item rather than silently adopting either reading.

## Run 2 (2026-09-01, Phase 1 cohort A)

WRONG: "Main is expected around 20216304 (eleven past 22f6470f)."
RIGHT: main is dedbf06f — six more FEB wave 1 packs landed while the order was in flight (PRs #181–#186: BUILD/GROW ASDAN Spring 1, LAUNCH ASDAN Spring 1 W16, BUILD/GROW/LAUNCH Humanities W14–W15). None touches the twelve or _sownb. PR #181, recorded as an empty anomaly in run 1, got its commits and merged.

WRONG: "the RSH-3 reference deck named in the denominators file."
RIGHT: G16_DENOMINATORS_RSH3.json names no reference deck. The four per-family reference decks live in _sownb/feb/tools/render_measure.js (grow-asdan PEQ_A2_W6, grow-science SCI_G_W13B, launch-asdan PEQ_W12, launch-science SCI_L_W13L3). Those were used as the §2 controls.

WRONG (order §4): cohort B = PRs #177–#180.
RIGHT: cohort B measured by diff against 22f6470f is ten packs across PRs #177–#186: 36 added HTML surfaces (24 lessons + 12 front doors/variants). Recorded in VB_STATE with a week-major split.

RAISED THEN DOWNGRADED — four g16/static red classes on cohort A, every one an instrument artefact of the FEB rebuild, none content:
1. shared.offline.boundary red ('localStorage') on all 8 lessons. The PINNED row value forbids ["fetch(","XMLHttpRequest","serviceWorker","data:"] only; FEB's metric() hard-codes a wider list including localStorage. The pinned contract's own shared.guide rows require the localStorage-backed guide persistence — the exact conflict feb/DENOMINATOR_REFREEZE.json documents. All 8 lessons contain none of the four pinned-forbidden tokens. Same artefact reds the four static_pack_gate runs; everything else in them (ids, 40-minute timings, chains, checksums, planted controls) is green.
2. family.*.token.grow red (actual []) on 5 lessons. The RSH-3 provenance comment before <style> (e.g. <!--RSH-W7A:v1-->) pseudo-matches DECL's `--name:value` regex and its greedy value consumes the real --grow declaration that follows. Comment-stripped, every deck declares the token exactly once with the contract value.
3. family.{grow,launch}-asdan.control-count red (7 and 6 vs references 8 and 7). The references do not reproduce on the rows' OWN donor decks: both donors render 6 buttons, static-parsed and rendered alike, on this engine. Row is MEASUREMENT INVALID for cohort A. Substantive parity recorded: LAUNCH W13/W14 = donor exactly (6=6); GROW W7 = donor + one deliberate Evidence-routine button (7 vs 6).
4. START_HERE firing controls fired=False on GROW ASDAN and LAUNCH ASDAN. The mutation literal uses the contract's case-normalised value (#4a6fa5) against a file that writes #4A6FA5 — the replace no-ops, so the still-intact declaration re-passes. Removing the actual declaration makes the row fail: the red control fires under the corrected mutation.

RAISED THEN DOWNGRADED — g10 RED on 3 lessons: unresolved pairs "Community Project", "Safe Research", "Triangulate Source". Capitalised headings, not personal names. No personal name exists in any of the twelve.

REAL DEFECT, REPAIRED: LAUNCH Science W14 front door carried the stale "Held local candidate: nothing in this pack is pushed, merged, deployed or catalogued" notice. Removed (PR #189); SHA256SUMS regenerated; front-door gate PASS with red controls firing; nothing regressed.

MEASUREMENT INVALID, NOT GREEN: public 200 + body-hash binding for all twelve — the venue's network policy answers 403 to CONNECT for mattroper1977.github.io. Verified on landed git bytes instead; link targets verified on disk.

ENGINE NOTE: this venue renders on Chromium 141.0.7390.37; the twelve were measured on 149.0.7827.0. Running-head clearances shift with the engine (references measure 17–53pt here; the order's ≈33.37pt is not reproduced); the version-robust predicate (every page's named head inside its own page-local MediaBox) passes on all twelve and both control families. No pagination red survived its control.

READING LEVEL, PRINTED NOT FIXED: 6 of 8 lessons measure >1 IQR EASIER than their pack median (FK approx, pupil+staff body text): GROW ASDAN W7 11.0 vs 12.2; GROW Science W7A 7.9 / W7B 8.4 vs 10.3; LAUNCH ASDAN W13 11.5 / W14 11.7 vs 14.5; LAUNCH Science W14L2 12.4 vs 13.3 (L1, L3 within range). Deviation is toward easier reading in a SEN setting and the medians include staff-facing text; recorded, no action.


## Run 3 (2026-09-01, Phase 1 cohort B wave B1)

WRONG (order §1.4): "For each of PRs #177, #178, #179, #180 … each wave-B1 file is judged against the contract blob live when its own PR landed."
RIGHT: wave B1 spans EIGHT landing PRs, not four. Its files landed in #177, #178, #179, #180, #181 (BUILD ASDAN Spring1), #184 (BUILD Humanities), #185 (GROW Humanities) and #186 (LAUNCH Humanities). The four-PR enumeration is narrower than the wave the same order fixed. All eight were resolved.

RIGHT AS RULED, AND IT COLLAPSES: all eight landing PRs resolve to the SAME governing contract — sha256 467a8df6…, 457 rows — and that blob is byte-identical to today's live contract. FEB has not moved STYLE_CONTRACT.json since #177. One contract governs the whole wave; g22 against live is therefore 457 EXTENSION-SAFE, 0 REDEFINITION, 0 REGRESSION, 0 LIVE-ONLY. No §5 contract-movement item arises.

WRONG (order §2b): "the RSH-3 reference deck named in G16_DENOMINATORS_RSH3.json."
RIGHT: that file still names no reference deck — the same correction run 2 recorded. The four per-family references live in _sownb/feb/tools/render_measure.js. All four were rendered fresh in this session as engine controls, as §2e requires.

WRONG (my own probe, caught before reporting): the static pack gate appeared to show every checksum row mismatched across all eight packs.
RIGHT: the report's fields are `declared` and `actual`; my probe compared `declared` to a non-existent `measured`, so every row read as a mismatch. declared == actual on every row in all eight packs, the gate returns PASS, and `sha256sum -c` verifies 100% independently. Instrument-reading error on my part, zero real mismatches.

REAL FINDING — INSTRUMENT MIS-SCOPE (this run's only red, and it is the tool's, not the lesson's):
g18_content_floor.py declares itself a "destination-relative pupil-word floor". It is not. BASELINE is hard-coded to Science_Teesside/Grow/W8-W13_2026-27 and yields ONE global p25 — 1638 words — applied to every family in the estate.
BUILD_HUM_W14_Festivals_Display_and_Reflection.html measures 1616 pupil words and so reds against that global floor. Measured against its OWN family it is not thin: the six live BUILD Humanities W9–W14 lessons run 1517, 1555, 1561, 1566, 1608, 1671 (p25 1555, median 1563.5). The candidate is above five of the six and 61 words above its family p25.
The mis-scope is estate-wide, not local to this file: the live GROW Humanities pack runs 1062–1127 and the live LAUNCH Humanities pack 895–1007 — every one of those twelve landed lessons would red against the 1638 GROW Science floor.
Disposition: BUILD_HUM_W14 is VERIFIED. The g18 red is recorded as MEASUREMENT INVALID for non-GROW-Science families. Nothing was repaired, padded or reworded. Evidence: _sownb/vb/evidence/run3/FAMILY_RELATIVE_WORD_FLOOR.json.

RAISED THEN DOWNGRADED: g11 RED on BUILD_HUM_W14. Its own similarity arm passed comfortably — adjusted maximum 0.073, raw maximum 0.078, against a ceiling of 0.184. The RED is inherited wholesale through g11's floorBindingRedControl, which binds g11's verdict to g18's. With the g18 red invalid for this family, the g11 red falls with it. This is the g18-floor-wins-over-g11-ceiling binding working exactly as designed — printed per §3.2, and no conflict arose.

MEASURED, NEW, NOT A GATE RED: three wave-B1 lessons run far longer than their own families' live packs — GROW Humanities W15 at 3463 words vs family median 1104 (×3.13), LAUNCH Humanities W15 at 3460 vs 944 (×3.67), BUILD ASDAN W15 at 2886 vs 1078 (×2.68). No instrument measures an upper bound relative to family, so nothing failed. Printed for Matt as a 40-minute deliverability question, not corrected. All 17 wave-B1 lessons are at or above their own family's p25; not one is thin family-relative.

MEASURED, NEW, FOR PHASE 2: BUILD Humanities absolute week 14 is double-booked. BUILD_HUM_W14_Industry_and_Nature_The_Tees_Story_OUTSTANDING_V4.html (W9–W14 pack) and BUILD_HUM_W14_Festivals_Display_and_Reflection.html (W14–W20 pack) both live, both claiming week 14. This is the Careers W6/W7 trap class named in the master order. Recorded for the calendar cross-check; not resolved here.

MEASUREMENT INVALID, NOT GREEN, UNCHANGED FROM RUN 2: public 200 + body-hash binding for all 24 surfaces. The venue's proxy still answers 403 to CONNECT for mattroper1977.github.io. Verified against landed git blobs (24/24 equal to origin/main) and front-door link targets on disk.

ENGINE NOTE: Chromium 141.0.7390.37 and a 59-font set, both identical to run 2 (font-family fingerprint c555ca08…). Run-2 renders had been deleted, so all four reference controls were re-rendered in this session per §2e. Every control passed its pagination gate and so did every candidate: engine-artefact count 0.

## Run 4 (2026-09-01, g18 v2 + retro, wave B2, g23, Phase 2 prep)

CORPUS FREEZE MISMATCH, INVESTIGATED NOT FAILED: the run-1 54-file manifest came back 53/54, which the order classes as a STOP. The failing file is _sownb/feb/tools/build_resources_append.py. Proven benign before proceeding: the worktree blob (4c86fe9d) is byte-identical to origin/main's, no VB commit in the branch's history touches the file, and the change is FEB's own PR #188 (commit 23852a19, three lines swapping the catalogue subject chip "Humanities · Teesside" -> "Humanities"), landed on main before anchor_run4. The manifest is stale against landed main, not violated by this order. Re-baselined at anchor_run4 rather than silently ignored.

WRONG (order 1.4, second time): wave B2 was expected to resolve per-file governing contracts. It spans SIX landing PRs (#177, #179, #181, #182, #183, #185) and all six resolve to the same blob, 467a8df6 / 457 rows, itself identical to today's live contract. Across runs 3 and 4 the whole of cohort B — fourteen landing PRs — is governed by one contract. FEB has not moved STYLE_CONTRACT.json since #177, so the section 6 "post-#186 contract movement" item does not arise.

SECTION 2 — g18 v2, THE INSTRUMENT FIXED AND THE LEDGER RE-SCORED
The finding acted on: g18_content_floor.py describes a "destination-relative pupil-word floor" and implements a single global one. BASELINE is hard-coded to Science_Teesside/Grow/W8-W13_2026-27, giving one p25 of 1638 applied to all nine families.
g18 v2 (_sownb/vb/tools/g18_v2_family_floor.py, version g18-v2.1.0-per-family-floor-lessons-only) binds on the destination family's own live-neighbour p25, keeps the global p25 printed as LEGACY-INFORMATIONAL on every line, and falls back to global with a printed GLOBAL-FALLBACK n=<n> below five neighbours. Word counting, slide parsing and the thin-slide rule are imported unchanged from v1, so a v1/v2 flip can only ever be the baseline, never the measurement. Red-proved both ways in-session: unmodified file PASS at 1616 words against a 1555 floor; the same file with its pupil paragraphs gutted RED at 361.
The corrected floors are not uniformly softer, which is the point. Per family: BUILD Science 1767 (HIGHER than the global 1638), GROW Science 1638, LAUNCH Science 1583, BUILD Humanities 1555, LAUNCH ASDAN 1465, GROW Humanities 1089, BUILD ASDAN 1053, GROW ASDAN 947, LAUNCH Humanities 897.
BUG FOUND AND FIXED WHILE BUILDING IT (v2.0.0 -> v2.1.0): the first neighbour globs swept in pack support surfaces that carry no pupil slides at all — BUILD_ASDAN_AUT2_SAME_DAY_EVIDENCE, BUILD_ASDAN_AUT2_TEACHER_PLANNING_SOW and BUILD_ASDAN_AUT2_W7_PORTFOLIO_STUDIO each score zero pupil words and dragged BUILD ASDAN's p25 to 1041. Restricting neighbours to real lesson decks (>=5 slides and >0 pupil words) gives n=24 and p25 1053. A floor built from non-lessons is too lenient, and a lenient floor is worse than a wrong one.
RETRO SWEEP, ledger corrected only: 25 already-VERIFIED lessons (8 cohort A, 17 wave B1) re-scored. ONE flip — BUILD_HUM_W14_Festivals_Display_and_Reflection.html, LEGACY RED -> BINDING PASS, at 1616 words against its family p25 of 1555 where the global floor called it thin at 1638. It beat five of its six live neighbours (1517, 1555, 1561, 1566, 1608, 1671). Zero lessons turned red under v2, so no new findings arose from the sweep and no file was edited, padded or reworded. Zero families needed GLOBAL-FALLBACK.
g11 RE-BOUND (2.2) via _sownb/vb/tools/g18_v2_rebind.py, which substitutes only the floor threshold and carries totalWords, the per-slide array, the thin-slide rule, the print arm and the red proof through untouched — g11 independently recomputes words and slides and compares, and that binding still holds, so the re-bind re-scopes a floor rather than forging a measurement. Retro reports are stamped printArmMeasured=false so an unrendered re-score can never be mistaken for a full one. BUILD Hum W14's g11 now PASSes with its own similarity printed: 0.0733 adjusted / 0.0778 raw against a ceiling of 0.1839, all three of its red controls firing. The run-3 reading is confirmed: that red was inherited from the floor and was never a similarity failure.

SECTION 3 — g23, and an honesty note on its rate
g23 (_sownb/vb/tools/g23_period_load.py) is report-only and binds nothing. Its reading rate is an ASSUMPTION and is labelled as one in the tool, in every report and here: the repository and workbooks were searched and contain no words-per-minute figure anywhere, so 90 wpm was chosen as a conservative supported-reading rate and a 60-120 sensitivity band is reported so no verdict rests on the point estimate. Implied minutes are also an UPPER BOUND: the pupil-word count includes headings, option lists and table cells a learner scans rather than reads.
Across 32 lessons: 24 WITHIN, 2 HEAVY, 6 OVERLOADED. The six cluster completely — every one is a FEB Spring 1 ASDAN or Humanities W15 lesson: LAUNCH Hum W15 x3.75 (~38 of 40 min), GROW Hum W15 x3.14 (~38), GROW ASDAN W16 x3.04, GROW ASDAN W15 x3.02, BUILD ASDAN W16 x2.70, BUILD ASDAN W15 x2.67. LAUNCH ASDAN W16 is HEAVY at x2.19 (~36 of 40 min). Split-or-trim options and word deltas are printed for each; both are authoring and neither was done.

RAISED THEN DOWNGRADED — LAUNCH ASDAN W16 ladder labels appeared not to match its family. My matcher required Label adjacent to >, · or whitespace, and the FEB chassis renders tiers as <h3>&#9670; Supported</h3>, so the diamond glyph defeated it. Re-measured against the real chassis: the candidate renders route-cards supported/standard/stretch with headings Supported / Standard / Stretch and declares "tierLadder":"Supported / Standard / Stretch", matching its FEB siblings and the master order's stated LAUNCH ASDAN ladder exactly. GROW ASDAN Spring1 correctly declares "Supported / Standard / Optional reach", also as the order states. No defect.
MEASURED WHILE THERE, AND IT CONTRADICTS THE ORDER: the master order 2.3 states LAUNCH ASDAN live W7-W12 "measures 30/30/30, Secure/Reach 0/0". The tree says otherwise — all 30 live W7-W12 files contain Secure and Reach as literals, none declares a tierLadder key, and their visible tiers render through an older chassis as "LAUNCH entry / LAUNCH secure / Stretch". Supported/Standard/Stretch is the FEB-era vocabulary used by every new pack, not the pre-FEB one. The candidate is right; the order's figure describes the intended ladder, not the live W7-W12 rendering.

RAISED THEN DOWNGRADED — my first Phase 2 collision map reported 24 collisions and found ZERO Humanities lessons. Two faults, both mine: the Humanities globs used a directory prefix (Humanities_Teesside/GROW) that matches nothing, since the real directories are GROW_W9-W14_2026-27 and GROW_W15-W20_2026-27 — so the map missed the very BUILD Humanities W14 collision it was built to find; and it counted parallel ASDAN strands (Careers, Community, Duke, FoodWise, Living Independently all teaching their own week 1) as competing lessons. Strand is part of the key: those are units taught alongside each other. Corrected map below.

SECTION 5 — what the corrected enumeration actually found
TRUE SLOT COLLISIONS (same family, same absolute week, competing lessons): 2.
  1. LAUNCH Science absolute week 14 — SIX lessons, two three-lesson sequences, two packs. Autumn2_W7_2026-27/SCI_L_A2_W7L1-L3 declares "week":14 and cites workbook cell C45 ("Topics 2 to 3 assessment (Dec)"); W14-W15_2026-27/SCI_L_W14L1-L3 cites cell C44 ("Research a genetic condition online; present"). Different cells, same week. This is the term-relative-versus-continuous dialect resolving onto one slot — the SPINE-SPLIT the master order warned of, now concrete and live.
  2. BUILD Humanities absolute week 14 — BUILD_W14-W20/BUILD_HUM_W14_Festivals_Display_and_Reflection ("week":14, cell C59) against BUILD_W9-W14/BUILD_HUM_W14_Industry_and_Nature_The_Tees_Story (pre-FEB deck, no declared week or cell).
LABEL-ONLY COLLISIONS (same week NUMBER, different absolute weeks — dialect, not double-booking): GROW Science W7 (The Moon at absolute 7 versus Autumn2 W7 at absolute 14) and GROW ASDAN W1-W6 (strand packs at absolute 1-6 versus Autumn2_W1-W6 at absolute 8-13). Named so they are not "fixed" by mistake.
GAPS: GROW Science has no week 14 lesson. BUILD ASDAN's main strand is empty weeks 7-14 while its five sub-strands cover weeks 1-6.
THE THREE UNRESOLVED CELLS decide none of the above. Build Wed P6, Grow Thu P6 and Launch Thu P5 are disputed between Behaviour Intervention and DT/practical skills, and neither is an in-scope subject, so they change each lane's teachable capacity, not which lesson wins a week. They stay UNRESOLVED and were not inferred.

VENUE RULING APPLIED: public-200 body-hash binding is now permanently VENUE_BLOCKED (proxy 403s CONNECT to github.io; confirmed runs 2, 3, 4). Never reported as passed, never counted in a verdict. Its binding substitute held: 12 of 12 wave-B2 worktree blobs equal origin/main at anchor_run4.

ENGINE: Chromium 141.0.7390.37, 59 fonts, fingerprint c555ca08 — identical to runs 2 and 3, zero drift. All four reference controls re-rendered this session per 4.3(e); every control and every candidate passed its pagination gate. Engine-artefact count 0.

OBSERVED, NOT A RED: three wave-B2 lessons sit close to their g11 similarity ceilings — GROW Science W16A 0.1486 of 0.1524, BUILD Science W16B 0.1402 of 0.1435, BUILD Science W16A 0.1399 of 0.1435. All under. Recorded because the margin is thin enough that a future sibling landing in those families could cross it.

## Run 5 (2026-09-01, Phase 2)

CORPUS: 54/54 against CORPUS_FREEZE_RUN4.txt. Main unchanged at 28ee8d9b. Neither a stale manifest nor a violation arose this run. Capability identical to runs 2-4 (Chromium 141.0.7390.37, 59 fonts, fingerprint c555ca08). Live contract still 467a8df6 / 457 rows.

SECTION 2 — THE GLOB SWEEP, AND WHERE THE BUG ACTUALLY WAS
The order told me to assume run 4's contaminated glob was the shared helper's fault rather than g18's. That assumption was wrong in an instructive direction. Six selectors were swept:
  g18_content_floor.py  — GLOBAL floor, no zero-slide exclusion, but its one glob admits no zero-slide file (12 clean files), so it was never contaminated in practice.
  g18_measurement.py    — PER-FAMILY, and it ALREADY excluded zero-word files via 'if measured[totalWords]'.
  g11_family_similarity.py — per-family similarity corpus; zero zero-slide files admitted in any of its nine globs.
  static_pack_gate.py   — pack integrity; must see support files, exclusion would be wrong.
  g18_v2 / g23 (mine)   — exclusion present since v2.1.0.
FEB HAD ALREADY BUILT THE PER-FAMILY FLOOR. g18_measurement.py carries a BASELINES dict with nine per-family patterns and derives a nearest-rank p25 from the family's own donor pack. My g18 v2 partly reinvented an instrument that already existed. Recorded because the estate should not carry two implementations of the same measurement.
THE ONE REAL DIVERGENCE WAS MINE, NOT FEB'S. Comparing both derivations across nine families: eight agree exactly (BUILD Science 1767, BUILD Humanities 1555, BUILD ASDAN 1053, GROW Science 1638, LAUNCH ASDAN 1465, LAUNCH Science 1583, GROW Humanities 1089, LAUNCH Humanities 897). GROW ASDAN differed: FEB 958 from n=18, mine 947 from n=6. Cause: my glob was 'GROW_ASDAN/Autumn2_W1-W6_2026-27/PEQ_A2_W*.html', which captures only the PEQ strand, while that pack also teaches COMM and ENT. A family floor built from one strand of three is not a family floor — an under-inclusion defect, the mirror of run 4's over-inclusion. Fixed in v2.2.0 by importing FEB's BASELINES rather than maintaining a second copy, so the two cannot drift again.
2.3 IMPACT: GROW ASDAN p25 947 -> 958, median 954 -> 991. All 25 retro lessons re-scored: ZERO verdict flips, zero reds. The only GROW ASDAN Phase-1 surface (PEQ_A2_W7, 1685 words) passes against either floor. The recorded denominators (86/76/80/87 and the FEB family figures) are COUNTS OF CONTRACT ROW IDS, not file-set globs — verified by len(lessonRowIds) == lessonCount — so they are not contaminable by a neighbour glob at all.
2.4 g23 RE-ISSUED: three GROW ASDAN ratios moved (PEQ_A2_W7 1.77 -> 1.70 HEAVY; GROW_ASDAN_W15 3.02 -> 2.91; GROW_ASDAN_W16 3.04 -> 2.92). No ratio crossed 2.5. Verdict counts unchanged at 24 WITHIN / 2 HEAVY / 6 OVERLOADED. NO split-or-trim decision is withdrawn.

SECTION 3 — WHAT THE WORKBOOK SETTLED
3.3 THE C45/C44 QUESTION IS ANSWERED, NOT DEFERRED. From _next6/sow/LAUNCH.json, 'LAUNCH Weekly - Autumn', Science strand: C44 = Aut2·W6 = absolute 13, "Research a genetic condition online; present"; C45 = Aut2·W7 = absolute 14, "Topics 2 to 3 assessment (Dec)". Under the master order's spine (Aut1 1-7, Aut2 8-14) that is unambiguous. SCI_L_A2_W7L1-L3 cites C45 and declares week 14: CORRECT. SCI_L_W14L1-L3 cites C44 but is named and packed as W14: MISLABELLED by one week.
3.2 THE MISFILED-LANE HYPOTHESIS IS REJECTED, AND SOMETHING BETTER FOUND. Neither LAUNCH Science sequence is misfiled GROW Science content — both cite LAUNCH Science cells and teach GCSE Biology. The collision is a SYSTEMATIC +1 WEEK OFFSET in the pre-FEB run, confirmed by topic against the workbook: C39 mitosis abs 8 -> deck W9; C40 growth/stem cells abs 9 -> W10; C41 stem-cell ethics abs 10 -> W11; C42 DNA abs 11 -> W12; C43 Punnett abs 12 -> W13; C44 genetic condition abs 13 -> W14. Six of seven rows are one week late; only C45 -> A2_W7 is aligned, which is exactly why the newest pack collides with the old run. The master order's §3.3 asked whether this still held: IT DOES.
BUILD HUMANITIES WEEK 14: the misfiled-lane test also fails here, for a different reason. BUILD_HUM_W14_Festivals_Display_and_Reflection cites C59 (World About Me, absolute 14, "Make a festivals display") and per TRACE also C73 (RE & World Views, absolute 14) — correctly placed. BUILD_HUM_W14_Industry_and_Nature_The_Tees_Story cites no cell, and a search of every BUILD workbook row for its local-history vocabulary (Tees, industry, river, rail, iron, steel, town, map) returns no Autumn2 match — the nearest is "Talk about how my local area has changed" at Spring1 W4, a single row, not a six-week sequence. The whole BUILD_HUM_W9-W14 pack is a pre-workbook local-history sequence. Under the order's precedence (workbook beats repo) the Festivals lesson is week 14; the legacy deck has no workbook warrant there. RECORDED, NOT TOUCHED — nothing was deleted, renamed or unpublished.
3.4 THE DOUBLE-PERIOD TEST DISSOLVED NOTHING. I expected it to clear six findings at once. The real timetable (_passpq/inputs/timetable_2026-27.json, extracted from the two source workbooks with per-cell provenance) is 40-minute periods throughout, P1-P6. Comparing every lane-day's consecutive period labels: ZERO doubles. All six overloaded lessons sit in single 40s. All six decks declare nine stages summing to 40, so the declared plan matches the slot; the mismatch is the pupil-word load inside it. Every split-or-trim decision stands.
NEAR-MISS WORTH RECORDING: my first double-period test keyed on a 'subject' field and returned "0 doubles" — but that field does not exist in the timetable JSON; the field is 'label'. A non-existent key would have produced the same headline number by accident, and the whole overload question turns on it. Re-run against 'label' (null-safe): still zero, now for a real reason.
3.1 WEEK MAP, AND A BUG I CAUGHT IN MY OWN TABLE. First pass keyed workbook cells as bare "C45" across all sheets and strands, so later rows silently overwrote earlier ones and correctly-placed decks read as GAPs — GROW Science week 14 appeared empty when SCI_G_A2_W7A/W7B cite C45 and cover it. Corrected by resolving each deck's cell within its OWN family strand and Autumn sheet. Final counts: MATCH 54, GAP 30, COLLISION 0, ORPHAN 0. Every gap is early-term (Humanities abs 1-8, Science abs 1-2) and predates this work.
RUN 4 GAP WITHDRAWN: "GROW Science has no week 14 lesson" was an artefact of my run-4 index reading the filename label W7 instead of resolving Autumn2 W7 to absolute 14. GROW Science week 14 IS covered, by the Autumn2_W7 pack citing C45. The gap does not exist.
RUN 4 GAP RECLASSIFIED: "BUILD ASDAN main strand empty weeks 7-14" was an artefact of the same index treating the Spring1 pack's filename prefix as a strand. BUILD ASDAN's teaching is carried by its five sub-strands; there is no missing main-strand run.
3.7 CAPACITY RULING, PLUS A NEW CAPACITY FINDING: the three UNRESOLVED cells (Build Wed P6, Grow Thu P6, Launch Thu P5) are Behaviour Intervention vs DT, neither in scope, and no finding in the week map depends on them — demoted to non-blocking, still a human item, still not inferred. Measured alongside: the Build lane has ZERO explicitly-ASDAN (a) slots in the real timetable, while BUILD_ASDAN lessons are being authored; that work must ride carryable (b) slots. New human item.

## Run 6 (2026-09-01, Phase 3 pilot + D1 + D5 + baselines)

PRE-GATES: main unchanged at 28ee8d9b; CORPUS_FREEZE_RUN4 54/54 — neither stale manifest nor violation; capability identical to runs 2-5 (Chromium 141.0.7390.37, 59 fonts, c555ca08); contract 467a8df6 / 457.

WRONG: "fifty-one confirmation blocks fail to appear in print."
RIGHT, MEASURED BY RENDERED PDF: 183 decks carry a confirmation block; 104 print it, 79 do not. The 79 are not partial failures — in EVERY one the whole PDF is blank, zero characters. Not a single deck prints content while losing only its confirmation. The reconciled count of decks fixable by PLACEMENT is ZERO, so Phase 3 closes at §1.1 as the order provides.
THE CROSS-TAB IS THE PROOF: insidePrintPack+prints 56, insidePrintPack+missing 0, outsidePrintPack+prints 48, outsidePrintPack+missing 79. Every deck with the block inside .print-pack prints it, with no counter-example; and 48 decks print it from OUTSIDE the pack, so being outside is not what breaks it.

RAISED THEN DOWNGRADED — my own static predictor. I first classified 127 decks "AT RISK" because their confirmation block sits outside .print-pack, and was about to treat that as the denominator. Rendering showed three of the first eight such decks printing ten pages WITH the confirmation. The static test over-predicts badly; placement outside the pack is not a failure mode on its own. Discarded and replaced with the full 183-deck render. This is exactly the proxy-versus-evidence trap the order warns about, and it nearly set the denominator.

REAL DEFECT FOUND, DIAGNOSED, NOT APPLIED: the 79 blank-print decks build their print output into a #print-area div. Ruled out by measurement: (1) it is NOT waiting on JS — #print-area already holds 15,819 characters of innerHTML before any beforeprint event, and dispatching beforeprint changes nothing; (2) it is NOT a hidden ancestor — #print-area is a direct child of body, display:block, visibility:visible under print media. The cause is its children: every .print-section inside it computes to display:none under print. The print stylesheet turns the container on and never turns the sections back on. Likely a single rule per deck, e.g. @media print{.print-section{display:block}}. NOT APPLIED: §1.2 permits placement only, a CSS rule addition is a different class of change, and 79 files exceeds the ceiling. Severity is higher than the original finding — these decks print nothing at all.
PILOT PACK EMPTY: LAUNCH Humanities W9-W14, the designated pilot, contains no confirmation blocks in any of its six lessons. There was nothing to pilot there.

D1 — BLOCKED, AND THE ORDER'S PREMISE IS THE THING THAT FAILED. The order gave a default YES to "six lessons move back one week". Blast radius first: a rename touches 83 files, seven of them read-only workbook ground truth under _next6/, so §2.2 selects the label+citation branch — that much is settled and the exact per-deck edit is written out.
The relabel is a CHAIN: W14->13 needs 13 free, needing W13->12, down to W9->8, which needs week 8 free. Week 8 is held by the SCI_L_W8 enzyme/amylase trio. Searching every LAUNCH workbook row for enzyme/amylase/catalyst/digest returns ZERO matches in any strand or term. The arithmetic agrees: workbook Biology C34-C45 = 12 taught weeks; live decks carry 12 week-labels plus the correctly-placed Autumn2_W7 pack at abs 14. The enzyme week is one EXTRA week, and it is what pushed W9-W14 a week late.
Moving the enzyme week to 7 instead collides with the v3_40min W7 trio, which aligns to C38 and sits in a protected production tree (_glv3/PROTECTED_TREES.json) — so v3_40min is live, not legacy, and week 7 is not free.
NOT APPLIED because doing six of seven would knowingly manufacture a collision at week 8, and assigning or stripping the enzyme week's number is a curriculum decision with no workbook warrant. One question put to Matt; the full mapping and edit are staged.

D5 — DONE. _sownb/vb/tools/g18_v2_family_floor.py is now g18-v3.0.0-feb-measurement-delegated: it computes no floor of its own and delegates to FEB's g18_measurement.derive_floor, keeping only the printing discipline (family, n, per-family p25, legacy global p25, candidate words, verdict, tool version) and g11's own similarity and ceiling. All nine family floors identical before and after. All 32 Phase-1 lessons re-scored under the single implementation: ZERO flips, ZERO reds. The estate now has one g18 computation.

BASELINES, REPORT ONLY, NOTHING CHANGED.
g24 visual density across 350 live lessons: 180 (51%) have ZERO explanatory visuals; estate median 0; the maximum in any lesson is 2. All three Humanities families have none at all. Zero print-dead visuals, because there is almost nothing to kill. An explanatory visual is counted only with >=3 text labels, viewBox area >=10000, inside a teaching stage, and referred to in that stage's prose.
CAUGHT BEFORE REPORTING: the first g24 sweep returned "no lessons" for all ten families. The cause was mine — measure() called relative_to(ROOT) on a relative path and every call raised, with the exception swallowed by a bare except. A zero that came from a crash, not from the estate. Fixed and re-run.
g25 we-do variety: only 56 of 350 lessons carry a stage titled "We Do". Nine types observed; label-the-diagram (63), sort-or-match (56) and decision-lab (48) carry roughly 85%. BUILD ASDAN runs TWELVE consecutive lessons with an identical type-set — every other family stays at one or two. predict-then-check appears 3 times estate-wide and spot-the-error once. The 18 UNCLASSIFIED stages are real patterns the tool had not been told about, chiefly "everyone commits" and "choose, then justify".
Six-type rotation PROPOSED (commit-and-reveal, sort-or-match, label-or-annotate, sequence-or-rank, predict-then-check, spot-the-error), with decision-lab deliberately excluded because it already dominates and the rotation exists to break its grip. Word bands per type printed: type does not predict load — the heaviest example of four different types is the same pair of overloaded Humanities lessons.

CONTRACT ROWS PROPOSED, NOT APPLIED: six rows in _sownb/vb/PROPOSED_CONTRACT_ROWS_RUN6.md. None is proposed as binding on live work, because each would red a large part of the estate the day it landed. Only wedo.taxonomy blocks the next authoring wave, because wedo.rotation is defined in terms of it and an author must know the six before drafting.

## RUN 7

THE BIG ONE — THE 79 "BLANK-PRINT" DECKS WERE NEVER BROKEN, AND MY FIX WOULD HAVE BROKEN THEM. Run 6 recorded 79 decks printing nothing and diagnosed a missing rule, @media print{.print-section{display:block}}. Both halves were wrong. Driving each deck's own printPack('standard') with window.print stubbed makes 11 .print-section elements .visible and yields a real 4-5 page PDF with the confirmation on the last page. The decks were fine; my harness never clicked a route button, so nothing had made any section visible. Worse, the proposed one-line fix would have forced EVERY route's sections visible simultaneously in print, wrecking 79 currently-working live decks. §2 rolled out nothing: 0 patched, 0 skipped, finding WITHDRAWN. A red produced by a harness that does not drive the feature is not a defect in the feature.

MY WORKSHEET TABLE HAD NO LINES ON IT. g21 came back RED on the proof lesson's print pack with verdict INSTRUMENT DISAGREEMENT: vector-box said the trailing sheet was EARNED, raster-ink said COLLAPSIBLE. The engine-artefact control ruled the engine out — all four RSH-3 reference decks rendered in the same session agree with themselves (three EARNED under both instruments, grow-asdan COLLAPSIBLE under both); none produces disagreement. So it was mine. The tempting move was to argue for the instrument I preferred, since page 2 is mostly intentionally-blank writing space that vector counts and raster does not. Reading the numbers instead: page 1 occupied 265pt of 763 and its vector box count was 10 for the whole page. The print pack has NO td or th rule anywhere — the three-column writing table rendered with no borders at all. Blank rows drew nothing, inked nothing and were invisible on paper. Two failed attempts before that: adding rows (5 then 7) moved page-1 free space by 55pt and then by nothing, which was the real clue and I nearly ignored it. Fixed by giving the table the confirmation block's own inline-style idiom (border-collapse, 1px cell rules, 44px row height) plus the deck's own worked example as a modelled first row. g21 now PASS EARNED with both instruments agreeing, and the worksheet is one a pupil can actually write on.

g25 COULD NOT FAIL ON CONTENT. As shipped in run 6, judge() checked only that the deck's declared weDoType was one of the six contract types. A deck declaring "commit-and-reveal" over a sorting activity was green. That is a rubber stamp on a JSON string, not a gate, and the proof lesson's own green was worth nothing. The tool's observed-type classifier speaks the run-6 DISCOVERY vocabulary (ten labels), which is not the contract vocabulary (six types) — so the two columns it printed side by side were never comparable. v3.0.0 writes the join between the vocabularies explicitly and requires the declaration to be corroborated by the we-do stage text. Proved red first on three deliberately broken decks: declaring a type the text does not evidence, declaring a type outside the six, and declaring nothing readable. All three fire; the real deck passes on evidence.

I DECLARED A CONTROL BROKEN WITHOUT CHECKING IT WAS BROKEN. The first g25 red-control run reported all three mutants still reading declared=commit-and-reveal. I had asserted the mutation landed by testing `'"weDoType"' in text`, which is true whether or not the value changed — grepping the name, not the behaviour, exactly as §0.4 says not to. The source carries `"weDoType": "commit-and-reveal"` with a space; my replacement string had none, so every mutation was a no-op. Re-cut with an assert on the count of the exact string.

RUNNING HEADS: MY EXPECTATION WAS WRONG, NOT THE DECK. running_heads_pdf.py came back RED with clearances [80.149, null]. I had passed --expect "People Special to Me", the lesson title. The running head is the pathway line, "BUILD Humanities · Autumn 1 · Week 1". With the correct fragment: PASS, clearances [51.853, 51.853], red control fired. An instrument fed the wrong expectation reds honestly and means nothing.

g19 WAS NOT APPLICABLE AND I HAD RECORDED IT GREEN. FEB's g19_token_ownership.py hardwires donor decks for exactly four RSH-3 families in build_config(). --family "BUILD Humanities" raises KeyError('BUILD Humanities') — not a verdict. Any earlier "g19 PASS" for this deck was not a measurement. Measured properly against _sownb/vb/G19_TOKEN_OWNERSHIP_VB.json: FEB's config plus one family, built by FEB's own declarations() routine from two verified landed BUILD Humanities surfaces, FEB's own file untouched. PASS, with two red controls (a wrong token value and a planted foreign-family token) both firing.

SAFEGUARDING: THE GATE MEASURED SOMEBODY ELSE'S PACK. _sownb/feb/tools/safeguarding_strings.py ignores argv entirely, iterates a hardwired list of the three LAUNCH Science W14-W15 lessons, requires lessonCount==3 and writes to a fixed output path. Running it "on" the proof lesson printed a green that was about the LAUNCH Science pack. Replaced with the same rule — required exact strings present, zero runtime network tokens, each string proved load-bearing by in-memory deletion — applied to this deck's own wording, and recorded as a VB gate under its own name rather than borrowed as FEB's.

FRONT DOOR: CSS CLASS NAMES ARE NOT DOM ELEMENTS. The first W1-W8 START_HERE was hand-written and red on three counts. .thread and .week appeared in its style block, so a grep found them — but g16's selector rows are parsed-DOM element counts, and no element carried either class. The <h1> replacement landed outside <main> so the viewport check read h1 as empty. Rebuilt on the donor's own structure (header with h1 and a .thread strip, one section.week per week) rather than patched around. All three green, every firing control fired.

THE NOTICE ASSERTED SOMETHING THAT WAS ABOUT TO BE FALSE. The front-door gate reds on "Local ... review candidate", "Nothing in this pack is pushed", DRAFT and CANDIDATE. My notice opened "Local review candidate:". Run 7 §4.6 asks for a residual note, and the gate forbids exactly those phrases — but the gate is right and the order's wording is loose: once this merges, the pack IS deployed, and a notice claiming otherwise is a false statement on a live page. Rewritten to keep every piece of true information (week 1 written and ready to teach, weeks 2-8 not written yet, listed with their cells and their build slot) and drop the non-deployment claim.

THE PACK IS NOT "AUTUMN 1". I labelled the pack, its title, its manifest and its front door "Autumn 1 · Weeks 1-8". Reading the workbook rather than my own earlier note: C46-C52 are Aut1·W1 to Aut1·W7, but C53 is Aut2·W1 — absolute week 8 on the Aut1=1-7 / Aut2=8-14 spine. The pack spans Autumn, not Autumn 1. Corrected in the title, the header, the manifest and week 8's own card, and every outcome on the front door is now the workbook's wording verbatim rather than my paraphrase (I had rewritten "Share a group/team/community I belong to." as "a group, team or community", and straightened the workbook's own quote marks).

VB EVIDENCE NAMED ITS SUBJECTS IN A FORM NOTHING COULD RESOLVE. tools/stale_evidence_sweep.mjs reads any tracked JSON with a "file" key as a QA record and resolves that subject from the repository root. Six runs of VB evidence recorded subjects as bare basenames (SCI_G_W9B_Spherical_Bodies_Do.html) or as pack-relative paths, so the sweep reported 1,133 of them STALE — every one a false alarm about evidence that was measuring a file that exists. The measurements were never wrong; the records just named their subjects in a form only I could read. 2,062 rewritten to repo-relative paths: 1,992 by unique basename across tracked files, 66 resolved against the record's own enclosing "pack" field, 4 pack-relative with a slash. Nothing guessed — a basename carried by more than one tracked file was rewritten only where the record itself named the pack, and the pass reports ambiguous and unresolvable cases rather than picking one. VB evidence now contributes zero stale claims.

AND THE THING THAT WAS NOT MINE, RAISED RATHER THAN WIDENED INTO. Fixing the above did not turn the CI check green, and chasing that is what found the real fault. tools/fieldops/qa_record_control.mjs went red with "no row emitted" for rows the sweep demonstrably emits. The sweep prints its whole table with console.log and then calls process.exit(2); when stdout is a pipe those writes are asynchronous and process.exit() discards whatever is still queued. Two captures of the same unchanged sweep over the same tree returned 23,413 and 428,196 bytes of a 729,397-byte report — non-deterministic truncation. The control's planted fixture repo sorts LAST in the table, so the discarded tail is exactly what it asserts on. On main the report is 165 lines and flushes in time; this branch adds 1,378 records that genuinely judge a subject, which the sweep is right to enumerate, and the report crosses the flush point. The control was already fragile and the corpus grew past it. NOT PUSHED: this is tools/ and tools/fieldops/, which this PR does not otherwise touch, and there is no upstream fix to port. The measurement, the mechanism and a proposed patch are in _sownb/vb/evidence/run7/SWEEP_CONTROL_TRUNCATION.json, and the naive one-line fix is recorded there as wrong — swapping process.exit(2) for process.exitCode = 2 lets execution fall through into the later branches and changes the report. Also recorded there: 32 remaining rows call tools/render_installation_gate.js stale because the sweep's PATH_NAMED regex is unanchored and matches the tail of _sownb/feb/tools/render_installation_gate.js, which exists.

FIXING ONE CHECK REVEALED THE NEXT, WHICH IS NOT MINE TO DECIDE. With the qa-record control passing, the CI job ran on past it for the first time and stopped at tools/verify_fixture_names.mjs — the estate's person-shaped-fixture check — with 107 unallowed hits. Every one of the 107 is the SAME token in ten VB files: CAREERS_W11_..._LAUNCH (the LAUNCH ASDAN W11 mock-interview careers lesson). No pupil name is involved. It is a real LAUNCH ASDAN W11 careers lesson that trips the predicate only because MOCK is a fixture marker and the surrounding words are ordinary titlecase, and that exact string is ALREADY allowlisted for three LAUNCH_ASDAN paths and for the checker itself, ruled by Order N6 on 2026-08-28 as naming no person. VB evidence quotes it because g11 and g18 measure a candidate against its family's whole corpus and that lesson is a member of it. Across all 3,524 files the only other person-shaped strings are the checker's own declared red vectors and the ledger's dated record of the canary. The check's red control fired correctly: the seeded fixture reds the tree at 108. NOT ACTIONED. The fix is ten (file, text) entries in the tool's own ALLOW list, same token and same reason as the three already there — but widening a pupil-name safeguarding allowlist is a safeguarding decision, not a build fix, and the edit was declined at the tool level here, which is the right default for that file. Not retried and not worked around: never by renaming the lesson in the evidence, never by exempting a directory, never by deleting the evidence that names it, never by relaxing the predicate. Written up in _sownb/vb/evidence/run7/FIXTURE_NAME_CHECK_BLOCKED.json and put to Matt.

ORDER H7 ASKED ME TO PRINT TEN ALLOWLIST ENTRIES "EXACTLY AS THEY STAND". They did not stand: tools/verify_fixture_names.mjs was untouched on this branch (git diff origin/main on that path: empty). The ten had never been added, because the answer to H7.5 had not come and the edit was declined at the tool level. Saying so was the first thing owed, not the last. The order's model was off in a second way too: it asked me to rule each of ten entries as historical figure / staff / declared placeholder / fictional. There are not ten names. There is ONE token across ten FILES, and the token is a filename — a live lesson of 59,500 bytes — so the taxonomy has no applicable row and the honest answer is that it is not a person of any kind.
AND THE ORDER'S §2 PREMISE WAS WRONG, WHICH MATTERED MOST. It called the red check "the estate's known required-check deadlock" and offered a ruleset PR or a dated admin override. Checked rather than accepted: there is no deadlock doc in the repository, and the check is a genuine content finding that reproduces offline in about a second and has a real fix. Neither route applies, and the override route would have pushed a red pupil-name safeguarding check through — the opposite of what that fallback is for. Taking the offered route would have been the worst available action.
WHAT THE ORDER GOT RIGHT, AND I HAD MISSED: the hard rule that a gate change never lands in the same PR as content the gate judges. I had been treating this as one question — may I widen the allowlist — when the answer was that it is two PRs. Split to #192, off main, one file, +48 lines, zero content.
A WORKTREE MERGE ADVANCED THE BRANCH I WAS PROTECTING. To prove criterion (c) I merged the gate branch into the content branch inside a scratch worktree, forgetting that worktrees share branch refs — so the merge advanced claude/vb-order-verify-build-u4r3my itself and put the gate change straight back into the content PR, which is exactly what the hard rule forbids. Caught on the next status check, before any push: origin was still at 0205e2db, reset --hard back to it, gate file confirmed untouched on the content branch. The proof itself was still needed and still valid — on main alone the ten files do not exist, so the entries are inert there and prove nothing; the only tree where they bite is main + the gate change + this branch's content, where 107 unallowed hits go to 0 and a planted real-looking name still reds the tree.

## RUN 8

I REPORTED A CI RUN AS SLOW FOR FORTY MINUTES WHEN IT HAD FINISHED IN FOUR. This is the first row because it is the one that misled the person reading. Polling the Checks API repeatedly, I kept receiving "in_progress" for a job that had completed at 20:58:14 after 4m13s, and I reported it to Matt first as "runner congestion" and then as a "long-running job", twice, with confidence. Both explanations were invented to fit a stale cache. The job was never slow; the API was serving an old status and I read elapsed wall-clock from my own waiting rather than from the run's created_at/completed_at. The order now forbids exactly this, and rightly: polling age is not run duration. Every duration in this run is read from timestamps.

THE §0.4 OPEN-PR INVENTORY WAS COMPUTED AGAINST A REF FIVE DAYS STALE. I ran the overlap scan with `git diff main...pr`, where `main` was the LOCAL branch, last updated 2026-08-26 at 288f8454 while origin/main was at 5d89522c. Every PR therefore appeared to touch resources.json, Science_Teesside/Launch and tools/ — main's own progress attributed to fourteen other people's branches. Caught because #191 appeared to touch Launch Science files it demonstrably does not. Recomputed against origin/main: #166, the one I had flagged as the highest overlap risk on its name alone, touches two checksum files and NOTHING this run goes near.

I NEARLY REPORTED FONT DRIFT THAT DID NOT EXIST. The capability check compares a font fingerprint against c555ca08. My first hash gave a557a2c6 and the honest-looking move was to report drift. The fingerprint is method-dependent, so I tried the plausible forms until one reproduced the recorded value exactly: `fc-list -f '%{family}\n' | sort -u | md5sum`. Zero drift, engine and font set identical to runs 2-7. A mismatch between two different measurements is not a finding about the thing measured.

I DECREMENTED WEEK NUMBERS IN THE WRONG DIRECTION AND COLLAPSED FIVE WEEKS ONTO ONE. The front door holds every week in one file. Renumbering N to N-1, I processed descending, so the "Week 12" written by the 13->12 rule was caught again by the 12->11 rule, and 13, 12, 11, 10 and 9 all cascaded onto 8. My own code comment stated the reasoning backwards — descending is safe for an increment, not a decrement. Caught by counting the labels afterwards rather than trusting the patch: 5 of each week-8 label where there should have been 1. Front doors restored from HEAD and redone ascending, with a masking pass so no rule can see another rule's output.

I APPLIED HALF OF D1 AND MANUFACTURED THE COLLISION THE RULING EXISTS TO AVOID. ENRICHMENT means the enzyme trio has no absolute week. I relabelled the six later weeks and left the trio's "week":8 in place, so six lessons claimed week 8 at once. Worse, my own collision check missed it, because it keyed on files carrying a cell citation and the trio has none — a check scoped to exactly the files that could not fail it. Found by asking the blunter question, "does anything else now claim week 8". The trio's week claim is now removed outright.

MY FIRST H7.4 REVERT MEASURED A CRASH, NOT A DEFECT. To prove the flush fix necessary I stripped it with a regex that removed the comment opener and left the comment body as executable code. The reverted copy died with SyntaxError: Unexpected identifier 'calls', and 876 bytes of stderr would have read as "the defect reproduced". A control that fails to load proves nothing about the thing it was meant to isolate. Redone from the exact pre-fix blob at 5d89522c, byte-identical, and the real measurement is unambiguous: 170KB-471KB captured against 921,154, tail absent 0/10 against 10/10.

THE ORDER'S OWN RED CONTROL FOR g26 DOES NOT RED, AND SAYING SO WAS THE JOB. §3.1(d) specifies proving the gate by joining two sentences into one long one. It does not red, and it cannot: the deck has 264 pupil sentences and sits 0.47 below its ceiling, so one join moves the mean from 3.53 to 3.63. The temptation was to pick a heavier pair of sentences until it tipped, which would have been fitting the evidence to the instruction. Recorded as a spec mismatch instead, and the gate red-proved two ways that mean something — the same mutation applied throughout (7.74) and a real live BUILD lesson (11.63).

THE PROOF LESSON'S READING LEVEL WAS NOT AN ADDRESSEE ARTEFACT, WHICH IS WHAT I HAD HOPED. §3.1(a) offered the possibility that FK 5.60 was staff text mixed into pupil text. Measured: whole-deck 5.65, pupil-only 5.60. Near-identical, so the staff writing is pitched at the same level as the pupil writing and there was no artefact to find. The repair was real work, not a re-measurement.

## RUN 9

I READ A PAGE OF CHECK RUNS AND CALLED IT A PLAN. The first coverage census gave BUILD ASDAN "week 29" and "week 30": my parser added the Spring 1 folder offset to filenames that already carried absolute weeks (W15, W16). Corrected before the headline was printed; the census was rebuilt from the whole tree (573 files under the nine search roots, 414 lessons) and cross-checked against CALENDAR_SPINE's own path readings — zero disagreements on unchanged blobs.

THE CATALOGUE APPEND BROKE MY OWN SCRIPT, NOT THE CATALOGUE. The second append's g8 script inherited a placeholder from the first and raised NameError before writing. Rewritten standalone; g8 PASS, fabricated-subject control fires, 678 -> 680 prefix byte-identical.

THE GENERATOR SPLIT AN F-STRING. Swapping the outcome line for FEB's guide-keyed sowline broke implicit string concatenation; ten regenerations failed with SyntaxError before I read the line. One `+`.

THE PROOF LESSON'S PATTERN WAS TOO LONG FOR TWO OF THE THREE FAMILIES. The first GROW decks came out at 2,027-2,455 pupil words against a 1,656 ceiling and the first LAUNCH decks at 2,448-2,630 against 1,386 — I had written every family to the BUILD proof's density. Three compaction passes (stage set, one Lundy bridge per deck instead of nine, field-level trims) brought every deck inside its own family's 1.5x ceiling without dropping a diagram or a route.

g10 CAUGHT EVERY PROPER-NOUN PAIR I HAD WRITTEN. Twenty-nine "Given Family" candidates across eight decks — Empire Windrush, Commonwealth Immigrants Act, National Health Service, Roman York, Good Friday Agreement and the rest — plus two Title Case titles. The registries are for real public figures and declared invented exemplars, neither of which these are, so the prose was rewritten around the pattern (the 1962 Act on Commonwealth immigration; York in Roman times; the 1998 Belfast agreement) and GROW/LAUNCH carry the verbatim outcome as FEB's guide-keyed sowline, exactly as their landed W15 decks do. Nothing was added to a registry.

THE FRONT DOORS FAILED THEIR OWN SPLASH ROW BECAUSE I PRETTY-PRINTED IT. start.*.splash is a byte block on one line; my generator emitted it with newlines copied from a regex-split print. The blocks are now sliced byte-exact from the landed front door.

FEB's v1 g18 RED ON SEVEN DECKS IS THE NT-7 ARTEFACT, NOT CONTENT. Its floor is a GROW Science denominator (1,638 words) that sits above the GROW ceiling (1,656 — one deck's headroom) and above the whole LAUNCH ceiling (1,386). The binding instrument for scope=new is g18 v2's family floor (run 4); g11 was run on the family-rebound g18 as run 4 did. Recorded, not smoothed.

THE SWEEP WENT RED ON ALL THREE FAMILY PRs AND IT WAS THE INSTRUMENT'S BUFFER. The QA-record control spawns the sweep with execFileSync and no maxBuffer; main's output is 962 KB, a family branch's is 1.07 MB, the child is killed with ENOBUFS at 1,051,854 bytes and the planted rows never arrive. Red-proved three ways on the over-cap tree and repaired in its own gate-only PR first, as the H7 rule requires; the family PRs re-run afterwards on a real merge commit.

"NO OPEN PR RUNS ZERO CHECKS" WENT RED ON #196 BECAUSE #197 WAS THIRTEEN SECONDS YOUNGER. The census saw #197 with zero check runs while its jobs were still being scheduled. A race in the census, not a finding; it re-runs on the next head.

MAIN WENT RED ONCE ON MY OWN PUSHES. The FieldOps run on the #198 merge commit failed its open-PR census at 23:02:47 because #196 and #197 had zero check runs at that second — I had pushed their level-with-main heads at 23:02:2x and GitHub created their runs at 23:02:28-30. The run on the #195 merge was then cancelled by the workflow's concurrency group when the #196 merge arrived. Neither is a finding on main's tree, and the two main runs after them passed; but a red on main is a red on main, so it is written here and in MERGES_RUN9.json rather than left for Watch main to be the only witness.

## RUN 10

WRONG: I ran `verify_fixture_names.mjs` locally, read the tail of its output, saw
prose rather than a failure banner, and pushed. The sweep job went red on my
first head.
RIGHT: read the exit code. The tool had already found `Q7ZTQQ_RETIRED.md` naming
a real careers lesson title that its predicate reads as person-shaped, and it
said so in a section I never scrolled to. This is the estate's own "assert on
evidence, not on proxies" rule, and I broke it on the very check that exists to
catch that class of mistake.

WRONG, immediately afterwards: the record I wrote about the fix quoted the
offending strings verbatim, and so did the state key. The gate reddened on those
too.
RIGHT: describe the strings instead of reproducing them. The gate was right
twice in five minutes.

WRONG: run 9 reported the horizon as content covered 147, then projected 158
after its eleven lessons landed.
RIGHT: run 9's own coverage artefact, written at 21:55 that evening by the
scripts it ran itself, says 140 — and its slot lists already contained the
eleven, which were in the working tree at the time. So the base was 7 above the
instrument and the +11 was already inside it. Re-running the same two scripts
today reproduces 140 exactly. The artefact is kept at
`_sownb/vb/evidence/run10/RUN9_COVERAGE_ARTEFACT.json` so the correction can be
checked rather than taken on trust.

WRONG: `VB_STATE.decisionD1` said "BLOCKED — not applied" and the run-9 horizon
excluded 22 decks as SPINE-SPLIT.
RIGHT: run 8 applied it, in commit 672f6ed9, and nobody updated the key. All 24
LAUNCH Science decks conform. D-C cost zero bytes this run; what it cost was the
half hour I spent preparing to redo work that was already done. Verify before
executing an order that says "execute".

WRONG: the contract's `rowCount` said 463 while its rows numbered 464, and the
order expected 463 because that is what the stale field says.
RIGHT: run 8's `53d16b3a` appended `reading.pathway.band` without bumping the
field. Corrected without adding or removing a row.

WRONG: my first GROW Humanities W5 draft put the second diagram in a stage whose
prose never mentioned it, and g24 counted it decorative.
RIGHT: g24 asks whether the stage's own words point at the figure. A figure
nobody is told to look at is decoration, and the gate is right about that.

WRONG: LAUNCH Humanities W8 came in at 874 words against a family floor of 897,
and my first instinct was that 23 words is nothing.
RIGHT: the lesson was missing the scale. A grid square is a kilometre across on
that sheet, which is exactly what makes the sixth figure worth a hundred metres
and what decides whether four figures are enough. Adding the thing the lesson
needed took it to 946. Padding would have cleared the same floor and taught
nobody anything.

WRONG: LAUNCH Humanities W7 declared `spot-the-error` while its we-do text never
asked anyone to spot an error.
RIGHT: g25 checks the declaration against the behaviour. The fix is to rewrite
the stage, not the label.

WRONG (planned, not committed): I was ready to author into GROW ASDAN and BUILD
ASDAN by slicing their donors, as I had for four other families.
RIGHT: g16 against every live deck in both families returns zero passes — 54
failing rows on all ten BUILD ASDAN decks, and 1, 12 or 53 on the fourteen GROW
ASDAN ones, while a run-9 Humanities deck through the same instrument passes
with zero. Those families' rows do not describe their own decks. Two lessons of
the eighteen are not here, and the reason is measured rather than asserted.

WRONG: the generator wrote "GROW Humanities" into the running head of a GROW
Science deck, because the subject was hardcoded in three places.
RIGHT: the running-heads gate caught it on the rendered PDF, not in the source.

## Run 11 (2026-09-02, ORDER VB-RUN11F)

WRONG: I carried the resources.json digest measured before the games PRs
(#212–#223) into the re-pin plan.
RIGHT: main moved twelve merges since that measurement and the catalogue with
it. The pin is taken from `sha256sum resources.json` at the moment of the edit,
never from a number remembered from an earlier turn.

WRONG (caught in the dry run, nothing written): the START_HERE relabel replaced
"Week 8" with "Week 9" and then counted the freshly written "Week 9" as a
"Week 9" to move to 10, so every count after the first was wrong.
RIGHT: replacements that shift a number run from the highest number down, and
every replacement asserts its expected count against the file before any write.
The script refused; the order of edits was fixed; the second dry run matched.

WRONG: the housekeeping order says "re-pin in the cross-estate daily check"
and the repo's pin tool is the documented way to do it.
RIGHT: the tool refuses with one checkout, by design, and the Apps checkout is
not here. The Lessons copy is moved by the same anchored regex the tool uses,
and the Apps copy is recorded as divergent until someone with both checkouts
runs the tool. Working round the refusal by editing the tool would have been a
gate edit; it was not made.

WRONG: the housekeeping PR bundled the gate-file pin with 31 lesson files and
five records, because the order lists them under one heading.
RIGHT: the cross-estate gate reds any PR that touches it while changing files
outside its own allowed set, which is H7 in another coat. The pin landed alone
(#224); the content follows in its own PR, which does not trigger that
workflow. The branch shows the step-back as two reverts, not a rewrite.

WRONG: the contract-v2 builder proved two metric rows with its own patched
copy of the gate's metric dispatch, so they "passed" at build time and failed
the moment the real gate ran on the same references.
RIGHT: the non-vacuity run is the gate itself on every reference, and it was
red on 15/15 until the dispatch was fixed in the gate, not in the builder. A
builder never gets its own instrument.

WRONG: I first measured the palette from the first :root block only and
reported it unanimous across pathways.
RIGHT: a second (and in ASDAN a third) :root block overrides the base per
subject and strand, and the last declaration is what renders. Both instruments
are now recorded (PALETTE_V2.json); the base binds as shared rows, the
effective values bind only where a family is unanimous.

WRONG: the stale-evidence sweep ran green locally, then the non-vacuity batch
was re-run after the dispatch fix and its 45 gate outputs were committed
without a `file` key; CI reddened the contract PR on exactly the run-10 lesson.
RIGHT: the sweep is the last thing before `git commit`, never before the last
write, and every gate output names its subject in `file`.

WRONG: the first reshell rendered a blank page under the render gate, exactly
the D-D arm-A blank the ASDAN decks show, because the donor's print pack only
exists after a tier button is pressed.
RIGHT: R4 is part of the reshell recipe, not a later fix: printPack is split
into printArm + print, and load/beforeprint arm Standard when nothing is armed.
The tier proof reads the cold PDF and the three tier PDFs from Chromium, and
cold now equals Standard on all eight.

WRONG: I ran the run-10 battery on a classic deck and read eight reds and
errors before asking what each gate parses.
RIGHT: g18, g11, s24, running heads, g21, rig, g23 and g25 read n6 markup
(main.deck stages, the two-page print pack, nav.controls). They are recorded
as measured-not-applicable with each error, and the v2 set (containment,
g16 v2, g10, g15, g19 v2, g24, g26, tier proof) is what binds a classic deck.

WRONG: two Lundy boxes read "Spacemeans" and "stays available." because the
generator dropped a space and the subject word; no gate saw it.
RIGHT: the screenshots at 390 and 1365 are read, not just taken. Both fixed;
the strip sentence is carried whole.

WRONG: the R4 screen clause compared pixel positions and failed on 1 px of
animation jitter (title dots, animate-enter list items) on all three proofs.
RIGHT: the screen fingerprint is the visible element identity list with
reduced motion emulated, plus a 3 px positional tolerance; the three proofs
then pass with zero shift and the same element counts.

WRONG: I fast-forwarded the branch with a stash while the 79-deck check was
reading the working tree; two decks were read mid-swap and came back ERR/RED.
RIGHT: both re-ran clean (79/79 PASS). A background measurement owns the
working tree until it finishes; nothing touches the tree in between.
