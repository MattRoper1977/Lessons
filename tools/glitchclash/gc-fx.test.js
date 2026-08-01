/* Proves whether the FX particle canvas is actually running. */
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
  await pg.goto(TARGET);
  await pg.waitForTimeout(1300);
  let fail=0; const ok=(c,l,d)=>{c?console.log('  PASS  '+l+(d?'   '+d:'')):(fail++,console.log('  FAIL  '+l+(d?'   '+d:'')));};

  const el = await pg.evaluate(()=>{const c=document.getElementById('fxcanvas');
    return c?{w:c.width,h:c.height,sw:c.style.width}:null;});
  console.log('  #fxcanvas: '+JSON.stringify(el));
  ok(!!el,'the canvas element exists');
  // 300x150 with no style width is the browser default: init() never touched it
  const expect = await pg.evaluate(()=>Math.round(innerWidth*Math.min(2,devicePixelRatio||1)));
  ok(el && el.w===expect && !!el.sw,'init() sized the canvas to the viewport — i.e. it ran',
     el?('width='+el.w+' (expected '+expect+') styleWidth="'+(el.sw||'')+'"'):'null');

  // does a strike actually paint anything?
  await pg.click('#scr-title [data-go="home"]'); await pg.waitForTimeout(250);
  await pg.evaluate(()=>__GCstart(0,{__scened:true})); await pg.waitForTimeout(600);
  const painted = await pg.evaluate(async ()=>{
    const c=document.getElementById('fxcanvas');
    if(!c || !c.width) return {ok:false,why:'canvas never sized'};
    for(let i=0;i<4;i++){ try{ __GCturn({act:'strike'}); }catch(e){} await new Promise(r=>setTimeout(r,220)); }
    await new Promise(r=>requestAnimationFrame(r));
    const x=c.getContext('2d').getImageData(0,0,c.width,c.height).data;
    let lit=0; for(let i=3;i<x.length;i+=4) if(x[i]>8) lit++;
    return {ok:lit>0, lit};
  });
  console.log('  lit pixels: '+JSON.stringify(painted));
  ok(painted.ok,'strikes actually paint particles',JSON.stringify(painted));

  console.log('\n=== the newly-live layer respects the calm settings ===');
  const clearAndStrike = async ()=>pg.evaluate(async ()=>{
    const c=document.getElementById('fxcanvas');
    c.getContext('2d').clearRect(0,0,c.width,c.height);
    for(let i=0;i<4;i++){ try{ __GCturn({act:'strike'}); }catch(e){} await new Promise(r=>setTimeout(r,200)); }
    await new Promise(r=>requestAnimationFrame(r));
    const x=c.getContext('2d').getImageData(0,0,c.width,c.height).data;
    let lit=0; for(let i=3;i<x.length;i+=4) if(x[i]>8) lit++;
    return lit;
  });
  // the module reads SV.settings.calm, not the body class — check the real setting
  await pg.evaluate(()=>{ __GCsave().settings.calm=true; });
  await pg.evaluate(()=>{ const bt=__GC(); if(!bt||bt.over) __GCstart(0,{__scened:true}); });
  await pg.waitForTimeout(500);
  const calmLit = await clearAndStrike();
  ok(calmLit===0,'Calm Mode paints no particles',String(calmLit));
  await pg.evaluate(()=>{ __GCsave().settings.calm=false;
    document.body.classList.add('reduce-motion'); });
  const rmLit = await clearAndStrike();
  ok(rmLit===0,'Reduced Motion paints no particles',String(rmLit));
  await pg.evaluate(()=>document.body.classList.remove('reduce-motion'));
  const backLit = await clearAndStrike();
  ok(backLit>0,'and they come back when both are off',String(backLit));

  console.log('\n=== it survives a resize ===');
  await pg.setViewportSize({width:390,height:844}); await pg.waitForTimeout(400);
  const resized = await pg.evaluate(()=>{const c=document.getElementById('fxcanvas');
    return {w:c.width, expect:Math.round(innerWidth*Math.min(2,devicePixelRatio||1))};});
  ok(resized.w===resized.expect,'the canvas refits on resize',JSON.stringify(resized));

  ok(errs.length===0,'no page or script errors',errs.slice(0,2).join(' | '));
  await b.close();
  console.log('\n'+(fail?fail+' FAILED':'FX PARTICLES VERIFIED'));
  process.exit(fail?1:0);
})();
