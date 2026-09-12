# GC1 download-registration release — 12 September 2026

Checkpoint: 2026-09-12T12:00:00.889742+00:00. This small publisher-repair pass is complete. Computing
content #493 is deployed and the selected 39 live files match reviewed output.
P6 catalogue/resources.json work remains a separate next transaction. This is
not a whole-programme closure or a claim that every main check is green.

## Exact release records

| Repository / PR | Reviewed PR head | Merge | Publication run | Result |
|---|---|---|---|---|
| Site #353 | 3259490039ce4df97bacc43e1c59fa68de1a0afe | bf7964758afd3d9e58e58ba58eb2048815917a09 | 34691568030 | build 103547614574 SUCCESS; deploy 103548301137 SUCCESS |
| Apps #83 | 12dbc9718139744797b5a37b6705ae2a5ae5b7e5 | cd8d478074634a0b432c00eeb7acf082994dd0e7 | 34691348779 | build 103547037874 SUCCESS; deploy 103547544120 SUCCESS |
| Lessons #512 | e2a7f422cc163fbe5f866c436b94827c32b62d79 | db5d804f5559a543c65c9d8bd0034a5764c05a40 | 34691889316 | build 103548484790 SUCCESS; deploy 103549456718 SUCCESS |

Apps and Site were independently reviewed; Apps publication completed before
Site merged, and Site publication completed before Lessons merged. No repeated
merge was needed after the interrupted session. Lessons merge tree
`d6d1c383f6977ffdd064365edf8d14053f16a3e0` equals the reviewed final tree.

## Cause and bounded repair

The initial #493 publication, run 34690363074, failed the separate teaching-pack
download-registration gate. Its 36 existing ICT rows were unchanged; 128 new
GROW_Computing download rows were absent from the approved registry. No old row
was removed or changed. The reviewed registry now contains 424 records across
seven prefix groups (previously 296), including 164 ICT records (previously 36).
All added routes resolve to actual generated files, use source education, kind
resource and download_request, and have empty aliases and source_ids.

Site changes exactly two files: the reviewed additions JSON and its separation
checker. The checker requires the extra rows when the actual Computing unit hub
is installed. Older pinned Lessons trees without that hub retain the original
36-row requirement; unexpected Computing rows there still fail. A legacy subject
index cannot establish whether this newer unit exists.

Lessons uses surgical Site carrier `3c2743fbfb345e1314f138d6b50d6a7ce18031ef`,
directly descended from its existing builder
`810ae8f8830dc9e30a7ceec9ada4ec24d575a04d`. Independent GitHub comparison confirmed
exactly the same two changed file paths and one added commit. The carrier preserves
the existing Science baseline, admissions and workflow bytes. Do not repoint this
caller to Site main: it carries different inherited inputs.

Lessons changes three files: both publication caller references; the governed
caller digest in tools/verify_cross_estate_unification.py; and one stale generated
resource-size value, ICT/Teaching_Packs/index.html, from 11,380 to 18,032 bytes.
The size generator changed no keys and checked all 1,463 entries. This is not a
size-table pin ratchet. Apps #83 mirrors only the governed caller-digest file;
its own caller, source input and publication pins are unchanged.

Reviewed additions SHA-256:
`faa329b20b5db39f44bf8cfeb5393ddac85d1a60dfe649d091ccac821bf67abb`.
Lessons caller SHA-256:
`2a478fb0aa2c4df2c244368e5f5b35b864912465aa4c581830e593e50058c8ac`.
Mirrored gate SHA-256:
`930b31647761f644ee70c09e914fbf7b247cd9047ab1822ab0da3206dab2da0e`.

## Verification

Seven new registry cases cover installed/absent packs, missing/extra/changed
rows and preservation of older rows. Existing partition and request checks remain.
Removing one real Computing row from assembled output failed; restoring it passed.
Tampering with the approved registry bytes failed the digest check; restoration
passed. The static contract passed and detected all three deliberate mutations.

Complete separation passed: 4,035 files, 1,644 HTML, 150 JSON manifests,
25,276 references, 79 migrations and 437 sitemap URLs, with no failures.
Actual publisher logs confirm 55 executable admission controls PASS, LEAK GATE
CLEAR, game-save controls PASS, and all-file admission PASS with 61 controls:
real PASS / planted tracked game FAIL / restored PASS. The job checked out both
the exact carrier and Lessons merge named above. Existing unit bytes were not edited.

The fresh live comparison fetched eight Interactive HTML files, eight pupil
Paper_Route PDFs and all 23 SB3 projects from madebymatt.uk/Lessons. **39/39 HTTP
200, 39/39 SHA-256 identical** to the reviewed assembled output. Request start
times range from 2026-09-12T11:57:16.673812+00:00 to 2026-09-12T11:58:11.384127+00:00. Per-file URLs, times, lengths and both hashes
are in [gc1-regfix-live-proof.json](rf3-evidence/gc1-regfix-live-proof.json).
The reproducible script is [gc1_regfix_live_proof.py](rf3-evidence/gc1_regfix_live_proof.py).
This comparison is byte proof for these 39 files, not a new browser or pedagogical
parity test. The previous 163-file ledger and full 204-position interaction proof
remain separately recorded in RF3_PHASE_READOUT.md.

Lessons publication artifacts, metadata read after completion:

| Artifact | ID | Bytes | Expiry UTC |
|---|---|---|---|
| education-lessons-review | 10297925529 | 732462940 | 2026-10-12T11:53:21Z |
| github-pages | 10298030498 | 730885644 | 2026-09-13T11:53:51Z |

Both were unexpired and bind to db5d804f. Artifact metadata and actual build logs
were read; this does not claim a separate local download of those ZIPs.

## Remaining audit red and next pass

Final Lessons PR checks: 12 SUCCESS, two expected SKIP, one attributed baseline
FAIL. The stale-evidence sweep failed identically on baseline 36ea1046 (job
103544410504), final PR (103546555972), and merged main (103548483855):
1,418 stale claims / 6,307 live / 6,899 row labels / 47 files matching no form,
exit 2. The historical-evidence parser also leaves verdict forms unparsed. No
audit gate was weakened or hidden.

At the final main readback all 23 check records were terminal. The latest workflow
watch, job 103549688372 at 11:56:55 UTC, reported six PASS workflows and one FAIL,
zero pending and zero without a verdict; the failing workflow is FieldOps run
34691888892 because of that sweep. Publication, static contract, browser matrix,
responsive downloads, live proof, derivation checks and placed-lab serve proof
passed. The watch correctly remains red; no whole-estate green is claimed.

Next in order is the separately scoped P6 catalogue/resources.json transaction,
with its governing exact-head checks and served evidence. Do not replay #493,
#512, #353 or #83. Preserve all other standing holds and the no-REGISTER-write
limit. SB1 is due before a second unit; P2Q still needs Matt to name that unit.

Matt's confirmed workflow remains laptop/Scratch work, screenshots/photos or
printable evidence, printed and scanned, emailed as a PDF to the UAS lead for
normal review or return. No advance lead check is required. Submission format
does not establish device-free teaching or G14/G15 paper-only parity. Existing
paper-route printing does not capture an external Scratch project. No email was
sent and the earlier speculative review PDF was not submitted.
