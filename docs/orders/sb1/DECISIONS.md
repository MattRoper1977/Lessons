# SB1 — official Scratch 3 schema in the existing checker

mbm-sb3-gate-SB1-TOP

## Authority

Matt requested the next implementation pass after the fitness review and its
same-tool extension proposal, saved at Lessons handover commit
`216da35757e8d9423dee16d0d50f80d0a9c2bb80`. This implements that proposal;
it does not replace the parent checker or introduce a second production checker.
Base main: `a20a09b96ddb0cdbe37709631603de82cc8b1d6a`.

## Four separate properties

- Exact reviewed digest remains publication admission. An unreviewed renamed ZIP
  already fails admission; this work closes an assertion gap, not a live vulnerability.
- The extension allowlist classifies a file. It does not validate Scratch.
- New `--schema` mode invokes official `scratch-parser` 6.0.1 and explicitly requires
  projectVersion 3. Scratch 2 acceptance by the general parser is insufficient.
- Existing parent-link functions and their 14 controls remain unchanged and callable
  separately. Schema mode never repairs behaviour or rejects intentionally faulty
  lesson logic. It does not impose this first unit's no-variable graph assumption
  on a future unit. The CI graph plant tests the preserved instrument on a genuine
  project selected from the schema report, not a hard-coded filename.

## Population and trigger derivation

The schema census unions all tracked case-insensitive `.sb3` paths with this
repository's `.sb3` admission rows. Validating all tracked files is a deliberate
conservative superset of the publisher's admitted files; it also catches new units
before a registry row exists. It does not claim every source-only file is published.
Currently both populations contain the same **23 full relative paths**, zero source-
only files, zero absent ARRIVING rows. Each has passed the official schema locally.

The registry comes from the immutable builder ref derived from both `uses` and
`builder_ref` in this commit's education-pages.yml. The checker verifies the builder
checkout SHA and exact committed registry bytes before citing that ref. It reports
source SHA, registry SHA256, parser version, population, per-file outcome and time.
Missing tracked or required admitted input is UNMEASURED; absent untracked ARRIVING
rows are explicitly reported; an empty measured population is never green.
This mode does not compare project digest pins: schema plants must fail as schema
or container errors, independently of the existing digest admission gate.

A separate SB1 job is added to existing `ux2-gates.yml`, already registered with
Watch. PR and push filters gain four suffix-specific patterns covering `.sb3`,
`.SB3`, `.Sb3` and `.sB3`, plus the existing checker, its two dependency files and
publisher caller. Newly added filenames are covered without editing a path list.
No bare `**`, new workflow, Watch-list edit, digest ratchet or cross-repo mirror is
needed. The existing schedule/manual events also run the job. This is a measured
adjustment to the proposal's new-workflow option: one Lessons PR remains sufficient.

All existing UX2 jobs, including PIN1's three-job/nine-proof census, are unchanged.
SB1 reports under its own job and artifact; it is not silently counted as PIN1's
original tenth proof. The dependency lock has 21 packages, exact integrity values
and only registry.npmjs.org download URLs. CI uses npm ci with install scripts off.

## Failure semantics

| State | Result |
|---|---|
| Every requested input accepted as Scratch 3 | PASS, exit 0 |
| Invalid archive/JSON/schema or Scratch 2 | FAIL, exit 1; official parser diagnosis |
| Missing Node/module/input, wrong parser version, timeout, malformed response, missing population or registry mismatch | UNMEASURED, exit 2 |

Dependency-install failure emits UNMEASURED and fails the job. Artifacts upload even
on schema failure and missing artifacts fail visibly. The job uses pipefail so a
failed control cannot be hidden by tee. The schema job must also pass its real
negative controls before it can complete successfully.

## Local proof readback

- Genuine Scratch 3 project: PASS. All 23 measured real projects: PASS.
- Genuine container copied without project.json: official parser rejects missing
  project/sprite JSON, independent of admission.
- Genuine container with corrupt project.json: official parser rejects JSON syntax.
- Well-formed `{}` project.json: schema rejection; the old parent checker accepted it.
- Scratch 2 project.json: rejected explicitly as version 2.
- Missing parser, missing Node, missing input and empty list: UNMEASURED, exit 2.
- New unregistered uppercase SB3 enters the census; deleting a tracked file cannot
  silently remove it from the denominator. **11/11 schema/population controls PASS.**
- Original graph self-tests: **14/14 PASS**. Its null-parent plant remains required
  in CI; the prior fitness pass already observed it firing on a genuine project.
- Existing publication controls executed before and after this implementation:
  **61/61 PASS both times**, identical outcomes and diagnoses apart from the
  expected temporary-directory names in three symlink-control messages. Disguised SB3: real PASS,
  planted FAIL, restored PASS in all three education trees; reason UNREVIEWED.
- AST comparison: every original graph function unchanged (only main gains flags).
  Parsed YAML comparison: every existing UX2 job unchanged. Watch derivation check
  still PASS, 21 workflows. git diff --check passes.

Actions results, exact candidate/merge refs and final status belong in the closing
readout. Local controls are not GitHub file-only trigger experiments. PIN1's original
RED/GREEN/DORMANT branch proofs remain separate and open. LP1's hold remains.
No second Scratch unit is admitted by this PR.

SB1_PARTIAL — implementation prepared; CI execution and release must be recorded.

mbm-sb3-gate-SB1-BOTTOM
