# Lesson standard 2026/27 — the authoring reference

Written under ORDER CX2 §4.1 (`docs/orders/CX2_FINISH_2026-09-15.md`), 15 September 2026.
This is a docs file. It is not served: `docs/` sits in the Site publisher's `SKIP` set
(`domain-split/build_education.py`, Site main `c63149ead07c33e35d78bbdc8935b7934e7d292b`),
confirmed in `CX2_CHECKPOINT.md` §1. Every lesson authored from here on cites this file by path
and by the commit that carried the version it was authored against.

The base is master order §25.2–§25.5, reproduced in Part A. Each line is annotated with the
Curriculum Policy clause that corroborates it (R9: the policy corroborates §25; it does not
replace it). Part B carries the CX2 §4.2–§4.8 refinements. Part C is the preservation list
that every later lesson inherits unchanged. Part D is the acceptance checklist.

## 0. Sources, by identity

| Source | Identity | Where it is |
|---|---|---|
| Master order §25.1–§25.5 (Lessons reference standard) | text as supplied to this session on 15 September 2026; the master order is not committed in this repository | quoted verbatim in Part A |
| Progress Schools Curriculum Policy 2026/2027, Issue 2 (August 2026) | `PS_Curriculum_Policy_-_2026_2027.pdf`, 444,764 bytes, 41 pages, SHA-256 `593ab59361d1f1d22360a0ba12bdb96e08dcd94404a07368c09768414e982aed` | supplied by Matt in this session; not committed |
| Feedback & Marking Policy 2025/2026 (Pilot), Issue 1, May 2026 — master-order reference copy, 16 pages | `Feedback_Policy_2025-2026_-_Pilot.pdf`, 208,449 bytes, SHA-256 `41046284a00c9218679b946134cbc6e53c1897aad28b15fc4bd4aa963720ff3b` | supplied by Matt in this session; Drive `1D8lpR-_1uQc2ND5C02T7BUfM8myBrC6M`; not committed |
| Same policy, Issue 1, second copy, 13 pages | `Feedback_Policy_-_2025_2026_Pilot.pdf`, 204,058 bytes, SHA-256 `aa41d67963846cf35e9bb6e53e708c7b46725c2d5cef432c2e1994a78e434e53` | supplied by Matt in this session; Drive `15hGPn0lGji4WRt-A_L2_19nidpP6XMRb`; not committed |
| Feedback & Marking Policy Issue 2 | **not found** — session uploads, all repository history, Drive titles and full text searched (`CX2_CHECKPOINT.md` §1). Issue 1 remains the code source (R9). | — |
| Reading-band instrument | `_sownb/vb/tools/g26_reading_band.py` v1.3.0, bands from `_sownb/STYLE_CONTRACT.json` row `reading.pathway.band` (both at commit `40f60d78841e95855aa345e26482dae6d7fd7a32`) | committed |

The two Feedback Policy copies carry the same Code/Meaning table; they differ only in the name
of the school's evidence platform in the `E` row and in section 12. Neither product name is
written into any public file (R10, Part B2).

---

## Part A — master §25, annotated

Clause references below are to the Curriculum Policy 2026/2027 Issue 2 unless stated.
Quotations are verbatim from that document.

### A.25.1 — Authoritative reference

Master §25.1 names the approved worked example (`BUILD_Sugar_Original_Chassis_Example.html`,
SHA-256 `a55fe3804c754032480a6bc8ee5cde0e78f798ea229053285072ea133c5fc823`, a review artifact,
not a public lesson URL) and the classroom chassis Matt selected from
`Science_Teesside/Build/SCI_B_W7_Where_Food_Comes_From.html` with useful features from
`Science_Teesside/Build/v3_40min/SCI_B_W7B_Food_Chain_Do.html`. *"Do not replace that
classroom design with the newer website hub design. Keep established pathway colours, clear
teaching-stage boxes, readable diagrams, familiar controls and the original approved silver M
wherever the brand mark is used."*

Since that ruling three lessons have been accepted against it and are the working exemplars:
Sugar (BUILD W8A, live), Friction (GROW W3, accepted candidate
`508f1967b6481671dafb149d7177b620b194074312cee0dbdd30553c166b634a`, not yet merged or live) and,
when it closes, Diffusion (LAUNCH W4L1).

### A.25.2 — What every new lesson carries forward

Each master line is quoted, then the policy clause that corroborates it.

1. **Arrival.** *"Four arrival questions in each Supported, Standard and Stretch route, in the
   original 2×2 style, with matching print questions and separately revealable answers.
   Retrieve taught knowledge and provide an accessible lead-in; do not assume a new concept has
   already been taught."*
   Corroborated by §12.2 (Cognition and learning): *"Chunking, overlearning and structured
   retrieval practice across every subject"*; §12.2 (Communication and interaction):
   *"Extended processing time as standard; no expectation of immediate response"*; §5.3 (Build):
   *"short learning episodes, first/then structures, overlearning, visual supports"*.
   Refinement (CX2 §3.2): the arrival assumes an *unknown starting point*; it never says
   "catching up".

2. **Objective, criteria, sequence.** *"A clear learning objective, success criteria and
   coherent teaching sequence: arrival, starter, I do, We do, further modelling/guided work as
   useful, independent learning and exit. Teach the real subject content and use suitable
   pacing; the sugar example's nine slides and 40 minutes are not a mandatory slide count or a
   universal timetable."*
   Corroborated by §5.4: *"Planning is built on weekly outcomes rather than rigid daily scripts:
   this is essential in AP/SEND contexts where student readiness fluctuates and rigid daily
   plans create failure"*; §12.2: *"Scaffolded writing sentence stems, paragraph frames, success
   criteria, modelled examples"* and *"worked examples"*.

3. **Knowledge organiser.** *"An on-screen knowledge organiser with a printable counterpart,
   using the lesson's vocabulary, key ideas, models and examples. Keep it easy to reach during
   tasks."*
   Corroborated by §12.2: *"Memory aids knowledge organisers, vocabulary mats, reference cards
   as the normal way of working"*; §8.2: *"Vocabulary - Tier 2 and Tier 3 vocabulary explicit
   in every scheme of work; vocabulary pre-teaching as standard"*; §12.2: *"Pre-taught Tier 2/3
   vocabulary; visual word banks and word maps"*.
   Refinement (CX2 §3.2): the organiser is reachable from every stage, and its vocabulary is
   labelled **Tier 2** or **Tier 3**.

4. **Animation and models.** *"Richer, purposeful animations that reveal the scientific idea in
   manageable steps. Provide pause/reset/replay where relevant and respect reduced motion.
   Preserve distinctions between model, supplied sample data and actual practical
   observations."*
   Corroborated by §12.2: *"Reduced cognitive load dual coding, removing extraneous detail,
   worked examples"* and *"Reading-age-matched texts and dual-coded resources"*.
   The model / supplied data / observation distinction has no single policy clause; it is a
   scientific-honesty rule of the master order and is kept as written (see Part C: core
   practical evidence is never logged from illustrative data).

5. **Video.** *"Short embedded videos where they improve explanation. Prefer classroom-ready,
   captioned material with a transcript and usable fallback ... No automatic playback or
   assumed external media availability."*
   Corroborated in principle by §8.2 (assistive technology *"where this is the normal way of
   working"*) and §12.2 visual supports; no clause requires video. Videos remain optional,
   captioned and transcribed, never autoplaying, with a local fallback.

6. **We do.** *"Substantive interactive We do activities: pupils make a choice or
   arrange/annotate evidence, check it, receive specific explanatory feedback and revise.
   Touch, keyboard, pointing or directing an adult should support the same learning ... Avoid
   decorative interaction or automatic claims of pupil understanding."*
   Corroborated by §8.3: *"Alternative response - symbols, choice boards, AAC, sign, drawing,
   scribing are all valid responses across the curriculum"*; §12.2: *"Alternative response
   methods verbal, written, drawn, signed, symbol-selected, demonstrated"*.

7. **Exit.** *"Easier exits that let children capture learning with minimal reading/writing
   burden. The approved pattern is two small checks per tier: choices/pointing for Supported,
   short completions for Standard, scaffolded reasoning for Stretch. Keep the scientific aim,
   allow equivalent spoken/signed/drawn answers and exact adult scribing, and interpret support
   honestly. Provide print and useful screen-answer capture without forcing duplicate
   completion."*
   Corroborated by §14.4: *"Communication need changes the method of response, not the
   entitlement to respond"* and its acceptable-response list (Part B3); §8.3 as above.
   Passing is allowed (master §25.3: *"Refusal is information; do not invent a response or
   punish passing"*).

8. **Continuation.** *"Refer to the next lesson by its name only, without day, period, clock
   time or date. In the sugar example: Body Science Checkpoint. Current-lesson pacing is a
   separate issue."*
   Corroborated by §5.4 (weekly outcomes, not daily scripts). This is also why dated week
   labels are off every pupil surface (Part C).

### A.25.3 — Lundy and marking: integrated teaching, optional displayed prompt

Master text, kept in force: *"Keep at most one small displayed Lundy prompt in the lesson,
naturally placed within an existing learning activity and optional to open/use. Do not add a
mandatory standalone Lundy stage, repeated status bars, an extra pupil loop form, a required
signature or a progression gate. The displayed prompt being optional does not make meaningful
feedback optional or limit the number of genuine feedback exchanges."*

*"R is used only after a pupil response and genuine adult engagement. No button, saved answer,
viewed video or completed exit automatically supplies Audience, Influence, R or an assessment
outcome ... A separate written comment or duplicated record is not required on every task."*

Corroborated by §14.3: *"the word 'marking' is deliberately replaced by 'feedback and
evidence' ... It must be meaningful, manageable and motivating. Written marking is used where
it adds value typically in Launch GCSE and Functional Skills writing"*; and by §14.4:
*"Feedback is also participation. Students have a right to respond to teaching about their
learning, in a form that works for them"*, with Space, Voice, Audience and Influence defined
as the four conditions. The Feedback Policy Issue 1 §7 states the R gate in the same terms:
*"The R code in the margin signifies that the loop has closed that the student responded AND
the staff member has engaged with the response."*

Fuller Space / Voice / Audience / Influence guidance lives in the **staff notes**, never on a
pupil surface. The FP1 finding stands: prescriptions in old desk cards that the policy does not
support are not copied as policy requirements.

### A.25.4 — Website routes once real lessons exist

Kept as written. It is a publication standard, not a curriculum clause: the accepted lesson is
the primary teaching entry on the homepage, hub, subject/pathway/term/week browsing, search,
catalogues, teaching-pack pages and audience routes; earlier routes and alternatives stay in
clearly labelled secondary sections; nothing unbuilt is marked available; no placeholder
download links; Education stays separate from Play. (This is the clause that makes the stale
offline companions question of CX2 R4 a §25.4 question: see `CX2_CHECKPOINT.md` §2, STOP S3.)

### A.25.5 — Deployment instruction and honest readiness

Kept as written. Matt's standing direction is to deploy this lesson type as future complete
lessons are built and checked; it does not authorise publishing unfinished examples, weakening
release gates, changing unrelated holds or starting an unspecified batch. Before promotion:
subject content, sequence and supported/independent claims; animations and interactions;
accessible response routes; print/organiser/exit parity; matching files and canonical links;
phone/desktop layout and keyboard use; then the existing release, source-admission and
live-verification requirements. Only accepted, actually published identities are highlighted.

---

## Part B — CX2 refinements

### B1 (§4.2) — Reading bands

Policy §6.2, reading domain, verbatim: Build *"Reading age significantly below chronological
age (typically below 8 where measurable)"*; Grow *"Reading age 8–11"*; Launch *"Reading age
11+ ... able to access GCSE / Functional Skills reading"*.

The estate's committed instrument is `g26_reading_band.py` (Flesch-Kincaid grade on
pupil-addressee text: inside the lesson deck, excluding script, style, svg and any element
carrying `data-mbm-guide` or `data-audience="staff"`). Its bands come from
`STYLE_CONTRACT.json` row `reading.pathway.band` and are not re-derived here:

| Pathway | Band (FK grade) | Contract's reading-age equivalent | Binding |
|---|---|---|---|
| BUILD | 1.0–4.0 | 6–9 | band |
| GROW | 3.0–7.0 | 8–12 | band |
| LAUNCH | ceiling 14.21 (floor withdrawn, Matt's ruling 2026-09-02) | not stated | ceiling only |

Rules:
- Measure **per route** (Supported / Standard / Stretch) per lesson, on pupil-facing text, and
  the whole lesson. The route method is the one used for Friction in `CX2_CHECKPOINT.md` §2.
- **Gate** for lessons authored under CX2 (§3 Diffusion, §8.3 Lane D): a route outside its band
  is a defect to fix before the lesson is Ready.
- **Report only** for accepted lessons (Sugar, Friction): measure, record, Matt list. No
  re-open. Current readings: Friction whole 6.98 (in band; organiser 7.51, Lesson B exit 7.87
  and three legacy worksheets above); Sugar 5.26 against BUILD 1.0–4.0.
- Subject and framework vocabulary is **kept** and bridged (the contract's `.word-bridge`
  lever), never stripped to lower a score.
- Symbol support at BUILD: no licensed symbol set ships (Widgit is not embeddable). Plain
  language plus the icon and diagram support already in the chassis is what "symbol-supported
  text" means here, and that limit is recorded, not hidden.

### B2 (§4.3) — Feedback codes and the staff card

One card per lesson, **staff-only** (`data-mbm-guide="staff"`, `teacher-only`), printable on
one A4 side, with **no pupil field** (R11). The card body is the policy's own two columns,
verbatim from the Feedback & Marking Policy Issue 1 §11 in source order. The third
(theory-mapping) column is not reproduced. `E` carries the R10 wording.

| Code | Meaning |
|---|---|
| VF | Verbal feedback given here |
| WS | Worked with support |
| I | Independent |
| NS + … | Next step one specific thing |
| E | Evidence captured on the school's digital evidence platform |
| R | Responded loop closed (Audience has happened) |
| // | Self-edit point |
| ? | Read this back to me |

Beneath the table, one line: **"Curriculum Policy 2026/27 §14.3 summary: VF WS I NS E R."**
followed by the delta, named: the Curriculum Policy lists six codes and reads NS as *"next
step"*, E as *"evidence on digital software app"* and R as *"responded to feedback"*; the
Feedback Policy adds `//` and `?`, expands NS to *"one specific thing"* and R to *"loop
closed (Audience has happened)"*. The Feedback Policy is the code source (R9).

Pathway rules, from §14.3's feedback-type table:
- **BUILD and GROW cards lead with VF** and carry **no written-comment expectation** on
  practical or exit tasks. §14.3: Verbal — *"Build/Grow, practical learning, emotional
  readiness - most effective for SEND/SEMH"*; *"Written marking is used where it adds value
  typically in Launch GCSE and Functional Skills writing"*.
- **LAUNCH cards may name written feedback for extended writing only.** §14.3: Written —
  *"Launch, FS/GCSE, extended writing - strategic, not every piece"*.
- The Voice line may cite the policy's own forms (Issue 1 §6): an edit in the margin *"in the
  same colour, on the same page"*, a re-attempt, a verbal reply, a demonstration, a captured
  comment. The R gate is Issue 1 §7 (quoted in A.25.3).
- **Never** cite "Yellow Box", "green pen" or "pupil responds in their own colour". They were a
  reconstruction, struck under GW1 §A2; they are not in the policy.
- Provenance line on the card: *"Codes from the Feedback & Marking Policy 2025/2026 (Pilot),
  Issue 1, May 2026, verified in session 2026-09-15 (SHA-256
  41046284a00c9218679b946134cbc6e53c1897aad28b15fc4bd4aa963720ff3b)."* The second copy
  (`aa41d679…`) was verified the same day and carries the same codes; a card may cite either
  full hash but never a product name and never a truncated hash as an identity.
- The Curriculum Policy's own name for the platform is *"digital software app"*; the Feedback
  Policy names the product. Public files use the R10 phrase only. The product name for staff
  notes is on the Matt list.

Applies to the Lane D cards (§8.3) and to the staff notes of §3.

### B3 (§4.4) — Alternative response list

Every exit and arrival, on screen and in print, names these response modes as **labels**, not
as new inputs:

verbal · written · drawn · signed · symbol / choice-selected · demonstrated / re-attempt ·
adult-scribed

Sources: §14.4 acceptable-response list (*Verbal, Written, Demonstrated, Signed, Selected from
symbols, Captured via Digital software app, Re-attempt, Engagement or practical application*);
§12.2 (*"verbal, written, drawn, signed, symbol-selected, demonstrated"*); §8.3 (*"symbols,
choice boards, AAC, sign, drawing, scribing"*). Where a pilot's exit or print lacks a mode,
add it as a label; never add a field.

### B4 (§4.5) — Career and real-world link

One link, in the **staff notes only**, no pupil field, no new slide. Policy §10, Gatsby
Benchmark 4 *"Linking curriculum to careers"*:

| Pathway | Policy wording | What the staff note carries |
|---|---|---|
| Build | *"Practical links in every theme."* | a practical, everyday link |
| Grow | *"Subject–career links in schemes of work."* | a subject-to-career link |
| Launch | *"GCSE/FS explicitly linked to destinations."* | a destination or qualification link |

§10: *"Careers is a golden thread, not a careers week."*

### B5 (§4.6) — Thematic cycle: what exists, measured 15 September 2026

Policy §5.1: *"Thematic curriculum - Transitions, Growth and Change running through every
subject on a three-year rolling cycle (Year A: Self and Belonging; Year B: Community and
Contribution; Year C: Future and Adulthood)."* §5.2: Autumn *Transitions*, Spring *Growth*,
Summer *Change*.

Search of the estate (text files, catalogue records, lesson metadata, and the shared-strings
of every `.xlsx` workbook):
- "Self and Belonging", "Community and Contribution", "Future and Adulthood": **0 files**.
- The schemes of work carry a different, term-based theme set: **Identity & Belonging**
  (Autumn), **Resilience & Change** (Spring), **Our World, My Future** (Summer) —
  `_next6/sow/BUILD.json` 20/20/20 rows, `GROW.json` 20/20/20, `LAUNCH.json` 32/32/32 with
  15 blank; `_passsg/SOW_MATRIX.md` records the GROW term-sheet titles carrying those three
  names; `_sca1/inputs/LAUNCH_KS4.xlsx` states *"One unifying theme per term, anchored to the
  SMSC calendar"*.
- "Year A" appears only as a planner title: `Build/_Archive_VersionA_LivingIndependently/
  BUILD_Slot_Planner_2026-27_vA.xlsx` (*"Weekly Slot Planner 2026/27 (Year A)"*).
- `resources.json`: no theme field on any of its 951 rows. No catalogue record carries a theme
  tag.

No theme tag is invented and no year letter is assigned. The 2026/27 year letter, and whether
the SoW's term themes are the policy's seasonal themes under other names, go to the Matt list.

### B6 (§4.7) — GROW Science ↔ Entry Level Certificate: gap row

Policy Appendix B, Science: *"Practical science as the route into the discipline; sensory
science; health and body links; biology of stress; Entry Level bridge in science; GCSE
Combined / Entry Level / Applied Science at Launch where appropriate."* §5.3 (Grow):
*"AQA Entry Level Certificates as a bridge to Launch"*.

| Item | State | Evidence |
|---|---|---|
| A named Entry Level science qualification at scheme level | PRESENT, but **Pearson Edexcel ELC Science 8939**, not AQA | `_next6/sow/slice_Science_Teesside__Grow__W8-W13_2026-27.md` (GROW Weekly – Autumn, Science rows: *"Pearson Edexcel Entry Level Certificate in Science 8939 (E1→E3); AQA UAS science units"*); `quality/QUALIFICATION_CLAIMS_REGISTRY.json` claim Q-004 |
| Lesson-level mapping to ELC components or outcomes | **ABSENT** | no component or outcome code anywhere in the estate; `_glv3/grow/GROW_COMPLETION_AUDIT.md`: *"Science v3 does not self-award Entry Level outcomes"*; `Science_Teesside/Grow/Autumn2_W7_2026-27/manifest.json` outcome lines name *"Entry Level Science / UAS"* only |

Not started under CX2. The AQA (policy) versus Pearson (scheme) discrepancy goes to the Matt
list; nothing here decides it.

### B7 (§4.8) — Public-surface hygiene

- **No product names for school platforms** on any public surface (R10). The phrase is *"the
  school's digital evidence platform"*.
- **No pupil data fields anywhere** (R11): no Boxall, PASS, BKSB, NGRT, CAT4 or reading-age
  data; templates ship blank.
- **No phone assumptions on pupil surfaces.** Mobile-phone-free day is a school rule; Matt's
  phone is a witness device only.
- The sweep of the three pilots and the return-week packs, and its results, are recorded in
  `CX2_CHECKPOINT.md`, not here.

---

## Part C — Preservation list (inherited unchanged)

- Timings are the lesson's own and are not a template: Friction W3A 40-minute plan; W3B
  32 + 4 + 4; ten stages [1, 4, 2, 9, 10, 4, 10, 32, 4, 4]. Sugar's nine slides and 40 minutes
  are an example, not a rule (A.25.2 item 2).
- One optional help/feedback disclosure per lesson; no compulsory Lundy stage, form, signature,
  gate or duplicate record (A.25.3).
- No day, period, clock or date words on a pupil surface; dated week labels are off every
  pupil surface; the date appears once, on the staff print card (§8.3).
- The next lesson is named, never scheduled: *Friction: test the surfaces*; *Levers, pulleys
  and gears*; *Body Science Checkpoint*.
- Classroom chassis, pathway colours, familiar controls, the original silver M (A.25.1).
- Model, supplied sample data and actual observation stay distinct; core-practical evidence is
  never logged from illustrative data (§8.3).
- Videos optional, captioned, transcribed, no autoplay, local fallback.
- External hosts are staff-gated and unloaded until a staff control opens them.
- Staff prompts are distinct per stage (nine distinct `data-prompt` values, never one string
  repeated).
- Furniture (way home, mark, skip link, prev/next, guide layer) is carried from the LIVE file
  at HEAD, never from a pack.
- Accessibility: Calm Mode / reduced motion respected; colour never the only cue; enlarged text
  and 320 px reflow without loss; keyboard reaches every stage; no-JavaScript shows every
  slide; every print route one page.

## Part D — Acceptance checklist for a lesson citing this standard

From CX2 §2.4 and §3.4. A lesson is Ready only when all of these are recorded with evidence:

1. Every stage × 320 / 390 / 768 / 1280 × default and reduced motion × light / dark / forced
   colours × enlarged text; keyboard transitions; no-JS shows every slide; print; media
   (headless H.264 stated UNTESTED, never passed); zero serious or critical axe findings.
2. Reading band per route (B1) — a gate for new work.
3. Feedback card (B2), response labels (B3), staff career link (B4), hygiene (B7).
4. Parity: native editable PPTX and slide PDF, pupil/teacher DOCX and PDF, resource pages,
   START_HERE, combined pupil pack with no staff content, one-page individual prints, offline
   companions only through a committed generator (R4).
5. Records: manifest, archives, checksums, hub, source pin, size table, week binding, lesson
   order, catalogue pins, PIN1 triggers, GLV3 boundary transaction.
6. Served proof after publication: every changed file byte-for-byte with its hash and HTTP 200,
   live axe / keyboard / no-JS / print / widths on the live URL, GLV3 boundary check on served
   bytes. From this container the live origin is unreachable (egress denied), so served proof
   runs through the repository's own workflow `glv3-production-byte-check.yml` and its log.
7. Nothing is called live until the served proof exists; nothing is called accepted until
   Matt's human pass is recorded in R1's shape (reported result, device, OS/browser/AT stated
   or "not stated by Matt", full candidate hash).
