# LIVETEACH_RECON — Phase 0 of the Live-Teach Projector Kit

Recon and decisions for the Live-Teach Projector Kit (master prompt, 2026-08-25).
No product code in this phase. Measured at HEAD `4a86bc3` unless a line says
otherwise; every load-bearing claim carries a `file:line` citation from that HEAD.

---

## Plain summary (read this bit on your phone, Matt)

**What happened:** I read the whole estate — the shared HUD, the theme engine,
the splash and exit conventions, every class-list storage key, and all twelve CI
workflows — before writing any code. Everything is documented below with file
and line references.

**Your three answers, recorded:**

| Q | Answer |
|---|---|
| Q1 — classroom PC + extended desktop + USB clicker? | **No / not sure** |
| Q2 — cold-call on the projector? | **HUD-only, with an explicit "project name" button** |
| Q3 — which repo? | **This one (Lessons)** — the tool would serve at `madebymatt.uk/Lessons/liveteach/` |

**What that means:** the master prompt's own stop condition fires. The projector
half of this tool (Phases 1–5: projector window + teacher window kept in sync,
clicker, telestrator, stage spotlight) only works as **two windows of the same
browser on one machine** — the classroom PC driving the projector. Your phone
cannot be the remote for it. So per the plan, **I stop after this phase and wait
for you** rather than building six phases of sync architecture that may have no
machine to run on.

**How to check, next time you're in the classroom (2 minutes):**
1. On the PC that feeds the projector, press **Windows key + P**.
2. If **"Extend"** is an option and picking it puts a second desktop on the
   projector → the answer to Q1 is **Yes** and the whole kit as designed goes ahead.
3. If it only mirrors (projector shows the same screen) → the kit still works,
   but the class would see your teacher window unless blackout is used — tell me
   and I'll design for that.
4. A USB clicker just acts as a keyboard (PageUp/PageDown) — any model that
   works in PowerPoint will work here. It plugs into that PC, not your phone.

**One more decision only you can make (needed before Phase 6, not today):** the
cold-call picker must read a class list from somewhere. The estate's own written
safeguarding rule says tools must **never read, parse or rewrite the existing
roster keys** (quality/SAFEGUARDING_CONTENT_GATE.md:83–88), and the master
prompt says creating a **new** roster key is a stop-and-ask. Those two rules
together mean there is no default — §5 below lays out the three options and what
each costs. Nothing is built until you pick one.

**Pre-existing issue you should know about (not caused by, and not fixed in,
this PR):** a handful of already-shipped lesson files on the public site contain
real pupil first names hard-coded in the page or in a filename. §8 lists where,
without repeating any name. Fixing them is safeguarding work that is never
self-merged here, so it needs its own pass with your sign-off.

---

## 1 · The estate as found

### 1.1 The live `/hud.js` — it is not in this repo, and it is already called "Live-Teach"

- `hud.js` lives at the root of the **sibling site repo**
  (`mattroper1977.github.io`), served estate-wide at the origin root as
  `/hud.js` (525 lines). This repo holds only the include tag (490 of 790 HTML
  files carry `<script defer src="/hud.js"></script>`), the coverage ledger
  `data/hud-coverage.json`, and the gate `tools/verify_hud_on_lessons_games.mjs`.
- Its own banner: `/* Made by Matt — Live-Teach HUD v1 — One floating dock for
  the whole estate: timer, name picker, noise meter, calm reset */` (site
  hud.js:1–3), and the dock's aria-label is "Live-Teach HUD" (hud.js:126).
  **"Live-Teach" already names an existing artefact.** The prohibition in the
  master prompt is therefore restated here by artefact, not by name:

  > **The HUD (do not touch):** the script `hud.js` in the site repo (served
  > `/hud.js`); everything it mounts (`#mbmhud-*` ids, `mbmhud-` class family,
  > `#mbmhud-style`); its sentinel `window.__mbmHud` (never set it — a page that
  > defines it silently disables the estate HUD); its storage keys
  > `mbm_hud_names` and `mbm_hud_used` (real pupil names live in the first —
  > the kit never reads or writes either); its read of `mbm_audience_view`; its
  > generated regions; and its ledgers/gates in both repos.

- Mode is decided from `location.pathname` alone (hud.js:40–49). Any
  `/Lessons/` page carrying the tag that is not a game gets the **full teacher
  dock** (timer, name picker, noise meter, calm reset) with no per-page opt-out.
  The only way for a `/Lessons/` page to not have the dock is to not carry the
  tag. Consequence for this kit: **liveteach pages do not carry the `/hud.js`
  tag** — which simultaneously satisfies "none of this code goes into the estate
  hud.js", avoids two name-pickers and two timers on one screen, and removes any
  arrow-key co-residency question.
- Measured keyboard reality (relevant to the clicker bridge): the HUD's only
  document-level key listener is Escape-only, capture phase (hud.js:401–411); it
  never preventDefaults, and holds arrows/PageUp/PageDown only for events
  originating inside its own dock (hud.js:431–450). The master prompt's fear —
  the clicker bridge's preventDefault breaking deck navigation if merged into
  the shared HUD — is confirmed as a real hazard *of merging*; kept out, there
  is no interaction at all.
- Trap for later phases: `IS_GAME` is the regex `/\/Games\//` against the whole
  pathname (hud.js:40), so **never create a folder named `Games` under
  `/liveteach/`**.

### 1.2 The reading-theme engine

- Canonical engine: `theme.js` in the site repo. This repo's
  `assets/mbm-theme.js` is **generated output** — one header line plus the
  canonical bytes verbatim, SHA-256-pinned
  (tools/verify_cross_estate_unification.py:63, checked daily) — never hand-edit
  it and never fork a copy into `/liveteach/`.
- Storage: single origin-wide key `mbm_reading_theme`, six values
  (`cream|pink|blue|light|dark|highlumen`), cream = attribute removed
  (assets/mbm-theme.js:9–27). The `highlumen` theme plus the hub's
  "High lumen — projector / IWB" mode (index.html:252,
  assets/mbm-platform.css:525) are **existing prior art for correction S5** —
  the projector view's high-lumen toggle should follow that vocabulary rather
  than invent one.
- Convention: standalone pages do **not** carry the theme engine — only the two
  hub pages do (repo-wide: 2 of 790 files), and FieldOps holds a ruled exemption
  for instrument-like pages because "retinting an instrument changes what it
  says" (CONVENTIONS_EXEMPTION_fieldops.md:37–45). A projector view showing
  data-bearing colour is exactly that case. **Decision: liveteach does not adopt
  `mbm_reading_theme`; it ships its own dark theme + high-lumen light toggle
  (S5), and this position is declared here CONVENTIONS_EXEMPTION-style so the
  next conformance sweep reads a decision, not a regression.**

### 1.3 Splash and exit conventions

- Splash: inlined canonical v2 splash (never `<script src>`), marker comment
  `mbm-splash-inline`, `MadeByMattSplash.start({title})`, ten gates S1–S10
  judged in both reduced-motion states (tools/verify_games_splash.mjs:6–16).
  The gate's own self-test depends byte-for-byte on the capture-phase key
  hardening — inline the canonical block verbatim, never "improve" it
  (verify_games_splash.mjs:246–266). The splash gate's default scope is
  `Games/` only, so liveteach's own harness must run the splash checks itself
  (the Physics_WaveOhm deck set this precedent).
- Exit: three sanctioned mechanisms. For a non-game teacher tool that carries no
  `/hud.js`, the compliant one is the **NAV-1 static back link**
  (`<a class="mbmhome" …>← Lessons</a>`, 44px target, focus ring, print:none —
  with the CSS actually shipped; markup-without-CSS was a recorded defect,
  RELEASE_LEDGER_2026-08-16.md:186). The stamped inline exit region is
  arcade-specific (back → `/games/`) and byte-pinned to a generator in the site
  repo — not appropriate here and never hand-copied.

### 1.4 The reduced-motion house rule (as written)

> "A pupil who cannot tolerate motion still gets the whole lesson: every part is
> visible, every label is on. They lose the animation, never the content."
> (grow-anim/grow-motion.css:304–306; named "the standing rule" in
> reports/REDUCED_MOTION_REGISTER.md:17–20.)

Practised requirements a liveteach page must meet:
- Both implementations: a CSS `@media (prefers-reduced-motion: reduce)` block
  **and** the JS `matchMedia` + class-toggle pattern, with a **live `change`
  subscription** (a boot-only read was a recorded defect,
  REDUCED_MOTION_REGISTER.md:180–184). The JS path also gates audio
  (quality/toolkits/ACCESSIBILITY_CONTRACT.md:20–23).
- Prefer a blanket scoped rule over an enumerated class list (lists rot — RM-1,
  REDUCED_MOTION_REGISTER.md:33–71).
- A pupil-facing stillness control independent of the OS setting (the Calm Mode
  pattern, Games/Glitch_Clash.html:500).
- Hide with `visibility`, never `opacity` alone (R-E22,
  ACCESSIBILITY_CONTRACT.md:26–28).
- Never `aria-live` on anything updating per second
  (ACCESSIBILITY_CONTRACT.md:15–17) — directly binding on the kit's timers.

### 1.5 The CI check suite

- Twelve workflow files. The floor: `fieldops-p2-and-sweep.yml` has **no
  `paths:` filter, deliberately** (its header cites two PRs that ran zero
  checks), so **every PR against `main` runs its five jobs** — sweep, fieldops,
  served, pr-census, inline-exit. A PR that only adds `/liveteach/` gets exactly
  those five today; it cannot be a zero-check PR **unless it is based on a
  branch other than `main`** (the trigger is `pull_request: branches: [main]`)
  — so every phase PR in this build targets `main`, as the master prompt already
  requires.
- The literal phrase "21-check suite" appears nowhere in the repo. The honest
  derivation to 21 distinct check contexts on `main`: 19 named jobs across the
  12 workflows + the `pages build and deployment` run + the `glv3/exact-tree`
  commit status (glv3-verify.yml:205–218). Two mechanisms keep the count
  honest: `tools/pr_check_census.mjs` gating against
  `tools/zero_check_baseline.json` on every PR, and
  `tools/watch_main_runs.mjs --verify-trigger-list`, which reds when a workflow
  exists that `watch-main.yml`'s hand-named list omits.
- **Binding consequence:** any new `liveteach` workflow must have its exact
  `name:` string appended to `watch-main.yml`'s `on.workflow_run.workflows`
  list **in the same PR**, or the watch goes red post-merge (daily cron at the
  latest).
- Sweeps that see new files on every PR: `verify_fixture_names.mjs` walks the
  whole tree and reds on person-shaped fixture tokens (two-TitleCase-word
  marker tokens, or the owner surname inside one) — all synthetic pupil data in
  liveteach fixtures must be non-person-shaped; `stale_evidence_sweep.mjs`
  judges `.json` under `evidence/`/`qa/` directories — liveteach will not ship
  such directories unless conforming to the claim forms.
- Browser-test pattern to copy for the liveteach harness:
  `tools/glitchclash/run.sh` — plain Node + Playwright Chromium suites against
  the shipped file, child exit status read before output greps, herestrings not
  pipes (the broken-pipe false-green fixed at `36da5d1`), `DIED` on a killed
  suite, non-zero exit on failure, `CHROMIUM_PATH` override; CI installs
  `npm install --no-save playwright && npx playwright install --with-deps
  chromium`, node 22. Gates must prove they can go red (INCONCLUSIVE /
  exit-code controls) and assert evidence, not proxies (CLAUDE.md).
- "Main went red on 2026-08-24": **not this repo's main.** The Lessons log has
  no commits on 23–24 Aug, and the top-shape ledger records all four mains green
  at the 25 Aug snapshot (_topshape/LEDGER_2026-08-25.md:128). The 24 Aug reds
  were **site-repo** backlog items (swatch gate red on main, resolved 24 Aug —
  _topshape/LEDGER_2026-08-25.md:395–403). The rule the master prompt draws —
  never push to `main` directly, each phase lands by PR with green checks —
  stands regardless, and is followed here.

---

## 2 · Roster storage census

Every localStorage family holding class lists, measured (files touching the
key, repo-wide, node_modules excluded):

| Key family | Files | Shape | Status |
|---|---|---|---|
| `mbm_cc_v1` | 175 | `[{n,g}]` / `[{n,b}]` / union `[{n,g,b}]` | The **living estate convention**. Tutor_Time code names it the "estate-shared roster" and one-way-migrates the legacy key into it (Tutor_Time/WB_W1_Democracy.html:419,427–431). 14-day TTL stamp + clear control in Tutor_Time. **Undocumented in REGISTER.md** — its §B stops before this key exists. |
| `ps_coldcall_roster` | 65 | mostly `["name",…]` strings | REGISTER R-B01 still declares it *the* estate-wide roster (REGISTER.md:227–231) — now stale. One writer stores objects into it (5 Intervention 10/L8a…:687,695), the exact corruption R-B02 records as breaking string consumers. |
| `coldCall_y10` | 4 | `[{name,grade}]` | R-B02: a deliberately **separate system**; "DO NOT MERGE", "grades stay local" (REGISTER.md:233–263; HANDOVER.md:491–492). |
| `coldCall_y10_geog` (+ 1 more cohort key) | 2+2 | `[{name,grade}]` | R-B03: deliberate cohort silos; merging silos is a data defect. |
| ~9 further micro-silos | 1–6 each | various | Per-lesson/per-unit keys (art, physics, chemistry). Several **hard-code real pupil first names as defaults in shipped files** — see §8. |
| `roster2` (sessionStorage) | 2 | `[{n,g}]` | Two Tutor_Time decks; the estate's only session-scoped, self-clearing roster — prior art for a privacy-lighter picker. |
| `mbm_hud_names` | 0 here | newline string | The HUD's own picker roster (site hud.js:50). **Off-limits** — part of the HUD artefact. |

Attendance: **no roster family carries absence flags.** The only attendance
data in the estate is one file's `present:{name:false}` map layered over the
legacy key (5_6 Local Choice/Rivers/L1e_Final_Briefing.html:504–528). The
picker's attendance UI (correction P4) has no estate precedent to reuse.

### The collision that makes this a Matt decision (master-prompt stop condition b)

Two binding texts point in opposite directions:

- The master prompt (P1): the picker **must reuse an existing roster source**;
  creating a new roster key family is a stop-and-ask.
- The estate's written safeguarding ruling: "**Do not touch the roster keys**
  … NEVER read, parse or rewrite the roster value itself — two different data
  models live behind these keys and both break if you touch the shape"
  (quality/SAFEGUARDING_CONTENT_GATE.md:83–88), reinforced by "No forced
  deletion. No schema migration. No key renames anywhere."
  (quality/toolkits/DATA_GOVERNANCE.md:22–25). And no safeguarding change in
  this estate is self-merged (SAFEGUARDING_CONTENT_GATE.md:104–107).

So **there is no compliant default**. The three options, honestly costed:

1. **Read-only reuse of `mbm_cc_v1`** (the living convention; 175 files;
   already carries attainment tiers). Requires Matt to rule that a *tolerant,
   read-only* parse (never writing, never migrating, treating `{n,g}`/`{n,b}`/
   strings defensively) is outside the mischief the ruling targets. Adds no new
   name storage. REGISTER.md would gain the missing `mbm_cc_v1` entry in the
   same pass.
2. **A new `mbm_liveteach_roster` key** — cleanest isolation, follows the
   estate's own `mbm_<slug>_` namespace rule, but is a *fourth-plus* roster
   system, which the master prompt forbids without sign-off, and Matt would
   type class lists again.
3. **Session-scoped roster** (the `roster2` pattern): names live only for the
   browser session, explicit clear control, nothing persists. Lightest privacy
   footprint; cost is re-entering names each lesson (or each PC login).

**Recommendation if Matt asks for one:** option 1, read-only, with option 3's
clear-visibility. But it ships only on his explicit ruling — recorded here as
an open decision, needed before Phase 6, not today.

---

## 3 · Placement decision

**`/liveteach/` folder at the root of this repo**, serving at
`https://madebymatt.uk/Lessons/liveteach/` (this repo is a project mount under
the site origin — `LESSONS_ORIGIN`, tools/verify_served.mjs:79; there is no
second origin, REGISTER R-D01). Note the URL the master prompt writes as
`/liveteach/` is, in this repo, `/Lessons/liveteach/` — a domain-root
`/liveteach/` would belong to the site repo, which Q3 ruled out.

Justification and constraints, from measurement:

- The name is unclaimed (zero hits repo-wide) and lowercase root folders are
  the estate's app-folder pattern (`build-engine`, `biology`, `primary`).
- **Never** a leading underscore (Jekyll excludes it — no `.nojekyll` exists,
  and the estate uses `_` to mean "records, not routes"), and no file may open
  with a `---` front-matter fence (Jekyll would Liquid-process it — every file
  starts `<!doctype html>`).
- `liveteach/index.html` exists from day one: a folder without one is a 404 by
  construction on Pages — the recorded FieldOps failure
  (CONVENTIONS_EXEMPTION_fieldops.md:92–104).
- **View layout: separate files per view** — `index.html` (launcher),
  `projector.html`, `teacher.html` — not one file with a role parameter.
  Reasons: (a) two windows of one URL invite opening the wrong role, and
  distinct filenames are phone-explainable ("open projector.html on the
  projector"); (b) this estate's gates and censuses judge *files* — separate
  files give each view its own contract; (c) a bare URL with no param must do
  something sensible, which is a third implicit view anyway. The teacher view's
  file is named `teacher.html`, not "hud", because "HUD" already names the
  estate artefact in §1.1.
- **Each view is a single self-contained HTML file** (estate offline-first
  promise; zero egress; no CDN/webfont/external image). The bus contract and
  keyboard registry that all views share will be authored once under
  `tools/liveteach/` and **stamped into the views as a generated, pinned
  region** — the estate's own inline-exit precedent for "shared code inside
  self-contained files" — with a harness check that the stamped copies match.
  (Fallback if that proves heavier than it earns in Phase 1: a shared JS file
  by relative path, the ratified visual-learning precedent. The decision
  between them is implementation, not architecture; the pinned-region intent is
  recorded here.)
- Liveteach pages carry **no `/hud.js` tag** (§1.1), a NAV-1 back link with its
  CSS shipped (§1.3), the canonical inlined splash (§1.3), and their own
  dark/high-lumen theme with a declared exemption from `mbm_reading_theme`
  (§1.2).
- Registration in `resources.json` (type `teacher`, entry point only per
  R-D04) is deferred to Phase 9, as its own step: appending an entry silently
  mints a hub chip (quality/DELIVERY_READINESS_CHECKLIST.md:41–46) and requires
  `tools/pin_manifests.py` re-pinning in the same commit
  (verify_cross_estate_unification.py:99–106). Until then the tool is reachable
  by URL and deliberately uncatalogued — the `hub-health.html` precedent.
- BroadcastChannel requires a real origin (two `file://` windows get opaque
  origins in Chromium and do not connect), so the kit is used from the live URL
  on the classroom PC; single-file self-containment is still kept for
  robustness and estate conformance.
- New storage keys (settings, RAG counts, picker history — never pupil names
  without §2's ruling) all live under the `mbm_liveteach_` prefix and get
  REGISTER.md §B entries in the phase that introduces them.

---

## 4 · CI plan for Phases 1–8 (so no phase ships ungated)

- One new workflow, `liveteach-verify` (paths: `liveteach/**`,
  `tools/liveteach/**`, itself), running the liveteach harness on the
  glitchclash pattern (§1.5), node 22, Playwright Chromium, with an exit-code
  control proving the gate can go red. Its exact `name:` is added to
  `watch-main.yml`'s trigger list **in the same PR** (the
  `--verify-trigger-list` control reds otherwise).
- Every phase PR targets `main` (a PR on any other base runs zero checks and
  becomes an undeclared zero-check census finding).
- Every Corrections Registry fix lands with a positive and a negative control
  in the harness, per the master prompt; suites assert evidence, not proxies.
- Synthetic roster data in tests uses non-person-shaped tokens (§1.5's
  fixture-name predicate).
- The QR decode gate (Q1 in the corrections registry) needs an independent
  decoder in-repo; `jsQR` would be vendored locally (the `Games/vendor/`
  precedent — no CDN), used by the harness only, never shipped to a page.

---

## 5 · Master-prompt premises, corrected by measurement

Recorded so later phases build on measured fact, not the prompt's recollection:

| Prompt says | Measured |
|---|---|
| "the live `/hud.js`" (in this estate) | Lives in the **site repo**; this repo holds tag + ledger + gate (§1.1). It is itself named "Live-Teach HUD v1" — the kit's docs disambiguate by artefact. |
| "`/theme.js`" | Canonical in the site repo; `assets/mbm-theme.js` here is a generated, hash-pinned copy (§1.2). |
| "`ps_coldcall_roster` ×~66" | ×65 — and the living convention is now `mbm_cc_v1` ×175, which REGISTER.md does not yet document (§2). |
| "main went red on 2026-08-24 from exactly that" | Not this repo's main (§1.5). The rule drawn from it stands and is followed. |
| "the 21-check suite" | Phrase absent from the repo; honest count = 19 named jobs + Pages build + one commit status (§1.5). |
| Placement "`/liveteach/`" | In this repo that URL is `/Lessons/liveteach/` (§3). |

---

## 6 · Stop report (master-prompt stop conditions a and b)

- **(a) Q1 is unknown.** Phases 1–5 (bus, stage engine, clicker, telestrator,
  QR-of-live-state) are designed around same-device dual-window sync and are
  **not started**. What survives a "No": Phase 6 (cold-call picker), Phase 7
  (classroom extras), Phase 8 (worksheet engine) re-scoped as single-window
  tools; additionally, a single-window projector view driven directly by the
  clicker on the PC it runs on (no second window, no bus) would preserve much
  of Phases 2–3's classroom value — offered as a re-scope option, not assumed.
- **(b) The roster ruling** (§2) is Matt's, because reuse sits inside the
  letter of a written safeguarding rule and novelty is forbidden by the master
  prompt. Needed before Phase 6 only.
- Nothing here required touching `/hud.js`, `/theme.js`, or any lesson deck,
  and nothing did (stop condition e not triggered). Main's checks are green
  (condition c not triggered).

**Next action is Matt's:** check the classroom PC (plain steps in the summary
above), then answer Q1. Yes → Phase 1 begins on the architecture as specced.
No → say which re-scope (picker / extras / worksheet / single-window projector)
is wanted first.

---

## 7 · Decisions taken this phase (binding on later phases)

1. Liveteach pages carry no `/hud.js` tag; the HUD prohibition is enforced by
   the artefact definition in §1.1.
2. Folder `/liveteach/` in this repo; three self-contained views
   (`index.html`, `projector.html`, `teacher.html`); shared code stamped as a
   pinned generated region (fallback: shared JS by relative path) — §3.
3. No `mbm_reading_theme` on liveteach pages — own dark + high-lumen theme,
   declared exemption per the FieldOps mechanism — §1.2.
4. NAV-1 back link + canonical inlined splash, self-gated in the liveteach
   harness — §1.3.
5. All liveteach storage under `mbm_liveteach_*`, REGISTER-registered per
   phase; pupil names nowhere until §2 is ruled.
6. New workflow registered in `watch-main.yml`'s list in the same PR; all phase
   PRs target `main` — §4.
7. Cold-call stays HUD-only with an explicit per-lesson "project name" button
   (Q2); names never enter bus messages, URLs, QR codes, exports or logs
   otherwise (master-prompt non-negotiable, unchanged).

---

## 8 · Pre-existing findings outside this task's scope (reported, not touched)

Found during the census; **not** fixed in this PR (safeguarding changes are
never self-merged — quality/SAFEGUARDING_CONTENT_GATE.md:104–107). No names are
reproduced here.

- Real pupil first names are hard-coded in shipped, publicly served files:
  preset buttons in `build-engine/roster-setup.html:10–11` (its
  `Build/Resources/` twin is already sanitised); a default roster written into
  storage by `ASDAN/HW_Social_Media_Wellbeing_Active.html:573,701`; a default
  roster in `5_6 Local Choice/Rivers/L1e_Final_Briefing.html:471`; and default
  class lists in ~12 `6 Art/` decks (e.g. `6 Art/Lesson3_Magritte_Study_v4.html:516–520`).
- Ten `ASDAN/Consent_*.html` filenames embed one pupil's first name.
- `node_modules/playwright` and `node_modules/playwright-core` are committed as
  dangling symlinks into a container path (commit `4b1029e`), and `.gitignore`
  does not cover `node_modules` — a cleanup candidate; liveteach phases will
  install with `--no-save` and add nothing under `node_modules/`.
- REGISTER.md's roster section (R-B01) is stale against the code: the
  175-file `mbm_cc_v1` system is undocumented there (§2).

---

## 9 · Provenance

Recon method: seven parallel read-only survey passes (HUD, theme, splash/exit,
roster census, CI, placement/house rules, SEMH/accessibility) plus an
independent completeness critique that re-measured contested claims; all
findings verified against HEAD `4a86bc3` (2026-08-25). Counts stated here were
measured by grep/find over the tree with `node_modules` excluded, not copied
from prose. The site repo was read via a shallow clone for `hud.js` facts only;
nothing in it was modified.
