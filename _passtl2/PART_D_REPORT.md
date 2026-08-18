# TL-2 PART D — LundyLoop Professional OS v2.1 (r3): STOPPED AT PHASE 0.5

**`PATCH_TRUTH_FAILED`** — emitted per the package master prompt's categorical Phase 0.5 instruction.
**Repository writes performed for Part D: zero.** Parts A/B/C are unaffected (D5: never stop A/B/C
for a D reason). Part B's PRs (#169, #37) remain HELD exactly as left. This file is TL-2
record-keeping mandated by addendum D6 ("alongside your existing TL-2 report, add a Part D
section") — it is not a deployment write; the uncommitted evidence workspace is
`LUNDYLOOP_V2_DEPLOY_EVIDENCE_2026-08-18/` outside every repo, as instructed.

## What passed before the stop

- **D1**: package zip **6,052,851 B**, sha256 `ab7349be278453e39dc0fae8dbfe5dc57989cffd3a20635c222479e5754fb925`
  — exact match, sidecar agrees.
- **Phase 0**: `verify_deploy_package.py` **PASS 47/47**; `source_release` v2.0 provenance archive
  hash **OK** (and correctly treated as provenance, not the deployable).
- Payload flagship (root) is **byte-identical to Matt's loose upload** (`7850f2a746b7ba64…`,
  177,813 B); suite copy 177,803 B (`8e7bdd17b33fd2da…`). `VERSION.json` = **2.1.0** ✓.
- **D5 pre-checks clear**: Apps `main` (`2e2de986b13c`) has **no** LundyLoop record in `apps.json`
  and no LundyLoop paths — no prior partial deploy. Site has no `/LundyLoop/` runtime copy.

## The Phase 0.5 counts (the 22 numbers)

Root / suite, gate expectation in brackets: PBKDF2_ITERS=600000 **1/1** [1] · Number(env.iterations)||250000
**1/1** [1] · iterations:250000 **0/0** [0] · id="retRecordedBy" **1/1** [1] · recordedBy!=='staff-proxy'
**1/1** [1] · **'Pupil / scribe' 2/2 [0 — DEVIATION]** · id="pupilModeBtn" **1/1** [1] ·
sensitive:hover **0/0** [0] · were NOT restored **1/1** [1] · Operating System · v2.1 **1/1** [1] ·
SpeechRecognition **0/0** [0].

## Diagnosis — the gate expectation is wrong, and it also found something real

1. **v2.0 baseline has 3 occurrences** of `'Pupil / scribe'` (counted in the package's own
   `source_release` archive). **v2.1 has 2.** The delta is exactly the one occurrence P4d's patch
   targeted — `patch_llpro_v2.1.py` asserts exactly-one match per replacement, and its own notes say
   "Every replacement matched exactly once". The build is internally consistent with its patch set.
2. **The packager never executed the gate**: `DEPLOY_PACKAGE_VERIFICATION_REPORT.md` records only
   that the gate was *added*; `FINAL_PROOF_CHECKLIST.md` leaves it as an unchecked box for the
   executor. "Expect 0" was an untested assumption that P4 removed every occurrence.
3. **The two residuals**:
   - `@95999` — **live code**: `appendEvent(c,'VOICE_CAPTURED',…,'Pupil / scribe')` in the pupil-capture
     save path. A genuine P4-adjacent residual: capture events hard-code pupil attribution with no
     `recordedBy` provenance. Lower stakes than the review path — capture *opens* a loop and never
     closes one, so no adult-authored closing act gets sealed as pupil-attributed — but it is the same
     attribution-honesty question. **Candidate P9.**
   - `@156371` — the fictional **demo-data seeder** labelling invented events. Harmless.

## Why the stop stands despite the benign-looking diagnosis

r3 exists because r2 shipped unverified v2.0 bytes on assumption. The gate's entire value is that a
surprise halts the deploy; the executor reasoning a red into a green would repeat the r2 failure
class. The bytes are almost certainly the right bytes — but "almost certainly" is what Phase 0.5 was
written to refuse.

## To unblock (Matt's choice, one line either way)

- **Re-issue as r4** with the corrected expectation (`'Pupil / scribe'` expect **2**), optionally
  adding a **P9** patch first (capture-path `recordedBy`, mirroring P4) — in which case expect **1**
  (demo seeder only) or 0 if the seeder is also relabelled; **or**
- **Override line**: `LundyLoop r3 proceeds with 'Pupil / scribe' = 2 — go`, accepting the two
  residuals as-is (they are: live capture-path attribution + demo seeder).

## Owner-held items — restated as OPEN, not resolved (verbatim per D4)

1. **"Participation debt"** remains the dashboard headline metric — the estate's ratified sense of
   *Influence* is "observable change in the adult's next teaching move"; this app uses it to mean
   overdue adult obligation. Relabel candidate only. **OPEN — awaiting Matt's ruling.**
2. **Closure standard.** A pupil-recorded review is the closing act for every pathway in this app;
   the estate's LL-I ruling is pathway-dependent (BUILD adult receipt · GROW/LAUNCH pupil-owned, no
   adult signatory). The B2 day-close design should land before TAs are trained on this alongside
   `R_Gate_Calibration_Game`. **OPEN — awaiting Matt's ruling.**

## D6 handback summary

- 22 patch-truth counts: above. Package digests: above. PR URLs: **none — stop token instead**:
  `PATCH_TRUTH_FAILED`. Merge SHAs: none. Served hashes: n/a. Behavioural screenshots: not reached.
- Browser-run status: not reached (would have been real Chromium over a real HTTP origin, the
  TL-2 30/30 / 25/25 method).
- Site-repo sequencing decision: not reached; for the record, #169 is unmerged so a future D run
  branches from current site `main` and the seven-leaf generator expectation stands.
- The Part B `/for/pupils/` static-page finding is **irrelevant to D by design** — LundyLoop is a
  Teacher tool (`safeForPupils:false`) and never lands on a pupil surface.
