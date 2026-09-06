#!/usr/bin/env python3
"""ORDER N6-M §M3 — assert that a patch left the PRINTED PAGE unchanged.

WHY NOT cmp ON THE PDF. Chromium writes a per-run identifier into the file, so
two renders of the SAME unmodified input differ at byte 459 while being the same
size and the same document. Measured, not assumed — that is what a byte compare
of the PDF actually tests, and it fails on a no-op.

So the assertion is made on the paper the PDF describes, which is what "print
byte-identical" has to mean here:

  · the page COUNT is identical
  · the extracted TEXT of every page is identical, character for character
  · the RASTER of every page is identical, hashed at 96 dpi

Raster identity is the strong one: it catches a moved rule, a changed margin or
a font substitution that text extraction would miss entirely.

Usage: n6m_print_equal.py <before-render-dir> <after-render-dir>
"""
import hashlib, json, os, sys

import numpy as np
import pypdfium2 as pdfium

DPI = 96


def fingerprint(pdf):
    doc = pdfium.PdfDocument(pdf)
    pages = []
    for i in range(len(doc)):
        pg = doc[i]
        txt = pg.get_textpage().get_text_range() or ''
        arr = pg.render(scale=DPI / 72.0, grayscale=True).to_numpy()
        pages.append({'text': hashlib.sha256(txt.encode()).hexdigest(),
                      'raster': hashlib.sha256(np.ascontiguousarray(arr)).hexdigest(),
                      'chars': len(txt)})
    doc.close()
    return pages


def load(d):
    """Key by FULL source path, not basename.

    Keying by basename silently drops every surface whose name repeats across
    packs — START_HERE.html, index.html, CURRICULUM_ALIGNMENT and friends. It
    made a 159-file comparison report 148 and call itself complete. A comparator
    that quietly narrows its own population is worse than one that fails.
    """
    man = json.load(open(os.path.join(d, 'render_manifest.json')))
    return {os.path.realpath(m['src']): m['pdf'] for m in man if not m.get('error')}


def main():
    before, after = sys.argv[1], sys.argv[2]
    b, a = load(before), load(after)
    common = sorted(set(b) & set(a))
    only_b, only_a = sorted(set(b) - set(a)), sorted(set(a) - set(b))
    bad = []
    for k in common:
        fb, fa = fingerprint(b[k]), fingerprint(a[k])
        if len(fb) != len(fa):
            bad.append((k, 'page count %d -> %d' % (len(fb), len(fa))))
            continue
        for i, (x, y) in enumerate(zip(fb, fa), 1):
            if x['text'] != y['text']:
                bad.append((k, 'page %d TEXT differs (%d -> %d chars)'
                            % (i, x['chars'], y['chars'])))
            elif x['raster'] != y['raster']:
                bad.append((k, 'page %d RASTER differs (text identical)' % i))
    print('surfaces compared      : %d' % len(common))
    print('page-for-page identical: %d' % (len(common) - len({k for k, _ in bad})))
    print('differing              : %d' % len({k for k, _ in bad}))
    for k in only_b:
        print('  ONLY IN BEFORE %s' % k)
    for k in only_a:
        print('  ONLY IN AFTER  %s' % k)
    for k, why in bad[:20]:
        print('  DIFFERS %s :: %s' % (k, why))
    return 1 if (bad or only_a or only_b) else 0


if __name__ == '__main__':
    sys.exit(main())
