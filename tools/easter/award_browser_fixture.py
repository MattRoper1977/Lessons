"""Create a disposable browser-test fixture; never a curriculum deck or lesson unit."""
import json
import tempfile
from pathlib import Path
import author_deck as ad


def create():
    folder = Path(tempfile.mkdtemp(prefix='award-browser-'))
    donor = ad.ROOT / 'Art_Teesside/BUILD_W1-W8_2026-27/BUILD_Art_W3_Find_Out_About_An_Artist_Whose_Work.html'
    content = {
        'id': 'AWARD_BROWSER_FIXTURE', 'title': 'Browser test fixture',
        'objective': 'Test interface behaviour; this is not learner evidence.',
        'slot': 'TEST ONLY', 'tierLadder': ['Core', 'Extend', 'Challenge'],
        'stages': [{'title': f'Test stage {i + 1}', 'minutes': 0 if i == 0 else 5,
                    'type': 'title' if i == 0 else 'task', 'phase': 'SEE',
                    'data-ta1': f'Fixture staff note for stage {i + 1}.',
                    'data-ta2': 'Fixture second staff note.',
                    'blocks': [{'kind': 'p', 'text': f'Test content for stage {i + 1}.'},
                               {'kind': 'staff', 'text': 'Fixture overview guidance.'}]} for i in range(9)],
        'print': {'intro': 'Test sheet, not learner evidence.', 'focusRows': ['First test', 'Second test'],
                  'tiers': ['First support choice.', 'Second support choice.', 'Third support choice.'],
                  'checks': [f'Test check {n}.' for n in range(1, 6)],
                  'figures': ['<svg viewBox="0 0 200 40" role="img"><text x="5" y="20">First test figure</text></svg>',
                              '<svg viewBox="0 0 200 40" role="img"><text x="5" y="20">Second test figure</text></svg>']}}
    plan = {'family': 'BUILD Art', 'ruledWeek': 1, 'title': content['title'],
            'outcomes': [content['objective']], 'cells': [], 'subject': 'Art',
            'artsAward': {'level': 'Bronze', 'parts': ['B'], 'slots': ['EVENT_SLOT']}}
    output = folder / 'fixture.html'
    ad.author(donor, plan, content, output)
    (folder / 'fixture.json').write_text(json.dumps(content), encoding='utf-8')
    manifest = folder / 'targets.json'
    manifest.write_text(json.dumps({'batch': [{'planIndex': 1001, 'route': str(output),
        'spec': 'fixture.json', 'artsAward': plan['artsAward']}]}), encoding='utf-8')
    return manifest


if __name__ == '__main__':
    print(create())
