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

## E — Teesside Maker Lab PRO v2.1 — COMPLETE AND PROVEN (r2)

Full record: `PART_E_REPORT_R2.md`; the r1 stop record stands as history in `PART_E_REPORT.md`.
The r1 stop was correct and the owner's r2 re-issue fixed the inventory, not the expectation —
verified here rather than trusted: 33 EXPECTED keys against 35 shipped files (the two
self-referential files uncovered by design), and every studio byte-identical to r1.

- r2 package `1b97902e…` exact; verifier 52/52; PATCH_TRUTH_PASS including the new
  `self-check EXPECTED == shipped set OK` line. The provenance note about the stale source-zip
  sidecar is carried verbatim in the record.
- Merges: Lessons **#135** → `cc560092…`; Apps **#16** → `957744e7…`; Apps **#17** →
  `6a8ae063…` (live acceptance); Site **#171** → `b912ad05…`.
- **Published bytes:** all 35 runtime files matched the merged bytes on the first attempt,
  cache-busted by merge SHA. **Live acceptance on `madebymatt.uk`: 8/8** — chip `saved 20:53`,
  shared state read back by the directly-opened studio, forged sync refused, genuine sync
  landing. The addendum makes that gate mandatory, so it was made to run on a runner rather
  than reported unreachable.
- Discovery: apps.json mirror blob-identical to the merged commit, provenance `957744e7`/38,
  seven declared leaves, Teach Hub creative-tools card. **The package's predicted search id was
  wrong** — the generator derives ids from the title, so
  `app-teesside-cross-curricular-maker-lab-pro` ships; every other spec field matches.
- Reported, not patched (payload bytes are fixed after install): the self-check's
  expected-files tile is a stale hardcoded `49`; and the launcher names its teacher rooms
  without stating they are teacher-only, though the suite is `safeForPupils:false` and every
  other Phase 8 boundary claim verified.
- Owner-held reading demand FK 15.5–18.9 stays **OPEN**, in no PR or catalogue copy.
- Sentinels echoed: `townlife-tl2-2026-08-18-PARTE-r2-TOP` / `…-BOTTOM`.
- **Token earned: `MAKERLAB_V21_MERGED_PUBLISHED_SHA_PROVEN`.**

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
| `MAKERLAB_V21_MERGED_PUBLISHED_SHA_PROVEN` | **EARNED** (Part E r2) |
| `PARTF_WAITING_ON_B` | **ACTIVE** — F listing surfaces held |
| `AFTERDARK_VENDORED_TOUCH_PUBLISHED_SHA_PROVEN` | not yet — awaits listings + live boot |
| B4/D2, C2/P1 stops | B still held on D2 line + Chromebook check; C unblocked by P1-A, rebuild ongoing |

## Everything owner-held or owed, in one place

1. B: Chromebook check (before #169/#37 merge).
2. B: the one-line D2 confirmation (verbatim above).
3. D: "Participation debt" headline label — OPEN.
4. D: closure standard vs the estate's pathway-dependent LL-I ruling — OPEN.
5. D: phone check of the live LundyLoop routes (human confirmation of the byte-proven deploy).
6. E: two package items for the next revision — the self-check's stale `49` expected-files
   tile, and a launcher line naming the Director and Moderation Hub staff-facing.
7. E: reading-demand FK 15.5–18.9 plain-language decision — OPEN.
8. F: phone check via PHONE_CHECKLIST (decides whether touch leaves the Settings override).
9. F: optional register swap line (`Afterdark register: ELIMS→OUTS, eliminated→knocked out — go`).
10. F: shelf/pupil listing pass once #169 merges or B is parked (derived counts + cross-page control).
11. PH-3 OPEN_ITEMS 42–52 stand as recorded (incl. item 52, the `_ph3` Jekyll-unserved report note).
