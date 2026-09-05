/* Education-only catalogue return context and a separate, measured lesson toolbar. */
(function () {
  'use strict';
  if (window.__mbmLessonNavigation || !location.pathname.startsWith('/Lessons/') || location.pathname.startsWith('/Lessons/Games/')) return;
  window.__mbmLessonNavigation = true;
  const ROOT='/Lessons/', KEY='mbm.lesson.return.v1';
  const HUBS=new Set([ROOT,ROOT+'index.html',ROOT+'Science_Teesside/index.html',ROOT+'Science_Teesside/',ROOT+'Humanities_Teesside/index.html',ROOT+'Humanities_Teesside/']);
  function safeHub(value) {
    try { const u=new URL(value,location.origin);if(u.origin!==location.origin||!HUBS.has(u.pathname)||/[\\\u0000-\u001f]/.test(value))return null;
      const clean=new URL(u.pathname,location.origin);for(const key of ['q','subject','collection','type','pathway','term','style','year','view'])if(u.searchParams.has(key))clean.searchParams.set(key,u.searchParams.get(key).slice(0,200));return clean.pathname+clean.search;
    } catch (_) { return null; }
  }
  const isHub=HUBS.has(location.pathname);
  if(isHub)document.addEventListener('click',function(event){
    const a=event.target.closest('a[href]');if(!a)return;
    try{const u=new URL(a.href,location.href);if(u.origin!==location.origin||!u.pathname.startsWith(ROOT)||u.pathname.startsWith(ROOT+'Games/')||HUBS.has(u.pathname)||!u.pathname.endsWith('.html'))return;
      const back=safeHub(location.href);if(!back)return;let map;try{map=JSON.parse(sessionStorage.getItem(KEY)||'{}')}catch(_){map={}}if(!map||typeof map!=='object'||Array.isArray(map))map={};map[u.pathname]=back;const keys=Object.keys(map);for(const old of keys.slice(0,Math.max(0,keys.length-40)))delete map[old];sessionStorage.setItem(KEY,JSON.stringify(map));
    }catch(_){} });
  if(isHub)return;
  function fallback(){const p=location.pathname.replace(/%20/gi,' '),query=new URLSearchParams();
    if(/Science|Biology|Chemistry|Physics/i.test(p))query.set('subject','Science');else if(/Humanities|History|Geography|Rivers|(?:^|[/_])RE(?:[/_]|$)/i.test(p))query.set('subject','Humanities & RE');else if(/Art/i.test(p))query.set('subject','Art');else if(/ASDAN|Vocational|PfA/i.test(p))query.set('subject','ASDAN & life skills');
    const match=p.match(/(?:^|[/_])(BUILD|GROW|LAUNCH)(?:[/_]|$)/i);if(match)query.set('pathway',match[1].toUpperCase());return ROOT+(query.size?'?'+query:'');}
  let back=fallback();try{const map=JSON.parse(sessionStorage.getItem(KEY)||'{}');back=safeHub(map[location.pathname])||back;}catch(_){}
  const style=document.createElement('style');style.id='mbm-lesson-navigation-style';style.textContent=`
    #mbm-lesson-tools{position:relative;z-index:2000;display:flex;align-items:center;gap:8px;flex-wrap:wrap;padding:6px max(10px,env(safe-area-inset-right)) 6px max(10px,env(safe-area-inset-left));background:#161d3d;color:#f6f5ec;border-bottom:3px solid #8ee6cb;font:600 14px/1.3 system-ui,sans-serif;box-sizing:border-box}
    #mbm-lesson-tools>a,#mbm-lesson-tools>button{position:static!important;inset:auto!important;transform:none!important;display:inline-flex;align-items:center;justify-content:center;min-height:44px;max-width:100%;width:auto;height:auto;margin:0!important;padding:8px 12px!important;background:#223950!important;color:#e5fbf5!important;border:1px solid #8ca7b4;border-radius:7px;font:600 14px/1.3 system-ui,sans-serif!important;box-shadow:none;opacity:1!important;text-decoration:none;letter-spacing:0}
    #mbm-lesson-tools>a:first-child{background:#b9e6cd!important;color:#142939!important}#mbm-lesson-tools>*:focus-visible{outline:3px solid #f2a24a;outline-offset:2px}#mbm-lesson-tools #mbmhud-home{margin-left:auto!important}#mbm-lesson-tools #mbmhud-home span{max-width:18ch}#mbm-lesson-tools #mbmhud-pill{min-height:44px!important}
    body.mbm-lesson-framed #mbm-lesson-tools{position:fixed;top:0;left:0;right:0}
    body.mbm-lesson-framed>.slide-container{height:calc(100vh - var(--mbm-lesson-top,64px) - var(--mbm-lesson-bottom,92px))!important;height:calc(100dvh - var(--mbm-lesson-top,64px) - var(--mbm-lesson-bottom,92px))!important;min-height:120px;margin-top:var(--mbm-lesson-top,64px)!important;align-items:stretch!important;padding:8px 0!important;box-sizing:border-box}
    body.mbm-lesson-framed>.slide-container>.slide{height:100%!important;max-height:100%!important;overflow-y:auto!important;margin:0 auto!important}
    body.mbm-lesson-framed>.controls{max-width:calc(100vw - 20px);flex-wrap:wrap;justify-content:flex-end;gap:6px!important}
    body.mbm-lesson-framed>.controls button{min-height:44px;touch-action:manipulation}
    #mbm-lesson-indicators{display:flex;gap:8px;align-items:center;flex:1 0 100%;flex-wrap:wrap}
    #mbm-lesson-indicators #auto-timer,#mbm-lesson-indicators .xp-wrap{position:static!important;inset:auto!important;transform:none!important;box-shadow:none!important;margin:0!important;min-height:40px;padding:4px 8px!important;font-size:14px!important;flex:0 1 auto}
    #mbm-lesson-indicators .xp-track{width:60px}#mbm-lesson-indicators #auto-timer .at-btn{min-width:40px;min-height:40px;padding:2px!important}
    #mbm-lesson-indicators #progressLabel{position:static!important;inset:auto!important;transform:none!important;max-width:100%;padding:5px 8px;margin:0;color:#e5fbf5;background:transparent;white-space:normal;font-size:12px;line-height:1.3}
    body.mbm-lesson-framed :is(.slide button,.v4-modal button){min-width:44px;min-height:44px;touch-action:manipulation}
    #mbmhud-dock{max-height:calc(100dvh - 24px);overflow:auto}
    @media(max-width:600px){#mbm-lesson-tools #mbmhud-home{font-size:12px!important;max-width:44px;padding:8px!important}#mbm-lesson-tools #mbmhud-home span{display:none}#mbm-lesson-tools #mbmhud-pill{margin-left:auto!important}}
    @media print{#mbm-lesson-tools{display:none!important}body.mbm-lesson-framed>.slide-container{margin-top:0!important;height:auto!important}}
  `;document.head.append(style);
  let bar,frame,controls;const resize=window.ResizeObserver?new ResizeObserver(measure):null;function mount(){
    const hudBack=document.getElementById('mbmhud-back'),hudHome=document.getElementById('mbmhud-home'),hudPill=document.getElementById('mbmhud-pill');
    document.querySelectorAll('a.mbmhome,a[data-lesson-home],a[href="/Lessons/"]').forEach(a=>{if(!a.closest('#mbm-lesson-tools'))a.href=back;});
    if(!hudBack&&!hudPill)return;
    if(!bar){bar=document.createElement('nav');bar.id='mbm-lesson-tools';bar.setAttribute('aria-label','Lesson and teacher tools');document.body.prepend(bar);if(resize)resize.observe(bar);}
    for(const el of[ hudBack,hudHome,hudPill])if(el&&el.parentElement!==bar)bar.append(el);
    if(hudBack){hudBack.href=back;hudBack.setAttribute('aria-label','Return to your lesson selection');hudBack.textContent='← Lessons';}
    frame=document.querySelector('body > .slide-container');controls=document.querySelector('body > .controls');if(resize&&controls)resize.observe(controls);
    if(frame&&controls){document.body.classList.add('mbm-lesson-framed');const indicators=[...document.querySelectorAll('body > #auto-timer,body > .xp-wrap,body > #progressLabel')];if(indicators.length){let row=document.getElementById('mbm-lesson-indicators');if(!row){row=document.createElement('div');row.id='mbm-lesson-indicators';bar.append(row)}for(const indicator of indicators)row.append(indicator)}measure();}
  }
  function measure(){if(!bar||!frame||!controls)return;document.body.style.setProperty('--mbm-lesson-top',Math.ceil(bar.getBoundingClientRect().height)+'px');const rect=controls.getBoundingClientRect();document.body.style.setProperty('--mbm-lesson-bottom',Math.ceil(innerHeight-rect.top+12)+'px');}
  let pending=false;function schedule(){if(pending)return;pending=true;requestAnimationFrame(()=>{pending=false;mount()});}
  mount();const observer=new MutationObserver(mutations=>{if(mutations.some(m=>[...m.addedNodes].some(n=>n.nodeType===1&&!n.closest?.('#mbm-lesson-tools'))))schedule();});observer.observe(document.body,{childList:true});
  addEventListener('resize',schedule);addEventListener('orientationchange',schedule);if(window.visualViewport)visualViewport.addEventListener('resize',schedule);

})();
