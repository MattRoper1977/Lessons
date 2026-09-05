#!/usr/bin/env python3
"""Inspect actual Chrome print pages; emit page images for visual review."""
import argparse
import json
from pathlib import Path
import fitz

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--artifacts', type=Path, required=True)
args = parser.parse_args()
root = args.artifacts
browser = json.loads((root/'science-browser.json').read_text())
rows = []
for record in browser['pdfs']:
    document = fitz.open(root/record['file'])
    row = {'file': record['file'], 'lesson': record['lesson'], 'level': record['level'],
           'pages': [], 'problems': []}
    text = ' '.join(' '.join(page.get_text().split()) for page in document)
    expected = record.get('requiredText')
    if expected and expected not in text:
        row['problems'].append('Required teaching text missing: '+expected)
    for index, page in enumerate(document):
        words = page.get_text('words')
        bounds = page.rect + (-1, -1, 1, 1)
        outside = [word[4] for word in words if not bounds.contains(fitz.Rect(word[:4]))]
        if len(words) < 3:
            row['problems'].append(f'Page {index+1}: empty or near-empty')
        if outside:
            row['problems'].append(f'Page {index+1}: out-of-page text '+repr(outside))
        image = f'{Path(record["file"]).stem}-p{index+1:02d}.png'
        page.get_pixmap(matrix=fitz.Matrix(1, 1)).save(root/image)
        row['pages'].append({'page': index+1, 'words': len(words), 'image': image})
    rows.append(row)
report = {'schema': 'original-science-pdf-inspection-v1', 'pdfs': rows,
          'scope': 'Every exported page rendered; word bounds, blank pages and required teaching text measured. Visual review of the page images remains required.',
          'result': 'PASS' if rows and all(not r['problems'] for r in rows) else 'FAIL'}
(root/'science-print.json').write_text(json.dumps(report, indent=2)+'\n')
print(json.dumps({'result': report['result'], 'pdfs': len(rows),
                  'pages': sum(len(r['pages']) for r in rows),
                  'problems': [{r['file']: r['problems']} for r in rows if r['problems']]}))
raise SystemExit(0 if report['result'] == 'PASS' else 1)
