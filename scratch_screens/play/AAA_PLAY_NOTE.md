# AAA Play Design Note — Unified Tile System, Discovery & Accessibility (`P-20-3` / `P-25`)

**Date:** `2026-11-02`
**Scope:** Design specification aligning `www.madebymatt-play.uk` with the education design direction across the games index (`/`, `/games/`) and per-game launch pages (`/games/<slug>/`), updated for all `P-25-2(a)–(g)` conditions.

---

## 1. Unified Tile System (`.play-tile`) Across Hero, Shelves & Launch Cards

Every interactive surface on Play shares a single structural component — **`.play-tile`** — eliminating ad-hoc card variants between the Hero Spotlight, category shelves, and launch-page preview cards:

| Variant | Grid / Layout | Shared `.play-tile` Primitives |
| :--- | :--- | :--- |
| **Hero Spotlight (`.play-tile.hero-tile` / `.spot-card`)** | Desktop: `grid-template-columns: 1.08fr 1fr` with `align-items: stretch` so `.hero-art` / `.spot-card > .thumb` fills 100% of the hero height (`object-fit: cover`, zero dark band beneath art); Phone (`≤ 760 px`): single-column stack (`16:9` art top, body below) | `16 px` border radius, `1 px solid #243456`, `#0D1424` surface, full-height artwork column on desktop, `Spotlight · 1 of 11` kicker + `Title — sub_genre` heading + pitch from `games.json`, data-derived capability chips, primary (`▶ Play Game`) + secondary (`Game Details & Seed`) `≥ 44 px` CTAs |
| **Shelf & Grid Card (`.play-tile.shelf-card` / `.game-card`)** | Vertical card inside `repeat(auto-fill, minmax(280px, 1fr))` grid (`16 px` gap) | `16:9` picture-only vector artwork header (`border-bottom: 1 px solid #243456`), `16 px` body padding, `Title — sub_genre` heading, plain-English `pitch` from `games.json`, data-derived capability chips (`classroom_facets`, `evidence.controls`, `session_band_labels`) |
| **Launch Page Preview Card (`.play-tile.launch-tile`)** | `1.15fr 1fr` split card on `/games/<slug>/` (`1fr` stack on mobile) | Full-height artwork frame, data-derived capability chips + `"🔇 Sound OFF by default"` badge, prominent `▶ Launch Fullscreen Game` CTA (`min-height: 48 px`), copyable numeric `Seed` pill (`min-height: 48 px`) matching the game's actual RNG seed format, and 3 data-backed panels (`What You Do (games.json)`, `Controls (evidence.json)`, `Seed, Escape & Local Save`) |

---

## 2. Picture-Only Vector Artwork Rules (`P-25-2a`, `P-25-2b`)

1. **Picture-Only `16:9` Vector Artwork per Card (`/assets/cards/<slug>.svg`)**:
   - **No text inside card art at all (`P-25-2a`)**: Card artwork is strictly picture-only. All `<text>` elements (such as the clipped `"…THE POINT"` header formerly in `apex-tennis.svg`) and `.thumb-block:not(.failed) > .thumb-title` text overlays are stripped/hidden so every card displays clean graphic vector art. (If an `<img>` fails to load and triggers `.thumb-block.failed`, the accessible fallback title remains available.)
   - **Full-Height Desktop Hero Art (`P-25-2b`)**: On desktop (`> 760 px`), `.hero-art` and `.spot-card > .thumb` stretch to `height: 100%` (`aspect-ratio: auto; object-fit: cover`) of the parent tile so no dark band ever appears beneath the hero artwork.
2. **Strict Content & Brand Guardrails**:
   - **No photos of people** (no stock photography, portraits, or avatars).
   - **No personal names or third-party logos** anywhere in visible text, SVG nodes, CSS classes, or DOM IDs.
   - **Brand preservation**: `"Made by Matt"` remains intact in the site header and brand metadata per standing rule.
   - **Intrinsic sizing**: Every card `<img>` sets explicit `width="640" height="360"` (`CLS = 0.000`).

---

## 3. Ruled Spotlight Order & `390×844` Phone-Load + Controls Gate (`P-25-2d`)

A game is featured in the Spotlight playlist only after passing its `390×844` (`deviceScaleFactor: 2`, mobile touch emulation) headless Chromium load, zero runtime errors, zero horizontal overflow (`scrollWidth <= 390`), and interactive controls verification. All **11 ruled Spotlight games** passed:

| Spotlight Order | Game (`Title — sub_genre`) | Route | `390×844` Load & Overflow | Verified Controls (`evidence.json` + Live DOM) |
| :---: | :--- | :--- | :---: | :--- |
| **`1 of 11` (Lead)** | **Apex Kick: World Stage — Aimed free-kick shooting** | `/apexkick/` | `HTTP 200` · `0` errors · `390/390 px` | `touch, keyboard` (`3` canvases, swipe/drag aim + `A/S/D`, `L/C/R`, `Space/Enter`) |
| **`2 of 11`** | **Blackout Pulse — Steer, parry and surge through neon** | `/cyberpulse/` | `HTTP 200` · `0` errors · `390/390 px` | `touch, keyboard` (`2` canvases, drag/tap parry & overcharge + `WASD/Arrows`, `Space`, `E`) |
| **`3 of 11`** | **Emberwild — Creature exploration and battles** | `/emberwild/` | `HTTP 200` · `0` errors · `390/390 px` | `touch, keyboard` (`4` canvases, touch D-pad/A/B + `WASD/Arrows`, `Z/Enter/Space`, `X/Esc`, `M`) |
| **`4 of 11`** | **Voxel Frontier: Beaconfall — Block world building and survival** | `/voxel/` | `HTTP 200` · `0` errors · `390/390 px` | `touch, keyboard` (`2` canvases, touch move/look/break/place + `WASD`, `Space`, `F`, `1–9`, `E`) |
| **`5 of 11`** | **House Olympiad — Sports-day events for 1–4 houses** | `/houseolympiad/` | `HTTP 200` · `0` errors · `390/390 px` | `touch, keyboard` (`1` canvas, touch/click event controls + `Arrows/WASD`, `Space`, `Enter`) |
| **`6 of 11`** | **Off-Brand: After Hours — Stealth shifts in a locked-down store** | `/offbrand/` | `HTTP 200` · `0` errors · `390/390 px` | `touch, keyboard, gamepad` (DOM + canvas start, virtual joystick/action buttons + `WASD/Arrows`, `E/Space`) |
| **`7 of 11`** | **Echo Vault — Sonar stealth extraction** | `/echovault/` | `HTTP 200` · `0` errors · `390/390 px` | `touch, keyboard` (`2` canvases, touch move/clap/hush + `WASD/Arrows`, `Space`, `Shift`, `E`) |
| **`8 of 11`** | **Skybreak Vector — 3D flight over islands and rings** | `/skybreak/` | `HTTP 200` · `0` errors · `390/390 px` | `touch, keyboard, gamepad` (`2` canvases, `#touch` flight stick & throttle + `W/S/A/D`, `Q/E`, `Space`) |
| **`9 of 11`** | **Touchline Dynasty — Football club management across seasons** | `/touchline/` | `HTTP 200` · `0` errors · `390/390 px` | `touch, keyboard` (`13` interactive controls, touch/click tactics & matchday UI + `1–5`, `Space`) |
| **`10 of 11`** | **Stormbreak — Three-lane hazard runner** | `/trailrunner/` | `HTTP 200` · `0` errors · `390/390 px` | `touch, keyboard` (`1` canvas, swipe left/right/up/down + `A/D` or `Left/Right`, `W/Up`, `S/Down`) |
| **`11 of 11`** | **Grapple — Rope-swing time-trial platformer** | `/Lessons/Games/Grapple.html` | `HTTP 200` · `0` errors · `390/390 px` | `touch, keyboard` (`2` canvases, DPR-aware backing store, hold/release grapple + `Space/Click`, `R`) |

---

## 4. Build-Time Derived Counts & Per-Game Claims (`P-25-2c`, `P-25-2e`, `P-25-2f`)

1. **All Counts Computed at Build Time (`P-25-2f`)**:
   - Derived directly from `data/source-manifests/games.json` and `domain-split/play/evidence.json` (never typed as literals):
     - **Catalogue games**: `games.length` = **`62`**
     - **Classroom activities**: `Object.keys(evidence.games).length - games.length` = **`7`**
     - **Calm filter count**: `games.filter(g => g.classroom_facets.includes('calm')).length` = **`9`**
     - **Touch filter count**: `games.filter(g => evidence.games[key].controls.includes('touch')).length` = **`43`**
     - **Keyboard filter count**: `games.filter(g => evidence.games[key].controls.includes('keyboard')).length` = **`53`**
2. **Responsive Search Placeholder (`P-25-2c`)**:
   - At `≤ 760 px` (phone portrait), `#query` / `#search-box` uses `"Search 62 games"` (computed from `data.catalogue` / `games.length`) so the placeholder never truncates.
3. **Every Per-Game Claim Comes from That Game's Data (`P-25-2e`)**:
   - **Capability chips**: Built per game from `g.classroom_facets`, `evidence.games[key].controls`, and `manifest.session_band_labels[g.session_band]`.
   - **What You Do & Controls**: Populated directly from `g.what_you_do` (`games.json`) and `evidence.games[key].instructions` (`evidence.json`).
   - **Real Seed Format**: For `Emberwild` (`/emberwild/`), the launch page displays its actual 32-bit numeric seed from `emberwild/index.html` (`default 0x454d4245 = 1162691141`, passed via `?seed=1162691141`).
   - **Escape Exit & Local Save Keys**: Displays `Emberwild`'s actual back/exit binding (`X or Escape to go back`) and exact allowlisted `localStorage` keys from `domain-split/game-storage-allowlist.json` (`mbm_emberwild_AUTOSAVE`, `mbm_emberwild_SLOT_1`).
   - **Unmeasured HUD Contrast Claim Dropped**: The unverified boilerplate claim `"WCAG AAA 7:1 across all HUD labels"` is removed.

---

## 5. WCAG AAA Hub Palette, Calm Mode & High Contrast Precedence (`P-25-2g`)

1. **Hub Surface Tokens (`≥ 7:1` Body, `≥ 4.5:1` Large)**:
   - `--bg-canvas`: `#070B14`; `--bg-surface`: `#0D1424`; `--bg-elevated`: `#131D33`; `--border-subtle`: `#243456`
   - `--text-primary`: `#F8FAFC` (`18.4:1` on canvas, `16.9:1` on surface)
   - `--text-secondary`: `#CBD5E1` (`12.1:1` on surface)
   - `--text-muted`: `#94A3B8` (`7.02:1` on surface)
   - `--accent-primary`: `#38BDF8` (`10.4:1` with `#04101E` CTA ink)
2. **Calm Mode & `prefers-reduced-motion` (`P-25-2g`)**:
   - Both `@media (prefers-reduced-motion: reduce)` and `[data-calm="true"]` disable all CSS animations, transitions, transforms, and animated art across hub and launch surfaces (`animation: none !important; transition: none !important; transform: none !important`).
3. **High Contrast Outranks the Theme (`P-25-2g`)**:
   - Declared at the end of `play.css` and mockup stylesheets so `@media (prefers-contrast: more), (forced-colors: active)` and `:root[data-contrast="high"], body[data-contrast="high"], .high-contrast` override all theme surface, ink, and border tokens (`#000000` canvas, `#FFFFFF` primary ink, `#94A3B8` high-visibility borders, `#7DD3FC` / `#38BDF8` focus/accent).

---

## 6. Updated Scratch Mockup Screenshots (`P-25` Proofs)

Rendered via headless Chromium from `render_aaa_mockups.mjs` using build-time data from `games.json`, `evidence.json`, and `game-storage-allowlist.json`:

| Mockup View | Viewport | Artifact Path | Scratch Mirror Path | Before (`P-20-3`) Bytes / SHA-256 | After (`P-25`) Bytes / SHA-256 |
| :--- | :---: | :--- | :--- | :--- | :--- |
| **Play Home (Phone Portrait)** | `390×844` | `...\aaa-play-home-390x844.png` | `...\scratch\play\mockups\aaa-play-home-390x844.png` | `219,680 B` · `2635f3cfdd25fa8e4ec4f7e2f033f6a9176036a70d5d1dd79f16ea7464acd0b5` | `193,403 B` · `d70e75c6da50367dfac52137bef730a5fa18c7f2be833bf8ebac48e0b4e04ee6` |
| **Play Home (Desktop / Whiteboard)** | `1280×800` | `...\aaa-play-home-1280x800.png` | `...\scratch\play\mockups\aaa-play-home-1280x800.png` | `248,213 B` · `71f96a02417abc89a3298fbf348b8902ed7d39e9cb95c0527a6796c3bb8e3e52` | `243,223 B` · `75cad1bc937d879938e219ee9c374aedf0de765f7e23e141cf66ff9faa3d876c` |
| **Game Launch Page (`Emberwild`)** | `1280×800` | `...\aaa-play-launch-1280x800.png` | `...\scratch\play\mockups\aaa-play-launch-1280x800.png` | `114,827 B` · `851ab15d5e699755866763816cb6c1aaa224ad551fcd989fa0cec0b67037bb12` | `110,723 B` · `2bae1e8b0ada0052e73e275323e0acf417cb5a283b7b6ec2d322163c89efab43` |
