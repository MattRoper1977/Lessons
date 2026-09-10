## D12 — Build a counterfactual to contradict you, not to pass

LF1-B §2.2 required that no page carry two adjacent nodes with identical text.
Measured on live: **0**. Measured on the fix: **0**. A two-column table would have
recorded that as a pass, and it would have proved nothing — the invariant reads 0
on live only because the pupil line said "the next unit" while its staff twin said
"W14", so they were never identical to begin with.

The third column is what made it an invariant rather than a formality: the
restorations applied with the twin deletions **withheld** — **9** adjacent
identical nodes. That is the measure firing, and it is the only evidence that the
9 deletions are necessary rather than tidy.

It also caught an instrument fault. The first counterfactual returned **6**, not
9. A standalone probe found a pair on `BUILD_HUM_W9` that the census called
absent — 232 characters, byte-equal, adjacent. The census was wrong: these decks
persist the chosen tier, so the guide pass's `page.reload()` came back showing
only the last tier the deck walk had pressed. It was measuring one tier's DOM and
calling it the page. Fixed with a fresh context; 6 → 9.

That fault was found only because the counterfactual supplied a number to
disagree with. A measurement that agrees with your expectation teaches you
nothing; give yourself something that can contradict you and check whether it
does.
