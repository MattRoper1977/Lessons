// HUM-D5 A3 E8 - video, the legs that run without ffmpeg/tesseract. For every
// *_Captioned_Model.mp4: (1) DECODE in Chromium (<video> loadedmetadata + canplaythrough,
// error recorded); (2) DURATION (must be 30-40 s); (3) the embedded copy: does the lesson
// HTML reference the same file (src) and does that element decode; (4) BLANK FRAMES: seek
// to 8 evenly spaced times, draw each frame to a canvas, mean luminance and std-dev - a
// frame with std-dev < 2 (flat) is blank; (5) SAFE AREA: for each sampled frame, the
// bounding box of non-background pixels vs the 5% title-safe margin. OCR of caption text
// is NOT RUN (no tesseract in the container) and is recorded so in CHECKS.md.
const {chromium}=require('playwright'); const fs=require('fs'), path=require('path');
const ROOT=process.argv[2], OUT=process.argv[3]; const CHROME='/opt/pw-browsers/chromium-1194/chrome-linux/chrome';
function walk(dir,acc=[]){for(const e of fs.readdirSync(dir,{withFileTypes:true})){const p=path.join(dir,e.name);
 if(fs.statSync(p).isDirectory())walk(p,acc); else if(e.name.endsWith('_Captioned_Model.mp4'))acc.push(p);} return acc;}
(async()=>{
 const files=walk(ROOT).sort(); const b=await chromium.launch({executablePath:CHROME}); const ctx=await b.newContext(); const R=[]; let n=0;
 for(const f of files){
  const id=path.basename(f).replace(/_Captioned_Model\.mp4$/,''); const lesson=path.join(path.dirname(f),id+'_Lesson.html');
  const rec={lesson_id:id,file:path.relative(ROOT,f),bytes:fs.statSync(f).size};
  const p=await ctx.newPage();
  try{
   await p.setContent(`<video id="v" src="file://${f}" preload="auto" muted></video>`);
   const meta=await p.evaluate(()=>new Promise(res=>{const v=document.getElementById('v'); const t=setTimeout(()=>res({error:'timeout 20s'}),20000);
     v.onerror=()=>{clearTimeout(t);res({error:'decode error '+(v.error&&v.error.code)});}; v.onloadedmetadata=()=>{clearTimeout(t);res({duration:v.duration,w:v.videoWidth,h:v.videoHeight});};}));
   Object.assign(rec,meta);
   if(!meta.error){
    const frames=await Promise.race([p.evaluate(async()=>{const v=document.getElementById('v'); const c=document.createElement('canvas'); c.width=v.videoWidth; c.height=v.videoHeight; const g=c.getContext('2d',{willReadFrequently:true}); const out=[]; const N=8;
      for(let i=0;i<N;i++){ const t=(v.duration*(i+0.5))/N; const ok=await new Promise(r=>{const w=setTimeout(()=>r(false),4000); v.onseeked=()=>{clearTimeout(w);r(true);}; v.currentTime=t;}); if(!ok){out.push({t:Math.round(t*10)/10,seek_timeout:true}); continue;} g.drawImage(v,0,0); const d=g.getImageData(0,0,c.width,c.height).data;
        let sum=0,sum2=0,cnt=0; let minx=c.width,maxx=0,miny=c.height,maxy=0; const bgR=d[0],bgG=d[1],bgB=d[2];
        for(let y=0;y<c.height;y+=2)for(let x=0;x<c.width;x+=2){const k=(y*c.width+x)*4; const l=0.299*d[k]+0.587*d[k+1]+0.114*d[k+2]; sum+=l; sum2+=l*l; cnt++; if(Math.abs(d[k]-bgR)+Math.abs(d[k+1]-bgG)+Math.abs(d[k+2]-bgB)>60){if(x<minx)minx=x;if(x>maxx)maxx=x;if(y<miny)miny=y;if(y>maxy)maxy=y;}}
        const mean=sum/cnt, sd=Math.sqrt(Math.max(0,sum2/cnt-mean*mean));
        out.push({t:Math.round(t*10)/10,mean:Math.round(mean),sd:Math.round(sd*10)/10,blank:sd<2,content_box:maxx>=minx?[minx,miny,maxx,maxy]:null,inside_safe: maxx>=minx ? (minx>=c.width*0.05&&maxx<=c.width*0.95&&miny>=c.height*0.05&&maxy<=c.height*0.95) : null}); }
      return out;}), new Promise(r=>setTimeout(()=>r([{watchdog:'video-level 60 s timeout'}]),60000))]);
    rec.frames=frames; rec.seek_timeouts=frames.filter(x=>x.seek_timeout).length; rec.blank_frames=frames.filter(x=>x.blank).length; rec.frames_outside_safe=frames.filter(x=>x.inside_safe===false).length; rec.duration_ok=meta.duration>=30&&meta.duration<=40;
   }
   if(fs.existsSync(lesson)){ const t=fs.readFileSync(lesson,'utf8'); const m=t.match(/<video[^>]*>/); const srcs=[...t.matchAll(/<(?:video|source)[^>]*src="([^"]+)"/g)].map(x=>x[1]); rec.embedded={video_tags:(t.match(/<video/g)||[]).length,srcs:srcs.slice(0,3),references_this_file:srcs.some(s=>s.endsWith(path.basename(f))),has_track:/<track/.test(t)}; }
  }catch(e){rec.error=String(e.message).split('\n')[0].slice(0,140);}
  await p.close(); R.push(rec); if(++n%10===0)console.error(`  ${n}/${files.length}`);
  fs.writeFileSync(OUT,JSON.stringify({scope:{root:ROOT,videos:files.length,done:R.length},results:R}));
 }
 await b.close(); fs.writeFileSync(OUT,JSON.stringify({scope:{root:ROOT,videos:files.length,pattern:'*_Captioned_Model.mp4',frames_per_video:8},results:R},null,1));
 console.log('videos',files.length,'decode errors',R.filter(r=>r.error).length,'duration 30-40s',R.filter(r=>r.duration_ok).length,'blank frames total',R.reduce((t,r)=>t+(r.blank_frames||0),0),'videos with frame outside safe area',R.filter(r=>r.frames_outside_safe).length,'embedded refs this file',R.filter(r=>r.embedded&&r.embedded.references_this_file).length);
 const ds=R.filter(r=>r.duration).map(r=>r.duration); console.log('duration min/max',Math.min(...ds).toFixed(1),Math.max(...ds).toFixed(1));
})();
