# REVIEW — Order VB run 7

Phone-shaped. Easiest first.

## The one thing to actually look at
**A new lesson exists.** BUILD Humanities, Autumn week 1, "People Special to Me".
Open it, press through the nine stages, then print it. Two pages: a worksheet
with the three-link table, and the learner confirmation with a signature line.

`Humanities_Teesside/BUILD_W1-W8_2026-27/BUILD_HUM_W1_People_Special_To_Me.html`

`_sownb/vb/PROOF_LESSON_NOTES.md` is the one-screen version: what it teaches,
why those two diagrams, and **one question I need you to answer** about reading
level before weeks 2–8 get built.

## The finding I withdrew
Run 6 said 79 decks print blank. **They do not.** My harness never clicked a
route button; the decks were fine all along. Driving each deck's own
`printPack()` gives 4–5 real pages with the confirmation on the last.

The fix I had proposed — one line of print CSS — would have forced *every*
route's sections visible at once and wrecked 79 working decks. **Nothing was
patched.** 0 changed, 0 skipped, finding withdrawn.

## The contract rows are in
Six new rows, all `scope: "new"` as you asked, so **no live lesson is judged by
them**. 457 rows → 463. Landed in PR #190, merged.

They cover: how many explanatory diagrams a lesson needs, how many decorative
ones it may have, the six kinds of "We Do", the no-repeat-within-three-weeks
rotation, a ceiling on words per period, and a requirement that a lesson states
its period length.

## D1 is still parked
You left the answer blank, so nothing was relabelled. It stays open.

## What went wrong before it went right
Six things, all mine, all in `_sownb/vb/WRONG_BEFORE_RIGHT.md`. The two worth a
sentence:

- **My worksheet table had no lines on it.** Blank rows with no borders — a
  writing table you cannot write on. The print gate caught it as a paper-economy
  disagreement; I only found the real cause by reading the numbers rather than
  arguing about which instrument to believe.
- **The "we do" gate could not fail.** It checked that the deck declared one of
  the six types, and nothing else — a deck could declare "commit-and-reveal"
  over a sorting activity and go green. It now checks the declaration against
  what the stage actually says, and I proved it red on three broken decks first.

## Not done this run
- Catalogue / `resources.json` entry for the new pack. That lands **alone**, per
  the rule that content and catalogue never travel together. First item of run 8.
- Weeks 2–8. Planned in `_sownb/vb/WAVE3_PLAN.md`, not started.
