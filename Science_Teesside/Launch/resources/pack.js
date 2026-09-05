/* Additive resources. No lesson clock, stage, saved pupil data or navigation changes. */
(()=>{
  'use strict';
  const boot=()=>{
  const dialog=document.getElementById('mbm-science-pack');
  const entry=document.getElementById('mbm-sp-entry');
  if(entry){
    const title=document.querySelector('.slide[data-title="Title"] .scaffold-box');
    const shared=document.getElementById('wedo2');
    for(const host of [title,shared])if(host&&!host.querySelector('[data-open-science-pack]'))host.append(entry.content.cloneNode(true));
  }
  if(dialog){
    // Keep Tab within the teaching panel, including the last-to-first boundary.
    // Native modal navigation may otherwise hand focus to browser chrome.
    // Escape and focus return remain the native dialog behaviour.
    dialog.addEventListener('keydown',e=>{
      e.stopPropagation();
      if(e.key!=='Tab')return;
      const focusable=[...dialog.querySelectorAll('a[href],button,textarea,input,select,summary,iframe,[tabindex]')]
        .filter(el=>!el.disabled&&el.tabIndex>=0&&el.getClientRects().length>0);
      const first=focusable[0],last=focusable[focusable.length-1];
      if(!first){e.preventDefault();dialog.focus();return;}
      if(e.shiftKey&&document.activeElement===first){e.preventDefault();last.focus();}
      else if(!e.shiftKey&&document.activeElement===last){e.preventDefault();first.focus();}
    });
    dialog.addEventListener('close',()=>{
      for(const frame of dialog.querySelectorAll('iframe'))frame.remove();
      for(const button of dialog.querySelectorAll('[data-play-video]'))button.hidden=false;
    });
  }
  document.addEventListener('click',e=>{
    const opener=e.target.closest('[data-open-science-pack]');
    if(opener&&dialog&&typeof dialog.showModal==='function'){
      e.preventDefault();dialog.showModal();return;
    }
    const button=e.target.closest('[data-play-video]');
    if(!button)return;
    const host=button.closest('[data-video]'),id=host?.dataset.video;
    if(!id||!/^[A-Za-z0-9_-]{11}$/.test(id))return;
    const frame=document.createElement('iframe');
    frame.title=host.dataset.videoTitle+' · freesciencelessons';
    frame.src='https://www.youtube-nocookie.com/embed/'+id+'?rel=0';
    frame.allow='fullscreen; picture-in-picture';frame.referrerPolicy='strict-origin-when-cross-origin';
    frame.setAttribute('allowfullscreen','');host.append(frame);button.hidden=true;
  });
  };
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',boot,{once:true});else boot();
})();
