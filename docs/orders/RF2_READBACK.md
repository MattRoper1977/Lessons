# RF2 — reconciliation against the recovered scopes

Release/control session, 11–12 September 2026. Successor to RF1_PARTIAL.
Every figure below was measured in this session at the time stated, or is marked **not run**.
No figure is carried from RF1 or from an order's own text without re-measurement.

**Mains at RF2's census — all four UNCHANGED from RF1's 21:45–22:00 figures, re-measured
2026-09-11 23:51:36–23:54:34 UTC:**

| Repo | Commit | Tree | vs RF1 |
|---|---|---|---|
| mattroper1977.github.io | `1651b84c800f6cd3169a29f794b075042ee54024` | `e4c79831afbfc29c58cb9b62d650579a5a59f6ce` | unchanged |
| Lessons | `aad04718c11a2396ecf323a662f55bf0e0c2441b` | `fa21544faa79f3efea25f9d58e68dc8c8c1ec28c` | unchanged |
| Matt-s-Apps- | `4cb8a634dbeaa3d98d7699252fdfff4253c47eef` | `a07ef2b907377fbe50f914c632afb84314e5dfdf` | unchanged |
| Games | `809b6c9a65f175cd48182e793bee166ad4f6bd3f` | `3477eb8565ae0138ef1f741611f27891136d0595` | unchanged |

Check states also reproduce RF1 exactly: Site 12 success / 5 failure / 1 cancelled / 12 skipped
(30 runs); Lessons 26/26 success; Apps 9 success + 2 skipped; Games 21 failure + 4 success.
**RF1's census has not expired under P5.2.** Nothing drifted in the two hours between them.

Caller chain, read from the actual files rather than carried:

- Lessons `education-pages.yml:43` (`uses:`) and `:45` (`builder_ref:`) both pin Site
  `810ae8f8830dc9e30a7ceec9ada4ec24d575a04d`. The historical `2e49afdd` freeze appears **only**
  inside a comment at `:27`, never in an executable field.
- Apps pins Site `6430f23f5b226464d3d8faa5050ab93f7fe0e5` on both fields.
- Games `play-publication.json` carries site `47b7d895…`, lessons `2c33266b…`.

**One caller contradiction to carry forward.** The Site publication workflow *at the pinned SHA*
`810ae8f8` falls back to Lessons `6ae34c37`, while Site main's copy of the same file falls back to
`2c33266b`. The fallback is inert when Lessons is itself the caller, but not when Site or Apps
triggers it. Named here; not repaired by RF2.

---

## §0 What was recovered, and what it cost

Appendix B arrived twice and both copies are the same bytes:
**SHA-256 `bc46f34b1ce7473364d3cfca8be34b002b36cb6b1eeb45cdc18d1f88bef08ed1`, 31,695 bytes.**
Matt's upload is byte-for-byte identical to the copy already committed on draft Site **#351**
(`docs/orders/2026-09-10-recovered-original-orders.md`, branch `codex/rf1-recovered-orders`,
head `4d98f4540ebc4dad8cc4632bf2d8b11e95295a79`, created 2026-09-11T22:13:59Z).

That creation time is *after* RF1's census closed, which is why RF1's appendix lists six open Site
PRs where RF2 §4.1 says seven. **#351 is the seventh.** (RF2 §4 gives #351 as created 22:36Z; the
API `created_at` is 22:13:59Z and 22:36:49Z is its `updated_at`. Measured value reported.)

**§0.3 — both PR pairs are real and distinct, confirmed live:**

| Reference | Title | State |
|---|---|---|
| Games #78 | Pin release: site `47b7d895b7` → `85e3e02059` | open, `mergeable_state: blocked`, head `d9b70dbc` |
| Games #79 | Pin release: lessons `2c33266b01` → `aad04718c1` | open, `mergeable_state: blocked`, head `38bb4d96` |
| Apps #78 | S1-F: mirror three catalogue guards from Lessons #506 | closed, **not merged**, 2026-09-11T10:06:18Z |
| Apps #79 | S1-I: mirror the reviewed combined-admission caller | closed, **merged** 2026-09-11T09:47:43Z |

Worth recording for the audit trail: master-order **v1 §4.5 said "Games #78/#79" and was correct**;
**v2 §1.3's "correction" to Apps was itself the error**; RF2 §0.3 corrects the correction. Both
pairs exist; neither replaces the other.

---

## §2 ML1 — CLOSED-BY-DL, residue answered, one documentary stop

**State: CLOSED-BY-DL with named residue. Owner: release/control.**

### §2.1 — the repair was already landed, and RF1 was right not to replay it

Confirmed. ML1 §1.4 is the clause that produced RF1's stop, and it is recorded as correct.

### §2.2 — #191, #192, #194: all three MERGED, verified independently

Not from the recovery index's word — re-verified against the API, and every merge commit confirmed
to exist:

| PR | Disposition | Merge commit | Merged |
|---|---|---|---|
| Site #191 | **MERGED** | `f41a9e32a9cc82ac759367e111bf2266a14d6208` | 26 August 2026 |
| Site #192 | **MERGED** | `72c31ba5d9077623b912137ff4439bb2fbce70cb` | 27 August 2026 |
| Site #194 | **MERGED** | `ed0a1ba32ea994558100c4695fb2880fcda4c2b1` | 27 August 2026 |

No renumbering, no closed-unmerged. They are absent from RF1's open-PR census because they merged
a fortnight before it.

ML1 §4.3's four pickup conditions on #191, measured rather than assumed:

| Condition | Result |
|---|---|
| Delta cap post-merge | **Satisfied** — re-measured 549→549, 0 gained, denominator 717 |
| Mirror clean by **two** instruments | **1 of 2** — shelf-mirror-guard on main at `f41a9e32` (run 33024174661, success) independently verified; the second is a record claim, **not re-run** |
| routes-serve-200 | **SKIPPED** on the PR head, SUCCESS post-merge on main. The record's claim is about main and is correct — but a skip on the PR is not a pass |
| "R4 line present once" | **Not establishable.** The lift-close record asserts it (`MBM_DEADLOCK_LIFT_CLOSE.md:159`), but the R4 line's *text* is defined in none of Appendix B §B1, `MBM_LIVE_MIRROR_LEG_DEADLOCK.md` or `MBM_DEADLOCK_LIFT_CLOSE.md`; the literal token `R4` appears in 0 of the 7 `for/*/index.html` pages at main. Without the sentence text it cannot be counted |

### §2.3 — MAIN STILL REDS ON REAL DRIFT: confirmed. **No stop.**

The check has **not** gone quiet, and this was the assertion RF2 §2.3 called live.

- The check is `.github/workflows/shelf-mirror-guard.yml`, workflow "Shelf mirror is not stale",
  job `mirror` (`:58`), step "Mirror is byte-identical to the canonical" (`:86`). The assertion,
  verbatim at `:88-90`, runs `tools/render_games_manifest_mirror.py --canonical … --check`.
- It **fired on push to main and went RED on real drift** on 3 September — run **33713403941**,
  STALE mirror 33,722 B vs canonical 33,110 B, exit 1. Its most recent main run is green and
  genuinely executing.
- It produces no record at `1651b84c` because that commit touches none of its three filtered paths
  (`:31-33`). That is **"no run created by a path filter"** — not a skipped check, and not a
  demotion. The distinction matters: a skip would be exactly the demotion ML1 §2.3 warns about.
- The second instrument closed the remaining doubt by a different route: the site mirror at
  `1651b84c` and `Games/main:games.json` are the **same git blob**
  (`2bb7ded7062f68d94ddcf7c34ec0bbbf5d9bc542`, 34,095 B), so there is demonstrably no committed
  drift at the current head for the check to red on. That turns "the check is quiet" from a
  suspicion into a measured non-event. Caveat as stated: this is the committed canonical, not the
  served bytes.
- `agx1-live-verify.yml` — the leg ML1's patch targets — has **no push-to-main trigger at all, by
  original design** (`:17-24`; the `:13-16` comment names the PR as the carrier). It is firing
  green on PRs today. The two legs must not be conflated.
- ML1 §2.4's tightenings are all present in the shipped file, and nothing carries `continue-on-error`.

### The one ML1 §5 STOP that is triggered — and why it is documentary

**"The documented patch no longer applies": TRIGGERED**, independently confirmed by six instruments.

`docs/MBM_LIVE_MIRROR_LEG_DEADLOCK.md:158-244` ("The patch, verbatim") fails a read-only
application check at Site main under `git apply --check`, `--recount`, `--recount -C1` and
`patch --dry-run -p1 --forward` (Hunk #1 FAILED at 255). The pre-image it searches for is absent
from the entire workflow tree — `grep 'PASS mirror is byte-identical' .github/workflows/` returns
0 hits across 57 files.

The second instrument found it fails for **two independent reasons**, where the first lane reported
only one: the recorded patch is also **malformed** — plain `git apply --check` exits **128** with
`corrupt patch at line 84`, because the hunk header says `@@ -255,15 +255,72 @@` while the body
carries old=14 / new=71. It is one context line short, almost certainly a whitespace-only trailing
line stripped by markdown. So it is unapplicable *before* it is ever compared to the file.

**This is a stale artefact, not a silent adaptation.** The same document's later section
"# APPLIED — ORDER DL, 2026-08-26" (`:395`) states in its own first paragraph that what landed
"is not byte-for-byte the patch recorded above", explains why the recorded patch fails its control
C4, and documents the three-operand design that did land.

**Residue, and the exact next action:** the "The patch, verbatim" heading at `:158` carries **no
superseded marker**. Any future pass running ML1 §1.4 literally will stop at precisely this point,
as this one did. The fix is one line of documentation — mark the section superseded by the APPLIED
section below it — and it belongs to whoever owns that document, under its own transaction.

### §2.4 verdict

**ML1 is CLOSED-BY-DL.** Its substance (§2.1–§2.4) is satisfied by the landed DL repair; §4.2's
residue is answered — all three PRs merged; §2.3 is confirmed live and reds on real drift. RF2 does
not emit `ML1_CLOSED` (it is not running ML1), but records that the order's requirements are met
except for three named items: the unmarked stale patch section, the unestablishable "R4 line", and
the second mirror instrument not re-run.

**Lessons open-PR census, re-measured 2026-09-12 00:31 UTC — 8 open, every head unchanged from RF1:**

| PR | Head | Title |
|---|---|---|
| #497 | `049cb29c` | TH1 A4 + A5: the .sb3 rule as an open item |
| #493 | `c460eada` | GC1 P2–P5: GROW Computing placed (164 files) |
| #465 | `7fc4e74a` | SX2R: a media census, and the correction it forced |
| #456 | `c4e23905` | SW2 T5 + SW2-F R2 — **held** |
| #118 | `1bcbdfe7` | [PARKED — DO NOT MERGE, RULED] Class of Ashes |
| #116 | `4a53d066` | [REFERENCE DIFF — DO NOT MERGE] Chemistry Lab v0.3 |
| #45 | `0c0f0487` | HELD — Pass SEMH-2 claims-accuracy tail |
| #43 | `f50b7207` | HELD on print check · tk1-access-2 |

The P5.2 shelf-life check therefore holds on **both** repositories, not just Site.
---

## §3 PRX1 — #350 audited clause by clause against the recovered §B2

**State: IN PROGRESS, release HELD. Owner: release/control.**
#350 is still open, still **draft**, head still `3c11780acc391a598f1cd486206d167a8b804ad9`,
5 success + 1 skipped, and **all four required contexts green** — read live from the repository
ruleset (`/rules/branches/main`, ruleset_id 21475918), not assumed.

### First, §0.5's three carried numbers — re-measured, as §0.5 itself demands

§0.5 says: *"Re-measure all three numbers; do not carry them."* Done, at Site main `1651b84c`,
denominator **91 tracked `.html` files**, by two independent instruments using different tokenizers
(one `html.parser`, one a hand-written character-level lexer). They agree on every figure.

| §0.5's carried claim | Re-measured | Verdict |
|---|---|---|
| "9 Site pages carry more than one `</header>`" | **9/91 by raw grep** — reproduced exactly. **6/91 by tokenizer** (3 pages' literals sit inside `<script>` strings). **NESTED: 0/91** | confirmed, with the grep/tokenizer distinction added |
| "none are in shared_navigation's curated list" | **0 of 9 at static source** — confirmed. **But see the build-stage finding below** | confirmed at source, incomplete as a statement |
| "0 of 7 audience_discovery targets carry more than one `</main>`" | **The denominator is wrong: the target set is 5, not 7.** The answer is **0 under either denominator** | number right, denominator wrong |

`</main>`: **4/91 by raw grep, 2/91 by tokenizer, NESTED 0/91.** Every multi-occurrence page is
strictly alternating OPEN/CLOSE at depth 1 — **siblings, not nesting** — verified with depth
tracking and printed line by line.

**PRX1 §5's `<main>` stop: NOT TRIGGERED** — on the nesting reading, which is the reading §1.2's own
sentence supports ("Nested `<main>` is invalid HTML so the expected answer is zero").

> **One ambiguity I am not going to resolve on your behalf.** §5 words the stop as *"the nesting
> census returns a non-zero for `<main>`"*, while §1.2 words the census as *"pages with >1
> `</main>`"*. Those are different questions and they give different answers here: **0** nested,
> but **2** pages with more than one `</main>` (`neonturf/index.html`, `touchline/index.html`).
> I have adopted the nesting reading, so no stop. **If you intended the literal §1.2 reading, the
> stop fires and PRX1's urgency changes.** Neither of those two pages is in either publisher target
> set, so the practical risk is nil either way — but the wording should be settled before PRX1 closes.

**A finding the static census cannot see, and both instruments found independently.**
`audience_discovery.py:179` injects a second `<header class="ad-heading">` *inside* the new `<main>`
on all 5 targets, and `build_education.py` runs `audience_discovery` (line 322) **before**
`shared_navigation` (line 326). So **at the moment the header regex actually executes, 5 of 5 of
those curated pages carry two `</header>`.** They are siblings, not nested, and the lazy regex still
matches the correct balanced outer header — **the defect stays latent** — but **the intersection is
non-empty at the build stage**, which is not what §0.5's "none are in the curated list" implies.
That sentence is true of the source tree and false of the tree the publisher actually operates on.

### The clause-by-clause table

| Clause | Requirement | Verdict | Evidence |
|---|---|---|---|
| **§1.1** | Re-derive curated list and target set at current main; report both with counts | **not satisfied** (not in the PR) | Measured here: **28 header targets**, **5 main targets**. `shared_navigation.py:177-181` branch split; `/asdan/`, `/uas/` and the conditional pack hub take the `<body>` branch and are **not** header targets. Confirmed twice: static re-derivation, and a live `refresh()` returning 31 routes − 3 = 28 |
| **§1.2** | Nesting census both ways | **not satisfied** (not in the PR) | Measured here — see table above. Both numbers, both methods, denominator 91 |
| **§1.3** | Repo-wide census of the same shape, file+line, classified writing vs measuring | **not satisfied** (not in the PR) | Measured here — **137 hits: 42 WRITING, 95 MEASURING** over 486 tracked files. **Not RF1's carried 133**; the count is not bent to match |
| **§2.1** | Both call sites replaced by a balanced walk that raises rather than truncates | **satisfied (2/2)** | `structural_html.replace_first_element` via `HTMLParser`; `shared_navigation.py:181` and `audience_discovery.py:232` both converted |
| **§2.2** | Keep the count assertion **and add a balance assertion** across the replaced region | **PARTIAL** | Count assertion kept at **both** sites (`if count != 1`, `if replaced != 1`). **No balance assertion exists** — balance is only *implied* by the tokenizer refusing a nested target tag. Measured straddle case: `'<div><header></div></header>'` **eats a non-target close tag and leaves `<div>` unclosed with no raise** |
| **§2.3** | Mechanism repair only; byte-identical output on every current input expected | **satisfied** — decided by §3.1 below | Four input shapes measured where old and new **differ**: uppercase start tag, whitespace inside the close tag, a decoy inside an HTML comment, a decoy inside `<script>`. The old regex has **no `re.I`**, so it does not match `<HEADER>`; the tokenizer does |
| **§3.1** | Golden test over every page in both target sets, byte-identical, count with denominator | **SATISFIED — 33/33 byte-identical** (see below) | RF1's 31 covered 24/28 header + 5/5 main (+2 pages that are **not** in the production target set). No per-page record of the 31 exists anywhere |
| **§3.2** | Planted nested `<header>`: repaired raises, old truncates — show both outputs | **satisfied** | `test_nested_fault_defeats_old_count_guard`; both outputs shown — old truncates with `count==1`, new raises `Nested <header> replacement is unsupported` |
| **§3.3** | Planted nested `<main>`: same | **satisfied** | Same test, `for tag in ('header','main')` |
| **§3.4** | Structural assertion: ask the **DOM** whether a should-be sibling became a **descendant** | **NOT SATISFIED** | **0 of 8 tests ask any DOM/parse-tree question.** All 8 assert on strings; the test file imports no parser |
| **§3.5** | Each plant asserts its own mutation landed before asserting the failure | **PARTIAL** | 4 of 8 tests are failure-asserting plants; **only 1 of those 4** asserts its own mutation landed. Also `test_unsafe_or_absent_boundaries` uses a bare `assertRaises` with no message regex, so it would pass on a `ValueError` raised for the *wrong reason* |
| **§4.1** | One PR, both call sites, **plus a DECISIONS entry naming the mechanism and the three census numbers** | **NOT SATISFIED** | Both call sites present; **no DECISIONS entry exists in the PR** |
| **§4.2** | The §1.3 census lands as a finding **in the same PR, unfixed** | **NOT SATISFIED** | Not in the PR. The census is measured (137) and ready to land |
| **§4.3** | Published output unchanged, proved by §3.1 | **follows §3.1** | — |

The suite itself runs clean: **8 tests, 8 pass, 0 fail/error/skip**. But it is wired into
**0 of 58 workflow files** — nothing in CI runs these controls, so they protect the next change only
if someone remembers to run them by hand.

### §3.4 — the control is producible, and it carries a subtlety worth keeping

I built the missing DOM control and ran it. **It fires on both planted cases.** But the *literal*
§3.4 question — "has an element that should be a sibling become a descendant?" — measures **False**,
because with well-formed input this fault does the **opposite**: the truncation leaves the outer
element unclosed, and the parser's repair **promotes what should be descendants into siblings**.

That is not a reason to skip §3.4. It is a reason to word the assertion as the *tree relationship
changed* rather than as one specific direction of change — otherwise the control, written literally,
would be a plant that cannot fire, which is exactly what §3.5 warns against. One operational note
for whoever lands it: my control uses `lxml`, and the professional-site-design-audit job installs no
`lxml`, so a landed control should use the standard library or declare the dependency.

### §1.3 — the repo-wide census, ready to land under §4.2

Scan set: **486 tracked files** at Site main `1651b84c` (424 py/js/mjs/cjs/ts/sh + 62 yml/yaml).
**137 in-shape hits: 42 WRITING, 95 MEASURING.** Five further raw matches in `uas/vendor/jspdf` and
`uas/vendor/pdfjs` were excluded as vendored third-party libraries, not repo extraction/injection
steps.

**This is not RF1's carried 133, and I am not bending it to fit.** The scan set and method are
stated so the +4 is explainable; RF1's own scan set and inclusion rules are recorded nowhere I can
read, so the difference is **not attributable** rather than reconciled.

Only writers are in PRX1's scope. **Two are genuine second instances of the #345 defect class in the
publication path, and both are LATENT at current main:**

| Writer | Shape | Why latent today |
|---|---|---|
| `domain-split/education_discovery.py:161` | `text.index('</div>', start)` after a `<div class="toolbar"` anchor — **`<div>` nests freely** | measured against the Apps `index.html` blob `58619f70`: the toolbar currently contains no nested `div`, so first-match is currently correct |
| `domain-split/build_publications.py:156` | `preview.find('</main>', start)` / `find('<section class="view', start+20)` bounding the published page body | measured 5 `<section class="view"` and 1 `</main>` in `domain-split/preview.html`; no nesting today |

Three further writers are the same shape at lower risk: `build_publications.py:212` (first of two
`<style>` in preview.html), `render_audience_homepages.py:858` (lazy `</article>`), and
`tools/stamp_chrome.py:98` (lazy `</button>` — **referenced by no workflow**, so whether it ever
runs against published bytes is not measurable from this repo alone).

The two named in PRX1 §0.1/§0.2 are included in the 42 and are the known defect, not new findings.

Per §4.2 these land **as a finding, unfixed**. Each of the two publication-path writers deserves its
own order; neither is PRX1's to repair.

### §3.1 — THE GOLDEN TEST: RUN, AND IT PASSES

**33 of 33 byte-identical. 28/28 header targets, 5/5 `<main>` targets. Zero differences.**
**PRX1 §5's "Any golden test differs" is NOT TRIGGERED.**

RF1 reported 31 pages with four "unavailable" and no per-page record. That gap is now closed: the
four build-generated pages (`owner/stats`, `stats/on-this-device`, `commission`,
`for/governors-trustees`) **were generated locally** — `usage_discovery.refresh` for the first two,
`build_publications.py` for `commission`, `governors_discovery.refresh` for the last — and the
Matt-s-Apps- blocker dissolved: `shared_navigation.refresh` needs exactly **one** Apps file, obtained
through the sanctioned API route and verified byte-exact against blob SHA
`58619f70967ba3d6217b6d31571d2c91191da535`, with **no clone**.

The comparison is stronger than §3.1 requires: `diff -rq` over the **entire** post-run output trees
(`education-site`, `education-lessons`, `education-apps` — every file, not only the 33 targets)
reports no difference at all. Both versions received byte-identical inputs, `diff -r`-verified before
each run, so the only variable was old-regex versus candidate-tokenizer.

**This is not a formality pass, and that distinction is the point.** The four divergent shapes are
real; they simply have no current carrier. A census run *first and independently* of the byte
comparison found **zero** target pages carrying any of them:

| Shape | Target pages carrying it |
|---|---|
| (1) uppercase/mixed-case start tag `<HEADER …>` | **0 of 33** |
| (2) whitespace inside the closing tag `</header   >` | **0 of 33** |
| (3) `<header>`/`<main>` literal inside an HTML comment | **0 of 33** |
| (4) `<header>`/`<main>` literal inside `<script>`/`<style>` | **0 of 33** |

And the divergence was **proved to fire**, with each plant asserting its own mutation landed first,
per §3.5 — so the pass is distinguishable from a test that cannot fail:

- **Shape (1), header leg.** Uppercased the `<header>`/`</header>` pair on `/members/`.
  **OLD raised** `Missing navigation insertion/replacement boundary` — the lazy regex carries no
  `re.I`, matched nothing, `count == 0`. **NEW completed all 31 routes normally.** A hard,
  observable divergence.
- **Shape (3), `<main>` leg.** Planted `<!-- <main>ghost</main> -->` immediately before the real
  `<main>` on `/for/partners/`. **OLD matched the commented pair and replaced the comment**, leaving
  the real `<main>` in place — which then tripped audience_discovery's own link-preservation guard.
  **NEW skipped the comment and replaced the real `<main>`.**

The census script itself was certified against five synthetic plants (one per shape plus a nested
control) and flagged all four shapes and the nesting.

### A correction to my own §0.5 finding above — the curated list is *not* free of multi-`</header>` pages

The static census (91 files at source) found the intersection empty, and reported a build-stage
finding of 5 affected pages. **The golden test, running against the bytes `shared_navigation`
actually receives, found SIX** — and the sixth is new:

| Target page | `</header>` count in the bytes the function receives | Why |
|---|---:|---|
| `/for/parents-carers/`, `/for/schools-semh/`, `/for/trusts/`, `/for/councils-organisations/`, `/for/partners/` | 2 each | `audience_discovery`'s generated `<main>` contains a `<header class="ad-heading">` |
| **`/Lessons/primary/`** | **7** | `primary_discovery` renders one `<header class="primary-header">` plus **six** `<header class="primary-unit-head">` unit cards |

Nesting depth was measured on each: **max depth 1 on all six — siblings, not nested.** Old lazy stop
and new tokenizer both select open@first → close@first-close and agree byte-for-byte. So the defect
remains **latent**.

But PRX1 §0.5's sentence — *"9 Site pages carry more than one `</header>`, none are in
shared_navigation's curated list"* — **is wrong at current main**, and wrong in the direction that
matters. Six of the twenty-eight curated pages carry more than one, one of them seven. That is
materially closer to live than §0.5 implies, and it is exactly the condition §0.5 predicts will go
live "the moment SW2 extends that list". Anyone extending the curated list should treat this as the
standing warning it now is.

### Fidelity limits on the golden test, stated rather than buried

Two generators were **not run**: `education_discovery.refresh` (needs the real Apps catalogue at
`output/education-apps/apps.json`, which cannot exist without cloning Matt-s-Apps-) and
`education_expansion.refresh` (depends on the former's outputs). In production these mutate
`/resources/`, `/tools/`, `/Matt-s-Apps-/` and the eight `/for/` pages before navigation runs —
`education_expansion` via an lxml re-serialisation that reflows bytes. Those pages were therefore
compared on pre-generator bytes.

**Mitigation, measured rather than assumed:** a repo-wide grep over `domain-split/*.py,*.js,*.html`
found **zero** non-lowercase `<header`/`<main` literals and **zero** whitespace-padded closing tags
in any generator. `education_discovery` emits only two `</header>`; `education_expansion` emits none.
Neither can introduce shape (1), (2), (3) or (4), and an lxml re-serialisation cannot either — lxml
emits lowercase tags with no internal whitespace. So the untested delta cannot carry a divergent
shape. That is an argument from measurement, not from confidence, and it is offered as exactly that.

**Net effect on the clause table:** §3.1 moves to **satisfied** with the fidelity limit named, and
§2.3's "byte-identical output on every current input" **holds**. §2.2, §3.4, §4.1 and §4.2 are
unchanged and still unsatisfied.

### Second instrument on the golden test — agrees, by a different route

ML1 §3.6: *"A single green from the check you just changed is not evidence about the check you just
changed. Two instruments."* The second instrument did **not** rebuild-and-diff. It applied each
version's replacement operation to the **same captured call-site bytes** and compared on three axes
at once:

1. **the chosen byte span** — the `(start, end)` region each version selects. **Identical on all 33.**
   This is the strongest of the three: two versions selecting the same span cannot differ for *any*
   replacement string, so the result does not depend on the replacement text happening to match.
2. **sha256 of the returned document** using the real replacement the live publisher passes.
   **Identical on all 33.**
3. **sha256 using a fixed sentinel replacement** in place of the real one — a replacement-independent
   probe. **Identical on all 33.**

Returned `count` was 1 from both versions on all 33; neither raised on any target. It then ran the
wholesale route as its own tie-breaker: two pristine builds, `diff -rq` over **4,270 files each**.
The only differing file is `domain-split/output/build-report.json`, and the only difference inside it
is the recorded provenance SHA — `git rev-parse HEAD` of two freshly-initialised scratch repos, not
content the candidate produced. **Both routes agree.**

It also **independently reproduced the six-page §0.5 correction** and the 5-not-7 denominator, and
certified its own harness with **ten plants** into real captured inputs — including a control on
unmutated `/members/` proving the harness does **not** report divergence where there is none, and
shapes (2) and (4) which the first instrument did not plant. Shape (2): `</header   >` — OLD
`count=0` (it requires the literal `</header>`), NEW `count=1` (its closing match is
`</tag[ \t\n\r\f]*>` with `re.I`). Shape (4): a `<header>` literal inside a `<script>` string — OLD
replaced **inside the script text**, NEW skipped CDATA and replaced the real header.

Three limits it stated rather than buried, all inert:

- The three `<body>`-insertion routes were deliberately not compared for header replacement — they
  do not take that branch, and `shared_navigation.py:182` is byte-identical in both versions. They
  were still identical in the full-tree diff.
- Apps input is two API-fetched, hash-verified files rather than a clone, so `education-apps` carries
  3 files instead of ~105. No target page is affected; the discrepancy is identical under both
  versions; and `education-apps/index.html` — the only Apps header target — matches an admitted
  reviewed digest exactly.
- Its Lessons basis was `0ca690bd` (main plus this session's own census commit) rather than
  `aad04718`. **Proven inert:** that file appears nowhere in the 4,270-file output and is referenced
  by no target input. The clone was not reset because this order is read-only on the repos.
---

## §4 BL1 — inventory complete, sequence proposed, nothing executed

**State: READY (inventory done, sequence proposed, awaiting Matt's approval for §3).
Owner: release/control.** BL1 §1 is read-only and was executed read-only: every GitHub call a GET,
zero mutations.

### §4.2 — is the PREREQ met?

BL1's PREREQ is "ML1 closed and #191/#192/#194 resolved". **Stated plainly: yes, in substance.**

- #191/#192/#194 — all three **merged and verified** (§2.2 above). Resolved.
- ML1 — **CLOSED-BY-DL**. The repair landed, and §2.3 confirms main still reds on real drift. The
  one triggered stop is a stale *document*, not a defect in the repair.

The honest qualification: BL1 §0.1 exists precisely to stop anyone accepting a carried claim, so
the prereq is recorded as met **on this session's measurements**, not on the recovery index's word.

### §4.1 — audit of RF1's inventory against BL1 §1.1–§1.5

RF1 produced "seven open Site PRs, no file overlaps, 12 exact-head failing records" without BL1's
text. Audited against the recovered clauses:

| BL1 clause | RF1 | RF2 measurement | Verdict |
|---|---|---|---|
| §1.1 open PRs | 7 | **7 confirmed** (#351, #350, #346, #291, #109, #106, #91) | correct |
| §1.2 failing exact-head sum | 12 | **12 confirmed**, twice by separate transports | correct |
| §1.3 overlap matrix | "no file overlaps" | **produced** — 21 of 21 pairs empty | **was missing as a matrix** |
| §1.4 AUTHORED/DERIVED | not produced | **produced** — vacuously satisfied | **was missing** |
| §1.5 per-PR classification | not produced | **produced** — 3 / 1 / 3 | **was missing** |

So RF1's three numbers were right; its three *required outputs* — the matrix, the classification and
the per-PR state — were absent. Those are supplied below.

### §1.2 — the two quantities BL1 insists must never be conflated

```
SUM ACROSS PRs of failing exact-head checks:
  0 (#351) + 0 (#350) + 0 (#346) + 1 (#291) + 2 (#109) + 2 (#106) + 7 (#91) = 12
  denominator: 45 exact-head check runs (5+6+5+6+3+4+16)

REDS ON SITE MAIN at 1651b84c (a DIFFERENT quantity):
  5 failing + 1 cancelled, out of 30 check runs
```

**5 ≠ 12**, and they are disjoint sets over different commits. BL1 §1.2's warning holds exactly.

One granularity trap the second instrument surfaced, worth pinning: **12 is the failing
check-RUN count; at check-SUITE granularity it is 11**, because #91's "Static gates" and "Gates are
proven red, not just green" are two runs inside one suite (run 34471015949). Anyone re-deriving
RF1's 12 at workflow granularity will get 11 and wrongly conclude the figure has moved.

Also recorded per BL1's own discipline: **5 skipped records** across the 45 (on #351, #350, #346,
#291, #91). A skip is an absence of evidence — LP1 §0.2's exact point — and must not be read as
green when sequencing.

Concentration: 7 of the 12 sit on #91 alone; 11 of the 12 sit on the three Aug-2026 estate-audit
PRs plus #291. The three PRs with current or near-current bases (#351, #350, #346) contribute **0**.

### §1.3 — THE OVERLAP MATRIX

Complete changed-file lists fetched with explicit pagination, not from PR bodies; each count equals
the PR object's own `changed_files`. 28 file-entries over 28 distinct paths.

```
        351  350  346  291  109  106   91
 351      -    0    0    0    0    0    0
 350           -    0    0    0    0    0
 346                -    0    0    0    0
 291                     -    0    0    0
 109                          -    0    0
 106                               -    0
  91                                    -
```

**21 of 21 pairs empty. Zero collisions.**

BL1's three named derived-surface collision candidates:

| candidate | open PRs touching it |
|---|---|
| `mbm-search-index.json` | **0 of 7** |
| `sitemap.xml` | **0 of 7** |
| `hud-coverage.json` | **0 of 7** |

This is the single most useful thing the matrix says. BL1's premise — "three arcs ordered in
isolation all contend" on these derived surfaces — **was true of the 29 August eleven-PR picture and
is not true of the current seven-PR picture.** The contending PRs have left the open set. Acting on
the remembered collision would have been acting on a picture that no longer exists, which is
precisely what BL1 §0.1 was written to prevent.

Near-misses, named so the empty result is not mistaken for a failure to look: #106, #109, #291 and
#91 all add files under `.github/workflows/` and `tools/`, but no filename is shared — four distinct
workflow files, eleven distinct tool files. #346 (`docs/SW2_LEDGER.md`) and #351 (`docs/orders/…`)
are both under `docs/` but in disjoint paths.

### §1.4 — AUTHORED / DERIVED

**Criterion:** DERIVED if a builder/generator/publisher in the repo writes it from other inputs, so
that regenerating after a merge reproduces it and a conflict is resolvable by re-running the
generator. AUTHORED if a human or agent wrote the bytes and no generator can reconstruct them.

**Result: vacuously satisfied.** The overlap set is empty, so there are 0 AUTHORED overlaps and
0 DERIVED overlaps. BL1 §4's stop condition "an overlapping file classifies AUTHORED" **cannot fire**.

For completeness over the whole 28-path set (not required): **28/28 AUTHORED, 0/28 DERIVED**. No
open PR carries a single derived artefact.

**Caveat, so this is not over-read:** file-level independence is not semantic independence. #350
rewrites the exact mechanism #346's ledger note documents. They share no file, so their merging
cannot conflict — but their *ordering* still carries meaning. Freedom here is freedom from textual
conflict only.

### §1.5 — per-PR classification (required output, not optional)

| PR | Classification | Basis |
|---|---|---|
| **#351** | understood, one measurement from done | base IS current main (0 behind), clean, 0 of 5 failing, 2 docs files, publication exclusion measured before writing |
| **#350** | understood, one measurement from done | base IS current main, clean, 0 of 6 failing; body enumerates what is *still required* — that precision is the signature of "understood" |
| **#346** | understood, one measurement from done | 1 markdown file, clean, 0 of 5 failing; base 35 behind but the file is untouched by those 35 commits |
| **#291** | **half-understood** | titled HELD, `unstable`, 1 of 6 failing, base 272 behind. Its body is candid: the pinch-zoom positive control cannot be made to fire in any available browser. The mechanism is understood; whether it can be measured at all is not |
| **#109** | **stale beyond recovery** | base **921 commits** behind, `blocked`, 2 of 3 failing, 33 days. Body: "Verification-only draft PR. **Do not merge.**" |
| **#106** | **stale beyond recovery** | base **922 commits** behind — the oldest in the set, `blocked`, 2 of 4 failing, 34 days. Body: the workflow "is disposable and will be removed" |
| **#91** | **stale beyond recovery** | base 35 behind, but 50 commits / 3,082 additions and **7 of 16** failing, 35 days; its own body concedes the audit "is intentionally expected to report red until its P0/P1 findings are triaged" — a triage that has not happened in 35 days |

**Tally: 3 understood / 1 half-understood / 3 stale beyond recovery = 7 of 7.** The split falls
exactly along base currency. Stale base and stale PR are the same fact measured two ways.

An important qualification on #350: "one measurement from done" is a **state** classification, not a
merge recommendation. Its own body says "Do not merge or auto-merge", and its outstanding PRX1 §3
evidence is considerably more than one measurement of work. It is classified understood because
nothing about it is unknown — not because it is nearly landable.

### §4.3 — PROPOSED sequence. Not executed.

BL1 §2 proposes; §3 merges only the portion Matt approves. **Nothing was merged. This is a handback.**

| Position | PR | Reason for this position |
|---|---|---|
| 1 | **#351** | Docs-only, publication-excluded by measurement against **both** builders (`810ae8f8` and `1651b84c`: `public_file('docs/orders/…') → False`). Base is current main, 0 reds, 0 overlaps. It is the only PR that makes *other* orders executable, and it cannot move published bytes. It also discharges Appendix B's own standing action and UX1-A §0.1 |
| 2 | **#346** | One markdown file, clean, 0 reds, `docs/` excluded. Lands the #345 warning for anyone stamping chrome while the PRX1 fix is still pending, and removes a stale-base PR from the set at zero risk |
| 3 | **#350** | **Conditional, not scheduled.** Only after its PRX1 §3 evidence is complete (see §3 below). It changes publisher code and must never precede its own golden test |
| — | **#291** | Do not sequence. HELD, and it gates nothing. Leave open; its finding is live and valuable |
| — | **#91, #106, #109** | **Propose closing unmerged**, per BL1 §4. #109 and #106 say "do not merge" / "disposable" in their own bodies; #91 needs a new audit against current main, which is a new audit, not a rebase |

**Swap line:** positions 1 and 2 are interchangeable. Both are docs-only with empty overlap and no
reds; the only argument for #351 first is that it makes the other recovered orders readable from the
repository rather than from a transcript. If Matt prefers #346 first, nothing measured here objects.

**BL1 §2.5 restated correctly:** no individual PR's failing-check count may rise, and no new failure
may appear on main. Whether merging any PR would clear or worsen the 5 reds on main is **not run** —
that needs post-merge re-measurement under §3.2 and is outside §1's read-only scope.

**BL1 §4's fourth stop condition is ARMED** for #91, #106 and #109 — "a stale PR would need rebasing
to be understood — propose closing it unmerged instead". Naming it is §1's job; the disposition is Matt's.
---

## §5 LP1 / PIN1 / SB1 — handoff. Not started, not run.

**RF2 §5.1: this session does not run these orders.** What follows is the recovered scope plus every
measured input, so the receiving owner starts from measurements rather than from carried figures.

### LP1 — PR-time mode for every live proof

**State: NOT VERIFIED / MISSING implementation. Owner: LP1/PIN1 owner, own session. PREREQ: ML1
closed — now met (§4.2).**

RF2 §5.2's named anchors, confirmed **exactly**:

| Anchor | Result |
|---|---|
| `fieldops-p2-and-sweep.yml:359` publication artifact recovery, condition `:360` | **confirmed verbatim**, condition is `github.event_name != 'pull_request'` |
| same file `:370` live comparison, condition `:371` | **confirmed verbatim**, same condition |
| Lessons #456 evidence that both actually skip | confirmed — #456 head carries 14 success + **2 skipped** + 0 failure |
| `|| echo` clone fallbacks | **3 of them, at lines 306–308** — RF1 said "303–307"; measured value reported |
| `prepare_served_publications.py:231` `per_page=30`, unpaginated | **confirmed present** |

**LP1 §1.1's carried 13 is CLOSE BUT NOT CONFIRMED — I measure 14.**

| Repo | LP1 carried | RF2 measured |
|---|---:|---:|
| Site | 6 | **7** |
| Lessons | 3 | 3 |
| Apps | 2 | **3** |
| Games | 1 | 1 |
| **Total** | **13** | **14** |

**Superseded within the hour.** The figure above is what RF2 measured as a *handoff input*. The
full LP1 §1 census — run immediately after RF2 closed, and filed separately at
`docs/orders/LP1_PIN1_S1_CENSUS.md` — scans all 97 workflow files across the four repos and gives
**18** (Site 9, Lessons 4, Apps 4, Games 1), or **16** collapsed. The progression 13 → 14 → 18 is
itself the finding: each deeper scan found more, because the gate is not always the literal
`github.event_name != 'pull_request'` string. Use 18/16, not 13 and not 14.

LP1 §5's stop — "the census contradicts §1.1 in a way that changes the scope materially" — is
**flagged, not decided**: that judgement is Matt's, not this session's.

Caveat stated rather than hidden: no workflow was executed, so every "skips on a pull request"
statement is read from the YAML condition, not observed in a run. No Actions run ids are cited for
these. LP1 §1.3 (which proofs *cannot* have a PR-time mode) is **not run** — it is LP1's own work.

### PIN1 — pin coverage by dependency

**State: NOT VERIFIED / MISSING implementation. Owner: with LP1.**

**PIN1 §1.1's carried 89 is CONTRADICTED — by roughly a factor of five.** Both instruments agree,
by independent methods (one an AST parse, one a separate enumeration).

The registry the #499 gates actually validate is `CATALOGUE_PINS["files"]` in
`Lessons/tools/verify_cross_estate_unification.py` (file SHA-256
`04c40f7e5a83d3daad795e7310c2ee1f19d7ab16b88779e016171fa51f125ddc`, 1,265 lines):

| Registry | file:line | paths pinned by digest |
|---|---|---:|
| `CANONICAL_HASHES` | `:60` | 4 |
| `MANIFEST_PINS` | `:99` | 2 |
| `CATALOGUE_PINS["files"]` | `:118` (block `:117`→`:557`) | **434** |
| `LUNDYLOOP_CI_PINS` | `:643` | 3 |
| `PUBLICATION_CALLER_SHA256_BY_KIND` | `:633` | 1 (`education-pages.yml`) |

**Union = 443 distinct paths, zero overlap between registries; 444 with the publisher-caller pin.**
That is the honest answer to "the pin set with its denominator". `CATALOGUE_PINS["files"]` alone is
434 at main and **425** at #499's base and head (#499 changed the two digests, not the row count).

**No registry measures 89.** Other candidate counts, each stated separately so none is silently
folded in: 734 `CATALOGUE_ORIGINAL_ROWS` (a row-count contract, not a path set) · 216
`CATALOGUE_SHELF_ROWS` · 47 `ALLOWED_DIFF` (a diff-boundary allowlist, not a pin) · 7
`CATALOGUE_RECORD_PATHS` · 3,529 Site admission-registry trees · 25/28 Site estate pin-dependents.

**The defect direction PIN1 §1.2 asks for:** asserted-but-not-triggered-on is **422 of 444** across
the union of both gates' trigger paths with globs expanded. (One lane first reported 438/444; the
second instrument corrected it — 438 counts a single gate and does not expand `ux2-gates.yml`'s
`assets/catalogue/**`, `data/**`, `tools/ux2/**`. The defect survives either way: 422/444 is still
95% uncovered, but 438 stated bare overstates it by 16 paths.) The **4 triggered-but-not-asserted
paths are precisely the checkers** — which is exactly why #499's gates fired at all, and is PIN1
§0.1's finding reproduced from the current tree.

**A gift for whoever runs §2:** PIN1 §2.2's "if the trigger cannot be derived" escape is unlikely to
be needed — a working precedent already exists at Site `tools/derive_pin_dependents.py`.

**A risk to carry into §2.3:** deriving the trigger list from that registry yields a ~444-entry
`paths:` block, 345 of them under `Science_Teesside/`. That is not `**`, so it does not breach §2.3
literally, but it is close to the spirit of "converts a targeted gate into noise".

**My earlier flag was wrong, and is withdrawn.** I reported `s1m-published-input-proof.yml:24` and
`tools/ux2/s1m_published_input_proof.py:11` pinning publisher `7072a5605e…` against a live caller of
`810ae8f8…` as PIN1-class drift. It is **not**: it is intentional historical pinning of a fixed past
deployment, and the same workflow's second job already uses the live `810ae8f8`. Corrected here
rather than left standing.

### SB1 — the sb3 schema gate

**State: NOT VERIFIED / MISSING implementation. Owner: Computing, riding with GC1.
RF2 §5.3 holds: the trigger is before a SECOND Scratch unit — it is not a new blocker for #493.**

| SB1 clause | Measured |
|---|---|
| `tools/gc1/check_sb3_parents.py` exists and is UNWIRED | **confirmed** — exists, nothing invokes it |
| §0.3 "no workflow references sb3 — grep is empty" | **contradicted as literally worded**: grep of Lessons `.github/workflows` returns **3 hits** — but all three are *comments* in `education-pages.yml`. **No workflow runs an sb3 schema gate**, so the substance of §0.3 stands |
| the acceptance rule actually in force | exact reviewed digest — confirmed |

**One finding SB1 does not anticipate:** Lessons main tracks **zero `.sb3` files**. The gate SB1
wants would today have no subject in-tree. That does not make the order wrong — its trigger is a
*second* Scratch unit, and #493 (unmerged, 164 files) carries the first — but whoever wires it
should know the proofs in §2 need a fixture before they can run at all.

---

## §6 The named Site and Games defects — assigned, not repaired

**RF2 §6.1/§6.2 honoured: no repairs were begun.** No commits, pushes, PR comments, reviews, merges
or workflow dispatches were made against any of these.

| # | Defect | Mechanism (measured) | Owner | Next action |
|---|---|---|---|---|
| 1 | Shelf control `#group` | `tools/lib/published-shelf-probe.cjs:100` demands `count===1` for 6 selectors incl. `#group`. The published shelf template `domain-split/play/index.html` carries **42 element ids and `group` is not one of them** — `UX2_PLAY_LEDGER.md:58` records `<select id="group">` as **RETIRED**. Present-but-failing, not absent | shelf/proof owner | Reconcile the probe with the retirement decision — the ledger already made the call the probe has not caught up with |
| 1b | *Second, downstream mismatch in the same probe* | Even with `#group` restored the next assertion fails: the probe expects `#result-count` to read "N of M games and activities" (`:114-117`), the builder writes `"<n> games"` (`domain-split/play/build.py:264`), and the ledger records live text as "n of 62 games" | same | Fix both in one pass, or the first fix buys one line of progress |
| 2 | Provenance's ten missing AS1 inputs | **Verified: exactly 10, all 10 exist.** Excluded at `build_education.py:242` via `SITE_GENERATOR_INPUTS` (`:71-82`); still required at `verify_deployment_provenance.py:325`. All 10 return `public_file()=True` **and** `is_served()=True`, so nothing but the explicit exclusion keeps them out, and all 10 appear in `git diff HEAD^ HEAD` so all 10 become changed-served witnesses. Job 103409664052 printed exactly 10 `[FAIL] … not present at the expected commit` lines, one-for-one | provenance owner | Make the two classifications agree. RF1's warning stands: a missing artifact path must not simply be dropped, or a real missing output hides |
| 3 | Driving-games served/derived mismatch | `.github/workflows/driving-games-live-verify.yml:101-147`. 2 of 3 subjects MATCH; `/rallyvector3d/` failed after 30+60+90s of waiting. **Re-derived here, not carried:** expected blob `01bafd929b43644b98b97783db1627fea64d54bfba2fb3537f723723fcd16257` — identical to the job's committed figure. Job started ~5 min after the merge, consistent with Pages lag outrunning the 180 s wait | Play pin/proof owner | Establish whether this is deployment lag or a real divergence — **not measurable from this session** (outbound HTTPS refused by the proxy, `curl (56) CONNECT tunnel failed, 403`) |
| 4 | Cancelled `verify-live` | **Body is now establishable.** Job 103409664192 = workflow "Professional site live verification", job `verify-live`, run 34643810013. Of 7 substantive steps: 3 succeeded (incl. `test_published_site.py`, 20 tests OK), **step 4 CANCELLED**, steps 5/6/7 **SKIPPED**. Last output `FETCH site: source 1651b84…` at 20:22:01Z, then 12m14s of silence to `The operation was canceled` | provenance owner / release-control | **Record as cancelled/unmeasured. Zero assertions about the served site were made — any readback listing it green would be false.** Cancellation cause not exposed by the API |
| 5 | Games merge rejection | Both #78 and #79 `mergeable_state: blocked`. Combined commit status `total_count: 0` — **zero legacy statuses have ever been posted**. `contract` and `aggregate` are each present and **success** on each head (27/27 success on #78). But **every sampled run behind those checks has `event: workflow_dispatch`** — 4 of 4 dispatched, 0 of 4 from `pull_request`, despite `pr-canonical-contract.yml` declaring `on: pull_request` | pin-release owner | See the ranked cause below |

**Defect 5 — the strongest candidate cause, with direct textual corroboration.** The Games workflow
carries its own instruction: *"Matt's ruleset click (his alone): require the check named
**\"PR canonical contract / aggregate\"** once this is on main."* That is a **workflow-qualified**
context name. The names actually reported are the **bare job names** `contract` and `aggregate`.
Two required contexts that are never reported under the names the ruleset requires read exactly as
**"2 of 2 required status checks are expected"** — which is the observed message.

Ranked alternatives, kept because the ruleset itself could not be read: (b) the ruleset pins the
contexts to an integration/app id that does not match the reporting app; (c) the required contexts
are legacy *status* contexts, and `total_count: 0` shows none has ever been posted. **Candidate (a)
is the only one with corroborating text in the repo.** Stated as ranked candidates, not asserted —
no branch-protection or rulesets tool is exposed in this session, so the actual required-context
strings remain unmeasured.

RF1's closing instruction is honoured: no unbounded repair arc was begun on any of these.
---

## §7 Blocker ceiling — reached in the PRX1 lane

RF2 §7: *"Three distinct unresolved blockers in one lane and you checkpoint, stop expanding that
lane, and continue eligible work elsewhere."*

The PRX1 lane carries **four** distinct unresolved blockers, each measured above, none of them the
same problem under a different name:

1. **§2.2** — no balance assertion; a measured straddle case passes unchecked.
2. **§3.4** — zero DOM/parse-tree coverage in the candidate.
3. **§4.1** — no DECISIONS entry.
4. **§4.2** — the §1.3 census has not landed as a finding.

A fifth — **§2.3/§3.1**, byte-identity unproven — was open when this lane was first checkpointed and
has since been **closed by measurement**: the golden test ran 33/33 byte-identical. It is recorded
here as retired rather than deleted, because RF2 §7 forbids restarting the count under a new name
and the honest record is that the lane went to five and came back to four.

**The ceiling is reached. This lane is checkpointed and not expanded further in this session.** The
count is not restarted under another name, and RF1's closing instruction — *"do not begin another
unbounded repair arc"* — is honoured. Eligible work elsewhere (ML1's residue, BL1's inventory, the
§5 handoff, the §6 assignments) was completed rather than abandoned, exactly as §7 directs.

The stop still permits a required rollback and its publication verification. **None was required:
RF2 made no production merge, moved no pin, and started no publication.**

---

## §8 READBACK

### Per-lane state

| Lane | State | Owner | Evidence · measurement time | Exact next action |
|---|---|---|---|---|
| **ML1** (row 4) | **CLOSED-BY-DL**, residue named | release/control | shelf-mirror-guard red on real drift run **33713403941** (3 Sep); #191/#192/#194 merge SHAs verified; patch-apply checks · 2026-09-12 00:0x UTC | Mark `MBM_LIVE_MIRROR_LEG_DEADLOCK.md:158` superseded by its own APPLIED section, under its own transaction |
| **PRX1** (row 5) | **IN PROGRESS**, release **HELD**, lane **checkpointed at the §7 ceiling** | release/control | #350 head `3c11780a`, 4/4 required contexts green · 23:53 UTC. **Golden test 33/33 byte-identical** (28/28 header, 5/5 main), plants proved to fire · 2026-09-12 00:45 UTC | Land the §1.1/§1.2/§1.3 censuses, the DECISIONS entry, a DOM control and a balance assertion — then re-audit. **Do not merge before that.** §3.1 is now satisfied; four clauses are not |
| **BL1** (row 6) | **READY** — inventory complete, sequence proposed, nothing executed | release/control | 7 open PRs, 12/45 failing exact-head, 21/21 empty pairs · 2026-09-11 23:5x UTC | Matt approves or amends the §4.3 sequence; only then does BL1 §3 execute |
| **LP1** (row 7) | **NOT VERIFIED / MISSING implementation** | LP1/PIN1 owner, own session | fieldops lines 359/360, 370/371 verbatim; 14 live proofs measured vs 13 carried | Recover nothing further — the scope is in hand. Decide whether 14-vs-13 is material under LP1 §5, then run §1.3 |
| **PIN1** (row 8) | **NOT VERIFIED / MISSING implementation** | with LP1 | 443/444 pinned paths across 5 registries; 422/444 asserted-but-not-triggered | Re-base the order on 444, not 89, before attempting §2. Precedent exists at Site `tools/derive_pin_dependents.py` |
| **SB1** (row 9) | **NOT VERIFIED / MISSING implementation** | Computing, with GC1 | `check_sb3_parents.py` exists, unwired; 0 `.sb3` files tracked | Not before a **second** Scratch unit. Needs a fixture before §2's proofs can run |
| **§6 defects** | **assigned, unrepaired** | five named owners | see §6 table | Each owner picks up; no repair begun here |
| **Brand marks** | **CLOSED by ruling** | Matt | current mark `assets/brand/micro_mark.svg`, 263 B, SHA-256 `c6b5d066…` | None. Both marks stay as they are; the nine supplied icon files are design references only, adopted nowhere |
| **Play surface redesign** | **HELD** | SW2/Play owner with Play pin owner | Games #78 promotion of Site `1651b84c` rejected by the idle-repaint gate: 8→36 frames/600 ms, cap 18, one regressed route of 69 | Reconcile the idle-repaint disagreement (AS1 measured 37.99→0 paints/sec on the same route) before any design work. Route via UX1 Part C, still MISSING-SCOPE. Part P remains header-parity only |

### What remains MISSING-SCOPE

Unchanged from RF2 §0.2. None was implemented, closed or superseded:

**GW1-E · GW1 §B–§F · LW1 · UX1 Part A §3 onward · UX1 Part B §1.5 onward · UX1 Part C ·
TH1 Part C · full LF1-M.**

A prioritisation for the second extraction pass, derived from the §0 prerequisites that *are*
recovered:

1. **GW1-E, GW1 §B–§F, LW1** — highest. The only remaining Lane A foundation scopes, and nothing
   gates them but their own text.
2. **TH1 Part C** — small, and two open Lessons PRs (#465, #497) are parked on it.
3. **LF1-M** — unblocks Lane F and clears UX1-A §0.5.
4. **UX1 Part C** — B7 records Part C as "separate and unaffected" by A and B.
5. **UX1 A §3+ and B §1.5+** — last. **Recovering them would not make either order runnable**:
   UX1-A §0.3/§0.4/§0.5/§0.6 are all currently unmet (return-week pathways unbuilt, #493 unmerged,
   LF1-M incomplete, the catalogue about to move), and "any miss is a stop". UX1-B additionally
   needs the mirror leg repaired and Part A landed.

One recursion worth naming: **UX1-A §0.1 requires UX1's order text to be committed to
`docs/orders/`**, Appendix B's own standing action says the same of every order in it — and the only
commit of Appendix B is on **unmerged draft #351**. Merging #351 is the cheapest single action that
moves a real prerequisite, and its publication exclusion is measured, not assumed.

### Standing limits — all honoured

No check weakened. **No production merge.** Lessons #456 held (open, 14 success + 2 skipped + 0
failure). Games #78/#79 untouched — read-only. Site #346 still owns `docs/SW2_LEDGER.md`. No Science
content writes. No SW2 design writes. **No `REGISTER.md` write.** No reset to `2e49afdd`. S1-M's
removed size-table ratchet not reinstated. No shared-queue token held.

### Evidence discipline

Every figure above carries its measurement time or an explicit **not run**. The five numbers that
decide a stop were each re-derived by a **second instrument** using a different method, per ML1
§3.6's "two instruments": the nesting census (hand-written lexer vs `html.parser`), the golden-test
denominators, ML1's quiet-or-not, BL1's failing-check sum (two transports), and PIN1's 89
(AST parse vs independent enumeration). **All five agreed on every headline number.**

Three carried figures were **contradicted** and are reported at their measured values, not bent to
fit: PRX1 §0.5's "7" audience targets (**5**), LP1 §1.1's "13" live proofs (**14**), and PIN1
§1.1's "89" pins (**443/444**). One figure I myself reported earlier in this session was wrong and
is **withdrawn**: the `s1m-published-input-proof.yml` publisher pin is intentional historical
pinning, not PIN1-class drift.

### Token

**RF2_PARTIAL.**

Per RF2 §8, PARTIAL is required if any RF1-owned scope is still missing, and eight scopes are.
It is also the correct token on its own merits: PRX1's release condition is not met, the PRX1 lane
has reached the §7 blocker ceiling, and BL1 §3 awaits Matt's approval by design rather than by
failure.

What RF2 did close, on evidence: ML1's residue (all three PRs verified merged; §2.3 confirmed live);
BL1 §1 in full, including the three outputs RF1 never produced; PRX1 §1.1, §1.2, §1.3 and **§3.1**;
the §5 handoff; and the §6 assignments. What it did not close is named above, per clause, with the
measurement that decides each.

<!-- mbm-rf2-reconcile-recovered-scopes-2026-09-12-BOTTOM -->
