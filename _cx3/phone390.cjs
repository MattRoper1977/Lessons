// CX3 phone render gate. 390x844 touch boot of served lesson routes; walks the deck with ArrowRight, measures the hook
// (.microfilm offsetHeight, .xr-hook/.frame svg heights) on every slide, presses the first control of every .xr-widget it meets.
// Usage: node phone390.cjs --root=<lessons> --site=<site> --list=<routes file> --out=<json>
const {chromium}=require('playwright');const http=require('http'),fs=require('fs'),path=require('path');
const args=Object.fromEntries(process.argv.slice(2).map(a=>{const m=a.match(/^--([^=]+)=(.*)$/);return m?[m[1],m[2]]:[a,true]}));
const ROOT=args.root,SITE=args.site,ROUTES=fs.readFileSync(args.list,'utf8').split('\n').map(s=>s.trim()).filter(Boolean);
const TYPES={'.html':'text/html; charset=utf-8','.js':'text/javascript','.css':'text/css','.json':'application/json','.webp':'image/webp','.png':'image/png','.svg':'image/svg+xml','.pdf':'application/pdf'};
const server=http.createServer((req,r)=>{let u=decodeURIComponent(req.url.split('?')[0]);let f=u.startsWith('/Lessons/')?path.join(ROOT,u.slice(9)):path.join(SITE,u.replace(/^\//,''));
 if(fs.existsSync(f)&&fs.statSync(f).isDirectory())f=path.join(f,'index.html');if(!fs.existsSync(f)){r.writeHead(404).end('nf');return;}r.writeHead(200,{'content-type':TYPES[path.extname(f)]||'application/octet-stream'});r.end(fs.readFileSync(f));});
(async()=>{await new Promise(r=>server.listen(0,'127.0.0.1',r));const origin='http://127.0.0.1:'+server.address().port;const browser=await chromium.launch();const out=[];
 for(const route of ROUTES){const ctx=await browser.newContext({viewport:{width:390,height:844},isMobile:true,hasTouch:true,deviceScaleFactor:3});const page=await ctx.newPage();const errors=[],failed=[];
  page.on('pageerror',e=>errors.push('pageerror: '+String(e).slice(0,200)));page.on('console',m=>{if(m.type()==='error')errors.push('console: '+m.text().slice(0,200));});
  page.on('response',rs=>{if(rs.status()>=400)failed.push(rs.status()+' '+rs.url());});
  const rec={route,errors,failed,slides:0,microfilm:[],hookSvg:[],widgets:[],pressed:0,pressErrors:0};
  try{await page.goto(origin+route,{waitUntil:'load',timeout:30000});await page.waitForTimeout(700);
   // dismiss splash / title if present
   const seen=new Set();
   for(let step=0;step<14;step++){
     const m=await page.evaluate(()=>{const vis=e=>{const b=e.getBoundingClientRect();const cs=getComputedStyle(e);return b.width>0&&b.height>0&&cs.visibility!=='hidden'&&cs.display!=='none'};
       const act=document.querySelector('.slide.active,.slide.on')||[...document.querySelectorAll('.slide')].find(vis);const id=act?(act.id||act.dataset.title||[...document.querySelectorAll('.slide')].indexOf(act)):null;
       const mf=[...document.querySelectorAll('.microfilm')].filter(vis).map(e=>({h:e.offsetHeight,w:e.offsetWidth,slide:id}));
       const hs=[...document.querySelectorAll('.xr-hook svg,.frame svg,.microfilm svg')].filter(vis).map(e=>({h:Math.round(e.getBoundingClientRect().height),slide:id}));
       const ws=[...document.querySelectorAll('.xr-widget')].filter(vis).map((e,i)=>{const b=e.querySelector('button,[role=button],select,input');return {key:(e.id||'')+'@'+id+'#'+i,k:i,id:e.id||null,slide:id,ctl:b?(b.id||b.textContent.trim().slice(0,40)):null}});
       return {id,mf,hs,ws,n:document.querySelectorAll('.slide').length};});
     rec.slides=m.n; if(m.id!==null&&seen.has(m.id)&&step>0)break; seen.add(m.id);
     rec.microfilm.push(...m.mf);rec.hookSvg.push(...m.hs);
     for(const w of m.ws){if(rec.widgets.find(x=>x.key===w.key))continue;const before=errors.length;
       try{const h=await page.evaluateHandle((k)=>{const vis=e=>{const b=e.getBoundingClientRect();return b.width>0&&b.height>0};const list=[...document.querySelectorAll('.xr-widget')].filter(vis);const e=list[k];return e?e.querySelector('button,[role=button],select,input'):null;},w.k);
         const el=h.asElement(); if(el){await el.scrollIntoViewIfNeeded().catch(()=>{});await el.click({timeout:2000,force:true}).catch(async()=>{await el.dispatchEvent('click')});await page.waitForTimeout(250);rec.pressed++;}
       }catch(e){rec.harness=(rec.harness||[]).concat(String(e).slice(0,120));}
       const d=errors.length-before; rec.pressErrors+=d; rec.widgets.push({...w,errAfterPress:d});}
     await page.keyboard.press('ArrowRight');await page.waitForTimeout(220);
   }
  }catch(e){errors.push('harness: '+String(e).slice(0,200));}
  rec.microfilmMaxH=rec.microfilm.length?Math.max(...rec.microfilm.map(x=>x.h)):null;rec.hookSvgMaxH=rec.hookSvg.length?Math.max(...rec.hookSvg.map(x=>x.h)):null;
  out.push(rec);await ctx.close();
  console.log(`${route.split('/').pop()} slides=${rec.slides} microfilmMaxH=${rec.microfilmMaxH} hookSvgMaxH=${rec.hookSvgMaxH} widgets=${rec.widgets.length} pressed=${rec.pressed} pressErr=${rec.pressErrors} errors=${errors.length} failed=${failed.length} ${errors.slice(0,2).join(' | ')} ${failed.slice(0,2).join(' | ')}`);}
 await browser.close();server.close();if(args.out)fs.writeFileSync(args.out,JSON.stringify(out,null,1));})().catch(e=>{console.error(e);process.exit(2)});
