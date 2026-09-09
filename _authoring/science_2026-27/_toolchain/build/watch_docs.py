from pathlib import Path
import concurrent.futures, hashlib, json, subprocess, time

ROOT=Path(__file__).resolve().parents[1]
PY='/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python3'
inflight={}
failed={}

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def render(path):
    log=ROOT/'qa'/(path.stem+'_docs.log')
    with log.open('w') as f:
        run=subprocess.run([PY,str(ROOT/'build/docs.py'),str(path),'--render'],stdout=f,stderr=subprocess.STDOUT)
    return run.returncode, str(log)

with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
    deadline=time.time()+7200
    last_status=0
    while time.time()<deadline:
        for path, future in list(inflight.items()):
            if not future.done(): continue
            code, log=future.result()
            print(json.dumps({'lesson':path.stem,'rendered':code==0,'log':log}),flush=True)
            if code: failed[path]=sha(path)
            del inflight[path]
        ready=[]
        current=[]
        for path in sorted((ROOT/'content').glob('*.json')):
            if path in inflight: continue
            try:
                digest=sha(path)
                d=json.loads(path.read_text())
                if not d.get('pupilPages') or sum(s['minutes'] for s in d['slides'])!=40:continue
                manifest=ROOT/'qa/docs'/d['id']/'manifest.json'
                if manifest.exists() and json.loads(manifest.read_text()).get('source_sha256')==digest:
                    current.append(path.stem);continue
                if failed.get(path)==digest:continue
                ready.append(path)
            except (ValueError,KeyError):continue
        for path in ready[:2-len(inflight)]:
            inflight[path]=pool.submit(render,path)
            print('Rendering '+path.stem,flush=True)
        if time.time()-last_status>60:
            print(json.dumps({'current_docs':len(current),'rendering':len(inflight),'pending':len(ready),'failed':len(failed)}),flush=True)
            last_status=time.time()
        if (ROOT/'qa/STOP_DOC_WATCH').exists() and not inflight: break
        time.sleep(3)
