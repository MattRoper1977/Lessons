"""Targeted W3A organiser/exit verification, not full pilot or publication acceptance."""
import asyncio, json, threading, functools, http.server, sys, os
from pathlib import Path
import fitz
from playwright.async_api import async_playwright

ROOT=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path(__file__).resolve().parents[2]
OUT=Path(sys.argv[2]).resolve() if len(sys.argv)>2 else Path('grow-organiser-exit-review').resolve()
OUT.mkdir(parents=True,exist_ok=True)
D=json.loads((ROOT/'tools/grow_resources/W3A_ORGANISER_EXIT.json').read_text())
AXE=Path(os.environ['NODE_PATH'])/'axe-core/axe.min.js'
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT)))
threading.Thread(target=server.serve_forever,daemon=True).start()
async def main():
 report={'scope':'New W3A organiser and exit only; headless Chromium, standalone and local HTTP. Full pilot, published copy and human AT remain untested.','organiser':[],'exit':[],'prints':[],'axe':[],'errors':[]}
 async with async_playwright() as p:
  b=await p.chromium.launch(headless=True)
  try:
   rel='Science_Teesside/Grow/SCI_G_W3_Friction.html'
   for mode,url in [('standalone',(ROOT/rel).as_uri()),('http',f'http://127.0.0.1:{server.server_port}/{rel}')]:
    for width in [320,390,768,1280]:
     ctx=await b.new_context(viewport={'width':width,'height':900},reduced_motion='reduce',accept_downloads=True)
     page=await ctx.new_page();page.set_default_timeout(5000)
     page.on('pageerror',lambda e:report['errors'].append(str(e)))
     await page.goto(url);await page.add_script_tag(path=str(AXE))
     assert await page.locator('.slide').evaluate_all('(ns)=>ns.map(n=>Number(n.dataset.timer))')==[1,4,2,9,10,4,10,32,4,4]
     for stage in range(7):
      await page.evaluate('(i)=>showSlide(i)',stage);await page.wait_for_timeout(60)
      button=page.locator('.slide.active .grow-ko-access button');await button.focus();await page.keyboard.press('Enter')
      dialog=page.locator('#grow-ko-dialog');assert await dialog.evaluate('(n)=>n.open')
      assert await page.evaluate('document.activeElement.id')=='grow-ko-heading'
      assert await dialog.evaluate('(n)=>n.scrollTop')==0
      title=await page.locator('.slide.active').get_attribute('data-title')
      for key in ['Space','ArrowRight','ArrowDown']:
       await page.keyboard.press(key);assert await page.locator('.slide.active').get_attribute('data-title')==title
      # The native top layer keeps the existing chassis controls inert to focus.
      await page.locator('button[onclick="nextSlide()"]').evaluate('(n)=>n.focus()')
      assert await page.evaluate("document.activeElement.closest('#grow-ko-dialog')!==null")
      for _ in range(5):
       await page.keyboard.press('Tab')
       assert await page.evaluate("document.activeElement===document.body || document.activeElement.closest('#grow-ko-dialog')!==null")
      dims=await dialog.evaluate('(n)=>({cw:n.clientWidth,sw:n.scrollWidth,left:n.getBoundingClientRect().left,right:n.getBoundingClientRect().right})')
      assert dims['sw']<=dims['cw']+1 and dims['left']>=0 and dims['right']<=width+1,dims
      await dialog.evaluate('(n)=>n.scrollTop=n.scrollHeight')
      await page.keyboard.press('Escape');await page.wait_for_timeout(30)
      assert not await dialog.evaluate('(n)=>n.open')
      assert await button.evaluate('(n)=>n===document.activeElement')
      await page.keyboard.press('Enter');assert await dialog.evaluate('(n)=>n.scrollTop')==0
      await page.get_by_role('button',name='Close organiser',exact=True).click();await page.wait_for_timeout(30)
      assert await button.evaluate('(n)=>n===document.activeElement')
      report['organiser'].append({'mode':mode,'width':width,'stage':title,'focus_scroll_return_native_keys':True,'no_horizontal_overflow':True})
     await page.evaluate('showSlide(6)')
     summary=page.locator('#grow-w3a-exit > summary');await summary.focus();await page.keyboard.press('Space')
     assert await page.locator('#grow-w3a-exit').evaluate('(n)=>n.open')
     assert await page.locator('.slide.active').get_attribute('data-title')=='We Do 2'
     for route,row in D['routes'].items():
      button=page.locator('[data-grow-exit-route="'+route+'"]');await button.focus();await page.keyboard.press('Enter')
      pane=page.locator('#grow-exit-'+route)
      assert await button.get_attribute('aria-pressed')=='true'
      assert await pane.locator('legend').all_text_contents()==[f'{i+1}. {q}' for i,q in enumerate(row['questions'])]
      assert await pane.locator('fieldset').count()==2
      assert not await pane.locator('details').evaluate('(n)=>n.open')
      if route=='supported':
       radio=pane.locator('input').first;await radio.focus();await page.keyboard.press('Space');assert await radio.is_checked()
       await page.keyboard.press('ArrowRight');assert await pane.locator('input').nth(1).is_checked()
       assert await page.locator('.slide.active').get_attribute('data-title')=='We Do 2'
       await pane.locator('input').nth(2).check()
       expected=['Right','Yes']
      else:
       entry=pane.locator('textarea').first;await entry.fill('My own response');await entry.focus();await page.keyboard.press('End');await page.keyboard.press('Space');await page.keyboard.press('ArrowRight');await page.keyboard.press('ArrowDown')
       assert await page.locator('.slide.active').get_attribute('data-title')=='We Do 2'
       expected=['My own response','[No response recorded]']
      async with page.expect_download() as info:
       await pane.get_by_role('button',name=f'Save {row["label"]} responses',exact=True).click()
      download=await info.value;path=OUT/f'{mode}-{width}-{route}-responses.txt';await download.save_as(path)
      saved=path.read_text();assert 'no automatic mark' in saved
      for answer in expected:assert answer in saved
      for answer in row['answers']:assert answer not in saved
      await pane.locator('summary').focus();await page.keyboard.press('Space');assert await pane.locator('details').evaluate('(n)=>n.open')
      assert await pane.locator('li').all_text_contents()==row['answers']
      assert await page.locator('.slide.active').get_attribute('data-title')=='We Do 2'
      dims=await page.locator('#grow-w3a-exit').evaluate('(n)=>({cw:n.clientWidth,sw:n.scrollWidth,left:n.getBoundingClientRect().left,right:n.getBoundingClientRect().right,dw:document.documentElement.scrollWidth})')
      assert dims['sw']<=dims['cw']+1 and dims['left']>=0 and dims['right']<=width+1 and dims['dw']<=width+1,dims
      await pane.locator('summary').focus();await page.keyboard.press('Space')
      violations=await page.evaluate("async()=> (await axe.run(document.querySelector('#grow-w3a-exit'))).violations.map(v=>({id:v.id,impact:v.impact,nodes:v.nodes.map(n=>n.target)}))")
      report['axe'].append({'mode':mode,'width':width,'scope':'exit-'+route,'violations':violations})
      assert not [v for v in violations if v['impact'] in ['serious','critical']],violations
      report['exit'].append({'mode':mode,'width':width,'route':route,'questions':2,'native_keys_grouping_download_reveal':True,'no_horizontal_overflow':True})
     await page.evaluate("setGrowExit('supported')")
     assert await page.locator('#grow-exit-supported input').nth(1).is_checked()
     await page.locator('#grow-w3a-exit').scroll_into_view_if_needed()
     await page.screenshot(path=str(OUT/f'{mode}-{width}-exit.png'))
     await page.locator('.slide.active .grow-ko-access button').click()
     violations=await page.evaluate("async()=> (await axe.run(document.querySelector('#grow-ko-dialog'))).violations.map(v=>({id:v.id,impact:v.impact,nodes:v.nodes.map(n=>n.target)}))")
     report['axe'].append({'mode':mode,'width':width,'scope':'organiser','violations':violations})
     assert not [v for v in violations if v['impact'] in ['serious','critical']],violations
     await page.screenshot(path=str(OUT/f'{mode}-{width}-organiser.png'))
     if width==1280:
      await page.evaluate('window.print=()=>{}')
      for choice,route in [('print-ko','supported')]+[('print-w3a-exit',k) for k in D['routes']]+[('print-w3a-exit-answers','supported')]:
       if choice=='print-ko':await page.get_by_role('button',name='Print organiser',exact=True).click()
       else:
        await page.evaluate('document.getElementById("grow-ko-dialog").close()')
        await page.evaluate('([id,r])=>printGrowSheet(id,r)',[choice,route])
       await page.emulate_media(media='print')
       sections=await page.locator('.print-section:visible').evaluate_all('(ns)=>ns.map(n=>n.id)');assert sections==[choice],sections
       name=f'{mode}-{choice}-{route}.pdf';dest=OUT/name
       await page.pdf(path=str(dest),format='A4',print_background=True,margin={'top':'12mm','bottom':'12mm','left':'12mm','right':'12mm'})
       doc=fitz.open(dest);text=' '.join(' '.join(pg.get_text() for pg in doc).split())
       assert len(doc)==1,(name,len(doc))
       if choice=='print-w3a-exit':
        for q in D['routes'][route]['questions']:assert text.count(' '.join(q.split()))==2,(name,q)
        for row in D['routes'].values():
         for answer in row['answers']:assert ' '.join(answer.split()) not in text
        assert 'answers' not in text.lower()
       elif choice=='print-ko':
        for fact in D['facts']:assert ' '.join(fact.split()) in text
       else:
        for row in D['routes'].values():
         for answer in row['answers']:assert ' '.join(answer.split()) in text,(name,answer)
       report['prints'].append({'mode':mode,'file':name,'pages':1,'content_verified':True,'from_open_dialog':choice=='print-ko'})
       if mode=='standalone':doc[0].get_pixmap(matrix=fitz.Matrix(1.4,1.4)).save(dest.with_suffix('.png'))
       await page.emulate_media(media='screen')
     await ctx.close()
   assert not report['errors'],report['errors']
   report['result']='PASS'
  except Exception as error:
   report['result']='FAIL';report['failure']=str(error);raise
  finally:
   (OUT/'organiser-exit-report.json').write_text(json.dumps(report,indent=2)+'\n');await b.close()
 print(json.dumps({k:len(report[k]) for k in ['organiser','exit','prints','axe','errors']}))
try:asyncio.run(main())
finally:server.shutdown()
