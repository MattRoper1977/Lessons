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

## 5a-SUPERSEDED. A withdrawn reading, struck rather than left to be re-cited

**Status: WITHDRAWN. Do not cite.** Order V6-PG §2.

An early arm of the passport work printed the word `OVERWRITTEN` and reported
that a V6 Apex Velodrome boot "replaced another game's passport". That reading
is struck for three reasons:

1. The record it seeded was **synthetic**, not written by any deployed writer.
2. It was **under-populated** — it carried no real profile, counters or badge
   sets, so "reset" and "rejected as unreadable" were indistinguishable.
3. It carried an **invalid `seasonId`** (`v4-s1`), which is not a season the
   estate issues, so the arm exercised the reader's error path rather than its
   merge path.

And it was wrong on its own terms: `lamport: 7` was in fact carried through that
boot, which the word `OVERWRITTEN` denies.

**What replaces it** is §5a below: the passport is seeded by booting the
**deployed Apex Kick**, so the record under test carries the estate's own schema
and node id; the seed is re-read intact at 2.5 s and again immediately before
navigation, with the arm aborting MEASUREMENT INVALID otherwise; and each arm is
run twice, with the build's own local record present and deleted.

**The rule it establishes, now binding on every future passport arm:** *a
passport arm may only be seeded from a record written by a deployed writer.* A
synthetic seed cannot distinguish a clobber from a rejection, which is the whole
question.

**Citation census, per §2.3.** `grep -n -F 'OVERWRITTEN'` returns no match in
`reports/` in this repository or in the Site estate, and no committed artefact
carries the withdrawn reading: the queue's first passport entry (`d80d7d9`)
already recorded the corrected arms. The reading existed only in a scratch probe
and in the session report that accompanied it. Nothing downstream depends on it,
so nothing required amendment beyond this marker.

---

## 5a-STRUCK. The passport-reset finding is WITHDRAWN — I made the same mistake twice

**Status: WITHDRAWN. Do not cite.** Order V6-PG §3.3.

§5a below reported that three of seven V6 builds — Marble, Apex Velodrome and
Grapple — reset `mbm_sports_passport_v4` on boot, discarding a child's name,
house, XP and badges. **That is not what was measured.**

The §5a arms seeded the passport by booting the deployed Apex Kick, which was
right, and then **marked it by hand**, which was not. One of those marks was
malformed:

```js
seeded.sets.badges.adds = ['first-lap'];
```

`sets.badges.adds` is an OR-set of `[tag, {id, clock, node}]` pairs, not an array
of strings. Measured directly against the runtime, mutating that record and
handing it back to `normalizePassport`:

```
THROW   sets.badges.adds = ['first-lap']  (bare string, hand-shaped)
        THREW: Invalid OR-set additions pair.
ok      counters.xp = [['other-node',340]] (well-formed pair)      accepted
ok      profile.name = {value,clock,node} (well-formed register)   accepted
ok      seasonId = 'v4-s1'                (invalid season)         accepted
ok      nodeId  = 'mbm-other-node-01'     (foreign node)           accepted
```

Only the hand-shaped badge array throws. Those three builds caught that throw and
installed a default — which is a **rejection of my malformed mark**, not a
clobber of a valid record. Every other hand mutation, including the foreign node
id, is accepted.

**This is the same failure the SUPERSEDED marker above already struck**, and the
rule that marker established — *a passport arm may only be seeded from a record
written by a deployed writer* — was necessary but not sufficient. It is now
extended, and the extension is enforced in code rather than in a report:

> **A passport arm may only be seeded from a record written by a deployed
> writer, AND marked through the runtime's own mutation API. No CRDT register,
> OR-set pair or counter may be hand-shaped by a probe.**

`tools/verify_sports_passport_contract.mjs` marks exclusively through
`MadeByMattV4Runtime.mutations.mutateProfile` and `.grantAward`, so the shape can
only be one the runtime itself produces. Under that instrument **no candidate
replaces a well-formed passport** — the C1′ column is green for all seven.

That column is not vacuous: the gate's own firing control installs a build with
an unconditional `defaultPassport()` write on boot, and C1′ reds it, naming every
field lost. A genuine clobber is still caught; there simply was not one.

What survives from §5a, re-derived under the corrected instrument, is in the
V6-PG contract table: `C1` (three builds do write the passport on boot, which is
a different and much smaller finding) and `C2` (six of seven default without
keeping a backup). The `mbm-default00000000` node id observation also survives,
but as a property of the *default* record those builds construct, not as
something they impose on a child's existing passport.

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

## 5d. V6-PG §6/§7 — the graft each held build needs (C2)

Recorded per §7.3: for every build that is HOLD rather than rejected, the one
clause it fails and the graft that would clear it. **No graft is landed here.**
§6.1's other half — the C1 fix — is not landable while C1 itself is in STOP: the
deployed `apexkick` reds C1 as worded and greens the proposed C1′, so the clause
has to be ruled before a build is changed to satisfy it.

The C2 reference implementation, cited per §0.6:

```
Apex_Curl_AAA_V6.html:1663    (loadPassport begins at 1659)
    catch(error){safeSet(PASSPORT_KEY+'_corrupt_backup',raw);return Runtime.defaultPassport();}
```

The graft is only byte-for-byte where the surrounding code already holds the
**raw string**. It does not everywhere, and that is the whole difficulty — a
build that parsed before it failed no longer has the thing C2 says to preserve.

| build | its defaulting path | does it still hold the raw string? | graft |
|---|---|---|---|
| **Grapple** `:5170` | `function loadPassport(){try{var raw=JSON.parse(localStorage.getItem(PASSPORT_KEY)\|\|'null');return RT.normalizePassport(raw);}catch(e){return RT.defaultPassport();}}` | **No** — `raw` is the *parsed* value, and the throw can come from `JSON.parse` itself | hoist the string: read `localStorage.getItem(PASSPORT_KEY)` into a `rawText` first, then parse. The catch then matches Apex Curl's line with `raw` → `rawText` |
| **Marble** `:5247` | identical to Grapple, character for character | **No** | identical graft |
| **Apex Velodrome** `:1692` | `try{var raw=readJson(PASSPORT_KEY);…}catch(_){passport=R.defaultPassport(state.nodeId);}` | **No** — `readJson` returns a parsed object and swallows its own parse error | same hoist, using `localStorage.getItem` rather than `readJson` for the backup argument |
| **Medevac Frontier** `:1719` | `…raw=localStorage.getItem(MV_RT.constants.PASSPORT_KEY);mvPassport=raw?MV_RT.normalizePassport(JSON.parse(raw)):MV_RT.defaultPassport(mvNode())}catch(e){mvPassport=MV_RT.defaultPassport(mvNode())}` | **Yes** — `raw` is already the string | Apex Curl's line grafts directly into the catch |
| **Wrecking Crew** `:5195` | `try{let i=localStorage.getItem(hn.constants.PASSPORT_KEY);bn=i?hn.normalizePassport(JSON.parse(i)):hn.defaultPassport(Jd())}catch{bn=hn.defaultPassport(Jd())}` | **Yes** — `i` is the string (minified name) | grafts directly, `raw` → `i` |
| **Neon Turf** | none — `grep -c -F 'PASSPORT_KEY'` returns 3, all of them a constant or a manifest entry | n/a | **no graft: C2 does not bind a build that never reads the passport** |

Neon Turf's row is the reason the gate's C2 clause was corrected mid-run. It
first failed Neon Turf for having no backup, when Neon Turf had discarded
nothing — it leaves a corrupt record exactly where it lies. The clause now tests
applicability first: if the corrupt record survives the boot, the build does not
default and C2 does not bind.

### Node id on a fresh install — C5's real surface

`Grapple:5170` and `Marble:5247` call `RT.defaultPassport()` **with no
argument**, which is what produces `mbm-default00000000`. That id is invisible to
any arm that seeds a passport first, because `normalizePassport` then keeps the
seed's node. It is only reachable on a fresh install, so the gate now carries a
fourth arm that boots each candidate into an empty origin and reads the id it
invents.

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
