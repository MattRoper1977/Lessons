# ASDAN Visual Learning — deep audit and design report

**Sentinel:** `asdan-visual-learning-2026-08-05`
**Repository inspected read-only:** `MattRoper1977/Lessons`
**Baseline inspected:** `a4b19e2f32dbbf9c59a0ce16c59b5cae69c222f4`
**Scope:** every taught lesson in BUILD, GROW and LAUNCH ASDAN, including the six BUILD D&T community-upcycling decks.

No repository write, commit, push, pull request, merge or deployment is performed by this pack.

## Executive finding

The ASDAN suite already has a substantial presentation chassis: lesson navigation, timers, teacher controls, print routes, differentiation, authored We Do activities, reduced-motion treatment and three maintained shared visual layers. The highest-value next step is therefore **not another decorative overlay**. It is a disciplined visual-learning layer that makes the decision, process, evidence and independent handover visible while leaving qualification claims and portfolio decisions to authorised people.

The pack covers **85 taught lesson decks across 14 subsections**:

- BUILD: **37** — Careers 7, Living Independently 6, FoodWise 6, Community Project 6, Duke and Enterprise 6, Community Upcycling D&T 6.
- GROW: **18** — PEQ 6, Community Project 6, Enterprise 6.
- LAUNCH: **30** — PEQ 6, Careers 6, Living Independently 6, Vocational 6, Community and Enterprise 6.

Hubs, schemes, printable evidence packs, trackers, witness statements, moderation records and qualification records are protected surfaces. They are documented but are not automatically mounted.

## The OWL design lens

The user asked for the work to be considered “as an owl”. The pack turns that into a practical design test rather than a mascot:

### O — Observe the thing that matters

Before pupils read a definition, the lesson exposes the feature, action, hazard, relationship, sequence, user need, cost, evidence form or consequence that they need to notice.

A visual fails this test when it merely decorates a slide or moves attention without clarifying what should be observed.

### W — Work the information

Pupils manipulate the idea: sort it, sequence it, test one variable, open a hotspot, select evidence, compare a frozen result or locate an authorised route.

A visual fails this test when the pupil can complete it through guessing, colour matching, copying a finished answer or repeated tapping without explaining a relationship.

### L — Leave with an independent next step

The screen finishes by handing control back. It states the real task, the first step, the success check, the least-help ladder and the adult route for safety, permission, assessment or reasonable adjustment.

A visual fails this test when pupils become successful only while the scaffold is visible.

## Governing teaching cycle

All 85 lessons use:

> **Notice or predict → manipulate → freeze → point to evidence → explain → transfer**

The cycle changes by pathway.

### BUILD — SEE → CHOOSE → SAY → DO

BUILD reduces simultaneous decisions and turns abstract vocabulary into observable examples. The pupil points, places, orders or opens information, says the deciding feature and then completes a real short task.

The design floor is:

- one dominant relationship at a time;
- no drag-only completion;
- immediate corrective guidance without public scoring;
- visible model and real-task separation;
- a spoken, pointed or selected response is valid rehearsal;
- the screen never replaces the practical, spoken or portfolio task.

### GROW — PREDICT → TEST → COMPARE → JUSTIFY

GROW requires a prediction before the controls unlock. Models retain frozen results. Where a model is used, the second valid run changes exactly one variable.

The design floor is:

- prediction committed before manipulation;
- one-variable comparison;
- finite movement that stops;
- retained before/after evidence;
- justification from the frozen evidence;
- independent transfer to a new example rather than repetition of the screen.

### LAUNCH — INVESTIGATE → LOCATE EVIDENCE → REASON → ACT

LAUNCH does not open the explanation merely because the activity is complete. It requires a structured, non-sensitive evidence locator:

1. what authentic form exists;
2. where it is located;
3. which authorised route comes next.

The locator deliberately includes “not yet available” and “not yet located”. It records no grade, level, criterion achievement, portfolio state or qualification status.

When the gate opens, the panel receives only the temporary DOM marker:

```html
data-asdan-opened-by="completed activity and selected structured evidence-locator route"
```

The marker disappears on reload. It is interface provenance, not evidence.

## Why this should improve outcomes

### 1. It reduces the distance between instruction and action

Many ASDAN tasks ask pupils to convert broad ideas—reliability, communication, budgeting, community need, risk, audience, quality, reflection—into observable actions. The new layer presents the conversion explicitly:

- claim → action → result;
- need → evidence → aim;
- hazard → control → check;
- income → outgoings → balance;
- user → problem → response;
- instruction → safe sequence → quality check;
- feedback → controlled change → effect.

### 2. It supports independence without removing access

The panel does not simply remove scaffolds. It fades responsibility through a four-part handover:

1. use the frozen visual to choose a first step;
2. complete the real task without copying the screen;
3. check against visible conditions;
4. request one specific prompt or use the authorised adult route.

The help ladder begins with self-cueing and ends with the responsible adult, assessor or access route. Reasonable adjustments remain available; independence is not defined as doing everything without support.

### 3. It protects authentic evidence

The visual tool contains no upload, camera, microphone, name field, clipboard export, local storage, session storage or network call. It never asks for a real bank statement, bill, identity document, medical information, tenancy information, disclosure, named audience response or fabricated witness.

The real lesson and centre process remain the source of evidence.

### 4. It creates useful stopping points

Animations and models stop. The final state stays visible so a teacher can point, question, compare and then release pupils to work. This is more teachable than ambient glow, continuous bounce or a diagram that resets before pupils have explained it.

### 5. It makes error informative but not punitive

Incorrect choices receive a reason and another route. There are no leaderboards, public ranks, grade labels, failure sounds or loss mechanics. A wrong rehearsal answer is not evidence about a pupil.

## Activity architecture

The payload set contains:

- **26 finite models**;
- **21 evidence-selection investigations**;
- **16 sequencing activities**;
- **12 hotspot investigations**;
- **10 sorting/click-to-place activities**.

### Sorting

Click card, then destination. HTML drag-and-drop is optional, never required. Correct placement leaves a retained trace; incorrect placement gives the deciding reason.

### Sequencing

Rows use native Move up and Move down buttons. Pupils explain what must already be true before the next step. This is suitable for routines, instructions, hygiene, project plans, applications, handovers and tool processes.

### Evidence selection

Pupils select the complete set of usable evidence and reject praise, labels, guesses, unsafe shortcuts or invented records. Visual states use symbols, borders and text as well as colour.

### Hotspots

An original simplified scene holds numbered, keyboard-operable hotspots. Each opens one concise relationship. The scene remains visible after all points are opened so pupils can compare the whole system.

### Models

Pupils choose values, run a finite check and retain the result. GROW and LAUNCH require two valid runs with exactly one changed variable. Models rehearse decision structure; their output is never a grade or evidence status.

## SVG and CSS animation standard

The pack includes **85 original SVG teaching models**, one for every taught deck. Each has a stable `viewBox`, `<title>`, `<desc>`, visible text labels and a reduced-motion state.

Use animation only when it represents:

- sequence;
- flow;
- comparison;
- a controlled change;
- a route;
- a reveal tied to a question;
- a process reaching a useful frozen state.

Do not animate merely to make a slide feel active. In particular:

- move the mark, item, cost, role, route, hazard, control or evidence token—not its label;
- keep the artboard and reference objects fixed;
- stop automatically;
- retain the previous state where comparison matters;
- never hide essential content behind JavaScript;
- make replay a teacher decision;
- print no transient controls;
- provide complete static parity.

## Supplementary-content ruling

The source lessons remain byte-for-byte authoritative outside the owned mount markers. The new panel does, however, add visible task-specific prompts, examples and original models. It is therefore a **supplementary lesson resource**, not a claim that the change is presentation-only or visually inert.

That distinction governs review:

- compare the authored lesson outside the marker blocks byte for byte;
- review every payload as new supplementary teaching content;
- preserve lesson wording, answers, order, assessment language, branding and approved colours;
- reject a payload that changes the intended answer, criterion, safety route or qualification claim;
- never edit the content-integrity gate in the same commit as the content it judges.

## Integration conclusion

A competing fourth lesson framework would repeat the estate’s own failure class: two sources of truth that drift. The pack therefore extends the sources already owned by each pathway:

- BUILD: `BUILD_ASDAN/_framework/asdan-teach.css` and `.js`, then the existing `apply_framework.py`;
- GROW: `GROW_ASDAN/visual-upgrade.css` and `.js`;
- LAUNCH: `LAUNCH_ASDAN/visual-upgrade.css` and `.js`;
- BUILD D&T: six standalone decks receive one owned inline marker block because they sit outside the BUILD ASDAN compiler.

The integration generator is dry-run by default, owns only its marker pairs and invokes no Git command.

## Honest remaining gate

This pack validates its own payloads, code, SVGs, standalone demonstrations and synthetic integration. It cannot honestly claim that the complete live repository has passed after integration until the exact current checkout runs:

- the BUILD framework content-integrity and browser gates;
- the GROW and LAUNCH shared-layer checks;
- representative navigation, timers, matching, WAGOLL, answer reveal, teacher controls and print routes;
- qualification-claim, data-firewall and safeguarding checks;
- the six D&T lessons against the school’s current risk assessments and actual equipment.

Those checks are specified in `TEST_PLAN.md` and `COMMIT_READY_NOTES.md`. A truthful withheld gate is safer than a fictional pass.
