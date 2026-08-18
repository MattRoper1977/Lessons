# PH-3 PHASE −1 — capability probe (2026-08-18)

| Probe | Result |
|---|---|
| `python3 --version` | Python 3.11.15 |
| `node --version` | v22.22.2 |
| `npm i jsdom` (isolated temp dir) | **SUCCEEDS** — jsdom installs and parses (`jsdom OK`) |
| `pip install pdfplumber` (temp venv) | **SUCCEEDS** — pdfplumber 0.11.10 imports |
| `_asdan_private/` at repo root | **ABSENT** → this pass runs in **FACTS MODE** on the §2 verified fact block; anything only a booklet can settle is marked UNDETERMINED |
| `.gitignore` covers `_asdan_private/` | Was **not** covered at BASE → added, single commit `PH-3: gitignore private ASDAN inputs` (first commit on the branch) |

## Operator gate lines present in this session

| Gate | Present? | Consequence |
|---|---|---|
| `P8: GO` | **NO** | A4 (C7 sentence) is NOT applied; recorded as OPEN_ITEMS item with the proposed text |
| `GO-MERGE` | **NO** | Branch pushed, PR opened, pass **HOLDS** for Matt's read + phone check |
| `GUIDE: keep/hide …` overrides | **NONE** | Job B hide-set is §5.2 as ruled |

## Repo/session facts

- Session attached repos: `MattRoper1977/Lessons` only at start. Job C's site repo will be attempted via `add_repo`; if not attachable, Job C is reported NOT RUN.
- `git remote -v` = `MattRoper1977/Lessons` ✓ · anchors `_passpq/ _close/OPEN_ITEMS.md REGISTER.md HANDOVER.md BUILD_ASDAN/ GROW_ASDAN/ LAUNCH_ASDAN/` all present ✓
- `origin/main` = `ae1d3c7af2526781aad6fb82e7cbbf6b87ded380` — **unchanged from PH-1/PH-2 BASE**.
- Quarantined `pass-ph1-peq-hardening` tip `ab7730c428c4f62cb4b67170ea22844e0cd39e78` — fetched read-only for the §4.5 recovery; never checked out; no workflow files will be added anywhere.
- The 10 baseline SHA-256 prefixes + byte sizes of §2.1 all match at BASE (10/10), including `GROW_ASDAN/Scheme_and_Resources.html` `42fcc0d46683` 10,333 B.
- Protected GROW strings verbatim ✓ (food-safety sentence ×1, C7 sentence ×1 at line 21); §5 Learner-confirmation 79/79 ✓; ASDAN html count 101 ✓.
- Environment: api.github.com/madebymatt.uk/Pages API proxy-blocked from Code — deployment verified via git truth + local checks only; Matt phone-checks. asdan.org.uk never fetched.
