/* SW2 K: one companion entry, one row per recorded file. No catalogue writes. */
(function(){
 'use strict';
 const H=window.MBM_HUB, main=document.querySelector('#pack-content');
 const order=[['lesson','pptx','Editable slides','editable'],['slides','pdf','Slides','print'],['pupil','docx','Pupil resources','editable'],['pupil','pdf','Pupil resources','print'],['teacher','docx','Teacher guide','editable'],['teacher','pdf','Teacher guide','print']];
 const E=H.esc;
 const href=path=>H.safeHref('/Lessons/'+path);
 const title=r=>String(r.displayTitle||r.title||'').replace(/\s*·\s*Companion pack\s*$/i,'');
 function chooser(){
  document.title='Lesson packs — Made by Matt';
  main.innerHTML='<div class="pk-intro"><h1>Lesson packs</h1></div><nav class="pk-chooser" aria-label="Choose a subject">'+H.cardsFromRows(H.state.rows).map(c=>`<a class="pk-action" href="/Lessons/subject.html?subject=${encodeURIComponent(c.slug)}">${E(c.name)} →</a>`).join('')+'</nav>';
  main.dataset.ready='chooser';
 }
 function show(pack,notes){
  const host=H.state.rows.find(r=>r._path===pack.companionOf), lesson=host||pack;
  const card=H.cardsFromRows(H.state.rows).find(c=>c.slug===H.cardOf(pack));
  const subject=card?card.name:String(pack.subject), pathway=H.tierOf(pack), halfTerm=pack.halfTerm||'';
  const back=new URLSearchParams({subject:H.cardOf(pack),pathway:pathway||'',unit:pack.unit||''});
  if(halfTerm)back.set('halfTerm',halfTerm);
  const files=pack.files.map((f,i)=>({f,i,rank:order.findIndex(o=>o[0]===f.role&&o[1]===f.type)})).sort((a,b)=>(a.rank<0?order.length:a.rank)-(b.rank<0?order.length:b.rank)||a.i-b.i);
  const badges=[...new Set(files.map(({f})=>f.type.toUpperCase()))];
  const note=notes?.entries?.[pack.id];
  const guide=pack.files.find(f=>f.role==='teacher'&&f.type==='pdf');
  const validNote=note&&guide&&note.source===guide.path&&typeof note.text==='string'&&note.text.trim().split(/\s+/).length<=60;
  const weeks=H.weeksOf(lesson);const position=weeks.length?`Week ${weeks.map(w=>w.week).join(', ')}`:'';
  document.title=title(lesson)+' — Lesson pack — Made by Matt';
  main.innerHTML=`<nav class="pk-breadcrumb" aria-label="Breadcrumb"><a href="/resources/">Resources</a><span aria-hidden="true">/</span><a href="/Lessons/subject.html?subject=${encodeURIComponent(H.cardOf(pack))}">${E(subject)}</a><span aria-hidden="true">/</span><span>Lesson pack</span></nav>
   <div class="pk-intro"><div class="pk-chips">${pathway?`<span class="pk-chip ${E(pathway)}">${E(pathway)}</span>`:''}${position?`<span class="pk-chip">${E(position)}</span>`:''}</div><h1>${E(title(lesson))}</h1><p class="pk-meta">${E(['Lesson pack',halfTerm].filter(Boolean).join(' · '))}</p><div class="pk-chips">${badges.map(t=>`<span class="pk-chip pk-format">${E(t)}</span>`).join('')}</div></div>
   ${pack.packRevisionDrift?'<p class="pk-drift"><span aria-hidden="true">ⓘ </span>Built from an earlier revision of this lesson.</p>':''}
   <div class="pk-layout"><div><section class="pk-card pk-files-card" aria-labelledby="inside-title"><h2 id="inside-title">Inside this pack</h2><ul class="pk-files">${files.map(({f,rank})=>{const o=order[rank];const dl=f.type!=='pdf'&&f.type!=='html';const size=H.state.sizes[f.path];return `<li class="pk-file" data-file="${E(f.path)}"><div><strong>${E(o?o[2]:f.role||f.path.split('/').pop())}</strong><span class="pk-file-meta">${E([f.type.toUpperCase(),o?o[3]:'',size?H.fmtBytes(size):''].filter(Boolean).join(' · '))}</span></div><a class="pk-action" href="${E(href(f.path))}"${dl?' download':''} aria-label="${E((dl?'Download':'Open')+' '+(o?o[2]:f.role)+' '+f.type.toUpperCase())}">${dl?'Download':'Open'}</a></li>`}).join('')}</ul></section>${validNote?`<section class="pk-card pk-note" aria-labelledby="before-title"><h2 id="before-title">Before you teach</h2><p>${E(note.text)}</p></section>`:''}</div>
   <aside class="pk-side"><section class="pk-card"><h2>Teach the lesson</h2><a id="delivery" class="pk-action pk-primary" href="${E(href(pack.companionOf))}">Open delivery lesson →</a><p class="pk-meta">Opens ${E([subject,pathway,halfTerm].filter(Boolean).join(' · '))}.</p><a class="pk-action pk-back" href="/resources/?${E(back.toString())}">Back to unit resources</a><button type="button" class="pk-action pk-save" id="save-pack" aria-pressed="false">Save pack</button><p class="pk-status" id="lesson-save-status" role="status" aria-live="polite"></p></section></aside></div>`;
  const save=document.querySelector('#save-pack'),key='mbm.lesson.saved.v1';
  const paint=()=>{const on=H.state.saved.includes(pack._path);save.setAttribute('aria-pressed',String(on));save.textContent=on?'Pack saved':'Save pack';};
  paint();save.addEventListener('click',()=>{const on=H.state.saved.includes(pack._path);const next=on?H.state.saved.filter(x=>x!==pack._path):[...H.state.saved,pack._path];try{localStorage.setItem(key,JSON.stringify(next));H.state.saved=next;paint();H.announce(on?'Pack removed from Saved.':'Pack saved on this device.');}catch(_){H.announce('This browser cannot save right now. You can still open the files or bookmark this page.');}});
  main.dataset.ready=pack.id;
 }
 H.loadAll().then(async()=>{
  const id=new URLSearchParams(location.search).get('id');
  const pack=H.state.rows.find(r=>r.id===id&&r.kind==='pack'&&r.companionOf);
  if(!pack){chooser();return;}
  let notes=null;try{const r=await fetch('assets/catalogue/pack-notes.json');if(r.ok)notes=await r.json();}catch(_){}
  show(pack,notes);
 }).catch(()=>{main.innerHTML='<div class="pk-intro"><h1>Lesson packs</h1><p>The pack catalogue could not load. Please try again.</p><a class="pk-action" href="/Lessons/">Choose a subject →</a> <a class="pk-action" href="/resources/">Resources →</a></div>';main.dataset.ready='error';});
})();
