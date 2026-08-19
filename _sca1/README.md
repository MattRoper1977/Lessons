# SCA-1 — Science Correctness Audit + Fix · records

BASE_SHA / ROLLBACK_SHA: `72778591e8c1fe1d9c5b979c90ccbbd868de4b3a`
Branch: `claude/sca-1-science-correctness`

## Read these first
- `PROPOSED.md` — every judgement call, not applied. **Matt rules on these.** P1 is the one
  to read first.
- `ROLLBACK.txt` — rollback SHA and the 5/5 identity gate.
- `G4_NOTE.md` — why the protected-string instrument is what it is (two earlier designs
  produced false positives; both are documented).

## Tables (`tables/`)
| file | what it is |
|---|---|
| `inventory.csv` | 53 files: bytes, sha256, script count, print-pack marker families, witness/WORD HELP/closure counts |
| `questions_raw.csv` | 2 060 extracted question rows (screen + print, all tiers, all three print dialects) |
| `questions_master.csv` | the same rows with a verdict and a disposition |
| `answer_keys.csv` | all 35 encoded hinge answers with stem, options and correct index |
| `findings_raw.csv` | 106 raw findings from the 15 per-week audits (pre-verification) |
| `wrong_dispositions.csv` | each of the 37 WRONG claims → FIXED (commit) or recorded |
| `parity.csv` | screen↔print parity per lesson per tier (81 OK, 24 condensed, 0 answer divergences) |
| `sow_alignment.csv`, `keywords_sow.csv` | Track D: 15/15 ALIGNED, 0 keywords absent |
| `reading_band.csv` | FK per stem — **report-only**, no band supplied except BUILD ≈ 6–9 |
| `uk_spelling_raw.csv`, `consistency_raw.csv` | Track B raw hits |
| `cmd_offpitch.csv`, `leakage.csv`, `double_negative.csv` | Track C raw hits |

## Instruments (`tools/`)
Every one is re-runnable. `gates.py` prints the G1–G10 table.
Three instruments were rebuilt mid-pass after they produced false results; each carries a
note explaining what was wrong and how it was verified afterwards:
- `extract.py` — first version missed GROW entirely (attribute order, `route-card`,
  hyphenated print dialect) and collapsed three `index.html` files onto one basename.
- `protected2.py` + `G4_NOTE.md` — whole-line and ±140-char hashing both produced false
  G4 failures.
- `safe_edit.py` — the CODE-stream mask had to become constant-width so that a prose edit
  changing a read-aloud string's length is not reported as a CODE delta.

## Universes (state them with any count)
- PROSE stream: 50 HTML files, 947 529 chars. CODE stream: 2 191 913 chars (69.3 %, exempt).
- Sentinels derived over git-tracked `*.html` at BASE_SHA = 778 files.
- Protected strings: 468 across 12 families.

## AMBER
- **LAUNCH SoW came off an unmerged branch** `origin/pass-sl-sow-launch`
  @ `2a1cfdad9cdbc09eba538be3190b89f5e35cf6f9`. Recommend committing it to
  `_passsl/inputs/` on main. Copy kept at `inputs/LAUNCH_KS4.xlsx`.
- **Edexcel 1BI0 spec UNVERIFIED** — `qualifications.pearson.com` is blocked by this
  environment's egress proxy (both the spec page and the direct PDF). Per §6, LAUNCH
  alignment is therefore SoW-rows-only. Nothing in this pass depends on a spec-point code.
- **`/hud.js` 404** in headless boot is served from the SITE repo at origin root, not a
  Lessons gap. It accounts for all 105 boot errors (35 lessons × 3 viewports) at baseline
  and after. Not stubbed, by instruction.
