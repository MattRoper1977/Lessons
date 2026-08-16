# Release ledger — combined order v2, 16 August 2026

Four independent targets, one runner, one shared discipline. Each has its own
branch and its own PR; none of them shares code with another.

| | Target | Verdict | PR |
|---|---|---|---|
| **A** | Scrap Core: Expedition SIGNATURE v10 | **P0 resolved, P1–P5 not attempted** | [#117](https://github.com/MattRoper1977/Lessons/pull/117) — open |
| **B** | Class of Ashes: Zero Period PRO v1.0.0 | **Patched and parked** | [#118](https://github.com/MattRoper1977/Lessons/pull/118) — open, do not merge |
| **C** | Virtual Chemistry Lab PRO Spatial v0.3 | **Both merge-blockers green; awaiting the V7 route** | [#116](https://github.com/MattRoper1977/Lessons/pull/116) — open |
| **D** | R-Wilton-4 | **Merged** | [#115](https://github.com/MattRoper1977/Lessons/pull/115) — merged |

All three payload baselines reproduced **exactly** before any work started:

| payload | sha256 | size | checksums |
|---|---|---|---|
| `Scrap_Core_Expedition_SIGNATURE_v10.html` | `33f1260b…97608` | 217,715 B / 3,121 lines | 15/15 verify |
| `Class_of_Ashes_Zero_Period_PRO.html` | `a04c41da…4896f` | 179,249 B / 604 lines | 15/15 verify |
| `Virtual_Chemistry_Lab_PRO_Spatial_v0.3.html` | `bd0e7596…6cdef` | 173,102 B / 1,646 lines | n/a |
| prototype (reference only) | `24fc1443…6348` | 59,316 B | — |

---

## R0.11 — a red that proves a dependency is not a red that proves a behaviour

Where a transform's sole removal crashes the build **because another transform
calls what it defines**, the red is measuring the crash. Label it; do not count
it as a control.

Three exist here: C's `X1c` (the `acidFirst` predicate both sequencing fixes
call), C's `X5a` (the table `X5b`'s template references), and B's `Y4d` (the
helper `Y4c` calls). All three are labelled **LOAD-BEARING** in their matrix
output rather than counted among the behavioural controls.

**The label's first implementation could never fire**, and it took a re-read of
the artefact to notice: it grepped the verdicts file for `ERR->ERROR`, but that
file stores `ERR ERROR` — the arrow exists only in the diff string built
separately for display. So every load-bearing transform printed as an ordinary
`watched`, and an earlier version of PR #118's description asserted a label the
tool had never applied. Corrected there and here. It is the tenth check caught
unable to fire this pass, and the first I introduced *while writing the rule
about them* — which is the argument for re-reading the artefact rather than the
summary, made against myself.

The alternative — folding transforms together until every red looks like a
behaviour red — is how a matrix gets gamed into looking complete. Target D
*did* merge two transforms, and that was right there because they were one
change split in two. B and C label instead, because halide and sulfate
sequencing, and the two halves of the subtitle fix, are genuinely separate
changes: folding them would buy a tidier table at the cost of being able to test
them apart. **Both treatments are recorded, which is what makes them consistent
rather than inconsistent.**

## Assert a positive margin, never the absence of a violation

`overlap === 0` passes when two boxes **touch**. That is not clearance, and it
was not a cosmetic error: under a real 8 px margin the Class of Ashes release
build fails **8 of 8** viewport/largeHud combinations rather than 6 — the two
wide ones had been scoring zero overlap on a zero gap and reading as passes.

This is the **second** target where the same predicate error hid a real failure,
so it is a rule rather than a one-off. Both instances came from a gate that was
honest about what it measured and wrong about what that meant.

## R0.13 — evidence outlives its subject, and looks identical to evidence that has not

Two tracked files recorded per-transform verdicts for **T10b — a transform merged
into T10 several commits earlier and non-existent since**. They were correctly
formatted, internally consistent, and describing nothing.

**An artefact recording a verdict must be checkable against the existence of its
subject, or it is decoration with a filename.**

### `evidence/` versus `work/`, and the near-miss that let it happen

- **`evidence/`** is written once per run and reviewed before it is committed.
- **`work/`** is rewritten mid-run by the removal matrix and is never evidence.

The `.gitignore` covered `drop_*/` and `work_*/` and **missed `work/`** — the
directory the matrix actually uses. Thirty-six files were tracked; two of them
were T10b's. A near-miss of exactly the shape this estate keeps producing: two
patterns that look like they cover the third and do not.

Fixed in Lessons and `Matt-s-Apps-`. The site repo had the same shape with
`audit-output/` — seven tracked screenshots — and now has the same fix.

### The sweep, and the false positives it produced first

`tools/stale_evidence_sweep.mjs` runs both directions across all three repos and
**removes nothing**, because a removal you cannot show the subject is absent for
is worse than keeping stale evidence.

Its first run flagged **four rows as stale — `T10a`, `T10b`, `X0`, `X1c` — and
every one was a false positive.** `T10a`/`T10b` are *control* ids in the controls
table; `X0`/`X1c` are *row* ids in the split-transport report. All four describe
subjects that exist. **A sweep built to catch stale evidence was one step from
deleting live evidence, because it matched an identifier's shape rather than the
claim being made about it.**

That is a different failure from the twelve below and is counted separately: those
are checks that could not fire, this is a check that fired wrongly. The second
kind destroys rather than merely fails to protect.

With the predicate corrected — only a removal-matrix row asserts "this transform
is watched", and those lines carry the verdict word — **forward: 0 stale.**

### The inverse direction, which is the more dangerous one

**`hud-coverage.json`'s `scriptLine` had no consumer.** A repo-wide grep over
every `.py`, `.mjs`, `.js`, `.sh` and `.yml` returns nothing. Twelve root game
routes carry that literal, inserted by hand in one August commit and maintained
by hand since.

The assertion that ought to have existed **would pass today** — all twelve
byte-identical. That is the argument for adding it, not against: today it is
free, and what it buys is the difference between *true* and *guaranteed*.
Landed on `claude/hud-coverage-scriptline-load-bearing` with a `--self-test`
that drops `defer` from one tag and requires a red.

## The finding worth more than the count

**Two of the last four unfireable checks were introduced in the same commits as
the rules about them.** The LOAD-BEARING label could not fire, and it was written
to record R0.11. The overlap predicate accepted touching boxes, in the pass that
established "assert a positive margin".

Writing a rule does not inoculate the author against the defect it names. That is
not a confession; it is a finding about how these defects propagate, and it is
the reason the removal matrix and the artefact-not-summary rule earn their cost —
neither depends on the author having understood their own rule.

## §S2 — the evidence rule, applied to this pass

Every claim below names the artefact that proves it, and every artefact
discriminates. Where a check would have passed on a broken build, it was
rewritten or deleted. **Twelve were caught this pass** — ten in these gates, a
Matt-side one (the button-label finding landed on VSL's gate 5, authored the same
afternoon), and one found by re-reading an artefact rather than its summary line.
The last four share a shape: **the fix was fine and the check was wrong, and only
removing the fix could tell the difference.**

| what was wrong with the check | how it was caught |
|---|---|
| a reduced-motion seed appended after `</html>`, inert text, never executed once | matched pair measured `body.calm` on both trees and found it false on both |
| storage-call records kept in a page global that `location.reload()` destroyed along with the evidence | the `removeItem` limb recorded nothing on a build that definitely removed |
| three localStorage removals masking each other, so one control watched none of them individually | removal matrix: dropping T1, T2 or T3 changed no verdict |
| a frozen-region assertion whose pattern no longer matched, reporting MOVED with nothing moved | the assertion said REGION NOT FOUND rather than passing |
| a rehydrate step that protected nothing `loadHash` already did | removal matrix reported it UNWATCHED; the step was deleted, not given a control |
| a control that only went red because the page threw | removal matrix showed a crash, not a change; the two transforms were merged into one |
| a button label recorded as a note, so the transform that changes it could be reverted with every gate green | removal matrix reported the transform UNWATCHED; the label is an assertion now |
| **an overlap predicate that passed when two boxes TOUCHED** — "zero intersection" is not clearance | removal matrix reported the derived-clearance transform UNWATCHED, because a fixed value abutted the HUD exactly. Tightened to a measured 8 px gap, under which release fails **8 of 8**, not 6 |
| *(Matt's)* VSL gate 5 — the same defect as the button label, on a gate authored the same afternoon | recorded here because it is the same defect class, not because it is mine |
| **the LOAD-BEARING label itself could never fire** — it grepped the verdicts file for `ERR->ERROR`, but that file stores `ERR ERROR`; the arrow only exists in the separately-built diff string | noticed because two transforms with a visible `ERR->ERROR` in their diff printed as ordinary `watched`. **The first introduced while writing the rule about them** |
| **NAV-1 shipped with its markup and none of its CSS**, and the control passed — it asked only whether the link had a non-zero box, which an unstyled inline link has | the lab had a way home with no 44 px target, no focus ring and no print suppression, and a green gate said it matched the convention. `T13` now reads the **live stylesheet** for all three |
| **`assert_unchanged` crashed instead of reporting** when `T15` could not be built in isolation, its anchor being text `T12` introduces | it declares the dependency now — R0.11 applied to a build rather than to a red |
| *(the same commit)* its text-delta report printed the **whole** delta, burying the one unauthorised string among the expected ones | printing the difference instead immediately exposed a mismatch on a **non-breaking space** nobody could see |

**The button label and the overlap predicate are worth reading twice.** In both
the *fix* was fine and the *check* was wrong, and only the removal matrix could
tell the difference. A gate that goes green on a reverted fix is not evidence
about the fix — it is evidence about the gate.

**Final matrix state: every transform on every target is watched.**
D 16/16 · C 18/18 · B 10/10 — and now measured with a label that fires, rather
than one that could not. Class of Ashes, verbatim:

```
B — Class of Ashes                     C — Chemistry Lab
Y1a  watched                           X1a  watched        X3d  watched
Y1b  watched                           X1b  watched        X3e  watched
Y2   watched                           X1c  LOAD-BEARING   X4   watched
Y3   watched                           X2a  watched        X5a  LOAD-BEARING
Y4a  watched                           X2b  watched        X5b  watched
Y4b  watched                           X2c  watched        X6c  watched
Y4c  watched                           X2d  watched        X6d1 watched
Y4d  LOAD-BEARING                      X3a  watched        X6d2 watched
Y5d  watched                           X3c  watched        X6d3 watched
Y5e1 watched
```

Three LOAD-BEARING, exactly the three R0.11 names, and each one now carries the
label because the check tests the diff string rather than the verdicts file.
`X2a`'s row is the one worth reading in full: dropping it reddens `V2a`, `V2c`,
`V2g` and `V3-roundtrip-work` together, because the privacy ruling widened what
that single transform removes from the URL and every part of it has its own
assertion behind it.

The matrices also now hold a lock on their evidence file. Two runs wrote into one
file concurrently and left an interleaved artefact with a half-line in it —
readable enough to skim past, which is exactly the problem.

Two claims in the incoming reports were checked and are **true but unproven by
their own artefacts** — the Class of Ashes touch-fire response (`shots: 0` in
their summary) and the briefing-map pixel proof (two near-black pixels compared).
Neither is a defect; both are recorded so the artefacts are not cited as proof.

---

## Target D — merged

Two rulings issued, both landed, both one swap line from being undone.

| item | what changed | artefact | red/green | planted failure seen red |
|---|---|---|---|---|
| Ruling A | C21 added as the taught fuel-oil feed, in all three feed lists | `W-R-C21`, `W-ID24`, `W-ID3` | red→green | yes (drop T8a/b/c) |
| Ruling A | C24 stays selectable, stays undistillable, stays declared | `W-R-C24`, `W-DESIGN` | UNREACHABLE, declared | yes (drop T8a) |
| Ruling A | the refusal message teaches, in two sentences | `T10a`, `T10b` | red→green | yes (drop T10) |
| Ruling B | five tray temperatures corrected | `W-DIAG` 4/5 → **5/5** | red→green | yes (drop T11) |
| Ruling B | the marker-vs-readout limb, across all feeds | `W-DIAG-MARK` 5/5 → **6/6** | already consistent | yes (drop T7) |
| Ruling B | the caption | `T12` | red→green | yes (drop T12) |

**Headline: release teaches 1 of its 5 selectable feeds into the right fraction;
the merged build teaches 6 of 7, C24 declared unreachable by design.**

Sixteen transforms; drop all sixteen → release byte for byte; drop each one → a
verdict changes. Mission transport green in all four release/staging splits,
both directions.

**Recorded and left:** 22 of the 38 pupil-facing inputs have no accessible name.
Identical on release. `staging/` is wired to no route; merging did not deploy it.

---

## Target C — both merge-blockers green

| item | what changed | artefact | red/green | planted failure |
|---|---|---|---|---|
| **V1** | sequencing predicate is order-aware; the model untouched | `V1 {chloride,bromide,iodide,sulfate} reversed` | 4 red → 4 green | yes (drop X1a/X1b/X1c) |
| **V1** | correct order keeps its clean positive | `V1 … correct` | green both sides, asserted | — |
| **V2** | `pupil` out of the serialiser | `V2a` | red→green | yes (drop X2a) |
| **V2** | name still in print and Export JSON | `V2b` | asserted; a first cut broke it | yes (drop X2d) |
| **V2** | both captions describe what the link carries | `V2d`, `V2e` | red→green | yes (drop X2b/X2c) |
| **V3** | 3,814 → **26** fresh; 8,093 → **1,485** on a realistic session | `V3`, `V3-detail` | red→green | yes (drop X3a/X3c) |
| **V3** | round-trip and legacy links still work | `V3-roundtrip`, `V3-legacy` | asserted | yes (drop X3d/X3e) |
| **V4** | `.drop-pill` rule; gap 0 px → **6 px** at 390 and 1440 | `V4 @390px`, `V4 @1440px` | red→green | yes (drop X4) |
| **V5** | 6 of 8 negated near-misses marked correct → **0** | `V5`, `V5b`, `V5c` | red→green | yes (drop X5a/X5b) |
| **V6.4** | reduced motion seeded from the OS | `V6.4a`, `V6.4b` | red→green | yes (drop X6c) |
| **V6.5** | **17** unnamed controls across five benches → **0** | `V6.5` | red→green | yes (drop X6d*) |
| **V0** | the frozen engine, pH model, mystery hash, 14 observation strings | `U2`, `U2s ×14` | unchanged | — |

**Not done:** splash, way home, `<noscript>`, `og:`, `canonical` — they depend on
the **V7 route**, which is Matt's ruling.

---

## Target B — patched and parked

| item | what changed | artefact | red/green | planted failure |
|---|---|---|---|---|
| **C1** | shape guards inside both normalizers | `C1` — 21 cases, release fails 2 | red→green | yes (drop Y1a/Y1b) |
| **C2** | autostart block removed | `C2` — 5 parameter sets, release fails 5 | red→green | yes (drop Y2) |
| **C3** | `window.__COA_QA` removed in full | `C3a`, `C3b` | red→green | yes (drop Y3) |
| **C3** | the game still deploys, driven through the real UI | `C3c` | asserted | — |
| **C4** | clearance derived from the drawn HUD | `C4` — release fails **8 of 8**, patched **0 of 8**, 12 px gap everywhere | red→green | yes (drop Y4a–d) |
| **C5.4** | viewport no longer blocks pinch zoom | `C5.4` | red→green | yes (drop Y5d) |
| **C5.5** | reduced motion from the OS, user choice still wins | `C5.5a`, `C5.5b` | red→green | yes (drop Y5e1) |
| **C0** | the fence | `C0` — shelf, both audience pages, curation renderer | ASSERTED | it exists to go red if anyone adds the route |

**Deliberately not done:** the storage-key rename (`COA-TRANSCRIPT-1` may be in
the wild and atomic migration was not proven), `canonical`, and every conformance
item that needs the shelf conventions. **Mode names and in-game copy untouched.**

---

## Target A — P0 resolved

| item | what changed | artefact | result |
|---|---|---|---|
| **P0.1** | 23 routes measured in a browser; every same-origin request recorded | `qa/P0_estate_injection_census.json` | 12/23 request `/hud.js`, **0** request `/theme.js`, **11 request nothing**, **no game ships a CSP** |
| **P0.1** | corroborated independently by a second sweep reading the estate's own tooling | `verify_hud_on_games.py --self-test` and one full run | **334 assertions passed, 0 failed**; 23 routes = 12 wired + 1 region-only + 10 declared. Same numbers, reached the other way round |
| **P0.2** | **the CSP is unchanged — no `'self'` on any directive** | `P0.2` | PASS |
| **P0.3** | the inline exit region stamped by the estate's own generator | `P0.3a` | PASS — 11 targets, 0 divergent |
| **P0.3** | zero CSP violations at boot and through one live descent | `P0.3b`, `P0.3e` | PASS |
| **P0.3** | the region **executed** — side effect, not tag | `P0.3c` | PASS |
| **P0.3** | canvas painting after the descent | `P0.3f` | PASS — 120,000 lit pixels |
| **P0.3g** | **PLANTED FAILURE: `<script src="/hud.js">` is BLOCKED** | `script-src-elem`, `errorText: csp` | **seen red** |
| **P0.3h** | and removing it restores a clean run | `P0.3h` | PASS |

**P1–P5 not attempted.** Placement is the larger half and half-proving it would
be worse than not starting.

**One estate finding, recorded not fixed:** `data/hud-coverage.json` records the
canonical `scriptLine` — `<script defer src="/hud.js"></script>` — and a repo-wide
grep shows **nothing reads it**. The tag is a per-file literal, committed into ten
game pages by one commit in August and maintained by hand since. A canonical
string that no code consumes is a convention with nothing holding it in place.

---

## Estate red count

**Before: unchanged. After: unchanged.** No target added a red, and no target
fixed one that was already there — the three pre-existing reds
(`render_audience_homepages --check`, `build_mbm_search_index --check`,
`verify_design_inheritance`) were explicitly out of scope and are untouched.

The one red this pass *records* is Target D's 22-of-38 unnamed inputs. It is
pre-existing, identical on the release build, and reported through a distinct
exit code (3) so it cannot be mistaken for a failure this work caused.

---

## The three rulings that closed the human items

**Class of Ashes — parked, and C0's fence is the position rather than a holding
pattern.** Not because the content is too violent — by the standard of what
fifteen-year-olds already play it plainly is not, and the enemies are an
insectoid Brood and a construct boss rather than people. The question is whether
a teacher should publish, under his own name, on the site his SEMH pupils reach
through lesson links, a game set in a school under attack with a mode called
PROTOCOL LOCKDOWN. Lockdown is not a neutral word in a school building. The cost
of parking is nothing; unpublishing is much harder than not publishing. **The
technical work proceeds regardless** — a parked artefact with a known boot-kill
is still a liability, and these fixes are the reference material for the next
pack that repeats them. If it is ever wanted on the shelf the route is a
**re-skin**, not a debate about content: strip the school framing and it
publishes on ordinary merits. That is a content commission with its own budget.

**Chemistry Lab — the Lessons repo, as a science practical instrument,
co-located with the FieldOps labs.** Not the Games shelf, and not Apps/Teacher
tools. The precedent is already ruled: FieldOps split labs 01–04 into Lessons
beside the science and sent only the Teacher Studio to Apps, because a lab is a
lesson instrument and a studio is a teacher tool. **VCL is a lab** — pupils do
the practical, it carries a 40-minute Introduce→Explore→Do arc, it is not
teacher-directed. The landing is sequenced, not blocked: the co-location path
does not exist until the FieldOps placement merges, and the route attaches to
**v0.4.1**, not to #116. #116 is the **reference diff** for re-applying these
fixes to v0.4 — which forks the unpatched v0.3 baseline with all six defects
surviving verbatim — not a shipping artefact.

**The URL carries the setup. It never carries the pupil's work.** Out of
`serialisableState()`: the name, the notes, the phase answers, the drawing
strokes. Retained: bench, apparatus configuration, sample codes, teacher fault
injection — everything Share exists to hand over. Share hands the URL out, so a
teacher sharing a bench setup would otherwise be shipping whichever pupil's
answers were last typed.

**No persistent graded record attached to a pupil's name**, in any of the three.
The estate already settled this in its own governance copy — *"not grades,
diagnoses"*, *"do not turn action counts into ability labels"* — and holding that
line in the science instruments while dropping it the moment the same pupils
meet a game would be incoherent. For an SEMH cohort a stored DISTINCTION /
MERIT / PASS beside their name is a shame trigger they cannot escape by playing
better. **Record what was done and observed, not what it was worth** — which is
the same move the marking fix already makes.

## Owed to a human

Items 1, 2 and 6 are **ruled** — see above. What is left is sequenced, not
blocked:

1. **v0.4.1** as its own order, with the removal matrix written in from the
   start rather than retrofitted, and #116's diff as the re-application
   reference.
2. ~~The FieldOps placement~~ — **done.** The co-location path VCL cites is
   **`Science_Teesside/Build/v4_fieldops/`**, quoted here so the VSL order does
   not re-derive it.
3. **Scrap Core P1–P5**, if placement is wanted.
4. **Play them on the phone.** Scrap Core: one descent to a titan. Chemistry
   Lab: the microscale bench in landscape, and Share on a real link.
5. **Eyes on the Scrap Core card copy and hue** — not written, not drafted.
6. **The fun question**, for all of them.

### Out of scope, and unchanged

`data/hud-coverage.json`'s `scriptLine` is a canonical string with **no
consumer**, against ten hand-maintained copies of that literal. It will drift.
The fix is one assertion comparing each declared route's literal against the
canonical string, or deleting the field. **It is R0.1 inverted — a declaration
nothing exercises, rather than a gate nothing runs.**


---

## The P2 split, and which branch carried which half

| half | repo · branch | path |
|---|---|---|
| labs 01–04 | Lessons · **`claude/close-order-seven-items-wdfhdf`** | `Science_Teesside/Build/v4_fieldops/` |
| 00 Teacher Studio | `Matt-s-Apps-` · `claude/fieldops-teacher-studio` | `FieldOps_Teacher_Studio.html` |

**Stated plainly because it was not planned: the labs went onto the ledger
branch.** There is no separate labs branch, and creating one retroactively would
split a proven build across two histories for tidiness. The consequence is that
the ledger's merge condition and the labs' merge condition apply to the *same*
merge, and both have to be met — which is stricter than either alone, not looser.

Transport across the split is proven **both directions**, 10 of 10, in
`tools/fieldops/evidence/split_transport.out`. Every fixture is authored by that
harness and **says so in its own filename** — the pack's twelve
`.buildmission.json` samples were never shipped.
