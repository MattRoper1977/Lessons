# Lessons estate audit

This directory contains a **read-only, whole-repository verification pass** for the
`MattRoper1977/Lessons` GitHub Pages estate. It does not rewrite lessons, repair
content, alter assessment wording, or modify the website repository.

The audit has four evidence layers:

1. **Repository integrity and syntax** — inventories every tracked file; checks
   encodings, path collisions, missing symlinks, likely committed credentials,
   JSON/YAML/TOML/CSV/XML/SVG/Python/shell/JavaScript/CSS/HTML syntax, image and
   document containers, media probes, and the resource-catalog schema.
2. **Web-page execution** — serves the Lessons checkout below `/Lessons/` and a
   read-only checkout of `mattroper1977.github.io` at `/`, then opens every tracked
   HTML file in headless Chrome in desktop and mobile/reduced-motion modes. It
   records page errors, unhandled rejections, local HTTP failures, visible surface,
   overflow, accessible-control warnings and one safe generic interaction.
3. **Publication evidence** — validates `site.json` and its Lesson Hub wiring,
   checks the public URLs, and byte-compares the high-value live files with
   `origin/main`. The review branch is never mistaken for the published source.
4. **Review bundle** — emits human and machine-readable reports, a patch plan,
   inventory, issue CSV/JSON, browser/live results, checksums and a download
   manifest. The workflow adds the exact branch patch and changed-file manifest.

## Scope and failure policy

All tracked files are inventoried and format-checked. Every tracked HTML file is
opened in the browser pass. Files in historical/support areas such as underscore
folders, reports, tools, fixtures and test directories are still recorded, but a
browser defect there is a warning rather than an automatic publication blocker.
Public candidate pages and broken public local references are blocking.

A red workflow is therefore useful evidence, not a request to weaken the gate. Fix
false positives in the instrument first; fix proven defects in separate, explicit
commits; keep pupil-facing or assessed wording for Matt and Claude to review.

## Local run

Requirements: Python 3.11+, Node.js, Bash, Chrome/Chromium, Git and (for full media
coverage) `ffprobe`.

```bash
python3 -m pip install -r tools/estate-audit/requirements.txt

git fetch --no-tags origin main:refs/remotes/origin/main
git clone --depth 1 https://github.com/MattRoper1977/mattroper1977.github.io.git .audit-site

tools/estate-audit/run.sh
```

Useful environment switches:

```bash
AUDIT_BROWSER=0 tools/estate-audit/run.sh   # syntax/reference/live pass only
AUDIT_LIVE=0 tools/estate-audit/run.sh      # local static/browser pass only
AUDIT_OUTPUT=/absolute/path tools/estate-audit/run.sh
SITE_ROOT=/absolute/path/to/site-checkout tools/estate-audit/run.sh
```

The default evidence directory is `audit-output/`. Generated evidence is not
silently committed by this tool.

## Output contract

- `ESTATE_AUDIT_REPORT.md` — executive result and measured counts.
- `PATCH_PLAN.md` — findings grouped into reviewable defect families.
- `issues.csv` / `issues.json` — complete issue ledger.
- `inventory.csv` — every tracked file, size, hash and public/support class.
- `browser-results.json` — one record per page and browser mode.
- `live-results.json` — exact checks, live-path census and Pages API evidence.
- `site-checks.json` — `site.json`, Lesson Hub and related-site references.
- `metadata.json` — commits, counts, extensions and gate summaries.
- `download-manifest.json` / `checksums.sha256` — bundle integrity.
- `review.patch` / `changed-files.txt` — added by the Actions workflow.

## Test the instrument

```bash
python3 -m unittest discover -s tools/estate-audit/tests -v
python3 -m py_compile tools/estate-audit/estate_audit.py
```
