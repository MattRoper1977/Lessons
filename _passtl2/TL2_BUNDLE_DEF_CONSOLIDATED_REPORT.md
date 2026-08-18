# TL-2 consolidated report — Bundle D·E·F close, with A/B/C status (2026-08-18)

Bundle sentinels echoed: `tl2-bundle-DEF-2026-08-18-TOP` · `tl2-bundle-DEF-2026-08-18-BOTTOM`
Bundle zip verified: `TL2_UPLOAD_BUNDLE_D_E_F_2026-08-18.zip` sha256 `36df8df3…` exact; every
BUNDLE_MANIFEST entry present with its listed SHA-256. Decoupling held throughout: A–F never shared
a branch, PR or commit; each stop landed nothing elsewhere.

## A — Town Life 1.0.2 (Washworks → Northstar Exchange) — COMPLETE (unchanged)

Landed earlier in TL-2; 30/30 runtime gates. See `PART_A_REPORT.md`. No bundle work touched it.

## B — Publish Town Life — HELD (unchanged), two items owed by Matt

Site PR **#169** + Games PR **#37** remain open and untouched. Owed:
1. **Chromebook check** before the merges (pupil-homepage placement = pupil use; throttled proxies
   measured 5.17–7.11 fps at 6×).
2. **D2 mechanism confirmation**, one line: `D2 confirmed — hand-edit the pupil page, derived
   counts — go`.

## C — PROTOCOL de-brand/rebuild — IN PROGRESS on its own track

Stopped correctly at C2/P1 in the first pass (census + pins reproduced first, nothing edited);
Matt's **P1-A ruling (original layouts)** authorises a rebuild, which is underway as its own
workstream. Nothing C-related was landed by this bundle; the pinned runtime
(`aca3ea1e…`, 374,402 B) and the C1 census stand as the baseline. Remaining: three original
layouts, C3 rename map, C4 register, C5 gates (census + control), C6 dual-surface placement —
sequenced against B/F for `/for/pupils/` per the one-open-PR rule.

## D — LundyLoop Professional OS v2.1.1 (r4) — COMPLETE AND PROVEN

Full record: `PART_D_REPORT.md` (r4 section appended beneath the preserved r3 stop).
- r4 package `1444acb9…` exact; verifier 48/48; **PATCH_TRUTH_PASS, all 22 counts** (the r3
  `'Pupil / scribe'` deviation now truly 0/0 via P9).
- Merges: Lessons **#134** → `5bfba624…`; Apps **#15** → `9672d6b7…`; Site discovery **#170**
  (12/12 checks) → `595b4d09…`. All post-merge workflows green in all three repos (Apps 4/4 at
  `9672d6b7`, Site 9/9 at `595b4d09`, incl. live verification + deployment provenance).
- Phase 7 live proof: runner-side `live-bytes` **PASS attempt 1** — all 9 renderable payload files
  serve byte-exact at the production origin (flagships `97a84d6b…` root / `dec36308…` suite);
  Pages deploy provenance direct (run 32175136356 at the merge SHA). Browser-vs-production LIMITED
  (session proxy) with compensating runner-side proof; Matt's phone check is the human confirm.
- Phase 10 screenshots delivered (pupil mode mobile; staff-proxy REVIEW_DUE), fictional demo data,
  cleared after and proven cleared.
- Owner-held items restated OPEN: "Participation debt" label · closure standard vs LL-I.
- Sentinels echoed in the D record: `townlife-tl2-2026-08-18-PARTD-r4-TOP` / `…-BOTTOM`.
- **Token earned: `LUNDYLOOP_V2_MERGED_PUBLISHED_SHA_PROVEN`.**

## E — Teesside Maker Lab PRO v2.1 (r1) — STOPPED at Phase 4, zero repo writes

Full record: `PART_E_REPORT.md`. Sequenced after D's Apps merge as ruled; package gates PASS
(52/52 + PATCH_TRUTH_PASS); install/parity/pin/static/browser gates all green including the
**acceptance test** (autosave chip "saved HH:MM", unified `MBM_MAKER_PRO_V2_*` state), the
**forged-postMessage control**, and reduced-motion — then the mandatory `RELEASE_SELF_CHECK.html`
gate failed on its first honest browser run: **CHECK FAILED · 18 issues (49 checked / 32 passed)**.
All 32 present files byte-match; the EXPECTED inventory was regenerated against the source-release
tree (17 unshipped `qa/` artefacts expected, shipped `PATCH_NOTES_v2.1.md` not inventoried).
Fix requires editing a payload byte after install → addendum E4 stop condition. Local branches
deleted un-pushed; **zero E writes in any repository**. Owner-held FK 15.5–18.9 reading-demand
restated OPEN. Awaiting an r2 package.
Sentinels echoed: `townlife-tl2-2026-08-18-PARTE-TOP` / `…-BOTTOM`.
- **Token NOT earned** (by design of the stop). Stop recorded: Phase-4 package-truth failure.

## F — NEON RIFT: AFTERDARK — DEPLOYED UNLISTED; listing held `PARTF_WAITING_ON_B`

Full record: `PART_F_REPORT.md`. Identity gate exact (`706b337b…` zip / `0fbbad3c…` inner HTML);
F1–F8 reproduced red then fixed; three.js 0.185.1 vendored with per-file hashes + MIT license;
touch layer shipped **behind the Settings override, default OFF** (SwiftShader harness measured
6.3 fps vs the 30 fps floor — honest red; real verdict is Matt's phone). Games PR **#38** merged →
main `52fa624a…`; Pages deploy success (run 32177423202); repo bytes at the merge SHA hash-verified
via raw. Live-route browser boot LIMITED (production origins proxy-blocked); PHONE_CHECKLIST in the
F record. Register census reported unchanged; ships as-is absent the owner's swap line. Shelf,
`/for/pupils/`, catalogue, genre counts: **held** — #169 unmerged, B not parked.
Sentinels echoed: `townlife-tl2-2026-08-18-PARTF-TOP` / `…-BOTTOM`.
- **Stop token: `PARTF_WAITING_ON_B`** (listing surfaces only).
- `AFTERDARK_VENDORED_TOUCH_PUBLISHED_SHA_PROVEN` not emitted — reserved for the fully published
  state (listings + live boot).

## Every token / stop across TL-2, in one place

| Token | State |
|---|---|
| `LUNDYLOOP_V2_MERGED_PUBLISHED_SHA_PROVEN` | **EARNED** (Part D r4) |
| `PATCH_TRUTH_FAILED` | r3 historical stop, ruled correct, superseded by r4 |
| `MAKERLAB_V21_MERGED_PUBLISHED_SHA_PROVEN` | not earned — E stopped (Phase-4 package truth) |
| `PARTF_WAITING_ON_B` | **ACTIVE** — F listing surfaces held |
| `AFTERDARK_VENDORED_TOUCH_PUBLISHED_SHA_PROVEN` | not yet — awaits listings + live boot |
| B4/D2, C2/P1 stops | B still held on D2 line + Chromebook check; C unblocked by P1-A, rebuild ongoing |

## Everything owner-held or owed, in one place

1. B: Chromebook check (before #169/#37 merge).
2. B: the one-line D2 confirmation (verbatim above).
3. D: "Participation debt" headline label — OPEN.
4. D: closure standard vs the estate's pathway-dependent LL-I ruling — OPEN.
5. D: phone check of the live LundyLoop routes (human confirmation of the byte-proven deploy).
6. E: an r2 package fixing the RELEASE_SELF_CHECK inventory (two shapes offered in the E record).
7. E: reading-demand FK 15.5–18.9 plain-language decision — OPEN.
8. F: phone check via PHONE_CHECKLIST (decides whether touch leaves the Settings override).
9. F: optional register swap line (`Afterdark register: ELIMS→OUTS, eliminated→knocked out — go`).
10. F: shelf/pupil listing pass once #169 merges or B is parked (derived counts + cross-page control).
11. PH-3 OPEN_ITEMS 42–52 stand as recorded (incl. item 52, the `_ph3` Jekyll-unserved report note).
