"""Check reviewed Humanities cover content, route mapping and native bytes.

This is static acceptance. Browser interaction and print evidence are separate.
"""
from pathlib import Path
from urllib.parse import urlsplit, unquote
import argparse
import copy
import hashlib
import json
import zipfile
from lxml import html
from build_resources import DEST, MINUTES, PATHWAYS, NATIVE_ROOT, archive_name, render, render_index

HERE = Path(__file__).resolve().parent


def digest(data):
    return hashlib.sha256(data).hexdigest()


def native_archive_contract(data, pathway, original_members, shared):
    """Require an exact pathway slice of the original reviewed member set."""
    import io
    expected = {name for name in original_members if name.startswith(pathway + '/') or name in shared}
    found = {}
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        names = archive.namelist()
        assert len(names) == len(set(names)), 'Duplicate archive member'
        assert set(names) == {NATIVE_ROOT + name for name in expected}, 'Incomplete or unexpected pathway members'
        for name in names:
            assert name.startswith(NATIVE_ROOT)
            relative = name.removeprefix(NATIVE_ROOT)
            blob = archive.read(name)
            source = original_members[relative]
            assert len(blob) == source['bytes'] and digest(blob) == source['sha256'], 'Changed original native member: ' + relative
            found[relative] = blob
    return found


def document_contract(document, content):
    ids = document.xpath('//*[@id]/@id')
    assert len(ids) == len(set(ids)), 'Duplicate element identity'
    assert document.xpath('//html/@lang') == ['en-GB']
    assert document.xpath('//h1/text()') == [content['title']], 'Lesson title'
    stages = document.xpath('//*[@data-stage]')
    assert [int(s.get('data-stage')) for s in stages] == list(range(8)), 'Stage sequence'
    assert [int(s.get('data-minutes')) for s in stages] == MINUTES, 'Period minutes'
    assert sum(int(s.get('data-minutes')) for s in stages) == 40
    assert document.xpath('//nav[@aria-label="Choose a week"]/a/@href') == [
        content['id'].split('_W')[0] + '_W' + str(n) + '.html' for n in range(3, 8)
    ], 'Complete five-week peer navigation'
    assert document.xpath('//a[@aria-current="page"]/@href') == [content['id'] + '.html']
    assert not document.xpath('//details[@open]'), 'Premature answer or teacher key'
    assert not document.xpath('//form|//iframe|//video|//script[not(@src)]'), 'Unexpected transport or executable content'
    assert len(document.xpath('//aside[contains(@class,"teacher-guide")]//details[contains(@class,"teacher-answers")]')) == 1
    assert document.xpath('//aside[contains(@class,"teacher-guide")]//details[contains(@class,"teacher-answers")]//li/text()') == content['answers']
    for node in document.xpath('//textarea'):
        assert len(document.xpath('//label[@for=$id]', id=node.get('id'))) == 1, 'Response field label'
    for node in document.xpath('//a[@target="_blank"]'):
        assert {'noopener', 'noreferrer'} <= set(node.get('rel', '').split())
    source_text = document.xpath('//*[@id="stage-2"]//div[contains(@class,"source-board")]/p[not(@class)]/text()')
    assert source_text == content['source_lines'], 'Reviewed source card'
    if content['lane'] == 'LAUNCH':
        assert document.xpath('//*[@id="stage-6"]//div[contains(@class,"re-source")]/p[not(@class)]/text()') == content['re_source_lines'], 'Integrated RE source card'
    assert document.xpath('//*[@id="stage-6"]/ol/li/text()') == content['task'], 'Reviewed pupil tasks'


def check(root, reference):
    root, reference = root.resolve(), reference.resolve()
    content_bytes = (HERE / 'CONTENT.json').read_bytes()
    content = json.loads(content_bytes)
    manifest = json.loads((HERE / 'SOURCE_MANIFEST.json').read_text())
    downloads = json.loads((HERE / 'DOWNLOAD_MANIFEST.json').read_text())
    assert digest(content_bytes) == manifest['content_sha256'], 'Final reviewed content changed'
    assert len(content) == 25 and len({c['id'] for c in content}) == 25
    records = {r['id']: r for r in manifest['records']}
    assert set(records) == {c['id'] for c in content}
    assert len(downloads['dependencies']) == 69, '66 individual downloads and three complete pathway archives'
    assert len({d['path'] for d in downloads['dependencies']}) == 69
    for item in downloads['dependencies']:
        file = root / item['path']
        assert file.is_relative_to(root) and file.is_file(), 'Missing native download: ' + item['path']
        data = file.read_bytes()
        assert len(data) == item['bytes'] and digest(data) == item['sha256'], 'Native download identity: ' + item['path']
    native_members_bytes = (HERE / 'ORIGINAL_MEMBER_MANIFEST.json').read_bytes()
    assert digest(native_members_bytes) == manifest['native_member_manifest_sha256'], 'Original member manifest identity'
    native_members = json.loads(native_members_bytes)
    assert native_members['source_archive_sha256'] == manifest['native_pack_sha256']
    assert native_members['source_archive_root'] == NATIVE_ROOT
    members_by_path = {member['path']: member for member in native_members['members']}
    assert len(native_members['members']) == len(members_by_path) == 132
    shared = set(native_members['shared_members'])
    assert shared == {'START_HERE_David_Humanities_RE.docx', 'START_HERE_David_Humanities_RE.pdf'}
    assert {r['pathway'] for r in downloads['archives']} == set(PATHWAYS) and len(downloads['archives']) == 3
    all_members = {}
    for archive in downloads['archives']:
        assert archive['filename'] == archive_name(archive['pathway'])
        file = root / DEST / archive['filename']
        data = file.read_bytes()
        assert len(data) == archive['bytes'] < 10_000_000 and digest(data) == archive['sha256']
        found = native_archive_contract(data, archive['pathway'], members_by_path, shared)
        assert set(archive['members']) == set(found)
        for name, blob in found.items():
            assert name not in all_members or (name in shared and all_members[name] == blob)
            all_members[name] = blob
    assert set(all_members) == set(members_by_path), 'All 132 original members must be available across the pathway packs'
    for item in downloads['dependencies']:
        file = root / item['path']
        if file.suffix == '.zip':
            continue
        relative = file.relative_to(root / DEST / 'downloads').as_posix()
        assert file.read_bytes() == all_members[relative], 'Individual download differs from reviewed native member: ' + relative
    assert not (root / DEST / 'David_Humanities_RE_OneDrive_Pack.zip').exists(), 'Superseded online archive must not remain'
    all_routes = [r for record in records.values() for r in record['existing_routes']]
    assert len(all_routes) == 30 and len({r['path'] for r in all_routes}) == 30
    for route in all_routes:
        file = reference / route['path']
        assert file.is_file() and digest(file.read_bytes()) == route['sha256'], 'Existing lesson preservation: ' + route['path']
    dest = root / DEST
    pages = []
    for c in content:
        record = records[c['id']]
        assert (record['pathway'], record['week'], record['subject'], record['sow']) == (c['lane'], c['week'], c['subject'], c['sow'])
        file = dest / (c['id'] + '.html')
        assert file.read_text() == render(c, content, record), 'Generated page must match reviewed content: ' + c['id']
        document = html.fromstring(file.read_text())
        document_contract(document, c)
        for node in document.xpath('//*[@href or @src]'):
            for attribute in ['href', 'src']:
                value = node.get(attribute)
                if not value:
                    continue
                url = urlsplit(value)
                if url.scheme:
                    assert attribute == 'href' and url.scheme == 'https' and value in c['source_refs'], 'Unexpected external source'
                elif not url.path:
                    assert url.fragment in document.xpath('//*[@id]/@id'), 'Missing local fragment'
                else:
                    target = (file.parent / unquote(url.path)).resolve()
                    assert target.is_relative_to(root), 'Path traversal'
                    relative = target.relative_to(root)
                    assert target.is_file() or (reference / relative).is_file(), 'Missing link: ' + value
        pages.append({'id': c['id'], 'path': file.relative_to(root).as_posix(), 'sha256': digest(file.read_bytes())})
    assert (dest / 'index.html').read_text() == render_index(content)
    index = html.fromstring((dest / 'index.html').read_text())
    assert len(index.xpath('//article[contains(@class,"lesson-card")]')) == 25
    assert index.xpath('//section[contains(@class,"pathway-section")]/@id') == ['build', 'grow', 'launch']
    assert index.xpath('//div[@class="downloads"]/a[@download]/@href') == [archive_name(lane) for lane in PATHWAYS]
    for link in index.xpath('//a[contains(@href,"?subject=")]/@href'):
        assert link == '../../index.html?subject=Humanities%20%26%20RE'
    for name in ['resource.css', 'resource.js']:
        assert (dest / name).read_bytes() == (HERE / name).read_bytes(), name + ' must match the reviewed source'
    script = (dest / 'resource.js').read_text()
    for forbidden in ['fetch(', 'XMLHttpRequest', 'localStorage', 'sessionStorage', 'sendBeacon', 'innerHTML']:
        assert forbidden not in script, 'Unexpected storage or transport: ' + forbidden
    css = (dest / 'resource.css').read_text()
    for required in ['@media print', '.teacher-guide,.answer', 'prefers-reduced-motion', 'min-height:44px']:
        assert required in css, 'Missing accessibility or print rule: ' + required
    seed = html.fromstring((dest / (content[0]['id'] + '.html')).read_text())
    controls = {}
    mutations = {
        'missing-title': lambda d: d.xpath('//h1')[0].getparent().remove(d.xpath('//h1')[0]),
        'premature-teacher-key': lambda d: d.xpath('//details[contains(@class,"teacher-answers")]')[0].set('open', ''),
        'wrong-period-duration': lambda d: d.xpath('//*[@data-stage]')[0].set('data-minutes', '41'),
        'missing-pupil-task': lambda d: d.xpath('//*[@id="stage-6"]/ol/li')[0].getparent().remove(d.xpath('//*[@id="stage-6"]/ol/li')[0]),
    }
    for name, mutate in mutations.items():
        changed = copy.deepcopy(seed)
        mutate(changed)
        try:
            document_contract(changed, content[0])
            controls[name] = False
        except AssertionError:
            controls[name] = True
    # These byte fixtures prove the archive check rejects content loss or drift.
    import io
    fixture = {'BUILD/example.pdf': b'pupil worksheet', 'START_HERE_David_Humanities_RE.pdf': b'teacher starting guide'}
    fixture_manifest = {name: {'sha256': digest(blob), 'bytes': len(blob)} for name, blob in fixture.items()}
    def fixture_zip(members):
        stream = io.BytesIO()
        with zipfile.ZipFile(stream, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
            for name, blob in members.items():
                archive.writestr(NATIVE_ROOT + name, blob)
        return stream.getvalue()
    assert native_archive_contract(fixture_zip(fixture), 'BUILD', fixture_manifest, {'START_HERE_David_Humanities_RE.pdf'}) == fixture
    controls['valid-native-archive'] = True
    bad_archives = {
        'missing-native-member': {'START_HERE_David_Humanities_RE.pdf': fixture['START_HERE_David_Humanities_RE.pdf']},
        'changed-native-bytes': {**fixture, 'BUILD/example.pdf': b'changed worksheet'},
        'wrong-pathway-member': {**fixture, 'GROW/unrelated.pdf': b'unrelated'},
    }
    for name, bad in bad_archives.items():
        try:
            native_archive_contract(fixture_zip(bad), 'BUILD', fixture_manifest, {'START_HERE_David_Humanities_RE.pdf'})
            controls[name] = False
        except AssertionError:
            controls[name] = True
    assert all(controls.values()), 'A planted defect escaped the checker'
    return {'result': 'PASS', 'scope': 'Static content, mapping, link, generated-byte and download checks; not a browser or print visual claim.', 'pages': pages, 'native_downloads': 66, 'pathway_archives': 3, 'original_members_preserved': len(all_members), 'existing_routes_preserved': 30, 'additional_coverage_claimed': 0, 'controls': controls}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, default=HERE.parents[1])
    parser.add_argument('--reference-root', type=Path)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    result = check(args.root, args.reference_root or args.root)
    if args.report:
        args.report.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: (len(v) if k == 'pages' else v) for k, v in result.items() if k != 'scope'}))
