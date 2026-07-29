# FINDINGS — Pass X (Instrument Integrity)

> **Letter rename, recorded per brief §0.** The brief is titled "Pass W", but **W is already spent** in this
> repo's git history — a prior content pass (`2976816` "Pass W: give every ASDAN We Do 1 an instruction line",
> `71751d2` "Pass W2…"), and `0706782` "Restore the Careers W6/W7 swap **that Pass W silently reverted**" (a real
> instance of the class this estate fears). My Phase-0 markdown grep missed it — it lived in commit subjects, not
> `*.md`. **This pass is renamed Pass X** (next free letter; Y also free, Z spent). Branch `pass-x-instruments`,
> working dir `_passx/`.

## Lineage
- **Pass U** (Lessons branch `pass-u-audit`, commit `7c4b2b4`, `_passu/FINDINGS.md`) found the FAIL-SILENT
  defect this pass repairs. Site branches from Pass U: `claude/pass-u-audit-hapesp` (site reconciliation) —
  named, not SHA-verified here.
- **Base:** `pass-x-instruments` off `origin/main` = `32ca685`. *(Corrected a base error: the branch was first
  cut off `pass-u-audit`; re-based onto `main` before any push, so Pass X carries only instrument commits.)*
- **Clone:** full — `git rev-parse --is-shallow-repository` = **false**, 485 commits. The work was NOT done on a
  shallow clone; that is the bug under repair.
- **R-E09 satisfied:** this pass modifies instruments and uses **none of them** to reach a content verdict.

## HEADLINE
The estate's most expensive defect class — a **false zero from an under-specified check** — had exactly **one
live instance** (`ko_staleness.py` on a shallow clone) and **one near-instance** (`verify_commit_set.py`'s
misleading diagnosis). Both are now **guarded, and each guard is proved to fire on a genuinely broken
assumption.** No past verdict was invalidated: a shallow false zero is recognisable, and no recorded verdict
shows it. **Deploy-visible change set: EMPTY** — only `LundyLoop/tools/*` and `_passx/*` moved.

---

## THE BLINDNESS CENSUS (all instruments, all classes)

| tool | external dependency | on failed assumption | class |
|---|---|---|---|
| classify.py | none (pure parse) | n/a | SAFE |
| identity_audit.py | `git ls-files` (HEAD) | complete on shallow | SAFE |
| hash_sweep.py | `git ls-files` + `rev-parse HEAD` | complete on shallow | SAFE |
| link_graph.py | `git ls-files` | complete on shallow | SAFE |
| print_pack_audit.py | `git ls-files` | complete on shallow | SAFE |
| assessed_conditions_gate.py | `git ls-files` | complete on shallow | SAFE |
| loop_mark_print_gate.py | Chromium (playwright) | playwright raises | FAIL-LOUD |
| sitemap_audit.py | network (urlopen) | "NOT a pass", exit 2 | FAIL-LOUD (house pattern) |
| verify_commit_set.py | git history `base..HEAD` | empty range → "found 0" FAIL, but no exit-code check → **misleading diagnosis** on shallow/unknown base | FAIL-WRONG → **repaired (X3)** |
| **ko_staleness.py** | git **cross-commit** history | shallow → 1 commit/file → **"0 candidates, clean"** | **FAIL-SILENT → repaired (X2)** |

**Two signals for the network scope:** only `sitemap_audit` imports `urllib.request/urlopen`; the other `urllib`
hits are `urllib.parse.unquote` (encoding) and a `SKIP` regex that *excludes* `https?:` links. So the
git-history FAIL-SILENT class is exactly one tool; the network FAIL class is exactly one tool, already loud.

**Other blindness classes (corpus / encoding / parse-shape)** are per-tool *logic*, already documented and
correctly handled in the record (R-C04 corpus; the percent-decode rules in hash_sweep/identity_audit; the
parse-shape rules in INSTRUMENTS). They have no single environment guard, and a wrong "fix" to correct logic is
a regression — **censused, not touched.** `require_corpus()` is provided in the preflight for future opt-in.

---

## WHAT WAS REPAIRED, AND HOW EACH GUARD WAS PROVED

### X1 · `LundyLoop/tools/preflight.py` — new shared instrument [LL-INST-11] (`357251b`)
Mirrors `sitemap_audit`'s house fail-loud shape rather than inventing a new one. Exposes
`require_full_clone(repo)`, `require_network(host)`, `require_corpus(min, actual, label)`,
`declare_assumptions([...])`. Helpers print `FAIL — … This is NOT a pass. Nothing below was checked.` and exit
non-zero (code 3). Self-test (`python3 preflight.py`) passes on this full clone.

### X2 · `ko_staleness.py` — guard the full-clone assumption (`7ecf75c`)
9-line additive change: `require_full_clone(REPO)` at the top of `main()`, then `declare_assumptions([...])`
so every result now prints `assumptions: full clone · 161-file KO corpus … · co-modification is a proxy…`.
- **Guard proved to FIRE (rule: break the assumption):** ran the patched tool against a **genuinely shallow
  clone** (`git clone --depth 1 file://… ; rev-parse --is-shallow-repository = true`) → printed the FAIL banner,
  **exit 3**, and reported **no count at all** (previously it reported "0 candidates, all clean").
- **Still correct on a healthy run:** full clone → **114 candidates / 3 / 44 (cardinality 161 ✓)**, exit 0 — the
  known-correct answer, with the assumptions banner beside it.

### X3 · `verify_commit_set.py` — name the real cause (`1738911`)
21-line additive change: before computing `base..HEAD`, fail loud if the clone is shallow, and check
`git rev-parse --verify <base>^{commit}`'s exit code so an unreachable base is named as such instead of
mis-reported as "commit count found 0".
- **Guards proved to FIRE:** (a) unknown base ref → `FAIL — base ref '…' does not resolve …`, exit 1;
  (c) shallow clone → `FAIL — shallow clone: base..HEAD cannot be trusted …`, exit 1.
- **Proved not to false-fire:** valid base `HEAD~5` on the full clone → passes both new guards and reaches
  `PASS commit count == 5 · found 5` (then continues to its declared-shape checks, as designed).

*All guards were exercised against a real broken assumption, per the brief's non-negotiable acceptance test —
a guard that never failed is an unasked question.*

---

## WHAT THE PAST VERDICTS ARE WORTH → `VERDICT_PROVENANCE.md`
Only `ko_staleness` is FAIL-SILENT. Every verdict in the record that rests on it cites a **non-zero** count
(R-G02 109 · R-E07 45 · HANDOVER §7 GROW_HUM_W7 7 · `_passu` U-10 114), and a non-zero count is itself proof of
full history. **CONFIRMED = all; UNDETERMINED = 0; INVALIDATED = 0.** The bug is future-facing; the one run that
hit it (Pass U's first attempt) caught itself via rule 4, before the number entered the ledger. The brief's
"37 of 49 KOs disagree with slides" claim is **UNVERIFIED** — not `ko_staleness` output (it is temporal, reads
no content), and absent from the repo record; recorded but not repeated as fact.

## THE 114 — CHARACTERISED, NOT TRIAGED → `CARRYFORWARD_KO.md`
Shape only, no per-file verdict: **39** are the R-E07 Loop-Mark print-feedback artefact (clear first — likely
noise), **75** other body-movers, **2** assessed (GROW_HUM_W7, LAUNCH_HUM_W7 — read first, Matt's key, Card not
body). By area: BUILD_ASDAN 31 · Art_Teesside 28 · GROW_ASDAN 18 · Build 14 · Grow 8 · Launch 8 · biology 3 ·
chemistry 3 · Physics 1. **No KO was read for content in this pass.**

---

## REFUSED / DELIBERATE — do not re-raise
| # | what a fresh audit will re-raise | why it is not for this pass |
|---|---|---|
| DX1 | 7 "SAFE" git tools also touch git — "guard them too" | they use only `git ls-files`/`show HEAD:`/`rev-parse HEAD`, all complete on a shallow clone; a guard there is dead weight (a guard that can't fire is noise, R-standing-6) |
| DX2 | corpus/encoding/parse-shape blindness "unfixed" | per-tool *logic*, already correct in the record; no environment guard applies; touching correct logic is a regression |
| DX3 | the 114 KO candidates | a candidate LIST, not defects; triage is the next pass (R-G02 OPEN, R-E09) |
| DX4 | 39 Loop-Mark candidates "are stale organisers" | R-E07: print-feedback text a KO does not summarise — expected artefact, not staleness |
| DX5 | INSTRUMENTS.md now under-counts (preflight/others lack entries) | R-G03 — its own scheduled reconciliation pass; not opened here (adding entries mid-measure is the R-G03/R-E09 error) |
| DX6 | the prior "Pass W" silently reverted the Careers swap | already restored at `0706782`; historical, closed by reading |

## TIER 2 — one decision for Matt
- **X-T2-01 · Adopt `declare_assumptions()` across the remaining instruments?** Pass X wired it into the two it
  repaired. Every other instrument would benefit from printing its scope+assumptions beside its result (the
  discipline that would have surfaced this bug years earlier). Additive, no behaviour change. **Recommended yes**,
  as a small dedicated pass (not folded into a measuring pass, R-E09). *No lesson / no `resources.json` / no
  assessed file is touched by it.*

## HAND-BACK (standing order)
- **Provably better, on the branch:** X1/X2/X3 — the FAIL-SILENT and FAIL-WRONG instruments now fail loud, each
  guard proved to fire; the false-zero class is closed at the tool.
- **Waiting on Matt:** X-T2-01 (adopt assumption-banners estate-wide); and the 114 triage as its own pass
  (CARRYFORWARD_KO.md is its starting table).
- **Left alone and why:** the 7 SAFE tools, the correct-logic blindness classes, INSTRUMENTS.md (R-G03), and
  every KO candidate — the record already rules them or schedules them.

*Tip SHA intentionally not written (R-G04): derive with `git log -1` on the branch. Nothing merged; Matt merges.*
