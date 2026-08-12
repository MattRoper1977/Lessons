# NAV-1 · Way Home + Latest-content organisation — decisions, at the time

Pass `lsg1c-nav1-2026-08-12`, PART B. Runs in the same session as LSG-1C
(Part A), under the superseding master prompt. Written **as the pass runs**.

---

## 0 · Precondition, base, rollback, identity

**Precondition (replaces the old serialization gate):** Part A's merge is on
main and Pages built that exact SHA.

- Part A merge commit: **`eb422a739f756fc3f97ffbfb0247d8d06ed905cd`** —
  `pages build and deployment` at head `eb422a7`: **completed / success**. ✔
- Part A close-records commit `3e48503`: its Pages build **failed on attempt 1
  with a runner-side TLS error** (`jekyll-github-metadata` API call,
  "certificate verify failed (self-signed certificate)" — GitHub
  infrastructure, nothing in the commit, which was a Markdown append).
  **Re-run via the API (not a retry-push): attempt 2 completed / success.**
  Recorded as AMBER-PAGES-FLAKE.

| Item | Value |
|---|---|
| Base | **`3e485033fafa2ff7d6c37eb3dcb831a05b011f22`** — the main Part A produced (merge `eb422a7` + its close-records commit) |
| **PART B ROLLBACK SHA** | **`3e485033fafa2ff7d6c37eb3dcb831a05b011f22`** — recorded before Part B's first commit; Part A's rollback (`470be57`) does not cover Part B |
| Branch | `claude/nav-1-way-home`, cut from that main |

**Identity 5/5:** origin = `MattRoper1977/Lessons` ✔ · Build/Grow/Launch
v3_40min = 10/10/15 lessons ✔ · `resources.json` parses, 640 entries, `added`
on 513, `new` on 240 ✔ · root `index.html` exists ✔ · main history contains
the Part A merge (`eb422a7`) and `e76c654` ✔.

### R-H02 · the serialization scan, and its context-read ruling

Scan: all **102** unmerged `origin/*` branches diffed against their
merge-base with main for `Science_Teesside/` touches. **One hit:**
`origin/claude/approved-0805` — 31 files, 25 in `Science_Teesside/`.

Context, derived not assumed: tip `e24bf04` dated **2026-08-05** (a week
stale, merge-base *before* the BSG/GSG/LSG merges); its own message says
"before opening this PR" — a **parked proposal awaiting review** ("labels on
3 decks, hides on 25 sheets"), touching only the **frozen v5 original** trees
(`Science_Teesside/{Build,Grow,Launch}/SCI_*` — no `v3_40min/` file, and not
the root hub or `resources.json`). **Intersection with Part B's write set:
0 files.**

**Ruling:** the serialization gate guards against another *in-flight pass*
writing this tree. A week-stale parked proposal with zero write-set
intersection is not that hazard class — the estate's context-read doctrine
(a hit is not a finding until its context is read) applies. **Recorded
prominently here, in the §B8 report and on Matt's morning list rather than
halting the delegated pass.** Note for that review: the branch does touch the
frozen v5 `SCI_L_W5_L2_OsmosisCP.html` (the A4 quarry) — the live A4 clip was
verified byte-equal against **current main's** copy, which is unchanged.

### 0.3 What changed under Part B's feet

The 15 LAUNCH lessons now carry Part A's fourteen `.sclab` labs, the W5L2
`.oslab` specimen and the A4 clip. Every Part B byte-region assertion
compares against **post-Part-A main (`3e48503`)**, and the button's
geometry/contrast checks run on lab-bearing slides too.
