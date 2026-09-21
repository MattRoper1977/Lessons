import fs from 'node:fs/promises';
import path from 'node:path';
import {createRequire} from 'node:module';
import {pathToFileURL,fileURLToPath} from 'node:url';
const require=createRequire(path.join(process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES,'@oai/artifact-tool/package.json'));
const {Presentation,PresentationFile}=await import(pathToFileURL(require.resolve('@oai/artifact-tool')).href);
const sharp=require('sharp');
const SKILL='/root/.codex/skills/builtins/presentations';
const {finalizePresentation,resolvePresentationFont,applyPresentationChartFont}=await import(pathToFileURL(SKILL+'/container_tools/artifact_tool_utils.mjs').href);
const ROOT=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const data=JSON.parse(await fs.readFile(path.join(ROOT,'source/content.json'),'utf8'));
const font=resolvePresentationFont({sourceFont:'Arial'});
const stages=['Title','Arrival','Starter','I Do','We Do','I Do 2','We Do 2','Independent','Exit'],timers=[0,4,4,5,5,4,4,10,4];
const routes=['supported','standard','stretch'];
const maps={};
for(const n of ['local','uk','world'])maps[n]=await sharp(await fs.readFile(path.join(ROOT,'qa',n+'.svg'))).resize(1400).png().toBuffer();
for(const [p,d] of Object.entries(data)){
 if(process.env.ONLY_PATHWAY && process.env.ONLY_PATHWAY!==p)continue;
 const color={BUILD:'#4e7a9b',GROW:'#3f7d6e',LAUNCH:'#7a5c9e'}[p];
 const deck=Presentation.create({slideSize:{width:1280,height:720}});
 function text(s,t,x,y,w,h,size=26,bold=false,c='#1f2937'){
  const sh=s.shapes.add({geometry:'textbox',position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'none',width:0}});sh.text=t;sh.text.style={typeface:font,fontSize:size,bold,color:c,autoFit:'none'};return sh;
 }
 function evidence(s,x=60,y=195,w=640,h=335,view='uk'){
  if(p==='LAUNCH'){
   const c=s.charts.add('bar',{position:{left:x,top:y,width:w,height:h},title:'Net UK territorial greenhouse gas emissions',categories:['1990','2023','2024'],series:[{name:'MtCO₂e',values:[790,384,373],fill:color}],barOptions:{direction:'column',grouping:'clustered'},hasLegend:false,dataLabels:{showValue:true,position:'outEnd'}});applyPresentationChartFont(c,{fontFamily:font});
  }else s.images.add({blob:maps[p==='BUILD'?'local':view],contentType:'image/png',alt:p==='BUILD'?'Fictional teaching plan with school, park and library':'Natural Earth coastline map with Middlesbrough marker',fit:'contain',position:{left:x,top:y,width:w,height:h}});
 }
 for(let i=0;i<9;i++){
  const s=deck.slides.add();s.background.fill='#ffffff';
  text(s,`${p} · HUMANITIES · Sum1·W1 · ${timers[i]} MIN`,60,28,1150,32,18,true,color);
  text(s,i===0?d.title:stages[i],60,76,1150,88,i===0?42:40,true);
  if(i!==0)text(s,d.tasks[i],60,162,1150,75,27,true);
  if(i===0){text(s,d.objective,60,195,1110,90,31,true);text(s,d.success.map(x=>'• '+x).join('\n\n'),60,310,750,230,27);text(s,'World of work\n\n'+d.career,870,310,335,230,24,false,color);}
  if(i===1){routes.forEach((r,k)=>{text(s,r.toUpperCase(),60+k*400,248,370,32,20,true,color);d.arrival[r].forEach((q,n)=>text(s,`${n+1}. ${q[1]}`,60+k*400,294+n*77,365,70,21));});text(s,'Choose one route. Point, speak, sign, draw, write or direct an adult.',60,624,1150,36,21);}
  if(i===2){evidence(s,60,258,670,320);text(s,'Words before work\n\n'+d.words.slice(0,4).map(x=>x[0]+' — '+x[1]).join('\n\n'),780,250,420,360,23);}
  if(i===3||i===5){evidence(s,60,255,640,335,i===5?'world':'uk');text(s,d.models[i===3?0:1],750,248,455,345,25);}
  if(i===4||i===6){const c=d.checks[i===4?0:1];evidence(s,60,255,620,335);text(s,c.question,735,246,465,96,27,true);text(s,c.options.map((x,j)=>String.fromCharCode(65+j)+'. '+x).join('\n\n'),735,357,465,250,24);}
  if(i===7){routes.forEach((r,k)=>{text(s,r.toUpperCase(),60+k*400,258,370,35,21,true,color);text(s,d.independent[k],60+k*400,312,360,275,25);});text(s,'Use the map or source, rehearse your explanation, then record your own response.',60,618,1150,42,22);}
  if(i===8){routes.forEach((r,k)=>{text(s,r.toUpperCase(),60+k*400,255,370,35,21,true,color);text(s,d.exit[k][0],60+k*400,311,360,205,28);});text(s,'Show your response to the adult. Agree one next step for the next lesson.',60,555,1140,82,27,true);}
  const source=p==='LAUNCH'?'Data: DESNZ, 5 February 2026, rounded headline totals. 1990 = 373 + 417. Selected years; MtCO₂e.':p==='GROW'?'Map: Natural Earth public-domain land. Simplified equirectangular view; country boundaries omitted.':'Original fictional teaching plan. Not to scale; not a safe walking route.';
  text(s,source,60,673,1080,25,14,false,'#3f5364');text(s,String(i+1)+' / 9',1160,673,70,25,14);
  const notes=[d.tasks[i],`Timing ${timers[i]} minutes; one 40-minute session. Independent starts after 26 minutes.`,d.prep,d.misconception];
  if(i===1)for(const r of routes)notes.push(r.toUpperCase(),...d.arrival[r].map(q=>q[1]+' Help: '+q[2]+' Answer: '+q[3]));
  if(i===4||i===6)notes.push('Expected answer: '+d.checks[i===4?0:1].feedback);
  if(i===8)notes.push(...d.exit.map((x,j)=>routes[j]+': '+x[1]),'EFL: 30-second clip, photo, or one-line context note. Central tags only. Listen / look before tagging (Audience).');
  if(i!==3&&i!==5)notes.push('Space: allow time and a trusted adult. Voice: receive the stage-specific response in the pupil’s chosen mode. Audience: read it back exactly. Influence: '+d.next[i]);
  notes.push(...d.sources.map(x=>x.join('\n')));s.speakerNotes.textFrame.setText(notes.join('\n\n'));
 }
 const qa=path.join(ROOT,'qa','slides-'+p);await fs.mkdir(qa,{recursive:true});
 const candidate=path.join(qa,'candidate.pptx');await(await PresentationFile.exportPptx(deck)).save(candidate);
 for(let i=0;i<9;i++){const png=await deck.export({slide:deck.slides.items[i],format:'png',scale:1});await fs.writeFile(path.join(qa,`slide-${i+1}.png`),new Uint8Array(await png.arrayBuffer()));}
 const final=path.join(ROOT,'packs',`HUM_Summer_1_${p}_Final`,p,'Summer_1/W01/Editable_Slides.pptx');
 const result=await finalizePresentation({workspaceDir:ROOT,candidatePath:candidate,finalPath:final,materializeLiteralChartWorkbooks:true,pythonExecutable:process.env.CODEX_PRIMARY_RUNTIME_PYTHON,integrityValidatorPath:SKILL+'/container_tools/inspect_presentation_package_integrity.py',layoutValidatorPath:SKILL+'/container_tools/inspect_presentation_layout_geometry.py',layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-bullet-geometry','--validate-heading-fit'],fontPolicy:{basis:'design',families:[font]},verifyArtifactToolImport:true,receiptPath:path.join(qa,'validation.json')});
 console.log(JSON.stringify({pathway:p,path:result.finalPath}));
}
