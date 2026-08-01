/* The new surfaces must behave under Calm Mode, Reduced Motion and keyboard. */
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
  const ctx=await b.newContext({viewport:{width:412,height:892},reducedMotion:'reduce'});
  const pg=await ctx.newPage();
  const errs=[]; pg.on('pageerror',e=>errs.push('PAGEERR '+e.message));
  await pg.goto(TARGET);
  await pg.waitForTimeout(1200);
  let fail=0; const ok=(c,l,d)=>{c?console.log('  PASS  '+l+(d?'   '+d:'')):(fail++,console.log('  FAIL  '+l+(d?'   '+d:'')));};

  const rm = await pg.evaluate(()=>document.body.classList.contains('reduce-motion'));
  ok(rm,'prefers-reduced-motion is honoured at boot');

  await pg.click('#scr-title [data-go="home"]'); await pg.waitForTimeout(300);
  await pg.evaluate(()=>{ const s=JSON.parse(localStorage.getItem('glitchclash_save')||'{}');
    s.stats=Object.assign({},s.stats,{wins:30}); localStorage.setItem('glitchclash_save',JSON.stringify(s)); });
  await pg.reload(); await pg.waitForTimeout(1000);
  await pg.click('#scr-title [data-go="home"]'); await pg.waitForTimeout(300);

  console.log('=== theme sheet keyboard + labels ===');
  await pg.click('[data-open="themes"]'); await pg.waitForTimeout(300);
  const focus = await pg.evaluate(()=>document.activeElement && document.activeElement.tagName);
  ok(focus==='BUTTON','focus moves into the sheet on open',String(focus));
  const labels = await pg.evaluate(()=>[...document.querySelectorAll('#themelist [data-theme]')]
    .map(b=>b.getAttribute('aria-label')));
  ok(labels.every(l=>l&&l.length>10),'every theme row carries a spoken label',labels[1]);
  const cur = await pg.evaluate(()=>!!document.querySelector('#themelist [aria-current="true"]'));
  ok(cur,'the selected theme is marked aria-current');
  const swatchHidden = await pg.evaluate(()=>{
    const b=document.querySelector('#themelist [data-theme="amber"]');
    return b.textContent.includes('Amber');   // colour is never the only cue
  });
  ok(swatchHidden,'theme names are text, not colour alone');
  await pg.keyboard.press('Escape'); await pg.waitForTimeout(250);
  const closed = await pg.evaluate(()=>!document.querySelector('.overlay.show'));
  ok(closed,'Escape closes the theme sheet');

  console.log('\n=== calm mode + endless ===');
  await pg.evaluate(()=>{ document.body.classList.add('calm'); });
  await pg.click('#endlessbtn'); await pg.waitForTimeout(400);
  await pg.click('#modgo'); await pg.waitForTimeout(1400);
  const inB = await pg.evaluate(()=>!!document.querySelector('#scr-battle.active'));
  ok(inB,'endless starts under Calm Mode');
  const noGlitch = await pg.evaluate(()=>{
    const before=[...document.body.classList].filter(c=>c.startsWith('gcx-')).length;
    for(let i=0;i<12;i++){ try{ __GCturn({act:i%2?'strike':'charge'}); }catch(e){} }
    return [...document.body.classList].filter(c=>c.startsWith('gcx-')&&c!=='gcx-crt').length-before;
  });
  ok(noGlitch<=0,'Calm Mode still suppresses reality glitches mid-run',String(noGlitch));
  const chip = await pg.evaluate(()=>{const c=document.querySelector('#stagechip'); return c?c.textContent:'';});
  ok(/Endless · Round/.test(chip),'the round is stated in text, not implied',chip);

  ok(errs.length===0,'no page or script errors',errs.slice(0,3).join(' | '));
  await b.close();
  console.log('\n'+(fail?fail+' FAILED':'ACCESSIBILITY CHECKS PASSED'));
  process.exit(fail?1:0);
})();
