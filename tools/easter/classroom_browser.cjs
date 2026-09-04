/* The real classroom surface in CI Chrome. No fixture creates a venue booking. */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const {chromium} = require('playwright');
const root = path.resolve(__dirname, '../..');
const targets = JSON.parse(fs.readFileSync(path.join(__dirname,'CLASSROOM_TARGETS.json'))).decks;
const palettes = {BUILD:'rgb(79, 134, 156)', GROW:'rgb(91, 145, 165)', LAUNCH:'rgb(53, 111, 131)'};
(async () => {
  const browser = await chromium.launch({headless:true, channel:process.env.CI ? 'chrome' : undefined});
  let checked = 0;
  try {
    const page = await browser.newPage({viewport:{width:1280,height:800}});
    const failures=[];
    page.on('pageerror',error=>failures.push(error.message));
    await page.route('http://classroom.test/**',route=>{
      const name = decodeURIComponent(new URL(route.request().url()).pathname).slice(1);
      const file=path.resolve(root,name);
      if (!file.startsWith(root+path.sep)||!fs.existsSync(file)||!fs.statSync(file).isFile())
        return route.fulfill({status:404,body:'No fixture'});
      return route.fulfill({contentType:file.endsWith('.json')?'application/json':'text/html',body:fs.readFileSync(file)});
    });
    async function checkTitle(expected) {
      const title=page.locator('main.deck>.slide').first().locator('h1');
      assert.equal(await title.count(),1,'missing title');
      assert.equal(await title.textContent(),expected,'title is the lesson title');
      assert.ok(await title.isVisible(),'visible heading');
    }
    async function inspect(row) {
      await page.goto('http://classroom.test/'+row.file);
      const cfg=JSON.parse(await page.locator('#lesson-config').textContent());
      await checkTitle(cfg.title);
      const state=await page.locator('main.deck>.slide').first().evaluate(el=>({
        border:getComputedStyle(el).borderTopColor,
        width:el.getBoundingClientRect().width, left:el.getBoundingClientRect().left,
        viewport:innerWidth, titleSize:parseFloat(getComputedStyle(el.querySelector('h1')).fontSize),
        labels:Array.from(el.querySelectorAll('.lundy-grid>span'),n=>n.textContent.trim())
      }));
      assert.equal(state.border,palettes[row.family.split(' ')[0]],row.file+': reference palette');
      assert.ok(state.width+state.left<=state.viewport+1 && state.left>=0,row.file+': no horizontal crop');
      assert.ok(state.titleSize>=28,row.file+': readable title');
      if(state.labels.length) assert.deepEqual(state.labels,['SPACE','VOICE','AUDIENCE','INFLUENCE']);
      assert.equal(await page.locator('main.deck>.slide').count(),9);
      checked++;
    }
    for(const row of targets) await inspect(row);
    // Responsive checks cover each pathway/subject shell; all 101 were read above.
    const representatives = [...new Map(targets.map(r=>[r.family,r])).values()];
    for(const viewport of [{width:390,height:844},{width:840,height:720}]) {
      await page.setViewportSize(viewport);
      for(const row of representatives) await inspect(row);
    }
    await page.emulateMedia({reducedMotion:'reduce'});
    const animation=await page.locator('main.deck>.slide').first().evaluate(el=>getComputedStyle(el).animationName);
    assert.equal(animation,'none');
    // A planted missing title proves that a visible shell alone cannot pass.
    await page.locator('main.deck>.slide').first().locator('h1').evaluate(el=>el.remove());
    await assert.rejects(()=>checkTitle('a title'),/missing title/);
    assert.ok(!failures.length,JSON.stringify(failures));
    console.log(JSON.stringify({classroomSurfaces:targets.length,viewportChecks:checked,
      responsiveFamilies:representatives.length,titleAndPalette:true,reducedMotion:true,missingTitleControl:true}));
  } finally {await browser.close();}
})().catch(error=>{console.error(error);process.exitCode=1;});
