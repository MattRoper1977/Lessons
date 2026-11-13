# P1 intake checks

All authored reports are inside `_incoming/pack1r/`. The estate tools, registries and publication manifests are unchanged.

* `check_static.py`: imports `classify()`, the title checker’s parser/heading/distinct functions, and the unchanged HUM-T loop battery. Population is the three entries in `population.json`. LISTED is NOT YET APPLICABLE. Internal title/H1/COVERAGE/landing-card equality is mandatory.
* `class_a_patterns.py`: ports the source pattern and helper-function list. The original `_passhumd5/scan_class_a.py` module is neither run nor imported. Raw HTML text-node whitespace is checked separately.
* `browser_checks.cjs`: imports the unchanged `render_proof.cjs` function through a VM export shim. Its file navigation is mapped to the specified served target and its hard-coded axe dependency is relocated to the intake copy. The function body is unchanged. Its historical loop counters r38–r40 are reported as loop evidence; they are not confused with the chassis contract’s dialog rows.
* Additional rendered checks drive the shell dialogs, closers, goto controls, timers, navigation, route controls, model reveals, answer controls, map views, volunteer picker, staff preference and print functions. The organiser print DOM is rendered to PDF. Axe runs on all nine stages and all six dialogs at 390 px. The two dimensions of row 42 are checked: separate loop listeners and one shell action per click.
* `check_pack.py`: checks the pathway selector matrix, effective palette values, companion-file containment, Class A findings and second-build HTML bytes. R-KO uses real HTML organiser content and measured A4 output, not dummy SVG identifiers.
* `print_companions.cjs`: generates paper resources and checks the three landing pages at 390 px.

Dependencies used: Chromium 138 from `@sparticuz/chromium` 138.0.2; Playwright from the supplied primary runtime; axe-core 4.10.3 (SHA256 `880970c081707360e64f34cea25ff91892f5bc95675b0776925b9709dd8a68bb`). Local dependency caches are ignored by Git. Standard Playwright browser download failed with network 502/timeouts; the alternate Chromium package completed and the actual browser checks ran. No failed download is counted as proof.

The served-equivalent tree is local test routing, not publication. Live education-origin HUD status and hash are recorded in `hud_origin.json`. The actual catalogue `index.html` is read from this checkout; no substitute page is fabricated. Native dialog IDs require no alias remap; row 40 exercises those actual callers and confirms no wrapper-level `showModal` failure.

Re-run with:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 _incoming/pack1r/qa/check_static.py
PYTHONDONTWRITEBYTECODE=1 python3 _incoming/pack1r/qa/check_pack.py
NODE_PATH="$CODEX_PRIMARY_RUNTIME_NODE_MODULES" "$CODEX_PRIMARY_RUNTIME_NODE" _incoming/pack1r/qa/browser_checks.cjs
```

The browser driver starts and stops its own read-only HTTP server. Runtime dependency paths may need relocating on another machine. Reports name the tested population rather than silently testing the whole estate.
