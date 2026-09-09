"""Check final review coverage and that packaged files are the reviewed versions."""
from pathlib import Path
import hashlib, json, zipfile

ROOT = Path(__file__).resolve().parents[1]
def read(name):
    return json.loads((ROOT / 'qa' / name).read_text())
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

sources = {p.stem: sha(p) for p in (ROOT / 'content').glob('*.json')}
assert len(sources) == 24
science = read('independent_science_review.json')
assert science['status'] == 'science_pass'
assert {k: v['source_sha256'] for k, v in science['lessons'].items()} == sources
assert all(v['status'] == 'science_pass' for v in science['lessons'].values())
for path, expected in science['interactive_engine_science']['files'].items():
    assert sha(ROOT / path) == expected, path
assert read('final_verification.json')['status'] == 'PASS'
assert read('ppt/FINAL_QA.json')['allPass']
assert read('SVG_REVIEW.json')['status'] == 'PASS'

html = read('HTML_FINAL_REPORT.json')
assert len(html['files']) == 24 and not html['local_missing_links']
dom = {row['id']: row for row in read('html_dom_report.json')}
for row in html['files']:
    id = row['id']
    assert row['sourceSha256'] == sources[id] == dom[id]['sourceSha256']
    assert row['htmlSha256'] == sha(ROOT / 'output' / id / 'Lesson.html') == dom[id]['htmlSha256']

review_files = [
    'root_build_first4_doc_visual_QA.json', 'BUILD_LAST4_DOC_VISUAL_QA.json',
    'grow_author_QA.json', 'root_two_doc_visual_QA.json',
    'root_launch_first3_doc_visual_QA.json', 'LAUNCH_LAST2_DOC_VISUAL_QA.json',
    'LAUNCH_MIDDLE2_DOC_VISUAL_QA.json',
]
reviewed = {}
for file in review_files:
    report = read(file)
    assert report['status'] == 'PASS', file
    assert not report.get('unresolved_findings'), file
    for row in report['lessons']:
        id = row['id']
        assert id not in reviewed, id
        assert row['source_sha256'] == sources[id], (file, id)
        reviewed[id] = file
assert set(reviewed) == set(sources)

packages = read('zip_validation.json')
for package in packages:
    path = Path(package['file'])
    assert path.stat().st_size < 20_000_000
    assert sha(path) == package['sha256']
    with zipfile.ZipFile(path) as archive:
        assert archive.testzip() is None
        prefix = path.stem + '/'
        for id in package['lessons']:
            assert archive.read(prefix + id + '/Editable_lesson_source.json') == (ROOT / 'content' / (id + '.json')).read_bytes()
            for source_file in (ROOT / 'output' / id).rglob('*'):
                if source_file.is_file():
                    assert archive.read(prefix + id + '/' + str(source_file.relative_to(ROOT / 'output' / id))) == source_file.read_bytes(), str(source_file)

counts = read('final_verification.json')['lessons']
result = {
    'status': 'PASS', 'lessons': 24, 'pathways': 3,
    'slides': sum(row['slides'] for row in counts),
    'pupil_pages': sum(row['pages']['Pupil'] for row in counts),
    'teacher_pages': sum(row['pages']['Teacher'] for row in counts),
    'review_reports': review_files, 'current_source_hashes': sources,
    'zip_bytes': {row['pathway']: row['bytes'] for row in packages},
    'native_browser_and_phone': 'Unverified; shipped JavaScript state checks and SVG render review are recorded separately.'
}
(ROOT / 'qa' / 'delivery_gate.json').write_text(json.dumps(result, indent=2))
print(json.dumps({k: v for k, v in result.items() if k not in ['current_source_hashes', 'review_reports']}, indent=2))
