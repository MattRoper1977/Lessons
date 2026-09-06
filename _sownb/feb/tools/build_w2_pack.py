#!/usr/bin/env python3
"""Build/update W2 pack support files from already-authored frozen targets."""
from __future__ import annotations
import argparse, hashlib, html, json, re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
BUILD=json.loads((ROOT/'_sownb/w2/BUILD_SET.json').read_text())['build']
CONTRACT=json.loads((ROOT/'_sownb/STYLE_CONTRACT.json').read_text())

CFG={
 'BUILD Science':{'home':'../../../index.html','tokens':'--grow:#4E7A9B;--navy:#10233f;--ink:#1f2937;--muted:#64748b;--paper:#fff;--line:#d8e0e8;--pale:#EAF4F8','accent':'var(--grow)','classes':'hero card','title':'BUILD Science · Weeks 14–20','subtitle':'Review, fossils, soils and light','alias':None},
 'BUILD Humanities':{'home':'../../index.html','tokens':'--ink:#18233F;--steel:#4F869C;--rust:#D06438;--teal:#16877A;--gold:#E1AB32','accent':'var(--steel)','classes':'thread week','title':'BUILD Humanities · Weeks 14–20','subtitle':'Evidence, time, change and caring','alias':None},
 'BUILD ASDAN':{'home':'../../index.html','tokens':'--ink:#17223B;--paper:#FFFCF5;--line:#CAD5DF;--gold:#B57918;--teal:#346B7B;--pale:#EAF6F8;--green:#246B55;--danger:#8A3C2D','accent':'var(--teal)','classes':'grid lesson-link','title':'BUILD ASDAN · Spring 1 · Weeks 1–3','subtitle':'Choice, collaboration and practical planning','alias':'START_HERE_BUILD_ASDAN_AUT2.html'},
}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def contract_value(row_id):return next(r['value'] for r in CONTRACT['rows'] if r['id']==row_id)
def rechain(paths):
 for index,path in enumerate(paths):
  source=path.read_text();match=re.search(r'(<script id="lesson-config" type="application/json">)(.*?)(</script>)',source,re.S)
  if not match:raise RuntimeError(f'no lesson-config: {path}')
  data=json.loads(match.group(2));data['previousFile']='START_HERE.html' if index==0 else paths[index-1].name;data['nextFile']='START_HERE.html' if index==len(paths)-1 else paths[index+1].name
  payload=json.dumps(data,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')
  path.write_text(source[:match.start(2)]+payload+source[match.end(2):],encoding='utf-8')
def start_html(family,items,cfg):
 splash=contract_value('shared.splash.byte-block');cards=[]
 for item in items:
  cards.append(f'<a class="card week lesson-link" href="{html.escape(Path(item["destination"]).name)}"><b>Week {item["week"]}{html.escape(str(item["slot"]))} · {html.escape(item["title"])}</b><span>{html.escape(" · ".join(item["outcomes"]))}</span></a>')
 return f'''<!doctype html><html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(cfg['title'])} · lesson pack</title><style>:root{{{cfg['tokens']}}}*{{box-sizing:border-box}}body{{margin:0;background:var(--paper,#f7f7f7);color:var(--ink);font-family:"Segoe UI",Arial,sans-serif}}main{{max-width:1040px;margin:auto;padding:18px}}.hero,.thread{{background:var(--ink);color:#fff;border-radius:18px;padding:22px;border-bottom:9px solid {cfg['accent']}}}h1{{font-size:clamp(2rem,6vw,3.6rem);line-height:1.05;margin:.2rem 0}}p,span{{line-height:1.45}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(245px,1fr));gap:12px;margin-top:16px}}.card,.week,.lesson-link{{display:block;border:2px solid var(--line,#ccd5df);border-top:8px solid {cfg['accent']};border-radius:13px;padding:14px;background:#fff;color:var(--ink);text-decoration:none;min-height:118px}}.card span,.week span,.lesson-link span{{display:block;margin-top:8px;color:#526173}}.mbmhome{{min-height:44px}}@media(max-width:420px){{main{{padding:10px}}}}@media print{{.mbmhome,.n6-splash{{display:none!important}}}}</style></head><body><!--n6-nav1:v1--><style id="n6-nav1-css">@media print{{.mbmhome,.n6-splash{{display:none!important}}}}.mbmhome{{display:inline-block;margin:6px 0 0 8px;font:600 .85rem/1.4 "Segoe UI",Arial,sans-serif;color:#1e3a8a;text-decoration:none}}.mbmhome:hover,.mbmhome:focus{{text-decoration:underline}}</style><a class="mbmhome" href="{cfg['home']}" aria-label="Back to the Lessons catalogue">← Lessons</a><!--/n6-nav1--><main><header class="hero thread"><p>BUILD · local offline lesson pack</p><h1>{html.escape(cfg['title'])}</h1><p>{html.escape(cfg['subtitle'])}. Open a lesson below; every target resolves inside this folder.</p></header><section class="grid">{''.join(cards)}</section></main>{splash}</body></html>'''
def main():
 p=argparse.ArgumentParser();p.add_argument('--pack',required=True);a=p.parse_args();pack=ROOT/a.pack
 items=[x for x in BUILD if (ROOT/x['destination']).parent==pack and (ROOT/x['destination']).is_file()]
 if not items:raise SystemExit('NO PACK: no authored frozen targets')
 items.sort(key=lambda x:(x['week'],str(x['slot']),x['destination']));family=items[0]['family'];cfg=CFG[family];paths=[ROOT/x['destination'] for x in items];rechain(paths)
 start=pack/'START_HERE.html';start.write_text(start_html(family,items,cfg),encoding='utf-8')
 if cfg['alias']:(pack/cfg['alias']).write_text(start.read_text(),encoding='utf-8')
 manifest={'schema':'w2-pack-v1','family':family,'title':cfg['title'],'start':'START_HERE.html','lessonCount':len(items),'timings':[0,3,3,4,3,3,4,16,4],'lessons':[{'file':Path(x['destination']).name,'week':x['week'],'slot':x['slot'],'title':x['title'],'cells':x['cells'],'outcomes':x['outcomes']} for x in items]}
 (pack/'manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
 files=sorted(list(pack.glob('*.html'))+[pack/'manifest.json'],key=lambda x:x.name)
 (pack/'SHA256SUMS.txt').write_text(''.join(f'{sha(x)}  {x.name}\n' for x in files),encoding='ascii')
 print(json.dumps({'status':'PASS','pack':a.pack,'family':family,'lessonCount':len(items),'files':[x.name for x in files]},indent=2));return 0
if __name__=='__main__':raise SystemExit(main())
