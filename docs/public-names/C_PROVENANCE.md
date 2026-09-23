# C · product names off public pages (ruling 2026-09-23)

Every changed file with its sha256 before and after is in `C_PROVENANCE.json` beside this file.

- **91 loop-transplant decks** (80 Humanities, 11 Science): `tools/hum/loop_adapter.py --retext` rewrote only the
  adapter's own TA-layer strings, rebuilt exactly as it had emitted them. "Evidence on Earwig" becomes "Evidence on the school's
  digital evidence platform" (583). "Earwig clip" becomes "evidence clip" (151). The label `ta-earwig` "Earwig, lean capture (E):"
  becomes `ta-evidence` "The school's digital evidence platform, lean capture (E):" (94). Each deck equals its prior bytes with
  only those substitutions. Census matches in them: 922 → 0 (828 visible + 94 class names).
- **Biology observation lesson**: the visible text changed in 6 places, to "the school’s digital evidence platform" and "evidence clip".
  **Retained on purpose, internal identifiers that are not displayed:** the saved-setting value `value="EFL clip"` and its
  comparison `v==='EFL clip'`, and the saved per-pupil state property `efl` (`efl:false` ×6, `p.efl` ×5, `].efl` ×2). All are
  stored in localStorage `ps_co2_final_observation_v1`; renaming them would lose teachers' saved records. The names gate
  allows exactly these counts and goes red if any count moves.
- **24 of 26 served weekly-plan workbooks** (`Planning/*/*.xlsx`): 80 occurrences of "EFL" in 72 cells, changed to "evidence platform"
  by `tools/public_names/xlsx_evidence_platform.py`, in cell text only. Formulas, styles, sheet structure and every other
  package part are byte-identical, verified cell by cell with openpyxl. The edit is made at XML level because an openpyxl
  load/save, even with no change, rewrites 11 of 12 parts and drops `xl/sharedStrings.xml`. The 2 ASDAN year plans carried no name.
- **Not changed:** 2 decks matched "EFL" only inside base64 image data (HUM_Spring_2 … BUILD_S2_W02_Lesson.html, RE_Autumn_BUILD …
  BUILD_RE_A2_W03_Lesson.html); the names gate skips `data:` URIs.
