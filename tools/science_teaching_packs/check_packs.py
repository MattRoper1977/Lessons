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
    # Native-pack source records describe the bytes used at authoring time.
    # Current classroom editions have their own reviewed, full-byte identities;
    # use those without rewriting the pack's historical source provenance.
    reviewed = json.loads((root / 'tools/easter/SCIENCE_ORIGINAL_TARGETS.json').read_text())
    assert reviewed['schema'] == 'original-science-browser-targets-v1'
    current_sources = {row['path']: row['expectedPatchedSha256'] for row in reviewed['targets']}
    assert len(current_sources) == len(reviewed['targets']), 'Duplicate classroom source expectation'
    assert set(current_sources) == set(bindings), 'Classroom source coverage drift'
    page = html.fromstring((packs / 'index.html').read_text())
    ids = page.xpath('//@id')
    assert len(ids) == len(set(ids)), 'Duplicate download anchor'
    assert 'David' not in page.text_content(), 'Public pack naming must be generic'
    files_seen = set()
    deck_count = archive_count = 0
    for pathway in ('BUILD', 'GROW', 'LAUNCH'):
        directory = packs / pathway
        source = json.loads((directory / 'SOURCE_MANIFEST.json').read_text())
        archives = json.loads((directory / 'DOWNLOAD_INDEX.json').read_text())['archives']
        expected = {f'W{w}L{p}' for w in range(3, 8) for p in range(1, 4)} if pathway == 'LAUNCH' else {f'W{w}{p}' for w in range(3, 8) for p in 'AB'}
        assert len(source['lessons']) == len(expected)
        assert {r['id'] for r in source['lessons']} == expected
        for lesson in source['lessons']:
            assert lesson['durationMinutes'] == 40
            original = root / lesson['source']['repoPath']
            assert digest(original) == current_sources[lesson['source']['repoPath']], 'Classroom source drift: ' + str(original)
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
        standard = [a for a in archives if a.get('kind') != 'format']
        assert len(standard) == len(expected) + 6
        per_week = 3 if pathway == 'LAUNCH' else 2
        assert sorted(len(a['lessonIds']) for a in standard) == [1]*len(expected) + [per_week]*5 + [len(expected)]
        formats = [a for a in archives if a.get('kind') == 'format']
        assert {a['format'] for a in formats} == {'PDF', 'PPTX', 'DOCX'}
        for archive in archives:
            path = directory / archive['file']
            assert path.stat().st_size == archive['bytes'] and digest(path) == archive['sha256']
            included = [lesson for lesson in source['lessons'] if lesson['id'] in archive['lessonIds']]
            required = {item['file'] for lesson in included for item in lesson['files']}
            required.update(item['file'] for item in source.get('packFiles', []))
            if archive.get('kind') == 'format':
                required = {rel for rel in required if Path(rel).suffix[1:].upper() == archive['format']}
            assert required <= set(archive['members'].values()), 'Incomplete companion resources: ' + str(path)
            with zipfile.ZipFile(path) as z:
                assert z.testzip() is None
                if archive.get('kind') != 'format':
                    manifests = [name for name in z.namelist() if Path(name).name == 'SOURCE_MANIFEST.json']
                    assert len(manifests) == 1, 'Missing or duplicate archived source provenance: ' + str(path)
                    archived_lessons = json.loads(z.read(manifests[0]))['lessons']
                    archived_sources = {row['id']: row['source'] for row in archived_lessons}
                    assert len(archived_sources) == len(archived_lessons), 'Duplicate archived source lesson'
                    assert archived_sources == {row['id']: row['source'] for row in included}, 'Pack source provenance drift: ' + str(path)
                for name, relative in archive['members'].items():
                    assert z.read(name) == (directory / relative).read_bytes(), 'Stale ZIP member: ' + name
                if archive.get('kind') == 'format':
                    assert all(Path(n).suffix[1:].upper() == archive['format'] for n in z.namelist())
                assert not any('David' in n or Path(n).is_absolute() or '..' in Path(n).parts for n in z.namelist())
            assert page.xpath('//a[@href=$href]', href=pathway + '/' + archive['file'])
            archive_count += 1
        for item in source.get('packFiles', []):
            path = directory / item['file']
            assert path.stat().st_size == item['bytes'] and digest(path) == item['sha256'], 'Pack guidance drift'
            if path.suffix in {'.pptx', '.docx', '.xlsx', '.pdf'}:
                files_seen.add(path)
    assert deck_count == 35
    for href in page.xpath('//a/@href'):
        u = urlsplit(href)
        if u.scheme or u.netloc or href.startswith('/'):
            continue
        if u.path:
            target = packs / unquote(u.path)
            assert target.exists(), 'Broken local download link: ' + href
        elif u.fragment:
            assert u.fragment in ids
    assert len(bindings) == 25
    return {'status': 'PASS', 'editable_powerpoints': deck_count, 'lesson_week_whole_format_archives': archive_count,
            'unique_native_downloads': len(files_seen), 'classroom_source_routes_preserved': len(bindings)}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    args = parser.parse_args()
    print(json.dumps(check(args.root.resolve()), indent=2))
