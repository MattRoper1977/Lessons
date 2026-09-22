#!/usr/bin/env python3
"""ORDER HUM-T / STOP-R2 -- make a page's IMPLIED <head> and <body> explicit.

The estate's usage adapter (domain-split/usage_discovery.py::inject) finds where to put
the usage furniture by looking for the literal strings </head> and </body>. HTML5 lets a
document leave both elements implied:

    <!doctype html><html lang="en-GB"><meta charset><title><style><h1>...</html>

is a WHOLE document -- the parser inserts head and body itself -- but it carries neither
closing tag, so the adapter refuses it. Wrapping such a page in a second document is not a
repair: it nests one document inside another. The repair is to write down the tags the page
already implies, moving not one byte of content.

WHAT IT INSERTS, and nothing else:
    <head>    immediately after the page's own <html ...> tag
    </head>   immediately before the first element that is not head content
    <body>    in the same place, immediately after </head>
    </body>   immediately before the page's own closing </html>

A page that already writes <head>...</head><body>...</body> is returned byte-identical, so
running the tool twice is running it once. A page with an explicit <body> but an implied
<head> gains only the two head tags.

REFUSED by name: a page with no <html> tag; a page with more than one <html> or </html>;
a page whose head and body cannot be told apart by the parser.

THE ORACLE. lxml parses the bytes before and again after. The two documents must serialise
identically -- the parser inserts the same implied head and body the tool writes down, so an
exact repair is invisible to it and any real edit is not.
"""
from __future__ import annotations

import argparse
import hashlib
import re
import sys
from pathlib import Path

from lxml import html as LH

HEAD_CONTENT = {'meta', 'title', 'style', 'link', 'base', 'script', 'noscript', 'template'}
HTML_OPEN = re.compile(r'<html\b[^>]*>', re.I)
HTML_CLOSE = re.compile(r'</html\s*>', re.I)
ELEMENT = re.compile(r'<([a-zA-Z][a-zA-Z0-9-]*)\b')


class Refuse(Exception):
    """A page this tool will not touch. Never repaired, always named."""


def has_explicit(text: str) -> tuple:
    low = text.lower()
    return ('</head>' in low, '</body>' in low)


def _first_body_offset(text: str, start: int) -> int:
    """Offset of the first element after `start` that is not head content.

    Walks only element start-tags, skipping the contents of <style>/<script>/<title>, so a
    <h1> written inside a stylesheet comment cannot be mistaken for the start of the body.
    """
    i = start
    low = text.lower()
    while True:
        m = ELEMENT.search(text, i)
        if not m:
            raise Refuse('no element after <html>: this is not a page with a body to mark')
        name = m.group(1).lower()
        if name not in HEAD_CONTENT:
            return m.start()
        close = '</%s>' % name
        j = low.find(close, m.end())
        i = m.end() if j < 0 else j + len(close)


def repair(text: str):
    """Pure. Returns (marked-up text, [(offset in the ORIGINAL, tag), ...]).

    The offsets are what makes this checkable: check() undoes exactly these insertions and
    demands the original back, so nothing can move without being seen.
    """
    head_closed, body_closed = has_explicit(text)
    if head_closed and body_closed:
        return text, []
    if len(HTML_OPEN.findall(text)) != 1 or len(HTML_CLOSE.findall(text)) != 1:
        raise Refuse('a page this tool marks up has exactly one <html> and one </html>')
    open_tag = HTML_OPEN.search(text)
    close_tag = HTML_CLOSE.search(text)

    inserts = []
    if not head_closed:
        inserts.append((open_tag.end(), '<head>'))
        boundary = (text.lower().find('<body') if body_closed
                    else _first_body_offset(text, open_tag.end()))
        if boundary < 0:
            raise Refuse('the page closes </body> but never opens <body>')
        if boundary <= open_tag.end():
            raise Refuse('the body starts before the head: this page is not what it seems')
        inserts.append((boundary, '</head>' if body_closed else '</head><body>'))
    if not body_closed:
        inserts.append((close_tag.start(), '</body>'))

    out, last = [], 0
    for offset, tag in sorted(inserts):
        out.append(text[last:offset]); out.append(tag); last = offset
    out.append(text[last:])
    return ''.join(out), inserts


def serialised(text: str) -> bytes:
    """lxml's view. NOT the oracle -- kept only to show why it cannot be.

    libxml2 does not implement HTML5's head/body inference: given a document that leaves both
    implied it puts the flow content INSIDE <head> and never opens <body> at all. It therefore
    calls an exact mark-up a change, and would call a nesting wrap no change. The oracle for
    this tool is Chromium, the parser that actually serves these pages: load the bytes before
    and after and compare document.doctype, head.innerHTML, body.innerHTML, title and the
    element count. That runs in dom_oracle.mjs, beside this file.
    """
    return LH.tostring(LH.document_fromstring(text), encoding='utf-8')


ALLOWED = ('<head>', '</head>', '<body>', '</body>', '</head><body>')


def check(before: str, after: str, inserts) -> None:
    """Raise unless `after` is `before` with ONLY the named tags written down.

    Undoing the recorded insertions must give back the original byte for byte. Nothing else
    is permitted to move, and no document furniture may be duplicated -- which is exactly
    what a wrap does, and what this tool must never do.
    """
    for _, tag in inserts:
        if tag not in ALLOWED:
            raise Refuse('the tool wrote something that is not a head or body tag: ' + tag)
    rebuilt, last = [], 0
    for offset, tag in sorted(inserts):
        rebuilt.append(before[last:offset]); rebuilt.append(tag); last = offset
    rebuilt.append(before[last:])
    if ''.join(rebuilt) != after:
        raise Refuse('bytes moved outside the recorded insertions')
    for mark in ('<!doctype', '<html', '</html>', '<head', '</head>', '<body', '</body>'):
        want = before.lower().count(mark) + sum(t.lower().count(mark) for _, t in inserts)
        if after.lower().count(mark) != want:
            raise Refuse('document furniture was duplicated or lost: ' + mark)
    for mark in ('<!doctype', '<html', '</html>'):
        if after.lower().count(mark) != before.lower().count(mark):
            raise Refuse('document furniture was duplicated: ' + mark)
    if after.lower().count('</head>') != 1 or after.lower().count('</body>') != 1:
        raise Refuse('the result must close head and body exactly once')


def self_test() -> int:
    bad = 0

    def ok(name, cond):
        nonlocal bad
        print('  [%s] %s' % ('ok' if cond else 'FAIL', name))
        bad += 0 if cond else 1

    implied = ('<!doctype html><html lang="en-GB"><meta charset="utf-8">'
               '<title>Week 1</title><style>h1{color:red}</style>'
               '<h1>Our school</h1><p>Text.</p></html>')
    out, ins = repair(implied)
    ok('an implied head and body are written down',
       '<html lang="en-GB"><head><meta' in out and '</style></head><body><h1>' in out
       and '</p></body></html>' in out)
    check(implied, out, ins)
    # Why Chromium, and not lxml, is the oracle. On the simplest shape libxml2 agrees; on the
    # shape the real Knowledge Organisers use -- a <button> as the first flow content -- it puts
    # that button inside <head>, never opens <body>, and so calls an EXACT mark-up a change.
    # A parser that cannot see the boundary cannot judge a tool that writes the boundary down.
    real = ('<!doctype html><html lang="en-GB"><meta charset="utf-8"><title>t</title>'
            '<style>p{}</style><button onclick="print()">P</button><section>b</section></html>')
    real_out, real_ins = repair(real)
    check(real, real_out, real_ins)
    ok('RED PROOF (lxml is not the oracle): libxml2 agrees on a simple page and disagrees on '
       'the real one, so Chromium judges the real pages',
       serialised(implied) == serialised(out) and serialised(real) != serialised(real_out))
    ok('RED PROOF (no duplication): one doctype, one <html>, one </html> after',
       out.lower().count('<!doctype') == 1 and out.lower().count('</html>') == 1)
    ok('RED PROOF (idempotent): running twice is running once', repair(out)[0] == out)
    ok('RED PROOF (no-op by hash): a page with both tags is byte-identical',
       hashlib.sha256(repair(out)[0].encode()).hexdigest()
       == hashlib.sha256(out.encode()).hexdigest())

    body_only = ('<!doctype html><html lang="en-GB"><meta charset="utf-8"><title>KO</title>'
                 '<style>p{}</style><body><article><h1>Our school</h1></article>'
                 '</body></html>')
    out2, ins2 = repair(body_only)
    check(body_only, out2, ins2)
    ok('a page with an explicit body gains only the two head tags',
       out2.count('<body>') == 1 and '</style></head><body>' in out2)

    whole = '<!doctype html><html><head><title>x</title></head><body><p>y</p></body></html>'
    ok('a whole document is returned byte-identical', repair(whole)[0] == whole)

    try:
        repair('<h2>no document at all</h2>'); ok('RED PROOF (no <html>): refused', False)
    except Refuse as e:
        ok('RED PROOF (no <html>): refused -- ' + str(e)[:40], True)
    try:
        repair('<html><p>a</p></html><html><p>b</p></html>')
        ok('RED PROOF (two documents): refused', False)
    except Refuse:
        ok('RED PROOF (two documents in one file): refused', True)
    try:
        o, i2 = repair(implied)
        check(implied, o.replace('Our school', 'Our street'), i2)
        ok('RED PROOF (content edited): refused', False)
    except Refuse as e:
        ok('RED PROOF (content edited): refused -- ' + str(e)[:34], True)
    try:
        nested = ('<!doctype html><html><head><title>t</title></head><body>'
                  + implied + '</body></html>')
        check(implied, nested, ins); ok('RED PROOF (nested document): refused', False)
    except Refuse:
        ok('RED PROOF (a wrap, not a mark-up): nesting is refused', True)
    style_trap = ('<!doctype html><html><meta charset="utf-8">'
                  '<style>/* <h1> in a comment */ h1{}</style><h1>Real</h1></html>')
    out3, ins3 = repair(style_trap)
    check(style_trap, out3, ins3)
    ok('an element named inside <style> does not start the body',
       '</style></head><body><h1>Real</h1>' in out3)
    print('explicit_document_tags self-test: %s' % ('PASS' if not bad else 'FAIL (%d)' % bad))
    return 1 if bad else 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('paths', nargs='*', type=Path)
    ap.add_argument('--write', action='store_true')
    ap.add_argument('--self-test', action='store_true')
    args = ap.parse_args(argv)
    if args.self_test:
        return self_test()
    moved = 0
    for p in args.paths:
        before = p.read_text()
        after, ins = repair(before)
        check(before, after, ins)
        if after != before:
            moved += 1
            if args.write:
                p.write_text(after)
    print('%d of %d page(s) %s' % (moved, len(args.paths),
                                   'marked up' if args.write else 'would be marked up'))
    return 0


if __name__ == '__main__':
    sys.exit(main())
