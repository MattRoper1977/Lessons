"""Check the actual CI print exports for pupil/teacher separation.

The existing print reviewer renders every export and checks clipping and blank
pages. This adds a complete 25-page export set and a planted teacher-key marker.
"""
from pathlib import Path
import argparse
import json
import fitz

HERE = Path(__file__).resolve().parent


def inspect(text, required, forbidden):
    normalized = ' '.join(text.split())
    problems = []
    if ' '.join(required.split()) not in normalized:
        problems.append('The lesson title is absent from its pupil print')
    if forbidden in normalized:
        problems.append('The teacher answer marker leaked into a pupil print')
    return problems


def run(artifacts):
    browser = json.loads((artifacts / 'humanities-cover-browser.json').read_text())
    content = json.loads((HERE / 'CONTENT.json').read_text())
    expected = {c['id'] + '-humanities-pupil.pdf' for c in content}
    assert browser['result'] == 'PASS', 'The browser acceptance must pass'
    assert len(browser['pdfs']) == 25 and {r['file'] for r in browser['pdfs']} == expected, 'One distinct pupil export per reviewed cover period'
    rows = []
    for entry in browser['pdfs']:
        with fitz.open(artifacts / entry['file']) as document:
            text = ' '.join(page.get_text() for page in document)
            pages = len(document)
        rows.append({'file': entry['file'], 'pages': pages, 'problems': inspect(text, entry['requiredText'], entry['forbiddenText'])})
    controls = {
        'valid-pupil': not inspect('My lesson. Pupil source and response.', 'My lesson.', 'ANSWER_LEAK'),
        'teacher-answer-leak': bool(inspect('My lesson. ANSWER_LEAK', 'My lesson.', 'ANSWER_LEAK')),
        'missing-title': bool(inspect('Pupil source and response.', 'My lesson.', 'ANSWER_LEAK')),
    }
    result = {'schema': 'humanities-cover-print-content-v1', 'result': 'PASS' if all(controls.values()) and all(not r['problems'] for r in rows) else 'FAIL', 'pdfs': rows, 'controls': controls, 'scope': 'Text extraction from actual Chromium exports. The existing print inspector supplies page images, blank-page and clipping checks. Human/agent visual review remains a release requirement.'}
    (artifacts / 'humanities-cover-print-content.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result))
    return 0 if result['result'] == 'PASS' else 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--artifacts', type=Path, required=True)
    args = parser.parse_args()
    raise SystemExit(run(args.artifacts))
