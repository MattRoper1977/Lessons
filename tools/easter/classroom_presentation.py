"""Apply the user-selected Art Studio appearance without replacing teaching/runtime."""
from pathlib import Path
from lxml import html as lh

CSS = Path(__file__).with_name('classroom_chassis.css')
PHASES = ('title', 'arrival', 'starter', 'ido', 'wedo', 'ido', 'wedo', 'independent', 'exit')
LABELS = {'title':'Lesson', 'arrival':'Retrieval', 'starter':'Starter', 'ido':'I Do',
          'wedo':'We Do', 'independent':'Independent work', 'exit':'Exit ticket'}


def apply(tree, family, title):
    """Keep data, timings, diagrams, scripts, evidence and print pages intact."""
    lane = family.split()[0].lower()
    if lane not in ('build', 'grow', 'launch'):
        raise ValueError('A known pathway is required for the classroom presentation')
    classes = (tree.get('class') or '').split()
    classes = [c for c in classes if c not in ('pathway-build','pathway-grow','pathway-launch')]
    tree.set('class', ' '.join(dict.fromkeys(classes + ['mbm-classroom', 'pathway-'+lane])))
    for old in tree.xpath('//style[@id="mbm-classroom-chassis"]'):
        old.getparent().remove(old)
    style = lh.Element('style', id='mbm-classroom-chassis')
    style.text = CSS.read_text(encoding='utf-8')
    tree.xpath('//head')[0].append(style)
    stages = tree.xpath('//main[contains(concat(" ",normalize-space(@class)," ")," deck ")]/section[contains(concat(" ",normalize-space(@class)," ")," slide ")]')
    for index, stage in enumerate(stages):
        phase = PHASES[index] if len(stages) == 9 else stage.get('data-type','')
        stage.set('data-classroom-phase', phase)
        for tag in stage.xpath('./span[contains(concat(" ",normalize-space(@class)," ")," tag ")]'):
            if not tag.text_content().strip():
                tag.text = family if phase == 'title' else LABELS.get(phase, stage.get('data-title','Lesson'))
        if index == 0:
            heads = stage.xpath('./h1')
            heading = heads[0] if heads else lh.Element('h1')
            if not heads:
                anchor = next((n for n in stage if n.tag not in ('div','span') or 'lundy' in (n.get('class') or '')), None)
                if anchor is not None: anchor.addprevious(heading)
                else: stage.insert(0, heading)
            heading.text = title
            for child in list(heading): heading.remove(child)
            for para in stage.xpath('./p'):
                text = para.text_content().strip()
                if text.startswith('Objective:'): para.set('class','mbm-lesson-objective')
                if text.startswith(('Success evidence:', 'Success looks like:')): para.set('class','mbm-lesson-success')
        # Empty labels were retained as furniture but erased by donor-text sweeping.
        for grid in stage.xpath('.//*[contains(concat(" ",normalize-space(@class)," ")," lundy-grid ")]'):
            spans = grid.xpath('./span')
            if len(spans) == 4:
                for node, label in zip(spans, ('SPACE','VOICE','AUDIENCE','INFLUENCE')):
                    if not node.text_content().strip(): node.text = label
        # Put the participation reminder after the teaching, not ahead of its title.
        for strip in stage.xpath('./div[contains(concat(" ",normalize-space(@class)," ")," lundy ")]'):
            stage.remove(strip); stage.append(strip)
