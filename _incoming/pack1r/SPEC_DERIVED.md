# PACK-1R specification derivation — P1 rulings applied

This source trace is updated for Matt’s R1–R3 rulings. Rendered results are reported separately in REPORT.md and qa/.
Base: Lessons main `3887f7acc99468b55ecc9f0b67b6be043aebc8ed`.
Full findings, 39 objective rows and source hashes: REPORT.md.

## Chassis selector trace

Source: `_sx3/CHASSIS_CONTRACT.md`, the three separate pathway tables and amendments A1–A3. Counts and intentional zeroes remain pathway-specific.

| Requirement | Exact selector / assertion | Source |
|---|---|---|
| Root / container | `main#lessonDeck.slide-container` | rows 1–2 |
| BUILD classification furniture | `nav.classic-toolbar`, `#xpWrap`, `#xpFill`, `#xpCount`, `#xpTotal`, `#lc-overlay`; no `nav.review-top` | BUILD rows 3–8 |
| GROW/LAUNCH classification furniture | `nav.review-top`, `a.skip`; no XP/complete furniture | GROW/LAUNCH rows 3–8 |
| Timer | `#auto-timer`, `#auto-timer-toggle`, `#auto-timer-display` | rows 9–10 |
| Word help / pause / tools / organiser | `#word-dialog`, `#pause-dialog`, `#tools-dialog`, `#organiser-dialog` | rows 11–14 |
| A4 knowledge organiser | `#organiser-dialog`, `#print-organiser`; one A4 page under rendered JS print | row 15, R-KO, row 27; no artificial SVG IDs |
| Staff layer / picker | `#ta-dialog`, `#cold-call-dialog` | rows 16–17 |
| Arrival routes | `#arrival-panel-supported`, `#arrival-panel-standard`, `#arrival-panel-stretch`; each `.arrival-four > article.arrival-cell` × 4, `h3`, `p.arrival-hint`, `p.arrival-answer` | rows 18–20 and content-mapping table |
| Arrival print / staff answers | `#print-arrival-supported`, `#print-arrival-standard`, `#print-arrival-stretch`; `#print-arrival-answers-*` × 3 | rows 21–22 |
| Exit / tasks / print area | `#print-exit-*`, `#print-task-*`, `#print-area` | rows 23–25 |
| Shared / answer / staff print | `#print-answers` or `#all-answers`, `#print-shared`, `.staff-card` or `#print-staff`, `.teacher-only` | rows 26, 28–30 |
| Reveal | `.science-reveal` only where the pathway exemplar has it; no fake equivalence from another markup form | row 31 and R-SR |
| Progress / navigation | `#progressBar`, `#progressLabel`, `#classic-progress`, `p#classic-status`, `#previous-slide`, `#next-slide`, `#slide-picker` | rows 32–34 |
| Stages / config | `.slide`, `script#lesson-config` | rows 35–36; R3: nine stages, 40 minutes in one session |
| Root pathway class | `html.pathway-build`, `html.pathway-grow`, `html.pathway-launch` | pathway-class table row, A3; no theme-* invention |
| BUILD HUD | literal `<script defer src="/hud.js">`; none on other pathways | A1; R1 exemption (a), served-equivalent 200 check |
| Lessons links | BUILD unclassed Lessons anchor; GROW/LAUNCH `a.mbmhome` plus `a.way-home`; relative depth measured from actual target folder | A2; R1 exemptions (b)–(c); two-level target depth and own-folder START_HERE |
| Palette | exact pathway custom-property values; no shared token layer | A3; contrast still measured in rendered browser |
| Storage | no BUILD own storage; only `mbm_guide_v1` under guarded access for other pathways | A3 |
| Provenance | compare all 19 named content-bearing regions against own exemplar; no retained science lesson content | narrative row 37 R-PROV (distinct from old table's pathway-class number) |
| Runtime / dialogs | every interactive element exercised; zero uncaught errors; open/close and real controls; preserved shell-owned nodes | rows 38–42; static parse cannot pass |
| Per-stage loop | `.slide .lundy.hum-t-loop[aria-label="Lundy participation status"]`, `.ls[data-lundy-step][data-state]`, `[data-action="lundy-voice"]`, `[data-action="lundy-audience"]`, `[data-action="lundy-influence"]` | row 45, `_hum/LOOP_CONTRACT.md` §§2,6–7 and `tools/hum/loop_adapter.py` |
| Loop exclusions / independence | zero panels for I Do; one on every response stage; state local to stage; Audience-before-Voice and Influence-before-Audience refused with a message | row 45; real browser proof required |
| Named act | every control feeding Voice visibly labels the act; stage-specific response and next-step branch | row 45 |
| RE safeguard | any community-belief source discussed from source evidence, not personal belief | row 46; all 39 intake lessons strand=Humanities |

## Policy-sourced content (verbatim clauses from uploaded editions)

Numbering is the policy BODY, not the contents page. The following new content will be inside the existing traced containers. Text quotations do not certify DOM behaviour.

| Element / intended container | Exact quotation | Clause / PDF page |
|---|---|---|
| Flexible weekly outcome framing, teacher notes / `#ta-dialog` | “Planning is built on weekly outcomes rather than rigid daily scripts” | Curriculum §5.4, p14 |
| Summer theme in `START_HERE.html` | “Summer” / “Change”; “Year A: Self and Belonging” | Curriculum §§5.1–5.2, p12 |
| Tier 2/3 vocabulary in `#word-dialog` and pre-teaching content | “Vocabulary - Tier 2 and Tier 3 vocabulary explicit in every scheme of work; vocabulary pre-teaching as standard.” | Curriculum §8.2, p20; line-wrap hyphen normalised |
| Oracy in stage task content | “Oracy - structured talk, discussion protocols, presentation, debate; planned across the timetable, not left to chance.” | Curriculum §8.3, p21 |
| Alternative response in arrival/task access text | “Alternative response - symbols, choice boards, AAC, sign, drawing, scribing are all valid responses across the curriculum.” | Curriculum §8.3, p21 |
| PfA / careers line in lesson content | “Practical links in every theme.” / “Subject–career links in schemes of work.” / “GCSE/FS explicitly linked to destinations.” | Curriculum §10 Gatsby 4 table, p23; BUILD/GROW/LAUNCH respectively |
| Reasonable adjustment in task help / `#ta-dialog` | “Extended processing time as standard; no expectation of immediate response.” | Curriculum §12.2, p25 |
| Retrieval purpose (within Arrival under R3) | “Chunking, overlearning and structured retrieval practice across every subject.” | Curriculum §12.2, p26 |
| Knowledge organiser / scaffold purpose | “Memory aids knowledge organisers, vocabulary mats, reference cards as the normal way of working.” | Curriculum §12.2, p26 |
| Space in `#ta-dialog`, quoted from actual edition | “Regulation first. A dysregulated student cannot respond to feedback. Co-regulation and time take priority over the technical content of the feedback.” | Feedback §5, p8 |
| Refusal in `#ta-dialog` | “Permission to refuse; refusal is treated as information.” | Feedback §5, p8 |
| No public comparison in `#ta-dialog` | “Establish Space at the start of the lesson - regulation, key adult, success criteria visible, no public comparison.” | Feedback §14 procedure step 1, p14 |
| Loop order | “All four conditions must be in order, or the cycle is broken.” | Feedback §3, p7 |
| Audience | “The adult names what they heard back to the student” | Feedback §7, p9 |
| R gate in staff layer | “The R code in the margin signifies that the loop has closed that the student responded AND the staff member has engaged with the response.” | Feedback §7, p9 |
| Modalities, pathway-specific in each response panel | “Point, sign, repeat after the adult, demonstrate, EFL clip”; “Short edit in margin; verbal reply; tick off success criteria; student voice clip.”; “In-lesson edit; structured verbal response; for full essays” | Feedback §10 table, p11; the supplied LAUNCH cell ends there |
| Choice board addition | “Selected from symbols - choice boards, AAC, Widgit-supported response.” | Curriculum §14.4, p31 |
| Staff codes | “VF Verbal feedback given here”; “WS Worked with support”; “I Independent”; “NS + … Next step one specific thing”; “E Evidence on EFL”; “R Responded loop closed (Audience has happened)”; “// Self-edit point”; “? Read this back to me” | Feedback §11 table, p12 |
| Lean capture in staff layer, EFL wording retained | “30-second clip, photo, or one-line context note.” “Central tags only. Listen / look before tagging (Audience).” | Feedback §14, p14, steps 2–3; §12 p12 supplies purpose |

## Unresolved trace / execution items

R1: exempt only the exact BUILD HUD tag, A2 Lessons anchors and own-folder a.way-home. Target directories are Humanities_Teesside/<PATHWAY>_W27-W39_2026-27/. Backlinks are ../../index.html (BUILD adds ?subject=Humanities&pathway=BUILD), and a.way-home is ./START_HERE.html. Every lesson has a target column in COVERAGE.csv, including reserved targets for the 36 unauthored rows.

R2: intake-local explicit-population imports are authorised; report output is allowed inside the intake. Class A patterns are ported without executing that module. LISTED is NOT YET APPLICABLE. Internal title/H1/COVERAGE/card consistency replaces registration checking at this stage.

R3: Title, Arrival, Starter, I Do, We Do, I Do 2, We Do 2, Independent, Exit. Timer minutes 0,4,4,5,5,4,4,10,4; Independent starts after 26 minutes, Exit has 4. One session. Arrival includes retrieval. Timer parity is with the science exemplar, not the untimed Humanities batch-1 deck.

The order's new `<head><title>` equality to the principal lesson `<h1>`, exact term-week token and output filenames are explicit PACK-1R additions. Existing principal science page titles are not identical to their lesson headings, so title equality must not be reported as copied exemplar behaviour. Pack file-format / hash / source requirements are PACK-1R output requirements, not policy quotations. The reviewed pack precedent has START_HERE, SHA256SUMS and a changelog but lacks root COVERAGE.csv, source/ and qa/; these requested additions are not falsely attributed to that precedent.

The pre-authoring STOP is closed by the user’s explicit rulings. The separate STOP-P1 gate remains: no further lessons are authored until “P1 ok”. Estate policies, exemplars, tools and registries are unchanged.
