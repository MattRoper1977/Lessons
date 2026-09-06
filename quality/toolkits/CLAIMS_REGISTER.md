# Claims register — the controlled evidence-status vocabulary, and the TK-1 census

**STATUS: draft · OWNER: Matt · Pass TK-1, 2026-08-04 · census derived at `74e6fee`**

---

## Part 1 — The controlled vocabulary

### Read this first: there are TWO axes, and confusing them is the failure mode

`quality/DELIVERY_READINESS_CHECKLIST.md` already owns a seven-state vocabulary. It describes **a resource**:
is this file fit to put in front of a class? The vocabulary below describes **a pupil's evidence**: how far has
this work travelled toward an award?

They are orthogonal. A `delivery-ready` worksheet can hold `draft` evidence; a `drafted` resource can capture
`centre-verified` evidence. **Never merge them, and never let a page display one where it means the other.**

### The six evidence states

| # | state | what it means | who may assert it |
|--:|---|---|---|
| 1 | **draft** | Work exists. No claim is made about it. | Pupil or teacher |
| 2 | **curriculum-aligned** | The task maps to a named criterion, outcome or unit. Alignment is a **teacher's** judgement about the task, not a statement about the pupil's work. | Subject lead |
| 3 | **candidate evidence** | Specific pupil work is offered against a specific criterion. Nothing has confirmed it yet. | Teacher / assessor |
| 4 | **centre-verified** | The assessor has judged the criterion met, and internal quality assurance has sampled or accepted it. | Assessor + IQA |
| 5 | **submitted** | Sent to the awarding organisation — registered, entered, moderated or sampled as that product requires. | Qualification lead |
| 6 | **certified** | The awarding organisation has confirmed the achievement. A certificate or statement exists. | Awarding organisation |

**Rules.**

- A page may display **one** state per item. Ambiguity is what the vocabulary exists to remove.
- **No state may be skipped forward.** In particular, nothing reaches `certified` because a lesson finished.
- States 4–6 are **not repository actions**. No commit moves anything to `centre-verified` or beyond, and no
  commit message may imply it.
- Where a state is unknown, the honest value is **`draft`**, not the most flattering plausible one.
- The vocabulary describes **status**, never **quality**. It is not a grade, and it does not rank pupils.

### Approved replacement wording

| do not write | write instead |
|---|---|
| "inspection-ready" | "a dated record of the routine, with pupil voice captured" |
| "banked qualification" | "candidate evidence recorded against \<exact unit/criterion\>" |
| "build real qualifications" | name the split honestly — "an ASDAN Short Course (a non-regulated programme) and, for those registered, PEQ units (regulated qualifications)" |
| "predicted grade" (on an ASDAN surface) | "evidence status" using the six states above. **ASDAN Short Courses carry no grade.** |
| "evidence-led" as a status badge | say what the evidence is and what state it is in |
| "predicted UAS grade" / UAS as a qualification | "Evidence status reviewed; remaining unit outcomes identified." **AQA UAS carries no level and no grade.** |

### One phrase that is exempt, and why

**"Portfolio of record" stays.** It is not marketing. It is Matt's deliberate declaration resolving which of two
competing print routes — the weekly evidence pack, or the in-lesson print sections — is authoritative for a
given suite. Removing it would reopen a settled question and leave two routes both claiming primacy. It may
gain status metadata like anything else; it is not softened, and it is not stripped.

---

## Part 2 — The census at `74e6fee`

Derived, per **R25**: a non-zero count is published as an **inventory**, never as a number.

### Confirmed and actionable — Phase 3 targets

| id | file:line | string | why it is wrong | disposition |
|---|---|---|---|---|
| C-01 | `build_asdan.html:25` | "an inspection-ready SMSC/BV/safeguarding record" | Asserts an external judgement no one in the estate can make. Nothing is inspection-ready by authorship. | reworded |
| C-02 | `build_asdan.html:13` | "**Evidence-led**" as a feature badge | A status badge with no state behind it. | reworded |
| C-03 | `BUILD_ASDAN/BUILD_ASDAN_Hub.html:6` | "Reluctant writers build real qualifications through making, doing and photographing — not paperwork" | Blends a non-regulated Short Course with regulated PEQ. Some of what BUILD banks is not a qualification at all. | reworded to the honest split |
| C-04 | `DT_Community_Upcycling/Scheme_of_Work.html:19` | "update the ASDAN tracker and predicted grade" | ASDAN Short Courses are non-regulated and carry **no grade**. | reworded to evidence status |
| C-05 | `DT_Community_Upcycling/Scheme_of_Work.html:38` | "lock the predicted grade" | As C-04, and "lock" implies a finality no internal process confers. | reworded to evidence status |

### Classified and deliberately not changed

| pattern | occurrences / files | classification | why untouched |
|---|--:|---|---|
| `banked` in a lesson-completion modal — *"The Workshop Audit — banked!"* | dominant share of 246 / 163 | **DIFFERENT-MODEL** | XP/celebration language at the end of a deck, meaning "you finished". Not a qualification claim, and it lives inside **lesson slideshows** (out of scope, §3). |
| `banked` near a certificate — `Build/Slideshows/BUILD_L1_LI_Where_Money_Comes_From.html:236`, *"Module 1 evidence banked — your first steps toward the Living Independently certificate"* | 1 (+1 archived twin) | **REAL but PROTECTED** | Genuinely overclaims. Inside a lesson slideshow → **proposed diff only**, recorded in the readback. |
| "Banks:" as a table-column verb — `GROW_ASDAN/Scheme_and_Resources.html:22` | 1 | **ACCURATE** | Means *this lesson contributes evidence toward*, which is exactly right and already honest. |
| `evidence-led` describing a **pupil task** — `Humanities_Teesside/*Scheme_of_Work.html`, `*Printable_Pack.html` | 7 / 4 | **DIFFERENT-MODEL** | *"evidence-led nominations (not a vote alone)"*, *"a named adult acts on one evidence-led recommendation"*. Pedagogy, not status. Rewording would damage the teaching. |
| `predicted grade` in the `cc-helper` string | 16 / 14 | **DIFFERENT-MODEL — PROTECTED** | The `coldCall_y10` graded cold-call system (**R-B02**): the grade drives tier-matched questioning. Legacy-frozen files, and the register forbids migration. |
| `Banked Strengths Deck` — `BUILD_ASDAN/Careers/CAREERS_W5,W6` | 2 | **DIFFERENT-MODEL** | A resource's proper name. |

### Retired — do not re-raise

| claim | status |
|---|---|
| Estate surfaces present AQA UAS as a qualification or show a UAS level | **FALSE. RETIRED at R-SEMH06.** Re-measured at `74e6fee`: the support-layer hits are Scheme-of-Work banners naming the unit *theme* (`AQA UAS 'Creating artwork'`) and tier language (`Work at your level`). No edit warranted; none made. The separate live item is 25 files carrying `AQA UAS unit code: TBC (Cheryl)` — `_close/OPEN_ITEMS.md` #8, commissioned as SEMH-2. |

---

## Part 3 — Owner, evidence and expiry

| claim class | owner | evidence required before the state may rise | expiry |
|---|---|---|---|
| ASDAN Short Course status | ASDAN coordinator (Cheryl) | recording documents + internal moderation record | 1 Sep 2026 review |
| ASDAN PEQ unit/credit/level | ASDAN coordinator + IQA | `_passpq/SPEC_FACTS.md` (spec v1.2 Oct 2025) — already in hand, two-source agreement total (**R-K03**) | on next spec revision |
| Arts Award part mapping | trained adviser (Explore/Bronze/Silver) | Trinity toolkit edition actually held | 1 Sep 2026 review |
| AQA UAS unit codes | UAS coordinator (Cheryl) | 60 tracked `*.html` carry the `TBC` literal (25 held byte-pristine per OPEN_ITEMS item 17; 35 `v3_40min` variants outside that set). Registration and unit entry are settled; **the code itself is an unverified centre record awaiting confirmation** and no surface may present it as a compliance claim. | blocking |
| JCQ access arrangements | SENCo + exams officer | centre evidence process; never a toolkit | annually, per JCQ cycle |
| Safety / first-aid wording | H&S lead + first-aid lead | `SAFETY_CONTENT_GATE.md` | 1 Sep 2026 review |

---

## Deferred — recorded so no rival design is authored

**Independence and prompt fading is already designed and accepted.** `quality/DESIGN_prompt_record.md`
(SEMH-1 §8, approved in principle by Matt 2026-08-04) specifies one adult-side **paper** line beside the
existing print surfaces, a WT→DS ladder in which DS is **not** a failure state, never a register, score or
aggregate, waiting on the LL-I specimen and the TA briefing.

The 2026-08-04 toolkit audit's P1 "Independence" row proposes the same thing in different words. **TK-1
authored nothing here.** Two designs for one behaviour is worse than one, and the estate already chose.
Recorded as an overlap, not as a gap.
