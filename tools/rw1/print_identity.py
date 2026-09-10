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
import re

LESSON = {'A': ('BUILD', 'Science', 'Sugar Evidence'),
          'B': ('BUILD', 'Science', 'Body Science Checkpoint')}
ROUTE = {'supported': 'Supported', 'standard': 'Standard', 'stretch': 'Stretch'}
# W4: shared sheets omit the route rather than guessing one.
SHARED = {'all', '', None}
DATE = re.compile(r'\s*&middot;\s*19 October 2026|\s*·\s*19 October 2026')


def line(which, route, staff=False):
    pathway, subject, title = LESSON[which]
    parts = ([('STAFF ANSWERS' if staff else None)] + [pathway, subject, title]
             + [ROUTE.get(route)])
    return ('<p class="science-meta">'
            + ' &middot; '.join(p for p in parts if p) + '</p>')


def apply(text, which):
    added = cleaned = normalised = 0
    out, pos = [], 0
    # NOT class="print-section": four of the sixteen carry a second class
    # (organiser-paper, exit-paper, mk-print) and an exact-string match skipped
    # every one of them, reporting "+0 added" as a success. Token match, in any
    # attribute order -- the same rule parity.py's cls() helper exists to enforce,
    # which I had already written and did not use here.
    SECTION = re.compile(r'<section\b(?=[^>]*\bclass="[^"]*(?<![-\w])print-section(?![-\w])[^"]*")([^>]*)>')
    for m in SECTION.finditer(text):
        attrs = m.group(1)
        route = (re.search(r'data-print-route="([^"]*)"', attrs).group(1)
                 if re.search(r'data-print-route="([^"]*)"', attrs) else '')
        staff = route == 'staff' or 'mk-print' in attrs
        end = text.find('</section>', m.end())
        body = text[m.end():end]
        meta = re.search(r'<p class="science-meta">(.*?)</p>', body, re.S)
        if staff:
            new_body = body                      # W3: staff sheets untouched
        elif meta is None:
            new_body = line(which, route) + body  # W: the four with no identity
            added += 1
        else:
            before = meta.group(0)
            after = line(which, route)
            if DATE.search(before):
                cleaned += 1
            elif before != after:
                normalised += 1
            new_body = body[:meta.start()] + after + body[meta.end():]
        out.append(text[pos:m.end()]); out.append(new_body); pos = end
    out.append(text[pos:])
    return ''.join(out), added, cleaned, normalised
