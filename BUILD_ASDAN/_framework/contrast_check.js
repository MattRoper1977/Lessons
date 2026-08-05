/* Measure text contrast on every slide of every deck, and write the manifest.
 *
 *   node _framework/contrast_check.js <strand>/[A-Z]*.html
 *   node _framework/contrast_check.js --manifest <strand>/[A-Z]*.html
 *
 * Reports; does not gate. Almost everything it finds is an approved brand
 * colour used as text — a palette decision, and not one this layer gets to
 * make. Its job is to keep that decision measured rather than assumed, and to
 * catch the layer adding a pattern that was not there before.
 *
 * TWO MEASUREMENT CONDITIONS, BOTH LOAD-BEARING
 *
 * 1 · Walk to the slide before measuring. Computed styles on a display:none
 *     subtree do not reflect what will paint, and Chromium never starts an
 *     animation there, so a label held by an animation reads as invisible.
 *     Measuring at load is how a label-timing bug can pass twice.
 *
 * 2 · Sample the background actually painted, not the immediate parent. A
 *     transparent parent over a gradient gives a ratio that is arithmetically
 *     correct and factually wrong. Two passes:
 *       - every element: composite each translucent background-color down the
 *         ancestor chain to the page, and name the nearest ancestor that
 *         actually paints one;
 *       - one representative per pattern: hide the text, screenshot the
 *         element's box, take the modal pixel. That is the real painted
 *         background including gradients, images and overlays, and it is what
 *         the manifest reports where the two disagree.
 */
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const CHROME = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome';
const MANIFEST = path.join(__dirname, '..', 'CONTRAST_MANIFEST.md');

/* Role decides what a failure means. Teaching text a pupil must read to learn
   is a defect; a control is a usability question; chrome that carries nothing
   is neither. Matched most-specific first. */
const ROLES = [
  ['UI', /\b(ilm-replay|v5-step-label|v5-step-controls|timer-|progress-label|controls|level-toggle|at-btn|lm-opt)\b/],
  ['decorative', /\b(country-badge|sow-strip|award-strip|title-dot|wagoll-tag)\b/],
  ['teaching', /\b(li-box|task-box|answer|v5-step|lundy-box|sc-v4|asp-v4|pres-|match-|wagoll-text|ilm-cap|wit-panel|slide-tag|product-card|scaffold-box)\b/],
];
/* A heading or paragraph carrying no class at all is still something a pupil
   reads. Matching on `tag + ' ' + cls` put every one of them in the UI bucket,
   because the trailing space defeated an anchored tag pattern — which quietly
   emptied the set this manifest exists to rule on. Tag and class are tested
   separately now, and the tag test is the fallback rather than a regex race. */
const TEXT_TAGS = /^(h1|h2|h3|h4|h5|p|li|strong|em|b|i|span|div|text|tspan|td|th)$/;

function roleOf(tag, cls) {
  const hay = (tag + ' ' + (cls || '')).trim();
  if (/^(button|input)$/.test(tag)) return 'UI';
  for (const [role, re] of ROLES) if (re.test(hay)) return role;
  if (TEXT_TAGS.test(tag)) return 'teaching';
  return 'UI';
}

(async () => {
  const args = process.argv.slice(2);
  const wantManifest = args.includes('--manifest');
  const files = args.filter((a) => !a.startsWith('--'));
  if (!files.length) {
    console.error('usage: contrast_check.js [--manifest] <files...>');
    process.exit(2);
  }

  const browser = await chromium.launch({ executablePath: CHROME });
  const patterns = new Map();
  let measured = 0;

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
      const rows = await page.evaluate(
        async ({ j }) => {
          // CONDITION 1 — be on the slide, with everything a class would see.
          currentSlide = j;
          showSlide(j);
          const slide = document.querySelectorAll('.slide')[j];
          slide.classList.add('show-ans');
          slide.querySelectorAll('.v5-step-controls button').forEach((b) => {
            for (let k = 0; k < 6; k++) b.click();
          });
          // A freshly created animation sits at currentTime 0 until a real
          // frame ticks, so anything read now reports its from-state.
          await new Promise((r) => setTimeout(r, 90));

          const parse = (c) => {
            const s = c || '';
            const m = s.match(/[\d.]+/g) || [0, 0, 0, 1];
            /* CSS Color 4 -- color(srgb r g b) carries 0..1 channels, not 0..255.
               Chromium serialises every color-mix() result this way, and the ASDAN
               visual-learning layer uses color-mix() throughout, so scraping the
               numbers and assuming 0..255 read a near-white mint as near-black and
               scored real, legible text at 1.42:1. Detected by the prefix, not by
               guessing from magnitude: an rgb() colour may legitimately be 0 0 1. */
            if (/^color\(\s*srgb/i.test(s)) {
              return { r: +m[0] * 255, g: +m[1] * 255, b: +m[2] * 255,
                       a: m[3] === undefined ? 1 : +m[3] };
            }
            return { r: +m[0], g: +m[1], b: +m[2], a: m[3] === undefined ? 1 : +m[3] };
          };
          const lum = (c) => {
            const s = [c.r, c.g, c.b].map((v) => {
              v /= 255;
              return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4);
            });
            return 0.2126 * s[0] + 0.7152 * s[1] + 0.0722 * s[2];
          };
          const over = (fg, bg) => ({
            r: fg.r * fg.a + bg.r * (1 - fg.a),
            g: fg.g * fg.a + bg.g * (1 - fg.a),
            b: fg.b * fg.a + bg.b * (1 - fg.a),
            a: 1,
          });
          const hex = (c) =>
            '#' + [c.r, c.g, c.b].map((v) => Math.round(v).toString(16).padStart(2, '0')).join('');
          const name = (el) =>
            el.tagName.toLowerCase() +
            String(el.className.baseVal ?? el.className)
              .split(' ')
              .filter(Boolean)
              .slice(0, 2)
              .map((c) => '.' + c)
              .join('');

          // CONDITION 2, pass one — composite the chain, name what paints.
          const background = (el) => {
            const stack = [];
            let painter = null;
            let gradient = null;
            for (let cur = el; cur && cur.nodeType === 1; cur = cur.parentElement) {
              const cs = getComputedStyle(cur);
              const c = parse(cs.backgroundColor);
              if (cs.backgroundImage && cs.backgroundImage !== 'none' && !gradient) {
                gradient = name(cur);
              }
              if (c.a > 0) {
                stack.push(c);
                if (!painter) painter = { el: cur, alpha: c.a };
              }
            }
            let acc = { r: 255, g: 255, b: 255, a: 1 };
            for (let k = stack.length - 1; k >= 0; k--) acc = over(stack[k], acc);
            return {
              colour: acc,
              painter: painter ? name(painter.el) + (painter.alpha < 1 ? ' (translucent)' : '') : 'page',
              gradient: gradient,
            };
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
            const box = el.getBoundingClientRect();
            if (!box.width || !box.height) return;

            const bg = background(el);
            const fg = over(parse(cs.color), bg.colour);
            const l1 = lum(fg);
            const l2 = lum(bg.colour);
            const ratio = (Math.max(l1, l2) + 0.05) / (Math.min(l1, l2) + 0.05);
            const size = parseFloat(cs.fontSize);
            const weight = parseInt(cs.fontWeight, 10) || 400;
            // WCAG large text, on the stricter reading: >=24px, or >=19px bold.
            const large = size >= 24 || (size >= 19 && weight >= 700);
            const target = large ? 3 : 4.5;

            out.push({
              sel: name(el),
              tag: el.tagName.toLowerCase(),
              cls: String(el.className.baseVal ?? el.className),
              fg: hex(fg),
              bg: hex(bg.colour),
              painter: bg.painter,
              gradient: bg.gradient,
              ratio: +ratio.toFixed(2),
              target: target,
              size: +size.toFixed(1),
              weight: weight,
              text: own.slice(0, 34),
              slide: slide.getAttribute('data-title'),
              pass: ratio >= target,
            });
          });
          return out;
        },
        { j: i }
      );

      rows.forEach((r) => {
        measured++;
        // Role is decided here rather than in the page, so the table below is
        // the single definition of what counts as teaching text.
        r.role = roleOf(r.tag, r.cls);
        if (r.pass) return;
        // Group by what defines the pattern — the selector and the type it is
        // set in — never by the ratio. Keying on a rounded ratio merges
        // unrelated elements that happen to land on the same number, and the
        // row then reports the first one's text and size for all of them.
        // That produced a row reading "Success looks like ×32 in 25 decks"
        // when only 31 such headings exist in the whole suite. A manifest is
        // ruled from, so a count that cannot be reproduced by pointing at
        // elements is worse than no count.
        const key = [r.sel, r.fg, r.bg, r.size, r.weight, r.target].join('|');
        if (!patterns.has(key)) {
          patterns.set(key, { ...r, decks: new Set(), count: 0, where: file + '#' + i });
        }
        const g = patterns.get(key);
        g.decks.add(path.basename(file));
        g.count++;
      });
    }
    await page.close();
  }

  // CONDITION 2, pass two — the true painted pixel behind one instance of each
  // pattern, which is the only way to be right about a gradient or an overlay.
  if (wantManifest) {
    const byFile = new Map();
    for (const [key, g] of patterns) {
      const [f] = g.where.split('#');
      if (!byFile.has(f)) byFile.set(f, []);
      byFile.get(f).push([key, g]);
    }
    for (const [f, entries] of byFile) {
      const page = await browser.newPage({
        viewport: { width: 1440, height: 900 },
        reducedMotion: 'reduce',
      });
      await page.goto('file://' + path.resolve(f));
      await page.waitForTimeout(150);
      for (const [, g] of entries) {
        const idx = +g.where.split('#')[1];
        const handle = await page.evaluateHandle(
          async ({ j, sel, ratio }) => {
            currentSlide = j;
            showSlide(j);
            const slide = document.querySelectorAll('.slide')[j];
            slide.classList.add('show-ans');
            slide.querySelectorAll('.v5-step-controls button').forEach((b) => {
              for (let k = 0; k < 6; k++) b.click();
            });
            await new Promise((r) => setTimeout(r, 90));
            const name = (el) =>
              el.tagName.toLowerCase() +
              String(el.className.baseVal ?? el.className)
                .split(' ')
                .filter(Boolean)
                .slice(0, 2)
                .map((c) => '.' + c)
                .join('');
            const hit = [...slide.querySelectorAll('*')].find(
              (el) => name(el) === sel && el.getBoundingClientRect().width
            );
            if (hit) {
              // Hide the ink so the shot is background only.
              hit.dataset.atInk = hit.style.color || '';
              hit.style.setProperty('color', 'transparent', 'important');
              hit.querySelectorAll('*').forEach((c) =>
                c.style.setProperty('color', 'transparent', 'important')
              );
            }
            return hit || null;
          },
          { j: idx, sel: g.sel, ratio: g.ratio }
        );
        const el = handle.asElement();
        if (!el) continue;
        let shot = null;
        try {
          shot = await el.screenshot({ type: 'png' });
        } catch (e) {
          /* clipped or zero-area — the composited value stands */
        }
        if (shot) {
          const modal = modalPixel(shot);
          if (modal) {
            g.painted = modal;
            const l1 = relLum(hexToRgb(g.fg));
            const l2 = relLum(hexToRgb(modal));
            g.paintedRatio = +(
              (Math.max(l1, l2) + 0.05) /
              (Math.min(l1, l2) + 0.05)
            ).toFixed(2);
          }
        }
        await page.evaluate(() => {
          document.querySelectorAll('[data-at-ink]').forEach((n) => {
            n.style.removeProperty('color');
            n.querySelectorAll('*').forEach((c) => c.style.removeProperty('color'));
            delete n.dataset.atInk;
          });
        });
      }
      await page.close();
    }
  }

  await browser.close();

  // The painted pixel is the truer measurement, so it decides the verdict —
  // including where it clears a target the composited chain said was missed.
  // Without this a row can sit in the manifest as a failure that the better
  // measurement already cleared, which is the same error as reporting a wrong
  // ratio, just pointing the other way.
  const rows = [...patterns.values()]
    .map((r) => {
      const truth = r.paintedRatio != null ? r.paintedRatio : r.ratio;
      r.truth = truth;
      r.reallyFails = truth < r.target;
      r.verdict = verdictFor(r);
      return r;
    })
    .sort((a, b) => b.count - a.count);
  const cleared = rows.filter((r) => !r.reallyFails);
  const failing = rows.filter((r) => r.reallyFails);
  const failures = failing.reduce((n, r) => n + r.count, 0);
  console.log(`\nmeasured ${measured} text elements across ${files.length} decks`);
  console.log(`${failures} below target, in ${failing.length} distinct patterns`);
  if (cleared.length) {
    console.log(
      `${cleared.length} pattern(s) the composited chain called a failure and the ` +
        `painted pixel clears`
    );
  }
  const byRole = {};
  failing.forEach((r) => {
    byRole[r.role] = (byRole[r.role] || 0) + r.count;
  });
  console.log('failures by role: ' + JSON.stringify(byRole));
  const byVerdict = {};
  failing.forEach((r) => {
    byVerdict[r.verdict] = (byVerdict[r.verdict] || 0) + r.count;
  });
  console.log('failures by verdict: ' + JSON.stringify(byVerdict));

  if (!wantManifest) {
    failing.forEach((r) =>
      console.log(
        `${String(r.count).padStart(5)}x  ${String(r.truth).padStart(5)} / ${r.target}  ` +
          `${r.role.padEnd(11)} ${r.sel.padEnd(28)} "${r.text}"  ${r.verdict}`
      )
    );
    return;
  }

  const row = (r) => {
    const painted = r.painted
      ? `\`${r.painted}\` — painted pixel${r.gradient ? `, over the gradient on \`${r.gradient}\`` : ''}`
      : `\`${r.bg}\` — \`${r.painter}\``;
    const ratio =
      r.paintedRatio != null && r.paintedRatio !== r.ratio
        ? `**${r.paintedRatio}** _(chain said ${r.ratio})_`
        : `**${r.truth}**`;
    return (
      `| \`${r.sel}\` ×${r.count} in ${r.decks.size} decks | ${r.slide} | \`${r.fg}\` | ${painted} | ${ratio} | ` +
      `${r.size} / ${r.weight} | ${r.role} | ${r.target}:1 | ${r.verdict} |`
    );
  };
  const head =
    '| selector | slide | fg | background actually painted (ancestor sampled) | ratio | px / weight | role | target | verdict |\n' +
    '|---|---|---|---|---|---|---|---|---|';

  const out = [];
  out.push('# Contrast manifest — BUILD_ASDAN');
  out.push('');
  out.push('Generated by `_framework/contrast_check.js --manifest`. Re-run it after any');
  out.push('change to the visual layer and compare: **the layer must not add a row.**');
  out.push('');
  out.push('## How this was measured');
  out.push('');
  out.push('Two conditions, both load-bearing:');
  out.push('');
  out.push('1. **Walked to the slide first.** Computed styles on a `display:none` subtree');
  out.push('   do not reflect what paints, and Chromium never starts an animation there, so');
  out.push('   a label held by an animation reads as invisible. Answers are revealed and');
  out.push('   every I Do step is out — the worst case for a reader.');
  out.push('2. **Background actually painted, not the immediate parent.** Every element gets');
  out.push('   its translucent backgrounds composited down the ancestor chain, and the');
  out.push('   nearest ancestor that really paints one is named. Then one instance of each');
  out.push('   pattern has its ink hidden and its box screenshotted, and the modal pixel is');
  out.push('   taken — the real painted background including gradients and overlays. Where');
  out.push('   the two disagree the painted pixel wins and the chain value is shown beside');
  out.push('   it. That difference is not cosmetic: it moves rows across the threshold in');
  out.push('   both directions.');
  out.push('');
  out.push('Large text is the stricter reading: 3:1 only at ≥24px, or ≥19px bold.');
  out.push('');
  out.push('## Headline');
  out.push('');
  out.push(`- **${measured}** text elements measured across ${files.length} decks`);
  out.push(`- **${failures}** below target, in **${failing.length}** distinct patterns`);
  out.push(
    `- by role — teaching **${byRole.teaching || 0}**, UI **${byRole.UI || 0}**, decorative **${byRole.decorative || 0}**`
  );
  Object.entries(byVerdict).forEach(([v, n]) => out.push(`- ${v} — **${n}**`));
  if (cleared.length) {
    out.push(
      `- **${cleared.length}** pattern(s) the composited chain called a failure and the painted pixel clears — listed at the foot`
    );
  }
  out.push('');
  out.push('## The rulings applied');
  out.push('');
  out.push('- **FIX** — pupil-facing text that carries meaning, below target, and fixable by');
  out.push('  moving the ink without touching a pathway, tier or suite identity hue.');
  out.push('- **left — identity hue** — the failing colour *is* the estate\'s colour language');
  out.push('  (a pathway, tier or subject hue). A contrast fix that recolours the language is');
  out.push('  a bigger regression than the thing it fixes. Not a contrast lever.');
  out.push('- **left — UI chrome** — a control, not something a pupil reads to learn.');
  out.push('- **left — decorative** — carries nothing the surrounding text does not.');
  out.push('');
  out.push('## Failing patterns');
  out.push('');
  out.push(head);
  failing.forEach((r) => out.push(row(r)));
  if (cleared.length) {
    out.push('');
    out.push('## Cleared by the painted-pixel measurement');
    out.push('');
    out.push('The composited chain called these failures. Sampling what is actually painted');
    out.push('clears them. They are recorded so nobody re-raises them from a weaker tool.');
    out.push('');
    out.push(head);
    cleared.forEach((r) => out.push(row(r)));
  }
  out.push('');
  fs.writeFileSync(MANIFEST, out.join('\n'));
  console.log(`\nmanifest written to ${MANIFEST}`);
})();

/* The verdict rules, in one place so the manifest and the report cannot drift.
   Identity hues are named explicitly rather than inferred: these are the
   pathway, tier and subject colours that make up the estate's colour language,
   and none of them is a contrast lever. */
const IDENTITY = [
  /slide-tag/, // white on the subject hue — the suite's own strip
  /lundy-box/, // the four boxes take the four subject hues
];
const TIER_IIVK = /^(#22c55e|#f97316|#1e3a8a)$/i; // with support / on your own / take it further

function verdictFor(r) {
  if (!r.reallyFails) return 'passes on the painted measurement';
  if (r.role === 'decorative') return 'left — decorative';
  if (r.role === 'UI') return 'left — UI chrome';
  if (IDENTITY.some((re) => re.test(r.sel))) return 'left — identity hue';
  if (TIER_IIVK.test(r.fg)) return 'left — identity hue';
  // A Lundy heading is a bare <h3>; it is identified by the slide it sits on.
  if (r.slide === 'Lundy Loop') return 'left — identity hue';
  return 'FIX';
}

/* ---- helpers used on the Node side for the painted-pixel pass ---- */
function hexToRgb(h) {
  return {
    r: parseInt(h.slice(1, 3), 16),
    g: parseInt(h.slice(3, 5), 16),
    b: parseInt(h.slice(5, 7), 16),
  };
}
function relLum(c) {
  const s = [c.r, c.g, c.b].map((v) => {
    v /= 255;
    return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4);
  });
  return 0.2126 * s[0] + 0.7152 * s[1] + 0.0722 * s[2];
}
/* Decode a PNG far enough to find its most common pixel. Only the colour
   types Chromium emits for a screenshot are handled; anything else returns
   null and the composited value stands. */
function modalPixel(buf) {
  const zlib = require('zlib');
  let pos = 8;
  let w = 0;
  let h = 0;
  let depth = 0;
  let type = 0;
  const idat = [];
  while (pos < buf.length) {
    const len = buf.readUInt32BE(pos);
    const tag = buf.toString('ascii', pos + 4, pos + 8);
    const data = buf.slice(pos + 8, pos + 8 + len);
    if (tag === 'IHDR') {
      w = data.readUInt32BE(0);
      h = data.readUInt32BE(4);
      depth = data[8];
      type = data[9];
    } else if (tag === 'IDAT') idat.push(data);
    else if (tag === 'IEND') break;
    pos += 12 + len;
  }
  if (depth !== 8 || (type !== 2 && type !== 6) || !w || !h) return null;
  const ch = type === 6 ? 4 : 3;
  let raw;
  try {
    raw = zlib.inflateSync(Buffer.concat(idat));
  } catch (e) {
    return null;
  }
  const stride = w * ch;
  const out = Buffer.alloc(h * stride);
  const paeth = (a, b, c) => {
    const p = a + b - c;
    const pa = Math.abs(p - a);
    const pb = Math.abs(p - b);
    const pc = Math.abs(p - c);
    return pa <= pb && pa <= pc ? a : pb <= pc ? b : c;
  };
  for (let y = 0; y < h; y++) {
    const f = raw[y * (stride + 1)];
    const line = raw.slice(y * (stride + 1) + 1, y * (stride + 1) + 1 + stride);
    for (let x = 0; x < stride; x++) {
      const a = x >= ch ? out[y * stride + x - ch] : 0;
      const b = y > 0 ? out[(y - 1) * stride + x] : 0;
      const c = x >= ch && y > 0 ? out[(y - 1) * stride + x - ch] : 0;
      let v = line[x];
      if (f === 1) v += a;
      else if (f === 2) v += b;
      else if (f === 3) v += (a + b) >> 1;
      else if (f === 4) v += paeth(a, b, c);
      out[y * stride + x] = v & 255;
    }
  }
  const tally = new Map();
  for (let y = 0; y < h; y++) {
    for (let x = 0; x < w; x++) {
      const i = y * stride + x * ch;
      const k = (out[i] << 16) | (out[i + 1] << 8) | out[i + 2];
      tally.set(k, (tally.get(k) || 0) + 1);
    }
  }
  let best = null;
  let n = -1;
  for (const [k, v] of tally) {
    if (v > n) {
      n = v;
      best = k;
    }
  }
  if (best === null) return null;
  return (
    '#' +
    [(best >> 16) & 255, (best >> 8) & 255, best & 255]
      .map((v) => v.toString(16).padStart(2, '0'))
      .join('')
  );
}
