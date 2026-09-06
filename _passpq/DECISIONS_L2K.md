# DECISIONS_L2K.md — pass PEQ-L2K (v2 + Addendum B), 2026-08-22

**Instruments:** `MASTER_PROMPT_Pass_PEQL2K_v2_YearPlan_20260821.md` (sentinels
`peq-l2k-v2-2026-08-21-TOP/BOTTOM`) + `ADDENDUM_B_PEQL2K_AllLevels_GLH_20260821.md`
(sentinels `peq-l2k-addendum-b-2026-08-21-TOP/BOTTOM`); both attached, v2 governs, B
extends Deliverable A to all three levels. Spec PDF v1.2 Oct 2025, 80pp, sha256
`52b06122…7422` (not committed — copyright rule, `inputs/README.md`).

**Base / ROLLBACK:** `2310ea0` (origin/main, > 971b0935). Branch `claude/peq-l2k`.
Companion branches: `claude/peq-l2k-manifests` (Lessons: resources.json + pin only) ·
`Matt-s-Apps- claude/peq-l2k-pin` (the Apps copy of the same pin move). This split is
deliberate: the cross-estate workflow triggers on the pin file and its boundary check
forbids lesson files and the pin moving in one diff, so the registration merges
separately, entirely inside ALLOWED_DIFF — the P6-closure shape.

## §1 Decisions made inside the pass

| # | Decision | Why |
|---|---|---|
| D1 | **The live 12 weeks measure 8.0 GLH** — 12 decks × one 40-min period; the decks program 53 min of slide time each (data-timer sums), so the claimed GLH is the supervised slot, never the programme. Deck→unit assignment follows each deck's banking line (LAUNCH W1–6 → ComSk; GROW W1/2/4/6 → LSk, W3 → TmWk, W5 → ThSk/CrTh per lane). | Addendum B gate: measured, method stated, never asserted. |
| D2 | **Co-delivery is the declared mechanism that closes the E3/L1 ledgers** (E3 7 h · L1 2 h · L2 0 h): one supervised session banked to two units, marked ⊕ per week on the SoW. Grounded in the spec's own model — ComSk plan/use evidence is *expected* to be generated through a challenge leading to another unit (pp25/54), ASDAN's worked plan co-assesses two units weekly, and E3 qual GLH (134) already sits below the six-unit sum (140). | Physical 133 h at 3.5 h/wk cannot equal 140 unit-GLH any other honest way; the alternative was overstating the deck hours. |
| D3 | **The Award pair is DecMk+TmWk in every lane** — unit GLH equals the Award's qualification GLH exactly at all three levels (40/36/32), and both units complete by W14. Extended adds Com+LSk (Easter); Certificate adds Th/CrTh+Wellb (summer). | The only pairing whose arithmetic lands exactly; same ladder in all lanes keeps the mixed room on one spine. |
| D4 | **L1 14-of-15 default:** all six L1 units taught and evidenced (15 cr; §5.1 permits exceeding); the named exact-14 fallback is five L1 units + ThSkE3. Question lodged in `QUESTIONS_FOR_CHERYL.md`. | Addendum B §B0 demands the default named, not implicit. |
| D5 | **The L2 route panels ride the existing guide machinery** — `data-mbm-guide="1"` + `data-l2route="1"`, the ⓘ Guidance toggle, key `mbm_guide_v1`. The master prompt's `data-mbm-route` does not exist in this repo; `data-mbm-guide` (guidepatch pattern) is the real attribute. | Use the estate's machinery as the prompt intends, not a second toggle. |
| D6 | **The print mirror (`#print-l2route`) prints only while the route toggle is on** — `printPack` gains one guarded line. The three standard packs stay text-identical bar the ruled strings, proven exactly (`l2k_printparity.mjs`: transform(base) === head, 6/6). | Reconciles "print mirror included" with "print-text-identical". |
| D7 | **One non-additive witness word:** "never both" → "never more than one" (three levels made the two-level wording false on a moderation-facing sheet). Everything else on the witness sheet is additive (the L2 tick box, the extended mapping sentence). | Leaving it would state a falsehood beside the assessor signature. |
| D8 | **The four standing "no Level 2" surface statements re-scoped** to "a staff-directed Level 2 route sits in-deck — registration at any level stays a coordinator decision" (+ the SoW's "Any L2 registration is a coordinator decision — none is claimed here"). | The ruling made the old sentences false; silence would contradict them. |
| D9 | **`data-speak-text` included on every panel** although the ASDAN chassis has no speech layer (it is a sci-v3 convention) — inert but present, per the prompt. PROPOSED P1. | Prompt-mandated; harmless. |
| D10 | **Protected manifest: +9 rows appended surgically** (7 `brandMBM` rows for the new Kitchen pages, 2 declared `kitchenfood` windows), never a wholesale rebuild — a rebuild was tried, shown to rewrite 157 unrelated baseline lines (erasing the standing authorised-delta record), and reverted. The E3 TSV rows for the six LAUNCH decks now name both rulings. | The gate's record of 75 authorised shifts must stay visible. |
| D11 | **New food content declared with its selector:** `protected.js` gains `kitchenfood` windows (`/blind taste test|allergen|no diet, calorie, weight or body framing|supervised bench/gi`) scoped to `GROW_ASDAN/PEQ_L2_Kitchen/`; existing food windows untouched. | Master prompt §4 food-census clause, by the existing declaration mechanism. |
| D12 | **resources.json appended textually** (2 entries before the closing bracket) after a `json.dump` rewrite was shown to reformat 88 escaped legacy rows, and reverted. Registered: the SoW page (`type: support`) + the Staff Guide as the resource hub (`type: teacher`), existing chips/subjects only, "working towards" in both titles. | Append-only union discipline. |
| D13 | **The L2 sweep whitelists the 29 short-course decks' `Stretch (L2 standard)` stems + ENT_W6's companion line + the v3 mirror's meta-statement** as inherited, held-out strings (DECISIONS.md §3 J5) — not PEQ claims, not this pass's scope. | The sweep must red on PEQ L2 claims without re-litigating a recorded hold. |

## §2 Gate record (every gate run at branch tip; controls deliberately fired)

| gate | result | fired control |
|---|---|---|
| §0 anchors — SPEC_FACTS_L2 §V (v2 + Addendum B0, 26 rows) | **verified, no mismatch, no STOP** | — |
| ledger proof `l2k_plan.py` (sums · milestones · windows · weekly 210 min) | **PASS** (build asserts before writing) | mis-set W14 by −10 min → `E3 W14: physical 200 != 210` **RED**, reverted |
| matrix zero-gap (174 ACs / 18 units) `l2k_build.py` | **PASS — 0 gaps** | `L2K_PLANT_GAP=1` → build refuses, exit 1 **RED** |
| pass gates `l2k_gates.py` G1–G5 (re-proof · page drift · xlsx values · cross-level minima · required statements) | **ALL GREEN** | `L2K_PLANT_XLEVEL=1` (E3 sheet given the 500-word L2 figure) → G4 **RED** |
| build idempotence | rebuild → 7/7 pages byte-identical | — |
| `v3_tier_gate.py` (minima-carry-level · tier stems · L1 sweep · **new L2 sweep**) | **PASS** — 12 decks · 169 live files · 0 unruled L2 strings | planted `Banks: ASDAN PEQ Level 2 Certificate` in a GROW deck → **RED**, reverted |
| `minima_gate.py` | 44 surfaces **PASS** | — (fired in PEQ-E3) |
| `verb_gate.py` | 0 off-pitch | — |
| deck patcher idempotence + reversibility | re-patch: 0 changed · strip → `git status` clean (byte-identical to base) | — |
| PART B Chromium `l2k_partb_gate.mjs` (390/768/1440) | 6 decks × 3 viewports: default-hidden · toggle · aria-pressed · `mbm_guide_v1` persistence across reload · toggle-on pack gains `print-l2route` · all three default packs free of it · zero errors (known `/hud.js` 404 filtered) — **ALL GREEN** | — |
| print parity `l2k_printparity.mjs` vs base `2310ea0` | 6/6: head print text == base + **exactly** the ruled transforms | divergence check is the gate itself (char-diff on any drift) |
| protected gate `protected_gate_e3.py` | 75 window shifts all authorised · every marker count unchanged · +9 manifest rows are the only manifest delta | wholesale-rebuild attempt showed 157-line drift → reverted (D10) |
| sentinels 50/123 | set-identical to base, counts hold | — |
| deck JS parse + `node --check` on touched tools | clean | — |
| chip gate `verify_lessons_chips.mjs` (served origin, with the 2 new entries) | **28/28 limbs PASS**, zero console errors | — (clicking IS the control) |
| `pin_manifests.py` | both copies re-pinned in one run, byte-identical (`resources.json 2bb276fe2a3f → de9e7c615153`) — carried on the manifests/pin branches | `--self-test` available; preflight refused single-checkout earlier in P6 |
| cross-estate `verify_cross_estate_unification.py --base origin/main --canonical <clone>` | boundary check **correctly red** on lesson-files+pin in one diff → drove the branch split above; the follow-up branch's diff is resources.json + pin only (ALLOWED_DIFF) | the red WAS the control |

## §3 The witness deltas, verbatim (additive-only audit)

1. Tick row: `☐ Entry 3 ☐ Level 1` → `☐ Entry 3 ☐ Level 1 ☐ Level 2` (addition).
2. Guidance sentence: "…Entry 3 *or* Level 1, never both (…§6.5). Supported and Standard
   evidence Entry 3; Stretch evidences Level 1." → "…Entry 3, Level 1 *or* Level 2,
   never more than one (…§6.5). Supported and Standard evidence Entry 3; Stretch
   evidences Level 1; the staff-directed Level 2 route evidences Level 2." (one word
   replaced — D7; the rest additive.)

## §4 Phone-checks after merge

1. **The SoW page** (`GROW_ASDAN/PEQ_L2_Kitchen/Scheme_of_Work.html`): the sensitivity
   table shows four rows (2/3/3.5/4 h/wk); the E3 lane ledger's totals row reads
   30·20·20·20·20·30 with "7 h" co-delivered; W14/W26/W38 rows are shaded milestones.
2. **One LAUNCH deck** (`LAUNCH_ASDAN/PEQ/PEQ_W4_Plan_a_Communication_Activity.html`):
   on load NO "Level 2 route" panel is visible; tap **ⓘ Guidance** — the panel appears
   on the Independent Work slide ("TWO plans covering two DIFFERENT ways"), and survives
   a reload; tap again — it hides. The award chip reads "…Entry 3 (Level 1 · Level 2
   routes)…".
3. **Teacher Print Tools** on the same deck with guidance OFF: the printed pack has no
   Level 2 route page; with guidance ON it gains one.
4. The witness sheet (any deck's print pack) shows three tick boxes: Entry 3 · Level 1 ·
   Level 2.
