/* Boots Glitch Clash, plays a battle, and checks the extras layer. */
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
  await pg.waitForTimeout(1800);
  let fail=0; const ok=(c,l,d)=>{c?console.log('  PASS  '+l+(d?'   '+d:'')):(fail++,console.log('  FAIL  '+l+(d?'   '+d:'')));};

  console.log('=== module ===');
  const api = await pg.evaluate(()=>typeof GCX==='object' ? Object.keys(GCX) : null);
  ok(!!api,'GCX module loaded', api?api.length+' exports':'MISSING');
  const spark = await pg.evaluate(()=>!!document.getElementById('gcx-spark'));
  ok(spark,'spark canvas installed');
  const achN = await pg.evaluate(()=>GCX.ACH.length);
  ok(achN===10,'10 achievements defined',String(achN));
  const gN = await pg.evaluate(()=>GCX.GLITCH_FX.length);
  ok(gN===7,'7 reality glitches defined',String(gN));

  console.log('\n=== audio ===');
  const aud = await pg.evaluate(()=>{ const before=GCX.isMuted();
    GCX.setMuted(!before); const after=GCX.isMuted(); GCX.setMuted(before);
    return {before,after,sfx:Object.keys(GCX.sfx).length}; });
  ok(aud.before!==aud.after,'mute toggles');
  ok(aud.sfx>=12,'sound effects defined',String(aud.sfx)+' cues');

  console.log('\n=== glitch is cosmetic only ===');
  const g = await pg.evaluate(()=>{
    const r=GCX.glitch(); const cls=[...document.body.classList].filter(c=>c.startsWith('gcx-'));
    return {fired:!!r,name:r&&r.name,cls}; });
  ok(g.fired,'a reality glitch fires',g.name);
  ok(g.cls.length>0,'body carries the glitch class',g.cls.join(','));
  const banner = await pg.evaluate(()=>!!document.querySelector('.gcx-sys .gcx-err'));
  ok(banner,'SYSTEM ERROR banner shown');

  console.log('\n=== calm mode suppresses distortion ===');
  const calm = await pg.evaluate(()=>{ document.body.classList.add('calm');
    const r=GCX.glitch(); document.body.classList.remove('calm'); return r; });
  ok(calm===null,'Calm Mode blocks reality glitches entirely');

  console.log('\n=== combo ===');
  const cmb = await pg.evaluate(()=>{ GCX.breakCombo();
    const a=GCX.combo(),b2=GCX.combo(),c=GCX.combo(); GCX.breakCombo();
    return {a,b:b2,c,after:GCX.comboNow()}; });
  ok(cmb.a===1&&cmb.b===2&&cmb.c===3,'combo counts up',JSON.stringify(cmb));
  ok(cmb.after===0,'taking a hit breaks the chain');

  console.log('\n=== play a real battle ===');
  const started = await pg.evaluate(()=>{ try{ __GCstart(0,{__scened:true}); return 'stage 1'; }catch(e){ return 'ERR '+e.message; } });
  await pg.waitForTimeout(1000);
  const inBattle = await pg.evaluate(()=>!!document.querySelector('#ef .card'));
  console.log('  entered via: '+started);
  ok(inBattle,'battle screen reached');
  if(inBattle){
    // charge builds energy, strike spends it — alternate so strikes actually land
    const seq=['charge','strike','charge','strike','charge','strike','strike','strike'];
    for(const cmd of seq){
      await pg.evaluate(c=>{ try{ __GCturn({act:c}); }catch(e){} }, cmd);
      await pg.waitForTimeout(700);
    }
    const logTxt = await pg.evaluate(()=>{const l=document.querySelector('#log')||document.querySelector('.log');
      return l?l.textContent.replace(/\s+/g,' ').slice(-320):'(no log)';});
    console.log('  log tail: '+logTxt);
    const st = await pg.evaluate(()=>{ const b=window.__GC?window.__GC():null;
      return b?{dealt:b.dmgDealt||0,best:b.bestCombo||0,glitches:b.glitchCount||0,
                started:!!b.startedAt,over:!!b.over}:null; });
    console.log('  battle telemetry: '+JSON.stringify(st));
    ok(st&&st.dealt>0,'damage dealt is tracked',st?String(st.dealt):'null');
    ok(st&&st.best>=1,'combo chain recorded',st?String(st.best):'null');
    ok(st&&st.started,'battle start timestamped');
    const sv = await pg.evaluate(()=>{ try{ return JSON.parse(localStorage.getItem('glitchclash_save')||'{}'); }catch(e){ return {}; } });
    console.log('  saved stats: '+JSON.stringify(sv.stats||{}));
  }
  await pg.screenshot({path:'gc-battle.png'});


  console.log('\n=== endless mode + boons ===');
  const gcx2 = await pg.evaluate(()=> typeof GCX2==='object' ? Object.keys(GCX2) : null);
  ok(!!gcx2,'GCX2 module loaded', gcx2?gcx2.length+' exports':'MISSING');
  const btn = await pg.evaluate(()=>{const b=document.getElementById('endlessbtn');
    return b?{txt:b.textContent.trim(),vis:!!b.offsetParent||true}:null;});
  ok(!!btn,'Endless button present on Home', btn?btn.txt:'MISSING');
  const scale = await pg.evaluate(()=>{
    const base={hp:100,atk:20,def:10};
    return {r1:GCX2.scaleGlitch(base,1), r5:GCX2.scaleGlitch(base,5)};});
  ok(scale.r1.hp===100 && scale.r5.hp>scale.r1.hp,'round 1 is unscaled, later rounds escalate',
     'r1 hp '+scale.r1.hp+' -> r5 hp '+scale.r5.hp);
  const boonMath = await pg.evaluate(()=>{
    const f={atk:20,def:10,maxhp:100,hp:100,en:0};
    GCX2.applyBoons([f],['edge','vital']);
    return f;});
  ok(boonMath.atk===23 && boonMath.maxhp===120,'boons change the numbers, not the rules',
     JSON.stringify(boonMath));

  // drive a real endless round through the shipped button
  const runStart = await pg.evaluate(()=>{ try{
      document.getElementById('endlessbtn').click(); return 'clicked'; }catch(e){ return 'ERR '+e.message; } });
  await pg.waitForTimeout(400);
  ok(await pg.evaluate(()=>!!document.getElementById('modgo')),'Endless offers run modifiers first');
  await pg.click('#modgo');                              // start a clean run
  await pg.waitForTimeout(1200);
  const inEndless = await pg.evaluate(()=>{ const b=window.__GC?window.__GC():null;
    return b?{endless:!!b.endless, round:b.endless&&b.endless.round}:null; });
  console.log('  start: '+runStart+'  state: '+JSON.stringify(inEndless));
  ok(inEndless&&inEndless.endless,'Endless button starts a flagged endless battle');
  ok(inEndless&&inEndless.round===1,'first endless battle is round 1', inEndless?String(inEndless.round):'null');

  console.log('\n=== siphon boon actually heals ===');
  const siphon = await pg.evaluate(async ()=>{
    __GCstart(0,{__scened:true});
    const bt=__GC();
    const p=bt.team[bt.active];
    p.siphon=8; p.hp=Math.max(1,p.maxhp-40);
    const before=p.hp;
    __GCturn({act:'guard'});
    return {before, after:__GC().team[0].hp, max:p.maxhp};
  });
  ok(siphon.after>siphon.before,'Siphon tops the Keeper up on its turn',
     siphon.before+' -> '+siphon.after+' / '+siphon.max);
  await pg.evaluate(()=>{ document.querySelectorAll('.overlay.show').forEach(o=>o.classList.remove('show')); });

  console.log('\n=== themes ===');
  const themeCount = await pg.evaluate(()=>GCX2.THEMES.length);
  ok(themeCount===5,'5 themes defined',String(themeCount));
  // leave the endless battle the way a player would, then open the sheet
  await pg.evaluate(()=>{ document.querySelectorAll('.overlay.show').forEach(o=>o.classList.remove('show')); });
  await pg.click('#quitbtn'); await pg.waitForTimeout(150);
  await pg.click('#quitbtn'); await pg.waitForTimeout(400);
  const home = await pg.evaluate(()=>!!document.querySelector('#scr-home.active'));
  ok(home,'quitting an endless run returns to Home');
  await pg.click('[data-open="themes"]');            // the shipped button, not an internal
  await pg.waitForTimeout(250);
  const sheet = await pg.evaluate(()=>{
    const shown=!!document.querySelector('#ov-themes.show');
    const n=document.querySelectorAll('#themelist [data-theme]').length;
    const locked=document.querySelectorAll('#themelist [data-theme][disabled]').length;
    return {shown,n,locked}; });
  ok(sheet.shown,'Arena Themes button opens the sheet');
  ok(sheet.n===5,'theme sheet renders every theme',sheet.n+' rows, '+sheet.locked+' locked');
  ok(sheet.locked>0,'themes start locked behind wins',String(sheet.locked));
  const painted = await pg.evaluate(()=>{ GCX2.applyTheme('amber');
    const bg=document.documentElement.style.getPropertyValue('--bg');
    GCX2.applyTheme('default');
    const cleared=document.documentElement.style.getPropertyValue('--bg');
    return {bg,cleared}; });
  ok(painted.bg==='#150f08','applying a theme repaints --bg',painted.bg);
  ok(painted.cleared==='','switching back to Signal clears the override','"'+painted.cleared+'"');
  const idColours = await pg.evaluate(()=>{ GCX2.applyTheme('mono');
    const keep=['--ring','--emm','--star','--bastion'].map(v=>document.documentElement.style.getPropertyValue(v));
    GCX2.applyTheme('default'); return keep; });
  ok(idColours.every(v=>v===''),'Keeper identity colours are never repainted',JSON.stringify(idColours));
  const hc = await pg.evaluate(()=>{ document.body.classList.add('hc');
    GCX2.applyTheme('amber');
    const during=document.documentElement.style.getPropertyValue('--bg');
    document.body.classList.remove('hc');
    GCX2.applyTheme('amber');
    const after=document.documentElement.style.getPropertyValue('--bg');
    GCX2.applyTheme('default');
    return {during,after}; });
  ok(hc.during==='','High Contrast overrides the theme','"'+hc.during+'"');
  ok(hc.after==='#150f08','theme returns when High Contrast is switched off',hc.after);
  const persist = await pg.evaluate(()=>{ GCX2.applyTheme('viridian');
    const a=localStorage.getItem('gc_theme'); const b=GCX2.currentTheme();
    GCX2.applyTheme('default'); return {a,b}; });
  ok(persist.a==='viridian'&&persist.b==='viridian','theme choice persists',JSON.stringify(persist));

  ok(errs.length===0,'no page or script errors',errs.slice(0,3).join(' | '));
  await b.close();
  console.log('\n'+(fail?fail+' FAILED':'ALL GLITCH CLASH CHECKS PASSED'));
  process.exit(fail?1:0);
})();
