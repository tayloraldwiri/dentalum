import sys,os,re,json,hashlib,concurrent.futures
sys.path.insert(0,'/workspace/pylibs')
import requests
from bs4 import BeautifulSoup
from pathlib import Path
from urllib.parse import urlparse,urljoin
root=Path('/workspace/sites/dentalum');assets=set()
for f in (root/'audit').glob('*.html'):
 s=BeautifulSoup(f.read_text(),'html.parser');m=s
 for i in m.select('img'):
  u=i.get('data-src') or i.get('src','')
  if u.startswith('http'):assets.add(u)
 for el in m.select('[style]'):
  for u in re.findall(r'url\([\'\"]?(https?[^)\'\"]+)',el.get('style','')):assets.add(u)
 for a in s.select('a[href]'):
  u=urljoin('https://dentalum.com',a['href'])
  if '/wp-content/uploads/' in u and u.endswith('.pdf'):assets.add(u)
assets.add('https://dentalum.com/wp-content/uploads/2025/10/dentalum_horizontal_logo_4.svg')
os.makedirs(root/'dist/assets',exist_ok=True)
manifest=json.load(open(root/'audit/assets.json')) if (root/'audit/assets.json').exists() else {}
def get(u):
 ext=Path(urlparse(u).path).suffix or '.bin';name=hashlib.sha256(u.encode()).hexdigest()[:14]+ext;dest=root/'dist/assets'/name
 if dest.exists():return u,{'local':'/assets/'+name,'status':200,'bytes':dest.stat().st_size}
 try:
  r=requests.get(u,timeout=30)
  if r.status_code==200:dest.write_bytes(r.content)
  return u,{'local':'/assets/'+name if r.status_code==200 else u,'status':r.status_code,'bytes':len(r.content)}
 except Exception as e:return u,{'local':u,'status':0,'error':str(e)}
with concurrent.futures.ThreadPoolExecutor(max_workers=12) as ex:
 for u,data in ex.map(get,assets):manifest[u]=data
json.dump(manifest,open(root/'audit/assets.json','w'),ensure_ascii=False,indent=2)
print('Assets',len(manifest),'failed',sum(x['status']!=200 for x in manifest.values()))
