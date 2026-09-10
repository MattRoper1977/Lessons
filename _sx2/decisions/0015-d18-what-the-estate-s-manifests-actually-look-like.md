## D18 — What the estate's manifests actually look like

Three envelopes are in use and only two were known:

| envelope | example | entries carry |
|---|---|---|
| object under `sequence` | `Build/W8-W13_2026-27/manifest.json` | `file`, `week`, `id` |
| object under `lessons` | various | `file`, `week`, `id` |
| **top-level array** | `Build/v3_40min/manifest-v3.json` | `file`, `week`, `id` |

`Grow/v3_40min/manifest-v3.json` is the array form but its entries carry **no
`week`**, where its Build and Launch siblings do. That is a data gap in one
manifest, and it is why 10 lesson decks that *are* listed still cannot be
resolved.

Across `Science_Teesside`, 97 files are unclaimed by any manifest, all served.
35 are lesson decks — 25 in folders with no manifest at all, 10 the weekless
`Grow/v3_40min` entries. The other 62 are companion worksheets, pack copies,
indexes, matrices and guides, which no manifest should list. Four served pages
have no inbound link from anywhere in the estate.
