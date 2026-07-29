# GROW_HUM_W7 — assessed residue — HELD-FOR-SCOPED-PASS (D3 ruling)

**File:** `Grow/Slideshows/GROW_HUM_W7_Write_The_Account.html` — ★ ASSESSED LESSON.
**Status: UNTOUCHED.** Assessed quarantine — single-hunk, never auto-fixed, never batched.
**This lands ONLY on Matt's explicit word.** Logged here verbatim, not acted on.

## The residue (verbatim, read-only)
KO Key-Word row, quoted exactly as it stands at BASE `59ad56a`:

```
<tr><td>Evaluation clause</td><td>Deployed provenance honesty</td></tr>
```

- The word **"Deployed"** echoes the **"Evaluation Deployments"** support that Pass LL-A2a removed when it
  replaced the Reference Zone with the Assessed Conditions Card. Whether this KO row now describes support that
  no longer exists, or is an independent (still-valid) phrasing, is a **content read against the Conditions
  Card** — assessed-file discipline, Matt's key.
- The KO does **not** literally name "Connective Bank" or "Evaluation Deployments" (both 0 occurrences), so the
  carry-forward's worst case (a KO describing removed support by name) is **not** confirmed on the face of it.

## "Reference Zone" ×3 — checked, benign
All three "Reference Zone" occurrences are the assessed-conditions design, e.g. verbatim:
`Do not print a Reference Zone into this session.` — i.e. instructions that the Reference Zone is *withheld* under
assessed conditions, not a stale reference to printed support. No action.

## Disposition
No proposed diff is applied. If Matt rules the `Evaluation clause` row stale, the fix is a single hunk inside
the `print-ko` block of `GROW_HUM_W7`, executed under assessed discipline (Matt's key) — out of scope for
Pass E, which excludes both assessed files (`GROW_HUM_W7`, `LAUNCH_HUM_W7`) with no exceptions.

---

## Season-close S4 decision — AWAITING-WORD (NOT committed)

**Outcome: HELD, not committed.** S4's commit gate permits a single hunk **only if** the residue is strictly
non-pupil-rendered (a comment, an attribute, or a staff-only note). The residue is a **rendered `<td>` cell in
the printed Knowledge Organiser table** — categorically pupil-facing, none of those. It therefore fails the gate
and is **held verbatim** below; `GROW_HUM_W7` stays byte-untouched. It lands only on Matt's explicit word.

Standing rule this brushes against: *no reference zone reaches an assessed session.* The three `Reference Zone`
strings in this file are the **guard** enforcing exactly that — `Do not print a Reference Zone into this
session.` — i.e. correct assessed design, **not** residue. They are **not** part of the proposed hunk.

### Proposed single hunk (verbatim, NOT applied) — removes only the `Evaluation clause` KO row
```diff
--- a/Grow/Slideshows/GROW_HUM_W7_Write_The_Account.html
+++ b/Grow/Slideshows/GROW_HUM_W7_Write_The_Account.html
@@ KO key-word table (print-ko) @@
-<table class="ko-table"><tr><th>Key Word</th><th>Definition</th></tr><tr><td>Assessed conditions</td><td>Approved arrangements yes, assistance no</td></tr><tr><td>Thesis echo</td><td>The close's developed restatement</td></tr><tr><td>Evaluation clause</td><td>Deployed provenance honesty</td></tr><tr><td>Time-boxing</td><td>Minutes budgeted per unit</td></tr><tr><td>Reach sentence</td><td>One controlled step beyond the enquiry</td></tr><tr><td>Independence</td><td>Your plan, your words, your account</td></tr></table>
+<table class="ko-table"><tr><th>Key Word</th><th>Definition</th></tr><tr><td>Assessed conditions</td><td>Approved arrangements yes, assistance no</td></tr><tr><td>Thesis echo</td><td>The close's developed restatement</td></tr><tr><td>Time-boxing</td><td>Minutes budgeted per unit</td></tr><tr><td>Reach sentence</td><td>One controlled step beyond the enquiry</td></tr><tr><td>Independence</td><td>Your plan, your words, your account</td></tr></table>
```

**Note for Matt's read:** whether this row is even a defect is itself the assessed decision. "Evaluation clause
— Deployed provenance honesty" *echoes* the removed "Evaluation Deployments" support, but "Deployed" may be
legitimate vocabulary for this assessed enquiry; the hunk above assumes removal, but a **reword** (keeping the
key word, changing the definition) is the equally valid option. Pass E takes no position — **AWAITING-WORD.**
