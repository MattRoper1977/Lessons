# EASTER LEDGER — campaign VB_EASTER_A3

Append-only. This file is the resume pointer: a fresh session re-enters the
campaign at §0a from the last line here. `VB_STATE.json → resume_easter_a3`
mirrors it; where the two disagree, this file is the record and VB_STATE is the
stale copy.

Every count below comes from a tool this repository can re-run. Nothing is
carried from memory.

---

## §0 preconditions — 2026-09-03

Main at `949e15f52e35c39fbbe0d204bc0acc3e06cce555`, tree clean, exact match to
the order's expected base. Predecessor A2R closed `VB_EASTER_A2R_PARTIAL`; PR
\#278 merged and blob-verified.

**§0b — the A2R mechanism, re-run on main, not recalled.**

| question | answer | evidence |
|---|---|---|
| g23 counts pupil teaching content ONCE; medians re-derived; ≤1.25 unchanged | yes | `g23_period_load.py` sha `0d0391150a207eaa`, 5/5 controls; contract `ed671277…`, `load.period.ceiling` = 1.5 unmoved; 1.25 is the stricter operative trim target |
| g24 screen-rendered only; no @media fail-open; transformed labels never visuals | yes | `g24_visual_density.py` sha `f0bccbb29ac940c4`, 9/9 incl. `print-only-svg-is-not-counted`, `rotated-text-label-is-not-a-visual` |
| g27 armed | yes | `g27_no_filename_weeks.py` sha `e07e61c5ad3295b4`; 134 tools scanned, 0 hits, 19/19 controls behaved as declared |
| g28 armed | yes | `g28_cell_existence.py` sha `63a08240712d0073`; `citesC999OnARealSheet` fires, `citesARealAddress` does not |
| workflow counts derived via `--list-controls`, nothing pinned | yes | no control/tool literal in `fieldops-p2-and-sweep.yml` sha `55d127c6b05fc594`; `mechanism_battery.py --prove-red` PASS, 11 tools / 98 controls |
| RSH-3 refs PASS; historical W16 candidates FAIL | qualified yes | four references PASS. **The historical W16 artefacts are NOT recoverable** — they existed only in the Codex preservation archive. A2R substituted four named negatives, all RED, recorded in `MECHANISM_PROOF_MATRIX.json`. |

No §3-residue PR was required.

**§0c — six over-ratio decks, not five.** All are over the 1.25 operative target:

| deck | words | family median | ratio | action |
|---|---|---|---|---|
| BUILD_HUM_W15 | 2036 | 1412 | 1.44 | TRIM |
| BUILD_HUM_W16 | 2159 | 1412 | 1.53 | TRIM |
| GROW_HUM_W15 | 3529 | 906 | 3.90 | TRIM → expect SPLIT |
| GROW_HUM_W16 | 1249 | 906 | 1.38 | TRIM |
| LAUNCH_HUM_W15 | 3526 | 822 | 4.29 | TRIM → expect SPLIT |
| LAUNCH_HUM_W16 | 1054 | 822 | 1.28 | TRIM |

---

## §1 target list — register only, 0 units against the ceiling

**Headline through week 26, content reading, re-derived at main: 573 · 134 · 439.**
Identical to the order's stated run-14 figure. Path reading 142 claimed, printed
as secondary and used for nothing.

**A near-miss worth recording.** Enumerating the spine directly gives 575 in
scope, not 573, and the difference is real but is not a coverage change: two
cells carry `scopeStatus: OUT_OF_SCOPE` in the spine —
`'GROW Weekly - Spring'!C116` (wk 20) and `!C117` (wk 21), both "Careers-specific
outcome; Careers is expressly outside ORDER FEB scope". The census excludes them
correctly and the naive enumeration did not. **573 stands; no renumber.** The
tool and the spine are both byte-unchanged since the run-14 close, which is how
the difference was localised rather than argued.

**§1c — 262 deck plans covering all 439 open cells.**

    plan sizes   1-cell ×146 · 2-cell ×55 · 3-cell ×61
    FORECAST     at BATCH_CEILING 24 → ≈40 cells per batch → 11 batches to DONE

Grouping is by family (lane + subject) and **ruled week**, not by strand, and the
reason is measured. Every one of the 573 cells in scope — all 134 covered, all
439 open — is a unique (lane, subject, strand, week) tuple: the workbook grants
exactly one outcome per strand per week. Grouping by strand makes every plan
one cell *by construction*, which is an artefact of the key, not a fact about
teaching. What the estate actually does is fuse strands within a family-week,
and the landed `BUILD_HUM_W16_Then_And_Now_And_What_Is_Fair.html` is the
precedent: it claims `'BUILD Weekly - Spring'!C41` (World About Me, "Compare old
and new objects") and `!C53` (RE & World Views, "Talk about what is right and
wrong, simply") under one title, and passes its gates.

Plans by family: LAUNCH ASDAN 43 · BUILD ASDAN 24 · BUILD Art 24 · LAUNCH Art 24
· GROW Art 23 · GROW ASDAN 22 · BUILD/GROW/LAUNCH Humanities 21 each ·
LAUNCH Science 15 · BUILD Science 13 · GROW Science 11.

**§1b — every claimed-but-unserved and unscorable cell resolved, none carried.**

*Five cells → RESHELL plans (§1e).* A standing deck claims the cell and its
content does not carry the outcome. That is a deck to repair, not a second deck
to build for the same week:

| cell | standing deck | score (threshold 0.85) |
|---|---|---|
| `'GROW Weekly - Autumn'!C107` | GROW_ART_W6_Artist_Research | 0.667 |
| `'GROW Weekly - Autumn'!C108` | GROW_ART_W7_Share_The_Portfolio | 0.667 |
| `'LAUNCH Weekly - Autumn'!C36` | SCI_L_W5L3_Osmosis_Data_Do | 0.800 |
| `'LAUNCH Weekly - Autumn'!C39` | SCI_L_W9L3_Identical_Daughter_Cells_Do | 0.600 |
| `'LAUNCH Weekly - Autumn'!C41` | SCI_L_W11L3_Stem_Cell_Discuss_Do | 0.400 |

*Three cells → HELD, human.* Their outcomes carry no distinctive words once
stopwords and corpus-ubiquitous terms are removed, so SERVES cannot be evaluated
either way. "I cannot measure this" and "this is missing" are different answers
and only one of them justifies building. See `EASTER_HUMAN.md`.

**§1d ordering** is week-major, ASDAN → Science → Humanities → Art, BUILD → GROW
→ LAUNCH, with weeks a cover teacher takes before Matt returns (ruled week ≤ 8)
promoted ahead of everything. Batch 1 is 24 of 24 cover-taught plans.

Targets: `tools/easter/EASTER_TARGETS.json`, rebuilt by
`tools/easter/build_targets.py` — re-runnable, so no number here has to be trusted.

---

## §0c — BUILD Humanities, PR #280

`BUILD_HUM_W15` 2036 → 1715 words, ×1.44 → **×1.21 WITHIN**. One lesson unit.

Not a trim. The excess was one `<p>` in stage 6 carrying the same instruction
block four times, verbatim. Duplicates deleted; 67 distinct pupil sentences
before and after; containment PASS on 194 sentences, 0 missing.
`tools/easter/dedupe_stage_text.py`, 7 controls, all fired.

**BUILD_HUM_W16 not trimmed — see A3-H5.** Its 394-word excess is 383 words of
Lundy banner printed on all ten stages. Same for GROW W16 (116 over, 112 banner)
and LAUNCH W16 (26 over, 144 banner). Trimming real teaching to offset a banner
the contract requires would damage three lessons; changing g23 to discount a
refrain would loosen a threshold, which §5 forbids. Held for a ruling.

---

## §0c — GROW Humanities, PR #281

`GROW_HUM_W15` 3529 → 2734 words (−795), ×3.90 → **×3.02**. One lesson unit.
86 distinct pupil sentences before and after; containment PASS on 261 sentences,
0 missing. Still OVERLOADED, and now on a defensible basis: **A3-H2 split
candidate stands.** After removing 795 words of verbatim within-paragraph
repetition it still carries three times a GROW Humanities lesson.

`GROW_HUM_W16` unchanged — see A3-H5 (116 over target, 112 of it Lundy banner).

**Two bugs in the de-duplication tool, both caught by its own controls, both
fixed in this PR.** The tool landed in #280 with them.

1. It located the edit on `stage_pupil_node()`, a pruned copy with the staff
   drawer and hidden nodes removed, so an element's `.text` there is a
   concatenation of fragments that were never contiguous in the file. On
   GROW_HUM_W15 that text matched the raw bytes **zero** times and the anchor
   guard refused the edit rather than applying it to the wrong span. Now
   located on the original tree.
2. It tested `is_staff()` on the element, but the drawer marker sits on the
   containing `<div data-audience="staff">`, so drawer text was not skipped.
   The `staff-drawer-text-is-untouched` control caught it. Now walks ancestors.

A third change follows from the first: an element with no children can still
fail to appear in the raw file, because the file writes HTML entities and the
parser hands back decoded characters — GROW_HUM_W15's stage-6 paragraph is 8,832
decoded characters matching zero raw bytes. The edit is now anchored to a raw
span located by decoding candidates and requiring exactly one match, and applied
back-to-front by offset, so every entity outside the removed sentences survives.

Regression: re-running the tool on the already-deduped BUILD_HUM_W15 is a no-op.

---

## PAUSE — VB_EASTER_A3_PAUSED, 2026-09-03

Stopped under §6 S2 at a clean transaction boundary: #279 and #280 merged and
blob-verified, #281 pushed with five of six checks green and the sixth stalled.
No half-merged batch; batch 1 not started.

Handoff: `_sownb/vb/VB_EASTER_A3_SAFE_HANDOFF.txt`.

**Resume at §0a from this file.** The next three actions, in order: merge #281
when its sixth check reports; LAUNCH Humanities de-duplication (pre-measured on
a scratch copy: 3526 → 2710 words, ×4.29 → ×3.30, 85 distinct sentences both
sides); then batch 1, whose 24 plans are all cover-taught weeks.

**The stalled check is not this campaign's.** No PR here touches a `Games/` file,
and the instrument lives in the site estate, cloned fresh at job start, so it can
change between runs with nothing in Lessons changing. It stalled twice on #278
earlier today, passed on #279 and #280, and is stalled again on #281 —
intermittent, not deterministic. One cancel-and-rerun was already spent on it.

