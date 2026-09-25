const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const {parseHTML} = require('linkedom');
const root = path.resolve(__dirname,'../..');
const originalRows = JSON.parse(fs.readFileSync(path.join(root,'resources.json'),'utf8'));
const metadata = JSON.parse(fs.readFileSync(path.join(root,'assets/catalogue/terms-and-styles.json'),'utf8'));
const science = JSON.parse(fs.readFileSync(path.join(root,'assets/catalogue/science-shelf.json'),'utf8'));
const humanities = JSON.parse(fs.readFileSync(path.join(root,'assets/catalogue/humanities-shelf.json'),'utf8'));
// Part L composes the already accepted shelves without editing resources.json.
const known = new Set(originalRows.map(r=>r.file||r.url));
const supplements = [[science,'Science'],[humanities,'Humanities']].flatMap(([shelf,subject])=>shelf.lessons.filter(r=>!known.has(r.path)).map(r=>({file:r.path,title:r.title,subject,type:r.resourceType||'lesson',family:subject+' Teesside',_shelfPathway:r.pathway})));
const rows = [...originalRows,...supplements];
const reports = [];
function check(name, fn){fn();reports.push({name,status:'PASS'});}
function environment(filename, search=''){
 const {document,window} = parseHTML(fs.readFileSync(path.join(root,filename),'utf8'));
 const location = new URL('https://madebymatt.uk/Lessons/'+filename+search);
 window.matchMedia = () => ({matches:false});
 window.HTMLElement.prototype.scrollIntoView = function(){};
 Object.defineProperty(window.HTMLAnchorElement.prototype,'href',{get(){return new URL(this.getAttribute('href')||'',location).href;},set(value){this.setAttribute('href',value);},configurable:true});
 // LinkeDOM supplies DOM parsing and events, but not a browser's selected-value
 // setter, location, navigation or rendering. Complete only those DOM interfaces.
 Object.defineProperty(window.HTMLOptionElement.prototype,'value',{get(){return this.hasAttribute('value')?this.getAttribute('value'):this.textContent;},set(value){this.setAttribute('value',String(value));},configurable:true});
 Object.defineProperty(window.HTMLSelectElement.prototype,'value',{get(){const selected=[...this.options].find(o=>o.hasAttribute('selected'));return selected?selected.value:(this.options[0]?.value||'');},set(value){[...this.options].forEach(o=>{if(o.value===String(value))o.setAttribute('selected','');else o.removeAttribute('selected');});},configurable:true});
 const context=vm.createContext({window,document,URL,URLSearchParams,console,Intl,setTimeout,clearTimeout,location,history:{replaceState(_,__,url){const next=new URL(url,location);location.href=next.href;}},fetch:async url=>({ok:true,status:200,json:async()=>JSON.parse(fs.readFileSync(path.join(root,url),'utf8'))})});
 return {document,window,context,location};
}
function runFile(env,filename){vm.runInContext(fs.readFileSync(path.join(root,filename),'utf8'),env.context,{filename});}
function event(env,element,type){const event=new env.window.Event(type,{bubbles:true,cancelable:true});if(type==='click')event.button=0;element.dispatchEvent(event);}
function visibleScience(env){return [...env.document.querySelectorAll('[data-lesson-path]')].filter(c=>!c.hidden);}
(async()=>{
 // UX2 A2/A3 (2026-09-08): the hub is the subject front door and the subject page is the
 // browsing surface. The old hub's term/style/year/subject filters were retired, so their
 // linkedom cases are replaced by the contracts the new surfaces carry.
 function hubEnv(file, search=''){
  const env=environment(file, search);
  runFile(env,'assets/catalogue/hub.js');env.context.MBM_HUB=env.window.MBM_HUB;
  const script=[...env.document.querySelectorAll('script:not([src])')].find(s=>s.textContent.startsWith('(function(){'));
  return {env, script};
 }
 async function boot(file, search=''){
  const {env, script}=hubEnv(file, search);
  vm.runInContext(script.textContent, env.context, {filename:file+':inline'});
  // the pages fetch five JSON files; wait for the derived line rather than a tick count
  for(let i=0;i<400;i++){ await new Promise(resolve=>setImmediate(resolve)); const text=(env.document.querySelector('#summary')?.textContent||'')+(env.document.querySelector('#count')?.textContent||''); if(/\d+ (lessons|resources|of)/.test(text)||env.document.querySelector('#chooser:not([hidden])')) break; }
  return env;
 }
 const H=hubEnv('index.html').env.window.MBM_HUB;
 const cards=H.cardsFromRows(H.state.rows.length?H.state.rows:JSON.parse(JSON.stringify(rows)).map(r=>{r._card=H.cardOf(r);r._tier=H.tierOf(r);r._fmt=H.formatOf(r);r._path=r.file||r.url||'';return r;}));
 const env=await boot('index.html');
 check('Hub renders one subject card per subject group and derives its count line',()=>{
  assert.equal(env.document.querySelectorAll('.scard').length,cards.length);
  assert.equal(env.document.querySelector('#count').textContent,`${rows.length} resources · ${cards.length} subjects`);
 });
 check('Every catalogue entry belongs to exactly one subject card',()=>{
  const total=cards.reduce((n,c)=>n+c.rows.length,0);assert.equal(total,rows.length);
  assert.equal(new Set(rows.map(r=>H.cardOf(r))).size,cards.length);
 });
 check('Format tiles open the existing flat results path pre-filtered by format',()=>{
  const tiles=[...env.document.querySelectorAll('.tile')].map(a=>a.getAttribute('href'));assert.deepEqual(tiles,['?format=html','?format=packs']);
 });
 const recommended=await boot('index.html','?view=recommended');
 // HUB1 R1 (2026-09-23): the count is DERIVED from the published metadata, never pinned. Before R1 it
// was the 15 LAUNCH W3-W7 lessons and the 6 FoodWise taught-week pages (21); R1 adds the one A / L1
// deck of every Autumn 2 Science cell, and those 21 must still be among what the view shows.
 const recommendedRows=rows.filter(r=>(metadata.entries[r.file||r.path]||{}).style==='recommended');
 check('Recommended view exposes exactly the catalogue rows styled recommended (derived: '+recommendedRows.length+'), the 15 LAUNCH and 6 FoodWise among them',()=>{
  const shown=recommended.document.querySelectorAll('#cards article.card').length;
  assert.equal(shown,recommendedRows.length);
  assert.ok(recommendedRows.length>=21,'the pre-R1 21 are still recommended');
  assert.equal(recommendedRows.filter(r=>/^Science_Teesside\/Launch\/SCI_L_W[3-7]_L[123]_/.test(r.file||r.path||'')).length,15);
  assert.equal(recommendedRows.filter(r=>/^BUILD_ASDAN\/FoodWise\//.test(r.file||r.path||'')).length,6);
 });
 const searching=await boot('index.html','?q=osmosis');
 check('Existing keyword search still returns matching resources with the announced count',()=>{const n=searching.document.querySelectorAll('#cards article.card').length;assert(n>0);assert(searching.document.querySelector('#status').textContent.startsWith(`Showing ${n} matching resources.`));});
 const legacy=await boot('index.html','?subject=Science&pathway=BUILD');
 check('Old hub query ?subject=Science&pathway=BUILD renders the BUILD science records',()=>{const n=legacy.document.querySelectorAll('#cards article.card').length;const expected=rows.filter(r=>H.cardOf(r)==='science'&&H.tierOf(r)==='BUILD').length;assert.equal(n,expected);assert(n>0);});
 let rendered=new Set();
 for(const c of cards){
  const segs=[...H.pathwaysPresent(c.rows), ...(c.rows.some(r=>!H.tierOf(r))?['ALL']:[])];
  for(const seg of segs){
   const page=await boot('subject.html',`?subject=${encodeURIComponent(c.slug)}&pathway=${seg}`);
   const expected=(seg==='ALL'?c.rows.filter(r=>!H.tierOf(r)):c.rows.filter(r=>H.tierOf(r)===seg)).map(r=>r.file||r.url||'');
   // open every row and expand every "Show n more" through the real controls
   for(let i=0;i<200;i++){const b=page.document.querySelector('button[data-toggle][aria-expanded="false"]');if(!b)break;event(page,b,'click');}
   for(let i=0;i<200;i++){const b=page.document.querySelector('button[data-more]');if(!b)break;event(page,b,'click');}
   const got=[...page.document.querySelectorAll('.lrow')].map(e=>e.dataset.resourcePath);
   if(JSON.stringify(got.slice().sort())!==JSON.stringify(expected.slice().sort()))throw new assert.AssertionError({message:`${c.slug}/${seg}: rendered ${got.length}, expected ${expected.length}; missing ${JSON.stringify(expected.filter(x=>!got.includes(x)).slice(0,4))}; extra ${JSON.stringify(got.filter(x=>!expected.includes(x)).slice(0,4))}`});
   got.forEach(x=>rendered.add(x));
   const tab=page.document.querySelector('#seg [role="tab"][aria-selected="true"]');
   if(segs.length>1||seg!=='ALL')assert.equal(tab&&tab.dataset.pathway,seg,`${c.slug}/${seg} tab`);
  }
 }
 check(`Every catalogue entry is rendered on exactly one subject × pathway path (${cards.length} subjects)`,()=>{assert.equal(rendered.size,rows.length);});
 const noSlug=await boot('subject.html','?subject=no-such-subject');
 check('Unknown subject slug shows the inline chooser',()=>{assert(!noSlug.document.querySelector('#chooser').hidden);assert.equal(noSlug.document.querySelectorAll('#chooser a').length,cards.length);});
 // ROUTES vs CARDS -- the ruling of 2026-09-22 on STOP-F2, carried into this check. The hub renders
 // one card per (route, week) the RECORD binds, so the one route bound to two weeks renders in both
 // and the page holds more cards than routes. Population is therefore counted in BINDINGS and
 // identity asserted on ROUTES, both derived from tools/catalogue/SCIENCE_WEEK_BINDINGS.json: the
 // record the builder READS, never the record it WRITES, which would make this check circular.
 // Nothing is loosened -- the retired lines asserted a bare count; these assert the exact route set,
 // the exact binding set, and that no card is rendered twice.
 const weekBindings=JSON.parse(fs.readFileSync(path.join(root,'tools/catalogue/SCIENCE_WEEK_BINDINGS.json'),'utf8')).entries;
 const scienceCards=science.lessons.flatMap(r=>{const ws=(weekBindings[r.path]||{}).weeks||[];return ws.length?ws.map(w=>({...r,term:w.term,week:String(w.weekWithinTerm)})):[{...r,week:'unspecified'}];});
 const scienceRoutes=[...new Set(science.lessons.map(r=>r.path))].sort();
 const launchCards=scienceCards.filter(r=>r.pathway==='LAUNCH');
 const launchRoutes=[...new Set(launchCards.map(r=>r.path))].sort();
 const cardKey=c=>`${c.dataset.lessonPath}|${c.dataset.term}|${c.dataset.week}`;
 const bindKey=r=>`${r.path}|${r.term}|${r.week}`;
 const routesOf=cards=>[...new Set(cards.map(c=>c.dataset.lessonPath))].sort();
 const sc=environment('Science_Teesside/index.html');runFile(sc,'assets/catalogue/science-shelf.js');
 check(`Science shelf renders every route in every week the record binds it (${scienceRoutes.length} routes, ${scienceCards.length} cards)`,()=>{
  const cards=visibleScience(sc);
  assert.deepEqual(routesOf(cards),scienceRoutes);
  assert.deepEqual(cards.map(cardKey).sort(),scienceCards.map(bindKey).sort());
  assert.equal(new Set(cards.map(cardKey)).size,cards.length);
 });
 let scienceCombinations=0;
 for(const pathway of ['','BUILD','GROW','LAUNCH'])for(const term of ['','Aut1','Aut2','Spr1'])for(const style of [...sc.document.querySelector('#science-style').options].map(o=>o.value)){
  sc.document.querySelector('#science-pathway').value=pathway;sc.document.querySelector('#science-term').value=term;sc.document.querySelector('#science-style').value=style;event(sc,sc.document.querySelector('#science-style'),'change');
  const expected=scienceCards.filter(r=>(!pathway||r.pathway===pathway)&&(!term||r.term===term)&&(!style||r.style===style));
  assert.equal(visibleScience(sc).length,expected.length,`${pathway}/${term}/${style}`);scienceCombinations++;
 }
 reports.push({name:`Science pathway/term/style filters match the record's bindings (${scienceCombinations} combinations)`,status:'PASS'});
 event(sc,sc.document.querySelector('#science-clear'),'click');
 check('Science clear filters restores all alternatives',()=>{assert.equal(visibleScience(sc).length,scienceCards.length);assert.deepEqual(routesOf(visibleScience(sc)),scienceRoutes);});
 const rec=environment('Science_Teesside/index.html','?pathway=LAUNCH&term=Aut1&style=recommended');runFile(rec,'assets/catalogue/science-shelf.js');
 check('Recommended deep link selects correct pathway, term and all 15 lessons',()=>{assert.equal(visibleScience(rec).length,15);assert(visibleScience(rec).every(c=>c.dataset.style==='recommended'));});
 const launch=environment('Science_Teesside/index.html','?pathway=LAUNCH');runFile(launch,'assets/catalogue/science-shelf.js');
 check(`All LAUNCH deep link exposes every preserved LAUNCH route across six terms (${launchRoutes.length} routes, ${launchCards.length} cards)`,()=>{assert.deepEqual(routesOf(visibleScience(launch)),launchRoutes);assert.equal(visibleScience(launch).length,launchCards.length);assert.deepEqual([...new Set(visibleScience(launch).map(c=>c.dataset.term))].sort(),['Aut1','Aut2','Spr1','Spr2','Sum1','Sum2']);});
 const launchWeek=environment('Science_Teesside/index.html','?pathway=LAUNCH&term=Aut2&week=1');runFile(launchWeek,'assets/catalogue/science-shelf.js');
 check('Week filter follows accepted term-local week, not obsolete filename numbering',()=>{const cards=visibleScience(launchWeek);assert.equal(cards.length,4);assert(cards.every(c=>c.dataset.lessonPath.includes('W9')));assert(cards.every(c=>c.querySelector('.science-week').textContent.includes('Autumn 2')));});
 check('All LAUNCH shortcut clears term/week/style and retains every version',()=>{event(launchWeek,launchWeek.document.querySelector('[data-shortcut="all-launch"]'),'click');assert.equal(visibleScience(launchWeek).length,launchCards.length);assert.deepEqual(routesOf(visibleScience(launchWeek)),launchRoutes);assert.equal(launchWeek.document.querySelector('#science-week').value,'');assert.equal(launchWeek.location.search,'?pathway=LAUNCH');});
 const unbound=environment('Science_Teesside/index.html','?week=unspecified');runFile(unbound,'assets/catalogue/science-shelf.js');
 check('Unproven weeks stay discoverable with an honest unknown label',()=>{
  // HUB1 R3 (2026-09-23) bound BUILD W8A/W8B to Aut1 W8, so the count is DERIVED from the shelf's own
  // records (a Science route with no bound week), never pinned; the two W8 decks must not be in it.
  const shown=visibleScience(unbound);
  assert.ok(shown.length>0,'the unknown-week view is not vacuous');
  assert(shown.every(c=>c.querySelector('.science-week').textContent==='Week not specified'));
  assert(!shown.some(c=>/SCI_B_W8[AB]_/.test(c.outerHTML)),'R3: BUILD W8A/W8B are bound, not unknown');
 });
 check('Science clear removes the week filter and restores all routes',()=>{event(unbound,unbound.document.querySelector('#science-clear'),'click');assert.equal(visibleScience(unbound).length,scienceCards.length);assert.deepEqual(routesOf(visibleScience(unbound)),scienceRoutes);assert.equal(unbound.location.search,'');});
 const full=environment('Science_Teesside/index.html','?style=full-lundy');runFile(full,'assets/catalogue/science-shelf.js');
 const fullLundyPaths=science.lessons.filter(r=>r.style==='full-lundy').map(r=>r.path).sort();
 check('Full Lundy shortcut exposes exactly the current matching source routes',()=>assert.deepEqual(visibleScience(full).map(c=>c.dataset.lessonPath).sort(),fullLundyPaths));
 check('Native keyboard/touch semantics and live status are declared',()=>{
  for(const doc of [sc.document])for(const s of doc.querySelectorAll('.toolbar select,.toolbar input'))assert(s.closest('label'));
  assert(env.document.querySelector('label[for="search"] #search'));
  assert.equal(sc.document.querySelector('#science-count').getAttribute('aria-live'),'polite');
  assert([...sc.document.querySelectorAll('.science-pathway')].every(d=>d.tagName==='DETAILS'&&d.firstElementChild.tagName==='SUMMARY'));
 });
 check('Science version shortcut applies its filters without losing alternatives',()=>{event(sc,sc.document.querySelector('[data-shortcut="full-lundy"]'),'click');assert.deepEqual(visibleScience(sc).map(c=>c.dataset.lessonPath).sort(),fullLundyPaths);assert.equal(sc.document.querySelector('#science-pathway').value,'');});
 check('Catalogue print hooks open and restore collapsed sections',()=>{const section=rec.document.querySelector('.science-pathway[data-pathway="LAUNCH"]');section.open=false;rec.window.dispatchEvent(new rec.window.Event('beforeprint'));assert.equal(section.open,true);rec.window.dispatchEvent(new rec.window.Event('afterprint'));assert.equal(section.open,false);});
 // UX2: the metadata-failure and alternative-batch cases tested the retired term/style filter chain; the
 // subject page groups by half-term and unit (record fields), so those cases are retired with the filters.
 const hu=environment('Humanities_Teesside/index.html');runFile(hu,'assets/catalogue/science-shelf.js');
 check('Humanities has every selected current and retained resource exactly once',()=>{assert.equal(visibleScience(hu).length,humanities.lessons.length);assert.deepEqual(visibleScience(hu).map(c=>c.dataset.lessonPath).sort(),humanities.lessons.map(r=>r.path).sort());});
 let humanitiesCombinations=0;
 const hTerms=[...hu.document.querySelector('#science-term').options].map(o=>o.value);
 const hStyles=[...hu.document.querySelector('#science-style').options].map(o=>o.value);
 for(const pathway of ['','BUILD','GROW','LAUNCH','OTHER'])for(const term of hTerms)for(const style of hStyles){
  hu.document.querySelector('#science-pathway').value=pathway;hu.document.querySelector('#science-term').value=term;hu.document.querySelector('#science-style').value=style;event(hu,hu.document.querySelector('#science-style'),'change');
  const expected=humanities.lessons.filter(r=>(!pathway||r.pathway===pathway)&&(!term||r.term===term)&&(!style||r.style===style));
  assert.equal(visibleScience(hu).length,expected.length,`Humanities ${pathway}/${term}/${style}`);humanitiesCombinations++;
 }
 reports.push({name:`Humanities pathway/term/style filters match every source route (${humanitiesCombinations} combinations)`,status:'PASS'});
 event(hu,hu.document.querySelector('#science-clear'),'click');
 check('Humanities clear restores all lessons and shared references',()=>assert.equal(visibleScience(hu).length,humanities.lessons.length));
 const unknown=environment('Humanities_Teesside/index.html','?term=unspecified');runFile(unknown,'assets/catalogue/science-shelf.js');
 check('Humanities unknown terms remain visible and honestly labelled',()=>{assert.equal(visibleScience(unknown).length,humanities.lessons.filter(r=>r.term==='unspecified').length);assert(visibleScience(unknown).length>0);assert(unknown.document.querySelector('#science-count').textContent.includes('Humanities resources'));});
 event(hu,hu.document.querySelector('[data-shortcut="full-lundy"]'),'click');
 check('Humanities full Lundy shortcut preserves all matching alternatives',()=>assert.equal(visibleScience(hu).length,humanities.lessons.filter(r=>r.style==='full-lundy').length));
 event(hu,hu.document.querySelector('[data-shortcut="autumn"]'),'click');
 check('Humanities Autumn shortcut selects by evidenced term only',()=>assert.equal(visibleScience(hu).length,humanities.lessons.filter(r=>r.term==='Aut1').length));
 const hs=visibleScience(hu)[0].closest('.science-pathway');hs.open=false;hu.window.dispatchEvent(new hu.window.Event('beforeprint'));
 check('Humanities print opens and restores a visible pathway',()=>{assert.equal(hs.open,true);hu.window.dispatchEvent(new hu.window.Event('afterprint'));assert.equal(hs.open,false);});
 // Q12 (ORDER RS1-G3, 2026-09-25): the start strip is laid out by science-shelf.css, and the Science
 // hub writer stopped linking it at edb27b0c (#612) while Humanities kept it. LinkeDOM computes no
 // styles, so this one check renders each hub in Chromium at 390 px and reads the COMPUTED display --
 // not the presence of a <link>, which a stylesheet that fails to load would still pass. The same sheet
 // orders the hub (catalogue.css makes main a flex column), so without it the filters render after the
 // whole lesson list; isVisible() is true either way, so position is asserted instead. Humanities is
 // the control: it never lost the link, so it proves the check can go green. Local-file bytes only;
 // every non-file request is refused, so nothing external can change the answer.
 const {chromium}=require('playwright');
 const browser=await chromium.launch({executablePath:process.env.MBM_CHROMIUM_PATH||undefined});
 try{
  for(const file of ['Science_Teesside/index.html','Humanities_Teesside/index.html']){
   const page=await browser.newPage({viewport:{width:390,height:844}});
   await page.route(url=>url.protocol!=='file:',route=>route.abort());
   await page.goto(require('node:url').pathToFileURL(path.join(root,file)).href,{waitUntil:'load'});
   const m=await page.evaluate(()=>{const grid=document.querySelector('.start-grid'),top=e=>e.getBoundingClientRect().top+scrollY,list=document.querySelector('#science-lessons');
    return {display:grid?getComputedStyle(grid).display:'(no .start-grid)',listTop:list?top(list):null,controls:[...document.querySelectorAll('.toolbar input,.toolbar select')].map(e=>{const b=e.getBoundingClientRect();return {id:e.id,top:Math.round(top(e)),left:b.left,right:b.right};})};});
   check(`${file.split('_')[0]} hub .start-grid computes display:grid at 390 px (Chromium)`,()=>assert.equal(m.display,'grid',`${file} .start-grid computes display:${m.display} at 390 px`));
   check(`${file.split('_')[0]} hub filter controls sit above the lesson list, inside 390 px (Chromium)`,()=>{
    assert(m.controls.length>=5&&m.listTop!==null,`${file} has its toolbar controls and #science-lessons`);
    for(const c of m.controls)assert(c.top<m.listTop&&c.left>=0&&c.right<=390,`${file} #${c.id} at y=${c.top}, x=${c.left}..${c.right}; the lesson list starts at y=${Math.round(m.listTop)}`);
   });
   await page.close();
  }
 }finally{await browser.close();}
 const report={scope:'Static DOM and JavaScript checks using LinkeDOM, plus one Chromium render per hub at 390 px for the computed .start-grid display; no keyboard hardware, touch hardware or print pagination was exercised.',resourceRows:rows.length,scienceRoutes:science.lessons.length,humanitiesResources:humanities.lessons.length,checks:reports};
 fs.writeFileSync(path.join(root,'tools/catalogue/DOM_CHECK_RESULTS.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report,null,2));
})().catch(error=>{console.error(error);process.exitCode=1});
