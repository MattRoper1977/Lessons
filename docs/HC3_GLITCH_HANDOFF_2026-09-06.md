# HC3 Glitch Clash save handoff — resumed 2026-09-07

Historical candidate description; status superseded: receiver and sender are now released, as documented in the dated appendix below. Supersedes the unsafe localStorage-writing receiver at 1e9578202a42b123f0731bfc7094871ed4ef32aa; that checkpoint remains in Git history. Current-main rollback: 5da7f04df02de0d775a96cbb77399d8c15ad1109. One game source file. Science packs and their owned gate updates are excluded.

The native raw JSON import/export format and existing engine remain. A fragment import now creates a separate campaign in the same-origin native IndexedDB database `mbm_glitchclash_imported_campaigns_v1`. Nothing writes or removes the legacy `glitchclash_save` through this imported-campaign path. Old open tabs therefore retain their legacy campaign.

An imported writer captures each snapshot before asynchronous work, serializes its own queue, and compares the record revision inside the same readwrite transaction as its update. A concurrent stale writer creates a separate continuation instead of replacing the other writer's record. Only transaction completion reports persistence. There is no compensating deletion. Saved campaigns lists every continuation; a tab keeps its own selection across reload, while a newly opened tab uses the last selected campaign as its default.

Import/switch/reset waits behind a bounded native dialog; queued writes finish before selection changes. Failed writes retain the in-memory state and expose retry/export. Ordinary native file import still opens a temporary campaign when durable storage is unavailable, warns before discard, and permits an explicit retry. URL transport cannot claim success using that temporary fallback. Timed campaign actions are tied to their originating save/battle so changing campaigns cannot transfer an old result to the new save.

Validation in progress: native-format and transaction controls pass locally against the actual inline source and a build-only IndexedDB test implementation. Controls cover missing persistence, concurrent writers, queues, atomic abort, quota/retry, denied/blocked storage, malformed saves, origin/path/size checks and per-tab selection. Phone/desktop Chromium fixtures and all eleven existing native suites must pass at this candidate revision before the hold can be resolved.

Release ordering remains Site reviewed source evidence → compatible education publishers → receiver merge → independent Games pin release with live source proof → education sender enablement. No education stub currently includes this receiver's sender. This one adapter does not close the other native importer formats or the entire HC3 order.


## Published recovery checkpoint — 2026-09-07, 04:20 UTC

**HC3_PARTIAL. This dated section supersedes the earlier receiver/sender holds and pending publisher status.** Earlier unsafe candidates and historical reds remain recorded above. The releases below were merged through their applicable checks and published. This is not an all-route completion claim.

| Serving repository | Published source | Publication run / review artifact |
|---|---|---|
| Site | 0a8fdac899b0d4e7664f51eb885a88d1ae8b26bb | 34079551819 / 10003303669 |
| Lessons | f37fc7414555f0dcb3e70370f957ee63e615ed25 | 34080421165 / 10003551917 |
| Apps | 753baf41f65370f20ef69a4f87999c7f491ce7df | 34080015656 / 10003452922 |
| Games | 9237d177b1f26b8ea0d9b103fe141560f319ad02 | 34077622659 / 10002616183 |

All four publications succeeded. Lessons and Apps now use Site 0a8fdac8 as their immutable publisher while publishing their own source. Games independently pins Site a30088ea8d3380b0c0e6040a361a9c0449450a89 and Lessons 138457849c2690de5413ed80d616725a5160f9d1. Later publisher/documentation commits are not missing game releases. Science release contents and ownership were preserved.

### Safe native save handoff: one released adapter

Lessons #354 merged as 91894c32cb530d82b0adce63d1e6999143ebc13f after its concurrency hold was explicitly resolved. Imported Glitch Clash campaigns use separate IndexedDB records; they never overwrite/remove the legacy glitchclash_save key. Atomic revision checks branch stale concurrent writers, snapshots are captured before queuing, and success waits for transaction completion. Per-tab selection, denied/blocked storage, quota/abort/retry, old tabs, delayed actions and reloads have dedicated controls. The unsafe 1e957820 candidate was not released.

Site #284 supplies exact reviewed receiver evidence; Games #69 published the safe receiver through the independently generated pin path. Site #292 then merged as 0a8fdac8 to publish /stub-handoff.js and decorate only /Lessons/Games/Glitch_Clash.html. Lessons #361 and Apps #47 published the matching caller revision. The sender reads only the deliberate route's exact legacy campaign key, rereads on activation, does not write/delete source saves, uses bounded fragments or the native JSON file importer, and adds no third-party dependency.

Actual published browser journey: Site run [34079551860, attempt 2](https://github.com/MattRoper1977/mattroper1977.github.io/actions/runs/34079551860/attempts/2), job 101615313821, artifact 10003623098, 481454437 bytes, SHA256 2399d16cbac5cead1f09010a2e2b8be6328e788ab6d26398912773fa3b0f961d. Root downloaded the archive, matched its digest and read handoff-publications.json plus every row of proof/handoff-live.json. The report says PASS, expectedCases=10, completedCases=10: fragment, empty origin, latest-at-click save, large native file and rejection at widths 390 and 1280. Every row has no console errors or unexpected requests; applicable rows preserve source and destination legacy data, consume the fragment and survive reload. Tests use the genuine served button/importer, real Tab/Enter controls and actual component hashes. No response substitution or injected alternative importer is used for this journey.

The apex education origin is SERVED with real/planted-byte/restored control PASS/FAIL/PASS. https://www.madebymatt.uk is explicitly UNAVAILABLE_ORIGIN: HTTP301 redirects to the apex before same-origin storage can be read. No storage was seeded/read there and recovery of saves held on that old origin is not proved. This is not silently counted as another successful origin.

Component SHA256: sender a92bc47354724fbd9b53e25d219ddaed29755a98988c3db7fac49fc7f488b639; 1353-byte stub 68190ef68b33986db42c8ae55a8c4a0458b6e58ac399dafbad3cbb2cb16a3c7c; published receiver e07efa965aa7ced5c1b2db06d01a846d8fa709e1c47529b4b6fe8f9b56484397. Publication artifacts have the exact three source/run/attempt/upload/deploy receipts listed in the archive. Attempt 1 correctly rejected the older Lessons stub; it is not green evidence.

Earlier receiver phone/desktop concurrency fixtures and all eleven existing native suites passed. Separate real-origin native fragment/file/rejection artifact 10002774552 also passed six cases. The final archive contains screenshots; the workspace execution/file service failed after JSON review and before their visual inspection. Browser assertions are proved; independent visual review of those final screenshots remains pending. A read-only reviewer independently confirmed the final job's command, exact publications, successful execution and uploaded digest from CI logs.

Other native adapters remain unfinished: Emberwild, Global Games V4, Apex Kick, Lumina Haven, Aurora Links V4 and Touchline require their own safe integrations. Titan Forge and Biopunk have native text formats incompatible with the order's oversized-JSON fallback. Town Life remains owned by Site #216. Passport/ghost-only imports are not full campaign importers. Existing bulk transfer is preserved. One adapter does not close §6.

### Inventory and publication identity

Site #293 repaired source identity; Site #297 preserves both the prior identified schema-2 report and the newly generated released inventory, alongside the original historical schema-1 report. Files: HC3_SAVE_INVENTORY_RELEASED_2026-09-07.json, HC3_SAVE_INVENTORY_IDENTIFIED_2026-09-07.json, HC3_SAVE_INVENTORY_RELEASED_SUMMARY_2026-09-07.json and HC3_SAVE_INVENTORY_PUBLICATION_BINDING_2026-09-07.json.

The fresh report is keyed by page route and anchored to Site0a8fdac8 / Lessons13845784. It contains 69 routes, 67 migration candidates, 358 unresolved observations (98 receiver and 260 key), 5953 parser/scope warnings across 49 routes, and 390 resolved route/key candidates. All 69 routes still have unresolved cases; typical pupil save sizes are null. No source script was silently missing. Candidates are not storage permissions.

Root independently compared every one of the 69 built payloads with the digest-verified Games9237 publication artifact10002616183. The source inventory is 1852809 bytes, SHA256 5d2c2beeca1dc229d21b63ce2319f61e53104bee9931d3e4dbde0606bad6d48f; Git blob597de84809e045c5bd94d03e3cb43330db05b478. The prior identified report remains blob9406484989e5f38892ec4a31ad17314299526158. Literal/namespace/prefix/wrapper, shadowing and unresolved-expression controls remain explicit. Built-byte and source-identity defects fire red and restored trees pass.

### Strong education publication and support boundaries

Site #289 merged as ef6574547cc5d11e0aec36b76e25b2e681152ce7. Final publication admission is an exact reviewed path-and-byte ALLOWLIST after coarse source filtering; adding a manifest row does not admit new bytes. Unknown, changed, missing, symlinked or disguised content fails. Forty-nine controls and an ordinary built-tree planted-game rejection passed. The composed sender build contains 2503 admitted files (Site188, Lessons2209, Apps106), 1366 HTML pages and 18384 checked references, with zero separation failures. This build measurement is not a whole-estate served runtime census. The existing four-link stubs still do not satisfy the strict one-link wording; no copy/link removal was hidden inside this save release.

count_marker.py and LESSON_ADULT handling are retained. The support report covers 1366 HTML pages, 145 generated footers, 499 reachable rows and 461 reachable nonadult rows. Adult Science Teaching_Packs and Humanities David_Cover each retain one intended configured link/footer; pupil Science/Humanities hubs have none. Root, Lessons index and Apps index have zero generated footers but retain seven source text occurrences comprising five Ko-fi links. They are owned by Site #25, Lessons #93 and Apps #2. Literal zero pupil/shared-page references is false; the check's held-record allowance must never be reported as literal zero. No source or builder workaround bypassed ownership.

### Deck, link and zoom residue

The machine-readable Site HC3_DECK_RESIDUE_2026-09-07.json names 16 alternative GROW/LAUNCH Humanities W1–W8 resource routes, exact source hashes, line numbers and proposed objective changes. They contain 48 print/screen duplicate IDs. No deck in that batch was edited or counted fixed. The contained proposal namespaces three print IDs and their three references per deck, preserving text/scripts/styles; it still requires its own ≤12-deck PRs and actual open/print/navigation proof.

Baseline limitations are separate: all eight GROW decks have no way-home anchor, phone CSS hides the TA control, and native print emits the tier worksheet while hiding the nine-slide deck. Do not fabricate a nine-slide print or phone TA proof by injecting CSS/controls. Full current pathway/deck and link-census counts remain null. The previously published statistics skip/canonical fix is complete as recorded above.

Merged viewport/touch corrections are preserved. Site #291 remains HELD at ea0876b2453c3a67c0dd883e3078ed54b4098aa7: the reconstructed touch instrument cannot zoom its own unblocked positive control (scale stays 1). Its route verdicts are MEASUREMENT INVALID; the 26 target pinch checks remain unproved, not 26 established defects. Do not repeat the already failed synthetic/headed variants or substitute metadata inspection.

### Weekly findings, automation and historical performance

Site #288 remains HELD at b7e0aaf2981a935fbffec7e87f1abc5495848831. Diagnostic run34078088304 artifact10002798706 (SHA256260765609c719f8a0fcd63c146ef1f3f1518524208945d430929ba691064c19b) names MTR34050355921, published-live34050346276 and pin-release34051249733 attempt5 as red. J4's last success31025606623 is dated Aug5 and stale; one never-run trailer, one retired red and 143 orphan findings remain separate. Current main's weekly workflow has not been made green. Fixes to the old verifier instrument are on main, but rerunning its old YAML would not prove the repaired current instrument. A fresh current-main dispatch/schedule is still needed; no dispatch capability was exposed here. Findings were not exempted away.

Games #67 strengthened independent pin guards; #68 and #69 published the tested source pins without manual pin edits. The workflow's PR-creation step still returns “GitHub Actions is not permitted to create or approve pull requests.” Exact external setting: Games → Settings → Actions → General → Workflow permissions → Allow GitHub Actions to create and approve pull requests. No admin capability was available. Zero game-touching commits were behind the released pins at the last staleness measurement; builder/docs changes are reported separately. Unattended release automation is not claimed complete.

Games #66 recovered all 69 historical raw payload rows from original artifact9990820021/run34038125168 at ec5ee7bb, digest812df7862d087160f2414f1dc311bae696887d4f4015d879de9c19b36ed2a2fe. Total20344993 raw bytes; 16 exceed500000. The original per-route gzip values, 18 quiet-route identities, full19 slow-route list and exact timing harness remain missing after archive/branch searches. Current pin performance and recompression are not substitutes. Historical rAF counts are not browser paints.

### Fresh publication witnesses and execution checkpoint

Lessons FieldOps run34080420720, artifact10003570274, digestb6d0c5f0f99daf52173c9b50f604bdfa94adc0ad82619dee664c39aa52a2bb3e, reports44/44 served subjects, zero red/inconclusive, five firing and thirteen regression controls. It binds all four published sources in the table. This is its named sample, not all69 games or all1366 education pages. Apps LundyLoop run34080015345 attempt2, job101614474715, artifact10003500931 (digest7599faeb3aa4dad56b62304bfd397a499b434ed76e4c582c167dc0995e9dd49e) matches all nine actual live files against Apps753's publication. Its first attempt exhausted a 240-second artifact wait before deployment; it remains historical inconclusive evidence.

The repeated Apps publication-order race has a concrete scheduling plan in Apps #48 and mirrored Lessons #362. Both are HELD plan-only drafts: the workspace exec server began returning “No such file or directory” before implementation, and local files/images became unavailable. No scheduling code or digest changed. Future repair must retain existing byte/provenance gates, trigger only after successful same-repository main publication, select workflow_run.head_sha rather than current GITHUB_SHA, preserve PR/push fixtures, and prove actual hosted order with all nine exact bytes. Both plans contain pre-edit rollback SHAs and their unrun control requirements.

Site #296 merged ef02340025c7038e4fe643899022519648d7c511: the readback script now requires the original byte-witness archive and exact source/run/attempt/job/upload metadata; green job names alone cannot create green counts. Missing complete deck/link/handoff datasets stay null. The previous dated snapshot is historical, not refreshed by this prose. A new script replay with the latest witness remains a saved resume item because execution failed before that final replay.

Lessons #340's unchanged HELD/R12 title/body and absence of explicit resolution comments/reviews remain a documentation discrepancy. Its merged correction and served proof were confirmed; no automatic revert was made.

Resume from the four published sources above and the saved ledger PRs, rechecking main/ownership before edits. First recover final handoff artifact10003623098 screenshots and the local execution venue. Then finish Apps#48/Lessons#362 scheduling, replay tools/hc_readback_counts.py against fresh API/FieldOps evidence, finish unowned objective deck/link batches with their real classroom gates, and resolve the named weekly/zoom/native-adapter residue. Protected PRs and existing branches remain untouched. Documentation-only PRs do not themselves constitute another game release.
