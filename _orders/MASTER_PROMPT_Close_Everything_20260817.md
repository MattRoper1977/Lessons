# MASTER PROMPT — Close everything
**Date:** 2026-08-17 · **Scope:** every open estate item, in one order, ranked by what actually matters
**State (hypotheses — derive them):** Lessons `c630fa8` · site `c3562478` · Apps `2e2de98` · branch `claude/new-session-1cuw3p` @ `55facdb`

**Sequencing is not negotiable: §2 runs first and alone.** If only one section of this order completes, it must be §2. Everything after it is bookkeeping, and bookkeeping does not outrank a pupil-data finding that has now survived four sessions.

---

## §0 RULES AND RULINGS

### §0.1 In force by number
R0.1 (three limbs) · R0.5 · R0.7 · R0.8 · R0.9 · R0.11 · R0.12 · R0.14 · R0.15 · R0.16 (unfiltered census) · R0.18 **as amended: a precondition may ask a question; it may not enumerate the permissible answers** · R0.19 · R0.20 · R0.21 · R0.23 · R0.24 · R0.25 · R0.26 · R0.27 · R0.28 · R0.29 · R0.30.

### §0.2 RULING — merge v0.4.1 on green, but land it UNLINKED
**Merge when every gate is green in CI and the four path tests pass. Do not wait for my ruling** — the same reasoning as #127: the harm of waiting accumulates and the fix is bounded.
**But the lab lands unreachable by navigation.** Placed at its route, proven served, and **added to no hub, no index, no catalogue, no `resources.json`** until Matt has done a paper read. Precedent is R-H08: a human observation gates the thing pupils will use, and no instrument can witness a paper read. State the unlinked status in the PR body and in the ledger.

### §0.3 RULING — the tag's three ledger references are a live falsehood and get corrected by supersession
The census found one reader: `RELEASE_LEDGER_2026-08-16.md`, in three places, describing a tag that **does not exist on any remote** — zero tags across all three repos. **Correct it by dated superseding pointer, never by rewrite**: the original entries were true when written, and the finding (*a local tag in a disposable container is a countdown, not preservation*) is worth more than a clean record. State the third case explicitly — `614f4d8` is the live head of remote `claude/hud-coverage-scriptline-load-bearing`, so the tag was a redundant alias, not preservation and not a bookmark.

### §0.4 RULING — the five held PRs are exempt-while-held, and the disposition goes in the PR body
Lessons #17, #35, #43, Apps #2, site #25. **A held PR with zero checks is not a defect** — it accurately reflects that nothing is asking to merge. Each gets its rebase, and its checks free, when its hold lifts. Write the disposition and its reason into each PR body so the next census does not re-raise them. **Do not rebase, do not merge, do not close.**

### §0.5 RULING — B2's disposition is forced this pass
B2 conformance has been "recorded as a gap" through three readbacks and no result has ever survived. **A gap named four times is not a gap, it is a decision nobody is making.** This order does not re-run it. It **reports what re-running would cost** — the order that governs it, the artefacts required, whether they still exist — so the choice is between *commission it* and *formally retire it with a reason*. Both are acceptable; a fourth "still a gap" is not.

### §0.6 RULING — the matcher stays deferred, and that is not a debt
No PyYAML in CI, no wiring into the watch's UNDETERMINED bucket, until the soak completes and it has a true-negative *at the wiring point*. `unenforced` is an honest state. Report the soak count; do not shorten it.

---

## §1 DERIVE THE STATE (R0.18, R0.30)

Print, for all three repos: head, open PRs with check counts, the watch's latest verdict and **soak count**, and the branch/tag facts. Name where each subject of this order lives before touching it. Any hypothesis above that is wrong → report the delta; a stop only where it changes what a section would do.

---

## §2 VSL v0.4.1 — RUNS FIRST, RUNS ALONE

**The artefact has arrived.** Execute, without restating or amending them:

2.1 `MASTER_PROMPT_VSL_Intake_and_Ledger_2026-08-17.md` **§5** — location printed · all 17 pack checksums verified by content · the four HTML measurements asserted (287,161 B · 1,978 lines · sha256 `137bbfac…` · 13 benches), any delta a stop · first commit stated as a ref (R0.19).
2.2 Then `MASTER_PROMPT_VSL_v0.4.1_RUN_2026-08-17.md` **from §1.2 onward, unchanged.** P0 re-measured after every phase · P8.0 removal matrix first, red-on-revert before any green counts · every gate ships a true-negative · R0.28 in the gate logic.
2.3 **One live amendment to that order's §8.1, and it removes an obstacle rather than adding one:** `fieldops-p2-and-sweep.yml` carries `pull_request`/`branches:[main]` with **no `paths:` filter — it matches everything**. A main-based VSL branch therefore picks up checks automatically. §8 still stands: **predict the trigger table before opening the PR, then compare** — the prediction should now expect that workflow to fire.
2.4 Merge on green per §0.2. **Then land it unlinked**, and say so in three places: PR body, ledger, readback.
2.5 Serve proof after merge: 200 **plus byte-identity to the committed blob**, chain named or empty. Predict the new derived route count with its predicate before merging, then compare (currently 29 = 23 site + 5 Lessons + 1 Apps — derive it, do not copy it forward, R0.29).

**Do not begin §3 until §2 has either merged or stopped with a named reason.**

---

## §3 THE MATCHER BRANCH

Open a PR for `55facdb`. It is report-only and nothing depends on it; the point is that its evidence stops being local (R0.20). Declared payload complete, no riders. Its own controls stay **labelled local** until PyYAML exists in CI — say so in the body rather than implying CI proved them.

---

## §4 RECORD CORRECTIONS

4.1 The tag's three ledger references, per §0.3 — superseding pointers, originals intact.
4.2 The five held PRs, per §0.4 — disposition written into each body.
4.3 `zero_check_baseline.json` reconfirmed **in CI** if the 401 is resolvable; if not, record **INCONCLUSIVE with the mechanism** and move on. Do not retry the 401 (R0.21). The MCP-derived figures matched the baseline exactly and that is worth stating.
4.4 `9a5b424` — confirm its untested-head status and the annotation naming it as the watch's own error are both still in the record.

---

## §5 THE FIVE DECLARED-NOT-DERIVED ROUTES

`/` · `__FULL_HOME__` · `/games/` · `/site.json` · `/Games/games.json` — inherited by the serve gate as unchecked. **One verdict each: extend the deriver to cover it, or declare it exempt with a written reason.** `__FULL_HOME__` is not a route and should say so; the two JSON files are data, not pages, and need a different assertion than byte-identity of a served page — say which, or exempt them. **Do not leave five unchecked things named but undisposed for a fifth session.**

---

## §6 B2 — REPORT THE COST, DO NOT RUN IT

Per §0.5: name the governing order, the artefacts it needs, whether they still exist and are reachable, and roughly what a re-run involves. **Then stop.** The choice is Matt's, and this order exists to make it a choice rather than a recurring line in a residue table.

---

## §7 THE CLOSING LEDGER ENTRY

One dated section, written last, containing only what this run measured:
- §2's outcome — the patch, the gates both directions, the merge, **the unlinked status and why**, the serve verdict.
- The tag correction, with the third case stated and the countdown finding kept.
- The held-PR dispositions.
- The five routes, each with its verdict.
- B2's cost report and the decision it now needs.
- The watch's soak count **as a dated snapshot citing the tool** (R0.29 — never a live value copied in).
- **What remains open, by name, and what is Matt's rather than the estate's.** An arc that closes with an empty remaining-list has stopped looking.

---

## §8 MATT'S OWN LIST — record it, attempt none of it

1. **Repo → Settings → General → automatically delete head branches.** Closes the stuck branch permanently and removes the 403 from the loop.
2. **Account → Settings → Notifications → Actions → "failed workflows only", Watching on the repo.** The watch's human leg. Until then R0.22 is satisfied in mechanism, not in effect.
3. **Revoke the GitHub token** — two were pasted into a chat session in July and it is still outstanding. This one is security, not tidiness.
4. **PLANS-3 close-out** — download all four deliverables, delete the sensitive uploads, and confirm the GROW W4A correction landed in both the school copy and the export.
5. **The 29 August Planning/ reconvergence** — its own small order when the date comes; not part of this one.
6. **The VSL paper read**, which is what unlinks §2.4.

---

## §9 READBACK — seven items
1. State as derived, deltas named, and which sections were reached.
2. **§2 in full** — intake measurements, every phase's before/after proof, the two-sided P2 assertion quoted byte-level, P3's measured figures against the 2,048 predicate, the gate table with reds and greens both named, the predicted vs actual trigger table, the merge, the unlinked confirmation, the serve verdict.
3. §3's PR, with its evidence-locality labelling.
4. §4's corrections, each as landed.
5. §5's five verdicts.
6. §6's cost report.
7. **What I refused, what I got wrong, and what remains open by name** — separating estate items from Matt's.

---

## §10 STOP CONDITIONS
- Any intake measurement differs → stop; a different file is a different subject.
- Any P0 number moves → stop; that is a regression in verified science.
- P2's absence assertion cannot be made byte-level → stop; a privacy fix proven by inspection is not proven.
- A gate cannot be shown red on revert **or** green on a known-good input → it is not a gate.
- Any path test fails → stop before placing.
- A ledger edit would rewrite rather than supersede → stop.
- A permission error → classify on first occurrence, record blocked, continue (R0.21).
- Reds growing rather than shrinking → hard stop.

---

## §11 OUT OF SCOPE
Rebasing or merging any held PR · #116 (reference diff, do not merge) · #117 (P0-only) · #118 (parked) · wiring the matcher or adding PyYAML · re-running B2 · the site tag (it does not exist — nothing to push) · any history rewrite · anything in §8.

---

*Everything in this order except §2 is record-keeping, and record-keeping is why the estate can be trusted — but it is not why it exists. The one thing here that changes what happens to a child is a pupil's name and notes travelling in a URL that Share hands out. Four sessions have now ended with that sentence intact. End this one differently.*
