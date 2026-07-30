# OVERVIEW_DIFF.md — non-lesson artefacts across BUILD / GROW / LAUNCH ASDAN

**Pass LA, Phase 1.** BASE `6945c223…`. **Method:** full recursive enumeration of
`BUILD_ASDAN/`, `GROW_ASDAN/`, repo root, and a case-insensitive `*launch*` sweep — every
path below is verbatim, none assumed. This table answers Matt's "extra overview doc"
question by measurement; **Matt picks at the STOP gate which doc(s) to replicate** for GROW
and LAUNCH.

---

## 1 · The three-column artefact table (non-lesson docs only)

| Artefact | BUILD_ASDAN | GROW_ASDAN | LAUNCH_ASDAN |
|---|---|---|---|
| **Pathway hub** | `BUILD_ASDAN/BUILD_ASDAN_Hub.html` | `GROW_ASDAN/GROW_ASDAN_Hub.html` | — (no folder yet) |
| **Scheme of Work** (standalone) | `BUILD_ASDAN/Scheme_of_Work.html` | — *(folded into Scheme_and_Resources)* | — |
| **Resources & Tools** (standalone) | `BUILD_ASDAN/Resources_and_Tools.html` | — *(folded into Scheme_and_Resources)* | — |
| **Combined Scheme + Resources** | — *(kept as two files)* | `GROW_ASDAN/Scheme_and_Resources.html` | — |
| **START_HERE** (one per slot) | 5× `START_HERE.html` | 3× `START_HERE.html` | — |
| **Root entry file** | `build_asdan.html` | — | — |
| **Printable evidence / witness pack** (standalone file) | NONE | NONE | — |
| **Overview / tracker doc** | NONE | NONE | — |

Lesson counts (context): BUILD_ASDAN **31**, GROW_ASDAN **18**, LAUNCH_ASDAN **0**.

---

## 2 · What BUILD has that GROW / LAUNCH lack (the BUILD-only column)

Three BUILD-only artefacts, all verified by enumeration:

1. **`BUILD_ASDAN/Resources_and_Tools.html`** — a *standalone* resources/tools list
   (`Resources & Tools List — BUILD Programme`). **This is the brief's headline candidate,
   and it is confirmed:** no GROW or LAUNCH sibling exists. GROW has no dedicated resources
   file at all.
2. **`BUILD_ASDAN/Scheme_of_Work.html`** — a *standalone* scheme-of-work page
   (`BUILD ASDAN — Scheme of Work (Studio Decks)`). GROW folds its scheme into the combined
   `Scheme_and_Resources.html`; BUILD keeps scheme and resources as **two separate files**.
3. **`build_asdan.html`** (repo root) — a pathway landing/entry page (`BUILD Pathway —
   Autumn 2026`). Neither `grow_asdan.html` nor `launch_asdan.html` exists.

## 3 · What GROW has that BUILD lacks (the mirror direction)

- **`GROW_ASDAN/Scheme_and_Resources.html`** — a single *combined* scheme+resources doc.
  BUILD has no combined file; it splits the same content across items 1–2 above. So the two
  pathways differ in **packaging**, not in whether the information exists: BUILD = two files,
  GROW = one merged file.

## 4 · What NEITHER BUILD nor GROW has (relevant to brief §5)

- **No standalone printable evidence/witness pack file.** In both pathways the Assessor
  Witness Statement lives **inside each lesson's own print pack** (`#print-witness`, wired
  into the `printPack` id array), not as a separate document. Brief §5 lists "printable
  evidence pack" among LAUNCH entry points "mirroring whatever the Phase-1 inventory shows
  GROW actually has" — **inventory shows GROW has none as a standalone**, so the witness
  stays per-lesson for LAUNCH too. (No contradiction: the brief defers to the inventory.)
- **No overview / progress-tracker doc** in either ASDAN pathway. (The only printable
  evidence packs in the repo belong to the *Teesside* pathways, e.g.
  `Humanities_Teesside/LAUNCH_Printable_Pack.html` — not ASDAN, reference-only.)

---

## 5 · The replication menu for Matt (pick at the STOP gate)

Whichever doc(s) Matt selects will be built for **GROW and LAUNCH**, generated **from the
lesson files themselves** (Pathway-Tracker principle: regenerate, never hand-invent), with
**LAUNCH's built last** (after its lessons exist). Options, most-to-least self-contained:

- **Option A — Standalone `Resources_and_Tools.html`** (the headline). Give GROW and LAUNCH
  their own resources/tools list, matching BUILD. *Lowest risk, directly answers the "extra
  overview" question.*
- **Option B — Standalone `Scheme_of_Work.html`.** Split GROW's (and author LAUNCH's) scheme
  out of the combined file, matching BUILD's two-file packaging. *Note: for GROW this means
  refactoring the existing combined file — more invasive; would touch a live GROW file.*
- **Option C — Root entry file** `grow_asdan.html` / `launch_asdan.html`, matching
  `build_asdan.html`. *Landing pages; small, additive, no existing file touched.*
- **Option D — New overview/progress-tracker doc** for all three (a doc type neither
  pathway currently has). *Largest new surface; only if Matt wants a genuinely new artefact.*

**Recommendation (for discussion, not decided):** **A + C** — both are purely *additive*
(no existing GROW file is refactored), both regenerate cleanly from lesson files, and
together they give GROW and LAUNCH parity with BUILD's standalone resources list and root
entry page. Option B is deferred because it would refactor a live GROW file; Option D only
if a new tracker is wanted. **Matt decides.**
