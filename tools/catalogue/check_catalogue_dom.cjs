const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const {parseHTML} = require('linkedom');
const root = path.resolve(__dirname,'../..');
const rows = JSON.parse(fs.readFileSync(path.join(root,'resources.json'),'utf8'));
const metadata = JSON.parse(fs.readFileSync(path.join(root,'assets/catalogue/terms-and-styles.json'),'utf8'));
const science = JSON.parse(fs.readFileSync(path.join(root,'assets/catalogue/science-shelf.json'),'utf8'));
const humanities = JSON.parse(fs.readFileSync(path.join(root,'assets/catalogue/humanities-shelf.json'),'utf8'));
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
 const env=environment('index.html');
 runFile(env,'assets/catalogue/catalogue.js');env.context.MBM_CATALOGUE=env.window.MBM_CATALOGUE;
 const script=[...env.document.querySelectorAll('script:not([src])')].find(s=>s.textContent.startsWith('const $='));
 vm.runInContext(script.textContent,env.context,{filename:'index.html:inline-catalogue'});
 await new Promise(resolve=>setImmediate(resolve));
 check('Root initial catalogue load preserves current-year resource count',()=>assert.equal(env.document.querySelectorAll('#cards article.card').length,rows.filter(r=>r.year==='2026-27').length));
 const allYears=env.document.querySelector('.ytab[data-year=""]');event(env,allYears,'click');
 check('All-years browse includes each declared resource row once',()=>assert.equal(env.document.querySelectorAll('#cards article.card').length,rows.length));
 check('All existing catalogue links remain usable, including space-containing paths',()=>{
  const links=[...env.document.querySelectorAll('#cards article.card a.go')];assert.equal(links.length,rows.length);assert(links.every(a=>a.getAttribute('href')!=='#'));
  const expected=rows.map(r=>encodeURI(r.file||r.url)).sort();assert.deepEqual(links.map(a=>a.getAttribute('href')).sort(),expected);
 });
 let combinations=0;
 for(const term of ['',...Object.keys(metadata.terms)])for(const style of ['',...Object.keys(metadata.styles)]){
  env.document.querySelector('#term').value=term;env.document.querySelector('#style').value=style;event(env,env.document.querySelector('#style'),'change');
  const expected=rows.filter(r=>env.context.MBM_CATALOGUE.matches(r,metadata,term,style));
  assert.equal(env.document.querySelectorAll('#cards article.card').length,expected.length,`${term}/${style}`);combinations++;
 }
 reports.push({name:`Root term/style filter intersections match source metadata (${combinations} combinations)`,status:'PASS'});
 env.document.querySelector('#term').value='Aut1';env.document.querySelector('#style').value='recommended';event(env,env.document.querySelector('#style'),'change');
 check('Recommended filter exposes exactly the 15 integrated LAUNCH Science lessons',()=>assert.equal(env.document.querySelectorAll('#cards article.card').length,15));
 event(env,env.document.querySelector('[data-clear-filters]'),'click');
 check('Clear filters restores all declared rows and resets both new controls',()=>{assert.equal(env.document.querySelectorAll('#cards article.card').length,rows.length);assert.equal(env.document.querySelector('#term').value,'');assert.equal(env.document.querySelector('#style').value,'');});
 env.document.querySelector('#subject').value='Science · Teesside';event(env,env.document.querySelector('#subject'),'change');
 check('Existing subject filter still operates with new organisation',()=>assert.equal(env.document.querySelectorAll('#cards article.card').length,rows.filter(r=>r.subject==='Science · Teesside').length));
 env.document.querySelector('#subject').value='';env.document.querySelector('#search').value='osmosis';event(env,env.document.querySelector('#search'),'input');
 check('Existing keyword search still returns matching resources',()=>assert(env.document.querySelectorAll('#cards article.card').length>0));
 const sc=environment('Science_Teesside/index.html');runFile(sc,'assets/catalogue/science-shelf.js');
 check('Science shelf has all 123 source routes exactly once',()=>{assert.equal(visibleScience(sc).length,123);assert.equal(new Set(visibleScience(sc).map(c=>c.dataset.lessonPath)).size,123);});
 let scienceCombinations=0;
 for(const pathway of ['','BUILD','GROW','LAUNCH'])for(const term of ['','Aut1','Aut2','Spr1'])for(const style of ['','recommended','current','full-lundy','earlier']){
  sc.document.querySelector('#science-pathway').value=pathway;sc.document.querySelector('#science-term').value=term;sc.document.querySelector('#science-style').value=style;event(sc,sc.document.querySelector('#science-style'),'change');
  const expected=science.lessons.filter(r=>(!pathway||r.pathway===pathway)&&(!term||r.term===term)&&(!style||r.style===style));
  assert.equal(visibleScience(sc).length,expected.length,`${pathway}/${term}/${style}`);scienceCombinations++;
 }
 reports.push({name:`Science pathway/term/style filters match source routes (${scienceCombinations} combinations)`,status:'PASS'});
 event(sc,sc.document.querySelector('#science-clear'),'click');
 check('Science clear filters restores all alternatives',()=>assert.equal(visibleScience(sc).length,123));
 const rec=environment('Science_Teesside/index.html','?pathway=LAUNCH&term=Aut1&style=recommended');runFile(rec,'assets/catalogue/science-shelf.js');
 check('Recommended deep link selects correct pathway, term and all 15 lessons',()=>{assert.equal(visibleScience(rec).length,15);assert(visibleScience(rec).every(c=>c.dataset.style==='recommended'));});
 const launch=environment('Science_Teesside/index.html','?pathway=LAUNCH');runFile(launch,'assets/catalogue/science-shelf.js');
 check('All LAUNCH deep link exposes all 57 preserved teaching versions across three terms',()=>{assert.equal(visibleScience(launch).length,57);assert.deepEqual([...new Set(visibleScience(launch).map(c=>c.dataset.term))].sort(),['Aut1','Aut2','Spr1']);});
 const launchWeek=environment('Science_Teesside/index.html','?pathway=LAUNCH&term=Aut2&week=1');runFile(launchWeek,'assets/catalogue/science-shelf.js');
 check('Week filter follows accepted term-local week, not obsolete filename numbering',()=>{const cards=visibleScience(launchWeek);assert.equal(cards.length,3);assert(cards.every(c=>c.dataset.lessonPath.includes('W9')));assert(cards.every(c=>c.querySelector('.science-week').textContent.includes('Autumn 2')));});
 check('All LAUNCH shortcut clears term/week/style and retains every version',()=>{event(launchWeek,launchWeek.document.querySelector('[data-shortcut="all-launch"]'),'click');assert.equal(visibleScience(launchWeek).length,57);assert.equal(launchWeek.document.querySelector('#science-week').value,'');assert.equal(launchWeek.location.search,'?pathway=LAUNCH');});
 const unbound=environment('Science_Teesside/index.html','?week=unspecified');runFile(unbound,'assets/catalogue/science-shelf.js');
 check('Unproven weeks stay discoverable with an honest unknown label',()=>{assert.equal(visibleScience(unbound).length,4);assert(visibleScience(unbound).every(c=>c.querySelector('.science-week').textContent==='Week not specified'));});
 check('Science clear removes the week filter and restores all routes',()=>{event(unbound,unbound.document.querySelector('#science-clear'),'click');assert.equal(visibleScience(unbound).length,123);assert.equal(unbound.location.search,'');});
 const full=environment('Science_Teesside/index.html','?style=full-lundy');runFile(full,'assets/catalogue/science-shelf.js');
 check('Full Lundy shortcut preserves access to all 88 alternatives',()=>assert.equal(visibleScience(full).length,88));
 check('Native keyboard/touch semantics and live status are declared',()=>{
  for(const doc of [env.document,sc.document])for(const s of doc.querySelectorAll('.toolbar select,.toolbar input'))assert(s.closest('label'));
  assert.equal(sc.document.querySelector('#science-count').getAttribute('aria-live'),'polite');
  assert([...sc.document.querySelectorAll('.science-pathway')].every(d=>d.tagName==='DETAILS'&&d.firstElementChild.tagName==='SUMMARY'));
 });
 check('Science version shortcut applies its filters without losing alternatives',()=>{event(sc,sc.document.querySelector('[data-shortcut="full-lundy"]'),'click');assert.equal(visibleScience(sc).length,88);assert.equal(sc.document.querySelector('#science-pathway').value,'');});
 check('Catalogue print hooks open and restore collapsed sections',()=>{const closed=[...env.document.querySelectorAll('#cards details:not([open])')];env.window.dispatchEvent(new env.window.Event('beforeprint'));assert(closed.every(d=>d.open===true));env.window.dispatchEvent(new env.window.Event('afterprint'));assert(closed.every(d=>d.open===false));const section=rec.document.querySelector('.science-pathway[data-pathway="LAUNCH"]');section.open=false;rec.window.dispatchEvent(new rec.window.Event('beforeprint'));assert.equal(section.open,true);rec.window.dispatchEvent(new rec.window.Event('afterprint'));assert.equal(section.open,false);});
 const fallback=environment('index.html');runFile(fallback,'assets/catalogue/catalogue.js');fallback.context.MBM_CATALOGUE=fallback.window.MBM_CATALOGUE;
 fallback.context.fetch=async url=>{if(url.includes('terms-and-styles'))throw new Error('Simulated unavailable metadata');return {ok:true,json:async()=>structuredClone(rows)}};
 vm.runInContext(script.textContent,fallback.context);await new Promise(resolve=>setImmediate(resolve));
 check('Metadata failure leaves existing resource catalogue and search usable',()=>{assert.equal(fallback.document.querySelectorAll('#cards article.card').length,rows.filter(r=>r.year==='2026-27').length);assert(fallback.document.querySelector('#term').disabled);assert(fallback.document.querySelector('#catalogue-feedback').textContent.includes('still search'));});
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
 const report={scope:'Static DOM and JavaScript checks using LinkeDOM; no browser rendering, keyboard hardware, touch hardware or print pagination was exercised.',resourceRows:rows.length,scienceRoutes:science.lessons.length,humanitiesResources:humanities.lessons.length,checks:reports};
 fs.writeFileSync(path.join(root,'tools/catalogue/DOM_CHECK_RESULTS.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report,null,2));
})().catch(error=>{console.error(error);process.exitCode=1});
