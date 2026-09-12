# LP1 §1 and PIN1 §1 — censuses

The order after RF2. Run 2026-09-12, release/control session, immediately after RF2 closed
`RF2_PARTIAL`. **§1 only.** Neither order's §2 (repair), §3 (proofs) nor beyond was attempted:
those need workflow edits across four repositories, one repo per PR under LP1 §4.1, and they are
not work to do without the ordering authority present.

**READ-ONLY throughout.** No commits, pushes, GitHub writes, PR comments or workflow dispatches
were made against any repository. Every "skips on a pull request" statement below is a **READ of a
YAML condition**, never a run **OBSERVED** — no workflow was executed and no Actions run inspected.

## Why these two, and why now

Both orders' PREREQ is "ML1 closed". RF2 §2 established it: Site #191, #192 and #194 are all
merged (`f41a9e32` 26 Aug, `72c31ba5` 27 Aug, `ed0a1ba3` 27 Aug, each verified against the API and
each merge commit confirmed to exist), and ML1 §2.3's live assertion holds — `shelf-mirror-guard.yml`
still reds on real drift (run 33713403941, 3 September). ML1 is **CLOSED-BY-DL**. The one triggered
ML1 §5 stop is a stale *document*, not a defect in the repair.

So LP1's PREREQ is met, and PIN1 "runs with or after LP1".

## The headline: both orders' opening figures are wrong

| Order | Carried figure | Measured | Verdict |
|---|---|---|---|
| **LP1 §1.1** | 13 live proofs (Site 6, Lessons 3, Apps 2, Games 1) | **18** (Site 9, Lessons 4, Apps 4, Games 1); **16** collapsed | **CONTRADICTED** on Site, Lessons and Apps; confirmed on Games |
| **PIN1 §1.1** | 89 pins | **444** distinct pinned paths (443 excluding the publisher-caller pin) | **CONTRADICTED** by a factor of ~5 |

Neither is merely stale. PIN1's 89 was **already wrong by ~4.9×** at PR #499's own head and base,
where the set measured 435 — that is, on the very PR the finding was drawn from. Its provenance is
**NOT LOCATED**: 89 matches no registry, no sum of registries, and no historical `CATALOGUE_PINS`
size. That was not inferred; it was searched for and not found.

LP1's progression is its own finding: **13 → 14 → 18**. Each deeper scan found more, because the
gate is not always the literal `github.event_name != 'pull_request'` string — three Site gates are
folded YAML that a single-line grep misses entirely, and two more are environment-variable ternaries
carrying no `if:` at all.

## Two premise corrections neither order anticipates

**PIN1 §0.1 says "the two gates that validate the 89-pin set". Measured, only ONE gate asserts any
pin digest** — `mbm-cross-estate-unification.yml:101`. `ux2-gates.yml` triggers on the checker but
asserts **zero of the 444 file pins**, because the only step that loads the gate module
(`ux2-gates.yml:81`) filters file-pin errors out before asserting
(`tools/ux2/prove_catalogue_gate.py:52-53` against the error string emitted at
`tools/verify_cross_estate_unification.py:843`).

This does not stop §1, but it **materially changes §2's scope**. §2.1 says "derive each gate's
trigger paths from the registry it asserts against" — and `ux2-gates.yml` has no registry to derive
from. Whether it becomes a pin gate or is left out of scope is a **decision, not a derivation**, and
it belongs to Matt before §2 starts.

**LP1's population is larger than its census clause implies.** Separately from the 18, there are
**21 further live proofs in workflows with no `pull_request` trigger at all.** Those produce *no PR
check* rather than a green one, so they are a different defect class from LP1 §0.1's "they skip and
the check reports green". They are reported separately below and are **not** folded into the 18 —
but LP1 §2 should rule on whether they are in scope, because an absent check and a green skip fail
the same way at the same moment.

---


# ORDER LP1 — §1 census

## LP1 §1 CENSUS — readback

**Order section read first:** Appendix B §B4, at `/tmp/claude-0/-home-user-Lessons/05c13970-a6c0-53bf-90f1-2f5c998f17c1/scratchpad/AppendixB.md:210-256`. Clauses quoted verbatim below where they bind the method.

**Refs measured at:** Site `/home/user/mattroper1977.github.io` main `1651b84c800f6cd3169a29f794b075042ee54024`; Lessons `/home/user/Lessons` main `aad04718c11a2396ecf323a662f55bf0e0c2441b`; Matt-s-Apps- main `4cb8a634dbeaa3d98d7699252fdfff4253c47eef` (API + raw.githubusercontent at that SHA, not cloned); Games main `809b6c9a65f175cd48182e793bee166ad4f6bd3f` (same). All line numbers below are from the blob at those SHAs.

---

### 0. RF2 carried facts, re-verified before being relied on

Per the evidence rule, I re-measured rather than carrying. Command: `sed -n '359,361p;370,372p;304,310p' .github/workflows/fieldops-p2-and-sweep.yml` in `/home/user/Lessons`.

```
      - name: Recover successful source-bound publication artifacts
        if: github.event_name != 'pull_request'
        env:
      - name: Every original subject serves the exact successful publication
        if: github.event_name != 'pull_request'
        run: |
```
```
          git clone --depth 1 -q https://github.com/MattRoper1977/mattroper1977.github.io.git "$RUNNER_TEMP/site" || echo "site clone failed"
          git clone --depth 1 -q https://github.com/MattRoper1977/Matt-s-Apps-.git "$RUNNER_TEMP/apps" || echo "apps clone failed"
          git clone --depth 1 -q https://github.com/MattRoper1977/Games.git "$RUNNER_TEMP/shelf" || echo "shelf clone failed"
```

| RF2 claim | Verdict | Evidence |
|---|---|---|
| Publication artifact recovery at 359, condition at 360 | **CONFIRMED verbatim** | `/home/user/Lessons/.github/workflows/fieldops-p2-and-sweep.yml:359-360` |
| Live comparison at 370, condition at 371 | **CONFIRMED verbatim** | same file `:370-371` |
| Condition is `github.event_name != 'pull_request'` | **CONFIRMED verbatim** both | `:360`, `:371` |
| Three non-fatal `\|\| echo` clone fallbacks at 306-308 | **CONFIRMED verbatim**, all three | `:306`, `:307`, `:308` |
| `prepare_served_publications.py:231` requests `per_page=30` with no pagination | **CONFIRMED** | `/home/user/Lessons/tools/prepare_served_publications.py:231` reads `/repos/{repo}/actions/workflows/{workflow}/runs?branch=main&per_page=30`. `grep -n "per_page\|page=\|Link\|paginate"` over the file returns only lines 231, 240, 250 — no `page=` cursor, no `Link` header handling anywhere. Pagination absent, confirmed by absence across the whole file. |
| RF2's first count: 14 live proofs (Site 7, Lessons 3, Apps 3, Games 1) | **SUPERSEDED** | See §1.1. RF2's Site 7 reconciles exactly with my collapsed Site 7. RF2 undercounts Lessons by 1 (`science-teaching-packs.yml:62`) and Apps by 1 (`verify-teesside-maker-lab-pro.yml` carries **two** independently gated live jobs, `:39` and `:63`, not one). |

---

### §1.1 — "Enumerate every live proof across all four repos: file, line, gating condition, what it asserts, and which event actually executes it."

#### Search method and file set (stated as §1.1 requires)

**Scan set / denominator: 97 workflow files — Site 58, Lessons 22, Apps 8, Games 9.** Verified there are **no `.yaml`-extension workflow files** in either clone (`ls … | grep -c ".yaml$"` → 0), so the `*.yml` glob is the complete set, 97/97.

Method, in four passes, because §1.1 warns the gate is not always the literal string:

1. **Trigger census.** For every one of the 97 files I extracted the whole `on:` block with `awk '/^on:/{flag=1} flag&&/^[a-z_]+:/&&!/^on:/{flag=0} flag'` and recorded whether `pull_request` appears. Result: **Site 47/58 and Lessons 17/22 trigger on `pull_request`**; Apps 5/8; Games 6/9.
2. **Gate census.** `grep -rn -E "if:.*(event_name|github\.ref ==|refs/heads/main|workflow_run|deployment)"` over all four sets, **plus** a separate multi-line pass (`grep -rn -A3 "if: >-"`) because three Site gates are folded YAML (`echovault-surfaces-verify.yml:59`, `relicforge-surfaces-verify.yml:59`, `maker-splash-canon-verify.yml:42`, `mbm-deployment-provenance.yml:41`) and a single-line grep misses them entirely.
3. **Non-`if:` gate census.** `grep -rnE "\$\{\{.*(event_name|inputs\.).*(&&|\|\|).*'https"` — this is how I found the two **environment-variable ternary gates** at `v4-games-deployment-verify.yml:163-164`, which carry no `if:` at all and which a gate-only scan would miss. Two hits, both in Site, none in Lessons/Apps/Games.
4. **Subject census.** `grep -rnE "madebymatt\.uk|madebymatt-play\.uk|mattroper1977\.github\.io"` over all four sets, then I read each hit in context to separate an **actual network fetch of a public origin** from a **string literal grepped inside a checked-out file** (e.g. `relicforge-verify.yml:61` `grep -c '<loc>https://madebymatt.uk/relicforge/</loc>' sitemap.xml` is a local file grep, **not** a live proof — it is excluded, as are the same shape at `echovault-verify.yml:61`, `neonbreach-verify.yml:139`, `neonsync-verify.yml:171`, `apexrally-verify.yml:81,85`, `biopunkhive-verify.yml:95`).

**Inherited gates were followed.** Games `play-domain-publication.yml`'s live job `verify-published` (`:145`) carries **no `if:` of its own**; it skips on a PR only through `needs: deploy` and `deploy`'s gate at `:132`. A grep for `if:` alone never finds it. I resolved every `needs:` chain in the four repos for this reason.

#### Population definition (stated, because it is what makes 13 wrong)

LP1 §0.1: *"Thirteen live proofs are gated `if: github.event_name != 'pull_request'` or equivalent. On a PR they skip and the check reports green."* The operative property is **the workflow runs on the PR and produces a check, and the proof inside it skips**. I therefore counted a proof into the 18 only when **both** hold. A live proof in a workflow with no `pull_request` trigger produces **no check on the PR at all** rather than a green one — a real defect of the same family, but a different one; those are reported separately below and are **not** folded into 18.

#### THE TABLE — one row per proof, all five columns

##### SITE — `mattroper1977.github.io` @ `1651b84c` — **9**

| # | File : line | Gating condition (verbatim) | What it asserts | Which event actually executes it |
|---|---|---|---|---|
| S1 | `.github/workflows/verify-games-audience-faces.yml:334` (job `live-proof`), gate at `:336`; asserting steps `:361`, `:376` | `if: github.event_name == 'push'` | `:361` `prepare_published_site.py --expected-sha` binds the exact successful Pages artifact, deployment attempt, upload window and ZIP digest and byte-compares the 13 deployed publication pages against the committed tree; `:376` drives Chromium against `MBM_BASE_URL=https://madebymatt.uk/ --publication education` | `push` to `main` only. Not `pull_request` (workflow does trigger on PR at `:4`), not `workflow_dispatch` |
| S2 | `.github/workflows/v4-games-deployment-verify.yml:163` (env ternary, **no `if:`**) | `V4_LIVE_ORIGIN: ${{ (github.event_name == 'push' \|\| inputs.live == true) && 'https://madebymatt-play.uk' \|\| '' }}` | Gates `verifyLivePublication()` at `tools/verify_v4_games_deployment.mjs:1017` (`if (LIVE_ORIGIN) await verifyLivePublication();`) — the live play-origin payload proof | `push` to `main`, or `workflow_dispatch` with `live=true`. On `pull_request` the variable resolves to the **empty string** and `:1019` silently falls back to `startServer()` — a local server. No skip is logged; the job is green either way |
| S3 | `.github/workflows/v4-games-deployment-verify.yml:164` (env ternary, **no `if:`**) | `V4_EDU_ORIGIN: ${{ (github.event_name == 'push' \|\| inputs.live == true) && 'https://madebymatt.uk' \|\| '' }}` | Gates `tools/verify_v4_games_deployment.mjs:350-352` — `if (EDU_ORIGIN) { … fetch(\`${EDU_ORIGIN}${game.route}\`) }`, the education-origin route leg | Same as S2; empty on `pull_request`, so the whole `if (EDU_ORIGIN)` block is dead |
| S4 | `.github/workflows/mbm-audience-discovery-closeout.yml:1264` (job `production`), gate at `:1268`; asserting step `:1274` | `if: github.event_name != 'pull_request'` | Every route derived from `data/audience-homepages.json` (≥7 audience + 6 named platform = 13) answers 200 at `https://madebymatt.uk`, and two removed paths 404. The job's own header at `:1265` names it *"reachability, not deployment"*, and `:1301-1313` states in-file that it proves nothing about a deployment | `push`, `workflow_dispatch` — anything but `pull_request` (workflow triggers on PR at `:4`) |
| S5 | `.github/workflows/maker-splash-canon-verify.yml:140`, gate at `:141` | `if: github.event_name == 'deployment_status'` | `tools/verify_deployment_provenance.py --publication education --expected-sha "${{ github.event.deployment.sha }}"` — that the deployment carrying this SHA is the one being served | `deployment_status` **only**. Not `push`, not `pull_request`, not `workflow_dispatch` — all four are triggers on this workflow (`:37-45`) |
| S6 | `.github/workflows/maker-splash-canon-verify.yml:148`, gate at `:149` | `if: github.event_name == 'deployment_status'` | For each of the 18 routes in `data/hud-coverage.json → makerSplash.applied`, fetches `https://www.madebymatt-play.uk{route}?mbm=$EXPECTED_SHA` with redirects refused (`:162-164`) and asserts `served_regions[0] == committed_regions[0]` (`:201`) plus status 200, `text/html`, exactly one region | `deployment_status` only |
| S7 | `.github/workflows/maker-splash-canon-verify.yml:209`, gate at `:210` | `if: github.event_name == 'deployment_status'` | `verify_maker_splash.mjs --mode=controls` (Town Life SS1–SS8 + cross-route controls) and `--mode=verify --scope=site`, both `--origin=https://www.madebymatt-play.uk` | `deployment_status` only |
| S8 | `.github/workflows/hc3-stub-handoff.yml:102` (job `live-handoff`), gate at `:103`; asserting step `:144-145` | `if: github.event_name != 'pull_request'` | `domain-split/check_stub_handoff_live.cjs` drives a real browser across the real education and play origins: a redirect probe per origin, then per origin × {390,1280} × {fragment, empty, latest, file, reject}, each response's sha256 asserted equal to the bound publication's digest (`check_stub_handoff_live.cjs:24` `exact()`, message *"Live component differs from its bound publication"*) | `push` to `main`, `workflow_dispatch` — not `pull_request` (workflow triggers on PR) |
| S9 | `.github/workflows/townlife-verify.yml:296`, gate at `:297` | `if: github.event_name == 'push' && github.ref == 'refs/heads/main'` | `tools/townlife/verify_live.mjs --expected-sha "$GITHUB_SHA"` — exact deployment binding, live served bytes, mobile shelf and cache readback. Origin is derived per route via `tools/lib/estate-map.cjs`, not pinned | `push` to `main` only |

**Site subtotal: 9** gated proofs. **7** if S5+S6+S7 are collapsed to one workflow-level proof for `maker-splash-canon-verify.yml`. The collapsed 7 is exactly RF2's Site figure.

##### LESSONS — `Lessons` @ `aad04718` — **4**

| # | File : line | Gating condition (verbatim) | What it asserts | Which event actually executes it |
|---|---|---|---|---|
| L1 | `.github/workflows/fieldops-p2-and-sweep.yml:359`, gate at `:360` | `if: github.event_name != 'pull_request'` | `tools/prepare_served_publications.py … --wait-seconds 1800` recovers the successful **source-bound** publication artifact for each checked-out source (Site, Lessons, Apps, shelf) — it asserts such a publication exists for this SHA and binds its artifact | `push` to `main`, `schedule` (`41 5 * * 1`), `workflow_dispatch` |
| L2 | `.github/workflows/fieldops-p2-and-sweep.yml:370`, gate at `:371` | `if: github.event_name != 'pull_request'` | `tools/verify_served.mjs` — every original subject across the three estates serves the exact bytes of the publication recovered by L1 | same as L1 |
| L3 | `.github/workflows/mbm-cross-estate-unification.yml:205` (job `live-proof`), gate at `:211`; asserting steps `:226`, `:254` | `if: github.event_name == 'push' \|\| github.event_name == 'workflow_dispatch'` (the in-file comment at `:206-210` records that this was `!= 'pull_request'` and was renamed positively when the `schedule` trigger was added) | `:226-252` polls `https://madebymatt.uk/Lessons/?mbm=$GITHUB_SHA` up to 60× for the marker `mbm-cross-estate-unification-lessons-apps-2026-08-08`, then 6 routes must answer 200, the manifest must parse, and four platform assets must `cmp` byte-identical to the checkout; `:254-258` runs `verify_cross_estate_browser.mjs` against the served base | `push` to `main`, `workflow_dispatch`. **Not** `schedule` and **not** `pull_request` — both are triggers on this workflow (`:4`, `:46`) |
| L4 | `.github/workflows/science-teaching-packs.yml:61`, gate at `:62` | `if: github.event_name == 'workflow_run' \|\| (github.event_name == 'workflow_dispatch' && inputs.verify_live)` | `check_hub_browser.cjs` against `SCIENCE_PACK_BASE_URL: https://madebymatt.uk/Lessons/Science_Teesside/Teaching_Packs/` — the published hub and all refreshed download bytes | `workflow_run` (completion of *Education Pages publication* on `main`), or `workflow_dispatch` with `verify_live=true`. **Not** `pull_request`, which is a trigger at `:3` |

**Lessons subtotal: 4.** This is the +1 over both LP1's carried 3 and RF2's 3: **L4 was missed by both.**

##### APPS — `Matt-s-Apps-` @ `4cb8a634` — **4**

| # | File : line | Gating condition (verbatim) | What it asserts | Which event actually executes it |
|---|---|---|---|---|
| A1 | `.github/workflows/verify-teesside-maker-lab-pro.yml:36` (job `live-bytes`), gate at `:39`; asserting step `:45-51` | `if: github.event_name == 'push' && github.ref == 'refs/heads/main'` | `tools/makerlab/verify_live_bytes.py --base https://madebymatt.uk/Matt-s-Apps-/ --sha "$GITHUB_SHA"` — every file in the payload **manifest** (not a typed list) serves bytes equal to what was merged; each request cache-busted with the merge SHA and `no-store`, retried until match or attempts exhausted | `push` to `main` only. Workflow also triggers on `pull_request` (`:4`) and `workflow_dispatch` (`:18`); both skip this job |
| A2 | `.github/workflows/verify-teesside-maker-lab-pro.yml:59` (job `live-acceptance`), gate at `:63`; asserting step `:75-76` | `if: github.event_name == 'push' && github.ref == 'refs/heads/main'` | `tools/makerlab/verify_live_acceptance.mjs https://madebymatt.uk/Matt-s-Apps-/` — browser acceptance test plus a forged-message negative control on the published origin | `push` to `main` only |
| A3 | `.github/workflows/verify-lundyloop-professional-os.yml:93` (job `live-bytes`), gate at `:94`; asserting step `:113-122` | `if: github.event_name == 'workflow_run' && github.event.action == 'completed' && github.event.workflow_run.status == 'completed' && github.event.workflow_run.conclusion == 'success' && github.event.workflow_run.head_branch == 'main' && github.event.workflow_run.head_repository.full_name == github.repository && (github.event.workflow_run.event == 'push' \|\| github.event.workflow_run.event == 'workflow_dispatch')` | `tools/lundyloop/verify_live_bytes.py --base https://madebymatt.uk/Matt-s-Apps-/ --sha "$PUBLICATION_SOURCE_SHA"`, with the builder ref resolved from the publication itself at `:105-112` | `workflow_run` completion of *Education Pages publication* on `main` **only**. The sibling `verify` job at `:41` runs on `pull_request`, so the workflow produces a PR check while this job skips |
| A4 | `.github/workflows/mbm-cross-estate-unification.yml:193` (job `live-proof`), gate at `:194`; asserting steps `:209`, `:237` | `if: (github.event_name == 'push' && github.ref == 'refs/heads/main') \|\| github.event_name == 'workflow_dispatch'` | Same shape as L3: `:209-235` polls `https://madebymatt.uk/Matt-s-Apps-/?mbm=$GITHUB_SHA` for the marker, 6 routes 200, `apps.json` parses, four platform assets `cmp` byte-identical; `:237+` proves the served responsive/standalone estate | `push` to `main`, `workflow_dispatch`. Not `pull_request` (`:4`), not `schedule` (`:cron 9 7 * * *`) |

**Apps subtotal: 4.** Double LP1's carried 2, and +1 over RF2's 3: **`verify-teesside-maker-lab-pro.yml` carries two independently gated live jobs (`:39` and `:63`), not one.**

##### GAMES — `Games` @ `809b6c9a` — **1**

| # | File : line | Gating condition (verbatim) | What it asserts | Which event actually executes it |
|---|---|---|---|---|
| G1 | `.github/workflows/play-domain-publication.yml:145` (job `verify-published`), which carries **no `if:` of its own**; it skips through `needs: deploy` (`:146`) and `deploy`'s gate at `:132`; asserting step `:187-191` | `if: github.ref == 'refs/heads/main' && (github.event_name == 'push' \|\| (github.event_name == 'workflow_dispatch' && inputs.publish))` — at `:132`, **inherited** | `domain-split/play/check.cjs` with `PLAY_REVIEW_URL: https://www.madebymatt-play.uk` — published phone and desktop discovery, previews, and retained game payloads, against expected payloads rebuilt at `:184` from the accepted publication tuple | `push` to `main`, or `workflow_dispatch` with `publish=true`. Workflow triggers on `pull_request` at `:5`, so a PR runs `build` (producing a check) while `deploy` and therefore `verify-published` skip |

**Games subtotal: 1.**

#### §1.1 VERDICT

| | Site | Lessons | Apps | Games | **Total** |
|---|---|---|---|---|---|
| **LP1 §1.1 carried** | 6 | 3 | 2 | 1 | **13** |
| RF2 interim | 7 | 3 | 3 | 1 | 14 |
| **Measured (per gate)** | **9** | **4** | **4** | **1** | **18** |
| **Measured (collapsed)** | **7** | **4** | **4** | **1** | **16** |

**13 is CONTRADICTED.** Contradicted on **Site** (6 → 9, or 7 collapsed), **Lessons** (3 → 4), **Apps** (2 → 4). **CONFIRMED on Games** (1 → 1).

The one component where this bears on §5's stop condition *"the census contradicts §1.1 in a way that changes the scope materially"* is **Apps: the carried figure is half the measured one.** Site's gap is partly a counting convention (collapsed vs per-gate); Lessons' and Apps' gaps are proofs that were simply not on the list.

---

### §1.2 — "For each, classify the assertion: served bytes, route reachability, marker presence, or content equality."

Exactly the four named classes. One class per proof; where a proof spans two I give the dominant and name the other.

| # | Class (dominant) | Spans / note |
|---|---|---|
| S1 | **served bytes** | Spans **content equality** at `:376` (the browser leg asserts rendered behaviour, not bytes). Dominant is served bytes: `:361` is what gives the job its name and its byte-for-byte comparison of 13 deployed pages |
| S2 | **served bytes** | `verify_v4_games_deployment.mjs:34` `liveBytes` — the live publication's payload bytes |
| S3 | **route reachability** | `fetch(\`${EDU_ORIGIN}${game.route}\`, {redirect:'follow'})` at `:352` — does the education origin answer this route |
| S4 | **route reachability** | Pure, and self-declared so: the job name at `:1265` is *"Routes serve 200 and removed paths 404 — reachability, not deployment"* |
| S5 | **content equality** | The honest label is *deployment identity* — none of the four classes names it exactly. Closest is content equality (served content must equal the commit named by `github.event.deployment.sha`). Flagged because this mismatch is precisely why §1.3 puts it in NOT POSSIBLE |
| S6 | **content equality** | `assert served_regions[0] == committed_regions[0]` at `:201`, with sha256 of both recorded. Spans **marker presence** (the `MBM-MAKER-SPLASH:BEGIN/END` region delimiters at `:166-168` are the marker the equality is scoped to) |
| S7 | **marker presence** | Behavioural: splash appears / skips / restores focus across SS1–SS8. Marker presence is the closest of the four — it probes for splash DOM state. Noted as behavioural because none of the four classes is a clean fit |
| S8 | **served bytes** | `check_stub_handoff_live.cjs:24` sha256 of each response vs the bound publication digest. Spans **route reachability** (the redirect probe at `:38-40` classifies an origin `UNAVAILABLE_ORIGIN` on 3xx before any byte assertion) |
| S9 | **served bytes** | Spans **content equality** (mobile shelf) and **route reachability** (cache readback). Dominant is served bytes — the step's own name leads with "live bytes" |
| L1 | **content equality** | Again the honest label is *publication provenance* — it asserts a successful source-bound publication for this SHA exists and binds its ZIP digest. Content equality is the closest of the four (artifact digest equality). Flagged for the same reason as S5 |
| L2 | **served bytes** | Pure. Step name: *"Every original subject serves the exact successful publication"* |
| L3 | **served bytes** | Spans all three of the others: **marker presence** (`grep -Fq 'mbm-cross-estate-unification-lessons-apps-2026-08-08'` at `:237`), **route reachability** (6 routes 200 at `:244-246`), **served bytes** (`cmp "assets/$asset" "/tmp/$asset"` at `:250`). Dominant is served bytes — `cmp` is the only hard equality in the job |
| L4 | **content equality** | *"the published hub and exact download bytes"*. Spans **route reachability** (the hub must answer) |
| A1 | **served bytes** | Pure, manifest-driven. Docstring: *"Prove the Maker Lab suite serves exactly the bytes that were merged"* |
| A2 | **marker presence** | Behavioural acceptance + forged-message control; same caveat as S7 |
| A3 | **served bytes** | Pure, same instrument family as A1 |
| A4 | **served bytes** | Identical span profile to L3 (marker at `:220`, reachability at `:227-229`, `cmp` at `:233`) |
| G1 | **served bytes** | *"retained game payloads"*. Spans **marker presence** (phone/desktop discovery and previews) |

**Class tally over 18:** served bytes 9 (S1, S2, S8, S9, L2, L3, A1, A3, A4 — and G1 = 10 counting G1) — precisely: **served bytes 10** (S1, S2, S8, S9, L2, L3, A1, A3, A4, G1), **route reachability 2** (S3, S4), **content equality 4** (S5, S6, L1, L4), **marker presence 2** (S7, A2). Total 18.

**The class does decide possibility, as §1.2 predicts.** Every one of the 4 content-equality rows either is or contains an origin-identity claim; two of them (S5, L1) are the ones with no PR-time mode at all. Every route-reachability row is possible. The served-bytes rows split on whether the "bytes" are bound to a *deployment* or merely to a *served response*.

---

### §1.3 — "Report which of the 13 CANNOT have a PR-time mode and why."

Measured against §2.1's definition, quoted: *"Each proof gains a second subject: the PR's own build, served locally in the runner, asserted with the same predicate as the live run."* Every one of the 18 is answered.

#### NOT POSSIBLE — 3 outright

| # | Verdict | Why |
|---|---|---|
| **S5** `maker-splash-canon-verify.yml:140` | **NOT POSSIBLE** | The subject *is* the deployment. `verify_deployment_provenance.py --expected-sha "${{ github.event.deployment.sha }}"` asks "did a deployment of this SHA happen, and is it the one being served". A PR branch has no deployment and no `github.event.deployment`. There is no local analogue of the predicate — a locally served build trivially "is" the PR's build, so the assertion would be a tautology. This is §2.4's case: report UNMEASURED, never green |
| **S8** `hc3-stub-handoff.yml:102` | **NOT POSSIBLE** as stated | The journey is a genuine **cross-origin** hop between two real Pages sites (education origin → play origin), including a redirect-availability probe that classifies an origin `UNAVAILABLE_ORIGIN` on 3xx (`check_stub_handoff_live.cjs:38-40`). One local server cannot reproduce two distinct public origins with their real redirect behaviour and their real storage partitioning. **Note:** the composed-fixture equivalent already exists as this workflow's own PR-side `handoff` job (`:38-53`, `check_stub_handoff_browser.cjs .handoff-fixture`), so the honest §2.4 report is UNMEASURED-for-the-live-journey with the fixture job named as what *is* covered |
| **L1** `fieldops-p2-and-sweep.yml:359` | **NOT POSSIBLE** | Its entire subject is "a successful publication run exists on `main` for this SHA, and here is its artifact, bound by run id, deployment attempt, upload window and ZIP digest". A PR has no publication run on `main`. The `--wait-seconds 1800` at `:367` exists solely because it waits for that run. There is nothing local to wait for |

#### MIXED — 6 (the origin/deployment leg impossible, the assertion leg possible)

| # | Verdict | Why |
|---|---|---|
| **S1** `verify-games-audience-faces.yml:334` | **MIXED — dominant NOT POSSIBLE** | `:361` binds the exact successful **Pages artifact** and its deployment attempt — impossible for a PR, same reason as L1. `:376` (the browser leg) **IS POSSIBLE**, and the machinery is already in the file: `:285-296` starts `python3 -m http.server 4173 --bind 127.0.0.1 --directory _served` and runs the *same* `verify_audience_discovery_browser.py` against it on every event. The residue is `--publication education`, which is a framing argument, not an origin |
| **S2** `v4-games-deployment-verify.yml:163` | **MIXED — mostly already built** | `verifyLivePublication()` (the claim "the play origin serves this") is **NOT POSSIBLE**. Everything else **already has** a PR-time mode: `verify_v4_games_deployment.mjs:1019` `const local = LIVE_ORIGIN ? null : await startServer();` serves the PR's own build and `:1028`/`:1035` run extra local-only legs. The §2.3 defect here is that the two modes are **not visibly distinguishable** in a way that can be read as UNMEASURED: `:1037` prints `extras` differently, but the step name and the check name are identical and the job is green either way |
| **S9** `townlife-verify.yml:296` | **MIXED — dominant NOT POSSIBLE** | The deployment binding (`GITHUB_TOKEN` at `:299`, `--expected-sha "$GITHUB_SHA"`) and the CDN cache readback cannot exist for a PR. The "live bytes == committed bytes" and "mobile shelf" halves **ARE POSSIBLE** against a locally served build, and `tools/townlife/verify_live.mjs:12-25` already derives the origin per route through `lib/estate-map.cjs` rather than pinning one, so a local base is a supported substitution rather than a rewrite |
| **L3** `mbm-cross-estate-unification.yml:205` (Lessons) | **MIXED** | `:226-252`, the wait-for-deployment loop, is **NOT POSSIBLE** (it polls a public URL for a marker and a SHA). `:254-258`, `verify_cross_estate_browser.mjs` over the served estate, **IS POSSIBLE** — and the same workflow's `browser-matrix` job already runs that identical instrument against a local mount at `:136-182` (`MBM_BASE_URL="http://127.0.0.1:4176/"` at `:182`). The four-asset `cmp` at `:250` is also possible locally |
| **A4** `mbm-cross-estate-unification.yml:193` (Apps) | **MIXED** | Identical to L3, line-for-line in shape (`:209-235` wait leg impossible; `:237+` assertion leg possible) |
| **G1** `play-domain-publication.yml:145` | **MIXED** | The `needs: deploy` half — "a deployment happened" — is **NOT POSSIBLE** by construction; the job literally depends on the deploy it verifies. The assertion half **IS POSSIBLE** and is unusually cheap: the `build` job already assembles the full artifact at `:66-86` and uploads it at `:82-87`, and `:184` rebuilds the expected payloads. Pointing `PLAY_REVIEW_URL` (`:190`) at a local server over `.sources/Site/domain-split/output/games` runs `check.cjs` with the same predicate |

#### POSSIBLE — 9

| # | Verdict | Why |
|---|---|---|
| **S3** `v4-games-deployment-verify.yml:164` | **POSSIBLE** | Route reachability against a locally served education build. `domain-split/build_education.py` produces that build in-runner. The cross-origin-split claim (that `madebymatt.uk` answers a game route as a *stub*) survives the substitution because the stub is produced by `build_education.moved_page`, which is part of the build |
| **S4** `mbm-audience-discovery-closeout.yml:1264` | **POSSIBLE**, and the cleanest case of all | The predicate is "these 13 derived routes answer 200 and two removed paths 404". The route set is already derived from `data/audience-homepages.json` in-runner (`:1288-1295`), with an empty read refused rather than passed. Point `base` at a local server over the PR's own education build and the predicate is identical. The job's own comment at `:1301-1313` already disclaims any deployment meaning, so nothing is lost |
| **S6** `maker-splash-canon-verify.yml:148` | **POSSIBLE** | Pure content equality of a delimited region. The local-origin adapter **already exists** in this very file at `:121-138` (`Pull-request origin-adapter control`, `python3 -m http.server 8765 --bind 127.0.0.1`, same instrument, `--origin=http://127.0.0.1:8765`). This is LP1 §2.1's exact shape, already implemented for a neighbouring step |
| **S7** `maker-splash-canon-verify.yml:209` | **POSSIBLE** | Same as S6 — the `:121` adapter already proves `--mode=verify --scope=site` works against a local origin; `--mode=controls` needs the same base and no new mechanism |
| **L2** `fieldops-p2-and-sweep.yml:370` | **POSSIBLE** with a substituted basis | `verify_served.mjs`'s predicate is "each original subject's served bytes equal the publication's bytes". If L1's recovered artifact is replaced by a publication **built locally from the PR's merge ref**, the predicate is preserved exactly. This is not speculative: `agx1-live-verify.yml:163-176` already does precisely that for the Site publication (`Reproduce the candidate publication from the merge ref`, gated `if: github.event_name == 'pull_request'` at `:167`) |
| **L4** `science-teaching-packs.yml:61` | **POSSIBLE**, and all but built | The same instrument, `check_hub_browser.cjs`, **already runs against a local server on a PR** at `:48-60` (`python -m http.server 4187 --bind 127.0.0.1`). The only residue is the "exact refreshed download bytes" leg, which is content equality and works identically against a local origin |
| **A1** `verify-teesside-maker-lab-pro.yml:36` | **POSSIBLE** | `verify_live_bytes.py` compares served bytes to a manifest-derived inventory; `--base` becomes the local server and `--sha` the merge SHA. **Caveat stated honestly:** the tool's docstring claims *"a match cannot be a CDN copy of the previous deploy"* — that specific claim is about a CDN and is **not** reproducible locally. A PR-time mode must not inherit that sentence, or it asserts something weaker under the same name, which is §5's first stop condition |
| **A2** `verify-teesside-maker-lab-pro.yml:59` | **POSSIBLE** | A browser acceptance test plus a forged-`postMessage` negative control is origin-agnostic; both work against `http://127.0.0.1:<port>/Matt-s-Apps-/` |
| **A3** `verify-lundyloop-professional-os.yml:93` | **POSSIBLE** | Same shape as A1, same caveat. One extra note: its gate is `workflow_run`-only, so its PR-time mode would also have to be a *new* job on the `pull_request` trigger, not a relaxation of `:94` |

#### §1.3 tally over 18

**3 outright NOT POSSIBLE** (S5, S8, L1) · **6 MIXED** (S1, S2, S9, L3, A4, G1) · **9 outright POSSIBLE** (S3, S4, S6, S7, L2, L4, A1, A2, A3).

Restated as §1.3 asks ("which CANNOT"): **9 of 18 carry a leg that cannot have a PR-time mode** (3 wholly + 6 partly), and in every one of those 9 the impossible leg is the same thing — **a claim about the public origin or about a deployment having happened**. That is the pattern §1.3 predicts, and it is worth recording as the finding rather than as nine separate notes.

**Encouraging measured fact for §2:** five of the 18 already have a working local-serve analogue *in the same file* — S1 (`:289`), S2 (`verify_v4_games_deployment.mjs:1019`), S6/S7 (`:121-138`), L3/A4 (`:182`/local mount), L4 (`:53-60`) — plus `agx1-live-verify.yml:163-176` as the merge-ref-rebuild precedent for L2. §2 is substantially a generalisation of patterns this estate has already written, not a new mechanism.

---

### §4.3 — vacuous rather than skipped

§4.3 verbatim: *"Where a proof is vacuous rather than skipped — asserting stub existence, or fetching an education route from a Play default — rename it to assert what it actually tests, or retarget it per ESTATE_MAP."*

#### V1 — `tools/verify_published_live.mjs:173` — **"fetching an education route from a Play default" — LOCATED, confirmed**

```
 50  const ORIGIN = val('--origin') || 'https://madebymatt-play.uk';
 56  const EDU_ORIGIN = val('--education-origin') || 'https://madebymatt.uk';
 90  const PATHS = [
 91    ...GAME_PATHS.map((p) => ({ p, kind: 'game' })),
 92    ...TOOL_PATHS.map((p) => ({ p, kind: 'tool' })),
 93  ];
173    const { status, body } = await fetchBytes(ORIGIN + p);          // ← every path, tool paths included
179    if (kind === 'game') {
181      const edu = await fetchBytes(EDU_ORIGIN + p);                 // ← EDU_ORIGIN only ever used here
185    }
```

`:173` fetches **every** path — `kind: 'tool'` included — from `ORIGIN`, which defaults to the **Play** origin at `:50` and is passed as `--origin "$PLAY"` by the only caller, `.github/workflows/published-live-verify.yml:155`. `EDU_ORIGIN` is consulted **only** inside the `if (kind === 'game')` branch at `:179-185`. A teacher-tool route is therefore fetched from the Play origin and its served bytes compared to the committed education blob — an assertion that cannot pass and is not about what the caller believes it is about.

The caller's own comment states the opposite intent, at `published-live-verify.yml:151-152`: *"Tool routes stay on the education origin."* The input description at `:28` names `/artsaward/` as the example tool path — an education route.

**Disposition per §4.3: retarget** (route `kind: 'tool'` through `EDU_ORIGIN` at `:173`), not rename. The intent is documented and correct; only the origin selection is wrong. Note `tools/lib/estate-map.cjs` already exists and answers "who serves this route" — `tools/townlife/verify_live.mjs:12-25` records this exact bug being fixed in the other direction (an education origin pinned and asked for Play routes) and names `estate-map.cjs` as the repair. Same fix, same helper.

#### V2 — `.github/workflows/published-live-verify.yml:30` — **vacuity by empty input**

```
 27        tool_paths:
 28          description: 'Space-separated TEACHER TOOL paths — serve, and must NOT be on the arcade shelf. e.g. "/artsaward/"'
 29          required: false
 30          default: ''
...
143          [ -n "$paths$tool_paths" ] || paths='/ouroboros/ /novasiege/'
166          [ -n "$paths${{ inputs.tool_paths }}" ] || paths='/ouroboros/ /novasiege/'
```

`tool_paths` defaults to the **empty string**, and the workflow's non-dispatch triggers are `push` (`:31-38`) and `schedule` (`:39-40`), neither of which can supply an input. So on **every push and every weekly scheduled run**, `TOOL_PATHS` is empty, `PATHS` contains only games, and the entire tool-route leg — including `:194-195`'s *"correctly absent from the arcade shelf"* — **asserts nothing**. The gate reports green having judged zero tool routes.

This is vacuity of the second kind: not a wrong subject but **no subject**. It also means V1 is currently **latent** — the Play-default bug fires only on a `workflow_dispatch` where someone types a tool path. Both need fixing together, or fixing V1 alone changes nothing observable.

**Disposition per §4.3: a DECISIONS-backed change** — either derive the tool-path set (the estate's own pattern, cf. `mbm-audience-discovery-closeout.yml:1288-1295`, which derives its routes and *refuses an empty read* rather than treating it as "nothing to check"), or rename the gate to state that it proves game paths only.

#### "asserting stub existence" — **NOT LOCATED**

I searched for it and did not find it. Rather than infer one, I state the negative with the reason.

- `grep -rniE "exists|is_file|isfile|os.path.exists|test -f|test -e" .github/workflows/*.yml | grep -iE "stub|handoff"` over Site returned **zero rows**.
- The two stub instruments both judge substantively, not by existence:
  - `tools/verify_education_stubs.py:5-13` asserts HTTP 200 with no redirect off the education origin, ≤2048 bytes, a `data-game-moved` marker, `<meta name="robots" content="noindex">`, a canonical to the play origin, exactly one link, no `<canvas>`, and no external script other than `/stub-handoff.js`. Its route set is derived by `tools/route_origins.py`, *"never typed here"* (`:15`).
  - `tools/verify_published_live.mjs:69-85` (`judgeStub`) applies the same eight predicates inline, including the subtle one at `:73` — a route that *redirects* to play is rejected as *"served by redirect, not a stub"*, which is exactly the existence-vs-behaviour distinction §4.3 is worried about, already handled.
- `domain-split/stub_handoff.py:16,22` and `domain-split/check_stub_handoff.cjs:12-24` likewise assert behaviour (plan shape, origin, `?view=calm`, base64url round-trip, size ceilings, and a planted-key mutation that must throw), not existence.

**Conclusion: the "stub existence" half of §4.3 is NOT LOCATED in the 97-file scan set or in the stub instruments those files invoke.** If it exists it is somewhere I did not scan — most plausibly in a repo-local script not referenced by any workflow. I have not inferred one.

---

### Reported separately, NOT folded into the 18

#### (a) Live proofs that run on a PR against the LIVE origin — worse than a skip

These do not skip; they execute on a `pull_request` while their subject remains the **already-published** site. Their PR verdict is therefore about `main`, not about the PR. §0.2's *"that green is an ABSENCE, not evidence"* has a sibling here: this green is evidence **about the wrong thing**.

| File : line | Gate | Note |
|---|---|---|
| `Site verify-games-audience-faces.yml:277-283` | `if: github.event_name == 'pull_request'` | Step name is *"Check the published Education audience pages **before merge**"*, and it fetches `MBM_BASE_URL=https://madebymatt.uk/`. It cannot see the PR's content |
| `Lessons mbm-cross-estate-unification.yml:184-188` | **no `if:`** | `MBM_BASE_URL="https://madebymatt.uk/$prefix/"` inside the un-gated `browser-matrix` job (`:121`) |
| `Apps mbm-cross-estate-unification.yml:160-164` | **no `if:`** | Identical |
| `Site echovault-surfaces-verify.yml:72-87` | job `if:` at `:59-62` excludes only non-success `deployment_status` | Live `https://www.madebymatt-play.uk/games.json` fetch with a hard assert at `:87`, runs on PR |
| `Site relicforge-surfaces-verify.yml:72-87` | same (`:59-62`) | Same shape |
| `Site post-merge-production-verify.yml:145`, `:177` | no event gate on job `verify` (`:69`) | The file **says so itself** at `:157-160`: *"these five read LIVE production, so on a PR they can only ever report the pre-merge world — which is why they are red on the PR and why that red is not evidence about the merge"* |
| `Games play-domain-publication.yml:88-122` | no `if:` | Comment at `:103`: *"This read-only guard runs on PRs too, before a pin is merged"* — deliberate, and it asserts the live catalogue population against `play-publication.json` |
| `Site agx1-live-verify.yml` job `live` (`:31`) | no job gate | Fetches live throughout (`:322`, `:350`, `:367`, `:412`, `:444`, `:487`, `:593`, `:817`, `:820`). **Partially PR-aware already**: `:133-176` build a candidate publication from `refs/pull/N/merge` and `:177-198` swap the comparison basis to it when `main` does not reproduce. This is ML1's subject, not LP1's, and I flag it only so it is not double-counted |

#### (b) Live proofs in workflows with **no** `pull_request` trigger — 21

These produce **no check on a PR at all**, so nothing "reports green"; they fall outside LP1 §0.1's stated population. Measured from the trigger census (pass 1) intersected with the subject census (pass 4).

- **Site (11):** `driving-games-live-verify.yml`, `neonbreach-live-verify.yml`, `olympics-live-verify.yml`, `titan-crown-live-verify.yml`, `published-live-verify.yml`, `serve-witness.yml`, `mbm-deployment-provenance.yml`, `professional-site-live-verify.yml`, `published-completion-verify.yml`, `mtr-live-gate.yml`, `education-publication.yml`
- **Lessons (5):** `wave-ohm-deck-live.yml`, `glv3-production-byte-check.yml`, `j4-absolute-ref-probe.yml`, `watch-main.yml`, `education-pages.yml`
- **Apps (3):** `stealth-live-verify.yml`, `wave-ohm-origin-drive.yml`, `education-pages.yml`
- **Games (2):** `apexpool-sports-verify.yml`, `pin-release.yml`

Two are worth naming because they are the estate's own best answer to LP1's problem and should inform §2 rather than be repaired by it: `Site serve-witness.yml:1-11` (*"publication is not served until the origin's bytes say so"* — byte-witnesses four publications daily, and is explicit that *"an unreachable route or a missing exact-source publication is INCONCLUSIVE, never green"*, which is §2.4's rule already in force); and `Lessons s1l-publication-readback.yml:26-29` / `s1m-published-input-proof.yml:31-34`, which are **`pull_request`-only** jobs that read the **deployed artifact via the GitHub API** rather than over HTTP — a third mode neither §2.1 nor this census anticipated, and a viable PR-time subject for several of the rows §1.3 marks MIXED.

---

### Evidence discipline notes

- **Every number has its denominator.** 18 of 97 workflow files' worth of gates; Site 9 of 58 files (47 of which trigger on PR); Lessons 4 of 22 (17 on PR); Apps 4 of 8; Games 1 of 9.
- **YAML read, not run observed.** Every gating condition above is a **condition read from the workflow file at the stated SHA**. I executed no workflow, dispatched nothing, and read no run logs. Where I say "on a PR this skips", that is the YAML's meaning, not an observed run. The one place I checked instrument behaviour beyond YAML (S2/S3, `verify_v4_games_deployment.mjs:1017-1037`) is labelled as a source read.
- **Not measured / not measurable, with reasons:** (i) whether any of the 18 has *ever* in fact reported green on a PR — that needs run history, which I did not query; (ii) whether the §4.3 "stub existence" case exists outside the workflow-reachable file set — see NOT LOCATED above; (iii) the runtime cost of each proposed PR-time mode — §2 territory, out of scope.
- **§2, §3 and beyond not attempted**, per the task's explicit exclusion. No PR-time mode is proposed or written here; where I name an existing local-serve analogue it is as *census evidence that a mode is possible*, not as a design.
---

# ORDER PIN1 — §1 census

# ORDER PIN1 §1 — READBACK (measure only)

**Scope actually executed:** §1.1, §1.2, §1.3. §2 (derivation) and §3 (proofs) NOT attempted — out of scope per the task. No commits, pushes, GitHub writes, PR comments or workflow dispatches were made. Everything below is a **READ of YAML and source**, never a run OBSERVED: I executed no workflow and inspected no Actions run.

**§0.3 compliance.** Nothing in this readback is framed as the GLV3 hole. GLV3's pathspec is an isolation guard; `.github/workflows/glv3-verify.yml` appears below only as a *pinned file* (a row in `CATALOGUE_PINS["files"]`), never as a cause. The finding stands on the measurement below.

---

## §1.1 — Enumerate the pin set

### Scan set and denominator

The pin set is declared in exactly one file, and it is the same file in both repos that run it:

| | |
|---|---|
| File | `/home/user/Lessons/tools/verify_cross_estate_unification.py` |
| Lessons main | `aad04718c11a2396ecf323a662f55bf0e0c2441b` |
| sha256 | `04c40f7e5a83d3daad795e7310c2ee1f19d7ab16b88779e016171fa51f125ddc` |
| lines | 1265 |
| Apps copy | `https://raw.githubusercontent.com/MattRoper1977/Matt-s-Apps-/4cb8a634dbeaa3d98d7699252fdfff4253c47eef/tools/verify_cross_estate_unification.py` |
| Apps sha256 | `04c40f7e5a83d3daad795e7310c2ee1f19d7ab16b88779e016171fa51f125ddc` — **byte-identical**; blob `7580d222d3ac51df7b15fc58fe77a04e3780d3b7` matches the SHA the API returned |
| Site copy | **does not exist** (`ls tools/verify_cross_estate_unification.py` → No such file) |
| Games copy | **does not exist** (`search_code "verify_cross_estate_unification repo:MattRoper1977/Games"` → `total_count: 0`) |

```
$ cd /home/user/Lessons && git rev-parse HEAD && sha256sum tools/verify_cross_estate_unification.py && wc -l tools/verify_cross_estate_unification.py
aad04718c11a2396ecf323a662f55bf0e0c2441b
04c40f7e5a83d3daad795e7310c2ee1f19d7ab16b88779e016171fa51f125ddc  tools/verify_cross_estate_unification.py
1265 tools/verify_cross_estate_unification.py
```

Counts were re-derived by AST-parsing the file (script at `/tmp/claude-0/-home-user-Lessons/05c13970-a6c0-53bf-90f1-2f5c998f17c1/scratchpad/census.py`), not read from any prior report. Two registries reference earlier names and so need a resolving namespace rather than bare `ast.literal_eval`.

### The five registries

| # | Registry | file:line | Count | Asserted at (verifier) | Gate(s) that assert it — workflow file:line |
|---|---|---|---|---|---|
| 1 | `CANONICAL_HASHES` | `tools/verify_cross_estate_unification.py:60` | **4** | `:1017-1023` | **A** Lessons `.github/workflows/mbm-cross-estate-unification.yml:101`; **C** Apps `.github/workflows/mbm-cross-estate-unification.yml:98`; **D** Apps `.github/workflows/verify-lundyloop-professional-os.yml:71` |
| 2 | `MANIFEST_PINS` | `:99` | **2** (`apps.json`, `resources.json`) | `:1027-1034` | A (`resources.json` only — `apps.json` absent, loop `continue`s at `:1029-1030`); C and D (`apps.json` only) |
| 3 | `CATALOGUE_PINS["files"]` | `:118`, inside the `# BEGIN/# END REVIEWED CATALOGUE PINS` block `:117-:557` | **434** | `:835-843` (`catalogue_errors`, which returns `[]` unless `kind == "lessons"`, `:797-798`) | **A only** |
| 4 | `LUNDYLOOP_CI_PINS` | `:643` | **3** | `:899-903` (returns `[]` unless `kind == "apps"`) | **C and D only** |
| 5 | Publisher caller — `PUBLICATION_CALLER_PATH` `:599`, digests `PUBLICATION_CALLER_SHA256` `:618` and `PUBLICATION_CALLER_SHA256_BY_KIND` `:633` | `:599` / `:633` | **1 path** (2 digest entries, keyed by repo *kind*, both naming the same path `.github/workflows/education-pages.yml`) | `:889-896` | A, C, D |

**Union: 444 distinct paths. Sum of the five registry sizes: 444. Zero overlap.** The four path-keyed file registries alone (1–4) union to **443**.

```
$ python3 .../census.py
CANONICAL_HASHES  line=60  count=4
MANIFEST_PINS  line=99  count=2
CATALOGUE_PINS['files'] count= 434       (line=118)
LUNDYLOOP_CI_PINS  line=643  count=3
PUBLICATION_CALLER_SHA256_BY_KIND line= 633 count= 2 keys= ['lessons', 'apps']
PUBLICATION_CALLER_PATH line= 599 = .github/workflows/education-pages.yml
=== overlaps ===
sum of sizes= 444 union= 444
union of 4 file registries (no publisher caller) = 443
```

### 89: CONTRADICTED

The real number is **444**. It is not a stale reading of an older state either:

```
$ git show e126664a5a4ae5f3bde19cafdf1d900b8324a108:tools/verify_cross_estate_unification.py | python3 .../countpins.py
#499 head:  CATALOGUE_PINS.files= 425 CANONICAL_HASHES= 4 MANIFEST_PINS= 2 LUNDYLOOP_CI_PINS= 3
#499 base (parent 389253de02da3df2ced6bc0e58ecfb1719787e5e):
            CATALOGUE_PINS.files= 425 CANONICAL_HASHES= 4 MANIFEST_PINS= 2 LUNDYLOOP_CI_PINS= 3
current main aad04718:
            CATALOGUE_PINS.files= 434 CANONICAL_HASHES= 4 MANIFEST_PINS= 2 LUNDYLOOP_CI_PINS= 3
```

At #499 — the PR PIN1 §0.1 draws its finding from — the set was **435** (425+4+2+3+1). #499 is merged (`git merge-base refs/pull/499/head origin/main` == the head itself). So 89 was wrong by ~4.9x at the moment of writing, and is wrong by ~5.0x now. **Where 89 came from: NOT LOCATED.** It matches no registry, no sum of registries, and no historical `CATALOGUE_PINS` size I could reach. I am not going to infer a provenance for it.

### Directory histogram of the 434 catalogue paths (denominator 434)

| Count | Top-level | Notes |
|---:|---|---|
| 345 | `Science_Teesside/` | of which **344** under `Science_Teesside/Teaching_Packs/` and 1 is `Science_Teesside/index.html` |
| 37 | `tools/` | `tools/catalogue` 11, `tools/humanities_resources` 9, `tools/science_teaching_packs` 8, `tools/ux2` 2, 7 singletons |
| 27 | `Humanities_Teesside/` | 26 under `David_Cover_Autumn1_W3-W7/` + `Humanities_Teesside/index.html` |
| 11 | `assets/` | all 11 under `assets/catalogue/` |
| 4 | `.github/` | `glv3-verify.yml`, `s1m-published-input-proof.yml`, `science-teaching-packs.yml`, `watch-main.yml` |
| 3 | (repo-root files) | `index.html`, `humanities_teesside.html`, `subject.html` |
| 3 | `_glv3/` | `tools/browser_verify.mjs`, `tools/chip_gate.mjs`, `tools/verify_change_boundary.py` |
| 2 | `primary/` | `year5/science/autumn/forces/{Lesson8_ExploreGravity.html, Y5_Forces_SoW_and_Plans.docx}` |
| 1 | `data/` | `data/calendar-spine.json` |
| 1 | `_sx2/` | `_sx2/DECISIONS.md` |
| **434** | **total** | |

All 434 exist in the Lessons working tree (0 missing).

### Non-pin lists in the same file — NOT folded into 444

Re-measured and confirmed, kept out of the denominator:

| Name | file:line | Count | Why excluded |
|---|---|---:|---|
| `CATALOGUE_RECORD_PATHS` | `:583` | 7 | boundary allowlist, carries no digest |
| `ALLOWED_DIFF` | `:649` | 47 | boundary allowlist (`boundary_errors` `:907-915`), carries no digest |
| `CATALOGUE_ORIGINAL_ROWS` | `:562` | 734 | a *row* count inside `resources.json`, not paths |
| `CATALOGUE_SHELF_ROWS` | `:570` | 216 | same |

---

## §1.2 — Trigger paths vs asserted paths, per gate

### Every gate that asserts any pin

Search over all four repos. Lessons and Site by local grep; Apps and Games by `mcp__github__search_code` + raw blob fetch at the returned SHA.

```
$ cd /home/user/Lessons && grep -rn "verify_cross_estate_unification\|pin_catalogue_contract" .github/workflows/
ux2-gates.yml:31/32, :46/47      (trigger paths only)
mbm-cross-estate-unification.yml:12, :25   (trigger paths)
mbm-cross-estate-unification.yml:101       (INVOCATION)

$ cd /home/user/mattroper1977.github.io && grep -rn "verify_cross_estate_unification\|pin_catalogue_contract" .github/
(no output — Site invokes it in no workflow, and does not carry the file)

search_code "verify_cross_estate_unification repo:MattRoper1977/Matt-s-Apps-" -> 5 hits incl.
  .github/workflows/mbm-cross-estate-unification.yml, .github/workflows/verify-lundyloop-professional-os.yml
search_code "verify_cross_estate_unification repo:MattRoper1977/Games"        -> total_count: 0
```

`tools/catalogue/pin_catalogue_contract.py` appears **only** as a trigger path (ux2-gates.yml:32, :47). No workflow in any of the four repos executes it. It is the re-pinning tool, not a gate.

**Four gates. Not two.**

| Gate | Repo | Workflow | Invocation | Job |
|---|---|---|---|---|
| A | Lessons | `.github/workflows/mbm-cross-estate-unification.yml` | `:101` | `static-contract` (`:76`) |
| B | Lessons | `.github/workflows/ux2-gates.yml` | `:81` (`tools/ux2/prove_catalogue_gate.py`) | `catalogue-contract` (`:64`) |
| C | Apps | `.github/workflows/mbm-cross-estate-unification.yml` | `:98` | `static-contract` (`:76`) |
| D | Apps | `.github/workflows/verify-lundyloop-professional-os.yml` | `:71` | `verify` (`:40`) |

### Gate B asserts none of the 444 — a correction to PIN1 §0.1's premise

§0.1 says "the two gates that validate the pins". Measured, **ux2-gates.yml validates none of them**. It triggers on the checker (`:31`, `:46`) and on the re-pinning tool (`:32`, `:47`), which is why it ran on #499 — but the assertion it makes is row-level, not file-pin-level:

- The only ux2 tool that loads the gate module at all is `tools/ux2/prove_catalogue_gate.py` (`grep -ln "CATALOGUE_PINS\|verify_cross_estate" tools/ux2/*` → that one file only).
- Its `main()` (`tools/ux2/prove_catalogue_gate.py:46-78`) asserts **only** through `row_errors()` (`:52-53`), whose filter admits an error only if it contains `"original catalogue row"`, `"hub rows"`, `"requires the original"` or `"carried"`.
- The file-pin failure string is emitted at `verify_cross_estate_unification.py:843` as `f"reviewed catalogue bytes differ: {rel}"`.

Empirically tested, not assumed:

```
error string: reviewed catalogue bytes differ: Science_Teesside/Autumn1/index.html
passes catalogue_errors_on() filter (stage 1): True
passes row_errors() filter (stage 2, the ONLY one main() uses): False
row-digest error passes stage2: True
```

The wider filter at `prove_catalogue_gate.py:43` would have admitted it; `main()` never calls that path unfiltered. The other ux2-gates jobs (`check_catalogue_schema.py`, `unit_tags.py`, `companion_catalogue.py`, `build_spine.py`, `resource_sizes.py`, `hub_gates.mjs`, `verify_lessons_chips.mjs`, `check_catalogue_dom.cjs`) contain **zero** references to any pin registry (`grep -c "sha256\|PINS\|digest" tools/catalogue/check_catalogue_dom.cjs` → `0`).

So gate B's asserted-pin set is **0 of 444**, and its asserted-but-not-triggered figure is **0 of 0 — vacuous, not clean**. Its `assets/catalogue/**`, `data/**`, `tools/ux2/**` globs buy no pin coverage whatsoever.

### Side-by-side

**Gate A — Lessons `mbm-cross-estate-unification.yml`**
Trigger paths, verbatim, `pull_request` `:6-16` (identical list repeated for `push` at `:19-29`), no globs:
```
      - index.html
      - assets/mbm-platform.css
      - assets/mbm-platform.js
      - assets/mbm-theme.js
      - assets/mbm-hub.css
      - tools/verify_cross_estate_unification.py
      - tools/verify_cross_estate_browser.mjs
      - docs/MBM_CROSS_ESTATE_UNIFICATION.md
      - .github/workflows/education-pages.yml
      - .github/workflows/mbm-cross-estate-unification.yml
```
plus `schedule: cron '53 6 * * *'` (`:46-47`) and `workflow_dispatch` (`:48`).

| | |
|---|---:|
| Asserted paths (kind=lessons, in this repo) | **440** of 444 (434 catalogue + 4 canonical + `resources.json` + publisher caller; the 3 LundyLoop pins short-circuit at `:899-900`, `apps.json` is absent) |
| Of those, triggered on | **6** — `index.html`, the 4 `assets/mbm-*` files, `.github/workflows/education-pages.yml` |
| **ASSERTED BUT NOT TRIGGERED** | **434 of 440** |

**Gate B — Lessons `ux2-gates.yml`**
Trigger paths verbatim, `pull_request` `:22-34` (repeated for `push` `:37-49`):
```
      - index.html
      - subject.html
      - resources.json
      - resources.schema.json
      - assets/catalogue/**
      - data/**
      - tools/ux2/**
      - tools/verify_lessons_chips.mjs
      - tools/verify_cross_estate_unification.py
      - tools/catalogue/pin_catalogue_contract.py
      - _sownb/CALENDAR_2026_27.json
      - .github/workflows/ux2-gates.yml
```
plus `schedule: cron '23 5 * * *'` (`:50-53`) and `workflow_dispatch` (`:54`).

| | |
|---|---:|
| Asserted pin paths | **0** of 444 |
| **ASSERTED BUT NOT TRIGGERED** | **0 of 0 — vacuous** |

**Gate C — Apps `mbm-cross-estate-unification.yml`**
Trigger paths: the same 10 as gate A (`pull_request` `:6-15`, `push` `:20-30`, which additionally watches branch `codex/mbm-cross-estate-unification-lessons-apps-2026-08-08`), `schedule: cron '9 7 * * *'` (`:51-52`), `workflow_dispatch`.

| | |
|---|---:|
| Asserted paths (kind=apps) | **9** — 4 canonical + `apps.json` + 3 LundyLoop + publisher caller |
| Triggered on | **5** — 4 canonical assets + `education-pages.yml` |
| **ASSERTED BUT NOT TRIGGERED** | **4 of 9** — `apps.json`, and all 3 `LUNDYLOOP_CI_PINS` |

**Gate D — Apps `verify-lundyloop-professional-os.yml`**
Trigger paths verbatim, `pull_request` `:5-14` (repeated `push` `:16-25`):
```
      - 'LundyLoop_Professional_OS.html'
      - 'LundyLoop_Professional_OS/**'
      - '_release-docs/lundyloop-professional-os-v2/**'
      - 'apps.json'
      - 'index.html'
      - 'tools/lundyloop/**'
      - 'tools/verify_cross_estate_unification.py'
      - '.github/workflows/verify-lundyloop-professional-os.yml'
```
plus `workflow_dispatch` (`:26`) and `workflow_run` on "Education Pages publication" (`:27-30`). No schedule.

| | |
|---|---:|
| Asserted paths (kind=apps) | **9** (same set as C) |
| Triggered on | **4** — `apps.json`, `tools/lundyloop/verify_live_bytes.py`, `tools/lundyloop/test_live_bytes.py`, `.github/workflows/verify-lundyloop-professional-os.yml` |
| **ASSERTED BUT NOT TRIGGERED** | **5 of 9** — the 4 canonical assets + the publisher caller |

Note the pairing: C and D are complementary. Between them, all 9 Apps-side pins are triggered on by at least one gate — **the LundyLoop pins are fully covered by gate D's own `tools/lundyloop/**` glob.** That direction of the Apps story is healthy.

### UNION figures — three, each with its scan set stated

| Scan set | Trigger union | Covered | **Asserted but not triggered** |
|---|---|---:|---:|
| The 444 declared union; triggers of the gates that **actually assert pins** (A/C same 10 paths, + D's 8) | A ∪ C ∪ D | 10 | **434 of 444** ← the honest figure |
| The 444 declared union; RF2's framing — both Lessons gates' triggers, ux2 globs expanded | A ∪ B | 22 | **422 of 444** |
| The 444 declared union; every gate's triggers regardless of what it asserts | A ∪ B ∪ C ∪ D | 26 | **418 of 444** |
| Lessons asserted set only (440); A ∪ B triggers | A ∪ B | 22 | **418 of 440** |
| **Bare single-gate, no glob expansion — do NOT report alone** | A only | 6 | 438 of 444 |

RF2's carried **422** reproduces exactly, and I have independently re-derived it (script `/tmp/claude-0/.../gates.py`). But it **credits gate B's globs with coverage gate B does not provide**: gate B asserts no pins, so a `data/**` change firing ux2-gates.yml fires nothing that reads a pin digest. On the measurement that matters for §2 — coverage by a gate that would actually go red on a stale pin — the figure is **434 of 444**.

### Characterising the 434 not-triggered (representative sample, not the full list)

Directory shape of the 418-figure set (the all-gate union; the 434-figure set is this plus `resources.json`, `subject.html`, the 10 `assets/catalogue/*` files, `data/calendar-spine.json`, `tools/ux2/resource_sizes.py`, `tools/ux2/s1m_published_input_proof.py`):

| Count | Directory |
|---:|---|
| 345 | `Science_Teesside/` (344 of them `Science_Teesside/Teaching_Packs/…`) |
| 35 | `tools/` |
| 27 | `Humanities_Teesside/` |
| 4 | `.github/workflows/` |
| 3 | `_glv3/tools/` |
| 2 | `primary/year5/science/autumn/forces/` |
| 1 | `_sx2/` |
| 1 | root (`humanities_teesside.html`) |
| **418** | |

**Representative sample (this is a sample, not the full 434):**
- `Science_Teesside/index.html`
- `Humanities_Teesside/index.html`
- `Humanities_Teesside/David_Cover_Autumn1_W3-W7/BH_W3.html`
- `humanities_teesside.html`
- `.github/workflows/glv3-verify.yml`
- `.github/workflows/watch-main.yml`
- `_glv3/tools/verify_change_boundary.py`
- `_sx2/DECISIONS.md`
- `primary/year5/science/autumn/forces/Y5_Forces_SoW_and_Plans.docx`
- `tools/catalogue/build_catalogue.py`
- `tools/science_teaching_packs/check_packs.py`
- `tools/humanities_resources/build_resources.py`
- **`resources.json`** — worth naming individually: a `MANIFEST_PINS` entry, asserted by gate A at `:1027-1034`, triggered on by gate B alone, and gate B asserts nothing. Edit `resources.json` and the gate that would catch a stale manifest pin does not fire at PR time.

### One mitigating fact, stated as a YAML READ not an observed run

Gates A (`cron '53 6 * * *'`, `:46-47`), B (`cron '23 5 * * *'`, `:50-53`) and C (`cron '9 7 * * *'`, `:51-52`) each carry a daily schedule, and A's job conditions (`:66`, `:211`) admit `push`/`workflow_dispatch` only — so on a scheduled run `static-contract` still executes and the full 440-path assertion runs. **This is a read of the YAML; I observed no run.** It does not close PIN1's finding: the schedule catches drift *within a day, post-merge*, on somebody else's clock — which is precisely §0.1's "surfaced later on somebody else's PR, where nobody has the context". Gate D has no schedule at all.

---

## §1.3 — Triggered but not asserted, classified

Every trigger path that matches none of the 444 asserted pins for that gate. 21 distinct patterns across the four gates. **Every one is DESIGN. No defect found in this direction.**

### Gate A — Lessons `mbm-cross-estate-unification.yml` (4 of 10 triggers)

| Path | file:line | Classification | Reason |
|---|---|---|---|
| `tools/verify_cross_estate_unification.py` | `:12`, `:25` | **DESIGN** | The checker itself. A checker edit must re-run the checker; it cannot pin its own bytes without recursion. Also in `ALLOWED_DIFF` (`:649` set). |
| `tools/verify_cross_estate_browser.mjs` | `:13`, `:26` | **DESIGN** | Executed by the `browser-matrix` job (`:106` `node --check`, `:162`, `:188`). It is gate code, deliberately kept off the digest pins and placed in `ALLOWED_DIFF` instead. |
| `docs/MBM_CROSS_ESTATE_UNIFICATION.md` | `:14`, `:27` | **DESIGN** | Documentation of this gate, in `ALLOWED_DIFF`. Triggering on it is conservative over-coverage, not a missing assertion. |
| `.github/workflows/mbm-cross-estate-unification.yml` | `:16`, `:29` | **DESIGN** | Self-trigger. It *is* asserted, structurally rather than by digest: `PUBLICATION_GATE_WORKFLOW_PATH` (`:637`) is read by `publication_trigger_errors` (`:847-886`), which requires this file's own `on:` block to name `education-pages.yml` exactly once under both `pull_request` and `push`. Not a digest pin, so it is correctly outside the 444. |

### Gate B — Lessons `ux2-gates.yml` (12 of 12 triggers)

All twelve are triggered-but-not-pin-asserted, because gate B asserts no pins at all. **All DESIGN** — they are genuinely asserted, by a *different subject*: catalogue schema (`:74-75`), unit-tag derivation (`:78-79`), companion-pack derivation (`:84-85`), spine and size-table derivations (`:95-96`), hub/subject Chromium limbs (`:117`), chip gate (`:126-127`), catalogue DOM (`:129`). Isolation by design, exactly as §1.3 anticipates.

Two of the twelve deserve naming because they are the ones that produced #499's misleading green:
- `tools/verify_cross_estate_unification.py` (`:31`, `:46`) — **DESIGN, but load-bearing for §2.** This trigger is why ux2-gates ran on #499. It caused a gate that asserts no pin to run on a checker edit, which is the appearance of pin coverage without the substance.
- `tools/catalogue/pin_catalogue_contract.py` (`:32`, `:47`) — **DESIGN.** Watches the re-pinning tool. No workflow in any of the four repos executes this tool, so this trigger buys a re-run of the row proofs only.

### Gate C — Apps `mbm-cross-estate-unification.yml` (5 of 10 triggers)

The same four as gate A, plus:

| Path | Classification | Reason |
|---|---|---|
| `index.html` | **DESIGN** | `catalogue_errors` returns `[]` for `kind != "lessons"` (`:797-798`), so Apps' `index.html` carries no digest pin. It is still read and structurally asserted by `run_checks` (`:978-1015`: sentinel, body classes, header, nav landmark, route order, duplicate IDs) and its wording is compared against `APPS_HUB_REVIEWED_WORDING_SHA256` (`:115`). Different assertion mechanism, not an absence. |

### Gate D — Apps `verify-lundyloop-professional-os.yml` (5 of 8 triggers)

| Path | file:line | Classification | Reason |
|---|---|---|---|
| `LundyLoop_Professional_OS.html` | `:7`, `:18` | **DESIGN** | The payload under test. Asserted by `tools/lundyloop/verify_lundyloop_static.py` (`:54`) and the live-bytes proof (`:118`), not by a digest pin. Explicitly *excluded* from the boundary allowlist — `self_test` at `:1204` asserts `boundary_errors({"LundyLoop_Professional_OS.html"}, kind)` is non-empty, i.e. the design is that this file is *not* silently permitted. |
| `LundyLoop_Professional_OS/**` | `:8`, `:19` | **DESIGN** | Same payload tree, same reasoning. |
| `_release-docs/lundyloop-professional-os-v2/**` | `:9`, `:20` | **DESIGN** | Release documentation for the package; asserted by the LundyLoop static verifier, not pinned. |
| `index.html` | `:11`, `:22` | **DESIGN** | As gate C. |
| `tools/verify_cross_estate_unification.py` | `:13`, `:24` | **DESIGN** | Checker self-trigger, as gate A. |

**Summary of §1.3: 21 triggered-but-not-asserted patterns, 0 defects, 21 design.** Three mechanisms account for all of them — (i) checker/gate self-triggering, which cannot be a pin without recursion; (ii) assertion by a different predicate (structural, derivational, or live-bytes) rather than by digest; (iii) conservative over-triggering on documentation. The asymmetry runs almost entirely the *other* way, and that direction is the defect.

---

## What §2 will have to reckon with (stated, not implemented)

Three facts from this census change §2.1's shape and are recorded here so the repair is not written against the order's stale premise:

1. **§2.1 says "derive each gate's trigger paths from the registry it asserts against." Gate B asserts against no registry.** There is nothing to derive for `ux2-gates.yml`. The honest options are to leave it alone (it is not a pin gate) or to make it one — a separate decision, not a derivation.
2. **The derivation target is gate A alone, and it is 434 paths wide** (or 440 including the 6 it already covers). A generated `paths:` list of that size is a real constraint on §2.2's "smallest honest alternative", and §2.3 forbids solving it with `**`.
3. **The Apps side does not need the repair.** Gates C and D between them already trigger on all 9 Apps-side pins, C via the canonical-asset and publisher paths and D via `tools/lundyloop/**`. Widening anything there would be noise.

A derivation precedent exists at `/home/user/mattroper1977.github.io/tools/derive_pin_dependents.py` (confirmed present; **not read, not run** — §2 is out of scope).

---

## Files and scripts

- Verifier under census: `/home/user/Lessons/tools/verify_cross_estate_unification.py`
- Gate A: `/home/user/Lessons/.github/workflows/mbm-cross-estate-unification.yml`
- Gate B: `/home/user/Lessons/.github/workflows/ux2-gates.yml`
- Gate B's only module-loading tool: `/home/user/Lessons/tools/ux2/prove_catalogue_gate.py`
- Gate C / D (API-only, not cloned): `MattRoper1977/Matt-s-Apps-` `.github/workflows/mbm-cross-estate-unification.yml`, `.github/workflows/verify-lundyloop-professional-os.yml` at `4cb8a634dbeaa3d98d7699252fdfff4253c47eef`
- Census scripts (scratchpad, reproducible): `/tmp/claude-0/-home-user-Lessons/05c13970-a6c0-53bf-90f1-2f5c998f17c1/scratchpad/census.py`, `gates.py`, `countpins.py`
- Derived data: `.../union_paths.json` (444), `.../catalogue_paths.json` (434), `.../uncovered.json` (418)

**PIN1 §1 complete. §2 and §3 NOT attempted.**