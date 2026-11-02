# Education Hub Surfaces — AAA Polish Design Note (`S-6-2`)

## 1. Scope & Boundary
- **In scope (Hub Surfaces Only)**:
  - Education Home (`education-site/index.html`)
  - Education Main hub (`education-site/main/index.html`)
  - Resources hub (`education-site/resources/index.html`)
  - Tools hub (`education-site/tools/index.html`)
  - Education Lessons hubs (`education-lessons/index.html`, `education-lessons/{english,maths,science}/index.html`, `education-lessons/primary/index.html`)
  - Education Apps hub (`education-apps/index.html`)
  - Five Audience Doors (`education-site/for/teachers/index.html`, `education-site/for/pupils/index.html`, `education-site/for/parents-carers/index.html`, `education-site/for/schools/index.html`, `education-site/for/schools-semh/index.html`)
- **Out of scope (Strict Boundary)**:
  - Never inside lesson packs, lesson slide decks, printable sheets, or interactive pack files.

---

## 2. Colour Tokens & WCAG AAA Contrast (`>= 7:1` Body, `>= 4.5:1` Large / Pathway Accents)

All hub surfaces honour the four reading modes (`light`, `sepia`, `dark`, `high-contrast`) with WCAG AAA contrast (`>= 7:1` for body text and UI labels, `>= 4.5:1` for large text and pathway accents):

| Token | Light (`default`) | Sepia | Dark | High-Contrast | Role & Verified Contrast Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `--mbm-bg` | `#f5f7f8` | `#f4efe6` | `#0f171e` | `#000000` | Page canvas background |
| `--mbm-surface` | `#ffffff` | `#fbf7f0` | `#16222c` | `#0a0a0a` | Card & tile surface |
| `--mbm-surface-subtle` | `#edf2f4` | `#ebe3d5` | `#1d2c38` | `#141414` | Featured band & neutral chip fill |
| `--mbm-ink` | `#122028` | `#1f1a14` | `#f1f5f8` | `#ffffff` | Primary body & heading ink (`16.3:1` on `#ffffff`, `15.1:1` on `#f5f7f8`) |
| `--mbm-muted` | `#334854` | `#463c30` | `#c3d2dc` | `#e6e6e6` | Secondary descriptions & metadata (`9.2:1` on `#ffffff`, `8.5:1` on `#f5f7f8` — AAA `>= 7:1`) |
| `--mbm-line` | `#cfd9df` | `#d3c7b4` | `#2c3f4f` | `#ffffff` | 1 px structural card border (`1.5 px` in high-contrast) |
| `--mbm-brand` | `#0b5563` | `#0b525b` | `#63c7d6` | `#ffff00` | Primary interactive accent & focus ring (`8.3:1` on `#ffffff` — AAA `>= 7:1`) |
| `--mbm-brand-ink` | `#ffffff` | `#ffffff` | `#081318` | `#000000` | Ink on primary CTA button (`8.3:1` — AAA `>= 7:1`) |

### Pathway Accents (`>= 4.5:1` Large / Badge Border, `>= 7:1` Badge Text)
Each pathway has a subtle left-border / top-bar accent and a high-contrast pill badge so teachers and pupils can scan pathways at a glance without rainbow clutter:

| Pathway | Accent Fill (`--pathway-bg`) | Accent Border (`--pathway-accent`) | Badge Ink (`--pathway-ink`) | Contrast (`--pathway-ink` on `--pathway-bg` / `--pathway-accent` on `--mbm-surface`) |
| :--- | :--- | :--- | :--- | :--- |
| **Primary** | `#eef6f0` | `#1e6b3b` (`6.5:1`) | `#124726` | `10.1:1` (AAA) |
| **PRE** | `#fef6ec` | `#944d00` (`5.9:1`) | `#613100` | `9.8:1` (AAA) |
| **BUILD** | `#eef5fa` | `#0b5563` (`8.3:1`) | `#073b46` | `11.4:1` (AAA) |
| **PATH** | `#f3f0fa` | `#4c3585` (`8.7:1`) | `#32205e` | `12.0:1` (AAA) |
| **CORE** | `#f9f0f2` | `#7d2438` (`7.9:1`) | `#561625` | `11.1:1` (AAA) |

---

## 3. Type Scale & Spacing Rhythm

### Type Scale (`Atkinson Hyperlegible`, fallback `system-ui, -apple-system, Segoe UI, sans-serif`)
- **Hero Display (`h1`)**: `clamp(1.65rem, 2.6vw, 2.25rem)`, `font-weight: 800`, `line-height: 1.18`, `letter-spacing: -0.015em`.
- **Section Heading (`h2`)**: `clamp(1.25rem, 1.8vw, 1.5rem)`, `font-weight: 800`, `line-height: 1.24`.
- **Tile Title (`h3` / `.mbm-hub-tile-title`)**: `1.0625rem` (`17px`), `font-weight: 700`, `line-height: 1.3`.
- **Body Copy (`.mbm-hub-tile-desc`, hero subline)**: `1rem` (`16px`), `font-weight: 400`, `line-height: 1.5`, max measure `62ch`.
- **Metadata / Chip / Eyebrow**: `0.8125rem` (`13px`), `font-weight: 700`, `line-height: 1.25`, `letter-spacing: 0.03em`.

### Spacing Rhythm (`8 px` Base Grid)
- **Masthead & Quick-Links Bar**: Single-line brand bar (`y = 0..64px`), followed immediately by the 3-column evenly spaced `nav[data-mbm-hub-links]` (`grid-auto-flow: column; grid-auto-columns: minmax(0, 1fr)`, `gap: 4px`, `min-height: 44px`).
- **Compact Hero**: Vertical padding `20px` on phone (`390px`), `28px` on desktop (`1280px`) — roughly half the previous vertical height so the featured block and door tiles sit above or at the fold.
- **Section Rhythm**: `24px` (`1.5rem`) vertical stack gap on phone, `32px` (`2rem`) on desktop; internal card padding `16px` (`1rem`) on phone, `20px` (`1.25rem`) on desktop; tile grid gap `14px` on phone, `16px` on desktop; `border-radius: 14px`.

---

## 4. Shorter Hero & Automatic Current-Week Featured Block

1. **Shorter Hero**:
   - **Headline**: `Real lessons, real packs, real games`
   - **Subline**: `By a teacher, for every pathway · Free · No login · Works offline`
   - **Two Primary Actions** (`min-height: 44px`): `Browse lessons` (primary filled button) and `Open current week` (secondary outlined button).
   - **Visual**: Coupled on desktop (`1280px`) with the warm classroom/desk illustration (`hero-classroom.webp`, `aspect-ratio: 16 / 10`), stacked cleanly on mobile (`390px`).
2. **Automatic Current-Week Featured Block**:
   - Immediately below the hero sits a single featured card driven by the UK school-term calendar helper (currently resolving to **Autumn 2 · Week 1** for 2 November) with a direct deep-link (`Open Autumn 2 Week 1 packs`) and three primary file chips plus `"All files (n)"`.

---

## 5. Unified Tile System (`#559` Component) & File Chips

1. **One Tile Component Everywhere**:
   - The `#559` `.mbm-hub-tile` component powers audience doors, subject cards (English, Maths, Science, Primary), and teacher tools (Unit Award Scheme tracker, ASDAN tracker).
   - Every tile contains: (a) a top visual banner (`aspect-ratio: 16 / 9`, `overflow: hidden`) with a local `.webp` illustration, (b) an eyebrow badge (`Pathway` or `Audience`), (c) a bold title (`17px`), (d) a concise one-sentence summary (`--mbm-muted`), and (e) a bottom action row (`min-height: 44px`).
   - All five audience page URLs are read dynamically from the canonical `AUDIENCE_PAGES` list in `domain-split/shared-navigation.js` (never hand-typed).
2. **File Chips on Lesson Cards (3 Primary + `"All files (n)"`)**:
   - Lesson cards surface **3 primary chips** (`Start lesson`, `Slides`, `Pupil sheet`) plus a single **`All files (n)`** chip in one neutral, high-contrast chip style (`background: var(--mbm-surface-subtle)`, `border: 1px solid var(--mbm-line)`, `color: var(--mbm-ink)`, `min-height: 36px` inside card / `44px` tap target) with a crisp 14 px inline SVG file-type icon, replacing the 7-chip rainbow row.

---

## 6. House-Style Imagery Rules (Local WebP, Alt Text, Names Rule)

- **Format & Storage**: All tile and hero illustrations are local `.webp` assets (`aspect-ratio: 16 / 9` for tiles at `640×360`, `16 / 10` for the hero at `800×500`), stored locally in the repository (zero external CDN requests, offline-ready).
- **Subject Matter & Names Rule**:
  - Warm, tactile flat-editorial classroom still-lifes and learning tools (open exercise books, geometric compass and ruler, laboratory flask and leaf specimen, reading lamp, tactile counters, checklist clipboard).
  - **Strict exclusions**: No photos of people or faces; no pupil, staff, school, place, product, platform, exam-board, awarding-body, real-person, or AI-model names or logos anywhere in imagery, filenames, or `alt` attributes.
- **Accessibility**: Informative `alt` text where the image conveys context, or `alt=""` (`role="presentation"`) when paired with an adjacent visible heading that already names the tile.

| Asset File (`scratch/mobile/assets/`) | Dimensions | Size (Bytes) | SHA-256 |
| :--- | :--- | ---: | :--- |
| `hero-classroom.webp` | `800×500` | `7,686` | `b6abc7c8de49dce9fbeed48538e8ef9d8f3e69dc16f6eb7c9ee241931b311fc3` |
| `door-teachers.webp` | `640×360` | `2,206` | `4686a2c79e0223cbc037524f7b15b4ed7bdde9f8aa2c30a728bfd11278ccd26c` |
| `door-pupils.webp` | `640×360` | `2,872` | `5a2cdea50771292e32f998333e9077f4f4f4dcedd287e486efebf05498d5eb23` |
| `door-parents.webp` | `640×360` | `2,082` | `1814c60b6a2f75f84c4bbc8c42b7aaa6e2e7fd81a7ec8cf3ebd1611842f54361` |
| `door-schools.webp` | `640×360` | `2,442` | `18a80af51ca10e50c547e21d4696daa092c9ae8104f2c6e733c29d6745c092d3` |
| `tool-asdan.webp` | `640×360` | `2,386` | `289b4b62b07b4ba5383689e83f4db8ead09a373486be78e569038bbeeebec62b` |
| `tool-uas.webp` | `640×360` | `1,644` | `d536dfa46193bba4cbe4e022c023966cd6ce9b0b705488ca3c62fa97d53d28c8` |

---

## 7. Motion Rules (`<= 180 ms`, `prefers-reduced-motion` Honoured)

- **Scope**: Motion is strictly limited to (1) tile/button hover and active press states (`160 ms cubic-bezier(0.22, 1, 0.36, 1)` transform `translateY(-2px)` and border-colour shift) and (2) initial page-reveal (`180 ms ease-out`, always under the `200 ms` ceiling).
- **Zero-JS / Mobile Fail-Safe**: Below-the-fold sections remain visible (`opacity: 1; transform: none`) if `IntersectionObserver` does not fire within `350 ms` or on narrow viewports.
- **Reduced Motion**:
  ```css
  @media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
      animation-duration: 0.01ms !important;
      animation-iteration-count: 1 !important;
      transition-duration: 0.01ms !important;
      scroll-behavior: auto !important;
      transform: none !important;
    }
  }
  ```

---

## 8. Rendered Scratch Mockup Screenshots

Rendered from `scratch/mobile/mockup_home.html` and `scratch/mobile/mockup_audience_schools_semh.html` via headless Chromium:

| Mockup File (`scratch/mobile/`) | Viewport | Size (Bytes) | SHA-256 |
| :--- | :--- | ---: | :--- |
| `mockup-home-390x844.png` | `390×844` | `63,446` | `9e840df761a33064a36a054a23eeb1b016641d4a3f62b6d8b9e6e85d1ef62486` |
| `mockup-home-1280x800.png` | `1280×800` | `114,836` | `a5f636dac9773a40f510c50a0854fbebe0eefd8ef792210f6206775a8ab09592` |
| `mockup-audience-schools-semh-390x844.png` | `390×844` | `52,377` | `ab7592d5ad77aa6cba63b6cb4701f2deffadffbd2b551e9215efe36dcd533317` |
| `mockup-audience-schools-semh-1280x800.png` | `1280×800` | `98,107` | `a1f6308e56d2c5f4fb279e1f7ee337f1e1dd0ceca6eb0f2dadb7e5af3f4b529b` |
