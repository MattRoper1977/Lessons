# NAV-1 · STAGE B PLAN — the rest of the estate, census → plan → STOP

**Nothing in this plan has been executed.** Stage A (the 35 new science
lessons + 3 suite indexes) and Stage A2 (the hub) are done; this document is
the census-derived proposal for everything else, waiting on **Matt's one-word
go**. Hundreds of files across a dozen chassis generations is exactly the
blast radius that stays behind a human gate.

## The way-home census (read-only, derived 2026-08-12)

Mechanisms found: **hud.js** (a shared header script, referenced by ~250
files; it lives at the DOMAIN root, so it resolves live on madebymatt.uk but
404s under `file://` and in offline packs — recorded as a property of the
mechanism, not a defect) · **explicit home link** (rare — `primary/` and two
root pages only) · **nothing**.

| Population | Files | Way home today | Verdict |
|---|---|---|---|
| `Science_Teesside/*/v3_40min` (35 lessons + 3 indexes + windows/guides/matrices) | 58 | **← Lessons control (Stage A, this pass)** on lessons + indexes | **DONE** |
| `Science_Teesside/{Build,Grow,Launch}` v5 originals | 25 | hud.js 25/25 | HAS (also frozen — never touched) |
| `primary/` | 53 | hud.js 46 + 7 explicit links | HAS (mixed; 0 with neither) — verify tail |
| `Art_Teesside/` | 53 | hud.js 31/53 | **LACKS in 22** (evidence packs, windows, printables) |
| `BUILD_ASDAN/` | 39 | hud.js 31/39 | **LACKS in 8** |
| `GROW_ASDAN/` | 24 | hud.js 18/24 | **LACKS in 6** |
| `LAUNCH_ASDAN/` | 38 | hud.js 30/38 | **LACKS in 8** |
| `Tutor_Time/` | 17 | hud.js 10/17 | **LACKS in 7** |
| `5 Intervention 10/` | 7 | hud.js 5/7 | **LACKS in 2** |
| `Build/`, `Grow/`, `Launch/` (top-level, non-science) | 67 | hud.js 30/67 | **LACKS in 37** |
| `Humanities_Teesside/` | 25 | none | **LACKS 25/25** |
| `6 Art/` | 18 | none | **LACKS 18/18** |
| `ASDAN/` + `ASDAN_Lundy/` | 35 | none | **LACKS 35/35** |
| `BUILD_Estate_v3/`, `GROW_Estate_v3/`, `LAUNCH_Estate_v3/` | 157 | none | **LACKS — but see the generated-tree caution below** |
| `5_6 Local Choice/` | 16 | hud.js 1/16 | **LACKS in 15** |
| `Assembly/`, `DT_Community_Upcycling/`, `build-engine/`, misc | ~30 | none | **LACKS** (low priority; several are staff-facing) |
| `biology/`, `chemistry/`, `2 Physics 10/` | 37 | (1 hud in Physics) | **EXCLUDED — frozen legacy science** |
| ★assessed files (2: `GROW_Estate_v3/Humanities…W7_Write_the_Account`, `LAUNCH_Estate_v3/Humanities…W7_Source_Assessment`) | 2 | — | **EXCLUDED — byte-identical or stop** |
| `Games/` | 31 | hud.js 28 | **EXCLUDED** (own governance, CLAUDE.md) |
| `LundyLoop/` | 33 | — | **EXCLUDED — staff docs** |
| `Baseline_Weeks/` | 8 | — | **EXCLUDED — standalone assessment context (report only)** |
| Root pages (`YearPlan`, `_huclose`, `_approved0805`, etc.) | ~10 | 2 have links | EXCLUDED — staff/records surfaces |

Populations that HAVE hud.js keep it; consistency is not a reason to double up.

## Generated-tree caution (derive before editing)

`{BUILD,GROW,LAUNCH}_Estate_v3/` mirror `Art_Teesside`/`*_ASDAN`/
`Humanities_Teesside` content and a CI workflow named "GROW LAUNCH v3
generated-tree verification" exists. **Before any Stage B edit there, derive
whether those trees are generator-owned** — an edit to a generated file is
overwritten or trips the byte-check. If generator-owned, the fix belongs in
the generator, which is a different pass.

## Insertion method per chassis dialect

1. **v3-family slide decks** (fixed `.controls` bottom bar, `section.slide`,
   one `</style>`): the Stage A pattern verbatim — fixed top-right
   `.mbmhome` anchor, derived relative path, print-hidden, byte-region guards.
   Populations: Humanities_Teesside, Art_Teesside teaching decks, *_ASDAN
   teaching decks, Tutor_Time decks.
2. **Static hub/index/evidence pages** (scrolling documents): the Stage A
   index pattern — in-flow `.mbmhome` at the top of `<body>`.
3. **Pre-v3 decks** (`6 Art/`, `5_6 Local Choice/`, `Build/Grow/Launch`
   non-science): chassis varies file-by-file — geometry must be re-derived
   per family (the §2.1 method: find the fixed chrome, probe the clear
   corner at 3 viewports). Do NOT assume the v3 seat.
4. **hud.js-bearing files**: untouched.

## Gate battery per changed file (the Stage A battery, verbatim)

- Real-Chromium boot, zero console/page errors; button present and clickable
  on first/middle/last slide; target path resolves in the repo tree.
- Geometry: no bounding-box intersection with any visible interactive
  element at 1280×800, 390×844, 844×390.
- Contrast read from computed style.
- Rendered print text identical to the pre-edit file (print-media emulation).
- Byte-region guards before the write: closure / close block / witness /
  print pack / tiers / word banks / external URLs, where present.
- Runtime census zero (storage/network/forms/assets/media queries).
- Sentinels 50 / 123 set-identical after every batch.
- One commit per population; populations sequenced smallest-risk first
  (Humanities_Teesside → *_ASDAN gaps → Art_Teesside gaps → Tutor_Time →
  pre-v3 families each behind its own geometry derivation).

**Estimated blast radius if everything above is approved: ~180–230 files**
(excluding the Estate_v3 trees pending the generator derivation; ~340 with
them).

**STOP. Nothing below the Stage A/A2 line lands without Matt's one-word go.**
