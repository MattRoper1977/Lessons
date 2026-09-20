# Final pass on the Reviewed packs — 2026-09-19 (Claude, in chat)
Base: Matt's *_Reviewed.zip set (third-party review of my 2026-09-19 build). Content, sources, Word/PDF/PPTX/MP4 files: unchanged.
Changed in every *_Lesson.html (106):
1. Varied exit quick-check restored. The review rebuilt the exit stage and dropped the #vary-exit block, so all exits had gone back to two typed questions. Block re-inserted above the route buttons (confidence / pick the word / word of the lesson / true-false, rotating by week). Screen only; print unchanged.
2. Card-round shared activity polished: gaps between control buttons, 48px targets, the chosen option now shows a tick and an outline, secondary controls are outlined so the answer choices stand out.
Changed in the 14 Humanities Autumn 2 BUILD/GROW lessons only (the review recovered these from an older pack, so they had none of my earlier fixes): varied starter block added, BUILD green hover fixed, duplicate ids in repeated map SVGs removed, vary CSS/JS added.
Removed: 11 *_Data.xlsx.inspect.ndjson tool artefacts. SHA256SUMS.txt regenerated in every pack.
Verified in Chromium, desktop 1280x720 and phone 390x844, all 106: 0 JS errors, 0 duplicate ids, 0 controls off-screen, 9 stages, 40 minutes, starter and exit blocks populated and responsive. 318 PDFs, 106 PPTX (notes on every slide) and 212 DOCX open.
NOT in this set: Humanities Autumn 1 BUILD + GROW (14 lessons). The uploaded HUM_Autumn_1_BUILD_GROW_Reviewed.zip was truncated (48 KB) and cannot be opened. See HUM_Autumn_1_BUILD_GROW_Fallback.zip and ORDER HUM-D4.


## Proof pass 2026-09-19 (HUM-D5 Part A, Claude)
Class A (mechanical) fixes applied by _passhumd5/apply_proof.py from replacements.json: **8 edits in 8 files** (house spellings, broken joins after "means", missing spaces after punctuation, doubled full stops, DOCX heading punctuation restored). Meaning-bearing items are ledgered in _passhumd5/PROOF_LEDGER.md, not changed.
PDFs re-rendered from the proofed sources: 4 (Pupil_Resources / Knowledge_Organiser, Chromium A4).
SHA256SUMS.txt regenerated (yes).

### Rulings applied 2026-09-19 (HUM-D5 Part A, Matt's H-rulings, Claude)
- H2 (B0002, arrival reminder strip): "Previous lesson reminder: <answer>" -> "Previous lesson reminder:" on every surface that carried it - 20 edits in 20 files in this pack; 20 PDFs re-rendered (Chromium A4). W01 lessons (word help) untouched, held by lesson id.
- H5 (B0123/B0124/B0127-B0129): one token or template change per pack, never per-file authoring - 42 edits in 12 Lesson.html files in this pack: LAUNCH primary button token --btn-bg #3b82f6 -> #2563eb (5.17:1); BUILD/GROW timer ink in the #auto-timer rule pair #c9803b -> #985719 (5.66:1); the rank-criterion select bound to its visible label (l.htmlFor); every static map/diagram <svg role="img"> given an accessible name (maps: role=group so their focusable place buttons are no longer nested inside an image). B0008 (43.5 px buttons) was the instrument reading a rect mid-animation: at rest every button is 44 px, no edit.
- H6: config.sehm (the one population string, 106 carriers) inserted into the 7 GROW_A1 Fallback configs only; nothing authored.
- SHA256SUMS.txt regenerated after these edits.

### Rulings applied 2026-09-20 (ORDER HUMD5-B, D1 + D2)
- D2 (B0125, model-node ribbon contrast): ONE rule per pack binds the existing --text token - `.step-ribbon>*` gains `color:var(--text)` - in 12 Lesson.html here. White on the I-do background was 1.23:1 (BUILD/GROW #f3e6da) and 1.19:1 (LAUNCH #ede9fe); it is now 11.98:1 and 12.36:1. Measured collateral across all 120 lessons: 284 .step-ribbon containers, 1124 direct children, 480 changed ink and every one of them is a model-node BUTTON (4 per lesson); the 644 evidence-card articles were already --text, and nothing in a print section changed.
- D1 limb (a) (B0004-B0005, surface the row that exists): 6 Pupil_Resources.html here gain a Source line under the map image, quoting the Sources_and_checks row and the in-image wording (Natural Earth terms of use, or OpenStreetMap contributors). 6 Pupil_Resources.pdf re-rendered (Chromium A4) and the line proved present in the extracted PDF text.
- D1 limb (b) (no row exists): Sources_and_checks.html gains 7 review rows naming each image and its lessons - Object_Picture_Choices.png (61), three Teaching_Visual_1.png variants (7 + 2 + 2), Visual_Resource.png (64, rendered by no surface), and the two Transporter Bridge photographs. The first five read "source not recorded - review before external distribution"; the two photographs instead RECORD the credit that already exists on their rendering surface (figcaption: Oliver Dixon CC BY-SA 2.0 / Reading Tom CC BY 2.0), because writing "not recorded" there would be false. That deviation from the ruling's wording is named here so it can be overruled. No image was removed or replaced.
- SHA256SUMS.txt regenerated after these edits.
