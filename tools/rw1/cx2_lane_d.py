#!/usr/bin/env python3
"""CX2 §8.3 Lane D · the post-build edits the return-week lessons need under the
Curriculum Policy alignment (docs/orders/LESSON_STANDARD_2026-27.md, Part B).

The return-week pack sources are not in this repository, so tools/rw1/apply_rw1.py
cannot be re-run. The built bytes on claude/rw1-w8-return-week are carried and
edited here by EXACT string replacement, every anchor counted and asserted, so a
second run changes nothing and --check reports the state without writing.

Steps, per file:
  cards   B2  the E code carries the R10 wording (no product name anywhere in a
              public file); the provenance line cites the policy as VERIFIED with
              its full SHA-256 (the document reached the session on 2026-09-15);
              the Curriculum Policy §14.3 summary line and its delta sit under the
              code table; BUILD and GROW cards lead with VF and carry no
              written-comment expectation on practical or exit tasks; the LAUNCH
              card names written feedback for extended writing only.
  dates   §8.3 dated week labels off every pupil surface. BUILD W8B's six pupil
              exit tickets (three routes x two copies) carried "Week of 19 October"
              inside their SVG; the census missed it (pattern narrower than the
              property, RW1-E §C3 family) and is widened in the same change.
  labels  B3  every exit and arrival names the response modes as labels, not
              inputs: say, write, draw, sign, choose/point, show, adult scribes.
  links   B4  one real-world link in the STAFF notes (TA brief): Build practical
              everyday; Grow subject-career; Launch destination/qualification.

    python3 tools/rw1/cx2_lane_d.py [--check] [paths...]
"""
import argparse, sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]

POLICY_SHA = '41046284a00c9218679b946134cbc6e53c1897aad28b15fc4bd4aa963720ff3b'
ALIGN_SHA = '9d16fb2cbb314bd883ece6eb9249f268fa5bee0a82f48c3be229df551ad722d8'
E_MEANING = 'Evidence captured on the school&rsquo;s digital evidence platform'

SUMMARY = ('<p class="mk-small mk-summary">Curriculum Policy 2026/27 &sect;14.3 summary: VF WS I NS E R '
           '(six codes; NS &ldquo;next step&rdquo;, E &ldquo;evidence on digital software app&rdquo;, R '
           '&ldquo;responded to feedback&rdquo;). The Feedback Policy, the code source, adds // and ? and '
           'expands NS to one specific thing and R to loop closed.</p>')
LEAD_VF = ('<p class="mk-lead">Lead with <b>VF</b>. Practical and exit tasks carry no written-comment '
           'expectation (Curriculum Policy 2026/27 &sect;14.3: written marking where it adds value, typically '
           'Launch GCSE and Functional Skills writing).</p>')
LEAD_LAUNCH = ('<p class="mk-lead">Lead with <b>VF</b> in the practical and exit tasks. Written feedback is for '
               'extended writing only, strategic and not every piece (Curriculum Policy 2026/27 &sect;14.3).</p>')

BUILD_PROV_OLD = ('<p class="mk-small mk-prov">Codes from Feedback &amp; Marking Policy 2025/2026, Issue 1, May 2026 '
                  '(Earwig version). Voice and Audience from <code>_sciv3/build/POLICY_ALIGNMENT.md</code> (sha256 '
                  '9d16fb2c&hellip;), the repository&rsquo;s hash-pinned alignment record. The policy document itself '
                  'was <b>not in the session</b> when this card was built, so its stated hash aa41d679&hellip; is '
                  'asserted, not verified.</p>')
BUILD_PROV_NEW = ('<p class="mk-small mk-prov">Codes from the Feedback &amp; Marking Policy 2025/2026 (Pilot), Issue 1, '
                  'May 2026, verified in session 2026-09-15 (SHA-256 ' + POLICY_SHA + '). Voice and Audience from '
                  '<code>_sciv3/build/POLICY_ALIGNMENT.md</code> (SHA-256 ' + ALIGN_SHA + '), the repository&rsquo;s '
                  'hash-pinned alignment record.</p>')
GL_FOOT_OLD = ('<footer>Made by Matt · Feedback &amp; Marking Policy 2025/2026 · Issue 1, May 2026 · Code/Meaning '
               'columns, printed p. 10</footer>')
GL_FOOT_NEW = ('<footer>Made by Matt · Feedback &amp; Marking Policy 2025/2026 (Pilot) · Issue 1, May 2026 · '
               'Code/Meaning columns, printed p. 10 · verified in session 2026-09-15, SHA-256 ' + POLICY_SHA + '</footer>')

# Response-mode labels (B3). Pupil-facing, so plain words.
BUILD_EXIT_OLD = '<p>Show what you understand. Use your book or one printed ticket. Write, draw, point or explain.</p>'
BUILD_EXIT_NEW = ('<p>Show what you understand. Use your book or one printed ticket. Write, draw, point, sign or '
                  'explain. An adult can write your words for you.</p>')
BUILD_SVG_OLD = 'Write, draw, point or explain. You can use the same questions in your book.'
BUILD_SVG_NEW = 'Write, draw, point, sign or explain. An adult can write it for you. Use the same questions in your book.'
ARRIVAL_OLD = '<p>Say, point, draw or write. An adult may read the questions.</p>'
ARRIVAL_NEW = '<p>Say, point, draw, sign or write. An adult may read the questions or write your answer for you.</p>'
GL_EXIT_OLD = '<p>Use your book OR one ticket. Show your explanation with the supplied evidence.</p>'
GL_EXIT_NEW = ('<p>Use your book OR one ticket. Show your explanation with the supplied evidence. Say it, write it, '
               'draw it, sign it, choose it or show it; an adult can scribe it.</p>')
GL_PRINT_EXIT_LINE = '<p class="response-modes">Say it, write it, draw it, sign it, choose it or show it; an adult can scribe it.</p>'
BUILD_DATED_TICKET = 'Body Science Checkpoint  •  Week of 19 October'
BUILD_TICKET = 'Body Science Checkpoint'

LINKS = {
    'SCI_B_W8B': ('Real-world link', 'Practical, everyday link (Build): reading the label on a lunch or a snack to '
                  'spot protein, carbohydrate and calcium; lifting a school bag to feel the biceps pull while the '
                  'triceps lets go.'),
    'SCI_G_W8A': ('Real-world link', 'Subject&ndash;career link (Grow): pilots, port and ship shift planners and weather '
                  'forecasters plan around sunrise and sunset times, and those times come from the same '
                  'Earth-rotation model this lesson uses.'),
    'SCI_G_W8B': ('Real-world link', 'Subject&ndash;career link (Grow): a 24-hour control room, an airport or a hospital '
                  'runs on day and night shifts planned from the same rotation model; the timeline task is the '
                  'kind of chart a shift planner reads.'),
    'SCI_L_W8L1': ('Real-world link', 'Destination link (Launch): this planning work is GCSE Biology core-practical '
                   'ground; the same enzyme and method skills are used in food and drink production and in '
                   'hospital and diagnostic laboratories, and lead on to Level 3 science and laboratory '
                   'apprenticeships.'),
    'SCI_L_W8L2': ('Real-world link', 'Destination link (Launch): the amylase and pH core practical is examined in GCSE '
                   'Biology; enzyme assays like it are routine in brewing, baking and clinical laboratories, '
                   'and a Level 3 science or laboratory-technician route builds directly on it.'),
    'SCI_L_W8L3': ('Real-world link', 'Destination link (Launch): rate calculations from timed observations are GCSE '
                   'Biology exam skills and the everyday work of laboratory technicians, quality-control '
                   'testers and biomedical science routes at Level 3 and beyond.'),
}

FILES = [
    'Science_Teesside/Build/W8-W13_2026-27/SCI_B_W8B_Autumn_Science_Checkpoint_Do.html',
    'Science_Teesside/Grow/W8-W13_2026-27/SCI_G_W8A_Day_And_Night_Explore.html',
    'Science_Teesside/Grow/W8-W13_2026-27/SCI_G_W8B_Day_And_Night_Do.html',
    'Science_Teesside/Launch/W8-W13_2026-27/SCI_L_W8L1_Enzyme_Action_Introduce.html',
    'Science_Teesside/Launch/W8-W13_2026-27/SCI_L_W8L2_Amylase_pH_Core_Practical_Explore.html',
    'Science_Teesside/Launch/W8-W13_2026-27/SCI_L_W8L3_Amylase_Rate_And_Topic_1_Do.html',
]


class Edit:
    """Replace `old` with `new` exactly `n` times. Already-applied counts as done;
    any other count is a loud failure, never a silent no-op."""
    def __init__(self, name, old, new, n=1):
        self.name, self.old, self.new, self.n = name, old, new, n

    def apply(self, text):
        have, done = text.count(self.old), text.count(self.new)
        if done >= self.n:
            # `new` may contain `old` (an insertion beside an anchor), so test "done" first.
            return text, 'already'
        if have == self.n and done == 0:
            return text.replace(self.old, self.new), 'applied'
        raise SystemExit('[FAIL] %s: found %d of %d anchors, %d already applied' % (self.name, have, self.n, done))


def section(text, id_):
    """The exact bytes of one <section id=...> ... </section>, by balanced walk."""
    i = text.find('id="%s"' % id_)
    assert i >= 0, id_
    start = text.rfind('<section', 0, i)
    depth, j = 0, start
    while j < len(text):
        if text.startswith('<section', j):
            depth += 1; j += 8
        elif text.startswith('</section>', j):
            depth -= 1; j += 10
            if depth == 0:
                return start, j
        else:
            j += 1
    raise AssertionError(id_)


def insert_after_in_section(text, id_, anchor, addition, name, n=1):
    """Insert `addition` after each of exactly `n` anchors inside one section."""
    a, b = section(text, id_)
    seg = text[a:b]
    if seg.count(addition) >= n:
        return text, 'already'
    assert seg.count(anchor) == n, '%s: %d anchors in #%s, expected %d' % (name, seg.count(anchor), id_, n)
    seg = seg.replace(anchor, anchor + addition)
    return text[:a] + seg + text[b:], 'applied'


def edits_for(rel):
    stem = Path(rel).name
    key = next(k for k in LINKS if stem.startswith(k))
    pw = 'BUILD' if key.startswith('SCI_B') else 'GROW' if key.startswith('SCI_G') else 'LAUNCH'
    plain = []
    if pw == 'BUILD':
        plain += [
            Edit('E code (R10)', '<td class="mk-code">E</td><td>Evidence on Earwig</td>',
                 '<td class="mk-code">E</td><td>' + E_MEANING + '</td>', 2),
            Edit('provenance verified', BUILD_PROV_OLD, BUILD_PROV_NEW, 2),
            Edit('§14.3 summary', '<p class="mk-small">Margin edits: in the same colour, on the same page.</p>',
                 SUMMARY + '<p class="mk-small">Margin edits: in the same colour, on the same page.</p>', 2),
            Edit('VF lead (card)', '<p class="mk-small">Staff copy &mdash; not for pupil books. Codes live in books, never on pupil slides or printouts.</p>',
                 '<p class="mk-small">Staff copy &mdash; not for pupil books. Codes live in books, never on pupil slides or printouts.</p>' + LEAD_VF, 1),
            Edit('VF lead (print)', '<p class="mk-staffonly">Staff copy &mdash; not for pupil books.</p>',
                 '<p class="mk-staffonly">Staff copy &mdash; not for pupil books.</p>' + LEAD_VF, 1),
            Edit('dated pupil exit tickets', BUILD_DATED_TICKET, BUILD_TICKET, 6),
            Edit('exit slide modes', BUILD_EXIT_OLD, BUILD_EXIT_NEW, 1),
            Edit('exit ticket modes (SVG)', BUILD_SVG_OLD, BUILD_SVG_NEW, 6),
            Edit('arrival print modes', ARRIVAL_OLD, ARRIVAL_NEW, 3),
        ]
        link_anchor = '<h3>Preparation and teaching</h3>'
    else:
        plain += [
            Edit('E code (R10)', '<td>E</td><td>Evidence on Earwig</td>', '<td>E</td><td>' + E_MEANING + '</td>', 1),
            Edit('provenance verified', GL_FOOT_OLD, GL_FOOT_NEW, 1),
            Edit('exit slide modes', GL_EXIT_OLD, GL_EXIT_NEW, 1),
            Edit('arrival print modes', ARRIVAL_OLD, ARRIVAL_NEW, 3),
        ]
        link_anchor = '<h3>Preparation</h3>'
    return pw, key, plain, link_anchor


def process(rel, check):
    path = REPO / rel
    text = before = path.read_text()
    pw, key, plain, link_anchor = edits_for(rel)
    log = []
    for e in plain:
        text, state = e.apply(text); log.append((e.name, state))
    if pw != 'BUILD':
        # §14.3 summary after the code table, and the VF lead after "Staff copy", both inside #print-marking only
        # (the first-lesson-back card carries the same "Staff copy" line and must not gain a marking rule).
        text, s = insert_after_in_section(text, 'print-marking', '</table>', SUMMARY, '§14.3 summary'); log.append(('§14.3 summary', s))
        lead = LEAD_LAUNCH if pw == 'LAUNCH' else LEAD_VF
        text, s = insert_after_in_section(text, 'print-marking', '<p><strong>Staff copy — not for pupil books</strong></p>', lead, 'VF lead'); log.append(('VF lead', s))
        for route in ('supported', 'standard', 'stretch'):
            # each exit sheet prints two copies of the ticket, so the heading appears twice
            text, s = insert_after_in_section(text, 'print-exit-' + route, '<h2>Exit ticket</h2>', GL_PRINT_EXIT_LINE, 'exit print modes', n=2); log.append(('exit print modes ' + route, s))
    # B4 staff link inside the TA brief, after the preparation paragraph
    head, body = LINKS[key]
    addition = '<h3>' + head + '</h3><p class="rw-link">' + body + '</p>'
    if addition in text:
        log.append(('staff link', 'already'))
    else:
        k = text.find(link_anchor); assert k >= 0 and text.count(link_anchor) == 1, 'link anchor in ' + rel
        pend = text.find('</p>', k) + 4
        text = text[:pend] + addition + text[pend:]; log.append(('staff link', 'applied'))
    import re
    for banned in (r'\bEarwig\b', r'\bCypher\b', r'\bEfL\b', r'\bEFL\b', 'asserted, not verified', 'Yellow Box', 'green pen'):
        # word-bounded: the bare substring "EFL" also occurs inside base64 image data
        m = re.search(banned, text)
        assert not m, '%s still carries %r at offset %d: %r' % (rel, banned, m.start(), text[max(0, m.start()-60):m.end()+60])
    changed = text != before
    if changed and not check:
        path.write_text(text)
    return changed, log


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--check', action='store_true', help='report without writing; non-zero if anything would change')
    ap.add_argument('paths', nargs='*')
    args = ap.parse_args()
    pending = 0
    for rel in (args.paths or FILES):
        changed, log = process(rel, args.check)
        applied = [n for n, s in log if s == 'applied']
        print('%-52s %s' % (Path(rel).name, ('WOULD CHANGE' if args.check else 'written') if changed else 'up to date'))
        for n, s in log:
            print('   [%s] %s' % ('ok' if s == 'applied' else '--', n))
        pending += changed
    if args.check and pending:
        raise SystemExit('[FAIL] %d file(s) differ from the Lane D edits' % pending)
