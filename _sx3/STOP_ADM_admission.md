# STOP-ADM — the six content PRs are red because of the caller I added in #584

Found while fencing. It changes the shape of §3's one content change, so it is
reported before anything is written to a deck.

## What is failing

Every one of the six content branches fails the cross-estate gate on the same
line. Measured directly against `claude/sx3-grow-1` with the same invocation the
caller makes (`--base origin/main`):

```
[FAIL] standalone/offline boundary violated by changed files:
  ['Science_Teesside/Grow/W8-W13_2026-27/SCI_G_W10A_Solar_System_Research_Explore.html',
   … all 12 decks on the branch …]
```

`boundary_errors()` permits only paths in
`ALLOWED_DIFF | CANONICAL_HASHES | CATALOGUE_PINS.files | CATALOGUE_RECORD_PATHS`.
Its stated invariant is *"no standalone lesson or studio is CHANGED by this
release"*.

## Why it started failing now — attribution

The estate admits a lesson deck by naming it in **two** places at once:

1. the workflow's `pull_request.paths` — an explicit **514-entry list**, not a
   glob, which includes specific decks such as `SCI_G_W3_Friction.html`,
   `SCI_L_W4_L1_Diffusion.html`, `SCI_B_W8A_Sugar_Labels_Explore.html`; and
2. the boundary's permitted set, via `CATALOGUE_PINS`.

Measured: of the **24** named Science `.html` files in that trigger list,
**24 are boundary-permitted**. The pairing is the mechanism.

> **Correction, ORDER SX3-M5 §1(a).** I first described that 24/24 pairing as an
> observed coincidence with a silent failure mode. It is not a coincidence and
> the failure mode is not silent: **`tools/pin1/derive_triggers.py` already
> asserts it**, in both directions, on every run. `CATALOGUE_PINS` is the
> registry; `--write` materialises the matching trigger paths into the
> workflow's `BEGIN/END PIN1 DERIVED PATHS` block; `--check` fails if the two
> sets differ either way. So the trigger list is **generated**, not
> hand-maintained, and admitting a deck is not a CI edit.
>
> This session met it head-on: adding `_sx3/FENCE.json` to `CATALOGUE_PINS`
> reddened `static-contract` on #589 with
> `missing=['_sx3/FENCE.json']`, and `derive_triggers.py --write` cleared it.

Measured on this release's decks:

| | in the 514-path trigger list | boundary-permitted |
|---|---|---|
| the 36 landing decks | **0** | **0** |
| the 20 held decks | 1 | 1 |

So before `#584`, a pull request touching only these decks **did not fire this
workflow at all** — they are not in its trigger list. The caller I added in
`#584`, `cross-estate-on-content.yml`, fires on `Science_Teesside/**`, which is
far broader. It subjects every Science deck to a gate whose boundary rejects any
deck that has not been admitted.

**That is mine.** ORDER SX3-END2 §1 asked for the dormant trigger to be fixed;
the caller does fire, and §1 was satisfied on that narrow point. But it fires on
content the gate is built to refuse, and I did not measure that before landing
it. The six red content runs are the consequence.

It is not *wrong* that these decks are now gated — they should be. What is wrong
is that they were never admitted, and the caller surfaced that as a wall rather
than as a finding.

## What the sequence has to be

Admission is not a separate step that can follow the content change; the boundary
and the pins are the same mechanism. Measured: adding the 12 landing decks of one
branch to the pinned set and re-stamping **refuses**, with

```
[FAIL] Part L lesson order differs from its accepted evidence projection
```

`pin_catalogue_contract.py` will not pin while `lesson-order.json` disagrees with
the decks. Which is correct, and it fixes the order of operations:

1. held decks out of every PR (corrective commit);
2. the content change — binding keys + token — so the decks become **provable**;
3. regenerate `lesson-order.json` → `weekBound == 274`, `unresolvedTiming == 0`;
4. add the 36 to the pinned set and re-stamp **both** gate copies;
5. only then does the boundary pass and the gate go green.

Steps 2–4 must be in the **same** pull request as the deck bytes. A content PR
without its pins is red by construction, and a pin PR without the content cannot
be stamped. This is what ORDER SX3-M2's CLOSE calls *3b … resources.json digests
+ pins*, but it cannot wait until 3b: it belongs in each content PR.

## What I am asking

§3 is authorised and I have written nothing to a deck. Two points need your word,
because both widen what "one content change" contains:

1. **Does the content change carry its own admission?** — i.e. each of the six
   PRs lands its decks, the regenerated `lesson-order.json`, and the 36 new
   entries in `CATALOGUE_PINS` in both estate copies. That is the only sequence
   that can be green, and it adds ~36 pinned paths and a `pin_catalogue_contract.py`
   list change to the release.
2. **Does the caller's path filter stay broad?** `Science_Teesside/**` will keep
   catching every future unadmitted deck the same way. Narrowing it to the
   admitted set would restore the old behaviour and re-hide the problem; leaving
   it broad means every new deck must be admitted before it can land. I think
   broad is right and the wall is the gate working — but it is a standing
   consequence and it is yours to choose, not mine.
