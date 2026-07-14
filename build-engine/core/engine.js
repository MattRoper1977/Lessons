/* Build Lesson Engine · core/engine.js
   Renders a full lesson from window.LESSON (JSON). One fix here updates every lesson.
   Requires: core/styles.css loaded; window.LESSON defined; <div id="app"></div>. */
(function(){
'use strict';
if (typeof window === 'undefined' || !window.LESSON) { return; }
var L = window.LESSON;
var XP_PER = 12;
var current = 0, xp = 0, audioCtx = null;

function icons(str){ return str.split(' ').map(function(i){return '<span>'+i+'</span>';}).join(''); }
function loItems(arr){ return arr.map(function(t){return '<div class="lo-item"><span class="chk">\u2713</span> '+t+'</div>';}).join(''); }
function idoCards(arr){ return arr.map(function(c){return '<div class="gcard '+c[0]+'"><h3>'+c[1]+' '+c[2]+'</h3><p>'+c[3]+'</p></div>';}).join(''); }
function stations(arr){ return arr.map(function(s,i){return '<div class="station"><h3>Station '+(i+1)+' \u00b7 '+s[0]+'</h3><p>'+s[1]+'</p></div>';}).join(''); }
function mcqs(arr){ return arr.map(function(m){
 var opts = m[3].map(function(t,i){return '<button class="opt" data-i="'+i+'">'+t+'</button>';}).join('');
 return '<div class="mcq" id="'+m[0]+'" data-ans="'+m[1]+'"><div class="q">'+m[2]+'</div>'+opts+'</div>';}).join(''); }

function render(){
 var h = ''
 +'<div id="progressbar"></div>'
 +'<div class="logo">P<span>rogress Schools</span></div>'
 +'<div class="toolbtns">'
 +' <button onclick="BE.toggleModal(\'tamodal\')">TA Focus</button>'
 +' <button onclick="BE.coldCall()">Cold Call</button>'
 +' <button onclick="BE.toggleCalm()" id="calmbtn">Calm Mode</button></div>'
 +'<section class="slide bt-title active"><div class="hero">'
 +' <div class="tag">'+L.tag+'</div><h1>'+L.hero+'</h1><p class="sub">'+L.sub+'</p>'
 +' <div class="iconrow">'+icons(L.icons)+'</div>'
 +' <p class="sub">Today is a <strong>hands-on</strong> lesson \u2014 we learn by doing.</p></div></section>'
 +'<section class="slide bt-teach"><div class="tag">ARRIVAL TASK \u00b7 do now, no help needed</div>'
 +' <h2>'+L.arrival.heading+'</h2><p>Tap a card, then tap where it belongs. Have a go \u2014 wrong answers are welcome here.</p>'
 +' <div class="chipzone" id="arr-chips"></div><div class="buckets" id="arr-buckets"></div>'
 +' <div class="box tip-box"><strong>While you wait:</strong> '+L.arrival.tipWait+'</div></section>'
 +'<section class="slide bt-teach"><div class="tag">LEARNING OBJECTIVE</div>'
 +' <h2>LO: '+L.learningObjective+'</h2><div id="lolist">'+loItems(L.successCriteria)+'</div>'
 +' <div class="box sc-box"><strong>Success criteria:</strong> '+L.scText+'</div>'
 +' <div class="box aspire-box"><strong>Aspire:</strong> '+L.aspire1+'</div></section>'
 +'<section class="slide bt-teach"><div class="tag">STARTER \u00b7 talk task</div>'
 +' <h2>'+L.starter.heading+'</h2><p>'+L.starter.prompt+'</p>'
 +' <div class="box stem-box"><strong>Sentence stems:</strong><br>'+L.starter.stems+'</div>'
 +' <button class="act" onclick="BE.hint(\'starter\')">Hint</button>'
 +' <p id="hint-starter" style="display:none;margin-top:8px;">'+L.starter.hint+'</p></section>'
 +'<section class="slide bt-teach"><div class="tag">I DO \u00b7 teacher explains</div>'
 +' <h2>'+L.iDo.heading+'</h2><div class="grid">'+idoCards(L.iDo.cards)+'</div>'
 +' <div class="box misc-box"><strong>Misconception:</strong> <s>'+L.iDo.miscWrong+'</s> '+L.iDo.miscRight+'</div></section>'
 +'<section class="slide bt-wedo"><div class="tag">WE DO \u00b7 together on the board</div>'
 +' <h2>'+L.weDo.heading+'</h2><div class="chipzone" id="wedo-chips"></div>'
 +' <div class="buckets" id="wedo-buckets"></div><div id="wedofb"></div>'
 +' <button class="act secondary" onclick="BE.hint(\'wedo\')">Hint</button>'
 +' <p id="hint-wedo" style="display:none;">'+L.weDo.hint+'</p></section>'
 +'<section class="slide bt-prac"><div class="tag">HANDS-ON \u00b7 the main event</div>'
 +' <h2>'+L.practical.heading+'</h2>'
 +' <div class="box tip-box"><strong>'+L.practical.tipLabel+'</strong> '+L.practical.tip+'</div>'
 +' <div class="stations">'+stations(L.practical.stations)+'</div>'
 +' <div class="box aspire-box"><strong>Aspire:</strong> '+L.aspire2+'</div></section>'
 +'<section class="slide bt-prac"><div class="tag">'+L.evidence.tag+'</div>'
 +' <h2>Capture your evidence</h2><p>'+L.evidence.intro+'</p>'
 +' <div class="box evidence-box">'
 +'  <p><strong>My name:</strong> <input id="ev-name" style="font-size:1.1rem;padding:6px;width:220px;"></p>'
 +'  <p style="margin-top:8px;"><strong>'+L.evidence.p1Label+'</strong><br><textarea id="ev-p1" rows="2" style="width:100%;font-size:1.1rem;padding:6px;"></textarea></p>'
 +'  <p style="margin-top:8px;"><strong>'+L.evidence.p2Label+'</strong><br><textarea id="ev-p2" rows="2" style="width:100%;font-size:1.1rem;padding:6px;"></textarea></p>'
 +'  <p style="margin-top:8px;"><strong>Skills I used today (tick with your TA):</strong> '+L.evidence.skillsLine+'</p></div>'
 +' <div class="box tip-box"><strong>Feedback loop:</strong> your teacher will deep-mark <em>one</em> part of this in dark green and draw a <strong>Yellow Box</strong>. Next lesson you respond inside it in a coloured pen of your choice.</div>'
 +' <button class="act" onclick="BE.printEvidence()">\ud83d\udda8\ufe0f Print my evidence sheet</button></section>'
 +'<section class="slide bt-exit"><div class="tag">EXIT TICKET</div><h2>Show what you know</h2>'
 + mcqs(L.mcqs)
 +' <button class="act" onclick="BE.showAnswers()">Show answers</button></section>'
 +'<nav><button onclick="BE.prevSlide()">\u25c0 Back</button><button onclick="BE.nextSlide()">Next \u25b6</button>'
 +' <span id="slidecount">1 / 9</span><span class="spacer"></span>'
 +' <span id="xplabel">XP 0</span><div id="xpwrap"><div id="xpbar"></div></div></nav>'
 +'<div class="modal" id="tamodal" onclick="if(event.target===this)BE.toggleModal(\'tamodal\')"><div class="card">'
 +' <h2>TA Focus \u2014 this slide</h2><p id="tabrief"></p>'
 +' <p style="margin-top:12px;font-size:.95rem;color:#4b5563;">Gesture anchor: open palm = \u201cyour idea please\u201d; thumb-to-table = \u201ccheck with your partner first\u201d.</p>'
 +' <button class="act" onclick="BE.toggleModal(\'tamodal\')">Close</button></div></div>'
 +'<div class="modal" id="ccmodal" onclick="if(event.target===this)BE.toggleModal(\'ccmodal\')"><div class="card" style="text-align:center;">'
 +' <h2>Cold Call</h2><p id="ccname" style="font-size:2rem;font-weight:800;margin:14px 0;color:var(--pink);"></p>'
 +' <p id="cctier" style="font-size:1.1rem;"></p><button class="act" onclick="BE.coldCall()">Again</button>'
 +' <button class="act secondary" onclick="BE.toggleModal(\'ccmodal\')">Close</button></div></div>'
 +'<div id="overlay"><h1>Lesson complete! \ud83c\udf89</h1>'
 +' <p style="font-size:1.3rem;margin:12px 0;">'+L.overlay+'</p>'
 +' <button class="act" onclick="document.getElementById(\'overlay\').classList.remove(\'open\')">Close</button></div>'
 +'<canvas id="confetticanvas"></canvas><div id="printarea"></div>';
 var app = document.getElementById('app') || document.body;
 app.innerHTML = h;
 document.title = L.title;
}

function ping(freq){
 try{
  if(!audioCtx) audioCtx = new (window.AudioContext||window.webkitAudioContext)();
  if(audioCtx.state === 'suspended') audioCtx.resume();
  var o = audioCtx.createOscillator(), g = audioCtx.createGain();
  o.frequency.value = freq; o.type = 'sine';
  g.gain.setValueAtTime(.12, audioCtx.currentTime);
  g.gain.exponentialRampToValueAtTime(.001, audioCtx.currentTime + .3);
  o.connect(g); g.connect(audioCtx.destination); o.start(); o.stop(audioCtx.currentTime + .3);
 }catch(e){}
}
function slides(){ return document.querySelectorAll('.slide'); }
function showSlide(i){
 var s = slides();
 if(i < 0 || i >= s.length) return;
 if(s[current]) s[current].classList.remove('active');
 current = i;
 if(s[current]) s[current].classList.add('active');
 var sc = document.getElementById('slidecount'); if(sc) sc.textContent = (current+1)+' / '+s.length;
 var pb = document.getElementById('progressbar'); if(pb) pb.style.width = ((current+1)/s.length*100)+'%';
 var tb = document.getElementById('tabrief'); if(tb) tb.textContent = L.taBriefs[current];
 if(current === 2) animateLO();
}
function animateLO(){
 var items = document.querySelectorAll('#lolist .lo-item');
 Array.prototype.forEach.call(items, function(el, idx){
  setTimeout(function(){ el.classList.add('show'); }, 300 + idx*450);
 });
}
function addXP(n){
 xp += n;
 var l = document.getElementById('xplabel'); if(l) l.textContent = 'XP '+xp;
 var b = document.getElementById('xpbar'); if(b) b.style.width = Math.min(100,xp)+'%';
}
function shuffle(arr){
 var a = arr.slice();
 for(var i=a.length-1;i>0;i--){ var j=Math.floor(Math.random()*(i+1)); var t=a[i];a[i]=a[j];a[j]=t; }
 return a;
}
function buildSort(chipZoneId, bucketZoneId, items, buckets, onCorrect, onWrong){
 var cz = document.getElementById(chipZoneId), bz = document.getElementById(bucketZoneId);
 if(!cz || !bz) return;
 cz.innerHTML=''; bz.innerHTML='';
 var selected = null;
 shuffle(items).forEach(function(item){
  var c = document.createElement('button');
  c.className='chip'; c.textContent=item.n; c.dataset.g=item.g;
  c.addEventListener('click', function(){
   var chips = cz.querySelectorAll('.chip');
   Array.prototype.forEach.call(chips, function(x){x.classList.remove('selected');});
   c.classList.add('selected'); selected=c; ping(520);
  });
  cz.appendChild(c);
 });
 buckets.forEach(function(label, gi){
  var b = document.createElement('div');
  b.className='bucket';
  b.innerHTML = '<div>'+label+'</div><div class="mark"></div><div class="drops"></div>';
  b.addEventListener('click', function(){
   if(!selected) return;
   var mk = b.querySelector('.mark');
   if(parseInt(selected.dataset.g) === gi){
    b.classList.add('flash-good'); setTimeout(function(){b.classList.remove('flash-good');},700);
    b.querySelector('.drops').textContent += '\u2713 '+selected.textContent+'  ';
    if(mk){ mk.textContent='\u2713 correct'; setTimeout(function(){mk.textContent='';},900); }
    selected.classList.remove('selected'); selected.classList.add('done');
    selected=null; ping(880); addXP(XP_PER); if(onCorrect) onCorrect();
    if(cz.querySelectorAll('.chip:not(.done)').length === 0) confetti();
   } else {
    b.classList.add('flash-bad'); setTimeout(function(){b.classList.remove('flash-bad');},700);
    if(mk){ mk.textContent='\u2717 not here'; setTimeout(function(){mk.textContent='';},900); }
    ping(220); if(onWrong) onWrong();
   }
  });
  bz.appendChild(b);
 });
}
function hint(id){
 var el = document.getElementById('hint-'+id); if(!el) return;
 el.style.display = el.style.display==='none' ? 'block' : 'none';
}
function toggleModal(id){ var m=document.getElementById(id); if(m) m.classList.toggle('open'); }
function toggleCalm(){
 document.body.classList.toggle('calm');
 var b = document.getElementById('calmbtn');
 if(b) b.textContent = document.body.classList.contains('calm') ? 'Calm \u2713' : 'Calm Mode';
}
function coldCall(){
 var roster = [];
 try{ roster = JSON.parse(localStorage.getItem('ps_coldcall_roster')||'[]'); }catch(e){}
 if(!roster.length) roster = ['Add roster in ps_coldcall_roster'];
 var name = roster[Math.floor(Math.random()*roster.length)];
 var r = Math.ceil(Math.random()*5);
 var tier = (r<=1)?'Foundation question':(r===2)?'Middle question':'Higher question';
 var n=document.getElementById('ccname'); if(n) n.textContent=name;
 var t=document.getElementById('cctier'); if(t) t.textContent='U/1\u2192F, 2\u2192M, 3\u20135\u2192H \u00b7 rolled '+r+' \u2192 '+tier;
 var m=document.getElementById('ccmodal'); if(m && !m.classList.contains('open')) m.classList.add('open');
 ping(660);
}
function wireMCQ(){
 var qs = document.querySelectorAll('.mcq');
 Array.prototype.forEach.call(qs, function(q){
  var opts = q.querySelectorAll('.opt');
  Array.prototype.forEach.call(opts, function(opt){
   opt.addEventListener('click', function(){
    if(q.classList.contains('locked')) return;
    q.classList.add('locked'); q.dataset.chosen = opt.dataset.i;
    opt.style.borderColor='#1f2a56'; opt.style.fontWeight='700'; ping(520);
   });
  });
 });
}
function showAnswers(){
 var correct = 0;
 var qs = document.querySelectorAll('.mcq');
 Array.prototype.forEach.call(qs, function(q){
  var ans=q.dataset.ans, chosen=q.dataset.chosen;
  q.classList.add('locked');
  var opts=q.querySelectorAll('.opt');
  Array.prototype.forEach.call(opts, function(opt){
   if(opt.dataset.i===ans){ opt.classList.add('correct'); opt.textContent='\u2713 '+opt.textContent; }
   else if(opt.dataset.i===chosen){ opt.classList.add('wrong'); opt.textContent='\u2717 '+opt.textContent; }
  });
  if(chosen===ans) correct++;
 });
 addXP(correct*10);
 var ov=document.getElementById('overlay'); if(ov) ov.classList.add('open');
 confetti();
}
function printEvidence(){
 var pa = document.getElementById('printarea'); if(!pa) return;
 function val(id){ var e=document.getElementById(id); return (e&&e.value)?e.value:''; }
 var name = val('ev-name')||'________________';
 var d = new Date().toLocaleDateString('en-GB');
 pa.innerHTML='';
 function row(txt, cls){
  var el=document.createElement('div'); el.className=cls||'prow'; el.textContent=txt; pa.appendChild(el); return el;
 }
 var h=document.createElement('h1'); h.textContent=L.evidence.printTitle; pa.appendChild(h);
 row('Name: '+name+'   \u00b7   Date: '+d+'   \u00b7   '+L.evidence.lessonLine+'   \u00b7   Lesson ID: '+L.lessonId);
 row('LO: '+L.learningObjective+'   \u00b7   Skills: '+(L.evidence.curriculumSkills||[]).join(', '));
 row(L.evidence.p1Label+' '+val('ev-p1'));
 row(L.evidence.p2Label+' '+val('ev-p2'));
 row('Skills used (tick): '+L.evidence.skillsLine+'   \u00b7   Independence stage (circle): 1 joined in \u00b7 2 with help \u00b7 3 with prompts \u00b7 4 myself \u00b7 5 somewhere new');
 row('Evidence ref: '+L.evidence.ref+'   \u00b7   Programme: '+(L.evidence.programme||'\u2014')+'   \u00b7   Criterion: '+(L.evidence.criterion||'TBC \u2014 not portfolio-ready')+'   \u00b7   Verified by: ________________');
 var yb=document.createElement('div'); yb.className='ybox';
 yb.textContent='YELLOW BOX \u2014 teacher deep-marks ONE section (dark green pen). Pupil improvement/redraft goes here:';
 pa.appendChild(yb);
 row('WWW (What Went Well): ______________________________________________');
 row('EBI (Even Better If): _______________________________________________');
 row('Next Steps: ________________________________________________________');
 row('My response (coloured pen of my choice): ____________________________');
 row('Formative judgement (circle one): Emerging \u00b7 Developing \u00b7 Secure \u00b7 Exceeding   \u2192   recorded on Arbor formative tab');
 var foot=document.createElement('div'); foot.className='small';
 foot.textContent='Literacy codes (dark green, in margin): Sp spelling \u00b7 P punctuation \u00b7 Cap capital letter \u00b7 T tense \u00b7 // new paragraph \u00b7 ^ missing word. Portfolio evidence: upload to Teams/ItsLearning for IQA.';
 pa.appendChild(foot);
 window.print();
}
function confetti(){
 if(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
 if(document.body.classList && document.body.classList.contains('calm')) return;
 var cv = document.getElementById('confetticanvas'); if(!cv || !cv.getContext) return;
 var ctx = cv.getContext('2d'); if(!ctx) return;
 cv.width=window.innerWidth; cv.height=window.innerHeight;
 var bits=[]; for(var i=0;i<90;i++){ bits.push({x:Math.random()*cv.width,y:-20-Math.random()*200,v:2+Math.random()*3,r:4+Math.random()*5,c:['#d6006d','#1f2a56','#f59e0b','#16a34a'][Math.floor(Math.random()*4)]}); }
 var t=0;
 (function fall(){
  ctx.clearRect(0,0,cv.width,cv.height);
  bits.forEach(function(b){ b.y+=b.v; ctx.fillStyle=b.c; ctx.fillRect(b.x,b.y,b.r,b.r); });
  t++;
  if(t<140) requestAnimationFrame(fall); else ctx.clearRect(0,0,cv.width,cv.height);
 })();
}
document.addEventListener('keydown', function(e){
 var tag = (e.target && e.target.tagName) || '';
 if(tag==='INPUT'||tag==='TEXTAREA'||tag==='SELECT') return;
 if(e.key==='ArrowRight'||e.key===' ') showSlide(current+1);
 if(e.key==='ArrowLeft') showSlide(current-1);
});
window.BE = {
 nextSlide:function(){showSlide(current+1);}, prevSlide:function(){showSlide(current-1);},
 hint:hint, toggleModal:toggleModal, toggleCalm:toggleCalm, coldCall:coldCall,
 showAnswers:showAnswers, printEvidence:printEvidence
};
render();
buildSort('arr-chips','arr-buckets', L.arrival.items, L.arrival.buckets, null, null);
var fbGood=0, fbBad=0;
buildSort('wedo-chips','wedo-buckets', L.weDo.items, L.weDo.buckets,
 function(){ var f=document.getElementById('wedofb'); if(f) f.textContent=L.feedback.good[(fbGood++)%L.feedback.good.length]; },
 function(){ var f=document.getElementById('wedofb'); if(f) f.textContent=L.feedback.bad[(fbBad++)%L.feedback.bad.length]; });
wireMCQ();
var tb=document.getElementById('tabrief'); if(tb) tb.textContent=L.taBriefs[0];
})();
