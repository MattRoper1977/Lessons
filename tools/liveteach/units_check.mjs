/* Live-Teach units check — the content-accuracy gate (spec G5 + W2 policy).

   For every manifest under liveteach/manifests/:
   U-CLAIM  each claim's expr, recomputed from the stage's own params, must
            equal its declared value, AND the printed number must appear in
            the claim text with its unit — a pupil checking the maths finds it
            correct, by construction.
   U-COORD  every spotlight/label coordinate is normalised 0–1 (G3 —
            manifests carry no pixel positions).
   U-DOUBLE a stage whose title or copy says "double"/"doubles"/"doubling"
            about frequency must carry exactly 2× the previous wave stage's f.
   U-PARAMS wave params are positive finite numbers; px_per_m is declared.

     node tools/liveteach/units_check.mjs             gate the manifests
     node tools/liveteach/units_check.mjs --self-test prove each rule can fail */
import fs from 'node:fs';
import path from 'node:path';

const HERE = path.dirname(new URL(import.meta.url).pathname);
const ROOT = path.resolve(HERE, '..', '..');
const MDIR = path.join(ROOT, 'liveteach', 'manifests');

function loadManifest(src) {
  const sandbox = {};
  // Manifests are browser scripts that assign window.LT_MANIFEST.
  new Function('window', src)(sandbox);
  return sandbox.LT_MANIFEST;
}

function evalExpr(expr, params) {
  if (!/^[0-9a-z_+\-*/(). ]+$/.test(expr)) throw new Error('illegal characters in expr: ' + expr);
  const names = Object.keys(params);
  return new Function(...names, 'return (' + expr + ');')(...names.map(n => params[n]));
}

export function judge(m) {
  const fails = [];
  if (!m || !Array.isArray(m.stages)) return ['not a manifest'];
  if (!m.units || typeof m.units.px_per_m !== 'number' || m.units.px_per_m <= 0)
    fails.push('U-PARAMS: units.px_per_m missing or not a positive number');
  let prevWave = null;
  m.stages.forEach((s, i) => {
    const at = 'stage ' + i + ' ("' + (s.title || '?') + '")';
    if (s.mode === 'wave') {
      for (const k of ['f', 'lambda', 'A']) {
        const v = s.params && s.params[k];
        if (typeof v !== 'number' || !isFinite(v) || v <= 0) fails.push('U-PARAMS: ' + at + ' param ' + k + ' must be a positive number');
      }
    }
    for (const c of s.claims || []) {
      let got;
      try { got = evalExpr(c.expr, s.params || {}); }
      catch (e) { fails.push('U-CLAIM: ' + at + ' expr unreadable: ' + e.message); continue; }
      if (Math.abs(got - c.value) > 1e-9)
        fails.push('U-CLAIM: ' + at + ' says ' + c.value + ' ' + c.unit + ' but ' + c.expr + ' = ' + got);
      /* The printed number must be THE number attached to the unit, with
         digit boundaries — a substring probe passed "12 m/s" for value 2
         (the review's live false-pass). */
      const esc = x => String(x).replace(/[.*+?^${}()|[\]\\/]/g, '\\$&');
      const bound = new RegExp('(^|[^\\d.])' + esc(c.value) + '\\s*' + esc(c.unit) + '($|[^\\w])');
      if (!bound.test(c.text))
        fails.push('U-CLAIM: ' + at + ' text does not print exactly ' + c.value + ' ' + c.unit + ' ("' + c.text + '")');
    }
    /* Pupils never read claims[].text — they read copy and labels. Every
       quantitative statement THERE must match the stage params too. */
    if (s.mode === 'wave' && s.params) {
      const visible = [s.copy || ''].concat((s.labels || []).map(l => l.text || ''));
      const rules = [
        [/f\s*=\s*([\d.]+)\s*Hz/g, s.params.f, 'f'],
        [/λ\s*=\s*([\d.]+)\s*m(?![\w/])/g, s.params.lambda, 'λ'],
        [/v\s*=[^=]*?([\d.]+)\s*m\/s/g, s.params.f * s.params.lambda, 'v'],
      ];
      for (const text of visible) {
        for (const [re, want, name] of rules) {
          for (const m of text.matchAll(re)) {
            if (Math.abs(Number(m[1]) - want) > 1e-9)
              fails.push('U-VISIBLE: ' + at + ' pupil-visible text prints ' + name + ' = ' + m[1] + ' but the stage params say ' + want + ' ("' + text.slice(0, 60) + '…")');
          }
        }
      }
    }
    for (const [what, coords] of [['spotlight', s.spotlight ? [s.spotlight.x, s.spotlight.y, s.spotlight.w, s.spotlight.h] : null],
                                  ...((s.labels || []).map((l, j) => ['label ' + j, [l.x, l.y]]))]) {
      if (!coords) continue;
      for (const v of coords) {
        if (typeof v !== 'number' || v < 0 || v > 1) fails.push('U-COORD: ' + at + ' ' + what + ' carries a non-normalised coordinate (' + v + ') — 0–1 only, no pixels');
      }
    }
    for (const [j, l] of (s.labels || []).entries()) {
      if (typeof l.y === 'number' && l.y < 0.12)
        fails.push('U-COORD: ' + at + ' label ' + j + ' sits in the banner band (y=' + l.y + ' < 0.12) and will be covered');
    }
    const prose = ((s.title || '') + ' ' + (s.copy || '')).toLowerCase();
    if (s.mode === 'wave' && /doubl/.test(prose) && /frequen/.test(prose)) {
      if (!prevWave) fails.push('U-DOUBLE: ' + at + ' doubles frequency with no previous wave stage to double from');
      else if (Math.abs(s.params.f - 2 * prevWave.params.f) > 1e-9)
        fails.push('U-DOUBLE: ' + at + ' says frequency doubles but f is ' + s.params.f + ' after ' + prevWave.params.f + ' (needs exactly 2x)');
    }
    if (s.mode === 'wave') prevWave = s;
  });
  return fails;
}

if (process.argv[2] === '--self-test') {
  let bad = 0;
  const say = (ok, label) => { console.log('  ' + (ok ? 'PASS' : 'FAIL') + '  ' + label); if (!ok) bad++; };
  const base = { units: { px_per_m: 100 }, stages: [] };
  const wave = (over) => Object.assign({ title: 't', mode: 'wave', params: { f: 1, lambda: 2, A: 1 }, copy: '' }, over);
  say(judge({ ...base, stages: [wave({ claims: [{ text: 'v = 3 m/s', expr: 'f*lambda', value: 3, unit: 'm/s' }] })] })
    .some(s => s.includes('U-CLAIM')), 'RED: a wrong claim value is reported (says 3, is 2)');
  say(judge({ ...base, stages: [wave({ claims: [{ text: 'v = 2 m/s', expr: 'f*lambda', value: 2, unit: 'm/s' }] })] })
    .length === 0, 'GREEN: a correct claim passes');
  say(judge({ ...base, stages: [wave({ claims: [{ text: 'Wave speed v = f × λ = 12 m/s', expr: 'f*lambda', value: 2, unit: 'm/s' }] })] })
    .some(s => s.includes('U-CLAIM')), 'RED: text printing 12 m/s for value 2 is reported (substring trap)');
  say(judge({ ...base, stages: [wave({ claims: [{ text: 'v = 4 m/s (λ = 2 m)', expr: 'f*lambda', value: 2, unit: 'm/s' }] })] })
    .some(s => s.includes('U-CLAIM')), 'RED: the value elsewhere in the sentence does not excuse a wrong speed');
  say(judge({ ...base, stages: [wave({ copy: 'the wavelength λ = 3 m here' })] })
    .some(s => s.includes('U-VISIBLE')), 'RED: pupil-visible copy contradicting params is reported');
  say(judge({ ...base, stages: [wave({ labels: [{ x: .5, y: .05, text: 'hello' }] })] })
    .some(s => s.includes('banner band')), 'RED: a label parked under the banner is reported');
  say(judge({ ...base, stages: [wave({ spotlight: { x: 120, y: .2, w: .1, h: .1 } })] })
    .some(s => s.includes('U-COORD')), 'RED: a pixel coordinate in a manifest is reported');
  say(judge({ ...base, stages: [wave({}), wave({ title: 'Double the frequency', params: { f: 3, lambda: 2, A: 1 } })] })
    .some(s => s.includes('U-DOUBLE')), 'RED: "double the frequency" with f=3 after f=1 is reported');
  say(judge({ ...base, stages: [wave({}), wave({ title: 'Double the frequency', params: { f: 2, lambda: 1, A: 1 } })] })
    .every(s => !s.includes('U-DOUBLE')), 'GREEN: an exact 2x doubling passes');
  console.log(bad ? '[SELF-TEST] FAIL — ' + bad : '[SELF-TEST] PASS');
  process.exit(bad ? 1 : 0);
} else {
  const files = fs.existsSync(MDIR) ? fs.readdirSync(MDIR).filter(f => f.endsWith('.js')) : [];
  if (!files.length) { console.log('[FAIL] no manifests found under liveteach/manifests/'); process.exit(1); }
  let bad = 0;
  for (const f of files) {
    let m;
    try { m = loadManifest(fs.readFileSync(path.join(MDIR, f), 'utf8')); }
    catch (e) { console.log('[FAIL] ' + f + ': does not evaluate: ' + e.message); bad++; continue; }
    const fails = judge(m);
    fails.forEach(x => console.log('[FAIL] ' + f + ': ' + x));
    bad += fails.length;
    if (!fails.length) console.log('[OK] ' + f + ' — every claim recomputes, every coordinate normalised');
  }
  process.exit(bad ? 1 : 0);
}
