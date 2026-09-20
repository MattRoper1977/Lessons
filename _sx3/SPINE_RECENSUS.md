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

---

## STOP — the boundary has no route for this record

CI on the first head found two reds. One was mine to fix; the other is a gate
question I will not answer on my own.

### Fixed: a seventh derived record, and why it only surfaces now

`Catalogue schema, tags and contract` failed on
`build_display_titles.py --check` — *"Display-title map is stale"*.

`assets/catalogue/display-titles.json` derives from `lesson-order.json`'s
`supplements`. On clean main that record **cannot go stale**, because
`build_lesson_order.py` asserts before it ever writes — so the chain stops and
nothing downstream moves. Repairing the assert lets the chain run to the end for
the first time, and the next record in it is then one regeneration behind.
Regenerated with its own writer: 236 entries, 118 companion pairs, only
`originalTitle` moves on 28 of them, and the writer's own guard
(`if title not in host['title']: raise`) did not fire, so every reviewed pair still
holds. `check_display_titles.cjs` PASS; `check_catalogue_schema.py` self-test 8/8
and 956 rows valid.

### STOPPED: `_sownb/CALENDAR_SPINE.json` is not admitted through the boundary

`static-contract` failed with

```
[FAIL] standalone/offline boundary violated by changed files: ['_sownb/CALENDAR_SPINE.json']
```

Reproduced locally against `origin/main`. Of the six modified files, five are
admitted through `CATALOGUE_PINS.files` and one is not admitted at all:

| modified file | admitted by |
|---|---|
| `assets/catalogue/lesson-order.json` | `CATALOGUE_PINS.files` |
| `assets/catalogue/science-shelf.json` | `CATALOGUE_PINS.files` |
| `assets/catalogue/terms-and-styles.json` | `CATALOGUE_PINS.files` |
| `tools/catalogue/TERM_AND_STYLE_EVIDENCE.json` | `CATALOGUE_PINS.files` |
| `tools/verify_cross_estate_unification.py` | `ALLOWED_DIFF` |
| **`_sownb/CALENDAR_SPINE.json`** | **nothing** |

`build_catalogue.py` line 37 reads this exact file, so R2 cannot be carried out
without modifying it. There is no transaction route: `fence_errors` is a deny list
of fenced decks, not an admission. The gate's own error names the remedy —
"the estate admits a deck by naming it in `CATALOGUE_PINS`".

Two routes exist, both touching gate machinery. **Measured, then reverted:**

| route | cost | effect |
|---|---|---|
| **(a)** add to `ALLOWED_DIFF` | 1 line in `tools/verify_cross_estate_unification.py` | **loosens** — the file may then change freely, pinned by nothing |
| **(b)** add to `REVIEWED_PATHS` | 1 line in `tools/catalogue/pin_catalogue_contract.py`, the re-pin in both gate copies, **+2 machine-derived trigger lines** in `.github/workflows/mbm-cross-estate-unification.yml` | **tightens** — the record carries a reviewed digest, and the gate starts firing when it changes |

Route (b) is the better one on the merits. The workflow edit is two additive lines
in a `paths:` watch list, one under `pull_request` and one under `push`, written by
`tools/pin1/derive_triggers.py --write` and never by hand; PIN1 asserts the two sets
are equal in both directions, so the admission **forces** it rather than choosing it.
It adds coverage and removes none.

It is still a CI edit, and the standing limits are "nothing loosened; no CI edit
except carrier pin moves under precedence, named". **So neither route is taken here.**

Worth saying plainly: the spine is not watched by that workflow today, and it
carries no reviewed digest. That is very likely *why* 254 of 529 entries drifted
without anything going red. Route (b) closes that hole as a side effect.

**Ruling needed:** route (a), route (b), or a third the estate prefers. Until then
this PR stays red on `static-contract` by design — the work is proved and staged,
and the last step is an admission that is not mine to grant.

---

# Narrowed: this PR ships the re-census only

CI found a fourth latency of the same family, and it decides the shape of this PR.

## A fourth record the repair unblocks — and this one has no runnable writer

`Hub and subject page in Chromium at 390px` failed on `check_catalogue_dom.cjs`:

```
AssertionError: //full-lundy
85 !== 54
```

The Science shelf filter compares the cards rendered from `Science_Teesside/index.html`
against `assets/catalogue/science-shelf.json`. Regenerating the catalogue moves **31
entries from `style: full-lundy` to `style: earlier`** (with the matching `batch`
relabel), so the JSON says 54 where the committed page still renders 85.

Those 31 are **not** caused by the re-census — proved earlier by diffing the writer's
output on clean main against this branch, which differs on 14 entries, term only. They
are pre-existing drift, and on clean main they never land because `build_lesson_order.py`
asserts first and the chain stops. Repairing the assert lets them through.

`display-titles.json` had a writer, so it was regenerated. This one's writer,
`tools/catalogue/build_science_shelf.py`, rewrites the whole of
`Science_Teesside/index.html` — a **served page under a GLV3 `PROTECTED` prefix**.
Bringing that into a spine-census PR would be a much larger change than the ruling
asks for, and it is not what R2 repairs.

`UX2 scheduled drift census` was red for the same reason and is not independent:
`needs: [catalogue-contract, derived-data, hub-and-subject]` with `if: always()`, so it
reports those jobs' outcomes. `catalogue-contract` is green on the current head.

## So the PR now carries the repair and nothing else

Reverted: `TERM_AND_STYLE_EVIDENCE.json`, `lesson-order.json`, `science-shelf.json`,
`terms-and-styles.json`, `display-titles.json` and both gate copies. Kept: the
re-censused spine, the tool, and this record.

The repair is unaffected. The regeneration was R2's **proof**, not its payload — the
committed records already read `Aut2` for those 14, and after this PR the next
regeneration keeps them instead of dropping them. Measured on this shape:

| check | result |
|---|---|
| four-writer sweep | **SWEEP PASS**, all four in step |
| `check_catalogue_dom.cjs` | **PASS**, 28 checks |
| `build_lesson_order.py --check` | **PASS** — 1080 entries, 274 week-bound |
| `build_display_titles.py --check` | **PASS** — 236 entries, 118 pairs |
| `hub_gates.mjs --red-proof` | **PASS — 303/303 limbs** |
| gate copies | byte-identical at `f38a2a6f91cc5c83`, equal to main |

The Apps companion has nothing left to carry and is closed.

## Carried out of this PR, named

**The catalogue cannot be regenerated on main without breaking two records.** Its own
writer moves 31 entries `full-lundy → earlier`, which `Science_Teesside/index.html`
does not reflect, and the only writer for that page rewrites a served GLV3-protected
file. That is a second ruling, separate from the spine: either the reclassification is
correct and the shelf page must be rebuilt and re-admitted, or the classifier has
drifted and should be brought back. Four latencies now sit behind the same assert —
the 14 terms (repaired here), `display-titles.json`, `Science_Teesside/index.html`, and
the UX2 census that reports on them.

---

# The boundary red did not go away — the gate stopped running

Narrowing the PR to three files made `static-contract` disappear from the checks.
That is **not** a resolution, and it must not be read as one.

| head | files changed | `static-contract` |
|---|---|---|
| `3da013e4` (wide) | 6, incl. catalogue records | **RAN and FAILED** — `standalone/offline boundary violated by changed files: ['_sownb/CALENDAR_SPINE.json']` |
| `374da075` (narrow) | 3: the spine, the tool, this record | **DID NOT RUN** |

The check lives in `.github/workflows/mbm-cross-estate-unification.yml`, whose
`paths:` filter is the PIN1-derived list. Measured:

```
$ grep -rn "_sownb/CALENDAR_SPINE.json" .github/workflows/*.yml
(no output)
```

**No workflow watches this file.** The only `_sownb` strings in any workflow are `run:`
steps, not path filters. The wide head fired the gate because it also touched
`assets/catalogue/*` and `tools/catalogue/*`, which are watched. Take those away and
the boundary check has nothing to trigger on.

So on this head the gate is not passing — it is absent. Green here means **not
judged**, not judged and cleared.

This is the same failure class the estate keeps cataloguing. `_sx3/RELEASE_LEDGER.md`
on the GLV3 fence: *"It had been rejecting every landing deck on every branch the whole
time."* And the same shape again in the Humanities `Teaching_Packs` finding: the 245
files there were never admitted, their commits simply never fired the fence.

It is also the second, independent argument for **route (b)**. Admitting the spine
through `REVIEWED_PATHS` makes `tools/pin1/derive_triggers.py --write` add
`- '_sownb/CALENDAR_SPINE.json'` to both PIN1 blocks — which is precisely the two lines
measured earlier. After that the gate would actually fire on a spine change, instead of
being silent on it. Route (a) (`ALLOWED_DIFF`) would admit the file and leave it
unwatched and unpinned, i.e. exactly the state that let 254 of 529 entries drift with
nothing going red.

**Nothing here is a reason to merge on the strength of a green.** The change is sound
on its own evidence — 14 digests derived from bytes, 0 terms lost,
`build_lesson_order --check` PASS, sweep PASS, DOM 28/28, hub gates 303/303 — but the
one gate that exists to judge whether this file may change at all has not looked at it.

---

# Admitted by pin — route (b), per ruling §1

`_sownb/CALENDAR_SPINE.json` is now in `REVIEWED_PATHS`, with the rationale in the
file naming this order. `ALLOWED_DIFF` was refused: it would admit the file and leave
it unwatched, which is the state that let 254 of 529 entries drift.

**Both consequences are machine-written, never by hand:**

- `pin_catalogue_contract.py --write` re-cut both gate copies from the rows it had
  just verified — byte-identical at `1796ab50ace3eb6a`.
- `derive_triggers.py --write` materialised the matching PIN1 trigger path. The
  workflow diff is **exactly two additive lines**, one per event:

```
+      - '_sownb/CALENDAR_SPINE.json'
+      - '_sownb/CALENDAR_SPINE.json'
```

PIN1 goes 557 → **558 exact triggers per event**, 551 asserted, 7 checker dependencies.
This is the #581 precedent: generated from the pins, never typed.

## What this buys, measured

Running the gate's own `boundary_errors()` over this branch's changed set:

| before | after |
|---|---|
| `standalone/offline boundary violated by changed files: ['_sownb/CALENDAR_SPINE.json']` | **NONE — admitted** |

And the gate will now **fire** on a spine change rather than being silent on it, which
is the half that matters: the previous green was a non-run.

| check | result |
|---|---|
| four-writer sweep | **SWEEP PASS** |
| `pin_catalogue_contract --check` | **PASS** |
| `derive_triggers --check` | **PASS** — 558 triggers per event |
| `build_lesson_order --check` | **PASS** — 1080 entries, 274 week-bound |
| `build_display_titles --check` | **PASS** — 236 entries, 118 pairs |
| `check_catalogue_dom.cjs` | **PASS**, 28 checks |
| gate copies | byte-identical, both repos |

`STATIC_CHECK_RESULTS.json` and `DOM_CHECK_RESULTS.json` drift on every run and are
read by no gate; ledger L24's deferral stands, so both are restored rather than
committed.

Per the ruling, this does not merge on the strength of a green: `static-contract` must
be **observed running** on the new head, with its run id recorded, and passing.
