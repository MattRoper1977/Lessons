# G1 — Glitch Clash: Fracture League — PARKED at the phase-0 boundary

**Status: PARKED, not started.** Branch `claude/g1-fracture-league` carries this
ledger and nothing else. No game file has been touched.

**Why parked.** AM9: *"an expansion merges ONLY completely green; anything less
parks its branch unmerged at a phase boundary with a named ledger."* The order
conditioned G1 on *clear budget after §1–§3*. §1–§3 consumed the sitting; the
budget for a G1 built to the ANNEX §6 bar — league layer, deterministic seed,
save migration on a real captured save, verifier extension, non-vacuity tampers,
playable at every phase boundary, photosensitivity + RM re-certified through
`verify_games_splash.mjs` — is not there. Starting the league layer and
abandoning it mid-phase is precisely the thin effort AM9 forbids.

Phase 0 of §6 is *"derive the CURRENT file first"*. That phase is COMPLETE and
its findings are below, so the next sitting starts from evidence rather than
from a description.

---

## Derived: the file as it actually stands

| | |
|---|---|
| path | `Games/Glitch_Clash.html` (Lessons repo — outside Progress pack scope, so Stage 3's zips stay valid) |
| size | 152,714 bytes · sha256 `ea4a26683f846f6e…` |
| title | `Glitch Clash — Card Battle \| Made by Matt` |
| script blocks | 2 — one inline (117,201 chars) and `<script defer src="/hud.js">` |
| act | ACT II present; "Keepers" present |
| `GAME_VERSION` | **absent** — there is no version-pinned identity anchor of that name in this game |

## Derived: the shipped rulings, located in the logic and quoted

**Turn-count arena rotation — CONFIRMED, and it must not move.**

```js
arenaFor(stageIdx, turn, rng){
  if(stageIdx < 3) return ARENAS[0];        // stages 1-3 always stable: teaching space
  const cycle = Math.floor((turn-1)/4);
  const pool = ARENAS.slice(1);
  return pool[(stageIdx + cycle) % pool.length];
}
```

Rotation is driven by `turn`, every 4 turns. **The locked teaching space is in
the code, not just in the brief**: stages 1–3 pin to `ARENAS[0]`, with that
comment. Both halves of the ruling are load-bearing.

**No wall clock touches rotation.** `Date.now()` appears 14 times in the inline
script; every occurrence is `runClock` (a run timer that pauses/resumes) or a
battle-start timestamp. None is within reach of arena, turn or stage selection —
checked by scanning the ±110 characters around every `Date.now()` for
arena/turn/stage/rotate. The ruling holds today and a league layer must not
introduce a clock-driven path.

**`arenaFor` already takes an `rng` argument.** There is a seam for a
deterministic run seed without restructuring the engine.

**The engine is already isolated** — its own comment reads
`/* ---------- Engine (pure, DOM-free) ---------- */`. An additive league layer
and its tests can sit against that boundary rather than against the DOM.

**Ride/Purge** (20 hits) and **Calm Mode** (26 hits) are both live in the logic.
Clash/damage vocabulary is dense (74 hits incl. `clashSkill`), so the scaled
clash is present; the exact scaling rule is NOT yet quoted here and must be
before it is preserved.

## THE FINDING THAT CHANGES THE SHAPE OF THE WORK

**There is no progress save key.** Every `localStorage` key in the file is a
setting:

```
gc_muted · gc_crt · gc_music · gc_theme      (+ "__t", a storage-availability probe)
```

ANNEX §6 requires *"save migration proven lossless on a real captured
pre-expansion save"*. **There is currently no pre-expansion progress save to
capture.** A league layer introducing run state would be creating the game's
first progress key, which is a different obligation from migrating one — and R6
of the annex (live keys never renamed) has nothing to bite on here yet.

This must be settled BEFORE building, not discovered halfway:

1. Confirm by playthrough that progress genuinely does not persist (the census
   above is static; a key written only deep into a run would not appear in a
   grep of quoted strings if it were built by concatenation).
2. If it truly does not persist, the "migration proof" for G1 becomes a
   **first-write proof**: a fresh install, a league run, a reload, and evidence
   that settings survived untouched and the new key is additive.
3. Name the new key to the house convention — `mbm_<game>_<thing>_v1` — which
   the existing `gc_*` keys do **not** follow. Renaming the existing four is
   forbidden (live keys, R6). So the game would carry two conventions, and that
   is a decision for Matt rather than a silent choice by me.

## Derived: what already exists to extend

`tools/glitchclash/` — 10 test files plus `run.sh`:

```
gc.test.js · gc-a11y.test.js · gc-cb.test.js · gc-clock.test.js
gc-endless.test.js · gc-fx.test.js · gc-hc.test.js · gc-mods.test.js
gc-music.test.js · gc-weekly.test.js
```

Not yet run in this sitting. §2.2 of the annex warns that some identity gates
pin a version prefix; `GAME_VERSION` is absent from this game, but the
suite has not been read for other pinned anchors. **Running all ten and
recording each result is the first action of the next sitting**, before any
edit — that is the annex's own rule, and it is not satisfied yet.

## Also derived, relevant to the league layer

- `Math.random()` — **15 calls** in the inline script. A deterministic run seed
  has to be separated from cosmetic RNG, so each of those 15 needs classifying
  as run-affecting or cosmetic. The word `seed` appears exactly **once**, so
  there is no existing seeding infrastructure to build on.
- `announce(` / `aria-live` — 21 hits. The announce contract exists and the
  league layer's recap must go through it rather than around it.

## The two register lessons from the hearth sitting bind here

1. **Tune and gate against the window a human watches.** A summary statistic
   over a long window hid a flicker that was almost a flat line over four
   seconds. Any league pacing, rival-intent telegraph or recap animation gets
   judged over the span a player actually sees, not over a full run.
2. **Drive related visual systems from one source.** The hearth read as an
   ornament because the fire lit nothing but itself. Fracture Cards, rival
   intent and arena state should answer each other from shared state rather than
   each animating privately.

## Not done, and not claimed

- The ten existing verifiers have **not** been run.
- The clash scaling rule is **not** quoted.
- No league design, no seed work, no save work, no gates, no frames.
- Photosensitivity and RM have **not** been re-certified for this game in this
  sitting.

**G2 is not started, per AM9.**
