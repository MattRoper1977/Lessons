#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ORDER N6-I · I1/I2 — `s24-print-renders`: the estate's print RENDER gate.

Why this gate exists, stated as plainly as it can be.

Two print defects shipped green through checks that looked reasonable:

  * The learner-confirmation block was inserted into all 24 BUILD_ASDAN decks
    and printed in none of them. It landed OUTSIDE `<section class="print-pack">`,
    which `@media print{body>*:not(.print-pack){display:none!important}}` hides.
    `grep` said 75/75. A print render said 51/75.
  * The LAUNCH_ASDAN print donor revealed all nine slides but left each at
    `height:91%` inside a clipped `body{overflow:hidden}`. That prints nine
    almost-empty pages, and is green to any "does the file contain @media print"
    check.

Both classes of defect are invisible to element-presence checks and to
`checkVisibility()`. Only the rendered artefact shows them. So this gate does not
inspect the DOM at all. It reads the PDF Chromium actually produced and measures:

  A. the learner-confirmation block is in the PRINTED TEXT of every named surface
  B. no page is blank or near-blank — measured on the RASTERISED page as ink
     coverage and as tint-invariant local variation, plus the page's own text
     length; never as element presence
  C. every deck's page count is at least the number of print units THE DOCUMENT
     ITSELF declares, printed as a table

Pixels are the load-bearing measurement. A page carrying a hidden 91%-tall slide
has a page box and no marks; a page carrying a signature table has marks.
Counting elements cannot tell those apart. Counting pixels can.

Two pixel measurements, because one has a blind spot — see `measure_pdf`. Ink is
coverage against white and is the right number for an ordinary sheet; a themed
background makes every pixel non-white and silences it, so `edge` measures local
variation instead, which a flat region of any colour cannot fake.

`s24_render.mjs --a11y` renders the same set under the estate's accessibility
invariants (reduced motion, dark scheme, the decks' own Calm Mode and High
Contrast). A print gate that only measures the default appearance is half a gate.

Dependencies: `pypdfium2` (rasterise + text), `numpy` (pixel arithmetic). When
either is missing the gate prints MEASUREMENT INVALID and never PASS — the same
contract `s23-no-learner-names` uses when its reference list is absent. A gate
that cannot measure must not report green. For a pack that HAS a print surface
`gates.py` escalates that to a failure: nothing withheld, so unmeasured is red.

Usage
  python3 s24_print_renders.py --packs <root> [<root>...] # derive the surface set, render, measure
  python3 s24_print_renders.py --renders <dir>            # measure an existing render set
  python3 s24_print_renders.py --render-set <manifest>    # render a listed set, then measure
  python3 s24_print_renders.py --self-test                # prove the measurement both ways
"""
import argparse
import collections
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

# ------------------------------------------------------------------ contract
# The printed strings that prove the learner-confirmation block reached paper.
# Taken from the ported T2-4 block itself, not retyped from the order.
LC_REQUIRED = ['Learner confirmation',
               'I confirm this is my own work.',
               'Learner name',
               'Signature']

# The source marker the N2 port leaves behind. Its presence is the SOURCE's own
# promise that this surface carries a learner signature block.
LC_MARKER = '<!--n6-learner-confirm:v1-->'

# Two different questions, and conflating them is how the original defect hid.
#
#   DELIVERY  — does a surface whose source carries the block actually PRINT it?
#               Derived from the file: if the marker is in the bytes, the words
#               must be on the paper. This is exactly the defect that shipped —
#               present in all 24 decks, printed in none.
#
#   COVERAGE  — is the block on every surface that is supposed to have one?
#               This cannot be derived from the files, because a surface that
#               lost the block would simply stop being asked about. It needs a
#               declared expectation, which is what --expect supplies and what
#               _next6/evidence/S24_EVIDENCE_SURFACES.txt commits to the repo.
#
# Delivery is always checked. Coverage is checked when an expectation is given,
# and its absence is reported rather than passed over: a run with no expectation
# file proves delivery only, and says so.
#
# The packs that are NOT evidence packs — Science, Humanities — were never
# specified to carry a learner signature. Demanding one of them would be the
# gate inventing a requirement, so a surface with no marker and no expectation
# entry is not LC-checked. It is still checked for blank pages and page count.


def source_promises_lc(path):
    try:
        return LC_MARKER in open(path, encoding='utf-8', errors='replace').read()
    except OSError:
        return False

# A page is NEAR-BLANK when it carries essentially no marks AND essentially no
# text. Both halves are required: a full-page background wash is not text but is
# not blank either, and a page of white-on-white text has characters but no ink.
#
# WHERE THESE NUMBERS COME FROM, and what they cannot do.
#
# Measured over the 812-page corpus, the bottom of the ink distribution is a
# CONTINUUM, not two clean clusters:
#
#     0.061% / 10 chars  orphaned clause      <- defect
#     0.129% / 20 chars  "and systems, not blame."
#     0.148% / 23 chars  orphaned clause
#     0.244% / 38 chars  orphaned clause
#     0.379% / 61 chars  orphaned sentence    <- still the same defect
#     0.498% / 86 chars  orphaned sentence    <- still the same defect
#     ----------------------------------------- largest gap in the bottom 40
#     0.757% / 76 chars  THE SIGNATURE PAGE   <- legitimate, sparse ON PURPOSE
#
# The awkward fact is that ink cannot separate "sparse on purpose" from "sparse
# by accident", and neither can character count: the legitimate signature page
# carries FEWER characters (76) than an orphan sheet it must not be confused
# with (86). A signature table is meant to be mostly white.
#
# So the floors are set where a failure is unambiguous and the margin to the
# sparsest LEGITIMATE page is nearly 2x, and the grey band above them is
# REPORTED rather than silently passed. Moving the hard floor up to 0.6% would
# catch two more real orphans and would also sit 1.26x from the signature page —
# close enough that a font substitution on another machine could red a clean
# tree. A standing gate that cries wolf gets switched off.
#
# Read the WARN list. Four pages failed this gate before the I1 fix; six were
# sparse. The fix cleared all six.
INK_FLOOR = 0.004       # 0.4% of the page's pixels carry any mark at all
EDGE_FLOOR = 0.008      # 0.8% local variation — the tint-invariant half, which
                        # keeps working when a themed background defeats INK_FLOOR
CHAR_FLOOR = 40         # non-whitespace characters in the page's text layer
INK_WARN = 0.010        # reported, not failed: the grey band above the floor
EDGE_WARN = 0.016
CHAR_WARN = 120
RASTER_SCALE = 1.0      # 72 dpi — enough to see a rule; ~595x842 px for A4

# Assertion 3 — "page count per deck is within a sane band".
#
# The band a surface is held to is the one the DOCUMENT DECLARES ABOUT ITSELF:
# every `.print-page` inside `.print-pack` that is visible in print media, or,
# on the deck chassis that has no print pack, every visible `.slide`. A print
# stylesheet that puts each unit on its own sheet cannot honestly produce fewer
# pages than it has units.
#
# This replaced a per-pack table of hard-coded bands, and it replaced it because
# that table failed during this order's own red-proof. A LAUNCH deck reverted to
# the naive donor-only port collapsed from ten printed pages to two — nine
# slides that reached no sheet at all — and the table let it pass, because the
# perturbed copy sat at a path the table's regex did not recognise and fell
# through to a permissive default. A gate whose scope depends on a directory
# name is a gate that goes quiet when a tree is copied. The document's own
# count cannot fall through.
#
# ABS_MAX is a runaway backstop only: not a claim about any pack, just a limit
# past which something has gone wrong enough to look at.
ABS_MAX = 60
UNIT_SLACK = 0            # a unit may overflow onto extra sheets; it may never
                          # occupy fewer than one

# ORDER N6-M — the ceiling, and why the floor alone was not enough.
#
# The band was [units, ABS_MAX]: a floor and a runaway backstop, no ceiling. That
# is exactly wide enough to miss the defect ORDER N6-F found. With N6-F's print-fit
# reverted, BUILD_ASDAN_A2_CON_W1 prints FOUR sheets from THREE declared units and
# sits inside [3, 60], so the gate passed a deck that had regained the overflow.
#
# It hid for a second reason worth recording: N6-I's orphans/widows control is
# also in these decks now, and it keeps the spilled sheet carrying four lines
# rather than a ten-character fragment. So the overflow no longer produces a
# near-blank page either. Each fix conceals the other's defect class from the
# check that found it. Neither gate reds without this ceiling.
#
# The ceiling applies to the DEFAULT variant only. Route filters and the
# accessibility variants legitimately reflow — larger type and Calm Mode spacing
# can push a unit onto a second sheet, and holding those to the same number would
# red a clean tree for being accessible.
UNIT_OVER_SLACK = 0       # default variant: a deck prints the units it declares


def band_for_record(rec, pages):
    """Return (kind, low, high, why) for one rendered variant."""
    d = rec.get('declared') or {}
    units = d.get('units') or 0
    kind = d.get('unitKind', 'none')
    if units:
        if rec.get('isDefault', True):
            hi = units + UNIT_OVER_SLACK
            why = ('%d visible %s unit(s) declared by the document; the default '
                   'variant prints the units it declares' % (units, kind))
        else:
            hi = ABS_MAX
            why = ('%d visible %s unit(s) declared by the document; non-default '
                   'variant, ceiling relaxed (route filters and the accessibility '
                   'variants legitimately reflow)' % (units, kind))
        return (kind, units - UNIT_SLACK, hi, why)
    return ('unbanded', 1, ABS_MAX, 'no print unit declared; sanity band only')


# ------------------------------------------------------------------ measuring
def _deps():
    try:
        import pypdfium2  # noqa: F401
        import numpy      # noqa: F401
        return None
    except Exception as e:                                   # pragma: no cover
        return str(e)


def measure_pdf(path):
    """Return per-page {page, ink, dark, chars} for one PDF, plus its full text.

    `ink` is the fraction of rasterised pixels that are not white. `dark` is the
    fraction below mid-grey — it separates a page of real text from a page of
    faint tint. Both come from the rendered bitmap, never from the DOM.
    """
    import numpy as np
    import pypdfium2 as pdfium

    doc = pdfium.PdfDocument(path)
    pages, text_all = [], []
    for i in range(len(doc)):
        pg = doc[i]
        tp = pg.get_textpage()
        txt = tp.get_text_range()
        text_all.append(txt)
        bmp = pg.render(scale=RASTER_SCALE, grayscale=True)
        arr = np.asarray(bmp.to_pil().convert('L'), dtype=np.uint8)
        total = arr.size
        # TWO measurements, because one of them has a blind spot.
        #
        # `ink` is coverage against white: the order's wording, and the right
        # number for an ordinary sheet. It has a blind spot. Calm Mode sets
        # `body.calm{background:#F4F1E9}`, which outranks the print block's
        # `body{background:#fff}` on SPECIFICITY and so survives into print.
        # Printed with background graphics on, every sheet carries a full-page
        # cream wash: 84.3% of pixels are then "not white", and a sheet holding
        # an orphaned twenty-character clause measures as densely inked. Under
        # that mode the ink floor can never fire, and the --a11y pass would hand
        # back a hollow green.
        #
        # `edge` is tint-invariant: the share of pixels where the image changes
        # against its neighbour. A flat region contributes nothing WHATEVER ITS
        # COLOUR — white sheet, cream sheet, dark-mode sheet — while text and
        # rules contribute a lot. Measured over the corpus it separates the same
        # way ink does and keeps separating when ink cannot:
        #
        #     orphan sheets   edge 0.085% · 0.182% · 0.527% · 0.700%
        #     signature page  edge 1.258%   <- legitimate, 1.8x the worst orphan
        #     content pages   edge 6.4% · 12.7%
        #
        # A modal-background version of `ink` was tried first and rejected: a
        # BUILD_ASDAN sheet under Calm Mode has TWO large flat regions, the cream
        # body and the white print-page, so "differs from the commonest value"
        # counts the entire print-page as marks and reports 16-26%. Local
        # variation has no such failure mode.
        int16 = arr.astype(np.int16)
        dx = np.abs(np.diff(int16, axis=1))
        dy = np.abs(np.diff(int16, axis=0))
        emask = np.zeros(arr.shape, dtype=bool)
        emask[:, :-1] |= dx > 12
        emask[:-1, :] |= dy > 12
        edge = float(emask.sum()) / total
        flat_pg = re.sub(r'\s+', ' ', txt)
        pages.append({
            'page': i + 1,
            'edge': edge,
            # A signature page is SUPPOSED to be mostly white — ruled boxes and
            # four labels. Marking it as the page that carries the learner
            # confirmation is what lets the sparse report distinguish "sparse on
            # purpose" from "sparse by accident", which ink alone cannot do:
            # the legitimate signature page carries FEWER characters (76) than
            # an orphan sheet it must not be confused with (86).
            'isLC': all(k in flat_pg for k in LC_REQUIRED),
            'ink': float((arr < 250).sum()) / total,
            'dark': float((arr < 128).sum()) / total,
            'chars': len(re.sub(r'\s+', '', txt)),
            'px': [int(arr.shape[1]), int(arr.shape[0])],
        })
        tp.close()
    doc.close()
    return pages, '\n'.join(text_all)


def is_near_blank(pg):
    """Almost nothing on the sheet.

    A page must be text-poor AND mark-poor. Mark-poor is satisfied by EITHER
    measurement being under its floor: `ink` catches the ordinary case, `edge`
    catches it when a themed background has made every pixel non-white. Neither
    alone covers both, and requiring both would let Calm Mode veto the check.
    """
    if pg['chars'] >= CHAR_FLOOR:
        return False
    return pg['ink'] < INK_FLOOR or pg.get('edge', 1.0) < EDGE_FLOOR


def is_sparse(pg):
    """Above the failing floor, below what a page of content looks like.

    Not a failure. Printed so the grey band is visible to a human instead of
    being hidden by wherever the hard threshold happens to sit. The learner
    confirmation page is excluded: it is sparse by design, and leaving it in
    buries the two or three pages that are sparse by accident under ninety-nine
    that are not.
    """
    if pg.get('isLC'):
        return False
    if is_near_blank(pg) or pg['chars'] >= CHAR_WARN:
        return False
    return pg['ink'] < INK_WARN or pg.get('edge', 1.0) < EDGE_WARN


# ------------------------------------------------------------------ the gate
def run(renders_dir, require_lc=True, verbose=True, band_check=True, expect=None):
    """Measure a render set. Returns (name, ok_or_None, detail, rows, report).

    expect: iterable of surface paths that MUST print the learner-confirmation
    block (the coverage contract). None means delivery-only.
    """
    bad = _deps()
    if bad:
        print('MEASUREMENT INVALID: s24-print-renders needs pypdfium2 + numpy (%s)' % bad,
              file=sys.stderr)
        return ('G12 s24-print-renders', None,
                'MEASUREMENT INVALID — pypdfium2/numpy absent', [], {})

    idx_path = os.path.join(renders_dir, 'index.json')
    if not os.path.exists(idx_path):
        print('MEASUREMENT INVALID: no render index at %s' % idx_path, file=sys.stderr)
        return ('G12 s24-print-renders', None,
                'MEASUREMENT INVALID — render index absent', [], {})
    index = json.load(open(idx_path, encoding='utf-8'))

    expect_set = None
    if expect:
        expect_set = {os.path.normpath(e) for e in expect}

    rows, report = [], []
    lc_expected, lc_seen = set(), set()
    per_file = collections.defaultdict(list)
    for rec in index:
        if rec.get('variant') == 'ERROR' or not rec.get('pdf'):
            rows.append((rec['file'], 'RENDER ERROR', rec.get('error', '')))
            report.append({'file': rec['file'], 'variant': 'ERROR', 'ok': False,
                           'error': rec.get('error', '')})
            per_file[rec['file']].append(False)
            continue
        pdf = os.path.join(renders_dir, rec['pdf'])
        pages, text = measure_pdf(pdf)
        flat = re.sub(r'\s+', ' ', text)
        norm = os.path.normpath(rec['file'])
        in_expect = expect_set is not None and norm in expect_set
        promised = source_promises_lc(rec['file'])
        lc_applies = require_lc and (promised or in_expect)
        if lc_applies:
            lc_expected.add(rec['file'])
        missing = [s for s in LC_REQUIRED if s not in flat] if lc_applies else []
        if lc_applies and not missing:
            lc_seen.add(rec['file'])
        blanks = [p for p in pages if is_near_blank(p)]
        sparse = [p for p in pages if is_sparse(p)]
        fam, lo, hi, why = band_for_record(rec, pages)
        in_band = lo <= len(pages) <= hi

        ok = True
        if missing:
            ok = False
            rows.append((rec['file'], rec['variant'],
                         'learner-confirmation ABSENT from print: missing %s%s' %
                         (missing, ' (source carries the block)' if promised
                          else ' (declared in the expectation list)')))
        if blanks:
            ok = False
            rows.append((rec['file'], rec['variant'],
                         'near-blank pages %s (ink<%.1f%% or edge<%.1f%%, chars<%d)'
                         % ([b['page'] for b in blanks], INK_FLOOR * 100,
                            EDGE_FLOOR * 100, CHAR_FLOOR)))
        if band_check and not in_band:
            ok = False
            rows.append((rec['file'], rec['variant'],
                         '%d printed pages, expected %d-%d — %s'
                         % (len(pages), lo, hi, why)))
        per_file[rec['file']].append(ok)
        report.append({
            'file': rec['file'], 'variant': rec['variant'], 'route': rec.get('route'),
            'isDefault': rec.get('isDefault', True), 'family': fam,
            'declared': rec.get('declared'), 'bandWhy': why,
            'pages': len(pages), 'band': [lo, hi], 'inBand': in_band,
            'lcApplies': lc_applies, 'lcInSource': promised, 'lcExpected': in_expect,
            'lcMissing': missing, 'nearBlank': [b['page'] for b in blanks],
            'sparse': [{'page': p['page'], 'ink': p['ink'],
                        'edge': p.get('edge'), 'chars': p['chars']}
                       for p in sparse],
            'minInk': min((p['ink'] for p in pages), default=0.0),
            'medInk': (sorted(p['ink'] for p in pages)[len(pages) // 2] if pages else 0.0),
            'minChars': min((p['chars'] for p in pages), default=0),
            'totalChars': sum(p['chars'] for p in pages),
            'ok': ok, 'pageDetail': pages,
        })

    surfaces = len(per_file)
    clean = sum(1 for v in per_file.values() if all(v))
    total_pages = sum(r.get('pages', 0) for r in report)
    total_blank = sum(len(r.get('nearBlank', [])) for r in report)
    total_sparse = sum(len(r.get('sparse', [])) for r in report)

    # Coverage: every surface the expectation list names must have been rendered
    # AND must print the block. A named surface that never appeared in the render
    # set is a red — a renamed or deleted evidence surface must not go quiet.
    rendered = {os.path.normpath(r['file']) for r in report}
    unrendered = sorted(expect_set - rendered) if expect_set is not None else []
    for u in unrendered:
        rows.append((u, 'MISSING', 'named in the expectation list but not rendered'))

    lc_n, lc_ok = len(lc_expected), len(lc_seen)
    lc_txt = ('%d/%d' % (lc_ok, lc_n)) if lc_n else 'n/a (no surface promises one)'
    cov = (' · coverage contract %d surfaces' % len(expect_set)) if expect_set is not None \
        else ' · DELIVERY ONLY (no --expect list; coverage unproven)'
    detail = ('%d surfaces / %d renders / %d pages · learner-confirmation %s · '
              'near-blank pages %d · sparse (reported, not failed) %d%s'
              % (surfaces, len(report), total_pages, lc_txt, total_blank,
                 total_sparse, cov))
    ok = clean == surfaces and surfaces > 0 and not unrendered
    if verbose:
        print_table(report)
    return ('G12 s24-print-renders', ok, detail, rows,
            {'surfaces': surfaces, 'renders': len(report), 'pages': total_pages,
             'lcOk': lc_ok, 'lcExpected': lc_n, 'lcCoverage': (
                 len(expect_set) if expect_set is not None else None),
             'unrendered': unrendered,
             'nearBlank': total_blank, 'sparse': total_sparse, 'clean': clean,
             'inkWarn': INK_WARN, 'charWarn': CHAR_WARN,
             'inkFloor': INK_FLOOR, 'charFloor': CHAR_FLOOR, 'rows': report})


def print_table(report):
    by_file = collections.OrderedDict()
    for r in report:
        by_file.setdefault(r['file'], []).append(r)
    print('%-58s %-10s %5s %-11s %8s %8s %6s %s'
          % ('surface', 'variant', 'pages', 'units>=', 'minInk', 'medInk', 'blank', 'LC'))
    print('-' * 132)
    for f, recs in by_file.items():
        short = f if len(f) <= 58 else '…' + f[-57:]
        for j, r in enumerate(recs):
            print('%-58s %-10s %5d %-11s %7.3f%% %7.3f%% %6d %s'
                  % (short if j == 0 else '', r['variant'], r['pages'],
                     '%d (%s)' % (r['band'][0], r['family']),
                     r['minInk'] * 100, r['medInk'] * 100,
                     len(r['nearBlank']),
                     ('MISSING' if r['lcMissing'] else
                      ('ok' if r.get('lcApplies') else '-'))))
    warn = [(r, p) for r in report for p in r.get('sparse', [])]
    if warn:
        print()
        print('SPARSE PAGES — reported, not failed (ink < %.1f%% or edge < %.1f%%, '
              'and < %d chars). Above the failing floor, below what a page of '
              'content looks like; read them.'
              % (INK_WARN * 100, EDGE_WARN * 100, CHAR_WARN))
        for r, p in sorted(warn, key=lambda w: w[1].get('edge', 0)):
            print('   ink %6.3f%%  edge %6.3f%%  %5d chars  %s [%s] p%d'
                  % (p['ink'] * 100, (p.get('edge') or 0) * 100, p['chars'],
                     os.path.basename(r['file']), r['variant'], p['page']))


# ------------------------------------------------------------------ rendering
def render(files, out_dir):
    """Render the given surfaces. Paths are made ABSOLUTE first, deliberately.

    ORDER N6-M: the sibling implementation of this gate (gates.g11) read 26/26
    one way and 0/26 another on the same correct tree, because the renderer
    resolves each path against ITS OWN working directory and was being handed
    repo-relative paths from a process running elsewhere. Every surface came
    back without its confirmation block and the gate reported a defect that was
    not there. It had only ever passed because the first harness happened to
    feed it absolute paths.

    This implementation inherits the same hazard by a different route — it runs
    node in the caller's cwd, so it is correct only while the caller happens to
    be at the repo root. Resolving here removes the dependency entirely. The
    failure it prevents is silent, total, and looks exactly like a real defect.
    """
    cmd = ['node', os.path.join(HERE, 's24_render.mjs'), '--out', out_dir] + \
        [os.path.abspath(f) for f in files]
    r = subprocess.run(cmd)
    return r.returncode == 0


# Surfaces are derived from the pack roots, never from "files that carry the
# block". Defining the population by the marker would be circular: a file that
# LOST the learner-confirmation block would silently drop out of the set the
# gate is meant to catch it in. This is the N2 patcher's own rule, restated —
# every HTML surface in the pack except the assessor-side and front-door pages,
# which are staff paperwork and carry no learner signature by design.
EXCLUDE = {'BUILD_ASDAN_AUT2_TEACHER_PLANNING_SOW.html', 'START_HERE.html',
           'START_HERE_BUILD_ASDAN_AUT2.html', 'STAFF_GUIDE.html', 'index.html',
           'PRINTABLE_RESOURCES.html'}


def surfaces_from_packs(roots):
    import glob as _glob
    out = []
    for r in roots:
        for p in sorted(_glob.glob(os.path.join(r, '**', '*.html'), recursive=True)):
            if os.path.basename(p) in EXCLUDE:
                continue
            out.append(p)
    return out


def surfaces_from_manifest(path):
    out = []
    for line in open(path, encoding='utf-8'):
        t = line.strip()
        if t and not t.startswith('#'):
            out.append(t)
    return out


# ------------------------------------------------------------------ self-test
def self_test():
    """Prove the measurement can go both ways on a synthetic pair.

    RED vector  — an A4 page with a 91%-tall hidden block and nothing else.
    GREEN vector — the same page with the learner-confirmation table visible.
    A gate whose red has never been seen is not evidence (N6 §4).
    """
    import tempfile
    bad = _deps()
    if bad:
        print('SELF-TEST INVALID: %s' % bad); return 2
    tmp = tempfile.mkdtemp(prefix='s24-selftest-')
    blankpg = ('<!doctype html><meta charset=utf-8><title>t</title>'
               '<style>@page{size:A4;margin:0}body{margin:0}'
               '.p{height:100vh;box-sizing:border-box;page-break-after:always}'
               '.p:last-child{page-break-after:auto}</style>'
               '<div class=p></div><div class=p></div>')
    inkpg = ('<!doctype html><meta charset=utf-8><title>t</title>'
             '<style>@page{size:A4;margin:0}body{margin:0}'
             '.p{height:100vh;box-sizing:border-box;page-break-after:always;padding:10mm}'
             '.p:last-child{page-break-after:auto}</style>'
             '<div class=p><p style="font-weight:800">5 &#183; Learner confirmation</p>'
             '<p>I confirm this is my own work.</p>'
             '<table style="width:100%;border-collapse:collapse">'
             '<tr><td style="padding:10px;border:1px solid #999;width:50%">Learner name (print)<br><br></td>'
             '<td style="padding:10px;border:1px solid #999">Signature<br><br></td></tr>'
             '<tr><td style="padding:10px;border:1px solid #999">Date<br><br></td>'
             '<td style="padding:10px;border:1px solid #999">&nbsp;</td></tr></table></div>')
    red = os.path.join(tmp, 'RED_blank.html'); open(red, 'w').write(blankpg)
    green = os.path.join(tmp, 'GREEN_signed.html'); open(green, 'w').write(inkpg)
    out = os.path.join(tmp, 'renders')
    if not render([red, green], out):
        print('SELF-TEST INVALID: renderer failed'); return 2
    idx = json.load(open(os.path.join(out, 'index.json')))
    verdict = {}
    for rec in idx:
        pages, text = measure_pdf(os.path.join(out, rec['pdf']))
        flat = re.sub(r'\s+', ' ', text)
        verdict[os.path.basename(rec['file'])] = {
            'pages': len(pages),
            'nearBlank': [p['page'] for p in pages if is_near_blank(p)],
            'lcMissing': [s for s in LC_REQUIRED if s not in flat],
            'ink': [round(p['ink'] * 100, 4) for p in pages],
        }
    r = verdict.get('RED_blank.html', {}); g = verdict.get('GREEN_signed.html', {})
    ok_red = bool(r.get('nearBlank')) and bool(r.get('lcMissing'))
    ok_green = not g.get('nearBlank') and not g.get('lcMissing')
    print(json.dumps(verdict, indent=1))
    print('RED   vector detected as blank + LC-missing : %s' % ('PASS' if ok_red else 'FAIL'))
    print('GREEN vector detected as inked + LC-present : %s' % ('PASS' if ok_green else 'FAIL'))
    return 0 if (ok_red and ok_green) else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--renders')
    ap.add_argument('--render-set')
    ap.add_argument('--packs', nargs='+')
    ap.add_argument('--expect', help='committed list of surfaces that MUST print the '
                                     'learner-confirmation block (the coverage contract)')
    ap.add_argument('--out')
    ap.add_argument('--json')
    ap.add_argument('--no-band', action='store_true')
    ap.add_argument('--no-lc', action='store_true')
    ap.add_argument('--self-test', action='store_true')
    a = ap.parse_args()

    if a.self_test:
        sys.exit(self_test())

    renders = a.renders
    files = None
    if a.render_set:
        files = surfaces_from_manifest(a.render_set)
    elif a.packs:
        files = surfaces_from_packs(a.packs)
    if files is not None:
        renders = a.out or os.path.join(os.getcwd(), '_s24_renders')
        print('rendering %d surfaces -> %s' % (len(files), renders))
        if not render(files, renders):
            print('RENDER FAILED'); sys.exit(2)
    if not renders:
        ap.error('need --packs, --renders or --render-set')

    expect = surfaces_from_manifest(a.expect) if a.expect else None
    name, ok, detail, rows, rep = run(renders, require_lc=not a.no_lc,
                                      band_check=not a.no_band, expect=expect)
    print()
    print('%-24s %s' % (name, detail))
    for r in rows:
        print('   · %s' % ' | '.join(str(x) for x in r))
    tag = 'PASS' if ok else ('MEASUREMENT INVALID' if ok is None else 'FAIL')
    print('===== %s: %s =====' % (name, tag))
    if a.json:
        json.dump(rep, open(a.json, 'w'), indent=1)
    sys.exit(0 if ok else (2 if ok is None else 1))


if __name__ == '__main__':
    main()
