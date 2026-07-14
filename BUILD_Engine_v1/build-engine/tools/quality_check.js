#!/usr/bin/env node
/* Build Engine Quality Checker
   Scans lessons/*.json + manifest.js. Output per lesson: PASS / WARNING / BLOCK.
   NOTE: version rules CORRECTED from the source document (which stated them inverted):
   - Version B lessons must NOT reference Living Independently
   - Version A lessons must NOT reference the double FoodWise slot
   Run: node tools/quality_check.js   (from build-engine/) */
'use strict';
const fs = require('fs');
const path = require('path');

const ROOT = path.join(__dirname, '..');
const LESSON_DIR = path.join(ROOT, 'lessons');
const HYGIENE_ORDER = ['Hair back','Apron on','Wash hands','Wipe surface'];
const VALID_SKILLS = new Set(['COM-01','COM-02','COM-03','COM-04','COM-05','COM-06',
 'LIFE-01','LIFE-02','LIFE-03','LIFE-04','LIFE-05',
 'FOOD-01','FOOD-02','FOOD-03','FOOD-04','FOOD-05',
 'WORK-01','WORK-02','WORK-03','WORK-04','WORK-05',
 'COMM-01','COMM-02','COMM-03','DIG-01','DIG-02']);

/* pupil-facing text fields to scan for premature credit-achievement claims */
function pupilText(L){
 return [L.scText, L.overlay, L.aspire1, L.aspire2,
  L.starter && L.starter.prompt, L.evidence && L.evidence.intro].filter(Boolean).join(' ');
}
function allText(L){ return JSON.stringify(L); }

function checkLesson(L, stem){
 const warns = [], blocks = [];

 /* ---- VERSION (corrected rules) ---- */
 const txt = allText(L);
 if (L.version === 'B' && /Living Independently/i.test(txt) && L.slot !== 'Careers')
  blocks.push('VERSION: Version B lesson references Living Independently');
 if (L.version === 'A' && /(double.{0,12}FoodWise|Practical Kitchen)/i.test(txt))
  blocks.push('VERSION: Version A lesson references the double-FoodWise slot');
 if (!['A','B','both'].includes(L.version))
  blocks.push('VERSION: version field must be A, B or both');

 /* ---- ACCREDITATION ---- */
 if (L.evidence.criterion == null || String(L.evidence.criterion).includes('___')) {
  warns.push('ACCREDITATION: criterion missing/placeholder -> NOT portfolio-ready (usable pedagogically)');
  if (L.evidence.portfolioReady === true)
   blocks.push('ACCREDITATION: portfolioReady=true but criterion incomplete');
 }
 if (/(credit (achieved|earned|awarded)|you have (your|a) credit|certificate is yours)/i.test(pupilText(L)))
  blocks.push('ACCREDITATION: pupil-facing text claims a credit before verified status');

 /* ---- ACCESSIBILITY (engine provides symbols/reduced-motion/keyboard; check content) ---- */
 (L.iDo.cards||[]).forEach(function(c,i){
  if(!c[2] || !c[3]) warns.push('ACCESSIBILITY: I-Do card '+i+' missing title/body text');
 });
 [L.scText, L.starter.prompt].forEach(function(t,i){
  if(t && t.length > 420) warns.push('ACCESSIBILITY: dense text in '+(i===0?'success criteria':'starter')+' ('+t.length+' chars)');
 });
 if (!L.taBriefs || L.taBriefs.length !== 9)
  blocks.push('ACCESSIBILITY/STRUCTURE: expected 9 TA briefs, found '+((L.taBriefs||[]).length));

 /* ---- SAFETY ---- */
 const s = L.safety || {};
 if (s.foodLesson && !s.allergyStatement)
  blocks.push('SAFETY: food lesson without an allergy statement');
 if (s.hygieneOrder){
  if (JSON.stringify(s.hygieneOrder) !== JSON.stringify(HYGIENE_ORDER))
   blocks.push('SAFETY: hygiene order inconsistent with canonical Hair->Apron->Hands->Surface');
 }
 if (s.offSite && !s.consentNote)
  blocks.push('SAFETY: off-site activity without approval/consent reminder');

 /* ---- EVIDENCE ---- */
 ['tag','p1Label','p2Label','skillsLine','printTitle','ref'].forEach(function(k){
  if(!L.evidence[k]) blocks.push('EVIDENCE: missing evidence.'+k);
 });
 (L.evidence.curriculumSkills||[]).forEach(function(id){
  if(!VALID_SKILLS.has(id)) blocks.push('EVIDENCE: unknown curriculum skill id '+id);
 });
 if(!(L.evidence.curriculumSkills||[]).length)
  warns.push('EVIDENCE: no curriculum skills mapped');

 /* ---- SORT DATA ---- */
 [['arrival',L.arrival],['weDo',L.weDo]].forEach(function(p){
  (p[1].items||[]).forEach(function(it){
   if(it.g < 0 || it.g >= p[1].buckets.length)
    blocks.push('DATA: '+p[0]+' item "'+it.n+'" maps to non-existent bucket '+it.g);
  });
 });
 (L.mcqs||[]).forEach(function(m){
  if(parseInt(m[1]) >= m[3].length) blocks.push('DATA: MCQ '+m[0]+' answer index out of range');
 });

 return {stem, warns, blocks};
}

/* ---- run ---- */
const files = fs.readdirSync(LESSON_DIR).filter(f=>f.endsWith('.json')).sort();
let anyBlock = false, anyWarn = false;
console.log('Build Engine Quality Checker \u00b7 '+files.length+' lessons\n'+'='.repeat(64));
files.forEach(function(f){
 const L = JSON.parse(fs.readFileSync(path.join(LESSON_DIR,f),'utf8'));
 const r = checkLesson(L, f.replace('.json',''));
 const status = r.blocks.length ? 'BLOCK PUBLICATION' : (r.warns.length ? 'PASS with WARNINGS' : 'PASS');
 if(r.blocks.length) anyBlock = true;
 if(r.warns.length) anyWarn = true;
 console.log('\n' + r.stem + '  [' + L.lessonId + ', v' + L.version + ']  ->  ' + status);
 r.blocks.forEach(b=>console.log('  BLOCK   ' + b));
 r.warns.forEach(w=>console.log('  WARN    ' + w));
});
console.log('\n'+'='.repeat(64));
console.log(anyBlock ? 'RESULT: BLOCKED lessons present \u2014 do not publish those files.'
 : anyWarn ? 'RESULT: all lessons publishable; warnings are honest gaps (e.g. ASDAN criteria await the student books).'
 : 'RESULT: all clean.');
process.exit(anyBlock ? 1 : 0);
