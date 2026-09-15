# LAUNCH W4L1 Diffusion — parity and acceptance record

15 September 2026. **Draft candidate. Not merged, not published, not served.** Lessons draft #546
on branch `claude/cx2-diffusion`, candidate first committed at `b7bfb30d22a71e0827b54f401dfc52e1e68d1d2d`, merged with main `423f11d9` at `ea251665`. Authored under
ORDER CX2 §3 against `docs/orders/LESSON_STANDARD_2026-27.md`.

Candidate: `Science_Teesside/Launch/SCI_L_W4_L1_Diffusion.html`
SHA-256 `563e0bddc7049afb1dfc7245b1810da5094c19bca8027a08bbaf4c26d5a0dc54`, 258,861 bytes.

## 1. What the candidate changes on the canonical lesson

- §25 standard on the LAUNCH chassis: heading focus after every slide change; dialog semantics
  (`role="dialog"`, `aria-modal`, focus trap, return focus) on the TA brief and cover modals; an
  Escape route from each.
- A four-question arrival in three routes, with print and answer sheets.
- A knowledge organiser as both dialog and print, with a Tier column and the particle model.
- One optional help prompt in We Do 2. The Lundy Loop slide and its print are removed; the single
  optional prompt is what remains, per the order's one-prompt rule.
- A two-check exit ticket per route, with print and answer sheets.
- Staff notes and the feedback card, using Feedback & Marking Policy 2025/2026 (Pilot) Issue 1
  codes. `E` reads "Evidence captured on the school's digital evidence platform" — no product is
  named on any surface (R10).
- Stage timings 0/4/1/4/4/3/5/15/4, summing to the 40-minute lesson.

## 2. Native parity

Built by `tools/launch_resources/author_w4l1_natives.py`, which rebuilds every output from the git
base on each run rather than editing a previous output.

| File | Change |
|---|---|
| `Week_4/W4L1_Diffusion.pptx` | 17 → 21 slides: three arrival route slides, two organiser slides, stage minutes matching the lesson, the help prompt, the two-check exit. Every new shape is a deep copy of a reviewed shape, so the deck design is unchanged. No day or period wording remains. |
| `Week_4/W4L1_Diffusion.pdf` | re-rendered from that deck |
| `Week_4/W4L1_Worksheet.docx` / `.pdf` | arrival routes, organiser and exit routes appended; day and period wording removed |
| `Teacher_Guide_And_Answers.docx` / `.pdf` | the W4L1 section gains the arrival and exit answers and the feedback card |
| `Pupil_Worksheets.pdf` | rebuilt from the fifteen worksheet PDFs in order |

`tools/launch_resources/refresh_w4l1_pack_records.py` then rewrote the LAUNCH manifest, checksum
rows, download index and every archive whose committed member map carries a changed file. The
teacher guide travels in all 21 archives, so all 21 were rebuilt from their committed member maps
with the builder's fixed timestamps.

## 3. All-stage acceptance

`tools/launch_resources/lesson_acceptance.py` with `W4L1_ACCEPTANCE.json` — the Friction harness
parametrised, run over standalone and http origins at 320/390/768/1280.

| Measure | Result |
|---|---|
| Stage cases | 108 |
| axe serious or critical violations | 0 |
| Keyboard stage transitions | 96 |
| Enlarged-text cases | 8 |
| Theme cases | 4 |
| No-JS cases | 4 |
| Print cases | 50 |
| Pack cases | 6, four pages each |
| Page errors | 0 |

Result: PASS. The remaining axe findings are moderate and belong to the shared chassis
(`landmark-one-main`, `region`, `heading-order`), identical in kind to Friction's.

Ten console `ERR_FILE_NOT_FOUND` lines are the chassis's `/hud.js` reference under `file://`, present
identically in the unmodified base — not introduced here.

## 4. Reading band

Instrument `_sownb/vb/tools/g26_reading_band.py` v1.3.0, Flesch-Kincaid on pupil-addressee text.

| Text | Pupil FK | LAUNCH band |
|---|---|---|
| Whole lesson | 7.5 | within ceiling 14.21 |
| Supported route | 8.10 | within |
| Standard route | 8.55 | within |
| Stretch route | 8.35 | within |

## 5. Admission and gates

`tools/launch_resources/admit_w4l1.py` declares a 36-member GLV3 replacement transaction, admits
every member and the original-targets ledger by digest through `REVIEWED_PATHS`, refreshes the
evidence sha256, lesson order and resource sizes, re-pins `CATALOGUE_PINS` and regenerates the PIN1
triggers. The original-targets row for this lesson moves stage count 10 → 9 and carries the
candidate hash.

| Gate | Result |
|---|---|
| GLV3 change boundary `--self-test` | PASS, 36 protected changes, 524 controls |
| Cross-estate static contract, with positive control | PASS, control detects 3 planted errors |
| `admit_w4l1.py --check` | PASS (idempotent) |
| `check_packs.py` | PASS, 25 classroom source routes preserved |
| Original-Science browser run | PASS, 743 cases, 33 routes, 84 PDFs |
| PIN1 triggers | PASS |

## 6. Human assistive-technology listening pass (R1, CX2)

Reviewer: Matt. Device: phone. Date: 2026-09-15. Result reported by Matt: "Sound works when listen
on phone". Candidate hash: `563e0bddc7049afb1dfc7245b1810da5094c19bca8027a08bbaf4c26d5a0dc54` (the
full hash of `Science_Teesside/Launch/SCI_L_W4_L1_Diffusion.html` in the heading above). Operating
system, browser and assistive technology: not stated by Matt. Accepted under CX2 R1 in the same
shape as Sugar's and Friction's; nothing further owed. This closes M-STOP S1 for this candidate.

This is a reported listening result on one device. It is not a full assistive-technology audit and
is not recorded as one.

## 7. What is not claimed

Not merged, not published, not served. The lesson and its pack files change public bytes, so
publication requires a Site carrier admitting the new served digests before this reaches
madebymatt.uk. Served bytes are UNMEASURED from this container: outbound access to the live host is
blocked by the environment's network policy, and the repository's production byte-check instrument
has compared unlike bytes since the published navigation injection, so its result is not evidence
either way.
