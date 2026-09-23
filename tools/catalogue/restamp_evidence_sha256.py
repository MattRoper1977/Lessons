#!/usr/bin/env python3
"""Re-stamp the recorded source digest of reviewed catalogue evidence entries.

    restamp_evidence_sha256.py --check
    restamp_evidence_sha256.py --write --decks <reviewed.json>
    restamp_evidence_sha256.py --self-test

tools/catalogue/TERM_AND_STYLE_EVIDENCE.json records, per hashed entry, the sha256 of the
bytes that entry's term/style evidence was derived from. When a reviewed release re-dresses a
deck, those bytes move and tools/catalogue/check_catalogue_static.py goes red on a content-hash
mismatch -- correctly, because nothing has yet said the evidence still holds for the new bytes.

restamp_generated_region_digests.py already covers the one case it can PROVE without judgement:
a change confined to the generated maker-splash region. It refuses anything else by name, which
is why it refuses a chassis re-dress. This tool covers the reviewed case instead, and it refuses
to act on judgement it has not been given:

  * the deck list is passed EXPLICITLY and has no default population. A deck outside the list is
    never touched, whatever its digest says.
  * each listed deck carries its REVIEWED NEW DIGEST. If the working tree does not match, the
    bytes moved after the review and the tool refuses the whole run.
  * a limb must hold on the new bytes. build_lesson_order.py proves a drifted deck through
    the narrowed token limb (_sx3/DECISION_quote_limb.md) or, since ORDER HUM-T STOP-T3
    ruling Q1 (Matt Roper, 2026-09-20), through its row in the signed, digest-pinned
    strand record tools/catalogue/HUMANITIES_STRAND.json when the row's term·week equals
    the deck's own projection (build_lesson_order.strand_proof), and, since Matt's ruling on the
    batch-2 limbs (2026-09-22), a Science deck through its pinned SCIENCE_WEEK_BINDINGS row
    (science_row_proof, the same three conditions) or its own "Autumn 2 · Week n" label equal to
    that row (science_label_proof); a deck it cannot prove is refused,
    because re-stamping would freeze in a week binding nothing can demonstrate. This is the
    latent loss _sx3/FENCE.json exists to fence, so a fenced path is refused outright.
  * the entry's recorded term/weeks must still agree with SCIENCE_WEEK_BINDINGS, and style is
    never written.
  * a deck HELD BY NAME (_sci/HELD.md, the R-GAPS rows of _sx3/RELEASE_LEDGER.md) is EXCLUDED from
    the list by derivation and never re-stamped; the rest of the list proceeds (Matt, 2026-09-23:
    "the re-stamp list excludes held decks BY DERIVATION ... never by hand"). restamp_plan still
    refuses a held deck it is handed, so no caller can re-stamp one by skipping the exclusion.

ONLY the sha256 field of a listed, moved, proved entry is rewritten. No other field, no other
entry, no shelf, no lesson-order projection. After --write, run build_lesson_order.py to project
the digests and re-pin.

--check takes no list: it asserts the invariant the estate actually needs, that no hashed entry's
recorded digest differs from the working tree. That is the same condition check_catalogue_static
asserts, reported per path instead of as one bare assertion.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = ROOT / 'tools/catalogue/TERM_AND_STYLE_EVIDENCE.json'
BINDINGS = ROOT / 'tools/catalogue/SCIENCE_WEEK_BINDINGS.json'
FENCE = ROOT / '_sx3/FENCE.json'
# Held decks, derived -- never typed into a batch's --decks list by hand (Matt, 2026-09-23, the
# limbs ruling 4). The held-by-name record, and the R-GAPS section of the release ledger.
HELD = ROOT / '_sci/HELD.md'
RELEASE_LEDGER = ROOT / '_sx3/RELEASE_LEDGER.md'
DECK_PATH = re.compile(r'`(Science_Teesside/[^`]+\.html)`')


def moved_entries(entries, digest_of):
    """(path, recorded, actual) for every hashed entry whose bytes no longer match."""
    out = []
    for path, meta in entries.items():
        recorded = meta.get('sha256') if isinstance(meta, dict) else None
        if not recorded:
            continue
        actual = digest_of(path)
        if actual is not None and actual != recorded:
            out.append((path, recorded, actual))
    return sorted(out)


def held_by_name(held_text, ledger_text):
    """{deck: record} for every Science deck the two records hold. Pure.

    _sci/HELD.md: every Science deck path it names in backticks -- the file lists held decks and,
    for other sets, only the record files that hold them. _sx3/RELEASE_LEDGER.md: the decks named
    in the rows of its R-GAPS section whose ruling cell carries R-GAPS (the section ends at the
    next heading)."""
    out = {p: '_sci/HELD.md' for p in DECK_PATH.findall(held_text or '')}
    section = re.search(r'^## R-GAPS.*?(?=^## |\Z)', ledger_text or '', re.M | re.S)
    for line in (section.group(0) if section else '').splitlines():
        cells = line.split('|')
        if len(cells) > 2 and 'R-GAPS' in cells[-2]:
            for p in DECK_PATH.findall(line):
                out.setdefault(p, '_sx3/RELEASE_LEDGER.md R-GAPS')
    return out


def exclude_held(reviewed, held):
    """(kept, excluded) -- the --decks list with every held deck taken OUT by derivation. Pure.

    excluded maps each dropped path to the record that holds it. Ruled 2026-09-23: the list
    excludes held decks by derivation, never by hand, so a batch list naming a held deck is not
    edited by hand and does not abort the run -- the held deck is named and left alone. If its
    bytes moved anyway, --check (and check_catalogue_static) stays red on it: excluded is never
    re-stamped."""
    held = held or {}
    kept = {p: d for p, d in reviewed.items() if p not in held}
    excluded = {p: held[p] for p in sorted(reviewed) if p in held}
    return kept, excluded


def held_paths():
    return held_by_name(HELD.read_text() if HELD.is_file() else '',
                        RELEASE_LEDGER.read_text() if RELEASE_LEDGER.is_file() else '')


def fenced_paths():
    if not FENCE.is_file():
        return set()
    return {row['path'] for row in json.loads(FENCE.read_text()).get('fenced', [])}


def restamp_plan(entries, reviewed, digest_of, proved, bindings, fenced, reasons=None, held=None):
    """Pure rule, so the self-test plants against the code the tree is judged by.

    Returns (errors, restamps, noops). `reviewed` maps path -> reviewed new digest. `reasons` maps
    a Science path to {limb: why} from build_lesson_order.derive()['scienceRefusals'], so a refusal
    names the limb that refused it."""
    errors, restamps, noops = [], [], []
    for path in sorted(reviewed):
        meta = entries.get(path)
        if not isinstance(meta, dict) or 'sha256' not in meta:
            errors.append('listed deck has no hashed evidence entry: ' + path)
            continue
        if path in fenced:
            errors.append('listed deck is fenced by _sx3/FENCE.json: ' + path)
            continue
        if held and path in held:
            errors.append('listed deck is held by name (%s): %s' % (held[path], path))
            continue
        actual = digest_of(path)
        if actual is None:
            errors.append('listed deck is not present in the tree: ' + path)
            continue
        if actual != reviewed[path]:
            errors.append('working tree disagrees with the reviewed new digest, so the bytes '
                          'moved after the review: ' + path)
            continue
        if actual == meta['sha256']:
            noops.append(path)
            continue
        if path not in proved:
            why = (reasons or {}).get(path)
            errors.append(('no limb proves the new bytes (%s): ' % '; '.join('%s -- %s' % kv for kv in sorted(why.items()))
                           if why else 'the narrowed token limb does not hold on the new bytes: ') + path)
            continue
        binding = bindings.get(path)
        if binding is not None:
            terms = set(meta.get('terms') or ([meta['term']] if meta.get('term') else []))
            if terms and not all(w['term'] in terms for w in binding.get('weeks', [])):
                errors.append('recorded term/weeks no longer agree with SCIENCE_WEEK_BINDINGS: ' + path)
                continue
        restamps.append((path, meta['sha256'], actual))
    return errors, restamps, noops


def load_proved():
    """The decks build_lesson_order.py currently proves through the narrowed limb."""
    return load_proofs()[0]


def load_proofs():
    """(proved set, {Science path: {limb: why}}) from one build_lesson_order.derive()."""
    sys.path.insert(0, str(ROOT / 'tools/catalogue'))
    import build_lesson_order
    d = build_lesson_order.derive()
    return set(d['refreshedSourceProofs']), d.get('scienceRefusals', {})


def digest_of_tree(path):
    f = ROOT / path
    return hashlib.sha256(f.read_bytes()).hexdigest() if f.is_file() else None


def run_check():
    entries = json.loads(EVIDENCE.read_text())['entries']
    moved = moved_entries(entries, digest_of_tree)
    hashed = sum(1 for m in entries.values() if isinstance(m, dict) and m.get('sha256'))
    print(f'SEARCH SCOPE: {EVIDENCE.relative_to(ROOT)} — {hashed} hashed entries, working-tree bytes')
    for path, recorded, actual in moved:
        print(f'  [MOVED] {path}\n      recorded {recorded}\n      tree     {actual}')
    if moved:
        print(f'[FAIL] {len(moved)} recorded digest(s) differ from the tree; a reviewed re-stamp is '
              f'needed, or the change was not intended')
        return 1
    print(f'[PASS] every hashed entry matches the tree')
    return 0


def run_write(decks_path):
    entries_doc = json.loads(EVIDENCE.read_text())
    entries = entries_doc['entries']
    listed = json.loads(Path(decks_path).read_text())
    held = held_paths()
    reviewed, excluded = exclude_held(listed, held)
    bindings = json.loads(BINDINGS.read_text())['entries'] if BINDINGS.is_file() else {}
    proved, reasons = load_proofs()
    errors, restamps, noops = restamp_plan(entries, reviewed, digest_of_tree, proved, bindings, fenced_paths(),
                                           reasons, held)
    print(f'SEARCH SCOPE: {len(listed)} reviewed deck(s) from {decks_path}, '
          f'against {EVIDENCE.relative_to(ROOT)}')
    print(f'  limb-proved decks available: {len(proved)}')
    for path, record in excluded.items():
        print(f'  [HELD] excluded by derivation ({record}), never re-stamped: {path}')
    for e in errors:
        print('  [REFUSED] ' + e)
    for path in noops:
        print(f'  [NO-OP] listed deck already matches its recorded digest: {path}')
    for path, old, new in restamps:
        print(f'  [RESTAMP] {path}\n      {old}\n   -> {new}')
    if errors:
        print(f'[FAIL] {len(errors)} refusal(s); nothing written')
        return 1
    # Only the sha256 of a listed, moved, proved entry is rewritten.
    before = json.dumps(entries_doc, ensure_ascii=False, indent=2) + '\n'
    for path, _old, new in restamps:
        entries[path]['sha256'] = new
    after = json.dumps(entries_doc, ensure_ascii=False, indent=2) + '\n'
    changed = sum(1 for a, b in zip(before.splitlines(), after.splitlines()) if a != b)
    assert changed == len(restamps), f'rewrote {changed} lines for {len(restamps)} re-stamps'
    EVIDENCE.write_text(after)
    print(f'[DONE] {len(restamps)} digest(s) re-stamped, {len(noops)} no-op, {len(excluded)} held and '
          f'excluded, {changed} line(s) changed in the file')
    return 0


def self_test():
    # CORRECTION #40 (ruled 2026-09-23: "correction numbered; the fix rides the limbs PR with its
    # planted-failure proof"). The failure counter is `bad`, never `ok`. It was `ok` until 2026-09-22,
    # and the Q1 block's `ok, why = strand_proof(...)` rebound it to a bool: the last Q1 line leaves it
    # False, so every failure counted before it was erased and the self-test printed PASS whatever
    # had failed. Found by the adversarial trace of the W9L1 re-stamp refusal. The planted-failure
    # proof is COMMITTED, not a one-off: RESTAMP_SELFTEST_PLANT plants one false check here, BEFORE
    # every rebinding, and the last check below runs this self-test in a child process with it set
    # and requires 'self-test FAIL (1)' and exit 1. Put the counter back to `ok` and that last check
    # goes red (the child prints PASS) -- measured when this was written.
    bad = 0

    def check(name, condition):
        nonlocal bad
        print(f'  [{"ok" if condition else "FAIL"}] {name}')
        bad += 0 if condition else 1

    planted = bool(os.environ.get('RESTAMP_SELFTEST_PLANT'))
    if planted:
        check('PLANTED FAILURE (correction #40 control): false on purpose, before any `ok, why = ...`', False)

    entries = {
        'A.html': {'sha256': 'a' * 64, 'term': 'Aut1', 'terms': ['Aut1'], 'style': 'full-lundy'},
        'B.html': {'sha256': 'b' * 64, 'term': 'Aut2', 'terms': ['Aut2'], 'style': 'classic'},
        'F.html': {'sha256': 'f' * 64, 'term': 'Aut1', 'terms': ['Aut1'], 'style': 'classic'},
        'T.html': {'sha256': 't' * 64, 'term': 'Aut1', 'terms': ['Aut1'], 'style': 'classic'},
        'U.html': {'sha256': 'u' * 64, 'term': 'Aut1', 'terms': ['Aut1'], 'style': 'classic'},
    }
    tree = {'A.html': '1' * 64, 'B.html': 'b' * 64, 'F.html': '3' * 64,
            'T.html': '4' * 64, 'U.html': '5' * 64}
    d = tree.get
    bindings = {'T.html': {'weeks': [{'term': 'Spr1', 'key': 'Spr1·W2'}]}}
    proved = {'A.html', 'F.html', 'T.html'}
    fenced = {'F.html'}

    e, r, n = restamp_plan(entries, {'A.html': '1' * 64}, d, proved, bindings, fenced)
    check('a listed, moved, proved deck is re-stamped', not e and [x[0] for x in r] == ['A.html'])

    e, r, n = restamp_plan(entries, {'A.html': '1' * 64}, d, proved, bindings, fenced)
    check('(i) an unlisted deck is never touched', 'B.html' not in [x[0] for x in r]
          and 'U.html' not in [x[0] for x in r] and len(r) == 1)

    e, r, n = restamp_plan(entries, {'T.html': '4' * 64}, d, proved, bindings, fenced)
    check('(ii) recorded term disagreeing with the binding is refused',
          len(e) == 1 and 'no longer agree with SCIENCE_WEEK_BINDINGS' in e[0] and not r)

    e, r, n = restamp_plan(entries, {'B.html': 'b' * 64}, d, proved, bindings, fenced)
    check('(iii) a listed deck whose bytes did not move is a reported no-op',
          not e and not r and n == ['B.html'])

    e, r, n = restamp_plan(entries, {'U.html': '5' * 64}, d, proved, bindings, fenced)
    check('a deck the token limb cannot prove is refused',
          len(e) == 1 and 'narrowed token limb' in e[0] and not r)

    e, r, n = restamp_plan(entries, {'F.html': '3' * 64}, d, proved, bindings, fenced)
    check('a fenced deck is refused outright', len(e) == 1 and 'fenced' in e[0] and not r)

    e, r, n = restamp_plan(entries, {'A.html': '9' * 64}, d, proved, bindings, fenced)
    check('bytes that moved after the review are refused',
          len(e) == 1 and 'moved after the review' in e[0] and not r)

    e, r, n = restamp_plan(entries, {'Z.html': '1' * 64}, d, proved, bindings, fenced)
    check('a listed deck with no evidence entry is refused',
          len(e) == 1 and 'no hashed evidence entry' in e[0] and not r)

    e, r, n = restamp_plan(entries, {}, d, proved, bindings, fenced)
    check('an empty list writes nothing', not e and not r and not n)

    # STOP-T3 ruling Q1: the strand-record limb, planted against the function the
    # projection is judged by. Row absent, row week differing from the projection, and a
    # record digest differing from its pin are each a refusal by name.
    sys.path.insert(0, str(ROOT / 'tools/catalogue'))
    from build_lesson_order import strand_proof
    rows = {'H/a.html': {'term': 'Aut1', 'week': 4}}
    ok, why = strand_proof('H/a.html', rows, 'd' * 64, 'd' * 64, ['Aut1·W4'])
    check('Q1: a pinned strand row agreeing with the projection proves the deck', ok and why == 'Aut1·W4')
    ok, why = strand_proof('H/z.html', rows, 'd' * 64, 'd' * 64, ['Aut1·W4'])
    check('Q1: row absent -> FAIL', not ok and 'no strand row' in why)
    ok, why = strand_proof('H/a.html', rows, 'd' * 64, 'd' * 64, ['Aut1·W5'])
    check('Q1: row week != projection -> FAIL', not ok and 'differs from the projection' in why)
    ok, why = strand_proof('H/a.html', rows, 'd' * 64, 'e' * 64, ['Aut1·W4'])
    check('Q1: record digest != pin -> FAIL', not ok and 'differs from its pin' in why)
    ok, why = strand_proof('H/a.html', rows, 'd' * 64, None, ['Aut1·W4'])
    check('Q1: an unpinned record proves nothing', not ok)
    ok, why = strand_proof('H/a.html', rows, 'd' * 64, 'd' * 64, [])
    check('Q1: a deck projecting no week cannot be compared, so it is not proved', not ok and 'projects no week' in why)

    # Ruling on the batch-2 limbs (Matt Roper, 2026-09-22): the Science ROW limb and the Science
    # LABEL limb, the Q1 shape for Science, planted against the functions derive() calls.
    from build_lesson_order import (science_row_proof, science_label_proof, science_limbs,
                                    deck_statement_text, NO_PROJECTION, week_keys)
    srows = {'S/a.html': {'weeks': [{'key': 'Aut2·W1', 'term': 'Aut2', 'weekWithinTerm': 1}]}}
    ok, why = science_row_proof('S/a.html', srows, 'd' * 64, 'd' * 64, ['Aut2·W1'])
    check('ROW: a pinned SCIENCE_WEEK_BINDINGS row agreeing with the projection proves the deck',
          ok and why == 'Aut2·W1')
    ok, why = science_row_proof('S/z.html', srows, 'd' * 64, 'd' * 64, ['Aut2·W1'])
    check('ROW RED PROOF: row absent -> refuse', not ok and 'no SCIENCE_WEEK_BINDINGS row' in why)
    ok, why = science_row_proof('S/a.html', srows, 'd' * 64, 'e' * 64, ['Aut2·W1'])
    check('ROW RED PROOF: pin mismatch -> refuse', not ok and 'differs from its pin' in why)
    ok, why = science_row_proof('S/a.html', srows, 'd' * 64, None, ['Aut2·W1'])
    check('ROW RED PROOF: an unpinned record proves nothing', not ok and 'differs from its pin' in why)
    ok, why = science_row_proof('S/a.html', srows, 'd' * 64, 'd' * 64, ['Aut2·W2'])
    check('ROW RED PROOF: row week != projection -> refuse', not ok and 'differs from the projection' in why)
    ok, why = science_row_proof('S/a.html', srows, 'd' * 64, 'd' * 64, [])
    check('ROW RED PROOF: a deck projecting no week cannot be compared, so it is not proved',
          not ok and 'projects no week' in why)
    # Second cut, after the adversarial review of the first.
    ok, why = science_row_proof('S/a.html', srows, 'd' * 64, 'd' * 64, ['Aut2·W1'], {'Aut2·W5'})
    check('ROW RED PROOF: a deck stating another week about itself is refused (admit_transaction\'s rule)',
          not ok and 'does not cover its row' in why)
    ok, why = science_row_proof('S/a.html', srows, 'd' * 64, 'd' * 64, ['Aut2·W1'], {'Aut2·W1', 'Aut1·W3'})
    check('ROW: a deck stating its own week and recalling another is still proved (stated covers the row)',
          ok and why == 'Aut2·W1')
    ok, why = science_row_proof('S/a.html', {'S/a.html': {'weeks': [{'key': 'Aut2·W1', 'term': 'Aut2', 'weekWithinTerm': 1},
                                                                     {'key': 'junk'}]}}, 'd' * 64, 'd' * 64, ['Aut2·W1'])
    check('ROW RED PROOF: a row carrying an unreadable week is refused, not quietly trimmed',
          not ok and 'unreadable week' in why)
    ok, why = science_row_proof('S/a.html', {'S/a.html': {'weeks': [{'key': 'Aut2·W1', 'term': 'Aut2', 'weekWithinTerm': 2}]}},
                                'd' * 64, 'd' * 64, ['Aut2·W1'])
    check('ROW RED PROOF: a row whose key disagrees with its own term/weekWithinTerm is refused',
          not ok and 'unreadable week' in why)
    limb, res = science_limbs('S/a.html', srows, 'd' * 64, 'd' * 64, ['Aut2·W2'], set(), 'Autumn 2 · Week 1')
    check('WIRING RED PROOF: a projection that disagrees with the row is refused, and a matching label does not rescue it',
          limb is None and 'differs from the projection' in res['row'] and res['label'].startswith('not tried'))
    limb, res = science_limbs('S/a.html', srows, 'd' * 64, 'd' * 64, [], set(), 'Space · Autumn 2 · Week 1')
    check('WIRING: where the evidence projects nothing, the label limb decides', limb == 'label' and res == 'Aut2·W1')
    limb, res = science_limbs('S/a.html', srows, 'd' * 64, 'd' * 64, [], set(), 'Space')
    check('WIRING: every limb that refuses is named, with its reason',
          limb is None and res == {'row': NO_PROJECTION, 'label': 'the deck writes no term-week label'})
    for rng in ('Autumn 2 · Week 1–2', 'Autumn 2 · Week 1-3', 'Autumn 2 · Week 1.5'):
        ok, why = science_label_proof('S/a.html', srows, 'd' * 64, 'd' * 64, rng)
        check('LABEL RED PROOF: %r is a range or decimal, refused' % rng, not ok and 'range or decimal' in why)
    from lxml import html as lhtml
    said = deck_statement_text(lhtml.fromstring('<html><body><section class="slide"><p>Space</p>'
                                                '<script>/* Autumn 2 · Week 1 */</script></section></body></html>'))
    check('LABEL: a week inside a <script> is not the deck saying it', 'Week 1' not in said and 'Space' in said)
    ok, why = science_label_proof('S/a.html', srows, 'd' * 64, 'd' * 64, 'Space · Autumn 2 · Week 1 · Explore')
    check('LABEL: a label equal to the pinned row proves the deck', ok and why == 'Aut2·W1')
    ok, why = science_label_proof('S/a.html', srows, 'd' * 64, 'd' * 64, 'Space · Autumn 2 · Week 3 · Explore')
    check('LABEL RED PROOF: wrong week in the label -> refuse', not ok and 'its SCIENCE_WEEK_BINDINGS row is' in why)
    ok, why = science_label_proof('S/z.html', srows, 'd' * 64, 'd' * 64, 'Space · Autumn 2 · Week 1 · Explore')
    check('LABEL RED PROOF: label present, row absent -> refuse', not ok and 'has no SCIENCE_WEEK_BINDINGS row' in why)
    ok, why = science_label_proof('S/a.html', srows, 'd' * 64, 'e' * 64, 'Space · Autumn 2 · Week 1 · Explore')
    check('LABEL RED PROOF: pin mismatch -> refuse', not ok and 'differs from its pin' in why)
    ok, why = science_label_proof('S/a.html', srows, 'd' * 64, 'd' * 64, 'Autumn 2 · Week 1, then Autumn 2 · Week 2')
    check('LABEL RED PROOF: a label naming any other week as well -> refuse',
          not ok and "the deck writes ['Aut2·W1', 'Aut2·W2']" in why)
    ok, why = science_label_proof('S/a.html', srows, 'd' * 64, 'd' * 64, 'LAUNCH · W9 · Lesson 1')
    check('LABEL: an absolute week ("W9") is not a term-week label, so it proves nothing', not ok and 'writes no term-week label' in why)

    # The same limbs against the REAL tree: the record, its pin, and the named decks.
    import build_lesson_order as blo
    from lxml import html as lhtml
    bdoc = json.loads(BINDINGS.read_text())
    brecord = hashlib.sha256(BINDINGS.read_bytes()).hexdigest()
    bpin = blo.catalogue_pin(BINDINGS)
    cells = {r['reference']: r for r in json.loads((ROOT / '_sownb/CALENDAR_SPINE.json').read_text())['workbookCells']}
    evidence = json.loads(EVIDENCE.read_text())['entries']
    terms = json.loads((ROOT / 'assets/catalogue/terms-and-styles.json').read_text())['entries']
    check('the real SCIENCE_WEEK_BINDINGS record equals its CATALOGUE_PINS digest', bpin == brecord)
    w9l1 = 'Science_Teesside/Launch/W8-W13_2026-27/SCI_L_W9L1_Cell_Cycle_Introduce.html'
    ok, why = science_row_proof(w9l1, bdoc['entries'], brecord, bpin,
                                blo.evidence_projection(evidence[w9l1]['evidence'], cells, terms[w9l1]['terms']))
    check('ROW, real tree: SCI_L_W9L1 is proved by its pinned row (Aut2·W1)', ok and why == 'Aut2·W1')
    # The five GROW *A decks of the SX3 31, named rather than globbed (W8A beside them is an
    # exemplar that writes no label at all). In derive() the ROW limb proves them first, because
    # their evidence projects their week; this proves the label limb would hold on them too.
    grow_a = ['Science_Teesside/Grow/W8-W13_2026-27/' + f for f in (
        'SCI_G_W9A_Spherical_Bodies_Explore.html', 'SCI_G_W10A_Solar_System_Research_Explore.html',
        'SCI_G_W11A_Global_Warming_Explore.html', 'SCI_G_W12A_Science_Connections_Explore.html',
        'SCI_G_W13A_Rover_Rescue_Plan_Explore.html')]
    label_ok = []
    for p in grow_a:
        text = blo.deck_statement_text(lhtml.fromstring((ROOT / p).read_text()))
        label_ok.append(science_label_proof(p, bdoc['entries'], brecord, bpin, text)[0])
    check('LABEL, real tree: the 5 GROW *A Explore decks are each proved by their own label',
          all((ROOT / p).is_file() for p in grow_a) and all(label_ok))
    # Ruling 4 (2026-09-23): held decks leave the re-stamp by DERIVATION, never by hand.
    held_md = '| `Science_Teesside/G/x.html` | GROW |\nsee `_sx3/HELD.md`\n'
    ledger = ('## R-GAPS — gaps\n| row | gap | decks | ruling |\n|---|---|---|---|\n'
              '| 30 | teacher-only | 1 of 36, `Science_Teesside/B/w12.html` | **R-GAPS**, named |\n'
              '| 31 | reveal | `Science_Teesside/B/other.html` | **R-SR**: no dressing |\n## Next\n'
              '| 9 | x | `Science_Teesside/B/after.html` | **R-GAPS** |\n')
    hb = held_by_name(held_md, ledger)
    check('HELD: derived from _sci/HELD.md and the R-GAPS rows, nothing else',
          hb == {'Science_Teesside/G/x.html': '_sci/HELD.md', 'Science_Teesside/B/w12.html': '_sx3/RELEASE_LEDGER.md R-GAPS'})
    e, r, n = restamp_plan({'Science_Teesside/B/w12.html': {'sha256': 'a' * 64, 'terms': ['Aut2']}},
                           {'Science_Teesside/B/w12.html': '1' * 64}, lambda p: '1' * 64,
                           {'Science_Teesside/B/w12.html'}, {}, set(), None, hb)
    check('HELD RED PROOF: a held deck on the --decks list is refused by name, even though a limb proves it',
          len(e) == 1 and 'held by name (_sx3/RELEASE_LEDGER.md R-GAPS)' in e[0] and not r)
    real = held_paths()
    check('HELD, real tree: SCI_B_W12 is held by its R-GAPS row, derived from the ledger',
          real.get('Science_Teesside/Build/W8-W13_2026-27/SCI_B_W12_Give_a_rock_a_job_Classic.html')
          == '_sx3/RELEASE_LEDGER.md R-GAPS')
    check('HELD, real tree: the two case-study decks are held, derived from _sci/HELD.md',
          real.get('Science_Teesside/Grow/W18-W26_2026-27/SCI_G_W18A_The_Cold_Case.html') == '_sci/HELD.md'
          and real.get('Science_Teesside/Launch/W17-W26_2026-27/SCI_L_W17_Evolution_Build_The_Evidence_Case.html')
          == '_sci/HELD.md')

    # Ruling 3 (2026-09-23): only the title stage is the deck's claim; a recall line is not.
    recall = lhtml.fromstring('<html><body><section class="slide"><p>BUILD · Science · Week 4A</p></section>'
                              '<section class="slide"><p>Retrieve the previous lesson: Aut1·W3</p></section></body></html>')
    ok, why = science_row_proof('S/a.html', {'S/a.html': {'weeks': [{'key': 'Aut1·W4', 'term': 'Aut1', 'weekWithinTerm': 4}]}},
                                'd' * 64, 'd' * 64, ['Aut1·W4'], set(week_keys(deck_statement_text(recall))))
    check('CLAIM: a recall line on a later stage is not the deck\'s claim, so the row proves it', ok)
    wrong = lhtml.fromstring('<html><body><section class="slide"><p>BUILD · Science · Autumn 1 · Week 3</p></section>'
                             '<section class="slide"><p>Retrieve: Aut1·W3</p></section></body></html>')
    ok, why = science_row_proof('S/a.html', {'S/a.html': {'weeks': [{'key': 'Aut1·W4', 'term': 'Aut1', 'weekWithinTerm': 4}]}},
                                'd' * 64, 'd' * 64, ['Aut1·W4'], set(week_keys(deck_statement_text(wrong))))
    check('CLAIM RED PROOF: a title stage claiming the wrong week still refuses', not ok and 'does not cover its row' in why)

    # Ruling 2 (2026-09-23): the decks the Science row limb proves LEAVE the fence; the rest stay.
    fence = json.loads(FENCE.read_text())
    def row_holds(p):
        return science_row_proof(p, bdoc['entries'], brecord, bpin,
                                 blo.evidence_projection(evidence[p]['evidence'], cells, terms[p]['terms']))
    released = [(r['path'], r['heldWeek']) for r in fence.get('released', {}).get('paths', [])]
    check('FENCE: every released deck is held by the row limb at the week the fence records (%d released)'
          % len(released), len(released) == 3 and all(row_holds(p) == (True, w) for p, w in released))
    check('FENCE RED PROOF: every deck still fenced is refused by the row limb, so it stays fenced (%d fenced)'
          % len(fence['fenced']), len(fence['fenced']) == 3
          and all(not row_holds(r['path'])[0] for r in fence['fenced']))

    # Ruled 2026-09-23 on SCI_G_W16B: a title-stage week the row does not bind refuses, whichever
    # limb would prove the deck. Its own cell (C29, Spr1·W2) covers the row; its title says Week 16.
    w16b = 'Science_Teesside/Grow/W15-W20_2026-27/SCI_G_W16B_Getting_The_Solid_Back_Do.html'
    w16b_claims = week_keys(blo.deck_statement_text(lhtml.fromstring((ROOT / w16b).read_text())))
    check('W16B RED PROOF, real tree: its title-stage "Spring 1 · Week 16" is a claim its row (Spr1·W2) does not bind',
          (blo.title_claim_conflict(bdoc['entries'][w16b], w16b_claims) or '').startswith(
              "the deck's title stage states ['Spr1·W16']"))
    check('and a title-stage claim equal to the row is no conflict',
          blo.title_claim_conflict(bdoc['entries'][w16b], ['Spr1·W2']) is None)

    # W14L1 -> unchanged (the ruling's control): its own lesson-config names its spine cell, so
    # derive() proves it by the explicit-cell deck limb before any Science limb is tried.
    w14 = next((ROOT / 'Science_Teesside/Launch/W14-W15_2026-27').glob('SCI_L_W14L1_*.html'))
    w14rel = w14.relative_to(ROOT).as_posix()
    cfg = json.loads(lhtml.fromstring(w14.read_text()).xpath('//script[@id="lesson-config"]/text()')[0])
    check('CONTROL, real tree: SCI_L_W14L1 is proved by its explicit cell, so no Science limb is reached',
          blo.explicit_cell_holds(cfg.get('source', {}), cells, evidence[w14rel]['evidence']))

    # Ruling 4, the EXCLUSION (review of the PR head): a held deck on a batch list is taken out by
    # derivation and the rest proceeds; the list is never edited by hand to make a run go through.
    kept, excluded = exclude_held({'Science_Teesside/B/w12.html': '1' * 64, 'Science_Teesside/B/x.html': '2' * 64}, hb)
    check('HELD: exclude_held drops exactly the held deck, names its record, and keeps the rest',
          kept == {'Science_Teesside/B/x.html': '2' * 64}
          and excluded == {'Science_Teesside/B/w12.html': '_sx3/RELEASE_LEDGER.md R-GAPS'})
    check('HELD RED PROOF: with nothing held, nothing is excluded',
          exclude_held({'Science_Teesside/B/w12.html': '1' * 64}, {}) == ({'Science_Teesside/B/w12.html': '1' * 64}, {}))

    # THE WIRING, through derive() itself on moved bytes (review of the PR head: the W9L1, W16B,
    # title-stage and fence proofs above test the pure helpers, and derive() is what decides).
    # Each deck's real bytes gain one comment in memory -- the tree is never written.
    w9l1 = 'Science_Teesside/Launch/W8-W13_2026-27/SCI_L_W9L1_Cell_Cycle_Introduce.html'
    w4a = 'Science_Teesside/Build/v3_40min/SCI_B_W4A_Muscles_Explore.html'
    released_all = [(x['path'], x['heldWeek']) for x in fence['released']['paths']]
    fenced_all = [x['path'] for x in fence['fenced']]
    # The re-stamp expectation below uses the released deck no held record names: SCI_G_A2_W7A/W7B
    # are listed in _sx3/HELD.md, which the held derivation does not read (a question for Matt), so
    # a check must not entrench either answer. SCI_B_W13 is named by no held record.
    rel_fence = next(x for x, _ in released_all if 'SCI_B_W13_Where_did_this_material' in x)
    still = next(x for x in fenced_all if 'SCI_B_W11A_' in x)
    probe = [w9l1, w4a, w16b, w14rel] + [x for x, _ in released_all] + fenced_all
    moved = {q: (ROOT / q).read_bytes() + b'\n<!-- restamp self-test: bytes moved -->\n' for q in probe}
    d = blo.derive(moved)
    rows_p, refused, unres = set(d.get('scienceRowProofs', [])), d.get('scienceRefusals', {}), set(d['unresolvedTiming'])
    wk = lambda q: ['%s·W%d' % (w['term'], w['week']) for w in d['entries'][q]['weeks']]
    check('WIRING, derive(): SCI_L_W9L1 on moved bytes is proved by the Science row limb at Aut2·W1',
          w9l1 in rows_p and wk(w9l1) == ['Aut2·W1'])
    check('WIRING, derive(): SCI_B_W4A on moved bytes is proved by the row limb at Aut1·W4 (the title-stage reader)',
          w4a in rows_p and wk(w4a) == ['Aut1·W4'])
    check('WIRING RED PROOF, derive(): SCI_G_W16B on moved bytes is refused for its title-stage claim',
          w16b in unres and 'claim' in refused.get(w16b, {}) and w16b not in rows_p)
    check('WIRING, derive(): every released fence deck on moved bytes holds the week the fence records (%d)'
          % len(released_all), len(released_all) == 3 and all(x in rows_p and wk(x) == [w] for x, w in released_all))
    check('WIRING RED PROOF, derive(): every deck still fenced is unresolved on moved bytes, refused by the row limb (%d)'
          % len(fenced_all), len(fenced_all) == 3 and all(x in unres and 'row' in refused.get(x, {}) for x in fenced_all))
    check('WIRING RED PROOF, derive(): SCI_B_W11A keeps its row reason AND gains its title-stage claim (merged, never overwritten)',
          set(refused.get(still, {})) >= {'row', 'claim'})
    check('WIRING CONTROL, derive(): SCI_L_W14L1 on moved bytes is proved by its explicit cell, no Science limb',
          w14rel in d['refreshedSourceProofs'] and w14rel not in rows_p and w14rel not in refused)
    plan = [w9l1, w4a, w16b, rel_fence, still, w14rel]
    digests = {q: hashlib.sha256(moved[q]).hexdigest() for q in plan}
    e, r, n = restamp_plan(evidence, digests, digests.get, set(d['refreshedSourceProofs']), bdoc['entries'],
                           fenced_paths(), refused, held_paths())
    check('WIRING, restamp_plan on derive(): W9L1, B_W4A, released SCI_B_W13 and W14L1 are re-stamped',
          {x[0] for x in r} == {w9l1, w4a, rel_fence, w14rel})
    check('WIRING RED PROOF, restamp_plan on derive(): W16B (its claim) and the fenced deck are refused, by name',
          len(e) == 2 and any('claim' in x and w16b in x for x in e) and any('fenced' in x and still in x for x in e))

    # The recorded reason, not only the outcome: a row with no term·week and an evidence record that
    # projects nothing is refused by BOTH limbs, and the label limb is really tried (review of the PR
    # head: it was recorded "not tried: the evidence projects a week" for decks projecting nothing).
    limb, why = blo.science_limbs('S/a.html', {'S/a.html': {'weeks': []}}, 'd' * 64, 'd' * 64, [], set(),
                                  'Autumn 1 · Week 8')
    check('WIRING: with no projection the label limb is tried and says why it refuses, never "not tried"',
          limb is None and 'not tried' not in why.get('label', '') and 'Aut1·W8' in why.get('label', ''))
    check('and a null weeks field is an empty row, never a crash (science_row_keys)',
          blo.science_row_keys({'weeks': None}) == [] and blo.title_claim_conflict({'weeks': None}, []) is None)

    # CORRECTION #40, the committed planted-failure proof: last, so no rebinding can follow it.
    if not planted:
        child = subprocess.run([sys.executable, str(Path(__file__).resolve()), '--self-test'],
                               env={**os.environ, 'RESTAMP_SELFTEST_PLANT': '1'},
                               capture_output=True, text=True)
        check('CORRECTION #40 CONTROL: a failure planted before every `ok, why = ...` still fails the '
              'self-test (child: "self-test FAIL (1)", exit 1)',
              child.returncode == 1 and 'self-test FAIL (1)' in child.stdout)

    print('self-test ' + ('PASS' if not bad else f'FAIL ({bad})'))
    return 1 if bad else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument('--check', action='store_true')
    mode.add_argument('--write', action='store_true')
    mode.add_argument('--self-test', action='store_true')
    ap.add_argument('--decks', help='JSON mapping deck path -> reviewed new sha256. Required with --write.')
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    if args.check:
        return run_check()
    if not args.decks:
        ap.error('--write requires --decks: the reviewed deck list is never defaulted')
    return run_write(args.decks)


if __name__ == '__main__':
    sys.exit(main())
