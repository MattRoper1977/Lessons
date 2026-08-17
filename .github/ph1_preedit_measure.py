from __future__ import annotations

from collections import Counter
from pathlib import Path
import html
import json
import re
import subprocess

OUT = Path('/tmp/ph1-preedit')
OUT.mkdir(parents=True, exist_ok=True)


def git(*args: str) -> str:
    return subprocess.check_output(['git', *args], text=True, errors='replace')


tracked = [Path(p) for p in git('ls-files').splitlines() if p]


def read(path: str | Path) -> str:
    return Path(path).read_text(encoding='utf-8', errors='replace')


# ---------------------------------------------------------------------------
# G4 detector finding
# ---------------------------------------------------------------------------
witness_samples = [
    'BUILD_ASDAN/Careers/CAREERS_W1_My_Strengths.html',
    'LAUNCH_ASDAN/PEQ/PEQ_W5_Deliver_the_Activity_and_Gather_Evidence.html',
    'Build/Slideshows/BUILD_DT_W1_Workshop_Audit.html',
]


def clean_snippet(value: str, limit: int = 2200) -> str:
    value = value.replace('\r', '')
    value = re.sub(r'>\s*<', '>\n<', value)
    value = re.sub(r'[ \t]+', ' ', value)
    lines = [line.strip() for line in value.splitlines() if line.strip()]
    result = '\n'.join(lines)
    if len(result) > limit:
        result = result[:limit] + '\n… [snippet truncated]'
    return result


def witness_extract(text: str) -> tuple[str, dict]:
    anchors = [
        text.lower().find('id="print-witness"'),
        text.lower().find("id='print-witness'"),
        text.lower().find('assessor witness statement'),
        text.lower().find('witness statement'),
    ]
    anchors = [value for value in anchors if value >= 0]
    if not anchors:
        return '', {'anchor': -1, 'section4': False, 'section5': False, 'learner': False, 'assessor': False}
    anchor = min(anchors)
    start = max(0, text.rfind('<div', 0, anchor), text.rfind('<section', 0, anchor))
    if start < 0:
        start = max(0, anchor - 800)
    next_print = text.find('class="print-section', anchor + 20)
    end_section = text.find('</section>', anchor + 20)
    end_div = text.find('</div>', anchor + 1200)
    candidates = [value for value in (next_print, end_section, end_div) if value > anchor]
    end = min(candidates) if candidates else min(len(text), anchor + 9000)
    if end - start < 1200:
        end = min(len(text), start + 7000)
    block = text[start:end]
    lowered = html.unescape(block).lower()
    # The real estate uses several visual section styles; detect numbered headings,
    # explicit section labels and the learner/assessor concepts separately.
    section4 = bool(re.search(r'(?:section\s*4|§\s*4|>\s*4\s*(?:[.·:)\-]|</)|\b4\s*[.·:)\-]\s*(?:assessor|witness|staff))', lowered))
    section5 = bool(re.search(r'(?:section\s*5|§\s*5|>\s*5\s*(?:[.·:)\-]|</)|\b5\s*[.·:)\-]\s*(?:learner|candidate|confirmation))', lowered))
    learner = bool(re.search(r'learner|candidate', lowered))
    assessor = bool(re.search(r'assessor|witness|staff', lowered))
    return block, {
        'anchor': anchor,
        'section4': section4,
        'section5': section5,
        'learner': learner,
        'assessor': assessor,
    }


g4_rows = []
for path in witness_samples:
    text = read(path)
    block, flags = witness_extract(text)
    # Extract checkable markup fragments carrying numbered headings or the key concepts.
    fragments = []
    for match in re.finditer(
        r'(?is)<(?:h[1-6]|p|div|section|label|strong|td|th)[^>]*>.*?(?:assessor|witness|learner|candidate|section\s*[45]|>\s*[45]\s*[.·:)\-]).*?</(?:h[1-6]|p|div|section|label|strong|td|th)>',
        block,
    ):
        fragment = clean_snippet(match.group(0), 900)
        if fragment and fragment not in fragments:
            fragments.append(fragment)
        if len(fragments) >= 5:
            break
    if not fragments:
        fragments = [clean_snippet(block, 1800)]
    g4_rows.append({'path': path, 'flags': flags, 'fragments': fragments})

concept_pair_count = sum(1 for row in g4_rows if row['flags']['learner'] and row['flags']['assessor'])
number_pair_count = sum(1 for row in g4_rows if row['flags']['section4'] and row['flags']['section5'])
if concept_pair_count >= 2:
    g4_conclusion = '(a) the old detector pattern does not match the real witness markup.'
else:
    g4_conclusion = '(b) the sampled estate surfaces do not contain the expected assessor/learner pairing.'

g4 = [
    '# PH-1 Amendment 2 §E3 — G4 detector finding',
    '',
    '- Repository: `MattRoper1977/Lessons`',
    '- Immutable BASE examined: `ae1d3c7af2526781aad6fb82e7cbbf6b87ded380`',
    '- Old detector result: 147/147 witness surfaces failed at BASE before any PH-1 edit.',
    f'- Sampled real witness surfaces: **{len(g4_rows)}**.',
    f'- Surfaces containing both assessor/witness and learner/candidate concepts: **{concept_pair_count}/{len(g4_rows)}**.',
    f'- Surfaces matching this report’s broad numbered 4/5 recogniser: **{number_pair_count}/{len(g4_rows)}**.',
    '',
    '## Conclusion',
    '',
    f'**{g4_conclusion}**',
    '',
    'The old 100% BASE failure cannot be used as evidence that PH-1 removed witness content. The check must compare each surface’s detected structure at BASE with the same surface at tip and must be mutation-proven before it is trusted.',
    '',
    '## Actual markup read',
    '',
]
for row in g4_rows:
    flags = row['flags']
    g4.extend([
        f"### `{row['path']}`",
        '',
        f"- Assessor/witness concept: **{flags['assessor']}**",
        f"- Learner/candidate concept: **{flags['learner']}**",
        f"- Broad Section 4 marker: **{flags['section4']}**",
        f"- Broad Section 5 marker: **{flags['section5']}**",
        '',
    ])
    for index, fragment in enumerate(row['fragments'], start=1):
        g4.extend([f'Fragment {index}:', '', '```html', fragment, '```', ''])

g4.extend([
    '## PH-1 boundary',
    '',
    '- This is a detector finding, not an instruction to rewrite a lesson.',
    '- No witness surface was modified.',
    '- The replacement G4 must be BASE-versus-tip only and must pass its three mandatory mutations before the real gate runs.',
    '',
])
(OUT / 'G4_DETECTOR_FINDING.md').write_text('\n'.join(g4), encoding='utf-8')

# ---------------------------------------------------------------------------
# Sign-off classification
# ---------------------------------------------------------------------------
def is_production_path(path: Path) -> bool:
    value = str(path)
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


production_files = sorted(str(path) for path in tracked if is_production_path(path))
pattern = re.compile(r'(?i)\bsign(?:\s+|-)off\b')
occurrences: list[dict] = []

# Filename/path occurrence required by Amendment 2 F1/F2.
for path in production_files:
    for match in pattern.finditer(path):
        occurrences.append({
            'path': path,
            'line': None,
            'offset': match.start(),
            'exact': match.group(0),
            'context_type': 'filename/path',
            'window': path,
            'bucket': 'B3',
            'reason': 'Filename/path is held; changing it would break links and requires a redirect plan.',
            'source': 'path',
        })


def inside_tag(text: str, pos: int) -> tuple[bool, str]:
    left = text.rfind('<', 0, pos)
    right = text.rfind('>', 0, pos)
    if left > right:
        close = text.find('>', pos)
        return True, text[left:close + 1 if close >= 0 else pos + 180]
    return False, ''


def inside_script(text: str, pos: int) -> bool:
    open_pos = text.lower().rfind('<script', 0, pos)
    close_pos = text.lower().rfind('</script', 0, pos)
    return open_pos > close_pos


def nearest_tag(text: str, pos: int) -> str:
    match = re.search(r'<([a-zA-Z0-9]+)(?:\s[^>]*)?>[^<]*$', text[max(0, pos - 500):pos])
    return match.group(1).lower() if match else ''


def classify(path: str, text: str, match: re.Match[str]) -> tuple[str, str, str]:
    pos = match.start()
    exact = match.group(0)
    window = html.unescape(text[max(0, pos - 360):min(len(text), match.end() + 420)])
    lower = window.lower()
    in_tag, tag_text = inside_tag(text, pos)
    if in_tag:
        tag_lower = tag_text.lower()
        if any(token in tag_lower for token in ('href=', ' id=', 'data-', 'aria-controls=', 'onclick=', 'queryselector', 'getelementbyid')):
            return 'B3', 'Attribute/path/selector context; editing could break navigation or script binding.', 'attribute/selector'
    if inside_script(text, pos):
        context_type = 'script/data'
    else:
        tag = nearest_tag(text, pos)
        if tag in {'h1', 'h2', 'h3', 'h4', 'h5', 'h6'}:
            context_type = 'heading'
        elif 'print-' in text[max(0, pos - 1800):pos].lower():
            context_type = 'print-zone line'
        else:
            context_type = 'body text'

    qualification_tokens = (
        'sign off the unit', 'sign-off the unit', 'unit sign-off', 'unit sign off',
        'comsk1', 'communication unit', 'unit complete', 'close the unit',
        'portfolio evidence', 'witness staff sign off', 'staff sign off the',
    )
    project_tokens = (
        'green light', 'trips & visits', 'trips and visits', 'risk assessment',
        'approver', 'permission to go ahead', 'aut 2 delivery', 'plan pack',
        'project case', 'site sign-off', 'partner sign-off', 'delivery decision',
        'sign-off decision', 'sign-off comes from', 'sign-off counts the same',
    )
    pupil_tokens = (
        'instructions:', 'independent', 'your task', 'i can ', 'sentence starters',
        'word bank', 'what will that take', 'true for you today', 'draw lines',
        'say how', 'write ', 'present my part',
    )

    if any(token in lower for token in project_tokens):
        return 'B2', 'Real-world/project approval context; replacing it with assessor sign-off would alter the pupil action or meaning.', context_type
    if any(token in lower for token in qualification_tokens):
        return 'B1', 'Qualification/evidence closure wording on a heading, staff surface, print line or generated content surface.', context_type
    if any(token in lower for token in pupil_tokens):
        return 'B2', 'Pupil task/action context; replacement would change what the pupil is being asked to do.', context_type
    if context_type in {'heading', 'print-zone line'}:
        return 'B1', 'Heading or print-zone wording within the qualification estate; safe claim-accuracy target subject to exact replacement.', context_type
    if 'staff' in lower or 'witness' in lower or 'assessor' in lower:
        return 'B1', 'Staff/witness-facing wording; safe claim-accuracy target.', context_type
    # Conservative remainder: leave rather than force a semantic change.
    return 'B2', 'Meaning is not demonstrably qualification sign-off; leave for Matt rather than alter an action or approval concept.', context_type


for path in production_files:
    text = read(path)
    for match in pattern.finditer(text):
        bucket, reason, context_type = classify(path, text, match)
        line = text.count('\n', 0, match.start()) + 1
        raw_window = text[max(0, match.start() - 170):min(len(text), match.end() + 230)]
        plain_window = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', html.unescape(raw_window))).strip()
        occurrences.append({
            'path': path,
            'line': line,
            'offset': match.start(),
            'exact': match.group(0),
            'context_type': context_type,
            'window': plain_window[:420],
            'bucket': bucket,
            'reason': reason,
            'source': 'content',
        })

occurrences.sort(key=lambda row: (row['path'], -1 if row['line'] is None else row['line'], row['offset']))
bucket_counts = Counter(row['bucket'] for row in occurrences)
# B4 is deliberately zero because the live production set excludes TEST COPY paths.
bucket_counts.setdefault('B4', 0)
total = len(occurrences)

signoff = [
    '# PH-1 Amendment 2 §F — sign-off classification',
    '',
    '- Repository: `MattRoper1977/Lessons`',
    '- Immutable BASE examined: `ae1d3c7af2526781aad6fb82e7cbbf6b87ded380`',
    '- Production paths only; no `*_Estate_v3` occurrence is included in the live total.',
    f'- Live occurrences measured: **{total}**.',
    f"- B1 — change: **{bucket_counts['B1']}**.",
    f"- B2 — leave/AWAITING-WORD: **{bucket_counts['B2']}**.",
    f"- B3 — filename/path/selector held: **{bucket_counts['B3']}**.",
    f"- B4 — TEST COPY out of scope: **{bucket_counts['B4']}**.",
    f"- Sum check: **{sum(bucket_counts.values())}**.",
    '',
]
if total != 101 or sum(bucket_counts.values()) != total:
    signoff.extend([
        f'> **STOP-ON-MISMATCH:** C3 committed census expected 101 live occurrences; this classifier measured {total}. The classification must not be used for edits until reconciled.',
        '',
    ])
else:
    signoff.extend([
        '**Count gate: PASS — B1+B2+B3+B4 = 101.**',
        '',
    ])

signoff.extend([
    '## Bucket rules used',
    '',
    '- **B1:** qualification/evidence closure wording on staff surfaces, headings, print lines or generated content surfaces; candidate for `Prepare for assessor sign-off`.',
    '- **B2:** pupil action or real-world approval wording where the replacement would change the task or meaning; leave and ask Matt.',
    '- **B3:** filename, path, href, ID, anchor or selector-sensitive occurrence; leave to preserve URLs and scripts.',
    '- **B4:** TEST COPY occurrence; outside the live count and outside PH-1 write scope.',
    '',
    '## All occurrences',
    '',
    '| # | Bucket | File | Line | Exact | Context type | Classification reason | Checkable context |',
    '|---:|---|---|---:|---|---|---|---|',
])
for index, row in enumerate(occurrences, start=1):
    line = 'path' if row['line'] is None else str(row['line'])
    context = row['window'].replace('|', '\\|').replace('`', '\\`')
    reason = row['reason'].replace('|', '\\|')
    signoff.append(
        f"| {index} | {row['bucket']} | `{row['path']}` | {line} | `{row['exact']}` | {row['context_type']} | {reason} | {context} |"
    )
signoff.extend([
    '',
    '## W6 filename ruling',
    '',
    '- `LAUNCH_ASDAN/PEQ/PEQ_W6_Review_Progress_and_Sign_Off_the_Unit.html` remains unchanged as a path under B3.',
    '- On-page qualification closure wording may be changed only where classified B1.',
    '- After P2, the page title and URL may differ; that later rename requires a separately authorised redirect plan.',
    '',
])
(OUT / 'SIGNOFF_CLASSIFICATION.md').write_text('\n'.join(signoff), encoding='utf-8')
(OUT / 'preedit-data.json').write_text(
    json.dumps(
        {
            'g4': g4_rows,
            'g4_conclusion': g4_conclusion,
            'signoff_total': total,
            'bucket_counts': dict(bucket_counts),
            'occurrences': occurrences,
        },
        indent=2,
    ),
    encoding='utf-8',
)
print(json.dumps({'g4_conclusion': g4_conclusion, 'signoff_total': total, 'bucket_counts': dict(bucket_counts)}, indent=2))
if total != 101:
    raise SystemExit(21)
