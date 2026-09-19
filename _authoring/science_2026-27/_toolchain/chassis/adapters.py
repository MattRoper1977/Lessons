"""SX3-2 — dialect adapters: read a built pack deck, hand back normalised content.

ORDER SX3-2 ruling: the generator-edit plan is withdrawn. Three dialects were measured across
the 79 incoming decks and each needs its own reader:

    A  sugar format, slide ids a0..b5, carries script#lesson-data   39 decks (BUILD 18, GROW 21)
    B  slide ids s0..sN                                             23 decks (LAUNCH)
    C  slides carry no id, and there is no #print-area at all       17 decks (BUILD 2, LAUNCH 15)

Each adapter returns the same shape, so the transplant into the pathway exemplar is one code
path. Nothing here writes prose: every string comes out of the pack.
"""
from __future__ import annotations

import json
import re

from lxml import etree
from lxml import html as LH

ROUTES = ('supported', 'standard', 'stretch')


def inner_html(node) -> str:
    """Serialise a node's children, not the node itself."""
    if node is None:
        return ''
    parts = [node.text or '']
    parts += [etree.tostring(c, encoding='unicode', method='html') for c in node]
    return ''.join(parts)


def text_of(node) -> str:
    return re.sub(r'\s+', ' ', (node.text_content() if node is not None else '')).strip()


ROUTE_RE = '(?:supported|standard|stretch)'


def detect(doc) -> str:
    """Classify by the CONTENT SHAPE each dialect actually uses, never by #lesson-data.

    R-READERS (ORDER SX3-2): #lesson-data is present in every dialect, so keying on it
    silently defaulted 40 decks to A and left the exemplar's own lesson in place. A deck this
    cannot classify is HELD, never defaulted.
    """
    ids = [e.get('id') for e in doc.xpath('//*[@id]')]
    if any(i and re.fullmatch(r'answer-arrival-[AB]-%s-\d+' % ROUTE_RE, i) for i in ids):
        return 'A'
    if any(i and re.fullmatch(r'answer-arrival-%s-\d+' % ROUTE_RE, i) for i in ids):
        return 'B'
    if any(i and re.fullmatch(r'arrival-%s-\d+' % ROUTE_RE, i) for i in ids):
        return 'C'
    if any(i and re.fullmatch(r'arrival-\d+-\d+', i) for i in ids) and doc.xpath('//*[@data-stage]'):
        return 'D'
    return 'unknown'


# --------------------------------------------------------------------------- dialect A

def read_a(doc) -> dict:
    data = {}
    node = doc.xpath('//script[@id="lesson-data"]')
    if node:
        data = json.loads(node[0].text)
    teaching = data.get('teaching', {})
    stages_raw = data.get('stages') or []
    stage_meta = {s['id']: s for s in stages_raw if isinstance(s, dict) and 'id' in s}

    slides = []
    for section in doc.xpath('//*[contains(concat(" ",normalize-space(@class)," ")," slide ")]'):
        key = section.get('id') or ''
        meta = stage_meta.get(key, {})
        heading = section.xpath('.//h1|.//h2')
        slides.append({
            'key': key,
            'title': meta.get('title') or text_of(heading[0] if heading else None),
            'timer': str(meta.get('minutes', section.get('data-minutes') or '')),
            'type': meta.get('type', section.get('data-type') or ''),
            'teacher': teaching.get(key, meta.get('note', '')),
            'html': inner_html(section),
        })

    source_ids = {}

    def dialog(identifier, key=None):
        found = doc.xpath('//dialog[@id=$i]', i=identifier)
        if not found:
            return ''
        # ORDER SX3-GO2b row 40: every reader records which pack dialog supplied each region,
        # so the transplant can forward that dialog's open/close to the exemplar dialog that
        # ends up holding it. Reader D already did; A, B and C did not, which is why two
        # decks kept a control reaching for a #staff-dialog that no longer existed.
        if key:
            source_ids[key] = identifier
        inner = found[0].xpath('.//*[contains(concat(" ",normalize-space(@class)," ")," dialog-inner ")]')
        body = inner[0] if inner else found[0]
        clone = LH.fromstring('<div>' + inner_html(body) + '</div>')
        for head in clone.xpath('.//*[contains(concat(" ",normalize-space(@class)," ")," dialog-head ")]'):
            head.getparent().remove(head)
        return inner_html(clone)

    arrivals, exits = {}, {}
    for panel in doc.xpath('//*[@data-route-panel]'):
        route = panel.get('data-route-panel')
        label = (panel.get('aria-label') or '').lower()
        if route not in ROUTES:
            continue
        kind = 'arrival' if 'arrival' in label else ('exit' if 'exit' in label else None)
        if kind is None:
            continue
        bucket = arrivals if kind == 'arrival' else exits
        if route in bucket:
            continue
        cells = []
        for card in panel.xpath('.//article[contains(concat(" ",normalize-space(@class)," ")," question-card ")]'):
            head = card.xpath('./h3')
            paras = card.xpath('./p')
            helps = card.xpath('./p[contains(concat(" ",normalize-space(@class)," ")," question-help ")]')
            answer = card.xpath('.//details[@data-answer]//p')
            cells.append({
                'title': inner_html(head[0]) if head else '',
                'question': inner_html(paras[0]) if paras else '',
                'help': inner_html(helps[0]) if helps else '',
                'answer': inner_html(answer[0]) if answer else '',
            })
        if cells:
            bucket[route] = cells

    return {
        'dialect': 'A',
        'arrivals': arrivals,
        'exits': exits,
        'title': data.get('title', ''),
        'pathway': data.get('pathway', ''),
        'slides': slides,
        'pages': data.get('pages', {}),
        'words': dialog('words-dialog', 'words'),
        'staff': dialog('staff-dialog', 'staff'),
        'organiser': dialog('organiser-dialog', 'organiser'),
        'tools': dialog('tools-dialog', 'tools'),
        'config': {k: data.get(k) for k in ('title', 'key', 'prefix', 'pathway', 'stages') if k in data},
        'lesson_data': data,
        'dialog_source_ids': source_ids,
        'lesson_js': '\n'.join((s.text or '') for s in doc.xpath('//script[not(@src) and not(@id)]')),
        'lesson_css': '\n'.join((s.text or '') for s in doc.xpath('//style')),
    }


def _cards_from(doc, pattern):
    """B: arrival/exit cells are question-cards holding details#answer-<kind>-<route>-<n>."""
    out = {}
    for node in doc.xpath('//details[@id]'):
        match = re.fullmatch(pattern, node.get('id') or '')
        if not match:
            continue
        route = match.group(1)
        card = node.getparent()
        head = card.xpath('./h3')
        paras = card.xpath('./p')
        helps = card.xpath('./p[contains(concat(" ",normalize-space(@class)," ")," question-help ")]')
        answer = node.xpath('./p')
        out.setdefault(route, []).append({
            'title': inner_html(head[0]) if head else '',
            'question': inner_html(paras[0]) if paras else '',
            'help': inner_html(helps[0]) if helps else '',
            'answer': inner_html(answer[0]) if answer else '',
        })
    return out


def read_b(doc) -> dict:
    out = read_a(doc)
    out['arrivals'] = _cards_from(doc, r'answer-arrival-(%s)-(\d+)' % ROUTE_RE)
    out['exits'] = _cards_from(doc, r'answer-exit-(%s)-(\d+)' % ROUTE_RE)
    return out


def _c_route(items, route):
    """C stores one item list; the three routes are its supported / plain / stretch faces."""
    cells = []
    for index, item in enumerate(items or [], 1):
        if route == 'stretch':
            question, answer = item.get('x') or item.get('q', ''), item.get('xa') or item.get('a', '')
        elif route == 'supported':
            question = ' '.join(x for x in (item.get('q', ''), item.get('s', '')) if x)
            answer = item.get('a', '')
        else:
            question, answer = item.get('q', ''), item.get('a', '')
        cells.append({'title': '%d.' % index, 'question': question,
                      'help': item.get('h', ''), 'answer': answer})
    return cells


def read_c(doc) -> dict:
    node = doc.xpath('//script[@id="lesson-data"]')
    data = json.loads(node[0].text) if node else {}
    slides = []
    names = data.get('stageNames') or []
    for index, section in enumerate(doc.xpath('//*[contains(concat(" ",normalize-space(@class)," ")," slide ")]')):
        heading = section.xpath('.//h1|.//h2')
        slides.append({
            'key': 'stage-%d' % index,
            'title': (names[index] if index < len(names) else '') or text_of(heading[0] if heading else None),
            'timer': str(data.get('minutes', '')),
            'type': '',
            'teacher': '',
            'html': inner_html(section),
        })

    source_ids = {}

    def dialog(identifier, key=None):
        found = doc.xpath('//dialog[@id=$i]', i=identifier)
        if not found:
            return ''
        if key:
            source_ids[key] = identifier
        return inner_html(found[0])

    vocab = data.get('vocab') or {}
    words = ''
    if vocab:
        words = '<dl>' + ''.join('<dt>%s</dt><dd>%s</dd>' % (k, v) for k, v in vocab.items()) + '</dl>'

    return {
        'dialect': 'C',
        'title': data.get('title', ''),
        'pathway': data.get('pathway', ''),
        'slides': slides,
        'pages': data.get('prints') or {},
        'arrivals': {r: _c_route(data.get('arrival'), r) for r in ROUTES},
        'exits': {r: _c_route(data.get('exit'), r) for r in ROUTES},
        'words': words or dialog('words-dialog', 'words'),
        'staff': dialog('staff-dialog', 'staff'),
        'organiser': dialog('organiser-dialog', 'organiser'),
        'tools': dialog('tools-dialog', 'tools'),
        'config': {k: data.get(k) for k in ('id', 'title', 'pathway', 'week', 'objective') if k in data},
        'lesson_data': data,
        'dialog_source_ids': source_ids,
        'lesson_js': '\n'.join((s.text or '') for s in doc.xpath('//script[not(@src) and not(@id)]')),
        'lesson_css': '\n'.join((s.text or '') for s in doc.xpath('//style')),
    }


def _d_route(items, index):
    """D stores one item list; q/a/h are three-element arrays, one entry per route."""
    cells = []
    for number, item in enumerate(items or [], 1):
        def pick(key):
            value = item.get(key)
            if isinstance(value, list):
                return value[index] if index < len(value) else (value[-1] if value else '')
            return value or ''
        cells.append({'title': '%d.' % number, 'question': pick('q'),
                      'help': pick('h'), 'answer': pick('a')})
    return cells


def read_d(doc) -> dict:
    node = doc.xpath('//script[@id="lesson-data"]')
    data = json.loads(node[0].text) if node else {}
    stage_names = data.get('stages') or []
    minutes = data.get('minutes') or []
    slides = []
    for index, section in enumerate(doc.xpath('//*[@data-stage]')):
        heading = section.xpath('.//h1|.//h2')
        name = stage_names[index] if index < len(stage_names) else ''
        if isinstance(name, dict):
            name = name.get('title') or name.get('tag') or ''
        slides.append({
            'key': section.get('id') or ('stage-%d' % index),
            'title': name or text_of(heading[0] if heading else None),
            'timer': str(minutes[index]) if index < len(minutes) and not isinstance(minutes, dict) else '',
            'type': '',
            'teacher': '',
            'html': inner_html(section),
        })

    source_ids = {}

    def dialog(key, *names):
        for identifier in names:
            found = doc.xpath('//dialog[@id=$i]', i=identifier)
            if found:
                source_ids[key] = identifier
                return inner_html(found[0])
        return ''

    vocab = data.get('vocab') or {}
    words = ('<dl>' + ''.join('<dt>%s</dt><dd>%s</dd>' % (k, v) for k, v in vocab.items()) + '</dl>') if vocab else ''
    return {
        'dialect': 'D',
        'title': data.get('title', ''),
        'pathway': 'LAUNCH',
        'slides': slides,
        'pages': {},
        'arrivals': {route: _d_route(data.get('arrival'), i) for i, route in enumerate(ROUTES)},
        'exits': {route: _d_route(data.get('exits'), i) for i, route in enumerate(ROUTES)},
        'words': words or dialog('words', 'dialog-words', 'words-dialog'),
        'staff': dialog('staff', 'dialog-staff', 'staff-dialog'),
        'organiser': dialog('organiser', 'dialog-ko', 'organiser-dialog'),
        'tools': dialog('tools', 'dialog-tools', 'tools-dialog'),
        'config': {k: data.get(k) for k in ('id', 'title', 'week', 'lesson', 'objective') if k in data},
        'lesson_data': data,
        'dialog_source_ids': source_ids,
        'dialog_source_ids': source_ids,
        'lesson_js': '\n'.join((s.text or '') for s in doc.xpath('//script[not(@src) and not(@id)]')),
        'lesson_css': '\n'.join((s.text or '') for s in doc.xpath('//style')),
    }


READERS = {'A': read_a, 'B': read_b, 'C': read_c, 'D': read_d}


def class_tags(doc) -> dict:
    """tag name the PACK used for each class, so a shimmed .frame or .chart keeps its element."""
    out = {}
    for element in doc.xpath('//*[@class]'):
        for name in (element.get('class') or '').split():
            out.setdefault(name, element.tag)
    return out


def id_tags(doc) -> dict:
    """tag name the PACK used for each id, so a shimmed #particles stays a <canvas>."""
    return {e.get('id'): e.tag for e in doc.xpath('//*[@id]') if e.get('id')}


def read(path) -> dict:
    doc = LH.fromstring(open(path, 'rb').read())
    kind = detect(doc)
    reader = READERS.get(kind)
    if reader is None:
        raise NotImplementedError('dialect %s reader not written yet: %s' % (kind, path))
    out = reader(doc)
    out['dialect'] = kind
    out['class_tags'] = class_tags(doc)
    out['id_tags'] = id_tags(doc)
    return out
