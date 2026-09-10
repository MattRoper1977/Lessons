# SX2 — Decisions record

Order SX2 (2026-09-09), written at the time, per the `_eca1`/`_glv3` convention.
Phase S: finish SX1 and get the Spring/Summer Science batch served.

**This file is generated.** One ruling per file in `_sx2/decisions/`; a landed
decision file is never edited. Add a ruling by adding a file, then run
`tools/decisions/build_index.py`. `--check` reds if this index and that directory
disagree.


| # | ruling | summary |
|---|---|---|
| `0001` | [Merged, with rollback SHAs](decisions/0001-merged-with-rollback-shas.md) | \| repo \| PR \| merged \| rollback \| |
| `0002` | [D1 — The publisher reads the admission registry from the BUILDER CHECKOUT, not Site main](decisions/0002-d1-the-publisher-reads-the-admission-registry-from-the-build.md) | This is the entry to read before touching publication. It is not obvious from |
| `0003` | [D2 — The apps caller pin was a mid-PR state, never on main](decisions/0003-d2-the-apps-caller-pin-was-a-mid-pr-state-never-on-main.md) | PUBLICATION_CALLER_SHA256_BY_KIND"apps" held c420519111f6: the Apps caller |
| `0004` | [D3 — Re-freezing the retained usage-registry baseline](decisions/0004-d3-re-freezing-the-retained-usage-registry-baseline.md) | check_education_separation.py freezes the digest of the rows |
| `0005` | [D4 — Part R builds the target pin-mover (Order SX3 amendment A1)](decisions/0005-d4-part-r-builds-the-target-pin-mover-order-sx3-amendment-a1.md) | tools/easter/SCIENCE_ORIGINAL_TARGETS.json pins 25 lessons by |
| `0006` | [D5 — Deferred: the zero-check gate should exclude conflicted PRs](decisions/0006-d5-deferred-the-zero-check-gate-should-exclude-conflicted-pr.md) | No code now. Own PR, later, never inside an order. |
| `0007` | [LF1 — A relabeller that cannot resolve a label must refuse, not guess](decisions/0007-lf1-a-relabeller-that-cannot-resolve-a-label-must-refuse-not.md) | Status: the tool change is here. The 121 restorations are proposed, not landed. |
| `0008` | [D11 — A changed admitted byte needs a registry move as much as a new path does](decisions/0008-d11-a-changed-admitted-byte-needs-a-registry-move-as-much-as.md) | education-publication-admission.json pins a digest per path. The publisher |
| `0009` | [D12 — Build a counterfactual to contradict you, not to pass](decisions/0009-d12-build-a-counterfactual-to-contradict-you-not-to-pass.md) | LF1-B §2.2 required that no page carry two adjacent nodes with identical text. |
| `0010` | [D13 — A browser-rendered census is the standard for a pupil-visible claim](decisions/0010-d13-a-browser-rendered-census-is-the-standard-for-a-pupil-vi.md) | Two false findings in one day, from opposite directions, both from not rendering: |
| `0011` | [D14 — What a render census has to cover](decisions/0011-d14-what-a-render-census-has-to-cover.md) | The LF1 numbers, same phrase, same 22 pages, by how it was measured: |
| `0012` | [D15 — One re-run is a discriminating test; a second identical failure is an outage](decisions/0012-d15-one-re-run-is-a-discriminating-test-a-second-identical-f.md) | An install-time failure — one that happens before any test body runs — is |
| `0013` | [D16 — A crash is not a refusal](decisions/0013-d16-a-crash-is-not-a-refusal.md) | A refusal names the problem, leaves the file byte-unchanged, and lets the run |
| `0014` | [D17 — A positive control is part of a clean result, not an optional extra](decisions/0014-d17-a-positive-control-is-part-of-a-clean-result-not-an-opti.md) | The census of those 47 returned 0. On its own that is worth nothing: a page that |
| `0015` | [D18 — What the estate's manifests actually look like](decisions/0015-d18-what-the-estate-s-manifests-actually-look-like.md) | Three envelopes are in use and only two were known: |
| `0016` | [LF1-G §6 — DEFERRED, recorded as the next order](decisions/0016-lf1-g-6-deferred-recorded-as-the-next-order.md) | The guide-mode CSS defect. html.mbm-guide-on data-mbm-guide{display:revert |
| `0017` | [D19 — A manifest entry with no week is a data defect, not a labelling decision](decisions/0017-d19-a-manifest-entry-with-no-week-is-a-data-defect-not-a-lab.md) | Granted by Matt, 2026-09-09, on the amendment argued in |
| `0018` | [D20 — RULE R-CAL-1, when a calendar token may be re-tokenised](decisions/0018-d20-rule-r-cal-1-when-a-calendar-token-may-be-re-tokenised.md) | Ruled by Matt, 2026-09-09. Landed verbatim below and in the docstring of |
| `0019` | [D21 — 75 of the 205 refusals are a numbered question, not a week](decisions/0019-d21-75-of-the-205-refusals-are-a-numbered-question-not-a-wee.md) | Found while proving the three Spr2·W6 pages under F6, because all three refuse |
| `0020` | [D22 — R-CAL-1 does not apply to `Tutor_Time/` or `Assembly/`](decisions/0020-d22-r-cal-1-does-not-apply-to-tutortime-or-assembly.md) | LF1-M §8e. Stated here so no future relabelling pass reaches for them. |
| `0021` | [D24 — WITHDRAWN (Matt, 2026-09-09). §8a's amended wording survives it.](decisions/0021-d24-withdrawn-matt-2026-09-09-8a-s-amended-wording-survives.md) | Withdrawn, not superseded: the ruling was correct on the evidence and the |
| `0022` | [D26 — STANDING RULE: path, never basename](decisions/0022-d26-standing-rule-path-never-basename.md) | Every comparison between an original and a re-cut, and every payload-to-original |
| `0023` | [D27 — gates measure rendered output, never source](decisions/0023-d27-gates-measure-rendered-output-never-source.md) | Any gate whose subject is what a pupil can see is measured in a laid-out page. |
| `0024` | [D28 — no instrument counts until it has a two-sided control](decisions/0024-d28-no-instrument-counts-until-it-has-a-two-sided-control.md) | Every gate, checker and comparison ships with a planted true positive (the |
| `0025` | [D29 — §4c restoration proceeds on the derived 86](decisions/0025-d29-4c-restoration-proceeds-on-the-derived-86.md) | Ruled by Matt, 2026-09-09 (LF1M-FIN). The count is the output of the |
| `0026` | [D30 — the loose Week 01 never lands](decisions/0026-d30-the-loose-week-01-never-lands.md) | GROW_Week_01_Interactive.html, 24,013 B, md5 b927e6f686, is provenance, |
| `0027` | [D31 — same-basename register](decisions/0027-d31-same-basename-register.md) | _authoring/BASENAME_CONFLICTS.md records every same-basename divergence: |
| `0028` | [D32 — G5 revised: rewrite becomes add](decisions/0028-d32-g5-revised-rewrite-becomes-add.md) | All eight lessons carry base64 data: URIs only, so there is no href to |
| `0029` | [D33 — a text-mode read is not a byte measurement](decisions/0029-d33-a-text-mode-read-is-not-a-byte-measurement.md) | Byte equality is asserted from binary reads or os.path.getsize plus a content |
| `0030` | [D34 — duplicate uploads](decisions/0030-d34-duplicate-uploads.md) | Byte-identical duplicates of files already measured; stored once by hash, and P1 is |
| `0031` | [D31 — a registry move travels with the bytes that need it](decisions/0031-d31-a-registry-move-travels-with-the-bytes.md) | Any PR that changes the bytes of an admitted served path MUST carry the registry |
| `0032` | [D3 — the §6 citation fix is CLOSED-VOID](decisions/0032-d3-the-section-6-citation-fix-is-closed-void.md) | Status: CLOSED-VOID. There was never anything to ship. Recorded here so nobody |

32 rulings. The text of each is in its own file and is never edited after landing.
