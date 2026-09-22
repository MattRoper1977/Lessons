# STOP-C3 — the naming branch is not fit to open. Three defects, measured.

Branch `claude/sci-stage-identity` @ df6bcb7a (pushed, NO PR opened).
Found by the six-lens adversarial review; each item below re-measured by me against
the branch head, not taken from the lens.

## D1 (CRITICAL) — declared_count reds rows 2, 14 and the row-45 composite across the estate

`declared_count()` resolves each stage through EYEBROW_STAGE only -- a 16-phrase
SCIENCE vocabulary -- but rows 2 and 14 now gate EVERY deck on it. Where a deck has no
eyebrow, or one outside that vocabulary, declared_count returns 0 while stage_name
resolves 1, 2 or 3 correctly by an earlier route. The rows then FAIL on correct decks.

                    decks   row 2 FAIL   row 14 FAIL
    Humanities        230           60            92
    Science           200          117           162

431 mismatches. 345 are declared=0 (no eyebrow channel at all); 86 have declared > 0
and are real disagreements (declared=3 resolved=1, declared=1 resolved=8, ...).

Row 45 is a composite of rows 1, 2, 14 and others, so it inverts with them.

The ruled intent was the opposite: stop rows passing over an EMPTY set. As implemented
it manufactures failures on decks that are right.

CANDIDATE SCOPING measured: assert only where "the eyebrow is this deck's identity
channel" (>=1 eyebrow present AND every eyebrow in the emitted vocabulary):
    Humanities  138 of 230 eligible -> row2 FAIL 0, row14 FAIL 0
    the 31       31 of  31 eligible -> row2 FAIL 0, row14 FAIL 0   (ruled population intact)
    Science      89 of 200 eligible -> row2 FAIL 35, row14 FAIL 51  <-- STILL RED
The residual 58 Science decks may be GENUINE instances of the very defect the ruling
exists to catch, or may be out of scope. That is the ruling needed.

## D2 (HIGH) — row 47, added because "an empty set is not a pass", passes over an empty set on every Humanities deck

    PATHWAY_SEGMENT = ^(build|grow|launch)\s+science(\s+\S+)?$

"science" is hard-coded, so on a Humanities deck the pathway segment is never stripped,
deck_title_heading() never equals any stage heading, the subset is empty, and row 47
PASSES having tested nothing.

    Humanities decks binding >=1 stage:   0
    Humanities decks binding ZERO:      230   (230/230 vacuous)

This is the identical failure mode ruling 3 was written to abolish, reproduced by the
row added to enforce it. Row 47 also has no declared-count guard of its own.

## D3 (MEDIUM) — the ordinal rule has no upper bound

Ruling 3: "the second 'I do' in document order is ido2". Measured on synthetic input:

    four bare "I do" stages -> ['ido', 'ido2', 'ido2', 'ido2']

The third and fourth are silently ido2 as well. The landed 31 carry at most two, so
nothing measured moves -- but the rule as coded says "every occurrence after the first",
which is not what was ruled.

## REFUTED — two lens findings I could not reproduce

- "248 unnamed, not 268". FALSE. Measured on main's oracle over the 31:
  {'unnamed': 268, 'title': 20, 'independent': 1, 'complete': 1} = 290. The figure
  reported to Matt and accepted is correct.
- "the ordinal rule never fires on the landed decks; the word table pre-empts it".
  FALSE. Of 45 ido2/wedo2 on the 31, the eyebrow route decides 45 and an earlier
  route decides 0.

## WHAT STANDS

- 0 stage NAMES change on 2123 Humanities stages / 742 files, and 0 on the 34 Science decks.
- The 31: 290 stages, 0 unnamed, 28 title, 54 modelling -> 208 expected panels,
  reproducing ruling 2's table exactly.
- Splitter: 29 self-test controls PASS; the three merged decks split 8->9, timer total
  unchanged; build_catalogue's own title-slide fallback reads ['Aut2'] before AND after
  on all three.

## NOT DONE, and deliberately

- No PR opened.
- The catalogue contract re-pin (deck_dom.py and verify_loop.py are REVIEWED_PATHS) is
  NOT done, so no Apps companion was cut either. Re-pinning would have frozen these
  bytes into both gate copies.
