# LAUNCH ASDAN visual upgrade guide

## Purpose

`visual-upgrade.css` and `visual-upgrade.js` form a progressive-enhancement layer for the complete LAUNCH ASDAN suite. They strengthen visual hierarchy, teacher-led pacing, interaction-state clarity, keyboard access, reduced-motion behaviour and print stability without replacing the existing v5 lesson chassis or changing curriculum content.

## Integration contract

All 38 HTML entry points load both shared assets. Files at the root of `LAUNCH_ASDAN/` use `visual-upgrade.css` and `visual-upgrade.js`; strand pages one directory deeper use `../visual-upgrade.css` and `../visual-upgrade.js`.

The shared layer must remain additive:

- preserve every existing word, question, answer, instruction, link and activity sequence;
- keep strand palettes and existing CSS custom properties authoritative;
- keep all existing navigation, timers, print controls, answer reveals and teacher controls;
- avoid frameworks and external animation dependencies;
- put state information into structure, border treatment and accessibility attributes rather than colour alone;
- keep runtime announcements non-visible and meaning-neutral.

## Motion policy

Motion is tied to the active teaching slide. Off-screen slides are paused, visual elements reveal in a short controlled sequence, and continuous decorative motion settles after a brief teaching window. `prefers-reduced-motion` removes reveal movement and collapses animation and transition durations. Print output suppresses all motion and shadows.

## Accessibility behaviour

The script is guarded and idempotent. It adds keyboard activation to non-native clickable controls, synchronises common pressed, revealed and hidden states, marks inactive slides as hidden from assistive technology, and announces slide and interaction changes through a visually hidden polite live region. Existing native semantics are retained.

## Maintenance checklist

1. Keep both shared references in every new LAUNCH ASDAN HTML entry point.
2. Use existing strand variables before adding any new colour value.
3. Prefer a short reveal or state transition to looping motion.
4. Test keyboard focus, answer and hint states, timers, printing and reduced-motion mode.
5. Run `node --check LAUNCH_ASDAN/visual-upgrade.js` and the repository's available HTML and asset checks before publication.
6. Confirm visible text is unchanged whenever shared references are added to generated lesson pages.
