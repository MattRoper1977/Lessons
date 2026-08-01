/* Prove a change to the decks is visually inert.
 *
 * For every element on every slide of every deck, records the computed values
 * of the properties that decide how it looks, plus its position and size. Run
 * once to snapshot, make the change, run again to compare.
 *
 * This is a stronger oracle than screenshot diffing and, unlike screenshots, it
 * is deterministic: it does not depend on font loading, emoji rasterisation or
 * where a per-slide countdown happens to be when the shutter opens.
 *
 *   node _framework/style_check.js --save    <files...>
 *   node _framework/style_check.js --compare <files...>
 */
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const BASELINE = path.join(__dirname, '.style-baseline.json');
const CHROME = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome';

const PROPS = [
  'display','position','visibility','opacity','color','background-color','background-image',
  'border-top-width','border-right-width','border-bottom-width','border-left-width',
  'border-top-color','border-right-color','border-bottom-color','border-left-color',
  'border-top-style','border-left-style','border-radius',
  'font-size','font-weight','font-style','font-family','line-height','letter-spacing',
  'text-align','text-transform','text-decoration-line','white-space',
  'margin-top','margin-right','margin-bottom','margin-left',
  'padding-top','padding-right','padding-bottom','padding-left',
  'flex-direction','flex-grow','flex-shrink','flex-basis','align-self','align-items',
  'justify-content','gap','grid-template-columns','order',
  'box-shadow','overflow-x','overflow-y','z-index','transform','filter','fill','stroke',
];

(async () => {
  const args = process.argv.slice(2);
  const mode = args.find((a) => a === '--save' || a === '--compare');
  const files = args.filter((a) => !a.startsWith('--'));
  if (!mode || !files.length) {
    console.error('usage: style_check.js --save|--compare <files...>');
    process.exit(2);
  }

  const browser = await chromium.launch({ executablePath: CHROME });
  const snap = {};

  for (const file of files) {
    const page = await browser.newPage({
      viewport: { width: 1440, height: 900 },
      reducedMotion: 'reduce',
    });
    await page.goto('file://' + path.resolve(file));
    await page.waitForTimeout(400);
    const count = await page.evaluate(() => document.querySelectorAll('.slide').length);
    for (let i = 0; i < count; i++) {
      const sig = await page.evaluate(
        ({ j, props }) => {
          currentSlide = j;
          showSlide(j);
          const slide = document.querySelectorAll('.slide')[j];
          const out = [];
          // The countdown's digits change its text width every second; it is
          // deck chrome, not slide content, so it stays out of the signature.
          slide.querySelectorAll('*').forEach((el) => {
            if (el.closest('#auto-timer')) return;
            const cs = getComputedStyle(el);
            const r = el.getBoundingClientRect();
            out.push(
              el.tagName + '|' + (el.className.baseVal ?? el.className) + '|' +
              [r.x, r.y, r.width, r.height].map((n) => Math.round(n)).join(',') + '|' +
              props.map((p) => cs.getPropertyValue(p)).join('|')
            );
          });
          return out.join('\n');
        },
        { j: i, props: PROPS }
      );
      snap[path.basename(file) + '#' + i] = crypto.createHash('sha256').update(sig).digest('hex');
    }
    await page.close();
  }
  await browser.close();

  if (mode === '--save') {
    fs.writeFileSync(BASELINE, JSON.stringify(snap, null, 1));
    console.log(`baseline saved: ${Object.keys(snap).length} slide signatures`);
    return;
  }

  const before = JSON.parse(fs.readFileSync(BASELINE, 'utf8'));
  const keys = Object.keys(snap);
  const diffs = keys.filter((k) => before[k] !== snap[k]);
  console.log(`compared ${keys.length} slide signatures`);
  if (diffs.length) {
    console.log(`FAIL · ${diffs.length} slide(s) resolve to different styles:`);
    diffs.slice(0, 20).forEach((k) => console.log('  · ' + k));
    process.exit(1);
  }
  console.log('PASS · every element resolves to identical styles and geometry');
})();
