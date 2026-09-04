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

## §0c — LAUNCH Humanities, PR #282

`LAUNCH_HUM_W15` 3526 → 2710 words (−816), ×4.29 → **×3.30**. One lesson unit;
three of 24 spent. 85 distinct pupil sentences before and after; containment
PASS on 258 sentences, 0 missing, red control fired. g18 BINDING PASS
(famP25 797, deck 2710) and GLOBAL PASS. Pack `SHA256SUMS.txt` refreshed for its
four existing rows; none added, none removed; `sha256sum -c` verifies.

Every non-text property of the file is byte-identical: 12 `<section>`, 82 `<div>`,
66 `<p>`, and all three `<script>` and all three `<style>` bodies hash the same
before and after. The print pack is unchanged at 1,812 characters. The whole
delta sits in one stage — **I Do 2 · connect, 1469 → 653 words** — and the other
eight stages are word-for-word identical.

**A3-H2 stands.** At ×3.30 this is still three times a LAUNCH Humanities lesson
and still a split candidate. What has changed is the basis: the excess is now
known to be teaching, not repetition.

---

## §2 precondition — the duplication is a generator defect, not three decks

Three W15 Humanities decks were trimmed one at a time and all three carried the
same defect in the same stage. Three independent authoring accidents do not
produce a uniform ×4 in one named stage, so before batch 1 builds anything on
top of this estate, the estate was asked the same question with the same
instrument.

`tools/easter/dedupe_sweep.py` — new, 10 controls, all fired, read-only.
`--project` copies each affected deck, dedupes **the copy** and re-runs g23, so
every ratio below is a number the gate printed and not arithmetic on a word
count. A planted mutation that made the projection write the source file reds
`projection-leaves-the-source-file-byte-unchanged`; withdrawn, it greens.

    377 decks scanned · 24 affected · 19 with removable duplication
    7,593 removable words · repeat factors: 170 sentences ×4, 17 ×2

**The shape.** Not a paragraph printed four times. In `SCI_B_W16B` the task
block — sentences 0–7 — appears four times inside one flat `<p>`, wrapped by
connective knowledge (8–14) and a procedural walkthrough (15–20) that each
appear once. The pattern of first-appearance indices is
`0..14, 0..7, 0..7, 0..7, 15..20`.

**What it is not.** The first reading was that a per-tier loop emitted
undifferentiated text, and that the decks are therefore *missing* their tiering.
That reading is wrong, and the clean sibling proves it:
`SCI_B_W14A` (unaffected) and `SCI_B_W14B` (affected) have the identical stage
structure — three distinct `<h3>` tier headings each with its own `<p>` — and
differ only in the long task paragraph, 108w against 597w. Nothing is missing.
One paragraph is repeated, and dedupe restores the authored shape rather than
inventing one.

**Ten of the nineteen are live g23 ceiling reds on main**, none previously
reported, because §0c looked only at Humanities. De-duplication alone clears
five of the ten and brings seven decks to the 1.25 operative target:

| group | decks | before | after | verdict |
|---|---|---|---|---|
| Science (Build/Grow/Launch, W7 + W14–W20) | 14 | ×1.28–1.78 | ×1.09–1.49 | all PASS; 5 reds cleared |
| ASDAN Spring1 W15/W16 (BUILD ×2, GROW ×2, LAUNCH ×1) | 5 | ×2.40–3.08 | ×1.97–2.57 | **all STILL RED** |

The five ASDAN decks are the useful negative result: their overload survives
de-duplication, so it is real teaching content and belongs with A3-H2's split
question, not with this one.

**The remediation moves no denominator.** Not one of the 24 affected files sits
in any of the nine family baseline sets (BASELINES membership, checked against
`_sownb/feb/tools/g18_measurement.py`; overlap 0 in every family). So deduping
them changes no family median and no p25 floor — the backlog cannot loosen g18
by lowering a floor, and no ratio elsewhere in the estate moves.

**Not done here, and why.** Nineteen decks is nineteen lesson units of a ceiling
of 24 with three already spent, and batch 1 alone needs 24 plans. Spending the
campaign's ceiling on de-duplication would starve the build the order actually
asks for. Recorded as **A3-H6** with its evidence and its projection, to be
scheduled as its own order. Nothing in the 19 was edited: `git status` shows one
lesson file changed in this PR.

Evidence: `_sownb/vb/evidence/a3/dedupe_sweep_live.json` (sweep + projection),
`dedupe_launch_humanities.json`, `g23_L15_before.json`, `g23_L15_after.json`,
`cgate_L15.json`, `g18_L15_after.json`, `battery_launch_hum.json`
(11 tools / 98 controls, `--prove-red` PASS).

---

## CORRECTION — the sixth check on #281 was never stalled

The PAUSE below was written on a false reading and is left in place because the
record is append-only. What it says was true when written and is false now:

- `AUTHORITATIVE_REMOTE_MAIN` was `727c3162…`. Main is now
  `e09005a8b1a8f820e8462017b5964ceefa02a7e8`.
- #281 was "5 of 6 checks GREEN … NOT MERGED. Do not merge on five of six."
  The sixth check **completed successfully at 22:50:33** on head `b35588b`, seven
  minutes before the handoff was written. The GitHub API was serving a stale job
  status; I read the stale status as a stall. #281 merged as `e09005a8` and all
  ten of its blobs are byte-identical between the merge commit and the branch
  head.

This was the second time in one session that API lag was read as a stalled job —
the first cost a cancelled healthy run on #278. Recorded in WRONG_BEFORE_RIGHT:
**a status endpoint is an instrument, and it was read without a control.** The
control now used is the one applied above: re-read the job's own conclusion and
timestamp before acting, and blob-verify a merge rather than trusting its status.

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

## A3-H6 — the duplication backlog, cleared. PR #283

Matt's ruling, 2026-09-03: **before batch 1, as its own order.** Nineteen decks,
nineteen lesson units; three were already spent, so the A2R ceiling of 24 now
stands at **22 spent, 2 remaining**. That is stated plainly because batch 1
alone needs 24 plans: the ceiling must be raised or re-scoped before the build
campaign can start. Nothing here assumes it will be.

**What changed.** Nineteen decks across seven packs and three subjects, all in
one stage each. Every count below comes from a tool in this PR.

    words removed        7,593        bytes removed        50,817
    decks edited            19        packs touched             7
    containment          19/19 PASS, 0 missing sentences, red control fired on each
    distinct sentences   identical before and after on every deck
    structure            element counts, script and style bodies, print packs and
                         staff drawers byte-identical on all 19

**g23, before → after.** The projection published in #282 said ten ceiling reds
would become five. Measured on the landed files, it is exactly that:

| group | decks | before | after | outcome |
|---|---|---|---|---|
| Science — Build/Grow/Launch, W7 and W14–W20 | 14 | ×1.28–1.78 | ×1.09–1.49 | **14/14 PASS**, 5 reds cleared |
| ASDAN Spring1 W15/W16 | 5 | ×2.40–3.08 | ×1.97–2.57 | 5 still RED → A3-H2 |

Ceiling reds across the nineteen: **10 → 5**. Seven decks now sit at or under
the 1.25 operative target.

**No denominator moved.** All nine family medians are byte-identical between the
before and after runs (`med` compared row-by-row, 0 moved), because no affected
deck is in any family baseline set. The correction cannot loosen g18 by lowering
a floor.

**The estate is clean of it.** Re-sweeping after the edit: total removable **0w**,
and the ×4 entry is gone from the repeat-factor histogram entirely — 170
sentences at ×4 before, none after. What remains is 76 words at ×2, refused
rather than missed: the `<p class='truth'>` safeguarding pair ("No diagnosis or
medical advice." / "No personal or family disclosure.") printed twice on eleven
title slides. It carries inline `<b>` markup, so string surgery would destroy
it, and 76 words across the estate moves no verdict. Reported, not chased.

**One deck to watch.** `SCI_G_W16A_Solubility_And_Recovery_Explore` lands at
×1.49 against a ceiling of 1.50 — roughly seven words of headroom. It passes,
and it is the deck a future edit is most likely to push back over.

**A trap the pre-flight caught, and the tool that closes it.** Twenty-eight packs
name their checksum file `SHA256SUMS.txt`; three name it `CHECKSUMS.sha256`.
Same format, both live on main. `GROW_ASDAN/Spring1_W1-W6_2026-27` is one of the
three and holds two of the nineteen decks, so a refresher knowing only the
common name would have left two edited decks with stale digests **and no error**.
It was found by asking every affected pack for its file before writing anything.

`tools/easter/refresh_pack_checksums.py` — new, 8 controls, all fired. It
refreshes rows the file ALREADY has, asserts the count did not move, never adds
a row, never drops one naming a missing file, and verifies afterwards. The
existing `_sownb/feb/tools/update_pack_checksums.py` was not reused: it
regenerates the entry set from a glob, so it would enrol files nobody reviewed,
and its three packs are literals so it cannot follow an edit. Result across the
seven packs: 19 rows refreshed, **0 added, 0 removed**, verify OK on all seven.

One control in it was rewritten before landing. The first version tried to prove
the row-count assertion fires by monkeypatching `len`, which tests the
monkeypatch rather than the guard — the assertion cannot be reached through the
public API, since `out` gains exactly one entry per input line. It is replaced by
a control on the risk the assertion exists for: a comment header and a blank line
survive verbatim, so the count cannot drift under a legal file.

**Battery: 14 tools, 123 controls**, derived, `--prove-red` PASS.


**Merged** `0d54ddca1c893fbb9e818c0b08675535a021e86c`, six of six checks green,
**75 of 75 paths blob-verified** against main. The sixth check — the site-estate
keyboard-reachability walk that this session twice misread as stalled — completed
successfully at 23:32:39, four minutes into the run.

---

## CAMPAIGN STATE at main `0d54ddca` — the ceiling is the blocker

    PRs landed   #279 #280 #281 #282 #283, all blob-verified
    ceiling      22 of 24 lesson units SPENT, 2 remaining
    batch 1      needs 24 plans. CANNOT START.
    headline     573 in scope / 134 covered / 439 open, unchanged; 0 batches run

Nothing here is a reason to start batch 1 on 2 units and stop halfway. The
ceiling is Matt's to raise or re-scope, and until he does, the campaign's open
work is the three human items below, not the build.

**Open, and all human:**

- **The ceiling.** Blocking everything.
- **A3-H2** — seven split candidates now, not two. Two Humanities decks
  (×3.02, ×3.30) and five ASDAN Spring1 decks (×1.97–2.57) whose overload
  survived de-duplication. The ASDAN five may be a timing question rather than
  a split: their minutes run against the reverse of their content.
- **A3-H5, and the same question in a second form.** Whether g23 counts a
  banner repeated on every stage once or once per stage; and whether it counts
  the title slide, `data-min="0"`, carrying 327–384 words in every deck in the
  estate. Answering either loosens g23 estate-wide, so §5 forbids me deciding
  it. Together they are roughly 14% of every deck's word count and they explain
  a large part of why the whole estate reads heavy.
- **A3-H1** (3 unscorable cells), **A3-H3** (19 stale lesson-config week labels
  blocking the reshell recipe), **A3-H4** (carried).

**What the estate gained across these five PRs.** Four gates that were measuring
nothing on 264 of 607 decks now measure both shells; a word-boundary undercount
that overstated all nine family medians is corrected; 8,388 words of duplicated
instruction are out of 22 decks; the ×4 defect is gone from the estate; and the
mechanism went from 11 tools / 98 controls to **14 tools / 123 controls**, all
derived, with the two Easter tools now exercised by CI that previously ran
neither.

---

## A3N R3 — chrome stops being counted. PR #286

**Ceiling: 0 lesson units.** No deck is edited by this PR.

**The rule.** The contract-mandated refrain and the title/identity slide count
ZERO, in the g23 numerator and in every deck of the family-median derivation.
Threshold 1.25 and ceiling 1.5 are untouched. Detected by contract identity —
the pinned contract's own `.lundy` selector row and its four `shared.lundy.*`
visible-string rows, read from the file, not typed into the tool — plus the
chassis's `data-type="title"`.

**R3's control fires.** The three W16 decks clear with no content edit:

| deck | before | after | verdict |
|---|---|---|---|
| BUILD_HUM_W16 | ×1.53 RED | **×1.37** | RED → PASS |
| GROW_HUM_W16 | ×1.38 | **×1.22** | now under the 1.25 target |
| LAUNCH_HUM_W16 | ×1.28 | **×1.14** | now under the 1.25 target |

**The estate-wide flip list says it is not a loosening — it is marginally
stricter.** `tools/easter/chrome_flip_list.py`, 6 controls, re-measures every
deck in all nine families both ways in one pass with the median recomputed under
each rule:

    20 decks move · 5 CLEARED (RED→PASS) · 7 REGRESSED (PASS→RED) · 8 target-only
    net verdict change: +2 RED

Every regressed deck carries LESS chrome than its family (0.9%–16.2% against
family shares of 20–38%), so each moves for the stated reason. **None flips for
a reason other than chrome exclusion, so nothing is parked.** The 7 new reds
join the normal trim queue.

**An anomaly the flip list surfaced, worth more than the flip.**
`LAUNCH_HUM_W8_Maps_Symbols_And_Grid_References` measures **0.9% chrome** where
its five LAUNCH Humanities siblings measure ~24%. A deck that barely carries the
refrain its family carries is a candidate `lundy-in-three-places` violation, not
a g23 problem. Logged as **A3-H7**; no edit here.

**Three generalisations were tried and all three were withdrawn by their own
controls** — the repeat-counts-once clause, an every-stage rule, and a
sibling-group rule. Each removed real teaching. Full working, with the measured
numbers, in `WRONG_BEFORE_RIGHT.md`. R3's repeat clause ships **OFF** as a
**DEFAULTED** decision under N1b, as a flag (`REPEAT_COUNTS_ONCE`) rather than
deleted code, so Matt's ruling is one line.

Mechanism: **15 tools, 134 controls**, derived, `--prove-red` PASS. g27 PASS.
Evidence `_sownb/vb/evidence/a3n/`.

---

## A3N R2 — the five ASDAN decks get their clock fixed. PR #287

**Ceiling: 0 lesson units** (R1: a timing PR counts zero).

**What was wrong.** All five shared one profile: `I Do 2 · connect` carrying
471–548 content words against **3 declared minutes** — 157–183 words a minute —
while `Independent · evidence` carried 256–293 against **16**, about 17 a minute.
The minutes ran against the reverse of the content. Total reading need is 25–28
minutes of the 40, so **the lesson fits; only its clock was wrong.**

**The derivation.** Each stage first takes the minutes its reading needs,
`ceil(contentWords / 90)` at g23's own assumed rate — a floor that is monotonic
in content by construction. The surplus is then distributed in proportion to
what the author already wrote.

    minutes  [0,3,3,4,3,3,4,16,4]  ->  [0,3,3,7,3,7,5,9,3]   BUILD_ASDAN_W15
                                       [0,3,3,7,3,7,5,9,3]   BUILD_ASDAN_W16
                                       [0,3,3,8,3,7,4,9,3]   GROW_ASDAN_W15
                                       [0,3,3,7,3,7,4,10,3]  GROW_ASDAN_W16
                                       [0,3,3,7,3,8,4,9,3]   LAUNCH_ASDAN_W16

    under-timed stages   2 -> 0 on every deck · session 40 preserved exactly
    content words        unchanged on every deck · containment 5/5 PASS, 0 missing

**Strict global monotonicity is NOT enforced, and that is DEFAULTED under N1b.**
Allocating the whole session by word count cuts `Independent · evidence` from 16
minutes to 3, because independent work is pupils DOING and its minutes were never
a reading figure. `--strict` measures exactly that and a control pins it. A tool
that compresses independent work to satisfy an arithmetic about words has
repaired the number and broken the lesson.

**THE SAME FACT WAS RECORDED IN THREE PLACES AND THE TOOL WAS WRITING TWO.**
`data-min` is what the gates read; `lesson-config.timings` is what the estate
reads; and `<div class="time">N min</div>` is **what a teacher reads off the
board** — static text, computed from nothing, no `updateTimerDisplay` on these
decks. The first application left five decks showing "4 min" on a stage now
allocated seven. Caught before anything shipped, by looking rather than
assuming; the decks were reverted and re-done. All three records now move
together and a control (`the-visible-minute-badge-moves-with-the-attribute`)
pins it. The reshell dropped one of three records once already and nothing
noticed for a year.

**The band decision, and a structural fact R2 could not have known.** A timing
fix **cannot move the g23 ratio** — the ratio is contentWords ÷ family median and
minutes do not enter it. So the re-measure gives the same answer either side of
the fix, and the fix stands on its own merits (2 under-timed stages → 0 on every
deck) rather than as a route to a ratio.

Measured under exact projection at R3's counting, all five are **>1.6 → SPLIT**:

| deck | ratio | band |
|---|---|---|
| BUILD_ASDAN_W15 | ×1.94 | SPLIT |
| BUILD_ASDAN_W16 | ×2.00 | SPLIT |
| GROW_ASDAN_W15 | ×2.04 | SPLIT |
| GROW_ASDAN_W16 | ×2.06 | SPLIT |
| LAUNCH_ASDAN_W16 | ×2.00 | SPLIT |

With `GROW_HUM_W15` (×3.13) and `LAUNCH_HUM_W15` (×3.22), **seven decks now
carry a SPLIT verdict**, which is where R2's other clause sends them.

Checksums refreshed across three packs, 5 rows, 0 added, 0 removed, verify OK.
Mechanism **16 tools, 142 controls**, derived, `--prove-red` PASS.

---

## A3N splits — REFUSED AS SPECIFIED, DEFAULTED under N1b

R2 authorises a split for `GROW_HUM_W15` (×3.13) and `LAUNCH_HUM_W15` (×3.22),
and defines it: *"A split happens at a stage boundary into two decks."*

**Neither deck has a stage boundary to split at.** Measured, every teaching stage
of both decks serves BOTH of its outcomes:

    GROW_HUM_W15    s1..s9  all serve outcome1 AND outcome2
    LAUNCH_HUM_W15  s1..s8  all serve both; only s9 (Exit) serves one

Both decks are slot `HUM+RE · Integrated Humanities and RE`, and their objectives
tie the two outcomes together in a single sentence — "Place supplied rights and
protest events in chronological order **and** explore how beliefs can support
resilience"; "Explain causes of a supplied 20th-century conflict **and** compare
reasons in an ethical decision". The integration is the design of the slot, not
an accident of drafting. Their stages are titled *"Rights chronology and belief
resilience"* throughout.

Cutting at any boundary yields two incomplete lessons — one with no Independent
or Exit, one with no Arrival or Starter. Producing two complete lessons instead
is not a split but a rewrite that discards the integration the slot exists for.

**DEFAULTED: not split, not trimmed, not edited.** Both cells stay covered by a
working integrated lesson. Trim-to-drawer is not the alternative either: at ×3.13
reaching 1.25 means moving ~1,350 of 2,245 words into the drawer, which REVIEW.md
already ruled "not a trim by any reading of R5.5". Logged as **A3-H8**.

The five ASDAN decks carry the same SPLIT verdict from R2's band (×1.94–2.06)
and are queued rather than attempted, because their split line has not been
tested and they are Spring decks with no cover-teaching urgency.

---

## BATCH 1 — opened at main `d4d7c914`, ceiling 0/24 (R1)

**R1 correction recorded, nothing reversed.** The 22 units previously counted
against A3-H6 were misattributed: under R1 a dedupe PR counts ZERO. #280–#283
and #286–#287 are all 0-unit PRs. Batch 1 opens at **0/24**.

**Composition.** 68 of the 262 plans are cover-taught (ruled week ≤ 7, all of
weeks 1–7). 65 AUTHOR, 3 RESHELL.

**Donor survey, and a boundary it exposes.** N3d requires one g19-green donor per
family. Nine of twelve families have a gate-readable 9-stage donor. **The three
Art families have none**, so all 19 Art cover-taught plans are unbuildable in
this batch and are PARKED with their cells, not attempted.

**Why "gate-readable" is the binding property.** 55 of 81 measured ASDAN and
Humanities decks declare their stage minutes as `data-minutes`; only 26 use
`data-min`, which is what `lesson_stages` and therefore every gate reads. This is
A2R's known R2 regression seen from the other side, and it decides donor
selection: a deck authored from a `data-minutes` donor would be born with no
timings any gate can see.

## BATCH 1 — closed. PR #288

**BATCH 1: +2 units, cells 134→139, open 439→434, parked 19, PR #288, main d4d7c914.**

Two decks authored, gated and landed; both cover-taught weeks a cover teacher
reaches before Matt returns.

| deck | cells | words | g23 | g18 | g25 | g28 |
|---|---|---|---|---|---|---|
| `BUILD_ASDAN_W1_My_Routine_My_Challenges_My_Area` | C130 · C144 · C174 | 989 | ×1.02 PASS | BINDING PASS | PASS | PASS |
| `GROW_ASDAN_W1_What_I_Am_Good_At_And_What_Our_Area_Needs` | C130 · C174 | 948 | ×1.02 PASS | BINDING PASS | PASS | PASS |

Both sit at **×1.02**, inside the 1.25 operative target, not merely under the
1.5 ceiling. g24 is RED on both for the estate-wide print-dead condition (A2R
R3): the chassis hides the slide container under `@media print`, so every
screen diagram in this estate is absent from the printed sheet. Both decks carry
**2 explanatory visuals where their donors carry 0**, and both figures are also
placed in the print pack so the printed sheet has them.

**The pipeline, and the five defects it caught before anything shipped.**
`author_deck.py` (8 controls) empties every teaching block from a donor's stages
and print pack and inserts authored content, then refuses to write a deck that
carries any donor text. It refused four times, and each refusal was a real
defect:

1. **The donor's whole print pack survived** the first build — 282 words carrying
   the wrong week, the wrong title and **the donor's workbook cells**, which is a
   coverage lie printed on the sheet a pupil is handed. The leak gate had only
   read `main.deck` stages; the print pack sits outside it.
2. **Nine Lundy elements per deck were stripped**, because only `lundy-strip` was
   in the keep list and this chassis also ships `lundy`, `lundy-grid` and
   `lundy-status`. That would have broken `lundy-in-three-places`.
3. **The leak gate flagged seven blocks that were all chassis** — the banner, its
   four dimension definitions, the guide-toggle text, the nav bar. Chassis text
   is now DERIVED rather than judged: a block that also appears in a third,
   unrelated deck of the family is furniture; a block only donor and output share
   is a leak.
4. **A print heading the author had not named kept its donor text** — "Every
   profile statement bound to genuine evidence or MISSING:" on a lesson about
   strengths. Surplus headings now fall back to the deck title.
5. **A success-criteria list in the print pack** kept two donor criteria.
   Unauthored items are now removed rather than left.

**A fourth record of the stage timings, and R2 shipped without it.** Pack
manifests carry a pack-level `timings` array. After R2, `GROW_ASDAN/Spring1` held
two decks with `[0,3,3,8,3,7,4,9,3]` and `[0,3,3,7,3,7,4,10,3]` under a manifest
still claiming `[0,3,3,4,3,3,4,16,4]` — a value true of neither. Repaired here:
per-lesson timings written into every `lessons[]` entry, and the pack-level field
kept only where every deck agrees. Where they differ it is **removed**, because a
false record is worse than a missing one. DEFAULTED under N1b.

**19 Art plans PARKED, not attempted.** No Art family has a gate-readable
9-stage donor, and N3d requires one donor per family per batch.

Mechanism **17 tools, 158 controls**, derived, `--prove-red` PASS. g27 PASS.
Both packs verify with `sha256sum -c`.

**Merged** `840e7dbb52933ee1aaea646b9129a0e79af71273`, six of six checks green,
23 of 23 paths blob-verified.

**BATCH 1 CLOSE — the measured rate, stated plainly.** Batch 1 delivered **2
units and 5 cells** across one full session. The ceiling of 24 was never the
constraint; authoring was. 434 cells remain open, and a forecast that divides
them by a 24-unit ceiling is wrong by more than an order of magnitude.

**N3e's catalogue PR did not run** for this batch — hud-coverage rows were not
added for the two new decks. CI is green without them, so it is a gap in the
batch procedure rather than a broken gate. Batch 2 runs it.

---

## BATCH 2 — 14 authored lessons. PR #290

**BATCH 2: +14 units, cells 139→170, open 434→403, parked 0, main `221df575`.**

Fourteen lessons authored, gated and landed, all cover-taught weeks 1–3 — the
weeks a cover teacher reaches first.

    g23   14/14 PASS      g18   14/14 BINDING PASS
    g25   14/14 PASS      g28   14/14 PASS
    g24   14/14 RED       estate-wide print-dead (A2R R3), unchanged
    donor leakage 0 across all 14 · 31 cells claimed, 31 unique, no collision
    words 738–1373, every deck inside its family's floor and 1.25× ceiling

**How they were written.** A workflow: one writer per plan against the workbook
outcomes, then an adversarial reviewer per draft on safeguarding, outcome
coverage, SEN fit and word budget, then a rewrite of everything rejected.
**The reviewers rejected all fourteen first drafts**, and their findings were
substantive rather than stylistic — an outcome carried by a single sentence in a
staff note, success criteria offered only on the Stretch row so most of the class
could not meet the outcome, a starter that named two photographs the pack does
not contain, and a class decision the objective promised but no stage made.

**Five defects the pipeline caught before anything shipped**, on top of batch 1's
five:

1. **`data-ta1` / `data-ta2` are read by NOTHING in this chassis** — zero
   references in its CSS or its JS. Nine prep instructions and a safeguarding
   deflection script would have been invisible to the cover teacher who needs
   them. A reviewer caught it. Adult guidance now also renders as a
   `data-mbm-guide="staff"` block, which the guide toggle actually shows.
2. **Three donor blocks survived every role handler** on the LAUNCH ASDAN print
   pack, including `SoW: 'LAUNCH Weekly - Autumn'!C171` — **the donor's own
   workbook cell**, printed on the sheet a pupil is handed. Role-based rewriting
   knows only the roles it was told about, and this estate has more print
   variants than roles. A final sweep now neutralises any donor-specific block
   left standing, whatever element it lives in.
3. **The build driver keyed decks on `family+week`**, and two LAUNCH ASDAN plans
   share week 1. The second deck would have carried the first one's cells, and
   every gate would have passed it: g28 checks a cell EXISTS, not that this deck
   teaches it. Now keyed on plan index, with an assertion.
4. **Three decks measured under their family floor** (by 6, 26 and 107 words).
   Extended with real teaching — a second worked example, what to do when stuck,
   a named common mistake — not padding.
5. **Two decks declared a we-do type their text did not evidence.** Rather than
   relabel to whatever the classifier saw, the We Do stages were rewritten so the
   task verb dominates the reveal mechanic: spotting the planted mistake, and
   ordering five pictures. Both now corroborate.

**A manifest this run refused to rewrite.** The Humanities packs carry a
different schema — no `lessons` array at all, but `sequence`, `notAuthoredYet`
and `weekSpine`, written by another hand. Rewriting one added an eleven-entry
`lessons` list and pushed `lessonCount` from 8 to 11 while `plannedLessonCount`
still said 8, leaving it internally inconsistent and `notAuthoredYet` still
naming decks that now exist. **Reverted.** `pack_furniture.py` now writes the
checksum rows and leaves an unrecognised manifest alone, reporting it. Their
`sequence` / `notAuthoredYet` / `weekSpine` fields still need a deliberate
update for the three new Humanities decks — logged as **A3-H9**.

Mechanism **19 tools, 176 controls**, derived, `--prove-red` PASS. g27 PASS.
Every pack verifies with `sha256sum -c`.

---

## A3N-2 §2 — g29 plan binding, and provenance made structural. PR #291

**Ceiling: 0 lesson units** (R1: a mechanism PR counts zero).

**Why g28 was not enough.** g28 asks whether a cited cell EXISTS. It cannot ask
whether THIS deck is the one that teaches it. Twice in this campaign a deck would
have shipped carrying another plan's cells and passed the whole stack:

- the batch-2 driver keyed on `family+week`, and two LAUNCH ASDAN plans share
  week 1, so the second deck would silently have taken the first's cells;
- an authoring run was launched from a task list typed out of a console print, in
  which five of twelve cell sets and **eight of twelve outcomes** were wrong.

Both are one failure — a rendering of the plan treated as the plan — and a cell
claimed by the wrong deck is a coverage lie: the census counts it taught and
nobody teaches it.

**The binding is derived, not named.**

    planId = sha256(family | ruledWeek | sorted(cells))[:12]

so it survives the targets file being regenerated or reordered, and two plans
sharing a family and a week still differ. A control pins that.

**g29's three must-fire controls all fire**, plus two more:

    a-deck-claiming-another-plans-cells-reds            RED, extra ["'S'!C9"]
    a-deck-claiming-a-subset-reds                       RED, missing ["'S'!C2"]
    two-correctly-bound-decks-in-one-family-week-pass   PASS, PASS
    the-plan-id-survives-the-targets-file-reordered     same id
    a-deck-with-no-planId-is-skipped-not-passed         SKIP

**§2d, batch 2 re-verified: 16 of 16 PASS, 0 RED, 0 SKIP.** The binding was
backfilled by DERIVATION rather than from a list of which deck I believed matched
which plan: a deck is bound only where exactly one plan has exactly its cells.
Zero or two matches writes nothing and reports, because an ambiguous binding is
worse than none. All 16 bound, 0 unmatched, 0 with outcomes differing from plan.

**§2c PROVENANCE — a run whose inputs cannot be traced REFUSES TO START.**
`build_from_specs.py` now requires specs, donors and plans as files, records each
sha256 in the run record, and exits with `PROVENANCE REFUSAL` otherwise. This is
the fifth instance of the same mistake in this campaign; remembering not to do it
is not a control, and refusing to start is.

g29 is armed in CI on every authored deck, not only on its own controls.
Mechanism **21 tools, 184 controls**, derived, `--prove-red` PASS.

---

## A3N-2 §1, first half — the Art measurement family. PR #292

**Ceiling: 0 lesson units** (R1: a mechanism PR counts zero).

§1 says "no Art family has a gate-readable donor" is a solvable authoring task.
Picking the donor turned up something underneath it: **Art had no measurement
family at all, and no Art lesson could have passed the gate stack however it was
written.**

The style contract has treated Art as first-class since g16 v2 was frozen —
`G16_DENOMINATORS_v2.json` names twelve families and gives each Art pathway 108
contract rows, more than any other. Only FEB's `BASELINES` named nine. The two
gates that divide by a family then disagreed with each other:

    g18   no Art family  ->  GLOBAL p25 fallback           floor 1638 words
    g23   no Art median  ->  ratio is None, and the clause
                             passes only a ratio that is
                             not None                       RED, always, binding

No live Art lesson in this estate exceeds **1107** words. The floor was 1638 and
the ceiling was unreachable. This was not a strict gate but an **undefined**
one, and undefined was being read as failure — while the line that would have
said so crashed on `f"{None:.0f}"` before it could print.

**The rule was already written; it had just never been applied to Art.**
Nearest-rank p25 of the family's own live neighbours, global fallback only below
`MIN_NEIGHBOURS=5`. Each Art pathway has fourteen measurable live lessons.

    VB extra  BUILD Art    n=14  p25= 888  median=1015.5  g23 ceiling <=1523w
    VB extra  GROW Art     n=14  p25= 902  median= 918.5  g23 ceiling <=1378w
    VB extra  LAUNCH Art   n=14  p25= 885  median= 894.5  g23 ceiling <=1342w

**No threshold moved.** The ceiling is still 1.5× the family median; the floor is
still the family p25. Leaving Art out was applying a *different* rule to one
subject, not a stricter one. A control derives all nine FEB families under the
merged map and every n, p25 and median is identical; a second worktree at
`origin/main` was measured against this tree to prove it rather than assert it.

**Four controls added, all firing:**

    the-nine-feb-families-still-derive                   9 of 9
    art-now-has-a-measured-family-not-a-global-fallback  n=14 >= 5
    the-art-floor-now-sits-below-the-art-ceiling         888 <= 1523
    an-unknown-family-still-errors                       MEASUREMENT INVALID

g23 keeps the same verdict for a missing denominator — still RED, because a
ceiling with no yardstick cannot pass anything — and now carries the REASON, and
prints instead of raising.

Mechanism **20 tools, 169 controls**, derived, `--prove-red` PASS.
Re-run: `python3 _sownb/vb/tools/g18_v2_family_floor.py --families`

**A3-H10 opened, not actioned.** The `Art_Teesside/<pathway>/W1-W8` copies of
the eight `*_Estate_v3` Art lessons measure **zero** content words under the
shell-aware instrument while their twins measure ~900–1100. Same titles, two
routes, one invisible to every gate. Excluded from the baseline automatically by
the `contentWords` filter, so it moves no number here.

---

## A3N-2 §1, second half — ART_DONOR_v1. PR #293

**Ceiling: 0 lesson units** (R1: the chassis are not lessons and no lesson is
committed here). One PR, alone.

### THREE chassis, and the reason is a gate, not a preference

§1a says the donor comes from the SAME pathway. g26 derives the pathway from the
ROUTE and reds a deck whose pupil Flesch-Kincaid sits outside its pathway's band
— BUILD 1.0–4.0, GROW 3.0–7.0, LAUNCH a ceiling of 14.21. A single
pathway-neutral chassis makes g26 return **NOT-APPLICABLE**, which exits zero: a
fail-open on the one gate that reads how a lesson speaks to a child. So the
route of each file carries its pathway token, and `prove_chassis.py` treats
NOT-APPLICABLE and NO FAMILY MEDIAN as failures rather than passes.

### The choice, and the first version of the tool that made it

    BUILD   0.135  BUILD_ASDAN_W3_Cook_One_Snack_as_a_Team_from_a_Picture_Card
    GROW    0.431  GROW_Humanities_W3_Match_the_Lamp_to_Its_Meaning
    LAUNCH  0.194  LAUNCH_ASDAN_W1_Choose_Our_Community_Need_and_Launch_My_Challenge

The margin is the WORST of the measured margins, not the mean, because a deck is
only as green as its nearest red — and an unmeasurable margin disqualifies a
row rather than counting as headroom.

The first revision of `pick_art_donor.py` carried a hand-written list of what a
chassis must have. It was wrong in four places at once: it looked for `hud.js`
(in 524 files in this estate and in **not one** deck that has passed the stack
this campaign), for `tier-1..3` (this estate names its print tiers
supported/standard/stretch), for a `running-head` class only some decks carry,
and it applied g26 as a hard filter when g26 is `scope:new` and does not bind a
live deck at all. It returned **zero candidates from a corpus of 136** and the
zero looked like a finding. The signature is now INTERSECTED from the sixteen
decks this campaign has taken through the stack green — 26 markers — with the
reference set in a file whose sha256 is recorded.

### Four defects the strip found, all of them live

1. **`empty_stage` kept a bare `<svg>`.** Right for icons, wrong for figures:
   the donor's two explanatory diagrams are direct children of their stages and
   carried "A routine in order / Step 1 needs nothing first" straight through.
   No shipped deck was affected — all sixteen carry their own two figures — but
   a chassis that kept them would have put one donor's diagram on every Art
   lesson.
2. **`render_figure` could never draw its columns shape.** It reads
   `spec["kind"]` to choose between chain and columns, and a block's own `kind`
   is already `"figure"`, so every figure authored through that path came out a
   chain. Batch 2 never hit it because both its decks passed raw `<svg>`. Now
   keyed on `shape`, with a control that renders both and compares them.
3. **`build_batch.py` still keyed on `family+week`.** That is the exact
   non-unique key g29 was written to catch after the fact; two cover-taught
   LAUNCH ASDAN plans share week 1. It now takes `--plan-index` and refuses an
   ambiguous family+week rather than silently taking the first match.
4. **A sweep that mutated the tree under `tree.iter()`.** lxml's walk is live;
   `_clear` removes children, the walk lost its place, and **seventeen donor
   blocks survived** — the running head, the workbook cells and every success
   criterion — with no error at all. `list()` before touching the tree.

### How a chassis is proved, given it teaches nothing

§1c says "gate as a FIXTURE deck, full stack green". Taken literally that cannot
be done honestly: a chassis has no pupil words, so g18's floor and g23's load are
not green on it, they are **meaningless** on it. So each chassis is EXERCISED as
a fixture — a real planned Art lesson is authored onto it and the whole stack
runs on that — and every gate is run on the DONOR too, with identical arguments.

    green on the probe                       -> PASS
    red on the probe, red on the donor       -> PRE-EXISTING, named
    red on the probe, GREEN on the donor     -> REGRESSION, and the run fails

That is stricter than matching the campaign's own flag choices, because nothing
can hide behind a scope setting. It caught a real one: LAUNCH's first draft came
in at 802 pupil words against its family floor of 885 and was reported as a
regression, not as a pass.

    BUILD   PASS  1013w  floor 888   x1.00  FK 1.95 in 1.0-4.0
    GROW    PASS   940w  floor 902   x1.02  FK 3.96 in 3.0-7.0
    LAUNCH  PASS  1025w  floor 885   x1.15  FK 5.07 under 14.21

**Three gates are red on the donors too and are named rather than dropped:**
g16 (the frozen v2 contract is RED on everything measured, including the live
Art decks it was written for, 86–88 of 108 rows), g19 (ten `:root` declarations,
zero scoped), and g24 at `--scope new` (one explanatory visual where the row
wants two, and print-dead — A2R R3's finding about the shell hiding the slide
container under `@media print`). A tool that failed the chassis on those would
be reporting the estate's backlog as this work's defect.

### Digests, per §1c

    BUILD_chassis.html   d394897a427883d8…  from BUILD_ASDAN_W3
    GROW_chassis.html    93ece5826cb52c3a…  from GROW_Humanities_W3
    LAUNCH_chassis.html  ea4f0a7e1145cb26…  from LAUNCH_ASDAN_W1

Each records its own donor and that donor's sha256 in its `lesson-config`, and
`prove_chassis.py` reads the comparison baseline from there rather than being
told — comparing against the chassis instead of the donor made every content
gate read PRE-EXISTING and reported PASS on a deck below its family floor.

Three Art content specs are committed (`BUILD_ART_W1`, `GROW_ART_W2`,
`LAUNCH_ART_W1`). They are inputs, not lessons; the decks they proved are not
committed. Batch 3 authors them to their routes.

**A fifth defect, found by CI within a minute of the push.** The new evidence
files carried `"verdict": "PASS"` with the subject under `out`, and the estate's
stale-evidence sweep reads a JSON evidence record structurally only when some
record names its subject under `file`. It fell back to reading the text, found a
bare verdict line with no path on it, and reported exactly what it exists to
report — a verdict whose subject cannot be seen. Both tools now name the subject
under `file`, and `prove_chassis` names the chassis rather than the probe,
because the probe is deleted at the end of the run and an evidence record
pointing at a file that is gone is the definition of stale. The sweep is now run
locally before a push; it takes seconds.

Mechanism **23 tools, 201 controls**, derived, `--prove-red` PASS.
Stale-evidence sweep: 0 inconclusive rows.

---

## BATCH 3 — twenty-four lessons, Art among them for the first time. PR #294

**Ceiling: 24 of 24 lesson units.** Batch full.

    W1  Art      BUILD, LAUNCH
    W2  Art      BUILD, GROW, LAUNCH
    W3  Art      BUILD, GROW, LAUNCH
    W4  ASDAN    BUILD, GROW, LAUNCH   Humanities BUILD, GROW, LAUNCH   Art BUILD, GROW, LAUNCH
    W5  ASDAN    BUILD, GROW, LAUNCH ×2   Humanities BUILD, GROW, LAUNCH

Week-major, ASDAN → Science → Humanities → Art, per §5. Every deck 24/24 PASS.

### Nine plans held back, each with the reason on the page

Six Science plans read *"Baseline assessment (PythonAnywhere) — no new science
content; unit starts W3"*. Authoring a teaching deck against an outcome that
says there is nothing to teach would be shipping something doubtful, and BUILD
Science's family floor is **1229** pupil words, which a baseline-assessment
session cannot honestly carry. The cover teacher does need a session sheet for
these; what it should contain is a ruling, not a gate's decision. **A3-H11.**

Three plans are RESHELL — they name a standing deck to reshell rather than a
lesson to author, which is a different pipeline. **A3-H12.**

Both are recorded in the target list itself, so the cells stay visibly open
rather than quietly missing.

### The target list is generated, and it carries the spec name

`build_batch3_targets.py` writes the batch from `EASTER_TARGETS.json` with that
file's sha256 recorded in what it writes. It also writes the **content spec
filename into each row**, and that is not tidiness: `LANE_SUBJECT_Wn` is not
unique. Two cover-taught LAUNCH ASDAN plans share week 5, and two shared week 1
in batch 2. A driver computing the name at use would have handed the second
plan the first plan's content, and every gate but g29 would have passed it.
Colliding names are disambiguated by the plan's own derived id.

### Every gate run twice, on the deck and on its donor

`prove_chassis` judges comparatively: green is a pass, red where the donor is
also red is PRE-EXISTING and named, red where the donor is green is a
REGRESSION and fails the deck. It caught four real ones during the run —
LAUNCH Art W1 at 802 words against a floor of 885, LAUNCH ASDAN W4 at 989
against 1058, LAUNCH ASDAN W5B at 1001 against 1058, and BUILD ASDAN W4 at
**FK 4.16 against the BUILD ceiling of 4.0**.

**That last one is worth keeping.** Almost all of the 4.16 came from the tier
ladder: a list whose items carry no terminal punctuation reads as ONE sentence
to any Flesch-Kincaid measure, so a three-item ladder counted as a forty-word
sentence. Punctuating the items took the deck to **3.20** with no change to a
word of teaching. It is a real reading-load fact, not a scoring trick — a
ladder read aloud has sentence boundaries in it — and it is now applied to
every spec this campaign writes. The two batch-1 specs were deliberately left
alone, because their decks are already shipped and a spec must stay in step
with the deck built from it.

### A3-H9 CLOSED — the Humanities manifests, in their own hand

§3 ruled: never rewrite a schema somebody else wrote; derive the grammar from
the rows already there; prove the round trip; any delta beyond the intended rows
is a revert.

`manifest_sequence.py` does exactly that, and the round trip is **measured, not
assumed** — the file is re-serialised with no changes at all and the bytes must
come back identical, with the serialisation derived per file. One manifest in
the estate does not round-trip: `Science_Teesside/Launch/W14-W15_2026-27` keeps
its `cadence` array on one hand-formatted line, which no `json.dumps` with
indentation reproduces. It is **REFUSED** rather than reflowed, and a control
pins that refusal.

The `lessonCount` / `plannedLessonCount` question that caused the earlier revert
is settled by measurement: every manifest in this estate carrying both has them
**equal**, and equal to `len(sequence)`. So they move together, and a control
checks that invariant across the estate before the tool writes anything.

    BUILD/GROW/LAUNCH Humanities   8 -> 10 lessons, 320 -> 400 minutes

The diff is the two rows and the three derived counts. Nothing else.

**A finding, logged not fixed.** Those folders hold *more* unlisted decks than
this batch added — batch 2's three Humanities decks and three older `*_HUM_W2`
files. This run added only what it authored and printed the rest; folding
somebody else's decks into a manifest inside a lesson PR would hide the drift
rather than record it. **A3-H13.**

### Two defects the batch found in the pipeline

1. **`deck_row` compared values, not provenance.** A deck whose week really was
   the template row's week read as "unfilled" and was refused, and the message
   blamed the deck. Two of this campaign's own decks were rejected that way.
   It now tracks which keys were filled from the deck.
2. **A new evidence format the estate's own sweep could not read** — see
   WRONG_BEFORE_RIGHT. CI caught it within a minute of the push.

### Furniture

Nine packs re-verified with `sha256sum -c`: three new Art packs created with
manifests and checksums, three ASDAN packs extended, three Humanities packs
given checksum rows with their manifests left to `manifest_sequence`. Existing
checksum rows are untouched in every case; only new rows and `manifest.json`'s
own digest moved.

Mechanism **25 tools, 223 controls**, derived, `--prove-red` PASS.
g29 across every authored deck: **43 decks, 40 PASS, 0 RED, 3 SKIP** — the three
skips are the chassis, which carry no `planId` and are correctly not treated as
lessons. g27 PASS. Stale-evidence sweep: 0 inconclusive rows.

---

## A file #294 deleted that #293's record cites

Blob-verifying #294 turned up one path that did not match: 90 of 91. The odd one
was `_sownb/vb/evidence/a3n/art_donor_pick.json`, the §1a margin measurement —
removed during the batch-3 run while its tool's controls were being repaired, and
never regenerated, so the batch commit deleted it. #293's ledger entry quotes its
numbers and tells the reader to re-run the tool.

Regenerated. **The pick is unchanged**: the same three donors at the same margins,
now measured against a corpus of 25 signature-complete decks rather than 16,
because batch 3's own decks joined it. A choice that survives its corpus growing
by half is a choice worth recording as stable.

The tell: `rm` in the middle of a repair, with the regeneration left to the end
of a long run. The blob verification is what found it, which is what it is for.

---

## A3N-3 §2 — the selector ruling, and the defect it uncovered. PR #296

**Ceiling: 0 lesson units.** No new lesson. Twenty-four existing ones repaired.

### What the ruling asked for, and what looking for it found

§2 ruled that the donor filter had decided what existed: it dropped every
nine-stage Art deck, and "no Art family has a gate-readable donor" was a filter
artifact rather than a finding. Print the exclusions with reasons, fix the
filter, add a must-not-exclude control naming the eighteen, and register the
pattern — family+week keying, the typed task list, the donor filter — as three
instances of **a selector deciding what exists**.

Doing that turned up a fourth instance, and it had shipped.

### `sweep_donor_text` deleted the navigation bar from fifteen of batch 3's decks

The sweep removes any text block present in the donor and absent from the family
reference. A deck's **navigation is exactly that**: every chassis generation
words its buttons differently, so the button row is never shared text between two
families. It read the row as donor leak and deleted it — Previous, Next, Teacher
tools, Evidence & print, Calm mode, all of it. Nothing errored, because a sweep
that drops in silence has nothing to error about.

**A cover teacher opening one of those decks could not move between stages with
the mouse, reach the print pack, or turn calm mode on.**

Batches 1 and 2 survived **by accident**, and the accident is the part worth
keeping. `all_text_blocks` only reports blocks of eight words or more. The BUILD
and GROW button rows separate their labels with spaces — *"Previous Teacher tools
Evidence & print Calm mode …"* is thirteen words — so they crossed the floor and
were swept. The LAUNCH rows run their labels together with no space, so they
counted under eight and were never offered to the sweep at all. **Whether a deck
kept its navigation depended on whether somebody had put a space between two
button labels.**

`strip_to_chassis` already had the guard — I wrote it there while building the
chassis and never carried it into the tool that ships the deck. The predicate is
now defined once, in `author_deck`, and imported by the strip.

**Both halves had to move together.** With the sweep fixed and the leak gate left
alone, twenty-two of twenty-four decks then reported a leak of exactly one block,
and that block was the button row: the gate reads text, and the donor's button
labels are legitimately present in both. The leak gate now excludes control
surfaces too.

**All twenty-four batch-3 decks rebuilt, 24/24 PASS, navigation restored,
9–11 buttons each.**

    the-navigation-survives-authoring          9 buttons -> 1 without the guard
                                               9 buttons -> 9 with it

### The selector rule, stated once and checked in g29

> Every selector that narrows a candidate set must print its exclusions with
> reasons before the set is used.

It lives in g29 because g29 exists for the same shape one level down — a deck
carrying the wrong plan's cells that every other gate passes. The control runs
each selector this campaign ships on a planted input that forces it to drop
something, and asserts every dropped item comes back with a reason:

    pick_art_donor.is_candidate
    build_batch_targets.build
    author_deck.sweep_donor_text
    manifest_sequence.plan

with a must-fire twin: a planted selector that drops three items and explains one
is caught. Red-proved — blanking one reason in the sweep names the offending
tool and function by name.

### The filter, fixed

The requirement that a donor already carry a `lesson-config` was wrong, and it
was the single predicate that dropped all forty-two nine-stage Art decks.
`strip_to_chassis` **writes** a fresh lesson-config into the chassis, so the
filter was demanding something the pipeline supplies for itself. Markers are now
split into what the strip supplies and what the donor must already have — derived
from the strip, not listed — and the scan covers **699 deck-shaped files** with
every exclusion printed, where the first version reported only the 136 that
survived it.

    signature 26 markers, 1 of them supplied by the strip
    deck-shaped scanned 699   signature-complete 40   excluded 659, each with reasons

**The must-not-exclude control names the eighteen** Spring2 `OUTSTANDING_V3` Art
decks by path and asserts that each is dropped only for furniture it genuinely
lacks and the strip cannot invent — never for a marker the strip supplies, never
for one the file actually has.

### ART NOW DONATES TO ART

With the filter fixed, an Art deck is the **best-margin candidate in BUILD**:

    BUILD   +0.153  BUILD_Art_W3_Find_Out_About_An_Artist_Whose_Work   (Art)
            +0.135  BUILD_ASDAN_W3_Cook_One_Snack…                     (the old pick)
    GROW    +0.098  GROW_Art_W3_Plan_An_Identity_Portrait_Or_Piece     (Art)
    LAUNCH  +0.158  LAUNCH_Art_W1_Set_Arts_Development_Goals           (Art)

`BATCH4_DONORS.json` uses those three. **ART_DONOR_v1 is retired as a donor** and
kept as the record of how the Art packs were bootstrapped.

### The part of §2 the measurement does not support, stated plainly

The forty-two Art decks that pre-date this campaign are still not donors, and the
reason is now a fact about each file rather than an artifact. They carry **no
guide toggle, no print pack and no splash** — `#n6m-guide-css`, `#n6m-guide-js`,
`data-mbm-guide`, `.print-pack`, `.print-page`, `.n6-lc-page`, `.n6-splash` — all
furniture the strip preserves and cannot invent. A chassis stripped from one
would produce Art lessons with nothing to print and no adult guidance drawer:
the two things the cover window most needs.

And after a strip that removes every word of content, a donor contributes only
furniture. Those decks' furniture is a strict subset of the campaign
generation's, so an Art source of that vintage would give an Art lesson less,
not more. **The three Art decks now used as donors are Art decks that carry the
whole chassis**, which is the version of "use an Art source" the measurement
supports. Logged as **A3-H14** if you want the older Art packs brought up to the
current chassis instead.

Mechanism **25 tools, 223 controls**, derived, `--prove-red` PASS.
g29 across every authored deck: **43 decks, 40 PASS, 0 RED, 3 SKIP.**
Stale-evidence sweep: 0 inconclusive rows. Nine packs verify with `sha256sum -c`.

---

## BATCH 4 — the run that died on an account limit, and what it cost

A3N-RESUME-B4 asked for state before resumption, from the thing and not the
record. Here is what the thing said.

### The workflow record, read from its own file

`~/.claude/projects/…/workflows/wf_26809076-34b.json`, 33 agents, 2 881 593 ms,
1 596 743 tokens, status `completed`. "Completed" is the harness's word for
*finished running*, not for *did the work*:

    Author  19 agents   14 returned   5 failed
    Review  14 agents    0 returned  14 failed

Every one of the nineteen failures carries the **same** error string, verbatim:

    You've hit your monthly spend limit · raise it at
    claude.ai/settings/usage?from=cc_cli_limit_message ·
    your session limit resets 4pm (UTC)

The five red author plans, with the tokens each had spent when it died:

    plan-62  BUILD Humanities W7   117 494 tokens — file WAS written before it died
    plan-63  GROW Humanities W7     80 958 tokens — file WAS written before it died
    plan-64  LAUNCH Humanities W7        0 tokens — never ran
    plan-65  BUILD Art W7               0 tokens — never ran
    plan-67  LAUNCH Art W7              0 tokens — never ran

**Why Review shows 0 of 14 is the question worth asking, and the record answers
it exactly.** All fourteen review agents were *scheduled* — they exist in the
run's agent list with labels and a model — and every one recorded **0 tokens**
against a spend-limit error. So it is neither "never started" nor "fourteen
review failures": the phase started and every agent died at its first request.
The review MECHANISM was never exercised and is therefore neither proved nor
disproved by this run. That distinction decides what to do: not a mechanism-fix
PR, but a re-run.

Fourteen decks were authored by an agent and **reviewed by nobody**. The review
is the step that made batch 2 work — all fourteen of batch 2's first drafts were
rejected by it. Gating fourteen unreviewed drafts because the gates went green
would be trusting the gates to do a job they have never done: gates measure
words, bands, shape and provenance. They do not read a lesson.

### The stash, emptied

One entry, `stash@{0}`, a three-parent WIP on this branch. Its untracked parent
`6c3a9ac` held exactly two files — `GROW_HUMANITIES_W7.json` and
`LAUNCH_ASDAN_W7.json`, 1007 lines — and its tracked parent held nothing. Both
are batch-4 authoring, so both were popped onto the batch-4 branch and are
committed here with their plan rows. `git stash list` is now empty, and nothing
in this campaign is left in a stash.

### The five red plans, recovered

- **62 and 63** were written to disk by their own agents before the limit killed
  them. The files are complete and valid; the agents died after the write. They
  are recovered from disk, not re-authored, and they go through the same review
  as everything else.
- **64, 65 and 67** never ran, and were authored in this session, one attempt
  each, from `BATCH4_TARGETS.json` read as a **file** —
  `sha256 2a535e7e75069afe6886edf12cf05c84ec1657505cb84b8c701c759a4c085920`,
  recorded by `run_batch` in its own evidence — and never from a console print.

Nothing was parked. The ceiling was not touched.

### The review, re-run — and it was not a formality

Thirty-eight agents, two lenses per spec, pipelined: a conformance pass (shape,
stage titles and minutes, pupil word count against the family floor, list
punctuation, figure pairing, JSON) and then a teaching-and-safeguarding pass on
what the conformance reviewer had already been through.

    38 agents · 0 errors · 30 FIXED · 7 PASS
    98 changes recorded against the seven lenses:
      A teaches the plan's outcome                11
      B the safeguard is real                     25
      C no asserted attendance, venue or booking  12
      D the teaching is actually taught           26
      E TA notes are actions an adult performs    18
      F the tier ladder is a ladder                4
      G voice                                      2

**Every one of those decks had already passed all nine gates green.** The gates
measure words, bands, shape, leakage and provenance. They do not read a lesson.
Three of the findings say what that difference is worth:

- **A stage that could not be taught.** BUILD Art W5's "We Do 2 · lab" had
  pupils check a partner's photograph and swap sheets — but no stage before it
  had told anybody to take a photograph, and the photo does not reach the sheet
  until the Independent stage. A cover teacher arrives at minute 23 with nothing
  to check. The shot is now taken in that stage.
- **A safeguard resting on words the deck never supplied.** GROW Art W5's sort
  named "six review cards" and never said what one said, so its guarantee that
  every comment comes from an approved list rested on text that did not exist —
  and the stage's own claim that "two cards are close, so tables will disagree"
  could not be true of cards nobody had written. The six card texts are now
  printed.
- **Twelve asserted attendances, in an estate where nothing is booked.**
  "Next week an employer visits our class community project." "You get about ten
  minutes with them." "An arts event is a public arts offer you attended." Two
  questions "asked at last term's visit", with what the visitor said and for how
  long. All twelve now read from the approved pack instead. This is precisely
  what AAE-R1B's g32 exists to catch, found on decks g32 has not yet been
  pointed at — and found by reading, not by measuring.

The one number a batch-3-style run would have reported is the one that was
already true before any of this: nineteen greens.

### Gated one deck at a time

R5: never one monolithic shell that can be stopped 53 seconds in and lose its
place. Each deck was built and gated in its own shell under its own wall
ceiling, sized as the order specifies — the first green deck measured **4s**, so
the ceiling is 4×3 floored at **60s**. The slowest deck took **6s**.

The shell output is deliberately **not** committed. The first version of the
driver wrote a plain-text timings log and kept each deck's stdout beside the
JSON record, and rows reading `plan 49  rc=0  4s  PASS  idx 49` state a verdict
in a shape matching none of the estate's claim forms. The stale-evidence sweep
exits 2 on a single `NO FORM MATCHED` row — *"the run does not pass with one
outstanding, because the alternative is calling it stale"* — and nineteen logs
plus a timings file failed CI. Every fact those rows carried is in
`batch4_build.json`, per row, in a form the sweep reads; the logs are
reproducible by re-running the driver.

    19 of 19 built · 19 of 19 PASS · 0 regressions · 0 donor leakage
    g18 19 PASS   g23 19 PASS   g25 19 PASS   g26 19 PASS
    g28 19 PASS   g29 19 PASS
    g16 · g19 · g24 PRE-EXISTING on all 19 — the donors carry them too

    family              wk  words   floor  ceiling   cells
    BUILD Art            5   1025     888     1523   C106
    GROW Art             5   1014     902     1378   C106
    BUILD ASDAN          6   1099     950     1457   C135 C149 C179
    GROW ASDAN           6   1020     906     1397   C135 C149 C179
    LAUNCH ASDAN         6   1293    1058     1610   C93 C121 C163
    LAUNCH ASDAN         6   1281    1058     1610   C219
    BUILD Humanities     6   1342    1209     1837   C65
    GROW Humanities      6    834     700     1076   C65
    LAUNCH Humanities    6    832     668     1038   C205
    BUILD Art            6    989     888     1523   C107
    LAUNCH Art           6   1032     885     1342   C149
    BUILD ASDAN          7   1200     950     1457   C136 C150 C180
    GROW ASDAN           7   1059     906     1397   C150
    LAUNCH ASDAN         7   1218    1058     1610   C220
    BUILD Humanities     7   1493    1209     1837   C66
    GROW Humanities      7    987     700     1076   C66
    LAUNCH Humanities    7    775     668     1038   C206
    BUILD Art            7   1017     888     1523   C108
    LAUNCH Art           7    998     885     1342   C150

**27 cells, 27 unique.** R6 asked that GROW ASDAN W7 be allowed to be thin
rather than padded: it came out of the review at **1059** against a floor of
906, because the review added teaching rather than words. LAUNCH Humanities W7,
the thinnest deck in the batch, went 684 → **775** against 668 the same way.

### Furniture and mechanism

Nine packs, **104 checksum rows, all OK** under `sha256sum -c` after the
rebuild. The three Humanities manifests moved 10 → 12 lessons, 400 → 480
minutes, and were reproduced byte-identically on a second run from restored
originals. Mechanism **25 tools, 226 controls**, derived, `--prove-red` PASS —
223 at batch 3 plus the three controls this run added. It reads 26 tools once
the Arts Award register PR lands, which adds g30.

### Batch 4 landed

    #297 merged 5966015b41379c158533069bea4be0d99ff37f5a
    89 of 89 paths blob-identical between origin/main and branch head dfe99f54
    six checks green, run 33901872775

Ceiling **19/24** for batch 4. Estate cells covered by this batch: **27, all
unique**.
## AAE §1 §3 §4 — the Arts Award register, the slots file, and six gates

**Ceiling: 0 lesson units.** Registers and gates count zero. Queued behind the
19 Art plans per the order; branch cut and built while batch 4 authors.

### The register is the spec until a PDF replaces it

`tools/artsaward/SPEC.json` is written once from §1 and is the only source any
deck, staff block or gate may cite. It carries, per level: title, RQF level,
qualification number, guided and independent hours, who it is open to and who it
is designed for, the standard, UCAS where there is one, every part with what it
requires, the marking scheme, the Attempted rule, the file cap and the
assessment areas — three for Explore and Bronze, **four** for Silver and Gold.

Gold's **Attempted rule and file cap are recorded as UNKNOWN**, toolkit-only,
with "never inferred from Silver" written into the file. A gate reds a deck that
states either.

    Explore  600/3894/9  Entry 3   35h  4 parts  cap 10  3 areas
    Bronze   501/0081/6  Level 1   60h  4 parts  cap 10  3 areas
    Silver   500/9914/0  Level 2   95h  9 parts  cap 20  4 areas
    Gold     500/9666/7  Level 3  150h  9 parts  cap UNKNOWN  4 areas  16 UCAS

The z-fold leaflet is recorded in the file as **not a source**; the 44 exemplar
decks are recorded as exemplars only.

### The slots file is one edit, not a rewrite

`tools/artsaward/SLOTS.json` holds EVENT, ORG, PRACTITIONER and SHOWING, each
naming which level and part it serves, with three routes — pupils visit, they
come in, live remote exchange. Five candidates are seeded and **every one is
UNCONFIRMED**; no slot has a booked entry. Decks are authored route-agnostic, so
a slot changing is a one-file edit.

### Six gates, one file, fourteen controls

They all divide by the same register and all need the same answer to "what is
pupil-facing text on this deck". Six files would be six copies of that answer
kept in step by hand — and this campaign has just shipped a defect of exactly
that shape, a control-surface predicate written in one tool and missing from the
next, which deleted the navigation bar from fifteen decks. One file, six gates,
each reporting its own verdict; `--gate g31` runs one.

    g30-an-explore-deck-calling-itself-level-1-reds
    g30-ucas-outside-gold-reds
    g30-a-file-cap-stated-for-gold-reds
    g31-a-unit-1c-called-organisation-research-reds
    g31-leadership-in-an-explore-deck-reds
    g31-leadership-in-an-arts-challenge-deck-reds
    g32-a-hardcoded-venue-reds
    g32-a-dated-event-reds
    g33-a-silver-list-missing-parts-reds
    g34-a-share-part-with-no-sharing-step-reds
    g35-a-mandatory-gantt-chart-reds
    g35-a-gold-attempted-rule-reds
    a-deck-that-names-the-award-and-declares-nothing-reds
    a-correct-deck-of-each-level-passes

**Scope is declared, and a deck cannot hide from it.** A deck is judged when its
lesson-config carries an `artsAward` block naming level and parts. A deck that
names the award and declares nothing is RED under `--scope new` — otherwise the
cheapest way past every gate would be to say nothing where the gates read.

**Binding on new work, report-only on live**, like g23's ceiling and g26's band.
The estate holds **76 deck-shaped files** that name the Arts Award and predate
the register. Reddening them all on the day it lands would manufacture a backlog
nobody asked for.

### The last control is the one that matters

`a-correct-deck-of-each-level-passes` exists because five of the other thirteen
prove a gate can go red, and none of them proves it can go green. Its first
version had a Gold fixture that reddened on g32 — Gold 1B needs ORG_SLOT and the
fixture declared none. **The gate was right and the fixture was wrong**, which is
the outcome you want from that control.

### g31 had to learn what the exemplar actually got wrong

The first version checked that a named Part exists at that level. The exemplar's
mistake was subtler and worse: it named a part that **does exist** and gave it
the wrong meaning — "Unit 1C = organisation research", when Silver 1C is
reviewing arts events. Filed that way, the work goes into the portfolio under a
part that wanted something else, and the adviser marks it there. g31 now
compares the words after a part token against the register's name for it, and
reds when they share no content word. Sharing one is a paraphrase; sharing none
is a mislabel.

### The contamination list, and the 191 findings that were not findings

`docs/ARTS_AWARD_BSG_CHECK.md` is generated, not written: per level, requirement
→ served by → evidence route → verdict, then every contradiction with deck and
line. Every requirement row reads **OPEN**, because nothing declares yet.

Its first run returned **49 files with 191 contradictions, every one of them the
word "ticket"** — because every deck in this estate ends on a stage called *Exit
Ticket*, and §4's g32 lists "ticket" among the things that red. Worse, §6b
explicitly **keeps a ticket as primary evidence**, so flagging the word argued
against the order that asked for it. The two clauses are reconciled by reading
g32 as it is meant: a ticket kept as evidence is fine; a ticket **booked or
brought for an attendance the deck asserts** is not.

Narrowed, the list went to zero — and a zero from a pattern that has just been
narrowed is the number to distrust, so the survey now carries its own must-fire:
a planted deck asserting a visit, a date, a venue and an invented requirement is
reported on all four, and a deck keeping a ticket as evidence is reported on
none. Both fire.

**What it then found is real: three live Art decks name MIMA in their own text,
eleven times between them** — the thing §3 exists to prevent, in decks that
predate it. Reported, not gated, because they are live.

Mechanism **26 tools, 237 controls**, derived, `--prove-red` PASS.

### The census the register makes possible, measured after batch 4

`g30 --scope live` over every HTML file naming the Arts Award, run the way CI
runs it:

    82 decks name the Arts Award   0 declare a level to the gates
    Art_Teesside 66 · GROW_Estate_v3 8 · BUILD_Estate_v3 8
    authored by this campaign (carry a planId) 17 — 7 BUILD, 6 LAUNCH, 4 GROW
    predate the register 65
    inferred level: Bronze 29 · Explore 26 · Silver 20 · undetermined 7
    3 with contradictions — the three MIMA decks, the same three R2 found

**Two things in that worth reading twice.**

R3(i) scopes the census to the 76 live Art decks. **Sixteen of the 82 are not in
`Art_Teesside`** — eight in each of the two `Estate_v3` folders. A census scoped
by folder misses them, so it is scoped by what a deck *claims*, not by where it
sits.

And **seventeen of the undeclared decks are this campaign's own.** They name
Trinity Arts Award Discover, Explore or Silver Unit 1 in their slot line and
declare nothing a gate can read. Report-only under `--scope live`, which is
right for work that predates the register — but they are new work, and the
register is what makes `--scope new` mean something for the Bronze, Explore and
Silver decks still to be authored.


## AAE-R1B R2 — the venue mentions, classified line by line

R2: classify every line EXAMPLE (an organisation named as teaching content or
"e.g." — keep) or ASSERTED (the pupil's visit, attendance or booking — convert
to an `ORG_SLOT`/`EVENT_SLOT` read). *Do not strip MIMA as an example: a
Teesside Art deck may name Teesside's gallery.*

`tools/artsaward/venue_classify.py`, 5 controls, all firing. It searches for
all five candidate organisations in `SLOTS.json`, not only the one the order
names.

    20 mentions   1 ASSERTED   19 EXAMPLE
    every one of them MIMA — The Auxiliary, Sawdust, Navigator North and
    Platform A appear nowhere in the estate

    4  Art_Teesside/Build/BUILD_ART_A2_W2_Arts_Inspiration.html
    6  Art_Teesside/Build/BUILD_ART_W2_Artists_Makers_and_Teesside_Connections.html
    1  Art_Teesside/Grow/GROW_ART_W4_Arts_Event_Attend_Capture_and_Review.html   ASSERTED
    3  Art_Teesside/Build/Spring2_2026-27/SPRING2_SOURCE_AND_ORGANISATION_CARDS.html
    3  Art_Teesside/Grow/Spring2_2026-27/SPRING2_SOURCE_AND_ORGANISATION_CARDS.html
    3  Art_Teesside/Launch/Spring2_2026-27/SPRING2_SOURCE_AND_ORGANISATION_CARDS.html

**The order's number reconciles exactly, and the extra nine are worth having.**
Eleven of the twenty are in the three *teaching decks* R2 names — 4 + 6 + 1 —
which is the eleven. The other nine are in three copies of one *card pack*, one
per pathway, where an organisation card reads *"Organisation card · MIMA.
Middlesbrough Institute of Modern Art describes itself as an art museum and
gallery…"*. That is the textbook EXAMPLE: content about an organisation, making
no claim that anybody went. A classification scoped to decks would have left
them unexamined, and the estate would still not know what they said.

### The one ASSERTED line, and why the drawing survives it

`GROW_ART_W4_Arts_Event_Attend_Capture_and_Review.html`, line 359:

    <text …>ADMIT ONE</text> … <text …>MIMA · GALLERY · SHOW</text>

A decorative SVG ticket, lettered with a venue, in a deck about attending an
arts event. **A ticket depicts an attendance whatever the words around it say** —
it tells a pupil they are going to a named place, and nothing in this estate is
booked. The conversion is one string:

    '>MIMA · GALLERY · SHOW<'  ->  '>GALLERY · SHOW<'

The ticket graphic stays. The venue comes from `EVENT_SLOT`, which is
`UNCONFIRMED`, which is the truth.

Nineteen EXAMPLE lines are untouched, by design and by the order. A control
holds that default open: *a bare fact defaults to EXAMPLE, because a Teesside
Art deck may name Teesside's gallery.* Another refuses to apply a conversion
whose string no longer matches its file, rather than editing blind.

### R3(i) — the census answer, measured rather than promised

The survey checks **eight** kinds of contradiction against the register. Across
all **82** decks that name the Arts Award, seven of them return zero:

    a level name that is not this deck's level          0
    a qualification number that is not this deck's      0
    UCAS outside Gold                                   0
    'leadership' in an Explore deck                     0
    a dated event inside the deck                       0
    a visit asserted in the deck                        0
    a requirement the register does not carry           0
    a venue named in the deck rather than in SLOTS.json 10 → 9

**Not one deck in this estate makes a false factual claim about the Arts
Award.** Every finding was a venue mention, and R2 classified those: one
ASSERTED, nineteen EXAMPLE. So R3(i) repairs nothing — and that is the census's
answer, not its failure to look. *"Zero units unless a deck is materially
rewritten"* resolves to zero, with the seven zeros printed above as the reason.

**Ten against eleven, and both right.** The survey counts *lines*; the
classifier counts *mentions*. In the same three decks that is 10 against 11,
because line 341 of `BUILD_ART_A2_W2` carries two — a pres-card `🖼️ MIMA` and
the answer line `MIMA or own answer`. A record that reported one of those
numbers without the other would look like a discrepancy for the rest of the
campaign.

**One caveat stated rather than buried.** g32 judges only decks that declare an
`artsAward` block, and every live deck is UNDECLARED, so g32 itself never
judged the converted line. The classifier is the measurement here. g32 binds
the Bronze, Explore and Silver decks still to be authored, which is where a
binding gate can do its work.

## The two things that stopped a Bronze deck being authorable

Found by trying to build one, not by reading the code. `author_deck` has
authored 59 decks and every one of them claims a workbook cell.

**1. There was nowhere to put the declaration.** The lesson-config is assembled
from the plan, and it had no `artsAward` key. All fourteen Bronze decks would
have landed UNDECLARED — the exact condition the register was built to end, and
RED under `--scope new`. The declaration is now carried from the plan, because
it belongs to the plan and not to the prose: *a deck cannot be in the scheme for
a reader and out of it for the gates.*

**2. A cell-less plan raised on its own source block.**
`cfg["source"]["cell"] = plan["cells"][0]` is an `IndexError` on an empty list,
and AAE-H7 rules that the Bronze decks have one. A plan with no workbook cell
now gets no `source` key rather than a `source` with an empty cell in it.

### The part that needed thinking about rather than patching

`_plan_id` keys on `family | ruledWeek | sorted(cells)`. With cells empty that
collapses to **family and week** — precisely the non-unique key g29 exists to
catch, and Bronze runs **two decks a week**. Every Bronze pair would have shared
an id.

A cell-less plan now keys on its own **Arts Award declaration and title**:
content of the plan, exactly as the cells are, so the id still survives the plan
file being reordered. Both halves are pinned — a must-fire twin proves the two
week-5 Bronze plans get different ids, and the reorder control proves the id
does not move.

### Key order is part of what shipped

`source` sits between `objective` and `timings` in every deck this campaign has
authored. The first version of this change appended it instead, which is
invisible in review and would have made every rebuilt deck differ from the deck
that shipped. Written back into its own position, and **proved**: a landed
batch-4 deck rebuilds **byte-identical** through the changed pipeline.

    author_deck 16 controls, all fired (13 + 3)
    mechanism 26 tools, 243 controls, derived, --prove-red PASS


## AAE-R1B continuation — Bronze batch opening, 2026-09-04

Matt supplied the governing AAE-R1B order again. Bronze AUTHOR 14 comes first,
then Explore 14, then Silver 14; each batch stays within 24 lesson units.
Questions are not a gate. The Lessons repository has one writer. Reviewers and
draft authors may work outside it; only the root writer integrates changes.

Remote main is `ea2e4f696712d226838a0b2f51ffcb307224e9eb`. #302's five changed
blobs were independently compared from its actual fork base `9fd27b1b` and all
five match the landed merge. The pushed continuation `94ede65e` has NINE specs,
A1–A6 and B1–B3, rather than the eight named in the handoff. No open PR overlaps
those paths or the planned Bronze routes. The inherited work is retained.

**Batch opening:** 14 planned / 24 allowed; 0 landed this run. Bronze workbook
cells **0 → 0**, deliberately unclaimed under AAE-H7. Gold new cells **0**;
Gold remains shelf-only. These are strand claims, not an estate coverage count.

Reading the saved plan against R3(ii) found B running into week 6 and D starting
only in week 7. The plan's prose also called the fourth B deck its third.
The corrected fourteen-slot sequence keeps all nine drafts: B3 teaches the
actual experience, review and evidenced share in week 5; C1/C2 remain weeks 5/6;
D is plan in week 6, delivery and review in week 7. No extra lesson unit is added.

Content review found the wrong tier labels, an A3 one-file-per-session direction,
incomplete file-plus-page locators, B directions treating handwritten initials
as mandatory, and missing EVENT_SLOT declarations. These are draft defects to
fix before the batch is built, not evidence that a shipped deck passed.


## The award identity reached the writer but not its gate — zero units

Resuming AAE-R1B from #302 reproduced a g29 RED on the first Bronze deck.
The writer used the award-aware identity introduced by #302; the gate still
loaded only workbook plans and still calculated the old empty-cell key.
Measured: all 262 workbook identities are unchanged; the fourteen Bronze
identities are distinct, while the old formula produced only seven.

A shared identity helper and explicit PLAN_SOURCES registry now bind g29 to
canonical workbook and award plans. Missing sources, duplicate identities,
stale source digests, changed target rows and changed award declarations fail.
The batch driver preserves per-deck input hashes and refuses missing specs or
an empty selection. Existing workbook semantics and bytes are preserved: a
landed BUILD Art W5 deck rebuilt byte-identically.

Slot-dependent decks now read the current SLOTS.json. Hosted reads bypass the
cache; offline staff can select that same file. Invalid or unconfirmed data is
visibly preparation-only. Candidate names are never copied into deck HTML.
The six reader controls exercise the actual JavaScript file/fetch code. A
Chromium UI check runs separately in CI; it has not been claimed from a local
browser, whose executable download was unavailable.

Mechanism: 27 tools, 271 declared controls, all fired; --prove-red caught its
planted failure. The first reader wrapper emitted JSON but not the battery's
required `n/n controls` line; the battery rejected that missing report. The
wrapper now reports its measured count and the unchanged battery passes.

The early sparse-checkout probe also errored in g18 because its legacy Science
baseline was absent. That is an incomplete environment, not a pre-existing
lesson defect. The complete checkout is now used for all batch gates.


## Award presentation checkpoint — zero units, PR 303

The first fourteen Bronze builds passed the comparative nine-gate stack; a
separate award run rejected the generated coverage note as a part name. The
trace now uses a semicolon and a direct g31 control proves that distinction.
Reading the HTML found unrelated donor print figures, blank headings, a
dropped fifth checklist item and toolbar labels calling different actions.
New award decks now generate their complete print sheets from their specs,
replace the legacy runtime, retain the live slot reader inside Teacher tools,
and use their own browser title. Existing non-award output is unchanged.

The author has 19/19 controls; the complete 27-tool battery has 274 controls
and its planted failure fired. Chromium UI proof remains pending on this
updated head; the previous CI failure was an intercepted-header assertion,
not a reader failure. The no-store source control stays. A disposable generated
fixture and the actual fourteen-deck browser gate now cover toolbar, keyboard,
modal, source-matched print and file-reader behaviour. These are checks of
behaviour and print content, not a claim about PDF pagination.


## Bronze fourteen-deck build checkpoint — 14 of 24 units

All fourteen authored specs are now built in week-major order. Each completed
its own sixty-second-ceiling shell, taking 8.36–9.11 seconds. All passed the
comparative stack; g16, g19 and g24 remain explicitly pre-existing on the
donor, not newly green. The independent g30–g35 pass is 14 of 14. Reading
values remain inside BUILD; content words range1092–1333 against888–1523.
The pack contains14 lessons,560 teaching minutes and an ordered start page.
It does not claim to deliver the entire60-hour award programme.

PartA: W1A1/A2,W2A3/A4,W3A5/A6. PartB: W4B1/B2,W5B3. PartC: W5C1,W6C2.
PartD: W6D1,W7D2/D3. EVENT_SLOT is read by the threeB decks. Suggested
evidence uses four cumulative part files within the10-file cap; no completed
pupil evidence is asserted. Bronze workbook cells0→0 underH7; Gold newcells0.
GROW placement remains a separate later transaction.

The PR303 browser fixture passed after correcting its missingUTF-8 declaration.
The actual fourteen generated decks still require their content-branch browser
run before merge. This checkpoint preserves the output; it is not a claim
that the content has landed or been served.


## PR303 merged and verified; Bronze browser proof

PR303 merged as4f36647151a525911e3dfd15b7d502b3c198ac9a after allseven
current-headjobs succeeded. All18changedblobs match the head, compared from
actualforkea2e4f696712d226838a0b2f51ffcb307224e9eb. Ledger andstate updated
beforecontinuing. The local/APIcommitgraphs differ, so mergingmain produced
record-onlyconflicts. Resolved by keeping the laterBronzecheckpoint plus the
identicalmechanismrecords, ratherthan restoringmain'sold g29-skipstatement.

PR304 browserrun33915719252/job101162293053 passed bothgeneratedfixtureand
allfourteenactualBronzedecks: toolbar,nav,focus/modal,livefileinputandthe
source-matchedprintcontent. TheseHTMLbytes have not changed since that run.
Retargetingto main now enables the remainingestatechecks; no contentmerge
is claimed yet.

PR304 now targets main at 4f366471. The byte-identical lesson outputs retain
the completed browser proof; the current head must also pass every estate job.
The source-figure control rebuilt114figures, with zero differences.


## Bronze front-door identity correction

Current-head browser run 33916590384 passed. Estate run 33916590307 found
a genuine metadata mistake: START_HERE used lesson-config, so the donor
control treated this pack index as a lesson missing its planId. The index
now uses pack-config. No lesson or gate is changed, and the checksum is
refreshed. The original control is retained. Full CI must pass on the new head.


## AAE assertion-scope correction — zero lesson units

R1 requires asserted attendance and booking to fire, while ticket examples,
Exit Ticket headings and organisations used as teaching examples must remain
allowed. Direct controls found missed asserted bookings and false positives
on examples, historical dates, observed file counts and Silver's truthful
restriction that its arts challenge must not focus on leadership.

The focused correction keeps all fourteen original controls and adds twenty-nine
positive and negative controls. g33 and g35 are unchanged. Natural explicit
sharing instructions are accepted; a draft swap without a final evidenced share
continues to fail. Both the old and corrected gate pass all fourteen Bronze
decks. The full battery passes: 27 tools, 303 controls, planted difference caught.

This is a separate zero-unit mechanism change. Bronze PR304 is not merged by
this record; merge order and current-head CI remain required.




## Bronze PR304 merged and blob-verified

Bronze merged as 2f7eda8e62096cd23fef8128b92c3563ed170bc3 after all seven
current-head jobs passed (runs 33917362837 and 33917362798). All 58 changed
blobs match, compared from the actual fork at 4f366471. merge304.json records
the full path list. Fourteen lesson units landed against the 24-unit ceiling.
Bronze cells remain 0 → 0 under AAE-H7. Gold new cells remain 0. Placement
is still pending. Ledger and state are updated before further batches.




## Silver multipart plan projection — same zero-unit mechanism PR

The canonical Silver plan truthfully assigns working with others alongside
practical planning and delivery. The old reader silently discarded secondary
parts. The source reader now retains each declared part and derives the union
of its slots, while rejecting empty, duplicate or contradictory declarations.
The existing single-part projection and IDs are unchanged. Seventeen permanent
controls expose the old loss and check the full source-to-target-to-deck binding.

The reconciled mechanism battery passes with 28 tools and 323 derived controls,
including 44 g29 controls and 43 award-claim controls. Its planted battery
failure is caught. Current-head CI remains required before PR305 merge.


## Mechanism evidence subject correction

CI run 33918746857 passed all functional checks but could not parse two
expected PASS labels in the historical negative-control report: the report
had omitted the file it measured. It now names the pre-fix reader and commit.
Merge blob rows also use the established file subject key, so JSON suffixes
are not truncated by the fallback text-path scanner. No result is altered,
no evidence is removed and no sweep rule is relaxed.

## Assertion follow-up — attendance references, zero units

Four truthful Silver denial or record-question references were false positives. Each exemption now matches the immediate grammar of that attendance occurrence only, including joined HTML paragraphs. All 43 prior controls remain unchanged; 24 new must-fire and benign controls bring g30–g35 to 67. The genuinely unconfirmed practitioner promise still reds and was corrected in the Silver source before rebuilding. No content batch or gate floor changes.

## R2 current-slot read follow-up — zero lesson units

The earlier MIMA edit removed the asserted ticket venue but did not actually
read ORG_SLOT. Reviewing the live GROW W4 prose also found remaining promises
of this week's event, onward sending and an unverified prior-cohort outcome.
The historical census's regex zero did not establish a full prose review.

This factual correction adds a working current-source reader to the actual
div.slide chassis. ORG_SLOT is an organisation reference, while EVENT_SLOT
independently supplies the applicable Bronze Part B route. Empty slots stay
preparation only. Screen/print duplicate claims are corrected together; all
ten stage timings, existing cells, styles and SVGs remain. All allowed MIMA
examples in the other decks and card pack remain unchanged. Twelve adapter
checks pass; actual rendered browser checks are required before merge.

## Verified merge #305

Exact head `99b8c114c4443f96da92151edc5fb7c991ef15df` merged as `fb96752c63077c41774673dcf3628c6f39cdb2d8`. Against actual fork `2f7eda8e62096cd23fef8128b92c3563ed170bc3`, all 12/12 changed blobs match. Evidence: `_sownb/vb/evidence/aae/merge305.json`. Required head runs: 33920574791. This record does not itself claim served-byte equality.

## R2 evidence subject correction — zero units

Current-head browser passed, but the estate sweep rejected the adapter report because its PASS rows lacked a subject file. The generator and regenerated report now name the actual deck. The structural snapshot uses repository-relative paths. No control, reported result, gate or game was changed to clear this failure.

## Explore next-batch plan checkpoint — 0 of 14 authored

Bronze has fourteen authored, built and award-gated decks, and its actual
fourteen-deck Chromium check passed on PR304. While the merge sequence
finishes, the next branch records fourteen Explore plans before authoring.
Ceiling24; next planned units14. No Explore deck has yet been written.
The registered requirements govern; original AAEsection5 has not been
recovered, so chosen media and weekly distribution are implementation
choices, not invented order text. An independent24-cell scan finds no
complete claim ready for this strand/week. No cell is invented or reassigned.
Explore stays BUILD-only and distinct from Bronze.








## Explore fourteen-deck pack checkpoint

All fourteen Explore decks are authored and built, with zero donor leakage.
Each passes the comparative nine-gate stack; g16/g19/g24 remain PRE-EXISTING
on the same donor. The separate binding g30–g35 scan passes all fourteen.
Measured teaching words span 1091–1308 in the BUILD Art 888–1523 band; pupil
FK spans 2.52–4.00 inside BUILD 1–4. Core retains all required evidence.

The sixteen checksum rows cover fourteen lessons, the start page and manifest.
A1–A4 serve two arts activities; B1–B4 require artist and organisation experience
through live or active work; C1–C4 retain a distinct artwork, its process and
final work; D1–D2 support choice and actual sharing of enjoyment/achievement.
Both Part B slot keys are read from the current source. The suggested four-file
layout is within the ten-file cap. Independent workbook review supports zero
new cells, without inheriting Bronze's H7 ruling. Browser proof is pending.

## Verified merge #306

Exact head `0f47b3de44b0b6680ea921362fd3959c5c20960f` merged as `e808f0aa1367925a8b88098c134c38d44a4fa384`. Against actual fork `fb96752c63077c41774673dcf3628c6f39cdb2d8`, all 9/9 changed blobs match. Evidence: `_sownb/vb/evidence/aae/merge306.json`. Required head runs: 33921327174,33921327049. This record does not itself claim served-byte equality.
