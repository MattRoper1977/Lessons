// TL-2 Part A gates: A4-1..A4-4 save compatibility + A6 re-run subset, on a REAL http origin.
import { chromium } from 'playwright';
import http from 'http'; import fs from 'fs';
const EXE='/opt/pw-browsers/chromium-1194/chrome-linux/chrome';
const V101=process.argv[2], V102=process.argv[3];
const results=[]; const add=(group,name,pass,detail)=>results.push({group,name,pass,detail});

function serve(file){
  const html=fs.readFileSync(file);
  const s=http.createServer((q,r)=>{r.writeHead(200,{'Content-Type':'text/html; charset=utf-8'});r.end(html)});
  return new Promise(res=>s.listen(0,'127.0.0.1',()=>res({s,port:s.address().port})));
}
const browser=await chromium.launch({executablePath:EXE,args:['--no-sandbox','--disable-dev-shm-usage']});

async function open(file,opts){
  opts=opts||{};
  const seed=opts.seed||null;
  const legacy=opts.legacy||null;
  const viewport=opts.viewport||{width:1280,height:900};
  const {s,port}=await serve(file);
  const ctx=await browser.newContext({viewport});
  // Seed BEFORE any page script runs: first boot schedules setTimeout(saveNow,2400),
  // which would otherwise clobber a post-load setItem with default state.
  if(seed) await ctx.addInitScript(function(v){try{localStorage.setItem('mbm_town_life_v10',v)}catch(e){}},seed);
  if(legacy) await ctx.addInitScript(function(v){try{localStorage.removeItem('mbm_town_life_v10');localStorage.setItem('mbm_town_life_v01',v)}catch(e){}},legacy);
  const page=await ctx.newPage();
  const errs=[]; page.on('pageerror',e=>errs.push('pageerror: '+e.message));
  page.on('console',m=>{if(m.type()==='error')errs.push('console: '+m.text())});
  const url='http://127.0.0.1:'+port+'/townlife/?qa';
  await page.goto(url);
  await page.waitForFunction(function(){return window.__MBM_TOWN_LIFE_READY__===true},{timeout:30000});
  await page.waitForTimeout(400);
  return {page,ctx,errs,close:async function(){await ctx.close();s.close()}};
}

// ---------- build a genuine v1.0.1 mid-conversion save ----------
let midSave=null, v101Payout=null, v101Rate=null;
{
  const h=await open(V101);
  midSave = await h.page.evaluate(async function(){
    const QA=window.MBMTownLifeQA; QA.clearWelcome();
    QA.addBonds(320); QA.startLaundering();
    await new Promise(function(r){setTimeout(r,3000)});
    return localStorage.getItem('mbm_town_life_v10');
  });
  const p=JSON.parse(midSave);
  v101Rate=p.laundering?p.laundering.rate:null;
  add('fixture','v1.0.1 mid-conversion save written',
      !!p.laundering && p.laundering.amount===320,
      {version:p.version, laundering:p.laundering, dirtyBonds:p.dirtyBonds, bytes:midSave.length});
  v101Payout = await h.page.evaluate(async function(){
    const QA=window.MBMTownLifeQA; QA.collectLaundering();
    await new Promise(function(r){setTimeout(r,600)});
    return QA.getProgress().cash;
  });
  add('fixture','v1.0.1 reference payout recorded', typeof v101Payout==='number', {cash:v101Payout, rate:v101Rate});
  await h.close();
}

// ---------- A4-1 control: same seed, same method, through v1.0.1 ----------
let v101SeededPayout=null;
{
  const h=await open(V101,{seed:midSave});
  const r=await h.page.evaluate(async function(){
    const QA=window.MBMTownLifeQA;
    const before=QA.getProgress();
    QA.collectLaundering();
    await new Promise(function(r){setTimeout(r,600)});
    return {loaded:before.laundering, cash:QA.getProgress().cash};
  });
  v101SeededPayout=r.cash;
  add('A4-1 control','v1.0.1 loads the same seed (apples-to-apples baseline)', !!r.loaded, {laundering:r.loaded, cash:r.cash});
  await h.close();
}

// ---------- A4-1 ----------
{
  const h=await open(V102,{seed:midSave});
  const r=await h.page.evaluate(async function(){
    const QA=window.MBMTownLifeQA;
    const before=QA.getProgress();
    QA.collectLaundering();
    await new Promise(function(r){setTimeout(r,600)});
    const after=QA.getProgress();
    return {loadedLaundering:before.laundering, loadedBonds:before.dirtyBonds,
            cashAfter:after.cash, launderingAfter:after.laundering, bondsAfter:after.dirtyBonds,
            version:QA.getState().version};
  });
  add('A4-1','v1.0.1 mid-conversion save loads in v1.0.2', !!r.loadedLaundering, {laundering:r.loadedLaundering});
  add('A4-1','conversion resumes and completes', r.launderingAfter===null, {launderingAfter:r.launderingAfter});
  add('A4-1','payout identical to v1.0.1 (same seed, same method)', r.cashAfter===v101SeededPayout, {v102:r.cashAfter, v101_seeded:v101SeededPayout, v101_livesession:v101Payout});
  add('A4-1','loaded save reports v1.0.2 after migration', r.version==='1.0.2', {version:r.version});
  add('A4-1','no page errors', h.errs.length===0, {errors:h.errs});
  await h.close();
}

// ---------- A4-2 ----------
{
  const h=await open(V101);
  const seed=await h.page.evaluate(async function(){
    const QA=window.MBMTownLifeQA; QA.clearWelcome(); QA.addBonds(250);
    QA.buyBusiness('garage'); // triggers saveSoon(); garage alone => no synergy rate change
    await new Promise(function(r){setTimeout(r,3000)});
    return localStorage.getItem('mbm_town_life_v10');
  });
  await h.close();
  const p=JSON.parse(seed);
  add('A4-2','fixture: bonds>0 and no conversion', p.dirtyBonds>0 && !p.laundering, {dirtyBonds:p.dirtyBonds, laundering:p.laundering});
  const h2=await open(V102,{seed:seed});
  const r=await h2.page.evaluate(async function(){
    const QA=window.MBMTownLifeQA;
    QA.startLaundering();
    await new Promise(function(r){setTimeout(r,400)});
    const prog=QA.getProgress();
    const body=document.body.innerText||'';
    return {laundering:prog.laundering, bonds:prog.dirtyBonds,
            hasExchange:/Exchange/.test(body), hasWashworks:/Washworks/.test(body)};
  });
  add('A4-2','conversion starts in v1.0.2', !!r.laundering, {laundering:r.laundering});
  add('A4-2','no "Washworks" in rendered text after starting', r.hasWashworks===false, {hasWashworks:r.hasWashworks, hasExchange:r.hasExchange});
  add('A4-2','no page errors', h2.errs.length===0, {errors:h2.errs});
  await h2.close();
}

// ---------- A4-3 legacy normaliser ----------
{
  const h=await open(V102,{legacy:JSON.stringify({profile:'Legacy',cash:777})});
  const page=h.page; const errs=h.errs;
  const r=await page.evaluate(function(){
    const QA=window.MBMTownLifeQA; const st=QA.getState();
    return {profile:st.profile, cash:st.cash, schema:st.schema, version:st.version,
            v10Written: !!localStorage.getItem('mbm_town_life_v10'),
            v01Kept: !!localStorage.getItem('mbm_town_life_v01')};
  });
  add('A4-3','legacy v01 fixture funnels through the normaliser', r.profile==='Legacy'&&r.cash===777,
      {profile:r.profile, cash:r.cash, schema:r.schema, version:r.version});
  add('A4-3','normalised result persisted under v10', r.v10Written===true, {v10Written:r.v10Written});
  add('A4-3','legacy record not deleted', r.v01Kept===true, {v01Kept:r.v01Kept});
  add('A4-3','no page errors', errs.length===0, {errors:errs});
  await h.close();
}

// ---------- A4-4 ----------
{
  const h=await open(V102);
  const r=await h.page.evaluate(function(){return {role:window.MBMTownLifeQA.getState().role}});
  add('A4-4','fresh save default role is Resident', r.role==='Resident', {role:r.role});
  await h.close();
}

// ---------- A6 version + operations + labels ----------
{
  const h=await open(V102);
  const r=await h.page.evaluate(async function(){
    const QA=window.MBMTownLifeQA; QA.clearWelcome();
    const st=QA.getState();
    const out={stateVersion:st.version, statusVersion:window.__MBM_TOWN_LIFE_STATUS__.version,
               schema:st.schema, storage:window.__MBM_TOWN_LIFE_STATUS__.storage,
               origin:location.origin};
    QA.buyBusiness('garage'); QA.buyBusiness('laundry');
    out.synergies=QA.getSynergies?QA.getSynergies():null;
    QA.addBonds(320); QA.startLaundering();
    out.laundering=QA.getProgress().laundering;
    QA.collectLaundering();
    await new Promise(function(r){setTimeout(r,500)});
    out.afterCollect=QA.getProgress().laundering;
    QA.openLedger('businesses');
    await new Promise(function(r){setTimeout(r,500)});
    out.bodyText=(document.body.innerText||'');
    return out;
  });
  add('A6-static','runtime version declaration is 1.0.2', r.stateVersion==='1.0.2', {stateVersion:r.stateVersion});
  add('A6-startup','status reports 1.0.2', r.statusVersion==='1.0.2', {statusVersion:r.statusVersion});
  add('A6-static','save schema declaration remains 10', r.schema===10, {schema:r.schema});
  add('A6-ops','synergy still fires with garage+laundry owned', r.synergies && r.synergies.garageWashworks===true, {synergies:r.synergies});
  add('A6-ops','conversion starts under the new name', !!r.laundering, {laundering:r.laundering});
  add('A6-ops','conversion completes and clears', r.afterCollect===null, {afterCollect:r.afterCollect});
  add('A6-label','no player-visible "Washworks" in rendered text', !/Washworks/.test(r.bodyText), {found:/Washworks/.test(r.bodyText)});
  add('A6-label','ledger renders "Northstar Exchange"', /Northstar Exchange/.test(r.bodyText), {present:/Northstar Exchange/.test(r.bodyText)});
  add('D3','real-origin storage selects local mode (not volatile)', r.storage==='local', {storage:r.storage, origin:r.origin});
  add('A6-runtime','no unexpected runtime or console errors', h.errs.length===0, {errors:h.errs});
  await h.close();
}

// ---------- A6 390px overflow + 44px rendered touch census ----------
{
  const h=await open(V102,{viewport:{width:390,height:844}});
  const r=await h.page.evaluate(function(){
    const de=document.documentElement;
    const overflow=de.scrollWidth-de.clientWidth;
    const small=[];
    let scanned=0;
    document.querySelectorAll('button,[role="button"],a,input,select').forEach(function(el){
      const cs=getComputedStyle(el);
      if(cs.display==='none'||cs.visibility==='hidden'||cs.opacity==='0')return;
      const rc=el.getBoundingClientRect();
      if(rc.width===0&&rc.height===0)return;
      scanned++;
      if(rc.height<44) small.push({tag:el.tagName,id:el.id||null,h:+rc.height.toFixed(1),text:(el.textContent||'').trim().slice(0,24)});
    });
    return {scrollWidth:de.scrollWidth, clientWidth:de.clientWidth, overflow:overflow, visibleScanned:scanned, under44:small};
  });
  add('A6-a11y','390px: no horizontal document overflow', r.overflow<=0, {scrollWidth:r.scrollWidth, clientWidth:r.clientWidth, overflow:r.overflow});
  add('A6-a11y','390px: rendered visible controls meet the 44px floor', r.under44.length===0, {visibleScanned:r.visibleScanned, under44Count:r.under44.length, under44:r.under44.slice(0,12)});
  add('A6-a11y','390px: no page errors', h.errs.length===0, {errors:h.errs});
  await h.close();
}

await browser.close();
const pass=results.filter(function(r){return r.pass}).length;
console.log(JSON.stringify({total:results.length,passed:pass,failed:results.length-pass,results:results},null,1));
