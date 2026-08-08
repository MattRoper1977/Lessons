# Made by Matt cross-estate unification — Lessons

Sentinel: `mbm-cross-estate-unification-lessons-apps-2026-08-08`

## Scope and baseline

This release starts from Lessons `main` commit `aad7b5017bbf517915304e2280894e9874647822` and upgrades the public `/Lessons/` catalogue hub. It does not bulk-edit individual lessons, simulations, games, printable packs or archived material.

The measured starting estate contains 1,403 tracked files, including 548 HTML files, 15 CSS files, 252 JavaScript/MJS/CJS files and 38 JSON files. `resources.json` remains the catalogue source of truth and currently contains 448 resources: 311 in the `2026-27` collection and 137 in the `2025-26` library.

## Deployment topology

GitHub-hosted verification established that `https://madebymatt.uk/Lessons/` and `https://madebymatt.uk/Lessons/resources.json` are served as a project mount under the same `madebymatt.uk` origin as Home, Games, Apps, Tools and Resources. Public path casing remains `/Lessons/`.

## Canonical platform source

The design and interaction reference is `MattRoper1977/mattroper1977.github.io` at measured commit `4681ba6b4533745f42542c1591a4bda5de0b8cfc`.

This repository carries controlled local copies so the hub does not require the main-site asset server to function:

- `assets/mbm-platform.css` — SHA-256 `e3eb9b83d3c791eca059386999c306711678877bba27248cc78a1ef584e1031d`
- `assets/mbm-platform.js` — SHA-256 `0958a73a78a9f6d428d6cbe6c77a8a1cd5f015022ce9a6acbba92e6bee901fd2`
- `assets/mbm-theme.js` — SHA-256 `af946d77c39aece10c3b6f4d7e119033c7c3ce419d79f0c97286e27bab512da7`
- `assets/mbm-hub.css` — shared Lessons/Apps integration layer, SHA-256 `1643f51bcfe7f89923e908cf4f79b36a80d8bfa767779ab1c9cebe2e1a8b513c`

The permanent contract test compares the first three files byte-for-byte with the current canonical repository. Updating the platform shell is therefore an explicit synchronisation operation rather than silent drift.

## What changes

- A common Made by Matt header with the route order Games, Lessons, Apps, Tools and Resources.
- Correct Lessons current-page state and stable case-sensitive URLs.
- The canonical mobile drawer, Escape/outside dismissal, focus return and scroll lock.
- The canonical `mbm_reading_theme` background preference using a repo-local theme engine.
- Stronger hub spacing, surface, card, focus, touch and responsive treatment while retaining the Lessons educational identity.
- Keyboard-scrollable pathway and subject rails.
- Accessible live result announcements and a clear-filter route.
- Defensive manifest loading and link handling.

BUILD, GROW and LAUNCH wording, current-year/library separation, catalogue data, lesson descriptions and logo markup remain unchanged.

## Offline and standalone boundary

Only the hub and its local shared assets are in scope. The verifier rejects any changed path outside the explicit allow-list, including every individual lesson file and `resources.json`.

The browser gate also opens representative BUILD, GROW, LAUNCH and science lessons after the hub changes. This proves that the release has not introduced mandatory platform dependencies, global CSS collisions or navigation/runtime regressions into standalone teaching experiences.

## Verification

Run locally or in CI:

```bash
python tools/verify_cross_estate_unification.py \
  --base origin/main \
  --canonical _reference/site \
  --self-test

MBM_BASE_URL=http://127.0.0.1:4173/Lessons/ \
  node tools/verify_cross_estate_browser.mjs
```

The static positive control deliberately changes `/Lessons/` to `/lessons/` in a temporary fixture and must fail before the release can pass.
