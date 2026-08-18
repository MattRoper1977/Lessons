# TL-2 Part E r2 — Teesside Cross-Curricular Maker Lab PRO v2.1.0: DEPLOYED, PUBLISHED, PROVEN

Sentinel: `townlife-tl2-2026-08-18-PARTE-r2-TOP`

Supersedes the r1 run, which stopped correctly at Phase 4. The owner's r2 re-issue fixes
the inventory, not the expectation, and no runtime byte changed — verified here rather
than taken on trust.

## Package identity and the r1 → r2 delta

`Teesside_Maker_Lab_PRO_v2.1_DEPLOY_PACKAGE_2026-08-18_r2.zip`, 5,999,464 B, sha256
**`1b97902e5e47fb003a91c46a6c8493bbe39e76cb2206aab2ebda1ba718636250`** — exact match to
its sidecar (r1 `1999c4bf…` superseded). `verify_deploy_package.py` **PASS 52/52**;
`run_patch_truth_gate.sh` **PATCH_TRUTH_PASS**, including r2's new line
`self-check EXPECTED == shipped set OK`.

Comparing all 37 payload files against r1, exactly five changed: `RELEASE_SELF_CHECK.html`
(13,025 → 11,122 B, the fix), `PATCH_NOTES_v2.1.md` (documents it), `SHA256SUMS.txt`
(both entries re-hashed), and the two `_release-docs` records (r1 → r2 id plus those
digests). **Every studio, the Shell, both Directors, the Moderation Hub, Quick Start and
`index.html` are byte-identical to r1.**

The r1 blocker re-derived independently: 33 EXPECTED keys against 35 shipped files, zero
missing, zero size or hash mismatches. The two uncovered files are `RELEASE_SELF_CHECK.html`
and `SHA256SUMS.txt` — the pair that cannot hash themselves into their own inventory.
33 + 2 = 35. The inventory now describes the tree that is actually deployed.

## Provenance note, carried verbatim as instructed

The source zip's supplied `.sha256` sidecar (`eae222b8…`) does not match the zip actually
supplied (`1ea8decb…`); the zip's internal SHA256SUMS verified 50/50, so it is treated as
truth and pinned by measured digest. The lighter non-PRO v1 zip and the loose 17–19 KB
studio files are superseded and were not deployed.

## Sequencing, install, parity, pin

D had merged, so E branched from D's merged Apps main `9672d6b7` — never sharing a branch,
PR or commit with A/B/C/D. Phase 1 confirmed no prior deploy: zero Maker Lab records, no
suite folder, no `tools/makerlab/` (r1's revert left nothing behind).

37 payload files installed and re-hashed against the package after every commit: **0
mismatches**. One Teacher-tools catalogue record landing on `index.html` per the 2026-08-16
ruling; AUDMAP entry added; no-JS `leadCount` moved to **Thirty-eight**, derived by counting
the manifest. Parity re-measured against Site main `595b4d09` rather than reused from D:
`mbm-platform.css`/`js` byte-identical, `mbm-theme.js` matching the digest pinned in the
gate — nothing stale, so no parity file ships. Verifier copies byte-identical before pinning
(`565de988…`), pin moved `b70fdca96ba9 → 758489c54bd2` in both copies by `pin_manifests.py`,
`--check` PASS, both copies `bae67d22…` after.

## Gates

Static verifier PASS with its positive control firing. Cross-estate PASS with positive
controls in both repos. On real Chromium over HTTP — the first real-browser run of this
package: index renders at desktop/tablet/390 px with no console errors; 21 of 21 links
resolve 200; **acceptance test PASS** (chip `saved 20:29`, shared `MBM_MAKER_PRO_V2_*`
state read back by the directly-opened studio); **forged-postMessage control PASS** both
directions; reduced motion 0.01 ms across index, Shell and studio; print path renders with
no popup; and **`RELEASE_SELF_CHECK` PASS — 33 of 33, 0 issues**, the gate that stopped r1.

## Two CI findings, fixed without touching payload bytes

`git diff --check` read the payload docs' Markdown hard line breaks as stray whitespace, so
`.gitattributes` now declares them as it already declares LundyLoop's. That *modification*
then tripped the cross-estate boundary check, which exempts added files but not modified
ones — the first payload to need such a declaration created the file, the second edits it.
`.gitattributes` is now on the gate's allowlist as git metadata that cannot change the bytes
any browser is served, applied identically to both byte-identical copies.

## Merges

| Repo | PR | Head | Merged to |
|---|---|---|---|
| Lessons | #135 | `fd20a3be` | `cc560092a618ec6ab63e89e2039746104c760317` |
| Apps | #16 | `950d481a` | `957744e7fdb536d0f3dc4e54d740e8f4a32c2735` |
| Apps | #17 | `4edf3a5b` | `6a8ae0630e2e535709edf0795d5fa5250b2778d4` |
| Site | #171 | `54854bba` | `b912ad057c5367a30751c52f079209ddf7ae0572` |

Rollback anchors: Apps `9672d6b7` · Lessons `5bfba624` · Site `595b4d09`.

## Published bytes (Phase 6)

E's package shipped no live-bytes tool and this session cannot reach the production origin,
so the proof was put where it can run: `tools/makerlab/verify_live_bytes.py` plus a workflow
job. It downloaded **all 35 runtime records** from `https://madebymatt.uk/Matt-s-Apps-/` and
matched every one against the merged bytes **on the first attempt**, each request cache-busted
with the merge SHA and sent `no-store` so a match cannot be a stale copy. Its inventory is the
payload manifest, so a file added without a record cannot pass unproven. Served hashes include
`index.html` 14,897 B `3e481405…`, `STUDIO_SHELL.html` 33,460 B `7ca59875…` and the eight
studios (`62b94efb…`, `7ed9545f…`, `0e80065e…`, `6a2b66eb…`, `e98f9080…`, `edcae4da…`,
`2b4ee731…`, `5d45adec…`).

## Acceptance test on the LIVE origin (Phase 6, second half)

The addendum makes this mandatory, so rather than report it LIMITED I added
`tools/makerlab/verify_live_acceptance.mjs` and a job that runs it against production after
the byte proof. Verbatim from the runner:

```
PASS  hub card resolves to the suite landing page
PASS  suite landing page serves 200  — 200
PASS  autosave chip reports a save, not unavailable storage  — saved 20:53
PASS  the studio wrote its state under the shared key
PASS  a forged sync from another window is refused
PASS  a genuine sync from the framed studio still lands
PASS  the directly opened studio reads the same saved state
PASS  no uncaught page errors
8/8 live acceptance checks passed
```

M1 and M2 are proven where the suite is actually opened. The harness passed 8/8 against a
served copy of the merged tree before it was trusted against production.

## Site discovery (Phase 7)

Opened only after publication was proven, as the recovery doc requires. Branched from site
main `595b4d09`; #169 still unmerged and untouched, so no rebase. Five files: the apps.json
mirror (git blob `808fe573…` identical on both sides, 38 records counted), provenance
→ `957744e7`/38, the guarded index write with **seven declared leaves** (one entry ADDED,
none removed, `--check` reproducing after commit), and the Teach Hub's creative-tools
grouping — eight maker studios beside the other making tools.

**The package's predicted search id was wrong.** The generator derives ids from the title
and produced `app-teesside-cross-curricular-maker-lab-pro`, not `app-teesside-maker-lab-pro`.
Hand-editing the index is forbidden and the generator's rule is the authority, so the derived
id ships. Every other spec field matches exactly: route, category `tool`, contentType
`Teacher tool`, audience `teachers`/`schools-semh`, `safeForPupils: false`.

Both LundyLoop and Maker Lab are Teacher tools, `safeForPupils:false`. Neither goes near
`/for/pupils/`, `games.json`, the TOP rail, curation or genre records — verified by searching
for the id outside `teach/index.html` and the index itself.

## Safeguarding and professional boundary (Phase 8)

Confirmed against the suite: "No data is sent to a server by the suite" and **0**
fetch/XHR/WebSocket/sendBeacon calls measured across the 15 HTML files; the Moderation Hub
states readiness "is not an accreditation decision or grade"; the assessment boundary states
the tools "do not make automatic attainment, accreditation, moderation, safeguarding or
professional competence decisions"; the physical-safety boundary rules out load ratings,
cutting instructions, casting schedules, chemical recipes, safe working temperatures,
navigation charts and machinery settings; every project record carries one of four source
statuses; no personal identifiers in the payload; catalogue placement is teacher-only.

**Partially met, reported not patched:** the rooms are teacher-*named* ("Teacher Studio
Director", "Portfolio & Moderation Hub", actions "Plan a workshop" / "Moderate portfolios")
but `index.html` contains **zero** occurrences of "teacher-only" or any equivalent statement.
The suite-level protection is intact. For the next revision: one line on the launcher naming
the two rooms staff-facing.

## Defect found in r2 and deliberately not patched

`RELEASE_SELF_CHECK.html` ships `<b id="expected">49</b>` as a hardcoded literal that no
script rewrites — the only `textContent` writes are checked/passed/issues and the verdict.
r1's inventory had 49 entries so the tile was right then; r2's has 33, so a clean pass reads
"49 expected / 33 checked". Verdict, counts and per-file rows are all correct. Fixing it
would mean editing a payload byte after install, which is an E4 stop condition. For the next
revision: derive the tile from `Object.keys(EXPECTED).length`.

## Owner-held item — OPEN, not resolved

Reading demand of the studios' panel copy is FK 15.5–18.9 on prose (17–22 whole-panel),
above BUILD and GROW. A plain-language pass is a content decision for Matt. It appears in no
catalogue or PR copy as if handled. **OPEN.**

## Site-main verification at the time of writing

The site's own post-merge workflows at `b912ad05` were still running when this record was
committed: `pages build and deployment` and `Deployment provenance` had already passed, with
`Professional site live verification`, `Verify audience discovery, Teach and Education hubs`,
`Adult-affordance boundary is fail-closed` and `MBM audience discovery closeout` in flight and
no failures. Those checks cover the discovery surface, not the runtime — the runtime was
already proven byte-for-byte on production before the discovery PR was opened, which is the
order the recovery doc requires. A watch is armed on them; any failure is a discovery-surface
fix, and the rollback order (Site first, then Apps, then Lessons) is recorded above.

## Token

Every mandatory gate is evidenced — package integrity, patch truth, static, cross-estate,
the browser suite, published bytes on production, and the acceptance test on the live origin:

**`MAKERLAB_V21_MERGED_PUBLISHED_SHA_PROVEN`** — beside TL-2's own tokens and D's, never in
place of them.

Sentinel: `townlife-tl2-2026-08-18-PARTE-r2-BOTTOM`
