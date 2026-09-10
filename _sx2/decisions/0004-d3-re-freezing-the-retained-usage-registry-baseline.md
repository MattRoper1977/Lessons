## D3 — Re-freezing the retained usage-registry baseline

`check_education_separation.py` freezes the digest of the rows
`registry_partition()` retains. The 51 new lesson records move it: **926 → 977
rows, 51 added, 0 removed, 0 field of any existing record changed.**

The method matters more than the number. A build at this repository's previously
pinned source `2c33266b` reproduces the *previous* baseline `d2439c61` **exactly
at 926 rows**. Without that equality the before/after comparison would prove
nothing, so re-freeze this way rather than by taking the new digest on trust.

---
