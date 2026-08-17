from __future__ import annotations

from collections import Counter, defaultdict
from pathlib import Path
import html
import json
import re
import subprocess

OUT = Path('/tmp/ph1-preedit-v2')
OUT.mkdir(parents=True, exist_ok=True)
BASE = 'ae1d3c7af2526781aad6fb82e7cbbf6b87ded380'
CENSUS_TIP = 'daf746f5d8894d1b56e203ed34b641b74b0e9522'


def git(*args: str) -> str:
    return subprocess.check_output(['git', *args], text=True, errors='replace')


def read(path: str | Path) -> str:
    return Path(path).read_text(encoding='utf-8', errors='replace')


def strip_markup(value: str) -> str:
    value = re.sub(r'(?is)<script\b.*?</script>', ' ', value)
    value = re.sub(r'(?is)<style\b.*?</style>', ' ', value)
    value = re.sub(r'(?s)<[^>]+>', ' ', value)
    value = html.unescape(value)
    return re.sub(r'\s+', ' ', value).strip()


def extract_element_by_id(text: str, target_id: str) -> str:
    opening = re.search(
        rf'(?is)<(?P<tag>[a-z][a-z0-9]*)\b[^>]*\bid=["\']{re.escape(target_id)}["\'][^>]*>',
        text,
    )
    if not opening:
        return ''
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


def compact_markup(value: str, limit: int = 1400) -> str:
    value = value.replace('\r', '')
    value = re.sub(r'>\s*<', '>\n<', value)
    value = re.sub(r'[ \t]+', ' ', value)
    value = '\n'.join(line.strip() for line in value.splitlines() if line.strip())
    return value if len(value) <= limit else value[:limit] + '\n… [snippet truncated]'


def marker_fragments(block: str) -> list[str]:
    decoded = html.unescape(block)
    positions = []
    for number in range(1, 6):
        match = re.search(rf'(?i)\b{number}\s*(?:·|&#183;|&middot;|[.:-])\s*', decoded)
        if match:
            positions.append((number, match.start()))
    fragments = []
    for number, pos in positions:
        start = max(0, decoded.rfind('<', 0, pos - 1))
        end = decoded.find('</p>', pos)
        if end < 0 or end - start > 1800:
            end = min(len(decoded), pos + 900)
        else:
            end += len('</p>')
        fragment = compact_markup(decoded[start:end], 1500)
        fragments.append(f'{number}:\n{fragment}')
    if not fragments:
        fragments.append('No numbered marker fragment was found. Opening witness markup:\n' + compact_markup(block, 2400))
    return fragments


# ---------------------------------------------------------------------------
# G4 detector finding — inspect three real witness surfaces at immutable BASE.
# ---------------------------------------------------------------------------
witness_samples = [
    'BUILD_ASDAN/Careers/CAREERS_W1_My_Strengths.html',
    'LAUNCH_ASDAN/PEQ/PEQ_W5_Deliver_the_Activity_and_Gather_Evidence.html',
    'Build/Slideshows/BUILD_DT_W1_Workshop_Audit.html',
]
g4_rows = []
for path in witness_samples:
    source = read(path)
    block = extract_element_by_id(source, 'print-witness')
    if not block:
        # Fall back to the first explicit witness heading, but record the fallback.
        anchor = source.lower().find('assessor witness statement')
        block = source[max(0, anchor - 300):min(len(source), anchor + 15000)] if anchor >= 0 else ''
        extraction = 'fallback around first Assessor Witness Statement text'
    else:
        extraction = 'complete element with id="print-witness"'
    visible = strip_markup(block)
    numbered = {}
    for number in range(1, 6):
        match = re.search(rf'(?i)(?:^|\s){number}\s*(?:·|[.:-])\s*([^0-9].{{0,220}}?)(?=(?:\s[1-5]\s*(?:·|[.:-]))|$)', visible)
        numbered[str(number)] = match.group(1).strip() if match else None
    flags = {
        'has_block': bool(block),
        'assessor_or_witness': bool(re.search(r'(?i)assessor|witness|staff', visible)),
        'learner_or_candidate': bool(re.search(r'(?i)learner|candidate', visible)),
        'section4': numbered['4'] is not None,
        'section5': numbered['5'] is not None,
    }
    g4_rows.append({
        'path': path,
        'extraction': extraction,
        'flags': flags,
        'numbered': numbered,
        'fragments': marker_fragments(block),
    })

pair_count = sum(1 for row in g4_rows if row['flags']['section4'] and row['flags']['section5'])
concept_count = sum(1 for row in g4_rows if row['flags']['assessor_or_witness'] and row['flags']['learner_or_candidate'])
if pair_count >= 1 or concept_count >= 2:
    conclusion = '(a) the old detector pattern does not match the real witness markup.'
else:
    conclusion = '(b) the sampled real witness surfaces lack the expected Section 4/5 pairing.'

g4_md = [
    '# PH-1 Amendment 2 §E3 — G4 detector finding',
    '',
    '- Repository: `MattRoper1977/Lessons`',
    f'- Immutable BASE examined: `{BASE}`',
    '- Old detector result: 147/147 witness surfaces failed at BASE before any PH-1 edit.',
    f'- Real witness surfaces opened: **{len(g4_rows)}**.',
    f'- Samples with both assessor/witness and learner/candidate concepts: **{concept_count}/{len(g4_rows)}**.',
    f'- Samples with literal numbered Sections 4 and 5 under the broad parser used here: **{pair_count}/{len(g4_rows)}**.',
    '',
    '## Conclusion',
    '',
    f'**{conclusion}**',
    '',
]
if conclusion.startswith('(a)'):
    g4_md.extend([
        'The estate does contain real witness structures, and the sampled markup shows why a detector tied to one exact wording or nesting pattern can fail every file. Replacement G4 must compare each surface with itself at BASE and tip, not impose a newly invented estate-wide template.',
        '',
    ])
else:
    g4_md.extend([
        'This is a real report-only estate finding. It is not a PH-1 content edit and must become a later open question if the full gate set reaches Phase 4.',
        '',
    ])
g4_md.extend(['## Actual markup read', ''])
for row in g4_rows:
    flags = row['flags']
    g4_md.extend([
        f"### `{row['path']}`",
        '',
        f"- Extraction: {row['extraction']}.",
        f"- Assessor/witness concept: **{flags['assessor_or_witness']}**.",
        f"- Learner/candidate concept: **{flags['learner_or_candidate']}**.",
        f"- Section 4 marker: **{flags['section4']}** — {row['numbered']['4'] or 'not detected'}.",
        f"- Section 5 marker: **{flags['section5']}** — {row['numbered']['5'] or 'not detected'}.",
        '',
    ])
    for fragment in row['fragments']:
        g4_md.extend(['```html', fragment, '```', ''])
g4_md.extend([
    '## Boundary and next gate',
    '',
    '- No lesson file was edited.',
    '- This report does not turn G4 green by itself.',
    '- The replacement G4 still requires the mandatory delete/content-change/whitespace mutation proof before the real BASE-versus-tip comparison may pass.',
    '',
])
(OUT / 'G4_DETECTOR_FINDING.md').write_text('\n'.join(g4_md), encoding='utf-8')


# ---------------------------------------------------------------------------
# C3 canonical sign-off classification — use the committed census rows exactly.
# ---------------------------------------------------------------------------
census = git('show', f'{CENSUS_TIP}:_passph1/CENSUS.md')
try:
    c3_block = census.split('## C3 — sign-off strings', 1)[1].split('## C4', 1)[0]
except IndexError:
    raise SystemExit('Unable to locate C3 block in committed census')
row_re = re.compile(
    r'^- `(?P<path>[^`]+)` L(?P<line>\d+) — `(?P<exact>[^`]+)` — \*\*(?P<context>[^*]+)\*\* — (?P<summary>.*)$'
)
canonical = []
for raw in c3_block.splitlines():
    match = row_re.match(raw)
    if match:
        canonical.append({
            'path': match.group('path'),
            'line': int(match.group('line')),
            'exact': match.group('exact'),
            'census_context': match.group('context'),
            'census_summary': match.group('summary'),
        })

filename_carriers = sorted({row['path'] for row in canonical if re.search(r'(?i)sign[_-]off', Path(row['path']).name)})

used_occurrence = defaultdict(int)


def locate_context(row: dict) -> tuple[str, str, bool]:
    source = read(row['path'])
    lines = source.splitlines()
    if row['line'] < 1 or row['line'] > len(lines):
        return row['census_summary'], '', False
    line_text = lines[row['line'] - 1]
    exact = row['exact']
    key = (row['path'], row['line'], exact)
    wanted = used_occurrence[key]
    used_occurrence[key] += 1
    found = [match for match in re.finditer(re.escape(exact), line_text)]
    if wanted >= len(found):
        found = [match for match in re.finditer(re.escape(exact), line_text, flags=re.I)]
    if wanted >= len(found):
        return row['census_summary'], '', False
    match = found[wanted]
    start = max(0, match.start() - 360)
    end = min(len(line_text), match.end() + 460)
    raw_window = line_text[start:end]
    plain = strip_markup(raw_window)
    # Determine whether the exact token lies within an opening tag/attribute.
    left = line_text.rfind('<', 0, match.start())
    right = line_text.rfind('>', 0, match.start())
    in_attribute = left > right
    tag_window = line_text[left:line_text.find('>', match.end()) + 1] if in_attribute else ''
    return plain or row['census_summary'], tag_window, in_attribute


def bucket(row: dict, context_text: str, tag_window: str, in_attribute: bool) -> tuple[str, str]:
    combined = html.unescape(' '.join([
        row['exact'], row['census_context'], row['census_summary'], context_text, tag_window,
    ])).lower()

    if in_attribute and any(token in tag_window.lower() for token in ('href=', ' id=', 'data-', 'aria-', 'onclick=', 'name=')):
        return 'B3', 'The occurrence sits in an attribute/path/selector-sensitive token; leave it to avoid breaking behaviour.'

    real_world = (
        'green light', 'trips & visits', 'trips and visits', 'risk assessment', 'approver',
        'permission to go ahead', 'aut 2 delivery', 'plan pack', 'project case', 'station is safe',
        "someone else's station", 'partner sign-off', 'partner confirmation', 'blueprint',
        'quality and safety sign-off route', 'site sign-off', 'delivery instead of paperwork',
        'consent forms', 'professional register', 'risk sign-off', 'sign-off decision',
    )
    pupil_action = (
        'instructions:', 'sentence starters', 'word bank', 'draw lines', 'match the review',
        'name future use, then sign off', 'true for you today', 'what will that take',
        'i can present my part', 'you sign off', 'sign off someone', 'sign-off counts the same',
    )
    qualification = (
        'sign off the unit', 'communication (comsk1)', 'communication unit', 'unit complete',
        'close communication', 'assessor witness statement', 'feedback sheet', 'knowledge organiser',
        'portfolio evidence', 'community evidence', 'completed challenges', 'practical + hygiene evidence',
        'foodwise m1', 'li m1 practical evidence', 'completed portfolio + predicted grade',
        'witness staff sign off', 'with plan, delivery and review all evidenced',
        'review and sign off', 'review progress and sign off',
    )

    if any(token in combined for token in real_world):
        return 'B2', 'Real-world, project, safety or partner approval: replacing it with assessor sign-off would change the task or meaning.'
    if any(token in combined for token in pupil_action):
        return 'B2', 'Pupil action or matching/scaffolding instruction: changing the term would alter what the pupil does.'
    if any(token in combined for token in qualification):
        return 'B1', 'Qualification/evidence closure wording on a staff, heading, print or generated surface.'
    if row['census_context'] == 'pupil task text':
        return 'B2', 'Committed census classifies this as pupil task text; leave it for Matt rather than alter the action.'
    if row['census_context'] in {'heading', 'print-zone line', 'staff/prose'} and 'unit' in combined:
        return 'B1', 'Unit/qualification heading, print or staff wording; claim-accuracy replacement is additive to the task.'
    return 'B2', 'No reliable qualification-only reading was established; conservative leave/AWAITING-WORD classification.'


classified = []
for row in canonical:
    context_text, tag_window, in_attribute = locate_context(row)
    chosen, reason = bucket(row, context_text, tag_window, in_attribute)
    classified.append({
        **row,
        'bucket': chosen,
        'reason': reason,
        'context_text': context_text,
        'attribute_window': tag_window,
        'in_attribute': in_attribute,
    })

counts = Counter(row['bucket'] for row in classified)
counts.setdefault('B1', 0)
counts.setdefault('B2', 0)
counts.setdefault('B3', 0)
counts.setdefault('B4', 0)

signoff_md = [
    '# PH-1 Amendment 2 §F — sign-off classification',
    '',
    '- Repository: `MattRoper1977/Lessons`',
    f'- Immutable BASE examined: `{BASE}`',
    f'- Canonical source: committed C3 list at `{CENSUS_TIP}`; the census was not rerun.',
    f'- C3 rows parsed: **{len(canonical)}**.',
    f"- B1 — change to `Prepare for assessor sign-off`: **{counts['B1']}**.",
    f"- B2 — leave/AWAITING-WORD: **{counts['B2']}**.",
    f"- B3 — structural/selector occurrence held: **{counts['B3']}**.",
    f"- B4 — TEST COPY out of scope: **{counts['B4']}**.",
    f'- Sum check: **{sum(counts.values())}**.',
    '',
]
if len(canonical) != 101 or sum(counts.values()) != 101:
    signoff_md.extend([
        f'> **STOP-ON-MISMATCH:** committed C3 says 101; parser found {len(canonical)} and bucket sum is {sum(counts.values())}. Do not run P2.',
        '',
    ])
else:
    signoff_md.extend(['**Count gate: PASS — B1+B2+B3+B4 = 101.**', ''])

signoff_md.extend([
    '## Filename/path ruling',
    '',
    f'- Filename carriers found in the canonical file set: **{len(filename_carriers)}**.',
])
for path in filename_carriers:
    signoff_md.append(f'- `{path}` — held; no rename, move or deletion in PH-1.')
if filename_carriers:
    signoff_md.extend([
        '',
        'The committed C3 list enumerates line-level content rows. The filename is therefore recorded as a separate structural carrier rather than silently added as a 102nd textual row. Its path remains unchanged under Amendment 2 F1.',
        '',
    ])

signoff_md.extend([
    '## Bucket rules',
    '',
    '- **B1:** qualification/evidence closure only; staff, heading, print or generated wording that can accurately become `Prepare for assessor sign-off` without altering the learner task.',
    '- **B2:** pupil action, real-world approval, project, partner or safety use; replacement would alter meaning or activity.',
    '- **B3:** attribute, selector, filename or path-sensitive carrier; held to protect navigation and scripts.',
    '- **B4:** `*_Estate_v3`; outside production and outside the C3 live total.',
    '',
    '## All 101 canonical occurrences',
    '',
    '| # | Bucket | File | Line | Exact census string | Census context | Reason | Checkable context |',
    '|---:|---|---|---:|---|---|---|---|',
])
for index, row in enumerate(classified, start=1):
    context = row['context_text'].replace('|', '\\|').replace('`', '\\`')[:520]
    reason = row['reason'].replace('|', '\\|')
    signoff_md.append(
        f"| {index} | {row['bucket']} | `{row['path']}` | {row['line']} | `{row['exact']}` | {row['census_context']} | {reason} | {context} |"
    )
signoff_md.extend([
    '',
    '## W6 page',
    '',
    '- The filename `LAUNCH_ASDAN/PEQ/PEQ_W6_Review_Progress_and_Sign_Off_the_Unit.html` is held.',
    '- B1 on-page headings and staff/print titles may change without changing the URL.',
    '- Any pupil instruction or matching activity remains B2.',
    '- A later rename requires Matt’s explicit decision and a redirect plan.',
    '',
])
(OUT / 'SIGNOFF_CLASSIFICATION.md').write_text('\n'.join(signoff_md), encoding='utf-8')
(OUT / 'preedit-v2-data.json').write_text(
    json.dumps({
        'g4_rows': g4_rows,
        'g4_conclusion': conclusion,
        'canonical_count': len(canonical),
        'bucket_counts': dict(counts),
        'filename_carriers': filename_carriers,
        'classified': classified,
    }, indent=2),
    encoding='utf-8',
)
print(json.dumps({
    'g4_conclusion': conclusion,
    'g4_section45_pairs': pair_count,
    'canonical_count': len(canonical),
    'bucket_counts': dict(counts),
    'filename_carriers': filename_carriers,
}, indent=2))
if len(canonical) != 101 or sum(counts.values()) != 101:
    raise SystemExit(21)
