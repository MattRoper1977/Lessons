# UX2 ledger — Lessons

Order UX2 (2026-09-08), Parts A and D. Every link, section, control, menu item,
pack file and route the order touched ends here as **SURVIVES**, **RELOCATES**
(named destination) or **RETIRED** (reason). Nothing is silently dropped.
Auto-decisions this order left open are logged at the end.

## Part A — the hub and the subject page

### The old hub (`/Lessons/index.html`, 64,234 B, measured in A0)

| item | verdict |
|---|---|
| Canonical platform header (`mbm-site-header`: brand, Menu, primary links Games · Lessons · Apps · Tools · Resources, More, Display) | SURVIVES — byte-shaped contract kept; the brand's small line reads "Lessons" (the tagline is footer-only). The publisher replaces `<header>` with the unified menu; nothing the hub needs lives inside it. |
| Skip link `#main` | SURVIVES |
| Breadcrumb Home → `/main/` · All resources → `/resources/` · Teacher tools → `/tools/` | RETIRED (row) — `/resources/` and `/tools/` SURVIVE in the header's primary links; `/main/` is overlaid by the homepage in the education build and the brand already links home |
| Eyebrow "Made by Matt · Teaching collection", h1 "Find your next lesson.", lead | RETIRED — replaced by h1 "Lessons" + S1 "Lessons for BUILD, GROW and LAUNCH pathways." (Appendix A) |
| `#count` "N of M resources" | SURVIVES — derived count line "<M> resources · <S> subjects" in browse; "N of M resources" in results |
| Journey tiles BUILD / GROW / LAUNCH (hidden) + `#jkey` | RETIRED — the pathway control is the subject page's segmented control |
| Year tabs 2026–27 / 2025–26 / Everything | RETIRED — "Pathways/Collections tabs NOT built"; every year renders; `?year=` is accepted and ignored |
| Toolbar: Search | SURVIVES — `#search` in the hub bar, same behaviour (flat results, `#status` "Showing n matching resources.", Clear filters) |
| Toolbar: Subject select, Pathway select, Term, Collection, Type, Teaching style | RETIRED — subject cards + the subject page's pathway control and format chips replace them; old query URLs (`?subject=…&pathway=…`, `?view=…`) still resolve on the hub |
| Catalogue shortcut links (All LAUNCH Science, LAUNCH Science pack, BUILD Science, GROW Science) | RETIRED — pathway deep links into the Science shelf; the shelf is a catalogue row on the Science page's Suites row and the pathway control replaces the query |
| Catalogue shortcut links (Science / Humanities teaching packs, Editable teaching packs · 7 subjects) | RELOCATES — each subject's pack hub is a catalogue row (`…/Teaching_Packs/index.html#build/#grow/#launch`) on its subject page's Suites row; the all-subjects landing (`Teaching_Packs/`) has no catalogue row and is retired (reason recorded in `tools/ux2/fixtures/retired-hrefs.json`) |
| Catalogue shortcut links (Humanities & RE, Art & Arts Award) | RELOCATES — subject cards HUMANITIES & RE and ART STUDIO |
| Views: Browse all / Recommended versions / Saved lessons (+ saved count) | RELOCATES — hub bar controls "Saved <n>" and "Recommended" (B1's header controls, delivered here); `?view=saved` / `?view=recommended` unchanged |
| Recently opened | RELOCATES — shown at the top of the Saved view |
| Subject chips `#quicknav` + the 23/23 chip gate | RETIRED (chips) — the gate is RE-POINTED at the subject page's format chips (`tools/verify_lessons_chips.mjs`) |
| Legend (format icons) | RETIRED — every row states its format in text (INTERACTIVE · PPTX · DOCX · PDF) and every card carries a text badge |
| `#cards` lanes (BUILD / GROW / LAUNCH / RESOURCES) with per-subject accordions and term/style batches | RELOCATES — the subject page (subject × pathway × half-term/unit or family rows) |
| Art suite callout + 60-second YouTube tour | RETIRED — the callout's four buttons became the Art page's pathway control; the click-to-load YouTube iframe is a third-party load on a pupil surface (0 third-party rule) — the URL `https://youtu.be/vhuk-K_wWas` is recorded here for the teacher page |
| "Science 2026-27 · 40-minute routes" card (three suite indexes) | RELOCATES — the Science page's Suites row (the three `v3_40min/index.html` rows are catalogue rows) |
| "Latest additions" (12, `added` desc) | RETIRED — replaced by "Added this half-term" (top 6 within the current half-term per the spine, "See all →" to the full list); `new:` is read nowhere |
| "From Matt" aside + mailto | RETIRED — maker voice belongs on the site homepage's maker panel (B2); the contact mailto SURVIVES in the footer |
| Footer "Made by Matt · Learn • Build • Explore" + "Single-file · offline-first · hand-built in Teesside" + contact | SURVIVES as F1 "Made by Matt · Lessons" with the tagline as its small line; contact line kept; no version, no Ko-fi |
| Print styles | SURVIVES — hub and subject page print as a clean expanded list |
| Storage keys `mbm.lesson.saved.v1`, `mbm.lesson.recent.v1`, `mbm.lesson.return.v1` | SURVIVE unchanged |
| `assets/catalogue/catalogue.js` (term/style grouping) | RETIRED from the hub; still used by the Science and Humanities shelves |
| `assets/catalogue/lesson-navigation.js` | SURVIVES — `subject.html` added to its hub set; query keys `format`, `unit`, `added` carried in the return context |

### New surfaces

| item | where |
|---|---|
| Hub: hub bar (search, Saved, Recommended) · S1 · tiles T1/T2 · "Added this half-term" · Subjects (4 fixed cards + one card per unmapped subject string) · F1 | `index.html`, `assets/catalogue/hub.css`, `assets/catalogue/hub.js` |
| Subject page: "← Lessons" · search · icon + name · S2 · Suites row (catalogue hub rows) · BUILD \| GROW \| LAUNCH (+ All only when a row has no pathway) · format chips · "<units> units · <lessons> lessons" · accordion (half-term · unit rows in spine order, then family rows A–Z) · lesson rows with Open/Download, Save, Pack chip · "Show <n> more" · Planning and evidence → (only from `data/planning-keys.json`) · scroll-to-top · print | `subject.html` |
| Pack sheet (dialog: Teach / Teacher / Pupil, drift note, Open/Download, Esc/×, focus trap and return) | `assets/catalogue/hub.js` |
| Published spine `data/calendar-spine.json` (derived from `_sownb/CALENDAR_2026_27.json`) | `tools/ux2/build_spine.py` |
| Size table `data/resource-sizes.json` | `tools/ux2/resource_sizes.py` (README "Resource sizes") |
| Gates | `tools/ux2/hub_gates.mjs`, `tools/verify_lessons_chips.mjs`, `tools/catalogue/check_catalogue_dom.cjs`, `tools/catalogue/verify_education_navigation.cjs`, `.github/workflows/ux2-gates.yml` |

## Part A1 — the tags

`halfTerm` on 411 lessons (Autumn 1 371, Autumn 2 40) and `unit` on 35, from the
named sources only; 464 lessons resolving to Autumn 2026 have no unit source and
are the worklist. The Science family manifests' `topic` is a per-lesson topic
(recorded, not used as a unit). Full census: `tools/ux2/unit_tags.py --report`.

## Part D — companion packs

See the D2/D3 pull requests and `data/companion-packs.json` for the per-pack
inventory (placed files, held files and their reasons, drift flags).

## AUTO-DECISIONs

1. **A1 tags on original rows.** The shared contract gate digest-locks the 734
   original rows. The two additive keys are stripped before hashing so every
   other byte stays locked (proved red on a title edit, an unknown key, a
   removal, a reorder, and a tag plus an edit). The Apps repository's copy of
   the gate is not written by this order (Appendix B), so it trails; an Apps
   PR is needed before the estate pin tools will accept the copies as equal.
2. **Unit source.** `manifest-v3.json` `topic` is one topic per lesson, not a
   unit; the unit comes from the scheme-of-work weekly row a lesson quotes
   verbatim, via that strand's grid row for the half-term.
3. **LIFESKILLS membership** matches ASDAN / PSHE / FoodWise / D&T / lifeskills
   / Vocational / PfA on the subject OR family string (the subject strings are
   "BUILD/GROW/LAUNCH Vocational & PfA"; their families carry the programme).
4. **"All" segment** appears only when a subject has rows with no derivable
   pathway (Science: Primary Science and the legacy library; extras). It shows
   only those rows, so every entry has exactly one subject × pathway path.
5. **Units line** reads "<n> units · <m> lessons" and drops the units part when
   no row on the page carries a unit (a zero would be a derived value but not a
   useful one).
6. **Format tiles** open the hub's existing flat-results path with
   `?format=html` / `?format=packs` (file-extension classes; packs = pptx +
   docx + companion-pack entries). No new engine.
7. **Sizes** are a committed derived file regenerated by
   `tools/ux2/resource_sizes.py` and checked by the UX2 gates workflow; the
   publisher is immutable and never edits source, so "before publish" means
   "in the pull request that changes the file".
8. **Header controls.** The publisher replaces `<header>` on `/Lessons/`, so
   the search field and the Saved/Recommended controls live in a hub bar
   directly under it.
9. **Focus after load** lands on the first format tile (hub, browse view), the
   first result (hub, results view) or the selected pathway tab (subject page)
   — named controls that do not raise a keyboard on a phone.
10. **Extras' descriptions.** Appendix A names copy for the four fixed cards
    only; an unmapped subject's card shows its name, chips, badges and
    "Browse <Name> →" without invented copy.
11. **Retired from the linkedom catalogue check:** the metadata-failure and
    "alternative version" cases tested the retired term/style filter chain.
