import asyncio,json,threading,functools,http.server,fitz,sys
from pathlib import Path
from playwright.async_api import async_playwright
ROOT=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path(__file__).resolve().parents[2]
OUT=Path(sys.argv[2]).resolve() if len(sys.argv)>2 else Path('grow-arrival-review').resolve()
OUT.mkdir(parents=True,exist_ok=True)
D=json.loads((ROOT/'tools/grow_resources/W3A_ARRIVAL.json').read_text())
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT)))
threading.Thread(target=server.serve_forever,daemon=True).start()
async def main():
 report={'cases':[],'errors':[],'pdfs':[]}
 async with async_playwright() as p:
  b=await p.chromium.launch(headless=True)
  rel='Science_Teesside/Grow/SCI_G_W3_Friction.html'
  for mode,url in [('standalone',(ROOT/rel).as_uri()),('http',f'http://127.0.0.1:{server.server_port}/{rel}')]:
   for width in [320,390,768,1280]:
    ctx=await b.new_context(viewport={'width':width,'height':900},reduced_motion='reduce');page=await ctx.new_page();page.on('pageerror',lambda e:report['errors'].append(str(e)))
    await page.goto(url);await page.evaluate('showSlide(1)');await page.wait_for_timeout(80)
    for route,row in D['routes'].items():
     button=page.locator('[data-arrival-route="'+route+'"]');await button.focus();await page.keyboard.press('Enter')
     grid=page.locator('#arrival-'+route)
     texts=await grid.locator(':scope > .task-box h3').all_text_contents()
     assert texts==[f'{i+1}. {q}' for i,q in enumerate(row['questions'])]
     assert await button.get_attribute('aria-pressed')=='true'
     assert await page.locator('#arrival-slide .grow-arrival-access').inner_text()==D['access']
     assert await grid.locator('details').evaluate('(n)=>n.open')==False
     summary=grid.locator('summary');await summary.focus();await page.keyboard.press('Space')
     assert await grid.locator('details').evaluate('(n)=>n.open')==True
     assert await page.locator('.slide.active').get_attribute('data-title')=='Arrival Task'
     await page.keyboard.press('ArrowRight');assert await page.locator('.slide.active').get_attribute('data-title')=='Arrival Task'
     assert await grid.locator('li').all_text_contents()==row['answers']
     await page.keyboard.press('Space')
     assert not await grid.locator('details').evaluate('(n)=>n.open')
     dimensions=await page.evaluate('''()=>{let n=document.querySelector('#arrival-slide');return {vw:innerWidth,dw:document.documentElement.scrollWidth,cw:n.clientWidth,sw:n.scrollWidth}}''')
     assert dimensions['dw']<=width+1 and dimensions['sw']<=dimensions['cw']+1,dimensions
     # Reach each question and print control through the existing slide scroller.
     for el in await grid.locator(':scope > .task-box, .grow-arrival-actions > button').all():
      await el.scroll_into_view_if_needed();assert await el.is_visible()
     report['cases'].append({'mode':mode,'width':width,'route':route,'questions':4,'keyboard_reveal':True,'no_horizontal_overflow':True})
    await page.evaluate("setArrivalLevel('supported');document.querySelector('#arrival-slide').scrollTop=0")
    await page.screenshot(path=str(OUT/f'{mode}-{width}-arrival.png'))
    if width==1280:
     await page.evaluate('window.print=()=>{}')
     for route,row in D['routes'].items():
      for staff in [False,True]:
       await page.evaluate('([r,a])=>printArrival(r,a)',[route,staff]);await page.emulate_media(media='print')
       sections=await page.locator('.print-section:visible').evaluate_all('(ns)=>ns.map(n=>n.id)')
       assert sections==['print-arrival-answers' if staff else 'print-arrival']
       name=f'{mode}-{route}-'+('staff' if staff else 'pupil')+'.pdf';dest=OUT/name
       await page.pdf(path=str(dest),format='A4',print_background=True,margin={'top':'12mm','bottom':'12mm','left':'12mm','right':'12mm'})
       doc=fitz.open(dest);text=' '.join(' '.join(pg.get_text() for pg in doc).split())
       assert len(doc)==1,(name,len(doc))
       for q in row['questions']:assert ' '.join(q.split()) in text,(name,q)
       for a in row['answers']:assert (' '.join(a.split()) in text)==staff,(name,a)
       report['pdfs'].append({'file':name,'pages':len(doc),'four_questions':True,'answers_only_in_staff':True})
       if mode=='standalone':doc[0].get_pixmap(matrix=fitz.Matrix(1.4,1.4)).save(OUT/name.replace('.pdf','.png'))
       await page.emulate_media(media='screen')
    await ctx.close()
  await b.close()
 assert not report['errors'],report['errors']
 (OUT/'arrival-report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({'cases':len(report['cases']),'one_page_prints':len(report['pdfs']),'runtime_errors':len(report['errors'])}))
try:asyncio.run(main())
finally:server.shutdown()
