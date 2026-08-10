"""Shared text/readability instrument for the Science v3 install.

One instrument, used for every set (three live suites, three new packs) so the
figures in the report are comparable. Written against BOTH print vocabularies —
GROW's `.print-*` and BUILD/LAUNCH's abbreviated `.p*` — because an instrument
written for one dialect produces false negatives on the other.
"""
import re, html as _html

# ---------------------------------------------------------------- text extraction

_DROP = re.compile(r'<(script|style)\b.*?</\1>', re.S | re.I)
_TAG = re.compile(r'<[^>]+>')
_COMMENT = re.compile(r'<!--.*?-->', re.S)


def strip_html(fragment: str) -> str:
    """HTML fragment -> visible text, with tags acting as word boundaries."""
    s = _COMMENT.sub(' ', fragment)
    s = _DROP.sub(' ', s)
    s = _TAG.sub(' ', s)
    s = _html.unescape(s)
    s = s.replace('‍', '').replace(' ', ' ')
    return re.sub(r'\s+', ' ', s).strip()


def visible_words(fragment: str) -> list:
    """Words that a readability measure should count.

    Emoji, glyphs (◆ ▲ ★), rule characters and bare punctuation are not words.
    """
    txt = strip_html(fragment)
    out = []
    for tok in re.split(r'\s+', txt):
        tok = tok.strip('·—–-“”"\'()[]{}:;,.!?%×→…')
        if not tok:
            continue
        if not re.search(r'[A-Za-z]', tok):
            continue
        out.append(tok)
    return out


# ---------------------------------------------------------------- readability

_VOWELS = 'aeiouy'


def syllables(word: str) -> int:
    w = re.sub(r'[^a-z]', '', word.lower())
    if not w:
        return 0
    if len(w) <= 3:
        return 1
    w = re.sub(r'(?:[^laeiouy]es|ed|[^laeiouy]e)$', '', w)
    w = re.sub(r'^y', '', w)
    n = len(re.findall(r'[aeiouy]{1,2}', w))
    return max(1, n)


def sentences(text: str) -> int:
    # Bullet/line units count as sentences: instructional prose is often unpunctuated.
    parts = [p for p in re.split(r'[.!?]+(?:\s|$)|\n+|(?<=[a-z])\s*·\s*', text) if p.strip()]
    return max(1, len(parts))


def fk_grade(fragment: str):
    """Flesch-Kincaid grade level. Returns (grade, words, sents, sylls)."""
    words = visible_words(fragment)
    if not words:
        return (None, 0, 0, 0)
    text = strip_html(fragment)
    ns = sentences(text)
    nw = len(words)
    sy = sum(syllables(w) for w in words)
    g = 0.39 * (nw / ns) + 11.8 * (sy / nw) - 15.59
    return (round(g, 2), nw, ns, sy)


# ---------------------------------------------------------------- structure helpers

def section_blocks(t: str, tag: str, cls: str):
    """Yield the inner HTML of every <tag class="...cls..."> ... </tag> block,
    matched by depth counting so nested same-tag elements do not truncate.

    Class matching is on whole space-separated tokens. A `\\b`-anchored match
    treats `slide-container` as carrying the class `slide` and swallows every
    slide inside it — that inflated the live word counts by ~60% on the first
    run of this instrument.
    """
    out = []
    for m in re.finditer(r'<%s\b[^>]*class="((?:[^"]*\s)?%s(?:\s[^"]*)?)"[^>]*>'
                         % (tag, re.escape(cls)), t):
        i = m.end()
        depth = 1
        pos = i
        pat = re.compile(r'</?%s\b' % tag)
        while depth and pos < len(t):
            mm = pat.search(t, pos)
            if not mm:
                break
            depth += -1 if mm.group(0).startswith('</') else 1
            pos = mm.end()
        out.append((m.start(), t[i:max(i, pos - len(tag) - 3)]))
    return out


def div_by_class(t: str, want: str):
    """Inner HTML of every <div> whose class token set contains all of `want`
    (space-separated), matched by depth counting. Non-greedy `.*?</div>` stops at
    the first nested close and silently drops the scaffold half of a tier route."""
    need = set(want.split())
    out = []
    for m in re.finditer(r'<div\b[^>]*class="([^"]*)"[^>]*>', t):
        if not need <= set(m.group(1).split()):
            continue
        i = m.end()
        depth, pos = 1, i
        pat = re.compile(r'</?div\b')
        while depth and pos < len(t):
            mm = pat.search(t, pos)
            if not mm:
                break
            depth += -1 if mm.group(0).startswith('</') else 1
            pos = mm.end()
            if depth == 0:
                out.append(t[i:mm.start()])
                break
    return out


def slide_texts(t: str):
    """Every on-screen slide's text, keyed by slide type.

    New packs use <section class="slide" data-type=...>; the live suites use
    <div class="slide">. Both are handled — checking only one produces a
    confident zero on the other set.
    """
    out = []
    for m in re.finditer(r'<section\b[^>]*class="slide[^"]*"[^>]*>', t):
        typ = re.search(r'data-type="([^"]*)"', m.group(0))
        i = m.end()
        j = t.find('</section>', i)
        out.append((typ.group(1) if typ else '?', t[i:j]))
    if out:
        return out
    # Live chassis: <div class="slide" data-title="I Do 1"> — type lives in the title.
    # Match on the class TOKEN SET, once, so `slide active` is not counted twice
    # and `slide-container` is not counted at all.
    live_map = [('title', 'title'), ('arrival', 'arrival'), ('glance', 'glance'),
                ('i do', 'ido'), ('we do', 'wedo'), ('independent', 'independent'),
                ('lundy', 'lundy'), ('exit', 'exit'), ('starter', 'starter')]
    for m in re.finditer(r'<div\b[^>]*class="([^"]*)"[^>]*>', t):
        if 'slide' not in m.group(1).split():
            continue
        head = m.group(0)
        dt = re.search(r'data-title="([^"]*)"', head)
        name = (dt.group(1) if dt else '').lower()
        typ = next((v for k, v in live_map if k in name), '?')
        i = m.end()
        depth, pos = 1, m.end()
        pat = re.compile(r'</?div\b')
        while depth and pos < len(t):
            mm = pat.search(t, pos)
            if not mm:
                break
            depth += -1 if mm.group(0).startswith('</') else 1
            pos = mm.end()
            if depth == 0:
                out.append((typ, t[i:mm.start()]))
                break
    return out
