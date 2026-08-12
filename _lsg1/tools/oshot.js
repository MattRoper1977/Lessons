const { chromium } = require('/opt/node22/lib/node_modules/playwright');
(async () => {
  const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome',args:['--no-sandbox']});
  const p=await b.newPage({viewport:{width:1120,height:1700}});
  await p.goto('file://'+process.argv[2],{waitUntil:'load'});
  await p.waitForTimeout(600);
  const r=await p.evaluate(()=>{
    const box=document.getElementById('oslab-W5L2');
    if(!box) return {err:'missing'};
    box.closest('.slide').classList.add('active');
    box.querySelector('.os-predict .os-btn').click();
    box.querySelectorAll('.os-row')[1].querySelectorAll('.os-btn').forEach(b=>b.click());
    box.querySelector('.os-glitch .os-btn[data-fix="1"]').click();
    const bad=[];
    box.querySelectorAll('.os-btn').forEach(el=>{const cs=getComputedStyle(el);
      if(cs.color===cs.backgroundColor) bad.push(el.textContent.trim().slice(0,18));
      if(cs.color==='rgb(255, 255, 255)'&&/255, 255, 255|250, 248|236, 230/.test(cs.backgroundColor)) bad.push('white-on-light:'+el.textContent.trim().slice(0,16));});
    return {frozen:box.querySelectorAll('#os-list li').length, bad};
  });
  await p.waitForTimeout(250);
  const el=await p.$('#oslab-W5L2'); if(el) await el.screenshot({path:process.argv[3]});
  console.log(JSON.stringify(r));
  await b.close();
})();
