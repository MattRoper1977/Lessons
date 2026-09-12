# PIN1 — UX2 scheduled census release

## Current checkpoint — PIN1 UX2 census pass merged

Measured 2026-09-12T13:16:02.888Z. Lessons #515 merged as `a20a09b96ddb0cdbe37709631603de82cc8b1d6a`.
The recovered §2.2 fallback is implemented for UX2 alone: existing daily schedule,
all nine existing proof-step outcomes, commit-bound JSON/Markdown/Actions summary,
FAIL on complete failed evidence and UNMEASURED (exit 2) on incomplete evidence.
No trigger paths, existing proof commands, pins or other workflows changed.

PR run `34695419199` and census job `103558313348` succeeded: 9/9 proof outcomes PASS;
all five reporter test methods passed in Actions. Artifact `10298985341` is saved.
All 12 PR checks are terminal: 11 SUCCESS, one independently matched baseline
sweep FAIL (1,418 stale / 6,307 live / 6,899 row labels / 47 unmatched files).
Reviewed, GitHub-tested and merged trees all equal `1e9cea18b5b5eca2d36148bf5edf2ec391c4751d`.

At this checkpoint, post-merge UX2 `34695886241`, publication `34695886467` and
FieldOps `34695886249` are in progress. Do not call them successful from PR results.
The first actual daily scheduled census is also NOT OBSERVED. Next continuation
starts by re-reading these runs; no background poller or dispatch is left running.

This bounded implementation pass is complete; **PIN1_PARTIAL** overall. The original
pinned-file RED/GREEN/DORMANT trigger proofs remain open. LP1's material-scope hold
remains. See `PIN1_UX2_RELEASE.md` and `pin1/DECISIONS.md` on main for exact scope.
Earlier P6 and other completed passes retain their own measured timestamps.


## Exact refs and evidence

- PR: https://github.com/MattRoper1977/Lessons/pull/515
- Base: `4f8227cef7a0191df25145d53fe2bc05f7aa2ef9`.
- Candidate: `4bc04e2976f4cf369ff1c0bbe822184a57b0f2b3`.
- GitHub PR tested merge: `7a47c1bb7884f9e88780fb3291175389d829e863` (the census correctly records this GITHUB_SHA).
- Actual main merge: `a20a09b96ddb0cdbe37709631603de82cc8b1d6a`.
- Local preparation commit: `8b518f1c17cb1271b496aa9288ad01fc206aa141`; remote commit has the identical tree.
- Census artifact: https://github.com/MattRoper1977/Lessons/actions/runs/34695419199/artifacts/10298985341
- Artifact: 1,080 bytes, unexpired when checked; uploaded ZIP SHA256 `1bc25b4fe70000d978d92698b24cf9a191e0a5fa8b54b8124042d9b633f52f32` from upload log. Metadata/log inspected; artifact ZIP not downloaded.
- Original browser evidence artifact: `10298770715`, 3,523,542 bytes, unexpired when checked.
- Baseline sweep job: `103557958483`, exit 2; its full measured headline exactly matches the previous P6 main baseline.

Implementation is four files only: UX2 workflow outcomes/final census, reporter,
reporter controls and DECISIONS. No Apps, Site or Games branch was advanced.
No pupil evidence was emailed. Existing user rulings and programme holds remain.

The census reports outcomes of UX2's actual catalogue, derivation and browser
assertions. Failed job outcomes alone cannot distinguish data drift from environment
failure, so the report sends the diagnosis back to the original proof logs. It
never presents UX2 as a file-pin gate. The declared pin counts in the opening
census have not been remeasured during this pass.

Local and Actions reporter tests are synthetic controls. They prove rejection of
missing/failed evidence; they are not GitHub scratch-branch trigger plants.
Neither a PR run nor a post-merge push is an observed scheduled event.

## Next small pass

1. Re-read the three post-merge runs above at the exact merge SHA; report any new failure without altering a check or pin to make this pass green.
2. Inspect the first actual scheduled UX2 census when one exists. Do not wait overnight or infer its result from the configured cron.
3. Keep PIN1's remaining trigger proofs and LP1's material-scope decision open. SB1 remains due before a second Scratch unit; do not admit that unit ahead of its gate.

PIN1_PARTIAL
