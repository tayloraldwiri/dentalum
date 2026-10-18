from playwright.sync_api import sync_playwright
import os,json
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'],proxy={'server':os.environ['HTTPS_PROXY'],'bypass':'localhost,127.0.0.1'})
 page=b.new_page();errs=[];page.on('console',lambda m:errs.append(m.text) if m.type=='error' else None);page.on('pageerror',lambda e:errs.append(str(e)))
 page.goto('http://localhost:4173/',wait_until='networkidle');page.wait_for_timeout(4000);print('widgets',page.locator('dm-booking').count(),'errors',errs[:10])
 page.locator('.nav-book').click();page.locator('.booking-option').first.click();page.wait_for_timeout(2500);print('widgets after',page.locator('dm-booking').count());page.screenshot(path='/workspace/sites/dentalum/audit/booking-check.png',full_page=False);b.close()
