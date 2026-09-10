## D20 — RULE R-CAL-1, when a calendar token may be re-tokenised

Ruled by Matt, 2026-09-09. Landed verbatim below and in the docstring of
`tools/relabel_public.py`, which is its enforcement mechanism.

> **RULE R-CAL-1 · WHEN A CALENDAR TOKEN MAY BE RE-TOKENISED**
> Ruled by Matt, 2026-09-09. Governs relabel_public.py and any successor. The refuse-don't-guess behaviour of #466/#473 is its enforcement mechanism.
>
> **PRINCIPLE**
> A week label is re-tokenised only when the referenced week resolves from an authority the tool can read. Where it cannot, the existing literal label stands. A correct literal label is not a defect; a wrong token is. The tool improves accurate labels — it never replaces an accurate literal with an inaccurate token.
>
> **RESOLVE — re-tokenise**
> R1. The referenced week lies inside the folder's own sequence AND the manifest entry for that week carries both a file and a week value.
> R2. Range references (W2–W3) resolve only when BOTH endpoints satisfy R1. A half-resolved range is a refusal, never a partial rewrite.
> R3. Array-shaped manifests resolve identically to sibling-week manifests where entries carry file, week and id (per #473's evidence). Shape is not a reason to refuse; missing data is.
>
> **REFUSE — leave the literal untouched, exit non-zero, file byte-unchanged**
> F1. Referenced week outside the folder's sequence (below min or above max). Majority case, correct behaviour, not a backlog. A cross-unit reference is authored prose about another unit.
> F2. No manifest claims the file.
> F3. Manifest claims the file but the entry carries no week. (D19: manifest defect, referred for data repair, not resolved by the tool.)
> F4. Manifest shape unrecognised. Refuse cleanly; never crash — a crash tells you nothing about the files after it.
> F5. Reference ambiguous: two entries claim the week, or it matches none.
> **F6. Entry carries an explicit no-week marker. The literal label stands. Not a defect, not a backlog, no repair.** *(added by Ruling 2, LF1-M, 2026-09-09 — see D19 as amended)*
> Every refusal names file, token, reason code, and quotes the sentence.
>
> **NEVER**
> N1. No fallback string, no placeholder, no opt-in variant, no pupil-visible stand-in of any kind.
> N2. No inference from neighbouring weeks, file order, filename or surrounding prose. Recovery from an authority, or refusal.
> N3. No partial write. Wholly rewritten or not at all.
> N4. No proxy proof. A run reports resulting text, not the disappearance of the input.
>
> **REPORTING**
> Every run outputs: resolved count, refused count by reason code, crashed count (must be 0), and a sample of resulting text for at least five resolutions across pathways. A run that resolves 0 and refuses all is a valid, reportable outcome — not a failure to work around.
>
> **CONSEQUENCE ACCEPTED**
> Most Science pages carrying a calendar token will not be re-tokenised by tool. That is the correct outcome. Re-tokenisation improves labels the tool can verify; it is not a coverage target to maximise.

### What adopting it changed in the tool

`--measure` is new: the REPORTING block as a dry run, writing nothing, so the
numbers and the resulting text can both be read before a byte moves. Three
behaviours changed to match the rule, and each of them **narrows** what the tool
will write:

- **F2 is now a file-level fact.** A file its folder's manifest does not list is
  refused whatever week it names. "Lesson 3" on a page that is not in the
  sequence is a claim about a sequence the page is not in. 26 files that the
  tool used to answer for now refuse.
- **F5 exists.** Two manifest lessons claiming one week used to produce
  `Lessons 3–4`; a bare `W9` does not say which, so it refuses.
- **The letter clamp is gone.** `min(k, len(ns) - 1)` turned `W7B` in a
  one-lesson week into lesson A. That was N2 inference from file order wearing a
  resolution's clothes — the same class of guess as `the previous unit`.

Measured over all 290 `Science_Teesside` pages: **resolved 54 → 27 files.**
R-CAL-1 refuses 27 files the implementation before it would have rewritten. The
178 that already refused did not move; they were re-attributed to F1 68 / F2 109
(83 folder has no manifest, 26 manifest does not list the file) / F3 13, plus 15
F5 and 12 F2 arriving from the old rewrite column. Crashed 0.

### Two things only reading the output could find (N4)

1. **`'BUILD Weekly - Spring'!C29` became `'the curriculum workbook`.** The cell
   pattern never consumed the opening quote, and `!B41, C41` left `, C41`
   stranded. Ten rewrites across the estate went through that path. A count of
   rewrites reports ten successes; reading the text reports an orphan quote on a
   pupil-facing page. Fixed, with the estate's real cell strings as fixtures.
2. **The sibling-week pathway fires zero times on the whole estate.** Of 80
   rewrites: 47 own-week, 20 `last week` → `last lesson`, 10 SoW cells, 2 term
   labels, 1 academic year, **0 `Lesson k`**. The code path that authored the
   121 wrong labels is now dead on this content — not by being removed, by
   never resolving.

### UNSEEN — a bucket the rule does not have, and why the report shows it

Four `START_HERE.html` pages carry `Absolute week 14` in visible text. The census
pattern is case-insensitive; the rewriter's week pattern is not. So the gate
counts a pupil-facing token the rewriter cannot see: neither resolved nor
refused. `--measure` reports these as **UNSEEN** rather than folding them into
"no change", because a bucket that says "nothing happened" is where a defect
hides. The same asymmetry hides a bare `W9B`: `\bW\d+\b` needs a word boundary
after the digit, so a lesson-letter reference standing alone is invisible to the
gate as well. **Neither is fixed here** — widening the rewriter's pattern changes
what it will write, and that wants a ruling, not a commit.
