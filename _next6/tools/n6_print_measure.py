#!/usr/bin/env python3
"""N6 · s24-print-renders — stage 2: measure the rendered paper.

Two measurements, both on the raster, neither on the DOM:

  ink coverage   per page, the fraction of pixels that are not white. A slide
                 left at `height:91%` inside a paginated container emits a real
                 A4 page carrying nothing; it is indistinguishable from a working
                 page to any `@media print` presence check and obvious here.

  sentinel text  the learner-confirmation block is looked for in text extracted
                 from the PDF, i.e. in what the printer would put on paper. The
                 August run's grep said 75/75 while the paper said 51/75.

Usage: n6_print_measure.py <renderdir> [--json out.json]
"""
import sys, os, json, glob

import numpy as np
import pypdfium2 as pdfium

# A page carrying a single line of 9pt text sits near 0.4%. A page carrying
# nothing at all is 0.000%. The band between is where a broken slide lands.
#
# The two tests are OR, not AND, and that matters. A slide left at `height:91%`
# prints as an EMPTY BORDERED BOX: zero characters, but ~0.7% ink from the
# border alone, which sails past any ink-only threshold. Requiring both
# conditions let exactly that page through. Either emptiness condemns a page.
# Measured against the clean estate this is a wide margin, not a hair trigger:
# the thinnest real page carries 94 characters and 0.66% ink.
BLANK_INK   = 0.0020   # < 0.20% of pixels inked, OR
BLANK_CHARS = 24       # fewer than this many extracted characters
DPI         = 96

SENTINELS = ['I confirm this is my own work', 'Learner confirmation']


def measure(pdf_path):
    doc = pdfium.PdfDocument(pdf_path)
    pages = []
    alltext = []
    scale = DPI / 72.0
    for i in range(len(doc)):
        pg = doc[i]
        txt = pg.get_textpage().get_text_range() or ''
        alltext.append(txt)
        bmp = pg.render(scale=scale, draw_annots=False)
        arr = bmp.to_numpy()                       # H x W x C, RGB(A), uint8
        grey = arr[:, :, :3].min(axis=2)           # darkest channel = ink in any hue
        h, w = grey.shape
        # "not white" with a tolerance for antialiasing haze
        inked = int((grey < 246).sum())
        cov = inked / float(w * h) if w * h else 0.0
        nchar = len(txt.strip())
        pages.append({'page': i + 1, 'ink': round(cov, 6), 'chars': nchar,
                      'blank': cov < BLANK_INK or nchar < BLANK_CHARS})
    doc.close()
    joined = '\n'.join(alltext)
    return pages, joined


def main():
    rd = sys.argv[1]
    outjson = None
    if '--json' in sys.argv:
        outjson = sys.argv[sys.argv.index('--json') + 1]
    man = json.load(open(os.path.join(rd, 'render_manifest.json')))
    rows = []
    for m in man:
        if m.get('error'):
            rows.append({'src': m['src'], 'error': m['error'], 'pages': [],
                         'sentinel': False, 'npages': 0, 'blanks': 0,
                         'external': m.get('external', [])})
            continue
        pages, text = measure(m['pdf'])
        low = text.lower().replace(' ', ' ')
        sent = any(s.lower() in low for s in SENTINELS)
        rows.append({'src': m['src'], 'error': None, 'pages': pages,
                     'sentinel': sent, 'npages': len(pages),
                     'blanks': sum(1 for p in pages if p['blank']),
                     'external': m.get('external', [])})
    if outjson:
        json.dump(rows, open(outjson, 'w'), indent=1)
    # summary to stdout
    nb = sum(r['blanks'] for r in rows)
    ns = sum(1 for r in rows if r['sentinel'])
    print('surfaces rendered : %d' % len(rows))
    print('sentinel on paper : %d/%d' % (ns, len(rows)))
    print('blank/near-blank  : %d pages' % nb)
    for r in rows:
        if r['error']:
            print('  RENDER-ERROR %s :: %s' % (os.path.basename(r['src']), r['error']))
    return 0


if __name__ == '__main__':
    sys.exit(main())
