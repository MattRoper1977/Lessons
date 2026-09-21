#!/usr/bin/env python3
"""HUM-D5 A0 - build TEXT_INDEX.jsonl: one row per text unit.

Row: {lesson_id, pack, surface, locator, text}
Static surfaces only; the rendered-DOM pass is render_text_index.py.
Every unreadable file is recorded as a NOT_RUN row with its reason -- never
silently skipped, never counted as a pass.
"""
import json, re, sys, csv, io, zipfile
from pathlib import Path

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else '/tmp/claude-0/humd5/unzipped')
OUT  = Path(sys.argv[2] if len(sys.argv) > 2 else '/tmp/claude-0/humd5/TEXT_INDEX.jsonl')

rows, notrun, seen = [], [], set()

def add(lesson_id, pack, surface, locator, text):
    if text is None: return
    t = re.sub(r'\s+', ' ', str(text)).strip()
    if t:
        rows.append({'lesson_id': lesson_id, 'pack': pack, 'surface': surface,
                     'locator': locator, 'text': t})

def skip(lesson_id, pack, surface, path, reason):
    notrun.append({'lesson_id': lesson_id, 'pack': pack, 'surface': surface,
                   'path': str(path), 'reason': reason})

def config_of(html_path):
    s = html_path.read_text(encoding='utf-8', errors='replace')
    # The key is matched with optional whitespace around '='. A literal
    # 'window.CLASSIC_LESSON=' missed every lesson that writes the spaced form --
    # measured on the twelve Summer 1 lessons of ADDENDUM 2, all of which write
    # 'window.CLASSIC_LESSON = ': 6 of 6 BUILD lessons produced 0 config rows and
    # 6 'not found or not parseable' skips. An index that cannot see a lesson makes
    # every check that reads it report on nothing and look clean doing it.
    m = re.search(r'window\.CLASSIC_LESSON\s*=\s*', s)
    if not m: return None, s
    i = m.end()
    d = 0; j = i; instr = False; esc = False
    while j < len(s):
        c = s[j]
        if instr:
            if esc: esc = False
            elif c == '\\': esc = True
            elif c == '"': instr = False
        else:
            if c == '"': instr = True
            elif c == '{': d += 1
            elif c == '}':
                d -= 1
                if d == 0: j += 1; break
        j += 1
    try: return json.loads(s[i:j]), s
    except Exception: return None, s

def walk(o, p=''):
    if isinstance(o, dict):
        for k, v in o.items(): yield from walk(v, f'{p}.{k}')
    elif isinstance(o, list):
        for k, v in enumerate(o): yield from walk(v, f'{p}[{k}]')
    else: yield p, o

def html_text(path, lesson_id, pack, surface):
    try:
        from lxml import html as LH
        doc = LH.parse(str(path)).getroot()
    except Exception as e:
        return skip(lesson_id, pack, surface, path, f'unreadable HTML: {e.__class__.__name__}')
    for bad in doc.xpath('//script|//style'):
        bad.getparent().remove(bad)
    for el in doc.iter():
        if el.text and el.text.strip():
            add(lesson_id, pack, surface, doc.getroottree().getpath(el), el.text)
        if el.tail and el.tail.strip():
            add(lesson_id, pack, surface, doc.getroottree().getpath(el) + '/tail', el.tail)

def docx_text(path, lesson_id, pack, surface):
    try:
        import docx
        d = docx.Document(str(path))
    except Exception as e:
        return skip(lesson_id, pack, surface, path, f'unreadable DOCX: {e.__class__.__name__}: {e}')
    for i, p in enumerate(d.paragraphs):
        add(lesson_id, pack, surface, f'para[{i}]', p.text)
    for ti, t in enumerate(d.tables):
        for ri, r in enumerate(t.rows):
            for ci, c in enumerate(r.cells):
                add(lesson_id, pack, surface, f'table[{ti}]/r{ri}/c{ci}', c.text)

def pptx_text(path, lesson_id, pack, surface):
    try:
        from pptx import Presentation
        pr = Presentation(str(path))
    except Exception as e:
        return skip(lesson_id, pack, surface, path, f'unreadable PPTX: {e.__class__.__name__}: {e}')
    for si, slide in enumerate(pr.slides, 1):
        for shi, sh in enumerate(slide.shapes):
            if sh.has_text_frame:
                for pi, para in enumerate(sh.text_frame.paragraphs):
                    add(lesson_id, pack, surface, f'slide{si}/shape{shi}/p{pi}',
                        ''.join(r.text for r in para.runs))
        if slide.has_notes_slide and slide.notes_slide.notes_text_frame is not None:
            add(lesson_id, pack, f'{surface}:notes', f'slide{si}',
                slide.notes_slide.notes_text_frame.text)

def pdf_text(path, lesson_id, pack, surface):
    try:
        import pymupdf
        doc = pymupdf.open(str(path))
    except Exception as e:
        return skip(lesson_id, pack, surface, path, f'unreadable PDF: {e.__class__.__name__}: {e}')
    for pi, page in enumerate(doc, 1):
        for bi, b in enumerate(page.get_text('blocks')):
            add(lesson_id, pack, surface, f'page{pi}/block{bi}', b[4])
    doc.close()

def xlsx_text(path, lesson_id, pack, surface):
    try:
        import openpyxl
        wb = openpyxl.load_workbook(str(path), data_only=True)
    except Exception as e:
        return skip(lesson_id, pack, surface, path, f'unreadable XLSX: {e.__class__.__name__}: {e}')
    for ws in wb.worksheets:
        for ri, row in enumerate(ws.iter_rows(values_only=True), 1):
            for ci, v in enumerate(row):
                if isinstance(v, str): add(lesson_id, pack, surface, f'{ws.title}!r{ri}c{ci}', v)

def csv_text(path, lesson_id, pack, surface):
    try: txt = path.read_text(encoding='utf-8', errors='replace')
    except Exception as e:
        return skip(lesson_id, pack, surface, path, f'unreadable CSV: {e}')
    for ri, row in enumerate(csv.reader(io.StringIO(txt))):
        for ci, v in enumerate(row):
            if v.strip(): add(lesson_id, pack, surface, f'r{ri}c{ci}', v)

EXT = {'.docx': docx_text, '.pptx': pptx_text, '.pdf': pdf_text,
       '.xlsx': xlsx_text, '.csv': csv_text}

lessons = sorted(ROOT.glob('*/**/*_Lesson.html'))
for lp in lessons:
    lesson_id = lp.name[:-len('_Lesson.html')]
    pack = lp.relative_to(ROOT).parts[0]
    cfg, raw = config_of(lp)
    if cfg is None:
        skip(lesson_id, pack, 'config', lp, 'window.CLASSIC_LESSON not found or not parseable')
    else:
        for p, v in walk(cfg):
            if isinstance(v, str) and v.strip():
                add(lesson_id, pack, 'config', p.lstrip('.'), v)
    for sib in sorted(lp.parent.iterdir()):
        if not sib.is_file() or sib.name == lp.name: continue
        stem = sib.name
        if not (stem.startswith(lesson_id) or stem in
                ('Sources_and_checks.html', 'START_HERE.html', 'Review_record.html')):
            continue
        sfx = sib.suffix.lower()
        surface = stem[len(lesson_id) + 1:] if stem.startswith(lesson_id + '_') else stem
        if sib in seen: continue
        seen.add(sib)
        if sfx == '.html': html_text(sib, lesson_id, pack, surface)
        elif sfx == '.txt': add(lesson_id, pack, surface, 'file', sib.read_text(encoding='utf-8', errors='replace'))
        elif sfx in EXT: EXT[sfx](sib, lesson_id, pack, surface)

# pack-level and SoW surfaces
for pack_dir in sorted(ROOT.iterdir()):
    if not pack_dir.is_dir(): continue
    for f in sorted(pack_dir.rglob('*')):
        if not f.is_file(): continue
        n = f.name
        if f in seen: continue
        if n in ('START_HERE.html', 'Review_record.html', 'Sources_and_checks.html') \
           or 'Scheme_of_Work' in n:
            seen.add(f)
            sfx = f.suffix.lower()
            sid = f'PACK::{pack_dir.name}'
            if sfx == '.html': html_text(f, sid, pack_dir.name, n)
            elif sfx == '.docx': docx_text(f, sid, pack_dir.name, n)

OUT.parent.mkdir(parents=True, exist_ok=True)
with OUT.open('w', encoding='utf-8') as fh:
    for r in rows: fh.write(json.dumps(r, ensure_ascii=False) + '\n')
Path(str(OUT).replace('.jsonl', '_NOT_RUN.jsonl')).write_text(
    '\n'.join(json.dumps(r, ensure_ascii=False) for r in notrun) + ('\n' if notrun else ''), encoding='utf-8')

import collections
print(f'lessons indexed : {len(lessons)}')
print(f'text rows       : {len(rows)}')
print(f'NOT RUN entries : {len(notrun)}')
print('\nrows per surface:')
for s, n in collections.Counter(r['surface'] for r in rows).most_common(40):
    print(f'  {n:7}  {s}')
if notrun:
    print('\nNOT RUN reasons:')
    for s, n in collections.Counter(r['reason'].split(':')[0] for r in notrun).most_common():
        print(f'  {n:5}  {s}')
