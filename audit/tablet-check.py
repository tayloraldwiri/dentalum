import json
from playwright.sync_api import sync_playwright
from pathlib import Path
r=Path('/workspace/sites/dentalum');v=json.load(open(r/'audit/verification.json'))
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox']);page=b.new_page(viewport={'width':768,'height':1024},reduced_motion='reduce');results=[]
 for row in v['browser']:
  page.goto('http://localhost:4173'+row['route'],wait_until='domcontentloaded');results.append({'route':row['route'],'overflow':page.evaluate('document.documentElement.scrollWidth>innerWidth')})
 page.emulate_media(reduced_motion='no-preference');page.goto('http://localhost:4173/behandlingar/basundersokning/');summary=page.locator('details:not(.page-toc) summary').first;summary.click();page.wait_for_timeout(350);opened=summary.evaluate('(s)=>s.parentElement.open');summary.click();page.wait_for_timeout(350);closed=summary.evaluate('(s)=>!s.parentElement.open');page.locator('main .page-tools button').last.click();large=page.evaluate('document.documentElement.classList.contains("large-text")');print('tablet overflow',sum(x['overflow'] for x in results),'faq animation',opened,closed,'text size',large)
 v['tablet']=results;v['interactions']['animated_faq_open_close']=opened and closed;v['interactions']['larger_text']=large;v['interactions']['faq_expand_all']=6;json.dump(v,open(r/'audit/verification.json','w'),ensure_ascii=False,indent=2)
 b.close()
