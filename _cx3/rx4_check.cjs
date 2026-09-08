// RX4 node checks for SCI_L_W13L2 (Punnett lab): predict -> act -> observe -> explain with retained evidence.
// Usage: node rx4_check.cjs <lessons root> <site root>   (exit 0 = all checks pass; prints one line per check)
const {chromium}=require('playwright');const http=require('http'),fs=require('fs'),path=require('path');
const [ROOT,SITE]=process.argv.slice(2);const ROUTE='/Lessons/Science_Teesside/Launch/W8-W13_2026-27/SCI_L_W13L2_Punnett_Square_Explore.html';
const server=http.createServer((req,r)=>{let u=decodeURIComponent(req.url.split('?')[0]);let f=u.startsWith('/Lessons/')?path.join(ROOT,u.slice(9)):path.join(SITE,u.replace(/^\//,''));if(fs.existsSync(f)&&fs.statSync(f).isDirectory())f=path.join(f,'index.html');if(!fs.existsSync(f)){r.writeHead(404).end('nf');return;}r.writeHead(200,{'content-type':f.endsWith('.html')?'text/html; charset=utf-8':f.endsWith('.js')?'text/javascript':'application/octet-stream'});r.end(fs.readFileSync(f));});
(async()=>{await new Promise(r=>server.listen(0,'127.0.0.1',r));const origin='http://127.0.0.1:'+server.address().port;const browser=await chromium.launch();const ctx=await browser.newContext({viewport:{width:390,height:844},isMobile:true,hasTouch:true});const page=await ctx.newPage();const errors=[];page.on('pageerror',e=>errors.push(String(e).slice(0,160)));page.on('console',m=>{if(m.type()==='error')errors.push(m.text().slice(0,160))});
 await page.goto(origin+ROUTE,{waitUntil:'load'});await page.waitForTimeout(600);await page.evaluate(()=>window.mbmShowSlide&&window.mbmShowSlide(4));await page.waitForTimeout(300);
 const sel=async(c,v)=>{await page.selectOption(`[data-control="${c}"]`,v);await page.waitForTimeout(60);};const q=c=>`[data-control="${c}"]`;const results=[];const check=(id,ok,note)=>{results.push([id,ok,note]);console.log((ok?'PASS ':'FAIL ')+id+' — '+note)};
 // gametes: top Pp, side Pp (guided)
 await sel('punnett-top-0','P');await sel('punnett-top-1','p');await sel('punnett-side-0','P');await sel('punnett-side-1','p');await page.click(q('punnett-check-gametes'));await page.waitForTimeout(150);
 const gr=await page.getAttribute('[data-science-lab]','data-gametes-ready');check('C0-gametes',gr==='true','gametes accepted (control, both files)');
 // C1: after gametes, a box's allele selects must stay disabled until a prediction is committed
 const hasPredict=await page.$(q('punnett-cell-0-0-predict'));const topDisabled=await page.$eval(q('punnett-cell-0-0-top'),e=>e.disabled);
 check('C1-predict-before-reveal',!!hasPredict&&topDisabled,'allele selects disabled until the box prediction is committed (predict select present='+!!hasPredict+', top disabled='+topDisabled+')');
 if(hasPredict){await sel('punnett-cell-0-0-predict','PP');}
 const topEnabled=hasPredict?await page.$eval(q('punnett-cell-0-0-top'),e=>!e.disabled):false;check('C1b-act-after-predict',topEnabled,'alleles enabled after the prediction');
 await sel('punnett-cell-0-0-top','P');await sel('punnett-cell-0-0-side','P');
 // C2: outcome line records prediction + result; explanation select enabled and recorded
 const outcome=await page.$(q('punnett-cell-0-0-outcome'));const otext=outcome?await outcome.textContent():'';check('C2-outcome-line',/Predicted PP · Result PP/.test(otext),'outcome line: '+JSON.stringify(otext.slice(0,80)));
 const hasExplain=await page.$(q('punnett-cell-0-0-explain'));if(hasExplain)await sel('punnett-cell-0-0-explain','dominant');
 const explained=await page.$eval('td[data-punnett-cell="0-0"]',e=>e.dataset.explain||'');check('C2b-explanation-retained',explained==='dominant','td[data-explain]='+JSON.stringify(explained));
 // finish the other boxes: predict then reveal (Pp x Pp: top P p / side P p)
 const plan=[['0-1','Pp','p','P'],['1-0','Pp','P','p'],['1-1','pp','p','p']];
 for(const [c,pred,t,s] of plan){if(hasPredict){await sel('punnett-cell-'+c+'-predict',pred);}await sel('punnett-cell-'+c+'-top',t);await sel('punnett-cell-'+c+'-side',s);if(hasExplain)await sel('punnett-cell-'+c+'-explain',pred==='pp'?'recessive':'combine');}
 await page.click(q('punnett-check-boxes'));await page.waitForTimeout(150);
 const sq=await page.getAttribute('[data-science-lab]','data-square-correct');const prob=await page.$eval(q('punnett-probabilities'),e=>e.hidden?'':e.textContent);
 check('C4-probabilities-regression',sq==='true'&&/pp: 1\/4 = 25%/.test(prob),'square correct='+sq+', probabilities shown='+/25%/.test(prob));
 // C5: retained evidence on the host: four boxes with prediction+result+explain
 const ev=await page.getAttribute('[data-science-lab]','data-evidence');let evj=null;try{evj=JSON.parse(ev||'null')}catch(e){}
 check('C5-evidence-retained',!!evj&&evj.boxes&&evj.boxes.length===4&&evj.boxes.every(b=>b.prediction&&b.result&&b.explain),'host[data-evidence]='+(ev?ev.slice(0,90):'absent'));
 // C3: the independent button opens the NEW cross (Pp x pp) and records the stage
 await page.evaluate(()=>window.mbmShowSlide&&window.mbmShowSlide(6));await page.waitForTimeout(200);
 const clicked=await page.evaluate(()=>{const b=document.querySelector('[data-control="punnett-open-independent"]')||document.querySelector('section#stage-6 button');if(!b)return false;b.click();return true;});await page.waitForTimeout(300);
 const crossVal=await page.$eval(q('punnett-cross'),e=>e.value);const stage=await page.getAttribute('[data-science-lab]','data-stage');const cap=await page.$eval('[data-control="punnett-grid"] caption',e=>e.textContent);
 check('C3-independent-new-cross',crossVal==='Pp-pp'&&stage==='independent'&&/Side parent: pp/.test(cap),'cross='+crossVal+' stage='+stage+' caption='+JSON.stringify(cap));
 check('C6-no-errors',errors.length===0,'console/page errors: '+errors.length+(errors[0]?' '+errors[0]:''));
 await browser.close();server.close();process.exit(results.every(r=>r[1])?0:1);})().catch(e=>{console.error('harness',e);process.exit(2)});
