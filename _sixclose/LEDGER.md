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
