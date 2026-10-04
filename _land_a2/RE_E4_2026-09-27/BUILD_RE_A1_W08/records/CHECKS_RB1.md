# CHECKS_RB1

27 September 2026. Review build only. Nothing published or merged.

**RB1 is not complete: F4 is BLOCKED.** Chromium is absent in this environment and the attempted installation returned invalid/truncated archives. The required 72 pupil PDFs (Pupil_Resources, Knowledge_Organiser and Word_Page for 24 lessons) have not been generated. No old or substitute pupil PDFs are included. HTML export sources and completion scripts are included.

No browser execution, viewport-fit, pointer, playback, or Chromium print result is claimed. Claude’s browser, print and Office review remains required.

## Verified inputs

| Input | SHA-256 |
|---|---|
| RE_A2_LIVE_PARITY_SOURCES.zip | `83952d664b18e803bb6ec7b1c147b89af048487387d503dbf85ceeb58f7c9304` |
| RB1_re_fit.css | `219fc6bb54b3fc84a4f235192b5c7c3344fd4cacafa09740aad880fd77bc9ce0` |
| RB1_re_print.css | `bbabb4bd2d7e9593b2ffdc3da08bed339bfe4444f8ec9a4bbc553d4fafab822e` |
| RE_BUILD_Autumn2_v3_2026-09-25.zip | `d651ee482b9b5adca9353fe3ffcb5b1622396e78360cb9260c92a505810bcef1` |
| RE_GROW_Autumn2_v3_2026-09-25.zip | `747f541919141ebf01c9fb986cacdd890752e2601abd2ce2d3df1ed68eed73e7` |
| RE_LAUNCH_Autumn2_v3_2026-09-25.zip | `bd37e959c77f8676da7715e201db1a678f4c82f0599a0f6893095953a3699480` |
| HR1P2B_2026-09-27.zip | `fbb5d4eb0b94f5df66bcbc5979fecae621ed2de4c1eff0aca1cb41045b856530` |

The live-source manifest contains 243 verified files. Original E2 records were recovered from the three hash-pinned E2 archives: 9/9 required records match their original manifests. Historical E2/E3 records are unchanged and retain their historical findings.

## CSS order

Each lesson ends its head styles with the exact fit block followed by the exact print block. Fit is the last screen-affecting style; print is the absolute last style. Both cannot literally occupy the final style position. The per-lesson audit reports their positions and hashes. Pupil print sources also carry the exact print block. Supplied CSS comments contain the explicitly mandated authoring labels; visible-text leak scans exclude these comments.

## Static HTML results

| Lesson | Checks passed | Unexplained data rows | Unexplained HTML fragments | Failures |
|---|---:|---:|---:|---|
| BUILD_RE_A1_W08 | 34/34 | 0 | 0 | None |
| BUILD_RE_A2_W01 | 44/44 | 0 | 0 | None |
| BUILD_RE_A2_W02 | 43/43 | 0 | 0 | None |
| BUILD_RE_A2_W03 | 43/43 | 0 | 0 | None |
| BUILD_RE_A2_W04 | 43/43 | 0 | 0 | None |
| BUILD_RE_A2_W05 | 43/43 | 0 | 0 | None |
| BUILD_RE_A2_W06 | 43/43 | 0 | 0 | None |
| BUILD_RE_A2_W07 | 44/44 | 0 | 0 | None |
| GROW_RE_A1_W08 | 34/34 | 0 | 0 | None |
| GROW_RE_A2_W01 | 43/43 | 0 | 0 | None |
| GROW_RE_A2_W02 | 43/43 | 0 | 0 | None |
| GROW_RE_A2_W03 | 43/43 | 0 | 0 | None |
| GROW_RE_A2_W04 | 43/43 | 0 | 0 | None |
| GROW_RE_A2_W05 | 43/43 | 0 | 0 | None |
| GROW_RE_A2_W06 | 43/43 | 0 | 0 | None |
| GROW_RE_A2_W07 | 43/43 | 0 | 0 | None |
| LAUNCH_RE_A1_W08 | 34/34 | 0 | 0 | None |
| LAUNCH_RE_A2_W01 | 43/43 | 0 | 0 | None |
| LAUNCH_RE_A2_W02 | 43/43 | 0 | 0 | None |
| LAUNCH_RE_A2_W03 | 43/43 | 0 | 0 | None |
| LAUNCH_RE_A2_W04 | 43/43 | 0 | 0 | None |
| LAUNCH_RE_A2_W05 | 43/43 | 0 | 0 | None |
| LAUNCH_RE_A2_W06 | 43/43 | 0 | 0 | None |
| LAUNCH_RE_A2_W07 | 43/43 | 0 | 0 | None |

Survival classifications distinguish exact retained content from the ruled book-first, P1, F6/F7, rangoli and restoration changes. The per-lesson JSON preserves the compared strings and reasons. No absent E3 source is reconstructed from memory.

## Staff fields and PDF geometry

| Lesson | Staff surfaces present | Required fields present / checked | PDF files | A4 geometry |
|---|---:|---:|---:|---|
| BUILD_RE_A1_W08 | 6/6 | 186/186 | 3 | PASS |
| BUILD_RE_A2_W01 | 6/6 | 186/186 | 2 | PASS |
| BUILD_RE_A2_W02 | 6/6 | 186/186 | 2 | PASS |
| BUILD_RE_A2_W03 | 6/6 | 186/186 | 2 | PASS |
| BUILD_RE_A2_W04 | 6/6 | 186/186 | 2 | PASS |
| BUILD_RE_A2_W05 | 6/6 | 186/186 | 2 | PASS |
| BUILD_RE_A2_W06 | 6/6 | 186/186 | 2 | PASS |
| BUILD_RE_A2_W07 | 6/6 | 186/186 | 2 | PASS |
| GROW_RE_A1_W08 | 6/6 | 186/186 | 3 | PASS |
| GROW_RE_A2_W01 | 6/6 | 186/186 | 2 | PASS |
| GROW_RE_A2_W02 | 6/6 | 186/186 | 2 | PASS |
| GROW_RE_A2_W03 | 6/6 | 186/186 | 2 | PASS |
| GROW_RE_A2_W04 | 6/6 | 186/186 | 2 | PASS |
| GROW_RE_A2_W05 | 6/6 | 186/186 | 2 | PASS |
| GROW_RE_A2_W06 | 6/6 | 186/186 | 2 | PASS |
| GROW_RE_A2_W07 | 6/6 | 186/186 | 2 | PASS |
| LAUNCH_RE_A1_W08 | 6/6 | 186/186 | 3 | PASS |
| LAUNCH_RE_A2_W01 | 6/6 | 186/186 | 2 | PASS |
| LAUNCH_RE_A2_W02 | 6/6 | 186/186 | 2 | PASS |
| LAUNCH_RE_A2_W03 | 6/6 | 186/186 | 2 | PASS |
| LAUNCH_RE_A2_W04 | 6/6 | 186/186 | 2 | PASS |
| LAUNCH_RE_A2_W05 | 6/6 | 186/186 | 2 | PASS |
| LAUNCH_RE_A2_W06 | 6/6 | 186/186 | 2 | PASS |
| LAUNCH_RE_A2_W07 | 6/6 | 186/186 | 2 | PASS |

The field matrix checks the complete IEDP line, preparation substitution, all adaptations and six invitation prompts/answers on TA dialog, Teacher Notes DOCX/PDF, TA PDF, Word staff section and slide 1 notes. Counts and missing fields are in QA/root/cross_surface.json.

## Return-week provenance

BUILD has four pictured choice items; two items map to two source lessons each so all Weeks 1–6 are sampled. GROW has six items. LAUNCH has six including an extended comparison. All three teach the source Week 7 outcome/model, use private RAG guidance, preserve the once-only line, and provide three routes. The 21 source lesson hashes and per-item mappings are preserved in the return source-map records. Recovered GROW source whole-file hashes differ from the pilot’s historical map; title, outcome, model, vocabulary and cards are identical across all seven source lessons. Both hash sets are recorded; byte identity is not claimed.

## Detailed lesson tables

Assessment-source labels E2/E3 are retained where they identify source cards. They are not treated as internal version labels. Office/PDF extraction normalizes line wrapping, including hyphenated words split across lines, before comparing text.

### BUILD_RE_A1_W08

| Item | Result |
|---|---|
| Document shell | PASS |
| Duplicate IDs | PASS |
| F1 CSS exact bytes | PASS |
| F2 CSS exact bytes | PASS |
| CSS final order: fit then print | PASS |
| Nine teaching stages | PASS |
| Nine brandlines | PASS |
| Book lines: opening 0; all other stages 1 | PASS |
| F5 brandlines have no leading zero | PASS |
| Review includes // and ? | PASS |
| OL-2 one bare closed staff disclosure | PASS |
| OL-2 exact staff summary | PASS |
| F8 Planned adaptations | PASS |
| F8 Invite a response | PASS |
| F8 IEDP line exact | PASS |
| F8 five broad areas | PASS |
| F8 six invite routes | PASS |
| F6 preparation line | PASS |
| OL-2 answers-with-staff warning | PASS |
| OL-4 no staff file links in top bar | PASS |
| OL-4 top bar labels | PASS |
| OL-2 staff links outside disclosure | PASS |
| TA opening static counts recorded | PASS |
| Visible internal-word scan | PASS |
| Banned wording scan | PASS |
| Pupil term-week scan excluding allowed headers | PASS |
| No served record filename references | PASS |
| F3 activity print cut heading | PASS |
| OL-9 ledger one H1 | PASS |
| Pupil companion HTML scans | PASS |
| First lesson back staff card | PASS |
| Return private RAG | PASS |
| Return once-only line | PASS |
| Return no dated staff card | PASS |

| Stage | Book line |
|---|---|
| 1 |  |
| 2 | In your book: Glue in today’s strip; date it. Answer questions 1 to 4. |
| 3 | In your book: Number 1 to 3. Write or draw one answer for each. |
| 4 | In your book: Watch the object-card model. No writing yet. |
| 5 | In your book: Write or draw an object and match its reason. |
| 6 | In your book: Write the letter of your answer. Explain one clue. |
| 7 | In your book: Number 1 to 4. Choose the answer or pair for each picture. |
| 8 | In your book: Read back one answer (?); improve it and mark //. |
| 9 | In your book: Describe one object card and give one reason it matters. |

TA opening static evidence: `[{"slide": 1, "title": "Special things, respect and belonging", "count": 0, "lines": [], "pass": true, "words": 0}, {"slide": 2, "title": "Arrival task", "count": 1, "lines": ["In your book: Glue in today’s strip; date it. Answer questions 1 to 4."], "pass": true, "words": 11}, {"slide": 3, "title": "Start the enquiry", "count": 1, "lines": ["In your book: Number 1 to 3. Write or draw one answer for each."], "pass": true, "words": 11}, {"slide": 4, "title": "I do · a worked method", "count": 1, "lines": ["In your book: Watch the object-card model. No writing yet."], "pass": true, "words": 7}, {"slide": 5, "title": "We do · match the evidence", "count": 1, "lines": ["In your book: Write or draw an object and match its reason."], "pass": true, "words": 9}, {"slide": 6, "title": "Check the idea", "count": 1, "lines": ["In your book: Write the letter of your answer. Explain one clue."], "pass": true, "words": 9}, {"slide": 7, "title": "Short individual book check", "count": 1, "lines": ["In your book: Number 1 to 4. Choose the answer or pair for each picture."], "pass": true, "words": 12}, {"slide": 8, "title": "Review and improve", "count": 1, "lines": ["In your book: Read back one answer (?); improve it and mark //."], "pass": true, "words": 10}, {"slide": 9, "title": "Exit ticket", "count": 1, "lines": ["In your book: Describe one object card and give one reason it matters."], "pass": true, "words": 10}]`

TA opening static evidence: `[{"slide": "slide-1", "chars": 412, "text": "Staff planning and targets Special things, respect and belonging Welcome pupils with the same learning goal and normal access arrangements. Introduce the short private check only after teaching the key idea. Begin from what each pupil shows; use fictional sources and accept a quiet response. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Print First lesson back staff card Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-2", "chars": 382, "text": "Staff planning and targets Arrival task Read one arrival prompt at a time. Offer the word bank, a reader, pointing or an exact scribe without choosing an answer. Collect each pupil’s own response before revealing; use what you see to choose the starting support. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Print First lesson back staff card Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-3", "chars": 380, "text": "Staff planning and targets Start the enquiry Give quiet thinking time for the three retrieval prompts. Invite a response by voice, pointing or showing the book. Record a useful misconception privately; use one source clue and hear the pupil’s own answer again. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Print First lesson back staff card Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-4", "chars": 387, "text": "Staff planning and targets I do · a worked method Use the manual model steps at a calm pace. Point to the question and then the relevant source detail. Rehearse the reason once; no writing is needed while pupils watch. Pause for processing before inviting a response. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Print First lesson back staff card Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-5", "chars": 388, "text": "Staff planning and targets We do · match the evidence Offer the shared cards for pupils to move or match. One person suggests and the other checks the evidence; swap after one turn. Hear an individual reason, then reduce the prompt so the pupil can try the link again. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Print First lesson back staff card Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-6", "chars": 373, "text": "Staff planning and targets Check the idea Collect every pupil’s answer letter and a source clue before revealing. Use the wrong option’s diagnosis to choose one teaching move. Do not treat silence or an access need as a misconception; recheck privately. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Print First lesson back staff card Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-7", "chars": 394, "text": "Staff planning and targets Short individual book check Keep this short check individual and low stakes. One adult supports agreed access while the other holds the group. Read or scribe exact words without choosing answers. Record the pupil’s response and support separately. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Print First lesson back staff card Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-8", "chars": 382, "text": "Staff planning and targets Review and improve Ask pupils to read one answer back using ?. Give one precise next step, allow a // edit and check the changed detail. Keep feedback private and record the pupil’s response; rejoin the route at one clearly named step. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Print First lesson back staff card Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-9", "chars": 385, "text": "Staff planning and targets Exit ticket Receive the exit response privately by book, voice, pointing or the agreed mode. Look for the key idea and a relevant source detail. Record the private RAG and access support, then pass one useful next step to the next lesson. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Print First lesson back staff card Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}]`

TA opening counts (static proxy, not browser visibility): `[{"slide": "slide-1", "chars": 412, "text": "Staff planning and targets Special things, respect and belonging Welcome pupils with the same learning goal and normal access arrangements. Introduce the short private check only after teaching the key idea. Begin from what each pupil shows; use fictional sources and accept a quiet response. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Print First lesson back staff card Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-2", "chars": 382, "text": "Staff planning and targets Arrival task Read one arrival prompt at a time. Offer the word bank, a reader, pointing or an exact scribe without choosing an answer. Collect each pupil’s own response before revealing; use what you see to choose the starting support. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Print First lesson back staff card Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-3", "chars": 380, "text": "Staff planning and targets Start the enquiry Give quiet thinking time for the three retrieval prompts. Invite a response by voice, pointing or showing the book. Record a useful misconception privately; use one source clue and hear the pupil’s own answer again. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Print First lesson back staff card Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-4", "chars": 387, "text": "Staff planning and targets I do · a worked method Use the manual model steps at a calm pace. Point to the question and then the relevant source detail. Rehearse the reason once; no writing is needed while pupils watch. Pause for processing before inviting a response. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Print First lesson back staff card Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-5", "chars": 388, "text": "Staff planning and targets We do · match the evidence Offer the shared cards for pupils to move or match. One person suggests and the other checks the evidence; swap after one turn. Hear an individual reason, then reduce the prompt so the pupil can try the link again. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Print First lesson back staff card Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-6", "chars": 373, "text": "Staff planning and targets Check the idea Collect every pupil’s answer letter and a source clue before revealing. Use the wrong option’s diagnosis to choose one teaching move. Do not treat silence or an access need as a misconception; recheck privately. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Print First lesson back staff card Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-7", "chars": 394, "text": "Staff planning and targets Short individual book check Keep this short check individual and low stakes. One adult supports agreed access while the other holds the group. Read or scribe exact words without choosing answers. Record the pupil’s response and support separately. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Print First lesson back staff card Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-8", "chars": 382, "text": "Staff planning and targets Review and improve Ask pupils to read one answer back using ?. Give one precise next step, allow a // edit and check the changed detail. Keep feedback private and record the pupil’s response; rejoin the route at one clearly named step. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Print First lesson back staff card Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-9", "chars": 385, "text": "Staff planning and targets Exit ticket Receive the exit response privately by book, voice, pointing or the agreed mode. Look for the key idea and a relevant source detail. Record the private RAG and access support, then pass one useful next step to the next lesson. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Print First lesson back staff card Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}]`

### BUILD_RE_A2_W01

| Item | Result |
|---|---|
| Document shell | PASS |
| Duplicate IDs | PASS |
| F1 CSS exact bytes | PASS |
| F2 CSS exact bytes | PASS |
| CSS final order: fit then print | PASS |
| Nine teaching stages | PASS |
| Nine brandlines | PASS |
| Book lines: opening 0; all other stages 1 | PASS |
| F5 brandlines have no leading zero | PASS |
| Review includes // and ? | PASS |
| OL-2 one bare closed staff disclosure | PASS |
| OL-2 exact staff summary | PASS |
| F8 Planned adaptations | PASS |
| F8 Invite a response | PASS |
| F8 IEDP line exact | PASS |
| F8 five broad areas | PASS |
| F8 six invite routes | PASS |
| F6 preparation line | PASS |
| OL-2 answers-with-staff warning | PASS |
| OL-3 13 live teacher-card headings | PASS |
| E3 11 staff sections survive | PASS |
| OL-4 no staff file links in top bar | PASS |
| OL-4 top bar labels | PASS |
| OL-2 staff links outside disclosure | PASS |
| TA opening static counts recorded | PASS |
| OL-1 vary-exit retained | PASS |
| OL-1 adapter exact restored hash | PASS |
| OL-1 starter before exit builder | PASS |
| OL-11 arrival prompt exact live | PASS |
| OL-1 exit config unchanged | PASS |
| OL-12 arrival embedded picture equals week PNG | PASS |
| X3 rangoli marked meaning equals evidence | PASS |
| X3 no welcome guests claim | PASS |
| Visible internal-word scan | PASS |
| Banned wording scan | PASS |
| Pupil term-week scan excluding allowed headers | PASS |
| No served record filename references | PASS |
| F3 activity print cut heading | PASS |
| OL-9 ledger one H1 | PASS |
| RB-3 approved mark credit row | PASS |
| RB-3 D1 block byte-identical | PASS |
| OL-9 per-link access checks | PASS |
| OL-3 no unexplained live card sentence loss | PASS |
| Pupil companion HTML scans | PASS |

| Stage | Book line |
|---|---|
| 1 |  |
| 2 | In your book: Glue in today's strip; date it. Answer 1 and 2 first. |
| 3 | In your book: Write one guess for Mystery light after the clues. |
| 4 | In your book: Watch the four model steps. No writing yet. |
| 5 | In your book: Match each card; write one meaning and the evidence card. |
| 6 | In your book: Write the letter of your answer and one reason. |
| 7 | In your book: Draw or write your route's task; use its stem. |
| 8 | In your book: Read back one answer (?); improve it and mark //. |
| 9 | In your book: Answer both questions under today's work. |

TA opening static evidence: `[{"slide": 1, "title": "A festival of light: Diwali", "count": 0, "lines": [], "pass": true, "words": 0}, {"slide": 2, "title": "Arrival", "count": 1, "lines": ["In your book: Glue in today's strip; date it. Answer 1 and 2 first."], "pass": true, "words": 11}, {"slide": 3, "title": "Start the enquiry", "count": 1, "lines": ["In your book: Write one guess for Mystery light after the clues."], "pass": true, "words": 9}, {"slide": 4, "title": "I do · a worked method", "count": 1, "lines": ["In your book: Watch the four model steps. No writing yet."], "pass": true, "words": 8}, {"slide": 5, "title": "We do · match and explain", "count": 1, "lines": ["In your book: Match each card; write one meaning and the evidence card."], "pass": true, "words": 10}, {"slide": 6, "title": "Apply the learning", "count": 1, "lines": ["In your book: Write the letter of your answer and one reason."], "pass": true, "words": 9}, {"slide": 7, "title": "Independent application", "count": 1, "lines": ["In your book: Draw or write your route's task; use its stem."], "pass": true, "words": 9}, {"slide": 8, "title": "Review and improve", "count": 1, "lines": ["In your book: Read back one answer (?); improve it and mark //."], "pass": true, "words": 10}, {"slide": 9, "title": "Exit ticket", "count": 1, "lines": ["In your book: Answer both questions under today's work."], "pass": true, "words": 6}]`

TA opening static evidence: `[{"slide": "slide-1", "chars": 276, "text": "Staff planning and targets A festival of light: Diwali Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-2", "chars": 256, "text": "Staff planning and targets Arrival Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-3", "chars": 266, "text": "Staff planning and targets Start the enquiry Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-4", "chars": 271, "text": "Staff planning and targets I do · a worked method Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-5", "chars": 274, "text": "Staff planning and targets We do · match and explain Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-6", "chars": 267, "text": "Staff planning and targets Apply the learning Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-7", "chars": 272, "text": "Staff planning and targets Independent application Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-8", "chars": 267, "text": "Staff planning and targets Review and improve Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-9", "chars": 260, "text": "Staff planning and targets Exit ticket Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}]`

TA opening counts (static proxy, not browser visibility): `[{"slide": "slide-1", "chars": 276, "text": "Staff planning and targets A festival of light: Diwali Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-2", "chars": 256, "text": "Staff planning and targets Arrival Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-3", "chars": 266, "text": "Staff planning and targets Start the enquiry Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-4", "chars": 271, "text": "Staff planning and targets I do · a worked method Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-5", "chars": 274, "text": "Staff planning and targets We do · match and explain Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-6", "chars": 267, "text": "Staff planning and targets Apply the learning Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-7", "chars": 272, "text": "Staff planning and targets Independent application Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-8", "chars": 267, "text": "Staff planning and targets Review and improve Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-9", "chars": 260, "text": "Staff planning and targets Exit ticket Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}]`

### BUILD_RE_A2_W02

| Item | Result |
|---|---|
| Document shell | PASS |
| Duplicate IDs | PASS |
| F1 CSS exact bytes | PASS |
| F2 CSS exact bytes | PASS |
| CSS final order: fit then print | PASS |
| Nine teaching stages | PASS |
| Nine brandlines | PASS |
| Book lines: opening 0; all other stages 1 | PASS |
| F5 brandlines have no leading zero | PASS |
| Review includes // and ? | PASS |
| OL-2 one bare closed staff disclosure | PASS |
| OL-2 exact staff summary | PASS |
| F8 Planned adaptations | PASS |
| F8 Invite a response | PASS |
| F8 IEDP line exact | PASS |
| F8 five broad areas | PASS |
| F8 six invite routes | PASS |
| F6 preparation line | PASS |
| OL-2 answers-with-staff warning | PASS |
| OL-3 13 live teacher-card headings | PASS |
| E3 11 staff sections survive | PASS |
| OL-4 no staff file links in top bar | PASS |
| OL-4 top bar labels | PASS |
| OL-2 staff links outside disclosure | PASS |
| TA opening static counts recorded | PASS |
| OL-1 vary-exit retained | PASS |
| OL-1 adapter exact restored hash | PASS |
| OL-1 starter before exit builder | PASS |
| OL-11 arrival prompt exact live | PASS |
| OL-1 exit config unchanged | PASS |
| OL-12 arrival embedded picture equals week PNG | PASS |
| X3 no welcome guests claim | PASS |
| Visible internal-word scan | PASS |
| Banned wording scan | PASS |
| Pupil term-week scan excluding allowed headers | PASS |
| No served record filename references | PASS |
| F3 activity print cut heading | PASS |
| OL-9 ledger one H1 | PASS |
| RB-3 approved mark credit row | PASS |
| RB-3 D1 block byte-identical | PASS |
| OL-9 per-link access checks | PASS |
| OL-3 no unexplained live card sentence loss | PASS |
| Pupil companion HTML scans | PASS |

| Stage | Book line |
|---|---|
| 1 |  |
| 2 | In your book: Glue in today's strip; date it. Answer 1 and 2 first. |
| 3 | In your book: Write one response to Which celebration?; use a clue. |
| 4 | In your book: Watch the four model steps. No writing yet. |
| 5 | In your book: Move or match each card; record your explanation and its evidence. |
| 6 | In your book: Write the letter of your answer and one reason. |
| 7 | In your book: Complete your route's task in your book; use its stem. |
| 8 | In your book: Read back one answer (?); improve it and mark //. |
| 9 | In your book: Answer both questions under today's work. |

TA opening static evidence: `[{"slide": 1, "title": "Comparing light in celebrations", "count": 0, "lines": [], "pass": true, "words": 0}, {"slide": 2, "title": "Arrival", "count": 1, "lines": ["In your book: Glue in today's strip; date it. Answer 1 and 2 first."], "pass": true, "words": 11}, {"slide": 3, "title": "Start the enquiry", "count": 1, "lines": ["In your book: Write one response to Which celebration?; use a clue."], "pass": true, "words": 9}, {"slide": 4, "title": "I do · a worked method", "count": 1, "lines": ["In your book: Watch the four model steps. No writing yet."], "pass": true, "words": 8}, {"slide": 5, "title": "We do · sort and justify", "count": 1, "lines": ["In your book: Move or match each card; record your explanation and its evidence."], "pass": true, "words": 11}, {"slide": 6, "title": "Apply the learning", "count": 1, "lines": ["In your book: Write the letter of your answer and one reason."], "pass": true, "words": 9}, {"slide": 7, "title": "Independent application", "count": 1, "lines": ["In your book: Complete your route's task in your book; use its stem."], "pass": true, "words": 10}, {"slide": 8, "title": "Review and improve", "count": 1, "lines": ["In your book: Read back one answer (?); improve it and mark //."], "pass": true, "words": 10}, {"slide": 9, "title": "Exit ticket", "count": 1, "lines": ["In your book: Answer both questions under today's work."], "pass": true, "words": 6}]`

TA opening static evidence: `[{"slide": "slide-1", "chars": 280, "text": "Staff planning and targets Comparing light in celebrations Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-2", "chars": 256, "text": "Staff planning and targets Arrival Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-3", "chars": 266, "text": "Staff planning and targets Start the enquiry Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-4", "chars": 271, "text": "Staff planning and targets I do · a worked method Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-5", "chars": 273, "text": "Staff planning and targets We do · sort and justify Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-6", "chars": 267, "text": "Staff planning and targets Apply the learning Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-7", "chars": 272, "text": "Staff planning and targets Independent application Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-8", "chars": 267, "text": "Staff planning and targets Review and improve Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-9", "chars": 260, "text": "Staff planning and targets Exit ticket Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}]`

TA opening counts (static proxy, not browser visibility): `[{"slide": "slide-1", "chars": 280, "text": "Staff planning and targets Comparing light in celebrations Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-2", "chars": 256, "text": "Staff planning and targets Arrival Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-3", "chars": 266, "text": "Staff planning and targets Start the enquiry Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-4", "chars": 271, "text": "Staff planning and targets I do · a worked method Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-5", "chars": 273, "text": "Staff planning and targets We do · sort and justify Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-6", "chars": 267, "text": "Staff planning and targets Apply the learning Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-7", "chars": 272, "text": "Staff planning and targets Independent application Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-8", "chars": 267, "text": "Staff planning and targets Review and improve Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-9", "chars": 260, "text": "Staff planning and targets Exit ticket Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}]`

### BUILD_RE_A2_W03

| Item | Result |
|---|---|
| Document shell | PASS |
| Duplicate IDs | PASS |
| F1 CSS exact bytes | PASS |
| F2 CSS exact bytes | PASS |
| CSS final order: fit then print | PASS |
| Nine teaching stages | PASS |
| Nine brandlines | PASS |
| Book lines: opening 0; all other stages 1 | PASS |
| F5 brandlines have no leading zero | PASS |
| Review includes // and ? | PASS |
| OL-2 one bare closed staff disclosure | PASS |
| OL-2 exact staff summary | PASS |
| F8 Planned adaptations | PASS |
| F8 Invite a response | PASS |
| F8 IEDP line exact | PASS |
| F8 five broad areas | PASS |
| F8 six invite routes | PASS |
| F6 preparation line | PASS |
| OL-2 answers-with-staff warning | PASS |
| OL-3 13 live teacher-card headings | PASS |
| E3 11 staff sections survive | PASS |
| OL-4 no staff file links in top bar | PASS |
| OL-4 top bar labels | PASS |
| OL-2 staff links outside disclosure | PASS |
| TA opening static counts recorded | PASS |
| OL-1 vary-exit retained | PASS |
| OL-1 adapter exact restored hash | PASS |
| OL-1 starter before exit builder | PASS |
| OL-11 arrival prompt exact live | PASS |
| OL-1 exit config unchanged | PASS |
| OL-12 arrival embedded picture equals week PNG | PASS |
| X3 no welcome guests claim | PASS |
| Visible internal-word scan | PASS |
| Banned wording scan | PASS |
| Pupil term-week scan excluding allowed headers | PASS |
| No served record filename references | PASS |
| F3 activity print cut heading | PASS |
| OL-9 ledger one H1 | PASS |
| RB-3 approved mark credit row | PASS |
| RB-3 D1 block byte-identical | PASS |
| OL-9 per-link access checks | PASS |
| OL-3 no unexplained live card sentence loss | PASS |
| Pupil companion HTML scans | PASS |

| Stage | Book line |
|---|---|
| 1 |  |
| 2 | In your book: Glue in today's strip; date it. Answer 1 and 2 first. |
| 3 | In your book: Write one response to Put the morning in order; use a clue. |
| 4 | In your book: Watch the four model steps. No writing yet. |
| 5 | In your book: Move or match each card; record your explanation and its evidence. |
| 6 | In your book: Write the letter of your answer and one reason. |
| 7 | In your book: Complete your route's task in your book; use its stem. |
| 8 | In your book: Read back one answer (?); improve it and mark //. |
| 9 | In your book: Answer both questions under today's work. |

TA opening static evidence: `[{"slide": 1, "title": "Retelling a festival story", "count": 0, "lines": [], "pass": true, "words": 0}, {"slide": 2, "title": "Arrival", "count": 1, "lines": ["In your book: Glue in today's strip; date it. Answer 1 and 2 first."], "pass": true, "words": 11}, {"slide": 3, "title": "Start the enquiry", "count": 1, "lines": ["In your book: Write one response to Put the morning in order; use a clue."], "pass": true, "words": 12}, {"slide": 4, "title": "I do · a worked method", "count": 1, "lines": ["In your book: Watch the four model steps. No writing yet."], "pass": true, "words": 8}, {"slide": 5, "title": "We do · build the sequence", "count": 1, "lines": ["In your book: Move or match each card; record your explanation and its evidence."], "pass": true, "words": 11}, {"slide": 6, "title": "Apply the learning", "count": 1, "lines": ["In your book: Write the letter of your answer and one reason."], "pass": true, "words": 9}, {"slide": 7, "title": "Independent application", "count": 1, "lines": ["In your book: Complete your route's task in your book; use its stem."], "pass": true, "words": 10}, {"slide": 8, "title": "Review and improve", "count": 1, "lines": ["In your book: Read back one answer (?); improve it and mark //."], "pass": true, "words": 10}, {"slide": 9, "title": "Exit ticket", "count": 1, "lines": ["In your book: Answer both questions under today's work."], "pass": true, "words": 6}]`

TA opening static evidence: `[{"slide": "slide-1", "chars": 275, "text": "Staff planning and targets Retelling a festival story Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-2", "chars": 256, "text": "Staff planning and targets Arrival Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-3", "chars": 266, "text": "Staff planning and targets Start the enquiry Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-4", "chars": 271, "text": "Staff planning and targets I do · a worked method Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-5", "chars": 275, "text": "Staff planning and targets We do · build the sequence Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-6", "chars": 267, "text": "Staff planning and targets Apply the learning Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-7", "chars": 272, "text": "Staff planning and targets Independent application Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-8", "chars": 267, "text": "Staff planning and targets Review and improve Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-9", "chars": 260, "text": "Staff planning and targets Exit ticket Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}]`

TA opening counts (static proxy, not browser visibility): `[{"slide": "slide-1", "chars": 275, "text": "Staff planning and targets Retelling a festival story Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-2", "chars": 256, "text": "Staff planning and targets Arrival Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-3", "chars": 266, "text": "Staff planning and targets Start the enquiry Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-4", "chars": 271, "text": "Staff planning and targets I do · a worked method Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-5", "chars": 275, "text": "Staff planning and targets We do · build the sequence Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-6", "chars": 267, "text": "Staff planning and targets Apply the learning Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-7", "chars": 272, "text": "Staff planning and targets Independent application Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-8", "chars": 267, "text": "Staff planning and targets Review and improve Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-9", "chars": 260, "text": "Staff planning and targets Exit ticket Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}]`

### BUILD_RE_A2_W04

| Item | Result |
|---|---|
| Document shell | PASS |
| Duplicate IDs | PASS |
| F1 CSS exact bytes | PASS |
| F2 CSS exact bytes | PASS |
| CSS final order: fit then print | PASS |
| Nine teaching stages | PASS |
| Nine brandlines | PASS |
| Book lines: opening 0; all other stages 1 | PASS |
| F5 brandlines have no leading zero | PASS |
| Review includes // and ? | PASS |
| OL-2 one bare closed staff disclosure | PASS |
| OL-2 exact staff summary | PASS |
| F8 Planned adaptations | PASS |
| F8 Invite a response | PASS |
| F8 IEDP line exact | PASS |
| F8 five broad areas | PASS |
| F8 six invite routes | PASS |
| F6 preparation line | PASS |
| OL-2 answers-with-staff warning | PASS |
| OL-3 13 live teacher-card headings | PASS |
| E3 11 staff sections survive | PASS |
| OL-4 no staff file links in top bar | PASS |
| OL-4 top bar labels | PASS |
| OL-2 staff links outside disclosure | PASS |
| TA opening static counts recorded | PASS |
| OL-1 vary-exit retained | PASS |
| OL-1 adapter exact restored hash | PASS |
| OL-1 starter before exit builder | PASS |
| OL-11 arrival prompt exact live | PASS |
| OL-1 exit config unchanged | PASS |
| OL-12 arrival embedded picture equals week PNG | PASS |
| X3 no welcome guests claim | PASS |
| Visible internal-word scan | PASS |
| Banned wording scan | PASS |
| Pupil term-week scan excluding allowed headers | PASS |
| No served record filename references | PASS |
| F3 activity print cut heading | PASS |
| OL-9 ledger one H1 | PASS |
| RB-3 approved mark credit row | PASS |
| RB-3 D1 block byte-identical | PASS |
| OL-9 per-link access checks | PASS |
| OL-3 no unexplained live card sentence loss | PASS |
| Pupil companion HTML scans | PASS |

| Stage | Book line |
|---|---|
| 1 |  |
| 2 | In your book: Glue in today's strip; date it. Answer 1 and 2 first. |
| 3 | In your book: Write one response to Respectful or not respectful?; use a clue. |
| 4 | In your book: Watch the four model steps. No writing yet. |
| 5 | In your book: Move or match each card; record your explanation and its evidence. |
| 6 | In your book: Write the letter of your answer and one reason. |
| 7 | In your book: Complete your route's task in your book; use its stem. |
| 8 | In your book: Read back one answer (?); improve it and mark //. |
| 9 | In your book: Answer both questions under today's work. |

TA opening static evidence: `[{"slide": 1, "title": "Taking part respectfully", "count": 0, "lines": [], "pass": true, "words": 0}, {"slide": 2, "title": "Arrival", "count": 1, "lines": ["In your book: Glue in today's strip; date it. Answer 1 and 2 first."], "pass": true, "words": 11}, {"slide": 3, "title": "Start the enquiry", "count": 1, "lines": ["In your book: Write one response to Respectful or not respectful?; use a clue."], "pass": true, "words": 11}, {"slide": 4, "title": "I do · a worked method", "count": 1, "lines": ["In your book: Watch the four model steps. No writing yet."], "pass": true, "words": 8}, {"slide": 5, "title": "We do · choose and explain", "count": 1, "lines": ["In your book: Move or match each card; record your explanation and its evidence."], "pass": true, "words": 11}, {"slide": 6, "title": "Apply the learning", "count": 1, "lines": ["In your book: Write the letter of your answer and one reason."], "pass": true, "words": 9}, {"slide": 7, "title": "Independent application", "count": 1, "lines": ["In your book: Complete your route's task in your book; use its stem."], "pass": true, "words": 10}, {"slide": 8, "title": "Review and improve", "count": 1, "lines": ["In your book: Read back one answer (?); improve it and mark //."], "pass": true, "words": 10}, {"slide": 9, "title": "Exit ticket", "count": 1, "lines": ["In your book: Answer both questions under today's work."], "pass": true, "words": 6}]`

TA opening static evidence: `[{"slide": "slide-1", "chars": 273, "text": "Staff planning and targets Taking part respectfully Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-2", "chars": 256, "text": "Staff planning and targets Arrival Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-3", "chars": 266, "text": "Staff planning and targets Start the enquiry Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-4", "chars": 271, "text": "Staff planning and targets I do · a worked method Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-5", "chars": 275, "text": "Staff planning and targets We do · choose and explain Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-6", "chars": 267, "text": "Staff planning and targets Apply the learning Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-7", "chars": 272, "text": "Staff planning and targets Independent application Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-8", "chars": 267, "text": "Staff planning and targets Review and improve Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-9", "chars": 260, "text": "Staff planning and targets Exit ticket Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}]`

TA opening counts (static proxy, not browser visibility): `[{"slide": "slide-1", "chars": 273, "text": "Staff planning and targets Taking part respectfully Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-2", "chars": 256, "text": "Staff planning and targets Arrival Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-3", "chars": 266, "text": "Staff planning and targets Start the enquiry Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-4", "chars": 271, "text": "Staff planning and targets I do · a worked method Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-5", "chars": 275, "text": "Staff planning and targets We do · choose and explain Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-6", "chars": 267, "text": "Staff planning and targets Apply the learning Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-7", "chars": 272, "text": "Staff planning and targets Independent application Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-8", "chars": 267, "text": "Staff planning and targets Review and improve Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-9", "chars": 260, "text": "Staff planning and targets Exit ticket Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}]`

### BUILD_RE_A2_W05

| Item | Result |
|---|---|
| Document shell | PASS |
| Duplicate IDs | PASS |
| F1 CSS exact bytes | PASS |
| F2 CSS exact bytes | PASS |
| CSS final order: fit then print | PASS |
| Nine teaching stages | PASS |
| Nine brandlines | PASS |
| Book lines: opening 0; all other stages 1 | PASS |
| F5 brandlines have no leading zero | PASS |
| Review includes // and ? | PASS |
| OL-2 one bare closed staff disclosure | PASS |
| OL-2 exact staff summary | PASS |
| F8 Planned adaptations | PASS |
| F8 Invite a response | PASS |
| F8 IEDP line exact | PASS |
| F8 five broad areas | PASS |
| F8 six invite routes | PASS |
| F6 preparation line | PASS |
| OL-2 answers-with-staff warning | PASS |
| OL-3 13 live teacher-card headings | PASS |
| E3 11 staff sections survive | PASS |
| OL-4 no staff file links in top bar | PASS |
| OL-4 top bar labels | PASS |
| OL-2 staff links outside disclosure | PASS |
| TA opening static counts recorded | PASS |
| OL-1 vary-exit retained | PASS |
| OL-1 adapter exact restored hash | PASS |
| OL-1 starter before exit builder | PASS |
| OL-11 arrival prompt exact live | PASS |
| OL-1 exit config unchanged | PASS |
| OL-12 arrival embedded picture equals week PNG | PASS |
| X3 no welcome guests claim | PASS |
| Visible internal-word scan | PASS |
| Banned wording scan | PASS |
| Pupil term-week scan excluding allowed headers | PASS |
| No served record filename references | PASS |
| F3 activity print cut heading | PASS |
| OL-9 ledger one H1 | PASS |
| RB-3 approved mark credit row | PASS |
| RB-3 D1 block byte-identical | PASS |
| OL-9 per-link access checks | PASS |
| OL-3 no unexplained live card sentence loss | PASS |
| Pupil companion HTML scans | PASS |

| Stage | Book line |
|---|---|
| 1 |  |
| 2 | In your book: Glue in today's strip; date it. Answer 1 and 2 first. |
| 3 | In your book: Write one response to Hope, remembrance or neither?; use a clue. |
| 4 | In your book: Watch the four model steps. No writing yet. |
| 5 | In your book: Move or match each card; record your explanation and its evidence. |
| 6 | In your book: Write the letter of your answer and one reason. |
| 7 | In your book: Complete your route's task in your book; use its stem. |
| 8 | In your book: Read back one answer (?); improve it and mark //. |
| 9 | In your book: Answer both questions under today's work. |

TA opening static evidence: `[{"slide": 1, "title": "Hope and remembrance", "count": 0, "lines": [], "pass": true, "words": 0}, {"slide": 2, "title": "Arrival", "count": 1, "lines": ["In your book: Glue in today's strip; date it. Answer 1 and 2 first."], "pass": true, "words": 11}, {"slide": 3, "title": "Start the enquiry", "count": 1, "lines": ["In your book: Write one response to Hope, remembrance or neither?; use a clue."], "pass": true, "words": 11}, {"slide": 4, "title": "I do · a worked method", "count": 1, "lines": ["In your book: Watch the four model steps. No writing yet."], "pass": true, "words": 8}, {"slide": 5, "title": "We do · sort and justify", "count": 1, "lines": ["In your book: Move or match each card; record your explanation and its evidence."], "pass": true, "words": 11}, {"slide": 6, "title": "Apply the learning", "count": 1, "lines": ["In your book: Write the letter of your answer and one reason."], "pass": true, "words": 9}, {"slide": 7, "title": "Independent application", "count": 1, "lines": ["In your book: Complete your route's task in your book; use its stem."], "pass": true, "words": 10}, {"slide": 8, "title": "Review and improve", "count": 1, "lines": ["In your book: Read back one answer (?); improve it and mark //."], "pass": true, "words": 10}, {"slide": 9, "title": "Exit ticket", "count": 1, "lines": ["In your book: Answer both questions under today's work."], "pass": true, "words": 6}]`

TA opening static evidence: `[{"slide": "slide-1", "chars": 269, "text": "Staff planning and targets Hope and remembrance Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-2", "chars": 256, "text": "Staff planning and targets Arrival Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-3", "chars": 266, "text": "Staff planning and targets Start the enquiry Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-4", "chars": 271, "text": "Staff planning and targets I do · a worked method Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-5", "chars": 273, "text": "Staff planning and targets We do · sort and justify Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-6", "chars": 267, "text": "Staff planning and targets Apply the learning Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-7", "chars": 272, "text": "Staff planning and targets Independent application Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-8", "chars": 267, "text": "Staff planning and targets Review and improve Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-9", "chars": 260, "text": "Staff planning and targets Exit ticket Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}]`

TA opening counts (static proxy, not browser visibility): `[{"slide": "slide-1", "chars": 269, "text": "Staff planning and targets Hope and remembrance Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-2", "chars": 256, "text": "Staff planning and targets Arrival Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-3", "chars": 266, "text": "Staff planning and targets Start the enquiry Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-4", "chars": 271, "text": "Staff planning and targets I do · a worked method Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-5", "chars": 273, "text": "Staff planning and targets We do · sort and justify Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-6", "chars": 267, "text": "Staff planning and targets Apply the learning Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-7", "chars": 272, "text": "Staff planning and targets Independent application Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-8", "chars": 267, "text": "Staff planning and targets Review and improve Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-9", "chars": 260, "text": "Staff planning and targets Exit ticket Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}]`

### BUILD_RE_A2_W06

| Item | Result |
|---|---|
| Document shell | PASS |
| Duplicate IDs | PASS |
| F1 CSS exact bytes | PASS |
| F2 CSS exact bytes | PASS |
| CSS final order: fit then print | PASS |
| Nine teaching stages | PASS |
| Nine brandlines | PASS |
| Book lines: opening 0; all other stages 1 | PASS |
| F5 brandlines have no leading zero | PASS |
| Review includes // and ? | PASS |
| OL-2 one bare closed staff disclosure | PASS |
| OL-2 exact staff summary | PASS |
| F8 Planned adaptations | PASS |
| F8 Invite a response | PASS |
| F8 IEDP line exact | PASS |
| F8 five broad areas | PASS |
| F8 six invite routes | PASS |
| F6 preparation line | PASS |
| OL-2 answers-with-staff warning | PASS |
| OL-3 13 live teacher-card headings | PASS |
| E3 11 staff sections survive | PASS |
| OL-4 no staff file links in top bar | PASS |
| OL-4 top bar labels | PASS |
| OL-2 staff links outside disclosure | PASS |
| TA opening static counts recorded | PASS |
| OL-1 vary-exit retained | PASS |
| OL-1 adapter exact restored hash | PASS |
| OL-1 starter before exit builder | PASS |
| OL-11 arrival prompt exact live | PASS |
| OL-1 exit config unchanged | PASS |
| OL-12 arrival embedded picture equals week PNG | PASS |
| X3 no welcome guests claim | PASS |
| Visible internal-word scan | PASS |
| Banned wording scan | PASS |
| Pupil term-week scan excluding allowed headers | PASS |
| No served record filename references | PASS |
| F3 activity print cut heading | PASS |
| OL-9 ledger one H1 | PASS |
| RB-3 approved mark credit row | PASS |
| RB-3 D1 block byte-identical | PASS |
| OL-9 per-link access checks | PASS |
| OL-3 no unexplained live card sentence loss | PASS |
| Pupil companion HTML scans | PASS |

| Stage | Book line |
|---|---|
| 1 |  |
| 2 | In your book: Glue in today's strip; date it. Answer 1 and 2 first. |
| 3 | In your book: Write one response to What makes something special?; use a clue. |
| 4 | In your book: Watch the four model steps. No writing yet. |
| 5 | In your book: Move or match each card; record your explanation and its evidence. |
| 6 | In your book: Write the letter of your answer and one reason. |
| 7 | In your book: Complete your route's task in your book; use its stem. |
| 8 | In your book: Read back one answer (?); improve it and mark //. |
| 9 | In your book: Answer both questions under today's work. |

TA opening static evidence: `[{"slide": 1, "title": "A big question", "count": 0, "lines": [], "pass": true, "words": 0}, {"slide": 2, "title": "Arrival", "count": 1, "lines": ["In your book: Glue in today's strip; date it. Answer 1 and 2 first."], "pass": true, "words": 11}, {"slide": 3, "title": "Start the enquiry", "count": 1, "lines": ["In your book: Write one response to What makes something special?; use a clue."], "pass": true, "words": 11}, {"slide": 4, "title": "I do · a worked method", "count": 1, "lines": ["In your book: Watch the four model steps. No writing yet."], "pass": true, "words": 8}, {"slide": 5, "title": "We do · choose and explain", "count": 1, "lines": ["In your book: Move or match each card; record your explanation and its evidence."], "pass": true, "words": 11}, {"slide": 6, "title": "Apply the learning", "count": 1, "lines": ["In your book: Write the letter of your answer and one reason."], "pass": true, "words": 9}, {"slide": 7, "title": "Independent application", "count": 1, "lines": ["In your book: Complete your route's task in your book; use its stem."], "pass": true, "words": 10}, {"slide": 8, "title": "Review and improve", "count": 1, "lines": ["In your book: Read back one answer (?); improve it and mark //."], "pass": true, "words": 10}, {"slide": 9, "title": "Exit ticket", "count": 1, "lines": ["In your book: Answer both questions under today's work."], "pass": true, "words": 6}]`

TA opening static evidence: `[{"slide": "slide-1", "chars": 263, "text": "Staff planning and targets A big question Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-2", "chars": 256, "text": "Staff planning and targets Arrival Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-3", "chars": 266, "text": "Staff planning and targets Start the enquiry Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-4", "chars": 271, "text": "Staff planning and targets I do · a worked method Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-5", "chars": 275, "text": "Staff planning and targets We do · choose and explain Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-6", "chars": 267, "text": "Staff planning and targets Apply the learning Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-7", "chars": 272, "text": "Staff planning and targets Independent application Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-8", "chars": 267, "text": "Staff planning and targets Review and improve Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-9", "chars": 260, "text": "Staff planning and targets Exit ticket Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}]`

TA opening counts (static proxy, not browser visibility): `[{"slide": "slide-1", "chars": 263, "text": "Staff planning and targets A big question Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-2", "chars": 256, "text": "Staff planning and targets Arrival Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-3", "chars": 266, "text": "Staff planning and targets Start the enquiry Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-4", "chars": 271, "text": "Staff planning and targets I do · a worked method Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-5", "chars": 275, "text": "Staff planning and targets We do · choose and explain Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-6", "chars": 267, "text": "Staff planning and targets Apply the learning Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-7", "chars": 272, "text": "Staff planning and targets Independent application Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-8", "chars": 267, "text": "Staff planning and targets Review and improve Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-9", "chars": 260, "text": "Staff planning and targets Exit ticket Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}]`

### BUILD_RE_A2_W07

| Item | Result |
|---|---|
| Document shell | PASS |
| Duplicate IDs | PASS |
| F1 CSS exact bytes | PASS |
| F2 CSS exact bytes | PASS |
| CSS final order: fit then print | PASS |
| Nine teaching stages | PASS |
| Nine brandlines | PASS |
| Book lines: opening 0; all other stages 1 | PASS |
| F5 brandlines have no leading zero | PASS |
| Review includes // and ? | PASS |
| OL-2 one bare closed staff disclosure | PASS |
| OL-2 exact staff summary | PASS |
| F8 Planned adaptations | PASS |
| F8 Invite a response | PASS |
| F8 IEDP line exact | PASS |
| F8 five broad areas | PASS |
| F8 six invite routes | PASS |
| F6 preparation line | PASS |
| OL-2 answers-with-staff warning | PASS |
| OL-3 13 live teacher-card headings | PASS |
| E3 11 staff sections survive | PASS |
| OL-4 no staff file links in top bar | PASS |
| OL-4 top bar labels | PASS |
| OL-2 staff links outside disclosure | PASS |
| TA opening static counts recorded | PASS |
| OL-1 vary-exit retained | PASS |
| OL-1 adapter exact restored hash | PASS |
| OL-1 starter before exit builder | PASS |
| OL-11 arrival prompt exact live | PASS |
| OL-1 exit config unchanged | PASS |
| OL-12 arrival embedded picture equals week PNG | PASS |
| X3 rangoli marked meaning equals evidence | PASS |
| X3 no welcome guests claim | PASS |
| Visible internal-word scan | PASS |
| Banned wording scan | PASS |
| Pupil term-week scan excluding allowed headers | PASS |
| No served record filename references | PASS |
| F3 activity print cut heading | PASS |
| OL-9 ledger one H1 | PASS |
| RB-3 approved mark credit row | PASS |
| RB-3 D1 block byte-identical | PASS |
| OL-9 per-link access checks | PASS |
| OL-3 no unexplained live card sentence loss | PASS |
| Pupil companion HTML scans | PASS |

| Stage | Book line |
|---|---|
| 1 |  |
| 2 | In your book: Glue in today's strip; date it. Answer 1 and 2 first. |
| 3 | In your book: Write one response to Which pairs are correct?; use a clue. |
| 4 | In your book: Watch the four model steps. No writing yet. |
| 5 | In your book: Move or match each card; record your explanation and its evidence. |
| 6 | In your book: Write the letter of your answer and one reason. |
| 7 | In your book: Complete your route's task in your book; use its stem. |
| 8 | In your book: Read back one answer (?); improve it and mark //. |
| 9 | In your book: Answer both questions under today's work. |

TA opening static evidence: `[{"slide": 1, "title": "Festival reflection and UAS evidence", "count": 0, "lines": [], "pass": true, "words": 0}, {"slide": 2, "title": "Arrival", "count": 1, "lines": ["In your book: Glue in today's strip; date it. Answer 1 and 2 first."], "pass": true, "words": 11}, {"slide": 3, "title": "Start the enquiry", "count": 1, "lines": ["In your book: Write one response to Which pairs are correct?; use a clue."], "pass": true, "words": 11}, {"slide": 4, "title": "I do · a worked method", "count": 1, "lines": ["In your book: Watch the four model steps. No writing yet."], "pass": true, "words": 8}, {"slide": 5, "title": "We do · match and explain", "count": 1, "lines": ["In your book: Move or match each card; record your explanation and its evidence."], "pass": true, "words": 11}, {"slide": 6, "title": "Apply the learning", "count": 1, "lines": ["In your book: Write the letter of your answer and one reason."], "pass": true, "words": 9}, {"slide": 7, "title": "Independent application", "count": 1, "lines": ["In your book: Complete your route's task in your book; use its stem."], "pass": true, "words": 10}, {"slide": 8, "title": "Review and improve", "count": 1, "lines": ["In your book: Read back one answer (?); improve it and mark //."], "pass": true, "words": 10}, {"slide": 9, "title": "Exit ticket", "count": 1, "lines": ["In your book: Answer both questions under today's work."], "pass": true, "words": 6}]`

TA opening static evidence: `[{"slide": "slide-1", "chars": 341, "text": "Staff planning and targets Festival reflection and UAS evidence Use a different example for shared practice. During independent assessment, keep the agreed reader, scribe, glossary or response mode, but withdraw answer models and record prompts separately. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-2", "chars": 312, "text": "Staff planning and targets Arrival Use a different example for shared practice. During independent assessment, keep the agreed reader, scribe, glossary or response mode, but withdraw answer models and record prompts separately. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-3", "chars": 322, "text": "Staff planning and targets Start the enquiry Use a different example for shared practice. During independent assessment, keep the agreed reader, scribe, glossary or response mode, but withdraw answer models and record prompts separately. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-4", "chars": 327, "text": "Staff planning and targets I do · a worked method Use a different example for shared practice. During independent assessment, keep the agreed reader, scribe, glossary or response mode, but withdraw answer models and record prompts separately. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-5", "chars": 330, "text": "Staff planning and targets We do · match and explain Use a different example for shared practice. During independent assessment, keep the agreed reader, scribe, glossary or response mode, but withdraw answer models and record prompts separately. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-6", "chars": 323, "text": "Staff planning and targets Apply the learning Use a different example for shared practice. During independent assessment, keep the agreed reader, scribe, glossary or response mode, but withdraw answer models and record prompts separately. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-7", "chars": 328, "text": "Staff planning and targets Independent application Use a different example for shared practice. During independent assessment, keep the agreed reader, scribe, glossary or response mode, but withdraw answer models and record prompts separately. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-8", "chars": 323, "text": "Staff planning and targets Review and improve Use a different example for shared practice. During independent assessment, keep the agreed reader, scribe, glossary or response mode, but withdraw answer models and record prompts separately. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-9", "chars": 316, "text": "Staff planning and targets Exit ticket Use a different example for shared practice. During independent assessment, keep the agreed reader, scribe, glossary or response mode, but withdraw answer models and record prompts separately. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}]`

TA opening counts (static proxy, not browser visibility): `[{"slide": "slide-1", "chars": 341, "text": "Staff planning and targets Festival reflection and UAS evidence Use a different example for shared practice. During independent assessment, keep the agreed reader, scribe, glossary or response mode, but withdraw answer models and record prompts separately. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-2", "chars": 312, "text": "Staff planning and targets Arrival Use a different example for shared practice. During independent assessment, keep the agreed reader, scribe, glossary or response mode, but withdraw answer models and record prompts separately. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-3", "chars": 322, "text": "Staff planning and targets Start the enquiry Use a different example for shared practice. During independent assessment, keep the agreed reader, scribe, glossary or response mode, but withdraw answer models and record prompts separately. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-4", "chars": 327, "text": "Staff planning and targets I do · a worked method Use a different example for shared practice. During independent assessment, keep the agreed reader, scribe, glossary or response mode, but withdraw answer models and record prompts separately. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-5", "chars": 330, "text": "Staff planning and targets We do · match and explain Use a different example for shared practice. During independent assessment, keep the agreed reader, scribe, glossary or response mode, but withdraw answer models and record prompts separately. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-6", "chars": 323, "text": "Staff planning and targets Apply the learning Use a different example for shared practice. During independent assessment, keep the agreed reader, scribe, glossary or response mode, but withdraw answer models and record prompts separately. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-7", "chars": 328, "text": "Staff planning and targets Independent application Use a different example for shared practice. During independent assessment, keep the agreed reader, scribe, glossary or response mode, but withdraw answer models and record prompts separately. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-8", "chars": 323, "text": "Staff planning and targets Review and improve Use a different example for shared practice. During independent assessment, keep the agreed reader, scribe, glossary or response mode, but withdraw answer models and record prompts separately. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-9", "chars": 316, "text": "Staff planning and targets Exit ticket Use a different example for shared practice. During independent assessment, keep the agreed reader, scribe, glossary or response mode, but withdraw answer models and record prompts separately. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}]`

### GROW_RE_A1_W08

| Item | Result |
|---|---|
| Document shell | PASS |
| Duplicate IDs | PASS |
| F1 CSS exact bytes | PASS |
| F2 CSS exact bytes | PASS |
| CSS final order: fit then print | PASS |
| Nine teaching stages | PASS |
| Nine brandlines | PASS |
| Book lines: opening 0; all other stages 1 | PASS |
| F5 brandlines have no leading zero | PASS |
| Review includes // and ? | PASS |
| OL-2 one bare closed staff disclosure | PASS |
| OL-2 exact staff summary | PASS |
| F8 Planned adaptations | PASS |
| F8 Invite a response | PASS |
| F8 IEDP line exact | PASS |
| F8 five broad areas | PASS |
| F8 six invite routes | PASS |
| F6 preparation line | PASS |
| OL-2 answers-with-staff warning | PASS |
| OL-4 no staff file links in top bar | PASS |
| OL-4 top bar labels | PASS |
| OL-2 staff links outside disclosure | PASS |
| TA opening static counts recorded | PASS |
| Visible internal-word scan | PASS |
| Banned wording scan | PASS |
| Pupil term-week scan excluding allowed headers | PASS |
| No served record filename references | PASS |
| F3 activity print cut heading | PASS |
| OL-9 ledger one H1 | PASS |
| Pupil companion HTML scans | PASS |
| First lesson back staff card | PASS |
| Return private RAG | PASS |
| Return once-only line | PASS |
| Return no dated staff card | PASS |

| Stage | Book line |
|---|---|
| 1 |  |
| 2 | In your book: Glue in today’s strip; date it. Answer questions 1 to 4. |
| 3 | In your book: Number 1 to 3. Write one word for each. |
| 4 | In your book: Watch Ruth and Dan. No writing yet. |
| 5 | In your book: Write each action’s value; explain one match. |
| 6 | In your book: Write the letter of your answer. Explain one clue. |
| 7 | In your book: Write your route’s six answers using its sentence stems. |
| 8 | In your book: Read back one answer (?); improve it and mark //. |
| 9 | In your book: Answer under today’s work: one value and one reason. |

TA opening static evidence: `[{"slide": 1, "title": "Shared values and what we remember", "count": 0, "lines": [], "pass": true, "words": 0}, {"slide": 2, "title": "Arrival task", "count": 1, "lines": ["In your book: Glue in today’s strip; date it. Answer questions 1 to 4."], "pass": true, "words": 11}, {"slide": 3, "title": "Start the enquiry", "count": 1, "lines": ["In your book: Number 1 to 3. Write one word for each."], "pass": true, "words": 9}, {"slide": 4, "title": "I do · a worked method", "count": 1, "lines": ["In your book: Watch Ruth and Dan. No writing yet."], "pass": true, "words": 7}, {"slide": 5, "title": "We do · source detective", "count": 1, "lines": ["In your book: Write each action’s value; explain one match."], "pass": true, "words": 7}, {"slide": 6, "title": "Check the idea", "count": 1, "lines": ["In your book: Write the letter of your answer. Explain one clue."], "pass": true, "words": 9}, {"slide": 7, "title": "Independent book check", "count": 1, "lines": ["In your book: Write your route’s six answers using its sentence stems."], "pass": true, "words": 9}, {"slide": 8, "title": "Review and improve", "count": 1, "lines": ["In your book: Read back one answer (?); improve it and mark //."], "pass": true, "words": 10}, {"slide": 9, "title": "Exit ticket", "count": 1, "lines": ["In your book: Answer under today’s work: one value and one reason."], "pass": true, "words": 9}]`

TA opening static evidence: `[{"slide": "slide-1", "chars": 409, "text": "Staff planning and targets Shared values and what we remember Welcome pupils with the same learning goal and normal access arrangements. Introduce the short private check only after teaching the key idea. Begin from what each pupil shows; use fictional sources and accept a quiet response. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Print First lesson back staff card Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-2", "chars": 382, "text": "Staff planning and targets Arrival task Read one arrival prompt at a time. Offer the word bank, a reader, pointing or an exact scribe without choosing an answer. Collect each pupil’s own response before revealing; use what you see to choose the starting support. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Print First lesson back staff card Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-3", "chars": 380, "text": "Staff planning and targets Start the enquiry Give quiet thinking time for the three retrieval prompts. Invite a response by voice, pointing or showing the book. Record a useful misconception privately; use one source clue and hear the pupil’s own answer again. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Print First lesson back staff card Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-4", "chars": 387, "text": "Staff planning and targets I do · a worked method Use the manual model steps at a calm pace. Point to the question and then the relevant source detail. Rehearse the reason once; no writing is needed while pupils watch. Pause for processing before inviting a response. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Print First lesson back staff card Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-5", "chars": 386, "text": "Staff planning and targets We do · source detective Offer the shared cards for pupils to move or match. One person suggests and the other checks the evidence; swap after one turn. Hear an individual reason, then reduce the prompt so the pupil can try the link again. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Print First lesson back staff card Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-6", "chars": 373, "text": "Staff planning and targets Check the idea Collect every pupil’s answer letter and a source clue before revealing. Use the wrong option’s diagnosis to choose one teaching move. Do not treat silence or an access need as a misconception; recheck privately. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Print First lesson back staff card Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-7", "chars": 389, "text": "Staff planning and targets Independent book check Keep this short check individual and low stakes. One adult supports agreed access while the other holds the group. Read or scribe exact words without choosing answers. Record the pupil’s response and support separately. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Print First lesson back staff card Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-8", "chars": 382, "text": "Staff planning and targets Review and improve Ask pupils to read one answer back using ?. Give one precise next step, allow a // edit and check the changed detail. Keep feedback private and record the pupil’s response; rejoin the route at one clearly named step. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Print First lesson back staff card Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-9", "chars": 385, "text": "Staff planning and targets Exit ticket Receive the exit response privately by book, voice, pointing or the agreed mode. Look for the key idea and a relevant source detail. Record the private RAG and access support, then pass one useful next step to the next lesson. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Print First lesson back staff card Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}]`

TA opening counts (static proxy, not browser visibility): `[{"slide": "slide-1", "chars": 409, "text": "Staff planning and targets Shared values and what we remember Welcome pupils with the same learning goal and normal access arrangements. Introduce the short private check only after teaching the key idea. Begin from what each pupil shows; use fictional sources and accept a quiet response. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Print First lesson back staff card Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-2", "chars": 382, "text": "Staff planning and targets Arrival task Read one arrival prompt at a time. Offer the word bank, a reader, pointing or an exact scribe without choosing an answer. Collect each pupil’s own response before revealing; use what you see to choose the starting support. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Print First lesson back staff card Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-3", "chars": 380, "text": "Staff planning and targets Start the enquiry Give quiet thinking time for the three retrieval prompts. Invite a response by voice, pointing or showing the book. Record a useful misconception privately; use one source clue and hear the pupil’s own answer again. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Print First lesson back staff card Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-4", "chars": 387, "text": "Staff planning and targets I do · a worked method Use the manual model steps at a calm pace. Point to the question and then the relevant source detail. Rehearse the reason once; no writing is needed while pupils watch. Pause for processing before inviting a response. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Print First lesson back staff card Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-5", "chars": 386, "text": "Staff planning and targets We do · source detective Offer the shared cards for pupils to move or match. One person suggests and the other checks the evidence; swap after one turn. Hear an individual reason, then reduce the prompt so the pupil can try the link again. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Print First lesson back staff card Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-6", "chars": 373, "text": "Staff planning and targets Check the idea Collect every pupil’s answer letter and a source clue before revealing. Use the wrong option’s diagnosis to choose one teaching move. Do not treat silence or an access need as a misconception; recheck privately. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Print First lesson back staff card Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-7", "chars": 389, "text": "Staff planning and targets Independent book check Keep this short check individual and low stakes. One adult supports agreed access while the other holds the group. Read or scribe exact words without choosing answers. Record the pupil’s response and support separately. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Print First lesson back staff card Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-8", "chars": 382, "text": "Staff planning and targets Review and improve Ask pupils to read one answer back using ?. Give one precise next step, allow a // edit and check the changed detail. Keep feedback private and record the pupil’s response; rejoin the route at one clearly named step. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Print First lesson back staff card Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-9", "chars": 385, "text": "Staff planning and targets Exit ticket Receive the exit response privately by book, voice, pointing or the agreed mode. Look for the key idea and a relevant source detail. Record the private RAG and access support, then pass one useful next step to the next lesson. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Print First lesson back staff card Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}]`

### GROW_RE_A2_W01

| Item | Result |
|---|---|
| Document shell | PASS |
| Duplicate IDs | PASS |
| F1 CSS exact bytes | PASS |
| F2 CSS exact bytes | PASS |
| CSS final order: fit then print | PASS |
| Nine teaching stages | PASS |
| Nine brandlines | PASS |
| Book lines: opening 0; all other stages 1 | PASS |
| F5 brandlines have no leading zero | PASS |
| Review includes // and ? | PASS |
| OL-2 one bare closed staff disclosure | PASS |
| OL-2 exact staff summary | PASS |
| F8 Planned adaptations | PASS |
| F8 Invite a response | PASS |
| F8 IEDP line exact | PASS |
| F8 five broad areas | PASS |
| F8 six invite routes | PASS |
| F6 preparation line | PASS |
| OL-2 answers-with-staff warning | PASS |
| OL-3 13 live teacher-card headings | PASS |
| E3 11 staff sections survive | PASS |
| OL-4 no staff file links in top bar | PASS |
| OL-4 top bar labels | PASS |
| OL-2 staff links outside disclosure | PASS |
| TA opening static counts recorded | PASS |
| OL-1 vary-exit retained | PASS |
| OL-1 adapter exact restored hash | PASS |
| OL-1 starter before exit builder | PASS |
| OL-11 arrival prompt exact live | PASS |
| OL-1 exit config unchanged | PASS |
| OL-12 arrival embedded picture equals week PNG | PASS |
| X3 no welcome guests claim | PASS |
| Visible internal-word scan | PASS |
| Banned wording scan | PASS |
| Pupil term-week scan excluding allowed headers | PASS |
| No served record filename references | PASS |
| F3 activity print cut heading | PASS |
| OL-9 ledger one H1 | PASS |
| RB-3 approved mark credit row | PASS |
| RB-3 D1 block byte-identical | PASS |
| OL-9 per-link access checks | PASS |
| OL-3 no unexplained live card sentence loss | PASS |
| Pupil companion HTML scans | PASS |

| Stage | Book line |
|---|---|
| 1 |  |
| 2 | In your book: Glue in today's strip; date it. Answer 1 and 2 first. |
| 3 | In your book: Write one response to What helps people feel they belong?; use a clue. |
| 4 | In your book: Watch the four model steps. No writing yet. |
| 5 | In your book: Move or match each card; record your explanation and its evidence. |
| 6 | In your book: Write the letter of your answer and one reason. |
| 7 | In your book: Complete your route's task in your book; use its stem. |
| 8 | In your book: Read back one answer (?); improve it and mark //. |
| 9 | In your book: Answer both questions under today's work. |

TA opening static evidence: `[{"slide": 1, "title": "Belonging across faiths", "count": 0, "lines": [], "pass": true, "words": 0}, {"slide": 2, "title": "Arrival", "count": 1, "lines": ["In your book: Glue in today's strip; date it. Answer 1 and 2 first."], "pass": true, "words": 11}, {"slide": 3, "title": "Start the enquiry", "count": 1, "lines": ["In your book: Write one response to What helps people feel they belong?; use a clue."], "pass": true, "words": 13}, {"slide": 4, "title": "I do · a worked method", "count": 1, "lines": ["In your book: Watch the four model steps. No writing yet."], "pass": true, "words": 8}, {"slide": 5, "title": "We do · sort and justify", "count": 1, "lines": ["In your book: Move or match each card; record your explanation and its evidence."], "pass": true, "words": 11}, {"slide": 6, "title": "Apply the learning", "count": 1, "lines": ["In your book: Write the letter of your answer and one reason."], "pass": true, "words": 9}, {"slide": 7, "title": "Independent application", "count": 1, "lines": ["In your book: Complete your route's task in your book; use its stem."], "pass": true, "words": 10}, {"slide": 8, "title": "Review and improve", "count": 1, "lines": ["In your book: Read back one answer (?); improve it and mark //."], "pass": true, "words": 10}, {"slide": 9, "title": "Exit ticket", "count": 1, "lines": ["In your book: Answer both questions under today's work."], "pass": true, "words": 6}]`

TA opening static evidence: `[{"slide": "slide-1", "chars": 272, "text": "Staff planning and targets Belonging across faiths Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-2", "chars": 256, "text": "Staff planning and targets Arrival Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-3", "chars": 266, "text": "Staff planning and targets Start the enquiry Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-4", "chars": 271, "text": "Staff planning and targets I do · a worked method Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-5", "chars": 273, "text": "Staff planning and targets We do · sort and justify Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-6", "chars": 267, "text": "Staff planning and targets Apply the learning Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-7", "chars": 272, "text": "Staff planning and targets Independent application Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-8", "chars": 267, "text": "Staff planning and targets Review and improve Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-9", "chars": 260, "text": "Staff planning and targets Exit ticket Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}]`

TA opening counts (static proxy, not browser visibility): `[{"slide": "slide-1", "chars": 272, "text": "Staff planning and targets Belonging across faiths Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-2", "chars": 256, "text": "Staff planning and targets Arrival Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-3", "chars": 266, "text": "Staff planning and targets Start the enquiry Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-4", "chars": 271, "text": "Staff planning and targets I do · a worked method Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-5", "chars": 273, "text": "Staff planning and targets We do · sort and justify Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-6", "chars": 267, "text": "Staff planning and targets Apply the learning Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-7", "chars": 272, "text": "Staff planning and targets Independent application Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-8", "chars": 267, "text": "Staff planning and targets Review and improve Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-9", "chars": 260, "text": "Staff planning and targets Exit ticket Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}]`

### GROW_RE_A2_W02

| Item | Result |
|---|---|
| Document shell | PASS |
| Duplicate IDs | PASS |
| F1 CSS exact bytes | PASS |
| F2 CSS exact bytes | PASS |
| CSS final order: fit then print | PASS |
| Nine teaching stages | PASS |
| Nine brandlines | PASS |
| Book lines: opening 0; all other stages 1 | PASS |
| F5 brandlines have no leading zero | PASS |
| Review includes // and ? | PASS |
| OL-2 one bare closed staff disclosure | PASS |
| OL-2 exact staff summary | PASS |
| F8 Planned adaptations | PASS |
| F8 Invite a response | PASS |
| F8 IEDP line exact | PASS |
| F8 five broad areas | PASS |
| F8 six invite routes | PASS |
| F6 preparation line | PASS |
| OL-2 answers-with-staff warning | PASS |
| OL-3 13 live teacher-card headings | PASS |
| E3 11 staff sections survive | PASS |
| OL-4 no staff file links in top bar | PASS |
| OL-4 top bar labels | PASS |
| OL-2 staff links outside disclosure | PASS |
| TA opening static counts recorded | PASS |
| OL-1 vary-exit retained | PASS |
| OL-1 adapter exact restored hash | PASS |
| OL-1 starter before exit builder | PASS |
| OL-11 arrival prompt exact live | PASS |
| OL-1 exit config unchanged | PASS |
| OL-12 arrival embedded picture equals week PNG | PASS |
| X3 no welcome guests claim | PASS |
| Visible internal-word scan | PASS |
| Banned wording scan | PASS |
| Pupil term-week scan excluding allowed headers | PASS |
| No served record filename references | PASS |
| F3 activity print cut heading | PASS |
| OL-9 ledger one H1 | PASS |
| RB-3 approved mark credit row | PASS |
| RB-3 D1 block byte-identical | PASS |
| OL-9 per-link access checks | PASS |
| OL-3 no unexplained live card sentence loss | PASS |
| Pupil companion HTML scans | PASS |

| Stage | Book line |
|---|---|
| 1 |  |
| 2 | In your book: Glue in today's strip; date it. Answer 1 and 2 first. |
| 3 | In your book: Write one response to Photo reveal: what clues show a place of worship?; use a clue. |
| 4 | In your book: Watch the four model steps. No writing yet. |
| 5 | In your book: Move or match each card; record your explanation and its evidence. |
| 6 | In your book: Write the letter of your answer and one reason. |
| 7 | In your book: Complete your route's task in your book; use its stem. |
| 8 | In your book: Read back one answer (?); improve it and mark //. |
| 9 | In your book: Answer both questions under today's work. |

TA opening static evidence: `[{"slide": 1, "title": "Place of worship enquiry", "count": 0, "lines": [], "pass": true, "words": 0}, {"slide": 2, "title": "Arrival", "count": 1, "lines": ["In your book: Glue in today's strip; date it. Answer 1 and 2 first."], "pass": true, "words": 11}, {"slide": 3, "title": "Start the enquiry", "count": 1, "lines": ["In your book: Write one response to Photo reveal: what clues show a place of worship?; use a clue."], "pass": true, "words": 16}, {"slide": 4, "title": "I do · a worked method", "count": 1, "lines": ["In your book: Watch the four model steps. No writing yet."], "pass": true, "words": 8}, {"slide": 5, "title": "We do · source detective", "count": 1, "lines": ["In your book: Move or match each card; record your explanation and its evidence."], "pass": true, "words": 11}, {"slide": 6, "title": "Apply the learning", "count": 1, "lines": ["In your book: Write the letter of your answer and one reason."], "pass": true, "words": 9}, {"slide": 7, "title": "Independent application", "count": 1, "lines": ["In your book: Complete your route's task in your book; use its stem."], "pass": true, "words": 10}, {"slide": 8, "title": "Review and improve", "count": 1, "lines": ["In your book: Read back one answer (?); improve it and mark //."], "pass": true, "words": 10}, {"slide": 9, "title": "Exit ticket", "count": 1, "lines": ["In your book: Answer both questions under today's work."], "pass": true, "words": 6}]`

TA opening static evidence: `[{"slide": "slide-1", "chars": 273, "text": "Staff planning and targets Place of worship enquiry Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-2", "chars": 256, "text": "Staff planning and targets Arrival Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-3", "chars": 266, "text": "Staff planning and targets Start the enquiry Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-4", "chars": 271, "text": "Staff planning and targets I do · a worked method Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-5", "chars": 273, "text": "Staff planning and targets We do · source detective Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-6", "chars": 267, "text": "Staff planning and targets Apply the learning Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-7", "chars": 272, "text": "Staff planning and targets Independent application Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-8", "chars": 267, "text": "Staff planning and targets Review and improve Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-9", "chars": 260, "text": "Staff planning and targets Exit ticket Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}]`

TA opening counts (static proxy, not browser visibility): `[{"slide": "slide-1", "chars": 273, "text": "Staff planning and targets Place of worship enquiry Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-2", "chars": 256, "text": "Staff planning and targets Arrival Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-3", "chars": 266, "text": "Staff planning and targets Start the enquiry Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-4", "chars": 271, "text": "Staff planning and targets I do · a worked method Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-5", "chars": 273, "text": "Staff planning and targets We do · source detective Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-6", "chars": 267, "text": "Staff planning and targets Apply the learning Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-7", "chars": 272, "text": "Staff planning and targets Independent application Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-8", "chars": 267, "text": "Staff planning and targets Review and improve Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-9", "chars": 260, "text": "Staff planning and targets Exit ticket Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}]`

### GROW_RE_A2_W03

| Item | Result |
|---|---|
| Document shell | PASS |
| Duplicate IDs | PASS |
| F1 CSS exact bytes | PASS |
| F2 CSS exact bytes | PASS |
| CSS final order: fit then print | PASS |
| Nine teaching stages | PASS |
| Nine brandlines | PASS |
| Book lines: opening 0; all other stages 1 | PASS |
| F5 brandlines have no leading zero | PASS |
| Review includes // and ? | PASS |
| OL-2 one bare closed staff disclosure | PASS |
| OL-2 exact staff summary | PASS |
| F8 Planned adaptations | PASS |
| F8 Invite a response | PASS |
| F8 IEDP line exact | PASS |
| F8 five broad areas | PASS |
| F8 six invite routes | PASS |
| F6 preparation line | PASS |
| OL-2 answers-with-staff warning | PASS |
| OL-3 13 live teacher-card headings | PASS |
| E3 11 staff sections survive | PASS |
| OL-4 no staff file links in top bar | PASS |
| OL-4 top bar labels | PASS |
| OL-2 staff links outside disclosure | PASS |
| TA opening static counts recorded | PASS |
| OL-1 vary-exit retained | PASS |
| OL-1 adapter exact restored hash | PASS |
| OL-1 starter before exit builder | PASS |
| OL-11 arrival prompt exact live | PASS |
| OL-1 exit config unchanged | PASS |
| OL-12 arrival embedded picture equals week PNG | PASS |
| X3 no welcome guests claim | PASS |
| Visible internal-word scan | PASS |
| Banned wording scan | PASS |
| Pupil term-week scan excluding allowed headers | PASS |
| No served record filename references | PASS |
| F3 activity print cut heading | PASS |
| OL-9 ledger one H1 | PASS |
| RB-3 approved mark credit row | PASS |
| RB-3 D1 block byte-identical | PASS |
| OL-9 per-link access checks | PASS |
| OL-3 no unexplained live card sentence loss | PASS |
| Pupil companion HTML scans | PASS |

| Stage | Book line |
|---|---|
| 1 |  |
| 2 | In your book: Glue in today's strip; date it. Answer 1 and 2 first. |
| 3 | In your book: Write one response to Match the word to the image idea; use a clue. |
| 4 | In your book: Watch the four model steps. No writing yet. |
| 5 | In your book: Move or match each card; record your explanation and its evidence. |
| 6 | In your book: Write the letter of your answer and one reason. |
| 7 | In your book: Complete your route's task in your book; use its stem. |
| 8 | In your book: Read back one answer (?); improve it and mark //. |
| 9 | In your book: Answer both questions under today's work. |

TA opening static evidence: `[{"slide": 1, "title": "Religious practice and subject vocabulary", "count": 0, "lines": [], "pass": true, "words": 0}, {"slide": 2, "title": "Arrival", "count": 1, "lines": ["In your book: Glue in today's strip; date it. Answer 1 and 2 first."], "pass": true, "words": 11}, {"slide": 3, "title": "Start the enquiry", "count": 1, "lines": ["In your book: Write one response to Match the word to the image idea; use a clue."], "pass": true, "words": 14}, {"slide": 4, "title": "I do · a worked method", "count": 1, "lines": ["In your book: Watch the four model steps. No writing yet."], "pass": true, "words": 8}, {"slide": 5, "title": "We do · repair the draft", "count": 1, "lines": ["In your book: Move or match each card; record your explanation and its evidence."], "pass": true, "words": 11}, {"slide": 6, "title": "Apply the learning", "count": 1, "lines": ["In your book: Write the letter of your answer and one reason."], "pass": true, "words": 9}, {"slide": 7, "title": "Independent application", "count": 1, "lines": ["In your book: Complete your route's task in your book; use its stem."], "pass": true, "words": 10}, {"slide": 8, "title": "Review and improve", "count": 1, "lines": ["In your book: Read back one answer (?); improve it and mark //."], "pass": true, "words": 10}, {"slide": 9, "title": "Exit ticket", "count": 1, "lines": ["In your book: Answer both questions under today's work."], "pass": true, "words": 6}]`

TA opening static evidence: `[{"slide": "slide-1", "chars": 290, "text": "Staff planning and targets Religious practice and subject vocabulary Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-2", "chars": 256, "text": "Staff planning and targets Arrival Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-3", "chars": 266, "text": "Staff planning and targets Start the enquiry Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-4", "chars": 271, "text": "Staff planning and targets I do · a worked method Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-5", "chars": 273, "text": "Staff planning and targets We do · repair the draft Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-6", "chars": 267, "text": "Staff planning and targets Apply the learning Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-7", "chars": 272, "text": "Staff planning and targets Independent application Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-8", "chars": 267, "text": "Staff planning and targets Review and improve Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-9", "chars": 260, "text": "Staff planning and targets Exit ticket Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}]`

TA opening counts (static proxy, not browser visibility): `[{"slide": "slide-1", "chars": 290, "text": "Staff planning and targets Religious practice and subject vocabulary Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-2", "chars": 256, "text": "Staff planning and targets Arrival Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-3", "chars": 266, "text": "Staff planning and targets Start the enquiry Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-4", "chars": 271, "text": "Staff planning and targets I do · a worked method Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-5", "chars": 273, "text": "Staff planning and targets We do · repair the draft Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-6", "chars": 267, "text": "Staff planning and targets Apply the learning Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-7", "chars": 272, "text": "Staff planning and targets Independent application Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-8", "chars": 267, "text": "Staff planning and targets Review and improve Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-9", "chars": 260, "text": "Staff planning and targets Exit ticket Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}]`

### GROW_RE_A2_W04

| Item | Result |
|---|---|
| Document shell | PASS |
| Duplicate IDs | PASS |
| F1 CSS exact bytes | PASS |
| F2 CSS exact bytes | PASS |
| CSS final order: fit then print | PASS |
| Nine teaching stages | PASS |
| Nine brandlines | PASS |
| Book lines: opening 0; all other stages 1 | PASS |
| F5 brandlines have no leading zero | PASS |
| Review includes // and ? | PASS |
| OL-2 one bare closed staff disclosure | PASS |
| OL-2 exact staff summary | PASS |
| F8 Planned adaptations | PASS |
| F8 Invite a response | PASS |
| F8 IEDP line exact | PASS |
| F8 five broad areas | PASS |
| F8 six invite routes | PASS |
| F6 preparation line | PASS |
| OL-2 answers-with-staff warning | PASS |
| OL-3 13 live teacher-card headings | PASS |
| E3 11 staff sections survive | PASS |
| OL-4 no staff file links in top bar | PASS |
| OL-4 top bar labels | PASS |
| OL-2 staff links outside disclosure | PASS |
| TA opening static counts recorded | PASS |
| OL-1 vary-exit retained | PASS |
| OL-1 adapter exact restored hash | PASS |
| OL-1 starter before exit builder | PASS |
| OL-11 arrival prompt exact live | PASS |
| OL-1 exit config unchanged | PASS |
| OL-12 arrival embedded picture equals week PNG | PASS |
| X3 no welcome guests claim | PASS |
| Visible internal-word scan | PASS |
| Banned wording scan | PASS |
| Pupil term-week scan excluding allowed headers | PASS |
| No served record filename references | PASS |
| F3 activity print cut heading | PASS |
| OL-9 ledger one H1 | PASS |
| RB-3 approved mark credit row | PASS |
| RB-3 D1 block byte-identical | PASS |
| OL-9 per-link access checks | PASS |
| OL-3 no unexplained live card sentence loss | PASS |
| Pupil companion HTML scans | PASS |

| Stage | Book line |
|---|---|
| 1 |  |
| 2 | In your book: Glue in today's strip; date it. Answer 1 and 2 first. |
| 3 | In your book: Write one response to Choose a big question; use a clue. |
| 4 | In your book: Watch the four model steps. No writing yet. |
| 5 | In your book: Move or match each card; record your explanation and its evidence. |
| 6 | In your book: Write the letter of your answer and one reason. |
| 7 | In your book: Complete your route's task in your book; use its stem. |
| 8 | In your book: Read back one answer (?); improve it and mark //. |
| 9 | In your book: Answer both questions under today's work. |

TA opening static evidence: `[{"slide": 1, "title": "Big question: do beliefs make us who we are?", "count": 0, "lines": [], "pass": true, "words": 0}, {"slide": 2, "title": "Arrival", "count": 1, "lines": ["In your book: Glue in today's strip; date it. Answer 1 and 2 first."], "pass": true, "words": 11}, {"slide": 3, "title": "Start the enquiry", "count": 1, "lines": ["In your book: Write one response to Choose a big question; use a clue."], "pass": true, "words": 11}, {"slide": 4, "title": "I do · a worked method", "count": 1, "lines": ["In your book: Watch the four model steps. No writing yet."], "pass": true, "words": 8}, {"slide": 5, "title": "We do · choose and explain", "count": 1, "lines": ["In your book: Move or match each card; record your explanation and its evidence."], "pass": true, "words": 11}, {"slide": 6, "title": "Apply the learning", "count": 1, "lines": ["In your book: Write the letter of your answer and one reason."], "pass": true, "words": 9}, {"slide": 7, "title": "Independent application", "count": 1, "lines": ["In your book: Complete your route's task in your book; use its stem."], "pass": true, "words": 10}, {"slide": 8, "title": "Review and improve", "count": 1, "lines": ["In your book: Read back one answer (?); improve it and mark //."], "pass": true, "words": 10}, {"slide": 9, "title": "Exit ticket", "count": 1, "lines": ["In your book: Answer both questions under today's work."], "pass": true, "words": 6}]`

TA opening static evidence: `[{"slide": "slide-1", "chars": 293, "text": "Staff planning and targets Big question: do beliefs make us who we are? Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-2", "chars": 256, "text": "Staff planning and targets Arrival Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-3", "chars": 266, "text": "Staff planning and targets Start the enquiry Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-4", "chars": 271, "text": "Staff planning and targets I do · a worked method Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-5", "chars": 275, "text": "Staff planning and targets We do · choose and explain Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-6", "chars": 267, "text": "Staff planning and targets Apply the learning Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-7", "chars": 272, "text": "Staff planning and targets Independent application Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-8", "chars": 267, "text": "Staff planning and targets Review and improve Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-9", "chars": 260, "text": "Staff planning and targets Exit ticket Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}]`

TA opening counts (static proxy, not browser visibility): `[{"slide": "slide-1", "chars": 293, "text": "Staff planning and targets Big question: do beliefs make us who we are? Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-2", "chars": 256, "text": "Staff planning and targets Arrival Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-3", "chars": 266, "text": "Staff planning and targets Start the enquiry Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-4", "chars": 271, "text": "Staff planning and targets I do · a worked method Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-5", "chars": 275, "text": "Staff planning and targets We do · choose and explain Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-6", "chars": 267, "text": "Staff planning and targets Apply the learning Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-7", "chars": 272, "text": "Staff planning and targets Independent application Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-8", "chars": 267, "text": "Staff planning and targets Review and improve Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-9", "chars": 260, "text": "Staff planning and targets Exit ticket Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}]`

### GROW_RE_A2_W05

| Item | Result |
|---|---|
| Document shell | PASS |
| Duplicate IDs | PASS |
| F1 CSS exact bytes | PASS |
| F2 CSS exact bytes | PASS |
| CSS final order: fit then print | PASS |
| Nine teaching stages | PASS |
| Nine brandlines | PASS |
| Book lines: opening 0; all other stages 1 | PASS |
| F5 brandlines have no leading zero | PASS |
| Review includes // and ? | PASS |
| OL-2 one bare closed staff disclosure | PASS |
| OL-2 exact staff summary | PASS |
| F8 Planned adaptations | PASS |
| F8 Invite a response | PASS |
| F8 IEDP line exact | PASS |
| F8 five broad areas | PASS |
| F8 six invite routes | PASS |
| F6 preparation line | PASS |
| OL-2 answers-with-staff warning | PASS |
| OL-3 13 live teacher-card headings | PASS |
| E3 11 staff sections survive | PASS |
| OL-4 no staff file links in top bar | PASS |
| OL-4 top bar labels | PASS |
| OL-2 staff links outside disclosure | PASS |
| TA opening static counts recorded | PASS |
| OL-1 vary-exit retained | PASS |
| OL-1 adapter exact restored hash | PASS |
| OL-1 starter before exit builder | PASS |
| OL-11 arrival prompt exact live | PASS |
| OL-1 exit config unchanged | PASS |
| OL-12 arrival embedded picture equals week PNG | PASS |
| X3 no welcome guests claim | PASS |
| Visible internal-word scan | PASS |
| Banned wording scan | PASS |
| Pupil term-week scan excluding allowed headers | PASS |
| No served record filename references | PASS |
| F3 activity print cut heading | PASS |
| OL-9 ledger one H1 | PASS |
| RB-3 approved mark credit row | PASS |
| RB-3 D1 block byte-identical | PASS |
| OL-9 per-link access checks | PASS |
| OL-3 no unexplained live card sentence loss | PASS |
| Pupil companion HTML scans | PASS |

| Stage | Book line |
|---|---|
| 1 |  |
| 2 | In your book: Glue in today's strip; date it. Answer 1 and 2 first. |
| 3 | In your book: Write one response to Good question or poor question?; use a clue. |
| 4 | In your book: Watch the four model steps. No writing yet. |
| 5 | In your book: Move or match each card; record your explanation and its evidence. |
| 6 | In your book: Write the letter of your answer and one reason. |
| 7 | In your book: Complete your route's task in your book; use its stem. |
| 8 | In your book: Read back one answer (?); improve it and mark //. |
| 9 | In your book: Answer both questions under today's work. |

TA opening static evidence: `[{"slide": 1, "title": "Questions for a faith or belief visitor", "count": 0, "lines": [], "pass": true, "words": 0}, {"slide": 2, "title": "Arrival", "count": 1, "lines": ["In your book: Glue in today's strip; date it. Answer 1 and 2 first."], "pass": true, "words": 11}, {"slide": 3, "title": "Start the enquiry", "count": 1, "lines": ["In your book: Write one response to Good question or poor question?; use a clue."], "pass": true, "words": 12}, {"slide": 4, "title": "I do · a worked method", "count": 1, "lines": ["In your book: Watch the four model steps. No writing yet."], "pass": true, "words": 8}, {"slide": 5, "title": "We do · sort and justify", "count": 1, "lines": ["In your book: Move or match each card; record your explanation and its evidence."], "pass": true, "words": 11}, {"slide": 6, "title": "Apply the learning", "count": 1, "lines": ["In your book: Write the letter of your answer and one reason."], "pass": true, "words": 9}, {"slide": 7, "title": "Independent application", "count": 1, "lines": ["In your book: Complete your route's task in your book; use its stem."], "pass": true, "words": 10}, {"slide": 8, "title": "Review and improve", "count": 1, "lines": ["In your book: Read back one answer (?); improve it and mark //."], "pass": true, "words": 10}, {"slide": 9, "title": "Exit ticket", "count": 1, "lines": ["In your book: Answer both questions under today's work."], "pass": true, "words": 6}]`

TA opening static evidence: `[{"slide": "slide-1", "chars": 288, "text": "Staff planning and targets Questions for a faith or belief visitor Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-2", "chars": 256, "text": "Staff planning and targets Arrival Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-3", "chars": 266, "text": "Staff planning and targets Start the enquiry Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-4", "chars": 271, "text": "Staff planning and targets I do · a worked method Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-5", "chars": 273, "text": "Staff planning and targets We do · sort and justify Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-6", "chars": 267, "text": "Staff planning and targets Apply the learning Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-7", "chars": 272, "text": "Staff planning and targets Independent application Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-8", "chars": 267, "text": "Staff planning and targets Review and improve Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-9", "chars": 260, "text": "Staff planning and targets Exit ticket Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}]`

TA opening counts (static proxy, not browser visibility): `[{"slide": "slide-1", "chars": 288, "text": "Staff planning and targets Questions for a faith or belief visitor Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-2", "chars": 256, "text": "Staff planning and targets Arrival Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-3", "chars": 266, "text": "Staff planning and targets Start the enquiry Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-4", "chars": 271, "text": "Staff planning and targets I do · a worked method Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-5", "chars": 273, "text": "Staff planning and targets We do · sort and justify Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-6", "chars": 267, "text": "Staff planning and targets Apply the learning Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-7", "chars": 272, "text": "Staff planning and targets Independent application Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-8", "chars": 267, "text": "Staff planning and targets Review and improve Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-9", "chars": 260, "text": "Staff planning and targets Exit ticket Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}]`

### GROW_RE_A2_W06

| Item | Result |
|---|---|
| Document shell | PASS |
| Duplicate IDs | PASS |
| F1 CSS exact bytes | PASS |
| F2 CSS exact bytes | PASS |
| CSS final order: fit then print | PASS |
| Nine teaching stages | PASS |
| Nine brandlines | PASS |
| Book lines: opening 0; all other stages 1 | PASS |
| F5 brandlines have no leading zero | PASS |
| Review includes // and ? | PASS |
| OL-2 one bare closed staff disclosure | PASS |
| OL-2 exact staff summary | PASS |
| F8 Planned adaptations | PASS |
| F8 Invite a response | PASS |
| F8 IEDP line exact | PASS |
| F8 five broad areas | PASS |
| F8 six invite routes | PASS |
| F6 preparation line | PASS |
| OL-2 answers-with-staff warning | PASS |
| OL-3 13 live teacher-card headings | PASS |
| E3 11 staff sections survive | PASS |
| OL-4 no staff file links in top bar | PASS |
| OL-4 top bar labels | PASS |
| OL-2 staff links outside disclosure | PASS |
| TA opening static counts recorded | PASS |
| OL-1 vary-exit retained | PASS |
| OL-1 adapter exact restored hash | PASS |
| OL-1 starter before exit builder | PASS |
| OL-11 arrival prompt exact live | PASS |
| OL-1 exit config unchanged | PASS |
| OL-12 arrival embedded picture equals week PNG | PASS |
| X3 no welcome guests claim | PASS |
| Visible internal-word scan | PASS |
| Banned wording scan | PASS |
| Pupil term-week scan excluding allowed headers | PASS |
| No served record filename references | PASS |
| F3 activity print cut heading | PASS |
| OL-9 ledger one H1 | PASS |
| RB-3 approved mark credit row | PASS |
| RB-3 D1 block byte-identical | PASS |
| OL-9 per-link access checks | PASS |
| OL-3 no unexplained live card sentence loss | PASS |
| Pupil companion HTML scans | PASS |

| Stage | Book line |
|---|---|
| 1 |  |
| 2 | In your book: Glue in today's strip; date it. Answer 1 and 2 first. |
| 3 | In your book: Write one response to Rank for Aaliyah; use a clue. |
| 4 | In your book: Watch the four model steps. No writing yet. |
| 5 | In your book: Move or match each card; record your explanation and its evidence. |
| 6 | In your book: Write the letter of your answer and one reason. |
| 7 | In your book: Complete your route's task in your book; use its stem. |
| 8 | In your book: Read back one answer (?); improve it and mark //. |
| 9 | In your book: Answer both questions under today's work. |

TA opening static evidence: `[{"slide": 1, "title": "Personal values and respect for others", "count": 0, "lines": [], "pass": true, "words": 0}, {"slide": 2, "title": "Arrival", "count": 1, "lines": ["In your book: Glue in today's strip; date it. Answer 1 and 2 first."], "pass": true, "words": 11}, {"slide": 3, "title": "Start the enquiry", "count": 1, "lines": ["In your book: Write one response to Rank for Aaliyah; use a clue."], "pass": true, "words": 10}, {"slide": 4, "title": "I do · a worked method", "count": 1, "lines": ["In your book: Watch the four model steps. No writing yet."], "pass": true, "words": 8}, {"slide": 5, "title": "We do · choose and explain", "count": 1, "lines": ["In your book: Move or match each card; record your explanation and its evidence."], "pass": true, "words": 11}, {"slide": 6, "title": "Apply the learning", "count": 1, "lines": ["In your book: Write the letter of your answer and one reason."], "pass": true, "words": 9}, {"slide": 7, "title": "Independent application", "count": 1, "lines": ["In your book: Complete your route's task in your book; use its stem."], "pass": true, "words": 10}, {"slide": 8, "title": "Review and improve", "count": 1, "lines": ["In your book: Read back one answer (?); improve it and mark //."], "pass": true, "words": 10}, {"slide": 9, "title": "Exit ticket", "count": 1, "lines": ["In your book: Answer both questions under today's work."], "pass": true, "words": 6}]`

TA opening static evidence: `[{"slide": "slide-1", "chars": 287, "text": "Staff planning and targets Personal values and respect for others Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-2", "chars": 256, "text": "Staff planning and targets Arrival Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-3", "chars": 266, "text": "Staff planning and targets Start the enquiry Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-4", "chars": 271, "text": "Staff planning and targets I do · a worked method Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-5", "chars": 275, "text": "Staff planning and targets We do · choose and explain Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-6", "chars": 267, "text": "Staff planning and targets Apply the learning Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-7", "chars": 272, "text": "Staff planning and targets Independent application Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-8", "chars": 267, "text": "Staff planning and targets Review and improve Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-9", "chars": 260, "text": "Staff planning and targets Exit ticket Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}]`

TA opening counts (static proxy, not browser visibility): `[{"slide": "slide-1", "chars": 287, "text": "Staff planning and targets Personal values and respect for others Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-2", "chars": 256, "text": "Staff planning and targets Arrival Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-3", "chars": 266, "text": "Staff planning and targets Start the enquiry Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-4", "chars": 271, "text": "Staff planning and targets I do · a worked method Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-5", "chars": 275, "text": "Staff planning and targets We do · choose and explain Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-6", "chars": 267, "text": "Staff planning and targets Apply the learning Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-7", "chars": 272, "text": "Staff planning and targets Independent application Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-8", "chars": 267, "text": "Staff planning and targets Review and improve Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-9", "chars": 260, "text": "Staff planning and targets Exit ticket Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}]`

### GROW_RE_A2_W07

| Item | Result |
|---|---|
| Document shell | PASS |
| Duplicate IDs | PASS |
| F1 CSS exact bytes | PASS |
| F2 CSS exact bytes | PASS |
| CSS final order: fit then print | PASS |
| Nine teaching stages | PASS |
| Nine brandlines | PASS |
| Book lines: opening 0; all other stages 1 | PASS |
| F5 brandlines have no leading zero | PASS |
| Review includes // and ? | PASS |
| OL-2 one bare closed staff disclosure | PASS |
| OL-2 exact staff summary | PASS |
| F8 Planned adaptations | PASS |
| F8 Invite a response | PASS |
| F8 IEDP line exact | PASS |
| F8 five broad areas | PASS |
| F8 six invite routes | PASS |
| F6 preparation line | PASS |
| OL-2 answers-with-staff warning | PASS |
| OL-3 13 live teacher-card headings | PASS |
| E3 11 staff sections survive | PASS |
| OL-4 no staff file links in top bar | PASS |
| OL-4 top bar labels | PASS |
| OL-2 staff links outside disclosure | PASS |
| TA opening static counts recorded | PASS |
| OL-1 vary-exit retained | PASS |
| OL-1 adapter exact restored hash | PASS |
| OL-1 starter before exit builder | PASS |
| OL-11 arrival prompt exact live | PASS |
| OL-1 exit config unchanged | PASS |
| OL-12 arrival embedded picture equals week PNG | PASS |
| X3 no welcome guests claim | PASS |
| Visible internal-word scan | PASS |
| Banned wording scan | PASS |
| Pupil term-week scan excluding allowed headers | PASS |
| No served record filename references | PASS |
| F3 activity print cut heading | PASS |
| OL-9 ledger one H1 | PASS |
| RB-3 approved mark credit row | PASS |
| RB-3 D1 block byte-identical | PASS |
| OL-9 per-link access checks | PASS |
| OL-3 no unexplained live card sentence loss | PASS |
| Pupil companion HTML scans | PASS |

| Stage | Book line |
|---|---|
| 1 |  |
| 2 | In your book: Glue in today's strip; date it. Answer 1 and 2 first. |
| 3 | In your book: Write one response to Strongest evidence; use a clue. |
| 4 | In your book: Watch the four model steps. No writing yet. |
| 5 | In your book: Move or match each card; record your explanation and its evidence. |
| 6 | In your book: Write the letter of your answer and one reason. |
| 7 | In your book: Complete your route's task in your book; use its stem. |
| 8 | In your book: Read back one answer (?); improve it and mark //. |
| 9 | In your book: Answer both questions under today's work. |

TA opening static evidence: `[{"slide": 1, "title": "Belief and identity assessment", "count": 0, "lines": [], "pass": true, "words": 0}, {"slide": 2, "title": "Arrival", "count": 1, "lines": ["In your book: Glue in today's strip; date it. Answer 1 and 2 first."], "pass": true, "words": 11}, {"slide": 3, "title": "Start the enquiry", "count": 1, "lines": ["In your book: Write one response to Strongest evidence; use a clue."], "pass": true, "words": 9}, {"slide": 4, "title": "I do · a worked method", "count": 1, "lines": ["In your book: Watch the four model steps. No writing yet."], "pass": true, "words": 8}, {"slide": 5, "title": "We do · match and explain", "count": 1, "lines": ["In your book: Move or match each card; record your explanation and its evidence."], "pass": true, "words": 11}, {"slide": 6, "title": "Apply the learning", "count": 1, "lines": ["In your book: Write the letter of your answer and one reason."], "pass": true, "words": 9}, {"slide": 7, "title": "Independent application", "count": 1, "lines": ["In your book: Complete your route's task in your book; use its stem."], "pass": true, "words": 10}, {"slide": 8, "title": "Review and improve", "count": 1, "lines": ["In your book: Read back one answer (?); improve it and mark //."], "pass": true, "words": 10}, {"slide": 9, "title": "Exit ticket", "count": 1, "lines": ["In your book: Answer both questions under today's work."], "pass": true, "words": 6}]`

TA opening static evidence: `[{"slide": "slide-1", "chars": 335, "text": "Staff planning and targets Belief and identity assessment Use a different example for shared practice. During independent assessment, keep the agreed reader, scribe, glossary or response mode, but withdraw answer models and record prompts separately. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-2", "chars": 312, "text": "Staff planning and targets Arrival Use a different example for shared practice. During independent assessment, keep the agreed reader, scribe, glossary or response mode, but withdraw answer models and record prompts separately. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-3", "chars": 322, "text": "Staff planning and targets Start the enquiry Use a different example for shared practice. During independent assessment, keep the agreed reader, scribe, glossary or response mode, but withdraw answer models and record prompts separately. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-4", "chars": 327, "text": "Staff planning and targets I do · a worked method Use a different example for shared practice. During independent assessment, keep the agreed reader, scribe, glossary or response mode, but withdraw answer models and record prompts separately. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-5", "chars": 330, "text": "Staff planning and targets We do · match and explain Use a different example for shared practice. During independent assessment, keep the agreed reader, scribe, glossary or response mode, but withdraw answer models and record prompts separately. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-6", "chars": 323, "text": "Staff planning and targets Apply the learning Use a different example for shared practice. During independent assessment, keep the agreed reader, scribe, glossary or response mode, but withdraw answer models and record prompts separately. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-7", "chars": 328, "text": "Staff planning and targets Independent application Use a different example for shared practice. During independent assessment, keep the agreed reader, scribe, glossary or response mode, but withdraw answer models and record prompts separately. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-8", "chars": 323, "text": "Staff planning and targets Review and improve Use a different example for shared practice. During independent assessment, keep the agreed reader, scribe, glossary or response mode, but withdraw answer models and record prompts separately. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-9", "chars": 316, "text": "Staff planning and targets Exit ticket Use a different example for shared practice. During independent assessment, keep the agreed reader, scribe, glossary or response mode, but withdraw answer models and record prompts separately. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}]`

TA opening counts (static proxy, not browser visibility): `[{"slide": "slide-1", "chars": 335, "text": "Staff planning and targets Belief and identity assessment Use a different example for shared practice. During independent assessment, keep the agreed reader, scribe, glossary or response mode, but withdraw answer models and record prompts separately. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-2", "chars": 312, "text": "Staff planning and targets Arrival Use a different example for shared practice. During independent assessment, keep the agreed reader, scribe, glossary or response mode, but withdraw answer models and record prompts separately. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-3", "chars": 322, "text": "Staff planning and targets Start the enquiry Use a different example for shared practice. During independent assessment, keep the agreed reader, scribe, glossary or response mode, but withdraw answer models and record prompts separately. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-4", "chars": 327, "text": "Staff planning and targets I do · a worked method Use a different example for shared practice. During independent assessment, keep the agreed reader, scribe, glossary or response mode, but withdraw answer models and record prompts separately. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-5", "chars": 330, "text": "Staff planning and targets We do · match and explain Use a different example for shared practice. During independent assessment, keep the agreed reader, scribe, glossary or response mode, but withdraw answer models and record prompts separately. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-6", "chars": 323, "text": "Staff planning and targets Apply the learning Use a different example for shared practice. During independent assessment, keep the agreed reader, scribe, glossary or response mode, but withdraw answer models and record prompts separately. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-7", "chars": 328, "text": "Staff planning and targets Independent application Use a different example for shared practice. During independent assessment, keep the agreed reader, scribe, glossary or response mode, but withdraw answer models and record prompts separately. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-8", "chars": 323, "text": "Staff planning and targets Review and improve Use a different example for shared practice. During independent assessment, keep the agreed reader, scribe, glossary or response mode, but withdraw answer models and record prompts separately. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-9", "chars": 316, "text": "Staff planning and targets Exit ticket Use a different example for shared practice. During independent assessment, keep the agreed reader, scribe, glossary or response mode, but withdraw answer models and record prompts separately. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}]`

### LAUNCH_RE_A1_W08

| Item | Result |
|---|---|
| Document shell | PASS |
| Duplicate IDs | PASS |
| F1 CSS exact bytes | PASS |
| F2 CSS exact bytes | PASS |
| CSS final order: fit then print | PASS |
| Nine teaching stages | PASS |
| Nine brandlines | PASS |
| Book lines: opening 0; all other stages 1 | PASS |
| F5 brandlines have no leading zero | PASS |
| Review includes // and ? | PASS |
| OL-2 one bare closed staff disclosure | PASS |
| OL-2 exact staff summary | PASS |
| F8 Planned adaptations | PASS |
| F8 Invite a response | PASS |
| F8 IEDP line exact | PASS |
| F8 five broad areas | PASS |
| F8 six invite routes | PASS |
| F6 preparation line | PASS |
| OL-2 answers-with-staff warning | PASS |
| OL-4 no staff file links in top bar | PASS |
| OL-4 top bar labels | PASS |
| OL-2 staff links outside disclosure | PASS |
| TA opening static counts recorded | PASS |
| Visible internal-word scan | PASS |
| Banned wording scan | PASS |
| Pupil term-week scan excluding allowed headers | PASS |
| No served record filename references | PASS |
| F3 activity print cut heading | PASS |
| OL-9 ledger one H1 | PASS |
| Pupil companion HTML scans | PASS |
| First lesson back staff card | PASS |
| Return private RAG | PASS |
| Return once-only line | PASS |
| Return no dated staff card | PASS |

| Stage | Book line |
|---|---|
| 1 |  |
| 2 | In your book: Glue in today’s strip; date it. Answer questions 1 to 4. |
| 3 | In your book: Number 1 to 3. Write one precise answer for each. |
| 4 | In your book: Watch how relevant evidence supports a point. No writing yet. |
| 5 | In your book: Match evidence to an influence; explain one link. |
| 6 | In your book: Write the letter of your answer. Explain one clue. |
| 7 | In your book: Answer 1 to 5 briefly; use point, evidence and explanation for 6. |
| 8 | In your book: Read back one answer (?); improve it and mark //. |
| 9 | In your book: Explain one belief-to-choice link using relevant evidence. |

TA opening static evidence: `[{"slide": 1, "title": "Evidence, belief and choices", "count": 0, "lines": [], "pass": true, "words": 0}, {"slide": 2, "title": "Arrival task", "count": 1, "lines": ["In your book: Glue in today’s strip; date it. Answer questions 1 to 4."], "pass": true, "words": 11}, {"slide": 3, "title": "Start the enquiry", "count": 1, "lines": ["In your book: Number 1 to 3. Write one precise answer for each."], "pass": true, "words": 10}, {"slide": 4, "title": "I do · a worked method", "count": 1, "lines": ["In your book: Watch how relevant evidence supports a point. No writing yet."], "pass": true, "words": 10}, {"slide": 5, "title": "We do · match the evidence", "count": 1, "lines": ["In your book: Match evidence to an influence; explain one link."], "pass": true, "words": 8}, {"slide": 6, "title": "Check the idea", "count": 1, "lines": ["In your book: Write the letter of your answer. Explain one clue."], "pass": true, "words": 9}, {"slide": 7, "title": "Short individual book check", "count": 1, "lines": ["In your book: Answer 1 to 5 briefly; use point, evidence and explanation for 6."], "pass": true, "words": 12}, {"slide": 8, "title": "Review and improve", "count": 1, "lines": ["In your book: Read back one answer (?); improve it and mark //."], "pass": true, "words": 10}, {"slide": 9, "title": "Exit ticket", "count": 1, "lines": ["In your book: Explain one belief-to-choice link using relevant evidence."], "pass": true, "words": 7}]`

TA opening static evidence: `[{"slide": "slide-1", "chars": 403, "text": "Staff planning and targets Evidence, belief and choices Welcome pupils with the same learning goal and normal access arrangements. Introduce the short private check only after teaching the key idea. Begin from what each pupil shows; use fictional sources and accept a quiet response. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Print First lesson back staff card Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-2", "chars": 382, "text": "Staff planning and targets Arrival task Read one arrival prompt at a time. Offer the word bank, a reader, pointing or an exact scribe without choosing an answer. Collect each pupil’s own response before revealing; use what you see to choose the starting support. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Print First lesson back staff card Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-3", "chars": 380, "text": "Staff planning and targets Start the enquiry Give quiet thinking time for the three retrieval prompts. Invite a response by voice, pointing or showing the book. Record a useful misconception privately; use one source clue and hear the pupil’s own answer again. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Print First lesson back staff card Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-4", "chars": 387, "text": "Staff planning and targets I do · a worked method Use the manual model steps at a calm pace. Point to the question and then the relevant source detail. Rehearse the reason once; no writing is needed while pupils watch. Pause for processing before inviting a response. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Print First lesson back staff card Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-5", "chars": 388, "text": "Staff planning and targets We do · match the evidence Offer the shared cards for pupils to move or match. One person suggests and the other checks the evidence; swap after one turn. Hear an individual reason, then reduce the prompt so the pupil can try the link again. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Print First lesson back staff card Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-6", "chars": 373, "text": "Staff planning and targets Check the idea Collect every pupil’s answer letter and a source clue before revealing. Use the wrong option’s diagnosis to choose one teaching move. Do not treat silence or an access need as a misconception; recheck privately. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Print First lesson back staff card Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-7", "chars": 394, "text": "Staff planning and targets Short individual book check Keep this short check individual and low stakes. One adult supports agreed access while the other holds the group. Read or scribe exact words without choosing answers. Record the pupil’s response and support separately. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Print First lesson back staff card Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-8", "chars": 382, "text": "Staff planning and targets Review and improve Ask pupils to read one answer back using ?. Give one precise next step, allow a // edit and check the changed detail. Keep feedback private and record the pupil’s response; rejoin the route at one clearly named step. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Print First lesson back staff card Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-9", "chars": 385, "text": "Staff planning and targets Exit ticket Receive the exit response privately by book, voice, pointing or the agreed mode. Look for the key idea and a relevant source detail. Record the private RAG and access support, then pass one useful next step to the next lesson. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Print First lesson back staff card Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}]`

TA opening counts (static proxy, not browser visibility): `[{"slide": "slide-1", "chars": 403, "text": "Staff planning and targets Evidence, belief and choices Welcome pupils with the same learning goal and normal access arrangements. Introduce the short private check only after teaching the key idea. Begin from what each pupil shows; use fictional sources and accept a quiet response. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Print First lesson back staff card Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-2", "chars": 382, "text": "Staff planning and targets Arrival task Read one arrival prompt at a time. Offer the word bank, a reader, pointing or an exact scribe without choosing an answer. Collect each pupil’s own response before revealing; use what you see to choose the starting support. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Print First lesson back staff card Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-3", "chars": 380, "text": "Staff planning and targets Start the enquiry Give quiet thinking time for the three retrieval prompts. Invite a response by voice, pointing or showing the book. Record a useful misconception privately; use one source clue and hear the pupil’s own answer again. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Print First lesson back staff card Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-4", "chars": 387, "text": "Staff planning and targets I do · a worked method Use the manual model steps at a calm pace. Point to the question and then the relevant source detail. Rehearse the reason once; no writing is needed while pupils watch. Pause for processing before inviting a response. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Print First lesson back staff card Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-5", "chars": 388, "text": "Staff planning and targets We do · match the evidence Offer the shared cards for pupils to move or match. One person suggests and the other checks the evidence; swap after one turn. Hear an individual reason, then reduce the prompt so the pupil can try the link again. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Print First lesson back staff card Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-6", "chars": 373, "text": "Staff planning and targets Check the idea Collect every pupil’s answer letter and a source clue before revealing. Use the wrong option’s diagnosis to choose one teaching move. Do not treat silence or an access need as a misconception; recheck privately. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Print First lesson back staff card Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-7", "chars": 394, "text": "Staff planning and targets Short individual book check Keep this short check individual and low stakes. One adult supports agreed access while the other holds the group. Read or scribe exact words without choosing answers. Record the pupil’s response and support separately. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Print First lesson back staff card Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-8", "chars": 382, "text": "Staff planning and targets Review and improve Ask pupils to read one answer back using ?. Give one precise next step, allow a // edit and check the changed detail. Keep feedback private and record the pupil’s response; rejoin the route at one clearly named step. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Print First lesson back staff card Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-9", "chars": 385, "text": "Staff planning and targets Exit ticket Receive the exit response privately by book, voice, pointing or the agreed mode. Look for the key idea and a relevant source detail. Record the private RAG and access support, then pass one useful next step to the next lesson. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Print First lesson back staff card Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}]`

### LAUNCH_RE_A2_W01

| Item | Result |
|---|---|
| Document shell | PASS |
| Duplicate IDs | PASS |
| F1 CSS exact bytes | PASS |
| F2 CSS exact bytes | PASS |
| CSS final order: fit then print | PASS |
| Nine teaching stages | PASS |
| Nine brandlines | PASS |
| Book lines: opening 0; all other stages 1 | PASS |
| F5 brandlines have no leading zero | PASS |
| Review includes // and ? | PASS |
| OL-2 one bare closed staff disclosure | PASS |
| OL-2 exact staff summary | PASS |
| F8 Planned adaptations | PASS |
| F8 Invite a response | PASS |
| F8 IEDP line exact | PASS |
| F8 five broad areas | PASS |
| F8 six invite routes | PASS |
| F6 preparation line | PASS |
| OL-2 answers-with-staff warning | PASS |
| OL-3 13 live teacher-card headings | PASS |
| E3 11 staff sections survive | PASS |
| OL-4 no staff file links in top bar | PASS |
| OL-4 top bar labels | PASS |
| OL-2 staff links outside disclosure | PASS |
| TA opening static counts recorded | PASS |
| OL-1 vary-exit retained | PASS |
| OL-1 adapter exact restored hash | PASS |
| OL-1 starter before exit builder | PASS |
| OL-11 arrival prompt exact live | PASS |
| OL-1 exit config unchanged | PASS |
| OL-12 arrival embedded picture equals week PNG | PASS |
| X3 no welcome guests claim | PASS |
| Visible internal-word scan | PASS |
| Banned wording scan | PASS |
| Pupil term-week scan excluding allowed headers | PASS |
| No served record filename references | PASS |
| F3 activity print cut heading | PASS |
| OL-9 ledger one H1 | PASS |
| RB-3 approved mark credit row | PASS |
| RB-3 D1 block byte-identical | PASS |
| OL-9 per-link access checks | PASS |
| OL-3 no unexplained live card sentence loss | PASS |
| Pupil companion HTML scans | PASS |

| Stage | Book line |
|---|---|
| 1 |  |
| 2 | In your book: Glue in today's strip; date it. Answer 1 and 2 first. |
| 3 | In your book: Write one response to Worship, prayer or reflection?; use a clue. |
| 4 | In your book: Watch the four model steps. No writing yet. |
| 5 | In your book: Move or match each card; record your explanation and its evidence. |
| 6 | In your book: Write the letter of your answer and one reason. |
| 7 | In your book: Complete your route's task in your book; use its stem. |
| 8 | In your book: Read back one answer (?); improve it and mark //. |
| 9 | In your book: Answer both questions under today's work. |

TA opening static evidence: `[{"slide": 1, "title": "Worship, prayer and practice", "count": 0, "lines": [], "pass": true, "words": 0}, {"slide": 2, "title": "Arrival", "count": 1, "lines": ["In your book: Glue in today's strip; date it. Answer 1 and 2 first."], "pass": true, "words": 11}, {"slide": 3, "title": "Start the enquiry", "count": 1, "lines": ["In your book: Write one response to Worship, prayer or reflection?; use a clue."], "pass": true, "words": 11}, {"slide": 4, "title": "I do · a worked method", "count": 1, "lines": ["In your book: Watch the four model steps. No writing yet."], "pass": true, "words": 8}, {"slide": 5, "title": "We do · match and explain", "count": 1, "lines": ["In your book: Move or match each card; record your explanation and its evidence."], "pass": true, "words": 11}, {"slide": 6, "title": "Apply the learning", "count": 1, "lines": ["In your book: Write the letter of your answer and one reason."], "pass": true, "words": 9}, {"slide": 7, "title": "Independent application", "count": 1, "lines": ["In your book: Complete your route's task in your book; use its stem."], "pass": true, "words": 10}, {"slide": 8, "title": "Review and improve", "count": 1, "lines": ["In your book: Read back one answer (?); improve it and mark //."], "pass": true, "words": 10}, {"slide": 9, "title": "Exit ticket", "count": 1, "lines": ["In your book: Answer both questions under today's work."], "pass": true, "words": 6}]`

TA opening static evidence: `[{"slide": "slide-1", "chars": 277, "text": "Staff planning and targets Worship, prayer and practice Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-2", "chars": 256, "text": "Staff planning and targets Arrival Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-3", "chars": 266, "text": "Staff planning and targets Start the enquiry Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-4", "chars": 271, "text": "Staff planning and targets I do · a worked method Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-5", "chars": 274, "text": "Staff planning and targets We do · match and explain Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-6", "chars": 267, "text": "Staff planning and targets Apply the learning Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-7", "chars": 272, "text": "Staff planning and targets Independent application Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-8", "chars": 267, "text": "Staff planning and targets Review and improve Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-9", "chars": 260, "text": "Staff planning and targets Exit ticket Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}]`

TA opening counts (static proxy, not browser visibility): `[{"slide": "slide-1", "chars": 277, "text": "Staff planning and targets Worship, prayer and practice Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-2", "chars": 256, "text": "Staff planning and targets Arrival Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-3", "chars": 266, "text": "Staff planning and targets Start the enquiry Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-4", "chars": 271, "text": "Staff planning and targets I do · a worked method Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-5", "chars": 274, "text": "Staff planning and targets We do · match and explain Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-6", "chars": 267, "text": "Staff planning and targets Apply the learning Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-7", "chars": 272, "text": "Staff planning and targets Independent application Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-8", "chars": 267, "text": "Staff planning and targets Review and improve Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-9", "chars": 260, "text": "Staff planning and targets Exit ticket Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}]`

### LAUNCH_RE_A2_W02

| Item | Result |
|---|---|
| Document shell | PASS |
| Duplicate IDs | PASS |
| F1 CSS exact bytes | PASS |
| F2 CSS exact bytes | PASS |
| CSS final order: fit then print | PASS |
| Nine teaching stages | PASS |
| Nine brandlines | PASS |
| Book lines: opening 0; all other stages 1 | PASS |
| F5 brandlines have no leading zero | PASS |
| Review includes // and ? | PASS |
| OL-2 one bare closed staff disclosure | PASS |
| OL-2 exact staff summary | PASS |
| F8 Planned adaptations | PASS |
| F8 Invite a response | PASS |
| F8 IEDP line exact | PASS |
| F8 five broad areas | PASS |
| F8 six invite routes | PASS |
| F6 preparation line | PASS |
| OL-2 answers-with-staff warning | PASS |
| OL-3 13 live teacher-card headings | PASS |
| E3 11 staff sections survive | PASS |
| OL-4 no staff file links in top bar | PASS |
| OL-4 top bar labels | PASS |
| OL-2 staff links outside disclosure | PASS |
| TA opening static counts recorded | PASS |
| OL-1 vary-exit retained | PASS |
| OL-1 adapter exact restored hash | PASS |
| OL-1 starter before exit builder | PASS |
| OL-11 arrival prompt exact live | PASS |
| OL-1 exit config unchanged | PASS |
| OL-12 arrival embedded picture equals week PNG | PASS |
| X3 no welcome guests claim | PASS |
| Visible internal-word scan | PASS |
| Banned wording scan | PASS |
| Pupil term-week scan excluding allowed headers | PASS |
| No served record filename references | PASS |
| F3 activity print cut heading | PASS |
| OL-9 ledger one H1 | PASS |
| RB-3 approved mark credit row | PASS |
| RB-3 D1 block byte-identical | PASS |
| OL-9 per-link access checks | PASS |
| OL-3 no unexplained live card sentence loss | PASS |
| Pupil companion HTML scans | PASS |

| Stage | Book line |
|---|---|
| 1 |  |
| 2 | In your book: Glue in today's strip; date it. Answer 1 and 2 first. |
| 3 | In your book: Write one response to A fictional person’s memory; use a clue. |
| 4 | In your book: Watch the four model steps. No writing yet. |
| 5 | In your book: Move or match each card; record your explanation and its evidence. |
| 6 | In your book: Write the letter of your answer and one reason. |
| 7 | In your book: Complete your route's task in your book; use its stem. |
| 8 | In your book: Read back one answer (?); improve it and mark //. |
| 9 | In your book: Answer both questions under today's work. |

TA opening static evidence: `[{"slide": 1, "title": "Pilgrimage and sacred places", "count": 0, "lines": [], "pass": true, "words": 0}, {"slide": 2, "title": "Arrival", "count": 1, "lines": ["In your book: Glue in today's strip; date it. Answer 1 and 2 first."], "pass": true, "words": 11}, {"slide": 3, "title": "Start the enquiry", "count": 1, "lines": ["In your book: Write one response to A fictional person’s memory; use a clue."], "pass": true, "words": 11}, {"slide": 4, "title": "I do · a worked method", "count": 1, "lines": ["In your book: Watch the four model steps. No writing yet."], "pass": true, "words": 8}, {"slide": 5, "title": "We do · source detective", "count": 1, "lines": ["In your book: Move or match each card; record your explanation and its evidence."], "pass": true, "words": 11}, {"slide": 6, "title": "Apply the learning", "count": 1, "lines": ["In your book: Write the letter of your answer and one reason."], "pass": true, "words": 9}, {"slide": 7, "title": "Independent application", "count": 1, "lines": ["In your book: Complete your route's task in your book; use its stem."], "pass": true, "words": 10}, {"slide": 8, "title": "Review and improve", "count": 1, "lines": ["In your book: Read back one answer (?); improve it and mark //."], "pass": true, "words": 10}, {"slide": 9, "title": "Exit ticket", "count": 1, "lines": ["In your book: Answer both questions under today's work."], "pass": true, "words": 6}]`

TA opening static evidence: `[{"slide": "slide-1", "chars": 277, "text": "Staff planning and targets Pilgrimage and sacred places Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-2", "chars": 256, "text": "Staff planning and targets Arrival Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-3", "chars": 266, "text": "Staff planning and targets Start the enquiry Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-4", "chars": 271, "text": "Staff planning and targets I do · a worked method Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-5", "chars": 273, "text": "Staff planning and targets We do · source detective Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-6", "chars": 267, "text": "Staff planning and targets Apply the learning Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-7", "chars": 272, "text": "Staff planning and targets Independent application Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-8", "chars": 267, "text": "Staff planning and targets Review and improve Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-9", "chars": 260, "text": "Staff planning and targets Exit ticket Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}]`

TA opening counts (static proxy, not browser visibility): `[{"slide": "slide-1", "chars": 277, "text": "Staff planning and targets Pilgrimage and sacred places Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-2", "chars": 256, "text": "Staff planning and targets Arrival Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-3", "chars": 266, "text": "Staff planning and targets Start the enquiry Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-4", "chars": 271, "text": "Staff planning and targets I do · a worked method Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-5", "chars": 273, "text": "Staff planning and targets We do · source detective Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-6", "chars": 267, "text": "Staff planning and targets Apply the learning Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-7", "chars": 272, "text": "Staff planning and targets Independent application Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-8", "chars": 267, "text": "Staff planning and targets Review and improve Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-9", "chars": 260, "text": "Staff planning and targets Exit ticket Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}]`

### LAUNCH_RE_A2_W03

| Item | Result |
|---|---|
| Document shell | PASS |
| Duplicate IDs | PASS |
| F1 CSS exact bytes | PASS |
| F2 CSS exact bytes | PASS |
| CSS final order: fit then print | PASS |
| Nine teaching stages | PASS |
| Nine brandlines | PASS |
| Book lines: opening 0; all other stages 1 | PASS |
| F5 brandlines have no leading zero | PASS |
| Review includes // and ? | PASS |
| OL-2 one bare closed staff disclosure | PASS |
| OL-2 exact staff summary | PASS |
| F8 Planned adaptations | PASS |
| F8 Invite a response | PASS |
| F8 IEDP line exact | PASS |
| F8 five broad areas | PASS |
| F8 six invite routes | PASS |
| F6 preparation line | PASS |
| OL-2 answers-with-staff warning | PASS |
| OL-3 13 live teacher-card headings | PASS |
| E3 11 staff sections survive | PASS |
| OL-4 no staff file links in top bar | PASS |
| OL-4 top bar labels | PASS |
| OL-2 staff links outside disclosure | PASS |
| TA opening static counts recorded | PASS |
| OL-1 vary-exit retained | PASS |
| OL-1 adapter exact restored hash | PASS |
| OL-1 starter before exit builder | PASS |
| OL-11 arrival prompt exact live | PASS |
| OL-1 exit config unchanged | PASS |
| OL-12 arrival embedded picture equals week PNG | PASS |
| X3 no welcome guests claim | PASS |
| Visible internal-word scan | PASS |
| Banned wording scan | PASS |
| Pupil term-week scan excluding allowed headers | PASS |
| No served record filename references | PASS |
| F3 activity print cut heading | PASS |
| OL-9 ledger one H1 | PASS |
| RB-3 approved mark credit row | PASS |
| RB-3 D1 block byte-identical | PASS |
| OL-9 per-link access checks | PASS |
| OL-3 no unexplained live card sentence loss | PASS |
| Pupil companion HTML scans | PASS |

| Stage | Book line |
|---|---|
| 1 |  |
| 2 | In your book: Glue in today's strip; date it. Answer 1 and 2 first. |
| 3 | In your book: Write one response to Order the life events; use a clue. |
| 4 | In your book: Watch the four model steps. No writing yet. |
| 5 | In your book: Move or match each card; record your explanation and its evidence. |
| 6 | In your book: Write the letter of your answer and one reason. |
| 7 | In your book: Complete your route's task in your book; use its stem. |
| 8 | In your book: Read back one answer (?); improve it and mark //. |
| 9 | In your book: Answer both questions under today's work. |

TA opening static evidence: `[{"slide": 1, "title": "Rites of passage and community", "count": 0, "lines": [], "pass": true, "words": 0}, {"slide": 2, "title": "Arrival", "count": 1, "lines": ["In your book: Glue in today's strip; date it. Answer 1 and 2 first."], "pass": true, "words": 11}, {"slide": 3, "title": "Start the enquiry", "count": 1, "lines": ["In your book: Write one response to Order the life events; use a clue."], "pass": true, "words": 11}, {"slide": 4, "title": "I do · a worked method", "count": 1, "lines": ["In your book: Watch the four model steps. No writing yet."], "pass": true, "words": 8}, {"slide": 5, "title": "We do · sort and justify", "count": 1, "lines": ["In your book: Move or match each card; record your explanation and its evidence."], "pass": true, "words": 11}, {"slide": 6, "title": "Apply the learning", "count": 1, "lines": ["In your book: Write the letter of your answer and one reason."], "pass": true, "words": 9}, {"slide": 7, "title": "Independent application", "count": 1, "lines": ["In your book: Complete your route's task in your book; use its stem."], "pass": true, "words": 10}, {"slide": 8, "title": "Review and improve", "count": 1, "lines": ["In your book: Read back one answer (?); improve it and mark //."], "pass": true, "words": 10}, {"slide": 9, "title": "Exit ticket", "count": 1, "lines": ["In your book: Answer both questions under today's work."], "pass": true, "words": 6}]`

TA opening static evidence: `[{"slide": "slide-1", "chars": 279, "text": "Staff planning and targets Rites of passage and community Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-2", "chars": 256, "text": "Staff planning and targets Arrival Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-3", "chars": 266, "text": "Staff planning and targets Start the enquiry Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-4", "chars": 271, "text": "Staff planning and targets I do · a worked method Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-5", "chars": 273, "text": "Staff planning and targets We do · sort and justify Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-6", "chars": 267, "text": "Staff planning and targets Apply the learning Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-7", "chars": 272, "text": "Staff planning and targets Independent application Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-8", "chars": 267, "text": "Staff planning and targets Review and improve Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-9", "chars": 260, "text": "Staff planning and targets Exit ticket Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}]`

TA opening counts (static proxy, not browser visibility): `[{"slide": "slide-1", "chars": 279, "text": "Staff planning and targets Rites of passage and community Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-2", "chars": 256, "text": "Staff planning and targets Arrival Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-3", "chars": 266, "text": "Staff planning and targets Start the enquiry Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-4", "chars": 271, "text": "Staff planning and targets I do · a worked method Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-5", "chars": 273, "text": "Staff planning and targets We do · sort and justify Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-6", "chars": 267, "text": "Staff planning and targets Apply the learning Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-7", "chars": 272, "text": "Staff planning and targets Independent application Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-8", "chars": 267, "text": "Staff planning and targets Review and improve Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-9", "chars": 260, "text": "Staff planning and targets Exit ticket Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}]`

### LAUNCH_RE_A2_W04

| Item | Result |
|---|---|
| Document shell | PASS |
| Duplicate IDs | PASS |
| F1 CSS exact bytes | PASS |
| F2 CSS exact bytes | PASS |
| CSS final order: fit then print | PASS |
| Nine teaching stages | PASS |
| Nine brandlines | PASS |
| Book lines: opening 0; all other stages 1 | PASS |
| F5 brandlines have no leading zero | PASS |
| Review includes // and ? | PASS |
| OL-2 one bare closed staff disclosure | PASS |
| OL-2 exact staff summary | PASS |
| F8 Planned adaptations | PASS |
| F8 Invite a response | PASS |
| F8 IEDP line exact | PASS |
| F8 five broad areas | PASS |
| F8 six invite routes | PASS |
| F6 preparation line | PASS |
| OL-2 answers-with-staff warning | PASS |
| OL-3 13 live teacher-card headings | PASS |
| E3 11 staff sections survive | PASS |
| OL-4 no staff file links in top bar | PASS |
| OL-4 top bar labels | PASS |
| OL-2 staff links outside disclosure | PASS |
| TA opening static counts recorded | PASS |
| OL-1 vary-exit retained | PASS |
| OL-1 adapter exact restored hash | PASS |
| OL-1 starter before exit builder | PASS |
| OL-11 arrival prompt exact live | PASS |
| OL-1 exit config unchanged | PASS |
| OL-12 arrival embedded picture equals week PNG | PASS |
| X3 no welcome guests claim | PASS |
| Visible internal-word scan | PASS |
| Banned wording scan | PASS |
| Pupil term-week scan excluding allowed headers | PASS |
| No served record filename references | PASS |
| F3 activity print cut heading | PASS |
| OL-9 ledger one H1 | PASS |
| RB-3 approved mark credit row | PASS |
| RB-3 D1 block byte-identical | PASS |
| OL-9 per-link access checks | PASS |
| OL-3 no unexplained live card sentence loss | PASS |
| Pupil companion HTML scans | PASS |

| Stage | Book line |
|---|---|
| 1 |  |
| 2 | In your book: Glue in today's strip; date it. Answer 1 and 2 first. |
| 3 | In your book: Write one response to A fictional pupil’s dilemma; use a clue. |
| 4 | In your book: Watch the four model steps. No writing yet. |
| 5 | In your book: Move or match each card; record your explanation and its evidence. |
| 6 | In your book: Write the letter of your answer and one reason. |
| 7 | In your book: Complete your route's task in your book; use its stem. |
| 8 | In your book: Read back one answer (?); improve it and mark //. |
| 9 | In your book: Answer both questions under today's work. |

TA opening static evidence: `[{"slide": 1, "title": "Moral teachings across worldviews", "count": 0, "lines": [], "pass": true, "words": 0}, {"slide": 2, "title": "Arrival", "count": 1, "lines": ["In your book: Glue in today's strip; date it. Answer 1 and 2 first."], "pass": true, "words": 11}, {"slide": 3, "title": "Start the enquiry", "count": 1, "lines": ["In your book: Write one response to A fictional pupil’s dilemma; use a clue."], "pass": true, "words": 11}, {"slide": 4, "title": "I do · a worked method", "count": 1, "lines": ["In your book: Watch the four model steps. No writing yet."], "pass": true, "words": 8}, {"slide": 5, "title": "We do · choose and explain", "count": 1, "lines": ["In your book: Move or match each card; record your explanation and its evidence."], "pass": true, "words": 11}, {"slide": 6, "title": "Apply the learning", "count": 1, "lines": ["In your book: Write the letter of your answer and one reason."], "pass": true, "words": 9}, {"slide": 7, "title": "Independent application", "count": 1, "lines": ["In your book: Complete your route's task in your book; use its stem."], "pass": true, "words": 10}, {"slide": 8, "title": "Review and improve", "count": 1, "lines": ["In your book: Read back one answer (?); improve it and mark //."], "pass": true, "words": 10}, {"slide": 9, "title": "Exit ticket", "count": 1, "lines": ["In your book: Answer both questions under today's work."], "pass": true, "words": 6}]`

TA opening static evidence: `[{"slide": "slide-1", "chars": 282, "text": "Staff planning and targets Moral teachings across worldviews Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-2", "chars": 256, "text": "Staff planning and targets Arrival Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-3", "chars": 266, "text": "Staff planning and targets Start the enquiry Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-4", "chars": 271, "text": "Staff planning and targets I do · a worked method Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-5", "chars": 275, "text": "Staff planning and targets We do · choose and explain Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-6", "chars": 267, "text": "Staff planning and targets Apply the learning Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-7", "chars": 272, "text": "Staff planning and targets Independent application Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-8", "chars": 267, "text": "Staff planning and targets Review and improve Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-9", "chars": 260, "text": "Staff planning and targets Exit ticket Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}]`

TA opening counts (static proxy, not browser visibility): `[{"slide": "slide-1", "chars": 282, "text": "Staff planning and targets Moral teachings across worldviews Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-2", "chars": 256, "text": "Staff planning and targets Arrival Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-3", "chars": 266, "text": "Staff planning and targets Start the enquiry Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-4", "chars": 271, "text": "Staff planning and targets I do · a worked method Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-5", "chars": 275, "text": "Staff planning and targets We do · choose and explain Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-6", "chars": 267, "text": "Staff planning and targets Apply the learning Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-7", "chars": 272, "text": "Staff planning and targets Independent application Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-8", "chars": 267, "text": "Staff planning and targets Review and improve Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-9", "chars": 260, "text": "Staff planning and targets Exit ticket Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}]`

### LAUNCH_RE_A2_W05

| Item | Result |
|---|---|
| Document shell | PASS |
| Duplicate IDs | PASS |
| F1 CSS exact bytes | PASS |
| F2 CSS exact bytes | PASS |
| CSS final order: fit then print | PASS |
| Nine teaching stages | PASS |
| Nine brandlines | PASS |
| Book lines: opening 0; all other stages 1 | PASS |
| F5 brandlines have no leading zero | PASS |
| Review includes // and ? | PASS |
| OL-2 one bare closed staff disclosure | PASS |
| OL-2 exact staff summary | PASS |
| F8 Planned adaptations | PASS |
| F8 Invite a response | PASS |
| F8 IEDP line exact | PASS |
| F8 five broad areas | PASS |
| F8 six invite routes | PASS |
| F6 preparation line | PASS |
| OL-2 answers-with-staff warning | PASS |
| OL-3 13 live teacher-card headings | PASS |
| E3 11 staff sections survive | PASS |
| OL-4 no staff file links in top bar | PASS |
| OL-4 top bar labels | PASS |
| OL-2 staff links outside disclosure | PASS |
| TA opening static counts recorded | PASS |
| OL-1 vary-exit retained | PASS |
| OL-1 adapter exact restored hash | PASS |
| OL-1 starter before exit builder | PASS |
| OL-11 arrival prompt exact live | PASS |
| OL-1 exit config unchanged | PASS |
| OL-12 arrival embedded picture equals week PNG | PASS |
| X3 no welcome guests claim | PASS |
| Visible internal-word scan | PASS |
| Banned wording scan | PASS |
| Pupil term-week scan excluding allowed headers | PASS |
| No served record filename references | PASS |
| F3 activity print cut heading | PASS |
| OL-9 ledger one H1 | PASS |
| RB-3 approved mark credit row | PASS |
| RB-3 D1 block byte-identical | PASS |
| OL-9 per-link access checks | PASS |
| OL-3 no unexplained live card sentence loss | PASS |
| Pupil companion HTML scans | PASS |

| Stage | Book line |
|---|---|
| 1 |  |
| 2 | In your book: Glue in today's strip; date it. Answer 1 and 2 first. |
| 3 | In your book: Write one response to Choose a big question; use a clue. |
| 4 | In your book: Watch the four model steps. No writing yet. |
| 5 | In your book: Move or match each card; record your explanation and its evidence. |
| 6 | In your book: Write the letter of your answer and one reason. |
| 7 | In your book: Complete your route's task in your book; use its stem. |
| 8 | In your book: Read back one answer (?); improve it and mark //. |
| 9 | In your book: Answer both questions under today's work. |

TA opening static evidence: `[{"slide": 1, "title": "Comparing responses to a life question", "count": 0, "lines": [], "pass": true, "words": 0}, {"slide": 2, "title": "Arrival", "count": 1, "lines": ["In your book: Glue in today's strip; date it. Answer 1 and 2 first."], "pass": true, "words": 11}, {"slide": 3, "title": "Start the enquiry", "count": 1, "lines": ["In your book: Write one response to Choose a big question; use a clue."], "pass": true, "words": 11}, {"slide": 4, "title": "I do · a worked method", "count": 1, "lines": ["In your book: Watch the four model steps. No writing yet."], "pass": true, "words": 8}, {"slide": 5, "title": "We do · sort and justify", "count": 1, "lines": ["In your book: Move or match each card; record your explanation and its evidence."], "pass": true, "words": 11}, {"slide": 6, "title": "Apply the learning", "count": 1, "lines": ["In your book: Write the letter of your answer and one reason."], "pass": true, "words": 9}, {"slide": 7, "title": "Independent application", "count": 1, "lines": ["In your book: Complete your route's task in your book; use its stem."], "pass": true, "words": 10}, {"slide": 8, "title": "Review and improve", "count": 1, "lines": ["In your book: Read back one answer (?); improve it and mark //."], "pass": true, "words": 10}, {"slide": 9, "title": "Exit ticket", "count": 1, "lines": ["In your book: Answer both questions under today's work."], "pass": true, "words": 6}]`

TA opening static evidence: `[{"slide": "slide-1", "chars": 287, "text": "Staff planning and targets Comparing responses to a life question Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-2", "chars": 256, "text": "Staff planning and targets Arrival Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-3", "chars": 266, "text": "Staff planning and targets Start the enquiry Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-4", "chars": 271, "text": "Staff planning and targets I do · a worked method Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-5", "chars": 273, "text": "Staff planning and targets We do · sort and justify Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-6", "chars": 267, "text": "Staff planning and targets Apply the learning Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-7", "chars": 272, "text": "Staff planning and targets Independent application Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-8", "chars": 267, "text": "Staff planning and targets Review and improve Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-9", "chars": 260, "text": "Staff planning and targets Exit ticket Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}]`

TA opening counts (static proxy, not browser visibility): `[{"slide": "slide-1", "chars": 287, "text": "Staff planning and targets Comparing responses to a life question Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-2", "chars": 256, "text": "Staff planning and targets Arrival Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-3", "chars": 266, "text": "Staff planning and targets Start the enquiry Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-4", "chars": 271, "text": "Staff planning and targets I do · a worked method Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-5", "chars": 273, "text": "Staff planning and targets We do · sort and justify Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-6", "chars": 267, "text": "Staff planning and targets Apply the learning Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-7", "chars": 272, "text": "Staff planning and targets Independent application Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-8", "chars": 267, "text": "Staff planning and targets Review and improve Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-9", "chars": 260, "text": "Staff planning and targets Exit ticket Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}]`

### LAUNCH_RE_A2_W06

| Item | Result |
|---|---|
| Document shell | PASS |
| Duplicate IDs | PASS |
| F1 CSS exact bytes | PASS |
| F2 CSS exact bytes | PASS |
| CSS final order: fit then print | PASS |
| Nine teaching stages | PASS |
| Nine brandlines | PASS |
| Book lines: opening 0; all other stages 1 | PASS |
| F5 brandlines have no leading zero | PASS |
| Review includes // and ? | PASS |
| OL-2 one bare closed staff disclosure | PASS |
| OL-2 exact staff summary | PASS |
| F8 Planned adaptations | PASS |
| F8 Invite a response | PASS |
| F8 IEDP line exact | PASS |
| F8 five broad areas | PASS |
| F8 six invite routes | PASS |
| F6 preparation line | PASS |
| OL-2 answers-with-staff warning | PASS |
| OL-3 13 live teacher-card headings | PASS |
| E3 11 staff sections survive | PASS |
| OL-4 no staff file links in top bar | PASS |
| OL-4 top bar labels | PASS |
| OL-2 staff links outside disclosure | PASS |
| TA opening static counts recorded | PASS |
| OL-1 vary-exit retained | PASS |
| OL-1 adapter exact restored hash | PASS |
| OL-1 starter before exit builder | PASS |
| OL-11 arrival prompt exact live | PASS |
| OL-1 exit config unchanged | PASS |
| OL-12 arrival embedded picture equals week PNG | PASS |
| X3 no welcome guests claim | PASS |
| Visible internal-word scan | PASS |
| Banned wording scan | PASS |
| Pupil term-week scan excluding allowed headers | PASS |
| No served record filename references | PASS |
| F3 activity print cut heading | PASS |
| OL-9 ledger one H1 | PASS |
| RB-3 approved mark credit row | PASS |
| RB-3 D1 block byte-identical | PASS |
| OL-9 per-link access checks | PASS |
| OL-3 no unexplained live card sentence loss | PASS |
| Pupil companion HTML scans | PASS |

| Stage | Book line |
|---|---|
| 1 |  |
| 2 | In your book: Glue in today's strip; date it. Answer 1 and 2 first. |
| 3 | In your book: Write one response to Describe or compare?; use a clue. |
| 4 | In your book: Watch the four model steps. No writing yet. |
| 5 | In your book: Move or match each card; record your explanation and its evidence. |
| 6 | In your book: Write the letter of your answer and one reason. |
| 7 | In your book: Complete your route's task in your book; use its stem. |
| 8 | In your book: Read back one answer (?); improve it and mark //. |
| 9 | In your book: Answer both questions under today's work. |

TA opening static evidence: `[{"slide": 1, "title": "A structured “compare” response", "count": 0, "lines": [], "pass": true, "words": 0}, {"slide": 2, "title": "Arrival", "count": 1, "lines": ["In your book: Glue in today's strip; date it. Answer 1 and 2 first."], "pass": true, "words": 11}, {"slide": 3, "title": "Start the enquiry", "count": 1, "lines": ["In your book: Write one response to Describe or compare?; use a clue."], "pass": true, "words": 10}, {"slide": 4, "title": "I do · a worked method", "count": 1, "lines": ["In your book: Watch the four model steps. No writing yet."], "pass": true, "words": 8}, {"slide": 5, "title": "We do · repair the draft", "count": 1, "lines": ["In your book: Move or match each card; record your explanation and its evidence."], "pass": true, "words": 11}, {"slide": 6, "title": "Apply the learning", "count": 1, "lines": ["In your book: Write the letter of your answer and one reason."], "pass": true, "words": 9}, {"slide": 7, "title": "Independent application", "count": 1, "lines": ["In your book: Complete your route's task in your book; use its stem."], "pass": true, "words": 10}, {"slide": 8, "title": "Review and improve", "count": 1, "lines": ["In your book: Read back one answer (?); improve it and mark //."], "pass": true, "words": 10}, {"slide": 9, "title": "Exit ticket", "count": 1, "lines": ["In your book: Answer both questions under today's work."], "pass": true, "words": 6}]`

TA opening static evidence: `[{"slide": "slide-1", "chars": 280, "text": "Staff planning and targets A structured “compare” response Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-2", "chars": 256, "text": "Staff planning and targets Arrival Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-3", "chars": 266, "text": "Staff planning and targets Start the enquiry Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-4", "chars": 271, "text": "Staff planning and targets I do · a worked method Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-5", "chars": 273, "text": "Staff planning and targets We do · repair the draft Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-6", "chars": 267, "text": "Staff planning and targets Apply the learning Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-7", "chars": 272, "text": "Staff planning and targets Independent application Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-8", "chars": 267, "text": "Staff planning and targets Review and improve Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-9", "chars": 260, "text": "Staff planning and targets Exit ticket Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}]`

TA opening counts (static proxy, not browser visibility): `[{"slide": "slide-1", "chars": 280, "text": "Staff planning and targets A structured “compare” response Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-2", "chars": 256, "text": "Staff planning and targets Arrival Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-3", "chars": 266, "text": "Staff planning and targets Start the enquiry Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-4", "chars": 271, "text": "Staff planning and targets I do · a worked method Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-5", "chars": 273, "text": "Staff planning and targets We do · repair the draft Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-6", "chars": 267, "text": "Staff planning and targets Apply the learning Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-7", "chars": 272, "text": "Staff planning and targets Independent application Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-8", "chars": 267, "text": "Staff planning and targets Review and improve Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-9", "chars": 260, "text": "Staff planning and targets Exit ticket Use questioning and the exit response to decide the next step. Record the learner’s individual contribution and the access support used. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}]`

### LAUNCH_RE_A2_W07

| Item | Result |
|---|---|
| Document shell | PASS |
| Duplicate IDs | PASS |
| F1 CSS exact bytes | PASS |
| F2 CSS exact bytes | PASS |
| CSS final order: fit then print | PASS |
| Nine teaching stages | PASS |
| Nine brandlines | PASS |
| Book lines: opening 0; all other stages 1 | PASS |
| F5 brandlines have no leading zero | PASS |
| Review includes // and ? | PASS |
| OL-2 one bare closed staff disclosure | PASS |
| OL-2 exact staff summary | PASS |
| F8 Planned adaptations | PASS |
| F8 Invite a response | PASS |
| F8 IEDP line exact | PASS |
| F8 five broad areas | PASS |
| F8 six invite routes | PASS |
| F6 preparation line | PASS |
| OL-2 answers-with-staff warning | PASS |
| OL-3 13 live teacher-card headings | PASS |
| E3 11 staff sections survive | PASS |
| OL-4 no staff file links in top bar | PASS |
| OL-4 top bar labels | PASS |
| OL-2 staff links outside disclosure | PASS |
| TA opening static counts recorded | PASS |
| OL-1 vary-exit retained | PASS |
| OL-1 adapter exact restored hash | PASS |
| OL-1 starter before exit builder | PASS |
| OL-11 arrival prompt exact live | PASS |
| OL-1 exit config unchanged | PASS |
| OL-12 arrival embedded picture equals week PNG | PASS |
| X3 no welcome guests claim | PASS |
| Visible internal-word scan | PASS |
| Banned wording scan | PASS |
| Pupil term-week scan excluding allowed headers | PASS |
| No served record filename references | PASS |
| F3 activity print cut heading | PASS |
| OL-9 ledger one H1 | PASS |
| RB-3 approved mark credit row | PASS |
| RB-3 D1 block byte-identical | PASS |
| OL-9 per-link access checks | PASS |
| OL-3 no unexplained live card sentence loss | PASS |
| Pupil companion HTML scans | PASS |

| Stage | Book line |
|---|---|
| 1 |  |
| 2 | In your book: Glue in today's strip; date it. Answer 1 and 2 first. |
| 3 | In your book: Write one response to Belief, practice or meaning?; use a clue. |
| 4 | In your book: Watch the four model steps. No writing yet. |
| 5 | In your book: Move or match each card; record your explanation and its evidence. |
| 6 | In your book: Write the letter of your answer and one reason. |
| 7 | In your book: Complete your route's task in your book; use its stem. |
| 8 | In your book: Read back one answer (?); improve it and mark //. |
| 9 | In your book: Answer both questions under today's work. |

TA opening static evidence: `[{"slide": 1, "title": "Beliefs and practices assessment", "count": 0, "lines": [], "pass": true, "words": 0}, {"slide": 2, "title": "Arrival", "count": 1, "lines": ["In your book: Glue in today's strip; date it. Answer 1 and 2 first."], "pass": true, "words": 11}, {"slide": 3, "title": "Start the enquiry", "count": 1, "lines": ["In your book: Write one response to Belief, practice or meaning?; use a clue."], "pass": true, "words": 11}, {"slide": 4, "title": "I do · a worked method", "count": 1, "lines": ["In your book: Watch the four model steps. No writing yet."], "pass": true, "words": 8}, {"slide": 5, "title": "We do · match and explain", "count": 1, "lines": ["In your book: Move or match each card; record your explanation and its evidence."], "pass": true, "words": 11}, {"slide": 6, "title": "Apply the learning", "count": 1, "lines": ["In your book: Write the letter of your answer and one reason."], "pass": true, "words": 9}, {"slide": 7, "title": "Independent application", "count": 1, "lines": ["In your book: Complete your route's task in your book; use its stem."], "pass": true, "words": 10}, {"slide": 8, "title": "Review and improve", "count": 1, "lines": ["In your book: Read back one answer (?); improve it and mark //."], "pass": true, "words": 10}, {"slide": 9, "title": "Exit ticket", "count": 1, "lines": ["In your book: Answer both questions under today's work."], "pass": true, "words": 6}]`

TA opening static evidence: `[{"slide": "slide-1", "chars": 337, "text": "Staff planning and targets Beliefs and practices assessment Use a different example for shared practice. During independent assessment, keep the agreed reader, scribe, glossary or response mode, but withdraw answer models and record prompts separately. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-2", "chars": 312, "text": "Staff planning and targets Arrival Use a different example for shared practice. During independent assessment, keep the agreed reader, scribe, glossary or response mode, but withdraw answer models and record prompts separately. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-3", "chars": 322, "text": "Staff planning and targets Start the enquiry Use a different example for shared practice. During independent assessment, keep the agreed reader, scribe, glossary or response mode, but withdraw answer models and record prompts separately. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-4", "chars": 327, "text": "Staff planning and targets I do · a worked method Use a different example for shared practice. During independent assessment, keep the agreed reader, scribe, glossary or response mode, but withdraw answer models and record prompts separately. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-5", "chars": 330, "text": "Staff planning and targets We do · match and explain Use a different example for shared practice. During independent assessment, keep the agreed reader, scribe, glossary or response mode, but withdraw answer models and record prompts separately. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-6", "chars": 323, "text": "Staff planning and targets Apply the learning Use a different example for shared practice. During independent assessment, keep the agreed reader, scribe, glossary or response mode, but withdraw answer models and record prompts separately. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-7", "chars": 328, "text": "Staff planning and targets Independent application Use a different example for shared practice. During independent assessment, keep the agreed reader, scribe, glossary or response mode, but withdraw answer models and record prompts separately. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-8", "chars": 323, "text": "Staff planning and targets Review and improve Use a different example for shared practice. During independent assessment, keep the agreed reader, scribe, glossary or response mode, but withdraw answer models and record prompts separately. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-9", "chars": 316, "text": "Staff planning and targets Exit ticket Use a different example for shared practice. During independent assessment, keep the agreed reader, scribe, glossary or response mode, but withdraw answer models and record prompts separately. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}]`

TA opening counts (static proxy, not browser visibility): `[{"slide": "slide-1", "chars": 337, "text": "Staff planning and targets Beliefs and practices assessment Use a different example for shared practice. During independent assessment, keep the agreed reader, scribe, glossary or response mode, but withdraw answer models and record prompts separately. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-2", "chars": 312, "text": "Staff planning and targets Arrival Use a different example for shared practice. During independent assessment, keep the agreed reader, scribe, glossary or response mode, but withdraw answer models and record prompts separately. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-3", "chars": 322, "text": "Staff planning and targets Start the enquiry Use a different example for shared practice. During independent assessment, keep the agreed reader, scribe, glossary or response mode, but withdraw answer models and record prompts separately. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-4", "chars": 327, "text": "Staff planning and targets I do · a worked method Use a different example for shared practice. During independent assessment, keep the agreed reader, scribe, glossary or response mode, but withdraw answer models and record prompts separately. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-5", "chars": 330, "text": "Staff planning and targets We do · match and explain Use a different example for shared practice. During independent assessment, keep the agreed reader, scribe, glossary or response mode, but withdraw answer models and record prompts separately. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-6", "chars": 323, "text": "Staff planning and targets Apply the learning Use a different example for shared practice. During independent assessment, keep the agreed reader, scribe, glossary or response mode, but withdraw answer models and record prompts separately. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-7", "chars": 328, "text": "Staff planning and targets Independent application Use a different example for shared practice. During independent assessment, keep the agreed reader, scribe, glossary or response mode, but withdraw answer models and record prompts separately. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-8", "chars": 323, "text": "Staff planning and targets Review and improve Use a different example for shared practice. During independent assessment, keep the agreed reader, scribe, glossary or response mode, but withdraw answer models and record prompts separately. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}, {"slide": "slide-9", "chars": 316, "text": "Staff planning and targets Exit ticket Use a different example for shared practice. During independent assessment, keep the agreed reader, scribe, glossary or response mode, but withdraw answer models and record prompts separately. Teacher notes and answers Teacher notes PDF TA brief (PDF) Slides (PowerPoint) Close", "method": "Static simulation of showTABrief dataset fields and closed details; not rendered-browser visibility."}]`

## Open gates

- F4: 72 exact Chromium pupil-PDF exports missing; pupil PDF geometry, text and page-break parity are therefore not assessed. BUILD W01’s required five-page count is not claimed.
- F1/F2: exact CSS is verified statically; pixel fit and HTML print pagination still require the stated browser review.
- Browser/Office interaction and playback checks remain with the reviewer as requested.
- Parent START_HERE navigation remains an external pack dependency, as in the accepted pilot.
- Required pupil-PDF links retain their intended filenames and will resolve after the exports are produced. Do not publish these review ZIPs as a completed RB1 release.


## PowerPoint static checks

24 decks; 499 slides. All decks authored/edited with @oai/artifact-tool and passed package import/finalization. The 21 Autumn 2 deck counts remain 450 in total; return decks are BUILD 16, GROW 16 and LAUNCH 17. The additional LAUNCH slide carries the two actual remembrance source passages needed for its extended check.

Text-box overlap checks compare every non-empty slide text box pair in native PPTX XML, requiring positive intersection in both dimensions (tolerance 0.1 px). Empty inherited placeholders are excluded. Results do not substitute for the separate Office review requested in the order.

Every teaching slide has its book line, staff move and expected responses in native speaker notes. Slide 1 has the complete staff guidance, planned adaptations, six route invitations and full IEDP sentence. Per-slide note counts and geometry findings are in each lesson JSON. All final slides were rendered with Artifact Tool; representative changed layouts were visually checked.

| Lesson | Slides | Notes min–max characters | Text-box overlaps | Final JSON matched | Matt Roper metadata | Full IEDP | Readable starter key | Model check restored |
|---|---:|---:|---:|---|---|---|---|---|---|
| BUILD_RE_A1_W08 | 16 | 513–10463 | 0 | True | True | True | return key | return combined model |
| BUILD_RE_A2_W01 | 21 | 2060–18528 | 0 | True | True | True | True | True |
| BUILD_RE_A2_W02 | 21 | 2012–19406 | 0 | True | True | True | True | True |
| BUILD_RE_A2_W03 | 21 | 1735–18826 | 0 | True | True | True | True | True |
| BUILD_RE_A2_W04 | 21 | 1974–19511 | 0 | True | True | True | True | True |
| BUILD_RE_A2_W05 | 21 | 2565–19171 | 0 | True | True | True | True | True |
| BUILD_RE_A2_W06 | 21 | 1841–18370 | 0 | True | True | True | True | True |
| BUILD_RE_A2_W07 | 23 | 2140–19295 | 0 | True | True | True | True | True |
| GROW_RE_A1_W08 | 16 | 581–17062 | 0 | True | True | True | return key | return combined model |
| GROW_RE_A2_W01 | 21 | 2436–20687 | 0 | True | True | True | True | True |
| GROW_RE_A2_W02 | 21 | 2399–19906 | 0 | True | True | True | True | True |
| GROW_RE_A2_W03 | 21 | 2191–19776 | 0 | True | True | True | True | True |
| GROW_RE_A2_W04 | 21 | 1947–19632 | 0 | True | True | True | True | True |
| GROW_RE_A2_W05 | 21 | 2272–20207 | 0 | True | True | True | True | True |
| GROW_RE_A2_W06 | 21 | 1947–20049 | 0 | True | True | True | True | True |
| GROW_RE_A2_W07 | 25 | 2568–21291 | 0 | True | True | True | True | True |
| LAUNCH_RE_A1_W08 | 17 | 550–12505 | 0 | True | True | True | return key | return combined model |
| LAUNCH_RE_A2_W01 | 21 | 2254–19922 | 0 | True | True | True | True | True |
| LAUNCH_RE_A2_W02 | 21 | 2103–20273 | 0 | True | True | True | True | True |
| LAUNCH_RE_A2_W03 | 21 | 2513–20713 | 0 | True | True | True | True | True |
| LAUNCH_RE_A2_W04 | 21 | 2319–20880 | 0 | True | True | True | True | True |
| LAUNCH_RE_A2_W05 | 22 | 2392–21294 | 0 | True | True | True | True | True |
| LAUNCH_RE_A2_W06 | 21 | 2454–21406 | 0 | True | True | True | True | True |
| LAUNCH_RE_A2_W07 | 23 | 3268–22721 | 0 | True | True | True | True | True |

All slides have positional numbering. BUILD return contains the four actual check pictures and choices. LAUNCH Autumn 2 Week 5 restores the evidence continuation and review faces, places model/exit faces under their correct titles, and positions the hinge after Shared activity cards. Its misplaced model and exit note paragraphs are removed from their former slides.

No delivery was published or merged.

## Notes per slide


### BUILD_RE_A1_W08

| Slide | Title | Notes characters | Staff move | Book line | Answer characters |
|---|---|---:|---|---|---:|
| 1 | Special things, respect and belonging | 10463 | True | opening | 68 |
| 2 | Arrival task | 1541 | True | In your book: Glue in today’s strip; date it. Answer questions 1 to 4. | 1202 |
| 3 | Start the enquiry | 572 | True | In your book: Number 1 to 3. Write or draw one answer for each. | 247 |
| 4 | I do · a worked method | 950 | True | In your book: Watch the object-card model. No writing yet. | 628 |
| 5 | Captioned model | 950 | True | In your book: Watch the object-card model. No writing yet. | 628 |
| 6 | We do · source detective | 513 | True | In your book: Write or draw an object and match its reason. | 193 |
| 7 | Check the idea | 2033 | True | In your book: Write the letter of your answer. Explain one clue. | 1711 |
| 8 | Independent book check | 1179 | True | In your book: Number 1 to 4. Choose the answer or pair for each picture. | 841 |
| 9 | Supported | 1179 | True | In your book: Number 1 to 4. Choose the answer or pair for each picture. | 841 |
| 10 | Supported · continued | 1179 | True | In your book: Number 1 to 4. Choose the answer or pair for each picture. | 841 |
| 11 | Standard | 1179 | True | In your book: Number 1 to 4. Choose the answer or pair for each picture. | 841 |
| 12 | Standard · continued | 1179 | True | In your book: Number 1 to 4. Choose the answer or pair for each picture. | 841 |
| 13 | Stretch | 1179 | True | In your book: Number 1 to 4. Choose the answer or pair for each picture. | 841 |
| 14 | Stretch · continued | 1179 | True | In your book: Number 1 to 4. Choose the answer or pair for each picture. | 841 |
| 15 | Review and improve | 523 | True | In your book: Read back one answer (?); improve it and mark //. | 197 |
| 16 | Exit ticket | 646 | True | In your book: Describe one object card and give one reason it matters. | 174 |

### BUILD_RE_A2_W01

| Slide | Title | Notes characters | Staff move | Book line | Answer characters |
|---|---|---:|---|---|---:|
| 1 | A festival of light: Diwali | 18528 | True | opening | 68 |
| 2 | Arrival questions 1 and 2 | 6294 | True | In your book: Glue in today's strip; date it. Answer 1 and 2 first. | 1656 |
| 3 | Arrival questions 3 and 4 | 6294 | True | In your book: Glue in today's strip; date it. Answer 1 and 2 first. | 1656 |
| 4 | Words for this lesson | 3368 | True | In your book: Glue in today's strip; date it. Answer 1 and 2 first. | 1656 |
| 5 | Starter | 2060 | True | In your book: Write one guess for Mystery light after the clues. | 159 |
| 6 | Model question | 2837 | True | In your book: Watch the four model steps. No writing yet. | 493 |
| 7 | Model evidence | 2837 | True | In your book: Watch the four model steps. No writing yet. | 493 |
| 8 | Model explanation | 2977 | True | In your book: Watch the four model steps. No writing yet. | 493 |
| 9 | Model check | 3142 | True | In your book: Watch the four model steps. No writing yet. | 493 |
| 10 | We do | 2729 | True | In your book: Match each card; write one meaning and the evidence card. | 290 |
| 11 | Shared activity cards | 2392 | True | In your book: Match each card; write one meaning and the evidence card. | 290 |
| 12 | Apply the learning | 11740 | True | In your book: Write the letter of your answer and one reason. | 2054 |
| 13 | Independent task supported | 3273 | True | In your book: Draw or write your route's task; use its stem. | 919 |
| 14 | Independent task standard | 3095 | True | In your book: Draw or write your route's task; use its stem. | 919 |
| 15 | Independent task stretch | 3126 | True | In your book: Draw or write your route's task; use its stem. | 919 |
| 16 | Review and improve | 2279 | True | In your book: Read back one answer (?); improve it and mark //. | 188 |
| 17 | Exit ticket | 2672 | True | In your book: Answer both questions under today's work. | 669 |
| 18 | Evidence A Diwali | 2500 | True | In your book: Match each card; write one meaning and the evidence card. | 290 |
| 19 | Evidence B The diya | 2500 | True | In your book: Match each card; write one meaning and the evidence card. | 290 |
| 20 | Evidence C Rangoli | 2500 | True | In your book: Match each card; write one meaning and the evidence card. | 290 |
| 21 | Evidence D Light as a symbol | 2500 | True | In your book: Match each card; write one meaning and the evidence card. | 290 |

### BUILD_RE_A2_W02

| Slide | Title | Notes characters | Staff move | Book line | Answer characters |
|---|---|---:|---|---|---:|
| 1 | Comparing light in celebrations | 19406 | True | opening | 68 |
| 2 | Arrival questions 1 and 2 | 6191 | True | In your book: Glue in today's strip; date it. Answer 1 and 2 first. | 1692 |
| 3 | Arrival questions 3 and 4 | 6191 | True | In your book: Glue in today's strip; date it. Answer 1 and 2 first. | 1692 |
| 4 | Words for this lesson | 3352 | True | In your book: Glue in today's strip; date it. Answer 1 and 2 first. | 1692 |
| 5 | Starter | 2012 | True | In your book: Write one response to Which celebration?; use a clue. | 132 |
| 6 | Model question | 3052 | True | In your book: Watch the four model steps. No writing yet. | 621 |
| 7 | Model evidence | 3052 | True | In your book: Watch the four model steps. No writing yet. | 621 |
| 8 | Model explanation | 3225 | True | In your book: Watch the four model steps. No writing yet. | 621 |
| 9 | Model check | 3166 | True | In your book: Watch the four model steps. No writing yet. | 621 |
| 10 | We do | 2722 | True | In your book: Move or match each card; record your explanation and its evidence. | 183 |
| 11 | Shared activity cards | 2122 | True | In your book: Move or match each card; record your explanation and its evidence. | 183 |
| 12 | Apply the learning | 12087 | True | In your book: Write the letter of your answer and one reason. | 2149 |
| 13 | Independent task supported | 3473 | True | In your book: Complete your route's task in your book; use its stem. | 1032 |
| 14 | Independent task standard | 3294 | True | In your book: Complete your route's task in your book; use its stem. | 1032 |
| 15 | Independent task stretch | 3354 | True | In your book: Complete your route's task in your book; use its stem. | 1032 |
| 16 | Review and improve | 2354 | True | In your book: Read back one answer (?); improve it and mark //. | 194 |
| 17 | Exit ticket | 2869 | True | In your book: Answer both questions under today's work. | 921 |
| 18 | Evidence A Diwali | 2451 | True | In your book: Move or match each card; record your explanation and its evidence. | 183 |
| 19 | Evidence B Hanukkah | 2451 | True | In your book: Move or match each card; record your explanation and its evidence. | 183 |
| 20 | Evidence C Both | 2451 | True | In your book: Move or match each card; record your explanation and its evidence. | 183 |
| 21 | Evidence D Comparing fairly | 2451 | True | In your book: Move or match each card; record your explanation and its evidence. | 183 |

### BUILD_RE_A2_W03

| Slide | Title | Notes characters | Staff move | Book line | Answer characters |
|---|---|---:|---|---|---:|
| 1 | Retelling a festival story | 18826 | True | opening | 68 |
| 2 | Arrival questions 1 and 2 | 5666 | True | In your book: Glue in today's strip; date it. Answer 1 and 2 first. | 1608 |
| 3 | Arrival questions 3 and 4 | 5666 | True | In your book: Glue in today's strip; date it. Answer 1 and 2 first. | 1608 |
| 4 | Words for this lesson | 2986 | True | In your book: Glue in today's strip; date it. Answer 1 and 2 first. | 1608 |
| 5 | Starter | 1735 | True | In your book: Write one response to Put the morning in order; use a clue. | 162 |
| 6 | Model question | 2372 | True | In your book: Watch the four model steps. No writing yet. | 477 |
| 7 | Model evidence | 2372 | True | In your book: Watch the four model steps. No writing yet. | 477 |
| 8 | Model explanation | 2494 | True | In your book: Watch the four model steps. No writing yet. | 477 |
| 9 | Model check | 2564 | True | In your book: Watch the four model steps. No writing yet. | 477 |
| 10 | We do | 2312 | True | In your book: Move or match each card; record your explanation and its evidence. | 320 |
| 11 | Shared activity cards | 2109 | True | In your book: Move or match each card; record your explanation and its evidence. | 320 |
| 12 | Apply the learning | 11803 | True | In your book: Write the letter of your answer and one reason. | 2128 |
| 13 | Independent task supported | 2963 | True | In your book: Complete your route's task in your book; use its stem. | 1036 |
| 14 | Independent task standard | 2784 | True | In your book: Complete your route's task in your book; use its stem. | 1036 |
| 15 | Independent task stretch | 2827 | True | In your book: Complete your route's task in your book; use its stem. | 1036 |
| 16 | Review and improve | 1826 | True | In your book: Read back one answer (?); improve it and mark //. | 185 |
| 17 | Exit ticket | 2525 | True | In your book: Answer both questions under today's work. | 897 |
| 18 | Evidence A Sent away | 2063 | True | In your book: Move or match each card; record your explanation and its evidence. | 320 |
| 19 | Evidence B Sita is taken | 2063 | True | In your book: Move or match each card; record your explanation and its evidence. | 320 |
| 20 | Evidence C The rescue | 2063 | True | In your book: Move or match each card; record your explanation and its evidence. | 320 |
| 21 | Evidence D Lamps light the way | 2063 | True | In your book: Move or match each card; record your explanation and its evidence. | 320 |

### BUILD_RE_A2_W04

| Slide | Title | Notes characters | Staff move | Book line | Answer characters |
|---|---|---:|---|---|---:|
| 1 | Taking part respectfully | 19511 | True | opening | 68 |
| 2 | Arrival questions 1 and 2 | 5923 | True | In your book: Glue in today's strip; date it. Answer 1 and 2 first. | 1689 |
| 3 | Arrival questions 3 and 4 | 5923 | True | In your book: Glue in today's strip; date it. Answer 1 and 2 first. | 1689 |
| 4 | Words for this lesson | 3151 | True | In your book: Glue in today's strip; date it. Answer 1 and 2 first. | 1689 |
| 5 | Starter | 1974 | True | In your book: Write one response to Respectful or not respectful?; use a clue. | 230 |
| 6 | Model question | 2591 | True | In your book: Watch the four model steps. No writing yet. | 527 |
| 7 | Model evidence | 2591 | True | In your book: Watch the four model steps. No writing yet. | 527 |
| 8 | Model explanation | 2755 | True | In your book: Watch the four model steps. No writing yet. | 527 |
| 9 | Model check | 2773 | True | In your book: Watch the four model steps. No writing yet. | 527 |
| 10 | We do | 2476 | True | In your book: Move or match each card; record your explanation and its evidence. | 269 |
| 11 | Shared activity cards | 2122 | True | In your book: Move or match each card; record your explanation and its evidence. | 269 |
| 12 | Apply the learning | 12573 | True | In your book: Write the letter of your answer and one reason. | 2373 |
| 13 | Independent task supported | 3162 | True | In your book: Complete your route's task in your book; use its stem. | 1089 |
| 14 | Independent task standard | 2983 | True | In your book: Complete your route's task in your book; use its stem. | 1089 |
| 15 | Independent task stretch | 3040 | True | In your book: Complete your route's task in your book; use its stem. | 1089 |
| 16 | Review and improve | 2020 | True | In your book: Read back one answer (?); improve it and mark //. | 224 |
| 17 | Exit ticket | 2573 | True | In your book: Answer both questions under today's work. | 849 |
| 18 | Evidence A Learning, not worship | 2199 | True | In your book: Move or match each card; record your explanation and its evidence. | 269 |
| 19 | Evidence B Our activity | 2199 | True | In your book: Move or match each card; record your explanation and its evidence. | 269 |
| 20 | Evidence C Rangoli-style patterns | 2199 | True | In your book: Move or match each card; record your explanation and its evidence. | 269 |
| 21 | Evidence D Taking part with respect | 2199 | True | In your book: Move or match each card; record your explanation and its evidence. | 269 |

### BUILD_RE_A2_W05

| Slide | Title | Notes characters | Staff move | Book line | Answer characters |
|---|---|---:|---|---|---:|
| 1 | Hope and remembrance | 19171 | True | opening | 68 |
| 2 | Arrival questions 1 and 2 | 6562 | True | In your book: Glue in today's strip; date it. Answer 1 and 2 first. | 1722 |
| 3 | Arrival questions 3 and 4 | 6562 | True | In your book: Glue in today's strip; date it. Answer 1 and 2 first. | 1722 |
| 4 | Words for this lesson | 3714 | True | In your book: Glue in today's strip; date it. Answer 1 and 2 first. | 1722 |
| 5 | Starter | 2588 | True | In your book: Write one response to Hope, remembrance or neither?; use a clue. | 290 |
| 6 | Model question | 3121 | True | In your book: Watch the four model steps. No writing yet. | 500 |
| 7 | Model evidence | 3121 | True | In your book: Watch the four model steps. No writing yet. | 500 |
| 8 | Model explanation | 3297 | True | In your book: Watch the four model steps. No writing yet. | 500 |
| 9 | Model check | 3287 | True | In your book: Watch the four model steps. No writing yet. | 500 |
| 10 | We do | 2990 | True | In your book: Move or match each card; record your explanation and its evidence. | 248 |
| 11 | Shared activity cards | 2612 | True | In your book: Move or match each card; record your explanation and its evidence. | 248 |
| 12 | Apply the learning | 12205 | True | In your book: Write the letter of your answer and one reason. | 2168 |
| 13 | Independent task supported | 3568 | True | In your book: Complete your route's task in your book; use its stem. | 936 |
| 14 | Independent task standard | 3389 | True | In your book: Complete your route's task in your book; use its stem. | 936 |
| 15 | Independent task stretch | 3433 | True | In your book: Complete your route's task in your book; use its stem. | 936 |
| 16 | Review and improve | 2565 | True | In your book: Read back one answer (?); improve it and mark //. | 216 |
| 17 | Exit ticket | 2917 | True | In your book: Answer both questions under today's work. | 687 |
| 18 | Evidence A The poppy | 2733 | True | In your book: Move or match each card; record your explanation and its evidence. | 248 |
| 19 | Evidence B Two minutes of silence | 2733 | True | In your book: Move or match each card; record your explanation and its evidence. | 248 |
| 20 | Evidence C A light in the window | 2733 | True | In your book: Move or match each card; record your explanation and its evidence. | 248 |
| 21 | Evidence D A memorial | 2733 | True | In your book: Move or match each card; record your explanation and its evidence. | 248 |

### BUILD_RE_A2_W06

| Slide | Title | Notes characters | Staff move | Book line | Answer characters |
|---|---|---:|---|---|---:|
| 1 | A big question | 18370 | True | opening | 68 |
| 2 | Arrival questions 1 and 2 | 5682 | True | In your book: Glue in today's strip; date it. Answer 1 and 2 first. | 1617 |
| 3 | Arrival questions 3 and 4 | 5682 | True | In your book: Glue in today's strip; date it. Answer 1 and 2 first. | 1617 |
| 4 | Words for this lesson | 2982 | True | In your book: Glue in today's strip; date it. Answer 1 and 2 first. | 1617 |
| 5 | Starter | 1841 | True | In your book: Write one response to What makes something special?; use a clue. | 232 |
| 6 | Model question | 2286 | True | In your book: Watch the four model steps. No writing yet. | 394 |
| 7 | Model evidence | 2286 | True | In your book: Watch the four model steps. No writing yet. | 394 |
| 8 | Model explanation | 2357 | True | In your book: Watch the four model steps. No writing yet. | 394 |
| 9 | Model check | 2472 | True | In your book: Watch the four model steps. No writing yet. | 394 |
| 10 | We do | 2336 | True | In your book: Move or match each card; record your explanation and its evidence. | 281 |
| 11 | Shared activity cards | 2040 | True | In your book: Move or match each card; record your explanation and its evidence. | 281 |
| 12 | Apply the learning | 11783 | True | In your book: Write the letter of your answer and one reason. | 2284 |
| 13 | Independent task supported | 2843 | True | In your book: Complete your route's task in your book; use its stem. | 918 |
| 14 | Independent task standard | 2664 | True | In your book: Complete your route's task in your book; use its stem. | 918 |
| 15 | Independent task stretch | 2741 | True | In your book: Complete your route's task in your book; use its stem. | 918 |
| 16 | Review and improve | 1846 | True | In your book: Read back one answer (?); improve it and mark //. | 191 |
| 17 | Exit ticket | 2307 | True | In your book: Answer both questions under today's work. | 713 |
| 18 | Evidence A Big questions | 2061 | True | In your book: Move or match each card; record your explanation and its evidence. | 281 |
| 19 | Evidence B A weak answer | 2061 | True | In your book: Move or match each card; record your explanation and its evidence. | 281 |
| 20 | Evidence C A stronger answer | 2061 | True | In your book: Move or match each card; record your explanation and its evidence. | 281 |
| 21 | Evidence D Different views | 2061 | True | In your book: Move or match each card; record your explanation and its evidence. | 281 |

### BUILD_RE_A2_W07

| Slide | Title | Notes characters | Staff move | Book line | Answer characters |
|---|---|---:|---|---|---:|
| 1 | Festival reflection and UAS evidence | 19295 | True | opening | 68 |
| 2 | Arrival questions 1 and 2 | 5510 | True | In your book: Glue in today's strip; date it. Answer 1 and 2 first. | 1491 |
| 3 | Arrival questions 3 and 4 | 5510 | True | In your book: Glue in today's strip; date it. Answer 1 and 2 first. | 1491 |
| 4 | Words for this lesson | 2939 | True | In your book: Glue in today's strip; date it. Answer 1 and 2 first. | 1491 |
| 5 | Starter | 2140 | True | In your book: Write one response to Which pairs are correct?; use a clue. | 348 |
| 6 | Model question | 2893 | True | In your book: Watch the four model steps. No writing yet. | 538 |
| 7 | Model evidence | 2893 | True | In your book: Watch the four model steps. No writing yet. | 538 |
| 8 | Model explanation | 3123 | True | In your book: Watch the four model steps. No writing yet. | 538 |
| 9 | Model check | 3083 | True | In your book: Watch the four model steps. No writing yet. | 538 |
| 10 | We do | 2785 | True | In your book: Move or match each card; record your explanation and its evidence. | 334 |
| 11 | Shared activity cards | 2140 | True | In your book: Move or match each card; record your explanation and its evidence. | 334 |
| 12 | Apply the learning | 11650 | True | In your book: Write the letter of your answer and one reason. | 2132 |
| 13 | Independent task supported | 3452 | True | In your book: Complete your route's task in your book; use its stem. | 1070 |
| 14 | Independent task standard | 3273 | True | In your book: Complete your route's task in your book; use its stem. | 1070 |
| 15 | Independent task stretch | 3276 | True | In your book: Complete your route's task in your book; use its stem. | 1070 |
| 16 | Review and improve | 2282 | True | In your book: Read back one answer (?); improve it and mark //. | 217 |
| 17 | Exit ticket | 2351 | True | In your book: Answer both questions under today's work. | 647 |
| 18 | Evidence A The reflection page | 2546 | True | In your book: Move or match each card; record your explanation and its evidence. | 334 |
| 19 | Evidence B A model page | 2546 | True | In your book: Move or match each card; record your explanation and its evidence. | 334 |
| 20 | Evidence C Evidence this half term | 2546 | True | In your book: Move or match each card; record your explanation and its evidence. | 334 |
| 21 | Evidence D Strong evidence | 2546 | True | In your book: Move or match each card; record your explanation and its evidence. | 334 |
| 22 | Evidence E1 Assessment source The diya | 2546 | True | In your book: Move or match each card; record your explanation and its evidence. | 334 |
| 23 | Evidence E2 Assessment source Rangoli | 2546 | True | In your book: Move or match each card; record your explanation and its evidence. | 334 |

### GROW_RE_A1_W08

| Slide | Title | Notes characters | Staff move | Book line | Answer characters |
|---|---|---:|---|---|---:|
| 1 | Shared values and what we remember | 17062 | True | opening | 68 |
| 2 | Arrival task | 1655 | True | In your book: Glue in today’s strip; date it. Answer questions 1 to 4. | 1316 |
| 3 | Start the enquiry | 622 | True | In your book: Number 1 to 3. Write one word for each. | 307 |
| 4 | I do · a worked method | 984 | True | In your book: Watch Ruth and Dan. No writing yet. | 671 |
| 5 | Captioned model | 984 | True | In your book: Watch Ruth and Dan. No writing yet. | 671 |
| 6 | We do · source detective | 581 | True | In your book: Write each action’s value; explain one match. | 261 |
| 7 | Check the idea | 2220 | True | In your book: Write the letter of your answer. Explain one clue. | 1898 |
| 8 | Independent book check | 977 | True | In your book: Write your route’s six answers using its sentence stems. | 641 |
| 9 | Supported | 977 | True | In your book: Write your route’s six answers using its sentence stems. | 641 |
| 10 | Supported · continued | 977 | True | In your book: Write your route’s six answers using its sentence stems. | 641 |
| 11 | Standard | 977 | True | In your book: Write your route’s six answers using its sentence stems. | 641 |
| 12 | Standard · continued | 977 | True | In your book: Write your route’s six answers using its sentence stems. | 641 |
| 13 | Stretch | 977 | True | In your book: Write your route’s six answers using its sentence stems. | 641 |
| 14 | Stretch · continued | 977 | True | In your book: Write your route’s six answers using its sentence stems. | 641 |
| 15 | Review and improve | 583 | True | In your book: Read back one answer (?); improve it and mark //. | 257 |
| 16 | Exit ticket | 672 | True | In your book: Answer under today’s work: one value and one reason. | 172 |

### GROW_RE_A2_W01

| Slide | Title | Notes characters | Staff move | Book line | Answer characters |
|---|---|---:|---|---|---:|
| 1 | Belonging across faiths | 20687 | True | opening | 68 |
| 2 | Arrival questions 1 and 2 | 6486 | True | In your book: Glue in today's strip; date it. Answer 1 and 2 first. | 1707 |
| 3 | Arrival questions 3 and 4 | 6486 | True | In your book: Glue in today's strip; date it. Answer 1 and 2 first. | 1707 |
| 4 | Words for this lesson | 3652 | True | In your book: Glue in today's strip; date it. Answer 1 and 2 first. | 1707 |
| 5 | Starter | 2472 | True | In your book: Write one response to What helps people feel they belong?; use a clue. | 285 |
| 6 | Model question | 3179 | True | In your book: Watch the four model steps. No writing yet. | 629 |
| 7 | Model evidence | 3179 | True | In your book: Watch the four model steps. No writing yet. | 629 |
| 8 | Model explanation | 3418 | True | In your book: Watch the four model steps. No writing yet. | 629 |
| 9 | Model check | 3411 | True | In your book: Watch the four model steps. No writing yet. | 629 |
| 10 | We do | 2953 | True | In your book: Move or match each card; record your explanation and its evidence. | 274 |
| 11 | Shared activity cards | 2608 | True | In your book: Move or match each card; record your explanation and its evidence. | 274 |
| 12 | Apply the learning | 14101 | True | In your book: Write the letter of your answer and one reason. | 2942 |
| 13 | Independent task supported | 3720 | True | In your book: Complete your route's task in your book; use its stem. | 1163 |
| 14 | Independent task standard | 3528 | True | In your book: Complete your route's task in your book; use its stem. | 1163 |
| 15 | Independent task stretch | 3577 | True | In your book: Complete your route's task in your book; use its stem. | 1163 |
| 16 | Review and improve | 2436 | True | In your book: Read back one answer (?); improve it and mark //. | 179 |
| 17 | Exit ticket | 3319 | True | In your book: Answer both questions under today's work. | 1075 |
| 18 | Evidence A Simran | 2658 | True | In your book: Move or match each card; record your explanation and its evidence. | 274 |
| 19 | Evidence B Yusuf | 2658 | True | In your book: Move or match each card; record your explanation and its evidence. | 274 |
| 20 | Evidence C Four lenses | 2658 | True | In your book: Move or match each card; record your explanation and its evidence. | 274 |
| 21 | Evidence D Belonging varies | 2658 | True | In your book: Move or match each card; record your explanation and its evidence. | 274 |

### GROW_RE_A2_W02

| Slide | Title | Notes characters | Staff move | Book line | Answer characters |
|---|---|---:|---|---|---:|
| 1 | Place of worship enquiry | 19906 | True | opening | 68 |
| 2 | Arrival questions 1 and 2 | 6666 | True | In your book: Glue in today's strip; date it. Answer 1 and 2 first. | 1830 |
| 3 | Arrival questions 3 and 4 | 6666 | True | In your book: Glue in today's strip; date it. Answer 1 and 2 first. | 1830 |
| 4 | Words for this lesson | 3745 | True | In your book: Glue in today's strip; date it. Answer 1 and 2 first. | 1830 |
| 5 | Starter | 2399 | True | In your book: Write one response to Photo reveal: what clues show a place of worship?; use a clue. | 210 |
| 6 | Model question | 3082 | True | In your book: Watch the four model steps. No writing yet. | 572 |
| 7 | Model evidence | 3082 | True | In your book: Watch the four model steps. No writing yet. | 572 |
| 8 | Model explanation | 3324 | True | In your book: Watch the four model steps. No writing yet. | 572 |
| 9 | Model check | 3256 | True | In your book: Watch the four model steps. No writing yet. | 572 |
| 10 | We do | 2877 | True | In your book: Move or match each card; record your explanation and its evidence. | 230 |
| 11 | Shared activity cards | 2497 | True | In your book: Move or match each card; record your explanation and its evidence. | 230 |
| 12 | Apply the learning | 13194 | True | In your book: Write the letter of your answer and one reason. | 2555 |
| 13 | Independent task supported | 3554 | True | In your book: Complete your route's task in your book; use its stem. | 1040 |
| 14 | Independent task standard | 3363 | True | In your book: Complete your route's task in your book; use its stem. | 1040 |
| 15 | Independent task stretch | 3422 | True | In your book: Complete your route's task in your book; use its stem. | 1040 |
| 16 | Review and improve | 2426 | True | In your book: Read back one answer (?); improve it and mark //. | 210 |
| 17 | Exit ticket | 2975 | True | In your book: Answer both questions under today's work. | 801 |
| 18 | Evidence A Prayer hall | 2580 | True | In your book: Move or match each card; record your explanation and its evidence. | 230 |
| 19 | Evidence B Mihrab and minbar | 2580 | True | In your book: Move or match each card; record your explanation and its evidence. | 230 |
| 20 | Evidence C Washing area | 2580 | True | In your book: Move or match each card; record your explanation and its evidence. | 230 |
| 21 | Evidence D Community use | 2580 | True | In your book: Move or match each card; record your explanation and its evidence. | 230 |

### GROW_RE_A2_W03

| Slide | Title | Notes characters | Staff move | Book line | Answer characters |
|---|---|---:|---|---|---:|
| 1 | Religious practice and subject vocabulary | 19776 | True | opening | 68 |
| 2 | Arrival questions 1 and 2 | 6658 | True | In your book: Glue in today's strip; date it. Answer 1 and 2 first. | 1836 |
| 3 | Arrival questions 3 and 4 | 6658 | True | In your book: Glue in today's strip; date it. Answer 1 and 2 first. | 1836 |
| 4 | Words for this lesson | 3586 | True | In your book: Glue in today's strip; date it. Answer 1 and 2 first. | 1836 |
| 5 | Starter | 2244 | True | In your book: Write one response to Match the word to the image idea; use a clue. | 281 |
| 6 | Model question | 2642 | True | In your book: Watch the four model steps. No writing yet. | 385 |
| 7 | Model evidence | 2642 | True | In your book: Watch the four model steps. No writing yet. | 385 |
| 8 | Model explanation | 2839 | True | In your book: Watch the four model steps. No writing yet. | 385 |
| 9 | Model check | 2782 | True | In your book: Watch the four model steps. No writing yet. | 385 |
| 10 | We do | 2657 | True | In your book: Move or match each card; record your explanation and its evidence. | 314 |
| 11 | Shared activity cards | 2473 | True | In your book: Move or match each card; record your explanation and its evidence. | 314 |
| 12 | Apply the learning | 13283 | True | In your book: Write the letter of your answer and one reason. | 2732 |
| 13 | Independent task supported | 3488 | True | In your book: Complete your route's task in your book; use its stem. | 1240 |
| 14 | Independent task standard | 3311 | True | In your book: Complete your route's task in your book; use its stem. | 1240 |
| 15 | Independent task stretch | 3361 | True | In your book: Complete your route's task in your book; use its stem. | 1240 |
| 16 | Review and improve | 2191 | True | In your book: Read back one answer (?); improve it and mark //. | 213 |
| 17 | Exit ticket | 2801 | True | In your book: Answer both questions under today's work. | 827 |
| 18 | Evidence A Salah | 2404 | True | In your book: Move or match each card; record your explanation and its evidence. | 314 |
| 19 | Evidence B Holy Communion | 2404 | True | In your book: Move or match each card; record your explanation and its evidence. | 314 |
| 20 | Evidence C Vague and precise | 2404 | True | In your book: Move or match each card; record your explanation and its evidence. | 314 |
| 21 | Evidence D Word bank | 2404 | True | In your book: Move or match each card; record your explanation and its evidence. | 314 |

### GROW_RE_A2_W04

| Slide | Title | Notes characters | Staff move | Book line | Answer characters |
|---|---|---:|---|---|---:|
| 1 | Big question: do beliefs make us who we are? | 19632 | True | opening | 68 |
| 2 | Arrival questions 1 and 2 | 6128 | True | In your book: Glue in today's strip; date it. Answer 1 and 2 first. | 1743 |
| 3 | Arrival questions 3 and 4 | 6128 | True | In your book: Glue in today's strip; date it. Answer 1 and 2 first. | 1743 |
| 4 | Words for this lesson | 3272 | True | In your book: Glue in today's strip; date it. Answer 1 and 2 first. | 1743 |
| 5 | Starter | 2060 | True | In your book: Write one response to Choose a big question; use a clue. | 249 |
| 6 | Model question | 2458 | True | In your book: Watch the four model steps. No writing yet. | 437 |
| 7 | Model evidence | 2458 | True | In your book: Watch the four model steps. No writing yet. | 437 |
| 8 | Model explanation | 2619 | True | In your book: Watch the four model steps. No writing yet. | 437 |
| 9 | Model check | 2616 | True | In your book: Watch the four model steps. No writing yet. | 437 |
| 10 | We do | 2411 | True | In your book: Move or match each card; record your explanation and its evidence. | 273 |
| 11 | Shared activity cards | 2192 | True | In your book: Move or match each card; record your explanation and its evidence. | 273 |
| 12 | Apply the learning | 13238 | True | In your book: Write the letter of your answer and one reason. | 2800 |
| 13 | Independent task supported | 3086 | True | In your book: Complete your route's task in your book; use its stem. | 1030 |
| 14 | Independent task standard | 2893 | True | In your book: Complete your route's task in your book; use its stem. | 1030 |
| 15 | Independent task stretch | 2915 | True | In your book: Complete your route's task in your book; use its stem. | 1030 |
| 16 | Review and improve | 1947 | True | In your book: Read back one answer (?); improve it and mark //. | 193 |
| 17 | Exit ticket | 2707 | True | In your book: Answer both questions under today's work. | 933 |
| 18 | Evidence A The big question | 2156 | True | In your book: Move or match each card; record your explanation and its evidence. | 273 |
| 19 | Evidence B Agree | 2156 | True | In your book: Move or match each card; record your explanation and its evidence. | 273 |
| 20 | Evidence C Disagree | 2156 | True | In your book: Move or match each card; record your explanation and its evidence. | 273 |
| 21 | Evidence D Discussion phrases | 2156 | True | In your book: Move or match each card; record your explanation and its evidence. | 273 |

### GROW_RE_A2_W05

| Slide | Title | Notes characters | Staff move | Book line | Answer characters |
|---|---|---:|---|---|---:|
| 1 | Questions for a faith or belief visitor | 20207 | True | opening | 68 |
| 2 | Arrival questions 1 and 2 | 6385 | True | In your book: Glue in today's strip; date it. Answer 1 and 2 first. | 1740 |
| 3 | Arrival questions 3 and 4 | 6385 | True | In your book: Glue in today's strip; date it. Answer 1 and 2 first. | 1740 |
| 4 | Words for this lesson | 3574 | True | In your book: Glue in today's strip; date it. Answer 1 and 2 first. | 1740 |
| 5 | Starter | 2272 | True | In your book: Write one response to Good question or poor question?; use a clue. | 219 |
| 6 | Model question | 3084 | True | In your book: Watch the four model steps. No writing yet. | 564 |
| 7 | Model evidence | 3084 | True | In your book: Watch the four model steps. No writing yet. | 564 |
| 8 | Model explanation | 3254 | True | In your book: Watch the four model steps. No writing yet. | 564 |
| 9 | Model check | 3322 | True | In your book: Watch the four model steps. No writing yet. | 564 |
| 10 | We do | 2929 | True | In your book: Move or match each card; record your explanation and its evidence. | 262 |
| 11 | Shared activity cards | 2460 | True | In your book: Move or match each card; record your explanation and its evidence. | 262 |
| 12 | Apply the learning | 13454 | True | In your book: Write the letter of your answer and one reason. | 2735 |
| 13 | Independent task supported | 3639 | True | In your book: Complete your route's task in your book; use its stem. | 1065 |
| 14 | Independent task standard | 3435 | True | In your book: Complete your route's task in your book; use its stem. | 1065 |
| 15 | Independent task stretch | 3475 | True | In your book: Complete your route's task in your book; use its stem. | 1065 |
| 16 | Review and improve | 2446 | True | In your book: Read back one answer (?); improve it and mark //. | 196 |
| 17 | Exit ticket | 3062 | True | In your book: Answer both questions under today's work. | 937 |
| 18 | Evidence A Good questions | 2627 | True | In your book: Move or match each card; record your explanation and its evidence. | 262 |
| 19 | Evidence B Questions to avoid | 2627 | True | In your book: Move or match each card; record your explanation and its evidence. | 262 |
| 20 | Evidence C A Humanist celebrant | 2627 | True | In your book: Move or match each card; record your explanation and its evidence. | 262 |
| 21 | Evidence D Three areas | 2627 | True | In your book: Move or match each card; record your explanation and its evidence. | 262 |

### GROW_RE_A2_W06

| Slide | Title | Notes characters | Staff move | Book line | Answer characters |
|---|---|---:|---|---|---:|
| 1 | Personal values and respect for others | 20049 | True | opening | 68 |
| 2 | Arrival questions 1 and 2 | 6217 | True | In your book: Glue in today's strip; date it. Answer 1 and 2 first. | 1794 |
| 3 | Arrival questions 3 and 4 | 6217 | True | In your book: Glue in today's strip; date it. Answer 1 and 2 first. | 1794 |
| 4 | Words for this lesson | 3344 | True | In your book: Glue in today's strip; date it. Answer 1 and 2 first. | 1794 |
| 5 | Starter | 2035 | True | In your book: Write one response to Rank for Aaliyah; use a clue. | 156 |
| 6 | Model question | 2528 | True | In your book: Watch the four model steps. No writing yet. | 487 |
| 7 | Model evidence | 2528 | True | In your book: Watch the four model steps. No writing yet. | 487 |
| 8 | Model explanation | 2731 | True | In your book: Watch the four model steps. No writing yet. | 487 |
| 9 | Model check | 2696 | True | In your book: Watch the four model steps. No writing yet. | 487 |
| 10 | We do | 2447 | True | In your book: Move or match each card; record your explanation and its evidence. | 284 |
| 11 | Shared activity cards | 2226 | True | In your book: Move or match each card; record your explanation and its evidence. | 284 |
| 12 | Apply the learning | 13512 | True | In your book: Write the letter of your answer and one reason. | 2869 |
| 13 | Independent task supported | 3194 | True | In your book: Complete your route's task in your book; use its stem. | 1122 |
| 14 | Independent task standard | 2996 | True | In your book: Complete your route's task in your book; use its stem. | 1122 |
| 15 | Independent task stretch | 3042 | True | In your book: Complete your route's task in your book; use its stem. | 1122 |
| 16 | Review and improve | 1947 | True | In your book: Read back one answer (?); improve it and mark //. | 187 |
| 17 | Exit ticket | 2743 | True | In your book: Answer both questions under today's work. | 905 |
| 18 | Evidence A Two priorities | 2164 | True | In your book: Move or match each card; record your explanation and its evidence. | 284 |
| 19 | Evidence B A respectful response | 2164 | True | In your book: Move or match each card; record your explanation and its evidence. | 284 |
| 20 | Evidence C A disrespectful response | 2164 | True | In your book: Move or match each card; record your explanation and its evidence. | 284 |
| 21 | Evidence D Respect is not agreement | 2164 | True | In your book: Move or match each card; record your explanation and its evidence. | 284 |

### GROW_RE_A2_W07

| Slide | Title | Notes characters | Staff move | Book line | Answer characters |
|---|---|---:|---|---|---:|
| 1 | Belief and identity assessment | 21291 | True | opening | 68 |
| 2 | Arrival questions 1 and 2 | 6511 | True | In your book: Glue in today's strip; date it. Answer 1 and 2 first. | 1722 |
| 3 | Arrival questions 3 and 4 | 6511 | True | In your book: Glue in today's strip; date it. Answer 1 and 2 first. | 1722 |
| 4 | Words for this lesson | 3633 | True | In your book: Glue in today's strip; date it. Answer 1 and 2 first. | 1722 |
| 5 | Starter | 2568 | True | In your book: Write one response to Strongest evidence; use a clue. | 290 |
| 6 | Model question | 3340 | True | In your book: Watch the four model steps. No writing yet. | 528 |
| 7 | Model evidence | 3340 | True | In your book: Watch the four model steps. No writing yet. | 528 |
| 8 | Model explanation | 3567 | True | In your book: Watch the four model steps. No writing yet. | 528 |
| 9 | Model check | 3562 | True | In your book: Watch the four model steps. No writing yet. | 528 |
| 10 | We do | 3285 | True | In your book: Move or match each card; record your explanation and its evidence. | 325 |
| 11 | Shared activity cards | 2695 | True | In your book: Move or match each card; record your explanation and its evidence. | 325 |
| 12 | Apply the learning | 14309 | True | In your book: Write the letter of your answer and one reason. | 3026 |
| 13 | Independent task supported | 4018 | True | In your book: Complete your route's task in your book; use its stem. | 1153 |
| 14 | Independent task standard | 3805 | True | In your book: Complete your route's task in your book; use its stem. | 1153 |
| 15 | Independent task stretch | 3810 | True | In your book: Complete your route's task in your book; use its stem. | 1153 |
| 16 | Review and improve | 2730 | True | In your book: Read back one answer (?); improve it and mark //. | 207 |
| 17 | Exit ticket | 3272 | True | In your book: Answer both questions under today's work. | 1041 |
| 18 | Evidence A Using a source | 2994 | True | In your book: Move or match each card; record your explanation and its evidence. | 325 |
| 19 | Evidence B Sample question | 2994 | True | In your book: Move or match each card; record your explanation and its evidence. | 325 |
| 20 | Evidence C Sample evidence | 2994 | True | In your book: Move or match each card; record your explanation and its evidence. | 325 |
| 21 | Evidence D This term | 2994 | True | In your book: Move or match each card; record your explanation and its evidence. | 325 |
| 22 | Evidence E1 Assessment source Rama and Sita | 2994 | True | In your book: Move or match each card; record your explanation and its evidence. | 325 |
| 23 | Evidence E2 Assessment source Practices | 2994 | True | In your book: Move or match each card; record your explanation and its evidence. | 325 |
| 24 | Evidence E3 Assessment source The oil | 2994 | True | In your book: Move or match each card; record your explanation and its evidence. | 325 |
| 25 | Evidence E4 Assessment source Hanukkah today | 2994 | True | In your book: Move or match each card; record your explanation and its evidence. | 325 |

### LAUNCH_RE_A1_W08

| Slide | Title | Notes characters | Staff move | Book line | Answer characters |
|---|---|---:|---|---|---:|
| 1 | Evidence, belief and choices | 12505 | True | opening | 262 |
| 2 | Arrival task | 1730 | True | In your book: Glue in today’s strip; date it. Answer questions 1 to 4. | 1391 |
| 3 | Start the enquiry | 616 | True | In your book: Number 1 to 3. Write one precise answer for each. | 291 |
| 4 | I do · a worked method | 832 | True | In your book: Watch how relevant evidence supports a point. No writing yet. | 493 |
| 5 | Captioned model | 832 | True | In your book: Watch how relevant evidence supports a point. No writing yet. | 493 |
| 6 | We do · source detective | 586 | True | In your book: Match evidence to an influence; explain one link. | 262 |
| 7 | Check the idea | 2305 | True | In your book: Write the letter of your answer. Explain one clue. | 1983 |
| 8 | Independent book check | 2019 | True | In your book: Answer 1 to 5 briefly; use point, evidence and explanation for 6. | 1674 |
| 9 | Sources for your comparison | 2019 | True | In your book: Answer 1 to 5 briefly; use point, evidence and explanation for 6. | 1674 |
| 10 | Supported | 2019 | True | In your book: Answer 1 to 5 briefly; use point, evidence and explanation for 6. | 1674 |
| 11 | Supported · continued | 2019 | True | In your book: Answer 1 to 5 briefly; use point, evidence and explanation for 6. | 1674 |
| 12 | Standard | 2019 | True | In your book: Answer 1 to 5 briefly; use point, evidence and explanation for 6. | 1674 |
| 13 | Standard · continued | 2019 | True | In your book: Answer 1 to 5 briefly; use point, evidence and explanation for 6. | 1674 |
| 14 | Stretch | 2019 | True | In your book: Answer 1 to 5 briefly; use point, evidence and explanation for 6. | 1674 |
| 15 | Stretch · continued | 2019 | True | In your book: Answer 1 to 5 briefly; use point, evidence and explanation for 6. | 1674 |
| 16 | Review and improve | 550 | True | In your book: Read back one answer (?); improve it and mark //. | 224 |
| 17 | Exit ticket | 683 | True | In your book: Explain one belief-to-choice link using relevant evidence. | 206 |

### LAUNCH_RE_A2_W01

| Slide | Title | Notes characters | Staff move | Book line | Answer characters |
|---|---|---:|---|---|---:|
| 1 | Worship, prayer and practice | 19922 | True | opening | 68 |
| 2 | Arrival questions 1 and 2 | 6465 | True | In your book: Glue in today's strip; date it. Answer 1 and 2 first. | 1773 |
| 3 | Arrival questions 3 and 4 | 6465 | True | In your book: Glue in today's strip; date it. Answer 1 and 2 first. | 1773 |
| 4 | Words for this lesson | 3608 | True | In your book: Glue in today's strip; date it. Answer 1 and 2 first. | 1773 |
| 5 | Starter | 2254 | True | In your book: Write one response to Worship, prayer or reflection?; use a clue. | 197 |
| 6 | Model question | 3110 | True | In your book: Watch the four model steps. No writing yet. | 704 |
| 7 | Model evidence | 3110 | True | In your book: Watch the four model steps. No writing yet. | 704 |
| 8 | Model explanation | 3358 | True | In your book: Watch the four model steps. No writing yet. | 704 |
| 9 | Model check | 3280 | True | In your book: Watch the four model steps. No writing yet. | 704 |
| 10 | We do | 2729 | True | In your book: Move or match each card; record your explanation and its evidence. | 212 |
| 11 | Shared activity cards | 2371 | True | In your book: Move or match each card; record your explanation and its evidence. | 212 |
| 12 | Apply the learning | 13402 | True | In your book: Write the letter of your answer and one reason. | 2837 |
| 13 | Independent task supported | 3433 | True | In your book: Complete your route's task in your book; use its stem. | 1030 |
| 14 | Independent task standard | 3258 | True | In your book: Complete your route's task in your book; use its stem. | 1030 |
| 15 | Independent task stretch | 3322 | True | In your book: Complete your route's task in your book; use its stem. | 1030 |
| 16 | Review and improve | 2304 | True | In your book: Read back one answer (?); improve it and mark //. | 194 |
| 17 | Exit ticket | 2993 | True | In your book: Answer both questions under today's work. | 865 |
| 18 | Evidence A Salah | 2446 | True | In your book: Move or match each card; record your explanation and its evidence. | 212 |
| 19 | Evidence B Christian prayer | 2446 | True | In your book: Move or match each card; record your explanation and its evidence. | 212 |
| 20 | Evidence C Non-religious reflection | 2446 | True | In your book: Move or match each card; record your explanation and its evidence. | 212 |
| 21 | Evidence D Purposes | 2446 | True | In your book: Move or match each card; record your explanation and its evidence. | 212 |

### LAUNCH_RE_A2_W02

| Slide | Title | Notes characters | Staff move | Book line | Answer characters |
|---|---|---:|---|---|---:|
| 1 | Pilgrimage and sacred places | 20273 | True | opening | 68 |
| 2 | Arrival questions 1 and 2 | 6747 | True | In your book: Glue in today's strip; date it. Answer 1 and 2 first. | 1950 |
| 3 | Arrival questions 3 and 4 | 6747 | True | In your book: Glue in today's strip; date it. Answer 1 and 2 first. | 1950 |
| 4 | Words for this lesson | 3665 | True | In your book: Glue in today's strip; date it. Answer 1 and 2 first. | 1950 |
| 5 | Starter | 2516 | True | In your book: Write one response to A fictional person’s memory; use a clue. | 384 |
| 6 | Model question | 2908 | True | In your book: Watch the four model steps. No writing yet. | 587 |
| 7 | Model evidence | 2908 | True | In your book: Watch the four model steps. No writing yet. | 587 |
| 8 | Model explanation | 3192 | True | In your book: Watch the four model steps. No writing yet. | 587 |
| 9 | Model check | 3032 | True | In your book: Watch the four model steps. No writing yet. | 587 |
| 10 | We do | 2544 | True | In your book: Move or match each card; record your explanation and its evidence. | 143 |
| 11 | Shared activity cards | 2103 | True | In your book: Move or match each card; record your explanation and its evidence. | 143 |
| 12 | Apply the learning | 13752 | True | In your book: Write the letter of your answer and one reason. | 2885 |
| 13 | Independent task supported | 3286 | True | In your book: Complete your route's task in your book; use its stem. | 967 |
| 14 | Independent task standard | 3111 | True | In your book: Complete your route's task in your book; use its stem. | 967 |
| 15 | Independent task stretch | 3135 | True | In your book: Complete your route's task in your book; use its stem. | 967 |
| 16 | Review and improve | 2234 | True | In your book: Read back one answer (?); improve it and mark //. | 221 |
| 17 | Exit ticket | 2952 | True | In your book: Answer both questions under today's work. | 937 |
| 18 | Evidence A Hajj | 2270 | True | In your book: Move or match each card; record your explanation and its evidence. | 143 |
| 19 | Evidence B Why Hajj matters | 2270 | True | In your book: Move or match each card; record your explanation and its evidence. | 143 |
| 20 | Evidence C Lourdes | 2270 | True | In your book: Move or match each card; record your explanation and its evidence. | 143 |
| 21 | Evidence D Place → action → meaning | 2270 | True | In your book: Move or match each card; record your explanation and its evidence. | 143 |

### LAUNCH_RE_A2_W03

| Slide | Title | Notes characters | Staff move | Book line | Answer characters |
|---|---|---:|---|---|---:|
| 1 | Rites of passage and community | 20713 | True | opening | 68 |
| 2 | Arrival questions 1 and 2 | 7041 | True | In your book: Glue in today's strip; date it. Answer 1 and 2 first. | 1887 |
| 3 | Arrival questions 3 and 4 | 7041 | True | In your book: Glue in today's strip; date it. Answer 1 and 2 first. | 1887 |
| 4 | Words for this lesson | 3962 | True | In your book: Glue in today's strip; date it. Answer 1 and 2 first. | 1887 |
| 5 | Starter | 2513 | True | In your book: Write one response to Order the life events; use a clue. | 167 |
| 6 | Model question | 3243 | True | In your book: Watch the four model steps. No writing yet. | 405 |
| 7 | Model evidence | 3243 | True | In your book: Watch the four model steps. No writing yet. | 405 |
| 8 | Model explanation | 3416 | True | In your book: Watch the four model steps. No writing yet. | 405 |
| 9 | Model check | 3419 | True | In your book: Watch the four model steps. No writing yet. | 405 |
| 10 | We do | 3170 | True | In your book: Move or match each card; record your explanation and its evidence. | 187 |
| 11 | Shared activity cards | 2586 | True | In your book: Move or match each card; record your explanation and its evidence. | 187 |
| 12 | Apply the learning | 14379 | True | In your book: Write the letter of your answer and one reason. | 3053 |
| 13 | Independent task supported | 3843 | True | In your book: Complete your route's task in your book; use its stem. | 972 |
| 14 | Independent task standard | 3668 | True | In your book: Complete your route's task in your book; use its stem. | 972 |
| 15 | Independent task stretch | 3691 | True | In your book: Complete your route's task in your book; use its stem. | 972 |
| 16 | Review and improve | 2789 | True | In your book: Read back one answer (?); improve it and mark //. | 222 |
| 17 | Exit ticket | 3457 | True | In your book: Answer both questions under today's work. | 1039 |
| 18 | Evidence A Bar and Bat Mitzvah | 2903 | True | In your book: Move or match each card; record your explanation and its evidence. | 187 |
| 19 | Evidence B Confirmation | 2903 | True | In your book: Move or match each card; record your explanation and its evidence. | 187 |
| 20 | Evidence C A Humanist naming ceremony | 2903 | True | In your book: Move or match each card; record your explanation and its evidence. | 187 |
| 21 | Evidence D Three questions | 2903 | True | In your book: Move or match each card; record your explanation and its evidence. | 187 |

### LAUNCH_RE_A2_W04

| Slide | Title | Notes characters | Staff move | Book line | Answer characters |
|---|---|---:|---|---|---:|
| 1 | Moral teachings across worldviews | 20880 | True | opening | 68 |
| 2 | Arrival questions 1 and 2 | 6362 | True | In your book: Glue in today's strip; date it. Answer 1 and 2 first. | 1782 |
| 3 | Arrival questions 3 and 4 | 6362 | True | In your book: Glue in today's strip; date it. Answer 1 and 2 first. | 1782 |
| 4 | Words for this lesson | 3522 | True | In your book: Glue in today's strip; date it. Answer 1 and 2 first. | 1782 |
| 5 | Starter | 2371 | True | In your book: Write one response to A fictional pupil’s dilemma; use a clue. | 205 |
| 6 | Model question | 3006 | True | In your book: Watch the four model steps. No writing yet. | 628 |
| 7 | Model evidence | 3006 | True | In your book: Watch the four model steps. No writing yet. | 628 |
| 8 | Model explanation | 3182 | True | In your book: Watch the four model steps. No writing yet. | 628 |
| 9 | Model check | 3214 | True | In your book: Watch the four model steps. No writing yet. | 628 |
| 10 | We do | 2841 | True | In your book: Move or match each card; record your explanation and its evidence. | 334 |
| 11 | Shared activity cards | 2531 | True | In your book: Move or match each card; record your explanation and its evidence. | 334 |
| 12 | Apply the learning | 13978 | True | In your book: Write the letter of your answer and one reason. | 3010 |
| 13 | Independent task supported | 3648 | True | In your book: Complete your route's task in your book; use its stem. | 1241 |
| 14 | Independent task standard | 3473 | True | In your book: Complete your route's task in your book; use its stem. | 1241 |
| 15 | Independent task stretch | 3516 | True | In your book: Complete your route's task in your book; use its stem. | 1241 |
| 16 | Review and improve | 2319 | True | In your book: Read back one answer (?); improve it and mark //. | 213 |
| 17 | Exit ticket | 3219 | True | In your book: Answer both questions under today's work. | 1119 |
| 18 | Evidence A A Christian teaching | 2575 | True | In your book: Move or match each card; record your explanation and its evidence. | 334 |
| 19 | Evidence B A Humanist principle | 2575 | True | In your book: Move or match each card; record your explanation and its evidence. | 334 |
| 20 | Evidence C The dilemma | 2575 | True | In your book: Move or match each card; record your explanation and its evidence. | 334 |
| 21 | Evidence D People differ | 2575 | True | In your book: Move or match each card; record your explanation and its evidence. | 334 |

### LAUNCH_RE_A2_W05

| Slide | Title | Notes characters | Staff move | Book line | Answer characters |
|---|---|---:|---|---|---:|
| 1 | Comparing responses to a life question | 21294 | True | opening | 68 |
| 2 | Arrival questions 1 and 2 | 6633 | True | In your book: Glue in today's strip; date it. Answer 1 and 2 first. | 1824 |
| 3 | Arrival questions 3 and 4 | 6633 | True | In your book: Glue in today's strip; date it. Answer 1 and 2 first. | 1824 |
| 4 | Words for this lesson | 3679 | True | In your book: Glue in today's strip; date it. Answer 1 and 2 first. | 1824 |
| 5 | Starter | 2403 | True | In your book: Write one response to Choose a big question; use a clue. | 283 |
| 6 | Model question | 3384 | True | In your book: Watch the four model steps. No writing yet. | 906 |
| 7 | Model evidence | 3384 | True | In your book: Watch the four model steps. No writing yet. | 906 |
| 8 | Model evidence continued | 3481 | True | In your book: Watch the four model steps. No writing yet. | 906 |
| 9 | Model explanation | 3604 | True | In your book: Watch the four model steps. No writing yet. | 906 |
| 10 | Model check | 3554 | True | In your book: Watch the four model steps. No writing yet. | 906 |
| 11 | We do | 2849 | True | In your book: Move or match each card; record your explanation and its evidence. | 311 |
| 12 | Shared activity cards | 2576 | True | In your book: Move or match each card; record your explanation and its evidence. | 311 |
| 13 | Apply the learning | 14445 | True | In your book: Write the letter of your answer and one reason. | 3133 |
| 14 | Independent task supported | 3678 | True | In your book: Complete your route's task in your book; use its stem. | 1207 |
| 15 | Independent task standard | 3503 | True | In your book: Complete your route's task in your book; use its stem. | 1207 |
| 16 | Independent task stretch | 3515 | True | In your book: Complete your route's task in your book; use its stem. | 1207 |
| 17 | Review and improve | 2392 | True | In your book: Read back one answer (?); improve it and mark //. | 214 |
| 18 | Exit ticket | 3202 | True | In your book: Answer both questions under today's work. | 1069 |
| 19 | Evidence A The question | 2576 | True | In your book: Move or match each card; record your explanation and its evidence. | 311 |
| 20 | Evidence B A Muslim response | 2576 | True | In your book: Move or match each card; record your explanation and its evidence. | 311 |
| 21 | Evidence C A Humanist response | 2576 | True | In your book: Move or match each card; record your explanation and its evidence. | 311 |
| 22 | Evidence D Comparing ideas, not people | 2576 | True | In your book: Move or match each card; record your explanation and its evidence. | 311 |

### LAUNCH_RE_A2_W06

| Slide | Title | Notes characters | Staff move | Book line | Answer characters |
|---|---|---:|---|---|---:|
| 1 | A structured “compare” response | 21406 | True | opening | 68 |
| 2 | Arrival questions 1 and 2 | 7338 | True | In your book: Glue in today's strip; date it. Answer 1 and 2 first. | 2103 |
| 3 | Arrival questions 3 and 4 | 7338 | True | In your book: Glue in today's strip; date it. Answer 1 and 2 first. | 2103 |
| 4 | Words for this lesson | 4106 | True | In your book: Glue in today's strip; date it. Answer 1 and 2 first. | 2103 |
| 5 | Starter | 2454 | True | In your book: Write one response to Describe or compare?; use a clue. | 249 |
| 6 | Model question | 3104 | True | In your book: Watch the four model steps. No writing yet. | 412 |
| 7 | Model evidence | 3104 | True | In your book: Watch the four model steps. No writing yet. | 412 |
| 8 | Model explanation | 3220 | True | In your book: Watch the four model steps. No writing yet. | 412 |
| 9 | Model check | 3272 | True | In your book: Watch the four model steps. No writing yet. | 412 |
| 10 | We do | 3327 | True | In your book: Move or match each card; record your explanation and its evidence. | 516 |
| 11 | Shared activity cards | 3130 | True | In your book: Move or match each card; record your explanation and its evidence. | 516 |
| 12 | Apply the learning | 14201 | True | In your book: Write the letter of your answer and one reason. | 2978 |
| 13 | Independent task supported | 4286 | True | In your book: Complete your route's task in your book; use its stem. | 1556 |
| 14 | Independent task standard | 4111 | True | In your book: Complete your route's task in your book; use its stem. | 1556 |
| 15 | Independent task stretch | 4139 | True | In your book: Complete your route's task in your book; use its stem. | 1556 |
| 16 | Review and improve | 2647 | True | In your book: Read back one answer (?); improve it and mark //. | 207 |
| 17 | Exit ticket | 3219 | True | In your book: Answer both questions under today's work. | 937 |
| 18 | Evidence A Describe or compare? | 3065 | True | In your book: Move or match each card; record your explanation and its evidence. | 516 |
| 19 | Evidence B The structure | 3065 | True | In your book: Move or match each card; record your explanation and its evidence. | 516 |
| 20 | Evidence C A weak comparison | 3065 | True | In your book: Move or match each card; record your explanation and its evidence. | 516 |
| 21 | Evidence D A model comparison | 3065 | True | In your book: Move or match each card; record your explanation and its evidence. | 516 |

### LAUNCH_RE_A2_W07

| Slide | Title | Notes characters | Staff move | Book line | Answer characters |
|---|---|---:|---|---|---:|
| 1 | Beliefs and practices assessment | 22721 | True | opening | 68 |
| 2 | Arrival questions 1 and 2 | 7885 | True | In your book: Glue in today's strip; date it. Answer 1 and 2 first. | 1998 |
| 3 | Arrival questions 3 and 4 | 7885 | True | In your book: Glue in today's strip; date it. Answer 1 and 2 first. | 1998 |
| 4 | Words for this lesson | 4728 | True | In your book: Glue in today's strip; date it. Answer 1 and 2 first. | 1998 |
| 5 | Starter | 3268 | True | In your book: Write one response to Belief, practice or meaning?; use a clue. | 248 |
| 6 | Model question | 4222 | True | In your book: Watch the four model steps. No writing yet. | 563 |
| 7 | Model evidence | 4222 | True | In your book: Watch the four model steps. No writing yet. | 563 |
| 8 | Model explanation | 4443 | True | In your book: Watch the four model steps. No writing yet. | 563 |
| 9 | Model check | 4430 | True | In your book: Watch the four model steps. No writing yet. | 563 |
| 10 | We do | 3977 | True | In your book: Move or match each card; record your explanation and its evidence. | 205 |
| 11 | Shared activity cards | 3271 | True | In your book: Move or match each card; record your explanation and its evidence. | 205 |
| 12 | Apply the learning | 15519 | True | In your book: Write the letter of your answer and one reason. | 3089 |
| 13 | Independent task supported | 4915 | True | In your book: Complete your route's task in your book; use its stem. | 1231 |
| 14 | Independent task standard | 4740 | True | In your book: Complete your route's task in your book; use its stem. | 1231 |
| 15 | Independent task stretch | 4751 | True | In your book: Complete your route's task in your book; use its stem. | 1231 |
| 16 | Review and improve | 3581 | True | In your book: Read back one answer (?); improve it and mark //. | 209 |
| 17 | Exit ticket | 4507 | True | In your book: Answer both questions under today's work. | 1389 |
| 18 | Evidence A The assessment question | 3720 | True | In your book: Move or match each card; record your explanation and its evidence. | 205 |
| 19 | Evidence B Belief, practice, meaning | 3720 | True | In your book: Move or match each card; record your explanation and its evidence. | 205 |
| 20 | Evidence C Evidence bank | 3720 | True | In your book: Move or match each card; record your explanation and its evidence. | 205 |
| 21 | Evidence D Routes | 3720 | True | In your book: Move or match each card; record your explanation and its evidence. | 205 |
| 22 | Evidence E1 Assessment source Salah | 3720 | True | In your book: Move or match each card; record your explanation and its evidence. | 205 |
| 23 | Evidence E2 Assessment source Non-religious reflection | 3720 | True | In your book: Move or match each card; record your explanation and its evidence. | 205 |

## Complete staff-section matrix


### Staff document checks — BUILD_RE_A1_W08

Static checks against the final lesson staff content. Every source paragraph and table cell survives on all four required staff surfaces; whitespace-only PDF line wrapping is ignored.

| Field | Teacher Notes Word | Word pack | Teacher Notes PDF | TA brief PDF |
|---|---|---|---|---|
| Teacher card | PASS | PASS | PASS | PASS |
| Forty minute route | PASS | PASS | PASS | PASS |
| Preparation | PASS | PASS | PASS | PASS |
| Access and regulation | PASS | PASS | PASS | PASS |
| Assessment | PASS | PASS | PASS | PASS |
| First lesson back · staff card | PASS | PASS | PASS | PASS |
| Book scan | PASS | PASS | PASS | PASS |
| Ask cover staff and TAs | PASS | PASS | PASS | PASS |
| Once-only return line | PASS | PASS | PASS | PASS |
| Today | PASS | PASS | PASS | PASS |
| Private RAG rule | PASS | PASS | PASS | PASS |
| What the check feeds into | PASS | PASS | PASS | PASS |
| Planned adaptations | PASS | PASS | PASS | PASS |
| Invite a response · two per route | PASS | PASS | PASS | PASS |
| Target opportunities | PASS | PASS | PASS | PASS |
| Book evidence and feedback | PASS | PASS | PASS | PASS |
| Teaching sequence | PASS | PASS | PASS | PASS |
| Model and answers | PASS | PASS | PASS | PASS |
| Arrival questions and answers | PASS | PASS | PASS | PASS |
| Starter answers | PASS | PASS | PASS | PASS |
| Shared activity reasoning | PASS | PASS | PASS | PASS |
| Hinge and diagnoses | PASS | PASS | PASS | PASS |
| Parallel hinge after a teaching move | PASS | PASS | PASS | PASS |
| If time is short | PASS | PASS | PASS | PASS |
| Planning and evaluation record | PASS | PASS | PASS | PASS |
| Individual check answers and source map | PASS | PASS | PASS | PASS |
| Exit guidance | PASS | PASS | PASS | PASS |
| F6 exact preparation | PASS | PASS | PASS | PASS |
| F8 full IEDP line | PASS | PASS | PASS | PASS |
| F8 EAL is not SEN | PASS | PASS | PASS | PASS |
| F8 Supported 1/2 Standard 1/2 Stretch 1/2 | PASS | PASS | PASS | PASS |
| A4 geometry | PASS | PASS | PASS | PASS |

| Surface | Characters | Missing source chunks | Banned words | Author |
|---|---:|---:|---:|---|
| Teacher_Notes.docx | 9765 | 0 | 0 | Matt Roper |
| Editable_Pack.docx | 15563 | 0 | 0 | Matt Roper |
| Teacher_Notes.pdf | 9765 | 0 | 0 | Matt Roper |
| TA_Brief.pdf | 9765 | 0 | 0 | Matt Roper |

Planned adaptations table: 5 body rows; 2 columns. Invite a response table: 6 body rows; 3 columns.
Word pack: F3 is an exact heading; organiser comes first; 5 real page breaks; 16 embedded pictures/logos.

The E-number labels immediately followed by “Assessment source” are evidence-card identifiers and are exempt from the version-word scan.

All DOCX files were rendered through LibreOffice; representative page images were inspected. Full reviewer Office and print checks remain separate from these static checks.


### Staff document checks — BUILD_RE_A2_W01

Static checks against the final lesson staff content. Every source paragraph and table cell survives on all four required staff surfaces; whitespace-only PDF line wrapping is ignored.

| Field | Teacher Notes Word | Word pack | Teacher Notes PDF | TA brief PDF |
|---|---|---|---|---|
| Teacher card | PASS | PASS | PASS | PASS |
| Forty minute route | PASS | PASS | PASS | PASS |
| Preparation | PASS | PASS | PASS | PASS |
| Access and regulation | PASS | PASS | PASS | PASS |
| Assessment | PASS | PASS | PASS | PASS |
| Model and answers | PASS | PASS | PASS | PASS |
| Arrival answers | PASS | PASS | PASS | PASS |
| Shared activity reasoning | PASS | PASS | PASS | PASS |
| Exit responses | PASS | PASS | PASS | PASS |
| Teaching and evidence record | PASS | PASS | PASS | PASS |
| Look for | PASS | PASS | PASS | PASS |
| Media | PASS | PASS | PASS | PASS |
| Source credits | PASS | PASS | PASS | PASS |
| Planning | PASS | PASS | PASS | PASS |
| Teaching sequence | PASS | PASS | PASS | PASS |
| Arrival questions and answers | PASS | PASS | PASS | PASS |
| Hinge and diagnoses | PASS | PASS | PASS | PASS |
| Parallel hinge after a teaching move | PASS | PASS | PASS | PASS |
| LOOP | PASS | PASS | PASS | PASS |
| Target opportunities | PASS | PASS | PASS | PASS |
| Exit guidance | PASS | PASS | PASS | PASS |
| If behind | PASS | PASS | PASS | PASS |
| Planning and evaluation record | PASS | PASS | PASS | PASS |
| Sources | PASS | PASS | PASS | PASS |
| Book evidence and feedback | PASS | PASS | PASS | PASS |
| Planned adaptations | PASS | PASS | PASS | PASS |
| Invite a response · two per route | PASS | PASS | PASS | PASS |
| F6 exact preparation | PASS | PASS | PASS | PASS |
| F8 full IEDP line | PASS | PASS | PASS | PASS |
| F8 EAL is not SEN | PASS | PASS | PASS | PASS |
| F8 Supported 1/2 Standard 1/2 Stretch 1/2 | PASS | PASS | PASS | PASS |
| A4 geometry | PASS | PASS | PASS | PASS |

| Surface | Characters | Missing source chunks | Banned words | Author |
|---|---:|---:|---:|---|
| Teacher_Notes.docx | 18292 | 0 | 0 | Matt Roper |
| Editable_Pack.docx | 27260 | 0 | 0 | Matt Roper |
| Teacher_Notes.pdf | 18292 | 0 | 0 | Matt Roper |
| TA_Brief.pdf | 18292 | 0 | 0 | Matt Roper |

Planned adaptations table: 5 body rows; 2 columns. Invite a response table: 6 body rows; 3 columns.
Word pack: F3 is an exact heading; organiser comes first; 5 real page breaks; 13 embedded pictures/logos.

The E-number labels immediately followed by “Assessment source” are evidence-card identifiers and are exempt from the version-word scan.

All DOCX files were rendered through LibreOffice; representative page images were inspected. Full reviewer Office and print checks remain separate from these static checks.


### Staff document checks — BUILD_RE_A2_W02

Static checks against the final lesson staff content. Every source paragraph and table cell survives on all four required staff surfaces; whitespace-only PDF line wrapping is ignored.

| Field | Teacher Notes Word | Word pack | Teacher Notes PDF | TA brief PDF |
|---|---|---|---|---|
| Teacher card | PASS | PASS | PASS | PASS |
| Forty minute route | PASS | PASS | PASS | PASS |
| Preparation | PASS | PASS | PASS | PASS |
| Access and regulation | PASS | PASS | PASS | PASS |
| Assessment | PASS | PASS | PASS | PASS |
| Model and answers | PASS | PASS | PASS | PASS |
| Arrival answers | PASS | PASS | PASS | PASS |
| Shared activity reasoning | PASS | PASS | PASS | PASS |
| Exit responses | PASS | PASS | PASS | PASS |
| Teaching and evidence record | PASS | PASS | PASS | PASS |
| Look for | PASS | PASS | PASS | PASS |
| Media | PASS | PASS | PASS | PASS |
| Source credits | PASS | PASS | PASS | PASS |
| Planning | PASS | PASS | PASS | PASS |
| Teaching sequence | PASS | PASS | PASS | PASS |
| Arrival questions and answers | PASS | PASS | PASS | PASS |
| Hinge and diagnoses | PASS | PASS | PASS | PASS |
| Parallel hinge after a teaching move | PASS | PASS | PASS | PASS |
| LOOP | PASS | PASS | PASS | PASS |
| Target opportunities | PASS | PASS | PASS | PASS |
| Exit guidance | PASS | PASS | PASS | PASS |
| If behind | PASS | PASS | PASS | PASS |
| Planning and evaluation record | PASS | PASS | PASS | PASS |
| Sources | PASS | PASS | PASS | PASS |
| Book evidence and feedback | PASS | PASS | PASS | PASS |
| Planned adaptations | PASS | PASS | PASS | PASS |
| Invite a response · two per route | PASS | PASS | PASS | PASS |
| F6 exact preparation | PASS | PASS | PASS | PASS |
| F8 full IEDP line | PASS | PASS | PASS | PASS |
| F8 EAL is not SEN | PASS | PASS | PASS | PASS |
| F8 Supported 1/2 Standard 1/2 Stretch 1/2 | PASS | PASS | PASS | PASS |
| A4 geometry | PASS | PASS | PASS | PASS |

| Surface | Characters | Missing source chunks | Banned words | Author |
|---|---:|---:|---:|---|
| Teacher_Notes.docx | 19199 | 0 | 0 | Matt Roper |
| Editable_Pack.docx | 28432 | 0 | 0 | Matt Roper |
| Teacher_Notes.pdf | 19239 | 0 | 0 | Matt Roper |
| TA_Brief.pdf | 19239 | 0 | 0 | Matt Roper |

Planned adaptations table: 5 body rows; 2 columns. Invite a response table: 6 body rows; 3 columns.
Word pack: F3 is an exact heading; organiser comes first; 5 real page breaks; 13 embedded pictures/logos.

The E-number labels immediately followed by “Assessment source” are evidence-card identifiers and are exempt from the version-word scan.

All DOCX files were rendered through LibreOffice; representative page images were inspected. Full reviewer Office and print checks remain separate from these static checks.


### Staff document checks — BUILD_RE_A2_W03

Static checks against the final lesson staff content. Every source paragraph and table cell survives on all four required staff surfaces; whitespace-only PDF line wrapping is ignored.

| Field | Teacher Notes Word | Word pack | Teacher Notes PDF | TA brief PDF |
|---|---|---|---|---|
| Teacher card | PASS | PASS | PASS | PASS |
| Forty minute route | PASS | PASS | PASS | PASS |
| Preparation | PASS | PASS | PASS | PASS |
| Access and regulation | PASS | PASS | PASS | PASS |
| Assessment | PASS | PASS | PASS | PASS |
| Model and answers | PASS | PASS | PASS | PASS |
| Arrival answers | PASS | PASS | PASS | PASS |
| Shared activity reasoning | PASS | PASS | PASS | PASS |
| Exit responses | PASS | PASS | PASS | PASS |
| Teaching and evidence record | PASS | PASS | PASS | PASS |
| Look for | PASS | PASS | PASS | PASS |
| Media | PASS | PASS | PASS | PASS |
| Source credits | PASS | PASS | PASS | PASS |
| Planning | PASS | PASS | PASS | PASS |
| Teaching sequence | PASS | PASS | PASS | PASS |
| Arrival questions and answers | PASS | PASS | PASS | PASS |
| Hinge and diagnoses | PASS | PASS | PASS | PASS |
| Parallel hinge after a teaching move | PASS | PASS | PASS | PASS |
| LOOP | PASS | PASS | PASS | PASS |
| Target opportunities | PASS | PASS | PASS | PASS |
| Exit guidance | PASS | PASS | PASS | PASS |
| If behind | PASS | PASS | PASS | PASS |
| Planning and evaluation record | PASS | PASS | PASS | PASS |
| Sources | PASS | PASS | PASS | PASS |
| Book evidence and feedback | PASS | PASS | PASS | PASS |
| Planned adaptations | PASS | PASS | PASS | PASS |
| Invite a response · two per route | PASS | PASS | PASS | PASS |
| F6 exact preparation | PASS | PASS | PASS | PASS |
| F8 full IEDP line | PASS | PASS | PASS | PASS |
| F8 EAL is not SEN | PASS | PASS | PASS | PASS |
| F8 Supported 1/2 Standard 1/2 Stretch 1/2 | PASS | PASS | PASS | PASS |
| A4 geometry | PASS | PASS | PASS | PASS |

| Surface | Characters | Missing source chunks | Banned words | Author |
|---|---:|---:|---:|---|
| Teacher_Notes.docx | 18637 | 0 | 0 | Matt Roper |
| Editable_Pack.docx | 27913 | 0 | 0 | Matt Roper |
| Teacher_Notes.pdf | 18637 | 0 | 0 | Matt Roper |
| TA_Brief.pdf | 18637 | 0 | 0 | Matt Roper |

Planned adaptations table: 5 body rows; 2 columns. Invite a response table: 6 body rows; 3 columns.
Word pack: F3 is an exact heading; organiser comes first; 5 real page breaks; 13 embedded pictures/logos.

The E-number labels immediately followed by “Assessment source” are evidence-card identifiers and are exempt from the version-word scan.

All DOCX files were rendered through LibreOffice; representative page images were inspected. Full reviewer Office and print checks remain separate from these static checks.


### Staff document checks — BUILD_RE_A2_W04

Static checks against the final lesson staff content. Every source paragraph and table cell survives on all four required staff surfaces; whitespace-only PDF line wrapping is ignored.

| Field | Teacher Notes Word | Word pack | Teacher Notes PDF | TA brief PDF |
|---|---|---|---|---|
| Teacher card | PASS | PASS | PASS | PASS |
| Forty minute route | PASS | PASS | PASS | PASS |
| Preparation | PASS | PASS | PASS | PASS |
| Access and regulation | PASS | PASS | PASS | PASS |
| Assessment | PASS | PASS | PASS | PASS |
| Model and answers | PASS | PASS | PASS | PASS |
| Arrival answers | PASS | PASS | PASS | PASS |
| Shared activity reasoning | PASS | PASS | PASS | PASS |
| Exit responses | PASS | PASS | PASS | PASS |
| Teaching and evidence record | PASS | PASS | PASS | PASS |
| Look for | PASS | PASS | PASS | PASS |
| Media | PASS | PASS | PASS | PASS |
| Source credits | PASS | PASS | PASS | PASS |
| Planning | PASS | PASS | PASS | PASS |
| Teaching sequence | PASS | PASS | PASS | PASS |
| Arrival questions and answers | PASS | PASS | PASS | PASS |
| Hinge and diagnoses | PASS | PASS | PASS | PASS |
| Parallel hinge after a teaching move | PASS | PASS | PASS | PASS |
| LOOP | PASS | PASS | PASS | PASS |
| Target opportunities | PASS | PASS | PASS | PASS |
| Exit guidance | PASS | PASS | PASS | PASS |
| If behind | PASS | PASS | PASS | PASS |
| Planning and evaluation record | PASS | PASS | PASS | PASS |
| Sources | PASS | PASS | PASS | PASS |
| Book evidence and feedback | PASS | PASS | PASS | PASS |
| Planned adaptations | PASS | PASS | PASS | PASS |
| Invite a response · two per route | PASS | PASS | PASS | PASS |
| F6 exact preparation | PASS | PASS | PASS | PASS |
| F8 full IEDP line | PASS | PASS | PASS | PASS |
| F8 EAL is not SEN | PASS | PASS | PASS | PASS |
| F8 Supported 1/2 Standard 1/2 Stretch 1/2 | PASS | PASS | PASS | PASS |
| A4 geometry | PASS | PASS | PASS | PASS |

| Surface | Characters | Missing source chunks | Banned words | Author |
|---|---:|---:|---:|---|
| Teacher_Notes.docx | 19254 | 0 | 0 | Matt Roper |
| Editable_Pack.docx | 28504 | 0 | 0 | Matt Roper |
| Teacher_Notes.pdf | 19294 | 0 | 0 | Matt Roper |
| TA_Brief.pdf | 19294 | 0 | 0 | Matt Roper |

Planned adaptations table: 5 body rows; 2 columns. Invite a response table: 6 body rows; 3 columns.
Word pack: F3 is an exact heading; organiser comes first; 5 real page breaks; 13 embedded pictures/logos.

The E-number labels immediately followed by “Assessment source” are evidence-card identifiers and are exempt from the version-word scan.

All DOCX files were rendered through LibreOffice; representative page images were inspected. Full reviewer Office and print checks remain separate from these static checks.


### Staff document checks — BUILD_RE_A2_W05

Static checks against the final lesson staff content. Every source paragraph and table cell survives on all four required staff surfaces; whitespace-only PDF line wrapping is ignored.

| Field | Teacher Notes Word | Word pack | Teacher Notes PDF | TA brief PDF |
|---|---|---|---|---|
| Teacher card | PASS | PASS | PASS | PASS |
| Forty minute route | PASS | PASS | PASS | PASS |
| Preparation | PASS | PASS | PASS | PASS |
| Access and regulation | PASS | PASS | PASS | PASS |
| Assessment | PASS | PASS | PASS | PASS |
| Model and answers | PASS | PASS | PASS | PASS |
| Arrival answers | PASS | PASS | PASS | PASS |
| Shared activity reasoning | PASS | PASS | PASS | PASS |
| Exit responses | PASS | PASS | PASS | PASS |
| Teaching and evidence record | PASS | PASS | PASS | PASS |
| Look for | PASS | PASS | PASS | PASS |
| Media | PASS | PASS | PASS | PASS |
| Source credits | PASS | PASS | PASS | PASS |
| Planning | PASS | PASS | PASS | PASS |
| Teaching sequence | PASS | PASS | PASS | PASS |
| Arrival questions and answers | PASS | PASS | PASS | PASS |
| Hinge and diagnoses | PASS | PASS | PASS | PASS |
| Parallel hinge after a teaching move | PASS | PASS | PASS | PASS |
| LOOP | PASS | PASS | PASS | PASS |
| Target opportunities | PASS | PASS | PASS | PASS |
| Exit guidance | PASS | PASS | PASS | PASS |
| If behind | PASS | PASS | PASS | PASS |
| Planning and evaluation record | PASS | PASS | PASS | PASS |
| Sources | PASS | PASS | PASS | PASS |
| Book evidence and feedback | PASS | PASS | PASS | PASS |
| Planned adaptations | PASS | PASS | PASS | PASS |
| Invite a response · two per route | PASS | PASS | PASS | PASS |
| F6 exact preparation | PASS | PASS | PASS | PASS |
| F8 full IEDP line | PASS | PASS | PASS | PASS |
| F8 EAL is not SEN | PASS | PASS | PASS | PASS |
| F8 Supported 1/2 Standard 1/2 Stretch 1/2 | PASS | PASS | PASS | PASS |
| A4 geometry | PASS | PASS | PASS | PASS |

| Surface | Characters | Missing source chunks | Banned words | Author |
|---|---:|---:|---:|---|
| Teacher_Notes.docx | 18914 | 0 | 0 | Matt Roper |
| Editable_Pack.docx | 28148 | 0 | 0 | Matt Roper |
| Teacher_Notes.pdf | 18954 | 0 | 0 | Matt Roper |
| TA_Brief.pdf | 18954 | 0 | 0 | Matt Roper |

Planned adaptations table: 5 body rows; 2 columns. Invite a response table: 6 body rows; 3 columns.
Word pack: F3 is an exact heading; organiser comes first; 5 real page breaks; 13 embedded pictures/logos.

The E-number labels immediately followed by “Assessment source” are evidence-card identifiers and are exempt from the version-word scan.

All DOCX files were rendered through LibreOffice; representative page images were inspected. Full reviewer Office and print checks remain separate from these static checks.


### Staff document checks — BUILD_RE_A2_W06

Static checks against the final lesson staff content. Every source paragraph and table cell survives on all four required staff surfaces; whitespace-only PDF line wrapping is ignored.

| Field | Teacher Notes Word | Word pack | Teacher Notes PDF | TA brief PDF |
|---|---|---|---|---|
| Teacher card | PASS | PASS | PASS | PASS |
| Forty minute route | PASS | PASS | PASS | PASS |
| Preparation | PASS | PASS | PASS | PASS |
| Access and regulation | PASS | PASS | PASS | PASS |
| Assessment | PASS | PASS | PASS | PASS |
| Model and answers | PASS | PASS | PASS | PASS |
| Arrival answers | PASS | PASS | PASS | PASS |
| Shared activity reasoning | PASS | PASS | PASS | PASS |
| Exit responses | PASS | PASS | PASS | PASS |
| Teaching and evidence record | PASS | PASS | PASS | PASS |
| Look for | PASS | PASS | PASS | PASS |
| Media | PASS | PASS | PASS | PASS |
| Source credits | PASS | PASS | PASS | PASS |
| Planning | PASS | PASS | PASS | PASS |
| Teaching sequence | PASS | PASS | PASS | PASS |
| Arrival questions and answers | PASS | PASS | PASS | PASS |
| Hinge and diagnoses | PASS | PASS | PASS | PASS |
| Parallel hinge after a teaching move | PASS | PASS | PASS | PASS |
| LOOP | PASS | PASS | PASS | PASS |
| Target opportunities | PASS | PASS | PASS | PASS |
| Exit guidance | PASS | PASS | PASS | PASS |
| If behind | PASS | PASS | PASS | PASS |
| Planning and evaluation record | PASS | PASS | PASS | PASS |
| Sources | PASS | PASS | PASS | PASS |
| Book evidence and feedback | PASS | PASS | PASS | PASS |
| Planned adaptations | PASS | PASS | PASS | PASS |
| Invite a response · two per route | PASS | PASS | PASS | PASS |
| F6 exact preparation | PASS | PASS | PASS | PASS |
| F8 full IEDP line | PASS | PASS | PASS | PASS |
| F8 EAL is not SEN | PASS | PASS | PASS | PASS |
| F8 Supported 1/2 Standard 1/2 Stretch 1/2 | PASS | PASS | PASS | PASS |
| A4 geometry | PASS | PASS | PASS | PASS |

| Surface | Characters | Missing source chunks | Banned words | Author |
|---|---:|---:|---:|---|
| Teacher_Notes.docx | 18145 | 0 | 0 | Matt Roper |
| Editable_Pack.docx | 27088 | 0 | 0 | Matt Roper |
| Teacher_Notes.pdf | 18145 | 0 | 0 | Matt Roper |
| TA_Brief.pdf | 18145 | 0 | 0 | Matt Roper |

Planned adaptations table: 5 body rows; 2 columns. Invite a response table: 6 body rows; 3 columns.
Word pack: F3 is an exact heading; organiser comes first; 5 real page breaks; 13 embedded pictures/logos.

The E-number labels immediately followed by “Assessment source” are evidence-card identifiers and are exempt from the version-word scan.

All DOCX files were rendered through LibreOffice; representative page images were inspected. Full reviewer Office and print checks remain separate from these static checks.


### Staff document checks — BUILD_RE_A2_W07

Static checks against the final lesson staff content. Every source paragraph and table cell survives on all four required staff surfaces; whitespace-only PDF line wrapping is ignored.

| Field | Teacher Notes Word | Word pack | Teacher Notes PDF | TA brief PDF |
|---|---|---|---|---|
| Teacher card | PASS | PASS | PASS | PASS |
| Forty minute route | PASS | PASS | PASS | PASS |
| Preparation | PASS | PASS | PASS | PASS |
| Access and regulation | PASS | PASS | PASS | PASS |
| Assessment | PASS | PASS | PASS | PASS |
| Model and answers | PASS | PASS | PASS | PASS |
| Arrival answers | PASS | PASS | PASS | PASS |
| Shared activity reasoning | PASS | PASS | PASS | PASS |
| Exit responses | PASS | PASS | PASS | PASS |
| Teaching and evidence record | PASS | PASS | PASS | PASS |
| Look for | PASS | PASS | PASS | PASS |
| Media | PASS | PASS | PASS | PASS |
| Source credits | PASS | PASS | PASS | PASS |
| Planning | PASS | PASS | PASS | PASS |
| Teaching sequence | PASS | PASS | PASS | PASS |
| Arrival questions and answers | PASS | PASS | PASS | PASS |
| Hinge and diagnoses | PASS | PASS | PASS | PASS |
| Parallel hinge after a teaching move | PASS | PASS | PASS | PASS |
| LOOP | PASS | PASS | PASS | PASS |
| Target opportunities | PASS | PASS | PASS | PASS |
| Exit guidance | PASS | PASS | PASS | PASS |
| If behind | PASS | PASS | PASS | PASS |
| Planning and evaluation record | PASS | PASS | PASS | PASS |
| Sources | PASS | PASS | PASS | PASS |
| Book evidence and feedback | PASS | PASS | PASS | PASS |
| Planned adaptations | PASS | PASS | PASS | PASS |
| Invite a response · two per route | PASS | PASS | PASS | PASS |
| F6 exact preparation | PASS | PASS | PASS | PASS |
| F8 full IEDP line | PASS | PASS | PASS | PASS |
| F8 EAL is not SEN | PASS | PASS | PASS | PASS |
| F8 Supported 1/2 Standard 1/2 Stretch 1/2 | PASS | PASS | PASS | PASS |
| A4 geometry | PASS | PASS | PASS | PASS |

| Surface | Characters | Missing source chunks | Banned words | Author |
|---|---:|---:|---:|---|
| Teacher_Notes.docx | 18982 | 0 | 0 | Matt Roper |
| Editable_Pack.docx | 28809 | 0 | 0 | Matt Roper |
| Teacher_Notes.pdf | 19022 | 0 | 0 | Matt Roper |
| TA_Brief.pdf | 19022 | 0 | 0 | Matt Roper |

Planned adaptations table: 5 body rows; 2 columns. Invite a response table: 6 body rows; 3 columns.
Word pack: F3 is an exact heading; organiser comes first; 5 real page breaks; 13 embedded pictures/logos.

The E-number labels immediately followed by “Assessment source” are evidence-card identifiers and are exempt from the version-word scan.

All DOCX files were rendered through LibreOffice; representative page images were inspected. Full reviewer Office and print checks remain separate from these static checks.


### Staff document checks — GROW_RE_A1_W08

Static checks against the final lesson staff content. Every source paragraph and table cell survives on all four required staff surfaces; whitespace-only PDF line wrapping is ignored.

| Field | Teacher Notes Word | Word pack | Teacher Notes PDF | TA brief PDF |
|---|---|---|---|---|
| Teacher card | PASS | PASS | PASS | PASS |
| Forty minute route | PASS | PASS | PASS | PASS |
| Preparation | PASS | PASS | PASS | PASS |
| Access and regulation | PASS | PASS | PASS | PASS |
| Assessment | PASS | PASS | PASS | PASS |
| Planning | PASS | PASS | PASS | PASS |
| Teaching sequence | PASS | PASS | PASS | PASS |
| LOOP | PASS | PASS | PASS | PASS |
| Target opportunities | PASS | PASS | PASS | PASS |
| If behind | PASS | PASS | PASS | PASS |
| Book evidence and feedback | PASS | PASS | PASS | PASS |
| First lesson back · staff card | PASS | PASS | PASS | PASS |
| Book scan | PASS | PASS | PASS | PASS |
| Ask cover staff and TAs | PASS | PASS | PASS | PASS |
| Once-only return line | PASS | PASS | PASS | PASS |
| Today | PASS | PASS | PASS | PASS |
| Private RAG rule | PASS | PASS | PASS | PASS |
| What the check feeds into | PASS | PASS | PASS | PASS |
| Planning and evaluation | PASS | PASS | PASS | PASS |
| Target moments | PASS | PASS | PASS | PASS |
| Model and answers | PASS | PASS | PASS | PASS |
| Arrival questions and answers | PASS | PASS | PASS | PASS |
| Starter answers | PASS | PASS | PASS | PASS |
| Shared activity reasoning | PASS | PASS | PASS | PASS |
| Hinge and diagnoses | PASS | PASS | PASS | PASS |
| Parallel hinge after a teaching move | PASS | PASS | PASS | PASS |
| Exit guidance | PASS | PASS | PASS | PASS |
| Teaching and evidence record | PASS | PASS | PASS | PASS |
| Look for | PASS | PASS | PASS | PASS |
| Media | PASS | PASS | PASS | PASS |
| Planning and evaluation record | PASS | PASS | PASS | PASS |
| Sources | PASS | PASS | PASS | PASS |
| Planned adaptations | PASS | PASS | PASS | PASS |
| Invite a response · two per route | PASS | PASS | PASS | PASS |
| Individual check answers and source map | PASS | PASS | PASS | PASS |
| F6 exact preparation | PASS | PASS | PASS | PASS |
| F8 full IEDP line | PASS | PASS | PASS | PASS |
| F8 EAL is not SEN | PASS | PASS | PASS | PASS |
| F8 Supported 1/2 Standard 1/2 Stretch 1/2 | PASS | PASS | PASS | PASS |
| A4 geometry | PASS | PASS | PASS | PASS |

| Surface | Characters | Missing source chunks | Banned words | Author |
|---|---:|---:|---:|---|
| Teacher_Notes.docx | 16556 | 0 | 0 | Matt Roper |
| Editable_Pack.docx | 23093 | 0 | 0 | Matt Roper |
| Teacher_Notes.pdf | 16556 | 0 | 0 | Matt Roper |
| TA_Brief.pdf | 16556 | 0 | 0 | Matt Roper |

Planned adaptations table: 5 body rows; 2 columns. Invite a response table: 6 body rows; 3 columns.
Word pack: F3 is an exact heading; organiser comes first; 5 real page breaks; 12 embedded pictures/logos.

The E-number labels immediately followed by “Assessment source” are evidence-card identifiers and are exempt from the version-word scan.

All DOCX files were rendered through LibreOffice; representative page images were inspected. Full reviewer Office and print checks remain separate from these static checks.


### Staff document checks — GROW_RE_A2_W01

Static checks against the final lesson staff content. Every source paragraph and table cell survives on all four required staff surfaces; whitespace-only PDF line wrapping is ignored.

| Field | Teacher Notes Word | Word pack | Teacher Notes PDF | TA brief PDF |
|---|---|---|---|---|
| Teacher card | PASS | PASS | PASS | PASS |
| Forty minute route | PASS | PASS | PASS | PASS |
| Preparation | PASS | PASS | PASS | PASS |
| Access and regulation | PASS | PASS | PASS | PASS |
| Assessment | PASS | PASS | PASS | PASS |
| Model and answers | PASS | PASS | PASS | PASS |
| Arrival answers | PASS | PASS | PASS | PASS |
| Shared activity reasoning | PASS | PASS | PASS | PASS |
| Exit responses | PASS | PASS | PASS | PASS |
| Teaching and evidence record | PASS | PASS | PASS | PASS |
| Look for | PASS | PASS | PASS | PASS |
| Media | PASS | PASS | PASS | PASS |
| Source credits | PASS | PASS | PASS | PASS |
| Planning | PASS | PASS | PASS | PASS |
| Teaching sequence | PASS | PASS | PASS | PASS |
| Arrival questions and answers | PASS | PASS | PASS | PASS |
| Hinge and diagnoses | PASS | PASS | PASS | PASS |
| Parallel hinge after a teaching move | PASS | PASS | PASS | PASS |
| LOOP | PASS | PASS | PASS | PASS |
| Target opportunities | PASS | PASS | PASS | PASS |
| Exit guidance | PASS | PASS | PASS | PASS |
| If behind | PASS | PASS | PASS | PASS |
| Planning and evaluation record | PASS | PASS | PASS | PASS |
| Sources | PASS | PASS | PASS | PASS |
| Book evidence and feedback | PASS | PASS | PASS | PASS |
| Planned adaptations | PASS | PASS | PASS | PASS |
| Invite a response · two per route | PASS | PASS | PASS | PASS |
| F6 exact preparation | PASS | PASS | PASS | PASS |
| F8 full IEDP line | PASS | PASS | PASS | PASS |
| F8 EAL is not SEN | PASS | PASS | PASS | PASS |
| F8 Supported 1/2 Standard 1/2 Stretch 1/2 | PASS | PASS | PASS | PASS |
| A4 geometry | PASS | PASS | PASS | PASS |

| Surface | Characters | Missing source chunks | Banned words | Author |
|---|---:|---:|---:|---|
| Teacher_Notes.docx | 20485 | 0 | 0 | Matt Roper |
| Editable_Pack.docx | 30130 | 0 | 0 | Matt Roper |
| Teacher_Notes.pdf | 20525 | 0 | 0 | Matt Roper |
| TA_Brief.pdf | 20525 | 0 | 0 | Matt Roper |

Planned adaptations table: 5 body rows; 2 columns. Invite a response table: 6 body rows; 3 columns.
Word pack: F3 is an exact heading; organiser comes first; 5 real page breaks; 13 embedded pictures/logos.

The E-number labels immediately followed by “Assessment source” are evidence-card identifiers and are exempt from the version-word scan.

All DOCX files were rendered through LibreOffice; representative page images were inspected. Full reviewer Office and print checks remain separate from these static checks.


### Staff document checks — GROW_RE_A2_W02

Static checks against the final lesson staff content. Every source paragraph and table cell survives on all four required staff surfaces; whitespace-only PDF line wrapping is ignored.

| Field | Teacher Notes Word | Word pack | Teacher Notes PDF | TA brief PDF |
|---|---|---|---|---|
| Teacher card | PASS | PASS | PASS | PASS |
| Forty minute route | PASS | PASS | PASS | PASS |
| Preparation | PASS | PASS | PASS | PASS |
| Access and regulation | PASS | PASS | PASS | PASS |
| Assessment | PASS | PASS | PASS | PASS |
| Model and answers | PASS | PASS | PASS | PASS |
| Arrival answers | PASS | PASS | PASS | PASS |
| Shared activity reasoning | PASS | PASS | PASS | PASS |
| Exit responses | PASS | PASS | PASS | PASS |
| Teaching and evidence record | PASS | PASS | PASS | PASS |
| Look for | PASS | PASS | PASS | PASS |
| Media | PASS | PASS | PASS | PASS |
| Source credits | PASS | PASS | PASS | PASS |
| Planning | PASS | PASS | PASS | PASS |
| Teaching sequence | PASS | PASS | PASS | PASS |
| Arrival questions and answers | PASS | PASS | PASS | PASS |
| Hinge and diagnoses | PASS | PASS | PASS | PASS |
| Parallel hinge after a teaching move | PASS | PASS | PASS | PASS |
| LOOP | PASS | PASS | PASS | PASS |
| Target opportunities | PASS | PASS | PASS | PASS |
| Exit guidance | PASS | PASS | PASS | PASS |
| If behind | PASS | PASS | PASS | PASS |
| Planning and evaluation record | PASS | PASS | PASS | PASS |
| Sources | PASS | PASS | PASS | PASS |
| Book evidence and feedback | PASS | PASS | PASS | PASS |
| Planned adaptations | PASS | PASS | PASS | PASS |
| Invite a response · two per route | PASS | PASS | PASS | PASS |
| F6 exact preparation | PASS | PASS | PASS | PASS |
| F8 full IEDP line | PASS | PASS | PASS | PASS |
| F8 EAL is not SEN | PASS | PASS | PASS | PASS |
| F8 Supported 1/2 Standard 1/2 Stretch 1/2 | PASS | PASS | PASS | PASS |
| A4 geometry | PASS | PASS | PASS | PASS |

| Surface | Characters | Missing source chunks | Banned words | Author |
|---|---:|---:|---:|---|
| Teacher_Notes.docx | 19681 | 0 | 0 | Matt Roper |
| Editable_Pack.docx | 29021 | 0 | 0 | Matt Roper |
| Teacher_Notes.pdf | 19721 | 0 | 0 | Matt Roper |
| TA_Brief.pdf | 19721 | 0 | 0 | Matt Roper |

Planned adaptations table: 5 body rows; 2 columns. Invite a response table: 6 body rows; 3 columns.
Word pack: F3 is an exact heading; organiser comes first; 5 real page breaks; 13 embedded pictures/logos.

The E-number labels immediately followed by “Assessment source” are evidence-card identifiers and are exempt from the version-word scan.

All DOCX files were rendered through LibreOffice; representative page images were inspected. Full reviewer Office and print checks remain separate from these static checks.


### Staff document checks — GROW_RE_A2_W03

Static checks against the final lesson staff content. Every source paragraph and table cell survives on all four required staff surfaces; whitespace-only PDF line wrapping is ignored.

| Field | Teacher Notes Word | Word pack | Teacher Notes PDF | TA brief PDF |
|---|---|---|---|---|
| Teacher card | PASS | PASS | PASS | PASS |
| Forty minute route | PASS | PASS | PASS | PASS |
| Preparation | PASS | PASS | PASS | PASS |
| Access and regulation | PASS | PASS | PASS | PASS |
| Assessment | PASS | PASS | PASS | PASS |
| Model and answers | PASS | PASS | PASS | PASS |
| Arrival answers | PASS | PASS | PASS | PASS |
| Shared activity reasoning | PASS | PASS | PASS | PASS |
| Exit responses | PASS | PASS | PASS | PASS |
| Teaching and evidence record | PASS | PASS | PASS | PASS |
| Look for | PASS | PASS | PASS | PASS |
| Media | PASS | PASS | PASS | PASS |
| Source credits | PASS | PASS | PASS | PASS |
| Planning | PASS | PASS | PASS | PASS |
| Teaching sequence | PASS | PASS | PASS | PASS |
| Arrival questions and answers | PASS | PASS | PASS | PASS |
| Hinge and diagnoses | PASS | PASS | PASS | PASS |
| Parallel hinge after a teaching move | PASS | PASS | PASS | PASS |
| LOOP | PASS | PASS | PASS | PASS |
| Target opportunities | PASS | PASS | PASS | PASS |
| Exit guidance | PASS | PASS | PASS | PASS |
| If behind | PASS | PASS | PASS | PASS |
| Planning and evaluation record | PASS | PASS | PASS | PASS |
| Sources | PASS | PASS | PASS | PASS |
| Book evidence and feedback | PASS | PASS | PASS | PASS |
| Planned adaptations | PASS | PASS | PASS | PASS |
| Invite a response · two per route | PASS | PASS | PASS | PASS |
| F6 exact preparation | PASS | PASS | PASS | PASS |
| F8 full IEDP line | PASS | PASS | PASS | PASS |
| F8 EAL is not SEN | PASS | PASS | PASS | PASS |
| F8 Supported 1/2 Standard 1/2 Stretch 1/2 | PASS | PASS | PASS | PASS |
| A4 geometry | PASS | PASS | PASS | PASS |

| Surface | Characters | Missing source chunks | Banned words | Author |
|---|---:|---:|---:|---|
| Teacher_Notes.docx | 19570 | 0 | 0 | Matt Roper |
| Editable_Pack.docx | 28698 | 0 | 0 | Matt Roper |
| Teacher_Notes.pdf | 19570 | 0 | 0 | Matt Roper |
| TA_Brief.pdf | 19570 | 0 | 0 | Matt Roper |

Planned adaptations table: 5 body rows; 2 columns. Invite a response table: 6 body rows; 3 columns.
Word pack: F3 is an exact heading; organiser comes first; 5 real page breaks; 13 embedded pictures/logos.

The E-number labels immediately followed by “Assessment source” are evidence-card identifiers and are exempt from the version-word scan.

All DOCX files were rendered through LibreOffice; representative page images were inspected. Full reviewer Office and print checks remain separate from these static checks.


### Staff document checks — GROW_RE_A2_W04

Static checks against the final lesson staff content. Every source paragraph and table cell survives on all four required staff surfaces; whitespace-only PDF line wrapping is ignored.

| Field | Teacher Notes Word | Word pack | Teacher Notes PDF | TA brief PDF |
|---|---|---|---|---|
| Teacher card | PASS | PASS | PASS | PASS |
| Forty minute route | PASS | PASS | PASS | PASS |
| Preparation | PASS | PASS | PASS | PASS |
| Access and regulation | PASS | PASS | PASS | PASS |
| Assessment | PASS | PASS | PASS | PASS |
| Model and answers | PASS | PASS | PASS | PASS |
| Arrival answers | PASS | PASS | PASS | PASS |
| Shared activity reasoning | PASS | PASS | PASS | PASS |
| Exit responses | PASS | PASS | PASS | PASS |
| Teaching and evidence record | PASS | PASS | PASS | PASS |
| Look for | PASS | PASS | PASS | PASS |
| Media | PASS | PASS | PASS | PASS |
| Source credits | PASS | PASS | PASS | PASS |
| Planning | PASS | PASS | PASS | PASS |
| Teaching sequence | PASS | PASS | PASS | PASS |
| Arrival questions and answers | PASS | PASS | PASS | PASS |
| Hinge and diagnoses | PASS | PASS | PASS | PASS |
| Parallel hinge after a teaching move | PASS | PASS | PASS | PASS |
| LOOP | PASS | PASS | PASS | PASS |
| Target opportunities | PASS | PASS | PASS | PASS |
| Exit guidance | PASS | PASS | PASS | PASS |
| If behind | PASS | PASS | PASS | PASS |
| Planning and evaluation record | PASS | PASS | PASS | PASS |
| Sources | PASS | PASS | PASS | PASS |
| Book evidence and feedback | PASS | PASS | PASS | PASS |
| Planned adaptations | PASS | PASS | PASS | PASS |
| Invite a response · two per route | PASS | PASS | PASS | PASS |
| F6 exact preparation | PASS | PASS | PASS | PASS |
| F8 full IEDP line | PASS | PASS | PASS | PASS |
| F8 EAL is not SEN | PASS | PASS | PASS | PASS |
| F8 Supported 1/2 Standard 1/2 Stretch 1/2 | PASS | PASS | PASS | PASS |
| A4 geometry | PASS | PASS | PASS | PASS |

| Surface | Characters | Missing source chunks | Banned words | Author |
|---|---:|---:|---:|---|
| Teacher_Notes.docx | 19423 | 0 | 0 | Matt Roper |
| Editable_Pack.docx | 28776 | 0 | 0 | Matt Roper |
| Teacher_Notes.pdf | 19423 | 0 | 0 | Matt Roper |
| TA_Brief.pdf | 19423 | 0 | 0 | Matt Roper |

Planned adaptations table: 5 body rows; 2 columns. Invite a response table: 6 body rows; 3 columns.
Word pack: F3 is an exact heading; organiser comes first; 5 real page breaks; 13 embedded pictures/logos.

The E-number labels immediately followed by “Assessment source” are evidence-card identifiers and are exempt from the version-word scan.

All DOCX files were rendered through LibreOffice; representative page images were inspected. Full reviewer Office and print checks remain separate from these static checks.


### Staff document checks — GROW_RE_A2_W05

Static checks against the final lesson staff content. Every source paragraph and table cell survives on all four required staff surfaces; whitespace-only PDF line wrapping is ignored.

| Field | Teacher Notes Word | Word pack | Teacher Notes PDF | TA brief PDF |
|---|---|---|---|---|
| Teacher card | PASS | PASS | PASS | PASS |
| Forty minute route | PASS | PASS | PASS | PASS |
| Preparation | PASS | PASS | PASS | PASS |
| Access and regulation | PASS | PASS | PASS | PASS |
| Assessment | PASS | PASS | PASS | PASS |
| Model and answers | PASS | PASS | PASS | PASS |
| Arrival answers | PASS | PASS | PASS | PASS |
| Shared activity reasoning | PASS | PASS | PASS | PASS |
| Exit responses | PASS | PASS | PASS | PASS |
| Teaching and evidence record | PASS | PASS | PASS | PASS |
| Look for | PASS | PASS | PASS | PASS |
| Media | PASS | PASS | PASS | PASS |
| Source credits | PASS | PASS | PASS | PASS |
| Planning | PASS | PASS | PASS | PASS |
| Teaching sequence | PASS | PASS | PASS | PASS |
| Arrival questions and answers | PASS | PASS | PASS | PASS |
| Hinge and diagnoses | PASS | PASS | PASS | PASS |
| Parallel hinge after a teaching move | PASS | PASS | PASS | PASS |
| LOOP | PASS | PASS | PASS | PASS |
| Target opportunities | PASS | PASS | PASS | PASS |
| Exit guidance | PASS | PASS | PASS | PASS |
| If behind | PASS | PASS | PASS | PASS |
| Planning and evaluation record | PASS | PASS | PASS | PASS |
| Sources | PASS | PASS | PASS | PASS |
| Book evidence and feedback | PASS | PASS | PASS | PASS |
| Planned adaptations | PASS | PASS | PASS | PASS |
| Invite a response · two per route | PASS | PASS | PASS | PASS |
| F6 exact preparation | PASS | PASS | PASS | PASS |
| F8 full IEDP line | PASS | PASS | PASS | PASS |
| F8 EAL is not SEN | PASS | PASS | PASS | PASS |
| F8 Supported 1/2 Standard 1/2 Stretch 1/2 | PASS | PASS | PASS | PASS |
| A4 geometry | PASS | PASS | PASS | PASS |

| Surface | Characters | Missing source chunks | Banned words | Author |
|---|---:|---:|---:|---|
| Teacher_Notes.docx | 20012 | 0 | 0 | Matt Roper |
| Editable_Pack.docx | 30373 | 0 | 0 | Matt Roper |
| Teacher_Notes.pdf | 20052 | 0 | 0 | Matt Roper |
| TA_Brief.pdf | 20052 | 0 | 0 | Matt Roper |

Planned adaptations table: 5 body rows; 2 columns. Invite a response table: 6 body rows; 3 columns.
Word pack: F3 is an exact heading; organiser comes first; 5 real page breaks; 13 embedded pictures/logos.

The E-number labels immediately followed by “Assessment source” are evidence-card identifiers and are exempt from the version-word scan.

All DOCX files were rendered through LibreOffice; representative page images were inspected. Full reviewer Office and print checks remain separate from these static checks.


### Staff document checks — GROW_RE_A2_W06

Static checks against the final lesson staff content. Every source paragraph and table cell survives on all four required staff surfaces; whitespace-only PDF line wrapping is ignored.

| Field | Teacher Notes Word | Word pack | Teacher Notes PDF | TA brief PDF |
|---|---|---|---|---|
| Teacher card | PASS | PASS | PASS | PASS |
| Forty minute route | PASS | PASS | PASS | PASS |
| Preparation | PASS | PASS | PASS | PASS |
| Access and regulation | PASS | PASS | PASS | PASS |
| Assessment | PASS | PASS | PASS | PASS |
| Model and answers | PASS | PASS | PASS | PASS |
| Arrival answers | PASS | PASS | PASS | PASS |
| Shared activity reasoning | PASS | PASS | PASS | PASS |
| Exit responses | PASS | PASS | PASS | PASS |
| Teaching and evidence record | PASS | PASS | PASS | PASS |
| Look for | PASS | PASS | PASS | PASS |
| Media | PASS | PASS | PASS | PASS |
| Source credits | PASS | PASS | PASS | PASS |
| Planning | PASS | PASS | PASS | PASS |
| Teaching sequence | PASS | PASS | PASS | PASS |
| Arrival questions and answers | PASS | PASS | PASS | PASS |
| Hinge and diagnoses | PASS | PASS | PASS | PASS |
| Parallel hinge after a teaching move | PASS | PASS | PASS | PASS |
| LOOP | PASS | PASS | PASS | PASS |
| Target opportunities | PASS | PASS | PASS | PASS |
| Exit guidance | PASS | PASS | PASS | PASS |
| If behind | PASS | PASS | PASS | PASS |
| Planning and evaluation record | PASS | PASS | PASS | PASS |
| Sources | PASS | PASS | PASS | PASS |
| Book evidence and feedback | PASS | PASS | PASS | PASS |
| Planned adaptations | PASS | PASS | PASS | PASS |
| Invite a response · two per route | PASS | PASS | PASS | PASS |
| F6 exact preparation | PASS | PASS | PASS | PASS |
| F8 full IEDP line | PASS | PASS | PASS | PASS |
| F8 EAL is not SEN | PASS | PASS | PASS | PASS |
| F8 Supported 1/2 Standard 1/2 Stretch 1/2 | PASS | PASS | PASS | PASS |
| A4 geometry | PASS | PASS | PASS | PASS |

| Surface | Characters | Missing source chunks | Banned words | Author |
|---|---:|---:|---:|---|
| Teacher_Notes.docx | 19844 | 0 | 0 | Matt Roper |
| Editable_Pack.docx | 29690 | 0 | 0 | Matt Roper |
| Teacher_Notes.pdf | 19884 | 0 | 0 | Matt Roper |
| TA_Brief.pdf | 19884 | 0 | 0 | Matt Roper |

Planned adaptations table: 5 body rows; 2 columns. Invite a response table: 6 body rows; 3 columns.
Word pack: F3 is an exact heading; organiser comes first; 5 real page breaks; 13 embedded pictures/logos.

The E-number labels immediately followed by “Assessment source” are evidence-card identifiers and are exempt from the version-word scan.

All DOCX files were rendered through LibreOffice; representative page images were inspected. Full reviewer Office and print checks remain separate from these static checks.


### Staff document checks — GROW_RE_A2_W07

Static checks against the final lesson staff content. Every source paragraph and table cell survives on all four required staff surfaces; whitespace-only PDF line wrapping is ignored.

| Field | Teacher Notes Word | Word pack | Teacher Notes PDF | TA brief PDF |
|---|---|---|---|---|
| Teacher card | PASS | PASS | PASS | PASS |
| Forty minute route | PASS | PASS | PASS | PASS |
| Preparation | PASS | PASS | PASS | PASS |
| Access and regulation | PASS | PASS | PASS | PASS |
| Assessment | PASS | PASS | PASS | PASS |
| Model and answers | PASS | PASS | PASS | PASS |
| Arrival answers | PASS | PASS | PASS | PASS |
| Shared activity reasoning | PASS | PASS | PASS | PASS |
| Exit responses | PASS | PASS | PASS | PASS |
| Teaching and evidence record | PASS | PASS | PASS | PASS |
| Look for | PASS | PASS | PASS | PASS |
| Media | PASS | PASS | PASS | PASS |
| Source credits | PASS | PASS | PASS | PASS |
| Planning | PASS | PASS | PASS | PASS |
| Teaching sequence | PASS | PASS | PASS | PASS |
| Arrival questions and answers | PASS | PASS | PASS | PASS |
| Hinge and diagnoses | PASS | PASS | PASS | PASS |
| Parallel hinge after a teaching move | PASS | PASS | PASS | PASS |
| LOOP | PASS | PASS | PASS | PASS |
| Target opportunities | PASS | PASS | PASS | PASS |
| Exit guidance | PASS | PASS | PASS | PASS |
| If behind | PASS | PASS | PASS | PASS |
| Planning and evaluation record | PASS | PASS | PASS | PASS |
| Sources | PASS | PASS | PASS | PASS |
| Book evidence and feedback | PASS | PASS | PASS | PASS |
| Planned adaptations | PASS | PASS | PASS | PASS |
| Invite a response · two per route | PASS | PASS | PASS | PASS |
| F6 exact preparation | PASS | PASS | PASS | PASS |
| F8 full IEDP line | PASS | PASS | PASS | PASS |
| F8 EAL is not SEN | PASS | PASS | PASS | PASS |
| F8 Supported 1/2 Standard 1/2 Stretch 1/2 | PASS | PASS | PASS | PASS |
| A4 geometry | PASS | PASS | PASS | PASS |

| Surface | Characters | Missing source chunks | Banned words | Author |
|---|---:|---:|---:|---|
| Teacher_Notes.docx | 20977 | 0 | 0 | Matt Roper |
| Editable_Pack.docx | 31619 | 0 | 0 | Matt Roper |
| Teacher_Notes.pdf | 21016 | 0 | 0 | Matt Roper |
| TA_Brief.pdf | 21016 | 0 | 0 | Matt Roper |

Planned adaptations table: 5 body rows; 2 columns. Invite a response table: 6 body rows; 3 columns.
Word pack: F3 is an exact heading; organiser comes first; 5 real page breaks; 13 embedded pictures/logos.

The E-number labels immediately followed by “Assessment source” are evidence-card identifiers and are exempt from the version-word scan.

All DOCX files were rendered through LibreOffice; representative page images were inspected. Full reviewer Office and print checks remain separate from these static checks.


### Staff document checks — LAUNCH_RE_A1_W08

Static checks against the final lesson staff content. Every source paragraph and table cell survives on all four required staff surfaces; whitespace-only PDF line wrapping is ignored.

| Field | Teacher Notes Word | Word pack | Teacher Notes PDF | TA brief PDF |
|---|---|---|---|---|
| Teacher card | PASS | PASS | PASS | PASS |
| Forty minute route | PASS | PASS | PASS | PASS |
| Preparation | PASS | PASS | PASS | PASS |
| Access and regulation | PASS | PASS | PASS | PASS |
| Assessment | PASS | PASS | PASS | PASS |
| First lesson back · staff card | PASS | PASS | PASS | PASS |
| Book scan | PASS | PASS | PASS | PASS |
| Ask cover staff and TAs | PASS | PASS | PASS | PASS |
| Once-only return line | PASS | PASS | PASS | PASS |
| Today | PASS | PASS | PASS | PASS |
| Private RAG rule | PASS | PASS | PASS | PASS |
| What the check feeds into | PASS | PASS | PASS | PASS |
| Planned adaptations | PASS | PASS | PASS | PASS |
| Invite a response · two per route | PASS | PASS | PASS | PASS |
| Target opportunities | PASS | PASS | PASS | PASS |
| Book evidence and feedback | PASS | PASS | PASS | PASS |
| Teaching sequence | PASS | PASS | PASS | PASS |
| Model and answers | PASS | PASS | PASS | PASS |
| Arrival questions and answers | PASS | PASS | PASS | PASS |
| Starter answers | PASS | PASS | PASS | PASS |
| Shared activity reasoning | PASS | PASS | PASS | PASS |
| Hinge and diagnoses | PASS | PASS | PASS | PASS |
| Parallel hinge after a teaching move | PASS | PASS | PASS | PASS |
| If time is short | PASS | PASS | PASS | PASS |
| Planning and evaluation record | PASS | PASS | PASS | PASS |
| Individual check answers and source map | PASS | PASS | PASS | PASS |
| Exit guidance | PASS | PASS | PASS | PASS |
| F6 exact preparation | PASS | PASS | PASS | PASS |
| F8 full IEDP line | PASS | PASS | PASS | PASS |
| F8 EAL is not SEN | PASS | PASS | PASS | PASS |
| F8 Supported 1/2 Standard 1/2 Stretch 1/2 | PASS | PASS | PASS | PASS |
| A4 geometry | PASS | PASS | PASS | PASS |

| Surface | Characters | Missing source chunks | Banned words | Author |
|---|---:|---:|---:|---|
| Teacher_Notes.docx | 10822 | 0 | 0 | Matt Roper |
| Editable_Pack.docx | 18235 | 0 | 0 | Matt Roper |
| Teacher_Notes.pdf | 10822 | 0 | 0 | Matt Roper |
| TA_Brief.pdf | 10822 | 0 | 0 | Matt Roper |

Planned adaptations table: 5 body rows; 2 columns. Invite a response table: 6 body rows; 3 columns.
Word pack: F3 is an exact heading; organiser comes first; 5 real page breaks; 12 embedded pictures/logos.

The E-number labels immediately followed by “Assessment source” are evidence-card identifiers and are exempt from the version-word scan.

All DOCX files were rendered through LibreOffice; representative page images were inspected. Full reviewer Office and print checks remain separate from these static checks.


### Staff document checks — LAUNCH_RE_A2_W01

Static checks against the final lesson staff content. Every source paragraph and table cell survives on all four required staff surfaces; whitespace-only PDF line wrapping is ignored.

| Field | Teacher Notes Word | Word pack | Teacher Notes PDF | TA brief PDF |
|---|---|---|---|---|
| Teacher card | PASS | PASS | PASS | PASS |
| Forty minute route | PASS | PASS | PASS | PASS |
| Preparation | PASS | PASS | PASS | PASS |
| Access and regulation | PASS | PASS | PASS | PASS |
| Assessment | PASS | PASS | PASS | PASS |
| Model and answers | PASS | PASS | PASS | PASS |
| Arrival answers | PASS | PASS | PASS | PASS |
| Shared activity reasoning | PASS | PASS | PASS | PASS |
| Exit responses | PASS | PASS | PASS | PASS |
| Teaching and evidence record | PASS | PASS | PASS | PASS |
| Look for | PASS | PASS | PASS | PASS |
| Media | PASS | PASS | PASS | PASS |
| Source credits | PASS | PASS | PASS | PASS |
| Planning | PASS | PASS | PASS | PASS |
| Teaching sequence | PASS | PASS | PASS | PASS |
| Arrival questions and answers | PASS | PASS | PASS | PASS |
| Hinge and diagnoses | PASS | PASS | PASS | PASS |
| Parallel hinge after a teaching move | PASS | PASS | PASS | PASS |
| LOOP | PASS | PASS | PASS | PASS |
| Target opportunities | PASS | PASS | PASS | PASS |
| Exit guidance | PASS | PASS | PASS | PASS |
| If behind | PASS | PASS | PASS | PASS |
| Planning and evaluation record | PASS | PASS | PASS | PASS |
| Sources | PASS | PASS | PASS | PASS |
| Book evidence and feedback | PASS | PASS | PASS | PASS |
| Planned adaptations | PASS | PASS | PASS | PASS |
| Invite a response · two per route | PASS | PASS | PASS | PASS |
| F6 exact preparation | PASS | PASS | PASS | PASS |
| F8 full IEDP line | PASS | PASS | PASS | PASS |
| F8 EAL is not SEN | PASS | PASS | PASS | PASS |
| F8 Supported 1/2 Standard 1/2 Stretch 1/2 | PASS | PASS | PASS | PASS |
| A4 geometry | PASS | PASS | PASS | PASS |

| Surface | Characters | Missing source chunks | Banned words | Author |
|---|---:|---:|---:|---|
| Teacher_Notes.docx | 19709 | 0 | 0 | Matt Roper |
| Editable_Pack.docx | 29267 | 0 | 0 | Matt Roper |
| Teacher_Notes.pdf | 19749 | 0 | 0 | Matt Roper |
| TA_Brief.pdf | 19749 | 0 | 0 | Matt Roper |

Planned adaptations table: 5 body rows; 2 columns. Invite a response table: 6 body rows; 3 columns.
Word pack: F3 is an exact heading; organiser comes first; 5 real page breaks; 13 embedded pictures/logos.

The E-number labels immediately followed by “Assessment source” are evidence-card identifiers and are exempt from the version-word scan.

All DOCX files were rendered through LibreOffice; representative page images were inspected. Full reviewer Office and print checks remain separate from these static checks.


### Staff document checks — LAUNCH_RE_A2_W02

Static checks against the final lesson staff content. Every source paragraph and table cell survives on all four required staff surfaces; whitespace-only PDF line wrapping is ignored.

| Field | Teacher Notes Word | Word pack | Teacher Notes PDF | TA brief PDF |
|---|---|---|---|---|
| Teacher card | PASS | PASS | PASS | PASS |
| Forty minute route | PASS | PASS | PASS | PASS |
| Preparation | PASS | PASS | PASS | PASS |
| Access and regulation | PASS | PASS | PASS | PASS |
| Assessment | PASS | PASS | PASS | PASS |
| Model and answers | PASS | PASS | PASS | PASS |
| Arrival answers | PASS | PASS | PASS | PASS |
| Shared activity reasoning | PASS | PASS | PASS | PASS |
| Exit responses | PASS | PASS | PASS | PASS |
| Teaching and evidence record | PASS | PASS | PASS | PASS |
| Look for | PASS | PASS | PASS | PASS |
| Media | PASS | PASS | PASS | PASS |
| Source credits | PASS | PASS | PASS | PASS |
| Planning | PASS | PASS | PASS | PASS |
| Teaching sequence | PASS | PASS | PASS | PASS |
| Arrival questions and answers | PASS | PASS | PASS | PASS |
| Hinge and diagnoses | PASS | PASS | PASS | PASS |
| Parallel hinge after a teaching move | PASS | PASS | PASS | PASS |
| LOOP | PASS | PASS | PASS | PASS |
| Target opportunities | PASS | PASS | PASS | PASS |
| Exit guidance | PASS | PASS | PASS | PASS |
| If behind | PASS | PASS | PASS | PASS |
| Planning and evaluation record | PASS | PASS | PASS | PASS |
| Sources | PASS | PASS | PASS | PASS |
| Book evidence and feedback | PASS | PASS | PASS | PASS |
| Planned adaptations | PASS | PASS | PASS | PASS |
| Invite a response · two per route | PASS | PASS | PASS | PASS |
| F6 exact preparation | PASS | PASS | PASS | PASS |
| F8 full IEDP line | PASS | PASS | PASS | PASS |
| F8 EAL is not SEN | PASS | PASS | PASS | PASS |
| F8 Supported 1/2 Standard 1/2 Stretch 1/2 | PASS | PASS | PASS | PASS |
| A4 geometry | PASS | PASS | PASS | PASS |

| Surface | Characters | Missing source chunks | Banned words | Author |
|---|---:|---:|---:|---|
| Teacher_Notes.docx | 20039 | 0 | 0 | Matt Roper |
| Editable_Pack.docx | 29872 | 0 | 0 | Matt Roper |
| Teacher_Notes.pdf | 20079 | 0 | 0 | Matt Roper |
| TA_Brief.pdf | 20079 | 0 | 0 | Matt Roper |

Planned adaptations table: 5 body rows; 2 columns. Invite a response table: 6 body rows; 3 columns.
Word pack: F3 is an exact heading; organiser comes first; 5 real page breaks; 13 embedded pictures/logos.

The E-number labels immediately followed by “Assessment source” are evidence-card identifiers and are exempt from the version-word scan.

All DOCX files were rendered through LibreOffice; representative page images were inspected. Full reviewer Office and print checks remain separate from these static checks.


### Staff document checks — LAUNCH_RE_A2_W03

Static checks against the final lesson staff content. Every source paragraph and table cell survives on all four required staff surfaces; whitespace-only PDF line wrapping is ignored.

| Field | Teacher Notes Word | Word pack | Teacher Notes PDF | TA brief PDF |
|---|---|---|---|---|
| Teacher card | PASS | PASS | PASS | PASS |
| Forty minute route | PASS | PASS | PASS | PASS |
| Preparation | PASS | PASS | PASS | PASS |
| Access and regulation | PASS | PASS | PASS | PASS |
| Assessment | PASS | PASS | PASS | PASS |
| Model and answers | PASS | PASS | PASS | PASS |
| Arrival answers | PASS | PASS | PASS | PASS |
| Shared activity reasoning | PASS | PASS | PASS | PASS |
| Exit responses | PASS | PASS | PASS | PASS |
| Teaching and evidence record | PASS | PASS | PASS | PASS |
| Look for | PASS | PASS | PASS | PASS |
| Media | PASS | PASS | PASS | PASS |
| Source credits | PASS | PASS | PASS | PASS |
| Planning | PASS | PASS | PASS | PASS |
| Teaching sequence | PASS | PASS | PASS | PASS |
| Arrival questions and answers | PASS | PASS | PASS | PASS |
| Hinge and diagnoses | PASS | PASS | PASS | PASS |
| Parallel hinge after a teaching move | PASS | PASS | PASS | PASS |
| LOOP | PASS | PASS | PASS | PASS |
| Target opportunities | PASS | PASS | PASS | PASS |
| Exit guidance | PASS | PASS | PASS | PASS |
| If behind | PASS | PASS | PASS | PASS |
| Planning and evaluation record | PASS | PASS | PASS | PASS |
| Sources | PASS | PASS | PASS | PASS |
| Book evidence and feedback | PASS | PASS | PASS | PASS |
| Planned adaptations | PASS | PASS | PASS | PASS |
| Invite a response · two per route | PASS | PASS | PASS | PASS |
| F6 exact preparation | PASS | PASS | PASS | PASS |
| F8 full IEDP line | PASS | PASS | PASS | PASS |
| F8 EAL is not SEN | PASS | PASS | PASS | PASS |
| F8 Supported 1/2 Standard 1/2 Stretch 1/2 | PASS | PASS | PASS | PASS |
| A4 geometry | PASS | PASS | PASS | PASS |

| Surface | Characters | Missing source chunks | Banned words | Author |
|---|---:|---:|---:|---|
| Teacher_Notes.docx | 20439 | 0 | 0 | Matt Roper |
| Editable_Pack.docx | 30122 | 0 | 0 | Matt Roper |
| Teacher_Notes.pdf | 20479 | 0 | 0 | Matt Roper |
| TA_Brief.pdf | 20479 | 0 | 0 | Matt Roper |

Planned adaptations table: 5 body rows; 2 columns. Invite a response table: 6 body rows; 3 columns.
Word pack: F3 is an exact heading; organiser comes first; 5 real page breaks; 13 embedded pictures/logos.

The E-number labels immediately followed by “Assessment source” are evidence-card identifiers and are exempt from the version-word scan.

All DOCX files were rendered through LibreOffice; representative page images were inspected. Full reviewer Office and print checks remain separate from these static checks.


### Staff document checks — LAUNCH_RE_A2_W04

Static checks against the final lesson staff content. Every source paragraph and table cell survives on all four required staff surfaces; whitespace-only PDF line wrapping is ignored.

| Field | Teacher Notes Word | Word pack | Teacher Notes PDF | TA brief PDF |
|---|---|---|---|---|
| Teacher card | PASS | PASS | PASS | PASS |
| Forty minute route | PASS | PASS | PASS | PASS |
| Preparation | PASS | PASS | PASS | PASS |
| Access and regulation | PASS | PASS | PASS | PASS |
| Assessment | PASS | PASS | PASS | PASS |
| Model and answers | PASS | PASS | PASS | PASS |
| Arrival answers | PASS | PASS | PASS | PASS |
| Shared activity reasoning | PASS | PASS | PASS | PASS |
| Exit responses | PASS | PASS | PASS | PASS |
| Teaching and evidence record | PASS | PASS | PASS | PASS |
| Look for | PASS | PASS | PASS | PASS |
| Media | PASS | PASS | PASS | PASS |
| Source credits | PASS | PASS | PASS | PASS |
| Planning | PASS | PASS | PASS | PASS |
| Teaching sequence | PASS | PASS | PASS | PASS |
| Arrival questions and answers | PASS | PASS | PASS | PASS |
| Hinge and diagnoses | PASS | PASS | PASS | PASS |
| Parallel hinge after a teaching move | PASS | PASS | PASS | PASS |
| LOOP | PASS | PASS | PASS | PASS |
| Target opportunities | PASS | PASS | PASS | PASS |
| Exit guidance | PASS | PASS | PASS | PASS |
| If behind | PASS | PASS | PASS | PASS |
| Planning and evaluation record | PASS | PASS | PASS | PASS |
| Sources | PASS | PASS | PASS | PASS |
| Book evidence and feedback | PASS | PASS | PASS | PASS |
| Planned adaptations | PASS | PASS | PASS | PASS |
| Invite a response · two per route | PASS | PASS | PASS | PASS |
| F6 exact preparation | PASS | PASS | PASS | PASS |
| F8 full IEDP line | PASS | PASS | PASS | PASS |
| F8 EAL is not SEN | PASS | PASS | PASS | PASS |
| F8 Supported 1/2 Standard 1/2 Stretch 1/2 | PASS | PASS | PASS | PASS |
| A4 geometry | PASS | PASS | PASS | PASS |

| Surface | Characters | Missing source chunks | Banned words | Author |
|---|---:|---:|---:|---|
| Teacher_Notes.docx | 20640 | 0 | 0 | Matt Roper |
| Editable_Pack.docx | 30449 | 0 | 0 | Matt Roper |
| Teacher_Notes.pdf | 20681 | 0 | 0 | Matt Roper |
| TA_Brief.pdf | 20681 | 0 | 0 | Matt Roper |

Planned adaptations table: 5 body rows; 2 columns. Invite a response table: 6 body rows; 3 columns.
Word pack: F3 is an exact heading; organiser comes first; 5 real page breaks; 13 embedded pictures/logos.

The E-number labels immediately followed by “Assessment source” are evidence-card identifiers and are exempt from the version-word scan.

All DOCX files were rendered through LibreOffice; representative page images were inspected. Full reviewer Office and print checks remain separate from these static checks.


### Staff document checks — LAUNCH_RE_A2_W05

Static checks against the final lesson staff content. Every source paragraph and table cell survives on all four required staff surfaces; whitespace-only PDF line wrapping is ignored.

| Field | Teacher Notes Word | Word pack | Teacher Notes PDF | TA brief PDF |
|---|---|---|---|---|
| Teacher card | PASS | PASS | PASS | PASS |
| Forty minute route | PASS | PASS | PASS | PASS |
| Preparation | PASS | PASS | PASS | PASS |
| Access and regulation | PASS | PASS | PASS | PASS |
| Assessment | PASS | PASS | PASS | PASS |
| Model and answers | PASS | PASS | PASS | PASS |
| Arrival answers | PASS | PASS | PASS | PASS |
| Shared activity reasoning | PASS | PASS | PASS | PASS |
| Exit responses | PASS | PASS | PASS | PASS |
| Teaching and evidence record | PASS | PASS | PASS | PASS |
| Look for | PASS | PASS | PASS | PASS |
| Media | PASS | PASS | PASS | PASS |
| Source credits | PASS | PASS | PASS | PASS |
| Planning | PASS | PASS | PASS | PASS |
| Teaching sequence | PASS | PASS | PASS | PASS |
| Arrival questions and answers | PASS | PASS | PASS | PASS |
| Hinge and diagnoses | PASS | PASS | PASS | PASS |
| Parallel hinge after a teaching move | PASS | PASS | PASS | PASS |
| LOOP | PASS | PASS | PASS | PASS |
| Target opportunities | PASS | PASS | PASS | PASS |
| Exit guidance | PASS | PASS | PASS | PASS |
| If behind | PASS | PASS | PASS | PASS |
| Planning and evaluation record | PASS | PASS | PASS | PASS |
| Sources | PASS | PASS | PASS | PASS |
| Book evidence and feedback | PASS | PASS | PASS | PASS |
| Planned adaptations | PASS | PASS | PASS | PASS |
| Invite a response · two per route | PASS | PASS | PASS | PASS |
| F6 exact preparation | PASS | PASS | PASS | PASS |
| F8 full IEDP line | PASS | PASS | PASS | PASS |
| F8 EAL is not SEN | PASS | PASS | PASS | PASS |
| F8 Supported 1/2 Standard 1/2 Stretch 1/2 | PASS | PASS | PASS | PASS |
| A4 geometry | PASS | PASS | PASS | PASS |

| Surface | Characters | Missing source chunks | Banned words | Author |
|---|---:|---:|---:|---|
| Teacher_Notes.docx | 21074 | 0 | 0 | Matt Roper |
| Editable_Pack.docx | 31005 | 0 | 0 | Matt Roper |
| Teacher_Notes.pdf | 21111 | 0 | 0 | Matt Roper |
| TA_Brief.pdf | 21111 | 0 | 0 | Matt Roper |

Planned adaptations table: 5 body rows; 2 columns. Invite a response table: 6 body rows; 3 columns.
Word pack: F3 is an exact heading; organiser comes first; 5 real page breaks; 13 embedded pictures/logos.

The E-number labels immediately followed by “Assessment source” are evidence-card identifiers and are exempt from the version-word scan.

All DOCX files were rendered through LibreOffice; representative page images were inspected. Full reviewer Office and print checks remain separate from these static checks.


### Staff document checks — LAUNCH_RE_A2_W06

Static checks against the final lesson staff content. Every source paragraph and table cell survives on all four required staff surfaces; whitespace-only PDF line wrapping is ignored.

| Field | Teacher Notes Word | Word pack | Teacher Notes PDF | TA brief PDF |
|---|---|---|---|---|
| Teacher card | PASS | PASS | PASS | PASS |
| Forty minute route | PASS | PASS | PASS | PASS |
| Preparation | PASS | PASS | PASS | PASS |
| Access and regulation | PASS | PASS | PASS | PASS |
| Assessment | PASS | PASS | PASS | PASS |
| Model and answers | PASS | PASS | PASS | PASS |
| Arrival answers | PASS | PASS | PASS | PASS |
| Shared activity reasoning | PASS | PASS | PASS | PASS |
| Exit responses | PASS | PASS | PASS | PASS |
| Teaching and evidence record | PASS | PASS | PASS | PASS |
| Look for | PASS | PASS | PASS | PASS |
| Media | PASS | PASS | PASS | PASS |
| Source credits | PASS | PASS | PASS | PASS |
| Planning | PASS | PASS | PASS | PASS |
| Teaching sequence | PASS | PASS | PASS | PASS |
| Arrival questions and answers | PASS | PASS | PASS | PASS |
| Hinge and diagnoses | PASS | PASS | PASS | PASS |
| Parallel hinge after a teaching move | PASS | PASS | PASS | PASS |
| LOOP | PASS | PASS | PASS | PASS |
| Target opportunities | PASS | PASS | PASS | PASS |
| Exit guidance | PASS | PASS | PASS | PASS |
| If behind | PASS | PASS | PASS | PASS |
| Planning and evaluation record | PASS | PASS | PASS | PASS |
| Sources | PASS | PASS | PASS | PASS |
| Book evidence and feedback | PASS | PASS | PASS | PASS |
| Planned adaptations | PASS | PASS | PASS | PASS |
| Invite a response · two per route | PASS | PASS | PASS | PASS |
| F6 exact preparation | PASS | PASS | PASS | PASS |
| F8 full IEDP line | PASS | PASS | PASS | PASS |
| F8 EAL is not SEN | PASS | PASS | PASS | PASS |
| F8 Supported 1/2 Standard 1/2 Stretch 1/2 | PASS | PASS | PASS | PASS |
| A4 geometry | PASS | PASS | PASS | PASS |

| Surface | Characters | Missing source chunks | Banned words | Author |
|---|---:|---:|---:|---|
| Teacher_Notes.docx | 21187 | 0 | 0 | Matt Roper |
| Editable_Pack.docx | 30878 | 0 | 0 | Matt Roper |
| Teacher_Notes.pdf | 21187 | 0 | 0 | Matt Roper |
| TA_Brief.pdf | 21187 | 0 | 0 | Matt Roper |

Planned adaptations table: 5 body rows; 2 columns. Invite a response table: 6 body rows; 3 columns.
Word pack: F3 is an exact heading; organiser comes first; 5 real page breaks; 13 embedded pictures/logos.

The E-number labels immediately followed by “Assessment source” are evidence-card identifiers and are exempt from the version-word scan.

All DOCX files were rendered through LibreOffice; representative page images were inspected. Full reviewer Office and print checks remain separate from these static checks.


### Staff document checks — LAUNCH_RE_A2_W07

Static checks against the final lesson staff content. Every source paragraph and table cell survives on all four required staff surfaces; whitespace-only PDF line wrapping is ignored.

| Field | Teacher Notes Word | Word pack | Teacher Notes PDF | TA brief PDF |
|---|---|---|---|---|
| Teacher card | PASS | PASS | PASS | PASS |
| Forty minute route | PASS | PASS | PASS | PASS |
| Preparation | PASS | PASS | PASS | PASS |
| Access and regulation | PASS | PASS | PASS | PASS |
| Assessment | PASS | PASS | PASS | PASS |
| Model and answers | PASS | PASS | PASS | PASS |
| Arrival answers | PASS | PASS | PASS | PASS |
| Shared activity reasoning | PASS | PASS | PASS | PASS |
| Exit responses | PASS | PASS | PASS | PASS |
| Teaching and evidence record | PASS | PASS | PASS | PASS |
| Look for | PASS | PASS | PASS | PASS |
| Media | PASS | PASS | PASS | PASS |
| Source credits | PASS | PASS | PASS | PASS |
| Planning | PASS | PASS | PASS | PASS |
| Teaching sequence | PASS | PASS | PASS | PASS |
| Arrival questions and answers | PASS | PASS | PASS | PASS |
| Hinge and diagnoses | PASS | PASS | PASS | PASS |
| Parallel hinge after a teaching move | PASS | PASS | PASS | PASS |
| LOOP | PASS | PASS | PASS | PASS |
| Target opportunities | PASS | PASS | PASS | PASS |
| Exit guidance | PASS | PASS | PASS | PASS |
| If behind | PASS | PASS | PASS | PASS |
| Planning and evaluation record | PASS | PASS | PASS | PASS |
| Sources | PASS | PASS | PASS | PASS |
| Book evidence and feedback | PASS | PASS | PASS | PASS |
| Planned adaptations | PASS | PASS | PASS | PASS |
| Invite a response · two per route | PASS | PASS | PASS | PASS |
| F6 exact preparation | PASS | PASS | PASS | PASS |
| F8 full IEDP line | PASS | PASS | PASS | PASS |
| F8 EAL is not SEN | PASS | PASS | PASS | PASS |
| F8 Supported 1/2 Standard 1/2 Stretch 1/2 | PASS | PASS | PASS | PASS |
| A4 geometry | PASS | PASS | PASS | PASS |

| Surface | Characters | Missing source chunks | Banned words | Author |
|---|---:|---:|---:|---|
| Teacher_Notes.docx | 22420 | 0 | 0 | Matt Roper |
| Editable_Pack.docx | 32809 | 0 | 0 | Matt Roper |
| Teacher_Notes.pdf | 22472 | 0 | 0 | Matt Roper |
| TA_Brief.pdf | 22472 | 0 | 0 | Matt Roper |

Planned adaptations table: 5 body rows; 2 columns. Invite a response table: 6 body rows; 3 columns.
Word pack: F3 is an exact heading; organiser comes first; 5 real page breaks; 13 embedded pictures/logos.

The E-number labels immediately followed by “Assessment source” are evidence-card identifiers and are exempt from the version-word scan.

All DOCX files were rendered through LibreOffice; representative page images were inspected. Full reviewer Office and print checks remain separate from these static checks.


## PDF geometry and metadata (created staff PDFs only)

| File | Pages | First-page width × height pt | All pages A4 | Title | Author |
|---|---:|---|---|---|---|
| BUILD_RE_A1_W08_First_Lesson_Back.pdf | 1 | 595.304 × 841.890 | True | Special things, respect and belonging | Matt Roper |
| BUILD_RE_A1_W08_TA_Brief.pdf | 4 | 595.304 × 841.890 | True | Special things, respect and belonging | Matt Roper |
| BUILD_RE_A1_W08_Teacher_Notes.pdf | 4 | 595.304 × 841.890 | True | Special things, respect and belonging | Matt Roper |
| BUILD_RE_A2_W01_TA_Brief.pdf | 6 | 595.304 × 841.890 | True | A festival of light: Diwali | Matt Roper |
| BUILD_RE_A2_W01_Teacher_Notes.pdf | 6 | 595.304 × 841.890 | True | A festival of light: Diwali | Matt Roper |
| BUILD_RE_A2_W02_TA_Brief.pdf | 6 | 595.304 × 841.890 | True | Comparing light in celebrations | Matt Roper |
| BUILD_RE_A2_W02_Teacher_Notes.pdf | 6 | 595.304 × 841.890 | True | Comparing light in celebrations | Matt Roper |
| BUILD_RE_A2_W03_TA_Brief.pdf | 6 | 595.304 × 841.890 | True | Retelling a festival story | Matt Roper |
| BUILD_RE_A2_W03_Teacher_Notes.pdf | 6 | 595.304 × 841.890 | True | Retelling a festival story | Matt Roper |
| BUILD_RE_A2_W04_TA_Brief.pdf | 6 | 595.304 × 841.890 | True | Taking part respectfully | Matt Roper |
| BUILD_RE_A2_W04_Teacher_Notes.pdf | 6 | 595.304 × 841.890 | True | Taking part respectfully | Matt Roper |
| BUILD_RE_A2_W05_TA_Brief.pdf | 6 | 595.304 × 841.890 | True | Hope and remembrance | Matt Roper |
| BUILD_RE_A2_W05_Teacher_Notes.pdf | 6 | 595.304 × 841.890 | True | Hope and remembrance | Matt Roper |
| BUILD_RE_A2_W06_TA_Brief.pdf | 6 | 595.304 × 841.890 | True | A big question | Matt Roper |
| BUILD_RE_A2_W06_Teacher_Notes.pdf | 6 | 595.304 × 841.890 | True | A big question | Matt Roper |
| BUILD_RE_A2_W07_TA_Brief.pdf | 6 | 595.304 × 841.890 | True | Festival reflection and UAS evidence | Matt Roper |
| BUILD_RE_A2_W07_Teacher_Notes.pdf | 6 | 595.304 × 841.890 | True | Festival reflection and UAS evidence | Matt Roper |
| GROW_RE_A1_W08_First_Lesson_Back.pdf | 1 | 595.304 × 841.890 | True | Shared values and what we remember | Matt Roper |
| GROW_RE_A1_W08_TA_Brief.pdf | 6 | 595.304 × 841.890 | True | Shared values and what we remember | Matt Roper |
| GROW_RE_A1_W08_Teacher_Notes.pdf | 6 | 595.304 × 841.890 | True | Shared values and what we remember | Matt Roper |
| GROW_RE_A2_W01_TA_Brief.pdf | 6 | 595.304 × 841.890 | True | Belonging across faiths | Matt Roper |
| GROW_RE_A2_W01_Teacher_Notes.pdf | 6 | 595.304 × 841.890 | True | Belonging across faiths | Matt Roper |
| GROW_RE_A2_W02_TA_Brief.pdf | 6 | 595.304 × 841.890 | True | Place of worship enquiry | Matt Roper |
| GROW_RE_A2_W02_Teacher_Notes.pdf | 6 | 595.304 × 841.890 | True | Place of worship enquiry | Matt Roper |
| GROW_RE_A2_W03_TA_Brief.pdf | 6 | 595.304 × 841.890 | True | Religious practice and subject vocabulary | Matt Roper |
| GROW_RE_A2_W03_Teacher_Notes.pdf | 6 | 595.304 × 841.890 | True | Religious practice and subject vocabulary | Matt Roper |
| GROW_RE_A2_W04_TA_Brief.pdf | 6 | 595.304 × 841.890 | True | Big question: do beliefs make us who we are? | Matt Roper |
| GROW_RE_A2_W04_Teacher_Notes.pdf | 6 | 595.304 × 841.890 | True | Big question: do beliefs make us who we are? | Matt Roper |
| GROW_RE_A2_W05_TA_Brief.pdf | 6 | 595.304 × 841.890 | True | Questions for a faith or belief visitor | Matt Roper |
| GROW_RE_A2_W05_Teacher_Notes.pdf | 6 | 595.304 × 841.890 | True | Questions for a faith or belief visitor | Matt Roper |
| GROW_RE_A2_W06_TA_Brief.pdf | 6 | 595.304 × 841.890 | True | Personal values and respect for others | Matt Roper |
| GROW_RE_A2_W06_Teacher_Notes.pdf | 6 | 595.304 × 841.890 | True | Personal values and respect for others | Matt Roper |
| GROW_RE_A2_W07_TA_Brief.pdf | 6 | 595.304 × 841.890 | True | Belief and identity assessment | Matt Roper |
| GROW_RE_A2_W07_Teacher_Notes.pdf | 6 | 595.304 × 841.890 | True | Belief and identity assessment | Matt Roper |
| LAUNCH_RE_A1_W08_First_Lesson_Back.pdf | 1 | 595.304 × 841.890 | True | Evidence, belief and choices | Matt Roper |
| LAUNCH_RE_A1_W08_TA_Brief.pdf | 4 | 595.304 × 841.890 | True | Evidence, belief and choices | Matt Roper |
| LAUNCH_RE_A1_W08_Teacher_Notes.pdf | 4 | 595.304 × 841.890 | True | Evidence, belief and choices | Matt Roper |
| LAUNCH_RE_A2_W01_TA_Brief.pdf | 6 | 595.304 × 841.890 | True | Worship, prayer and practice | Matt Roper |
| LAUNCH_RE_A2_W01_Teacher_Notes.pdf | 6 | 595.304 × 841.890 | True | Worship, prayer and practice | Matt Roper |
| LAUNCH_RE_A2_W02_TA_Brief.pdf | 6 | 595.304 × 841.890 | True | Pilgrimage and sacred places | Matt Roper |
| LAUNCH_RE_A2_W02_Teacher_Notes.pdf | 6 | 595.304 × 841.890 | True | Pilgrimage and sacred places | Matt Roper |
| LAUNCH_RE_A2_W03_TA_Brief.pdf | 6 | 595.304 × 841.890 | True | Rites of passage and community | Matt Roper |
| LAUNCH_RE_A2_W03_Teacher_Notes.pdf | 6 | 595.304 × 841.890 | True | Rites of passage and community | Matt Roper |
| LAUNCH_RE_A2_W04_TA_Brief.pdf | 6 | 595.304 × 841.890 | True | Moral teachings across worldviews | Matt Roper |
| LAUNCH_RE_A2_W04_Teacher_Notes.pdf | 6 | 595.304 × 841.890 | True | Moral teachings across worldviews | Matt Roper |
| LAUNCH_RE_A2_W05_TA_Brief.pdf | 6 | 595.304 × 841.890 | True | Comparing responses to a life question | Matt Roper |
| LAUNCH_RE_A2_W05_Teacher_Notes.pdf | 6 | 595.304 × 841.890 | True | Comparing responses to a life question | Matt Roper |
| LAUNCH_RE_A2_W06_TA_Brief.pdf | 6 | 595.304 × 841.890 | True | A structured “compare” response | Matt Roper |
| LAUNCH_RE_A2_W06_Teacher_Notes.pdf | 6 | 595.304 × 841.890 | True | A structured “compare” response | Matt Roper |
| LAUNCH_RE_A2_W07_TA_Brief.pdf | 6 | 595.304 × 841.890 | True | Beliefs and practices assessment | Matt Roper |
| LAUNCH_RE_A2_W07_Teacher_Notes.pdf | 6 | 595.304 × 841.890 | True | Beliefs and practices assessment | Matt Roper |

## Office render scope

The document workflow produced 51 render results covering 404 pages (48 DOCX documents and three First Lesson Back cards). Static bounds found no blank pages or text outside a page. Representative page images were inspected. These findings do not replace the reviewer’s full Office and print checks.

## Current file hashes

Each ZIP has its own SHA256SUMS. Per-lesson QA also records old/new SHA-256 and changed/unchanged status for each current file against its recovered baseline. Missing baseline pupil PDFs are explicitly classified as F4 pending, not as unchanged or passed.
