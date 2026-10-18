import sys,os,json,re,hashlib,concurrent.futures
sys.path.insert(0,'/workspace/pylibs')
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin,urlparse
base='https://dentalum.com'; root='/workspace/sites/dentalum'; seen={}; queue={base+'/',base+'/sitemap_index.xml',base+'/wp-sitemap.xml',base+'/robots.txt'}
def fetch(u):
 try:
  r=requests.get(u,timeout=40);return u,r.status_code,r.url,r.text
 except Exception as e:return u,0,u,str(e)
while queue:
 batch=sorted(queue-set(seen));queue=set()
 if not batch:break
 with concurrent.futures.ThreadPoolExecutor(max_workers=10) as ex:
  for u,status,final,html in ex.map(fetch,batch):
   seen[u]={'status':status,'final':final}; fn=hashlib.sha256(u.encode()).hexdigest()[:16]+'.html';open(root+'/audit/'+fn,'w').write(html);seen[u]['file']=fn
   if status!=200:continue
   s=BeautifulSoup(html,'html.parser')
   links=[a.get('href') for a in s.select('a[href]')]+[x.get_text() for x in s.select('loc')]
   if u.endswith('robots.txt'):links+=re.findall(r'Sitemap:\s*(\S+)',html)
   for l in links:
    v=urljoin(final,l).split('#')[0].split('?')[0];p=urlparse(v)
    if p.netloc in ['dentalum.com','www.dentalum.com'] and not re.search(r'\.(pdf|jpg|png|svg|webp|jpeg|zip|mp4)$',p.path,re.I) and '/wp-json' not in v and v not in seen:queue.add(v)
 print('Crawled',len(seen),'pending',len(queue),flush=True)
json.dump(seen,open(root+'/audit/crawl.json','w'),ensure_ascii=False,indent=2)
