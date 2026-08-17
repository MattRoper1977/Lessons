from __future__ import annotations

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
