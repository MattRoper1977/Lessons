# ESTATE MAP — 2026-09-06 (Order HC1, P0)

Token: `mbm-two-domain-healthcheck-2026-09-06-HC1`. Written from the repos themselves on
2026-09-06; every fact below was measured in this session, not carried from Appendix A.
Where a measurement could not be taken from this venue it says so.

## 0. Venue

| item | measured |
|---|---|
| Repos reachable (cloned) | `MattRoper1977/Lessons` (full clone), `MattRoper1977/mattroper1977.github.io` (depth 400 + pinned SHAs), `MattRoper1977/Games` (depth 40), `MattRoper1977/Matt-s-Apps-` (depth 80 + pin). `MattRoper1977/Games-` (pushed 2026-07-16) not cloned: pre-split leftover, read-only, purpose = old shelf copy; not part of either publication. |
| Auth identity | `MattRoper1977` (GitHub API `get_me`) |
| `https://madebymatt.uk/`, `https://madebymatt-play.uk/`, `www.` of each | **NOT reachable**: egress proxy answers 403 on CONNECT. |
| Origin-witness route used instead | CI runs on GitHub-hosted runners: Lessons `fieldops-p2-and-sweep.yml` job *Merged is not served* (`tools/verify_served.mjs`, byte-identity to the deployed Pages artifact), Site `mbm-deployment-provenance.yml` + `published-completion-verify.yml`, Games `play-domain-publication.yml` job *verify-published*, Apps `mbm-cross-estate-unification.yml` job *live-proof*. Their latest logs at the HEAD SHAs below were read through the Actions API. |
| Actions artifacts | Metadata readable; the zip download redirects to `*.blob.core.windows.net`, which the proxy also blocks. So the four published trees were **rebuilt locally from the exact pinned sources with the exact pinned builder** (see §3) and every offline measurement in HC1 was taken on those trees. |
| Pages settings API (`/repos/*/pages`) | 403 — "not permitted through this proxy". Not guessed. Indirect measurement: each repo's publication workflow reads its own Pages config and only runs the `deploy` job when `build_type == 'workflow'`; that job ran and succeeded on every repo (job ids in §2). |
| Rulesets (`/repos/*/rulesets`, measured) | Lessons **0** · Apps **0** · Site **1** (`21475918` "FIN required checks (main)": *Fetch the live estate and compare to raw-at-SHA*, *Static gates*, *Gates are proven red, not just green*, *verify*) · Games **1** (`21475919`: *contract*, *aggregate*). |

## 1. Domain → repo → path prefix → what lives there → how it deploys

| domain | repo | HEAD (main) | serves | what lives there | deploys via |
|---|---|---|---|---|---|
| `madebymatt.uk` (education) | `mattroper1977.github.io` | `d9115711a989da54229441c3ae64549aa1d5f0eb` | `/` | homepage, audience homepages `/for/*`, `/resources/`, `/tools/`, `/teach/`, `/education-hub/`, `/start/`, `/stats/`, `/account/`, `/members/`, `/mailing-list/`, `/privacy/`, teacher tools (`/uas/`, `/asdan/`, `/artsaward/`, `/evidence-binder/`), `/game-saves/` (export only), search index, **stubs** for every former game route | `education-publication.yml` on push to main: builds `education-site` with `domain-split/build_education.py` from its own SHA + Lessons pin `5ba6271` + Apps pin `2db4a9c`, uploads Pages artifact, `deploy-pages`. Last: run 34043927215, deploy job 101515683894 ✓. |
| `madebymatt.uk/Lessons/` | `Lessons` | `904a3c1a6d065438b763048cc9f51221c2e636ad` | `/Lessons/` | every lesson deck, hub, pathway tree, printable, teaching pack; `resources.json` (filtered copy); **stubs** for `Games/*.html` and the six other former game routes | `education-pages.yml` → reusable `mattroper1977.github.io/.github/workflows/education-publication.yml@ff764b65` (builder pinned) with Lessons = its own SHA, Apps pin `2db4a9c`. Last: run 34038868201, deploy job 101502049570 ✓. |
| `madebymatt.uk/Matt-s-Apps-/` | `Matt-s-Apps-` | `96d160f0326160ab88da301ec28d0130b6c446fb` | `/Matt-s-Apps-/` | 30 studios/tools + 4 science investigations + master hub; `apps.json` | same reusable workflow at `ff764b65`, Apps = its own SHA, Lessons pin `5ba6271`. Last: run 34038531016, deploy job 101501121788 ✓. |
| `madebymatt-play.uk` (games) | `Games` | `ec5ee7bb2724dc0219a53b7e60508b42bbd2a051` | `/` | 62 canonical games (35 from Site dirs, 27 from `Lessons/Games/`), 6 classroom activities + 1 staff activity (all Lessons files), games home (`/`, `/games/`, `/Games/`, `/main/`, `/for/pupils/`, `/Lessons/` all = games home), `/privacy/`, `/stats/`, `/game-saves/` (import), `games.json` mirror, `data/domain-catalogue.json` | `play-domain-publication.yml` on push to main touching `games.json` / `play-publication.json` / the workflow: builds with `domain-split/build_publications.py` from `play-publication.json` pins **Site `ff764b65` + Lessons `78ff8fc9`**, verifies Pages cname ∈ {madebymatt-play.uk, www} and HTTPS 200 on `/data/domain-catalogue.json`, `deploy-pages`, then `verify-published` (browser). Last: run 34038125168, deploy 101499958375 ✓, verify-published 101499986608 ✓. |

**Note on pins.** The three education publications do not all build from the same
Lessons commit: `/Lessons/` is built from Lessons HEAD, but the Site root and Apps
publications embed Lessons discovery data from pin `5ba6271` (a commit on the PR #338
branch, squashed into main as `e7dcbfb`). Play embeds Lessons at `78ff8fc9` (same PR
branch, head). Lessons main has moved one commit (`904a3c1`, verifier-only) since, so
today the pins and main are content-equivalent for every published lesson file. Any
future lesson edit requires a reviewed pin bump in Site (`education-publication.yml`)
and Games (`play-publication.json`) before it appears in Site-root discovery or on play.

## 2. Route census (derived from the canonical manifests and the rebuilt trees)

Manifests, by name:
- Site `reports/v6fin/V6FIN_W7_69_ROUTE_CENSUS_2026-09-03.json` — **69** game routes (62 canonical-shelf + 7 w7-additional). The play builder's source of truth.
- Games `games.json` — **62** shelf rows; Site `data/source-manifests/games.json` is its byte mirror and is what play publishes as `/games.json`, `/Games/games.json`, `/data/source-manifests/games.json`.
- Site `data/mbm-search-index.json` — 747 entries in source (491 lesson, 138 resource, 72 game, 24 app, 13 tool, 9 page); **677** in the published education copy (game category removed; counts block rewritten).
- Lessons `resources.json` — 737 rows (460 `lesson` + 80 `Lesson`, 88 teacher, 43 support, 22 pupil, 11 hubs, 2 revision, **31 `game`**); the published copy is filtered of game rows.
- Apps `apps.json`; Games `play-publication.json` (domain, pins, 62 + 7 counts).
- Site `domain-split/education_policy.py` — the classification ruling: `EDUCATIONAL_ACTIVITIES` (8 retained routes), `MIGRATIONS`; `build_education.py` `LEGACY` (5 old-path aliases).

Manifest ↔ tree disagreements (each its own line):
- search index has **72** game entries vs the **69** census: the three extras are `/Lessons/5 Intervention 10/Lesson_VIR_Intervention.html` (ruled educational, retained on edu), `/Lessons/5_6 Local Choice/Trekkers_Trail_Runner (2).html` and `/Lessons/Games/Voxel_Frontier.html` (legacy aliases → stubs). Consistent with the ruling; not a defect.
- `resources.json` lists 31 `game` rows but `Games/` holds 31 files of which 6 are not `game` rows (`Axiom_Shift`, `Charcoal`, `Glitch_Clash`, `Hold_the_Mark` are in the census under Site's index; `Off_Brand`, `Orbital_source` are legacy aliases). All 31 `Games/*.html` publish as stubs regardless (builder rule `relative.startswith('Games/')`).
- Site `data/source-manifests/games.json` = Games `games.json` byte-for-byte (the play workflow asserts it; `Site shelf mirror is not stale` green 2026-09-03).

Counts per published tree (rebuilt, see §3):

| tree | files | html | full pages | game-moved stubs | other stubs |
|---|---|---|---|---|---|
| education-site `/` | 187 | 81 | 34 | 42 (every former Site game dir + `/games/` + `/Games/` + `/experiences/medevac-frontier/` + `/resources/medevac-frontier/` + `/next/games.html`) | 5 (`/next/*` design previews → "Continue to Made by Matt Education") |
| education-lessons `/Lessons/` | 2051 | 1225 | 1188 | 37 (31 `Games/*.html` + 6 other former game routes) | 0 |
| education-apps `/Matt-s-Apps-/` | 106 | 60 | 60 | 0 | 0 |
| play `/` | 465 | 81 | 81 | 0 | 0 |

Education routes (full pages): **1282** · game routes on play: **69** (62 games + 7 activities) · apps: **60** · stubs on education: **84**.
Every stub: 1.1–1.2 KB, `<meta name="robots" content="noindex">`, plain text, one "Open the game" link to the play URL (query/hash carried across by 3 lines of script), link to `/game-saves/` export and `/for/pupils/`. **No `rel=canonical`** to the play URL (order's stub definition asks for one — see HC1 ledger).

## 3. How the trees were reproduced here

| tree | builder (Site) | Lessons source | Apps source | local output |
|---|---|---|---|---|
| education-lessons | `ff764b65` worktree | `904a3c1` (main) | `2db4a9c` | `/home/user/work/out-A/education-lessons` |
| education-apps | `ff764b65` | `5ba6271` | `96d160f` (main) | `/home/user/work/out-B/education-apps` |
| education-site | `d911571` (main) | `5ba6271` | `2db4a9c` | `/home/user/work/out-C/education-site` |
| play | `ff764b65` | `78ff8fc9` | — | `/home/user/work/out-D/games` |

All four builds reported the same counts CI reports (69 payloads, 0 missing initial-load refs; 187 / 2051 / 106 output files). Byte identity to the deployed artifacts could not be asserted from here (artifact storage blocked); it is asserted in CI by `verify_served.mjs` (Lessons: "44 served byte-identical · 0 red · 0 inconclusive", run 34038867832) and `verify_deployment_provenance.py` (Site: 9 witnesses byte-identical at `d911571`, run 34044012989).

## 4. Shared-asset table — which origin serves each now

| asset | education `/` (Site) | `/Lessons/` | `/Matt-s-Apps-/` | play | notes |
|---|---|---|---|---|---|
| `hud.js` | yes (33 966 B, `716c4474…`) | no | no | yes (33 494 B, `fbf0eef7…`) | play copy has `HOMES` rewritten to the games homepage only; all `https://madebymatt.uk` literals replaced by the builder |
| splash `assets/brand/mbm-splash.js` | yes | no | no | yes | identical bytes (`0bb61e56…`) |
| sports passport (`houseolympiad`, `apexpool`, …; keys `mbm_*passport*`) | no | no | no | **yes only** | expected: passport is a game concern |
| account / Members / sync (`/account/`, `/members/`, `assets/mbm-account.js`, Supabase) | **yes only** | no | no | no | play has no account surface; no Supabase reference in the play tree |
| search index `data/mbm-search-index.json` | yes (677 entries, no game category) | — | — | no; play has its own `data/domain-catalogue.json` (62 games, 6 activities, 1 staff) | education also ships `data/domain-catalogue.json` (765 education + 564 pupil rows, 3 external GitHub links) |
| service worker | **none** | none | none | `micro-tinkerer/sw.js` only (game-scoped) | no estate-wide SW exists on either origin; Appendix A's "SW from the resilience layer" is GONE |
| shared CSS/JS `assets/mbm-platform.css` / `.js`, `styles.css`, `theme.js` | yes | `assets/mbm-platform.*`, `assets/mbm-theme.js`, `assets/mbm-hub.css` (generated copies, contract-tested) | same as Lessons | `styles.css`, `theme.js`, `assets/mbm-platform.*` (js host-rewritten) | |
| lesson navigation adapter `assets/catalogue/lesson-navigation.js` | — | yes (injected into every published lesson by the builder) | — | — | not in source decks; served-only |
| game-save transfer `assets/game-saves.js`, `data/game-storage-allowlist.json`, `/game-saves/` | yes (export leg) | no | no | yes (import leg) | identical bytes; the allowlist must stay byte-identical (policy) |
| education navigation `assets/education-navigation.css`, `shared-navigation.*`, `usage-client.js` | yes | via absolute `/assets/...` URLs | via absolute | no | |

## 5. Origin-scoped state (P1 1.4 summary)

localStorage/sessionStorage keys are per origin. Census of the served trees:
- education: `mbm_reading_theme` (theme preference: exists on both origins, **expected** not to carry), `ps_coldcall_roster` (100 lesson pages), `mbm_primary_read`, `mbm_tt_evidence`, per-lesson class keys; `BroadcastChannel` in liveteach (`LT.CHANNEL`, same origin). IndexedDB in apps studios and `/account/`.
- play: per-game keys (`voxelcraft:*`, `gc_*`, `mbm_titanforge_*`, `apexkick.v4.*`, `MICRO_TINKERER_SAVE_V2`, …), `BroadcastChannel('mbm_vector_overdrive_scores')`, 1 SW (micro-tinkerer).
- **BROKEN-BY-CONSTRUCTION, handled:** every game save that lived on `madebymatt.uk` is unreachable from play; the estate ships an explicit export (`madebymatt.uk/game-saves/`) → import (`madebymatt-play.uk/game-saves/`) route with a byte-pinned allowlist. Not silent.
- **EXPECTED:** passport on play only; account on education only; reading theme per origin (documented on `/stats/` copy: "Education and Play have separate choices").
- **No lesson reads a game's evidence key** (no `Lessons` page references a key that only a play page writes) — measured by key intersection of the two trees: the only shared keys are `mbm_reading_theme` and `ps_coldcall_roster` (the latter written by the Kids-vs-Staff activity on play and by lessons on education; classroom rosters are session-local, no cross-origin expectation found).
- Config outside the repos: Supabase allowed origins/redirects need **only `https://madebymatt.uk`** (no account on play) — unchanged by the split; FormSubmit forms remain on `madebymatt.uk` (`/privacy/`, `/thanks/`, contact form in `mbm-platform.js`) — unchanged; Ko-fi pills are links only.

## 6. Reorg archaeology

| repo | last pre-split SHA | first split commit | record |
|---|---|---|---|
| Site | `bb5f97a2f185aa603cc394d0a3ddbd16ceab72ad` (2026-09-04, #254) | `b7f86aed97860d1f9a60e60b2430987576e7f78c` (2026-09-05 "Prepare separate learning and games redesign for domain selection") | `domain-split/README.md` (+ "Education-only publication contract (6 September 2026)"), `domain-split/config.json` (`site_source_commit` = the pre-split SHA) |
| Lessons | `ccbe7a8bd70692fbf5a6c5352c7bf823c54f463f` (2026-09-05, #326) | `db697e5dc971a0afb0de0c57f072452b9b3705bb` (#328 "Prepare filtered education publication without changing source lessons") | `233b60c` "Bind served proof to deployed publications after domain split" (verifier); no MIGRATION/REORG doc in Lessons |
| Games | `fb15334283ea40475094ba0546527535fff5f622` (2026-09-03, #52) | `320aa2a5cb8b11a90716f35ec2bfc2be55db2ebc` (#53 "Prepare standalone games publication for madebymatt-play.uk") | `docs/play-domain.md` |
| Apps | `e1e4b8f6d2d1c919f81f9a2023d5fdf1ad027ed6` (2026-09-04, #23) | `7d54019d8ab99ad522a74ea9fb43f9d21eaed237` (#24 "Prepare separate education Apps publication") | — |

No game *files* moved between repos. The split is a **publication-time filter**: source games stay in `Lessons/Games/` and the Site game directories; the builders decide which origin serves them. There is no move commit to cite.

Prior-order tokens found in the ledgers (so finished work is not redone): GS1 (19 Lessons files / 15 Site), SC2 (48 / 11), SC3 (35 / 6), VB run 14 (12 files; `_sownb/TERM_DATES.md` is its section C), VB run 15 (2), V6FIN (6 / 8: W7 69-route closeout `65b87f3` 2026-09-03 is CLOSED at 69/69 SHIP), TS (Site `reports/…` Order TS P1 closed 2026-08-25). The V6 site release (#234 in Appendix A) is GONE as a PR: its content shipped through #246–#270.

## 7. Open PRs (markers · touch set)

Lessons (12): #118 **PARKED — DO NOT MERGE** (tools/coa/*) · #117 (tools/scrapcore/*) · #116 **REFERENCE DIFF — DO NOT MERGE** (tools/vcl/*) · #94 draft (.github trigger file) · #93 draft (Games/Orbital*, chemistry/Lesson2_pH_Scale_v4.html, index.html, a workflow) · #45 **HELD** (ASDAN_Lundy/EVIDENCE_STATUS_AND_CLAIMS.html, HANDOVER, REGISTER, _close/OPEN_ITEMS, _semh2/*) · #43 **HELD** (Art_Teesside/Launch/Printable_LAUNCH_Evidence_and_Lundy_Pack.html) · #35 **HELD** (Art_Teesside/Build/BUILD_ART_A2_W1–W7 + 24 more Art files) · #31, #30, #26 (Art_Teesside/Build/BUILD_ART_A2_* + verify-art-teesside workflow) · #17 (grow-anim/wire_lessons.py + node_modules).
Site (6): #216 (echovault/hyperdraft/medevac/neonmeridian/novasiege/rallyvector3d/townlife index.html + splash tool) · #109 draft · #106 · #96 (docs) · #91 draft (assets/mbm-features.js, ouroboros/index.html, tools) · #25 **HOLD** (index.html, privacy/, thanks/).
Games: none. Apps (2): #4 draft (qa/*) · #2 (index.html).
Route ownership for HC1 edits therefore excludes: `Art_Teesside/Build/BUILD_ART_A2_*`, `Art_Teesside/Launch/Printable_*`, `ASDAN_Lundy/EVIDENCE_STATUS_AND_CLAIMS.html`, `Games/Orbital*`, `chemistry/Lesson2_pH_Scale_v4.html`, Lessons `index.html`; Site `index.html`, `privacy/`, `thanks/`, the seven #216 game pages; Apps `index.html`.

## 8. Workflows — latest conclusion on main (2026-09-06)

Lessons (17 on main): all green at HEAD except three last run before the split by dispatch only — `j4-absolute-ref-probe` (2026-08-05), `wave-ohm-deck-live` (08-12), `glv3-production-byte-check` (08-22). Reds on 2026-09-06 at `e7dcbfb` (`fieldops` served job INCONCLUSIVE: games publication still in progress inside the 240 s wait; `unification` live-proof: verifier read the raw source menu instead of the published one — repaired by #339) are green at `904a3c1`. `watch-main` 396/397 reds are those same runs being reported.
Site (52 on main): `Education publication`, `Published Education completion`, `Deployment provenance`, `Professional site live verification`, `Domain split publication`, `The way out of every declared game` green at `d911571`/`1273a84`. **`Estate check health` red** on its 2026-08-31 schedule (see HC1 ledger). Several game live-verifiers last ran before the split and still fetch game routes on `madebymatt.uk` (P2.5 finding, listed in the ledger).
Games (8): all green; `play-domain-publication` green at `ec5ee7b`.
Apps (8): all green at `96d160f`; `unification` reds at `9a96172`/`9b2d933`/`b83cdec` were the same verifier defect, fixed by Apps #34.

## 9. Appendix A reconciled line by line

| Appendix A line | verdict |
|---|---|
| Site repo served madebymatt.uk with 31 games at `/<game>/` | CHANGED-TO: Site serves madebymatt.uk education only; its 35 game dirs publish as stubs; the games serve at `madebymatt-play.uk/<game>/` from the Games repo's Pages. |
| Lessons served `/Lessons/` with 28 games at `Games/<file>.html` | CHANGED-TO: `/Lessons/` still served by Lessons; its 31 `Games/*.html` (+6 other game routes) publish as stubs; 27 of them + 7 activities serve at `madebymatt-play.uk/Lessons/...`. |
| Games repo held the shelf/manifest rows | CONFIRMED, and now also owns the play publication workflow and pins. |
| Matt-s-Apps- held apps | CONFIRMED (`/Matt-s-Apps-/`, own filtered publication). |
| Canonical games manifest `data/source-manifests/games.json` (59 routes) | CHANGED-TO: 62 rows (Titan Forge, Touchline, Skybreak added 09-02/03); the 69-route census is the play builder's source. |
| shared `hud.js` at site root | CONFIRMED on education root; CHANGED-TO also a host-rewritten copy on play. |
| splash key `mbm_splash_last` | CONFIRMED (`ma_splash_*` per-game keys also present); splash script identical on both origins. |
| passport fallback literal `mbm-default00000000` | present in play tree (`houseolympiad`/sports games); GONE from education. |
| Supabase accounts/Members + seven-word sync | CONFIRMED, education origin only. |
| Ko-fi pills on adult pages only | CHANGED-TO: Ko-fi *links* also appear in the `mbm-support-footer` on `/Lessons/` hubs including pupil-reachable subject hubs (P1 1.9 finding). |
| SW + projector/sensory modes from the resilience layer | GONE: no service worker on either origin except `micro-tinkerer/sw.js`; projector kit = `Lessons/liveteach/` (no SW). |
| Open PRs Site #234, #235, #220, #219, #216, #218, #91 | #234/#235/#220/#219 GONE (merged or closed); #218 merged 09-02; #216 and #91 CONFIRMED open. |
| Lessons 13 open incl. PARKED / DO NOT MERGE | CHANGED-TO: 12 open, markers confirmed. |
| mains: Lessons `c2a9c725`, Site `6723b146`, Games `a320144a` | CHANGED-TO: Lessons `904a3c1a`, Site `d9115711`, Games `ec5ee7bb`, Apps `96d160f0`. |
| rulesets measured 0 on 26 Aug | CHANGED-TO: Site 1, Games 1 (both created 2026-08-25 19:34 UTC), Lessons 0, Apps 0. |

## 10. R12 check

- Every route in §2 has exactly one serving origin **except two files published in full on both**, by written ruling (`education_policy.py` `EDUCATIONAL_ACTIVITIES` + play "Classroom activities / For staff"): `/Lessons/5 Intervention 10/Lesson_VIR_Pupil_App.html` and `/Lessons/LundyLoop/5_staff_training/R_Gate_Calibration_Game.html`. The same *paths* `/`, `/main/`, `/for/pupils/`, `/Lessons/`, `/privacy/`, `/stats/`, `/game-saves/`, `/404.html` exist on both origins with **different** documents (each domain's own front door); that is by design, not a leak.
- No repo without a nameable purpose. `Games-` is an unused pre-split leftover.
- Decision recorded in the readback: the dual publication is documented, not ambiguous, so measurement continued; nothing served was changed without Matt.


## HC3 recovery addendum

The map above is restored verbatim as HC1 historical evidence. Current publication refs, proof SHAs, source ownership, changed Ko-fi treatment and unresolved boundary limitations are recorded in HC3_HEALTH_2026-09-06.md beside it. The domains and repo/path ownership remain the same. Do not treat the historical HEADs, counts or proxy limitations above as a fresh HC3 measurement.
