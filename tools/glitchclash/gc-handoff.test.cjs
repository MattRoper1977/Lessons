/* Native campaign handoff controls; real game code, no source eval of pupil data. */
'use strict';
const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm'),assert=require('node:assert/strict');
const target=path.resolve(process.argv[2]||path.join(__dirname,'../../Games/Glitch_Clash.html'));
const html=fs.readFileSync(target,'utf8');
const source=[...html.matchAll(/<script\b[^>]*>([\s\S]*?)<\/script>/gi)].map(m=>m[1]).find(s=>s.includes('const SAVE_VERSION = 3;'));
assert(source,'Native game script missing');
function load(script=source){
 const context={TextEncoder,TextDecoder,URL,URLSearchParams,atob,btoa};
 vm.createContext(context);vm.runInContext(script,context);
 return vm.runInContext('({CampaignImport,STARTERS})',context);
}
const {CampaignImport:api,STARTERS}=load();
const seed={v:3,owned:[...STARTERS],dups:{},team:[...STARTERS],cleared:[],xp:123,stickers:{},settings:{calm:false,motion:'auto',hc:false,cb:false},dailyDone:'',weeklyDone:'',tutorialDone:false,seen:{},stats:{wins:0,clashWins:0}};
const base='https://www.madebymatt-play.uk/Lessons/Games/Glitch_Clash.html';
const encode=text=>Buffer.from(text,'utf8').toString('base64url');
const link=value=>base+'#mbm_import='+encode(JSON.stringify(value));
function storage(initial={}){const data=new Map(Object.entries(initial));return {getItem:k=>data.has(k)?data.get(k):null,setItem:(k,v)=>data.set(k,v),removeItem:k=>data.delete(k),data};}
function roundtrip(candidate){const db=storage();const result=candidate.receive(link(seed),db);assert.equal(result.xp,123);assert.equal(JSON.parse(db.getItem('glitchclash_save')).xp,123);}
roundtrip(api);
const planted=source.replace('storage.setItem(KEY,value);','/* planted missing persistent write */');
assert.notEqual(planted,source);
assert.throws(()=>roundtrip(load(planted).CampaignImport));
roundtrip(load().CampaignImport);
console.log('CONTROL real PASS / planted dropped write FAIL / restored PASS');
assert.equal(api.receive(base+'#keep=one',storage()),null);
assert.equal(api.cleanURL(base+'?q=ok#keep=one&mbm_import=abc&other=two'),base+'?q=ok#keep=one&other=two');
assert.equal(api.cleanURL(base+'#plain-anchor'),null);
for(const value of [null,[],{}, {...seed,v:4},{...seed,xp:null},{...seed,team:'wrong'},{...seed,settings:null},{...seed,owned:['toString'],team:['toString']},JSON.parse(JSON.stringify(seed).replace('"dups":{}','"dups":{"__proto__":{"bad":true}}'))]){
 const db=storage();assert.throws(()=>api.receive(link(value),db));assert.equal(db.data.size,0);
}
for(const key of ['wins','clashWins','bestCombo','dmgDealt','bosses','nohit','glitches','battles','playMs','bestEndless']) assert.throws(()=>api.receive(link({...seed,stats:{...seed.stats,[key]:'not-a-number'}}),storage()));
let deep={};for(let i=0;i<30;i++)deep={child:deep};
assert.throws(()=>api.receive(link({...seed,extra:deep}),storage()));
for(const url of [base+'#mbm_import=!',base+'#mbm_import='+encode('{'),base+'#mbm_import='+Buffer.from([0xff]).toString('base64url'),link(seed)+'&mbm_import=again',link({...seed,extra:'x'.repeat(32768)}),link(seed).replace('https:','http:'),link(seed).replace('www.madebymatt-play.uk','madebymatt.uk'),link(seed).replace('Glitch_Clash.html','glitch_clash.html')]){
 const db=storage();assert.throws(()=>api.receive(url,db));assert.equal(db.data.size,0);
}
const existing='{"keep":"exact previous bytes"}';
const db=storage({glitchclash_save:existing,unrelated:'preserve'});
assert.throws(()=>api.receive(link(seed),db));assert.equal(db.getItem('glitchclash_save'),existing);assert.equal(db.getItem('unrelated'),'preserve');
const noWrite=storage();noWrite.setItem=()=>{};
assert.throws(()=>api.receive(link(seed),noWrite));assert.equal(noWrite.getItem('glitchclash_save'),null);
const denied=storage();denied.getItem=()=>{throw Error('denied')};
assert.throws(()=>api.receive(link(seed),denied));assert.equal(denied.data.size,0);
const quota=storage({unrelated:'keep'});quota.setItem=(key,value)=>{quota.data.set(key,value);throw Error('quota')};
assert.throws(()=>api.receive(link(seed),quota));assert.equal(quota.getItem('glitchclash_save'),null);assert.equal(quota.getItem('unrelated'),'keep');
const concurrent=storage();concurrent.setItem=()=>{concurrent.data.set('glitchclash_save',existing);throw Error('another writer')};
assert.throws(()=>api.receive(link(seed),concurrent));assert.equal(concurrent.getItem('glitchclash_save'),existing);
const unconfirmed=storage();unconfirmed.setItem=(key,value)=>{unconfirmed.data.set(key,value);throw Error('quota')};unconfirmed.removeItem=()=>{throw Error('denied rollback')};
assert.throws(()=>api.receive(link(seed),unconfirmed),/reload before playing/);
// The ordinary native file path still accepts its existing raw format and sanitizer.
assert.equal(api.prepare(JSON.stringify(seed)).xp,123);
assert.equal(api.prepare(JSON.stringify({...seed,extra:'x'.repeat(40000)})).extra.length,40000);
console.log('Glitch campaign transport: persistence, rejection, cleanup and native file compatibility PASS');
