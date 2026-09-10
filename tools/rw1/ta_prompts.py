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
 # LW1 §A3. All seven pack files across all three pathways ship the SAME single
 # sentence nine times -- byte-identical between BUILD, GROW and LAUNCH -- so
 # this is the generator's defect, not a pathway's. The stage each prompt belongs
 # to was established by DOM ANCESTRY (data-prompt sits on the section.slide
 # itself, one per slide, slides 1-9), not by the nearest preceding heading,
 # which is off by one.
 #
 # Each question names THAT STAGE'S OWN EVIDENCE. Stage 1 is the untimed overview
 # and keeps the generic sentence, as I1 directs. Staff-facing only -- the
 # attribute feeds the guide-gated dialog, never a pupil surface -- so the pupil
 # delta stays zero and RW1-A B6's four-item ceiling is untouched.
 'GROW': {
  'A': [GENERIC,
    'You chose that answer. What did you actually see change \u2014 the Sun, or where you are?',
    'Point to the part you mean and name it, before you say what it does.',
    'Watch the marker, not the lamp. Say where it is now, and whether it is in light or dark.',
    'You put that card there. Which position on the model made you choose it?',
    'Who is moving in that explanation \u2014 the Sun, or you? Say it again as the observer.',
    'Show me which way your sketch is facing. Which side is the light coming from?',
    'Your explanation says the Sun moves. Say it again using what actually turns.',
    'On the ticket, show me the part of the model that answered it, not only the answer.'],
  'B': [GENERIC,
    'You chose that cause. What did the observations actually record?',
    'Clouds make it darker. Say what makes it night, and what is different about the two.',
    'That is the fourth position. Has anything come back to where it started?',
    'You matched those two. Say the clue that connects them, in your own words.',
    'Read your row across. Which part is what you saw, and which part is what you think it means?',
    'Point to the recorded fact that disagrees with that explanation.',
    'Four rows, four clues. Show me the row you are least sure about, and say why.',
    'On the ticket, show me which observation you used, not only your conclusion.'],
 },
 'LAUNCH': {
  'L1': [GENERIC,
    'You picked that route. Show me the line you used to decide.',
    'Blue-black or orange-brown \u2014 say what that tells you is in the drop, not how fast it happened.',
    'Name the three steps in order. Which one is the enzyme not used up in?',
    'You put that label on that part. Say what the part does before you name it.',
    'The pH changed. Say what changed about the active site, and what you would measure.',
    'Read your sequence aloud. Which step must come before mixing, and why?',
    'Name the one thing you are changing, and one thing you are keeping the same.',
    'On the ticket, show me the supplied evidence you used, not only the conclusion.'],
  'L2': [GENERIC,
    'You picked that route. Show me the line you used to decide.',
    'Which setup is ready? Say the one thing that must be in place before anything is mixed.',
    'The reaction keeps going. Say what leaves it, and what stays in it.',
    'You placed that card there. Which decision does it change?',
    'Give me the last blue-black time and the first orange-brown time. Which one is the endpoint?',
    'That record says more than the observation shows. Trim it to what was actually seen.',
    'Show me where your record says WHEN, not only WHAT.',
    'On the ticket, show me the observation your explanation rests on.'],
  'L3': [GENERIC,
    'You picked that route. Show me the line you used to decide.',
    'A finished first. Say which has the larger rate, and why a shorter time means faster.',
    'Show the working: equation, substitution, unit. Which of the three is missing?',
    'You placed that card. Say which link it makes in the chain.',
    'Your point sits between two tested values. Say what the graph can and cannot show there.',
    'Digestion or diffusion \u2014 say which changes the molecule, and which changes where it is.',
    'Your claim is wider than five single runs. Trim it to what these points show.',
    'On the ticket, name the command word, and show that your answer does what it asks.'],
 },
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
