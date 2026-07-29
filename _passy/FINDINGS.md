# FINDINGS — Pass Y (declare_assumptions rollout)

**Branch** `pass-y-assumptions` off `main` `e09db7c`. Additive only. Deploy-visible change set **empty**.
R-H09 name gate: "Pass Y" verified free in git, REGISTER and HANDOVER before adoption.

## What shipped
Assumptions banners on **7 result-printing instruments**, routed by output contract:
- **STDERR** (stdout is JSON — a text line corrupts `json.load`/`jq`): `identity_audit`, `hash_sweep`,
  `link_graph`, `print_pack_audit`, `assessed_conditions_gate`.
- **STDOUT** (human-read text): `sitemap_audit`, `verify_commit_set`.
- `classify.py` (a library, no result surface) **declares** `ASSUMPTIONS` as data; `print_pack_audit` **reads**
  and prints them attributed — proved read-not-restate (change classify → audit banner changes, no audit edit).
- Recorded as **R-E12** (amended: *respect the output contract, not enumerate consumers; the failure signal is
  the exit code, never a non-empty stderr*).

## Proof gate (a–d), all instruments — see the merged-tip re-proof in the session record
(a) output diff == exactly the banner · (b) exit codes unchanged in every path · (c) verdict byte-identical
(JSON stdout `cmp`-identical; text stdout single-line diff) · (d) X3 guards still fire, **no `require_full_clone`
added to the shallow-safe tools**, `ko_staleness` unchanged (114, empty stderr).

## THE FINDING — R-E13 · `loop_mark_print_gate` is fail-silent BY ABSENCE
- **Precondition:** LL-INST-09 needs **playwright + Chromium** (renders each file at `media=print`). **Absent in
  the agent sandbox** (`ModuleNotFoundError: playwright`).
- **Why it is a finding, not a to-do.** An instrument that cannot run *in the environment where passes execute*
  never runs, never reports, and **its silence is indistinguishable from a clean result** — Pass X's own thesis
  (a false zero from a check that never examined the thing), pointing at a class Pass X's census did not include:
  the instrument that is simply never invoked here.
- **Unproven at HEAD:** no `loop_mark_print_gate` verdict exists in any agent-run pass; the print-reaches-paper
  claims it checks (R-A07 family) are unverified by this instrument, Pass Y included. Its banner was **not**
  added — a banner proved on no run is an unasked question (standing rule 6).
- **Disposition:** attaches to whichever future pass legitimately runs in a Chromium-capable environment — not a
  special errand. Until then, absence of a `loop_mark_print_gate` result means **not run**, never **clean**.

## Unchanged
The 114 KO candidates stay **characterised, not triaged** (39 R-E07 artefacts · 75 body-movers · 2 assessed)
until a separate key. The "37 of 49 KOs" stays **UNVERIFIED at HEAD** (R-G05) — not re-derived in passing.

## Carry-forward
- Add the `loop_mark_print_gate` banner + take its verdict from a Chromium-capable run (R-E13).
- The stdout-contract rule (R-E12) governs every future instrument: JSON on stdout ⇒ banner to stderr, always.

*Tip SHA not written (R-G04): derive with `git log -1`.*
