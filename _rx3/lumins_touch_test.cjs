// RX3 P1b.1 — Lumins hold-menu reproduction with REAL touch events (CDP Input.dispatchTouchEvent), 390 px.
// Usage: node lumins_touch_test.cjs <url> [label]
// Asserts on game state via window.__LUMINS.G (present in the original and the remaster), never on the DOM looking right.
const {chromium}=require('playwright');
const url=process.argv[2],label=process.argv[3]||url;
const HOLD_MS=460; // read from the file: var HOLD_MS=460
async function main(){
  const browser=await chromium.launch();
  const ctx=await browser.newContext({viewport:{width:390,height:844},deviceScaleFactor:3,isMobile:true,hasTouch:true,userAgent:'Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Mobile Safari/537.36'});
  const page=await ctx.newPage();const errors=[];page.on('pageerror',e=>errors.push(String(e)));page.on('console',m=>{if(m.type()==='error')errors.push(m.text());});
  await page.goto(url,{waitUntil:'load'});
  const cdp=await ctx.newCDPSession(page);
  const touch=async(type,x,y)=>cdp.send('Input.dispatchTouchEvent',{type,touchPoints:type==='touchEnd'?[]:[{x,y,id:1}]});
  const tap=async(x,y)=>{await touch('touchStart',x,y);await page.waitForTimeout(60);await touch('touchEnd',x,y);};
  const G=()=>page.evaluate(()=>{const g=window.__LUMINS.G;return {state:g.state,focus:g.focus,skills:Object.assign({},g.skills),wheel:g.wheel?{hot:g.wheel.hot}:null,armed:g.armed,lvl:g.lvl};});
  const wheelShown=()=>page.evaluate(()=>document.getElementById('tool-wheel').classList.contains('show'));
  const result={label,url,steps:[]};const note=(k,v)=>{result.steps.push([k,v]);console.log(k,JSON.stringify(v));};
  // 1. reach play state through the real intro button
  await page.waitForFunction(()=>window.__LUMINS&&document.getElementById('go'),null,{timeout:15000});
  const go=await page.$('#go');const gb=await go.boundingBox();await tap(gb.x+gb.width/2,gb.y+gb.height/2);
  await page.waitForFunction(()=>window.__LUMINS.G.state==='play',null,{timeout:10000});
  let g=await G();note('play-state',g);
  const cv=await page.$('#cv');const cb=await cv.boundingBox();
  // a canvas point away from the tools bar: centre of the canvas
  const cx=cb.x+cb.width/2, cy=cb.y+cb.height/2; const pts={A:[cx,cy],B:[cx-70,cy+90],N:[cx+70,cy-90]};
  // wedge geometry from the file: wheelPos = [[0,-72],[69,-22],[43,60],[-43,60],[-69,-22]] in SKILLDEF order; pick the first skill with stock>0
  const skillOrder=await page.evaluate(()=>Array.from(document.querySelectorAll('#tools [data-id],#tools button')).map(b=>b.dataset.id||b.id));
  const tool=Object.keys(g.skills).sort((a,b)=>g.skills[b]-g.skills[a])[0]; // the tool with the most stock, so every scenario has stock left
  const wheelPos=[[0,-72],[69,-22],[43,60],[-43,60],[-69,-22]];
  const SK=['block','dig','bash','build','float'];
  const idx=SK.indexOf(tool);
  note('tool-under-test',{tool,idx,stock:g.skills[tool]});
  const before=g.skills[tool];
  // 2. Scenario A (Matt's phone): hold past HOLD_MS, LIFT, then tap the wedge
  await touch('touchStart',pts.A[0],pts.A[1]);await page.waitForTimeout(HOLD_MS+240);
  const openA=await wheelShown();g=await G();note('A.hold-opens-menu',{shown:openA,wheel:g.wheel});
  const centre=await page.evaluate(()=>{const w=document.getElementById('tool-wheel');return w._centre?{x:w._centre.x,y:w._centre.y}:null;});
  await touch('touchEnd',pts.A[0],pts.A[1]);await page.waitForTimeout(120);
  const stillOpen=await wheelShown();g=await G();note('A.after-lift',{shown:stillOpen,wheel:g.wheel});
  let wx=(centre?centre.x:pts.A[0])+wheelPos[idx][0], wy=(centre?centre.y:pts.A[1])+wheelPos[idx][1];
  await tap(wx,wy);await page.waitForTimeout(200);
  g=await G();const usedA=g.skills[tool]===before-1;note('A.tap-item-selects',{usedA,stockNow:g.skills[tool],shown:await wheelShown()});
  // reset any leftover wheel by tapping far outside, then wait
  await page.waitForTimeout(200);
  // 3. Scenario B (drag-select): hold, move onto the wedge while holding, release
  g=await G();const beforeB=g.skills[tool];
  await touch('touchStart',pts.B[0],pts.B[1]);await page.waitForTimeout(HOLD_MS+240);
  const openB=await wheelShown();const centreB=await page.evaluate(()=>{const w=document.getElementById('tool-wheel');return w._centre?{x:w._centre.x,y:w._centre.y}:null;});
  const bx=(centreB?centreB.x:pts.B[0])+wheelPos[idx][0], by=(centreB?centreB.y:pts.B[1])+wheelPos[idx][1];
  await touch('touchMove',bx,by);await page.waitForTimeout(80);g=await G();const hotB=g.wheel?g.wheel.hot:null;
  await touch('touchEnd',bx,by);await page.waitForTimeout(200);g=await G();
  const usedB=g.skills[tool]===beforeB-1;note('B.drag-select',{openB,hotB,usedB,stockNow:g.skills[tool]});
  // 4. Negative control: hold, lift, tap far outside -> menu closed, stock unchanged
  g=await G();const beforeN=g.skills[tool];
  await touch('touchStart',pts.N[0],pts.N[1]);await page.waitForTimeout(HOLD_MS+240);await touch('touchEnd',pts.N[0],pts.N[1]);await page.waitForTimeout(120);
  const openN=await wheelShown();await tap(cb.x+20,cb.y+20);await page.waitForTimeout(200);
  g=await G();note('N.outside-tap-closes',{openBeforeTap:openN,shownAfter:await wheelShown(),stockUnchanged:g.skills[tool]===beforeN});
  // 5. Parity: mouse hold + release + click the wedge (desktop path) — new context without touch
  const ctx2=await browser.newContext({viewport:{width:1280,height:800}});const p2=await ctx2.newPage();await p2.goto(url,{waitUntil:'load'});
  await p2.waitForFunction(()=>window.__LUMINS&&document.getElementById('go'),null,{timeout:15000});await p2.click('#go');
  await p2.waitForFunction(()=>window.__LUMINS.G.state==='play',null,{timeout:10000});
  const c2=await (await p2.$('#cv')).boundingBox();const mx=c2.x+c2.width/2,my=c2.y+c2.height/2;
  let g2=await p2.evaluate(()=>Object.assign({},window.__LUMINS.G.skills));const tool2=Object.keys(g2).sort((a,b)=>g2[b]-g2[a])[0];const i2=SK.indexOf(tool2);const b2=g2[tool2];
  await p2.mouse.move(mx,my);await p2.mouse.down();await p2.waitForTimeout(HOLD_MS+240);
  const mOpen=await p2.evaluate(()=>document.getElementById('tool-wheel').classList.contains('show'));
  const mc=await p2.evaluate(()=>{const w=document.getElementById('tool-wheel');return w._centre?{x:w._centre.x,y:w._centre.y}:null;});
  // drag-select path
  await p2.mouse.move((mc?mc.x:mx)+wheelPos[i2][0],(mc?mc.y:my)+wheelPos[i2][1],{steps:4});await p2.waitForTimeout(80);await p2.mouse.up();await p2.waitForTimeout(150);
  g2=await p2.evaluate(()=>Object.assign({},window.__LUMINS.G.skills));const mDrag=g2[tool2]===b2-1;
  // release-then-click path
  const b3=g2[tool2];await p2.mouse.move(mx-70,my+90);await p2.mouse.down();await p2.waitForTimeout(HOLD_MS+240);await p2.mouse.up();await p2.waitForTimeout(120);
  const mc3=await p2.evaluate(()=>{const w=document.getElementById('tool-wheel');return w._centre?{x:w._centre.x,y:w._centre.y}:null;});
  const mOpenAfterRelease=await p2.evaluate(()=>document.getElementById('tool-wheel').classList.contains('show'));
  await p2.mouse.click((mc3?mc3.x:mx-70)+wheelPos[i2][0],(mc3?mc3.y:my+90)+wheelPos[i2][1]);await p2.waitForTimeout(150);
  g2=await p2.evaluate(()=>Object.assign({},window.__LUMINS.G.skills));const mClick=g2[tool2]===b3-1;
  note('M.mouse-parity',{mOpen,mDrag,mOpenAfterRelease,mClick,tool2});
  result.errors=errors;result.verdict={A_tap_after_lift:usedA,B_drag_select:usedB,negative_control_ok:!(await wheelShown()),mouse_drag:mDrag,mouse_click_after_release:mClick};
  console.log('VERDICT',JSON.stringify(result.verdict),'errors',errors.length);
  require('fs').writeFileSync(process.env.OUT||'/dev/null',JSON.stringify(result,null,1));
  await browser.close();
}
main().catch(e=>{console.error('HARNESS-ERROR',e);process.exit(2);});
