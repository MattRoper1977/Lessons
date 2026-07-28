# PLAN — Pass U (Lessons body)

Branch: `pass-u-audit` off `main` (real name recorded here per brief §3). Repo tip at start: `32ca685`.
Working dir: `_passu/`. FINDINGS.md + PLAN.md committed to branch.

## Framing correction (recorded, not relitigated)
The brief describes a "Pass Q / Pass U" programme with site branches `claude/pass-q-audit-c5tg3s@6845f44`
and `pass-u-audit`. **The actual Lessons repo records no Pass Q or Pass U** — its history is Lundy Loop
(LL-A…LL-I), Pass V (D&T v5), Pass S. The brief's rigor rules are honoured; its stated site SHAs/branches
are treated as UNVERIFIED cached claims (REGISTER R-G01). Site-side reconciliation done read-only in the
site repo already in the session.

## Prime directive (HANDOVER §"Start here")
This estate has been healthier than its instruments every time tested: 10 false-positive chains, 0 defects
ever reaching a pupil. **When an instrument disagrees with the estate, suspect the instrument first.**
Bar for a real finding is very high. Deliver honest dispositions, not alarm.

## Method (OWL)
Run the estate's OWN instruments (LL-INST-01…10). Do not rebuild them. Two independent signals per finding.
Every zero replayed against a planted positive. Scripts over reads; specimens over populations.

## Instruments to run (static, read-only)
1. classify.py (REQUIRED STAGE)   — print architecture
2. print_pack_audit.py            — slot requests vs markup
3. identity_audit.py              — declared↔actual, both directions
4. hash_sweep.py                  — dup/near-dup + catalogue both directions (needs numpy)
5. link_graph.py                  — inbound graph, broken links, orphans
6. ko_staleness.py                — KO candidate list (expect ~109 + 45 LL-G artefact = context)
7. assessed_conditions_gate.py    — the 2 assessed files' Card offers
8. sitemap_audit.py               — expected to fail loud (proxy 403) = correct, not a pass
9. loop_mark_print_gate.py        — Chromium render (run only if a print finding needs it)
10. verify_commit_set.py          — used at commit time only

## Sweep categories (BEAVER) beyond instruments
- node --check every inline <script> estate-wide
- Four-surface agreement spot-check (rule 11) on a W-lesson specimen
- Co-present contradiction hunt (rule 10) — the signature defect
- Storage-key roster vs baseline; do-not-fix ledger (REGISTER B) respected
- Reduced-motion: HANDOVER open queue already scopes remaining RM as scheduled programmes — REPORT ONLY

## Triage
T1 fix now (mechanical, provably safe, record says which half is true).
T2 build+STOP (pupil-facing, assessed, type changes, layout).
T3 report only (curriculum, scheduled programmes, do-not-fix ledger).

## Commit plan
One defect class per commit: `Pass U<n>: <class> — <n files> — rollback <prev SHA>`.
Verify each at origin by a read separate from the write.
