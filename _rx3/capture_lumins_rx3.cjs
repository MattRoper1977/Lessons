/* Local re-run of Site domain-split/play/capture.cjs for Lumins only: same viewport, same ordinary player
 * inputs (key 4, two cell clicks), same 20 s trim and poster steps; served from the lane A tree + Site root. */
const {chromium}=require('playwright');const fs=require('fs'),path=require('path'),crypto=require('crypto'),cp=require('child_process'),http=require('http');
const ROOT='/home/user/lessons-lumins',SITE='/tmp/site-2eaf',out=process.argv[2];fs.mkdirSync(out,{recursive:true});
const TYPES={'.html':'text/html; charset=utf-8','.js':'text/javascript','.css':'text/css','.webp':'image/webp','.png':'image/png','.svg':'image/svg+xml','.json':'application/json'};
function serve(){return new Promise((res,rej)=>{const s=http.createServer((req,r)=>{let url=decodeURIComponent(req.url.split('?')[0]);let file=url.startsWith('/Lessons/')?path.join(ROOT,url.slice(9)):path.join(SITE,url.replace(/^\//,''));try{if(fs.existsSync(file)&&fs.statSync(file).isDirectory())file=path.join(file,'index.html');if(!fs.existsSync(file)){r.writeHead(404).end('nf');return}r.writeHead(200,{'Content-Type':TYPES[path.extname(file)]||'application/octet-stream'});fs.createReadStream(file).pipe(r)}catch(e){r.writeHead(500).end()}});s.listen(0,'127.0.0.1',()=>res(s))})}
const wait=ms=>new Promise(r=>setTimeout(r,ms));const hash=p=>crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
async function shot(page,name){await page.screenshot({path:path.join(out,name+'.png')});fs.writeFileSync(path.join(out,name+'.txt'),await page.locator('body').innerText());}
async function optional(page,selector){const l=page.locator(selector);if(await l.count()&&await l.first().isVisible()){await l.first().click();await wait(300);return true;}return false;}
(async()=>{const server=await serve();const base='http://127.0.0.1:'+server.address().port;const browser=await chromium.launch({args:['--enable-webgl','--use-angle=swiftshader','--enable-unsafe-swiftshader']});
 const viewport={width:960,height:540};const dir=path.join(out,'lumins');fs.mkdirSync(dir,{recursive:true});const context=await browser.newContext({viewport,recordVideo:{dir,size:viewport}});const page=await context.newPage();page.setDefaultTimeout(10000);const began=Date.now();let clipStart=0;const errors=[];page.on('pageerror',e=>errors.push(String(e).slice(0,160)));page.on('console',m=>{if(m.type()==='error')errors.push('console: '+m.text().slice(0,160))});
 const item={id:'lumins',title:'Lumins',route:'/Lessons/Games/Lumins.html',status:'needs-visual-review',viewport,device:'Headless Chromium (Playwright 1.56.1), local re-run of the CI capture script; fresh isolated context',captured_at:new Date().toISOString()};
 await page.goto(base+'/404.html');if(await page.evaluate(()=>localStorage.length)!==0)throw Error('Capture profile was not empty');
 await page.goto(base+'/Lessons/Games/Lumins.html',{waitUntil:'load'});await wait(2800);await shot(page,'lumins-start');
 if(!await optional(page,'#go')){const first=page.getByText(/First Steps/).first();if(await first.isVisible())await first.click();await page.locator('#go').click();}
 await shot(page,'lumins-ready');clipStart=(Date.now()-began)/1000;item.trim_start_seconds=clipStart;
 await page.keyboard.press('4');const box=await page.locator('#cv').boundingBox();
 for(const [c,r] of [[15,13],[17,12]]){await page.mouse.click(box.x+(c+.5)*box.width/40,box.y+(r+.5)*box.height/24);await wait(300);}
 await wait(17000);item.description='Build two bridge sections across the first gap and guide Lumins toward the rescue portal.';
 await wait(Math.max(0,21000-(Date.now()-began-clipStart*1000)));await shot(page,'lumins-after');
 item.storage_keys=await page.evaluate(()=>Object.keys(localStorage));item.errors=errors;
 const video=page.video();await context.close();const src=await video.path();item.source_recording='lumins/'+path.basename(src);
 const dest=path.join(out,'lumins.mp4');cp.execFileSync('ffmpeg',['-y','-ss',String(clipStart),'-i',src,'-t','20','-an','-c:v','libx264','-preset','medium','-crf','24','-pix_fmt','yuv420p','-movflags','+faststart',dest],{stdio:'ignore'});
 cp.execFileSync('ffmpeg',['-y','-ss','8','-i',dest,'-frames:v','1','-vf','scale=960:-2','-quality','82',path.join(out,'lumins.webp')],{stdio:'ignore'});
 for(const t of [2,6,10,14,18]){cp.execFileSync('ffmpeg',['-y','-ss',String(t),'-i',dest,'-frames:v','1',path.join(out,'frame-'+t+'.png')],{stdio:'ignore'});}
 const probe=JSON.parse(cp.execFileSync('ffprobe',['-v','error','-show_format','-show_streams','-of','json',dest],{encoding:'utf8'}));item.duration_seconds=Number(probe.format.duration);item.codec=probe.streams[0].codec_name;item.bytes=fs.statSync(dest).size;item.video_sha256=hash(dest);item.poster_sha256=hash(path.join(out,'lumins.webp'));
 fs.writeFileSync(path.join(out,'item.json'),JSON.stringify(item,null,2));console.log(JSON.stringify(item,null,1));await browser.close();server.close();})().catch(e=>{console.error(e);process.exit(1)});
