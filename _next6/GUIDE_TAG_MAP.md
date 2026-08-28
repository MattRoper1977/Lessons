# N6-F §F3.3 — Guidance toggle: the map

**Nothing in this document has been applied. No file was patched.** This is the
survey the toggle would need before anyone writes a patcher for it.

---

## Why the PH-3 patcher cannot do this job

PH-3 finds staff-facing guidance by looking for `.li-box`, `.task-box` and
`.wit-panel`. Measured across all 192 files in the twelve packs:

| PH-3 selector | files carrying it |
|---|---|
| `.li-box` | **0 / 192** |
| `.task-box` | **0 / 192** |
| `.wit-panel` | **0 / 192** |

Not one. Every file therefore falls through PH-3's classifier and is filed as
chassis doc — which is why the toggle appears to have nothing to do here while
in fact having 1,840 elements to consider. This is a false negative across the
whole estate, not a coverage gap at the edges.

These packs are built on a different chassis. Its guidance lives in `.ta` /
`.ta-card`, `.staff-card`, `.note`, `.scaffold`, `.model-step`, `.good` and
`.evidence-note`, with route metadata in `.route`.

---

## What each real selector carries

Counts are elements whose visible text matches a staff-facing marker (TA,
teaching assistant, staff, teacher, adult, prompt, model this, say:, ask:,
check for, watch for, if the pupil, scribe, supervis…). `.route` is counted in
full, because every route box is route metadata whether or not it addresses an
adult.

| selector | files | staff-facing elements | what it holds |
|---|---|---|---|
| `.route` | 151 | **1,049** | Supported / Standard / Stretch route metadata |
| `.note` | 132 | **281** | rationale and caution addressed to the adult |
| `.ta` / `.ta-card` | 108 | **177** | the TA brief: prompt ladders, what to wait for |
| `.model-step` | 150 | **124** | step-by-step teaching sequence |
| `.good` | 157 | **99** | authorship and evidence-integrity reminders |
| `.scaffold` | 108 | **56** | the scaffold text revealed behind a route button |
| `.staff-card` | 18 | **36** | least-prompt-first ladder, GROW_ASDAN only |
| `.evidence-note` | 18 | **18** | what does and does not count as evidence |
| | | **1,840 total** | |

## Per pack

| pack | files | `.ta` | `.staff-card` | `.note` | `.scaffold` | `.model-step` | `.good` | `.evidence-note` | `.route` |
|---|---|---|---|---|---|---|---|---|---|
| BUILD_ASDAN/Autumn2_W1-W6_2026-27 | 28 | 0 | 0 | 0 | 0 | 35 | 63 | 0 | 288 |
| GROW_ASDAN/Autumn2_W1-W6_2026-27 | 22 | 0 | 36 | 181 | 18 | 20 | 27 | 18 | 72 |
| LAUNCH_ASDAN/W7-W12_2026-27 | 32 | 72 | 0 | 0 | 0 | 45 | 0 | 0 | 90 |
| Science_Teesside/Build/W8-W13_2026-27 | 15 | 12 | 0 | 12 | 0 | 4 | 0 | 0 | 132 |
| Science_Teesside/Grow/W8-W13_2026-27 | 16 | 12 | 0 | 7 | 2 | 3 | 0 | 0 | 145 |
| Science_Teesside/Launch/W8-W13_2026-27 | 21 | 18 | 0 | 16 | 0 | 6 | 2 | 0 | 216 |
| Humanities_Teesside/BUILD_W9-W14_2026-27 | 8 | 6 | 0 | 25 | 18 | 0 | 0 | 0 | 18 |
| Humanities_Teesside/GROW_W9-W14_2026-27 | 8 | 18 | 0 | 0 | 1 | 0 | 0 | 0 | 16 |
| Humanities_Teesside/LAUNCH_W9-W14_2026-27 | 9 | 0 | 0 | 22 | 17 | 2 | 0 | 0 | 18 |
| Art_Teesside/Build/Spring2_2026-27 | 11 | 13 | 0 | 6 | 0 | 3 | 3 | 0 | 18 |
| Art_Teesside/Grow/Spring2_2026-27 | 11 | 13 | 0 | 6 | 0 | 3 | 2 | 0 | 18 |
| Art_Teesside/Launch/Spring2_2026-27 | 11 | 13 | 0 | 6 | 0 | 3 | 2 | 0 | 18 |
| **total** | **192** | **177** | **36** | **281** | **56** | **124** | **99** | **18** | **1,049** |

The distribution is not even, and that matters for anyone scoping the work.
BUILD_ASDAN has no `.ta` at all and 288 route boxes; LAUNCH_ASDAN is the
opposite, 72 TA cards and 90 routes; GROW_ASDAN is the only pack using
`.staff-card` and `.evidence-note`, and it holds 181 of the 281 `.note`
elements on its own. A single hide-set will behave differently in each.

---

## Worked example

From `LAUNCH_ASDAN/W7-W12_2026-27/lessons/PEQ/PEQ_W7_What_Makes_a_Team_Effective_…_LAUNCH.html`.

**Would be tagged and hidden — `.ta-card`, addressed to the adult:**

> **Priority now** — Protect the distinction between access support and supplying
> examples: cue the learner's own episode, wait, and let the learner decide how
> each item is classified.

A pupil reading that learns nothing about the task and something about how they
are being managed. It is written for the person standing next to them.

**Would stay visible — `.route`, addressed to the pupil:**

> **◆ Supported route** — Complete the core routine with agreed reading, sensory,
> motor or communication access.
> 🧰 Scaffold: Decision/action → evidence → reason → limitation → next step.

The route box tells a pupil which version of the task is theirs. Hiding it would
remove the thing that makes the lesson navigable, and would take the `.scaffold`
text with it — the scaffold is nested *inside* the route box, not beside it.

**Untouched either way — `.task`:**

> **Quiet retrieval** — Locate or describe one genuine previous decision, action,
> draft, observation or feedback item that can help today.

---

## What this implies for a hide-set

1. **`.route` must not be in it.** 1,049 of the 1,840 elements are route boxes,
   and they are pupil-facing navigation. Including them would look like a large
   win on the counter and would gut the lessons. The remaining **791** elements
   are the honest target.
2. **`.scaffold` is nested inside `.route`.** Any rule that hides a route hides
   a scaffold as a side effect. If scaffolds are wanted in the hidden set they
   need to be addressed directly, and if they are not, a route-level rule must
   not be used at all.
3. **`.good` and `.evidence-note` are borderline.** They carry authorship and
   evidence-integrity statements. Some of that is staff instruction; some is a
   claim the pack makes to a reader about what the evidence is worth, which an
   inspector or a parent has a reason to see. These 117 elements want a ruling
   before they are tagged, not a regex.
4. **A marker attribute beats a class rename.** Tagging in place —
   `data-audience="staff"` on the existing element — keeps the additivity gate
   satisfiable, because stripping the attribute returns the file byte-identical.
   Renaming classes does not.

## Cost estimate

| item | estimate |
|---|---|
| elements in scope once `.route` is excluded | **791** across 192 files |
| files touched | 155 of 192 (37 carry none) |
| patcher | one pass, same shape as `n6_print_fit.py`: marked, idempotent, strip-reversible |
| per-pack selector variance | 4 distinct chassis dialects — the patcher needs a per-pack selector table, not one global list |
| the ruling needed first | `.good` + `.evidence-note` (117 elements): staff instruction, or public claim? |
| the ruling after that | does the toggle persist? `localStorage` is currently a gate violation under offline integrity, so this needs either a narrow exemption or a persistence-free toggle |
| gate work | the offline-integrity gate must be taught the exemption if one is granted, or it will go red on every patched file |

The mechanical part is small and well understood. The two rulings are the cost.
