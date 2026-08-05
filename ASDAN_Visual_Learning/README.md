> # BLOCKED — DO NOT MOUNT
>
> **This toolkit is committed but mounted by nothing. No lesson loads it, and none may until
> the blockers below are cleared.** Landed 5 Aug 2026 as band A of the ASDAN Visual-Learning
> review (vendor sentinel `asdan-visual-learning-2026-08-05`, pack SHA-256 `9740ae0c…`,
> 139/139 manifest entries re-hashed OK).
>
> **The named blocking items:**
>
> 1. **The vendor's own decisive gate is unrun.** Full post-integration regression in a real,
>    current checkout was declared withheld by the vendor and has not been run here. Nothing
>    pupil-facing merges until it is.
> 2. ~~**Reduced motion is honoured in CSS but not in JS.**~~ **CLEARED 5 Aug 2026.** The engine
>    now reads `matchMedia('(prefers-reduced-motion: reduce)')` at load and registers a change
>    listener that takes effect live; `.asvl-static` — previously driven only by the manual
>    "Static diagrams" button — follows the OS preference, so the control can no longer report
>    `aria-pressed="false"` while CSS is suppressing motion. Proven in real Chromium in **both**
>    directions (reduce-off → `animation-name: asvl-attention`; reduce-on → `none`), plus a live
>    mid-session change, against a stub that fails when the listener is removed. The one
>    `@keyframes` family is classified in `reports/REDUCED_MOTION_REGISTER.md` **RM-3**.
> 3. **The six D&T decks are not on this chassis.** `Build/Slideshows/BUILD_DT_W1..W6.html` carry
>    **0** `ASDAN-TEACH:` marker blocks and **0** `visual-upgrade` references, and the BUILD
>    compiler's scope is `BUILD_ASDAN/*/*.html`, which does not reach them. Any D&T integration is
>    a separate, authored decision — it does not follow from mounting this toolkit.
> 4. **`docs/MEDIA_REGISTER.md` is a candidate register only** — see its own header. No URL in it
>    has been resolved; this container has no network.
>
> Removing this block is a decision with a name on it, not a tidy-up.

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
