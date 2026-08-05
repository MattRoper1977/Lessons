> # ADOPTED — a standing part of the BUILD/GROW/LAUNCH ASDAN provision
>
> **ADOPTED.** A standing part of the BUILD/GROW/LAUNCH ASDAN provision, mounted on all 85 taught
> decks, maintained in this repository. **Ruled by Matt, 5 Aug 2026.** This supersedes the earlier
> "vendor pack under review" framing: it is no longer a trial, and no longer supplementary.
>
> **Alignment, with the boundary intact.** It supports the teaching of the PEQ six skills and
> aligns with the estate's audited accreditation claims. **It performs no assessment, moderation,
> evidence-state or quality-assurance function. No awarding-body endorsement is implied. The
> data/evidence firewall document remains authoritative and unchanged.**
>
> **What adoption deliberately did NOT change.** No public-surface accreditation claim moved — the
> ComSk1-only registration and the provisional-wording rules stand untouched. No catalogue entry
> was minted: this is runtime loaded by lessons, not a standalone resource. No prior banner was
> resurrected.
>
> **Mount state:** 31 BUILD (materialised via `BUILD_ASDAN/_framework/`), 18 GROW and 30 LAUNCH
> through their shared `visual-upgrade` layers, 6 D&T by per-file integration. The vendor's own
> `integrate.py --check` passes.
>
> **The one parked item:** `docs/MEDIA_REGISTER.md` remains a **candidate register and gates
> nothing** — no URL in it has been resolved, and `lesson-payloads.json` carries 0 external URLs
> and 0 embeds, so no mounted surface depends on it.
>
> **Accessibility:** eyebrow, sequence badges and buttons render on a solid chip
> (`--asvl-accent-chip`, the pathway hue at a 74% mix toward black), derived across all nine
> measured (tint, accent) pairs: white-on-chip ≥ 4.6:1, chip-vs-header ≥ 3:1.

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
