"""Paired Friction feedback checkpoint; not full pilot, AT or publication acceptance."""
import asyncio,json,threading,functools,http.server,sys,os
from pathlib import Path
import fitz
from playwright.async_api import async_playwright
ROOT=Path(sys.argv[1]).resolve();OUT=Path(sys.argv[2]).resolve();OUT.mkdir(parents=True,exist_ok=True)
D=json.loads((ROOT/'tools/grow_resources/W3_FEEDBACK.json').read_text())
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT)))
threading.Thread(target=server.serve_forever,daemon=True).start()
async def main():
 report={'scope':'Feedback changes only, standalone/local HTTP, default theme and reduced motion; no live, full pilot or human AT claim.','prompts':[],'staff':[],'navigation':[],'axe':[],'prints':[],'pack_selection':[],'errors':[]}
 async with async_playwright() as p:
  browser=await p.chromium.launch(headless=True)
  try:
   rel='Science_Teesside/Grow/SCI_G_W3_Friction.html'
   for mode,url in [('standalone',(ROOT/rel).as_uri()),('http',f'http://127.0.0.1:{server.server_port}/{rel}')]:
    for width in [320,390,768,1280]:
     ctx=await browser.new_context(viewport={'width':width,'height':900},reduced_motion='reduce');page=await ctx.new_page();page.set_default_timeout(5000)
     page.on('pageerror',lambda e:report['errors'].append(str(e)))
     await page.goto(url);await page.add_script_tag(path=str(Path(os.environ['NODE_PATH'])/'axe-core/axe.min.js'))
     assert await page.locator('.slide').count()==10
     assert await page.locator('.slide').evaluate_all('(ns)=>ns.map(n=>Number(n.dataset.timer))')==[1,4,2,9,10,4,10,32,4,4]
     assert await page.locator('.grow-help-prompt').count()==2
     assert await page.locator('[data-title="Lundy Loop"],#print-lundy,.lundy-grid').count()==0
     for which,index in [('a',6),('b',8)]:
      await page.evaluate('(i)=>showSlide(i)',index);await page.wait_for_timeout(50)
      title=await page.locator('.slide.active').get_attribute('data-title')
      prompt=page.locator('#grow-help-'+which);assert not await prompt.evaluate('(n)=>n.open')
      assert await prompt.locator('input,textarea,select,button').count()==0
      await prompt.locator('summary').focus();await page.keyboard.press('Space')
      assert await prompt.evaluate('(n)=>n.open')
      assert await prompt.locator('p').inner_text()==D['prompt_'+which]
      for key in ['ArrowRight','ArrowDown']:
       await page.keyboard.press(key);assert await page.locator('.slide.active').get_attribute('data-title')==title
      await prompt.scroll_into_view_if_needed()
      dims=await prompt.evaluate('(n)=>({cw:n.clientWidth,sw:n.scrollWidth,l:n.getBoundingClientRect().left,r:n.getBoundingClientRect().right,dw:document.documentElement.scrollWidth})')
      assert dims['sw']<=dims['cw']+1 and dims['l']>=0 and dims['r']<=width+1 and dims['dw']<=width+1,dims
      scope='#grow-help-a' if which=='a' else '#grow-review-evidence'
      violations=await page.evaluate('async(s)=>(await axe.run(document.querySelector(s))).violations.map(v=>({id:v.id,impact:v.impact,nodes:v.nodes.map(n=>n.target)}))',scope)
      report['axe'].append({'mode':mode,'width':width,'scope':scope,'violations':violations});assert not [v for v in violations if v['impact'] in ['serious','critical']],violations
      await page.screenshot(path=str(OUT/f'{mode}-{width}-help-{which}.png'))
      await prompt.locator('summary').focus();await page.keyboard.press('Space');assert not await prompt.evaluate('(n)=>n.open')
      report['prompts'].append({'mode':mode,'width':width,'lesson':which,'native_keyboard':True,'no_response_field':True,'horizontal_fit':True})
     assert await page.locator('#grow-review-evidence > ol > li').all_text_contents()==D['review_steps']
     await page.locator('button[onclick="nextSlide()"]').focus();await page.keyboard.press('Enter');assert await page.locator('.slide.active').get_attribute('data-title')=='Exit Ticket'
     assert await page.locator('.slide.active h2').evaluate('(n)=>n===document.activeElement')
     await page.locator('button[onclick="prevSlide()"]').focus();await page.keyboard.press('Enter');assert await page.locator('.slide.active').get_attribute('data-title')=='Review the evidence'
     assert await page.locator('.slide.active h2').evaluate('(n)=>n===document.activeElement')
     await page.evaluate('showSlide(0)');await page.get_by_role('button',name='Resume Lesson B',exact=False).focus();await page.keyboard.press('Enter');assert await page.locator('.slide.active').get_attribute('data-title')=='Independent Work'
     report['navigation'].append({'mode':mode,'width':width,'ten_stages_same_timers':True,'review_exit_heading_focus':True,'resume_lesson_b':True})
     await page.evaluate('showSlide(0)');staff=page.locator('#grow-feedback-staff');await staff.locator('summary').focus();await page.keyboard.press('Space');assert await staff.evaluate('(n)=>n.open')
     assert await staff.locator('h3').all_text_contents()==[x[0] for x in D['staff_sections']]
     await staff.get_by_role('button',name='Print staff feedback guidance',exact=True).scroll_into_view_if_needed()
     dims=await staff.evaluate('(n)=>({cw:n.clientWidth,sw:n.scrollWidth})');assert dims['sw']<=dims['cw']+1,dims
     await page.keyboard.press('ArrowRight');assert await page.locator('.slide.active').get_attribute('data-title')=='Title'
     report['staff'].append({'mode':mode,'width':width,'optional_disclosure':True,'reachable_print':True,'horizontal_fit':True})
     if width==1280:
      await page.evaluate('window.print=()=>{}')
      for route in ['supported','standard','stretch']:
       await page.evaluate('(r)=>printPack(r)',route)
       ids=await page.locator('.print-section.visible').evaluate_all('(ns)=>ns.map(n=>n.id)')
       assert all(x not in ids for x in ['print-teacher-feedback','print-feedback','print-witness','print-w3a-exit-answers','print-arrival-answers'])
       assert all(x in ids for x in ['print-w3a-exit','print-review-evidence','print-exit'])
       report['pack_selection'].append({'mode':mode,'route':route,'selected':ids,'staff_records_and_keys_excluded':True})
      for kind in ['teacher-feedback','review-evidence']:
       if kind=='teacher-feedback':await staff.get_by_role('button',name='Print staff feedback guidance',exact=True).click()
       else:await page.evaluate("printSection('review-evidence','standard')")
       await page.emulate_media(media='print');assert await page.locator('.print-section:visible').evaluate_all('(ns)=>ns.map(n=>n.id)')==['print-'+kind]
       dest=OUT/f'{mode}-{kind}.pdf';await page.pdf(path=str(dest),format='A4',print_background=True,margin={'top':'12mm','bottom':'12mm','left':'12mm','right':'12mm'})
       doc=fitz.open(dest);assert len(doc)==1,(kind,len(doc));text=' '.join(doc[0].get_text().split())
       for t in ([x[1] for x in D['staff_sections']] if kind=='teacher-feedback' else D['review_steps']):assert ' '.join(t.split()) in text
       assert 'writing it is what closes it' not in text
       if mode=='standalone':doc[0].get_pixmap(matrix=fitz.Matrix(1.4,1.4)).save(dest.with_suffix('.png'))
       report['prints'].append({'mode':mode,'kind':kind,'pages':1,'content_verified':True});await page.emulate_media(media='screen')
     await ctx.close()
   assert not report['errors'];report['result']='PASS'
  except Exception as exc:report['result']='FAIL';report['failure']=str(exc);raise
  finally:(OUT/'feedback-report.json').write_text(json.dumps(report,indent=2)+'\n');await browser.close()
 print(json.dumps({k:len(report[k]) for k in ['prompts','staff','navigation','axe','prints','pack_selection','errors']}))
try:asyncio.run(main())
finally:server.shutdown()
