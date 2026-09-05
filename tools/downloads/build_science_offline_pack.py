#!/usr/bin/env python3
"""Explicit offline-only HUD adaptation. Never edits either source repository."""
import argparse
import json
from pathlib import Path
import posixpath
import re
import tempfile

from build_download_pack import build, digest, lesson_label, portal

SCRIPT = re.compile(r'<script\b[^>]*>.*?</script\s*>', re.I | re.S)
HUD_SRC = re.compile(r'\bsrc\s*=\s*([\"\'])/hud\.js\1', re.I)
GROW_ID = re.compile(r'\bid\s*=\s*([\"\'])grow-hud-loader\1', re.I)
EXPECTED_GROW_CALL = 'add("/hud.js",function(){add("hud.js");});'


def adapt_html(data: bytes, member: str, expected: int):
    """Only the reviewed Site-HUD tag or exact GROW loader is adapted."""
    text = data.decode('utf-8')
    hud_path = posixpath.relpath('hud.js', posixpath.dirname(member))
    adapter_path = posixpath.relpath('offline-hud-navigation.js', posixpath.dirname(member))
    changed = []
    def replace(match):
        block = match.group(0)
        tag = block.split('>', 1)[0]
        if HUD_SRC.search(tag):
            if re.search(r'\basync\b', tag, re.I):
                raise ValueError('Asynchronous HUD tag needs a separate reviewed adaptation')
            changed.append('absolute-script-src-to-relative-bundled-hud')
        elif GROW_ID.search(tag):
            if EXPECTED_GROW_CALL not in block or 'function add(src,onfail)' not in block:
                raise ValueError('GROW HUD loader changed; refuse an unreviewed replacement')
            changed.append('reviewed-grow-loader-to-ordered-bundled-hud')
        else:
            return block
        # Ordered deferred scripts preserve all HUD teaching functions and let
        # the offline navigation adapter run after the real HUD has mounted.
        return f'<script defer src="{hud_path}"></script><script defer src="{adapter_path}"></script>'
    after = SCRIPT.sub(replace, text)
    if len(changed) != expected:
        raise ValueError(f'HUD adaptation count differs from parsed dependencies: {member}: {len(changed)} != {expected}')
    return after.encode(), changed


def build_offline(repo: Path, definition: dict, site_hud: Path, expected_hud_sha: str, output: Path | None = None):
    source_report = build(repo, definition)
    reviewed_grow_fallbacks = {e['target'] for e in source_report['dependencies'] if
        e.get('kind') == 'grow-hud-loader' and e.get('url') == 'hud.js' and e.get('scope') == 'local'}
    allowed_errors = [e for e in source_report['errors'] if
        (e.get('target') == '/hud.js' and e.get('scope') == 'site-root') or
        (e.get('reason') == 'missing local dependency' and e.get('file') in reviewed_grow_fallbacks)]
    if len(allowed_errors) != len(source_report['errors']):
        return {'status':'REFUSED','reason':'Unreviewed runtime dependency','sourceReport':source_report}
    needs_hud = any(e.get('target') == '/hud.js' for e in allowed_errors)
    if not needs_hud:
        # Already self-contained lessons need no wrapper or rewritten bytes.
        report = build(repo, definition, output)
        report['offlineAdaptation'] = {'required':False,'sourceFilesChanged':0}
        return report
    raw_hud = site_hud.read_bytes()
    if digest(raw_hud) != expected_hud_sha:
        raise ValueError('Site hud.js bytes differ from the explicitly reviewed hash')
    adapter = Path(__file__).with_name('offline-hud-navigation.js').read_bytes()
    changes = []
    with tempfile.TemporaryDirectory(prefix='lesson-offline-stage-') as temp:
        stage = Path(temp)
        for row in source_report['sources']:
            path = row['path']
            data = (repo / path).read_bytes()
            if digest(data) != row['sha256']:
                raise ValueError('Lesson changed during packaging; rerun against a stable source')
            target = stage / 'Lessons' / path
            target.parent.mkdir(parents=True, exist_ok=True)
            relevant = [e for e in source_report['dependencies'] if e['from'] == path and e.get('target') == '/hud.js']
            transformed, kinds = adapt_html(data, 'Lessons/' + path, len(relevant)) if path.endswith('.html') else (data, [])
            target.write_bytes(transformed)
            changes.append({'source':path,'member':'Lessons/'+path,'sourceSha256':digest(data),'packagedSha256':digest(transformed),'adaptations':kinds})
        (stage / 'hud.js').write_bytes(raw_hud)
        (stage / 'offline-hud-navigation.js').write_bytes(adapter)
        lesson_entries = ['Lessons/'+p for p in definition['files'] if p.endswith('.html')]
        labels = {p: lesson_label((stage / p).read_bytes()) for p in lesson_entries}
        (stage / 'Lessons/index.html').write_bytes(portal(definition['title'], lesson_entries, 'Lessons/index.html', labels))
        adaptation = {'schema':'science-offline-hud-adaptation-v1','required':True,
            'sourceFilesChanged':sum(bool(c['adaptations']) for c in changes),
            'sourceFiles':changes,'siteHud':{'source':'Site/hud.js','sha256':digest(raw_hud),'bytes':len(raw_hud),'packagedByteExact':True},
            'adapterSha256':digest(adapter),'reason':'Preserve the Live-Teach timer, name picker, mic meter, calm reset and announcements in extracted files.',
            'layout':'Lessons/ preserves the exact Site HUD lesson-path predicate; all original relative paths remain beneath that wrapper.',
            'navigation':'HUD Back opens the local pack home. A previously chosen Site homepage keeps its original destination as a labelled online link.',
            'acceptance':'Static packaging and focused adapter controls only; full offline browser acceptance still required.'}
        (stage / 'OFFLINE_ADAPTATION.json').write_text(json.dumps(adaptation,indent=2,sort_keys=True)+'\n')
        adapted = dict(definition)
        adapted['continuations'] = {'Lessons/'+p:r for p,r in definition.get('continuations',{}).items()}
        adapted['entry'] = 'Lessons/index.html'
        adapted['files'] = ['Lessons/'+p for p in definition['files']] + ['Lessons/index.html','hud.js','offline-hud-navigation.js','OFFLINE_ADAPTATION.json']
        report = build(stage, adapted, output)
        report['offlineAdaptation'] = adaptation
        report['originalDefinition'] = definition
        return report


if __name__ == '__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--repo',type=Path,required=True)
    p.add_argument('--definition',type=Path,required=True)
    p.add_argument('--site-hud',type=Path,required=True)
    p.add_argument('--site-hud-sha256',required=True)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--report',type=Path,required=True)
    a=p.parse_args()
    try:
        if a.output.resolve().is_relative_to(a.repo.resolve()) or a.report.resolve().is_relative_to(a.repo.resolve()):
            raise ValueError('Output/report must be outside the source checkout')
        report=build_offline(a.repo,json.loads(a.definition.read_text()),a.site_hud,a.site_hud_sha256,a.output)
    except (ValueError,OSError) as exc:
        report={'status':'REFUSED','errors':[{'reason':str(exc)}]}
    a.report.parent.mkdir(parents=True,exist_ok=True)
    a.report.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    print(json.dumps({k:report[k] for k in ['id','status','memberCount','zipBytes','zipSha256','errors'] if k in report}))
    raise SystemExit(0 if report['status']=='BUILT' else 1)
