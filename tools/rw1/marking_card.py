#!/usr/bin/env python3
"""RW1 §4.2-§4.5 · the Lundy layer becomes an assessment layer.

Removes the "Lundy alongside learning" staff desk card and puts one
"Feedback and marking · this lesson" card in its place, per lesson.

PROVENANCE, and it is labelled at the moment of writing because that is now a
standing rule (GW1 A6): a reconstruction that enters the record is later quoted
as source.

  SOURCE OF THE EIGHT CODES: ORDER GW1 §A3, Matt's own transcription of the two
  columns from Feedback & Marking Policy 2025/2026, Issue 1, May 2026 (Earwig
  version). RW1-B §J1 rules that Matt's own written expansions ARE a C2 source.
  DOCUMENT NOT SEEN. GW1 §A1 states sha256
  aa41d67963846cf35e9bb6e53e708c7b46725c2d5cef432c2e1994a78e434e53 and asks that
  it be verified against the file in the session. The file is NOT in the session
  -- no upload matches it and it is not in either return-week zip -- so that hash
  is ASSERTED, NOT VERIFIED. Say so on the card. When the document arrives,
  verify the hash and upgrade the provenance line; do not upgrade it before.

STRUCK under GW1 §A2 as contaminated -- a reconstruction of mine that entered the
record and was then quoted back as source: "Yellow Box", "green pen", "pupil
responds in their own colour", "EFL". They are not in the policy.

The five cause reads are not invented either: they are compressed, one line each,
from the removed desk card's own three-column table, which is authored pack
content.
"""
import re

POLICY_SRC = '_sciv3/build/POLICY_ALIGNMENT.md'
POLICY_ALIGN_SHA = '9d16fb2c'

# The document's own two columns, verbatim, in source order (GW1 A3). The third
# theory-mapping column is deliberately not reproduced.
CODES = [
    ('VF',      'Verbal feedback given here'),
    ('WS',      'Worked with support'),
    ('I',       'Independent'),
    ('NS + &hellip;', 'Next step one specific thing'),
    ('E',       'Evidence on Earwig'),
    ('R',       'Responded loop closed (Audience has happened)'),
    ('//',      'Self-edit point'),
    ('?',       'Read this back to me'),
]
MARGIN_EDIT = 'in the same colour, on the same page'
POLICY = ('Feedback &amp; Marking Policy 2025/2026, Issue 1, May 2026 (Earwig version)')
POLICY_SHA = 'aa41d679&hellip;'  
VOICE = ('point, sign, verbal response, demonstration, re-attempt, edit or '
         'authorised short clip')
AUDIENCE = 'an adult genuinely receives the response'

LESSONS = {
    # Authored teaching content, one block per pathway. Keyed by pathway so a
    # fix to the card's SHAPE lands once and reaches both, while the content
    # stays separate -- the two pathways teach different lessons.
    'BUILD': {
        'A': dict(
            id='W8A', title='Sugar Evidence: Read the Label',
            brand='BUILD &middot; Science &middot; Week 8A &middot; Explore',
            prompts=[
                ('Supported', 'This value is per serving and that one is per 100&nbsp;g. Show me the two numbers you compared.'),
                ('Standard',  'You have used total carbohydrate. Find the sugars line and say what changes.'),
                ('Stretch',   'Your claim is wider than your evidence. Rewrite it so it says only what these four labels show.'),
            ],
            causes=[
                ('Secure',              'reads and orders all four values with the basis',      'teach one mixed-basis comparison using equal masses'),
                ('Mixed',               'orders correctly but drops the unit or basis',          'model reading one complete sugar line'),
                ('Misconception',       'uses carbohydrate, or calls the lowest-sugar item healthiest', 'model the sugar row and one bounded comparison'),
                ('Access barrier',      'can explain orally but cannot read the small label',    'present one enlarged label and let the pupil point'),
                ('Method or data',      'one card uses a serving basis',                          'replace it with matched-basis data before comparing'),
            ],
            wedo='We do &middot; order the labels',
            arrival_heading='Arrival line &mdash; say this once, then start',
            arrival=('&ldquo;I&rsquo;ve been out for a while and I haven&rsquo;t seen what you&rsquo;ve been '
                     'doing, so I&rsquo;m not going to pretend I have. Today I start from what you show me.&rdquo;'),
            arrival_note=('One sentence, at arrival, said once. Not an explanation, not an apology, not an '
                          'invitation for pupils to account for the gap, and not a discussion topic.'),
        ),
        'B': dict(
            id='W8B', title='Body Science Checkpoint',
            brand='BUILD &middot; Science &middot; Week 8B &middot; Do',
            prompts=[
                ('Supported', 'You have written that the bone pushes the muscle. Show me which one pulls.'),
                ('Standard',  'You have named a job the skeleton does. Add the clue that shows it.'),
                ('Stretch',   'Check your food-chain arrow. Say what it is pointing at and why.'),
            ],
            causes=[
                ('Secure',              'names the job and gives the clue that establishes it',  'ask for a second clue from a different body system'),
                ('Mixed',               'names the job but the clue belongs to another job',      'model one job and its clue, then re-ask'),
                ('Misconception',       'says the bone pushes the muscle, or reverses the arrow', 'demonstrate the pair pulling, then re-draw one arrow'),
                ('Access barrier',      'can point to it on the model but cannot write it',       'take the answer by pointing and scribe it'),
                ('Method or data',      'the evidence card does not carry the clue needed',       'swap in a card that does before judging the answer'),
            ],
            wedo='We do &middot; match the evidence',
            arrival_heading='Arrival line',
            arrival=('&ldquo;Last lesson your evidence showed __, so today we&rsquo;re starting with __.&rdquo;'),
            arrival_note=('The ordinary inheritance line returns here, and it names W8A&rsquo;s evidence '
                          'specifically &mdash; by now there is a lesson this teacher has actually seen.'),
        ),
    },
    # Measured/authored by the GW1-B survey. _lesson() refuses a missing block
    # rather than falling back to BUILD's, which is how a reconstruction from
    # one pathway once became the source for another.
    'GROW': {},
}


def _lesson(k, pw):
    block = LESSONS.get(pw['name'] if isinstance(pw, dict) else pw)
    if not block or k not in block:
        raise KeyError(
            'marking card: no authored content for pathway %r lesson %r. '
            'Author it in LESSONS; do not reuse the other pathway\'s.'
            % ((pw['name'] if isinstance(pw, dict) else pw), k))
    return block[k]

# Staff surface only (RW1-A B3): the dated header stays on the four staff
# sheets and never reaches a pupil one. Same week for both pathways -- it is
# the same return week -- so it is one constant, not a per-pathway one.
WEEK = 'Week 8 &middot; w/c 19 October 2026'


def causes_line(k, pw):
    """§4.5: if the sheet will not fit, compress the five cause reads to a single
    line of five labels BEFORE dropping any policy content -- the codes and the
    R-gate are why the sheet exists. After the GW1 A3 retrofit the code table
    grew and both cards overflowed A4 (W8A by 62px, W8B by 40px), so the PRINT
    variant takes the compressed line. The on-page card keeps the full table:
    one A4 side is a print constraint, and nothing is lost on screen."""
    return ('<p class="mk-causes-line"><b>Read the cause, not the child:</b> '
            + ' &middot; '.join(c[0] for c in _lesson(k, pw)['causes']) + '.</p>')


def _body(k, pw, compact=False):
    L = _lesson(k, pw)
    rows = ''.join(
        '<tr><td><b>%s</b></td><td>%s</td><td>%s</td></tr>' % c for c in L['causes'])
    prompts = ''.join(
        '<li><b>%s</b> &mdash; %s</li>' % p for p in L['prompts'])
    return (
      '<h4>Codes</h4>'
      '<div class="science-table-wrap"><table class="science-table mk-codetable"><tbody>'
      + ''.join('<tr><td class="mk-code">%s</td><td>%s</td></tr>' % c for c in CODES)
      + '</tbody></table></div>'
      '<p class="mk-small">Margin edits: ' + MARGIN_EDIT + '.</p>'

      '<h4>The R gate</h4>'
      '<ul class="mk-gate"><li><b>Voice</b> &mdash; ' + VOICE + '.</li>'
      '<li><b>Audience</b> &mdash; ' + AUDIENCE + '.</li>'
      '<li><b>R</b> only when both happened.</li></ul>'

      '<h4>NS + &hellip; prompts, one per route</h4><ul class="mk-prompts">' + prompts + '</ul>'

      + (causes_line(k, pw) if compact else
         '<h4>Read the cause, not the child</h4>'
         '<div class="science-table-wrap"><table class="science-table mk-causes"><thead><tr>'
         '<th scope="col">Cause</th><th scope="col">What you see</th>'
         '<th scope="col">Next teaching move</th></tr></thead><tbody>' + rows + '</tbody></table></div>')
      +

      '<h4>Involvement moment &mdash; ' + L['wedo'] + '</h4>'
      '<p>Pupil voice is invited here and can be recorded as <b>VF</b>. Voice is ' + VOICE + ' &mdash; '
      'pointing, signing, demonstrating and re-attempting all count, not only speaking.</p>'

      '<h4>' + L['arrival_heading'] + '</h4>'
      '<p class="mk-script">' + L['arrival'] + '</p>'
      '<p class="mk-small">' + L['arrival_note'] + '</p>'

      '<p class="mk-small mk-prov">Codes from ' + POLICY + '. Voice and Audience from '
      '<code>' + POLICY_SRC + '</code> (sha256 ' + POLICY_ALIGN_SHA + '&hellip;), the repository&rsquo;s '
      'hash-pinned alignment record. The policy document itself was <b>not in the session</b> when this '
      'card was built, so its stated hash ' + POLICY_SHA + ' is asserted, not verified.</p>')


def card(k, pw):
    """The on-page staff card. teacher-only AND data-mbm-guide="staff" (RW1 4.4)."""
    return ('<section class="teacher-only mk-card" data-mbm-guide="staff" id="marking-card">'
            '<h3>Feedback and marking &middot; this lesson</h3>'
            '<p class="mk-small">Staff copy &mdash; not for pupil books. Codes live in books, never on '
            'pupil slides or printouts.</p>'
            '<p><button type="button" class="ghost" onclick="printSection(\'marking\',\'standard\')">'
            'Print marking card, A4</button></p>'
            + _body(k, pw) + '</section>')


def print_section(k, pw):
    """§4.5 · its own print route, on the existing printSection(id,level) mechanism.
    printSelectors sweeps .print-section, so printing this hides every other one."""
    L = _lesson(k, pw)
    return ('<section class="print-section mk-print" id="print-marking">'
            '<header class="mk-head"><p>' + L['brand'] + ' &middot; ' + WEEK + '</p>'
            '<h2>Feedback and marking &middot; ' + L['id'] + '</h2>'
            '<p class="mk-staffonly">Staff copy &mdash; not for pupil books.</p></header>'
            + _body(k, pw, compact=True) +
            '<footer class="mk-foot"><p>Made by Matt</p></footer></section>')


CSS = (
 '.mk-card{margin:18px 0}'
 '.mk-small{font-size:.82rem;color:#475569}'
 '.mk-codetable td{font-size:.88rem;padding:3px 7px}'
 '.mk-code{font-family:ui-monospace,Menlo,Consolas,monospace;font-weight:700;white-space:nowrap;width:1%}'
 '.mk-script{font-style:italic;border-left:3px solid #94a3b8;padding-left:10px}'
 '.mk-causes td,.mk-causes th{font-size:.86rem;padding:4px 6px}'
 '.mk-causes-line{font-size:.86rem}'
 '@media print{'
 '.mk-print{font-size:9.4pt;line-height:1.28}'
 '.mk-print h2{font-size:13pt;margin:2pt 0 4pt}'
 '.mk-print h4{font-size:9.8pt;margin:6pt 0 2pt;page-break-after:avoid;break-after:avoid}'
 '.mk-print p,.mk-print li{margin:2pt 0}'
 '.mk-print .science-table-wrap,.mk-print table,.mk-print .mk-gate{page-break-inside:avoid;break-inside:avoid}'
 '.mk-print .mk-causes td,.mk-print .mk-causes th{padding:2pt 3pt;font-size:8.4pt}'
 '.mk-print .mk-head{border-bottom:1.5pt solid #000;padding-bottom:2pt;margin-bottom:4pt}'
 '.mk-print .mk-staffonly{font-weight:700;text-transform:uppercase;letter-spacing:.06em;font-size:8pt}'
 '.mk-print .mk-foot{border-top:.75pt solid #000;margin-top:4pt;padding-top:2pt;font-size:7.6pt}'
 '.mk-print .mk-prov{font-size:7.4pt}'
 '}')
