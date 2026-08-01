/* Weekly Gauntlet: deterministic plan, three clashes, paid once a week,
   and it must NOT touch the campaign economy. */
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

  console.log('=== ISO week key ===');
  const wk = await pg.evaluate(()=>({
    now:  localWeekKey(),
    // 2026-01-01 is a Thursday -> ISO week 1 of 2026
    jan1: localWeekKey(new Date(2026,0,1)),
    // 2027-01-01 is a Friday -> still ISO week 53 of 2026
    ny27: localWeekKey(new Date(2027,0,1)),
    // 2026-12-31 is a Thursday -> ISO week 53 of 2026
    dec31:localWeekKey(new Date(2026,11,31)),
    mon:  localWeekKey(new Date(2026,7,3)),   // Mon 3 Aug 2026
    sun:  localWeekKey(new Date(2026,7,9)),   // Sun 9 Aug 2026 - same ISO week
    nxt:  localWeekKey(new Date(2026,7,10)) }));
  console.log('  '+JSON.stringify(wk));
  ok(/^\d{4}-W\d{2}$/.test(wk.now),'shape is YYYY-Www',wk.now);
  ok(wk.jan1==='2026-W01','1 Jan 2026 is week 1',wk.jan1);
  ok(wk.ny27==='2026-W53','1 Jan 2027 still belongs to 2026',wk.ny27);
  ok(wk.dec31===wk.ny27,'the turn of the year does not split a week',wk.dec31+' vs '+wk.ny27);
  ok(wk.mon===wk.sun,'Monday and Sunday share a key',wk.mon+' / '+wk.sun);
  ok(wk.nxt!==wk.sun,'the next Monday rolls over',wk.nxt);

  console.log('\n=== the plan is deterministic and boss-free ===');
  const plan = await pg.evaluate(()=>{
    const a=__GCplan('2026-W31'), b=__GCplan('2026-W31'), c=__GCplan('2026-W32');
    return {a,b,c,bossy:a.stages.filter(i=>__GCglitches()[i].trait==='boss').length,
            modOk:!!__GCmod(a.mod)}; });
  ok(JSON.stringify(plan.a)===JSON.stringify(plan.b),'the same week gives the same gauntlet',
     JSON.stringify(plan.a));
  ok(JSON.stringify(plan.a)!==JSON.stringify(plan.c),'a different week gives a different one',
     JSON.stringify(plan.c));
  ok(plan.a.stages.length===3,'three clashes',String(plan.a.stages.length));
  ok(plan.bossy===0,'no bosses in the gauntlet',String(plan.bossy));
  ok(plan.modOk,'the handicap is a real modifier',plan.a.mod);

  console.log('\n=== playing it ===');
  const before = await pg.evaluate(()=>({xp:__GCsave().xp,wins:(__GCsave().stats||{}).wins||0,
    owned:__GCsave().owned.length,cleared:__GCsave().cleared.length,done:__GCsave().weeklyDone}));
  await pg.click('#weeklybtn'); await pg.waitForTimeout(1200);
  const started = await pg.evaluate(()=>{const bt=__GC();
    return bt&&bt.endless?{round:bt.endless.round,wk:bt.endless.weekly,mods:bt.endless.mods,
      chip:document.getElementById('stagechip').textContent}:null;});
  console.log('  '+JSON.stringify(started));
  ok(started&&started.round===1,'opens on clash 1');
  ok(started&&started.wk,'the battle is flagged weekly',started?String(started.wk):'null');
  ok(started&&started.mods.length===1,'exactly one handicap is applied',
     started?started.mods.join(','):'null');
  ok(started&&/^Weekly · Clash 1 of 3/.test(started.chip),
     'the chip says Weekly, not Endless',started?started.chip:'null');

  // force the three clashes through
  for(let r=0;r<3;r++){
    for(let i=0;i<80;i++){
      const over = await pg.evaluate(()=>{ const bt=__GC(); return !bt||bt.over; });
      if(over) break;
      await pg.evaluate(()=>{ try{ const bt=__GC();
        bt.glitch.hp=1; __GCturn({act:'strike'}); }catch(e){} });
      await pg.waitForTimeout(90);
    }
    await pg.waitForTimeout(700);
  }
  await pg.waitForTimeout(900);
  const after = await pg.evaluate(()=>({xp:__GCsave().xp,wins:(__GCsave().stats||{}).wins||0,
    owned:__GCsave().owned.length,cleared:__GCsave().cleared.length,done:__GCsave().weeklyDone,
    sheet:(document.getElementById('resultsheet')||{}).textContent||''}));
  console.log('  before '+JSON.stringify(before)+'\n  after  '+JSON.stringify({xp:after.xp,wins:after.wins,owned:after.owned,cleared:after.cleared,done:after.done}));
  ok(after.done===wk.now,'the week is marked done',after.done||'(none)');
  ok(/cleared/i.test(after.sheet),'a completion sheet is shown');
  ok(after.xp-before.xp>=60,'the 60 XP bonus is paid',String(after.xp-before.xp));
  ok(after.owned>before.owned,'a card pack is awarded',before.owned+' -> '+after.owned);
  ok(after.cleared===before.cleared,'no campaign stage is ticked off',
     before.cleared+' -> '+after.cleared);
  ok(after.wins-before.wins===3,'three wins counted, not four',
     String(after.wins-before.wins));

  console.log('\n=== the reward is once a week ===');
  const xp2 = await pg.evaluate(()=>__GCsave().xp);
  await pg.click('#ov-result [data-close]'); await pg.waitForTimeout(400);   // back to Home
  await pg.click('#weeklybtn'); await pg.waitForTimeout(1000);
  for(let r=0;r<3;r++){
    for(let i=0;i<80;i++){
      const over = await pg.evaluate(()=>{ const bt=__GC(); return !bt||bt.over; });
      if(over) break;
      await pg.evaluate(()=>{ try{ const bt=__GC(); bt.glitch.hp=1; __GCturn({act:'strike'}); }catch(e){} });
      await pg.waitForTimeout(90);
    }
    await pg.waitForTimeout(700);
  }
  await pg.waitForTimeout(900);
  const second = await pg.evaluate(()=>({xp:__GCsave().xp,owned:__GCsave().owned.length,
    sheet:(document.getElementById('resultsheet')||{}).textContent||''}));
  ok(second.owned===after.owned,'a repeat run pays no second card pack',
     after.owned+' -> '+second.owned);
  // per-clash XP is still paid on a repeat, the same as replaying a campaign
  // stage; it is the 60 bonus and the pack that are once a week.
  ok((after.xp-before.xp)-(second.xp-xp2) === 60,'and the 60 bonus exactly once',
     'first +'+(after.xp-before.xp)+', repeat +'+(second.xp-xp2));
  ok(/practice run/.test(second.sheet),'the sheet says the reward was already collected');

  console.log('\n=== once a week ===');
  const label = await pg.evaluate(()=>document.getElementById('weeklybtn').textContent);
  ok(/done this week/.test(label),'the button says it is done',label);

  ok(errs.length===0,'no page or script errors',errs.slice(0,3).join(' | '));
  await b.close();
  console.log('\n'+(fail?fail+' FAILED':'WEEKLY GAUNTLET VERIFIED'));
  process.exit(fail?1:0);
})();
