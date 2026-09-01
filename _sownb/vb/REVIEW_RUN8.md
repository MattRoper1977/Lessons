# REVIEW — Order VB run 8

Phone-shaped. Easiest first.

## Both PRs from last night are in
#191 (the proof lesson) merged as `46ad336e`. #192 (the ten allowlist entries)
merged as `5d89522c`. All 411 files #191 changed are byte-identical on main.

## The one thing to look at
**The proof lesson now reads at the level you asked for.** It measured Flesch–Kincaid
5.60. Your ruling put BUILD at 1.0–4.0. It now measures **3.53**.

I rewrote 28 blocks of prose into short plain sentences, one idea each. I did not
touch a single task, timing, tier label, diagram or the print layout — that is what
makes it a repair rather than a rewrite. And I did not strip the hard words to win:
SPACE, VOICE, AUDIENCE and INFLUENCE are your participation model, so they stay, and
they now have a plain-English bridge behind the Word help button.

Worth a look: open week 1 and read a stage aloud. It should sound like it is meant
for the room it is for.

## The thing I think you need to know
**Nothing else in the estate is anywhere near these bands.**

| pathway | live lessons | the easiest one | your band |
|---|---|---|---|
| BUILD | 62 | 6.25 | 1.0–4.0 |
| GROW | 45 | 7.43 | 3.0–7.0 |

Not one live BUILD or GROW lesson is inside its band. The rows only bind on new
work, so nothing is retrospectively failed and nothing breaks — but from now on new
lessons will read noticeably plainer than the lessons beside them. That is a real
change in house voice, and it is your call whether that is what you want.

LAUNCH had no band on record, so I set a provisional one from its own live lessons:
**11.64–14.21**, from 82 of them. One line from you replaces it.

## The worksheet has three blank rows now, not six
Your rule: a row only exists if a pupil can fill it in that period. The independent
stage is 16 minutes and the hardest route asks for two people — so two rows, plus
the one spare you allow. The print still comes out at two pages with the
confirmation on the last.

## D1 is done
The enzyme/amylase week becomes enrichment with no fixed week, exactly as you said,
and the six later weeks move onto the workbook's own numbering. I checked it twice
without looking at a single week number — once against what each lesson is *about*,
once by printing it and reading the PDF. Both agree.

A bonus: this **removed three collisions** that were already there. Nothing new
appeared.

## The flush fix stays, and I proved it
You said red-proof or revert. Reverting it loses between 450KB and 750KB of a 921KB
report, differently every time, and the line being checked vanishes in all ten
trials. With it, 921,154 bytes every time. Written to a file the report is
byte-identical, so it changes *when*, not *what*. KEEP.

## What I did not do
**I did not author the eleven new lessons.** The batch is planned, the cells are
traced, the we-do types are assigned and the reading bands are known —
`_sownb/vb/WAVE3_RUN1_BATCH.md` lists it week by week. But eleven decks at the full
standard is more than this run could finish properly, and a deck that cannot pass
its own battery is not a deck. Run 9 builds them.

The catalogue entry is also not in yet — it lands alone, after the ruling PR merges.

## Two mistakes of mine, both caught by measuring
- I renumbered the front-door weeks in the wrong direction, and every week cascaded
  onto week 8. Caught by counting the labels instead of trusting the patch.
- My first attempt to prove the flush fix broke the file syntactically, so it measured
  a crash rather than the defect. Redone from the exact original.
