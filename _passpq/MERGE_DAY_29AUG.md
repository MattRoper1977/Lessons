# MERGE_DAY_29AUG.md — the estate, left safe to sit

**Written for 29 August 2026, when Matt is off.** Everything below is measured, not recalled.
Commands and their real output are quoted so anyone can re-run them.

> **The short answer.** If nobody touches this repository on the 29th, **nothing breaks.**
> The estate is stable, GitHub Pages serves `main` only, and the two unmerged branches are on a
> recorded *do-not-merge, do-not-delete* list where they have sat safely since July. The
> colleague can start on the kitchen frame without Matt. §4 used to name two things that could
> not be done without him; at this pass **both are closed**, so there is nothing left to wait on.

---

## 1 · What is live at this pass's merge

**Refreshed for PEQ-YEAR-3, 22 Aug 2026.** Supersedes the YEAR-2 SHAs below it.

| | |
|---|---|
| **Lessons base** | `18aa280c` |
| **Apps base** | `93bbf98e` |
| **Branch (both)** | `claude/peq-year-3` |
| **Rollback** | `git reset --hard 18aa280c` (Lessons) · `git reset --hard 93bbf98e` (Apps) |
| **Serves from** | `main` only |

**New in PEQ-YEAR-3.** The owner supplied the real 2026-27 timetable, so the hours stopped being
inferred: `_passpq/TIMETABLE_2026-27.md` carries every guided slot with a workbook cell cited per
row. Rates are measured **per room** (Build 0 ASDAN-labelled slots, Grow 2, Launch 4; all three 8
carryable = 5.333 h/wk), reachability is stated at both the floor and the ceiling with the
unreachable named, and the **one cooking-labelled slot in the whole school** — Build Wed P5,
Science Teacher, 25.33 GLH a year — is stated with the kitchen re-sized around it as a *context*
across each lane's carryable cluster. The planner-derived band, the owner slot-ruling and the
"GROW/LAUNCH not establishable" verdict are all retired; YEAR-2's lodged GROW/LAUNCH question is
**closed by evidence**.

**The two source workbooks are EVIDENCE and are gitignored** — never committed, never
redistributed, same rule as the ASDAN instruments. Their sha256 is recorded in the extract so the
work is reproducible without them.

**Spring and summer term dates are still unevidenced.** The workbooks are *weekly* timetables, not
an annual calendar — verified: zero term, half-term, Easter or INSET dates in either. Those block
lengths remain **tagged assumptions**, `_assert_calendar()` remains intact (re-proved this pass: a
planted regression to the 14-week autumn goes red), and the single lodged question stands:
*confirm term dates / teaching weeks for spring and summer 2026-27.*

**The AQA UAS wording is applied, not proposed.** Every staff-facing surface that names a UAS
unit code or unit title now reads it as an **unverified centre record awaiting confirmation** —
88 sites across 19 files, including the catalogue's 30 search descriptions, which closes the one
deferral PEQ-YEAR-2 left open. The pupil-facing half stays **PROPOSED and untouched**: that is
Matt's authoring, and the 25 Science Teesside witness sheets stay byte-pristine under OPEN_ITEMS
item 17. `_passpq/tools/uas_census.py --gate` proves both holds and both counts.

**The staff pack no longer waits on the local lockup.** The owner supplied it; the pack is Stage 2
of this pass, not a blocked line.

## 2 · SL and SBX — re-measured, and left alone (unchanged again at PEQ-YEAR-3)

**Unchanged again.** SL 12 ahead / 7 conflicted; SBX 5 ahead / 8 conflicted — the same figures
PEQ-YEAR-1 and PEQ-YEAR-2 measured. **PEQ-YEAR-3 does not merge them either, and the reason is
recorded here so nobody re-litigates it:** main's own `Art_Teesside/HANDOVER.md:25` rules SBX's
Bronze → Explore change a **REGRESSION**, confirmed on two independent signals, and the A2 decks
on main carry **Bronze only, zero "Explore"**, with all seven A2 lessons already catalogued.
**Merging SBX would reintroduce content the estate has already ruled bad into seven live
pupil-facing decks.** SL's residue is a *proposal* awaiting the owner's read, and its one valuable
artefact is already on main in a newer copy — merging it would regress that file.

The conflict sets have not grown across three passes because each pass has happened to work in a
corner of the estate disjoint from both branches. PEQ-YEAR-3 is no exception: it touches the
Kitchen frame, `_passpq/`, the claim registers and the staff-facing UAS wording — none of which
SL or SBX carry.

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

## 4 · The two old blockers — both now closed

This section listed two things nobody could do without Matt. **Neither is blocked any more.**
It is kept, rather than deleted, because the reasoning is what stops a future pass re-blocking
itself.

1. **The staff pack — unblocked at PEQ-YEAR-3.** `tools/build_staff_pack.py --mirror` hard-stops
   without `--logo`: *"There is no fallback to the typographic mark … a pack built without the
   real lockup is not a Progress Schools pack."* It verifies the image by SHA-256, and the binary
   is deliberately **not in git**. That was a genuine block for two passes. **The owner has now
   supplied the lockup**, so the pack is **Stage 2 of this pass**, not a waiting line. The rule
   that made it a block stands unchanged: no logo binary enters git, ever, and a pack without the
   real mark is not a pack.

2. **`resources.json` — unblocked at PEQ-YEAR-2, and moved again at PEQ-YEAR-3.** PEQ-YEAR-1 left
   this file untouched because `tools/pin_manifests.py` writes **both gate copies or neither**,
   and the Apps checkout was unreachable from that session. Every pass since has attached
   `MattRoper1977/Matt-s-Apps-`, so the tool has run properly:

   ```
   $ python3 tools/pin_manifests.py
      REPINNED  …/matt-s-apps-/tools/verify_cross_estate_unification.py   resources.json: 907e7875d0e4 -> 69b94dfe83af
      REPINNED  …/Lessons/tools/verify_cross_estate_unification.py        resources.json: 907e7875d0e4 -> 69b94dfe83af
   [DONE] pins moved in 2 copy/copies; both copies byte-identical
   ```

   `apps.json` is unchanged again (`a4a06b999b5f`). PEQ-YEAR-2 put the four Kitchen frame pages
   **in the catalogue** and healed `resources.json:6109`. PEQ-YEAR-3 closes the last UAS
   deferral: the catalogue's **30 `desc` sites** now carry the same claim qualifier the schemes of
   work carry, so the hub search results and the scheme-of-work cells no longer state one claim
   two ways. Both repos merge together — **Lessons first, then Apps**.

   One consequence to know for any future pass that lands here **without** the Apps checkout: the
   pin cannot be moved, so `resources.json` must not be edited at all. That is what PEQ-YEAR-1
   did, and it was right.

## 5 · What the colleague can do without anybody

Everything she needs is merged and self-contained:
`GROW_ASDAN/PEQ_L2_Kitchen/COOKING_HANDOVER.md` (start here), then the week shells, criteria-by-week
and completion checklist. None of it depends on the open timetable question, the staff pack, the
catalogue registration, or either unmerged branch.
