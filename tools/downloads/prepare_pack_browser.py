#!/usr/bin/env python3
"""Validate/extract the twelve explicit release ZIPs for file:// browser tests."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import shutil
import zipfile


PACKS = [
    (f'{lane}-science-{term}-main', 'science', lane.upper(), term)
    for lane in ['build','grow','launch'] for term in ['aut1','aut2','spr1']
] + [(f'{level}-arts-award-main','award','GROW' if level=='silver' else 'BUILD',level)
     for level in ['bronze','explore','silver']]


def validate_archive(archive):
    names=archive.namelist()
    if len(names)!=len(set(names)) or len(names)!=len(set(n.casefold() for n in names)):
        raise ValueError('Duplicate or case-colliding ZIP members')
    for item in archive.infolist():
        p=PurePosixPath(item.filename)
        if p.is_absolute() or '\\' in item.filename or any(s in {'.','..'} or s.startswith(('_','.')) for s in p.parts):
            raise ValueError('ZIP member escapes public extraction scope: '+item.filename)
        if (item.external_attr >> 16) & 0o170000 == 0o120000:
            raise ValueError('Symlink ZIP member refused')
        if p.suffix.lower() in {'.xlsx','.xls','.xlsm'}:
            raise ValueError('Workbook is not teaching-pack content')
    return names


def prepare(definitions, archives, extracted, manifest):
    definitions=definitions.resolve();archives=archives.resolve();extracted=extracted.resolve()
    extracted.mkdir(parents=True,exist_ok=True)
    result={'schema':'lesson-offline-browser-manifest-v1','packs':[],
            'scope':'All 12 pack entry surfaces and required lesson files; 15 interactive representatives. No claim that every lesson interaction or curriculum outcome is tested.'}
    for ident,kind,lane,term in PACKS:
        definition=json.loads((definitions/(ident+'.json')).read_text())
        if definition['id']!=ident:
            raise ValueError('Definition id mismatch')
        lessons=definition.get('lessons')
        if not lessons or len(lessons)!=len(set(lessons)):
            raise ValueError('Non-empty unique lesson identities are required')
        if not all(p in definition['files'] and p.endswith('.html') for p in lessons):
            raise ValueError('Every declared lesson must be an explicit HTML member')
        if kind=='award' and len(lessons)!=14:
            raise ValueError('Each AAE definition must contain exactly 14 lessons')
        source=archives/(ident+'.zip')
        destination=extracted/ident
        if destination.exists():
            # Refuse stale content rather than making a deleted ZIP member look present.
            raise ValueError('Extraction destination already exists; supply a fresh directory: '+str(destination))
        with zipfile.ZipFile(source) as z:
            names=validate_archive(z)
            if 'START_HERE.html' not in names or 'PACK.json' not in names:
                raise ValueError('Pack has no generated launch/manifest files')
            prefix='Lessons/' if 'Lessons/'+lessons[0] in names else ''
            members=[prefix+p for p in lessons]
            missing=[m for m in members if m not in names]
            if missing:raise ValueError('Missing required lesson files: '+repr(missing))
            # Every source member recorded in the ZIP must agree with its bytes.
            metadata=json.loads(z.read('PACK.json'))
            for row in metadata['sources']:
                if row['path'] not in names or hashlib.sha256(z.read(row['path'])).hexdigest()!=row['sha256']:
                    raise ValueError('PACK.json source hash mismatch: '+row['path'])
            later=None
            if kind=='award':
                for m in members[1:]:
                    text=z.read(m).decode()
                    config=re.search(r'<script\b[^>]*\bid=["\']lesson-config["\'][^>]*>(.*?)</script>',text,re.S)
                    if config and json.loads(config.group(1)).get('artsAward',{}).get('slots'):
                        later=m;break
                if not later:raise ValueError('Award pack must supply a later slot-reader representative')
                if 'tools/artsaward/SLOTS.json' not in names:raise ValueError('Missing offline slot register')
            destination.mkdir()
            z.extractall(destination)
            result['packs'].append({'id':ident,'root':ident,'kind':kind,'pathway':lane,'term':term,
                'archive':source.name,'zipSha256':hashlib.sha256(source.read_bytes()).hexdigest(),
                'title':definition['title'],'entry':'START_HERE.html',
                'packStart':prefix+definition['entry'],'lessons':members,'firstLesson':members[0],
                'laterSample':later,'expectHud':prefix=='Lessons/' and term=='aut1',
                'memberCount':len(names),'declaredLessonCount':len(members),'validatedSourceHashes':len(metadata['sources'])})
    result['packCount']=len(result['packs'])
    result['packagedLessonFiles']=sum(p['declaredLessonCount'] for p in result['packs'])
    result['interactiveRepresentativeCount']=sum(1+bool(p['laterSample']) for p in result['packs'])
    manifest.parent.mkdir(parents=True,exist_ok=True)
    manifest.write_text(json.dumps(result,indent=2)+'\n')
    return result


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--definitions',type=Path,required=True)
    p.add_argument('--archives-dir',type=Path,required=True)
    p.add_argument('--extracted-dir',type=Path,required=True)
    p.add_argument('--manifest',type=Path,required=True)
    a=p.parse_args()
    result=prepare(a.definitions,a.archives_dir,a.extracted_dir,a.manifest)
    print(json.dumps({k:result[k] for k in ['packCount','packagedLessonFiles','interactiveRepresentativeCount']}))
