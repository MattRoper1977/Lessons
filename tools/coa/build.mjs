/* Class of Ashes: Zero Period PRO v1.0.0 — release/ -> staging/.
 *
 * Same discipline as tools/fieldops and tools/vcl: named exact-string swaps,
 * each must match exactly once or throw; drop them all and the builder returns
 * release byte for byte.
 *
 * C0 SCOPE FENCE. This game is NOT being placed. Nothing here creates a route,
 * a card, a manifest entry, a genre, a hue, a take or a link into it, and the
 * gate set asserts that the shelf is byte-identical before and after.
 *
 * PROVENANCE, which belongs in the PR: the prototype at v0.1.0 has 0
 * localStorage calls, 0 normalizers and 0 __COA_QA. Every defect fixed below
 * was introduced by the PRO release's own "Reliability and hardening" work.
 *
 * Usage: node build.mjs [--drop=Y1,Y3 ...] [--out=staging]
 */
import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.env.COA_ROOT || path.dirname(new URL(import.meta.url).pathname);
const DROP = new Set((process.argv.find(a => a.startsWith('--drop=')) || '').replace('--drop=', '').split(',').filter(Boolean));
const OUT = (process.argv.find(a => a.startsWith('--out=')) || '--out=staging').slice(6);
const FILE = 'Class_of_Ashes_Zero_Period_PRO.html';

let src = fs.readFileSync(path.join(ROOT, 'release', FILE), 'utf8');
const applied = [];
function swap(id, from, to) {
  if (DROP.has(id)) { applied.push(`${id} DROPPED`); return; }
  const n = src.split(from).length - 1;
  if (n !== 1) throw new Error(`${id}: expected exactly 1 occurrence, found ${n}\n  ${from.slice(0, 140)}`);
  src = src.replace(from, to);
  applied.push(id);
}

/* =====================================================================
 * C1 — the null-parse boot kill.  The only correctness defect.
 *
 * Storing the literal string "null" under either the settings or the profile
 * key kills boot: safeParse returns JSON.parse('null') === null, which is not
 * undefined, so the raw={} DEFAULT PARAMETER never fires and the first property
 * read throws. activeRun is unaffected — the scope is exactly two keys.
 *
 * The guard goes INSIDE both normalizers, not at the call sites, so every
 * future caller inherits it. Guard on SHAPE, not on undefined: that is the
 * whole lesson of the defect.
 *
 * Their own qa/TEST_SUMMARY.json shows why they reported a pass — the injected
 * settings were {"difficulty":"nightmare","aimAssist":"500",...}, a well-formed
 * OBJECT with bad VALUES. The top-level TYPE was never varied.
 * ===================================================================== */
swap('Y1a',
  `function normalizeSettings(raw={}){const out=Object.assign({},defaultSettings)`,
  `function normalizeSettings(raw={}){if(!raw||typeof raw!=='object'||Array.isArray(raw))raw={};const out=Object.assign({},defaultSettings)`);
swap('Y1b',
  `function normalizeProfile(raw={}){const out=freshProfile()`,
  `function normalizeProfile(raw={}){if(!raw||typeof raw!=='object'||Array.isArray(raw))raw={};const out=freshProfile()`);

/* =====================================================================
 * C3 — the ungated QA hook.
 *
 * window.__COA_QA ships live with grant, setPlayer, hurt, teleport, spawn,
 * strike, forceWave, forceBoss, setStats and save. Anyone with a console
 * rewrites the run AND the persistent Academic Transcript, which is a
 * pupil-visible record of grades, best wave and commendation seals.
 *
 * Scrap Core v10 removed its hooks outright. This matches that: the whole
 * assignment goes. The cost is that the gate set must drive the game through
 * the DOM and real input events, which it does.
 * ===================================================================== */
{
  const start = src.indexOf('window.__COA_QA=');
  if (!DROP.has('Y3')) {
    if (start < 0) throw new Error('Y3: window.__COA_QA= not found');
    /* the assignment ends at the newline that begins the next statement */
    const nl = src.indexOf('\n', start);
    if (nl < 0) throw new Error('Y3: could not find the end of the __COA_QA assignment');
    const removed = src.slice(start, nl + 1);
    if (removed.includes('const qs=new URLSearchParams')) throw new Error('Y3: the slice swallowed the next statement');
    src = src.slice(0, start) + src.slice(nl + 1);
    applied.push(`Y3 (removed ${removed.length} chars)`);
  } else applied.push('Y3 DROPPED');
}

/* =====================================================================
 * C2 — unvalidated URL parameters.
 *
 * ?autostart=1&overclock=bogus threw at boot: qs.get() values went straight
 * into startRun with no check against MODES / CLASSES / OVERCLOCKS. The
 * hardening was asymmetric — localStorage defended, URL input trusted — and
 * the prototype does not have this at all.
 *
 * Repair (1), the order's preferred one: the block exists only to serve the QA
 * harness that C3 removes, so it goes with it. Nothing else reads autostart.
 * ===================================================================== */
swap('Y2',
  `const qs=new URLSearchParams(location.search);if(qs.get('autostart')==='1'){pending={mode:qs.get('mode')||'operation',classId:qs.get('class')||'prefect',overclock:qs.get('overclock')||'field',seed:qs.get('seed')||'QA-AUTOSTART'};startRun(pending.mode,pending.classId,pending.overclock)}\n`,
  ``);

/* =====================================================================
 * C4 — subtitle / HUD collision at short landscape heights.
 *
 * #subtitles sits at bottom:134px, dropping to bottom:82px under
 * @media(max-height:560px). The drawn HUD's bottom-left vitals panel occupies
 * vh+16 from the bottom, and vh is 106 in compact mode (CW<980). At 915x412
 * the page is compact AND short, so the subtitle panel lands at 82px inside a
 * 122px band — on top of the ammo/heat/scrap readout.
 *
 * The clearance is DERIVED from the same expression the draw path uses, not
 * guessed: whatever vh is, the subtitles clear it.
 * ===================================================================== */
swap('Y4a',
  `#subtitles{position:fixed;z-index:10;left:50%;bottom:134px;`,
  `#subtitles{position:fixed;z-index:10;left:50%;bottom:var(--hud-bottom,134px);`);
swap('Y4b',
  `max-height:560px){#subtitles{bottom:82px}.panel{max-height:96vh}`,
  `max-height:560px){.panel{max-height:96vh}`);
swap('Y4c',
  ` const vh=compact?106:118,vw=compact?330:430,vy=CH-vh-16;`,
  ` const vh=compact?106:118,vw=compact?330:430,vy=CH-vh-16;setSubtitleClearance(vh+16);`);
swap('Y4d',
  `function drawHUD(){`,
  `/* The subtitle band is positioned from the HUD panel actually drawn, so the
   two cannot drift apart. Written only when the value changes. */
let _subClearance=-1;
function setSubtitleClearance(px){const v=Math.round(px)+12;if(v===_subClearance)return;_subClearance=v;try{document.documentElement.style.setProperty('--hud-bottom',v+'px')}catch(e){}}
function drawHUD(){`);

/* =====================================================================
 * C5.4 — the viewport.  v10 stripped exactly these two.
 * ===================================================================== */
swap('Y5d',
  `<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no,viewport-fit=cover">`,
  `<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">`);

/* =====================================================================
 * C5.5 — reduced motion.  [PORT v10]
 *
 * The in-JS reducedMotion setting is real and gates six things, but it defaults
 * false and never reads the OS. Seeded the way v10 seeds
 * SYSTEM_PREFERS_REDUCED_MOTION, with an explicit user choice still winning:
 * the seed only applies where the stored settings do not carry a boolean.
 * ===================================================================== */
swap('Y5e1',
  `const defaultSettings={difficulty:'standard',aimAssist:46,screenShake:72,master:78,music:42,sfx:82,subtitles:true,damageNumbers:true,highContrast:false,largeHud:false,reducedMotion:false,reducedFlashes:false,activeWindow:'standard',autoAimTouch:true};`,
  `const SYSTEM_PREFERS_REDUCED_MOTION=(()=>{try{return !!(window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches)}catch(e){return false}})();
const defaultSettings={difficulty:'standard',aimAssist:46,screenShake:72,master:78,music:42,sfx:82,subtitles:true,damageNumbers:true,highContrast:false,largeHud:false,reducedMotion:SYSTEM_PREFERS_REDUCED_MOTION,reducedFlashes:SYSTEM_PREFERS_REDUCED_MOTION,activeWindow:'standard',autoAimTouch:true};`);

fs.mkdirSync(path.join(ROOT, OUT), { recursive: true });
fs.writeFileSync(path.join(ROOT, OUT, FILE), src);
console.log(`built ${path.join(ROOT, OUT, FILE)}`);
for (const a of applied) console.log('  ' + a);
