# G1 — Glitch Clash: Fracture League — PARKED at the phase-0 boundary

**Status: PARKED at phase 0, second pass.** Branch `claude/g1-fracture-league`
carries this ledger and nothing else. No game file has been touched.

**This is the corrected ledger.** The first version got two derivations wrong and
they are recorded below rather than quietly fixed, because this document is the
next sitting's brief and a brief that has been silently repaired is worse than
one that shows its workings.

**Why still parked, after the resume.** Matt's key ruling landed and phase 0 is
now genuinely complete: the ten suites are green, both remaining rulings are
quoted, and the save architecture is understood. The build did not start for a
reason that is about evidence rather than time: **this sitting corrected its own
derivation twice**, and both errors pointed the same way — a null grep result
read as an absence. Designing a league layer, a deterministic seed and a save
migration on top of a document I have just had to correct twice is exactly the
thin effort AM9 forbids. The next sitting starts from a ledger that has been
checked against the file rather than against itself.

The original park reasoning also still holds. AM9: *"an expansion merges ONLY
completely green; anything less parks its branch unmerged at a phase boundary
with a named ledger."* The order conditioned G1 on *clear budget after §1–§3*.
§1–§3 consumed the sitting; the
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

## CORRECTION — THE PREVIOUS VERSION OF THIS LEDGER WAS WRONG, TWICE

Recorded loudly, because this ledger was going to be the next sitting's brief,
and the register's own rule is *measure the file, don't trust the brief*. Here
the brief was mine.

**WRONG 1 — "there is no progress save key". There is.**

```js
const GAME_VERSION = "2.0.0";
const SAVE_VERSION = 3;
const DEFAULT_SAVE = ()=>({
  v:SAVE_VERSION, owned:[...STARTERS], dups:{}, team:[...STARTERS],
  cleared:[], xp:0, stickers:{}, settings:{calm:false,motion:"auto",hc:false,cb:false},
  dailyDone:"", weeklyDone:"", tutorialDone:false, seen:{}, stats:{wins:0, clashWins:0}
});
function save(){ try{ store().setItem("glitchclash_save", JSON.stringify(SV)); }catch(e){} }
```

The key is **`glitchclash_save`** and it holds the whole progress object. The
census missed it for a dull reason worth naming: `save()` writes through
`store()`, not through a literal `localStorage.setItem(...)`, so a grep for
`localStorage\.\w+Item\(` found only the four settings keys and the storage
probe. The separate grep for quoted strings containing gc/glitch/clash returned
CSS class names and I read a null result as an absence.

`store()` also falls back to an in-memory object when localStorage throws, so
the game already degrades safely in a blocked-storage browser.

**WRONG 2 — "GAME_VERSION is absent". It is `"2.0.0"`.**

My grep was `GAME_VERSION\s*=\s*'` and the file uses double quotes. An absence
claimed from a quoting artefact.

**What the corrections change.**

- There IS a real pre-expansion save to capture, so ANNEX §6's *"save migration
  proven lossless on a real captured pre-expansion save"* is satisfiable exactly
  as written. The "first-write proof instead" reasoning in the previous version
  rested on a false premise and is withdrawn.
- Matt's ruling still stands and is now more precise: the new league progress key
  is **`mbm_glitchclash_league_v1`**, additive alongside `glitchclash_save`,
  which is NOT renamed (R6). The four `gc_*` settings keys stay verbatim.
- **The dual convention is deliberate and is recorded here as such.** After the
  league layer the game carries three key shapes: `glitchclash_save` (progress,
  unprefixed, live since v1), `gc_muted` / `gc_crt` / `gc_music` / `gc_theme`
  (settings, live), and `mbm_glitchclash_league_v1` (new, house convention).
  Renaming any of the first two is forbidden while they hold real players'
  progress, so the game is a mixed-convention game on purpose rather than by
  neglect.

**Derived negative, and it is good news:** no suite pins `GAME_VERSION` or
`SAVE_VERSION`. Three suites reference `glitchclash_save` by name
(`gc.test.js`, `gc-a11y.test.js`, `gc-endless.test.js`) and that key is not
moving. So the ANNEX §2.2 trip hazard — a version-pinned identity anchor that
breaks on a bump — **does not apply to this game**, and nothing needs widening.

## Derived: the two remaining rulings, now quoted

**The scaled clash.** Timing feeds a `skill` in 0..1 from the ring, and it moves
both the balance and the payoff:

```js
// skill (0..1) from the timing ring shifts the power balance up to +/-35%
const skillMult = 0.65 + skill*0.7;
const pPow = p.atk*pSpec.mult*skillMult + p.en*0.4 + rng()*8;
...
d = Math.max(2, Math.round(d*(0.7+skill*0.6)));   // timing scales the payoff
...
d = Math.max(2, Math.round(d*(1.3-skill*0.5)));   // good timing softens a lost clash
```

Ring tiers: PERFECT `1.0` · GOOD `0.75` · CLOSE `0.4` · MISSED `0.12`. Note the
losing branch — good timing *softens a lost clash* rather than only rewarding a
won one. A league layer must not flatten that.

**Calm Mode widens the window, and does not play for you.**

```js
const calm = SV.settings.calm || document.body.classList.contains("reduce-motion");
// Calm Mode: half speed, much wider window — slower, not automatic
const period   = calm ? 2600 : 1300;
const zoneDeg  = calm ? 96   : 44;
```

Reduced motion turns Calm Mode ON by itself — the two are already wired
together, which is the shared-source pattern the hearth sitting argued for.

**One thing a deterministic run seed has to reach:** `zoneStart = 40 +
Math.random()*240` places the ring's target arc. That is not cosmetic — it sets
where the player must tap — so it belongs to the run seed, not to cosmetic RNG.

## Derived: what already exists to extend

## Derived: what already exists to extend

`tools/glitchclash/` — 10 test files plus `run.sh`:

```
gc.test.js · gc-a11y.test.js · gc-cb.test.js · gc-clock.test.js
gc-endless.test.js · gc-fx.test.js · gc-hc.test.js · gc-mods.test.js
gc-music.test.js · gc-weekly.test.js
```

**All ten now RUN and PASSING** — the annex's rule (run every dedicated verifier
before editing anything) is satisfied, and the result is the baseline any league
work has to keep:

```
gc          ALL GLITCH CLASH CHECKS PASSED     gc-music    MENU MUSIC VERIFIED
gc-endless  ENDLESS RUN VERIFIED               gc-cb       COLOURBLIND PALETTE VERIFIED
gc-mods     RUN MODIFIERS VERIFIED             gc-hc       HIGH CONTRAST VERIFIED
gc-clock    TIME ATTACK VERIFIED               gc-a11y     ACCESSIBILITY CHECKS PASSED
gc-weekly   WEEKLY GAUNTLET VERIFIED
ALL GLITCH CLASH SUITES PASSED
```

The game already ships Endless, Run Modifiers, Time Attack and a Weekly
Gauntlet. **The league layer is additive to those, not a replacement**, and the
next sitting should read how they compose before designing a route on top.

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

- ~~The ten existing verifiers have not been run.~~ **RUN — all ten pass at
  this baseline** (`gc`, `gc-endless`, `gc-mods`, `gc-clock`, `gc-weekly`,
  `gc-fx`, `gc-music`, `gc-cb`, `gc-hc`, `gc-a11y`): *ALL GLITCH CLASH SUITES
  PASSED*. That is the green baseline the league layer must protect.
- ~~The clash scaling rule is not quoted.~~ **Quoted above.**
- No league design, no seed work, no save work, no gates, no frames.
- Photosensitivity and RM have **not** been re-certified for this game in this
  sitting.

**G2 is not started, per AM9.**
