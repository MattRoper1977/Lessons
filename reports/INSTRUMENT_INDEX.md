# Instrument Index

Every test/gate script in the tree, with what it claims and whether it has been
audited. Written for the instrument-close pass, 2026-08-01.

**No script is omitted for being obviously fine.** "Obviously fine" is what the
print tautology looked like: `return a ? getComputedStyle(a).display !== 'none' || true : true`
— `X || true`, which passed every deck in every state for as long as it existed.

Re-derive this list rather than trust it:

```sh
git ls-files '*.js' '*.mjs' '*.sh' '*.py' \
  | xargs grep -lE 'process\.exit|sys\.exit|assert|SystemExit'
```

## The standing requirement

Every instrument must assert a **count, a value, or a set invariance** — never
merely the absence of a thrown exception. An instrument that exits 0 having
matched nothing is the cheapest possible false green.

Recorded as INSTRUMENTS.md standing rule 13 (timing) and REGISTER R-E22 (gate
shape).

## Totals

| | count |
|---|---|
| instruments | 41 |
| — AUDITED-SOUND | 9 |
| — AUDITED-FLAGGED | 5 |
| — NOT-YET-AUDITED | 27 |
| generators (produce artefacts; not instruments) | 19 |
| engines (runtime libraries) | 2 |
| **total scripts accounted for** | **62** |

## Instruments

| script | lang | exits non-zero | asserts a count/value | status | note |
|---|---|---|---|---|---|
| `LundyLoop/tools/classify.py` | python | no | yes | **AUDITED-FLAGGED** | Does NOT use the preflight guard, unlike 8 of its 12 siblings. Not shown broken; flagged because a false zero here closes a question rather than raising one. classify.py is R-E05's named defence, so a silent zero from it is expensive. |
| `LundyLoop/tools/loop_mark_print_gate.py` | python | no | yes | **AUDITED-FLAGGED** | Does NOT use the preflight guard, unlike 8 of its 12 siblings. Not shown broken; flagged because a false zero here closes a question rather than raising one. classify.py is R-E05's named defence, so a silent zero from it is expensive. |
| `Science_Teesside/launch-engine/check.js` | node | yes | yes | **AUDITED-FLAGGED** | 33 static assertions on payload + source text; never renders, so it structurally cannot see a cascade fault. Its motion-name rule measures class NAMES and claims "no rival vocabulary" — `.sci-spotmove` passed it while composing with `.g-spot` to defeat its own gate. |
| `Science_Teesside/launch-engine/test/health.js` | node | no | yes | **AUDITED-FLAGGED** | Now sound for JS errors, overflow, duplicate ids and cross-SVG refs. Its print assertion was a tautology (`X || true`); retired, and replaced by print-pack.js. |
| `build-anim/tools/preview.mjs` | node | yes | yes | **AUDITED-FLAGGED** | THROW-ONLY. Its only failure condition is `errs.length` — a thrown page error. Renders assets and reports "rendered N asset(s)" but never asserts N>0, and cannot detect the failure build-anim/README.md itself names: "a step targeting a part name that does not exist does nothing at all, quietly." Patch recorded below; NOT applied — gate 1 holds build-anim/ untouched. |
| `LundyLoop/tools/assessed_conditions_gate.py` | python | no | yes | **AUDITED-SOUND** | Uses the preflight guard (LL-INST-11), so an absent corpus or shallow clone fails loud instead of returning a plausible zero. |
| `LundyLoop/tools/hash_sweep.py` | python | no | yes | **AUDITED-SOUND** | Uses the preflight guard (LL-INST-11), so an absent corpus or shallow clone fails loud instead of returning a plausible zero. |
| `LundyLoop/tools/identity_audit.py` | python | no | yes | **AUDITED-SOUND** | Uses the preflight guard (LL-INST-11), so an absent corpus or shallow clone fails loud instead of returning a plausible zero. |
| `LundyLoop/tools/preflight.py` | python | no | yes | **AUDITED-SOUND** | LL-INST-11. The estate's own answer to the false-zero family, built after ko_staleness.py returned "0 candidates, all clean" on a shallow clone. Exits 3 when its environment is not what it requires. |
| `LundyLoop/tools/print_pack_audit.py` | python | no | yes | **AUDITED-SOUND** | Uses the preflight guard (LL-INST-11), so an absent corpus or shallow clone fails loud instead of returning a plausible zero. |
| `LundyLoop/tools/sitemap_audit.py` | python | yes | yes | **AUDITED-SOUND** | Uses the preflight guard (LL-INST-11), so an absent corpus or shallow clone fails loud instead of returning a plausible zero. |
| `LundyLoop/tools/verify_commit_set.py` | python | no | yes | **AUDITED-SOUND** | Uses the preflight guard (LL-INST-11), so an absent corpus or shallow clone fails loud instead of returning a plausible zero. |
| `Science_Teesside/launch-engine/build.js` | node | yes | yes | **AUDITED-SOUND** | Pins source SHA-256 into every dist artefact. |
| `Science_Teesside/launch-engine/test/gate-leak.js` | node | yes | yes | **AUDITED-SOUND** | Measures computed style on the shown slide across 4 gate types. Demonstrated failing on a reintroduced leak. |
| `Art_Teesside/tools/assert_cooccurrence.py` | python | no | yes | **NOT-YET-AUDITED** |  |
| `Art_Teesside/tools/assert_estate.py` | python | no | yes | **NOT-YET-AUDITED** |  |
| `Art_Teesside/tools/assert_kit.py` | python | no | yes | **NOT-YET-AUDITED** |  |
| `Art_Teesside/tools/assert_print.js` | node | no | yes | **NOT-YET-AUDITED** |  |
| `BUILD_ASDAN/_framework/qa_check.py` | python | yes | yes | **NOT-YET-AUDITED** |  |
| `BUILD_ASDAN/_framework/smoke_test.js` | node | no | yes | **NOT-YET-AUDITED** |  |
| `BUILD_ASDAN/_framework/style_check.js` | node | yes | yes | **NOT-YET-AUDITED** | Claims a change is visually inert. Iterates a set; empty-set behaviour unverified. |
| `_passla/build/gates.py` | python | no | yes | **NOT-YET-AUDITED** |  |
| `_passsci1/batch_gate.py` | python | no | yes | **NOT-YET-AUDITED** |  |
| `_passsci1/gates.py` | python | no | yes | **NOT-YET-AUDITED** |  |
| `_passsci1/hub_chip_gate.js` | node | no | yes | **NOT-YET-AUDITED** |  |
| `build-engine/tools/quality_check.js` | node | no | yes | **NOT-YET-AUDITED** | Iterates and can complete on an empty set; no exit-1 path found by inspection. |
| `grow-anim/wire_lessons.py` | python | yes | yes | **NOT-YET-AUDITED** |  |
| `tools/glitchclash/gc-a11y.test.js` | node | no | yes | **NOT-YET-AUDITED** |  |
| `tools/glitchclash/gc-cb.test.js` | node | no | yes | **NOT-YET-AUDITED** |  |
| `tools/glitchclash/gc-clock.test.js` | node | no | yes | **NOT-YET-AUDITED** |  |
| `tools/glitchclash/gc-endless.test.js` | node | no | yes | **NOT-YET-AUDITED** |  |
| `tools/glitchclash/gc-fx.test.js` | node | no | yes | **NOT-YET-AUDITED** |  |
| `tools/glitchclash/gc-hc.test.js` | node | no | yes | **NOT-YET-AUDITED** |  |
| `tools/glitchclash/gc-mods.test.js` | node | no | yes | **NOT-YET-AUDITED** |  |
| `tools/glitchclash/gc-music.test.js` | node | no | yes | **NOT-YET-AUDITED** |  |
| `tools/glitchclash/gc-weekly.test.js` | node | no | yes | **NOT-YET-AUDITED** |  |
| `tools/glitchclash/gc.test.js` | node | no | yes | **NOT-YET-AUDITED** |  |
| `tools/verify_axiomshift.js` | node | yes | yes | **NOT-YET-AUDITED** |  |
| `tools/verify_axiomshift.sh` | bash | no | no | **NOT-YET-AUDITED** |  |
| `tools/verify_charcoal.sh` | bash | yes | no | **NOT-YET-AUDITED** |  |
| `tools/verify_offbrand.sh` | bash | yes | no | **NOT-YET-AUDITED** |  |

## The `preview.mjs` patch, recorded and not applied

Job 1 asks for this fixed; gate 1 holds `build-anim/` untouched. **The gate wins**
— it was reaffirmed across two briefs ("its convergence has its own gated slot").
The patch is recorded here so it is actionable without violating the gate.

Today its only failure condition is a thrown page error:

```js
if (errs.length) { console.error(errs.join('\n')); await browser.close(); process.exit(1); }
```

`rendered ${n} asset(s)` is printed but never asserted, so `n === 0` exits 0. The
fix is to assert the count, and to assert that each step actually moved something:

```js
if (n === 0) { console.error('rendered 0 assets — nothing was exercised'); process.exit(1); }
// and, per build-anim/README.md's own warning about silent no-ops:
const dead = await page.evaluate(() => [...document.querySelectorAll('.ba-stage')]
  .filter(s => s.querySelectorAll('[data-part]:not(.ba-hidden)').length === 0)
  .map(s => s.dataset.baAsset));
if (dead.length) { console.error('stages that revealed nothing: ' + dead.join(', ')); process.exit(1); }
```

## Generators — produce artefacts, assert nothing, correctly

- `Art_Teesside/tools/kit_text.py`
- `BUILD_ASDAN/_framework/apply_framework.py`
- `BUILD_ASDAN/_framework/prune_dead_css.py`
- `LundyLoop/tools/bundle_facts.py`
- `LundyLoop/tools/patch_loopmark.py`
- `Science_Teesside/launch-engine/inject.js`
- `_passla/build/boot.js`
- `_passla/build/gen.py`
- `_passla/build/gen_catalogue.py`
- `_passsci1/build_contact_sheet.py`
- `_passsci1/build_pack.py`
- `_passsci1/inputs/build_staff_pack.py`
- `_passsci1/place.py`
- `_passsci1/planner_update.py`
- `_passsci1/render_topic.py`
- `_passsci1/render_v5.py`
- `build-anim/inject.py`
- `grow-anim/inject.py`
- `tools/build_staff_pack.py`

## Engines — runtime libraries, not instruments

- `Science_Teesside/launch-engine/sci-engine.js`
- `grow-anim/grow-anim.js`

## Named backlog

The 27 NOT-YET-AUDITED instruments are a pass of their own. The two
largest clusters:

- **`tools/glitchclash/*.test.js` (10 files)** — a real suite with descriptive
  headers, gated in CI on `Games/*.html` paths. Untouched here because nothing in
  this pass changed the game.
- **`Art_Teesside/tools/assert_*` and `_passsci1/` gates** — belong to passes with
  their own registers. Auditing them without their briefs would repeat the mistake
  this pass exists to correct: measuring something adjacent to the claim.
