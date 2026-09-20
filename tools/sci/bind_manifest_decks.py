#!/usr/bin/env python3
"""ORDER SCI-COMPLETE PASS A3 — bind the selected Spring and Summer decks to their weeks.

build_science_shelf.py refuses a shelf route with no entry in
tools/catalogue/SCIENCE_WEEK_BINDINGS.json, so a route selected for the shelf needs
a binding, and the binding must be DERIVED under the record's own rule:

    Calendar binding uses explicit current content/manifest/SoW evidence. No week
    inferred from filename or folder. termWeek resolved from workbook cells
    outranks obsolete cell.absoluteWeek and CALENDAR_SPINE.calendar blocks.

So, per selected route without an entry:

  * the manifest row's workbook cells are resolved in _sownb/CALENDAR_SPINE.json,
    and the spine's termWeek is the binding. Every cell must resolve or the route
    is refused.
  * the ruled absolute week is term base + week within term, the bases read from
    the record's own calendarNotes line ("Ruled absolute offsets: ..."), never
    typed here. Where the manifest also states absoluteWeek, the two must agree
    or the route is refused. ORDER SCI-COMPLETE §Q4: the science bases are also
    written to tools/catalogue/TERM_BASES.json for the other subject to read.
  * a workbook week the calendar does not timetable (the record's own note:
    "Spring2 has five timetabled weeks; workbook Spr2·W6 is not timetabled") is
    bound to its term and week and marked timetabled: false, with no ruled
    absolute week. It is listed, not hidden.
  * a route whose cells resolve to more than one week keeps every week and is
    listed as a two-week deck; the record holds no precedent for one.

The evidence written is the shape the record already holds for a manifest-bound
route (method "current manifest lesson row with resolved workbook cells"), so a
reader sees nothing new. Style and title come from the rebuilt evidence record and
the deck's own <title>. Nothing here edits a lesson.

  bind_manifest_decks.py [--write]
  bind_manifest_decks.py --self-test
"""
from __future__ import annotations
import argparse, hashlib, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BINDINGS = ROOT / 'tools/catalogue/SCIENCE_WEEK_BINDINGS.json'
SELECTION = ROOT / 'tools/catalogue/SHELF_SELECTION.json'
SPINE = ROOT / '_sownb/CALENDAR_SPINE.json'
EVIDENCE = ROOT / 'tools/catalogue/TERM_AND_STYLE_EVIDENCE.json'
TERM_BASES = ROOT / 'tools/catalogue/TERM_BASES.json'
METHOD = 'current manifest lesson row with resolved workbook cells'
SOW_METHOD = 'current manifest lesson row sow declaration'
TOKEN = re.compile(r'\b(Aut|Spr|Sum)([12])·W(\d+)\b')
TERM_LABEL = {'Aut1': 'Autumn 1', 'Aut2': 'Autumn 2', 'Spr1': 'Spring 1',
              'Spr2': 'Spring 2', 'Sum1': 'Summer 1', 'Sum2': 'Summer 2'}


class Refuse(Exception):
    pass


def ruled_bases(notes):
    """Parse 'Ruled absolute offsets: Aut1 +0, Aut2 +8, ...' from the record's own notes."""
    for n in notes:
        if n.startswith('Ruled absolute offsets:'):
            return {t: int(v) for t, v in re.findall(r'(Aut1|Aut2|Spr1|Spr2|Sum1|Sum2)\s*\+(\d+)', n)}
    raise Refuse('the record carries no "Ruled absolute offsets" note; bases cannot be derived')


def untimetabled(notes):
    """Workbook weeks the record's notes say the calendar does not timetable."""
    out = set()
    for n in notes:
        for key in re.findall(r'workbook\s+((?:Aut|Spr|Sum)[12]·W\d+)\s+is not timetabled', n):
            out.add(key)
    return out


def weeks_for(refs, cells, bases, not_timetabled, manifest_abs, sow=None):
    """Pure: the weeks list for one route, or a Refuse.

    With `sow`, the route is the builder's sow-declaration fallback: the week is the
    token the manifest row itself writes, and every cell that DOES resolve must
    agree with it. A token that no resolving cell corroborates is refused."""
    keys = []
    if sow is not None:
        toks = ['%s%s·W%s' % m for m in TOKEN.findall(sow)]
        if not toks:
            raise Refuse('sow declaration carries no term·week token')
        resolved = {cells[r]['termWeek'] for r in refs if r in cells}
        if not resolved:
            raise Refuse('no cited cell resolves to corroborate the sow token')
        if not resolved <= set(toks):
            raise Refuse('resolving cells %s disagree with the sow token %s' % (sorted(resolved), toks))
        keys = list(dict.fromkeys(toks))
    for r in ([] if sow is not None else refs):
        if r not in cells:
            raise Refuse('cell not in the calendar spine: ' + r)
        tw = cells[r]['termWeek']
        if tw not in keys:
            keys.append(tw)
    weeks = []
    for key in keys:
        term, w = key.split('·W')
        n = int(w)
        entry = {'key': key, 'term': term, 'weekWithinTerm': n, 'label': TERM_LABEL[term] + ' · Week ' + str(n)}
        if key in not_timetabled:
            entry['timetabled'] = False
        else:
            entry['ruledAbsoluteWeek'] = bases[term] + n
            if manifest_abs is not None and len(keys) == 1 and manifest_abs != entry['ruledAbsoluteWeek']:
                raise Refuse('manifest absoluteWeek %s disagrees with the ruled week %s for %s'
                             % (manifest_abs, entry['ruledAbsoluteWeek'], key))
        weeks.append(entry)
    return weeks


def derive():
    rec = json.loads(BINDINGS.read_text())
    bases = ruled_bases(rec['calendarNotes']); nt = untimetabled(rec['calendarNotes'])
    cells = {c['reference']: c for c in json.loads(SPINE.read_text())['workbookCells']}
    ev = json.loads(EVIDENCE.read_text())['entries']
    sel = json.loads(SELECTION.read_text())['science']
    new, refused, listed = {}, [], []
    for row in sel:
        rel = row['path']
        if rel in rec['entries']:
            continue
        evid = next((e for e in row.get('classificationEvidence', []) if e.get('method') in (METHOD, SOW_METHOD)), None)
        if not evid:
            refused.append((rel, 'selected without manifest evidence')); continue
        mf = ROOT / evid['source']
        item = next((i for i in json.loads(mf.read_text()).get('lessons', []) if i.get('file') == evid['file']), None)
        if not item:
            refused.append((rel, 'manifest row vanished: ' + evid['source'])); continue
        by_sow = evid['method'] == SOW_METHOD
        refs = [c.get('reference', '') if isinstance(c, dict) else c for c in item.get('cells', [])] if by_sow else evid['refs']
        try:
            weeks = weeks_for(refs, cells, bases, nt, item.get('absoluteWeek'), sow=item.get('sow') if by_sow else None)
        except Refuse as x:
            refused.append((rel, str(x))); continue
        e = ev.get(rel, {})
        p = ROOT / rel
        title = re.search(r'<title>(.*?)</title>', p.read_text(errors='replace'), re.S)
        new[rel] = {
            'pathway': e.get('pathway'), 'style': e.get('style'),
            'title': re.sub(r'\s+', ' ', title.group(1)).strip() if title else rel,
            'weeks': weeks,
            'sourceSha256': hashlib.sha256(p.read_bytes()).hexdigest(),
            'sourceProofUnchanged': True,
            'evidence': [({'method': SOW_METHOD, 'source': evid['source'], 'file': evid['file'], 'quote': item['sow'],
                           'corroboratingCells': [{'reference': r, 'termWeek': cells[r]['termWeek']} for r in refs if r in cells],
                           'unresolvedCells': [r for r in refs if r not in cells],
                           'proof': 'manifest row sow token, corroborated by every cited cell the spine resolves'}
                          if by_sow else
                          {'method': METHOD, 'source': evid['source'],
                           'references': [{'reference': r, 'termWeek': cells[r]['termWeek'],
                                           'workbook': cells[r].get('workbook'),
                                           'outcome': cells[r].get('verbatimOutcome')} for r in refs],
                           'proof': 'current recorded curriculum binding'})],
            'status': 'verified', 'reason': None,
            'bound': {'by': 'tools/sci/bind_manifest_decks.py', 'basis': 'manifest row cells resolved in the calendar spine; ruled offsets from this record\'s calendarNotes'}}
        if any(w.get('timetabled') is False for w in weeks):
            listed.append((rel, 'workbook week not timetabled: ' + ', '.join(w['key'] for w in weeks)))
        if by_sow:
            listed.append((rel, 'bound by the manifest sow token; unresolved cell(s): ' + ', '.join(r for r in refs if r not in cells)))
        if len(weeks) > 1:
            listed.append((rel, 'two-week deck, no precedent in the record: ' + ', '.join(w['key'] for w in weeks)))
    return rec, bases, new, refused, listed


def self_test():
    bad = 0
    def check(name, cond):
        nonlocal bad
        print('  [%s] %s' % ('ok' if cond else 'FAIL', name)); bad += 0 if cond else 1
    notes = ['Ruled absolute offsets: Aut1 +0, Aut2 +8, Spr1 +15, Spr2 +21, Sum1 +26, Sum2 +33.',
             'Spring2 has five timetabled weeks; workbook Spr2·W6 is not timetabled.']
    bases = ruled_bases(notes); nt = untimetabled(notes)
    check('bases are read from the record, Aut2 = 8 + n', bases['Aut2'] == 8 and bases['Sum2'] == 33)
    cells = {'A': {'termWeek': 'Spr1·W3'}, 'B': {'termWeek': 'Spr1·W4'}, 'S': {'termWeek': 'Spr2·W6'}}
    w = weeks_for(['A'], cells, bases, nt, 18)
    check('a resolved cell binds to the spine week with the ruled absolute week', w[0]['key'] == 'Spr1·W3' and w[0]['ruledAbsoluteWeek'] == 18)
    try:
        weeks_for(['A'], cells, bases, nt, 19); check('a manifest absoluteWeek that disagrees is refused', False)
    except Refuse as x:
        check('a manifest absoluteWeek that disagrees is refused', 'disagrees' in str(x))
    try:
        weeks_for(['Z'], cells, bases, nt, None); check('a cell outside the spine is refused', False)
    except Refuse as x:
        check('a cell outside the spine is refused', 'not in the calendar spine' in str(x))
    w = weeks_for(['S'], cells, bases, nt, None)
    check('an untimetabled workbook week is bound, marked, and given no absolute week',
          w[0]['timetabled'] is False and 'ruledAbsoluteWeek' not in w[0])
    w = weeks_for(['A', 'B'], cells, bases, nt, 18)
    check('a two-week deck keeps both weeks', [x['key'] for x in w] == ['Spr1·W3', 'Spr1·W4'])
    w = weeks_for(['A', 'Q'], cells, bases, nt, 18, sow='Spr1·W3 — x')
    check('a sow token corroborated by the resolving cell binds; the unresolved cell does not block',
          w[0]['key'] == 'Spr1·W3' and w[0]['ruledAbsoluteWeek'] == 18)
    try:
        weeks_for(['B', 'Q'], cells, bases, nt, 19, sow='Spr1·W3 — x'); check('a sow token the resolving cell contradicts is refused', False)
    except Refuse as x:
        check('a sow token the resolving cell contradicts is refused', 'disagree' in str(x))
    try:
        weeks_for(['Q'], cells, bases, nt, None, sow='Spr1·W3 — x'); check('a sow token with no corroborating cell is refused', False)
    except Refuse as x:
        check('a sow token with no corroborating cell is refused', 'corroborate' in str(x))
    try:
        ruled_bases(['nothing here']); check('missing offsets note is refused, never defaulted', False)
    except Refuse:
        check('missing offsets note is refused, never defaulted', True)
    print('self-test ' + ('PASS' if not bad else 'FAIL (%d)' % bad))
    return 1 if bad else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--write', action='store_true'); ap.add_argument('--self-test', action='store_true')
    a = ap.parse_args()
    if a.self_test:
        return self_test()
    try:
        rec, bases, new, refused, listed = derive()
    except Refuse as x:
        print('[FAIL] ' + str(x)); return 1
    print('SEARCH SCOPE: %d selected route(s), %d already bound, %d to bind, %d refused'
          % (len(json.loads(SELECTION.read_text())['science']), len(rec['entries']), len(new), len(refused)))
    for rel, why in refused: print('  REFUSED %s: %s' % (rel, why))
    for rel, why in listed: print('  LISTED  %s: %s' % (rel.split('/')[-1], why))
    import collections
    print('  by term: %s' % dict(collections.Counter(w['term'] for e in new.values() for w in e['weeks'][:1])))
    if refused:
        print('[FAIL] refusals; nothing written'); return 1
    if a.write and new:
        rec['entries'].update(new)
        rec.setdefault('bindingRuns', []).append({'by': 'tools/sci/bind_manifest_decks.py', 'bound': len(new),
                                                  'listed': [r for r, _ in listed]})
        BINDINGS.write_text(json.dumps(rec, ensure_ascii=False, indent=1) + '\n')
        tb = json.loads(TERM_BASES.read_text()) if TERM_BASES.is_file() else {'schema': 1, 'purpose': 'Per-subject ruled term bases: absolute week = base + week within term. Created by whichever order lands first (SCI-COMPLETE §Q4) and read by the other.'}
        tb['science'] = {'bases': bases, 'source': 'tools/catalogue/SCIENCE_WEEK_BINDINGS.json calendarNotes', 'calendar': rec.get('calendarSource')}
        TERM_BASES.write_text(json.dumps(tb, ensure_ascii=False, indent=2) + '\n')
        print('[DONE] bindings %d -> %d; TERM_BASES.json science bases written' % (len(rec['entries']) - len(new), len(rec['entries'])))
    return 0


if __name__ == '__main__':
    sys.exit(main())
