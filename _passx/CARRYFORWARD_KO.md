# CARRYFORWARD — the 114 KO candidates (for the NEXT pass)

**This is a CHARACTERISATION: shape and counts only. It states no verdict on any individual KO.** Produced
with the repaired `ko_staleness.py` on a **full clone** (assumptions banner: full clone · 161-file KO corpus ·
network not required · co-modification is a proxy, not consistency). Cardinality re-asserted: 114 + 3 arch +
44 clean = 161 = KO files.

## What a candidate IS (and is not)
A candidate is a file whose **visible body** last moved *after* its KO block last moved, in a **content** pass.
It reads no content and makes no correctness judgement — `ko_staleness`'s own blind twin is a KO and body that
moved in the *same* commit but inconsistently, which it cannot see. **A candidate is a file to READ, never a
defect.** The 44 "clean" are UNCHECKED, not verified.

## Shape of the 114

### Class split — the single most useful cut before triage
| class | count | what it means for the next pass |
|---|---|---|
| **R-E07 Loop-Mark artefact** | **39** | first body-mover is a `Pass LL-G sub-pass … Loop Mark` commit — visible text added to **print-feedback**, which a KO does not summarise. REGISTER **R-E07** predicted exactly this and says *do not read these as stale organisers*. **Very likely instrument noise; cheapest to clear first, by confirming the mover is the Loop Mark and the KO text is unchanged.** |
| **other body-mover** | **75** | genuine candidate-for-reading population — a content pass moved the body after the KO. Still a LIST, not a count of defects. |

### By area (all 114)
| area | n | note |
|---|---|---|
| BUILD_ASDAN | 31 | overlaps heavily with the 39 Loop-Mark artefact set |
| Art_Teesside | 28 | movers dominated by "LAUNCH_HUM parity", "Pass C Arts Award", "Art Pass J/L" |
| GROW_ASDAN | 18 | |
| Build | 14 | |
| Grow | 8 | includes 1 assessed (below) |
| Launch | 8 | includes 1 assessed (below) |
| biology | 3 | |
| chemistry | 3 | |
| 2 Physics 10 | 1 | |

### The 2 assessed candidates — READ FIRST, alone, against the Card (not the body)
- `Grow/Slideshows/GROW_HUM_W7_Write_The_Account.html` ★ASSESSED — HANDOVER §7 / R-G02 flag it: its first
  content mover class includes `Pass LL-A2a`, which **removed the Connective Bank and Evaluation Deployments**.
  If its KO names either, the KO describes support that no longer exists — a fourth surface disagreeing.
- `Launch/Slideshows/LAUNCH_HUM_W7_Source_Assessment.html` ★ASSESSED.
- **Nothing `★ ASSESSED` is triaged, edited, or verdicted by the next pass without Matt's key and the
  assessed-file diff discipline (one hunk, inside the intended block).**

## Suggested triage order & cost (for the next pass to cost itself)
1. **Clear the 39 Loop-Mark artefacts** (cheap, mostly mechanical confirmation vs R-E07) → expected to drop the
   live list toward ~75.
2. **The 2 assessed** — highest consequence, lowest count; Matt's key, read against the Card.
3. **The remaining ~73 by area**, chassis by chassis (BUILD_ASDAN / Art_Teesside cluster first — largest).

**No KO was read for content in Pass X. This table is where the next pass starts, not a result about any file.**
