# ASDAN estate scope and integration architecture

## Authoritative inventory

The scope was derived from the pathway and subsection hubs, not from a broad filename guess.

| Pathway | Taught decks | Subsections |
|---|---:|---|
| BUILD | 37 | Careers 7 · Living Independently 6 · FoodWise 6 · Community Project 6 · Duke and Enterprise 6 · Community Upcycling D&T 6 |
| GROW | 18 | PEQ 6 · Community Project 6 · Enterprise 6 |
| LAUNCH | 30 | PEQ 6 · Careers 6 · Living Independently 6 · Vocational 6 · Community and Enterprise 6 |
| **Total** | **85** | **14** |

The exact files are listed in `LESSON_UPGRADE_MAP.md` and `lesson-payloads.json`.

## Protected non-lesson surfaces

The automatic integration does not mount into:

- pathway and subsection hubs;
- schemes of work and weekly plans;
- printable evidence packs;
- witness statements;
- tracking, moderation or qualification records;
- claims registers and safeguarding files;
- proposed Lundy/ASDAN portfolio-studio artefacts.

Those files have different responsibilities. A visual rehearsal must not quietly become a second qualification or evidence workflow.

## Existing source ownership

### BUILD ASDAN

The 31 lessons under `BUILD_ASDAN/` are self-contained files compiled from:

- `BUILD_ASDAN/_framework/asdan-teach.css`
- `BUILD_ASDAN/_framework/asdan-teach.js`
- `BUILD_ASDAN/_framework/apply_framework.py`

The existing framework documentation explicitly says to edit the source rather than the injected copies. The new layer follows that rule.

### GROW ASDAN

The 18 lesson decks load:

- `GROW_ASDAN/visual-upgrade.css`
- `GROW_ASDAN/visual-upgrade.js`

The new owned blocks are appended to those maintained sources.

### LAUNCH ASDAN

The 30 lesson decks load:

- `LAUNCH_ASDAN/visual-upgrade.css`
- `LAUNCH_ASDAN/visual-upgrade.js`

The new owned blocks are appended to those maintained sources.

### BUILD Community Upcycling D&T

The six decks in `Build/Slideshows/` sit outside the BUILD ASDAN compiler. They receive one inline block bounded by a dedicated HTML marker pair. This preserves their standalone/offline packaging.

## Owned markers

```text
/* ASDAN-VISUAL-LEARNING:CSS:BEGIN v1 */
/* ASDAN-VISUAL-LEARNING:CSS:END v1 */

/* ASDAN-VISUAL-LEARNING:JS:BEGIN v1 */
/* ASDAN-VISUAL-LEARNING:JS:END v1 */

<!-- ASDAN-VISUAL-LEARNING:HTML:BEGIN v1 -->
<!-- ASDAN-VISUAL-LEARNING:HTML:END v1 -->
```

The integration tool edits only content inside those markers. It is dry-run by default and invokes no Git command.

## Integration workflow

From a clean checkout:

```bash
python3 ASDAN_Visual_Learning/build_payloads.py --check
python3 ASDAN_Visual_Learning/check.py

python3 ASDAN_Visual_Learning/integrate.py   --repo .   --patch-out /tmp/asdan-visual-source-integration.patch   --json-report /tmp/asdan-visual-source-integration.json

git apply --stat /tmp/asdan-visual-source-integration.patch
git apply --check /tmp/asdan-visual-source-integration.patch
git apply /tmp/asdan-visual-source-integration.patch

python3 BUILD_ASDAN/_framework/apply_framework.py

python3 ASDAN_Visual_Learning/integrate.py   --repo .   --check   --expect-build-materialized
```

The source patch modifies six shared source files and six standalone D&T lessons. The existing BUILD compiler then materialises the source into its 31 decks. GROW and LAUNCH lessons continue to load their maintained shared files.

## Rollback

Before commit:

```bash
python3 ASDAN_Visual_Learning/integrate.py --repo . --strip
python3 BUILD_ASDAN/_framework/apply_framework.py
```

After creating a patch, the patch may also be reversed through Git after its application has been checked:

```bash
git apply --check --reverse /tmp/asdan-visual-source-integration.patch
git apply --reverse /tmp/asdan-visual-source-integration.patch
```

## Why no separate loader is added to 85 files

A separate loader would create four problems:

1. a competing visual source beside the three existing maintained layers;
2. a new relative-path and offline dependency in self-contained BUILD decks;
3. a larger regression surface for print, timers, navigation and teacher controls;
4. a second injection mechanism that could drift from the estate’s content-integrity checks.

The source-owned approach keeps the current architecture authoritative.

## Baseline rule

`0002.BASELINE.txt` records the inspected baseline for review. It is not permission to apply blindly. Resolve the current checkout and run the exact patch generator. If the target shape has changed, stop and review the new source ownership rather than forcing a stale patch.

## Content classification

The marker-owned panel preserves the original file outside its markers, but its visible lesson-specific prompts are supplementary teaching content. It must therefore receive lesson-resource review rather than being described as a CSS-only or accessibility-only change. The existing content-integrity gates remain independent and are not edited by this integration.
