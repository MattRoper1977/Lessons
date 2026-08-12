# Teach-Green Close — 2026-08-12

Closes the teach-green pass. Four things merged on 12 August (Teach Hub card
fix, High Lumen theme, HUD keyboard guard, hud.js announcer); two were gated on
Matt and are released here.

Bases re-derived from remote before any work. All three were unmoved from the
values in the previous report, so its measurements still stood:

| repo | rollback SHA |
|---|---|
| `mattroper1977.github.io` | `7d800ebc` |
| `Lessons` | `000f3c48` |
| `Matt-s-Apps-` | `d8db0480` |

---

## VERIFIED_BY_MATT · 2026-08-12

Matt verified on his own hardware, not in a harness:

- **the six Teach Hub cards on his real phone** — they filter and jump to the
  workspace, with no reload;
- **High Lumen on the classroom projector** — approved.

That closes morning-list items 1 and 2 of the previous report, and it is the
authority for releasing Stage B and the link grid. Neither decision is
re-litigated here; only the code state they rest on was re-verified.

**Re-assertion at HEAD before starting** — the four merged features, measured
rather than assumed: 6/6 Teach Hub cards bound in real Chromium at phone and
desktop with a clean console · High Lumen present as the sixth
`mbm_reading_theme` value on all 7 ported pages **and in all four engine
copies** · hud.js keyboard guard and announcer both present · all four merged
gates re-run green.

---

## Overlap — one hit, examined and cleared rather than waved through

The matrix ran every unmerged branch in all three repos against the exact files
this pass would touch. Two hits:

- **`claude/teach-green-links`** — this pass's own branch, which §2 exists to
  merge. Expected.
- **`claude/pr110-audience-discovery-close-8y477v`** — unmerged, and touching
  all four of `teach/index.html`, `education-hub/index.html`,
  `assets/mbm-search.css`, `tools/render_discovery_hubs.py`.

The second one had to be resolved before proceeding, because §0.3 says any
overlap stops the pass. It is **superseded, not live**:

- its `teach/index.html` is **byte-identical** to pre-pass main (`5f979e7a`), so
  its content was already in main before this pass began;
- its renderer differs from pre-pass main by 5 lines, and the difference is that
  the branch hardcodes `SENTINEL` while main imports it from
  `render_audience_homepages.py` — main is the later, single-definition version;
- it carries the same closeout sentinel as main, its tip is dated 2026-08-09,
  and **no open PR references it** (open PRs are #109, #106, #96, #91, #25).

Recorded rather than stopped on, with the evidence above. It is the source
branch for work that landed by another route.

---

## The exclusion list, resolved from the estate's own rulings

§1.2's exclusions are named in prose. They were resolved to exact paths from the
records rather than guessed, because two of them are easy to get wrong:

| exclusion | what it actually is | in the 277? |
|---|---|---|
| **frozen legacy science** | REGISTER.md:1545, R-SEMH02 (ruled 2026-08-04): the 2025-26 freeze on `biology/`, `chemistry/`, `2 Physics 10/`, `5 Intervention 10/`. Path-scoped, four trees. | **37 excluded** |
| **★assessed** | The estate keeps TWO selectors. `★ ASSESSED LESSON` is the *inclusion* selector and returns exactly the 2 byte-locked decks. `★ ASSESSED` is the *exclusion* selector. | **0** — see below |
| **Games / LundyLoop / report-only Baseline** | Hard-excluded by name. | **0** — none carries a slide deck |

**The star nearly went wrong, and the way it goes wrong is worth recording.** `★`
appears in **221** HTML files, where it is the **Stretch tier** marker in body
copy. Excluding on that would have removed 221 files including the plan's own
recommended first population. The marker that means *assessed* is `★` in the
`<title>` — exactly 2 files repo-wide — and the estate's own exclusion selector
`★ ASSESSED` returns 7. **Zero of either set is in the rollout**, so the
question is settled either way, but the rollout tool excludes on the title
marker, which is a strict superset of the estate selector for these decks.

**The two byte-locked assessed decks already load hud.js** and were covered when
the announcer merged. Their pinned hashes are unchanged:

```
a5545585ca28bbba01b55476abb73a9b0819bcc7  Grow/Slideshows/GROW_HUM_W7_Write_The_Account.html
eb14d6104b94503d0e7ec0a99565ef116a333a57  Launch/Slideshows/LAUNCH_HUM_W7_Source_Assessment.html
```

**Stale count, reported not fixed:** REGISTER.md:64 records the `★ ASSESSED`
exclusion selector as returning **6** files. It now returns **7** — a rebuild
copy at `GROW_Estate_v3/Humanities_Teesside/GROW_HUM_W7_Write_the_Account.html`
(note the lowercase "the") post-dates the register's verification. Not a scope
change; the inclusion selector still returns exactly 2.

---

## Census — no delta

Re-derived at HEAD and identical to `docs/ANNOUNCER_STAGE_B.md`:

```
decks with slides   502
load hud.js         225   (covered when the announcer merged)
without hud.js      277
```

`277 − 37 frozen legacy science − 2 assessed rebuild copies = 238 in scope.`

Two further deductions were made during the rollout, both from gates rather than
from reading:

- **−2 animation reference pages.** `build-anim/demo.html` and
  `grow-anim/demo.html` are "Animation Framework" reference pages carrying one
  `class="slide"` container each and no deck. The census matched them because
  its deck test accepted the bare string `.slide`, which also matches a CSS
  rule. The runtime gate found 0 slides, 0 announcements and no live region —
  hud.js requires `slides.length > 1` before it arms at all. Reverted; the deck
  test now requires more than one real slide element.
- **−78 GLV3 decks.** See the STOP below.

**Landed: 158 decks across 10 populations.**

---

## Stage B — the rollout

Per file, one line before the document's own `</body>`:

```html
<script defer src="/hud.js"></script>
```

**That form was derived, not chosen:** 220 of the 225 already-covered decks use
it. The other 5 wrap it in a loader with a relative fallback for `file://`,
which is out of scope — hud.js loading from the domain root and 404ing under
`file://` is an established property of this estate (§1.4), not a defect to fix
in a pass about announcements. No copy of hud.js is vendored.

**The anchor needed a rule.** Five decks carry a *second* `</body>` inside a
JavaScript string — the print-window template they hand to `document.write`.
Inserting at the first match would have corrupted that template. The tool
anchors on the **last** `</body>` and refuses the file unless nothing but
`</html>` and whitespace follows it, so the anchor is proven rather than
assumed. It skipped those five until the rule existed, which is the behaviour
§1.3 asks for.

### Proof of inertness — exact diff, not region sampling

`tools/stage_b_announcer.py --prove` asserts that each changed file equals its
base with that one string inserted **and nothing else**. That is stronger than
comparing regions one at a time, because it leaves nothing unchecked. The named
regions are then asserted on top so the proof is readable:

```
238/238 differ from origin/main by exactly the include
closure · witness · tiers · print · Oak · loop-mark — identical, every file
sentinels  ll-g:loop-mark 50/50 · written-closure 123/123, set-identical
frozen legacy science · assessed decks · Games · LundyLoop — 0 changed
```

Sentinel derivation is copied from `_lsg1/tools/lgates.py` so the two cannot
disagree. This is a hold pass: no movement is declared, so unchanged is the only
green.

### Print — both dialects

- `_nav1/tools/nprint.js` **reused, not rebuilt**: renders under `file://`,
  where hud.js never mounts.
- The new runtime gate renders **over HTTP with the HUD actually mounted** —
  the dialect nprint.js cannot reach, and the one that matters in a classroom.

---

## The STOP — two estates backed out, on a gate that was right

`.github/workflows/glv3-verify.yml` governs `GROW_Estate_v3` and
`LAUNCH_Estate_v3`. Its broken-link check parses every `href` and `src` and
resolves any `/`-absolute path **against the repository root**. `/hud.js` is not
in this repository — it is served from the domain root by the site repo. So the
include reads to that gate as broken links. Reproduced locally against the
gate's exact resolution model:

```
before revert   html 94   broken links 78   all of them '/hud.js'  (33 GROW + 45 LAUNCH)
after revert    html 94   broken links  0
```

That gate was green before this pass and went red because of it, so §4.1's STOP
applies and was taken. Both estates are restored to `000f3c48` byte-for-byte and
are excluded in the scope rule so no later run re-adds them silently.

**The workflow was not touched.** Editing the guardrail that is blocking you, in
the pass where it blocks you, is how a gate stops meaning anything — and this
one is right about what it can see. Within this repository the path genuinely
does not exist; it only resolves once the site repo is serving the root, which
is exactly the cross-repo mount §1.4 establishes and this gate has no model of.

**Three ways out, none of them mine to choose:**

1. teach `glv3-verify.yml` that `/hud.js` is a domain-root mount rather than a
   repo path — one allowance, made in a pass that is not also adding the include;
2. give those two estates the loader form the other 5 already-covered decks use,
   which tries `/hud.js` and falls back to a relative path — but that is the
   `file://` fix §1.4 explicitly rules out, so it would need Matt to reopen that
   ruling;
3. leave them uncovered, and accept 78 decks without the announcer.

**Stage B therefore stands at 158 decks across 10 populations.** The 78 GLV3
decks are the only part of the go that did not land.

---

## Reported, not fixed

**Three gates red since `5f979e7a`, none caused by either pass**, re-measured at
the merged HEAD and unchanged:

| gate | finding | owner |
|---|---|---|
| `render_audience_homepages.py --check` | `for/pupils/index.html` stale | unknown |
| `build_mbm_search_index.py --check` | 4 game entries differ (trail-runner, trekkers, intervention pupil/teacher apps) | unknown |
| `verify_design_inheritance.py` | 4 promoted images absent from `visual-provenance.json` | unknown |

**§3.1(b) was not done, and should not be.** The close order authorised removing
a "duplicate `data-mbm-filter="origin"` control" on the Education Hub. There is
no duplicate. The two controls are a deliberate two-button toggle group inside
`role="group" aria-label="Filter by origin"`, and `assets/mbm-search.js:379`
implements group semantics for exactly this shape. Measured:

```
baseline                 493 results
origin=internal          453 results   aria: internal=true  external=false
origin=external           40 results   aria: internal=false external=true
                         453 + 40 = 493 — the two partition the set
all 6 select filters      move the count
```

Removing either button would delete a working filter. **The observation came
from my own previous report and was wrong; it is corrected here.**

---

## My own regression, found by a gate and fixed

`Made by Matt cross-estate unification` requires the Lessons and Apps copies of
`assets/mbm-theme.js` to be **byte-identical** to the site's `theme.js`. The High
Lumen pass broke that, and the reason is worth recording precisely: I edited the
three copies separately and wrote **slightly different comment wording** into
each. The executable code was identical. Only the prose differed — and the gate
is right not to care which bytes differ.

```
before High Lumen   site af946d77c39a   lessons af946d77c39a   identical
after               site 2e463f7d2583   lessons ed08eb375da5   drifted
now                 all three 6934f92739429496…                identical
```

`CANONICAL_HASHES` moved to the new digest, which is that manifest's job when a
shared asset legitimately changes.

**Two pre-existing drifts were left alone**, measured at the pre-pass SHAs
(Lessons `e0ca832` vs site `5f979e7a`):

```
assets/mbm-platform.css   site 0a172aa3e218   lessons e3eb9b83d3c7
assets/mbm-platform.js    site 0841046b6e2d   lessons 0958a73a78a9
```

Both were already unequal to canonical before either pass, so this gate was
failing before I arrived. I briefly synced them and then reverted that: they are
shared runtime files in two repositories, the drift is not mine, and overwriting
a hub's platform shell to clear a red line is not a fix. Reported for a pass that
owns them.

---

## Recorded, not built — theme-engine unification

The reading-theme engine exists in **four** edit sites: `theme.js` in the site
repo, `assets/mbm-theme.js` in Lessons, `assets/mbm-theme.js` in Matt's Apps,
and a self-contained inline implementation on the homepage. The High Lumen pass
proved they drift: updating one left the Lessons and Creator hubs showing five
swatches while the rest of the estate showed six, and the divergence was
invisible until a rendered contrast audit measured a cream background where the
theme should have painted white. A single shared engine with the three copies
reduced to imports would make that class of drift impossible. It is a bigger
change than any of these passes and touches every themed page, so it is
**recorded as a proposed future pass and no code was written for it here.**

The case strengthened during this close: the four copies drifted **twice in one
day**. The first time cost the Lessons and Creator hubs their sixth swatch until
a rendered contrast audit caught it. The second time it was comment text alone,
caught by the cross-estate gate. Neither was a coding error; both were the
inevitable consequence of four edit sites for one file.


---

# Pass TG-78 — the GLV3 gate learns the mount, and the 78 land · 2026-08-12

Closes the one part of the Teach-Green go that did not land. Bases re-derived
and all three unmoved at their floors: Lessons `7123d351`, site `c65aeb5c`,
Apps `1f0a803d`.

## Preconditions

- **Overlap:** 105 unmerged Lessons branches scanned against `glv3-verify.yml`,
  the two GLV3 estates and `_teachgreen/`. **Zero overlaps.** The three
  `audit/glv3-*` branches and the pre-programme PRs were left alone.
- **The 78 derived, not guessed:** by the recorded scope rule with the GLV3
  exclusion lifted — GROW 33 + LAUNCH 45 = **78**, matching this ledger exactly.
- **Failure reproduced first:** grafting `/hud.js` into one of the 78 and running
  the gate's own model gave **1 broken link, `/hud.js`** — the `a108c4e3` class.

## The mount map

`_glv3/tools/mount_map.py`, with its own `--self-test`:

```
/Lessons/**   ->  this repository's tree      (unchanged)
/**           ->  the site repo at a PINNED SHA, over raw.githubusercontent
```

Order: this repo's mount → the historic repo-relative reading (kept; much of the
estate is written that way and those links are real) → the site mount → broken.
A 404 from the site mount is BROKEN. Anything else non-200 — timeout, DNS, 5xx,
proxy refusal — is **UNVERIFIED and RED**, never green. The SHA is pinned once
per run and printed every run.

### Both directions proven (§1.3)

```
clean tree              GREEN   mount map · site repo pinned at c65aeb5c…
graft /hud.js           GREEN   <- the a108c4e3 failure class, now resolved
graft /no-such-file.js  RED     'not in …github.io@c65aeb5c'
tree after both         0 estate files modified
```

The first run of those probes reported GREEN for both. The graft had silently
not happened — a bash function that did not forward its arguments — so both runs
measured a clean tree. Recorded, because a probe that passes for the wrong
reason is the exact failure mode this pass exists to remove.

## The workflow diff, in full (§1.4)

```diff
diff --git a/.github/workflows/glv3-verify.yml b/.github/workflows/glv3-verify.yml
index c55d9f7a..e9977b63 100644
--- a/.github/workflows/glv3-verify.yml
+++ b/.github/workflows/glv3-verify.yml
@@ -83,18 +83,29 @@ jobs:
               def handle_starttag(self,tag,attrs):
                   for k,v in attrs:
                       if k.lower() in {'href','src'} and v: self.links.append(v)
-          broken=[]
+          # Link resolution knows about the deployed mounts: this repository is
+          # served at /Lessons/, the site repo at the domain root. A "/"-absolute
+          # href is therefore not always repo-relative. See _glv3/tools/mount_map.py.
+          sys.path.insert(0, str(root/'_glv3'/'tools'))
+          from mount_map import SiteMount, pin_site_sha, resolve, BROKEN, UNVERIFIED
+          site_sha = pin_site_sha()
+          print('mount map · site repo pinned at ' + site_sha)
+          site = SiteMount(site_sha)
+          broken=[]; unverified=[]
           for p in html:
               q=P(); q.feed(p.read_text(encoding='utf-8',errors='replace'))
               for raw in q.links:
                   u=urlsplit(raw.strip())
                   if u.scheme or u.netloc or raw.startswith(('mailto:','tel:','data:','javascript:','#')): continue
-                  path=unquote(u.path)
-                  if not path: continue
-                  target=(root/path.lstrip('/')) if path.startswith('/') else (p.parent/path)
-                  if target.is_dir(): target=target/'index.html'
-                  if not target.exists(): broken.append({'from':p.relative_to(root).as_posix(),'link':raw,'target':str(target.relative_to(root) if target.is_relative_to(root) else target)})
+                  status, detail = resolve(raw, p, root, site)
+                  if status == BROKEN:
+                      broken.append({'from':p.relative_to(root).as_posix(),'link':raw,'detail':detail})
+                  elif status == UNVERIFIED:
+                      unverified.append({'from':p.relative_to(root).as_posix(),'link':raw,'detail':detail})
           assert not broken, broken[:20]
+          # Fail-safe: a mount we could not reach is red on its own message, never
+          # a silent pass. A gate that goes quiet on a network hiccup looks green.
+          assert not unverified, ['UNVERIFIED — site mount unreachable, not a pass'] + unverified[:20]
           required=['_glv3/GATES_STATIC.json','_glv3/GATES_BROWSER.json','_glv3/GATES_CHIPS.json','_glv3/INPUT_INTEGRITY.json','_glv3/COUNT_RECONCILIATION.json','_glv3/AUTONOMOUS_SENTINEL.json','_glv3/POSITIVE_CONTROLS.json']
           for rel in required: assert (root/rel).is_file() and (root/rel).stat().st_size>0, rel
           contacts=list((root/'_glv3/contact_sheet').rglob('*.png'))
@@ -140,13 +151,34 @@ jobs:
         shell: bash
         run: |
           set -euo pipefail
+          # The local server roots this repository at /, but the deployed domain
+          # roots the SITE repo there and mounts this one at /Lessons/. Without
+          # the mount, /hud.js 404s and the boot gate fails on the console error
+          # — the same disagreement the static link check had, one layer down.
+          # Materialise the mount from the pinned site SHA. This is a test
+          # fixture: it is untracked, it is removed immediately afterwards, and
+          # nothing is vendored into the repository.
+          SITE_SHA="$(git ls-remote https://github.com/MattRoper1977/mattroper1977.github.io main | cut -f1)"
+          test -n "$SITE_SHA"
+          echo "runtime mount · site repo pinned at ${SITE_SHA}"
+          curl --fail --silent --show-error --retry 3 --max-time 60 \
+            -o "$GITHUB_WORKSPACE/hud.js" \
+            "https://raw.githubusercontent.com/MattRoper1977/mattroper1977.github.io/${SITE_SHA}/hud.js"
+          trap 'rm -f "$GITHUB_WORKSPACE/hud.js"' EXIT
           python -m http.server 4173 --bind 127.0.0.1 --directory "$GITHUB_WORKSPACE" >/tmp/glv3-http.log 2>&1 & server=$!
-          trap 'kill "$server" 2>/dev/null || true; cat /tmp/glv3-http.log || true' EXIT
+          trap 'kill "$server" 2>/dev/null || true; rm -f "$GITHUB_WORKSPACE/hud.js"; cat /tmp/glv3-http.log || true' EXIT
           for _ in $(seq 1 40); do curl -fsS http://127.0.0.1:4173/ >/dev/null && break; sleep 0.25; done
           timeout 50m node _glv3/tools/browser_verify.mjs http://127.0.0.1:4173
           timeout 20m node _glv3/tools/chip_gate.mjs http://127.0.0.1:4173
           kill "$server" 2>/dev/null || true; wait "$server" 2>/dev/null || true; trap - EXIT
+          rm -f "$GITHUB_WORKSPACE/hud.js"
           rm -rf node_modules
+          # Narrowly the fixture, and nothing else. An earlier version asserted a
+          # clean porcelain over the WHOLE tree and turned a passing job red: the
+          # browser and chip gates legitimately regenerate _glv3/contact_sheet,
+          # and node_modules is tracked, so `rm -rf node_modules` shows as
+          # deletions. The mount had worked; the check was wrong.
+          test ! -e "$GITHUB_WORKSPACE/hud.js" || { echo 'runtime mount left residue: hud.js'; exit 1; }
           git diff --check
 
       - name: Upload exact-SHA evidence
```

## Three reds before green, all mine, all the same shape

| SHA | result | cause |
|---|---|---|
| `a108c4e3` | RED | the original stop: 78 broken links, all `/hud.js` |
| `4b1029e2` | RED | static check passed; **`browser_verify.mjs` boot gate** 404ed on `/hud.js` — its local server roots this repo at `/` |
| `9f55c850` | RED | mount worked; **my own residue check** asserted a clean porcelain over the whole tree and fired on the gates' regenerated contact sheets and on `rm -rf node_modules` |
| `99167470` | **GREEN** | with all 78 includes in place |

The pattern in all three is one thing: I proved the piece I had just written and
not the job around it. First the static block alone. Then the mount, without its
own cleanup assertion. A narrow proof reads exactly like a broad one until CI
disagrees.

## Attestation for the 78 (§2)

```
exact diff, base 000f3c48   236 files differ by exactly the include, nothing else
regions per file            closure · witness · tiers · print · Oak · loop-mark identical
sentinels                   ll-g:loop-mark 50/50 · written-closure 123/123, set-identical
assessed pair               a5545585ca28bbba… / eb14d6104b94503d…  unchanged
frozen legacy science       biology, chemistry, 2 Physics 10, 5 Intervention 10 — 0 changed
Games / LundyLoop / Baseline                                       — 0 changed
assets/mbm-theme.js         6934f92739429496…                      unchanged
hud.js                      not modified
deck test                   78/78 carry >1 real slide; the announcer arms on all
print                       78/78 rendered print text identical to base
runtime                     14 decks x 2 viewports, both populations, all green
```

The runtime sampler was corrected to reach 14: it hardcoded four indices and
ignored `MAX_PER_POP`, so a request for 7 per population returned 4.

## Production (§3.2)

The environment cannot reach `madebymatt.uk` (HTTP 000 at the proxy), so the
dispatch-only `glv3-production-byte-check.yml` was used unchanged — it already
samples one GROW and one LAUNCH file, **both of which are in the 78**:

```
checkout SHA: 9f55c85026c0736bb2111cca24d7ffc4bf45ebd5
PASS  identical  d442d3343e38cbc3  50504 B  GROW_Estate_v3/…/GROW_HUM_W1_Time_Detectives.html
PASS  identical  26be4377daf50216  47675 B  LAUNCH_Estate_v3/…/LAUNCH_HUM_W1_Source_Investigation.html
RESULT: ALL IDENTICAL — production serves this checkout byte-exact for the sample.
```

Production therefore serves the include. `pages build and deployment` success at
`99167470`.

## Final

| | |
|---|---|
| Lessons main | `99167470` |
| pinned site SHA (gate output) | `c65aeb5c9a8fd186d4139e5de306a32b29ee17b2` |
| Stage B total | **236 decks** — 158 + the 78 |
| decks with slides still uncovered | 0 |
