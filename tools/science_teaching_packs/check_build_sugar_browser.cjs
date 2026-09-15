/** EDU-Q1 BUILD pilot: inspect the authored lesson, never award pupil outcomes. */
const {chromium}=require('playwright');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const crypto=require('node:crypto');
const {execFileSync}=require('node:child_process');
const root=path.resolve(__dirname,'../..');
const rel='Science_Teesside/Build/W8-W13_2026-27/SCI_B_W8A_Sugar_Labels_Explore.html';
const url=new URL(rel,process.env.EDU_Q1_BASE_URL||'http://127.0.0.1:4187/').href;
const out=path.join(root,'audit-output/science-teaching-packs-edu-q1');
fs.mkdirSync(out,{recursive:true});
const report={source:process.env.GITHUB_SHA||null,lessonSha256:crypto.createHash('sha256').update(fs.readFileSync(path.join(root,rel))).digest('hex'),checks:[],limits:['No physical-device or screen-reader journey is claimed.','Companion PowerPoint and publication acceptance are separate gates.']};
const check=(name,value)=>{assert.ok(value,name);report.checks.push(name)};
(async()=>{
 const browser=await chromium.launch({headless:true});
 const context=await browser.newContext({viewport:{width:1280,height:900},acceptDownloads:true,reducedMotion:'reduce'});
 const page=await context.newPage();const errors=[];page.on('pageerror',e=>errors.push(e.message));
 try{
  const response=await page.goto(url,{waitUntil:'load'});check('Source page returns 200',response.status()===200);
  check('Nine stages total forty minutes',await page.locator('.slide').evaluateAll(es=>es.length===9&&es.reduce((n,e)=>n+Number(e.dataset.timer),0)===40));
  check('Unique element identifiers',await page.evaluate(()=>{const a=[...document.querySelectorAll('[id]')].map(e=>e.id);return a.length===new Set(a).size}));
  check('One optional integrated feedback prompt',await page.locator('main .sugar-lundy').count()===1);
  for(const width of [320,390,768,1280]){
   await page.setViewportSize({width,height:900});
   for(let i=0;i<9;i++){
    await page.evaluate(i=>window.mbmShowSlide(i),i);
    const fit=await page.evaluate(()=>({page:document.documentElement.scrollWidth<=innerWidth+1,slide:document.querySelector('.slide.active').scrollWidth<=document.querySelector('.slide.active').clientWidth+1,focus:document.activeElement===document.querySelector('.slide.active h1,.slide.active h2')}));
    check(`Stage ${i+1} fits ${width}px and receives focus`,fit.page&&fit.slide&&fit.focus);
    if(width===390||width===1280)await page.screenshot({path:path.join(out,`stage-${i+1}-${width}.png`)});
   }
  }
  await page.setViewportSize({width:1280,height:900});
  await page.evaluate(()=>window.mbmShowSlide(1));
  for(const route of ['supported','standard','stretch']){
   await page.locator(`[data-arrival-route="${route}"]`).press('Enter');
   check('Four arrival questions '+route,await page.locator(`#arrival-panel-${route} .arrival-cell`).count()===4);
   const parity=await page.evaluate(route=>{
    const screen=[...document.querySelectorAll(`#arrival-panel-${route} .arrival-cell`)];
    const print=[...document.querySelectorAll(`#print-arrival-${route} .arrival-paper-card`)];
    const norm=e=>e.textContent.replace(/\s+/g,' ').trim();
    return screen.length===4&&screen.every((e,i)=>norm(e.querySelector('h3'))===norm(print[i].querySelector('h3'))&&norm(e.querySelector('p'))===norm(print[i].querySelector('p')));
   },route);check('Arrival screen and print questions match '+route,parity);
   await page.locator('[data-arrival-reveal]').press('Enter');
   check('Arrival reveal retains useful focus '+route,await page.locator('[data-arrival-reveal]').evaluate(e=>e===document.activeElement));
  }
  await page.locator('[data-action="ta"]').press('Enter');
  check('TA dialog starts at its heading',await page.locator('#ta-dialog .v4-modal').evaluate(e=>e.scrollTop===0&&e.querySelector('h2')===document.activeElement));
  await page.keyboard.press('Escape');
  check('TA Escape restores invoking control',await page.locator('[data-action="ta"]').evaluate(e=>e===document.activeElement));
  await page.locator('[data-action="tools"]').press('Enter');
  check('Tools dialog opens after TA Escape',await page.locator('#tools-dialog').evaluate(e=>e.open));
  check('Tools dialog focuses Close',await page.locator('#tools-dialog [data-action="close"]').evaluate(e=>e===document.activeElement));
  await page.locator('#slide-picker').selectOption('4');
  check('Tools selection waits for confirmation',await page.locator('#tools-dialog').evaluate(e=>e.open)&&await page.locator('#slide-2').evaluate(e=>e.classList.contains('active')));
  await page.locator('#tools-dialog [data-action="goto"]').press('Enter');
  check('Tools slide jump focuses new heading',await page.locator('#slide-5 h2').evaluate(e=>e===document.activeElement));
  // Cross a queued native close event before reopening the same dialog.
  for(let i=0;i<3;i++){
   await page.locator('[data-action="tools"]').press('Enter');
   await page.keyboard.press('Escape');
   await page.locator('[data-action="tools"]').press('Enter');
   await page.waitForFunction(()=>document.querySelector('#tools-dialog')?.open&&document.activeElement===document.querySelector('#tools-dialog [data-action="close"]'));
   await page.locator('#tools-dialog [data-action="close"]').press('Enter');
   check('Repeated Tools close preserves focus '+i,await page.locator('[data-action="tools"]').evaluate(e=>e===document.activeElement));
  }
  for(const letter of ['A','B','C','D']){
   await page.locator(`[data-item="${letter}"]`).press('Enter');
   await page.locator(`[data-zone="${letter}"] [data-place-here]`).press('Enter');
  }
  await page.locator('[data-sort-check]').press('Enter');
  check('Keyboard label ordering gives four specific correct results',await page.locator('[data-item][data-result="correct"]').count()===4);
  await page.locator('[data-item="A"]').press('Enter');await page.locator('[data-zone="D"] [data-place-here]').press('Enter');await page.locator('[data-sort-check]').press('Enter');
  check('A wrong arrangement is rejected',await page.locator('[data-item][data-result="revisit"]').count()>0);
  await page.locator('[data-sort-reveal]').press('Enter');check('Sort reveal retains focus',await page.locator('[data-sort-reveal]').evaluate(e=>e===document.activeElement));
  await page.evaluate(()=>window.mbmShowSlide(5));
  for(let i=0;i<3;i++)await page.locator('#add-portion').press('Enter');
  check('Four equal servings give twelve grams sugar',/100 g food.*12 g sugar/.test(await page.locator('#portion-equation').innerText()));
  check('Serving limit does not discard focus',await page.locator('#add-portion').evaluate(e=>e===document.activeElement&&e.getAttribute('aria-disabled')==='true'));
  await page.evaluate(()=>window.mbmShowSlide(6));
  for(const token of ['number','unit','basis']){
   await page.locator(`[data-detective-tool="${token}"]`).press('Enter');await page.locator(`[data-label-token="${token}"]`).press('Enter');
  }
  await page.locator('#detective-check').press('Enter');
  report.detectiveFeedback=await page.locator('#detective-status').innerText();
  check('Label annotation returns explanatory feedback',report.detectiveFeedback.length>25);
  await page.evaluate(()=>window.mbmShowSlide(8));await page.locator('[data-exit-route="standard"]').press('Enter');
  await page.getByLabel('Sugar in B',{exact:true}).selectOption({label:'9 g'});await page.getByLabel('Compare',{exact:true}).selectOption({label:'less'});await page.getByLabel('What do the numbers compare?',{exact:true}).selectOption({label:'sugar'});
  const [download]=await Promise.all([page.waitForEvent('download'),page.locator('#save-sugar-exit').click()]);
  const downloaded=fs.readFileSync(await download.path(),'utf8');check('Exit capture preserves response without awarding a mark',downloaded.includes('9 g')&&downloaded.includes('less')&&downloaded.includes('not a mark'));
  await download.delete();
  await page.evaluate(()=>{window.print=()=>{};});
  for(const route of ['supported','standard','stretch']){
   await page.evaluate(route=>window.printPack(route),route);
   const ids=await page.locator('.print-section.visible').evaluateAll(es=>es.map(e=>e.id));
   check('Pupil print excludes staff answers '+route,ids.includes('print-organiser')&&ids.includes('print-arrival-'+route)&&ids.includes('print-task-'+route)&&ids.includes('print-exit-'+route)&&!ids.some(id=>/answers|staff/.test(id)));
   await page.emulateMedia({media:'print'});await page.pdf({path:path.join(out,`pupil-${route}.pdf`),preferCSSPageSize:true,printBackground:true});await page.emulateMedia({media:'screen'});
   await page.evaluate(()=>dispatchEvent(new Event('afterprint')));
  }
  for(const id of ['organiser','staff','answers','arrival-answers-supported','arrival-answers-standard','arrival-answers-stretch']){
   await page.evaluate(id=>window.printSection(id,'standard'),id);
   check('Selected print section is isolated '+id,await page.locator('.print-section.visible').count()===1);
   await page.emulateMedia({media:'print'});await page.pdf({path:path.join(out,`${id}.pdf`),preferCSSPageSize:true,printBackground:true});await page.emulateMedia({media:'screen'});
   await page.evaluate(()=>dispatchEvent(new Event('afterprint')));
  }
  // DOM visibility passed while the first organiser PDF contained no text.
  // Inspect the produced bytes before allowing the browser report to pass.
  report.pdfReport=JSON.parse(execFileSync('python',['tools/science_teaching_packs/check_build_sugar_pdfs.py',out],{cwd:root,encoding:'utf8'}));
  check('Browser PDFs retain organiser text, complete tickets and printable margins',report.pdfReport.status==='PASS');
  await page.evaluate(()=>document.documentElement.style.fontSize='200%');
  for(let i=0;i<9;i++){await page.evaluate(i=>window.mbmShowSlide(i),i);check('No horizontal loss at 200 percent text '+(i+1),await page.locator('.slide.active').evaluate(e=>e.scrollWidth<=e.clientWidth+1));}
  await page.screenshot({path:path.join(out,'text-200.png')});
  await page.goto(url+'#slide-5');check('Incoming legacy slide fragment retained',await page.locator('#slide-5').evaluate(e=>e.classList.contains('active')));
  check('No autoplay media',await page.locator('video[autoplay],audio[autoplay]').count()===0);
  check('Reduced motion disables CSS animation',await page.evaluate(()=>[...document.querySelectorAll('.slide.active *')].every(e=>getComputedStyle(e).animationName==='none')));
  check('No JavaScript errors',errors.length===0);
  const fallback=await browser.newContext({javaScriptEnabled:false,viewport:{width:390,height:900}});const nojs=await fallback.newPage();await nojs.goto(url);
  check('No-script lesson remains readable',await nojs.locator('#slide-8').isVisible());await nojs.screenshot({path:path.join(out,'no-script.png')});await fallback.close();
  report.status='PASS';
 }catch(error){report.status='FAIL';report.error=String(error);report.pageErrors=errors;report.failureState=await page.evaluate(()=>({focus:document.activeElement?.outerHTML,dialogs:[...document.querySelectorAll('dialog')].map(e=>({id:e.id,open:e.open,display:getComputedStyle(e).display})),picker:document.querySelector('#slide-picker')?.getBoundingClientRect().toJSON()})).catch(()=>null);await page.screenshot({path:path.join(out,'failure.png')}).catch(()=>{});throw error;
 }finally{console.log('EDU_Q1_REPORT '+JSON.stringify(report));fs.writeFileSync(path.join(out,'report.json'),JSON.stringify(report,null,2)+'\n');await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1});
