# SCA-1 CLOSE v2 §4 — the two pre-existing reds, classified

**They are the same red.** One root cause in one workflow; the second workflow is the
reporter doing its job. Neither is caused by ECA-1, SCA-1 or this pass — both were red
on `7277859` (this estate's base before ECA-1) and on `a810d44`.

## (i) Root — FieldOps P2, the sweep, and the serve proof

- **Workflow**: `.github/workflows/fieldops-p2-and-sweep.yml` — "FieldOps P2, the sweep,
  and the serve proof". **No `paths:` filter**, so every changed path matches and it runs
  on every push to main (R0.1 limb 3 — the workflow states this in its own comments).
- **Job**: "The stale-evidence sweep can still find something"
- **Failing step**: "The sweep over all three estates, and all three must be assessed"
- **Command**: `node tools/stale_evidence_sweep.mjs --require-roots=3` → **exit 2**
- **The exact assertion that failed** (run 32249330300, head `a810d44`):

  ```
  [INCONCLUSIVE] 0 subject(s) this sweep could not resolve and 20 row(s) it could not parse.
    Teesside_Maker_Lab_PRO/qa/PROFESSIONAL_QA_RESULTS.json:6 "boot": "PASS", — this row
      states a verdict and matched none of the claim forms
    … 19 more …
  A subject the tool cannot see is not a subject that is gone. The run does not
  pass with one outstanding, because the alternative is calling it stale.
  ```

- **It is NOT the three-root requirement.** That passed — the sibling clones worked and
  all three roots were assessed:

  | repo | assessed | evidence files | claims judged |
  |---|---|---:|---:|
  | Lessons | yes | 2 | 24 |
  | mattroper1977.github.io | yes | 0 | 0 |
  | Matt-s-Apps- | yes | 3 | 0 |

  Forward sweep result: **0 stale claims · 24 live · 0 declarations without a consumer ·
  0 repos tracking output under an ignored path.** Nothing in this estate is stale.

- **What actually goes red**: 20 verdict rows in the **sibling repository
  `Matt-s-Apps-`** — 18 in `Teesside_Maker_Lab_PRO/qa/PROFESSIONAL_QA_RESULTS.json`, 2 in
  `.../STATIC_CHECK_RESULTS.json` — all of the flat JSON shape `"name": "PASS",`, which
  matches none of the sweep's claim forms. The tool deliberately refuses to call an
  unparsed verdict row green, because its own v2 reported exactly this as "0 stale" and
  read as passing.

- **Classification: a REAL DEFECT, but not in this repository's content.** It is a
  claim-grammar gap between `tools/stale_evidence_sweep.mjs` (which lives here) and
  another estate's QA file shape (which does not). It is **not** an environment failure —
  the clones succeeded and every root was assessed — and **not** a stale fixture or
  hand-list in Lessons.

- **Not fixed, deliberately**, against the ≤10-line rule's three limbs:
  1. The remedy is a semantic decision, not a mechanical patch: either the sweep gains a
     claim form for flat `"key": "PASS"` JSON (and then starts issuing staleness verdicts
     over MakerLab QA evidence), or `Matt-s-Apps-` moves those files to a sanctioned claim
     shape. Choosing between those is a cross-estate ruling.
  2. **The red-on-target → green-after proof is unobtainable in this session**: the failing
     input lives in `Matt-s-Apps-`, which this session's GitHub scope does not include, so
     I cannot reproduce the failure or demonstrate the fix.
  3. Relaxing `--require-roots` or downgrading INCONCLUSIVE would be precisely the "check
     that cannot fire dressed politely" the workflow's own comments forbid. **No workflow
     was disabled or weakened.**

- **Honest note on my local reproduction**: running the same command in this container
  also exits 2, but for a *different* reason — the two sibling repos are not cloned here,
  so it fails at `ROOTS 1 assessed, 3 required`. That is **not** the CI failure. The CI
  log is the authority and is quoted above. The sweep's own self-test passes locally
  (`--self-test` → exit 0), so the instrument can fire.

## (ii) Reporter — Watch main

- **Workflow**: `.github/workflows/watch-main.yml` — "Watch main — a red nobody is told
  about is a red nobody has"
- **Job**: "Every workflow on main has a verdict, and it is PASS" · **failing step**:
  "The measurement" (`node tools/watch_main_runs.mjs`) → **exit 1**
- **The assertion, and what it found** (run 32249444863):

  ```
  PASS   pages build and deployment                     a810d44 · run 32249328763
  PASS   Made by Matt cross-estate unification          7277859 · run 32227888314
  PASS   Reading-theme parity with the canonical engine 7277859 · run 32226310511
  FAIL   FieldOps P2, the sweep, and the serve proof    a810d44 · run 32249330300
  3 PASS · 1 FAIL · 0 NO VERDICT · 0 pending · 5 dormant · 3 dispatch-only, of 11 derived
  [RED] 1 failing · 0 without a verdict.
  ```

- **Classification: NOT a defect — correct behaviour.** It names the FieldOps run and
  links it, excludes itself (it cannot witness its own in-progress run), and correctly
  classifies 5 dormant and 3 dispatch-only workflows without letting them colour the
  verdict. Its controls pass (`--self-test`, `--verify-trigger-list`), and its write leg
  stayed a dry run as designed. **Nothing to fix.** It goes green the moment FieldOps does.

## Verdict handed forward

**One red.** Fix the sweep's claim grammar (or the sibling's QA file shape) and both
workflows go green together. Owned by the FieldOps own-session, which inherits this
classification; nothing in this pass should be read as having addressed it.
