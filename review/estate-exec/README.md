# Estate-review execution run — 2026-08-05

Acts on the four-pass review that opened PR #70 (audit tooling) and PR #71 (fix pack).
The full record, including the evidence verdict and every rejection, is the `§R` section
of `_sixclose/LEDGER.md`.

## What this directory is

`validate_estate_exec.py` — the validator for what landed. It is deliberately *not* a
general estate audit tool, and it is not proposed as standing tooling.

    python3 review/estate-exec/validate_estate_exec.py --repo . --self-test

Two rules it is built around, both written against defects in the work it checks:

1. **Every count is proved by enumeration**, and markup patterns are counted only after
   `<script>`, `<style>` and comment bodies are blanked. A census that skipped this
   returned 379 files / 6,438 hits for a raw `<` — all of it correct `i<n` loop code.

2. **Every check must be able to fail.** `--self-test` tampers a scratch copy to break
   each check in turn and asserts it goes red. A harness that cannot fail proves nothing:
   the fix pack's own `validate_applied.py` asserted both `'id="title"' not in grid` and
   `count('class="panel-title"') == 3`, which cannot both hold while its patch leaves a
   fourth `id="title"` in place.

Current state: **15/15 checks pass live, 15/15 proved able to fail.**

## What is NOT changed here

`/assets/video/poster-art.jpg` (patch 0004) and the ten Science Teesside `g-mblur` files
(patch 0005) are untouched by design — see `§R5` of the LEDGER for the derivations.
