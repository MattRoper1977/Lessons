"""Small offline classroom activities. Integration draft: no repository writes.

Normalise once, render screen/pupil print/staff key from that same object.
The uid is a required document-unique token supplied by the deck builder.
"""
from copy import deepcopy
from html import escape
import json
import re
import xml.etree.ElementTree as ET

MODES = {'sort', 'match', 'choice', 'order'}
TOKEN = re.compile(r'^[A-Za-z][A-Za-z0-9_-]*$')
SVG_NS = 'http://www.w3.org/2000/svg'
SVG_TAGS = {'svg', 'title', 'desc', 'g', 'rect', 'circle', 'ellipse', 'path',
            'line', 'polyline', 'polygon', 'text', 'tspan', 'defs',
            'linearGradient', 'radialGradient', 'stop', 'clipPath', 'pattern'}


def _text(value, field):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f'{field}: expected nonempty text')
    return value


def _id(value, field):
    if isinstance(value, bool) or not isinstance(value, (str, int)):
        raise ValueError(f'{field}: expected a text or integer ID')
    value = str(value)
    if not value or len(value) > 100:
        raise ValueError(f'{field}: invalid ID')
    return value


def _options(values, field):
    if not isinstance(values, list) or not 2 <= len(values) <= 20:
        raise ValueError(f'{field}: expected 2–20 choices')
    result = [{'id': _id(v['id'], field), 'label': _text(v['label'], field)}
              for v in values if isinstance(v, dict)]
    if len(result) != len(values) or len({v['id'] for v in result}) != len(values):
        raise ValueError(f'{field}: malformed or duplicate choices')
    return result


def normalize_activity(raw):
    """Accept both supplied draft shapes; never silently render an unknown mode."""
    if not isinstance(raw, dict) or raw.get('mode') not in MODES:
        raise ValueError('activity mode must be sort, match, choice or order')
    mode = raw['mode']
    rows = raw.get('items')
    if not isinstance(rows, list) or not 1 <= len(rows) <= 20:
        raise ValueError('activity items: expected 1–20 items')
    global_options = raw.get('categories', raw.get('options', raw.get('positions')))
    if mode == 'order' and global_options is None:
        raise ValueError('order activity needs explicit positions or options')
    out = {'mode': mode, 'heading': _text(raw.get('heading'), 'heading'),
           'instruction': _text(raw.get('instruction'), 'instruction'),
           'discussion': raw.get('discussion', raw.get('transfer', '')),
           'staffNote': raw.get('staffNote', ''), 'items': []}
    for optional in ('discussion', 'staffNote'):
        if not isinstance(out[optional], str):
            raise ValueError(f'{optional}: expected text')
    for i, row in enumerate(rows):
        if not isinstance(row, dict):
            raise ValueError(f'item {i}: expected object')
        if mode != 'choice' and 'options' in row:
            raise ValueError(f'item {i}: per-item options require choice mode')
        opts = _options(row.get('options', global_options), f'item {i} options')
        answer = _id(row.get('answer'), f'item {i} answer')
        if answer not in {v['id'] for v in opts}:
            raise ValueError(f'item {i}: answer is not one of its choices')
        out['items'].append({'id': _id(row.get('id', f'item-{i+1}'), f'item {i} id'),
                             'label': _text(row.get('label'), f'item {i} label'),
                             'answer': answer,
                             'feedback': _text(row.get('feedback'), f'item {i} feedback'),
                             'options': opts})
    if len({x['id'] for x in out['items']}) != len(out['items']):
        raise ValueError('item IDs must be unique')
    if mode == 'order':
        expected = {str(i + 1) for i in range(len(rows))}
        if ({x['answer'] for x in out['items']} != expected or
                any({v['id'] for v in x['options']} != expected for x in out['items'])):
            raise ValueError('order positions and answers must be a permutation of 1..item count')
    diagram = raw.get('diagram')
    if diagram is not None:
        if not isinstance(diagram, dict):
            raise ValueError('diagram must be an object')
        out['diagram'] = {k: _text(diagram.get(k), 'diagram.' + k)
                          for k in ('svg', 'alt', 'caption')}
        _svg(out['diagram'], 'validation-diagram')
    _check_legacy_print(raw, out)
    return out


def _check_legacy_print(raw, normalized):
    """Reject an existing screen/print mismatch instead of preserving it."""
    p = raw.get('print')
    if p is not None:
        if p.get('heading') != normalized['heading'] or p.get('instruction') != normalized['instruction']:
            raise ValueError('print heading/instruction disagrees with screen')
        if p.get('taskRows') != [i['label'] for i in normalized['items']]:
            raise ValueError('print rows disagree with screen')
        choices = normalized['items'][0]['options']
        if p.get('choices') != [c['label'] for c in choices]:
            raise ValueError('print choices disagree with screen')
        keys = p.get('staffOnly', {}).get('answerKey', [])
        expected = [{'label': row['label'], 'answer': next(o['label'] for o in row['options'] if o['id'] == row['answer']), 'feedback': row['feedback']} for row in normalized['items']]
        if keys != expected:
            raise ValueError('print staff key disagrees with screen')
    p = raw.get('printFallback')
    if p is not None:
        for field in ('heading', 'instruction', 'discussion'):
            if p.get(field, '') != normalized[field]:
                raise ValueError(f'print fallback {field} disagrees with screen')
        if len(p.get('items', [])) != len(normalized['items']):
            raise ValueError('print fallback item count disagrees with screen')
        for old, row in zip(p['items'], normalized['items']):
            if old.get('label') != row['label'] or _id(old.get('id'), 'print item ID') != row['id']:
                raise ValueError('print fallback item disagrees with screen')
            if 'options' in old and _options(old['options'], 'print options') != row['options']:
                raise ValueError('print fallback choices disagree with screen')
        keys = p.get('staffOnlyAnswerKey', [])
        expected = [{'id': x['id'], 'answer': x['answer'], 'feedback': x['feedback']} for x in normalized['items']]
        observed = [dict(x, answer=_id(x.get('answer'), 'print answer')) for x in keys]
        if observed != expected:
            raise ValueError('print fallback staff key disagrees with screen')
        for field in ('categories', 'positions'):
            if field in p and _options(p[field], 'print ' + field) != normalized['items'][0]['options']:
                raise ValueError('print fallback choices disagree with screen')
        if p.get('diagram') != raw.get('diagram'):
            raise ValueError('print fallback diagram disagrees with screen')


def _uid(uid):
    if not isinstance(uid, str) or not TOKEN.fullmatch(uid):
        raise ValueError('uid: supply a document-unique letter-led token')
    return uid


def _svg(diagram, uid):
    source = diagram['svg']
    if '<!' in source or '<?' in source:
        raise ValueError('SVG declarations and processing instructions are not supported')
    try:
        root = ET.fromstring(source)
    except ET.ParseError as exc:
        raise ValueError('invalid SVG') from exc
    if root.tag.split('}')[-1] != 'svg' or 'viewBox' not in root.attrib:
        raise ValueError('diagram needs an SVG root and viewBox')
    ids = {}
    for node in root.iter():
        if node.tag.split('}')[-1] not in SVG_TAGS:
            raise ValueError('unsupported SVG element')
        if 'id' in node.attrib:
            old = node.attrib['id']
            if old in ids or not TOKEN.fullmatch(old):
                raise ValueError('SVG IDs must be unique safe tokens')
            ids[old] = uid + '-' + old
        for key, value in node.attrib.items():
            local = key.split('}')[-1].lower()
            if local.startswith('on') or local in ('href', 'style') or 'javascript:' in value.lower():
                raise ValueError('SVG events, links and inline styles are not supported')
            if 'url(' in value and not re.fullmatch(r'url\(#[A-Za-z][A-Za-z0-9_-]*\)', value):
                raise ValueError('SVG external resources are not supported')
    for node in root.iter():
        for key, value in list(node.attrib.items()):
            if key == 'id':
                node.set(key, ids[value])
            elif key in ('aria-labelledby', 'aria-describedby'):
                if any(part not in ids for part in value.split()):
                    raise ValueError('SVG accessible reference does not exist')
                node.set(key, ' '.join(ids[part] for part in value.split()))
            elif value.startswith('url(#'):
                ref = value[5:-1]
                if ref not in ids:
                    raise ValueError('SVG local resource does not exist')
                node.set(key, f'url(#{ids[ref]})')
    root.set('role', 'img')
    if 'aria-labelledby' not in root.attrib:
        root.set('aria-label', diagram['alt'])
    ET.register_namespace('', SVG_NS)
    return ET.tostring(root, encoding='unicode')


def _figure(data, uid):
    if 'diagram' not in data:
        return ''
    d = data['diagram']
    return '<figure class="mbm-act-figure">' + _svg(d, uid) + '<figcaption>' + escape(d['caption']) + '</figcaption></figure>'


def render_activity(data, uid):
    """Screen markup for a normalized activity; escaped text, no inline events."""
    uid = _uid(uid)
    e = escape
    bits = [f'<section class="mbm-activity" data-mbm-activity="{e(uid)}" aria-labelledby="{uid}-heading" data-mode="{data["mode"]}">',
            f'<h3 id="{uid}-heading">{e(data["heading"])}</h3>',
            f'<p id="{uid}-instruction">{e(data["instruction"])}</p>',
            _figure(data, uid + '-screen'),
            '<div class="mbm-act-items">']
    for i, row in enumerate(data['items']):
        rid = uid + '-row-' + str(i + 1)
        bits.append(f'<div class="mbm-act-row" data-activity-row="{i}">')
        if data['mode'] == 'choice':
            bits.append(f'<fieldset aria-describedby="{uid}-instruction {rid}-feedback"><legend>{e(row["label"])}</legend>')
            for oi, opt in enumerate(row['options']):
                oid = rid + '-option-' + str(oi + 1)
                bits.append(f'<label class="mbm-act-choice" for="{oid}"><input id="{oid}" type="radio" name="{rid}" value="{e(opt["id"], quote=True)}"> <span>{e(opt["label"])}</span></label>')
            bits.append('</fieldset>')
        else:
            bits.append(f'<label for="{rid}-select">{e(row["label"])}</label><select id="{rid}-select" aria-describedby="{rid}-feedback"><option value="">Choose…</option>')
            for opt in row['options']:
                bits.append(f'<option value="{e(opt["id"], quote=True)}">{e(opt["label"])}</option>')
            bits.append('</select>')
        bits.append(f'<p class="mbm-act-row-feedback" id="{rid}-feedback"></p></div>')
    bits += ['</div><div class="mbm-act-actions">',
             '<button type="button" data-activity-action="check">Check choices</button>',
             '<button type="button" data-activity-action="retry">Retry</button>',
             f'<button type="button" data-activity-action="explain" aria-expanded="false" aria-controls="{uid}-explanations">Show explanations</button>',
             '</div>',
             f'<p class="mbm-act-status" role="status" aria-live="polite" aria-atomic="true"></p>',
             f'<div id="{uid}-explanations" class="mbm-act-explanations" hidden><h4>Model explanations</h4><ol>']
    for row in data['items']:
        answer_label = next(o['label'] for o in row['options'] if o['id'] == row['answer'])
        bits.append(f'<li><b>{e(row["label"])}</b> — {e(answer_label)}. {e(row["feedback"])}</li>')
    bits.append('</ol><p>This model supports discussion. A well-explained different connection can be useful too.</p></div>')
    if data['discussion']:
        bits.append('<p class="mbm-act-discussion">' + e(data['discussion']) + '</p>')
    payload = {'mode': data['mode'], 'items': [{'answer': r['answer']} for r in data['items']]}
    safe_json = json.dumps(payload, ensure_ascii=False, separators=(',', ':')).replace('<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026').replace('\u2028', '\\u2028').replace('\u2029', '\\u2029')
    bits.append('<script type="application/json" data-activity-data>' + safe_json + '</script></section>')
    return ''.join(bits)


def render_pupil_print(data, uid):
    """Append AFTER author_print_pack, inside .print-pack, not inside a slide."""
    uid = _uid(uid) + '-print'
    e = escape
    bits = [f'<section class="mbm-activity-print" data-activity-print="{uid}" aria-labelledby="{uid}-heading">',
            f'<h3 id="{uid}-heading">{e(data["heading"])}</h3><p>{e(data["instruction"])}</p>', _figure(data, uid), '<ol>']
    for row in data['items']:
        bits.append('<li><p class="mbm-print-task">' + e(row['label']) + '</p>')
        bits.append('<p class="mbm-print-options">' + ' · '.join(e(o['label']) for o in row['options']) + '</p>')
        bits.append('<p class="mbm-print-response">My choice / reason: <span>____________________________</span></p></li>')
    bits.append('</ol>')
    if data['discussion']:
        bits.append('<p>' + e(data['discussion']) + '</p>')
    bits.append('</section>')
    return ''.join(bits)


def render_staff_key(data, uid):
    """Existing award_chassis.js copies this data-mbm-guide into Teacher tools."""
    _uid(uid)
    e = escape
    bits = ['<div class="box rehearsal mbm-activity-staff" data-mbm-guide="staff">',
            '<h4>Activity model: ' + e(data['heading']) + '</h4><ol>']
    for row in data['items']:
        label = next(o['label'] for o in row['options'] if o['id'] == row['answer'])
        bits.append('<li><b>' + e(row['label']) + '</b> — ' + e(label) + '. ' + e(row['feedback']) + '</li>')
    bits.append('</ol><p>This classroom check is not an award grade or proof of completed pupil evidence.</p>')
    if data['staffNote']:
        bits.append('<p>' + e(data['staffNote']) + '</p>')
    return ''.join(bits) + '</div>'


def render_bundle(raw, uid):
    data = normalize_activity(raw)
    return {'screen': render_activity(data, uid), 'pupilPrint': render_pupil_print(data, uid),
            'staff': render_staff_key(data, uid)}
