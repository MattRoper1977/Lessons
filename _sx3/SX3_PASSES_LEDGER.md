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
