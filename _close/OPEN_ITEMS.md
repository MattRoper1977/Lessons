# OPEN ITEMS — season close (2026-07-29), at main `8540eee`

Derived **only** from committed records at the landed tip. Nothing invented. Each item cites its source.

| # | open item | status / blocker | recorded in |
|--:|---|---|---|
| 1 | **T2-4 learner-signature** row on ASDAN print packs | awaits Matt's one-line spec (September) | `REGISTER.md` R-RL01 ("EXCLUDED, untouched (await committed spec / Matt): … T2-4 learner-signature") |
| 2 | **T2-2 / T2-3 unit codes** ("Delivering a Project" → real GROW GCOMM/ENT unit codes) | blocked — the referenced PEQ unit is NONEXISTENT; needs the committed ASDAN unit spec (the ASDAN PDFs) | `_passpq/FINDINGS.md` §T2-2; `REGISTER.md` R-RL01 |
| 3 | **Slideshows S/S/S tiering rebuild** (Supported/Standard/Stretch) | deferred to its own lettered pass | `REGISTER.md` R-RL01 ("… Slideshows tiering rebuild") |
| 4 | **BUILD SoW workbook adoption** | vB (FoodWise-only) is the live instrument audited; vA archived/superseded; workbook-side items are Matt's file, outside repo scope, no patches | `_passsb/FINDINGS.md` §R4 "WORKBOOK-SIDE items" and §3. **Note:** the season-close brief's phrase *"workbook vC-PROPOSED"* does **not** appear in any committed record — the records name **vA (archived)** and **vB (live)** only; corrected here per "invent nothing." |
| 5 | **Discover & Explore adviser training** | required before Arts Award **Explore** can run at BUILD; a scheme/booking decision (human lead time), Matt's call, not a defect | `_passsb/FINDINGS.md` (l.228, l.324) |
| 6 | **Assessed residue — `GROW_HUM_W7` `Evaluation clause` KO row** | **AWAITING-WORD** (S4): pupil-rendered `<td>`, so not auto-committable; proposed hunk held verbatim, `GROW_HUM_W7` untouched | `_passe/ASSESSED_RESIDUE_HELD.md` (season-close S4) |

## Surviving remote branches with ZERO unique commits vs `main` — safe for Matt's UI deletion
Enumerated by `git rev-list --count origin/main..origin/<branch>` at `8540eee` (0 = fully merged / no unique work):

- `art-remediation`
- `claude/grow-sow-audit-phase-3-8tb3oz`
- `pass-e-ko-triage`  *(Pass E held snapshot; its content landed via `pass-e-land`; API delete returned 403)*
- `pass-pq-peq-audit`
- `pass-q-careers-w7-print-fix`
- `pass-q-ko-triage`
- `pass-sb-sow-build`
- `pass-sg-sow-grow`
- `pass-x-instruments`
- `pass-y-assumptions`
- `pilot/launch-hum-w1-illuminator`

## Remote branches WITH unique commits — do NOT delete (real unmerged work)
- `pass-sl-sow-launch` — **12** unique commits
- `pass-sbx-art-a2` — **5** unique commits *(the SBX C1 Bronze→Explore work — NOT-LANDED, see S2)*
- `pass-art-a2b` — **2** unique commits
- `pass-u-audit` — **1** unique commit
