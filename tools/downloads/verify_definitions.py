#!/usr/bin/env python3
"""Verify current source placement and exact lesson selection for each ZIP."""
import hashlib
import json
from pathlib import Path
import re
import sys
from urllib.parse import quote

from lxml import html
from build_download_pack import lesson_label

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[1]
sys.path.insert(0, str(ROOT/'_sownb/vb/tools'))
import cell_coverage


def verify():
    placement = json.loads((BASE/'SOURCE_PLACEMENT.json').read_text())
    cells, listing, claims, _ = cell_coverage.load()
    actual_science = {p for p in listing if p.startswith('Science_Teesside/') and cell_coverage.is_lesson(p,(ROOT/p).read_text())}
    recorded_main = {r['path'] for r in placement['sources']}
    alternatives = placement['retainedAlternatives']
    if len(alternatives)!=len(set(alternatives)) or recorded_main.intersection(alternatives) or actual_science != recorded_main.union(alternatives):
        raise ValueError('Science route census changed; review new routes for the explicit main/alternative selection')
    rows = []
    by_path = {}
    calendar = (ROOT/'_sownb/TERM_DATES.md').read_text()
    for row in placement['sources']:
        path = ROOT/row['path']
        raw = path.read_bytes()
        tree = html.fromstring(raw)
        slides = tree.xpath('//*[contains(concat(" ",normalize-space(@class)," ")," slide ")]')
        if not slides:
            raise ValueError('No current teaching title stage: '+row['path'])
        title_stage = ' '.join(slides[0].text_content().split())
        e = row['classificationEvidence'][0]
        method = e['method']
        if method.startswith('workbook cell'):
            refs = row['cellReferences']
            if not refs or not all(ref in cells and ref in claims[row['path']] for ref in refs):
                raise ValueError('Current source trace no longer supports placement: '+row['path'])
            term_weeks = sorted({cells[ref]['termWeek'] for ref in refs})
            if term_weeks != sorted(row['termWeeks']):
                raise ValueError('Current workbook term differs: '+row['path'])
            weeks = [cell_coverage.ruled_week(cells[ref]) for ref in refs]
            if not all(isinstance(w,int) and w <= 26 for w in weeks):
                raise ValueError('Source is outside the ruled timetable boundary')
        elif method == 'own current title-slide SoW declaration':
            if not all(tw in title_stage for tw in row['termWeeks']):
                raise ValueError('Own title-stage SoW changed: '+row['path'])
        elif method == 'own explicit enrichment label combined with ruled school calendar':
            if e['quote'] not in title_stage or 'Absolute week 8 is the enrichment week' not in calendar:
                raise ValueError('Explicit enrichment declaration changed')
        elif method == 'own manifest sequence week plus explicit pack curriculum-calendar declaration':
            manifest = json.loads((ROOT/e['source']).read_text())
            matched = [r for r in manifest['sequence'] if r['id']==e['manifestId'] and (Path(e['source']).parent/r['file']).as_posix()==row['path']]
            if len(matched)!=1 or matched[0]['week'] != e['declaredWeek']:
                raise ValueError('Explicit current manifest row changed')
            alignment = ' '.join((ROOT/e['alignmentSource']).read_text().split())
            if e['quote'] not in alignment or 'Absolute week 8 is the enrichment week' not in calendar:
                raise ValueError('Explicit enrichment calendar alignment changed')
        else:
            raise ValueError('Unreviewed source placement method: '+method)
        if {tw.split('·')[0] for tw in row['termWeeks']} != {row['term']}:
            raise ValueError('Source terms do not fit the pack')
        if row['path'] in by_path:
            raise ValueError('Duplicate source identity')
        by_path[row['path']] = row
        rows.append({'file':row['path'],'sha256':hashlib.sha256(raw).hexdigest(),
                     'pathway':row['pathway'],'term':row['term'],'termWeeks':row['termWeeks'],
                     'method':method,'currentSourcePlacement':'PASS'})
    selected = []
    award = []
    for path in sorted((BASE/'definitions').glob('*.json')):
        definition = json.loads(path.read_text())
        lessons = definition['lessons']
        if len(lessons)!=len(set(lessons)) or not all(p in definition['files'] for p in lessons):
            raise ValueError('Lesson selection is not unique and explicit')
        if definition.get('subject') == 'Science':
            expected = {r['path'] for r in placement['sources'] if r['term']==definition['term'] and r['pathway']==definition['pathway']}
            if set(lessons) != expected:
                raise ValueError('Science term/pathway selection changed: '+definition['id'])
            selected += lessons
            for target, continuation in definition.get('continuations', {}).items():
                if target not in by_path or by_path[target]['term']==definition['term'] or by_path[target]['pathway']!=definition['pathway']:
                    raise ValueError('Continuation is not the stated other-term lesson')
                if continuation['onlineUrl'] != 'https://madebymatt.uk/Lessons/'+quote(target,safe='/') or continuation['title'] != lesson_label((ROOT/target).read_bytes()):
                    raise ValueError('Continuation destination or title differs from the actual lesson')
        elif definition.get('subject') == 'Arts Award':
            target_file = ROOT/definition['awardTargets']
            expected = [r['route'] for r in json.loads(target_file.read_text())['batch']]
            if lessons != expected or len(lessons)!=14:
                raise ValueError('Award order/lesson identities differ')
            award += lessons
        else:
            raise ValueError('Definition needs explicit subject metadata')
        for member in definition['files']:
            if not (ROOT/member).is_file():
                raise ValueError('Missing selected source: '+member)
    if set(selected)!=set(by_path) or len(selected)!=len(by_path):
        raise ValueError('Main Science selection was lost or duplicated')
    if len(award)!=len(set(award)):
        raise ValueError('Award lesson selected more than once')
    return {'schema':'download-current-source-review-v1','files':rows,'scienceLessons':len(selected),
            'awardLessons':len(award),'newCoverageCells':0,'note':'Placement and selection only; not a certificate of curriculum completion.'}


if __name__=='__main__':
    print(json.dumps(verify(),indent=2))
