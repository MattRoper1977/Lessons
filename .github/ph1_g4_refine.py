from __future__ import annotations

from pathlib import Path
import importlib.util
import json
import re
import shutil
import subprocess
import tempfile

BASE = 'ae1d3c7af2526781aad6fb82e7cbbf6b87ded380'
OUT = Path('/tmp/ph1-g4-refine')
OUT.mkdir(parents=True, exist_ok=True)
ROOT = Path.cwd()

comparator = r'''from __future__ import annotations

from pathlib import Path
import hashlib
import html
import re
import subprocess

PRINT_WITNESS_ID_RE = re.compile(r'(?i)id=["\']print-witness["\']')
WITNESS_HEADING_RE = re.compile(r'(?i)Assessor Witness Statement')


def extract_balanced_element(text: str, opening: re.Match[str]) -> str:
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
    return ''


def extract_element_by_id(text: str, target_id: str = 'print-witness') -> str:
    opening = re.search(
        rf'(?is)<(?P<tag>[a-z][a-z0-9]*)\b[^>]*\bid=["\']{re.escape(target_id)}["\'][^>]*>',
        text,
    )
    return extract_balanced_element(text, opening) if opening else ''


def extract_print_section_witness(text: str) -> str:
    # Some real witness sheets may lack the conventional ID. Accept a fallback
    # only when the heading is actually inside an element whose class contains
    # print-section. Mere prose saying a suite has a witness sheet is excluded.
    heading = WITNESS_HEADING_RE.search(text)
    if not heading:
        return ''
    candidates = []
    for opening in re.finditer(
        r'(?is)<(?P<tag>[a-z][a-z0-9]*)\b(?=[^>]*\bclass=["\'][^"\']*\bprint-section\b[^"\']*["\'])[^>]*>',
        text[:heading.start()],
    ):
        candidates.append(opening)
    for opening in reversed(candidates):
        block = extract_balanced_element(text, opening)
        if block and WITNESS_HEADING_RE.search(block):
            return block
    return ''


def witness_block(text: str) -> str:
    block = extract_element_by_id(text)
    return block if block else extract_print_section_witness(text)


def canonical(block: str) -> str:
    value = html.unescape(block).replace('\r\n', '\n').replace('\r', '\n')
    value = re.sub(r'\s+', ' ', value).strip()
    value = re.sub(r'>\s+<', '><', value)
    return value


def fingerprint_text(text: str) -> str | None:
    block = witness_block(text)
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
        if not PRINT_WITNESS_ID_RE.search(text) and not WITNESS_HEADING_RE.search(text):
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

spec = importlib.util.spec_from_file_location('g4cmp', OUT/'G4_WITNESS_COMPARATOR.py')
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
base_snapshot = module.snapshot(ROOT)

# Explicit false-positive control: suite hub mentions a witness sheet but is not one.
hub = 'LAUNCH_ASDAN/LAUNCH_ASDAN_Hub.html'
hub_excluded = hub not in base_snapshot

samples = [
    'BUILD_ASDAN/Careers/CAREERS_W1_My_Strengths.html',
    'LAUNCH_ASDAN/PEQ/PEQ_W5_Deliver_the_Activity_and_Gather_Evidence.html',
    'Build/Slideshows/BUILD_DT_W1_Workshop_Audit.html',
]
for sample in samples:
    if sample not in base_snapshot:
        raise RuntimeError(f'real witness sample missing from refined snapshot: {sample}')

mutation_root = Path(tempfile.mkdtemp(prefix='ph1-g4-refined-'))
for relative in samples:
    destination = mutation_root / relative
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(ROOT/relative, destination)

base_three = {path: module.fingerprint_file(ROOT/path) for path in samples}

# Delete section
delete_path = samples[0]
text = (mutation_root/delete_path).read_text(encoding='utf-8', errors='replace')
block = module.witness_block(text)
(mutation_root/delete_path).write_text(text.replace(block, '', 1), encoding='utf-8')
delete_tip = module.fingerprint_file(mutation_root/delete_path)
delete_red = base_three[delete_path] is not None and delete_tip is None

# Alter content
alter_path = samples[1]
text = (mutation_root/alter_path).read_text(encoding='utf-8', errors='replace')
block = module.witness_block(text)
mutated = block.replace('Assessor Witness Statement', 'Assessor Witness Statement MUTATED', 1)
(mutation_root/alter_path).write_text(text.replace(block, mutated, 1), encoding='utf-8')
alter_tip = module.fingerprint_file(mutation_root/alter_path)
alter_red = base_three[alter_path] != alter_tip

# Whitespace only
space_path = samples[2]
text = (mutation_root/space_path).read_text(encoding='utf-8', errors='replace')
block = module.witness_block(text)
mutated = re.sub(r'>\s*<', '>\n       <', block)
(mutation_root/space_path).write_text(text.replace(block, mutated, 1), encoding='utf-8')
space_tip = module.fingerprint_file(mutation_root/space_path)
space_green = base_three[space_path] == space_tip

proven = hub_excluded and delete_red and alter_red and space_green
report = [
    '# PH-1 replacement G4 — refined witness comparator mutation proof',
    '',
    f'- Immutable BASE: `{BASE}`.',
    f'- Actual witness surfaces derived at BASE: **{len(base_snapshot)}**.',
    '- Surface rule: an explicit `id="print-witness"`, or an `Assessor Witness Statement` heading genuinely enclosed by a `print-section` element.',
    f'- False-positive control `LAUNCH_ASDAN/LAUNCH_ASDAN_Hub.html` excluded: **{hub_excluded}**.',
    '',
    '## Mandatory mutations',
    '',
    f'1. Delete witness section — `{delete_path}` — red: **{delete_red}**.',
    f'2. Alter witness content — `{alter_path}` — red: **{alter_red}**.',
    f'3. Whitespace-only reformat — `{space_path}` — stays green: **{space_green}**.',
    '',
]
report += [
    '**MUTATION VERDICT: PROVEN.** The refined comparator rejects the known hub false positive and exhibits all three required mutation behaviours.' if proven else '**MUTATION VERDICT: UNPROVEN.** G4 remains red.',
    '',
    'Real G4 remains pending until this comparator checks immutable BASE against the final branch tip.',
    '',
]
(OUT/'G4_MUTATION_PROOF.md').write_text('\n'.join(report), encoding='utf-8')
data={
    'base_surface_count': len(base_snapshot),
    'hub_false_positive_excluded': hub_excluded,
    'delete_red': delete_red,
    'alter_red': alter_red,
    'whitespace_green': space_green,
    'proven': proven,
}
(OUT/'g4-refine-data.json').write_text(json.dumps(data,indent=2),encoding='utf-8')
print(json.dumps(data,indent=2))
if not proven:
    raise SystemExit(41)
