const {chromium}=require('./gc1-runtime/node_modules/playwright');
const fs=require('fs'),path=require('path'),http=require('http'),assert=require('node:assert/strict');
const live=process.argv.includes('--live');
const root=path.resolve('gc1-p6'),site=path.resolve('gc1-regfix-site');
const key='ICT/Teaching_Packs/index.html#grow-computing';
const expected=JSON.parse(fs.readFileSync('recovery/gc1-p6-row.json'));
const report={mode:live?'live':'candidate',measured_at:new Date().toISOString(),catalogue:[],prints:[],errors:[]};
let server,browser;
(async()=>{
 let base='https://madebymatt.uk';
 if(!live){server=http.createServer((req,res)=>{const url=new URL(req.url,'http://local');let rel=decodeURIComponent(url.pathname);let p=path.join(rel.startsWith('/Lessons/')?root:site,rel.startsWith('/Lessons/')?rel.slice(9):rel);if(fs.existsSync(p)&&fs.statSync(p).isDirectory())p=path.join(p,'index.html');if(!fs.existsSync(p)){res.writeHead(404);res.end();return;}const types={'.html':'text/html','.js':'text/javascript','.json':'application/json','.css':'text/css','.svg':'image/svg+xml','.pdf':'application/pdf'};res.writeHead(200,{'content-type':types[path.extname(p)]||'application/octet-stream'});fs.createReadStream(p).pipe(res)});await new Promise(r=>server.listen(0,'127.0.0.1',r));base='http://127.0.0.1:'+server.address().port;}
 const launch={args:['--no-sandbox']};
 if(live&&process.env.HTTPS_PROXY){const proxy=new URL(process.env.HTTPS_PROXY);launch.proxy={server:proxy.origin};if(proxy.username){launch.proxy.username=decodeURIComponent(proxy.username);launch.proxy.password=decodeURIComponent(proxy.password);}}
 browser=await chromium.launch(launch);
 for(const width of [390,1280]){
  // The runtime HTTPS proxy CA is not in Chromium's store; Python byte fetches
  // separately retain certificate verification. This probe measures rendering.
  const page=await browser.newPage({ignoreHTTPSErrors:live,viewport:{width,height:844}});page.on('pageerror',e=>report.errors.push(String(e)));
  for(const q of ['71638','Scratch','GROW Computing']){
   await page.goto(base+'/Lessons/?q='+encodeURIComponent(q),{waitUntil:'domcontentloaded',timeout:60000});
   const card=page.locator('article.card').filter({has:page.locator('a[href="'+key+'"]')});
   await card.waitFor({state:'visible'});assert.equal(await card.count(),1);assert.ok((await card.innerText()).includes(expected.desc));
   assert.equal(await card.locator('h3 a').getAttribute('href'),key);
   assert.equal(await card.locator('.chips').innerText().then(t=>/Autumn|Spring|Summer/.test(t)),false);
   report.catalogue.push({width,query:q,count:1,title:await card.locator('h3').innerText()});
  }
  await page.locator('article.card').filter({has:page.locator('a[href="'+key+'"]')}).locator('h3 a').click({noWaitAfter:true});
  await page.waitForURL('**/Lessons/'+key,{waitUntil:'domcontentloaded',timeout:60000});
  assert.ok(page.url().endsWith('/Lessons/'+key));await page.locator('#grow-computing').waitFor({state:'visible'});
  assert.ok(await page.locator('#grow').count());
  await page.close();
 }
 if(live){
  for(let w=1;w<=8;w++){
   const page=await browser.newPage({ignoreHTTPSErrors:true,viewport:{width:390,height:844}});page.on('pageerror',e=>report.errors.push(String(e)));
   const n=String(w).padStart(2,'0');const url=base+`/Lessons/ICT/Teaching_Packs/GROW_Computing/Week_${n}/GROW_Week_${n}_Interactive.html`;
   const response=await page.goto(url,{waitUntil:'domcontentloaded',timeout:60000});assert.equal(response.status(),200);
   await page.evaluate(()=>window.dispatchEvent(new Event('beforeprint')));await page.emulateMedia({media:'print'});
   const paper=page.locator('.print-record .gc1-paper');assert.equal(await paper.count(),1);assert.ok(await paper.isVisible());
   const text=await paper.innerText();assert.ok(text.length>1000);assert.match(text,/paper route/i);assert.match(text,/completion/i);
   const heading=await paper.locator('h1').innerText();assert.match(heading,new RegExp('Week\\s+0?'+w+'\\b','i'));
   report.prints.push({week:w,url,status:200,visible:true,characters:text.length,heading});await page.close();
  }
 }
 assert.equal(report.errors.length,0);report.status='PASS';
})().catch(e=>{report.status='FAIL';report.failure=String(e.stack||e);process.exitCode=1}).finally(async()=>{if(browser)await browser.close();if(server)server.close();fs.writeFileSync(`recovery/gc1-p6-browser-${live?'live':'candidate'}.json`,JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report));});
