# Served proof — Summer 1 Humanities, on the publication the window builds
Build: Site `e305c446`/`3df5c730` + Lessons `1e668ee4` + Apps `ad806305`
(`domain-split/output`, the same bytes CI builds). Chromium, 390 × 844, unfiltered.

## Row 45 — the 126 panels, measured with the estate's own counter
`verify_loop.panels()` over `deck_dom.parse()` on the **published** bytes of all
18 signed lessons. Never a regex (correction from the 4× overcount).

| pathway | W01 | W02 | W03 | W04 | W05 | W06 | stages |
|---|---|---|---|---|---|---|---|
| BUILD  | 7 | 7 | 7 | 7 | 7 | 7 | 9 each |
| GROW   | 7 | 7 | 7 | 7 | 7 | 7 | 9 each |
| LAUNCH | 7 | 7 | 7 | 7 | 7 | 7 | 9 each |

**18 lessons, 9 stages each, 7 panels each, 126 panels.** The distribution is a
single bucket `(stages=9, row45=7)` ×18 — the nine-stage expectation exactly,
with no exemplar decks in this set. Record: `ROW45_su1_built.json`.

## The 50 marked-up pages, as served

**Structure (ruling 3 — a parseable whole document by DOM, not tags by grep).**
50/50 load in Chromium with `doctype=html`, exactly one `<html>` element, a real
`document.head` and a non-empty `document.body`; and in the bytes, exactly one
`<!doctype`, one `</html>`, one `</head>` and one `</body>` each. **0 structurally
bad.** Record: `FIFTY_SERVED.json`.

**Usage furniture — measured, and smaller than the order assumed.**
`usage_discovery.refresh()` injects into three populations only: the fixed hub
list, routes the registry marks `lesson_open`, and `teaching_download_pages()`.
Intersected with the 50:

| population | of the 50 |
|---|---|
| hubs | 0 |
| `lesson_open` routes (792 estate-wide) | 0 |
| `teaching_download_pages` (64 estate-wide) | **2** |

The two are `Humanities_Teesside/GROW_W27-W39_2026-27/START_HERE.html` and
`.../LAUNCH_W27-W39_2026-27/START_HERE.html`. **Both carry
`/assets/usage-client.js` and `/assets/usage.css`, once each — 2/2, no
duplication.** The other 48 (36 Knowledge_Organiser/Pupil_Resources, 12
Sources_and_checks) are outside every adapter population, as is every other KO
and Pupil_Resources page in the estate, so they were never going to take
furniture. That is the adapter's own selection rule, not a defect of this window.

So "the 50 pages with usage furniture" resolves, on measurement, to **2 pages
that take it and 48 the adapter never visits**. The STOP-R2 corrective is still
fully discharged: the refusal that blocked publication was `inject()` raising on
pages it *does* visit, and those pages now take the furniture cleanly.

**Layout control — the mark-up changed nothing.**
Pre-markup bytes (`1e668ee4^`) rendered beside the published bytes at 390 px:
`scrollWidth` **identical on 50/50**. Horizontal overflow count **20 before, 20
after**. Record: `overflow_control.mjs`.

## FINDING (pre-existing, not this window's, raised not hidden)

20 of the 50 scroll sideways on a 390 px phone, unchanged by this work:

- **17 of the 18 `*_SU1_W*_Pupil_Resources.html`** at `scrollWidth 570`
  (every one except BUILD W01)
- `GROW_W27-W39_2026-27/START_HERE.html` (415) and
  `LAUNCH_W27-W39_2026-27/START_HERE.html` (430)
- `GROW_W27-W39_2026-27/Sources_and_checks.html` (497)

570 px is a fixed-width grid or table in the pupil-facing resource sheet. These
are the pages pupils open on a phone. Recommend a named pass; no check is
touched and nothing is changed here.

## What "served" means here, and what it cannot mean

This container cannot reach the live origin. Measured, not assumed:

```
madebymatt.uk:443 -> connect_rejected
"gateway answered 403 to CONNECT (policy denial or upstream failure)"
  (curl -sS "$HTTPS_PROXY/__agentproxy/status", recentRelayFailures, 02:21:43Z)
```

So this proof is on the **published bytes** — the exact output
`build_education.py` emits from the pinned sources, which is what the
publication uploads — rendered in the browser that serves them. It is NOT a
fetch of the live origin, and must not be reported as one.

That the origin serves those bytes is proved instead by the estate's own
instrument, which runs where egress is allowed: AGX-1's *"Fetch the live estate
and compare to raw-at-SHA"* and its *"Live education bytes must equal the
committed publication, byte for byte"* step. That job was **SUCCESS on the
window head 3df5c730, run 35676183098**, and re-runs against main after deploy.
Its verdict is better evidence than a curl from here would have been, because it
compares every byte rather than one page I chose.
