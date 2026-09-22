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


# RULING 5 (standing instrument rule, 2026-09-22): a stage is identified by its slide id --
# by what the deck declares for that slide -- and NEVER by the data-type attribute.
#
# data-type is a CATEGORY, not an identity, and the estate proves it: one value covers three
# slides ("We do", "Check", "Review" are all data-type="wedo") on 120 landed decks and all 18
# Summer 1 decks, two slides ("Opening" and "Arrival" are both data-type="arrival") on the same
# 120, and SEVEN slides on the 15 Autumn 1 W3-W7 decks, where "Try one together", "Choose, then
# explain" and "Show what you mean" are all data-type="ido".
#
# Reading it as the identity made verify_loop row 14 (P1-1, "the Title stage carries no panel")
# run over an EMPTY title_stages on 120 of 220 landed decks and on all 18 Summer 1 decks: the
# overview stage was typed "arrival", so the row could not see the stage it exists to protect
# and passed without testing anything.
#
# The order below is the deck's own declarations, every step justified by a measured count:
#   1. data-title + the slide's own heading -- present on 1,853 of 2,033 landed slides and
#      162 of 162 Summer 1 slides, BETTER coverage than data-type's 1,763
#   2. data-kind -- the declared role, on 180 landed slides ('opening' marks the overview)
#   3. data-timer == "0" -- the deck's own statement that a stage has no teaching time.
#      Measured: timer 0 appears at position 0 on 128 landed decks and all 18 Summer 1 decks,
#      and nowhere else except the 8 id="complete-slide" slides, which step 1 already names
#      'complete'. So it needs no position argument to be safe.
#   4. 'unnamed' -- and never data-type. Measured after the change: 0 slides reach it.
#
# First match wins, so the "2" stages and the specific phrases are tested before their base
# words: "We do . review the evidence" is a We Do, not a Review.
STAGE_NAMES = [
    ('title',       re.compile(r'\btitle\b|lesson overview|today at a glance|at a glance'
                               r'|start here|\bopening\b', re.I)),
    ('arrival',     re.compile(r'\barrival\b|start with what you know', re.I)),
    # "Start the enquiry" is the STARTER, measured: 132 slides carry it and every one of them sits
    # at position 2, after the overview (data-timer="0") and the arrival task, with data-timer="3".
    # It was in the title pattern for one revision of this file and wrongly took 132 teaching
    # stages out of `eligible`; the adversarial review caught it before it reached a transplant.
    ('starter',     re.compile(r'\bstarter\b|start the enquiry', re.I)),
    ('vocabulary',  re.compile(r'words that help', re.I)),
    ('ido2',        re.compile(r'i do\s*2', re.I)),
    ('ido',         re.compile(r'\bi do\b|watch a worked example', re.I)),
    ('wedo2',       re.compile(r'we do\s*2', re.I)),
    ('wedo',        re.compile(r'\bwe do\b|try one together', re.I)),
    ('check',       re.compile(r'check the method|check the reasoning|^check$', re.I)),
    ('independent', re.compile(r'\bindependent\b|now it is your turn|choose, then explain'
                               r'|show what you mean|make the reasoning visible', re.I)),
    ('lundy_stage', re.compile(r'lundy loop', re.I)),
    ('review',      re.compile(r'review and improve|\breview\b', re.I)),
    ('voice',       re.compile(r'your voice shapes', re.I)),
    ('exit',        re.compile(r'\bexit\b|before you go', re.I)),
    ('complete',    re.compile(r'\bcomplete\b', re.I)),
]

# data-kind is a declared ROLE, not the type attribute ruling 5 forbids.
KIND_STAGE = {'opening': 'title', 'learn': 'learn', 'task': 'independent',
              'review': 'review', 'voice': 'voice', 'exit': 'exit'}


def stage_probe(node: Node) -> str:
    """What the deck itself says this slide is: its declared title and its own heading.
    data-type is not read here and is not read anywhere in stage identity (ruling 5)."""
    probe = node.attrs.get('data-title') or ''
    hs = node.find(lambda n: n.tag in ('h1', 'h2', 'h3'))
    if hs:
        probe = probe + ' ' + hs[0].inner_text()
    return ' '.join(probe.split())


COMPLETE_RX = re.compile(r'\bcomplete\b', re.I)
LESSON_ID_RX = re.compile(r'title-([a-z])\d+$')


# STOP-C1 (ruled 2026-09-22): the SCIENCE stage-identity route.
#
# Ruling 5 forbids data-type as an identity. Science decks carry no data-kind either -- measured,
# absent on all 317 stages of the three exemplars plus the SX3 31 -- so neither route above can
# name them: 268 of 290 stages on the 31 came back 'unnamed', which left verify_loop row 2 running
# over an EMPTY modelling set on 31 of 31 decks and row 14 over an empty title set on 8 of 31.
#
# What names them is the EYEBROW: <span class="slide-tag tag-NAME">TEXT</span>. Its TEXT, never its
# class. The generator settles which of the two is the deck's declaration --
# _authoring/science_2026-27/_toolchain/build/build_html.py:109-111 emits
#     st  = s['stage']
#     typ = {'I do':'ido','We do':'wedo','You do':'independent'}.get(st,'')
#     tag = {'Opening':'arrival','Retrieval':'starter',...}.get(st,'starter')
#     ...data-type="{typ}"...<span class="slide-tag tag-{tag}">{e(st)}</span>
# so data-type and the tag- class are both LOSSY MAPS of s['stage'] while the text is s['stage']
# VERBATIM. The eyebrow is upstream of data-type, not laundered from it. Measured over the 34:
# 9 data-type values cover 15 distinct eyebrow texts, and data-type="wedo" alone covers "We do",
# "We do 2", "Check" and "Review evidence" -- the very conflation ruling 5 exists to forbid, which
# reading the text repairs rather than repeats.
#
# THE ROUTE RUNS LAST, after the table and after data-kind, and that ordering is load-bearing.
# The eyebrow is estate furniture, not a Science marker: it sits on 1772 of 2123 HUMANITIES stages
# (83.5%, 191 of 230 decks) and it DOES conflate there -- "I Do - learn and model" covers six
# different names across 103 stages, "I Do" covers ido and ido2 30/30, "Review" covers review and
# check. Measured Humanities impact by placement, all 230 decks:
#     eyebrow BEFORE the table    622 names changed on 191 decks, 191 decks red
#     eyebrow after the table      34 names changed on  15 decks,  15 decks red
#     eyebrow LAST                  0 names changed on   0 decks,   0 decks red
# Last means the route fires only where everything else returns 'unnamed' -- exactly the Science
# gap -- so a Humanities stage the table already names never reaches it.
EYEBROW_STAGE = {
    'opening': 'title',
    'arrival': 'arrival', 'arrival task': 'arrival',
    'starter': 'starter',
    'retrieval': 'retrieve',
    'i do': 'ido', 'i do 2': 'ido2',
    'we do': 'wedo', 'we do 2': 'wedo2',
    'hinge': 'check', 'check': 'check',
    'review': 'review', 'review evidence': 'review',
    'you do': 'independent', 'independent': 'independent',
    'refine': 'independent', 'workshop': 'independent',
    'exit': 'exit',
}

# The eyebrow alone cannot separate the FIRST "I do" from the SECOND: all three exemplars label
# both modelling stages "I do", and 23 of the 31 need an "I do 2" that no exemplar wording
# supplies. Ruled: the second occurrence in DOCUMENT ORDER is the "2" variant.
EYEBROW_ORDINAL = {'ido': 'ido2', 'wedo': 'wedo2'}

# The inverse, and the reason it exists: 23 of the 31 label the second modelling stage "I do 2"
# outright. Document order and the deck's own label must AGREE. A deck that declares "I do 2"
# before it declares any "I do" is declaring two things that contradict each other, and the
# ruled answer (STOP-C2 ruling 3) is RED for that deck rather than a quiet acceptance of
# whichever reading happens to be consulted first.
EYEBROW_ORDINAL_BASE = {'ido2': 'ido', 'wedo2': 'wedo'}


def stage_eyebrow(node: Node) -> str:
    """The stage's own rendered eyebrow label -- its text, never its class."""
    for n in node.walk():
        if 'slide-tag' in n.classes():
            return ' '.join(n.inner_text().split())
    return ''


def stage_lesson(node: Node) -> str:
    """'a' or 'b' for a two-lesson deck, read from the stage heading id (title-a3, title-b0).

    The five 13-stage GROW decks are two lessons concatenated: they carry TWO "Arrival" and TWO
    "Exit" eyebrows, which the eyebrow text cannot tell apart. The heading ids can, so a control
    that must not double-count a closing stage reads the lesson from here rather than inferring
    it. Stage identity itself is unaffected.
    """
    for h in node.find(lambda n: n.tag in ('h1', 'h2', 'h3')):
        m = LESSON_ID_RX.match((h.attrs.get('id') or '').strip())
        if m:
            return m.group(1)
    return ''


def _document_stages(node: Node):
    a = node.ancestors()
    return stages(a[-1]) if a else [node]


def eyebrow_names(stage_list) -> list:
    """The eyebrow route over a WHOLE document, in one left-to-right pass.

    Resolved as a sequence rather than per node because every ordinal question -- is this the
    first "I do" or the second, has the deck already declared the "1" this "2" needs, is this a
    third -- is a question about what the DECK has declared SO FAR, and the answer must be the
    name the route actually gave those earlier stages, not their raw labels. A per-node walk that
    re-read the labels could count a bare "I do" and an explicit "I do 2" as different things and
    hand out ido2 twice.

    '' means the stage carries no eyebrow. 'unnamed' means it carries one this route refuses:
    a label outside the emitted vocabulary, a "2" declared before its "1" (STOP-C2 ruling 3), or
    a modelling kind declared more times than a lesson has (STOP-C3 D3). Never a silent pass.
    """
    out, seen = [], {}
    for node in stage_list:
        label = stage_eyebrow(node)
        if not label:
            out.append('')
            continue
        name = EYEBROW_STAGE.get(label.lower())
        if name is None:
            out.append('unnamed')
            continue
        if name in EYEBROW_ORDINAL_BASE:                    # an explicit "I do 2" / "We do 2"
            base = EYEBROW_ORDINAL_BASE[name]
            if not seen.get(base) or seen.get(name):
                out.append('unnamed')                       # no "1" yet, or a second "2"
                continue
        elif name in EYEBROW_ORDINAL:                       # a bare "I do" / "We do"
            two = EYEBROW_ORDINAL[name]
            if seen.get(name) and seen.get(two):
                out.append('unnamed')                       # D3: a third -- unbounded modelling
                continue
            if seen.get(name):
                name = two
        seen[name] = seen.get(name, 0) + 1
        out.append(name)
    return out


def eyebrow_stage_name(node: Node) -> str:
    """This stage's name under the eyebrow route, resolved in its document's own order."""
    doc_stages = _document_stages(node)
    names = eyebrow_names(doc_stages)
    for s, n in zip(doc_stages, names):
        if s is node:
            return n
    return ''


# STOP-C3 D1 (ruled 2026-09-22): WHICH NAMING CHANNEL A DECK DECLARES.
#
# The eyebrow vocabulary is SIXTEEN phrases emitted by one generator. Gating every deck on it
# was wrong in the opposite direction from the defect it was written for: measured, it turned
# rows 2 and 14 RED on 60 and 92 of 230 Humanities decks and 117 and 162 of 200 Science decks,
# every one of them a deck whose stages an earlier route names perfectly well.
#
# Ruled: a deck is gated on the channel it ACTUALLY DECLARES. The channel is the one that names
# EVERY stage of the deck -- not most, not the first -- and it is read off the deck, never
# assumed from its path. Measured under this rule: Humanities 230/230 table, the SX3 31 31/31
# eyebrow, the verify_loop run population 91/91 table, and 19 Science decks declare NEITHER,
# which is RED rather than a pass.
def identity_channel(stage_list) -> str:
    """'table', 'eyebrow', or '' when the deck declares no naming channel at all."""
    if not stage_list:
        return ''
    if all(table_stage_name(s) for s in stage_list):
        return 'table'
    if all(EYEBROW_STAGE.get(stage_eyebrow(s).lower()) for s in stage_list):
        return 'eyebrow'
    return ''


PATHWAY_CLASS_RX = re.compile(r'\bpathway-([a-z]+)\b', re.I)


def declared_pathways(doc: Node) -> set:
    """The pathway(s) the deck declares on its root element, e.g. <html class="pathway-build">.

    Read from the deck rather than hard-coded, so the title-heading predicate that uses it works
    on every subject instead of the one it was first written against.
    """
    for n in doc.walk():
        if n.tag == 'html':
            return {m.group(1).lower()
                    for m in PATHWAY_CLASS_RX.finditer(n.attrs.get('class') or '')}
    return set()


def table_stage_name(node: Node) -> str:
    """Everything stage_name resolves BEFORE the eyebrow route: the timer marker, the STAGE_NAMES
    word table, then data-kind. '' when none of them names the stage.

    Split out of stage_name so a caller can ask which naming CHANNEL a deck declares without
    re-implementing the oracle beside it. stage_name calls this, so there is one route, not two.
    """
    probe = stage_probe(node)
    # A stage the deck gives NO teaching time is either the overview or the completion marker, and
    # nothing else: measured, data-timer="0" appears at position 0 on 128 landed decks and all 18
    # Summer 1 decks, and elsewhere only on the 8 id="complete-slide" slides. Tested before the
    # word table so that a topic word in an overview's own heading cannot claim it.
    if (node.attrs.get('data-timer') or '').strip() == '0':
        return 'complete' if COMPLETE_RX.search(probe) else 'title'
    for name, rx in STAGE_NAMES:
        if rx.search(probe):
            return name
    kind = (node.attrs.get('data-kind') or '').strip()
    if kind:
        return KIND_STAGE.get(kind, kind)
    return ''


def stage_name(node: Node) -> str:
    table = table_stage_name(node)
    if table:
        return table
    eyebrow = eyebrow_stage_name(node)          # STOP-C1: the science route, LAST by ruling
    if eyebrow:
        return eyebrow
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
