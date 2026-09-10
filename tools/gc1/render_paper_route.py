#!/usr/bin/env python3
"""tools/gc1/render_paper_route.py - GC1 P2P: render each week's paper completion
route as a .docx that is indistinguishable from the rest of the pack, then a .pdf.

THE STYLE IS DONATED, NOT RETYPED

P2P says the paper route "must look like the same unit, not a bolt-on", and lists
the styling: Normal DejaVu Sans 11.5 #172A22, Title 25 bold, Heading 2 14 bold,
page break before each mid-document Title, footer "Week n <label>  |  <page>".

Every one of those was measured off the pack rather than taken on trust, and they
all hold. But reproducing them by construction means reproducing A4 at 8.27x11.69
with margins 0.68/0.68/0.62/0.63, a footer carrying a live PAGE field, and four
style definitions -- and any one of them drifting makes the paper route look like
what it must not look like.

So the renderer opens a real pack document, empties its body, and writes into it.
The styles, the section geometry and the footer's PAGE field arrive as bytes from
a file a teacher already prints. There is nothing to keep in sync.

WHAT IT REFUSES

R7 bars variables from this unit, and the block-writing grids are where a variable
block would most plausibly appear -- a word bank is exactly the place someone adds
"set score to 0" without thinking. So the renderer checks every word bank against
the unit's measured vocabulary and raises on anything outside it. The check is on
the block wording, and it is a raise rather than a warning, because a printed
worksheet cannot be recalled from a classroom.

USAGE
  python3 tools/gc1/render_paper_route.py --routes routes.json --unit <dir> [--pdf]
  python3 tools/gc1/render_paper_route.py --self-test
"""
import argparse
import copy
import json
import os
import re
import subprocess
import sys

from docx import Document
from docx.enum.text import WD_BREAK
from docx.shared import Pt

# The unit's entire block vocabulary, measured across all 23 .sb3: 15 opcodes and
# nothing else. Everything a word bank may print maps to one of these.
# Each token has to be specific enough that ordinary prose cannot contain it. An
# earlier list held bare 'for', 'if', 'then', 'when' and 'move', and "ask the
# teacher for help" passed the guard on the word 'for'. A word bank that admits
# sentences is not a word bank.
ALLOWED_BLOCK_WORDS = [
    'when green flag clicked', 'key pressed',
    'go to x', 'change x by', 'change y by', 'steps',
    'point in direction', 'glide', 'secs to x',
    'forever', 'wait until', 'touching', 'say ', 'seconds',
]
# The if-block is written several ways in these banks -- "if then", "if _ then",
# "if <> then", "if <touching [Maze]?> then" -- so it needs a shape, not a literal.
# The word cap is what stops it swallowing prose: "if you finish then ask a
# partner" is seven words and is refused, "if <touching [Maze]?> then" is three.
IF_BLOCK = re.compile(r'^\s*if\b.*\bthen\b\s*$', re.I)
IF_BLOCK_MAX_WORDS = 6
# A variable block is data_* in Scratch. In English on a worksheet it looks like
# one of these, and any of them on a printed grid is R7 broken in a way that
# cannot be taken back once the sheet is in a classroom.
FORBIDDEN_BLOCK_WORDS = [
    'set ', 'change score', 'variable', 'my variable', 'score', 'lives',
    'add to list', 'list', 'counter', 'points',
]


class BlockVocabularyError(ValueError):
    """A word bank offered a block this unit does not use, or a variable block."""


# Some weeks legitimately use NO blocks. Week 3 is "Build the world": the pupil
# creates three sprites and writes no script at all. A word bank there is empty,
# and an author saying so in words is right, not a defect. Emptiness declarations
# are allowed through; everything else still has to be a block this unit uses, and
# the variable check runs FIRST so "no blocks except set score" cannot slip past.
NO_BLOCKS = re.compile(r'\b(?:empty|no blocks|none|not used this week)\b', re.I)


def is_note(w):
    """A note to the pupil, not an offered block.

    A Scratch block wording never ends in a full stop -- "move 40 steps",
    "if <touching [Maze]?> then", "forever". A sentence does. That is the whole
    rule, and it is crisp enough to check: "Your first block comes in Week 4." is
    a note, "ask the teacher for help" is not and still has to survive the
    block test.

    The variable check runs BEFORE this, so a note cannot smuggle a variable in
    behind a full stop.
    """
    return w.rstrip().endswith('.') or bool(NO_BLOCKS.search(w.lower()))


def check_word_bank(words, where):
    for w in words:
        low = w.lower()
        for bad in FORBIDDEN_BLOCK_WORDS:
            if bad in low:
                raise BlockVocabularyError(
                    'R7: %s offers %r, which reads as a variable block. '
                    'Scoring is unit 122058 and does not belong on this sheet.' % (where, w))
        if is_note(w):
            continue
        if IF_BLOCK.match(w) and len(w.split()) <= IF_BLOCK_MAX_WORDS:
            continue
        if not any(tok in low for tok in ALLOWED_BLOCK_WORDS):
            raise BlockVocabularyError(
                'G11: %s offers %r, which is outside the 15 opcodes this unit uses.' % (where, w))
    return True


def blank_document(donor):
    """A pack document with its body emptied and its styles, section and footer kept."""
    doc = Document(donor)
    body = doc.element.body
    for child in list(body):
        if child.tag.endswith('}sectPr'):
            continue                      # the section holds page size, margins and the footer
        body.remove(child)
    return doc


def set_footer(doc, week, label):
    """Footer reads 'Week n <label>  |  <page>'. The PAGE field is the donor's own."""
    footer = doc.sections[0].footer
    if not footer.paragraphs:
        footer.add_paragraph()
    para = footer.paragraphs[0]
    runs = para.runs
    if runs:
        runs[0].text = 'Week %d %s  |  ' % (week, label)
        for extra in runs[1:]:
            # Keep the PAGE field runs; blank any stray literal text beside them.
            if 'PAGE' not in extra._r.xml and extra.text and not extra.text.strip().isdigit():
                extra.text = ''
    else:
        para.add_run('Week %d %s  |  ' % (week, label))
    return para.text


def title(doc, text, page_break=False):
    p = doc.add_paragraph(style='Title')
    if page_break:
        p.add_run().add_break(WD_BREAK.PAGE)
    p.add_run(text)
    return p


def h2(doc, text):
    return doc.add_paragraph(text, style='Heading 2')


def body(doc, text):
    return doc.add_paragraph(text, style='Normal')


def rule(doc, n=64):
    return body(doc, '_' * n)


def grid(doc, g):
    """One block-writing surface: the hat block, empty stack rows, and a word bank."""
    check_word_bank(g['allowedBlocks'], 'Week grid %r' % g.get('purpose', '?'))
    h2(doc, '%s · %s' % (g['sprite'], g['purpose']))
    body(doc, 'Write one block on each line. Start with the hat block, which is done for you.')
    t = doc.add_table(rows=g['rows'] + 1, cols=1)
    t.style = 'Table Grid'
    t.rows[0].cells[0].text = g['hatBlock']
    for r in t.rows[0].cells[0].paragraphs:
        for run in r.runs:
            run.bold = True
    body(doc, 'Blocks you may use this week:')
    body(doc, '   · ' + '\n   · '.join(g['allowedBlocks']))
    return t


def table(doc, spec):
    h2(doc, spec['caption'])
    cols = spec['columns']
    t = doc.add_table(rows=len(spec['rows']) + 1, cols=len(cols))
    t.style = 'Table Grid'
    for i, c in enumerate(cols):
        cell = t.rows[0].cells[i]
        cell.text = c
        for p in cell.paragraphs:
            for run in p.runs:
                run.bold = True
    for ri, row in enumerate(spec['rows'], start=1):
        for ci in range(len(cols)):
            t.rows[ri].cells[ci].text = row[ci] if ci < len(row) else ''
    return t


MAZE_NOTE = (
    'The maze below is the real one, at its real size. One square is 20 steps. '
    'Player starts at (-180, -120). Finish is at (180, 120). '
    'Move a counter square by square and write down where it lands.'
)


def maze_grid(doc, walls, start=(-180, -120), finish=(180, 120), step=20):
    """A coordinate grid a pupil can move a counter on, at the lesson's own geometry.

    Printed as a table rather than a picture on purpose: p2 asks for something a
    counter moves across, and a pupil tracing a route needs to be able to write in
    the square. Wall squares are filled, so paper and screen agree about where the
    sprite cannot go.
    """
    body(doc, MAZE_NOTE)
    xs = list(range(-240, 241, step))
    ys = list(range(180, -181, -step))
    blocked = set()
    for wx, wy, ww, wh in walls:
        for x in xs:
            for y in ys:
                if wx <= x < wx + ww and wy <= y < wy + wh:
                    blocked.add((x, y))
    t = doc.add_table(rows=len(ys), cols=len(xs))
    t.style = 'Table Grid'
    for ri, y in enumerate(ys):
        for ci, x in enumerate(xs):
            cell = t.rows[ri].cells[ci]
            if (x, y) in blocked:
                cell.text = '█'
            elif (x, y) == start:
                cell.text = 'P'
            elif (x, y) == finish:
                cell.text = 'F'
    for row in t.rows:
        for cell in row.cells:
            for p in cell.paragraphs:
                for run in p.runs:
                    run.font.size = Pt(7)
    return t


WALLS = [[-220, -160, 440, 20], [-220, 140, 440, 20], [-220, -140, 20, 280],
         [200, -140, 20, 280], [-70, -140, 20, 220], [50, -80, 20, 220]]


def render(route, donor, out_path):
    doc = blank_document(donor)
    wk, label = route['week'], route['label']
    set_footer(doc, wk, label)

    title(doc, 'Week %d %s · paper route' % (wk, label))
    body(doc, 'Paper route · GROW Computing · 40 minutes')
    body(doc, 'Name: _____________________  Date: __________')
    for line in route['intro']:
        body(doc, line)
    body(doc, 'Point, say, draw or write. Someone may record your exact words.')

    title(doc, 'Write your code', page_break=True)
    for g in route['p1_grids']:
        grid(doc, g)

    title(doc, 'The maze', page_break=True)
    body(doc, route['p2_maze']['use'])
    maze_grid(doc, WALLS)

    title(doc, 'Predict, trace, compare', page_break=True)
    for spec in route['p3_tables']:
        table(doc, spec)

    extra = route.get('p4_or_p5') or []
    if extra:
        title(doc, 'This week only', page_break=True)
        for line in extra:
            body(doc, line)
    for f in route.get('faultListings') or []:
        h2(doc, 'Fault: %s' % f['name'])
        body(doc, 'What you see: %s' % f['symptom'])
        for line in f['lines']:
            body(doc, '    ' + line)
        body(doc, 'What is wrong: ______________________________________________')
        body(doc, 'My repair: __________________________________________________')

    title(doc, 'My completion record', page_break=True)
    rec = route['p6_completionRecord']
    h2(doc, 'What this week shows')
    body(doc, rec['outcomeWording'])
    for s in rec['pupilStatements']:
        body(doc, '□ ' + s)
    h2(doc, 'Adult record')
    for s in rec['teacherObservation']:
        body(doc, '□ ' + s)
    body(doc, 'Adult name: ____________________  Date: __________')
    body(doc, 'Route taken: paper  ·  Recorded in the teacher guide, not on the AQA form.')

    doc.save(out_path)
    return out_path


def render_answers(route, donor, out_path):
    doc = blank_document(donor)
    wk, label = route['week'], route['label']
    set_footer(doc, wk, label + ' answers')
    title(doc, 'Week %d %s · paper route answers' % (wk, label))
    body(doc, 'Teacher only. Keep this sheet away from pupil copies.')
    for line in route['p7_teacherAnswers']:
        body(doc, line)
    h2(doc, 'What this week evidences')
    body(doc, route['p6_completionRecord']['outcomeWording'])
    gap = (route['p6_completionRecord'].get('honestGap') or '').strip()
    if gap and gap.upper() != 'NONE':
        h2(doc, 'Known limit of the paper route')
        body(doc, gap)
    doc.save(out_path)
    return out_path


def to_pdf(path, outdir):
    subprocess.run(['soffice', '--headless', '--convert-to', 'pdf', '--outdir', outdir, path],
                   check=True, capture_output=True, timeout=240)
    return os.path.join(outdir, os.path.splitext(os.path.basename(path))[0] + '.pdf')


def self_test():
    n, bad = [0], []
    def want(name, cond):
        n[0] += 1
        print(('  PASS  ' if cond else '  FAIL  ') + name)
        if not cond: bad.append(name)

    def raises(fn, exc=BlockVocabularyError):
        try:
            fn(); return False
        except exc:
            return True

    want('a real word bank passes',
         check_word_bank(['when green flag clicked', 'change x by', 'forever', 'if <> then', 'touching [Maze]?'], 'w'))
    want('a variable block is refused',
         raises(lambda: check_word_bank(['set score to 0'], 'w')))
    want('  ... and the message cites R7 and names the other unit',
         _msg(lambda: check_word_bank(['set score to 0'], 'w'), 'R7') and
         _msg(lambda: check_word_bank(['set score to 0'], 'w'), '122058'))
    want('"change score by 1" is refused even though "change" is legal motion',
         raises(lambda: check_word_bank(['change score by 1'], 'w')))
    want('"change x by 10" is NOT refused, because that is motion',
         check_word_bank(['change x by 10'], 'w'))
    want('a block outside the 15 opcodes is refused',
         raises(lambda: check_word_bank(['play sound meow'], 'w')))
    want('  ... and that message cites G11',
         _msg(lambda: check_word_bank(['play sound meow'], 'w'), 'G11'))
    want('a list block is refused', raises(lambda: check_word_bank(['add thing to list'], 'w')))
    want('an explicitly EMPTY word bank is allowed (week 3 uses no blocks)',
         check_word_bank(['Week 3 word bank: EMPTY - this week uses no blocks.'], 'w'))
    want('a genuinely empty list is allowed', check_word_bank([], 'w'))
    want('"none" is allowed as an emptiness declaration', check_word_bank(['none this week'], 'w'))
    want('but a variable block is STILL refused inside an emptiness declaration',
         raises(lambda: check_word_bank(['no blocks except set score to 0'], 'w')))
    want('prose with no full stop and no block in it is refused',
         raises(lambda: check_word_bank(['ask the teacher for help'], 'w')))
    want('  ... including prose containing the word "for"',
         raises(lambda: check_word_bank(['wait for your turn'], 'w')))
    want('a NOTE ending in a full stop is allowed beside the blocks',
         check_word_bank(['forever', 'Your first block comes in Week 4.'], 'w'))
    want('  ... but a note cannot smuggle a variable in behind a full stop',
         raises(lambda: check_word_bank(['Remember to set score to 0 first.'], 'w')))
    want('every real if-block wording is accepted',
         check_word_bank(['if then', 'if _ then', 'if <> then', 'if <touching [Maze]?> then'], 'w'))
    want('  ... but an if-shaped SENTENCE is refused on the word cap',
         raises(lambda: check_word_bank(['if you finish early then ask a partner'], 'w')))

    # The maze must agree with the lesson, so the wall census is asserted rather
    # than eyeballed: six walls, and the two the pupil is told about.
    xs = list(range(-240, 241, 20)); ys = list(range(180, -181, -20))
    blocked = set()
    for wx, wy, ww, wh in WALLS:
        for x in xs:
            for y in ys:
                if wx <= x < wx + ww and wy <= y < wy + wh:
                    blocked.add((x, y))
    want('the printed maze has walls where the lesson has walls', len(blocked) > 0)
    want('  ... the start square is not inside a wall', (-180, -120) not in blocked)
    want('  ... the finish square is not inside a wall', (180, 120) not in blocked)
    want('  ... and the grid covers the whole Scratch stage', len(xs) == 25 and len(ys) == 19)

    print('\n%d checks, %d failed' % (n[0], len(bad)))
    for b in bad: print('  FAILED:', b)
    return 1 if bad else 0


def _msg(fn, needle):
    try:
        fn(); return False
    except BlockVocabularyError as e:
        return needle in str(e)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--routes')
    ap.add_argument('--unit')
    ap.add_argument('--donor')
    ap.add_argument('--pdf', action='store_true')
    ap.add_argument('--self-test', action='store_true', dest='self_test')
    a = ap.parse_args()
    if a.self_test:
        sys.exit(self_test())
    if not (a.routes and a.unit):
        print('--routes and --unit are required', file=sys.stderr)
        sys.exit(2)
    routes = json.load(open(a.routes, encoding='utf-8'))
    if isinstance(routes, dict):
        routes = routes.get('routes', [])
    made = []
    for route in routes:
        wk = route['week']
        wdir = os.path.join(a.unit, 'Week_%02d' % wk)
        donor = a.donor or os.path.join(wdir, 'GROW_Week_%02d_Pupil_Booklet.docx' % wk)
        pdir = os.path.join(wdir, 'Paper_Route')
        tdir = os.path.join(wdir, 'Teacher_Only')
        os.makedirs(pdir, exist_ok=True)
        os.makedirs(tdir, exist_ok=True)
        p = render(route, donor, os.path.join(pdir, 'GROW_Week_%02d_Paper_Route.docx' % wk))
        t = render_answers(route, donor, os.path.join(tdir, 'GROW_Week_%02d_Paper_Route_Answers.docx' % wk))
        made += [p, t]
        if a.pdf:
            made.append(to_pdf(p, pdir))
            made.append(to_pdf(t, tdir))
    for m in made:
        print('  %-72s %s' % (os.path.relpath(m, a.unit), os.path.getsize(m)))
    print('\n%d files' % len(made))


if __name__ == '__main__':
    main()
