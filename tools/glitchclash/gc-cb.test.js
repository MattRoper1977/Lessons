/* Colourblind palette: applies, persists, redraws, and never becomes the only cue. */
const { chromium } = require('playwright');
const path = require('path');
/* The file under test: an argument, so this runs against a working tree, a
   checkout or a release copy. Defaults to the game in this repo. */
const TARGET = 'file://' + (process.argv[2]
  ? path.resolve(process.argv[2])
  : path.resolve(__dirname, '..', '..', 'Games', 'Glitch_Clash.html'));
(async()=>{
  const b=await chromium.launch({executablePath: process.env.CHROMIUM_PATH || undefined,
    args:['--use-gl=swiftshader','--enable-unsafe-swiftshader','--no-sandbox']});
  const ctx=await b.newContext({viewport:{width:412,height:892}});
  const pg=await ctx.newPage();
  const errs=[]; pg.on('pageerror',e=>errs.push('PAGEERR '+e.message));
  pg.on('console',m=>{ if(m.type()==='error'&&!/Failed to load|ERR_/.test(m.text())) errs.push('CONSOLE '+m.text()); });
  await pg.goto(TARGET);
  await pg.waitForTimeout(1300);
  let fail=0; const ok=(c,l,d)=>{c?console.log('  PASS  '+l+(d?'   '+d:'')):(fail++,console.log('  FAIL  '+l+(d?'   '+d:'')));};

  await pg.click('#scr-title [data-go="home"]'); await pg.waitForTimeout(300);
  console.log('=== toggle ===');
  await pg.click('#scr-home [data-open="settings"]'); await pg.waitForTimeout(250);
  const label0 = await pg.evaluate(()=>document.getElementById('cbtoggle').textContent);
  ok(/Off$/.test(label0),'starts off',label0);
  await pg.click('#cbtoggle'); await pg.waitForTimeout(250);
  const on = await pg.evaluate(()=>({
    label: document.getElementById('cbtoggle').textContent,
    cls: document.body.classList.contains('cb'),
    ring: document.documentElement.style.getPropertyValue('--ring'),
    emm:  document.documentElement.style.getPropertyValue('--emm'),
    star: document.documentElement.style.getPropertyValue('--star'),
    bast: document.documentElement.style.getPropertyValue('--bastion') }));
  ok(/On$/.test(on.label),'toggles on',on.label);
  ok(on.cls,'body carries the cb class');
  ok(on.ring==='#EE4687'&&on.emm==='#09FDFA'&&on.star==='#D6F438'&&on.bast==='#C656EA',
     'all four identity colours are repainted',[on.ring,on.emm,on.star,on.bast].join(' '));

  console.log('\n=== it survives a reload ===');
  await pg.reload(); await pg.waitForTimeout(1300);
  const after = await pg.evaluate(()=>({
    cls: document.body.classList.contains('cb'),
    ring: document.documentElement.style.getPropertyValue('--ring'),
    label: document.getElementById('cbtoggle').textContent }));
  ok(after.cls&&after.ring==='#EE4687','the setting is restored at boot',after.ring);
  ok(/On$/.test(after.label),'the button agrees',after.label);

  console.log('\n=== the SVG glyphs follow, not just the CSS ===');
  await pg.click('#scr-title [data-go="home"]'); await pg.waitForTimeout(250);
  await pg.click('[data-go="team"]'); await pg.waitForTimeout(500);
  const glyphs = await pg.evaluate(()=>{
    const svgs=[...document.querySelectorAll('#collection .glyph, #teamslots .glyph')];
    const cols=new Set();
    svgs.forEach(s=>s.querySelectorAll('[stroke],[fill]').forEach(n=>{
      const v=n.getAttribute('stroke')||n.getAttribute('fill');
      if(v&&v!=='none') cols.add(v.toUpperCase()); }));
    return [...cols];
  });
  const cbSet=['#EE4687','#09FDFA','#D6F438','#C656EA'];
  const shipped=['#F27EA9','#5EEAD4','#FFD166','#7FB4FF'];
  ok(glyphs.some(c=>cbSet.includes(c)),'card glyphs are drawn in the colourblind palette',glyphs.join(' '));
  ok(!glyphs.some(c=>shipped.includes(c)),'no glyph is still using a shipped hex',
     glyphs.filter(c=>shipped.includes(c)).join(' ')||'none');

  console.log('\n=== colour is never the only cue ===');
  const cues = await pg.evaluate(()=>{
    const subs=[...document.querySelectorAll('#collection .m-sub')].map(e=>e.textContent);
    return { n:subs.length, named: subs.filter(t=>/Ring|Star|Bastion|\bM\b/.test(t)).length };
  });
  ok(cues.n>0 && cues.named===cues.n,'every card still states its shape in words',
     cues.named+'/'+cues.n);

  console.log('\n=== turning it off restores the shipped look ===');
  await pg.click("#scr-team [data-go=\"home\"]"); await pg.waitForTimeout(300);
  await pg.click('#scr-home [data-open="settings"]'); await pg.waitForTimeout(250);
  await pg.click('#cbtoggle'); await pg.waitForTimeout(300);
  const off = await pg.evaluate(()=>({
    cls: document.body.classList.contains('cb'),
    ring: document.documentElement.style.getPropertyValue('--ring') }));
  ok(!off.cls && off.ring==='','the override is cleared, not overwritten','"'+off.ring+'"');

  ok(errs.length===0,'no page or script errors',errs.slice(0,3).join(' | '));
  await b.close();
  console.log('\n'+(fail?fail+' FAILED':'COLOURBLIND PALETTE VERIFIED'));
  process.exit(fail?1:0);
})();
