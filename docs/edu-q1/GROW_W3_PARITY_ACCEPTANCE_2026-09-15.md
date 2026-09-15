# EDU-Q1 — Friction native parity, records and all-stage acceptance checkpoint

15 September 2026. **Draft continuation of the Friction pilot; still unmerged, unpublished and not yet human-AT tested.** Continues from Lessons draft #538 head `1fa3ab94712bef3320c625000de9e978f8cf3d7c` (tree `2a707b06f73152f9ca538d52029872414e1704be`) on base main `929cf731173aeca8c9941cecd76cb350387499d1`. This checkpoint was developed on branch `claude/made-by-matt-handoff-ycul48`, which starts from that exact head; it has not been pushed to the #538 branch.

All nine handoff hashes were verified against the #538 head before any work. Matt remains on High. The old live URL still serves the previously published lesson; nothing here is live.

## 1. Editable slides and slide PDFs (W3A 12 → 17 slides, W3B 15 slides)

`tools/grow_resources/author_w3_slides.py` rebuilds both decks from the exact 6 September bytes at the review base. Every new shape is a deep copy of a reviewed shape, so fills, fonts, insets and the footer/brand furniture are unchanged. Content comes from the same JSON that authored the screen and the DOCX/PDF.

- **W3A**: the single three-line arrival becomes three route slides (2–4), each with the same four questions as the screen and pupil pages 7–9, the access line and staff answers in the notes only. Two knowledge-organiser reference slides (6–7, 0 minutes) carry the objective, success criteria, five key words, key ideas, the labelled sliding-box model statement, helpful/unhelpful examples and the fair-comparison reminder (pupil page 10). The sort slide (13) carries the lesson's one optional help line; its notes give the Space/Voice/Audience/Influence guidance and the eight-plus-two minute split. A two-check exit slide (16) lists both checks for each route with the explanations in the notes only, and the closing slide names **Friction: test the surfaces**. We Do 2 notes are re-timed 3 + 2 + 2 + 2 + 1 = 10 minutes; the seven stages still total 40. Pupil page references now name pages 2, 6, 7–9, 10 and 11–13.
- **W3B**: slide 13 (the old Lundy Loop) becomes **Review the evidence**: intro, three steps, close line and the optional help line, with the staff guidance in the notes. Slide 2 names the Lesson A prediction. The 32 + 4 + 4 plan is unchanged; the W3B exit slides are unchanged. The next lesson is named in the final notes.
- No slide or note in either deck contains a day, period or clock time. Historical conversion citations are retained as historical; changed notes carry a 15 September revision line.
- Slide PDFs were rendered with the same renderer family as the shipped PDFs (LibreOffice 24.2 with Carlito). Rendering the unchanged 6 September decks locally and comparing with the shipped PDFs differed by under 0.6 % of pixels per page (anti-aliasing). Against that same-renderer baseline, **all 22 unchanged slides (9 in W3A, 13 in W3B) render pixel-identical**; the 8 new or changed W3A pages and 2 changed W3B pages were rendered and visually reviewed, and fixed defects (leftover template paragraphs, a wrong clone source, duplicated "optional") before finalising.

## 2. Resource pages, START_HERE and the combined pupil pack

- `resources/GS_W3A.html` and `GS_W3B.html`: schedule and period-link wording is now *Lesson A · 40 minutes* / *Lesson B · 40 minutes* and *Lesson A resources* / *Lesson B resources*; no day or clock words remain. `CONTENT.json` records the same values. The other eight resource pages are byte-identical (the committed pages differ from a full generator rebuild for unrelated reasons, so only exact string edits were applied). `check_resources.py` passes.
- `W3A/START_HERE.txt` names the pupil page set (1–2, one of 3–5, cards 6, one of 7–9, organiser 10, one of 11–13, two tickets per sheet, screen or paper once) and the deck alignment; `W3B/START_HERE.txt` states the 32 + 4 + 4 plan with no separate feedback form. Both carry revision 2026-09-15.
- The combined pupil pack (default print selection) is **6 A4 pages for each route** in both delivery modes; every page has text and it contains no staff answer, witness or marking section. All 46 individual print outputs (13 sections, route-specific ones in all three routes) are one A4 page each. The Standard pack's six pages were visually reviewed: the arrival grid moves whole to the page after its heading, which is cosmetic and recorded, not fixed.
- The teaching-pack offline HTML companions under `Teaching_Packs/GROW/HTML`, `Resources`, `Teacher_Notes.html`, `Pupil_Resources.html` and `GROW/index.html` still reflect the 6 September lesson (they mention the old Lundy stage). They have no generator in this repository and are not members of any manifest or ZIP; they are left byte-identical and are an open item for the lane that produced them.

## 3. Lesson repairs found by the all-stage acceptance (source changed)

The acceptance harness ran on every one of the ten stages, which the earlier scoped suites did not, and found pre-existing defects that also exist on main. Fixes are CSS or attribute-level except where stated:

- **No JavaScript**: previously one visible slide and no organiser. A `<noscript>` style and note now show all ten stages in order, open every arrival and exit route, show the print organiser, hide the JavaScript-only widgets and keep tables inside scroll regions. Verified at 320 and 1280 px: 10 stages, 12 arrival questions, 6 exit legends, organiser visible, no horizontal overflow.
- **Phone-width layout**: the Independent Work results table (548 px of unbreakable underscores) and a 20 px hidden overflow on the title slide are fixed (`overflow-wrap:anywhere`, hidden horizontal slide overflow, clipped decorative dots); sort bins may shrink under 200 % text.
- **Colour contrast**: the route buttons (white on `#22c55e` 2.3:1 and `#f97316` 2.8:1), route headings, the auto-timer amber (3.2:1), the success-criteria gold (2.0:1), the story-strip greys (2.3:1 and 4.3:1) and the small bold "observe" labels and caption on steel blue (4.2:1) now use deeper shades of the same hues (`#15803d`, `#c2410c`, `#8a5622`, `#7a5a12`, `#475569`, `#334155`, `#35657e`). Pathway identity and the classroom chassis are preserved.
- The labelled ramp figure's inner SVG is marked decorative (its container already carries the accessible name); the surface-test diagram host is a focusable named region; the slide container is the `main` landmark.
- The screen and print WAGOLL now read "transfers movement energy to heat and slows the wheel", the wording the teacher pack and deck already used.

Arrival, organiser, exit, help-prompt and review components, all stage timers and the W3B boundary are unchanged. Remaining axe results are moderate only: `region` for the fixed timer/XP/progress widgets, `page-has-heading-one` on non-title stages (the H1 lives on the title slide) and `heading-order` for the success-criteria H3; these are recorded, not hidden.

## 4. Records and admission

- `refresh_w3_pack_records.py`: `SOURCE_MANIFEST.json` W3A/W3B file sizes, digests and revision (2026-09-15; manifest revision 2026-09-15, W4–W7 unchanged); the seven archives that carry Week 3 content rewritten from their committed member maps with the builder's fixed timestamps (the twelve other archives are byte-identical; a full rebuild would have changed every archive because of a different zlib and would have added post-6-September lesson folders to the whole-pack archive); `SHA256SUMS.txt` existing rows only; `Teaching_Packs/index.html` and the download bindings through `build_hub`. `check_packs.py` and `test_source_binding.py` pass.
- `tools/easter/SCIENCE_ORIGINAL_TARGETS.json` pin moved with `sx2_move_pins.py`; `data/resource-sizes.json` rewritten with `resource_sizes.py --write`; `SCIENCE_WEEK_BINDINGS.json` Friction digest re-cut with a reviewed note and an unchanged calendar binding; only the Friction entry of `TERM_AND_STYLE_EVIDENCE.json` replaced from the generator (a full regeneration changes 213 unrelated entries on main too); `lesson-order.json` rebuilt and `--check` passes; `check_catalogue_static.py` fails identically on main ("Every committed resource row has additive metadata") and is a pre-existing condition.
- `admit_w3_friction.py`: a 28-file GROW W3 replacement transaction (canonical lesson, two resource pages, fourteen native and START_HERE files, three pack records, seven archives, the download hub) written into `_glv3/tools/verify_change_boundary.py`, which now judges named transactions (Sugar and GROW W3) with the same exact-blob, exact-bytes, owner-pin and negative-control rule; four new reviewed paths added to `pin_catalogue_contract.py`; `CATALOGUE_PINS` re-pinned with that helper (468 files, 734 original rows preserved, 116 derived pack rows; the Apps copy of the gate is out of this repository's scope and must be brought level by the Apps owner as with Sugar #103); PIN1 triggers regenerated and checked (481 per event).

## 5. Evidence

| Check | Result |
|---|---|
| All-stage acceptance (`friction_acceptance.py`) | 120 stage cases (standalone and local HTTP × 320/390/768/1280 reduced motion, 390/1280 default motion × 10 stages): zero serious/critical axe violations, no horizontal overflow; 108 keyboard transitions with heading focus (embedded models step first on stages 3, 5, 6, 7, by design); 8 enlarged cases (200 % zoom at 1280, 320 px reflow at double density, 200 % text at 1280 and 390); dark scheme and forced colours (contrast recorded, not asserted under forced colours); no media in the lesson, resource clips have controls, no autoplay, `preload="none"`; 4 no-JavaScript cases; 46 one-page prints; 6 six-page packs; zero page errors |
| Regression suites on the final bytes | focus 162 (0 errors); arrival 24 cases, 12 one-page prints; organiser 56, exit 24, 10 prints, 32 axe runs; feedback 16/8/8/16 axe/4 prints/6 pack selections; all zero errors |
| Decks | 22 unchanged slides pixel-identical; 10 changed/new pages reviewed; both decks open, unique shape ids, checksum-clean ZIPs |

Reproduce from the repository root with the installed Chromium, PyMuPDF and axe-core:

```sh
NODE_PATH=/path/to/node_modules python3 tools/grow_resources/friction_acceptance.py . /path/to/review/acceptance
python3 tools/grow_resources/author_w3_slides.py            # decks from the review base
python3 tools/grow_resources/refresh_w3_pack_records.py     # manifests, archives, checksums, hub
python3 tools/grow_resources/admit_w3_friction.py --check   # transaction, pins, PIN1 (the apps.json stand-in makes --check report differing pins; --write restores that pin)
```

## 6. Candidate hashes

| File | SHA-256 |
|---|---|
| `Science_Teesside/Grow/SCI_G_W3_Friction.html` | `508f1967b6481671dafb149d7177b620b194074312cee0dbdd30553c166b634a` |
| `W3A/GROW_Science_Autumn1_W3A_Friction.pptx` | `13dceb4a32f65165df9353349a69c87465e7f33b9f941036f8f714fd10a9f9da` |
| `W3A/GROW_Science_Autumn1_W3A_Friction.pdf` (17 pages) | `0e57d93e45bf29236754a735e42f6d2ae923aa1a23c65ebe9ed19041347ced7d` |
| `W3B/GROW_Science_Autumn1_W3B_Friction_Test.pptx` | `3049816d76009ebe3ad1b609e9ca22ec54c3abc82d3e8037b012386759ba278b` |
| `W3B/GROW_Science_Autumn1_W3B_Friction_Test.pdf` (15 pages) | `1ce1ba083eb62b521368b3c5863c098733ae7d677a1e7c0e641b8e0fd7681d3a` |
| `W3A/START_HERE.txt` | `b5c46c92125be91cb86f64c5969ad8378ab3948b41a82e7be01e7378ccdfc81c` |
| `W3B/START_HERE.txt` | `70a87773d7f0bc53b67cc1023263f2837ec473ceffc6ec1fc79b82823805c756` |

The eight pupil/teacher DOCX/PDF files keep the hashes recorded in `GROW_W3_FEEDBACK_2026-09-15.md`. Pack record and resource-page hashes are in the commit and `SHA256SUMS.txt`.

## 7. Still open before any release

1. **Human assistive-technology listening pass on Friction** by Matt or an accessibility reviewer, naming the real OS, browser, assistive technology and the exact candidate hash above. Sugar's pass does not close this.
2. Immutable publisher output admission (Site registry) and the Apps gate copy, through their owners; required CI on a pull request (this branch alone triggers no PR workflows).
3. The offline HTML companions listed in section 2 and the pre-existing static catalogue check failure on main.
4. Merge only outside the 08:30–15:30 UK school-day hold and after every gate above; then served-file verification before calling anything live.

Preserve EDU-Q1 → EDU-D3 → PLAY-D2 → PLAY-Q1 → PLAY-I1 → justified MAINT-1 → PLAY-X1, EDU-TRY-LESSON, EDU-HERO, EDU-HEADER-BRAND and PLAY-BRAND amendments, Site291/Lessons456/LP1 holds, completed Sugar and account/admin work, the W3A 40-minute plan, the W3B 32 + 4 + 4 boundary and the LAUNCH shared guide. Original RESULTS.md Not-run rows are unchanged. Keep High for authoring and acceptance; Light only for routine CI monitoring.
