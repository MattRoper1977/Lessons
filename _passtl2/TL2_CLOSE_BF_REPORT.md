# TL-2 CLOSE (B · F) — Part B STOPPED at a keyboard trap; F listing still held

Sentinel: `tl2-close-BF-2026-08-18-TOP`

## Outcome in one line

Part B is **not merged**. Six defects were found in PRs that reported "25/25 passed"; five
are fixed and pushed, the sixth cannot be fixed by this pass because it lives in Town Life's
own bytes. F's listing pass stays held behind B, so
`AFTERDARK_VENDORED_TOUCH_PUBLISHED_SHA_PROVEN` remains unearned.

## §1 gates — all passed, nothing blocked entry

- Branch `claude/new-session-s7jbn0`, clean worktree.
- #169 head `65c5d0a`, #37 head `9bc08b0` — one commit each, `updated_at` equal to
  `created_at`, so untouched since the Part B report. No `PARTB_HEAD_DRIFT`. (The report
  records branch names and PR numbers, not head SHAs, so "unchanged since it was written" is
  the strongest available reading of that gate — stated rather than glossed.)
- Single-writer: the five other open Site PRs (#109, #106, #96, #91, #25) touch none of
  `/for/pupils/`, `/games/` or the games manifest — checked file by file.
- Count derived from the record: **24 site-served + 29 Lessons = 53**, matching the recorded
  24+29=53. No `COUNT_DERIVATION_MISMATCH`.
- Town Life runtime on the branch: 304,744 B, sha256 `3605124f…`, byte-identical to the
  Part A gated artefact.

## "25/25 passed" was Part B's own harness; the estate's CI was red on 8 checks

Verified at the original head `65c5d0a` before this session touched anything, so none of it
was introduced here. Full detail in the evidence workspace; summary:

| # | Defect | Status |
|---|---|---|
| 1 | Derived search index never regenerated — discovery gate would red on main | fixed |
| 2 | `/for/pupils/` is machine-generated and was hand-edited | fixed by regenerating |
| 3 | Town Life claimed the whole-shelf `NEW ·` marker (S4 allows one) | fixed |
| 4 | New card art unrecorded in `visual-provenance.json` | fixed |
| 5 | Town Life had no declared hud.js status | fixed (excluded + exit region stamped) |
| 6 | **Town Life traps keyboard focus on its welcome screen** | **STOP — needs a game fix** |

Two of those deserve restating because they change a stated premise:

**`/for/pupils/` is generated.** The owner's D2 line says to hand-edit it. It is literal HTML
in the browser — which is what the earlier finding measured — but it is built by
`tools/render_audience_homepages.py`, whose contract is "Generated output is never
hand-edited. --check fails if the committed HTML differs by a single byte." Regenerating
honours the intent through the mechanism the estate actually uses, and the data file says why
that is better: the games there are read from `games/index.html`'s CURATION and TAXONOMY "so
this page and /games/ cannot disagree" — the cross-page control is structural, not a number
to write by hand. It also fixed two things the hand-edit got wrong: Town Life sat in the
wrong position within its genre group, and was **missing from the surprise set entirely**, so
the random-game feature would never have offered it.

**The `NEW ·` marker.** Gate S4 allows at most one holder and ratchets on the baseline; Part B
knowingly made it two and left retiring Emberwild's to the owner. The estate's own doctrine,
written into its shelf transforms, is that a game-specific change "never mints, moves or
removes the whole-shelf release slot" — the same rule the owner applied to Afterdark. The
prefix was dropped from Town Life; Emberwild keeps the slot until it is moved deliberately.
No other game's curation was touched. Rail gates then 8/8, validator PASS at 53.

## The stop: Town Life's welcome dialog holds focus in front of the exit

Every declared root game must carry a keyboard-reachable way out. After the exit region was
stamped it renders correctly at 390, 768 and 1440 px — 44x44, on top, visible, accessible
name "Back: Arcade", href resolving to `/games/` — but:

    [FAIL] /townlife/: exit is reachable by Tab · presses: null

Measured with a direct Tab walk: the welcome dialog cycles
`#profileName → #startBtn → #openHelpFromWelcome` and never releases, for all 130 presses
tried. Measured both ways so the claim is no broader than the defect:

- welcome screen, the state a pupil lands in — exit **not** reachable by keyboard;
- after clicking "Enter Town" — exit **is** reachable, at press 21.

The repair belongs in the game's welcome-dialog focus handling. This pass may not make it:
"no payload byte edits to Town Life" is an explicit red line, and such an edit would move the
artefact off the sha256 Parts A and B pin it by. The platform cannot fix it from outside —
the region is already stamped, rendered and correct; the game never yields focus to it. Both
available contracts are mandatory for a declared root game, so no configuration lands B
green.

**Identity note, since the stamp does change the served file:** the region is the estate's
own 3222-byte block, byte-identical across all 11 targets. Running the estate's stripper over
the stamped file reproduces `3605124f…` exactly — the Part A pin. The game is unchanged; only
the platform's region is added, exactly as on the other ten, which is what the stripper exists
for.

## Merge order — a correction worth carrying forward

Part B's report says merge Site first. The two PRs are **mutually blocking**: #169 fails
"Mirror equals the canonical shelf" because the Games canonical lacks Town Life, and #37 fails
"Site mirror has caught up with this shelf" because the Site mirror lacks it. Each repo's gate
clones the other at `main`, and the site's browser gates build their served tree by copying
the Games canonical, so most of #169's remaining failures share that one root. It resolves
only by merging the pair back to back — which is what would have happened had the stop not
intervened.

## State left behind

Both PRs open, six commits pushed across them, nothing merged, no repository on `main`
touched. Whenever a Town Life build releases focus to the exit, B lands with no further work.
Games #37 is green but for the mutual-block check.

## Owner-held list, as this close leaves it

- **Town Life v1.0.3**: release keyboard focus from the welcome dialog to the platform exit
  (ids `mbmexit-back`, `mbmexit-home`). Blocks Part B, and therefore Part F's listing.
- **Chromebook check** before first pupil use in September — deferred by ruling, never
  performed, and not claimed anywhere.
- **LundyLoop**: "Participation debt" label · closure standard vs LL-I.
- **Maker Lab**: reading-demand plain-language pass · the three handed-back findings
  (the stale `49` tile, teacher-only wording, the predicted search id) → v2.1.1 decision.
- **Part C**: callsign + layout-name proposal awaiting the owner.
- **Emberwild's `NEW ·` marker**: still held; moving it is a whole-shelf editorial act.
- The stale `/games/` comment "the page paints 60 cards for 52 games", now off by one; left
  alone rather than widening a reviewed PR's diff at merge time.

Sentinel: `tl2-close-BF-2026-08-18-BOTTOM`
