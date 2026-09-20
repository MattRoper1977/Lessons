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
