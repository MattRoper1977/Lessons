# Classic slideshow chassis

This is Matt's classic full-screen slideshow layout, recovered directly from the source repository at `c4cfa942cb60735233a63aa656d94a38a6e41c8c`. It does not use the previous exemplar stylesheet.

`styles/` contains the complete first inline CSS block from one approved classic reference for each of the 12 pathway/subject families. Existing Science navigation-space and print-flow patches are included when present. Geometry, source typeface, stage boxes and family colours are retained. The manifest records the exact donor path, file hash, literal CSS hash and resulting tokens.

The styles vary by **subject as well as pathway**. Humanities uses the classic purple / pink / yellow stages; Art and ASDAN have their own existing family palettes; Science uses its scoped pathway overrides. No new brand mark was drawn. An original logo can be embedded unchanged through `logo_data_uri`.

## Interface

```python
from chassis.shell import render_shell
html = render_shell(
    {
        'id': 'lesson_id',
        'title': 'Lesson title',
        'pathway': 'BUILD',
        'subject': 'Science',
        'staff': '<p>Trusted, authored teacher guidance.</p>',
        'word_help': '<dl><dt>Term</dt><dd>Plain definition.</dd></dl>',
        'extra_css': '.subject-widget { ... }',
        'menu_href': 'START_HERE.html',
    },
    slides_html,
    print_html,
    inline_js,
)
```

Descriptive subjects are normalised: “Creative Arts” selects Art, and “ASDAN · Enterprise” selects ASDAN.

Supply complete slide elements using `class="slide"`, a `data-title`, the minutes in `data-timer`, and `data-type="ido"`, `"wedo"` or `"independent"` where appropriate. An optional `data-teacher` or `data-stage-index` connects a slide to the relevant TA guidance. The first slide is selected by the runtime; slide IDs are preserved.

The runtime exposes the familiar `showSlide`, `nextSlide`, `prevSlide`, `switchLevel`, `printPack`, `printSection` and `v5RevealNext` functions. `mbmShowSlide(index)` is an alias for zero-based navigation. `classic-slide-change` is dispatched on the document with `{index, slide}` in `event.detail`.

Print sections use the original `.print-section` and `#print-area` convention. The paired `.print-resource` and `.print-sheet` resource classes are also supported. Shared sections have no route restriction. Dedicated routes can use `data-print-route="supported|standard|stretch"`; the `print-scaffold-<route>` and `print-worksheet-<route>` IDs work automatically. Native printing defaults to Standard. Keep teacher answers out of the pupil print sections.

## Bounded adaptations

`controls.js` is a content-independent revision of the classic control approach. It retains the source function names and visible Previous / TA Brief / Cold Call / Next layout, while avoiding donor-specific quiz answers, pupil rosters, obsolete external scripts and cross-site storage. It adds keyboard-safe navigation, inactive-slide focus exclusion, native modal focus handling, opt-in stage timing, pause, word help, work export and the three print routes.

`controls.css` is the literal timer/modal block from the BUILD Science donor, allowing families that had a different older dialog implementation to share those original-looking controls. `access.css` adds minimum control sizing, mobile space, focus visibility and reduced-motion support. Content widget CSS is supplied separately; it does not replace family tokens.

Content has to provide actual learning activities, purposeful visuals, tiered tasks, a Lundy slide and corresponding pupil resources. This shell alone cannot certify curriculum, reading-level, historical contract or browser-layout compliance.

## Verification limit

Literal style equivalence, token recovery and source hashes were checked locally. The Python shell compiles and JavaScript parses. Local browser navigation was blocked by the browser security policy during this task, so no live browser rendering or accessibility claim is made by this package.
