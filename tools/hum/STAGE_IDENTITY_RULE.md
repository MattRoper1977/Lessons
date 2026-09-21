# STANDING INSTRUMENT RULE 5 — stage identity

> **A stage is identified by its slide id — by what the deck declares for that slide — and
> never by the `data-type` attribute.** This binds every E-check and every HUM-T / PASS B
> verifier. `data-type` may still be styled on, counted and reported; it may never be the
> value an identity function returns.
>
> Ruled by Matt, 2026-09-22 (Addendum 2 ruling 5, re-affirmed at A3.5 ruling 7).

## What was wrong

`tools/hum/deck_dom.py::stage_name()` — the single identity oracle that `loop_adapter.py`
and `verify_loop.py` both call — returned `data-type` verbatim and short-circuited the table
below it that reads the slide's own words. On a pack deck every slide carries `data-type`, so
that table never ran at all.

## Why that mattered, measured — 220 landed Humanities decks (2,033 slides) and the 18 Summer 1 decks (162)

**`data-type` is a category, not an identity.** One value covers several slides:

| value | slides it covers | where |
|---|---|---|
| `wedo` | 3 — "We do", "Check", "Review" | 120 landed decks and all 18 Summer 1 |
| `arrival` | 2 — "Opening" and "Arrival" | the same 120, and all 18 Summer 1 |
| `ido` | **7** | the 15 Autumn 1 W3–W7 decks |

**A row that enforced a rule ran over an empty set.** `verify_loop` row 14 is P1-1, "the Title
stage carries no panel", and it tests `title_stages`. Because the overview slide is typed
`arrival`, that list was **empty on 120 of the 220 landed decks and on all 18 Summer 1 decks**:
the row passed without testing anything, on more than half the estate. The self-test's own red
proof for row 14 is written `if tstage is not None: …`, so it was skipped for the same reason —
the proof was conditional on the identity that was broken.

**The prospective damage, had PASS B run first.** On the 15 Autumn 1 W3–W7 decks (0 panels
today, on PASS B's ruled order) `stage_name` returns `ido` for seven slides per deck, including
"Try one together", "Choose, then explain" and "Show what you mean" — pupil-response stages.
**103 slides across the 15** would have been excluded from `eligible` as teacher modelling: the
adapter withholds panels that belong there, and row 2 then passes over a modelling set it
wrongly widened, confirming the absence it caused.

**What was NOT wrong, corrected against my own first reading.** `ido2` and `wedo2` are not
unreachable: 22 landed slides carry each. And the Summer 1 modelling set was never empty —
every one of the 18 has `slide-4` typed `ido`. The empty set was the **title** set.

## The rule as implemented

`stage_name()` resolves the slide's own declarations, in this order, each step justified by a
measured count:

1. **`data-title` + the slide's own heading** — present on 1,853 of 2,033 landed slides and
   162 of 162 Summer 1 slides, *better* coverage than `data-type`'s 1,763. Its vocabulary is
   the stage names, and it distinguishes what `data-type` collapses ("We do" / "Check" /
   "Review"; "Opening" / "Arrival"; "I Do 1" / "I Do 2").
2. **`data-kind`** — the declared role, on 180 landed slides; `opening` marks the overview.
3. **`data-timer == "0"`** — the deck's own statement that a stage has no teaching time.
   Measured: timer 0 appears at position 0 on 128 landed decks and all 18 Summer 1 decks, and
   nowhere else except the 8 `id="complete-slide"` slides, which step 1 has already named
   `complete`. So it is safe as a last resort and needs no position argument.
4. **`unnamed`** — never `data-type`.

`STAGE_NAMES` gained `vocabulary`, `check`, `review` and `voice`, and new phrases for the
words the estate actually uses. Every pattern was derived from the measured `data-title`
vocabulary (198 distinct values landed, 39 in Summer 1); none was invented.

## The controls it passed

**Nothing moved.** Across the **62 decks that already carry a `lundy hum-t-loop` panel**, the
`eligible`, `modelling` and `title` sets are **identical** before and after — 0 decks move.
The change reaches only decks that have not been transplanted.

**Nothing lost.** Slides resolving to `unnamed`: **0 before, 0 after**. Every slide in the
estate and in Summer 1 still resolves to a named stage.

**The untestable row became testable.** Decks where row 14 ran over an empty `title_stages`:
**120 → 0** landed, **18 → 0** Summer 1.

**Where it lands.** 135 un-transplanted landed decks and all 18 Summer 1 decks change: the
Autumn 1 W3–W7 decks go `eligible 4 → 10, modelling 7 → 1`, and the Summer 1 decks go
`eligible 8 → 7, title 0 → 1`.

**Red proof (a) — row 2 reds when an I Do stage carries a panel.** On
`GROW_HUM_W11_Light_Across_the_Map_OUTSTANDING_V3_1.html`, with the deck's *own* panel bytes
grafted into its I Do stage:

```
row 2 as shipped                                  : PASS  modelling stages tested: 2   []
row 2 with a panel grafted into the I Do stage    : FAIL  modelling stages tested: 2   ['ido']
```

**Red proof (b) — the empty set, proved both ways.** On `BUILD_SU1_W02_Lesson.html` with a
panel grafted onto its overview stage (`slide-1`, `data-title="Opening"`, `data-timer="0"`):

```
row 14 under the SHIPPED identity (data-type) : PASS  title stages tested: 0   []
row 14 under the FIXED identity   (slide id)  : FAIL  title stages tested: 1   ['title']
```

The breach is the same breach in both runs. The shipped identity could not see it.

**The battery is unchanged.** `verify_loop.py --self-test` returns the same 6 PASS and the same
one SKIP ("the fixture-driven rows: no untransplanted copy of the fixture is available"), exit 0,
on the patched code and on `git HEAD`. That SKIP is pre-existing and is not cleared by this change.

## Still open

18 already-transplanted decks carry a Lundy panel on their Title stage — the pre-P1 batch-1
decks already scheduled for a re-cut. Row 14 reds on them; that is the row working, not a new
defect, and the re-cut is the fix.
