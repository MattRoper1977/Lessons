const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const path=require('path');
const DIR='/home/user/Lessons/Science_Teesside/Launch/v3_40min';
(async () => {
  const files=process.argv.slice(2);
  const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
    args:['--no-sandbox','--disable-dev-shm-usage']});
  let bad=0;
  for(const f of files){
    const full=path.isAbsolute(f)?f:path.join(DIR,f);
    const ctx=await b.newContext(); const p=await ctx.newPage();
    const errs=[];
    p.on('console',m=>{if(m.type()==='error')errs.push('console: '+m.text())});
    p.on('pageerror',e=>errs.push('pageerror: '+e.message));
    p.on('requestfailed',r=>{if(!/favicon|thenational\.academy/.test(r.url()))errs.push('reqfail: '+r.url())});
    await p.goto('file://'+full,{waitUntil:'load'});
    await p.waitForTimeout(400);
    const probe=await p.evaluate(()=>{
      const out={did:[],fail:[],contrast:[]};
      try{
        const c=document.querySelector('.lc-opt'); if(c){c.click();out.did.push('commit')}
        const w=document.querySelector('.lw-btn'); if(w){w.click();w.click();out.did.push('wordhelp')}
        const t=document.querySelector('.tierbtn'); if(t){t.click();out.did.push('tier')}
        const s=document.querySelector('.lspeak'); if(s&&!s.hidden){s.click();out.did.push('speak')}
        // contrast by computed style on every grafted control
        document.querySelectorAll('.lc-opt,.lw-btn,.lspeak').forEach(el=>{
          const cs=getComputedStyle(el);
          if(cs.color===cs.backgroundColor) out.contrast.push((el.textContent||'').trim().slice(0,18));
          if(cs.color==='rgb(255, 255, 255)'&&/255, 255, 255|246, 243|236, 230/.test(cs.backgroundColor))
            out.contrast.push('white-on-light: '+(el.textContent||'').trim().slice(0,18));
        });
      }catch(e){out.fail.push(String(e))}
      return out;
    });
    await p.waitForTimeout(150);
    if(probe.fail.length) errs.push('probe threw: '+probe.fail.join('; '));
    if(probe.contrast.length) errs.push('CONTRAST: '+probe.contrast.join(', '));
    const nm=path.basename(full);
    if(errs.length){bad++;console.log('FAIL  '+nm);errs.slice(0,5).forEach(e=>console.log('        '+e))}
    else console.log('ok    '+nm+'   [driven: '+probe.did.join(',')+']');
    await ctx.close();
  }
  await b.close();
  console.log(bad?('\nBOOT FAIL — '+bad+' of '+files.length):('\nBOOT PASS — '+files.length+'/'+files.length+' surfaces, zero console/page errors, contrast probed by computed style'));
  process.exit(bad?1:0);
})();
