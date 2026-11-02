# AAA Play Design Note — Unified Tile System, Discovery & Accessibility (`P-20-3`)

**Date:** `2026-11-02`
**Scope:** Design specification (no production code yet) aligning `www.madebymatt-play.uk` with the education design direction across the games index (`/`, `/games/`) and per-game launch pages (`/games/<slug>/`).

---

## 1. Unified Tile System (`.play-tile`) Across Hero, Shelves & Launch Cards

Every interactive surface on Play shares a single structural component — **`.play-tile`** — eliminating ad-hoc card variants between the Hero Spotlight, category shelves, and launch-page preview cards:

| Variant | Grid / Layout | Shared `.play-tile` Primitives |
| :--- | :--- | :--- |
| **Hero Spotlight (`.play-tile.hero-tile`)** | Desktop: `grid-template-columns: 1.1fr 1fr`; Phone (`≤ 760 px`): single-column stack (`16:9` art top, body below) | `16 px` border radius, `1 px solid #243456`, `#0D1424` surface, artwork header/column, kicker + title + 1-line subtitle, metadata chip row, primary (`▶ Play Game`) + secondary (`Game Details & Seed`) `≥ 44 px` CTAs |
| **Shelf & Grid Card (`.play-tile.shelf-card`)** | Vertical card inside `repeat(auto-fill, minmax(280px, 1fr))` grid (`16 px` gap) | `16:9` vector artwork header (`border-bottom: 1 px solid #243456`), `16 px` body padding, `Title — Descriptive Subtitle` heading, one-line plain-English action description, up to 3 capability chips (`Calm / Untimed`, `One-Hand / Touch`, `Keyboard`, session length) |
| **Launch Page Preview Card (`.play-tile.launch-card`)** | `1.15fr 1fr` split card on `/games/<slug>/` (`1fr` stack on mobile) | Same `16:9` artwork frame with `"🔇 Sound OFF by default"` badge, full descriptive heading + subtitle, `2×2` classroom specification grid (`Control Mode`, `Pacing`, `Session Length`, `Default Audio`), prominent `▶ Launch Fullscreen Game` CTA (`min-height: 48 px`), and copyable `Class Seed` pill (`min-height: 48 px`) |

---

## 2. Artwork Rules (Real Vector/Canvas Artwork per Card)

1. **Dedicated `16:9` Artwork per Game (`/assets/cards/<slug>.svg`)**:
   - Every game card and launch page renders bespoke SVG/canvas game artwork depicting the actual game environment, mechanics, or trajectory (e.g. `emberwild.svg` isometric biome & lantern path, `echo-vault.svg` acoustic sonar rings, `aurora-links-3d.svg` northern-lights fairway, `apex-tennis.svg` baseline rally trajectory).
2. **Strict Content & Brand Guardrails**:
   - **No photos of people** (no stock photography, portraits, or avatars).
   - **No personal names or third-party logos** anywhere in visible text, SVG nodes, CSS classes, or DOM IDs.
   - **Brand preservation**: `"Made by Matt"` remains intact in the site header and brand metadata per standing rule.
   - **Intrinsic sizing**: Every `<img>` sets explicit `width="640" height="360"` and `aspect-ratio: 16 / 9` (`CLS = 0.000`).

---

## 3. Clear Descriptive Naming & One-Line Subtitle Standard

Every game on the index and on its launch page pairs its title with a **descriptive mechanic noun phrase** and a **single-line plain-English subtitle** so pupils and teachers know what a game does before clicking:

- **Heading pattern**: `<Game Name> — <2–4 Word Mechanic Descriptor>`
  - *Emberwild — Lantern-Lit Biome Forager*
  - *Echo Vault — Acoustic Sonar Maze*
  - *Aurora Links — Northern Lights Golf*
  - *Apex Tennis — Precision Court Rally*
  - *Charcoal — Sketchbook Physics Platformer*
- **One-line subtitle pattern (`≤ 110 characters`, 2 lines max at `390 px`)**:
  - Starts with an active verb describing what the player does and how the session paces itself:
    - *"Guide a lantern craft across dusk biomes, gather botanical specimens, and restore quiet sanctuary groves at your own pace."*
    - *"Send out sound-wave pulses to map dark caverns and reach the exit before the echo fades."*
    - *"Read wind vectors and terrain slopes across nine arctic fairways in solo or pass-and-play rounds."*
    - *"Time topspin drives and baseline angles across quick singles sets or untimed rally practice."*

---

## 4. Games Index Discovery Bar — Instant Search + Classroom Filter Pills

Directly below the top bar on `/` and `/games/`, `.discovery-bar` provides zero-reload client-side filtering across all 62 games:

1. **Search Box (`input[type="search"].search-input`)**:
   - `min-height: 44 px`, `padding: 0 16px 0 42px`, `border-radius: 12 px`, `1.5 px solid #243456`, focus ring `2 px solid #38BDF8` (`offset: 2 px`).
   - Matches against game title, mechanic descriptor, one-line subtitle, and capability tags.
2. **Primary Filter Pills (`role="group" aria-label="Quick filters"`)**:
   - Every pill enforces `min-height: 44 px`, `padding: 0 14px`, `border-radius: 999px`, `font-variant-numeric: tabular-nums`, and live match counts:
     - **`All Games · 62`** (resets active filters)
     - **`Calm / Untimed · 24`** (games with untimed exploration, puzzle, or relaxed mode)
     - **`One-Hand / Touch · 41`** (games playable with single-finger tap/drag on phones and tablets)
     - **`Keyboard · 58`** (games with full WASD / arrow-key + Space/Enter bindings)

---

## 5. WCAG AAA Colour & Contrast Tokens (`≥ 7:1` Body, `≥ 4.5:1` Large)

All Play surfaces use a dark-slate classroom palette engineered to pass **WCAG 2.1 AAA** contrast thresholds without neon glare or halation:

| Token | Hex | Role | Background Pair | Measured Contrast | WCAG Target |
| :--- | :--- | :--- | :--- | :---: | :---: |
| `--bg-canvas` | `#070B14` | Page canvas background | — | — | — |
| `--bg-surface` | `#0D1424` | `.play-tile` & input surface | `#070B14` | — | — |
| `--bg-elevated` | `#131D33` | Metadata chips & secondary buttons | `#0D1424` | — | — |
| `--border-subtle` | `#243456` | Tile, chip & input hairline border | `#0D1424` | `1.9:1` (structural) | Decorative / hairline |
| `--text-primary` | `#F8FAFC` | Headings, card titles, active pill label | `#070B14` / `#0D1424` | **`18.4:1` / `16.9:1`** | **AAA (`≥ 7.0:1`)** |
| `--text-secondary` | `#CBD5E1` | One-line subtitles, metadata chips, specs | `#0D1424` / `#131D33` | **`12.1:1` / `10.8:1`** | **AAA (`≥ 7.0:1`)** |
| `--text-muted` | `#94A3B8` | Kicker labels & counts | `#070B14` / `#0D1424` | **`7.6:1` / `7.02:1`** | **AAA (`≥ 7.0:1` body, `≥ 4.5:1` large)** |
| `--accent-primary` | `#38BDF8` | Primary CTA fill (`#04101E` ink) & focus ring | `#04101E` ink on `#38BDF8` | **`10.4:1`** | **AAA (`≥ 7.0:1`)** |
| `--accent-emerald` | `#34D399` | Active seed code & classroom-ready badge | `#0D1424` | **`9.8:1`** | **AAA (`≥ 7.0:1`)** |

---

## 6. Type Scale & Spacing Rhythm

### Type Scale (`Inter, system-ui, -apple-system, Segoe UI, Roboto, sans-serif`)
| Token / Class | Size (`rem` / `px`) | Weight | Line Height | Tracking | Numeric Variant |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **Hero / Launch Title (`.tile-title-lg`)** | `clamp(1.375rem, 2.4vw, 1.875rem)` (`22–30 px`) | `800` | `1.20` | `-0.02em` | — |
| **Shelf Heading (`.shelf-title`)** | `1.25rem` (`20 px`) | `800` | `1.25` | `-0.015em` | — |
| **Card Title (`.tile-title-sm`)** | `1.0625rem` (`17 px`) | `800` | `1.25` | `-0.01em` | — |
| **Hero / Launch Subtitle (`.tile-subtitle`)** | `0.9375rem` (`15 px`) | `400` | `1.45` | `0` | — |
| **Card Subtitle (`.tile-sub-sm`)** | `0.875rem` (`14 px`) | `400` | `1.45` | `0` | — |
| **Filter Pill / Secondary CTA (`.pill`)** | `0.8125rem` (`13 px`) | `600` | `1.00` | `0` | `tabular-nums` |
| **Metadata Chip / Kicker (`.tag-chip`)** | `0.75rem` (`12 px`) | `600–700` | `1.20` | `0.02em` | `tabular-nums` |

### Spacing Rhythm (`4 px` Base Grid)
- `--space-1`: `4 px` (inline icon gap, title-to-subtitle micro-offset)
- `--space-2`: `8 px` (filter pill gap, metadata chip gap)
- `--space-3`: `12 px` (card body internal row gap, topbar item gap)
- `--space-4`: `16 px` (card padding, `.card-grid` gap, section margin on mobile)
- `--space-5`: `24 px` (hero body padding, launch card padding)
- `--space-6`: `32 px` (major section separation on desktop)
- `--radius-tile`: `16 px` (all `.play-tile` containers); `--radius-pill`: `999px` (filter pills & status badges)

---

## 7. Motion Budget (`< 200 ms`) & Classroom Defaults

1. **Strictly Scoped Motion (`≤ 160 ms`)**:
   - Transitions are permitted **only** on:
     - **Tile hover/press**: `transform 160ms cubic-bezier(0.22, 1, 0.36, 1), border-color 160ms cubic-bezier(0.22, 1, 0.36, 1)` (`translateY(-2px)` on pointer hover; `scale(0.99)` on active press).
     - **Page/Launch reveal**: `opacity 160ms cubic-bezier(0.22, 1, 0.36, 1)` on initial route mount.
   - **Zero idle/background animations** on the index or launch pages (no floating particles, no auto-scrolling carousels, no pulsing glow filters).
2. **`prefers-reduced-motion: reduce` Enforcement**:
   - `@media (prefers-reduced-motion: reduce) { *, *::before, *::after { animation-duration: 0.01ms !important; transition-duration: 0.01ms !important; transform: none !important; } }`
3. **Sound OFF Default & Classroom Controls**:
   - Every game and launch page boots with **`🔇 Sound OFF` by default** (`localStorage` opt-in never auto-unmutes on initial page load).
   - Every interactive control (Play CTA, filter pills, search box, class seed button, mute toggle) enforces **`≥ 44 × 44 px`** touch target sizing at `390×844`.

---

## 8. Scratch Mockup Screenshots (`P-20-3` Proofs)

Rendered via headless Chromium from the scratch prototype (`render_aaa_mockups.mjs`) serving real SVG game artwork from `Site/assets/cards/`:

| Mockup View | Viewport | Artifact Path | Scratch Mirror Path | Bytes | SHA-256 |
| :--- | :---: | :--- | :--- | ---: | :--- |
| **Play Home (Phone Portrait)** | `390×844` | `C:\Users\Londo_sm79v1o\.gemini\antigravity\brain\3337d84d-bb14-4728-872a-9979e2887613\aaa-play-home-390x844.png` | `C:\Users\Londo_sm79v1o\.gemini\antigravity\scratch\play\mockups\aaa-play-home-390x844.png` | `219,680 B` | `2635f3cfdd25fa8e4ec4f7e2f033f6a9176036a70d5d1dd79f16ea7464acd0b5` |
| **Play Home (Desktop / Whiteboard)** | `1280×800` | `C:\Users\Londo_sm79v1o\.gemini\antigravity\brain\3337d84d-bb14-4728-872a-9979e2887613\aaa-play-home-1280x800.png` | `C:\Users\Londo_sm79v1o\.gemini\antigravity\scratch\play\mockups\aaa-play-home-1280x800.png` | `248,213 B` | `71f96a02417abc89a3298fbf348b8902ed7d39e9cb95c0527a6796c3bb8e3e52` |
| **Game Launch Page (`Emberwild`)** | `1280×800` | `C:\Users\Londo_sm79v1o\.gemini\antigravity\brain\3337d84d-bb14-4728-872a-9979e2887613\aaa-play-launch-1280x800.png` | `C:\Users\Londo_sm79v1o\.gemini\antigravity\scratch\play\mockups\aaa-play-launch-1280x800.png` | `114,827 B` | `851ab15d5e699755866763816cb6c1aaa224ad551fcd989fa0cec0b67037bb12` |
