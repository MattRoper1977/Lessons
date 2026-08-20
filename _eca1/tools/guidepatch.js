#!/usr/bin/env node
// ECA-1 PART B — visibility patch. Extends PH-3's estate toggle (data-mbm-guide,
// html.mbm-guide-on, "ⓘ Guidance" button, key G, localStorage mbm_guide_v1).
// Roles: staff | route | lundy. Hidden means CSS-hidden, never removed.
// Idempotent (re-run = no change). Reversible: guidestrip.js restores BASE bytes.
// Usage: guidepatch.js [--dry] file...
const fs = require('fs');

const STYLE = '<style id="mbm-guide-css">html:not(.mbm-guide-on) [data-mbm-guide],html:not(.mbm-guide-on) .asvl-purpose,html:not(.mbm-guide-on) .asvl-route{display:none!important}.mbm-guide-btn[aria-pressed="true"]{box-shadow:inset 0 0 0 2px currentColor}</style>';
const BUTTON = '<button class="mbm-guide-btn" aria-pressed="false" onclick="mbmGuideToggle()">ⓘ Guidance</button>';
const SCRIPT = `<!--mbm-guide:v1--><script id="mbm-guide-js">
(function(){
  var KEY='mbm_guide_v1';
  function stored(){try{return localStorage.getItem(KEY)==='1'}catch(e){return false}}
  function store(on){try{localStorage.setItem(KEY,on?'1':'0')}catch(e){}}
  function apply(on){
    document.documentElement.classList.toggle('mbm-guide-on',on);
    var b=document.querySelector('.mbm-guide-btn');
    if(b){b.setAttribute('aria-pressed',on?'true':'false');b.textContent=on?'ⓘ Guidance ✓':'ⓘ Guidance';}
    var live=document.getElementById('vu-live-region');
    if(live)live.textContent=on?'Guidance shown':'Guidance hidden';
  }
  window.mbmGuideToggle=function(){var on=!document.documentElement.classList.contains('mbm-guide-on');store(on);apply(on);};
  document.addEventListener('keydown',function(e){
    if(e.key!=='g'&&e.key!=='G')return;
    var t=e.target;
    if(t&&(t.tagName==='INPUT'||t.tagName==='TEXTAREA'||t.isContentEditable))return;
    if(document.querySelector('.v4-modal-overlay.visible,.lesson-complete-overlay.visible,.midpoint-overlay.visible,.mbm-modal.open,.overlay.visible,.overlay.open'))return;
    window.mbmGuideToggle();
  });
  apply(stored());
})();
<\/script>`.replace('<\\/script>', '<' + '/script>');

const STAFF_LABELS = {
  'v5-art': ['How it works:', 'Instructions:', 'Step 1:', 'Step 2:', 'Why:'],
  'hum-v4': ['Instructions:', 'How to play:', 'Why:'],
};
const ROUTE_LABELS = ['🧭 Coming next:', '🧭 And that&rsquo;s the unit:', "🧭 And that's the unit:"];

function chassisOf(f, s) {
  if (/\/v3_40min\/SCI_/.test(f)) return 'sci-v3';
  if (s.includes('mbmTAopen')) return 'hum-v4';
  if (s.includes('showTABrief')) return /_DT_/.test(f) ? 'v5-dt' : (/Art_Teesside/.test(f) ? 'v5-art' : 'v5-asdan');
  return 'doc';
}

// Masked ranges: script/style blocks + balanced print subtrees (#print-area and every
// class="...print-section..." div).
function maskedRanges(s) {
  const ranges = [];
  const re = /<(script|style)\b[^>]*>[\s\S]*?<\/\1>/gi;
  let m;
  while ((m = re.exec(s)) !== null) ranges.push([m.index, m.index + m[0].length]);
  const dre = /<div\b[^>]*(?:id="print-area"|class="[^"]*print-section[^"]*")[^>]*>/g;
  while ((m = dre.exec(s)) !== null) ranges.push([m.index, balancedEnd(s, m.index)]);
  return ranges;
}
function balancedEnd(s, start) {
  const tag = /<\/?div\b/g;
  tag.lastIndex = start + 1;
  let depth = 1, m;
  while ((m = tag.exec(s)) !== null) {
    depth += m[0][1] === '/' ? -1 : 1;
    if (depth === 0) return s.indexOf('>', m.index) + 1;
  }
  return s.length;
}
const inMask = (ranges, i) => ranges.some(([a, b]) => i >= a && i < b);

// Is offset i on the deck's dedicated Lundy Loop slide? (nearest preceding data-title)
function onLundySlide(s, i) {
  const t = (s.slice(0, i).match(/data-title="([^"]*)"(?![\s\S]*data-title=)/) || [])[1] || '';
  return /Lundy/i.test(t);
}

function addAttr(openTag, role) {
  if (openTag.includes('data-mbm-guide')) return openTag;
  return openTag.replace(/^(<\w+)/, `$1 data-mbm-guide="${role}"`);
}

function patch(f, dry) {
  const orig = fs.readFileSync(f, 'utf8');
  let s = orig;
  const chassis = chassisOf(f, s);
  if (chassis === 'doc') return { f, chassis, skip: true };
  const stats = { f, chassis, staff: 0, route: 0, lundy: 0, wraps: 0, injected: false, ambers: [] };

  if (chassis === 'sci-v3') {
    // lundy: .lundy-mini (GROW) / .lundy (BUILD, LAUNCH) blocks on every slide EXCEPT the
    // exit slide (data-type="exit") — those stay visible (the Lundy close lives there).
    const masks = maskedRanges(s);
    const em = /<section class="slide[^>]*data-type="exit"/.exec(s);
    const exitAt = em ? em.index : Infinity;
    const acts = [];
    const re = /<div class="(?:lundy-mini|lundy)">/g;
    let m;
    while ((m = re.exec(s)) !== null) {
      if (inMask(masks, m.index)) continue;
      if (m.index > exitAt) continue; // on/after the exit slide: keep visible
      acts.push([m.index, m[0]]);
    }
    for (const [i, tag] of acts.reverse()) {
      const nt = tag.replace('<div ', '<div data-mbm-guide="lundy" ');
      s = s.slice(0, i) + nt + s.slice(i + tag.length); stats.lundy++;
    }
    // staff: teacher-note .note divs (voice-keyed, never class-wide — pupil access notes stay)
    const staffNoteRe = /<div class="note">(?=(?:\s*)(?:Arrival retrieves|<b>Fade it:<\/b>|<b>Fade:<\/b>))/g;
    const masks2 = maskedRanges(s);
    const acts2 = [];
    while ((m = staffNoteRe.exec(s)) !== null) { if (!inMask(masks2, m.index)) acts2.push(m.index); }
    for (const i of acts2.reverse()) {
      s = s.slice(0, i) + '<div class="note" data-mbm-guide="staff">' + s.slice(i + '<div class="note">'.length);
      stats.staff++;
    }
    // staff wrap: the "TA fade route:" tail inside the WORD HELP footer
    const fadeRe = /<b>TA fade route:<\/b>[^<]*/;
    const fm = fadeRe.exec(s);
    if (fm && !inMask(maskedRanges(s), fm.index)
        && !s.slice(Math.max(0, fm.index - 40), fm.index).includes('data-mbm-guide')) {
      s = s.slice(0, fm.index) + '<span data-mbm-guide="staff">' + fm[0] + '</span>' + s.slice(fm.index + fm[0].length);
      stats.wraps++;
    }
    // staff: the teacher's spoken influence-opener script line (GROW)
    s = tagAll(s, /<div class="teacher-say">/g, null, stats, 'staff', 0,
      t => t.replace('<div ', '<div data-mbm-guide="staff" '));
    // route: source-note provenance + the "Weeks 1 and 2 were baseline" entry lines (GROW)
    s = tagAll(s, /<p class="source-note">/g, null, stats, 'route', 0,
      t => t.replace('<p ', '<p data-mbm-guide="route" '));
    s = tagAll(s, /<div class="retr-declare">/g, null, stats, 'route', 0,
      t => t.replace('<div ', '<div data-mbm-guide="route" '));
  } else {
    // 1. Lundy boxes on v5-asdan / v5-dt / v5-art / hum-v4: NOT TAGGED.
    //    Row B-2 (PROP-1, ruled 2026-08-20). On these four chassis all four
    //    SPACE/VOICE/AUDIENCE/INFLUENCE boxes sit on ONE dedicated Lundy Loop slide, so
    //    hiding them by default left that slide rendering as a heading and nothing else
    //    on 140 of 175 decks — a quiet slide in front of a class, not decluttered guidance.
    //    The science chassis is different and is left alone: its .lundy-mini strips are
    //    per-slide clutter beside other content, and the sci-v3 branch above still tags them.
    stats.ambers.push('lundy-box tagging skipped on this chassis (B-2)');
  }

  // 2. Chassis-specific staff/route tagging (v5-art and hum-v4 get the full set;
  //    v5-asdan/v5-dt keep PH-3's staff set — only DT route labels added here).
  if (chassis === 'v5-art' || chassis === 'hum-v4') {
    // task-box Steps: lines
    s = tagAll(s, /<p><strong>Steps:<\/strong>/g, i => `<p data-mbm-guide="staff"><strong>Steps:</strong>`, stats, 'staff', 17);
    // li-box guidance labels
    const labels = STAFF_LABELS[chassis];
    const masks2 = maskedRanges(s);
    const boxes = [];
    const lre = /<div\b[^>]*class="li-box[^"]*"[^>]*>/g;
    let m;
    while ((m = lre.exec(s)) !== null) {
      if (inMask(masks2, m.index)) continue;
      const end = balancedEnd(s, m.index);
      boxes.push([m.index, s.indexOf('>', m.index) + 1, end]);
    }
    for (const [start, innerStart, end] of boxes.reverse()) {
      const openTag = s.slice(start, innerStart);
      if (openTag.includes('data-mbm-guide')) continue;
      const inner = s.slice(innerStart, end);
      const label = (inner.match(/^\s*<(?:strong|b)>([^<]{0,45})/) || [])[1];
      if (!label || !labels.some(L => label.startsWith(L))) continue;
      // B-2: the "Why:" li-box on the Lundy Loop slide is that slide's rationale, not
      // staff guidance. Tagging it hid the only remaining text once the boxes were hidden.
      if (label.startsWith('Why:') && onLundySlide(s, start)) continue;
      const counter = inner.match(/<span[^>]*>[^<]*<span[^>]*id="(?:pres-num|match-score)"[^>]*>/)
        || inner.match(/<span[^>]*id="(?:pres-num|match-score)"[^>]*>/);
      if (counter) {
        // counter-WRAP: wrap label→text before the counter span; counter stays outside.
        const cut = inner.indexOf(counter[0]);
        const head = inner.slice(0, cut);
        if (head.includes('<span')) { stats.ambers.push(`wrap blocked (nested span) @${start}`); continue; }
        s = s.slice(0, innerStart) + `<span data-mbm-guide="staff">` + head + `</span>` + inner.slice(cut) + s.slice(end);
        stats.wraps++;
      } else {
        s = s.slice(0, start) + addAttr(openTag, 'staff') + s.slice(innerStart);
        stats.staff++;
      }
    }
    // route: sow-strip (Title provenance chip)
    s = tagAll(s, /<(div|span)\b([^>]*)class="sow-strip"([^>]*)>/g, null, stats, 'route', 0, (tag) => addAttr(tag, 'route'));
  }
  if (chassis === 'v5-dt') {
    // route: Coming next / And that's the unit li-boxes on Exit
    const masks3 = maskedRanges(s);
    const lre = /<div\b[^>]*class="li-box[^"]*"[^>]*>/g;
    const acts = [];
    let m;
    while ((m = lre.exec(s)) !== null) {
      if (inMask(masks3, m.index)) continue;
      const innerStart = s.indexOf('>', m.index) + 1;
      const inner = s.slice(innerStart, balancedEnd(s, m.index));
      const label = (inner.match(/^\s*<(?:strong|b)>([^<]{0,60})/) || [])[1] || '';
      if (ROUTE_LABELS.some(L => label.startsWith(L))) acts.push([m.index, s.slice(m.index, innerStart)]);
    }
    for (const [i, tag] of acts.reverse()) {
      const nt = addAttr(tag, 'route');
      if (nt !== tag) { s = s.slice(0, i) + nt + s.slice(i + tag.length); stats.route++; }
    }
  }

  // 3. Injections — only where the toggle is not already installed (v5-art, hum-v4, sci-v3).
  if (!s.includes('id="mbm-guide-css"')) {
    if (!s.includes('</head>')) { stats.ambers.push('no </head>'); }
    else {
      s = s.replace('</head>', STYLE + '</head>');
      const cre = /(<(?:div|nav) class="controls">[\s\S]*?<\/(?:div|nav)>)/;
      const cm = s.match(cre);
      if (!cm) stats.ambers.push('no .controls');
      else {
        let controls = cm[1];
        const anchor = controls.match(/<button[^>]*onclick="(?:showTABrief|mbmTAopen|openTA)\(\)"[^>]*>[^<]*<\/button>/);
        controls = anchor
          ? controls.replace(anchor[0], anchor[0] + BUTTON)
          : controls.replace(/<\/(div|nav)>$/, BUTTON + '</$1>');
        s = s.replace(cm[1], controls);
      }
      const tail = s.lastIndexOf('</body>');
      if (tail === -1) stats.ambers.push('no </body>');
      else s = s.slice(0, tail) + SCRIPT + '\n' + s.slice(tail);
      stats.injected = true;
    }
  }

  if (!dry && s !== orig) fs.writeFileSync(f, s);
  stats.changed = s !== orig;
  return stats;
}

function tagAll(s, re, _mk, stats, role, _n, fn) {
  const masks = maskedRanges(s);
  const acts = [];
  let m;
  while ((m = re.exec(s)) !== null) {
    if (inMask(masks, m.index)) continue;
    if (m[0].includes('data-mbm-guide')) continue;
    acts.push([m.index, m[0]]);
  }
  for (const [i, old] of acts.reverse()) {
    const nt = fn ? fn(old) : old.replace(/^(<\w+)/, `$1 data-mbm-guide="${role}"`);
    if (nt !== old) { s = s.slice(0, i) + nt + s.slice(i + old.length); stats[role === 'route' ? 'route' : 'staff']++; }
  }
  return s;
}

const dry = process.argv.includes('--dry');
const files = process.argv.slice(2).filter(a => a !== '--dry');
for (const f of files) {
  const r = patch(f, dry);
  console.log(JSON.stringify(r));
}
