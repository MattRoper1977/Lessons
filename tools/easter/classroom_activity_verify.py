"""DOM/source checks only. This does not claim a browser interaction test."""
from copy import deepcopy
import json
from pathlib import Path
import subprocess
from lxml import html as lh

from classroom_activity import normalize_activity, render_bundle

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
DRAFTS = ROOT / 'tools/artsaward/content'
files = sorted(DRAFTS.glob('BRONZE_*.json'))
checks = []


def check(name, condition):
    checks.append({'id': name, 'passed': bool(condition)})
    assert condition, name


def rejects(name, data):
    try:
        normalize_activity(data)
    except (ValueError, KeyError, TypeError) as e:
        checks.append({'id': name, 'passed': True, 'caught': str(e)})
    else:
        raise AssertionError(name + ': planted defect did not fire')


check('fourteen-real-source-drafts', len(files) == 14)
screen_chunks, print_chunks, staff_chunks, raw_rows = [], [], [], []
for n, path in enumerate(files):
    spec = json.loads(path.read_text())
    activities = [b['data'] for st in spec['stages'] for b in st['blocks'] if b['kind'] == 'activity']
    check(path.stem + '-one-primary-authored-activity', len(activities) == 1)
    raw = activities[0]
    raw_rows.append(raw)
    normalized = normalize_activity(raw)
    bundle = render_bundle(raw, 'lesson-activity-' + str(n))
    s, p, t = (lh.fromstring(bundle[k]) for k in ('screen', 'pupilPrint', 'staff'))
    rendered_labels = s.xpath('.//div[@data-activity-row]/label/text() | .//fieldset/legend/text()')
    print_labels = p.xpath('.//p[@class="mbm-print-task"]/text()')
    check(path.stem + '-same-screen-and-print-questions', rendered_labels == print_labels == [x['label'] for x in normalized['items']])
    row_nodes = s.xpath('.//div[@data-activity-row]')
    choices = []
    for row in row_nodes:
        if normalized['mode'] == 'choice':
            choices.append(row.xpath('.//label/span/text()'))
        else:
            choices.append(row.xpath('.//option[@value!=""]/text()'))
    expected_options = [[o['label'] for o in r['options']] for r in normalized['items']]
    check(path.stem + '-same-screen-and-print-options', choices == expected_options and p.xpath('.//p[@class="mbm-print-options"]/text()') == [' · '.join(r) for r in expected_options])
    label_ids = set(s.xpath('.//label/@for'))
    input_ids = set(s.xpath('.//input/@id | .//select/@id'))
    check(path.stem + '-all-controls-labelled', input_ids <= label_ids and len(input_ids) > 0)
    check(path.stem + '-pupil-print-has-no-feedback-or-key', not p.xpath('.//script | .//*[@data-mbm-guide] | .//*[@class="mbm-act-explanations"]') and not any(r['feedback'] in p.text_content() for r in normalized['items']))
    check(path.stem + '-staff-key-has-all-model-reasons', t.get('data-mbm-guide') == 'staff' and all(r['feedback'] in t.text_content() for r in normalized['items']))
    explain = s.xpath('.//button[@data-activity-action="explain"]')[0]
    target = s.xpath('.//*[@id=$id]', id=explain.get('aria-controls'))[0]
    check(path.stem + '-explanations-hidden-before-request', target.get('hidden') is not None and explain.get('aria-expanded') == 'false')
    check(path.stem + '-polite-status-and-no-submit', bool(s.xpath('.//*[@role="status"][@aria-live="polite"][@aria-atomic="true"]')) and all(x.get('type') == 'button' for x in s.xpath('.//button')))
    screen_chunks.append(bundle['screen'])
    print_chunks.append(bundle['pupilPrint'])
    staff_chunks.append(bundle['staff'])

combined = lh.fromstring('<main>' + ''.join(screen_chunks + print_chunks + staff_chunks) + '</main>')
ids = combined.xpath('.//*[@id]/@id')
check('fourteen-screen-and-print-views-have-unique-ids', len(ids) == len(set(ids)))
for attribute in ('aria-labelledby', 'aria-describedby', 'aria-controls'):
    refs = [word for value in combined.xpath('.//@' + attribute) for word in value.split()]
    check('all-' + attribute + '-targets-exist', set(refs) <= set(ids))

bad = deepcopy(raw_rows[0]); bad['mode'] = 'drag'; rejects('unknown-mode-is-rejected', bad)
bad = deepcopy(raw_rows[0]); bad['items'][0]['answer'] = 'absent'; rejects('missing-answer-option-is-rejected', bad)
bad = deepcopy(raw_rows[0]); bad['items'][0]['id'] = 'same'; bad['items'][1]['id'] = 'same'; rejects('duplicate-item-id-is-rejected', bad)
bad = deepcopy(raw_rows[0]); bad['categories'][1]['id'] = bad['categories'][0]['id']; rejects('duplicate-choice-id-is-rejected', bad)
order = next(r for r in raw_rows if r['mode'] == 'order')
bad = deepcopy(order); bad['items'][1]['answer'] = bad['items'][0]['answer']; rejects('duplicate-order-answer-is-rejected', bad)
valid_print = deepcopy(raw_rows[0])
n = normalize_activity(valid_print)
valid_print['print'] = {'heading': n['heading'], 'instruction': n['instruction'], 'taskRows': [i['label'] for i in n['items']], 'choices': [o['label'] for o in n['items'][0]['options']], 'staffOnly': {'answerKey': [{'label': i['label'], 'answer': next(o['label'] for o in i['options'] if o['id'] == i['answer']), 'feedback': i['feedback']} for i in n['items']]}}
normalize_activity(valid_print)
bad = deepcopy(valid_print); bad['print']['taskRows'][0] = 'Changed only on paper'; rejects('divergent-print-task-is-rejected', bad)
bad = deepcopy(valid_print); bad['print']['staffOnly']['answerKey'][0]['feedback'] = 'Different reason'; rejects('divergent-print-key-is-rejected', bad)
late_choice = next(r for r in raw_rows if r['mode'] == 'choice' and 'options' in r['items'][0])
valid_fallback = deepcopy(late_choice)
n = normalize_activity(valid_fallback)
valid_fallback['printFallback'] = {'heading': n['heading'], 'instruction': n['instruction'], 'discussion': n['discussion'], 'items': deepcopy(n['items']), 'staffOnlyAnswerKey': [{'id': i['id'], 'answer': i['answer'], 'feedback': i['feedback']} for i in n['items']]}
normalize_activity(valid_fallback)
bad = deepcopy(valid_fallback); bad['printFallback']['items'][0]['options'][0]['label'] = 'Wrong print choice'; rejects('divergent-late-choice-is-rejected', bad)

for name, svg in [
    ('script', '<svg viewBox="0 0 1 1"><script>bad()</script></svg>'),
    ('event', '<svg viewBox="0 0 1 1" onload="bad()"/>'),
    ('external-link', '<svg viewBox="0 0 1 1"><path href="https://invalid.example/"/></svg>'),
    ('external-fill', '<svg viewBox="0 0 1 1"><path fill="url(https://invalid.example/)"/></svg>'),
    ('duplicate-svg-id', '<svg viewBox="0 0 1 1"><path id="a"/><path id="a"/></svg>'),
    ('missing-svg-label-target', '<svg viewBox="0 0 1 1" aria-labelledby="missing"/>')
]:
    bad = deepcopy(raw_rows[0]); bad['diagram'] = {'svg': svg, 'alt': 'Test', 'caption': 'Test'}
    rejects('unsafe-' + name + '-rejected', bad)

hostile = deepcopy(raw_rows[0])
hostile.pop('print', None)
hostile['items'][0]['label'] = '<img src=x onerror=alert(1)>'
hostile['items'][0]['feedback'] = '</script><script>alert(2)</script>'
html = lh.fromstring(render_bundle(hostile, 'escaped-text')['screen'])
check('labels-and-feedback-are-text-not-executable-html', not html.xpath('.//img') and len(html.xpath('.//script')) == 1 and '<img src=x onerror=alert(1)>' in html.text_content())

js = (HERE / 'classroom_activity.js').read_text()
css = (HERE / 'classroom_activity.css').read_text()
check('runtime-does-not-create-storage-network-or-focus-loop', not any(x in js for x in ('localStorage', 'sessionStorage', 'fetch(', 'XMLHttpRequest', 'setInterval', 'setTimeout', 'keydown', 'focusin')))
check('runtime-has-all-three-actions-and-boot-guard', all(x in js for x in ("action === 'check'", "action === 'retry'", "action === 'explain'", 'if (root.dataset.activityReady) return;')))
check('print-css-hides-screen-and-staff-key', '@media print{' in css and '.mbm-activity,.mbm-activity-staff,#award-teacher-notes .mbm-activity-staff{display:none!important}' in css)
result = subprocess.run(['node', '--check', str(HERE / 'classroom_activity.js')], capture_output=True, text=True)
check('runtime-javascript-parses', result.returncode == 0)

report = {'schema': 'activity-renderer-dom-source-controls-v1', 'scope': 'DOM structure, source constraints, schema rejection and JavaScript syntax; browser and print pagination are tested separately.', 'sourceSpecs': [{'file': str(p.relative_to(ROOT))} for p in files], 'count': len(checks), 'passed': sum(x['passed'] for x in checks), 'checks': checks}
print(json.dumps(report, indent=2))
