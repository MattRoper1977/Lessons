#!/usr/bin/env python3
"""RX3 P0 record: every number below is measured by this script or read from rx2's records, never typed."""
import json,subprocess,hashlib,datetime,os,sys
LM='/home/user/lessons-main';PIN='/home/user/lessons-pin';SITE='/tmp/site-2eaf'
def sh(*a):return subprocess.check_output(a,text=True).strip()
def sha(p):return hashlib.sha256(open(p,'rb').read()).hexdigest()
out=[]
pred={'Site':'2eafa9a4c2a86c440708a1d692bf1d66a3d1cba0','Lessons':'a91780fceea8a1eade23e8a682391902bf7d3ae8','Games':'fbf1aa1163ada27ada2c9bb00bfcb5888bf64d0b','Apps':'65015ed54557d6fe3cf1b218014c588dcdb80c40'}
mains={'Site':sh('git','-C','/home/user/mattroper1977.github.io','rev-parse','origin/main'),'Lessons':sh('git','-C','/home/user/Lessons','rev-parse','origin/main'),'Games':sh('git','-C','/home/user/games','rev-parse','origin/main'),'Apps':sh('git','ls-remote','https://github.com/MattRoper1977/Matt-s-Apps-.git','HEAD').split()[0]}
out.append('## 0b mains');out+=['- %s %s %s'%(k,v[:8],'CONFIRMED' if v==pred[k] else 'MOVED-TO '+v) for k,v in mains.items()]
rx2=json.load(open('/tmp/claude-0/-home-user-Lessons/66c1d222-c1e7-597f-9ba2-ca04f6d2c4f3/scratchpad/rx2_results.json'))
games={'Charcoal':'ea813830','Grid_Chase':'de402aae','Lumins':'eff03ab8','Static':'38a9ece3','The_Last_Lighthouse_v1_1_The_Archipelago_Update_FINAL':'1bab9473','Vortex':'3211c289','Grapple':'cd31d2a3','Marble':'76890535','Neon_Garden':'5d73f3ce','Orbital':'eced4aac','Prism':'899c124d','Wrecking_Crew':'5ba2ee30'}
changed=[g for g,p in games.items() if not sha(f'{LM}/Games/{g}.html').startswith(p)]
out.append('## 0b rx2-measured targets re-hashed on main %s'%mains['Lessons'][:8]);out.append('- twelve games: %d/12 SAME, CHANGED=%s'%(12-len(changed),changed or 'none'))
# chassis donors from rx2 CHASSIS_MAP: donor paths; hash them now and compare with the pack manifest's recorded sha where available
import re
cm=open('/home/user/Lessons/_rx2/CHASSIS_MAP.md').read();donors=re.findall(r'\| (BUILD|GROW|LAUNCH) (ASDAN|Art|Humanities|Science) \| ([^ |]+) \|',cm)
pack='/tmp/claude-0/-home-user-Lessons/66c1d222-c1e7-597f-9ba2-ca04f6d2c4f3/scratchpad/intake/pack33/Classic_Lessons_33_Complete_Pack/manifest.json'
pm=json.load(open(pack)) if os.path.exists(pack) else {}
ptxt=json.dumps(pm)
dch=[]
for fam,sub,path in donors:
    h=sha(f'{LM}/{path}')
    dch.append((fam,sub,path,h[:8],'in-pack-manifest' if h in ptxt else 'NOT-IN-MANIFEST'))
out.append('- twelve chassis donors: %d/12 whole-file sha256 still present in the pack manifest (drift check)'%sum(1 for d in dch if d[4]=='in-pack-manifest'))
out+=['  - %s %s %s %s %s'%d for d in dch if d[4]!='in-pack-manifest']
# 0d Lumins hashes
reg=json.load(open(f'{SITE}/domain-split/play/source-revisions.json'))['payloads']['Lessons/Games/Lumins.html']
out.append('## 0d Lumins');out.append('- served on Lessons main: sha256 %s blob %s'%(sha(f'{LM}/Games/Lumins.html'),sh('git','-C',LM,'rev-parse','HEAD:Games/Lumins.html')))
out.append('- pre-remaster original 13845784: sha256 %s blob %s'%(sha(f'{PIN}/Games/Lumins.html'),sh('git','-C',PIN,'rev-parse','HEAD:Games/Lumins.html')))
out.append('- route %s · registry current=%s · revisions: %s'%(reg['route'],reg['current'],'; '.join('%s blob %s src %s pub %s'%(r['id'],r['git_blob'][:8],r['source_sha256'][:8],r['published_sha256'][:8]) for r in reg['revisions'])))
# 0e admission re-marked
adm=open('/home/user/Lessons/_rx2/ADMISSION.md').read().splitlines()
rows=[l for l in adm if l.startswith('| ') and '**' in l]
remark=[];counts={'REPLACE':0,'ADD':0,'ADD-BESIDE(R3)':0}
for l in rows:
    cells=[c.strip() for c in l.strip('|').split('|')]
    v=cells[-1].strip('*');v2='ADD-BESIDE(R3)' if v=='STOP' else v;counts[v2]+=1
    remark.append('| %s | %s | %s | %s | %s |'%(cells[0],cells[2],cells[3],cells[5],v2))
out.append('## 0e admission (rx2 table, six STOP rows re-marked ADD-BESIDE(R3))');out.append('| id | sheet | cells | donor | verdict |');out.append('|---|---|---|---|---|');out+=remark;out.append('Counts: '+' · '.join('%s %d'%kv for kv in counts.items()))
# 0e R2 week table
cal=json.load(open(f'{LM}/_sownb/CALENDAR_2026_27.json'));ws=cal['weekStarts']
spine=json.load(open(f'{LM}/_sownb/CALENDAR_SPINE.json'))['workbookCells'];cells={x['reference']:x for x in spine}
eng=json.load(open(f'{LM}/build-engine/lessons/foodwise-aut1-w1.json'))
run=datetime.date(2026,9,7)
out.append('## 0e R2 week table (run date %s Europe/London; placement = build-engine slot %r, term %r, FW pages self-label "FoodWise M1 · Week n" in the same slot; grid strand = PfA rows C130–C136 Aut1 W1–W7; the cell TEXT does not name FoodWise — see readback)'%(run,eng['slot'],eng['term']))
out.append('| FoodWise cell | live page | chassis page | SoW placement | calendar week | Monday | started? | R2 → recommended |');out.append('|---|---|---|---|---|---|---|---|')
import glob
for n in range(1,7):
    live=os.path.basename(glob.glob(f'{LM}/BUILD_ASDAN/FoodWise/FW_W{n}_*.html')[0]);ch=f'BUILD_FOOD_W{n}.html';ref="'BUILD Weekly - Autumn'!C%d"%(129+n);c=cells.get(ref,{})
    wk=c.get('absoluteWeek',n);mon=datetime.date.fromisoformat(ws[str(wk)]);started=mon<=run
    out.append('| FW W%d | %s | %s | %s (%s) | %s | %s | %s | %s |'%(n,live,ch,ref,c.get('termWeek','?'),wk,mon,'Y' if started else 'N','LIVE '+live if started else 'CHASSIS '+ch))
print('\n'.join(out))
