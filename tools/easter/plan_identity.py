"""Shared plan identity and canonical source reading; no authoring dependencies."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REGISTRY = ROOT / 'tools/easter/PLAN_SOURCES.json'


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def plan_id(plan: dict) -> str:
    # The exact algorithm shipped in #302. Workbook IDs remain unchanged.
    if plan.get('cells'):
        tail = '|'.join(sorted(plan['cells']))
    else:
        aa = plan.get('artsAward') or {}
        tail = '|'.join(['award', str(aa.get('level', '')),
                         ','.join(sorted(aa.get('parts', []))),
                         str(plan.get('title', ''))])
    key = '|'.join([str(plan.get('family', '')), str(plan.get('ruledWeek', '')), tail])
    return hashlib.sha256(key.encode('utf-8')).hexdigest()[:12]


def read_source(path: Path, kind: str):
    path = Path(path)
    if not path.is_file():
        raise ValueError(f'PROVENANCE REFUSAL: registered source absent: {path}')
    doc = json.loads(path.read_text(encoding='utf-8'))
    if kind == 'workbook':
        return doc['plans']
    if kind != 'award-rows':
        raise ValueError(f'Unknown plan source kind: {kind}')
    origin = doc['derivedFrom']
    source = ROOT / origin['path']
    if source.resolve() != (ROOT / 'tools/artsaward/SPEC.json').resolve():
        raise ValueError('PROVENANCE REFUSAL: award authority must be tools/artsaward/SPEC.json')
    if digest(source) != origin['sha256']:
        raise ValueError(f'PROVENANCE REFUSAL: {path.name} has stale source digest')
    level = origin['level']
    register = json.loads(source.read_text(encoding='utf-8'))
    ref = register['levels'][level]
    slots = json.loads((ROOT/'tools/artsaward/SLOTS.json').read_text(encoding='utf-8'))
    rows = doc['rows']
    if (not rows or len(rows) != doc['count'] or len({r['seq'] for r in rows}) != len(rows)
            or len({r['spec'] for r in rows}) != len(rows)):
        raise ValueError(f'PROVENANCE REFUSAL: count or sequence collision in {path}')
    plans = []
    for row in rows:
        if row['part'] not in ref['parts']:
            raise ValueError(f'Invalid {level} part in {path}: {row["part"]}')
        aa = {'level': level, 'parts': [row['part']]}
        needed = sorted(k for k,v in slots['slots'].items()
                        if row['part'] in v.get('serves',{}).get(level,[]))
        if needed:
            aa['slots'] = needed
        if row.get('listsPortfolio'):
            aa['listsPortfolio'] = True
        plans.append({'family': doc['family'], 'ruledWeek': row['week'],
                      'cells': [], 'title': row['title'],
                      'subject': doc.get('subjectName', 'Art'),
                      'outcomes': [row['outcome']], 'artsAward': aa})
    return plans


def index_plans(plans):
    result = {}
    for plan in plans:
        pid = plan_id(plan)
        if pid in result:
            raise ValueError(f'PROVENANCE REFUSAL: duplicate plan identity {pid}')
        result[pid] = plan
    return result


def load_registry(registry=REGISTRY):
    registry = Path(registry)
    doc = json.loads(registry.read_text(encoding='utf-8'))
    result, sources = {}, []
    for source in doc['sources']:
        path = ROOT / source['path']
        plans = read_source(path, source['kind'])
        source_index = index_plans(plans)
        overlap = set(result) & set(source_index)
        if overlap:
            raise ValueError(f'PROVENANCE REFUSAL: duplicate IDs across sources: {sorted(overlap)}')
        for pid,plan in source_index.items():
            result[pid] = {**plan, '_planSource': source['path']}
        sources.append({**source, 'sha256': digest(path), 'plans': len(plans)})
    dependencies = []
    if any(s['kind'] == 'award-rows' for s in sources):
        dependencies = [{'path': rel, 'sha256': digest(ROOT / rel)} for rel in
                        ['tools/artsaward/SPEC.json', 'tools/artsaward/SLOTS.json']]
    return result, {'registrySha256': digest(registry), 'sources': sources,
                    'dependencies': dependencies}


def validate_award_targets(doc):
    """Digest is necessary; every supplied row must also equal its source row."""
    source = ROOT / doc['derivedFrom']['path']
    if digest(source) != doc['derivedFrom']['sha256']:
        raise ValueError('PROVENANCE REFUSAL: target source digest is stale')
    source_doc = json.loads(source.read_text(encoding='utf-8'))
    plans = read_source(source, 'award-rows')
    by_spec = {r['spec']: p for r,p in zip(source_doc['rows'],plans)}
    if not doc['batch'] or len(doc['batch']) != doc['count']:
        raise ValueError('PROVENANCE REFUSAL: target count is empty or inconsistent')
    for key in ('planIndex', 'route'):
        if len({r[key] for r in doc['batch']}) != len(doc['batch']):
            raise ValueError(f'PROVENANCE REFUSAL: duplicate target {key}')
    seen = set()
    for row in doc['batch']:
        name = row['spec']
        if name in seen or name not in by_spec:
            raise ValueError(f'PROVENANCE REFUSAL: duplicate or unknown spec {name}')
        seen.add(name)
        expected = by_spec[name]
        actual = {'family': row['family'], 'ruledWeek': row['week'],
                  'cells': row.get('cells',[]), 'title': row['title'],
                  'subject': row['subject'], 'outcomes': row['outcomes'],
                  'artsAward': row['artsAward']}
        if actual != expected:
            raise ValueError(f'PROVENANCE REFUSAL: target {name} differs from its canonical plan')
    return by_spec
