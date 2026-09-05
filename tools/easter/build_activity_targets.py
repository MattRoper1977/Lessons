#!/usr/bin/env python3
"""Derive the browser oracle from authored specs, separately from page markup."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def build(targets, content_dir):
    manifest = json.loads(targets.read_text())
    result = []
    inputs = [{'file': str(targets.relative_to(ROOT)),
               'sha256': hashlib.sha256(targets.read_bytes()).hexdigest()}]
    for row in manifest['batch']:
        source = content_dir / row['spec']
        spec = json.loads(source.read_text())
        activities = [(si, bi, block['data'])
                      for si, stage in enumerate(spec['stages'])
                      for bi, block in enumerate(stage['blocks'])
                      if block['kind'] == 'activity']
        if len(activities) != 1:
            raise ValueError(f'{source}: expected one primary activity, found {len(activities)}')
        si, bi, activity = activities[0]
        result.append({'file': row['route'], 'spec': str(source.relative_to(ROOT)),
                       'activityId': f'{spec["id"]}-stage{si}-{bi + 1}',
                       'activitySchema': activity, 'stageIndex': si})
        inputs.append({'file': str(source.relative_to(ROOT)),
                       'sha256': hashlib.sha256(source.read_bytes()).hexdigest()})
    if len({row['file'] for row in result}) != len(result):
        raise ValueError('Duplicate activity route')
    return {'schema': 'classroom-activity-browser-targets-v1',
            'kind': 'authored-decks', 'inputs': inputs, 'targets': result}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--targets', type=Path, required=True)
    parser.add_argument('--content-dir', type=Path, default=ROOT/'tools/artsaward/content')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = build(args.targets.resolve(), args.content_dir.resolve())
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps({'targets': len(result['targets']), 'output': str(args.output)}))
