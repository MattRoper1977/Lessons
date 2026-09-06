# HC3 Glitch Clash native fragment receiver

Measured route /Lessons/Games/Glitch_Clash.html is unowned by the current open PR census. Its existing native campaign import accepts raw Glitch Clash save JSON; the boot key is glitchclash_save. Claude's fragment receiver was not recoverable. The existing bulk transfer is unchanged.

This batch reconstructs only this game's receiver through the existing native parse/sanitize import path. The hash path must require the canonical Play origin/path, a bounded UTF-8 fragment, a valid native campaign save, no conflicting destination save and a successful persistent write/readback. Rejections preserve destination data and clear only the import fragment. Normal file import retains its existing native format and in-memory fallback behavior. No external game script or new save schema.

Rollback: Lessons d2a4a1cf3fd5840123e047a5c7dd86700a781526; canonical Play remains at the preceding published pin until its own release passes. One game file. No Education stub button is enabled by this PR. The sender must wait for exact Play receiver publication.

Required controls: real seeded native save, one planted dropped-persistence/readback defect red, restored green; malformed/null/array/version/prototype/depth/size/wrong origin/path/conflict/quota rejection; fragment clearing; normal native file import; all eleven existing Glitch suites. Phone/desktop browser checks before merge and exact Play source-pin proof after release. This is one adapter, not completion of all ten native importers.
