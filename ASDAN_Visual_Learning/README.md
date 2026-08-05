> # STATUS — mounted across all 85 taught decks
>
> **This toolkit is live.** All 85 ASDAN lesson decks load it: 31 BUILD (materialised through
> `BUILD_ASDAN/_framework/`), 18 GROW and 30 LAUNCH through their shared `visual-upgrade` layers,
> and the 6 D&T decks by per-file integration. The BLOCKED — DO NOT MOUNT wording that headed
> this file has been **removed rather than softened**: it had become untrue, and a blocked banner
> on a mounted toolkit is a co-present contradiction.
>
> **The four original blocking items, all closed:**
>
> 1. The vendor's decisive post-integration regression — **RUN**, in a real browser, per batch.
>    A green from an older tip was never accepted as a green.
> 2. Reduced motion in JS — **CLEARED** at `cc4f6fa`; `matchMedia` read at load and watched live.
> 3. The six D&T decks' chassis — **RESOLVED**; their staff answers organ is present and they
>    mount by per-file integration, which is what `integrate.py` always did for those paths.
> 4. `docs/MEDIA_REGISTER.md` — **still a candidate register, and it gates nothing.** No URL in
>    it has been resolved. `lesson-payloads.json` carries 0 external URLs and 0 embeds, so no
>    mounted surface depends on it. This is the one parked item, and it stays parked.
>
> **Accessibility.** The eyebrow, the sequence badges and the button family all render on a
> **solid chip** — `--asvl-accent-chip`, the pathway hue darkened by a fixed 74% mix toward black.
> Text darkening alone could never hold a floor, because the header gradient's tint moves per
> deck and the contrast pair was unstable; the chip makes the pair known. Derived across all nine
> measured (tint, accent) pairs in the estate: white-on-chip ≥ 4.6:1 (worst 4.68) and
> chip-vs-header ≥ 3:1 (worst 3.94). Solid, never translucent — translucency would re-import the
> moving background.

# ASDAN Visual Learning

Progressive-enhancement toolkit for all 85 taught BUILD, GROW and LAUNCH ASDAN lesson decks in the Lessons repository.

## Supplementary-content boundary

The existing authored lesson text, answers, order and assessment wording remain untouched. The mounted panel does add visible, task-specific rehearsal prompts and original diagrams, so it is **supplementary teaching content**, not a visually inert style-only change. Review the 85 payloads as new resources before any mount commit. Content-integrity comparison must exclude only the owned marker blocks; the integration commit must not weaken the gate that judges it.

## What it does

- mounts one lesson-specific visual rehearsal in the intended We Do slide;
- uses sorting, sequencing, evidence selection, hotspots and finite models;
- enforces prediction before action in GROW and LAUNCH;
- enforces a structured evidence-locator gate in LAUNCH;
- hands pupils from rehearsal to the real independent task;
- stores nothing and makes no assessment or qualification decision;
- supplies 85 original accessible SVG teaching models;
- integrates through the estate’s existing shared sources.

## What it does not do

It does not upload evidence, collect names, store data, assign a level, map a criterion, grade work, mark an evidence state, moderate, verify or certify a qualification.

## Validate

```bash
python3 build_payloads.py --check
python3 check.py
node --check asdan-visual-learning.js
python3 browser_test.py --evidence-dir /tmp/asdan-visual-browser
```

## Generate the exact source patch

From the Lessons repository root after this directory has been added:

```bash
python3 ASDAN_Visual_Learning/integrate.py   --repo .   --patch-out /tmp/asdan-visual-source-integration.patch   --json-report /tmp/asdan-visual-source-integration.json
```

Review with:

```bash
git apply --stat /tmp/asdan-visual-source-integration.patch
git apply --check /tmp/asdan-visual-source-integration.patch
```

After applying locally, materialise BUILD through its existing compiler:

```bash
python3 BUILD_ASDAN/_framework/apply_framework.py
python3 ASDAN_Visual_Learning/integrate.py --repo . --check --expect-build-materialized
```

Read `docs/ESTATE_SCOPE_AND_INTEGRATION_ARCHITECTURE.md`, `docs/DATA_EVIDENCE_AND_ASSESSMENT_FIREWALL.md` and `docs/TEST_PLAN.md` before any commit.
