# DECISIONS_YEAR1.md — pass PEQ-YEAR-1, gate record

**Instrument:** `MASTER_PROMPT_Pass_PEQYEAR1_20260821.md` · sentinels
`peq-year-1-2026-08-21-TOP` / `-BOTTOM`
**Base:** `2a8f9f5` (*Merge PEQ-L2K close: P9 lodged (#146)*) — the expected PEQ-L2K merge chain.
**Branch:** `claude/new-session-yed8ua`.
**Rollback:** `git reset --hard 2a8f9f56344f323436b86558e0aee51839657262`

> **Branch-name note.** The instrument names `claude/peq-year-1`. This session is bound to
> `claude/new-session-yed8ua` and may not push elsewhere, so the work is on that branch. Same
> base, same content; only the ref name differs.

---

## §1 · The timetable — measured, then STOPPED

Full record: [`DERIVATION_YEAR1.md`](DERIVATION_YEAR1.md). Reproduce:
`python3 _passpq/tools/year1_derive.py` (exit **1** while any lane is unestablishable — that is
the gate, not a bug).

| | |
|---|---|
| **Established** | the **40-minute** period unit (15 agreeing statements, all three lanes, every one on a science row) · BUILD's **six discrete weekly slots at one period each** ("one-slot week" — the only cell in the estate that fixes a slot count) · BUILD's stable 8/8 row layout, bounding its PEQ time at **0.67–4.67 h/wk** |
| **Not established** | the carryable-slot share (needs the member-gated delivery guide or a coordinator ruling) · **GROW**, whose ASDAN row is empty 8/8 weeks · **LAUNCH**, whose eight planners disagree on their own row structure · spring and summer, which have no dates anywhere in the repo |
| **Verdict** | **STOP** per §1.4. A guessed slot is worse than a paused pass. |

Every lane derivation was independently challenged by an adversarial auditor before this
verdict; all three initial measurements were refuted, which is what drove the pass to the
evidence that actually settles it.

## §2 · The year map — re-based, not re-anchored

The re-anchoring §2 asks for is **blocked by §1's STOP**: there is no derived constant to
regenerate on, and inventing one is the failure mode §1.4 names. What was done instead, because
it needs no derived rate and answers §2's actual question:

- The sensitivity table is **re-based from the round numbers 2/3/3.5/4 onto the measured
  40-minute period**, across the 1–7 period band the evidence supports. Every row but one is a
  whole count of the school's real periods.
- **No row is marked live.** The weekly rate is labelled an owner input on the page, which is
  what it has always been and was not previously said.
- Reachability is reported per lane per qualification at every period count.
- The **co-delivery claim is re-checked**: at six periods a week the E3 lane's 7 declared hours
  are unnecessary and the page says to withdraw them.
- Ledgers still sum (G1) and the matrix still has **0 gaps** at 38 weeks.

**What the re-basing exposed.** 3.5 h/wk is **5.25 periods** — the only rate in the band that
is not a whole number of the school's periods, and *exactly* the point at which the E3 and L1
Certificates flip from out-of-reach to reachable. At five whole periods those lanes land the
Extended Award. That is now stated on the page as the timetabling decision it is, rather than
sitting unnoticed inside a round number.

## §0 · Hedges — 245 triaged, 184 stale, rewritten

Before/after table: the workflow record, summarised in the commit messages. Families: planning
READMEs · BUILD/LAUNCH year-plan workbooks · live ASDAN schemes, hubs and START_HEREs · Estate
v3 mirrors · governance registers · the two generators that would otherwise regress their own
pages. **Kept**: every achievement, EQA-booking, IQA, signature, "working towards" and "no
Level 2 is registered" string, and the L1 14-of-15 note as a centre choice already made.

Four corrections applied on review, three of them to wording this pass had itself proposed:

| defect | fix |
|---|---|
| *"The entered codes are:"* asserted the repo's module names **are** the entered codes | restated as *"Confirm the module/challenge codes below against the entry record"* |
| LI/FoodWise decks lost the **challenge-code check** along with the registration hedge | restored — registration and codes are different things |
| *"registered via the **UAS/ASDAN** coordinator"* merged two awarding bodies, 12 places | reduced to a tense change only |
| `gen_resources.py` `build_launch()` kept the stale string **split across two Python lines**, invisible to every line-based grep, and would have reverted the page on the next build | fixed; a concat-normalised re-sweep now returns 0 |

## §3 · Orchestration — recorded as decided fact

L1 lane = **all six L1 units, 15 credits, all at level** (§5.1 permits exceeding 14; the
exact-14 combination stays named as a *fallback*, not an open alternative) · **barred
combinations** stated (one level per skill, witness Level tick is the record) · the **LAUNCH
room runs E3/L1/L2 concurrently**. Written into the ledger, the year map and
`CREDIT_PATHWAYS.md`. **Lane targets deliberately not set** — they follow from the period count
§1 could not derive; both honest outcomes are stated instead.

## §4 · The colleague's frame — built, with zero cooking content

`COOKING_HANDOVER.md` + `Cooking_Handover.html` · `Kitchen_Week_Shell.html` (38 pre-filled week
pages, each with an empty *"What we are cooking this week"* box) · `Criteria_By_Week.html` (the
coverage matrix inverted, generated from the same mapping so the two cannot drift) ·
`Kitchen_Completion_Checklist.html`. All generated by `l2k_build.py` in estate house style, so
they cannot be hand-edited out of sync.

## §5 · Merge day — [`MERGE_DAY_29AUG.md`](MERGE_DAY_29AUG.md)

SL and SBX **measured on an unshallowed clone** (a shallow clone makes `merge-base` fail and
`A...B` degenerate into garbage counts): 12 and 5 commits ahead, 7 and 8 conflicted files, both
on the estate's recorded never-merge list. **Neither merged, neither deleted.** If nobody merges
on the 29th, nothing breaks — and merging SL would actively regress a workbook main has already
moved past.

---

## §6 · Gates

| gate | result | control fired |
|---|---|---|
| ledger proof `l2k_plan.py` | **PASS** (asserts before writing) | — |
| matrix zero-gap `l2k_build.py` (174 ACs / 18 units) | **PASS — 0 gaps** | `L2K_PLANT_GAP=1` → *"RED GATE (planted control): CrThSk2 has unmapped criteria"*, exit 1 |
| pass gates `l2k_gates.py` G1–G5 | **ALL GREEN** | `L2K_PLANT_XLEVEL=1` → G4 **RED** on 3 surfaces |
| build idempotence | rebuild → 11/11 byte-identical | — |
| `v3_tier_gate.py` | **PASS** — 12 decks, 0 unruled L2 strings | (fired for real — see below) |
| `minima_gate.py` | **PASS** — 44 surfaces | — |
| `verb_gate.py` | **PASS** — 0 off-pitch | — |
| `protected_gate_e3.py` | **PASS** — 75 window shifts all authorised, every marker count unchanged | (fired for real — see below) |
| sentinels 50/123 | **PASS** — set-identical to base, counts hold | — |
| food census `_sca1/tools/protected2.py` | **PASS** — 468 protected strings, 12 families, 46 files, **unchanged** | — |
| **`food_gate.py` (new)** | **PASS** — ZERO on the 5 new surfaces, FROZEN census on the 7 existing (verified against HEAD) | `PEQ_YEAR1_PLANT_DISH=1` → **RED**, 9 hits |
| print parity `l2k_printparity.mjs` vs `2310ea0` | **PASS** — 6/6 decks, only the ruled transforms | divergence check is itself the gate |
| PART B `l2k_partb_gate.mjs` | **ALL GREEN** — 6 decks × 3 viewports | — |
| chip gate `verify_lessons_chips.mjs` | **PASS — 28/28 limbs**, zero console errors | clicking is the control |
| `node --check` · `py_compile` | clean on every touched tool | — |
| `pin_manifests.py --check` | **BLOCKED** — `MISSING apps.json (no owning checkout found)` | see below |
| `year1_derive.py` | **exit 1 by design** — the §1 STOP | — |

### Two gates that fired for real, and what they caught

1. **`v3_tier_gate` went red on 7 files.** The hedge rewrite ended the preceding clause with a
   full stop, capitalising the allowlisted string to *"**No** Level 2 is registered or claimed"*
   and dropping it out of `L2_ALLOWED_ANY`. Rejoined with a semicolon; 13 occurrences restored
   verbatim. **The gate was right and the edit was wrong.**
2. **`protected_gate_e3` went red** with `MARKER COUNT MOVED [] -> [n]` on the four new pages. A
   count move is unconditionally red and *cannot* be authorised in the deltas TSV — that
   mechanism is for window shifts on existing files. The four are new surfaces, so the delta is
   additive and belongs in the manifest, per the PEQ-L2K precedent (*"+9 manifest rows are the
   only manifest delta"*). **+5 rows appended, −0**; the 746 existing rows byte-unchanged; and
   the append asserts first that no file lost a stream without gaining one, so a deleted
   protected surface cannot slip through disguised as an addition.

### The food gate's own two false starts

Worth recording, because a gate that passes wrongly is worse than one that fails. Version 1
built its alternation by splitting a pipe-delimited blob, producing **empty alternatives that
matched at every position** — 495 372 "hits" on one file. Version 2 fixed that but split on
whitespace too, tearing *"fish and chips"* into three entries so the bare word **"and" became a
dish**. Version 3 is explicit Python lists with assertions that the compiled pattern cannot
match the empty string, plus a discrimination test (neutral frame text → 0; a real recipe → 9).

### `resources.json` — untouched, deliberately

`pin_manifests.py` writes **both gate copies or neither**, and the Apps checkout is unreachable
here. The current pin matches on disk
(`de9e7c61515397bae87ef3c7afadb57426afbe4fcf0f58dbe7b174cdac582374`) and stays green **because**
the pass left the file alone. The four new pages are therefore not in the catalogue yet, and
`resources.json:6109` now contradicts the page it indexes. Both logged as
[`PROPOSED_YEAR1.md`](PROPOSED_YEAR1.md) P6 — the honest blocked line, not a silent skip.

### Phone checks

`Cooking_Handover.html` and `Kitchen_Week_Shell.html` rendered at 390 px and in print emulation:
clean, house style, zero console errors. Horizontal overflow at 390 px is the estate's
pre-existing norm for these print-first pages (existing pages: 0–796 px; the new ones: 9–91 px),
and `Scheme_of_Work.html` measures **796 px before and after** — the re-based sensitivity table
did not widen it.
