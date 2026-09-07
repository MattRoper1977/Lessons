/* Candidate browser controls; publication proof is a separate release gate. */
'use strict';
const {chromium}=require('playwright');
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const source=path.resolve(process.argv[2]),publication=path.resolve(process.argv[3]),out=path.resolve(process.argv[4]||'audit-output/hc3-glitch');
const routePath='/Lessons/Games/Glitch_Clash.html',origin='https://www.madebymatt-play.uk',key='glitchclash_save';
const html=fs.readFileSync(source,'utf8').replaceAll('https://madebymatt.uk','https://madebymatt-play.uk').replace('window.__GCstart = (i,o)=>startBattle(i,o);','window.__fixtureChoose=chooseCampaign;window.__GCstart = (i,o)=>startBattle(i,o);');
const legacyHTML=fs.readFileSync(path.join(publication,routePath),'utf8');
const seed={v:3,owned:['stryke','halo','brik'],dups:{stryke:2},team:['stryke','halo','brik'],cleared:[],xp:123,stickers:{},settings:{calm:false,motion:'auto',hc:false,cb:false},dailyDone:'',weeklyDone:'',tutorialDone:false,seen:{},stats:{wins:0,clashWins:0}};
const fragment=value=>'mbm_import='+Buffer.from(typeof value==='string'?value:JSON.stringify(value)).toString('base64url');
const results=[];let browser;
const types={'.js':'text/javascript','.css':'text/css','.json':'application/json','.svg':'image/svg+xml','.html':'text/html','.png':'image/png','.jpg':'image/jpeg','.woff2':'font/woff2'};
async function fixture({width=390,existing=null,candidate=html,denied=false,abort=false}={}){
 const context=await browser.newContext({viewport:{width,height:844},isMobile:width<600,hasTouch:width<600});
 const errors=[],requests=[];
 await context.addInitScript(({key,existing,denied,abort})=>{
  if(existing!==null&&localStorage.getItem(key)===null)localStorage.setItem(key,existing);
  window.__fixtureRestoreIDB=()=>{};
  if(denied){const original=IDBFactory.prototype.open;IDBFactory.prototype.open=function(){throw new DOMException('Denied','SecurityError');};window.__fixtureRestoreIDB=()=>{IDBFactory.prototype.open=original;};}
  if(abort){const original=IDBObjectStore.prototype.add;IDBObjectStore.prototype.add=function(...args){const request=original.apply(this,args);this.transaction.abort();return request;};window.__fixtureRestoreIDB=()=>{IDBObjectStore.prototype.add=original;};}
 },{key,existing,denied,abort});
 await context.route('**/*',async request=>{
  const url=new URL(request.request().url());
  if(url.origin!==origin){requests.push('unexpected origin '+url.href);return request.abort();}
  if(url.pathname===routePath)return request.fulfill({status:200,contentType:'text/html',body:url.searchParams.has('fixture-legacy')?legacyHTML:candidate});
  let filePath=path.resolve(publication,'.'+decodeURIComponent(url.pathname));
  if(!filePath.startsWith(publication+path.sep)){requests.push('path escape');return request.abort();}
  if(fs.existsSync(filePath)&&fs.statSync(filePath).isDirectory())filePath=path.join(filePath,'index.html');
  if(!fs.existsSync(filePath)){requests.push('missing '+url.pathname);return request.fulfill({status:404,body:'Missing fixture asset'});}
  return request.fulfill({status:200,contentType:types[path.extname(filePath)]||'application/octet-stream',body:fs.readFileSync(filePath)});
 });
 async function page(hash=fragment(seed),legacy=false){
  const p=await context.newPage();p.on('pageerror',e=>errors.push(e.message));
  await p.goto(origin+routePath+(legacy?'?fixture-legacy=1':'')+'#keep=one'+(hash?'&'+hash:''),{waitUntil:'load'});
  await settle(p);return p;
 }
 return {context,page,errors,requests,async finish(name,details={}){assert.deepEqual(errors,[],name+' page errors');assert.deepEqual(requests,[],name+' asset failures');results.push({name,width,...details,errors,requests});await context.close();}};
}
async function settle(page){
 await page.waitForFunction(()=>typeof window.__GCsave==='function'&&!document.querySelector('#campaign-waiting[open]')&&(!window.__GCcampaign||!window.__GCcampaign()?.pending));
}
async function state(page){return page.evaluate(async key=>({legacy:localStorage.getItem(key),memory:window.__GCsave(),campaign:window.__GCcampaign?.(),records:await campaignRepository.list(),hash:location.hash,text:document.body.textContent,home:!!document.querySelector('#scr-home.active')}),key);}
async function settings(page){
 if(!await page.locator('#ov-settings').evaluate(e=>e.classList.contains('show')))await page.locator('.screen.active [data-open="settings"]').click();
 await page.locator('#calmtoggle').waitFor({state:'visible'});
}
async function saveXP(page,xp){
 // The existing native harness seam seeds state. Persistence uses a real UI action.
 await page.evaluate(xp=>{window.__GCsave().xp=xp;},xp);await settings(page);await page.locator('#calmtoggle').click();await settle(page);
}
async function tabTo(page,id){
 for(let i=0;i<45;i++){await page.keyboard.press('Tab');if(await page.evaluate(id=>document.activeElement?.id===id,id))return;}
 throw Error('Real Tab walk did not reach '+id);
}
async function acceptedCase(name,options={}){
 const f=await fixture(options),p=await f.page(),s=await state(p);
 assert.equal(s.memory.xp,123);assert.equal(s.records.length,1);assert.equal(JSON.parse(s.records[0].save).xp,123);
 assert.deepEqual(JSON.parse(s.records[0].save).team,seed.team);assert.equal(s.legacy,options.existing??null);
 assert(s.home&&!s.hash.includes('mbm_import')&&s.hash.includes('keep=one'));
 await settings(p);assert(await p.locator('#campaignretrybtn').isHidden(),'Idle saved campaigns must not show Retry');await tabTo(p,'campaignsbtn');await p.keyboard.press('Enter');await p.locator('[data-campaign-id]').waitFor();
 await p.screenshot({path:path.join(out,name+'-'+(options.width||390)+'.png')});
 await f.finish(name,{records:1,legacyUnchanged:true,realTab:true});
}
async function conflictCase(candidate=html){
 const initial=JSON.stringify({...seed,xp:9}),f=await fixture({existing:initial,candidate});
 try{
  const old=await f.page('',true),a=await f.page();
  await saveXP(old,999);const before=await old.evaluate(key=>localStorage.getItem(key),key);
  const b=await f.page(''); // Both current documents hold the same record revision.
  await Promise.all([saveXP(a,200),saveXP(b,300)]);
  let sa=await state(a),sb=await state(b);
  assert.equal(sa.legacy,before);assert.equal(sb.legacy,before);assert.equal(sa.records.length,2);
  assert.notEqual(sa.campaign.id,sb.campaign.id);assert.deepEqual(sa.records.map(r=>JSON.parse(r.save).xp).sort((a,b)=>a-b),[200,300]);
  // A queued burst follows the branch it created; it cannot change the other tab's identity.
  await b.evaluate(()=>{window.__GCsave().xp=301;document.querySelector('#motiontoggle').click();window.__GCsave().xp=302;document.querySelector('#motiontoggle').click();});await settle(b);
  sb=await state(b);assert.equal(sb.records.length,2);assert.equal(JSON.parse(sb.records.find(r=>r.id===sb.campaign.id).save).xp,302);
  await a.reload();await settle(a);assert.equal((await state(a)).records.length,2);assert.equal((await state(a)).campaign.id,sa.campaign.id);assert.equal((await state(a)).memory.xp,200);
  await settings(a);await a.locator('#campaignsbtn').click();await a.locator('[data-campaign-id]').first().waitFor();
  assert.equal(await a.locator('[data-campaign-id]').count(),2);
  const keptId=sa.campaign.id;await a.locator('[data-campaign-id="'+keptId+'"]').click();await settle(a);
  assert.equal((await state(a)).memory.xp,200);assert.equal((await state(a)).legacy,before);
  await f.finish('old tab plus concurrent imported campaigns',{legacyUnchanged:true,records:2,queuedWrites:true,selection:true});
 }catch(error){await f.context.close();throw error;}
}
(async()=>{
 fs.mkdirSync(out,{recursive:true});browser=await chromium.launch({args:['--use-gl=swiftshader','--enable-unsafe-swiftshader']});
 for(const width of [390,1280])await acceptedCase('accepted',{width});
 await acceptedCase('existing legacy retained',{existing:JSON.stringify({...seed,xp:9})});
 await conflictCase();
 const planted=html.replace('if(campaignWriter){\n    return campaignWriter.write(snapshot)','if(false && campaignWriter){\n    return campaignWriter.write(snapshot)');assert.notEqual(planted,html);
 await assert.rejects(()=>conflictCase(planted),/strictly equal|Expected values|records/);
 await conflictCase();
 results.push({name:'persistence routing firing control',real:'PASS',planted:'FAIL',restored:'PASS'});
 for(const [name,value] of [['null',null],['array',[]],['wrong version',{...seed,v:4}],['unknown card',{...seed,owned:['toString'],team:['toString']}],['invalid statistic',{...seed,stats:{...seed.stats,bestCombo:'not-a-number'}}],['prototype',{...seed,dups:JSON.parse('{"__proto__":{"x":1}}')}],['oversized',{...seed,extra:'x'.repeat(32768)}],['malformed','{']]){
  const f=await fixture(),p=await f.page(fragment(value)),s=await state(p);assert.equal(s.records.length,0);assert.equal(s.legacy,null);assert(!s.hash.includes('mbm_import'));assert.equal(s.memory.xp,0);await f.finish('reject '+name);
 }
 for(const options of [{denied:true},{abort:true}]){
  const f=await fixture({...options,existing:JSON.stringify({...seed,xp:9})}),p=await f.page();
  const s=await p.evaluate(key=>({legacy:JSON.parse(localStorage.getItem(key)),xp:__GCsave().xp,hash:location.hash,campaign:__GCcampaign()}),key);
  assert.equal(s.xp,9);assert.equal(s.legacy.xp,9);assert.equal(s.campaign,null);assert(!s.hash.includes('mbm_import'));
  await p.evaluate(()=>__fixtureRestoreIDB());assert.equal((await state(p)).records.length,0);await f.finish(options.denied?'denied persistence':'aborted transaction');
 }
 {
  const f=await fixture(),p=await f.page(''),s=await state(p);assert.equal(s.records.length,0);assert.equal(s.legacy,null);assert.equal(s.hash,'#keep=one');await f.finish('no transfer');
 }
 for(const denied of [false,true]){
  const existing=JSON.stringify({...seed,xp:9}),f=await fixture({denied,existing}),p=await f.page('');
  await p.locator('#importfile').setInputFiles({name:'glitch-clash-save.json',mimeType:'application/json',buffer:Buffer.from(JSON.stringify({...seed,xp:321,extra:'x'.repeat(40000)}))});
  await p.waitForFunction(()=>__GCsave().xp===321);await settle(p);
  assert.equal(await p.evaluate(key=>localStorage.getItem(key),key),existing);
  if(denied){
   assert.equal(await p.evaluate(()=>__GCcampaign().volatile),true);await settings(p);assert(await p.locator('#campaignretrybtn').isVisible());
   await p.evaluate(()=>__fixtureRestoreIDB());await p.locator('#campaignretrybtn').click();await settle(p);
  }
  const s=await state(p);assert.equal(s.records.length,1);assert.equal(JSON.parse(s.records[0].save).xp,321);assert.equal(s.legacy,existing);
  await f.finish(denied?'native file memory fallback and retry':'ordinary native oversized file',{legacyUnchanged:true,nativeFileBytes:40000});
 }
 {
  const f=await fixture(),p=await f.page();
  await p.evaluate(()=>{const original=IDBObjectStore.prototype.put;IDBObjectStore.prototype.put=function(){throw new DOMException('Quota','QuotaExceededError');};window.__fixtureRestoreIDB=()=>{IDBObjectStore.prototype.put=original;};});
  await saveXP(p,444);assert.equal(await p.evaluate(()=>__GCcampaign().failed),true);assert(await p.locator('#campaignretrybtn').isVisible());
  assert.equal(JSON.parse((await state(p)).records[0].save).xp,123);
  await p.evaluate(()=>__fixtureRestoreIDB());await p.locator('#campaignretrybtn').click();await settle(p);
  const s=await state(p);assert.equal(s.campaign.failed,false);assert.equal(JSON.parse(s.records[0].save).xp,444);await f.finish('failed save retained and explicit retry');
 }
 async function openRing(p){
  await p.evaluate(()=>{
   window.__GCstart(1,{__scened:true});const b=__GC();
   b.team[b.active].en=100;b.glitch.en=100;
   b.team[b.active].hp=b.team[b.active].maxhp=1000;b.glitch.hp=b.glitch.maxhp=1000;
   window.__fixtureAI=Engine.aiChoose;Engine.aiChoose=()=> 'guard';
  });
  await p.locator('#actions [data-key="3"]').click();
  await p.evaluate(()=>{const b=__GC();b.team[b.active].en=100;b.glitch.en=100;Engine.aiChoose=()=> 'special';});
  await p.locator('#actions [data-key="4"]').click();
  await p.evaluate(()=>{Engine.aiChoose=window.__fixtureAI;});
  await p.locator('#ov-ring.show').waitFor();
 }
 {
  const f=await fixture(),p=await f.page(),before=await state(p);
  await openRing(p);await p.locator('#ringtap').click();
  await p.locator('#clash.show').waitFor();await p.waitForFunction(()=>document.querySelector('#clashresult').textContent.length>0);
  await p.locator('#clashok').click();await settle(p);
  assert.equal(await p.evaluate(()=>__GC().usedClash),true);
  assert(await p.evaluate(()=>__GC().turn>1));assert.equal((await state(p)).campaign.id,before.campaign.id);
  assert.equal((await state(p)).legacy,before.legacy);await f.finish('normal unswitched timing ring still completes');
 }
 {
  const f=await fixture(),p=await f.page();
  await openRing(p);await p.keyboard.press('Escape');
  await p.locator('#quitbtn').click();await p.locator('#quitbtn').click();
  const other=await p.evaluate(async seed=>{const r=await campaignRepository.create(JSON.stringify({...seed,xp:555}));return r.id;},seed);
  await settings(p);await p.locator('#campaignsbtn').click();await p.locator('[data-campaign-id="'+other+'"]').click();await settle(p);
  const before=await state(p);
  await p.keyboard.press('Enter');await p.keyboard.press('Space');
  // Observe beyond the old normal ring's 3*1300 ms deadline and completion delay.
  await p.waitForTimeout(4700);
  const after=await state(p);assert.equal(after.memory.xp,555);assert.deepEqual(after.records,before.records);
  assert.equal(await p.evaluate(()=>__GC()),null);assert.equal(after.legacy,before.legacy);
  await f.finish('old timing ring cannot reward or continue a selected campaign');
 }
 {
  const f=await fixture(),p=await f.page();await p.evaluate(()=>__GCstart(1,{__scened:true}));
  const target=p.locator('#pf');
  const box=await target.boundingBox();assert(box,'Native fighter card missing');
  await p.mouse.move(box.x+box.width/2,box.y+box.height/2);await p.mouse.down();
  await p.evaluate(async seed=>{const r=await campaignRepository.create(JSON.stringify({...seed,xp:666}));await __fixtureChoose(r.id);},seed);
  await p.mouse.up();await p.waitForTimeout(250);await settle(p);
  assert.equal((await state(p)).memory.xp,666);assert.equal(await p.evaluate(()=>__GC()),null);
  await f.finish('captured native pointer cancelled on campaign adoption');
 }
 console.log('Browser controls real PASS / planted legacy-routing defect FAIL / restored PASS; cases '+results.length);
 fs.writeFileSync(path.join(out,'receiver-browser.json'),JSON.stringify({scope:'Candidate fixtures, actual Chromium tabs and native UI saves; baseline publication assets; not live proof',status:'PASS',results},null,2)+'\n');
})().catch(error=>{fs.mkdirSync(out,{recursive:true});fs.writeFileSync(path.join(out,'receiver-browser.json'),JSON.stringify({status:'FAIL',error:String(error.stack),results},null,2)+'\n');console.error(error);process.exitCode=1;}).finally(async()=>{if(browser)await browser.close();});
