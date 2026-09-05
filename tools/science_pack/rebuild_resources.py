"""Add the inherited resource content to the landed Science chassis.

Keep every existing timed stage, CSS rule and executable inline script intact.
The resource page remains usable if the optional dialog enhancement cannot load.
"""
from pathlib import Path
from html import escape
from lxml import html
import json,re,shutil,hashlib,subprocess

REPO=Path(__file__).resolve().parents[2]
DEST=REPO/'Science_Teesside/Launch/resources'
LESSONS=json.loads((Path(__file__).parent/'RESOURCE_CONTENT.json').read_text())
ACT={c['id']:c['activity'] for c in LESSONS}
H=lambda s:escape(str(s),quote=True)
CONCEPT={'L5StAE_uuxM':'W3L1','O965gA4goVI':'W4L1','aPUPfzsqDgs':'W4L2','B0cH91joZwA':'W5L1','ECldVkp6Rw0':'W6L1'}
FALLBACK={
'L5StAE_uuxM':'Magnification compares image size with actual size. Resolution is the ability to distinguish two close points as separate. Increasing size alone does not reveal more detail.',
'O965gA4goVI':'Particles continue to move randomly and cross in both directions. At equilibrium the crossings balance, so there is no net movement.',
'aPUPfzsqDgs':'A thin wall gives a short diffusion distance. Oxygen moves down its concentration gradient from alveolar air into the arriving blood.',
'B0cH91joZwA':'Water moves through a partially permeable membrane. Its net movement is from a more dilute solution to a more concentrated solution.',
'ECldVkp6Rw0':'Active transport causes net movement against the concentration gradient and requires energy released by respiration. The cell type alone does not prove the mechanism.'}

def content(c,prefix):
 a=ACT[c['id']];v=c['video'];concept=CONCEPT[v['id']]
 files=''.join(f'<a class="mbm-sp-button" href="{prefix}{c["id"]}_{t}.pdf">{label} worksheet PDF</a>' for t,label in [('supported','Supported'),('standard','Standard'),('depth','Depth')])
 if c['id']=='W7L3':files+=f'<a class="mbm-sp-button" href="{prefix}LAUNCH_Science_Assessment.pdf">Week 7 assessment PDF · 24 marks</a>'
 table=''
 if a.get('table'):
  rows=a['table'];table='<div class="mbm-sp-table-wrap"><table><thead><tr>'+''.join('<th scope="col">'+H(x)+'</th>' for x in rows[0])+'</tr></thead><tbody>'
  for row in rows[1:]:table+='<tr>'+''.join(('<th scope="row">' if i==0 else '<td>')+H(x)+('</th>' if i==0 else '</td>') for i,x in enumerate(row))+'</tr>'
  table+='</tbody></table></div><p>'+H(a['after'])+'</p>'
 else:table='<ol>'+''.join('<li>'+H(x)+'</li>' for x in a['items'])+'</ol>'
 route=''
 if c['id']=='W5L2':route='<p class="mbm-sp-notice"><strong>Wednesday route:</strong> default cover work is planning and calculation using explicitly supplied sample data. Use a practical only when the equipment, supervision, local risk assessment and soak/measurement handover have already been arranged. Record only practical steps pupils actually complete.</p>'
 elif c['id']=='W5L3':route='<p class="mbm-sp-notice"><strong>Friday analysis:</strong> use the labelled sample dataset below, or a clearly identified set of measurements collected during the arranged practical. Keep raw results visible. Sample-data analysis does not record practical completion.</p>'
 elif c['id']=='W7L3':route='<p class="mbm-sp-notice"><strong>Assessment choice:</strong> the separate full paper is 24 marks and needs a 25-minute slot. Within this lesson’s existing 15-minute independent stage, Q2, Q3 and Q5 provide an 11-mark selection. This is an original classroom assessment, not an official exam paper.</p>'
 stem=c['id'].lower()
 return f'''<p class="mbm-sp-kicker">LAUNCH Science · {H(c['id'])} · lesson resources</p>
<h2>{H(a['title'])}</h2>
<p>Choose one shared task or resource within the current lesson stage. Keep the lesson’s 40-minute timetable and 15-minute independent work.</p>
{route}
<div class="mbm-sp-files">{files}</div>
<details class="mbm-sp-section" open><summary>We Do · {H(a['title'])}</summary>
<p><strong>{H(a['prompt'])}</strong></p>{table}
<p>Discuss, point, write or dictate your first reason. Use one example first; extend only if there is time.</p>
<label class="mbm-sp-label" for="{stem}-first">Our first reason <span>(optional written record)</span></label>
<textarea id="{stem}-first" rows="3" placeholder="Keep your first idea here, or give it aloud."></textarea>
<details class="mbm-sp-answer"><summary>Reveal shared reasoning after an attempt</summary><p>{H(a['check']).replace(chr(10),'<br>')}</p></details>
<label class="mbm-sp-label" for="{stem}-repair">One change to our explanation</label><textarea id="{stem}-repair" rows="2"></textarea>
<p class="mbm-sp-small">This page keeps your writing while it stays open. It does not save or send it.</p></details>
<details class="mbm-sp-section"><summary>Model explanation and diagram</summary>
<figure><img src="{prefix}{c['id']}_model.svg" alt="Scientific model supporting {H(c['topic'])}"><figcaption>A model illustration. Use the stated measurements for calculations.</figcaption></figure>
<p>{H(c['extra']['say'])}</p><p><strong>Watch for:</strong> {H(c['extra']['trap'])}</p>
<details><summary>Give a smaller support cue</summary><p>{H(c['support'])}</p></details></details>
<details class="mbm-sp-section"><summary>Optional video · {H(v['title'])}</summary>
<p><strong>Watch for:</strong> {H(v['question'])}</p><p>Use a short relevant extract within I Do, then pause for an explanation. The clip replaces part of the modelling time.</p>
<div class="mbm-sp-video" data-video="{H(v['id'])}" data-video-title="{H(v['title'])}"><button type="button" class="mbm-sp-button" data-play-video>Play video here</button></div>
<p><a href="https://www.youtube.com/watch?v={H(v['id'])}" target="_blank" rel="noopener noreferrer">Open the freesciencelessons video in a new tab</a></p>
<details open><summary>No-video version · use the same question</summary><figure><img src="{prefix}{concept}_model.svg" alt="Still model for {H(v['title'])}"></figure><p>{H(FALLBACK[v['id']])}</p></details>
<p class="mbm-sp-small">Internet is needed for the optional clip. It is concept teaching; viewing it is not completion of a practical.</p></details>'''

report=[]
for c in LESSONS:
 page=content(c,'')
 (DEST/(c['id']+'.html')).write_text(f'<!doctype html><html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{H(c["id"])} · LAUNCH Science resources</title><link rel="stylesheet" href="pack.css"></head><body class="mbm-sp-page"><main class="mbm-sp-body"><nav><a href="../{H(Path(c["online_path"]).name)}">Return to the lesson</a> · <a href="../../../index.html?subject=Science">Browse Science</a></nav>{page}</main><script src="pack.js" defer></script><script defer src="/hud.js"></script></body></html>\n')
 f=REPO/c['online_path'];before=f.read_text()
 # Preserve idempotency while leaving all previous scripts/styles byte-identical.
 before=re.sub(r'\n?<!-- MBM LAUNCH PACK START -->.*?<!-- MBM LAUNCH PACK END -->\n?', '',before,flags=re.S)
 before=re.sub(r'<!-- MBM PACK LINK -->.*?<!-- MBM PACK LINK END -->','',before,flags=re.S)
 old=html.fromstring(before)
 # Precise content correction to the inherited plant-cell hotspot; engine untouched.
 repaired=before.replace('Only plant cells have one.','Plant cells have a cell wall; animal cells do not. Fungi and bacteria also have cell walls.')
 link=f'<!-- MBM PACK LINK --><a class="ghost small mbm-sp-entry" href="resources/{c["id"]}.html" data-open-science-pack>Resources · shared task, PDFs and video</a><!-- MBM PACK LINK END -->'
 repaired,n=re.subn(r'(<h3\b[^>]*>[^<]*Teacher print tools</h3>)',lambda m:m[1]+link,repaired,count=1,flags=re.I)
 assert n==1,('Missing title print tools',c['id'])
 addition=f'''\n<!-- MBM LAUNCH PACK START -->
<link rel="stylesheet" href="resources/pack.css">
<dialog id="mbm-science-pack" class="mbm-sp-dialog" aria-labelledby="mbm-sp-heading"><div class="mbm-sp-closebar"><h2 id="mbm-sp-heading">Lesson resources · {c['id']}</h2><form method="dialog"><button type="submit" class="mbm-sp-button">Return to lesson</button></form></div><div class="mbm-sp-body">{content(c,'resources/')}</div></dialog>
<template id="mbm-sp-entry"><a class="ghost small mbm-sp-entry" href="resources/{c['id']}.html" data-open-science-pack>Resources · shared task, PDFs and video</a></template>
<script src="resources/pack.js" defer></script>
<!-- MBM LAUNCH PACK END -->\n'''
 f.write_text(repaired.replace('</body>',addition+'</body>'))
 after=html.fromstring(f.read_text())
 stages=lambda d:[(x.get('data-title'),x.get('data-timer')) for x in d.xpath('//*[contains(concat(" ",normalize-space(@class)," ")," slide ")]')]
 styles=lambda d:[x.text for x in d.xpath('//style')]
 scripts=lambda d:[x.text for x in d.xpath('//script[not(@src) and not(@type="application/json")]')]
 assert stages(old)==stages(after),c['id']
 assert styles(old)==styles(after),c['id']
 assert scripts(old)==scripts(after),c['id']
 report.append({'id':c['id'],'path':c['online_path'],'stages_and_timers_unchanged':True,'existing_css_unchanged':True,'existing_executable_inline_scripts_unchanged':True,'source_sha256':hashlib.sha256(f.read_bytes()).hexdigest()})
print('Updated',len(report),'resource pages and in-lesson panels. Existing timing, CSS and executable inline scripts preserved.')
