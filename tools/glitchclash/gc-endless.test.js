/* Plays a full Endless run through the shipped UI until the boon picker
   appears, then picks a boon and confirms it reaches the next battle. */
const { chromium } = require('playwright');
const path = require('path');
/* The file under test: an argument, so this runs against a working tree, a
   checkout or a release copy. Defaults to the game in this repo. */
const TARGET = 'file://' + (process.argv[2]
  ? path.resolve(process.argv[2])
  : path.resolve(__dirname, '..', '..', 'Games', 'Glitch_Clash.html'));
(async () => {
  const b = await chromium.launch({ executablePath: process.env.CHROMIUM_PATH || undefined,
    args:['--use-gl=swiftshader','--enable-unsafe-swiftshader','--no-sandbox'] });
  const pg = await (await b.newContext({viewport:{width:412,height:892}})).newPage();
  const errs=[]; pg.on('pageerror',e=>errs.push('PAGEERR '+e.message));
  pg.on('console',m=>{ if(m.type()==='error'&&!/Failed to load|ERR_/.test(m.text())) errs.push('CONSOLE '+m.text()); });
  await pg.goto(TARGET);
  await pg.waitForTimeout(1500);
  let fail=0; const ok=(c,l,d)=>{c?console.log('  PASS  '+l+(d?'   '+d:'')):(fail++,console.log('  FAIL  '+l+(d?'   '+d:'')));};

  const st = ()=>pg.evaluate(()=>{ const bt=window.__GC?window.__GC():null;
    return { round: bt&&bt.endless&&bt.endless.round, over: bt&&bt.over,
             boonSheet: !!document.querySelector('#ov-result.show [data-boon]'),
             inBattle: !!document.querySelector('#scr-battle.active'),
             boons: bt&&bt.endless&&bt.endless.boons ? bt.endless.boons.slice() : null }; });

  await pg.click('#scr-title [data-go="home"]'); await pg.waitForTimeout(400);   // ▶ Play
  await pg.click('#endlessbtn'); await pg.waitForTimeout(400);
  await pg.click('#modgo');                              // clean run, no modifiers
  await pg.waitForTimeout(1600);
  console.log('=== endless run ===');
  let s = await st();
  ok(s.round===1,'run opens on round 1',String(s.round));

  /* Wins are forced by dropping the enemy to 1 HP before each strike.
     This suite is about the RUN MACHINERY — the round chain, the picker, the
     boon carrying forward — not about whether random play happens to win. An
     earlier version hammered strike and hoped; it failed roughly one run in
     three when the dice went the other way, which is useless as a gate. */
  let seenRounds=new Set([1]), sawBoon=false, maxRound=1, turns=0;
  for(let i=0;i<120 && !sawBoon;i++){
    /* Only act on a LIVE battle. Driving a turn into a finished one is
       something no player can do — the action bar is behind the result
       overlay — and it stampedes the run into the next round before the boon
       sheet can be read. */
    const acted = await pg.evaluate(()=>{ try{ const bt=__GC();
      if(!bt || bt.over) return false;
      bt.glitch.hp=1; __GCturn({act:'strike'}); return true; }catch(e){ return false; } });
    await pg.waitForTimeout(acted?140:200); turns++;
    const q = await st();
    if(q.boonSheet){ sawBoon=true; break; }
    if(q.round){ seenRounds.add(q.round); maxRound=Math.max(maxRound,q.round); }
  }
  console.log('  turns driven: '+turns+'   rounds seen: '+[...seenRounds].sort((a,b)=>a-b).join(','));
  ok(maxRound>=2 || sawBoon,'the run advanced past round 1','max round '+maxRound);
  ok(sawBoon,'boon picker appears after a cleared third round');

  if(sawBoon){
    /* The loop detects the sheet the moment its markup exists, which can be
       mid open-transition. Wait for a button that is actually visible before
       clicking one, or the click races the animation and times out. */
    await pg.waitForSelector('#ov-result [data-boon]', {state:'visible', timeout:5000});
    await pg.waitForTimeout(250);
    const offer = await pg.evaluate(()=>[...document.querySelectorAll('#ov-result [data-boon]')]
      .map(b=>b.dataset.boon));
    console.log('  offered: '+offer.join(', '));
    ok(offer.length===3,'three boons offered',String(offer.length));
    ok(new Set(offer).size===3,'boons offered are distinct');
    const skip = await pg.evaluate(()=>!!document.querySelector('#ov-result [data-close]'));
    ok(skip,'the picker can be skipped');
    await pg.click('#ov-result [data-boon]');
    await pg.waitForTimeout(1400);
    const after = await st();
    console.log('  after pick: '+JSON.stringify(after));
    ok(after.inBattle,'picking a boon starts the next battle');
    ok(after.boons && after.boons.length===1,'the boon is carried into the run',
       after.boons?after.boons.join(','):'null');
    const applied = await pg.evaluate(()=>{ const bt=window.__GC?window.__GC():null;
      return bt ? {round:bt.endless.round, ehp:bt.enemy&&bt.enemy.maxhp} : null; });
    console.log('  next battle: '+JSON.stringify(applied));
    ok(applied && applied.round>=4,'the run continues past the pick',applied?String(applied.round):'null');
  }
  const sv = await pg.evaluate(()=>{ try{ return JSON.parse(localStorage.getItem('glitchclash_save')||'{}').stats||{}; }catch(e){ return {}; } });
  console.log('  saved: bestEndless='+(sv.bestEndless||0)+'  wins='+(sv.wins||0));
  ok((sv.bestEndless||0)>=1,'best endless round is banked',String(sv.bestEndless||0));
  ok((sv.wins||0)>=1,'cleared endless rounds count as wins (they feed theme unlocks)',String(sv.wins||0));

  ok(errs.length===0,'no page or script errors',errs.slice(0,3).join(' | '));
  await pg.screenshot({path:'gc-endless.png'});
  await b.close();
  console.log('\n'+(fail?fail+' FAILED':'ENDLESS RUN VERIFIED'));
  process.exit(fail?1:0);
})();
