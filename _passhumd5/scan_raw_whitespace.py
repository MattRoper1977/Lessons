#!/usr/bin/env python3
"""HUM-D5 A1 - whitespace/punctuation scan against the RAW files.

Defect D5: the text index normalises \\s+ to a single space, so a double-space
check run against the index can never fire. It is run here against the source
bytes instead, on the surfaces where a double space is a defect rather than
formatting: rendered text nodes in HTML, DOCX/PPTX runs, and plain text.
HTML source indentation is NOT a defect and is excluded.
"""
import re, json, zipfile, collections
from pathlib import Path
from lxml import html as LH

ROOT = Path('/tmp/claude-0/humd5/unzipped')
W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
A = '{http://schemas.openxmlformats.org/drawingml/2006/main}'
groups = collections.defaultdict(lambda: {'occurrences': [], 'samples': []})

def flag(kind, cur, lesson, surface, locator, sample):
    g = groups[(kind, cur)]
    g['kind'], g['current'] = kind, cur
    g['occurrences'].append({'lesson_id': lesson, 'surface': surface, 'locator': locator})
    if len(g['samples']) < 3: g['samples'].append(sample)

def check(text, lesson, surface, locator):
    if not text: return
    for m in re.finditer(r'\S  +\S', text):
        flag('double-space', re.sub(r' +', '␣␣', m.group(0)), lesson, surface, locator, m.group(0))
    for m in re.finditer(r'\s+[,.;:!?]', text):
        flag('space-before-punctuation', m.group(0).strip() or m.group(0), lesson, surface, locator,
             text[max(0, m.start()-30):m.end()+30])
    for m in re.finditer(r'[,.;:!?](?=[A-Za-z])', text):
        seg = text[max(0, m.start()-18):m.end()+18]
        if re.search(r'\d[.,]\d|\b[A-Z]\.[A-Z]|www\.|https?:|\.\w{2,4}\b', seg): continue
        flag('missing-space-after-punctuation', seg.strip(), lesson, surface, locator, seg)

def zip_runs(path, tag):
    try: z = zipfile.ZipFile(path)
    except Exception: return
    for name in z.namelist():
        if not name.endswith('.xml'): continue
        try: root = LH.fromstring(z.read(name))
        except Exception: continue
        for t in root.iter(tag):
            if t.text: yield name, t.text

for lp in sorted(ROOT.glob('*/**/*_Lesson.html')):
    lesson = lp.name[:-len('_Lesson.html')]
    for sib in sorted(lp.parent.iterdir()):
        if not sib.is_file() or not sib.name.startswith(lesson): continue
        surface = sib.name[len(lesson)+1:]
        sfx = sib.suffix.lower()
        if sfx == '.html':
            try: doc = LH.parse(str(sib)).getroot()
            except Exception: continue
            for bad in doc.xpath('//script|//style'):
                bad.getparent().remove(bad)
            tree = doc.getroottree()
            for el in doc.iter():
                if el.text and el.text.strip(): check(el.text, lesson, surface, tree.getpath(el))
        elif sfx == '.txt':
            check(sib.read_text(encoding='utf-8', errors='replace'), lesson, surface, 'file')
        elif sfx == '.docx':
            for n, t in zip_runs(sib, W+'t'): check(t, lesson, surface, n)
        elif sfx == '.pptx':
            for n, t in zip_runs(sib, A+'t'): check(t, lesson, surface, n)

items = sorted(groups.values(), key=lambda g: -len(g['occurrences']))
for i, g in enumerate(items, 1): g['id'] = f'W{i:04d}'
Path('/tmp/claude-0/humd5/CLASS_A_WHITESPACE.jsonl').write_text(
    '\n'.join(json.dumps(g, ensure_ascii=False) for g in items) + ('\n' if items else ''), encoding='utf-8')
occ = collections.Counter(); grp = collections.Counter()
for g in items: occ[g['kind']] += len(g['occurrences']); grp[g['kind']] += 1
print(f'distinct groups: {len(items)}   occurrences: {sum(occ.values())}')
for k, n in grp.most_common(): print(f'  {k:34} {n:5} groups  {occ[k]:6} occ')
print('\ntop 6 by occurrence:')
for g in items[:6]:
    print(f"  {len(g['occurrences']):5}x [{g['kind']}] {g['current']!r}")
    print(f"        e.g. …{g['samples'][0][:80]}…")
