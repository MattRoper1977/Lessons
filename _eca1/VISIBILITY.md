# ECA-1 PART B — visibility census and gate record

Mechanism: PH-3's estate toggle extended. `data-mbm-guide="staff|route|lundy"`,
CSS hides tagged elements unless `html.mbm-guide-on`; "ⓘ Guidance" button in the
controls bar; key G (guarded against inputs and open modals incl. science
`.overlay.visible/.open`); `localStorage mbm_guide_v1`; default hidden; print CSS
untouched. Hidden means CSS-hidden, never removed.

## Tag census (measured at apply; uniform per chassis, 0 AMBERs)

| chassis | files | staff | route | lundy | wraps | toggle installed |
|---|---|---|---|---|---|---|
| v5-asdan | 79 | (PH-3's set already on) | (sow-strip already) | 316 (4/deck, Lundy Loop slide) | 0 | PH-3 (verified) |
| v5-dt | 6 | (PH-3's set) | 6 ("🧭 Coming next"/"And that's the unit", Exit) | 24 | 0 | PH-3 (verified) |
| v5-art | 31 | 186 (How it works/Instructions/Step 1–2/Why + Steps:) | 31 (sow-strip) | 124 | 62 (counter boxes) | ECA-1 |
| hum-v4 | 24 | 168 (Instructions/How to play/Why + Steps:) | 24 (sow-strip) | 96 | 24 | ECA-1 |
| sci-v3 | 35 | 110 (voice-keyed notes + teacher-say) | 13 (source-note ×2 GROW + retr-declare ×3) | 280 (8/deck — every slide EXCEPT exit) | 25 (TA-fade tails) | ECA-1 |

KEEP visible by rule: Key Idea/Key Question/Spark, 👀 captions, tier toggles+tasks,
word banks, WORD HELP, `.award-strip`, Teacher Print Tools, `.asvl-notice`,
Cold Call/TA Brief buttons, exit tickets, whole print pack, "← Lessons" (NAV-1),
"Last lesson (Recall)" arrival retrieval headers (task content, not route),
science `retr-route` access lines + pupil-voiced access notes (PROPOSED_B §3).

## Gates (all green, whole 175-deck universe)

- **Reversibility**: `guidestrip.js` on every patched file → `git diff` EMPTY vs the
  pre-patch HEAD — byte-identical per file, all 175.
- **Idempotence**: second `guidepatch.js` run → changed:false ×175.
- **Print identical**: Chromium `emulateMedia('print')` body text recorded pre-patch
  for all 175 and byte-compared post-patch — identical ×175.
- **Default hidden asserted in Chromium** ×175: every `[data-mbm-guide]`
  `display:none` at first load; button present `aria-pressed=false`; G reveals all
  tagged elements and stores `mbm_guide_v1=1`; G again re-hides and stores 0; zero
  page errors. (Negative control: pre-patch the same assert failed on exactly the
  90 not-yet-patched decks and passed on PH-3's 85.)
- **Keyboard/focus**: ArrowRight/ArrowLeft slide nav and Escape verified per chassis
  exemplar post-patch; the button is in the controls bar tab order.
- **jscheck** 659 blocks OK · **sentinels 50/123 set-identical** · **PROTECTED
  IDENTICAL** (manifest defined over the guide-stripped view, which reversibility
  proves equals HEAD bytes) · boot clean.
- Contact sheets: `_eca1/visibility/{v5-asdan,v5-dt,v5-art,hum-v4,sci-build,
  sci-grow,sci-launch}/` — 3 slides × default/revealed × 390/1440.
