from playwright.sync_api import sync_playwright
import json,time
root='/workspace/sites/dentalum'
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
 page=b.new_page(viewport={'width':1440,'height':1000},device_scale_factor=1);errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 for route,name in [('/','home'),('/behandlingar/basundersokning/','treatment'),('/kliniker/ostergotland/dentalum-atvidaberg/','clinic'),('/team/','team')]:
  page.goto('http://localhost:4173'+route,wait_until='networkidle');page.evaluate("document.querySelectorAll('.js-reveal').forEach(e=>e.classList.add('visible'))");page.wait_for_timeout(700);page.screenshot(path=root+'/audit/'+name+'-desktop.png',full_page=True)
  print(route,'overflow',page.evaluate('document.documentElement.scrollWidth>innerWidth'),'details',page.locator('details').count(),'people',page.locator('.person-card').count(),'booking widgets',page.locator('dm-booking').count(),flush=True)
 page.goto('http://localhost:4173/',wait_until='networkidle');page.locator('.nav-book').click();page.locator('.booking-option').first.click();page.wait_for_timeout(2000);print('booking after click',page.locator('dm-booking').first.evaluate('(e)=>({style:e.getAttribute("style"),html:e.innerHTML.slice(0,400)})') if page.locator('dm-booking').count() else 'no widget');print('errors',errors)
 page.set_viewport_size({'width':390,'height':844});page.goto('http://localhost:4173/',wait_until='networkidle');page.evaluate("document.querySelectorAll('.js-reveal').forEach(e=>e.classList.add('visible'))");page.wait_for_timeout(700);page.screenshot(path=root+'/audit/home-mobile.png',full_page=True)
 b.close()
