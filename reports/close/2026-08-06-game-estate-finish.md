# Game estate finish sitting — 6 August 2026 (second sitting)

Finishes what the audit/repair sitting parked. Every figure derived at the SHAs
named; nothing quoted from the order as fact.

## §0 · Gate

Heads at open, via `ls-remote`, all three exactly at the expected minimums:
Lessons `3dc23c6`, Games `919f4a2`, site `878d54f`. The prior sitting's three
markers (run ledger, splash census JSON, `PHONE_CHECKLIST.md`) all present.

**Capability, probed by launch this session, not inherited.** Chromium: OK.
**WebKit: still unavailable in the container** — the Playwright download 403s
through the agent proxy. That is what §C's runner route was for.

**Sequencing.** No in-flight branch collides. Site PR #25 (HOLD, homepage AJAX)
touches the site's `index.html`; this sitting's site scope was `tools/` only, so
the surfaces are disjoint and #25 was not touched. Stale non-PR branches that
appear to touch `index.html` are leftovers with no open PR — the in-flight check
was re-derived against open PRs only, which is the honest population.

## §A · Splash coverage — 10 games, complete

**The committed census was wrong twice, and the correction is the first result.**
It sampled each game once at 2.2 seconds. Trail Runner's bespoke splash
auto-closes at ~1.6–2.2 s and Apex Golf's is removed at ~2.0 s, so both were
sampled just past their own closing frame and recorded as unbranded. Re-derived
by polling 150 ms → 3 s: both have had a brand splash all along.

| disposition | games |
|---|---|
| **patched** (10) | Globe Snake · Neon Snake Overdrive · Neon Siege · Neon Garden · Orbital · Grid Chase · Prism · Slipstream · Kids vs Staff: Showdown · Trekkers Trail Runner |
| **preserved bespoke** | Trail Runner, Apex Golf (both census false negatives), Marble, and the 27 already branded |
| **excluded by rule** | `Orbital_source.html` — non-shelf secondary; a splash there is the modernisation R11 forbids |

Real set: **10, not 14. The site repository needed no change at all**, so §A is
one PR on Lessons (#79, merged `c2419ef`).

Donor verified unmoved at `e375642c…` and **inlined, not linked** — these games
are single-file and offline-first, and a `<script src>` would reintroduce exactly
the remote dependency Band 2 removed. The splash plays above each game's existing
boot screen and fades to reveal it: one start state, not two.

**Two deliberate hardenings over the donor.** `preventDefault` does not stop the
skip key bubbling to the window-level handlers these games install, so the key
that skipped the splash would also fire a gameplay action. Skip paths now
`stopPropagation`/`stopImmediatePropagation` and listen on `window` in the
capture phase, ahead of any game handler registered earlier; the overlay swallows
stray clicks.

**Gate: `tools/verify_games_splash.mjs`, 360/360** — appearance, labelled modal
dialog, pointer + Escape/Enter/Space skip each with a leak counter, single
auto-close, focus return, static reduced motion, zero remote requests, zero save
mutation, zero overflow, one start state; per game, both RM states; targets
derived from the marker so an eleventh game joins automatically.

Its `--self-test` is a **real** negative control: it weakens an actual patched
game back to the donor's `preventDefault`-only form and proves the leak assertion
goes red (`keydown 0→1`).

### Four of the gate's own bugs, found before any green was believed

1. A fixed 500 ms wait raced game boot and called four *present* splashes absent.
2. Sharing one page across assertions lost the ~1.1 s reduced-motion window
   (Trekkers boots at 942 ms; the window closes at 2032 ms).
3. A fixed post-skip delay raced the 600 ms fade-out.
4. Counting any `transition-duration > 0` as "animated" failed Trekkers for using
   the standard `transition-duration:.01ms` reduced-motion idiom — **penalising a
   game for being more careful**. Perceptibility now has a 20 ms floor.

Measured splash visibility: **3.6 s** full motion, **1.09–1.68 s** reduced — the
donor's intended behaviour, confirmed rather than assumed.

## §B · Instrument corrections

**Scope discrepancy, flagged not worked around.** §B places these in the Games
repo; both named instruments live in the **site** repo. The delegation was
explicit ("FIX BOTH"), so they were fixed where they actually are, under a
`tools/`-only allowlist, and §B.3's census ran in Games as written.

**site PR #76** (merged `1e47200`), `tools/` only:

- `verify_apexkick.js` — **counted the wrong thing.** It regexed every `http`
  string in the file and subtracted two innocent shapes by hand, so a
  `rel=canonical`, an `og:url` and an `og:image` counted as "remote resources":
  three metadata values no browser requests while rendering. It now counts
  references in positions that actually fetch, with metadata excluded by
  construction rather than by a growing allowlist. **24/25 → 25/25.**
  - tamper: a real `<script src="https://…/tracker.js">` → **FAILS**
  - tamper: two *more* metadata URLs → **still PASSES** (miscount proven gone)
- `verify_arcade_sports_browser.js` — **five literal rosters** in a file whose own
  header says "every expected count is DERIVED… No literal totals". Membership,
  rendered hrefs, per-surface counts, the card-art check that named Apex Tennis,
  and copy that had to read "Four Apex games" — all now derive from the
  manifest's Sports collection, including the copy's count word. **23/28 → 28/28.**
  - tamper: drop a member → **FAILS** · tamper: promote a sixth → **FAILS**
  - recorded for the next reader: this gate *routes* `/Games/games.json` to the
    manifest under test, so rail-vs-manifest is necessarily self-consistent; the
    **copy** assertion is what actually catches roster drift, which is why both
    tampers land there.

**Games PR #23** (merged `68e7e13`), `tools/` docs only. The pin census found
every **live** Games instrument already derived. Two pinned ones remain and both
belong to the retired Apex Sports family — `verify_apexpool_sports_browser.js`
was one all along (the retired workflow runs it) but had never been named in the
record; it is named now. **Neither converted, deliberately:** both describe a
*transition*, not an invariant, and re-deriving them would mean writing a
different gate that happens to share a filename, destroying the audit trail the
record exists to preserve. The census table is appended so the next sweep starts
from a derived answer.

## §C · WebKit — attested

The container still cannot install WebKit (403 through the proxy, re-probed this
session). The runner route worked.

**Slice actually run** — named honestly, because it is not the full 516-cell
matrix: **43 targets × phone portrait 390×844 × reduced-motion on/off × online,
in WebKit *and* Chromium side by side** = 172 cells, so any WebKit-only failure
is attributable to the engine rather than to the slice. Not run in WebKit:
desktop and landscape viewports, and the blocked-network half.

Run three times. Twice for coverage — once against `919f4a2`-era main (run
`31092238813`) and again against **post-splash main** (run `31095157097`, branch
commit `ac24a98`, parent `c2419ef`) so the attestation covers the ten new
splashes — and both were identical:

```
 targets: 43     cells: 172
 webkitLoadFail: 0     chromiumLoadFail: 0
 webkitPageErrors: 0   webkitOverflow: 0
 findings: []          NO WEBKIT-ONLY FINDINGS
```

**A third run, because of a correction to this instrument found while reading
its own green.** The comparison script printed its findings but never exited
non-zero, so the job would have gone green *with findings present* — a gate that
could not fail, which is the one thing this estate has learned to check for. It
now `process.exit`s on any finding. Run `31096090270` carries that hardening and
is green, so the zero above is now a zero the job would have refused to report
if it were false.

The temporary workflow lives only on `claude/webkit-attestation`, which is
**retained but never merged** — it has not reached `main` in any repository.

## §D · Expansions — not started, ledgered

G1 Fracture League, G2 Proofline, G3 Constellation Workshop: **none started.**
§D's default is "not this session", and its only-if required clear remaining
budget after §A and §B. §A alone ran 360 browser gates across ten games and two
reduced-motion states, plus four of its own instrument bugs; §B ran four tampers
across two repositories. The honest reading is that the budget for a §6-bar
expansion — save-migration proof on a real captured save, extended verifier with
named anchor widening, non-vacuity tampers, photosensitivity and RM recert — was
not there, and starting one to park it half-done is the failure mode §D names.

Standing context that remains current for G2: Axiom Shift's harness ran green
this estate-day at 69 assertions, max flash **2.600 Hz** — its photosensitivity
floor is measured and current, not inherited.

## Instrument corrections, cumulative

This estate now has a short register of gates that could not fail, all caught by
negative controls rather than by inspection:

1. (prior sitting) `img.complete && naturalWidth === 0` — `loading="lazy"` made
   every below-the-fold image exempt.
2. (prior sitting) `getContext('webgl')` **creates** a context, so menu shells
   read as live.
3. (prior sitting) a single-moment overflow sample passed a projection-dependent
   defect that peaked at 3314 px.
4. (this sitting) a splash census sampled at exactly the auto-close boundary and
   produced two false negatives.
5. (this sitting) three timing races and one over-strict animation threshold in
   the splash gate itself.
6. (this sitting) an apexkick matcher that counted metadata as fetched resources.

## Honest not-run / still open

- WebKit desktop, landscape, and blocked-network halves: **NOT RUN** (slice named
  above).
- The audit pack remained absent this sitting too; it was optional by this
  order and parked nothing.
- Live-origin checks (`verify_surfaces.js` and friends): still NOT RUN from the
  container; live propagation was proven byte-identical on a runner this morning.
- Frame-budget gates: not attestable in a shared container; runner history green.
- All three expansions: ledgered above.
- Matt's phone pass, including the ten new skip-by-touch rows.
