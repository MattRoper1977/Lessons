# SB1 — closing readout

mbm-sb3-gate-SB1-TOP

## Current checkpoint — SB1_CLOSED, schema gate merged and proved on main

Measured 2026-09-12T14:00:32.452Z. Lessons #516 is merged at `12828ac35af20b1058b9f5f1c0774f30d34df0b1`.
The existing checker now has an official Scratch 3 schema mode and a separate job
in UX2. The final PR proof and the post-merge SB1 job both PASS: 23/23 projects,
11/11 schema/population controls and 14/14 original parent fixture controls.
Main proof: run `34697885634`, job `103564413035`, reporting that exact main SHA.
All 61 admission controls pass before and after; disguised SB3 stays refused in
all three trees. No digest, publisher pin, pupil project or original graph function
was changed. All existing UX2 jobs and PIN1's nine-proof census remain unchanged.

Final head `9b6f4d44a46a709e87216ae5dc0b7d8b228651f3`; PR tested merge
`b94e19a260cf46666ec54bc4a2f69cd1bbd7c077`. Reviewed/tested/merged tree:
`a59a2c4b17eb56ae1c594e7fc4d01c6bc60cf33c`. All 13 PR checks terminal:
12 SUCCESS, 1 independently matched baseline sweep FAIL (1,418 stale / 6,307 live /
6,899 row labels / 47 unmatched). No checks suppressed. Initial `acd67215` was
superseded before the final proof to remove an unnecessary real-project graph
assertion; the gate remains schema-only for valid blank and variable projects.

This closes SB1's implemented gate and its requested proofs. Broader post-merge
publication `34697885918`, FieldOps `34697885618` and the remaining UX2 browser/census
jobs were still running at their last inspected snapshot; do not infer their
completion from SB1's job success. The next continuation begins by reading those
exact runs. No background poller is left active. No second Scratch unit was added.
PIN1's original trigger plants and LP1's material-scope hold remain open; the first
scheduled invocation of the new PIN1 census remains unobserved in this session.
See `SB1_RELEASE_READOUT.md` for exact proof results, artifact references and limits.
Earlier SB1_BLOCKED fitness and prepared-SB1_PARTIAL statements are historical,
superseded by this authorised implementation and proof.


## Gate and scope

Matt asked to continue after the recorded same-tool extension proposal. Five files
changed in one Lessons PR: the existing checker, its package/lock files, the UX2
workflow and `docs/orders/sb1/DECISIONS.md`. No competing #497 files were edited.

The official parser is scratch-parser 6.0.1, installed by npm ci from an integrity-
locked 21-package graph, install scripts disabled. The schema result must explicitly
be Scratch 3; the parser's ability to accept Scratch 2 is not credited as success.
The source population is every tracked case-insensitive .sb3 plus Lessons admission
rows from the unchanged caller-pinned builder registry. Current sets coincide:
23 tracked, 23 registered/present, zero source-only, zero absent ARRIVING.
This deliberately also checks new source files before their digest is admitted;
it does not claim that every source-only file is published.

The caller's two immutable refs must agree. Builder checkout SHA and committed
registry bytes must match before they are cited. Publisher remains
`d87ad04ff36313a37584dab4feb243e984f0c5fa`. Source SHA, registry digest, parser version,
full relative paths, denominator and measurement time are in both saved CI reports.
The checker does not edit a pupil project or assert behavioural correctness.

## Trigger derivation

Existing UX2 PR/push filters gain suffix-only patterns for .sb3/.SB3/.Sb3/.sB3,
plus the existing checker, package/lock and publisher caller. These cover new names
without maintaining the first unit's 23-path list. There is no unqualified `**`.
The same already-registered workflow also retains its schedule/manual events.
Every original UX2 job is unchanged; SB1 is separate from the PIN1 nine-proof census.
Watch's source derivation still passes for all 21 workflows, so no unrelated pinned
Watch or cross-repository mirror changes were necessary.

## Required proofs and controls

| Proof | Observed result |
|---|---|
| Genuine projects | 23/23 official Scratch 3 PASS, on final PR and actual main |
| Genuine ZIP copied without project.json | Official parser FAIL: missing project/sprite JSON; not a digest failure |
| Otherwise preserved container with corrupted project.json | Official parser FAIL: JSON syntax |
| Valid JSON `{}` (old checker accepted it) | Official schema FAIL: missing required meta |
| Scratch 2 | FAIL: expected Scratch 3, got 2 |
| No inputs / missing input / missing module / missing Node | UNMEASURED, exit 2 |
| Newly tracked unregistered uppercase filename | Included in population |
| Tracked file removed from working tree | Cannot silently disappear from denominator |
| Existing graph fixture suite | 14/14 PASS, original functions unchanged |
| Independent local null-parent mutation | Original 0 errors, planted 1; FIRES |
| Existing admission, before and after | 61/61 PASS each; all three disguised-SB3 plants FAIL and restore PASS |

The 11 schema/population controls run in the actual CI job. Their archive mutations
are asserted to have landed before invoking the parser. The current invalid-fixture
checks are independent of digest admission. The source graph functions remain
separate: a valid blank or variables project must not fail a schema gate because
of the first unit's stronger graph assumptions. Initial candidate `acd67215` had
that unnecessary extra CI graph plant; final `9b6f4d44` removes it while preserving
all 14 fixture controls. Superseded Actions runs are not the final proof.

Admission controls ran twice against the preserved actual P6 assembled tree.
All checker/module/registry bytes match the actual publisher pin. The only raw-log
differences are random temporary-directory names in three symlink diagnostics;
all statuses and normalised diagnoses match. Neither before nor after is merely
a copied prior count. No full publisher rebuild is claimed by those control runs.

## Exact Actions evidence

- PR https://github.com/MattRoper1977/Lessons/pull/516
- Final PR run `34697413719`, SB1 job `103563270694`, SUCCESS.
- PR artifact `10299227466`, 2,287 bytes, unexpired when inspected; contains schema
  report and controls. Upload/API metadata and job content inspected; ZIP not downloaded.
- Actual main run `34697885634`, SB1 job `103564413035`, SUCCESS; main log records
  23 projects, 11 schema/population controls and 14 graph fixture controls.
- Final PR baseline sweep job `103563206495`, exit 2, exactly matches the prior main
  baseline. All other 12 final PR checks SUCCESS; none pending at merge.
- Rollback base: `a20a09b96ddb0cdbe37709631603de82cc8b1d6a`.

Evidence files under `rf3-evidence/`: SB1_CI_PROOF.json, SB1_MAIN_PROOF.json,
SB1_ADMISSION_BEFORE.json, SB1_ADMISSION_AFTER.json, SB1_ADMISSION_BINDING.json,
SB1_PARENT_RED_LOCAL.txt and SB1_RELEASE_STATE.json. Decisions on main:
https://github.com/MattRoper1977/Lessons/blob/12828ac35af20b1058b9f5f1c0774f30d34df0b1/docs/orders/sb1/DECISIONS.md

## Limits and next boundary

SB1_CLOSED means the schema gate is wired, merged and proved in real CI, including
on its actual main commit. It is not a new publication-success claim, a proof of
pupil completion or admission of a second unit. Local/parser controls are not
PIN1's separate file-only RED/GREEN/DORMANT GitHub trigger experiments. The broad
estate programme is not closed.

Read the outstanding post-merge runs first on continuation. Keep LP1's scope stop,
PIN1's remaining branch proofs, the other recorded holds and the named-second-unit
requirement intact. No further order was started during this bounded pass.

SB1_CLOSED

mbm-sb3-gate-SB1-BOTTOM
