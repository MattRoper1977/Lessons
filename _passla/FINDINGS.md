# FINDINGS.md — Pass LA (LAUNCH ASDAN suite), Phase 0 + Phase 1

**Pass:** LAUNCH ASDAN suite build (+ GROW/LAUNCH overviews).
**Branch:** `pass-la-launch-asdan` (off BASE; parks UNMERGED).
**Authority chain:** official ASDAN PDFs (ABSENT — see below) → `_passpq/PEQ_PRIMER.md` +
brief §2.2 + Evidence Binder corroborator → nothing. Spec-dependent lines tagged
`UNVERIFIED-AGAINST-SPEC`.

---

## 0 · Phase 0 environment gates — result

| gate | result |
|---|---|
| **Right-repo proof** | **PASS.** Repo = `MattRoper1977/Lessons`. `_passpq/` resolves at root; `BUILD_ASDAN/` (Hub + 5 slots + 31 lessons) resolves; `GROW_ASDAN/GROW_ASDAN_Hub.html` resolves. (The session opened attached to `mattroper1977.github.io` — the wrong repo, as the brief warned — and `Lessons` was attached and cloned before any work.) |
| **BASE pinned** | `6945c223ab55469df09b9c53c79fd2c584cc06b1` — origin/main HEAD at open (`Merge CLOSE-1: re-close 20 GROW/LAUNCH science decks onto the written-line`). |
| **Branch** | `pass-la-launch-asdan` created off BASE. No PR. Matt merges. |
| **SoW acquired** | `LAUNCH KS4 - 2026-27.xlsx` from `pass-sl-sow-launch@2a1cfda`, committed read-only under `_passla/inputs/` with provenance. Nothing merged. |
| **Official ASDAN PDFs** | **ABSENT.** `_passpq/inputs/` holds only its README. Proceeding on primer + baked facts + Binder corroborator; spec-dependent claims tagged `UNVERIFIED-AGAINST-SPEC` for the PQ resume. Not blocking (brief §0). |

**Fetch-recheck discipline for pushes:** main is actively pushed to. Fetch-recheck before
every push, max 2 attempts, then STOP — never force. (No push in Phase 1 except the
`_passla/` docs on the branch.)

---

## 1 · Estate inventory (enumerated, not assumed)

### BUILD_ASDAN/ — 40 files
- **Hub:** `BUILD_ASDAN/BUILD_ASDAN_Hub.html` (`BUILD ASDAN · Autumn 1`)
- **Standalone non-lesson docs (2):** `Resources_and_Tools.html`, `Scheme_of_Work.html`
- **START_HERE (5):** Careers, Community_Project, Duke_and_Enterprise, FoodWise, Living_Independently
- **Lessons (31):** Careers 7 (W1–W7) · Community_Project 6 · Duke_and_Enterprise 6 · FoodWise 6 · Living_Independently 6
- **Root entry file:** `build_asdan.html` (`BUILD Pathway — Autumn 2026`)

### GROW_ASDAN/ — 23 files
- **Hub:** `GROW_ASDAN/GROW_ASDAN_Hub.html` (`GROW ASDAN · the full term`)
- **Combined non-lesson doc (1):** `Scheme_and_Resources.html` (`GROW ASDAN · Scheme of Work & Resources · Aut 1`) — scheme + resources merged into one file
- **START_HERE (3):** PEQ, Community_Project, Enterprise
- **Lessons (18):** PEQ 6 (W1–W6) · Community_Project 6 (GCOMM) · Enterprise 6 (ENT)
- **Root entry file:** NONE

### LAUNCH ASDAN — does not exist
No `LAUNCH_ASDAN/` folder and no LAUNCH-ASDAN lessons anywhere (confirmed by two sweeps).
All existing `Launch/` material is the separate Teesside/Art/Hum pathway, **not ASDAN**.
Zero LAUNCH ASDAN lessons — brief §2.1 confirmed.

### Chassis (donor) — GROW PEQ W1, verified faithful v5
`GROW_ASDAN/PEQ/PEQ_W1_Knowing_Myself.html` (604 lines): title
`GROW ASDAN · PEQ Level 1 (E3 floor · L2 stretch) W1 · Knowing Myself`; carries the full
feature set — witness (`#print-witness`, "Witness Statement"), `printPack` id array,
`_ccQuestions` (Cold Call), Lundy, confetti/XP, `prefers-reduced-motion`. **Carries NO
sentinel** (`ll-g:loop-mark` = 0), as required. This is the donor for Phase 2.

---

## 2 · Sentinel (`ll-g:loop-mark`) baseline — DISCREPANCY vs brief, reconciled

- Brief §2.1 states the sentinel derives to **45** files (31 BUILD_ASDAN + 6 D&T + 8 Art_Teesside).
- **Repo at BASE shows 50 HTML files** carrying it: BUILD_ASDAN **31** + Art_Teesside **8**
  + Build **6** + Science_Teesside **5**. The extra **5 Science_Teesside** decks were marked
  by later science passes (BASE = a CLOSE-1 merge that re-closed 20 GROW/LAUNCH **science**
  decks). (Total `grep -l` hits = 64, incl. 14 non-HTML docs/tooling that merely *mention*
  the string — REGISTER.md, `_passsci1/*`, `LundyLoop/tools/*`, etc.; those are not the set.)
- **Assessment:** baseline drift from intervening science passes, **not** a live contradiction
  in the deliverables. Science is standing no-touch; this pass does not modify it and will
  **not** add the sentinel to any LAUNCH file.
- **Gate for this pass:** SET-invariance of the 50-file HTML set pre/post + new LAUNCH files
  carry no sentinel. The absolute number (50, not 45) is the baseline; **never "restore" 45
  or 49** (both are stale). Flagged to Matt in the STOP report.

---

## 3 · UNVERIFIED-AGAINST-SPEC register (PDFs absent)

Every PEQ credit/unit/level fact used in `SUITE_PROPOSAL.md` derives from brief §2.2 +
`_passpq/PEQ_PRIMER.md` + the Evidence Binder (Ofqual-URN-bearing), all tagged
`UNVERIFIED-AGAINST-SPEC`. Carried forward to HANDOVER for the PQ resume to reconcile:

- Unit credit values (ComSk1 3 · DecMkSk1 2 · LSk1 2 · TmWkSk1 2 · ThSk1 3 · WellbLe1 3 = 15).
- Rules of combination (Award 4 · Extended Award 9 · Certificate 14, min 11 at level).
- The "plan used over ≥10 hours" cumulative-cross-week window.
- Command-verb level pitch (E3 State/List/Identify · L1 Outline/Describe/range).
- Activity minimums (ComSk1 presentation ≥3 min OR ≥250 words; teams ≥3).
- Safeguarding-disclosure notice wording for DecMk/WellbLe (also `UNDETERMINED — needs unit booklets`).
