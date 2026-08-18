# TL-2 Part E — Teesside Cross-Curricular Maker Lab PRO v2.1: STOPPED at Phase 4 (package self-check stale)

Sentinel: `townlife-tl2-2026-08-18-PARTE-TOP`

## Sequencing decision (E0)

E waited for D's Apps PR as ruled; D's Apps #15 merged to `9672d6b7bc12d865e4d6a2109e0bd26f282bd1c1`
and E branched from that main. Never shared a branch/PR/commit with A/B/C/D.

## Package gates (Phase 0/1 — PASS)

`Teesside_Maker_Lab_PRO_v2.1_DEPLOY_PACKAGE_2026-08-18_r1.zip` **5,999,516 B, sha256
`1999c4bf9e1fc681d2249fed3b72266e02dbaf5eb80abd6aff7d8bb1b65649f8`** — exact. `verify_deploy_package.py`
**PASS 52/52**; `run_patch_truth_gate.sh` **PATCH_TRUTH_PASS**. Provenance note carried verbatim per
E2: the source zip's supplied `.sha256` sidecar (`eae222b8…`) does not match the zip actually
supplied (`1ea8decb…`); the zip's internal SHA256SUMS verified 50/50, so it is treated as truth and
pinned by measured digest.

## What ran clean before the stop (all local-only, since reverted; nothing was ever pushed)

Phase 2 install from `9672d6b7`: 37 payload files byte-verified, 0 mismatches; apps.json +1 Teacher
tools record per CATALOGUE_ENTRY_SPEC (38 total, derived); AUDMAP + leadCount "Thirty-eight";
`tools/makerlab/verify_makerlab_static.py` installed — **PASS + positive control** (planted
`window.open` detected). Phase 2.5 parity: platform css/js byte-match Site canonical; theme engine
matches the pinned canonical digest ("Reading-theme parity" CI green at base). Phase 3: paired pin
`b70fdca96ba9 → 758489c54bd2` in BOTH verifier copies, byte-identical, `--check` PASS; cross-estate
verifier PASS + positive controls in Apps and Lessons.

Phase 4 real-Chromium-over-HTTP gates (first real-browser run of this package, as E2 predicted):
- index renders at desktop/tablet/390, 0 real console errors (one 404 = the bare test origin's
  `/favicon.ico`, environmental); all 21 links resolve 200; "← All apps" resolves to the hub.
- **ACCEPTANCE TEST PASS** (the reason v2.1 exists): `STUDIO_SHELL.html?app=1`, typed into the
  embedded studio's learner field → autosave chip **"saved 19:30"** (never "browser storage
  unavailable"); `MBM_MAKER_PRO_V2_shadow_rig_pro_v2` carries the typed marker; direct-opened
  studio 01 restores it into `#proLearner`. Screenshots in the evidence workspace.
- **Forged-postMessage control PASS**: window-sourced forged SYNC_APP rejected (no `forged:true`
  lands); frame-sourced genuine sync lands.
- Reduced-motion: max transition/animation duration **0.01 ms** across index + shell + studio.
- Print path: print-media renders, zero popups.

## The stop (Phase 4, mandatory gate) — first honest run of `RELEASE_SELF_CHECK.html`

> CHECK FAILED · 18 issues found. — checked 49 · passed 32 · issues 18

Every file that exists passes byte-for-byte (32/32). The 18 issues are structural to the package:
**17 MISSING** — all `qa/` artefacts (15 `PRO_QA_*.png`, `PORTABLE_EXPORT_QA_RESULTS.json`,
`SUITE_VISUAL_QA_MONTAGE.jpg`) that the EXPECTED inventory lists but the deploy payload does not
ship; **1 EXTRA** — `PATCH_NOTES_v2.1.md`, shipped but never inventoried. Root cause proven from the
package itself: the v2 source-release zip carries 21 `qa/` files; the deploy payload trims `qa/` to
4 and adds PATCH_NOTES; the packager regenerated EXPECTED (M5) against the **source-release tree**,
not the deploy payload. The build machine had no browser, so this could not be caught there.

**Stop condition hit (addendum E4): "any payload byte would need editing after install"** — the only
fix is editing `RELEASE_SELF_CHECK.html` (a payload file, pinned in SHA256SUMS.txt and
PAYLOAD_MANIFEST.json). Per the D-r3 precedent the package gets fixed, not the expectation. Local
branches deleted un-pushed; both worktrees reset; **zero E writes in any repository**.

## For the r2 package (Matt's choice)

Regenerate EXPECTED inside `RELEASE_SELF_CHECK.html` from the actual deploy payload (36 records;
note the two by-design inventory exclusions: the self-check page itself and SHA256SUMS.txt), or ship
the full source-release `qa/` set and inventory PATCH_NOTES. The runtime payload itself proved
healthy — acceptance, forged-message and RM results above stand and should reproduce identically.

## Owner-held item — OPEN, not resolved

Reading demand: FK 15.5–18.9 on the studios' `<p>`/`<h2>` prose (17–22 whole-panel) — above
BUILD/GROW. A plain-language pass is a content decision for Matt. **OPEN.**

Token: **not earned** — `MAKERLAB_V21_MERGED_PUBLISHED_SHA_PROVEN` requires every gate evidenced.
Stop recorded instead: Phase-4 RELEASE_SELF_CHECK package-truth failure, E4 stop condition.

Sentinel: `townlife-tl2-2026-08-18-PARTE-BOTTOM`
