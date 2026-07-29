# PLAN — Pass X (Instrument Integrity)

Branch `pass-w-instruments` off `main` (real name; harness did not rename). Repo tip at start `32ca685`
(origin/main == main, unchanged since Pass U). **Full clone confirmed** (`git rev-parse --is-shallow-repository`
= false, 485 commits) — the work is NOT done on a shallow clone (that is the bug under repair).

Letter W is FREE (only `_passu` exists; no pass-w branch; "Pass X" unused). R-E09 satisfied: this pass modifies
instruments and uses NONE of them to reach a content verdict.

## Scope fence
No lesson, no `resources.json`, no pupil-facing content, nothing `★ ASSESSED`. The 114 KO candidates are
characterised (shape/counts only) in CARRYFORWARD_KO.md — never triaged, never verdicted, never touched.

## THE BLINDNESS CENSUS (Phase 1) — every instrument, classified

| tool | external dependency | on failed assumption | class |
|---|---|---|---|
| classify.py | none (pure parse of file text) | n/a | SAFE |
| identity_audit.py | `git ls-files` (HEAD tree) | complete on shallow | SAFE |
| hash_sweep.py | `git ls-files` + `rev-parse HEAD` | complete on shallow | SAFE |
| link_graph.py | `git ls-files` | complete on shallow | SAFE |
| print_pack_audit.py | `git ls-files` | complete on shallow | SAFE |
| assessed_conditions_gate.py | `git ls-files` | complete on shallow | SAFE |
| loop_mark_print_gate.py | Chromium (playwright) | playwright raises | FAIL-LOUD |
| sitemap_audit.py | network (urlopen) | "NOT a pass", exit 2 | FAIL-LOUD (house pattern) |
| verify_commit_set.py | git history `base..HEAD` | empty range → "found 0" FAIL, but no git exit-code check → **misleading diagnosis** when base is outside a shallow clone | FAIL-WRONG (diagnosis) |
| **ko_staleness.py** | git **cross-commit** history (`git log -- file`, `git show <old>:file`) | shallow → 1 commit/file → every KO+body "co-moved" → **"0 candidates, clean"** | **FAIL-SILENT** |

Only ONE true FAIL-SILENT. Two signals for the network scope: only sitemap_audit imports `urllib.request/urlopen`;
the other `urllib` hits are `urllib.parse.unquote` (encoding) and a `SKIP` regex excluding `https?:` links.

Other blindness classes (corpus/encoding/parse-shape) are per-tool LOGIC, already documented in REGISTER/INSTRUMENTS
(R-C04 corpus, the encoding rules, the parse-shape rules). They have no single environment-guard; censused in FINDINGS,
not repaired here (a wrong "fix" to correct logic is a regression).

## THE FIX, AS A CLASS (Phase 2)
1. `LundyLoop/tools/preflight.py` — shared, mirrors sitemap_audit's fail-loud shape. Exposes
   `require_full_clone(repo)`, `require_network(host)`, `require_corpus(expected_min, actual, label)`,
   `declare_assumptions([...])` (prints assumptions alongside results).
2. `ko_staleness.py` — call `require_full_clone` + `declare_assumptions` at top of `main()`. One commit.
3. `verify_commit_set.py` — check git exit code / base reachability so a shallow/unknown base names its real cause. One commit.

**Acceptance per tool: prove the guard FIRES on a genuinely broken assumption (real shallow clone / unknown base),
show the non-zero exit, THEN prove the repaired tool still returns its known-correct number on a full clone.**

## WHAT PAST VERDICTS ARE WORTH (Phase 3)
`VERDICT_PROVENANCE.md`: every record-verdict resting on a FAIL-SILENT tool → CONFIRMED / UNDETERMINED / INVALIDATED.
Only `ko_staleness` is FAIL-SILENT, so the scope is the KO-staleness verdicts (R-G02, R-E07, HANDOVER §7, `_passu` U-10).

## Commits
One per instrument: `Pass X<n>: <tool> — <assumption guarded> — rollback <SHA>`. Verify each at origin by a read
separate from the write. Deploy-visible change set: EMPTY (touches only tools + `_passw/` records).
