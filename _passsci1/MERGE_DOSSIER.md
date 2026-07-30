# Merge dossier — Science (Pass SCI) into `main`

> **SCI-3F RE-DERIVATION (2026-07-30, at ship time).** This dossier was written at close-out
> against `origin/main = e3f7212`. Under Matt's SCI-3F authorisation THIS branch is being merged
> to `main` and pushed. `origin/main` has since advanced to **`2324ddc`** (only `Games/Off_Brand.html`
> touched — off my surface). The unmerged set below is **re-derived from `git ls-remote` at `2324ddc`**
> and supersedes §1's e3f7212 table. Rollback SHA recorded in DECISIONS.md before the merge step.
>
> **Unmerged branches at `2324ddc` (ahead>0):** the estate has largely converged since close-out —
> most SoW/audit passes are now IN main. Genuinely unmerged:
>
> | Branch | tip | ahead | has `Science_Teesside/` | touches `resources.json` |
> |---|---|---|---|---|
> | **claude/sci-1-pass-science-build-b2dyew** (mine, rebased) | e9b72b3→rebased | 15 | **yes (25)** | yes (append 25) |
> | pass-sl-sow-launch | 2a1cfda | 12 | no | no |
> | pass-sbx-art-a2 | 462cfa6 | 5 | no | yes (Art entries) |
> | pass-art-a2b | 952d260 | 2 | no | no |
> | pass-u-audit | 7c4b2b4 | 1 | no | no |
> | *(all others: art-remediation, grow-sow-audit, pass-e/q-ko-triage, pass-pq-*, pass-sb/sg-sow, pass-x, pass-y, pilot/launch-hum)* | — | **0 (MERGED)** | — | — |
>
> **Load-bearing fact still holds:** NO other unmerged branch contains `Science_Teesside/` — the 25
> lessons remain unique; **zero lesson-file conflict.** The only both-sides file vs `2324ddc` is
> `resources.json`, resolved by union (my appends vs main's mid-file `featured` flags are disjoint;
> the rebase auto-unioned cleanly, 411 entries, all flags preserved). REGISTER.md: NOT touched by
> main since merge-base `2236d0b` → no conflict this pass.

---
*Historical close-out record below (derived at `e3f7212`, retained unchanged):*

**Purpose (SCI-3 §3):** make Matt's 29-Aug merge sitting boring. A document, not an action.
**Nothing here merges. Nothing pushes to `main`. No PR.** Matt merges.

Derived at close-out, not carried from any briefing. `origin/main` moved twice during this pass
(`2236d0b` → `e3f7212`); every figure below is re-derived against the current tip.

- **Current `origin/main`:** `e3f7212` ("Featured: fill the /resources/ Popular strip to 4").
- **This branch:** `claude/sci-1-pass-science-build-b2dyew`, tip `d6df2e5` (+ the SCI-3 commit).
- **My change vs main (three-dot):** 68 files — 25 `Science_Teesside/` lessons, 15 `Planning/`
  workbooks, 27 `_passsci1/` tooling, **1 `resources.json`**.

---

## 1 · The unmerged set (derived from `git ls-remote`, checked against `origin/main` = e3f7212)

16 unmerged branches. **`pass-pq-t24-learner-signature` is already MERGED** (rode in at `bc215d1`,
R-E21). The high "ahead" counts are long-lived pass histories, not conflict surface.

| Branch | tip | ahead | has `Science_Teesside/` | character |
|---|---|---|---|---|
| **claude/sci-1-pass-science-build-b2dyew** (mine) | d6df2e5 | 13 | **yes (25)** | the science suite |
| pass-sl-sow-launch (SL) | 2a1cfda | 496 | no | LAUNCH SoW — FREEZE+HANDOVER |
| pass-sg-sow-grow (SG) | dc41a56 | 489 | no | GROW SoW close-out |
| pass-sb-sow-build (SB) | 4f5c6a4 | 493 | no | BUILD SoW close-out |
| pass-sbx-art-a2 (SBX) | 462cfa6 | 498 | no | Art workbook |
| pass-pq-peq-audit (PQ) | b137a90 | 487 | no | PEQ audit |
| pass-q-careers-w7-print-fix | c481dcf | 550 | no | Careers print fix |
| pass-q-ko-triage | cd50515 | 516 | no | KO triage |
| pass-e-ko-triage | e888220 | 549 | no | KO triage (coexists w/ Q) |
| pass-u-audit | 7c4b2b4 | 485 | no | audit record |
| pass-x-instruments | 98a8dbd | 488 | no | instruments |
| pass-y-assumptions | 45f0c63 | 503 | no | REGISTER assumptions |
| art-remediation | 46d3906 | 424 | no | art |
| pass-art-a2b | 952d260 | 546 | no | art handover |
| claude/grow-sow-audit-phase-3-8tb3oz | 710c888 | 495 | no | **relabels 8 Art LAUNCH entries in `resources.json`** |
| pilot/launch-hum-w1-illuminator | 0cfd758 | 380 | no | HUM illuminator pilot |

**The load-bearing fact: no other branch contains `Science_Teesside/`.** The 25 lessons, their
folder, and the 15 `Planning/` science-row workbooks are unique to this branch — **zero lesson-file
conflict with any branch.**

## 2 · Intersection matrix (where merge day actually goes wrong)

My work shares a file with the rest of the estate in exactly **two** places; everything else is
mine alone.

| File / class | Mine | Also touched by | Conflict |
|---|---|---|---|
| `Science_Teesside/**` (25 lessons) | append (new) | **nobody** | none |
| `Planning/{BUILD,GROW,LAUNCH}/*.xlsx` (science rows) | edit 15 | **nobody** (SL/SG/SB/PQ/X checked: 0) | none |
| `_passsci1/**` (tooling) | append (new tree) | nobody (own pass tree) | none |
| **`resources.json`** | **append 25 entries (end of array)** | `main`@e3f7212 (3 `featured` flags, mid-file); `grow-sow-audit` (relabels 8 Art entries); other SoW passes likely add their own entries | **trivial — keep both** |
| **`REGISTER.md`** | append **R-G06** (end) | every close-out pass appends entries (e.g. Pass Y R-E12, R-E21) | **trivial — append both** |

## 3 · Named conflicts, in advance

- **`resources.json` — keep both.** My additions are **25 objects appended at the end of the array**;
  `main`'s `e3f7212` added `"featured": true` to 3 *existing* entries mid-file; `grow-sow-audit`
  relabels 8 *existing* Art entries. All three touch **disjoint entries**, so the resolution is the
  **union**: keep every entry, keep every field edit. A JSON array unions cleanly; the only manual
  step is deleting a stray `]`/`,` if git leaves conflict markers. **Post-resolve invariant:** the 25
  `sci-tees-*` ids present and unique, and every `featured` flag preserved. (Live proof it is trivial:
  `e3f7212`'s edit does not touch my appended block at all.)
- **`REGISTER.md` — append both, never reorder.** Every pass appends `R-*` entries at the tail; my
  R-G06 is one more. Conflicts here are always tail-append collisions — take both blocks, in either
  order. Never renumber or reorder existing entries (R-G03's own lesson).
- **Nothing else conflicts with my branch.** Branch-vs-branch conflicts among SL/SG/SB/SBX/PQ/etc.
  are *their* business and out of this dossier's scope — but note they will collide with each other on
  `resources.json` and `REGISTER.md` by the same union/append policy.

## 4 · Conflict policy per file class (write it before the time pressure)

| Class | Policy |
|---|---|
| `_pass*/` trees, `REGISTER.md`, `INSTRUMENTS.md`, `_close/` | **append, never reorder.** Take both sides' new blocks. |
| `resources.json`, other catalogues/indexes | **union of entries.** Keep all; then re-derive (see §5). |
| Lesson HTML | **resolve by measurement, not replay** — re-render from the committed spec and gate; never hand-merge generated HTML. (Not needed here: no lesson-file overlap.) |
| Planner `.xlsx` | mine only; take mine. |
| Protected blobs (2× `★ ASSESSED LESSON`, Art W8 "Silver" ×24) | **assert byte-identical** post-merge; if changed, STOP. |

## 5 · Post-merge assertion set (a gate that passed on a branch has NOT passed on the merge)

Run against **merged `main`**, not against this branch:

1. **All lesson gates** on the 25 science files *from their merged path*: `node --check` every inline
   script · jsdom boot clean · tag balance + `</html>` · print sections by derivation (15/11/4-named)
   · witness in all 3 tier packs by render · zero exit answers on any print surface · reduced motion
   classified, icon+word survives · LL-INST-09 green all tiers.
2. **Contact-sheet render assertions** (`build_contact_sheet.py`): 25/25, 0 clips, 0 label overlaps,
   no blank/overflow print p1. (Catches a merge that corrupted a lesson's markup.)
3. **Sentinel, re-derived on the merged tree, universe stated** (`sentinel.py`): tracked `*.html`,
   `_passsci1/` excluded. Expect **main's count + 25** with the 25 as the file-list delta. Today
   main = 45, so a clean merge of this branch alone = **70**; if SL/SG/etc. merge first, re-derive —
   do not predict (R-G06).
4. **Hub reachability on merged `resources.json`**: the `Science · Teesside` chip count equals the
   number the 2026-27 collection returns (25). `main`'s `featured` flags do not change the science
   chip; re-derive from the hub filter, do not read a config.
5. **Cardinality:** 25 `Science_Teesside/*.html` on disk == 25 `sci-tees-*` entries, ids unique.
6. **Legacy science byte-identical** (`biology/ chemistry/ "2 Physics 10/"`) — proved against a hash
   baseline, not asserted.
7. **Protected blobs byte-identical** (the 2 assessed files, Art W8 "Silver").
8. **Staff packs rebuilt** from merged `main` (they are artefacts; a merge invalidates the zips).

## 6 · Rollback SHAs (recorded before the step, not after)

- **Before merging this branch:** roll back to **`e3f7212`** (current `origin/main`). Recorded now.
- **Branch tip to merge:** `d6df2e5` (+ the SCI-3 commit; use the pushed tip at merge time).
- If merging several branches in sequence, record each step's pre-merge `main` SHA **before** that
  step. The dossier cannot pre-compute those — main's tip after each prior merge is only known then.

---

*Derived SCI-3, 2026-07-29. Do not merge. Matt merges.*
