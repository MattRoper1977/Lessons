#!/usr/bin/env python3
"""Exercise the shipped slot reader in Node, including its async file/fetch paths."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[2]
READER = ROOT / 'tools/artsaward/slot_reader.js'
CONTROL_IDS = [
    'empty-and-unconfirmed-slots-stay-preparation-only',
    'confirmation-requires-a-name-and-a-real-route',
    'hosted-reader-loads-current-json-without-a-cache',
    'offline-reader-loads-the-selected-json-file',
    'malformed-missing-and-oversize-sources-are-refused',
    'one-source-update-changes-the-next-read',
]

JS = r'''
const api = require(process.argv[1]);
const clone = x => JSON.parse(JSON.stringify(x));
const source = {schema:'arts-award-slots-v1',slots:{EVENT_SLOT:{entries:[]}}};
const key = ['EVENT_SLOT'];
const rows=[];
function rec(id, expected, observed) {
 rows.push({id,expected,observed,fired:JSON.stringify(expected)===JSON.stringify(observed)});
}
async function refuses(fn){try {await fn();return false;}catch{return true;}}
(async()=>{
 const unconfirmed=clone(source);unconfirmed.slots.EVENT_SLOT.entries=[{name:'Fixture',route:'R1',status:'UNCONFIRMED'}];
 rec('empty-and-unconfirmed-slots-stay-preparation-only',[false,false],
     [api.readSlots(source,key)[0].ready,api.readSlots(unconfirmed,key)[0].ready]);
 const outcomes=[];
 for(const e of [{status:'CONFIRMED'}, {name:'Fixture',status:'CONFIRMED'},
   {name:'Fixture',route:'R9',status:'CONFIRMED'}, {name:'Fixture',route:'R2',status:'CONFIRMED'}]) {
  const doc=clone(source);doc.slots.EVENT_SLOT.entries=[e];outcomes.push(api.readSlots(doc,key)[0].ready);
 }
 rec('confirmation-requires-a-name-and-a-real-route',[false,false,false,true],outcomes);
 const ready=clone(source);ready.slots.EVENT_SLOT.entries=[{name:'Fixture event',route:'R3',status:'CONFIRMED'}];
 let called;
 const hosted=await api.loadHosted('/current.json',key,async(url,options)=>{
  called={url,...options};return {ok:true,json:async()=>ready};
 });
 rec('hosted-reader-loads-current-json-without-a-cache',
     {ready:true,url:'/current.json',cache:'no-store',credentials:'same-origin'},
     {ready:hosted[0].ready,...called});
 const local=await api.loadFile({size:100,text:async()=>JSON.stringify(ready)},key);
 rec('offline-reader-loads-the-selected-json-file',['Fixture event',true],
     [local[0].entries[0].name,local[0].ready]);
 const bad=[];
 bad.push(await refuses(()=>api.readSlots({},key)));
 bad.push(await refuses(()=>api.readSlots(source,['ABSENT'])));
 bad.push(await refuses(()=>api.loadFile({size:1,text:async()=>'{bad'},key)));
 bad.push(await refuses(()=>api.loadFile({size:1048577,text:async()=>JSON.stringify(ready)},key)));
 bad.push(await refuses(()=>api.loadHosted('/no',key,async()=>({ok:false}))));
 rec('malformed-missing-and-oversize-sources-are-refused',[true,true,true,true,true],bad);
 const changed=clone(ready);changed.slots.EVENT_SLOT.entries[0].name='Updated fixture';
 const next=await api.loadFile({size:100,text:async()=>JSON.stringify(changed)},key);
 rec('one-source-update-changes-the-next-read',['Fixture event','Updated fixture'],
     [local[0].entries[0].name,next[0].entries[0].name]);
 console.log(JSON.stringify(rows));
})().catch(error=>{console.error(error);process.exit(1);});
'''


def self_test():
    completed = subprocess.run(['node', '-e', JS, str(READER)], capture_output=True, text=True)
    if completed.returncode:
        raise RuntimeError(completed.stderr)
    rows = json.loads(completed.stdout)
    seen = [r['id'] for r in rows]
    missing = [key for key in CONTROL_IDS if key not in seen]
    return {'tool': 'award-slot-reader', 'file': 'tools/artsaward/slot_reader.js',
            'sha256': hashlib.sha256(READER.read_bytes()).hexdigest(),
            'controlsDeclared': len(CONTROL_IDS), 'controlsRun': len(rows),
            'controlsFired': sum(r['fired'] for r in rows), 'missingControls': missing,
            'allListedControlsFired': not missing and all(r['fired'] for r in rows),
            'controls': rows}


if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--list-controls',action='store_true')
    parser.add_argument('--self-test',action='store_true')
    parser.add_argument('--output')
    args=parser.parse_args()
    if args.list_controls:
        print('\n'.join(CONTROL_IDS));raise SystemExit(0)
    result=self_test()
    if args.output:Path(args.output).write_text(json.dumps(result,indent=1)+'\n')
    for row in result['controls']:
        print(('ok ' if row['fired'] else 'FAIL ') + row['id'])
    print(f"{result['controlsFired']}/{result['controlsRun']} controls fired")
    raise SystemExit(0 if result['allListedControlsFired'] else 1)
