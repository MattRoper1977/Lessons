# Ruling 3 measured — how much currently passes without testing anything

Ruling 3: *"an empty set is not a pass. Row 14 asserts title_stages == the shape's declared
title count … and then 'no panel on any title stage'; a mismatch is RED. Same rule applied
to every 'X stages carry no panel' row."*

`verify()` builds three subsets, all three from `stage_name()`:

```python
eligible    = [s for s in st if stage_name(s) not in MODELLING_STAGES and stage_name(s) != 'title']
modelling   = [s for s in st if stage_name(s) in MODELLING_STAGES]
title_stages= [s for s in st if stage_name(s) == 'title']
```

Measured over the 31, current oracle vs what the decks declare by eyebrow:

| decks | stages | `eligible` now / declared | `modelling` now / declared | `title_stages` now / declared |
|---:|---:|---:|---:|---:|
| 3 | 7 | **7** / 5 | **0** / 1 | **0** / 1 |
| 3 | 8 | **8** / 6 | **0** / 2 | 0 / 0 |
| 20 | 9 | **8** / 6 | **0** / 2 | 1 / 1 |
| 5 | 13 | **13** / 11 | **0** / 1 | **0** / 1 |

## Two rows pass vacuously today

```
row 2  runs over an EMPTY modelling set on 31 of 31 decks that DECLARE modelling stages
row 14 runs over an EMPTY title set on     8 of 31 decks that DECLARE a title stage
```

- **Row 2** — "I Do stages carry no panel" — tests nothing at all on the **entire
  population**. Every one of the 31 declares 1 or 2 modelling stages; the oracle finds none.
- **Row 14** — "P1-1: the Title stage carries no panel" — tests nothing on **8 of 31**:
  the 3 seven-stage and 5 thirteen-stage decks, whose `Opening` carries `data-timer='2'`
  rather than `'0'`, so the existing timer route misses it. The 20 nine-stage decks are
  found correctly (timer 0). The 3 eight-stage decks declare no title at all, so 0 / 0 is
  correct there and is NOT a vacuous pass — which is exactly why the assertion must compare
  against the declared count rather than simply forbid an empty set.

## And a third, worse consequence — `eligible` is OVER-counted on all 31

Because an unnamed stage is excluded from neither `MODELLING_STAGES` nor `title`, it falls
into `eligible` by default. On the 7-, 8- and 13-stage decks `eligible` is therefore the
**entire** stage list (7/7, 8/8, 13/13), and on the nine-stage decks it is 8 of 9.

Row 1 demands exactly one panel on every `eligible` stage. So under the current oracle,
**had the PASS C transplant run, it would have placed a Lundy panel on every modelling stage
and on every title stage of all 31 decks** — 62 modelling stages and 28 openings that should
carry none. Row 2 would then have confirmed the absence it caused, because its own subset
was empty.

This is the same failure ruling 5 documents for Humanities, now measured on Science, and it
is the concrete reason STOP-C1 had to be fixed before batch 1 rather than after.

## What ruling 3 therefore requires

Both rows gain a declared-count assertion ahead of the panel assertion:

- row 2: `len(modelling) == declared_modelling_count(shape)`, then "no panel on any"
- row 14: `len(title_stages) == declared_title_count(shape)`, then "no panel on any"

with a mismatch RED. The declared count must come from the deck's own declaration, not from
the oracle under test, or the assertion is circular.

Red proof named in the ruling: **a 9-stage deck with its title stage renamed → FAIL.** Under
the current code that mutation makes `title_stages` empty and row 14 passes; under the ruled
form it must go RED.
