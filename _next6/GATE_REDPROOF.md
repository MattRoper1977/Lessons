# N6 §4 — gate red-proof

Every gate below was run once against a **deliberately perturbed** copy of the intake tree
and observed to fail. A gate whose red has never been seen is not evidence, and §4 requires
this before any green is trusted.

Reproduce: copy `packs/` to `perturb/`, apply the perturbation, run
`python3 _next6/tools/run_gates.py <perturb> <intake>`.

| gate | perturbation applied | observed red |
|---|---|---|
| G1 syntax | injected `function(){` into an inline `<script>` | `6 inline JS blocks … 1 errors` |
| G2 tag balance + dup id | duplicated a live `id` and opened an unclosed `<div>` | `1 files with tag-balance errors, 1 with duplicate ids` |
| G3 timings sum 40 | rewrote one `"timings"` array to `[1,2,3]` | `12 timings arrays, 1 not summing to 40` |
| G4 offline integrity | added `localStorage`, `fetch()`, and `<script src="https://…">` | `3 violations` |
| G5 reduced motion | added an unguarded `@keyframes n6perturb` | `1 not neutralised` |
| G6 manifest ↔ disk | appended a manifest entry for a file not on disk | `1 hard manifest disagreement` |
| G9 sentinel SET-invariance | planted one `ll-g:loop-mark` absent from intake | `intake 0 files, now 1 files, symmetric diff 1` |
| G10 s23-no-learner-names | supplied a synthetic reference list + planted its token | `1 reference entries, 1 hits` |

**G10 also red-proves its INVALID path.** With no reference list it returns
`MEASUREMENT INVALID` and never `PASS` — the order's §4.10 requirement. The real reference
list is deliberately **not committed**: a list of learner names in a public repository is
itself the disclosure the gate exists to prevent. `tools/verify_fixture_names.mjs` is the
list-free predicate half and its own `--self-test` passes in **both** directions
(3 RED vectors, 5 GREEN, plus a seeded-file control that reds the real tree).

**G7 (print parity) and G8 (additivity)** are proved by construction inside the N2 and N7
commits — each records a strip-the-insertion → byte-identical assertion. They cannot be
red-proved on an unperturbed tree because they compare against intake, so their red is the
mismatch itself.
