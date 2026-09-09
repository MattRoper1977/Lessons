import json,copy
from pathlib import Path
p=Path('/workspace/scratch/53a97a57d058/science_next24/content/build_plant_parts_atlas.json');d=json.loads(p.read_text());page=d['pupilPages'][0];v=copy.deepcopy(d['slides'][2]['visual'])
v['title']='Identify A–D on the plant';v['description']='Simplified flowering plant with letter-only leaders: A points to branching roots below soil, B to upright stem, C to leaves, D to flower. Names are for pupils to supply.'
for e in v['elements']:
 if e.get('text') in ['A  Roots','B  Stem','C  Leaves','D  Flower']:e['text']=e['text'][0]+' __________'
page['intro']='Identify A–D on this simplified plant. Use location and shape clues.'
page['blocks']=[{'type':'visual','visual':v},{'type':'text','text':'E • Observation record: a potted shoot has a visible stem and leaves. Its roots are hidden by the pot; no flower is visible today.'},{'type':'response','prompt':'W1. Name A, B, C and D. Give one location clue.','lines':1},{'type':'response','prompt':'W2. Improve “the plant in E has no roots or flowers”.','lines':1}]
d['slides'][5]['notes']=d['slides'][5]['notes'].replace('Paper route uses the descriptions.','Paper route uses the lettered plant diagram and observation E.')
for a in d['answers']:
 if a['label'] in ['We do W1–W2','We do W1-W2'] and 'Location clue:' not in a['answer']:
  a['answer']=a['answer'].replace('W2 roots','Location clue: roots branch below the soil, leaves attach along the stem, or flower has petals in this example. W2 roots')
p.write_text(json.dumps(d,ensure_ascii=False,indent=2))
