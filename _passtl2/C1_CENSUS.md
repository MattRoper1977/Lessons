# TL-2 C1 — PROTOCOL branded-token census, reproduced

Reproduced 18 August 2026 against the pinned runtime
`aca3ea1e3feb133b07b686dab2aecc901899a65d77b1f07f697cf08967730642` (374,402 B), **before any editing**,
as C1 requires. Part C is **stopped at C2 (P1 unanswered)** — nothing was edited.

## C0 pins — all pass

| Pin | Expected | Measured | Result |
|---|---|---|---|
| C0-1 runtime | 374,402 B · `aca3ea1e…` | identical | PASS |
| C0-2 package | `48f72942…` · CHECKSUMS 21/21 | identical · 21 entries, 21 OK, 0 FAILED | PASS |
| C0-3 structure | 1 inline script (264,966 B) · `node --check` · 0 URL literals · 250 ids, 0 dupes · ends `</html>` | 1 · 264,966 · OK · 0/0 · **250, 0** · yes | PASS |
| C0-4 storage | `…studio_v2` · `…studio_v1` · `…advanced_suite_v2` | all three present | PASS |
| C0-5 suite | 6 modes · schema 2 · `RTCPeerConnection({ iceServers: [] })` | clash, crossfire, physics, sandtable, golf, sync · `SCHEMA_VERSION = 2` · 1 | PASS |

Package filename note: the prompt names `…_PRODUCTION_2026-08-18.zip`; the supplied file is
`…_PRODUCTION_20260818.zip` and expands to a hyphenated internal directory. The sha256 matches exactly,
so it is the same artefact under a different outer filename.

## C1 census — reproduced

**Agent roster — all ten match exactly** (46 tokens total):

| brimstone | omen | viper | sova | fade | breach | jett | raze | killjoy | cypher |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 3 | 6 | 3 | 7 | 3 | 5 | 5 | 2 | 6 | 6 |

**Role taxonomy — all four match exactly:** Controller 4 · Initiator 5 · Duelist 5 · Sentinel 2.

**Maps:** runtime Ascent 7 ✓ · Haven 4 ✓. Docs (over the full 12-file doc set) Ascent 17 ✓ · Haven 1 ✓.

**Trademark:** runtime VALORANT 1 ✓ · Riot 2 ✓; docs VALORANT 1 ✓ · Riot 3 ✓.

**Callouts:** all 15 listed callouts present. `Mid crate` 4 · `Mid … wall` 4 (the prompt's "twelve
`Mid crate …`/`Mid … wall` entries" resolves to 8 by these two patterns — see counting notes).

**Blueprint titles:** all three present verbatim.

## Counting-method notes — state these before editing

Two prompt figures are correct only under a specific counting method, and one breakdown is wrong.

1. **`Spike` 83 is a SUBSTRING count.** Whole-word `spike` is **66**; raw substring `pike`/`spike`
   occurrences total **83**. The 83 includes identifiers where `spike` is a fragment
   (`spikeCountdownText` 2, `spikeStatusText` 2, `evaluateSpike` 2, `runtime.lastSpikeSecond` 4,
   `spike-panel` 3, `spike-actions` 4, `state.spike` 20). Both numbers are right; a rename plan must
   say which it is using. The save-schema fields are `plantedAt` (15) and `defusedAt` (13).

2. **`bind` — the prompt's breakdown is WRONG, and the real hazard is larger.** The prompt says
   "13 hits, of which 11 are the map and 2 are JavaScript `.bind()`". Measured:

   | form | count | what it is |
   |---|---:|---|
   | raw substring `bind` (ci) | **13** | matches the prompt's total |
   | `.bind(` JavaScript calls | **0** | **there are none** |
   | `tabindex` | **3** | CSS `[tabindex]:focus-visible` + 2 `<canvas tabindex="0">` |
   | `bindSetting(` | **6** | a local helper function and its five call sites |
   | the map itself | **4** | `bind: {`, `id: "bind"`, `name: "BIND"`, `displayName: "BIND // …"` |

   So a blind replace of `bind` would break **`tabindex` attributes and six `bindSetting` call sites** —
   not `.bind()`, which does not occur. C5-1's stated exclusion should therefore be
   **whole-word `bind` excluding `tabindex` and `bindSetting`**, and that exclusion must be stated
   explicitly in the gate rather than applied silently.

## The P1 question, as the artefacts actually present it

Reported as measurement, not as a recommendation — P1 is Matt's ruling and Part C stops until it lands.

The package **already asserts original geometry**, in two places:

- `PHYSICS_AND_ANALYSIS_NOTES.md` §10: *"Maps are original schematic training maps, not surveyed
  proprietary layouts."*
- `DESIGN_AND_ARCHITECTURE.md` §10: *"The map blueprints and operatives are original schematic
  coaching constructs."*

Yet the same build ships publisher map names (Ascent/Haven/Bind), the publisher's own callout
vocabulary (A HEAVEN, CATWALK, MID PIZZA, B MARKET, A LONG, C LINK…), a blueprint titled
`ASCENT // SAN MARCO TRAINING BLUEPRINT`, the ten publisher agent names, the four publisher role
names, and a fan-content disclaimer naming VALORANT and Riot.

**That is the tension C2 exists to resolve, and it cannot be settled by counting tokens.** Whether the
floorplans are genuinely original constructs that were merely *labelled* with publisher vocabulary, or
are reconstructions, is a judgement about the geometry itself. If they are original, P1-A is largely a
relabelling plus deleting a disclaimer that was never needed; if they are reconstructions, the docs'
originality claim is itself inaccurate and P1-A means authoring three new layouts.

I did not attempt to settle it, and no geometry was touched.
