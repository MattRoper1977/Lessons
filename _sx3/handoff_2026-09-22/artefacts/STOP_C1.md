# STOP-C1 — the row-45 expectation cannot be DERIVED for the SX3 31

The order requires, for Autumn 2 batch 1, a **"derived row-45 expectation (6 on science
nine-stage)"**. I attempted the derivation and it cannot be done with the oracle the estate
currently has. Reporting rather than guessing.

## The rule, read from the code

`tools/hum/verify_loop.py` row 1: *"one panel per non-modelling, non-title stage"*.

```python
eligible = [s for s in st if stage_name(s) not in MODELLING_STAGES
            and stage_name(s) != 'title']
```

with `MODELLING_STAGES = {'ido', 'ido2'}` (`tools/hum/loop_adapter.py:45`).

So the expectation is **stages − title − modelling**. For a nine-stage deck that gives
9 − 1 − 2 = **6**, exactly the order's figure. The rule is right and the figure is
consistent with it.

## Why it cannot be derived HERE

`deck_dom.stage_name()` names a stage by, in order: `data-timer="0"` (→ title/complete),
a regex table `STAGE_NAMES`, then `data-kind`, else `'unnamed'`. Run over all 31 decks
(290 stages):

```
stage-name histogram across the 31:
   'unnamed'                    268
   'title'                       20
   'independent'                  1
   'complete'                     1
```

**268 of 290 stages are unnamed.** The `STAGE_NAMES` table is Humanities phrasing
throughout — `watch a worked example`, `try one together`, `now it is your turn`,
`words that help`, `start the enquiry` — and Science decks word their stages differently,
so nothing matches and no `data-kind` is carried.

The consequence is the trap: `ido`/`ido2` are **invisible** on these decks, so the
modelling count comes back 0 for every one of the 31, and the computed expectation is

```
stages  title  ido/ido2  row45 "expected"  decks
     7      0         0               7      3
     8      0         0               8      3
     9      1         0               8     20
    13      0         0              13      5
```

That **8** for the nine-stage limb is not a derivation. It is what the formula returns when
the modelling detector silently finds nothing. It contradicts the order's 6 by exactly the
2 modelling stages the oracle cannot see — which is the tell, not a coincidence.

(The single `'independent'` and single `'complete'` are incidental matches on the generic
words in those two regexes, not evidence the table works on Science.)

## What is needed

The per-deck expectation for the 11 non-nine-stage decks (3 × 7-stage, 3 × 8-stage,
5 × 13-stage) cannot be stated until this is resolved. Two routes, both needing a ruling
because both touch a check:

- **(a) A Science stage-name table.** Extend `STAGE_NAMES` (or add a Science-specific
  oracle) so `ido`/`ido2` and the other stage kinds are found on SCI decks by their own
  wording. This makes the expectation derivable for all 31 and for everything after them.
  It is a check change, so H-LOOSE applies: no check edited without a ruling.
- **(b) Declare the expectations.** Take 6 for the nine-stage limb as given by the order,
  and have the remaining three shapes declared the same way. Faster, but it is typing an
  expectation rather than deriving one, which cuts against derive-don't-type.

I have not taken either. Nothing has been transplanted, reclassified or edited.

## What IS established and stands

- The population: 31 distinct members, derived from
  `_glv3/tools/verify_change_boundary.py::REPLACEMENT_TRANSACTIONS`, matching
  `_sx3/HELD.md`'s "Build 1 · Grow 7 · Launch 23" exactly.
- The whole 31 is Autumn 2; batch 1 is a choice of ≤12 from them.
- row45 is **0 on all 31** — measured with `verify_loop.panels()` over `deck_dom.parse()`,
  never a regex. That zero is the gap PASS C fills and is not in doubt: it does not depend
  on stage naming, only on the absence of `lundy`-class ribbons.
- Shape buckets (stage counts) are sound: 3 × 7, 3 × 8, 20 × 9, 5 × 13.

Per-deck detail written to `PASSC_ROW45_DERIVED.json` — with the caveat above attached to
its `row45_expected` column, which must not be used until STOP-C1 is ruled.

## Two further measurements taken while checking the above

`data-kind` — the third naming route — is **absent on every one of the 290 stages**:

```
data-kind on the 290 stages: {'<absent>': 290}
data-timer: {'4': 132, '5': 47, '10': 35, '2': 27, '0': 20, '6': 8}
```

The 20 `data-timer="0"` stages are exactly the 20 named `title`, which is why that one route
works and the other two do not.

Sample probe text from stages the table fails to name — Science wording throughout:

```
Give a Rock a Job · Classic
Four clues to start
One rock for every job?
Make the science visible
Use the evidence together
Show your science
```

"Four clues to start" is plainly a starter, but the table looks for `\bstarter\b` or
`start the enquiry`, so it does not match. That is the shape of the whole problem.
