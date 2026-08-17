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

### And **2 reporting defects of the same family (R0.12)**, counted separately

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
| the zero-check census reported **"12 draft, 0 not"** over rows showing three drafts. The baseline subtraction had been folded into the label — the draft count was derived as `zeroes − gated` *after* `gated` lost its declared entries — so **nine PRs recorded as open findings were reported as an expected state**. The gate never misbehaved; only the sentence describing it did | found by reading the job log of the run that produced it, on PR #124, rather than its green tick — the split is now read from the rows by one function shared with its control, and the control reproduces the retired arithmetic and requires it to disagree |

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

- ~~The serve proof has **not yet run against production**.~~ **SUPERSEDED
  2026-08-17** — it ran on push to `main` and passed; the result and its run id
  are at the end of this ledger. Left standing rather than rewritten: it was true
  when written, and the container's 403 that prompted it is still true.
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

## Addendum, 2026-08-17 (second) — the gap the 3xx fix opened, and where controls may run

**Permitting a redirect is not asserting where it ends.** The old tool failed the
Studio for answering `301` at all; removing that made the chain legal and compared
bytes at the far end. Correct, and it opened the other side: **a chain terminating
on an origin nobody asserted would have had its bytes compared there, and a match
would have read as SERVED.** A mirror or a re-pointed CNAME is precisely the case
where the bytes plausibly *do* match, so this was a hole shaped like a pass.

- **Control (e)** — a terminus outside the permitted set is **RED, naming both**
  the origin reached and the ones permitted. Checked **before** the byte
  comparison, because after it the mirror has already been called SERVED.
- **The permitted set is derived, never hand-listed:** the canonical domain from
  the site repo's `CNAME`, and `<owner>.github.io` from that repo's own remote.
  A set that cannot be derived is **INCONCLUSIVE** — an empty permitted set would
  reject every route, which is as useless as passing every route.
- **The control is a matched pair in one check**, deliberately: the rogue
  terminus must be rejected *and* both genuine origins accepted. Asserting only
  the rejection would be satisfied by a predicate that rejects everything.
- **A stale claim removed on the way past:** the comment above the origin
  constants said they "are not derivable from any file in these trees". The
  site's `CNAME` had always falsified that, and the false claim is what made a
  hand-listed destination set look like the only option.

**Where controls may run, which turned out to be the more useful finding.** The
live verdict needs the branch deployed, and a PR branch is not — that is why the
verdict leg skips there. **The controls never needed it.** (a) asks a
known-absent route for a `404`; (b) asks a real route for bytes and asserts they
differ from a deliberately mutated hash. Both use production as a *fixture*, not
as the subject, and neither claim changes with the branch. `--controls-only` now
runs **all five on every event, pull requests included**. Until this, the only
controls a PR could fire were the offline three — in the workflow written because
gates were not running where they were needed.

**D1's `finally`, measured rather than believed.** Both destructive controls in
`verify_fieldops_served.mjs` rewrite a shipped file and restore it in a `finally`.
The builder is now hashed before and after and the equality asserted — a `finally`
taken on trust is the same species as every unfired check in the table above.

## What remains open, by name

- ~~**The serve result itself.**~~ **CLOSED 2026-08-17 — CI-derived, on `main`.**
  Run [`32022110081`](https://github.com/MattRoper1977/Lessons/actions/runs/32022110081),
  job **`Merged is not served - the placed labs and the Studio`** (id `95363779146`),
  on `main` at `0352995`: **29 served byte-identical · 0 red · 0 inconclusive, of
  29 derived · content-type 29 as expected, 0 not**, and all four controls FIRED
  in the same run. Read from the job log, not from a green tick. The Studio
  answers through a named chain —
  `github.io/Matt-s-Apps-/FieldOps_Teacher_Studio.html -> 301 -> madebymatt.uk/…`
  — and the bytes at the destination match, which is the case the older tool got
  wrong.

  **The locality, stated (R0.20), because this entry and "verified locally only"
  were both true at once and a reader could fairly call that a contradiction.**
  They have different subjects. This entry is about **what `main` serves**, and
  its every figure came from CI. The "locally only" caveat was about **a branch's
  diff** — the re-expression and its controls — which had never run anywhere but
  a container. Neither claim covers the other's subject, and the entry is
  qualified rather than downgraded because nothing in it was locally derived.

  **The predicate for 29 (R0.8), which this number has never carried:** 23 site +
  5 lessons + 1 apps.
  - **site 23** — every href in the canonical shelf (`MattRoper1977/Games`
    `games.json`, **52 entries**) that the site's own P0 deriver buckets as a
    site-served game route with a directory behind it. The other **29** shelf
    entries are handed to the Lessons estate and are not site routes.
  - **lessons 5** — the **4** labs `tools/fieldops/build.mjs` names in `LABS[]`,
    plus **1** hub, read off those labs' own NAV-1 link rather than assumed.
  - **apps 1** — the same builder's `STUDIO`.
  - **Residue, named and not checked by this gate:** the deriver's five
    declared-not-derived site routes — `/`, `__FULL_HOME__`, `/games/`,
    `/site.json`, `/Games/games.json`. The serve proof inherits that exclusion.
  - **A collision worth naming before it costs someone an afternoon: the 29
    served routes and the 29 shelf entries left to Lessons are different sets
    that happen to be the same size.** 23 + 5 + 1 = 29 and 52 − 23 = 29. Nothing
    connects them.
- **Twelve zero-check pull requests**, declared in `tools/zero_check_baseline.json`
  and ratcheted so the thirteenth reds. Recorded, not repaired.
- **B2 conformance** — abandoned, no result survives, and the ledger says so.
- ~~**`verify_inline_exit.mjs`**~~ **WIRED 2026-08-17.** The gate that proves a
  child's way out of a game is keyboard-reachable judges **14 routes across both
  estates, three of which live here** — `Off_Brand`, `Charcoal`, `Axiom_Shift`.
  It ran in two site workflows only, and site workflows fire on site paths: a
  change to one of those three games in *this* repository could have broken the
  way out and no gate would have noticed. Nothing blocked it — the tool already
  accepted `--lessons`; what it lacked was a caller on this side. Added as its
  own job in `fieldops-p2-and-sweep.yml`, which carries no `paths:` filter, so
  every change here matches it. Measured before wiring, across both estates:
  **529 passed · 0 failed**, so this adds a gate rather than a red. `/emberwild/`
  is **judged, not excluded** — issue **#149** is RESOLVED, and resolved in the
  game (Tab is no longer a game key) rather than by declaring an exemption.
- **VSL v0.4.1** — its own order. v0.4 still carries all six V-findings verbatim,
  including **V2: pupil name and notes in the URL that Share hands out, at an
  SEMH provision.**

---

# Closing entry — 2026-08-17. The arc ends with main green and something watching it.

Only what this run measured.

## Rules landed, in id order, with provenance

**R0.20 — evidence has a locality, and it is stated or the claim is not made.**
A gate that has not run in CI on *this change* is UNVERIFIED, whatever it did
locally. *Provenance:* `verify_served.mjs` and the D1 control were proven on a
branch whose workflow fires only on `pull_request` and `push: main`, so its push
triggered nothing at all.

**R0.21 — a retry loop classifies before it repeats.**
Backoff is for a declared class of transient failure; any other failure is read
on its first occurrence. *Provenance:* four non-fast-forward push rejections
retried four times before being read; the cause was the remote branch still
holding the pre-squash head. **And it recurred in this run, which is recorded
rather than quietly fixed:** the branch delete below failed four times, and from
the first attempt of the retry loop the error already read `HTTP 403` — an
authorization refusal, not a transport blip. Three of those four attempts were
made with the answer already on the screen.

**R0.22 — a failure on the default branch reaches a person by a mechanism, not
by inspection.** *Provenance:* runs `32017557268` and `32018424063`, both red on
`main`, both found only because someone went and looked. **Sub-rule: cancelled is
not green and not red — it is NO VERDICT**, and it never counts as coverage.
*Provenance:* the `inline-exit` job killed by `cancel-in-progress`, whose
neighbouring greens looked exactly like coverage.

**R0.23 — a pattern states its scope and prints its match set before it acts.**
*Provenance, all three instances, all self-found:* a filtered `grep` that
under-reported a removal census by one; `git tag -l` run in the wrong repository
and reported absent, twenty minutes after that exact error was recorded here; and
`pkill -f "sleep 180"` matching its own wrapper and killing the shell. Same
defect, three blast radii — the census one gated a deletion, which is R0.10.

**Beside R0.15 — a control that reads a stable external artefact to prove the
harness can go red is not a live-deployment check, and must not be gated behind
one.** Recognising that controls (a) and (b) use production as a *fixture* rather
than as the subject converted three PR-firable controls into five.

## The merge

`#124` squash-merged as **`036b545`**, base `0352995`, single parent, matching
this repository's convention.

| ref | before | after |
|---|---|---|
| Lessons `main` | `0352995` | **`036b545`** |
| branch `claude/close-order-seven-items-wdfhdf` | `2f1fa87` | unchanged — **delete refused, HTTP 403** |
| site | `c3562478` | `c3562478` |
| Apps | `2e2de98` | `2e2de98` |

**Loss statement, proven and not assumed:** `2f1fa87` is not an ancestor of
`036b545` because the merge was a squash, so ancestry proves nothing. `git diff
2f1fa87 origin/main` is **empty** — every byte of the branch survives in main.

## The closing measurement — the failure is gone, and it is the same 301

Both red runs on `main` had **one cause, not two**: identical failure line,
identical subject, identical `7 pass · 1 fail · 0 inconclusive`.

**Before** — run `32018424063` at `b6f92ca`, job `95352744737`:

```
00_BUILD_FieldOps_Teacher_Studio.html   FAIL   served without a redirect chain
  https://mattroper1977.github.io/Matt-s-Apps-/FieldOps_Teacher_Studio.html -> HTTP 301
  -> https://madebymatt.uk/Matt-s-Apps-/FieldOps_Teacher_Studio.html.
  A redirect is not a serve; the visitor's URL is not the file's.
7 pass · 1 fail · 0 inconclusive          ##[error]Process completed with exit code 1
```

**After** — run `32027709223` at `036b545`, job `95380509725`:

```
apps  00_BUILD_FieldOps_Teacher_Studio.html   SERVED
  200 · 6678059f11fc · 55394 B · chain: https://mattroper1977.github.io/Matt-s-Apps-/
  FieldOps_Teacher_Studio.html -> 301 -> https://madebymatt.uk/Matt-s-Apps-/...
  content-type: text/html as expected
29 served byte-identical · 0 red · 0 inconclusive, of 29 derived
```

**The deployment did not change. The 301 is the same 301, to the same place. The
judgement changed.** That is the whole claim, and it is why the before/after had
to name one subject rather than report a general green.

## The watch

`tools/watch_main_runs.mjs` + `.github/workflows/watch-main.yml`.

- **Subject set derived**, never hand-listed: every file matching `/\.ya?ml$/`
  directly in `.github/workflows/` — **12 matched, 1 excluded as self, 11 judged.**
- **A watch cannot be its own witness.** Its own run is necessarily in progress
  while it asks, so it would report NO VERDICT on itself and be red forever. The
  exclusion is by path and is **printed**, because an exclusion nobody can see is
  a blind spot.
- **Three categories: PASS · FAIL · NO VERDICT.** Cancelled, skipped, timed out,
  stale, `action_required`, `neutral` and null are listed by name rather than
  swept up by an `else`, so a conclusion GitHub adds later surfaces as unknown.
- **A missing run and a failed run are different findings**, because the repairs
  differ: a failing gate needs a fix, a silent one needs a trigger.
- **Controls, each named in the output and all firing:** (a) a failed run is
  detected *and named*; (b) an empty run list exits 2, never green; (c) a
  cancelled run reports NO VERDICT, not PASS; (d) a workflow in the tree but
  absent from the run set is NEVER STARTED; (e) the watch excludes itself. Plus
  the pair proving it is neither stuck red nor stuck green.
- **`workflow_run` has no wildcard**, so its `workflows:` list must be written by
  hand — which is exactly how PR #114 came to run zero checks. It is therefore
  named **and** guarded: `--verify-trigger-list` compares the list to the derived
  set and goes red both ways, proven by dropping an entry (named `Verify
  Charcoal`) and by adding one no workflow provides.

### The surfacing mechanism, and what it does not do

Three legs in the repository: the result goes to `$GITHUB_STEP_SUMMARY`; the
check **fails visibly** on the default branch; and a red appends a dated line
here, guarded three ways — only on failure, only if that run id is not already
recorded, and with `[skip ci]` so the push cannot trigger the workflows the job
is watching.

**The human leg, stated plainly because the in-repo legs do not reach a person.**
GitHub's Actions-failure emails go to the account that *triggered* the run. These
runs are triggered by automation, so **they do not arrive in Matt's inbox**. To
make a red actually reach him, one of these has to be enabled by hand, and none
of them can be enabled from inside the repository:

- GitHub → Settings → Notifications → **Actions** → "Send notifications for
  failed workflows only", with **Watching** set on this repository; or
- a `CODEOWNERS`-independent subscription: Watch → Custom → **Actions**; or
- a webhook or an email step in the job itself, which needs a secret.

Until one of those is on, the watch converts "nobody knew" into "it is written
down where someone will see it next time they look" — which is better, and is
**not** the same as being told.

## What remains open, by name

| item | state | what closes it |
|---|---|---|
| tag `close-fixes/combined-614f4d8` | ~~exists, site repo, unpushed, annotated on `614f4d8`~~ **SUPERSEDED 2026-08-17 — the tag no longer exists anywhere, and the row above was already wrong when written.** It was annotated inside a disposable container that has since been reclaimed. `git ls-remote --tags` returns **zero tags** on all three repos, and no site clone survives; the annotation went with the container and cannot be reprinted, so §1.2's "print the annotation" is unanswerable rather than skipped. **Nothing was lost by that:** `614f4d8` is the live head of remote branch `claude/hud-coverage-scriptline-load-bearing`, so the commit never depended on the tag to stay reachable — this ledger's own branch table says so two sections up | **nothing — closed.** Not "a push from a site-scoped session": that session now has push scope to the site repo and still cannot do it, because the object is gone rather than unreachable. Recreating the tag would fabricate an annotation nobody can check against the original |
| branch `claude/close-order-seven-items-wdfhdf` | **still present at `2f1fa87`. Delete refused: `HTTP 403`** — this session's credentials can push commits but not delete a ref. Content proven identical to main, so it is clutter and not risk | a delete from a session or account with ref-delete permission, or the repo's own auto-delete-on-merge setting |
| nine declared zero-check PRs (of 21 open, 12 zero-check, 3 draft) | recorded and ratcheted, **not repaired** | its own pass: rebase the conflicted ones, give the rest a matching workflow |
| B2 conformance | abandoned, no result survives, recorded as a gap in those words | re-running the conformance order |
| VSL v0.4.1 | four tests recorded above; `Science_Teesside/Build/virtual_science_lab` does not exist, 0 tracked files — correct | its own order. v0.4 still carries **V2: pupil name and notes in the Share URL, at an SEMH provision** |
| five declared-not-derived routes (`/`, `__FULL_HOME__`, `/games/`, `/site.json`, `/Games/games.json`) | inherited unchecked by the serve proof, named as such | extending the deriver, or a ruling that they stay out |
| the watch's **human leg** | the in-repo legs are live; no notification reaches a person | enabling Actions-failure notifications on the account, which cannot be done from inside the repository |

### Opening a PR sometimes starts no checks — observed twice, then contradicted

**This was written up as a rule and the rule was wrong. It is withdrawn here, in
the same ledger, rather than left to be discovered later.**

What is measured, and stands:

| PR | head at which it was OPENED | run for that head? |
|---|---|---|
| **#124** | `8dc1160` | **none, ever** |
| **#125** | `ec7931e` | **none** — still none 2.5 minutes later; the first run on that PR came only after a further commit was pushed |
| **#126** | `6176076` | **yes** — run `32029420526`, `event: pull_request`, started ~25 s after opening |

All three were opened through the same API with the same credentials, against the
same branch and the same workflow. **Two started nothing; the third started
everything.** The first cut of this entry generalised from the two and named a
cause — GitHub's recursion guard for integration-token events. That was wrong
twice over: it is contradicted by #126, and it was already contradicted by both
merges, which used the same API and did produce push-to-`main` runs.

**The honest state: a pull request can open with zero checks, this has happened
twice in one day, and the condition that decides it is UNKNOWN.** Not "probably
timing", not "probably the token" — unknown, and recorded as unknown.

**What survives, and is the part that matters:** a PR carrying no checks is not
visibly different from one that passed, and it can arise without any defect in
any workflow file. That is the standing argument for
`tools/pr_check_census.mjs --gate`, which reds on an undeclared zero-check PR
whatever produced it. The gate does not need the cause. **The lesson is not the
mechanism; it is that the count must be measured on every run rather than
reasoned about.**

### The watch's own landing commit stopped CI, by describing the thing that stops CI

The squash message that merged the watch explained its ledger-append guard, and
in doing so wrote the literal CI-skip token — `[skip ci]` — into the commit message.
GitHub honoured it. **The push to `main` at `210e6cc` produced no workflow run at
all**, including the watch's own. A sentence describing a mechanism invoked the
mechanism.

Two things follow, and both are now in the tooling rather than in a reader's
memory:

- **A skip token silences every event-driven trigger, including any watch.** No
  in-repo, event-driven mechanism can catch this, because it is silenced by the
  same token. **Only the scheduled sweep can**, which is the first concrete
  justification for the cron leg beyond "a workflow that never starts emits
  nothing".
- **The watch had a blind spot of exactly this shape.** It judged the latest run
  *per workflow* — which answers *"is each gate passing"*, not *"was this commit
  checked"*. Those come apart completely here: `main` moved, nothing ran, the
  newest runs still belonged to the previous commit, and **every gate would have
  reported PASS while the actual head had been tested by nothing.** The watch now
  reads the head commit, reports `TESTED BY NOTHING` when no run carries its sha,
  names the skip token when that is the cause, and **reds the verdict even when
  every workflow is green**. Control (f) covers it in both directions.

This is the R0.23 family again — a pattern matching somewhere it was never meant
to act — and the third instance of a defect in this arc being found by reading
what actually happened rather than by a gate reporting it.

**The 29/29 collision, kept permanently so it does not become a phantom finding:**
the 29 routes the serve proof checks (23 site + 5 Lessons + 1 Apps) and the 29
shelf entries the site deriver leaves to the Lessons estate (52 − 23) are
different sets that happen to be the same size. Nothing connects them.

- **2026-08-17 — main was red.** Detected by the watch, not by inspection. Run [`32029976055`](https://github.com/MattRoper1977/Lessons/actions/runs/32029976055) <!-- watch:32029976055 -->

  **FALSE POSITIVE, and left standing because the watch wrote it (R0.13).** That
  line is the watch's own first live execution, and it was wrong. The run
  reported **6 PASS · 0 FAIL · 0 NO VERDICT**, and went red only because six
  workflows had no run in the recent window — **three are `workflow_dispatch`-only
  and cannot have an automatic run at all, and three are path-filtered on game
  files this commit never touched.** Dormancy is not failure. `main` was green.

  It is the failure mode named three paragraphs above it in this same ledger —
  *"a gate that is always red is deleted within the week"* — reached on execution
  number one, by the file that warns about it. Worse, the red drove the
  ledger-append leg, so **a false finding wrote itself into this document and
  pushed to `main`** as `9a5b424`. A destructive-ish consequence of a false
  positive is exactly what R0.14 and R0.15 exist to stop.

  Fixed: dormant and dispatch-only workflows are reported with their triggers
  named and **do not colour the verdict**. Deciding whether a path-filtered
  workflow *should* have run on a given commit means matching its filters against
  that commit's changed files; this tool does not do that, so it does not
  pronounce on it — a stated limitation instead of a confident wrong answer.
  **Control (g)** pins the regression, and red is now reserved for FAIL, NO
  VERDICT, or a head tested by nothing.

---

# THE ARC IS CLOSED — 2026-08-17

Written last, from measured artefacts. Superseded by dated pointer only.

## 1 · The closing measurement

Both red runs on `main` had **one cause, not two** — identical failure line,
identical subject, identical `7 pass · 1 fail · 0 inconclusive`.

- **Before** — run `32018424063` @ `b6f92ca`, job `95352744737`: the Studio failing
  *served without a redirect chain*.
- **After** — run `32027709223` @ `036b545`, job `95380509725`: `SERVED · 200 ·
  6678059f11fc · 55394 B · chain → 301 → madebymatt.uk`.

> **Same 301, same destination, opposite verdict. The deployment never changed;
> the judgement did.**

**The estate was never broken — the gate was.**

## 2 · Two counts, separate, neither netted against the other

**Checks that COULD NOT FIRE — twelve.** Predicate and derivation are unchanged
and still machine-checked above: one row per check that could not fire, where it
was found, two such defects in one commit counting twice; 10 in these gates + 1
Matt-side + 1 found by re-reading an artefact.

**Checks that FIRED WRONGLY — three instruments.** A different species, so it
gets its own count and its own predicate: **one row per instrument that returned
a verdict which was false at the moment it returned it, counted per instrument
and not per wrong verdict** — otherwise one bad regex outvotes a whole gate.

| instrument | wrong verdicts | found on |
|---|---|---|
| the stale-evidence sweep, v1 | **4** — `T10a`, `T10b`, `X0`, `X1c` called stale; all four existed | its own corpus run, which is what produced R0.14 |
| `verify_fieldops_served.mjs` — any `3xx` treated as FAIL | **2** — the Teacher Studio, twice | runs `32017557268` @ `7efbf22` and `32018424063` @ `b6f92ca` |
| `watch_main_runs.mjs` | **2** — red on a green estate, twice | run `32029976055` @ `9b875b6` (dormancy read as failure) and run `32032047401` @ `0933118` (a still-running sibling read as *no verdict*) |

Twelve could not fire; three fired wrongly. **Both numbers are the arc's result.
Neither cancels the other, and a gate that fires wrongly is the more dangerous of
the two, because it produces evidence.**

## 3 · R0.20 – R0.27, with what enforces each

**R0.24 is deliberately unallocated.** The closing order introduced its new rules
as R0.26 and R0.27 and referred to a write-leg rule as R0.25, skipping 24. Under
**R0.17** ids are allocated here, not in an order — but renumbering would leave a
dangling reference in a document already issued. The order's ids are kept and the
hole is recorded, so a later reader does not hunt for a lost rule.

| rule | what it says | provenance | enforced by |
|---|---|---|---|
| **R0.20** | evidence has a locality; CI green and local green are different claims | the D1 control proven only on a branch whose push triggered nothing | **unenforced** — convention only |
| **R0.21** | a retry loop classifies before it repeats | four non-fast-forward retries; then **four retries of a legible `HTTP 403` inside the run that ratified this rule** | **unenforced** — and demonstrably so |
| **R0.22** | a failure on the default branch reaches a person by a mechanism, not by inspection | runs `32017557268`, `32018424063`, both found by looking | `watch-main.yml` — in mechanism; **the human leg does not exist** |
| **R0.23** | a pattern states its scope and prints its match set before acting | a filtered grep; `git tag -l` in the wrong repo; `pkill -f` killing its own wrapper | partly — `watch_main_runs.mjs` and `--verify-trigger-list` print scope and match set; elsewhere **unenforced** |
| **R0.24** | *unallocated — see above* | — | — |
| **R0.25** | the write leg is split from the judge, and every appended line carries run id, verdict and predicate | run `32029976055` wrote a false finding into this document and pushed it | **enforced by withdrawal**: both conditions are false, so the write leg is dry-run and the job is `contents: read` |
| **R0.26** | a rule lands as a mechanism or it does not land | R0.16's amendment violated 20 minutes after being recorded; R0.21 violated inside its own ratifying run | this table — every rule now carries its enforcement or the word `unenforced` |
| **R0.27** | a document must not contain a control token in an executable position | #125's squash message described the skip-ci guard and included the literal token; `210e6cc` got **no CI run at all** | partly — the token no longer appears anywhere in `.github/workflows/`; in commit messages **unenforced** |

**Four of eight are `unenforced` or partly so, and that is the honest state.**
R0.26 exists because writing a rule down was repeatedly mistaken for putting it
in force.

## 4 · Four merges, and why there were four

`#124` carried the payload. **`#125`, `#126` and `#127` exist to repair defects
introduced while building the watch in `#125`.** Stated plainly: *three of the
four merges this session repaired defects introduced by the second.*

| PR | merged as | what it was |
|---|---|---|
| **#124** | `036b545` | the payload: control (e), the D1 control, the census split, the inline-exit wiring |
| **#125** | `210e6cc` | the watch — and its squash message stopped CI on its own landing commit |
| **#126** | `9b875b6` | the untested-head blind spot, and a withdrawn rule |
| **#127** | `758304f` | the false positive: dormancy is not failure |

## 5 · The watch's two live verdicts — one false, one true

| run | head | verdict | truth |
|---|---|---|---|
| `32029976055` | `9b875b6` | FAILED | **false.** 6 PASS · 0 FAIL · 0 NO VERDICT; red on dormant workflows; `main` was green |
| `32030762018` | `758304f` | SUCCESS | true |

Control **(f)** exists because of the first; control **(g)** exists because of the
second. **A sample of two is not a track record**, and the soak countdown is
printed in every run so nobody has to remember that.

## 6 · The human leg — qualified, not claimed

The watch converts *nobody knew* into *it is written where someone will see it*.
**Better, and not the same as being told.** GitHub's Actions-failure mail goes to
the account that triggered the run; these are automation-triggered, so they reach
nobody. **R0.22 is satisfied in mechanism and not in effect, and this ledger keeps
saying so until the account setting is on.**

### Addendum — a third false red, and the pattern behind all three

Run `32032047401` @ `0933118` reported **`0 failing · 1 without a verdict`**, head
tested by 2 runs. **The estate was green.** The single "no verdict" was a sibling
workflow still *in progress*: the watch triggers on `workflow_run: completed`,
which fires when the **first** workflow finishes, while the others are still
running.

**PENDING is not NO VERDICT.** *Not finished yet* and *finished without a result*
are different states, and collapsing them is the same mistake as reading dormancy
as failure — **three times in one arc, an ABSENCE has been treated as a BAD
RESULT.** That is the honest summary of this watch's defect record, and it is a
judgement error, not a plumbing one: every mechanism worked each time.

Fixed structurally rather than by comment: `classify()` returns a fourth bucket,
`PENDING` is printed separately and does not colour the verdict, and a **completed**
run with no result is still NO VERDICT and still reds. **Control (h)** pins all
three directions.

**The standing rule below was already in force and needed no action:** the write
leg was dry before this run, so the second false red **wrote nothing** — `main`
did not move. That is the withdrawal working exactly as intended, and it is the
only reason this red cost nothing.

### The confirming measurement — run 4

| run | head | verdict | truth |
|---|---|---|---|
| `32029976055` | `9b875b6` | FAILED | **false** — dormancy read as failure |
| `32030762018` | `758304f` | SUCCESS | true |
| `32032047401` | `0933118` | FAILED | **false** — a still-running sibling read as *no verdict* |
| **`32032881091`** | **`3202144`** | **SUCCESS** | **true** — `main` green, the watch agrees, nothing written |

**Four live verdicts: two false reds, two greens.** Both false reds were the same
error in different clothes, and both were caught by reading the run rather than
by the run announcing itself. **Consecutive greens from the newest: 1.** The soak
counter therefore stands at **1 of 10**, unchanged by run 4 — a green after a red
restarts the count, which is the point of counting consecutively.

**Neither false red is netted away by the greens.** The watch's entry in the
fired-wrongly table stays at **2 wrong verdicts**, permanently.

## 7 · The watch's standing conditions, each as currently true or false

| condition | state |
|---|---|
| the writer is split from the judge | **FALSE** — one job, `watch` |
| every appended line carries run id, verdict and predicate | **FALSE** — the one line it wrote carried only the run id |
| **therefore the write leg is DRY-RUN** | **TRUE, now** — it prints exactly what it would append, appends nothing, and the job is `contents: read` |
| soak target | **10** consecutive green; **1** accrued; countdown printed in every run |
| dormancy is reported, never judged, and the limitation is in the tool's own output | **TRUE** — the tool prints that a workflow which has silently stopped running is not distinguishable there from one correctly dormant, and that `UNDETERMINED` is the honest word |
| `9a5b424` — the false line and the untested head it created | **recorded**, annotated in place as the watch's own error, not deleted |

**STANDING RULE, in force from now: if the watch reds again on a green estate,
the write leg is disabled outright and the reporting leg is kept.** Two false
reds with a write leg attached is worse than no watch. The write leg is already
dry; this rule governs whether it is ever re-armed.

## 8 · What remains open, by name

| item | state | what closes it |
|---|---|---|
| branch `claude/close-order-seven-items-wdfhdf` | delete refused `HTTP 403`; content proven identical to main — **clutter, not risk** | a session with ref-delete permission, or repo → Settings → **Automatically delete head branches** |
| tag `close-fixes/combined-614f4d8` | ~~exists in the site repo, unpushed, annotated~~ **SUPERSEDED 2026-08-17 — gone with the container that annotated it.** Zero tags on all three remotes; `614f4d8` stays alive as the head of `claude/hud-coverage-scriptline-load-bearing`. See the fuller entry in §"What remains open, by name" above | **nothing — closed.** The push was never the blocker; the object is |
| **the watch's human leg** | **does not exist** | an account-level notification setting — Account → Notifications → Actions → *failed workflows only*, with Watching set on the repo |
| nine declared zero-check PRs | recorded, ratcheted, not repaired | its own pass |
| B2 conformance | a gap; abandoned, no result survives | re-running the conformance order |
| VSL v0.4.1 | nothing created, correctly | its own order — v0.4 still carries **V2: pupil name and notes in the Share URL, at an SEMH provision** |
| five declared-not-derived routes | inherited unchecked, named | extending the deriver, or a ruling |
| whether a path-filtered workflow should have run | ~~reported, deliberately **not** judged~~ **ANSWERED 2026-08-17** by `tools/workflow_dormancy_matcher.py` — report-only, seven controls fired both ways on every run, and it reproduces PR #124's hand-verified 1-of-11 trigger table exactly from that commit's changed files | wiring it into the watch's UNDETERMINED bucket — a separate decision needing its own true-negative **there**, which this tool's soak counter does not authorise |

**Next work opens as new orders, not extensions of this one.** Ranked: the
path-filter matcher (turns UNDETERMINED into an assertion, and makes *silently
stopped running* detectable) · the nine zero-check PRs · B2 conformance · **VSL
v0.4.1, which is the only one carrying a pupil-data finding and should be ranked
accordingly.**

*The arc's goal is met: `main` is green, the Studio failure is gone and named, and
something now watches. It is also true that three of four merges this session
repaired defects introduced while building the watch, and that the watch's first
live verdict was false. Both sentences belong in the record, next to each other,
unhedged. The mechanism works; the judgement of what deserves a red is the thing
still being learned.*

---

# THE RULE REGISTER, AND THE VSL INTAKE STOP — 2026-08-17 (Phase A)

**This section supersedes, by dated pointer and not by edit, the rule table in
*THE ARC IS CLOSED*.** That table stays readable and stays true as at its date;
this one is the allocator of record from here.

## Collision check, run before anything was written

Scope: `RELEASE_LEDGER_2026-08-16.md`. For each of R0.20–R0.30, every site that
*binds* the id was printed and read.

| id | prior ledger binding | verdict |
|---|---|---|
| R0.20 – R0.23 | bound, and to the same rule the orders propose | **no collision** |
| **R0.24** | bound to the literal word ***unallocated*** | **no collision** — a placeholder is not a rival claimant, so the pointer below gives it content without contest |
| R0.25 – R0.27 | bound, and to the same rule the orders propose | **no collision** |
| R0.28 – R0.30 | not allocated | **free** |

**Zero collisions. Nothing was renumbered on either side.**

## R0.24 — dated superseding pointer, not an edit

The line above that reads `| **R0.24** | *unallocated — see above* | — | — |`
**stands and is not edited.** It was accurate on the date it was written.

> **SUPERSEDED 2026-08-17 by `MASTER_PROMPT_VSL_Intake_and_Ledger_2026-08-17`.
> R0.24 now has content: *every gate ships a true-negative control — a known-good
> subject that must come back green.* A control block that only demonstrates reds
> is what produced this watch's first false positive.**

## R0.20 – R0.30, in id order, each with its enforcement or the word `unenforced`

| id | rule | provenance | enforced by |
|---|---|---|---|
| **R0.20** | evidence has a locality; CI green and local green are different claims | the D1 control proven only on a branch whose push triggered nothing | **unenforced** — convention |
| **R0.21** | a retry loop classifies before it repeats | four non-fast-forward retries; then four retries of a legible `HTTP 403` inside the run that ratified the rule | **unenforced** — and demonstrably so |
| **R0.22** | a failure on the default branch reaches a person by a mechanism, not by inspection | runs `32017557268`, `32018424063`, both found by looking | `watch-main.yml` in mechanism; **the human leg does not exist** |
| **R0.23** | a pattern states its scope and prints its match set before acting | a filtered grep; `git tag -l` in the wrong repo; `pkill -f` killing its own wrapper | partly — the watch and `--verify-trigger-list` print scope and match set; **elsewhere unenforced**. *It is also what made the VSL stop a measurement rather than a hunch* |
| **R0.24** | **every gate ships a true-negative control — a known-good subject that must come back green** | a control block that only demonstrated reds produced the watch's first false positive | **unenforced** — no mechanism yet asserts it across the estate; its first enforcement is the VSL gate suite, which is blocked |
| **R0.25** | the write leg is split from the judge, and every appended line carries run id, verdict and predicate | run `32029976055` wrote a false finding into this document and pushed it | **enforced by withdrawal** — both conditions false, so the write leg is dry-run and the job is `contents: read` |
| **R0.26** | a rule lands as a mechanism or it does not land | R0.16's amendment violated 20 minutes after being recorded; R0.21 violated inside its own ratifying run | **this table** — every rule carries its enforcement or the word `unenforced` |
| **R0.27** | a document must not contain a control token in an executable position | a squash message described the skip-ci guard and included the literal token; `210e6cc` got no CI run at all | partly — the token appears nowhere in `.github/workflows/`; in commit messages **unenforced** |
| **R0.28** | **an absence is not a result** | dormancy read as failure, then pending read as no-verdict; and the VSL stop, where reporting P0 green from a file containing none of the biology would have been the same error | partly — `classify()` carries PASS · FAIL · NO VERDICT · PENDING as separate buckets, and dormancy does not colour the verdict; **outside the watch, unenforced** |
| **R0.29** | **no live-derived value is copied into a static document** | the soak counter: written as *1 of 10*, and every commit correcting it moves the count again | **unenforced** — the tool derives and prints it on every run, and the ledger's figure is a dated snapshot by construction |
| **R0.30** | **an order names where its subject lives, and proving reachability is its first act — before scope, before gates, before anything** | the VSL run order specified its subject by bytes, lines, sha256 and bench count, and never said where it was; it has only ever existed as a chat upload | **unenforced** — its mechanism would be an order template that cannot omit a location |

**Seven of eleven are `unenforced` or only partly enforced.** That is the measured
state, and under R0.26 it means seven of these rules have not yet landed.

## The R0.17 violation, recorded

**R0.24 through R0.30 were allocated inside chat orders rather than in this
ledger, which is what R0.17 forbids: rule identifiers are allocated in the ledger,
never in an order.** Matt has recorded the violation as his own and ruled the
resolution: **the ledger is the allocator; an order's id is a proposal until
landed here; if a proposal ever collides, the ledger wins and the order is
corrected.** This section is the landing. The violation is recorded beside the
rules because a register that hides how its own ids arrived is worth less than one
that does not.

## The VSL intake stop, recorded as a finding

**Not an absence of work — a measurement.** The v0.4.1 run order was executed and
stopped at its own §1.1: *the baseline artefact is not reachable from any ref,
tree, history or upload.*

**Scopes searched, with their match sets (R0.23):**

| scope | match |
|---|---|
| `/home/user/Lessons`, `/workspace/vcl`, site, `coa`, `scrapcore` trees | none |
| filesystem sweep, `*Laborator*html` and `*PRO_v0*` | none |
| **every ref** — Lessons 288, site 322, Apps 37, Games 70 | **no `Virtual_Science*` file on any ref** |
| Lessons history, all branches, `v0_4` / `v0.4` | none |
| this session's uploads (6 HTML files) | not among them |

**Required against present:**

| | required | the only VSL-family artefact reachable |
|---|---|---|
| file | `Virtual_Science_Laboratory_PRO_v0_4.html` | `Virtual_Chemistry_Lab_PRO_Spatial_v0_3.html`, on `#116`'s branch |
| bytes | 287,161 | **173,102** · Δ −114,059 |
| lines | 1,978 | **1,646** · Δ −332 |
| sha256 | `137bbfac…` | **`bd0e7596…`** |
| benches | 13 — 5 chemistry + 8 biology | **5 chemistry, 0 biology** |

**Why v0.3 was refused, and the hash is the weaker reason.** Eight biology
benches are absent, and the P0 re-measurement list is mostly biology — the ×10
calibration, ψ = −1.02 MPa, the enzyme endpoints, inverse-square, the ecology
labelling, the 25 °C gate. **Reporting P0 green from a file containing none of it
would be an absence read as a result — R0.28, inside the order that put R0.28 in
force.** And `#116`'s own body forbids it independently: it exists so that a fixed
5-bench file and an unfixed 13-bench file never sit in the estate together.

**R0.30 is the rule this produced**, and its provenance is above: an order that
named its subject by four measurements and never named where it lived.

**One line closes it: the artefact itself, attached to a session or pushed to a
branch on Lessons.** Nothing downstream is unresolved — the rulings, swap lines,
nine gates with their true-negatives, and the four placement tests are all
specified and waiting.

## V2's rank is unchanged, and a blocked item is not a de-ranked item

**Pupil name and notes are serialised into `location.hash`; Share hands that URL
out; the field's own caption says *"Name for print/export only."* At an SEMH
provision.** It is the highest item on the board, it is the only one on the board
that is not a quality issue, and **it is still unfixed.**

