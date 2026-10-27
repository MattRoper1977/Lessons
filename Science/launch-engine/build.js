#!/usr/bin/env node
/* ==========================================================================
   Build the minified artefacts that inject.js inlines into the decks.
   --------------------------------------------------------------------------
       npm install --no-save terser clean-css
       node build.js

   WHY THERE IS A BUILD STEP AT ALL

   The engine ships inside fifteen self-contained lesson files. Unminified it
   added ~100 KB to each, roughly doubling them. The reasoning comments in the
   source are worth keeping — they are the record of why nothing reveals early
   — but they are worth keeping in ONE place, not fifteen.

   So: readable source lives here, minified output goes in `dist/`, and the
   decks carry a pointer back to this directory.

   WHY dist/ IS COMMITTED, AND WHY IT CANNOT GO STALE

   `inject.js` must run with no dependencies — it is the thing anyone touching
   a lesson will reach for, and making it need `npm install` would eventually
   mean someone edits the injected block by hand instead. So dist/ is committed
   and inject.js just reads it.

   A committed build artefact normally rots: someone edits the source, forgets
   to rebuild, and the decks silently keep the old engine. Every dist file
   therefore carries the SHA-256 of the source it was built from, and BOTH
   inject.js and check.js refuse to proceed when it does not match. Staleness
   becomes a loud failure rather than a silent one.
   ========================================================================== */

'use strict';
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const HERE = __dirname;
const DIST = path.join(HERE, 'dist');

let Terser, CleanCSS;
try {
  Terser = require('terser');
  CleanCSS = require('clean-css');
} catch (e) {
  console.error('Missing build tools. Run:\n  npm install --no-save terser clean-css\n');
  process.exit(1);
}

const sha = s => crypto.createHash('sha256').update(s, 'utf8').digest('hex').slice(0, 16);

/* The banner is the contract: it names the source and pins its hash. Do not
   strip it — inject.js and check.js both read it. */
function banner(srcName, srcText) {
  return `/*! LAUNCH Scientific Observation Layer — generated from ${srcName} */\n` +
         `/*! source-sha256:${sha(srcText)} — do not edit; edit the source and run build.js */\n`;
}

const targets = [
  { src: path.join(HERE, 'sci-engine.js'), out: 'sci-engine.min.js', name: 'launch-engine/sci-engine.js', kind: 'js' },
  { src: path.join(HERE, 'sci-engine.css'), out: 'sci-engine.min.css', name: 'launch-engine/sci-engine.css', kind: 'css' },
  { src: path.join(HERE, '..', '..', 'grow-anim', 'grow-motion.css'), out: 'grow-motion.min.css', name: 'grow-anim/grow-motion.css', kind: 'css' }
];

(async () => {
  fs.mkdirSync(DIST, { recursive: true });
  let total = 0, totalMin = 0;

  for (const t of targets) {
    const src = fs.readFileSync(t.src, 'utf8');
    let min;

    if (t.kind === 'js') {
      const r = await Terser.minify(src, {
        /* The engine is ES5 on purpose — these decks get opened on whatever is
           on the classroom machine. Keep the output at the same level. */
        ecma: 5,
        compress: { passes: 2, drop_debugger: true },
        mangle: true,
        format: { comments: false, ascii_only: false }
      });
      if (r.error) throw r.error;
      min = r.code;
    } else {
      const r = new CleanCSS({ level: 2, returnPromise: false }).minify(src);
      if (r.errors && r.errors.length) throw new Error(r.errors.join('; '));
      /* clean-css level 2 merges rules across the sheet. That is safe here
         because neither sheet relies on duplicate-selector ordering, but it is
         worth knowing if a future rule ever does. */
      if (r.warnings && r.warnings.length) {
        r.warnings.slice(0, 3).forEach(w => console.log(`    warning: ${w}`));
      }
      min = r.styles;
    }

    const body = banner(t.name, src) + min + '\n';
    fs.writeFileSync(path.join(DIST, t.out), body, 'utf8');
    total += src.length; totalMin += body.length;
    const pct = (100 - (body.length / src.length) * 100).toFixed(0);
    console.log(`  ${t.out.padEnd(22)} ${(src.length / 1024).toFixed(1).padStart(6)} KB → ${(body.length / 1024).toFixed(1).padStart(6)} KB  (−${pct}%)`);
  }

  console.log(`  ${'total'.padEnd(22)} ${(total / 1024).toFixed(1).padStart(6)} KB → ${(totalMin / 1024).toFixed(1).padStart(6)} KB  ` +
              `(−${(100 - (totalMin / total) * 100).toFixed(0)}%)`);
  console.log('\nNow run: node check.js && node inject.js');
})().catch(e => { console.error('build failed:', e.message); process.exit(1); });
