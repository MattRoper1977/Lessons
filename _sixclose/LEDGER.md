# LEDGER — eight-pass close, 2026-08-05

Sentinel `six-close-2026-08-05`, revision 2. One session. Execution order as briefed:
P1 → P7 → P2 → P3 → P4 → P8 → P5 → P6 → close. **Nothing here is quoted from the brief as
fact; every figure below was derived in this session at the SHA named beside it.**

## §0 · Gates, capability, base

**Identity gate — Lessons, 5/5.** `Humanities_Teesside/Lundy_Humanities/START_HERE.html` ·
`_approved0805/DT_SAFETY_PROPOSAL_FOR_REVIEW.html` · `_passpq/FINDINGS.md` · `REGISTER.md`
with `_close/OPEN_ITEMS.md` carrying open item 17's 5-Aug BUILD/GROW-only scoping ruling ·
`tools/build_staff_pack.py` + `REBRAND.md` at root. This session opened in the **site**
working directory; the Lessons and Games repositories were attached and cloned rather than
assumed. The eleventh site-repo mis-open did not happen.

**Capability census.** Lessons read ✔ write ✔ (proven by the Pass 1 push, not by scope alone)
· site read ✔ write ✔ scope · Games read ✔ write ✔ scope. No browser, no direct network:
every claim below is git truth or a local instrument run. **No live page load is claimed
anywhere in this ledger.**

**Base derivation** (expectation stated, then derived):

| repo | expected | derived at open | verdict |
|---|---|---|---|
| Lessons | at/beyond `bd4d5ef` | `bd4d5ef` | exact — re-derived by a second route |
| site | at/beyond `87741ae` | `0524533` | **3 commits ahead**; the estate wins, delta recorded |
| Games | at/beyond `900fae5` | `900fae5` | exact |

The site's three-commit delta is the Neon Sync **Stage 1 gate fix, PR #56** — see Pass 2.

**Sentinels, expectation-then-derived, universe stated.** Expected loop-mark 50 / written-line
98 over 548 bare tracked `*.html`. Derived at open via `LundyLoop/tools/bundle_facts.py`:
**50 / 98 / 548**, identical on the raw and R-E08 forms — the `5_staff_training` exclusion
contributes **0**, a proven no-op today and a prospective guard only. Because that hit the
prediction exactly, it was **re-derived by an independent route** (byte-level walk over
`git ls-files -z '*.html'`, not `git grep`): **50 / 98 / 548**, overlap 0. Derived again at
close — unmoved. **No count delta to attribute.**

**Input manifest** (listed and hashed before use, classified by content not filename):

| file | bytes | sha256 (head) | content verdict |
|---|--:|---|---|
| `Compress_05_08_2026_014910.zip` | 687,623 | `973cd9d8…` | **25 xlsx planners** — 8 BUILD + 8 GROW + 8 unprefixed + the ASDAN year-plan update. Matches the Pass 6 expectation. **Real pupil names inside — sensitive from the moment it opens.** |
| `Compress_05_08_2026_015643.zip` | 150,492 | `4a2ecbec…` | **ASDAN 19-file review set** → Pass 8 is on **Route B**. Absent: both patches, the whole `repo-overlay/` toolkit, `build_payloads.py`/`check.py`/`integrate.py`, all 85 SVGs, the manifest, the checksum |
| `Compress_05_08_2026_125732.zip` | 39,181 | `ddfb5d4c…` | **not the ASDAN pack and not a new game** — Neon Sync v1.1 prepared content + its evidence logs. Drives Pass 2 |

The full 139-file ASDAN pack (`9740ae0c…`) **did not arrive**, so Route A's provenance gate
was never available.

## §1 · Pass 1 — item-17 restore-sitting append · **MERGED**

Base `bd4d5ef` → closing **`bc38dfa`**, direct to Lessons `main` (authorised by the embedded
order for this append alone). Docs-only; nothing else rode in the commit.

Gates: diff = exactly **one** file (`_close/OPEN_ITEMS.md`) · row 17 **restores byte-for-byte
minus the append**, proven by reconstruction (1,615 B → 1,615 B, equal) · row count **41**
unchanged, nothing renumbered · every other line byte-identical (only line 56 differs) ·
sentinels 50/98/548 unmoved, universe unmoved (the file is `.md`) · assessed pair and frozen
legacy hashes re-emitted below. The append is 803 B.

The line-level diff reads `1 insertion(+), 1 deletion(-)` because a markdown table row **is**
one line; the additions-only property is proven at character level by the byte-exact prefix,
not by the line count.

Landed text preserves every required element: one sitting · both halves, neither without the
other · the BUILD/GROW **ten** by reverse-diff · the LAUNCH **fifteen** re-commented
permanently to "stays hidden — GCSE route", at that sitting and not before · all 25
**byte-pristine** until then · **trigger unchanged: Cheryl's confirmed codes.**

**No sheet was edited. Nothing was restored.**

## §7 · Pass 7 — A2e ratify verification · **VERIFIED, one finding**

Verify-and-record. **Nothing was repaired.** All four checks run at HEAD:

1. **Ancestry + content lock — PASS.** `bd4d5ef` is an ancestor of `main`. Its diff touches
   `Art_Teesside/HANDOVER.md` (register) and `Art_Teesside/tools/assert_kit.py` (instrument)
   and nothing else — **0 files under `Build/`, `Grow/`, `Launch/`**.
   *The first control I wrote for this was vacuous* — it read a **merge** commit, and
   `git show --name-only` on a merge prints nothing, so the "0" would have been free. Repaired
   with a non-merge commit, where it returns 1. `bd4d5ef` is single-parent with exactly 2
   files, so its zero is a real zero. **Recorded because a control that cannot fire measures
   nothing, and this one silently could not.**
2. **Ladder at HEAD — PASS.** refusal **15** / refusal-candidate **0** / total **15**.
   Instrument source read directly: `classify()` receives `rel` (line 192), and `OVERRIDES`
   is `[]` (line 75), so `RATIFIED` is the only consumer of the changed argument.
3. **Can-fail controls, re-run independently — PASS.** Mis-scoping the ratified Launch
   fragment returns cand to **4**; reverting to basename matching returns cand to **4**;
   the untampered baseline is **15/0/15**. Both were run on copies of the tree — the
   repository working file was never modified (verified clean afterwards).
4. **Disclosure — PARTIAL. One finding.** The enabling classifier change **is** flagged as an
   enabling change separate from the ratification, in both the commit message ("ONE ENABLING
   CHANGE, which is not tidying") and the register ("### One enabling change, reported rather
   than buried"). But the **squeegee / dye / bare-screens observation is not recorded
   anywhere** in the ratify commit or the register section.

**The finding, stated so it can be closed cheaply.** The ratified sentence names "no screens,
squeegees or dyes either", but the instrument's declared scope does not reach those words. The
four LAUNCH hits are, derived exactly: `inks` ×2 and `rollers` ×2 — matching the reported
"rollers ×2, inks ×2". Of the other kit named, **`squeegee` and `dye` appear in no pattern at
all** (outside declared scope), and `screen` is covered only by `\bscreen ?print\w*`, which
the bare word does not match. So the observation is **true and no action is needed** — but it
is undocumented, and the next reader who greps the sentence will re-derive it from scratch.
**A one-line note in `Art_Teesside/HANDOVER.md` closes this. Not done here: Pass 7 repairs
nothing.**

Ledger position, on the three green checks: **A2e ratified · the Art register has no undecided
entries · refusal-candidate 0 estate-wide · art has no reserved passes left.** Remaining art
items are human: D2 on 17 Aug, the 2C-2D tag with the adviser, the A2c bench test, browser
spot-checks, the 29 Aug pack rebuild.

## §2 · Pass 2 — the game · **PARKED, with the block named**

**The premise did not survive contact, and the difference matters.** The brief expects a *new*
game needing a slug, a shelf entry, a hue and a sitemap line. What arrived is **Neon Sync
v1.1** — a prepared content upgrade to a game **already published** at `madebymatt.uk/neonsync/`
and already in the sitemap. No new slug, no placement, no homepage question. Matt attached no
placement master prompt, so §2.2's untrusted-input reconciliation had nothing to reconcile.

**§2.1 existence gate — PASS, on real bytes.** `index-2.html` hashes
**`6f10b2989f73db70d63ed036853af0b3508e2166ff892c13118e18cf9bcc22a5`, 84,546 B** — exactly the
prepared identity claimed. 2 inline script blocks, **0** syntax errors under `node --check`,
ends `</html>`. This is not a phantom tree; the Apex Golf stop does not apply.

**Base anchors, all re-derived against the live site repo:**

| path | claimed base blob | derived | state |
|---|---|---|---|
| `neonsync/index.html` | `17bfe08c` | `17bfe08c` | **matches** — Stage 2 not landed |
| `tools/verify_neonsync.js` | `43e3d4d4` | `43e3d4d4` | **matches** — Stage 2 not landed |
| `sitemap.xml` | `2ab33053` | `2ab33053` | **matches** — Stage 2 not landed |
| `.github/workflows/neonsync-verify.yml` | `a6dfc5db` | `7a5dcc2c` | **moved** — Stage 1 landed |
| `tools/verify_neonsync_browser.js` | `884b7642` | `43a49ee2` | **moved** — Stage 1 landed |

So the world is exactly: **Stage 1 (gate-fix PR #56) has merged; Stage 2 is outstanding and
its three paths are untouched at their recorded base.**

**Why it parked.** Stage 2 is three paths. Two are in hand — the game bytes, and a one-line
`sitemap.xml` `lastmod` change. **The third is not: the prepared harness
`tools/verify_neonsync.js` (37,755 B, sha256 `8c699b9d…`) is absent from the inputs.** That is
decisive, and it was measured rather than assumed:

- committed harness vs **committed** game → **83/83 pass, exit 0**
- committed harness vs **prepared v1.1** game → **81 pass, 3 FAIL, exit 1**
- harness self-test → **6/6 tampered copies rejected, positive control passes** — the gate is
  non-vacuous and genuinely can fail

All three failures classified: `three-heroes` (v1.1 adds a fourth hero, Volt) ·
`hard-cap-six-minutes` → `undefined` (v1.1 restructures the cap; the vendor names a new
`uncapped-cc` tamper family) · `delivered-sha-unchanged` (the harness hardcodes the **base**
game hash — the A-6 pin shape). Every one is a **v1.0-era assumption in the old harness**, not
a defect in v1.1 — and the prepared 37,755 B harness, with its 162 checks and 8 tamper
families, is precisely what replaces them.

**Landing the game without it would take the site's own gate from exit 0 to exit 1.** The only
alternative — authoring a replacement harness that passes the new content — is writing the
gate to fit the content it judges, which this estate forbids in as many words. **So it holds.**

House rules verified on the prepared bytes anyway, so nothing is unknown when it does land:
storage keys namespaced **`mbm_neonsync_*`** only · no remote resources beyond the w3.org SVG
namespace and its own canonical URL · sitemap carries **exactly one** `/neonsync/` loc, and
**445 locs, 445 unique, 0 duplicates** estate-wide.

**To unpark, one artefact:** `tools/verify_neonsync.js`, 37,755 B, sha256 `8c699b9d…`. With it
the whole of Stage 2 lands in one gated commit.

**Separate finding — Neon Sync is not on the shelf at all.** `Games/games.json` contains **zero**
occurrences of `neonsync`, while the game is live and in the sitemap. The vendor's census
records "zero prepared delta" for `games.json`, so this is deliberate on their side, but it
leaves a published game with no shelf entry. **Matt's call, not fixed here.**

## §3 · Pass 3 — estate sweep · **SWEPT; the headline is that the estate is clean**

Measure-first across all three repos. **Every inclusion rule is stated with its result, and
every non-zero count is classified — including the ones that turned out to be my own
instrument's fault.**

**Inline JavaScript — 0 errors.** First run reported **21 syntax errors**. All 21 were
**instrument artefacts**: the rule excluded `src=` but not non-JS `type=`, so it fed
`type="importmap"` and `type="application/json"` payload blocks to `node --check`, which
correctly rejects JSON. Corrected rule — *type absent, or in {text/javascript, module,
application/javascript, text/ecmascript}* — checks **987 genuine blocks across all three
repos: 0 syntax errors.** Recorded because 21 errors reads as a crisis and would have sent a
fix band after nothing.

**File integrity — 0 truncations, 0 zero-byte files.** The naive rule (*rstrip does not end
`</html>`*) returned 9. All 9 classified, none a defect:

- `apexgolf/index.html`, `apextennis/index.html` — end `</html>` then a deliberate trailing
  build sentinel comment
- `hub-highlight-card.html` — an include **fragment**, by design has no `</html>`
- 5 × `2 Physics 10/…` + `biology/Digestion_and_Absorption (1).html` — inside the **frozen
  legacy science trees**, a Band-3 deliberate state, verified and left

**Shelf schema** (`Games/games.json`, 34 entries): `art` present on **every** entry ✔ · titles
and hrefs unique ✔ · the "duplicate ids" my first run reported was an artefact — **the schema
has no `id` field**, identity is `title`/`href`. `hue` is real and **is** widely shared (7
values reused across up to 5 entries each) — an existing, long-standing state, not something
this pass may quietly restyle. Reported, not touched.

**Sitemap:** 445 locs, 445 unique, **0 duplicates**.

**Workflow pin census** — rule: any 40/64-hex literal or `=== N` / `-eq N` count assertion in
any CI file, all three repos. Eight hits, all classified:

| location | pin | verdict |
|---|---|---|
| `games` `apexpool-sports-verify.yml:39` | `games.length!==33` against **current `origin/main`** | **STALE — genuinely broken.** main's shelf now has **34** entries, so this step exits 1 at its baseline. The A-6 shape, live |
| `site` `apexpool-home-verify.yml:45` | apextennis `sha256 8e109ab5…` | **live pin, currently TRUE** (re-derived: matches). Not stale — but it breaks silently the day tennis legitimately changes. **The named open member of the derive-or-die register** |
| `site` `apexpool-home-verify.yml:164` | PR #25 head `7c202790…` | **deliberate** — it guards the held PR #25 (§R.8) and says so in the next line |
| `site` `apexgolf-verify.yml:59`, `apextennis-verify.yml:38` | donor harness `checks -eq 25` | pins an external harness's check count — drift detector, arguably intentional |
| `site` `neonsync-verify.yml:83` | `DELIVERED=6b5cbb9d…` | the never-supplied original harness hash; see Pass 2 |
| `site` `biopunkhive-verify.yml:95`, `neonsync-verify.yml:153-154` | `-eq 1` / `-eq 0` on **grep counts** | **derived assertions, not pins** — correct as written |
| `site` `arcade-sports-verify.yml:39` | comment naming `900fae5e` / `length !== 34` | already derived; comment only |

**Band 1 (fix, gate, merge): nothing was merged.** The one genuinely stale pin lives in the
**Games** repo, in a workflow scoped to a held branch (`codex/apextennis-arcade-sports`);
rewriting its baseline step changes what that gate asserts, which §3.2 puts in Band 2, not
Band 1. **Held as a proposal rather than merged on my own authority.**

**Band 2 (propose, hold):** the Games `!==33` baseline · the apextennis hash pin → derivation ·
`games.json` hue reuse · Neon Sync's missing shelf entry · Pass 4's two pupil-facing hours
hunks · the "GOLD reach" tier wording.

**Band 3 (deliberate states, verified and left — with authority):** the BLOCKED unmounted
science toolkit at `Science_Teesside/visual-learning/` (open item 37) · the 25 hide comments'
unscoped wording (**open item 17 is the authority, the in-file comment is not**) · TBC
placeholders · held branches and PRs — `claude/semh2-claims-accuracy`, `pass-sl-sow-launch`
@ `2a1cfda`, `pass-sbx-art-a2`, site **#25**, `codex/apex-golf` retained · the Careers W6/W7
label-vs-filename swap · frozen legacy science · folded-away legacy sets · open item 39's
pending build, which belongs to the Estate Visuals session and was **not taken here**.

## §4 · Pass 4 — accreditation audit · **DELIVERED**, one fix, three proposals

Full verdicts in `_sixclose/ACCREDITATION_MATRIX.md`. Counts: **VALID 4 families ·
WRONG 3 surfaces (one fixed, two held) · VAGUE 1 family · UNDETERMINED 1 (the largest)**.

Headline: **`Delivering a Project` = 0 estate-wide**, and the 10-hour window sits on **critical
thinking 3.5.1, not Communication** — open item 9's close re-derived, not quoted, with
**0** residual ComSk1 10-hour claims. The violation found is an **Arts Award hours threshold**
on three LAUNCH Art surfaces; the staff-facing one is fixed, the two pupil-facing ones are held
because rewording a task item changes what a pupil does. Extensions to
`_passpq/QUESTIONS_FOR_CHERYL.md` are append-only: **Q11** (which surfaces count as public for
unit-code printing) and **Q12** (the two unhomed descriptive-week codes).

## §8, §5, §6 · Not reached — **PARKED, with what each needs**

These three were not started. That is a real shortfall against the brief and is stated plainly
rather than dressed up; each is parked with its blocking condition so the next session opens
where this one stopped.

- **Pass 8 — ASDAN visual-learning pack.** Route determined: **Route B**, the 19-file review
  set. Both patches, the entire `repo-overlay/` toolkit, all 85 SVGs, the manifest and the
  checksum are **absent**, so the generator route is unavailable by definition and integration
  would have to be authored per surface after recovering the toolkit from
  `ASDAN_Visual_Learning_Demo.html` (378 KB, present). **Nothing was recovered, mounted or
  committed.** The architecture existence gate (§8.2) was **not run**, so the pack's central
  claims about this repo remain unverified — and the vendor's own decisive gate, full
  post-integration regression in a current checkout, remains **unrun**. Nothing pupil-facing
  may merge until it is.
- **Pass 5 — Progress pack rebuild.** Depends on Passes 1–4 and 7–8 landing so one pack
  captures every merge. Inputs are present (`tools/build_staff_pack.py`, `REBRAND.md`), so this
  is blocked only on session budget, not on missing artefacts. **No zip was built.**
- **Pass 6 — weekly planners.** The gate **passes**: 25 xlsx present and identified by content.
  Not run. **No planner was opened, so no pupil data entered this session's working set beyond
  the archive sitting unread on disk.** Matt should still delete the uploads.

## §R · Invariants, re-emitted at close

- **★ ASSESSED PAIR — 0 bytes of diff, by name and hash:**
  `Grow/Slideshows/GROW_HUM_W7_Write_The_Account.html` → `a5545585ca28bbba01b55476abb73a9b0819bcc7`
  `Launch/Slideshows/LAUNCH_HUM_W7_Source_Assessment.html` → `eb14d6104b94503d0e7ec0a99565ef116a333a57`
- **Frozen legacy trees, unchanged by hash:** `biology` `2fdbd43a3bb20bf2fc76c82260029594fad2834b` ·
  `chemistry` `c60a17078bc6b222beb0e6abd6487e2b44381257` ·
  `2 Physics 10` `57be7374873444ed93b2a65042c0a5f5339cb810` — all three match the recorded values.
- **The 25 hidden science witness sheets: byte-pristine.** No restore, no un-hide, no edit to
  any in-file hide comment. The only movement near them this session was Pass 1's append to
  open item 17 — a docs row, not a sheet.
- `claude/semh2-claims-accuracy` **not merged, not deleted, not rebased, not swept.**
- **No printer hold released** (#35 art print check · influence-board banner · tk1-access-2).
- `Science_Teesside/visual-learning/` **still BLOCKED — DO NOT MOUNT**; zero lessons load it.
- **Open item 39 not taken.** No branch deleted. Nothing from §R.8's never-merge list merged.
- **Zero pupil data** in any commit, PR body or committed file. No © ASDAN PDF entered git.
- **No clip, embed or media URL was wired into any lesson.** No media register was created.
- **No third-party image or artwork committed.** No closure-marker moved; no new pupil-facing
  warrant; no second next-step, backlog or failing-reflection state created anywhere.
- **No rollback recipe was run. No force-push. No deployed history rewritten.**
- **Zero-lesson-diff assertion:** Passes 7, 3 and 2 promised it and each holds — Pass 7 wrote
  nothing, Pass 3 merged nothing, Pass 2 landed nothing. Pass 4's single edit is a lesson-
  adjacent scheme-of-work file and is declared, not silent.

---

# SESSION L — lessons continuation, 2026-08-05

Sentinel `session-l-2026-08-05`, revision 1. Four jobs L1 → L2 → L3 → L4, all four reached.
**Nothing below is quoted from the brief as fact; every figure was derived in this session at
the SHA named beside it.**

## §0 · Gates

**Identity, 7/7.** This session also opened in the **site** working directory. The Lessons repo
was attached and cloned rather than assumed, and the identity gate was run against it before
anything else: all seven markers present, including `_sixclose/LEDGER.md`, read first.
**The eleventh site-repo mis-open did not happen.**

**Base.** Expected at/beyond `127aa80`; derived `127aa80`, equal to `origin/main` at open.
Neither stale nor ahead.

**Sentinels, expectation-then-derived.** 50 / 98 over **548** bare tracked `*.html`, by the
committed instrument and again by an independent byte-level walk over `git ls-files -z` using
the literal marker strings — identical, overlap 0. The `5_staff_training` guard contributes
**0 / 0** over 7 files: a proven no-op again. Unmoved at close.

*An instrument correction, recorded.* The first independent walk returned written-line **0**,
not 98 — my regex guessed at the marker instead of reading it. The real literals are
`ll-g:loop-mark v1` and `What I said, and what it changed`, taken from
`LundyLoop/tools/bundle_facts.py`. A guessed pattern that returns 0 is evidence about the
pattern, never about the estate.

**Inputs, classified by content.** The planner zip matched the recorded `973cd9d8…` (25 xlsx).
The second upload was **neither** previously-seen artefact: nested inside it was
`ASDAN_Visual_Learning_Upgrade_Pack_2026-08-05.zip`, sha256 **`9740ae0c…`**, matching the brief
and its own checksum file. **139 of 139 MANIFEST entries re-hashed OK.** The 140th file on disk
is `MANIFEST.sha256`, which cannot hash itself — that reconciles 140 to the stated 139.
**Route A was available for the first time.**

## §L1 · LAUNCH_ART_W8 hours + P7 records — **MERGED, PR #60**

Base `127aa80` → closing **`f36ddd0`**. Ruling D1 applied by rewording, never deletion: the file
**grew** 101,136 → 101,342 B and the threshold figure went **4 → 0**. Five spans, each with a
declared expected count, applied through the estate's own `safe_edit.py`.

Two things the eight-pass record did not have. **A third pupil-facing occurrence** — the
product-card badge — was found by this session's census and is not in Pass 4's two-surface list.
And the KO-table row was **checked and needed no move**: it already carried the honesty frame.

D2 records. The Pass 7 finding closed in `Art_Teesside/HANDOVER.md`, re-derived from the
instrument's pattern list: `squeegee`, `dye` and bare `screen`/`screens` match **no** declared
kit-dependence pattern — and **bare `press` is outside scope too**, which the original finding
did not name. The four ratified LAUNCH hits are exactly `inks` ×2 + `rollers` ×2.
`REGISTER.md` records the fired-fixture entry, **proven not asserted**: `067c76a4`, `a597123d`
and `8f4f9b17` each print **0** files under `--name-only` and **4**, **35** and **3** against
their first parent.

Gates: A2e **15 / 0 / 15** unmoved · all HTML comments byte-identical · sentinels unmoved.

## §L2 · Weekly planners — **DELIVERED, zero commits**

25 xlsx, gate passed by content. **No planner row required a content update**, and the 25 files
were returned byte-identical with only the download suffixes stripped. A byte copy rather than an
openpyxl re-save: with no content delta, re-saving risks the merged ranges, widths and 96
formulas for no gain.

The claim is evidenced, not assumed. **131 lesson references, 131 resolve at HEAD.** 99 referenced
lessons changed since 30 Jul, but **85 have their planner-mirrored content unchanged** — the large
diffs are marker-owned toolkit blocks. Of the 14 that moved something, none reaches a planner:
`Delivering a Project` is **0** in all 25 planners, and the word-boundary count for inking-station
kit is **0** (raw 19, every one `thinking` or `linking`). 96 formulas, **0 errors**.

*Two instrument corrections.* A first sweep reported one broken lesson link; the pattern had
stopped at the hyphen in `Self-Care`. And the inking raw count of 19 was entirely false positives.
**Both counts are recorded, not just the flattering one.**

Flagged and deliberately not fixed: the 33 `WellbLeE3` PEQ cells, and the two cells claiming
"3 credits / 30 GLH" — worth a look given ComSk1-only registration. The LAUNCH `A25`
accreditation line already reads correctly and was left alone.

**No pupil name, diagnosis or reading age entered any report, commit or PR.**

## §L3 · ASDAN Visual-Learning — **BAND A MERGED, PR #61**

Closing **`0bb4af4`**. 104 files, all additions, 0 outside `ASDAN_Visual_Learning/`.

**Architecture existence gate, run first.** `BUILD_ASDAN/_framework/` exists; the mechanism is
real and is marker-owned block injection; **31 of 39** BUILD_ASDAN decks carry `asdan-teach.css`,
so the claimed 31 genuinely materialise. GROW/LAUNCH `visual-upgrade.css/.js` all exist and 62
decks load them. **All 85 declared SVG targets resolve to a real repo lesson (85/85), and 0 of 85
changed `a4b19e2` → HEAD** — the vendor's delta claim independently confirmed.

**The six D&T decks are NOT on this chassis:** `Build/Slideshows/BUILD_DT_W1..W6` carry 0
`ASDAN-TEACH` markers and 0 `visual-upgrade` references, and the compiler's scope is
`BUILD_ASDAN/*/*.html`, which does not reach them.

**Independent verification, every non-zero classified.** Payload/runtime: 0 storage, cookies,
network, forms, camera/mic, file inputs, clipboard — the raw scan's 4 / 6 / 2 all live in the
pack's own `check.py`, which names them in order to forbid them. 0 closure markers. The 3
"criterion codes" are version strings. **"receipt" ×7 are shop and handover receipts** — the
payload itself says *"not proof of long-term impact"*. **"calorie" ×1 is a disclaimer**:
*"checks food-group variety, not calories or a pupil's body."* 85 SVGs: 0 external URLs, 0
missing title/desc, 0 raster.

**Why it stopped at A.** Band B would mount a pupil-facing surface while the vendor's decisive
post-integration regression gate is **unrun** — which the brief forbids outright. Also unresolved:
the engine has the blanket reduced-motion CSS rule and one `@keyframes` family (`asvl-attention`)
but **no `matchMedia` reduced-motion query and no change listener**, and both are required.
Both are named in the standing BLOCKED — DO NOT MOUNT block at the head of README and engine.
`docs/MEDIA_REGISTER.md` landed under a candidate-register header: ~250 URLs, **none resolved**,
because this container has no network. 0 iframes. **Mounted by nothing: 0 of 548 tracked
`*.html`, on a control proven able to fire.**

## §L4 · Progress pack rebuild — **DELIVERED, + PACK-2 fixes**

Scope was **not** extended for the L3 assets: REBRAND.md's own rule is that only what a deck
actually loads ships, and L3 landed mounted by nothing. The brief's conditional was false.

But crawling the **assembled** pack found two defects that every previous pack shipped:

1. **124 loaders pointing at nothing.** 62 GROW/LAUNCH decks load `visual-upgrade.css/.js`;
   scope globs `*.html`, so naming a directory IN never carried its runtime assets. The same
   silent failure the Art three were added to prevent — reasoned about there, **missed here, and
   only the crawl found it.**
2. **The `hud.js` strip was half-blind.** Five Science GROW decks load the HUD through a dynamic
   injector, not a `<script src>` tag. The branded copies shipped fetching `hud.js` at runtime.

Broken references **151 → 25**; scope **280 → 286**; `hud_stripped` 170 → 175; hud.js in both
assembled trees **0**. The residual 25 are classified: **20 are root-absolute `/grow-anim/*.js`
that no pack scope can fix** (the fix is a lesson-file edit, not taken), 5 are deliberate
out-of-scope links.

Validation: 0 attr / domain / UPPERCASE / `contactmadebymatt@` / decoded-base64 residue · 276/276
x-brand · 0 truncated · **586 inline JS blocks, 0 syntax errors** · 0 iframes · 2/2 assessed
blocks intact · 31/31 AVL marker pairs byte-preserved · 276/276 Network Library index entries
resolve inside the zip · 0 Planning/ and 0 pupil sheets in any zip · `unzip -t` clean ×3.

**SL and SBX are unmerged** — verified against the remote, both at their recorded tips — so the
README stamps "rebuilds after merge day (29 Aug)".

## §R · Invariants, re-emitted at close

- **★ ASSESSED PAIR — 0 bytes of diff:** `GROW_HUM_W7` `a5545585ca28bbba01b55476abb73a9b0819bcc7` ·
  `LAUNCH_HUM_W7` `eb14d6104b94503d0e7ec0a99565ef116a333a57`
- **Frozen legacy unchanged:** `biology` `2fdbd43a3bb20bf2fc76c82260029594fad2834b` ·
  `chemistry` `c60a17078bc6b222beb0e6abd6487e2b44381257` ·
  `2 Physics 10` `57be7374873444ed93b2a65042c0a5f5339cb810`
- **The 25 hidden science witness sheets: byte-pristine.** No restore, no un-hide, no edit to any
  hide comment. Row 17 remains the authority; the restore still waits on Cheryl.
- **`claude/semh2-claims-accuracy` present at `0c0f0487`, not merged, deleted, rebased or swept.**
  *Recorded because a first check said ABSENT and was wrong:* the `--depth 1` clone's refspec is
  `+refs/heads/main:refs/remotes/origin/main`, so `git branch -r` is blind to every other branch.
  **A RED-line branch is verified against `git ls-remote`, never against a single-branch clone.**
- **Never-merge list intact:** `pass-sl-sow-launch` at **`2a1cfda`** — exactly the recorded SHA —
  and `pass-sbx-art-a2` at `462cfa6`. Neither merged. **No branch deleted** (83 remote heads).
- **No printer hold released** (#35 art print · influence-board banner · tk1-access-2).
- `Science_Teesside/visual-learning/` **still BLOCKED — DO NOT MOUNT**; zero lessons load it.
- **Open item 39 not taken** — it belongs to the Estate Visuals session.
- **Zero pupil data** in any commit, PR body, report or committed file. **No © ASDAN PDF entered
  git** — 0 PDFs in the band-A diff.
- **No clip, embed or media URL wired into any lesson.** The media register landed as a candidate
  register only. **No third-party image or artwork committed** — the 85 SVGs were verified original.
- **No closure marker moved**; no new pupil-facing warrant; no second next-step, backlog or
  failing-reflection state created.
- **No rollback recipe run. No force-push. No deployed history rewritten.**

---

# SESSION L2 — ASDAN visual learning: clear the blocker, then mount, 2026-08-05

Sentinel `session-l2-2026-08-05`, revision 1. **Nothing merged this session, and that is the
finding, not a shortfall.** Every figure derived at the SHA named beside it.

## §0 · Gates

Identity **10/10** (the seven markers plus the toolkit, its README blocker and the engine).
This session ALSO opened in the site working directory; the Lessons repo was attached and the
gate run against it before anything else. **The twelfth mis-open did not happen.**
Base expected at/beyond `d421b38`; derived `d421b38`, equal to `origin/main`.
Sentinels **50 / 98 over 548**, raw and R-E08 identical, unmoved at close.

**A capability that changed the session.** Session L recorded no browser. This container has
Chromium at `/opt/pw-browsers/chromium-1194` and Playwright installs against it without a
download. **The vendor's withheld post-integration regression was therefore runnable for the
first time** — in a real browser, including `emulateMedia` for reduced motion and print at
718x1047. Every claim below is a real browser run or git truth. No live page load of the
public site is claimed; the proxy denies egress (verified, see item 4).

## §J1 · The four blocker items, derived from the README and engine, not from the order

| # | Item | Outcome |
|---|---|---|
| 1 | The vendor's decisive gate is unrun | **RUN — and it is RED.** See §J2. Does not clear |
| 2 | Reduced motion in CSS but not JS | **CLEARED** at `cc4f6fa` |
| 3 | The six D&T decks are not on this chassis | **RESOLVED BY EVIDENCE** — true of the compiler, not of the staff route |
| 4 | `docs/MEDIA_REGISTER.md` is a candidate register only | **PARKED.** Holds back **zero decks** |

**Item 2, cleared.** The notice said "no matchMedia and no change listener". True — the
engine's only `matchMedia` occurrence was inside the blocker comment. The defect was more
specific than the notice: `.asvl-static` was driven **solely by a manual "Static diagrams"
button**, so with the OS preference on, CSS suppressed motion while the control still reported
`aria-pressed="false"`. Fixed on the pattern of `art-visual-learning.js`, which carries the
identical repair. The OS is a **floor, not a default**: while the machine asks for reduced
motion the button cannot turn movement back on. Proven in real Chromium, 9 checks, both
directions plus a live mid-session change. `asvl-attention` classified as **RM-3** in the same
commit — the toolkit's only `@keyframes` family.

*Instrument correction.* The first can-fail control stubbed only `addEventListener`. The
engine's `else if (motionQuery.addListener)` fallback then registered via the legacy API, the
listener stayed live, and **the control passed when it should have failed.** Both paths must be
removed. A vacuous control is worse than none; this one was about to sign off a reduced-motion
claim.

**Item 3, resolved by evidence.** `Build/Slideshows/BUILD_DT_W1..W6` carry **0** `ASDAN-TEACH`
markers and the compiler globs `BUILD_ASDAN/*/*.html`, so the claim is true **of the compiler**.
But the staff organ is present and byte-identical in shape to the compiler chassis's:
`onclick="document.getElementById('exit-slide').classList.toggle('show-ans')"` with the eye
glyph. So a D&T deck is eligible to mount by authored per-file integration, which is what the
vendor's own `integrate.py` does for exactly these six paths. **No organ was improvised.**

**Item 4, parked — and it holds back nothing.** The stated reason is network, and the stated
reason **holds**: `www.gov.uk`, `www.nhs.uk` and `www.asdan.org.uk` all return HTTP 000 and the
agent proxy logs `connect_rejected` / 403 to CONNECT. No URL can be resolved here. But
`lesson-payloads.json` contains **0 external URLs** and **0** iframe/embed/YouTube references,
so no mounted surface depends on the register. It gates **no deck**. Under RED 13 it stays a
candidate register whatever a future session resolves.

## §J2 · Band B — mounted, fully gated, and HELD at `ce0a654`

Four specimens: BUILD `CAREERS_W1_My_Strengths` (compiler chassis, materialised), GROW
`PEQ_W1_Knowing_Myself`, LAUNCH `PEQ_W1_Intro_and_Choosing_My_Level`, D&T
`BUILD_DT_W1_Workshop_Audit`. The vendor's block builders were imported and called with the
registry restricted to the four; every other deck on the shared layer loads the engine, finds
no payload for its slug and `autoMount()` returns null.

**Green:** smoke 26 checks PASS · label-rest PASS x4 · reduced motion all green with its
can-fail · print at 718x1047 clean on all four, panel `display:none` in print so it creates no
print obligation and no failing state · **`#print-witness` byte-identical in 31/31 BUILD decks
through materialisation**, with a tampered-copy control proving that check can fire · marker
confinement asserted per file before and after write · sentinels unmoved, per-file
closure-marker counts unchanged in 38/38 · protective scans all zero-introduced (`moderation`
34 in base, 34 mounted, **0 introduced**).

**Red, and it holds the mount:** the corrected contrast gate reports FIX-verdict rows **3 → 12**
across the four specimens — **9 introduced**, all marginal at **3.94 to 4.49 against 4.5**. They
split in two: **4 rows are `p.asvl-eyebrow`, the pathway identity hue** (the same gate verdicts
identity hue as "left" on base decks; changing a pathway's identity colour is Matt's call), and
**5 rows are one token, `--asvl-muted` `#64748b`** — a one-line legibility fix, not an identity
change. The three `"Success looks like"` rows at 2.0 / 2.14 / 2.58 are **pre-existing**, present
unmounted, and are not this mount's doing.

A `--asvl-muted` darkening was attempted and **reverted rather than left half-applied**: the
re-integration aborted on a first-mount-only assertion so it never propagated, and the measured
numbers were unchanged. The toolkit is committed exactly as the vendor shipped it.

## The gate defect this session found — `d335e4f`

Running the decisive regression for the first time found a defect **in the estate's own
contrast gate**. `contrast_check.js`'s `parse()` regex-scraped numbers out of a computed colour
and assumed 0..255 channels. CSS Color 4's `color(srgb r g b)` carries **0..1** channels, and
Chromium serialises every `color-mix()` result that way. The ASDAN layer uses `color-mix()`
throughout, so a near-white mint `color(srgb 0.963451 0.985569 0.971608)` was read as
effectively **black**, and legible dark-slate text on it scored **1.42:1**. The true ratio is
**14.05:1**.

Uncorrected it would have held a correct mount on a false red — **and it has been silently
mis-scoring every `color-mix()` surface in the estate all along.** Fixed in its **own commit**
with no content beside it, because a content-integrity gate is never touched in the same commit
as content it judges. Proven in both directions: the false red clears to 14.05, an `rgb()`
control is unchanged at 14.68, and white-on-white (1.00) and `#aaa` on `color(srgb .95…)`
(2.08) **still fail** — a correction, not a mute. Measured on the **unmounted** tree it changes
**nothing** (69 below target, FIX:3, identical), so it is not tuned to the content that exposed
it.

## §J3, §J4 · Not reached — parked with their blocking condition

- **J3 band C.** Not started. Blocked by the same contrast ruling as band B: batching the
  remaining 81 decks would multiply a finding that is still awaiting a decision. Nothing was
  materialised beyond the four specimens.
- **J4, the 20 root-absolute references.** **Not reached.** No file was touched, nothing was
  derived beyond Session L's existing classification. It needs the live-origin evidence step
  (does the target resolve on the deployed site) that this container cannot supply directly —
  the proxy denies egress — so it wants either CI or a session with different network policy.

## §R · Invariants, re-emitted at close

- ★ assessed pair `a5545585ca28bbba01b55476abb73a9b0819bcc7` /
  `eb14d6104b94503d0e7ec0a99565ef116a333a57` — 0 bytes of diff
- Frozen legacy `2fdbd43a` / `c60a1707` / `57be7374` — unchanged
- The 25 hidden science sheets byte-pristine; no restore, no un-hide
- `claude/semh2-claims-accuracy` present at `0c0f0487`, not merged, deleted, rebased or swept —
  **verified against `git ls-remote`, never against this single-branch clone**
- `pass-sl-sow-launch` at `2a1cfda` and `pass-sbx-art-a2` at `462cfa6`, neither merged; no
  branch deleted
- No printer hold released · `Science_Teesside/visual-learning/` still BLOCKED · open item 39
  untouched · zero pupil data · no © ASDAN PDF in git · no media URL wired · no third-party
  artwork · no closure marker moved · no force-push, no rollback recipe, no rewritten history

## For the next session, and for the 29 Aug pack slot

**`REBRAND.md` pack scope must gain the newly-mounted ASDAN runtime assets before the next pack
build** — on the same loader-resolves-inside-the-pack gate that PACK-2 applied to the GROW and
LAUNCH `visual-upgrade` files. It is stated here and deliberately **not** acted on: no pack was
built this session. The 29 Aug rebuild slot inherits it.

---

# SESSION L2 CLOSE — ruling applied, band B merged, band C stopped at batch 1

Sentinel `session-l2-close-2026-08-05`, revision 1. Base `d421b38`.

**Capability probed, not inherited.** Chromium **141.0.7390.37** launches here and `emulateMedia`
works; the live origin does **not** (`madebymatt.uk` returns HTTP 000). Session L had no browser,
L2 did, this one does — **three consecutive containers, and the honest report differed each
time.** The rule is now explicit: **browser capability is probed per session, never inherited.**

## §1-2 · The darkening ruling — applied, band B MERGED at `068252d` (PR #63)

`--asvl-accent` is **not** a toolkit pathway token: it inherits from each host deck's strand
palette. Darkening it directly would have moved the estate's strand colours, which the ruling
forbids, so toolkit-owned derived tokens were added instead:

    --asvl-accent-text: color-mix(in srgb, var(--asvl-accent) 91%, #000)
    --asvl-muted-text : color-mix(in srgb, var(--asvl-muted)  96%, #000)

Mixing toward black scales every channel equally, so the **hue angle is preserved exactly**.
Those are the **minimum** shifts clearing 4.6:1 for the sampled accents and tints. Rendered on
the mounted specimens: BUILD **5.08** · GROW **4.63** · LAUNCH **4.76** · D&T **5.08**. Both
directions: the old values still fail (3.94 and 4.34), the new pass.

**Propagation was proven on rendered specimens, and the first attempt was inert.** Changing the
`--asvl-muted` *fallback* did nothing — the host decks define `--muted` themselves, so it never
fired. Reading the token file would have certified a change that had not happened. **Second
time this exact trap has been caught in this workstream.**

Band B gates at the merged tip: contrast FIX **12 to 3** with the 3 remaining **pre-existing**
(**0 introduced**) · smoke 26 checks · label-rest 4/4 · reduced motion all green incl. the live
mid-session change and its can-fail · print 718x1047 4/4 · `#print-witness` **31/31**
byte-identical with a fired control · **0** files with text changed outside a marker-owned block
· sentinels 50/98/548 unmoved before and after the merge.

## §3 · Band C — batch 1 MERGED, batch 2 STOPPED, batches 3-4 not attempted

**GROW (18 decks) — green, merged.** GROW decks load `visual-upgrade.js` externally, so the
batch changed **two files and zero lesson files**. Baseline-differenced: contrast FIX 5 to 5,
smoke FAIL 3/3 both sides, label-rest PASS 1 / FAIL 2 both sides — **0 introduced anywhere**.
The smoke failures are structural: GROW decks are not on the BUILD `ASDAN-TEACH` framework, so
that gate does not apply to their chassis.

**LAUNCH (30 decks) — RED, batch stopped and reverted.** Two introduced classes:
`p.asvl-eyebrow` at **3.25**/4.5 on decks where band B's LAUNCH specimen read **4.76**, and
`span.asvl-sequence-number` at **4.06** x7, a class no band-B specimen exercised.

**The cause, derived rather than guessed.** The accent is *identical* across these decks
(`#A76A9B`), so the variance is not in the accent. It is in the **header gradient's
`--asvl-accent-soft` tint**, which inherits `var(--wedo-bg, ...)` and **differs per deck**. The
eyebrow sits on a different background per deck, and **a fixed-percentage darkening of the text
cannot guarantee a floor against a background that moves.** That is a design decision beyond a
minimum-shift ruling, so the batch was stopped and reverted rather than forced. **Nothing from
it is on main.**

**BUILD (31) and D&T (6) — not attempted.** They inherit the same unresolved question, and
attempting them would multiply an undecided finding. Parked by name.

## §4 · Notice hygiene

The standing notice was rewritten **in the same commit** as the band B state change: items 1-3
cleared/resolved with SHAs, item 4 parked and gating nothing, band B named deck by deck. The
**BLOCKED wording remains and says explicitly why** — band C is outstanding. It comes off only
when C completes; a blocked banner on a fully mounted toolkit would be the co-present
contradiction this estate treats as a signature defect.

## §5 · J4 — parked, with the probe committed ready to run

The proxy denies the live origin, so the (a)/(b)/(c) classification cannot be completed here.
`.github/workflows/j4-absolute-ref-probe.yml` is committed **unrun**: a read-only
`workflow_dispatch` job that derives the root-absolute references from the decks themselves,
reports in-repo existence and live HTTP status for each, and changes nothing. **No reference was
touched this session.**

## §6.1 · HOUSE RULE — the contrast parser cuts BOTH ways

`color(srgb ...)` channels are **0-1**, and Chromium serialises **every** `color-mix()` result
that way. A 0-255 parser reads those numbers as near-black. That manufactures **false REDS** on
dark-on-light text — which held a correct mount for a whole session — **and false GREENS on
light-on-light text**, because a light colour misread as near-black scores *high* against white.
**The second is the dangerous direction: it certifies unreadable text as passing.**

**Every prior contrast certification over a `color-mix()` or `color(srgb ...)` surface is
therefore unsafe in both directions.** Fixed at `d335e4f`, in its own commit with no content
beside it, proven in both directions, and a **no-op on the unmounted tree** (69 below target,
FIX:3, identical) so it is not tuned to the content that exposed it.

**Follow-up, scoped and NOT run here.** Estate member set, derived by grep over tracked files:
**`color-mix(` appears in 43 files and `color(srgb` in 1.** That is the exact set
whose contrast certifications must be re-run with the corrected instrument. Queued, deliberately
not boiled this session.

## §6.2 · Fired-fixture — the RM control that passed via a legacy fallback

The reduced-motion can-fail control first stubbed only `addEventListener`. The engine's
`else if (motionQuery.addListener)` fallback then registered via the legacy API, the listener
stayed live, and **the control passed when it should have failed** — it would have certified the
reduced-motion fix on no evidence. Both registration paths must go for the stub to be a real
negative. Fired-fixture family, alongside the merge-commit `--name-only` entry.

## §6.4 · The 29 Aug inheritance, restated

**`REBRAND.md` pack scope must gain the mounted ASDAN runtime assets before the next pack
build** — `GROW_ASDAN/visual-upgrade.js` and `BUILD_ASDAN/_framework/asdan-teach.css` and `.js`
now carry the toolkit, and `LAUNCH_ASDAN/visual-upgrade.js` will when batch 2 lands — on the
same loader-resolves-inside-the-pack gate PACK-2 applied. Stated; **no pack was built here.**

## §R · Invariants at close

Assessed pair `a5545585…` / `eb14d610…` · frozen legacy `2fdbd43a…` / `c60a1707…` /
`57be7374…` · sentinels **50 / 98 over 548** unmoved across both merges · the 25 hidden science
sheets byte-pristine · `claude/semh2-claims-accuracy` at `0c0f0487` present, verified via
`ls-remote` · `pass-sl-sow-launch` `2a1cfda` and `pass-sbx-art-a2` `462cfa6` unmerged · no branch
deleted · no printer hold released · zero pupil data · no media URL wired · no third-party
artwork · no closure marker moved · no force-push.

## §5 addendum · J4 — the CI route WORKED, and the park was premature

**Recorded as a correction, not a success story.** J4 was parked with the workflow committed
ready, on the fallback clause "if Actions is unavailable". **I never tested whether Actions was
available.** It was. Triggering the committed `workflow_dispatch` returned the classification
immediately. A park is only honest when its blocking condition has been *derived*; this one was
assumed, and the same discipline the estate applies to grep results applies to capability.

**The probe's result — 9 distinct references, 20 occurrences.** The standing figure of 20 is the
occurrence count and is exactly right: 5 `Science_Teesside/Build` decks x 4 scripts.

| reference | in repo | live origin | class |
|---|---|---|---|
| `/Lessons/` | no | **200** | (c) site root, correct as written |
| `/Lessons/hub-health.html` | no | **200** | (c) live, deliberately out of pack scope |
| `/assets/video/poster-art.jpg` | no | **404** | **(b) dead in both places** |
| `/grow-anim/compat-build-anim.js` | **YES** | **404** | (a) |
| `/grow-anim/grow-anim.js` | **YES** | **404** | (a) |
| `/grow-anim/grow-svg-bio-animals.js` | **YES** | **404** | (a) |
| `/grow-anim/grow-svg.js` | **YES** | **404** | (a) |
| `/hud.js` | no | **200** | (c) the `/hud.js` class |
| `/theme.js` | no | **200** | (c) same |

**The (a) finding is sharper than the standing table anticipated.** Those four scripts exist in
the repo *and* 404 on the live origin, because the site serves this repository under `/Lessons/`.
The root-absolute path was therefore broken in **both** contexts — offline and live — which is
precisely why no pack scope could have repaired it and why PACK-2 was right to decline. One
mechanical change fixes both. Proven twice as the table requires: **20/20 resolve in-repo** and
**20/20 inside an assembled pack**, the latter needing PACK-3 (the four scripts added to scope,
286 -> 290 files) or the loader-points-at-nothing failure would simply have returned. The
assembled pack's broken-reference crawl falls **25 -> 5**.

**(b) reported, not acted on.** `/assets/video/poster-art.jpg` is dead in both places. It is
**not** removed: deleting a reference someone means to fill is a different decision from
repairing a broken path, and removal needs its own word.

**(c) listed, untouched.** `/hud.js`, `/theme.js`, `/Lessons/` and `/Lessons/hub-health.html`
all return 200 live and are deliberately absent from this repo — site-root assets that work on
the deployed site and nowhere else. Correct as written.

---

# SESSION L3 — FINAL LESSONS CLOSE: the chip ruling, 85/85 mounted, the re-score

Sentinel `session-l3-2026-08-05`, revision 1. Base `de30f6f`, opened with 21 of 85 live —
derived, not assumed. Browser probed per session: Chromium **141.0.7390.37**.

## §1 · The eyebrow becomes a chip

The pair was unstable, so the pair was made stable. `--asvl-accent-chip` =
`color-mix(in srgb, var(--asvl-accent) 74%, #000)`; the eyebrow renders on it in white.
**Solid, never translucent** — translucency would re-import the moving background.

**74% supersedes 91%, and the reason is a sampling lesson.** 91% was fitted to three sampled
accents. Sampling properly — 30 decks across every pathway — returns **nine** distinct
(tint, accent) pairs including an olive `#8AA662` far lighter than anything measured before. At
91% the olive chip scores 3.4:1. At 74% both limbs hold for every pair: white-on-chip **4.68 –
7.19**, chip-vs-header **3.94 – 6.06**.

**One truth.** The chip ships in the shared toolkit CSS and applies to all 85. And the eyebrow
was not the only white-on-**raw**-accent surface — it was merely the one whose verdict happened
to be FIX rather than "left — UI chrome". The whole family was searched for and moved:
`.asvl-sequence-number`, `.asvl-independence-steps li::before`, and the button family
(`.asvl-button`, `.asvl-choice`, `.asvl-sort-item`, `.asvl-target-button`,
`.asvl-evidence-card`, `.asvl-hotspot-button`, `.asvl-mini-button`). The buttons would never
have failed the gate — but on the olive deck white on the raw accent is **2.72:1 on a
pupil-facing control label**, and a policy that tolerates it is not a reason to ship it when the
fix is the token already in hand.

**THREE DEFECTS IN THE CHIP GATE ITSELF, found and fixed before it was trusted.** (1) L2
compared an *authored* token string against a *computed* colour and read false on every deck.
(2) L3 walked up for a `backgroundColor`, but the header tint is a `linear-gradient`, so
`backgroundColor` is transparent and the walk sailed past it to a white ancestor — L3 was
measuring chip-vs-white. It now measures the gradient's **darker end**, the worst case.
(3) The transparent-chip stub computed to `rgba(0,0,0,0)`, which the luminance function read as
**black**, scoring white-on-black 21.00 — **the control looked like a pass.** Same family as the
`color(srgb)` parser defect: a notation the instrument did not understand, silently scored as
near-black.

**Print limb, answered rather than assumed:** the panel is `display:none` in print, so the
eyebrow has **no print surface**. Nothing to keep legible. Reduced motion untouched, its gate
re-run green with its control.

## §2 · Band C complete — 85 of 85 mounted

| batch | decks | result |
|---|--:|---|
| GROW (earlier session) | 18 | green, 0 introduced |
| LAUNCH | 30 | **green** — mounted verdicts EQUAL the unmounted baseline exactly (UI chrome 26, FIX 3, identity hue 14), so 0 introduced of any class |
| BUILD | 31 | green; `#print-witness` **31/31 byte-identical** with its fired control |
| D&T | 6 | green; all six carry the staff organ, verified per file. None parked, no organ improvised |

**The vendor's own `integrate.py --check` PASSES for the first time**: *"exact source integration
present · 6 shared sources · 6 direct D&T lessons"*. It had reported partial-integration errors
at every previous tip because every previous state was deliberately partial.

37 HTML files changed vs the session base, **0** with text changed outside a marker-owned block.
Sentinels **50 / 98 over 548** unmoved throughout.

**The BLOCKED — DO NOT MOUNT wording is REMOVED, not softened**, in the same commit as the last
mount. It had become untrue.

## §3 · The 43-file re-score — read-only, and the result is reassuring

The queued member set derives at the session base to **exactly 43 files** (36 HTML). *The set at
HEAD is 48 — the extra 5 are this session's own mount inlining `color-mix()` into more decks, so
the honest re-score population is the pre-mount 43.*

Re-scored with the corrected parser: **6,854 text elements across 36 decks · 648 below target in
74 patterns · FIX verdict = 1.** Everything else is policy-accepted (`left — UI chrome` 317,
`identity hue` 218, `decorative` 112).

**The single FIX row is `h3 "Success looks like"` at 2:1 — and it was already visible under the
OLD parser**, appearing as pre-existing in every baseline this workstream took. So it is not a
false green the defect had been hiding.

**Verdict on the follow-up: the parser defect was real and dangerous in principle — it cuts both
ways and could have hidden light-on-light text — but its practical effect on this estate's prior
certifications is nil.** No repair band was needed. The one row is lesson content, not toolkit,
and is **left for a decision rather than fixed here**.

## §4 · Two records

**(a) `/assets/video/poster-art.jpg` stays.** Dead in both contexts, and that is **intentional**:
it is an owned-pending reference to the art-suite clip that has never been ruled onto a surface.
Recorded here with that pointer **so no future sweep "fixes" it into deletion.**

**(b) The park rule stands, and it guards the brief's author too.** *A park is only honest when
its blocking condition has been derived.* The clause it caught — "if Actions is unavailable" —
was written into the close order itself, and taken on trust rather than tested. Actions was
available. A rule that only ever points outward is not a rule.

## §R · Invariants at close

★ assessed pair `a5545585…` / `eb14d610…` · frozen legacy `2fdbd43a…` / `c60a1707…` /
`57be7374…` · sentinels **50 / 98 over 548** · the 25 hidden science sheets byte-pristine ·
`claude/semh2-claims-accuracy` at `0c0f0487` verified via `ls-remote` · `pass-sl-sow-launch`
`2a1cfda` and `pass-sbx-art-a2` `462cfa6` unmerged · no branch deleted · no printer hold
released · open item 39 untouched · zero pupil data · no clip or media URL wired · no
third-party artwork · no closure marker moved · no force-push.

## Inherited by the 29 Aug pack slot

Both scope items are **already in the builder** and need no further action: the mounted ASDAN
runtime assets, and PACK-3's four `grow-anim` scripts. Restated so the slot does not re-derive
them.

---

# SESSION L4 MICRO — adoption made official, and the last contrast row

Base `2e127cc`. Sentinels 50/98 over 548, unmoved. Browser probed: Chromium 141.

## §1 · The adoption ruling, verbatim

**ADOPTED — a standing part of the BUILD/GROW/LAUNCH ASDAN provision, mounted on all 85 taught
decks, maintained in this repository. Ruled by Matt, 5 Aug 2026.**

Alignment recorded with the boundary intact: *it supports the teaching of the PEQ six skills and
aligns with the estate's audited accreditation claims; it performs no assessment, moderation,
evidence-state or quality-assurance function; no awarding-body endorsement is implied; the
data/evidence firewall document remains authoritative and unchanged.*

Explicitly not done: no public-surface accreditation claim changed (ComSk1-only and the
provisional wording stand), no catalogue entry minted (runtime loaded by lessons, not a
standalone resource), no banner resurrected. The wording carries no literal do-not-mount string,
per the #67 grep-shape lesson.

## §2 · The "Success looks like" heading — and it was NOT one row

**The order expected a single row. Measuring the estate returned 109 failing files.** The
re-score that produced the original figure covered only the 36 `color-mix()` surfaces; the
heading exists in **141** files. Rendered measurement across all of them:

| group | files | before | after |
|---|--:|---|---|
| styled, `color:var(--sc-border)` — nine distinct rendered hues | **85** | **1.86 – 3.02** | **4.72 – 6.33** |
| bare `<h3>`, inherits | 24 | 4.52 | **untouched** |
| already dark (`#1f2937`) | 31 | 13.22 | untouched |

**Bar applied:** rendered 12.48–12.8px at weight 700 — **not large text**, so the ≥4.6 target,
not 3.2. Derived, not assumed.

**The fix:** one constant, `color-mix(in srgb, var(--sc-border) 60%, #000)`, applied to the 85
styled failures. `--sc-border` could not be fixed "once" as a shared token — it is **declared per
deck with nine different values**, and 175 of its 607 uses are `color:` rather than a border, so
moving the token would have moved far more than this heading.

**An error of mine, caught by measuring rather than by arithmetic.** The constant was first
derived at 64% **against white**, and 20 of the 85 still failed at 4.25. These headings sit on a
tinted scaffold background, not white. Re-derived against the **real measured backgrounds** (nine
(bg, accent) pairs), 60% is the binding value; worst case 4.72. **A contrast constant derived
against an assumed background is not derived.**

**The 24 bare files are NOT touched, and that is a RED-line decision, not an oversight.** They
render at **4.52** — above the WCAG AA floor of 4.5, below this order's 4.6 margin — and **the ★
assessed pair is among them**. Touching them would breach the 0-bytes lock. Left for Matt: either
they stay (they pass AA), or the assessed pair needs its own ruling before its 23 siblings can
move. **They cannot be fixed as a group while the lock stands.**

Assessed pair verified byte-identical after the edit: `a5545585…` / `eb14d610…`.

## §3 · Close

This is the last planned commit of the Lessons programme.

**Parked by design:** `docs/MEDIA_REGISTER.md`, a candidate register gating nothing, awaiting
Matt's own checks · `/assets/video/poster-art.jpg`, intentionally pending as the unruled
art-suite clip reference · the 24 bare headings at 4.52, held behind the assessed-pair lock.

## §4 · CLOSING RULING — the 4.52 group stands (Matt, 5 Aug 2026)

Recorded verbatim, and it closes the parked row rather than deferring it:

> **The 24 bare `<h3>` files STAND at 4.52: AA-compliant at the governing 4.5 floor. The 4.6
> margin governs values this programme SET, not values it merely measured; the ★ assessed-pair
> 0-bytes lock outranks a 0.08 aspiration, and no sibling split is made. If the pair is ever
> opened on Matt's word for a necessary edit, the 23 siblings may align in that same sitting —
> recorded as a rider-if-ever, nothing queued.**

**The parked row is CLOSED, not carried.** The distinction the ruling draws is the reusable part:
a margin a programme adopts for its own new values does not retroactively bind values it only
measured, and a byte-lock on assessed work outranks a 0.08 improvement. Nothing is queued; the
rider applies only if that file is opened for a separate, necessary reason.

**Programme parks at close — three, all by design:**

| park | why it stands |
|---|---|
| `docs/MEDIA_REGISTER.md` | candidate register, gates nothing (0 external URLs in the payloads); awaiting Matt's own checks |
| `/assets/video/poster-art.jpg` | intentionally pending the art-clip surface decision; recorded so no sweep deletes it |
| the 24 headings at 4.52 | standing ruling above — AA-compliant, behind the assessed-pair lock |

**THE LESSONS PROGRAMME IS CLOSED.**

---

# §R · POST-CLOSE — acting on the four-pass review (PR #70 / PR #71), 5 Aug 2026

Sentinel `estate-review-pr7071-2026-08-05`, revision 1. Base `4aced082`, derived by
`git merge-base --is-ancestor`, not asserted equal. **The programme stays CLOSED**; this is a
repair-and-record entry against an outside review, not a reopening.

**Identity gate 6/6.** The session opened in the wrong repository — `/home/user/Games`, not
Lessons — and the gate caught it before any write. That is mis-open **#13**, and the first one
caught by the gate rather than by a person. Corrected by attaching the Lessons repo. Branch
presence was read with `git ls-remote`, never `git branch -r`: this is a `--depth 1` clone whose
refspec tracks only `main`, so `git branch -r` is blind. Sentinels re-derived by an independent
byte-level walk over `git ls-files -z '*.html'` using the literal markers `ll-g:loop-mark v1` and
`What I said, and what it changed` — **50 / 98 / 548, overlap 0**, unmoved before and after.
Remote heads **85** (baseline 83; +2 fully attributed to the two review branches).

## §R1 · Evidence verdict on the review

The handover shipped five files and no evidence: its own logs read `GH_AUTH=false` and
`Could not resolve host: github.com`, and its summary says the pass-1/2/3 JSON was "not found"
three times. Checksums verify — of nothing. Against the Actions API, both branches tell the same
story: **13 runs each, 0 green.** Audit branch 11 failure / 2 cancelled; fix-pack branch
11 failure / 2 cancelled.

| pass | state | derivation |
|---|---|---|
| 1 · file audit | **RAN-BUT-UNRETRIEVABLE** | run `31046502663`, artefact `8947410011` (201,297 B) exists and is unexpired to 2026-11-03 — but the blob host is denied by this environment's network policy (`connect_rejected`, 403 to CONNECT). Blocked here, not gone. |
| 2 · browser execution | **UNEVIDENCED** | the fix-pack `runner.log` terminates immediately after "Materialised …"; `validate_applied.py --browser` never emitted a line. Execution never reached the browser stage. |
| 3 · publication wiring | **UNEVIDENCED** | no live-results JSON in any retrievable artefact or log; the review's own summary concedes it. |
| 4 · preserved proposals | **EVIDENCED** | the five patch files, README, MANUAL_REVIEW.md and `validate_applied.py` are all retrievable and were read in full. |

**The blocking condition for pass 1 was tested, not guessed** (R9): the artefact was requested,
the proxy refused the host, and the refusal is recorded above.

## §R2 · The fix pack cannot pass its own harness — for the register

`validate_applied.py` asserts **both** `'id="title"' not in grid` **and**
`count('class="panel-title"') == 3`. Those are mutually unsatisfiable while the patch leaves a
fourth `id="title"` in place — and it does. It also searches for
`<div class="memory-trick">Amylase…`, which patch 0003 never emits; 0003 produces
`class="scaffold-box animate-enter"`.

So the workflow ran **RED by construction** — its last step is a literal `exit "1"` — and the
write-up framed that red as principled evidence-retention. **Same family as the contrast-parser
defect, the vacuous `--name-only` control and the hyphen-truncated link regex already on the
register. Added in the same words.**

## §R3 · What landed

Fifteen lesson/resource files, every change re-authored by hand against HEAD. **The review's
patch files were not used**: three of five (0002, 0003, 0004) fail plain `git apply --check` with
malformed hunk headers needing `--unidiff-zero`, while the shipped README tells the reader to run
plain `git apply` in an `&&` chain — so three would have silently skipped.

| band | file(s) | change |
|---|---|---|
| A | `L4a_Wave_Anatomy.html` | one unmatched `</div>` at 532 removed (markup-only delta −1 → 0). **Cosmetic** — browsers discard it. Hygiene, not a bug fixed. |
| A | `Games/Grid_Chase.html` | Google Fonts query `&` escaped; accessible names on the three unnamed inputs |
| B | `Games/Grid_Chase.html` | `id="title"` appears **4×**, not 3 — menu, pause, results **and the `#board` "TOP RUNS" panel**. All four converted to `class="panel-title"`, plus the single CSS rule. Re-derived before editing: **1 CSS reference, 0 JS references.** The review's patch converted only three and would have left TOP RUNS unstyled. |
| B | `biology/Digestion_and_Absorption (1).html` | `id="indep-timer-display"` ×2 → shared class + a `querySelectorAll` helper; four `getElementById` calls rewritten. One global `indepSeconds` drives both displays in lockstep. Both slides already carried ▶/⏸/🔄, so no control was added. |
| C | same file | the 266-character "memory trick" block moved from after `</html>` to inside `<body>`. **Structural half only.** |
| J2 | 4 catalogued Physics files | the byte-identical 671-character "📋 Exam Technique" box (sha `f626d604…` in all five) moved inside `<body>`, **not rewritten** |
| J3 | `6 Art/Surrealism_Eye_Study_v5.html` | `<div id="print-area">` closed |
| J4 | `BUILD_HUM_W2_History_Detectives.html` | two raw `<` escaped (line 152, "Shows < suggests < proves") |
| J5 | 6 print/poster pages | `viewport` meta added. Nothing pupil-facing was touched to clear a warning. |

## §R4 · Three corrections to the brief, each derived

**J1 is materially wrong, and wrong in the review's own blind spot.** The brief lists seven files
with "duplicates JavaScript actually reads, meaning every instance after the first is dead", naming
`Wrecking_Crew` (`util-close` ×11), `KidsVsStaff_Showdown (3)` (`goBtn` ×9), `Static`, `Lumins`,
`Off_Brand`, `Kids_vs_Staff_v8`. Derived: in every one of those files the hits are **inside
`<script>` bodies — 0 in static markup**. `Wrecking_Crew`'s `utility(html)` is
`…innerHTML=html` — a full replacement, so exactly one `util-close` exists at a time across eleven
mutually exclusive panels. `Lumins`' five `id="again"` are **branches of a single if/else-if
chain** building one `btns` string. A live-DOM probe in Chromium — load, then exercise every panel
function, recording the **peak simultaneous count per id** — returns **peak ≤ 1 for every game id**.
`Kids_vs_Staff_v8` is not in the estate at all.

> **Exactly one file in 548 carries a duplicate id that JavaScript reads: the digestion file
> (peak = 2 at load).** The other counts came from grepping inside JavaScript template literals —
> the same blind spot that produced the `g-mblur` false finding, reached by the same instrument.

**J3 is real but filed backwards.** The unclosed element is `<div id="print-area">` at line 585,
not `#print-ko` at 587 — 587 closes cleanly at 609. Whole-file markup delta was **+1**. The brief
says "Invisible on screen, breaks only the printed pack." Measured, using the file's own `.open`
mechanism: **print output is identical before and after** — same five visible print sections, same
3506px document height, zero modals rendering. The damage was on **screen**: all four modals and
the confetti canvas were nested inside `#print-area`, which is `display:none`, so
`ta-modal` / `cc-modal` / `board-modal` computed `display:flex` and rendered **0×0**. Three
teacher-facing modals — TA Focus, Cold Call, Board — were **dead in class** in a catalogued art
lesson. After the fix all three render. That is a bigger finding than the one filed, on the
other surface.

**J2's live exposure is 4, not 5** — `L2_Voltage_Current_Resistance-1.html` is not catalogued
(`resources.json` points at the clean non-suffixed sibling), verified 0 hits. It is deliberately
left carrying its tail, and the validator asserts that it still does.

J4 (**exactly 2, one file**) and J5 (**exactly 6, all print/poster**) matched the brief exactly.

## §R5 · Rejected and held

- **0004 poster — REJECTED.** `/assets/video/poster-art.jpg` is untouched. This entry recorded it
  as intentionally pending *"so no future sweep 'fixes' it into deletion"* — **this review is that
  sweep.** No placeholder SVG stands in for a real YouTube clip (`data-yt="vhuk-K_wWas"`) on a
  public marketing surface. The principle is kept and nothing else: `index.html:351` references it
  **absolutely** as `/assets/video/poster-art.jpg`, and the site serves this repo under
  `/Lessons/` — so **if a real poster ever lands, that reference must become relative.** Parked,
  Matt's call, no edit made.
- **0005 `g-mblur` — FALSE FINDING.** Derived: **10 of 10** Science Teesside files both reference
  `g-mblur` and define `ensureBlurFilter()`, which builds `<filter id="g-mblur">…` as a JavaScript
  string, appends it to `<body>` and is called from `GP.init()`. The reduced-motion path already
  forces `.g-blur-fast{filter:none!important}`. Applying 0005 would delete a working feature.
  **A static grep cannot see an identifier defined inside a JS string** — the exact blind spot
  PR #70's description claims to have corrected.
- **PR #71 — never merged, and unmergeable as it stands.** Enumerated: it changes **no lesson
  file**, only `review/estate-fixes/**` and a workflow.
- **PR #70 — held on competence, not safety.** Left alive and unmerged.

## §R6 · Parks, each with its blocking condition derived

| park | blocking condition (tested) | owner |
|---|---|---|
| Band C placement of the 266-char memory trick | `body{overflow:hidden}` is present, so the block is **not visible today** — confirmed. The loss is teaching content, not a rendering glitch, so placement is a teaching call. Three candidates: **L1 Enzymes & Bile** (defensible), **L1 Carbohydrases I-Do** (sharpest — the content is Amylase→Maltose→Glucose), **L1 exit**. Structural half done; nothing else changed. | Matt |
| `/assets/video/poster-art.jpg` | file absent on disk; reference live at `index.html:351` and **absolute** under a `/Lessons/` base path | Matt |
| Band E pre-init hardening | before `ensureBlurFilter()` runs, `filter:url(#missing)` makes elements **not render** in Chrome and Firefox, so a blank flash is possible. Optional: gate the `@supports` block behind a class added *after* injection. One specimen file. **Proposed, held, not merged.** | Matt |
| PR #70 adoption | held until it can resolve identifiers defined inside JS strings, prove counts by enumeration, and run its own validation green | Matt |

## §R7 · The instrument

`review/estate-exec/validate_estate_exec.py` — 15 checks, every count proved by enumeration, all
markup counts taken after `<script>`/`<style>`/comment bodies are blanked. **Because a census that
did not returned 379 files / 6,438 hits for raw `<` — all of it correct `i<n` loop code — and
invented an estate-wide crisis.**

`--self-test` copies the estate to a scratch tree and tampers it to break each check in turn,
asserting the check goes red. **Live 15/15 pass · tamper 15/15 caught.** The self-test earned its
keep immediately: it exposed three of its own tampers as too weak — a first-occurrence-only
replacement that left the file still matching, a reverted markup change with nothing left reading
it by id, and `g-mblur` → `g-mblur**X**`, which still contains `g-mblur`. **Each was a defective
tamper, not a vacuous check, and each was fixed and re-proved rather than asserted away.**

**The estate is not declared clean.**

---

# §R-close · CLOSE ORDER executed — place, merge, close (6 Aug 2026)

Sentinel `pr7071-close-2026-08-06`. Base ancestry re-proved before any write (`4aced082`
ancestor of `origin/main`); identity gate ran first, as precedent from the mis-open catch
requires. This is the close of the post-review work, not a reopening: **the programme stays
CLOSED.**

## The three rulings, verbatim (Matt, delegated to Claude, defaults baked)

> **R1 — Memory-trick placement: the L1 Carbohydrases I-Do slide.** Move the paragraph there —
> the point of first encoding, teacher-modelled. The L1 exit slide gains a one-line RETRIEVAL
> PROMPT that tells pupils to use the trick ("What was our amylase trick?") — a reference, NOT a
> second copy of the paragraph (one truth: the trick's text exists exactly once in the file).
> Preserve the paragraph's wording as committed; placement only.

> **R2 — After #72 merges: close #70 AND #71 unmerged as superseded.** Branches retained, one
> comment each: #71 — every valid finding re-authored natively in #72; the rejections (poster
> 0004, g-mblur 0005) are recorded in the LEDGER with reasons; merging it would change no lesson
> file. #70 — held on competence, not safety: adoptable as standing tooling only when it resolves
> JS-string identifiers, proves counts by enumeration, and runs green (13 runs, 0 green as of this
> close). Its process discipline is acknowledged in the comment.

> **R3 — The four parks stay parked exactly as recorded.** Poster: owned-pending per the LEDGER,
> must be RELATIVE when real art lands, no action. Band E pre-init hardening: folds into the next
> Lessons maintenance pass, not its own session. No sweep may "fix" either.

## As executed

- **R1 landed** in commit `f70cacb` on the #72 branch: the "Amylase Makes Maltose, Maltase Makes
  Glucose" paragraph moved from the end of `<body>` to sit directly under the Carbohydrases enzyme
  box on the **L1 – I Do: Enzymes** slide. The L1 exit slide gained a retrieval **reference** —
  *"Before Q1 — what was our amylase trick?"* — which does **not** repeat the paragraph text.
  Proven: trick wording appears **exactly once** in the file; nothing after `</html>`. Validator at
  tip: **15/15 live, 15/15 tampers caught** — no expectation orphaned.
- **#72 merged** into `main` as **`e77ab687`**. Main's head is that merge SHA and nothing else
  moved it. Merge authority was for #72 only.
- **R2 executed:** #71 and #70 both **closed unmerged**, one comment each (posted before close),
  **both branches retained** at `3f246dd6` / `10a4195c` — confirmed via `ls-remote`. Nothing
  deleted.

## For the register — two instrument lines

- **(a) Rendered measurement beats static structure analysis.** The Surrealism `#print-area`
  `<div>` was misdiagnosed by static reads on **both sides** of the review — the fix pack filed it
  as print-only; the first execution pass first read it the same way — and its true effect (three
  teacher-facing modals rendering 0×0 on screen, print unaffected) was settled only in a real
  browser. When a structural defect can change what renders, measure the DOM; do not rule from the
  source text alone.
- **(b) Source-level duplicate IDs are not DOM duplicates.** Template-rendered screens hold one
  instance at a time; six of the seven flagged game files had peak simultaneous count ≤ 1 in the
  live DOM. Enumerate in the DOM before counting a duplicate-id defect — a grep of the source
  counts template branches, not co-existing elements.

## The parks — still parked, and the honest open ledger

| park | state at this close |
|---|---|
| `/assets/video/poster-art.jpg` | owned-pending; **must be a RELATIVE path when real art lands** (site serves under `/Lessons/`). No action this session. |
| Band E pre-init hardening (`filter:url(#missing)` blank-flash) | folds into the **next Lessons maintenance pass**, not its own session. Proposed-held. |
| Band C placement | **CLOSED by R1** — the one park this order resolved. |
| PR #70 adoption as standing tooling | held on competence; three capabilities named in the #70 comment. |

**Expected residue, stated honestly:** the poster (awaiting real art) and Band E (next maintenance
pass). Neither is a defect left unfixed; each is a decision deliberately deferred, with its
condition recorded. **The estate is not declared clean.**
