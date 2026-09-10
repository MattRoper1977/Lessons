## D27 — gates measure rendered output, never source

Any gate whose subject is what a pupil can see is measured in a **laid-out page**.

A regex over source is not a measurement of visibility: it cannot see a payload
the page renders, and it cannot see where the page renders it. `innerText` on a
**detached** clone is not one either: with no layout it degrades to `textContent`
and swallows every `<script>` body.

Both produced confident, specific, false findings this week — the first said V08
showed a pupil-facing YouTube URL when it sits in the staff aside; the second said
25 of 42 decks failed §8a when none does.

**Applies to every pupil-visible gate in the estate.** Existing gates that still
read source are listed in `_sx2/tutor_time/GATES_READING_SOURCE.md`. They are
**listed, not fixed**, under this order.
