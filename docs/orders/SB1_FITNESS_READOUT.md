# SB1 — existing-tool fitness pass

mbm-sb3-gate-SB1-TOP

## Result and stop

The next bounded pass after PIN1 #515 is complete as a fitness review.
**SB1 implementation is BLOCKED by §3.1**: "Wire the existing tool; do not write a
second one. If check_sb3_parents.py is unfit, say why and propose rather than replace."
This pass establishes that it is unfit as a schema gate. It remains useful as a
separate block-parent assertion. No production tool or workflow was changed and
no replacement checker or implementation PR was created.

Measured against Lessons main `a20a09b96ddb0cdbe37709631603de82cc8b1d6a`.
The existing `tools/gc1/check_sb3_parents.py` has SHA256
`43ded2eb09e27895b9ea7f3e20ba0eb33a8a86a14902ae596a3b68b339f52961`.
Its bytes match the exact main revision. Full measured results and timestamp:
`rf3-evidence/SB1_FITNESS.json`.

## What the existing tool actually asserts

It opens each ZIP, decodes project.json, then checks each target's block links:
referenced children must exist in that target and name their referring block as
parent. Per-target identity matters because different sprites reuse block IDs.
It does not invoke the official parser or validate the Scratch schema. Its own
self-test deliberately treats a missing `targets` key as clean. Its directory CLI
also returns exit 0 after checking zero `.sb3` files.

The graph assertion is not a general substitute for Scratch validation: its own
comment limits interpretation of input references to this unit's measured lack of
variables and lists. Do not silently apply that assumption to a second unit.

Current source census: **23 tracked .sb3 files, 23 parent-check passes, 0 errors**.
Parent controls: **14/14 passed**. A null-parent plant derived from a genuine
project changed Courier's referenced child; original 0 problems, planted 1,
control FIRES. All plants were confined to temporary copies and discarded.

## Local comparison with the official parser

Installed official `scratch-parser` **6.0.1**, provenance from its package metadata
(`scratchfoundation/scratch-parser`, MIT Media Lab), was called through its documented
buffer/callback API. These are local diagnostic executions, not CI gate proofs.

| Input | Existing parent checker | Official parser | What this establishes |
|---|---|---|---|
| W01_Start.sb3 | PASS | PASS, projectVersion 3 | One genuine Scratch 3 project parses |
| Renamed ZIP with README.txt, no project.json | UNREADABLE | Rejects: missing project or sprite JSON | Container rejection, independent of digest admission |
| ZIP with syntactically corrupt project.json | UNREADABLE | JSON syntax rejection | Malformed JSON is rejected |
| ZIP whose project.json is `{}` | **PASS** | Schema rejection; SB3 missing required `meta` | Existing tool cannot assert schema validity |
| Empty directory | **exit 0, zero checked** | Not invoked | Missing population can currently appear green |

The `{}` plant is additional to SB1's two negative examples: both negative examples
alone would let the unsuitable parent checker appear sufficient. The official
parser also supports older project versions, so merely accepting its output is
insufficient; a future gate must require `projectVersion === 3` explicitly.
Only the genuine fixture above was schema-parsed in this pass; do not turn the
23 parent-link passes into 23 new schema validations.

## Admission protection and control count

Exact reviewed digest is still the acceptance rule. The extension allowlist only
makes `.sb3` classifiable; it does not certify Scratch schema. This is a gap in
assertions, not evidence of a live vulnerability.

The preserved P6 assembled-tree evidence reports **61 controls PASS**, including
real-PASS / disguised-sb3-FAIL / restored-PASS in all three education trees, each
rejected as UNREVIEWED. This was READ from the prior execution; it was not rerun
or relabelled as a new SB1 result. No admission code, registry or publisher pin was
changed. **Post-implementation control count: NOT MEASURED**, because implementation
stopped here. §2.4 still needs before/after executions when the gate is implemented.

## Concrete proposal for the implementation pass

Extend the **same existing Python entry point**; preserve its parent-link functions,
14 controls and planted-link proof. Add an explicit official-schema mode that calls
the pinned official parser through a small Node invocation inside that entry point,
then requires Scratch 3. Do not create a second production checker or replace the
parent-link predicate with a schema test.

1. Bind parser dependencies with a reviewed lockfile and install them in CI. Missing
   Node/module, timeout or unusable parser output must report UNMEASURED and exit 2.
   Invalid containers, JSON, schema or non-Scratch-3 versions must exit 1 with the
   relevant parser diagnosis. Running locally does not prove parser availability in CI.
2. Enumerate the admitted `.sb3` population from the publisher's actual admitted
   paths, retain full relative paths, and publish its denominator. Missing input or
   an unexpectedly empty set must not become green. Do not freeze the gate to the
   first unit's 23 paths or assume every arbitrary source `.sb3` is published.
3. Trigger PRs on the extension-specific `**/*.sb3` pattern, plus the existing checker,
   dependency lockfile and gate workflow. This catches newly added units and is not
   the forbidden unqualified `**`. Confirm additions/edits/deletions and the derived
   admitted population in the implementation PR; no trigger change is made here.
4. Prove the genuine, missing-project.json, corrupt-JSON, invalid-schema, unavailable-
   parser and empty-population cases in CI. Re-run the existing disguised-code controls
   before and after. Keep parser schema and parent-graph results separately named.
5. One implementation PR with DECISIONS distinguishing digest admission, extension
   classification, schema and graph checks. Keep the second Scratch unit held until
   this gate is wired and its actual PR execution is proved.

This is a recorded proposal under §3.1, not an implemented gate or an assertion that
§4's CI/parser/trigger stop conditions have been tested and cleared. LP1's material-
scope hold and PIN1's outstanding trigger proofs remain separate and unchanged.

PR number: none (fitness stop before implementation).

SB1_BLOCKED

mbm-sb3-gate-SB1-BOTTOM
