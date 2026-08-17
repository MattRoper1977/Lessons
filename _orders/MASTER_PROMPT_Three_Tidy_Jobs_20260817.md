# MASTER PROMPT — Three tidy jobs: the site tag, the zero-check PRs, the path-filter matcher
**Date:** 2026-08-17 · **After:** Phase A closed at Lessons `c630fa8`
**State (hypotheses — derive them):** Lessons `c630fa8` · site `c3562478` · Apps `2e2de98`

Three independent jobs in three different scopes. **They share no files.** A stop in one does not block the others — report and continue. Each lands as its own PR or push; **nothing here merges anything else, and nothing here touches VSL.**

---

## §0 RULES AND RULINGS

### §0.1 In force
R0.1 (three limbs) · R0.5 (residue named) · R0.8 (a count without a predicate is not a measurement) · R0.9 · R0.14 (destructive: dry-run, report candidates) · R0.16 (no removal without an **unfiltered** reader census) · R0.19 (ref tables before/after) · R0.20 (evidence has a locality) · R0.21 (classify before retrying — a permission error is read on its first occurrence) · R0.23 (a pattern prints its scope and match set before acting) · R0.24 (every gate ships a true-negative) · R0.25 (write legs dry by default) · R0.26 (a rule lands as a mechanism or not at all) · R0.28 (an absence is not a result) · R0.29 (no live value copied into a static document) · R0.30 (name where the subject lives, and prove reachability first).

### §0.2 R0.30 applied up front — where each subject lives
- **§1's tag** lives in the **site repo**, locally, unpushed. This section is unrunnable from a Lessons-scoped session. Prove push scope to the site repo **before** anything else in §1; if absent, stop §1 only, report, and go to §2.
- **§2's PRs** live across **all three repos**. Enumerate per repo.
- **§3's matcher** lives in the **Lessons** tools tree beside the watch.

### §0.3 RULING — a zero-check PR is not automatically a defect
Some PRs are correctly unchecked: a reference diff that will never merge, a parked branch, a docs-only note. **The verdict per PR is one of three — gets a check · declared exempt with a reason · closed —** and never "fixed" by default. **R0.28: a draft with no checks and a PR whose filters missed are different findings and are reported apart.**

### §0.4 RULING — the census and the matcher stay REPORTS, not gates
Neither becomes a merge gate, and neither writes to the ledger, until it has a true-negative control and a declared soak (R0.24, R0.25). **The watch's false positive came from a gate that could go red before it had ever been shown able to go green.** Do not repeat it here — these are the two tools most likely to.

---

## §1 THE SITE TAG — one command, and the census decides what it means

1.1 **Precondition:** prove this session can push to the site repo. On any permission error, **classify on the first occurrence** (R0.21) — no retry loop — record blocked, and skip to §2.
1.2 Confirm the tag: `close-fixes/combined-614f4d8`, annotated, on commit `614f4d8`, present locally, absent on the remote. Print the annotation.
1.3 **Establish what the tag is for, because it changes the stakes.** Is `614f4d8` an ancestor of site `main`?
   - **Yes** → the tag is a bookmark; pushing it is convenience.
   - **No** → the tag may be the **only reference keeping that commit alive**, and pushing it is preservation. Say which, in the readback.
   Also report whether `hud-coverage-scriptline-load-bearing` still exists locally or remotely.
1.4 **Unfiltered reader census (R0.16)** across all three repos, all orders, all ledgers, for both the tag name and the commit SHA. Print the scopes and the match sets (R0.23). The last filtered census under-reported by one, and that error reads as permission.
1.5 Push **that tag by its full ref only** — `refs/tags/close-fixes/combined-614f4d8`. **Never `--tags`**, which would push every other local tag unexamined: a pattern acting beyond its stated scope is R0.23's whole subject.
1.6 Ref table before/after (R0.19), and a one-line loss statement — a tag push adds a ref and removes nothing; say so rather than implying it.

---

## §2 THE NINE ZERO-CHECK PRs — a table, then a verdict each

Last measurement: **21 open · 12 zero-check (3 draft, 9 not) · all nine declared · 0 undeclared · 0 to prune.** Re-derive it; do not carry those numbers forward (R0.29).

2.1 For every open PR in all three repos, produce one row: repo · number · title · draft? · check count · **cause of zero checks** — which `paths:` filter failed to match, or no `pull_request` trigger, or draft, or base out of date. **The cause is the deliverable**; a count of nine without causes is not a measurement (R0.8).
2.2 Assign each zero-check PR exactly one verdict:
   - **gets a check** — rebase onto a current base, or extend a workflow so its filter matches. Print the filter and the matched path (R0.1 limb 3) and prove the run (id, conclusion).
   - **declared exempt** — with a written reason, in the PR body. **#116 (reference diff, do not merge) and #118 (parked, ruled) are exempt by disposition, not defects.** Do not rebase them, do not retitle them, do not give them checks.
   - **closed** — only where the PR is genuinely dead, and only after an unfiltered census of anything referencing it. Nothing is closed silently.
2.3 **#117 stays P0-only.** Its scope is in its title and its README; that is a disposition, not an omission.
2.4 **No merges in this pass.** It is a checks pass. Anything that becomes mergeable is reported as such and left.
2.5 Residue named (R0.5): any PR whose cause cannot be established is **UNDETERMINED**, not "probably a filter".

---

## §3 THE PATH-FILTER MATCHER — the one that unlocks a real finding

Today the watch reports dormancy and refuses to judge it, which is honest and is why UNDETERMINED exists. This closes it. **The finding it unlocks: a workflow that SHOULD have run and did not — a workflow that has silently stopped running.** Nothing in the estate can currently detect that.

### 3.1 Semantics — get these right or the tool will lie confidently
- `paths:` and `paths-ignore:` are mutually exclusive within one event filter.
- Glob rules: `*` does **not** cross `/`; `**` does. `!` negations are order-significant — **last match wins**.
- **Branch filters gate it too.** A workflow whose paths match but whose `branches:` exclude the ref is **correctly dormant**, not a finding. Omitting this is the likeliest way to ship a tool that produces false reds — the exact failure the watch already made once.
- No `paths:` on that event → matches everything → not dormant by filter.
- `workflow_dispatch`-only → **NOT APPLICABLE**, provable from `on:`. `schedule` → runs regardless of paths. `workflow_run` → depends on an upstream run and stays **UNDETERMINED**; do not guess it.

### 3.2 Verdicts — four, and UNDETERMINED must get smaller, not disappear
**SHOULD HAVE RUN** (and did / **did not** ← the finding) · **CORRECTLY DORMANT** · **NOT APPLICABLE** · **UNDETERMINED**. Report the count of each with its predicate. A tool that returns zero UNDETERMINED on a repo containing `workflow_run` chains is overclaiming.

### 3.3 The regression fixture is already in hand, and it is free
**PR #124's trigger table**: 1 of 11 ran — `fieldops-p2-and-sweep.yml`, run `32026427208` — with seven `paths:` filters matching nothing in that diff and three workflows having no `pull_request` trigger. **The matcher must reproduce that table exactly**, from the commit's changed files. A hand-verified real-world answer beats any synthetic fixture, and this one cost nothing to obtain.

### 3.4 Controls — both directions on every run (R0.24)
(a) a workflow whose filter matches a changed file and did not run → **red, named** · (b) a correctly dormant workflow → **green, not a finding** · (c) `*` vs `**` boundary: a file one directory deeper → proves the glob semantics · (d) a negation-ordering fixture → last match wins · (e) paths match but branch filter excludes → **correctly dormant** · (f) empty workflow set → **exit 2** · (g) **true-negative: the real set on the #124 commit returns exactly the #124 table and zero findings.**
Output shows *n* reds fired and *n* greens returned, every run.

### 3.5 Landing conditions
Report-only. **Not wired into the watch's verdict, not writing to the ledger** (§0.4). It prints its result and its soak count. Wiring it into the watch's UNDETERMINED bucket is a later decision and needs its own true-negative there too.

---

## §4 OUT OF SCOPE — untouched, and say so
VSL (blocked on the artefact, not on anything here) · merging anything · the two account/repo settings, Matt's alone · B2 conformance · #116/#117/#118 content · the five declared-not-derived routes · any history rewrite.

---

## §5 READBACK — six items
1. §0.2's reachability results — which of the three sections were runnable, and which were not, with the reason.
2. §1: the ancestor question answered, the unfiltered census with scopes and match sets, the ref table, and what the tag turned out to be for.
3. §2: the full PR table with a **cause** in every row and one verdict each; the counts with their predicates; anything UNDETERMINED named.
4. §3: the four verdict counts, the seven controls each named and fired in both directions, and **the #124 table reproduced or the discrepancy quoted**.
5. What I refused and why.
6. What remains open, by name.

---

## §6 STOP CONDITIONS
- A permission error → classify on first occurrence, record blocked, continue to the next section. Never a retry loop.
- The census returns readers for the tag or a PR proposed for closure → stop that item, report the readers.
- Any control fires in only one direction → not a control; do not land the tool.
- The matcher cannot reproduce the #124 table → stop; a matcher that disagrees with a hand-verified answer is wrong until proven otherwise.
- Reds growing rather than shrinking → hard stop.

---

*None of these three is urgent. They are worth doing because each one is small, bounded, and removes a piece of ambiguity from the record — and because the matcher, alone among them, turns something the estate currently cannot see into something it can.*
