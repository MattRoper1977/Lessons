## D5 — Deferred: the zero-check gate should exclude conflicted PRs

**No code now. Own PR, later, never inside an order.**

`tools/pr_check_census.mjs` reds when any non-draft open PR across the three
repositories has zero check runs and is not declared in
`tools/zero_check_baseline.json`. The intent is sound: a green tick on a PR
nothing ran is a false green.

But a PR whose `mergeable_state` is `dirty` **cannot be merged at all**, so it
carries no false-green risk — GitHub can build no merge ref, so no workflow can
fire however the filters are written. The gate's own output says exactly this:
`conflicted — no merge ref, so no workflow could fire`. The result is that one
conflicted PR anywhere in the estate reds **every** PR in the estate, including
unrelated ones in other repositories.

Observed 2026-09-09: three conflicted PRs (Lessons #456, Apps #73, Site #339)
red-flagged Lessons #457, which had 13 green checks and no relationship to any
of them.

Proposed rule: exclude `mergeable_state == 'dirty'` from the undeclared count and
report it as a separate conflicted census, keeping it visible without letting it
gate. `draft` is already excluded on the same reasoning — draftness is read, not
inferred — and conflictedness is the stronger signal of the two.

Do **not** work around this by adding transient conflicts to
`zero_check_baseline.json`. That file's own `_how_it_fails` calls an unpruned
entry stale evidence, and a conflict that clears on rebase would leave a row
nobody prunes.

---
