# §4 — the 31 `full-lundy → earlier` decks: the classifier has NOT drifted

Ruling §4 asked for a measurement before any rebuild: the classifier's basis, and
whether the **served bytes** carry it. Measured on all 31, not three.

## The classifier's basis

`tools/catalogue/build_catalogue.py`:

```python
loops = doc.xpath('//*[contains(concat(" ",normalize-space(@class)," ")," lundy-grid ")
                    or contains(concat(" ",normalize-space(@class)," ")," lundy-loop ")]')
...
elif len(loops) >= 4:
    result['style'] = 'full-lundy'; result['batch'] = 'Full Lundy Loop · repeated prompts'
```

Four or more elements carrying `lundy-grid` or `lundy-loop`. The evidence row records
the count it saw, as `repeatedLundyPanels`.

## The measurement

SCOPE: all 31 decks whose style moves `full-lundy → earlier`. Committed record =
`origin/main`'s `TERM_AND_STYLE_EVIDENCE.json`; writer output = `build_catalogue.py`
run on a clean `origin/main` worktree; served bytes = the files as they stand on main.

| | recorded `repeatedLundyPanels` | writer now | **served bytes, counted directly** |
|---|---:|---:|---:|
| 23 LAUNCH + GROW + BUILD decks | **10** | 0 | **0** |
| 8 (A2 W7 ×3, W14 ×3, and 2 more) | **9** | 0 | **0** |
| **all 31** | 9 or 10 | **0** | **0** |

Unanimous. Every one of the 31 was recorded with 9 or 10 Lundy panels and **now
carries none at all**. The threshold is 4.

## Verdict

**The classifier has not drifted. The files did.** `build_catalogue.py` reads the
markers correctly; the SX3 transplant removed them, so `earlier` is the true class of
these 31 decks today, and the committed `full-lundy` is the stale value. This is the
expectation §4 set out ("Held A: 0 vs 98"), confirmed on the whole population rather
than a sample.

No STOP-X. The rebuild path in §4 applies:

1. rebuild `Science_Teesside/index.html` with `tools/catalogue/build_science_shelf.py`;
2. admit via `SHELVES` — it is already `Science_Teesside/index.html` there, and pinned;
3. a Site transition pair for its published digest, in the same window.

## Ledger line

The SX3 release changed 31 decks' style class from `full-lundy` to `earlier` by
removing their Lundy panels. That is a real change to what those decks are, not a
record error. The authoring order's **Held A lane (Lundy restoration)** moves them
back; when it does, the same writer will return them to `full-lundy` on its own, and
the shelf page must be rebuilt again in that window.

Until the shelf page is rebuilt, `check_catalogue_dom.cjs` reds on any branch that
regenerates the catalogue — `//full-lundy 85 !== 54` — because the page still renders
the old class. That is the fourth latency behind the `build_lesson_order.py` assert.

## STOP-X — the shelf writer is gated on an audit that 77 of its 129 sources have invalidated

ORDER FINISH-2 §4 ruled: *rebuild `Science_Teesside/index.html` with its writer*.
Measured on `origin/main` `6bb8238f`, on a clean branch with no deck change of
mine, the writer refuses:

```
build_science_shelf.py: AssertionError: Review changed Science week binding:
  Science_Teesside/Build/SCI_B_W3_Backbones.html
```

`week_binding()` asserts every shelf row's current bytes equal the `sourceSha256`
recorded in `tools/catalogue/SCIENCE_WEEK_BINDINGS.json`. That record is not a
byte census. It declares itself: `schema: science-week-audit-v1`,
`auditedAt: 2026-09-06T11:48:28Z`, scope *"Read-only audit … checked against
accepted source hashes"*, rule *"Calendar binding uses explicit current
content/manifest/SoW evidence. No week inferred from filename or folder."*
Re-stamping its digest would claim that audit was repeated. It was not.

### Census — scope: all 129 `entries`, working-tree bytes at `6bb8238f`, tags/script/style stripped

| | count |
|---|---|
| `sourceSha256` matches the tree | 52 |
| **stale** | **77** (Build 11 · Grow 25 · Launch 41) |
| missing binding or file | 0 |

STOP-C2b measured 55 on `3e2dcbd2`; the 22 since are the SX3 landings. The 77,
bucketed by what in the **current** artefact still re-proves the recorded week
(the same five buckets as `_sx3/STOP_C2b_55_buckets.md`):

| bucket | what re-proves the binding | count |
|---|---|---|
| A | the audit's own evidence quote, verbatim (first 80 alphanumerics) | 35 |
| B | the binding in token form (`Aut2·W4`) | 7 |
| C | the binding in label form (`Autumn 2 · Week 4`) | 6 |
| D | **nothing** — the deck does not restate its week | **27** |
| E | the record itself holds no week (`status: unset`, W8A / W8B) | 2 |

Bucket D was re-measured through `<script id="lesson-config">` (the workbook
route `admit_landing_decks.py` carries): its `week` is the filename week
(`W13` → `13`) and disagrees with `ruledAbsoluteWeek` (`14`) on 15 of 29 — exactly
the "obsolete absoluteWeek" the audit's own rule outranks. It is not evidence.

Cross-check that nothing has *moved*: for 75 of the 77 the recorded term equals
the term `build_catalogue.py` derives from current bytes; the other 2 are bucket E
(no term recorded). Zero disagreements.

### Why this is STOP-X and not a re-stamp

- **48** (A+B+C) could be re-cut on the CX3 precedent (`tools/cx3_recut.py`: single
  writer, `sourceSha256` + a `reviewed: {date, reason}` note, calendar binding
  unchanged) — the artefact itself restates the week.
- **29** (D+E) cannot: STOP-C2b named it — *"the record asserts a fact the artefact
  does not restate, so the only thing holding the binding is the byte hash — and
  the bytes have already moved."* Re-cutting them writes a digest over an
  unprovable claim.
- The writer needs all 129. There is no partial rebuild, and loosening the assert
  is refused by the LIMITS.

STOP-C2b assigned the repair to *"the shelf-restore order (§5d)"*. No such order
exists in `docs/orders/` or `_sx3/`. That is the absent ruling.

### What §4 needs from Matt (one decision, three forms)

1. **Re-cut the 48 on the CX3 precedent and re-audit the 29** by the record's own
   rule (workbook cell / manifest row named per deck) — an audit, its own order.
2. **Re-cut all 77 as a census** with a `reviewed.reason` that says so — the
   record's `rule` line then no longer describes it, and it must be re-titled.
3. **Leave the shelf as served** (54 full-lundy cards as on main) and carry §4 to
   the evidence-model order with this table as its input.

### F3 is not blocked by this

`restamp_evidence_sha256.py` is the ruled re-stamp for `TERM_AND_STYLE_EVIDENCE`
and never runs `build_catalogue.py`; `check_catalogue_dom.cjs` reads only the
checked-in shelf JSON and `index.html`, never a deck. Measured on the F2 branch:
all 20 split decks proved through the narrowed limb, 0 fenced, 0 in
`SCIENCE_ORIGINAL_TARGETS`, 0 without a hashed entry. The DOM check stays exactly
as on main. F3 lands by that route; only §4 stops.

### Finding for the next order (recorded, not repaired)

`_sownb/CALENDAR_SPINE.json` `existingHtml`: **240 of 529 stale** on `6bb8238f`
(Science 71 · Art 33 · ASDAN 87 · Slideshows 31 · Humanities 18). The 14
re-censused in #597 were the ones the catalogue's term re-derivation needed. The
eighth writer is therefore scoped per PR, as the rule states; a whole-spine check
would be red from its first run.
