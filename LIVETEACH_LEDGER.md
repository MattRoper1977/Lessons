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

- **Branch/PR/merge:** `claude/new-session-43lyml` → PR #152 → merge `7d80bb0`
  (6 checks green; the first liveteach-verify CI run passed with its in-CI
  red-proof step — job log verified line-by-line, not trusted from the tick).
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

## LT3 — Stage engine (spec Phase 2: G1–G7)

- **Branch/PR/merge:** `claude/new-session-43lyml` → PR → merge SHA recorded at
  next append.
- **Delivered:** manifest schema + loader (G7 — lessons are external data
  under `liveteach/manifests/`, selected by `?lesson=`, whitelisted id, a
  missing lesson is a VISIBLE `role=alert` error and the teaching tools stay
  alive); the exemplar `waves_v1` manifest (real units per W2: f is real hertz
  because the clock is real seconds, lengths are metres through a declared
  `px_per_m` stated on-screen as a scale bar, and every quantitative claim
  carries a machine-checkable `{expr, value, unit}` form); the wave renderer
  inside the ONE existing loop (G4); the evenodd spotlight (G1 — outer rect +
  ROI, single fill, sim untouched beneath); DOM labels and banner built with
  createElement/textContent only (G6) at normalised 0–1 coordinates scaled at
  draw (G3); clamped bidirectional stage sync with the HUD authoritative-free
  (G2); a "playback ×N" chip whenever the wave runs off 1× so the manifest's
  stated f stays honest copy; stage prev/next on the strip AND the HUD.
- **Gates, with negative controls named:**
  - `units_check.mjs` (new): recomputes every claim from its stage's params,
    demands the printed number and unit appear in the claim text, rejects any
    non-normalised coordinate, and enforces the exact-2f rule wherever prose
    says frequency doubles; its `--self-test` proves each rule can red
    (wrong value, pixel coordinate, f=3 "doubling").
  - `lt-stage.test.js` (new, 19 checks): the G1 pixel proof (bright sim
    content sampled INSIDE the ROI, dark veil outside); G2 no-ops at both
    ends on both windows plus a wild `STAGE_SET{index:99}` clamped over the
    bus; G3 label centred at its normalised position; W2 rendered wavelength
    = λ×px_per_m and the playback chip at ×2/gone at 1×; G6 hostile markup in
    stage text stays literal; G7 external load positive + missing-manifest
    negative control with timers proven alive after it.
  - One suite defect found and fixed during the build: the clamp test
    originally sent `STAGE_SET` from the projector's own page — a
    BroadcastChannel never hears its own messages, so the test proved
    nothing; it now travels the real HUD→projector path.
- **Adversarial review round (four lenses, 26 confirmed findings, all fixed):**
  the sharpest were about honesty and about gates that could not fail. (1) The
  "one wavelength" label was pinned to viewport-relative coordinates while the
  wavelength renders in fixed pixels — at 1280 px it captioned 2.88
  wavelengths as one; physical lengths are now shown ONLY by an engine-drawn
  bracket in wave space (`showBracket`), and viewport labels may not claim
  lengths. (2) The 50 ms dt clamp silently slowed "real hertz" under load —
  the wave now takes raw dt. (3) The G6 test was a tautology (it set
  textContent itself); it now serves a HOSTILE manifest through the suite's
  own server and was proven to red against an innerHTML-regressed engine
  before landing. (4) The units gate matched numbers by substring ("12 m/s"
  passed for 2) and never read pupil-visible copy — now digit-boundary
  matching plus a U-VISIBLE scan of copy and labels against params, with new
  red vectors. (5) The wavelength check was arithmetic on the seam — now
  MEASURED from canvas pixels (crest spacing 200 px ±10, scale bar = px_per_m
  ±6). Also fixed: scale bar drawn after the veil and clear of the strip;
  taps repaint under Calm/pause; STAGE_SET validates integers; broken-vs-
  missing manifests get different honest errors, Escape dismisses them, and
  the box never intercepts taps; stage changes announce politely off-screen;
  disabled buttons look disabled; the chip moved clear of the banner title;
  manifests themselves are now gated as pure data (G-DATA) and swept by the
  static gates recursively; warm-up copy rewritten to match what the field
  sim actually does. Stage suite now 30 checks.
- **Decisions applied:** D4, D5.
