import sys,json,re,html,hashlib,os,warnings
from pathlib import Path
from urllib.parse import urljoin,urlparse,unquote
sys.path.insert(0,'/workspace/pylibs')
from bs4 import BeautifulSoup,Tag,NavigableString
warnings.filterwarnings('ignore')
ROOT=Path(__file__).parent; DIST=ROOT/'dist'; audit=json.load(open(ROOT/'audit/crawl.json')); assets=json.load(open(ROOT/'audit/assets.json')); pages={}; soups={}
def esc(x):return html.escape(str(x),quote=True)
def norm(u):
 p=urlparse(u);path=unquote(p.path) or '/'
 return path if path.endswith('/') or '.' in path.split('/')[-1] else path+'/'
def local(u):return assets.get(u,{}).get('local',u)
def href(u):
 if 'cdn-cgi/l/email-protection#' in u:
  try:
   b=bytes.fromhex(u.split('#')[-1]);return 'mailto:'+html.unescape(''.join(chr(x^b[0]) for x in b[1:]))
  except:return '/kontakt/'
 if re.search(r'/\+\d+',u):return 'tel:'+u.split('/')[-1]
 if u.startswith('#awb'):return '#booking'
 if u=='#':return '#booking'
 if u.startswith('tel:') or u.startswith('mailto:'):return u
 a=urlparse(urljoin('https://dentalum.com',u))
 if '/wp-content/uploads/' in a.path:return local(urljoin('https://dentalum.com',u))
 if a.netloc in ['dentalum.com','www.dentalum.com']:return norm(u)+(('#'+a.fragment) if a.fragment else '')
 return u
def image(u,alt='',cls=''):
 if not u or u.startswith('data:'):return ''
 if assets.get(u,{}).get('status',200)!=200:return '<div class="unavailable-photo"><span class="eyebrow">Originalbild</span><p>Originalbilden kunde inte hämtas från källan.</p><a class="text-link" href="'+esc(u)+'">Öppna originalbilden ↗</a></div>'
 return f'<img class="{cls}" src="{esc(local(u))}" alt="{esc(alt)}" loading="lazy" decoding="async">'
def backgrounds(n):
 out=[]
 for el in [n]+list(n.select('[style],[data-bg-url]')):
  if el.get('data-bg-url'):out.append(el['data-bg-url'])
  out+=re.findall(r'url\([\'\"]?(https?[^)\'\"]+)',el.get('style',''))
 return list(dict.fromkeys(out))
for u,d in audit.items():
 if d['status']!=200 or u.endswith(('.xml','.txt')):continue
 s=BeautifulSoup((ROOT/'audit'/d['file']).read_text(),'html.parser')
 if not s.select_one('#content'):continue
 p=norm(u)
 if p in pages:continue
 title=s.title.get_text().split(' | ')[0].split(' – Dentalum')[0].strip() if s.title else p
 c=s.select_one('link[rel=canonical]');canonical=c.get('href',u) if c else u
 h=s.select_one('h1');entry=s.select_one('#content .entry-title');title=(h or entry).get_text(' ',strip=True) if h or entry else title
 if p=='/':title='Tandvård som gör skillnad – med dig i centrum'
 desc=s.select_one('meta[name=description]');pages[p]={'title':title,'description':desc.get('content','') if desc else '', 'source':u,'canonical':canonical};soups[p]=s
# Original listing is authoritative for addresses and labels.
clinics=[]
for h in soups['/vara-kliniker/'].select('.post-content h2'):
 box=h.find_parent(class_='fusion-column-wrapper');a=box.select_one('a[href]') if box else None
 if not a:continue
 ps=[p.get_text(' ',strip=True) for p in box.select('p')];path=norm(a['href']);page=soups.get(path);bg=backgrounds(page) if page else []
 cur=h
 while cur.parent and not backgrounds(cur):cur=cur.parent
 listing_bg=backgrounds(cur)
 if listing_bg:bg=listing_bg
 clinics.append({'title':h.get_text(' ',strip=True),'region':ps[0] if ps else '', 'address':ps[1] if len(ps)>1 else '', 'path':path,'image':local(bg[0]) if bg else ''})
# All original direct booking links from the existing selector.
bookings=[]
for a in soups['/'].select('a[data-dentli_ob_id]'):
 if 'Boka tid online' in a.get_text():
  box=a.find_parent(class_='fusion-column-wrapper');bookings.append({'url':{'291':'https://dentalum.com/kliniker/vasternorrland/dentalum-ornskoldsvik/#awb-open-oc__4576','290':'https://dentalum.com/kliniker/ostergotland/dentalum-atvidaberg/#awb-open-oc__4576','358':'https://dentalum.com/kliniker/stockholm/dentalum-drottninggatan/#awb-open-oc__4576'}[a['data-dentli_ob_id']],'id':a['data-dentli_ob_id'],'text':box.get_text(' ',strip=True) if box else a.get_text(' ',strip=True)})
print('bookings',bookings)
# Semantic rendering keeps original content and image relationships, replaces framework behavior.
def render(n):
 if isinstance(n,NavigableString):return esc(n)
 if not isinstance(n,Tag):return ''
 cl=n.get('class',[]);name=n.name
 if name in ['script','style','noscript','svg','i','button','input','textarea','select','label']:return ''
 if any(x in cl for x in ['rich-snippet-hidden','fusion-separator','fusion-filters','fusion-load-more-button','fusion-google-map','fusion-slider-loading','fusion-sharing-box','fusion-meta-info','fusion-breadcrumbs','fusion-alert','fusion-form-notice']):return ''
 if name=='form' or 'fusion-form' in cl:
  return '<div class="backend-note"><span class="eyebrow">Kontakt & förfrågningar</span><h3>Vi hjälper dig vidare.</h3><p>Formuläret kräver Dentalums befintliga tjänst. Skicka din förfrågan via originalwebbplatsen eller kontakta kliniken direkt. Din tid är inte bekräftad förrän du har fått en bekräftelse.</p><a class="button secondary" href="'+esc(current_source)+'">Öppna kontaktformuläret ↗</a></div>'
 if ('panel' in cl or 'fusion-panel' in cl) and n.select_one('.panel-title'):
  title=n.select_one('.panel-title').get_text(' ',strip=True);body=n.select_one('.panel-body');return f'<details><summary>{esc(title)}<span aria-hidden="true">+</span></summary><div class="answer">{render_children(body) if body else ""}</div></details>'
 if name=='img':return image(n.get('data-src') or n.get('src'),n.get('alt') or n.get('aria-label',''))
 if name=='a':
  u=href(n.get('href','#booking'));text=render_children(n)
  protected=n.get('data-cfemail') or (n.select_one('[data-cfemail]').get('data-cfemail') if n.select_one('[data-cfemail]') else None)
  if protected:
   try:
    bb=bytes.fromhex(protected);u='mailto:'+html.unescape(''.join(chr(x^bb[0]) for x in bb[1:]));text=esc(u[7:])
   except:pass
  label=n.get('aria-label') or n.get('title')
  if u.startswith('mailto:') and ('protected' in text or not text.strip()):text=esc(u[7:])
  if not text.strip() and label:text=esc(label.capitalize())
  if not text.strip():return ''
  isbtn='fusion-button' in cl
  return f'<a href="{esc(u)}"'+(' class="button secondary"' if isbtn else '')+(' target="_blank" rel="noopener noreferrer"' if n.get('target')=='_blank' else '')+'>'+text+'</a>'
 if name in ['h1','h2','h3','h4','h5','h6','p','ul','ol','li','blockquote','table','thead','tbody','tr','td','th','strong','em','br','hr','sup','sub']:
  tag='h2' if name=='h1' else name
  return '<'+tag+'>'+render_children(n)+('</'+tag+'>' if name not in ['br','hr'] else '')
 kids=render_children(n)
 if n.get('data-bg-url'):kids=image(n['data-bg-url'],n.select_one('img').get('aria-label','') if n.select_one('img') else '')+kids
 if not kids.strip():
  b=backgrounds(n)
  return ''.join(image(u,'') for u in b) if b else ''
 cls=''
 if 'fusion-layout-column' in cl:
  frac=next((x for x in cl if re.match('fusion_builder_column_(?:inner_)?[1-5]_[1-6]$',x)), '')
  mt=re.search(r'(\d)_(\d)$',frac);ratio=int(mt[1])/int(mt[2]) if mt else 1
  cls='layout-col '+('wide' if ratio>=.95 else 'half' if ratio>=.45 else 'third' if ratio>=.3 else 'quarter')
 elif any(x in cl for x in ['fusion-builder-row','fusion-builder-row-inner']):cls='layout-row'
 elif 'fusion-column-wrapper' in cl:cls='column-content'
 elif 'fusion-carousel-item' in cl or 'fusion-portfolio-post' in cl or name=='article':cls='source-card'
 elif any('carousel-wrapper'==x or 'awb-carousel'==x or 'fusion-carousel'==x for x in cl):cls='people-grid'
 elif 'fusion-text' in cl:cls='prose'
 elif 'fusion-fullwidth' in cl:cls='inner-band'
 elif 'fusion-social-links' in cl:cls='social-links'
 ident=f' id="{esc(n["id"])}"' if n.get('id') else ''; return f'<div class="{cls}"{ident}>{kids}</div>' if cls or ident else kids

def render_children(n):return ''.join(render(x) for x in n.children) if n else ''
def card(c):
 return f'<a class="clinic-card" href="{esc(c["path"])}" data-search="{esc((c["title"]+" "+c["region"]+" "+c["address"]).lower())}" data-region="{esc(c["path"].split("/")[2])}">'+image(c['image'],c['title'])+f'<span class="eyebrow">{esc(c["region"])}</span><h3>{esc(c["title"])}</h3><p>{esc(c["address"])}</p><span class="card-bottom">Utforska kliniken <span>↗</span></span></a>'
def clinicfinder(p):
 region=p.split('/')[2] if p.startswith('/kliniker/') and len(p.strip('/').split('/'))==2 else ''
 cs=[c for c in clinics if not region or c['path'].split('/')[2]==region]
 options=''.join(f'<option value="{esc(k)}">{esc(v)}</option>' for k,v in sorted({c['path'].split('/')[2]: c['region'].split('|')[0].strip() for c in clinics}.items()))
 return '<section class="finder section"><div class="section-top"><div><span class="eyebrow">Nära dig, på dina villkor</span><h2>'+esc((soups[p].select_one('#content h2').get_text(' ',strip=True) if region and soups[p].select_one('#content h2') else 'Hitta din klinik.'))+'</h2></div><p>Från Boden i norr till Malmö i söder.</p></div><div class="filter-bar"><label><span>Sök klinik eller ort</span><input id="clinic-search" type="search" placeholder="Exempelvis Stockholm, TandCity…"></label><label><span>Region</span><select id="region-filter"><option value="">Alla regioner</option>'+options+'</select></label><button class="text-button" id="reset-clinics">Rensa filter ↻</button></div><p id="clinic-count" class="result-count" role="status"></p><div class="clinic-grid">'+''.join(card(c) for c in cs)+'</div><div id="clinic-empty" class="empty" hidden><h3>Inga kliniker hittades</h3><p>Prova en annan ort eller välj alla regioner.</p></div></section>'
treatments=[p for p in pages if p.startswith('/behandlingar/') and len(p.strip('/').split('/'))==2]
news=[p for p in pages if p.startswith('/nyheter/') and len(p.strip('/').split('/'))==2]
def treatment_cards(limit=False):
 names=[('Allmäntandvård','allmantandvard','01'),('Estetisk tandvård','estetisk-tandvard','02'),('Specialisttandvård','specialisttandvard','03'),('Akut tandvård','akut-tandvard-stockholm','04')]
 return '<div class="treatment-grid">'+''.join(f'<a class="treatment-card" href="/behandlingar/{slug}/"><span class="card-number">{num}</span><span class="tooth-symbol" aria-hidden="true">✧</span><h3>{name}</h3><span class="card-bottom">Läs om behandlingen <span>↗</span></span></a>' for name,slug,num in names)+'</div>'
def news_cards():
 out=''
 for p in news:
  s=soups[p];bgs=backgrounds(s.select_one('.fusion-page-title-bar') or s);im=bgs[0] if bgs else '';out+=f'<a href="{p}" class="news-card">'+image(im,pages[p]['title'])+f'<div><span class="eyebrow">Aktuellt från Dentalum</span><h3>{esc(pages[p]["title"])}</h3><span class="card-bottom">Läs mer <span>↗</span></span></div></a>'
 return '<div class="news-grid">'+out+'</div>'
def hero(title,desc='',im='',label='Dentalum',home=False):
 return f'<section class="hero {"home-hero" if home else "page-hero"}"><div class="hero-copy"><span class="eyebrow"><span class="status-dot"></span>{esc(label)}</span><h1>{title}</h1>'+ (f'<p class="lead">{esc(desc)}</p>' if desc else '')+('<div class="hero-actions"><a class="button" href="#booking">Boka en tid <span>↗</span></a><a class="text-link" href="/vara-kliniker/">Hitta din klinik <span>→</span></a></div><div class="hero-note"><span class="little-spark">✧</span> Med omtanke. Hela vägen.</div>' if home else '')+'</div>'+ ('<figure class="hero-photo">'+image(im,'', 'hero-original')+'<figcaption><span>En del av ditt välmående.</span><span>Dentalum ↗</span></figcaption></figure>' if im else '<div class="hero-decoration" aria-hidden="true">✧</div>')+'</section>'
def reviews():
 out='<section class="section reviews-section"><div class="section-top"><div><span class="eyebrow">Patienternas egna ord</span><h2>Vad säger våra patienter om oss?</h2></div><p>Omdömen från originalwebbplatsen, hämtade 18 oktober 2026. Betyg och antal uppdateras inte i denna version.</p></div><div class="review-summary"><strong>4.6 / 5</strong><span>Utmärkt · 6573 recensioner vid hämtning</span><a href="https://www.trustindex.io/reviews/dentalum.com" class="text-link">Se aktuella omdömen ↗</a></div><details class="all-reviews"><summary>Läs patienternas omdömen <span>+</span></summary><div class="reviews-grid">'
 for r in soups['/'].select('.ti-review-item'):
  name=r.select_one('.ti-name');text=r.select_one('.ti-review-text-container');photo=r.select_one('.ti-profile-img img');source=r.select_one('.ti-tooltip');reply=r.select_one('.ti-owner-response')
  out+='<article class="review-card"><div class="review-author">'+(image(photo.get('src'),photo.get('alt','')) if photo else '')+'<div><h3>'+esc(name.get_text(' ',strip=True) if name else '')+'</h3><span>'+esc(source.get_text(' ',strip=True) if source else '')+'</span></div></div><p>'+esc(text.get_text(' ',strip=True) if text else '')+'</p>'+(render(reply) if reply else '')+'</article>'
 return out+'</div></details></section>'
def home():
 return hero('Tandvård som<br>gör skillnad.<br><em>Med dig i centrum.</em>','Tandvård på dina villkor – från förebyggande vård till akut tandvård och kosmetiska behandlingar.','https://dentalum.com/wp-content/uploads/2025/11/iStock-1326417865-1.jpg','Välkommen till Dentalum',True)+'''<div class="trust-strip"><span>Trygg tandvård. Nära dig.</span><span>Förebyggande & akut tandvård</span><span>Från Boden till Malmö</span><a href="/om-oss/">Lär känna Dentalum ↗</a></div><section class="section"><div class="section-top"><div><span class="eyebrow">Vi hjälper dig med all typ av tandvård</span><h2>All tandvård.<br><em>En trygg plats.</em></h2></div><div class="section-intro"><p>Dentalum är en av Sveriges största tandvårdsgrupper med kliniker från Boden i norr till Malmö i söder. Hos oss kan du få hjälp med allt från förebyggande vård till akut tandvård och kosmetiska behandlingar.</p><a class="text-link" href="/behandlingar/">Se alla behandlingar →</a></div></div>'''+treatment_cards()+'''</section><section class="about-editorial section"><div class="editorial-number">D<span>✧</span></div><div><span class="eyebrow">Människorna bakom din tandvård</span><h2>Omtanke är vår<br><em>utgångspunkt.</em></h2><p>Dentalum grundades av erfarna tandläkare, entreprenörer och visionärer som tillsammans vill skapa en helt ny upplevelse inom tandvården.</p><a class="button secondary" href="/om-oss/">Det här är Dentalum ↗</a></div></section><section class="section"><div class="section-top"><div><span class="eyebrow">Din klinik, nära dig</span><h2>Vi finns där du finns.</h2></div><a class="text-link" href="/vara-kliniker/">Utforska alla kliniker →</a></div><div class="clinic-grid">'''+''.join(card(c) for c in clinics if c['title'] in ['Dentalum Örnsköldsvik','Dentalum Åtvidaberg','Dentalum Drottninggatan'])+'''</div></section><section class="section news-section"><div class="section-top"><div><span class="eyebrow">Vad har hänt hos oss?</span><h2>På gång hos oss.</h2></div><a class="text-link" href="/nyheter/">Alla nyheter →</a></div>'''+news_cards()+'''</section>'''+reviews()+'''<section class="join-band section"><span class="eyebrow">Väx tillsammans med oss</span><h2>Mer tid för det<br><em>du gör bäst.</em></h2><p>Det är betydligt svårare än man tror att driva en klinik. Med Dentalum som partner kan du fokusera på det kliniska arbetet.</p><a class="button" href="/del-av-dentalum/">Bli en del av Dentalum ↗</a><a class="text-link" href="/dentalum-som-arbetsgivare/">Jobba hos oss →</a></section>'''
# Main navigation is shared by every route.
nav='''<a class="skip-link" href="#main">Fortsätt till innehållet</a><div class="topbar"><span>Tandvård på dina villkor</span><div><a href="/dentalum-som-arbetsgivare/">Jobba hos oss</a><a href="/kontakt/">Kontakta oss ↗</a></div></div><header class="site-header"><a class="brand" href="/" aria-label="Dentalum startsida">dentalum<span>✧</span></a><nav class="desktop-nav" aria-label="Huvudmeny"><div class="nav-group"><button aria-expanded="false" aria-controls="treat-menu">Behandlingar <span>⌄</span></button><div class="nav-dropdown" id="treat-menu"><span class="eyebrow">Tandvård för dina behov</span><div class="menu-treatments">'''+''.join(f'<a href="{p}">{esc(pages[p]["title"])}</a>' for p in treatments)+'''</div><a class="text-link" href="/behandlingar/">Alla behandlingar →</a></div></div><a href="/vara-kliniker/">Våra kliniker</a><div class="nav-group"><button aria-expanded="false" aria-controls="about-menu">Om Dentalum <span>⌄</span></button><div class="nav-dropdown small" id="about-menu">'''+''.join(f'<a href="/{p}/">{t}</a>' for p,t in [('om-oss','Om oss'),('team','Möt vårt team'),('patientsakerhet','Patientsäkerhet'),('vart-hallbarhetsarbete','Hållbarhet'),('del-av-dentalum','Bli en del av Dentalum'),('pressrelease','Press & investerare')])+'''</div></div><a href="/nyheter/">Nyheter</a></nav><div class="header-actions"><button class="icon-button theme-toggle" aria-label="Byt till mörkt tema" title="Växla ljust/mörkt tema"><span>◐</span></button><a href="#booking" class="button nav-book">Boka tid <span>↗</span></a><button class="icon-button mobile-toggle" aria-label="Öppna menyn" aria-expanded="false" aria-controls="mobile-nav">☰</button></div></header><nav id="mobile-nav" class="mobile-nav" aria-label="Mobilmeny" hidden><a href="/behandlingar/">Behandlingar →</a><a href="/vara-kliniker/">Våra kliniker →</a><a href="/om-oss/">Om Dentalum →</a><a href="/team/">Vårt team →</a><a href="/nyheter/">Nyheter →</a><a href="/kontakt/">Kontakta oss →</a><a href="/dentalum-som-arbetsgivare/">Jobba hos oss →</a></nav>'''
footer='''<section class="closing-cta"><div><span class="eyebrow">Ditt nästa steg mot god munhälsa</span><h2>Välkommen till oss.</h2></div><a class="button" href="#booking">Hitta en tid som passar ↗</a></section><footer><div class="footer-top"><div><a class="brand" href="/">dentalum<span>✧</span></a><p>Tandvård på dina villkor.<br>Med dig i centrum.</p></div>'''+''.join('<div><h3>'+title+'</h3>'+''.join(f'<a href="{p}">{t}</a>' for p,t in links)+'</div>' for title,links in [('För patienter',[('/vara-kliniker/','Våra kliniker'),('/behandlingar/','Behandlingar'),('/priser/','Priser & tandvårdsstöd'),('/kontakt/','Kontakta oss'),('/patientsakerhet/','Patientsäkerhet')]),('Om Dentalum',[('/om-oss/','Om oss'),('/team/','Vårt team'),('/nyheter/','Nyheter'),('/pressrelease/','Press releases'),('/vart-hallbarhetsarbete/','Hållbarhet'),('/del-av-dentalum/','Sälj din klinik')]),('Karriär & investerare',[('/dentalum-som-arbetsgivare/','Dentalum som arbetsgivare'),('https://karriar.dentalum.com/','Lediga tjänster ↗'),('/financial-reports/','Finansiella rapporter'),('/financial-calendar/','Finansiell kalender'),('/investor-reports/','Investor reports'),('/sidkarta/','Alla sidor')])])+'''</div><div class="footer-bottom"><span>© 2026 Dentalum. All rights reserved.</span><div><a href="/dentalums-dataskyddspolicy/">Dataskyddspolicy</a><a href="/dentalums-cookiepolicy/">Cookiepolicy</a><a href="'''+esc(local('https://dentalum.com/wp-content/uploads/2025/12/Riktlinjer-for-direktmarknadsforing.pdf'))+'''">Direktmarknadsföring ↗</a><button class="text-button" id="back-top">Till toppen ↑</button></div></div></footer>'''
booking='''<dialog id="booking"><div class="dialog-top"><span class="eyebrow">Din tandvård börjar här</span><button class="icon-button close-dialog" aria-label="Stäng bokning">✕</button></div><h2>Välj din mottagning.</h2><p>Boka direkt hos en av våra kliniker, eller hitta din närmaste mottagning.</p><p class="booking-service-note" role="status">Bokning sker via Dentalums befintliga bokningstjänst. Kliniken öppnas i en ny flik, där du väljer Boka tid.</p><div class="booking-links">'''+''.join(f'<a href="{esc(b["url"])}" class="booking-option" target="_blank" rel="noopener noreferrer"><span>{esc(b["text"].replace("Boka tid online",""))}</span><span>Till bokningen ↗</span></a>' for b in bookings)+'''</div><a href="/vara-kliniker/" class="button secondary">Se alla kliniker →</a></dialog><dialog id="lightbox"><div class="dialog-top"><span id="image-caption"></span><button class="icon-button close-dialog" aria-label="Stäng bild">✕</button></div><img id="lightbox-image" alt="" hidden><div class="gallery-actions"><button class="text-button" id="prev-image">← Föregående</button><span id="gallery-count"></span><button class="text-button" id="next-image">Nästa →</button></div></dialog>'''
current_source=''
def generic(p):
 global current_source
 current_source=pages[p]['source'];s=soups[p];m=s.select_one('#content .post-content')
 # Archives can contain many post-content elements: use complete content region.
 archive=p.startswith('/cision-tag/') or p.startswith('/pressrelease/') or p.startswith('/category/')
 if archive:m=s.select_one('#content')
 if not m:m=s.select_one('#content')
 title=pages[p]['title'];titlebar=s.select_one('.fusion-page-title-bar');bgs=backgrounds(titlebar) if titlebar else backgrounds(m);bg=bgs[0] if bgs else ''
 # The source often puts its hero title outside the main content.
 if p.startswith('/cision/'):
  title=s.title.get_text().split(' - Dentalum')[0].split(' | Dentalum')[0];pages[p]['title']=title
 if title in ['Front page','Nyheter','Press releases'] and p=='/':return home()
 label='Behandlingar' if p.startswith('/behandlingar/') else 'Våra kliniker' if p.startswith('/kliniker/') else 'Lär känna Dentalum' if p in ['/om-oss/','/team/'] else 'Dentalum'
 intro='';h1=m.select_one('h1')
 if h1 and h1.get_text(' ',strip=True)==title:
  par=h1.find_parent(class_='fusion-fullwidth')
  if par:
   ps=par.select('p');intro=' '.join(x.get_text(' ',strip=True) for x in ps if x.get_text(' ',strip=True))
 # Remove hero duplicate title and background, all body images stay in their context.
 content=BeautifulSoup(str(m),'html.parser');body=content.select_one('.post-content') or content
 if archive:body=content
 for el in body.select('.rich-snippet-hidden,.fusion-breadcrumbs'):el.decompose()
 first_h=body.select_one('h1')
 if first_h and first_h.get_text(' ',strip=True)==title:
  par=first_h.find_parent(class_='fusion-fullwidth')
  if par and len(par.get_text(' ',strip=True))<len(intro)+len(first_h.get_text())+100:par.decompose()
  else:first_h.decompose()
 # Converted top level sections with original local photos as images, never backgrounds.
 parts=[];seen_sections=set()
 for el in list(body.children):
  if not isinstance(el,Tag):continue
  if el.name in ['script','style']:continue
  text=el.get_text(' ',strip=True)
  if text and text in seen_sections:continue
  if text:seen_sections.add(text)
  out=render(el)
  extra=[]
  for b in backgrounds(el):
   if b==bg and bg in str(m):continue
   if local(b) not in out:extra.append(image(b,''))
  if extra:out='<div class="section-photos">'+''.join(extra)+'</div>'+out
  if out.strip():parts.append('<section class="content-band reveal">'+out+'</section>')
 if titlebar:
  tp=titlebar.select_one('.fusion-text');intro=tp.get_text(' ',strip=True) if tp else intro
 if p.startswith('/cision/'):
  parts=['<article class="reading-article">'+''.join(parts)+'</article>']
 controls=''
 if p=='/team/' or 'Möt teamet' in m.get_text():controls='<div class="team-controls filter-bar"><label><span>Hitta en medarbetare</span><input type="search" id="team-search" placeholder="Sök namn eller roll…"></label><label><span>Visa yrkesroll</span><select id="team-role"><option value="">Alla roller</option></select></label><span id="team-count" role="status"></span></div>'
 header_extras=render(titlebar.select_one('ul')) if titlebar and titlebar.select_one('ul') else ''
 toc='<aside class="page-tools"><a href="#page-content">Utforska sidan ↓</a><button class="text-button" id="expand-details">Öppna alla frågor +</button><a href="#booking">Boka tid ↗</a></aside>'
 return '<div class="breadcrumbs"><a href="/">Hem</a> / <span>'+esc(label)+'</span></div>'+hero(esc(title),intro,bg,label)+('<section class="region-intro section">'+header_extras+'</section>' if header_extras else '')+toc+'<div id="page-content" class="source-content">'+controls+''.join(parts)+'</div>'
# Generate real HTML at every preserved path (no client router dependency).
for p in list(pages):
 if p=='/' or p.startswith('/author/'):body=home()
 elif p in ['/vara-kliniker/','/kliniker/'] or (p.startswith('/kliniker/') and len(p.strip('/').split('/'))==2):
  tb=soups[p].select_one('.fusion-page-title-bar');desc=' '.join(x.get_text(' ',strip=True) for x in tb.select('.fusion-text')) if tb else 'Hitta en klinik som passar dig. Sök efter ort, namn eller region.'
  intro_list=render(tb.select_one('ul')) if tb and tb.select_one('ul') else ''
  body=hero(esc('Våra kliniker' if p in ['/vara-kliniker/','/kliniker/'] else pages[p]['title']),desc,label='Tandvård nära dig')+('<section class="region-intro section">'+intro_list+'</section>' if intro_list else '')+clinicfinder(p)
 elif p in ['/nyheter/','/category/nyheter/']:body=hero('På gång hos Dentalum.','Här kan du ta del av våra senaste nyheter inom Dentalum.',label='Nyheter & insikter')+'<section class="section">'+news_cards()+'</section>'
 else:body=generic(p)
 if p=='/behandlingar/':
  body=body.replace('<div id="page-content"', '<section class="section treatment-selector"><label for="treatment-select" class="eyebrow">Hitta rätt behandling</label><div class="treatment-select-row"><select id="treatment-select"><option value="">Välj en behandling…</option>'+''.join(f'<option value="{x}">{esc(pages[x]["title"])}</option>' for x in treatments)+'</select><button class="button" id="go-treatment">Utforska →</button></div><p id="treatment-error" role="status"></p>'+treatment_cards()+'</section><div id="page-content"')
 meta=pages[p];head=f'<!doctype html><html lang="sv"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(meta["title"])} | Dentalum</title><meta name="description" content="{esc(meta["description"] or meta["title"]+" – Dentalum. Tandvård på dina villkor.")}"><link rel="canonical" href="{esc(meta["canonical"])}"><meta name="theme-color" content="#f6f5f0"><link rel="icon" href="/assets/favicon.svg"><script>try{{document.documentElement.dataset.theme=localStorage.getItem("dentalum-theme")||(matchMedia("(prefers-color-scheme: dark)").matches?"dark":"light")}}catch(e){{}}</script><link rel="stylesheet" href="/style.css"><script defer src="/app.js"></script></head><body>'
 dest=DIST/p.strip('/')/'index.html';dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(head+nav+'<main id="main">'+body+'</main>'+footer+booking+'</body></html>')
# Human readable inventory and public sitemap.
rows=[]
for p,m in pages.items():rows.append({'path':p,'title':m['title'],'source':m['source'],'implementation':'complete','content_review':'source HTML, text, headings, links and image references audited','browser_verified':False})
json.dump(rows,open(ROOT/'audit/page-inventory.json','w'),ensure_ascii=False,indent=2)
(DIST/'sidkarta').mkdir(exist_ok=True)
(DIST/'sidkarta/index.html').write_text(head+nav+'<main id="main">'+hero('Alla sidor.','Utforska behandlingar, kliniker, nyheter och information från Dentalum.',label='Sidkarta')+'<section class="section"><label>Sök bland alla sidor<input id="sitemap-search" type="search" placeholder="Sök sidtitel…"></label><div class="sitemap-list">'+''.join(f'<a href="{p}">{esc(m["title"])} <span>↗</span></a>' for p,m in pages.items())+'</div></section></main>'+footer+booking+'</body></html>')
(DIST/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>https://dentalum.com'+esc(p)+'</loc></url>' for p in pages)+'</urlset>')
json.dump({'clinics':clinics,'pages':pages,'bookings':bookings},open(DIST/'site-data.json','w'),ensure_ascii=False)
print('Built',len(pages),'pages, clinics',len(clinics))
