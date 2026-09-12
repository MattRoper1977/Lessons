# Pass SEMH-2 — proposed diff sets (Matt reads; NOTHING here is applied)

**STATUS: PROPOSED — every diff in this folder is emitted for Matt's read and applied
nowhere by this pass.** All three sets verified `git apply --check --whitespace=error-all`
clean at base `84f4f31`. Claim-accuracy / safety-wording only: no task design, no timings,
nothing a pupil does changes in any hunk.

## 1 · `proposed_dt_dust_ht.diff` — OPEN_ITEMS #18 re-emitted at HEAD (§4)

**Status: PENDING-LOCAL-APPROVAL intact (H&S / COSHH / technician rows in
`quality/toolkits/PENDING_APPROVALS.md` govern). The #18 unlock condition is met (#34 merged
at `6e7317f`, an ancestor of HEAD) — the diffs are appliable but touch the protected v5 D&T
decks, so they wait for the D&T lead + local sign-off.** 4 files, 7 hunks, wording drawn from
the ruled accounts in `quality/toolkits/SAFETY_CONTENT_GATE.md` (dust hierarchy; reclaimed
timber acceptance):

- `BUILD_DT_W5_Finish.html` — the blanket "Dust masks for sanding" line becomes the ruled
  prevent → extract → RPE order with the named stop condition; "the door stays open" as the
  stated ventilation control becomes the centre's-arrangements form with the same stop
  condition. Sensory-week access framing kept.
- `BUILD_DT_W1/W2/W3` print cut-list — "HT wood only" becomes the ruled six-check acceptance
  (HT stamp one check of several; reject on any one failure even when HT-stamped). The
  pupil-facing rule "If a row does not say HT in the Material box, do not cut it" is kept
  verbatim.
- `BUILD_DT_W2/W3` pre-tool line — "HT pallet wood only" becomes "accepted wood only
  (HT-stamped and passed every acceptance check)". Line rhythm kept.

**Not touched:** printPack id lists, the Lundy print-page text (R-A07 BOUNDARY / OPEN_ITEMS
#7), timings, tasks.

## 2 · `proposed_tbc_unit_code_hide.diff` — the derived 25 (§5.1)

**Derivation (re-run, never quote):** tracked files containing `unit code: TBC` = 30; minus
5 documentation/tooling carriers (`REGISTER.md`, three `quality/` registers,
`_passsci1/render_v5.py`) = **25 Science_Teesside lesson files** (Build 5 · Grow 5 ·
Launch 15), exactly one instance per file, all on the witness-statement print header.
Matches SEMH-1's historical count by fresh derivation.

**The mechanism, byte-reversible:** the provisional sentence
`AQA UAS unit code: TBC (Cheryl).` is wrapped in a marked HTML comment
(`<!-- semh2-hide (reversible; restore on Cheryl's confirmation): … -->`). The `<br>` and the
rest of the header line are untouched — no layout break; the code returns the moment Cheryl
confirms by deleting the comment markers. Greppable marker: `semh2-hide`.

**Why proposed, not applied:** pupil-adjacent print surfaces — Matt's read stands
(OPEN_ITEMS #17(a)).

## 3 · `proposed_constructed_source_labels.diff` — LAUNCH Humanities (§5.2)

**Derivation over the seven non-assessed LAUNCH_HUM decks** (W7 excluded — assessed pair
untouched): the constructed-source instances are —

| deck | instances (TRUE-in-substance, mis-cited) |
|---|---|
| W1 Source_Investigation | the teaching archive: port tonnage ledger 1901–09 · 1907 quay photograph · 'Bustling dock' postcard · 1908 strike report · trade directory (1905) · docker's 1950 memoir · 1906 crane investment minutes |
| W3 Archive_NOP | the NOP specimen attributions ('Written at the works office, 1871' · 'Made to pull men north' · 'Sent to shame the council into action' · siblings in the same sort exercise) |
| W4 Century_Of_Change | the paired 1915/2015 street-corner photographs (a framing device; lightest instance) |
| W2 · W5 · W6 · W8 | **none** — W6's "90,000 by 1901" is the real census figure (a fact citation, judged real, not relabelled); W8's OS maps are real artefacts |

**One wording style** ("… reconstructed from period records for this lesson …"), one label
per presenting surface (screen + print twin), never per-mention: W1 ×2 insertions, W3 ×2,
W4 ×2. The teaching is not undermined — the label says the substance is documented Teesside
history; only the specific documents are declared illustrative.

**Why proposed, not applied:** pupil-facing lesson surfaces — Matt's read stands
(OPEN_ITEMS #17(b)).
