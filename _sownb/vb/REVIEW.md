# REVIEW — Order VB run 2 (Phase 1, cohort A)

One screen per surface, easiest first. Twelve surfaces: eight lessons, four front doors.

## The one thing that changed
LAUNCH Science W14 front door (`Science_Teesside/Launch/W14-W15_2026-27/START_HERE.html`).
It still told readers "Held local candidate: nothing in this pack is pushed, merged, deployed or catalogued" — untrue since RSH-3 landed it.
The paragraph is gone; checksums regenerated; every front-door check passes with its red controls firing. PR #189.
Worth a look: open the page, confirm the notice is gone and the three lesson links work.

## GROW ASDAN W7 front door — VERIFIED
House style, logo painted, home link resolves, no residual note, links resolve. Nothing to look at.

## GROW Science W7 front door — VERIFIED
Same battery, all green. Nothing to look at.

## LAUNCH ASDAN W13–W14 front door — VERIFIED
Same battery, all green. Nothing to look at.

## GROW ASDAN W7 lesson — VERIFIED
g16 pinned contract, g18 floor, g19, g10, g15, render install, s24 print, running heads, g21, confirmation + signature in the printed PDF page 3. All green.
Worth a look: it prints on 3 pages with the learner confirmation on the last.

## GROW Science W7A and W7B — VERIFIED (2 surfaces)
Full battery green. Confirmation prints with signature line.
Worth a look: reading level measures easier than the W8–W13 pack median (FK ~8 vs ~10.3) — printed as a deviation, not changed.

## LAUNCH ASDAN COMM W13 and W14 — VERIFIED (2 surfaces)
Full battery green. These print on 2 pages, confirmation on page 2 — tighter than the old 10-page chassis, no near-blank sheets (g21 green).

## LAUNCH Science W14 L1, L2, L3 — VERIFIED (3 surfaces)
Full battery green including the named safeguarding strings on all three. Confirmation prints with signature line.

## What the reds actually were (none of them content)
Four instrument artefacts, each proven at the call site and recorded in WRONG_BEFORE_RIGHT.md:
1. FEB's offline metric forbids localStorage; the pinned RSH-3 contract row does not (the guide feature requires it).
2. FEB's token regex is swallowed by the RSH-3 provenance comments (`<!--RSH-W7A:v1-->`); strip comments and every token is found once, correct.
3. The control-count row's pinned references (8/7) don't reproduce on the rows' own donor decks (6 rendered) — row MEASUREMENT INVALID, rendered parity with live donors recorded instead.
4. START_HERE firing controls no-op on a case difference (`#4A6FA5` vs stored `#4a6fa5`); the corrected mutation fires.

## What could not be measured from this venue
Public 200 + body-hash binding: the network policy denies mattroper1977.github.io. MEASUREMENT INVALID, all twelve, not relabelled. Link targets verified on disk instead.
