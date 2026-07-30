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

### 1 · The Progress Schools mark is typographic. Never drawn, never invented.

Set it as **text**. Do not draw a logo, do not generate an SVG mark, do not
approximate one from memory, and do not carry over the Made by Matt logo geometry
with the letters changed. If a visual mark is genuinely required, it comes from
Progress Schools — it is not produced here.

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

**IN:** `Art_Teesside` · `BUILD_ASDAN` · `GROW_ASDAN` · `Humanities_Teesside` (docs) ·
`Build/Slideshows/BUILD_DT_W*` · `Build/Slideshows/BUILD_HUM_W*` · `Grow/Slideshows` ·
`Launch` · `Tutor_Time` · `DT_Community_Upcycling` · **`Science_Teesside`** (the current
Teesside science suite, added PACK-1 v2) · root unit hubs (`art_teesside.html`,
`build_asdan.html`, `build_dt_upcycling.html`, `humanities_teesside.html`) ·
`LundyLoop/assets/style.css`.

**OUT:** `Games` and personal apps (dual-branding rule — Made-by-Matt only) · **frozen legacy
science: `biology/`, `chemistry/`, `2 Physics 10/`** (these stay OUT even though
`Science_Teesside/` is IN) · superseded legacy art tasters (`Build/Slideshows/BUILD_ART_W\d_`) ·
old `BUILD_L1_` / `FW_L1_` · site furniture (`404.html`, root `index.html`, `hub-health`) ·
any pupil/student sheets or pupil data (never enter any zip).

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

---

## What this recipe cannot tell you

- Whether a given file *should* be in a staff pack at all. That is a content decision.
- Whether Progress Schools' own brand guidance has changed. This records the estate's
  practice, not their policy — if the two ever conflict, theirs wins and this file is
  the thing that is wrong.
- Anything about pupil-facing material. This is a staff-pack procedure only.
