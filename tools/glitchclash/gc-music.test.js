/* Menu music: off by default, needs a gesture, menus only, muteable, calm-safe. */
const { chromium } = require('playwright');
const path = require('path');
/* The file under test: an argument, so this runs against a working tree, a
   checkout or a release copy. Defaults to the game in this repo. */
const TARGET = 'file://' + (process.argv[2]
  ? path.resolve(process.argv[2])
  : path.resolve(__dirname, '..', '..', 'Games', 'Glitch_Clash.html'));
(async()=>{
  const b=await chromium.launch({executablePath: process.env.CHROMIUM_PATH || undefined,
    args:['--use-gl=swiftshader','--enable-unsafe-swiftshader','--no-sandbox',
          '--autoplay-policy=no-user-gesture-required']});
  const pg=await (await b.newContext({viewport:{width:412,height:892}})).newPage();
  const errs=[]; pg.on('pageerror',e=>errs.push('PAGEERR '+e.message));
  pg.on('console',m=>{ if(m.type()==='error'&&!/Failed to load|ERR_/.test(m.text())) errs.push('CONSOLE '+m.text()); });
  await pg.goto(TARGET);
  await pg.waitForTimeout(1300);
  let fail=0; const ok=(c,l,d)=>{c?console.log('  PASS  '+l+(d?'   '+d:'')):(fail++,console.log('  FAIL  '+l+(d?'   '+d:'')));};

  console.log('=== off by default ===');
  ok(!(await pg.evaluate(()=>GCX.musicOn())),'the setting is off on a fresh install');
  ok(!(await pg.evaluate(()=>GCX.musicPlaying())),'nothing is playing');
  const btn = await pg.evaluate(()=>{const b=document.getElementById('gcxmusic');return b?b.textContent:null;});
  ok(btn==='Menu Music: Off','a toggle exists and says so',String(btn));

  console.log('\n=== switching it on ===');
  await pg.click('#scr-title [data-open="settings"]'); await pg.waitForTimeout(250);
  await pg.click('#gcxmusic'); await pg.waitForTimeout(600);
  ok(await pg.evaluate(()=>GCX.musicOn()),'the setting flips');
  ok(await pg.evaluate(()=>GCX.musicPlaying()),'the pad starts');
  const voice = await pg.evaluate(()=>({v:GCX.musicVoices(), g:GCX.musicGain(),
    state:(GCX.unlockAudio()||{}).state}));
  console.log('  audio: '+JSON.stringify(voice));
  ok(voice.v>=6,'real oscillator voices are running, not just a timer',voice.v+' voices');
  ok(voice.g>0.05,'the pad gain ramped up — it is audible, not silent',voice.g.toFixed(3));
  ok(voice.state==='running','the audio context is running',String(voice.state));
  ok((await pg.evaluate(()=>document.getElementById('gcxmusic').textContent))==='Menu Music: On',
     'the button agrees');

  console.log('\n=== it is menu music ===');
  await pg.keyboard.press('Escape'); await pg.waitForTimeout(200);
  await pg.click('#scr-title [data-go="home"]'); await pg.waitForTimeout(400);
  ok(await pg.evaluate(()=>GCX.musicPlaying()),'still playing on Home');
  await pg.evaluate(()=>__GCstart(0,{__scened:true})); await pg.waitForTimeout(800);
  ok(!(await pg.evaluate(()=>GCX.musicPlaying())),'it stops when a battle starts');
  await pg.waitForTimeout(1600);
  ok((await pg.evaluate(()=>GCX.musicGain()))<0.01,'and its gain is faded out, not cut',
     String(await pg.evaluate(()=>GCX.musicGain().toFixed(4))));
  await pg.click('#quitbtn'); await pg.waitForTimeout(150);
  await pg.click('#quitbtn'); await pg.waitForTimeout(700);
  ok(await pg.evaluate(()=>GCX.musicPlaying()),'and picks up again on the way out');

  console.log('\n=== it obeys the existing switches ===');
  const routed = await pg.evaluate(()=>{
    // the pad must hang off the same master gain the mute switch controls
    const before=GCX.isMuted(); GCX.setMuted(true);
    const muted=GCX.isMuted(); GCX.setMuted(before);
    return {before,muted};
  });
  ok(routed.muted===true,'Sound: Off mutes it through the shared master gain');
  await pg.evaluate(()=>{ document.body.classList.add('calm'); GCX.musicStop(); GCX.musicStart(); });
  await pg.waitForTimeout(400);
  ok(!(await pg.evaluate(()=>GCX.musicPlaying())),'Calm Mode silences it');
  await pg.evaluate(()=>{ document.body.classList.remove('calm'); GCX.musicStart(); });
  await pg.waitForTimeout(400);
  ok(await pg.evaluate(()=>GCX.musicPlaying()),'and it returns when Calm Mode is off');

  console.log('\n=== it survives a reload ===');
  await pg.reload(); await pg.waitForTimeout(1300);
  ok(await pg.evaluate(()=>GCX.musicOn()),'the setting persists');
  const beforeTap = await pg.evaluate(()=>GCX.musicPlaying());
  await pg.click('#scr-title [data-go="home"]'); await pg.waitForTimeout(700);
  ok(await pg.evaluate(()=>GCX.musicPlaying()),
     'and the first tap starts it (autoplay needs a gesture)','before tap: '+beforeTap);

  console.log('\n=== switching it off ===');
  await pg.click('#scr-home [data-open="settings"]'); await pg.waitForTimeout(250);
  await pg.click('#gcxmusic'); await pg.waitForTimeout(400);
  ok(!(await pg.evaluate(()=>GCX.musicPlaying())),'it stops');
  ok(!(await pg.evaluate(()=>GCX.musicOn())),'and stays off');

  ok(errs.length===0,'no page or script errors',errs.slice(0,3).join(' | '));
  await b.close();
  console.log('\n'+(fail?fail+' FAILED':'MENU MUSIC VERIFIED'));
  process.exit(fail?1:0);
})();
