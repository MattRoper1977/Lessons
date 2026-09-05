// Static DOM/event verification only: no browser layout, native dialog focus or playback.
const fs=require('fs'),path=require('path'),vm=require('vm'),assert=require('node:assert/strict');
const {parseHTML}=require('linkedom');
const root=path.resolve(__dirname,'../..');
const configs=JSON.parse(fs.readFileSync(path.join(__dirname,'RESOURCE_CONTENT.json'),'utf8'));
const script=fs.readFileSync(path.join(root,'Science_Teesside/Launch/resources/pack.js'),'utf8');
const report=[];
for(const c of configs){
 const {document,window}=parseHTML(fs.readFileSync(path.join(root,c.online_path),'utf8'));
 Object.defineProperty(document,'readyState',{value:'loading',configurable:true});
 const context=vm.createContext({document,window,console});
 vm.runInContext(script,context,{filename:'pack.js'});
 const click=e=>{const event=new window.Event('click',{bubbles:true,cancelable:true});e.dispatchEvent(event);return event;};
 assert.equal(document.querySelectorAll('#wedo2 [data-open-science-pack]').length,0);
 document.dispatchEvent(new window.Event('DOMContentLoaded'));
 assert.equal(document.querySelectorAll('#wedo2 [data-open-science-pack]').length,1);
 assert.equal(document.querySelectorAll('.slide[data-title="Title"] [data-open-science-pack]').length,1);
 const dialog=document.getElementById('mbm-science-pack');
 const opener=document.querySelector('.slide[data-title="Title"] [data-open-science-pack]');
 // Unsupported native dialogs retain the ordinary, fully formed resource-page link.
 assert.equal(click(opener).defaultPrevented,false);
 assert(fs.existsSync(path.resolve(root,path.dirname(c.online_path),opener.getAttribute('href'))));
 let opens=0;dialog.showModal=()=>{opens++;dialog.setAttribute('open','');};
 assert.equal(click(opener).defaultPrevented,true);assert.equal(opens,1);
 let deckKeys=0;document.addEventListener('keydown',()=>deckKeys++);
 const textarea=dialog.querySelector('textarea');textarea.value='Our first reason';
 const key=new window.Event('keydown',{bubbles:true,cancelable:true});key.key='ArrowRight';textarea.dispatchEvent(key);assert.equal(deckKeys,0);
 assert.equal(dialog.querySelectorAll('iframe').length,0);
 const button=dialog.querySelector('[data-play-video]');click(button);
 const frame=dialog.querySelector('iframe');assert(frame);
 assert.equal(frame.getAttribute('src'),'https://www.youtube-nocookie.com/embed/'+c.video.id+'?rel=0');
 assert(frame.getAttribute('title').includes(c.video.title));
 assert(button.hidden);assert(dialog.querySelector('details details[open] img'));
 dialog.dispatchEvent(new window.Event('close'));
 assert.equal(dialog.querySelectorAll('iframe').length,0);assert.equal(button.hidden,false);
 assert.equal(textarea.value,'Our first reason');
 report.push({lesson:c.id,initialisation_after_existing_mount:'PASS',resource_entry_no_duplicates:'PASS',ordinary_link_fallback:'PASS',dialog_enhancement_dispatch:'PASS',deck_key_propagation_isolated:'PASS',video_created_only_on_action:'PASS',correct_video_title_and_target:'PASS',embedded_no_video_model_present:'PASS',close_removes_frame_preserves_attempt:'PASS'});
}
const result={method:'LinkeDOM parsing and actual DOM events. showModal is a narrow dispatch stub; it does not verify native browser focus containment or rendering.',lessons:report,limits:['No actual browser, keyboard or touch hardware used.','No video playback, native dialog focus or print pagination verified.']};
fs.writeFileSync(path.join(__dirname,'DOM_CHECK_RESULTS.json'),JSON.stringify(result,null,2)+'\n');
console.log('PASS: 15 lessons × 9 scoped DOM/event checks; native browser behaviour remains unverified.');
