# Deferred verification queue — 2026-08-30

Written under Order SOLO-1 §S5, during the subagent quota outage. Everything
here is work that could **not** be verified solo, or was verified only under an
instrument weaker than the claim needs. **This is the first work when the quota
resets on Sep 1 at 12:00 UTC. If the reset lands mid-run, this queue is worked
before any new audit is opened.**

Ordered by consequence. Each entry names the exact command a verifier should
run and the observation that would refute the finding.

Filed in this repository rather than the Site estate so that Site PR #226 keeps
the scope its own description states. The subjects are mostly Site subjects.

---

## 0. Standing record — what was NOT measured

Per §0.2, these produced **no evidence at all** and nothing downstream may cite
them:

| audit | status |
|---|---|
| Voxel Builder Zoom — 5 verification agents | **MEASUREMENT INVALID** (all died) |
| Neon Turf AAA V6 | **NOT RUN** |
| Apex Curl AAA V6 | **NOT RUN** |
| Apex Velodrome AAA V6 | **NOT RUN** |
| Medevac Frontier AAA V6 | **NOT RUN** |
| Grapple AAA V6 | **NOT RUN** |
| Marble AAA V6 | **NOT RUN** |
| Wrecking Crew AAA V6 | **NOT RUN** |

No sentence of the form "the V6 audit found no issues" is available, and none
may be written.

---

## 1. WebKit's pointer-lock return shape — UNPINNED in a shipped gate

**Consequence: a live gate is running with one engine's contract unmeasured.**

`tools/verify_v4_games_deployment.mjs` pins `EXPECTED_LOCK_SHAPE` per engine.
Chromium and Firefox are pinned from CI measurement. WebKit is `null` — the run
that would have measured it aborted at Firefox's assert before WebKit's leg. An
unpinned engine reports `UNPINNED`, never `ok`, and `'other'` still reds, so the
gate is not blind; but the value is not yet a contract.

- **Run:** the V4 browser matrix through to the WebKit leg and read
  `INFO webkit pointer-lock return shape — webkit: '<shape>' — UNPINNED`.
- **Then:** set `webkit` to that observed value in `EXPECTED_LOCK_SHAPE`.
- **Refuted by:** WebKit reporting `'other'` — that would be a real product or
  platform finding, not a value to pin.

Do **not** pin WebKit from documentation. The Firefox entry was originally
`'undefined'` on exactly that basis and CI refuted it on the first run
(`RETURN_SHAPE_DRIFT: firefox: expected 'undefined', observed 'thenable'`,
run 33329658992, head `de0e4770`).

---

## 2. Voxel Builder Zoom — blocker 2's *permanence*

**Consequence: on a phone, one-finger look would die for the rest of a session.**

The adoption step is CONFIRMED: at the canvas `touchend`, `endLook` adopts
`ev.touches[0]`, whose target is `#d-left`, as the new `lookId`. Measured
through a **synthetic** `TouchEvent` dispatch, because CDP
`Input.dispatchTouchEvent` cannot express a partial release (`touchEnd` takes no
remaining points). What is **not** measured end-to-end is the consequence — that
the adopted touch's `touchend` never reaches the canvas listener, so `lookId`
stays pinned to it permanently.

- **Run:** the sequence on a real touch device, or under a driver that supports
  partial multi-touch release: hold `#d-left`, land a finger on the canvas, lift
  the canvas finger, release `#d-left`, then attempt a one-finger canvas look.
- **Observation that would refute it:** the camera yaw changes on that final
  drag.
- **Instrument warning:** canvas pixels are **not** a valid observable here. An
  idle control proves the canvas repaints with no input at all, so a pixel diff
  reads "camera moved" unconditionally. An earlier run of this probe was
  discarded for exactly that reason. Use a yaw read, not a screenshot.

---

## 3. Voxel Builder Zoom — the four dimensions not re-measured solo

Six dimensions were named: *"the pinch implementation, boot/render errors,
accessibility, saves/migration, offline+performance, and code quality"*. Pinch
was re-measured solo (entries 2 and 4). The rest carry findings from agents that
were **never adversarially verified**, so none of them may drive an edit.

Highest-consequence unverified claims, each needing its own positive control
first:

| claim | command | refuted by |
|---|---|---|
| A malformed save throws out of async `startGame()` and hard-locks on "Generating world…" with Start disabled | seed `localStorage` with a malformed save, boot, assert `#start` becomes enabled again | Start re-enabling, or a visible recovery path |
| "New world" does not erase the world when a legacy v1 save exists; the world returns byte-identical next boot | seed a v1 save, press New world, reboot, compare the serialised world by value | a differing world on the second boot |
| The start/pause overlay is not modal — 21 tab stops land on controls painted behind it | rendered tab-cycle census at 390×844 | every tab stop resolving to a control inside the overlay |
| The only exit link renders 130.6 × 12 CSS px against the estate's 44×44 floor | `getBoundingClientRect()` census of every exit affordance | a ≥44×44 exit affordance existing |
| At 390×844 the "← Made by Matt · Arcade" link paints over the "Builder Zoom changelog & limits" disclosure | rendered overlap census of the two boxes | disjoint rects |

---

## 4. Voxel Builder Zoom — confirmed defects awaiting a repair decision

CONFIRMED by code trace against the upload
(`3b02a032-Voxel_Frontier_Beaconfall_V4_Builder_Zoom.html`, 717,573 B,
sha256 `f06172c8464b1394fdd2db1f97730c8d63aaf0e66e7a13c6112905c9af6b5f45`).
These are not queued for *verification* — they are queued for a repair decision,
and are listed here so the queue is the single place to look.

| line | defect |
|---|---|
| 1869 | `ev.touches.length>=2` is the document-wide contact list. Measured: with `#d-left` held, the canvas `touchstart` sees `ev.touches=2, ev.targetTouches=1`, so a d-pad contact plus a look finger enters the pinch branch. `ev.targetTouches` is the contact list this test wants. |
| 1898 | `setBuilderZoom(zoomFov,true,true)` at gesture end announces and **persists** even when the value never changed — a two-finger tap writes `localStorage` and fires an aria-live announcement for a zoom that did not happen. |
| 503–506 | `Number.isFinite(Number(prefs.zoomFov))` is true for `null` (`Number(null) === 0`), so a null pref clamps to `MIN_BUILDER_FOV` (30) and the game boots at **maximum** builder zoom instead of `DEFAULT_FOV`. |
| 1795 | The shift/alt/ctrl/meta+wheel path calls `setBuilderZoom(..., true, true)` on **every wheel tick**, writing storage and announcing each time, where the touch path correctly defers both to gesture end. |
| 1794 | `e.ctrlKey` is included in the zoom branch and `preventDefault()`ed while pointer-locked, so browser zoom is suppressed during play. The estate's contract is at `tools/verify_v4_games_deployment.mjs:162` (`browser zoom is blocked`), which tests only the viewport meta — the upload's meta is clean, so **this gate cannot see this defect**. Widening it is a proposal, not a repair. |
| 1888 / absent | The upload drops `<script defer src="/hud.js"></script>`, which is where the deployed build gets its accessible way out. Present at `voxel/index.html:1888` on main; no match in the upload. |
| 2013 | HUD identity is `Beaconfall · Builder Zoom`; the V4 gate waits on the literal `Beaconfall · V4 M2` (main: `voxel/index.html:1877`). |

**The build is not deployable as it stands.**

---

## 5. The seven AAA V6 games — gates not yet run

All seven parse. `node --check` over every inline `<script>` block, with a
deliberate syntax-error control proving the checker rejects a known-bad block on
each file:

| upload | bytes | sha256 (16) | inline blocks | syntax failures |
|---|---:|---|---:|---:|
| Neon Turf | 218,081 | `3429e5413ce15217` | 3 | 0 |
| Apex Curl | 254,895 | `7c90dcaebc653775` | 8 | 0 |
| Apex Velodrome | 261,735 | `934545692f3121d1` | 8 | 0 |
| Medevac Frontier | 457,204 | `16747cde6d4933a7` | 4 | 0 |
| Grapple | 649,930 | `484741cbb1c6e1d8` | 5 | 0 |
| Marble | 660,686 | `2918990e96d994d9` | 5 | 0 |
| Wrecking Crew | 866,156 | `8a89f58419eb9483` | 9 | 0 |

Parsing is not passing. **None of the estate gates have been run against any of
them**, and none is NOT STARTED-with-a-verdict: they are simply NOT STARTED.
Current deployed counterparts, for the byte delta each replacement implies:

| game | repo | current bytes | current sha256 (16) |
|---|---|---:|---|
| Neon Turf | Site `/neonturf/` | 120,495 | `b6b6141326548e32` |
| Apex Curl | Site `/apexcurl/` | 111,203 | `19f39c3440e7a032` |
| Apex Velodrome | Site `/apexvelodrome/` | 130,192 | `047836e5adc852de` |
| Medevac Frontier | Site `/medevac/` | 355,783 | `b84dc4b7d7c7edc7` |
| Grapple | Lessons `Games/Grapple.html` | 536,363 | `958fd957c3debb2f` |
| Marble | Lessons `Games/Marble.html` | 538,576 | `7ac1f43e52d31f3a` |
| Wrecking Crew | Lessons `Games/Wrecking_Crew.html` | 188,408 | `f4067cc3b6064ce3` |

Per §S4.2, each still needs, one at a time and atomically: its **real** estate
gates (splash, inline exit, hud coverage, sports rail, flash census where it
applies — never a bespoke substitute where an estate verifier exists), plus the
three mandatory traps — dual-canvas CP4b with the 2D canvas named explicitly and
the probe positive-controlled before any blank is trusted; any shared-save or
passport write measured **by value** on a seeded save, never read from the code
path; and touch-target and zoom claims taken as rendered censuses, not greps.

Running order, cheapest-to-prove first, by bytes: Neon Turf, Apex Curl, Apex
Velodrome, Medevac Frontier, Grapple, Marble, Wrecking Crew.

---

## 5a. The shared sports passport — three V6 builds reset it (CONFIRMED)

**Consequence: a child who has played any sports game loses their name, house,
XP and badges the moment one of these three boots. This is the most serious
finding of the session.**

`mbm_sports_passport_v4` is a live cross-game estate key. On the deployed tree
its writers are four games — `apexkick`, `auroralinks`, `houseolympiad`,
`olympics`. All seven V6 uploads reference it.

Measured by value, not read from the code path. The passport is seeded by
booting the **deployed Apex Kick**, so the record under test is the estate's own
schema and node id, not a synthetic one; it is then marked
(`name=Robin`, `xp=340`, `badges=['first-lap']`), re-read to prove the mark
survived, and each V6 build is booted in that same origin:

| V6 upload | shared passport after its boot |
|---|---|
| Neon Turf | preserved |
| Medevac Frontier | preserved |
| Wrecking Crew | preserved |
| Apex Curl | preserved |
| **Marble** | **RESET** — `name=Player`, `xp=[["mbm-default00000000",0]]`, `badges=[]` |
| **Apex Velodrome** | **RESET** — `name=Player`, `xp=[["mbm-velo-…",0]]`, `badges=[]` |
| **Grapple** | **RESET** — `name=Player`, `xp=[["mbm-default00000000",0]]`, `badges=[]` |

Alternatives ruled out, each with its own arm:

- *A deferred write from the first boot overwrote the seed.* No — the seed was
  re-read intact 2.5 s after writing and immediately before navigation, and the
  arm aborts as MEASUREMENT INVALID if it is not.
- *The V6 build rebuilds the passport only when its own local record exists.*
  No — the reset happens identically with `mbm_apex_velodrome_v4` present and
  with it deleted.
- *The V6 build rejected an unreadable synthetic record.* No — the decisive run
  uses a passport written by a deployed estate game, in the estate's own schema.

Secondary observation: Marble and Grapple write node id `mbm-default00000000`,
a placeholder rather than a per-install identity. Every install sharing one node
id defeats the per-node clocks the passport's counters are built on.

- **Run:** the table above, per game, on any candidate build.
- **Refuted by:** `name=Robin`, `xp` containing 340, and `badges` containing
  `first-lap` all surviving the boot.

**None of Marble, Apex Velodrome or Grapple may be deployed until this is
resolved.**

---

## 5b. The Apex storage-key assertion does not measure what its label says

**Consequence: the gate's green on one V6 build and red on another are both
artefacts of a prefix, not measurements of the games.**

`tools/apex_rc_gate.mjs:90` collects keys from the SOURCE by the regex
`['"]((?:apex)_[a-z0-9_]+)['"]`, then asserts "touches exactly the declared
storage keys". Two consequences, both observed:

- **Blind.** Apex Curl V6 passed 17/17 including that assertion, yet a
  fresh-context runtime census shows it writes `mbm_apex_curl_v4` and
  `mbm_apex_curl_v6_data` at load, while the deployed build writes nothing at
  all. Neither key begins `apex_`, so the regex cannot see them.
- **Red on correct behaviour.** Apex Velodrome V6 failed that one assertion out
  of 17 for three literals, none of which is an undeclared write:
  `apex_velodrome_rc_v1` and `apex_velodrome_rc_stars_v1` are its
  `LEGACY_STORAGE` / `LEGACY_STARSTORE` — old keys read for migration — and
  `apex_velodrome_aaa_v4_` is an export filename prefix
  (`…telemetry.csv`, `…replay_diff.csv`), the exact category the filter on the
  next line exists to exclude and whose pattern `_v\d_\d_rc\d_$` does not match.

**Not repaired.** Under §0.5 a gate is not adjusted to make something pass, even
when the old value looks wrong. This is written up as a proposal for Matt: a
runtime key census in a fresh context would measure what the label claims, where
a source regex cannot.

Positive control for the gate itself, so its greens are not vacuous: a
one-character mutation inside Apex Curl's stamped exit region (`/games/` →
`/gomes/`) takes it from 17/17 to 13/17, reddening the byte-identity assertion
and all three rendered exit-control assertions.

---

## 5c. Neon Turf V6 drops hud.js (CONFIRMED)

```
[FAIL] /neonturf/ is declared wired and carries no hud.js script tag at all
       …31 claim(s) hold, 1 do not
```
Positive control, same gate and tree with the deployed file restored: **32 hold,
0 do not**. Provenance: `neonturf/index.html:1206` on main carries
`<script defer src="/hud.js"></script>`; the upload has no match. The
inline-exit gate passes with the upload in place (973 passed, 0 failed, all six
of its own controls firing), so it is the wired HUD way out that is missing, not
every exit affordance. Same defect class as the Voxel Builder Zoom upload.

---

## 6. CyberPulse #218 — a diagnosed product defect, unrepaired

CyberPulse attempts WebGL2 without detecting software rasterisation, which hangs
the estate harnesses on runners without hardware GL.

- **Run:** the CyberPulse browser matrix on a SwiftShader runner and capture
  where it stalls.
- **Refuted by:** the same matrix completing on a software rasteriser without a
  hang.

---

## 7. C1 — a standing condition, not a finding

Recorded under Order SOLO-1C. The `smokeVoxel` pointer-lock wait could not be
reached by a synthetic never-decides case; everything upstream reds first, which
is the fail-closed proof. **If any upstream bounded wait is ever loosened, this
wait's end-to-end reachability becomes untested and must be re-proven before that
change lands.**
