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
