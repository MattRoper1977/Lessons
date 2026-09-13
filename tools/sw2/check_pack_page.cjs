/* K3: independent record census plus actual browser/print/keyboard journeys. */
const fs=require('fs'),path=require('path'),assert=require('assert/strict');
const {chromium}=require('playwright');
const root=path.resolve(__dirname,'../..');
const arg=(n,d)=>{const i=process.argv.indexOf(n);return i<0?d:process.argv[i+1]};
const base=arg('--base','http://127.0.0.1:8765'),out=path.resolve(arg('--output','audit-output/pack-page'));
fs.mkdirSync(out,{recursive:true});
const packs=JSON.parse(fs.readFileSync(path.join(root,'resources.json'),'utf8')).filter(r=>r.kind==='pack'&&r.companionOf);
const notes=JSON.parse(fs.readFileSync(path.join(root,'assets/catalogue/pack-notes.json'),'utf8')).entries;
const rank=f=>['lesson:pptx','slides:pdf','pupil:docx','pupil:pdf','teacher:docx','teacher:pdf'].indexOf(f.role+':'+f.type);
const report={base,packs:[],matrix:[],errors:[],requests:[],notes:0};
function contrast(f,b){const l=s=>{const v=s.match(/[\d.]+/g).slice(0,3).map(Number).map(x=>{x/=255;return x<=.04045?x/12.92:((x+.055)/1.055)**2.4});return v[0]*.2126+v[1]*.7152+v[2]*.0722};return (Math.max(l(f),l(b))+.05)/(Math.min(l(f),l(b))+.05)}
(async()=>{
 const browser=await chromium.launch();
 try{
 const page=await browser.newPage({viewport:{width:390,height:844},reducedMotion:'reduce'});
 page.on('pageerror',e=>report.errors.push(String(e)));
 page.on('request',r=>{if(new URL(r.url()).origin!==new URL(base).origin)report.requests.push(r.url())});
 async function open(p){await page.goto(base+'/Lessons/pack.html?id='+encodeURIComponent(p.id));await page.waitForFunction(id=>document.querySelector('#pack-content')?.dataset.ready===id,p.id);}
 for(const pack of packs){
  await open(pack);
  const facts=await page.evaluate(()=>({title:document.querySelector('h1').textContent,rows:[...document.querySelectorAll('.pk-file')].map(r=>({path:r.dataset.file,href:r.querySelector('a').getAttribute('href'),download:r.querySelector('a').hasAttribute('download')})),delivery:document.querySelector('#delivery').getAttribute('href'),drift:!!document.querySelector('.pk-drift'),note:document.querySelector('.pk-note p')?.textContent||null,back:document.querySelector('.pk-back').getAttribute('href'),badges:[...document.querySelectorAll('.pk-format')].map(e=>e.textContent)}));
  const files=[...pack.files].sort((a,b)=>(rank(a)<0?99:rank(a))-(rank(b)<0?99:rank(b)));
  assert.equal(facts.rows.length,pack.files.length,pack.id+' count');
  assert.deepEqual(facts.rows.map(r=>r.path),files.map(f=>f.path),pack.id+' membership/order');
  for(let i=0;i<files.length;i++){assert.equal(decodeURI(facts.rows[i].href),'/Lessons/'+files[i].path);assert.equal(facts.rows[i].download,!['pdf','html'].includes(files[i].type));}
  assert.equal(decodeURI(facts.delivery),'/Lessons/'+pack.companionOf);
  assert.equal(facts.drift,!!pack.packRevisionDrift);assert.equal(facts.note,notes[pack.id]?.text||null);
  assert.deepEqual([...facts.badges].sort(),[...new Set(files.map(f=>f.type.toUpperCase()))].sort());
  if(facts.note)report.notes++;
  const back=new URL(facts.back,base);assert.equal(back.pathname,'/resources/');assert.equal(back.searchParams.get('unit'),pack.unit||'');assert.equal(back.searchParams.get('halfTerm'),pack.halfTerm);
  report.packs.push({id:pack.id,files:facts.rows.length,title:facts.title,drift:facts.drift,note:!!facts.note});
 }
 assert.equal(report.packs.length,packs.length);assert(packs.length>0);
 const paths=[...new Set(packs.flatMap(p=>[p.companionOf,...p.files.map(f=>f.path)]))];
 for(let i=0;i<paths.length;i+=12){await Promise.all(paths.slice(i,i+12).map(async rel=>{const res=await page.request.head(base+'/Lessons/'+encodeURI(rel));assert.equal(res.status(),200,rel)}));}
 report.resolving=paths.length;
 const sugar=packs.find(p=>/sugar/i.test(p.title)),drift=packs.find(p=>p.packRevisionDrift),noted=packs.find(p=>notes[p.id]);
 for(const width of [390,900,1280])for(const theme of ['cream','pink','blue','light','dark','highlumen']){
  await page.setViewportSize({width,height:900});
  await page.evaluate(t=>localStorage.setItem('mbm_reading_theme',t),theme);await open(theme==='dark'?drift:sugar);
  const facts=await page.evaluate(()=>{
   const visible=e=>{const r=e.getBoundingClientRect();return r.width&&r.height&&getComputedStyle(e).visibility!=='hidden'};
   const pairs=[];for(const e of document.querySelectorAll('.pk-main *')){if(!visible(e)||![...e.childNodes].some(n=>n.nodeType===3&&n.textContent.trim()))continue;const s=getComputedStyle(e);let p=e,b='';while(p){b=getComputedStyle(p).backgroundColor;if(b!=='rgba(0, 0, 0, 0)'&&b!=='transparent')break;p=p.parentElement;}pairs.push({tag:e.tagName,text:e.textContent.slice(0,45),ink:s.color,bg:b,large:parseFloat(s.fontSize)>=24||(parseFloat(s.fontSize)>=18.66&&Number(s.fontWeight)>=700)});}
   return {overflow:document.documentElement.scrollWidth>innerWidth,small:[...document.querySelectorAll('a,button,summary')].filter(e=>visible(e)&&!e.classList.contains('skip')).filter(e=>{const r=e.getBoundingClientRect();return r.width<43.9||r.height<43.9}).map(e=>e.outerHTML.slice(0,100)),pairs};
  });
  assert(!facts.overflow,`overflow ${width}/${theme}`);assert.deepEqual(facts.small,[],`targets ${width}/${theme}`);
  for(const p of facts.pairs){p.ratio=contrast(p.ink,p.bg);assert(p.ratio>=(p.large?3:4.5)-.01,JSON.stringify({width,theme,...p}));}
  await page.locator('#delivery').focus();const ring=await page.locator('#delivery').evaluate(e=>({style:getComputedStyle(e).outlineStyle,width:getComputedStyle(e).outlineWidth}));assert.equal(ring.style,'solid');assert(parseFloat(ring.width)>=3);
  report.matrix.push({width,theme,minContrast:Math.min(...facts.pairs.map(p=>p.ratio)),pairs:facts.pairs.length});
  if(theme==='cream')await page.screenshot({path:path.join(out,'pack-'+width+'.png'),fullPage:true});
 }
 await page.evaluate(()=>localStorage.setItem('mbm_reading_theme','cream'));await open(sugar);
 await page.locator('#save-pack').click();assert.equal(await page.locator('#save-pack').getAttribute('aria-pressed'),'true');
 await page.reload();await page.waitForSelector('#save-pack');assert.equal(await page.locator('#save-pack').getAttribute('aria-pressed'),'true');
 await page.goto(base+'/Lessons/?view=saved');await page.waitForFunction(()=>window.MBM_HUB?.state.rows.length>0);assert.equal(await page.locator('[data-resource-path]').filter({has:page.locator('a[href*="'+sugar.file.split('/').pop()+'"]')}).count()>0,true,'Saved pack reachable');
 await open(sugar);await page.locator('#save-pack').click();assert.equal(await page.locator('#save-pack').getAttribute('aria-pressed'),'false');
 const menu=page.locator('.mbm-unified-menu>summary');await menu.click();await page.locator('.mbm-menu-close').click();assert.equal(await menu.evaluate(e=>document.activeElement===e),true);
 for(const p of [sugar,drift,noted]){await open(p);await page.emulateMedia({media:'print'});assert.equal(await page.locator('header').isVisible(),false);assert.equal(await page.locator('footer').isVisible(),false);assert.equal(await page.locator('.pk-file').count(),p.files.length);assert(await page.locator('#delivery').isVisible());assert.equal(await page.locator('.pk-note').isVisible(),false);await page.pdf({path:path.join(out,p.id+'.pdf'),format:'A4',printBackground:true});await page.emulateMedia({media:'screen'});}
 for(const url of ['/Lessons/pack.html','/Lessons/pack.html?id=unknown','/Lessons/pack.html?id=%3Cscript%3E']){await page.goto(base+url);await page.waitForSelector('[data-ready="chooser"]');assert(await page.locator('.pk-chooser a').count()>0);}
 assert.deepEqual(report.errors,[]);assert.deepEqual(report.requests,[]);
 report.status='PASS';console.log(JSON.stringify({status:report.status,packs:report.packs.length,files:report.packs.reduce((n,p)=>n+p.files,0),notes:report.notes,links:report.resolving,matrix:report.matrix.length}));
 }finally{fs.writeFileSync(path.join(out,'acceptance.json'),JSON.stringify(report,null,2));await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1});
