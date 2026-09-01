#!/usr/bin/env node
"use strict";
const fs=require("node:fs"),path=require("node:path"),crypto=require("node:crypto");
const{pathToFileURL,fileURLToPath}=require("node:url");
const modules=process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES,browserPath=process.env.RSH_CHROMIUM_PATH;
if(!modules||!browserPath)throw new Error("proved runtime and Chromium required");
const{chromium}=require(path.join(modules,"playwright"));
const ROOT=path.resolve(__dirname,"../../..");
const views=[{name:"phone",width:390,height:844},{name:"tablet",width:768,height:1024},{name:"desktop",width:1365,height:900}];
function human(value){return!!value&&value.trim().length>8&&!/^(BUILD|GROW|LAUNCH) (ASDAN|Science|Humanities|Art) W\d+(?:\s*[-–]\s*W?\d+)?$/i.test(value.trim())&&!/_/.test(value)}
function rowPass(row){return row.horizontalOverflowPx===0&&human(row.title)&&human(row.h1)&&row.homeResolves&&row.cardsResolve&&row.lessonTargetCount>0&&row.logo.present&&row.logo.painted&&row.logo.width==="64"&&row.logo.height==="64"&&row.logo.viewBox==="0 0 100 100"&&row.offlineOnly}
function wholePass(rows,openMarkers,closeMarkers,residual){return rows.length===views.length&&rows.every(rowPass)&&openMarkers>=2&&closeMarkers>=2&&!residual}
(async()=>{
  const rel=process.argv[2],outRel=process.argv[3];if(!rel||!outRel)throw new Error("usage: front_door_gate.js FILE OUTPUT");
  const file=path.resolve(ROOT,rel),source=fs.readFileSync(file,"utf8");
  const forbiddenSource=["fetch(","XMLHttpRequest","serviceWorker","http://","https://","localStorage","sessionStorage","data:"].filter(token=>source.includes(token));
  const browser=await chromium.launch({executablePath:browserPath,headless:true,args:["--no-sandbox"]});
  try{
    const rows=[];
    for(const view of views){
      const page=await browser.newPage({viewport:{width:view.width,height:view.height},colorScheme:"light"}),requests=[];
      page.on("request",request=>requests.push(request.url()));await page.goto(pathToFileURL(file).href,{waitUntil:"load"});
      const row=await page.evaluate(()=>{
        const targets=[...document.querySelectorAll('main a[href$=".html"]')].filter(anchor=>!anchor.classList.contains("mbmhome"));
        const home=document.querySelector("a.mbmhome"),logo=document.querySelector('svg[viewBox="0 0 100 100"]');
        const style=logo?getComputedStyle(logo):null,rect=logo?logo.getBoundingClientRect():null;
        return{title:document.title,h1:document.querySelector("h1")?.textContent?.trim()||"",horizontalOverflowPx:Math.max(0,document.documentElement.scrollWidth-innerWidth),homeHref:home?.href||null,lessonTargetHrefs:targets.map(anchor=>anchor.href),lessonTargetCount:targets.length,logo:{present:!!logo,painted:!!logo&&style.display!=="none"&&style.visibility!=="hidden"&&+style.opacity>0&&rect.width>0&&rect.height>0,width:logo?.getAttribute("width"),height:logo?.getAttribute("height"),viewBox:logo?.getAttribute("viewBox"),label:logo?.getAttribute("aria-label")}};
      });
      row.viewport=view;row.requests=requests;row.homeResolves=!!row.homeHref&&row.homeHref.startsWith("file:")&&fs.existsSync(fileURLToPath(row.homeHref));
      row.cardsResolve=row.lessonTargetHrefs.length>0&&row.lessonTargetHrefs.every(url=>url.startsWith("file:")&&fs.existsSync(fileURLToPath(url)));
      row.offlineOnly=forbiddenSource.length===0&&requests.every(url=>url.startsWith("file:"));row.pass=rowPass(row);rows.push(row);await page.close();
    }
    const openMarkers=(source.match(/<!--n6-nav1:v1-->/g)||[]).length;
    const closeMarkers=(source.match(/<!--\/n6-nav1-->/g)||[]).length;
    const residual=/Local .*review candidate|Nothing in this pack is pushed|\bDRAFT\b|\bCANDIDATE\b/i.test(source);
    const mutateFirst=mutation=>rows.map((row,index)=>index===0?{...row,...mutation}:{...row});
    const controls={
      missingHome:{mutation:"first viewport home does not resolve",fired:!wholePass(mutateFirst({homeResolves:false}),openMarkers,closeMarkers,residual)},
      machineTitle:{mutation:"all titles and h1 values become Launch Science W14",fired:!wholePass(rows.map(row=>({...row,title:"Launch Science W14",h1:"Launch Science W14"})),openMarkers,closeMarkers,residual)},
      brokenTarget:{mutation:"first viewport lesson target does not resolve",fired:!wholePass(mutateFirst({cardsResolve:false}),openMarkers,closeMarkers,residual)},
      missingMarker:{mutation:"one wrapper side is missing",fired:!wholePass(rows,openMarkers,1,residual)},
      forbiddenRuntime:{mutation:"first viewport requests or embeds a prohibited runtime",fired:!wholePass(mutateFirst({offlineOnly:false}),openMarkers,closeMarkers,residual)},
      residualReviewNote:{mutation:"a local-review notice is present",fired:!wholePass(rows,openMarkers,closeMarkers,true)}
    };
    const report={gate:"front-door",file:rel,sha256:crypto.createHash("sha256").update(fs.readFileSync(file)).digest("hex"),chromiumVersion:await browser.version(),lessonTargetSelector:'main a[href$=".html"]:not(.mbmhome)',openMarkers,closeMarkers,forbiddenSource,residualReviewNote:residual,viewports:rows,controls,status:wholePass(rows,openMarkers,closeMarkers,residual)&&Object.values(controls).every(control=>control.fired)?"PASS":"RED"};
    const out=path.resolve(ROOT,outRel);fs.mkdirSync(path.dirname(out),{recursive:true});fs.writeFileSync(out,JSON.stringify(report,null,2)+"\n");
    console.log(JSON.stringify({status:report.status,openMarkers,closeMarkers,forbiddenSource,residual,controls:Object.fromEntries(Object.entries(controls).map(([key,value])=>[key,value.fired])),viewports:rows.map(row=>({name:row.viewport.name,overflow:row.horizontalOverflowPx,home:row.homeResolves,targets:row.lessonTargetCount,cards:row.cardsResolve,logoPainted:row.logo.painted,offline:row.offlineOnly}))},null,2));
    if(report.status!=="PASS")process.exitCode=1;
  }finally{await browser.close()}
})().catch(error=>{console.error(error.stack||String(error));process.exitCode=1});
