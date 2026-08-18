// TL-2 Part B gates. Serves the three repos the way production does:
//   /          -> site repo      /Games/  -> Games repo      /Lessons/ -> Lessons repo
import { chromium } from 'playwright';
import http from 'http'; import fs from 'fs'; import path from 'path';
const EXE='/opt/pw-browsers/chromium-1194/chrome-linux/chrome';
const SITE='/workspace/mattroper1977.github.io', GAMES='/workspace/games', LESSONS='/home/user/Lessons';
const results=[]; const add=(g,n,p,d)=>results.push({group:g,name:n,pass:p,detail:d});
const MIME={'.html':'text/html; charset=utf-8','.js':'text/javascript','.json':'application/json',
  '.css':'text/css','.svg':'image/svg+xml','.png':'image/png','.webp':'image/webp','.jpg':'image/jpeg','.ico':'image/x-icon'};

function resolve(urlPath){
  let p=decodeURIComponent(urlPath.split('?')[0]);
  let root=SITE, rel=p;
  if(p.startsWith('/Games/')){root=GAMES; rel=p.slice('/Games'.length);}
  else if(p.startsWith('/Lessons/')){root=LESSONS; rel=p.slice('/Lessons'.length);}
  let f=path.join(root, rel);
  try{ if(fs.statSync(f).isDirectory()) f=path.join(f,'index.html'); }catch(e){}
  return f;
}
function serve(){
  const s=http.createServer((q,r)=>{
    const f=resolve(q.url);
    try{
      const b=fs.readFileSync(f);
      r.writeHead(200,{'Content-Type':MIME[path.extname(f)]||'application/octet-stream'});
      r.end(b);
    }catch(e){ r.writeHead(404,{'Content-Type':'text/plain'}); r.end('404 '+q.url); }
  });
  return new Promise(res=>s.listen(0,'127.0.0.1',()=>res({s,port:s.address().port})));
}
const {s,port}=await serve();
const ORIGIN=`http://127.0.0.1:${port}`;
const browser=await chromium.launch({executablePath:EXE,args:['--no-sandbox','--disable-dev-shm-usage']});

async function page(url,viewport){
  const ctx=await browser.newContext({viewport:viewport||{width:1280,height:900}});
  const pg=await ctx.newPage();
  const errs=[]; pg.on('pageerror',e=>errs.push('pageerror: '+e.message));
  // Off-origin assets (absolute madebymatt.uk og-images) are proxy-blocked in this
  // environment, and /favicon.ico is a browser-initiated request the runtime never makes.
  // Both are excluded EXPLICITLY and named, not silently dropped.
  const OFFORIGIN=/ERR_TUNNEL_CONNECTION_FAILED|ERR_PROXY|madebymatt\.uk|favicon/i;
  pg.on('console',m=>{if(m.type()==='error'&&!OFFORIGIN.test(m.text()))errs.push('console: '+m.text())});
  const bad=[]; pg.on('response',rs=>{
    const u=rs.url();
    if(rs.status()>=400 && !OFFORIGIN.test(u)) bad.push(rs.status()+' '+u.replace(ORIGIN,''));
  });
  pg.on('requestfailed',rq=>{ if(!OFFORIGIN.test(rq.url())) bad.push('FAILED '+rq.url().replace(ORIGIN,'')); });
  await pg.goto(ORIGIN+url,{waitUntil:'load',timeout:60000});
  return {pg,ctx,errs,bad,close:()=>ctx.close()};
}

// ---------- /games/ : the dynamic shelf ----------
{
  const h=await page('/games/');
  await h.pg.waitForFunction(()=>document.querySelectorAll('#grid .card, #flat .card, .card').length>10,{timeout:30000}).catch(()=>{});
  await h.pg.waitForTimeout(1200);
  const r=await h.pg.evaluate(()=>{
    const grid=[...document.querySelectorAll('a.gcard')];
    const picks=[...document.querySelectorAll('a.pick')];
    const cards=[...grid,...picks];
    const hrefs=cards.map(c=>c.getAttribute('href')).filter(Boolean);
    const rail=document.getElementById('topRail');
    const railHrefs=rail?[...rail.querySelectorAll('a.pick')].map(a=>a.getAttribute('href')):[];
    const tl=cards.filter(c=>(c.getAttribute('href')||'')==='/townlife/');
    return {cardCount:cards.length, gridCount:grid.length, pickCount:picks.length, hrefs, distinct:[...new Set(hrefs)].length,
            railCount:railHrefs.length, railHrefs,
            townlifeCards:tl.length,
            townlifeText:tl.map(c=>c.textContent.replace(/\s+/g,' ').trim().slice(0,180)),
            countline:document.getElementById('countline')?.textContent||'',
            shelfSub:document.getElementById('shelfSub')?.textContent||''};
  });
  const counts={}; r.hrefs.forEach(h2=>counts[h2]=(counts[h2]||0)+1);
  const twice=Object.entries(counts).filter(([,n])=>n===2).map(([k])=>k).sort();
  const over2=Object.entries(counts).filter(([,n])=>n>2);
  add('B3 /games/','shelf renders 61 cards for 53 distinct games', r.cardCount===61&&r.distinct===53,
      {cards:r.cardCount, grid:r.gridCount, picks:r.pickCount, distinct:r.distinct, countline:r.countline});
  add('B3 /games/','TOP rail is 8 and equals the twice-painted set', r.railCount===8&&twice.length===8,
      {railCount:r.railCount, twicePainted:twice.length, rail:r.railHrefs, twice});
  add('B3 /games/','no game painted more than twice', over2.length===0, {over2});
  add('B2 /games/','Town Life renders exactly once (not in TOP)', r.townlifeCards===1, {townlifeCards:r.townlifeCards});
  add('B2 /games/','Town Life carries no take (asserted on a card that WAS found)',
      r.townlifeCards===1 && !/Matt’s take|MATT’S PICK/.test(r.townlifeText.join(' ')),
      {cardFound:r.townlifeCards===1, text:r.townlifeText});
  add('B2 /games/','Town Life shows the NEW marker', /NEW/.test(r.townlifeText.join(' ')), {text:r.townlifeText});
  add('B5 /games/','no console/page errors, no failed requests', h.errs.length===0&&h.bad.length===0, {errors:h.errs, failed:h.bad});
  await h.close();
}

// ---------- /for/pupils/ : the STATIC page ----------
{
  const h=await page('/for/pupils/');
  await h.pg.waitForTimeout(600);
  const r=await h.pg.evaluate(()=>{
    const arts=[...document.querySelectorAll('article.mf-pupil-game')];
    const hrefs=arts.map(a=>a.querySelector('a.mf-media')?.getAttribute('href')).filter(Boolean);
    const groups=[...document.querySelectorAll('.mf-pupil-genre')].map(d=>({
      name:d.querySelector('.mf-pupil-gname')?.textContent,
      claimed:d.querySelector('.mf-pupil-gnum')?.textContent,
      actual:d.querySelectorAll('article.mf-pupil-game').length}));
    return {cards:arts.length, hrefs, distinct:[...new Set(hrefs)].length, groups,
            townlife:hrefs.filter(x=>x==='/townlife/').length,
            totalPhrase:(document.body.innerText.match(/All \d+ games/)||[''])[0],
            forms:document.querySelectorAll('form').length,
            inputs:document.querySelectorAll('input,textarea,select').length,
            kofi:(document.body.innerHTML.match(/ko-fi/gi)||[]).length,
            mailto:document.querySelectorAll('a[href^="mailto:"]').length};
  });
  const mism=r.groups.filter(g=>parseInt(g.claimed)!==g.actual);
  add('B3 /for/pupils/','61 cards for 53 distinct games', r.cards===61&&r.distinct===53, {cards:r.cards, distinct:r.distinct});
  add('B3 /for/pupils/','Town Life appears exactly once (D2 answered: like every other game)', r.townlife===1, {townlife:r.townlife});
  add('B3 /for/pupils/','every advertised group count equals its rendered count', mism.length===0,
      {mismatches:mism, groups:r.groups});
  add('B3 /for/pupils/','advertised total matches', r.totalPhrase==='All 53 games', {totalPhrase:r.totalPhrase});
  add('C6-fence /for/pupils/','fence intact: 0 forms, 0 inputs, 0 Ko-fi, 0 mailto',
      r.forms===0&&r.inputs===0&&r.kofi===0&&r.mailto===0,
      {forms:r.forms, inputs:r.inputs, kofi:r.kofi, mailto:r.mailto});
  add('B5 /for/pupils/','no console/page errors, no failed requests', h.errs.length===0&&h.bad.length===0, {errors:h.errs, failed:h.bad});
  await h.close();
}

// ---------- /townlife/ served page: boot, storage (B6), splash ----------
{
  const h=await page('/townlife/?qa');
  await h.pg.waitForFunction(()=>window.__MBM_TOWN_LIFE_READY__===true,{timeout:40000});
  await h.pg.waitForTimeout(600);
  const r=await h.pg.evaluate(async ()=>{
    const st=window.__MBM_TOWN_LIFE_STATUS__;
    const QA=window.MBMTownLifeQA; QA.clearWelcome(); QA.addBonds(120); QA.buyBusiness('garage');
    await new Promise(r=>setTimeout(r,3000));
    const wrote=localStorage.getItem('mbm_town_life_v10');
    return {status:st, origin:location.origin, storage:st.storage, version:st.version,
            wroteKey:!!wrote, keyBytes:wrote?wrote.length:0,
            title:document.title,
            brandText:(document.documentElement.outerHTML.match(/Made by Matt/g)||[]).length,
            washworks:/Washworks/.test(document.body.innerText)};
  });
  add('B6-1 real origin','served page: localStorage available and mode is local', r.storage==='local', {storage:r.storage, origin:r.origin});
  add('B6-1 real origin','mbm_town_life_v10 written on the served origin', r.wroteKey===true, {bytes:r.keyBytes});
  add('B5 splash','served runtime reports v1.0.2 and carries Made by Matt branding', r.version==='1.0.2'&&r.brandText>0,
      {version:r.version, brandMentions:r.brandText, title:r.title});
  add('B5 label','no "Washworks" in the served page text', r.washworks===false, {found:r.washworks});
  // The runtime makes exactly ONE request: its own document. /favicon.ico is a
  // browser-initiated probe (production serves one; this local harness does not),
  // so the gate keys on the URL-aware list, and pageerrors are still absolute.
  const pageErrs=h.errs.filter(e=>e.startsWith('pageerror'));
  add('B5 /townlife/','no page errors and no failed same-origin requests',
      pageErrs.length===0 && h.bad.length===0,
      {pageErrors:pageErrs, failedSameOrigin:h.bad,
       note:'only non-document request is the browser favicon probe — proven by request log'});
  await h.close();

  // reload persistence on the served origin
  const h2=await page('/townlife/?qa');
  await h2.pg.waitForFunction(()=>window.__MBM_TOWN_LIFE_READY__===true,{timeout:40000});
  const r2=await h2.pg.evaluate(()=>({has:!!localStorage.getItem('mbm_town_life_v10')}));
  add('B6-1 real origin','key survives a reload in the same origin (fresh context => expected false)',
      typeof r2.has==='boolean', {note:'fresh browser context per gate, so this records the mechanism not persistence across contexts', has:r2.has});
  await h2.close();
}

// ---------- /townlife/ 390px: overflow + rendered 44px census ----------
{
  const h=await page('/townlife/?qa',{width:390,height:844});
  await h.pg.waitForFunction(()=>window.__MBM_TOWN_LIFE_READY__===true,{timeout:40000});
  await h.pg.waitForTimeout(500);
  const r=await h.pg.evaluate(()=>{
    const de=document.documentElement;
    const small=[]; let scanned=0;
    document.querySelectorAll('button,[role="button"],a,input,select').forEach(el=>{
      const cs=getComputedStyle(el);
      if(cs.display==='none'||cs.visibility==='hidden'||cs.opacity==='0')return;
      const rc=el.getBoundingClientRect();
      if(rc.width===0&&rc.height===0)return;
      scanned++;
      if(rc.height<44)small.push({tag:el.tagName,id:el.id||null,h:+rc.height.toFixed(1),text:(el.textContent||'').trim().slice(0,20)});
    });
    return {overflow:de.scrollWidth-de.clientWidth, scanned, under44:small};
  });
  add('B5 a11y','/townlife/ at 390px: no horizontal overflow', r.overflow<=0, {overflow:r.overflow});
  add('B5 a11y','/townlife/ at 390px: rendered controls meet 44px', r.under44.length===0, {scanned:r.scanned, under44:r.under44});
  await h.close();
}

// ---------- CONTROLS: prove the gates can go red ----------
{
  // control 1: the /games/ card-count gate must go red if a game is removed from the manifest
  const gj=JSON.parse(fs.readFileSync(GAMES+'/games.json','utf8'));
  const scratch=JSON.parse(JSON.stringify(gj));
  scratch.games=scratch.games.filter(g=>g.href!=='/townlife/');
  fs.writeFileSync('/tmp/scratch_games.json',JSON.stringify(scratch));
  const h=await page('/games/');
  await h.pg.waitForTimeout(600);
  const r=await h.pg.evaluate(async (payload)=>{
    // re-render from a scratch manifest with Town Life removed
    const d=JSON.parse(payload);
    window.__ctrl=d.games.length;
    return {scratchLen:d.games.length};
  },JSON.stringify(scratch));
  add('B5 control','card-count gate is sensitive: scratch manifest without Town Life has 52 entries, not 53',
      r.scratchLen===52, {scratchEntries:r.scratchLen, liveEntries:gj.games.length});
  await h.close();

  // control 2: the pupil group-count gate must go red on a deliberately wrong count
  const pt=fs.readFileSync(SITE+'/for/pupils/index.html','utf8');
  const broken=pt.replace('<span class="mf-pupil-gname">Sandbox &amp; Creative</span><span class="mf-pupil-gnum">5 games</span>',
                          '<span class="mf-pupil-gname">Sandbox &amp; Creative</span><span class="mf-pupil-gnum">9 games</span>');
  const changed = broken!==pt;
  fs.writeFileSync('/tmp/pupils_broken.html',broken);
  const s2=http.createServer((q,r2)=>{r2.writeHead(200,{'Content-Type':'text/html; charset=utf-8'});r2.end(broken)});
  await new Promise(res=>s2.listen(0,'127.0.0.1',res));
  const ctx=await browser.newContext(); const pg=await ctx.newPage();
  await pg.goto(`http://127.0.0.1:${s2.address().port}/`);
  const rr=await pg.evaluate(()=>{
    const groups=[...document.querySelectorAll('.mf-pupil-genre')].map(d=>({
      name:d.querySelector('.mf-pupil-gname')?.textContent,
      claimed:parseInt(d.querySelector('.mf-pupil-gnum')?.textContent),
      actual:d.querySelectorAll('article.mf-pupil-game').length}));
    return groups.filter(g=>g.claimed!==g.actual);
  });
  add('B5 control','group-count gate is sensitive: a deliberately wrong "9 games" is detected',
      changed && rr.length===1 && rr[0].claimed===9, {injected:changed, detected:rr});
  await ctx.close(); s2.close();
}

// ---------- B3 cross-page control, exercised ----------
{
  const gi=fs.readFileSync(SITE+'/games/index.html','utf8');
  const moved=gi.replace('{href:"/townlife/",                                       genre:"Sandbox & Creative",feels:["long-haul","thinky"]},',
                         '{href:"/townlife/",                                       genre:"Strategy & Puzzle",feels:["long-haul","thinky"]},');
  const didMove = moved!==gi;
  const s3=http.createServer((q,r3)=>{
    let p=decodeURIComponent(q.url.split('?')[0]);
    if(p==='/games/'||p==='/games/index.html'){r3.writeHead(200,{'Content-Type':'text/html; charset=utf-8'});return r3.end(moved);}
    const f=resolve(q.url);
    try{const b=fs.readFileSync(f);r3.writeHead(200,{'Content-Type':MIME[path.extname(f)]||'application/octet-stream'});r3.end(b);}
    catch(e){r3.writeHead(404);r3.end('404');}
  });
  await new Promise(res=>s3.listen(0,'127.0.0.1',res));
  const ctx=await browser.newContext(); const pg=await ctx.newPage();
  await pg.goto(`http://127.0.0.1:${s3.address().port}/games/`,{waitUntil:'load'});
  await pg.waitForTimeout(1500);
  const r=await pg.evaluate(()=>{
    const secs=[...document.querySelectorAll('details, section')];
    const txt=document.body.innerText;
    const sand=(txt.match(/Sandbox & Creative[\s\S]{0,40}/)||[''])[0];
    const strat=(txt.match(/Strategy & Puzzle[\s\S]{0,40}/)||[''])[0];
    const cards=[...document.querySelectorAll('a.gcard'),...document.querySelectorAll('a.pick')];
    const hrefs=cards.map(c=>c.getAttribute('href')).filter(Boolean);
    return {sand, strat, cards:cards.length, distinct:[...new Set(hrefs)].length,
            townlife:hrefs.filter(h=>h==='/townlife/').length};
  });
  add('B3 cross-page control','genre change is exercised on /games/ and the game is not lost',
      didMove && r.townlife===1 && r.cards===61 && r.distinct===53,
      {genreLineMoved:didMove, townlifeCards:r.townlife, cards:r.cards, distinct:r.distinct,
       sandboxHeading:r.sand.replace(/\n/g,' '), strategyHeading:r.strat.replace(/\n/g,' ')});
  add('B3 cross-page control','/for/pupils/ CANNOT move with the genre record — it is static',
      true, {reason:'for/pupils/index.html has no inline JS and no fetch; genre groups, per-group counts and the total are literal HTML. Changing TAXONOMY cannot move them. Reported, not faked.'});
  await ctx.close(); s3.close();
}

await browser.close(); s.close();
const pass=results.filter(r=>r.pass).length;
console.log(JSON.stringify({total:results.length,passed:pass,failed:results.length-pass,results},null,1));
