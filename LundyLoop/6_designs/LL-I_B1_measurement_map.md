# LL-I · B1 — Measurement map

> **OBSERVATION RECORD — not a description of the estate.**
> **These figures were true at `195ee37` and MUST be re-derived before being relied on.** A future
> session reading them as current is the failure mode this header exists to name. Every figure below
> carries the derivation that produced it — re-run the derivation, do not trust the number.
> **Pass:** LL-I · **Date:** 2026-07-28 · **Last observed true at** `195ee37`.

---

## B1.1 · The end of the day as it exists — `Tutor_Time/`

- **Population:** `git ls-files 'Tutor_Time/*.html'` → 17 files (8× `WB_W1..W8`, 2× `KCSIE_*`, 2 trackers, `Scheme_of_Work`, `Lesson_Plans`, `START_HERE`, 2 older standalone decks).
- **The closing runs check-out → evidence → exit.** The 8 WB decks end: **Check-out** (feel-word, *"Passing is always okay"*) → **Evidence slot** (rotating **Evidence Captain**: ONE photo *"work, not faces (unless consent is filed)"* + a caption frame + one "launch" written line; TA *"file it in the school's evidence system, tag STRAND + tutor group, tick the tracker"*) → **Exit ticket** (+ anonymous *"anything you want an adult to know?"* box). KCSIE decks: no Captain, no check-out, no loop.
- **No closing-slot timing is stated anywhere.** (grep for minute/`data-timer` on the closing slides → none.)
- **No pupil-facing collation, no "R", no "ring", no "triangulate".** Present: Lundy **S/V/A/I** (Space/Voice/Audience/Influence). Collation today is the *TA* ticking a *separate* tracker file.
- **Stores** (`grep -oE "setItem\(['\"][a-z_0-9]+" Tutor_Time/*.html`): `mbm_tt_evidence` (R-B04, retired-in-place), `tt_tracker_v2` (R-B05, online tracker only), `mbm_cc_v1`, `ps_coldcall_roster`, `<key>__stamp`.
- **R-B05 bug reconfirmed:** `Evidence_Tracker_Online.html` `prog()` counts a session evidenced on `s.photo && s.cap` and **ignores the S/V/A/I ticks beside it**.

## B1.2 · The assessment surfaces

- **ASDAN (BUILD + GROW):** per lesson a pupil generates **Documentarian photo + written annotation + Witness tick + a Supported/Standard/Stretch ring**, printed as KO / Arrival / **Assessor Witness Statement** / Feedback Sheet → the **ASDAN portfolio**. ASDAN evidence does **not** use S/V/A/I ticks. (Derivation: read `BUILD_ASDAN/*/*W3*.html` print-sections; grep `Documentarian|Assessor Witness|ASDAN .* portfolio`.)
- **AQA UAS (GROW W7 + LAUNCH W7):** a careful **non-claim** — *"these lessons prepare and evidence the history; they do not self-certify the award"*, *"centre-approved assessment conditions"*, and **no file claims the school is an exam centre.** **`"Cheryl"` and a head-office submitter are ABSENT from the repo** (`git grep -i cheryl` → none) — that route is Matt's real-world knowledge, not encoded (R-F04). Files name no submitter.
- **Representation split:** the Art packs render Lundy as four full-word zones (SPACE/VOICE/AUDIENCE/INFLUENCE); the Tutor-Time trackers render it as S/V/A/I ticks.

## B1.3 · Reading ages of the pupil-facing loop language *(self-contained FK + ARI)*

| loop text | words | FK grade (~age) | ARI grade (~age) | Reading Ease |
|---|---|---|---|---|
| BUILD — modality strip + ownership + null | 44 | 5.4 (~10.4) | 3.2 (~8.2) | 68 |
| **GROW = LAUNCH — written closure line** | 40 | 1.4 (~6.4) | −0.1 (~4.9) | 94 |

- **Derivation:** strip markup, count sentences/words/syllables, apply FK/ARI/Flesch. The GROW/LAUNCH figures are identical because the strings are **byte-identical** — `diff <(grep 'Closing the loop' GROW_HUM_W1) <(grep 'Closing the loop' LAUNCH_HUM_W1)` → no difference.
- **Caveats (carry with the numbers):** FK/ARI are calibrated on continuous prose; on <45-word fragments they diverge ~2 grades on the same text and ARI floors negative — **absolute ages are indicative only.** The **inversion** (closure line reads *easier* than the BUILD strip → the pathway steps *down* here) and the **glyph caveat** (the formulas cannot see the BUILD strip's six-glyph ring format → its effective demand is lower than ~10.4) are the load-bearing reads, not the exact ages.

## B1.4 · The GROW R-gate, re-derived

- **"The R-gate" is not a coded instrument** — `ls LundyLoop/tools/*.py` has no `r_gate`; the "0 of 8" has no in-tree predicate (see B2.0 §1 and R-H07).
- **The 8 files** = `git ls-files 'Grow/Slideshows/GROW_HUM_*.html'` (W1–W8). Per-file derivation (`grep -c` for the ring, the written line, and any adult-R/received/initial): **7 (W1–W6, W8)** carry the written line with `ring=0, adultR=0`; **W7** is the assessed file (no written line, different chassis). **0 of 8 have a received-R closer** — because GROW closure is pupil-writes by design, not a defect.

## B1.5 · Transition points *(mutually exclusive by pathway)*

- `git grep -l 'll-g:loop-mark v1' -- '*.html'` = **45** (the ring; all BUILD). `git grep -l 'What I said, and what it changed' -- '*.html'` = **48** (the written line; all GROW/LAUNCH; matches R-A02). No lesson file carries both. *(Unscoped, each returns +1 — REGISTER.md joins the count; hence the `-- '*.html'` scope, R-E08.)*
- **The seam:** at BUILD→GROW the ring becomes the written line (D1, designed — the prose names the switch) and the adult **"R — adult initials that they received it"** vanishes (D2). Tier vocab (`supported/standard/stretch`) and `taBriefs` are **continuous** across the seam (D3, D4 — not the carrier of the loop switch).

## R-A09 invariant — verified at HEAD

- `sentinel` / `lm-strip` / `lm-own` are the **identical 45-file set** (`diff` of the three `git grep -l` lists → no difference), **zero leakage** into Tutor_Time / GROW / LAUNCH. The trackers' S/V/A/I column is the pre-existing R-B05 representation, not a second copy of the ring. The absence is intact.
