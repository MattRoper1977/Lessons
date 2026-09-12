# PIN1 — UX2 scheduled census, bounded pass

mbm-pin-coverage-PIN1-TOP

## Authority and scope

Matt authorised the next small pass after P6. LP1's material-scope stop remains;
LP1's census has run, satisfying PIN1's "runs with or after LP1" sequencing.
This pass implements only the recovered PIN1 §2 ruling, filed at Lessons
`166455338f2c9eb4a878f9a11892ad031a516178`,
`docs/orders/LP1_PIN1_S1_CENSUS.md`:

> **PIN1 §2:** `ux2-gates.yml` has no registry, so PIN1 §2.2 applies — a scheduled census reporting drift, that gate ALONE, UNMEASURED never green, never widen to `**`.

Base: Lessons main `4f8227cef7a0191df25145d53fe2bc05f7aa2ef9`.
The original census's 444 declared paths and 440 Lessons assertions are historical
measurements, not remeasured totals in this pass. UX2 is not the digest gate.
No registry or new file-pin assertion is invented here. Gate A's missing trigger
coverage and the Apps gates are outside this narrow ruling.

## Smallest honest alternative

UX2 already runs daily at 05:23 UTC and already tests catalogue, derived data and
browser predicates. Reuse those executions. Each existing proof step exposes its
actual outcome. A final `always()` job collects all three jobs and all nine proof
outcomes into commit-bound JSON, Markdown and an Actions job summary. The same
reporter runs on the workflow's existing PR, push and manual events, so it can be
exercised before the first scheduled invocation. No paths, schedule, original
commands, predicates, job conditions, pins or size tables change.

This is a census of **UX2's existing assertions**, not pin-trigger coverage:

| Evidence | Census | Exit |
|---|---|---:|
| All nine proofs and three jobs succeeded | PASS for UX2 assertions only | 0 |
| Complete outcomes include assertion or execution failure | FAIL; original job logs diagnose the failure | 1 |
| Missing/extra dependency, missing proof/context, skipped/cancelled/unknown outcome | UNMEASURED; any known failures retained | 2 |

A job failure alone cannot distinguish data drift from an execution failure. The
report explicitly says this and names the affected proof; it does not fabricate
a list of stale pins. A green report cannot be cited as pin coverage or a live
publication proof. An incomplete census takes precedence over a known failure
while retaining both. Artifact upload runs on failure and errors if no report
exists. Checkout/runtime/upload failures also fail the job.

## Verification and limits

Five local unittest methods exercise every proof's failed, skipped, cancelled,
missing and unknown outcomes; failed/incomplete jobs; changed dependency
population; missing context; malformed JSON; failure retained alongside missing
evidence; and CLI report preservation with exit 2. All passed. These are reporter
controls, not observed GitHub events or scratch-branch trigger plants.

Parsed YAML comparison with the exact base confirms the complete `on` block is
unchanged and every existing job's `run` commands are unchanged. The added proof
IDs/outputs only expose execution evidence. `git diff --check` passes.

GitHub execution and release state are recorded in the continuation readout after
the candidate has run. A scheduled event must be observed separately: source
configuration or a PR event cannot be relabelled as an observed scheduled run.

PIN1 §3's pinned-file-only RED, corrected-pin GREEN and unrelated-file DORMANT
scratch-branch proofs are **not performed and not closed** by this non-pin gate
fallback. No assertion that the whole PIN1 order or LP1 is closed is made.

Next: inspect this candidate's actual nine-proof census; preserve a failed or
UNMEASURED result without repinning/weakening another check to make it pass.
After release, inspect the first actual scheduled census before claiming it was
observed. Keep broader pin-trigger work and LP1's scope decision separate.

PIN1_PARTIAL

mbm-pin-coverage-PIN1-BOTTOM
