(function () {
  'use strict';
  const controls = {q:document.getElementById('science-search'),pathway:document.getElementById('science-pathway'),term:document.getElementById('science-term'),style:document.getElementById('science-style')};
  const cards = [...document.querySelectorAll('[data-lesson-path]')];
  const batches = [...document.querySelectorAll('.catalogue-batch')];
  const terms = [...document.querySelectorAll('.catalogue-term')];
  const pathways = [...document.querySelectorAll('.science-pathway')];
  const count = document.getElementById('science-count');
  const subject = document.body.dataset.catalogueSubject || 'Science';
  const noun = document.body.dataset.catalogueNoun || 'lesson';
  function setFromQuery(query) {
    for (const [key, control] of Object.entries(controls)) {
      const value = query.get(key) || '';
      control.value = control.tagName === 'SELECT' && ![...control.options].some(o => o.value === value) ? '' : value;
    }
  }
  function refresh(updateURL) {
    const q = controls.q.value.trim().toLowerCase();
    let shown = 0;
    cards.forEach(card => {
      const show = (!q || card.textContent.toLowerCase().includes(q)) && ['pathway','term','style'].every(key => !controls[key].value || card.dataset[key] === controls[key].value);
      card.hidden = !show;
      if (show) shown++;
    });
    for (const [containers, selector] of [[batches,'[data-batch-count]'],[terms,'[data-term-count]'],[pathways,'[data-pathway-count]']]) {
      containers.forEach(container => {
        const n = [...container.querySelectorAll('[data-lesson-path]')].filter(card => !card.hidden).length;
        container.hidden = n === 0;
        container.querySelector(selector).textContent = (selector==='[data-pathway-count]'?'':'· ') + n + ' '+noun+(n===1?'':'s');
        if (container.tagName === 'DETAILS' && n && Object.values(controls).some(control => control.value)) container.open = true;
      });
    }
    count.textContent = `${shown} of ${cards.length} ${subject} ${noun}s`;
    document.getElementById('science-empty').hidden = shown !== 0;
    if (updateURL) {
      const query = new URLSearchParams();
      Object.entries(controls).forEach(([key,control]) => { if (control.value) query.set(key,control.value); });
      try { history.replaceState(null,'',location.pathname+(query.toString()?'?'+query:'')+location.hash); } catch (_) { /* Filtering also works for saved copies. */ }
    }
  }
  Object.entries(controls).forEach(([key,control]) => control.addEventListener(key==='q'?'input':'change',()=>refresh(true)));
  document.getElementById('science-clear').addEventListener('click',()=>{Object.values(controls).forEach(control=>{control.value='';});refresh(true);controls.q.focus();});
  document.querySelectorAll('[data-shortcut]').forEach(link => link.addEventListener('click',event=>{
    if (event.button!==0 || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
    event.preventDefault();setFromQuery(new URL(link.href).searchParams);refresh(true);controls.style.focus();
  }));
  window.addEventListener('popstate',()=>{setFromQuery(new URLSearchParams(location.search));refresh(false);});
  let printClosed=[];
  window.addEventListener('beforeprint',()=>{printClosed=pathways.filter(section=>!section.hidden&&!section.open);printClosed.forEach(section=>{section.open=true;});});
  window.addEventListener('afterprint',()=>{printClosed.forEach(section=>{section.open=false;});printClosed=[];});
  setFromQuery(new URLSearchParams(location.search));refresh(false);
})();
