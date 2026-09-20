# PASS A1/A2 — the joined census and the re-proof
ORDER SCI-COMPLETE · Lessons main `96452dad`, branch `claude/sci-shelf-restore`

## The two censuses are one census at two commits

`_sx3/STOP_C2b_shelf_restore.md` measured **55 drifted** at `3e2dcbd2` and split them
36 / 1 / 18. `_sx3/STOP_C2b_55_buckets.md` re-measured the same 55 with a label
instrument and corrected the split to 35 / 1 / 1 / 16 / 2. Neither is a *shelf*
census: both count `SCIENCE_WEEK_BINDINGS.json` rows whose bytes moved. Measured
again at `96452dad` the same way, the drift has grown from 55 to **77**, which is
the order's figure. `lesson-order.json`'s science pins are a different record and
are **not** drifted: 281 fresh, 23 unpinned, 0 drift.

## A1 — the 77, by what re-proves them

| limb | what it means | count |
|---|---|---|
| 1 quote verbatim | the recorded evidence sentence is still present, word for word | **35** |
| 1b token form | the quote broke but the deck still writes `Aut2·W7` | **7** |
| 2 label form | the deck writes `Autumn 2 · Week 7` instead of the token | **6** |
| 3 nothing re-proves | the deck restates no binding at all | **27** |
| 4 no week recorded | the binding itself records no week | **2** |

**48 re-provable · 29 identity-only** — exactly the split the order names.
By pathway: BUILD 11 · GROW 25 · LAUNCH 41.

## A2 — what was written

The 48 are re-stamped with the limb that re-proved them recorded per row. The 29
are identity-pinned with the basis written down as *identity only; the deck restates
no binding; term from the deck's own lesson-config* — a weaker claim, recorded as one,
so nothing passes as re-proved that was not.

**Every one of the 29 is an `Aut2` binding or has no week at all.** That is the
evidence-model defect at its sharpest: the record asserts a fact the artefact never
restates, so only the byte hash held it, and the bytes had already moved.

### Accepting three forms is not a loosening

The estate writes a binding three ways and the estate's own readers
(`term_codes`, `weeks_from`) already accept token **or** label. Only the quote limb
ever demanded one form. The re-proof tool accepts all three and still refuses a deck
that states nothing, or states the wrong week — both are red-proved.

## The writer runs

`build_science_shelf.py` has not been able to run since the 2026-09-06 audit. It runs
now: *Built static Science shelf with 129 lesson links and 3 pathways.* That clears the
STOP-X carried by tasks #36 and #46.

### and it had the HUB-1 stylesheet fault, as predicted

The first successful run produced a hub with a **651-byte** stylesheet where the served
hub carries **18,657** — the root-page scrape ORDER HUB-1 found and recorded as a
fragile dependency for this order. The writer now reads the pinned
`assets/catalogue/shelf-base.css`, which **contains the served science block verbatim**
(the only difference is a 361-byte provenance comment; zero CSS rules differ), and
asserts it is the house block rather than trusting a regex against a page.