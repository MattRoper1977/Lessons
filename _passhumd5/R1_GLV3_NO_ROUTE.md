# R1 STOP — GLV3 has no additive-pinned-pack route for Humanities

Ruling R1 lands the proofread packs "to Teaching_Packs as additive, pinned pack
files (the HP1/HC5 precedent; GLV3's additive-pinned-pack route)". Measured against
the verifier, that route does not exist for Humanities. Nothing has been staged
there.

## The route is prefix-gated to Science

`_glv3/tools/verify_change_boundary.py`:

```python
SCIENCE_PACKS = 'Science_Teesside/Teaching_Packs/'
...
elif rel.startswith(SCIENCE_PACKS) and rel in pins:
    # Owner-requested 6 September additive BUILD/GROW downloads.
    # Every individual file has an explicit reviewed digest; the
    # prefix alone never admits a file or an existing-file edit.
    if status != 'A' or not (root / rel).is_file() or pins[rel] != sha(root / rel):
        errors.append('Science teaching pack must be an exact reviewed addition: ' + rel)
```

`Humanities_Teesside` IS in `PROTECTED`, but its only routes are `SHELVES`
(`Humanities_Teesside/index.html`) and `COVER`
(`Humanities_Teesside/David_Cover_Autumn1_W3-W7`). There is no Teaching_Packs clause.

## Proved by executing `judge()`, read-only, with controls

| case | result |
|---|---|
| **A** addition under `Humanities_Teesside/Teaching_Packs/…`, unpinned | `original GLV3 protected-path fence rejected` |
| **B** the same addition **with a pin injected into `pin_map`** | **still rejected** — the prefix test fails before the pin is consulted |
| **C** *positive control*: the equivalent **Science** pack path, pinned, status `A` | **ADMITTED, no errors** |
| **D** *negative control*: that same Science path as `M` | `Science teaching pack must be an exact reviewed addition` |

C and D prove the harness is exercising the real logic, not returning a constant.
Pins in `CATALOGUE_PINS`: **354 Science pack files, 0 Humanities.** Pinning a
Humanities pack file changes nothing.

## The HP1/HC5 precedent is a non-run, not an admission

`glv3-verify.yml` fires only on `GROW_Estate_v3/**`, `LAUNCH_Estate_v3/**`,
`resources.json`, `_finish/ROUTES.md`, `_glv3/**` and its own file.
**`Humanities_Teesside/**` is not in the filter.** The 245 Humanities
`Teaching_Packs` files already on disk were landed by commits that touched none of
those paths, so the fence never ran on them. `_sx3/RELEASE_LEDGER.md` already
records this class for Science: *"It had been rejecting every landing deck on every
branch the whole time."*

## And "the download series" is what wakes the fence

R1 lands the packs **as the download series**. The pack rows are derived from
`data/companion-packs.json` into `resources.json` — and `resources.json` **is** a
`glv3-verify` trigger path. So the same PR that adds the rows wakes the fence for
the first time, and it then judges the whole protected diff: every new
Humanities_Teesside pack file appears as `A` and each is rejected. A Humanities pack
PR that also touches `resources.json` both fires the fence and has no route through it.

A replacement transaction is not an escape either: a transaction member must be
status `M` and carry a `beforeGitBlob`, which a brand-new file has none of — so a
transaction is unconstructible for added files. Ledger **L18** already ruled exactly
this for a new protected page and closed it with `PATHWAY_PARENTS`, an addition-only
pin-checked set.

## What a Humanities route would cost

Following the `PATHWAY_PARENTS` precedent: a new reviewed `HUMANITIES_PACKS` clause
in `judge()`, **with its own red-proof controls** (the existing routes each carry
three or four planted reds, and `--self-test` runs them in CI); a pin per file; a
re-cut of the verifier's own sha256, which is itself pinned in `CATALOGUE_PINS`, in
**both** estate gate copies in the same window; and PIN1 trigger regeneration —
`derive_triggers.py` materialises one `paths:` entry per pinned file into both PIN1
blocks, which already carry 557 entries each.

That is a gate change with CI edits, which the standing limits reserve. **Ruling
needed.** The options as I see them:

1. **Open a Humanities route** in `verify_change_boundary.py`, built like
   `PATHWAY_PARENTS`, with its refusal controls — a reviewed gate change.
2. **Land the packs where the fence does not reach** (not under a `PROTECTED`
   prefix) and accept that they are not in the download series.
3. **Land as the download series in two windows**: pack files first in a PR that
   touches no trigger path, then the `resources.json` rows separately — which the
   ledger's own Science precedent shows is exactly the blind spot that let 245 files
   land unjudged, so I would not choose it without it being ruled.

Separately and still open: **R9.** Re-cut at `origin/main` `cbfbc70c`, all tracked
files are **1,127.4 MB**, tracked minus `_*`/`.*` is **921.1 MB**, and the `.git`
pack is **1.46 GiB**. The packs add **230.3 MB** (mp4 46.5 MB), taking all-tracked to
**1,357.6 MB**. R9's own text says STOP before the content PR and report; every
measure except one already exceeds 950 MB before landing anything.
