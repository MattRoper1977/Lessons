# SCA-1 CLOSE v2 §1 — hinge answer-key shuffle (P1, owner-ruled APPLY)

BASE `d6280de`. Universe: the 35 science `v3_40min` decks — one hinge question each
(`_sca1close/tables/hinges.json`).

## The defect, measured

All 35 hinge questions authored the correct option **first**. Measured on the real
files in headless Chromium before any edit: pressing the first button scored
**35/35 (100%)**; the correct option's rendered position histogram was `{0: 35}`.
A pupil with no science knowledge scored every hinge in the suite.

## What changed

One additive `<script id="sci-hinge-shuffle">` block per deck (34 lines, byte-identical
across all 35; **1190 insertions, 0 deletions**). At render it Fisher–Yates shuffles the
option **buttons** of every `.soft` / `.soft-check` wrapper, screen only.

- **RNG**: `crypto.getRandomValues` with rejection sampling (no modulo bias), falling
  back to `Math.random` where crypto is absent.
- **Timing**: runs at render — immediately if the DOM is parsed, else on
  `DOMContentLoaded`.
- **Exemption mechanism**: a wrapper carrying `data-shuffle="off"` is skipped.

## Scoring is by identity, never index — and was already

`answer()` compares the button's authored `data-i` against the wrapper's `data-c`;
`softAnswer()` compares `data-index` against `data-correct`. Those attributes travel
with the node, so DOM order cannot enter the verdict. Verified estate-wide that nothing
reads options positionally: `.option)[` → 0, `children[N]` → 0;
`querySelectorAll('.option')` is used only to clear classes. (`.microfilm[data-i]` is a
film cursor on a different element and is not touched.)

## Exemptions: 0 of 35 — with the instrument calibrated first

`_sca1close/tools/exemptions.js calibrate` proves the detector on **10 controls, all
pass**: it fires on "all of the above", "none of these", "both of the above",
"options 1 and 2" and a monotonic single-unit numeric ladder; it does **not** fire on
domain-language "both" ("Both muscles push" — the two muscles in the *stem*, not the
option list), on unordered value sets (`0.05 mm | 8000 mm | 20.4 mm`), on mixed units
(`×200 | ×4.5 | 200 mm`), or on plain prose.

Run over the suite: **0 exempt**. The only two phrase candidates —
`SCI_B_W4A` "Both muscles push" and `SCI_L_W7L2` "Both processes with
similarities/differences" — are domain language and shuffle safely. No question in the
suite depends on option order. **Exemption list: empty**; the mechanism ships unused.

## Print and read-aloud

- **Print**: hinge option strings are not duplicated into any print section (checked per
  deck: every occurrence is in the slide, none in a `print-pack/page/section` region),
  and there are **no A)/B)/C)/D) position letters** anywhere. Authored order is what
  reaches paper and screen order is not observable in print. Proven by rendering
  `media=print` for all 35 before and after: **body text byte-identical ×35**.
  Print-set-parity predicate: *the printed option set for a hinge is empty, so set
  equality holds trivially and order is excluded by construction.*
- **Read-aloud**: no hinge sits inside a `[data-speak-host]` (0 of 35), so no authored
  `data-speak-text` enumerates options. Where the speak fallback applies it reads
  `host.textContent` — i.e. live **rendered** order.

## Controls (on the merged bytes)

| control | before | after | verdict |
|---|---|---|---|
| press first button | **35/35 = 100%** | **31/105 = 29.5%** (chance 33.3%) | PASS |
| correct-option position, >100 loads | `{0:35}` all pos0 | `{0:34, 1:32, 2:39}` = 32.4/30.5/37.1% | PASS (uniform) |
| identity-keyed scoring after shuffle | — | **35/35 correct** | PASS |
| index-keyed variant (score by DOM position) | — | **misscores 71/105** | RED, as required |
| tier panels | 0 hinges sit inside a tier panel; all 35 are top-level in the We Do slide, so all shuffle | | PASS |

## Regression gates on the 35 touched decks

`node --check` 105 blocks OK · boot ×3 viewports clean · sentinels **50/123**
set-identical · ECA-1 PROTECTED **IDENTICAL (736 rows)** · SCA-1 protected manifest +
food census **byte-identical** (`a551018ccb605d6a` / `c06e3c3e0ee630d9`) before and
after · PART B still holds on these tagged decks: default-hidden + G-toggle +
persistence re-asserted ×35, print identical ×35, PART B strip→re-patch round-trips and
the combined strip returns **exactly HEAD bytes (0 diff)** · idempotent (second run
changes nothing ×35) · **CP1 additive: 0 deletions**.

### Note on the "468 protected strings" figure
`_sca1/MERGE.md` records 468 across 12 families. Today's `_sca1/tools/protected.py`
carries **19** families and reports **524** matched lines. An independent recount of the
same family set at `e907653` (SCA-1's merge) and at `d6280de` (this pass's base) gives
the **same number at both revisions** — so this is a counting-basis/family-set
difference recorded at different times, **not content drift**. The manifest sha is
unchanged by this pass.
