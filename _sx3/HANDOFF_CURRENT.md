# HANDOFF — current state (overwritten at every DONE and every STOP)

## 0. Read this first

The one-read handoff for Lessons, Site (`mattroper1977.github.io`), Apps (`Matt-s-Apps-`), Games
and Games-. Overwritten, never appended: `git log -- _sx3/HANDOFF_CURRENT.md` holds every earlier
version (23 Sep: c2169dcb, #669). Written 27 Sep 2026 at a STOP by session
https://claude.ai/code/session_01GpMenFJ7hQxSZE4g9Nfut9. Replaced at every DONE report and every
STOP by one docs-only PR that changes this file alone, never inside a landing window
(2026-09-27_HANDOFF-RULE.txt).

**Who rules.** "Claude" in this file is the reviewing Claude conversation; its rulings reach a
working session through Matt, the site owner. A working session never rules for itself: anything
unruled is a STOP (§9.3).

**Situation (27 Sep, ~17:15 UTC).** LAND-SCI-56 v2 (Science lands once: 56 lessons) is at **STOP
before W1**. Its prep fired four of the order's own STOP conditions (accessibility lost against
live, point 1; banned words and wrong lines, point 5; hub gaps, point 4; route gaps, point 7) and
one CI gate (`git diff --check`). Claude has **ruled the STOP report in full** (RULING STOP-SCI-56,
27 Sep, §6): one more supplier round, **SC3R4**, re-cuts all 24 week ZIPs (all 56 lessons, the 21
P1s included) from the report's §3A table plus the SG ruling (SG1–SG15). Claude issues that order
to GPT; the working session sends nothing to GPT. GPT's deadline is Fri 9 Oct, Mon 12 Oct at the
latest. **Nothing pushes and nothing lands until Claude's own check of the SC3R4 re-delivery says
go** (Claude sends its hashes). This file's docs-only PR is the only exception. Lessons and Apps
mains have not moved since 26 Sep; Site main last moved 27 Sep 08:16Z (#452).

## 1. The exact next step

1. Re-read the five mains with `git ls-remote` and compare with §2. Expect Lessons main to be
   exactly one docs-only commit on 372debcd: this file's merge, whose diff from 372debcd is only
   `_sx3/HANDOFF_CURRENT.md` (step 4). Either way run the order's BASE check (§5, item 1): diff
   Lessons main against 372debcd over the estate files the records name; expect 0 changed (0/28,
   and 0/214 if D44 widens it); any change is a STOP.
2. Obtain the files in §8 from Matt and check each sha256 before use: first
   `RULINGS_2026-09-27.zip`, `STOP_REPORT_LAND_SCI56.md` and
   `LAND_SCI56_STOP_EVIDENCE_2026-09-27.zip`.
3. The STOP report is ruled (§6). **Nothing lands until Claude's check of the SC3R4 re-delivery
   says go**: no window, no content PR, no mailing merge. This file's own docs-only PR is the only
   exception. Until then, build the step-3 tools the ruling asks for (§6, "What the ruling sets"),
   on a scratch branch only: no draft PR before the hardened guard is green on the frozen tree
   (D34), because the repos are public.
4. For this file's merge commit, confirm (report at the next STOP or DONE): the diff from 372debcd
   is only `_sx3/HANDOFF_CURRENT.md`; its publication succeeded (run id); then **dispatch** Site
   `mailing-functions-live.yml` and `published-completion-verify.yml` (workflow_dispatch; nothing
   on the Site runs on a Lessons commit) and record both run ids. Whether that SHA becomes the
   landing's BEFORE is D45; nothing branches from it before then.
5. When the SC3R4 re-delivery and Claude's hashes arrive (through Matt): check every ZIP by hash,
   re-run the whole prep on a frozen tree with the step-3 tools, then follow the STOP report's §4
   steps 3–10 in order: → build the Lessons branch → W1 → Apps gate copy → Lessons content PR
   (carrier last) → Site W2 EQUAL → Apps companion → pure carrier → LAND_SCI56_DONE → handoff PR.
   Any new finding outside the ruled classes is a STOP. Code sends nothing to GPT.
6. **Yield rule** (MKT1-Q): when a ruling is outstanding and a landing is ready, yield at a PR
   boundary, **never between W1 and W2**. It governs a landing already in progress; today it
   permits nothing but this file's PR (step 3).

## 2. The mains (`git ls-remote`, 27 Sep 2026 16:41 UTC)

| repo | main | what it is | colour |
|---|---|---|---|
| Lessons | `372debcd459630af365e1234930b569314951264` | #680, pure carrier closing DLG-1 (26 Sep) | green: publication 36240684994; Watch main 36319771060 and cross-estate 36319191285 success |
| Site | `e050aba40f4adaeb741ed66b994516bd7408404a` | #452, MKT1 M3 mailing (27 Sep) | green: publication 36305687128, Domain split 36305687129, completion 36306231879, live verification 36306231907, mailing live check 36306231877; its two reds re-run once each (authorised), green on attempt 2 (§10) |
| Apps | `6415a2968f9f5c435ce8584474d0d5cdf73654d0` | #190, gate copy for the DLG-1 carrier (26 Sep) | green: publication 36240048643 |
| Games | `909c29c24e876f2990f05ed2b4a00fe43fc0bb74` | #99 (17 Sep), untouched | red: scheduled Pin release (§10) |
| Games- | `803e3bcafa02a6fc283a685c759488528913fdbb` | README (16 Jul), untouched | no workflows |

Pins that tie them (unchanged since 26 Sep):
- **Carriers:** Lessons `education-pages.yml` `uses:`/`builder_ref` = Site `117d4cff` (#451), one
  behind Site main (#452 moved no pin file and no Lessons or Apps path; Lessons admission is
  identical at both, 5,949 paths). Apps = Site `08d74766` (#390, 16 Sep), unmoved since.
- **L33** (`_sx3/SX3_PASSES_LEDGER.md:505`, standing): a carrier bump belongs on the first Lessons
  PR after a Site merge. This file's PR carries none: it changes only this file (HANDOFF-RULE),
  as #665 did after Site #439 with a green publication. The landing's own route (W1, then the
  Lessons content PR with its carrier last) moves the pin past e050aba4.
- **Site EQUAL set:** five lines in three files (`domain-split-verify.yml:167/236`,
  `education-publication.yml:150/221`, `published-completion-verify.yml:38`), all on Lessons
  `5c9e02a8` (#679) and Apps `9dc25231` (#189).
- **Gate copies:** `tools/verify_cross_estate_unification.py` byte-identical on both mains (sha256
  `e980a2e48ffea0e28985c59364f65bcfdf210c9af55e1811ad79b51954382522`); pin check PASS.
- **Designated branch** `claude/rs1-g3-science-hub-hszvpj`: tree-identical to main in Lessons (head
  742f1ca3 before this file's PR), Site (db31aa80) and Apps (3b785441); last PRs #680, #452, #190.

## 3. All five repos are public

GitHub API, 27 Sep 2026: Lessons, mattroper1977.github.io, Matt-s-Apps-, Games and Games- all
report `visibility: public`, so this file is world-readable on github.com even though
madebymatt.uk never serves it. Consequences (HANDOFF-PLAN-CONDITION, SCOPE-SCHOOL-SYSTEM-NAMES):
- No ruling text is committed; nothing goes under `_sx3/rulings/`. The texts are in one ZIP that
  Matt holds (§8). No repo text names a school system or school product (write "school-system
  names" or "the leak list"), the school's internal arrangements, how the site owner works or what
  he does or does not have; no email address, key, token, internal hostname, credential or pupil
  data. STOP reports stay private.
- `_sx3/` is not served: the Site publisher's `public_file()` refuses any path segment starting `_`
  (five named exceptions, none in `_sx3`); admission holds 0 `_sx3` paths at 117d4cff and e050aba4;
  live `/Lessons/_sx3/*` is 404. Every handoff PR shows a red proof of this before merge, in its PR
  body: import `public_file` and `REVIEWED_ARCHIVE_DOCUMENTS` from Site
  `domain-split/build_education.py` at the Lessons carrier pin; every `_sx3/` path must be refused,
  and no `_sx3` path may be in that list or in `education-publication-admission.json`
  (`education-lessons`), with a served control; it must go red when `_sx3/HANDOFF_CURRENT.md` is
  planted in each of the three; then fetch the live `/Lessons/_sx3/HANDOFF_CURRENT.md` (404).
- Pre-existing, unfixed: public Lessons main names school systems in 277 files: 103 served text
  files and 2 served workbooks (the sweep, §5), and 172 unserved (D52; more if D51 goes the other
  way). Site: one served line (the sweep) and one unserved file (D50, D52).

## 4. Landed since the 23 Sep recovery (first-parent after Lessons e763a398, Site 5251edc, Apps afbd0ad; every publication succeeded)

| # | item | PRs in merge order (short SHA) |
|---|---|---|
| 1 | recovery docs | Site #439 ccec5b7 · Lessons #665 63885d63 · Site #441 bc7cd71 · Lessons #669 c2169dcb |
| 2 | D3 (verify_loop row 48) | Apps #179 f325471 → Lessons #666 3da87a8b |
| 3 | HUB1 v2, #655 chain | Site #440 7d310e1 → Apps #180 2fd5621 → Lessons #667 6d5a05ad → Site W2 #442 9fd80be → Apps #183 8002b50 → Lessons carrier #672 f06e83a7; closed by Site #443 d9cdcee (HUB1_READBACK) |
| 4 | LW-4 §1 (staff files beside lessons, unserved) | Apps #181 91358f2 → Lessons #670 1213ece9 |
| 5 | Q12 Science hub stylesheet, #655 chain | Site #444 3e5e489 → Apps #184 045088e → Lessons #673 7aed39b3 → Site W2 #445 be9441d → Apps #185 29710ca → Lessons carrier #674 645aa4bb |
| 6 | completion pin b54c9006 → 7aed39b3, declared EQUAL | Site #446 cc28d5c (old known red cleared) |
| 7 | Correction #41: EQUAL set is five lines in three files (docs) | Lessons #676 afb2244a |
| 8 | Job 11 (LW-4 §1 addendum 2) | Apps #182 6952699 → Lessons #671 55eb2bd1 |
| 9 | LAND-A2 Science (21 Autumn 2 lessons), #655 chain | Site #448 214749c → Apps #187 1ad001c → Lessons #677 c0b9b51f → Site W2 #449 079fba9 → Apps #188 a67b30e → Lessons carrier #678 c527b7c1 |
| 10 | DLG-1 (173 pages), #655 chain | Site #450 de2ed59 → Apps #189 9dc2523 → Lessons #679 5c9e02a8 → Site W2 #451 117d4cf → Apps #190 6415a29 → Lessons carrier #680 372debcd |
| 11 | MKT1 PR1 / M3 (Site only) | Site #452 e050aba |

## 5. Queue, in order

| # | item | route and preconditions | DONE report |
|---|---|---|---|
| 1 | **LAND-SCI-56 v2**: 21 Autumn 2 P1/L1 replaced in place, 28 new P2/L2/L3, 7 return-week lessons in 3 new A1_W08 folders; records under `_land_a2/SC3R_2026-09-27/` | STOP now; ruled in full (§6). Supplier round SC3R4 (Claude orders it; GPT Fri 9 Oct, Mon 12 Oct latest) → Claude's check and hashes → re-delivery checked by hash → prep re-run with the step-3 tools → BASE (Lessons main still 372debcd, else diff the estate files the records name against 372debcd; STOP on change; after this file's merge expect 0 changed) → W1 → Apps gate copy → Lessons content PR (carrier last) → Site W2 EQUAL → Apps companion → pure carrier | LAND_SCI56_DONE: three main SHAs before/after; served files per folder; parity; guards; browser proof; hub rows with heads unchanged; M3 unchanged; each publication with its mailing live-check run. Then a handoff PR |
| 2 | **Mailing PR** (Site): repo copy of the subscribe function + live-check changes + the verify_jwt gate fix, in one PR | After LAND_SCI56_DONE, in the ruled deploy-and-test order at merge (2026-09-27_MKT1-PART2-APPROVED.txt, C1–C5 in 2026-09-27_MKT1-PART2-V2-APPROVED.txt). Branch rebuilt as in §8. Any STOP condition: no merge, no retry | none of its own (feeds MKT1_DONE) |
| 3 | **LAND-RE-24** (24 RE lessons + RB4 as a 25th item; all sources verified; RB4's page takes the DLG-1 fix) | After item 2 (D53). A proposal to land it before LAND-SCI-56, while Science waits on the supplier, was put to Claude on 27 Sep; unanswered at writing | LAND_RE24_DONE, then a handoff PR |
| 4 | **The SWEEP** (school-system names out of the rest of the served set: one Lessons PR with 103 text files, 2 workbook cells, the served .md files (D49b), the D9 theme item on the served subset and R10's 9 lessons to the standing wording; one Site PR with 1 line; one red guard over the whole served set that matches digests, not names (D47, D50)) | After item 3 (D53); other leak-list terms are measured and reported before anything changes on them. When its PR opens, close drafts #675, #447, #186 with a one-line comment naming it (never merge or rebase). Then the unserved files in a docs-only PR under the hashed guard (D52) | not named yet |
| 5 | **HUM v12 / HR1** (Humanities Autumn 2 lands once) | After item 4, by #655; waits on the supplier's v12 delivery (not received). If that delivery is accepted before the sweep PR is open, HUM v12 goes ahead of the sweep (D53) | LAND_HUM_DONE, then a handoff PR |
| 6 | **MKT1 PR2 (M4)** → **PR4 (M1)** → **PR3 (M2)** → **MKT1 Lessons arm** (#655) | After item 5 (D53); each after the previous publication; not inside a window | MKT1_DONE, then a handoff PR |

**Ruled but unscheduled** (no slot; ask before starting any):
- RS1-G4 §4 Q11 (W11A/W11B binding; "Your task · 1 of 2") and §6 record-only reports (§3, the C
  trio, is superseded by the sweep). R8 §2 GLV3 structural-gap PR (whether it precedes RE-24 is
  unruled). R10 POLISH concurrency PR. R12 follow-ups (browser-matrix cascade; one game's home
  control at 1440 px). B9. LAND-SP1 (Science start page). OFFLINE-A2 (parked).
  The 52-page off-origin fonts/thumbnails job (MKT1-Q Q11), after RE and HUM v12.
- MKT1-A item 10 (start-page rows 11/12) and the Humanities start page (LAND-A2 L3, R7 start page
  v2) were to ride with the RE E4 and LAND-SP1 start-page landings. LAND-RE-24 replaced E4 and
  names neither, so where they land now is unruled: ask.
- Correction #41 (2026-09-25_RS1-G4-S1-NOTE.txt): `_sx3/SX3_PASSES_LEDGER.md` still lacks it; it
  goes in the next PR that legitimately touches that file (never a handoff PR).
- From the 23 Sep file, never re-scheduled: W9L1 fix → PASS C batch 2 → item 4 (HUM-T P1 re-cut) →
  serve-witness floating (Q7) → LW-1 R2/R3; the S06 entry; the line-1703 flag in
  `_sx3/SX3_PASSES_LEDGER.md`; the #668 donor; Held A (`_sx3/STOP_G2_build_w9_w14_generations.md`;
  `_sx3/HELD.md:63`) and Held B (`_sx3/STOP_S3_stage_contract.md`; `_sx3/HELD.md:70`)
  re-authoring. Branches `claude/lw4-find-out-more` and `claude/sci-b1` hold unmerged commits with
  no PR (status unruled).

## 6. Rulings

Texts: `RULINGS_2026-09-27.zip` (§8). The table below cites 39 of its 50 files; the other 11 are
closed or superseded. `RULINGS_INDEX.md` in the ZIP is the full list, with each status. Older
rulings in force: the 23 Sep file (c2169dcb) and its records.

| id | date | governs | file in RULINGS_2026-09-27.zip | status / open work |
|---|---|---|---|---|
| LAND-SCI-56-v2 (+ LAND-SCI-BF, -R2, superseded but cited for AT LANDING 1's authorised changes) | 26–27 Sep | the current landing; §9 no canonical = self-canonical; §10 M3 files unchanged | 2026-09-27_LAND-SCI-56-v2.txt, 2026-09-26_LAND-SCI-BF.txt, 2026-09-26_LAND-SCI-BF-R2.txt | OPEN: STOP before W1 |
| MKT1 Part 2 (V2-APPROVED governs the hashes and C1–C5; APPROVED the order at merge; TWO-ANSWERS part-standing; RECOVERY-NOTED the §8 route) | 27 Sep | the mailing PR | 2026-09-27_MKT1-PART2-V2-APPROVED.txt, 2026-09-27_MKT1-PART2-APPROVED.txt, 2026-09-27_MKT1-PART2-TWO-ANSWERS.txt, 2026-09-27_MKT1-PART2-RECOVERY-NOTED.txt | OPEN (queue item 2) |
| MKT1-Q | 27 Sep | PR2/PR4/PR3/Lessons arm; queue; yield rule; Q11 fonts job | 2026-09-27_MKT1-Q-Q1-Q15.txt | OPEN |
| MKT1 order, MKT1-A, M2 code | 26 Sep | M1–M4 content; PR2 items 7–9, 11–12; item 10 at start pages | 2026-09-26_MKT1-ORDER.txt, 2026-09-26_MKT1-A-RULING.txt, 2026-09-26_MKT1-GOATCOUNTER-CODE.txt | OPEN (queue position superseded by MKT1-Q) |
| LAND-RE-24 + A1 | 27 Sep | RE lands once; RB4 as 25th item; base check | 2026-09-27_LAND-RE-24-ORDER.txt, 2026-09-27_LAND-RE-24-A1-AND-PRE-STOP.txt, 2026-09-27_LAND-RE-24-A1-SOURCE-CONFIRMED.txt, 2026-09-27_RB4-BASE-STOP.txt | OPEN (queue item 3) |
| PRE-STOP 1, 2, 4, 5 | 27 Sep | names vs values; replacement wording; C trio superseded; the W8B dated line | 2026-09-27_LAND-RE-24-A1-AND-PRE-STOP.txt | 1, 2, 5 STANDING; 3 CLOSED (re-runs done; its Maker splash line still applies, §10); 4 OPEN (close #675/#447/#186 when the sweep PR opens) |
| READING-AGE | 27 Sep | text levels exempt; refined value check; served .md on the sweep list | 2026-09-27_READING-AGE.txt | STANDING |
| SCOPE-SCHOOL-SYSTEM-NAMES | 27 Sep | estate-wide rule; two jobs; unserved files unchanged; `_sx3` records left; reviewer read | 2026-09-27_SCOPE-SCHOOL-SYSTEM-NAMES.txt | OPEN (sweep) |
| HANDOFF-RULE, HANDOFF-PLAN-CONDITION | 27 Sep | this file | 2026-09-27_HANDOFF-RULE.txt, 2026-09-27_HANDOFF-PLAN-CONDITION.txt | STANDING |
| HUM v12 set | 26–27 Sep | Humanities once as v12, S1–S18; H1–H46 and landing points; R9 superseded (whether its checks carry to v12: ask) | 2026-09-26_R11-HUM-A2-V11-STOP.txt, 2026-09-27_HUM-H.txt, 2026-09-26_LAND-A2-R9-HUMANITIES-GO.txt | OPEN (queue item 5) |
| RE route | 25–26 Sep | RB-1..RB-4, REC-1; P1/P2; scope, records, start page v2 | 2026-09-26_R7b-RE-E3-STOP-QUEUE.txt, 2026-09-26_RE-BRIEF-ACCEPTED.txt, 2026-09-25_LAND-A2-R7-RE.txt | OPEN (part-superseded) |
| R8 DLG-1 | 26 Sep | §1 W8B expiry; §2 GLV3 gap PR; §3 exceptions shrink-only; hub pills | 2026-09-26_LAND-A2-R8-DLG1.txt | OPEN (§7) |
| R10, R12, SP1 | 26 Sep | POLISH concurrency PR; two follow-ups; B9 | 2026-09-26_LAND-A2-R10.txt, 2026-09-26_DLG1-R12-MAILING.txt, 2026-09-26_SP1-BRIEF-REVIEWED.txt | OPEN, unscheduled (§5) |
| LAND-A2 standing set | 25–26 Sep | L1–L4; served-set rules; nothing worse live (H0–H3); records never served; do not change the publisher; supplier QA; any red = STOP | 2026-09-25_LAND-A2.txt, 2026-09-25_LAND-A2-R1-L2.txt, 2026-09-25_LAND-A2-R2.txt, 2026-09-25_LAND-A2-L2-NOTE.txt, 2026-09-25_LAND-A2-R4-SCIENCE.txt, 2026-09-25_LAND-A2-R5-HUMANITIES.txt, 2026-09-25_LAND-A2-R6.txt, 2026-09-26_DLG1-PROCEED-ACK.txt | STANDING (R6 item 8 carries to v12) |
| RS1-G4, S1-NOTE (RS1-G2 §6–§8, which they cite, exists in no file) | 25 Sep | §4 Q11; §6 reports; Correction #41 | 2026-09-25_RS1-G4.txt, 2026-09-25_RS1-G4-S1-NOTE.txt | OPEN: RS1_G4_DONE never reported; ask Claude to restate RS1-G2 §7 or confirm RS1-G4 §4 is complete |

**STOP-SCI-56 is ruled** (27 Sep). Files, all in `RESEND_STOP_SCI56_FOR_CODE_2026-09-27.zip`
(§8), held by Matt: `RULING_STOP_SCI56_2026-09-27.md` (the answers D1–D53 by tier and "What SC3R4
changes for your prep"), `RULING_SCI_GUIDANCE_SG_2026-09-27.md` (SG1–SG15) and
`ORDER_SC3R4_2026-09-27.md` (what GPT was asked: A1–A18 and B1–B15, for the parity and claims
checks only). A later note from Claude (D40 addendum) sets the fit proof's platform.

**What the ruling sets, in short** (read the file; this is only a map):
- **Supplier round SC3R4:** all 24 ZIPs re-cut; nothing from SC3R3 is reused. Landing fixers are
  pre-authorised only as named fallbacks (D3, D8c, D9, D38, all in the RB-2 / R11 S14 shape); D39
  has none (DONE states the splits).
- **Parity (point 1):** the P1s differ from live by the ordered edits (S1–S10 as ruled) and by the
  SG changes; each is a ruled difference, and the OTHER list must hold nothing outside S1–S10 and
  SG1–SG15. Claude sends per-page counts of the re-delivery; the claims script re-proves them.
- **The hardened guard (point 5):** it judges what a person can read (visible text, alt,
  aria-label, title, placeholder, meta content, Office descriptions, theme and layout names,
  caption text) and reports markup names with counts (D14); the reassurance line is accepted only
  with a button that exists on that page (D10); dates by three pinned kinds (D17); the tier names
  the SG ruling sets (D6); four SG limbs; value checks as ruled (D51); names matched as digests,
  never spelled, with the red proof reading its plants from a file outside the repo (D50).
- **Browser proof:** fit sizes gain 1536x864; the proof counts only on a Windows runner with Chrome
  and Segoe UI (a manual-start workflow, committed only once the hardened guard is green, adding
  no name list); pass is 0 px internal scroll at every fit size, with any failing slide listed for
  a ruling; DONE names font, platform and Chrome version (D40). The progress-pill rule is part of
  the hit-test (D37).
- **Tools and route:** the hub binder committed as a tool with its static pin and red proof (D27);
  unit-tag override (D24); "added" = the actual landing date (D25); the Science GLV3 limb, with
  `admit_transaction.py --check` verifying the declaration (D29); PDFs marked binary in
  `.gitattributes` on exact paths only, never globs, with a red proof (D30); Site publication
  timeout 25 minutes in the W1 PR (D33); `base_independent.py` gates BASE, any change to the 214
  is a STOP (D44).
- **Later landings:** the sweep's shape and wording (D47, D48 rows 1–6 all ruled), served .md
  (D49), unserved files (D52), queue (D53, §5). The RE sources count is settled (D46).

## 7. Dated items

**14 Oct: check the W8B exception; it expires 16 Oct.**

If W8B's fallback limb is not on Lessons main by then, STOP and send Claude a W8B release-ruling
request **that day, 14 Oct**, not on the 16th (R8 §1, D20; `tools/hum/dialog_audience_exceptions.json`). From 16 Oct the dialog check fails on SCI_B_W8B.
No queued item lands that limb: not LAND-SCI-56 (D29's GLV3 limb is a different limb) and not the
R8 §2 GLV3 gap PR. So expect the 14 Oct check to need the release ruling. The old reminder routine
is bound to the old session and will not reach a new one: whichever session picks this up sets
its own 14 Oct reminder, with the user's approval.

Critical path (STOP report §1, as ruled): Claude issues the SC3R4 order → GPT re-delivery **Fri 9
Oct, Mon 12 Oct at the latest** → Claude's check and hashes → about one working day to check it
and re-run the prep (a new container first rebuilds the prep tools, §8) → about two for W1 to
close-out → **LAND_SCI56_DONE by Wed 14 Oct** → exception lapses Fri 16 Oct → hard deadline Mon 19
Oct (LAND-RE-24 has the same deadline). Carrier merges avoid the daily schedules 06:47–07:31 UTC.

## 8. Held outside the repos, and how to recover each

| item | held by | sha256 | recover by |
|---|---|---|---|
| `RULINGS_2026-09-27.zip` (50 verbatim rulings, `RULINGS_INDEX.md`, `SHA256SUMS`) | Matt | `b31d8515ff2c6d67e06b39447f38637a0fafac49656a95d0b1164f097958f48c` | ask Matt; cite, never commit |
| `STOP_REPORT_LAND_SCI56.md` | Matt, Claude | `0095b077f2ade520f0508a70dd34aa3e4c15bc974a6e64f2f2ea3bdef3bd15f2` | ask Matt |
| `RESEND_STOP_SCI56_FOR_CODE_2026-09-27.zip` (the full STOP-SCI-56 ruling, the SG ruling, the SC3R4 order for reference, `SHA256SUMS`) | Matt, Claude | `a034ca333be844dc6387ffaa5ec94b75600e62f176f410cdf0f2888ca98f9b1c` | ask Matt; cite, never commit |
| `LAND_SCI56_STOP_EVIDENCE_2026-09-27.zip` (93 files, 128 entries with folders: prep outputs, plans, parity verifiers, hub tool patch, GLV3 limb draft, W1 admission draft, value check) | Matt, Claude | `a3165514998e4dd5b77132112571d3ea70605ef372d74746a3acda2d80099615` | ask Matt. The placement, guard, browser-proof and route tools and the staged Lessons tree are container-only (not in this ZIP): rebuild them from the report's §3–§4 and this ZIP. Size it at roughly the first prep again (about five hours on 27 Sep, which included writing them), on top of the step-3 day in §7 |
| Mailing PR branch: 7 commits on Site `e050aba4`, local to the writing container, never pushed | Matt, Claude (both files) | `MKT1_PART2_AB_v2.patch` `0a1cdf2d2fb1f3be4ca2a42080998cbae980102590ab5551e674f9c5631ccd2c`; `subscribe-mailing-list.index.ts` `16779734a67f0c3d61c80184eef1f983a675b2a3b86d7dcb2598400528ec0acc` (VERSION 472733a4f770); `MKT1_PART2_READBACK_v2.md` `b51ad4d7a1a78e87606fe2552226019efaf64706bebcb7d511029a75dd6c32ff` | `git am MKT1_PART2_AB_v2.patch` on a branch from e050aba4; the function file must equal the patched one (the HTTP harness is inside the patch). At its turn (after LAND_SCI56_DONE), rebase onto current Site main and check the function file's sha256 again; any conflict or hash change: STOP. Push it as the designated branch or one extra `claude/` branch for this PR (§9.1) |
| RB4: `RB4_LAUNCH_A1_W07.zip`; base `RB4_SOURCE_LAUNCH_A1_W07.zip`; landed page after the DLG-1 fixer | Matt | `b2cc9173adbcde8e804a1d2a43da58a39c524d10eccf10a51cae32a37c357c08`; `1eda173b918d5abe6b8d1389fb4123c00293b5d19b967ffaa9173cf7016aeb15`; page `c11e704da779d803b57e7d952e1d8c4c4b1a1da9d619e4afdae1cfdfcf16f9dc` | ask Matt; re-apply the ruled DLG-1 fixer and check the page hash |
| Briefs already delivered: `LIVE_PARITY_RE_A2.md`, `LIVE_PARITY_RE_A2_BUILD_W01.md`, `RE_A2_LIVE_PARITY_SOURCES.zip`; `LIVE_PARITY_HUM_A2.md`, `HUM_A2_LIVE_PARITY_SOURCES_2026-09-27.zip`, `HUM_A2_D0.md`; `LIVE_PARITY_SP1.md`, `HUM_SP1_LIVE_PARITY_SOURCES.zip`; `MKT1_PLAN_AND_QUESTIONS.md` | Matt | `46c2e2295cc4d286a45edb1041ebe2e1253ae3f180d4707f4ddbd8c24aef2059`, `1fcbc526564f44ba2e413f52be6cd736dbab216fa49d130ffb68951b0edfd63b`, `83952d664b18e803bb6ec7b1c147b89af048487387d503dbf85ceeb58f7c9304`; `a92a159275a9dcf66b1d07488f125e31411b4817b96bf388f11df3b62ec7f8be`, `a7307d9eac2273dc103654f36c9b910be64e489409d8e08dc2554af4caae2279`, `64215607202a387e4cb3dfc339ed1d1d3d35f7690c17417983d66f078025d0fb`; `93993d43cf80c9c66861f7554965f3001572ee3d9e66a08fc49e99089f52af5c`, `670c425d83df082fcd74ce340b74261887423daf7336a86823ca349a37b8b700`; `0ade65b2c9dd7a02b96f766d38bd3e4aa932addefd9b4f901889e45962d9663c` | ask Matt |
| Container-only, no copy: `V12_LANDING_CHECKS.md` (internal HUM v12 checks); the MKT1 map and M1/M2/M4 prototypes; the brief assemblers | nobody | `V12_LANDING_CHECKS.md` `1f5dc5660544f8a4d061cfeceef1132fc39b48fd5f96132a895d5f13d2740466` | rebuild: the v12 landing points are in 2026-09-27_HUM-H.txt; MKT1 from the plan above and the rulings |

**The 24-week sources**, all held by Matt: Science `<prefix>_<week>.zip` (LAND-SCI-56 order) and RE
`RB3_<week>.zip` (LAND-RE-24 order; extract each into its own folder) with the RE companion
`SHA256SUMS` (`c4d055bfe1f0c2dab0cce4219a20cc5c2c0908255c1742327fd085ea973d5b1c`). Ignore a
truncated second upload of SC3R3_LAUNCH_A2_W02 (228,636 B, not a valid zip).

| week | Science prefix | Science sha256 | RE (RB3) sha256 |
|---|---|---|---|
| BUILD_A1_W08 | SC3R2 | `f1e8813bf5e2eb8638c0cad01eb05c9a90233b6206001b9afc9b24bab97ac9ee` | `ced6ecb5cef6079298e93ec3e4bbbf2c4ebe403088c5d954bdc7b9c2762d25ec` |
| BUILD_A2_W01 | SC3R2 | `717ebb1fd637090f44536553d7b968eb1efce2ea37499c8843d185726f771f11` | `a072fd0cbe5017974439b91ea8c985bc8ab160f465c962d0f518eb95119f3afb` |
| BUILD_A2_W02 | SC3R2 | `f4df4df9a319e8d4a49638050d13456e69cdf406bae70600a18171de86e8f812` | `01f36d7ef6d4dc88f13d4ee4d1b070194b0aa743da86eed2e895af2e38c63fb2` |
| BUILD_A2_W03 | SC3R2 | `09f6ac426b729e3930167b77b295e2e1e780e53b77a43095f8e224ebf4626830` | `9547943d280b9cade642255f18840257a9d6888f9a256bf6001491d5d47261f4` |
| BUILD_A2_W04 | SC3R2 | `b7a614c0d6a36843e3bd4691e593948c8bf2a6c09759613f0aef48379fd92bfe` | `3224149e84415e5f60e9fa7213a3cdbd40f6b9c404e2bebccc44ff89dcd18b3e` |
| BUILD_A2_W05 | SC3R2 | `977fd8561badbf1196f73513ca90119ccb66ab90deb05d65b919872b5630232e` | `07c759db926f91bb373504f84e845f84a0108261e9e1eabce36191fa0ca33f5f` |
| BUILD_A2_W06 | SC3R2 | `07240fcee5e65221b0a90f59cc4f445aeda1f2acb3df1246cb343fc7d3d495a1` | `16e2c02b56452f4a20de61b52abc29958f803d04ef64bf9ee20f0d4c049e9faf` |
| BUILD_A2_W07 | SC3R2 | `c2c729e4028f548c69be5521d88f69da62e8042d3e69746a3d1c6d8637b13414` | `90f749ffccd4aace302a9c533030a1d641e96d0e138c40ffb9fb03242cd8564f` |
| GROW_A1_W08 | SC3R3 | `4470bb7feef45f975cae900fbbd8a6da53c637cc90a09d6131d5b17dc1e606c1` | `9fd9da87890d3a4bf8537bd84580164033beb7980136f17d4361c66d3d958f74` |
| GROW_A2_W01 | SC3R2 | `a68a7ec2b188b61d9bd57e63f7e7169a48b3684504fa925945130c9a754ee089` | `234ca9f385d15eac49984306829bcc61e3dd9ef5dae0767686a482f0a9dbf64f` |
| GROW_A2_W02 | SC3R3 | `b804438dfffdd675a5052589c328ada46d0ddad56bf214700ce24ae64b30516a` | `f3e4b1c25c305cb0a80406e00dbf14a69e1ab9c2bc1efefac9d1124737c4b00c` |
| GROW_A2_W03 | SC3R3 | `d4a4ab84c4b0b6106e2f4f5e121f3d8a3de7c1221445dac38eaba6da269f4c57` | `efa452341c57aa2af67e8778649c74e23c3a6285939a7e24b2edd38e15251cf5` |
| GROW_A2_W04 | SC3R3 | `8e5f2f56da8187d193acfae8c31579f5b3c08e5c11cabf976c8333aa8d9a5313` | `9dd2f59f15dc96b2ab47eda1b52871599efa5561ddfdbc969b1321eb349bd5f2` |
| GROW_A2_W05 | SC3R3 | `ad08e1bb8a6dc397d2f2f956191d40f0ddde601dcad70e5e1ca5571ad57a08b1` | `253ebbb38f43b4b68970cb928b45c28cd0cf41b06d43401d4576834a10386561` |
| GROW_A2_W06 | SC3R3 | `d307178b505d6d11290586750942e444ea7cd4c78cd01f2537c9387f71663e14` | `fba84c72c38dc336da1da40a02ff973bddf4df14290b74d589787b68355c39a2` |
| GROW_A2_W07 | SC3R3 | `844ec641446bf107d8c7a978fab27cfc8ce9e0a2e4f9baeb97b09e7663b42e42` | `6c5f330c2cbdfe93329c2be8c894a1aa52588aff8388527d79d1dc17c388b666` |
| LAUNCH_A1_W08 | SC3R3 | `b8ed9b2eb109a531e5765eb46e85e776c6ba4dde492d22db5a46b98d672220b4` | `14b238f6eb39cbc771829334ffa115918f7418430639bd31fbe3626b7a15ed07` |
| LAUNCH_A2_W01 | SC3R3 | `191b38df6945a8e20286e91fe483871bbd7169f7db4f74101cb17ed8e9adec68` | `9e53b01e10a6e4bf0483ebf41c9d2744e460738812f5f44f2d4cc520c8033c31` |
| LAUNCH_A2_W02 | SC3R3 | `a0cf52e341aa0a13238c94a0848e67d1d19194fde4a27e2be23545e93b43e689` | `4603ad1afb118ac8e4ce3a1cb177a9f0679c085be5313859ca24de0a19e53934` |
| LAUNCH_A2_W03 | SC3R3 | `bf288d4193ae7f51c3018f135f6c5621722737b8464d7ff197cb377712395346` | `a3b5880a80f1493b73860476c2216dd1c60f05b1a567b42a202bc64fb6958b2c` |
| LAUNCH_A2_W04 | SC3R3 | `e50d45bccd0c2fd189f928dc80a957b48aaea83da5aeee2174e99630fd989d2b` | `c87765c4e1a03bfa957d5467ed62771312bea84d5735618015d5ef3fade386e0` |
| LAUNCH_A2_W05 | SC3R3 | `620769159c1904a8946c9e96d02258f224baccb97be72bf28d51e09a621eaad3` | `8a510cb01295126e62ac58921301a3b814a607328cbcfcfaa5212342d8309b61` |
| LAUNCH_A2_W06 | SC3R3 | `c3b56ae30565071a8ddedf1775fa2ba69f49d736959d74faabc0d02705d180b9` | `a2c64b9a1326324eb7cb27e08f2c5d9cabd560b9b277d8b8584dad3569365e30` |
| LAUNCH_A2_W07 | SC3R3 | `4fdbbf107bcda90fcf18b691aba785e39271f7edd82495bdec34b0dd0f177ad7` | `eced0bdbd571e98cbcdfbabdf44adcdbe99682d7ea141eca9c99c763c09dfd06` |

## 9. Standing rules for whoever picks this up

1. **Identity and branch.** Every repo is under the GitHub owner MattRoper1977. Work on
   `claude/rs1-g3-science-hub-hszvpj` in Lessons, Site and Apps (one extra `claude/` branch per PR
   allowed). Restart a merged `claude/` branch from `origin/main` with `--force-with-lease` against
   its recorded head (now Lessons 742f1ca3, Site db31aa80, Apps 3b785441; this file's PR head
   replaces Lessons'). Never force-push `main`.
2. **One step at a time.** One landing window at a time; each step only after the previous
   publication succeeds, read by run id. `git ls-remote` main before every merge (never the PR's
   cached base); merge only what a relayed ruling authorises, and only when green. Route #655:
   Site W1 → Apps → Lessons (carrier last) → Site W2 (the five EQUAL lines) → Apps pure carrier →
   Lessons pure carrier.
3. **STOP.** Anything not ruled: STOP and report before building further; STOP reports go to Claude
   through Matt, never into a repo. Any red after a merge: STOP; re-run only when a ruling says so.
4. **Commits and PRs.** End each commit with the Co-Authored-By and Claude-Session trailers from the
   session's attribution instructions, and each PR body with the Claude Code footer and session
   link. No model identifier anywhere else in a pushed file.
5. **Supplier QA** is never committed (LAND-A2 R4 Q2; RB4's check file) unless an order names it a
   record (LAND-SCI-56 point 3), and a supplier's QA script is never the pass test.
6. **Live parity first**: diff against live before replacing any served file; an unauthorised loss
   is a STOP. Records never served; `LESSON_SOURCE.json` never served (it may sit in the repo, as
   under `_land_a2/`, but never in the published set); do not change the publisher.
7. **GPT lane.** New science lesson content, computing and cyber-safety lessons and assemblies, and
   security-weakness work go to GPT, held by name as "GPT work"; Code lands and measures.
   Exception: the mailing PR (LAND-SCI-56 v2 Part 2 A/B) is Code's by ruling.
8. **Guards** each carry a red proof. No canonical = self-canonical. No landing changes M3's five
   files or `features.mailing`. After each Lessons or Apps publication, dispatch Site
   `mailing-functions-live.yml` (workflow_dispatch) and report its run id; after a Lessons
   publication also dispatch `published-completion-verify.yml`, as R12 §3 did. After a Site
   publication both run by themselves.
9. **Held by name**, never forced: `_sx3/HELD.md`, `_sci/HELD.md`, `_hum/HELD.md`,
   `_sx3/RELEASE_LEDGER.md:1312`.
10. **The handoff PR** changes only this file, never a pinned file (`_sci/HELD.md`,
    `_sx3/RELEASE_LEDGER.md`, `_sci/WEEK_TOKEN_DISAGREEMENTS.md`, `_sx3/SX3_PASSES_LEDGER.md`,
    `_sx3/FENCE.json`, `_sx3/CHASSIS_CONTRACT.md`). Only FieldOps runs on the PR (9 jobs). On the
    main push: Education Pages publication and FieldOps, then Science teaching packs and Watch main
    (workflow_run); all must be green (the 23 Sep file said the publication did not run). The
    unification and cross-estate-on-content workflows are path-skipped on both. The unification
    gate reds only on a PR diff that modifies this file, so never put it in a PR that triggers that
    gate; its scheduled run on main stays green with the change in history (#669 changed this file;
    36319191285 on 372debcd is green). Then dispatch the Site checks (rule 8). Reviewer read before
    merge: no school-system names, nothing on how the site owner works or what he does or does not
    have, the `_sx3` red proof (§3).
11. **No keys**: no key, token or credential in chat or any repo; publish no new address.

## 10. Known reds and watch items

- **Games "Pin release" (known red, untouched, parked by RS1-G4 §6):** every scheduled run fails
  (runs 69–86 all failed; latest completed 86 = 36318030603, 27 Sep); its PRs #100 (lessons →
  372debcd) and #102 (site → e050aba4) are green on their 27 Sep heads.
- **Lessons Watch main soak:** green since 26 Sep 12:50Z; soak 3/10 at the 27 Sep 12:11Z run
  (36318150977; §2 cites the later 12:40Z run, also green); its write leg is still a dry run. The
  four reds of 26 Sep 12:12–12:14Z were one re-run flake.
- **Site "Verify audience discovery" INCONCLUSIVE pattern:** it fails when its wait runs out while
  the Education publication is still running (079fba99 36198691321; e050aba4 36305687136, green on
  the authorised attempt 2). A timing item, not a site fault, but a re-run still needs a ruling.
- **Site "Maker splash" /auroralinks/:** red once on e050aba4 (36306232053: 41.5 ms at 390×844,
  under the 280 ms minimum), green on attempt 2. If it reds there again while live visits show
  1.6–2.2 s, log it as a harness timing item for later, not a site fault (PRE-STOP 3; its re-runs
  are closed, this line stands).
- **Open PRs:** the C trio (Lessons #675, Site #447, Apps #186) waits for the sweep PR; Lessons #668
  (GPT job specs) waits on its donor; the older PRs in the 23 Sep file are unchanged.
