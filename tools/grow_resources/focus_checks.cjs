/* EDU-Q1 GROW W3A: targeted keyboard regression checks, not pilot acceptance.
 * Run: node tools/grow_resources/focus_checks.cjs [repository-root] [report-dir]
 * Requires the existing Playwright runtime. Exercises the canonical paired
 * lesson as a standalone file and through a local HTTP server. */
'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const http = require('node:http');
const {pathToFileURL} = require('node:url');
const {chromium} = require('playwright');
const source = 'Science_Teesside/Grow/SCI_G_W3_Friction.html';

async function run(root, out) {
  fs.mkdirSync(out, {recursive:true});
  const report = {scope:'GROW W3A keyboard repair; shared W3B navigation only. Local HTTP is not a publication proof. No assistive-technology listening claim.',cases:[],errors:[]};
  const server = http.createServer((req,res) => {
    const file = path.resolve(root, '.' + decodeURIComponent(new URL(req.url,'http://localhost').pathname));
    if (!file.startsWith(root+path.sep) || !fs.existsSync(file) || !fs.statSync(file).isFile()) {res.writeHead(404).end();return;}
    res.setHeader('Content-Type',file.endsWith('.html')?'text/html; charset=utf-8':file.endsWith('.js')?'text/javascript':file.endsWith('.css')?'text/css':'application/octet-stream');
    fs.createReadStream(file).pipe(res);
  });
  await new Promise(resolve => server.listen(0,'127.0.0.1',resolve));
  const browser = await chromium.launch({headless:true});
  const urls = {standalone:pathToFileURL(path.join(root,source)).href,http:`http://127.0.0.1:${server.address().port}/${source}`};
  try {
    for (const [mode,url] of Object.entries(urls)) for (const [width,motion] of [[320,'reduce'],[1280,'reduce'],[1280,'no-preference']]) {
      const context = await browser.newContext({viewport:{width,height:900},reducedMotion:motion});
      const page = await context.newPage();page.setDefaultTimeout(5000);
      page.on('pageerror',e=>report.errors.push({mode,width,motion,error:e.message}));
      const check = async (name,fn) => {await fn();report.cases.push({mode,width,motion,name,passed:true});};
      const active = () => page.locator('.slide.active').getAttribute('data-title');
      const focused = sel => page.locator(sel).first().evaluate(n=>n===document.activeElement);
      const goto = async i => {await page.evaluate(i=>showSlide(i),i);await page.waitForTimeout(60);};
      const deckNext = page.locator('button[onclick="nextSlide()"]');
      await page.goto(url,{waitUntil:'load'});
      await check('load does not steal focus',async()=>assert.equal(await page.evaluate(()=>document.activeElement.tagName),'BODY'));
      await check('Next focuses Arrival heading',async()=>{await deckNext.focus();await page.keyboard.press('Enter');assert.equal(await active(),'Arrival Task');assert.equal(await focused('.slide.active h2'),true);});
      await check('heading ArrowRight and ArrowLeft navigate',async()=>{await page.keyboard.press('ArrowRight');assert.equal(await active(),'Today at a Glance');assert.equal(await focused('.slide.active h2'),true);await page.keyboard.press('ArrowLeft');assert.equal(await active(),'Arrival Task');});
      await check('same slide refresh preserves control focus',async()=>{await deckNext.focus();await page.evaluate(()=>showSlide(1));assert.equal(await focused('button[onclick="nextSlide()"]'),true);});
      const titles=await page.locator('.slide').evaluateAll(nodes=>nodes.map(n=>n.dataset.title));
      for(let i=0;i<titles.length;i++) await check('context focus: '+titles[i],async()=>{await goto(i);assert.equal(await focused('.slide.active h1,.slide.active h2'),true);assert.equal(await page.locator('.slide.active h1,.slide.active h2').first().getAttribute('tabindex'),'-1');});
      await check('both periods retain exact pacing and boundary',async()=>{
        assert.deepEqual(await page.locator('.slide').evaluateAll(nodes=>nodes.map(n=>Number(n.dataset.timer))),[1,4,2,9,10,4,10,32,4,4]);
        await goto(0);const resume=page.getByRole('button',{name:'Resume Lesson B',exact:false});await resume.focus();await page.keyboard.press('Enter');assert.equal(await active(),'Independent Work');assert.equal(await focused('.slide.active h2'),true);
        await page.locator('button[onclick="prevSlide()"]').focus();await page.keyboard.press('Enter');assert.equal(await active(),'We Do 2');assert.equal(await focused('.slide.active h2'),true);
      });
      await goto(3);
      await check('model step keeps focus while enabled',async()=>{await page.locator('.slide.active .g-next').first().focus();await page.keyboard.press('Enter');assert.equal(await focused('.slide.active .g-next'),true);});
      await check('prediction pause focuses reveal before disabling Next',async()=>{await page.keyboard.press('Enter');assert.equal(await focused('.slide.active .g-pause button'),true);assert.equal(await active(),'I Do 1');});
      await page.screenshot({path:path.join(out,`${mode}-${width}-${motion}-prediction.png`),fullPage:true});
      await check('Space reveals once and restores model focus',async()=>{await page.keyboard.press('Space');assert.equal(await active(),'I Do 1');assert.equal(await page.locator('.slide.active .g-pause').count(),0);assert.equal(await focused('.slide.active .g-next'),true);assert.equal(await page.locator('.slide.active .g-stage').first().evaluate(n=>n._g.i),3);});
      await check('model completion focuses Replay',async()=>{for(let i=0;i<4;i++)await page.keyboard.press('Enter');assert.equal(await focused('.slide.active .g-reset'),true);assert.equal(await page.locator('.slide.active .g-stage').first().evaluate(n=>n._g.i),7);});
      await check('Replay restarts without moving focus',async()=>{await page.keyboard.press('Enter');assert.equal(await focused('.slide.active .g-reset'),true);assert.equal(await page.locator('.slide.active .g-stage').first().evaluate(n=>n._g.i),0);});
      await check('deck Next advances/reveals model without stealing focus',async()=>{await deckNext.focus();for(let i=0;i<3;i++){await page.keyboard.press('Enter');assert.equal(await focused('button[onclick="nextSlide()"]'),true);assert.equal(await active(),'I Do 1');}assert.equal(await page.locator('.slide.active .g-stage').first().evaluate(n=>n._g.i),3);});
      await check('Show all retains focus and completes model',async()=>{await page.locator('.slide.active .g-all').first().focus();await page.keyboard.press('Enter');assert.equal(await focused('.slide.active .g-all'),true);assert.equal(await page.locator('.slide.active .g-stage').first().evaluate(n=>n._g.i),7);});
      await check('next actual slide focuses its heading',async()=>{await deckNext.focus();await page.keyboard.press('Enter');assert.equal(await active(),'We Do 1');assert.equal(await focused('.slide.active h2'),true);});
      await check('Space activates example card without changing slide',async()=>{await page.locator('.slide.active .pres-card').first().focus();await page.keyboard.press('Space');assert.equal(await active(),'We Do 1');assert.equal(await focused('.slide.active .pres-card'),true);assert.equal(await page.locator('#pres-num').innerText(),'1');});
      await check('ArrowRight on example card does not change slide',async()=>{await page.keyboard.press('ArrowRight');assert.equal(await active(),'We Do 1');assert.equal(await focused('.slide.active .pres-card'),true);});
      await check('Space selects sort card and places it without navigation',async()=>{await goto(6);const card=page.locator('#kw-pills .match-pill').first();await card.focus();await page.keyboard.press('Space');assert.equal(await card.evaluate(n=>n.classList.contains('selected')),true);assert.equal(await active(),'We Do 2');const bin=page.locator('.sort-bin[data-cat="c_true"]');await bin.focus();await page.keyboard.press('Space');assert.equal(await active(),'We Do 2');assert.equal(await bin.locator('.sort-chip').count(),1);assert.equal(await focused('.sort-bin[data-cat="c_true"]'),true);});
      await check('resource link retains native Space/ArrowRight',async()=>{await goto(0);const link=page.locator('.slide.active a[href="resources/GS_W3A.html"]').first();await link.focus();await page.keyboard.press('Space');await page.keyboard.press('ArrowRight');assert.equal(await active(),'Title');assert.equal(await link.evaluate(n=>n===document.activeElement),true);});
      await context.close();
    }
    assert.deepEqual(report.errors,[],'No runtime errors');
    report.result='PASS';
  } catch(e) {report.result='FAIL';report.failure=e.stack;throw e;}
  finally {fs.writeFileSync(path.join(out,'focus-report.json'),JSON.stringify(report,null,2)+'\n');await browser.close();await new Promise(resolve=>server.close(resolve));}
  console.log(JSON.stringify({result:report.result,cases:report.cases.length,runtimeErrors:report.errors.length}));
}
if(require.main===module) run(path.resolve(process.argv[2]||path.join(__dirname,'../..')),path.resolve(process.argv[3]||'grow-focus-review')).catch(e=>{console.error(e);process.exitCode=1;});
module.exports={run};
