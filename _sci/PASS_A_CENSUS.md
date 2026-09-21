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
---

# PASS A3/A4 — the 51 Spring and Summer routes, and the rebuild
ORDER SCI-COMPLETE · Lessons main `3887f7ac` merged in, branch `claude/sci-shelf-restore`

## A3 — selected and bound, every value derived

`tools/sci/select_manifest_decks.py` (self-test PASS, 7 red proofs) reads the six pathway
folder manifests and selects a route only when the manifest row names a file in the tree and
every workbook cell it cites resolves in `_sownb/CALENDAR_SPINE.json`. The evidence recorded
beside the route is the shape `build_catalogue.py` itself emits, so selection and rebuilt
evidence agree. Nothing is read from a folder or file name.

| route evidence | count |
|---|---:|
| manifest row with every cell resolved in the spine | **43** |
| manifest row sow token, the builder's own fallback: the row cites a second, B-column cell the spine never held, named beside the token | **8** |
| selection | **129 → 180** |

`tools/sci/bind_manifest_decks.py` (self-test PASS, 10 red proofs) binds each selected route:
term and week from the spine cell (or, for the 8, from the row's own token, which every
resolving cell must corroborate); the ruled absolute week from the record's own calendar note
(*Aut1 +0, Aut2 +8, Spr1 +15, Spr2 +21, Sum1 +26, Sum2 +33*), cross-checked against the
manifest's `absoluteWeek` and refused on disagreement. Bindings **129 → 180**.

| term | routes |
|---|---:|
| Spr1 | 13 |
| Spr2 | 18 |
| Sum1 | 18 |
| Sum2 | 2 |

**Listed, not hidden:**

| deck | why it is listed |
|---|---|
| `SCI_B_S2_W6_The_Evidence_Museum` | workbook week `Spr2·W6`; the record's note: *Spring2 has five timetabled weeks; workbook Spr2·W6 is not timetabled*. Bound to term and week, marked `timetabled: false`, no absolute week. |
| `SCI_G_S2_W6_The_Spring_Science_Evidence_Exchange` | as above |
| `SCI_L_S2_W6_Health_And_Plants_Evidence_Checkpoint` | as above |
| `SCI_L_W18L2_Genetic_Engineering_Change_Test_Decide` | two cells, `Spr1·W3` and `Spr1·W4`; both kept; the record holds no two-week precedent |
| `SCI_G_W18A`, `W18B`, `W19`, `W20`, `W21`, `W22`, `W23`, `W24` | bound by the manifest sow token; the unresolved `'GROW Weekly - Spring'!B30…B36` cells are named in the entry |

**§Q4.** `tools/catalogue/TERM_BASES.json` is created here with the science bases read from the
bindings record's own note. HUM-T writes its `humanities` bases into the same record.

## A4 — the builders run clean

`build_catalogue.py` (merge guard: 118 rows preserved, 0 dropped), `build_science_shelf.py`
(**180 lesson links, 3 pathways**), `build_lesson_order.py`, `build_display_titles.py`
(236 guarded entries, PASS) and the static check all run; `check_catalogue_static.py`'s shelf
count is re-pinned 129 → 180 with `Spr2`, `Sum1`, `Sum2` admitted to its term list. The pinned
`assets/catalogue/shelf-base.css` is asserted by the writer (A2).

**No term moved on rebuild:** 0 of 1080 entries changed term or terms.

Two things did move, and they go to STOP-SIGN-A rather than shipping quietly:

| finding | count | root cause |
|---|---:|---|
| style re-derived `full-lundy → earlier` | **31** | The decks' current bytes carry **no** Lundy furniture (`lundy` 0, `lundy-grid` 0, `lundy-loop` 0, `data-lundy-status` 0, measured per deck). The record said `full-lundy` with 9–10 repeated panels because an earlier evidence re-stamp moved the digest without re-deriving the classification. The builder now reads the bytes as they are. Their proper class is a chassis question for PASS B; `earlier` is what the builder's current rules yield. |
| composite title re-derived from the deck's own `<title>` | **32** | 5 are genuinely stale (the lesson title in the composite no longer matches the deck: `SCI_B_W8B`, `SCI_L_A2_W7L3`, `SCI_L_W13L2`, `SCI_L_W9L2`, `SCI_L_W9L3`); 27 differ only in the lane/week/duration wrapper (`LAUNCH GCSE Biology W10L1 · … · 40 minutes` → `LAUNCH Science · …`). The display-title guard passes on all 236 entries. |

The six BUILD Humanities decks that landed in HUM-T batch 1 also re-derive their
*current presentation structure* evidence (their new loop panels are now counted); term,
style and title are unchanged.
