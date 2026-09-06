"""Verify public pack payloads, source binding and direct download discovery."""
from pathlib import Path
from hashlib import sha256
from urllib.parse import urlsplit, unquote
import argparse
import json
import zipfile
from lxml import html

ROOT = Path(__file__).resolve().parents[2]
PACK_REL = 'Science_Teesside/Teaching_Packs'


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def check(root=ROOT):
    packs = root / PACK_REL
    bindings = json.loads((root / 'assets/catalogue/science-download-bindings.json').read_text())
    page = html.fromstring((packs / 'index.html').read_text())
    ids = page.xpath('//@id')
    assert len(ids) == len(set(ids)), 'Duplicate download anchor'
    assert 'David' not in page.text_content(), 'Public pack naming must be generic'
    files_seen = set()
    deck_count = archive_count = 0
    for pathway in ('BUILD', 'GROW'):
        directory = packs / pathway
        source = json.loads((directory / 'SOURCE_MANIFEST.json').read_text())
        archives = json.loads((directory / 'DOWNLOAD_INDEX.json').read_text())['archives']
        assert len(source['lessons']) == 10
        assert {r['id'] for r in source['lessons']} == {f'W{w}{p}' for w in range(3, 8) for p in 'AB'}
        for lesson in source['lessons']:
            assert lesson['durationMinutes'] == 40
            original = root / lesson['source']['repoPath']
            assert digest(original) == lesson['source']['sha256'], 'Classroom source drift: ' + str(original)
            assert bindings[lesson['source']['repoPath']].split('#')[1] in ids
            assert any(f['format'] == 'PPTX' and f['role'] == 'Teaching slides' for f in lesson['files'])
            assert any(f['format'] == 'DOCX' and f['role'] == 'Pupil materials' for f in lesson['files'])
            assert any(f['format'] == 'PDF' and f['role'] == 'Teacher guidance and answers' for f in lesson['files'])
            for item in lesson['files']:
                rel = Path(item['file'])
                assert not rel.is_absolute() and '..' not in rel.parts
                path = directory / rel
                assert path.stat().st_size == item['bytes'] and digest(path) == item['sha256'], 'Download drift: ' + str(path)
                assert page.xpath('//a[@href=$href]', href=pathway + '/' + item['file']), 'Missing direct format link'
                if path.suffix in {'.pptx', '.docx', '.xlsx'}:
                    with zipfile.ZipFile(path) as z:
                        assert z.testzip() is None
                        text = ''.join(z.read(n).decode('utf-8') for n in z.namelist() if n.endswith('.xml'))
                        assert 'David' not in text, 'Personal naming in public document: ' + str(path)
                        if path.suffix == '.pptx':
                            assert '<a:t>' in text, 'PowerPoint has no editable text'
                    if path.suffix == '.pptx' and path not in files_seen: deck_count += 1
                elif path.suffix == '.pdf':
                    assert path.read_bytes().startswith(b'%PDF-')
                files_seen.add(path)
        assert len(archives) == 16
        assert sorted(len(a['lessonIds']) for a in archives) == [1]*10 + [2]*5 + [10]
        for archive in archives:
            path = directory / archive['file']
            assert path.stat().st_size == archive['bytes'] and digest(path) == archive['sha256']
            with zipfile.ZipFile(path) as z:
                assert z.testzip() is None
                assert not any('David' in n or Path(n).is_absolute() or '..' in Path(n).parts for n in z.namelist())
            assert page.xpath('//a[@href=$href]', href=pathway + '/' + archive['file'])
            archive_count += 1
    assert deck_count == 20
    for href in page.xpath('//a/@href'):
        u = urlsplit(href)
        if u.scheme or u.netloc or href.startswith('/'):
            continue
        if u.path:
            target = packs / unquote(u.path)
            assert target.exists(), 'Broken local download link: ' + href
        elif u.fragment:
            assert u.fragment in ids
    assert len(bindings) == 10
    return {'status': 'PASS', 'editable_powerpoints': deck_count, 'lesson_week_whole_archives': archive_count,
            'unique_native_downloads': len(files_seen), 'existing_weekly_source_routes_preserved': len(bindings)}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    args = parser.parse_args()
    print(json.dumps(check(args.root.resolve()), indent=2))
