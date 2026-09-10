# RW1-C §O · the verify queue, before and after

**Before: 35 items. After: 18.** Seventeen retired — 2 duplicates, 15 already
answered by `tools/rw1/parity.py` (DOM query) or `tools/rw1/render_check.cjs`
(browser). What that saves goes to K1–K5, which is where the risk is.

## O1 · duplicates removed (2)

| dropped | kept |
|---|---|
| `D4 "Original W8A lesson" link` (2nd copy) | the first, now proved: `madebymatt.uk` 0/0 |
| `CROSS-LINK W8A↔W8B` (2nd copy) | the first, and it grew — the forward link was pack-relative and would have 404ed |

## O2 · retired, with the run that answers them (15)

Each cites a measurement already taken, per O2.

| retired check | answered by | value |
|---|---|---|
| way-home present | parity `a.mbmhome` | 1 / 1 |
| Made by Matt mark | parity + render `div.n6-splash` | 1 / 1, **renders**, `aria-label="Made by Matt"` |
| skip link present | render | 1, and **focus moves** |
| prev link | parity `[rel=prev]` | 1 / 1 |
| next link | parity `[rel=next]` | 1 / 1 |
| nav row | parity `a.next-link` | 3 / 3 |
| guide layer present | render `button.n6m-guide-btn` | in DOM, visible, "ⓘ Guidance" |
| guide CSS block | parity `style#n6m-guide-css` | 1 / 1 |
| guide storage | parity, script text | 1 / 1 |
| `data-ta1` → `data-prompt` | parity | 9 → 9, declared supersession |
| `teacher-only` present | parity | 2 / 2 |
| `data-mbm-guide="staff"` | parity | 3 / 3 |
| `.lundy-grid` gone | grep + parity | `lundy` 0 / 0 |
| pupil-facing Lundy gone | same | 0 / 0 |
| duplicate ids | parity + render | 0 / 0, both |

## Kept — parity.py does not cover these (18)

Slide count · cross-links resolve as **served** paths · catalogue link ·
`START_HERE` reference · **ECA-1 hide-by-default behaviour** (a toggle *state*,
not an attribute count) · served-file checks after landing · the six print routes
and what each emits · A4 fit for three staff cards · the entry-point dependency
audit · IF NEW / IF REVISION splits summing 40.0 · the §5.3 script appearing
exactly once · the catch-up register · drag completing by keyboard · reduced
motion halting all motion · third-party loads in a browser · pin moves ·
admission · the rendered `#basis-caption`.

## Kept although parity touches it, and why

**ECA-1 hide-by-default.** Parity proves `data-mbm-guide="staff"` is *present* on
3 nodes. It cannot prove the toggle *hides* them by default, or that they are
absent from the accessibility tree with the guide off. That is behaviour, and
§4.4 asks for it with a red proof. No other instrument covers it.
