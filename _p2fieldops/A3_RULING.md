# A3 / §2.8 — the stale-evidence sweep red, ruled at source

## What the red actually is (measured this session, not inherited)

`node tools/stale_evidence_sweep.mjs --require-roots=3` → **exit 2**, closing
`[INCONCLUSIVE] 0 subject(s) this sweep could not resolve and 20 row(s) it could not parse.`
Reproduced locally with all three roots resolvable, and confirmed red in CI at
`a2f0b5b` (run 32279705417, job "The stale-evidence sweep can still find something",
failing step "The sweep over all three estates, and all three must be assessed").

The 20 rows, by my own count (R0.2):

| file | rows |
|---|---|
| `Teesside_Maker_Lab_PRO/qa/PROFESSIONAL_QA_RESULTS.json` | 18 |
| `Teesside_Maker_Lab_PRO/qa/STATIC_CHECK_RESULTS.json` | 2 |

## "The one outstanding" — named, as A3 requires

It is **not a separate item**. `pass with one outstanding` is a fixed closing
sentence printed by `stale_evidence_sweep.mjs:561` whenever
`unresolved.length || noform.length` is non-zero — a statement of the tool's
policy, not a pointer to a particular row. The outstanding set here is exactly
the 20 unparsed rows; `unresolved` is **0**. Nothing else is outstanding, so
nothing else is left behind by closing them.

## Which side is stale — decided by reading

**Neither. The rows are live and the grammar is short.**

- The 20 rows are QA verdicts about the Maker Lab PRO release, in three JSON
  documents naming **41 file subjects between them — of which 0 are missing**
  (checked against `Teesside_Maker_Lab_PRO/`). They are current: HEAD of Apps is
  `6a8ae06` "Merge Maker Lab live acceptance test on the published origin".
- The sweep's file filter **already selects `.json`** under `evidence/` and `qa/`
  (`forward()`: `/\.(out|json|txt|md|log)$/`). It intends to judge these files.
  Its claim grammar, however, is entirely line-oriented text: `REPORT_ROW`
  requires a line to *begin* with a bare `[A-Z]…` label, so `  "boot": "PASS",`
  cannot match, falls to `ASSERTING_ROW`, and is booked `no-form-matched`.
- The natural experiment that proves it is structural rather than staleness:
  `MOBILE_QA_RESULTS.json` holds **12 records of the identical shape** and
  produces **0** unparsed rows — only because its records carry `"ok": true`
  booleans instead of verdict *words*. Same data, same directory, same validity;
  visible or invisible purely by whether a line happens to contain "PASS".

## Ruling: (c) — widen the grammar, minimally, with the new form named

- **(b) remove — rejected.** They are live verdicts with a reader; deleting them
  would destroy the QA record of a release merged three commits ago.
- **(a) repair the data — rejected.** It would mean writing text rows into
  machine-generated JSON: either corrupting a valid schema or bolting a text twin
  onto a tool's output. A3 requires provenance preserved, and the provenance here
  is "this file is what the QA runner emitted".
- **(c) widen — taken.** The condition A3 sets is met exactly: a legitimate
  verdict form the estate uses elsewhere (three files, two repositories' worth of
  convention) that the grammar cannot see.

**This strengthens the sweep; it does not loosen it.** Before: 20 rows unparsed,
**0 claims judged** in Apps. After: the JSON records are parsed structurally and
their named subjects resolved, so a QA record naming a file that has since been
deleted now comes back **STALE** — detection the sweep did not previously have.
The `no-form-matched` control is untouched and still fires for every other shape.

New form named: **`qa-record`** — a JSON QA document whose records name a `file`
subject, resolved by a new `qa-subject` resolver against the project directory
that owns the `qa/` folder (never bare repo root: resolving `index.html` against
the root would return **STALE — SUBJECT ABSENT** for a file that plainly exists,
which is the "worst possible verdict" this tool's own comments warn about).
Document-level verdicts with no named subject (`"overall": "PASS"`) are booked
`NOT A CLAIM` with a stated reason — the same treatment the tool already gives
report-row labels, never silence.
