## D51 — the serve proof passes green on every PR without running

**STRUCTURAL, not incidental.** Filed under GW1-C §2.

### The mechanism

`.github/workflows/fieldops-p2-and-sweep.yml`, **lines 356 and 367**, in the job
*"Merged is not served — the placed labs and the Studio"*:

```yaml
      - name: Recover successful source-bound publication artifacts
        if: github.event_name != 'pull_request'          # line 356
      …
      - name: Every original subject serves the exact successful publication
        if: github.event_name != 'pull_request'          # line 367
```

On a pull request both steps **skip**. The job's remaining steps pass, so the job
passes, so the check reports **green**.

The reasoning behind the guard is sound and stated in the workflow itself — *"a
PR branch is not deployed"*, so there is no publication of that source to compare
against. The consequence is what was never stated: **no pull request in this
estate can prove anything about publication, and the green it reports reads as
evidence when it is an absence.**

### The worked example, and it is mine

**PR #498** raised `--wait-seconds` from 240 to 1800 in the caller and left the
ceiling inside the tool it calls at 300. Its serve-proof check went **green** —
because it skipped. Merged on that green, main failed in under a second:

```
[INCONCLUSIVE] Publication wait must be bounded to 1–300 seconds
```

A PR whose entire subject was the serve proof was gated by a serve proof that did
not run. The check most qualified to catch it was the one structurally incapable
of doing so.

### Why this is different in kind from the other instances

The register's family — now twenty entries — is faults in what code *looked at*
or *reported*, and every one of them was caught by **a person or an instrument
reading an output**. Even D49's census, which printed `0` on five branches,
existed as a wrong number somebody could read.

**This one produces a green with nothing behind it, on every pull request this
estate will ever open.** There is no output to misread, because there is no
output. It is not a wrong answer; it is the absence of an answer wearing the
costume of a right one.

### The open question — a question, not a proposal

> Could the step run on pull requests against a **scratch publication** — one
> built from the PR head rather than looked up by source SHA — so that a PR
> proves something about publication rather than skipping?

Not answered here. It bears on cost (a publication per PR), on isolation (where
scratch output goes and who cleans it up), and on whether a scratch publication
is evidence about the *real* one or a different thing wearing its name — which
is the same question this estate keeps asking about proxies. It needs a decision,
not an implementation.

### What was deliberately NOT done

**The workflow was not edited.** GW1-C §2.3: never edit a check to make your own
PR pass, and **that rule holds even when the check is defective** — arguably
especially then, because a defective check is the easiest thing to justify
touching. #499 sits behind this same vacuous green and is merged on that basis
with the defect recorded rather than removed from its own path.
