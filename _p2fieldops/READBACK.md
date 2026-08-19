# P2 FieldOps own session — §READBACK

ROLLBACK_LESSONS `a2f0b5b` · ROLLBACK_APPS `6a8ae06` · merge `cb83ea9` (PR #139)

## 1. Identity + intake — PASS, by a route the prompt did not anticipate

§1.2 expected a 15-file release pack attached to the session with `SHA256SUMS.txt`
selected by content. **One** file was attached:
`00_BUILD_FieldOps_Teacher_Studio.html`, 54,780 B, and **no checksum file at all**
(0 uploaded; the three "SHA256" grep hits are prose in the two prompts and the
`sha256()` function inside the Studio itself). Taken literally that is "the pack
is absent → STOP".

**Repo wins over any document (R0.16), and it does here.** The release bytes are
in the repository, tracked, at `tools/fieldops/release/`, and the attached file is
**byte-identical** to the repo's copy:

    a7e50f8c0e33d8b6d8595c68c9e9238d503d3cd66eec6cd3003a6433daac0754  (uploaded)
    a7e50f8c0e33d8b6d8595c68c9e9238d503d3cd66eec6cd3003a6433daac0754  tools/fieldops/release/00_...

All five release apps are present at exactly the sizes §1.2 names — 54,780 /
54,737 / 54,567 / 55,697 / 52,056 — so the negative control every patch is measured
against exists and is verified. Intake satisfied **by hash, not by name**, which is
what R0.7 actually asks for.

## 2. The "FieldOps P2 red" — §1.3 answered, and A2 measured, not predicted

| head | FieldOps | note |
|---|---|---|
| `a810d44` · `51e8124` · `d6280de` | failure | inherited red, identical each time |
| `0b407e0` | **cancelled** | **not** a failure — never completed |
| `a2f0b5b` | failure (run 32279705417) | same job, same failing step |
| `f59df00` (PR #139) | **success** | after the A3 repair |

`0b407e0` matters: the previous session recorded it "still pending, expected to
fail the same way". It was **cancelled**, by this workflow's own
`concurrency: cancel-in-progress: true` when `a2f0b5b` was pushed. It confirms
nothing, and the addendum's "do not predict either" was the right instruction.

## 3. A3 / §2.8 — the red, closed at source

Full reasoning: `_p2fieldops/A3_RULING.md`. Ruled **(c) widen minimally**; neither
side was stale. Measured before → after:

| | before | after |
|---|---|---|
| rows it could not parse | 20 | **0** |
| claims judged in Matt-s-Apps- | 0 | **41** |
| stale claims | 0 | 0 |
| sweep exit (roots present) | **2** | **0** |

**R0.1 three limbs.** (a) CI step "The sweep over all three estates, and all three
must be assessed" — red at `a2f0b5b`, **success** at `f59df00`. (b)
`tools/fieldops/qa_record_control.mjs` plants a QA record naming an absent file
and requires `STALE`; **proven able to go red by mutation** — stubbing the
resolver to a rubber-stamp fails 2 of its 4 checks, exit 1. It runs in CI as
"The qa-record form can still call a planted subject stale" — success. (c)
workflow `.github/workflows/fieldops-p2-and-sweep.yml`, **no `paths:` filter by
deliberate design**, so every path matches, including both files changed.

Sweep self-test: **PASS, 0 checks failed**, after the change.

## 4. A4 — the two passes are provably disjoint

SCA-1 CLOSE v2's hinge shuffle marker is `data-shuffle=`. **0 occurrences** across
FieldOps deployed + release + staging (predicate: the attribute, not the English
word "hinge" — the labs have a legitimate hinge of their own). Positive control:
**35** science v3_40min decks carry it. File-set intersection of the 43 files
SCA-1 P1 touched with the 26 FieldOps files: **0**.

## 5. §2 patch set — verified, not restated (R0.2)

`tools/fieldops/build.mjs` + `controls.mjs` re-run this session from release bytes:
**0 failures, 0 undeclared unreachable, 1 declared unreachable by design.**

One divergence from the prompt worth stating plainly: §2.1 anticipates a
**"1-of-5 → 6-of-6"** headline. The measured headline is **1 of 5 → 6 of 7**, with
**C24 declared unreachable by design** — at the 390 °C furnace ceiling C24 is
selectable but cannot be distilled, so the harness books it `UNREACHABLE` rather
than counting it as taught. The repo's own number governs.

## 6. Refused for want of a control (R0.9)

Nothing was refused. The one item that could not be *proved* here is the live
serve check, below — reported, not worked around.

## 7. Serve proof

Pages build **success** on the merge commit `cb83ea9`. The live origin
`mattroper1977.github.io` is unreachable from this environment (HTTP 000 on two
attempts; `api.github.com` returns 200 from the same shell), so per §8:

**raw-pin NOT RUN — network blocked**

No GitHub raw read was substituted for it.

---

## 8. Confirmed on main — measured, not predicted (check-in, 2026-08-19)

The FieldOps run on the merge commit `cb83ea9` was **cancelled**, not failed: pushing
the readback commit `9919a74` tripped this workflow's own
`concurrency: cancel-in-progress: true` — the identical mechanism that cancelled
`0b407e0` and that §2 above documents. Worth noting as a live reproduction of it
rather than a new problem.

The measurement that counts is on main head **`9919a74`** (run 32288345978):

| job | conclusion |
|---|---|
| FieldOps P2 — the build is reproducible and the labs still boot | success |
| **The stale-evidence sweep can still find something** | **success** |
| No open PR runs zero checks | success |
| Merged is not served — the placed labs and the Studio | success |
| The way out of a game is keyboard-reachable — both estates | success |

and at step level inside the sweep job:

| step | conclusion |
|---|---|
| The authored positive controls, the regressions, and the seventh form | success |
| **The qa-record form can still call a planted subject stale** | **success** |
| **The sweep over all three estates, and all three must be assessed** | **success** |

`pages build and deployment` — success.

**`Watch main` is green as well** (runs 32288393865 and 32288726959, both success).
That closes the loop the SCA-1 CLOSE v2 classification opened: the reporter was
never defective, it was correctly naming the failing FieldOps run, and it greens
when FieldOps does. It now has.

The red first observed at `a810d44` is closed on main, with its repair guarded by a
control proven able to fail. Later documentation-only commits re-run the same
workflow over the same code; this entry records the run that first proved it green.
