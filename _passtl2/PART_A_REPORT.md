# TL-2 PART A — Washworks rename + 1.0.1 → 1.0.2

Pass TL-2 / PR-1, 18 August 2026. Sentinel TOP `townlife-tl2-2026-08-18-TOP`.
Part A is **complete and gated**. Parts B and C are **stopped** at their own decision gates — see
`_passtl2/TL2_STOP_REPORT.md`.

## Phase 0 — all pins pass

| Pin | Expected | Measured | Result |
|---|---|---|---|
| P0-1 zip | 3,178,647 B · `c53460123b8c…` | 3,178,647 B · `c53460123b8cfd3dad771a704c50595168f5d18aaa3b9c2a0b1b19c094ae902d` | PASS |
| P0-2 contents | 197 files · 196 entries · 196 pass · integrity | 197 · 196 · 196 pass 0 fail · `unzip -t` "No errors" | PASS |
| P0-3 runtime | 304,742 B · 304,462 chars · `7d318509…` | identical on all three | PASS |
| P0-4 version markers | exactly 2 occurrences of `1.0.1` | 2 (`version:'1.0.1'`, `const VERSION = '1.0.1'`) | PASS |
| P0-5 structure | 1 inline script · `node --check` · 0 URL literals · 164 ids, 0 dupes · ends `</html>` | 1 · OK · 0/0 · 164, 0 · yes | PASS |
| P0-6 storage | writes/removes `mbm_town_life_v10` + `__mbm_probe`; reads 10; probe never read | confirmed: 10 literal keys (v10 + 9 legacy); probe written+removed, never read | PASS |

Superseded candidate correctly identified as `a7e49cf83b3a…` and **not used**.

### Two corrections to the prompt's own figures

1. **Non-ASCII count.** The house rule states 151 non-ASCII characters. The measured figure is
   **171 occurrences** (17 distinct: 62 two-byte + 109 three-byte). The 280-byte delta the rule
   quotes is confirmed exactly (62×1 + 109×2 = 280). The sha256 match is dispositive that this is
   the pinned artefact, so this is a prose error, not a different file.
2. **`id` attribute counting.** A naive `id="` grep returns 253 with 1 "duplicate" on PROTOCOL and
   would have produced a false C0-3 pin failure. The matches were the tails of
   `data-waypoint-id="…"` and `data-agent-id="…"`. With a proper attribute boundary
   (`(?<![-\w])id\s*=`), PROTOCOL is **250 / 0 duplicates** and Town Life is **164 / 0** — both pins
   pass exactly.

## A1 — scope, measured

**22 occurrences of `Washworks` across 17 lines.** (The prompt's 22 and a line-based count of 17 are
both correct in different units; a subagent reporting "17" had counted lines.)

| Class | Count | Action |
|---|---:|---|
| 1 — player-visible strings | **17** | renamed |
| 2 — `businessSynergySnapshot().garageWashworks` | **5** | **unchanged** (A3 ruling) |
| 3 — `state.laundering` (19), `LaunderingManager` (8), `state.dirtyBonds` (24) | — | **unchanged**; contain no `Washworks` token |

Also left unchanged: the business id **`laundry`**. It is a live save-schema key
(`state.businesses.laundry`); renaming it would invalidate every existing save. It is internal and
never printed, so it is Class 3 by the ruling's own logic.

## A2 — the new name

**`Northstar Exchange`** (default taken; no swap line was supplied).

Naming treatment, applied per string rather than by substitution:
- **`Northstar Exchange`** in full where it is the proper name — the location and business `name:`
  fields, and "convert at Northstar Exchange." where the same sentence already says "Northstar Garage".
- **`Exchange` / `the Exchange`** as the in-sentence shorthand, mirroring how the original used bare
  `Washworks` as shorthand for `Northstar Washworks`.

Grammatical agreement was re-read per string, as A2 requires: one article changed **`A` → `An`**
("An Exchange conversion is already running."), and two strings gained **`the`** ("into the Exchange",
"to the Exchange"). No new non-ASCII characters were introduced (verified: the v1.0.2 non-ASCII set is
a subset of v1.0.1's).

Full per-string table with byte deltas: `_passtl2/RENAME_TABLE.json` (also in the package at
`_tl2/RENAME_TABLE.json`). Net runtime delta **+2 bytes**, which equals the sum of the per-string
deltas exactly.

**These 17 strings are a proposal on voice, not a decision.** Human item 3 stands: a ledger label
reads differently on a phone than in a diff.

## A3 — persistence gate: PROVEN, and Class 2 still stays

Driven through the real purchase path on a real origin: Garage and Exchange both `owned:true, tier:1`,
live `businessSynergySnapshot().garageWashworks === true`. The payload under `mbm_town_life_v10`
(4,339 B) contains:

- **no `garageWashworks` key**, and
- **no occurrence of the string `Washworks` at all**, and
- no state key matching `/synerg/i`.

So the identifier is computed by `businessSynergySnapshot()`, never serialised — the expected branch.
Renaming it would therefore have been *safe*, and it is **still not renamed**, because it is invisible
to players and outside the ruling's scope. The gate produced the evidence; it did not license the edit.

A useful corollary: since no save contains the token at all, **the rename cannot invalidate any
existing save** — save compatibility is safe by construction, not merely by test.

Evidence: `_passtl2/A3_PERSISTENCE_EVIDENCE.json`.

## A4 / A6 — 30 checks, 30 passed

Harness: real **Chromium 1194** over a loopback **HTTP origin** (`http://127.0.0.1:PORT/townlife/?qa`),
not `page.set_content`. Results: `_passtl2/PARTA_GATES.json`.

| Check | Result |
|---|---|
| A4-1 mid-conversion v1.0.1 save loads, resumes, completes in v1.0.2 | PASS |
| A4-1 payout identical | **£740** in all three runs: v1.0.1 live, v1.0.1 seeded, v1.0.2 seeded (amount 320, rate 0.75) |
| A4-2 bonds 250, no conversion → starts under the new name | PASS |
| A4-3 legacy normaliser executes (`v01`, profile Legacy, cash 777 → schema 10, persisted under v10, v01 kept) | PASS |
| A4-4 fresh-save default role `Resident` | PASS |
| A6 version declarations read 1.0.2 · schema still 10 | PASS |
| A6 synergy still fires · conversion starts and completes | PASS |
| A6 no `Washworks` in rendered text · ledger renders "Northstar Exchange" | PASS |
| A6 390 px horizontal overflow | **0** (scrollWidth 390 = clientWidth 390) |
| A6 44 px rendered touch floor | **12 visible controls scanned, 0 under 44 px** |
| A6 zero console/page errors, desktop and 390 px | PASS |

**A4-1/A4-2/A4-3 failed on the first run and the cause was my harness, not the rename.** First boot
schedules `setTimeout(saveNow, 2400)`, which fired after a post-load `setItem` and overwrote the seed
with default state; and a freshly written v10 save outranks a legacy key in `loadState()`'s
`[SAVE_KEY, ...LEGACY_KEYS]` order. Fixed by seeding through `addInitScript` before any page script
runs. A **v1.0.1 control run through the identical seeding path** was added so "same payout" is a
measured comparison rather than an assertion.

**A4-3 scope, stated exactly as TL-1 D5 established it:** this proves the legacy code path executes.
It is **not** evidence of nine real historical save formats, and that wording is not re-inflated here.

## D3 — real-origin storage, closed locally

TL-1 recorded D3 `UNPROVEN-ON-REAL-ORIGIN` because managed Chromium's `URLBlocklist: ["*"]` blocked
`file://` and loopback before document commit. **That constraint does not apply in this session.** On
`http://127.0.0.1:PORT` the runtime reports `storage: "local"` (not `volatile memory save`),
`localStorage` is writable, and `mbm_town_life_v10` is written and re-read across a reload.

This is the substance of D3 on a genuine origin. The remaining, distinct dimension — the *deployed*
bytes on `https://madebymatt.uk/townlife/` — still awaits Part B (B6-1) and Matt's phone tap, so D3 is
**closed on the local-origin question and open on the deployed-origin question**. It is not claimed as
fully closed.

## A5 — version bump and identity

- Both literals `1.0.1` → `1.0.2`. Considered **alone**, the edit leaves byte length unchanged at
  304,742 and yields **`differing_positions == 2`** (bytes 39248, 40032).
- The string `1.0.1` was **not** banned globally. It is 0 in the runtime because both live occurrences
  were the version markers; changelog, release-note and verification-report references to 1.0.1 are
  correct history and **stay**.

| Measure | v1.0.1 | v1.0.2 |
|---|---|---|
| UTF-8 bytes | 304,742 | **304,744** |
| Characters | 304,462 | **304,464** |
| SHA-256 | `7d31850989bd…` | **`3605124fda9387c71fc1a7c02091d1110f5d82363ec7788de4ea90757d6e38da`** |
| Inline script SHA-256 | `0a6b44170737…` | `7de03505e01fd0815f99f398c3bf4b0bdd06fc92fc73591bd1e47d58ea7dba84` |

Package: **203 files · 202 checksum entries · 202 OK / 0 FAILED** · zip 3,191,350 B ·
sha256 `10cac0b135dda6661d0a68ccb94cd338d61a4539ce79857c740ef77135c44f3c` · `unzip -t` clean.
`RELEASE_MANIFEST.json` runtime identity regenerated (it asserted the old hash) and an
`evidenceTreeProvenance` field added; `status: HELD` / `published: false` remain true.

**The 196-file evidence tree is inherited, not re-proven.** It was produced against `7d318509…` and
no longer matches the shipped runtime. The packaged `qa/QA_SYSTEM_RESULTS.json` 99/99 describes the
**v1.0.1** binary and has not been re-run in full against v1.0.2 — it must not be quoted as if it had.
Full statement in `V1_0_2_IDENTITY.md`.

## Documentation

Renamed where a doc makes a **live claim** about the shipped build: `README.md` (4),
`TECHNICAL_ARCHITECTURE.md` (1), `ORIGINALITY_AND_SAFETY_NOTES.md` (2).

Left unchanged as **history**: `CHANGELOG.md` (2), `GOLD_MASTER_RELEASE_NOTES.md` (1),
`VERIFICATION_REPORT.md` (1) — each records what v1.0.1 did or did not change, and the `_tl1/` and
`qa/` trees are frozen evidence of that build. Rewriting them would falsify the record, on exactly the
principle A5 uses to protect 1.0.1 references. A new v1.0.2 changelog section was prepended.

## Still unexecuted — listed, not dropped

Firefox, WebKit, Chromebook, Android, iOS, physical thermal/low-power, human screen-reader and
motor/cognitive evaluation, genuine v0.9–v0.1 save artefacts.
