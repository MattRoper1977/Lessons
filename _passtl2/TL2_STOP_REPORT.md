# TL-2 — STOP REPORT: what landed, what is held, and why

Pass TL-2 / PR-1, 18 August 2026. Sentinel TOP `townlife-tl2-2026-08-18-TOP` ·
BOTTOM `townlife-tl2-2026-08-18-BOTTOM`.

| Part | Status |
|---|---|
| **A — Washworks rename + 1.0.1 → 1.0.2** | **COMPLETE and gated.** 30/30 runtime checks passed. See `PART_A_REPORT.md`. |
| **B — publish Town Life** | **STOPPED at B4.** Decision **D2** (pupil surface) is unanswered. |
| **C — PROTOCOL de-brand** | **STOPPED at C2.** Decision **P1** (does the geometry change?) is unanswered. C0 pins and the C1 census were reproduced first; nothing was edited. |

Parts A and B were kept uncoupled from C as §0 requires, so A landing does not depend on C.

## Why B and C stopped

No swap lines or decision answers were supplied with the prompt. Both gates are explicit and doubled:

- **B4** — "⚠ DECISION D2 — THE PUPIL SURFACE. **STOP HERE IF UNANSWERED**" … "Do not proceed past B4
  on inference. This is Matt's call." §6 lists "D2 is unanswered" as a stop condition.
- **C2** — "⚠ **HARD STOP** — DECISION P1" … "it cannot be inferred." §6 lists "P1 is unanswered".

Both sections state a *default* (Town Life appears on `/for/pupils/` like every other game; PROTOCOL
gets original layouts). I read those as recommendations **to Matt**, not as authorisation for me to
proceed — because each is paired with an explicit unanswered-means-stop condition, and because the
substance is not mine to settle: D2 puts a game containing a bank-vault role on the children's
homepage automatically, and P1 decides whether Part C is a relabelling or a rebuild.

## Nothing was published

- No entry was added to `games.json` in either repo. No genre record was touched. No route was created.
- Neither the Games repo nor the site repo was modified in any way by this pass.
- **The shelf count is unchanged at 52.**

## Part B — the baseline, derived not pinned (§B1/§B3)

| Measure | Value |
|---|---|
| Manifest entries today | **52** |
| site-served / Lessons-hosted | **23 / 29** — matches the prompt's stated baseline exactly |
| Games-repo manifest vs site mirror | **byte-identical as JSON** — no drift; "one manifest writer" is satisfiable |
| `townlife` / `protocol` present | no / no |
| Would become, with Town Life | **24 + 29 = 53** |
| Would become, with both | **25 + 29 = 54** |

**Discrepancy in the prompt's own premise:** §B2 names the canonical manifest
`_shelf/games.json` in the Games repo. **There is no `_shelf/` directory in that repo.** The manifest is
`games.json` at the repository root, mirrored at `data/source-manifests/games.json` in the site repo.
Whoever executes Part B should use those paths; a literal `_shelf/games.json` write would create a
second manifest, which is exactly the duplicate-source-of-truth failure this arc has been removing.

## Part C — pins and census done, geometry untouched

C0-1…C0-5 all pass. The C1 census reproduces: all ten roster tokens exact, all four role names exact,
runtime Ascent 7 / Haven 4, docs Ascent 17 / Haven 1 / Riot 3 / VALORANT 1, all 15 callouts, all three
blueprint titles. Details and two counting-method corrections in `C1_CENSUS.md`, including one
substantive fix: **there are no JavaScript `.bind()` calls at all** — the 13 `bind` hits are 3
`tabindex`, 6 `bindSetting`, and 4 map tokens, so the blind-replace hazard is larger and different from
the one the prompt describes.

The package already claims original geometry in two docs while shipping publisher map names, callouts
and a fan-content disclaimer. That tension is the P1 question and is recorded, not resolved.

## OPEN_ITEMS 52 — the accident §0 warned about did NOT happen, and not because it was avoided

§A0-2 asks the close report to state that the site provenance gate is green at this tip by self-heal
rather than repair. **That line does not apply to this pass, because the self-heal never occurred.**
Stated accurately:

> Part B was the push that would have touched a served file and incidentally turned the site's
> provenance gate green. **Part B stopped at B4, so no site push happened.** The gate therefore remains
> exactly as PH-3 left it — red at site commit `4b74945`, on witness `asdan/_ph3/JOB_C_REPORT.md`
> returning HTTP 404 because Jekyll never publishes underscore-prefixed directories.
> **OPEN_ITEMS 52 remains open and its three options remain Matt's to choose.** When Part B does land,
> the gate will go green by self-heal, not by repair — and that green must not be read as the defect
> being fixed.

Compliance with the other two guards: **A0-1** — `asdan/_ph3/JOB_C_REPORT.md` was not deleted, renamed,
moved or `include:`d; it was not touched at all. **A0-3** — no workflow file in any repo was modified.

## What unblocks each part

**Part B** needs one line:
- `Town Life is adult-shelf only — go` → per B4 I must then **stop and report** rather than improvise a
  mechanism, because a declared exclusion needs a gated field and inventing one mid-pass creates a
  sixth taxonomy source; or
- an explicit confirmation of the default (Town Life appears on `/for/pupils/` like every other game).

Optional Part B swaps, defaults noted: NEW marker **ON**; genre **Sandbox & Creative**; feel tags
**long-haul + thinky**.

**Part C** needs P1:
- `PROTOCOL gets original layouts — go` (confirms default P1-A) — the geometry becomes authored work and
  is the bulk of Part C. Per §C2 I will stop and say so if three layouts cannot be authored to the
  standard of the existing ones rather than degrading the tool to one map; or
- `PROTOCOL keeps the geometry — go` (selects P1-B) — the disclaimer **stays**, and the build does not go
  on a pupil surface, which makes the "available for kids" half of the instruction unreachable.

Optional Part C swaps, defaults noted: Live Sync **OFF** on the released build; keep the persisted
`spike` save field and map it at the boundary; genre **Strategy & Puzzle**.

## Human items still outstanding (§5)

1. Matt's phone tap on live `/townlife/` — the only real touch proof, and the deployed-origin half of D3.
2. **Chromebook check before any pupil use** — throttled proxies measured 5.17–7.11 fps at 6×. Not optional.
3. Eyes on the 17 renamed strings in context — they are a proposal on voice.
4. **D2 and P1** — both blocking, above.
5. PROTOCOL callsigns and layout names — not authored, because P1 is unanswered.
6. PROTOCOL phone tap on live `/protocol/` — not reachable this pass.
