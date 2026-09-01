# REVIEW — Order VB run 5 (Phase 2)

Phone-shaped, easiest first. Nothing was authored, edited, renamed, moved or deleted. This run measured, ruled, and wrote down decisions.

## The headline: the week-14 "double-booking" is not duplicate work
LAUNCH Science looked like it had six lessons fighting over week 14. It doesn't. The workbook settles it outright:

- **C44** = Autumn 2 Week 6 = **absolute week 13** — "Research a genetic condition online; present."
- **C45** = Autumn 2 Week 7 = **absolute week 14** — "Topics 2 to 3 assessment (Dec)."

So the assessment trio (`SCI_L_A2_W7L1–L3`, cites C45, declares week 14) is **correctly placed**. The genetic-condition trio (`SCI_L_W14L1–L3`, cites C44) is **week 13 content wearing a W14 label**.

And it isn't a one-off. Matched topic by topic, the whole older LAUNCH Science run is exactly one week late against its own cells — mitosis, growth, stem-cell ethics, DNA, Punnett, genetic conditions, all +1. Only the newest pack is aligned, which is precisely why it collides. The master order asked me to re-check whether that offset still held. **It does.**

Nothing needs writing. It needs relabelling — proposed below, not applied.

## The other week 14: BUILD Humanities
Two decks claim it. The workbook backs one of them:
- `BUILD_HUM_W14_Festivals_Display_and_Reflection` cites C59 ("Make a festivals display; evidence") — the workbook's week 14. Correct.
- `BUILD_HUM_W14_Industry_and_Nature_The_Tees_Story` cites no cell, and its local-history topic matches no BUILD Humanities row anywhere in the workbook. It's part of an older Teesside local-history sequence that predates the current scheme.

I have not touched it. What to do with a pre-workbook pack is your call, not a defect I can rule on.

## The overload question — answered, and the answer is bad news
I hoped the six overloaded lessons were written for double periods. They weren't.

The real timetable is **40-minute periods throughout**, and I checked every lane and day for the same subject running in two consecutive slots: **zero doubles**. All six sit in single 40s. Each declares nine stages summing to 40 — the plan is honest; it's the reading load inside it that doesn't fit.

So all six split-or-trim decisions stand. None dissolved.

One thing worth seeing while I was in there: the **Build lane has no explicitly-ASDAN slot at all** in the real timetable. BUILD ASDAN lessons are being written for slots that have to be borrowed from Community project, PfA, Careers and Enrichment.

## The instrument sweep
Run 4 found one contaminated glob and I assumed the fault was in the shared helper. It wasn't — and the sweep turned up something better: FEB already shipped a **per-family** floor in `g18_measurement.py`, and it already excluded the zero-slide pages. My v2 had partly reinvented it.

Comparing all nine families, the two derivations agreed on eight. The one disagreement was **mine**: my GROW ASDAN glob captured only the PEQ strand (6 lessons) when that pack also teaches COMM and ENT (18 lessons). A family floor built from one strand of three isn't a family floor. v2.2.0 now imports FEB's baselines instead of keeping a second copy.

Effect: GROW ASDAN floor 947 → 958, median 954 → 991. Three g23 ratios moved slightly. **No verdict changed anywhere, and no Phase-1 verdict depended on it.**

## Gaps — scoped, not filled
The week map came out **54 MATCH, 30 GAP, 0 COLLISION, 0 ORPHAN** once cells are honoured. Every gap is early-term (Humanities weeks 1–8, Science weeks 1–2) and pre-dates all of this work. The run-4 "GROW Science week 14 gap" was my own index reading a `W7` filename instead of resolving Autumn 2 Week 7 to absolute 14 — that gap does not exist.

## What I've stopped us relitigating
There's now a **NO-TOUCH register** in the state file. The two label-only collisions (GROW Science W7, GROW ASDAN W1–W6) are in it: same week *number*, different actual weeks, because terms restart their numbering. They are not defects. Any future run that re-flags them has to cite the register and move on.

## Decisions waiting for you
Six, all in the state file's `decisionPacket`, easiest first. The short version:
1. Relabel the LAUNCH Science run to match its cells (metadata only, exact before/after listed) — recommended.
2. The six overloaded lessons: split or trim. Word deltas given.
3. The untraced BUILD Humanities local-history pack.
4. Whether the Build lane's missing ASDAN slot is real or a timetable labelling matter.

Nothing above has been applied.
