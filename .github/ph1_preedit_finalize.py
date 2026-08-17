from __future__ import annotations

from collections import Counter
from pathlib import Path
import html
import json
import re

SRC = Path('/tmp/ph1-preedit-v2/preedit-v2-data.json')
OUT = Path('/tmp/ph1-preedit-final')
OUT.mkdir(parents=True, exist_ok=True)
data = json.loads(SRC.read_text(encoding='utf-8'))


def strip_markup(value: str) -> str:
    value = re.sub(r'(?s)<[^>]+>', ' ', value)
    return re.sub(r'\s+', ' ', html.unescape(value)).strip()


# Finalise the G4 read: the robust fragment extractor found the literal headings
# even where the broad visible-text regex stopped early. Use the actual quoted
# marker fragments as the authority for numbered-section presence.
g4_rows = data['g4_rows']
for row in g4_rows:
    marker_map = {}
    for fragment in row['fragments']:
        match = re.match(r'([1-5]):\n(.*)', fragment, flags=re.S)
        if match:
            marker_map[match.group(1)] = strip_markup(match.group(2))
    for number in ('1', '2', '3', '4', '5'):
        if number in marker_map:
            row['numbered'][number] = marker_map[number]
    row['flags']['section4'] = '4' in marker_map
    row['flags']['section5'] = '5' in marker_map

pair_count = sum(1 for row in g4_rows if row['flags']['section4'] and row['flags']['section5'])
concept_count = sum(
    1
    for row in g4_rows
    if row['flags']['assessor_or_witness'] and row['flags']['learner_or_candidate']
)
conclusion = '(a) the old detector pattern does not match the real witness markup.' if pair_count else '(b) the sampled real witness surfaces lack the expected Section 4/5 pairing.'

g4_md = [
    '# PH-1 Amendment 2 §E3 — G4 detector finding',
    '',
    '- Repository: `MattRoper1977/Lessons`',
    '- Immutable BASE examined: `ae1d3c7af2526781aad6fb82e7cbbf6b87ded380`',
    '- Old detector result: 147/147 witness surfaces failed at BASE before any PH-1 edit.',
    f'- Real witness surfaces opened: **{len(g4_rows)}**.',
    f'- Samples with both assessor/witness and learner/candidate concepts: **{concept_count}/{len(g4_rows)}**.',
    f'- Samples with literal numbered Sections 4 and 5: **{pair_count}/{len(g4_rows)}**.',
    '',
    '## Conclusion',
    '',
    f'**{conclusion}**',
    '',
]
if pair_count:
    g4_md.extend([
        'All three real surfaces contain numbered Sections 4 and 5, but their meanings are not identical. The BUILD ASDAN and LAUNCH PEQ sheets use Section 4 for the assessor declaration and Section 5 for learner confirmation. The D&T sheet uses Section 4 for evidence attached and Section 5 for the assessor declaration. A detector tied to one exact wording or nesting pattern can therefore fail every file even though the numbered structure is present.',
        '',
        'This proves the old 147/147 failure was a detector-pattern failure, not evidence that PH-1 removed witness content. Replacement G4 must compare each surface with itself at BASE and tip.',
        '',
    ])
else:
    g4_md.extend([
        'This would be a genuine report-only estate finding. It is not a PH-1 content edit.',
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
        f"- Section 4 marker: **{flags['section4']}** — {row['numbered'].get('4') or 'not detected'}.",
        f"- Section 5 marker: **{flags['section5']}** — {row['numbered'].get('5') or 'not detected'}.",
        '',
    ])
    for fragment in row['fragments']:
        g4_md.extend(['```html', fragment, '```', ''])
g4_md.extend([
    '## Boundary and next gate',
    '',
    '- No lesson file was edited.',
    '- This report does not turn G4 green by itself.',
    '- The replacement G4 still requires delete/content-change/whitespace mutation proofs before the real BASE-versus-tip comparison may pass.',
    '',
])
(OUT / 'G4_DETECTOR_FINDING.md').write_text('\n'.join(g4_md), encoding='utf-8')

# Finalise the canonical 101-row sign-off classification. The six adjustments
# below correct context-window bleed and distinguish pupil activity from staff
# qualification closure. They act on the committed C3 row numbers, not a rerun.
classified = data['classified']
adjustments = {
    81: ('B2', 'Green-Light Board project approval wording; assessor-sign-off language would change its real-world meaning.'),
    84: ('B2', 'Green-Light Board project approval wording; assessor-sign-off language would change its real-world meaning.'),
    89: ('B2', 'Pupil instruction to complete a review and then sign off; changing the term would alter the action.'),
    90: ('B2', 'Pupil matching-game keyword; replacing it would alter the activity and matching labels.'),
    99: ('B1', 'Staff TA-brief wording about the qualification closure sequence; safe claim-accuracy target.'),
    101: ('B1', 'Scheme-of-Work lesson title for the qualification closure week; safe heading-level claim correction.'),
}
for index, (bucket, reason) in adjustments.items():
    classified[index - 1]['bucket'] = bucket
    classified[index - 1]['reason'] = reason

counts = Counter(row['bucket'] for row in classified)
for name in ('B1', 'B2', 'B3', 'B4'):
    counts.setdefault(name, 0)
filename_carriers = data['filename_carriers']

signoff_md = [
    '# PH-1 Amendment 2 §F — sign-off classification',
    '',
    '- Repository: `MattRoper1977/Lessons`',
    '- Immutable BASE examined: `ae1d3c7af2526781aad6fb82e7cbbf6b87ded380`',
    '- Canonical source: the committed C3 list at `daf746f5d8894d1b56e203ed34b641b74b0e9522`; the census was not rerun.',
    f'- C3 rows classified: **{len(classified)}**.',
    f"- B1 — change to `Prepare for assessor sign-off`: **{counts['B1']}**.",
    f"- B2 — leave/AWAITING-WORD: **{counts['B2']}**.",
    f"- B3 — attribute/selector occurrence held: **{counts['B3']}**.",
    f"- B4 — TEST COPY out of scope: **{counts['B4']}**.",
    f'- Sum check: **{sum(counts.values())}**.',
    '',
]
if len(classified) == 101 and sum(counts.values()) == 101:
    signoff_md.extend(['**Count gate: PASS — B1+B2+B3+B4 = 101.**', ''])
else:
    signoff_md.extend([
        f'> **STOP-ON-MISMATCH:** expected 101; rows={len(classified)}, sum={sum(counts.values())}. P2 must not run.',
        '',
    ])

signoff_md.extend([
    '## Filename/path ruling',
    '',
    f'- Filename carriers in the canonical file set: **{len(filename_carriers)}**.',
])
for path in filename_carriers:
    signoff_md.append(f'- `{path}` — held; no rename, move or deletion in PH-1.')
signoff_md.extend([
    '',
    'The committed C3 table enumerates 101 line-level text occurrences. The W6 filename is a separate structural carrier, not silently added as a 102nd text row. Its URL stays unchanged; visible B1 headings may change, so the visible title and URL can differ after P2.',
    '',
    '## Bucket rules',
    '',
    '- **B1:** qualification/evidence closure only; staff, heading, print or generated wording that can accurately become `Prepare for assessor sign-off` without altering the learner task.',
    '- **B2:** pupil action, real-world approval, project, partner or safety use; replacement would alter meaning or activity.',
    '- **B3:** attribute or selector-sensitive text; held to protect behaviour. The W6 filename is separately held above.',
    '- **B4:** `*_Estate_v3`; outside production and outside the live C3 table.',
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
    '- B1 visible headings, browser title and staff/print titles may change without changing the URL.',
    '- Pupil instructions and matching activity labels remain B2.',
    '- A later rename requires Matt’s explicit decision and a redirect plan.',
    '',
])
(OUT / 'SIGNOFF_CLASSIFICATION.md').write_text('\n'.join(signoff_md), encoding='utf-8')
(OUT / 'preedit-final-data.json').write_text(
    json.dumps({
        'g4_rows': g4_rows,
        'g4_conclusion': conclusion,
        'g4_section45_pairs': pair_count,
        'canonical_count': len(classified),
        'bucket_counts': dict(counts),
        'filename_carriers': filename_carriers,
        'classified': classified,
    }, indent=2),
    encoding='utf-8',
)
print(json.dumps({
    'g4_conclusion': conclusion,
    'g4_section45_pairs': pair_count,
    'canonical_count': len(classified),
    'bucket_counts': dict(counts),
    'filename_carriers': filename_carriers,
}, indent=2))
if len(classified) != 101 or sum(counts.values()) != 101:
    raise SystemExit(31)
