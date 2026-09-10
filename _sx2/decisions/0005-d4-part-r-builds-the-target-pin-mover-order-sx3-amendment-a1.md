## D4 — Part R builds the target pin-mover (Order SX3 amendment A1)

`tools/easter/SCIENCE_ORIGINAL_TARGETS.json` pins 25 lessons by
`expectedPatchedSha256`, asserted as `Source identity: <file>` by the long
`Original Science navigation` job. **All 25 are files the Autumn 1 refresh
patches**, so any R landing reds that job unless the hashes move with it. No tool
rewrites them today; the file is hand-maintained, and it is *not* in
`CATALOGUE_PINS`, so no catalogue re-pin is involved.

Ruled (SX3 A1): the mover is built **once, in Part R, inside the fence**. It
recomputes `expectedPatchedSha256` from the patched bytes, rewrites the JSON in
the same commit, **fails if any target path is missing**, and is red-proved by
planting one stale hash. SX3 reuses it for its 64 REPLACE/PATCH files.

---
