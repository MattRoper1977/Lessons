# AMEND-3R-GC1 — SECOND ISSUE

- **Issued:** 2026-09-10
- **Status:** SECOND ISSUE — canonical
- **Sentinels:** `mbm-fin5-2026-09-10-TOP` / `mbm-fin5-2026-09-10-BOTTOM`
- **Supersedes:** every earlier AMEND-3R-GC1 wording, in chat or in any context.
  There is nothing to reconcile against and nothing to paraphrase.
- **Source:** ORDER FIN5 §B, transcribed verbatim below.

> **Why this file exists.** The first issue of this order lived only in chat. When
> that context was lost the order was unrecoverable and GC1 blocked at P0–P1 with
> zero writes. Standing rule from here: **any order with gates gets a
> `docs/orders/` file before it runs.**

---

## §B · AMEND-3R-GC1 — CANONICAL, SECOND ISSUE

This text is now the order. Every earlier AMEND-3R-GC1 wording, in chat or in any context, is
SUPERSEDED. There is nothing to reconcile against and nothing to paraphrase.

B0. FIRST ACTION, BEFORE ANY PHASE. Commit this §B verbatim to the Lessons repo at
    docs/orders/AMEND-3R-GC1.md, dated today, carrying the sentinel above and the words SECOND
    ISSUE. No phase starts until that commit exists. The original block was caused by an order that
    lived only in chat; this closes it. Standing rule from here: any order with gates gets a
    docs/orders/ file before it runs.

### SUBJECT

The GROW Computing unit, AQA UAS 71638 Programming with Scratch (unit 6), Level One, GROW pathway,
8 × 40 min. Weeks 1–6 are Matt's existing packs (34 + 59 files). Weeks 7–8 are the build delivered
2026-09-09 (32 files, zip 1,053,102 B). Twenty-three .sb3 across the eight weeks. Six AQA outcomes,
every one of them evidenced by the Summary sheet only.

### STANDING RULINGS

R1. Home is ICT/Teaching_Packs/GROW_Computing/ — a SECOND unit under the existing ICT subject page.
    The live GROW ICT unit's URLs are NEVER renamed, moved or shadowed.
R2. Unit weeks are SEQUENCE LABELS and are EXEMPT from R-CAL-1 and RX4 relabelling. They are bound
    to pupil save filenames W01_MyCode…W08_Final and to printed booklets already in pupils' hands.
R3. Served lessons link the sibling .sb3 file. The base64 data: URI stays as the offline fallback —
    managed browsers can block data: downloads. Both routes ship; neither replaces the other.
R4. Teacher_Only material sits behind the ECA-1 guide toggle on served surfaces, hidden by default.
R5. One unit zip plus three collections. No per-week zips (HC5 size ruling).
R6. Content PR first, resources.json PR second (GLV3). Never combined.
R7. NO VARIABLES anywhere in this unit. Scoring is the separate 122058 unit and building it here
    spends that unit's assessed construction early. This binds the paper route too.
R8. NEW. The unit must be completable on paper, end to end, by a pupil with no device, and the
    paper route must produce evidence of the same six outcomes. Screen and paper are two routes to
    one qualification, not a main route and a consolation worksheet.
R9. NEW. Awarding-body documents are never altered. The AQA Summary sheet is completed identically
    whichever route a pupil took. Route is recorded in the teacher guide, not on AQA's form.

### PHASES

P2 · REPAIR WEEKS 1–6 IN PLACE
    Four audited defects. Fix all four before anything is placed.
    d1 Print route dead in all six. The @media print CSS hides header/main/footer and shows
       .print-record; Weeks 1–2 ship an EMPTY .print-record, Weeks 3–6 dropped the element. Copy
       back the working container and the beforeprint filler (fillPrint) from Weeks 7–8.
       This is now load-bearing: P2P depends on printing actually working.
    d2 Duplicate id "centre" in the Week 1 and Week 2 lessons.
    d3 The two Start_Here hubs do not cross-link and neither mentions Weeks 7–8.
    d4 Zero estate furniture in all eight lessons — no way-home, no Made by Matt, no guide toggle,
       no prev/next, no usage layer. Same class as the HC6 companions; fix it the same way.
    Gates at exit: G1 G2 G3 G4 G5 G6 G7 G11.

P2P · THE PAPER COMPLETION ROUTE  ·  NEW, AND THE REASON THIS ORDER WAS RE-ISSUED
    Diagnose it correctly before you build. The unit is NOT short of printable material — it
    already ships Pupil_Booklet, Step_by_Step and Challenge in docx and pdf for every week. What it
    lacks is a route to COMPLETION AND EVIDENCE without a device, because the assessed construction
    is a Scratch project. Building more worksheets does not satisfy R8. Building an evidence path
    does.
    Per week, author a Paper_Route/ set that carries:
    p1 A block-writing surface. Pupils write Scratch scripts in block syntax on a printed grid —
       hat block, stack, inputs — one grid per script the screen lesson expects. The grid is the
       paper equivalent of the editor, so it must be able to hold every block the week actually
       uses and no more (R7 bars variable blocks from the grid entirely).
    p2 The maze printed to its real geometry, so paper tracing and screen behaviour agree. Walls
       [[-220,-160,440,20],[-220,140,440,20],[-220,-140,20,280],[200,-140,20,280],[-70,-140,20,220],
       [50,-80,20,220]], Player start (-180,-120), Finish (180,120). Print a coordinate grid a pupil
       can move a counter on, not a decorative picture.
    p3 Prediction and trace tables — predict, trace, compare — which is the paper form of running
       the project and is what a moderator will read as evidence of understanding.
    p4 Week 7 specific: a design sheet for the Hazard glide between (0,-100) and (0,100), and the
       equal Star-collectible alternative, both with the coordinates and the contact rule stated as
       belonging to Player. Both routes stay available on paper exactly as on screen, because the
       Star route is the awarding body's own exemplar.
    p5 Week 8 specific: the five checks (arrows, walls, finish, feature, restart) as an expected /
       actual / cause / repair / re-check table, plus the three seeded faults printed as script
       listings — down arrow using change y by 10, wall check with no forever so it runs once at the
       flag, win script with no empty say so the message survives restart. Finish and feature must
       still PASS on paper by design, so the paper pupil learns the same lesson: a repair must not
       break a passing check.
    p6 A completion record per week that maps that week's work to the outcome(s) it evidences, in
       the same words the Summary sheet uses. This is the piece that makes it a route rather than
       an activity.
    p7 Teacher answers for every paper artefact, in Teacher_Only/, behind the R4 toggle on any
       served surface.
    Format: docx source plus pdf, matching the existing pack styling exactly — Normal DejaVu Sans
    11.5 #172A22, Title 25 bold, Heading 2 14 bold, page break before each mid-doc Title, footer
    "Week n <label>  |  <page>", PDFs converted by LibreOffice in the same container. It must look
    like the same unit, not a bolt-on.
    The served lesson also prints it: the .print-record repaired in P2 emits that week's paper route
    so a teacher can produce it from the lesson page with no download. Both delivery paths ship.
    Gates at exit: G5 G14 G15 G16.

P2Q · THE SECOND UNIT  ·  GATED, DO NOT START
    Matt has said one other unit needs the same change. He has not named it. My inference is the
    live ICT/Teaching_Packs/GROW/ unit (GROW ICT Autumn 1, W1–W7), on the grounds that it is the
    only other unit in the ICT tree and shares the device-dependent construction problem. That is
    an inference, not an instruction.
    Do NOT touch any second unit until Matt names it. When he does, apply R8, R9 and P2P's p1–p7
    adapted to that unit's own construction, with the same gates, as a SEPARATE PR from GC1's.
    Nothing in P2Q blocks P2, P2P, P3, P4, P5 or P6.

P3 · PLACE THE UNIT
    Build ICT/Teaching_Packs/GROW_Computing/ per R1. Eight weeks, pack anatomy preserved:
    Interactive.html · Teaching_Slides.pptx + .pdf · Pupil_Booklet / Step_by_Step / Challenge
    docx + pdf · Paper_Route/ from P2P · Teacher_Only/ guide + W0n_Teacher_Model.sb3 ·
    Scratch_Projects/ starter, recovery, bug-hunt. Cross-link both hubs (d3) and add the ICT
    subject-page entry. There is no ICT/index.html or README today — create neither as a side
    effect; if the subject page needs one, that is its own PR and it is not this one.
    Gates at exit: G8 G12.

P4 · WIRE THE SERVED SURFACES
    R3 sibling .sb3 links on every week, data: fallback retained. R4 toggle on all Teacher_Only
    content including P2P's answers. Estate furniture live, not merely present in markup. Every
    week's page offers the paper route visibly — a pupil or cover teacher must be able to find it
    without knowing it exists.
    Gates at exit: G9 G10 G14.

P5 · PACKAGE
    One unit zip plus three collections per R5; the paper route travels inside the unit zip, not as
    a fourth artefact. Record every artefact's byte size and md5 in the PR body, sizes as BYTES and
    unit-labelled per §D2.
    Gate at exit: G13.

P6 · PUBLISH — MATT HAS RULED: EDUCATION SIDE
    Destination is madebymatt.uk, the education domain. Full catalogue entry, card and search text.
    Branch (b), school-network-only, is withdrawn and is not to be revisited.
    R6 sequencing: content PR, then resources.json PR. Served proof required: the run id, both jobs
    green, and a fetch of one lesson at its live URL — plus one fetch proving the paper route
    reaches a pupil, either as a served file or by printing from the lesson page.
    Gates at exit: G5 G14 G15 re-run against the SERVED routes, not the working tree.

### GATES

G1  All 23 .sb3 pass the official Scratch 3 schema (npm scratch-parser). 23/23 or red.
G2  node --check passes on all eight lessons' JS.
G3  Zero storage APIs (localStorage, sessionStorage, indexedDB) across all eight lessons.
G4  Zero duplicate ids across all eight lessons. Specifically proves d2 dead.
G5  Print route live on all eight: .print-record present AND non-empty after beforeprint, verified
    under Chromium print emulation, not by reading the CSS. A blank page is a red. After P2P, the
    printed output must be that week's paper route, not a stub.
G6  Estate furniture present and functional on all eight: way-home, Made by Matt, guide toggle,
    prev/next, usage layer. Count, do not eyeball.
G7  External hrefs allowlisted to exactly two — the scratch.mit.edu editor and the AQA unit page.
    Any third external href is a red.
G8  Link integrity: the existing 26/26 and 57/57 both still pass, plus the new cross-links and the
    subject-page entry. Zero broken, zero orphans.
G9  Every week's sibling .sb3 link resolves at its served path AND the data: fallback still loads.
    Both proven per week, eight and eight.
G10 Zero teacher-only or answer text in the default DOM of any served lesson. Toggle closed by
    default; open it and the content appears. Two assertions, run both. Includes P2P answers.
G11 Zero variable blocks in all 23 .sb3 (R7). Assert on block opcodes, not filenames. The paper
    route's block-writing grids must offer no variable block either.
G12 No calendar or spine token is bound to W01–W08 anywhere in the unit (R2), and the pupil save
    filenames W01_MyCode…W08_Final appear unchanged in the lessons, the booklets and the new paper
    route.
G13 Chromium drive at 390px across all eight lessons: every stage, all three routes, every model
    button, the print record filled, and in Week 8 all five checks run before AND after each of the
    three repairs. Zero console errors.
    Note: the first block-walker used in the Weeks 7–8 build was blind to CONDITION inputs and
    returned two vacuous passes. If you reuse it, prove it sees conditions before you trust it.
G14 NEW · PAPER ROUTE EXISTS AND IS DEVICE-FREE. Every one of the eight weeks has a Paper_Route
    artefact in docx and pdf, and a pupil can complete that week using only printed matter and a
    pen. Red if any week's paper route requires a screen, a login, a QR scan or a download to
    finish. Eight of eight or red.
G15 NEW · EVIDENCE PARITY. Every one of the six AQA outcomes is reachable by the paper route alone,
    and the mapping is stated in writing in the teacher guide with the same wording the Summary
    sheet uses. Assert per outcome, six of six. This is the gate that decides whether R8 was met;
    the others only decide whether it was met tidily.
G16 NEW · AWARDING-BODY DOCUMENTS UNTOUCHED. Zero modifications to the AQA Summary sheet or any
    other awarding-body artefact. Diff them; byte-identical or red. Route is recorded in the
    teacher guide only (R9).

Any gate red halts its phase. It does not halt phases that do not depend on it.

---

`mbm-fin5-2026-09-10-BOTTOM`
