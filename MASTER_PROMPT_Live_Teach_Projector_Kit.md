# MASTER PROMPT — Live-Teach Projector Kit (Phased Build, Commit & Merge)

You are Claude Code working in Matt Roper's madebymatt.uk estate. Matt is a science/art teacher at an SEMH alternative provision (Progress Schools Tees Valley). He works **from his phone only** — he cannot run anything locally. Everything must be proven by you in-repo (harness + measurements) and verifiable by him on a phone or the classroom PC.

## MISSION

Build ONE new standalone classroom tool — the **Live-Teach Projector Kit** — consolidating six reviewed fragments: (1) canvas→print worksheet engine, (2) BroadcastChannel projector/HUD sync, (3) USB clicker bridge + keyboard shortcuts, (4) declarative lesson-stage manifest with spotlight/label overlays, (5) telestrator drawing overlay, (6) URL hash state serializer + QR share + decay-weighted cold-call picker + classroom extras (RAG tally, silent bell, TTS/earcons, SVG sparkline copy).

All six fragments were reviewed in chat and every one had defects — some fatal. The **Corrections Registry** below is binding. You are building the corrected consolidation, not pasting the fragments.

Work in phases. **Each phase = its own branch → commit(s) → PR → merge only when all checks are green and the phase gate passes.** Never push to main directly (main went red on 2026-08-24 from exactly that; the 21-check suite must stay reporting).

---

## PHASE 0 — RECON & DECISIONS (no product code)

1. **Read the estate.** Locate the live `/hud.js`, the reading-theme engine (`/theme.js`, `mbm_reading_theme`), the splash/exit conventions used by the games, the reduced-motion house rule, and the CI check suite. List what you find in `LIVETEACH_RECON.md`.
2. **Census existing roster storage.** Find every localStorage key currently holding class lists (known family: `ps_coldcall_roster` ×~66, plus any `mbm_hud_*` / `lth_*` keys). The cold-call picker in Phase 6 must REUSE an existing roster source. **Creating a new roster key system is a STOP — ask Matt.** The estate already has multiple roster systems; you will not add another.
3. **Placement.** Default: standalone tool at `/liveteach/` (own folder, single-file-per-view or one file with role param — your call, justify it). **Prohibition: none of this code goes into the estate `/hud.js` or any lesson deck.** The clicker bridge preventDefaults arrow keys; merged into the shared HUD it would break deck navigation estate-wide.
4. **Ask Matt these setup questions before Phase 1 if not already answered in your session:**
   - Q1 (gates Phases 1–5): Is there a classroom PC driving the projector that you can plug a USB clicker into, with extended desktop (projector as second display)? *(BroadcastChannel is same-browser-same-device only. If the answer is no, STOP after Phase 0 and report — Phases 6–8 still have standalone value and can be re-scoped as single-window tools, but the sync architecture dies.)*
   - Q2: Should the cold-call selection ever appear on the projector, or HUD-only? (Default if unanswered: HUD-only, with an explicit per-lesson "project name" button.)
   - Q3: Which repo hosts this — the site repo alongside the games? (Default: yes.)
5. Commit `LIVETEACH_RECON.md` + your answers/decisions. PR, merge when green.

---

## NON-NEGOTIABLES (apply to every phase)

- **Privacy:** pupil names live in localStorage only. Names NEVER appear in URLs, hashes, QR codes, exported files, bus messages rendered on the projector (unless Q2 opt-in), or console logs. Render names with `textContent` only — never innerHTML.
- **Honest copy:** no UI text may claim something the code cannot do (see fullscreen correction below). No fake privacy claims.
- **Audio off by default.** TTS and earcons ship behind an explicit toggle, defaulting OFF — this is an SEMH setting; unexpected sound is a sensory trigger. Respect the sensory-shield principle.
- **`prefers-reduced-motion`:** every animation (particles, banner slides, silent-bell flash, toast) must have a reduced-motion path. The silent bell in reduced-motion mode becomes a static colour-change, not a flash.
- **Estate conventions:** Made by Matt splash, exit/back route, no console errors, works at phone widths for the HUD view (Matt may run the HUD on the PC but will *check* it on his phone).
- **Every fix in the Corrections Registry needs a positive AND a negative control in the test harness** (prove the fix works; prove the old failure no longer reproduces).
- **Real units:** any physics shown to pupils uses honest units. Pixels are never labelled Hz. If the sim can't map to real units, label quantities as "model units" explicitly. Content accuracy is a hard gate (a pupil checking the maths must find it correct).

---

## MESSAGE BUS CONTRACT (Phase 1 deliverable, used by all later phases)

- Channel name: `mbm_liveteach_v1` (namespaced — the estate is one origin; a generic name invites cross-page collisions).
- **All listeners use `bus.addEventListener('message', …)` — NEVER assign `bus.onmessage`.** Two fragments each overwrote `onmessage` and silently killed the other's handlers. Assigning onmessage anywhere in this codebase is a lint failure.
- Every message: `{ v: 1, type, payload }`. Unknown `type` or missing `v` is ignored silently.
- **State resync:** the projector, on load AND on receiving `HUD_HELLO`, broadcasts `PROJECTOR_STATE` (full current state: stage index, sim running/speed, blackout, hint/poll visibility, telestrator active). The HUD, on load AND on receiving `PROJECTOR_STATE`, reconciles all its indicators and its step counter. This kills the reload-desync class of bugs permanently.

## KEYBOARD REGISTRY (single source of truth — one keydown listener total per view)

One `registerKey(code, handler, description)` registry per view. Registering a code twice throws at boot — this is the guard against the KeyB-class collision. Final map (HUD view):

| Key | Action |
|---|---|
| Space | Sim pause/resume |
| 1 / 2 / 3 | Timers 1 / 3 / 5 min |
| 0 | Clear all overlays (timer, hint, poll) |
| H | Hint toggle (state tracked in HUD variables — never read from projector DOM copies) |
| P | Poll toggle (same state rule) |
| N | Cold-call: pick next |
| M | Cold-call: pass/bounce (P is taken by poll — the fragment's P binding is dead) |
| D | Telestrator draw toggle |
| C | Telestrator clear |
| 7 / 8 / 9 | RAG tally Red / Amber / Green |
| Q | QR share modal |
| B / Period | Blackout toggle (clicker) — **pulse is button-only now; B is blackout, nothing else** |
| PageUp/PageDown, ←/→ | Stage prev/next (clicker) |
| F5 | preventDefault + toast explaining fullscreen (see corrections) |
| Esc | Clear blackout, close topmost modal, blur inputs |

Guard clause: skip all hotkeys when focus is in INPUT/TEXTAREA/SELECT/contenteditable (the fragments missed the last two). The clicker keys (PageUp/PageDown/arrows/B/Period) are registered in **BOTH views**, so the clicker works whichever window has focus.

---

## CORRECTIONS REGISTRY (binding — each item gets a harness proof)

**From the worksheet engine (fragment 1):**
- W1. The line-art conversion strips the grid, leaving the printed figure with no measurement scale while the worksheet asks pupils to measure wavelength. Re-draw a calibrated grid (with a labelled scale bar in real units) onto the offscreen canvas before thresholding, or after as an overlay.
- W2. Fake units (rad/px sold as Hz, "λ = 314 px") — replace with an explicit model↔real-units mapping shown on the worksheet, or "model units" labelling. The v = f×λ task must be completable with correct numbers.
- W3. `$v = f \times \lambda$` prints literally — use plain text "v = f × λ".
- W4. Handwriting lines are CSS background gradients that most print engines strip — use bordered elements (e.g. repeated bottom-bordered divs) so lines survive any printer.
- W5. Remove the dead `threshold` parameter or actually use it.

**From the projector sync demo (fragment 2):**
- S1. Particle count capped (e.g. 150); pulses beyond the cap recycle the oldest. The O(n²) connection loop uses a spatial grid or a hard pair budget.
- S2. "Pause / Reset" mislabel — provide real Pause/Resume + separate Stop.
- S3. Speed buttons reflect the active speed (highlight follows state, synced via PROJECTOR_STATE).
- S4. simSpeed applied once (per-update only), not at particle construction too.
- S5. Projector visuals must survive a washed-out classroom projector: minimum contrast for lines/labels, and a "high-lumen" toggle that swaps to a light theme.

**From the clicker bridge (fragment 3):**
- C1. KeyB double-fire collision — resolved by the keyboard registry above.
- C2. **Remote fullscreen is impossible**: `requestFullscreen()` needs a user gesture in the receiving tab; a bus message is not one. Do not fake it. F5/the HUD button shows an honest toast: "Click the projector window once and press F11 / the fullscreen button there." Provide a fullscreen button ON the projector view (that one works — it's a real click).
- C3. Delete the unused `presentationKeys` array pattern; no dead code ships.
- C4. Dual-view clicker registration (above) so the remote survives focus loss.

**From the stage engine (fragment 4):**
- G1. **Spotlight must not erase content.** `destination-out` on the main canvas deletes the very pixels being highlighted. Implement dimming as an evenodd path (outer rect + inner ROI, single fill) or four surrounding rects, or a separate overlay canvas. Harness proof: pixel-sample inside the ROI shows sim content present.
- G2. Bidirectional step sync: the HUD's step counter is authoritative-FREE — it displays whatever `HUD_STAGE_SYNC`/`PROJECTOR_STATE` reports. No independent unbounded counter anywhere. Pressing Next at the last stage is a no-op on both sides immediately.
- G3. All spotlight/label coordinates in manifests are **normalised 0–1**, scaled at draw time. Manifests carry no pixel positions.
- G4. One animation loop. Overlays draw inside the existing loop; adding a second rAF loop is a lint failure.
- G5. Content accuracy: "doubling frequency" means exactly 2f in the manifest values; every quantitative claim in stage copy must be verified against the parameters.
- G6. Stage banner content set via safe DOM building (createElement/textContent), not innerHTML — manifests will eventually be authored per-lesson.
- G7. Manifests are external data: the engine loads `manifest.js`/JSON per lesson, with this wave lesson as the shipped exemplar. Design the schema so BUILD/GROW/LAUNCH variants of one lesson are three manifests on one engine.

**From the telestrator (fragment 5):**
- T1. Uses the bus contract (addEventListener) — the fragment's `bus.onmessage` assignment would have killed the timer/hint/poll handlers.
- T2. Message-type mismatch fixed: local projector strokes and remote HUD strokes converge on one stroke message type; define it once.
- T3. All stroke coordinates normalised 0–1 both directions (the fragment normalised remote strokes but drew local ones in raw pixels, and the mini-pad's 500×220 aspect distorts onto 16:9 — letterbox the mini-pad to the projector's aspect, which the projector reports in PROJECTOR_STATE).
- T4. Resize preserves strokes correctly (the getImageData backup loses data when the canvas grows; store strokes as a vector list and replay on resize).
- T5. Draw-mode ON optionally dims/freezes the sim (per the idea spec) — controlled, reversible, synced.

**From serializer/QR/picker (fragment 6):**
- U1. URL serializer: fix the string double-encode (`encodeURIComponent` stored into state, then URLSearchParams encodes again — tags arrive mangled). Store raw, encode once at write time.
- U2. `syncStateToURL` uses replaceState by default (no history spam); an explicit "bookmark this state" action uses pushState.
- U3. Schema `f` comment says "(Hz)" — units per W2 policy.
- Q1. **The QR engine is unverified hand-rolled crypto-adjacent code and its block structure is wrong for versions 4 and 6** (ECC-M v4/v6 require multiple interleaved Reed-Solomon blocks; the code computes one block — its own comments admit "2 blocks"/"4 blocks" while never interleaving). Codes above ~44 data bytes will not scan. Gate: add an independent decoder (e.g. jsQR) to the test harness and prove **round-trip decode** for representative URLs at every version you allow. Either implement proper block interleaving or hard-cap at version 3 and keep share-URLs short (the serializer's default-omission helps). A QR that hasn't been machine-decoded in CI does not ship. Also verify mask-0-only output still decodes at your allowed versions (no mask evaluation is spec-non-compliant but usually scannable — prove it, don't assume it).
- Q2. QR modal displays the URL as selectable text beneath the code (fallback when scanning fails).
- P1. Cold-call picker reads the roster from the **existing estate storage** found in Phase 0 — never the hardcoded `sampleRoster`, never a new key family without Matt's sign-off.
- P2. **No-immediate-repeat guard**: min-weight floor means a pupil can be drawn twice consecutively (~1%). In an SEMH AP that's not "attentiveness", it's a trigger. The just-called pupil's weight is 0 for exactly one round, then decay-recovery applies. Document the pedagogy in a code comment.
- P3. `renderProbabilities` builds rows with createElement/textContent (names via innerHTML template strings is a privacy/XSS landmine once real rosters load).
- P4. Absent pupils excluded from probability display; attendance toggle surfaced in the UI (the class exists in the fragment but has no UI).
- P5. Picker history stays in memory/localStorage; it is not broadcast.

**Classroom extras (idea list):**
- X1. RAG tally: 7/8/9 increment counters; optional anonymous histogram on the projector (counts only, never names); reset button; counts persist for the lesson only.
- X2. Silent bell: soft amber pulse on the projector; reduced-motion variant is a static banner.
- X3. TTS (speechSynthesis) + Web Audio earcons: OFF by default, single audio toggle, volumes modest, earcons ≤ 300 ms, no repeating alarms.
- X4. SVG sparkline copy: builds clean `<svg>` from recorded data arrays, `navigator.clipboard.writeText`, with a download fallback (clipboard write can be blocked on school machines).

---

## PHASES 1–8 (each: branch → commit → PR → green checks → merge)

**Phase 1 — Core shell.** Launcher + projector + HUD views, bus contract, state resync, particle cap (S1–S5), splash/exit, reduced-motion, theme/high-lumen toggle, keyboard registry with the Phase 1 keys (Space, timers, 0, H, P, Esc — with correct toggle state tracking). Gate: harness proves resync after projector reload; proves H/P toggle both directions; proves no `onmessage` assignment exists (grep gate).

**Phase 2 — Stage engine.** Manifest schema + loader, exemplar wave-lesson manifest (real units per W2), corrected spotlight pipeline (G1), normalised coords (G3), single-loop integration (G4), step sync (G2), stage banner (G6). Gate: pixel-sample proof inside ROI; step-clamp proof both sides; a units check that recomputes every quantitative stage claim from the manifest parameters.

**Phase 3 — Clicker bridge.** Registry-based clicker keys in both views, blackout curtain, honest fullscreen handling (C2), projector-side fullscreen button. Gate: simulated keydown proofs for every clicker key in both views; proof B fires exactly one action.

**Phase 4 — Telestrator.** Vector-stored strokes, normalised both directions, aspect-correct mini-pad, resize replay, D/C keys, colour/width sync. Gate: resize-preserves-strokes proof; stroke drawn on HUD renders at correct normalised position on a different-sized projector canvas.

**Phase 5 — URL serializer + QR.** Corrected serializer (U1–U3), copy-link, QR modal with the decode-round-trip CI gate (Q1) and URL fallback (Q2). Gate: jsQR (or equivalent) decodes generated QRs for short/medium/long state URLs; double-encode regression test on `tag`.

**Phase 6 — Cold-call picker.** Estate-roster integration (P1 — this is the phase most likely to STOP; if the roster census was ambiguous, ask Matt before writing), no-immediate-repeat (P2), safe rendering (P3), attendance UI (P4), N/M keys, Q2-dependent projector display. Gate: 10,000-draw simulation proving zero immediate repeats and long-run call-count balance within tolerance; proof no name string ever appears in a bus message payload when HUD-only mode is set.

**Phase 7 — Classroom extras.** RAG tally + histogram, silent bell, audio scaffolding (off-by-default proof), sparkline copy with fallback (X1–X4). Gate: audio state defaults proof; reduced-motion bell variant proof.

**Phase 8 — Worksheet engine.** Corrected capture (W1–W5), pulling live stage/params into the sheet, plus stage title + date + the pupil-fills-name header. Print CSS with bordered lines. Gate: automated render of the print layer showing grid + scale bar present in the exported image; no `$` in printed text.

**Phase 9 — Close.** `LIVETEACH_README.md` (what it is, the same-device constraint stated plainly, clicker setup steps, key map table), a phone-checkable live URL list for Matt, final ledger of SHAs per phase, and a one-paragraph handover note of anything deferred. PR, merge, report.

---

## STOP CONDITIONS

Stop and ask Matt rather than guessing when: (a) Q1 answer is no or unknown by end of Phase 0; (b) roster storage census is ambiguous or would require a new key family; (c) any check suite goes red on main; (d) the QR decode gate fails and fixing block interleaving would exceed the phase's scope — in that case ship version-capped and log the deferral; (e) anything requires touching `/hud.js`, `/theme.js`, or lesson decks.

## REPORTING

After each merge: phase, branch, merge SHA, gates passed (with the negative controls named), anything deferred. Plain language — Matt reads these on his phone.
