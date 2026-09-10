## D31 — same-basename register

`_authoring/BASENAME_CONFLICTS.md` records every same-basename divergence:
basename, both paths, both sizes, both md5s, which is canonical, and why.

Any future upload sharing a basename with a landed file is compared by **content
hash before use**. A hash mismatch is a listed conflict reported by name — never a
silent overwrite, never a merge. **This is D26 applied to inbound files rather than
to lookups.**
