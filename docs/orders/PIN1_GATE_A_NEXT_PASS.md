# PIN1 — actual digest gate, next implementation pass

Source-only refresh 2026-09-12T14:12:04.207Z, Lessons main `12828ac35af20b1058b9f5f1c0774f30d34df0b1`.
This is the next eligible PIN1 §2.1 work under the recovered full order. The filed
§2.2 ruling for UX2 remains scoped to that gate alone; its fallback is delivered.
The actual digest gate has a registry, so its remaining derivation is distinct work.

| Measured set | Count |
|---|---:|
| Declared distinct paths, all five registry groups | 444 |
| Canonical assets / manifests / catalogue files / LundyLoop / caller | 4 / 2 / 434 / 3 / 1 |
| Gate A's asserted Lessons paths | 440 |
| Current PR and push trigger paths (identical) | 10 |
| Asserted paths which trigger gate A | 6 |
| Asserted paths which do not trigger gate A | 434 |
| Asserted files absent from the checked source | 0 |
| Trigger paths without a digest assertion | 4, all DESIGN |

Gate A is `.github/workflows/mbm-cross-estate-unification.yml`. Its actual checker
is `tools/verify_cross_estate_unification.py`. The six covered paths are index.html,
the four canonical assets and the education-pages.yml caller. The full 434-path
list, every registry membership and every trigger/assertion classification are
in `rf3-evidence/PIN1_GATE_A_REFRESH.json`, with both Git blobs verified against
actual main. This refresh reproduces the earlier count at a new exact revision;
it does not reuse the old timestamp or claim an observed Actions gate run.

The four reverse-asymmetry paths are the checker itself, browser verifier,
workflow itself and docs/MBM_CROSS_ESTATE_UNIFICATION.md. They are intentional
self-trigger/structural/documentation coverage, not missing digest assertions.
The 444 declared union includes Apps-only conditional paths; do not report it as
440 Lessons assertions or credit UX2's non-pin predicates with digest coverage.

## Bounded implementation sequence

1. Derive gate-A trigger coverage from the actual registry and assertion predicates,
   respecting conditional manifest/repository ownership. Adding a declared dependency
   must not silently escape the generated coverage. Preserve existing intentional
   self-trigger paths and refuse unqualified `**`.
2. Inspect the shared checker's change boundary and Apps mirror requirements before
   choosing the smallest code location. Do not ratchet a pin or waive a check to make
   the repair's own PR green. The original PIN1 scope governs this separate repair;
   the UX2-only fallback ruling is not authority to widen other unrelated gates.
3. Verify the generated trigger list agrees with the current registry and prove it
   catches a newly declared dependency. Record full path denominators, both directions.
4. Execute PIN1 §3 exactly: pinned-file-only RED without checker edits; corrected-pin
   GREEN; unrelated change leaves this gate DORMANT. Use scratch branches and close
   all three after collecting actual Actions evidence. Local matcher output alone
   cannot close those event proofs.

No implementation or scratch branch was made in this refresh pass. Apps coverage
is not remeasured here; the earlier complementary-gate observation keeps its original
scope/time. LP1's material-scope stop, held PR ownership and the remaining missing
orders survive. PIN1 is not closed by either this census or SB1's schema proof.

PIN1_PARTIAL
