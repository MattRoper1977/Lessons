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

---

# Part D r4 run — LundyLoop Professional OS v2.1.1: DEPLOYED, PUBLISHED, PROVEN (2026-08-18)

Sentinel: `townlife-tl2-2026-08-18-PARTD-r4-TOP`
The r3 record above stays as history per the r4 addendum ("append the r4 run beneath it").
Owner ruling that opened this run: the r3 stop was correct; r4 fixes the residuals (P9), not the
expectation. Re-run from D1.

## D1/Phase 0/0.5 — package identity and patch truth

r4 zip **6,054,748 B, sha256 `1444acb9028636fce1ba55c41ef6ea086766953819128cbb09f957bb50828afd`**
(sidecar agrees; r3 `ab7349be…` superseded). `verify_deploy_package.py` **PASS 48/48**;
`source_release/` v2.0 archive hash OK (verified, not installed). The SHIPPED
`run_patch_truth_gate.sh`: **PATCH_TRUTH_PASS — all 22 counts** on both flagships (root
**178,005 B**, suite **177,995 B**), including `'Pupil / scribe'` **0/0** (the r3 deviation),
`Operating System · v2.1.1` 1/1, VERSION 2.1.1. The r3→r4 delta is exactly P9: capture-path actor
derived from the pupil's chosen route with `scribed`+`pupilPresent` detail; demo seeder `demo:true`.

## Phases 1–6 — install, parity, pin, gates, PRs, merges

- Apps branch `codex/lundyloop-professional-os-v2-apps-2026-08-15`: payload 23/23 bytes-unaltered;
  apps.json +1 Teacher-tools record (37 total, derived); index.html AUDMAP + no-JS leadCount
  "Thirty-seven"; `tools/lundyloop/` verifiers + CI workflow installed. Two first-CI findings fixed
  without payload edits: workflow step order (static verifier before the `_reference/site`
  checkout) and `.gitattributes` declaring payload-Markdown hard breaks.
- Phase 2.5 parity: `mbm-platform.css`/`js` byte-identical to Site canonical (b520cf36…/095a29e6…);
  verifier copies byte-identical pre-pin → no parity sync needed.
- Phase 3: paired pin `94fb05b883d9 → b70fdca96ba9` in BOTH verifier copies via `pin_manifests.py`;
  `--check` green; cross-estate verifier PASS + positive control in Apps and Lessons.
- Phase 4: static verifier PASS + control; browser verifier on real Chromium over real HTTP 55/57,
  the 2 fails proven environmental by pristine-main control (favicon probes; session proxy).
- **PRs and merges (Phase 6, coordinated):** Lessons **#134** → main
  `5bfba62408d27a1960bda50b911d261906ecebe6`; Apps **#15** → main
  `9672d6b7bc12d865e4d6a2109e0bd26f282bd1c1` (both 2026-08-18T19:10:53Z). All four Apps-main
  workflows at that head green (Verify LundyLoop 32175138077 · cross-estate unification
  32175138089 · reading-theme parity 32175138244 · pages build 32175136356).

## Phase 7 — exact served bytes (live proof)

`live-bytes` job (run 32175138077) ran on the GitHub runner where madebymatt.uk is reachable:
**`"status":"PASS"` on attempt 1** — every payload record ending `.html`/`.jpg` (9 of 22; the other
13 are docs, repo-proven only) fetched with cache-busting `?source=<merge-sha>` and matched
repository sha256 exactly. **Served flagship hashes:** root `LundyLoop_Professional_OS.html`
`97a84d6b58989e5fd2fcbc5071aa784e7b140e63f5c6b5060f4bc3240b986bfc`; suite
`LundyLoop_PRO_Participation_Operating_System.html`
`dec3630866c0a52070d26d196bdea55cc3af8f06ef64b815991788e9b0523ba8` (suite `index.html` + LAUNCHER
`19b32ad3…`). Every checked path is new in this merge, so a byte-match cannot be a stale deploy.
Pages provenance direct: `pages build and deployment` run 32175136356 at the merge SHA, success,
completed 19:11:15Z. Artifact `lundyloop-live-32175138077` (id 9338765896) retains the JSON 90 days.
**Browser-vs-production: LIMITED** (madebymatt.uk proxy-blocked from this session) — compensated by
the runner-side byte proof + the CI Playwright browser run at the merged tip; Matt's phone check
remains the human confirmation.

## Phase 8 — Site discovery (sequencing decision per D3)

Branched `codex/lundyloop-professional-os-v2-discovery-2026-08-18` from freshly fetched site main
(`4b74945`, post-PH-3; **#169 still unmerged — not touched**; no rebase needed). Changes confined to
the declared discovery surface: `data/source-manifests/apps.json` mirrored byte-for-byte from the
merged Apps commit (blob `4cd4d80a…` equal both sides; 37 records derived); provenance `sources.apps`
→ `9672d6b7…`/37; guarded search-index write with **exactly the seven declared leaves** the prompt
states (`entries.app-lundyloop-professional-os`, `counts.tool`, `counts.total`,
`sourceHashes.apps.json`, `sourceHashes.provenance.json`, `sourceProvenance.apps.commit`,
`sourceProvenance.apps.entries`) — one entry ADDED, zero removed, `--check` reproduces post-commit;
Teach Hub "Assessment and evidence" card added via `render_discovery_hubs.py` (both hubs re-render
`--check` green; education-hub byte-identical). New index entry `safeForPupils:false`, audiences
teachers/schools-semh. `/for/pupils/`, `/games/`, `games.json`, TOP rail untouched (verified: zero
mentions outside teach + index). **Site PR #170** → 12/12 checks green → merged to main
`595b4d098e5362ba3c28bc769806dea7a210aca6`; all 9 site-main workflows at that head green, including
"Professional site live verification" and "Deployment provenance".
The Part B `/for/pupils/` literal-HTML finding is **irrelevant to D by design** — LundyLoop is a
Teacher tool and never lands on a pupil surface.

## Phase 10 — behavioural screenshots (demo data, fictional, cleared after)

In `LUNDYLOOP_V2_DEPLOY_EVIDENCE_2026-08-18/phase10/` with in-image captions stating the data is
fictional: (a) `phase10_a_pupil_mode_mobile.png` — 390 px, Pupil mode on: only Pupil Capture
navigable (all other nav hidden), top actions gone except the Shield, "Hold to return to staff
view" exit bar visible; (b) `phase10_b_staffproxy_review_due.png` — Return & Review, demo case R5,
"Who is recording this review?" = **Staff on the pupil's behalf — pupil NOT present**, case badge
**"Review due" before and after** the staff-proxy record (loop stays open). Demo data cleared
afterwards and proven cleared on reload (return queue empty). `PHASE10_RESULTS.json` records the
assertions; zero page errors.

## Owner-held items — restated OPEN, not resolved (verbatim per D4)

1. **"Participation debt"** remains the dashboard headline metric — relabel candidate only.
   **OPEN — awaiting Matt's ruling.**
2. **Closure standard** — pupil-recorded review closes every pathway here; the estate's LL-I ruling
   is pathway-dependent (BUILD adult receipt · GROW/LAUNCH pupil-owned). **OPEN — awaiting Matt's
   ruling.**

## Token

Every gate above is evidenced: **`LUNDYLOOP_V2_MERGED_PUBLISHED_SHA_PROVEN`** — beside TL-2's own
tokens, not in place of them.

Sentinel: `townlife-tl2-2026-08-18-PARTD-r4-BOTTOM`
