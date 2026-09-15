# CX2 checkpoint — 15 September 2026

Append-only. Every entry: pass · source identities · owned files · PR/head · run id · exact next action.

## 0. First actions
- 0.4(a) Order committed verbatim: `docs/orders/CX2_FINISH_2026-09-15.md`.
- R3 done: `codex/edu-q1-grow-w3a-focus-20260915` fast-forwarded 1fa3ab94712bef3320c625000de9e978f8cf3d7c → 8d155f299c53e133d525d4fcc64bbc733b5d3250 (ancestry verified, tree 0e4c070a1114cb585446cc40c12c43c32f2a9861 = the tree the 120-stage acceptance and the 430-control GLV3 self-test ran on, so 2.1 cites those runs). PR #538 head now 8d155f2 (6 commits, 58 files). Branch `claude/made-by-matt-handoff-ycul48` deleted on the remote.
- Next: 0.4(c) publisher admission of docs/, 0.4(d) policy documents, R1 record, R5 diagnosis, R4 mechanism search.

## 1. First actions completed — 15 September 2026
- 0.4(c) `docs/` is in the Site publisher's `SKIP` set (`domain-split/build_education.py` at Site main c63149ead07c33e35d78bbdc8935b7934e7d292b: `public_file('docs/orders/CX2_FINISH_2026-09-15.md')` → False). Docs are not served.
- 0.4(d) Policy documents, supplied by Matt in this session and hash-recorded (not committed; uploads only):
  - Progress Schools Curriculum Policy 2026/2027, Issue 2 (August 2026): `PS_Curriculum_Policy_-_2026_2027.pdf`, 444,764 bytes, SHA-256 `593ab59361d1f1d22360a0ba12bdb96e08dcd94404a07368c09768414e982aed`, 41 pages. Confirms §14.3 minimal codes VF WS I NS E R, §14.4 Lundy, Tier 2/3 vocabulary, three-year thematic cycle, "digital software app" wording, Boxall as placement/progress instrument.
  - Feedback & Marking Policy 2025/2026 (Pilot), Issue 1, May 2026, EFL wording, 16 pages: `Feedback_Policy_2025-2026_-_Pilot.pdf`, 208,449 bytes, SHA-256 `41046284a00c9218679b946134cbc6e53c1897aad28b15fc4bd4aa963720ff3b` (the master-order reference copy; also on Drive as 1D8lpR-_1uQc2ND5C02T7BUfM8myBrC6M).
  - Second copy, same policy, Issue 1, Earwig wording, 13 pages: `Feedback_Policy_-_2025_2026_Pilot.pdf`, 204,058 bytes, SHA-256 `aa41d67963846cf35e9bb6e53e708c7b46725c2d5cef432c2e1994a78e434e53` (Drive 15hGPn0lGji4WRt-A_L2_19nidpP6XMRb). Both are Issue 1.
  - Feedback & Marking Policy Issue 2: searched this session's uploads, the Lessons repository (all history), Drive titles and full text. Not found. R9: Issue 1 remains the code source; S6 does not arise.
  - `13-Gathering_Feedback_and_Portfolio_Evidence.pptx` (SHA-256 `04dbc4f3b08d99744b12a2a84a3965bbc3dcc866f8522d16946db4bb59b7cb55`) is an Arts Award lesson deck, not a policy.
- R5: `check_catalogue_static.py` red on main 929cf731 (51 Spring/Summer Science lesson rows absent from TERM_AND_STYLE_EVIDENCE.json). Own PR #539 from branch `claude/cx2-r5-catalogue-evidence` head d10543f2d41c3e47c98f9f27d2a82153a7396ae3: generators re-run, red-before/green-after, planted control red, pins re-cut. Next: required CI green → merge → publication settled → rebase #538.
- R4 finding: `Teaching_Packs/GROW/HTML/*.html`, `Resources/*.html`, `Teacher_Notes.html`, `Pupil_Resources.html`, `GROW/index.html` are not exports of the canonical lesson (different chassis, no slide elements, one script, no long byte runs shared with the 6 September source). No generator exists in the repository or its history (`git log -S mbm-offline-classroom` finds nothing); they arrived whole in PR #431. Sugar's six native companions were produced outside the repository; the in-repo mechanism for Friction's DOCX/PDF is `tools/grow_resources/author_w3*.py`. STOP S3 raised in the readback with options; other lanes continue.

## 2. §2.3 reading-band report (Friction, report only) and S3 — 15 September 2026
Instrument: `_sownb/vb/tools/g26_reading_band.py` v1.3.0 (13/13 controls fired), bands from `_sownb/STYLE_CONTRACT.json` (GROW 3.0–7.0, BUILD 1.0–4.0, LAUNCH ≤14.21 ceiling), Flesch-Kincaid on pupil-addressee text.

| Text | Pupil FK | GROW band |
|---|---|---|
| Whole lesson (instrument's own run) | 6.98 | PASS |
| Arrival Supported / Standard / Stretch | 5.64 / 5.76 / 5.44 | in band |
| Lesson A exit Supported / Standard / Stretch | 3.70 / 6.54 / 5.88 | in band |
| Knowledge organiser | 7.51 | above |
| Review the evidence (B) | 6.96 | in band |
| Help prompts | 5.19 | in band |
| Lesson B exit slide (unchanged legacy) | 7.87 | above |
| Print scaffold Supported / Standard / Stretch | 7.80 / 5.62 / 5.29 | Supported above |
| Print worksheet Supported / Standard / Stretch (legacy) | 7.33 / 7.96 / 7.70 | above |

Accepted lesson: no re-open (4.2). Matt list: organiser, W3B exit, Supported scaffold and the three legacy worksheets read above the GROW band. Sugar (accepted): pupil FK 5.26 against BUILD 1.0–4.0, RED report-only, Matt list.

**STOP S3 (R4).** The stale offline companions (`Teaching_Packs/GROW/HTML/*.html`, `Resources/*.html`, `Teacher_Notes.html`, `Pupil_Resources.html`, `GROW/index.html`) are linked from the public hub `Science_Teesside/Teaching_Packs/web-slides.html` and listed as retained alternatives in `tools/downloads/SOURCE_PLACEMENT.json`. They are a separately authored offline chassis, not an export of the canonical bytes; no generator exists in the repository or its history. Options: (A) author a new in-repo exporter that regenerates the W3A/W3B offline companions from the current canonical lesson in the same chassis — new design work, needs a ruling; (B) inside #538, retire the two Week 3 companion entries on web-slides.html/GROW/index.html/Teacher_Notes.html to a clearly labelled superseded section that links the canonical lesson and the native pack (satisfies §25.4, smallest change, no generator needed because nothing is regenerated); (C) leave as is and ship the duplicate (violates R4). Friction Ready waits on this ruling; every other lane continues.

## 3. R5 PR #539 — CI failure fixed — 15 September 2026
- #539 head d10543f failed `Catalogue schema, tags and contract` at `companion_catalogue.py --self-test` ("evidence entry differs from its derivation"): `build_catalogue.py` had overwritten the 116 companion-pack evidence entries that `tools/ux2/companion_catalogue.py --write` owns.
- Fix commit 28610814313d0ca6deba8e6f45085e247f9370ed on `claude/cx2-r5-catalogue-evidence`: `companion_catalogue.py --write` re-run after the rebuild (116 entries re-derived, 0 pack rows changed), `build_lesson_order.py` re-derived, static check re-run, the two derived-file pins re-cut in `tools/verify_cross_estate_unification.py` (apps.json digest restored from origin/main, not a stand-in). `resources.json` unchanged (951 rows).
- Owned files in the fix: `assets/catalogue/lesson-order.json`, `tools/catalogue/STATIC_CHECK_RESULTS.json`, `tools/catalogue/TERM_AND_STYLE_EVIDENCE.json`, `tools/verify_cross_estate_unification.py`.
- Local proof on the fix tree (each exit 0): `build_display_titles.py --check`, `check_display_titles.cjs`, `check_catalogue_schema.py --self-test` (8/8 plants red) and plain, `unit_tags.py --self-test`/`--check`, `prove_catalogue_gate.py` (8 controls), `companion_catalogue.py --self-test` (6/6 plants red)/`--check` (116 packs), `build_spine.py --check`, `resource_sizes.py --check` (1463 sizes), `check_catalogue_static.py`, `build_lesson_order.py --check` (1075 entries), `derive_triggers.py --check` (471 asserted, 477 triggers).
- Evidence delta versus main 929cf73: 51 Spring/Summer Science entries added, 46 Science/Humanities entries with a refreshed `sha256` (8 with refreshed evidence quotes), 0 removed; the 116 pack entries equal their derivation.
- CI on 2861081 in progress (ux2-gates run 35008854934, S1L/static-contract run 35008854986). Session subscribed to #539 events. Next: required checks green → merge (one merge; Pages deploy settled) → rebase #538 → re-run pack/binding/size/lesson-order/PIN1/GLV3.
