# LAUNCH ASDAN visual upgrade guide

## Purpose

`visual-upgrade.css` and `visual-upgrade.js` are the progressive-enhancement layer for the complete LAUNCH ASDAN suite. They strengthen visual hierarchy, teacher-led pacing, interaction-state clarity, keyboard access, reduced-motion behaviour and print stability without replacing the existing v5 lesson chassis or changing curriculum content.

## Integration contract

All 38 HTML entry points load both shared assets. Files at the root of `LAUNCH_ASDAN/` use `visual-upgrade.css` and `visual-upgrade.js`; strand pages one directory deeper use `../visual-upgrade.css` and `../visual-upgrade.js`.

The shared layer must remain additive:

- preserve every existing word, question, answer, instruction, link and activity sequence;
- keep strand palettes and existing CSS custom properties authoritative;
- keep all existing navigation, timers, print controls, answer reveals and teacher controls;
- avoid frameworks and external animation dependencies;
- communicate state through structure, border treatment, symbols and accessibility attributes rather than colour alone;
- keep runtime announcements non-visible and meaning-neutral.

## Navigation and lifecycle rule

Slide entry is detected only when the original lesson code changes the `active` class. Shared presentation classes such as `vu-ready`, `vu-entering` and `vu-motion-settled` must never trigger another slide synchronisation.

The observer compares the old and new `active` state and batches one update into the next animation frame. This prevents the recursive class-mutation loop that previously reset reveal states continuously and could make navigation unresponsive.

Reveal hiding is scoped to the short `vu-entering` phase. If JavaScript is unavailable or stops during initialisation, lesson content remains visible.

## We Do interaction policy

Existing authored interactions remain authoritative. The shared layer adds progress feedback to matching, presentation-card, sentence-highlighting and staged-reveal activities.

Where a We Do slide contains several suitable static teaching cards and no authored activity to track, those cards become teacher-controlled checkpoints. Clicking, tapping, Enter or Space marks a point as discussed. A compact progress rail shows class progress without adding or changing lesson wording.

Do not use checkpoints for pupil assessment, scoring or evidence. They are temporary classroom pacing controls only and reset when the page is reloaded.

## Motion policy

Motion is tied to the active teaching slide. Off-screen slides are paused. Authored SVG illuminators replay when their slide becomes active, receive one short diagram spotlight, and settle after the teaching window. Continuous decorative motion is not introduced.

`prefers-reduced-motion` removes reveal movement and collapses animation and transition durations. Print output suppresses motion, transient progress controls, state symbols and shadows.

## Accessibility behaviour

The script is guarded and idempotent. It adds keyboard activation to known non-native clickable controls, synchronises pressed, current, revealed and validation states, marks inactive slides as hidden from assistive technology, and announces slide and interaction changes through a visually hidden polite live region. Existing native semantics are retained.

## Maintenance checklist

1. Keep both shared references in every new LAUNCH ASDAN HTML entry point.
2. Use existing strand variables before adding any new colour value.
3. React only to a genuine change in the original `active` slide state.
4. Prefer one short reveal or state transition to looping motion.
5. Test next and previous navigation at desktop and narrow widths.
6. Test matching, highlight, presentation-card and checkpoint activities with pointer and keyboard input.
7. Test printing and `prefers-reduced-motion` mode.
8. Run `node --check LAUNCH_ASDAN/visual-upgrade.js`, inline-script syntax checks, HTML parsing, local-reference checks and `git diff --check` before publication.
9. Confirm visible lesson text is unchanged whenever the shared layer is revised.
