#!/usr/bin/env python3
"""HUM-D5 A3 E8 - video legs with PyAV (bundled ffmpeg; the Playwright Chromium build has
no H.264 decoder, so render_e8_video.js could not load metadata on any file).
Per *_Captioned_Model.mp4: DECODE (every frame of the video stream is decoded; any
decoder error is recorded), DURATION (container mvhd, must be 30-40 s), the EMBEDDED
COPY (the lesson HTML's data:video/mp4 payload is compared byte-for-byte with the
file), BLANK FRAMES (8 frames at even intervals: mean luminance and standard
deviation on a 4x-subsampled grey grid; sd < 2 is blank), SAFE AREA (bounding box of
pixels differing from the corner background by > 60 vs the 5% title-safe margin).
Caption OCR is NOT RUN (no tesseract). Prints its search scope."""
import av, sys, os, glob, json, struct, hashlib, base64, re
import numpy as np
ROOT, OUT = sys.argv[1], sys.argv[2]
def mvhd(path):
    d=open(path,'rb').read(); i=d.find(b'mvhd')
    if i<0: return None
    v=d[i+4]
    if v==0: ts,du=struct.unpack('>II',d[i+16:i+24])
    else: ts=struct.unpack('>I',d[i+24:i+28])[0]; du=struct.unpack('>Q',d[i+28:i+36])[0]
    return du/ts if ts else None
files=sorted(glob.glob(os.path.join(ROOT,'**','*_Captioned_Model.mp4'),recursive=True)); R=[]
for f in files:
    lid=os.path.basename(f).replace('_Captioned_Model.mp4',''); rec={'lesson_id':lid,'file':os.path.relpath(f,ROOT),'bytes':os.path.getsize(f),'duration_mvhd':mvhd(f)}
    try:
        c=av.open(f); vs=c.streams.video[0]; rec['codec']=vs.codec_context.name; rec['size']=[vs.width,vs.height]; rec['fps']=float(vs.average_rate) if vs.average_rate else None
        frames=[]; n=0; errs=0
        for fr in c.decode(vs):
            n+=1; frames.append(fr) if n%1==0 else None
        rec['frames_decoded']=n; rec['stream_duration']=float(vs.duration*vs.time_base) if vs.duration else None
        N=8; idx=[int((i+0.5)*n/N) for i in range(N)]; samples=[]
        for k in idx:
            fr=frames[min(k,n-1)]; g=fr.to_ndarray(format='gray')[::4,::4].astype(np.float32); rgb=fr.to_ndarray(format='rgb24')[::4,::4].astype(np.int16)
            bg=rgb[0,0]; diff=np.abs(rgb-bg).sum(axis=2)>60; ys,xs=np.nonzero(diff)
            H,W=diff.shape; box=[int(xs.min()),int(ys.min()),int(xs.max()),int(ys.max())] if len(xs) else None
            inside=bool(box and box[0]>=W*0.05 and box[2]<=W*0.95 and box[1]>=H*0.05 and box[3]<=H*0.95) if box else None
            samples.append({'frame':int(k),'t':round(float(fr.pts*vs.time_base),2) if fr.pts is not None else None,'mean':round(float(g.mean()),1),'sd':round(float(g.std()),1),'blank':bool(g.std()<2),'box':box,'inside_safe':inside})
        rec['samples']=samples; rec['blank_frames']=sum(s['blank'] for s in samples); rec['frames_outside_safe']=sum(1 for s in samples if s['inside_safe'] is False)
        c.close()
    except Exception as e: rec['decode_error']=str(e)[:160]
    rec['duration_ok']=bool(rec['duration_mvhd'] and 30<=rec['duration_mvhd']<=40)
    lesson=os.path.join(os.path.dirname(f),lid+'_Lesson.html')
    if os.path.exists(lesson):
        t=open(lesson,encoding='utf-8').read(); m=re.search(r'src="data:video/mp4;base64,([A-Za-z0-9+/=]+)"',t)
        if m:
            payload=base64.b64decode(m.group(1)); rec['embedded']={'present':True,'bytes':len(payload),'identical_to_file':hashlib.sha256(payload).hexdigest()==hashlib.sha256(open(f,'rb').read()).hexdigest()}
        else: rec['embedded']={'present':False}
    R.append(rec)
json.dump({'scope':{'root':ROOT,'videos':len(files),'pattern':'*_Captioned_Model.mp4','frames_sampled':8,'decoder':'PyAV '+av.__version__},'results':R},open(OUT,'w'),indent=1)
ok=[r for r in R if 'decode_error' not in r]
print('SCOPE videos',len(files),'decoded fully',len(ok),'decode errors',len(R)-len(ok))
print('duration 30-40 s:',sum(r['duration_ok'] for r in R),'/',len(R),'| outside:',[(r['lesson_id'],round(r['duration_mvhd'],1)) for r in R if not r['duration_ok']][:30])
print('blank frames total',sum(r.get('blank_frames',0) for r in ok),'videos with any blank',sum(1 for r in ok if r.get('blank_frames')),'| outside safe area (videos)',sum(1 for r in ok if r.get('frames_outside_safe')))
print('embedded copy present',sum(1 for r in R if r.get('embedded',{}).get('present')),'identical to file',sum(1 for r in R if r.get('embedded',{}).get('identical_to_file')))
print('codecs',{r.get('codec') for r in ok},'sizes',{tuple(r.get('size',[])) for r in ok},'frames per video min/max',min(r['frames_decoded'] for r in ok),max(r['frames_decoded'] for r in ok))
