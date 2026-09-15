#!/usr/bin/env python3
"""LW1 §B2 · one sentence, on the LAUNCH marking cards, in staff-facing text.

WHAT IT SAYS AND WHY IT IS ONE SENTENCE. The pack already labels its supplied
amylase observations honestly -- "Supplied illustrative observations, not your
practical results" on the pupil surface, and "it does not certify physical
practical completion" in the staff route-choice block of all three files. What
was missing is the same statement where a teacher records evidence: on the
marking card itself.

§B2 is explicit that this is a sentence and not a mechanism. No code, no
receipt, no new field, nothing for a pupil to fill in. It is added to W8L2 and
W8L3, the two lessons that USE the dataset; W8L1 is planning only and touches no
observations, supplied or otherwise.

Idempotent: the marker is the sentence itself.
"""
import re, sys
from pathlib import Path

LINE = ('<p class="cp-evidence"><strong>Core practical evidence.</strong> '
        'The Edexcel core practical is evidenced by the pupil doing the '
        'practical. The illustrative route evidences the interpretation skills '
        'only, and is never recorded as core practical completion.</p>')

# Immediately after the marking card's own "Staff copy" header line, so it sits
# with the rest of the recording guidance rather than at the end of the codes.
ANCHOR = re.compile(
    r'(id="print-marking"[^>]*>.*?<p><strong>Staff copy[^<]*</strong></p>)', re.S)


def apply(text):
    if 'cp-evidence' in text:
        return text, 0
    new, n = ANCHOR.subn(lambda m: m.group(1) + LINE, text, count=1)
    return new, n


if __name__ == '__main__':
    total = 0
    for p in sys.argv[1:]:
        path = Path(p)
        text = path.read_text(encoding='utf-8')
        out, n = apply(text)
        # A denominator, not a bare count: how many marking cards were there to
        # reach, and how many now carry the line?
        cards = len(re.findall(r'id="print-marking"', out))
        have = len(re.findall(r'class="cp-evidence"', out))
        assert cards, '%s has no marking card to put the line on' % p
        assert have == cards, ('%s: %d of %d marking cards carry the CP line'
                               % (p, have, cards))
        if n:
            path.write_text(out, encoding='utf-8')
        print('  %-52s %d of %d marking cards carry the line (%s)'
              % (path.name[:52], have, cards, 'added' if n else 'already present'))
        total += n
    print('  %d files edited' % total)
