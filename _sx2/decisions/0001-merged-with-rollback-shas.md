## Merged, with rollback SHAs

| repo | PR | merged | rollback |
|---|---|---|---|
| Lessons | #454 content (51 lessons, 309 pack files, authoring source) | `d4b9b0ca` | `2c33266b` |
| Apps | #74 gate-copy sync, stale apps caller pin corrected | `ca7c3a36` | `630e838a` |
| Lessons | #455 catalogue, 848 → 950 rows | `331b0074` | `d4b9b0ca` |
| Apps | #75 caller-digest parity | `3bd55dbf` | `ca7c3a36` |

Lessons #453 was closed unmerged and superseded by #454 + #455. The GLV3 fence
never needed repair: `glv3-verify.yml` is `verify_change_boundary.py`'s only
caller and does not trigger on `Science_Teesside/**`. #453 carried content *and*
`resources.json`, which summoned the fence and then handed it protected content
to judge. Split, #454 ran 9 checks instead of 13 and the fence never fired.

---
