from pathlib import Path
import json
R=Path('/workspace/scratch/53a97a57d058/science_next24/content')
p=R/'grow_irreversible_change_detectives.json';d=json.loads(p.read_text())
d['interactive']['steps'][2]['question']='Which result can cooling the remaining liquid wax produce?'
p.write_text(json.dumps(d,ensure_ascii=False,indent=2))
p=R/'launch_ecosystem_evidence_web.json';d=json.loads(p.read_text())
# Amend only the reviewed scientific diagram, its paired interactive copy and exact prose fields.
for v in [d['slides'][2]['visual'],d['interactive']['steps'][0]['visual']]:
 for e in v['elements']:
  if e.get('text')=='Plant cover\nchanges shade':e['text']='Plant cover\nchanges\nshade';e['h']=95
for v in [d['slides'][3]['visual'],d['interactive']['steps'][1]['visual']]:
 v['elements']=[e for e in v['elements'] if not (e['type']=='line' and e['x']==840 and e['y']==365 and e['x2']==840 and e['y2']==195)]
 v['description']=v['description'].replace('blue tits eat caterpillars, aphids and ladybirds','blue tits eat caterpillars and aphids')
b=d['pupilPages'][0]['blocks'][0];b['text']=b['text'].replace('; ladybirds → blue tits','')
d['slides'][3]['notes']=d['slides'][3]['notes'].replace('leaves→aphids→ladybirds→blue tits and leaves→caterpillars→blue tits','leaves → aphids → ladybirds and leaves → caterpillars → blue tits')
for a in d['answers']:
 if a['label']=='N1–N4':
  a['answer']=a['answer'].replace('leaves→aphids→ladybirds→blue tits and leaves→caterpillars→blue tits','leaves → aphids → ladybirds and leaves → caterpillars → blue tits').replace('abundance20','abundance 20').replace('A2/B4','A 2 / B 4')
 if a['label']=='T1–T3':a['answer']=a['answer'].replace('blue tits could be affected directly or through ladybirds but have other food','blue tits could lose aphids as prey but have other food')
 if a['label']=='W1–W3':a['answer']=a['answer'].replace('B4','B 4')
 if a['label']=='Evidence and responsive teaching':a['answer']=a['answer'].replace('A2/B4','A 2 / B 4').replace('abundance20','abundance 20')
d['teacherNotes'][2]=d['teacherNotes'][2].replace('Topic9','Topic 9').replace('Topic7–8','Topics 7–8')
p.write_text(json.dumps(d,ensure_ascii=False,indent=2))
