# PROP-1 — the gate record

Branch `claude/prop-1-apply` · rollback anchor `e63f047` · 34 commits · 202 files changed.

## §2 gates → merge

| gate | result | evidence |
|---|---|---|
| per-family control pairs fired | **PASS** | each family gated at its own commit; blocking findings from the adversarial verifiers fixed before the family landed |
| print parity | **PASS** | every screen edit swept its print mirror in the same commit; old strings re-grepped to 0 per family |
| payload shas regenerated + consistent | **PASS** | 3 payloads; **33/33 sharing files carry the new sha** for each; `build_payloads.py --check`, `integrate.py --check --expect-build-materialized`, `check.py` all PASS |
| PART B gates where guidepatch ran | **PASS** | 140 decks: default-hidden · G-toggle · persistence · **print-identical vs a pre-strip snapshot** · idempotence (0/140 changed on re-run, 0 bytes) · reversibility (strip→re-patch returns 140/140 byte-identical) |
| scored controls proven | **PASS** | **118/118** controls in headless Chromium: all-correct = full marks, one-wrong = n−1, 0 page errors |
| sentinels 50 / 123 | **PASS** | set-identical to base at every commit, including through XP26's structural block move |
| protected manifest | **PASS** | 35 window shifts, **each named in `PROTECTED_DELTAS.tsv` with its authorising row**; every marker count unchanged |
| food census | **PASS** | 51 tracked entries estate-wide, **0 moved**; `_sca1/food_census.base.json` byte-identical to base and to `.now` |
| `node --check` all touched blocks | **PASS** | 694 blocks OK / 0 FAIL over 259 files |
| boot multiset = baseline × 3 viewports | **PASS** | 181 changed files × 3 viewports = 543 runs, **all clean**; the identical file set at `e63f047` is also all clean → error multiset identical (both empty) |
| chip gate if `resources.json` touched | **N/A** | `resources.json` not touched |
| both repos' gates if anything crosses | **N/A** | nothing crosses; Apps is out of scope |

## Answer keys

Measured across **all 202 changed files**: exactly **3** carry a moved
`data-correct|c|e|h|m|fix` attribute — `A-P109`, `A-P110` (the deliberate pill-id collapse
that fixes a control rejecting two thirds of correct taps) and `SCA-P7` (the `data-h` hint
its row quotes verbatim). All three are their row's literal instruction; all three are
Chromium-proven.

## Row tally

| | rows |
|---|---:|
| table `apply` | 284 |
| ruled in by §0.2 | 17 |
| ruled in by §-1a addendum (A-P118, A-P126) | 2 |
| **applied** | **303** |
| withdrawals executed | 11 |
| **actioned** | **314** |
| held untouched (A-4 · A-7 · A-13 · A-22 · A-50 · XA21 · A-47 · XP18 · SCA-P4) | 9 |
| **table total** | **323** |

Within the 303: `XP30` stopped on a count mismatch (§1) and is reported unapplied;
`A-P123`, `A-P113`, `A-P126` and `XO2` are closed with no edit because the bytes or the
ruling made an edit wrong, each verified rather than assumed.
