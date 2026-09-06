# PROPOSED_YEAR1.md — judgement calls this pass did NOT take

Pass PEQ-YEAR-1. Each item is something the pass found, could have decided, and deliberately
did not. Each says what it would take to close it.

**P1 was closed by an owner ruling during the pass** and is kept here with its resolution, since
it is the item every other number depends on. P2 is superseded by it. P3–P9 remain open.

---

## P1 · The carryable-slot ruling — **CLOSED 2026-08-22**

**Question.** Of BUILD's six timetabled weekly slots (Careers · Vocational/D&T · Living
Independently · FoodWise · Community A · Community B), how many may bank a guided hour to PEQ
as well as to their own ASDAN short course?

**Answer (owner, 2026-08-22): all six.** 6 carryable slots + the PEQ row = **7 periods × 40 min
= 4.667 h/wk**, the top of the band §1 measured.

Applied: `WEEKLY_MIN` 210 → 280, ledger and all pages regenerated, co-delivery withdrawn on all
three lanes, every lane targeting the full Certificate with milestones at W14/W26/W38 proven in
the ledger. See `DECISIONS_YEAR1.md` §1b–§2.

**Recorded as an owner input, not a repo finding.** The repo argues both ways and settles
neither — the Slot Planner forbids double-claiming between LI and FoodWise, while the PEQ spec
expects PEQ evidence to be generated through other activity (pp25/39/54). If the **PEQ delivery
guide** (member-gated, still not held) later contradicts this, the ruling is where to look
first, and `WEEKLY_MIN` is the single constant to change.

## P2 · Five periods or six — **SUPERSEDED by P1**

The timetabling question is answered at seven periods. Kept here only as the fallback table, so
a timetable change can be costed without re-deriving:

| Weekly periods | h/wk | Entry 3 | Level 1 | Level 2 | E3 co-delivery |
|---|---|---|---|---|---|
| 5 × 40 min | 3.33 | Extended Award | Extended Award | Certificate | n/a |
| 6 × 40 min | 4.00 | Certificate | Certificate | Certificate | not needed |
| **7 × 40 min** | **4.67** | **Certificate** | **Certificate** | **Certificate** | **withdrawn — live plan** |

Below **four** periods the Extended Award goes too; at **one**, nothing is reachable at all.

## P3 · `WEEKS = 38` is unsourced, and `BLOCKS` contradicts the evidenced autumn

`_passpq/tools/l2k_plan.py` carries `WEEKS = 38` with **no stated source**
(`git log -S 'WEEKS = 38'` returns one commit whose message justifies the GLH measurement and
the milestone weeks, never the year length). Its `BLOCKS` spends **14** weeks on autumn
(`("Aut1", 1, 7), ("Aut2", 8, 14)`) against the **15** the repo evidences in five places
(Aut1 = 8, Aut2 = 7).

| candidate | where it comes from |
|---|---|
| **38** | what the code says; no derivation anywhere |
| **39** | what the three SoW workbooks total (7+7+6+6+6+7) — but their autumn is the **dead placeholder** 14-week shape the READMEs retract |
| **40** | evidenced autumn (15) + the SoW's spring/summer remainder (25) |

**Not silently changed**, because changing the week count moves every milestone week on every
generated page, and the right value depends on P4. **Owner: Matt**, once the final calendar
publishes.

---

## P4 · Spring and summer 2026-27 have no dates in the repo

No term dates, no half-term dates, no Easter date, no INSET day — swept across every
`.md`/`.txt`/`.json`/`.py` and all nine source workbooks, cell by cell. Autumn is evidenced
(1 Sep – 18 Dec, half term 26–30 Oct, 15 weeks) and even that is captioned *"Redcar & Cleveland
2026-27 **DRAFT** calendar — reconfirm when the final publishes."*

**What closes it.** The final LA calendar. It also retires P3.

---

## P5 · Two repo defects found while measuring — not this pass's scope to fix

1. **GROW has no PEQ slot.** `Planning/GROW/…Week01–08.xlsx` row 18 is labelled
   *"Careers / Vocational (ASDAN)"* and is **empty in 8 of 8 weeks** — every cell B–I reads
   `None`. The row was created and never filled. GROW's PEQ hours are unmeasurable at any
   value, including zero.
2. **LAUNCH's eight weekly planners disagree with each other.** A PEQ row is populated in 3 of
   8 weeks and absent from the file entirely in 4; rows 17–19 carry different labels in
   different weeks (`PfA/ASDAN PEQ`, `PfA/ASDAN`, `PE`, `Careers / Vocational (ASDAN)`,
   `Independent Living Skills`, `Living Independently`). The `Slot Plan Aut1` tab *does* carry
   a clean five-strand PEQ column for all 8 weeks, and contradicts the weekly files it
   summarises.

Both are planner-authoring work, not PEQ work. Reproduce with
`python3 _passpq/tools/year1_derive.py`.

---

## P6 · `resources.json` — two items, both blocked on the same thing

`tools/pin_manifests.py` writes **both gate copies or neither** (Lessons *and* Apps), and the
Apps checkout is unreachable from this session:

```
$ python3 tools/pin_manifests.py --check
manifests:
   MISSING apps.json (no owning checkout found)      # exit 1
```

So the pass left `resources.json` untouched, and its pin stays green. Two consequences:

1. **The four new Kitchen pages are not registered in the catalogue.** They are reachable from
   the year map and the handover and print correctly, but will not appear in `resources.json`
   until a pass with both checkouts registers them and re-pins **in the same commit**.
2. **`resources.json:6109` now contradicts the page it indexes.** Its `desc` still reads
   *"…core-skills audit (registration via UAS coordinator)"* while
   `GROW_ASDAN/PEQ/PEQ_W1_Knowing_Myself.html` now reads *"registered via the UAS coordinator"*.
   `_passla/build/gen_catalogue.py` only *appends* rows ("Existing {before} byte-preserved"), so
   **no rebuild will ever repair this** — it is hand-maintained and needs a deliberate edit.

---

## P7 · The entered AQA UAS unit codes — a fact this pass does not have

Two families still carry `TBC (Cheryl)` and were **left alone rather than guessed**:

| family | files | what the replacement needs |
|---|---|---|
| D&T decks `BUILD_DT_W1–W6` | 6 files, 27 string occurrences | the entered **vocational** UAS unit code |
| Science witness sheets | 30 BUILD/GROW files | the entered **science** UAS unit code |
| LAUNCH science witness sheets | 15 files | **no code at all** — per the 2026-08-05 scoping ruling LAUNCH science is the GCSE route, so the hidden slot should be deleted outright rather than filled |

The registration *status* rows in `quality/QUALIFICATION_CLAIMS_REGISTRY.json` were updated
(Q-003 → `unit entered` / `centre-confirmed`); the `pupil_facing_wording` carrying the literal
`TBC (Cheryl)` was **not**, because writing a code nobody has read from the entry record would
be a fabricated compliance claim. **Owner: Cheryl**, from the AQA UAS entry record.

---

## P8 · The staff pack cannot be built in this environment

`tools/build_staff_pack.py --mirror` hard-stops without `--logo`, verifies the PNG by SHA-256,
and the binary is deliberately not in git. **Nobody can produce the pack without Matt's
machine**, and nothing in the kitchen year needs it. Stated so nobody waits on it.

---

## P9 · One wording call, taken narrowly, worth an owner glance

The hedge rewrite initially produced *"registered via the **UAS/ASDAN** coordinator"* in 12 new
places, merging two awarding bodies into one label — against
`_passpq/QUESTIONS_FOR_CHERYL.md`'s own answer that *"AQA UAS is a different awarding body from
ASDAN… keep the two named separately on surfaces."* Reduced to a **tense change only**
(*"registration via UAS coordinator"* → *"registered via the UAS coordinator"*). One
pre-existing *"UAS/ASDAN coordinator"* on `GROW_ASDAN_Hub.html` predates this pass and was left
alone. If the estate wants one canonical phrasing, that is an owner call.

---

# Lodged by PEQ-YEAR-2 (2026-08-22)

Two questions for Matt, both blocking a figure that is currently carried as an assumption. Each
is one line, as asked.

### Q-Y2-1 · Term dates

> **Confirm term dates / teaching weeks for spring and summer 2026-27.**

**Why it is open.** Autumn is evidenced at **15** teaching weeks and the block boundaries now
match it. Spring and summer have **no term date anywhere in the repo** — no Easter date, no
February or May half-term, no INSET day. Their block lengths are declared assumptions, tagged as
such on the year map.

**What the answer unlocks.** The year length. `WEEKS = 38` is the SoW scheme's 39 with a week
taken off summer, on top of the dead 14-week autumn. Evidenced autumn plus that scheme's
spring/summer would give **40**. Neither 39 nor 40 can be set today: `lane_rows()` hand-allocates
exactly 38 weeks and `build()` refuses any other length, so a real answer means re-allocating all
three lanes — worth doing once, against a real calendar, not twice against guesses. It changes no
milestone at the live seven-period rate; it *would* matter at 3 or 5 periods.

### Q-Y2-2 · GROW and LAUNCH slots

> **GROW/LAUNCH PEQ slots — confirm from the September timetable.**

**Why it is open.** The 4.667 h/wk rate was established on **BUILD**. GROW's ASDAN planner row is
**empty in all eight built weeks**; LAUNCH's eight planners **disagree with one another on their
own row structure**, carrying a populated PEQ row in three weeks and none at all in four. Neither
is a measurement, and neither was invented.

**What the answer unlocks.** Whether the one-rate assumption is safe outside the kitchen. The
year map runs all three *level* lanes at 4.667, which is correct for one mixed class in one
kitchen; read as a statement about the GROW and LAUNCH *rooms* it is an assumption, and the pages
now say so. Two repo defects sit underneath and are planner-authoring work, not PEQ work: GROW's
row was created and never filled, and LAUNCH's weekly files need reconciling to one row structure.

Reproduce either finding with `python3 _passpq/tools/year1_derive.py`.
