# SX3 ledger — entries opened at the sixth pin move (Site #409)

## L1. Comment-correction defect, caught by gate s10
- Where: .github/workflows/education-publication.yml, the comment above the Lessons carrier pin.
- What: while correcting a STALE comment (it still described b54c9006 and claimed
  "Held EQUAL to domain-split-verify.yml", untrue since #408), two LESSONS paths were
  written bare inside a SITE workflow:
      tools/verify_cross_estate_unification.py
      tools/catalogue/STATIC_CHECK_RESULTS.json
- Caught by: MBM audience discovery closeout run 35449614441, head d820cb6d,
  step s10-workflows-reference-no-path-that-does-not-exist (1 of 47 gate steps).
  tools/check_workflow_paths.py: "never existed ... whatever it was meant to check
  has never been checked".
- Class: a correction introducing a second defect of the same family as the one it fixed.
  The pin move itself was never implicated.
- Repair: c0130703, comment-only. All three repo-qualified with a Lessons/ prefix.
  education-pages.yml was NOT flagged (outside the gate's tools/assets/data scope) but
  was wrong the same way; qualified too, rather than left correct-by-luck.
- Re-proved locally on /tmp/pubvenv/bin/python3 (3.12.3):
  check_workflow_paths.py --self-test -> 5 passed, 0 failed
  check_workflow_paths.py            -> 216 paths, every one exists (218->216: the two
                                        invalid references are gone, nothing excluded)

## L2. Instrument correction #7
get_job_logs returns a blob URL, not log content, unless return_content=true.
The blob host (productionresultssa2.blob.core.windows.net) is refused by the egress
proxy here with 403 CONNECT, so the URL form is unusable in this environment.
Always pass return_content=true. Cost when first learned: 1 wasted CI read.

## L3. Domain split publication path-filter gap  [PASS 6]
.github/workflows/domain-split-verify.yml triggers on pull_request/push with paths:
    domain-split/**
    supabase/**
    .github/workflows/domain-split-verify.yml
A change to .github/workflows/education-publication.yml matches 0 of 3, so the gate is
BLIND to a change in the carrier workflow that feeds it. Same class as the pin drift:
a gate that cannot see the thing it depends on. Worked around on #409 by manual
workflow_dispatch (no inputs). NOT widened in #409.

## L4. The four remaining b54c9006 pins — measured, read-only
Scope: the 13 scripts those workflows execute plus every local module they import
(computed transitive closure, 16 files).
  play-discovery-verify.yml:36
  published-completion-verify.yml:25
  splash-region-records.yml:53
  splash-region-records.yml:114
Findings: baseline_sha              -> 0 hits
          education-publication-admission -> 0 hits
          check_education_separation / check_education_publication_admission -> 0 hits
          usage-registry            -> 2 hits, BOTH writes (save(...)) in
                                       domain-split/usage_discovery.py, into the
                                       throwaway .play-review/output tree; no digest
                                       comparison anywhere in the closure.
Verdict: none reads the fence or the admission registry. They are green by CONSTRUCTION,
not green by absence — they cannot go red from ec7dc075->d0dc6b3e. They are the PASS 6
lag-control's population and nothing more.

## L7. The 14:10 cross-estate red WAS the unpublished-Site case  [CLOSED]
Made by Matt cross-estate unification, run 35447908661 on eab8daaf, FAILED at
~14:10 while Site main (0cd8f842) was red and had published nothing.
Ruled out locally FIRST: the static-contract leg
(verify_cross_estate_unification.py --base origin/main --canonical _reference/site
--self-test) PASSES against BOTH Site states -- ab62d6e4 (post-#409) and
0cd8f842 (the failing run's own input). So the static contract was never the cause.
The live-proof leg could NOT be reproduced here: the egress proxy refuses
madebymatt.uk with 403 CONNECT (organisation policy), all routes return 000.
Re-run after Site main went green (Education publication 35452403688, Pages
deployed): attempt 2 -> failed_jobs 0 of 4 total. CONFIRMED: the precondition,
not the gate.
Consequence for STOP-P1: the three typed PUBLISHED digests were NOT stale --
the live bytes still hash to 01e571fa (lessons '') and 048f41f8
(lessons subject.html). This release did not move those two routes' published
bytes. My earlier speculation that they had gone stale was WRONG and is
withdrawn. The repair remains correct as prevention, not as a live fix.

## L8. Lessons has no typed-literal census  [PASS 6 lag-control population]
tools/census_typed_literals.py exists in the SITE repo only. The Lessons repo has
no equivalent, which is why a hand-typed published-digest table
(check_tokens_inert.cjs PUBLISHED, three digests) has never been in any census's
scope. Larger than the four b54c9006 pins: not one gate blind to one pin, but a
whole repository outside the instrument's reach.

## L9. check_tokens_inert.cjs copies are DELIBERATELY not byte-identical
lessons 482642d3, 66 lines; apps 829f5d1a, 78 lines. The Apps copy carries 12
extra lines for the SW2 A hub-heading exemption (sw2Heading, approved-ink check,
widened planted-defect selector). Nothing asserts byte-identity for this file and
making it so would delete a real Apps-side control. The PUBLISHED table is the
shared part and is identical in both. PASS 6 re-pins the TABLE in both copies,
not the files.

## L10. CORRECTION — "pinned vs SERVED origin"  [RULING, recorded]
The three PUBLISHED digests in check_tokens_inert.cjs were NEVER stale. The local
rebuild's digests (5c4e3ced... etc.) differ from the served bytes because THE
CONTAINER'S BUILD IS NOT THE SERVING BUILD. Every "pinned -> built" line in this
ledger is re-labelled "pinned vs SERVED origin".

THE LESSON, stated as an instrument rule:
  A local build reproduces the BUILDER, not the SERVED ORIGIN.
  The origin (madebymatt.uk) was unreachable from this container -- 403 CONNECT,
  organisation policy -- so the served bytes were NEVER MEASURED HERE at all.
  They were first measured when CI's live-proof leg passed on the re-run of
  35447908661 (failed_jobs 0 of 4). Until that moment, every statement about the
  served bytes was an inference from a local build, not a measurement of the origin.

Class: mistaking a reproduction of the builder for a measurement of the origin.
Sits beside instrument corrections #6 (derive a SHA, never transcribe),
#7 (get_job_logs needs return_content=true; the blob host is 403 here) and
#8 (actions_list silently ignores head_sha / event / workflow_id filters --
observed three times; filter locally from the returned payload).

## L11. The PUBLISHED re-derivation control returns to the NEXT ORDER
Not PASS 6. The release does not grow for a fix that fixes nothing live.
The defect class stands and is recorded: three digests typed by hand, in a
repository with no typed-literal census (L8), guarded by nothing. Prevention,
carried forward, not bundled into this release.

## L12. STOP-P1 CONFIRMED BY MEASUREMENT OF THE ORIGIN  [PASS 6]
live-proof job 105928321042, run 35447908661 attempt 2, STEP 4
(`node tools/sw2/check_tokens_inert.cjs --base https://madebymatt.uk/Lessons/ --published`):

  16:31:17  Error: Expected admitted publication did not become ready:
    [{"route":"","status":200,
      "actual":"5c4e3ced64113e43570279915c608e7b5dbc19b089c9a2dc806bcfaf46e3b722"},
     {"route":"subject.html","status":200,
      "actual":"93a071a895033cceddfa9a45530bd5c1e42e690d1959a716ef798b28f3bd9206"}]
      at waitForPublished (tools/sw2/check_tokens_inert.cjs:43:9)
  ##[error]Process completed with exit code 1.

  route           PINNED (check_tokens_inert.cjs:22)   SERVED (origin, HTTP 200)
  lessons ""      01e571fa7b4d619d...                  5c4e3ced64113e43...   MISMATCH
  lessons subject 048f41f8c63c2a90...                  93a071a895033cce...   MISMATCH
  /assets/mbm-tokens.css                               matched (absent from the failure list)

Polled 60 x 5s, 16:26:18 -> 16:31:17. Both routes 200 throughout: the origin is
UP and STABLE at these bytes. The step before it PASSED --
"[PASS] lessons browser matrix: 8 widths, 4 unchanged standalone samples" -- and
the served hub reports "1046 resources - 13 subjects". The RELEASE IS LIVE AND
CORRECT. Only the typed digest table is stale.

STOP-P1 stands EXACTLY as first recorded: typed pins stale vs served bytes.

## L13. WITHDRAWN: the "local build" attribution of 5c4e3ced
5c4e3ced was recorded as a LOCAL REBUILD digest. It is not. It is the SERVED
ORIGIN's actual bytes, measured by CI over HTTPS at status 200. The re-labelling
of "pinned -> built" lines to "pinned vs LOCAL build (not served)" is WITHDRAWN
and reverted to "pinned vs SERVED origin".
L10's INSTRUMENT RULE IS KEPT and remains true: a local build reproduces the
BUILDER, not the SERVED ORIGIN, and this container cannot reach the origin
(403 CONNECT). That is exactly why the served bytes could only ever be measured
by CI -- and when CI finally measured them, they did not match the pins.

## L14. Correction #9  [instrument]
get_job_logs `failed_jobs: 0` is NOT a pass. It means no job has failed YET.
Completion is a SEPARATE fact and must be established before any verdict is
reported. I reported attempt 2 green on an in-progress run; the ruling that
followed rested on it. Second liveness misread after `updated_at`.

## L15. L11 REVERSED by its own condition
The PUBLISHED re-derivation control returns to PASS 6. It does not "fix nothing
live": two of three pinned routes are stale against the origin right now, and
Watch main is red by attribution until they are re-pinned.
Shape: derive the digests FROM THE SERVED ORIGIN IN CI (live-proof already
fetches those bytes; the tool records what it fetched), --check compares,
--write re-pins; red-proved by a planted digest and by a route missing from the
fetch. Lands as a Lessons PR + Apps companion -- the TABLE re-pinned identically
in both, the FILES divergent by design (L9).

## L16. Instrument catch: PATTERN vs RULE
I observed that no START_HERE page appeared in REVIEWED_PATHS and concluded the
three new ones did not belong there. That was a PATTERN read off 110 entries, not
the RULE. The rule is in verify_change_boundary.judge(): a protected ADDITION is
admitted only with a CATALOGUE_PINS entry whose sha256 equals the file, and pins
come from REVIEWED_PATHS. The order's spec ("+ REVIEWED_PATHS") was right and my
inference was wrong.
RULE: an absence in a list is evidence about the list, never about the contract.
Read the contract.

## L17. Instrument catch: base...HEAD reads COMMITTED work only
verify_change_boundary.py reported "protectedChanges: 0, status PASS" while the
three files sat STAGED but uncommitted. It compares `git diff --name-status
base...HEAD`, so it measured an empty diff. I nearly recorded "Science_Teesside
is not protected" from it. Committing first produced the true reading:
protectedChanges 3, all three rejected. Science_Teesside IS in PROTECTED.
RULE: before trusting a diff-based gate, prove it is looking at your change --
a zero-finding result must be distinguished from a zero-input result.
Same family as #9 (failed_jobs: 0 is not a pass). Caught before it reached the
operator this time.

## L18. GLV3 had no route for a NEW protected navigation page  [closed by ruling]
judge() admits a protected path by exactly four routes: SHELVES (2 entries, the
subject indexes), ALL_REPLACEMENTS (member must be status 'M' with a
beforeGitBlob), the SCIENCE_PACKS prefix (Science_Teesside/Teaching_Packs/), and
explicit_cover_paths (97 paths, all under the Humanities cover ruling). A
brand-new pathway landing page matched none, and a "fifth transaction" was
UNCONSTRUCTIBLE: a transaction member must be a modification and a new file has
no beforeGitBlob.
Closed by RULING Option 2: PATHWAY_PARENTS, addition-only, pin-checked, modelled
on the cover set. Options 1 (changes what SHELVES means) and 3 (general
weakening) refused.

## L19. The Apps e172f07 push-run live-proof failure  [PASS 6 record]
Made by Matt cross-estate unification run 35435940616 (push, 09:53) FAILED on
Apps main e172f07; the scheduled run 35441365119 (11:54) PASSED on the IDENTICAL
head. Latest-per-workflow is therefore green and Apps main was not red. Same
timing family as the Lessons live-proof case: a gate whose verdict depends on
when it ran relative to a publication, not on the commit it judges.

## L20. _authoring/.../chassis/{adapters.py,estate_shell.py}  [PASS 6]
The SX3 transplant toolchain, Part 2 of this release, never committed. NOT 3b's.
Excluded from the 3b branch, left untracked. They commit on the #591 toolchain
branch in PASS 6 with the rest of the tools, so the release's mechanism is in the
record.

## L21. THE FOUR DERIVED RECORDS — one class, one sweep  [PASS 6 tooling]
Every resources.json row must also appear in FOUR derived records. SX3 3b hit
all four, one at a time, each as its own CI red, each found only after a push:

  TERM_AND_STYLE_EVIDENCE   check_catalogue_static.py    (red on #410 head 1)
  CATALOGUE_PINS            pin_catalogue_contract.py    (GLV3 admits a
                            protected ADDITION only via this pin -- the
                            PATHWAY_PARENTS clause reads pins.get(rel))
  data/resource-sizes.json  tools/ux2/resource_sizes.py  (red on #593, UX2 gates)
  PIN1 trigger list         tools/pin1/derive_triggers.py(red on #593, static-contract)

RULE: before any push that adds or removes a catalogue row, run all four
writers' --check together. Each has a --write; regenerate with it, never
hand-edit. Script written and passing all four:
  /tmp/claude-0/pass6/pre_ci_catalogue_sweep.sh
Held OUT of the 3b branch deliberately -- it is tooling, not 3b content, and
adding it would move the head and re-trigger CI. It lands on the #591
toolchain branch in PASS 6 beside adapters.py/estate_shell.py.

## L22. The live-proof pull_request guard
mbm-cross-estate-unification.yml's live-proof job carries
  if: github.event_name == 'push' || github.event_name == 'workflow_dispatch'
so it does NOT run on a pull request. Therefore: on a PR, a cross-estate red is
NEVER STOP-P1. It is static-contract or browser-matrix and must be
root-caused, not attributed to the known live-proof failure. On main the job
does run and STOP-P1's two routes are the expected red.
Same job in the SITE repo's MBM workflow carries the same guard on its
"Routes serve 200" job.

## L23. DERIVED RECORDS SPLIT: INTERNAL vs PUBLISHED  [RULING, recorded]
L21 named four derived records every resources.json row must appear in. They
are NOT one kind. Three are INTERNAL -- regenerating them moves no served byte:
    TERM_AND_STYLE_EVIDENCE      tools/  (0 registry entries)
    CATALOGUE_PINS               tools/  (0 registry entries)
    PIN1 trigger list            .github/workflows/  (0 registry entries)
One is PUBLISHED -- regenerating it moves a served byte and so moves a
registry digest:
    data/resource-sizes.json     education-lessons tree, admitted by digest
Other published derived records in the same class:
    resources.json, assets/catalogue/lesson-order.json,
    education-site/data/domain-catalogue.json,
    education-site/data/resource-discovery.json

THE DEFECT THIS NAMES. On 3b the granted build (and #410's seven registry
entries) were taken BEFORE resource_sizes.py --write ran. The write moved a
published byte the registry did not admit. Result: Education Pages
publication 35467537946 on Lessons main 124f513b,
    "CHANGED education-lessons/data/resource-sizes.json".
I treated all four derived records as internal. One ships.

RULE (two halves):
  (a) the pre-CI sweep ends with the education publication census whenever
      any PUBLISHED derived record moved -- the four --checks are not enough;
  (b) the build that supplies registry digests is taken AFTER the LAST
      regeneration, never before. Regenerate, THEN build, THEN write pairs.

THE CARRIER COST, recorded. education-pages.yml pins the Site builder by SHA
(immutable). So every Site registry fix, however small, costs a Lessons
carrier bump -- a new Lessons commit, a re-cut caller digest, mirrored gate
copies, an Apps companion. Two PRs and a companion to admit one moved byte.
That cost is the six-pin lag-control's reason to exist.

L24  A FIFTH DERIVED RECORD, STALE ON MAIN. tools/catalogue/STATIC_CHECK_RESULTS.json
is rewritten by check_catalogue_static.py on every run (baseline SHA,
resourceSha256, term counts). On Lessons main 124f513b it still records
baseline 4506bb96 / resources.json c85be00a (pre-3b); running the sweep on the
carrier worktree rewrote it to 124f513b / 733772e9 / any 205. It is a RESULTS
record, read by no gate (to confirm in PASS 6), so it was NOT committed in the
carrier ("nothing else moves"); restored with git checkout after reading the
diff. PASS 6: decide whether it joins the four-writer sweep (regenerate-and-
commit) or is dropped from tracking; until then it drifts on every catalogue
change.

L25  INSTRUMENT SLIP (HUM-D5, own): `npm install axe-core` in a directory with
no package.json removed the unlisted playwright packages ("removed 2
packages") while the E3 visibility run was using them; the running process
survived (modules already loaded) and its 120/120 result was checked for
completeness afterwards. Reinstalled with --save so both persist. Rule: in a
scratch node dir, install every package in one --save call.

MAIN-PUSH TABLE, Lessons main b32bf1c7 (#594 carrier re-cut), read 1/3 at 22:14Z,
filtered locally from a 30-run page (API filters advisory, #8):
  Education Pages publication            35472218580  push  SUCCESS   <- STOP-R resolved
  FieldOps P2, the sweep, the serve proof 35472218231  push  SUCCESS   (was FAILURE on 124f513b)
  UX2 gates                              35472218239  push  SUCCESS
  Made by Matt cross-estate unification  35472218232  push  in_progress at read 1 (live-proof runs on push; STOP-P1 expected)
  GROW LAUNCH v3 generated-tree verif.   not triggered (paths: carrier diff touches no protected path; it ran on 124f513b because Science_Teesside changed)
  Watch main: observer, reported separately when read.
Site #411 merged a1b2a85c (derived); Lessons #594 merged b32bf1c7 (derived); Apps #117 merged 85f7e07f (API; derived below).
Read counts: Site #411 head 2f36f00b 2/3; Lessons #594 head 0248ea78 1/3; Lessons main b32bf1c7 1/3; Apps #117 head 167195b 1/3.
APPS MAIN 85f7e07f (#117 companion), read 1 of 1 at 22:22Z:
  Education Pages publication            35472709978  push  SUCCESS  (builder 08d74766, the Apps carrier, unchanged)
  Verify LundyLoop Professional OS       35472709689  push  SUCCESS
  Made by Matt cross-estate unification  35472709705  push  FAILURE  (same as on 2fc3135 and e172f07: live-proof, STOP-P1 routes; log unread, budget)
Lessons main b32bf1c7, read 3/3 at 22:29Z: Made by Matt cross-estate unification 35472218232
  completed FAILURE (22:19:03Z). Log NOT read (this head's three reads are spent); attributed
  to STOP-P1's two routes BY PATTERN (identical outcome on eab8daaf, 124f513b, and on Apps
  main e172f07 / 2fc3135 / 85f7e07). A grant of one log read would make it a measured fact.
SEQUENCE STATE: step (2) of the latest ruling is complete - Site #411 (a1b2a85c), Lessons
  carrier #594 (b32bf1c7), Apps companion #117 (85f7e07f); Education Pages publication
  SUCCESS on both Lessons and Apps main. Step (3) served proof needs the publication
  artefact or a Watch main dispatch: origin is 403 here, the artefact download host is
  403 (correction #7) -> STOP for a grant (dispatch + reads) before PASS 5.

ORDER FINISH S1 - the one granted log read on cross-estate 35472218232 was taken at
tail_lines=120 and did NOT reach the ##[error]: the tail shows the live-proof job's
final audit JSON (standalone routes 200, reducedMotion 200, errors [], fatal null)
and the artefact upload; the check_tokens_inert --published step is earlier in an
877-line log. Instrument slip of the #10 family (tail truncation, already recorded)
repeated by me: STOP-X for one read at full depth. Attribution stays BY PATTERN.
S2 read 1/3: FieldOps 35472218231 jobs listed; read 2/3: its `served` job log
105975115150 - "59 served byte-identical · 0 red · 0 inconclusive, of 59 derived";
PUBLICATION lessons: checked source b32bf1c7 == deployed source; run 35472218580;
artifact 10594130215 sha256 068cec97...; the 15 LAUNCH Science decks + hub served at
digests equal to the Site registry's admitted values (checked locally, 15/15, hub
5c4e3ced == registry). Read 3/3 reserved for the Watch main verdict.
S2 read 3/3: Watch main dispatch 35475189621 (workflow_dispatch, 23:06:39Z, head b32bf1c7) completed
  FAILURE - the observer reporting the cross-estate red (and 35472978193, workflow_run at 22:19, the same).
  Watch main stays red by attribution until the PASS 6 control closes STOP-P1.
PASS 6 (S4): #590 (breach record, docs-only; FieldOps 35378714202 SUCCESS on 8217a180, mergeable clean)
  merged squash -> Lessons main 18ff3333 (derived below). #591 toolchain next: update from main,
  add adapters.py / estate_shell.py / sweep + census tail / ledger L1-L25 / corrections, regenerate
  STATIC_CHECK_RESULTS.json with its writer and pin it.
STOP-X (Site pins): the order names b32bf1c7 for both Site pins, but #590 (and #591) move Lessons main
  past it; "held EQUAL to Lessons main" and the literal SHA now disagree. Not ruled here.
HUM-D5 H3 STOP-X (not applied): the "five pupil-sheet prose answers" are not prose answers on
  inspection. BUILD_RE_A1_W02 ("In a synagogue the Torah scroll is kept in a special cupboard
  called the Ark.") and BUILD_RE_A1_W06 ("It is held every year on 21 September.") are EVIDENCE
  CARD text (config cards[].text, 8 occurrences each in Lesson.html): removing them from the
  pupil sheet strips the pupil's evidence and breaks E2 parity. BUILD_RE_A2_W04 ("We use battery
  lights only. No real flame.") is a safety instruction. BUILD_S2_W04's leak maps to no answer
  string (apostrophe variant in the scanner, ’ vs '). GROW_RE_A2_W03 is a Choose-hint (B0002
  family) and is in the held-PDF set. Ruling requested before any move.

L26  TWO INSTRUMENT CATCHES OF THE #10 FAMILY (SX3-FU1, own), both with self-tests.
Both are the same class as #11 (a force-revealed index is not a visibility
measurement): an instrument that answers a NARROWER question than the one asked,
and returns a confident wrong answer rather than an error.

(a) VISIBLE STAGE vs WHOLE DECK. The F2 acceptance test asked "same text, nothing
lost" and read `document.body.innerText`. innerText returns only the RENDERED text,
so on a one-stage-at-a-time deck it returns ONE stage. Before the split the visible
stage 0 was the merged ARRIVAL; after it was the new OPENING. The instrument compared
two different stages and reported 92 failures - `text SHRANK 2687->1942`,
`TEXT LOST {'to':1,'04:00':1,'ARRIVAL':1,'LAUNCH':1}`. Nothing was lost.
The second attempt, `textContent` on the deck root, was also wrong but differently:
textContent inserts NO whitespace at element boundaries, so tokens glue across edges
(`ArrivalLAUNCH`, `MINUTESReview`). Moving a boundary re-glues them, and a string diff
scores a legitimate reordering as delete+insert.
Settled form: the deck's non-empty TEXT NODES in document order, compared as a
multiset. Boundary-independent, and it reports a reordering AS a reordering. On that
basis: 20/20, nothing lost, exactly two nodes created.
RULE: before trusting a text instrument, state which DOM property it reads and what
that property does at element boundaries and with hidden content.

(b) A STRUCTURAL EDIT IS NOT PROVED BY READING ITS DIFF. The first cut of the arrival
split stranded `div.knowledge-shortcut` - the knowledge-organiser opener - in the
arrival stage. Contract row 41 puts it in slide 1, and on all three exemplars it is
the LAST CHILD of the opening stage; on a merged deck it trails the arrival content,
so the cut takes it. The diff looked clean: no text lost, stage counts right, every
row-1-to-37 count unchanged. Only DRIVING THE REAL CONTROL in a browser caught it -
row 41 went 155 dialogs opened to 132, failing on 23/23 decks.
RULE: contract rows 38-42 are behavioural. The contract's own standing rule 5 already
says a static parse is structurally unable to emit PASS for them; this extends it -
a rendered COUNT is not enough either, the control has to be driven.
Both faults are now planted in `split_arrival_stage.py --self-test` (27/27) so neither
can return silently.

L27  `[data-arrival-root]` ORPHANED AT `<body>` ON ALL 31 LANDED SCIENCE DECKS.
Found by F1, measured on all 31, NOT repaired by SX3-FU1 and deliberately so - it is
outside the split's scope and repairing it silently inside a shape change would hide
it. The F2 acceptance test asserts the orphan is still exactly as found
(`arrivalRootStage == -1` before AND after, unchanged), so the split cannot quietly
move or fix it. Carried open to the next science order.

L28  A GUARD NO EVIDENCE CAN SATISFY  [finding for the evidence-model order].
`tools/catalogue/build_catalogue.py` re-proves a census binding with
    outcomes = all(len(norm(CELLS[x]['verbatimOutcome'])) > 28
                   and norm(CELLS[x]['verbatimOutcome']) in body for x in refs)
The workbook outcome for the LAUNCH W9-W13 decks is `'Explain growth & stem cells.'`,
which is EXACTLY 28 characters. The guard is `> 28`, so that limb can never fire for
those decks even against a byte-perfect match. The threshold is presumably there to
stop a short generic outcome matching by accident; as written it silently excludes a
real binding rather than reporting that it declined one.
NOT changed here, per ruling R2 - recorded for the evidence-model order. The binding
is instead registered by the second instrument (restored lesson-config,
preserved_outcome / explicit_cell).

L29  L17, SECOND INSTANCE (own): A GATE JUDGED BEFORE THE COMMIT PASSES VACUOUSLY.
     tools/verify_cross_estate_unification.py --base origin/main judges base...HEAD.
     Run on F3a's worktree with the changes staged, not committed, HEAD equalled the
     base and the boundary judged an empty set: [PASS], nothing judged. After the
     first commit the same gate named two unadmitted modifications (the ledger, the
     sweep script). L17's rule stands and is restated here because it caught me a
     second time: commit, then judge; a gate result taken before the commit is not
     a pre-CI result.

L30  THE LOCAL PRE-CI NEVER RAN git diff --check  [instrument gap; STOP-R on #600].
     cross-estate/static-contract runs `git diff --check origin/main...HEAD` after
     the unification gate. Neither the eight-writer sweep nor the three gates run
     locally include it, so #600's head ebfde962 went red (run 35508760763, job
     106072898977, exit 2) on 68 CR-at-EOL lines in nine RFC 4180 CSVs
     (*_Data.csv, CRLF as reviewed and summed in the packs) that no local
     instrument had read. Measured: 68 of 68 are CR at end of line, 0 literal
     trailing spaces; core.whitespace=cr-at-eol silences all 68. Fixed by
     declaration, not by bytes: .gitattributes `whitespace=cr-at-eol` on the pack
     CSVs, the estate's own route for a bytes-unaltered payload the whitespace
     check misreads (the gate's rationale for admitting .gitattributes). The sweep
     gains the same `git diff --check "$BASE"...HEAD` tail in the re-pin commit
     that carries this entry, so the gap closes where it opened.

L31  THE SITE'S LESSONS PIN AND ITS APPS PIN MOVE TOGETHER OR NOT AT ALL
     [instrument gap; STOP-R on Site #413].
     verify_catalogue_contract_controls.py builds an Apps fixture from the Site's
     Apps checkout and runs the LESSONS gate copy against it. The two pins must
     therefore name commits whose gate copies agree, and nothing said so: the
     FINISH-2 window moved the Lessons pins to 6bb8238f (gate copy 1796ab50, the
     #597 spine admission) and left the Apps pin at dfca094b (bd4cb83f, before
     #119). Red, mine, on "Complete separated publications" run 35510178578 job
     106076593121. Three measured pairs settled it:
       Site main's own pair   Lessons b32bf1c7 + Apps dfca094b  PASS 274
       this PR before the fix Lessons 6bb8238f + Apps dfca094b  FAIL
       this PR after the fix  Lessons 6bb8238f + Apps a7d330b8  PASS 273
     tools/lessons_pin_lag_control.py censuses every LESSONS pin and G1 compares
     the two estates' gate copies, but nothing censuses the Site's APPS pins or
     asserts pin-pair agreement. That is the next order's Site item, beside the
     pinned-but-unwatched census: extend the lag control to the Apps pins and make
     pair agreement a control with its own red proof.

L32  THE APPLY RECORD AND ITS VERIFICATION ARE TWO DIFFERENT DOCUMENTS (HUM-D5, own).
     _passhumd5/APPLY_PLAN.json is written by apply_proof.py on EVERY run, write or
     dry. The committed record (09:14:54Z) is the write run: write=true, 22 files,
     22 already_applied, 0 refusals -- D1's actual application. A later verification
     pass (10:21:28Z) overwrote the working copy with write=false, 460 files, 1087
     already_applied, 0 planned_edits, 0 refusals, 128 skipped: the proof that
     nothing remained to apply across the whole pack set. Committing that over the
     first would have replaced an apply record with a dry run under the same name
     and the same schema -- indistinguishable in review except by the write flag.
     The working copy was restored to the committed record and the verification's
     figures carried into the readback as their own measurement. Finding for the
     evidence-model order: a record whose meaning depends on a boolean field inside
     it should carry that field in its NAME, or the tool should refuse to overwrite
     a write-run record with a dry-run one.

L33  THE CARRIER BUMP ON THE LAST LESSONS PR LEAVES THE EARLIER MERGES PUBLISHING AT
     THE OLD CARRIER  [sequencing; STOP-R on Lessons main 8fe3702c].
     Education Pages publication run 35512157865, job 106081826175 "publication /
     build", 12:58:56 -> 13:02:25Z, FAILURE: "Education file admission blocked
     publication" with exactly ten CHANGED paths -- the nine F3a decks and
     assets/catalogue/lesson-order.json. Attributed locally without a build: the
     run's referenced_workflows names education-publication.yml@a1b2a85c, the Site
     carrier Lessons still pins because the carrier bump sits on #600 (the order's
     "last Lessons PR"); the one build's digests for those ten are admitted 0/10 in
     the registry at a1b2a85c and 10/10 at fa4aa9e7 (#413). So #598's and #599's
     main pushes cannot publish green: the pairs that admit their bytes exist only
     at a carrier they do not yet name. It is the same mechanism and the same closer
     as the named red window (#600 lands the carrier bump), but it is not the named
     red (that is check_education_separation.py after #600), so it is STOP-R and
     nothing merged past it. FieldOps P2 on the same push is expected to follow it
     red: its serve-proof polls for a successful publication (the ordering
     dependency the order records). Finding: a carrier bump belongs on the FIRST
     Lessons PR of a window whose Site PR has merged, or as its own PR immediately
     after the Site merge; on the last PR it guarantees a red publication per
     earlier merge.

L34  THE NAMED RED WINDOW, WIDENED BY RULING (a) TO COVER BOTH REDS  [ORDER FINISH-2,
     ruling 2026-09-20; precedent #408/#410; no new bytes].
     Three Lessons-main publications go red inside this window, each by a mechanism
     the window already contains and each closed by the same two commits:
       1. main 8fe3702c (#598, F3a)   Education Pages publication 35512157865, job
          106081826175, FAILURE 13:02:25Z -- admission: CHANGED x10 (the nine F3a
          decks + assets/catalogue/lesson-order.json) at the old carrier a1b2a85c,
          whose registry predates #413 (0/10 admitted there, 10/10 at fa4aa9e7).
          CLOSER: #600 lands the carrier bump (education-pages.yml -> fa4aa9e7).
       2. main 5915a63c (#599, F3b)   Education Pages publication 35513233724 -- the same
          admission red, now the 20 decks + lesson-order.json at the old carrier.
          CLOSER: the same.
       3. main <#600 merge; SHA and run id in the CLOSE readback, FINISH2_CLOSE.md,
          since this entry lands IN #600>   Education Pages publication -- the carrier
          now names fa4aa9e7 so the 21 F3 pairs admit; the 1750 pack files are
          UNREVIEWED at that registry and check_education_separation.py reds on
          "Download additions differ from the reviewed installed pack:
          /Lessons/Humanities_Teesside/Teaching_Packs/" (663 emitted vs 108
          approved). CLOSER: Site PR-2 -- the 663-row reviewed list in emitted
          order with its digest re-pinned, 1750 [digest, ARRIVING], the
          usage-registry pair, both pins to post-merge Lessons main with ITS Apps
          companion (L31) -- then the publication is re-dispatched on Lessons main
          and its SUCCESS run id closes the window.
     FieldOps P2 follows each of the three red (its serve-proof polls for a
     successful publication of that SHA: the ordering dependency the next order
     carries). Any red not in this list is STOP-R.
     STANDING RULE (Matt, from L33): a carrier bump belongs on the FIRST Lessons PR
     after a Site merge, not the last -- a pair that publishes at the old carrier
     publishes against a registry its digests are not in.

L35  A PIN DESIGN THAT CANNOT BE LOADED IS NOT A PIN  [ORDER FINISH-2, manifest-pin
     ruling 2026-09-20; pin-design change, named as such].
     WHAT HAPPENED. #600 pinned the 1750 HUM-D5 pack files individually, as R1
     required and as SCIENCE_PACKS does. PIN1 materialises one exact trigger path per
     pinned file, so the derived mbm-cross-estate-unification.yml reached 4,645 list
     entries / 534,033 bytes -- and GitHub never loaded it. Three push runs on this
     branch completed instantly with ZERO jobs and the run named by the file path
     rather than by the workflow's own `name:` (35509145935 on 4dd90c43, 35512149909
     on 6ad78b5c, 35513723753 on d2f5b7c3), and across 330 pull_request runs of that
     workflow not one was ever created for a #600 head. The gate did not fail on this
     PR: it never ran on it, on any head, at any point.
     HOW IT WAS MISSED. The PR looked green because its OTHER workflows (FieldOps,
     UX2, GLV3) ran and passed, and because I recorded "static-contract run 35509150284
     observed; 534 KB workflow proved" -- a run id that is in neither run list of that
     workflow. INSTRUMENT CORRECTION #11: a workflow is proved to run by ITS OWN run,
     read from that workflow's run list with jobs > 0, never by a green-looking suite
     and never by a run id transcribed from elsewhere. This is L17's rule (a gate is
     fixed only when OBSERVED to run on its target) applied to the gate's EXISTENCE,
     not to its verdict, and it is L17's third instance.
     THE RULING. Pin the packs BY MANIFEST; cover the route on the caller.
       1. CATALOGUE_PINS carries the 11 SHA256SUMS.txt manifests, one per Final pack,
          plus the 134 files of the two packs that ship without one (HUM_00, 7; the
          Autumn 1 Fallback, 127 -- recorded, not invented). 145 pinned paths for 1750
          files; REVIEWED_PATHS 2246 -> 642, CATALOGUE_PINS 2296 -> 692, PIN1 2310 ->
          706 exact triggers per event, workflow 534,033 -> 139,627 bytes (main's own
          copy is 104,085). gateSha256 b1056230 -> fd3608a5.
       2. cross-estate-on-content.yml gains Humanities_Teesside/** beside
          Science_Teesside/**, on pull_request AND on push to main. push carries
          Humanities only: Science pack files keep their own per-file PIN1 paths on
          both events, and it is the Humanities members that stopped having one. The
          caller is admitted by DIGEST PIN (REVIEWED_PATHS), not by ALLOWED_DIFF --
          the #597 s1 route (b) precedent: ALLOWED_DIFF would let it change freely,
          pinned by nothing, which is how coverage falls away silently.
     WHY THIS IS NOT A LOOSENING, PROVED NOT ASSERTED. Dropping 1605 per-file pins
     would have stopped the gate digest-checking those bytes, so the indirection was
     carried into the gate itself, not only into GLV3:
       - catalogue_errors() expands every pinned manifest and digest-checks each of
         the 1605 listed members on EVERY run. Controls (gate self-test): member drift
         red / member missing red / manifest enlargement red on BOTH the expansion and
         its own pin / unreadable manifest red / empty manifest red / restored green.
       - GLV3's HUMANITIES_PACKS manifest route admits a member only when its manifest
         is pinned, the manifest's own bytes still equal that pin, the member is listed
         BY NAME, and the member's bytes equal the listed digest. Self-test 1321 -> 1330
         controls, 0 FAIL, carrying the ruling's three named red proofs: bytes drifted
         from the listed digest -> rejected; a file the manifest does not list ->
         rejected; a manifest enlarged to admit one -> stops matching its pin, so the
         route closes. Judge PASS, protectedChanges 1750.
       - The writer's "omits existing admissions" refusal is the control that stops an
         admission being withdrawn silently, so it was reconciled BY PROOF, never by an
         exception list: manifest_admitted() withdraws a per-file pin only while a
         still-pinned manifest lists that exact path at the digest the file on disk
         actually has. Contract controls 273 -> 280, 0 FAIL, including: a member whose
         bytes drift is no longer proved so its pin cannot be withdrawn; withdrawing
         the manifests withdraws the proof for every member they carried; and a
         manifest-admitted member's byte drift is rejected by the COMPLETE gate.
     NAMED CONSEQUENCE, FAILING CLOSED. boundary_errors() admits a changed path by
     exact membership of CATALOGUE_PINS, and it was deliberately NOT given a manifest
     route. It only ever sees --diff-filter=MRD, so the 1750 ADDITIONS never reach it
     and this PR is unaffected; but a future MODIFICATION of a manifest-admitted member
     will red there until it is admitted. That is a refusal, not a hole -- loud, not
     silent -- and it is the first item for the next pack update rather than something
     to widen here on my own initiative.
     STANDING RULE: an exact-path registry cannot carry a payload-scale population.
     When a pinned set would push the derived workflow past main's own scale, the set
     is pinned through a reviewed manifest and the manifest is expanded and
     digest-checked by the gate -- never pinned per file until the workflow stops
     loading, and never admitted by a directory wildcard.

L36  THE HUB IS DERIVED FROM A SIGNED RECORD, NOT FROM A TITLE  [ORDER HUB-1, 2026-09-20;
     strand record STOP-SIGN, C1 restated, W8 option (ii), W14 ownership].
     WHAT WAS ORDERED. Make lessons, packs and downloads easy to find on the composite
     Humanities hub (Humanities_Teesside/index.html): a Start-here strip (S1), ONE
     current card per week under Pathway -> Strand -> Term -> Week (S2), one card per
     pack with download links read from the pack's own manifest (S3), earlier versions
     in one collapsed section at the end (S4), terms from the subject's own bases (S5),
     filters and no-JavaScript order kept (S6); controls C1-C4 red-proved; nothing
     deleted (142 cards in == 142 out).
     THE RECORDS THAT DECIDE. Strand is derived from a record, never from a title:
     tools/catalogue/HUMANITIES_STRAND.json, 73 rows (one per served dated-folder
     lesson card with a week), basis named per row in the ruled precedence
     a) RE SoW week objective 14 / b) Humanities SoW week objective 35 / c) pair
     pattern 3 / d) content read 8 / e) Matt's rulings 13; UNASSIGNED 0. Signed
     verbatim on Matt's word and digest-pinned (a review decision, so a pin).
     Term bases are PER SUBJECT (ruling: option ii): the Humanities SoW's own
     7,7,6,6,6,7 -> 0,7,14,20,26,32; the spine's ruledMapping (0,8,15,21,26,33) is
     science's and stays with the science bindings. W8 -> Aut2 week 1.
     The route family IS the marking (M2 ruling): Humanities_Teesside/<dated folder>
     = current (82: 73 lessons + 9 folder start pages), *_Estate_v3 (27) and
     Build|Grow|Launch/Slideshows (25) = earlier, the rest (8) = reference.
     A Classic alternative is a badge-level card in the same week row.
     WEEK 14 OWNERSHIP (ruling 3, measured). Humanities SoW, Build Autumn 2 week 7:
     "Make a festivals display and gather UAS evidence" -> Festivals Display and
     Reflection (BUILD_W14-W20, whose START_HERE claims "Absolute week 14") is
     CURRENT; Industry and Nature: The Tees Story (BUILD_W9-W14, listed in no SoW)
     is the ALTERNATIVE, Humanities, basis (e), the sixth card of the retained
     OUTSTANDING_V4 Tees series.
     INSTRUMENT CORRECTION #12. Basis (c) is a rule with a precondition (a slot of
     exactly two cards). The first derivation applied it to a three-card slot and
     assigned RE to a local-history deck. A rule with a precondition must ASSERT
     the precondition; the basis key now records the withdrawal condition and the
     row reached Matt as a thirteenth ruling instead of hiding behind a green table.
     C1 RESTATED (ruling). Exactly one current card per (pathway, term, week, strand)
     slot that has a lesson ANYWHERE in the served estate -- the shelf OR the pack
     tree. Measured: 65 shelf-current slots + 55 slots filled by pack lessons
     (RE Aut1 4, RE Aut2 19, Humanities Aut2 2, Spr1 12, Spr2 18); double-current 0;
     UNASSIGNED 0. A slot the SoW plans but nothing serves is a GAP, listed in the
     hub's "Not yet published" note and here, never red: 39, all Humanities Summer 1
     (18) and Summer 2 (21). RE gaps 0, as the ruling expected. The ruling expected
     69 Humanities gaps; the measured 39 is the same rule applied to the pack tree
     as it stands -- the eight HUM Spring packs (36 lessons) serve Spring 1 and 2.
     THE WRITER. build_humanities_shelf.py reads the shelf record, the signed strand
     record, the pack tree (SHA256SUMS.txt / MANIFEST.json / DOWNLOADS_MANIFEST.json
     are the ONLY source of download links; 15 pack cards) and the two SoWs, through
     the shared tools/catalogue/hub_sections.py (the same change the science writer
     takes once it can run), and REFUSES to write while any C1-C4 control is red.
     Self-test 13 controls, 0 FAIL: double-current red / UNASSIGNED red / earlier
     card rendered as current red / current-family card with no strand row red /
     missing pack link red / dropped, duplicated and invented cards red / a pack
     lesson fills an empty slot green / a gap counts and does not red.
     It also writes assets/catalogue/humanities-hub-bindings.json: every slot, its
     current card and where it came from, its alternatives, the gaps, the packs.
     PROOF (Playwright Chromium 390x844, served at /Lessons/): S1 strip inside the
     first fold (cards at 346-571 px), no horizontal scroll; GROW · RE · Autumn 1 ·
     Week 4 (W4 · Eight Nights, One Lamp, and What the Light Is For; the RE SoW's
     "Hanukkah & the theme of light") opened in 2 taps, its pack lesson linked from
     the same row; Autumn 1 BUILD Complete Pack zip (4,124,845 bytes, HTTP 200) in
     2 taps; every pack card link resolves over HTTP; axe 0 serious/critical (one
     moderate heading-order); the strand filter works; with JavaScript off all 142
     cards are listed, current first, earlier last. Static gate PASS, linkedom DOM
     gate 28/28 PASS, contract controls 280 / 0 FAIL, gate self-test PASS, GLV3 judge
     PASS, PIN1 PASS.
     FINDING, NAMED AND CARRIED, NOT PATCHED. The two shelf writers scraped their house
     stylesheet from the root index.html's first <style>. The root page no longer
     holds that 18,657-byte block (its first <style> is a 651-byte header media rule),
     so a fresh run of EITHER writer produced an unstyled hub whose header overflowed
     to 701 px and failed contrast -- measured, and measured absent on the served hub,
     which still carries the old inline copy. The block now lives in
     assets/catalogue/shelf-base.css, carried forward VERBATIM from the served hub
     (not authored), pinned, and embedded by the writer. The science writer keeps the
     dead scrape until the shelf-restore order.
     FINDING, RECORDED UNDER TERM_BASES. assets/catalogue/lesson-order.json carries
     weeks for all 142 shelf paths: 62 rows agree with the record, 6 (the Tees series)
     have none, and the five Autumn-2 _Classic cards sit one week early -- base 8
     showing through. The hub derives from the SoW record, not from lesson-order's
     timing; nothing patched.
     STOP-X, SCIENCE LEG. build_science_shelf.py asserts every week binding's
     sourceSha256; 77 of 129 are stale (the 2026-09-06 audit), so the science hub
     cannot be regenerated without loosening that guard. The shelf-restore decision
     rules it; the science hub is re-measured as served (title sync 129/129 PASS).
     A RED FOUND AND FIXED ON THE FIRST HEAD, ATTRIBUTED. CI on #602's 3223563d: the VB
     mechanism battery marked g27_no_filename_weeks.py FAIL (VB-RUN13 R0: no tool derives
     a week from a filename or folder name). hub_sections.week_from_name() read W<n> from
     a filename to group Earlier versions, and the writer read W<nn> from a pack folder to
     key download rows. Both removed: Earlier versions group Pathway -> the shelf record's
     own term (lesson-order.json records a week for 1 of the 52, so a week grouping had no
     record behind it); a pack lesson's pathway, term and week are read from ITS OWN config
     text ("week": N, "term", "pathway" -- all 120 carry exactly one), and download rows
     are keyed by the lesson's directory and labelled by that week. Same derivation (55
     filled, 39 gaps); g27 PASS; the battery SUCCESS on 29886812. S4's "-> Week" is met as
     far as a record allows and no further.
     THE HUB'S BYTES MOVED WITH THE FIX, SO THE SIGNED TABLE MOVED. A signature that names
     digests is not stretched over new ones: the four changed rows were tabled again and
     re-signed (hub ea77a660->2c89f93d; resource-sizes abd0a1ba->aabb7da9; hub pin
     7594ce3f->6f69b888; gate 1987983a->3539ad6a), the five others unchanged. The Site
     prepare script asserts every built row equals the signed table before it writes.
     LANDING. Two Lessons PRs of <= 12 files with the Apps gate companion each, one merge
     at a time, each on its own green read: #602 -> a16505ce (with Apps #124 -> 553d3c14),
     #603 -> 9e8a947a (with Apps #125 -> f374e8cc). The gate observed on both mains by run
     id (35526015474 static-contract SUCCESS; 35526807463, all four jobs SUCCESS). The
     window opened exactly as named: publication 35526015846 on a16505ce red on the one
     path (UNREVIEWED shelf-base.css), FieldOps red only because it waits on it; at
     9e8a947a the publication (35526807535) red on the first tree censused
     (usage-registry), the six lessons-tree paths behind that halt. The Site window is one
     PR (#415): the seven-path table with the re-signature verbatim in reviewSources, both
     L31 pin pairs to 9e8a947a/f374e8cc, and one consequence of S3 named: the hub's direct
     pack links make the build emit 825 reviewed download rows where the list held 663 --
     the 663 kept in order, 162 appended, TEACHING_PACK_ADDITIONS_SHA256 re-pinned. The
     carrier bump on the first Lessons PR after the Site merge (L33) is the closer:
     Lessons #604 -> 9eca50b2 (with Apps #126 -> d4e0d608), education-pages.yml uses@ and
     builder_ref 3ed4577f -> 5a039ae1, the caller digest re-cut in both gate copies.
     THE CLOSER, OBSERVED (correction #11: by its own run id, never "did not run"). On
     9eca50b2 the Education Pages publication ran as run 35529424558, referencing
     education-publication.yml@5a039ae1, and completed SUCCESS at 18:41:48Z -- the window
     is CLOSED by that run id. FieldOps 35529424141 SUCCESS: its serve proof reads the
     publication provenance (lessons: checked source 9eca50b2 == deployed source, run
     35529424558, artifact 10611091922) and 59 of 59 derived routes served byte-identical,
     0 red, 0 inconclusive, 5/5 controls fired; unification 35529424116 SUCCESS; UX2
     35529424134 SUCCESS. Site main 5a039ae1: Domain split publication 35528465172,
     Education publication 35528465209, audience closeout 35528465178 and splash records
     35528465189 all SUCCESS (AGX-1 is pull_request-only: 35526945959 on the PR head,
     SUCCESS). Apps main d4e0d608: publication 35529440885, unification 35529440385,
     LundyLoop 35529440393, all SUCCESS. The hub's served bytes are proved by the chain,
     not by a hand fetch: the registry admits 2c89f93d, the publication that reads it went
     green on this tree, and the serve proof shows that publication deployed; the 390x844
     harness ran on those exact bytes. The serve proof's 59-route set does not include the
     hub path itself, and the live domain was not reachable from the landing session
     (proxy 403) -- recorded, not glossed.
     STANDING RULE: a hub groups by what a signed record says, never by what a title
     looks like; a slot the plan names but nothing serves is a listed gap, never a
     red -- and never a card invented to fill it. A signature names digests; when the
     bytes move, the table is signed again, never stretched.

L37  ORDER HUM-T, BATCH 1: THREE CORRECTIONS, THE STOP-T3 RULINGS, AND THE §Q4 RECORD
     (accepted by Matt Roper, 2026-09-20).
     1. A DIFF GATE ON AN EMPTY CHANGE SET IS NOT A PASS (instrument correction, own).
        The local battery ran the diff-based gates (cross-estate static contract, GLV3
        change boundary) before the commit, so they compared origin/main with an
        identical HEAD and judged nothing; the report said so, "protectedChanges": 0,
        and CI then refused the same head twice. The batch runner now commits first and
        gates the committed head, the way CI does. STANDING RULE: a gate whose population
        is the diff is proved only on a committed head.
     2. THE RENUMBERED CHASSIS CONTRACT ADMITTED BY NAME. The STOP-T2 ruling renumbered
        _sx3/CHASSIS_CONTRACT.md; its siblings SX3_PASSES_LEDGER.md and FENCE.json were
        pinned, it was not. Admitted through REVIEWED_PATHS, its digest carried into both
        gate copies, the trigger derived by tools/pin1/derive_triggers.py --write and
        asserted as a pair by PIN1 (710 asserted, 717 exact triggers).
     3. THE HUMANITIES REPLACEMENT DECLARER. The GLV3 fence protects the whole
        Humanities_Teesside prefix and had no route for an in-place deck edit; the
        designed admission is a declared replacement transaction, and only a Science
        declarer existed. tools/hum/admit_transaction.py derives the declaration (before
        blob from the merge base, digest and size from the bytes on disk, pin from the
        gate copy) and refuses a deck outside the measured landable set, an addition, a
        deletion, an unpinned deck, and a pin that disagrees with its bytes. Seven red
        proofs. replacement_errors is untouched.
     BATCH 1 LANDED: Lessons #606 -> 3887f7ac (squash), Apps #128 -> 327da98e; the
     unification gate observed on the PR head, run 35540344306 / job 106156730725,
     SUCCESS. On main: cross-estate contract 35541047675, GLV3 35541047347 and UX2
     35541047334 SUCCESS; Education Pages publication 35541047709 FAILURE as the L33
     admission red (the log names exactly the six decks, the lesson order and the size
     table), FieldOps 35541047352 red behind it ("exact-source publication failed"). The
     Site window is #416 (eight transition pairs derived from the local build, both L31
     pin pairs to 3887f7ac/327da98e); the carrier bump on this PR is the closer.
     STOP-T3, RULED. The census _hum/EVIDENCE_LIMB_CENSUS.md measured two digest fences:
     all 73 signed decks pinned in TERM_AND_STYLE_EVIDENCE.json, 31 holding a limb the
     re-stamp tool accepts; 27 of the David cover pack's 30 pinned routes signed decks,
     15 of them among the 31; 16 landable under both. Matt's rulings, 2026-09-20:
       Q1 YES. HUMANITIES_STRAND.json (signed, digest-pinned) is an accepted binding
          source: a deck's term.week may be proved by its strand row when no deck limb
          holds. Implemented as build_lesson_order.strand_proof (row present; record
          digest == its CATALOGUE_PINS pin; row term.week == the deck's own projection),
          asserted by check_catalogue_static.py on every strand-proved deck and used by
          the re-stamp tool through the projection; six red proofs in the re-stamp
          self-test (row absent, row week != projection, digest != pin, unpinned record,
          no projected week). The 12 decks that spell the whole A1 reference in the cell
          field (the doubled reference the gate can never find) are RECORDED HERE AS A
          DECK DEFECT for the evidence-model order, not corrected.
       Q2 YES. tools/hum/restamp_cover_routes.py re-stamps a cover route only when it is
          named in the batch's declared replacement transaction and its bytes on disk
          equal the declared transplanted bytes; basis recorded per route, verbatim:
          "re-stamped to HUM-T transplanted bytes under Matt's STOP-SIGN per batch;
          original review basis unchanged". Refuses a route outside the batch, bytes
          that differ from the declaration, a missing route, and a batch with no
          declaration; seven red proofs. The manifest is pinned afterwards.
       Q3 The order does not close at 16: all 57 proceed in batches under Q1/Q2; a deck
          neither rescues is HELD by name.
     §Q4 RECORD. tools/catalogue/TERM_BASES.json is created by SCI-COMPLETE PASS A (the
     first to land) with the science bases read from SCIENCE_WEEK_BINDINGS.json's own
     calendar note (Aut1 +0, Aut2 +8, Spr1 +15, Spr2 +21, Sum1 +26, Sum2 +33). HUM-T
     writes its humanities bases (Aut2 = 7 + n) into the same record when its first
     week-bearing change lands.

L38  A CARRIER THAT MOVES A PUBLISHED FILE IS NOT A CARRIER  [ORDER HUM-T batch 1, second
     window, 2026-09-20; INSTRUMENT CORRECTION #13, own].
     The L33 carrier for batch 1 (Lessons #608 -> 68635747, Apps #130 -> 166101ca) carried
     the STOP-T3 ruling Q1 tooling with it, and that tooling's record, strandProofs, rides
     assets/catalogue/lesson-order.json -- a file the Education Pages publication serves.
     The carrier's own publication was therefore refused by the very registry it had just
     been pointed at: run 35544583041, job 106168117337, "Education file admission blocked
     publication: CHANGED education-lessons/assets/catalogue/lesson-order.json". The
     admission fence held exactly as designed; the sequencing was mine, and L33 alone does
     not prevent it.
     STANDING RULE: the carrier bump rides a PR that changes NO file the publication
     serves. A carrier may move the workflow pin, the two gate copies, the static-check
     baseline and records outside the published trees (_sx3/, _hum/, _sci/); anything that
     changes lesson-order.json, resource-sizes.json, a deck, a shelf or any other served
     path belongs in the content PR whose Site window admits it. Proved before every push,
     not argued: tools/hum/check_carrier_pure.py takes the education-lessons key set of the
     Site's education-publication-admission.json as the served set, intersects it with the
     branch's changed and committed paths, and refuses a non-empty intersection by name. It
     refuses rather than passes when the registry is missing, unreadable, names no
     education-lessons tree, or admits no path. Seven red proofs plus the missing-registry
     refusal; and it reproduces this correction's own failure -- judged against the main
     the carrier left (3887f7ac), it names assets/catalogue/lesson-order.json, exactly what
     run 35544583041 named, and passes on the pure carrier that replaces it.
     THE SECOND WINDOW: Site #417 (claude/humt-b1-window-2), one transition pair derived
     from the local build of the two mains, assets/catalogue/lesson-order.json 34abdfee ->
     325b864f; the local build reproduced the CI refusal before the edit and admitted
     after it. Both L31 pin pairs to 68635747 / 166101ca, gate copies byte-identical there
     (gateSha256 fa70ffab). Nothing outside Matt's batch 1 signature of 2026-09-20 moves
     but that one record key: no deck, no week, no term.
     THE CLOSER is this PR, a pure carrier under the rule above; its Education Pages
     publication run id is reported to Matt with the batch 1 close and entered in the
     HUM-T CLOSE record.
     BATCH 1 SERVED PROOF (taken on the publication's own output bytes for 3887f7ac; the
     six decks' bytes are unchanged since, which is why this window admits only the lesson
     order): BUILD_HUM_W1_People_Special_To_Me.html, served digest 9a93f7be, admitted by
     the registry; 7 panels, 7 reached by the deck's own navigation (row 41); rows 38-40
     7/7; rows 45, 45.1, 45.2, 13 and 46 PASS; axe serious 2, pre-transplant 2, so 0
     introduced.
