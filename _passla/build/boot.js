// jsdom boot harness: load a lesson HTML, run its inline scripts, report any throw.
// Usage: NODE_PATH=<scratch>/node_modules node boot.js <file.html>
const fs = require('fs');
const { JSDOM, VirtualConsole } = require('jsdom');
const file = process.argv[2];
const htmlRaw = fs.readFileSync(file, 'utf8');
// strip the external hud.js (not needed for boot; avoids a resource fetch)
const html = htmlRaw.replace(/<script[^>]*src="\/hud\.js"[^>]*><\/script>/,'');
const errors = [];
const vc = new VirtualConsole();
vc.on('jsdomError', e => errors.push('jsdomError: ' + (e && e.message)));
// shim AudioContext so any accidental call doesn't hard-fail (real page guards with try/catch)
const dom = new JSDOM(html, {
  runScripts: 'dangerously',
  url: 'https://example.org/lesson',   // localStorage needs an origin
  pretendToBeVisual: true,
  virtualConsole: vc,
  beforeParse(window) {
    window.AudioContext = window.webkitAudioContext = function(){
      return { state:'running', resume(){}, currentTime:0,
        createOscillator(){return {frequency:{value:0,setValueAtTime(){}},type:'',connect(){},start(){},stop(){}}},
        createGain(){return {gain:{value:0,setValueAtTime(){},linearRampToValueAtTime(){},exponentialRampToValueAtTime(){}},connect(){}}},
        destination:{} };
    };
    window.print = function(){};
    window.matchMedia = window.matchMedia || function(){return {matches:false,addListener(){},removeListener(){},addEventListener(){},removeEventListener(){}}};
  }
});
// let timeouts (DOMContentLoaded work, _atOnSlideChange at 150ms) fire
setTimeout(() => {
  // exercise the risky content-driven functions once, to catch content/JS mismatches
  const w = dom.window;
  try {
    if (typeof w.showColdCall === 'function') { /* needs class list; skip actual roll */ }
    ['presReset','resetMatch','revealMatch'].forEach(fn => { try { if (typeof w[fn]==='function') w[fn](); } catch(e){ errors.push(fn+': '+e.message); } });
  } catch (e) { errors.push('exercise: ' + e.message); }
  if (errors.length) { console.error(errors.join('\n')); process.exit(1); }
  console.log('BOOT-OK');
  process.exit(0);
}, 400);
