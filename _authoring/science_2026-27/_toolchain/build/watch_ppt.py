from pathlib import Path
import subprocess,json,hashlib,time,datetime
R=Path('/workspace/scratch/53a97a57d058/science_next24')
NODE='/opt/codex/runtimes/codex-primary-runtime/dependencies/node/bin/node'
failed={}
while not (R/'qa/ppt/STOP_WATCH').exists():
    batch=[]
    for src in sorted((R/'content').glob('*.json')):
        try:
            raw=src.read_bytes();d=json.loads(raw)
            if not d.get('slides'):continue
            sha=hashlib.sha256(raw).hexdigest();m=R/'qa/ppt'/d['id']/'build-manifest.json'
            if m.exists() and json.loads(m.read_text()).get('sourceSha256')==sha:continue
            if failed.get(str(src))==sha:continue
            batch.append((src,sha))
        except (json.JSONDecodeError,KeyError):continue
    if batch:
        for src,sha in batch:
            result=subprocess.run([NODE,str(R/'build/ppt.mjs'),str(src)])
            if result.returncode:failed[str(src)]=sha
        continue
    time.sleep(2)
