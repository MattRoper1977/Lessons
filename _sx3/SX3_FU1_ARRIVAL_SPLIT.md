# ORDER SX3-FU1 — arrival stage split

F1 measured, F2 built and applied. Every figure below is rendered in a real browser
(chromium via playwright) over a named scope, per the contract's standing rule 5.

## F1 — the finding

Scope: all 31 landed science decks plus the 3 pathway exemplars named in
`CHASSIS_CONTRACT.md` (lines 19–23).

| pathway | decks | stage 0 shape |
|---|---:|---|
| exemplars (BUILD, GROW, LAUNCH) | 3 | **9 stages**; stage 0 is the title stage (`data-timer="0"`), stage 1 the arrival |
| BUILD landed | 1 | already two-stage |
| GROW landed | 7 | already two-stage |
| LAUNCH landed | 23 | **merged**: stage 0 is `data-type="arrival"` and carries BOTH the `<h1>` title block and the arrival root — 8 stages, one short of the exemplar |

BUILD and GROW were measured, not assumed; they already conform and are untouched.

Separately found and **left alone**: `[data-arrival-root]` is orphaned at `<body>`
on all 31 landed decks — inside no stage at all. That is a pre-existing defect
outside this order's scope. F2 neither moves nor silently repairs it, and the
acceptance test asserts it is still exactly as found.

## F2 — the one adapter rule

`tools/sx3/split_arrival_stage.py`. When source stage 0 carries both the title
block and the arrival root, it splits into the exemplar's two-stage shape, with
the timer minutes carried to the arrival stage. Applied to 23 decks; a second
pass reports 0 applicable, so it is idempotent. Self-test: 27/27 PASS, including
every planted fault.

Exactly two strings are created, both derived, neither authored:
`<span class="slide-tag tag-opening">Opening</span>` (the house form already on the
BUILD and GROW decks) and `<h2 id="title-a1" tabindex="-1">TITLE</h2>`, where TITLE
is the merged stage's own `data-title`.

### The knowledge shortcut crosses the cut

Contract row 41: "All three exemplars keep the knowledge-organiser opener inside
slide 1." Measured: on all three, `div.knowledge-shortcut` is the **last child of
the opening stage**. On a merged deck it is the last child of the merged stage,
which puts it *after* the cut — so the first version of this rule sent it to the
arrival stage, where it is not on the stage a teacher sees at load.

That was caught by driving the real control in a browser, not by reading the diff:
**row 41 went 155 dialogs opened → 132, with the organiser opener failing on 23/23
decks.** The rule now moves it back, and refuses rather than guessing if a deck
carries more than one or carries one anywhere but trailing.

## Acceptance — "same text, one more stage, nothing lost"

BEFORE = the pre-split bytes at `HEAD`, extracted to a separate tree; AFTER = the
working tree. Text basis: every non-empty **text node** of `main#lessonDeck`, in
document order.

Two earlier instruments were wrong and are recorded so they are not repeated:

1. `document.body.innerText` returns only the **visible** stage. Before the split
   the visible stage 0 is the merged arrival; after it is the new opening. It
   compared two different stages and reported "text lost" — the #11 family.
2. `textContent` puts no whitespace at element boundaries, so tokens glue across
   edges (`ArrivalLAUNCH`). Moving a boundary re-glues them, and a string diff
   scores the legitimate reordering as delete+insert.

**23/23 PASS, 0 failures**, and the 8 untouched decks are byte-identical on every
measured field:

- stage count +1 on exactly the 23; `timer_total` unchanged on all 31
- text nodes +2 and only +2; **nothing lost**; the two additions are exactly
  `Opening` and the arrival heading
- the tail stages shift by exactly one, byte-for-byte, metadata included
- the two new stages together hold the whole of the old stage 0, plus those two
- `interactive` +1 (the new `h2[tabindex="-1"]`), `h2` +1; buttons, route panels,
  route controls, `h1`, images and arrival roots all unchanged

**Reordered, not lost:** the arrival tag span and the `science-meta` line (which
ends `· N MINUTES`) travel to the arrival stage, because the order carries the
minutes there. The exemplar's own brandline sits on the opening stage, but it
states no minutes; the landed `science-meta` does, so leaving it on an untimed
opening stage would print a false figure. Named deviation, not a silent one.

## Rows 1–42, re-measured

Rendered over all 31 decks, before and after, by driving the real controls.

| rows | result |
|---|---|
| 1–34, 36, 37 | **no change**, any deck |
| 35 (stages) | 8 → 9 on the 23. The contract's figure of 9 is the stage count; the selector `[id^="slide-"]` also matches `#slide-picker`, confirmed by measuring all three exemplars (9 stages, 10 matches). **Before: 23/23 off the exemplar. After: 0/23 off.** The split lands on the exemplar, it does not overshoot |
| 38 (JS errors) | 1 of 31 before, the same 1 after — `SCI_B_W12_Give_a_rock_a_job_Classic.html`, `ERR_FILE_NOT_FOUND` for the absolute `/hud.js`, an artefact of `file://` loading on an **untouched BUILD deck**, and the known cross-repo dependency of contract section A1 |
| 39 (dialog controls that still drive) | 187 → 187, 0 changed |
| 40 (pack dialog remap) | **not measurable here**: these 31 decks carry 0 `#dialog-*` nodes, before and after. Not reported as a pass |
| 41 (every dialog opens) | 186 driven; 155 opened before, **155 after, 0 changed**. Also unchanged: 30 that open at 0×0 and 31 with no control found — both pre-existing |
| 42 (no double-driving) | elements stamped `data-sx3-shell="1"`: 15–18 per deck, 0 decks changed |

### Off-exemplar rows that F2 did not touch and did not cause

Identical before and after on all 23; recorded for a later order, not fixed here:

| row | exemplar | landed | note |
|---|---:|---:|---|
| 13 `#tools-dialog` | 1 | 2 | duplicate id |
| 14 `#organiser-dialog` | 1 | 2 | duplicate id |
| 15, 21, 22, 23, 24, 26, 27, 28, 29 | 4, 3, 3, 3, 6, 2, 1, 1, 2 | 0 | the print family — the contract's own VOID ruling says the pack owns `#print-area` at runtime and deletes every static `#print-*` section the moment JS runs, so 0 at runtime is what that ruling predicts |
| 30 `.teacher-only` | 3 | 1 | pre-existing |

---

# Correction: 20 decks split, 3 refused, and the landing is blocked on main

The first pass split 23. Regenerating the derived records afterwards — which any
change to a deck's bytes forces — showed that three of them lost their catalogue
term binding. Both facts below were measured against a clean `origin/main`
worktree, so each red is attributed before anything was written.

## The 3 refusals

On most decks the `science-meta` line states only the arrival stage's minutes. On
three it glues two different facts together:

```
LAUNCH · GCSE BIOLOGY FOUNDATION · W12 · LESSON Classic · 4 MINUTES · Aut2·W4
                                                          ^^^^^^^^^   ^^^^^^^
                                            the arrival stage's timer  the LESSON's term
```

`build_catalogue.py`'s weakest fallback derives a deck's term from a term code
appearing anywhere in **stage 0's text**. F2 carries the minutes to the arrival
stage, so the term travels with them and the catalogue term silently falls to
`unspecified`. The adapter now refuses rather than dropping a binding:

| deck | term at risk |
|---|---|
| `SCI_L_W9_Copy_separate_divide_Classic.html` | `Aut2·W1` |
| `SCI_L_W12_Zoom_into_genetic_information_Classic.html` | `Aut2·W4` |
| `SCI_L_W13L2_Punnett_Square_Explore.html` | `Aut2·W5` |

All three are left exactly as found. Splitting them needs a ruling: either the term
is registered by a stronger instrument, or the meta is separated into a stage line
and a lesson line — neither is derivable from the deck.

**20 decks split, and the rendered acceptance is 20/20, 0 failures**, with the 11
untouched decks byte-identical on every measured field. F2's isolated effect on the
catalogue record is now exactly **20 sha256 updates and nothing else** — proved by
running `build_catalogue.py` on a clean main worktree and on this branch and
diffing the two writer outputs.

## The landing is blocked by a pre-existing defect on main

`origin/main` at `cbfbc70c` **cannot regenerate its own catalogue record.** Measured
on a clean worktree, with no change of mine:

- `build_lesson_order.py --check` PASSES on pristine main — the committed records are
  mutually consistent.
- but running `build_catalogue.py` first, then `build_lesson_order.py`, **asserts** on
  `SCI_L_W10L1_Growth_And_Differentiation_Introduce.html`.

Its own writer changes 38 entries and drops the term on **14 LAUNCH W9–W13 decks**,
every one of them from `current content re-proves audited workbook binding` to
`current presentation structure`. Root cause, for one of the 14:

| limb of the re-prove | state |
|---|---|
| `blobSha256` unchanged | **no** — `_sownb/CALENDAR_SPINE.json` still pins the **pre-transplant** bytes `503c0cdd…`; the deck is now `612b4544…` |
| verbatim outcome present in the body | **no** — the transplant re-worded the deck |
| that outcome long enough to count | **no** — `'Explain growth & stem cells.'` is exactly 28 characters and the guard is `len(...) > 28`, so a byte-perfect match would still be rejected |
| `secondInstrumentEvidence` | **empty** |

No limb can fire. The committed record still reads `Aut2` only because it has not
been regenerated since the transplant changed those bytes.

**Consequence.** Any change to a science deck forces a catalogue regeneration, which
breaks `build_lesson_order.py`, which blocks `pin_catalogue_contract.py` — the pins
step. So F3's landing cannot complete the four-writer sweep until the spine is
reconciled. F2 is simply the first change to trip a latency that is already there.
The derived records are therefore **left untouched on this branch**: regenerating
them would carry main's 14 term losses into an F2 PR.

## Sweep attribution

Run against a clean `origin/main` worktree and an `origin/main` Apps worktree:

| writer | clean main | this branch | attributed to |
|---|---|---|---|
| `check_catalogue_static` | PASS | FAIL | **F2** — the 20 deck hashes moved |
| `pin_catalogue_contract --check` | PASS | — | — |
| `data/resource-sizes.json` | PASS | FAIL | **F2** — the 20 deck sizes moved |
| `derive_triggers --check` | PASS | PASS | — |
| publication census | NOT RUN | NOT RUN | needs the one granted build |

A fifth red seen first time round — `gate copies differ` — was **not** the estate: the
local Apps clone sat on `claude/sx3-apps-pair4`. Lessons main and Apps main hold the
gate byte-identical at `f38a2a6f91cc5c83…`, exactly as the order names.
