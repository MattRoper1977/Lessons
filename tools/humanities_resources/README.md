# David's Humanities and RE cover version

This additive publication uses the final reviewed native content for 25 cover
periods in Autumn 1, Weeks 3–7. BUILD and GROW each have five Humanities and five
separate RE periods. LAUNCH has five integrated Humanities/RE periods. Every
period is 40 minutes. Together these map to 30 existing routes; this does not
claim any new coverage cell or qualification credit.

The complete native source pack stays preserved. Its SHA-256 is
`90a0ad96b9771d8dd04db9cd287dbe9af9e1a64c56167737edd5852b43b9eb43`.
The website offers three complete pathway ZIPs, each under 10 MB. Each ZIP
contains every original member for that pathway plus the two shared starting
guides. They keep the original folder names so all three can be extracted into
the same place. Only the outer ZIP container is rebuilt; no Office or PDF
member is changed or regenerated. The immutable member manifest binds all 132
original files, and the three archives must collectively preserve them all.
The 25 editable PowerPoints, 25 pupil PDFs, 15 shared weekly teacher-plan PDFs
and teaching guide are also available separately. Their bytes must match the
same reviewed original members exactly.

The website pages have eight timed stages, direct week navigation, pupil
responses, deliberate answer reveals and closed teacher guidance. Pupil writing
lasts only while the current page stays open and is not stored or transmitted.
Without JavaScript, all stages and the native disclosures remain usable.
Printing the website page hides teacher guidance, answer reveals and model
answers. The reviewed pupil PDFs remain the principal classroom handouts.

## Rebuild and static acceptance

```sh
python tools/humanities_resources/build_resources.py --root . --native-zip /path/to/David_Humanities_RE_OneDrive_Pack.zip
python tools/humanities_resources/check_resources.py --root . --report tools/humanities_resources/STATIC_CHECK_RESULTS.json
```

For an isolated payload, pass `--reference-root /path/to/current/Lessons` to the
checker. It checks the existing 30 lesson identities there without writing to
them. The generator writes only this new cover directory and its own download
manifest. `CONTENT.json` is bound to the final reviewed native-content digest;
changing the source cards or tasks requires a deliberate new review.

## Browser and print acceptance

The supplemental `browser_checks.cjs` is designed for the existing installed CI
driver in `tools/easter/science_original_browser.cjs`. It does not start a
browser. After the existing GROW supplemental call, the driver calls:

```js
await require('../humanities_resources/browser_checks.cjs').run({browser, root, out, configure, measured, report});
```

The supplement checks all 25 pages on desktop and phone: full stage navigation,
focus, touch targets, pupil responses, answer reveals, week links, 40-minute
timing, and local downloads. Five representative periods also run without
JavaScript. Negative controls plant an incorrect duration and a print leak.

Its 25 actual Chromium pupil-PDF exports are added to the parent driver's
`report.pdfs`, so the existing `science_print_review.py` renders and checks every
page. After that reviewer, run:

```sh
python tools/humanities_resources/check_print_content.py --artifacts "$RUNNER_TEMP/science-review"
```

Archive `humanities-cover-browser.json`, `humanities-cover-print-content.json`,
the screenshots, PDFs and every rendered page image with the existing browser
evidence. Inspect the new screenshots and print-page images before publishing.
Static success alone is not a claim that the browser or visual review passed.

## Integration boundary

Add the cover index to the Humanities shelf and lesson-hub discovery surfaces.
Keep the existing school-plan routes intact; their paths, cells and hashes are
recorded in `SOURCE_MANIFEST.json`. The resource pages link back to those routes,
and the full catalogue remains reachable from the shared lesson-hub link.
No Science, Arts Award, games, frozen-W7 or campaign coverage records are edited
by this payload.
