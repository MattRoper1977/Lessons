"""Stage reviewed native Science files and rebuild download metadata and ZIPs.

Run only after the supplied BUILD, GROW and LAUNCH directories pass visual QA.
Existing public file and archive paths are retained. Authoring sidecars are excluded.
"""
from pathlib import Path
from hashlib import sha256
from copy import deepcopy
import argparse
import json
import re
import shutil
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[2]
PACKS = ROOT / 'Science_Teesside/Teaching_Packs'
REVISION = '2026-09-06'
NATIVE = {'.pptx', '.docx', '.pdf', '.xlsx', '.txt'}


def load(path):
    return json.loads(path.read_text())


def save(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')


def metadata(directory, relative, role=None):
    path = directory / relative
    result = {'file': relative, 'filename': path.name, 'format': path.suffix[1:].upper(),
              'bytes': path.stat().st_size, 'sha256': sha256(path.read_bytes()).hexdigest(),
              'revision': REVISION}
    if role:
        result['role'] = role
    return result


def copy_reviewed_existing(pathway, reviewed):
    directory = PACKS / pathway
    manifest = load(directory / 'SOURCE_MANIFEST.json')
    files = {item['file'] for lesson in manifest['lessons'] for item in lesson['files']}
    files.update(p.relative_to(directory).as_posix() for p in directory.rglob('*')
                 if p.is_file() and p.suffix in NATIVE and 'downloads' not in p.parts)
    for relative in sorted(files):
        target = directory / relative
        source = reviewed / relative
        if not source.is_file():
            matches = list(reviewed.rglob(target.name))
            # GROW authoring packages use a longer prefix than the live DOCX names.
            if not matches and pathway == 'GROW' and any(role in target.name for role in ('_Pupil.', '_Teacher.')):
                code = re.search(r'W[3-7][AB]', target.name).group()
                role = 'Pupil' if '_Pupil.' in target.name else 'Teacher'
                matches = list(reviewed.glob(f'lessons/{code}/*_{role}{target.suffix}'))
            if len(matches) == 1:
                source = matches[0]
            elif target.suffix in {'.txt', '.xlsx'} or target.parent == directory:
                # Approved unchanged pack-level guidance and recording templates.
                continue
            else:
                raise ValueError(f'Missing or ambiguous reviewed replacement: {relative}')
        shutil.copyfile(source, target)
    if (reviewed / 'SOURCE_MAPPING.json').is_file():
        shutil.copyfile(reviewed / 'SOURCE_MAPPING.json', directory / 'SOURCE_MAPPING.json')
    known_names = {Path(relative).name for relative in files}
    for path in reviewed.iterdir():
        if path.is_file() and path.suffix in NATIVE and path.name not in known_names:
            shutil.copyfile(path, directory / path.name)
    manifest['revision'] = REVISION
    manifest['visualRefresh'] = 'Editable teaching materials aligned with the classroom HTML design.'
    for lesson in manifest['lessons']:
        lesson['revision'] = REVISION
        for item in lesson['files']:
            item.update(metadata(directory, item['file']))
            item.pop('pages', None)  # Old page totals must not describe refreshed PDFs.
    manifest['packFiles'] = [metadata(directory, p.relative_to(directory).as_posix(), 'Pack guidance')
                             for p in sorted(directory.iterdir()) if p.is_file() and p.suffix in NATIVE]
    save(directory / 'SOURCE_MANIFEST.json', manifest)


def create_launch(slides, documents):
    directory = PACKS / 'LAUNCH'
    directory.mkdir(exist_ok=True)
    for supplied in (slides, documents):
        for path in sorted(supplied.rglob('*')):
            if path.is_file() and path.suffix in NATIVE:
                target = directory / path.relative_to(supplied)
                if 'David' in target.name:
                    raise ValueError('Personal source filename cannot become a public download')
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(path, target)
    lessons = []
    sources = ROOT / 'Science_Teesside/Launch'
    for week in range(3, 8):
        for part in range(1, 4):
            code = f'W{week}L{part}'
            html_source, = sources.glob(f'SCI_L_W{week}_L{part}_*.html')
            deck, = (directory / f'Week_{week}').glob(f'{code}_*.pptx')
            title = deck.stem[len(code) + 1:].replace('_', ' ')
            repo_path = html_source.relative_to(ROOT).as_posix()
            files = []
            for path in sorted((directory / f'Week_{week}').glob(code + '_*')):
                if path.suffix not in NATIVE:
                    continue
                role = ('Teaching slides' if path.suffix == '.pptx' or path.stem == deck.stem else
                        'Pupil materials' if '_Worksheet' in path.name else
                        'Supported worksheet' if '_supported' in path.name else
                        'Depth worksheet' if '_depth' in path.name else 'Standard worksheet')
                files.append(metadata(directory, path.relative_to(directory).as_posix(), role))
            for relative, role in [
                (f'Week_{week}/W{week}_Weekly_Plan.docx', 'Weekly teaching plan'),
                (f'Week_{week}/W{week}_Weekly_Plan.pdf', 'Weekly teaching plan'),
                ('Teacher_Guide_And_Answers.docx', 'Teacher guidance and answers'),
                ('Teacher_Guide_And_Answers.pdf', 'Teacher guidance and answers')]:
                files.append(metadata(directory, relative, role))
            if code == 'W7L3':
                for extension in ('docx', 'pdf'):
                    files.append(metadata(directory, f'Week_7/LAUNCH_Science_Assessment.{extension}', 'Assessment'))
            lessons.append({'id': code, 'title': title, 'week': week, 'part': str(part),
                            'durationMinutes': 40, 'htmlUrl': 'https://madebymatt.uk/Lessons/' + repo_path,
                            'source': {'repo': 'MattRoper1977/Lessons', 'repoPath': repo_path,
                                       'gitBlob': subprocess.check_output(['git', 'hash-object', str(html_source)], text=True).strip(),
                                       'sha256': sha256(html_source.read_bytes()).hexdigest()},
                            'revision': REVISION, 'files': files})
    start = directory / 'START_HERE.txt'
    start.write_text('LAUNCH Science | Autumn 1 | Weeks 3-7\n\n15 editable 40-minute lessons.\n'
                     'Open Teacher_Guide_And_Answers.pdf first. The Word version is editable.\n'
                     'Keep each Week_n folder together when using PowerPoint worksheet links.\n'
                     'Whole, week and lesson ZIPs include companion resources. Format ZIPs contain only the selected file type.\n'
                     'The week 7 assessment and its mark scheme are separate from the short lesson practice.\n'
                     'Weeks 1-2 baseline and Week 8 enrichment are outside this pack.\n')
    manifest = {'schema': 'made-by-matt-teaching-pack-v1', 'title': 'LAUNCH Science',
                'subtitle': 'Autumn 1 - Weeks 3-7', 'revision': REVISION, 'lessonCount': 15,
                'durationMinutesPerLesson': 40, 'scope': {'included': '15 taught lessons, three per week.',
                'baseline': 'Weeks 1-2 baseline remains separate.', 'week8': 'Week 8 enrichment remains separate.'},
                'visualRefresh': 'Original editable pack content with refreshed visual design and printable resources.',
                'lessons': lessons, 'packFiles': [metadata(directory, p.name, 'Pack guidance')
                for p in sorted(directory.iterdir()) if p.is_file() and p.suffix in NATIVE]}
    save(directory / 'SOURCE_MANIFEST.json', manifest)


def rebuild_archives(pathway):
    directory = PACKS / pathway
    source = load(directory / 'SOURCE_MANIFEST.json')
    existing = directory / 'DOWNLOAD_INDEX.json'
    old = load(existing)['archives'] if existing.exists() else []
    lessons = source['lessons']
    specs = []
    if old:
        specs = [a for a in old if a.get('kind') != 'format']
    else:
        specs.append({'file': f'downloads/{pathway}_Science_Autumn1_W3-W7_Complete_Pack.zip',
                      'lessonIds': [x['id'] for x in lessons]})
        for week in range(3, 8):
            week_lessons = [x for x in lessons if x['week'] == week]
            specs.append({'file': f'downloads/{pathway}_Science_Autumn1_W{week}_Teaching_Pack.zip',
                          'lessonIds': [x['id'] for x in week_lessons]})
            for lesson in week_lessons:
                specs.append({'file': f'downloads/{pathway}_Science_Autumn1_{lesson["id"]}_Lesson_Pack.zip',
                              'lessonIds': [lesson['id']]})
    for extension in ('PPTX', 'DOCX', 'PDF'):
        specs.append({'file': f'downloads/{pathway}_Science_Autumn1_W3-W7_{extension}_Collection.zip',
                      'lessonIds': [x['id'] for x in lessons], 'kind': 'format', 'format': extension})
    archives = []
    all_files = {p.relative_to(directory).as_posix(): p for p in directory.rglob('*')
                 if p.is_file() and p.suffix in NATIVE and 'downloads' not in p.parts}
    for spec in specs:
        chosen = [x for x in lessons if x['id'] in spec['lessonIds']]
        kind = spec.get('kind') or ('whole' if len(chosen) == len(lessons) else 'lesson' if len(chosen) == 1 else 'week')
        wanted = {f['file'] for lesson in chosen for f in lesson['files']}
        wanted.update(f['file'] for f in source.get('packFiles', []))
        wanted.update(rel for rel in all_files if any(rel.startswith(f'lessons/{l["id"]}/') for l in chosen))
        if kind == 'whole':
            wanted.update(all_files)
        if kind == 'format':
            # Prefer the manifest's canonical downloads; legacy filename aliases
            # remain served but must not duplicate documents in format bundles.
            canonical = {f['file'] for lesson in chosen for f in lesson['files']}
            canonical.update(f['file'] for f in source.get('packFiles', []))
            wanted = {rel for rel in canonical if Path(rel).suffix[1:].upper() == spec['format']}
        output = directory / spec['file']
        output.parent.mkdir(exist_ok=True)
        # Keep legacy archive layouts as well as the public archive filenames.
        prefix = '' if pathway == 'BUILD' and kind != 'format' else (
            output.stem + '/' if pathway == 'GROW' and kind != 'format' else pathway + '_Science_Autumn1_W3-W7/')
        members = {prefix + (Path(rel).name if not prefix else rel): rel for rel in sorted(wanted)}
        if len(members) != len(wanted):
            raise ValueError('Archive member collision: ' + str(output))
        subset = deepcopy(source)
        subset['lessons'] = deepcopy(chosen)
        subset['lessonCount'] = len(chosen)
        if pathway == 'BUILD' and kind != 'format':
            for lesson in subset['lessons']:
                for item in lesson['files']:
                    item['file'] = Path(item['file']).name
        with zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
            for name, rel in members.items():
                info = zipfile.ZipInfo(name, (2026, 9, 6, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                archive.writestr(info, (directory / rel).read_bytes())
            if kind != 'format':
                info = zipfile.ZipInfo(prefix + 'SOURCE_MANIFEST.json', (2026, 9, 6, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                archive.writestr(info, json.dumps(subset, indent=2, ensure_ascii=False) + '\n')
                if pathway == 'BUILD' and (directory / 'SOURCE_MAPPING.json').is_file():
                    mapping = load(directory / 'SOURCE_MAPPING.json')
                    mapping['lessons'] = [l for l in mapping['lessons'] if any(l['id'] == c.get('artifactId') for c in chosen)]
                    mapping['taughtLessons'] = len(chosen)
                    mapping_info = zipfile.ZipInfo('SOURCE_MAPPING.json', (2026, 9, 6, 0, 0, 0))
                    mapping_info.compress_type = zipfile.ZIP_DEFLATED
                    archive.writestr(mapping_info, json.dumps(mapping, indent=2, ensure_ascii=False) + '\n')
        item = metadata(directory, spec['file'])
        item.update({'kind': kind, 'lessonIds': spec['lessonIds'], 'members': members})
        if kind == 'format':
            item['format'] = spec['format']
        archives.append(item)
    save(existing, {'revision': REVISION, 'archives': archives})


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--build', type=Path, required=True)
    parser.add_argument('--grow', type=Path, required=True)
    parser.add_argument('--launch-slides', type=Path, required=True)
    parser.add_argument('--launch-documents', type=Path, required=True)
    args = parser.parse_args()
    for value in vars(args).values():
        assert value.is_dir(), value
    copy_reviewed_existing('BUILD', args.build.resolve())
    copy_reviewed_existing('GROW', args.grow.resolve())
    create_launch(args.launch_slides.resolve(), args.launch_documents.resolve())
    for pathway in ('BUILD', 'GROW', 'LAUNCH'):
        rebuild_archives(pathway)
    from build_hub import build
    build()
