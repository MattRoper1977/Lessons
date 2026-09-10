#!/usr/bin/env python3
"""RW1-B §I1 · nine stage-specific TA prompts per lesson.

The pack repeats one sentence nine times. Live carried nine DISTINCT prompts.
A prompt that never changes trains staff to stop reading it, so the repetition
is a regression even though the count matches.

Each prompt names THAT STAGE'S OWN EVIDENCE. Staff-facing only -- the attribute
feeds the guide-gated #ta-dialog, never a pupil surface -- so the pupil delta is
zero and RW1-A B6's four-item ceiling is untouched. No policy dependency.

Stage 1, the overview, keeps the pack's generic sentence, as I1 directs.
"""
GENERIC = 'Which piece of evidence supports your answer? Show us where.'

PROMPTS = {
 'BUILD': {
 'A': [GENERIC,
   'Point to the part of the label you used, and name it before you say the number.',
   'Show me the sugars line, not the carbohydrate line. What number is on it?',
   'Say all three: the number, the unit, and what it is per. Leaving one out changes the answer.',
   'You moved that one. Which value made you move it?',
   'Are these two on the same basis? Show me where each label says per 100 g.',
   'Read your own order back to me. Does every step still hold?',
   'Your claim says more than four labels can show. Trim it to what you can point at.',
   'On the ticket, show me which label answered it, not only what the answer was.'],
 'B': [GENERIC,
   'Which muscle is pulling here? Show me the one that is letting go.',
   'Point to the joint you mean. What moves, and what stays still?',
   'Name the job, then give me the clue that shows it. The clue is the part that counts.',
   'You matched those two. Say what connects them, in your own words.',
   'What job does that nutrient do in the body? Say the job, not the food.',
   'Which way is the arrow pointing, and what is it carrying?',
   'Where does this model stop being true? Name one thing it cannot show.',
   'On the ticket, show me the evidence you used, not only your conclusion.'],
 },
 # Authored by the GW1-B survey pass. Absent, not copied: nine BUILD prompts on a
 # GROW lesson would be nine prompts naming evidence that lesson does not have,
 # which is the same defect as nine identical ones wearing a different disguise.
 'GROW': {},
}


def apply(text, which, pw):
    """Replace the nine data-prompt values in document order. Idempotent: the
    generic sentence survives at stage 1, so re-running is a no-op after the
    first pass except where a value still equals the generic beyond stage 1."""
    import re
    name = pw['name'] if isinstance(pw, dict) else pw
    block = PROMPTS.get(name) or {}
    if which not in block:
        raise KeyError('ta prompts: no authored prompts for pathway %r lesson %r. '
                       'Author them; do not reuse the other pathway\'s.' % (name, which))
    vals = block[which]
    out, i, n = [], 0, [0]

    def sub(m):
        k = n[0]; n[0] += 1
        return 'data-prompt="%s"' % (vals[k] if k < len(vals) else m.group(1))

    text = re.sub(r'data-prompt="([^"]*)"', sub, text)
    return text, n[0]
