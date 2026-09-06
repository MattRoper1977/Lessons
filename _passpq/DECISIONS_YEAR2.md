# DECISIONS_YEAR2.md — pass PEQ-YEAR-2, gate record

**Instrument:** `MASTER_PROMPT_Pass_PEQYEAR2_20260821.md` · sentinels
`peq-year-2-2026-08-21-TOP` / `-BOTTOM`
**Lessons base:** `63271c33` (a descendant of the expected `72e1fa4c`) · branch `claude/peq-year-2`
**Apps base:** `a7e80737` · branch `claude/peq-year-2`
**Rollback:** `git reset --hard 63271c33` (Lessons) · `git reset --hard a7e80737` (Apps)

## §0 · The gate that shaped the pass — **PASSED**

Both checkouts present and fetched. `MattRoper1977/Matt-s-Apps-` attached and cloned to
`/home/user/matt-s-apps-`; both copies of `tools/verify_cross_estate_unification.py` confirmed
**byte-identical** before any work, and both manifest pins present. **§1 therefore ran.** This is
the whole reason the pass exists: PEQ-YEAR-1 had one checkout and correctly refused to touch a
pinned manifest it could not re-pin.

---

## §1 · The catalogue, and line 6109

### Line 6109, before and after

```
before   "desc": "Strengths, interests, starting points — v5 studio lesson with full print
          pack. ASDAN PEQ Entry 3 baseline — core-skills audit
          (registration via UAS coordinator)."

after    "desc": "Strengths, interests, starting points — v5 studio lesson with full print
          pack. ASDAN PEQ Entry 3 baseline — core-skills audit
          (registered via the UAS coordinator)."
```

**What it asserted vs what the page says.** The catalogue described the page as still awaiting
registration, via a coordinator route yet to run. The page it indexes —
`GROW_ASDAN/PEQ/PEQ_W1_Knowing_Myself.html` — was corrected by PEQ-YEAR-1 and reads *"registered
via the UAS coordinator"* in **all 8** places. `_passla/build/gen_catalogue.py` only ever
**appends** rows ("Existing {before} byte-preserved"), so **no rebuild could ever have repaired
it**; the catalogue is hand-maintained on that axis.

**A second stale desc, same class, fixed in the same commit.** The Kitchen SoW entry still
advertised *"the 2/3/4 h-per-week sensitivity table"*, which PEQ-YEAR-1 replaced with the 1–7
period band at the derived seven-period rate.

### The four entries

| id | file | type |
|---|---|---|
| `grow-asdan-peq-l2k-cooking-handover` | `Cooking_Handover.html` | `support` |
| `grow-asdan-peq-l2k-week-shells` | `Kitchen_Week_Shell.html` | `support` |
| `grow-asdan-peq-l2k-criteria-by-week` | `Criteria_By_Week.html` | `support` |
| `grow-asdan-peq-l2k-completion-checklist` | `Kitchen_Completion_Checklist.html` | `support` |

**`support`, not `teacher`, and that is the AUDMAP point rather than a copy of the sibling hub.**
`index.html` renders `type:"teacher"` with an **"interactive"** format icon and an **"OPEN TOOL →"**
label. These four are print-first static documents; `support` gives **"OPEN PACK →"** and no
interactive icon, and matches the sibling Kitchen SoW entry. `isPack()` fires only for
`lesson`/`revision`, so none gains a spurious print-pack icon either.

**On AUDMAP itself:** it lives in the **Apps** repo's `index.html`, keys on studio **name**, and
governs `apps.json`. It does not reach `resources.json`, so the literal default cannot misfile
these — the Lessons catalogue has no audience filter at all. The precedent it stands for does
reach them, which is why the type was chosen from what `index.html` actually renders.

Fields derived from the two existing Kitchen entries, not invented: subject **"GROW Vocational &
PfA"** (an existing chip, in both `PRIORITY` and `PRINTPACK`; **44 → 48**), family, year, keyword
spine. Appended at the tail, where the existing Kitchen entries sit and what `REGISTER.md`'s
append-only-union rule wants.

**Proof:** 647 → **651** entries · valid JSON · all 651 ids unique · all four targets exist on
disk · **0 schema errors in the new rows** (the 264 total are pre-existing legacy) · diff is 81
insertions + the 2 desc corrections, no reformat of the other 647.

### The pin — `pin_manifests.py` only, both copies in one run

| manifest | before | after |
|---|---|---|
| `resources.json` | `de9e7c615153` | **`907e7875d0e4`** |
| `apps.json` | `a4a06b999b5f` | unchanged |

Both gate copies **byte-identical** after the move (`cmp`), `--check` green in both, and the Apps
repo's only diff is the gate copy. **Chip gate 28/28 limbs, zero console errors** — limb count
unmoved; only the numbers inside moved, which is what "wording/additions only" means.

---

## §2 · The week count

**Autumn is evidenced at 15, and this file had it at 14.** Re-derived from the dates rather than
read off a label: 31 Aug → 14 Dec 2026 is 105 days = 16 Mondays; minus the one half-term week
(26–30 Oct) = **15**, split Aut1 **8** and Aut2 **7**. Stated identically in five places and
enumerated week by week in `BUILD_Autumn_Year_Plan_ASDAN_Update.xlsx [Autumn Overview] A6:B21`.
The 7 + 7 = 14 in `BLOCKS` was the **placeholder shape the Planning READMEs declare dead**.

```
BLOCKS  Aut1 W1-7  Aut2 W8-14  Spr1 W15-20  Spr2 W21-26  Sum1 W27-32  Sum2 W33-38
     →  Aut1 W1-8  Aut2 W9-15  Spr1 W16-21  Spr2 W22-27  Sum1 W28-33  Sum2 W34-38
```

### Milestone deltas: **none**

| lane | Award | Extended | Certificate |
|---|---|---|---|
| Entry 3 | W14 → W14 | W26 → W26 | W38 → W38 |
| Level 1 | W14 → W14 | W26 → W26 | W38 → W38 |
| Level 2 | W14 → W14 | W26 → W26 | W38 → W38 |

Every unit's complete-week identical; **0 of the 63 reachability cells change** at 4.667 h/wk.
Verified by rebuilding and diffing the ledger against HEAD, not asserted. `BLOCKS` turns out to
enter **no assertion and no allocation** — it is a JSON field and a label lookup — so correcting
it fixes what the pages *say* without moving a minute. It mattered in a teacher-facing way: **W8
is the AUDIT week and the last week of Aut 1**, and the printed week shells were labelling it
Aut2.

### A second deviation, found while checking the first

The SoW workbooks' own scheme totals **39** weeks (7+7+6+6+6+7), and `BLOCKS` gave **Sum2 six
weeks, not seven**. So `WEEKS = 38` is that 39 with a week taken off **summer**, *on top of* the
dead 14-week autumn — two deviations, not one, and only the autumn half is correctable here.

### Why the year stays 38

Neither 39 nor 40 can simply be set: `lane_rows()` hand-allocates exactly 38 weeks and `build()`
asserts every week sums to `DESIGN_MIN`, so `WEEKS = 39` dies on `AssertionError: E3 W39: design
0 != 210` — **verified for both 39 and 40**. Re-cutting the year would move every milestone and
every criteria-to-week mapping on the strength of **24 weeks the repo cannot evidence**. §2's own
guard — *"Ledgers must still sum or the pass STOPs"* — settles it. Autumn's correct +1 is
absorbed by Sum2, the last and least-evidenced block, and the page says so.

### Spring and summer: declared assumptions, on the page

No term date, no Easter date, no February or May half-term, no INSET day anywhere in the repo.
`TERM_EVIDENCE` now carries each block's length **and whether it is evidenced**; the year map
tags every block **evidenced** or **assumption** and states the total year length. The question
is lodged on the page: *confirm term dates / teaching weeks for spring and summer 2026-27*.

**`_assert_calendar()`** makes the scheme self-guarding — `BLOCKS` must span `WEEKS`, start at W1,
end at `WEEKS`, have no gap or overlap, agree with `TERM_EVIDENCE` row for row, and total exactly
15 evidenced autumn weeks. Proven on three planted faults, each red: a scheme not covering the
year, a `TERM_EVIDENCE` row disagreeing with its block, and a **silent regression to the 14-week
autumn**.

---

## §3 · The UAS codes — kept TBC, made safe

**Not resolved, as instructed.** What changed is how the estate *describes* them.

**A YEAR-1 regression corrected.** Q-003's subject is the AQA UAS **unit code**. PEQ-YEAR-1 set
its status from the **registration** fact, so a claim about a code nobody has read came to read
`status: "centre-confirmed"`, `confidence: "high"`. Registration and unit entry *are* settled; the
code is not, and collapsing the two is the exact overreach §3 exists to close. Now
`unverified-centre-record-awaiting-confirmation`.

**The count was wrong by 35.** The record says 25 files carry the `TBC (Cheryl)` literal.
Re-measured at this SHA: **60 tracked `*.html`**, 63 surfaces under `Science_Teesside/` including
3 `.body.txt`. The 25 is right about the **hold** — Build 5 / Grow 5 / Launch 15, exactly item
17's set — but **38 further surfaces** (the `v3_40min` variants) carry the identical hidden
comment, sit outside that ruling, and were unaccounted for in every register.

### The canonical wording (Q-003, pointed at from three registers)

> Every AQA UAS unit code and unit title on any estate surface is an **unverified centre record
> awaiting confirmation** from the UAS coordinator's entry record. It is not a compliance claim,
> and no surface may present it as one. Registration and unit entry being settled does **not**
> confirm a code.

### The pupil-facing half is PROPOSED, and that is a ruling not a dodge

Two of Matt's standing rulings reach it, both `_close/OPEN_ITEMS.md` item 17: the 25 science
sheets *"stay byte-pristine"* until the restore sitting, and **"Pupil-facing authoring stays
Matt's."** So the strips go to `quality/toolkits/PROPOSED_uas_claim_qualifier.md` — the same route
item 17(b) and `PROPOSED_asdan_claim_accuracy_residuals.md` used for this exact class.

| | count |
|---|---|
| occurrences proposed | **185** |
| live files | **44** |
| distinct strings | **88** |
| of which assert a named **UAS unit title** as settled fact | **108 occurrences, 12 titles** |
| held byte-pristine (item 17) | 25 files |
| held-adjacent, unrecorded until now | 38 surfaces |
| short-course module family (FoodWise/LI/Duke) | **HELD**, untouched |

The 38 were **not** edited: correcting variants while the sheets they mirror are byte-frozen would
diverge the two halves mid-hold, which is the failure the byte-reversibility test exists to
prevent.

---

## §4 · Provenance

The 4.667 figure appears in 13 files. Three gaps were not merely missing but **wrong**:

1. **Actively false.** The year map's sensitivity footer read *"No row is marked live. The weekly
   rate is an owner input, not a derived figure"* — stale pre-ruling text sitting seven lines
   under a paragraph calling it derived and directly beneath a row flagged **"THE DERIVED RATE —
   this is the live plan"**. Replaced with the split itself.
2. **Stale total.** The ledger footer hardcoded **133** year-GLH in three places, the figure from
   before the re-anchor. Now derived from the constant.
3. **A divergence PEQ-YEAR-1 introduced.** `COOKING_HANDOVER.md` promises its printable HTML is
   *"same content"*; the generated HTML had **no hours section at all**, and the markdown's own
   was the worst instance in the estate — no split, no ruling date, no owner attribution, no link.
   Both now carry the same two-row **Measured / Ruled** table.

**GROW and LAUNCH, said plainly.** The year map, the handover and `CREDIT_PATHWAYS.md` now state
that the seven-period week was established on **BUILD**; that GROW's ASDAN row is **empty in all
eight built weeks** and LAUNCH's eight planners **disagree on their own row structure**; and that
running all three *level* lanes at one rate is right for one mixed class in one kitchen but is an
**assumption** if read as a statement about the GROW or LAUNCH *rooms*.

**G5 was why this drifted** — it read only `Scheme_of_Work.html`. It now also gates the handover
in **both formats** for the split, the ruling date and the GROW/LAUNCH statement, and the year map
for lane provenance, the one-rate assumption and the calendar evidence split.

---

## §5 · Merge day — refreshed, nothing acted on

Both counts **unchanged**: SL 12 ahead / 7 conflicted; SBX 5 ahead / 8 conflicted. The clone was
**not** shallow (1395 commits, both `merge-base` calls exit 0), so 911/902 behind are real.

**The re-measurement's "standing cost" list was checked and is wrong.** It claimed the estate
carries three unfixed defects because SBX is unmerged. Main's own `Art_Teesside/HANDOVER.md:25`
rules SBX's Bronze → Explore a **REGRESSION** on two signals, and `:29` records C2/C3 already done
identically by R1 and every SBX A2 catalogue id already present. Verified directly: the A2 decks
carry **Bronze only, zero "Explore"**, and **all seven** A2 lessons are catalogued. So the note
now says the opposite: **merging SBX would reintroduce known-bad content into seven live decks.**
SL's residue is a *proposal*, and its workbook is already on main in a newer copy.

Neither merged, neither deleted. The staff-pack lockup line is kept. The `resources.json` blocked
line is **closed** — Apps is attached, so the pin moved properly.

---

## §6 · Gates

| gate | result | control |
|---|---|---|
| ledger proof + `_assert_calendar()` | **PASS** | 3 planted calendar faults → all **RED** |
| matrix zero-gap (174 ACs / 18 units) | **PASS — 0 gaps** | `L2K_PLANT_GAP=1` → **RED** |
| pass gates G1–G5 (**widened this pass**) | **ALL GREEN** | `L2K_PLANT_XLEVEL=1` → G4 **RED** |
| `v3_tier_gate` · `minima_gate` · `verb_gate` | **PASS** | — |
| protected gate | **PASS** — every marker count unchanged | — |
| food gate (ZERO + FROZEN) | **PASS** | `PEQ_YEAR1_PLANT_DISH=1` → **RED** |
| sentinels 50/123 | **PASS** — set-identical | — |
| food census `protected2.py` | **PASS** — unchanged | — |
| **pin check, both gate copies** | **PASS** | — |
| chip gate | **PASS — 28/28 limbs**, zero console errors | clicking is the control |
| print parity vs `2310ea0` | **PASS — 6/6 decks** | divergence check is the gate |
| boot clean, 11 Kitchen pages | **PASS** — zero console errors | — |
| `node --check` · `py_compile` | clean | — |

---

## The merge, and the evidence it landed

| | |
|---|---|
| **Lessons merge** | `283d67143a4c50db2eac2660cf20a38f1b8dfdb6` — `--no-ff` on `63271c33` |
| **Apps merge** | `93bbf98ea911bab9601c91efd3f5119a13ec6718` — `--no-ff` on `a7e80737` |
| **Order** | Lessons first, then Apps, as instructed |
| **Pages** | `pages build and deployment` on `283d6714` — **completed / success** |

### Both pins, read back from the two merge SHAs

```
Lessons 283d6714  "resources.json": "907e7875d0e4…
Apps    93bbf98e  "resources.json": "907e7875d0e4…
```

Identical, and the two gate copies are byte-identical (`cmp`) at the merged tips.

### The four pages, re-fetched from the merge SHA

| file | HTTP | bytes |
|---|---|---|
| `Cooking_Handover.html` | 200 | 13 387 |
| `Kitchen_Week_Shell.html` | 200 | 165 229 |
| `Criteria_By_Week.html` | 200 | 77 446 |
| `Kitchen_Completion_Checklist.html` | 200 | 10 880 |

`resources.json` at that SHA carries **651** entries and all six Kitchen ids.

### Phone check — opened from the catalogue, not by URL

The hub was loaded and each page reached **through the catalogue's own search**, never by typing
a path:

```
Cooking Handover              FOUND via search  [Support]
Weekly Shells                 FOUND via search  [Support]
Criteria by Week              FOUND via search  [Support]
Weekly Completion Checklist   FOUND via search  [Support]

GROW chip now reads: GROW Vocational & PfA (48)
zero console errors
```

Each renders as **Support** — the "OPEN PACK →" presentation, not the "interactive tool" one —
which is the §1 type decision showing up where a reader meets it.
