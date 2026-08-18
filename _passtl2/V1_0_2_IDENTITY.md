# Town Life v1.0.2 — executable identity

Produced by TL-2 Part A on 18 August 2026 from the canonical `MBM_Town_Life_v1_0_1_FINAL` package.

## Runtime identity

| Measure | v1.0.1 (previous) | v1.0.2 (shipped) |
|---|---|---|
| Path | `MBM_Town_Life_GOLD_v1_0.html` | `MBM_Town_Life_GOLD_v1_0.html` |
| UTF-8 bytes (`wc -c`) | 304,742 | 304,744 |
| Characters (`LC_ALL=C.UTF-8 wc -m`) | 304,462 | 304,464 |
| SHA-256 | `7d31850989bd36849be29b2e53e72e1906ff4597ab62e81e9225fa95cae9afd2` | `3605124fda9387c71fc1a7c02091d1110f5d82363ec7788de4ea90757d6e38da` |
| Inline script bytes | 265,585 | 265,587 |
| Inline script SHA-256 | `0a6b44170737dc71c8d04a9877eee62502617257489f5b924fe2d3dbbdca3bd1` | `7de03505e01fd0815f99f398c3bf4b0bdd06fc92fc73591bd1e47d58ea7dba84` |
| `id` attributes | 164 | 164 |
| `http://` / `https://` literals | 0 / 0 | 0 / 0 |
| Save schema / key | 10 / `mbm_town_life_v10` | 10 / `mbm_town_life_v10` (unchanged) |

Byte counts are from `wc -c`/`stat`; character counts from `LC_ALL=C.UTF-8 wc -m`. The two differ by
280 because the runtime carries 171 non-ASCII characters (17 distinct: 62 two-byte, 109 three-byte).
The TL-2 prompt's house rule states 151; the measured figure is **171 occurrences**, and the 280-byte
delta it quotes is confirmed exactly.

## THE EVIDENCE TREE IS INHERITED, NOT RE-PROVEN

**The 196-file evidence tree in this package was produced against runtime
`7d31850989bd36849be29b2e53e72e1906ff4597ab62e81e9225fa95cae9afd2` (v1.0.1) and no longer matches the
shipped runtime `3605124fda9387c71fc1a7c02091d1110f5d82363ec7788de4ea90757d6e38da`.** Every claim in that tree that is *about the executable* is inherited
rather than re-proven, except the checks re-run in TL-2 A4/A6 and recorded below. The packaged
`qa/QA_SYSTEM_RESULTS.json` 99/99 result describes the v1.0.1 binary; it has **not** been re-run in
full against v1.0.2 and must not be quoted as if it had.

## What WAS re-proven against v1.0.2 (30/30 passed)

Harness: real Chromium 1194 over a loopback **HTTP origin** (`http://127.0.0.1:PORT/townlife/?qa`),
not `page.set_content`. Full results: `_tl2/PARTA_GATES.json`.

- **A3 persistence gate** — with Garage + Exchange owned, `garageWashworks` is absent from the saved
  payload, and the string `Washworks` appears nowhere in it. Computed, not persisted; Class 2 unchanged.
- **A4-1** — a v1.0.1 save written mid-conversion loads, resumes and completes in v1.0.2. Payout
  **£740** identical across v1.0.1 live, v1.0.1 seeded and v1.0.2 seeded (amount 320, rate 0.75).
- **A4-2** — a v1.0.1 save with `dirtyBonds` 250 and no conversion starts one under the new name.
- **A4-3** — the legacy normaliser executes: a synthetic `mbm_town_life_v01` fixture (profile Legacy,
  cash 777) funnels through, persists under v10, and the legacy record is not deleted.
  **This proves the code path runs, nothing more** — there are still no genuine v0.9–v0.1 artefacts.
- **A4-4** — default role on a fresh save is still `Resident`.
- **A6** — version declarations read 1.0.2, schema still 10, synergy still fires, conversion starts
  and completes, no `Washworks` in rendered text, ledger renders "Northstar Exchange", 390px
  horizontal overflow **0**, all 12 rendered visible controls ≥44px, zero console/page errors.
- **D3 (real-origin storage)** — storage mode resolves to **`local`** on a real origin, not
  `volatile memory save`. TL-1 recorded this UNPROVEN because managed Chromium's
  `URLBlocklist: ["*"]` blocked `file://` and loopback; that constraint does not apply here.
  Confirmation on the published `https://madebymatt.uk/townlife/` still awaits Part B.

## Still unexecuted — unchanged by this pass

Firefox, WebKit, Chromebook, Android, iOS, physical thermal/low-power, human screen-reader and
motor/cognitive evaluation, and genuine v0.9–v0.1 save artefacts.

## Documentation edits (live claims only)

| `README.md` | `faster Washworks conversion` | `faster Exchange conversion` |
| `README.md` | `- Northstar Washworks.` | `- Northstar Exchange.` |
| `README.md` | `**Garage + Washworks:**` | `**Garage + Exchange:**` |
| `README.md` | `garage recovery and Washworks conversion;` | `garage recovery and Exchange conversion;` |
| `TECHNICAL_ARCHITECTURE.md` | `- Washworks conversion duration.` | `- Exchange conversion duration.` |
| `ORIGINALITY_AND_SAFETY_NOTES.md` | `and Washworks conversion are abstract game systems` | `and Exchange conversion are abstract game systems` |
| `ORIGINALITY_AND_SAFETY_NOTES.md` | `- Washworks conversion is a delayed economy mechanic` | `- Exchange conversion is a delayed economy mechanic` |

History files were deliberately **not** rewritten — they record what v1.0.1 did or did not change,
and rewriting them would falsify the record, exactly as A5 protects 1.0.1 references. Residual
`Washworks` counts, all historical: {"CHANGELOG.md": 2, "GOLD_MASTER_RELEASE_NOTES.md": 1, "VERIFICATION_REPORT.md": 1}.
