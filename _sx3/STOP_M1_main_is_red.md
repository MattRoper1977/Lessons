# STOP-M1 — main is red, and the cause is this release's own CI work

## Verdict

`main` has been red since **cb1eb052 (#584)**. It is red now at **3e2dcbd2 (#585)**.
Attribution: mine. #584 added a workflow and did not register it with the watch.

## The failing check

Workflow: `Watch main — a red nobody is told about is a red nobody has`
(`.github/workflows/watch-main.yml`), job *"Every workflow on main has a verdict,
and it is PASS"*, step `node tools/watch_main_runs.mjs --verify-trigger-list`.

Failing runs at the current head `3e2dcbd2`:

| run | conclusion |
|---|---|
| [35361593690](https://github.com/MattRoper1977/Lessons/actions/runs/35361593690) | failure |
| [35361671166](https://github.com/MattRoper1977/Lessons/actions/runs/35361671166) | failure |
| [35361843496](https://github.com/MattRoper1977/Lessons/actions/runs/35361843496) | failure |

The one failing line:

```
[FAIL] derived but NOT listed — this workflow's completion would never wake the
       watch: Cross-estate contract on lesson content
```

## When it went red

`tools/watch_main_runs.mjs --verify-trigger-list` run in a clean worktree at each
of the last three main commits:

| commit | caller file present | control |
|---|---|---|
| `d872ef99` — LV2–LV6 record (#575) | no | green |
| `cb1eb052` — Fire the cross-estate contract on lesson-content PRs (**#584**) | yes | **FAIL** |
| `3e2dcbd2` — Grant the caller the permissions its callee declares (#585) | yes | **FAIL** |

(An earlier reading of mine showed d872ef99 failing too. That was a bad
instrument: `git checkout <sha> -- .github` does not delete a file absent from
that tree, so the caller file stayed in the working tree. The worktree
measurement above replaces it.)

#585 neither caused this nor fixed it.

## Why it is right that this is red

`workflow_run` has no wildcard, so `watch-main.yml` names the workflows whose
completion wakes the watch. The file's own header says a hand-maintained list is
the defect this estate has already been bitten by, and that `--verify-trigger-list`
exists to go red the moment a workflow is added and not listed. It did exactly
that. The control is not broken; the list is short by one.

## The fix, verified but NOT pushed

One line in `.github/workflows/watch-main.yml`, inside the contiguous block (a
comment inside the list would truncate it — the file says so):

```yaml
      - "Served digest census"
+     - "Cross-estate contract on lesson content"
```

Measured in a clean worktree at `3e2dcbd2` with that one line added:

```
PASS  the trigger list is exactly the derived set (23 workflow(s)).
```

`.github/workflows/watch-main.yml` is digest-pinned in `CATALOGUE_PINS`, so the
change also moves one pin, re-stamped into both gate copies by
`pin_catalogue_contract.py` — the same procedure used for the quote limb.

## Why I stopped instead of pushing it

Two standing rules collide and I will not resolve them myself:

1. **"Any red on main halts everything: report with attribution, do not proceed."**
   So: reported, attributed, halted. Nothing merges while this stands — including
   Lessons #586 and Matt-s-Apps- #109, both of which are otherwise ready.
2. **ORDER SX3-FINISH §1: "§1 below is the last CI edit."** and
   **ORDER SX3-FINISH2: "No CI edits remain."** The fix above is a CI edit, and
   the budget for those is spent.

**Requested ruling:** authorise the one line above as a CI edit outside the spent
budget, on the ground that it repairs a red this release caused. On that word it
goes up as its own PR in both estates, with the run id quoted once observed
green on main.
