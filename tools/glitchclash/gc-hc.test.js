/* High Contrast must still darken the page now the fill lives on <html>. */
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
  const fill=()=>pg.evaluate(()=>getComputedStyle(document.documentElement).backgroundColor);
  const before=await fill();
  ok(before==='rgb(13, 19, 34)','the page fill is painted from <html>',before);
  await pg.click('#scr-title [data-open="settings"]'); await pg.waitForTimeout(250);
  await pg.click('#hctoggle'); await pg.waitForTimeout(300);
  const after=await fill();
  const cls=await pg.evaluate(()=>({h:document.documentElement.classList.contains('hc'),
                                    b:document.body.classList.contains('hc')}));
  ok(cls.h&&cls.b,'both <html> and <body> are flagged',JSON.stringify(cls));
  ok(after==='rgb(0, 0, 0)','High Contrast blacks the page out',after);
  // and a theme must not be able to undo it
  await pg.evaluate(()=>GCX2.applyTheme('amber')); await pg.waitForTimeout(150);
  ok(await fill()==='rgb(0, 0, 0)','a theme cannot override High Contrast');
  await pg.click('#hctoggle'); await pg.waitForTimeout(300);
  const back=await fill();
  ok(back!=='rgb(0, 0, 0)','switching it off restores the theme',back);
  ok(errs.length===0,'no page or script errors',errs.slice(0,2).join(' | '));
  await b.close();
  console.log('\n'+(fail?fail+' FAILED':'HIGH CONTRAST VERIFIED'));
  process.exit(fail?1:0);
})();
