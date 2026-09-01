# PROPOSED CONTRACT ROWS — run 6

**NOT APPLIED.** Nothing here is in `STYLE_CONTRACT.json`. These are proposals for Matt, each derived from a measurement in this run, not from taste.

Every row states what enforces it and whether it binds new work only or live work too. **No row is proposed as binding on live work**, because every one of them would red a large part of the estate on the day it landed, and this order does not rewrite finished lessons to satisfy a new rule.

---

## visuals.explanatory.min
**Value:** at least one explanatory visual in every "I do" stage, and at least two per lesson. Each must be print-safe and referred to in the prose of its own stage.
**Rationale:** measured — 51% of 350 live lessons have zero explanatory visuals; the estate median is 0 and the maximum anywhere is 2. All three Humanities families have none at all.
**Enforced by:** g24 (`_sownb/vb/tools/g24_visual_density.py`), currently report-only.
**Binds:** NEW WORK ONLY. Binding on live work would red roughly half the estate at once.

## visuals.decorative.max
**Value:** at most one decorative visual per lesson, and decorative visuals never count toward `visuals.explanatory.min`.
**Rationale:** without a ceiling the cheapest way to satisfy the row above is to add pictures that explain nothing. g24 already counts the two separately, so the ceiling costs nothing to enforce.
**Enforced by:** g24.
**Binds:** NEW WORK ONLY.

## wedo.rotation
**Value:** no two consecutive lessons in a family use the same "we do" type, and across any six consecutive lessons at least four distinct types appear.
**Rationale:** measured — BUILD ASDAN runs twelve consecutive lessons with an identical type-set. Three types carry ~85% of all observed "we do" activity.
**Enforced by:** g25 (`_sownb/vb/tools/g25_wedo_variety.py`), currently report-only.
**Binds:** NEW WORK ONLY.

## wedo.taxonomy
**Value:** the six types in `BASELINE_VISUALS_WEDO.md` — commit-and-reveal, sort-or-match, label-or-annotate, sequence-or-rank, predict-then-check, spot-the-error.
**Rationale:** discovered from the estate, not imposed. Four are already in use; two (predict-then-check, 3 uses; spot-the-error, 1 use) are nearly absent and are included precisely to bring them back.
**Enforced by:** g25.
**Binds:** NEW WORK ONLY — **and it cannot be enforced at all until Matt confirms the six.** This is the blocking one.

## load.period.ceiling
**Value:** pupil words ≤ 1.5× the family median. Reading time is estimated at an **assumed** 90 words per minute, with a 60–120 band reported; no measured reading rate exists in this repository or the workbooks.
**Rationale:** measured — six live lessons run 2.67×–3.75× their family median; two need ~96% of a 40-minute period for reading alone, and the real timetable has no double periods.
**Enforced by:** g23, which becomes BINDING on new work at this row and stays report-only on live work.
**Binds:** NEW WORK ONLY.

## period.declared
**Value:** every new deck declares its period length, and its stage timings sum to exactly that.
**Rationale:** all 48 verified surfaces already declare nine stages summing to 40, so this codifies existing practice rather than changing it. It exists so that if a double period is ever timetabled, a deck built for it says so instead of being read as an overload.
**Enforced by:** the static pack gate's timing-spine check, already running.
**Binds:** NEW WORK ONLY. Live work already satisfies it.

---

## What the next authoring wave cannot start without

**`wedo.taxonomy`.** Every other row can be measured and applied to a lesson after it is drafted. The taxonomy has to exist before drafting, because `wedo.rotation` is defined in terms of it and an author needs to know which six types they are rotating through. One confirmation unblocks both rows.

The remaining five can be adopted in the same PR as the first new lesson, or deferred, without blocking anything.
