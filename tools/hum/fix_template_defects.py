#!/usr/bin/env python3
"""ORDER HUM-T — the two mechanical template defects released by ruling 5.

(a) THE BORROWED TITLE. Twelve RE decks carry another lesson's <title>, in three
    blocks of four. The fix is LISTED's rule: the title is the deck's own <h1>,
    keeping whatever pathway/subject suffix the deck already used.

(b) THE STRAY WORKED EXAMPLE. Four GROW RE decks carry "<i>the council minute</i>"
    in a pupil template cell. It belongs to the W16 Sources lesson the block was
    built from. Its sibling cells in the same table are blank, so the fix is to
    make it blank like them. Nothing is authored and nothing else is touched.

Repeated print-pack instructions are NOT touched. The order's test ("repeated
outside any row structure") does not separate residue from deliberate page
furniture — provenance notices, support lines and sheet headers repeat for good
reasons — so they stay Class B, report only.
"""
from __future__ import annotations
import html as ihtml
import json, re, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from deck_dom import parse, splice                                  # noqa: E402

TITLE_RX = re.compile(r'(<title\b[^>]*>)(.*?)(</title>)', re.S | re.I)
COUNCIL_RX = re.compile(r'<i\s*>\s*the council minute\s*</i>', re.I)


def own_h1(html: str) -> str | None:
    doc = parse(html)
    h = doc.find(lambda n: n.tag == 'h1')
    return h[0].inner_text().strip() if h else None


def _norm(s: str) -> str:
    return re.sub(r'[^a-z0-9]+', ' ', ihtml.unescape(s or '').lower()).strip()


def fix_title(html: str):
    """title := the deck's own h1, keeping the deck's own trailing suffix.

    A title that ALREADY carries its own h1 is correct and is left untouched —
    that is the same test the census used to find the twelve."""
    m = TITLE_RX.search(html)
    h1 = own_h1(html)
    if not m or not h1:
        return html, None
    old = m.group(2).strip()
    nt, nh = _norm(old), _norm(h1)
    if not nh or nh in nt or nt in nh:
        return html, None                      # already correct
    suffix = ''
    if '·' in old:
        suffix = ' ·' + old.rsplit('·', 1)[1].rstrip()
    new = ihtml.escape(h1, quote=False) + suffix
    if new.strip() == old:
        return html, None
    return html[:m.start(2)] + new + html[m.end(2):], (old, new)


def fix_council(html: str):
    """The stray example becomes a blank cell — but ONLY where it is an orphan.

    In the W16 Sources lesson the same words are one cell of a COMPLETE worked
    example: every cell in that row is filled. In the four RE decks built from
    that template only this one cell came across and its siblings are blank.
    That difference is the whole test, so the genuine example is never touched."""
    if not COUNCIL_RX.search(html):
        return html, 0
    doc = parse(html)
    edits = []
    for n in doc.walk():
        if n.tag != 'i' or n.inner_text().strip().lower() != 'the council minute':
            continue
        cell = n
        while cell is not None and cell.tag not in ('td', 'th'):
            cell = cell.parent
        rowel = cell
        while rowel is not None and rowel.tag != 'tr':
            rowel = rowel.parent
        if cell is None or rowel is None:
            continue
        # A complete worked example has EVERY cell in italics. An orphan fragment
        # sits alone in a row whose other cells are plain labels or blank.
        siblings = [c for c in rowel.children if c.tag in ('td', 'th') and c is not cell]
        italic_siblings = [c for c in siblings
                           if any(x.tag == 'i' and x.inner_text().strip() for x in c.children)]
        if italic_siblings:
            continue                     # a complete worked example — leave it
        edits.append((n.start, n.end, ' '))
    if not edits:
        return html, 0
    return splice(html, edits), len(edits)


def fix_short_rows(html: str):
    """(c) THE TWO-CELL EVIDENCE ROW. Eight decks carry a three-column pupil
    evidence table whose first body row has only two cells, so the third column
    ("My reason, in my words") has nowhere to write. The missing cells are added,
    empty, exactly matching the row's own sibling cells.

    A row that spans the table with colspan is CORRECT and is left alone — that is
    how "No sites sampled yet" is written, and it is not a defect."""
    doc = parse(html)
    edits = []
    added = 0
    for t in doc.walk():
        if t.tag != 'table':
            continue
        header = None
        for tr in t.find(lambda n: n.tag == 'tr'):
            cells = [c for c in tr.children if c.tag in ('td', 'th')]
            if not cells:
                continue
            width = sum(int(c.attrs.get('colspan') or 1) for c in cells)
            if header is None and any(c.tag == 'th' for c in cells):
                header = width
                continue
            if header is None or width >= header:
                continue
            if any(c.attrs.get('colspan') for c in cells):
                continue                      # a deliberate spanning row
            last = cells[-1]
            filler = ' '.join('<td>&nbsp;</td>' for _ in range(header - width))
            edits.append((last.end, last.end, filler))
            added += header - width
    if not edits:
        return html, 0
    return splice(html, edits), added


def fix(html: str):
    html, t = fix_title(html)
    html, c = fix_council(html)
    html, r = fix_short_rows(html)
    return html, {'title': t, 'council_cells': c, 'cells_added': r}


def self_test() -> bool:
    checks = []
    a = ('<html><head><title>Wrong Lesson · GROW Humanities</title></head>'
         '<body><h1>Eight Nights, One Lamp</h1></body></html>')
    out, info = fix(a)
    checks.append(('title becomes the deck\'s own h1, suffix kept',
                   '<title>Eight Nights, One Lamp · GROW Humanities</title>' in out))
    checks.append(('the change is reported', info['title'] is not None))
    b = '<html><head><title>Right · X</title></head><body><h1>Right</h1></body></html>'
    out2, info2 = fix(b)
    checks.append(('a correct title is left alone', out2 == b and info2['title'] is None))
    c = '<table><tr><td><i>the council minute</i></td><td> </td></tr></table>'
    out3, info3 = fix_council(c)
    checks.append(('the stray example is blanked', '<i>' not in out3 and info3 == 1))
    d = '<td>a real council minute from 1894</td>'
    out4, n4 = fix_council(d)
    checks.append(('genuine prose mentioning a council minute is untouched',
                   out4 == d and n4 == 0))
    whole = ('<table><tr><td><i>the council changed what it did</i></td>'
             '<td><i>the council minute</i></td><td><i>it records a decision</i></td></tr></table>')
    out8, n8 = fix_council(whole)
    checks.append(('a COMPLETE worked example row is left intact', out8 == whole and n8 == 0))
    short = ('<table><tr><th>A</th><th>B</th><th>C</th></tr>'
             '<tr><td>label</td><td>x</td></tr></table>')
    out10, n10 = fix_short_rows(short)
    checks.append(('a short row gains the missing cell',
                   n10 == 1 and out10.count('<td>') == 3))
    span = ('<table><tr><th>A</th><th>B</th><th>C</th></tr>'
            '<tr><td colspan="3">No sites sampled yet</td></tr></table>')
    out11, n11 = fix_short_rows(span)
    checks.append(('a deliberate spanning row is left alone', out11 == span and n11 == 0))
    full = ('<table><tr><th>A</th><th>B</th></tr><tr><td>x</td><td>y</td></tr></table>')
    out12, n12 = fix_short_rows(full)
    checks.append(('a complete row is left alone', out12 == full and n12 == 0))
    orphan = ('<table><tr><td>Three details from the approved source</td>'
              '<td><i>the council minute</i></td><td> </td></tr></table>')
    out9, n9 = fix_council(orphan)
    checks.append(('an orphan fragment IS blanked', n9 == 1 and '<i>' not in out9))
    f = ('<html><head><title>LAUNCH · Lesson 2 of 6 · Settlement &amp; Urbanisation</title>'
         '</head><body><h1>Settlement &amp; Urbanisation</h1></body></html>')
    out6, info6 = fix(f)
    checks.append(('a title that already carries its own h1 is untouched',
                   out6 == f and info6['title'] is None))
    g = ('<html><head><title>Other Lesson · GROW</title></head>'
         '<body><h1>Fish &amp; Chips</h1></body></html>')
    out7, _ = fix(g)
    checks.append(('an ampersand in the h1 is re-escaped in the title',
                   '<title>Fish &amp; Chips · GROW</title>' in out7))
    e = '<html><head><title>No Heading</title></head><body><p>x</p></body></html>'
    out5, info5 = fix(e)
    checks.append(('a deck with no h1 is left alone', out5 == e))
    ok = True
    for name, good in checks:
        print(('  PASS ' if good else '  FAIL ') + name)
        ok = ok and good
    return ok


if __name__ == '__main__':
    if '--self-test' in sys.argv:
        sys.exit(0 if self_test() else 1)
    root = Path(sys.argv[1])
    rec = json.loads((root / 'tools/catalogue/HUMANITIES_STRAND.json').read_text())
    write = '--write' in sys.argv
    changed = 0
    for r in rec['lessons']:
        p = root / r['path']
        src = p.read_text(errors='replace')
        out, info = fix(src)
        if out != src:
            changed += 1
            print('%-6s W%-3s %-11s %s' % (r['pathway'], r['week'], r['strand'], p.name))
            if info['title']:
                print('    title  %r -> %r' % info['title'])
            if info['council_cells']:
                print('    blanked %d stray example cell(s)' % info['council_cells'])
            if info['cells_added']:
                print('    added %d missing evidence cell(s)' % info['cells_added'])
            if write:
                p.write_text(out)
    print('%d decks %s' % (changed, 'rewritten' if write else 'would change (dry run)'))
