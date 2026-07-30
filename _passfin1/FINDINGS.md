# Pass FIN-1 — FINDINGS (record of a clean 459-file estate)

**Date:** 2026-07-30 · **Repo:** mattroper1977/lessons · **main SHA:** 654962529e74ecae01a642172dda0c378abb42c3 (unchanged; no fix shipped)

## Verdict
The reported "BUILD Humanities pupil content not populating" bug **did not reproduce**. The estate at
HEAD is clean of the reported defect class. No source fix was needed or made. This pass is a
measurement-and-record pass.

## What was measured
1. **§1 — 8 BUILD_HUM v4 lessons × 2 transports (http:// + file://) = 16 renders:** 0 script errors,
   0 page errors, every data-driven region populated (Arrival ×3, Starter, We Do sort+match, Independent,
   Lundy ×4, Exit ×3), every print-pack section populated, level-switch reveals all tiers. Screenshots:
   `_passfin1/shots_W1/`. The described `registerXP`/xp-chassis-organ failure family is **structurally
   absent** — these files contain no such symbols.
2. **§3.1 — full estate render sweep, 459 tracked *.html:** 84 flagged; **0 online-breaking code
   defects; 0 humanities failures.** All flags = blocked external hosts (Google Fonts ×75, YouTube
   thumbnails ×52, jsdelivr ×8, tailwind ×2, cdnjs ×1) or absolute-root shared assets (`/theme.js` ×2,
   resolve at the domain root like `/hud.js`). Full list: `SWEEP_FAILURE_LIST.md`. Matt's ruling: the
   11 offline functional breakers are all in `Games/` and `5_6 Local Choice/`, **outside staff-pack
   scope** — the list is a finding, not a work queue.
3. **§3.2 — resources.json:** valid JSON, 411 entries (active YEAR 2026-27 = 267), 0 missing active-year
   files, chip gate PASS across 21 subjects.
4. **§3.3 — frozen science:** Science_Teesside, biology, chemistry, "2 Physics 10" tree hashes
   **identical** to 2ce19ce.
5. **§3.4 — LL-INST-09 loop-mark spot sample:** 6 lessons (2 BUILD_ASDAN, 2 Build, 2 Science) × 3 tiers
   × 17 assertions PASS.
6. **§3.5 — sentinel universes:** 459 html at 88d6d32 = 459 at HEAD = 459 working. Unchanged.
7. **§3.6 — print parity (BUILD_HUM_W1, all tiers):** 8 populated print sections/tier, 0 empty.
   `print-lundy` absent from packs = **R-A07 `DIFFERENT_MODEL` (ruled RECORD, not a defect)** — adding
   `'lundy'` to printPack is the documented anti-pattern; untouched.

## Art follow-up (Matt's two pre-PACK-1 items)
- **Art_Teesside/Build print-pack population:** all 8 BUILD_ART W1–W8 PASS LL-INST-09 (17/17 × 3 tiers,
  9 sections on paper). 0 console failures. Offline-safe (only absolute ref is `/hud.js`).
- **Art ZIP verdict:** the committed pipeline `_passsci1/inputs/build_staff_pack.py` produces MadeByMatt
  offline BUILD Art copies **byte-identical to repo blobs except the intended hud.js `<script>` strip
  (−38 b)**; LL-INST-09 on the offline copies PASS. **The transform does not eat pack data.**
  **RECONSTRUCTION CAVEAT (quoted so it is not lost):** that pipeline's own docstring states it is
  *"rebuild of the pack builder that was never committed (404 on main)."* The AVAILABLE builder is
  proven clean; a lost original cannot be diffed. If a real-artefact zip predates this reconstruction,
  a later session must diff the actual zip. PACK-1's fresh build from the proven pipeline supersedes
  any older copy regardless.

## AMBERs (verbatim — see DECISIONS.md)
- `/hud.js` referenced by 218 tracked HTML files but absent from this repo; NOT a production defect
  (no CNAME → project page → absolute `/hud.js` resolves at the user-page domain root); bites only pure
  `file://`, where content still fully populates.
- (HUM-1) resources.json shelves the Humanities_Teesside SoW/Tracker/Packs under year=2025-26 though
  their content headers read "Autumn 1, 2026-27" and the 24 lessons they describe are tagged 2026-27.

## REDs standing
Frozen science untouched · assessed conditions blocks untouched · D&T v5 printPack lists untouched ·
no parked branch touched · no deletion · no unverified clips · no history rewrite · pupil data never handled.
