# AAA Play Design Note — Unified Tile System, Discovery & Accessibility (`P-20-3` / `P-25` / `P-26`)

**Date:** `2026-11-02`
**Scope:** Design specification aligning `www.madebymatt-play.uk` with the education design direction across the games index (`/`, `/games/`) and per-game launch pages (`/games/<slug>/`), updated for all `P-25-2(a)–(g)` and `P-26-2(a)–(e)` conditions.

---

## 1. Unified Tile System (`.play-tile`) Across Hero, Shelves & Launch Cards

Every interactive surface on Play shares a single structural component — **`.play-tile`** — eliminating ad-hoc card variants between the Hero Spotlight, category shelves, and launch-page preview cards:

| Variant | Grid / Layout | Shared `.play-tile` Primitives |
| :--- | :--- | :--- |
| **Hero Spotlight (`.play-tile.hero-tile` / `.spot-card`)** | Desktop: `grid-template-columns: 1.08fr 1fr` with `align-items: stretch` so `.hero-art` / `.spot-card > .thumb` fills 100% of the hero height (`object-fit: cover`, zero dark band beneath art); Phone (`≤ 760 px`): single-column stack (`16:9` art top, body below) | `16 px` border radius, `1 px solid #243456`, `#0D1424` surface, full-height artwork column on desktop, `Spotlight · 1 of 11` kicker + `Title — sub_genre` heading + pitch from `games.json`, data-derived capability chips, primary (`▶ Play Game`) + secondary (`Game Details & Seed`) `≥ 44 px` CTAs |
| **Featured Playlist (`.play-tile.playlist-tile`)** | Desktop companion panel beside Hero Spotlight (`11` ruled picks in 2 columns) | Clean header (`Featured Playlist · 1 of 11` without developer/viewport tags), showing the game name only on each row (`1 Apex Kick: World Stage` … `11 Grapple`) so no row ever cuts mid-word (`P-26-2a`, `P-26-2d`) |
| **Shelf & Grid Card (`.play-tile.shelf-card` / `.game-card`)** | Vertical card inside `repeat(auto-fill, minmax(280px, 1fr))` grid (`16 px` gap); shelf caption reads `62 games in catalogue` (`P-26-2a`) | `16:9` picture-only vector artwork header (`border-bottom: 1 px solid #243456`), `16 px` body padding, `Title — sub_genre` heading, plain-English `pitch` from `games.json`, data-derived capability chips (`classroom_facets`, `evidence.controls`, `session_band_labels`) |
| **Launch Page Preview Card (`.play-tile.launch-tile`)** | `1.15fr 1fr` split card on `/games/<slug>/` (`1fr` stack at `390×844`) | Full-height artwork frame, data-derived capability chips + `"🔇 Sound OFF by default"` badge, prominent `▶ Play Game` CTA (`min-height: 48 px` desktop / `44 px` mobile), copyable plain-English `Seed: 1162691141 · Copy link` pill, and 3 plain-English teacher/pupil panels: **`What you do`**, **`Controls`**, and **`Seed, exit and saving`** (`P-26-2b`, `P-26-2c`) |

---

## 2. Picture-Only Vector Artwork & Branded-Object Audit (`P-25-2a`, `P-25-2b`, `P-26-2e`)

1. **Picture-Only `16:9` Vector Artwork per Card (`/assets/cards/<slug>.svg`)**:
   - **No text inside card art at all (`P-25-2a`)**: Card artwork is strictly picture-only. All `<text>` elements (such as the clipped `"…THE POINT"` header formerly in `apex-tennis.svg`) and `.thumb-block:not(.failed) > .thumb-title` text overlays are stripped/hidden so every card displays clean graphic vector art.
   - **Full-Height Desktop Hero Art (`P-25-2b`)**: On desktop (`> 760 px`), `.hero-art` and `.spot-card > .thumb` stretch to `height: 100%` (`aspect-ratio: auto; object-fit: cover`) of the parent tile so no dark band ever appears beneath the hero artwork.
2. **Full 42-Card SVG Audit for Branded-Object Look-Alikes (`P-26-2e`)**:
   - All **42** `Site/assets/cards/*.svg` files were inspected line by line:
     - **`emberwild.svg`**: Formerly drew a two-hemisphere red-and-white sphere (`#E8EEF2` circle + `#A04B00` upper half-arc + `#12210F` outline + `#FFC163` center button) at `<g transform="translate(84,40)">` that read as a branded capture ball. Replaced with a tapered **wayfinder lantern** in `Emberwild`'s own emerald and amber palette (`#2E6B3A` roof/base, `#8FE07A` ring, `#FFC163` / `#FFF7D6` glowing lantern pane, `#FFB347` halo).
     - **All other 41 card SVGs** (`apex-curl.svg`, `apex-golf-door.svg`, `apex-golf.svg`, `apex-pool.svg`, `apex-rally.svg`, `apex-tennis-door.svg`, `apex-tennis.svg`, `apex-velodrome.svg`, `aurora-links-3d.svg`, `axiom-shift.svg`, `biopunk-hive.svg`, `charcoal.svg`, `crown-badge.svg`, `cyberpulse.svg`, `echo-vault.svg`, `fracture-engine.svg`, `global-games.svg`, `house-olympiad.svg`, `lumina-haven.svg`, `micro-tinkerer.svg`, `neon-breach.svg`, `neon-garden.svg`, `neon-siege.svg`, `neon-snake-overdrive.svg`, `neon-sync.svg`, `neon-turf-overdrive.svg`, `off-brand-door.svg`, `off-brand.svg`, `prism.svg`, `relicforge.svg`, `skybreak-vector.svg`, `slipstream-gp.svg`, `slipstream-hyperdraft.svg`, `the-last-lighthouse.svg`, `titan-forge.svg`, `touchline-dynasty.svg`, `town-life.svg`, `trail-runner.svg`, `trekkers-trail-runner-tees-coast.svg`, `voxelcraft.svg`, `wrecking-crew.svg`): Verified clean — **0** branded look-alikes.
3. **Strict Content & Brand Guardrails**:
   - **No photos of people**, **no personal names**, and **no third-party logos or branded objects**.
   - **Brand preservation**: `"Made by Matt"` remains intact in the site header and brand metadata per standing rule.

---

## 3. Ruled Spotlight Order & `390×844` Phone-Load + Controls Gate (`P-25-2d`, `P-26-2d`)

All **11 ruled Spotlight games** pass `390×844` (`deviceScaleFactor: 2`, mobile touch emulation) headless Chromium load, zero runtime errors, zero horizontal overflow (`scrollWidth <= 390`), and interactive controls verification, and display in the desktop playlist by game name only with zero mid-word truncation (`truncatedPlaylistItems: []`):

| Spotlight Order | Playlist Label (`P-26-2d`) | Full Heading (`Title — sub_genre`) | Route | `390×844` Gate |
| :---: | :--- | :--- | :--- | :---: |
| **`1 of 11` (Lead)** | **Apex Kick: World Stage** | **Apex Kick: World Stage — Aimed free-kick shooting** | `/apexkick/` | `HTTP 200` · `0` errors · `390/390 px` |
| **`2 of 11`** | **Blackout Pulse** | **Blackout Pulse — Steer, parry and surge through neon** | `/cyberpulse/` | `HTTP 200` · `0` errors · `390/390 px` |
| **`3 of 11`** | **Emberwild** | **Emberwild — Creature exploration and battles** | `/emberwild/` | `HTTP 200` · `0` errors · `390/390 px` |
| **`4 of 11`** | **Voxel Frontier: Beaconfall** | **Voxel Frontier: Beaconfall — Block world building and survival** | `/voxel/` | `HTTP 200` · `0` errors · `390/390 px` |
| **`5 of 11`** | **House Olympiad** | **House Olympiad — Sports-day events for 1–4 houses** | `/houseolympiad/` | `HTTP 200` · `0` errors · `390/390 px` |
| **`6 of 11`** | **Off-Brand: After Hours** | **Off-Brand: After Hours — Stealth shifts in a locked-down store** | `/offbrand/` | `HTTP 200` · `0` errors · `390/390 px` |
| **`7 of 11`** | **Echo Vault** | **Echo Vault — Sonar stealth extraction** | `/echovault/` | `HTTP 200` · `0` errors · `390/390 px` |
| **`8 of 11`** | **Skybreak Vector** | **Skybreak Vector — 3D flight over islands and rings** | `/skybreak/` | `HTTP 200` · `0` errors · `390/390 px` |
| **`9 of 11`** | **Touchline Dynasty** | **Touchline Dynasty — Football club management across seasons** | `/touchline/` | `HTTP 200` · `0` errors · `390/390 px` |
| **`10 of 11`** | **Stormbreak** | **Stormbreak — Three-lane hazard runner** | `/trailrunner/` | `HTTP 200` · `0` errors · `390/390 px` |
| **`11 of 11`** | **Grapple** | **Grapple — Rope-swing time-trial platformer** | `/Lessons/Games/Grapple.html` | `HTTP 200` · `0` errors · `390/390 px` |

---

## 4. Plain-English Teacher & Pupil Copy Built from Canonical Data (`P-25-2c/e/f`, `P-26-2a/b/c`)

1. **No Developer Jargon on Any Surface (`P-26-2a`, `P-26-2b`, `P-26-2c`)**:
   - Playlist header reads `"Featured Playlist · 1 of 11"` (removed `"390×844 VERIFIED"`).
   - Shelf caption reads `"62 games in catalogue"` (removed `"Derived from games.json"`).
   - Launch page panel headings read **`"What you do"`**, **`"Controls"`**, and **`"Seed, exit and saving"`** (no file names).
   - Launch page body is 100% plain English for teachers and pupils — zero code identifiers, DOM selectors, storage keys, or hex literals:
     - **What you do**:
       - *"Explore routes with stairs, ledges and tall-grass encounters."*
       - *"Press as the rings meet for optional bonus power in battle."*
       - *"Make story choices that lead to one of five futures."*
     - **Controls**:
       - *"WASD or arrows to move; Z, Enter, Space or A to interact; X or Escape to go back; M opens the field kit. Touch D-pad available."*
       - *"Play with touch, keyboard or mouse."*
       - *"Calm Motion and High Contrast are in Settings."*
     - **Seed, exit and saving**:
       - *"Sound starts off. Tap the speaker to turn it on."*
       - *"Share the seed so the whole class gets the same world."*
       - *"Progress saves on this device. Press Escape or X to step back at any time."*
2. **All Counts Computed at Build Time (`P-25-2f`)**:
   - Catalogue games: **`62`**; Classroom activities: **`7`**; Calm: **`9`**; Touch: **`43`**; Keyboard: **`53`**.
   - Phone search placeholder at `≤ 760 px`: **`"Search 62 games"`** (`P-25-2c`).

---

## 5. WCAG AAA Hub Palette, Calm Mode & High Contrast Precedence (`P-25-2g`)

1. **Hub Surface Tokens (`≥ 7:1` Body, `≥ 4.5:1` Large)**:
   - `--bg-canvas`: `#070B14`; `--bg-surface`: `#0D1424`; `--bg-elevated`: `#131D33`; `--border-subtle`: `#243456`
   - `--text-primary`: `#F8FAFC` (`18.4:1` on canvas, `16.9:1` on surface); `--text-secondary`: `#CBD5E1` (`12.1:1` on surface); `--text-muted`: `#94A3B8` (`7.02:1` on surface); `--accent-primary`: `#38BDF8` (`10.4:1` with `#04101E` CTA ink)
2. **Calm Mode & High Contrast Precedence (`P-25-2g`)**:
   - `@media (prefers-reduced-motion: reduce)` and `[data-calm="true"]` disable all CSS animations, transitions, and transforms (`!important`).
   - `@media (prefers-contrast: more), (forced-colors: active)` and `:root[data-contrast="high"], body[data-contrast="high"], .high-contrast` outrank the theme at the end of the stylesheet.

---

## 6. Updated Scratch Mockup Screenshots (`P-26` Proofs)

Rendered via headless Chromium from `render_aaa_mockups.mjs` across all four ruled views (`390×844` and `1280×800` for both Home and Launch):

| Mockup View | Viewport | Previous (`P-25`) Bytes / SHA-256 | Updated (`P-26`) Bytes / SHA-256 |
| :--- | :---: | :--- | :--- |
| **Play Home (Phone Portrait)** | `390×844` | `193,403 B` · `d70e75c6da50367dfac52137bef730a5fa18c7f2be833bf8ebac48e0b4e04ee6` | `193,331 B` · `e318e794f528645b7ca3e57ed3a0294a7cd39a504c17dd3053cf64253f65a816` |
| **Play Home (Desktop / Whiteboard)** | `1280×800` | `243,223 B` · `75cad1bc937d879938e219ee9c374aedf0de765f7e23e141cf66ff9faa3d876c` | `226,798 B` · `235bafa8c317a6bf9d66b4259ba476bf10b4eddd07ae7b8f20a0e57188f0b29e` |
| **Game Launch Page (`Emberwild` Desktop)** | `1280×800` | `110,723 B` · `2bae1e8b0ada0052e73e275323e0acf417cb5a283b7b6ec2d322163c89efab43` | `87,220 B` · `7f0da60934748cada518a9b73cb296f2f65582ea0f13f535861ae86252e79978` |
| **Game Launch Page (`Emberwild` Phone)** | `390×844` | *(new in `P-26-3`)* | `173,132 B` · `066f5b554d944fed3a8141bf15807dc2b10ae9efc7b193ff4132fe6cf567641a` |
