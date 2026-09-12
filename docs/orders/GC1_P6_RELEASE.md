# GC1 P6 — catalogue publication readout

Measured 2026-09-12T12:52:30.989626+00:00. **The separately requested P6 catalogue pass is complete for
Matt's confirmed laptop/Scratch teaching and printed-evidence submission route.**
The Computing card is live; all eight served print routes passed Chromium checks;
24/24 served lesson and pupil paper files match the previously reviewed bytes.
This is not whole-programme closure, pupil completion or a device-free parity claim.

## Release references

| Transaction | Reviewed head | Merge | Publication |
|---|---|---|---|
| Apps #84, catalogue digest mirror | af54b7a233a810d33d5b2331321e6b7c81e33ab7 | e751f51a346d3837b5786b0ad063a732f2778306 | 34693048064; build 103551617791 / deploy 103552361542 SUCCESS |
| Lessons #513, catalogue | 4b35fdec69b54a753d020410f9ef971feafbd30f | 751948ea70ba6d27b0356539c94a8712ba79b025 | 34693397611 FAILED admission; deploy skipped; superseded below |
| Apps #85, caller digest mirror | ad849648918e62a187504fe26614d2c6c8dd2ea3 | c9a7a4e3496b0f1449ad035b4f77c3d6d7dbc56a | 34693856307; build 103553822662 / deploy 103554378007 SUCCESS |
| Lessons #514, admission caller | 1a095000d67442a7e065b6bc565f8cfc1f00ee50 | 4f8227cef7a0191df25145d53fe2bc05f7aa2ef9 | 34694243164; build 103554856058 / deploy 103555671187 SUCCESS |

Each Apps publication succeeded before the matching Lessons merge. Both final
merge trees equal their reviewed candidate trees. Catalogue tree:
`28cc32203b8a2343f43ce6c808edda0355883acc`; final Lessons tree:
`331b320b733fde919a068c6878b947d29d06f7ab`.

## Catalogue change

One new row, `grow-computing-scratch-71638`, links
`ICT/Teaching_Packs/index.html#grow-computing`. Its card names Programming with
Scratch, AQA UAS 71638, Level One, eight 40-minute lessons, editable slides,
pupil booklets, paper activities and teacher guidance. It uses the established
ICT family and GROW grouping. Weeks 1–8 remain sequence labels; no half-term
or calendar binding was invented. The neighbouring ICT unit remains accessible.

Source catalogue: 950 → 951 rows; every previous value and relative row order
is preserved. Education-filtered publication: 919 → 920 rows. The existing
filter still excludes the same 31 recreational-game records. Two metadata files
gain exactly one Computing record; none of their previous entries changes.
The original 734-row guard, 101 reviewed appended rows and 116 derived companion
rows remain checked. Both gate copies are identical.

## Admission repair and preflight correction

The initial preflight covered catalogue and browser contracts but omitted the
complete publication admission check. That was insufficient: #513's deployment
failed before publishing. Build 103552590177 reported the first two changed Site
outputs; a full census then identified exactly four changed paths across all
three output trees, with no unreviewed or missing path:

- education-site/data/domain-catalogue.json — one additional Computing record.
- education-site/data/resource-discovery.json — source record count 950 → 951.
- education-lessons/resources.json — the new filtered catalogue row.
- education-lessons/assets/catalogue/terms-and-styles.json — its metadata.

The repair uses Site carrier `d87ad04ff36313a37584dab4feb243e984f0c5fa`, directly
on existing carrier `3c2743fbfb345e1314f138d6b50d6a7ce18031ef`. Independent GitHub
comparison confirms **one registry file, four changed lines**. Each line retains
its previous reviewed digest beside exactly one new digest. No old admission
is removed; there are no wildcards, third digests or new derivation rules.
Builder code, workflow code, source selection, Science baseline and size-table
derivation are unchanged. The caller and its governed digest changed together.
This does not advance Site main's independent publication/source pins.

## Verification and limits

- Schema: eight deliberate invalid cases refused; real catalogue passes.
- Catalogue preservation gate: eight controls pass; 950 prior rows independently
  compared unchanged; all 116 companion records and existing tags check correctly.
- Static contract passes and detects three deliberate mutations. The existing
  1,463-entry source size table still derives without changes or missing files.
- Complete output separation: 4,035 files, 1,644 HTML, 150 manifests, 25,278
  references, 79 migrations, 437 sitemap URLs; zero failures.
- Both prior and new outputs pass admission. All four unreviewed third-value
  controls fail. The full 61-control admission suite passes, including real PASS /
  tracked planted game FAIL / restored PASS. Final publication repeats its gates.
- All 163 Computing unit output files remain byte-identical after catalogue
  generation; no lessons, Scratch projects or awarding-body documents were edited.
- Live Chromium, 390px and 1280px: searches for `71638`, `Scratch` and
  `GROW Computing` each display one matching card with the reviewed text; its
  link opens the Computing section and the existing ICT section remains present.
- All eight live lessons return HTTP 200. After beforeprint and Chromium print
  emulation, each week's own visible paper route is non-empty, has its correct
  week heading and completion text, and exceeds 1,000 characters. Zero page errors.
- Live file comparison: eight lessons, eight pupil PDFs and eight pupil DOCX
  files; **24/24 HTTP 200 and SHA-256 identical** to reviewed assembled output.

The runtime's HTTPS proxy certificate is not in Chromium's trust store, so the
rendering probe accepts that proxy certificate. The independent Python byte
fetches retain certificate verification. No browser certificate/security claim
is made. Browser and file measurements are recorded after final deployment.
The first live browser attempt timed out waiting for network idle. The successful
retry waited for DOMContentLoaded and then the actual required card and print
elements; none of the content assertions was removed.

Literal original G14/G15 paper-only completion and six-outcome parity have not
been newly asserted. Matt explicitly confirmed that normal Scratch work uses
laptops available to every pupil, and work is captured, printed, scanned and
emailed as PDF to the UAS lead for normal review or return. No advance route
approval is required. Existing paper-route printing is not a capture of an
external Scratch project. No pupil scans, observations or completion claims
were invented; no email or speculative route-review PDF was sent.

## Existing findings retained

The broad historical catalogue-static check fails on both baseline and candidate
because 51 older rows lack evidence metadata; 167 lack public term/style metadata.
Only the new Computing record was added in this pass. A broad generator trial
rewrote unrelated companion evidence; those trial changes were discarded. The
existing companion derivation check subsequently passed unchanged.

The stale-evidence sweep also remains red with the same baseline measurements:
1,418 stale claims / 6,307 live / 6,899 row labels / 47 files matching no form,
exit 2. #513's final checks were 13 SUCCESS / two expected SKIP / that one FAIL;
#514's were 12 SUCCESS / two expected SKIP / that one FAIL. Neither audit was
disabled, hidden or labelled green. Final main check states are in the CI record;
no whole-estate green is claimed. All 23 main check records are terminal: 18
SUCCESS and five FAIL (the sweep plus four summaries reporting it). Latest Watch
job 103556050596 reports five PASS workflows / one FAIL / zero pending / zero
without a verdict; the failing workflow is FieldOps 34694242678 because of the
unchanged sweep.

## Durable evidence and continuation

See `rf3-evidence/gc1-p6-review.json`, `gc1-p6-admission-delta.json`,
`gc1-p6-admission-controls.json`, `gc1-p6-release-ci.json`,
`gc1-p6-browser-live.json` and `gc1-p6-served-files.json`. Browser and fetch
scripts are included beside the evidence; their workspace-relative inputs use
the reviewed checkout/output layout recorded by these files.

Do not replay #493, #512, #513 or #514, or Apps #83–#85. The separate P6 catalogue
transaction is finished. SB1 remains due before a second unit and P2Q remains
held until Matt names it. All other programme holds remain in RF3_CONTINUATION.md;
no REGISTER write, brand replacement or unrelated programme release occurred.
