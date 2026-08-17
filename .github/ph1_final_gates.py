from __future__ import annotations

from pathlib import Path
from collections import Counter
import hashlib
import html
import importlib.util
import json
import os
import re
import subprocess
import tempfile

BASE = os.environ['PH1_BASE']
TARGET = os.environ['PH1_TARGET']
BASE_DIR = Path(os.environ['PH1_BASE_DIR'])
TIP_DIR = Path(os.environ['PH1_TIP_DIR'])
REPO = Path(os.environ['PH1_REPO'])
OUT = Path(os.environ.get('PH1_GATE_OUT', '/tmp/ph1-final-gates'))
OUT.mkdir(parents=True, exist_ok=True)
NODE_PATH = os.environ.get('NODE_PATH', '')
JSDOM_VERSION = os.environ.get('PH1_JSDOM_VERSION', 'UNRESOLVED')

P_COMMITS = {
    'P1': '4c8bfa413e3df3fa604daf4aafbab058c90f0cbf',
    'P2': 'e60f6500a22e93a2a4267e6bf20caf6f9c5f37a1',
    'P3': '4c573608525d1a06e9d5d67376904ee3118f49e2',
    'P4': '3f29c050fb5e8f42fc5d2aa1dbb7c02ce9bde2f5',
    'P5': '3e66061012cfc4ebc5c01b02a1f3975e05537c8c',
    'P6': 'ae8631882d7d3a02e1bf0c12032e610513c52650',
    'P7': '6e5b34981e667cc398bea364f35d5fd72e59104a',
}


def run(cmd: list[str], cwd: Path | None = None, check: bool = False, timeout: int | None = None, env: dict | None = None) -> subprocess.CompletedProcess[str]:
    merged = dict(os.environ)
    merged['NODE_PATH'] = NODE_PATH
    if env:
        merged.update(env)
    return subprocess.run(
        cmd,
        cwd=str(cwd or REPO),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=check,
        timeout=timeout,
        env=merged,
    )


def git(*args: str, cwd: Path | None = None) -> str:
    result = run(['git', *args], cwd=cwd, check=True)
    return result.stdout


def tracked(root: Path, patterns: list[str] | None = None) -> list[str]:
    args = ['ls-files']
    if patterns:
        args += ['--', *patterns]
    return [line for line in git(*args, cwd=root).splitlines() if line]


def production_path(value: str) -> bool:
    path = Path(value)
    if path.suffix.lower() != '.html':
        return False
    if any(part.endswith('_Estate_v3') for part in path.parts):
        return False
    if value.startswith(('BUILD_ASDAN/', 'GROW_ASDAN/', 'LAUNCH_ASDAN/')):
        return True
    if value in {'build_asdan.html', 'build_dt_upcycling.html'}:
        return True
    if value.startswith('DT_Community_Upcycling/'):
        return True
    if re.fullmatch(r'Build/Slideshows/BUILD_DT_W[1-6]_[^/]+\.html', value):
        return True
    return False


def read_at(root: Path, path: str) -> str:
    return (root / path).read_text(encoding='utf-8', errors='replace')


changed_paths = [line for line in git('diff', '--name-only', BASE, TARGET, '--').splitlines() if line]
touched_html = sorted(path for path in changed_paths if path.lower().endswith('.html'))
production_base = sorted(path for path in tracked(BASE_DIR, ['*.html']) if production_path(path))
production_tip = sorted(path for path in tracked(TIP_DIR, ['*.html']) if production_path(path))

# ---------------------------------------------------------------------------
# G1 — node --check every inline script block
# ---------------------------------------------------------------------------
SCRIPT_RE = re.compile(r'<script(?P<attrs>[^>]*)>(?P<body>.*?)</script>', re.I | re.S)


def extract_scripts(text: str) -> list[str]:
    output = []
    for match in SCRIPT_RE.finditer(text):
        if re.search(r'\bsrc\s*=', match.group('attrs'), re.I):
            continue
        body = match.group('body')
        if body.strip():
            output.append(body)
    return output


def node_check(root: Path) -> dict:
    errors = []
    total = 0
    per_file = {}
    for path in touched_html:
        blocks = extract_scripts(read_at(root, path))
        per_file[path] = len(blocks)
        total += len(blocks)
        for index, block in enumerate(blocks):
            with tempfile.NamedTemporaryFile('w', suffix='.js', encoding='utf-8', delete=False) as handle:
                handle.write(block)
                temp_path = handle.name
            result = run(['node', '--check', temp_path], cwd=root)
            Path(temp_path).unlink(missing_ok=True)
            if result.returncode != 0:
                errors.append({'file': path, 'block': index, 'stderr': result.stderr.strip()[-1200:]})
    return {'blocks': total, 'files': len(touched_html), 'per_file': per_file, 'errors': errors, 'pass': not errors}


g1_base = node_check(BASE_DIR)
g1_tip = node_check(TIP_DIR)
G1 = {'pass': g1_tip['pass'], 'base': g1_base, 'tip': g1_tip}

# ---------------------------------------------------------------------------
# G2 — proven jsdom harness, actual page loads
# ---------------------------------------------------------------------------
harness = TIP_DIR / '_passph1/G2_HARNESS.cjs'


def jsdom_load(root: Path) -> dict:
    args = ['node', str(harness), *[str(root / path) for path in touched_html]]
    try:
        result = run(args, cwd=root, timeout=max(180, len(touched_html) * 6))
    except subprocess.TimeoutExpired as exc:
        return {'pass': False, 'harness_failed': True, 'error': f'HARNESS_TIMEOUT: {exc}', 'results': []}
    try:
        payload = json.loads(result.stdout)
    except Exception as exc:
        return {
            'pass': False,
            'harness_failed': True,
            'error': f'HARNESS_OUTPUT: {type(exc).__name__}: {exc}',
            'returncode': result.returncode,
            'stdout': result.stdout[-3000:],
            'stderr': result.stderr[-3000:],
            'results': [],
        }
    if not isinstance(payload, list) or len(payload) != len(touched_html):
        return {
            'pass': False,
            'harness_failed': True,
            'error': f'HARNESS_COUNT: expected {len(touched_html)} results; got {len(payload) if isinstance(payload, list) else type(payload).__name__}',
            'returncode': result.returncode,
            'results': payload if isinstance(payload, list) else [],
        }
    failures = [item for item in payload if not item.get('rendered') or item.get('errors')]
    return {
        'pass': not failures and result.returncode == 0,
        'harness_failed': False,
        'returncode': result.returncode,
        'files': len(payload),
        'failures': failures,
        'results': payload,
    }


g2_base = jsdom_load(BASE_DIR)
g2_tip = jsdom_load(TIP_DIR)
G2 = {'pass': g2_tip['pass'] and not g2_tip.get('harness_failed'), 'base': g2_base, 'tip': g2_tip, 'jsdom_version': JSDOM_VERSION}

# ---------------------------------------------------------------------------
# G3 — print-section count unchanged per touched file
# ---------------------------------------------------------------------------
PRINT_RE = re.compile(r'class=["\'][^"\']*\bprint-section\b[^"\']*["\']', re.I)
base_print = {path: len(PRINT_RE.findall(read_at(BASE_DIR, path))) for path in touched_html}
tip_print = {path: len(PRINT_RE.findall(read_at(TIP_DIR, path))) for path in touched_html}
print_diffs = {path: [base_print[path], tip_print[path]] for path in touched_html if base_print[path] != tip_print[path]}
G3 = {
    'pass': not print_diffs,
    'base_total': sum(base_print.values()),
    'tip_total': sum(tip_print.values()),
    'base': base_print,
    'tip': tip_print,
    'diffs': print_diffs,
}

# ---------------------------------------------------------------------------
# G4 — mutation-proven witness comparator, BASE versus tip only
# ---------------------------------------------------------------------------
comparator_path = TIP_DIR / '_passph1/G4_WITNESS_COMPARATOR.py'
spec = importlib.util.spec_from_file_location('ph1_g4_comparator', comparator_path)
if not spec or not spec.loader:
    G4 = {'pass': False, 'harness_failed': True, 'error': 'Unable to import proven comparator'}
else:
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    g4_base = module.snapshot(BASE_DIR)
    g4_tip = module.snapshot(TIP_DIR)
    G4 = module.compare(g4_base, g4_tip)
    G4['mutation_proof'] = 'delete red; content red; whitespace green; hub false-positive excluded'

# ---------------------------------------------------------------------------
# G5 — derive the loop-mark sentinel set at BASE and tip
# ---------------------------------------------------------------------------
def loopmark_set(ref: str) -> list[str]:
    result = run(['git', 'grep', '-I', '-l', 'll-g:loop-mark', ref, '--', '*.html'], cwd=REPO)
    files = []
    for line in result.stdout.splitlines():
        value = line.split(':', 1)[1] if ':' in line else line
        if value.startswith('_passsci1/'):
            continue
        files.append(value)
    return sorted(set(files))


sentinel_base = loopmark_set(BASE)
sentinel_tip = loopmark_set(TARGET)
G5 = {
    'pass': sentinel_base == sentinel_tip,
    'base_count': len(sentinel_base),
    'tip_count': len(sentinel_tip),
    'added': sorted(set(sentinel_tip) - set(sentinel_base)),
    'removed': sorted(set(sentinel_base) - set(sentinel_tip)),
    'base_set': sentinel_base,
    'tip_set': sentinel_tip,
}

# ---------------------------------------------------------------------------
# G6 — production banned claims
# ---------------------------------------------------------------------------
def occurrence_contexts(text: str, pattern: re.Pattern[str], limit: int = 30) -> list[dict]:
    output = []
    for match in pattern.finditer(text):
        line = text.count('\n', 0, match.start()) + 1
        context = re.sub(r'\s+', ' ', html.unescape(text[max(0, match.start()-120):match.end()+180])).strip()
        output.append({'line': line, 'match': match.group(0), 'context': context[:420]})
        if len(output) >= limit:
            break
    return output


def affirmative_l2(text: str) -> list[dict]:
    patterns = [
        re.compile(r'(?i)\b(?:can\s+be\s+|may\s+be\s+)?registered\s+(?:at|for)\s+level\s*2\b'),
        re.compile(r'(?i)\bregister(?:ing)?\s+(?:[a-z]+\s+){0,5}(?:at|for)\s+level\s*2\b'),
        re.compile(r'(?i)\b(?:level\s*2|l2)\s+registration\b'),
    ]
    found = []
    seen = set()
    for pattern in patterns:
        for match in pattern.finditer(text):
            preceding = text[max(0, match.start()-55):match.start()].lower()
            if re.search(r'(?:\bno\b|\bnot\b|\bnever\b|\bwithout\b|does\s+not)\s*$', preceding):
                continue
            key = (match.start(), match.end())
            if key in seen:
                continue
            seen.add(key)
            line = text.count('\n', 0, match.start()) + 1
            context = re.sub(r'\s+', ' ', html.unescape(text[max(0, match.start()-170):match.end()+240])).strip()
            found.append({'line': line, 'match': match.group(0), 'context': context[:520]})
    return sorted(found, key=lambda item: item['line'])


TEN_COMM_RE = re.compile(
    r'(?is)(?:10[- ]?hour|600[- ]?minute|ten\s+hours).{0,220}(?:ComSk1|Communication)|(?:ComSk1|Communication).{0,220}(?:10[- ]?hour|600[- ]?minute|ten\s+hours)'
)
ADJ_NOT_BOTH_RE = re.compile(r'(?is)(?:adjacent|level\s+above|level\s+below|credits?).{0,180}\bnot\s+both\b|\bnot\s+both\b.{0,180}(?:adjacent|level\s+above|level\s+below|credits?)')


def banned_census(root: Path, paths: list[str]) -> dict:
    result = {
        'Delivering a Project': [],
        'ASDAN Studio · ASDAN Studio': [],
        'affirmative L2 registration': [],
        'Communication 10-hour/600-minute': [],
        'adjacent-level not both': [],
    }
    for path in paths:
        text = read_at(root, path)
        for label, needle in (
            ('Delivering a Project', 'Delivering a Project'),
            ('ASDAN Studio · ASDAN Studio', 'ASDAN Studio · ASDAN Studio'),
        ):
            for item in occurrence_contexts(text, re.compile(re.escape(needle), re.I)):
                result[label].append({'file': path, **item})
        for item in affirmative_l2(text):
            result['affirmative L2 registration'].append({'file': path, **item})
        for item in occurrence_contexts(text, TEN_COMM_RE):
            result['Communication 10-hour/600-minute'].append({'file': path, **item})
        for item in occurrence_contexts(text, ADJ_NOT_BOTH_RE):
            result['adjacent-level not both'].append({'file': path, **item})
    counts = {label: len(items) for label, items in result.items()}
    return {'counts': counts, 'occurrences': result, 'pass': all(value == 0 for value in counts.values())}


g6_base = banned_census(BASE_DIR, production_base)
g6_tip = banned_census(TIP_DIR, production_tip)
G6 = {'pass': g6_tip['pass'], 'base': g6_base, 'tip': g6_tip}

# ---------------------------------------------------------------------------
# G7 — prefers-reduced-motion blocks byte-identical
# ---------------------------------------------------------------------------
def reduced_motion_blocks(text: str) -> list[str]:
    blocks = []
    for match in re.finditer(r'@media\s*\([^)]*prefers-reduced-motion[^)]*\)\s*\{', text, re.I):
        depth = 0
        end = None
        for position in range(match.start(), len(text)):
            char = text[position]
            if char == '{':
                depth += 1
            elif char == '}':
                depth -= 1
                if depth == 0:
                    end = position + 1
                    break
        if end is not None:
            blocks.append(text[match.start():end])
    return blocks


def block_hashes(root: Path) -> dict[str, list[str]]:
    return {
        path: [hashlib.sha256(block.encode('utf-8')).hexdigest() for block in reduced_motion_blocks(read_at(root, path))]
        for path in touched_html
    }


rm_base = block_hashes(BASE_DIR)
rm_tip = block_hashes(TIP_DIR)
rm_diffs = {path: {'base': rm_base[path], 'tip': rm_tip[path]} for path in touched_html if rm_base[path] != rm_tip[path]}
G7 = {
    'pass': not rm_diffs,
    'base_blocks': sum(len(value) for value in rm_base.values()),
    'tip_blocks': sum(len(value) for value in rm_tip.values()),
    'diffs': rm_diffs,
}

# ---------------------------------------------------------------------------
# G8 — repo-precedent tag balance and closing html
# ---------------------------------------------------------------------------
BALANCE_TAGS = ('div', 'script', 'style', 'table', 'svg', 'ul', 'ol')

def tag_gate(root: Path) -> dict:
    errors = []
    detail = {}
    for path in touched_html:
        text = read_at(root, path)
        file_errors = []
        for tag in BALANCE_TAGS:
            opens = len(re.findall(rf'<{tag}[\s>]', text, re.I))
            closes = len(re.findall(rf'</{tag}>', text, re.I))
            if opens != closes:
                file_errors.append({'tag': tag, 'open': opens, 'close': closes})
        ends = text.rstrip().lower().endswith('</html>')
        if not ends:
            file_errors.append({'tag': 'html-end', 'open': 1, 'close': 0})
        detail[path] = {'errors': file_errors, 'ends_html': ends}
        if file_errors:
            errors.append({'file': path, 'errors': file_errors})
    return {'pass': not errors, 'files': len(touched_html), 'errors': errors, 'detail': detail}


g8_base = tag_gate(BASE_DIR)
g8_tip = tag_gate(TIP_DIR)
G8 = {'pass': g8_tip['pass'], 'base': g8_base, 'tip': g8_tip, 'balance_tags': BALANCE_TAGS}

# ---------------------------------------------------------------------------
# G9 — final diff confined to census production paths and authorised records
# ---------------------------------------------------------------------------
def allowed_diff_path(path: str) -> bool:
    if path.startswith('_passph1/'):
        return True
    if path in {'REGISTER.md', '_close/OPEN_ITEMS.md'}:
        return True
    return production_path(path)


unexpected_paths = sorted(path for path in changed_paths if not allowed_diff_path(path))
G9 = {
    'pass': not unexpected_paths,
    'base_changed_file_count': len(changed_paths),
    'tip_changed_file_count': len(changed_paths),
    'changed_paths': changed_paths,
    'unexpected': unexpected_paths,
}

# ---------------------------------------------------------------------------
# G10 — no pupil names, ASDAN PDFs or localStorage keys added
# ---------------------------------------------------------------------------
fixture = run(['node', 'tools/verify_fixture_names.mjs'], cwd=TIP_DIR, timeout=120)
fixture_pass = fixture.returncode == 0
pdfs = sorted(path for path in tracked(TIP_DIR) if path.lower().endswith('.pdf') and 'asdan' in path.lower())
KEY_RE = re.compile(r'''localStorage\s*\.\s*(?:getItem|setItem|removeItem)\s*\(\s*(["'])(?P<key>.*?)\1''', re.I | re.S)


def localstorage_keys(root: Path) -> set[str]:
    keys = set()
    for path in tracked(root):
        if Path(path).suffix.lower() not in {'.html', '.js', '.mjs', '.cjs'}:
            continue
        try:
            text = read_at(root, path)
        except Exception:
            continue
        keys.update(match.group('key') for match in KEY_RE.finditer(text))
    return keys


keys_base = localstorage_keys(BASE_DIR)
keys_tip = localstorage_keys(TIP_DIR)
added_keys = sorted(keys_tip - keys_base)
G10 = {
    'pass': fixture_pass and not pdfs and not added_keys,
    'base': {
        'localStorage_key_count': len(keys_base),
        'tracked_ASDAN_PDFs': 0,
    },
    'tip': {
        'fixture_name_gate_pass': fixture_pass,
        'fixture_name_output': (fixture.stdout + '\n' + fixture.stderr).strip()[-5000:],
        'tracked_ASDAN_PDFs': pdfs,
        'localStorage_key_count': len(keys_tip),
        'localStorage_keys_added': added_keys,
    },
}

GATES = {'G1': G1, 'G2': G2, 'G3': G3, 'G4': G4, 'G5': G5, 'G6': G6, 'G7': G7, 'G8': G8, 'G9': G9, 'G10': G10}
red = [name for name, value in GATES.items() if not value.get('pass')]
overall = 'GREEN' if not red else 'RED'

# Diff stats for exact final file list.
numstat_rows = []
for line in git('diff', '--numstat', BASE, TARGET, '--').splitlines():
    parts = line.split('\t', 2)
    if len(parts) == 3:
        added, deleted, path = parts
        numstat_rows.append({'path': path, 'added': added, 'deleted': deleted})

# Commit log, including the seven authorised edit commits.
log_rows = []
for line in git('log', '--format=%H%x09%s', f'{BASE}..{TARGET}').splitlines():
    sha_value, subject = line.split('\t', 1)
    log_rows.append({'sha': sha_value, 'subject': subject})

# Machine-readable results.
results = {
    'repository': 'MattRoper1977/Lessons',
    'base': BASE,
    'target_tip': TARGET,
    'overall': overall,
    'red_gates': red,
    'touched_html_count': len(touched_html),
    'touched_html': touched_html,
    'gates': GATES,
    'p_commits': P_COMMITS,
    'numstat': numstat_rows,
    'log': log_rows,
}
(OUT / 'GATE_RESULTS.json').write_text(json.dumps(results, indent=2), encoding='utf-8')

# Human gate report.
def status(value: dict) -> str:
    return 'PASS' if value.get('pass') else 'RED'


gate_md = [
    '# PH-1 Phase 3 — gate results',
    '',
    '- Repository: `MattRoper1977/Lessons`',
    f'- Immutable BASE: `{BASE}`',
    f'- Gate input tip: `{TARGET}`',
    f'- Touched production HTML files: **{len(touched_html)}**',
    f'- Overall: **{overall}**',
    f"- Red gates: **{', '.join(red) if red else 'none'}**",
    '',
    '| Gate | BASE measurement | Tip measurement | Result |',
    '|---|---|---|---|',
    f"| G1 | {g1_base['blocks']} inline blocks, {len(g1_base['errors'])} syntax errors | {g1_tip['blocks']} inline blocks, {len(g1_tip['errors'])} syntax errors | **{status(G1)}** |",
    f"| G2 | {g2_base.get('files', 0)} loaded; {len(g2_base.get('failures', []))} failed; harness-failed={g2_base.get('harness_failed')} | {g2_tip.get('files', 0)} loaded; {len(g2_tip.get('failures', []))} failed; harness-failed={g2_tip.get('harness_failed')}; jsdom {JSDOM_VERSION} | **{status(G2)}** |",
    f"| G3 | print-section total {G3['base_total']} | print-section total {G3['tip_total']}; changed files {len(print_diffs)} | **{status(G3)}** |",
    f"| G4 | witness set {G4.get('base_count', 'n/a')} | witness set {G4.get('tip_count', 'n/a')}; changed {len(G4.get('changed', []))}; added {len(G4.get('added_at_tip', []))}; missing {len(G4.get('missing_at_tip', []))} | **{status(G4)}** |",
    f"| G5 | loop-mark sentinel {G5['base_count']} | loop-mark sentinel {G5['tip_count']}; +{len(G5['added'])}/-{len(G5['removed'])} | **{status(G5)}** |",
    f"| G6 | {json.dumps(g6_base['counts'], sort_keys=True)} | {json.dumps(g6_tip['counts'], sort_keys=True)} | **{status(G6)}** |",
    f"| G7 | reduced-motion blocks {G7['base_blocks']} | reduced-motion blocks {G7['tip_blocks']}; changed files {len(G7['diffs'])} | **{status(G7)}** |",
    f"| G8 | {len(g8_base['errors'])} balance/end errors | {len(g8_tip['errors'])} balance/end errors | **{status(G8)}** |",
    f"| G9 | diff files {len(changed_paths)} | unexpected files {len(unexpected_paths)} | **{status(G9)}** |",
    f"| G10 | localStorage keys {len(keys_base)}; ASDAN PDFs 0 | added keys {len(added_keys)}; ASDAN PDFs {len(pdfs)}; fixture-name gate={fixture_pass} | **{status(G10)}** |",
    '',
]

for name, value in GATES.items():
    gate_md.extend([f'## {name} — {status(value)}', '', '```json', json.dumps(value, indent=2)[:30000], '```', ''])
(OUT / 'GATE_RESULTS.md').write_text('\n'.join(gate_md), encoding='utf-8')

# Ordered stop/final report. Phase 4 records are deliberately not written when red.
census_rows = [
    ('C1', 'approximately 84 in LAUNCH PEQ', '84 live / 312 whole-tree'),
    ('C2', 'not fixed', '2 production pages'),
    ('C3', 'not fixed', '101 line-level occurrences; B1 18 / B2 80 / B3 3 / B4 0'),
    ('C4', '0', '0'),
    ('C5', 'not fixed', '6 pages'),
    ('C6', 'report only', '0'),
    ('C7', '0', '1 affirmative Level 2 registration claim'),
]
p_status = [
    ('P1', 'DONE', '2 staff/print minima blocks added; pupil tasks unchanged.'),
    ('P2', 'PARTIAL', '18 B1 occurrences corrected; 80 B2 and 3 B3 occurrences held; W6 filename unchanged.'),
    ('P3', 'DONE', '6 measured credit-route pages carry the corrected route rules.'),
    ('P4', 'DONE', '4 suite-level partial-achievement notes added.'),
    ('P5', 'DONE — REPORT ONLY', 'C6 was zero; no lesson wording changed.'),
    ('P6', 'DONE', '7 BUILD hub/START_HERE panels and 1 LAUNCH Vocational panel added.'),
    ('P7', 'DONE', 'Prohibited tools, automatic awards and PEQ002 credit claims were not deployed.'),
]
awaiting = [
    'Should the live GROW Level 2 registration claim be corrected in a separately authorised P8?',
    'Which, if any, of the 80 B2 pupil-action or real-world sign-off occurrences should change?',
    'Should the 2 W6 witness-section sign-off occurrences be changed in a later pass that intentionally establishes a new G4 baseline?',
    'Should `PEQ_W6_…_Sign_Off_the_Unit.html` be renamed later with a redirect plan?',
    'What should happen to the materially divergent `*_Estate_v3` TEST COPY estates on main?',
    'Are the LAUNCH Vocational banked titles affected by the planned ASDAN Vocational Taster withdrawal?',
    'Is any learner evidence still held in the ASDAN e-portfolio that needs exporting?',
]
stop_md = [
    '# PH-1 final execution report — stopped on gate result',
    '',
    '## BASE, tip and deployment commits',
    '',
    f'- BASE: `{BASE}`',
    f'- Gate input tip: `{TARGET}`',
    '- Branch: `pass-ph1-peq-hardening`',
    '- Census: `daf746f5d8894d1b56e203ed34b641b74b0e9522`',
]
for key, value in P_COMMITS.items():
    stop_md.append(f'- {key}: `{value}`')
stop_md.extend(['', '## Census — predicted versus actual', '', '| Census | Predicted | Actual |', '|---|---|---|'])
for item, predicted, actual in census_rows:
    stop_md.append(f'| {item} | {predicted} | {actual} |')
stop_md.extend(['', '## P1–P7 status', '', '| Item | Status | Reason |', '|---|---|---|'])
for item, item_status, reason in p_status:
    stop_md.append(f'| {item} | **{item_status}** | {reason} |')
stop_md.extend(['', '## Gate results', '', '| Gate | Result |', '|---|---|'])
for name in GATES:
    stop_md.append(f'| {name} | **{status(GATES[name])}** |')
stop_md.extend([
    '',
    f"**Overall: {overall}. Red gates: {', '.join(red) if red else 'none'}.**",
    '',
])
if red:
    stop_md.extend([
        'Phase 4 records were **not** written. `REGISTER.md` and `_close/OPEN_ITEMS.md` remain unchanged because PH-1 forbids fix-forward or records closure past a red gate.',
        '',
    ])
stop_md.extend(['## Exact BASE-to-tip changed files', '', '| File | Added | Deleted |', '|---|---:|---:|'])
for row in numstat_rows:
    stop_md.append(f"| `{row['path']}` | {row['added']} | {row['deleted']} |")
stop_md.extend(['', '## AWAITING-WORD — one-line questions', ''])
for question in awaiting:
    stop_md.append(f'- {question}')
stop_md.extend([
    '',
    '## Rollback',
    '',
    f'`git checkout pass-ph1-peq-hardening && git revert --no-commit {BASE}..HEAD && git commit -m "Rollback PH-1" && git push origin pass-ph1-peq-hardening`',
    '',
])
(OUT / 'PH1_STOP_REPORT.md').write_text('\n'.join(stop_md), encoding='utf-8')

print(json.dumps({'overall': overall, 'red_gates': red, 'target': TARGET, 'touched_html': len(touched_html)}, indent=2))
