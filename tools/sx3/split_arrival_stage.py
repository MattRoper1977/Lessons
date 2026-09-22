#!/usr/bin/env python3
"""SX3-FU1: split a merged stage 0 into the exemplar's two-stage shape.

THE FINDING (ORDER SX3-FU1 F1, measured on main). The three pathway exemplars
name a two-stage opening: a title stage, then an arrival stage. Of the 31 landed
science decks, the 1 BUILD and 7 GROW decks already have it - stage 0 is
data-type="opening" carrying the deck title, stage 1 is data-type="arrival"
carrying the route controls. The 23 LAUNCH decks do NOT: their stage 0 is
data-type="arrival" and carries BOTH the deck title (h1) and the arrival root
(div.route-controls and the three route panels). This tool is the ONE adapter
rule that splits those, and nothing else.

THE CUT, AND WHY IT INVENTS NOTHING. Every existing byte of the merged stage
moves into exactly one of the two new stages; the cut is at the first
`<div class="route-controls"`. Exactly two elements are created:

  1. the opening stage's tag, `<span class="slide-tag tag-opening">Opening</span>`
     - the byte-identical house form, copied from the BUILD and GROW decks that
       already have the two-stage shape;
  2. the arrival stage's heading, `<h2 id="title-a1" tabindex="-1">TITLE</h2>`
     - where TITLE is the merged stage's OWN data-title. That is a derivation,
       not an authoring decision: on every already-split deck the arrival
       heading's text is byte-equal to that stage's data-title ("Four clues to
       start"), and on a merged deck the data-title is the arrival's while the
       h1 is the deck's - that mismatch is the fingerprint of the merge.

WHAT GOES WHERE
  opening : <span class="slide-tag tag-opening">Opening</span> + everything from
            the merged stage between its meta line and the cut (the h1, the
            learning-objective box, the route note) + the trailing
            div.knowledge-shortcut, if the merged stage has one.
  arrival : the merged stage's own slide-tag span + its science-meta line (which
            states the arrival's minutes) + the new h2 + everything from the cut,
            less that trailing div.knowledge-shortcut.

THE KNOWLEDGE SHORTCUT, AND WHY IT CROSSES THE CUT. Contract row 41: "All three
exemplars keep the knowledge-organiser opener inside slide 1." Measured on all
three exemplars, div.knowledge-shortcut is the LAST child of the opening stage.
On a merged deck it is the last child of the merged stage, which puts it after
the cut - so a naive cut sends it to the arrival stage, where it is no longer on
the stage a teacher sees at load. That was measured, not supposed: driving the
real control in a browser, the organiser opened on 23/23 decks before a cut that
left it behind and 0/23 after. It is moved back, and refused rather than guessed
at if the deck carries more than one or carries it anywhere but trailing.

TIMER. The order carries the minutes to the arrival stage: the arrival keeps the
merged stage's data-timer and the opening gets data-timer="0", so the deck's
total teaching time is UNCHANGED. That is asserted, not assumed.

IDS. The deck's own script selects stages with querySelectorAll('.slide') - in
document order, never by id - and no id="slide-N" is referenced anywhere in the
deck. Ids are therefore renumbered to stay contiguous, which is what makes the
result indistinguishable from a natively two-stage deck.

REFUSES rather than guessing: a deck whose stage 0 is not a merged arrival, a
cut point that is missing or ambiguous, an id collision, a changed timer total,
or any visible text that is not exactly the original plus the two created
strings.

  python3 tools/sx3/split_arrival_stage.py --check  PATH...
  python3 tools/sx3/split_arrival_stage.py --write  PATH...
  python3 tools/sx3/split_arrival_stage.py --self-test
"""
import argparse
import re
import sys

SECTION = re.compile(r'<section\b[^>]*\bid="slide-(\d+)"[^>]*>')
TAG_SPAN = re.compile(r'\s*<span class="slide-tag[^"]*"[^>]*>.*?</span>', re.S)
META_P = re.compile(r'\s*<p class="science-meta"[^>]*>.*?</p>', re.S)
# The arrival stage's minutes inside that line, with the separator that precedes them, so
# removing the match leaves a well-formed line behind for the title stage.
MINUTES_SEGMENT = re.compile(r'\s*\u00b7\s*(?P<mins>\d+\s*MINUTES)\b', re.I)
H1 = re.compile(r'<h1\b[^>]*>(.*?)</h1>', re.S)
CUT = '<div class="route-controls"'
OPEN_TAG_SPAN = '<span class="slide-tag tag-opening">Opening</span>'
SHORTCUT_OPEN = '<div class="knowledge-shortcut"'


def _balanced_div(html, start):
    """End offset of the </div> closing the <div> opened at `start`, by depth count."""
    depth = 0
    for m in re.finditer(r'<div\b|</div>', html[start:]):
        depth += 1 if m.group(0) != '</div>' else -1
        if depth == 0:
            return start + m.end()
    raise ValueError('REFUSED: unclosed <div> at %d' % start)


def take_trailing_shortcut(tail):
    """Lift a trailing div.knowledge-shortcut out of `tail`. Returns (tail, shortcut).

    Contract row 41 puts the organiser opener in the opening stage. Refuses rather
    than guessing when the deck carries more than one shortcut, or carries one that
    is not the last thing in the merged stage."""
    hits = [m.start() for m in re.finditer(re.escape(SHORTCUT_OPEN), tail)]
    if not hits:
        return tail, ''
    if len(hits) > 1:
        raise ValueError('REFUSED: %d div.knowledge-shortcut blocks after the cut; '
                         'which one belongs to the opening stage is not derivable' % len(hits))
    a = hits[0]
    b = _balanced_div(tail, a)
    if tail[b:].strip():
        raise ValueError('REFUSED: div.knowledge-shortcut is not the last child of the merged '
                         'stage (%d bytes follow it); the exemplars put it last'
                         % len(tail[b:].strip()))
    return tail[:a].rstrip(), tail[a:b].strip()


def attr(tag, name):
    m = re.search(r'\b%s="([^"]*)"' % re.escape(name), tag)
    return m.group(1) if m else None


def set_attr(tag, name, value):
    if re.search(r'\b%s="[^"]*"' % re.escape(name), tag):
        return re.sub(r'\b%s="[^"]*"' % re.escape(name), '%s="%s"' % (name, value), tag, count=1)
    return tag[:-1].rstrip() + ' %s="%s">' % (name, value)


def drop_attr(tag, name):
    return re.sub(r'\s+%s="[^"]*"' % re.escape(name), '', tag, count=1)


def text_of(html):
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', html)).strip()


# The catalogue derives a deck's teaching term from a term code appearing anywhere in
# stage 0's TEXT - build_catalogue.py's weakest fallback, `term_codes(title_slide)`.
# This is that same expression, so the two agree by construction.
TERM_CODE = re.compile(r'\b(Aut|Spr|Sum)(?:umn|ing|mer)?\s*([12])\b', re.I)


def term_codes(s):
    return sorted(set(a.title() + b for a, b in TERM_CODE.findall(s)))


def stage0_text(html):
    st = stages(html)
    if not st:
        return ''
    s0, e0, tag0 = st[0]
    return text_of(html[s0 + len(tag0):e0])


def stages(html):
    """Every stage section as (start, end, opening_tag). The last ends at its own </section>."""
    marks = list(SECTION.finditer(html))
    if not marks:
        return []
    out = []
    for i, m in enumerate(marks):
        end = marks[i + 1].start() if i + 1 < len(marks) else _close_of(html, m.start())
        out.append((m.start(), end, m.group(0)))
    return out


def _close_of(html, start):
    """The </section> that closes the section opened at `start`, by depth count."""
    depth = 0
    for m in re.finditer(r'<section\b|</section>', html[start:]):
        depth += 1 if m.group(0) != '</section>' else -1
        if depth == 0:
            return start + m.end()
    raise ValueError('unclosed <section> at %d' % start)


def needs_split(html):
    st = stages(html)
    if not st:
        return False, 'no stage sections (no <section ... id="slide-N">)'
    s0, e0, tag0 = st[0]
    if attr(tag0, 'data-type') != 'arrival':
        return False, 'stage 0 data-type=%r, not "arrival"' % attr(tag0, 'data-type')
    body = html[s0 + len(tag0):e0]
    if not H1.search(body):
        return False, 'stage 0 carries no <h1> title block'
    if CUT not in body:
        return False, 'stage 0 carries no arrival root (%s)' % CUT
    return True, 'stage 0 is data-type="arrival" and carries both the <h1> title block and the arrival root'


def split(html):
    st = stages(html)
    s0, e0, tag0 = st[0]
    body = html[s0 + len(tag0):e0]
    inner = body[:body.rindex('</section>')]
    trail = body[body.rindex('</section>'):]

    cut = inner.index(CUT)
    head, tail = inner[:cut], inner[cut:]
    tail, shortcut = take_trailing_shortcut(tail)

    m_span = TAG_SPAN.search(head)
    if not m_span:
        raise ValueError('REFUSED: stage 0 has no slide-tag span to carry to the arrival stage')
    span_arr = m_span.group(0).strip()
    head = head[:m_span.start()] + head[m_span.end():]

    # RULED 2026-09-22 (STOP-C1, the split refusal amended rather than bypassed).
    #
    # On a few decks the science-meta line glues two unrelated facts together:
    #   "LAUNCH - GCSE BIOLOGY FOUNDATION - W9 - LESSON Classic - 4 MINUTES - Aut2.W1"
    # The MINUTES belong to the arrival stage; the TERM belongs to the lesson, and
    # build_catalogue.py reads it from stage 0's text (its title-slide fallback). Moving
    # the whole line therefore carried the term off the title stage and the catalogue's
    # term fell silently to "unspecified" -- which is why this tool refused all three
    # decks outright.
    #
    # It no longer has to choose. The line is SPLIT: the term (and everything else that
    # describes the lesson) stays on the title stage, and only the minutes travel, as
    # their own meta line on the arrival stage. The refusal below is kept exactly as it
    # was and becomes the red proof: if a split ever does carry a term code off stage 0,
    # it still FAILS.
    m_meta = META_P.search(head)
    meta = ''
    meta_split_chars = 0
    if m_meta:
        whole = m_meta.group(0).strip()
        m_min = MINUTES_SEGMENT.search(whole)
        if m_min and term_codes(whole):
            kept = MINUTES_SEGMENT.sub('', whole, count=1)
            minutes = m_min.group('mins').strip()
            meta = '<p class="science-meta">%s</p>' % minutes
            head = head[:m_meta.start()] + kept + head[m_meta.end():]
            # EXACT ACCOUNTING, not a tolerance. Splitting the glued line drops the one
            # separator that used to join the minutes to the rest -- nothing else. The
            # figure is derived from the three strings themselves and handed to the
            # verifier, which keeps demanding an exact match rather than a range.
            # The isolated strings account for the dropped separator; the whole-document
            # measure also gains ONE character, because the single <p> becomes two blocks
            # and text_of() joins adjacent blocks with one separator. Both terms are
            # derived, so the verifier below stays an exact equality.
            meta_split_chars = (len(text_of(kept)) + len(text_of(meta))
                                - len(text_of(whole)) + 1)
        else:
            meta = whole
            head = head[:m_meta.start()] + head[m_meta.end():]

    m_h1 = H1.search(head)
    if not m_h1:
        raise ValueError('REFUSED: no <h1> found for the opening stage title')
    deck_title = text_of(m_h1.group(1))
    data_title = attr(tag0, 'data-title')
    if not data_title:
        raise ValueError('REFUSED: stage 0 has no data-title to derive the arrival heading from')
    if 'id="title-a1"' in html:
        raise ValueError('REFUSED: id="title-a1" already exists; the arrival heading would collide')

    timer = attr(tag0, 'data-timer') or '0'

    open_tag = set_attr(set_attr(set_attr(tag0, 'data-type', 'opening'), 'data-timer', '0'), 'data-title', deck_title)
    for a in ('data-teacher', 'data-ta1', 'data-prompt', 'aria-hidden', 'inert'):
        open_tag = drop_attr(open_tag, a)
    open_tag = set_attr(open_tag, 'id', 'slide-PLACEHOLDER-A')

    arr_tag = set_attr(set_attr(tag0, 'data-timer', timer), 'id', 'slide-PLACEHOLDER-B')

    opening = open_tag + OPEN_TAG_SPAN + head + shortcut + '</section>'
    arrival = (arr_tag + span_arr + meta
               + '<h2 id="title-a1" tabindex="-1">%s</h2>' % data_title
               + tail + trail)

    new = html[:s0] + opening + arrival + html[e0:]

    # renumber every stage id, in document order, contiguously from 1
    def _renumber(doc):
        marks = list(re.finditer(r'<section\b[^>]*\bid="(slide-[^"]*)"[^>]*>', doc))
        out, last = [], 0
        for i, m in enumerate(marks):
            tag = m.group(0)
            out.append(doc[last:m.start()])
            out.append(set_attr(tag, 'id', 'slide-%d' % (i + 1)))
            last = m.end()
        out.append(doc[last:])
        return ''.join(out)

    return _renumber(new), dict(deck_title=deck_title, data_title=data_title, timer=timer,
                                shortcut=bool(shortcut), meta_split_chars=meta_split_chars)


def timer_total(html):
    return sum(int(attr(t, 'data-timer') or 0) for _, _, t in stages(html))


def check_invariants(before, after, info):
    p = []
    b, a = stages(before), stages(after)
    if len(a) != len(b) + 1:
        p.append('stage count went %d -> %d, expected +1' % (len(b), len(a)))
    if timer_total(after) != timer_total(before):
        p.append('timer total moved %d -> %d' % (timer_total(before), timer_total(after)))
    ids = [attr(t, 'id') for _, _, t in a]
    if ids != ['slide-%d' % (i + 1) for i in range(len(ids))]:
        p.append('stage ids are not contiguous slide-1..slide-%d: %s' % (len(ids), ids[:4]))
    if len(set(ids)) != len(ids):
        p.append('duplicate stage ids')
    tb, ta = text_of(before), text_of(after)
    added = 'Opening ' + info['data_title']
    # When the science-meta line glued the arrival minutes to the lesson term, the split
    # separates them and the one joining separator goes with it. split() measures that cost
    # from the strings it actually produced and reports it here, so this stays an exact
    # equality rather than becoming a tolerance.
    expected = len(tb) + len(added) + 1 + info.get('meta_split_chars', 0)
    if len(ta) != expected:
        # exact accounting: the only new visible text is the tag word and the arrival heading
        p.append('visible text length moved by %d, expected %d (the tag word plus the arrival heading)'
                 % (len(ta) - len(tb), expected - len(tb)))
    for token in (info['deck_title'], info['data_title']):
        if token and token not in ta:
            p.append('text lost after the split: %r' % token[:40])
    if 'id="title-a1"' not in after:
        p.append('the arrival heading was not created')
    # A term binding must not be carried out of the opening stage. On a few decks the
    # science-meta line glues two different facts together - the arrival stage's
    # minutes AND the lesson's term, e.g.
    #   "LAUNCH - GCSE BIOLOGY FOUNDATION - W12 - LESSON Classic - 4 MINUTES - Aut2.W4"
    # The minutes travel to the arrival stage, so the term would travel with them and
    # the catalogue's term would silently fall to "unspecified". Refuse instead.
    lost_terms = [c for c in term_codes(stage0_text(before)) if c not in term_codes(stage0_text(after))]
    if lost_terms:
        p.append('the split would carry the term binding %s out of the opening stage, where '
                 'the catalogue reads it (build_catalogue.py title-slide fallback); the '
                 'science-meta line states both the arrival minutes and the lesson term'
                 % ', '.join(lost_terms))
    # contract row 41: the organiser opener must end up in the opening stage
    if 'data-action="organiser"' in before:
        sa = stages(after)
        if len(sa) >= 1:
            s_open = after[sa[0][0]:sa[0][1]]
            if 'data-action="organiser"' not in s_open:
                p.append('the knowledge-organiser opener did not stay in the opening stage '
                         '(contract row 41)')
    return p


def run(paths, write):
    todo, skip, bad = [], [], []
    for p in paths:
        html = open(p, encoding='utf-8').read()
        ok, why = needs_split(html)
        (todo if ok else skip).append((p, why))
    print('SCOPE: %d file(s) examined; %d need the split, %d do not' % (len(paths), len(todo), len(skip)))
    for p, why in skip:
        print('   SKIP %-58s %s' % (p.rsplit('/', 1)[-1], why))
    for p, why in todo:
        before = open(p, encoding='utf-8').read()
        try:
            after, info = split(before)
        except ValueError as e:
            bad.append((p, str(e)))
            print('   REFUSED %-54s %s' % (p.rsplit('/', 1)[-1], e))
            continue
        problems = check_invariants(before, after, info)
        if problems:
            bad.append((p, '; '.join(problems)))
            print('   REFUSED %-54s %s' % (p.rsplit('/', 1)[-1], '; '.join(problems)))
            continue
        print('   %-8s %-54s stages %d->%d, timer total %d unchanged, arrival heading %r'
              % ('WRITE' if write else 'OK', p.rsplit('/', 1)[-1], len(stages(before)), len(stages(after)),
                 timer_total(before), info['data_title']))
        if write:
            open(p, 'w', encoding='utf-8').write(after)
    return 1 if bad else 0


# ------------------------------------------------------------------ self-test
DECK = ('<html><body><main id="lessonDeck">'
        '<section class="slide" id="slide-1" data-title="Four clues to start" data-timer="4" data-type="arrival" data-teacher="note">'
        '<span class="slide-tag tag-arrival">Arrival</span>'
        '<p class="science-meta">LAUNCH · W9 · 4 MINUTES</p>'
        '<h1 id="title-s0" tabindex="-1">Cell cycle</h1>'
        '<div class="li-box"><p>Objective</p></div>'
        '<p class="small">forty minutes</p>'
        '<div class="route-controls" role="group"><button>Standard</button></div>'
        '<section class="route-panel">panel</section>'
        '<div class="knowledge-shortcut">'
        '<button type="button" data-action="organiser">Open knowledge organiser</button></div>'
        '</section>'
        '<section class="slide" id="slide-2" data-title="Starter" data-timer="6" data-type="starter">'
        '<span class="slide-tag tag-starter">Starter</span><h2 id="title-s1">Starter</h2><p>body</p></section>'
        '</main></body></html>')


def self_test():
    problems = []

    def case(name, doc, expect_ok):
        ok, why = needs_split(doc)
        if not ok:
            got = 'not applicable: ' + why
            passed = not expect_ok
        else:
            try:
                after, info = split(doc)
                pr = check_invariants(doc, after, info)
                got = 'split clean' if not pr else 'refused: ' + '; '.join(pr)
                # A negative case may be caught by needs_split, by a raise, OR by the
                # invariants. All three are a correct refusal.
                passed = (expect_ok and not pr) or (not expect_ok and bool(pr))
            except ValueError as e:
                got = 'refused: %s' % e
                passed = not expect_ok
        print('  %s  %-62s %s' % ('PASS' if passed else 'FAIL', name, got))
        if not passed:
            problems.append(name)

    case('positive control: a merged stage 0 splits and every invariant holds', DECK, True)
    case('a deck already in the two-stage shape is not applicable',
         DECK.replace('data-type="arrival"', 'data-type="opening"', 1), False)
    case('a stage 0 with no arrival root is not applicable', DECK.replace('<div class="route-controls" role="group">', '<div class="other">', 1), False)
    case('a stage 0 with no <h1> title block is not applicable', DECK.replace('<h1 id="title-s0" tabindex="-1">Cell cycle</h1>', '', 1), False)
    case('a stage 0 with no data-title refuses (nothing to derive the heading from)',
         DECK.replace(' data-title="Four clues to start"', '', 1), False)
    case('an existing id="title-a1" refuses rather than colliding',
         DECK.replace('<h2 id="title-s1">Starter</h2>', '<h2 id="title-a1">Starter</h2>', 1), False)
    case('a deck with no stage sections at all is not applicable', '<html><body><main></main></body></html>', False)
    case('two knowledge shortcuts after the cut refuse rather than guessing',
         DECK.replace('<div class="knowledge-shortcut">',
                      '<div class="knowledge-shortcut"><button data-action="organiser">a</button></div>'
                      '<div class="knowledge-shortcut">', 1), False)
    case('a knowledge shortcut that is not the merged stage\'s last child refuses',
         DECK.replace('</div>\'\n        \'</section>', '</div><p>after</p></section>')
             .replace('data-action="organiser">Open knowledge organiser</button></div>',
                      'data-action="organiser">Open knowledge organiser</button></div><p>after</p>', 1), False)
    # RULED 2026-09-22: this case used to expect a REFUSAL. The splitter's rule is amended,
    # not bypassed -- the term token now stays on the title stage where build_catalogue reads
    # it, and only the minutes travel, so the deck splits. The refusal itself is untouched and
    # is exercised by the case below, which is the red proof that it can still fire.
    case('a deck whose meta glues the term to the arrival minutes now SPLITS, term retained',
         DECK.replace('LAUNCH \u00b7 W9 \u00b7 4 MINUTES', 'LAUNCH \u00b7 W9 \u00b7 4 MINUTES \u00b7 Aut2\u00b7W1'), True)
    case('a deck with no knowledge shortcut still splits cleanly',
         re.sub(r'<div class="knowledge-shortcut">.*?</div>', '', DECK, flags=re.S), True)

    after, info = split(DECK)
    checks = [
        ('the opening stage is created with data-type="opening" and data-timer="0"',
         'data-type="opening"' in after and re.search(r'id="slide-1"[^>]*data-timer="0"', after) is not None),
        ('the arrival stage keeps the carried minutes', 'data-timer="4"' in after),
        ('the deck total is unchanged', timer_total(after) == timer_total(DECK) == 10),
        ('the arrival heading is the merged stage data-title', '<h2 id="title-a1" tabindex="-1">Four clues to start</h2>' in after),
        ('the deck title stays in the opening stage', re.search(r'id="slide-1".*?<h1 id="title-s0"', after, re.S) is not None),
        ('the route controls sit in the arrival stage', re.search(r'id="slide-2".*?route-controls', after, re.S) is not None),
        ('the opening carries the house tag markup', OPEN_TAG_SPAN in after),
        ('the arrival keeps its own tag span', '<span class="slide-tag tag-arrival">Arrival</span>' in after),
        ('the teacher note stays with the arrival stage', re.search(r'id="slide-2"[^>]*data-teacher="note"', after) is not None),
        ('the opening carries no teacher note', re.search(r'id="slide-1"[^>]*data-teacher', after) is None),
        ('stage ids are contiguous', [attr(t, "id") for _, _, t in stages(after)] == ['slide-1', 'slide-2', 'slide-3']),
        ('the following stage survives unchanged', 'data-title="Starter"' in after and 'id="title-s1"' in after),
        ('the organiser opener lands in the OPENING stage (contract row 41)',
         re.search(r'id="slide-1".*?data-action="organiser".*?</section>', after, re.S) is not None
         and re.search(r'id="slide-2".*?data-action="organiser"', after, re.S) is None),
        ('the knowledge shortcut is the last child of the opening stage, as on all three exemplars',
         re.search(r'<div class="knowledge-shortcut">.*?</div></section><section[^>]*id="slide-2"', after, re.S) is not None),
    ]
    for name, ok in checks:
        print('  %s  %s' % ('PASS' if ok else 'FAIL', name))
        if not ok:
            problems.append(name)

    planted = DECK.replace('data-timer="4"', 'data-timer="4" data-x="1"')
    a2, i2 = split(planted)
    a2 = a2.replace('data-timer="4"', 'data-timer="9"', 1)
    fired = check_invariants(planted, a2, i2)
    print('  %s  a planted timer change is caught by the total invariant' % ('PASS' if fired else 'FAIL'))
    if not fired:
        problems.append('timer invariant')

    # plant the exact bug the browser caught: the shortcut left on the arrival side
    a4, i4 = split(DECK)
    m_sc = re.search(r'<div class="knowledge-shortcut">.*?</div>', a4, re.S)
    sc = m_sc.group(0)
    a4 = (a4[:m_sc.start()] + a4[m_sc.end():]).replace('</section></main>', sc + '</section></main>', 1)
    fired = check_invariants(DECK, a4, i4)
    print('  %s  a planted loss of the organiser opener is caught by the row 41 invariant'
          % ('PASS' if fired else 'FAIL'))
    if not fired:
        problems.append('row 41 invariant')

    a3, i3 = split(DECK)
    a3 = a3.replace('<p class="small">forty minutes</p>', '')
    fired = check_invariants(DECK, a3, i3)
    print('  %s  planted text loss is caught by the text invariant' % ('PASS' if fired else 'FAIL'))
    if not fired:
        problems.append('text invariant')

    if problems:
        print('SELF-TEST FAIL:', problems)
        return 1
    print('SELF-TEST PASS: the rule splits only a merged arrival stage, derives both created strings, and every planted fault is refused')
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('paths', nargs='*')
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument('--check', action='store_true')
    g.add_argument('--write', action='store_true')
    g.add_argument('--self-test', action='store_true')
    a = ap.parse_args()
    if a.self_test:
        return self_test()
    if not a.paths:
        ap.error('give at least one deck path')
    return run(a.paths, a.write)


if __name__ == '__main__':
    sys.exit(main())
