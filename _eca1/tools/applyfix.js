#!/usr/bin/env node
// ECA-1 PART A fixer. Applies an edit table of exact-string replacements.
// Every edit declares its expected occurrence count; a mismatch blocks that edit
// (reported, not applied). --check reports counts without writing.
// Usage: applyfix.js table.json [--check]
const fs = require('fs');
const table = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const check = process.argv.includes('--check');
let applied = 0, blocked = 0;
const byFile = {};
for (const e of table) (byFile[e.file] = byFile[e.file] || []).push(e);
for (const [file, edits] of Object.entries(byFile)) {
  let s = fs.readFileSync(file, 'utf8');
  for (const e of edits) {
    const n = s.split(e.old).length - 1;
    if (n !== e.n) { console.log(`BLOCK ${file} :: expected ${e.n} got ${n} :: ${e.old.slice(0, 70)}`); blocked++; continue; }
    if (!check) s = s.split(e.old).join(e.new);
    applied++;
  }
  if (!check) fs.writeFileSync(file, s);
}
console.log(`${check ? 'check' : 'apply'}: ${applied} edits ok, ${blocked} blocked, ${Object.keys(byFile).length} files`);
process.exit(blocked ? 1 : 0);
