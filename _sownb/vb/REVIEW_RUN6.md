# REVIEW — Order VB run 6

Phone-shaped, easiest first. **Nothing was authored and no lesson file was changed.** Two things I was told to do turned out to be blocked or unnecessary once measured; both are explained below with what I found instead.

## Phase 3 closes — and the real defect is bigger
The recorded finding was 51 confirmation blocks that fail to print. That figure was measured against the CSS page and is invalid, so I re-measured every candidate by rendering it to PDF.

**183 decks have a confirmation block. 104 print it. 79 do not — and in every one of those 79 the entire PDF is blank.** Not one deck prints content but loses only its signature line.

So the placement fix Phase 3 was built around applies to **zero** decks. Every deck with the block inside `.print-pack` prints it — 56 out of 56, no exceptions — and 48 more print it from outside the pack too. Phase 3 closes here, as the order says it should.

What I found instead is worse and more useful. Those 79 decks build their print output into a `#print-area` div. The div is populated — 15,819 characters of it on the one I traced — and it is visible under print. But every `.print-section` inside it computes to `display:none`: the print stylesheet switches the container on and never switches the sections back on. I ruled out the two obvious alternatives (it is not waiting on a `beforeprint` event, and there is no hidden ancestor).

It looks like one CSS line per deck. I have not applied it: that is a rule addition, not the placement move this run permits, and 79 files is well past the ceiling.

Also worth knowing: the pilot pack I was pointed at, LAUNCH Humanities W9–W14, has no confirmation blocks at all. There was nothing there to pilot.

## The LAUNCH Science relabel is blocked — one question unblocks it
A rename would touch 83 files, seven of them read-only workbook ground truth, so the label-and-citation route is the right one. That part is ready.

But the relabel is a chain — W14→13 needs 13 free, which needs W13→12, all the way down to W9→8. **Week 8 is held by the enzyme/amylase trio, and there is no enzyme row anywhere in the LAUNCH workbook.** I searched every row, every strand, every term: zero matches.

The arithmetic says the same thing. The workbook has 12 taught Biology weeks; the estate has 12 week-labels plus the correctly-placed Autumn2 pack. The enzyme week is one extra, and it is what pushed everything after it a week late. Moving it down to week 7 instead would collide with the v3_40min W7 trio, which is correctly placed and sits in a protected production tree.

Doing six of the seven would knowingly create a collision at week 8. Deciding what the enzyme week *is* would be me inventing curriculum. So I stopped and left everything as it was.

**The question:** the enzyme/amylase week has no workbook row. Is it (a) extra enrichment that should sit outside the numbered sequence, (b) part of the Topic 1 review week alongside the v3_40min W7 trio, or (c) a workbook row that is genuinely missing? Any answer unblocks the whole relabel; the exact edit for all six weeks is written out and ready.

## One g18 now, and nothing moved
There were two implementations of the same measurement. FEB's was already correct, so mine now delegates to it and computes nothing of its own — it only adds the printing discipline (family, n, per-family floor, legacy global floor, verdict, tool version on every line). All 32 Phase-1 lessons re-scored under the single implementation: **zero flips, zero reds.**

## What your two asks actually look like today
Measured, not guessed. Full detail in `BASELINE_VISUALS_WEDO.md`.

**Visuals.** Of 350 live lessons, **180 have no explanatory diagram at all** — 51%. The estate median is zero and the best lesson anywhere has two. All three Humanities families have none between them.

**"We do" variety.** Only 56 lessons have a stage titled "We Do". Three activity types carry about 85% of them, and **BUILD ASDAN runs twelve consecutive lessons with the same type-set.** Two genuinely useful types are nearly extinct: predict-then-check appears 3 times in the estate, spot-the-error once.

I have proposed a six-type rotation built from what is there plus those two gaps, and six contract rows in `PROPOSED_CONTRACT_ROWS_RUN6.md`. **None are applied.** None are proposed as binding on existing lessons — every one of them would red half the estate overnight.

## The one thing that blocks the next build
Confirming the six "we do" types. Everything else can be adopted alongside the first new lesson; the taxonomy has to exist before drafting, because the rotation rule is defined in terms of it.
