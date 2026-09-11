/* Execute the same assertion used by browser_checks.cjs against actual model
 * fragments. Mutations affect the temporary browser DOM, never source files.
 */
'use strict';
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const crypto=require('node:crypto');
const {chromium}=require('playwright');
const {assertRenderedModel}=require('./rendered_model.cjs');
const {resourceFallbackUrl}=require('./browser_checks.cjs');
const args={};
for(let i=2;i<process.argv.length;i+=2){
  assert.ok(['--root','--fixtures','--out','--channel'].includes(process.argv[i]));
  assert.ok(process.argv[i+1]);args[process.argv[i].slice(2)]=process.argv[i+1];
}
const root=fs.realpathSync(args.root||path.join(__dirname,'../..'));
const fixturePath=path.resolve(args.fixtures||path.join(__dirname,'model_fixtures.json'));
const fixtures=JSON.parse(fs.readFileSync(fixturePath,'utf8'));
const out=path.resolve(args.out||'model-controls.json');
assert.equal(fixtures.schema,'s1b-no-video-model-controls-v1');
assert.ok(fixtures.inlineModels.length>0);
const origin='http://s1b-model-controls.test';
const results=[];
const fallbackUrlControls=[];
let currentDocument;
// These use the same destination assertion as the real-click browser check.
const fallbackLesson=JSON.parse(fs.readFileSync(path.join(root,'tools/science_pack/RESOURCE_CONTENT.json'),'utf8')).find(c=>c.online_path===fixtures.oldImage.sourcePath);
assert.ok(fallbackLesson);
const fallbackSource=fs.readFileSync(path.join(root,fallbackLesson.online_path),'utf8');
const fallbackHref=fallbackSource.match(/<a\b[^>]*\bhref="([^"]+)"[^>]*\bdata-open-science-pack\b/);
assert.ok(fallbackHref,'Actual lesson resource entry exists');
const lessonUrl=origin+'/Lessons/'+fallbackLesson.online_path;
assert.equal(resourceFallbackUrl(fallbackHref[1],lessonUrl,fallbackLesson.id),new URL('resources/'+fallbackLesson.id+'.html',lessonUrl).href);
fallbackUrlControls.push({name:'actual-resource-entry',expected:'PASS',observed:'PASS',passed:true});
console.log(JSON.stringify(fallbackUrlControls[fallbackUrlControls.length-1]));
assert.throws(()=>resourceFallbackUrl('#mbm-science-pack',lessonUrl,fallbackLesson.id),{code:'ERR_ASSERTION'});
fallbackUrlControls.push({name:'planted-hash-resource-entry-rejected',expected:'FAIL',observed:'FAIL',passed:true});
console.log(JSON.stringify(fallbackUrlControls[fallbackUrlControls.length-1]));
(async()=>{
  const browser=await chromium.launch({headless:true,channel:args.channel||(process.env.CI?'chrome':undefined)});
  const context=await browser.newContext();
  await context.route('**/*',async route=>{
    const url=new URL(route.request().url());
    if(url.origin!==origin)return route.abort('blockedbyclient');
    if(url.pathname===currentDocument?.path)return route.fulfill({contentType:'text/html',body:currentDocument.html});
    const file=path.resolve(root,'.'+decodeURIComponent(url.pathname.replace(/^\/Lessons/,'')));
    if(!file.startsWith(root+path.sep)||!fs.existsSync(file))return route.fulfill({status:404,body:'Missing local control asset'});
    await route.fulfill({contentType:path.extname(file)==='.svg'?'image/svg+xml':'application/octet-stream',body:fs.readFileSync(file)});
  });
  const page=await context.newPage();
  async function run(name,fixture,mutate,expected){
    assert.equal(crypto.createHash('sha256').update(fixture.html).digest('hex'),fixture.fragmentSha256,'Actual source fragment identity');
    currentDocument={path:'/Lessons/'+fixture.sourcePath,html:'<!doctype html><section id="control">'+fixture.html+'</section>'};
    await page.goto(origin+currentDocument.path,{waitUntil:'domcontentloaded'});
    await page.locator('#control img').evaluateAll(nodes=>Promise.all(nodes.map(n=>n.decode())));
    if(mutate)await page.evaluate(mutate);
    let verdict='PASS',error=null;
    try{await assertRenderedModel(page.locator('#control figure'));}catch(e){verdict='FAIL';error=e.message;}
    const passed=verdict===expected;
    results.push({name,expected,observed:verdict,passed,error,sourcePath:fixture.sourcePath,sourceCommit:fixture.sourceCommit});
    console.log(JSON.stringify(results[results.length-1]));
    assert.equal(passed,true,name+': a planted defect must redden and an actual model must render');
  }
  try{
    for(const fixture of fixtures.inlineModels)await run('actual-inline/'+fixture.name,fixture,null,'PASS');
    await run('existing-real-img',fixtures.oldImage,null,'PASS');
    const fixture=fixtures.inlineModels[0];
    await run('same-document-absolute-gradient-renders',fixture,()=>{
      const svg=document.querySelector('#control svg');
      svg.innerHTML='<defs><linearGradient id="control-gradient"><stop stop-color="red"/><stop offset="1" stop-color="blue"/></linearGradient></defs><rect width="640" height="360"/>';
      svg.querySelector('rect').style.fill='url("'+document.URL+'#control-gradient")';
    },'PASS');
    await run('neither-img-nor-svg',fixture,()=>document.querySelector('#control figure').replaceChildren(),'FAIL');
    await run('missing-svg',fixture,()=>document.querySelector('#control svg').remove(),'FAIL');
    await run('empty-svg-retains-dimensions-and-defs',fixture,()=>{
      for(const child of [...document.querySelector('#control svg').children])if(!['title','desc','defs'].includes(child.tagName))child.remove();
    },'FAIL');
    await run('broken-svg-path',fixture,()=>document.querySelector('#control svg').innerHTML='<path d="BROKEN_PATH"/>','FAIL');
    await run('unresolved-svg-fragment',fixture,()=>document.querySelector('#control svg').innerHTML='<use href="#missing-model"/>','FAIL');
    await run('unresolved-absolute-svg-fragment',fixture,()=>{
      document.querySelector('#control svg rect').style.fill='url("'+document.URL+'#missing-model")';
    },'FAIL');
    await run('external-svg-fragment',fixture,()=>{
      document.querySelector('#control svg rect').style.fill='url("https://unreviewed.invalid/model.svg#external")';
    },'FAIL');
    await run('broken-img-still-fails',fixtures.oldImage,async()=>{
      const image=document.querySelector('#control img');image.src='data:image/svg+xml,BROKEN';
      try{await image.decode();}catch{ /* Wait for this replacement to fail before testing its state. */ }
    },'FAIL');
    await run('restored-actual-inline-after-negatives',fixture,null,'PASS');
    await run('restored-existing-real-img-after-negatives',fixtures.oldImage,null,'PASS');
  }finally{
    await browser.close();fs.mkdirSync(path.dirname(out),{recursive:true});
    fs.writeFileSync(out,JSON.stringify({schema:'s1b-no-video-model-controls-result-v1',cases:results.length,passed:results.filter(r=>r.passed).length,fallbackUrlControls,results},null,2)+'\n');
  }
  console.log(JSON.stringify({kind:'model-controls-summary',cases:results.length,passed:results.filter(r=>r.passed).length,fallbackUrlControls}));
  assert.ok(results.every(r=>r.passed),'Every planted defect must redden; every actual model must render');
})().catch(error=>{console.error(error);process.exitCode=1;});
