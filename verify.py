import json,sys,re,collections
from pathlib import Path
sys.path.insert(0,'/workspace/pylibs')
from bs4 import BeautifulSoup
from urllib.parse import urlparse,unquote
from playwright.sync_api import sync_playwright
root=Path('/workspace/sites/dentalum');dist=root/'dist';routes=['/'+str(p.relative_to(dist).parent).replace('\\','/').replace('.','').strip('/')+'/' for p in dist.rglob('index.html')];routes=list(dict.fromkeys('/' if r=='//' else r for r in routes));report={'routes':len(routes),'broken_links':[],'broken_assets':[],'broken_fragments':[],'browser':[],'errors':[],'interactions':{}}
for f in dist.rglob('index.html'):
 s=BeautifulSoup(f.read_text(),'html.parser')
 for a in s.select('a[href]'):
  h=a['href'];p=urlparse(h)
  if p.scheme or p.netloc:continue
  if h.startswith('#'):
   if h[1:] and not s.find(id=h[1:]):report['broken_fragments'].append([str(f.relative_to(dist)),h])
  elif h.startswith('/'):
   target=dist/unquote(p.path).strip('/')
   if not target.exists() and not (target/'index.html').exists():report['broken_links'].append([str(f.relative_to(dist)),h])
 for img in s.select('img[src]'):
  if img['src'].startswith('/') and not (dist/img['src'].lstrip('/')).exists():report['broken_assets'].append(img['src'])
print('Static check', {k:len(v) for k,v in report.items() if isinstance(v,list)},flush=True)
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox']);page=b.new_page(viewport={'width':1440,'height':1000},reduced_motion='reduce')
 page.on('pageerror',lambda e:report['errors'].append(str(e)))
 for ix,r in enumerate(routes):
  page.goto('http://localhost:4173'+r,wait_until='load');page.evaluate('document.querySelectorAll("img[loading]").forEach(e=>e.loading="eager")');page.evaluate('''async()=>{await Promise.race([Promise.all([...document.querySelectorAll('img[src]')].map(i=>i.complete?Promise.resolve():new Promise(r=>{i.onload=r;i.onerror=r}))),new Promise(r=>setTimeout(r,1500))])}''')
  info=page.evaluate('''()=>({title:document.title,h1:document.querySelectorAll('main h1').length,overflow:document.documentElement.scrollWidth>innerWidth,images:[...document.querySelectorAll('img[src]')].filter(i=>i.complete&&!i.naturalWidth).map(i=>i.src),light:document.documentElement.dataset.theme})''')
  page.set_viewport_size({'width':390,'height':844});info['mobileOverflow']=page.evaluate('document.documentElement.scrollWidth>innerWidth');page.locator('.theme-toggle').click();info['dark']=page.evaluate('document.documentElement.dataset.theme');info['darkOverflow']=page.evaluate('document.documentElement.scrollWidth>innerWidth');page.locator('.theme-toggle').click();page.set_viewport_size({'width':1440,'height':1000});report['browser'].append({'route':r,**info})
  if ix%30==0:print('Checked',ix+1,'/',len(routes),flush=True)
 # Exercise each shared control family, including empty and reset states.
 page.goto('http://localhost:4173/vara-kliniker/');page.locator('#clinic-search').fill('Stockholm');report['interactions']['clinic_search']=page.locator('.finder .clinic-card:visible').count();page.locator('#clinic-search').fill('zzzzzz');report['interactions']['clinic_empty']=page.locator('#clinic-empty').is_visible();page.locator('#reset-clinics').click();report['interactions']['clinic_reset']=page.locator('.finder .clinic-card:visible').count();page.locator('#region-filter').select_option('skane');report['interactions']['region_filter']=page.locator('.finder .clinic-card:visible').count()
 page.goto('http://localhost:4173/behandlingar/basundersokning/');page.locator('summary').first.click();report['interactions']['faq_open']=page.locator('details[open]').count();page.locator('#expand-details').click();report['interactions']['faq_expand_all']=page.locator('details[open]').count();page.locator('#expand-details').click();report['interactions']['faq_collapse_all']=page.locator('details[open]').count()
 page.goto('http://localhost:4173/team/');page.locator('#team-search').fill('Marianne');report['interactions']['team_search']=page.locator('.person-card:visible').count();page.locator('#team-search').fill('zzzz');report['interactions']['team_empty']=page.locator('#team-count').text_content();page.locator('#team-search').fill('');page.locator('.source-content img').first.focus();page.keyboard.press('Enter');report['interactions']['gallery_open']=page.locator('#lightbox').evaluate('(d)=>d.open');page.locator('#next-image').click();report['interactions']['gallery_next']=page.locator('#gallery-count').text_content();page.keyboard.press('Escape')
 page.goto('http://localhost:4173/behandlingar/');page.locator('#go-treatment').click();report['interactions']['treatment_empty']=page.locator('#treatment-error').text_content();page.locator('#treatment-select').select_option('/behandlingar/tandimplantat/');page.locator('#go-treatment').click();page.wait_for_url('**/behandlingar/tandimplantat/');report['interactions']['treatment_navigation']=page.url.endswith('/behandlingar/tandimplantat/')
 page.set_viewport_size({'width':390,'height':844});page.locator('.mobile-toggle').click();report['interactions']['mobile_open']=page.locator('#mobile-nav').is_visible();page.keyboard.press('Escape');report['interactions']['mobile_escape']=not page.locator('#mobile-nav').is_visible();page.locator('.nav-book').click();report['interactions']['booking_open']=page.locator('#booking').evaluate('(d)=>d.open');report['interactions']['booking_links']=page.locator('.booking-option').count();page.keyboard.press('Escape');report['interactions']['booking_escape']=not page.locator('#booking').evaluate('(d)=>d.open')
 page.locator('.theme-toggle').click();page.reload();report['interactions']['theme_persisted']=page.evaluate('document.documentElement.dataset.theme');report['interactions']['reduced_motion']=page.evaluate('getComputedStyle(document.querySelector(".hero-copy")).animationName')
 for route,name,width,theme in [('/','home-mobile-dark',390,'dark'),('/','home-desktop-final',1440,'light'),('/kliniker/ostergotland/dentalum-atvidaberg/','clinic-mobile',390,'light'),('/behandlingar/basundersokning/','treatment-final',1440,'dark'),('/team/','team-final',1440,'light')]:
  page.set_viewport_size({'width':width,'height':900});page.goto('http://localhost:4173'+route);page.evaluate('(t)=>document.documentElement.dataset.theme=t',theme);page.evaluate('document.querySelectorAll("img[loading]").forEach(e=>e.loading="eager")');page.wait_for_timeout(400);page.screenshot(path=str(root/'audit'/f'{name}.png'),full_page=True)
 b.close()
json.dump(report,open(root/'audit/verification.json','w'),ensure_ascii=False,indent=2);print('FINISHED',json.dumps(report['interactions'],ensure_ascii=False));print('ISSUES',[(r['route'],r['overflow'],r['mobileOverflow'],r['h1'],r['images']) for r in report['browser'] if r['overflow'] or r['mobileOverflow'] or r['h1']!=1 or r['images']]);print('errors',report['errors'])
