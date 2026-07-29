# VERDICT PROVENANCE — Pass X

**Question:** for the one FAIL-SILENT instrument (`ko_staleness.py`), is every verdict in the record that
rests on it still worth what it says? Marked **CONFIRMED** (assumption provably met) / **UNDETERMINED**
(record silent — needs a re-run) / **INVALIDATED** (assumption provably broken).

## The decisive property
A shallow-clone run of `ko_staleness` produces a **distinctive, recognisable output**: with one commit per
file, `i_ko <= i_body` for every file → **"CANDIDATES … 0 · clean 161"**. A *non-zero* candidate count is
therefore itself proof the run had full history — the false zero cannot masquerade as a real number. So any
recorded verdict citing a non-zero count is decidable from the number alone.

## `ko_staleness.py` (LL-INST-08) — every recorded verdict

| verdict in the record | count cited | provenance | mark |
|---|---|---|---|
| REGISTER **R-G02** — "161 KO · 109 candidates · 8 dropped · 44 clean" @ `35efefd` | 109 (non-zero) | non-zero ⇒ full history | **CONFIRMED** |
| REGISTER **R-G01 row 6** — "KOs ×161 · 109 candidates" @ `35efefd` | 109 | same run as R-G02 | **CONFIRMED** |
| REGISTER **R-E07** — "visible() hash moves in 45 of 45" @ `d601842` | 45 movement (non-zero) | non-zero ⇒ full history | **CONFIRMED** |
| HANDOVER **§7** / R-G02 read-first — GROW_HUM_W7 "7 content movers" | 7 (non-zero) | per-file history read | **CONFIRMED** |
| `_passu` **U-10** @ `7c4b2b4` — final "114 candidates" | 114 | post-`--unshallow` | **CONFIRMED** |
| `_passu` transient — "0 candidates, 161 clean" on the shallow clone | 0 | **the false zero itself** — but it was **CAUGHT by rule 4** (a zero replayed against a case that must be non-zero) and **never entered the ledger** | not a verdict; the near-miss that motivated Pass X |

**Summary counts: CONFIRMED = every recorded `ko_staleness` verdict. UNDETERMINED = 0. INVALIDATED = 0.**
The FAIL-SILENT bug was real and **future-facing** — the danger is the *next* shallow clone, not the past
record. No recorded verdict fell into it, because a false zero is recognisable and none of them show it. The
one run that did hit it (Pass U's first attempt) caught itself. Pass X converts "caught by a vigilant reader"
into "caught by the tool" so the next reader need not be vigilant.

## `verify_commit_set.py` (LL-INST-10) — not FAIL-SILENT
Its only recorded use is the Pass LL-G deployment gate (R-F08), run in-session on the full working clone; it
already fails loud (empty range → "found 0" → FAIL). Pass X only improves its **diagnosis** (names shallow /
unreachable base). No past verdict is at risk. **CONFIRMED / not-at-risk.**

## A brief claim I could NOT verify — recorded honestly
The Pass X brief states *"an earlier pass found 37 of 49 knowledge organisers disagreeing with their own
slides, printing wrong answers onto pupil revision sheets."* **This is not `ko_staleness` output.** That tool
is explicitly *temporal* — "asks nothing about correctness and reads no content" (its docstring) — and cannot
produce a "disagrees with slides" verdict. No "37 of 49" appears in `HANDOVER.md`, `REGISTER.md`,
`INSTRUMENTS.md`, or `_passu/FINDINGS.md`. A *semantic* KO-vs-slide check, if it exists, is a **different
instrument**; if the "37 of 49" refers to a future triage of the 114 candidates, that triage **has not run**
(it is the next pass, CARRYFORWARD_KO.md). **Marked UNVERIFIED — not relied on, not repeated as fact.**
(Standing rule 8 / R-H07: a number quoted across passes inherits an authority it never earned.)
