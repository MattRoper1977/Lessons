/* Native-format and transactional campaign controls against the real inline code. */
'use strict';
const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm'),assert=require('node:assert/strict');
const {IDBFactory,IDBObjectStore}=require('fake-indexeddb');
const target=path.resolve(process.argv[2]||path.join(__dirname,'../../Games/Glitch_Clash.html'));
const html=fs.readFileSync(target,'utf8');
const source=[...html.matchAll(/<script\b[^>]*>([\s\S]*?)<\/script>/gi)].map(m=>m[1]).find(s=>s.includes('const SAVE_VERSION = 3;'));
assert(source,'Native game script missing');
function storage(initial={}){
  const data=new Map(Object.entries(initial)),writes=[];
  return {getItem:key=>data.get(key)??null,setItem:(key,value)=>{writes.push(key);data.set(key,value);},removeItem:key=>{writes.push(key);data.delete(key);},data,writes};
}
function load(script=source,{factory=new IDBFactory(),legacy=storage()}={}){
  const context={TextEncoder,TextDecoder,URL,URLSearchParams,atob,btoa,setTimeout,clearTimeout,indexedDB:factory,localStorage:legacy};
  vm.createContext(context);vm.runInContext(script,context);
  return {...vm.runInContext('({CampaignImport,CampaignStore,campaignRepository,STARTERS})',context),context,legacy};
}
const seed={v:3,owned:['stryke','halo','brik'],dups:{stryke:2},team:['stryke','halo','brik'],cleared:[],xp:123,stickers:{},settings:{calm:false,motion:'auto',hc:false,cb:false},dailyDone:'',weeklyDone:'',tutorialDone:false,seen:{},stats:{wins:0,clashWins:0}};
const base='https://www.madebymatt-play.uk/Lessons/Games/Glitch_Clash.html';
const encode=text=>Buffer.from(text,'utf8').toString('base64url');
const link=value=>base+'#mbm_import='+encode(JSON.stringify(value));
const native=xp=>JSON.stringify({...seed,xp});
async function roundtrip(game){
  const record=await game.CampaignImport.receive(link(seed),game.campaignRepository);
  assert.equal(JSON.parse(record.save).xp,123);
  assert.equal(JSON.parse((await game.campaignRepository.read(record.id)).save).xp,123);
  assert.equal((await game.campaignRepository.list()).length,1);
  assert.equal(game.legacy.writes.length,0);
  return record;
}
(async()=>{
  await roundtrip(load());
  const planted=source.replace('const request=store.add(record);','const request=store.get(0); /* planted missing write */');
  assert.notEqual(planted,source);
  await assert.rejects(()=>roundtrip(load(planted)));
  await roundtrip(load());
  console.log('CONTROL real PASS / planted missing record FAIL / restored PASS');

  const selection=load().CampaignStore, sharedSelection=storage(),tabA=storage(),tabB=storage();
  selection.prefer(1,sharedSelection,tabA);selection.prefer(2,sharedSelection,tabB);
  assert.equal(selection.preferred(sharedSelection,tabA),1);assert.equal(selection.preferred(sharedSelection,tabB),2);
  assert.equal(selection.preferred(sharedSelection,storage()),2);
  selection.prefer(null,sharedSelection,tabA);assert.equal(selection.preferred(sharedSelection,tabA),null);
  const game=load(),api=game.CampaignImport,repo=game.campaignRepository;
  assert.equal(await api.receive(base+'#keep=one',repo),null);
  assert.equal(api.cleanURL(base+'?q=ok#keep=one&mbm_import=abc&other=two'),base+'?q=ok#keep=one&other=two');
  assert.equal(api.cleanURL(base+'#plain-anchor'),null);
  const invalid=[null,[],{}, {...seed,v:4},{...seed,xp:null},{...seed,team:'wrong'},{...seed,settings:null},{...seed,owned:['toString'],team:['toString']}];
  invalid.push(JSON.parse(JSON.stringify(seed).replace('"dups":{"stryke":2}','"dups":{"__proto__":{"bad":true}}')));
  for(const key of ['wins','clashWins','bestCombo','dmgDealt','bosses','nohit','glitches','battles','playMs','bestEndless']) invalid.push({...seed,stats:{...seed.stats,[key]:'not-a-number'}});
  let deep={};for(let i=0;i<30;i++)deep={child:deep};invalid.push({...seed,extra:deep});
  for(const value of invalid) await assert.rejects(()=>api.receive(link(value),repo));
  for(const url of [base+'#mbm_import=!',base+'#mbm_import='+encode('{'),base+'#mbm_import='+Buffer.from([0xff]).toString('base64url'),link(seed)+'&mbm_import=again',link({...seed,extra:'x'.repeat(32768)}),link(seed).replace('https:','http:'),link(seed).replace('www.madebymatt-play.uk','madebymatt.uk'),link(seed).replace('Glitch_Clash.html','glitch_clash.html')]) await assert.rejects(()=>api.receive(url,repo));
  assert.equal((await repo.list()).length,0);

  // Old tabs can write their legacy campaign before, during and after import.
  const legacy=storage({glitchclash_save:native(9),unrelated:'keep'});
  const isolated=load(source,{legacy});
  const receiving=isolated.CampaignImport.receive(link(seed),isolated.campaignRepository);
  legacy.setItem('glitchclash_save',native(999));
  const imported=await receiving;
  const first=isolated.campaignRepository.writer(imported);
  const saving=first.write(native(234));legacy.setItem('glitchclash_save',native(1000));await saving;
  assert.equal(legacy.getItem('glitchclash_save'),native(1000));assert.equal(legacy.getItem('unrelated'),'keep');
  assert.deepEqual(legacy.writes,['glitchclash_save','glitchclash_save']);

  // Both documents begin at the same revision. The second atomic transaction
  // branches; its next queued snapshot follows that branch without extra copies.
  const shared=new IDBFactory(),a=load(source,{factory:shared}),b=load(source,{factory:shared});
  const original=await a.campaignRepository.create(native(123));
  const wa=a.campaignRepository.writer(original),wb=b.campaignRepository.writer(await b.campaignRepository.read(original.id));
  await Promise.all([wa.write(native(400)),wb.write(native(500)),wb.write(native(501))]);
  const branches=await a.campaignRepository.list();
  assert.equal(branches.length,2);assert.notEqual(wa.state().id,wb.state().id);
  assert.deepEqual(Array.from(branches,x=>JSON.parse(x.save).xp).sort((x,y)=>x-y),[400,501]);
  assert.equal((await wb.flush()).parentId,original.id);assert.equal(wb.state().pending,0);
  for(let i=0;i<5;i++) await b.campaignRepository.read(wb.state().id);
  assert.equal((await b.campaignRepository.list()).length,2);

  const other=await a.campaignRepository.create(native(700));
  const otherWriter=a.campaignRepository.writer(other);
  await Promise.all([wa.write(native(401)),otherWriter.write(native(701))]);
  assert.equal(JSON.parse((await a.campaignRepository.read(otherWriter.state().id)).save).xp,701);
  assert.equal(JSON.parse((await a.campaignRepository.read(wa.state().id)).save).xp,401);

  // Abort after add rolls back atomically, without read/delete compensation.
  const before=JSON.stringify(await a.campaignRepository.list());
  const originalAdd=IDBObjectStore.prototype.add;
  try{
    IDBObjectStore.prototype.add=function(...args){const request=originalAdd.apply(this,args);this.transaction.abort();return request;};
    await assert.rejects(()=>a.campaignRepository.create(native(800)));
  }finally{IDBObjectStore.prototype.add=originalAdd;}
  assert.equal(JSON.stringify(await a.campaignRepository.list()),before);
  const originalPut=IDBObjectStore.prototype.put;
  try{
    IDBObjectStore.prototype.put=function(){throw new DOMException('Quota','QuotaExceededError');};
    await assert.rejects(()=>wa.write(native(900)));assert.equal(wa.state().failed,true);
    await assert.rejects(()=>wa.flush());
  }finally{IDBObjectStore.prototype.put=originalPut;}
  assert.equal(JSON.parse((await a.campaignRepository.read(wa.state().id)).save).xp,401);
  await wa.write(native(402));assert.equal(wa.state().failed,false);

  const denied=load(source,{factory:{open(){throw Error('denied');}}});
  await assert.rejects(()=>denied.CampaignImport.receive(link(seed),denied.campaignRepository));
  assert.equal(denied.legacy.writes.length,0);
  const blockedFactory={open(){const request={};setTimeout(()=>request.onblocked(),0);return request;}};
  await assert.rejects(()=>load(source,{factory:blockedFactory}).campaignRepository.create(native(123)));
  assert.equal(api.prepare(JSON.stringify(seed)).xp,123);
  assert.equal(api.prepare(JSON.stringify({...seed,extra:'x'.repeat(40000)})).extra.length,40000);
  console.log('Native format, isolated legacy state, atomic branching, ordered queues, abort/quota/retry and rejection controls PASS');
})().catch(error=>{console.error(error);process.exitCode=1;});
