# STOP-RESP-3 — the window was cut from the content diff, and the content diff is not the moving set

## What happened

Site #430 admitted **27** paths, derived from the Lessons branch's content diff. CI on the
Lessons partner (#647) then went red:

```
[PASS] data/calendar-spine.json equals its derivation (6 blocks, 40 weeks)
[FAIL] data/resource-sizes.json differs from the working tree — run: python3 tools/ux2/resource_sizes.py --write
```

Regenerating with the repo's own tool moved exactly 3 rows — the three `START_HERE.html`
files that gained the responsive furniture:

```
Humanities_Teesside/BUILD_W27-W39_2026-27/START_HERE.html     9415 -> 10281
Humanities_Teesside/GROW_W27-W39_2026-27/START_HERE.html      9832 -> 10698
Humanities_Teesside/LAUNCH_W27-W39_2026-27/START_HERE.html   10756 -> 11690
```

But `data/resource-sizes.json` is **itself a served path**. Building the education tree at
the pending head against the merged window refuses exactly one path, measured not assumed:

```
ValueError: Education file admission blocked publication:
CHANGED education-lessons/data/resource-sizes.json
```

Its admitted value on Site main is already a pair, and the pending build is a **third**
state:

```
admitted pair : ['6428ad5e9ee0…', 'cb7f4b85b57a…']
built pending : c05660602697427d3ffe0a90adca1ededac9efee7053a40d20fe66314392c328  (149800 bytes)
already admitted? False
```

## The general lesson — a correction to the standing shape

The ruled pending-then-land fold says step 1's window "admits the moving paths". I derived
that set from the **content diff**, and that is wrong in the general case:

> **The moving set is the content diff PLUS every derived artefact the content change
> forces to be regenerated — and some of those artefacts are themselves served.**

Here the chain is: 21 responsive pages change → `tools/ux2/resource_sizes.py --check` goes
red → the size table is regenerated → and the size table is a published path. The 28th mover
is not visible in the content diff at all; it only appears once the derivation is re-run.

So the window must be cut **after** the derived regeneration, not before it. Concretely, for
any future fold:

1. make the content change,
2. run every `--check`-style derivation the repo owns (`resource_sizes.py`,
   `build_spine.py`, the catalogue writers, the pack checksum re-cut) and apply their
   `--write`,
3. **then** take the moving set and cut the window from it.

Doing (3) before (2) admits a set that is short by exactly the derived artefacts.

## Resolution: a step 1b window

A second small Site window re-cutting `data/resource-sizes.json`'s pair to
`[main-today, pending]`, exactly as #430 did for the 27. The `main-today` element is being
derived by building at Lessons main rather than assumed to be the existing pair's second
element.

This does not disturb #430, which is correct as far as it goes; it extends it by one path.
Correction #33 (served-set intersection before merge) and the one-window-at-a-time rule
both still hold — this window follows #430 rather than running beside it.
