# GROW ASDAN visual and interaction upgrade guide

## Purpose

`visual-upgrade.css` and `visual-upgrade.js` form a progressive-enhancement layer for the full GROW ASDAN suite. They improve teacher-led interaction, visual explanation, keyboard access, responsive delivery and purposeful motion without replacing the existing lesson chassis or changing approved ASDAN/PEQ content.

## Content contract

The authored lesson files remain the source of truth. The shared layer must preserve:

- every question, answer, example, instruction and success criterion;
- learning outcomes, assessment language and evidence requirements;
- lesson order and activity order;
- external links, branding, approved colours, print packs, timers and teacher controls.

New runtime text is limited to non-visible accessibility announcements and neutral interaction-state labels. The matching connection trail repeats existing card and target text; it introduces no new teaching claim.

## Entry-point references

All 24 HTML entry points load the shared files. Root files use:

```html
<link rel="stylesheet" href="visual-upgrade.css">
<script src="visual-upgrade.js" defer></script>
```

Pages one folder below the suite root use `../visual-upgrade.css` and `../visual-upgrade.js`.

## Pass 1 — We Do interactions

The 18 lessons contain 36 We Do slides in two consistent activity families.

### Discussion and reveal cards

Each of the 18 first We Do activities keeps its original `presTap()` and `presReset()` behaviour. The shared layer adds:

- a compact progress rail;
- numbered discussion-point controls for keyboard or pointer focus;
- a dice control that selects an unrevealed card without revealing it, supporting talk-before-tap and teacher-led turn taking;
- visible completion marks;
- click-order badges on genuine ordering activities.

The controls are temporary classroom pacing aids. They do not score pupils, change answers or create assessment evidence.

### Matching and WAGOLL activities

Each of the 18 second We Do activities keeps its original matching logic, score, reveal controls and WAGOLL model. The shared layer adds:

- selected-card focus and reduced visual competition from other cards;
- tick, cross, double-border and dashed-border state cues that do not rely on colour alone;
- a responsive progress rail;
- a connection trail that retains each completed pair using the exact existing card and target wording;
- keyboard activation for non-native matching controls;
- polite, non-visible state announcements.

## Pass 2 — CSS and SVG motion

Motion is tied to teaching purpose and active-slide state.

- Off-screen slide animations are paused.
- Authored illuminator SVGs replay when their slide becomes active.
- Clicking, tapping, Enter or Space on an illuminator replays it for explanation.
- A short light sweep gives the diagram one teaching spotlight.
- Repeating decorative motion settles after approximately six seconds.
- The existing authored SVG classes and strand palettes remain authoritative.

`prefers-reduced-motion` removes shared reveal movement and diagram sweeps. Print output suppresses all shared transient controls, motion and shadows.

## Navigation lifecycle

The observer compares the previous and current `active` class state. It reacts only when the lesson's original navigation genuinely changes the active slide and batches one synchronisation into the next animation frame.

Shared entry, motion and activity classes must never recursively trigger another navigation pass. Reveal hiding is limited to the short `grow-entering` state so content remains visible if enhancement JavaScript is unavailable.

## Maintenance checklist

1. Keep both shared references in every new GROW ASDAN HTML entry point.
2. Preserve authored content exactly unless a separately approved curriculum change is made.
3. Prefer interaction that reveals relationships, sequence or class progress over points and rewards.
4. Use existing CSS custom properties before adding colours.
5. Keep diagram movement short, replayable and connected to explanation.
6. Test Previous and Next navigation, keyboard operation and 390px-wide controls.
7. Test all `pres-card`, matching, reset, reveal and WAGOLL states.
8. Test `prefers-reduced-motion` and print output.
9. Run HTML parsing, exact content round-trip, local-reference, inline JavaScript, shared JavaScript and `git diff --check` validation before publication.
