/* Time Attack: a RUN clock, never a turn clock. */
const { chromium } = require('playwright');
const path = require('path');
/* The file under test: an argument, so this runs against a working tree, a
   checkout or a release copy. Defaults to the game in this repo. */
const TARGET = 'file://' + (process.argv[2]
  ? path.resolve(process.argv[2])
  : path.resolve(__dirname, '..', '..', 'Games', 'Glitch_Clash.html'));
(async()=>{
  const b=await chromium.launch({executablePath: process.env.CHROMIUM_PATH || undefined,
    args:['--use-gl=swiftshader','--enable-unsafe-swiftshader','--no-sandbox']});
  const pg=await (await b.newContext({viewport:{width:412,height:892}})).newPage();
  const errs=[]; pg.on('pageerror',e=>errs.push('PAGEERR '+e.message));
  pg.on('console',m=>{ if(m.type()==='error'&&!/Failed to load|ERR_/.test(m.text())) errs.push('CONSOLE '+m.text()); });
  await pg.goto(TARGET);
  await pg.waitForTimeout(1300);
  let fail=0; const ok=(c,l,d)=>{c?console.log('  PASS  '+l+(d?'   '+d:'')):(fail++,console.log('  FAIL  '+l+(d?'   '+d:'')));};
  const chip=()=>pg.evaluate(()=>{const c=document.getElementById('clockchip');
    return {hidden:c.hidden,txt:c.textContent,label:c.getAttribute('aria-label')};});
  await pg.click('#scr-title [data-go="home"]'); await pg.waitForTimeout(300);

  console.log('=== off by default ===');
  await pg.click('#endlessbtn'); await pg.waitForTimeout(400);
  const listed = await pg.evaluate(()=>[...document.querySelectorAll('[data-mod]')].map(b=>b.dataset.mod));
  ok(listed.includes('clock'),'Time Attack is offered',listed.join(','));
  await pg.click('#modgo'); await pg.waitForTimeout(1200);
  ok((await chip()).hidden,'a clean run shows no clock');
  await pg.click('#quitbtn'); await pg.waitForTimeout(150);
  await pg.click('#quitbtn'); await pg.waitForTimeout(500);

  console.log('\n=== armed ===');
  await pg.click('#endlessbtn'); await pg.waitForTimeout(400);
  await pg.click('[data-mod="clock"]'); await pg.waitForTimeout(150);
  await pg.click('#modgo'); await pg.waitForTimeout(1400);
  const c0=await chip();
  console.log('  '+JSON.stringify(c0));
  ok(!c0.hidden,'the clock is shown');
  ok(/^⏱ 1:(2[6-9]|30)$/.test(c0.txt),'it starts near 1:30 and is already counting',c0.txt);
  ok(/seconds remaining/.test(c0.label||''),'it is spoken, not just drawn',c0.label);

  console.log('\n=== it never interrupts a turn ===');
  const mid = await pg.evaluate(async ()=>{
    const before=__GC().glitch.hp;
    __GCturn({act:'strike'});
    await new Promise(r=>setTimeout(r,300));
    return {before, after:__GC().glitch.hp, over:__GC().over};
  });
  ok(mid.after<mid.before,'a turn still resolves normally with the clock live',
     mid.before+' -> '+mid.after);

  console.log('\n=== a sheet pauses it ===');
  const t1 = await pg.evaluate(()=>(__GCclock()||{left:0}).left);
  await pg.evaluate(()=>__GCov('settings'));
  await pg.waitForTimeout(1400);
  const t2 = await pg.evaluate(()=>(__GCclock()||{left:0}).left);
  ok(Math.abs(t2-t1)<400,'time does not run down while a sheet is open',
     Math.round(t1)+' -> '+Math.round(t2)+' ms');
  await pg.evaluate(()=>__GCclose()); await pg.waitForTimeout(900);
  const t3 = await pg.evaluate(()=>(__GCclock()||{left:0}).left);
  ok(t3 < t2-400,'and it resumes when the sheet closes',Math.round(t2)+' -> '+Math.round(t3));

  console.log('\n=== clearing a round adds time ===');
  const before = await pg.evaluate(()=>(__GCclock()||{left:0}).left);
  await pg.evaluate(async ()=>{ for(let i=0;i<40;i++){ const bt=__GC();
    if(!bt||bt.over) break; bt.glitch.hp=1; __GCturn({act:'strike'});
    await new Promise(r=>setTimeout(r,80)); } });
  await pg.waitForTimeout(1500);
  const after = await pg.evaluate(()=>(__GCclock()||{left:0}).left);
  console.log('  '+Math.round(before)+' -> '+Math.round(after)+' ms');
  ok(after > before,'a cleared round tops the clock up',
     Math.round(before/1000)+'s -> '+Math.round(after/1000)+'s');
  ok(after-before > 20000,'by roughly the advertised 30 seconds',
     Math.round((after-before)/1000)+'s');

  console.log('\n=== running out ends the run ===');
  const cleared = await pg.evaluate(()=>__GCrun()?__GCrun().round-1:0);
  await pg.evaluate(()=>__GCclockSet(600));
  await pg.waitForTimeout(1600);
  const end = await pg.evaluate(()=>({
    sheet:(document.getElementById('resultsheet')||{}).textContent||'',
    run:!!__GCrun(), clock:!!__GCclock(), battle:!!__GC(),
    best:(__GCsave().stats||{}).bestEndless||0 }));
  console.log('  '+JSON.stringify({...end,sheet:end.sheet.slice(0,60)}));
  ok(/Time up/.test(end.sheet),'a Time up sheet is shown');
  ok(!end.run && !end.clock,'the run and the clock are both torn down');
  ok(end.best>=cleared,'the rounds cleared are banked',end.best+' >= '+cleared);
  ok((await chip()).hidden,'the chip is hidden again');

  ok(errs.length===0,'no page or script errors',errs.slice(0,3).join(' | '));
  await b.close();
  console.log('\n'+(fail?fail+' FAILED':'TIME ATTACK VERIFIED'));
  process.exit(fail?1:0);
})();
