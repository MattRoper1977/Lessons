# MERGE_DAY_29AUG.md — the estate, left safe to sit

**Written for 29 August 2026, when Matt is off.** Everything below is measured, not recalled.
Commands and their real output are quoted so anyone can re-run them.

> **The short answer.** If nobody touches this repository on the 29th, **nothing breaks.**
> The estate is stable, GitHub Pages serves `main` only, and the two unmerged branches are on a
> recorded *do-not-merge, do-not-delete* list where they have sat safely since July. The
> colleague can start on the kitchen frame without Matt. There is one build that genuinely
> cannot run without him, named in §4, and nobody should wait on it.

---

## 1 · What is live at this pass's merge

| | |
|---|---|
| Base | `2a8f9f5` — *Merge PEQ-L2K close: P9 lodged (#146)* |
| Branch | `claude/new-session-yed8ua` |
| Rollback | `git reset --hard 2a8f9f56344f323436b86558e0aee51839657262` |
| Serves from | `main` only — there is no `gh-pages` branch among the 162 remote heads, and every workflow pins `ref: main` |

**Live after this merge** — new, teacher-facing, print-first, all under `GROW_ASDAN/PEQ_L2_Kitchen/`:

- `COOKING_HANDOVER.md` + `Cooking_Handover.html` — the colleague's frame
- `Kitchen_Week_Shell.html` — 38 pre-filled week pages with an empty cooking box
- `Criteria_By_Week.html` — the coverage matrix inverted by week
- `Kitchen_Completion_Checklist.html` — the weekly tick sheet

**Also live:** the year map's hours paragraph and sensitivity table, re-based onto the measured
40-minute period and with **no row marked live** (`Scheme_of_Work.html`); the
registration-contingent hedge strings rewritten across the estate; `_passpq/DERIVATION_YEAR1.md`
and `_passpq/tools/year1_derive.py`.

**Explicitly NOT live** — and none of it is waiting on the 29th:

- Any cooking content. No recipe, menu, dish or ingredient was generated; `food_gate.py` proves it.
- Any re-anchored year map. §1 stopped rather than guess a timetable — see `DERIVATION_YEAR1.md`.
- `resources.json`. **Untouched by design** — see §4.
- The SL and SBX branches. Measured below, merged nowhere.

---

## 2 · SL and SBX — measured, and left alone

Measured on an **unshallowed** clone. This matters: the clone arrives shallow, and on a truncated
graph `git merge-base` exits 1, which makes `A...B` silently degenerate into "every commit on
each side" and produces garbage ahead/behind counts. `git fetch --unshallow` first, or do not
believe the numbers.

### `pass-sl-sow-launch` — LIVE, not merged

```
git rev-parse origin/pass-sl-sow-launch        2a1cfdad9cdbc09eba538be3190b89f5e35cf6f9
git rev-list --left-right --count origin/main...origin/pass-sl-sow-launch
                                               903     12          # behind  ahead
git merge-base origin/main origin/pass-sl-sow-launch
                                               32ca685e  (2026-07-28)
git log -1 --format='%ci %s' origin/pass-sl-sow-launch
   2026-07-29  Pass SL: FREEZE + HANDOVER (12th, final) — park unmerged for 29 Aug sitting
```

25 files, +11 728 / −8. **Conflict prediction: NOT clean — 7 conflicted files.**

```
git merge-tree --write-tree --name-only origin/main origin/pass-sl-sow-launch   # exit 1
Art_Teesside/Launch/LAUNCH_ART_W2_Practice_Careers_and_Pathways.html
Art_Teesside/Launch/LAUNCH_ART_W4_Arts_Experience_Attend_Analyse_and_Share.html
Art_Teesside/Launch/LAUNCH_ART_W5_Design_the_Leadership_Project.html
Art_Teesside/Launch/LAUNCH_ART_W6_Pilot_Lead_and_Adapt.html
Art_Teesside/Launch/LAUNCH_ART_W7_Deliver_and_Curate_the_Arts_Project.html
Art_Teesside/Launch/LAUNCH_ART_W8_Review_Influence_and_Portfolio_Audit.html
_passsl/inputs/LAUNCH KS4 - 2026-27.xlsx          CONFLICT (add/add)
```

The `add/add` on the workbook is explained and is the important part: **main already carries that
workbook**, landed independently by pass SCA-1 (`7208b3d6`, `a946f1ce`), and has since edited it.
Main's blob is `080360e3` (111 721 bytes); SL's is `73b9de37` (115 585). **Merging SL would
regress a file main has moved past.** Only SL's *analysis outputs* are genuinely unmerged.

### `pass-sbx-art-a2` — LIVE, not merged

```
git rev-parse origin/pass-sbx-art-a2           462cfa6af0733f92fbeba00d635b6db9cdae30c7
git rev-list --left-right --count origin/main...origin/pass-sbx-art-a2
                                               894     5
git merge-base origin/main origin/pass-sbx-art-a2
                                               4f5c6a4e   (= pass-sb-sow-build tip)
git log -1 --format='%ci %s' origin/pass-sbx-art-a2
   2026-07-28  Pass SBX §4: workbook vC-PROPOSED + change table + C4 SC proposals
```

11 files, +199 / −7. **Conflict prediction: NOT clean — 8 conflicted files** (all seven BUILD Art
decks plus `resources.json`).

Main's own `Art_Teesside/HANDOVER.md:29` already adjudicates this branch: *"SBX reconciliation —
nothing to re-land; C1 rejected."* It records that C2 and C3 were done identically by R1
(byte-identical sow-strips), that C5's `resources.json` entries are already present with richer
descriptions, and that **C1 is rejected as a regression**. SBX's decks additionally carry
pre-remediation `pull` language its base predates. **Merging it would reintroduce known-bad
content into seven live decks.**

### Already absorbed — nothing to do

| branch | SHA | ahead |
|---|---|---|
| `pass-sb-sow-build` | `4f5c6a4e` | **0** |
| `pass-sg-sow-grow` | `dc41a560` | **0** |

Note `_passsb/` on main is **SB**, not SBX — SBX writes to `_passsbx/`, which does not exist on
main at all.

### The estate's own record agrees

- `_sixclose/LEDGER.md:442` — *"Never-merge list intact: `pass-sl-sow-launch` at `2a1cfda` … and `pass-sbx-art-a2` at `462cfa6`. Neither merged."* Both SHAs match the measurement exactly.
- `_close/OPEN_ITEMS.md:40-42` — filed under *"Remote branches WITH unique commits — do NOT delete (real unmerged work)"*: SL 12 commits, SBX 5. Counts match.
- `REGISTER.md:1475` — where those branches overlap this estate it is on `resources.json` and `REGISTER.md` only, *"both append-only-union: at the sitting keep both sides, never reorder."*

**This pass did not merge them and did not delete them.** Report only, as instructed.

---

## 3 · If nobody merges on the 29th

**Nothing breaks.** Stated plainly because the honest answer is the reassuring one:

- **Nothing is served from them.** Pages builds from `main`; neither branch is deployed to anyone.
- **Nothing on main depends on them.** No live file references `_passsbx/` (absent from main
  entirely); the `_passsl/` references on main are backward-looking provenance notes in closed
  records; neither pass directory contains a single servable `.html`.
- **SL's one operationally valuable artefact is already on main** — and main's copy is newer.
  Merging would regress it.
- **SBX is worse than unnecessary** — main's own handover records C1 as a rejected regression.
- **Both merges are non-trivial** — 7 and 8 conflicted files, all live lesson decks plus the
  append-only-union `resources.json`. A rushed merge on a day Matt is away carries real risk and
  delivers no benefit.

The only genuinely open residue is **decision-shaped, not code-shaped**: two *proposed* workbooks
(`_passsbx/proposed/Build SOW 2026-2027 vC-PROPOSED.xlsx` and SL's `ART_REALIGN_PROPOSAL.md`) for
Matt to accept or reject at his leisure. They lose nothing by sitting.

**The correct action on 29 August is: do not merge, do not delete.** Both branches are on the
recorded do-not-delete list precisely so the history stays auditable while staying out of `main`.

---

## 4 · Two things that are blocked without Matt — do not wait on them

1. **The staff pack cannot be built.** `tools/build_staff_pack.py --mirror` hard-stops without
   `--logo`: *"There is no fallback to the typographic mark … a pack built without the real
   lockup is not a Progress Schools pack."* It verifies the PNG by SHA-256, and the binary is
   deliberately **not in git** (it lives on Matt's machine). Nobody can produce the pack on the
   29th, and nothing in the kitchen year needs it.
2. **`resources.json` cannot be re-pinned, so this pass did not touch it.** Its SHA is pinned
   inside `tools/verify_cross_estate_unification.py`, and `tools/pin_manifests.py` writes **both
   gate copies or neither** — Lessons *and* Apps. The Apps checkout is not reachable from this
   session:
   ```
   $ python3 tools/pin_manifests.py --check
   manifests:
      MISSING apps.json (no owning checkout found)      # exit 1
   ```
   The current pin is correct and matches on disk
   (`de9e7c61515397bae87ef3c7afadb57426afbe4fcf0f58dbe7b174cdac582374`), so the gate is green —
   and it stays green precisely because the pass left the file alone. The four new Kitchen pages
   are therefore **not registered in `resources.json`**; they are reachable from the year map and
   the handover, and print correctly, but they will not appear in the catalogue until a pass with
   both checkouts registers them and re-pins in the same commit. Logged in `PROPOSED_YEAR1.md`.

---

## 5 · What the colleague can do without anybody

Everything she needs is merged and self-contained:
`GROW_ASDAN/PEQ_L2_Kitchen/COOKING_HANDOVER.md` (start here), then the week shells, criteria-by-week
and completion checklist. None of it depends on the open timetable question, the staff pack, the
catalogue registration, or either unmerged branch.
