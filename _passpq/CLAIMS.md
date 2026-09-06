# CLAIMS.md — the ASDAN/PEQ accreditation-claim census (Pass PQ)

**Base SHA** `32ca685e1df619b333f3ee4385aed227aa675cdf` (origin/main).
**Authority** §2 baseline (PROVISIONAL — spec download blocked; see `inputs/README.md`),
corroborated internally by the Evidence Binder's Ofqual-URN-bearing unit table.
**Method** every string extracted verbatim by grep from the files; counts state their unit.

Classification key (from brief §3): **VALID** · **WRONG-PRODUCT** (PEQ language on
short-course content or vice versa) · **WRONG-LEVEL** · **NONEXISTENT** (names a unit/code
the spec doesn't contain) · **VAGUE** ("ASDAN evidence", no unit) · **PLACEHOLDER** (module
codes deliberately left blank pending Cheryl — expected, not a defect).

---

## 0 · Population (derived mechanically, not guessed)

| group | files | of which lessons |
|---|---|---|
| `BUILD_ASDAN/` | 39 | **31** (Careers 7, Community 6, Duke&Enterprise 6, FoodWise 6, Living Independently 6) + 5 START_HERE + Hub + Resources_and_Tools + Scheme_of_Work |
| `GROW_ASDAN/` | 23 | **18** (Community 6, Enterprise 6, PEQ 6) + 3 START_HERE + Hub + Scheme_and_Resources |
| `ASDAN/ASDAN PEQs/Evidence_Binder_PEQ_v7.html` | 1 | — (the PEQ evidence-management backbone) |
| `build_asdan.html` (root launcher) | 1 | — |
| **core accreditation-claim population** | **64** | **49 lessons** |

Secondary / adjacent (carry "ASDAN" but are not accreditation surfaces — noted, not
row-by-row censused): `ASDAN/Consent_Aimee_*` ×10 (consent teaching resources; "Aimee is
fictional, not a pupil" provenance protected under R-D03/R-H01), `ASDAN/HW_Social_Media_Wellbeing_Active.html`
(wellbeing homework, PEQ-adjacent), `build-engine/` (a lesson-generation toolchain whose
JSON seeds reference the same short-course challenge labels), `resources.json` (catalogue).

**T-audit reconciliation (source = EXTERNAL-TRANSCRIPT, per close-out ruling item 2).** The
T-audit's 159-lesson table was **deliberately emitted as transcript text, never committed** —
it is not a lost artefact. The population is instead reconciled against **REGISTER R-A02 @
`7226b08`** (as Pass SB did): R-A02's LL-3 population records **BUILD_ASDAN 31** (lacks the
writing line) and **GROW_ASDAN 18** (carries it) = **49 ASDAN lessons**, matching this
pass's mechanical derivation exactly and the sentinel-45 loop-mark set (all 31 BUILD_ASDAN
lessons are sentinel-protected). **No delta.** The full 159-table pathway cross-check remains
available from the EXTERNAL-TRANSCRIPT source if a wider reconciliation is ever wanted.

---

## 1 · Term frequency (unit-labelled, whole population)

Counts are **string occurrences**, not files, across `BUILD_ASDAN` + `GROW_ASDAN`:

| term | BUILD_ASDAN | GROW_ASDAN |
|---|---|---|
| `ASDAN` | 721 | 409 |
| `PEQ` | 0 | 238 |
| `Personal Effectiveness` | 0 | 22 |
| `E3` / `Entry 3` | 0 | 19 / 1 |
| `Level 1` / `L1` | 0 | 27 / 115 |
| `Level 2` / `L2` | 0 | 6 / 48 |
| PEQ unit codes (ComSk/DecMk/LSk/TmWk/ThSk/WellbLe/CrThSk) | 0 | 0 |
| `Certificate` / `credit` | 0 | 0 |

**Headline of the census, visible in one table:** BUILD_ASDAN names **no level, no
product, no PEQ, no unit** — it says "ASDAN" 721 times and nothing that ties any of it to
the PEQ qualification. All PEQ/level vocabulary lives in GROW. **No lesson anywhere carries
a PEQ unit code** (the deliberate PLACEHOLDER) — the only place unit codes exist is the
Evidence Binder.

---

## 2 · BUILD_ASDAN claims — what each module actually banks

Verbatim `Banks:` award-strip strings (occurrence counts across screen+print surfaces):

| module | verbatim banking claim | classification |
|---|---|---|
| FoodWise | `Banks: ASDAN FoodWise M1 challenge 1…4`, `ASDAN FoodWise M1 (practical)`, `ASDAN FoodWise M1 — module complete` | **WRONG-PRODUCT** (for PEQ) / VALID (as short course) |
| Living Independently | `Banks: ASDAN LI M1 challenge 1…4`, `ASDAN LI M1 (budget challenge)`, `ASDAN LI M1 (practical) — module complete`, `ASDAN LI M8 / AQA UAS` | **WRONG-PRODUCT** / VALID (short course + AQA UAS) |
| Careers | `Banks: AQA UAS 'Personal challenge'`, `… · SMSC Kindness`, `… · links Humanities/D&T`, `… — term complete` | **WRONG-PRODUCT** (this is AQA Unit Award Scheme, not ASDAN, not PEQ) |
| Community Project | `Banks: ASDAN/UAS community evidence`, `… · links D&T Slot 2`, `… — project complete` | **VAGUE** / WRONG-PRODUCT |
| Duke & Enterprise | `Banks: AQA UAS 'Personal challenge' · SMSC Kindness` | **WRONG-PRODUCT** (AQA UAS) |

**Reading (provisional, UNVERIFIED-AGAINST-SPEC).** Every BUILD banking claim names either
an **ASDAN short course** (FoodWise, Living Independently — §2: "a separate product from
PEQ") or the **AQA Unit Award Scheme** (a different awarding body entirely). None names a
PEQ unit, an E3 level, or "Personal Effectiveness." Against §2's estate-scope claim that
*"the 2026/27 SoWs scope PEQ to E3 at BUILD"*, **BUILD as built does not deliver or claim
PEQ at all.** This is the single largest finding in the pass and is elaborated in
COVERAGE_BUILD.md and FINDINGS §A. Whether the correct fix is (a) accept BUILD = short
courses + UAS and register accordingly, or (b) overlay PEQ E3 unit banking onto the same
work, is a **Cheryl registration decision**, not a repo patch.

`"ASDAN module codes"` on the BUILD Hub and `"Each lesson names the ASDAN
module/challenge"` on the BUILD Scheme are the closest BUILD comes to a PEQ hook — and they
point at short-course module codes, not PEQ units. → **PLACEHOLDER-adjacent / VAGUE.**

### 2a · The `AQA UAS` question (both tiers)

`AQA UAS` = the **AQA Unit Award Scheme**, a real, separate accreditation. The provision
dual-banks it alongside ASDAN. This is legitimate (§2 permits cross-unit/cross-scheme
challenge design), but note: **"registration via UAS coordinator" is the AQA UAS admin
route; PEQ registration is with ASDAN and is a different act.** Conflating them is a
Cheryl question (QUESTIONS_FOR_CHERYL §Q4), not a defect in itself.

---

## 3 · GROW_ASDAN claims — PEQ named correctly, units named loosely

### 3a · Product & level framing (GROW Scheme + Hub + lesson titles) — VALID

Verbatim:
- `GROW ASDAN · PEQ Level 1 (E3 floor · L2 stretch)` (every PEQ lesson title) — **VALID.**
- `Personal Effectiveness (PEQ Level 1)` / `ASDAN PEQ Level 1 Award (Entry 3 floor).
  Stretch tier written to L2 evidence standard.` (GROW Scheme) — **VALID** and correctly
  names the **Award** size. The "L2 stretch" is the deliberate design brief §4 protects.
- `PEQ Level 1 per the 2026/27 Qualification Map (E3–L1 only)` (GROW Scheme) — **VALID.**
- `registration via UAS coordinator` / `PEQ cohort registration via the UAS/ASDAN
  coordinator` — **STALE from 2026-08-21**: no longer a forward-looking process note —
  learners are registered and their units are entered. VALID as a record of the route that
  was used (see §2a caveat).

### 3b · Unit-name banking claims — the drift

Verbatim `Banks:` strings and their classification against §2's six core skills
(Communication, Decision making, Learning, Team working, Thinking, Wellbeing):

| verbatim claim | intended PEQ unit (inferred) | classification |
|---|---|---|
| `ASDAN PEQ L1 baseline — core-skills audit` | (cross-unit baseline) | **VAGUE** |
| `ASDAN PEQ L1 'Working with Others'` | Team working skills (TmWkSk1) | **VAGUE** — friendly label, not the unit title |
| `ASDAN PEQ L1 'Problem Solving'` | Thinking skills (ThSk1) | **VAGUE** — friendly label, not the unit title |
| `ASDAN PEQ L1 — managing own performance` | Learning skills (LSk1) | **VAGUE** — reads as a Wider-Key-Skills name |
| `ASDAN PEQ L1 — planning & reviewing own learning` | Learning skills (LSk1) | **VAGUE** |
| `ASDAN PEQ L1 — reviewing & presenting progress` | Communication skills (ComSk1) | **VAGUE** |
| `ASDAN PEQ L1 'Delivering a Project'` (×7 phase variants) | — | **NONEXISTENT as a PEQ unit** |
| `AQA UAS enterprise · ASDAN PEQ 'Working with Others' / core-skills / presentation` | cross-bank | VAGUE + see §2a |

**The one hard error: "Delivering a Project."** It appears on the GROW Community and
Enterprise strands as a banked PEQ L1 unit. **PEQ contains no "Delivering a Project"
unit** — the Evidence Binder's own (Ofqual-URN-bearing) table has only the six core skills
at each level. "Delivering a Project" is a **CoPE/AoPE module name** (§2: "PEQ replaces
CoPE/AoPE"). Naming it as a PEQ unit conflates the *activity* (a community project, which
legitimately generates cross-unit skill evidence) with a *unit* that does not exist.
→ **NONEXISTENT**, Tier-2 correction candidate (COVERAGE_GROW.md, FINDINGS §B).

**The six friendly labels are defensible but imprecise.** W1–W6 map cleanly to the six
skills (Knowing Myself→Learning; Goals That Work→Decision making; Working With
Others→Team working; Managing Myself→Learning/Wellbeing; Solving Problems→Thinking;
Present My Progress→Communication). Using pupil-friendly names on pupil surfaces is sound
SEMH practice; the issue is that the **assessor/moderator-facing** `Banks:` strings and
witness headers also use the friendly label instead of the formal unit title+code the
Binder already holds. Preferred fix (estate "reference by code" rule, §5): reconcile the
staff-side strings to the Binder's unit codes (e.g. "evidences TmWkSk1"). Tier 2.

---

## 4 · Evidence Binder claims — VALID, and the internal source of truth

`ASDAN/ASDAN PEQs/Evidence_Binder_PEQ_v7.html` embeds the full PEQ unit table **with
Ofqual URNs**, all matching §2:

```
E3: ComSkE3 R/651/6411 3cr/30 · DecMkSkE3 K/651/6419 2/20 · LSkE3 A/651/6423 2/20 ·
    TmWkSkE3 K/651/6428 2/20 · ThSkE3 D/651/6415 2/20 · WellbLeE3 A/651/6432 3/30  (=14 = E3 Certificate)
L1: ComSk1 T/651/6412 3/27 · DecMkSk1 R/651/6420 2/18 · LSk1 D/651/6424 2/18 ·
    TmWkSk1 L/651/6429 2/18 · ThSk1 F/651/6416 3/27 · WellbLe1 D/651/6433 3/27
L2: CrThSk2 H/651/6417 3/24 (Critical thinking skills)
```

Criterion structure is spec-shaped (e.g. ComSkE3: E3.1 know → E3.4 create a plan → E3.5
use the plan ["Presentation min 2 min / discussion min 5 min / text min 100 words. Group
min 3"] → E3.6 identify own success) and carries the §2 piggyback note ("Usually via a
challenge for another PEQ unit"). Qualification sizes offered: Award ≈40h / Extended Award
≈90h / Certificate ≈140h in Personal Effectiveness at E3, L1, L2. **All VALID.**

→ **The Binder is correct PEQ; the lessons drift from it.** The Binder is the reconciliation
target for every Tier-2 unit-label fix.

---

## 5 · Classification tally (unit = distinct claim-string type, not file)

| class | count (distinct claim types) | where |
|---|---|---|
| VALID | GROW product/level framing (~6) + entire Evidence Binder unit/criterion set | GROW Scheme/Hub/titles; Binder |
| VAGUE | BUILD "ASDAN/UAS community evidence"; GROW friendly-label unit banks (~7) | BUILD Community; GROW PEQ/Enterprise |
| WRONG-PRODUCT | all BUILD short-course + AQA-UAS banks (~12 distinct) | BUILD FoodWise/LI/Careers/Duke |
| NONEXISTENT | `PEQ L1 'Delivering a Project'` (7 phase variants) | GROW Community + Enterprise |
| WRONG-LEVEL | **none found** — L2 appears only as declared *Stretch* design, never as a registration/banking level | (GROW Stretch tier) |
| PLACEHOLDER | PEQ unit codes absent from all 49 lessons (deliberate, pending Cheryl) | whole provision |

**Mechanical self-inconsistency — FIXED (T2-1, authorised & applied):** `ASDAN Studio ·
ASDAN Studio` doubled in the KO / witness headers of **all 49 ASDAN lessons** (BUILD 31 +
GROW 18), 98 occurrences. Truth settled in-file (the single form is canonical on the screen
tag line). Sentinel + witness protection made it Tier-2 not Tier-1; **authorised in the
close-out ruling and applied** at commit `0a392a7` (98→0, gates passed). See FINDINGS §Tier-2.
