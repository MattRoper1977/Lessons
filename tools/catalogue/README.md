# Lesson catalogue and subject shelves

The additive catalogue preserves resources.json and every current resource URL. It adds term and teaching-version controls to the Lesson Hub, plus static Science and Humanities shelves. Both shelves retain ordinary working links without JavaScript; filters progressively enhance them.

## Classification and coverage

Science selection remains the explicit SHELF_SELECTION.json record. Humanities selection combines all current Humanities rows in resources.json with the exact lesson rows in the nine declared pack manifests in HUMANITIES_SELECTION.json. Those manifests use both lessons and sequence arrays; singular cell and plural cells identities are resolved against the current workbook spine. Static checks fail if a declared manifest or the retained Humanities catalogue gains a route absent from the selection.

Terms come from current lesson/config/manifest declarations and resolved workbook cells. The filename week is never a calendar proof. A changed deck can retain an audited manifest binding only when the current lesson config, current exact manifest row and recorded audited outcome/objective/cell references all agree. Unprovable dates stay under Term not specified and appear in TERM_REVIEW.json, including uncatalogued subject-shelf alternatives.

The reviewed snapshot retains 734 source resource rows, 123 Science routes and 134 Humanities resources: 114 lessons and 20 schemes, hubs or references. Humanities includes 61 explicit-manifest lesson routes that were not individual resources.json rows. This improves discovery without rewriting that manifest or hiding its older alternatives. These counts describe source selection, not curriculum completion.

The refreshed Science evidence records 65 Autumn 1, 45 Autumn 2, 11 Spring 1 and two unspecified routes. The two W11 permeability lessons retain their routes and full Lundy style; their old proof hashes no longer match current source, and no exact current binding was substituted. Humanities records 78 Autumn 1, 16 Autumn 2, six Spring 1, 20 references and 14 unspecified resources. Earlier cached all-Science-term-covered reports are superseded.

## Native packs and online resources

David's native PowerPoint, Word and PDF cover packs are separate deliverables from browser/offline HTML archives. GROW has five original lesson routes, ten timetabled Monday/Tuesday periods, and ten supplemental resource pages in PR #329. Those are different counts and formats. This catalogue does not invent download URLs, modify archive builders or claim native-file validation.

## Rebuild and verification

Run after reconciling the current lesson branches, so proof hashes describe their final source:

```sh
python tools/catalogue/build_catalogue.py
python tools/catalogue/build_science_shelf.py
python tools/catalogue/build_humanities_shelf.py
python tools/catalogue/check_catalogue_static.py
NODE_PATH=/path/to/qa/node_modules node tools/catalogue/check_catalogue_dom.cjs
```

Dependencies are Python/lxml and a QA-only LinkeDOM installation; the website does not load LinkeDOM. For an isolated review tree, check_catalogue_static.py accepts --baseline-root /path/to/the/source/repository for its immutable resources.json comparison.

The isolated candidate passed 22 static and 24 DOM checks: 77 root term/style intersections, 80 Science intersections and 120 Humanities intersections, retained links, deep links, unknown-term visibility, metadata-load fallback, native control semantics and print open/restore logic. See the actual JSON reports for their source baseline and limits. These results do not establish browser rendering, physical keyboard/touch interaction or print pagination. Refresh generated files and checks after merging later lesson updates, then run the required browser/print and repository publication gates.

The subject shelves omit recreational-game navigation from their headers. Root lesson publication retains its existing education filtering. Historical resource records, calendar rulings and lesson bytes are otherwise preserved.
