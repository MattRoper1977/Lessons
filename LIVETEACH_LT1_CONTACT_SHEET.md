# LT1 Contact Sheet — pupil-name remediation (for Matt's post-hoc veto)

Order LT-GO, decision D3. Every change below replaced a first name with a
neutral placeholder; no logic, counts, grades, or behaviour changed (29 lines
swapped for 29 lines across 23 files). Real names are redacted as `[name]`
throughout this sheet and appear nowhere in the diff except as the removed text.
To veto any item, quote its number — `git revert` restores it cleanly.

## A · Replaced (23 files)

| # | File(s) | Line | Before → After |
|---|---|---|---|
| A1 | `6 Art/` — Lesson3, Lesson4, Lesson5, Lesson6, Lesson7, Lesson8, Lesson10 ×2, Lesson12, Lesson13, Lesson14, Lesson15 (12 files) | `_ccDefault` block in each | 12 × `{n:'[name]',g:'…'}` → `Pupil A`–`Pupil L`, **grades kept in place** |
| A2 | `5_6 Local Choice/Rivers/` L1a:1547, L1b:1122, L1c:1653, L1d:1382 | `ccPupils` | 9 × `"[name]"` → `Pupil A`–`Pupil I` |
| A3 | `5_6 Local Choice/Rivers/L1e_Final_Briefing.html:471` | `DEFAULT_ROSTER` | same 9 → `Pupil A`–`Pupil I` |
| A4 | `ASDAN/HW_Social_Media_Wellbeing_Active.html:573` | `DEFAULT_ROSTER` | same 9 → `Pupil A`–`Pupil I` (this file wrote these names into `ps_coldcall_roster` when empty — it now seeds neutrals) |
| A5 | `ASDAN/HW_Social_Media_Wellbeing_Active.html:578` | scenario text | `"[name] joins an online gaming group…"` → `"Ash joins…"` (the name coincided with a class member; the neighbouring scenarios already use fictional names) |
| A6 | `Games/` WorldCup_ThreeLions_Final:495, WorldCup_v3_MatchDirector:587, WorldCup_v5_Showdown:723 | `DEFAULT_ROSTER` | the 10-name class list → England squad surnames (Pickford, Walker, Stones, Rice, Bellingham, Foden, Saka, Kane, Sterling, Grealish). **Pedagogical cost:** the class no longer see themselves as the players; veto A6 if you'd rather re-personalise from a device-local list. |
| A7 | `build-engine/roster-setup.html:10–11` | two preset buttons | BUILD group (4) and full Year 10 (10) presets + button labels → `Pupil A…` style, mirroring your already-sanitised twin `Build/Resources/BUILD_Setup_ColdCall_Roster.html` |
| A8 | `ASDAN/ASDAN PEQs/Evidence_Binder_PEQ_v7.html:194` | placeholder | `"e.g. Witness statement: [name] led the group discussion…"` → `"…the learner led…"` (the name was a real class member's) |

## B · Judged and left, with reasons

| # | Where | Why left |
|---|---|---|
| B1 | `ASDAN/Consent_*` ×10 (filenames + content), `resources.json` rows, `5_6 Local Choice/index.html` rows, `REGISTER.md:836`, `_passpq/CLAIMS.md:26` | The estate has already adjudicated this name **fictional**: the files' own provenance header ("a fictional case-study character used for RSE consent teaching, not a real pupil. Safeguarding review has cleared these materials"), the REGISTER R-D03-family provenance note, and CLAIMS.md. The recon §8 claim that these embed a real pupil's name was **wrong** — corrected here. |
| B2 | The 12-name `6 Art` default list itself | Its first initials run perfectly A→L (a textbook demo-roster pattern), so it was probably synthetic — **replaced anyway** (A1) because in a small setting even a coincidence identifies; recorded so you know the judgement went both ways. |
| B3 | "…Under Pressure" medal names (`Opening_Night`, `The_Foxglove_Case`) | The idiom, not a pupil. |
| B4 | "Big [name]'s tower, 96 metres" (`Games/KidsVsStaff_Showdown`) | The London landmark. |
| B5 | Word problems in `BUILD_ASDAN/Careers/CAREERS_W4` ("[name] starts at 8:30…") | The name is from the synthetic A–L demo set, not the real class; standard fictional word-problem usage. |
| B6 | WAGOLL model answers (`BUILD_ASDAN/…/COMM_W3`, `Build/Slideshows/BUILD_DT_W2`) and the Repair-Café volunteer (`Baseline_Weeks/baseline-reading-writing-standard.html`) | Names used are from the synthetic demo set / fictional characters, not the real class. |
| B7 | `REGISTER.md:230,243` example rosters | Documentation examples ("Amy" + one common name), generic; REGISTER is append-only and provenance-bearing. |
| B8 | All "Will …?" sentence-start matches estate-wide (science decks, KCSIE assembly, grow-anim, primary, careers) | The modal verb. One pupil shares it; only roster entries were the pupil, and those are gone (A6, A7). |
| B9 | Base64 image data matches (`Tees_Trekkers` ×2, `Surrealism_Eye_Study`) | Coincidental byte sequences inside `data:` URIs. |

## C · Requires your ruling (nothing blocked on it)

| # | Item |
|---|---|
| C1 | **CLOSED 2026-08-26 (sitting SAT-F §6).** `biology/Structure_of_the_Thorax.html:1372` carried the real 9-name `Y10_FALLBACK` list. Matt lifted the freeze for this one file and it took the neutralisation above — nine names to `Pupil A`–`Pupil I`, array length and quote style preserved, diffstat one file / one line. `eviRoster()` at :1379 reads the list only when the pasted roster is empty, so behaviour is unchanged. The legacy-science freeze otherwise stands; no other frozen path was touched. Landed on main at `b37f1e5` (PR #159). |
| C4 | **NEW 2026-08-26, NOT fixed — needs your word.** Closing C1 meant re-running the nine-name census estate-wide, and it surfaced a line LT1 never read: `ASDAN/Consent_Aimee_La.html` and `ASDAN/Consent_Aimee_P2.html` each carry a teacher-facing TA deployment note naming **three real pupils** by first name (one the distinctive hyphenated entry), plus a named adult. LT1 filed this whole `Consent_*` family under **B1** — the *filename* character is adjudicated fictional, which is correct — and so never looked past the filename at the body text. B1 remains right about the filename and wrong as a clearance for the body. The other eight `Consent_*` files are clean; the pattern appears nowhere else in the estate. One line, duplicated across two files. Left unfixed under the same rule that held C1: safeguarding changes are not self-merged. Fix is the neutralisation above. **These two files are live on Pages.** |
| C2 | **Site repo** (`mattroper1977.github.io`, outside this order's scope): `uas/app.html:449` placeholder caption and `asdan/moderation-lab/index.html:597` demo forename each use a first name coinciding with a real class member (both read as demo data; surname "Demo", "e.g." caption). Flagged for a site-repo pass. |
| C3 | **Git history**: the removed names remain in this public repo's history. Removing them fully needs a history rewrite + force-push — disruptive, your call, not attempted. |

## D · Gates run

- **Positive control:** the name-census detector (names never committed; run
  locally) found the class lists in 71 files before the edits and, after them,
  exactly the judged set in B and C1 — nothing else.
- **Negative control:** a seeded file containing one census name was detected
  by the same detector, then removed; the tree re-verified clean.
- `tools/verify_fixture_names.mjs`: clean before and after; its `--self-test`
  (which seeds and must detect a person-shaped fixture) passes — the sweep can
  still go red.
- The diff is line-for-line (29/29): array lengths, grades, and quote styles
  preserved, so no consumer parses differently.
