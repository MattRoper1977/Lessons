#!/usr/bin/env python3
"""Build a route-preserving Science front page from reviewed source metadata."""
import html
import json
import posixpath
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[2]
TERMS = {'Aut1':'Autumn 1','Aut2':'Autumn 2','Spr1':'Spring 1','Spr2':'Spring 2'}
PATHWAYS = {'BUILD':'Core ideas, pictures and practical exploration.',
            'GROW':'Develop explanations through models and fair tests.',
            'LAUNCH':'Apply scientific ideas, analyse evidence and evaluate methods.'}

def esc(value):
    return html.escape(str(value), quote=True)

def link(path):
    return quote(posixpath.relpath(path, 'Science_Teesside'), safe='/')

def lesson(row):
    preferred = row['choice'] == 'main'
    week = ', '.join(row['termWeeks']).replace('Aut1·','').replace('Aut2·','').replace('Spr1·','').replace('Spr2·','')
    role = row['cadence'].get('lessonRole') or 'Lesson'
    if row['version'] == 'original':
        role = 'Two-session deck' if row['pathway'] != 'LAUNCH' else 'Single-session lesson'
    elif row['version'] == 'v3_40min':
        role = 'Expanded 40-minute version'
    else:
        role = {'one period in an explicit multi-lesson sequence':'Linked lesson'}.get(role,role)
    searchable = ' '.join([row['title'],week,role,row['pathway'],row['termLabel']]).casefold()
    return f'''<li class="lesson-row" data-choice="{esc(row['choice'])}" data-search="{esc(searchable)}">
<div><div class="meta"><span class="badge{'' if preferred else ' alt'}">{'Main version' if preferred else 'Alternative'}</span><span>{esc(week)}</span><span>{esc(role)}</span></div>
<h3>{esc(row['title'])}</h3>{'<p>Supported, Standard and Stretch print options inside.</p>' if row.get('printTierButtons') else ''}</div>
<a class="lesson-open" href="{link(row['path'])}">Open lesson<span class="quiet" aria-hidden="true"> →</span></a></li>'''

def build():
    source = json.loads((ROOT/'tools/easter/SCIENCE_NAVIGATION.json').read_text())
    rows=source['routes']
    if len({r['path'] for r in rows}) != len(rows):
        raise ValueError('Duplicate Science route')
    for row in rows:
        file=(ROOT/row['path']).resolve()
        if not file.is_relative_to(ROOT) or not file.is_file():
            raise ValueError('Missing Science route: '+row['path'])
        if row['term'] not in TERMS or row['pathway'] not in PATHWAYS or not row['classificationEvidence']:
            raise ValueError('Unresolved source classification: '+row['path'])
    css=(ROOT/'tools/easter/teaching_hub.css').read_text()
    downloads_path=ROOT/'tools/easter/DOWNLOAD_PACKS.json'
    downloads=json.loads(downloads_path.read_text()).get('packs',[]) if downloads_path.is_file() else []
    groups=[]
    for pathway in PATHWAYS:
        for term,label in TERMS.items():
            subset=[r for r in rows if r['pathway']==pathway and r['term']==term]
            if not subset: continue
            subset.sort(key=lambda r:(min(r['calendarWeeks'] or [99]),r['path']))
            mains=[r for r in subset if r['choice']=='main']
            alternatives=[r for r in subset if r['choice']=='alternative']
            pack=next((p for p in downloads if p.get('subject')=='Science' and p.get('pathway')==pathway and p.get('term')==term),None)
            download=''
            if pack and (ROOT/pack['output']).is_file():
                download=f'<a class="button" download href="{link(pack["output"])}">Download {esc(label)} pack · ZIP</a>'
            notes=''
            if pathway=='BUILD' and term=='Aut2':
                notes='<p class="support-note">Rock testing is a four-part sequence. Use its teacher notes to plan those sessions across the available Science periods.</p>'
            groups.append(f'''<section class="term-group" data-pathway="{pathway}" data-term="{term}" id="{pathway.lower()}-{term.lower()}">
<div class="group-head"><div><div class="eyebrow">{pathway} Science</div><h2>{label}</h2><p>Open a main lesson or take the whole pack with you.</p></div>{download}</div>{notes}
<ul class="lesson-list main-list">{''.join(lesson(r) for r in mains)}</ul>
{('<details class="alternatives"><summary>Alternative expanded versions</summary><p class="quiet">The earlier classroom version above is the main route. These versions remain available when their extra scaffolding suits your group.</p><ul class="lesson-list">'+''.join(lesson(r) for r in alternatives)+'</ul></details>') if alternatives else ''}</section>''')
    output=f'''<!doctype html><html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Science · Main lessons and downloads · Made by Matt</title><meta name="description" content="Find BUILD, GROW and LAUNCH Science by term. Main classroom versions, printable resources, downloadable packs and preserved alternatives."><style>{css}</style></head><body>
<header><nav class="breadcrumb" aria-label="Breadcrumb"><a href="../index.html">All lessons</a><a href="../teaching/index.html">Teaching by subject</a></nav>
<div class="hero"><div class="eyebrow">Teesside · 2026–27</div><h1>Science, ready to find.</h1><p class="lead">Choose your pathway and term. Start with the main classroom version: clear models, practical learning and printable pupil resources. Expanded alternatives are kept together below the main lessons.</p><p class="quiet">BUILD: two Science periods each week · GROW: two · LAUNCH: three. Each timetable period is 40 minutes.</p></div>
<nav class="pathways" aria-label="Science pathways">{''.join(f'<a class="pathway {k.lower()}" href="?pathway={k}" data-pathway-link="{k}"><strong>{k}</strong><span>{esc(v)}</span></a>' for k,v in PATHWAYS.items())}</nav></header>
<main><form class="filter-panel" role="search" id="science-filters"><label>Pathway<select id="pathway"><option value="">All pathways</option>{''.join(f'<option>{p}</option>' for p in PATHWAYS)}</select></label><label>Term<select id="term"><option value="">All terms</option>{''.join(f'<option value="{t}">{l}</option>' for t,l in TERMS.items())}</select></label><label class="search-label">Find a lesson<input id="query" type="search" placeholder="e.g. muscles, friction, osmosis" autocomplete="off"></label><button type="button" id="clear">Clear filters</button></form>
<p class="result-count" id="results" role="status">88 main lessons · 35 alternatives</p><noscript><p>All lesson links are available below. Use your browser's Find command to locate a topic.</p></noscript>
{''.join(groups)}<p class="empty" id="empty" hidden>No lessons match those filters. Try another term, pathway or topic.</p>
<p class="support-note">For paper copies, open a lesson and choose its print or evidence tools. Downloaded video links still need the internet; the included lesson pages and pupil tasks can be used offline.</p></main>
<footer><a href="../index.html">Browse the full lesson catalogue</a> · Existing lesson links remain available.</footer>
<script>
(()=>{{'use strict';const $=id=>document.getElementById(id),pathway=$('pathway'),term=$('term'),query=$('query');
function filter(write=true){{let main=0,alt=0;const q=query.value.trim().toLocaleLowerCase();
document.querySelectorAll('.term-group').forEach(group=>{{const groupMatch=(!pathway.value||group.dataset.pathway===pathway.value)&&(!term.value||group.dataset.term===term.value);let found=0;
group.querySelectorAll('.lesson-row').forEach(row=>{{row.hidden=!(groupMatch&&(!q||row.dataset.search.includes(q)));if(!row.hidden){{found++;row.dataset.choice==='main'?main++:alt++;}}}});group.hidden=!found;
const alternative=group.querySelector('.alternatives');if(alternative){{alternative.hidden=![...alternative.querySelectorAll('.lesson-row')].some(row=>!row.hidden);if(q&&!alternative.hidden)alternative.open=true;}}
}});$('results').textContent=main+' main lessons · '+alt+' alternatives';$('empty').hidden=main+alt>0;
if(write){{const url=new URL(location.href);for(const [key,value]of [['pathway',pathway.value],['term',term.value],['q',query.value.trim()]]){{value?url.searchParams.set(key,value):url.searchParams.delete(key);}}try{{history.replaceState(null,'',url);}}catch(_){{}}}}
}}
function restore(){{const params=new URLSearchParams(location.search);pathway.value=params.get('pathway')||'';term.value=params.get('term')||'';query.value=params.get('q')||'';filter(false);}}
pathway.addEventListener('change',()=>filter());term.addEventListener('change',()=>filter());query.addEventListener('input',()=>filter());$('science-filters').addEventListener('submit',event=>event.preventDefault());
$('clear').addEventListener('click',()=>{{pathway.value='';term.value='';query.value='';filter();query.focus();}});
document.querySelectorAll('[data-pathway-link]').forEach(a=>a.addEventListener('click',event=>{{if(event.button||event.ctrlKey||event.metaKey||event.shiftKey||event.altKey)return;event.preventDefault();pathway.value=a.dataset.pathwayLink;filter();pathway.focus();}}));
addEventListener('popstate',restore);restore();}})();
</script></body></html>'''
    destination=ROOT/'Science_Teesside/index.html'
    destination.write_text(output,encoding='utf-8')
    return {'file':str(destination.relative_to(ROOT)),'routes':len(rows),'main':sum(r['choice']=='main' for r in rows),'alternative':sum(r['choice']=='alternative' for r in rows),'groups':len(groups)}

if __name__=='__main__': print(json.dumps(build()))
