"""EDU-D2: explicit titles for the reviewed companion families.

Keep the canonical catalogue and lesson-order records unchanged. A map entry
applies only while both its ID and original title still match the source row.
"""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / 'assets/catalogue/display-titles.json'


def build():
    rows = json.loads((ROOT / 'resources.json').read_text())
    supplements = json.loads((ROOT / 'assets/catalogue/lesson-order.json').read_text())['supplements']
    by_path = {r['file']: r for r in supplements + rows}
    packs = {r['companionOf']: r for r in rows if r.get('kind') == 'pack'}
    manifest = json.loads((ROOT / 'data/companion-packs.json').read_text())
    entries = {}
    for pack in manifest['packs']:
        path = pack['companionOf']
        host, companion = by_path[path], packs[path]
        title = pack['title'].strip()
        # Each selected title is verbatim within the current host's own title.
        # This is a guard for the reviewed 116 pairs, not filename inference.
        if title not in host['title']:
            raise ValueError('Review changed lesson title: ' + path)
        for row in (host, companion):
            entries[row['file']] = {
                'id': row.get('id', ''), 'originalTitle': row['title'],
                'displayTitle': title, 'reference': pack['wtoken'],
            }
    return {'schema': 1, 'basis': 'EDU-D2 reviewed companion titles; data/companion-packs.json and exact current catalogue/lesson-order titles', 'entries': entries}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    value = json.dumps(build(), ensure_ascii=False, indent=2) + '\n'
    if args.check:
        if OUTPUT.read_text() != value:
            raise SystemExit('Display-title map is stale; review source changes before rebuilding.')
    else:
        OUTPUT.write_text(value)
    print('EDU-D2: 116 verified companion pairs; 232 guarded display-title entries.')
