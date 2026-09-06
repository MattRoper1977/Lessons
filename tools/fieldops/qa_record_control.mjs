#!/usr/bin/env node
/* R0.1 limb (b) for the qa-record form added to tools/stale_evidence_sweep.mjs.
 *
 * WHY THIS FILE EXISTS. The widening closed a red: twenty QA rows in
 * Matt-s-Apps- that the sweep's line-oriented grammar could not parse held it at
 * exit 2. A widening that closes a red is exactly the change that must be able
 * to go red itself — otherwise "0 stale" means "the form stopped firing", which
 * is the failure version 2 of the sweep shipped and this estate has now been
 * bitten by twice.
 *
 * So this plants a QA record naming a file that is NOT there and requires the
 * sweep to call it STALE, and a second naming a file that IS there and requires
 * SUBJECT EXISTS. Break the form and both halves fail loudly.
 *
 * NOTE ON "RED". The sweep exits 0 on a dry run even when it finds stale
 * claims, by design — "removing real evidence is worse than keeping stale
 * evidence, so the default is to report". The red signal for a stale subject is
 * therefore the VERDICT and the stale COUNT, not the process exit code, and
 * that is what this control asserts. */
import { execFileSync } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const SWEEP = path.resolve(HERE, '..', 'stale_evidence_sweep.mjs');
let fails = 0;
const check = (name, ok, detail = '') => {
  console.log(`  ${ok ? 'PASS' : 'FAIL'}  ${name}${detail ? ' — ' + detail : ''}`);
  if (!ok) fails++;
};

function fixture(records, extraFiles = {}) {
  const t = fs.mkdtempSync(path.join(os.tmpdir(), 'qarec-'));
  fs.mkdirSync(path.join(t, 'Proj', 'qa'), { recursive: true });
  fs.writeFileSync(path.join(t, 'Proj', 'qa', 'PLANTED_QA_RESULTS.json'),
                   JSON.stringify(records, null, 2));
  for (const [name, body] of Object.entries(extraFiles))
    fs.writeFileSync(path.join(t, 'Proj', name), body);
  execFileSync('git', ['-C', t, 'init', '-q']);
  execFileSync('git', ['-C', t, 'add', '-A']);
  execFileSync('git', ['-C', t, '-c', 'user.email=c@x', '-c', 'user.name=c',
                       'commit', '-qm', 'planted control fixture']);
  return t;
}

function sweep(root) {
  try {
    return execFileSync('node', [SWEEP], { encoding: 'utf8', maxBuffer: 64 * 1024 * 1024, env: { ...process.env, MBM_APPS_REPO: root } });
  } catch (e) { return (e.stdout || '') + (e.stderr || ''); }
}

console.log('\n§A3 qa-record — the widened form must judge, not rubber-stamp\n');

/* 1. the planted stale subject */
const t1 = fixture(
  [{ file: 'present.html', kind: 'control', checks: { boot: 'PASS' }, ok: true },
   { file: 'deleted.html', kind: 'control', checks: { boot: 'PASS' }, ok: true }],
  { 'present.html': '<!doctype html><title>present</title>\n' });
const out1 = sweep(t1);
const row = (s, subj) => (s.split('\n').find(l => l.includes('qa-record') && l.includes(subj)) || '').trim();
check('a QA record naming an absent file is STALE',
      /STALE/.test(row(out1, 'deleted.html')), row(out1, 'deleted.html') || 'no row emitted');
check('a QA record naming a present file is SUBJECT EXISTS',
      /SUBJECT EXISTS/.test(row(out1, 'present.html')), row(out1, 'present.html') || 'no row emitted');
const m = out1.match(/FORWARD\s+(\d+) stale claim/);
check('the planted row moves the stale count off zero', m && Number(m[1]) >= 1,
      m ? `${m[1]} stale claim(s)` : 'no FORWARD line');
fs.rmSync(t1, { recursive: true, force: true });

/* 2. the form must not swallow: JSON that names no subject still reaches the
      text grammar, so NO FORM MATCHED can still fire. */
const t2 = fixture({ note: 'no record names a file', status: 'PASS' });
const out2 = sweep(t2);
check('JSON naming no subject still reaches the text forms (no silent swallow)',
      /NO FORM MATCHED|no form|NO CLAIM FOUND/i.test(out2),
      'the fallback still reports rather than passing in silence');
fs.rmSync(t2, { recursive: true, force: true });

console.log(`\n[QA-RECORD CONTROL] ${fails === 0 ? 'PASS' : 'FAIL'} — ${fails} check(s) failed`);
process.exit(fails === 0 ? 0 : 1);
