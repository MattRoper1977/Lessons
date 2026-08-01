# Instrument index

One file, two sections, because they answer different questions.
**Section 1** is what has been audited and what each instrument asserts.
**Section 2** is what has been named and deliberately not audited.
Reading a section 2 entry as a finding is the mistake this split exists to prevent.

---

# Section 1 · Audited inventory

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
matched nothing produces a **false zero**, which `preflight.py` names as *"the
most expensive defect class: it CLOSES a question that was never examined."*
That is the estate's own phrase and the one to use.

Recorded as INSTRUMENTS.md standing rules 13 (timing), 14 (false zero),
15 (fix at the gate), 16 (prove the input set) and REGISTER R-E22 (gate shape).

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


## BUILD_ASDAN visual framework — three instruments (arriving with #14)

Audited here against the standing requirement, by reading them rather than by
carrying the claim: each proves its input set is non-empty before it can report a
zero, which is the false-zero guard rule 2 asks for.

| instrument | asserts | empty-set behaviour | status |
|---|---|---|---|
| `BUILD_ASDAN/_framework/contrast_check.js` | contrast ratios per element, counted | `if (!files.length) … exit(2)` | **AUDITED-SOUND** |
| `BUILD_ASDAN/_framework/smoke_test.js` | `total === 10` slides, forward and back to the last slide and home | `if (!total)` fails rather than passing | **AUDITED-SOUND** |
| `BUILD_ASDAN/_framework/label_rest_check.js` | label rest-state per deck | `if (!files.length) … exit(2)` | **AUDITED-FLAGGED — deliberately red** |

**`label_rest_check.js` is red on purpose, on four decks: CAREERS_W6, COMM_W1,
DUKE_W5, LI_W2.** It is not a broken instrument and the reds are not a backlog: the
question of whether each is design or defect is recorded as open for Matt in
`reports/close/2026-08-01-convergence.md`. An instrument left red with its reason
written down is worth more than one silenced — but only while the reason is
written down, which is what this row is for.

## Named backlog — four passes, not one sweep

The 27 NOT-YET-AUDITED instruments are **not** a general sweep. Each cluster
belongs to a register that must be loaded first; auditing without the brief is
how you measure the wrong thing confidently. Filed as discrete future passes.

### BL-1 · Glitch Clash suite — 10 scripts
- **Load first:** the Glitch Clash brief, plus `tools/glitchclash/run.sh` for how
  the suite is invoked in CI.
- **Files:** `tools/glitchclash/gc*.test.js`.
- **Why not folded in:** CI gates it on `Games/*.html` paths, and nothing in this
  session changed the game. Running it here would prove only that an unchanged
  thing is unchanged. It is also the one cluster with genuinely descriptive
  per-file headers, so it is the cheapest to audit when its own pass comes.

### BL-2 · Art Teesside assertions — 5 scripts
- **Load first:** `Art_Teesside/` register (`AT-INST-01..04` are self-numbered, so
  a register exists).
- **Files:** `assert_estate.py`, `assert_cooccurrence.py`, `assert_kit.py`,
  `assert_print.js`, `kit_text.py`.
- **Why not folded in:** they assert co-occurrence and closed-kit invariants whose
  *expected sets* live in that register. Without it, "0 violations" cannot be
  distinguished from "0 items examined" — the false zero exactly.

### BL-3 · `_passsci1` and `_passla` gates — ~8 scripts
- **Load first:** the SCI-3 / Pass LA briefs; several carry hardcoded expected
  constants (`gates.py`, `batch_gate.py`, `hub_chip_gate.js`).
- **Why not folded in:** standing rule 3 in this index's terms — an assertion
  against a hardcoded constant is only meaningful beside the brief that set it.
  `verify_commit_set.py` already caught a stale constant of exactly this kind in
  its own declaration.

### BL-4 · BUILD_ASDAN and build-engine — 4 scripts
- **Load first:** `BUILD_ASDAN/_framework/` conventions.
- **Files:** `qa_check.py`, `smoke_test.js`, `style_check.js`,
  `build-engine/tools/quality_check.js`.
- **Why not folded in:** `style_check.js` claims a change is *visually inert*,
  which is a claim about rendering, and its empty-set behaviour is unverified.
  `.at-reveal` (recorded in R-E22) also lives in this cluster's stylesheet, so the
  pass has a concrete first question to answer.

## Known-incomplete: the fill-mode enumeration

The gate census scanned **five stylesheets**. Tested afterwards, that was
incomplete — fill modes also live in:

- inline `style="…animation:…both"` (5 files, including `Science_Teesside/Grow/SCI_G_W3_Friction.html`)
- longhand `animation-fill-mode` (the `2 Physics 10/` decks)
- deck-level `<style>` blocks (`fadeInUp` and the framework animations, inlined)

**Currently harmless, and the reason matters.** Every gate is hardened with
`visibility:hidden` (R-E22), so it holds against *any* fill-mode class declared
anywhere, enumerated or not — INSTRUMENTS.md standing rule 15.

**It becomes load-bearing the first time anyone patches a call site instead of a
gate.** At that moment the fix is only as complete as this enumeration, and this
enumeration is known not to be. An incompleteness that states its own trigger is
manageable; one that is quietly carried is not.

---

# Section 2 · Named future passes

Work this session identified but did not open. Each entry names the class, the
search pattern that would find it, and what a pass would have to prove. **Nothing
here has been audited.** An entry is a scope, not a finding.

Companion: `LundyLoop/tools/INSTRUMENTS.md` is the instrument register proper
(LL-INST-NN entries, with derivation and quarantine status). Section 1 above is
the audited inventory. This section is the *backlog* — classes of defect worth a
pass, not instruments that exist.

---

## IDX-1 · Early returns that skip trailing work

**Filed 2026-08-01. Not audited.**

`if (!x) return;` at the top of a function whose *tail* does something unrelated to
`x` is a silent-skip generator: the guard is written for the head, and every later
addition to the function silently inherits it.

**This estate has been bitten by it once, measurably.** `grow-anim.js`'s `paint()`
opened with

```js
function paint(stage) {
  var st = stage._g, bar = $('.g-bar', stage); if (!st || !bar) return;
```

and a later pass appended `fit(stage);` to its tail. The guard exists because the
*bar-painting* code needs a bar; the *fitting* code does not. Result: every stage
carrying `data-grow-nobar` was never fitted — five stages across the five BUILD
decks, each left depending on an async `ResizeObserver` as its only backstop. That
is a visible reflow in the classroom and invisible to any synchronous check. It was
found only because two probes disagreed by 37px.

**Search pattern.** Functions whose first statement is a guard-return and whose body
is longer than the guard's concern:

```bash
# candidate sites: a guard-return in the first two lines of a function
rg -n --multiline --multiline-dotall \
  'function [a-zA-Z]+\([^)]*\) \{\n\s*(var [^\n]*)?\n?\s*if \([^)]*\) return;' \
  --glob '*.js' --glob '!node_modules'
```

Each hit needs reading, not counting: the question is whether anything after the
guard is independent of what the guard tests. A pass would have to (a) enumerate
every guard-return site in `grow-anim/`, `build-anim/` and `LundyLoop/tools/`,
(b) for each, state what the guard protects and what the tail does, and (c) prove
by a failing-then-passing test that no tail is unreachable for a live input class.

**Why it is worth a pass rather than a lint.** A lint would flag every guard-return
in the estate, which is most of them and nearly all correct. The defect is semantic
— *unrelated* tail work — and only reading separates the two.

---

---

## IDX-2 · Instruments not yet entered in the register — **SUPERSEDED**

Filed unverified, and rightly: the count and its scope were carried from a brief
and not re-derived. **Section 1 has since derived them.** 27 NOT-YET-AUDITED
instruments, broken into four discrete passes — BL-1 Glitch Clash (10), BL-2 Art
Teesside (5), BL-3 `_passsci1`/`_passla` (~8), BL-4 BUILD_ASDAN and build-engine
(4) — each with the register that must be loaded first. Read §1's *Named backlog*,
not this entry.

Kept rather than deleted because the transition is the point: an entry marked
unverified became a verified one, which is rule 3 working as intended.

---

## IDX-3 · Fill-mode enumeration, known incomplete — **SUPERSEDED**

Also filed unverified, also since derived. §1's *Known-incomplete: the fill-mode
enumeration* names exactly what the census missed — inline `style="…animation:…both"`
in 5 files, longhand `animation-fill-mode` in the Physics 10 decks, and deck-level
`<style>` blocks — and states its own trigger: it becomes load-bearing the first
time anyone patches a call site instead of a gate.

---

## IDX-4 · The breakpoint fires on viewport height alone

**Filed 2026-08-01. Not audited. Do not build the width-banded threshold yet.**

`grow-anim.css`'s short-viewport arrangement switches on `@media (max-height: 960px)`.
The derivation shows the real constraint is height **and** width together — the
single-column We Do 2 slide's minimum-fit height rises as the viewport narrows:

| width | worst deck needs |
|---:|---:|
| 1920 | 932px |
| 1536 | 932px |
| 1366 | 935px |
| 1280 | 953px |
| 1093 | 953px |
| 1024 | 1005px |
| 819 | 1029px |
| 683 | 1069px |

A single threshold is therefore a simplification. **The exact failing region is:
width ≤ 1024, and height above 960 but below that width's own minimum-fit value.**
A 900×1000 viewport keeps the single column and fits; a 700×1000 viewport keeps it
and does not. Neither is in the matrix and neither is a classroom anyone has named.

**Why it is filed rather than built.** The last layout change nearly shipped a worse
regression than the one it fixed — `.slide.wedo2-layout { display: grid }` beat the
deck's own `.slide { display: none }` and halved every other slide — and that one at
least had a measured classroom behind it. This one has none. A pass would have to
(a) establish that any real machine lands in the region, and (b) show a width-banded
media query is more robust than a single threshold rather than merely more precise.

Raw derivation: `reports/convergence/_data/breakpoint-derivation.json`.
