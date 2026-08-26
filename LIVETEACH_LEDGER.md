# LIVETEACH_LEDGER — the Live-Teach Projector Kit build, phase by phase

One readback block per merged phase (order LT-GO). Convention: a phase's merge
SHA lands in the block at the **next** phase's append, because a ledger cannot
carry the SHA of the merge that ships it. Decisions D1–D5 are quoted from the
order and marked as applied where a phase leans on them.

---

## Phase 0 — Recon & decisions (governing spec: MASTER_PROMPT_Live_Teach_Projector_Kit.md)

- **Branch/PR/merge:** `claude/new-session-43lyml` → PR #150 → merge `26dd45d`.
- **Delivered:** `LIVETEACH_RECON.md` — estate survey (HUD, theme, splash/exit,
  reduced-motion, CI), 15-family roster census, placement at
  `/Lessons/liveteach/`, Q1–Q3 recorded.
- **Gates:** all 5 PR checks green; post-merge fieldops + Pages deploy +
  watch-main all green. Negative controls seen live: the stale-evidence
  sweep's self-test, the pr-census emptied-baseline red-proof, and the
  fixture-name sweep's seeded-detection control (run locally).
- **Deferred at the time:** Q1 unknown (dissolved by LT-GO D1); roster ruling
  (settled by LT-GO D2: session-only, in memory, nowhere else); the recon §8
  name exposures (executed as LT1, below).

## LT1 — Pupil-name remediation (safeguarding; LT-GO D3)

- **Branch/PR/merge:** `claude/new-session-43lyml` → PR #151 → merge `309cf7e`
  (all 6 checks green, incl. the games-rendered gate over the edited WorldCup
  files).
- **Delivered:** 23 public files' hard-coded class rosters neutralised
  (`Pupil A…` style; WorldCup squads → England player surnames), one scenario
  and one placeholder sentence de-named, `MASTER_PROMPT_Live_Teach_Projector_Kit.md`
  landed in-repo (the governing spec, verbatim from the session upload),
  REGISTER.md brought up to the code (R-LT101: LT1 record + the `mbm_cc_v1`
  ×175 census R-B01 predates), and `LIVETEACH_LT1_CONTACT_SHEET.md` for Matt's
  post-hoc veto.
- **Gates, with negative controls named:**
  - Name-absence: a local census over 23 real name tokens (names never
    committed) detected 71 files before the edits (positive control), and
    after them exactly the judged-and-left set in the contact sheet;
    **negative control** — a seeded file carrying one census name was
    detected, then removed and the tree re-verified clean.
  - `tools/verify_fixture_names.mjs` clean; **negative control** — its
    `--self-test` seeds a person-shaped fixture and must go red, and did.
  - Diff shape: 29 insertions / 29 deletions across 23 files — array lengths,
    grades and quoting preserved.
- **Corrections to the recon recorded:** the ASDAN `Consent_*` family is
  adjudicated **fictional** (provenance in the files, REGISTER R-D03 family,
  `_passpq/CLAIMS.md`) — recon §8 was wrong to list it; the `6 Art` list reads
  as synthetic (A→L initials) and was replaced belt-and-braces.
- **Deferred (contact sheet C1–C3):** the frozen
  `biology/Structure_of_the_Thorax.html:1372` fallback list (the one real-name
  file left; frozen path + no-self-merged-safeguarding rule); two site-repo
  demo strings; git history retention.
- **Decisions applied:** D3 (names first, contact-sheet + post-hoc veto),
  D4 (self-merge on green), D5 (container limits recorded, not blocking).

## LT2 — Core shell, mode-agnostic (LT-GO D1)

- **Branch/PR/merge:** `claude/new-session-43lyml` → PR → merge SHA recorded at
  next append.
- **Delivered:** `/liveteach/` — `index.html` (launcher: both setups explained,
  the Win+P check, key map), `projector.html` (particle wave sim, timer / hint
  / poll overlays, auto-hiding control strip carrying every teaching action,
  high-lumen and Calm toggles, canonical splash, NAV-1 back link),
  `teacher.html` (optional HUD: renders only what `PROJECTOR_STATE` reports,
  drives the projector over the bus). Shared bus + keyboard-registry +
  motion/theme code is ONE source (`tools/liveteach/core_source.js`) stamped
  byte-identically into all three views (`stamp_core.mjs`, the inline-exit
  pinning pattern); the canonical Made by Matt splash implementation is pinned
  the same way (`stamp_splash.mjs`, hardening bytes verbatim from the Games
  copy). CI: `.github/workflows/liveteach-verify.yml`, registered in
  watch-main's trigger list in the same PR (`--verify-trigger-list` PASS, 12
  workflows).
- **Bus contract shipped as specified:** channel `mbm_liveteach_v1`; every
  message `{v:1, type, payload}`; unknown type / missing v ignored;
  addEventListener only; projector broadcasts `PROJECTOR_STATE` on load and on
  every `HUD_HELLO`.
- **Gates, with negative controls named:**
  - `tools/liveteach/run.sh` — 7 steps, all green: stamp checks (core +
    splash) with their `--self-test` perturbation controls; static gates
    (onmessage assignment, one rAF loop per view, TDZ init rule) with a
    6-vector self-test (3 red vectors must red, 3 green must pass); the
    lt-shell browser suite (~30 checks).
  - Named LT2 gates in lt-shell: resync after projector reload (HUD
    reconciles to the fresh broadcast); H/P toggle both directions by real
    keydown; single-window completeness (timer, hint, poll, pause/resume,
    stop, speed, clear — all driven from the strip with no HUD open); S1 cap
    bites at exactly 150 with the spawn volume proven to exceed it (negative
    control); S2 pause vs stop as different verbs on frame evidence; S3
    speed highlight follows state; S4 construction velocity identical at 1×
    and 2× with the baked-in-speed failure value (80) checked absent
    (negative control); canvas bitmap matches viewport (the estate's
    default-canvas trap); reduced-motion holds the sim still while the
    content stays painted; storage audit — the only key ever written is
    `mbm_liveteach_v1_settings`.
  - CI carries its own red-proof: the workflow perturbs a stamped byte,
    demands rejection, restores, demands a pass.
- **Found by the harness during the build (both fixed before the PR):** under
  reduced motion the sim never painted its first frame — content lost, the
  house rule's exact failure — fixed with an unconditional first draw; the
  suite's http server 404'd favicon requests into the console-clean gate.
- **Adversarial review round (four lenses, 18 confirmed findings, every one
  fixed and now pinned by a suite check):** no heartbeat, so a healthy idle
  pair false-alarmed "projector quiet" at 5 s (live-reproduced; fixed with a
  3 s HUD hello the projector already answers, plus the projector's linked
  latch re-arming on any HUD message); Escape was swallowed by the
  editable-focus guard exactly when its blur half was needed; browser chords
  (Ctrl+P) fired teaching hotkeys; Space on a focused button was stolen from
  native activation (the Calm button was unreachable by keyboard); the HUD's
  Escape didn't do what both key cards promised (new `ESC_TOPMOST` message
  into the projector's topmost chain); the suite's splash check passed
  vacuously (now asserts the splash rendered AND skip beat the auto-close);
  Calm alone still auto-hid the strip that had turned it on; the timer's
  aria-live region sat inside a visibility-hidden subtree and never announced;
  the canonical splash's skip button measured under 44 px (override added
  outside the pinned bytes — canonical untouched; site-repo note in the
  residue); the G-TDZ static gate was bypassable by any statement before the
  wrapped init (regex hardened, new red vector). Suite now 44 checks.
- **Decisions applied:** D1 (single-window first-class; the HUD is optional on
  identical bus code), D4, D5.
