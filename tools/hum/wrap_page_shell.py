#!/usr/bin/env python3
"""ADDENDUM 3 v3 — give a served page the HTML shell the estate's publication requires.

RULED by Matt Roper, 2026-09-22 (STOP-R, option 2). The Site's usage adapter refuses any page
it must inject furniture into unless the page is a whole HTML document:

    ValueError: Usage adapter needs an HTML shell: .../GROW_W27-W39_2026-27/START_HERE.html
    (domain-split/usage_discovery.py, inject(): '</head>' not in text or '</body>' not in text)

Fifty of the seventy served pages in the three Summer 1 pathway trees arrived as fragments; all
ninety-two pages of the estate's existing Humanities pathway dirs are whole documents. This tool
makes the fifty whole WITHOUT touching a byte of what they say:

    <!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>TITLE</title></head><body>THE ORIGINAL BYTES, UNCHANGED</body></html>

TITLE is read from the page's own first heading; where the page has none, it falls back to the
lesson id its filename carries. A page that already has a shell is left BYTE-IDENTICAL, so the
tool is idempotent and running it twice is running it once.

    wrap_page_shell.py <path>... [--write]   wrap the shell-less pages among these
    wrap_page_shell.py --self-test           the red proofs
"""
from __future__ import annotations
import argparse, hashlib, re, sys
from pathlib import Path

HEAD = ('<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        '<title>%s</title>\n</head>\n<body>\n')
TAIL = '\n</body>\n</html>\n'
HEADING = re.compile(r'<h([1-6])\b[^>]*>(.*?)</h\1>', re.S | re.I)
TAG = re.compile(r'<[^>]+>')
LESSON_ID = re.compile(r'((?:BUILD|GROW|LAUNCH)_SU1_W\d{2})')


def has_shell(text: str) -> bool:
    """The publication's own test, quoted: a page is whole when it closes head AND body."""
    return '</head>' in text and '</body>' in text


def title_for(text: str, path: Path) -> str:
    """The page's own first heading, or - where it has none - the lesson id its filename carries."""
    m = HEADING.search(text)
    if m:
        words = ' '.join(TAG.sub(' ', m.group(2)).split())
        if words:
            return words
    m = LESSON_ID.search(path.name)
    return m.group(1) if m else path.stem


def wrap(text: str, path: Path) -> str:
    """Pure. A page with a shell is returned unchanged; a fragment is placed, byte for byte,
    inside a whole document."""
    if has_shell(text):
        return text
    return HEAD % title_for(text, path) + text + TAIL


def body_of(text: str) -> str:
    i, j = text.find('<body>'), text.rfind('</body>')
    return text[i + len('<body>'):j] if i >= 0 and j > i else text


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('paths', nargs='*', type=Path)
    parser.add_argument('--write', action='store_true')
    parser.add_argument('--self-test', action='store_true')
    args = parser.parse_args(argv)
    if args.self_test:
        return self_test()
    wrapped = skipped = 0
    for p in args.paths:
        before = p.read_text(encoding='utf-8', errors='replace')
        after = wrap(before, p)
        if after == before:
            skipped += 1
            continue
        assert before in after, 'the original bytes must survive verbatim: ' + str(p)
        if args.write:
            p.write_text(after, encoding='utf-8')
        wrapped += 1
        print('  %-72s %s -> %s  %7d -> %7d' % (
            str(p)[-72:], hashlib.sha256(before.encode()).hexdigest()[:12],
            hashlib.sha256(after.encode()).hexdigest()[:12], len(before.encode()), len(after.encode())))
    print('[%s] %d page(s) wrapped, %d already whole' % ('DONE' if args.write else 'DRY', wrapped, skipped))
    return 0


def self_test() -> int:
    bad = 0

    def check(name, cond):
        nonlocal bad
        print('  [%s] %s' % ('ok' if cond else 'FAIL', name))
        bad += 0 if cond else 1

    frag = '<h2>Words to use</h2>\n<table><tr><td>river</td></tr></table>\n'
    p = Path('GROW_SU1_W03_Knowledge_Organiser.html')
    out = wrap(frag, p)
    check('a fragment becomes a whole document', has_shell(out))
    check('the title is the page\'s own first heading', '<title>Words to use</title>' in out)
    check('RED PROOF: not one byte of the page changes inside <body>', body_of(out).strip() == frag.strip())
    check('the original bytes survive verbatim', frag in out)

    shelled = '<!DOCTYPE html><html><head><title>Already</title></head><body><p>x</p></body></html>'
    check('RED PROOF (no-op by hash): a page that already has a shell is byte-identical',
          hashlib.sha256(wrap(shelled, p).encode()).hexdigest()
          == hashlib.sha256(shelled.encode()).hexdigest())
    check('RED PROOF (idempotent): running twice is running once',
          wrap(wrap(frag, p), p) == wrap(frag, p))
    headless = '<table><tr><td>no heading at all</td></tr></table>'
    check('RED PROOF (fallback title): a page with no heading takes its lesson id',
          '<title>GROW_SU1_W03</title>' in wrap(headless, p))
    check('a page with no heading and no lesson id in its name takes its stem',
          '<title>Sources_and_checks</title>' in wrap(headless, Path('Sources_and_checks.html')))
    check('half a shell is not a shell: </head> alone does not count',
          not has_shell('<head></head><p>x</p>') and has_shell('<head></head><body></body>'))
    print('wrap_page_shell self-test: %s' % ('PASS' if not bad else 'FAIL (%d)' % bad))
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
