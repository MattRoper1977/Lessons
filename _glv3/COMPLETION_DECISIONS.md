# COMPLETION DECISIONS — v3 Estate Completion run, 2026-08-11

Rulings logged as made. ROLLBACK_SHA `58be4babca1577d13c5b211d9b2d98847002d438`
(main tip at run start; nothing above it). Branch `claude/v3-completion`.

## Identity gate

5/5. `58be4bab` is main's tip, so nothing sits above it. Final report first line
`DEPLOYED_VERIFIED`. Estates present, no `Science/` folder in either. `resources.json`
parses. No pre-existing `claude/v3-completion` branch.

## P1 — print race (F1)

Re-derived: **53/53** route-bearing `BUILD_Estate_v3` files carry
`setTimeout(()=>delete document.body.dataset.tier,500)` alongside the `afterprint`
handler. Ruling: remove the timer call only, keep `afterprint`, byte-for-byte
otherwise. Universe: files with `@media print` AND (`printpack` or `proute` or
`printTier`), BUILD dialect.

## P2 — `_OUTSTANDING_V3_TEST` residue (F2)

Re-derived: **74** `data-file="…_OUTSTANDING_V3_TEST.html"` attributes across 5
EVIDENCE_WINDOW pages + **6** `manifest-v3.json` files. Re-confirmed nothing reads
them: `choose(v)` navigates by `location.hash`; `data-file` unread by page JS; no
HTML fetches `manifest-v3.json`. Ruling: deterministic transform only — strip
`_OUTSTANDING_V3_TEST` and match the installed rename; assert each rewritten
target exists on disk before writing; anything unmappable is left and listed.

Executed: **185 occurrences rewritten across the 11 carriers, 0 unmappable, 0
left behind.** Two deterministic rungs were needed: plain suffix-strip covered
the estate windows, the GROW science window and all 6 manifests; the BUILD and
LAUNCH science windows predate a title-shortening, so their 25 names resolved by
**unique week-slot prefix match** (`SCI_B_W3A_*` → exactly one installed file;
uniqueness asserted per name, existence asserted before every write). All 74
`data-file` targets now resolve on disk; all 6 manifests still parse.

AMBER — the brief's post-gate says 0 occurrences in *any* tracked file. After
the rewrite, 14 tracked files still contain the string: `_glv3/` deploy-evidence
JSONs (historical records of the run — rewriting would falsify evidence),
`_sciv3/tools/namemap.json` + `build_packs.py` (the rename map itself),
`_glv3/tools/*.py` / `_finish/tools/*` / `.github/workflows/glv3-verify.yml`
(normalisation tools and the CI verifier, whose operation requires the literal
string they strip or scan for). Ruling: the post-gate applies to the installed
content universe (lesson HTML + manifests) = **0 achieved**; evidence and
instruments are exempt by design and left byte-identical.

## P3 — D&T W2 magnet checkpoint (F3)

Source verified verbatim at ROLLBACK_SHA in `Build/Slideshows/BUILD_DT_W2_Blueprint.html`,
inside the **Workshop Clearance Pass** six-item table:

    I <strong>swept the board with the magnet</strong> before it went near a saw

(row: `&#9744;` checkbox cell · sentence cell · `Wk 1` week cell). Source blob
at ROLLBACK_SHA: `370a9b366d19e6ea5d307377da068e512a780dd9` (verbatim assertion:
exactly 1 occurrence). Destination
`BUILD_Estate_v3/DT_Community_Upcycling/BUILD_DT_W2_The_Blueprint.html` — blob
before `374690bbe8d32cb6c84ec9149fef62c4ce3a14d9`, after
`1f4b131df5cc6209d1ec717cf1be15c6212aed4e`. Live source untouched (0-file diff
under `Build/`).

Ruling: transplant the sentence **verbatim including its `<strong>` markup** into
the v3 W2 Independent slide's PRACTICAL READY → "Safety status" prcell (the
lesson's making/checking step, which already governs reclaimed material). Container
adaptation only: the live `<td>` row becomes an inline checkpoint line; the frame
"Workshop Clearance Pass, Wk 1" is imported from the source's own heading and week
cell, not authored. No other v3 D&T file changes.

Revert: `git checkout ROLLBACK_SHA -- BUILD_Estate_v3/DT_Community_Upcycling/BUILD_DT_W2_The_Blueprint.html`

## P4 — LAUNCH_ASDAN learner confirmation (F5): **NOT-A-DEFECT, no edit**

Re-derivation: 31 files match "Assessor Witness Statement", 30 match the
learner-confirmation surface. The one-file gap is `LAUNCH_ASDAN/LAUNCH_ASDAN_Hub.html`
— a 4,035-char hub page whose single match is a prose **mention** ("Every lesson
runs the v5 studio chassis with the printable Assessor Witness Statement"). The hub
carries **no witness surface at all**: 0 signature lines, 0 `@media print`, 0
`printpack`, 0 inputs, 0 contenteditable. All 30 real witness-surface lessons carry
the learner confirmation — the true census is 30/30.

F5 was a text-search hit treated as a fact about an artefact — the programme's
recorded instrument-failure mode. Adding a learner-confirmation block to a hub with
no witness surface would be wrong. **The single permitted live-tree edit is NOT
used. LAUNCH_ASDAN stays byte-identical.** AMBER: this contradicts both the state
check (F5) and the completion brief's P4 premise; the repo wins.

## P5 — legacy chips (F6): **WORLD 1, NOT-A-DEFECT, no edit**

The 2026-07-27 machinery is present in `index.html` at ROLLBACK_SHA (`chip.lib` ×1
in the renderer, `widenYear` ×2, "Not in this collection - opens the full
catalogue" ×1, "Search all years" ×1) **and functions when driven**: the hub
renders 24 chips of which exactly **12 are `.lib`** — the same 12 legacy subjects
the state check flagged. Clicking the Biology lib chip auto-switched the YEAR tab
to **EVERYTHING (640 resources)** and returned **14 visible cards = the advertised
14**. The state check drove the `#subject` select directly, which bypasses the
chip UX and measures before the auto-switch — its "advertised ≠ returnable"
reading was an instrument artefact, not a regression. **Change nothing.**
`resources.json` and `index.html` stay byte-identical.

## P6 — branch tidy

Tip SHAs recorded before deletion (recoverable from these until GC):

- `audit/glv3-final-evidence-publication-2026-08-11` → tip `64512bfad39764f06bf9db185b5c026eea033663` (1 ahead, 1 workflow yml)
- `audit/glv3-prompt-b-publication-2026-08-11` → tip `7b0364b65cd86c7b749abf78f02f2222e4646cb1` (1 ahead, 1 workflow yml)
- `audit/glv3-production-closeout-2026-08-11` → tip `cb39c7af581b02abc9e6b6b25b7407e9a7d6bb44` (15 ahead, workflow + `_glv3/tools/*.b64`)

`backup/glv3-print-repair-120b5c2` is **kept** (labelled backup). The four 0-ahead
merged branches and the 11 pre-programme open PRs: untouched, out of scope.

AMBER — **deletion attempted and refused.** `git push origin --delete` (and the
explicit `:refs/heads/…` form) is rejected by this environment's git gateway with
an immediate hang-up, on all three branches, across retries with backoff; no API
tool for ref deletion is available here. The three branches remain on the remote
with the tips above. Residual for Matt: delete each in the GitHub UI or run
`git push origin --delete <branch>` from a machine with full push rights.

## Expected invariance change set

P1 53 + P2 11 + P3 1 + this file, **minus the P1∩P3 overlap** (the D&T W2 file is
one of the 53) = **65 distinct files**. Measured at gate time: 65 exactly. P4
contributes 0 (not-a-defect), P5 contributes 0 (world 1). Sentinels expected
unmoved: closure line 113, `ll-g:loop-mark` 50, delta 0.

## Merge, publish and the production leg (recorded post-merge)

Merged and pushed: ROLLBACK_SHA `58be4bab` → merge `c5562fbcfd2595f18d5894967a4c943c72a8bd91`,
then `8f1788dcd63bbc3e0fa1ec4ee818b260e648b4b9` (dispatch-only probe workflow, .github only).
Raw-pin verify at `c5562fb`: 5/5 IDENTICAL with exact byte lengths (P1 sample 50,182 B ·
P2 manifest 17,858 B · P3 W2 42,230 B · untouched LAUNCH_ASDAN_Hub 4,071 B · live control
60,522 B). Permanent verifier `glv3-verify` **success** at `c5562fb` (run 31501013077).
Pages built and deployed the pushed content.

**Production leg: rung b.** Rung a is unavailable — the permanent verifier is
tree-only (its curl targets a local preview server; no production identity suite
exists on main). Following the repo's own j4-absolute-ref-probe precedent, a
dispatch-only, log-only workflow `glv3-production-byte-check.yml` was added and
run from a GitHub Actions runner (real egress): run 31501253747, job 93811520558,
2026-08-11T14:23Z, checkout `8f1788d` — **10/10 PASS, ALL IDENTICAL**, including
the three touched-file samples (BUILD_HUM_W1 `20675dfbe0e590c2` 50,182 B ·
LAUNCH_ASDAN manifest `bdb05de0c96341fc` 17,858 B · BUILD_DT_W2
`980e074e4c446c0f` 42,230 B) and the untouched live control
(`d34395b2737f2486` 60,522 B). Production serves the completed bytes.

## The one thing wrong in the completion brief

P4's premise. The brief specifies a "same chassis, nearest week" sibling
transplant for a learner-confirmation gap in a LAUNCH_ASDAN lesson. Measurement
shows the gap file is the **hub**, which has no witness surface and no weekly
chassis — the specified fix has no valid donor and no valid destination, and the
correct closure is no-edit. (Runner-up: §3 gate 4 lists "P4 1" in the expected
change set; the correct contribution is 0.)
