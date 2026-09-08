// RX3 family gate: 390x844 touch boot of served lesson routes. Two roots (/Lessons/* -> --root, else --site).
// Per route: page/console errors, the way-home visible in the first viewport without scrolling, staff guidance hidden by default,
// the first slide's h1 count, and the print route markers. Usage: node boot390.cjs --root=<lessons> --site=<site> --routes=a,b --out=json
const {chromium}=require('playwright');const http=require('http'),fs=require('fs'),path=require('path');
const args=Object.fromEntries(process.argv.slice(2).map(a=>{const m=a.match(/^--([^=]+)=(.*)$/);return m?[m[1],m[2]]:[a,true]}));
const ROOT=args.root,SITE=args.site,ROUTES=args.routes.split(',');
const TYPES={'.html':'text/html; charset=utf-8','.js':'text/javascript','.css':'text/css','.json':'application/json','.webp':'image/webp','.png':'image/png','.svg':'image/svg+xml'};
const server=http.createServer((req,r)=>{let u=decodeURIComponent(req.url.split('?')[0]);let f=u.startsWith('/Lessons/')?path.join(ROOT,u.slice(9)):path.join(SITE,u.replace(/^\//,''));
 if(fs.existsSync(f)&&fs.statSync(f).isDirectory())f=path.join(f,'index.html');if(!fs.existsSync(f)){r.writeHead(404).end('nf');return;}r.writeHead(200,{'content-type':TYPES[path.extname(f)]||'application/octet-stream'});r.end(fs.readFileSync(f));});
(async()=>{await new Promise(r=>server.listen(0,'127.0.0.1',r));const origin='http://127.0.0.1:'+server.address().port;const browser=await chromium.launch();const out=[];
 for(const route of ROUTES){const ctx=await browser.newContext({viewport:{width:390,height:844},isMobile:true,hasTouch:true,deviceScaleFactor:3});const page=await ctx.newPage();const errors=[],failed=[];
  page.on('pageerror',e=>errors.push('pageerror: '+String(e).slice(0,160)));page.on('console',m=>{if(m.type()==='error')errors.push('console: '+m.text().slice(0,160));});page.on('requestfailed',q=>failed.push(q.url()));
  page.on('response',rs=>{if(rs.status()>=400)failed.push(rs.status()+' '+rs.url());});
  const t0=Date.now();await page.goto(origin+route,{waitUntil:'load'});await page.waitForTimeout(900);
  const m=await page.evaluate(()=>{const vis=e=>{if(!e)return null;const b=e.getBoundingClientRect();const cs=getComputedStyle(e);return {x:Math.round(b.x),y:Math.round(b.y),w:Math.round(b.width),h:Math.round(b.height),display:cs.display,visibility:cs.visibility,inViewport:b.width>0&&b.height>0&&b.bottom<=innerHeight&&b.top>=0&&b.right<=innerWidth}};
   const home=document.querySelector('.mbmhome');const ta=[...document.querySelectorAll('[data-mbm-guide]')];const taVisible=ta.filter(e=>{const b=e.getBoundingClientRect();return b.width>0&&b.height>0}).length;
   const active=document.querySelector('.slide.active')||document.querySelector('.slide');
   return {title:document.title,home:vis(home),guideTagged:ta.length,guideVisible:taVisible,guideBtn:!!document.querySelector('.mbm-guide-btn'),h1:document.querySelectorAll('h1').length,h1Text:(document.querySelector('h1')||{}).textContent,
    activeSlide:active?active.id:null,scrollW:document.documentElement.scrollWidth,innerW:innerWidth,printArea:!!document.getElementById('print-area'),canonical:(document.querySelector('link[rel=canonical]')||{}).href,hud:!!document.querySelector('script[src="/hud.js"]'),splash:!!document.querySelector('.n6-splash'),storage:Object.keys(localStorage)};});
  out.push({route,ms:Date.now()-t0,errors,failed,...m});await ctx.close();}
 await browser.close();server.close();if(args.out)fs.writeFileSync(args.out,JSON.stringify(out,null,1));
 for(const r of out)console.log(`${r.errors.length===0&&r.failed.length===0&&r.home&&r.home.inViewport&&r.guideVisible===0&&r.h1===1&&r.scrollW<=r.innerW?'PASS':'FAIL'} ${r.route} errors=${r.errors.length} failed=${r.failed.length} home=${r.home?JSON.stringify(r.home):'MISSING'} guide=${r.guideVisible}/${r.guideTagged} btn=${r.guideBtn} h1=${r.h1} overflow=${r.scrollW>r.innerW} storage=${r.storage.length} ${r.errors.concat(r.failed).slice(0,2).join(' | ')}`);
 process.exit(out.every(r=>r.errors.length===0&&r.failed.length===0&&r.home&&r.home.inViewport&&r.guideVisible===0&&r.h1===1&&r.scrollW<=r.innerW)?0:1);})().catch(e=>{console.error(e);process.exit(2)});
