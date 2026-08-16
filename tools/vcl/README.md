# Virtual Chemistry Lab PRO Spatial v0.3 — Target C

`release/` is what was handed over (sha256 `bd0e7596…`). `staging/` is built from
it by **eighteen** named exact-string transforms, each of which must match
exactly once or throw.

```sh
tools/vcl/run.sh          # build staging/, controls, assert-unchanged
tools/vcl/run.sh --drops  # also drop each transform and check a gate notices
```

## V0 — what was not touched, asserted rather than promised

The frozen set is checked mechanically, not by inspection: the pH model, the
deterministic mystery hash, the Cu/Fe²⁺/Fe³⁺/Al³⁺/Ca²⁺ hydroxide chain, the
carbonate effervescence, the sequencing teaching copy, the safety boundary, the
40-minute arc, **and each of the fourteen existing observation and warning
strings individually**.

That last one is worth the detail. The first cut of the assertion spanned those
strings as one region — which the V1 fix legitimately splits by inserting new
branches between them, so the span differed and the gate reported MOVED with
nothing frozen having been touched. Presence of each exact string, at the same
count, is the claim that actually matters.

Also confirmed unchanged: zero `localStorage`, zero `sessionStorage`, zero
external subresources, and the viewport — **which was already correct. Leave it.**

---

## V1 — the bench rewarded the procedure it teaches against. MERGE-BLOCKER.

`microResolve` rebuilt the well from an **order-independent ion pool** on every
drop, and the sequencing check was presence-only: `drop("reagent_hno3") > 0`.
Silver nitrate first, then nitric acid, gave a byte-identical clean positive to
doing it correctly, **with no warning at all**.

The left panel of that same bench teaches *"Halides: fresh portion → dilute
nitric acid → silver nitrate"*, and the bench's own question 3 asks why the
halide test must be acidified with nitric rather than hydrochloric acid. A pupil
could do it backwards, get the textbook-perfect precipitate, and be assessed on
reasoning the simulator had just told them did not matter.

**The model is untouched. Only the predicate changed** — `w.drops` was already an
ordered array, so the acidification index must precede the silver or barium
index. Every existing observation and warning string is reused verbatim; the one
new string is for the case that previously had no words at all.

| | correct order | reversed |
|---|---|---|
| chloride | white AgCl, no warning | **pale precipitate + warning** |
| bromide | cream AgBr, no warning | **pale precipitate + warning** |
| iodide | yellow AgI, no warning | **pale precipitate + warning** |
| sulfate | dense white BaSO₄, no warning | **white precipitate + warning** |

Release fails all four reversed cases. The new wording says why, in chemistry
rather than in scolding: *"Carbonate, sulfite and hydroxide precipitate with
silver as well, so an unacidified result cannot be read as a halide test."*

## V2 — the pupil's name was in the URL, and the label said it was not. MERGE-BLOCKER.

The field is captioned **"Name for print/export only"**. `syncHash()` base64url-
encoded the whole of `state`, `state.pupil` included, into `location.hash` on
every action, and **Share** copied `location.href`.

`pupil` is excluded from the serialiser, which makes the existing caption true —
the caption was not rewritten, the code was made to match it. `V2b` asserts the
name is *still* in print and in Export JSON, because the first cut of this fix
took it out of the export too.

**`notes` is kept, deliberately.** This app has zero `localStorage`, so the hash
is its only persistence: dropping the note would destroy a pupil's written
conclusion on reload. The captions are corrected instead — the Share help card
now says the link carries the note and **not** the name, and the note's own label
says it travels in the address bar and in a shared link. Both are asserted;
the removal matrix caught that nothing had been watching them.

## V3 — the state URL was over the common ceiling

Measured on release: **3,814 characters on a fresh load**, 8,093 after a
realistic 40-minute microscale session. 2,048 is still a real limit in link
handlers, previews and QR paths, so Share was least reliable exactly when there
was something worth sharing.

The state model is unchanged. Only what gets encoded:

1. **deltas from `initialState()`** — untouched benches cost nothing
2. a well's colour, ppt, pH, observation, warnings, pool and counts are **all
   derived from its drops**, so only the drops are stored
3. events lose a never-displayed timestamp and carry indices and keys rather
   than display names

| | release | staging |
|---|---|---|
| fresh load | 3,814 | **26** |
| each bench, untouched | 3,834–3,841 | 81–107 |
| realistic 40-minute session | 8,093 | **1,485** |

Shrinking an encoding is where links die, so two controls exist for that alone:
**V3-roundtrip** asserts a shared link restores the wells, the observations, the
event log, the note and the written answer — including **per-moment** event
observations, which a first cut quietly flattened to the well's final state —
and **V3-legacy** asserts a link minted by the *release* build still opens here.

## V4 — `.drop-pill` had no CSS rule at all

The class appeared exactly once in the file, in the template, with the pills
joined by `""`. Rendered as `1× FeCl₃ · 0.10 M1× NaOH · 0.40 M`. One rule, derived
from the existing `.var-tag` chip idiom. Measured gap at 390 px and 1440 px:
**0 px → 6 px**.

## V5 — answer marking was negation-blind. Option (a).

*"the glowing splint does not relight"* was marked **Correct: oxygen relights a
glowing splint.** Release marks **6 of 8** negated near-misses as correct.

The keyword items stop claiming a verdict at all. They show the model answer and
say which ideas the wording does and does not yet mention; the button reads
**Compare**, not Check. It cannot be wrong, which a keyword marker can always be.

The items that compare a **computed value** — the rate at 20 s, the concordant
titre, the concentration, the mystery identity — keep their verdict. Those are
arithmetic against state, not keyword presence, and downgrading them would lose
real marking.

The order named six regexes; this covers **eight**, because rates-0 and gastest-2
have the identical defect written a different way. That widening is deliberate.

## V6 — conformance

- **reduced motion**: `matchMedia` count was **0**. Ported from the shape v10
  uses — seeded from the OS, explicit user choice still wins.
- **accessible names**: predicate stated before counting. Under *aria-label /
  aria-labelledby / label[for] / wrapping label / title / button text, a
  placeholder NOT counted*, release has **17 unnamed across the five benches** —
  not 3. The 3 in the handover note is the count on the default bench under a
  looser predicate. All 17 are named; the gate walks every bench.
- **viewport**: already correct. Untouched, and asserted untouched.

### Not done in this pass

Splash, way home, `<noscript>`, `og:` and `canonical` are **not** here. They need
the house conventions derived from the live shelf, and — more to the point — the
way home and the `<noscript>` both depend on **V7**, the deployment route, which
is Matt's ruling. Landing a hand-written approximation of a generated control is
exactly what the estate's inline-exit ledger exists to prevent.

## V7 — awaiting a route

This does **not** go on the Games shelf. V1 and V2 are green, so the
merge-blockers are cleared, but the route and the surface that links to it are
Matt's call and nothing here creates either.
