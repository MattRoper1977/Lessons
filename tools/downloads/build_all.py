#!/usr/bin/env python3
"""Build the explicit downloadable packs from a stable checkout; do not publish."""
import argparse
import json
from pathlib import Path
import tempfile

from build_download_pack import build, digest
from build_science_offline_pack import build_offline

ROOT = Path(__file__).resolve().parents[2]
BASE = Path(__file__).resolve().parent


def build_all(output: Path):
    output = output.resolve()
    if output.is_relative_to(ROOT):
        raise ValueError('Review builds must be outside the source checkout')
    output.mkdir(parents=True, exist_ok=True)
    hud = BASE/'vendor/hud.js'
    pin = json.loads((BASE/'vendor/HUD_SOURCE.json').read_text())
    if digest(hud.read_bytes()) != pin['sha256']:
        raise ValueError('Reviewed HUD source pin differs')
    reports = []
    for path in sorted((BASE/'definitions').glob('*.json')):
        definition = json.loads(path.read_text())
        if path.stem != definition['id']:
            raise ValueError('Definition filename and id disagree')
        archive = output/(definition['id']+'.zip')
        report = build_offline(ROOT, definition, hud, pin['sha256'], archive)
        if report['status'] != 'BUILT':
            raise ValueError(json.dumps(report))
        missing = [r for r in report['navigation'] if r.get('resolution') == 'outside-explicit-pack-not-crawled']
        if missing:
            raise ValueError('Unresolved navigation in the release pack: '+json.dumps(missing))
        with tempfile.TemporaryDirectory(prefix='lesson-pack-repeat-') as temp:
            repeated = build_offline(ROOT, definition, hud, pin['sha256'], Path(temp)/'repeat.zip')
            if repeated.get('zipSha256') != report['zipSha256']:
                raise ValueError('Rebuilding the same inputs changed the archive')
        report['deterministicRebuild'] = True
        report['sourceDefinition'] = {'file':str(path.relative_to(ROOT)), 'sha256':digest(path.read_bytes())}
        (output/(definition['id']+'-report.json')).write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
        reports.append({'id':definition['id'],'archive':archive.name,'sha256':report['zipSha256'],'bytes':report['zipBytes'],
                        'members':report['memberCount'],'deterministicRebuild':True,
                        'outsidePackNavigation':[r for r in report['navigation'] if r.get('resolution')=='outside-explicit-pack-not-crawled'],
                        'offlineAdaptations':report.get('offlineAdaptation',{}).get('sourceFilesChanged',0)})
        print(definition['id'],report['zipBytes'],'bytes',flush=True)
    (output/'build_summary.json').write_text(json.dumps({'packs':reports,'count':len(reports),'status':'PACKAGING_ONLY_BROWSER_REVIEW_REQUIRED'},indent=2)+'\n')
    return reports


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    build_all(args.output)
