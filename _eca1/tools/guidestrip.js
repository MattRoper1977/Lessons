#!/usr/bin/env node
// ECA-1 PART B reversibility instrument: remove exactly what guidepatch.js added.
// PH-3's install (data-mbm-guide="1" + its blocks) is BASE state on the 85 ASDAN/D&T
// decks and is left untouched there. Usage: guidestrip.js file...  (writes in place)
const fs = require('fs');

for (const f of process.argv.slice(2)) {
  let s = fs.readFileSync(f, 'utf8');
  // 1. Unwrap ECA-1 counter-wraps (role-valued, never "1"): <span data-mbm-guide="staff">X</span>
  // Loop until stable — repairs any accidental nesting too.
  let prev;
  do { prev = s; s = s.replace(/<span data-mbm-guide="(?:staff|route|lundy)">((?:(?!<\/?span)[\s\S])*?)<\/span>/g, '$1'); } while (s !== prev);
  // 2. Remove ECA-1 role attributes (PH-3's ="1" stays).
  s = s.replace(/ data-mbm-guide="(?:staff|route|lundy)"/g, '');
  // 3. Remove injected blocks ONLY where PH-3's install is absent (no ="1" tags = ECA-1 installed it).
  if (!s.includes('data-mbm-guide="1"')) {
    s = s.replace(/<style id="mbm-guide-css">[\s\S]*?<\/style>/, '');
    s = s.replace(/<button class="mbm-guide-btn"[^>]*>[^<]*<\/button>/, '');
    s = s.replace(/<!--mbm-guide:v1--><script id="mbm-guide-js">[\s\S]*?<\/script>\n?/, '');
  }
  fs.writeFileSync(f, s);
  console.log('stripped', f);
}
