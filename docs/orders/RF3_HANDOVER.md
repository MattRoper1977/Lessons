# RF3 — handover

Written 2026-09-12 on budget exhaustion, mid-order. Nothing below was measured for this
document; every figure is carried from earlier in the session with its measurement time
attached. **The next session re-reads before it transacts — all of §3 has a shelf life (P5.2).**

---

## 1. BRANCH AND COMMITS

### Lessons — `claude/rf2-reconcile-recovered-scopes-7ay3e5` (pushed)

| SHA | What |
|---|---|
| `0ca690b` | LP1 §1 and PIN1 §1 censuses: both opening figures contradicted |
| `c9d6877` | RF2 readback: reconcile #350 and the board against the recovered Appendix B |
| *(this file)* | RF3 handover |

### ⚠ Site — `codex/rf1-prx1-candidate` — **COMMITTED LOCALLY, NEVER PUSHED**

**`f746d5f81118bef0b8ec5d9c2d6b8a5e888bf639`** — "PRX1 §2.2/§3.4/§4.1/§4.2: balance
assertion, tree question, DECISIONS, census"

**This is the single thing most likely to be lost.** It exists only in the container's
worktree at `/home/user/mattroper1977.github.io`, on a branch whose remote head is still
`3c11780acc391a598f1cd486206d167a8b804ad9`. If the container is reclaimed, all four §2
clauses are gone and must be redone from scratch.

Four files in that commit:

| File | State |
|---|---|
| `domain-split/structural_html.py` | modified — adds `VOID_ELEMENTS`, `_RegionBalance`, `_assert_balanced`, and one call in `replace_first_element` |
| `tools/test_structural_html.py` | modified — adds `Tree`/`tree_of`/`is_descendant` helpers and 3 tests (8 → 11) |
| `reports/prx1/DECISIONS.md` | new, 106 lines |
| `reports/prx1/SHAPE_CENSUS.md` | new, 156 lines |

**Recovery, if the container still lives:**

```
git -C /home/user/mattroper1977.github.io log --oneline -1 codex/rf1-prx1-candidate
git -C /home/user/mattroper1977.github.io push -u origin codex/rf1-prx1-candidate
```

Nothing else is staged or uncommitted in either repository. The working tree was clean at
both commits.

---

## 2. WHERE RF3 GOT TO

| Section | State | Evidence |
|---|---|---|
| §1.1 merge #351 | **DONE** | merged `30e86ad64bd1aaaf3a6887f9eb4cd4d9dbcde436`. Taken out of draft first (it was a draft). Retires UX1-A §0.1 |
| §1.2 merge #346 | **NOT STARTED** | blocked only on §1.6's "Pages deploy terminal between" — see below |
| §1.3 merge #350 | **NOT DONE** | conditional on §2, and §2.5 was not reached |
| §1.4 #291 held | **DONE (by not acting)** | untouched, no read, no comment |
| §1.5 close #91/#106/#109 | **DONE** | all three closed unmerged, each with a comment naming contents, reason and branch. All three branches verified **PRESENT** by `git ls-remote` after closing |
| §2.1 balance assertion | **DONE, UNPUSHED** | in `f746d5f`. Negative control satisfied: the new test FAILS against `3c11780a` (`ValueError not raised`), passes at `f746d5f`, 11/11 |
| §2.2 tree question | **DONE, UNPUSHED** | `test_straddling_close_tag_turns_a_sibling_into_a_descendant`, built on `html.parser` (no `lxml` — the design-audit job installs none) |
| §2.3 DECISIONS entry | **DONE, UNPUSHED** | `reports/prx1/DECISIONS.md`, D-1…D-8 |
| §2.4 §1.3 census landed | **DONE, UNPUSHED** | `reports/prx1/SHAPE_CENSUS.md`, unfixed, classified |
| §2.5 undraft + merge #350 | **NOT DONE** | |
| §3 ML1 closure record | **PARTIAL** | the closure record is written into `docs/orders/RF2_READBACK.md` §2 on the Lessons branch. §3.2's "mark the DOCUMENT stale in place" — editing `docs/MBM_LIVE_MIRROR_LEG_DEADLOCK.md` in the Site repo — was **NOT DONE** |
| §4 PIN1 §2 ruling filed | **NOT DONE** | the ruling is recorded in this handover §4 only |
| §5 figures + P5.5 | **PARTIAL** | the corrected figures are in `0ca690b`; P5.5 is articulated inside `reports/prx1/SHAPE_CENSUS.md` (unpushed) but is **not filed as a findings-ledger entry** |

**The §2 golden re-run never completed.** The balance assertion is new behaviour that can
*raise* where the old code did not, so PRX1 §2.3/§5 require re-proving 33/33 byte-identical
before #350 can ship. A launched re-run was stopped on the budget instruction. The only
evidence gathered was a local scan of **all 91 tracked `.html` files at Site main: 0 raises
for both tags** (46 header replacements, 44 main replacements, rest absent) — a strong
signal, but **not** the assembled-tree proof §3.1 requires.

---

## 3. PR AND MAIN STATE AS LAST SEEN

**All four mains, as at 2026-09-11 23:51–23:54 UTC** (unchanged from RF1's 21:45–22:00 census):

| Repo | Commit | Tree |
|---|---|---|
| mattroper1977.github.io | `1651b84c800f6cd3169a29f794b075042ee54024` → **now `30e86ad64bd1aaaf3a6887f9eb4cd4d9dbcde436`** (as at 09:00 UTC 12 Sep, after #351) | was `e4c79831afbfc29c58cb9b62d650579a5a59f6ce` |
| Lessons | `aad04718c11a2396ecf323a662f55bf0e0c2441b` | `fa21544faa79f3efea25f9d58e68dc8c8c1ec28c` |
| Matt-s-Apps- | `4cb8a634dbeaa3d98d7699252fdfff4253c47eef` | `a07ef2b907377fbe50f914c632afb84314e5dfdf` |
| Games | `809b6c9a65f175cd48182e793bee166ad4f6bd3f` | `3477eb8565ae0138ef1f741611f27891136d0595` |

**Site open PRs, as at 09:07 UTC 12 Sep** (was 7, now 3):

| PR | State |
|---|---|
| #350 | open, **still draft**, head `3c11780a…` remote. Remote does **not** carry `f746d5f` |
| #346 | open, not draft, head `d28cb836…`, base `85e3e020` (35 behind), 0 of 5 failing — **next to merge** |
| #291 | open, draft, **HELD**, untouched |
| #351 | **merged** `30e86ad6…` |
| #91 / #106 / #109 | **closed unmerged**, branches preserved |

**Lessons open PRs: 8, as at 00:31 UTC 12 Sep** — #497, #493, #465, #456 (held), #118, #116,
#45, #43. Every head unchanged from RF1's census.

**Pages deploy after #351, as at 09:07 UTC:** the docs-only merge *did* trigger a
publication — **Education publication** run `34684701623` — which is F7 in action (a workflow
with no path filter makes every merge a publication). 20 runs total on `30e86ad6`, **1 still
pending** ("Maker splash canon and application") when the session stopped. §1.6 requires that
terminal before #346 merges. **Re-read it; do not assume it finished.**

---

## 4. THE RULINGS IN FORCE — carried verbatim

- **BL1 order approved:** #351 → #346 → #350 conditional; #291 held; #91/#106/#109 closed
  unmerged with branches PRESERVED and a comment naming contents and reason.
- **PRX1 ambiguity:** the **NESTING** reading is authoritative. 0 nested, 2 pages with >1
  `</main>`, neither in a target set. No stop fires. Both numbers go in the DECISIONS entry.
- **PRX1 ceiling:** lifted ONCE for exactly four named clauses. A fifth item is a STOP.
- **PIN1 §2:** `ux2-gates.yml` has no registry, so PIN1 §2.2 applies — a scheduled census
  reporting drift, that gate ALONE, UNMEASURED never green, never widen to `**`.
- **ML1:** CLOSED-BY-DL. The deadlock document is stale in place — do not repair or delete it.

---

## 5. CORRECTED FIGURES, WITH THEIR MEASUREMENT

Both measured **2026-09-12 00:34–00:46 UTC**, read-only, across all 97 workflow files in the
four repos and the gate source at Lessons main `aad04718`.

- **Live proofs: 18**, not the carried 13 — Site 9, Lessons 4, Apps 4, Games 1; **16** if
  `maker-splash-canon-verify.yml`'s three separately gated steps collapse to one. Contradicted
  on Site, Lessons and Apps; confirmed on Games. **Plus 21 further live proofs in workflows
  with no `pull_request` trigger at all** — those produce *no* PR check rather than a green
  one, a different and quieter defect class, reported separately and **not** folded into the 18.
- **Pins: 444** distinct pinned paths (443 excluding the publisher-caller pin) across five
  registries in `tools/verify_cross_estate_unification.py`, not the carried 89. **Only ONE
  gate asserts any pin digest** (`mbm-cross-estate-unification.yml:101`) — PIN1 §0.1's "two
  gates" premise is contradicted. **Provenance of 89 is NOT LOCATED**: it matches no registry,
  no sum of registries, and no historical `CATALOGUE_PINS` size, including at #499's own head
  and base where the set was already 435.
- **P5.5 — A CARRIED FIGURE ACQUIRES AUTHORITY BY REPETITION.** Every order quoting a count
  cites the measurement that produced it, or states it is unverified. The §1.3 census is its
  own illustration: RF1 carried **133**, an RF2 pass measured **137**, this session measured
  **129** — three methods, three numbers, none previously recorded with its method.

---

## 6. STANDING LIMITS THE NEXT SESSION INHERITS

No check weakened, ever. Lessons #456 held. **Games #78/#79 are their owner's — and are
distinct from Apps #78/#79** (Games: two open, bot-opened, both `mergeable_state: blocked`;
Apps: #78 closed unmerged, #79 merged 09:47:43Z 11 Sep). Site #346 owns `docs/SW2_LEDGER.md`.
No `REGISTER.md` write. No reset to pin `2e49afdd`. No reinstating S1-M's removed size-table
ratchet. One writer on the shared queue. **Blocker ceiling: three distinct blockers in a lane,
checkpoint and stop.**

**MISSING-SCOPE, still not inferrable:** GW1-E · GW1 §B–§F · LW1 · UX1 Part A §3+ ·
UX1 Part B §1.5+ · UX1 Part C · TH1 Part C · full LF1-M.

Also inherited, from RF2: **both brand marks stay as they are** by Matt's ruling — current
mark `assets/brand/micro_mark.svg`, 263 bytes, SHA-256 `c6b5d066…`. The nine supplied icon
files are design references, adopted nowhere.

---

## 7. THE FIRST THREE ACTIONS FOR THE NEXT SESSION

1. **Push `f746d5f` from `/home/user/mattroper1977.github.io` to `codex/rf1-prx1-candidate`,
   or if the container is gone, redo the four §2 clauses from `reports/prx1/DECISIONS.md`'s
   description in this handover.** Nothing else in RF3 can proceed until the §2 work is on the
   remote. Check first: `git ls-remote origin codex/rf1-prx1-candidate` — if it returns
   `3c11780a`, the work is unpushed.

2. **Re-run the PRX1 §3.1 golden test against the pushed head.** The balance assertion can
   raise where the old code did not, so 33/33 byte-identical (28 header + 5 main) must be
   re-proved with **no new raise on any target** before #350 ships. A raise on a real page is a
   hard STOP — it would break the publisher. The 91-file source scan showed 0 raises, which is
   encouraging and is not the proof.

3. **Merge #346, after confirming the #351 Pages deploy reached terminal.** Re-measure #346 at
   its exact head first (BL1 §3.2 — a merge moves the picture), and stop the sequence if its
   checks have changed character (§3.3).

Then, and only then: #350 undraft → confirm all four required contexts on the final head →
merge → emit `PRX1_CLOSED` / `_PARTIAL` / `_BLOCKED`. After that, RF3 §3.2 (mark the deadlock
document stale in place, in the Site repo, its own PR), §4.3 (file the PIN1 ruling in the
LP1/PIN1 handoff) and §5.2 (file P5.5 in the findings ledger) remain outstanding.

**RF3_PARTIAL.**

<!-- mbm-rf3-handover-2026-09-12-BOTTOM -->
