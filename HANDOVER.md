# HANDOVER — Lundy Loop programme

**Current as of Pass LL-G, commit 6.** Supersede this file wholesale next session; do not append
— **with one exception: the queue may be appended to, provided each entry carries its own
trigger**, so it can be carried forward intact by whoever rewrites the file. Carrying
those entries forward is a **requirement of this header, not a courtesy** — whoever
supersedes this file is bound by the rule they are rewriting.

It is the one artefact here with no history worth reading.

---

## Read these first. This file does not repeat them.

| document | what it holds |
|---|---|
| [`/REGISTER.md`](REGISTER.md) | Estate conventions, deliberate absences, selectors, storage keys, deletion records with restore SHAs, cached-claims enumeration. **31 entries.** |
| [`/REBRAND.md`](REBRAND.md) | The Made by Matt → Progress Schools procedure. Governs every staff pack. |
| [`/LundyLoop/tools/INSTRUMENTS.md`](LundyLoop/tools/INSTRUMENTS.md) | The eight instruments, what each cannot detect, the blind-twin table, and the standing rules that govern instruments. |
| [`/LundyLoop/tools/`](LundyLoop/tools/) | The instruments themselves. Run them; do not rebuild them. |

**A handover that duplicates the register creates a twin, and twins diverge.** This
file carries only what those four cannot: where we got to, the open rulings, and the
queue with decisions attached.

---

## Start here, before anything else

**This estate has been healthier than its instruments every single time it was
tested.** Ten false-positive chains, seven corrections against Matt's own claims,
and **not one defect that reached a pupil**. The print subsystem went
691 → 12 → 4 → 7 → **0**: five alarms, five retirements, zero real defects.

A fresh session reading the open list below will assume this is a repo in trouble.
**It is not.** It is a repo that has been examined harder than most and has held up.
Start from that rather than from suspicion — and when an instrument disagrees with
the estate, suspect the instrument first. That has been right every time so far.

---

## How this works

- **Nothing commits without asking Matt for a key.** Every time, every pass, including
  one-file changes. Short-expiry tokens; he revokes when the work is done.
- **Declare the manifest before staging. Explicit paths only — never a directory
  glob.** Then assert the pushed commit's file list against the declared manifest
  **from a fresh clone**, not from the working copy.
- **Fetch after every push.** `refs/remotes/origin/main` is a cached claim; pushing
  to an explicit URL leaves it stale, silently, every time.
- **Report before authoring.** Measurement and specs go to Matt before anything is
  written into a lesson. He reads every word of anything pupil-facing or assessed —
  inline, not as a file reference.
- **Stop rather than start badly.** Do not open authoring work inside assessed files
  at the end of a long session. That call has been made four times and was right
  every time.
- **Check Matt's claims against HEAD before building on them.** Seven have moved so
  far. He would rather be corrected than obeyed.

---

## Where we got to — 11 commits this session, all verified from fresh clones

| SHA | what |
|---|---|
| `3b805af` | Instruments and their inventory |
| `5053aa3` | Remove 29 displaced root copies (28 identical + 1 stale revision) |
| `03b79b1` | Remove 10 superseded subject posters |
| `452102f` | Provenance note on the leadership layer |
| `918d7de` | Remove `wrangler.toml` |
| `d02ec43` | `classify.py` as required stage, `identity_audit.py`, two fixes |
| `4d17f50` | **site repo** — sitemap: the seven leadership documents |
| `7226b08` | `REGISTER.md` + `REBRAND.md` at root |
| `4023ab5` | R-A02 verified, R-A01 second selector, three rules |
| `8c384a7` | `assessed_conditions_gate.py` |
| `35efefd` | Blind-twin table in `INSTRUMENTS.md` |

40 files deleted, all recoverable — restore SHAs are in `REGISTER.md` §C.

---

## OPEN RULINGS — decided, not yet built. Do not re-decide these.

### 1 · Closed-world Card + declared authorisation — **design them together**
- **Closed-world line**, both Cards: *"anything not named above is not allowed."*
  Converts silence from permission-by-default into prohibition-by-default.
- **Declared authorisation**: every tier-offer names the Card clause permitting it
  (`authorised-by: supported-frames`). The gate stops doing string similarity and
  asks three exact questions instead.
- Together they make `assessed_conditions_gate` decidable in both directions.
- **This is a change inside assessed files. It should start a session, not end one.**

### 2 · The four unmentioned tier-offers
Three are rulings; **one is a tool artefact**:

| tier-offer | what it is |
|---|---|
| LAUNCH Standard — Route Card (45 min) | real ruling |
| GROW Standard — Time Budget (39 min) | real ruling |
| LAUNCH Supported — three frames, Card authorises two | real ruling — **remove the concession frame** *"However it cannot show ___"*; it is *prompting on what to argue* in a costume, and it brings LAUNCH into line with GROW, which is already clean |
| GROW Supported — Opening/Close Frame | **not a ruling.** Word-for-word correct against its Card; the token matcher cannot see it |

### 3 · The reconciliation pass — text to Matt first
- Timing strips **named explicitly in all three allowed lists** — *"order to everyone,
  numbers to nobody"* goes in the Card verbatim.
- The concession frame out of LAUNCH Supported.
- **Navigation staff note:** *the assessed slide is displayed front-of-class; where a
  pupil is working from a device for access reasons, the adult controls navigation.*

### 4 · The floor-lock — design for Matt's eyes, do not build
- `prevSlide()` is **unguarded** in both assessed files, `ArrowLeft` is bound, and
  there is no lock of any kind. Verified 2026-07-26.
- Front-of-class delivery makes the **default** safe. The **access arrangements the
  Card guarantees** — a device for reading support, a scribe at the screen, a separate
  room — are exactly what puts a pupil in front of a navigable file.
- **The assessed set, inside the boundary:** the assessed task slide, the Conditions
  Card, and the sources. All three have legitimate mid-sitting re-show reasons, the
  Card most of all — a pupil returning from a break is exactly who needs telling what
  is allowed. Locking that would be a lock that withholds access.
- Everything **before** the boundary is locked out: the teaching, the We Do Close
  Moves, the Reveal Answers button.

### 5 · A2b — drafted, not shipped. Full draft in the session log; rulings below.
- **Publish no durations.** Order to the pupil, numbers to the supervising adult as a
  **pacing note**: if a pupil is still on Source A past the halfway point, check they
  know they can move on.
- **The 30-vs-8 imbalance** (30 min reading, 8 min for the marked judgement) is
  registered as an **observation for review after the first sitting** — not changed on
  an arithmetic hunch.
- **W6 connective revisit**, both LAUNCH and GROW. Shared core (*a connective is a
  claim, not a joiner*), different examples: LAUNCH's serve source-utility, GROW's
  serve causal explanation in an account. Tier rule applies.
- **Local examples — Matt's ruling, all three, two jobs.** The **Transporter Bridge**
  carries the demonstration because it takes all three connectives on the same facts.
  The **Stockton & Darlington railway** and **Billingham chemical works** carry the
  practice, because each wants one connective and choosing is the skill.
  **Not Redcar** — wrong coalfield, and too raw for a grammar point.
- **The null is `"I can't defend either yet — I need ___"`**, not *"I'm not sure"*.
  It converts a null into an observable pupil action. **This is the LL-5 standard
  null wherever a gate needs one.**
- The LL-3 writing line **already carries its own null** — *"Pass is always allowed"*.
  Do not author a competing one.

### 6 · Still carried, and will be forgotten first
**LL-E must be re-derived, not reconciled** (R-E03) — its own derivation died with the
sandbox. **LL-5 needs L3 redefined or declared unquotable BEFORE the pass runs**
(R-E02), or it moves the way L5 did. Two days carried.

### 7 · KO staleness — read one file
`Grow/Slideshows/GROW_HUM_W7_Write_The_Account.html`. Assessed, 7 content movers, and
the first is `Pass LL-A2a`, which **removed the Connective Bank and the Evaluation
Deployments**. If its KO names either, it describes support that no longer exists —
a fourth surface disagreeing with the Card. **Read it against the Card, not the body.**
Full list: `python3 LundyLoop/tools/ko_staleness.py`.

---

## The queue, in order

1. Closed-world + declared authorisation, designed together → re-run the gate
2. The reconciliation pass (text to Matt first)
3. The floor-lock design
4. A2b drafts — LAUNCH W6 and GROW W6
5. LL-E's reconciled table
6. LL-5 — 58 files, BUILD 28 · GROW 20 · LAUNCH 10. Six specimens across three suites
   before authoring at scale. **L3 settled first.**
7. KO triage from §7


### Added by Pass LL-G — owed, with triggers attached

**Written down rather than remembered.** A shelved item with no written trigger either
gets forgotten, or gets restarted by someone who does not know why it stopped.

8. **`INSTRUMENTS.md` repair — LANDED (H-series Route U · H3 `64d8fb4`).** Three instruments had no entry of their own —
   `assessed_conditions_gate.py`, `sitemap_audit.py`, `ko_staleness.py` — while being
   referenced by ID in the blind-twin table and in R-G01. Re-observe R-G01 row 2, whose
   *"6 listed / 6 actual"* went stale silently while its own "what keeps it true" column
   already said `nothing`. **Target after Pass LL-G lands: 10 scripts / 11 entries**
   (11 includes the quarantined `LL-INST-03-v1`, which has an entry and no script — do
   not read that as an off-by-one). Registered as **R-G03**.
   **TRIGGER: none — it is owed now.** Small, self-contained, no dependency on anything
   below.
   **Carry the counts fix into it:** *"N listed / N actual"* is a sentence that could be
   a derivation. Four counts went stale during Pass LL-G alone, every one correct when
   written and not re-derived when its subject moved. `bundle_facts.py` is the shape —
   a number a script prints when it runs cannot be stale; a number in prose can.

9. **The `ko_staleness.py` refinement.** Two lines in `visible()`'s caller, excluding
   regions whose own markup declares them not-KO-relevant (`class="lm-strip"`,
   `class="lm-own"`). Tested: restores the pre-patch body hash in **45 of 45** files.
   Take the self-describing region, **not** an entry in the `ARCHITECTURE` list — a wrong
   entry there silently *drops* a real candidate, which already happened once with
   `Pass LL-A2a`, and that is the expensive direction. Registered as **R-E07**.
   **TRIGGER: after Pass LL-G's KO output has been read and judged — never during.**
   An instrument must not be modified in the pass it is measuring (**R-E09**). Until
   then the 45 new candidates are an expected artefact, not forty-five stale organisers.

10. **The TA card, both brandings — LANDED (H-series Route U · H1 `9af1e63`).** Progress Schools variant into the staff pack;
    Made by Matt variant onto the site. One page each, already built and gate-checked
    (REBRAND rules 1–5 clean; ~10 lines of headroom at 110% zoom with the estate font
    substituted).
    **TRIGGER: before the first staff briefing of term — not the first week of
    lessons.** A TA who meets the printed strip before they meet the card will fill the
    box in on the pupil's behalf, which is the exact failure the pass exists to remove.
    **Until this lands, the 45 files carry a printed strip and nothing else.** The strip
    is the mechanism; the card is the behaviour that makes it mean anything.

11. **The day card and the tutor-time ninety seconds — SHELVED, not abandoned.**
    Designed in full (Pass LL-G deliverable B2 §(c) and §(d)): a pupil-held A5 week card,
    five rows, no second copy; and ninety seconds inside the existing Tutor Time evidence
    slot, run by the rotating Evidence Captain.
    **TRIGGER: only if the lesson-level mark is observed working in a real room** — a
    pupil answering *"what does this ring mean?"* with an event rather than with the
    sheet, and blanks present rather than absent. See the three-week check.
    **Why it stopped, and by whose decision:** stopping was the *recommendation* — the
    lesson-level mark is the smaller true answer and should be shown to work before
    anything is built on it — and **Matt took it**. This is a decision, not work that
    ran out of time, and not abandoned work. The design exists in full and is ready.
    **R-A09 binds anything built here: no second copy, ever.**

*Queue entries 8–11 added by Pass LL-G at `d601842`.*

### Added by Pass LL-I — the day-close designs, with triggers

Two ratified designs live at `LundyLoop/6_designs/` (B2 the day-close reader, B3 the
GROW→LAUNCH warrant step-up). Everything below flows from them.

12. **The specimen pass.** Build one specimen of the day-close + LAUNCH warrant line —
    the specimen chosen to *break* the design, per the LL-G rule — gated, before any batch.
    **Inputs, all under `LundyLoop/6_designs/`:** the ratified designs (`LL-I_B2_day_close_reader.md`,
    `LL-I_B3_grow_launch_stepup.md`) and the measurement records they rest on
    (`LL-I_B1_measurement_map.md`, `LL-I_B2_0_closure_definitions.md` — OBSERVATION RECORDs,
    re-derive before relying).
    **TRIGGER: a new session with Matt's go; one specimen, gated, before scale.**
13. **The calibration-game pathway section — LANDED (September-cluster pass).** The
    pathway-scoped section is authored into
    `LundyLoop/5_staff_training/R_Gate_Calibration_Game.html` (B2 §5): the game is scoped to the
    BUILD close; a GROW · LAUNCH card states closure is the pupil *writing* the line, the adult is
    audience not verifier, no adult initial is expected, and the day-close re-read is a
    strengthening not a requirement (a day whose close never happened is a closed day; no
    "catch it up tomorrow"). The week-one failure case — GROW room, no R box, nothing missing —
    is named as a false record ("receipt by the back door"); *"Not yet = Voice present, Audience
    pending"* is reused verbatim; no new vocabulary; both sentinels unmoved (45 / 48).
    **Rebuilt at `eea4062`** (LL-I, Option 1): the answer-model gap resolved — label 0
    `Closed (R)→Closed`, the legend broadened pathway-relative — and scenarios 15–16 (GROW/LAUNCH)
    authored **into the question array itself**, so a question-only TA meets both closes inside the
    flow (R-H10). Provenance: **card at `a5092bb` · legend, label and scenarios 15–16 at `eea4062`.**
    **R-H08 CLOSED** on Matt's stated second paper read of the rebuilt game (card at `a5092bb` ·
    legend, label and scenarios 15–16 at `eea4062`). The read itself is a human observation, not a
    derivation; no instrument witnessed it.
14. **The LL-5 GROW/LAUNCH population rework.** The 48 written-line files (R-A02) inherit
    B2's pupil-reader and B3's evidence/warrant step-up. **TRIGGER: after the specimen is
    judged; L3/L4/L5 settled against the day-close capture route first (R-E02).**
15. **The LAUNCH line wording.** The pupil-facing warrant clause on LAUNCH's closure line.
    **TRIGGER: the specimen pass — it is authoring and waits for Matt's read; ship gate applies.**

*Queue entries 12–15 added by Pass LL-I.*

### September-cluster pass — what landed, what stopped

- **LANDED (one commit):** queue entry 13, the calibration-game pathway section — see entry 13
  above. Both sentinels re-derived unchanged (45 / 48) after the edit. The section stays out of
  both counts **by authoring discipline — it quotes neither sentinel marker** — not by any
  exclusion on the raw §0.4 grep, which reaches into `LundyLoop/5_staff_training/`. The folder's
  exclusion lives only in the R-E08 derivation of record; see **R-E10** for the reconciliation of
  the raw grep against the derivation of record.
- **STOPPED AT INTAKE — no commit made, nothing reconstructed:** H1 (the TA card, both
  brandings — queue 10), H2 (`patch_loopmark.py` + `bundle_facts.py` into `LundyLoop/tools/`),
  and therefore H3 (`INSTRUMENTS.md`, whose count is derived only *after* H2). The pass ran from
  a fresh clone in which the untracked `_intake/` staging folder was absent, so none of the
  H-series source artefacts were present. Per the order's stop rule they were **not** rebuilt,
  re-authored or inferred. **Queue entries 8, 9, 10 and R-G03 remain OPEN, unchanged.** Re-run
  H1 → H2 → H3 from a session that actually carries the artefacts in `_intake/` (a local session,
  or artefacts committed to a staging branch — an ephemeral remote clone will not see files
  dropped on a local machine, which is the failure this cluster was commissioned to end).
- **UPDATE — the H-series LANDED via Route U** (`intake_september.zip`, all four artefact hashes
  verified against the confirmed v2 manifest; cards taken from the approved tone drafts, not the
  zip): **H1** `9af1e63` (both TA cards into `5_staff_training/`), **H2** `51d14aa`
  (`patch_loopmark.py` + `bundle_facts.py` into `tools/`), **H3** `64d8fb4` (INSTRUMENTS.md 13/13
  both directions + REGISTER R-H11 and R-H08 CLOSED). **Queue 8, 10 and R-G03 are now closed
  (above).** **Queue 9** (the `ko_staleness.py` R-E07 refinement) is a **separate, gated item —
  not H-series work** (R-E09 forbids modifying an instrument in a pass that measures it) — and
  **stays OPEN**; it was not touched by this order. Two dispositioned residues: R-G03's REGISTER
  STATUS still reads OPEN (its flip was outside H3's confirmed register payload, which carried only
  the near-match entry + the R-H08 flip); and both TA cards were placed exactly as Matt approved —
  the Progress card carries no `x-brand` tag and uses `Progress Schools — Tees Valley` rather than
  the estate strip (REBRAND checks 3–4), flagged, not edited.

---

## What Matt still owes, and what he has ruled out

**Owed:** nothing blocking. **Ruled out:** merging graded cold-call into the shared
roster (R-B02); changing the assessed source load on an arithmetic hunch; rewriting
history to tidy the gmail/hotmail author split.

**Unrun:** `sitemap_audit.py` cannot execute from the agent sandbox — outbound HTTP is
proxied and returns 403. **It fails loudly rather than reporting a pass**, which is
correct. Run it from a machine with network egress.

---

# SESSION: Pass V + D&T v5 + estate reduced-motion + Pass S (session_0183, 2026-07-28)

A separate programme from the Lundy Loop work above, sharing the repo. Bootstraps by
cloning, not by memory. All commits verified from fresh clones / live at pinned SHA.

## Commit ledger (each with rollback)
| Work | Commit(s) | Rollback |
|---|---|---|
| Include Lundy in printed pack, W1–W6 (per-deck) | `b1b7ee0` `4452e46` `9efbdc8` `cf53665` `26d2eb3` `7889055` | `16b5ea5` |
| W1 title → "The Workshop Audit" (all surfaces) | `32d0f23` | `7889055` |
| Stale week labels (W6 banner, Print-Tools ×5) | `9210562` | `32d0f23` |
| RM: Art_Teesside 31 | `e3082d2` | `9210562` |
| RM: BUILD_ASDAN 31 | `6816fc0` | `e3082d2` |
| RM: GROW_ASDAN 18 | `cef0c73` | `6816fc0` |
| RM: Build D&T 6 | `f1d85c0` | `cef0c73` |
| RM: BUILD_HUM 8 | `6bc13b7` | `f1d85c0` |
| RM: GROW_HUM 7 (non-assessed) | `47f8494` | `6bc13b7` |
| RM: GROW_HUM_W7 (assessed, alone) | `e425bb8` | `47f8494` |
| ASDAN Consent provenance note (×10) | `0ec1da0` | `e425bb8` |
| REGISTER R-A07 boundary | `32441c5` | `8ead540` |
| Pass S: W1/W2/W3/W5 (per-file) | `6bbf34e` `1bca277` `96f8294` `b92fe6d` | `7e42831` → each prior |

RM standard applied to **102 files** (86 `.ilm *` CAREERS chassis + 16 HUM). ASDAN 2 and
LAUNCH_HUM 8 already covered — not touched.

## Standing rules logged this session
- **Measure the repo before authoring anything a spec calls "new."** Five false premises
  dissolved before build: hidden-nail sweep already present · chassis is 10 slides not 9 ·
  LAUNCH_HUM already RM-covered · ASDAN already RM-covered · Pass S A/B ergonomics/chamfer
  already written.
- **RM detection must see BOTH implementations:** CSS `@media (prefers-reduced-motion)`
  AND JS `matchMedia(...)` + class-toggle + class-scoped CSS (e.g. `body.reduce ...`). A
  CSS-only classifier called ASDAN a defect; it is a better implementation (it gates audio).
- **Assessed-file edits — house formulation:** diff pre/post, assert exactly one changed
  hunk lying entirely between the `@media (prefers-reduced-motion)` open brace and its
  matching close. Proves nothing outside moved, including what nobody enumerated. Beats
  listing the Card / tiers / print sections.
- **Whitespace-both-sides:** when normalising whitespace for a containment test, strip it
  from BOTH needle and haystack, or the match never fires.
- **Never classify an RM block from a truncated selector capture** — brace-match to the
  closing `}` and read the whole thing. (Corrected a 24→16 count.)
- **An instrument wrong twice does not close a question.** Re-run it after every fix to its
  own blind spot; treat any bucket it calls "clean" as unverified until asked how it knows.
- **Deliberate print triplication** (per-tier worksheet copy) is marked do-not-de-duplicate
  in-file; a pupil receives only their own tier's sheet (Pass N print-reference pattern).

## Open queue (this programme)
1. **LIGHT RM — 10 files, approved, specimens gated:** primary/space 6 · Assembly 3 ·
   Tutor_Time 1. Each chassis its own specimen back to Matt before its batch. NB Assembly:
   commit `8bc2b8b` already patched `.phonepop/.tick/.filmyet` for the opacity:0 trap — first
   establish whether these 3 are those 3 with different residue or a different three.
2. **MEDIUM RM — 25 files:** 6 Art 13 · 2 Physics 10 12. 6 Art shares CAREERS keyframe
   names — verify semantics per file; same names ≠ same function in a different chassis.
3. **Nudge-gap content pass:** all 86 CAREERS files carry the transient `.match-target.wrong`
   red-border shake nudge with no icon+word at that cue — colour-alone breach candidate
   needing a text nudge. Content pass, not an RM commit.
4. **HEAVY RM — 34 files, gated on a fresh go from Matt:** biology 10 · chemistry 8 ·
   Intervention 6 · Local Choice 10. Four separate chassis. Biology builds print content at
   runtime → static validation insufficient; jsdom rendering with process-level error
   handlers is mandatory.

## The human's open calls (not the session's to decide)
- **Estate `data-timer` question:** the deck timers sum to ~53 min (inherited from the CAREERS
  donor, likely chassis-wide) while the timetable period is 40 min authoritative. `data-timer`
  is a per-phase on-screen countdown, not a schedule; drop-first phases exist by design. No
  session edits timers in passing — candidate estate-wide question.
- **Games (21 files) decorative-motion question:** motion is the content; suppressing it
  destroys the artefact. Open sub-question: should decorative splash/title motion respect RM
  while gameplay does not? Defect class otherwise closed.
- **Lundy print-page wording sub-check:** the physical print check confirmed ORDER, not
  wording. If the printed Lundy page on the six v5 decks ever reads as staff instructions
  rather than pupil-facing, that is a wording fix, never a revert (recorded at R-A07 BOUNDARY).
- **Pass S recovery route** assumes the TA can help a returning pupil measure the model at the
  bench (reclaimed-timber build; no "standard sizes" reference exists — confirmed absent).

---

## IN-FLIGHT BRANCHES — for a merge session running without the author present

*Added by Pass Y (2026-07-29). Bounded operational note. Branch list and bases **derived from the repo**
(`git merge-base <branch> origin/main`), not remembered. `main` has moved under in-flight work more than once
this cycle — a diverged branch is the expected state, not a surprise (R-SB02 / R-H02).*

| branch | cut from (derived base) | ahead | state vs main |
|---|---|---|---|
| `pass-sl-sow-launch` | `32ca685` | +11 | diverged — unmerged |
| `pass-sbx-art-a2` | `4f5c6a4` | +5 | diverged — unmerged |
| `pass-pq-peq-audit` | `32ca685` | +3 | diverged — unmerged |
| `pass-sg-sow-grow` | `32ca685` | +5 | diverged — unmerged |

**Each was cut before recent merges landed, so each is now behind `main`.** When merging any of them:
- **Expect `REGISTER.md` conflicts** — several passes append entries at the file tail, so two branches adding
  entries collide there. **Resolve by KEEPING EVERY ENTRY from both sides (append-only union), never by
  choosing one side.** An entry dropped in a merge is a silent deletion of a recorded decision. The same holds
  for `HANDOVER.md` queue additions.
- Use an **explicit merge commit (no rebase, no squash)** — the ledgers are SHA-anchored (R-G01 family);
  a rebase orphans every recorded reference.
- **Re-read `origin/main` immediately before each merge** and re-prove at the merged tip, not on the branch.

*(`pass-y-assumptions` is being merged in this session and is omitted. `pass-x-instruments`, `pass-sb-sow-build`
and `pilot/launch-hum-w1-illuminator` are already merged. Older branches — `art-remediation`,
`claude/grow-sow-audit-phase-3-*` — are outside this bounded note; enumerate with the derived-base method above
if they become live.)*

---

## Pass E (KO Triage) — landing note (2026-07-29)

**Held on `pass-e-ko-triage` (base `12cb6d9`); nothing merged.** Re-derived **117** KO-staleness candidates at
HEAD (not the carried 114; +3, within ±10; `117+0+44=161` KO corpus). Read all 115 non-assessed:
**112 STILL-TRUE, 3 STALE**. R-G05 re-tested → **0/49** (retired by Pass G's rebuild). Assessed pair read-only,
held for Matt.

**Held Tier-2 fixes (KO text only, deploy-visible, awaiting Matt's per-row key):**
- BUILD_ASDAN — `CAREERS_W6` KO h1 W6→W7, `CAREERS_W7` KO h1 W7→W6 (week labels lagged the restored slot-swap).
- Build — `BUILD_HUM_W6` KO gains the PEEL Link row + completed Key Fact.

**Coexistence (R-H02): a parallel Pass Q (the same briefed pass, renamed Z→Q) already merged to `main`
(`59ad56a`)** — 0 STALE/114, R-G05 refuted 0/49, a CAREERS_W7 *print* fix. Pass Q landed first and holds;
Pass E **corroborates R-G05 independently** and **adds 3 STALE** on axes Pass Q's KO-vs-We-Do-2 read did not
cover (KO h1 week label; HUM writing-model completeness). All 3 pre-date Pass Q's head. Reconciliation and the
open decisions (letter E-vs-Q; whether to merge the 3 fixes; expected `REGISTER.md`/`CAREERS_W7` merge
conflicts) are in `_passe/COEXISTENCE_PassQ.md`. **Re-read `origin/main` before any merge** — it has moved twice
during this pass.
