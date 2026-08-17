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

## R0.12 — read the artefact, not its summary

**A true summary is not evidence that the thing it summarises is complete.**
The last line of a report is the one place a defect can hide behind an accurate
statement.

*Provenance:* raised by the run of 2026-08-16 during the removal-matrix pass.
Four of the unfireable checks that pass found were found by reading an artefact
instead of its summary line, and the summary was true every time — "every
transform watched" was true while two labels were missing; "0 unexpected changes"
was true while a pattern had stopped matching. R0.12 is the generalisation of the
R0.1 family: the summary line is where an unexercised gate looks identical to an
exercised one.

*Landed 2026-08-17, and late.* It had been cited by **four** separate orders —
the P2 finish, the B2 conformance order, the closing order and the #120 merge
order — while being defined in no ledger — a rule everything was audited against, missing from
the record that governs. That absence is now its own rule, R0.17, and the one
reporting defect counted under **§S2** is R0.12's own failure mode: a
report that ran, was true, and buried the finding inside itself.

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

That is a different failure from the ones tabled under **§S2 — the evidence rule,
applied to this pass**, and is counted separately: those are checks that could not
fire, this is a check that fired wrongly. The second kind destroys rather than
merely fails to protect. The number is not repeated here — it is derived from the
table by `tools/verify_ledger_tally.mjs`, and a number repeated in prose is a
second place for it to be wrong.

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
rewritten or deleted.

**Counted as one row per check that could not fire, where it was found; two such
defects in one commit count twice.** A commit is an authoring artefact, not a
unit of defect, and collapsing two unfireable checks because they shared one
would measure working habits rather than exposure. **The table below has 12 rows:
10 in these gates, 1 Matt-side, 1 found by re-reading an artefact (10 + 1 + 1 =
12).** `tools/verify_ledger_tally.mjs` derives that from the table on every run,
because this file has now stated a wrong count twice — nine above a table of ten,
then twelve above a table of thirteen.

Four of the twelve share a shape: **the fix was fine and the check was wrong, and
only removing the fix could tell the difference.**

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

### And **1 reporting defect of the same family (R0.12)**, counted separately

Held to a different predicate, because it is a different thing: *a report that
ran, was true, and buried the finding inside itself.* The **checks that could not
fire** table is checks
that **could not fire**. This one fired, and told the truth, and that was the
problem — so counting it there would have made the headline number describe two
species at once. It sat in that table as a thirteenth row for two revisions,
which is how the prose came to say twelve above thirteen rows.

| the report that was true and buried it | how it was caught |
|---|---|
| `assert_unchanged`'s text-delta report printed the **whole** delta — every authorised string alongside the one that was not — in the same commit as the row above | printing the *difference* instead immediately exposed a mismatch on a **non-breaking space** nobody could see |

**The button label and the overlap predicate are worth reading twice.** In both
the *fix* was fine and the *check* was wrong, and only the removal matrix could
tell the difference. A gate that goes green on a reverted fix is not evidence
about the fix — it is evidence about the gate.

**Final matrix state: every transform on every target is watched.**
**C 18/18 and B 10/10 are countable from the tables quoted below — 18 ids and 10
rows, counted, not asserted.** **D reported 16/16 by the Target D removal-matrix
run recorded in [#115](https://github.com/MattRoper1977/Lessons/pull/115); the
matrix is not quoted in this ledger and the figure is not countable from this
artefact.** Searched for it at `tools/fieldops/evidence/*.out`, in the tracked
tree, and in the surviving run output at `/tmp/p2matrix.out` — which holds **6**
rows, T1 to T5b, being the truncated output of a 19-transform run that died
before finishing. The claim is kept and downgraded rather than deleted: a number
no reader can reproduce from the page it sits on is not evidence, and deleting it
would lose a result that was genuinely reported.

Measured with a label that fires, rather
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

The Class of Ashes park, the Chemistry Lab route and the graded-artefact question
are **ruled** — see **R0.11**, **§S2** and the target sections that carry each
ruling. What is left is sequenced, not blocked:

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

### ~~Out of scope, and unchanged~~ — closed, see the addendum

`data/hud-coverage.json`'s `scriptLine` was a canonical string with **no
consumer**. **It is R0.1 inverted — a declaration nothing exercises, rather than
a gate nothing runs.** ~~against ten hand-maintained copies~~ — **twelve**, and
the ten was the exclusion count; the addendum settles that by name. Closed by
`tools/verify_hud_script_line.py`, which derives the route set from the coverage
record at run time and is proven red on each route individually.


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

---

# ADDENDUM — the close-order fixes

Written after the §3 readback, because that readback landed two fixes that were
correct in substance and unproven in coverage, and one fix that did not do what
its name said. Nothing below disputes a verdict already recorded. All of it is
about whether the evidence for those verdicts can go red.

## R0.14 — a destructive check must match the claim, not the shape

*A check whose action is destructive must (a) match on the **claim**, never on an
identifier's shape, (b) be **dry-run by default**, with deletion behind an
explicit flag, and (c) **report candidates for ruling** rather than act on them.*

The cause: the stale-evidence sweep's first run reported four stale subjects —
**`T10a`**, **`T10b`**, **`X0`** and **`X1c`**. All four exist. `T10a` and `T10b`
are control ids in a controls table. `X0` and `X1c` are row labels in the
split-transport report, where the subject of the row is named in the row text and
the id is only a label. The sweep had matched an identifier's shape.

This is a **different species from the twelve**. The twelve were checks that
could not fire. This was a check that fired wrongly, and had `--apply` existed at
that moment it would have deleted live evidence. A check that fails to protect
costs you the protection. A check that fires wrongly costs you the thing it was
protecting.

The same defect then reappeared **inside the fix for it**, one layer down: the
rewritten sweep's transform resolver tested for `swap('T4'` and reported `T4`
stale, because `T4` is declared with `inject(`, not `swap(`. Matching the shape
of a declaration rather than the fact of one. It is caught by a fixture now.

## R0.15 — the fix for a false positive must ship a positive control

*Narrowing a predicate until the false reds disappear is indistinguishable, from
the outside, from breaking the check.*

This is not hypothetical, and it is the rule this addendum exists to record. The
sweep's **second** version narrowed to removal-matrix rows only. The four false
positives went away. So did every true positive: the tracked corpus contains no
matrix row at all, so both evidence files returned NOT APPLICABLE and the
headline read `FORWARD 0 stale`. **Version 2 was reported as a fix and was a
check that could no longer fire.** It was caught by asking the question R0.15
demands — what would this find if something were stale? — and the answer was
nothing.

Version 3 matches the claim: a (form, subject, resolver) triple read from the
row's own grammar, with six forms, each grounded in a shape that actually occurs
in tracked evidence. `--self-test` authors **three** genuinely-stale fixtures, of
three different shapes, and requires all three to be caught by name:

| fixture | shape | caught |
|---|---|---|
| `T7b` | subject **deleted** | STALE — SUBJECT ABSENT |
| `T9` | subject **renamed** (`build.mjs` now declares `T9renamed`, so a substring test would call it live) | STALE — SUBJECT ABSENT |
| `P2.9gone` | subject exists, **claim** does not — the row asserts `T1` moves a control that is no longer in `controls.mjs` | STALE — SUBJECT ABSENT |

…and on the same rows, `T1` and `T4` must come back **not** stale, and the four
regression subjects must come back not stale with their reasons named. All
seven hold. Over the real corpus: **0 stale · 24 live · 13 row labels correctly
not judged · 0 files matching no form**, and that zero now means something.

Default run reports and exits 0. `--apply` deletes only a file in which *every*
claim names an absent subject, and refuses anything outside `evidence/` or `qa/`.

## The twelve versus ten, settled by name

The census split 23 routes as 12 wired + 1 region-only + 10 declared, and an
earlier note described the canonical literal as hand-inserted into **ten** game
pages. Those two numbers were never in conflict; the note had read the wrong
list. **The ten is the exclusion count.** The wired set is twelve and always was.

- **ALL (23)** — root-level game routes in `data/mbm-search-index.json`
- **EXCLUDED (10)** — `hud-coverage.json .excluded[].route`: `/apexpool/`,
  `/apexrally/`, `/biopunkhive/`, `/echovault/`, `/neonmeridian/`, `/neonsync/`,
  `/novasiege/`, `/ouroboros/`, `/rallyvector3d/`, `/relicforge/`
- **REGION-ONLY (1)** — `/emberwild/`
- **A = W = D − region-only (12)** — `/apexgolf/`, `/apexkick/`, `/apextennis/`,
  `/auroralinks/`, `/fracture/`, `/hyperdraft/`, `/luminahaven/`, `/medevac/`,
  `/neonbreach/`, `/neonturf/`, `/olympics/`, `/voxel/`

`D \ A` = `{/emberwild/}` · `A \ D` = `{}` · `W \ A` = `{}` · `A \ W` = `{}`.
The single delta is the region-only route, and it was the finding: `/emberwild/`
is neither excluded nor wired, its status lived only in prose, and the first cut
of the assertion **skipped** it — indistinguishable from a route whose HUD had
gone missing. `inlineExitRegion.regionOnly` now declares it, and the exemption is
audited rather than free.

**Per-route mutation matrix:** 36 rows, two mutation kinds on each wired route
(`drop-defer` for attribute-level comparison, `corrupt-src` for comparison
against the canonical string rather than against "a script tag exists"), plus
`strip-region` / `wire-a-hud` on the region-only route and `wire-a-hud` on each
excluded route. **36 named reds, 0 silent passes, 0 partial assertions, all
restored, final full run green.** Three derivation controls fire first: declaring
a route raises `|A|`, excluding one lowers it, and an empty or malformed
`hud-coverage.json` exits 2 rather than iterating zero routes and reporting
success.

## The corrected `.gitignore` position: ignoring is not untracking

`.gitignore` has no effect on files git already tracks. The site repository was
tracking **seven** files under `audit-output/audience-discovery/` — six PNGs and
one `results.json`, added in `c1bfa98`. The rule alone changed nothing about
them. `git ls-files audit-output/`: **7 before, 0 after**, all seven now covered
by `.gitignore:14`, with a probe file under the directory absent from
`git status --porcelain`. Lessons: **0**. `Matt-s-Apps-`: **0**.

**What §3.2 found.** All seven were inspected before anything was committed —
rendered, not judged by filename. Six are above-the-fold screenshots of public
marketing surfaces (the root discovery page desktop and phone, `/for/pupils/`
desktop and phone, the no-JS organisation homepage, `/education-hub/` at 320px)
and the seventh is a `results.json` of assertion names and route paths. **No
pupil name, no roster, no class list, no initials against performance, no
`mbm_hud_names` content on screen, in any of the seven.** No history rewrite is
called for, and none was done.

**And the part that mattered more than the cleanup.** Untracking those files
would have silently killed a live gate. `mbm-audience-discovery-closeout.yml`
asserted `git diff --quiet audit-output/` after its deliberate-failure control
run — a step that exists because such a run once wrote into the committed
artefact and had to be reverted by hand. `git diff` says nothing whatever about
an untracked path. **The tidying commit would have left that assertion passing
for ever, on a hazard it had stopped watching** — the thirteenth instance of the
species, introduced by the fix for another instance of it. The claim is
re-expressed rather than deleted, per the BD4 rule: hash the directory before and
after. Same claim, no dependence on what git tracks, and strictly wider — it
catches a created file and a deleted one, which the diff never could.
`tools/verify_audit_output_guard.sh` is the control for that control and proves
both halves, including that the retired predicate passes over a clobbered file on
an untracked tree.

## Why the audit output was committed at all

`c1bfa98` added it alongside a Supabase pinning change; the generator's default
output path **is** `audit-output/audience-discovery` (`ARTIFACTS` in
`tools/verify_audience_discovery_browser.py`), and the workflow uploads that same
path as an artefact — so the tool was never writing somewhere it should not have
been. This was output committed once and then depended upon by a gate, not a
papered-over path bug: which is exactly why untracking it needed the gate
re-expressed in the same commit rather than after.

---

# ADDENDUM 2 — the residue

Follows the close-order addendum above, which is merged at `a46d9b9`. R0.14 and
R0.15 are already there in full and are not repeated. This carries what the
close order left, and one thing it left is an admission.

## R0.16 — no removal without a reader census

*Before anything is deleted, untracked, ignored, renamed or excluded, enumerate
what reads it — code, gates, workflows, manifests, and documents that are
themselves asserted — and report the census with the removal. **A removal with an
empty census is safe; a removal with a non-empty census is a re-expression,
never a delete.***

Its own rule rather than a fourth limb of R0.14, because R0.14 governs checks
whose *action* is destructive and this governs **any** removal, by anyone,
including one a human orders.

**The evidence is `audit-output/`.** `git rm --cached -r audit-output/` was
ordered for tidiness. Nothing asked what read those files, and one thing did:
`mbm-audience-discovery-closeout.yml` asserted `git diff --quiet audit-output/`
after its deliberate-failure control run, a step that exists because such a run
once wrote into the committed artefact and had to be reverted by hand. `git diff`
says nothing whatever about an untracked path. The removal would have converted a
live gate into a permanent green — **the fix for one instance of the species
creating the next.**

The second piece of evidence is older and is mine: the ruling on `scriptLine`
read *"make the field load-bearing with one assertion, or delete it; either is
acceptable"*. Under R0.16 the delete branch of that ruling was **unsafe as
stated**, because it offered a removal without requiring the census first. It
happened to be harmless there. It was not harmless in `audit-output/`.

## R0.17 — rule identifiers are allocated in the ledger, never in an order

An order may cite only ids that exist in the ledger **at the time it is written**.
Citing an unlanded id is a broken reference, not a forward declaration.

*Evidence:* **R0.12 was cited by four separate orders and defined in no ledger.**
Counted by grepping the four order documents, not carried over: the order that
wrote this rule said three.
Not a renumbering — an absence, and the rule everything in the seven-items close
was governed by was missing from the record it governs. It is landed above, with
its text and its provenance unchanged, and this rule exists so the next one is
not written the same way.

## R0.18 — preconditions are measurements, not quotations

An order states how to **derive** a precondition; it never states the value the
precondition had on the day the order was written.

*Evidence, and it is Matt's to own:* the merge order of 2026-08-17 pinned PR #120
at head `09f04e0` and asserted docs-only scope. By run time `09f04e0` was five
commits stale, the PR was closed and merged at `a46d9b9`, and the scope was **57
changed paths of which 56 were not documentation** — a workflow file, four placed
labs, the whole tools tree, staging and evidence files, 36 scratch deletions. The
run stopped on the precondition rather than adapting to it, which was correct.
A quoted precondition is a measurement with a timestamp nobody checks.

## The fix is where the next defect is — four in one pass

Not three. R0.14, R0.15 and R0.16 all have the same shape, and this pass produced
four instances of it, each found by the thing built to find the last one:

1. The sweep's own resolver called **`T4`** stale, testing for `swap('T4'` when
   `T4` is declared with `inject(` — R0.14 recurring inside the fix for R0.14.
2. The `audit-output/` gate, above — R0.16's founding case.
3. The sweep's first CI run reported **`FORWARD 0 stale` over three repositories
   it could not see**, because the roots were absolute container paths. Its
   self-test still bit, so the job was green and the sweep's line was vacuous.
4. The `NO FORM MATCHED` control, added so a row shape nobody anticipated would
   be *reported* rather than skipped, immediately found **twelve real rows in the
   tracked corpus that the sweep had been passing over in silence** — the whole
   `U1`–`U7` vocabulary of `assert_unchanged`, and every `A0 PASS` row, because
   the row pattern demanded two spaces before the verdict and knew only four
   verdict words. Three widenings followed, each reported by the control rather
   than discovered by luck.

## What "0 stale" now means, and what it costs to say it

- **Declaration forms are enumerated, not known.** Every `<callee>('<ID>'` site in
  the builder is a declaration, whatever the callee is called. A transform found
  in no recognised form is `UNRESOLVED — FORM NOT RECOGNISED`, **never** `STALE`,
  because STALE is what `--apply` acts on. *"I cannot see it"* and *"it is not
  there"* are different answers and only one of them justifies a removal.
- **Control:** a transform declared with double quotes — a seventh form nobody
  wrote a rule for — comes back `UNRESOLVED`, the unresolved count is non-zero,
  it is **not** among the removal candidates, and the run exits 2 rather than
  passing with one outstanding. Restored, unresolved returns to 0.
- **Assessed roots are asserted.** `--require-roots=3` exits 2 unless three were
  read. Control: point one root at nothing → exit 2 naming it; restore → 3/3.
  Per repo, what was read: **Lessons 2 evidence files / 24 claims judged · site 0
  / 0 · `Matt-s-Apps-` 0 / 0.** A total is not three numbers, and two of those
  three estates keep no tracked evidence at all — which is a fact about them, not
  a clean bill.
- Corpus today: **0 stale · 24 live · 31 row labels correctly not judged · 0
  unresolved · 0 rows matching no form.**

## Merged is not served — and it is still not proven

> **SUPERSEDED 2026-08-17, and left standing (R0.13).** This entry was true when
> written and is the record of why the instrument exists. Two things below have
> since changed and are corrected at the end of this ledger, not here: serving
> **is** now proven on `main` (run `32022110081`), and the network legs described
> below have been removed from `verify_fieldops_served.mjs` — they treated the
> Studio's `301` as a failure. `tools/verify_served.mjs` holds R0.4 for these
> routes now; what remains in the older file is the declaration check, D1.

`a46d9b9` and `2e2de98` merged. **Nothing has yet confirmed the Pages build
serves them.** `tools/verify_fieldops_served.mjs` is the instrument, and it is
written because a human tapping a URL is not a gate and does not run again next
month.

- **The route set is derived** from `tools/fieldops/build.mjs`'s `LABS` and
  `STUDIO`, evaluated rather than grepped. That is canonical in the strong sense:
  the builder cannot emit a lab it does not name, `assert_unchanged`'s U1 pins
  that dropping every transform reproduces release byte for byte, and **no
  manifest in the estate lists these files** — `resources.json` does not, and the
  site's shelf holds games. It is then cross-checked against the placed directory,
  so a lab declared and not placed, or placed and not declared, is red before a
  byte is fetched.
- **`derive_live_routes.mjs` cannot cover them and should not be made to.** It
  derives games the *site* serves and classifies anything under `/Lessons/` as
  another estate, deliberately, because neither repository holds the other's
  files. The four labs are Lessons files and the Studio is an Apps file. They
  were invisible to it and always were; the derivation belongs on this side.
- Asserted per subject: **HTTP 200 · no redirect chain · sha256 identical to the
  merged blob.** 200 alone is not the assertion — a stale deploy answers 200 all
  day.
- **This instrument's own first run was wrong in the estate's favourite way.** It
  accepted the container proxy's `403` as a reachable origin and printed five
  FAILs and a passing 404-control about a deployment it had never spoken to. The
  root must answer **200**; anything else is a fact about the runner and is
  INCONCLUSIVE. The absent-route control now requires **404 exactly**, not merely
  "not 200", because "not 200" passes in any environment that blanket-refuses.

## The zero-check census — 12 of 21

PR #120 ran zero checks from two stacked causes. The generalisation, measured
across all three estates:

| repo | open PRs | zero check runs |
|---|---|---|
| Lessons | 13 | **9** — #9, #17, #35, #43, #45, #93, #116, #117, #118 |
| `mattroper1977.github.io` | 6 | **1** — #25 |
| `Matt-s-Apps-` | 2 | **2** — #2, #4 |

**Twelve open pull requests carry a green tick that means nothing was asked.**
Including all three of the close order's own dispositions — #116, #117 and #118 —
which were reported as verified and have never had a check run against them.
Their evidence is real and local; what is absent is the trigger limb.

`tools/pr_check_census.mjs --gate` is the standing assertion, and it names the
cause per PR: conflicted (no merge ref, so no filter could have saved it), filter
miss, draft, or no applicable workflow.

## `/emberwild/` — the order's premise, corrected

The residue order records the region-only exemption as resting on *"an unfixed
accessibility defect"*. **Issue #149 is closed as completed**, by #155
(`bc67b82a`), and it was not closed by declaring anything: the defect was
repaired in the game. `bindKeyboard` had bound Tab to the menu and
`preventDefault`ed it, and swallowed Enter with the same handler, so a keyboard
player reached **0 focusable elements in 60 presses** past 14 visible controls.
Tab is no longer a game key and the handler stands down on a control. The exit is
reached in **13** presses and navigates to `/games/`, against `/relicforge/`'s 8.
Adding `/hud.js` was tried in a scratch copy and reached **0 of 60** — it would
have turned the gate green and left the player exactly as stuck.

`verify_inline_exit.mjs` is run by two named workflows, so it is not hand-run.
**But it was not judging `/emberwild/` at all**: its targets derived from
`.excluded` alone, 13 routes, and the region-only route is in neither list. Not
unwatched — `verify_hud_on_games.py`'s three-way classify holds that region to
*reaching and navigating* — but the gate that measures 44×44 as rendered, on-top
where a finger lands and reachable-by-Tab was not measuring the one route whose
numbers #149 turned on. Derived from both keys now: **13 routes → 14, 492
assertions → 529, 0 failed.**

## B2 — stated plainly

**Abandoned, and no result survives.** The conformance workflow was last observed
with 5 of 8 agent results returned; its journal and transcripts are not on disk,
and no conformance matrix or per-app verdict exists anywhere in the working tree
or the scratch. **The ledger merged at `a46d9b9` is therefore incomplete against
its own order: §5 of the close order required the B2 conformance matrix and three
per-app verdicts, and neither was produced.** That is recorded here rather than
left to be inferred, because an incomplete ledger that does not admit it is worse
than an open item.

The 19-transform result **is** in the ledger and holds, re-run in CI on the merge:
`assert_unchanged` reports **0 unexpected changes across U1–U7**, all 19
transforms dropped, release reproduced byte for byte.

## Evidence that survives the tooling

Job-level success was accepted once for PR #165 because only the tail of an
861-line log could be fetched. Every gate in `fieldops-p2-and-sweep.yml` now
writes its counts, predicates and per-control results to `$GITHUB_STEP_SUMMARY`
**and** uploads them as an artifact, so step-level evidence is a fetch rather than
a log scrape for every future run.

## Still open, and named so it cannot be inferred

- The serve proof has **not yet run against production**. It runs on push to
  `main`, weekly, and on dispatch; from this container every origin answers 403.
- **Twelve PRs with no checks.** The gate exists; the twelve are not fixed.
- B2, above.
- `close-fixes/combined-614f4d8` — see the branch table.

## Branch dispositions, and one SHA recorded because a tag would not push

| ref | SHA | disposition |
|---|---|---|
| `claude/hud-coverage-scriptline-load-bearing` | **`614f4d8`** | **Superseded, kept, never force-pushed.** Carried both §2 and §3 payloads on one branch. **It never had a pull request** — nothing to close. |
| `claude/hud-coverage-scriptline-derived` | `afa7c7d` | the assertion, rebuilt over a derived route set — PR #165, open, CI green |
| `claude/untrack-audit-output` | `7befc56` | **merged** — `8a90d18` |
| `claude/close-order-seven-items-wdfhdf` | — | **merged** — `a46d9b9`; restarted from `main` for this residue |
| `Matt-s-Apps- · claude/fieldops-teacher-studio` | `0adb400` | **merged** — `2e2de98` |
| `claude/vcl-spatial-v03-patch` · `claude/coa-zero-period-patch-parked` · `claude/scrapcore-v10-placement` | — | unchanged: reference, parked, P0 only |

**The tag would not push.** `close-fixes/combined-614f4d8` was annotated locally
and `git push origin close-fixes/…` returned **HTTP 403**: this session's
credentials carry branch push and not tag push. A local tag in a disposable
container is a countdown, not preservation, so it is not relied on.

The order offered deletion as the alternative. **Refused, under R0.16 applied to
itself:** the reader census for that branch is not empty — the §READBACK
describes it, this ledger now points at it, and it is the only remote copy of the
combined state. A removal with a non-empty census is a re-expression, never a
delete. The branch stays and the SHA is written here, which is what the record
needed the tag for.

---

# CLOSING ENTRY — 2026-08-17

Written last, and containing only what was measured in this run.

## R0.17, R0.18 and R0.19, each with its provenance

R0.17 and R0.18 are landed above in id order. **R0.19 joins them**, and all
three came from the same place: an order was wrong, the run stopped, and the
stop was right.

- **R0.17** — from R0.12's absence. Cited by four orders, defined in no ledger.
- **R0.18** — from the stale-precondition stop. A merge order pinned a head five
  commits behind and asserted docs-only over 57 paths of which 56 were not.
- **R0.19** — from the post-squash force-update.

## R0.19 — any operation that moves a ref reports the ref table, before and after

*And states what would have been lost.* A force-update reported as "pushed" is
indistinguishable from one that ate work.

*Provenance:* after #122 was squash-merged, the branch label still pointed at its
own pre-merge history and had to be fast-forwarded onto the merge commit. The
report gave remote `4259c15` → `b6f92ca`, tree byte-identical, nothing discarded
that was not already in main, unpushed commits 0. **That is the standard, not a
courtesy.**

## Serve — the route set, and the verdict

**29 routes derived**, composed from three canonical records with no hand list
anywhere:

| group | count | derived from |
|---|---|---|
| site | **23** | the site repo's own `tools/derive_live_routes.mjs`, **invoked**, reading the canonical shelf in the `MattRoper1977/Games` repository |
| lessons | **5** | `tools/fieldops/build.mjs` `LABS[]` (4), plus the hub read off the labs' own NAV-1 `href` rather than assumed (1) |
| apps | **1** | the same builder's `STUDIO` |

Predicate, stated so the 29 can be re-derived: *every game the site's P0 deriver
emits from the canonical shelf, plus every lab the FieldOps builder names and the
hub their NAV-1 link resolves to, plus that builder's Studio.*

**The assertion is byte-identity of the served response to the committed blob.**
200 is a precondition and never the verdict — every serve failure this estate has
actually had would have passed a 200-only check.

**Verdict from this container: UNVERIFIED.** All three origins answered **403**
to the runner's proxy, not 200. That is a fact about the runner and is reported
as one; nothing is claimed about the deployment. The gate runs in CI on push to
`main`, weekly, and on dispatch.

### Two defects found inside this gate, before it landed

The order predicted the serve check would be where this pass hid its defect. It
was, twice:

1. **A partial proxy block would have reported a whole estate as RED.** The first
   cut only bailed when *every* origin was dead; with one blocked and two
   reachable it would have marched on and called an unreachable estate's routes
   failures. A runner fact wearing a deployment verdict. Unreachable groups are
   INCONCLUSIVE now, per group, naming the status they actually got.
2. **The content-type result was buried in a detail string** rather than reported
   as its own outcome — a true line that hides a finding inside itself, which is
   R0.12 in the gate written to satisfy R0.4. It is its own reported field now,
   and a mismatch is a red.

## The VSL route ruling — approved, and not created

**`Science_Teesside/Build/virtual_science_lab/`**, against the landed FieldOps
path `Science_Teesside/Build/v4_fieldops/`. Four tests, run against the tree on
main, all **PASS**:

| test | result |
|---|---|
| **sibling, not tenant** | both under `Science_Teesside/Build/`; the candidate is not inside `v4_fieldops/` |
| **named for the instrument, not the version** | no `v0_4`, no `PRO`, no date — versions live in the file and here |
| **no collision** | 0 tracked files under the candidate; no root-level `virtual*`/`vsl*`/`vcl*` directory to shadow |
| **no empty route** | v0.4.1 does not exist in the tree, so **the directory was not created** |

**The condition, which is the point of the fourth test: it is created only when
v0.4.1 exists.** No placeholder, no index stub, no "coming soon" — an empty route
is a 404 waiting for somebody to link it.

*Adjacent but distinct, so a later reader does not conflate them:* a root-level
`chemistry/` directory holds 9 teaching lesson files including
`L3c_VirtualLab_AcidsAlkalis (2).html`. Those are lessons; the VSL is an
instrument. The candidate does not shadow them and is not a home for them.

## The tally control, on main

`tools/verify_ledger_tally.mjs` runs on main and its three mutation controls each
go red there — re-run against main's tool and main's ledger, not quoted from the
branch: prose number changed → red, row added → red, row removed → red, restored
→ green. Prose N=12, table 12 rows, sub-counts 10+1+1.

## Addendum, 2026-08-17 — one tool re-expressed, and a census that under-reported

Post-close cleanup of the one item this arc left in a wrong state rather than
merely unfinished.

**`verify_fieldops_served.mjs` was giving a wrong verdict, not just a redundant
one.** It treated any `3xx` as a FAIL, which is what reddened the Teacher Studio
at `b6f92ca` — the `301` there is the user Pages site redirecting `github.io` to
the custom domain, and the bytes at the far end are identical. Two tools fetching
the same routes with different opinions about redirects is how an estate acquires
a verdict that depends on which gate you ask. **The census under R0.16 came back
non-empty** (this ledger, the file, and `.github/workflows/fieldops-p2-and-sweep.yml`
line 194), so it is re-expressed and not deleted: the network legs are gone, the
declared base URLs went with them, and what is kept is **D1** — the builder's
`LABS[]` and the placed directory naming the same files — because that is the one
check here that nothing else in the estate makes.

**D1 had never been shown able to fail.** The self-test asserted that D1 said
PASS, which is not the same thing, and D1 is now the file's only reason to exist.
A control is added: declare a lab that was never placed, and D1 must go red *and
name it*. It fires. The mutation is applied to the **builder**, restored in a
`finally` — deleting a placed lab to prove a point would be a destructive check
on a shipped file (R0.14), and the builder reaches the same verdict without
touching one.

**And the census itself was wrong first.** My initial reader census used a
filtered grep and missed the workflow reference under `.github/` — it found two
readers where there are three. An unfiltered grep found it. For a census whose
whole job is to gate removals, **under-reporting is the dangerous direction**: it
is the error that reads as permission. R0.16 censuses are run unfiltered.

## What remains open, by name

- ~~**The serve result itself.**~~ **CLOSED 2026-08-17.** Run
  [`32022110081`](https://github.com/MattRoper1977/Lessons/actions/runs/32022110081)
  on `main` at `0352995`: **29 served byte-identical · 0 red · 0 inconclusive, of
  29 derived · content-type 29 as expected, 0 not**, and all four controls FIRED
  in the same run. Read from the job log, not from a green tick. The Studio
  answers through a named chain —
  `github.io/Matt-s-Apps-/FieldOps_Teacher_Studio.html -> 301 -> madebymatt.uk/…`
  — and the bytes at the destination match, which is the case the older tool got
  wrong.
- **Twelve zero-check pull requests**, declared in `tools/zero_check_baseline.json`
  and ratcheted so the thirteenth reds. Recorded, not repaired.
- **B2 conformance** — abandoned, no result survives, and the ledger says so.
- **`verify_inline_exit.mjs`** — the gate that proves a child's way out of eleven
  games is keyboard-reachable. It runs in two named site workflows; what it does
  not have is a Lessons-side trigger for the three Lessons games it judges.
- **VSL v0.4.1** — its own order. v0.4 still carries all six V-findings verbatim,
  including **V2: pupil name and notes in the URL that Share hands out, at an
  SEMH provision.**
