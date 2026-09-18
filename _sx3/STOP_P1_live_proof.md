# STOP-P1 — the served-proof gate has been red on main since 17 September

Not this release's defect. Reported rather than fixed: it predates the release,
and §7(e)/3c needs it green at CLOSE.

## The failure

Workflow `Made by Matt cross-estate unification`, job **`live-proof`**, step
*"Prove the served responsive and standalone estate"*.

Reproduces. Runs on main, latest first, with each run's `live-proof` verdict:

| head | overall | static-contract | live-proof | when |
|---|---|---|---|---|
| `f6660a1c` (#588) | **failure** | success | **failure** | 18 Sep 16:35 |
| `88fbb011` (#586) | **failure** | success | **failure** | 18 Sep 16:18 |
| `00a01f5a` (#587) | cancelled | success | cancelled | 18 Sep 16:05 |
| `cb1eb052` (#584) | **failure** | success | **failure** | 18 Sep 14:33 |
| `d872ef99` (#575) | success | success | *skipped* | 18 Sep 11:54 |
| `8d76957c` (#574) | **failure** | success | **failure** | 17 Sep 23:11 |
| `ae4c7d20` | **failure** | success | **failure** | 17 Sep 17:25 |
| `8b880d6c` | success | success | *skipped* | 17 Sep 12:14 |

It has failed on **every main commit where it actually ran** since 17 September.
Where the workflow reports success, `live-proof` was **skipped**, not passed.
`static-contract` passes throughout, and `browser-matrix` — the same checks
against a local build — passes. Only the **served** arm fails.

## The cause, established

The step runs two commands under `set -euo pipefail`:

```
node tools/verify_cross_estate_browser.mjs
node tools/sw2/check_tokens_inert.cjs --base "$(cat /tmp/mbm-live-base)" --published --output …
```

The printed evidence from the first shows `"errors": [], "fatal": null`, and that
harness exits non-zero only when `errors` is non-empty — so it passed and the
failure is the second command.

`check_tokens_inert.cjs --published` asserts, before anything else, that each
served route's bytes equal a digest **hard-coded in the tool**:

```js
const PUBLISHED={"apps":{"":"a2d5dedc…"},
  "lessons":{"":"01e571fa…","subject.html":"048f41f8…"}};
…
if(!expected||response.status()!==200||sha256(await response.body())!==expected)
  throw Error('Published HTML differs from admitted builder output: '+route);
```

**Measured.** The education publication was built locally from clean
`origin/main` on all three inputs the CI job uses — Lessons `f6660a1c`, Apps
`1b85bf2`, Site builder at the pinned carrier
`f70f49733373ccfc1660e85771a80eb6f612d6b9` — and every one of the three pinned
digests differs:

| estate · route | pinned | built from clean main |
|---|---|---|
| lessons `''` | `01e571fa7b4d619d…` | `5c4e3ced64113e43…` |
| lessons `subject.html` | `048f41f8c63c2a90…` | `93a071a895033cce…` |
| apps `''` | `a2d5dedca49c9fa8…` | `f15bc17d01e76150…` |

So the gate's pinned expectation no longer matches what the builder produces.

## Why it went stale

The pins were last set on **14 September** by `59d40c7b`, *"Match published proof
hashes to reviewed EDU-D2 owner outputs"*. Neither `index.html` nor
`subject.html` has changed in the Lessons tree since. What changed is an **input**
the published hub is built from: `resources.json` went **951 → 953 rows**
between `59d40c7b` (14 Sep) and `8b880d6c` (16 Sep). The first `live-proof`
failure is 17 September.

The published hub is not a copy of the source `index.html` — `build_education.py`
runs it through `clean_shell()` and `with_lesson_navigation()`. So a resource-row
addition moves the published bytes without touching the source file, and nothing
re-stamps this tool's pins when that happens.

## What I could not establish

Whether the pin was ever correct — i.e. whether rebuilding from the 14 September
tree reproduces `01e571fa…`. The rebuild at `59d40c7b` did not produce output and
I stopped rather than spend further on a defect outside this release. The
direction is established without it: the pins are stale against current main.

Also not read: the failing line in the CI log itself. The log middle is
unreachable from this environment — the tail does not span the failing step and
the blob-storage log download is refused by the network policy (403 on CONNECT,
as are the live origins and the publication artefact). The cause above is
established by local rebuild, not by reading CI's own error text.

## What it blocks

`PUBLISHED` is a hand-maintained digest table with no control that re-stamps it
when its inputs move — the same class of defect as the `watch-main` trigger list,
which at least had `--verify-trigger-list` to catch it. This one has nothing.

ORDER SX3-M2 §7(e)/3c requires a green publication and served proof at CLOSE.
This is that gate. It is red, it is not this release's, and the fix is a re-stamp
of three digests plus — properly — a control that keeps them from going stale
silently.
