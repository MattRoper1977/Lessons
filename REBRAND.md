# REBRAND — Made by Matt → Progress Schools

**The procedure for producing a staff-facing pack from an estate file.**

This is a *procedure*, deliberately kept out of [`REGISTER.md`](REGISTER.md), which is
a set of *constraints* instruments load and assert against. A register that starts
accumulating procedures keeps accumulating them until nobody reads it.

Companion: [`REGISTER.md`](REGISTER.md) — estate conventions and exceptions ·
[`LundyLoop/tools/INSTRUMENTS.md`](LundyLoop/tools/INSTRUMENTS.md) — instruments.

**Why this file exists:** this recipe governed every staff pack ever produced and
existed nowhere in either repository. It lived in one person's head.

---

## Surface, measured at `d02ec43`

| what | files |
|---|---|
| contain `Made by Matt` | **271** |
| contain `madebymatt` (any case) | **44** |
| already name `Progress Schools` | **55** |
| carry an `x-brand` meta tag | **0** |

Forms the wordmark takes — **this is the list that gets missed**:

```
110 ×  aria-label="Made by Matt"      <- invisible to the eye, read aloud by screen readers
 83 ×  alt="Made by Matt"             <- invisible until the image fails
  1 ×  aria-label="Made by Matt collections"
  1 ×  <meta name="description" content="... from Made by Matt — ...">
```

**Do not rebrand by eye.** Roughly two thirds of the occurrences are in attributes
that never render as text. A visual check on a rebranded pack passes while a screen
reader still announces the wrong organisation.

---

## The rules

### 1 · The mark ~~is typographic~~ — SUPERSEDED 2026-08-07, the real logo now exists

**Original rule, kept because it explains the one below:** set the mark as
**text**. Do not draw a logo, do not generate an SVG mark, do not approximate one
from memory, and do not carry over the Made by Matt logo geometry with the letters
changed. If a visual mark is genuinely required, it comes from Progress
Schools — it is not produced here.

**What changed:** the last clause finally happened. Matt supplied the real
Progress Schools lockup (the P mark + wordmark), so the placeholder is retired
and the trademark replaces the Made-by-Matt mark directly. The rule's *purpose*
is unchanged and now binds harder:

- **Never recolour, restyle, stretch or redraw it.** It is embedded as supplied
  and only ever scaled by `width` with `height:auto`, so the aspect ratio cannot
  drift. A dark header gets a white chip behind the logo; the artwork itself is
  never touched.
- Optimise **one** master asset (trim, ≤10 KB, 2× display size) and embed it as a
  base64 data URI per page. No external asset file — a pack that ships an
  `images/` folder breaks the moment a page is moved, and these pages get moved.
- Where only the 64×64 mark footprint exists, crop to the P mark alone with
  `alt="Progress Schools"` and the wordmark as adjacent text.

The strip (rule 2) is still required alongside the logo. The lockup shows the
wordmark, but the strip is a separate estate convention with occurrences to match.

**The binary stays out of git. Its SHA is recorded here instead**, because a pack that
cannot be rebuilt from the repo plus a recorded hash is not reproducible:

```
logo  SHA-256  b112fd98e3368f73df4da5588a04238ee4a816b56007ba60e2e63d0286cbdb04
      225x225 PNG, the P mark + "Progress Schools" wordmark lockup
```

The builder asserts this hash before it uses the file. **Absent `--logo` is a hard stop** —
there is no fallback to the typographic mark. A pack built without the real lockup is not a
Progress Schools pack, and silently producing one is how a placeholder ends up in a school.

`tools/build_staff_pack.py --mirror --logo PATH` implements all of this.

### 2 · The strip

```
PROGRESS SCHOOLS · TEES VALLEY
```

Upper case, middle dot with a space either side. **47 occurrences of `PROGRESS
SCHOOLS` already exist** in the estate (45 bare, 2 as `PROGRESS SCHOOLS — Studio
Board`) — match them rather than inventing a variant.

### 3 · Replace every form of the wordmark, attributes included

Work through **all four** of these, in this order, because the last two are the ones
that survive a careless pass:

1. Visible text — headings, footers, body copy.
2. `alt="Made by Matt"` → the pack's own description, or `alt=""` if the image is
   decorative. **An alt attribute is not a place to put a brand name.**
3. **`aria-label="Made by Matt"`** — 110 of these. This is *the* trap. It renders
   nowhere, survives every visual check, and is read aloud.
4. `<meta name="description" ...>` and any `og:` / `twitter:` content.

### 4 · Domain wording

`madebymatt.uk` appears in 44 files. In a staff-facing pack, replace or remove it.
**Check `href` values as well as link text** — a link reading *"the pack"* pointing at
`madebymatt.uk` is still the public site.

**One exception, added 2026-08-07 on Matt's instruction:** every rebranded page
carries the credit **`by madebymatt.uk`**, small and unobtrusive, in the footer.
This is the *only* permitted Made-by-Matt string. The residue sweep whitelists it
by **exact match** and still fails on every other spelling, so the exception
cannot quietly widen into "the sweep is off". Add the credit **after** the domain
rewrite has run, or the rewrite eats it like any other mention of the domain.

**The exemption is anchored on the credit as element text**, not on the substring. Matching
the token `madebymatt.uk` on its own would pass `href="https://madebymatt.uk"` — a live link
to the public site, which is precisely what this rule exists to catch. The check deletes one
occurrence of `>by madebymatt.uk<` and then requires **zero** matches in what remains, so an
href, a `src`, any attribute value, and a second credit all still fail. Verified with a
negative control on each of those four shapes.

**Rule 4 is about the personal public site, not one spelling of it.** A repo-wide census found
four spellings, only one of which the sweep had ever known. They are now **named alternates** in
`PERSONAL_ORIGIN_FORMS`, used by both the rewrite and the verify pass so the two cannot drift:

| spelling | what it is | occurrences (repo) | ever in pack scope |
|---|---|---|---|
| `madebymatt.uk` | the custom domain, canonical | 77 | yes — swept since the first pack |
| `mattroper1977.github.io` | the Pages origin the custom domain fronts | 26 | **yes, 2 — unswept until 2026-08-07** |
| `mattroper1977.pythonanywhere.com` | the live-lessons app | 2 | no |
| `ko-fi.com/madebymattuk` | donation link on the public index | 1 | no |

Content pages now point at the **custom domain**, which collapses the Pages origin into the
spelling the sweep has always caught. Adding the next form is a one-line change.

### 5 · The `x-brand` meta tag

```html
<meta name="x-brand" content="progress-schools">
```

Add to the `<head>` of every rebranded file. **Zero files carry it today**, so it is
currently a reliable marker of *"this file has been through the rebrand"* — which is
its purpose: a rebranded pack can be identified without reading it.

Corollary: **it must be added only when the rebrand is actually complete in that
file.** A tag asserting a state the file isn't in is the failure mode this estate has
paid for repeatedly. See `REGISTER.md` on declarations that point outward.

### 6 · "Progress Schools" as plain text is fine in staff-facing content

Naming the organisation in prose needs no mark, no strip and no styling. Rule 1
constrains the *mark*, not the *name*.

### 7 · The two assessed files take a conditions-block swap, not a rebrand

`Grow/Slideshows/GROW_HUM_W7_Write_The_Account.html` and
`Launch/Slideshows/LAUNCH_HUM_W7_Source_Assessment.html` carry an Assessed Conditions
Card. In a staff pack, **swap the conditions block** rather than restyling the file.

`REGISTER.md` R-A01 binds here: support access may change, **content, outcomes and
success criteria may not** — ask first, every time. Select these two with the literal
string **`★ ASSESSED LESSON`**. The shorter `★ ASSESSED` returns six files and four of
them must not be touched.

---

## Pack scope (areas)

The builder (`tools/build_staff_pack.py`) is the executable source of truth for scope; this
section records it in prose. Scope is **complete-current**, never a git-diff.

**IN:** `Art_Teesside` · `BUILD_ASDAN` · `GROW_ASDAN` · `LAUNCH_ASDAN` · `Humanities_Teesside` (docs) ·
`Build/Slideshows/BUILD_DT_W*` · `Build/Slideshows/BUILD_HUM_W*` · `Grow/Slideshows` ·
`Launch` · `Tutor_Time` · `DT_Community_Upcycling` · **`Science_Teesside`** (the current
Teesside science suite, added PACK-1 v2) · root unit hubs (`art_teesside.html`,
`build_asdan.html`, `build_dt_upcycling.html`, `humanities_teesside.html`) ·
`LundyLoop/assets/style.css` · **the three Art visual-learning runtime assets**
(`Art_Teesside/visual-learning/art-visual-learning.css`,
`art-visual-payloads.js`, `art-visual-learning.js`) · **the four GROW/LAUNCH ASDAN
visual-upgrade runtime assets** (`GROW_ASDAN/visual-upgrade.css`, `GROW_ASDAN/visual-upgrade.js`,
`LAUNCH_ASDAN/visual-upgrade.css`, `LAUNCH_ASDAN/visual-upgrade.js`), added PACK-2.

**Why those three, and only those three.** Scope globs `*.html`, so a directory being IN
does not carry its non-HTML assets — `LundyLoop/assets/style.css` is named individually for
the same reason. All 31 Art_Teesside lesson decks now load these three files from inside an
`AVL-MOUNT` marker pair, by **relative** path (`../visual-learning/…`). Derived at
`66428e3`: 31 decks, 3 distinct references, 31 uses each, **zero absolute or protocol-relative
references**. If they do not ship, every staff copy carries a loader pointing at nothing and
the *We Do* panel silently never mounts — offline and on OneDrive, with no error a teacher
would see.

**And the same for the GROW/LAUNCH four, found by the crawl rather than by reasoning (PACK-2).**
`GROW_ASDAN` and `LAUNCH_ASDAN` are both in the IN list, but scope globs `*.html`, so neither
carried its runtime assets. The crawl over the assembled pack returned **124 references to
`visual-upgrade.css` / `visual-upgrade.js` from 62 shipping decks, resolving to nothing** — the
largest broken-link family in the pack, and the same silent failure the Art three were added to
prevent. Naming a directory IN is not the same as shipping what its decks load; **the crawl is
what catches the difference, which is why it is run over the assembled pack and not the repo.**

**OUT:** `Games` and personal apps (dual-branding rule — Made-by-Matt only) · **frozen legacy
science: `biology/`, `chemistry/`, `2 Physics 10/`** (these stay OUT even though
`Science_Teesside/` is IN) · superseded legacy art tasters (`Build/Slideshows/BUILD_ART_W\d_`) ·
old `BUILD_L1_` / `FW_L1_` · site furniture (`404.html`, root `index.html`, `hub-health`) ·
any pupil/student sheets or pupil data (never enter any zip) · **the visual-learning
directory's non-runtime contents** — `README.md` and anything else there is recovery
documentation for this repo, not something staff need in a pack. Only the three files a deck
actually loads go in. `reports/REDUCED_MOTION_REGISTER.md` and `tools/` stay OUT as before.

---

## Verification before a pack ships

Run all four. The first two are the ones a human check misses.

```bash
# 1 — no wordmark survives in ANY attribute, not just visible text
grep -rniE '(aria-label|alt|content|title)="[^"]*made by matt' <pack>

# 2 — no domain wording, in text or in href
grep -rni 'madebymatt' <pack>

# 3 — the rebrand marker is present in every file, and only where it is true
grep -rLn 'name="x-brand"' <pack>

# 4 — the strip is present and matches the estate form
grep -rc 'PROGRESS SCHOOLS · TEES VALLEY' <pack>
```

All four must be run. Rule 3's trap is that checks 1 and 2 pass a visual inspection
and fail a grep, while check 3 fails silently — a missing `x-brand` tag has no
symptom, exactly like a missing sitemap entry.

### Counts that can reach zero are not gates

The strip count silently fell to **zero** in the first mirror build: the real logo replaced the
typographic mark, and the mark had been carrying the strip. Check 4 above only asserted "at
least one file", so a run with the strip on *no* page would have passed had the assertion been
written a shade differently. Three counts are now permanently gated and the build refuses to
package if any fails:

| count | gate |
|---|---|
| strip | `> 0` |
| credit | **exactly one per page** — not "at least one", so a duplicate fails too |
| logo | equals the number of pages that carried a visible mark; and the on-disk count may not be lower |

Also gated: 0 broken internal links over the **assembled** tree, 0 inline-JS syntax errors,
0 truncated files, the ★assessed conditions blocks byte-identical, and — for a mirror-shape
pack — 0 collisions with unregenerable OneDrive-only artefacts.

### The inline-JS gate, and why `</body>` is not a safe anchor

Several decks build a printable view with `w.document.write('<html>…</body></html>')`. The
**first** `</body>` in those files is inside a JavaScript string literal. Appending anything
at it produces an unterminated string and kills the whole script block — and because the code
only runs when a teacher presses Print, opening the page from `file://` never reveals it.
Insert at the last closing tag followed by nothing but whitespace, and gate every inline
`<script>` body with `node --check`. Testing the print path means *executing* it, not loading
the page.

---

## Third-party fetches (rule 8)

**An offline pack makes no network request.** A `<link>` to a font CDN fails on a school
machine without internet and phones out on one with it — the same defect shape as the `hud.js`
loader, differing only in that it degrades quietly instead of breaking a panel.

Vendor rather than drop, unless Matt rules otherwise: fetch the CSS, keep the `latin` and
`latin-ext` subsets only (a UK pack renders no Cyrillic, Greek or Vietnamese), inline each
`woff2` as a data URI, and remove the `<link>` **and** its `preconnect` hints. Cache the files
on disk so a rebuild is not a network dependency, and **fail the build** if a font cannot be
resolved — silently leaving the link defeats the point.

A labelled link to a teaching resource (Oak National Academy) is not a fetch and stays.

## Mirror-shape packs (PACK-4)

The default build preserves the repo tree because its links assume the repo tree. A mirror
pack assembles into the school's OneDrive geometry instead — and is only safe because it does
**both halves**: assemble to the drive's shape *and* rewrite every internal link against the
same map. Zip geometry then equals drive geometry, so a link between two co-shipped folders
still resolves after a drag-and-merge. Do one half without the other and every cross-folder
link dies silently.

Three rules learned building the first one:

1. **A hub is position-dependent after a rewrite.** Never tell anyone to hand-copy a rebranded
   root hub into a subfolder: its hrefs are written for depth 0, so the copy is a branded page
   with dead links — worse than an unbranded page that works. Emit each copy at its own depth
   and crawl it **from its own location**.
2. **Flattening collides filenames.** Census every basename repeated across the folders being
   flattened *before* assembling. Renaming is reversible; overwriting is not.
3. **A page the pack authors or re-emits is a Progress Schools page.** "Only pages that
   previously carried a mark" is a rule against inventing branding on someone else's page. It
   does not cover a page this build writes, nor a hub re-emitted at a new path — those carry
   the lockup. Brand the root original too, or the two copies of a hub disagree.
4. **A merge replaces same-named files.** Where the destination holds artefacts that cannot be
   regenerated, print the collision list explicitly — **empty or not**. A silent pass is
   indistinguishable from a check that never ran.

---

## What this recipe cannot tell you

- Whether a given file *should* be in a staff pack at all. That is a content decision.
- Whether Progress Schools' own brand guidance has changed. This records the estate's
  practice, not their policy — if the two ever conflict, theirs wins and this file is
  the thing that is wrong.
- Anything about pupil-facing material. This is a staff-pack procedure only.
