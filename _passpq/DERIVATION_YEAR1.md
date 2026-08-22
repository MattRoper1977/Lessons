# DERIVATION_YEAR1.md — §1: the timetable, measured

**Pass:** PEQ-YEAR-1 · **base** `2a8f9f5` · **branch** `claude/new-session-yed8ua`
**Instrument:** `MASTER_PROMPT_Pass_PEQYEAR1_20260821.md` (sentinels `peq-year-1-2026-08-21-TOP/BOTTOM`)
**Reproduce:** `python3 _passpq/tools/year1_derive.py` → `_passpq/inputs/year1_timetable_evidence.json`
(exit 1 = not establishable, and that is the current state)

---

## The verdict, first

**§1 stopped, and was then resolved by an owner ruling.** Both halves matter, and the record
keeps them apart.

**The stop.** The repo does not contain a weekly constant. Measurement bounded the lane at
**1–7 periods (0.67–4.67 h/wk)** and could go no further: which of BUILD's six carryable slots
may bank a guided hour to PEQ *as well as* to their own ASDAN short course is not a repo fact.
Per §1.4 the pass refused to pick a number — *"do not invent a timetable. A guessed slot is
worse than a paused pass."*

**The ruling (owner, 2026-08-22): all six carryable slots carry PEQ.** That selects the top of
the measured band — 6 slots + the PEQ row = **7 periods × 40 min = 280 min = 4.667 GLH/week** —
and the year map is re-anchored on it (§2 below, and `DECISIONS_YEAR1.md`).

**Keep the provenance straight.** 40 minutes and six-slots-at-one-period were **measured**. Seven
periods is **measured band + owner ruling**. The ruling selects *within* what measurement
established; it does not extend it, and it is recorded as an owner input, never as a repo
finding. Three things below were established by measurement and are worth having on their own.

---

## What IS established

### 1 · The period unit — **40 minutes**. Established.

Fifteen statements across the three lanes' weekly planners, **all agreeing**, no contradiction
anywhere in the estate:

| lane | file | cell | quote |
|---|---|---|---|
| BUILD | `Planning/BUILD/…Week03_14Sep.xlsx` (also W04–W07) | `[Weekly Plan]!D12` | "Runs across **BOTH weekly 40-min periods**: Period 1 → up to We Do 2; Period 2 = extended Independent Work…" |
| GROW | `Planning/GROW/…Week03_14Sep.xlsx` (also W04–W07) | `[Weekly Plan]!D12` | "Runs across **BOTH weekly 40-min periods**…" |
| LAUNCH | `Planning/LAUNCH/…Week03_14Sep.xlsx` (also W04–W08) | `[Weekly Plan]!D12` | "THREE lessons this week (Discover → Use → Master), **one per 40-min period**." |

Corroborated by the science chassis directory name `Science_Teesside/*/v3_40min/`.

**Read this carefully before reusing it.** Every one of the fifteen sits on a **Science** row.
It fixes the estate's *period unit*. It says nothing whatever about how many periods any PEQ
strand receives — and no cell anywhere states that.

### 2 · The BUILD slot architecture — **six weekly slots, one period each**. Established.

`Build/_Archive_VersionA_LivingIndependently/BUILD_Slot_Planner_2026-27_vA.xlsx`
`[Slot Architecture]!A2`:

> "**Six discrete weekly slots.** LI carries the non-food modules; FoodWise carries the food
> modules — shared module titles are never double-claimed. The Careers slot double-serves LI
> Modules 8–9, **which is how LI reaches certification on a one-slot week.**"

"one-slot week" is the sentence that fixes the count: each slot gets **one** period per week.
This is the **only** cell in the estate that fixes a slot count, and it is a BUILD file.

### 3 · The BUILD row structure — stable and complete. Established.

All 8 BUILD weekly planners carry an identical row layout, every PEQ-relevant row populated
**8/8 weeks**:

| row | label | kind | populated |
|---|---|---|---|
| 18 | ASDAN PEQ (WellbLeE3) | **core** — banks PEQ criteria directly | 8/8 |
| 19 | Slot 1 · Careers (ASDAN) | carryable | 8/8 |
| 20 | Slot 2 · Vocational / D&T (ASDAN) | carryable | 8/8 |
| 21 | Slot 3 · PfA — ASDAN Living Independently | carryable | 8/8 |
| 22 | Slot 4 · PfA — ASDAN FoodWise | carryable | 8/8 |
| 23 | Slot 5 · Community A — Community Project & Vocational | carryable | 8/8 |
| 24 | Slot 6 · Community B — Junior/Young Duke + Social Enterprise | carryable | 8/8 |
| 17 | PE | — | **0/8 — a dead row, not a slot** |

So BUILD's PEQ time is bounded, and the bounds are wide:

- **floor — 0.67 h/wk** (row 18 alone: 1 × 40 min) → 25.3 GLH over 38 weeks
- **ceiling — 4.67 h/wk** (all seven rows: 7 × 40 min) → 177.3 GLH over 38 weeks

The shipped plan's 3.5 h/wk sits inside that band, at about 5¼ slots per week.

---

## What is NOT established — and why the pass stops

### A · GROW has no PEQ slot to measure

`Planning/GROW/…Week01–08.xlsx` `[Weekly Plan]!` row 18 is labelled
**"Careers / Vocational (ASDAN)"** and is **empty in 8 of 8 weeks** — every cell B–I reads
`None`. The row exists as a heading and was never filled.

GROW's PEQ hours per week are therefore **not measurable at any value, including zero** — an
empty row is a planner that was not completed, not a timetable that allocates nothing.

### B · LAUNCH's planners disagree with each other

The 8 LAUNCH weekly files do not share a row structure. Measured label-by-label:

| week file | row 17 | row 18 | row 19 |
|---|---|---|---|
| W01 | `PfA/ASDAN PEQ` **(populated)** | PE (empty) | Independent Living Skills |
| W02 | `PfA/ASDAN PEQ` **(populated)** | PE (empty) | Living Independently |
| W03 | `PfA/ASDAN` **(populated)** | PE (empty) | Independent Living Skills |
| W04 | `PfA/ASDAN PEQ` **(empty)** | PE (empty) | Careers / Vocational (ASDAN) |
| W05–W08 | PE (empty) | Careers / Vocational (ASDAN) | — |

A PEQ row is populated in **3 of 8 weeks** and is **absent from the file entirely in 4**. That
is not a weekly slot; it is a row that was dropped part-way through the term's build. Note the
LAUNCH `Slot Plan Aut1` tab *does* carry a clean five-strand PEQ column for all 8 weeks — but
it is an outcomes plan, with no period count and no slot length, and it contradicts the weekly
files it is supposed to summarise.

### C · The carryable share is a ruling, not a fact — on every lane

Even on BUILD, where the arithmetic is clean, the number that matters is not "how many slots"
but **"how many of those slots may bank an hour to PEQ as well as to their own ASDAN short
course."** The repo argues both ways and settles neither:

- **Against.** The Slot Planner's own rule: *"shared module titles are **never
  double-claimed**"*; and the BUILD year plan's *"No double-claiming: Duke cookery challenge
  explicitly excluded from FoodWise."* The six slots exist to bank **LI, FoodWise, UAS and Duke**
  credit.
- **For.** The PEQ spec's own delivery model, already recorded in `SPEC_FACTS.md` §19 and
  quoted in `l2k_plan.py`: Communication evidence is *expected* to be generated through a
  challenge that leads to another unit (spec pp25/39/54), and ASDAN's worked assessment plan
  co-assesses two units in the same weekly activities.

Resolving this needs the **PEQ delivery guide** — member-gated, **not held**, and listed as
outstanding in `_passpq/inputs/README.md` — or a coordinator ruling. Per the estate's standing
rule, a finding that depends on a document the centre does not hold stays
**STILL-UNDETERMINED**, never inferred.

### D · Two-thirds of the year has no calendar

- **Autumn 2026 = 15 teaching weeks.** Evidenced in five places (`Planning/*/README.txt` and
  both year-plan workbooks' `Key Dates & Compliance` tabs): 1 Sep – 18 Dec, half term 26–30 Oct,
  Aut 1 = 8 weeks, Aut 2 = 7. Re-derived from the dates rather than trusted from the label.
  Carries its own caveat on every copy: *"Redcar & Cleveland 2026-27 **DRAFT** calendar —
  reconfirm when the final publishes."*
- **Spring and summer 2026-27: nothing.** No term dates, no half-term dates, no Easter date, no
  INSET day anywhere in the repo — swept across every `.md`/`.txt`/`.json`/`.py` and all nine
  source workbooks, cell by cell.
- The three SoW workbooks *do* carry a `Half-term & weeks` column totalling **39 weeks**
  (7+7+6+6+6+7). It cannot be used: its autumn half is **7 + 7 = 14**, which is precisely the
  shape all three `Planning/*/README.txt` files declare dead —
  *"an earlier ASDAN yearplan used PLACEHOLDER dates … 14 weeks … **Those placeholders are
  dead — do not reuse them.**"* The spring/summer counts in that same column were built on the
  same footing and have no calendar behind them.

### E · A real defect found on the way

`_passpq/tools/l2k_plan.py` carries `WEEKS = 38` with **no stated source** — `git log -S 'WEEKS = 38'`
returns one commit whose message justifies the GLH measurement and the milestone weeks but never
the year length. Worse, its `BLOCKS` spends only **14** weeks on autumn
(`("Aut1", 1, 7), ("Aut2", 8, 14)`), contradicting the 15-week autumn the repo evidences in five
places. Candidate year lengths: **38** (what the code says) · **39** (what the SoW totals) ·
**40** (evidenced autumn + SoW remainder). Logged in `PROPOSED_YEAR1.md`; not silently changed.

---

## What closed it, and what is still open

**Closed — the carryable ruling (owner, 2026-08-22).** *All six* of BUILD's carryable slots may
bank guided hours to PEQ alongside their own ASDAN short course. That converts the measured
0.67–4.67 h/wk band into a single figure: **7 periods = 4.667 h/wk = 177.3 GLH a year per lane.**

What follows from it, all of it proven in the ledger rather than asserted:

| | |
|---|---|
| **Every lane targets the full Certificate** | E3 Certificate (14 cr) · L1 Certificate (14 cr, claimed from the six-unit 15) · L2 Certificate (15 cr) |
| **Milestones hold on all three lanes** | Award **W14** → Extended Award **W26** → Certificate **W38** |
| **The co-delivery claim is withdrawn** | was E3 7 h and L1 2 h; at 4.667 h/wk the hours are real supervised time and the six-unit ledgers close without it |
| **Declared QA/consolidation** | 37.3 h (E3) · 42.3 h (L1) · 57.3 h (L2) — never claimed against a unit |

Had the timetable given **five** periods instead of seven, the honest answer for Entry 3 and
Level 1 would have been the **Extended Award**. The sensitivity table on the year map now shows
where every threshold falls, so a later timetable change can be read off it rather than
re-argued.

**Still open — and unaffected by the ruling:**

1. **The spring and summer term dates** for 2026-27, from the final Redcar & Cleveland calendar
   — which also retires the unsourced `WEEKS = 38`.
2. **GROW's empty ASDAN row** and **LAUNCH's inconsistent weekly planners** (§B and §A above).
   Planner-authoring defects, not PEQ questions; logged in `PROPOSED_YEAR1.md` P5.
