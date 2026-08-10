# A10 — the public Baseline Weeks pack

Nine files (8 HTML + `README.md`), published at `Baseline_Weeks/` in the repo root — not under
`Science_Teesside/`, because the pack spans Reading & Writing, Maths and Science and filing it
under one subject would misfile two thirds of it.

Independently re-verified after editing, not taken from its README: **0 localStorage /
sessionStorage / indexedDB / cookies / fetch / XHR / sendBeacon / `<form>` / external URLs /
external scripts**, across all 8 HTML files. Print stylesheet present in 8/8.

---

## A10.1 — the answer key is in the page. Disclosed, not removed.

`DATA.items[].correct` holds the keyed option index and the scoring block reads it. Anyone who
views source can read the key.

Not removed and not restructured — that is a redesign, not a repair. Instead a plain statement was
added to **both** `README.md` and the `index.html` staff notes, so the exposure is a decision
rather than an accident.

**AMBER for Matt.** If the key should come out, that is a separate pass.

## A10.2 — the deficit label on an all-uncertain strand. Fixed, proven by render.

`attempted === 0 && uncertain > 0` rendered **"Need more evidence"** with *"Too little evidence was
collected in this sitting…"* — a deficit statement earned by using the safe option, on the screen
of the pupil most likely to have needed it.

Now renders **"Not started yet"** / *"This strand was not attempted today. That is information
about readiness, not about ability — pick it up in ordinary teaching."*

Proven by driving the real UI in headless Chromium (`_sciv3/tools/baseline_render.mjs`), choosing
the escape option on every item in all six assessments, and reading the rendered profile.

## A10.2b — AMBER, beyond the letter of A10.2: a second false deficit, firing on every sitting

Render turned up a sibling case the document does not name.

The strand loop only counts `kind === 'mcq'` items. **The "Writing / communication" strand in both
reading-writing files has zero MCQ items** — it is `text` + `teacher` only. So `attempted` can
never rise above 0 and `uncertain` never above 0 either, and the strand rendered:

> **Writing / communication — Need more evidence**
> "Too little evidence was collected in this sitting to make a useful starting statement."

**on every sitting**, including one where the pupil wrote a full response. That is the same
false-deficit harm A10.2 names, on the strand where the pupil has written the most, and it is
unconditional rather than conditional.

Fixed the same way: a strand with no scoreable items now reads **"Answered in writing"** /
*"This strand is answered in the pupil's own words, so it is not summarised here. Read the
response — that is the evidence."*

A10.2 says "leave every other branch untouched", so **this is flagged rather than assumed**. It is
one `else if` clause in `_sciv3/tools/build_baseline.py`; deleting it reverts the behaviour exactly.

**Every other branch was proven unchanged by rendering the original and the repaired file
side by side and diffing the output** — including the one-item strands that correctly render
"Developing / mixed evidence" rather than "Clear evidence seen".

## A10.3 — one organ, two names. Recorded, changed nothing.

The escape option is **"Not sure yet"** in the three standard files and **"Not ready yet"** in the
three specialist/SEMH files. The matching regex handles both (`/not sure|not ready/i`), so nothing
is broken.

**For Matt to rule on: deliberate or accidental?** Neither wording was changed.

> Worth recording: a first pass of the scanner here counted "Not sure yet" as *absent* from the
> SEMH files and came within one step of reporting a false safeguarding finding — the escape hatch
> looked missing from exactly the route that needs it most. The instrument was wrong, not the pack.

## A10.4 — the pathway vocabulary collision. Placeholder, no invented mapping.

These files use **"Pathway A — Standard Transitions"** and **"Pathway B — Specialist / SEMH"**,
with **zero** occurrences of BUILD, GROW or LAUNCH. Every other pupil-facing surface in the estate
uses BUILD/GROW/LAUNCH.

The route names were **not** renamed: the whole school is an SEMH provision, so "Pathway A —
Standard" may describe a cohort that does not exist there. That is a curriculum judgement.

`index.html` now carries a clearly-marked **PLACEHOLDER** section for how the two vocabularies
relate, stating that it awaits Matt's own words and must not be filled in from anywhere else.

**AMBER — this is the one item that needs Matt before the pack is shown to colleagues.**

---

## §3.1 — what the hub now says, and the honest limits

Three statements were added to `index.html` because they are the things most likely to be
misunderstood:

1. **A public website is not a fallback for an internet outage.** If the connection is down,
   `madebymatt.uk` is exactly as unreachable as PythonAnywhere. What this pack genuinely covers is
   the baseline app being down while the internet is up. *"If you have no internet at all, print
   these in advance — that is the offline route."*
2. **This is a different instrument from the baseline app.** That one is keyed to
   BUILD/GROW/LAUNCH across seven assessment IDs; this one is Reading & Writing / Maths / Science
   across two routes. **Results are not interchangeable and must not be entered into the app's
   database as if they were.** No attempt was made to reconcile them.
3. The answer-key disclosure (A10.1).

**No W3 lesson links either baseline.** The route hubs link `Baseline_Weeks/` as a resource; no
lesson cites it as prior learning, because these HTML assessments are not necessarily what any
given pupil sat.

## Two AMBERs that are not mine to resolve

- **Reading & Writing is a colleague's subject**, and the school already baselines reading through
  its own assessment. Publishing a Made by Matt reading baseline alongside it is a scope question,
  not a technical one.
- **Maths is a colleague's subject** on the same grounds.

Both recorded by name; neither acted on.
