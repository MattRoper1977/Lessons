#!/usr/bin/env node
// ECA-1 §1.1 inventory — measured at BASE (origin/main 7277859).
// Universe: ASDAN trees (BUILD/GROW/LAUNCH_ASDAN), D&T 6 (Build/Slideshows/BUILD_DT_*),
// Art_Teesside (all html), Humanities 24 ({Build,Grow,Launch}/Slideshows/*_HUM_*),
// Humanities_Teesside docs, Science v3_40min 35 (PART B conditional — DEFERRED, SCA-1 absent).
// Estate_v3 trees are TEST COPIES — excluded by rule (§0).
const fs = require('fs'), path = require('path'), crypto = require('crypto');
const { execSync } = require('child_process');

const root = process.cwd();
const tracked = execSync("git ls-files '*.html'", { encoding: 'utf8' }).trim().split('\n');

function inUniverse(f) {
  if (/^(BUILD_ASDAN|GROW_ASDAN|LAUNCH_ASDAN|Art_Teesside|Humanities_Teesside)\//.test(f)) return true;
  if (/^(Build|Grow|Launch)\/Slideshows\/[A-Z]+_(DT|HUM)_/.test(f)) return true;
  if (/^Science_Teesside\/(Build|Grow|Launch)\/v3_40min\//.test(f)) return true;
  return false;
}

function count(hay, re) { const m = hay.match(re); return m ? m.length : 0; }

const rows = [['path','bytes','sha256','chassis','scripts','print_sections','print_boxes','wit_panel','loop_mark','closure_line','ta_brief','cc','lundy_boxes','sow_strip','award_strip','guide_tagged']];
for (const f of tracked.filter(inUniverse).sort()) {
  const buf = fs.readFileSync(f);
  const s = buf.toString('utf8');
  const sha = crypto.createHash('sha256').update(buf).digest('hex').slice(0, 12);
  let chassis;
  if (/\/v3_40min\//.test(f)) chassis = /SCI_/.test(f) ? 'sci-v3' : 'sci-v3-doc';
  else if (s.includes('mbmTAopen')) chassis = 'hum-v4';
  else if (s.includes('showTABrief')) chassis = /_DT_/.test(f) ? 'v5-dt' : (/Art_Teesside/.test(f) ? 'v5-art' : 'v5-asdan');
  else chassis = 'doc';
  rows.push([f, buf.length, sha, chassis,
    count(s, /<script/g),
    count(s, /class="print-section/g),
    count(s, /class="print-box/g),
    count(s, /wit-panel/g) ? 1 : 0,
    s.includes('ll-g:loop-mark') ? 1 : 0,
    s.includes('What I said, and what it changed') ? 1 : 0,
    s.includes('_taBriefs') ? 'v5' : (s.includes('mbmTA') ? 'mbm' : ''),
    s.includes('_ccQuestions') || s.includes('mbmCC') ? 1 : 0,
    count(s, /class="lundy-box/g),
    count(s, /class="sow-strip|<span class="sow-strip/g),
    count(s, /award-strip/g) > 0 ? 1 : 0,
    s.includes('data-mbm-guide') ? 1 : 0]);
}
fs.writeFileSync('_eca1/tables/inventory.csv', rows.map(r => r.join(',')).join('\n') + '\n');
const byChassis = {};
for (const r of rows.slice(1)) byChassis[r[3]] = (byChassis[r[3]] || 0) + 1;
console.log('rows:', rows.length - 1, JSON.stringify(byChassis));
