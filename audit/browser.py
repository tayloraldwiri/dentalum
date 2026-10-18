from playwright.sync_api import sync_playwright
import json
root='/workspace/sites/dentalum'
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
 page=browser.new_page(viewport={'width':1440,'height':1000},device_scale_factor=1)
 page.goto('http://localhost:4173/',wait_until='networkidle');page.screenshot(path=root+'/audit/home-desktop.png',full_page=True)
 print('title',page.title(),'overflow',page.evaluate('document.documentElement.scrollWidth>innerWidth'))
 page.goto('http://localhost:4173/behandlingar/basundersokning/',wait_until='networkidle');page.screenshot(path=root+'/audit/treatment-desktop.png',full_page=True)
 page.goto('http://localhost:4173/kliniker/ostergotland/dentalum-atvidaberg/',wait_until='networkidle');page.screenshot(path=root+'/audit/clinic-desktop.png',full_page=True)
 print('clinic people',page.locator('.person-card').count(),'details',page.locator('details').count())
 browser.close()
