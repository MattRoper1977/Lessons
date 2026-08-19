#!/usr/bin/env node
// SCA-1 CLOSE v2 §1 — hinge answer-key shuffle.
// All 35 science hinge questions author the correct option first. This injects a
// render-time Fisher-Yates shuffle of the option BUTTONS (screen only).
//
// Why this is safe by construction:
//  - Scoring is already IDENTITY-keyed: answer()/softAnswer() compare the button's
//    authored data-i / data-index against the wrapper's data-c / data-correct. Those
//    attributes travel with the node, so DOM order never enters the verdict. Nothing
//    in the estate indexes options positionally (verified: `.option)[`, `children[N]`
//    → 0 occurrences; querySelectorAll('.option') is used only for class clearing).
//  - Print is untouched: hinge option strings are not duplicated into any print
//    section (verified per deck), so authored order is what reaches paper and no
//    A/B/C/D position letters exist.
//  - Read-aloud is untouched: no hinge sits inside a [data-speak-host]; where the
//    speak fallback applies it reads live textContent, i.e. RENDERED order.
//  - Order-dependent sets are exempted via data-shuffle="off" on the wrapper.
//
// Usage: hingeshuffle.js [--dry] file...   |   --strip file...  (reversibility gate)
const fs = require('fs');

const MARK = '<!--sci-hinge-shuffle:v1-->';
const BLOCK = MARK + '<script id="sci-hinge-shuffle">\n' +
`(function(){
  /* SCA-1 CLOSE v2 P1. Hinge options are authored correct-first; shuffle at render,
     screen only. Verdicts are by authored option identity (data-i / data-index), never
     position. Wrappers marked data-shuffle="off" are order-dependent and stay authored. */
  function rint(n){
    try{
      if(window.crypto&&window.crypto.getRandomValues&&n>0){
        var a=new Uint32Array(1),lim=Math.floor(4294967296/n)*n;
        do{window.crypto.getRandomValues(a)}while(a[0]>=lim);
        return a[0]%n;
      }
    }catch(e){}
    return Math.floor(Math.random()*n);
  }
  function shuffle(box){
    var k=[],i;
    for(i=0;i<box.children.length;i++){if(box.children[i].tagName==='BUTTON')k.push(box.children[i]);}
    if(k.length<2)return;
    for(i=k.length-1;i>0;i--){var j=rint(i+1),t=k[i];k[i]=k[j];k[j]=t;}
    for(i=0;i<k.length;i++)box.appendChild(k[i]);
  }
  function run(){
    var w=document.querySelectorAll('.soft,.soft-check'),i,box;
    for(i=0;i<w.length;i++){
      if(w[i].getAttribute('data-shuffle')==='off')continue;
      box=w[i].querySelector('.options');
      if(box)shuffle(box);
    }
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',run);
  else run();
})();
` + '<' + '/script>';

const strip = process.argv.includes('--strip');
const dry = process.argv.includes('--dry');
const files = process.argv.slice(2).filter(a => !a.startsWith('--'));

for (const f of files) {
  const orig = fs.readFileSync(f, 'utf8');
  let s = orig;
  if (strip) {
    s = s.replace(new RegExp(MARK.replace(/[-[\]{}()*+?.,\\^$|#]/g, '\\$&') + '<script id="sci-hinge-shuffle">[\\s\\S]*?<\\/script>\\n?'), '');
  } else if (!s.includes('id="sci-hinge-shuffle"')) {
    const tail = s.lastIndexOf('</body>');
    if (tail === -1) { console.log(JSON.stringify({ f, err: 'no </body>' })); continue; }
    s = s.slice(0, tail) + BLOCK + '\n' + s.slice(tail);
  }
  if (!dry && s !== orig) fs.writeFileSync(f, s);
  console.log(JSON.stringify({ f, changed: s !== orig, mode: strip ? 'strip' : 'patch' }));
}
