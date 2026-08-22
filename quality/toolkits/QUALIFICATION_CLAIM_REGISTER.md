# Qualification claim register — one row per product actually delivered

**STATUS: draft · OWNER: Matt · Pass TK-1, 2026-08-04**

What may be said about each product, and what may not. **Companion, not replacement**, to
`quality/QUALIFICATION_CLAIMS_REGISTRY.json`, which holds per-claim provenance rows `Q-001…Q-010`. This file is
the **per-product** view and cites those IDs; it introduces no new claim rows.

## Authority, stated before the table

Facts here come from, in order: (1) **`_passpq/SPEC_FACTS.md`** — derived line-by-line from the **ASDAN PEQ
specification v1.2, October 2025**, obtained 2026-07-30, with **total** two-source agreement against the
Evidence Binder on every code, Ofqual URN, credit and GLH (**R-K03**); (2) the TK-1 brief §2; (3) the audit.
Where (1) and (2) differ, (1) wins — a specification in hand outranks a brief's summary of one.

**Nothing here was checked against an awarding body's website.** No egress. Rows resting on the brief or the
audit alone are marked **SUPPLIED-BY-AUDIT**, review-by **1 September 2026**.

---

## Registration status — settled, and not to be reopened

| body | status | evidence |
|---|---|---|
| **ASDAN** | **REGISTERED — DONE.** The centre is registered; the PEQ suite is approved. | Matt, 2026-07-30 ("we're already registered"); `quality/QUALIFICATION_CLAIMS_REGISTRY.json` Q-001, status `centre-confirmed` |
| **Trinity (Arts Award)** | **REGISTERED — DONE.** Adviser trained at **Explore, Bronze and Silver**. **Not Gold.** | Matt, 2026-07-30 |

**No page, register, checklist or PR text may frame either registration as outstanding.** What genuinely remains
open is different and is already logged at `_close/OPEN_ITEMS.md` #11: the **mandatory first-year EQA sampling
booking** for PEQ (operational 1 Jan 2026, so it attaches to this delivery year), the **IQA-before-EQA** rhythm,
and **names to ASDAN roughly four weeks before sampling**. Those are centre actions; no commit closes them.

---

## The products

### 1 · ASDAN Short Courses — FoodWise, Living Independently

| field | value |
|---|---|
| Regulated? | **No — a non-regulated programme.** Portfolio, recording documents, internal moderation. |
| Registration | centre registered — DONE |
| Recording | ASDAN recording documents + portfolio |
| QA | internal moderation |
| **May claim** | "an ASDAN Short Course — a non-regulated programme"; credits/challenges completed; evidence states 1–4 from `CLAIMS_REGISTER.md` |
| **May NOT claim** | that it is a qualification · any **grade** · any **level** · any hours threshold · certification before ASDAN confirms |

### 2 · ASDAN PEQ — Personal Effectiveness Qualifications

| field | value |
|---|---|
| Regulated? | **Yes — regulated qualifications.** Operational 1 January 2026. E3 / L1 / L2 / L3. |
| Registration | centre registered, suite approved, learners registered and units entered — DONE. |
| Signatures | assessor **and** learner — live estate-wide since `bc215d1` (**R-E20/R-E21**), present on all 79 ASDAN witness surfaces |
| QA | **IQA before EQA.** First-year centres **must book an EQA sampling activity in year one** — open, `_close/OPEN_ITEMS.md` #11 |
| Units delivered | **ComSk1** (Communication skills, L1) — Ofqual `T/651/6412`, **3 credits**, **27 GLH** |
| Sizes | L1 Award `610/5904/3` = 4 credits · L1 Extended Award `610/5906/7` = 9 · **L1 Certificate `610/5905/5` = 14** (min 11 at level, max 3 adjacent) |
| Credit definition | **one credit ≈ 10 hours of learning, including assessment** (spec §5.1 p9). This is the credit **definition**; it is **not** a threshold a pupil must evidence. |
| **May claim** | the exact unit code, Ofqual URN, credit and GLH as above; registration status; evidence states 1–6 |
| **May NOT claim** | a **ten-hour window on Communication** — the spec places it on the other five skills only, and the false claim was removed at **R-K04** · certification before ASDAN confirms · that a Short Course is a PEQ unit |
| Open | GROW descriptive-week → unit-code mapping is **STILL-UNDETERMINED** and **must not be guessed** (`_close/OPEN_ITEMS.md` #8) |

### 3 · ASDAN CoPE / AoPE

**Closed to new registrations — last new registrations 31 December 2025.** Context only. No page may offer it
as a route. **SUPPLIED-BY-AUDIT.**

### 4 · ASDAN Vocational Tasters

Being withdrawn: purchases and registrations to 31 December 2026, final certification 31 August 2027.
**The estate does not deliver them.** Context only — nothing to fix. **SUPPLIED-BY-AUDIT.**

### 5 · AQA Unit Award Scheme (UAS)

| field | value |
|---|---|
| Regulated? | **No. UAS is a recording-of-achievement scheme, not a qualification.** |
| What a statement shows | the outcomes achieved. **No level. No grade.** |
| **May claim** | "AQA UAS records achievement against named unit outcomes"; the unit **theme**; evidence status |
| **May NOT claim** | "predicted UAS grade" · a UAS **level** · that UAS is a qualification |
| Approved wording | *"Evidence status reviewed; remaining unit outcomes identified."* |
| Status at HEAD | **Q-002, `verified`. R-SEMH06: the claim that estate surfaces misdescribe UAS is FALSE and RETIRED.** Re-measured by TK-1 at `74e6fee` and confirmed. **Not re-raised.** |
| Open | **25 files carry `AQA UAS unit code: TBC (Cheryl)`** — `_close/OPEN_ITEMS.md` #8, Q-003 `awaiting-centre-confirmation`, commissioned as SEMH-2. Not TK-1's. |

### 6 · Trinity Arts Award — Explore, Bronze, Silver

| field | value |
|---|---|
| Regulated? | Yes — Explore ≈ Entry 3, Bronze ≈ Level 1, Silver ≈ Level 2 (**Q-006, SUPPLIED-BY-AUDIT**) |
| Registration | centre registered with Trinity — DONE |
| Adviser | trained at **Explore, Bronze and Silver**. **NOT Gold.** |
| Part map (verified against Trinity guidance per brief §2) | **Explore Part B** requires an artist/craftsperson **AND** an arts/cultural organisation · **Bronze Part C** is research into a real person working in the arts · **Silver Unit 1 Part D** covers careers, practitioners and organisations |
| Evidence | grouped and labelled **by Part**, with an Evidence Locator Form |
| **May claim** | the part map above; evidence states 1–6 |
| **May NOT claim** | **any hours threshold at any level — none exists** · a **public showing below Gold** (it is a **Gold Unit 2** requirement only) · any **Gold** progression route, the adviser not being trained for it |
| Toolkit editions | Dec 2023 sixth-edition Discover/Explore; seventh-edition Bronze/Silver and Gold — **SUPPLIED-BY-AUDIT**, adviser to confirm against the edition actually held, review-by 1 Sep 2026 |

### 7 · Pearson (context — Q-004, Q-005)

Entry Level Certificate Science 8939 at Entry 1–3; GCSE Biology 1BI0 Foundation grades 1–5. Both
**SUPPLIED-BY-AUDIT**. They appear *beside* UAS lines on some surfaces; the grade range belongs to Pearson, not
to UAS, and that distinction is what R-SEMH06 turned on.

### 8 · JCQ access arrangements — not a product, and never a promise

A toolkit may record classroom practice. It may **not** promise an arrangement, and may not say it builds the
case "for free". Arrangements rest on evidence of need and the candidate's **normal way of working**, assessed
through the centre's own evidence and application process, and they are the **SENCo and exams officer's** to
determine.

**Approved wording, to appear wherever a toolkit touches this:**

> This is a classroom-practice record. It may contribute to centre evidence but does not establish or guarantee
> a JCQ access arrangement.

A March 2026 mid-year update to the 2025/26 JCQ AARA document exists. **SUPPLIED-BY-AUDIT** — exams officer to
confirm the live edition. Review-by 1 Sep 2026.

---

## The three sentences that must survive every future edit

1. **Registration is done — for ASDAN and for Trinity.** Anything framing it as outstanding is wrong.
2. **There is no hours threshold, at any level, for any award in this estate.** If one appears, it is fabricated,
   and this is the fourth time.
3. **A pupil's evidence state is not a grade, and an ASDAN Short Course has no grade to predict.**
