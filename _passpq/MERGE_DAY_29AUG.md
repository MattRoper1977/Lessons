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

**Refreshed for PEQ-YEAR-2, 22 Aug 2026.** The PEQ-YEAR-1 entry below it still stands; this
section supersedes its SHAs.

| | |
|---|---|
| **Lessons base** | `63271c33` (PEQ-YEAR-1's record commit) |
| **Lessons branch** | `claude/peq-year-2` |
| **Apps base** | `a7e80737` — *Merge PEQ-L2K pin: resources.json digest moves with Lessons #145 (#19)* |
| **Apps branch** | `claude/peq-year-2` (the gate copy only) |
| **Rollback** | `git reset --hard 63271c33` (Lessons) · `git reset --hard a7e80737` (Apps) |
| **Serves from** | `main` only — no `gh-pages` among the remote heads; every workflow pins `main`; all 695 Pages deployments have run from `main` |

**New in PEQ-YEAR-2:** the four Kitchen frame pages are **in the catalogue** (`resources.json`
647 → 651, pin `de9e7c615153` → moved, both gate copies together); `resources.json` line 6109 no
longer contradicts the page it indexes; the autumn block boundaries match the **evidenced 15
teaching weeks**; spring and summer are labelled **assumptions** on the page; the AQA UAS codes
are recorded as an **unverified centre record awaiting confirmation** with the surface count
re-measured (25 → 60); and the measured-vs-ruled provenance for 4.667 h/wk now travels to the
handover and the year map, both gated.

**Also live: the year map re-anchored on the derived weekly rate.** `WEEKLY_MIN` 210 → **280**
(7 timetabled 40-minute periods = 4.667 h/wk), following the owner ruling of 22 Aug that all six
carryable slots bank guided hours to PEQ. Consequences, all regenerated and gate-proven:
**all three lanes now target the full Certificate** (Award W14 → Extended W26 → Certificate
W38); the **co-delivery claim is withdrawn** on every lane (was E3 7 h, L1 2 h); and 37–57 hours
a lane are declared as QA/consolidation, never claimed against a unit. Also live: the
registration-contingent hedge strings rewritten across the estate,
`_passpq/DERIVATION_YEAR1.md`, `_passpq/PROPOSED_YEAR1.md`, `_passpq/DECISIONS_YEAR1.md` and
`_passpq/tools/year1_derive.py`.

**Explicitly NOT live** — and none of it is waiting on the 29th:

- Any cooking content. No recipe, menu, dish or ingredient was generated; `food_gate.py` proves it.
- Any change to `WEEKS = 38`, which remains unsourced, or to the spring/summer calendar, which
  the repo does not contain. Logged as `PROPOSED_YEAR1.md` P3/P4.
- Fixes to GROW's empty ASDAN planner row or LAUNCH's inconsistent weekly planners (P5).
- `resources.json`. **Untouched by design** — see §4.
- The SL and SBX branches. Measured below, merged nowhere.

---

## 2 · SL and SBX — re-measured 22 Aug, and left alone

**Both counts are unchanged from the PEQ-YEAR-1 read: SL 12 ahead / 7 conflicted files; SBX 5
ahead / 8 conflicted files.** `origin/main` moved `2a8f9f5` → `63271c33` (the eight PEQ-YEAR-1
commits), and PEQ-YEAR-1 happened to work in a corner of the estate disjoint from both branches,
so no conflict set grew.

The clone was **not** shallow this time (`git rev-parse --is-shallow-repository` → `false`, no
`.git/shallow`, 1395 commits on `origin/main`), and both `git merge-base` calls exited 0 — so the
behind-counts (911 and 902) are real, not the degenerate "every commit on each side" the shallow
trap produces.

| branch | SHA | behind / ahead | conflicted files | ancestor of main? |
|---|---|---|---|---|
| `pass-sl-sow-launch` | `2a1cfdad` | 911 / **12** | **7** | no |
| `pass-sbx-art-a2` | `462cfa6a` | 902 / **5** | **8** | no |

### What is actually left in each — checked against main, not assumed

**SBX is superseded, and its headline change is a rejected regression.** Main's own
`Art_Teesside/HANDOVER.md:25` rules SBX's C1 (Bronze → Explore on the seven BUILD A2 decks) a
**REGRESSION**, confirmed on two independent signals: Matt's design record (Autumn 2 is Bronze
across two terms) and the deployed printable pack's own badges. *"Both say Bronze; SBX's Explore
matches neither."* Verified again this pass directly against main — the A2 decks carry **Bronze
only, zero occurrences of Explore**, and all **seven** A2 lessons are in the catalogue
(`art-tees-build-a2-w1` … `-w7`). C2 and C3 were done identically by R1 (sow-strips
byte-identical to SBX's) and C5's catalogue entries are already present with richer descriptions.
**Merging SBX would reintroduce known-bad content into seven live pupil-facing decks.**
`HANDOVER.md:29`: *"`pass-sbx-art-a2` is superseded; its deletion is Matt's."*

**SL's residue is a proposal, not a fix.** Its Art re-align (relabelling LAUNCH Art W2/W4 to
"Arts Aut 2" and W5–W8 to Unit 2 Spring/Summer) lives in `_passsl/ART_REALIGN_PROPOSAL.md` and is
**Matt's to accept or reject** — it was never ruled in. SL's one operationally valuable artefact,
the LAUNCH KS4 workbook, was already lifted off the branch and landed on main by pass SCA-1, and
main's copy has since been edited past SL's — which is why the merge shows a binary `add/add`
conflict on it. **Merging SL would regress a file main has moved past.**

### The estate's own record, unchanged

`_sixclose/LEDGER.md:442` — *"Never-merge list intact: `pass-sl-sow-launch` at `2a1cfda` … and
`pass-sbx-art-a2` at `462cfa6`. Neither merged."* Both SHAs still match.
`_close/OPEN_ITEMS.md:40-42` files them under *"Remote branches WITH unique commits — do NOT
delete (real unmerged work)"*.

**This pass did not merge them and did not delete them.** Report only, as instructed.

## 3 · If nobody merges on the 29th

**Nothing breaks.** Nothing is served from either branch; nothing on main depends on either; and
on the evidence above, merging either would make the estate *worse*, not better — SBX by
reintroducing a ruled regression, SL by regressing a workbook main has already moved past.

The one thing that does decay with time is the merge itself: SBX is 902 commits behind against a
`resources.json` that has been rewritten end to end since its base, and the next pass that touches
`Art_Teesside/` or the catalogue will raise both conflict counts. If the sitting slips, the honest
recommendation is to stop treating these as mergeable branches: the surviving value is
`_passsl`/`_passsbx`'s pass records plus two *proposed* workbooks for Matt to accept or reject,
not the twelve and five commits of history around them.

**The correct action on 29 August is unchanged: do not merge, do not delete.**

## 4 · Two things that are blocked without Matt — do not wait on them

1. **The staff pack cannot be built.** `tools/build_staff_pack.py --mirror` hard-stops without
   `--logo`: *"There is no fallback to the typographic mark … a pack built without the real
   lockup is not a Progress Schools pack."* It verifies the PNG by SHA-256, and the binary is
   deliberately **not in git** (it lives on Matt's machine). Nobody can produce the pack on the
   29th, and nothing in the kitchen year needs it.
2. **`resources.json` — no longer blocked. Closed in PEQ-YEAR-2.** PEQ-YEAR-1 left this file
   untouched because `tools/pin_manifests.py` writes **both gate copies or neither** and the Apps
   checkout was unreachable from that session. This pass attached
   `MattRoper1977/Matt-s-Apps-`, so the tool ran properly:

   ```
   $ python3 tools/pin_manifests.py --apps /home/user/matt-s-apps- --lessons /home/user/Lessons
      REPINNED  …/matt-s-apps-/tools/verify_cross_estate_unification.py   resources.json: de9e7c615153 -> 907e7875d0e4
      REPINNED  …/Lessons/tools/verify_cross_estate_unification.py        resources.json: de9e7c615153 -> 907e7875d0e4
   [DONE] pins moved in 2 copy/copies; both copies byte-identical
   ```

   `apps.json` is unchanged (`a4a06b999b5f`). The four Kitchen frame pages are now **in the
   catalogue**, and `resources.json:6109` no longer contradicts the page it indexes. Both repos
   merge together — Lessons first, then Apps.

   One consequence to know for any future pass that lands here without the Apps checkout: the pin
   cannot be moved, so `resources.json` must not be edited at all. That is what PEQ-YEAR-1 did,
   and it was right.

## 5 · What the colleague can do without anybody

Everything she needs is merged and self-contained:
`GROW_ASDAN/PEQ_L2_Kitchen/COOKING_HANDOVER.md` (start here), then the week shells, criteria-by-week
and completion checklist. None of it depends on the open timetable question, the staff pack, the
catalogue registration, or either unmerged branch.
