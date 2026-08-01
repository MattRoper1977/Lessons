/* Measure text contrast on every slide of every deck.
 *
 *   node _framework/contrast_check.js <strand>/[A-Z]*.html
 *   node _framework/contrast_check.js --list <strand>/[A-Z]*.html   # each one
 *
 * Walks each slide with its answers revealed and its I Do steps out, works out
 * each text element's effective background by compositing every translucent
 * layer above the page, and reports anything below WCAG AA (4.5:1, or 3:1 for
 * text that counts as large).
 *
 * This reports rather than gates. Almost everything it finds is an approved
 * brand colour used as text — a palette decision, not a layout one — and the
 * README records the ruling on each. Its job is to keep that decision measured
 * rather than assumed, and to catch the layer making anything worse.
 */
const { chromium } = require('playwright');
const path = require('path');

const CHROME = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome';

(async () => {
  const args = process.argv.slice(2);
  const list = args.includes('--list');
  const files = args.filter((a) => !a.startsWith('--'));
  if (!files.length) {
    console.error('usage: contrast_check.js [--list] <files...>');
    process.exit(2);
  }

  const browser = await chromium.launch({ executablePath: CHROME });
  const groups = new Map();
  let elements = 0;

  for (const file of files) {
    const page = await browser.newPage({
      viewport: { width: 1440, height: 900 },
      reducedMotion: 'reduce',
    });
    await page.goto('file://' + path.resolve(file));
    await page.waitForTimeout(150);
    const slides = await page.evaluate(() => document.querySelectorAll('.slide').length);
    if (!slides) {
      await page.close();
      continue;
    }

    for (let i = 0; i < slides; i++) {
      const found = await page.evaluate((j) => {
        currentSlide = j;
        showSlide(j);
        const slide = document.querySelectorAll('.slide')[j];
        // Worst case for the reader: answers up, every step out.
        slide.classList.add('show-ans');
        slide.querySelectorAll('.v5-step-controls button').forEach((b) => {
          for (let k = 0; k < 6; k++) b.click();
        });

        const parse = (c) => {
          const m = c.match(/[\d.]+/g) || [0, 0, 0, 1];
          return { r: +m[0], g: +m[1], b: +m[2], a: m[3] === undefined ? 1 : +m[3] };
        };
        const luminance = (c) => {
          const s = [c.r, c.g, c.b].map((v) => {
            v /= 255;
            return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4);
          });
          return 0.2126 * s[0] + 0.7152 * s[1] + 0.0722 * s[2];
        };
        const composite = (fg, bg) => ({
          r: fg.r * fg.a + bg.r * (1 - fg.a),
          g: fg.g * fg.a + bg.g * (1 - fg.a),
          b: fg.b * fg.a + bg.b * (1 - fg.a),
          a: 1,
        });
        // The page is white; stack every translucent background between the
        // element and the root back down onto it.
        const backgroundOf = (el) => {
          const stack = [];
          for (let cur = el; cur && cur.nodeType === 1; cur = cur.parentElement) {
            const c = parse(getComputedStyle(cur).backgroundColor);
            if (c.a > 0) stack.push(c);
          }
          let acc = { r: 255, g: 255, b: 255, a: 1 };
          for (let k = stack.length - 1; k >= 0; k--) acc = composite(stack[k], acc);
          return acc;
        };

        const out = [];
        slide.querySelectorAll('*').forEach((el) => {
          if (el.closest('#print-area')) return;
          const cs = getComputedStyle(el);
          if (cs.visibility === 'hidden' || cs.display === 'none' || +cs.opacity === 0) return;
          const own = Array.prototype.filter
            .call(el.childNodes, (n) => n.nodeType === 3 && n.textContent.trim())
            .map((n) => n.textContent.trim())
            .join(' ');
          if (!own) return;
          const r = el.getBoundingClientRect();
          if (!r.width || !r.height) return;

          const bg = backgroundOf(el);
          const fg = composite(parse(cs.color), bg);
          const l1 = luminance(fg);
          const l2 = luminance(bg);
          const ratio = (Math.max(l1, l2) + 0.05) / (Math.min(l1, l2) + 0.05);
          const size = parseFloat(cs.fontSize);
          const weight = parseInt(cs.fontWeight, 10) || 400;
          const large = size >= 24 || (size >= 18.66 && weight >= 700);
          const need = large ? 3 : 4.5;
          out.push({
            pass: ratio >= need,
            ratio: +ratio.toFixed(2),
            need: need,
            size: +size.toFixed(1),
            sel:
              el.tagName.toLowerCase() +
              String(el.className.baseVal ?? el.className)
                .split(' ')
                .filter(Boolean)
                .slice(0, 2)
                .map((c) => '.' + c)
                .join(''),
            text: own.slice(0, 30),
          });
        });
        return out;
      }, i);

      found.forEach((f) => {
        elements++;
        if (f.pass) return;
        const key = f.sel + '|' + f.ratio + '|' + f.need;
        if (!groups.has(key)) groups.set(key, { ...f, decks: new Set(), count: 0 });
        const g = groups.get(key);
        g.decks.add(path.basename(file));
        g.count++;
        if (list) console.log(`${path.basename(file)}#${i}  ${f.ratio}  ${f.sel}  "${f.text}"`);
      });
    }
    await page.close();
  }
  await browser.close();

  const rows = [...groups.values()].sort((a, b) => b.count - a.count);
  const failing = rows.reduce((n, r) => n + r.count, 0);
  console.log(`\nmeasured ${elements} text elements across ${files.length} decks`);
  console.log(`${failing} below WCAG AA, in ${rows.length} distinct patterns:\n`);
  rows.forEach((r) => {
    console.log(
      `${String(r.count).padStart(5)}x  ${String(r.ratio).padStart(5)} (needs ${r.need})  ` +
        `${r.sel.padEnd(30)} ${String(r.size).padStart(5)}px  "${r.text}"  [${r.decks.size} decks]`
    );
  });
})();
