# SCA-1 — MERGE record

| | |
|---|---|
| BASE_SHA / ROLLBACK_SHA | `72778591e8c1fe1d9c5b979c90ccbbd868de4b3a` |
| Branch | `claude/sca-1-science-correctness` |
| PR | [#136](https://github.com/MattRoper1977/Lessons/pull/136) |
| Merge commit | `e9076531304696e1078b11d79e22c70a1578854a` (`--no-ff`) |
| Merged | 2026-08-19 11:39 UTC |
| Files changed | 45 (`Science_Teesside/*/v3_40min` only, plus `_sca1/`) |

## Gate table at the branch tip — all green, no RED

| gate | result | evidence |
|---|---|---|
| G1 `node --check` | PASS | 38 inline scripts, 0 failed |
| G2 boot 3 viewports (390/768/1440) | PASS | 150 runs; console-error multiset identical to baseline |
| G3 print-pack marker families | PASS | every family >= baseline in all 50 files |
| G4 PROTECTED manifest | PASS | 468 strings / 12 families byte-identical |
| G5 food census | PASS | byte-identical across all 50 files |
| G6 sentinels 50 / 123 | PASS | sorted file sets identical to baseline |
| G7 CODE-stream delta = 0 | PASS | 0 deltas across all 50 files |
| G8 diff scope | PASS | only the three `v3_40min` folders + `_sca1/` |
| G9 LAUNCH no mark-scheme | PASS | 0 on any pupil/print surface (context-read) |
| G10 WRONG dispositioned | PASS | 37 claims: 18 fixed w/ SHAs, 19 recorded or refuted |

## Post-merge verification

**Sentinels re-derived at `e907653`** (universe: git-tracked `*.html`, 778 files):

- `ll-g:loop-mark` -> **50 files**, sorted set identical to baseline
- `What I said, and what it changed` -> **123 files**, sorted set identical to baseline

**Pages** — run `32248672856` on `e9076531`, all three jobs **success**:
`build` 11:39:42->11:40:21 · `deploy` ("Deploy to GitHub Pages") 11:40:25->11:40:35 ·
`report-build-status` success.

**Raw-pin, one changed lesson per pathway** at the merge SHA — all HTTP 200, fix visible,
superseded string gone:

| lesson | HTTP | fix present | old string gone |
|---|---|---|---|
| `SCI_B_W4A_Muscles_Explore.html` | 200 | "string or yarn" x2 | "elastic" gone |
| `SCI_G_W6B_Earth_And_Planets_Do.html` | 200 | "Neptune sits about 3.5 km away" | "1.2 km" gone |
| `SCI_L_W4L1_Diffusion_Introduce.html` | 200 | "a more crowded area and a less crowded one" x2 | "empty one" gone |

## Caveats recorded at merge

- The **live Pages URL could not be fetched from this environment** — `mattroper1977.github.io`
  is blocked by the agent egress proxy (HTTP 000; `raw.githubusercontent.com` returns 200 from
  the same shell). Deployment is evidenced by the Pages `deploy` job succeeding and by the
  raw-pin above, not by a live GET. Worth a phone check.
- **`Watch main — a red nobody is told about is a red nobody has`** was already failing at
  BASE_SHA `7277859` (three consecutive failures at 07:06, 07:08, 07:32 on the pre-merge SHA).
  It is not caused by this pass.
- **Edexcel 1BI0 spec UNVERIFIED** — `qualifications.pearson.com` is blocked by the same proxy,
  so LAUNCH alignment is SoW-rows-only per section 6.
- **LAUNCH SoW came off unmerged branch** `origin/pass-sl-sow-launch` @ `2a1cfdad`.
  Recommend committing it to `_passsl/inputs/` on main.

## Rollback

`git revert -m 1 e9076531304696e1078b11d79e22c70a1578854a`, or reset to
`72778591e8c1fe1d9c5b979c90ccbbd868de4b3a`.
