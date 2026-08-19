#!/usr/bin/env node
// ECA-1 §1.4 extractor — PROSE / CODE hashes per file (gate: CODE delta = 0 on Track B),
// plus a QUESTIONS dump mode for audit reading.
// Usage: extract.js hashes > file.tsv   |   extract.js questions <file.html>
const fs = require('fs'), crypto = require('crypto');
const { execSync } = require('child_process');
const { splitCode, visibleText } = require('./lib');
const sha = s => crypto.createHash('sha256').update(s).digest('hex').slice(0, 16);

if (process.argv[2] === 'questions') {
  const s = fs.readFileSync(process.argv[3], 'utf8');
  const { prose } = splitCode(s);
  const text = visibleText(prose);
  // sentences ending in ? from visible prose
  const qs = text.match(/[^.!?]{6,300}\?/g) || [];
  qs.forEach((q, i) => console.log(`${i + 1}\t${q.trim()}`));
  // plus question strings living in JS pools (_ccQuestions etc.) — CODE stream, listed separately
  const { code } = splitCode(s);
  const jsqs = code.match(/"[^"]{6,200}\?"/g) || [];
  jsqs.forEach((q, i) => console.log(`js${i + 1}\t${q.slice(1, -1)}`));
  process.exit(0);
}

const files = process.argv.length > 3 ? process.argv.slice(3) :
  execSync("git ls-files '*.html'", { encoding: 'utf8' }).trim().split('\n')
    .filter(f => /^(BUILD_ASDAN|GROW_ASDAN|LAUNCH_ASDAN|Art_Teesside|Humanities_Teesside)\//.test(f)
      || /^(Build|Grow|Launch)\/Slideshows\/[A-Z]+_(DT|HUM|ART)_/.test(f)
      || /^Science_Teesside\/(Build|Grow|Launch)\/v3_40min\//.test(f)).sort();
for (const f of files) {
  const { code, prose } = splitCode(fs.readFileSync(f, 'utf8'));
  console.log(`${f}\tCODE:${sha(code)}\tPROSE:${sha(visibleText(prose))}`);
}
