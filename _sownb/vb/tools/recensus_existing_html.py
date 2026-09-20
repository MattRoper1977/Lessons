#!/usr/bin/env python3
"""Re-census `blobSha256` for named `existingHtml` entries of CALENDAR_SPINE.json.

WHY THIS EXISTS. `existingHtml[].blobSha256` records the bytes a deck had when it
was last censused. `tools/catalogue/build_catalogue.py` re-proves a deck's workbook
binding when those bytes are unchanged:

    unchanged = sha256(file) == EXISTING[path]['blobSha256']
    ...
    if unchanged or outcomes or cell_labels or ... :
        terms = [the ruled term of the cells in contentCellReferences]

A release that changes a deck's bytes without re-censusing leaves that limb false.
The record still SHOWS the old answer, because it has not been regenerated since -
so nothing looks wrong until the next change forces a regeneration, and then the
term falls to "unspecified" and `build_lesson_order.py` asserts. Measured on
origin/main cbfbc70c: 254 of 529 entries stale; regenerating the catalogue there
drops the term on 14 LAUNCH W9-W13 decks and breaks build_lesson_order outright.

CENSUS, NOT RE-AUTHOR. This records what the bytes ARE. It derives no week, reads
no filename, and touches no ruling:

  * it writes ONLY `blobSha256`, and only on entries whose path is named on the
    command line - never a scan, never "all stale";
  * every digest is DERIVED from the file's bytes, never transcribed
    (instrument correction #6);
  * `calendar` / `termBlocks` / `termDates` / `ruledMapping` / `boundary` /
    `februaryBoundary` / `workbookCells` / `targets` and every other top-level key
    are asserted byte-equal afterwards;
  * within `existingHtml` every other field of every entry - `contentCellReferences`,
    `secondInstrumentEvidence`, `spineStatus`, `surface`, the readings - is asserted
    unchanged.

It does not resurrect `census_spine.py`, retired by VB-RUN13 R0 for deriving a
teaching week from a filename. No week is derived here at all, so `g27` has nothing
to flag: the paths are given, the digests come from bytes.

SURGICAL. CALENDAR_SPINE.json was written by a formatter that puts some nested
objects on one line, so `json.dumps` cannot reproduce it and a re-serialise would
rewrite all 60,437 lines. This replaces the 64 hex characters in place and then
PARSES the result and compares the whole structure, so the minimal diff is also a
proved one.

  recensus_existing_html.py --check PATH...
  recensus_existing_html.py --write PATH...
  recensus_existing_html.py --self-test
"""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SPINE = ROOT / "_sownb/CALENDAR_SPINE.json"
ARRAY_KEY = '"existingHtml": ['
HEX64 = re.compile(r'"blobSha256": "([0-9a-f]{64})"')
PATH_KEY = re.compile(r'"path": "((?:[^"\\]|\\.)*)"')


def digest_of(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def array_span(text: str):
    """The [start, end) offsets of the existingHtml array, by bracket count."""
    i = text.find(ARRAY_KEY)
    if i < 0:
        raise ValueError('REFUSED: no "existingHtml" array in the spine')
    if text.find(ARRAY_KEY, i + 1) >= 0:
        raise ValueError('REFUSED: more than one "existingHtml" key')
    start = i + len(ARRAY_KEY) - 1
    depth = 0
    for m in re.finditer(r'[\[\]]', text[start:]):
        depth += 1 if m.group(0) == '[' else -1
        if depth == 0:
            return start, start + m.end()
    raise ValueError('REFUSED: unclosed "existingHtml" array')


def locate(text: str, wanted):
    """For each wanted path, the (start, end) span of its blobSha256 hex digits.

    Anchored inside the existingHtml array only, so a path that also appears under
    `targets` or anywhere else cannot be matched by accident.
    """
    lo, hi = array_span(text)
    body = text[lo:hi]
    paths = [(m.start(), json.loads('"' + m.group(1) + '"')) for m in PATH_KEY.finditer(body)]
    if not paths:
        raise ValueError('REFUSED: existingHtml contains no "path" key')
    found, seen = {}, {}
    for idx, (off, p) in enumerate(paths):
        seen[p] = seen.get(p, 0) + 1
        if p not in wanted:
            continue
        nxt = paths[idx + 1][0] if idx + 1 < len(paths) else len(body)
        hits = list(HEX64.finditer(body, off, nxt))
        if len(hits) != 1:
            raise ValueError('REFUSED: %r has %d blobSha256 fields in its entry, expected 1'
                             % (p, len(hits)))
        found.setdefault(p, []).append((lo + hits[0].start(1), lo + hits[0].end(1)))
    for p in wanted:
        if p not in found:
            raise ValueError('REFUSED: %r is not an existingHtml entry' % p)
        if seen[p] > 1:
            raise ValueError('REFUSED: %r appears %d times in existingHtml; which entry is '
                             'meant is not derivable' % (p, seen[p]))
    return found


def verify(before_text: str, after_text: str, expected: dict, root: Path = ROOT):
    """Every difference must be exactly an expected blobSha256, and nothing else."""
    problems = []
    b, a = json.loads(before_text), json.loads(after_text)
    if set(b) != set(a):
        problems.append('top-level keys changed')
        return problems
    for k in b:
        if k == 'existingHtml':
            continue
        if b[k] != a[k]:
            problems.append('top-level key %r changed; this tool censuses existingHtml only' % k)
    eb, ea = b.get('existingHtml', []), a.get('existingHtml', [])
    if len(eb) != len(ea):
        problems.append('existingHtml length %d -> %d' % (len(eb), len(ea)))
        return problems
    changed = {}
    for x, y in zip(eb, ea):
        if x == y:
            continue
        diff = {k for k in set(x) | set(y) if x.get(k) != y.get(k)}
        if diff != {'blobSha256'}:
            problems.append('entry %r changed fields %s; only blobSha256 may move'
                            % (x.get('path'), sorted(diff)))
            continue
        changed[x.get('path')] = y['blobSha256']
    if changed != expected:
        problems.append('digests written %s != expected %s'
                        % (sorted(changed.items()), sorted(expected.items())))
    for p, d in changed.items():
        f = root / p
        if not f.is_file():
            problems.append('%r is not on disk' % p)
        elif digest_of(f) != d:
            problems.append('%r written digest is not the digest of its bytes' % p)
    return problems


def apply(text: str, wanted, root: Path):
    spans = locate(text, wanted)
    edits, expected, already = [], {}, []
    for p in wanted:
        f = root / p
        if not f.is_file():
            raise ValueError('REFUSED: %r is not on disk' % p)
        want = digest_of(f)
        (s, e), = spans[p]
        if text[s:e] == want:
            already.append(p)
            continue
        edits.append((s, e, want, text[s:e]))
        expected[p] = want
    out, last = [], 0
    for s, e, want, _old in sorted(edits):
        out.append(text[last:s])
        out.append(want)
        last = e
    out.append(text[last:])
    return ''.join(out), expected, already, {p: (o, w) for s, e, w, o in edits for p in [
        next(k for k, v in spans.items() if v[0][0] == s)]}


def run(paths, write):
    text = SPINE.read_text(encoding='utf-8')
    new, expected, already, moves = apply(text, list(dict.fromkeys(paths)), ROOT)
    print('SCOPE: %d path(s) named; %d already censused at their current bytes; %d to re-record'
          % (len(set(paths)), len(already), len(expected)))
    for p in already:
        print('   UNCHANGED %s' % p)
    for p, (old, want) in sorted(moves.items()):
        print('   %-8s %s\n            %s -> %s' % ('WRITE' if write else 'STALE', p, old[:16], want[:16]))
    if not expected:
        return 0
    problems = verify(text, new, expected, ROOT)
    if problems:
        for m in problems:
            print('   REFUSED %s' % m)
        return 1
    print('   verified: only those blobSha256 values differ; every other top-level key and '
          'every other existingHtml field is unchanged')
    if write:
        SPINE.write_text(new, encoding='utf-8')
        print('   written: %s' % SPINE)
    return 0


# ------------------------------------------------------------------ self-test
SPINE_FIXTURE = '''{
  "schemaVersion": 1,
  "calendar": {
    "termBlocks": {"Autumn1": [1, 7], "Autumn2": [8, 14]},
    "termDates": {"Autumn1": "2026-09-01"}
  },
  "ruledMapping": {"a": 1},
  "boundary": "ruled",
  "februaryBoundary": "ruled",
  "workbookCells": [
    {"reference": "'X'!C1", "termWeek": "Aut2 \\u00b7 W1"}
  ],
  "existingHtml": [
    {
      "path": "one.html",
      "contentCellReferences": ["'X'!C1"],
      "spineStatus": "ruled",
      "blobSha256": "%s",
      "secondInstrumentEvidence": {"manifestOutcome": "keep me"}
    },
    {
      "path": "two.html",
      "contentCellReferences": [],
      "spineStatus": "ruled",
      "blobSha256": "%s"
    }
  ],
  "targets": [{"path": "one.html", "note": "a path OUTSIDE existingHtml"}]
}
'''
ZERO = '0' * 64


def self_test():
    import tempfile
    problems = []

    def case(name, ok):
        print('  %s  %s' % ('PASS' if ok else 'FAIL', name))
        if not ok:
            problems.append(name)

    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        (root / 'one.html').write_text('ONE')
        (root / 'two.html').write_text('TWO')
        d1, d2 = digest_of(root / 'one.html'), digest_of(root / 'two.html')
        text = SPINE_FIXTURE % (ZERO, d2)

        new, expected, already, _m = apply(text, ['one.html'], root)
        case('a stale entry is re-recorded from the file bytes', expected == {'one.html': d1})
        case('an entry already at its current bytes is left alone', already == [])
        case('the verifier accepts that write', verify(text, new, expected, root) == [])
        case('the OTHER entry is untouched', json.loads(new)['existingHtml'][1]['blobSha256'] == d2)
        case('secondInstrumentEvidence survives',
             json.loads(new)['existingHtml'][0]['secondInstrumentEvidence'] == {'manifestOutcome': 'keep me'})
        case('the edit is exactly the digest, nothing reformatted',
             len(new) == len(text) and new != text and new.replace(d1, ZERO, 1) == text)

        _n2, e2, a2, _ = apply(new, ['one.html'], root)
        case('idempotent: a second run has nothing to do', e2 == {} and a2 == ['one.html'])

        try:
            apply(text, ['missing.html'], root)
            case('a path that is not an existingHtml entry refuses', False)
        except ValueError as e:
            case('a path that is not an existingHtml entry refuses', 'not an existingHtml entry' in str(e))

        try:
            apply(text.replace('"targets": [{"path": "one.html"', '"targets": [{"path": "three.html"'),
                  ['three.html'], root)
            case('a path present only OUTSIDE existingHtml refuses', False)
        except ValueError as e:
            case('a path present only OUTSIDE existingHtml refuses', 'not an existingHtml entry' in str(e))

        (root / 'two.html').unlink()
        try:
            apply(text, ['two.html'], root)
            case('a path missing on disk refuses', False)
        except ValueError as e:
            case('a path missing on disk refuses', 'not on disk' in str(e))
        (root / 'two.html').write_text('TWO')

        dup = text.replace('"path": "two.html"', '"path": "one.html"')
        try:
            apply(dup, ['one.html'], root)
            case('a duplicated path refuses rather than guessing', False)
        except ValueError as e:
            case('a duplicated path refuses rather than guessing', 'appears 2 times' in str(e))

        tampered = new.replace('"termDates": {"Autumn1": "2026-09-01"}',
                               '"termDates": {"Autumn1": "2026-09-02"}')
        case('a planted termDates change is caught by the verifier',
             any('termDates' in m or "'calendar'" in m for m in verify(text, tampered, expected, root)))

        t2 = new.replace('"spineStatus": "ruled"', '"spineStatus": "widened"', 1)
        case('a planted spineStatus change is caught by the verifier',
             any('spineStatus' in m for m in verify(text, t2, expected, root)))

        t3 = new.replace(d1, ZERO.replace('0', 'a'))
        case('a digest that is not the digest of the bytes is caught',
             verify(text, t3, expected, root) != [])

        t4 = new.replace('"workbookCells": [', '"workbookCells": [{"reference": "'"'"'X'"'"'!C2"},')
        case('a planted workbookCells change is caught by the verifier',
             any('workbookCells' in m for m in verify(text, t4, expected, root)))

    if problems:
        print('SELF-TEST FAIL:', problems)
        return 1
    print('SELF-TEST PASS: only the named entries move, only blobSha256 moves, every digest '
          'is derived from bytes, and every planted fault is refused')
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('paths', nargs='*')
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument('--check', action='store_true')
    g.add_argument('--write', action='store_true')
    g.add_argument('--self-test', action='store_true')
    a = ap.parse_args()
    if a.self_test:
        return self_test()
    if not a.paths:
        ap.error('name at least one existingHtml path')
    return run(a.paths, a.write)


if __name__ == '__main__':
    sys.exit(main())
