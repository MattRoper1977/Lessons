#!/usr/bin/env python3
"""HUM-D5 A2 - apply the Class A replacement map to every surface where a string occurs.

    apply_proof.py --root <unzipped packs> --map _passhumd5/replacements.json [--write] [--only A0001,A0003]

Exact-match, per-file, idempotent, refusing on zero or unexpected match counts:
  * every group in the map is expanded to (file, current, proposed) edits, one per
    ledger occurrence; occurrences of the same string in the same file are merged and
    their count is the EXPECTED count for that file;
  * HTML (Lesson.html, Pupil_Resources.html, Knowledge_Organiser.html, ...): the whole
    file is edited, so the body and the config JSON stay in step; the count found in
    the file is recorded against the ledger rows (config, body and rendered rows all
    describe the SAME file, so they are not a file count); zero hits refuses, every hit is
    replaced so body and config JSON stay in step; JSON safety: a proposed string may not introduce
    a double quote or a backslash;
  * DOCX / PPTX: runs are edited in place (python-docx / python-pptx), formatting kept;
    a string that spans two runs is refused (never split-merged); notes slides included;
  * PDFs are never edited: touched lessons are listed for re-rendering by the caller;
  * computed kinds (missing-space-after-punctuation, doubled-full-stop,
    space-before-punctuation) carry a context snippet as `current` and derive the exact
    edit by rule inside that snippet; the snippet itself is the exact-match key.
  * idempotent: a second --write finds 0 matches for a done edit and reports it as
    ALREADY_APPLIED (the proposed string is present the expected number of times) -
    never as a refusal.
Without --write nothing is changed; the plan and its counts are printed and written to
APPLY_PLAN.json beside the map."""
import argparse, json, os, re, sys, collections, copy
from docx import Document
from pptx import Presentation
SURFACE_FILE={'config':'{id}_Lesson.html','Lesson.html':'{id}_Lesson.html','rendered:stage':'{id}_Lesson.html','rendered:details':'{id}_Lesson.html','rendered:print':'{id}_Lesson.html','rendered:modal':'{id}_Lesson.html','rendered:route':'{id}_Lesson.html','rendered:block':'{id}_Lesson.html',
 'Humanities_Scheme_of_Work_2026-27.docx':'Humanities_Scheme_of_Work_2026-27.docx','Humanities_Scheme_of_Work_2026-27.html':'Humanities_Scheme_of_Work_2026-27.html','RE_Scheme_of_Work_Autumn_2026.docx':'RE_Scheme_of_Work_Autumn_2026.docx','RE_Scheme_of_Work_Autumn_2026.html':'RE_Scheme_of_Work_Autumn_2026.html','Editable_Pack.docx':'{id}_Editable_Pack.docx','Editable_Slides.pptx':'{id}_Editable_Slides.pptx',
 'Editable_Slides.pptx:notes':'{id}_Editable_Slides.pptx','Pupil_Resources.html':'{id}_Pupil_Resources.html','Knowledge_Organiser.html':'{id}_Knowledge_Organiser.html',
 'Teacher_Notes.docx':'{id}_Teacher_Notes.docx','Model_Transcript.txt':'{id}_Model_Transcript.txt','Data.csv':'{id}_Data.csv','Sources_and_checks.html':'Sources_and_checks.html',
 'START_HERE.html':'START_HERE.html','Review_record.html':'Review_record.html'}
PDF_SURFACES={'Pupil_Resources.pdf','Knowledge_Organiser.pdf','Teacher_Notes.pdf'}
def derive(kind,current,proposed):
    """Exact (current, proposed) for computed kinds; for explicit kinds return as given."""
    if proposed: return current,proposed
    if kind=='missing-space-after-punctuation':
        p=re.sub(r'([,;:])(?=[A-Za-z])',r'\1 ',current); return current,p
    if kind=='doubled-full-stop':
        p=re.sub(r'\.\.(?!\.)','.',current); return current,p
    if kind=='space-before-punctuation':
        p=re.sub(r'\s+([.,;:!?])',r'\1',current); return current,p
    raise SystemExit(f'no rule for computed kind {kind!r}')
def lesson_dirs(root):
    m={}
    for dp,_,fs in os.walk(root):
        for fn in fs:
            if fn.endswith('_Lesson.html'): m[fn[:-len('_Lesson.html')]]=dp
    return m
def docx_runs(path,kind):
    if kind=='docx':
        d=Document(path); runs=[r for p in d.paragraphs for r in p.runs]
        for t in d.tables:
            for row in t.rows:
                for c in row.cells:
                    for p in c.paragraphs: runs.extend(p.runs)
        return d,runs
    pr=Presentation(path); runs=[]
    for s in pr.slides:
        shapes=list(s.shapes)
        for sh in shapes:
            if sh.has_text_frame:
                for p in sh.text_frame.paragraphs: runs.extend(p.runs)
            if getattr(sh,'has_table',False) and sh.has_table:
                for row in sh.table.rows:
                    for c in row.cells:
                        for p in c.text_frame.paragraphs: runs.extend(p.runs)
        if s.has_notes_slide:
            for p in s.notes_slide.notes_text_frame.paragraphs: runs.extend(p.runs)
    return pr,runs
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--root',required=True); ap.add_argument('--map',required=True); ap.add_argument('--write',action='store_true'); ap.add_argument('--only',default='')
    a=ap.parse_args(); groups=json.load(open(a.map,encoding='utf-8')); only=set(x for x in a.only.split(',') if x)
    dirs=lesson_dirs(a.root)
    # expand to per-file edits
    edits=collections.defaultdict(lambda: collections.Counter())   # (path, kind, current, proposed) -> expected count
    skipped=[]
    for g in groups:
        if only and g['id'] not in only: continue
        for o in g['occurrences']:
            surf=o['surface']
            if surf in PDF_SURFACES: skipped.append((g['id'],o['lesson_id'],surf,'pdf: re-render, not edited')); continue
            if surf not in SURFACE_FILE: skipped.append((g['id'],o['lesson_id'],surf,'surface not mapped')); continue
            lid=o['lesson_id']
            if lid.startswith('PACK::'):
                pack=lid.split('::',1)[1]; cand=[os.path.join(dp,fn) for dp,_,fs in os.walk(a.root) for fn in fs if fn==surf and pack in dp]
                if not cand: skipped.append((g['id'],lid,surf,'pack file not found')); continue
                path=cand[0]
            else:
                if lid not in dirs: skipped.append((g['id'],lid,surf,'lesson dir not found')); continue
                path=os.path.join(dirs[lid],SURFACE_FILE[surf].format(id=lid))
                if surf in ('Sources_and_checks.html','START_HERE.html','Review_record.html') or surf.startswith(('Humanities_Scheme','RE_Scheme')):
                    # pack-level files sit above the lesson dir
                    d=dirs[lid]; found=None
                    while d and d!=a.root:
                        if os.path.exists(os.path.join(d,surf)): found=os.path.join(d,surf); break
                        d=os.path.dirname(d)
                    if not found: skipped.append((g['id'],lid,surf,'pack file not found')); continue
                    path=found
            cur,pro=derive(g['kind'],o.get('current') or g['current'],o.get('proposed') or g.get('proposed'))
            if g.get('per_occurrence_strings') and not (o.get('current') and o.get('proposed')): skipped.append((g['id'],lid,surf,'per-occurrence strings missing')); continue
            if cur==pro: skipped.append((g['id'],lid,surf,'no-op (current == proposed)')); continue
            if (surf=='config' or path.endswith('.html')) and not g.get('raw'):
                # `raw` groups edit markup or JSON STRUCTURE (an svg opener, a new config key), not
                # text inside a JSON string; they are validated after the write instead (below).
                if '"' in pro or '\\' in pro: raise SystemExit(f'{g["id"]}: proposed string is not JSON-safe: {pro!r}')
            edits[(path,g['kind'],cur,pro)][g['id']]+=1
    plan=[]; refusals=[]; touched=set()
    byfile=collections.defaultdict(list)
    for (path,kind,cur,pro),ids in edits.items(): byfile[path].append((kind,cur,pro,sum(ids.values()),sorted(ids)))
    for path,items in sorted(byfile.items()):
        if not os.path.exists(path): refusals.append((path,'missing file')); continue
        ext=os.path.splitext(path)[1].lower()
        if ext in ('.html','.txt','.csv'):
            text=open(path,encoding='utf-8').read(); new=text; results=[]
            for kind,cur,pro,expected,ids in items:
                n=new.count(cur); done=new.count(pro)
                if n==0:
                    if done>=1: results.append({'ids':ids,'current':cur[:60],'status':'ALREADY_APPLIED','found':0,'expected':expected}); continue
                    refusals.append((path,f'{ids}: zero matches for {cur!r}')); results.append({'ids':ids,'current':cur[:60],'status':'REFUSED_ZERO','found':0,'expected':expected}); continue
                if cur in pro and done>=1 and n<=done: results.append({'ids':ids,'current':cur[:60],'status':'ALREADY_APPLIED','found':0,'expected':expected}); continue
                new=new.replace(cur,pro); results.append({'ids':ids,'current':cur[:60],'proposed':pro[:60],'status':'PLANNED','found':n,'ledger_rows':expected,'note':'every hit in the file replaced: body and config JSON stay in step'})
            if any(r['status']=='PLANNED' for r in results):
                touched.add(path)
                if path.endswith('_Lesson.html'):
                    # a raw edit may not break the config: prove window.CLASSIC_LESSON still parses
                    i=new.find('window.CLASSIC_LESSON'); j=new.find('=',i)+1
                    try: json.JSONDecoder().raw_decode(new[j:].lstrip())
                    except Exception as e: raise SystemExit(f'{path}: window.CLASSIC_LESSON would not parse after the edit: {e}')
                if a.write: open(path,'w',encoding='utf-8').write(new)
            plan.append({'file':os.path.relpath(path,a.root),'edits':results})
        elif ext in ('.docx','.pptx'):
            doc,runs=docx_runs(path,'docx' if ext=='.docx' else 'pptx'); results=[]; changed=False
            for kind,cur,pro,expected,ids in items:
                # whitespace-tolerant on the RAW run: the index collapses \s+, and a DOCX heading
                # keeps two spaces where its punctuation was stripped ("Christianity  key beliefs")
                rx=re.compile(r'\s+'.join(re.escape(t) for t in cur.split()))
                # a run that already holds the PROPOSED text is done: never match `current` inside it
                # (when `current` is a prefix of `proposed`, e.g. "Book or place" -> "Book or place?",
                # a second pass would otherwise append again - measured, repaired, and closed here)
                # "done" means the run holds the proposed text and NOT the current one: when the
                # proposed string is a prefix of the current one (H2: "Previous lesson reminder: X"
                # -> "Previous lesson reminder:"), every unedited run also contains it (measured:
                # 180 DOCX/PPTX edits were skipped as already applied on the first A0028 write)
                # Two prefix cases, both measured on this map:
                #   A  current is a prefix of proposed ("Book or place" -> "Book or place?"): a run that
                #      already holds the proposed text is done, and `current` still matches inside it;
                #   B  proposed is a prefix of current ("Previous lesson reminder: X" -> "Previous lesson
                #      reminder:"): every unedited run also holds the proposed text, so holding it is
                #      not "done" - only a run without `current` is.
                done_runs=[r for r in runs if pro in r.text and not rx.search(r.text)] if not (cur in pro) else [r for r in runs if pro in r.text]
                hits=[r for r in runs if rx.search(r.text) and not (cur in pro and pro in r.text)]; n=sum(len(rx.findall(r.text)) for r in hits)
                # a string split across runs: count in paragraph text but not in any run
                if n==0:
                    para_n=sum(1 for p in (getattr(doc,'paragraphs',[]) ) if cur in p.text) if ext=='.docx' else 0
                    done=sum(r.text.count(pro) for r in done_runs)
                    if done>=1: results.append({'ids':ids,'current':cur[:60],'status':'ALREADY_APPLIED','found':0,'expected':expected}); continue
                    refusals.append((path,f'{ids}: zero run matches for {cur!r}'+(' (spans runs)' if para_n else ''))); results.append({'ids':ids,'current':cur[:60],'status':'REFUSED_ZERO'+('_SPANS_RUNS' if para_n else ''),'found':0,'expected':expected}); continue
                if n<expected: refusals.append((path,f'{ids}: found {n} < expected {expected} for {cur!r}')); results.append({'ids':ids,'current':cur[:60],'status':'REFUSED_COUNT','found':n,'expected':expected}); continue
                for r in hits: r.text=rx.sub(lambda m: pro, r.text)
                changed=True; results.append({'ids':ids,'current':cur[:60],'proposed':pro[:60],'status':'PLANNED','found':n,'expected':expected})
            if changed:
                touched.add(path)
                if a.write: doc.save(path)
            plan.append({'file':os.path.relpath(path,a.root),'edits':results})
        else: refusals.append((path,'unsupported extension'))
    out={'root':a.root,'map':a.map,'write':a.write,'files':len(plan),'planned_edits':sum(1 for p in plan for e in p['edits'] if e['status']=='PLANNED'),'already_applied':sum(1 for p in plan for e in p['edits'] if e['status']=='ALREADY_APPLIED'),'refusals':refusals,'skipped':skipped,'touched_files':sorted(os.path.relpath(t,a.root) for t in touched),'plan':plan}
    json.dump(out,open(os.path.join(os.path.dirname(a.map),'APPLY_PLAN.json'),'w'),indent=1,ensure_ascii=False)
    print(f"{'WRITE' if a.write else 'DRY RUN'}: files {out['files']}  planned edits {out['planned_edits']}  already applied {out['already_applied']}  refusals {len(refusals)}  skipped {len(skipped)}")
    sk=collections.Counter(s[3] for s in skipped); print('  skipped by reason:',dict(sk))
    for r in refusals[:15]: print('  REFUSED',r)
    lessons=sorted(set(os.path.basename(t).split('_Lesson')[0].split('_Editable')[0].split('_Pupil')[0].split('_Knowledge')[0].split('_Teacher')[0].split('_Model')[0] for t in touched))
    print('  touched files',len(touched),'lessons',len(lessons))
    if refusals and a.write: sys.exit(2)
if __name__=='__main__': main()
