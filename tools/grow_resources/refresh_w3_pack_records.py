"""Refresh the GROW pack records for the reviewed Week 3 Friction replacements only.

Rewrites, from the bytes on disk:
  * SOURCE_MANIFEST.json  - W3A/W3B file sizes, digests and revision; manifest revision
  * DOWNLOAD_INDEX.json and the seven downloads/*.zip that carry Week 3 content,
    written from their committed member maps with the builder's fixed timestamps
  * SHA256SUMS.txt        - existing rows only, digests recomputed, row count asserted
  * Teaching_Packs/index.html and science-download-bindings.json - through build_hub()

It never adds or removes a manifest file, an archive or a checksum row, and it
refuses if a lesson outside Week 3 would change. Run after the native files and
START_HERE.txt files are final:

    python3 tools/grow_resources/refresh_w3_pack_records.py
"""
from hashlib import sha256
from pathlib import Path
import json, subprocess, sys, zipfile
from copy import deepcopy

ROOT = Path(__file__).resolve().parents[2]
PACK = ROOT / 'Science_Teesside/Teaching_Packs/GROW'
REVISION = '2026-09-15'
WEEK3 = {'W3A', 'W3B'}
sys.path.insert(0, str(ROOT / 'tools/science_teaching_packs'))
import build_hub  # noqa: E402


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def load(path):
    return json.loads(path.read_text())


def save(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')


def refresh_manifest():
    manifest = load(PACK / 'SOURCE_MANIFEST.json')
    changed = []
    for lesson in manifest['lessons']:
        for item in lesson['files']:
            path = PACK / item['file']
            current = digest(path)
            if current != item['sha256']:
                assert lesson['id'] in WEEK3, 'unexpected change outside Week 3: ' + item['file']
                item['bytes'] = path.stat().st_size; item['sha256'] = current; item['revision'] = REVISION
                changed.append(item['file'])
            else:
                assert path.stat().st_size == item['bytes'], item['file']
        if lesson['id'] in WEEK3:
            lesson['revision'] = REVISION
    for item in manifest.get('packFiles', []):
        assert digest(PACK / item['file']) == item['sha256'], 'pack guidance changed: ' + item['file']
    manifest['revision'] = REVISION
    save(PACK / 'SOURCE_MANIFEST.json', manifest)
    return changed


def refresh_archives():
    """Rewrite only the archives that carry Week 3 content, using each archive's
    committed member map verbatim, the builder's fixed timestamps and compression,
    and the same archived SOURCE_MANIFEST.json subset. Archives without Week 3
    content are not touched, so their committed bytes stay identical."""
    index = load(PACK / 'DOWNLOAD_INDEX.json')
    source = load(PACK / 'SOURCE_MANIFEST.json')
    stamp = (2026, 9, 6, 0, 0, 0)
    changed, kept = [], []
    for archive in index['archives']:
        if not WEEK3 & set(archive['lessonIds']):
            kept.append(archive['file']); continue
        output = PACK / archive['file']
        members = archive['members']
        kind = archive.get('kind')
        prefix = '' if kind == 'format' else next(iter(members)).split('/', 1)[0] + '/'
        chosen = [x for x in source['lessons'] if x['id'] in archive['lessonIds']]
        with zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as z:
            for name, rel in members.items():
                info = zipfile.ZipInfo(name, stamp); info.compress_type = zipfile.ZIP_DEFLATED
                z.writestr(info, (PACK / rel).read_bytes())
            if kind != 'format':
                subset = deepcopy(source); subset['lessons'] = deepcopy(chosen); subset['lessonCount'] = len(chosen)
                info = zipfile.ZipInfo(prefix + 'SOURCE_MANIFEST.json', stamp); info.compress_type = zipfile.ZIP_DEFLATED
                z.writestr(info, json.dumps(subset, indent=2, ensure_ascii=False) + '\n')
        current = digest(output)
        if current != archive['sha256']:
            archive['bytes'] = output.stat().st_size; archive['sha256'] = current; archive['revision'] = REVISION
            changed.append(archive['file'])
    save(PACK / 'DOWNLOAD_INDEX.json', index)
    return {'rebuilt': changed, 'untouched': kept}


def refresh_sums():
    path = PACK / 'SHA256SUMS.txt'
    rows = path.read_text().splitlines()
    out, changed = [], []
    for row in rows:
        old_digest, rel = row.split('  ', 1)
        current = digest(PACK / rel)
        if current != old_digest:
            changed.append(rel)
        out.append(f'{current}  {rel}')
    assert len(out) == len(rows)
    path.write_text('\n'.join(out) + '\n')
    return changed


if __name__ == '__main__':
    report = {'manifestFiles': refresh_manifest(), 'archives': refresh_archives(), 'checksumRows': refresh_sums()}
    build_hub.build()
    print(json.dumps(report, indent=2))
