# FieldOps FIX-1 — the labs' directory URL 404s

Pass: `fieldops-fix1-2026-08-19` · BASE / ROLLBACK = `3ca150a` (`origin/main` at start).
Branch: `claude/new-session-jbjr5k`, cut fresh from `origin/main` (the previous PR for it
is merged; a merged PR cannot track new work).

---

## §0 — Diagnosis, before any fix

| # | Check | Finding |
|---|---|---|
| 0.1 | `git ls-tree origin/main Science_Teesside/Build/v4_fieldops/` | **4 files, all labs. `index.html` present? NO.** Hypothesis confirmed. |
| 0.2 | Lab bytes vs `tools/fieldops/staging/` | **byte-identical, all four** — `b06553809fef`, `ef1a2588ae4b`, `f37709131892`, `e0dfcd53fc3d`. Not a content problem. |
| 0.3 | The 4 `resources.json` entries added at `3ca150a` | all four `"file":` values name a **lab HTML file**, e.g. `Science_Teesside/Build/v4_fieldops/01_Newport_Bridge_Lift_Permit_Lab.html`. **0 target the bare directory → no retarget.** |
| 0.4 | The Studio's T16-rewritten engine URLs | all four are `https://madebymatt.uk/Lessons/Science_Teesside/Build/v4_fieldops/0N_….html` — **file-targeting, 0 directory-targeting → nothing in Apps is touched.** |

**Cause.** GitHub Pages serves no directory listing. A directory with an `index.html`
is served as that file; a directory without one is a 404. `v4_fieldops/` had no
`index.html`, so the bare directory URL was a 404 **by construction** while every lab
beneath it served correctly. That is exactly the shape of the owner's report: the
Studio works, the labs work when reached by their own URL, the folder does not open.

**The symptom reproduced, and the fix measured against it.** `_fieldopsfix1/pages_sim.mjs`
serves a tree the way Pages does — a directory URL yields `<dir>/index.html` if it
exists, else 404, never a listing. Output in `_fieldopsfix1/pages_sim.out`:

```
BEFORE (origin/main 3ca150a)        AFTER (this branch)
404  /…/v4_fieldops/                200  /…/v4_fieldops/   title="BUILD FieldOps — Science Instruments"
200  /…/01_Newport…_Lab.html        200  /…/01_Newport…_Lab.html
200  /…/v3_40min/                   200  /…/v3_40min/            # sibling reference, green both sides
404  /…/Build/                      404  /…/Build/               # CONTROL: still 404 both sides
```

Three limbs, per R0.1: **red on the target** before the change; **green after**; and a
**control that stays red** — `Science_Teesside/Build/` genuinely has no `index.html`
and returns 404 in both runs, so the harness is not answering 200 to everything. The
sibling `v3_40min/` is the fourth line and is green on both sides, which separates
"directory with an index" from "directory without one" rather than assuming it.

---

## §1 — The fix

**One new file: `Science_Teesside/Build/v4_fieldops/index.html`** (9 lines, 3,272 bytes).

Shape **derived, not invented**: it is `Science_Teesside/Build/v3_40min/index.html` —
the sibling app-index one directory across — reduced to what this hub needs. Carried
over verbatim: the `<style>` block's body/main/header/`.call`/table rules, the whole
NAV-1 chrome block, and the back-link anchor, which is byte-identical to the sibling's:

```html
<a class="mbmhome" href="../../../index.html" aria-label="Back to the Lessons catalogue">← Lessons</a>
```

Dropped from the sibling: its `.links` button row (this hub has nothing to link that is
not already in the table) and its `.v3banner`. Nothing added that the sibling does not
carry.

Contents: title **BUILD FieldOps — Science Instruments**; one `.call` line stating they
are **instruments, not lessons** — each runs beside the BUILD science lessons and
replaces no lesson in the route; a four-row table, one row per lab, linking by relative
filename. **No link to the Teacher Studio** — the ratified ruling stands, pupils do not
see the teacher tool; `grep -ci studio` on the file returns 0.

Measured on the file: `lang="en-GB"` · **0** external URLs (`https?://` or `//host`) ·
**0** `<script>` blocks · **0** `localStorage`/`sessionStorage`/`indexedDB`/`document.cookie` ·
**0** hud references · print rule `@media print{.mbmhome{display:none!important}}` present.

Per §0.3 and §0.4 the other two limbs of §1 do not apply: no `resources.json` entry
targets the bare directory (0 diff), and no Studio engine URL does (Apps untouched).

### The one thing §0 did not predict — and the gate that caught it

`tools/verify_fieldops_served.mjs` check **D1** asserts that `build.mjs`'s `LABS[]` and
the placed directory name the same files. Placing an authored hub the builder does not
emit made that **declared 4, placed 5 · placed but not declared: index.html — FAIL**.
Running the repo's own CI gates locally before merging is what surfaced it; nothing in
the diagnosis would have.

Repaired at source rather than by loosening the check. `PLACED_NON_LAB = ['index.html']`
is declared beside `PLACED` with its reason, and D1 now reads *required* = LABS +
PLACED_NON_LAB. So the hub is a **requirement, not a tolerance**: delete it and D1 reds
by name, which pins this defect against recurrence offline, on every push.

Because that widening closed a red, it has to be able to go red itself. Two new controls,
both mutating the **placed directory** (the record each limb is about), both restored in
a `finally`, with the directory hashed by name and bytes before and after and the equality
**asserted**, per R0.14:

- **C4** a file placed and declared nowhere → `placed but not declared: ZZ_placed_and_never_declared.html` — **FAIL, by name**
- **C5** the hub removed → `required but not placed: index.html` — **FAIL, by name**

Ten checks, `[OFFLINE] PASS — 0 failed` (`_fieldopsfix1/d1.out`). The file's header
docblock — which states what it asserts and what each exit code means — was updated in
the same commit.

**Deliberately not done:** `tools/verify_served.mjs` was *not* extended with a live
route for the directory URL. It could be (`/…/v4_fieldops/` compared against the hub's
committed blob, exactly as it already does for `${LESSONS_ORIGIN}/`), but D1 now pins
the recurrence offline and deterministically, and a live assertion I cannot exercise
from this runner — production answers this container 403 — would ship untested. Named
here rather than left as a silent omission.

---

## §2 — Gates

| Gate | Verdict |
|---|---|
| **Diff is one new file ± the gate it forced** | `A Science_Teesside/Build/v4_fieldops/index.html` (+9), `M tools/verify_fieldops_served.mjs` (+82/−6), plus this record and its two harnesses under `_fieldopsfix1/` |
| Manifests digest-pinned, never hand-edited | **`resources.json` 0 diff → `pin_manifests.py` not run, correctly.** Both repos' copies of `verify_cross_estate_unification.py` byte-identical, sha `d11970783c92…` |
| Lessons cross-estate static contract | **PASS** |
| Apps cross-estate static contract | **PASS** (run in the Apps checkout) |
| apps.json / counts untouched, proven | apps.json **0 diff**, index.html **0 diff**, Apps tree clean and HEAD == origin/main `234a405`; `leadCount` = `Thirty-nine`, apps.json items = **39** — match |
| Apps no-JS count gate (`verify_lundyloop_static.py`) | **PASS**, `"failures": []` |
| Chip gate (`resources.json` unchanged; run anyway) | **PASS — 28/28 limbs**, zero console errors |
| Link-crawl over `v4_fieldops/`, in a real browser | **PASS** — hub renders 5 links; all 4 labs resolve and report their own titles; root catalogue resolves; **CONTROL** an absent lab does not resolve |
| Pages-behaviour reproduction, before/after + control | **PASS** — table above |
| `node --check` on the new file's scripts | **0 script blocks — no subject** (measured, not assumed). `tools/verify_fieldops_served.mjs` parses |
| Boot clean, 390/768/1440 | **PASS** — `boot: all clean`, 0 console errors, 0 pageerrors, 0 request failures |
| Sentinels | **50 loop-mark / 123 closure, set-identical to base** |
| PROTECTED strings + food census | **IDENTICAL (736 rows)** |
| Nothing under `v3_40min/` touched | **0 files** |
| FieldOps sweep `--self-test` | **PASS — 0 failed** |
| Sweep `--require-roots=3` | **exit 0** · 3/3 roots assessed · 0 stale, 65 live · 0 files matching no form · Lessons 24 claims, Apps 41, site 0 |
| Planted-stale control (`qa_record_control.mjs`) | **PASS — 4/4 fire**, the planted subject is called STALE |
| **Is `index.html` in the sweep's universe?** | **No — outside, on both predicates.** Selector: `/(^\|\/)(evidence\|qa)\//.test(f) && /\.(out\|json\|txt\|md\|log)$/.test(f)`. Directory predicate `false`, extension predicate `false`. Control: `evidence/x.json` → `true`. It cannot re-red the sweep |
| Default run is a dry run (R0.14) | **PASS** — tree unchanged |
| `assert_unchanged.mjs` | **PASS — 0 unexpected changes**, 20 transforms, drop-all reproduces release |
| `verify_ledger_tally.mjs` + self-test | **PASS** both — stated count == counted count; 3 red paths fire |
| `verify_fixture_names.mjs` + self-test | **PASS** both — 0 person-shaped fixture strings |
| `verify_served.mjs --self-test` | **PASS** — 32 routes compose (site 26, lessons 5, apps 1); the new file is not among them |
| `verify_served.mjs --controls-only` | **INCONCLUSIVE (exit 2)** — the lessons origin answers **403** from this runner. Per R0.9 a runner fact is not a gate verdict. Controls (c)(d)(e) fired offline; the network legs run in CI |
| `pr_check_census.mjs` self-test / `--gate` | self-test **PASS**; `--gate` **INCONCLUSIVE (exit 2)** — GitHub API returns 401 here. Runs in CI |

**Which workflows this diff actually fires**, read from the trigger blocks rather than
assumed: `fieldops-p2-and-sweep.yml` carries **no `paths:` filter** on `push: [main]`,
so it runs — that is the one whose gates are tabled above. `watch-main.yml` then runs on
its completion. Every other workflow in `.github/workflows/` is path-filtered to
`Games/**`, `assets/**`, `index.html`, `GROW_Estate_v3/**` or similar and does **not**
match this diff. Apps has **no diff at all**, so no Apps workflow fires and no Apps
merge is needed.

---

## §3 — Out of scope, untouched

Lab bytes · the Studio card · any count · `resources.json` · `apps.json` ·
`Science_Teesside/Build/FieldOps/` (the phantom — still 0 files, still not created).

---

## Close-out, measured after the merge

| | |
|---|---|
| PR | **#140**, five checks green on `3868f8a` (the PR merge ref) |
| Merge | **`3b9273e`**, `--no-ff` via the GitHub API (the PR #136 precedent) |
| `main` before → after | `3ca150a` → `3b9273e` |
| `v4_fieldops/` at `main` | **5 files**: the four labs and `index.html` |
| Pages | **run #683 on `3b9273e` — success** (`pages-build-deployment`, 23:02:58Z) |
| FieldOps workflow on `main` | **run #72 on `3b9273e` — success**, all five jobs |

**The live serve proof, which only runs on a push.** Step "Every subject serves,
unredirected, byte-identical" on the merge commit:
**32 served byte-identical · 0 red · 0 inconclusive, of 32 derived**, content-type
32 as expected. The four labs answered 200 unredirected at their own shas
(`b06553809fef`, `ef1a2588ae4b`, `f37709131892`, `e0dfcd53fc3d`) and all five
production controls fired, including (a) a known-absent route answering 404 and
(b) a one-byte hash mutation going red against real bytes. That is the evidence
this container could not produce — from here the origin answers **403**, which
`verify_served.mjs` correctly calls INCONCLUSIVE rather than a failed control.

Note what those 32 routes do **not** include: the new hub. `verify_served.mjs`'s
`hubFrom()` reads the labs' NAV-1 link, which resolves to the **root catalogue**
`index.html` (50,807 B, `a9cf8fba2cd1`) — a different file that happens to share a
name. The directory-URL claim is pinned by D1 offline, not by a live route; see
"Deliberately not done" above.

### The pin

**Raw-pin RUN, and green** — but on the repository blob, not the custom domain:

```
GET https://raw.githubusercontent.com/MattRoper1977/Lessons/3b9273e/Science_Teesside/Build/v4_fieldops/index.html
  200 · 3272 B · sha256 d88eee1280bcbe75…  ==  the local file, byte-identical
```

**Live-origin pin NOT RUN — network blocked.** Both `https://madebymatt.uk/…` and
`https://mattroper1977.github.io/…` return HTTP 000 from this container: not a 403,
no connection at all. Stated as a runner fact, not a verdict about the estate — the
CI runner reached the same origin on the same commit and got 32/32 byte-identical.

### Phone-check URLs

- **The one that was broken** — `https://madebymatt.uk/Lessons/Science_Teesside/Build/v4_fieldops/`
  should now open the hub, titled *BUILD FieldOps — Science Instruments*, with four
  links and a **← Lessons** back button, and no Teacher Studio link.
- **One lab direct, as a control** — `https://madebymatt.uk/Lessons/Science_Teesside/Build/v4_fieldops/01_Newport_Bridge_Lift_Permit_Lab.html`
  (this one already worked; if the hub loads and this does not, the cause is not FIX-1).
