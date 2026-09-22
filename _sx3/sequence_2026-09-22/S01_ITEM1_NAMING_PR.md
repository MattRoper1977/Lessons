# S01 — Item 1 closed: the naming PR landed, row-45 expectation regenerated (2026-09-22)

Sequence ledger, entry 1. Written by session `01Grmg9b`, which executed the 2026-09-22 handoff
and the autonomy order that followed it.

This is a new file rather than an append to `_sx3/SX3_PASSES_LEDGER.md`. That file is
digest-pinned in both gate copies, so appending would force an Apps re-pin for a docs change.
The gate diffs with `--diff-filter=MRD`, which means an added file cannot trip the
standalone/offline boundary.

Every figure below was re-derived in this session from git, the GitHub API or the repo's own
tools. The draft was then checked by two independent adversarial verifiers. They upheld 38 of 41
claims; the three they refuted and eleven omissions are corrected in this text.

## Mains after the item

| repo | main | how |
|---|---|---|
| Apps | `359692f352978c1581764c097c7a9946229c0a95` | squash of #171, the gate-copy companion, merged 18:01:07Z. Merged FIRST (correction #18 / L31) |
| Lessons | `7fb0fbd18454f200b9d61f877dcbf4a193317cff` | squash of #651, the handoff addendum. Merged 18:08:34Z (`merged_at`) by the previous session. Docs only, 1 file |
| Lessons | `5e9604cc73faac256bf94a63a2760c1f858414f5` | squash of #649, the naming PR, merged 18:15:18Z |
| Site | `acb7bfa9bb525ecd3dbffee2c68c208719d2888e` | unchanged |

G1: both gate copies are byte-identical at **`c1da1041463a`** (blob `ad9d3681`). This supersedes
`ba4dc229bede`, which was correct at the handover. The #171/#649 pair moved it as planned:
`CATALOGUE_PINS.files` 1044 → 1045, adding `tools/sx3/split_arrival_stage.py`.

## Task 1 — the publication #650 triggered

| gate on `9e1835df` | run | conclusion |
|---|---|---|
| **Education Pages publication** | **35762685587** | build `106864395347` SUCCESS · deploy `106866919445` SUCCESS |
| FieldOps P2 | 35762684885 | SUCCESS |
| Watch main | 35763550002, 35763668434, 35763983011 | SUCCESS ×3 |
| Science teaching pack downloads | 35763550148 | SUCCESS |

`education-pages.yml` has **no `paths:` filter**. Its trigger is `push: branches: [main]` plus
`workflow_dispatch`, so every merge publishes, docs-only merges included.

**Served bytes, measured source-side.** The publisher's own commands (`build_publications.py`
then `build_education.py`) were run twice. Both runs used the pins the run itself used: Site
`acb7bfa9` and Apps `86933c99`. Lessons was at `91ed7980` for one and `9e1835df` for the other.

- `education-lessons`: **5739 files, 0 added, 0 removed, 0 changed**. The tree digest is
  `39eb2088b5385a77…` in both builds.
- `education-apps` (107 files) and `education-site` (203 files) are also identical.
- The publisher ships nothing under `_sx3/` at all: there are 0 such paths in every build. The 17
  added files are therefore unpublished by construction, not by any exception.

**LIMIT.** Neither the served host nor the artifact store was measured. The egress proxy refused
`mattroper1977.github.io:443` and `productionresultssa15.blob.core.windows.net:443` with `403` on
CONNECT. Because of that:
- no live byte was read;
- no artifact zip was compared.

For context only, the artifact sizes by publication:

| artifact | `91ed7980` | `9e1835df` | `7fb0fbd1` | `5e9604cc` |
|---|---|---|---|---|
| `education-lessons-review` (plain zip) | 910526624 | 910526624 | 910526624 | 910526624 |
| `github-pages` (tar in zip, the one that deploys) | 908931792 | 908932078 | 908932164 | 908932539 |

The `github-pages` variation is consistent with tar header mtimes changing compression, but that
is an explanation, not a measurement. Neither size is proof of byte equality.

## Task 2 — merge order

1. **Apps #171 merged on green.**
   - Checks at `c80a072f`: 9, all complete by 17:25:39Z, with 5 SUCCESS + 4 skipped.
   - Result: `359692f3`.
   - Push runs:
     - cross-estate 35764421673 SUCCESS
     - LundyLoop 35764421834 SUCCESS
     - **Apps publication 35764423173** SUCCESS (build `106870212636`, deploy `106871871824`)
   - The Apps publication was rebuilt source-side at `2e630325` and at `359692f3`, with Site
     `08d74766` and Lessons `aaba36d8`: `education-apps` 107 files, 0 changed.
2. **Base merge of main `9e1835df` into `claude/sci-stage-identity`.** No rebase and no force.
   - `bd4aa84c..0e6aa994` is a fast-forward: ahead 2, behind 0. The branch timeline has no
     force-push event.
   - It brings in exactly the 17 added handoff files.
   - The PR's diff (6 files, +550/−13) is byte-identical before and after the merge.
   - Checked locally at `0e6aa994` before the push:
     - PIN1 PASS 1052/1059
     - static contract PASS, positive control PASS (3)
     - `git diff --check` clean
     - `pin_catalogue_contract --check` PASS: 1045 reviewed, 734 original rows, gate `c1da1041463a`
     - `split_arrival_stage --self-test` 29 PASS
     - `verify_loop --self-test` 41 PASS + 1 SKIP. **LIMIT:** the SKIP is the whole fixture-driven
       block ("no untransplanted copy of the fixture is available"), so those rows were not
       exercised. The AUT1 control also needs git object `aed400da`. On a shallow clone it FAILs
       ("git could not produce the object"); it passed only after `git fetch --unshallow`.
3. **#649 checks on `0e6aa994`:** 17 checks, **15 SUCCESS + 2 skipped**, 0 failure. The skipped
   pair is `announce-live-run` and `live-proof`, both skipped by design on `pull_request`. Runs
   35764758573, 35764758612 and 35764758620. The last check completed at 18:14:20Z.
4. **#649 merged** as `5e9604cc` at 18:15:18Z.

**On the pre-merge head `bd4aa84c`, `browser-matrix` had FAILED** after the handoff was written.
- Where: run 35760437854, job 106856851825, step 8, *Verify the published Education menu and
  unchanged standalone pages*. That step runs against `https://madebymatt.uk/Lessons/`.
- The log says: `[FAIL] … LAUNCH_HUM_W1_Source_Investigation.html: non-success first-party
  responses [{"url":"https://madebymatt.uk/Lessons/Launch/Slideshows/LAUNCH_HUM_W1_Source_Investigation.html","status":503}]`.
- In the same job, step 6 served that deck from the local mount and recorded
  `[PASS] lessons browser matrix: 8 widths, 4 unchanged standalone samples`.
- Source: the log was read through the GitHub MCP job-log tool in this session and saved. The
  run's artifact `10710003453` (4858432 B) corroborates it. The log cannot be re-read from this
  container through `api.github.com`, because it redirects to blob storage, which is denied.
- It is classed as a live-origin transient, and that is an inference. It is supported by the same
  step passing on `0e6aa994` (job 106871346982). No re-run was spent: the base merge made a new
  head.

## Post-merge

A push-triggered run carries its commit. A `workflow_run`-triggered run reports the default
branch's HEAD at trigger time, **not** the commit it is judging. The rows below say which is which.

| gate | run | ran on / triggered by | conclusion |
|---|---|---|---|
| Education Pages publication (#651) | 35765236498 | push `7fb0fbd1` | build `106872981352` · deploy `106876940362` SUCCESS |
| FieldOps P2 (#651) | 35765235588 | push `7fb0fbd1` | **CANCELLED** 18:16:34Z by its concurrency group when `5e9604cc` landed. #651's tree never had a FieldOps run of its own; `5e9604cc`'s supersedes it |
| **Education Pages publication (#649)** | **35765958435** | push `5e9604cc` | build `106875416035` (18:21:30–18:32:45Z) · deploy `106881852697` (18:32:48–18:33:30Z) SUCCESS |
| Made by Matt cross-estate unification | 35765957571 | push `5e9604cc` | SUCCESS |
| UX2 gates | 35765957663 | push `5e9604cc` | SUCCESS |
| FieldOps P2, the sweep, and the serve proof | 35765957767 | push `5e9604cc` | SUCCESS |
| Science teaching pack downloads | 35766614365 | workflow_run ← #651's publication | SUCCESS. Checked the live hub 18:22:51–18:23:41Z, i.e. #651's deployment, not #649's |
| **Science teaching pack downloads** | **35767957843** | workflow_run ← #649's publication | attempt 1 **FAILURE** (job `106882154622`) → re-run → attempt 2 **SUCCESS** (job `106883094468`) |
| Watch main | 35766092570, 35766481480, 35766614367, 35766871865, 35767830814, 35767957879, 35768004021 | workflow_run | SUCCESS ×7 |
| Watch main | 35768113533 | workflow_run ← the packs failure | **FAILURE**: `[RED] 1 failing · 0 without a verdict` |
| Watch main | 35768466108 | workflow_run ← the re-run | SUCCESS. Main green again, 18:38:59Z |

**The one red on main, and why it was re-run rather than stopped on.** Run 35767957843 is the
post-publication check.
- Against the source, `check_packs.py` reported `"status": "PASS"`: 35 PowerPoints, 62 archives,
  258 native downloads.
- Against the live origin, `check_hub_browser.cjs` then failed on one request:

  ```
  AssertionError [ERR_ASSERTION]: Download response:
    BUILD/lessons/W6B/BUILD_Science_Autumn1_W6B_Model_Plate_Comparison_Pupil.docx
  503 !== 200
  ```

This is the second single-request 503 from `madebymatt.uk` today. The file's bytes did not move:
the source-side rebuild at `5e9604cc` shows 0 changed paths.

**This session** spent the pre-granted re-run: `rerun_failed_jobs` on the same head, no push.
GitHub records the re-run under the repository owner's identity (18:36:00Z); the previous
session did not do it. A second failure would have been treated as real (STOP-R). The re-run
passed.

**Served bytes for #651 + #649, measured source-side.** A full local build at `5e9604cc` was
compared with the `9e1835df` build: 5739 files, **0 added, 0 removed, 0 changed**, and the digest
is unchanged. The live host was not measured: LIMIT, as above.

## Correction #39 — the base I read was not the base I merged onto

The previous session merged **#651** at 18:08:34Z, between my base merge and the #649 merge.
When I checked mergeability I took `base.sha = 9e1835df` from the PR object, which caches it and
still reads `9e1835df` now, instead of reading `main`. As a result #649 was squashed onto
`7fb0fbd1`, not onto the `9e1835df` its CI had run against.

Measured afterwards:
- #649's diff as merged (`7fb0fbd1..5e9604cc`) is **byte-identical** to its diff as tested
  (`9e1835df..0e6aa994`).
- The merged tree differs from the tested tree by exactly #651's own diff: 1 file, +54, under
  `_sx3/handoff_2026-09-22/`.
- The push-triggered gates on `5e9604cc` then ran on the exact merged tree: the publication,
  cross-estate, UX2 and FieldOps.

**Rule:** before a merge, read `main` itself (`git ls-remote` or the branches API), never
`pull.base.sha`. A second session was writing to main. It went idle at 18:08:46Z ("Stopping
here."), but two writers on this estate is a hazard every handoff should name.

## Re-measure — the landing gate, per the §9 addendum

`build_all`'s own per-deck path was run over the 91-deck strand record: `fix_template` →
`adapt` → `verify`, counting `AlreadyAdapted` as skipped.

```
b5b87361 (base)  population=91 buildable=11 skipped(already adapted)=80 HELD=0 fail rows []
5e9604cc (main)  population=91 buildable=11 skipped(already adapted)=80 HELD=0 fail rows []
```

**LIMIT — what this gate cannot see.** It verifies only the 11 buildable decks. The 80
already-transplanted decks raise `AlreadyAdapted` and never reach `verify()`. That is why the 24
shipped Humanities decks with a pupil-response panel on the title slide (owed item 4) stay
invisible to it. When verification ran `verify()` directly over the shipped bytes, rows 14 and 47
both FAIL on those same 24 decks at `5e9604cc`. Row 47 is new in #649; row 14 FAILs identically
at `b5b87361`.

## Re-measure — one stage of the 290 is misnamed (found by adversarial verification)

`SCI_L_W9L1_Cell_Cycle_Introduce.html`, stage 6:
- its eyebrow declares `wedo2`;
- `stage_name()` returns **`complete`**, because the `STAGE_NAMES` word table matches
  `\bcomplete\b` in the heading "Build a complete cycle", and that table is consulted before the
  eyebrow route.

Across the 31, **46 `ido2`/`wedo2` are declared and 45 resolve**. This corrects STOP_C3.md's "the
eyebrow route decides 45 and an earlier route decides 0": an earlier route decides 1, wrongly.

- Row-45 counts are unaffected, because `wedo2` and `complete` are both eligible.
- `loop_adapter.earwig_stages` treats `complete` as a closing stage and returns **`{6, 8}`**.
  Transplanting this deck would therefore place the Earwig TA line twice.
- Row 12 asks for at least one such line, so it cannot catch this.
- Changing `stage_name` precedence is a check change, and no check changes without a ruling. The
  finding is carried into PASS C as a **named exception on W9L1**. It is not fixed here.

## `PASSC_ROW45_DERIVED.json`, regenerated on `5e9604cc`

The file is written beside this entry. It records its source commit, its oracle and the W9L1
exception. It uses the repo's own oracle:
- `deck_dom.stage_name` and `identity_channel`;
- `verify_loop.declared_count`;
- `loop_adapter.MODELLING_STAGES`.

`row45_expected` is the size of `verify()`'s own `eligible` set: stages − title − modelling (P1-1).

```
decks 31 | channel {'eyebrow': 31} | declared==resolved: title 31/31, modelling 31/31 | unnamed 0
(stages, title, modelling) -> row45_expected:
   (9, 1, 2) -> 6   x 20
   (13,1, 1) -> 11  x 5
   (7, 1, 1) -> 5   x 3
   (8, 0, 2) -> 6   x 3     <- the three merged title+arrival decks, not yet split
totals: stages 290 · title 28 · modelling 54 · expected panels 208 · panels now 0
```

The old artefact read title 20, modelling **0** and expected 270. It was blind to modelling,
because the pre-#649 oracle named 268 of the 290 stages `unnamed`. Expectations change on every
deck:
- 23 decks: 8 → 6
- 5 decks: 13 → 11
- 3 decks: 7 → 5

The new figures reproduce the derived-expectations table in
`_sx3/handoff_2026-09-22/artefacts/STOP_C1_DERIVATION.md` (28 · 54 · 208) and the order's
"6 on science nine-stage".

## Owed to Matt — unchanged by this item

- The NOAA 2025 value.
- A ruling on `serve-witness.yml:31`.
- The 24 Humanities decks with a panel on the title slide.
- The 390 px served proof. Egress was re-tested at 18:00:03Z: 3/3 `403` on CONNECT to
  `mattroper1977.github.io`. Recorded as a LIMIT.
- New: the W9L1 naming exception above.
