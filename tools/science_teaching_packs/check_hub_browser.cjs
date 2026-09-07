/** Responsive Science pack discovery and exact-byte download proof. */
const {chromium}=require('playwright');
const fs=require('node:fs');
const path=require('node:path');
const crypto=require('node:crypto');
const assert=require('node:assert/strict');
const root=path.resolve(__dirname,'../..');
const packs=path.join(root,'Science_Teesside/Teaching_Packs');
const base=process.env.SCIENCE_PACK_BASE_URL || 'http://127.0.0.1:4187/Science_Teesside/Teaching_Packs/';
const output=process.env.SCIENCE_PACK_BROWSER_OUTPUT || path.join(root,'audit-output/science-teaching-packs');
const digest=buffer=>crypto.createHash('sha256').update(buffer).digest('hex');
const load=filename=>JSON.parse(fs.readFileSync(filename,'utf8'));

(async()=>{
 fs.mkdirSync(output,{recursive:true});
 const manifests={};
 const downloads=new Map();
 for(const pathway of ['BUILD','GROW','LAUNCH']){
  const source=load(path.join(packs,pathway,'SOURCE_MANIFEST.json'));
  const archives=load(path.join(packs,pathway,'DOWNLOAD_INDEX.json')).archives;
  manifests[pathway]={source,archives};
  for(const item of [...source.lessons.flatMap(l=>l.files),...(source.packFiles||[]),...archives])downloads.set(pathway+'/'+item.file,item);
 }
 const browser=await chromium.launch({headless:true});
 const context=await browser.newContext({acceptDownloads:true});
 const results={base,source:process.env.SCIENCE_PACK_SOURCE_SHA||process.env.GITHUB_SHA||null,publicationRun:process.env.SCIENCE_PACK_PUBLICATION_RUN||null,viewports:[],downloadBytes:[]};
 try{
  for(const width of [390,1280]){
   const page=await context.newPage();
   // Context defaults can override page options; set the viewport explicitly.
   await page.setViewportSize({width,height:900});
   const response=await page.goto(base,{waitUntil:'domcontentloaded',timeout:60000});
   assert.equal(response.status(),200,'Hub response');
   await page.screenshot({path:path.join(output,'hub-'+width+'.png')});
   const counts=await page.evaluate(()=>({
    overflow:document.documentElement.scrollWidth>innerWidth,
    lessons:document.querySelectorAll('article.lesson').length,
    archives:[...document.querySelectorAll('a[download]')].filter(a=>a.getAttribute('href').endsWith('.zip')).length,
    emptyLinks:[...document.querySelectorAll('a')].filter(a=>!a.textContent.trim()).length,
   }));
   assert.equal(counts.overflow,false,'Horizontal overflow at '+width);
   assert.equal(counts.lessons,35);assert.equal(counts.archives,62);assert.equal(counts.emptyLinks,0);
   // The geometry assertion must detect an actual planted overflow.
   await page.evaluate(()=>{const e=document.createElement('div');e.id='overflow-control';e.style.cssText='position:absolute;left:0;top:0;width:calc(100vw + 100px);height:1px';document.body.append(e)});
   assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),true,'Overflow rejection control');
   await page.locator('#overflow-control').evaluate(e=>e.remove());
   assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false,'Restored geometry');
   const clickProof=[];
   for(const pathway of ['BUILD','GROW','LAUNCH']){
    const id=pathway.toLowerCase();
    await page.locator('a[href="#'+id+'"]').click();
    await page.waitForFunction(target=>{
     const element=document.getElementById(target);
     const offset=(parseFloat(getComputedStyle(document.documentElement).scrollPaddingTop)||0)
      +(parseFloat(getComputedStyle(element).scrollMarginTop)||0);
     return location.hash==='#'+target && Math.abs(element.getBoundingClientRect().top-offset)<=2;
    },id,{timeout:5000});
    await page.screenshot({path:path.join(output,id+'-'+width+'.png')});
    await page.locator('#'+id+'-week-7').evaluate(e=>e.open=false);
    await page.locator('a[href="#'+id+'-week-7"]').click();
    // Fragment navigation dispatches hashchange asynchronously after the click.
    await page.waitForFunction(target=>document.getElementById(target).open,
     id+'-week-7',{timeout:5000});
    assert.equal(await page.locator('#'+id+'-week-7').evaluate(e=>e.open),true,'Week link opens selected week');
    await page.waitForFunction(target=>{
     const element=document.getElementById(target);
     const offset=(parseFloat(getComputedStyle(document.documentElement).scrollPaddingTop)||0)
      +(parseFloat(getComputedStyle(element).scrollMarginTop)||0);
     return location.hash==='#'+target && Math.abs(element.getBoundingClientRect().top-offset)<=2;
    },id+'-week-7',{timeout:5000});
    await page.screenshot({path:path.join(output,id+'-week-7-'+width+'.png')});
    const whole=manifests[pathway].archives.find(a=>a.kind==='whole');
    const [download]=await Promise.all([
     page.waitForEvent('download',{timeout:120000}),
     page.locator('a[href="'+pathway+'/'+whole.file+'"]').click(),
    ]);
    const file=await download.path();
    assert.equal(digest(fs.readFileSync(file)),whole.sha256,'Whole pack browser download bytes');
    clickProof.push({pathway,file:whole.file,sha256:whole.sha256});
    await download.delete();
   }
   results.viewports.push({width,...counts,overflowControl:'PASS',weekNavigation:'PASS',clickProof});
   await page.close();
  }
  // Every individual file and every archive must match this exact source build.
  for(const [relative,item] of downloads){
   const response=await context.request.get(new URL(relative,base).href,{timeout:120000});
   assert.equal(response.status(),200,'Download response: '+relative);
   const bytes=await response.body();
   assert.equal(bytes.length,item.bytes,'Download length: '+relative);
   assert.equal(digest(bytes),item.sha256,'Download hash: '+relative);
   results.downloadBytes.push({file:relative,bytes:bytes.length,sha256:item.sha256});
   await response.dispose();
  }
  results.status='PASS';
 }catch(error){
  results.status='FAIL';results.error=String(error);results.navigation=[];
  for(const [index,page] of context.pages().entries()){
   results.navigation.push(await page.evaluate(()=>{
    const element=document.getElementById(location.hash.slice(1));
    return {hash:location.hash,scrollY,top:element?.getBoundingClientRect().top,open:element?.open,
     scrollPadding:getComputedStyle(document.documentElement).scrollPaddingTop,
     scrollMargin:element?getComputedStyle(element).scrollMarginTop:null};
   }));
   await page.screenshot({path:path.join(output,'failure-'+index+'.png')});
  }
  throw error;
 }
 finally{
  fs.writeFileSync(path.join(output,'results.json'),JSON.stringify(results,null,2)+'\n');
  await browser.close();
 }
 console.log(JSON.stringify({status:results.status,base,viewports:results.viewports.map(v=>v.width),exactDownloads:results.downloadBytes.length}));
})().catch(error=>{console.error(error);process.exitCode=1});
