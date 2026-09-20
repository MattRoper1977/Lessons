#!/usr/bin/env python3
"""A small offset-tracking HTML reader for the Humanities decks.

Why offsets: the adapter edits a deck by SPLICING the original bytes, never by
re-serialising a parse tree. Re-serialising would rewrite parts of the file the
order does not touch; splicing cannot.

VB-RUN13 R0 / g27: nothing here derives a teaching week from a path.
"""
from __future__ import annotations
import re
import html as _html
from html.parser import HTMLParser

VOID = {'area','base','br','col','embed','hr','img','input','link','meta',
        'param','source','track','wbr'}
RAW = {'script','style'}


class Node:
    __slots__ = ('tag','attrs','children','parent','text','start','open_end','end')

    def __init__(self, tag, attrs, parent, start):
        self.tag = tag; self.attrs = attrs; self.parent = parent
        self.children = []; self.text = []
        self.start = start        # offset of '<' of the start tag
        self.open_end = None      # offset just after the start tag's '>'
        self.end = None           # offset just after the end tag's '>'

    def classes(self):
        return set((self.attrs.get('class') or '').split())

    def walk(self):
        stack = [self]
        while stack:
            n = stack.pop()
            yield n
            stack.extend(reversed(n.children))

    def ancestors(self):
        a = []; p = self.parent
        while p is not None:
            a.append(p); p = p.parent
        return a

    def find(self, pred):
        return [n for n in self.walk() if pred(n)]

    def inner_text(self, skip=None):
        out = []
        stack = [(self, False)]
        while stack:
            n, _ = stack.pop()
            if n.tag in RAW:
                continue
            if skip is not None and n is not self and skip(n):
                continue
            out.extend(n.text)
            stack.extend((c, False) for c in reversed(n.children))
        t = _html.unescape(' '.join(out)).replace('\xa0', ' ')
        return re.sub(r'\s+', ' ', t).strip()


class _Reader(HTMLParser):
    def __init__(self, html):
        # convert_charrefs=True keeps a character reference inside its own text
        # run. With it False, "partner&#x27;s" arrived as three text nodes and the
        # join put spaces in: "partner ' s".
        super().__init__(convert_charrefs=True)
        self.html = html
        self._lines = [0]
        for m in re.finditer('\n', html):
            self._lines.append(m.end())
        self.root = Node('#root', {}, None, 0)
        self.cur = self.root

    def _off(self):
        line, col = self.getpos()
        return self._lines[line - 1] + col

    def handle_starttag(self, tag, attrs):
        a = {k.lower(): (v or '') for k, v in attrs}
        n = Node(tag, a, self.cur, self._off())
        n.open_end = self._off() + len(self.get_starttag_text() or '')
        self.cur.children.append(n)
        if tag not in VOID:
            self.cur = n
        else:
            n.end = n.open_end

    def handle_startendtag(self, tag, attrs):
        a = {k.lower(): (v or '') for k, v in attrs}
        n = Node(tag, a, self.cur, self._off())
        n.open_end = n.end = self._off() + len(self.get_starttag_text() or '')
        self.cur.children.append(n)

    def handle_endtag(self, tag):
        end = self._off() + len(tag) + 3   # '</' + tag + '>'
        n = self.cur
        while n is not self.root and n.tag != tag:
            n = n.parent
        if n is self.root:
            return
        n.end = end
        if n.parent is not None:
            self.cur = n.parent

    def handle_data(self, d):
        if d.strip():
            self.cur.text.append(d.strip())


def parse(html: str) -> Node:
    r = _Reader(html)
    r.feed(html)
    # any element never closed ends at EOF
    for n in r.root.walk():
        if n.end is None:
            n.end = len(html)
    return r.root


STAGE_NAMES = [
    ('title',       re.compile(r'\btitle\b|lesson overview|today at a glance|at a glance|start here', re.I)),
    ('arrival',     re.compile(r'\barrival\b', re.I)),
    ('starter',     re.compile(r'\bstarter\b', re.I)),
    ('ido2',        re.compile(r'i do\s*2', re.I)),
    ('ido',         re.compile(r'\bi do\b', re.I)),
    ('wedo2',       re.compile(r'we do\s*2', re.I)),
    ('wedo',        re.compile(r'\bwe do\b', re.I)),
    ('independent', re.compile(r'\bindependent\b', re.I)),
    ('lundy_stage', re.compile(r'lundy loop', re.I)),
    ('exit',        re.compile(r'\bexit\b', re.I)),
    ('complete',    re.compile(r'\bcomplete\b', re.I)),
]


def stage_name(node: Node) -> str:
    dt = (node.attrs.get('data-type') or '').strip()
    if dt:
        return dt
    probe = node.attrs.get('data-title') or ''
    hs = node.find(lambda n: n.tag in ('h1', 'h2', 'h3'))
    if hs:
        probe = probe + ' ' + hs[0].inner_text()
    for name, rx in STAGE_NAMES:
        if rx.search(probe):
            return name
    return 'unnamed'


def stages(doc: Node):
    """Top-level slides only, in document order."""
    sl = [n for n in doc.walk()
          if 'slide' in n.classes()
          and not any('slide' in a.classes() for a in n.ancestors())]
    return sorted(sl, key=lambda n: n.start)


def is_ribbon(n: Node) -> bool:
    return 'lundy' in n.classes()


def splice(html: str, edits):
    """edits: list of (start, end, replacement). Applied right-to-left so
    earlier offsets stay valid. Overlapping edits are refused."""
    es = sorted(edits, key=lambda e: e[0])
    for a, b in zip(es, es[1:]):
        if a[1] > b[0]:
            raise ValueError('overlapping edits: %r and %r' % (a[:2], b[:2]))
    out = html
    for start, end, rep in reversed(es):
        out = out[:start] + rep + out[end:]
    return out
