#!/usr/bin/env node
// node --check every inline <script> in the given files (or the whole universe).
const fs = require('fs'), os = require('os'), path = require('path');
const { execSync, execFileSync } = require('child_process');
const { scripts } = require('./lib');

let files = process.argv.slice(2);
if (!files.length) {
  files = execSync("git ls-files '*.html'", { encoding: 'utf8' }).trim().split('\n')
    .filter(f => /^(BUILD_ASDAN|GROW_ASDAN|LAUNCH_ASDAN|Art_Teesside|Humanities_Teesside)\//.test(f)
      || /^(Build|Grow|Launch)\/Slideshows\/[A-Z]+_(DT|HUM)_/.test(f)
      || /^Science_Teesside\/(Build|Grow|Launch)\/v3_40min\//.test(f));
}
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'jscheck-'));
let bad = 0, checked = 0;
for (const f of files) {
  const blocks = scripts(fs.readFileSync(f, 'utf8'));
  blocks.forEach((b, i) => {
    if (!b.trim()) return;
    if (/^\s*(application\/json|text\/template)/.test(b)) return;
    const t = path.join(tmp, 'b.js');
    fs.writeFileSync(t, b);
    try { execFileSync('node', ['--check', t], { stdio: 'pipe' }); checked++; }
    catch (e) { bad++; console.log(`FAIL ${f} [script ${i}]: ${e.stderr.toString().split('\n')[1] || ''}`); }
  });
}
console.log(`jscheck: ${checked} blocks OK, ${bad} FAIL, ${files.length} files`);
process.exit(bad ? 1 : 0);
