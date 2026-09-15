"""Refresh the LAUNCH pack records for the reviewed W4L1 Diffusion replacements only.

Rewrites, from the bytes on disk:
  * SOURCE_MANIFEST.json  - W4L1 file sizes, digests and revision; the three pack-guidance
                            files the W4L1 revision changes (Pupil_Worksheets.pdf and the
                            teacher guide DOCX/PDF); manifest revision
  * DOWNLOAD_INDEX.json and every downloads/*.zip whose member map carries a changed
    file, written from the committed member maps with the builder's fixed timestamps
    (the teacher guide and the combined worksheets travel in every archive, so every
    archive is rewritten; each one is reported)
  * SHA256SUMS.txt        - existing rows only, digests recomputed, row count asserted
  * Teaching_Packs/index.html and science-download-bindings.json - through build_hub()

It never adds or removes a manifest file, an archive or a checksum row, and it
refuses if a lesson other than W4L1 or a pack file outside the three would change.
Run after tools/launch_resources/author_w4l1_natives.py:

    python3 tools/launch_resources/refresh_w4l1_pack_records.py
"""
from hashlib import sha256
from pathlib import Path
import json, sys, zipfile
from copy import deepcopy

ROOT = Path(__file__).resolve().parents[2]
PACK = ROOT / 'Science_Teesside/Teaching_Packs/LAUNCH'
REVISION = '2026-09-15'
LESSON = 'W4L1'
PACK_FILES = {'Pupil_Worksheets.pdf', 'Teacher_Guide_And_Answers.docx', 'Teacher_Guide_And_Answers.pdf'}
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
                assert lesson['id'] == LESSON or item['file'] in PACK_FILES, 'unexpected change outside W4L1: ' + item['file']
                item['bytes'] = path.stat().st_size; item['sha256'] = current; item['revision'] = REVISION
                if item['file'] not in changed:
                    changed.append(item['file'])
            else:
                assert path.stat().st_size == item['bytes'], item['file']
        if lesson['id'] == LESSON:
            lesson['revision'] = REVISION
    for item in manifest.get('packFiles', []):
        path = PACK / item['file']
        current = digest(path)
        if current != item['sha256']:
            assert item['file'] in PACK_FILES, 'pack guidance changed outside the W4L1 revision: ' + item['file']
            item['bytes'] = path.stat().st_size; item['sha256'] = current; item['revision'] = REVISION
            if item['file'] not in changed:
                changed.append(item['file'])
    manifest['revision'] = REVISION
    save(PACK / 'SOURCE_MANIFEST.json', manifest)
    return changed


def refresh_archives(changed_files):
    """Rewrite every archive whose committed member map carries a changed file, using
    that member map verbatim, the builder's fixed timestamps and compression, and the
    same archived SOURCE_MANIFEST.json subset. Any other archive keeps its bytes."""
    index = load(PACK / 'DOWNLOAD_INDEX.json')
    source = load(PACK / 'SOURCE_MANIFEST.json')
    stamp = (2026, 9, 6, 0, 0, 0)
    changed, kept = [], []
    for archive in index['archives']:
        members = archive['members']
        if not (set(members.values()) & set(changed_files)):
            kept.append(archive['file']); continue
        output = PACK / archive['file']
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
    index['revision'] = REVISION
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
    files = refresh_manifest()
    report = {'manifestFiles': files, 'archives': refresh_archives(files), 'checksumRows': refresh_sums()}
    build_hub.build()
    print(json.dumps(report, indent=2))
