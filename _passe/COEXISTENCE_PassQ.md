# Pass E ↔ Pass Q coexistence (R-H02) — reconciliation

**Discovered at post-push fetch.** While Pass E ran (branched from `12cb6d9`), a **parallel Pass Q
(KO Triage)** — the *same briefed pass*, run independently — landed on `main`, which moved
`12cb6d9 → 59ad56a`. Pass Q's own ledger records the identical origin: *"provisional Z collided (two Pass Z
commits in git history); self-renamed to Q."* Pass E hit the same collision and renamed to **E**. So this is
one pass, run twice; **Pass Q landed first.** Per R-H02 the first-lander holds and the second corroborates —
Pass E does not overwrite Pass Q.

## What Pass Q landed on main (`12cb6d9..59ad56a`)
- `7e16d67` Pass Q ledger — **0 STALE of 114** at HEAD `c034ffd`; `_passq/` (ledger + scripts); no `*.html` touched.
- `569e622` REGISTER — **R-G05 REFUTED AT HEAD (Pass Q, 0/49)** + an R-H09 cross-repo letter clause.
- `c481dcf`/`db2ebbb` — **CAREERS_W7 print We-Do-2 answer bank** fix (it carried W6's answers). Merged, approved by Matt.
- `59ad56a` — R-G03 closed (unrelated).

## Agreements (independent corroboration — the valuable half)
| claim | Pass Q (landed) | Pass E (held) | status |
|---|---|---|---|
| R-G05 "37 of 49" at HEAD | 0 / 49 disagree (`c034ffd`) | 0 / 49 snapshots (`12cb6d9`) | **AGREE** — two methods, same number |
| the 112 non-STALE KOs | STILL-TRUE | STILL-TRUE | agree |
| assessed pair | READ-ONLY, STILL-TRUE on read | READ-ONLY, surface STILL-TRUE + residue flag | agree (both defer to Matt) |

## Divergence: Pass Q found 0 STALE, Pass E found 3 STALE — all 3 pre-date Pass Q's head
Pass Q's verdict rule (TRIAGE.md §3): *"STALE only if the KO disagrees with the We-Do-2 print mirror /
on-screen We-Do-2."* That scope does not examine two axes Pass E read:

| Pass E STALE | axis | Pass Q verdict | reconciliation |
|---|---|---|---|
| `CAREERS_W6_My_Career_Profile` KO h1 `W6`→`W7` | KO **h1 week label** vs the file's own `<title>`/slide-tag | STILL-TRUE (def. content only) | **additive, not contradictory** — Pass Q read definitions, not the week label. KO h1 was already `W6` while `<title>`=`slot W7` at `c034ffd` (verified). High confidence. |
| `CAREERS_W7_After_Year_11` KO h1 `W7`→`W6` | same | STILL-TRUE (def. content only) | additive. (Pass Q *separately* fixed this file's print answer bank — a third, distinct issue, now on main.) High confidence. |
| `BUILD_HUM_W6_Plan_The_Story` KO → PEEL (add Link row) | KO **writing model** vs body | **STILL-TRUE** | **genuine same-axis divergence.** PEEL landed `07-24` (before both heads); body teaches *"What does PEEL stand for? … link"* + a Link bank, and the sibling `GROW_HUM_W6` KO *was* updated to "PEEL unit" — but this KO was not. Whether a KO must enumerate every writing-model element is a **judgment call for Matt**; Pass Q (conservative) said no, Pass E said yes. |

## What Matt decides (not resolved this session — held, no merge)
1. **Letter/identity:** Pass Q (Q, landed) and Pass E (E, held) are the same pass. Keep Pass E as a distinct
   corroborating/additive pass, or fold its 3 fixes into the Pass-Q lineage and retire the E letter?
2. **The 3 STALE fixes** (held on `pass-e-ko-triage`): merge on top of Pass Q's landed 0-STALE result?
   The two Careers h1 fixes are additive and low-risk; BUILD_HUM_W6 is the one judgment call.
3. **Merge conflicts to expect** (Pass E branch vs current `main`): `REGISTER.md` (both appended R-G05) and
   `CAREERS_W7` (Pass Q's print fix + Pass E's KO-h1 fix). Both are held; resolution is a merge-time task,
   Matt's key. Pass E's branch is intentionally based on the pre-Pass-Q tip `12cb6d9`.
