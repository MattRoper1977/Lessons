#!/usr/bin/env python3
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile

from build_download_pack import digest
from build_science_offline_pack import adapt_html, build_offline

BASE=Path(__file__).parent
REPO=BASE.resolve().parents[1]
HUD=BASE/'vendor/hud.js'


def controls():
    rows=[]
    def check(name, condition):
        assert condition, name
        rows.append({'id':name,'pass':True})
    with tempfile.TemporaryDirectory() as tmp:
        temp=Path(tmp)
        definition=json.loads((BASE/'definitions/grow-science-aut1-main.json').read_text())
        report=build_offline(REPO,definition,HUD,digest(HUD.read_bytes()),temp/'pack.zip')
        check('all-five-grow-hud-loaders-adapted',report['status']=='BUILT' and report['offlineAdaptation']['sourceFilesChanged']==5)
        with zipfile.ZipFile(temp/'pack.zip') as z:
            check('site-hud-byte-exact',z.read('hud.js')==HUD.read_bytes())
            check('offline-back-destination-exists','Lessons/index.html' in z.namelist())
            for row in report['offlineAdaptation']['sourceFiles']:
                if row['adaptations']:
                    data=z.read(row['member']).decode()
                    check('ordered-local-loader-'+Path(row['source']).stem,
                        '<script defer src="../../../hud.js"></script><script defer src="../../../offline-hud-navigation.js"></script>' in data
                        and 'add("/hud.js"' not in data)
        again=build_offline(REPO,definition,HUD,digest(HUD.read_bytes()),temp/'repeat.zip')
        check('adapted-zip-rebuild-deterministic',report['zipSha256']==again['zipSha256'])
        try:
            build_offline(REPO,definition,HUD,'0'*64)
        except ValueError:
            check('changed-hud-pin-refused',True)
        else:
            raise AssertionError('changed HUD not refused')
        try:
            adapt_html(b'<script id="grow-hud-loader">unknownLoader()</script>','Lessons/a.html',1)
        except ValueError:
            check('changed-grow-loader-refused',True)
        else:
            raise AssertionError('changed loader not refused')
        try:
            adapt_html(b'<script src="/hud.js"></script>','Lessons/a.html',2)
        except ValueError:
            check('mismatched-adaptation-count-refused',True)
        else:
            raise AssertionError('mismatched count not refused')
        # Unit-level DOM fixture: real adapter, real URL resolution; no claim of
        # full browser/HUD acceptance is made by this focused check.
        js = r'''
const fs=require('fs'),vm=require('vm');
function node(attrs){return {attrs:{...attrs},textContent:'',setAttribute(k,v){this.attrs[k]=v;},getAttribute(k){return this.attrs[k];},querySelector(){return this.caption;},caption:{textContent:'Pupils & learners'}};}
const back=node({href:'/Lessons/'}),home=node({href:'/for/pupils/',title:'Your homepage: Pupils & learners','aria-label':'Your homepage: Pupils & learners'});
const doc={currentScript:{src:'file:///tmp/extracted/offline-hud-navigation.js'},getElementById(id){return id==='mbmhud-back'?back:id==='mbmhud-home'?home:null;}};
vm.runInNewContext(fs.readFileSync(process.argv[1],'utf8'),{document:doc,URL});
if(back.attrs.href!=='file:///tmp/extracted/Lessons/index.html')throw Error('offline back wrong');
if(home.attrs.href!=='https://madebymatt.uk/for/pupils/'||!home.attrs['aria-label'].includes('needs internet'))throw Error('chosen home changed or unlabelled');
const src=fs.readFileSync(process.argv[2],'utf8');
const part=src.split('  /* ---------- styles ---------- */')[0]+'globalThis.classification={lesson:IS_LESSON,back:BACK}; }catch(e){throw e}})();';
const context={window:{},location:{pathname:'/tmp/extracted/Lessons/Science_Teesside/Grow/lesson.html'},localStorage:{getItem(){return null;}}};
vm.runInNewContext(part,context);
if(!context.classification.lesson||context.classification.back.h!=='/Lessons/')throw Error('exact HUD lesson activation failed');
const negative={window:{},location:{pathname:'/tmp/extracted/Science_Teesside/Grow/lesson.html'},localStorage:{getItem(){return null;}}};
vm.runInNewContext(part,negative);
if(negative.classification.lesson)throw Error('negative path control did not distinguish wrapper');
console.log('adapter navigation and exact HUD path predicate passed');
'''
        subprocess.run(['node','-e',js,str(BASE/'offline-hud-navigation.js'),str(HUD)],check=True,capture_output=True,text=True)
        check('real-adapter-local-back-and-online-home',True)
        check('exact-hud-path-predicate-positive-and-negative',True)
    return rows


if __name__=='__main__':
    rows=controls()
    (BASE/'offline-hud-controls.json').write_text(json.dumps({'controls':rows,'passed':len(rows),'failed':0},indent=2)+'\n')
    print(f'{len(rows)}/{len(rows)} offline HUD adaptation controls passed')
