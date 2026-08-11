# GROW + LAUNCH Estates v3 — Decisions

Sentinel: `grow-launch-estate-v3-deploy-2026-08-10`

Branch: `claude/gl-estate-v3`

ROLLBACK_SHA: `1e8a428b523d1b970a8a3a2ab2a99f48a8271d09`

## Identity and input gates

- Target repository is `MattRoper1977/Lessons`.
- Identity gate passed 7/7 at ROLLBACK_SHA.
- `BUILD_Estate_v3/` exists and `_finish/ROUTES.md` exists.
- No prior `GROW_Estate_v3/`, `LAUNCH_Estate_v3/`, `_glv3/DECISIONS.md`, or `claude/gl-estate-v3` existed before this run.
- Inputs: `GROW_ESTATE_v3_REPAIRED_2026-08-10.zip` and `LAUNCH_ESTATE_v3_REPAIRED_2026-08-10.zip`.
- GROW derives to 34 deployable lessons: Art 8, Humanities 8, ASDAN 18. Science folder absent. Repaired print tier present in 16 lesson files (Art 8 + Humanities 8). Audit contains the final `Post-verification edits applied 2026-08-10` section.
- LAUNCH derives to 46 deployable lessons: Art 8, Humanities 8, ASDAN 30. Science folder absent. Repaired print tier present in 8 lesson files (Humanities 8). Audit contains the final `Post-verification edits applied 2026-08-10` section.
- Total deployable lessons: 80. Screen-only lessons: 56 (GROW ASDAN 18 + LAUNCH ASDAN 30 + LAUNCH Art 8).

## Standing rulings

- Install one labelled parallel GROW estate and one labelled parallel LAUNCH estate. Existing lessons remain the default.
- Live files are RED: do not edit, move, rename or delete anything in `Art_Teesside/`, `GROW_ASDAN/`, `LAUNCH_ASDAN/`, `Grow/Slideshows/`, `Launch/Slideshows/`, `Science_Teesside/`, `Humanities_Teesside/`, `Baseline_Weeks/`, or `BUILD_Estate_v3/`.
- Extend `_finish/ROUTES.md`; do not create a rival route map.
- No Arts Award Part or Silver Unit tag changes.
- No Arts Award hours threshold.
- No inferred PEQ unit codes, credits, levels or criterion mappings.
- No L2 registration claim.
- No `new art form` claim.
- Do not author a print pack for the 56 screen-only lessons.
- D4 LAUNCH W3L1 arrival prompts and D5 Baseline Pathway A/B placeholder remain untouched.
- Any similar unmapped placeholder stays explicitly marked and empty.

## A1 — screen-only routes

The 56 screen-only lessons are an accepted AMBER state for this run, not a defect to repair. Each affected route hub must state: `This route is screen-only. Printable pupil work, portfolio evidence and ASDAN assessment records come from the existing lessons.`

Retiring any live GROW or LAUNCH ASDAN suite would remove the Assessor Witness Statement and the T2-4 learner-confirmation line from PEQ delivery. Retiring live LAUNCH Art would remove the only printable Silver portfolio route.

## A2 — PEQ mapping

The v3 ASDAN lessons use `PEQ` but do not name PEQ unit codes. Report live-vs-v3 mappings from the repository; do not close gaps by inference. Any `STILL-UNDETERMINED` mapping remains undetermined.

## A3 — Arts Award tags

Report only; change nothing:

- GROW Bronze: W2 live A+D vs v3 A; W4 live A+B vs v3 B.
- LAUNCH Silver: W1–W7 mirror live; W8 live all five ranges vs v3 Unit 2E only.
- Confirm GROW W5 and LAUNCH W2 produce organisation evidence artefacts, not merely teaching references.

## Derived live Humanities paths

GROW:

- `Grow/Slideshows/GROW_HUM_W1_Time_Detectives.html`
- `Grow/Slideshows/GROW_HUM_W2_Source_Detectives.html`
- `Grow/Slideshows/GROW_HUM_W3_Cause_And_Consequence.html`
- `Grow/Slideshows/GROW_HUM_W4_People_Who_Shaped_Britain.html`
- `Grow/Slideshows/GROW_HUM_W5_Significance.html`
- `Grow/Slideshows/GROW_HUM_W6_Plan_The_Account.html`
- `Grow/Slideshows/GROW_HUM_W7_Write_The_Account.html`
- `Grow/Slideshows/GROW_HUM_W8_Where_In_The_World.html`

LAUNCH:

- `Launch/Slideshows/LAUNCH_HUM_W1_Source_Investigation.html`
- `Launch/Slideshows/LAUNCH_HUM_W2_Cause_Consequence_Courtroom.html`
- `Launch/Slideshows/LAUNCH_HUM_W3_Archive_NOP.html`
- `Launch/Slideshows/LAUNCH_HUM_W4_Century_Of_Change.html`
- `Launch/Slideshows/LAUNCH_HUM_W5_People_Modern_Britain.html`
- `Launch/Slideshows/LAUNCH_HUM_W6_Structured_Account.html`
- `Launch/Slideshows/LAUNCH_HUM_W7_Source_Assessment.html`
- `Launch/Slideshows/LAUNCH_HUM_W8_OS_Map_Skills.html`

## Spec contradiction noted

§9.1 says `6/6`, while §0 defines seven identity checks and says `7/7 or stop`. This run uses 7/7.

The phrase `audit .md ends with "Post-verification edits applied 2026-08-10"` is treated as the final audit section heading: in both repaired ZIPs that heading is present near the tail and is followed by the repair verification text; it is not literally the final line.

## Deterministic Humanities print-surface reconstruction

- The repaired completion audits classify 24 lessons as print-bearing: GROW Art 8, GROW Humanities 8 and LAUNCH Humanities 8.
- The sixteen repaired Humanities source files carried the print CSS/function markers but contained zero actual `.proute` elements.
- The generator creates only the missing print wrapper, copying the same lesson's already-authored Independent `.route.s`, `.route.m` and `.route.h` contents into Supported/Standard/Stretch `.proute` surfaces and reusing its authored Independent mission. No new teaching content is authored.
- All 24 print-bearing files use one lowercase `support` / `standard` / `stretch` data-tier contract and clear it only on `afterprint`. The 56 accepted screen-only lessons remain untouched and receive no print pack.

## Source-authored PEQ code provenance

- Exact repaired input contains PEQ code wording in 6 of the 48 deployable ASDAN lessons; all are LAUNCH PEQ lessons carrying source-authored `ComSk1` in qualification/boundary wording.
- Every write to a generated ASDAN lesson is checked against the exact source code-count map. New/inferred PEQ code drift is RED.
- A code mention is not treated as a criterion mapping; the live Evidence Binder/authorised mapping remains necessary where criterion mapping is not explicitly stated.
- Source wording is preserved rather than deleted to manufacture a zero-code result.

## Measured execution results

- Static gates executed against ROLLBACK_SHA `1e8a428b523d1b970a8a3a2ab2a99f48a8271d09` and the generated branch worktree.
- Catalogue union: base 552 + new 88 = final 640.
- `_finish/ROUTES.md` extended with six GROW/LAUNCH rows; no rival route map created.
- No root `sitemap.xml` exists at rollback, so none was invented.
- Sentinel expected deltas derived before copy: loop 0, closure 0.
- All live RED trees are blob-identical to rollback after install.
- Browser boot/print/chip/contact-sheet results are appended by the browser gate before commit.

## Complete-universe filename-reference finalisation

- Count reconciliation proves 80 deployable source lesson paths carried the authorised `_OUTSTANDING_V3_TEST` filename token.
- Four generated same-day evidence-window support pages contained the expected 64 embedded source-filename references after their lesson-copy stage. The generation pipeline removed only that exact token from those references.
- The complete 94-page generated HTML universe was then scanned at zero residue, and every quoted HTML reference in the four support pages resolved.
- The LAUNCH ASDAN support page deliberately retains 30 repository-rooted source-provenance references to the protected installed tree; these were resolved separately from its generated page-relative lesson links.

## Embedded test-filename reference normalization

- The count reconciliation proves exactly 80 deployable source lesson paths carried the authorised `_OUTSTANDING_V3_TEST` filename token.
- Deterministic candidate generation removed that token from output filenames, links and embedded filename references before browser verification.
- Browser verification independently rechecked all installed estate HTML and found 0 output occurrence(s).

## Browser execution results

- Browser boot: 94 new HTML files, 0 console/page errors.
- Print browser gate: 24/24 repaired route-bearing lesson files passed; 56 screen-only lessons remained screen-only by the static gate.
- Catalogue browser gate: all 88 new resources are reachable through active 2026-27 + their existing chip; advertised = rendered = JSON-derived count. Catalogue-shell diagnostics are kept separate from the 94-page estate boot gate.
- Contact sheets: 80 per-lesson PNGs plus combined Art, ASDAN and Humanities sheets under `_glv3/contact_sheet/`.

## Chip-count browser gate

- Art · Teesside Studio Suite: advertised 81 = returned 81 = JSON-derived 81 in active 2026-27; all 18 GLV3 additions on the chip are reachable.
- GROW Vocational & PfA: advertised 42 = returned 42 = JSON-derived 42 in active 2026-27; all 20 GLV3 additions on the chip are reachable.
- Humanities: advertised 59 = returned 59 = JSON-derived 59 in active 2026-27; all 18 GLV3 additions on the chip are reachable.
- LAUNCH Vocational & PfA: advertised 68 = returned 68 = JSON-derived 68 in active 2026-27; all 32 GLV3 additions on the chip are reachable.
