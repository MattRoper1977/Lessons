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

8. **`INSTRUMENTS.md` repair.** Three instruments have no entry of their own —
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

10. **The TA card, both brandings.** Progress Schools variant into the staff pack;
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

---

## What Matt still owes, and what he has ruled out

**Owed:** nothing blocking. **Ruled out:** merging graded cold-call into the shared
roster (R-B02); changing the assessed source load on an arithmetic hunch; rewriting
history to tidy the gmail/hotmail author split.

**Unrun:** `sitemap_audit.py` cannot execute from the agent sandbox — outbound HTTP is
proxied and returns 403. **It fails loudly rather than reporting a pass**, which is
correct. Run it from a machine with network egress.
