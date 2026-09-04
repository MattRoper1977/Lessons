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
