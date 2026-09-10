#!/usr/bin/env python3
"""RW1-E §W · one identity line at the top of every print sheet.

W1: this is a PRINT-ONLY change. Print sections are screen-hidden, so the
rendered screen DOM delta stays at exactly the four items B6 permits. Enumerated
here as the separate fifth change rather than smuggled into one of the four.

W2: pupil sheets carry NO week token and NO date --
    pathway · subject · lesson title · route
"Week 8A" trips the relabeller's public-token gate, and putting it on eleven
pupil sheets would multiply the pre-existing B4 failure by eleven. B4 said
report, not worsen.

AND IT REMOVES A DATE THAT WAS ALREADY THERE. Three pupil arrival sheets emitted
"BUILD Science · Sugar Evidence: Read the Label · 19 October 2026 · Supported".
My own B3 check missed them: I grepped for "w/c 19 October 2026" and these carry
the date WITHOUT the "w/c". Seventh instance of the family, and the same shape --
a pattern narrower than the property it claimed to test.

W3: the four staff/teacher sheets keep their dated header. B3 is untouched; the
date stays staff-only.

The class is .science-meta, which is not invented here: the Science authoring
toolchain emits exactly this at _authoring/science_2026-27/_toolchain/build/
build_html.py:144, and the pack already carries its print CSS.
"""
import re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import pathways

ROUTE = {'supported': 'Supported', 'standard': 'Standard', 'stretch': 'Stretch'}
# W4: shared sheets omit the route rather than guessing one.
SHARED = {'all', '', None}


def date_re(pw):
    """The dates to strip, per pathway. Both the entity and the literal middot
    forms occur in these files, so both are matched -- and the date is matched
    INDEPENDENTLY of any 'w/c' prefix, because a check that assumed the prefix
    missed three pupil sheets that carry the bare date."""
    return re.compile('|'.join(pathways.need(pw, 'date_tokens')))


def line(which, route, pw, staff=False):
    pathway, subject, title = pathways.need(pw, 'identity', which)
    parts = ([('STAFF ANSWERS' if staff else None)] + [pathway, subject, title]
             + [ROUTE.get(route)])
    return ('<p class="science-meta">'
            + ' &middot; '.join(p for p in parts if p) + '</p>')


def apply(text, which, pw):
    """Returns (text, added, cleaned, normalised, stats).

    GW1-B R1: this function once reported "+0 added" as a success because its
    section pattern matched none of the sections it was supposed to be editing.
    A count with no denominator cannot tell "examined 16, none needed a change"
    from "examined 0". So it now returns what it examined, and the four outcome
    counts must reconcile to it exactly.
    """
    added = cleaned = normalised = 0
    stats = {'sections_examined': 0, 'staff_skipped': 0, 'pupil_sections': 0,
             'already_correct': 0}
    out, pos = [], 0
    DATE = date_re(pw)
    # NOT class="print-section": four of the sixteen carry a second class
    # (organiser-paper, exit-paper, mk-print) and an exact-string match skipped
    # every one of them, reporting "+0 added" as a success. Token match, in any
    # attribute order -- the same rule parity.py's cls() helper exists to enforce,
    # which I had already written and did not use here.
    SECTION = re.compile(r'<section\b(?=[^>]*\bclass="[^"]*(?<![-\w])print-section(?![-\w])[^"]*")([^>]*)>')
    for m in SECTION.finditer(text):
        stats['sections_examined'] += 1
        attrs = m.group(1)
        route = (re.search(r'data-print-route="([^"]*)"', attrs).group(1)
                 if re.search(r'data-print-route="([^"]*)"', attrs) else '')
        staff = route == 'staff' or 'mk-print' in attrs
        end = text.find('</section>', m.end())
        body = text[m.end():end]
        meta = re.search(r'<p class="science-meta">(.*?)</p>', body, re.S)
        if staff:
            stats['staff_skipped'] += 1
            new_body = body                      # W3: staff sheets untouched
        elif (stats.__setitem__('pupil_sections', stats['pupil_sections'] + 1)
              or meta is None):
            new_body = line(which, route, pw) + body  # W: the four with no identity
            added += 1
        else:
            before = meta.group(0)
            after = line(which, route, pw)
            if DATE.search(before):
                cleaned += 1
            elif before != after:
                normalised += 1
            else:
                stats['already_correct'] += 1
            new_body = body[:meta.start()] + after + body[meta.end():]
        out.append(text[pos:m.end()]); out.append(new_body); pos = end
    out.append(text[pos:])
    # The reconciliation IS the denominator check. If these do not add up, the
    # pattern is seeing sections it is not accounting for, which is exactly the
    # failure this function shipped once.
    accounted = added + cleaned + normalised + stats['already_correct']
    assert accounted == stats['pupil_sections'], (
        'print identity did not account for every pupil section: '
        '%d accounted vs %d pupil sections of %d examined'
        % (accounted, stats['pupil_sections'], stats['sections_examined']))
    assert stats['sections_examined'] > 0, (
        'print identity examined ZERO print sections -- a denominator of zero '
        'is a failure, not a pass')
    return ''.join(out), added, cleaned, normalised, stats
