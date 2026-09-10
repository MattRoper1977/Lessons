## D22 — R-CAL-1 does not apply to `Tutor_Time/` or `Assembly/`

LF1-M §8e. Stated here so no future relabelling pass reaches for them.

The tutor-time sessions carry **batch slots**, not spine weeks. "Batch 03 · 28 Sep"
is a position in a publishing run of three linked morning sessions a week; it is
not `Aut1·W4`, it does not map through `_sownb/TERM_DATES.md`, and it has no
manifest week to be relative to. A tool that turned a batch number into
"Lesson n of N" would be inventing a sequence that does not exist — the same
class of error as the 121, with a different vocabulary.

**So:**

- `tools/relabel_public.py` is never run over `Tutor_Time/` or `Assembly/`, in
  report, apply, revert or gate mode.
- Batch and week labels in those trees are **not** bound to spine or calendar
  tokens, and the forbidden-token gate's vocabulary does not govern them.
- The placeholder dates (14 Sep → 14 Dec, break week of 26 Oct) are **not**
  resolved against the real calendar and are never presented as scheduled (§8f).
- `[PLANNED]` sessions are proposals: no route, no card, no catalogue entry.

The naming follows the same logic and is ruled in §2a: successors route under
`Lessons/Tutor_Time/<strand>/<id>/` with strand folders `Behaviour`,
`Safeguarding`, `British_Values`. Cards, hub copy, catalogue entries and search
text say **"Tutor Time"**, never "assembly". `Assembly/` survives only as the
three genuine assembly routes among the retiring originals, plus their three
posters, behind successor-pointer pages. **No new `Assembly/` routes.**

The estate already agreed with the ruling before it was made: across the 42 decks
measured, visible text carries `tutor*` 126 times against `assembl*` 61, and not
one `<title>` says assembly.
