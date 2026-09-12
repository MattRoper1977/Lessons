# RF3 continuation — 12 September 2026

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

This supplements `RF3_HANDOVER.md` at `cb5b2966`; the original is unchanged.

## Durable work and release sequence

Claude's local-only `f746d5f81118bef0b8ec5d9c2d6b8a5e888bf639` was unavailable:
its container path is absent here and GitHub could not resolve that object. Its four
authorized clauses were reconstructed, not recovered verbatim. The repair was pushed
to the existing `codex/rf1-prx1-candidate` branch as `6ba679ac48ec22917bcc96908ed4ed1dfe759d19`.
Final evidence-only head: `70a22acb08fb8a2fa401015a8fde4bafdf401ebf`.

Full production pipeline golden, measured 09:27 UTC: **33/33 byte-identical
operations, 28 headers and five mains, zero new raises**. These operate on 28
distinct replacement pages. Three body insertions are separate. Both upstream
education discovery/expansion generators ran. Actual full-function comparisons and
unchanged-byte refusal plants passed at 09:30 UTC. Reproduction scripts, input refs,
per-target hashes, DOM-tree question and complete classified census are committed
in Site `reports/prx1/DECISIONS.md` and `SHAPE_CENSUS.md` at the final head.

| Transaction | Merge | Normal Education publication | Result |
|---|---|---|---|
| #351, inherited | `30e86ad64bd1aaaf3a6887f9eb4cd4d9dbcde436` | `34684701623`; deploy `103530234267` | SUCCESS, re-read before #346 |
| #346 | `3b82e4f945ebb9d4662bee2136c694a7b548503e` | `34685950395`; build `103532851601`, deploy `103533535796` | SUCCESS |
| #350 | `9dcaa721426e499d511001aec4e22314e84d7ae7` | `34686576342`; build `103534489233`, deploy `103535017631` | SUCCESS |
| #352, ML1 historical notice | `5ec70ec5a56c4814140db191bef2f33e4c94adb9` | `34686941860`; build `103535460569`, deploy `103535988423` | SUCCESS |

All four required checks passed at each final PR head before merging. #350's
additional Complete separated publications job `103533249403` succeeded; #346's
remaining generator job `103533567291` succeeded. #350 main's later generator
`103535049641` and separated-publication `103534489291` also succeeded. Two post-main shelf
failures were read from actual logs: jobs `103535049846` and `103535049464` both assert
`Missing current shelf control #group`, matching the inherited baseline. No check
was weakened. No whole-estate green is claimed.

ML1 is CLOSED-BY-DL under Matt's ruling. #352 adds only a historical/superseded
notice to `docs/MBM_LIVE_MIRROR_LEG_DEADLOCK.md`; all original text survives unchanged.
No obsolete patch was replayed, repaired or deleted. #350 is PRX1_CLOSED for the
authorized RF3 candidate scope; other writers remain unmodified census findings.

At Lessons `ae5e96becac7bb12e8fe9501fe7fdb8b9f6745ae`, the existing handover branch
now contains P5.5 in `docs/orders/RF3_FINDINGS.md` and Matt's exact PIN1 ux2-gates
ruling appended to `docs/orders/LP1_PIN1_S1_CENSUS.md`. REGISTER.md was not edited.
Those internal docs paths are excluded by the actual publication policy at both
current Site and Lessons' pinned builder. This does not claim the wider Lane G
ledger migration is complete.

## Historical Computing preflight — superseded by current checkpoint

Lessons #493 remains OPEN, head `c460eada50a93b266f7330e70cb436b82ec6304d`.
Its instruments dependency #492 is merged at `00d052e57564460e6199170af6e441bd7e02bdbf`.
All eight recorded #493 checks pass, but these do not replace fresh publication proof.
An isolated local merge with current Lessons main `aad04718c11a2396ecf323a662f55bf0e0c2441b`
is clean: candidate `e5efff3b069c0b595992dc1454abe169473b0371`, tree
`751fcc8bd12316869cea5f5f78c353f718e8ecd8`. Exactly 164 files change: 163 under
GROW_Computing and ICT/Teaching_Packs/index.html. The neighbouring unit and caller
pin are unchanged. The full build and all-file admission with 61 controls passed.
Inputs are actual Lessons builder `810ae8f8830dc9e30a7ceec9ada4ec24d575a04d`
and its selected Apps `3ad0a7df958274e5401e8d40d0a94096be0962bc`.
Do not revert the caller to the historical 2e49afdd pin.

Local workspace: `/workspace/scratch/1703bef47fa2`. Candidate is `gc1-current`,
builder is `builder-810`, output is `builder-810/domain-split/output`, logs are
`recovery/gc1-build.log` and `gc1-admission.log`. Isolated test #511 passed and closed
unmerged; required G10 and full G13 interactions remain unmeasured. See the phase
readout for the narrow continuation needed at the blocker ceiling. Preserve original
paper route, paired downloads, seeded faults and awarding-body document identities.
Content PR and resources.json catalogue PR must stay separate. Never infer P2Q.

## Programme board retained

| Row | Scope | Position / next eligible action |
|---|---|---|
| 1 | SX2R §5 + TH1C | S1-M closed; TH1C full original still missing; recover documentary residue only |
| 2 | GW1-E → GW1 B–F → LW1 | Original scopes missing; do not reconstruct authority from titles |
| 3 | GC1 #493 | Content merged 36ea1046; registration repair Site #353 / Apps #83 / Lessons #512 merged and deployed, Lessons db5d804f. Admission 61 controls PASS; live 39/39 identical. P6 catalogue and admission complete via #513/#514; live card/8 prints/24 byte comparisons pass; baseline audit red recorded |
| 4 | ML1 | CLOSED-BY-DL; historical notice #352 merged and deployed |
| 5 | PRX1 | Authorized RF3 repair merged and deployed, full golden proved |
| 6 | BL1 | Approved #351 → #346 → #350 sequence completed; #291 HELD |
| 7 | LP1 | Census materially changes scope: 18 gated proofs (16 collapsed maker steps), plus 21 separate no-PR-trigger proofs; §5 STOP pending scope ruling |
| 8 | PIN1 | Ruling filed; 444 distinct pinned paths, 443 excluding caller, five registries, one asserting digest gate; implementation not closed |
| 9 | SB1 | Full order recovered; existing parent tool inspection underway; due before second unit, not before #493 |
| 10 | LF1-M | Full original missing; retain S06/S04 S2 and B02/B05/V04 replacement holds |
| 11 | UX1A | §3+ missing; reconcile with landed UX2/SW2 after recovery |
| 12 | SW2 → Part B | Supplied sequence retained; Lessons #456 HELD; partial UX1B §1.5+ missing |
| 13 | UX1C | Full original missing; no competing homepage/hub/resources work |
| 14 | GC1 P2Q | HELD until Matt names second unit |
| Added | AR / S1-M | Closed; do not replay; findings migration remains separate |
| Added | AS1 | Closed; no implied Play rollout |
| Added | SCI-UP1 | Archives, 90 IDs, 68 live routes and 117 SoW cells checked; placement/QA/admission pending; governing family limit unlocated |
| New | FP2 + return week | 19/19 card-file manifestations verified; nine related live Code E panels exposed; report-only pass complete, Code E held |
| New | Findings ledger | P5.5 filed; broader relocation outside served tree not done under no-REGISTER-write hold |

The LP1/PIN1 figures above cite the source census measured 12 September 00:34–00:46
UTC, rechecked against unchanged workflow source at Site 3b82e4f. They are not live
proof counts. The opening 89-path PIN1 figure remains unlocated.

Standing limits survive: #291 untouched; Lessons #456 held; Games #78/#79 remain
with pin owner; Apps #91/#106/#109 closed unmerged with branches preserved; no
REGISTER write, brand-asset replacement, size-table ratchet or check weakening.
Three distinct blockers stop their lane, not every other eligible lane.

Small-pass continuation at 12 September 10:41 UTC: Matt authorized the missing
Computing proofs; all pass without content edits. Earlier 192-position coverage
was partial because Weeks 1–2 have ten slides each. Complete required 390px
coverage is now 204 positions. See RF3_PHASE_READOUT.md and
rf3-evidence/gc1-interactions-readback.json. This checkpoint completes the proof
pass; it does not merge #493 or close P6. Other holds are unchanged.

Release-pass correction: final guide read found the same conditional later-device
Outcome 5 requirement in its DOCX and PDF. No later resolving ruling recovered.
G14/G15 prevent merging #493; no merge attempted. This supersedes the earlier
“content transaction next” readiness statement, not the valid browser proofs.

Later user clarification supersedes the advance-lead-approval hold above: all
pupils have laptops; normal Scratch work is captured, printed, scanned and emailed
as a PDF through the existing lead process. #493 merged 36ea1046 with exactly the
tested tree. This is not proof of device-free parity. P6 remains separate.

Historical initial publication readback (superseded): 34690363074 build 103544411018 FAILURE, deploy
103544618859 SKIPPED. Exact delta: 36 existing ICT registrations unchanged,
128 new Computing rows unregistered; zero removals/changes. No live deployment.
That publisher-registration repair and deployment verification are now complete; see the current checkpoint and GC1_REGISTRATION_RELEASE.md. P6 remains next.
