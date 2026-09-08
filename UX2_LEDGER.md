# UX2 ledger — Lessons

Order UX2 (2026-09-08), Parts A and D. Every link, section, control, menu item,
pack file and route the order touched ends here as **SURVIVES**, **RELOCATES**
(named destination) or **RETIRED** (reason). Nothing is silently dropped.
Auto-decisions this order left open are logged at the end.

## Part A — the hub and the subject page

### The old hub (`/Lessons/index.html`, 64,234 B, measured in A0)

| item | verdict |
|---|---|
| Canonical platform header (`mbm-site-header`: brand, Menu, primary links Games · Lessons · Apps · Tools · Resources, More, Display) | SURVIVES — byte-identical to main (the shared contract gate pins the brand markup, small line included). The publisher replaces `<header>` with the unified menu; nothing the hub needs lives inside it. |
| Skip link `#main` | SURVIVES |
| Breadcrumb Home → `/main/` · All resources → `/resources/` · Teacher tools → `/tools/` | RETIRED (row) — `/resources/` and `/tools/` SURVIVE in the header's primary links; `/main/` is overlaid by the homepage in the education build and the brand already links home |
| Eyebrow "Made by Matt · Teaching collection", h1 "Find your next lesson.", lead | RETIRED — replaced by h1 "Lessons" + S1 "Lessons for BUILD, GROW and LAUNCH pathways." (Appendix A) |
| `#count` "N of M resources" | SURVIVES — derived count line "<M> resources · <S> subjects" in browse; "N of M resources" in results |
| Journey tiles BUILD / GROW / LAUNCH (hidden) + `#jkey` | RETIRED — the pathway control is the subject page's segmented control |
| Year tabs 2026–27 / 2025–26 / Everything | RETIRED — "Pathways/Collections tabs NOT built"; every year renders; `?year=` is accepted and ignored |
| Toolbar: Search | SURVIVES — `#search` in the hub bar, same behaviour (flat results, `#status` "Showing n matching resources.", Clear filters) |
| Toolbar: Subject select, Pathway select, Term, Collection, Type, Teaching style | RETIRED — subject cards + the subject page's pathway control and format chips replace them; old query URLs (`?subject=…&pathway=…`, `?view=…`) still resolve on the hub |
| Catalogue shortcut links (All LAUNCH Science, LAUNCH Science pack, BUILD Science, GROW Science) | RETIRED — pathway deep links into the Science shelf; the shelf is a catalogue row on the Science page's Suites row and the pathway control replaces the query. The shelf itself SURVIVES as a static link in the Subjects section head, "Science by pathway and term" (the shelf page's own title; A5) |
| Catalogue shortcut links (Science / Humanities teaching packs, Editable teaching packs · 7 subjects) | RELOCATES — each subject's pack hub is a catalogue row (`…/Teaching_Packs/index.html#build/#grow/#launch`) on its subject page's Suites row; the all-subjects landing (`Teaching_Packs/`) has no catalogue row and is retired (reason recorded in `tools/ux2/fixtures/retired-hrefs.json`) |
| Catalogue shortcut links (Humanities & RE, Art & Arts Award) | RELOCATES — subject cards HUMANITIES & RE and ART STUDIO. The Humanities shelf (`Humanities_Teesside/index.html`) SURVIVES as a static link in the Subjects section head, "Humanities by pathway and term" (the shelf page's own title; A5) |
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
| Header styling (sticky navy header, brand flex layout, small-line letterspacing) and the no-JS narrow-width nav rules | SURVIVES — ported verbatim from the old hub's inline styles into `hub.css` (screen rules) and the hub's `<noscript>` block (no-JS rules); the browser matrix measures the header at 320–1440 |
| Reading themes (pink, blue, light, dark, highlumen; cream default) | SURVIVE — each page's `<style id="mbmTheme">` block carries one token rule per engine theme (the theme-parity contract); component rules stay in `hub.css`; `hub_gates.mjs` measures contrast on all six and asserts the hub's and the subject page's blocks are identical |
| Print styles | SURVIVES — hub and subject page print as a clean expanded list |
| Storage keys `mbm.lesson.saved.v1`, `mbm.lesson.recent.v1`, `mbm.lesson.return.v1` | SURVIVE unchanged |
| `assets/catalogue/catalogue.js` (term/style grouping) | RETIRED from the hub; still used by the Science and Humanities shelves |
| `assets/catalogue/lesson-navigation.js` | SURVIVES — `subject.html` added to its hub set (inserted after `index.html`: the Site publisher anchors on the set's last entry to append the Primary hubs, so the tail is unchanged); query keys `format`, `unit`, `added` carried in the return context |

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

Per-pack inventory (placed files, held files and their reasons, drift flags):
`data/companion-packs.json` (D2). The catalogue entries (D3) are DERIVED from
it by `tools/ux2/companion_catalogue.py` and appended after the reviewed hub
rows; `--check` and six red proofs run in the UX2 gates workflow, and the
shared contract gate's appended-row count and digest are re-cut from the
verified rows by `tools/catalogue/pin_catalogue_contract.py`.

| item | verdict |
|---|---|
| 65 packs (Science 48: BUILD 15 / GROW 13 / LAUNCH 20; Humanities 17: BUILD 6 / GROW 5 / LAUNCH 6) | LANDED — 363 files byte-identical to intake under each subject's Teaching_Packs convention; 27 files held at file level (5 truncated Slides.pdf; 22 Teacher docx/pdf whose body text carries OUTSTANDING_V4 / _V3_1); the pack HTML is never deployed |
| The LAUNCH Art W3 pack the Read Me claims | ABSENT from every uploaded zip — nothing landed, nothing stubbed |
| Catalogue entries | 65 rows, one per pack, `kind:"pack"`, `companionOf`, `files[]`, `builtFrom`, `packRevisionDrift` (18 true), `halfTerm` (Autumn 2 = 58, Autumn 1 = 7) |
| Pack chip on a lesson row | NOT YET — none of the 65 matched lessons has a catalogue row (the record lists each directory's START_HERE and the reviewed "Classic" lessons only), so every pack renders as its own row under its subject × pathway × half-term and the chip attaches to 0 lesson rows today; a future catalogue row for a matched lesson attaches its pack automatically (`companionOf` join) |
| The two packs that pre-date the order (BUILD Science W3A Backbones; GROW Humanities W3) | UNTOUCHED — catalogued as hub rows already; drift reported in the D2 report, not re-catalogued |
| Size (measured with `du -sb`) | Lessons working tree 924,204,578 B → 1,025,995,956 B (+101,791,378 B incl. the manifest and tools); the published `education-lessons` tree 685,727,843 B before Part D, so ≈787 MB after the 363 files land — about 213 MB of headroom under the 1 GB Pages limit; each publication tree is its own Pages site |

## Part D AUTO-DECISIONs

1. **Subject and family of a pack row** come from the catalogue row that states
   its lesson directory's convention (the START_HERE teacher row), never typed:
   Science packs read "Science · Teesside" / "Science Teesside" (four BUILD
   W14–W20 packs read the directory's "BUILD Science", two LAUNCH Autumn-2 W7
   packs "LAUNCH Science"); Humanities packs "Humanities" / "Humanities Teesside".
2. **halfTerm of a pack row** is the matched lesson's when that lesson is
   catalogued, else the pack's own term from the filename week (D2's
   tie-break rule); `unit` is copied only from a catalogued lesson, so no pack
   row carries one today.
3. **Row id** is the manifest id with `_` → `-` (`pack-launch-science-a2-w7l2`)
   because the catalogue id pattern is `^[a-z0-9-]+$`; nothing else changes.
4. **The catalogue PR touches** resources.json, the schema (own commit), the
   derivation tool, the UX2 gates workflow, the size table, the pin tool and
   the gate's re-cut literals, and this ledger — and zero files under any
   Teaching_Packs tree (GLV3 isolation asserted both ways).
5. **Type** of a pack row is `support` (the record's existing value for
   material that sits alongside a lesson); `kind:"pack"` is the discriminator
   the hub and the Resources page read.
6. **Pack rows in the shipped-tree checks.** Three checks that read the whole
   catalogue treated every row as a lesson-shaped one. Each is a scope statement,
   not a narrowing: `preserved_rows_errors()` called with no pack rows now derives
   them from this checkout's placement manifest (the Site runs
   `check_catalogue_static.py` from its pinned Lessons source and passes none, so
   the default of "no packs" read all 65 real rows as unreviewed appends); the
   Humanities shelf selection excludes `kind: "pack"` (a pack's file is a deck
   placed beside a lesson, not a shelf entry); and every pack row's file now
   carries a term-and-style evidence entry DERIVED by
   `tools/ux2/companion_catalogue.py --write` from the manifest — half-term and
   pathway from the row's own derived values, the digest the D2 manifest recorded,
   method "companion pack placement manifest" — appended in derivation order with
   the record's existing 907 entries untouched. `--check` re-derives all three.
7. **Old `?subject=` URLs keep their exact meaning.** The GLV3 exact-tree gate,
   which fires on any `resources.json` change, was the first thing to reach the
   hub's flat results since Part A replaced the old controls, and it found that
   `?subject=<a record subject string>` returned nothing: the filter matched only
   a subject card's slug, while the retired select had filtered by the record's
   own subject string. Four such strings (`Art · Teesside Studio Suite`,
   `GROW Vocational & PfA`, `LAUNCH Vocational & PfA`, `Humanities`) resolved to
   an unmapped slug that owns no rows. The hub now filters by an exact record
   subject when the value names one, and by the card otherwise — the old meaning
   and the UX2 one, in that order. Values that are not record subjects
   (`Science`, `ASDAN & life skills`) are unaffected. The GLV3 chip gate is
   re-pointed at that surface: its content — advertised == returned == the count
   derived from the record, and every GLV3 entry reachable — is unchanged, and
   the year clause goes because the results view renders every year.

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
12. **Derived-count contract re-pointed.** The shared contract gate required
    three tokens naming the old hub's year-tab and subject-chip counters. Those
    controls are retired; keeping dead functions to satisfy a grep would be a
    vacuous pass. The gate now names the two derived count expressions and the
    fetch they derive from. The Apps copy of the gate trails (see 1).
13. **Boundary list.** The order's ledger, the README, the re-pointed chip
    gate, the UX2 workflow and tools, and the three derived data files are
    listed in the gate's change boundary in the documented Ruling 6 shape (files
    that cannot change a studio's served bytes); the size table changes on
    every lesson edit and must not red the boundary.
14. **Static shelf links (A5).** The Site's static catalogue gate
    (`check_catalogue_static.py`, run by its domain-split job on the pinned
    Lessons source, not by any Lessons workflow) requires the hub itself to link
    `Humanities_Teesside/index.html` without JavaScript. A2's subject cards are
    rendered by `hub.js`, so the served hub carried no such link and Site #331
    went red on the first pin to the A2 main. The hub's Subjects section head now
    carries two static links, one per original shelf, named by the shelf pages'
    own titles ("Science by pathway and term", "Humanities by pathway and term").
    Additive: nothing else on the hub changes; the catalogue pins are re-cut. The
    ledger rows land here rather than in A5 because this file is itself a
    published file admitted in a two-state transition pair (Part A → Part D).
15. **One publication-caller digest per repository (A5).** The shared contract
    gate assumed both education publication callers advance together and pinned
    one caller digest. The UX2 pin moves (#436, #438) advanced the Lessons caller
    alone — the order writes nothing to the Apps repository — so the Site's
    catalogue contract control, which runs the Lessons copy of the gate against
    its pinned Apps checkout as kind "apps", went red on that digest. The gate
    now keys the reviewed caller digest by kind: the Lessons caller's, and the
    Apps caller's at the Site's reviewed Apps pin 924ab986. Both callers stay
    byte-pinned; neither check is weakened; moving the Site's Apps pin moves the
    Apps entry.
