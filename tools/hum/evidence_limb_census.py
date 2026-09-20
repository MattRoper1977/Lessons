#!/usr/bin/env python3
"""ORDER HUM-T landing — which signed Humanities/RE decks can be re-stamped.

Every one of the 73 signed decks carries a pinned source digest in
tools/catalogue/TERM_AND_STYLE_EVIDENCE.json. tools/catalogue/check_catalogue_static.py
asserts that pin against the working tree, so ANY byte change to a deck — the loop
transplant included — turns it red until the entry is re-stamped.

tools/catalogue/restamp_evidence_sha256.py is the only tool that may re-stamp, and it
refuses a deck whose week binding nothing but the pin can demonstrate: re-stamping
such a deck would freeze in a binding no limb proves. build_lesson_order.py holds the
limbs it accepts, and drops an unproved deck into unresolvedTiming, where its weeks
project as [].

This census measures, per deck, whether a limb holds on the CURRENT (pre-transplant)
bytes. A limb that holds before holds after, because the transplant only adds: it
never removes a config field, a declared cell or a term token.

    evidence_limb_census.py            markdown census to stdout
    evidence_limb_census.py --json     the landable/blocked split as JSON
    evidence_limb_census.py --self-test
"""
from __future__ import annotations

import argparse, json, re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
STRAND = ROOT / 'tools/catalogue/HUMANITIES_STRAND.json'
EVIDENCE = ROOT / 'tools/catalogue/TERM_AND_STYLE_EVIDENCE.json'
SPINE = ROOT / '_sownb/CALENDAR_SPINE.json'
BINDINGS = ROOT / 'tools/catalogue/SCIENCE_WEEK_BINDINGS.json'
COVER_MANIFEST = ROOT / 'tools/humanities_resources/SOURCE_MANIFEST.json'


def norm(s):
    return re.sub(r'\s+', ' ', s).strip()


def limbs(entry, config, text, cells, audit):
    """The three limbs build_lesson_order.py accepts for a drifted deck, by name.

    Returns {limb name: bool}. `enrichment` and the approved-Science digest limb are
    Science-only and cannot hold for a Humanities deck, so they are not offered here.
    """
    declared = config.get('source', {}) if isinstance(config, dict) else {}
    ref = "'" + declared.get('sheet', '') + "'!" + declared.get('cell', '')
    explicit = (ref in cells
                and norm(declared.get('outcome', '')) == norm(cells[ref]['verbatimOutcome'])
                and any(ref in p.get('refs', []) for p in entry.get('evidence', [])))
    preserved = any(p.get('currentOutcome') and config.get('sow') == p['currentOutcome']
                    and p.get('refs') and all(r in cells for r in p['refs'])
                    for p in entry.get('evidence', []))
    proofs = [p for p in entry.get('evidence', [])
              if p.get('method') == 'own title slide declaration' and isinstance(p.get('quote'), str)]
    tokens = {w['key'] for w in audit.get('weeks', [])}
    token = bool(proofs) and bool(tokens) and all(k in text for k in tokens)
    return {'declared cell': explicit, 'preserved outcome': preserved, 'term token': token}


def corrected_ref(declared):
    """The reference the deck actually declares.

    build_lesson_order.py builds "'<sheet>'!<cell>", but some decks record the WHOLE
    A1 reference in `cell`, so the gate builds "'X'!'X'!C63" and the cell can never be
    found. That is a defect in the construction, not in the deck. This reads the deck's
    intent so the census cannot blame a deck for the gate's spelling.
    """
    cell = declared.get('cell', '') or ''
    return cell if '!' in cell else "'" + declared.get('sheet', '') + "'!" + cell


def why_not(entry, config, cells):
    if not config:
        return 'the deck carries no lesson-config, so it declares nothing'
    declared = config.get('source', {})
    ref = corrected_ref(declared)
    prefix = 'even read as the deck spells it, ' if '!' in (declared.get('cell') or '') else ''
    if ref not in cells:
        return prefix + 'the declared cell is not a spine cell: ' + ref
    if not norm(declared.get('outcome', '')):
        return prefix + 'the deck declares the cell but records no outcome text'
    if norm(declared.get('outcome', '')) != norm(cells[ref]['verbatimOutcome']):
        return prefix + 'the declared outcome differs from the spine cell'
    return prefix + 'the declared cell is not named in the recorded evidence'


def rescued_by_correction(entry, config, cells):
    """Would the declared-cell limb hold if the reference were built as the deck spells it?

    Measured, not assumed: this is what says whether the construction defect costs a deck.
    """
    if not config:
        return False
    declared = config.get('source', {})
    ref = corrected_ref(declared)
    return (ref in cells
            and norm(declared.get('outcome', '')) == norm(cells[ref]['verbatimOutcome'])
            and any(ref in p.get('refs', []) for p in entry.get('evidence', [])))


def cover_pinned_paths():
    """Lesson routes the David cover pack pins by digest.

    tools/humanities_resources/check_resources.py asserts each of these 30 routes
    against the WORKING TREE (verify_change_boundary.py calls check(root, root)), so a
    transplant of any of them turns the GLV3 boundary gate red. Unlike the evidence
    record, nothing derives this manifest — build_resources.py reads it and never writes
    it — so there is no mechanical re-stamp and no limb to hold. A deck pinned here
    cannot be transplanted without a ruling.
    """
    if not COVER_MANIFEST.is_file():
        return set()
    doc = json.loads(COVER_MANIFEST.read_text())
    return {r['path'] for record in doc.get('records', []) for r in record.get('existing_routes', [])}


def is_landable(limb_holds, cover_pinned, strand_provable=False, q2=True):
    """A deck lands when the evidence fence admits it and the cover fence admits it.

    Evidence fence: a deck limb holds, OR (STOP-T3 ruling Q1, Matt Roper 2026-09-20) its
    row in the signed, digest-pinned strand record agrees with the deck's own projection.
    Cover fence: not pinned by the David cover pack, OR (ruling Q2) the route is re-stamped
    in its signed batch by tools/hum/restamp_cover_routes.py. A deck neither rescues is
    HELD by name (ruling Q3)."""
    return (bool(limb_holds) or bool(strand_provable)) and (not cover_pinned or q2)


def strand_provable(rel, cells, entry, rows, record_digest, pinned_digest):
    """Q1 on the pre-transplant bytes: what the deck projects today, against its strand row.

    The projection is what build_lesson_order.weeks_from reads from the deck's recorded
    evidence, filtered to the deck's own terms, exactly as the projection does."""
    sys.path.insert(0, str(ROOT / 'tools/catalogue'))
    import build_lesson_order as blo
    keys = [k for k in blo.weeks_from_cells(entry.get('evidence', []), cells)
            if blo.WEEK_KEY.match(k) and blo.WEEK_KEY.match(k)[1] in entry.get('terms', [])]
    return blo.strand_proof(rel, rows, record_digest, pinned_digest, keys)


def census(read_source):
    from lxml import html
    cells = {r['reference']: r for r in json.loads(SPINE.read_text())['workbookCells']}
    ev = json.loads(EVIDENCE.read_text())['entries']
    sci = json.loads(BINDINGS.read_text())['entries']
    cover = cover_pinned_paths()
    sys.path.insert(0, str(ROOT / 'tools/catalogue'))
    import build_lesson_order as blo
    srows, srecord, spin = blo.strand_rows()
    rows = []
    for r in json.loads(STRAND.read_text())['lessons']:
        rel = r['path']
        entry = ev.get(rel, {})
        src = read_source(rel)
        tree = html.fromstring(src)
        text = norm(' '.join(tree.itertext()))
        cfgs = tree.xpath('//script[@id="lesson-config"]/text()')
        config = json.loads(cfgs[0]) if cfgs else {}
        held = limbs(entry, config, text, cells, sci.get(rel, {}))
        pinned_by_cover = rel in cover
        q1_ok, q1_why = strand_provable(rel, cells, entry, srows, srecord, spin)
        ok = is_landable(any(held.values()), pinned_by_cover, q1_ok)
        rows.append({'path': rel, 'pathway': r['pathway'], 'strand': r['strand'],
                     'term': r.get('term'), 'week': r.get('week'),
                     'pinned': bool(entry.get('sha256')),
                     'limb': next((k for k, v in held.items() if v), None),
                     'landable': ok,
                     'limbHolds': any(held.values()),
                     'strandProvable': q1_ok,
                     'strandWhy': q1_why,
                     'coverPinned': pinned_by_cover,
                     'coverRoute': 'Q2 re-stamp in its signed batch' if pinned_by_cover else None,
                     'refConstructionDefect': '!' in ((config.get('source') or {}).get('cell') or ''),
                     'rescuedByCorrectedRef': (not any(held.values())) and rescued_by_correction(entry, config, cells),
                     'reason': None if ok else ('HELD (Q3): no deck limb, and the strand row cannot be compared: ' + q1_why)})
    return rows


def from_git(revision):
    def read(rel):
        out = subprocess.run(['git', '-C', str(ROOT), 'show', f'{revision}:{rel}'],
                             capture_output=True, text=True)
        if out.returncode:
            raise SystemExit('cannot read %s at %s' % (rel, revision))
        return out.stdout
    return read


def self_test():
    bad = 0

    def check(name, cond):
        nonlocal bad
        print('  [%s] %s' % ('ok' if cond else 'FAIL', name))
        bad += 0 if cond else 1

    cells = {"'S'!C1": {'verbatimOutcome': 'Do the thing.', 'termWeek': 'Aut1·W1'}}
    entry = {'evidence': [{'refs': ["'S'!C1"]}]}
    cfg = {'source': {'sheet': 'S', 'cell': 'C1', 'outcome': 'Do the thing.'}}
    check('a declared cell matching the spine holds',
          limbs(entry, cfg, '', cells, {})['declared cell'])
    check('a declared cell the evidence does not name fails',
          not limbs({'evidence': []}, cfg, '', cells, {})['declared cell'])
    cfg2 = {'source': {'sheet': 'S', 'cell': 'C1', 'outcome': 'Something else.'}}
    check('a declared outcome that differs fails',
          not limbs(entry, cfg2, '', cells, {})['declared cell'])
    e3 = {'evidence': [{'currentOutcome': 'X', 'refs': ["'S'!C1"]}]}
    check('a preserved outcome holds', limbs(e3, {'sow': 'X'}, '', cells, {})['preserved outcome'])
    check('a preserved outcome the config no longer carries fails',
          not limbs(e3, {'sow': 'Y'}, '', cells, {})['preserved outcome'])
    e4 = {'evidence': [{'method': 'own title slide declaration', 'quote': 'q'}]}
    a4 = {'weeks': [{'key': 'Aut1·W1'}]}
    check('a term token present in the text holds',
          limbs(e4, {}, 'lesson for Aut1·W1 today', cells, a4)['term token'])
    check('a term token absent from the text fails',
          not limbs(e4, {}, 'no token here', cells, a4)['term token'])
    check('a deck with no config is refused by name',
          'no lesson-config' in why_not(entry, {}, cells))
    check('an empty declared outcome is named as such',
          'records no outcome text' in why_not(entry, {'source': {'sheet': 'S', 'cell': 'C1'}}, cells))
    whole = {'source': {'sheet': 'S', 'cell': "'S'!C1", 'outcome': 'Do the thing.'}}
    check('a reference the deck spells whole is read as the deck spells it',
          corrected_ref(whole['source']) == "'S'!C1"
          and rescued_by_correction(entry, whole, cells))
    check('the construction defect is named when it is the deck spelling',
          'even read as the deck spells it' in
          why_not(entry, {'source': {'sheet': 'S', 'cell': "'S'!C9"}}, cells))
    check('correcting the reference rescues nothing when no outcome is recorded',
          not rescued_by_correction(entry, {'source': {'sheet': 'S', 'cell': "'S'!C1"}}, cells))
    check('a limb with no cover pin lands', is_landable(True, False))
    check('before Q2, a cover-pinned deck was refused even when a limb held', not is_landable(True, True, q2=False))
    check('under Q2, a cover-pinned deck lands and its route is re-stamped in the batch', is_landable(True, True))
    check('under Q1, a deck with no limb but a strand row agreeing with its projection lands', is_landable(False, False, strand_provable=True))
    check('a deck with no limb and no strand proof is HELD whatever the cover says',
          not is_landable(False, False) and not is_landable(False, True))
    check('the cover manifest is read and names its routes', len(cover_pinned_paths()) == 30)
    print('self-test ' + ('PASS' if not bad else 'FAIL (%d)' % bad))
    return 1 if bad else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--revision', default='origin/main',
                    help='read deck bytes from this revision (default origin/main)')
    ap.add_argument('--json', action='store_true')
    ap.add_argument('--self-test', action='store_true')
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    rows = census(from_git(args.revision))
    if args.json:
        print(json.dumps({'revision': args.revision, 'rows': rows}, indent=1, ensure_ascii=False))
        return 0
    land = [r for r in rows if r['landable']]
    block = [r for r in rows if not r['landable']]
    limb = [r for r in rows if r['limbHolds']]
    print('SEARCH SCOPE: %d signed decks in %s, bytes at %s'
          % (len(rows), STRAND.relative_to(ROOT), args.revision))
    print('pinned source digest: %d of %d' % (sum(r['pinned'] for r in rows), len(rows)))
    print('re-stampable (a limb holds): %d' % len(limb))
    print('refused (only the pin holds the week): %d' % (len(rows) - len(limb)))
    print('of the re-stampable, also pinned by the David cover pack: %d'
          % sum(r['coverPinned'] for r in limb))
    print('rescued by the strand row (ruling Q1): %d' % sum(r['strandProvable'] and not r['limbHolds'] for r in rows))
    print('cover routes to re-stamp in their batch (ruling Q2): %d' % sum(r['coverPinned'] for r in land))
    print('LANDABLE under the rulings: %d' % len(land))
    print('HELD by name (ruling Q3): %d' % len(block))
    print('refused decks whose config spells the whole reference in `cell`: %d'
          % sum(r['refConstructionDefect'] for r in block))
    print('of those, rescued if the reference were built as the deck spells it: %d'
          % sum(r['rescuedByCorrectedRef'] for r in block))
    print()
    print('| deck | pathway | limb | verdict |')
    print('| --- | --- | --- | --- |')
    for r in sorted(rows, key=lambda r: (r['pathway'], r['path'])):
        print('| %s | %s | %s | %s |'
              % (r['path'].split('/')[-1], r['pathway'],
                 r['limb'] or '—', 'LANDABLE' if r['landable'] else r['reason']))
    return 0


if __name__ == '__main__':
    sys.exit(main())
