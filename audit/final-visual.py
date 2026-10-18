from playwright.sync_api import sync_playwright
from pathlib import Path
r=Path('/workspace/sites/dentalum/audit')
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox']);page=b.new_page(reduced_motion='reduce');
 for route,name,w,theme in [('/','home-desktop-final',1440,'light'),('/','home-mobile-dark',390,'dark'),('/kliniker/ostergotland/dentalum-atvidaberg/','clinic-mobile',390,'light'),('/behandlingar/basundersokning/','treatment-final',1440,'dark'),('/team/','team-final',1440,'light')]:
  page.set_viewport_size({'width':w,'height':900});page.goto('http://localhost:4173'+route);page.evaluate('(t)=>document.documentElement.dataset.theme=t',theme)
  for y in range(0,page.evaluate('document.documentElement.scrollHeight'),700):page.evaluate('(y)=>scrollTo(0,y)',y);page.wait_for_timeout(80)
  page.evaluate('scrollTo(0,0)');page.wait_for_timeout(200);page.screenshot(path=str(r/(name+'.png')),full_page=True)
 page.goto('http://localhost:4173/kliniker/ostergotland/dentalum-atvidaberg/');page.locator('.people-grid img').first.scroll_into_view_if_needed();page.wait_for_timeout(500);print(page.locator('.people-grid img').first.evaluate('(i)=>({src:i.src,w:i.naturalWidth,complete:i.complete,opacity:getComputedStyle(i).opacity})'));page.screenshot(path=str(r/'people-viewport.png'))
 b.close()
