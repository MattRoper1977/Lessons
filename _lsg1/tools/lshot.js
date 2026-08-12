const { chromium } = require('/opt/node22/lib/node_modules/playwright');
(async () => {
  const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome',args:['--no-sandbox']});
  const p=await b.newPage({viewport:{width:1150,height:1500}});
  const [file,sel,out]=process.argv.slice(2);
  await p.goto('file://'+file,{waitUntil:'load'});
  await p.waitForTimeout(600);
  await p.evaluate((sel)=>{const e=document.querySelector(sel); if(e) e.closest('.slide').classList.add('active');},sel);
  await p.waitForTimeout(300);
  const el=await p.$(sel);
  if(el) await el.screenshot({path:out}); else await p.screenshot({path:out});
  await b.close();
})();
