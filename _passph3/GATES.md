# PH-3 GATES — every gate, with the number behind it

Run environment: Python 3.11.15 · Node v22.22.2 · jsdom 30.0.1 (npm reachable) · pdfplumber
0.11.10 · openpyxl (temp venv). FACTS MODE (no `_asdan_private/`). Gate harnesses live in the
session scratchpad; every run's method is described inline below. Job A gates were re-run after
**every** A-step commit; the numbers below are from the final run.

## Job A (G1–G9) — ALL PASS

| gate | result | the number behind it |
|---|---|---|
| G1 content preservation | **PASS** | Protected food-safety sentence ×1, three-line before-teaching checklist ×1 (byte-exact incl. its embedded newlines), C7 sentence present unchanged (HELD); §5 Learner-confirmation 79/79. Byte-diff confinement proven in the strong form: for each of the 26 touched files, stripping the authorized insertions and reversing the authorized replacements reproduces BASE **byte-identically** (26/26). |
| G2 additive-by-default | **PASS** | Deletions outside authorized A2/A5 replacements: **0** — same byte-reversal proof (these single-line files make line-count deltas meaningless, so the gate was run on content, the stronger form). |
| G3 doubled tokens | **PASS** | `\b(\w+)[  ]+\1\b` case-insensitive over every inserted/replaced text segment: 0 hits. |
| G4 duplicate blocks / placeholders | **PASS** | `peq-comsk1-minima` ×1 + `peq-comsk1-minima-print` ×1 in W4 and W5 each, 0 elsewhere; `peq-facts-panel` ×1 in each of 17 files, 0 elsewhere; placeholder strings (TODO/TBC/lorem/[insert/"Staff qualification route: see") in new text: 0. |
| G5 pupil-text register | **PASS** | Changed pupil-surface strings = exactly the 8 registered A2 edits (`PUPIL_TEXT_REGISTER.md`); replacement-presence asserted 1× each; nothing else changed in any `.task-box`/tier/arrival/exit/answer/match-pill/WAGOLL/KO surface (byte-reversal covers the complement). |
| G6 facts | **PASS** | All numbers in new blocks match §2.3 (3/4/3/4/3·8·250/3/2/2 · 4-9-14 · 15 · 3 adjacent · 3 years · 31 Aug 2026 · 31 Dec 2026 · 31 Aug 2027). Banned strings in new text: 0. `10-hour` appears **only** inside the two authorized negation sentences (A1 block "There is no 10-hour plan-use requirement on Communication"; A3 panel "applies to every skill except Communication"). New unit-code tokens: ComSk1 only, on the two pages that already carry it. |
| G7 idempotence | **PASS** | A1, A2, A3 apply scripts each re-run → 0 changes (assert-before-replace + presence keys). |
| G8 well-formedness | **PASS** | `html.parser` + tag-balance depth 0 on every touched file; print-section count per file unchanged; script blocks byte-identical on all Job A files (5/5 blocks in W4, 5/5 in W5, all others). |
| G9 estate | **PASS** | ASDAN html 101; lessons w/ Learner confirmation 79; ComSk1 total 92 = 84 + 8 authorized (4 A1 blocks ×1 + A2 net 0 + A1 print ×1 each… enumerated in harness as inserts 8 / replacements net 0); sentinel + hud loaders unchanged (also re-proven under B-G6). |

## Job B (B-G0–B-G7) — ALL PASS

| gate | result | the number behind it |
|---|---|---|
| B-G0 inventory first | **PASS** | `GUIDANCE_INVENTORY.md` committed at `fd95fff` before any deck was written to. |
| B-G1 reversibility | **PASS 85/85** | remove marker+style+script+button, unwrap spans, strip attrs → byte-identical to the pre-Job-B tree (= BASE for 82 decks; BASE+authorized-Job-A for W4/W5/DT-W6). |
| B-G2 idempotence | **PASS** | second apply: 0/85 patched, zero diff. |
| B-G3 print purity | **PASS** | `data-mbm-guide` inside any `#print-area`: 0/85; print-section counts unchanged 85/85; every pre-existing script block (incl. `printPack` id lists) byte-identical 85/85. |
| B-G4 protected lines | **PASS** | protected D&T strings inside tagged elements: 0; id'd elements inside any tag/wrapper: 0 (`#pres-num`/`#match-score` outside their wrappers by construction, verified). |
| B-G5 runtime | **PASS 85/85** | jsdom 30, https origin + repo-mapped resources: 0 console errors (expected `/hud.js` absence + jsdom CSS-parser noise excluded); default hidden (computed display:none); button/aria/storage flip; `g`/`G` toggles, ignored in modals; arrows navigate; TA Brief + Cold Call open; `mbm_guide_v1='1'` honoured on reload; asvl-panel rendered on **48/48** visual-upgrade decks with `.asvl-purpose` hidden, `.asvl-notice` visible. |
| B-G6 estate invariants | **PASS** | `node --check` on 263 unique inline script blocks: 0 failures; div balance unchanged 85/85; `ll-g:loop-mark` per-deck counts unchanged and repo-wide bearing set = **50 files = BASE** (LAUNCH none); hud loader per file unchanged; new absolute URLs 0; new `<script src>` 0. |
| B-G7 pupil-visible text | **PASS** | per-slide tag-stripped text equal to pre-Job-B for every slide of all 85 decks (button text lives in `.controls`, outside slides). |

## Job C — ALL PASS except C5 (STOPPED by rule)

| gate | result | number |
|---|---|---|
| Measurement match | **PASS** | `asdan/app.html` at site BASE: sha `e92239177d06`, 89,692 B, Progress×8, ComSk1×6, PROVISIONAL_LINE present, `Level 2` 0 — all equal §6. |
| C1–C4 exact-match apply | **PASS** | 10 replacement groups, each asserted at its expected count, idempotent (2nd run: 0). Diff scope: `asdan/app.html` only (+ docs report). |
| `node --check` | **PASS** | 0 failures over all inline blocks. |
| Runtime (jsdom + fake-indexeddb) | **PASS** | boots clean; 3 presets render (new ceilings + provisional line); `PATHWAY_MINS`=53; 14/14 seeded slots `mins:53`; `creditsFromHours` unchanged (53→5, 9.9→0); v2.5-format backup imports through the real `#bk-file` handler; saved `centre` beats the new fallback. |
| Request surface | **PASS** | http(s) refs 4 = base 4; `<script src>` 1 = 1; hud loader retained. |
| C5 PDFs | **STOPPED** | no generator exists in either repo (searched); binaries not hand-edited; the exact stale sentences are quoted in `JOB_C_REPORT.md`. |

## UNPROVEN (stated, not hidden)

- **Live deployment rendering**: the Pages API and madebymatt.uk are proxy-blocked from this
  session — no live browser load is claimed anywhere. Verification is git truth + local file
  checks + jsdom. **Matt phone-checks after merge** (list in the HANDOVER queue entry).
- **BOOKLET-mode items**: GROW W3/W5 per-criterion mapping UNDETERMINED (FACTS MODE).
