/* Classic control names and progression retained; standalone, no shared-site writes. */
(function () {
  'use strict';
  const deck = document.querySelector('.slide-container');
  const slides = Array.from(deck.querySelectorAll('.slide'));
  const data = window.CLASSIC_LESSON || {};
  let currentSlide = 0;
  let tick = null;
  let returnFocus = null;
  let modalWasRunning = false;
  const remaining = new Map();
  const levels = ['supported', 'standard', 'stretch'];
  const printSelectors = '.print-section,.print-resource,.print-sheet';
  const byId = id => document.getElementById(id);
  const number = value => Math.max(0, Number(value) || 0);
  function seconds(slide) { return Math.round(number(slide.dataset.timer) * 60); }
  function timerLeft() { return remaining.has(currentSlide) ? remaining.get(currentSlide) : seconds(slides[currentSlide]); }
  function updateTimerDisplay() {
    const left = timerLeft();
    const display = byId('auto-timer-display');
    if (display) display.textContent = String(Math.floor(left / 60)).padStart(2,'0') + ':' + String(left % 60).padStart(2,'0');
    const button = byId('auto-timer-toggle');
    if (button) { button.textContent = tick ? 'Ⅱ' : '▶'; button.setAttribute('aria-label', tick ? 'Pause stage timer' : 'Start stage timer'); }
    const timer = byId('auto-timer');
    if (timer) timer.classList.toggle('done', left === 0 && seconds(slides[currentSlide]) > 0);
  }
  function pauseTimer() { if (tick) clearInterval(tick); tick = null; updateTimerDisplay(); }
  function startTimer() {
    if (tick || timerLeft() <= 0 || document.querySelector('.classic-dialog[open]')) return;
    tick = setInterval(() => {
      remaining.set(currentSlide, Math.max(0, timerLeft() - 1));
      if (timerLeft() === 0) {
        pauseTimer();
        const notice=byId('classic-status');
        if (notice) notice.textContent = 'Stage time has ended. Move on when ready.';
      }
      updateTimerDisplay();
    },1000);
    updateTimerDisplay();
  }
  function autoTimerToggle() { if (tick) pauseTimer(); else startTimer(); }
  function autoTimerReset() { pauseTimer(); remaining.set(currentSlide, seconds(slides[currentSlide])); updateTimerDisplay(); }
  function updateProgress() {
    const slide=slides[currentSlide];
    byId('progressBar').style.width = ((currentSlide + 1) / slides.length * 100) + '%';
    byId('progressLabel').textContent = (slide.dataset.title || 'Slide') + ' • ' + (currentSlide + 1) + '/' + slides.length;
    const progress=byId('classic-progress');
    progress.setAttribute('aria-valuenow',String(currentSlide+1));
    progress.setAttribute('aria-valuetext',byId('progressLabel').textContent);
    byId('previous-slide').disabled=currentSlide===0;
    byId('next-slide').disabled=currentSlide===slides.length-1;
    const picker=byId('slide-picker');
    if(picker)picker.value=String(currentSlide);
  }
  function showSlide(index) {
    index = Math.max(0, Math.min(slides.length - 1, number(index)));
    pauseTimer();
    currentSlide = index;
    slides.forEach((slide, i) => {
      slide.classList.toggle('active',i===index);
      slide.inert = i !== index;
      slide.setAttribute('aria-hidden', String(i !== index));
    });
    updateProgress(); updateTimerDisplay();
    slides[index].scrollTop=0;
    document.dispatchEvent(new CustomEvent('classic-slide-change', {detail:{index, slide:slides[index]}}));
  }
  function nextSlide(){if(currentSlide < slides.length-1)showSlide(currentSlide+1);}
  function prevSlide(){if(currentSlide > 0)showSlide(currentSlide-1);}
  function switchLevel(prefix,level) {
    if(!levels.includes(level))return;
    levels.forEach(value=>{
      const el=byId(prefix+'-'+value);
      if(el){el.hidden=value!==level;el.style.display=value===level?(el.classList.contains('arrival-grid')?'grid':'block'):'none';}
    });
    document.querySelectorAll('[data-level-prefix="'+prefix+'"] [data-level]').forEach(button=>button.setAttribute('aria-pressed',String(button.dataset.level===level)));
  }
  function v5RevealNext(button){
    const slide=button.closest('.slide');if(!slide)return;
    const next=slide.querySelector('.v5-step:not(.revealed)');
    if(next){next.hidden=false;next.classList.add('revealed');}
    const total=slide.querySelectorAll('.v5-step').length;
    const shown=slide.querySelectorAll('.v5-step.revealed').length;
    const label=slide.querySelector('.v5-step-label');if(label)label.textContent='Step '+shown+' of '+total;
    button.disabled=shown>=total;
    if(button.disabled)button.textContent='✓ All revealed';
  }
  function openModal(id){
    const modal=byId(id);if(!modal)return;
    returnFocus=document.activeElement;
    modalWasRunning=Boolean(tick);pauseTimer();
    document.documentElement.classList.add('classic-modal-open');
    modal.showModal();
    const focus=modal.querySelector('button, input, select, textarea, a[href]');if(focus)focus.focus();
  }
  function closeModal(id){const modal=byId(id);if(modal&&modal.open)modal.close();}
  document.querySelectorAll('.classic-dialog').forEach(dialog=>{
    dialog.addEventListener('close',()=>{
      document.documentElement.classList.remove('classic-modal-open');
      const resume=modalWasRunning;modalWasRunning=false;
      if(returnFocus&&returnFocus.isConnected)returnFocus.focus();
      if(resume)startTimer();
    });
    dialog.addEventListener('click',event=>{if(event.target===dialog)dialog.close();});
  });
  function showTABrief(){
    const stage=slides[currentSlide];
    byId('ta-current-title').textContent=stage.dataset.title||'Current stage';
    const notes = stage.dataset.teacher || ((data.stages || [])[Number(stage.dataset.stageIndex)] || {}).teacher || 'Use the lesson guidance below.';
    byId('ta-current-text').textContent=notes;
    openModal('ta-dialog');
  }
  function showColdCall(){
    const stage=slides[currentSlide];
    const question=stage.dataset.prompt || stage.querySelector('h2,h1')?.textContent || data.objective || 'What do you notice? What helps you decide?';
    byId('cold-call-question').textContent=question;
    openModal('cold-call-dialog');
  }
  function printArm(level){
    if(!levels.includes(level))level='standard';
    document.body.classList.remove(...levels.map(value=>'print-'+value));
    document.body.classList.add('print-'+level);
    document.querySelectorAll(printSelectors).forEach(section=>{
      const specific=section.id.match(/^print-(?:scaffold|worksheet)-(supported|standard|stretch)$/);
      const classRoute=levels.find(value=>section.classList.contains(value+'-content'));
      const route=section.dataset.printRoute || (specific ? specific[1] : classRoute || 'all');
      section.classList.toggle('visible',route==='all'||route===level);
    });
    const visible=Array.from(document.querySelectorAll('.print-section.visible,.print-resource.visible,.print-sheet.visible'));
    document.querySelectorAll(printSelectors).forEach(section=>section.classList.remove('print-last'));
    if(visible.length)visible[visible.length-1].classList.add('print-last');
    if(byId('print-date'))byId('print-date').textContent=new Date().toLocaleDateString('en-GB');
  }
  function printPack(level){pauseTimer();printArm(level);window.print();}
  function printSection(id,level){
    printArm(level||'standard');
    document.querySelectorAll(printSelectors).forEach(section=>section.classList.toggle('visible',section.id==='print-'+id));
    window.print();
  }
  window.addEventListener('beforeprint',()=>{if(!/\bprint-(supported|standard|stretch)\b/.test(document.body.className))printArm('standard');});
  function downloadNotes(){
    const fields=Array.from(deck.querySelectorAll('textarea, input[data-note]'));
    const text=[data.title||'Lesson work','',...fields.map((field,i)=>{
      const slide=field.closest('.slide');
      const label=field.getAttribute('aria-label')||field.labels?.[0]?.textContent||'Response '+(i+1);
      return (slide?.dataset.title||'Work')+' — '+label+'\n'+(field.value||'(No response recorded)');
    })].join('\n\n');
    const uri=URL.createObjectURL(new Blob([text],{type:'text/plain;charset=utf-8'}));
    const link=document.createElement('a');link.href=uri;link.download=(data.id||'lesson')+'_My_Work.txt';
    document.body.appendChild(link);link.click();link.remove();setTimeout(()=>URL.revokeObjectURL(uri),1000);
  }
  document.addEventListener('keydown',event=>{
    if(document.querySelector('.classic-dialog[open]')||event.altKey||event.ctrlKey||event.metaKey)return;
    if(event.target.closest('button,input,textarea,select,a,[contenteditable="true"],[role="button"],[role="slider"]'))return;
    if(event.key==='ArrowRight'||event.key===' '){event.preventDefault();nextSlide();}
    if(event.key==='ArrowLeft'){event.preventDefault();prevSlide();}
  });
  document.addEventListener('visibilitychange',()=>{if(document.hidden)pauseTimer();});
  document.querySelectorAll('[data-action]').forEach(button=>button.addEventListener('click',()=>{
    const action=button.dataset.action;
    if(action==='previous')prevSlide();if(action==='next')nextSlide();if(action==='ta')showTABrief();
    if(action==='cold-call')showColdCall();if(action==='timer-toggle')autoTimerToggle();if(action==='timer-reset')autoTimerReset();
    if(action==='words')openModal('word-dialog');if(action==='pause')openModal('pause-dialog');
    if(action==='tools')openModal('tools-dialog');if(action==='notes')downloadNotes();
    if(action==='close')closeModal(button.closest('dialog').id);
    if(action==='print')printPack(button.dataset.level||'standard');
  }));
  const picker=byId('slide-picker');
  if(picker){slides.forEach((slide,index)=>{const option=document.createElement('option');option.value=String(index);option.textContent=(index+1)+'. '+(slide.dataset.title||'Slide');picker.appendChild(option);});picker.addEventListener('change',()=>{showSlide(Number(picker.value));closeModal('tools-dialog');});}
  Object.assign(window,{mbmShowSlide:showSlide,showSlide,nextSlide,prevSlide,switchLevel,v5RevealNext,showTABrief,showColdCall,printArm,printPack,printSection,pauseTimer,startTimer,autoTimerToggle,autoTimerReset,downloadNotes,openModal,closeModal});
  Object.defineProperty(window,'classicCurrentSlide',{get:()=>currentSlide});
  printArm('standard');showSlide(0);
}());
