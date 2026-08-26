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
  - **S5 (a washed-out classroom projector)** is the high-lumen toggle: a full
    light palette flagged on BOTH `<html>` and `<body>` — the estate's recorded
    page-fill gotcha — with the sim's line and dot colours picked per theme
    rather than low-alpha-on-dark, pinned by the persistence and figure/ground
    checks below.
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
  wrapped init (regex hardened, new red vector). Suite now 45 checks.
- **Decisions applied:** D1 (single-window first-class; the HUD is optional on
  identical bus code), D4, D5.

## LT3 — Stage engine (spec Phase 2: G1–G7)

- **Branch/PR/merge:** `claude/new-session-43lyml` → PR #153 → merge `fd9a4d7`
  (6 checks green).
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
  - **G5 (content accuracy) is a gate, not a promise.** `units_check.mjs`
    reads the manifest and recomputes rather than trusting the prose:
    `U-DOUBLE` requires a stage claiming doubled frequency to carry *exactly*
    2f, `U-CLAIM` matches every stated value against the parameters on a digit
    boundary, `U-VISIBLE` scans copy and labels for an f/λ/v that disagrees
    with the numbers, and `U-COORD` keeps overlay coordinates normalised and
    clear of the banner band. Its `--self-test` carries red vectors, among
    them "12 m/s claimed for a value of 2" and a doubling stage set to 3f.
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

## LT4 — Clicker bridge (spec Phase 3: C1–C4)

- **Branch/PR/merge:** `claude/new-session-43lyml` → PR #154 → merge `b917eb8`
  (6 checks green).
- **Delivered:** the clicker keys registered in BOTH views (C4 — the remote
  survives focus loss): PageUp/PageDown and ←/→ for stages, B and full stop
  for the blackout, F5 answered with honest fullscreen advice; the blackout
  curtain on the projector (above every teaching surface, below the control
  strip so the way out stays reachable; Esc clears blackout FIRST per the
  spec's key map); the projector-side ⛶ Fullscreen button — a real user
  gesture, so it genuinely works — while the HUD's F5 and its Fullscreen
  button only ever advise, because a bus message is not a user gesture (C2,
  stated in the copy exactly as the code behaves); a shared toast channel
  (role=status); blackout state rides PROJECTOR_STATE so the HUD indicator
  and aria-pressed follow.
- **Gates (lt-clicker.test.js, 24 checks):** simulated keydown proof for
  every clicker key in each view; **C1 proof** that B fires exactly one
  action per press (state sequence AND broadcast count over a second
  listener); F5 `defaultPrevented` + toast + projector NOT fullscreened from
  the HUD (the honest-copy negative control); the projector's own button
  genuinely entering fullscreen; curtain z-order measured between banner and
  strip; registry census — every clicker key present in both views exactly
  once. Full harness (12 steps) green.
- **Adversarial review round (three lenses, 12 confirmed findings, all
  fixed):** a held B key strobed the curtain via auto-repeat (blocking —
  repeats are now dropped centrally, one press one action); F5 with focus in
  the hint input reloaded the projector mid-lesson (carve-out beside the
  Escape one; suite asserts `defaultPrevented` at a focused input); clicker
  presses acted invisibly BEHIND the boot splash (the registry now sleeps
  while `.mbm-splash` exists — suite proves a pre-skip PageDown changes
  nothing); the C1 broadcast count raced the 3 s heartbeat about 1 run in 6
  (it now counts blackout TRANSITIONS); `BLACKOUT_SET` was dead code (the C3
  class) — the HUD button now sends it as an idempotent SET, killing the
  crossed-toggle race, with live coverage; a refused `requestFullscreen`
  (managed classroom Chrome) was a silent unhandled rejection — now an honest
  toast, with a stubbed-refusal control; blackout is announced politely in
  both views; the toast hid via `visibility` (out of the accessibility tree —
  the same trap the file itself documents) — now opacity + pointer-events;
  toast hold time scales with message length. Clicker suite now 32 checks.
- **Decisions applied:** D1 (every clicker action also works single-window),
  D4, D5.

## LT5 — Telestrator (spec Phase 4: T1–T5)

- **Branch/PR/merge:** `claude/new-session-43lyml` → PR #155 → merged as
  `ba1d57b`.
- **Delivered:** an ink layer on the projector (above sim/banner/labels,
  below status/blackout/strip; pointer-active only in draw mode) and a
  mini-pad on the HUD, letterboxed to the projector's broadcast aspect (T3 —
  the fragment's fixed 500×220 pad distorted onto 16:9). One stroke message
  type both directions, `TELE_STROKE` (T2), all coordinates normalised 0–1 at
  capture and scaled at draw, line width as a fraction of canvas height (T3).
  Strokes are vectors replayed on resize — never a getImageData backup (T4) —
  capped at 200 with oldest-recycles. Draw mode freezes the sim and restores
  the previous running state on toggle-off, synced over PROJECTOR_STATE (T5).
  D/C keys in both views; three named colour swatches + two widths riding
  each stroke; `TELE_SYNC` hands a reloading HUD the full ink so the
  reload-desync class stays dead; incoming strokes are validated and clamped,
  malformed ones ignored silently per the bus contract. Single-window mode
  draws directly on the projector (order D1); ink persists nowhere.
- **Gates (lt-tele.test.js, 14 checks):** pixel-evidence both ways — a
  projector stroke paints the mini-pad at the same normalised spot and a pad
  stroke lands at its normalised position on the different-sized projector;
  resize-preserves-strokes at the same normalised point; pad aspect equals
  broadcast aspect; freeze/restore on frame evidence; C clears both screens;
  malformed-stroke negative control; TELE_SYNC repopulation after HUD reload;
  storage audit unchanged. Two suite defects found while building (both
  environmental truths worth recording): the pad card sat below the fold so
  the synthetic mouse never touched it (scrollIntoView first), and a
  backgrounded page throttles rAF, so frame counting fronts the page first.
- **Adversarial review round (three lenses, 16 confirmed findings, all
  fixed):** three blocking — a stale `savedRun` let draw-off silently revert
  the teacher's explicit mid-draw Stop (any non-telestrator run change now
  supersedes the saved state, with a negative control); all three ink colours
  measured under 2:1 on the high-lumen page (strokes now carry a swatch NAME
  on the wire and each view resolves a per-theme hex at draw time, with a
  pixel control proving the light variant is darker); the strip parked itself
  over the board during drawing (ink-layer pointer traffic no longer wakes
  it). Also fixed: the pad now draws only while draw mode is on and dims
  otherwise (a stray phone touch cannot paint the class screen, and the
  projector refuses off-mode strokes too); capture now honours the
  validator's own caps — points clamp 0–1 at capture and a marathon stroke
  auto-splits at 2000 points so nothing a view sends can be something its
  peer refuses (the split initially orphaned its continuation by resetting
  the pointer id — caught by the suite, fixed); a second finger or palm never
  hijacks a stroke (pointer-id guard); draw-off commits an in-flight stroke;
  per-move rendering is incremental, not a full replay; `TELE_SYNC` answers
  only fresh hellos, not every heartbeat; draw mode gets a persistent chip
  (touch boards have no cursor) and polite announcements in both views;
  `setPointerCapture` degrades gracefully for synthetic/assistive pointers.
  Tele suite now 22 checks.
- **Decisions applied:** D1 (mini-pad dual-mode-only), D4, D5.

---

## LT6 — URL serializer + QR (spec Phase 5: U1–U3, Q1–Q2)

- **Branch/PR/merge:** `claude/new-session-43lyml` → PR #156 → merged as
  `b9493db` (all 6 checks green; the liveteach job's log read line-by-line to
  confirm the 19 steps and the in-CI red-proof genuinely ran).
- **Delivered:** a share address and a QR panel on **both** views. The
  serializer's whitelist is the privacy boundary: `lesson`, `stage`, `speed`,
  `hl`, `tag` — five keys, defaults omitted (a fresh lesson shares as a bare
  address), and nothing else is ever serialized. Hint prose, poll, timers and
  ink deliberately stay off the wire; there is no path by which a pupil-facing
  sentence reaches a URL or a QR code. **U1:** values are stored raw and
  encoded exactly once, by `URLSearchParams` at write time — the fragment
  stored `encodeURIComponent` output and let the params object encode it
  again, so tags arrived mangled. **U2:** `broadcast()` mirrors state into the
  address bar with `replaceState`, so an hour of teaching adds nothing to the
  back stack; the single `pushState` is the Bookmark button, and a `popstate`
  handler re-applies the address so the back button restores the *state*, not
  just the URL. **U3:** `f` and λ never travel at all — they live in the
  manifest with real units (LT3), so the "(Hz)" mislabel has nowhere to
  recur. **Q2:** the address shows as a selectable readonly input,
  pre-selected on open, and survives when the QR cannot render; Copy falls
  back honestly when a school machine blocks the clipboard.
- **Q1 — the QR engine, rebuilt and machine-proven.** The reviewed fragment's
  encoder computed ONE Reed–Solomon block at versions 4 and 6, where ECC-M
  requires 2 and 4 interleaved blocks — its own comments said "2 blocks"/"4
  blocks" while never interleaving, so anything over ~44 bytes could not
  scan. `tools/liveteach/qr_source.js` carries the standard per-version block
  table *with* interleaving, evaluates all eight masks by the four penalty
  rules, and caps at version 6 (106 bytes) with an honest throw above it. It
  is stamped byte-identically into both views by `stamp_qr.mjs` (the pinned
  region pattern; `--check` reds on drift, `--self-test` proves it can).
- **Gates (`qr_gate.mjs`, an INDEPENDENT decoder):** vendored jsQR round-trips
  the exact string at **every allowed version 1–6**; all **eight masks** are
  forced and decoded at both a single-block and an interleaved version (the
  registry asked for mask verification, not assumption); the shipped mask is
  proven to be the lowest-penalty one, so the rules are live rather than
  decorative; every capacity boundary v1–v5 is pinned at the last byte that
  fits and the first that steps up. **Negative controls:** a corrupted matrix
  fails to decode, and the fragment's own single-block v4 is *rebuilt here*
  and shown undecodable — proving this gate would have caught the defect Q1
  documents.
- **Gates (`lt-share.test.js`, 55 checks):** the tag round-trips raw → URL →
  raw with the double-encode red control alongside; history discipline
  (walking a lesson adds nothing, Bookmark adds exactly one, back restores
  stage AND speed); the QR canvas compared **module for module** against
  `LTQR.encode` of the address actually shown, demanding pure black on pure
  white, with a flipped-module red control proving the comparator can fail;
  the whitelist audited with hint prose, poll and timer all live; hostile boot
  params clamped or dropped; the Esc ladder; the HUD building the projector's
  address from broadcast state. Full harness now **19 steps**.
- **Adversarial review round (six lenses):** one confirmed by an independent
  verifier, the rest adjudicated in-session after the verifier fleet hit a
  usage limit — nothing was treated as refuted by default. Fixed: an unusable
  `?lesson=` (wrong charset) silently became the default lesson while the
  first URL sync destroyed the evidence, so Share exported the wrong lesson as
  though it were meant — it now raises a visible error carrying the rejected
  name, and does not tell the teacher to check a bar it is about to rewrite;
  `SIM_SPEED` accepted any number and would serialize an address its own boot
  params reject; `?hl=1` from someone else's link silently rewrote this
  browser's saved display preference (`setHighlumen` gains a transient mode —
  only a real button press persists); the panel claimed `aria-modal` while the
  strip stayed live above it and its toast sat outside it; the safeguarding
  warning never reached the tag field (focus lands past the visible line) and
  the too-long flip was silent; Q during blackout opened a panel under the
  curtain and handed focus to something invisible (Q now advises, and
  blacking out stands the panel down); launcher and HUD copy claimed the
  address "reopens this lesson state" when it carries stage, speed and display
  only. **Five of my own new checks were vacuous** and were rebuilt on
  evidence — the whitelist check could pass on an address with no params, the
  reload check compared a state identical on both sides, the too-long check
  read an inline-style proxy instead of what is visible, and neither the HUD
  follow nor the too-long recovery verified the canvas re-encoded, so stale
  pixels under a fresh address would have passed.
- **Decisions applied:** D1 (both views first-class — the panel is on the
  projector too, not HUD-only), D4, D5.

---

## LT7 — Cold-call picker (spec Phase 6: P1–P5; order LT-GO D2)

- **Branch/PR/merge:** `claude/new-session-43lyml` → PR #157 → merged as
  `373ce52`.
- **The roster rule, and the ruling behind it.** P1 asked the picker to read
  the estate's roster storage. Order LT-GO **D2 overrides it**: the class list
  is **session-only** — typed or pasted at the start of the lesson, held in one
  variable per tab, and written to no storage key, no address, no QR, no log
  and no bus message. Closing the tab is the delete button, and the launcher
  says so in as many words. The LT2 storage audit still finds exactly one key,
  holding display settings. No new key family was created, so P1's actual
  prohibition ("never a new key family without Matt's sign-off") is honoured
  by having no key at all.
- **P2 — the guarantee is structural, not statistical.** The reviewed fragment
  gave every pupil a minimum weight, so the pupil who had just answered could
  come straight back up. In a mainstream room that reads as keeping people on
  their toes; in an SEMH alternative provision it reads as being singled out,
  and the escalation costs the rest of the lesson. Weight here **is** "draws
  since you were last called", which is exactly 0 for the pupil who just
  answered — they cannot be drawn next, not merely rarely — and the same
  counter does the decay-recovery that keeps the room balanced. No floor to
  tune, no dice roll to lose. The pedagogy is documented at the top of
  `tools/liveteach/picker_source.js`.
- **Q2, as answered.** A picked name shows on the teacher's screen only. The
  ONE sanctioned way a name crosses the bus is the explicit "Show on
  projector" press, and that message carries the name and nothing else — no
  list, no history, no odds. The projector also carries its own picker for
  single-window teaching (D1: every teaching action reachable there). Rosters
  do not travel between windows, so in a two-window setup that panel simply
  stays empty; its copy says plainly that the class can see this screen rather
  than implying a privacy it cannot offer.
- **Gates (`picker_gate.mjs`, 10,000 draws):** zero immediate repeats; every
  pupil within **3.04%** of an even share (min 808, max 858, even 833); zero
  repeats with a quarter of turns passed, so passing is a scaffold rather than
  an exit; the guarantee holding in rooms of 2, 3, 4 and 6; with one pupil
  present it degrades **openly**, flagging every draw it could not cover
  rather than pretending; attendance removing and restoring a pupil mid-lesson;
  displayed odds summing to exactly 1 with the absent pupil listed at zero.
  **Negative controls:** the fragment's own min-weight floor is rebuilt and
  shown to produce back-to-back calls that this gate counts; a deliberately
  biased draw blows the balance tolerance, so a passing balance means
  something; an absent pupil is never drawn in 500 attempts.
- **Gates (`lt-pick.test.js`, 62 checks — 36 at first write, the rest added by the review round below):** a third page taps the bus and
  records every message, then every roster name is searched for across the lot
  after 13 draws — with a check that the tap heard live traffic, so the
  no-names result cannot be vacuous. Also: no storage key, no name in storage,
  no name in the address, the textarea emptied on load; a name containing
  markup renders literally with no element created from it (P3); attendance
  stated in text and honoured over 40 further draws (P4); the cooldown visible
  at 0% and labelled "just asked" (P2); a reload forgetting the list with
  nothing left behind to restore it from (D2); N/M in both views, registered
  once each; the projector's own picker, the Escape ladder and the blackout
  stand-down; and a projected name suppressed under print media, because
  printing makes a file and the non-negotiables put names out of exported
  files. The roster fields opt out of autofill and spellcheck for the same
  reason.
- **Engine ships as one stamped source** (`picker_source.js` → both views via
  `stamp_picker.mjs`), so the 10k simulation exercises the exact bytes that run
  in the classroom. The stamper's self-test perturbs the P2 weight into a
  min-weight floor and demands the drift gate notice. Harness now 23 steps.
- **Adversarial review round (five lenses) — and it found a real break in the
  guarantee this phase rests on.** Reproduced before fixing: pick Ann, mark Ann
  away, draw, mark Ann back — Ann is drawn again immediately. Two causes.
  `since` advanced only for pupils who were present, so a pupil marked away
  moments after being called kept `since = 0`, and a frozen zero never
  expires; and `setPresent` CLEARED `st.last` when that pupil went away,
  erasing the single fact P2 depends on. Now: a returning pupil re-enters at
  least at 1 (in the pool, ordinary priority — someone who has just walked
  back in is the last person who should be cold-called on the spot), `st.last`
  is kept because an away pupil is already excluded by `present`, and the
  uniform fallback drops the just-called pupil too whenever anyone else is
  available. The gate now fuzzes attendance churn — 16,000 draws across rooms
  of 2, 3, 4 and 8, a third of turns flipping somebody's attendance — counting
  only AVOIDABLE repeats, and a **red control rebuilds the pre-fix engine and
  shows the same fuzz catching it: 140 avoidable repeats before, 0 after**.
  The balance tolerance dropped 15% → 8% across six seeds (the engine's own
  spread measures under 4.5%, so 15% sat five times above the noise it was
  policing), and the roster-cap probe now uses 80 DISTINCT names — the old one
  deduplicated to a single entry and asserted 1 ≤ 40.
- **Also fixed, each pinned:** "0 — clear every overlay" left a pupil's name on
  the wall; drawing again left the PREVIOUS pupil named to the room while the
  HUD showed the new one (a new draw now retracts, and the HUD renders what is
  actually on the projector from the broadcast, with a Clear control that stays
  reachable after a reload); a name could be projected under the blackout
  curtain and reported as shown; the two centred panels could both open at the
  same depth and strand focus in a buried card; marking a pupil away destroyed
  keyboard focus in both views, and the projector announced nothing when it
  did; away rows measured 2.66:1 in high-lumen; rows could not wrap, so a name
  collapsed at phone width while a decorative bar kept its 60 px; eligible
  pupils rounded to "0%", which is what an *excluded* pupil shows; the
  projector's forty attendance buttons had no focus ring. Roster parsing is
  Unicode-safe (NFC dedupe, character-wise truncation) and reports names
  dropped past the cap. Copy corrected where it outran the code — the absolute
  no-repeat claim, the two-window safeguard described as if it applied to
  single-window teaching, the HUD's "never sent to the projector" above a Show
  on projector button, and the projector panel warning only about the picked
  name while displaying every name on a class-facing screen.
- **Suite gaps the review found, all closed:** the console listener filtered to
  type `error`, so a `console.log` of a pupil name was invisible — it now
  captures every level and scans them; the storage audit read only
  localStorage, now sessionStorage and cookies too; the markup probe never
  reached either of the projector's name sinks, so an `innerHTML` there would
  have shipped green — both are now fed hostile text, one of them over the
  bus; nothing had ever read the projector's ADDRESS or the string the QR
  encodes while a name was on the wall; 40 draws were asserted against a
  12-entry history window; and a `KeyQ` press documented as a check asserted
  nothing. Suite now **62 checks**.
- **Decisions applied:** D2 (session-only roster — the ruling this phase turns
  on), D1 (a picker on the projector too, since rosters do not travel), D4, D5.

---

## LT8 — Classroom extras (spec Phase 7: X1–X4)

- **Branch/PR/merge:** `claude/new-session-43lyml` → PR #157 → merged as
  `373ce52`.
- **X1 RAG tally.** 7/8/9 count stuck / nearly / got it, from either window,
  into the projector's state. **Counts only** — and that is the whole
  safeguarding story: the panel is anonymous *by construction* rather than by
  policy, so there is no name to leak and nothing to reconstruct one from.
  Each row carries a word, a shape glyph and a number, so it reads with the
  colour ignored. The panel reveals itself on the first vote (a counter nobody
  can see is a counter nobody trusts). Counts live for the lesson: memory, a
  reset button, and the tab close.
- **X2 silent bell.** A slow amber breath plus a banner, **button-only** — the
  spec retired the pulse key so B stays blackout and nothing else. Under
  `prefers-reduced-motion` **or Calm** the breath is replaced by a held tint
  and the banner alone: the house rule's named substitution, so the cue
  survives when the motion goes. Announced, so a screen-reader user gets the
  same signal.
- **X3 audio.** Off at every load, with **no stored preference to inherit** —
  in an SEMH room a toggle that remembers "on" from last lesson is exactly the
  surprise the rule exists to prevent, so the *absence* of persistence is the
  feature. Earcons are single shaped tones under 300 ms at a peak gain of
  0.06, always scheduled to stop; TTS speaks a projected cold-call name and the
  end of a timer, cancelling before each so nothing stacks or loops.
- **X4 sparkline.** A standalone SVG built from the recorded series —
  cumulative lines per colour, its own text labels and an aria-label, so it
  still reads pasted into a report. Clipboard first, with the download
  fallback treated as the real path rather than a courtesy, because school
  machines block clipboard writes; the toast says which actually happened.
- **Gates (`lt-extras.test.js`, 48 checks — 33 at first write, the rest added by the review round below).** The two the spec names for this
  phase are both on evidence, not proxies. **Audio defaults:** a patched
  `AudioContext` counts LIVE oscillators, so a wired-but-silent path is
  distinguishable from a working one — zero starts with sound off across three
  sound-capable actions, a real start with it on, peak gain in range, a
  scheduled stop, and OFF again after a reload. **Reduced-motion bell:** a page
  booted under the OS setting, reading the *computed* animation, then proving
  the static banner and held tint carry the cue. Plus the SVG parsed back
  through `DOMParser`, the clipboard-blocked download exercised, and the tally
  proven to contain no name with a cold-called pupil live in the session.
- **Adversarial review round (four lenses; nine findings confirmed by
  verifiers who reproduced them).** "Copy graph" wrote SVG *source* as plain
  text while the button, the toast and the launcher all promised an image —
  paste that into a document and you get a wall of angle brackets. It now
  writes a real PNG through `ClipboardItem` where the browser supports it,
  falls back to SVG source, then to a download, and each path says which
  happened. The exported graph separated its three series by hue alone, which
  fails the colour rule in the one artefact most likely to be printed in black
  and white: each series now carries its own dash and its own end label. A
  single recorded vote exported a blank graph (one moveto, no lineto, which
  SVG paints as nothing), and the 500-entry cap let the drawn curves drift
  below the totals printed beside them — the legend is now read from the same
  series the curves are. A vote forced the tally back up after the teacher had
  hidden it to take an uninfluenced vote; the auto-reveal is now once per
  tally and any explicit hide disarms it. "0 — clear every overlay" left the
  tally and the bell on the board (the counts survive — that is what Reset is
  for). Taking a name off the wall did not stop the speech saying it. The
  panel's heading was an orphaned `h3`, and the HUD announced nothing at all
  when the tally moved or the bell rang.
- **The audio gate was the weakest part of the suite and is now the
  strongest.** The probe wraps `AudioNode.connect`, so a tone routed nowhere
  is distinguishable from one that reaches the speakers; it records start and
  stop times, so the spec's "earcons ≤ 300 ms" is asserted rather than
  assumed; and the silence-with-sound-off check now fires a path that can
  actually speak, since the three it fired before could only ever make
  earcons. **Every bell check read a class name on an element that ships
  `visibility: hidden`** — all of them would have passed with nothing on
  screen — so they now read what is painted. The no-persistence check
  inspected values and never keys.
- **Decisions applied:** D1 (every extra reachable on the projector; the HUD
  mirrors), D4, D5.

---

## LT9 — Worksheet engine (spec Phase 8: W1–W5)

- **Branch/PR/merge:** `claude/new-session-43lyml` → PR #157 → merged as
  `373ce52`.
- **W1, the serious one.** The reviewed fragment's line-art conversion
  stripped the grid, leaving a figure the worksheet then asked pupils to
  *measure*. Here the threshold pass runs **first** and the calibrated grid is
  drawn after it, so nothing can strip it: half-metre rules both ways, a
  heavier line every metre, and a scale bar labelled "1 metre" on a white
  backing. The arithmetic is checkable — at λ = 2 m the figure draws one
  wavelength as 320 px against a 160 px scale bar, so a pupil measuring off
  the grid gets 2 m exactly.
- **W2 honest units.** The model-to-real mapping is *stated* ("the grid squares
  are 0.5 m across"), the printed f, λ and A are the stage's own, and
  v = f × λ works out. Off a wave stage there are no honest numbers to print,
  so the sheet says there is nothing to measure rather than inventing some.
  Frequency is handed over in as many words, because a still drawing cannot
  show it and implying otherwise would be the same dishonesty W2 exists to
  stop. **W3:** plain text "v = f × λ" — the fragment printed the LaTeX
  source. **W4:** answer lines are bordered divs, because most print engines
  drop background gradients and a worksheet whose lines vanish at the printer
  is worse than none. **W5:** the threshold is live — it *is* the cut that
  makes the line art.
- **The answer is deliberately not on the sheet.** A first pass printed a
  worked-answer box and quoted the wavelength back in task 4, which between
  them made two of the four tasks pointless. Both are gone; the teacher gets
  the working on the HUD's stage card instead, where the pupils are not
  looking. The header prints the stage title and the date and leaves a **ruled
  space** for a name rather than printing one — nothing is stored, so nothing
  can be printed, and a cold-called name showing on the wall is not carried
  onto the page.
- **Gates (`lt-sheet.test.js`, 41 checks — 37 at first write, the rest added by the review round below).** The spec names this phase's gate
  and both halves are here. The exported PNG is **decoded back to pixels** in
  the page and searched for grey grid runs in both axes and for the scale
  bar's longest contiguous black run with a tick at each end — with a **red
  control** proving the same sampler finds neither in a blank image (the first
  version of that sampler counted the "1 metre" label as bar, which the tick
  check caught). The no-`$` half checks the printed text and the markup for
  LaTeX escapes. Plus: bordered lines read under *print* media with their
  computed border and no background image; the sheet proven to be the only
  thing printed; the answer proven **absent** on both wave stages and present
  on the HUD; and W5 proven live by rendering at two thresholds and showing
  the pixels differ.
- **Decisions applied:** D1, D4, D5.
- **Adversarial review round — a content-accuracy break, confirmed by
  rendering.** The scale bar was painted on an opaque backing plate AFTER the
  curve, and on the full-amplitude stage that plate erased the bottom of the
  trough: a pupil measuring the wave's height got **0.875 m where the lesson
  said 1 m**. The geometry now keeps them apart by construction — the figure
  reserves a band for the bar, and `pxm` is capped so a full wave always fits
  the drawing area. The suite measures the exported PNG on **every** wave
  stage and demands crest and trough be symmetric about the axis, with a red
  control that plates over a trough and proves the scan reports it.
- **The sheet also gave away its own tasks.** It printed the wavelength and
  amplitude that tasks 1 and 4 ask pupils to measure, so the calibrated grid
  and the scale bar existed for work nobody needed to do. The given box now
  carries only what a still drawing genuinely cannot show — the frequency —
  and discloses the playback speed when it is not 1×, since "what the class
  saw" quietly meant something else at ½× or 2×. The print layer no longer
  stays `aria-hidden` when it IS the printed document.
- **The W1 gate proved existence, not calibration.** It counted grey runs and
  a black run; it now MEASURES the grid pitch against the scale bar and
  demands one be exactly half the other, so a bar drawn at half a metre while
  labelled "1 metre" — or a grid at the wrong spacing — goes red.
- **Decisions applied:** D1, D4, D5.

---

## LT10 — Close

- **Branch/PR/merge:** `claude/new-session-43lyml` → PR #157 (LT7–LT10) →
  merged as `373ce52`, all six checks green. The liveteach job's log was read
  line by line before merging, per the estate's assert-on-evidence rule: all
  24 steps genuinely ran, including both statistical simulations and all eight
  browser suites.
- **Delivered:** `LIVETEACH_README.md` (what the kit is, the same-device
  constraint stated plainly, clicker setup, the full key map, and a section on
  pupil names saying exactly what the kit does and does not do with them);
  `LIVETEACH_PHONE_CHECKS.md` (the physical checks only a real device settles,
  **none ticked by the session** — the first is that the deployed page exists at
  all, since this container's proxy refuses the live host); and
  `LIVETEACH_RESIDUE.md` (the handover: what was deferred, what could not be
  verified from here, and every delegated decision with the override line that
  reverses it). The launcher gained a troubleshooting card for the four things
  most likely to look like faults and not be.
- **Final gate state:** `tools/liveteach/run.sh` — **24 steps**, all green,
  carrying **335 checks** in total.
  Four stampers with their perturbation self-tests, the static gates
  (`onmessage`, one rAF loop per view, the TDZ rule, manifests-are-data), the
  units checker, the QR decode gate against a vendored independent decoder at
  every allowed version and every mask, the picker's 10,000-draw simulation
  plus the attendance-churn fuzz, and eight headless-browser suites
  (`lt-shell` 45, `lt-stage` 30, `lt-clicker` 32, `lt-tele` 22, `lt-share` 55,
  `lt-pick` 62, `lt-extras` 48, `lt-sheet` 41).
- **The lesson worth keeping from this build.** Across the phases, the
  adversarial review rounds found **more defects in my own gates than in the
  product** — checks that read a class name on an element that ships hidden, a
  console listener filtered to a level the defect would never use, a storage
  audit that read one store of three, a probe that counted an oscillator
  starting without asking whether it reached the speakers, a grid gate that
  proved the grid existed but never that it was calibrated, and a roster-cap
  probe whose input deduplicated to one name so it asserted 1 ≤ 40. Every one
  of them was green. The rule that caught them is the estate's own — **assert
  on evidence, not on proxies** — and the practice that made it stick was
  writing the red control first: a check that has never been shown to fail is
  not yet a check.
