## L51 — STOP-RESP-1 and STOP-RESP-2: two rulings, three standing records

Date: 2026-09-22. Ruled by Matt this turn; carried out in the order ruled.

### STOP-RESP-1 — option (c): admit by REVIEWED_PATHS, not ALLOWED_DIFF

`tools/easter/refresh_pack_checksums.py` is admitted through `REVIEWED_PATHS` in
`tools/catalogue/pin_catalogue_contract.py`, with its derived trigger pair materialised by
`tools/pin1/derive_triggers.py --write` — the route first used for #597. `ALLOWED_DIFF`
stays closed at 57 entries, identical before and after.

The distinction is the whole point and is worth stating plainly: **`REVIEWED_PATHS` pins a
file's digest; `ALLOWED_DIFF` exempts it.** Admitting here is a tightening, not a loosening.
`CATALOGUE_PINS.files` 1043 → 1044.

Measured after: `PIN1 PASS: 1051 asserted, 1058 exact triggers per event, 7 checker
dependencies`, and `[PASS] lessons cross-estate static contract` with the positive control
detecting 3 errors.

L49 gains the follow-up line: *"lands with the responsive pair via REVIEWED_PATHS"*.

### STANDING RECORD 1 — the pending-then-land fold

**Any pair whose diff intersects the served set lands in three steps, in this order.**
This is the shape already used for #581, now recorded as standing rather than ad hoc:

1. **Site window** admits the moving paths as `[main-today, pending]` transition pairs,
   with the four EQUAL pin lines **left at current main**. P5 must agree and no P2/P4 red
   may be introduced. Merge.
2. **The Lessons pair with the carrier bump folded in** — content *and*
   `builder_ref`/`uses:@` moved to the new Site SHA in one push. Apps companion first per
   L31. The publication then reads the new registry on its first run. Merge on green.
3. **A small re-pin window** moving the four EQUAL lines to the new Lessons main — the
   sixth-pin discharge pattern → pure carrier → publication.

Why the fold in step 2 rather than a separate carrier: the publication resolves
`.sources/Site` from `builder_ref`, so until that line moves it reads the **old** admission
record and refuses the moving paths by name. That is the failure recorded at run
35714663331. Folding the carrier into the content push is what keeps reds out of the
sequence entirely.

Cost: one extra small window. Benefit: reds nowhere. Correction #33 continues to hold — the
served-set intersection is run **before** the merge, not after.

Note on L38 ("a carrier that moves a published file is not a carrier"): step 2 is not a
carrier and is not claimed as one. It is a content push that carries its own closer. The
purity assertion there is **scoped to the carrier lines** — the workflow diff must be
exactly the two carrier lines, and the served paths that move must be exactly the set the
step-1 window admitted, verified as a set rather than a count. The whole-diff form of
`tools/hum/check_carrier_pure.py` refuses step 2 by design and is not the test. Step 3 is
the pure carrier, and there the whole-diff form applies unchanged.

**AMENDMENT (2026-09-25, Correction #41; Site #446 `cc28d5c5`; Claude's note on RS1-G4 §1).** Steps
1 and 3 above say "the four EQUAL pin lines". Since Site #446 the EQUAL set is **five lines in three
Site workflow files**: the declared-EQUAL Lessons pin in `domain-split-verify.yml`,
`education-publication.yml` and `published-completion-verify.yml`, and its Apps companion in
`domain-split-verify.yml` and `education-publication.yml`. Every EQUAL window (step 3) discharges all
five; step 1 leaves all five at current main. The text above stands as the record of the rule as it
was; the full correction, with the five lines as measured on Site `d9cdceef`, is
`_sx3/ROUTE_EQUAL_SET_2026-09-25.md`.

### STANDING RECORD 2 — pin before declaration

The declaration refuses on a stale catalogue pin. **The pin moves first, then the
declaration.** Recorded as the standing order.

### STANDING RECORD 3 — "180 cards" was wrong

The ledger's "180 cards" is corrected to **"180 rows / 184 cards"** wherever it appears.

### Container limit measured, not a pass

Egress to `mattroper1977.github.io:443` is denied by the agent proxy from 2026-09-22
14:17 UTC (`gateway answered 403 to CONNECT`, 3/3 attempts), having succeeded at 12:10 the
same day. The 390 px served proof on the 21 Summer 1 responsive pages is therefore **owed,
not done**, and is recorded as a limit rather than a pass. Publication SUCCESS remains
provable by run id.

The source-side substitute that *was* run, by DOM over the whole document rather than by
grep, on all 21:

```
parseable whole document (html+head+body)  21/21
meta viewport width=device-width           21/21
@media screen and (max-width: Npx)         21/21
breakpoints present                        ['600']px
FAILURES: none
```

`main` carries `@media print` only and no viewport meta, so the change is real and the
390 px viewport falls under the 600 px breakpoint on every page.

### Finding raised, not fixed

The three Summer 1 packs' `SHA256SUMS.txt` list 60 files they do not ship (28 BUILD,
16 GROW, 16 LAUNCH), all "open or read" failures — **zero checksum mismatches**. Membership
is byte-identical to `origin/main` for all three packs and the responsive branch changed
digest values only (7/7, 9/9, 8/8 — symmetric), so this is pre-existing, not a regression.
Raised for a ruling rather than fixed: either prune the absent entries or ship the missing
documents.

Separately, `tools/lessons_pin_lag_control.py` reports a P0 red on
`.github/workflows/serve-witness.yml:31` — a Lessons checkout with no `ref:`, no floating
declaration and no `rev-parse` recording its resolved commit. Pre-existing on main, newly
surfaced by the #429 ceiling removal, and **not** a CI gate: every reference to the lag
control in `.github/workflows/` is inside a comment, with no `run:` invocation. Raised for
a ruling; no check is edited without one.

---

## STANDING RECORD 4 — the carrier points at the SHA that admits EVERYTHING, and it moves last

Added to the fold rule after STOP-RESP-3 and STOP-RESP-4, both found by measurement rather
than reasoning:

> **A carrier must point at the Site SHA that admits EVERY mover in the pair, derived
> artefacts included. The carrier bump is therefore the LAST edit on the Lessons branch,
> made only after every window it depends on has merged.**

Why it had to be said. The Summer 1 fold put the carrier at `aeb47509` — the window that
admitted the 27 *content* movers. Regenerating the size table then produced a 28th,
`data/resource-sizes.json`, which is itself served and which `aeb47509` does not admit. The
publication resolves `.sources/Site` from `builder_ref`, so #647's own publication would
have read `aeb47509` and refused that path by name. Step 3 could not have repaired it: by
then step 2's publication has already run.

Two consequences follow, and both cost real PRs:

1. **A carrier drags the gate copy, and therefore an Apps companion.**
   `education-pages.yml`'s digest is pinned in `PUBLICATION_CALLER_SHA256_BY_KIND["lessons"]`,
   which lives in the gate copy that must stay byte-identical across Lessons and Apps. So
   every carrier bump forces a gate re-pin in *both* repos. The new digest cannot exist
   before the Site SHA does, so the companion for a carrier-bearing fold must be cut **after**
   the Site merge — a single companion opened up front cannot carry it. That is why Apps #168
   exists beside #167.

2. **Re-bumping a carrier repeats the whole cost.** Pointing #647 at S2 changes
   `education-pages.yml` again, moves its digest again, and needs another Apps companion.
   Hence: bump once, last, at a SHA that already admits everything.

The rule collapses both into one ordering: derive everything, window everything, merge the
windows, and only then bump the carrier.

---

## THE SUMMER 1 RESPONSIVE FOLD — what it cost, and why

Ruled as a three-step pending-then-land fold. It took **six PRs plus a re-bump**, and both
overruns came from the same habit: reasoning about what a change touches instead of
measuring it. Both were caught by gates before reaching main. Nothing went red on any main.

| # | PR | head | what it was |
|---|---|---|---|
| 1 | Site #430 | `aeb47509` | the 27 content movers, `[main-today, pending]` |
| 2 | Apps #167 | `5929f4af` | gate copy: responsive re-pin + STOP-RESP-1 |
| 3 | Apps #168 | `d7fc8b8c` | gate copy: the caller pin the carrier dragged |
| 4 | Site #431 | `0f931086` | **the derived 28th mover** |
| 5 | Apps #169 | `86933c99` | gate copy: the caller pin the RE-bump dragged |
| 6 | Lessons #647 | `b5b87361` | content + carrier, at the SHA admitting everything |
| 7 | Site #432 | open | EQUAL discharge + the clock raise |

### Overrun 1 — the window was cut from the content diff

`data/resource-sizes.json` is served, and regenerating it is *forced* by the content change,
yet it appears nowhere in the content diff. The pre-push battery caught it:

```
[FAIL] data/resource-sizes.json differs from the working tree
```

and building against #430's record then named exactly one path:

```
ValueError: Education file admission blocked publication:
CHANGED education-lessons/data/resource-sizes.json
```

Cost: Site #431.

### Overrun 2 — the carrier pointed at a SHA that did not admit everything

`education-pages.yml`'s digest is pinned inside the gate copy that must stay byte-identical
across Lessons and Apps, so **every** carrier bump drags an Apps companion — and the digest
cannot exist before the Site SHA does, so the companion must be cut *after* the Site merge.
Doing it twice cost Apps #168 and #169.

### The proof the second fix worked is in the run's own metadata

Publication `35750993659`, on Lessons main `b5b87361`:

```
referenced_workflows:
  .../education-publication.yml@0f93108616d196cc5869380ce390a6c8c34a8812
```

It resolved the Site workflow at `0f931086`, not the older `aeb47509` — i.e. at the record
that admits the derived mover. That is the run saying so, not me.

### The discharge

```
P4 domain-split-verify.yml:118   b5b873616790: 0 commits behind, 0 paths changed, 0 published  EQUAL holds
P4 education-publication.yml:101 b5b873616790: 0 commits behind, 0 paths changed, 0 published  EQUAL holds
P5 EQUAL-declared pins agree: b5b873616790
```

Zero behind is the point: held at `4f19ac9e` through the fold while the windows admitted both
byte-states, then moved onto the head carrying the delivered bytes.

### Owed, not done

The **390 px served proof** on the 21 pages. Container egress to the served host is denied
(403 on CONNECT, 3/3 attempts), where it succeeded at 12:10 the same day. Recorded as a
container limit, **not** a pass. The source-side substitute that *was* run, by DOM over the
whole document on all 21 pages:

```
parseable whole document (html+head+body)  21/21
meta viewport width=device-width           21/21
@media screen and (max-width: 600px)       21/21
```

`main` carries `@media print` only and no viewport meta at all.
