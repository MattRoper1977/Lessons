#!/usr/bin/env python3
"""K1: verbatim first PDF section, bounded by its own first two bookmarks.

Reuse UX2's PDF text and s23 checks. No truncation, paraphrase or hand-written
preparation. Ambiguous boundaries, missing guides and >60 words omit the card.
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools/ux2'))
from check_companion_packs import pdf_lines, s23_hits
from pypdf import PdfReader


def derive(root=ROOT):
    rows = json.loads((root / 'resources.json').read_text())
    entries, audit = {}, []
    for pack in rows:
        if pack.get('kind') != 'pack' or not pack.get('companionOf'):
            continue
        guides = [f for f in pack['files'] if (f['role'], f['type']) == ('teacher', 'pdf')]
        record = {'id': pack['id'], 'reason': 'no teacher PDF'}
        if len(guides) == 1:
            path = root / guides[0]['path']
            def flatten(items):
                for item in items:
                    if isinstance(item, list):
                        yield from flatten(item)
                    else:
                        yield item
            marks = list(flatten(PdfReader(path).outline))
            _, lines = pdf_lines(path)
            record.update(source=guides[0]['path'], sha256=hashlib.sha256(path.read_bytes()).hexdigest(), reason='ambiguous first section')
            if len(marks) >= 2:
                first, second = str(marks[0].title), str(marks[1].title)
                starts = [i for i, line in enumerate(lines) if line.strip() == first]
                ends = [i for i, line in enumerate(lines) if line.strip() == second]
                if len(starts) == len(ends) == 1 and starts[0] < ends[0]:
                    text = '\n'.join(lines[starts[0]:ends[0]])
                    words = len(text.split())
                    record.update(words=words, firstHeading=first, nextHeading=second)
                    if s23_hits(text.splitlines()):
                        raise ValueError('s23 learner-name field in ' + pack['id'])
                    record['reason'] = 'over 60 words' if words > 60 else 'empty section' if ends[0] == starts[0] + 1 else 'rendered'
                    if record['reason'] == 'rendered':
                        entries[pack['id']] = {k: record[k] for k in ('source', 'sha256')}
                        entries[pack['id']]['text'] = text
        audit.append(record)
    return {'schema': 1, 'entries': entries, 'audit': audit}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = derive()
    data = json.dumps(result, ensure_ascii=False, indent=2) + '\n'
    target = ROOT / 'assets/catalogue/pack-notes.json'
    if args.check:
        assert target.read_text() == data, 'Pack notes differ from the current teacher PDFs'
    else:
        target.write_text(data)
    print(json.dumps({'packs': len(result['audit']), 'rendered': len(result['entries']), 's23': 0}))
