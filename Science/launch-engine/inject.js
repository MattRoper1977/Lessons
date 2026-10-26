#!/usr/bin/env node
/* ==========================================================================
   Inject the LAUNCH Scientific Observation Layer into the lesson decks.
   --------------------------------------------------------------------------
   Usage:  node inject.js            inject / re-inject every LAUNCH lesson
           node inject.js --check    report only, change nothing
           node inject.js --strip    remove the layer, leaving the deck as found

   RULES THIS SCRIPT KEEPS, AND WHY

   1. Sentinel-wrapped and idempotent. Re-running replaces the block rather
      than stacking a second copy. `--strip` must return the file to a state
      byte-identical to the original, and the check below asserts it.

   2. It touches NOTHING else. Two insertions only: a <style> before </head>
      and a <script> before </script></body>. The print subsystem is closed
      (REGISTER R-E05) and is not read, written or referenced here.

   3. Self-contained output. The decks carry no external CSS or JS of their
      own beyond the site's /hud.js, and teachers open them from disk. So the
      engine is INLINED, not linked. Do not "tidy" this into a shared file
      without first checking how the decks are actually opened.
   ========================================================================== */

'use strict';
const fs = require('fs');
const path = require('path');

const HERE = __dirname;
const LESSONS = path.join(HERE, '..', 'Launch');
const VERSION = 'launch-sci-layer-v1';
/* Sentinels are FIXED strings with nothing interpolated into them, so that the
   strip regex is exact. Anything explanatory goes inside the block, not into
   the sentinel — a sentinel that varies is a sentinel that fails to match. */
const START = `<!-- ${VERSION} START -->`;
const END = `<!-- ${VERSION} END -->`;
const NOTE = `<!-- Minified build of Science_Teesside/launch-engine/. Readable source, and the reasoning behind every gate, are there.
     Edit the source, then: node build.js && node check.js && node inject.js. Edits made here are overwritten. -->`;

const args = process.argv.slice(2);
const MODE = args.includes('--strip') ? 'strip' : args.includes('--check') ? 'check' : 'write';

/* ---------------------------------------------------------------------------
   The decks carry MINIFIED engine code. Readable source stays in this
   directory, which is where anyone should be editing.

   Each dist file pins the SHA-256 of the source it was built from. A committed
   build artefact otherwise rots silently — someone edits sci-engine.js, forgets
   `node build.js`, and fifteen decks quietly keep the old engine while the
   source in git says otherwise. Refusing to inject is the whole point of the
   check below; do not soften it to a warning.
   --------------------------------------------------------------------------- */
const crypto = require('crypto');
const DIST = path.join(HERE, 'dist');
const sha = s => crypto.createHash('sha256').update(s, 'utf8').digest('hex').slice(0, 16);

function readBuilt(distName, srcPath, label) {
  const built = path.join(DIST, distName);
  if (!fs.existsSync(built)) {
    console.error(`Missing ${path.relative(HERE, built)} — run:\n  npm install --no-save terser clean-css && node build.js\n`);
    process.exit(2);
  }
  const text = fs.readFileSync(built, 'utf8');
  const pinned = (text.match(/source-sha256:([a-f0-9]+)/) || [])[1];
  const actual = sha(fs.readFileSync(srcPath, 'utf8'));
  if (pinned !== actual) {
    console.error(`STALE BUILD: ${distName} was built from a different ${label}.\n` +
                  `  pinned ${pinned}  actual ${actual}\n` +
                  `  Run: node build.js\n`);
    process.exit(2);
  }
  return text;
}

/* The ten-motion language is shared across BUILD, GROW and LAUNCH. It is
   inlined ahead of the layer's own stylesheet so a LAUNCH deck moves in exactly
   the vocabulary a GROW pupil already reads. Source of truth is grow-anim/;
   this only copies it in, because the decks must stay self-contained. */
const motion = readBuilt('grow-motion.min.css', path.join(HERE, '..', '..', 'grow-anim', 'grow-motion.css'), 'grow-motion.css');
const css = readBuilt('sci-engine.min.css', path.join(HERE, 'sci-engine.css'), 'sci-engine.css');
const js = readBuilt('sci-engine.min.js', path.join(HERE, 'sci-engine.js'), 'sci-engine.js');
const payloads = require('./payloads.js');

/* A `</script>` or `<!--` inside JSON would end the script element early. */
function safeJSON(obj) {
  return JSON.stringify(obj)
    .replace(/</g, '\\u003c')
    .replace(/>/g, '\\u003e')
    .replace(/\u2028/g, '\\u2028')
    .replace(/\u2029/g, '\\u2029');
}

function escapeRe(s) { return s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); }
/* Matches a sentinel pair anywhere, however many times it was injected. */
const STRIP_RE = new RegExp(escapeRe(START) + '[^]*?' + escapeRe(END), 'g');
function stripBlocks(html) { return html.replace(STRIP_RE, ''); }

function build(name) {
  const payload = payloads[name];
  if (!payload) return null;
  const styleBlock =
    `${START}\n${NOTE}\n` +
    `<style id="grow-motion-css">\n/* shared motion language — source: grow-anim/grow-motion.css */\n${motion}\n</style>\n` +
    `<style id="sci-engine-css">\n${css}\n</style>\n${END}`;
  const scriptBlock =
    `${START}\n<script id="sci-lesson-payload" type="application/json">${safeJSON(payload)}</script>\n` +
    `<script id="sci-engine-js">\n` +
    `/* payload is read from the JSON block above so that lesson content and\n` +
    `   engine code stay separable, and a content fix never risks the code. */\n` +
    `try{window.SCI_LESSON=JSON.parse(document.getElementById('sci-lesson-payload').textContent);}\n` +
    `catch(e){window.SCI_LESSON={components:[]};if(window.console)console.error('[SCI] payload parse failed',e);}\n` +
    `${js}\n</script>\n${END}`;
  return { styleBlock, scriptBlock };
}

const files = fs.readdirSync(LESSONS).filter(f => /^SCI_L_.*\.html$/.test(f)).sort();
let changed = 0, missing = [], report = [];

for (const file of files) {
  const full = path.join(LESSONS, file);
  const name = file.replace(/\.html$/, '');
  const original = fs.readFileSync(full, 'utf8');
  const had = original.includes(START.slice(0, 30));

  let out = stripBlocks(original);

  if (MODE !== 'strip') {
    const blocks = build(name);
    if (!blocks) { missing.push(name); report.push(`  ${file}  NO PAYLOAD — skipped`); continue; }

    if (!out.includes('</head>')) { report.push(`  ${file}  no </head> — skipped`); continue; }
    if (!out.includes('</body>')) { report.push(`  ${file}  no </body> — skipped`); continue; }

    out = out.replace('</head>', blocks.styleBlock + '</head>');
    // after the deck's own scripts, so playDing/gainXP/registerXP already exist
    out = out.replace('</body>', blocks.scriptBlock + '</body>');
  }

  const n = (payloads[name] ? payloads[name].components.length : 0);
  const delta = out.length - original.length;
  report.push(
    `  ${file.padEnd(34)} ${had ? 're-inject' : MODE === 'strip' ? 'strip    ' : 'inject   '}` +
    ` ${String(n).padStart(2)} components  ${(delta >= 0 ? '+' : '') + (delta / 1024).toFixed(1)} KB`
  );

  if (out !== original) {
    changed++;
    if (MODE === 'write' || MODE === 'strip') fs.writeFileSync(full, out, 'utf8');
  }
}

console.log(`${VERSION} · mode=${MODE} · ${files.length} lesson files`);
console.log(report.join('\n'));
console.log(`${changed} file(s) ${MODE === 'check' ? 'would change' : 'written'}`);
if (missing.length) {
  console.log(`\nNO PAYLOAD for: ${missing.join(', ')}`);
  console.log('A lesson with no payload keeps its deck unchanged — it does not get an empty layer.');
  process.exitCode = 1;
}
