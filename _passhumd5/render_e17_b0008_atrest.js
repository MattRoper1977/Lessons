// HUM-D5 B0008 re-measure with the corrected instrument (correction #12):
// getBoundingClientRect is scaled by .slide.active's 450 ms fadeIn transform, so
// heights are read as offsetHeight AND as rect after a 700 ms settle, per stage,
// for every <button> and <a>, <input>, <select>, <summary> that is visible on
// that stage. Scope printed. Output: E17_B0008_ATREST.json
const {chromium}=require('playwright');const fs=require('fs'),path=require('path');
const ROOT='/tmp/claude-0/humd5/unzipped', OUT='/tmp/claude-0/humd5/E17_B0008_ATREST.json';
const CHROME='/opt/pw-browsers/chromium-1194/chrome-linux/chrome';
function lessons(d,a=[]){for(const e of fs.readdirSync(d,{withFileTypes:true})){const p=path.join(d,e.name);if(e.isDirectory())lessons(p,a);else if(e.name.endsWith('_Lesson.html'))a.push(p);}return a;}
const MEASURE=()=>{const out=[];const active=document.querySelector('section[id^="slide-"].active');
 for(const el of document.querySelectorAll('button,a,input,select,summary,textarea')){
  if(!el.checkVisibility({checkOpacity:true,checkVisibilityCSS:true}))continue;
  const r=el.getBoundingClientRect(); if(!(r.width>0&&r.height>0))continue;
  out.push({stage:active?active.id:null,tag:el.tagName.toLowerCase(),id:el.id||null,cls:(el.className&&el.className.baseVal!==undefined?el.className.baseVal:el.className)||'',offsetH:el.offsetHeight,rectH:+r.height.toFixed(3),rectW:+r.width.toFixed(1)});
 } return out;};
(async()=>{const files=lessons(ROOT).sort();console.log('SCOPE root='+ROOT+' pattern=*_Lesson.html lessons='+files.length+' viewport=390x844 DPR3 mobile settle=700ms');
 const b=await chromium.launch({executablePath:CHROME});const res=[];
 for(const f of files){const id=path.basename(f).replace(/_Lesson\.html$/,'');const ctx=await b.newContext({viewport:{width:390,height:844},deviceScaleFactor:3,isMobile:true,hasTouch:true});const p=await ctx.newPage();
  try{await p.goto('file://'+f,{waitUntil:'load',timeout:45000});await p.waitForTimeout(700);
   const n=await p.evaluate(()=>document.querySelectorAll('section[id^="slide-"]').length);const rows=[];const seen=new Set();
   for(let i=0;i<n;i++){if(i>0){const nx=await p.$('#next-slide');if(!nx)break;await nx.click();await p.waitForTimeout(700);}
    const m=await p.evaluate(MEASURE);const st=m[0]?m[0].stage:null;if(st&&seen.has(st))break;if(st)seen.add(st);rows.push(...m);}
   const under=rows.filter(r=>r.offsetH<44||r.rectH<44);
   res.push({lesson_id:id,rows:rows.length,under44:under.length,under44_rows:under.slice(0,40),min_button_offsetH:Math.min(...rows.filter(r=>r.tag==='button').map(r=>r.offsetH)),min_button_rectH:Math.min(...rows.filter(r=>r.tag==='button').map(r=>r.rectH))});
   console.log(id,'rows',rows.length,'under44',under.length,'minBtn',res[res.length-1].min_button_offsetH,res[res.length-1].min_button_rectH);
  }catch(e){res.push({lesson_id:id,error:String(e.message).slice(0,200)});console.log(id,'ERROR',e.message.slice(0,120));}
  await ctx.close();}
 await b.close();fs.writeFileSync(OUT,JSON.stringify({scope:{root:ROOT,pattern:'*_Lesson.html',lessons:files.length,viewport:'390x844 DPR3 mobile',settle_ms:700,instrument:'offsetHeight and rect after settle (correction #12)'},results:res},null,1));console.log('WROTE',OUT);})();
