# Release ledger — combined order v2, 16 August 2026

Four independent targets, one runner, one shared discipline. Each has its own
branch and its own PR; none of them shares code with another.

| | Target | Verdict | PR |
|---|---|---|---|
| **A** | Scrap Core: Expedition SIGNATURE v10 | **P0 resolved, P1–P5 not attempted** | [#117](https://github.com/MattRoper1977/Lessons/pull/117) — open |
| **B** | Class of Ashes: Zero Period PRO v1.0.0 | **Patched and parked** | [#118](https://github.com/MattRoper1977/Lessons/pull/118) — open, do not merge |
| **C** | Virtual Chemistry Lab PRO Spatial v0.3 | **Both merge-blockers green; awaiting the V7 route** | [#116](https://github.com/MattRoper1977/Lessons/pull/116) — open |
| **D** | R-Wilton-4 | **Merged** | [#115](https://github.com/MattRoper1977/Lessons/pull/115) — merged |

All three payload baselines reproduced **exactly** before any work started:

| payload | sha256 | size | checksums |
|---|---|---|---|
| `Scrap_Core_Expedition_SIGNATURE_v10.html` | `33f1260b…97608` | 217,715 B / 3,121 lines | 15/15 verify |
| `Class_of_Ashes_Zero_Period_PRO.html` | `a04c41da…4896f` | 179,249 B / 604 lines | 15/15 verify |
| `Virtual_Chemistry_Lab_PRO_Spatial_v0.3.html` | `bd0e7596…6cdef` | 173,102 B / 1,646 lines | n/a |
| prototype (reference only) | `24fc1443…6348` | 59,316 B | — |

---

## §S2 — the evidence rule, applied to this pass

Every claim below names the artefact that proves it, and every artefact
discriminates. Where a check would have passed on a broken build, it was
rewritten or deleted. Six such were caught **in this pass's own gates**:

| what was wrong with the check | how it was caught |
|---|---|
| a reduced-motion seed appended after `</html>`, inert text, never executed once | matched pair measured `body.calm` on both trees and found it false on both |
| storage-call records kept in a page global that `location.reload()` destroyed along with the evidence | the `removeItem` limb recorded nothing on a build that definitely removed |
| three localStorage removals masking each other, so one control watched none of them individually | removal matrix: dropping T1, T2 or T3 changed no verdict |
| a frozen-region assertion whose pattern no longer matched, reporting MOVED with nothing moved | the assertion said REGION NOT FOUND rather than passing |
| a rehydrate step that protected nothing `loadHash` already did | removal matrix reported it UNWATCHED; the step was deleted, not given a control |
| a control that only went red because the page threw | removal matrix showed a crash, not a change; the two transforms were merged into one |

Two claims in the incoming reports were checked and are **true but unproven by
their own artefacts** — the Class of Ashes touch-fire response (`shots: 0` in
their summary) and the briefing-map pixel proof (two near-black pixels compared).
Neither is a defect; both are recorded so the artefacts are not cited as proof.

---

## Target D — merged

Two rulings issued, both landed, both one swap line from being undone.

| item | what changed | artefact | red/green | planted failure seen red |
|---|---|---|---|---|
| Ruling A | C21 added as the taught fuel-oil feed, in all three feed lists | `W-R-C21`, `W-ID24`, `W-ID3` | red→green | yes (drop T8a/b/c) |
| Ruling A | C24 stays selectable, stays undistillable, stays declared | `W-R-C24`, `W-DESIGN` | UNREACHABLE, declared | yes (drop T8a) |
| Ruling A | the refusal message teaches, in two sentences | `T10a`, `T10b` | red→green | yes (drop T10) |
| Ruling B | five tray temperatures corrected | `W-DIAG` 4/5 → **5/5** | red→green | yes (drop T11) |
| Ruling B | the marker-vs-readout limb, across all feeds | `W-DIAG-MARK` 5/5 → **6/6** | already consistent | yes (drop T7) |
| Ruling B | the caption | `T12` | red→green | yes (drop T12) |

**Headline: release teaches 1 of its 5 selectable feeds into the right fraction;
the merged build teaches 6 of 7, C24 declared unreachable by design.**

Sixteen transforms; drop all sixteen → release byte for byte; drop each one → a
verdict changes. Mission transport green in all four release/staging splits,
both directions.

**Recorded and left:** 22 of the 38 pupil-facing inputs have no accessible name.
Identical on release. `staging/` is wired to no route; merging did not deploy it.

---

## Target C — both merge-blockers green

| item | what changed | artefact | red/green | planted failure |
|---|---|---|---|---|
| **V1** | sequencing predicate is order-aware; the model untouched | `V1 {chloride,bromide,iodide,sulfate} reversed` | 4 red → 4 green | yes (drop X1a/X1b/X1c) |
| **V1** | correct order keeps its clean positive | `V1 … correct` | green both sides, asserted | — |
| **V2** | `pupil` out of the serialiser | `V2a` | red→green | yes (drop X2a) |
| **V2** | name still in print and Export JSON | `V2b` | asserted; a first cut broke it | yes (drop X2d) |
| **V2** | both captions describe what the link carries | `V2d`, `V2e` | red→green | yes (drop X2b/X2c) |
| **V3** | 3,814 → **26** fresh; 8,093 → **1,485** on a realistic session | `V3`, `V3-detail` | red→green | yes (drop X3a/X3c) |
| **V3** | round-trip and legacy links still work | `V3-roundtrip`, `V3-legacy` | asserted | yes (drop X3d/X3e) |
| **V4** | `.drop-pill` rule; gap 0 px → **6 px** at 390 and 1440 | `V4 @390px`, `V4 @1440px` | red→green | yes (drop X4) |
| **V5** | 6 of 8 negated near-misses marked correct → **0** | `V5`, `V5b` | red→green | yes (drop X5a/X5b) |
| **V6.4** | reduced motion seeded from the OS | `V6.4a`, `V6.4b` | red→green | yes (drop X6c) |
| **V6.5** | **17** unnamed controls across five benches → **0** | `V6.5` | red→green | yes (drop X6d*) |
| **V0** | the frozen engine, pH model, mystery hash, 14 observation strings | `U2`, `U2s ×14` | unchanged | — |

**Not done:** splash, way home, `<noscript>`, `og:`, `canonical` — they depend on
the **V7 route**, which is Matt's ruling.

---

## Target B — patched and parked

| item | what changed | artefact | red/green | planted failure |
|---|---|---|---|---|
| **C1** | shape guards inside both normalizers | `C1` — 21 cases, release fails 2 | red→green | yes (drop Y1a/Y1b) |
| **C2** | autostart block removed | `C2` — 5 parameter sets, release fails 5 | red→green | yes (drop Y2) |
| **C3** | `window.__COA_QA` removed in full | `C3a`, `C3b` | red→green | yes (drop Y3) |
| **C3** | the game still deploys, driven through the real UI | `C3c` | asserted | — |
| **C4** | clearance derived from the drawn HUD | `C4` — 6 of 8 overlap → **0 of 8** | red→green | yes (drop Y4a–d) |
| **C5.4** | viewport no longer blocks pinch zoom | `C5.4` | red→green | yes (drop Y5d) |
| **C5.5** | reduced motion from the OS, user choice still wins | `C5.5a`, `C5.5b` | red→green | yes (drop Y5e1) |
| **C0** | the fence | `C0` — shelf, both audience pages, curation renderer | ASSERTED | it exists to go red if anyone adds the route |

**Deliberately not done:** the storage-key rename (`COA-TRANSCRIPT-1` may be in
the wild and atomic migration was not proven), `canonical`, and every conformance
item that needs the shelf conventions. **Mode names and in-game copy untouched.**

---

## Target A — P0 resolved

| item | what changed | artefact | result |
|---|---|---|---|
| **P0.1** | 23 routes measured in a browser; every same-origin request recorded | `qa/P0_estate_injection_census.json` | 12/23 request `/hud.js`, **0** request `/theme.js`, **11 request nothing**, **no game ships a CSP** |
| **P0.2** | **the CSP is unchanged — no `'self'` on any directive** | `P0.2` | PASS |
| **P0.3** | the inline exit region stamped by the estate's own generator | `P0.3a` | PASS — 11 targets, 0 divergent |
| **P0.3** | zero CSP violations at boot and through one live descent | `P0.3b`, `P0.3e` | PASS |
| **P0.3** | the region **executed** — side effect, not tag | `P0.3c` | PASS |
| **P0.3** | canvas painting after the descent | `P0.3f` | PASS — 120,000 lit pixels |
| **P0.3g** | **PLANTED FAILURE: `<script src="/hud.js">` is BLOCKED** | `script-src-elem`, `errorText: csp` | **seen red** |
| **P0.3h** | and removing it restores a clean run | `P0.3h` | PASS |

**P1–P5 not attempted.** Placement is the larger half and half-proving it would
be worse than not starting.

---

## Estate red count

**Before: unchanged. After: unchanged.** No target added a red, and no target
fixed one that was already there — the three pre-existing reds
(`render_audience_homepages --check`, `build_mbm_search_index --check`,
`verify_design_inheritance`) were explicitly out of scope and are untouched.

The one red this pass *records* is Target D's 22-of-38 unnamed inputs. It is
pre-existing, identical on the release build, and reported through a distinct
exit code (3) so it cannot be mistaken for a failure this work caused.

---

## Owed to a human

1. **The Class of Ashes content decision.** A school under attack; PROTOCOL
   LOCKDOWN; an SEMH room. Nothing proceeds to placement without it.
2. **The Chemistry Lab route (V7)** — which estate it belongs to and what links
   to it. Both merge-blockers are green and waiting on this alone.
3. **Scrap Core P1–P5**, if placement is still wanted this week.
4. **Play all three on the phone.** Scrap Core: one descent to a titan. Class of
   Ashes: one Operation period plus the landscape subtitle band. Chemistry Lab:
   the microscale bench in landscape, and Share on a real link.
5. **Eyes on the Scrap Core card copy and hue** — not written, not drafted.
6. **Grades and records, decided once across the batch.** Scrap Core's Field
   Report, Class of Ashes' Academic Transcript and the Chemistry Lab's named
   practical record now put three graded, named artefacts in front of the same
   pupils. One decision, not three.
7. **The fun question**, for all of them.
