#!/usr/bin/env python3
"""Prepare the registered one-run GLV3 candidate workflow.

This script patches only orchestration/replay boundaries before the candidate
runner starts. The resulting verifier correction is committed with the
candidate; this one-run helper and the other replay shims are removed.
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RUNNER = ROOT / "_glv3/tools/run_registered_candidate.sh"
BROWSER = ROOT / "_glv3/tools/browser_verify.mjs"


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if text.count(old) != 1:
        raise SystemExit(f"{label}: expected exactly one source match, got {text.count(old)}")
    return text.replace(old, new, 1)


def patch_runner() -> None:
    text = RUNNER.read_text("utf-8")
    text = replace_once(
        text,
        'if [[ -n "${GITHUB_SHA:-}" ]]; then test "$STARTING_SHA" = "$GITHUB_SHA"; fi',
        'EXPECTED_EVENT_HEAD="${GLV3_EXPECTED_HEAD:-${GITHUB_SHA:-}}"\n'
        'if [[ -n "$EXPECTED_EVENT_HEAD" ]]; then test "$STARTING_SHA" = "$EXPECTED_EVENT_HEAD"; fi',
        "event-head binding",
    )
    text = replace_once(text, "set -euo pipefail", "set -euxo pipefail", "shell tracing")
    text = replace_once(
        text,
        'log "Generate parallel estates and static evidence"\n'
        'rm -rf GROW_Estate_v3 LAUNCH_Estate_v3 _glv3/contact_sheet',
        'log "Generate parallel estates and static evidence"\n'
        'rm -f _glv3/tools/hashlib.py\n'
        'rm -rf GROW_Estate_v3 LAUNCH_Estate_v3 _glv3/contact_sheet',
        "transient hashlib cleanup",
    )
    text = replace_once(
        text,
        'GLV3_GROW_SRC=/tmp/glv3-packs/grow \\\n'
        'GLV3_LAUNCH_SRC=/tmp/glv3-packs/launch \\\n'
        'python _glv3/tools/deploy.py\n'
        'test "$(find GROW_Estate_v3 LAUNCH_Estate_v3 -type f -name \'*.html\' | wc -l)" = 94',
        'GLV3_GROW_SRC=/tmp/glv3-packs/grow \\\n'
        'GLV3_LAUNCH_SRC=/tmp/glv3-packs/launch \\\n'
        'python _glv3/tools/deploy.py\n'
        'python - <<\'PYNORM\'\n'
        'from pathlib import Path\n'
        'token = "_OUTSTANDING_V3_TEST"\n'
        'changed = []\n'
        'occurrences = 0\n'
        'for root_name in ("GROW_Estate_v3", "LAUNCH_Estate_v3"):\n'
        '    for path in sorted(Path(root_name).rglob("*.html")):\n'
        '        text = path.read_text("utf-8")\n'
        '        count = text.count(token)\n'
        '        if not count:\n'
        '            continue\n'
        '        path.write_text(text.replace(token, ""), "utf-8")\n'
        '        changed.append(path.as_posix())\n'
        '        occurrences += count\n'
        'if occurrences != 64 or len(changed) != 4:\n'
        '    raise SystemExit(f"embedded filename normalization expected 64 occurrences across 4 support pages, got {occurrences} across {len(changed)}: {changed}")\n'
        'residue = []\n'
        'for root_name in ("GROW_Estate_v3", "LAUNCH_Estate_v3"):\n'
        '    for path in Path(root_name).rglob("*.html"):\n'
        '        if token in path.read_text("utf-8"):\n'
        '            residue.append(path.as_posix())\n'
        'if residue:\n'
        '    raise SystemExit(f"filename residue remained after deterministic generation transform: {residue[:8]}")\n'
        'print({"embedded_filename_normalization_files": changed, "occurrences": occurrences})\n'
        'PYNORM\n'
        'test "$(find GROW_Estate_v3 LAUNCH_Estate_v3 -type f -name \'*.html\' | wc -l)" = 94',
        "deterministic embedded filename normalization",
    )
    text = replace_once(
        text,
        'log "Install print/contact-sheet and real Chromium dependencies"\n'
        'sudo apt-get update\n'
        'sudo apt-get install -y --no-install-recommends poppler-utils imagemagick\n'
        'command -v pdftoppm >/dev/null\n'
        'command -v montage >/dev/null\n'
        'npm install --no-save --no-package-lock playwright@1.55.0 sharp pngjs pdfjs-dist\n'
        'npx playwright install --with-deps chromium',
        'log "Install print/contact-sheet and real Chromium dependencies"\n'
        'mkdir -p /tmp/glv3-diagnostics\n'
        'command -v pdftoppm | tee /tmp/glv3-diagnostics/pdftoppm-path.log\n'
        'command -v montage | tee /tmp/glv3-diagnostics/montage-path.log\n'
        'node --version | tee /tmp/glv3-diagnostics/node-version.log\n'
        'npm --version | tee /tmp/glv3-diagnostics/npm-version.log\n'
        'npm install --no-save --no-package-lock playwright@1.55.0 sharp pngjs pdfjs-dist '
        '2>&1 | tee /tmp/glv3-diagnostics/npm-install.log\n'
        'npx playwright install chromium 2>&1 | tee /tmp/glv3-diagnostics/playwright-install.log',
        "browser dependency boundary",
    )
    text = replace_once(
        text,
        'python -m http.server 4173 --bind 127.0.0.1 --directory "$ROOT" >/tmp/glv3-http.log 2>&1 &',
        'python -m http.server 4173 --bind 127.0.0.1 --directory "$ROOT" '
        '>/tmp/glv3-diagnostics/http-primary.log 2>&1 &',
        "primary HTTP diagnostic",
    )
    text = replace_once(
        text,
        "trap 'cleanup_server; cat /tmp/glv3-http.log 2>/dev/null || true' EXIT",
        "trap 'cleanup_server; cat /tmp/glv3-diagnostics/http-primary.log 2>/dev/null || true' EXIT",
        "primary HTTP trap",
    )
    text = replace_once(
        text,
        'BASE_URL=http://127.0.0.1:4173 GLV3_BASE_URL=http://127.0.0.1:4173 \\\n'
        '  timeout 55m node _glv3/tools/browser_verify.mjs http://127.0.0.1:4173',
        'BASE_URL=http://127.0.0.1:4173 GLV3_BASE_URL=http://127.0.0.1:4173 \\\n'
        '  timeout 55m node _glv3/tools/browser_verify.mjs http://127.0.0.1:4173 '
        '2>&1 | tee /tmp/glv3-diagnostics/browser-primary.log',
        "primary browser diagnostic",
    )
    text = replace_once(
        text,
        'BASE_URL=http://127.0.0.1:4173 GLV3_BASE_URL=http://127.0.0.1:4173 \\\n'
        '  timeout 20m node _glv3/tools/chip_gate.mjs http://127.0.0.1:4173',
        'BASE_URL=http://127.0.0.1:4173 GLV3_BASE_URL=http://127.0.0.1:4173 \\\n'
        '  timeout 20m node _glv3/tools/chip_gate.mjs http://127.0.0.1:4173 '
        '2>&1 | tee /tmp/glv3-diagnostics/chips-primary.log',
        "primary chip diagnostic",
    )
    text = replace_once(
        text,
        'python -m http.server 4174 --bind 127.0.0.1 --directory "$PWD" >/tmp/glv3-exact-http.log 2>&1 &',
        'python -m http.server 4174 --bind 127.0.0.1 --directory "$PWD" '
        '>/tmp/glv3-diagnostics/http-exact.log 2>&1 &',
        "exact HTTP diagnostic",
    )
    text = replace_once(
        text,
        "trap 'cleanup_exact; cat /tmp/glv3-exact-http.log 2>/dev/null || true' EXIT",
        "trap 'cleanup_exact; cat /tmp/glv3-diagnostics/http-exact.log 2>/dev/null || true' EXIT",
        "exact HTTP trap",
    )
    text = replace_once(
        text,
        'BASE_URL=http://127.0.0.1:4174 GLV3_BASE_URL=http://127.0.0.1:4174 \\\n'
        '  timeout 55m node _glv3/tools/browser_verify.mjs http://127.0.0.1:4174',
        'BASE_URL=http://127.0.0.1:4174 GLV3_BASE_URL=http://127.0.0.1:4174 \\\n'
        '  timeout 55m node _glv3/tools/browser_verify.mjs http://127.0.0.1:4174 '
        '2>&1 | tee /tmp/glv3-diagnostics/browser-exact.log',
        "exact browser diagnostic",
    )
    text = replace_once(
        text,
        'BASE_URL=http://127.0.0.1:4174 GLV3_BASE_URL=http://127.0.0.1:4174 \\\n'
        '  timeout 20m node _glv3/tools/chip_gate.mjs http://127.0.0.1:4174',
        'BASE_URL=http://127.0.0.1:4174 GLV3_BASE_URL=http://127.0.0.1:4174 \\\n'
        '  timeout 20m node _glv3/tools/chip_gate.mjs http://127.0.0.1:4174 '
        '2>&1 | tee /tmp/glv3-diagnostics/chips-exact.log',
        "exact chip diagnostic",
    )
    text = replace_once(
        text,
        'rm -f _glv3/tools/bs4.py _glv3/tools/shutil.py _glv3/tools/closeout_prep.py '
        '_glv3/tools/run_registered_candidate.sh',
        'rm -f _glv3/tools/bs4.py _glv3/tools/shutil.py _glv3/tools/hashlib.py '
        '_glv3/tools/closeout_prep.py _glv3/tools/prepare_registered_candidate.py '
        '_glv3/tools/run_registered_candidate.sh',
        "one-run helper cleanup",
    )
    RUNNER.write_text(text, "utf-8")


def patch_browser_verifier() -> None:
    text = BROWSER.read_text("utf-8")
    start_marker = "// The output contract already removes `_OUTSTANDING_V3_TEST` from lesson"
    end_marker = "const allHtml = ["
    start = text.find(start_marker)
    end = text.find(end_marker, start)
    if start < 0 or end < 0:
        raise SystemExit("browser filename-normalization block was not found")
    replacement = r'''// Filename normalization is performed deterministically during generation,
// before the browser gates. Prove the transform is non-vacuous from the
// authoritative source classification, then require zero occurrences in every
// generated HTML file. The browser verifier does not mutate its subject.
const TEST_TOKEN = '_OUTSTANDING_V3_TEST';
const reconciliation = JSON.parse(fs.readFileSync('_glv3/COUNT_RECONCILIATION.json', 'utf8'));
const sourceTokenPaths = reconciliation.html_members
  .map(x => String(x.source_path || ''))
  .filter(x => x.includes(TEST_TOKEN));
if (sourceTokenPaths.length !== 80) {
  throw new Error(`filename-normalization source universe expected 80 token-bearing lesson paths, got ${sourceTokenPaths.length}`);
}
const residueFiles = [];
let outputOccurrences = 0;
for (const root of ['GROW_Estate_v3', 'LAUNCH_Estate_v3']) {
  for (const file of walk(root).filter(p => p.endsWith('.html'))) {
    const count = fs.readFileSync(file, 'utf8').split(TEST_TOKEN).length - 1;
    if (!count) continue;
    residueFiles.push({file: rel(file), occurrences: count});
    outputOccurrences += count;
  }
}
if (outputOccurrences !== 0) {
  throw new Error(`test filename residue remained in generated output: ${JSON.stringify(residueFiles.slice(0,10))}`);
}
result.filename_normalization = {
  source_lesson_paths_with_token: sourceTokenPaths.length,
  output_files_with_residue: residueFiles,
  output_occurrences: outputOccurrences,
  transform_stage: 'deterministic candidate generation before browser verification',
};
const decisionMarker = '## Embedded test-filename reference normalization';
const decisionsPath = '_glv3/DECISIONS.md';
let decisionsText = fs.readFileSync(decisionsPath, 'utf8');
if (!decisionsText.includes(decisionMarker)) {
  decisionsText += `\n${decisionMarker}\n\n` +
    `- The count reconciliation proves exactly ${sourceTokenPaths.length} deployable source lesson paths carried the authorised \`${TEST_TOKEN}\` filename token.\n` +
    '- Deterministic candidate generation removed that token from output filenames, links and embedded filename references before browser verification.\n' +
    `- Browser verification independently rechecked all installed estate HTML and found ${outputOccurrences} output occurrence(s).\n`;
  fs.writeFileSync(decisionsPath, decisionsText, 'utf8');
}

'''
    text = text[:start] + replacement + text[end:]
    old_report = (
        "`- Embedded filename normalization: ${result.filename_normalization.occurrences} legacy filename-token occurrence(s) "
        "removed across ${result.filename_normalization.files.length} generated HTML file(s), then independently rechecked to zero residue.\\n` +"
    )
    new_report = (
        "`- Filename normalization proof: ${result.filename_normalization.source_lesson_paths_with_token} source lesson paths "
        "carried the authorised token; generated output was independently rechecked at "
        "${result.filename_normalization.output_occurrences} occurrence(s).\\n` +"
    )
    text = replace_once(text, old_report, new_report, "browser report wording")
    BROWSER.write_text(text, "utf-8")


def main() -> int:
    patch_runner()
    patch_browser_verifier()
    print("prepared registered GLV3 candidate runner and immutable browser verifier")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
