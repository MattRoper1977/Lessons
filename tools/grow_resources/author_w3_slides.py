"""Align the GROW W3A/W3B editable decks with the canonical Friction lesson.

Reads the exact reviewed 6 September decks from the git base recorded below and
writes the aligned decks in place. Every new shape is a deep copy of an existing
reviewed shape (fills, fonts, sizes, insets), so the deck design is unchanged.
Content comes from the same JSON that authored the screen and the DOCX/PDF:
W3A_ARRIVAL.json, W3A_ORGANISER_EXIT.json and W3_FEEDBACK.json.

Rebase BASE before running this over later deck edits.

    python3 tools/grow_resources/author_w3_slides.py [--root REPO]
"""
from copy import deepcopy
from pathlib import Path
import argparse, io, json, re, subprocess

from lxml import etree
from pptx import Presentation
from pptx.oxml.ns import qn

BASE = '929cf731173aeca8c9941cecd76cb350387499d1'
HERE = Path(__file__).resolve().parent
PACK = 'Science_Teesside/Teaching_Packs/GROW/lessons/'
A_DECK = PACK + 'W3A/GROW_Science_Autumn1_W3A_Friction.pptx'
B_DECK = PACK + 'W3B/GROW_Science_Autumn1_W3B_Friction_Test.pptx'
ARRIVAL = json.loads((HERE / 'W3A_ARRIVAL.json').read_text())
KO = json.loads((HERE / 'W3A_ORGANISER_EXIT.json').read_text())
FB = json.loads((HERE / 'W3_FEEDBACK.json').read_text())
EMU = 914400
A_NS = 'http://schemas.openxmlformats.org/drawingml/2006/main'
SOURCES = ['[Sources]',
           'https://github.com/MattRoper1977/Lessons/blob/main/Science_Teesside/Grow/SCI_G_W3_Friction.html',
           'Historical conversion source Git blob: 170d772a5e9d23909e95a534c5c1e16ee7df67c8 (read 6 September 2026). '
           'Revision 15 September 2026 aligns this deck with the canonical lesson’s four-question arrivals, '
           'knowledge organiser, two-check Lesson A exit and optional help prompt. Native editable diagrams are '
           'original explanatory models; no source publisher media copied.',
           '[/Sources]']
B_SOURCES = ['[Sources]',
             'https://github.com/MattRoper1977/Lessons/blob/main/Science_Teesside/Grow/SCI_G_W3_Friction.html',
             'Historical conversion source Git blob: 170d772a5e9d23909e95a534c5c1e16ee7df67c8. Revision 15 September '
             '2026: the four-minute review stage matches the canonical lesson’s Review the evidence and optional '
             'help prompt; no separate feedback form or standalone participation stage.',
             '[/Sources]']


def baseline(root, rel):
    data = subprocess.check_output(['git', '-C', str(root), 'show', BASE + ':' + rel])
    return Presentation(io.BytesIO(data))


def shape_by_name(slide, name):
    for shape in slide.shapes:
        if shape.name == name:
            return shape
    raise KeyError(name)


def strip_creation_ids(element):
    for ext in element.iter('{%s}extLst' % A_NS):
        parent = ext.getparent()
        if parent is not None and parent.tag == qn('p:cNvPr'):
            parent.remove(ext)


def renumber(slide):
    next_id = 2
    for el in slide.shapes._spTree.iter(qn('p:cNvPr')):
        if el.getparent().getparent().tag == qn('p:nvGrpSpPr'):
            continue
        el.set('id', str(next_id)); next_id += 1


def clone_slide(prs, src):
    """New slide with deep copies of every shape on src (src carries no pictures)."""
    new = prs.slides.add_slide(src.slide_layout)
    for shape in list(new.shapes):
        shape._element.getparent().remove(shape._element)
    src_bg = src._element.cSld.find(qn('p:bg'))
    if src_bg is not None:
        new._element.cSld.insert(0, deepcopy(src_bg))
    for el in src.shapes._spTree:
        if el.tag in (qn('p:sp'), qn('p:cxnSp'), qn('p:grpSp')):
            assert el.tag != qn('p:pic')
            copy = deepcopy(el); strip_creation_ids(copy); new.shapes._spTree.append(copy)
    renumber(new)
    return new


def move_slide(prs, old_index, new_index):
    lst = prs.slides._sldIdLst; items = list(lst); el = items[old_index]
    lst.remove(el); lst.insert(new_index, el)


def set_text(shape, text):
    body = shape.text_frame._txBody
    for extra in body.findall(qn('a:p'))[1:]:
        body.remove(extra)
    paragraph = shape.text_frame.paragraphs[0]
    runs = paragraph.runs
    runs[0].text = text
    for extra in runs[1:]:
        extra._r.getparent().remove(extra._r)


def set_paragraphs(shape, lines):
    body = shape.text_frame._txBody
    paras = body.findall(qn('a:p'))
    template = deepcopy(paras[0])
    for p in paras:
        body.remove(p)
    for line in lines:
        p = deepcopy(template)
        runs = p.findall(qn('a:r'))
        runs[0].find(qn('a:t')).text = line
        for extra in runs[1:]:
            p.remove(extra)
        body.append(p)


def set_size(shape, sz, bold=None, colour=None):
    for rpr in shape._element.iter(qn('a:rPr'), qn('a:defRPr')):
        rpr.set('sz', str(sz))
        if bold is not None:
            rpr.set('b', '1' if bold else '0')
        if colour is not None:
            clr = rpr.find(qn('a:solidFill'))
            if clr is not None:
                clr.find(qn('a:srgbClr')).set('val', colour)


def place(shape, x, y, cx, cy):
    shape.left, shape.top, shape.width, shape.height = int(x * EMU), int(y * EMU), int(cx * EMU), int(cy * EMU)


def add_from(slide, template_shape, name, x, y, cx, cy, text=None, lines=None, sz=None, bold=None, colour=None, fill=None, anchor=None):
    el = deepcopy(template_shape._element); strip_creation_ids(el)
    if anchor is not None:
        el.find(qn('p:txBody')).find(qn('a:bodyPr')).set('anchor', anchor)
    slide.shapes._spTree.append(el)
    shape = slide.shapes[-1]
    shape.name = name
    place(shape, x, y, cx, cy)
    if lines is not None:
        set_paragraphs(shape, lines)
    elif text is not None:
        set_text(shape, text)
    if sz is not None:
        set_size(shape, sz, bold, colour)
    if fill is not None:
        sf = el.find(qn('p:spPr')).find(qn('a:solidFill'))
        sf.find(qn('a:srgbClr')).set('val', fill)
    renumber(slide)
    return shape


def remove_shapes(slide, prefix_or_names):
    for shape in list(slide.shapes):
        if shape.name in prefix_or_names or any(shape.name.startswith(p) for p in prefix_or_names if p.endswith('-')):
            shape._element.getparent().remove(shape._element)


def set_notes(slide, paragraphs):
    slide.notes_slide.notes_text_frame.text = '\n'.join(paragraphs)


def notes_text(slide):
    return slide.notes_slide.notes_text_frame.text


def replace_notes(slide, replacements):
    """Exact replacement; the reviewed notes mix straight and curly apostrophes."""
    text = notes_text(slide)
    for old, new in replacements.items():
        candidates = [old, old.replace('\u2019', "'"), old.replace("'", '\u2019')]
        hit = next((c for c in candidates if c in text), None)
        assert hit is not None, (old, text[:120])
        text = text.replace(hit, new)
    set_notes(slide, text.split('\n'))


def renumber_pages(prs):
    for index, slide in enumerate(prs.slides, 1):
        set_text(shape_by_name(slide, 'page'), f'{index:02d}')


def check_no_day_words(prs):
    day = re.compile(r'\b(Monday|Tuesday|Wednesday|Thursday|Friday|P[12]\b|\d{2}:\d{2})')
    for index, slide in enumerate(prs.slides, 1):
        for shape in slide.shapes:
            if shape.has_text_frame:
                assert not day.search(shape.text_frame.text), (index, shape.name, shape.text_frame.text)
        assert not day.search(notes_text(slide)), (index, notes_text(slide))


# ----------------------------------------------------------------------------- W3A
def build_a(root):
    prs = baseline(root, A_DECK)
    slides = list(prs.slides)
    templates = {
        'row': shape_by_name(slides[8], 'line-0'), 'cue': shape_by_name(slides[8], 'cue-0'),
        'rule': shape_by_name(slides[8], 'row-rule-0'), 'access': shape_by_name(slides[1], 'access'),
        'strip': shape_by_name(slides[8], 'bins'), 'box': shape_by_name(slides[6], 'help'),
        'header': shape_by_name(slides[6], 'help-header'), 'model': shape_by_name(slides[10], 'model'),
    }
    arrival_src = slides[1]

    # ---- three arrival route slides replace the single three-line arrival
    routes = ['supported', 'standard', 'stretch']
    # The reviewed arrival slide becomes the Supported route in place; the other
    # two routes are clones of it. Nothing is deleted, so part names stay unique.
    for route in routes:
        data = ARRIVAL['routes'][route]
        slide = arrival_src if route == 'supported' else clone_slide(prs, arrival_src)
        remove_shapes(slide, ['line-', 'cue-', 'row-rule-', 'access'])
        set_text(shape_by_name(slide, 'title'), f'Arrival \u00b7 {data["label"]} route')
        add_from(slide, templates['strip'], 'strip', 0.667, 2.45, 12.0, 0.40,
                 text='FOUR QUICK QUESTIONS   /   POINT, SAY, SIGN, DRAW OR WRITE   /   YOU MAY PASS')
        positions = [(0.667, 2.95), (6.98, 2.95), (0.667, 4.33), (6.98, 4.33)]
        for i, (x, y) in enumerate(positions):
            add_from(slide, templates['box'], f'question-{i}', x, y, 5.72, 1.28,
                     text=f'{i + 1}. {data["questions"][i]}', sz=1600, fill='E7EFE9' if i % 2 == 0 else 'F0EBE3')
        add_from(slide, templates['access'], 'access', 0.667, 5.72, 12.0, 0.62, text=ARRIVAL['access'], sz=1350)
        set_notes(slide, [
            f'Arrival Task \u2014 4 minutes shared across the three route slides; show the route you have chosen. '
            'This slide is within Lesson A\u2019s existing 40-minute sequence, not extra teaching time.',
            ARRIVAL['response'] + ' Use pupil arrival page 7 (Supported), 8 (Standard) or 9 (Stretch); staff answers are '
            'on the teacher pages. Screen or paper once, not both.',
            ARRIVAL['staff'],
            f'[Staff answers \u2014 {data["label"]}; do not display]',
            *[f'{i + 1}. {answer}' for i, answer in enumerate(data['answers'])],
            '', *SOURCES])
    count = len(prs.slides)
    move_slide(prs, count - 2, 2); move_slide(prs, count - 1, 3)

    slides = list(prs.slides)   # title, arr×3, glance, ido1, demo, wedo1, job, ido2, sort, check, model, keep
    assert [s.shapes.title.text if s.shapes.title else '' for s in slides][:0] == []
    assert shape_by_name(slides[4], 'title').text_frame.text == 'Three things to work out'
    assert shape_by_name(slides[8], 'title').text_frame.text == 'The job changes the answer'

    # ---- knowledge organiser, two reference slides after Today at a Glance
    ko1 = clone_slide(prs, slides[8])   # 'The job changes the answer' two-column layout
    remove_shapes(ko1, ['help-header', 'hinder-header', 'help', 'hinder'])
    set_text(shape_by_name(ko1, 'title'), 'Friction knowledge organiser (1 of 2)')
    add_from(ko1, templates['strip'], 'objective', 0.667, 2.30, 12.0, 0.55, text='Objective: ' + KO['objective'], sz=1600)
    add_from(ko1, templates['header'], 'words-header', 0.667, 2.95, 7.30, 0.55, text='KEY WORDS', sz=1800)
    add_from(ko1, templates['box'], 'words', 0.667, 3.50, 7.30, 3.05, anchor='t',
             lines=[f'{word} — {meaning}' for word, meaning in KO['vocabulary']], sz=1500)
    add_from(ko1, templates['header'], 'success-header', 8.22, 2.95, 4.45, 0.55, text='SUCCESS CRITERIA', sz=1800, fill='F0EBE3')
    add_from(ko1, templates['box'], 'success', 8.22, 3.50, 4.45, 3.05, anchor='t',
             lines=[f'{i + 1}. {item}' for i, item in enumerate(KO['success'])], sz=1500, fill='F0EBE3')
    set_notes(ko1, [
        'Knowledge organiser — 0 minutes (reference). Return to this slide at any point in Lesson A; it matches '
        'pupil page 10 and the on-screen organiser. It is not an extra stage.',
        'Read the objective and the success criteria aloud when useful. Key words can be pointed to during the sort.',
        '', *SOURCES])
    ko2 = clone_slide(prs, slides[8])
    remove_shapes(ko2, ['help-header', 'hinder-header', 'help', 'hinder'])
    set_text(shape_by_name(ko2, 'title'), 'Friction knowledge organiser (2 of 2)')
    add_from(ko2, templates['header'], 'ideas-header', 0.667, 2.30, 7.30, 0.50, text='KEY IDEAS AND MODEL', sz=1800)
    add_from(ko2, templates['box'], 'ideas', 0.667, 2.80, 7.30, 2.65, anchor='t', lines=[*KO['facts'], 'Model: ' + KO['model']], sz=1400)
    add_from(ko2, templates['header'], 'examples-header', 8.22, 2.30, 4.45, 0.50, text='HELPFUL OR UNHELPFUL?', sz=1800, fill='F0EBE3')
    add_from(ko2, templates['box'], 'examples', 8.22, 2.80, 4.45, 2.65, anchor='t', lines=KO['examples'], sz=1400, fill='F0EBE3')
    add_from(ko2, templates['box'], 'comparison', 0.667, 5.55, 12.0, 0.85, text='Use evidence: ' + KO['comparison'], sz=1300)
    set_notes(ko2, [
        'Knowledge organiser — 0 minutes (reference). The sliding-box statement is an explanatory model, not a '
        'force measurement. Supplied results are model data; actual observations are recorded separately.',
        'Roughness alone does not predict every result: smooth rubber and smooth glass can still grip. A brief hand rub '
        'need not produce noticeable warmth.',
        '', *SOURCES])
    count = len(prs.slides)
    move_slide(prs, count - 2, 5); move_slide(prs, count - 1, 6)

    slides = list(prs.slides)
    # ---- We Do 2 sort slide: one optional help prompt line, no response field
    sort_slide = slides[12]
    assert shape_by_name(sort_slide, 'title').text_frame.text == 'Sort the claims'
    add_from(sort_slide, templates['access'], 'help-prompt', 0.667, 6.00, 12.0, 0.62,
             text=FB['prompt_title'] + ' ' + FB['prompt_a'], sz=1250)
    replace_notes(sort_slide, {
        'We Do 2 — sort — 4 minutes. This slide is within Monday’s existing 40-minute sequence, not extra teaching time.':
        'We Do 2 — sort — 3 minutes. This slide is within Lesson A’s existing 40-minute sequence, not extra '
        'teaching time. We Do 2 stays ten minutes: about eight for the sort, check and model, then two for the exit.',
        'Use pupil sheet2 or cut-out cards;': 'Use pupil page 2 or the page 6 cut-out cards;',
        'Make decisions before going to the answer slide.':
        'Make decisions before going to the answer slide. The help line is the lesson’s one optional prompt: a pupil '
        'may point, say, sign or show an idea, question or change; the adult listens, explains what can change and '
        'checks whether it helped. Invite a pupil to name one word or idea in a sorted claim that needs checking; hear, '
        'read or watch the response and adapt the explanation or scaffold. Passing is allowed; no extra record.',
    })
    replace_notes(slides[13], {
        'We Do 2 — check — 3 minutes. This slide is within Monday’s existing 40-minute sequence, not extra teaching time.':
        'We Do 2 — check — 2 minutes. This slide is within Lesson A’s existing 40-minute sequence, not extra teaching time.'})
    replace_notes(slides[14], {
        'We Do 2 — model explanation — 2 minutes. This slide is within Monday’s existing 40-minute sequence, not extra teaching time.':
        'We Do 2 — model explanation — 2 minutes. This slide is within Lesson A’s existing 40-minute sequence, not extra teaching time.'})

    # ---- Lesson A exit: two small checks per route, answers in notes only
    exit_slide = clone_slide(prs, slides[12])
    remove_shapes(exit_slide, ['line-', 'cue-', 'row-rule-', 'bins', 'help-prompt'])
    set_text(shape_by_name(exit_slide, 'title'), 'Finish Lesson A · two small checks')
    add_from(exit_slide, templates['strip'], 'routes', 0.667, 2.30, 12.0, 0.40,
             text='CHOOSE ONE ROUTE, ONCE     /     SUPPORTED   ·   STANDARD   ·   STRETCH     /     YOU MAY PASS')
    y = 2.80
    for route in routes:
        data = KO['routes'][route]
        for i, question in enumerate(data['questions']):
            text = question
            if data.get('options'):
                text += '  ' + ' / '.join(data['options'][i])
            add_from(exit_slide, templates['cue'], f'cue-{route}-{i}', 0.667, y + 0.06, 1.15, 0.36, text=f'{data["label"][:3].upper()} {i + 1}', sz=1200)
            add_from(exit_slide, templates['row'], f'line-{route}-{i}', 1.85, y, 10.6, 0.48, text=text, sz=1700)
            add_from(exit_slide, templates['rule'], f'rule-{route}-{i}', 1.85, y + 0.50, 10.55, 0.0)
            y += 0.53
    add_from(exit_slide, templates['access'], 'access', 0.667, 6.02, 12.0, 0.60,
             text='Point, say, sign, draw, type or use paper. An adult can scribe your words. Explanations are separate; '
                  'your response is not automatically marked. Next lesson: ' + KO['next_lesson'] + '.', sz=1300)
    set_notes(exit_slide, [
        'We Do 2 — exit — 2 minutes. This slide is within Lesson A’s existing 40-minute sequence, not extra teaching time.',
        KO['exit_intro'] + ' Pupil exit routes are pages 11 (Supported), 12 (Standard) and 13 (Stretch), two tickets per page.',
        KO['staff'],
        '[Staff explanations — do not display]',
        *[f'{KO["routes"][r]["label"]} {i + 1}. {answer}' for r in routes for i, answer in enumerate(KO['routes'][r]['answers'])],
        'Next lesson: ' + KO['next_lesson'] + '.',
        '', *SOURCES])
    move_slide(prs, len(prs.slides) - 1, 15)

    slides = list(prs.slides)
    keep = slides[16]
    assert shape_by_name(keep, 'title').text_frame.text == 'Keep your prediction for next time'
    set_text(shape_by_name(keep, 'line-1'), 'Next lesson: ' + KO['next_lesson'] + '.')
    replace_notes(keep, {
        'We Do 2 — stop and retain work — 1 minute. This slide is within Monday’s existing 40-minute sequence, not extra teaching time.':
        'We Do 2 — stop and retain work — 1 minute. This slide is within Lesson A’s existing 40-minute sequence, not extra teaching time.',
        'End Monday here, exactly as the source period break requires.': 'End Lesson A here after the two-check exit.',
        'Do not add Tuesday’s workshop, feedback or exit ticket to today. Tuesday source: 32-minute investigation/workshop, 4-minute pupil feedback, 4-minute exit ticket. A separate Lesson B deck will retain that pacing and the source three-surface repeated-trial task.':
        'Do not add Lesson B’s workshop, evidence review or exit ticket to this lesson. Lesson B, Friction: test the '
        'surfaces, keeps its own deck and pacing: 32-minute investigation workshop, 4-minute evidence review, 4-minute exit ticket.',
    })
    # remaining day wording in retained notes
    for slide in slides:
        text = notes_text(slide)
        if 'Monday' in text or 'Tuesday' in text:
            replace_notes(slide, {k: v for k, v in {
                'within Monday’s existing 40-minute sequence': 'within Lesson A’s existing 40-minute sequence',
                'Tuesday': 'Lesson B', 'Monday': 'Lesson A'}.items() if k in text})
    replace_notes(slides[0], {'Source read 6 September 2026.': 'Source read 6 September 2026; revision 15 September 2026 '
                              '(four-question arrivals on slides 2–4, organiser on slides 6–7, two-check exit on '
                              'slide 16, optional help prompt on slide 13; pupil pages: common 1–2, response 3–5, '
                              'cards 6, arrival 7–9, organiser 10, exit 11–13).'})
    renumber_pages(prs)
    check_no_day_words(prs)
    assert len(prs.slides) == 17
    return prs


# ----------------------------------------------------------------------------- W3B
def build_b(root):
    prs = baseline(root, B_DECK)
    slides = list(prs.slides)
    row, cue, rule = shape_by_name(slides[8], 'line-0'), shape_by_name(slides[8], 'cue-0'), shape_by_name(slides[8], 'row-rule-0')
    strip = shape_by_name(slides[7], 'left-heading')
    # slide 2 retrieval wording names the lesson, not a day
    set_text(shape_by_name(slides[1], 'line-0'), 'Find your Lesson A prediction. Do not erase it.')
    replace_notes(slides[0], {
        'Tuesday begins with the source’s 32-minute Independent Work workshop. Retain Monday’s prediction; use slide 2 immediately.':
        'Lesson B begins with the source’s 32-minute Independent Work workshop. Retain the Lesson A prediction; use slide 2 immediately. '
        'Lesson B stays 32 + 4 + 4 minutes: workshop, Review the evidence, Exit Ticket.'})
    # slide 13: Lundy Loop stage becomes Review the evidence
    review = slides[12]
    assert shape_by_name(review, 'title').text_frame.text == 'Your voice can change the lesson'
    remove_shapes(review, ['line-', 'cue-', 'row-rule-'])
    set_text(shape_by_name(review, 'title'), FB['review_title'])
    add_from(review, strip, 'intro', 0.667, 2.30, 12.0, 0.62, text=FB['review_intro'], sz=1500)
    y = 3.05
    for i, step in enumerate(FB['review_steps']):
        add_from(review, cue, f'cue-{i}', 0.667, y + 0.20, 0.35, 0.35, text=f'{i + 1:02d}')
        add_from(review, row, f'line-{i}', 1.09, y, 11.35, 0.80, text=step, sz=1700)
        add_from(review, rule, f'row-rule-{i}', 1.09, y + 0.83, 11.30, 0.0)
        y += 0.90
    add_from(review, strip, 'close', 0.667, 5.78, 12.0, 0.40, text=FB['review_close'], sz=1300)
    add_from(review, strip, 'help-prompt', 0.667, 6.20, 12.0, 0.45,
             text=FB['prompt_title'] + ' ' + FB['prompt_b'], sz=1150)
    staff = {title: text for title, text in FB['staff_sections']}
    set_notes(review, [
        'Review the evidence — 4 minutes within the source’s 40-minute lesson. Exact four-minute stage between '
        'the 32-minute workshop and the 4-minute exit; no separate feedback form or standalone participation stage.',
        'Revisit one conclusion against the existing results or clearly labelled model data. Hear, read or watch the '
        'pupil response; adapt the explanation or scaffold and explain any limit. Preserve original values and label '
        'retries. Passing is allowed. No automatic R.',
        'Lesson B: review the evidence — ' + staff['Lesson B: review the evidence'],
        'Listen and act — ' + staff['Listen and act'],
        'Use marking codes honestly — ' + staff['Use marking codes honestly'],
        'Policy and timing — ' + staff['Policy and timing'],
        '', *B_SOURCES])
    replace_notes(slides[14], {'Clarify that friction opposes relative sliding or attempted sliding at a contact; static grip can help a person walk forwards.':
                               'Clarify that friction opposes relative sliding or attempted sliding at a contact; static grip can help a person walk forwards. '
                               'Next lesson: Levers, pulleys and gears.'})
    for slide in slides:
        text = notes_text(slide)
        if 'Monday' in text or 'Tuesday' in text:
            replace_notes(slide, {k: v for k, v in {'Tuesday': 'Lesson B', 'Monday’s': 'Lesson A’s', 'Monday': 'Lesson A'}.items() if k in text})
    renumber_pages(prs)
    check_no_day_words(prs)
    assert len(prs.slides) == 15
    return prs


def save(prs, path):
    buf = io.BytesIO(); prs.save(buf); path.write_bytes(buf.getvalue())


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--root', type=Path, default=HERE.parents[1])
    args = ap.parse_args()
    root = args.root.resolve()
    save(build_a(root), root / A_DECK)
    save(build_b(root), root / B_DECK)
    print('written', A_DECK, B_DECK)
