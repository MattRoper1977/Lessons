from __future__ import annotations

from pathlib import Path
import hashlib
import importlib.util
import json
import os
import re
import shutil
import subprocess
import tempfile

BASE = 'ae1d3c7af2526781aad6fb82e7cbbf6b87ded380'
OUT = Path('/tmp/ph1-gate-proofs')
OUT.mkdir(parents=True, exist_ok=True)
ROOT = Path.cwd()
NODE_PATH = os.environ.get('NODE_PATH', '')
JSDOM_VERSION = os.environ.get('JSDOM_VERSION', 'UNRESOLVED')


def run(cmd: list[str], cwd: Path | None = None, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        cwd=str(cwd or ROOT),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=check,
        env={**os.environ, 'NODE_PATH': NODE_PATH},
    )


# ---------------------------------------------------------------------------
# Proven jsdom harness
# ---------------------------------------------------------------------------
harness = r'''#!/usr/bin/env node
'use strict';
const fs = require('fs');
const path = require('path');
const { pathToFileURL } = require('url');
const { JSDOM, VirtualConsole, ResourceLoader } = require('jsdom');

function serialise(value) {
  if (value instanceof Error) return `${value.name}: ${value.message}`;
  if (typeof value === 'string') return value;
  try { return JSON.stringify(value); } catch (_) { return String(value); }
}

class LocalOnlyLoader extends ResourceLoader {
  constructor(errors) { super(); this.errors = errors; }
  fetch(url, options) {
    if (/^https?:\/\//i.test(url)) {
      this.errors.push(`NETWORK_DEPENDENCY: ${url}`);
      return null;
    }
    try {
      const result = super.fetch(url, options);
      if (result && typeof result.catch === 'function') {
        return result.catch(err => {
          this.errors.push(`RESOURCE_ERROR ${url}: ${serialise(err)}`);
          return null;
        });
      }
      return result;
    } catch (err) {
      this.errors.push(`RESOURCE_ERROR ${url}: ${serialise(err)}`);
      return null;
    }
  }
}

async function loadOne(file) {
  const absolute = path.resolve(file);
  const errors = [];
  const virtualConsole = new VirtualConsole();
  virtualConsole.on('jsdomError', err => errors.push(`JSDOM_ERROR: ${serialise(err)}`));
  virtualConsole.on('error', (...args) => errors.push(`CONSOLE_ERROR: ${args.map(serialise).join(' ')}`));
  const html = fs.readFileSync(absolute, 'utf8');
  let dom;
  try {
    dom = new JSDOM(html, {
      url: pathToFileURL(absolute).href,
      runScripts: 'dangerously',
      resources: new LocalOnlyLoader(errors),
      pretendToBeVisual: true,
      virtualConsole,
      beforeParse(window) {
        window.alert = () => {};
        window.confirm = () => true;
        window.prompt = () => null;
        window.print = () => {};
        window.scrollTo = () => {};
        window.matchMedia = window.matchMedia || (() => ({
          matches: false,
          media: '',
          onchange: null,
          addListener() {}, removeListener() {}, addEventListener() {}, removeEventListener() {}, dispatchEvent() { return false; }
        }));
        window.requestAnimationFrame = window.requestAnimationFrame || (cb => setTimeout(() => cb(Date.now()), 16));
        window.cancelAnimationFrame = window.cancelAnimationFrame || (id => clearTimeout(id));
        if (window.HTMLCanvasElement) {
          window.HTMLCanvasElement.prototype.getContext = function() { return null; };
        }
      }
    });
  } catch (err) {
    errors.push(`HARNESS_CONSTRUCTION: ${serialise(err)}`);
    return { file, rendered: false, readyState: null, marker: null, errors };
  }

  const window = dom.window;
  await new Promise(resolve => {
    let settled = false;
    const finish = () => { if (!settled) { settled = true; resolve(); } };
    if (window.document.readyState === 'complete') setTimeout(finish, 50);
    else window.addEventListener('load', () => setTimeout(finish, 120), { once: true });
    setTimeout(() => {
      if (!settled) errors.push('HARNESS_TIMEOUT: load did not settle within 4000ms');
      finish();
    }, 4000);
  });
  await new Promise(resolve => setTimeout(resolve, 100));
  const document = window.document;
  const rendered = Boolean(document && document.body && document.body.childNodes.length > 0);
  const marker = document && document.documentElement ? document.documentElement.getAttribute('data-ph1-control') : null;
  const readyState = document ? document.readyState : null;
  try { window.close(); } catch (_) {}
  return { file, rendered, readyState, marker, errors };
}

(async () => {
  const files = process.argv.slice(2);
  if (!files.length) {
    console.error('usage: node G2_HARNESS.cjs <html> [...]');
    process.exit(64);
  }
  const results = [];
  for (const file of files) results.push(await loadOne(file));
  process.stdout.write(JSON.stringify(results, null, 2) + '\n');
  process.exit(results.some(result => !result.rendered || result.errors.length) ? 1 : 0);
})().catch(err => {
  console.error(err && err.stack ? err.stack : String(err));
  process.exit(70);
});
'''
(OUT / 'G2_HARNESS.cjs').write_text(harness, encoding='utf-8')

fixtures = Path(tempfile.mkdtemp(prefix='ph1-g2-controls-'))
broken = fixtures / 'broken.html'
clean = fixtures / 'clean.html'
broken.write_text(
    '<!doctype html><html><body><main>broken control</main><script>throw new Error("PH1_CONTROL_THROW")</script></body></html>\n',
    encoding='utf-8',
)
clean.write_text(
    '<!doctype html><html><body><main id="ok">clean control</main><script>document.documentElement.setAttribute("data-ph1-control","clean-ran")</script></body></html>\n',
    encoding='utf-8',
)

broken_run = run(['node', str(OUT / 'G2_HARNESS.cjs'), str(broken)], check=False)
clean_run = run(['node', str(OUT / 'G2_HARNESS.cjs'), str(clean)], check=False)
try:
    broken_json = json.loads(broken_run.stdout)
except Exception:
    broken_json = []
try:
    clean_json = json.loads(clean_run.stdout)
except Exception:
    clean_json = []

broken_detected = (
    broken_run.returncode != 0
    and len(broken_json) == 1
    and any('PH1_CONTROL_THROW' in item for item in broken_json[0].get('errors', []))
)
clean_detected = (
    clean_run.returncode == 0
    and len(clean_json) == 1
    and clean_json[0].get('rendered') is True
    and clean_json[0].get('marker') == 'clean-ran'
    and clean_json[0].get('errors') == []
)

g2_report = [
    '# PH-1 replacement G2 — jsdom harness proof',
    '',
    f'- jsdom requested: `26.1.0`.',
    f'- jsdom resolved: `{JSDOM_VERSION}`.',
    f'- Node: `{run(["node", "--version"]).stdout.strip()}`.',
    '- Environment: GitHub Actions runner with network available for the pinned package install.',
    '',
    '## Broken control',
    '',
    f'- Fixture: inline `throw new Error("PH1_CONTROL_THROW")`.',
    f'- Harness exit: **{broken_run.returncode}**.',
    f'- Genuine runtime throw detected: **{broken_detected}**.',
    '',
    '```json',
    json.dumps(broken_json, indent=2),
    '```',
    '',
    '## Clean control',
    '',
    '- Fixture: clean body plus an inline script setting `data-ph1-control="clean-ran"`.',
    f'- Harness exit: **{clean_run.returncode}**.',
    f'- Rendered, marker observed and zero errors: **{clean_detected}**.',
    '',
    '```json',
    json.dumps(clean_json, indent=2),
    '```',
    '',
]
if broken_detected and clean_detected and JSDOM_VERSION == '26.1.0':
    g2_report.extend([
        '**CONTROL VERDICT: PROVEN.** The harness rejects a genuine runtime throw and accepts the known-clean page.',
        '',
        'This proves the detector only. Real G2 remains pending until it is run across the touched production files after P1–P7.',
        '',
    ])
else:
    g2_report.extend([
        '**CONTROL VERDICT: UNPROVEN.** Real G2 must remain red and no edit phase may begin.',
        '',
    ])
(OUT / 'G2_HARNESS_PROOF.md').write_text('\n'.join(g2_report), encoding='utf-8')


# ---------------------------------------------------------------------------
# Proven BASE-versus-tip witness comparator
# ---------------------------------------------------------------------------
comparator = r'''from __future__ import annotations

from pathlib import Path
import hashlib
import html
import re
import subprocess

WITNESS_RE = re.compile(r'(?i)id=["\']print-witness["\']|Assessor Witness Statement')


def extract_element_by_id(text: str, target_id: str = 'print-witness') -> str:
    opening = re.search(
        rf'(?is)<(?P<tag>[a-z][a-z0-9]*)\b[^>]*\bid=["\']{re.escape(target_id)}["\'][^>]*>',
        text,
    )
    if not opening:
        anchor = text.lower().find('assessor witness statement')
        if anchor < 0:
            return ''
        next_print = text.lower().find('class="print-section', anchor + 30)
        end = next_print if next_print > anchor else min(len(text), anchor + 18000)
        return text[max(0, text.rfind('<div', 0, anchor)):end]
    tag = opening.group('tag')
    depth = 1
    token_re = re.compile(rf'(?is)</?{re.escape(tag)}\b[^>]*>')
    for token in token_re.finditer(text, opening.end()):
        raw = token.group(0)
        if raw.startswith('</'):
            depth -= 1
            if depth == 0:
                return text[opening.start():token.end()]
        elif not raw.rstrip().endswith('/>'):
            depth += 1
    return text[opening.start():min(len(text), opening.start() + 22000)]


def canonical(block: str) -> str:
    value = html.unescape(block).replace('\r\n', '\n').replace('\r', '\n')
    value = re.sub(r'\s+', ' ', value).strip()
    value = re.sub(r'>\s+<', '><', value)
    return value


def fingerprint_text(text: str) -> str | None:
    block = extract_element_by_id(text)
    if not block:
        return None
    return hashlib.sha256(canonical(block).encode('utf-8')).hexdigest()


def fingerprint_file(path: Path) -> str | None:
    return fingerprint_text(path.read_text(encoding='utf-8', errors='replace'))


def tracked_html(root: Path) -> list[Path]:
    output = subprocess.check_output(['git', '-C', str(root), 'ls-files', '*.html'], text=True)
    return [root / line for line in output.splitlines() if line]


def snapshot(root: Path) -> dict[str, str]:
    result = {}
    for path in tracked_html(root):
        text = path.read_text(encoding='utf-8', errors='replace')
        if not WITNESS_RE.search(text):
            continue
        fingerprint = fingerprint_text(text)
        if fingerprint is not None:
            result[str(path.relative_to(root))] = fingerprint
    return result


def compare(base: dict[str, str], tip: dict[str, str]) -> dict:
    base_set = set(base)
    tip_set = set(tip)
    changed = sorted(path for path in base_set & tip_set if base[path] != tip[path])
    return {
        'pass': base_set == tip_set and not changed,
        'base_count': len(base_set),
        'tip_count': len(tip_set),
        'missing_at_tip': sorted(base_set - tip_set),
        'added_at_tip': sorted(tip_set - base_set),
        'changed': changed,
    }
'''
(OUT / 'G4_WITNESS_COMPARATOR.py').write_text(comparator, encoding='utf-8')

spec = importlib.util.spec_from_file_location('g4cmp', OUT / 'G4_WITNESS_COMPARATOR.py')
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

base_snapshot = module.snapshot(ROOT)
mutation_root = Path(tempfile.mkdtemp(prefix='ph1-g4-mutations-'))
samples = [
    'BUILD_ASDAN/Careers/CAREERS_W1_My_Strengths.html',
    'LAUNCH_ASDAN/PEQ/PEQ_W5_Deliver_the_Activity_and_Gather_Evidence.html',
    'Build/Slideshows/BUILD_DT_W1_Workshop_Audit.html',
]
for relative in samples:
    destination = mutation_root / relative
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(ROOT / relative, destination)

baseline_three = {path: module.fingerprint_file(ROOT / path) for path in samples}

# 1. Delete the witness section entirely.
delete_path = samples[0]
delete_text = (mutation_root / delete_path).read_text(encoding='utf-8', errors='replace')
delete_block = module.extract_element_by_id(delete_text)
(mutation_root / delete_path).write_text(delete_text.replace(delete_block, '', 1), encoding='utf-8')
delete_tip = module.fingerprint_file(mutation_root / delete_path)
delete_red = baseline_three[delete_path] is not None and delete_tip is None

# 2. Alter witness content.
alter_path = samples[1]
alter_text = (mutation_root / alter_path).read_text(encoding='utf-8', errors='replace')
alter_block = module.extract_element_by_id(alter_text)
mutated_block = alter_block.replace('Assessor Witness Statement', 'Assessor Witness Statement MUTATED', 1)
(mutation_root / alter_path).write_text(alter_text.replace(alter_block, mutated_block, 1), encoding='utf-8')
alter_tip = module.fingerprint_file(mutation_root / alter_path)
alter_red = baseline_three[alter_path] != alter_tip

# 3. Reformat whitespace only.
space_path = samples[2]
space_text = (mutation_root / space_path).read_text(encoding='utf-8', errors='replace')
space_block = module.extract_element_by_id(space_text)
space_mutated = re.sub(r'>\s*<', '>\n        <', space_block)
(mutation_root / space_path).write_text(space_text.replace(space_block, space_mutated, 1), encoding='utf-8')
space_tip = module.fingerprint_file(mutation_root / space_path)
space_green = baseline_three[space_path] == space_tip

mutation_proven = delete_red and alter_red and space_green

g4_report = [
    '# PH-1 replacement G4 — witness comparator mutation proof',
    '',
    f'- Immutable BASE: `{BASE}`.',
    f'- Witness surfaces derived at BASE: **{len(base_snapshot)}**.',
    '- Comparator: extract each surface’s own witness block, canonicalise whitespace, SHA-256 the canonical block, then compare BASE and tip sets and fingerprints.',
    '',
    '## Mandatory mutations',
    '',
    f'1. **Delete a witness section entirely** — `{delete_path}`',
    f'   - Baseline fingerprint: `{baseline_three[delete_path]}`',
    f'   - Mutated fingerprint: `{delete_tip}`',
    f'   - Comparator went red: **{delete_red}**.',
    '',
    f'2. **Alter witness content** — `{alter_path}`',
    f'   - Baseline fingerprint: `{baseline_three[alter_path]}`',
    f'   - Mutated fingerprint: `{alter_tip}`',
    f'   - Comparator went red: **{alter_red}**.',
    '',
    f'3. **Whitespace-only reformat** — `{space_path}`',
    f'   - Baseline fingerprint: `{baseline_three[space_path]}`',
    f'   - Mutated fingerprint: `{space_tip}`',
    f'   - Comparator stayed green: **{space_green}**.',
    '',
]
if mutation_proven:
    g4_report.extend([
        '**MUTATION VERDICT: PROVEN.** All three required detector behaviours were observed.',
        '',
        'Real G4 remains pending until BASE is compared with the final branch tip after P1–P7.',
        '',
    ])
else:
    g4_report.extend([
        '**MUTATION VERDICT: UNPROVEN.** G4 stays red and no edit phase may begin.',
        '',
    ])
(OUT / 'G4_MUTATION_PROOF.md').write_text('\n'.join(g4_report), encoding='utf-8')

proof_data = {
    'jsdom_requested': '26.1.0',
    'jsdom_resolved': JSDOM_VERSION,
    'broken_control': broken_detected,
    'clean_control': clean_detected,
    'g2_proven': broken_detected and clean_detected and JSDOM_VERSION == '26.1.0',
    'g4_base_surface_count': len(base_snapshot),
    'g4_delete_red': delete_red,
    'g4_alter_red': alter_red,
    'g4_whitespace_green': space_green,
    'g4_proven': mutation_proven,
}
(OUT / 'gate-proof-data.json').write_text(json.dumps(proof_data, indent=2), encoding='utf-8')
print(json.dumps(proof_data, indent=2))

if not proof_data['g2_proven'] or not proof_data['g4_proven']:
    raise SystemExit(40)
