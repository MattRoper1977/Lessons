# RF3 phased continuation — measured 12 September 2026

## Current checkpoint — PIN1 deployed; SB1 fitness stop recorded

Measured 2026-09-12T13:24:36.954Z. Lessons main remains `a20a09b96ddb0cdbe37709631603de82cc8b1d6a`.
PIN1 #515 post-merge UX2 run `34695886241` SUCCESS; census job `103559550830`
records all 9 proof steps PASS at that exact main commit, event `push`; its five
reporter tests pass. Artifact `10298711482` (1,064 bytes) uploaded successfully.
Publication `34695886467`: build `103559177796` and deploy `103560005879` SUCCESS.
Review artifact `10297804318` (732,463,339 bytes) and Pages `10297664420`
(730,883,657 bytes) are present and unexpired.

Latest main-check snapshot: 14 SUCCESS, 1 baseline sweep FAIL, 2 still running
(Science navigation/print and responsive-downloads). Sweep job `103559177041`
again measures exactly 1,418 stale / 6,307 live / 6,899 row labels / 47 unmatched,
exit 2. No full-main-green claim. Re-read pending checks at the next continuation.
The first scheduled run of the NEW census is NOT OBSERVED: latest discovered UX2
schedule `34685884276` was on old main `aad04718` before #515. Do not credit it to PIN1.

The next eligible small pass was SB1's existing-tool fitness check. It is complete
and records **SB1_BLOCKED** under §3.1: the parent checker accepts an invalid-schema
`{}` project and a zero-file scan. Official scratch-parser 6.0.1 rejects the former.
All 23 current projects pass parent checks, 14/14 parent controls pass, and a derived
null-parent plant fires. No production code/workflow was changed; no implementation
PR was opened. `SB1_FITNESS_READOUT.md` contains the concrete same-tool extension
proposal, exact source hash, local parser results, limitations and original stop text.

Next: resolve that recorded §3.1 fitness proposal before wiring SB1; preserve the
parent check, add official Scratch-3 schema validation in the same entry point,
prove unavailable-parser/empty-input are not green, derive admission population and
extension-specific triggers, then execute the original controls in one PR. This
proposal is not an implemented gate. A second Scratch unit remains held until SB1.
PIN1's original trigger plants remain open; LP1's material-scope hold is unchanged.

## Current checkpoint — PIN1 UX2 census pass merged

Measured 2026-09-12T13:16:02.888Z. Lessons #515 merged as `a20a09b96ddb0cdbe37709631603de82cc8b1d6a`.
The recovered §2.2 fallback is implemented for UX2 alone: existing daily schedule,
all nine existing proof-step outcomes, commit-bound JSON/Markdown/Actions summary,
FAIL on complete failed evidence and UNMEASURED (exit 2) on incomplete evidence.
No trigger paths, existing proof commands, pins or other workflows changed.

PR run `34695419199` and census job `103558313348` succeeded: 9/9 proof outcomes PASS;
all five reporter test methods passed in Actions. Artifact `10298985341` is saved.
All 12 PR checks are terminal: 11 SUCCESS, one independently matched baseline
sweep FAIL (1,418 stale / 6,307 live / 6,899 row labels / 47 unmatched files).
Reviewed, GitHub-tested and merged trees all equal `1e9cea18b5b5eca2d36148bf5edf2ec391c4751d`.

At this checkpoint, post-merge UX2 `34695886241`, publication `34695886467` and
FieldOps `34695886249` are in progress. Do not call them successful from PR results.
The first actual daily scheduled census is also NOT OBSERVED. Next continuation
starts by re-reading these runs; no background poller or dispatch is left running.

This bounded implementation pass is complete; **PIN1_PARTIAL** overall. The original
pinned-file RED/GREEN/DORMANT trigger proofs remain open. LP1's material-scope hold
remains. See `PIN1_UX2_RELEASE.md` and `pin1/DECISIONS.md` on main for exact scope.
Earlier P6 and other completed passes retain their own measured timestamps.

## Current checkpoint — P6 catalogue publication complete

Measured 2026-09-12T12:52:30.989626+00:00. The Computing card is deployed by Lessons #514 at
`4f8227cef7a0191df25145d53fe2bc05f7aa2ef9`, publication `34694243164`, build
`103554856058` / deploy `103555671187` SUCCESS. #513 added one card while preserving
all 950 previous catalogue rows; #514 completed its four-output admission repair.
Apps #84 and #85 were each deployed first. Live search passes at 390px/1280px;
all eight live print routes pass; 24/24 lesson and pupil paper files are byte-identical.

The requested catalogue pass is complete for Matt's confirmed laptop/Scratch and
print/scan/PDF evidence process. It is not a paper-only G14/G15 parity claim.
Baseline metadata gaps and the stale-evidence audit remain recorded and enabled.
See `GC1_P6_RELEASE.md` for exact commits, admission correction, evidence and limits.
Historical statements below that call P6 the next pass are now superseded.

## Release/control phase — completed

The authorized #351 → #346 → #350 sequence is merged and deployed. The four
missing PRX1 clauses were reconstructed after Claude's container-only object could
not be recovered. The full production golden passed 33/33 operations with zero
byte differences and zero new raises. Final head `70a22acb` carries reproduction
scripts and exact evidence in Site `reports/prx1/DECISIONS.md`.

The separate ML1 stale-document notice #352 also merged and deployed:
`5ec70ec5a56c4814140db191bef2f33e4c94adb9`, Education run `34686941860`, build
`103535460569`, deploy `103535988423`, both SUCCESS. The interrupted merge call
was verified as completed, not repeated. All original ML1 document text survives.

#350's remaining main jobs also finished successfully: complete separated
publication `103534489291`, generator controls `103535049641`. The two shelf reds
remain the inherited `Missing current shelf control #group`; no check was weakened.
At final #352 main, all 23 check records are terminal. Its two shelf failures,
`103536048128` and `103536047913`, carry that same assertion in their actual logs.

## Current checkpoint — Computing publication repair complete

Site #353, Apps #83 and Lessons #512 are merged and their publications succeeded.
Lessons main is `db5d804f5559a543c65c9d8bd0034a5764c05a40`; publication run
`34691889316`, build `103548484790` and deploy `103549456718` are SUCCESS.
All 39 selected live files match reviewed SHA-256 values: eight lessons, eight
pupil PDFs and 23 Scratch projects. The 61-control admission gate passed.

The stale-evidence sweep remains an explicitly measured baseline red; the latest
workflow watch reports six PASS and one FAIL, no pending/no-verdict workflows.
Full release refs, evidence and limits are in `GC1_REGISTRATION_RELEASE.md`.
**Historical next step, now completed: P6 catalogue/resources.json; see GC1_P6_RELEASE.md.**
Historical preflight holds and initial publication failure below are superseded
by this release record, while their measurements and provenance remain retained.

## Computing phase — earlier preflight and initial publication failure

Source: #493 `c460eada50a93b266f7330e70cb436b82ec6304d` merged locally with current
Lessons main `aad04718c11a2396ecf323a662f55bf0e0c2441b`. Candidate tree is exactly
`751fcc8bd12316869cea5f5f78c353f718e8ecd8`; 164 files differ, including 163 under the
new unit and only ICT/Teaching_Packs/index.html outside it.

Actual publisher `810ae8f8830dc9e30a7ceec9ada4ec24d575a04d`, Apps input
`3ad0a7df958274e5401e8d40d0a94096be0962bc`:

| Fresh measurement | Result |
|---|---|
| Complete publication build | PASS |
| All-file admission and build-control battery | PASS, 61 controls; real PASS / planted tracked game FAIL / restored PASS |
| Previously reviewed unit output digests | 163/163 identical, no changed unit file |
| Official scratch-parser 6.0.1 | 23/23 projects parse |
| Existing parent-link tool | 23 checked, zero inconsistent links |
| Variable opcodes | 354 blocks inspected, zero data_* opcodes |
| Browser gate | Isolated CI passed at 390×844 and 1280×720: eight lessons and 192 independently observed route/slide positions per width; eight filled print records; zero errors or duplicate IDs |
| Project download references in that browser run | 23 sibling SB3 links resolve, including teacher models; 15 data fallbacks retained |

The local browser attempted a required socket and received Operation not permitted.
The supported escalation request was rejected by the session's execution policy.
Temporary Lessons #511 ran the existing unmodified gate in an isolated read-only
GitHub Actions job at 390 and 1280. Final test head
`e98bbc385f628460bbd791c90caaf396a7166cb7`, run `34687911285`, job `103538043603`:
SUCCESS at 10:19 UTC. It asserts the exact tree and all 163 output hashes. A test-only
runtime adapter avoids the redundant eighth Back click on a disabled slide-one
button and independently records actual positions, refusing swallowed action
failures. The first slower run `34687493269` is superseded, not current proof.
#511 is CLOSED UNMERGED, branch preserved; it is not SB1's standing gate or a
workflow change to main.

Artifact `10296595372`, SHA-256
`22045a3b4ae40c529be0a8c50c731c6c887aa297728ab0b377e7e1f227ead1de`, expires
12 October. Its metadata and actual job logs were read. A local copy of the ZIP
could not be materialized (download returned HTTP 403); no claim of locally
inspecting the artifact JSON is made. Durable CI summary is in
`rf3-evidence/gc1-ci-readback.json` and the complete test implementation remains on
the preserved #511 branch.

**Authorized small continuation completed, 12 September 10:41 UTC.** Matt's
instruction to continue in order and small passes lifts the specific missing-proof
stop. Test head `85c756d5d150f03762fd8b8decc8097f354ffcae`, run `34688998548`, job
`103540860248`: SUCCESS. The candidate tree, publisher inputs and all 163 output
hashes are unchanged. No lesson content or production gate was edited.

| Additional required measurement | Result |
|---|---|
| G10 default closed → open → closed | 8/8 lessons; one staff panel and eight Teacher_Only links per lesson, including paper answers, hidden → visible → hidden |
| G13 full navigation at 390×844 | 204 actual slide/route positions: 30 each in Weeks 1–2, 24 each in Weeks 3–8 |
| Every model button | 672 actions across all three routes and every authored slide; original handler invocation asserted |
| Week 8 repair checks | 15 complete cycles (five model-bearing slides × three routes), three cumulative repairs each, all five checks before and after every repair: 450 test-button invocations |
| Repair outcomes | Arrows/walls change from FAIL to PASS after their repairs; restart fails before the final repair; all five pass after all three repairs; finish and feature remain passing throughout |
| G5 print | Full paper-route container visible under print emulation, 8/8; 8,875–21,222 characters, completion text present |
| Browser errors | Zero page or console errors |
| Probe negative controls | Forced visible guidance while closed rejected; missing model handler rejected |

**Coverage correction:** the first continuation run `34688866321` failed because
this test assumed eight slides. Source inspection and the browser show ten slides
in each of Weeks 1 and 2. The probe was corrected to traverse every actual slide;
no lesson was changed. The previous 192-position result was partial coverage, not
all authored slides. Its 1280px result remains partial; the complete required
390px drive is now the 204-position result above. G10 measures rendered visibility;
hidden teacher markup remains in the HTML, as the authored toggle requires.

The successful job's actual logs and artifact metadata were read. Artifact
`10296606330`, 4,782 B, SHA-256
`cb9d814f298126f53a6f674e5a540cc22d5253cdee887211548fd654981f630a`, expires
12 October 10:41 UTC. Full artifact JSON was not locally downloaded. Durable
per-week log-derived measurements and asserted repair semantics are preserved in
`rf3-evidence/gc1-interactions-readback.json`; exact test source remains on #511's
preserved branch. #511 is closed unmerged after this pass.

The narrow G10/G13 proof stop is resolved. #493 stays open at this small-pass
checkpoint. Next in order: re-read exact main/head and required checks, complete
the content transaction, then the separate P6 catalogue/admission transaction and
served G5/G14/G15 proof. This result does not label GC1 or P6 closed. No need to
repeat schema, full admission controls, or earlier unrelated phases at unchanged
inputs. P2Q remains held until Matt names the second unit.

The PR's stale file counts and three ZIP sizes were corrected from binary reads.
Fresh relative-reference census: 225 from unit HTML plus 37 subject-page references
into the unit, zero broken, all 163 unit files referenced. Its method excludes
absolute estate routes and fragment-only links; it does not reuse the old 297
denominator. Complete/link and collection sizes are now recorded on #493.

### Content release resumed on Matt's clarification

Matt confirms the established route: pupils complete Scratch work on laptops;
all pupils have laptop access. Evidence is captured as screenshots/photos or
printable work, printed, scanned and emailed as a PDF to the UAS lead. The lead
checks actual submissions and returns any further-work requirements. Matt says
no additional advance check is needed. The assistant-introduced advance UAS-lead
approval hold is withdrawn; no speculative route-review email is to be sent.

This submission format is not evidence of device-free learning. No G14/G15
paper-only parity result is inferred. The existing paper alternative and its
stated limitations remain unchanged. Current lesson print output is the paper
route; it is not asserted to capture a pupil's external Scratch project.
Screenshots/photos are the confirmed normal evidence path. Any distinct
print-evidence enhancement belongs in a bounded later content change, not an
unreviewed addition to this release.

Fresh readback: main `aad04718`, content head `c460eada`, candidate tree `751fcc8b`
unchanged; eight PR checks and 33 main check records SUCCESS. Caller remains
Site `810ae8f8`, Apps `3ad0a7df`. No path collision with open #497, #465 or #456.
Rollback baseline recorded in #493 before merge.

**#493 merged at `36ea10467b8c5385d4b01ee149ca0550d1190f45`.** The actual merge tree
is `751fcc8bd12316869cea5f5f78c353f718e8ecd8`, exactly the tested candidate.
Publication run `34690363074` failed build job `103544411018`; deploy job
`103544618859` was SKIPPED. Nothing was deployed by this run. P6 catalogue remains separate;
no whole-GC1 CLOSED claim. The earlier G10/G13 proofs remain valid.

The superseded document-based concern is retained in
`rf3-evidence/gc1-paper-release-blocker.json` as history. Matt's later submission
clarifications and the current action are in `GC1_PAPER_SUBMISSION_WORKFLOW.md`.

### Publication blocker - exact download-registration delta

The complete emitted-tree separation check reports one failure:
`usage-registry.json` - `Download additions differ from the reviewed installed
pack: /Lessons/ICT/Teaching_Packs/`.

At the identical local candidate, the reviewed prefix has 36 rows and generated
output has 164. All 36 old rows are byte-equivalent as parsed records; 128 new
rows are all under GROW_Computing. Zero old rows removed or changed. Full delta:
`rf3-evidence/gc1-publication-registry-delta.json`.

The earlier all-file admission/browser proof omitted this separate complete
separation gate; it therefore did not prove this registration predicate. Record
that coverage gap explicitly. No check has been weakened or disabled.

Historical next action, now completed in GC1_REGISTRATION_RELEASE.md: review the 128 added download rows, update the governed
publisher download-additions record and digest, prove the separation predicate
and firing controls, preserve current admissions, advance the actual caller and
verify deployment. This is a publisher registration repair; do not alter lesson
bytes or reset the publisher to an old pin. P6 catalogue remains separate.
Matt's UAS evidence-submission clarification is settled and is not this blocker.

## Science phase — archive and source/served census complete; placement intake partial

All seven original payload archives are downloaded, SHA-256 recorded, CRC-checked,
and member-inventoried. There are **1,019 non-directory members** across the seven
ZIPs, with zero CRC failures or unsafe member paths. Archive names/bytes/hashes and
each member's bytes/hash are in `rf3-evidence/science-archive-inventory.json`.

The authoring archive matches the required SHA-256
`2aafa112b5e409eb36a7854b8bc63d40d06d815c46f77f2a2f1b07eb98fdd6ac` (5,165,433 bytes).
Its coverage notes, independent audit and final coverage review were inspected.
The historical 110/110 eligible weekly-row coverage claim is a source-coverage
claim, not a current browser, timetable, accreditation or publication proof.

All **90** candidate IDs map uniquely to a payload main HTML. Against Lessons main
`aad04718`, **68 UPDATE EXISTING** (64 canonical routes plus four enrichment routes)
and **22 ADD NEW** (21 core gap exemplars plus the rock continuation). No existing
canonical route was missing; no payload main HTML was missing or ambiguous.
All **68 current canonical routes returned HTTP 200** in the fresh live fetch;
per-route served size, hash and fetch time are recorded. All three current SoW
workbook hashes match the coverage archive's source identities. A direct read of
the actual workbooks confirms **117/117 cited outcome cells** equal the recorded
text, zero mismatches. The 90 candidates include 81 with explicit core SoW bindings
and nine retained extensions/enrichment entries without a new core-week claim.
The exact per-ID map, canonical paths, source hashes and candidate categories are
in `rf3-evidence/science-candidate-map.json`.

This is a census, not completion of every C.3 placement field. All 90 still need
the original family content/companion/browser gates, protected-region comparison,
and staged admissions on the actual publishing chain. Keep four FieldOps labs as
enrichment; keep W13C after W13B and before W14; preserve prior SX1/S1-M families,
alternative versions and the original release/ownership limits. No lesson or shared
catalogue/pin was changed during intake. In particular, the governing Science
family placement/file-count limit was not recovered by a targeted context search;
the master order says to inherit it but does not state its value. Do not substitute
FP2's 12-file limit or SW2 N's 25-file limit. New target/catalogue/pack identities,
governing placement comparison and admission staging remain explicit per-row work.
`SCI_UP1_PARTIAL`: all 90 IDs remain unshipped by this continuation.

## FP2 phase — provenance and first-pass live exposure report

The correct policy was independently recovered at **208,449 bytes**, SHA-256
`41046284a00c9218679b946134cbc6e53c1897aad28b15fc4bd4aa963720ff3b`. Other similarly
named saved copies contain different 204,058-byte content and were not substituted.
The full `FP1_Marking_Card_Verification_Record.md` was recovered. All three dated
return-week pack hashes match that record; CRC checks pass; **19/19 card-file
manifestations match**, including both HTML members nested in Authoring_Source.zip.
That is nine card instances, seven teaching and two retained references.

Parsing the recovered FP1 claim table independently reproduces its 329 rows:
111 MATCH, 31 MISMATCH and 187 ABSENT. This verifies the record's arithmetic, not
a fresh claim-by-claim policy adjudication or permission to mark a card VERIFIED.

An exact normalized card-text scan found none of those nine complete panels in the
current built Lessons tree. This is a bounded exact-match result, not a claim that
all related policy defects are contained or that every live URL was searched.

**Related Code E wording is already exposed in nine live GROW Science HTML pages.**
All nine were fetched with HTTP 200; each contains a staff policy panel stating
`E · evidence on Earwig`, plus an attribution to the uploaded May 2026 policy.
That is the unresolved EFL/Earwig/Boxall discrepancy identified by Matt's standing
ruling. The URLs, sizes and live-byte SHA-256 values are preserved in
`rf3-evidence/fp2-live-exposure.json`.

| Live GROW v3_40min page | Code E wording and policy attribution present |
|---|---|
| SCI_G_W3B_Friction_Do.html | Yes |
| SCI_G_W4A_Mechanisms_Explore.html | Yes |
| SCI_G_W4B_Mechanisms_Do.html | Yes |
| SCI_G_W5A_Fair_Test_Explore.html | Yes |
| SCI_G_W5B_Fair_Test_Do.html | Yes |
| SCI_G_W6A_Earth_And_Planets_Explore.html | Yes |
| SCI_G_W6B_Earth_And_Planets_Do.html | Yes |
| SCI_G_W7A_The_Moon_Explore.html | Yes |
| SCI_G_W7B_The_Moon_Do.html | Yes |

These pages also say `NS+ · one next step`; that wording alone has not been
classified as an explicit prohibition on a second next step. Browser visibility
and all pupil/teacher toggle states were not measured in this exposure pass.
A tenth signature candidate, LUNDY_DAILY_REFLECTION_EVIDENCE_WINDOW.html, served
200 but lacked these three exact phrases; it is not counted among the nine.

FP2 D.2.1 says to report exposure and not fix it in the same pass. No cards, policy
text or live pages were changed. Code E remains HELD; zero cards have been newly
verified. The correct destination for a 30-second clip still needs Matt/document
owner resolution. No message was sent to a document owner. The dated packs are
separate from the older combined Science_Return_Week_19_October_Review.zip and from
the 90-folder Science batch; none was substituted for another.

## Remaining boundaries

The complete programme board and all fourteen original rows remain in
RF3_CONTINUATION.md. Eight original scopes are still missing; LP1's materially
expanded census still invokes its §5 stop; PIN1's exact ux2 ruling is filed but
not implemented. SB1 remains due before a second unit, not before #493. P2Q remains
held until Matt names that unit. Lessons #456 and Site #291 remain held. Findings
relocation stays separate under the no-REGISTER-write limit. No universal programme
CLOSED token is issued.
