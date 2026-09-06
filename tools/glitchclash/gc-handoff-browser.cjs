/* Native receiver browser fixtures. This does not claim that the candidate is live. */
'use strict';
const {chromium}=require('playwright');
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const source=path.resolve(process.argv[2]),publication=path.resolve(process.argv[3]),out=path.resolve(process.argv[4]||'audit-output/hc3-glitch');
const routePath='/Lessons/Games/Glitch_Clash.html',origin='https://www.madebymatt-play.uk',key='glitchclash_save';
const sourceHTML=fs.readFileSync(source,'utf8');
const html=sourceHTML.replaceAll('https://madebymatt.uk','https://madebymatt-play.uk');
const seed={v:3,owned:['stryke','halo','brik'],dups:{stryke:2},team:['stryke','halo','brik'],cleared:[],xp:123,stickers:{},settings:{calm:false,motion:'auto',hc:false,cb:false},dailyDone:'',weeklyDone:'',tutorialDone:false,seen:{},stats:{wins:0,clashWins:0}};
const fragment=value=>'mbm_import='+Buffer.from(typeof value==='string'?value:JSON.stringify(value)).toString('base64url');
const results=[];let browser;
const types={'.js':'text/javascript','.css':'text/css','.json':'application/json','.svg':'image/svg+xml','.html':'text/html','.png':'image/png','.jpg':'image/jpeg','.woff2':'font/woff2'};
async function run(name,{width=390,hash=fragment(seed),existing=null,quota=false,candidate=html,file=null}={}){
 const context=await browser.newContext({viewport:{width,height:844},isMobile:width<600,hasTouch:width<600});
 const errors=[],requests=[];
 await context.addInitScript(({key,existing,quota})=>{
  if(existing!==null)localStorage.setItem(key,existing);
  if(quota){const original=Storage.prototype.setItem;Storage.prototype.setItem=function(k,v){if(k===key)throw new DOMException('Quota','QuotaExceededError');return original.call(this,k,v);};}
 },{key,existing,quota});
 const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
 await page.route('**/*',async request=>{
  const url=new URL(request.request().url());
  if(url.origin!==origin){requests.push('unexpected origin '+url.href);return request.abort();}
  if(url.pathname===routePath)return request.fulfill({status:200,contentType:'text/html',body:candidate});
  let filePath=path.resolve(publication,'.'+decodeURIComponent(url.pathname));
  if(!filePath.startsWith(publication+path.sep)){requests.push('path escape');return request.abort();}
  if(fs.existsSync(filePath)&&fs.statSync(filePath).isDirectory())filePath=path.join(filePath,'index.html');
  if(!fs.existsSync(filePath)){requests.push('missing '+url.pathname);return request.fulfill({status:404,body:'Missing fixture asset'});}
  return request.fulfill({status:200,contentType:types[path.extname(filePath)]||'application/octet-stream',body:fs.readFileSync(filePath)});
 });
 await page.goto(origin+routePath+'#keep=one'+(hash?'&'+hash:''),{waitUntil:'load'});
 await page.waitForFunction(()=>typeof window.__GCsave==='function');
 if(file){await page.locator('#importfile').setInputFiles({name:'glitch-clash-save.json',mimeType:'application/json',buffer:Buffer.from(JSON.stringify(file))});await page.waitForFunction(xp=>window.__GCsave().xp===xp,file.xp);}
 const state=await page.evaluate(key=>({stored:localStorage.getItem(key),memory:window.__GCsave(),hash:location.hash,text:document.body.textContent,home:!!document.querySelector('#scr-home.active')}),key);
 assert.deepEqual(errors,[],name+' page errors');assert.deepEqual(requests,[],name+' asset failures');
 if(width===390&&name==='accepted')await page.screenshot({path:path.join(out,'receiver-phone.png')});
 if(width===1280)await page.screenshot({path:path.join(out,'receiver-desktop.png')});
 const result={name,width,stored:state.stored===null?null:JSON.parse(state.stored),memoryXP:state.memory.xp,hash:state.hash,home:state.home,errors,requests,text:state.text};
 results.push({...result,text:undefined});await context.close();return result;
}
function accepted(result){return JSON.stringify(result.stored?.owned)===JSON.stringify(seed.owned)&&JSON.stringify(result.stored?.team)===JSON.stringify(seed.team)&&result.stored?.dups.stryke===2&&result.stored?.xp===123&&result.memoryXP===123&&result.home&&!result.hash.includes('mbm_import')&&result.hash.includes('keep=one');}
(async()=>{
 fs.mkdirSync(out,{recursive:true});browser=await chromium.launch({args:['--use-gl=swiftshader','--enable-unsafe-swiftshader']});
 for(const width of [390,1280])assert(accepted(await run('accepted',{width})));
 const planted=html.replace('storage.setItem(KEY,value);','/* planted dropped write */');assert.notEqual(planted,html);
 const failed=await run('planted dropped persistence',{candidate:planted});
 assert(!accepted(failed));assert.equal(failed.stored,null);assert(failed.text.includes('could not keep the imported campaign'));
 assert(accepted(await run('restored')));
 for(const [name,value] of [['null',null],['array',[]],['wrong version',{...seed,v:4}],['unknown card',{...seed,owned:['toString'],team:['toString']}],['invalid optional statistic',{...seed,stats:{...seed.stats,bestCombo:'not-a-number'}}],['prototype',{...seed,dups:JSON.parse('{"__proto__":{"x":1}}')}],['oversized',{...seed,extra:'x'.repeat(32768)}],['malformed','{']]){
  const result=await run(name,{hash:fragment(value)});assert.equal(result.stored,null);assert(!result.hash.includes('mbm_import'));assert.equal(result.memoryXP,0);
 }
 const conflict=await run('existing campaign',{existing:JSON.stringify({...seed,xp:9})});assert.equal(conflict.stored.xp,9);assert.equal(conflict.memoryXP,9);assert(!conflict.hash.includes('mbm_import'));
 const quota=await run('quota',{quota:true});assert.equal(quota.stored,null);assert(!quota.hash.includes('mbm_import'));
 const empty=await run('no transfer',{hash:''});assert.equal(empty.stored,null);assert.equal(empty.hash,'#keep=one');
 const native=await run('ordinary native oversized file',{hash:'',file:{...seed,xp:321,extra:'x'.repeat(40000)}});assert.equal(native.stored.xp,321);assert.equal(native.memoryXP,321);
 console.log('Browser control real PASS / planted dropped persistence FAIL / restored PASS; receiver cases '+results.length);
 fs.writeFileSync(path.join(out,'receiver-browser.json'),JSON.stringify({scope:'Candidate receiver fixtures with baseline publication assets; not live publication proof',status:'PASS',results},null,2)+'\n');
})().catch(error=>{fs.mkdirSync(out,{recursive:true});fs.writeFileSync(path.join(out,'receiver-browser.json'),JSON.stringify({status:'FAIL',error:String(error.stack),results},null,2)+'\n');console.error(error);process.exitCode=1;}).finally(async()=>{if(browser)await browser.close();});
