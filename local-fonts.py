import sys,re,hashlib
sys.path.insert(0,'/workspace/pylibs')
import requests
from pathlib import Path
r=Path('/workspace/sites/dentalum/dist');p=r/'style.css';s=p.read_text();imp=re.search(r"@import url\('([^']+)'\);",s)
if imp:
 css=requests.get(imp[1],headers={'User-Agent':'Mozilla/5.0'},timeout=30).text
 for u in set(re.findall(r'url\((https[^)]+)\)',css)):
  data=requests.get(u,timeout=30);data.raise_for_status();name='font-'+hashlib.sha256(u.encode()).hexdigest()[:12]+'.woff2';(r/'assets'/name).write_bytes(data.content);css=css.replace(u,'/assets/'+name)
 s=s.replace(imp[0],css);p.write_text(s);print('Fonts localized')
