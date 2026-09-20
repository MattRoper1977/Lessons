# D2 — model-node ribbon contrast: the rendered proof

Ruling D2: fix to >= 4.5:1 by one token per pack, re-measure with axe, zero other
visual change. All three limbs are measured below, not asserted.

## The edit

One declaration, `color:var(--text)` added to `.step-ribbon>*`. 120 occurrences over
120 files, applied by exact match and idempotent.

## Limb 1 — axe

120 of 120 lessons, desktop and phone. **0 serious/critical nodes of any rule; 0
nodes below 4.5:1.** Nothing NOT RUN.

## Limb 2 — zero other visual change

A rendered before/after sweep of the whole pack: pristine as shipped against the
workspace, 120 lessons each, **every stage walked with the pupil `#next-slide`
control**, then re-measured under print media emulation. For every `.step-ribbon`
child: computed colour, painted background (walked up the ancestor chain to the
first non-transparent one), font size, font weight, visibility and the WCAG ratio.

A 700 ms settle after load and after every stage change: `button{transition:all .2s}`
means a colour read taken too early returns the PREVIOUS value.

Across all 120 lessons, screen and print, exactly **two** measured fields differ:

| field | child-instances changed |
|---|---:|
| `fg` (computed colour) | 480 screen, 1124 print |
| `ratio` (derived from `fg`) | 480 screen, 1124 print |

Nothing else moved: not the element set, not geometry, not font size or weight, not
the painted background, not visibility. 0 decks with page errors. That is the limb.

## Limb 3 — the fix works, and on paper it fixes something worse

**Screen.** 787 visible ribbon children: contrast **11.98 to 12.36**, 0 below 4.5:1.
The 480 that changed were all `BUTTON`, which had been inheriting; the other 644
already carried an explicit colour.

**Print.** This is where the real defect was. Before the edit the print copies held:

| colour | children | ratio |
|---|---:|---|
| `#ffffff` | 480 | **1.19 — white on white, invisible on the printed page** |
| `#000000` | 644 | 17.69 |

After: all 1124 are `#1f2937` at **11.98 to 12.36**, 0 below 4.5:1.

Named honestly: 644 children went from pure black at 17.69 to the house `--text` at
12.36. That is a reduction, well above the 4.5:1 the ruling sets, and it is the
price of one token per pack rather than two. The 480 that were printing invisibly
are now legible, which the ruling did not ask for and which no static parse could
have seen.
