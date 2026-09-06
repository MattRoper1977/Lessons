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

## The CI check that was red is fixed
Two separate things, and the check was right about both.

**Mine.** 192 VB evidence files said `"status": "PASS"` and never said *what*
passed. The stale-evidence sweep treats that as a verdict it cannot check — its
hardest finding — and refuses to pass on it. It is right: a gate report that
says PASS without naming its subject is not evidence. Every one of them now
names the file it judged, taken from what the record already knew rather than
typed in by me.

**Broken by this branch.** That alone did not clear it. The sweep prints its
report and then exits; on a pipe those writes are asynchronous and the exit
throws away whatever is still queued. Two runs of the *same* sweep over the
*same* tree kept 23 KB and 428 KB of a 729 KB report. The control it feeds
plants its own test rows at the very end, so the part thrown away was exactly
the part being checked — a control going red because its output vanished, which
is the one thing that control exists to prevent.

One line: the sweep now writes synchronously. The report is byte-identical
before and after, the exit codes are identical, and I broke the form on purpose
first to confirm the control can still fail. All four checks this workflow runs
pass locally.

That is one line in a shared FieldOps tool. **Say if you would rather it came
out and the check stayed red** — I would rather tell you I touched it than have
you find it.
