// SCA-1 §1.3 baseline: node --check on every inline script + headless boot at 3 viewports.
import fs from 'fs'; import path from 'path'; import vm from 'vm';
import { chromium } from 'playwright';
const ROOT='/home/user/Lessons/Science_Teesside';
const OUT=process.argv[2]||'/home/user/Lessons/_sca1/baseline';
fs.mkdirSync(OUT,{recursive:true});
const files=[];
for(const p of ['Build','Grow','Launch']){
  const d=path.join(ROOT,p,'v3_40min');
  for(const f of fs.readdirSync(d).sort()) if(f.endsWith('.html')) files.push(path.join(d,f));
}
// ---- node --check equivalent on inline scripts
const syn=[];
for(const f of files){
  const t=fs.readFileSync(f,'utf8');
  const re=/<script\b([^>]*)>([\s\S]*?)<\/script>/gi; let m,i=0;
  while((m=re.exec(t))){
    i++;
    if(/\bsrc=/i.test(m[1])) continue;
    if(/type\s*=\s*["'](?!text\/javascript|application\/javascript)/i.test(m[1])) continue;
    try{ new vm.Script(m[2],{filename:`${path.basename(f)}#${i}`}); syn.push({file:path.basename(f),idx:i,ok:true}); }
    catch(e){ syn.push({file:path.basename(f),idx:i,ok:false,err:String(e.message)}); }
  }
}
fs.writeFileSync(path.join(OUT,'syntax.json'),JSON.stringify(syn,null,1));
const bad=syn.filter(s=>!s.ok);
console.log(`node --check: ${syn.length} inline scripts, ${bad.length} FAILED`);
bad.forEach(b=>console.log(`  FAIL ${b.file}#${b.idx}: ${b.err}`));
// ---- headless boot at 3 viewports
const VPS=[{w:390,h:844},{w:768,h:1024},{w:1440,h:900}];
const browser=await chromium.launch();
const jobs=[]; for(const f of files) for(const vp of VPS) jobs.push({f,vp});
const boot=[]; const CONC=8;
async function worker(){
  while(jobs.length){
    const {f,vp}=jobs.shift();
    const ctx=await browser.newContext({viewport:{width:vp.w,height:vp.h}});
    const pg=await ctx.newPage(); const errs=[];
    pg.on('console',m=>{if(m.type()==='error')errs.push(m.text().slice(0,300));});
    pg.on('pageerror',e=>errs.push('PAGEERROR: '+String(e.message).slice(0,300)));
    try{ await pg.goto('file://'+f,{waitUntil:'load',timeout:30000}); await pg.waitForTimeout(600); }
    catch(e){ errs.push('NAV: '+String(e.message).slice(0,200)); }
    boot.push({file:path.basename(f),vp:`${vp.w}x${vp.h}`,errors:errs});
    await ctx.close();
  }
}
await Promise.all(Array.from({length:CONC},worker));
boot.sort((a,b)=>a.file.localeCompare(b.file)||a.vp.localeCompare(b.vp));
await browser.close();
fs.writeFileSync(path.join(OUT,'boot.json'),JSON.stringify(boot,null,1));
const withErr=boot.filter(b=>b.errors.length);
console.log(`boot: ${boot.length} (file x viewport) runs, ${withErr.length} with console errors`);
const agg={};
withErr.forEach(b=>b.errors.forEach(e=>{agg[e]=(agg[e]||0)+1;}));
Object.entries(agg).sort((a,b)=>b[1]-a[1]).slice(0,15).forEach(([e,n])=>console.log(`  x${n} ${e}`));
