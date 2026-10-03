# PACK-1R P1 authoring source

The explicit population is Sum1 W1 BUILD, GROW and LAUNCH. `content.py` is the editorial source; `content.json` is its generated, readable snapshot. `coverage_plan.json` preserves all 39 exact SoW objectives and proposed served targets. No remaining lesson is generated until P1 approval.

Run from the Lessons checkout, with bytecode disabled:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 _incoming/pack1r/source/build.py
PYTHONDONTWRITEBYTECODE=1 "$CODEX_PRIMARY_RUNTIME_PYTHON" _incoming/pack1r/source/companions.py
RUNTIME_NODE_MODULES="$CODEX_PRIMARY_RUNTIME_NODE_MODULES" "$CODEX_PRIMARY_RUNTIME_NODE" _incoming/pack1r/source/slides.mjs
```

`build.py` reads the three unchanged science exemplars for their effective palette values and imports `stage_task()` to derive the response point. It writes only inside this intake. The HTML is deterministic; `qa/pack_checks.json` records the second-build byte comparison. `companions.py` fixes DOCX properties and ZIP timestamps. Slides use native editable text and native charts with embedded data; map outlines are embedded images with source attribution. Presentation finalization refuses an existing destination, so stage a new candidate before replacing an already validated deliverable. Full binary regeneration parity is a later full-pack release check, not claimed by this P1 report.

`ne_110m_land.geojson` is Natural Earth public-domain land geometry, fetched from the Natural Earth vector repository. Maps use a simplified equirectangular projection. They omit country boundaries; markers and labels are author-added location aids. The source SVGs are retained under `qa/`.

The three landing pages under `landing/` are destined for the respective served lesson folders. Pack-root START_HERE files are companion indexes. The exact served route map is in `qa/serve.py`; it does not copy lessons into a second HTML generation.

No BUILD HUD is vendored or inlined. The served-equivalent harness fetches the unchanged education-origin HUD into memory and serves it at `/hud.js` only for the test.
