# Pass CLOSE-1 — DECISIONS

## Identity gate 4/4 PASS: 2ce19ce · e888cc1 · 210c669 ancestors · Science_Teesside=25
## Rollback SHA (origin/main before any commit): 210c669743c466e4a595813f52a59543a1172a2b
## Branch: claude/close-1-reconcile · Matt authorised MERGE TO MAIN this pass after §5 stop.

## §1 PRE-FLIGHT
### §1.1 parked-branch collision matrix (0 overlap with the 18 art files)
- pass-sbx-art-a2 (head 462cfa6): 11 files — Art_Teesside 7, _passsbx 3, resources.json 1. Overlap w/ 18: 0
- pass-art-a2b   (head 952d260):  3 files — Art_Teesside 3.                       Overlap w/ 18: 0
- The 18 art targets live in Grow/Slideshows, Launch/Slideshows, Launch/ — disjoint from both branches
  (which touch Art_Teesside/, a different tree). No file excluded by collision. Branches NOT touched.
### §1.2 freeze status: NO live freeze on the 18 targets.
- Reduced-motion (e3082d2, Art_Teesside 31) is a COMPLETED pass, not an active freeze; REGISTER records
  "no freeze happened". Constraint noted: reduced-motion blocks must stay invariant in any edit.
- Protected blob Art_Teesside/Grow/GROW_ART_W8 (4cf5d81e, SG) is a DIFFERENT tree from the target
  Grow/Slideshows/GROW_ART_W8_Festival_Sounds.html. Parked pass-sbx-art-a2 unmerged/report-only.
- Verdict: science ships; art is investigation-only in §3; art application waits for Matt (§6).
### §1.3 derivation at HEAD 210c669: loop-mark 70 · written-line 48 · both 0 — holds.

## AMBERs (logged at time)
(entries appended inline)

## §2 SCIENCE RE-CLOSE — DONE + gated (committed 53dbc5a)
- Byte-identity gate PASS: GROW & LAUNCH deployed closure element identical (343b).
- 20 decks: removed ring <tr> + lm-own + loop-mark <style> block; installed written-line closure in
  print-lundy (copy verbatim). Screen surface carried no ring (print-only) — unchanged.
- Render gate: 40 renders (http+file://) x3 tiers — 0 console err, print pack populated, marker on paper.
- Sentinel (working tree): loop-mark 70->50, written-line 48->68. Matches expectation exactly.

## §3 ART INVESTIGATION — classify only, NOTHING changed
- LL-G loop-mark scope was "15 BUILD lessons" — the 18 art files were NEVER in LL-G scope.
- All 18 carry NO Lundy zones but a full Arts Award evidence-flow closure: "Capture your evidence"
  slide (authorship "what it shows about my progress" + "my next step — the one I mean" + witness
  statement "thinking WITNESSED, not performed"), ending "Lesson complete!".
- Subject is Arts Award (REGISTER P3: resources.json Art->Arts Award relabel, Arts Award=8).
- VERDICT all 18: ALREADY-CLOSED-DIFFERENTLY (mechanism: Arts Award evidence-capture / authorship /
  witness / next-step) AND DELIBERATE-DIVERGENCE (Arts Award pathway has its own closure; cite REGISTER
  P3). GENUINELY-OPEN: 0. Matt's §3b warning confirmed — the "neither marker" was not a gap.

## §4 ASSESSED PAIR — proposed diff only, R-A01 untouched
- GROW_HUM_W7 + LAUNCH_HUM_W7: no print-lundy, no written-line; ★ASSESSED supervised-conditions.
- Closure would sit OUTSIDE the conditions block (print pack is separate from the screen assessed card);
  R-A01 NOT engaged. Exact proposed insertion before print-feedback -> _passclose1/assessed_pair_PROPOSED.diff
- CHANGE NOTHING. Caveat: full S/V/A/I zones would be authored (RED); minimal diff adds the marker only.
  Open question: should a supervised assessed lesson carry pupil-voice closure at all.
