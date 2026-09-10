#!/usr/bin/env python3
"""tools/measure_size.py - a size is a number AND a unit, and the unit is not optional.

WHY THIS EXISTS

D30 stated four sizes. Two were wrong, and the two that were wrong were exactly
the two that could be:

    loose GROW_Week_01_Interactive.html   24,008 B claimed   24,013 actual
    zip   GROW_Week_01_Interactive.html   33,712 B claimed   33,725 actual
    loose GROW_Week_01_Teaching_Slides.pptx  47,188 B        correct
    zip   GROW_Week_01_Teaching_Slides.pptx  59,661 B        correct

Both HTML figures were `len(text)`. Both .pptx figures were right, because a
binary file has no text mode to be misread in. Every md5 matched, so nothing was
misidentified -- it was a REPORTING defect, not a content defect. But GC1's gates
compare byte sizes, so a character count wearing a "B" would have failed a gate
for a reason that did not exist, or passed one that should have failed.

CRLF was not the cause and checking for it would not have caught this: both files
have zero CRLF pairs. The gap is multi-byte UTF-8 -- five such characters in one
file, thirteen in the other. A "collapse line endings" theory explains the shape
of the error and gets the cause wrong, which is worse than no theory.

WHAT IT ENFORCES

    size_b(path)      -> (n, 'B')      reads bytes, always
    size_chars(path)  -> (n, 'chars')  reads text, always
    label(n, unit)    -> "24,013 B"    refuses any unit but those two
    report(path)      -> both, side by side, so a gap is visible rather than latent

A text-mode read CANNOT be labelled B. That is a raise, not a warning, because a
warning is a thing you scroll past at one in the morning.

USAGE
  python3 tools/measure_size.py <path> [<path> ...]
  python3 tools/measure_size.py --self-test
"""
import argparse
import hashlib
import os
import sys

BYTES, CHARS = 'B', 'chars'
UNITS = (BYTES, CHARS)


class UnitError(ValueError):
    """Raised when a measurement is about to be labelled with a unit it is not."""


def label(n, unit):
    if unit not in UNITS:
        raise UnitError('unit must be one of %r, got %r' % (UNITS, unit))
    return '{:,} {}'.format(n, unit)


def size_b(path):
    """The number of BYTES on disk. Opened binary so there is no decoding to get wrong."""
    with open(path, 'rb') as fh:
        return len(fh.read()), BYTES


def size_chars(path, encoding='utf-8'):
    """The number of CHARACTERS after decoding. Never a byte count, and never labelled B."""
    with open(path, encoding=encoding) as fh:
        return len(fh.read()), CHARS


def measured(n, unit, claimed_unit):
    """Label a measurement, refusing to relabel a text-mode read as bytes.

    This is the whole point of the module. size_chars returns 'chars'; asking for
    'B' back is the D30 mistake, so it raises rather than obliging.
    """
    if unit == CHARS and claimed_unit == BYTES:
        raise UnitError('a text-mode read is not a byte measurement (D33): '
                        'got %d characters, refusing to label them B' % n)
    if unit != claimed_unit:
        raise UnitError('measured in %s, asked to label %s' % (unit, claimed_unit))
    return label(n, claimed_unit)


def report(path, encoding='utf-8'):
    """Both readings side by side, plus the md5 that settles identity.

    Printing both is deliberate. A single number invites the reader to assume the
    unit; two numbers that differ make the question unavoidable, and two that
    agree say the file is pure ASCII and the distinction did not bite this time.
    """
    nb, _ = size_b(path)
    try:
        nc, _ = size_chars(path, encoding)
    except (UnicodeDecodeError, ValueError):
        nc = None                     # a binary file has no text mode to be misread in
    with open(path, 'rb') as fh:
        raw = fh.read()
    return {
        'path': path,
        'bytes': nb,
        'chars': nc,
        'gap': (nb - nc) if nc is not None else None,
        'crlf': raw.count(b'\r\n'),
        'md5': hashlib.md5(raw).hexdigest(),
        'label': label(nb, BYTES),
    }


def self_test():
    import tempfile
    n, bad = [0], []
    def want(name, cond):
        n[0] += 1
        print(('  PASS  ' if cond else '  FAIL  ') + name)
        if not cond: bad.append(name)

    def raises(fn):
        try:
            fn(); return False
        except UnitError:
            return True

    want('label formats with a thousands separator', label(24013, BYTES) == '24,013 B')
    want('label accepts chars', label(24008, CHARS) == '24,008 chars')
    want('label refuses an invented unit', raises(lambda: label(1, 'bytes')))
    want('label refuses an empty unit', raises(lambda: label(1, '')))

    want('a text-mode read cannot be labelled B (the D30 mistake)',
         raises(lambda: measured(24008, CHARS, BYTES)))
    try:
        measured(24008, CHARS, BYTES)
        msg = ''
    except UnitError as e:
        msg = str(e)
    want('  ... and the message cites D33 and says what it refused',
         'D33' in msg and '24008' in msg.replace(',', ''))

    want('a byte read labelled B is fine', measured(24013, BYTES, BYTES) == '24,013 B')
    want('a char read labelled chars is fine', measured(24008, CHARS, CHARS) == '24,008 chars')
    want('bytes asked to be chars is also refused', raises(lambda: measured(1, BYTES, CHARS)))

    with tempfile.TemporaryDirectory() as d:
        # Five multi-byte characters: the exact shape of the loose Week 01 file,
        # where 24,013 bytes read as 24,008 characters.
        p = os.path.join(d, 'multibyte.html')
        text = 'x' * 24003 + '—' * 5          # 24008 chars, 24003 + 15 = 24018 bytes
        open(p, 'w', encoding='utf-8').write(text)
        r = report(p)
        want('report gives both readings', r['bytes'] != r['chars'])
        want('  ... chars is the smaller of the two', r['chars'] < r['bytes'])
        want('  ... and the gap is the multi-byte overhead', r['gap'] == r['bytes'] - r['chars'])
        want('  ... with zero CRLF, so line endings are excluded as the cause', r['crlf'] == 0)
        want('  ... and the default label is BYTES', r['label'].endswith(' B'))
        want('size_b and size_chars disagree on this file',
             size_b(p)[0] != size_chars(p)[0])

        # A pure-ASCII file: the two agree, and the distinction is invisible. This is
        # why the defect survived - most files never show it.
        q = os.path.join(d, 'ascii.txt')
        open(q, 'w', encoding='utf-8').write('hello')
        want('on pure ASCII the two readings agree, which is how this hid',
             report(q)['gap'] == 0)

        # A binary file has no text mode to be misread in, which is why both .pptx
        # figures in D30 were right.
        b = os.path.join(d, 'thing.bin')
        open(b, 'wb').write(bytes(range(256)) * 4)
        rb = report(b)
        want('a binary file reports bytes and no char count', rb['chars'] is None and rb['bytes'] == 1024)
        want('  ... and still reports an md5 for identity', len(rb['md5']) == 32)

    print('\n%d checks, %d failed' % (n[0], len(bad)))
    for x in bad: print('  FAILED:', x)
    return 1 if bad else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('paths', nargs='*')
    ap.add_argument('--self-test', action='store_true', dest='self_test')
    a = ap.parse_args()
    if a.self_test:
        sys.exit(self_test())
    if not a.paths:
        print('give one or more paths, or --self-test', file=sys.stderr)
        sys.exit(2)
    print('%-52s %12s %12s %7s %s' % ('path', 'bytes', 'chars', 'gap', 'md5'))
    for p in a.paths:
        r = report(p)
        print('%-52s %12s %12s %7s %s'
              % (os.path.basename(p)[-52:], label(r['bytes'], BYTES),
                 label(r['chars'], CHARS) if r['chars'] is not None else '-',
                 r['gap'] if r['gap'] is not None else '-', r['md5'][:10]))


if __name__ == '__main__':
    main()
