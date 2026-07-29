# Pass SCI-2 — Findings

Autonomy pass. Decisions made under the SCI-2 GREEN/AMBER/RED bands are logged live in
`_passsci1/DECISIONS.md`; this is the narrative companion. Full detail there.

## What was measured

**Sentinel, reconciled and made self-deriving (§1).** The disagreement (45→70 vs 51/76) was a
**universe** confusion, not an error:

- **Now (HEAD), tracked `*.html`: 70.** At the fork (`8540eee`): **45.** origin/main: **45** (the
  second writer added no loop-mark html). Delta **+25** = exactly the 25 science lessons.
- The **51** was the ALL-FILES universe (html + 6 non-html tooling/docs). That universe is
  **unstable**: it reads **79** now, not 51+25=76, because my own committed tooling (`render_v5.py`,
  `FINDINGS.md`, `sentinel.py`) also mentions the string. So the all-files number must never be
  carried; the `*.html` universe is the gate's and the one to quote.
- **The "six files"** (the 51-vs-45 gap): `LL-I_B1_measurement_map.md`, `INSTRUMENTS.md`,
  `bundle_facts.py`, `patch_loopmark.py`, `REGISTER.md`, `_passsg/FINDINGS.md` — all **non-html
  tooling/docs**, **all present** in both `8540eee` and HEAD, **never removed**, and **not** the
  second writer's (they predate the fork). They are outside the sentinel universe.
- **`_passsci1/sentinel.py`** now recomputes from git at emit time and prints the file list; a
  single filesystem grep that swept the gitignored `out/` and `pack/` artefacts returned a
  polluted **235**, which is exactly the carried-number failure mode the emitter removes.

## What was decided (GREEN — done, logged)

- **Packs rebuilt on current head** so both include the osmosis clip; the pre-clip zips were stale
  by definition. 219 html rebranded, 0 wordmark residue, x-brand every page, assessed conditions
  intact, crawl clean, both zips `unzip -t` OK. Delivered.
- Sentinel emitter written; decision log started; clip register built.

## What was flagged (AMBER)

- **The sentinel universe correction above** — it contradicts figures in my own earlier reports
  (the "51"/"76"). The number to trust is the emit-time `*.html` derivation.
- **Clip verification is impossible this session.** Oak, NASA and BBC all return **403** to the
  session fetch tool (BBC blocked outright). No new clip was wired (§4 forbids wiring the
  unverified). Candidates are staged in `_passsci1/CLIP_REGISTER.md` with honest status; the
  renderer's `clip=` field means each is a one-line change once Matt's check clears it.
- **BUILD W5 & W6 (food) left EMPTY BY DESIGN for clips** — most available food clips carry
  "healthy/unhealthy" or restriction framing, which §5 forbids at any tier. Recorded, not silent.

## What was refused (RED / rules)

- No clip wired that could not be verified — the whole clip batch stays as register candidates.
- Nothing merged; nothing pushed to `main`. Branch only. The 29 Aug sitting is Matt's.
- No frozen/assessed/protected files touched; no pupil data in any zip; no invented codes.

## Deliverables this pass
`_passsci1/sentinel.py` (self-deriving emitter) · `SENTINEL_AFTER.txt` (70, tracked html) ·
`DECISIONS.md` (live log) · `CLIP_REGISTER.md` (all 25 lessons) · `FINDINGS_SCI2.md` (this) ·
both packs rebuilt with the clip and delivered.

Nothing merges. Matt merges.
