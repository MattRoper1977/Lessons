/* Live-Teach static gates — the greppable half of the phase gates.

   G-ONMSG  assigning `.onmessage =` anywhere in liveteach is a failure: two of
            the reviewed fragments each overwrote onmessage on the same channel
            and silently killed the other's handlers. addEventListener only.
   G-RAF    one animation loop per view (spec G4): every requestAnimationFrame
            call in a view must pass the same single callback identifier, so a
            second loop cannot slip in beside the first.
   G-TDZ    every stamped core region is followed by its LT.boot() init — init
            sits immediately after the module, never above it (the estate's
            thrice-bitten TDZ rule), and never wrapped in a bare catch.

     node tools/liveteach/static_gates.mjs            gate the tree
     node tools/liveteach/static_gates.mjs --self-test  prove each gate can fail */
import fs from 'node:fs';
import path from 'node:path';

const HERE = path.dirname(new URL(import.meta.url).pathname);
const ROOT = path.resolve(HERE, '..', '..');
const VIEW_DIR = path.join(ROOT, 'liveteach');
const ONMSG = /\.onmessage\s*=/;

function viewFiles(dir) {
  if (!fs.existsSync(dir)) return [];
  return fs.readdirSync(dir).filter(f => f.endsWith('.html') || f.endsWith('.js')).map(f => path.join(dir, f));
}

export function judge(file, text) {
  const fails = [];
  if (ONMSG.test(text)) fails.push('G-ONMSG: `.onmessage =` assignment found');
  if (file.endsWith('.html')) {
    const rafs = [...text.matchAll(/requestAnimationFrame\(\s*([A-Za-z_$][\w$]*)\s*\)/g)].map(m => m[1]);
    const distinct = [...new Set(rafs)];
    if (distinct.length > 1) fails.push('G-RAF: more than one rAF callback (' + distinct.join(', ') + ') — one loop per view');
    if (text.includes('MBM-LIVETEACH-CORE:END')) {
      const after = text.slice(text.indexOf('MBM-LIVETEACH-CORE:END'));
      const bootAt = after.indexOf('LT.boot()');
      if (bootAt === -1 || bootAt > 400) fails.push('G-TDZ: LT.boot() must directly follow the stamped core region');
      const guard = after.slice(0, bootAt === -1 ? 400 : bootAt);
      if (/try\s*\{\s*$/.test(guard.trimEnd())) fails.push('G-TDZ: LT.boot() is wrapped in a catch — a failed init must be a visible error');
    }
  }
  return fails;
}

function run(files) {
  let bad = 0;
  for (const f of files) {
    const text = fs.readFileSync(f, 'utf8');
    for (const fail of judge(f, text)) {
      console.log('[FAIL] ' + path.relative(ROOT, f) + ': ' + fail);
      bad++;
    }
  }
  return bad;
}

if (process.argv[2] === '--self-test') {
  // Each gate must be able to go red: seed one violation per gate and demand
  // it is reported, then demand the clean vectors pass.
  let bad = 0;
  const say = (ok, label) => { console.log('  ' + (ok ? 'PASS' : 'FAIL') + '  ' + label); if (!ok) bad++; };
  say(judge('x.html', 'bus.onmessage = function(){};').some(s => s.includes('G-ONMSG')), 'RED: an onmessage assignment is reported');
  say(judge('x.html', 'bus.addEventListener("message", h);').length === 0, 'GREEN: addEventListener alone is clean');
  say(judge('x.html', 'requestAnimationFrame(loop); requestAnimationFrame(secondLoop);').some(s => s.includes('G-RAF')), 'RED: a second rAF loop is reported');
  say(judge('x.html', 'requestAnimationFrame(loop); requestAnimationFrame(loop);').every(s => !s.includes('G-RAF')), 'GREEN: one callback, called twice, is one loop');
  say(judge('x.html', '<!-- MBM-LIVETEACH-CORE:END -->\n<script>\nsomethingElse();\n</script>').some(s => s.includes('G-TDZ')), 'RED: a missing post-region LT.boot() is reported');
  say(judge('x.html', '<!-- MBM-LIVETEACH-CORE:END -->\n<script>\nLT.boot();\n</script>').every(s => !s.includes('G-TDZ')), 'GREEN: immediate LT.boot() is clean');
  console.log(bad ? '[SELF-TEST] FAIL — ' + bad + ' check(s)' : '[SELF-TEST] PASS');
  process.exit(bad ? 1 : 0);
} else {
  const files = [...viewFiles(VIEW_DIR), path.join(HERE, 'core_source.js')];
  const bad = run(files);
  if (bad) { console.log(bad + ' static-gate failure(s).'); process.exit(1); }
  console.log('[OK] static gates clean across ' + files.length + ' file(s)');
}
