#!/usr/bin/env node
/* ==========================================================================
   Contract checker for the LAUNCH Scientific Observation Layer.
   Run with plain `node check.js` — no browser, no dependencies.
   --------------------------------------------------------------------------
   WHY THIS EXISTS

   A `discover` or `method` step names SVG group ids it will reveal. If an id
   does not exist in the scene, the step still runs, still asks its question,
   still ticks itself off — and reveals nothing. The component looks like it is
   working. That failure is invisible to a browser smoke test and invisible to
   a screenshot of any single step, and it shipped once already (the alveolus
   builder had `parts: []` on all three steps).

   So: every id a payload names must exist in the scene it names. This checks
   that, plus the other contracts that fail silently rather than loudly.
   ========================================================================== */

'use strict';
const fs = require('fs');
const path = require('path');
const vm = require('vm');

const HERE = __dirname;
const payloads = require('./payloads.js');
const engineSrc = fs.readFileSync(path.join(HERE, 'sci-engine.js'), 'utf8');

/* Enough of a DOM for the engine to define itself. It bails out of mounting
   because there are no .slide elements, which is exactly what we want. */
const stubNode = () => ({
  setAttribute() {}, getAttribute() { return null; }, appendChild() {},
  addEventListener() {}, removeAttribute() {}, querySelector() { return null; },
  querySelectorAll() { return []; }, style: {}, classList: { add() {}, remove() {} }
});
const sandbox = {
  window: {}, console,
  document: {
    readyState: 'complete',
    createElement: stubNode, createElementNS: stubNode,
    querySelector: () => null, querySelectorAll: () => [],
    addEventListener() {}, getElementById: () => null
  },
  setTimeout, clearTimeout, setInterval, clearInterval, requestAnimationFrame: () => 0, Math, Date, JSON
};
sandbox.window.document = sandbox.document;
sandbox.window.matchMedia = () => ({ matches: false });
vm.createContext(sandbox);
vm.runInContext(engineSrc, sandbox);
const SCI = sandbox.window.SCI;

let problems = [];
function fail(where, msg) { problems.push(`${where}: ${msg}`); }

/* the ten slide titles every LAUNCH deck actually has */
const SLIDES = new Set(['Title', 'Arrival Task', 'Today at a Glance', 'I Do 1', 'We Do 1',
  'I Do 2', 'We Do 2', 'Independent Work', 'Lundy Loop', 'Exit Ticket']);

/* parts are addressed by data-part (see sci-engine.js) — ids belong to
   generated gradient/clip references and must never be named by a payload */
const partsIn = svg => new Set([...svg.matchAll(/data-part="([^"]+)"/g)].map(m => m[1]));

let checked = 0;
for (const [lesson, payload] of Object.entries(payloads)) {
  const seenKeys = new Set();
  payload.components.forEach((c, i) => {
    const where = `${lesson} · ${c.key || '#' + i}`;
    checked++;

    if (!c.key) fail(where, 'no key — the layer cannot stay idempotent without one');
    if (seenKeys.has(c.key)) fail(where, 'duplicate key within the lesson');
    seenKeys.add(c.key);

    if (!SCI.comps[c.type]) fail(where, `unknown component type "${c.type}"`);
    if (!SLIDES.has(c.slide)) fail(where, `slide "${c.slide}" is not one of the deck's ten`);
    /* `after` is legitimate on a pause (its follow-up sentence). It is only a
       bug when it holds a SELECTOR, which means the author meant `anchor` —
       the mistake that once fed a whole sentence to querySelector. */
    if (typeof c.after === 'string' && /^[.#][\w-]+$/.test(c.after)) {
      fail(where, `\`after: "${c.after}"\` looks like a mount anchor — the key for that is \`anchor\``);
    }
    if (c.anchor && !/^[.#][\w-]+$/.test(c.anchor)) {
      fail(where, `\`anchor: "${c.anchor}"\` is not a simple selector`);
    }

    /* every scene named must exist */
    const scenes = [];
    if (c.scene) scenes.push([c.scene, c.sceneOpts]);
    (c.levels || []).forEach(l => scenes.push([l.scene, l.sceneOpts]));
    (c.panels || []).forEach(p => scenes.push([p.scene, p.sceneOpts]));
    scenes.forEach(([name]) => { if (!SCI.scenes[name]) fail(where, `scene "${name}" does not exist`); });

    /* every part id a step reveals must exist in that component's scene */
    if (c.scene && SCI.scenes[c.scene]) {
      const ids = partsIn(SCI.scenes[c.scene](c.sceneOpts || {}));
      (c.steps || []).forEach(st => {
        if (!st.parts || !st.parts.length) {
          fail(where, `step "${st.name || st.label}" reveals nothing — it will tick itself off and show no science`);
        }
        (st.parts || []).forEach(id => {
          if (!ids.has(id)) fail(where, `step "${st.name || st.label}" names part "${id}", which is not in scene "${c.scene}"`);
        });
      });
    }

    /* a simulator must exist and must actually respond to each of its params */
    if (c.type === 'model') {
      const sim = SCI.sims[c.sim];
      if (!sim) { fail(where, `sim "${c.sim}" does not exist`); return; }
      const base = {}; (sim.params || []).forEach(p => base[p.key] = (c.start && c.start[p.key] != null) ? c.start[p.key] : p.value);
      const ref = JSON.stringify(sim.render(base, c));
      (sim.params || []).forEach(p => {
        const alt = Object.assign({}, base);
        alt[p.key] = p.type === 'choice'
          ? (p.options.find(o => o.value !== base[p.key]) || p.options[0]).value
          : (base[p.key] === p.max ? p.min : p.max);
        if (JSON.stringify(sim.render(alt, c)) === ref) {
          fail(where, `control "${p.label}" changes nothing — a control that does not move the model is a lie about the science`);
        }
      });
    }

    /* THE WITHHOLDING RULE, mechanically enforced.
       `observe` and `discover` exist to make a pupil name things themselves. A
       scene that prints its own captions hands the answer over before the
       question is asked, and it is invisible in a screenshot of the finished
       state — you only see it mid-build. So: a scene used by either component
       must suppress its captions when asked to be bare, and must never print
       any of the words the component is about to reveal. */
    if ((c.type === 'observe' || c.type === 'discover') && c.scene && SCI.scenes[c.scene]) {
      const opts = c.sceneOpts || {};
      const stripped = SCI.scenes[c.scene](Object.assign({}, opts, { bare: true }));
      const tagsOf = svg => [...svg.matchAll(/<text([^>]*)>([^<]*)<\/text>/g)];
      const left = tagsOf(stripped).map(m => m[2].toLowerCase());
      /* Any text surviving a bare render must be explicitly marked neutral —
         a caption that orients the pupil ("what you see") rather than one that
         names a structure for them. Marking is the author saying so on the
         record; silence is treated as an unsuppressed label. */
      tagsOf(stripped).forEach(m => {
        if (!/class="[^"]*sci-neutral/.test(m[1])) {
          fail(where, `scene "${c.scene}" still prints "${m[2].trim()}" when bare. Suppress it, or mark it class="sci-neutral" if it names nothing the pupil must work out.`);
        }
      });
      const reveals = (c.hotspots || []).map(h => h.label).concat((c.labels || []).map(l => l.label));
      reveals.forEach(label => {
        const words = String(label).toLowerCase().split(/[^a-z]+/).filter(w => w.length > 4);
        left.forEach(t => {
          if (words.length && words.every(w => t.includes(w))) {
            fail(where, `scene "${c.scene}" still prints "${t.trim()}", which is what the label "${label}" is supposed to reveal`);
          }
        });
      });
    }

    /* pedagogy contracts: LAUNCH withholds, so the withholding must be there */
    if (c.type === 'observe') {
      if (!(c.hotspots || []).length) fail(where, 'observe with no hotspots reveals nothing after the looking');
      (c.hotspots || []).forEach(h => {
        if (h.x < 0 || h.x > 100 || h.y < 0 || h.y > 100) fail(where, `hotspot "${h.label}" is outside the figure (${h.x},${h.y})`);
      });
      if ((c.holdSeconds != null && c.holdSeconds < 5)) fail(where, 'holdSeconds under 5 is not long enough to make anyone look');
    }
    if (c.type === 'chain' && (c.stages || []).length < 3) fail(where, 'a chain shorter than 3 is not a chain');
    if (c.type === 'compare') {
      if ((c.panels || []).length !== 2) fail(where, 'compare needs exactly two panels');
      if (!(c.differences || []).length) fail(where, 'compare with no differences to find');
      if (!c.explanation) fail(where, 'compare with nothing behind the lock');
    }
    if (c.type === 'graph') {
      if ((c.points || []).length < 3) fail(where, 'a graph of fewer than 3 points shows no pattern');
      if (!c.caveat) fail(where, 'invented or typical data must carry a caveat saying so');
    }
    if (c.type === 'zoom' && (c.levels || []).length < 3) fail(where, 'a zoom of fewer than 3 levels does not teach scale');
    if ((c.type === 'pause') && !(c.options || []).length) fail(where, 'a pause with no options cannot record a prediction');
  });
}

/* ---------------------------------------------------------------------------
   THE SHARED MOTION LANGUAGE
   grow-anim/grow-motion.css defines ten movements that mean the same thing in
   BUILD, GROW and LAUNCH. A pupil arriving in LAUNCH already reads them. If
   this layer defines its own version of one, the same movement starts meaning
   two things depending on which folder the lesson came from — and that is
   invisible until a pupil is confused by it in a classroom.
   --------------------------------------------------------------------------- */
{
  const motionPath = path.join(HERE, '..', '..', 'grow-anim', 'grow-motion.css');
  if (!fs.existsSync(motionPath)) {
    fail('motion', 'grow-anim/grow-motion.css is missing — the layer inlines it and cannot build without it');
  } else {
    const shared = fs.readFileSync(motionPath, 'utf8');
    const ours = fs.readFileSync(path.join(HERE, 'sci-engine.css'), 'utf8');
    const classesIn = css => new Set([...css.matchAll(/\.(g-[a-z0-9-]+)\s*[,{:]/g)].map(m => m[1]));
    const sharedClasses = classesIn(shared);
    /* we may USE a .g- class from JS, but must never restyle one here */
    classesIn(ours).forEach(c => {
      if (sharedClasses.has(c)) fail('motion', `sci-engine.css restyles "${c}", which belongs to the shared motion language`);
    });
    /* THE HOLE THIS CLOSES. Refusing to RESTYLE a .g- class is not enough — a
       private class under a different name is a rival spelling of the same
       verb, and nothing above would have caught it. `.sci-spot` was exactly
       that: a radial-gradient reimplementation of `.g-spot`, carrying the same
       sentence in its comment. Pupils would have met two spellings of "look
       here, everything else is off" depending on which pathway they were in.
       So: no private class may take the NAME of a shared verb. */
    const verbNames = new Set([...sharedClasses].map(c => c.replace(/^g-/, '')));
    [...ours.matchAll(/\.sci-([a-z0-9-]+)\s*[,{:[]/g)].map(m => m[1]).forEach(name => {
      if (verbNames.has(name)) {
        fail('motion', `sci-engine.css defines ".sci-${name}", a private spelling of the shared verb ".g-${name}". ` +
          `Use the shared class; if this layer needs to ADD to it, name the addition something the vocabulary does not already own.`);
      }
    });

    /* and every .g- class the engine applies must actually be defined there */
    const engine = fs.readFileSync(path.join(HERE, 'sci-engine.js'), 'utf8');
    /* The lookbehind matters: it stops `sci-ring-bg` matching as "g-bg" and
       stops the custom property `--g-heat` matching as a class name. */
    [...engine.matchAll(/(?<![\w-])(g-[a-z0-9-]+)/g)].map(m => m[1]).forEach(c => {
      if (!sharedClasses.has(c)) fail('motion', `engine applies "${c}", which grow-motion.css does not define`);
    });
  }
}

/* ---------------------------------------------------------------------------
   BUILD FRESHNESS
   The decks carry minified code from dist/. Every dist file pins the SHA-256
   of its source. Checking it here as well as in inject.js means the failure
   surfaces when someone runs the checker, not only when they inject.
   --------------------------------------------------------------------------- */
{
  const crypto = require('crypto');
  const sha = t => crypto.createHash('sha256').update(t, 'utf8').digest('hex').slice(0, 16);
  [
    ['dist/sci-engine.min.js', 'sci-engine.js'],
    ['dist/sci-engine.min.css', 'sci-engine.css'],
    ['dist/grow-motion.min.css', path.join('..', '..', 'grow-anim', 'grow-motion.css')]
  ].forEach(([built, src]) => {
    const bp = path.join(HERE, built), sp = path.join(HERE, src);
    if (!fs.existsSync(bp)) return fail('build', `${built} is missing — run: node build.js`);
    const pinned = (fs.readFileSync(bp, 'utf8').match(/source-sha256:([a-f0-9]+)/) || [])[1];
    const actual = sha(fs.readFileSync(sp, 'utf8'));
    if (pinned !== actual) {
      fail('build', `${built} is STALE — built from a different ${path.basename(src)} (pinned ${pinned}, actual ${actual}). Run: node build.js`);
    }
  });
}

/* every lesson file must have a payload, and vice versa */
const files = fs.readdirSync(path.join(HERE, '..', 'Launch'))
  .filter(f => /^SCI_L_.*\.html$/.test(f)).map(f => f.replace(/\.html$/, ''));
files.forEach(f => { if (!payloads[f]) fail(f, 'lesson has no payload'); });
Object.keys(payloads).forEach(k => { if (!files.includes(k)) fail(k, 'payload has no lesson file'); });

console.log(`checked ${checked} components across ${Object.keys(payloads).length} lessons`);
if (problems.length) {
  console.log('\n' + problems.map(p => '  ✗ ' + p).join('\n'));
  console.log(`\n${problems.length} problem(s)`);
  process.exit(1);
}
console.log('all contracts hold');
