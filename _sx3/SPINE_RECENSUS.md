# Spine re-census — repairing main's catalogue re-derivation

Ruling R2: *census, not re-author.* `_sownb/CALENDAR_SPINE.json`'s `blobSha256` is a
derived record that was never re-censused after the release. This re-records 14
entries with a purpose-built census tool and proves the ruled outcome.

## The defect this repairs

`origin/main` at `cbfbc70c` **cannot regenerate its own catalogue record.**

- `build_lesson_order.py --check` PASSES on pristine main — the committed records are
  mutually consistent, so nothing looks wrong.
- Run `build_catalogue.py` first, then `build_lesson_order.py`, and it **asserts** on
  `SCI_L_W10L1_Growth_And_Differentiation_Introduce.html`.

`build_catalogue.py` re-proves a deck's workbook binding like this:

```python
unchanged = sha256(file) == EXISTING[path]['blobSha256']
...
if unchanged or outcomes or cell_labels or reviewed_solar_equivalence or audited_current_binding:
    terms = [the ruled term of the cells in contentCellReferences]
```

For the 14 LAUNCH W9–W13 decks **no limb can fire**:

| limb | state |
|---|---|
| `unchanged` | **no** — the spine pins the **pre-transplant** bytes (`SCI_L_W10L1`: `503c0cdd…`, current `612b4544…`) |
| `outcomes` | **no** — the transplant re-worded the deck, so the verbatim outcome is no longer in the body |
| that outcome long enough to count | **no** — `'Explain growth & stem cells.'` is exactly 28 characters against a `len(...) > 28` guard, so a byte-perfect match would still be rejected (ledger L28; the guard is NOT changed here) |
| `cell_labels` | no |
| `audited_current_binding` | **no** — `secondInstrumentEvidence` is `{}` for these entries |

So the term fell to `unspecified` and `build_lesson_order.py` asserted. The committed
record still read `Aut2` only because it had not been regenerated since the bytes moved.

**The spine is stale far beyond these 14: 254 of 529 `existingHtml` entries** carry a
`blobSha256` that is not their current bytes, across Art, ASDAN, Careers, Community,
Duke, FoodWise, Life Skills, DT, Humanities, Science and Lundy. Per R2 only the 14 are
re-recorded here. The other 240 are carried open — they break nothing today, and
widening this PR would be re-authoring by another name.

## The tool

`_sownb/vb/tools/recensus_existing_html.py`. It records what the bytes ARE:

- writes **only** `blobSha256`, and only on entries **named on the command line** —
  never a scan, never "all stale";
- every digest **derived** from the file's bytes, never transcribed (correction #6);
- asserts every other top-level key byte-equal afterwards — `calendar`, `termBlocks`,
  `termDates`, `ruledMapping`, `boundary`, `februaryBoundary`, `workbookCells`,
  `targets` and the rest — and every other field of every `existingHtml` entry,
  including `contentCellReferences` and `secondInstrumentEvidence`;
- **surgical**: the spine was written by a formatter that puts some nested objects on
  one line, so `json.dumps` cannot reproduce it and a re-serialise would rewrite all
  60,437 lines. The tool replaces the 64 hex characters in place, then **parses the
  result and compares the whole structure**, so the minimal diff is a proved one.

It does **not** resurrect `census_spine.py`, retired by VB-RUN13 R0 for deriving a
teaching week from a filename. No week is derived here at all — the paths are given
and the digests come from bytes — so `g27_no_filename_weeks.py` has nothing to flag.

Self-test: **15/15**, including a planted `termDates` change, a planted `spineStatus`
change, a planted digest that is not the digest of the bytes, a planted `workbookCells`
row, a duplicated path, a path present only outside `existingHtml`, and a path missing
on disk — each refused.

## The proof the ruling asks for

| requirement | result |
|---|---|
| spine diff | **14 insertions, 14 deletions, every one a `blobSha256`** |
| regenerate the catalogue → decks losing term | **0** |
| `build_lesson_order.py --check` | **PASS** — 1080 entries, 274 week-bound, 136 version links |
| `pin_catalogue_contract` | **PASS** after the re-pin |
| four-writer sweep | **SWEEP PASS**, all four in step |

**Isolated effect, proved by running `build_catalogue.py` on a clean `origin/main`
worktree and on this branch and diffing the two writer outputs: exactly 14 entries,
each `term unspecified → Aut2`, each by the method `unchanged source census with
resolved workbook cells`, proof `unchanged bytes`. Nothing else.**

The other refreshes in `TERM_AND_STYLE_EVIDENCE.json` — 31 entries `style`
`full-lundy → earlier`, 32 `title`, the `batch` relabels — are **identical on clean
main**, i.e. pre-existing drift its own writer corrects either way, not something this
change caused.

## Carried, not done here

- **The 240 other stale entries.** Named above; nothing depends on them today.
- **The `> 28` guard** (ledger L28) is untouched, per R2, and recorded for the
  evidence-model order.
- **`tools/catalogue/STATIC_CHECK_RESULTS.json`** moves on every catalogue change and
  is read by no gate. Ledger L24 defers whether it joins the sweep or leaves tracking;
  that deferral stands, so it is restored rather than committed, as the carrier did.
- **Sequencing.** All 14 of these decks are inside the 20 that SX3-FU1 splits. A deck
  whose bytes change goes stale again by construction, so the F3 PRs must re-census the
  decks they touch, at their post-split bytes, in the same PR — exactly as the four
  derived-record writers are run. This PR repairs main so that it can.
