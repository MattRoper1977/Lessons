# LAUNCH ASDAN Weeks 7–12 — QA report

Checked: 28 August 2026

## Scope

- 30 standalone lesson files: five strands across six chronological weeks.
- Pack Week 7 maps to Autumn 1 Week 7.
- Pack Weeks 8–12 map to Autumn 2 Weeks 1–5.
- Autumn 2 Weeks 6–7 remain reserved for the later evidence, portfolio and IQA block.

## Automated checks

- Static contract: PASS across all 30 lessons.
- Each lesson: one H1, nine slides, inherited slide-type order and exactly 40 timed minutes.
- Local links and 30-card Start Here index: PASS.
- JavaScript syntax, unique IDs and one-file offline operation: PASS.
- No external request, browser-storage, form, service-worker or evaluation pathway in lesson
  files: PASS.
- ~~No print pathway in lesson files: PASS.~~ **AMENDED — Order N6 · N3, 2026-08-28.**
  The absence of a print pathway was a *deliberate build decision*, not an oversight, and this
  line correctly recorded it. It was **overridden for portfolio reasons**: these are ASDAN
  evidence lessons and the portfolio is paper, so a pack with no route to paper cannot serve
  its own purpose. Authorised by Matt, 2026-08-28 (D3).
  The house print route (the GROW_ASDAN `@media print` donor, byte-for-byte, plus a LAUNCH
  chassis addendum neutralising `body{overflow:hidden}`, `.deck{height:100%;display:flex}`
  and `.slide{height:91%}`) is now present in all 30 lesson files. It is print-CSS only —
  no button, no `#print-area`, no `window.print` — so the *screen* claims above are untouched.
  Proven, not asserted: all 30 decks render an identical screen (every element's computed
  style and the full body text compared against the intake bytes in headless Chromium,
  30/30 identical), and all 30 print all 9 slides with ≥8,719 characters of text across a
  10-page PDF. Stripping the marked `<style id="n6-print-route">` block returns each file
  byte-identical to intake, 30/30.
- Accent text contrast: minimum checked ratio 4.96:1.
- Full browser interaction runs: 30 of 30 PASS.
- Microfilm play/pause/stop runs: one per strand, 5 of 5 PASS.
- Mobile/touch runs at 390 × 844: one per strand, 5 of 5 PASS.
- Reduced-motion run: PASS.

## Interaction and accessibility coverage

The browser suite exercised previous/next and keyboard navigation, direct slide hashes, microfilm controls, both progressive teacher models, correct/retry hinge states, all four lab routes, all three scaffold toggles, four evidence-status routes, TA Brief, five Live Loop branches, Staff Ready, Escape handling, focus return and Calm mode.

It also checked persistent runtime errors/requests, dark focus outlines, visible and named mobile toolbar controls, model-step live announcements, drawer `inert` state, focus restoration, timer stop on slide change or staff-tool opening, and prevention of duplicate slide announcements.

## Visual review

The Start Here hub, the PEQ Week 8 independent task at desktop size and the Community Week 10 decision lab at mobile size were rendered and inspected. The lesson surface remains scrollable above fixed controls at both sizes.

## Non-vacuity controls

- A deliberate 16-to-15-minute mutation was rejected by the timing gate.
- A deliberate remote-image injection was rejected by the offline gate.

## Qualification and evidence boundary

- Week 12 is an interim review and preparation for assessor review, not automatic completion.
- The PEQ route states the initial-assessment/registration gate, minimum three-person team, collaborative plan elements, two SMART goals at Level 1 and at least 10 genuine hours using the same plan.
- Scheduled lesson time, rehearsal, simulation and cross-strand activity are never automatically counted as assessed evidence.
- Evidence remains learner-owned, authentic and centre-controlled; staff support is attributed separately.
- Partner, participant, approval, response, impact and registration status are never assumed.

## Centre actions before assessment use

Recheck the live ASDAN course page and current unit booklet; confirm learner registration, level and qualification size; authorise practical work and external contact locally; map candidate evidence; and complete the centre’s assessor, IQA/EQA, safeguarding and reasonable-adjustment processes.
