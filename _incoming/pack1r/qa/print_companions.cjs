const fs=require('fs'),path=require('path'),{chromium}=require('playwright');
const ROOT=path.resolve(__dirname,'..');
(async()=>{
 const browser=await chromium.launch({headless:true,executablePath:path.join(__dirname,'vendor/chromium/package/bin/chromium'),args:['--no-sandbox','--disable-dev-shm-usage','--disable-gpu','--no-zygote']});
 const page=await browser.newPage({viewport:{width:390,height:844}});
 const pop=JSON.parse(fs.readFileSync(path.join(__dirname,'population.json'))),out=[];
 for(const r of pop){
  const folder=path.dirname(path.join(ROOT,r.html));
  for(const name of ['Knowledge_Organiser','Pupil_Resources']){
   await page.goto('file://'+path.join(folder,name+'.html'));
   // Print every evidence view, including the world map that follows the UK map.
   await page.evaluate(()=>document.querySelectorAll('[data-map-panel]').forEach(x=>x.hidden=false));
   await page.pdf({path:path.join(folder,name+'.pdf'),format:'A4',preferCSSPageSize:true,printBackground:true});out.push({id:r.id,file:name+'.pdf'});
  }
  const landing=path.join(ROOT,'landing',path.dirname(r.target).split('/').pop(),'START_HERE.html');
  await page.goto('file://'+landing);await page.screenshot({path:path.join(__dirname,r.pathway+'-landing-390.png'),fullPage:true});
  await page.addScriptTag({path:path.join(__dirname,'vendor/axe.min.js')});const v=await page.evaluate(async()=>{const r=await axe.run();return r.violations.filter(v=>['serious','critical'].includes(v.impact)).map(v=>v.id);});out.push({id:r.id,landingAxe:v});
 }
 fs.writeFileSync(path.join(__dirname,'print_companions.json'),JSON.stringify(out,null,2));await browser.close();
})();
