## D50 — a serve proof whose retrieval bound is shorter than the thing it waits for

SX2R §5's window opened and its own first condition — *main green between every
pair* — is not met. **Main has been red for twelve consecutive runs.** The cause
is not any pull request's content. It is one number.

### What is actually failing

`FieldOps P2, the sweep, and the serve proof` on `509c61de`: **7 of 8 jobs pass.**
The one that fails is *"Merged is not served — the placed labs and the Studio"*,
at step 7, *"Recover successful source-bound publication artifacts"*:

```
WAIT lessons: publication 34474582596 is in_progress
WAIT lessons: no completed publication for source 509c61de…
[INCONCLUSIVE] lessons: exact-source publication did not become available
               within the retrieval bound
##[error]Process completed with exit code 2
```

The job's own controls pass first — *"The instrument's offline controls"* and
*"All five controls fire — including on a pull request"*. **The instrument works.
It cannot reach the thing it measures.**

### The measurement

`tools/prepare_served_publications.py` waits for the *Education Pages
publication* run for the same commit, so it can compare served bytes against a
publication that actually deployed. Its bound is
`--wait-seconds` default **240** — four minutes.

Twelve consecutive publication runs on `main`, measured from the run list:

| run | duration | | run | duration |
|---|---|---|---|---|
| 153 | **7m49s** | | 147 | 7m13s |
| 152 | 7m58s | | 146 | 13m49s |
| 151 | 26m17s | | 145 | **6m20s** |
| 150 | 15m43s | | 144 | 7m43s |
| 149 | 7m39s | | 143 | 7m56s |
| 148 | 7m43s | | 142 | 7m58s |

**Minimum 6m20s. Median ≈7m50s. Maximum 26m17s. The bound is 4m00s — below every
one of the twelve.** Both workflows are started by the same push and run
concurrently, so the serve proof gives up 3m16s before the publication it is
waiting for succeeds. On `509c61de` that publication, run 153, **did succeed**.

This is not a flake and not a regression. **In this configuration the gate has
never been able to finish its measurement on a push.** A re-run cannot help: the
race is structural, and re-running only re-loses it.

### Two faults, and the second is the one that misleads

1. **The bound is wrong.** It must exceed the publication's runtime, and 240s
   never did. Nothing about the estate changed to break this; it has been
   arriving too early since it was written.
2. **`[INCONCLUSIVE]` exits 2 and therefore reads as a failure.** The tool is
   honest in words — it says it *did not measure*, not that it *found a
   problem* — and then reports that honesty through the same channel as a real
   red. Twelve reds on main all say "the estate is broken" when what they mean
   is "I arrived too early." Sibling of GW1-B R2: the computation was right and
   the report was not.

### Why this stops §5 rather than being worked around

- SX2R §5's own rule is *any red stops the sequence where it stands*.
- The five R6 PRs all move served bytes, and LW1 §F4 requires **a served proof
  per pathway**. Merging them while the serve proof cannot reach a publication
  would produce five merges with no served proof — defeating the point of the
  sequence rather than merely inconveniencing it.
- Raising a bound so a gate can *complete its measurement* is not the same as
  skipping a test, but it does change how long every push blocks, and that is
  the estate owner's call and not mine to take unasked.

**§5 is held. Nothing merged. The five PRs are untouched and still merge clean.**

### The proposed fix, for the record

Raise `--wait-seconds` from **240** to **1800** (30 minutes), which clears the
worst of the twelve (26m17s) with margin, and keep the job's `timeout-minutes`
above it. Separately, give `[INCONCLUSIVE]` an exit code distinct from a real
failure, so a gate that could not measure is not reported as a gate that found
something.
