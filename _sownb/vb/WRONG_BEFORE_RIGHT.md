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
