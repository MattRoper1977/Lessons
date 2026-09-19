# HUM-D5 — STATE

Resume at the first phase not marked done.

| phase | state | note |
|---|---|---|
| A0 INTAKE       | **BLOCKED — STOP at intake** | 92 of 120 lessons in hand; 2 RE packs missing |
| A1 PROOFREAD    | not started | needs the full 120, or a ruling to proceed on 92 |
| A2 APPLY CLASS A| not started | |
| A3 CHECKS E1-E18| not started | |
| A4 CLOSE PART A | not started | |
| PART B          | not started | hard-gated; see INFLIGHT.md |

## A0 intake result (2026-09-19)

Packs attached to the order: 13 zips, 12 distinct.
RE_Autumn_GROW_Final.zip was uploaded TWICE and the two are byte-identical
(md5 2de3d2c9c6430ea7d80a01f895b2dbff, 13460339 bytes both). One copy used.
That is a duplicate upload, NOT two generations, so it is not the "two
generations for one lesson id" STOP.

### Missing inputs — this is the STOP
  RE_Autumn_BUILD_Final.zip     NOT SUPPLIED
  RE_Autumn_LAUNCH_Final.zip    NOT SUPPLIED
28 of the 42 RE lessons are therefore absent (BUILD 14 + LAUNCH 14).

### SHA256SUMS verification
  HUM_Autumn_1_LAUNCH_Final          PASS   96 files
  HUM_Autumn_2_BUILD_Final           PASS  120 files
  HUM_Autumn_2_GROW_Final            PASS  110 files
  HUM_Autumn_2_LAUNCH_Final          PASS  114 files   (both zip halves, merged)
  HUM_Spring_1_BUILD_GROW_Final      PASS  183 files
  HUM_Spring_1_LAUNCH_Final          PASS   83 files
  HUM_Spring_2_BUILD_GROW_Final      PASS  193 files
  HUM_Spring_2_LAUNCH_Final          PASS  103 files
  RE_Autumn_GROW_Final               PASS  201 files
  HUM_00_SoW_and_Order               NOT RUN — pack contains no SHA256SUMS.txt
  HUM_Autumn_1_BUILD_GROW_Fallback   NOT RUN — pack contains no SHA256SUMS.txt

### Generation check — all Final, despite the folder name
Every Final zip contains a folder named *_Reviewed/. The order withdraws the
Reviewed GENERATION, whose marker is missing exit quick-checks. Measured: all
92 *_Lesson.html files carry #vary-exit AND a starter block (#vary-starter or
#re-starter), 92 of 92. The folder name is legacy; the content is Final.
CHANGELOG_Final_2026-09-19.md present in all 9 Final packs (absent from the
SoW pack and the Fallback, neither of which is a Final pack).

### Lessons in hand: 92
  Humanities  78 of 78  COMPLETE
    Autumn 1 BUILD+GROW  14 (Fallback generation - R13)
    Autumn 1 LAUNCH       7
    Autumn 2 BUILD        7 | GROW  7 | LAUNCH  7
    Spring 1 BUILD+GROW  12 | LAUNCH 6
    Spring 2 BUILD+GROW  12 | LAUNCH 6
  RE          14 of 42  INCOMPLETE
    Autumn GROW          14
    Autumn BUILD          0  pack not supplied
    Autumn LAUNCH         0  pack not supplied

### R13
HUM_Autumn_1_BUILD_GROW_Final.zip was NOT supplied; the Fallback was.
So the Fallback path is the live one: those 14 rows carry
generation="fallback-2026-09-19" in the report and lead the residue list.
Both were not supplied, so the "never land both" clause is not engaged.

---

## A0 RECONCILIATION (ordered 2026-09-19) — the answer is §3, not §2

The intake record and the A0 index did not disagree; they described two
different moments. Intake ran BEFORE RE_Autumn_BUILD_Final.zip and
RE_Autumn_LAUNCH_Final.zip were supplied. They arrived in the message
carrying the ruling, were verified on arrival, and the index was built after.
Nothing was miscounted, so correction #10 does not apply.

### Measured population, by the real pattern *_Lesson.html
  HUM_Autumn_1_BUILD_GROW_Fallback  14      RE_Autumn_BUILD_Final    14
  HUM_Autumn_1_LAUNCH_Final          7      RE_Autumn_GROW_Final     14
  HUM_Autumn_2_BUILD_Final           7      RE_Autumn_LAUNCH_Final   14
  HUM_Autumn_2_GROW_Final            7
  HUM_Autumn_2_LAUNCH_Final          7      HUM_00_SoW_and_Order      0
  HUM_Spring_1_BUILD_GROW_Final     12        (SoW pack, correctly not
  HUM_Spring_1_LAUNCH_Final          6         counted as lessons)
  HUM_Spring_2_BUILD_GROW_Final     12
  HUM_Spring_2_LAUNCH_Final          6      TOTAL                   120

By pathway, from the filename: BUILD 26 / GROW 26 / LAUNCH 26 = 78 Humanities;
BUILD_RE 14 / GROW_RE 14 / LAUNCH_RE 14 = 42 RE.

### The 28 that were NOT SUPPLIED at intake are now SUPPLIED
  RE_Autumn_BUILD_Final.zip   12931456 bytes
    sha256 70b1c36e882a056a406d4120605ffca72cd7b225ba1aa3d055404661c45134f9
  RE_Autumn_LAUNCH_Final.zip  14421087 bytes
    sha256 5bb70f0ca5cd3412c371d0f8d4d50771c3c8da249c1985a438d58b742aec5803

  SHA256SUMS re-verified: BUILD PASS (201 files), LAUNCH PASS (201 files).
  Generation: 14/14 carry #vary-exit AND a starter block in each pack;
  CHANGELOG_Final_2026-09-19.md present in both. Final, not Reviewed.

### Rendered pass scope
  on disk 120 | static index 120 | rendered index 120 | missing none
  RE BUILD 14/14 rendered, RE LAUNCH 14/14 rendered.
  NOT RUN files: 0 entries in both. The per-lesson pageerror -> NOT RUN rule
  stands and fired zero times because zero lessons raised a page error.

The intake record's "NOT SUPPLIED" is superseded for these two packs. The
report carries them as supplied, with the arrival hashes above.
