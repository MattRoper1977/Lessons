// Red-prove tools/sx3/check_dialog_openers.mjs refuses a scope it cannot print.
//
// The fault this guards against is specific and it happened: an earlier version
// read a hard-coded /tmp path and ignored its argument, so it reported a clean
// result for 75 decks that were not the ones under measurement. A harness that
// silently measures the wrong thing is worse than one that fails.
//
//   node tools/sx3/test_check_dialog_openers.mjs
import { execFileSync } from 'child_process';
import { mkdtempSync, writeFileSync, mkdirSync } from 'fs';
import { tmpdir } from 'os';
import { join } from 'path';

const HARNESS = new URL('./check_dialog_openers.mjs', import.meta.url).pathname;
let failures = 0;

function run(args) {
  try {
    const stdout = execFileSync('node', [HARNESS, ...args], { encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] });
    return { code: 0, stdout, stderr: '' };
  } catch (e) {
    return { code: e.status, stdout: e.stdout || '', stderr: e.stderr || '' };
  }
}

function check(name, condition, detail) {
  if (condition) { console.log(`PASS  ${name}`); }
  else { console.log(`FAIL  ${name}${detail ? ' — ' + detail : ''}`); failures++; }
}

// 1. No argument at all must refuse. This is the fault, directly.
const none = run([]);
check('refuses with no directory argument', none.code === 2 && /directory of .html decks is required/.test(none.stderr),
      `code=${none.code} stderr=${none.stderr.slice(0, 80)}`);

// 2. A path that does not exist must refuse, naming the resolved path, and must
//    NOT quietly fall back to some other directory.
const missing = run([join(tmpdir(), 'sx3-does-not-exist-' + Date.now())]);
check('refuses a directory that does not exist', missing.code === 2 && /cannot read/.test(missing.stderr),
      `code=${missing.code} stderr=${missing.stderr.slice(0, 80)}`);

// 3. A file where a directory is expected must refuse.
const scratch = mkdtempSync(join(tmpdir(), 'sx3-openers-'));
const notDir = join(scratch, 'a-file.html');
writeFileSync(notDir, '<html></html>');
const file = run([notDir]);
check('refuses a file where a directory is expected', file.code === 2 && /cannot read/.test(file.stderr),
      `code=${file.code} stderr=${file.stderr.slice(0, 80)}`);

// 4. An empty directory must refuse rather than report "0 decks, all fine".
const empty = join(scratch, 'empty');
mkdirSync(empty);
const none2 = run([empty]);
check('refuses a directory with no decks in it', none2.code === 2 && /contains no .html deck/.test(none2.stderr),
      `code=${none2.code} stderr=${none2.stderr.slice(0, 80)}`);

// 5. The scope it measured must be PRINTED, with the resolved path and a count,
//    so a wrong directory is visible in the output rather than inferred.
const real = join(scratch, 'decks');
mkdirSync(real);
writeFileSync(join(real, 'deck.html'),
  '<html><body><button data-action="open">Open</button>' +
  '<dialog id="reachable-dialog"></dialog>' +
  '<script>document.querySelector("button").addEventListener("click",()=>document.getElementById("reachable-dialog").showModal())</script>' +
  '</body></html>');
const ok = run([real, join(scratch, 'out.json')]);
check('prints the resolved scope and the deck count', /SEARCH SCOPE: 1 deck\(s\) in /.test(ok.stdout) && ok.stdout.includes(real),
      ok.stdout.slice(0, 120));
check('passes a deck whose dialog can be opened', ok.code === 0 && /all dialogs openable: 1/.test(ok.stdout),
      `code=${ok.code} ${ok.stdout.slice(0, 120)}`);

// 6. And it must go RED on a deck carrying a dialog nothing opens. A harness
//    that cannot fail is not a harness.
const bad = join(scratch, 'bad');
mkdirSync(bad);
writeFileSync(join(bad, 'deck.html'),
  '<html><body><dialog id="unreachable-dialog"></dialog></body></html>');
const red = run([bad, join(scratch, 'bad.json')]);
check('fails a deck carrying a dialog nothing opens', red.code === 1 && /unopenable: unreachable-dialog/.test(red.stdout),
      `code=${red.code} ${red.stdout.slice(0, 140)}`);

console.log(failures ? `\n${failures} check(s) failed` : '\nall checks passed');
process.exit(failures ? 1 : 0);
