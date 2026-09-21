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

**The battery is unchanged — and that is not a control.** `verify_loop.py --self-test` returns the
same 6 PASS and the same one SKIP ("the fixture-driven rows: no untransplanted copy of the fixture
is available"), exit 0, on the patched code and on `git HEAD`. A second review round challenged
that line as evidence, and it is right. Measured by wrapping `verify_loop.stage_name` in a call
counter and running `self_test(Path('.'))`: those six controls call `stage_name()` **zero times**.
They are pure `earwig_stages()` arithmetic over name lists the test supplies itself. An unchanged
battery therefore says nothing whatever about a change to the oracle, and it is struck here as
evidence for this one. What the measurement found instead is worse than the claim it removes.

**The fixture-driven battery has been dark since #613.** `self_test` takes its fixture from
`git show origin/main:Humanities_Teesside/GROW_W1-W8_2026-27/GROW_Humanities_W4_Explore_Hanukkah_And_The_Theme_Of_Light.html`
and skips everything downstream when that copy already carries the panel. #613 (`256e5331`,
HUM-T batch 2) transplanted that very deck on main. So from the moment #613 merged, 29 of the
self-test's 35 checks have not run — among them the row 14 red proof, the four row 16 proofs and
the two row 15 proofs. Supplied with the pre-transplant bytes the battery runs in full:

```
fixture from origin/main (as shipped)   :  6 checks,   0 stage_name() calls,  29 SKIPPED
fixture from 256e5331^ (pre-transplant) : 35 checks, 775 stage_name() calls,  35 PASS 0 FAIL
```

**And un-skipped it still could not have caught this defect.** Run against the *shipped* data-type
oracle with that same pre-transplant fixture it is 35 PASS, 0 FAIL, with the row 14 red proof
present and passing. Its one fixture is a nine-stage deck that types its own stages
`title / arrival / starter / ido / wedo / ido2 / wedo2 / independent / exit` — the single shape on
which the data-type short-circuit and the name-derived oracle agree stage for stage, all nine
identical, no slide carrying an `id` at all. A red proof is only as wide as its fixture; this one
is one deck, and it is the deck the defect does not touch.

Neither the skip nor the single fixture is altered here. `verify_loop.py` is a check, and no check
is edited without a ruling; both go to Matt as findings.

## Still open

18 already-transplanted decks carry a Lundy panel on their Title stage — the pre-P1 batch-1
decks already scheduled for a re-cut. Row 14 reds on them; that is the row working, not a new
defect, and the re-cut is the fix.

## Estate-wide sweep — three sites outside the ruled scope, named not changed

The rule binds "every E-check and the HUM-T / PASS B verifiers", and those are fixed at the oracle
above. A sweep of every `data-type` read in `tools/` and `_passhumd5/` finds three more places that
take stage identity from the type attribute. All three sit OUTSIDE the ruled scope, so none was
touched. They are recorded here with their measured size, for a decision.

**`tools/easter/classroom_presentation.py:26`** — the largest.

```python
phase = PHASES[index] if len(stages) == 9 else stage.get('data-type','')
stage.set('data-classroom-phase', phase)
```

It stamps `data-classroom-phase` from `data-type` on any deck that does not have exactly nine
stages. Measured across the landed Humanities decks:

```
decks by stage count : {9: 197, 10: 8, 12: 15}
the data-type fallback fires on 23 of 220
```

On the 15 twelve-stage decks (Autumn 1 W3–W7) seven slides would all be stamped `ido`. The chassis
CSS selects on `[data-classroom-phase]`, so unlike the verifier sites this one reaches what is
**displayed**, not only what is checked.

**`tools/build_resources/author_w8a_chassis.py:544`** — `indep = [s for s in stages if
s.get('data-type') == 'independent']`, then asserts the list is exactly `['slide-8']` with
`data-timer="10"`. Identity by type, but pinned to one expected id, so it reds rather than silently
mis-identifying. Lowest concern of the three.

**`tools/sx3/split_arrival_stage.py:172–179, 217`** — reads stage 0's `data-type == 'arrival'` to
decide whether the split is needed, and writes `data-type="opening"`. This is the writer that
created the opening/arrival split in the first place; a deck it has not run on is exactly a deck
whose overview is still typed `arrival`.

## Two defects in the first cut of this fix, found by adversarial review

**"Start the enquiry" is the STARTER.** It was in the `title` pattern for one revision. Measured:
132 slides carry the phrase and every one sits at **position 2**, after the overview
(`data-timer="0"`) and the arrival task, with `data-timer="3"`. Reading it as the overview gave
**131 of 238 decks two title stages** and removed 132 teaching stages from `eligible`. Now in
`starter`. After: exactly one title stage on 220 of 220 landed decks and 18 of 18 Summer 1 decks.

**A topic word must not beat the deck's own statement that a stage has no teaching time.**
`GROW_A2_W07_Lesson.html`'s overview reads "Belief and belonging review"; the `review` pattern
claimed it before the timer fallback ran, so the overview resolved to `review` — eligible — and a
panel would have landed on the metadata stage. `data-timer == "0"` is now tested **first** and
resolves only between the two stages that legitimately carry no teaching time:

```python
if (node.attrs.get('data-timer') or '').strip() == '0':
    return 'complete' if COMPLETE_RX.search(probe) else 'title'
```

Measured: 1 deck before, 0 after.

## Known drift: 11 transplanted decks record a stage name this oracle no longer returns

`ido -> ido2` and `wedo -> wedo2` on 22 slides across GROW_HUM W9–W14 (5 decks) and LAUNCH_HUM
W9–W14 (6). The eligible / modelling / title sets do **not** move — `ido2` is modelling exactly as
`ido` is, `wedo2` eligible exactly as `wedo` is — so no panel moves and no row changes verdict.
But each panel records `data-loop-stage-name="wedo"` where the slide's own heading says "We Do 2",
so **those 11 decks are not byte-reproducible by their own adapter until they are re-cut**, by one
attribute value per deck. The new name is the correct one; the old was the defect. Recorded rather
than preserved.

## A second review round: three more claims, each re-measured before it was believed

The first round is above. A second set of lenses returned three further claims against this fix.
None was taken on trust; each was measured here.

**"The self-test is not evidence — it never calls `stage_name()` once."** CONFIRMED, and it
carried a larger finding with it. Struck and recorded under *The controls it passed*, above.

**"90 slides whose own text says 'I Do' leave `modelling` and receive a pupil-response panel."**
REFUTED as worded, CONFIRMED in its number, against a population I had not measured. Across the
220 landed and 18 Summer 1 decks, slides whose own words say "I Do" and are *not* in `modelling`:
**0**. My first answer stopped there and called the claim refuted; that was the wrong predicate on
the wrong set. The 90 is real and it is elsewhere — see the next section. And no slide receives a
panel, because none of those decks is transplanted.

**"`data-kind='learn'` maps to a name in neither `MODELLING_STAGES` nor the title set, so 17
slides become eligible."** CONFIRMED, and it is 90, not 17.

## What the fixed oracle does to the Autumn 1 W3–W7 decks — nothing served, ruling wanted

Measured over the fifteen `*_Humanities_W3..W7.html` decks in
`Humanities_Teesside/Teaching_Packs/{BUILD,GROW,LAUNCH}/HTML/`, shipped oracle against fixed:

```
stages whose NAME changes across the two oracles : 105 of 180
of those, stages whose ELIGIBILITY changes       :  90, every one ido -> eligible
    ido -> independent  28        ido -> arrival     15
    ido -> learn        17        ido -> vocabulary  15
                                  ido -> wedo        15
```

Those decks stamp `data-type="ido"` on every stage after the title. Under the shipped oracle all
twelve stages of each were "modelling", `eligible` was **empty**, and the deck could never have
received a pupil-response panel at all — the same empty-set failure as row 14, in a different row
and on a different set of decks. The fixed oracle reads each stage from its own heading and
`data-kind`, which is what ruling 5 is for. This is the change working, not a regression.

**Nothing served or judged changes today.** None of the fifteen carries a panel (`panels=0` on all
fifteen) and none appears in `HUMANITIES_STRAND.json`, so `verify_loop` does not see them. The
change lands when the Aut1 W3–W7 PASS B batch is cut.

**Before that batch it needs a ruling.** Two of the new names are new to the estate as
panel-bearing stages: `learn` (17 slides) and `vocabulary` (15). `loop_adapter.py:179` derives the
panel's visible label from the stage name, so a pupil would read a panel headed "learn" or
"vocabulary". Nothing fails closed — the adapter keys only off `MODELLING_STAGES`, `lundy_stage`,
`title` and `exit`/`complete`, and the task text is derived from the slide's own content, so an
unfamiliar name needs no table entry. It is a wording decision, and it is not mine to take.
