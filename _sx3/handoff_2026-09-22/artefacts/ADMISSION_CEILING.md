# The admission job's clock — measured trend, ruled response

## The numbers, all observed rather than estimated

| run | job | duration | headroom vs the 35m ceiling |
|---|---|---:|---:|
| recorded reference (in the workflow's own comment) | NAV-2 era | 24m09s | 10m51s |
| Site #430 | 106783786108 | **31m47s** | 3m13s |
| Site #431 | 106803396986 | **32m05s** | **2m55s** |

Two consecutive runs within three minutes of the ceiling is a trend, not a one-off.
On present growth the next fold hits it.

## Ruled response

1. **The pre-ruled single re-run stays in force** for any timeout.
2. **`timeout-minutes: 35 -> 60`** on the Site's `Complete separated publications` job
   (`.github/workflows/domain-split-verify.yml`), APPROVED IN ADVANCE, to be carried in the
   **next Site window** — which is step 3 of this fold, the small EQUAL re-pin window.
   It is a **config-only change**: it asserts nothing, loosens no gate, changes no step,
   threshold or scope. It buys wall-clock, nothing else. To be named as such in that PR body.
3. **Next-order item, with a target rather than an observation**: the job's duration grew from
   24m to 32m because the education tree is now **5,739 files** and the browser mount walks all
   of them. Target: **split the browser mount into its own job**, so that all-file admission
   (the named step 14, `check_education_publication_admission.py --build-control`) and the mount
   return **separate verdicts** instead of sharing one clock and one conclusion.

   Why that is the right cut rather than simply a bigger number: today a mount slowdown and an
   admission failure are indistinguishable from outside — one red, one duration, one job. Split,
   the admission verdict stays fast and legible and the mount can be given whatever clock it
   needs without hiding behind it.

## What must NOT be done

Raising the timeout is not a fix for the growth, and the raise must not be allowed to stand in
for the split. It is a clock, bought once, so the next fold does not stop on it.
