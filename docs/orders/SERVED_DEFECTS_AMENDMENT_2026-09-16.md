# Amendment to the CX2 master order — two served-estate defects found on Matt's phone

**Raised:** 16 September 2026, by Matt, from the live estate on his phone, with two screenshots.
**Approved:** by Matt, in his own words, to be added to the master order and corrected.
**Governs:** `docs/orders/CX2_FINISH_2026-09-15.md`. Nothing in the original order is withdrawn. These
are additions, and they inherit its discipline in full: generated is not uploaded, merged is not
served, silence is not green, an unavailable tool is UNMEASURED and never passed, no gate is ever
skipped, disabled or weakened, and no product name, assistive-technology name, URL or curriculum
mapping is invented.

---

## D-1 — The Sugar Evidence BUILD lesson is on the wrong chassis

**Route.** `/Lessons/Science_Teesside/Build/W8-W13_2026-27/SCI_B_W8A_Sugar_Labels_Explore.html`,
served from the education domain. This is an accepted, published EDU-Q1 identity.

**What Matt saw.** The lesson opens on a bare shell: a timer pill, a row of pale pill controls
(`← Lessons`, `Word help`, `Pause`, `Tools & print`), the slide, and a footer of
`◀ Previous / TA Brief / Question / Next ▶`. He supplied the GROW Friction lesson as the example of
the correct chassis and said the colours must be BUILD's, not GROW's.

**Measured, not assumed.** A census of every `SCI_*` lesson by chassis marker shows two distinct
shells in the Science estate. The correct one carries a dark header bar with a `TEACH` control, an
XP meter, a home control, a stage-chip strip, a knowledge-organiser control, a pathway band and a
`Cold Call` footer control. **BUILD already has five lessons on it** — `SCI_B_W3_Backbones`,
`SCI_B_W4_Muscle_Pairs`, `SCI_B_W5_Right_Nutrition`, `SCI_B_W6_Balanced_Plate`,
`SCI_B_W7_Where_Food_Comes_From` — alongside the five GROW lessons `SCI_G_W3_Friction`,
`W4_Mechanisms`, `W5_Fair_Test`, `W6_Earth_And_Planets`, `W7_The_Moon`.

**So BUILD's colours on this chassis are not a design decision to be invented.** They already exist
and are already served. The BUILD W3–W7 lessons are the donor for pathway colour, and the ruling
"classroom chassis, pathway colours, familiar controls" in `LESSON_STANDARD_2026-27.md` §A.25.1 is
what this lesson currently fails.

**Required.**
1. Put `SCI_B_W8A_Sugar_Labels_Explore.html` on the same chassis as the BUILD W3–W7 lessons, in
   BUILD's pathway colours, taking the colour from those committed lessons and never from GROW's.
2. Preserve every piece of this lesson's content and behaviour: all nine stages and their order, the
   learning objective and success criteria as authored, the TA brief, the arrival and exit questions,
   the timer, `Word help`, `Tools & print`, the print and offline routes, the response modes named
   under CX2 §4.4, and the feedback card ruling under §4.3. A chassis change is not a licence to
   re-author the lesson.
3. Re-run the full acceptance this lesson was accepted under, on the actual bytes: every stage at
   320/390/768/1280, default and reduced motion, light/dark/forced colours, enlarged text, keyboard
   transitions, no-JS, print, zero serious or critical axe findings, and the §4.2 reading band as a
   gate per route.
4. Move every record the bytes move, in the same commit: the recorded content digest in
   `tools/catalogue/TERM_AND_STYLE_EVIDENCE.json`, its projection in
   `assets/catalogue/lesson-order.json`, the reviewed catalogue pins, `data/resource-sizes.json`,
   the BUILD pack `SHA256SUMS.txt` and `manifest.json`, and the Site education admission registry.
5. Publication and a served proof on the live URL before this is called done. Matt's phone is the
   witness device.

**Instrument.** Before any fix, commit a chassis census that names, for every Science lesson, which
shell it is on, with a planted-failure control. A lesson moved onto the chassis must move that
census from red to green for its own row. The census is the evidence; a screenshot is not.

**Not in scope here.** The census will name other lessons on the bare shell. Whether the rest of the
estate moves to the chassis is Matt's decision and goes on the Matt list with the count, not a
silent sweep.

---

## D-2 — The Apps estate serves the header without the Learn • Build • Explore tagline

**Route.** `madebymatt.uk/Matt-s-Apps-/` and every page the Apps publication writes.

**What Matt saw.** The unified education header renders the mark and `MADE BY MATT`, but the
`Learn • Build • Explore` tagline beneath the brand block is absent. EDU-HEADER-BRAND (CX2 §5.2)
requires it "beneath the logo/brand block as readable text" at 320 and 390.

**Root cause, proved from the repositories rather than inferred.**
- The education publication deploys **only the tree belonging to the repository that triggered it**:
  `education-publication.yml` resolves a `kind` from the triggering repository and uploads
  `domain-split/output/education-<kind>`. So `/Matt-s-Apps-/` is served by the **Apps** repository's
  own Pages deployment, not by the Lessons or Site one.
- The Apps repository pins its publisher at Site `d7e2cba6f84f28e9ffd143bc55f99d3cc0c39c15`
  (14 September 2026, 11:31), which **predates EDU-D3** (Site `a47539df`, 16 September 2026, 04:14).
- At that pin, **none** of the eight navigation templates in `domain-split/sw2/` contains the
  tagline; on Site main **all eight** do. The Apps publication therefore writes the pre-EDU-D3
  header by construction.
- The Apps publication last ran on **15 September 2026 at 15:09 UTC** (run 34985908890), so the
  bytes Matt is looking at are that build.
- Rendered check, for completeness: in a full local build at the current Site builder the tagline is
  present AND visible in the header at 390 px (a `SMALL` element, 153×15 px at y=32, `display:inline`,
  `visibility:visible`, `opacity:1`). This is not a CSS visibility defect; it is a stale publisher.

**Required.**
1. Advance the Apps repository's `education-pages.yml` publisher pin (`uses@` and `builder_ref`) to
   the current Site carrier, and re-cut the Apps caller digest that the shared cross-estate gate
   pins (`PUBLICATION_CALLER_SHA256_BY_KIND["apps"]`) from the caller file's own bytes.
2. Publish, and verify on the served bytes that the tagline is present on the Apps front door and on
   a sample of the app pages, at 320 and 390.
3. Record whether advancing the pin moves any other Apps published byte, and admit those bytes
   properly rather than quietly.

**Standing finding this exposes.** Three repositories publish three trees through one shared builder,
each pinned independently, and nothing fails when one falls behind — the estate simply serves an
older design on that path. The three publisher pins and the two copies of the shared cross-estate
gate should be reported together, with their dates, so a lagging pin is visible before a person
finds it on a phone. That report is a Matt-list item, not a silent addition.

---

## Where these sit in the order

Both are §10 estate check-over rows in shape: an instrument, a finding, a fix with a red-before and
green-after, one merge at a time, a served proof after each. D-2 is also an EDU-D3 completion row —
EDU-D3 is CLOSED on the Site, and its intent is not met on the Apps path until D-2 lands. Neither
re-opens EDU-Q1's accepted lesson content: D-1 changes the shell a lesson is mounted on, and the
lesson's words are preserved.

mbm-served-defects-amendment-2026-09-16-BOTTOM
