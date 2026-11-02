# Education site · quick-links fix and look direction · Mon 2 Nov 2026

The owner delegated both items today ("you decide and you're in control"). He is unwell, so keep owner pin edits to a minimum by batching (see section 3).

## 1 · Quick-links spacing (do first, fold into Site #550)

**Fault.** The top quick-link row (`nav[data-mbm-hub-links]`: Lessons, Resources, Tools) is a 4-column grid with only 3 links. When ruling D4 removed Apps from the row, the stylesheet kept `repeat(4,minmax(0,1fr))`. The links bunch to the left and leave an empty fourth slot. At 1024 px the centres are 140 / 383 / 626 inside a 20–989 bar.

**Fix.** Edit `domain-split/shared-navigation.css` line 55, and nothing else:
`grid-template-columns:repeat(4,minmax(0,1fr));` becomes `grid-template-columns:none;grid-auto-flow:column;grid-auto-columns:minmax(0,1fr);`.
The column count then follows however many links there are.

Tested live by injection:
- Desktop 1024: centres 180 / 504 / 829 in a 20–989 bar.
- Phone 375: centres 72 / 188 / 303, no sideways scroll, every link still at least 44 px.

**Guard.** Add one assertion to `domain-split/check_education_hub_links.cjs` `assertPublicRow`: the quick links share one row at equal widths (within 1 px).

**Patches** (in `scratch\quicklinks`):
- `quicklinks_css.diff` (sha256 79b90c44…)
- `quicklinks_check.diff` (sha256 9d46cb17…)

**Landing.** Site #550 (site-mobile-masthead) already edits this file and is first in the queue. Fold the fix into #550 so it needs no separate admission or pin round.

## 2 · Look direction to match the new tiles

Measured on the live homepage today:
- 1 image in `main` (the logo).
- 0 animations.
- Two fonts.
- The "One topic, three pathways" block shows **Autumn 2 Week 6** science while the term is in Week 1.
- The "Inspect the box" lists carry 9–10 multi-coloured file chips per card, which reads busy.
- "Teacher Tools" is two plain rows.

Direction: calm, premium and classroom-safe. Use the same visual language as the house-style assemblies the owner praised ("Following instructions", "The rule of law").

1. **One tile system.** "Choose your door", Subjects and Teacher Tools all use the #559 tile component: same radius, shadow, icon slot and a picture slot. No plain rows.
2. **Pictures.**
   - The hero gets one realistic, age-suitable photo in the assembly house style (secondary-age learners in a specialist setting, no identifiable real people).
   - Each door tile and each Teacher Tools tile gets a small illustrative image.
   - Images are local, compressed WebP with alt text, and the names rule applies to every image and caption.
3. **Shorter hero.** Keep the facts but split the long headline. The headline is "Real lessons, real packs, real games". A short line under it reads "By a teacher, for every pathway · Free · No login · Works offline". Then the two buttons.
4. **Current week, automatically.** The featured "One topic, three pathways" block should show this week's lessons (Autumn 2 Week 1 from Tue 3 Nov), derived from the term calendar, not a fixed week.
5. **Calmer file lists.**
   - Each card shows three primary actions: Start lesson, Slides, Pupil sheet.
   - "All files (n)" opens the full list.
   - All file chips use one neutral style with a small file-type icon, not a different fill colour per type.
6. **Gentle motion.**
   - Tiles fade or rise in as they scroll into view, with a soft hover lift and focus ring.
   - At most 200 ms, no autoplay, and switched off entirely under prefers-reduced-motion.
   - No motion on text a pupil is reading.
7. **Palette.**
   - Keep navy, deep green and warm cream as the base, plus one accent per pathway (BUILD, GROW, LAUNCH) used consistently on chips and tile tops.
   - Every text and background pair must reach at least 4.5:1 contrast in both themes. The existing palette check applies.

## 3 · Sequencing and owner load

**Order:**
1. Quick-links fix inside #550.
2. #552.
3. #559 (tiles).
4. Then one "look" PR covering items 1–7 above.
5. Then the school-filter queue (#539 … #555, #574).

**Owner load.** Batch every education-site change that needs admission pairs into as few publisher-pin carriers as possible. The owner commits each carrier by hand on his phone, and he is unwell today. Hand him one pin edit at the end of a batch, not one per PR. Give him the exact three replacement lines; I will check each commit to the byte.

**Evidence per PR:**
- Before and after screenshots at 390×844 and 1280×800.
- 0 console errors.
- The palette and contrast check passes.
- The names scan shows 0 hits.
- The hub-links evenness assertion passes.
