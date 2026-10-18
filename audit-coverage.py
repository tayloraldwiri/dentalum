import sys,json,re,warnings
sys.path.insert(0,'/workspace/pylibs')
from bs4 import BeautifulSoup
from pathlib import Path
warnings.filterwarnings('ignore');root=Path('/workspace/sites/dentalum'); inv=json.load(open(root/'audit/page-inventory.json'));assets=json.load(open(root/'audit/assets.json'));crawl=json.load(open(root/'audit/crawl.json'));report=[]
for row in inv:
 src=BeautifulSoup((root/'audit'/crawl[row['source']]['file']).read_text(),'html.parser');src=src.select_one('#content')
 out=BeautifulSoup((root/'dist'/row['path'].strip('/')/'index.html').read_text(),'html.parser');text=out.get_text(' ',strip=True)
 images=set()
 for img in src.select('img'):
  u=img.get('data-src') or img.get('src','')
  if u.startswith('http'):images.add(u)
 for x in src.select('[style]'):
  images.update(re.findall(r'url\([\'\"]?(https?[^)\'\"]+)',x.get('style','')))
 missing=[u for u in images if assets.get(u,{}).get('local',u) not in str(out)]
 headings=[h.get_text(' ',strip=True) for h in src.select('h1,h2,h3,h4') if h.get_text(' ',strip=True) not in text]
 if missing or headings:report.append({'path':row['path'],'missing_images':missing,'missing_headings':headings})
json.dump(report,open(root/'audit/coverage-gaps.json','w'),ensure_ascii=False,indent=2)
print('Pages with gaps',len(report));print(json.dumps(report,ensure_ascii=False)[:14000])
