# Reviewed lesson downloads

This builds the existing main Science lessons by their verified source term and
the fourteen lessons in each Arts Award strand. It does not claim that the Easter
curriculum is complete. Definitions explicitly name lessons, support resources
and four links to another term's lesson; filenames never supply menu titles or
term placement.

Run from the Lessons checkout:

```sh
python tools/downloads/verify_definitions.py > /tmp/download-source-review.json
python tools/downloads/build_all.py --output /tmp/lesson-pack-zips
python tools/downloads/prepare_pack_browser.py --definitions tools/downloads/definitions --archives-dir /tmp/lesson-pack-zips --extracted-dir /tmp/lesson-pack-extracted --manifest /tmp/download-browser-manifest.json
node tools/downloads/offline_pack_browser.cjs --manifest /tmp/download-browser-manifest.json --packs-dir /tmp/lesson-pack-extracted --report /tmp/download-browser-acceptance.json --channel chrome
```

Use a fresh extraction directory. The browser driver is Playwright 1.62.1 with
installed Chrome. The download job in the monitored FieldOps workflow records exact archive hashes,
current source placement, structural controls, extracted-file interactions and
pack-start screenshots. FieldOps is already registered with Watch main.

The package builder copies explicitly selected public files and their local
runtime dependencies. It refuses private paths, workbooks, symlinks, missing
runtime assets and externally loaded runtime code. The included Arts Award slot
register must be the canonical empty register. Teachers can load it through the
existing file picker; downloading a pack never confirms a booking or experience.

The exact reviewed Site HUD is pinned in `vendor/HUD_SOURCE.json`. Science packs
that need it use a `Lessons/` wrapper to preserve its own lesson-mode predicate.
Only the recognised script loader is adapted in packaged copies. The packer leaves source lessons and the Site repository unchanged. The separate
Guidance toolbar repair in this PR also fixes live Science navigation. A small adapter keeps Back inside the
download and labels a previously chosen online homepage as needing internet.

Home links receive local pack menus. The Solar System source-card page and its
two teacher resources are explicitly included. Four cross-term links open clear
continuation pages with a local return and an optional canonical online link.
These are navigation pages, not extra lessons. Release builds refuse any other
unresolved local navigation.

Archive order, timestamps and permissions are fixed. Every build is repeated and
compared using the same Python/zlib environment. Browser acceptance covers all
twelve starts and 130 lesson members: 88
Science and 42 award lessons, with fifteen interactive representatives. It checks
actual navigation, teacher tools, timers, calm controls, print invocation and
print-media content with the network disabled. It does not claim to test every
activity, physical printing, microphone capture or online video playback. All 47
repaired Guidance routes also require actual toolbar and Next/Previous clicks at
1280px and 390px, giving 94 focused regression cases.

The archive files become public downloads only after the exact reviewed ZIPs are
included in the final catalogue/navigation transaction.
