# Merge dossier — Science (Pass SCI) into `main`

> **SCI-3F STAMP — re-derived AFTER the ship, at merged `main = 2ce19ce` (2026-07-30).**
> This dossier was first written at close-out against `origin/main = e3f7212`, then re-derived at
> `2324ddc` pre-merge; the SCI-3F ship then advanced `main` to **`2ce19ce`**, which makes any
> pre-merge unmerged-set table false the moment it is read (the "stamp that couldn't be true when
> written" family — R-G03/R-E12). This block is the authoritative one and is stamped at the tip it
> describes.
>
> - **Stamp SHA (describes THIS `main`):** `2ce19ce`.
> - **Pre-SCI-3F rollback SHA (recorded here, not only in DECISIONS.md):** **`2324ddc`**
>   ("Off-Brand v3.1.2…"). Undo the ship with `git push --force-with-lease origin 2324ddc:main`.
> - **Derivation command (re-runnable):**
>   `for b in $(git ls-remote --heads origin | sed 's#.*refs/heads/##'); do echo "$b $(git rev-list --count origin/main..origin/$b) $(git ls-tree -r --name-only origin/$b | grep -c '^Science_Teesside/')"; done`
>
> **Unmerged branches at `2ce19ce` (ahead > 0):**
>
> | Branch | tip | ahead vs 2ce19ce | has `Science_Teesside/` | touches `resources.json` |
> |---|---|---|---|---|
> | claude/sci-1-pass-science-build-b2dyew (mine) | e9b72b3 | 15* | yes (25) | yes |
> | pass-sl-sow-launch | 2a1cfda | 12 | no | no |
> | pass-sbx-art-a2 | 462cfa6 | 5 | no | **yes (Art entries)** |
> | pass-art-a2b | 952d260 | 2 | no | no |
> | pass-u-audit | 7c4b2b4 | 1 | no | no |
> | *(art-remediation, grow-sow-audit, pass-e/q-ko-triage, pass-pq-*, pass-sb/sg-sow, pass-x, pass-y, pilot/launch-hum)* | — | 0 (MERGED) | — | — |
>
> **\* My own branch is CONTENT-MERGED, ref superseded.** The 25 lessons on `e9b72b3` are
> byte-identical in `2ce19ce` (0 differing); the "ahead 15" is only because the SCI-3F rebase gave
> the commits new SHAs, so the old ref is not an ancestor. Nothing on it needs merging on 29 Aug —
> it can be deleted in the UI (Matt deletes branches, not this pass).
>
> **Post-merge overlap matrix (my new main ∩ each parked branch's changed paths):**
> `pass-sl-sow-launch` 12 ahead → **0** overlap · `pass-sbx-art-a2` 5 ahead → **`resources.json` only**
> (0 sci-tees lines; 37 disjoint Art lines) · `pass-art-a2b` 2 ahead → **0** · `pass-u-audit` 1 ahead → **0**.
> NO other unmerged branch contains `Science_Teesside/` — the 25 lessons stay unique.
>
> **GUARANTEED 29-Aug conflict — `resources.json` on the `pass-sbx-art-a2` merge (policy, explicit):**
> That branch adds Art entries to the same `resources.json` this ship already extended with 25
> `sci-tees` objects. The conflict is now certain. Resolution:
> 1. **Union both sides** — keep every entry from main and every entry sbx-art-a2 adds; the two edit
>    disjoint regions (my sci block at the array tail, its Art entries elsewhere).
> 2. **Re-validate JSON** — `python3 -c "import json;json.load(open('resources.json'))"` must pass.
> 3. **Assert entry count == main_count + sbx_added − duplicates** (there should be 0 duplicate ids;
>    if any, the union kept one — investigate before committing).
> 4. **Assert all 25 `sci-tees` ids survive** — `grep -c '"id": "sci-tees' == 25`, ids unique — and
>    every `featured` flag main carries (4) is preserved.

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
3. **Sentinel, re-derived on the merged tree, universe stated** (`sentinel.py`): tracked `*.html`
   **CONTAINING `ll-g:loop-mark`** (NOT raw `git ls-files '*.html'`, which is ~459 and is context
   only), `_passsci1/` excluded. Expect **main's loop-mark count + 25** with the 25 as the file-list
   delta. Today main = 45, so a clean merge of this branch alone = **70**; if SL/SG/etc. merge first,
   re-derive — do not predict (R-G06). [SCI-3F verified: 45→70 at the merge boundary.]
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
