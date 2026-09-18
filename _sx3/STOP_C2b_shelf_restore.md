# STOP-C2b — the Science shelf cannot be rebuilt at all, before the 51 are reached

ORDER SX3-MOVE Lane 1 asked whether `build_catalogue.py` rebuilds the shelf
without the 51 `SCIENCE_WEEK_BINDINGS` entries. Measured, not inferred. The
answer is **no**, and for a reason the order did not anticipate.

## Search scope

`tools/catalogue/SHELF_SELECTION.json` `science[]` (129 rows) ·
`assets/catalogue/science-shelf.json` `lessons[]` (129 rows, generated) ·
`tools/catalogue/SCIENCE_WEEK_BINDINGS.json` `entries` (129) ·
the 51 paths in `/tmp/shelf51.json` · all bytes read from the working tree at
`origin/main` (`3e2dcbd2`).

## What the shelf is

`assets/catalogue/science-shelf.json` is **generated**, not authored:
`build_catalogue.py` writes it from `SHELF_SELECTION.json`'s `science[]` list.
So "one PR, one file" is not available — the authored file is
`SHELF_SELECTION.json`, and a rebuild also rewrites `science-shelf.json`,
`terms-and-styles.json`, `TERM_AND_STYLE_EVIDENCE.json` and
`Science_Teesside/index.html`.

## Blocker 1 — the generator is already dead on main

`build_science_shelf.py` on the **unchanged** checked-in 129:

```
AssertionError: Review changed Science week binding:
  Science_Teesside/Build/SCI_B_W3_Backbones.html
```

Census of all 129 against their recorded `sourceSha256`:

| | count |
|---|---|
| sha256 matches the recorded binding | 74 |
| **sha256 has drifted** | **55** |
| missing binding or missing file | 0 |
| term conflict | 0 |

Drift by pathway: Build 10 · Grow 21 · Launch 24.

Re-proving those 55 against their own recorded evidence quote in the current
content: **36 still re-provable**, **1 not re-provable**
(`SCI_G_A2_W7B_Autumn_Science_Evidence_Do.html`, `Aut2·W7`), **18 carry no quote
or refs to re-prove with** (of which 2 have no week set at all:
`SCI_B_W8A_Sugar_Labels_Explore.html`, `SCI_B_W8B_Autumn_Science_Checkpoint_Do.html`).

Nothing in CI notices. `build_science_shelf.py` is byte-pinned in
`CATALOGUE_PINS` and named as a path trigger, but **no workflow executes it**.
`Science_Teesside/index.html` is a checked-in artefact that is in sync with the
JSON (both say 129) and that the generator can no longer reproduce.

## Blocker 2 — the 51, as expected

With the 51 added to `SHELF_SELECTION.json`, `build_catalogue.py` runs clean and
reports `Science shelf: 180 routes`. `build_science_shelf.py` then fails on the
**same** pre-existing drift, before reaching any of the 51. Their own defect —
zero week-binding entries — is the second blocker, not the first.

## A separate finding: `build_catalogue.py` is not reproducible either

A no-op rebuild at `origin/main` changes three tracked files:

- `science-shelf.json` — 6 rows flip `full-lundy` → `earlier` with different
  titles (the repeated-Lundy-panel count in those decks has dropped below 4
  since the catalogue was last built)
- `terms-and-styles.json` — the same 6, plus 2 added `.pptx` rows
- `TERM_AND_STYLE_EVIDENCE.json` — **125 entries change**; every `.pptx` row
  loses its `term`, `batch`, `sha256` and `title` (`classify()` returns early for
  non-`.html`). Those rows were written by a different tool, so the checked-in
  evidence file is a **merged** artefact and re-running `build_catalogue.py`
  alone destroys the pack rows.

The tree was restored after every measurement; nothing was left modified.

## Derived binding design for the 51 (spine-sourced)

Requested by the order. Scope: `TERM_AND_STYLE_EVIDENCE.json` entries for the 51,
cell references resolved against `_sownb/CALENDAR_SPINE.json` `workbookCells`.

**None of the 51 appear in the spine's `existingHtml` (0 of 51).** So the binding
cannot come from the census. It comes from the workbook cells instead:

| source | decks | instrument |
|---|---|---|
| `refs` resolving to spine `workbookCells` → `termWeek` | **43** | spine workbook cell — exactly as ruled |
| manifest `sow` declaration whose verbatim text opens with the term·week token (`Spr1·W3 — lesson A — …`) | **8** | manifest SoW string, **not** the spine |

The 8 are all GROW (`SCI_G_W18A`…`SCI_G_W24`). I am naming the instrument
difference rather than smoothing it: 43 are spine-sourced, 8 are declaration-sourced.

Result: **51 of 51 derive a week.** No term conflicts against the row's own
`term`/`terms`. `ruledAbsoluteWeek` follows the recorded offsets
(Aut1 +0, Aut2 +8, Spr1 +15, Spr2 +21, Sum1 +26, Sum2 +33).

Term breakdown of the derived rows: **Spr1 13 · Spr2 18 · Sum1 18 · Sum2 2** —
the breakdown the order stated. Pathway split is 17 BUILD · 17 GROW · 17 LAUNCH;
all 51 classify as `earlier`.

Two facts in that derivation need a ruling of their own:

1. **Three decks bind to `Spr2·W6`** — `SCI_B_S2_W6_The_Evidence_Museum.html`,
   `SCI_G_S2_W6_The_Spring_Science_Evidence_Exchange.html`,
   `SCI_L_S2_W6_Health_And_Plants_Evidence_Checkpoint.html` — and the spine's own
   `calendarNotes` says *"Spring2 has five timetabled weeks; workbook Spr2·W6 is
   not timetabled."* The workbook cell says W6; the ruled calendar says W6 does
   not exist. I have not chosen between them.
2. **One deck spans two Spr1 weeks** —
   `SCI_L_W18L2_Genetic_Engineering_Change_Test_Decide.html`. Existing entries do
   carry multi-week `weeks` arrays, so the shape is supported; flagging it so the
   13-rows/14-keys difference is not read as an error.

## What I did not do

I did not write a derived binding, did not touch `SHELF_SELECTION.json` beyond a
restored measurement, and did not attempt a shelf rebuild on a branch. Blocker 1
makes the 51 moot until it is ruled on: restoring the shelf to 180 requires the
129 to be buildable first, and 55 of them are not.
