#!/usr/bin/env python3
"""RW1 §4.2-§4.5 · the Lundy layer becomes an assessment layer.

Removes the "Lundy alongside learning" staff desk card and puts one
"Feedback and marking · this lesson" card in its place, per lesson.

PROVENANCE, because this is policy content and reconstruction is not allowed:
the policy DOCUMENT is not in this repository. RW1-A C3 therefore binds this card
to _sciv3/build/POLICY_ALIGNMENT.md and nothing else -- a hash-pinned reviewed
archive document (sha256 9d16fb2c...), byte-identical to the digest the publisher
pins in REVIEWED_ARCHIVE_DOCUMENTS. What that document does not contain is
OMITTED and listed, never inferred: the codes' verbatim expansions, the policy's
grouping headings, "Yellow Box next step in green pen", and "pupil responds in
their own colour".

The five cause reads are not invented either: they are compressed, one line each,
from the removed desk card's own three-column table, which is authored pack
content.
"""
import re

POLICY_SRC = '_sciv3/build/POLICY_ALIGNMENT.md'
POLICY_SHA = '9d16fb2c'

# As the source document has them, in its order.
CODES = 'VF &middot; WS &middot; I &middot; NS+ &middot; E &middot; R &middot; // &middot; ?'
VOICE = ('point, sign, verbal response, demonstration, re-attempt, edit or '
         'authorised short clip')
AUDIENCE = 'an adult genuinely receives the response'

LESSON = {
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
}

WEEK = 'Week 8 &middot; w/c 19 October 2026'   # staff surface only (RW1-A B3)


def _body(k):
    L = LESSON[k]
    rows = ''.join(
        '<tr><td><b>%s</b></td><td>%s</td><td>%s</td></tr>' % c for c in L['causes'])
    prompts = ''.join(
        '<li><b>%s</b> &mdash; %s</li>' % p for p in L['prompts'])
    return (
      '<h4>Codes</h4>'
      '<p class="mk-codes">' + CODES + '</p>'
      '<p class="mk-small">Recorded as the staff-side policy reference lists them. Their wording and '
      'grouping are <b>not</b> reproduced here: the policy document is not in this repository, and '
      'reconstructing it would be inventing policy. Ask Matt to supply it.</p>'

      '<h4>The R gate</h4>'
      '<ul class="mk-gate"><li><b>Voice</b> &mdash; ' + VOICE + '.</li>'
      '<li><b>Audience</b> &mdash; ' + AUDIENCE + '.</li>'
      '<li><b>R</b> only when both happened.</li></ul>'

      '<h4>NS+ prompts, one per route</h4><ul class="mk-prompts">' + prompts + '</ul>'

      '<h4>Read the cause, not the child</h4>'
      '<div class="science-table-wrap"><table class="science-table mk-causes"><thead><tr>'
      '<th scope="col">Cause</th><th scope="col">What you see</th>'
      '<th scope="col">Next teaching move</th></tr></thead><tbody>' + rows + '</tbody></table></div>'

      '<h4>Involvement moment &mdash; ' + L['wedo'] + '</h4>'
      '<p>Pupil voice is invited here and can be recorded as <b>VF</b>. Voice is ' + VOICE + ' &mdash; '
      'pointing, signing, demonstrating and re-attempting all count, not only speaking.</p>'

      '<h4>' + L['arrival_heading'] + '</h4>'
      '<p class="mk-script">' + L['arrival'] + '</p>'
      '<p class="mk-small">' + L['arrival_note'] + '</p>'

      '<p class="mk-small mk-prov">Source: <code>' + POLICY_SRC + '</code> (sha256 ' + POLICY_SHA +
      '&hellip;), the repository&rsquo;s hash-pinned policy alignment record. '
      'Omitted pending the policy document: code expansions, the policy&rsquo;s own grouping headings, '
      'the Yellow Box / green pen mechanism, and the pupil-response colour rule.</p>')


def card(k):
    """The on-page staff card. teacher-only AND data-mbm-guide="staff" (RW1 4.4)."""
    return ('<section class="teacher-only mk-card" data-mbm-guide="staff" id="marking-card">'
            '<h3>Feedback and marking &middot; this lesson</h3>'
            '<p class="mk-small">Staff copy &mdash; not for pupil books. Codes live in books, never on '
            'pupil slides or printouts.</p>'
            '<p><button type="button" class="ghost" onclick="printSection(\'marking\',\'standard\')">'
            'Print marking card, A4</button></p>'
            + _body(k) + '</section>')


def print_section(k):
    """§4.5 · its own print route, on the existing printSection(id,level) mechanism.
    printSelectors sweeps .print-section, so printing this hides every other one."""
    L = LESSON[k]
    return ('<section class="print-section mk-print" id="print-marking">'
            '<header class="mk-head"><p>' + L['brand'] + ' &middot; ' + WEEK + '</p>'
            '<h2>Feedback and marking &middot; ' + L['id'] + '</h2>'
            '<p class="mk-staffonly">Staff copy &mdash; not for pupil books.</p></header>'
            + _body(k) +
            '<footer class="mk-foot"><p>Made by Matt</p></footer></section>')


CSS = (
 '.mk-card{margin:18px 0}'
 '.mk-small{font-size:.82rem;color:#475569}'
 '.mk-codes{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:1.05rem;letter-spacing:.04em}'
 '.mk-script{font-style:italic;border-left:3px solid #94a3b8;padding-left:10px}'
 '.mk-causes td,.mk-causes th{font-size:.86rem;padding:4px 6px}'
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
