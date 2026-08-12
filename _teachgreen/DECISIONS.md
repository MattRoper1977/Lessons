# Teach-Green Close — 2026-08-12

Closes the teach-green pass. Four things merged on 12 August (Teach Hub card
fix, High Lumen theme, HUD keyboard guard, hud.js announcer); two were gated on
Matt and are released here.

Bases re-derived from remote before any work. All three were unmoved from the
values in the previous report, so its measurements still stood:

| repo | rollback SHA |
|---|---|
| `mattroper1977.github.io` | `7d800ebc` |
| `Lessons` | `000f3c48` |
| `Matt-s-Apps-` | `d8db0480` |

---

## VERIFIED_BY_MATT · 2026-08-12

Matt verified on his own hardware, not in a harness:

- **the six Teach Hub cards on his real phone** — they filter and jump to the
  workspace, with no reload;
- **High Lumen on the classroom projector** — approved.

That closes morning-list items 1 and 2 of the previous report, and it is the
authority for releasing Stage B and the link grid. Neither decision is
re-litigated here; only the code state they rest on was re-verified.

**Re-assertion at HEAD before starting** — the four merged features, measured
rather than assumed: 6/6 Teach Hub cards bound in real Chromium at phone and
desktop with a clean console · High Lumen present as the sixth
`mbm_reading_theme` value on all 7 ported pages **and in all four engine
copies** · hud.js keyboard guard and announcer both present · all four merged
gates re-run green.

---

## Overlap — one hit, examined and cleared rather than waved through

The matrix ran every unmerged branch in all three repos against the exact files
this pass would touch. Two hits:

- **`claude/teach-green-links`** — this pass's own branch, which §2 exists to
  merge. Expected.
- **`claude/pr110-audience-discovery-close-8y477v`** — unmerged, and touching
  all four of `teach/index.html`, `education-hub/index.html`,
  `assets/mbm-search.css`, `tools/render_discovery_hubs.py`.

The second one had to be resolved before proceeding, because §0.3 says any
overlap stops the pass. It is **superseded, not live**:

- its `teach/index.html` is **byte-identical** to pre-pass main (`5f979e7a`), so
  its content was already in main before this pass began;
- its renderer differs from pre-pass main by 5 lines, and the difference is that
  the branch hardcodes `SENTINEL` while main imports it from
  `render_audience_homepages.py` — main is the later, single-definition version;
- it carries the same closeout sentinel as main, its tip is dated 2026-08-09,
  and **no open PR references it** (open PRs are #109, #106, #96, #91, #25).

Recorded rather than stopped on, with the evidence above. It is the source
branch for work that landed by another route.

---

## The exclusion list, resolved from the estate's own rulings

§1.2's exclusions are named in prose. They were resolved to exact paths from the
records rather than guessed, because two of them are easy to get wrong:

| exclusion | what it actually is | in the 277? |
|---|---|---|
| **frozen legacy science** | REGISTER.md:1545, R-SEMH02 (ruled 2026-08-04): the 2025-26 freeze on `biology/`, `chemistry/`, `2 Physics 10/`, `5 Intervention 10/`. Path-scoped, four trees. | **37 excluded** |
| **★assessed** | The estate keeps TWO selectors. `★ ASSESSED LESSON` is the *inclusion* selector and returns exactly the 2 byte-locked decks. `★ ASSESSED` is the *exclusion* selector. | **0** — see below |
| **Games / LundyLoop / report-only Baseline** | Hard-excluded by name. | **0** — none carries a slide deck |

**The star nearly went wrong, and the way it goes wrong is worth recording.** `★`
appears in **221** HTML files, where it is the **Stretch tier** marker in body
copy. Excluding on that would have removed 221 files including the plan's own
recommended first population. The marker that means *assessed* is `★` in the
`<title>` — exactly 2 files repo-wide — and the estate's own exclusion selector
`★ ASSESSED` returns 7. **Zero of either set is in the rollout**, so the
question is settled either way, but the rollout tool excludes on the title
marker, which is a strict superset of the estate selector for these decks.

**The two byte-locked assessed decks already load hud.js** and were covered when
the announcer merged. Their pinned hashes are unchanged:

```
a5545585ca28bbba01b55476abb73a9b0819bcc7  Grow/Slideshows/GROW_HUM_W7_Write_The_Account.html
eb14d6104b94503d0e7ec0a99565ef116a333a57  Launch/Slideshows/LAUNCH_HUM_W7_Source_Assessment.html
```

**Stale count, reported not fixed:** REGISTER.md:64 records the `★ ASSESSED`
exclusion selector as returning **6** files. It now returns **7** — a rebuild
copy at `GROW_Estate_v3/Humanities_Teesside/GROW_HUM_W7_Write_the_Account.html`
(note the lowercase "the") post-dates the register's verification. Not a scope
change; the inclusion selector still returns exactly 2.

---

## Census — no delta

Re-derived at HEAD and identical to `docs/ANNOUNCER_STAGE_B.md`:

```
decks with slides   502
load hud.js         225   (covered when the announcer merged)
without hud.js      277
```

`277 − 37 frozen legacy science − 2 assessed rebuild copies = 238 in scope.`

---

## Stage B — the rollout

Per file, one line before the document's own `</body>`:

```html
<script defer src="/hud.js"></script>
```

**That form was derived, not chosen:** 220 of the 225 already-covered decks use
it. The other 5 wrap it in a loader with a relative fallback for `file://`,
which is out of scope — hud.js loading from the domain root and 404ing under
`file://` is an established property of this estate (§1.4), not a defect to fix
in a pass about announcements. No copy of hud.js is vendored.

**The anchor needed a rule.** Five decks carry a *second* `</body>` inside a
JavaScript string — the print-window template they hand to `document.write`.
Inserting at the first match would have corrupted that template. The tool
anchors on the **last** `</body>` and refuses the file unless nothing but
`</html>` and whitespace follows it, so the anchor is proven rather than
assumed. It skipped those five until the rule existed, which is the behaviour
§1.3 asks for.

### Proof of inertness — exact diff, not region sampling

`tools/stage_b_announcer.py --prove` asserts that each changed file equals its
base with that one string inserted **and nothing else**. That is stronger than
comparing regions one at a time, because it leaves nothing unchecked. The named
regions are then asserted on top so the proof is readable:

```
238/238 differ from origin/main by exactly the include
closure · witness · tiers · print · Oak · loop-mark — identical, every file
sentinels  ll-g:loop-mark 50/50 · written-closure 123/123, set-identical
frozen legacy science · assessed decks · Games · LundyLoop — 0 changed
```

Sentinel derivation is copied from `_lsg1/tools/lgates.py` so the two cannot
disagree. This is a hold pass: no movement is declared, so unchanged is the only
green.

### Print — both dialects

- `_nav1/tools/nprint.js` **reused, not rebuilt**: renders under `file://`,
  where hud.js never mounts.
- The new runtime gate renders **over HTTP with the HUD actually mounted** —
  the dialect nprint.js cannot reach, and the one that matters in a classroom.

---

## Reported, not fixed

**Three gates red since `5f979e7a`, none caused by either pass**, re-measured at
the merged HEAD and unchanged:

| gate | finding | owner |
|---|---|---|
| `render_audience_homepages.py --check` | `for/pupils/index.html` stale | unknown |
| `build_mbm_search_index.py --check` | 4 game entries differ (trail-runner, trekkers, intervention pupil/teacher apps) | unknown |
| `verify_design_inheritance.py` | 4 promoted images absent from `visual-provenance.json` | unknown |

**§3.1(b) was not done, and should not be.** The close order authorised removing
a "duplicate `data-mbm-filter="origin"` control" on the Education Hub. There is
no duplicate. The two controls are a deliberate two-button toggle group inside
`role="group" aria-label="Filter by origin"`, and `assets/mbm-search.js:379`
implements group semantics for exactly this shape. Measured:

```
baseline                 493 results
origin=internal          453 results   aria: internal=true  external=false
origin=external           40 results   aria: internal=false external=true
                         453 + 40 = 493 — the two partition the set
all 6 select filters      move the count
```

Removing either button would delete a working filter. **The observation came
from my own previous report and was wrong; it is corrected here.**

---

## Recorded, not built — theme-engine unification

The reading-theme engine exists in **four** edit sites: `theme.js` in the site
repo, `assets/mbm-theme.js` in Lessons, `assets/mbm-theme.js` in Matt's Apps,
and a self-contained inline implementation on the homepage. The High Lumen pass
proved they drift: updating one left the Lessons and Creator hubs showing five
swatches while the rest of the estate showed six, and the divergence was
invisible until a rendered contrast audit measured a cream background where the
theme should have painted white. A single shared engine with the three copies
reduced to imports would make that class of drift impossible. It is a bigger
change than any of these passes and touches every themed page, so it is
**recorded as a proposed future pass and no code was written for it here.**
