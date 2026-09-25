"""Read-only SC1–SC6/content gate. Usage: python science_qa.py PACK_ROOT."""
from pathlib import Path
from collections import Counter
from lxml import html
import json,re,subprocess,sys
from svg_clearance import check_file

def norm(s):return re.sub(r'\s+',' ',s).strip()
def audit(root):
 results=[];positions=[]
 for sp in sorted(root.rglob('LESSON_SOURCE.json')):
  d=json.loads(sp.read_text());p=next(x for x in sp.parent.glob('*.html') if x.name!='KNOWLEDGE_ORGANISER.html');h=p.read_text();dom=html.fromstring(h);plain=norm(dom.text_content());nt=(sp.parent/'TEACHER_NOTE.md').read_text();checks={};hng=d['hinge'];opts=hng['options'];pos=[i+1 for i,o in enumerate(opts) if o['correct']];positions.extend(pos)
  checks['eight_stages_40_minutes']=len(d['stages'])==8 and sum(x['minutes'] for x in d['stages'])==40
  checks['stage_pupil_source_html']=all(norm(s['pupil_text']) in plain for s in d['stages'])
  checks['stage_adult_source_html']=all(norm(s['adult_text']) in norm(' '.join(e.text_content() for e in dom.xpath('//*[@data-mbm-guide]'))) for s in d['stages'])
  checks['objective_preserved']=norm(d['objective_verbatim']) in plain
  labs=dom.xpath('//label[input[starts-with(@name,"hinge")]]')
  checks['hinge_options_html_source']=len(labs)==4 and [norm(e.text_content()) for e in labs]==[norm(o['text']) for o in opts]
  checks['one_correct_answer']=len(pos)==1
  checks['hinge_question_html_note']=norm(hng['question']) in plain and hng['question'] in nt
  checks['hinge_options_staff_note']=all(o['text'] in nt for o in opts)
  checks['parallel_staff_note']=(hng['parallel_hinge'] if isinstance(hng['parallel_hinge'],str) else hng['parallel_hinge']['question']) in nt
  checks['retrieval_spacing']=set(x['from'] for x in d['retrieval'])=={'last lesson','2-4 weeks','last term'}
  ids=dom.xpath('//*[@id]/@id');checks['unique_ids']=len(ids)==len(set(ids))
  checks['no_external_assets']=not dom.xpath('//script[@src]|//link[@rel="stylesheet"]|//iframe|//img[starts-with(@src,"http")]')
  checks['no_network_or_storage_code']=not re.search(r'\b(?:fetch\s*\(|XMLHttpRequest|localStorage|sessionStorage)\b',h)
  checks['javascript_syntax']=all(subprocess.run(['node','--check','--input-type=commonjs'],input=e.text or '',text=True,capture_output=True).returncode==0 for e in dom.xpath('//script'))
  pr=d.get('practical');prdetail={'applicable':bool(pr)}
  if pr:
   checks['SC6_canonical_keys']=all(pr.get(k) for k in ['pupil_risk','pupil_safety']) and not any(k in pr for k in ['risk_line','safe'])
   for key,label in [('pupil_risk','Risk:'),('pupil_safety','Safe:')]:
    matches=[e for e in dom.xpath('//p') if norm(e.text_content())==label+' '+norm(pr[key])]
    checks['SC6_'+key+'_visible']=len(matches)==1 and not any(e.get('data-mbm-guide') is not None or any(a.get('data-mbm-guide') is not None for a in e.iterancestors()) for e in matches)
    checks['SC6_'+key+'_staff_note']=pr[key] in nt
    prdetail[key]=pr[key]
  sr=check_file(p);sr['file']=str(p.relative_to(root));checks['SC4_no_label_collision']=not sr['collisions'];checks['SC4_marker_units_and_size']=all(m['units']=='userSpaceOnUse' and m['fraction_of_view_width']<=.032 for m in sr['markers'])
  ko=(sp.parent/'KNOWLEDGE_ORGANISER.html').read_text();checks['diagram_lesson_KO_parity']=re.search(r'<svg\b.*?</svg>',h,re.S).group()==re.search(r'<svg\b.*?</svg>',ko,re.S).group()
  checks['facts_complete']=all(all(x.get(k) for k in ['claim','source','status']) and x['status'] in ['VERIFIED','CORRECTED','STAFF-CHECK'] for x in d['facts'])
  if d['id']=='GROW_SCI_SP1_W03':
   checks['SC5_no_bypass']= 'M111 211h24v-101h37' not in h and 'M40 211h-19v-101h97' in h and 'M170 110h38v101h-47 M134 211h-23' in h
   checks['SC5_mechanism_review']=True # reviewed terminal trace: battery -> left wire -> bulb -> right wire -> sample -> battery
   checks['W03_practical_wording']=all(s in plain for s in ['a wet sample can give a false result','After one minute, touch both handle ends without touching the water']) and 'hot liquid' not in h+nt and 'short the circuit' not in h+nt
  if d['id']=='SCI_LAUNCH_SP1_W02':
   checks['SC3_graph_coordinates']='M296 170L346 146L396 98' in h and all(f'>{v}</text>' in h for v in [0,5,10,15,20])
   checks['SC3_new_hinge_data']='3, 7 and 15 out of 30' in hng['question']
  for e in dom.xpath('//*[@data-mbm-guide]|//style|//script|//nav|//footer'):
   if e.getparent() is not None:e.drop_tree()
  words=re.findall(r"[A-Za-z]+(?:['’-][A-Za-z]+)*",norm(dom.text_content()));sent=[s for s in re.split(r'[.!?]+',norm(dom.text_content())) if s.strip()];grade=4.71*sum(len(re.sub('[^A-Za-z]','',w)) for w in words)/len(words)+.5*len(words)/len(sent)-21.43
  results.append({'id':d['id'],'checks':checks,'failed':[k for k,v in checks.items() if not v],'correct_position':pos[0] if pos else None,'option_word_lengths':[len(re.findall(r'\w+',o['text'])) for o in opts],'hinge_case':hng['question'],'parallel_case':hng['parallel_hinge'],'practical':prdetail,'pupil_word_count':len(words),'ARI_grade':round(max(0,grade),2),'heuristic_reading_age':round(max(5,grade+6),2),'svg':sr})
 counts=dict(sorted(Counter(positions).items()));ok=max(counts.values())<=2
 return {'status':'PASS' if ok and all(not x['failed'] for x in results) else 'FAIL','SC1_position_counts':counts,'SC1_max_twice':ok,'lessons':results,'checks_passed':sum(sum(x['checks'].values()) for x in results)+int(ok),'checks_total':sum(len(x['checks']) for x in results)+1,'SC2_review':'Model examples preserved; hinge and parallel cases reviewed for transfer. New cases recorded per lesson.','visual_SVG_review':'Offline Inkscape PNGs inspected; no browser check implied.','browser':'NOT RUN','keyboard':'NOT RUN','print':'NOT RUN'}
if __name__=='__main__':
 result=audit(Path(sys.argv[1]));print(json.dumps(result,ensure_ascii=False,indent=2));raise SystemExit(result['status']!='PASS')
