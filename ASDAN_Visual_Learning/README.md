> # BLOCKED — DO NOT MOUNT (band C outstanding)
>
> **Band B is mounted. The rest of the estate is not.** Four decks load this toolkit —
> `CAREERS_W1_My_Strengths` (BUILD), `PEQ_W1_Knowing_Myself` (GROW),
> `PEQ_W1_Intro_and_Choosing_My_Level` (LAUNCH) and `BUILD_DT_W1_Workshop_Audit` (D&T).
> **No other deck may be mounted outside a gated band-C batch.** This wording comes off
> entirely when band C completes; a blocked banner on a fully mounted toolkit would be a
> co-present contradiction, which is this estate's signature defect.
>
> **The four original blocking items:**
>
> 1. ~~The vendor's decisive gate is unrun.~~ **RUN AND GREEN for band B.** The full suite was
>    executed in real Chromium against the mounted specimens: contrast, smoke (26 checks),
>    label-rest, reduced motion, print at 718×1047, marker confinement, `#print-witness`
>    byte-identity and the estate protective scans. It must be re-run per band-C batch — a
>    green from an older tip is not a green.
> 2. ~~Reduced motion is honoured in CSS but not in JS.~~ **CLEARED** at `cc4f6fa`.
> 3. ~~The six D&T decks are not on this chassis.~~ **RESOLVED.** True of the BUILD compiler
>    (0 `ASDAN-TEACH` markers; it globs `BUILD_ASDAN/*/*.html`) but not of the staff route: the
>    D&T chassis carries the exit-slide answers organ, byte-identical in shape to the compiler
>    chassis's. They mount by authored per-file integration, which is what `integrate.py`
>    already does for exactly these six paths.
> 4. **`docs/MEDIA_REGISTER.md` is a candidate register only — PARKED, and it gates nothing.**
>    No URL in it has been resolved; egress is denied here (`gov.uk`, `nhs.uk`, `asdan.org.uk`
>    all return HTTP 000, the proxy logging `connect_rejected`). But `lesson-payloads.json`
>    carries **0** external URLs and **0** embeds, so no mounted surface depends on it. It
>    stays a candidate register regardless of what a future session resolves.
>
> **Accessibility ruling applied (5 Aug 2026).** `.asvl-eyebrow` no longer paints the raw
> inherited accent. A toolkit token `--asvl-accent-text` darkens it by a fixed 91% mix toward
> black — the hue angle is preserved exactly, only lightness moves — clearing ≥4.6:1 on every
> pathway (BUILD 5.08, GROW 4.63, LAUNCH 4.76). `--asvl-muted-text` does the same at 96% for
> muted body text. **The estate's strand palette is untouched:** `--asvl-accent` still drives
> every border, ring and fill unchanged, and whatever `--muted` a host deck supplies is
> darkened rather than replaced.
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
