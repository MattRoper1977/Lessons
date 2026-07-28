# Pass SL — Art_Teesside/Launch Re-alignment — MAPPING PROPOSAL (design-first; awaiting Matt's approval)

**No Art file touched.** This is the map Ruling 2 requires before any build. Approve or amend, then I build on `pass-sl-sow-launch`, one class per commit, gates G1–G6.

## The governing finding: the SoW itself splits the award across the year
Derived from `LAUNCH - Autumn/Spring/Summer` Creative Arts rows:

| SoW slot | Topic | Silver/Gold parts implied |
|--|--|--|
| **Autumn Aut1** (7 wks) | Identity, arts & **developing as an artist** (Unit 1) | 1A, 1B |
| **Autumn Aut2** (7 wks) | **Experiencing & reviewing** the arts (Unit 1) | 1C, 1D |
| **Spring Spr1** (6 wks) | **Arts leadership & sharing skills** (Unit 2) | 2A, 2B, 2C, 2D |
| Spring Spr2 (6 wks) | Researching arts pathways (Gold) | (Gold) |
| **Summer Sum1** (6 wks) | **Leading an arts project** (Unit 2 / Silver consolidation) | 2C, 2D, 2E |
| Summer Sum2 (7 wks) | Portfolio completion, moderation & celebration | 2E, certification |

**So the SoW places Unit 1 in Autumn and Unit 2 leadership in Spring/Summer.**

## Current suite (grounded @ 32ca685; tags hyphen-range-aware, self-test passed)
| Wk | Title | Silver part(s) tagged | Unit |
|--|--|--|--|
| W1 | Frame the Local Challenge | 1A | 1 |
| W2 | Practice Careers & Pathways | 1D | 1 |
| W3 | Implement & Critically Develop | 1B | 1 |
| W4 | Arts Experience: Attend, Analyse & Share | 1C | 1 |
| W5 | Design the Leadership Project | 2A, 2B (+1D) | 2 |
| W6 | Pilot, Lead & Adapt | 2C, 2D | 2 |
| W7 | Deliver & Curate the Arts Project | 2C, 2D (+1C) | 2 |
| W8 | Review, Influence & Portfolio Audit | **all 1A–2E incl 2E** | audit |
Union across suite = **all 9 parts 1A–1D, 2A–2E present** (G1 currently satisfied). Public-showing = 3 **guardrail** mentions (all "Gold requirement, not required at Silver") → 0 assertions (G3 ✓). No hours/TQT (G3 ✓).

**The suite compresses Unit 1 into W1–W4 and runs Unit 2 leadership in W5–W8 of Autumn** — i.e. it front-loads the whole award into Autumn, where the SoW spreads it across the year.

## THE TENSION you must rule (G1 ↔ SoW ↔ Silver)
A *pure* SoW re-sequence = Autumn is **Unit 1 only** (1A–1D across the 8 weeks), Unit 2 (2A–2E) moves to Spring/Summer. **But no Spring or Summer Art suite exists in this repo.** Remove Unit 2 from Autumn with nowhere to land and **G1 fails** — 2A–2E lose their tagged home. Per G2 this must be answered, not silently dropped; per your conflict clause, **Silver wins**. Hence two options:

### ► Option A — Re-theme Unit 1, keep Unit 2 as the Autumn back-half (RECOMMENDED, gate-safe now)
Keep the single 8-week Silver vehicle. Changes:
- **W1** re-themed from "**Frame the Local Challenge**" (leadership framing on a Unit-1 part — violates G2 "Unit 1 challenge stays art-form") → **"Identity & Developing as an Artist"** (SoW Aut1; art-form challenge, 1A). 
- **W1–W4** (Unit 1) re-framed to the SoW Autumn arc — Aut1 *developing as an artist* (W1 1A, W3 1B) + Aut2 *experiencing & reviewing* (W4 1C, W2 1D research) — and **SoW vocab injected** (N4): art form, technique, portfolio, identity, reflection / audience, critique, inspiration, influence.
- **W5–W8** (Unit 2 leadership) **retained unchanged in structure** — they are the correct home for 2A–2E and there is no Spring/Summer suite to receive them. Framing checked so it doesn't contradict the SoW.
- **Half-term labels corrected**: W1–W3 → Aut1; W4 → Aut2 (experiencing/reviewing); W5–W8 → tagged "Unit 2 (SoW Spring/Summer) — taught early in this Silver vehicle" rather than the current blanket "Aut 1".
- **G1 after:** all 9 parts keep a home (Unit 1 in W1–W4, Unit 2 in W5–W8, W8 audit) → PASS.
- **Cost / accepted divergence (Silver-wins):** Unit 2 sits in Autumn, not Spring/Summer as the SoW prefers. This is the honest conflict — **flagged for your acceptance**: keep Unit 2 in the Autumn vehicle until Spring/Summer Art suites are built.
- **Blast radius:** W1 (retheme, heaviest), W2–W4 (vocab/framing, light), W5–W8 (framing check + label only), + 4 surfaces (START_HERE, Scheme_of_Work, Printable pack WEEKS[], in-folder SoW). ~8 lessons + 3 support files.

### ► Option B — Pure SoW sequence (bigger; NOT shippable this pass)
Autumn 8 wks = Unit 1 only; **build new Spring Spr1 + Summer Sum1/Sum2 Art suites** to carry Unit 2 (2A–2E). Cost: those suites don't exist — building them is a **coverage-gap project outside this pass's remit**; until they exist G1 fails. Defer unless you want to commission the new suites.

## What I would NOT change (survives either option — G3/G4)
- Public-showing guardrails (all 3, negating) — kept; count of *assertions* stays 0.
- Pass C survivors, relocated-not-deleted if a week moves: W1 pre-committed shrink-line (✓ present), W2 artist **AND arts-organisation** evidence (✓), W5 stranger-ready crew cards (✓), print-pack authorship-vs-support splits (✓). **W4 "staggered share"**: keyword `stagger` not matched — I will pinpoint the actual mechanism in W4 and preserve it before touching that file (open item, not a licence to drop it).
- No hours/TQT, no mark schemes/bands (G3/N11). Lundy boxes, reduced-motion, ll-g sentinel, slide counts — byte-preserved unless explicitly targeted (G6).

## Build sequence if you approve Option A
1. Class 1 — **SURFACE alignment**: reconcile START_HERE + Scheme_of_Work + Printable WEEKS[] to the corrected arc/labels (no lesson-content change).
2. Class 2 — **W1 retheme** (art-form identity challenge; SoW vocab).
3. Class 3 — **W2–W4 vocab/framing** to SoW Unit-1 arc.
4. Class 4 — **W5–W8 label + framing check** (structure preserved).
Each commit: one class, cardinality asserted null-delimited, print/screen parity with whole-file stale-string assertion, `node --check` + jsdom per touched file, `.lundy-box`/slide counts unchanged, reduced-motion byte-preserved, G1 nine-part re-derivation == all present, rollback base named.

**Awaiting: your pick (A / B / amend), and confirmation to keep Unit 2 in the Autumn vehicle under Option A.**
