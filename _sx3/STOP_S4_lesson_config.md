# STOP-S4 — §7(b)'s token fixes 6 of 36. The real defect is in the transplant.

ORDER SX3-M2 §7(b) directs one content change: a visible derived token per deck.
Measured against the actual proposed content, that lifts **6 of the 36**. The
other 30 fail for a different reason, and that reason is a chassis-transplant
defect, not a content question. Reported before writing to any deck.

## What landing the 36 does today

Search scope: a clean worktree at `origin/main` with only the 36 landing files
replaced by their branch versions — the 20 held files left at main — then
`tools/catalogue/build_lesson_order.py` run for real.

```
{"entries": 1077, "weekBound": 238, "versionLinks": 136, "refreshedSourceProofs": 0}
unresolvedTiming: 36
```

All 36 land in `unresolvedTiming` and **all 36 lose their week binding** in the
derived view: `weekBound` falls 274 → 238. That is exactly the state ORDER
SX3-END2 §5 refuses.

No `AssertionError` fires, because the assert only guards `style: recommended`
decks and all of those are in the held 20. The bindings drop silently.

## Why §7(b)'s token is not enough

The narrowed limb, as signed and landed in #586, is:

```python
token_proved = bool(proofs) and bool(tokens) and all(key in text for key in tokens)
```

`proofs` is a recorded `own title slide declaration` in
`TERM_AND_STYLE_EVIDENCE.json`. Of the 36 landing decks, **6 have one; 30 do
not.** For those 30 the limb never reaches the token, so writing the token
changes nothing. Measured with the token assumed written: 6 proved, 30 still
unresolved.

## The actual defect

The 30 are bound by `current content re-proves audited workbook binding`, which
the `preserved_outcome` limb tests by comparing the deck's
`lesson-config.sow` against the recorded `currentOutcome`. Measured on all 30:

```
   30  proposed lesson-config has no `sow`
```

The deck at `origin/main` carries `sow` equal to the recorded outcome. The
transplanted deck does not — because the transplant **replaces** `lesson-config`
wholesale instead of merging it. Across the 36:

| lesson-config key | decks that LOSE it in the transplant |
|---|---|
| `timings`, `previousFile`, `nextFile`, `id` | 30 |
| `week`, `objective` | 27 |
| `handoff`, `model1Steps`, `model2Steps`, `glitch`, `independent`, `mission` | 24 |

and the transplant adds its own `stages`, `key`, `pathway`, `prefix`.

`previousFile` / `nextFile` are lesson navigation. That is very likely the same
root as the "Original Science navigation" defect ORDER SX3-END4 asked be
root-caused.

This is the same class as chassis-contract rows 43 and 44 — estate furniture
restore, exemplar sibling-nav unwrap. The transplant's stated principle is to
keep every structural element and id and replace only content-bearing regions.
`lesson-config`'s binding keys are structural: they are the deck's tie to the
scheme of work and to its neighbours.

## Measured fix, simulated end to end

Simulation in a throwaway worktree only; nothing written to any branch. The
binding keys the transplant drops are merged back from the deck at `origin/main`
(`sow`, `objective`, `week`, `id`, `previousFile`, `nextFile`, `timings`,
`source`), then the real builder is run:

```
{"entries": 1077, "weekBound": 268, "versionLinks": 136, "refreshedSourceProofs": 30}
still unresolved of the 36: 6
```

**30 of 36 recovered with no visible content written and no jargon added.**
`weekBound` 238 → 268.

The remaining 6 are exactly the decks with **no `lesson-config` on main to merge
from**, and all 6 carry a recorded own-title-slide declaration and a binding —
so they are precisely the 6 that §7(b)'s token lifts:

- `Science_Teesside/Build/W8-W13_2026-27/SCI_B_W12_Give_a_rock_a_job_Classic.html` — `Aut2·W4`
- `Science_Teesside/Grow/W8-W13_2026-27/SCI_G_W9_Turn_Earth_explain_the_sky_Classic.html` — `Aut2·W1`
- `Science_Teesside/Grow/W8-W13_2026-27/SCI_G_W12_Follow_the_warming_chain_Classic.html` — `Aut2·W4`
- `Science_Teesside/Launch/W8-W13_2026-27/SCI_L_W9_Copy_separate_divide_Classic.html` — `Aut2·W1`
- `Science_Teesside/Launch/W8-W13_2026-27/SCI_L_W12_Zoom_into_genetic_information_Classic.html` — `Aut2·W4`
- `Science_Teesside/Launch/W8-W13_2026-27/SCI_L_W13L2_Punnett_Square_Explore.html` — `Aut2·W5`

Note `source` matters: without it, 12 remained; with it, 6. It is what the
`explicit_cell` limb reads, and it carries the 3 LAUNCH `A2_W7` assessment decks
and the 3 LAUNCH `W14` genetic-condition decks.

## What I propose, and why I stopped to ask

The two measures together are `30 + 6 = 36`, restoring `weekBound` to main's 274.
Both are deck-byte changes, so both fit inside §7's **one** content change:

1. a chassis-contract row — carry `lesson-config`'s binding keys through the
   transplant instead of replacing the block; and
2. §7(b)'s visible derived token, on the 6 that have no config to carry.

I stopped because (1) is not what §7(b) says. §7(b) assumed the token was the
fix; measured against the real content it is the fix for 6 decks out of 36. The
standing instruction since ORDER SX3-END4 is to root-cause before a content
change, and this is the root cause — but changing the shape of the one permitted
content change is the operator's call, not mine.

**Requested:** authorise (1) alongside (2) as the single content change. Nothing
has been written to any deck.
