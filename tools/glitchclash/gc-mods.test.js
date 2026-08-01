/* Run modifiers: they show, they toggle, they change the numbers, and the
   reward scales with how many are on. */
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
  await pg.click('#scr-title [data-go="home"]'); await pg.waitForTimeout(300);

  console.log('=== the sheet ===');
  await pg.click('#endlessbtn'); await pg.waitForTimeout(400);
  const sheet = await pg.evaluate(()=>({
    shown:!!document.querySelector('#ov-result.show'),
    n:document.querySelectorAll('[data-mod]').length,
    pay:(document.getElementById('modpay')||{}).textContent,
    pressed:[...document.querySelectorAll('[data-mod]')].map(b=>b.getAttribute('aria-pressed')),
    go:!!document.getElementById('modgo') }));
  ok(sheet.shown,'Endless opens the modifier sheet, not the run');
  ok(sheet.n===5,'five modifiers offered',String(sheet.n));
  ok(sheet.go,'a start button is present');
  ok(sheet.pay==='Reward ×1.00','a clean run pays ×1.00',sheet.pay);
  ok(sheet.pressed.every(p=>p==='false'),'all start unchecked, and say so via aria-pressed');

  console.log('\n=== toggling ===');
  await pg.click('[data-mod="brittle"]'); await pg.waitForTimeout(150);
  await pg.click('[data-mod="swift"]');   await pg.waitForTimeout(150);
  const t = await pg.evaluate(()=>({
    pay:document.getElementById('modpay').textContent,
    on:[...document.querySelectorAll('[data-mod][aria-pressed="true"]')].map(b=>b.dataset.mod),
    ticks:[...document.querySelectorAll('[data-mod]')].map(b=>b.querySelector('[data-tick]').textContent) }));
  ok(t.on.length===2,'two modifiers armed',t.on.join(','));
  ok(t.pay==='Reward ×1.70','the payout scales with how many are on',t.pay);
  ok(t.ticks.filter(x=>x==='☑').length===2,'the tick is a character, not a colour',t.ticks.join(''));
  await pg.click('[data-mod="brittle"]'); await pg.waitForTimeout(150);
  const off = await pg.evaluate(()=>document.getElementById('modpay').textContent);
  ok(off==='Reward ×1.35','un-toggling drops the payout back',off);
  await pg.click('[data-mod="brittle"]'); await pg.waitForTimeout(150);

  console.log('\n=== they actually change the numbers ===');
  // baseline: what an unmodified round-1 team and enemy look like
  const base = await pg.evaluate(()=>{
    __GCstart(0,{__scened:true, endless:{round:1,boons:[],mods:[]}});
    const bt=__GC(); return {hp:bt.team[0].maxhp, atk:bt.team[0].atk, eatk:bt.glitch.atk, ehp:bt.glitch.maxhp}; });
  const mod = await pg.evaluate(()=>{
    __GCstart(0,{__scened:true, endless:{round:1,boons:[],mods:['brittle','swift']}});
    const bt=__GC(); return {hp:bt.team[0].maxhp, atk:bt.team[0].atk, eatk:bt.glitch.atk, ehp:bt.glitch.maxhp}; });
  console.log('  clean: '+JSON.stringify(base)+'\n  mods:  '+JSON.stringify(mod));
  ok(mod.hp<base.hp,'Brittle cuts your effective HP',base.hp+' -> '+mod.hp);
  ok(mod.atk>base.atk,'Sudden Death raises your attack',base.atk+' -> '+mod.atk);
  ok(mod.eatk>base.eatk,'…and the enemy\'s too',base.eatk+' -> '+mod.eatk);
  ok(mod.ehp===base.ehp,'neither touches enemy HP at the same round',base.ehp+' vs '+mod.ehp);

  const hard = await pg.evaluate(()=>{
    __GCstart(0,{__scened:true, endless:{round:1,scaleRound:5,boons:[],mods:['hardcore']}});
    const bt=__GC(); return {ehp:bt.glitch.maxhp, chip:document.getElementById('stagechip').textContent}; });
  ok(hard.ehp>base.ehp,'Hardcore starts the escalation at round 5',base.ehp+' -> '+hard.ehp);
  ok(/Hardcore/.test(hard.chip),'live modifiers are named in the stage chip',hard.chip);

  ok(errs.length===0,'no page or script errors',errs.slice(0,3).join(' | '));
  await b.close();
  console.log('\n'+(fail?fail+' FAILED':'RUN MODIFIERS VERIFIED'));
  process.exit(fail?1:0);
})();
